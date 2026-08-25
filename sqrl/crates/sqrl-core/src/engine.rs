//! `EngineCore`: the sans-executor durable-execution engine.
//!
//! One `EngineCore` owns one shard: its workflows, their journals (via an
//! exclusively-owned [`StorageShard`]), its timer wheel, and its group-commit
//! state. It contains **no threads, no wall clock, no ambient entropy**: a
//! driver (the deterministic simulator or the real thread-per-core
//! scheduler) feeds it commands, calls [`EngineCore::tick`], executes the
//! step futures it emits, and feeds results back. The same engine code
//! therefore runs identically under simulation and in production — the
//! foundation of sqrl's deterministic simulation testing.
//!
//! ## The revelation rule
//!
//! Every outcome (step result, timer fire, signal arrival) reaches
//! orchestration code through an ordered *revelation queue*, one outcome per
//! poll, in journal order — including during live execution. A live run is
//! thus a replay of its own journal as it forms, which makes
//! `select!`-style races deterministic across crash/recovery.

use crate::config::{EngineConfig, FsyncPolicy};
use crate::ctx::Ctx;
use crate::error::{Error, Rejected, StepError, StorageError};
use crate::event::{JournalEvent, JournalRecord};
use crate::handle::TerminalResult;
use crate::id::WorkflowId;
use crate::inject::{Clock, Entropy};
use crate::instance::{BoxStepFut, InstanceInner, Resolution, StepClosure, StepReg, Waiting};
use crate::registry::{Registry, WorkflowFut};
use crate::snapshot::{
    InflightStep, Outcome, SnapshotBody, SnapshotMeta, SnapshotRecord, StartInfo, TerminalStatus,
};
use crate::state::{FailureKind, StateKind, WorkflowState};
use crate::storage::{AppendEntry, AppendPayload, JournalReadout, StorageShard, StorageStats};
use crate::sync::Completer;
use crate::time::LogicalTime;
use std::cell::RefCell;
use std::collections::{BTreeMap, BTreeSet, VecDeque};
use std::panic::{catch_unwind, AssertUnwindSafe};
use std::pin::Pin;
use std::rc::Rc;
use std::sync::Arc;
use std::task::{Context as TaskContext, Poll, Waker};

/// Commands a driver feeds into an engine core. All variants are `Send`.
pub enum EngineCmd {
    /// Start a new workflow.
    Start {
        /// Unique workflow id.
        id: WorkflowId,
        /// Registered workflow name.
        name: String,
        /// Serialized input.
        input: Vec<u8>,
        /// Admission reply (backpressure, duplicate id, unknown name).
        admit: Completer<Result<(), Rejected>>,
        /// Terminal-result watcher (resolves when durable).
        terminal: Completer<TerminalResult>,
    },
    /// Deliver an external signal.
    Signal {
        /// Target workflow.
        id: WorkflowId,
        /// Signal name.
        name: String,
        /// Serialized payload.
        payload: Vec<u8>,
        /// Acknowledgement.
        ack: Completer<Result<(), Error>>,
    },
    /// Cancel a workflow.
    Cancel {
        /// Target workflow.
        id: WorkflowId,
        /// Acknowledgement.
        ack: Completer<Result<(), Error>>,
    },
    /// Attach a terminal watcher to an existing workflow.
    Watch {
        /// Target workflow.
        id: WorkflowId,
        /// Watcher completed with the terminal result (immediately if the
        /// workflow is already terminal).
        terminal: Completer<TerminalResult>,
        /// Whether the workflow was found.
        ack: Completer<Result<(), Error>>,
    },
    /// A dispatched step finished (driver-supplied).
    StepFinished {
        /// Workflow the step belongs to.
        id: WorkflowId,
        /// Command seq of the step.
        seq: u64,
        /// Attempt number that finished.
        attempt: u32,
        /// Serialized result or step error.
        outcome: Result<Vec<u8>, StepError>,
    },
    /// Report status of all workflows on this shard.
    Status {
        /// Reply channel.
        reply: Completer<Vec<StatusEntry>>,
    },
    /// Report engine + storage counters for this shard.
    Metrics {
        /// Reply channel.
        reply: Completer<(EngineMetrics, StorageStats)>,
    },
    /// No-op; forces a tick.
    Tick,
    /// Flush, sync, and stop accepting work.
    Shutdown,
}

impl EngineCmd {
    /// The workflow id this command routes on (None for shard-wide ops).
    pub fn workflow(&self) -> Option<&WorkflowId> {
        match self {
            EngineCmd::Start { id, .. }
            | EngineCmd::Signal { id, .. }
            | EngineCmd::Cancel { id, .. }
            | EngineCmd::Watch { id, .. }
            | EngineCmd::StepFinished { id, .. } => Some(id),
            EngineCmd::Status { .. }
            | EngineCmd::Metrics { .. }
            | EngineCmd::Tick
            | EngineCmd::Shutdown => None,
        }
    }
}

/// A driver: routes commands to engine shards. Implemented by the
/// deterministic `SimScheduler` (sqrl-sim) and the thread-per-core
/// `RealScheduler` (sqrl facade).
pub trait Scheduler {
    /// Number of shards.
    fn num_shards(&self) -> usize;
    /// Route a command to the right shard and wake it.
    fn submit(&self, cmd: EngineCmd);
}

/// One line of `Status` output.
#[derive(Debug, Clone)]
pub struct StatusEntry {
    /// Workflow id.
    pub id: WorkflowId,
    /// Registered name (empty when unknown/passivated without cache).
    pub name: String,
    /// Lifecycle state.
    pub state: StateKind,
    /// Failure description if failed.
    pub failure: Option<String>,
    /// Journal records so far. **0 for passivated or terminal workflows** —
    /// their journals are not held in memory; use `sqrl inspect` (CLI) for
    /// persisted counts.
    pub records: u64,
    /// Whether the instance is passivated.
    pub passivated: bool,
}

/// A step the driver must execute on the step pool. The future is already
/// panic-proof: panics inside the step surface as `StepError::Panic`.
pub struct StepDispatch {
    /// Workflow the step belongs to.
    pub workflow: WorkflowId,
    /// Command seq of the step.
    pub seq: u64,
    /// Attempt number (1-based).
    pub attempt: u32,
    /// The step future.
    pub fut: BoxStepFut,
}

/// Output of one engine tick.
#[derive(Default)]
pub struct TickOutput {
    /// Steps to execute on the step pool.
    pub dispatches: Vec<StepDispatch>,
    /// When the engine next needs a tick even if no external event arrives
    /// (timer deadline or fsync deadline). `None` = fully idle.
    pub next_wake: Option<LogicalTime>,
}

/// Engine counters (per shard).
#[derive(Debug, Default, Clone, Copy, PartialEq, Eq)]
#[allow(missing_docs)]
pub struct EngineMetrics {
    pub starts: u64,
    pub completions: u64,
    pub failures: u64,
    pub cancellations: u64,
    pub backpressure_rejections: u64,
    pub step_dispatches: u64,
    pub step_retries: u64,
    pub timers_fired: u64,
    pub signals_delivered: u64,
    pub snapshots_taken: u64,
    pub passivations: u64,
    pub reactivations: u64,
    pub nd_failures: u64,
    pub illegal_transitions: u64,
    pub records_appended: u64,
}

// ---------------------------------------------------------------------------
// Internal instance representation
// ---------------------------------------------------------------------------

#[derive(Debug, Clone)]
enum Reveal {
    StepOk {
        seq: u64,
        bytes: Vec<u8>,
        at: LogicalTime,
    },
    StepErr {
        seq: u64,
        error: StepError,
        attempts: u32,
        at: LogicalTime,
    },
    Timer {
        seq: u64,
        at: LogicalTime,
    },
    Signal {
        name: String,
        payload: Vec<u8>,
        at: LogicalTime,
    },
    Resumed {
        at: LogicalTime,
    },
}

struct QueuedReveal {
    reveal: Reveal,
    from_history: bool,
}

#[derive(Default)]
struct StepRuntime {
    name: String,
    opts: crate::config::StepOptions,
    closure: Option<StepClosure>,
    failed_attempts: u32,
    dispatched_attempt: Option<u32>,
    pending_retry: Option<LogicalTime>,
}

struct Instance {
    cell: Rc<RefCell<InstanceInner>>,
    fut: Option<WorkflowFut>,
    state: WorkflowState,
    reveals: VecDeque<QueuedReveal>,
    resolved_in_history: BTreeSet<u64>,
    steps: BTreeMap<u64, StepRuntime>,
    pending_timers: BTreeMap<u64, LogicalTime>,
    record_index: u64,
    records_since_snapshot: u64,
    outcome_log: Vec<Outcome>,
    start: StartInfo,
    watchers: Vec<Completer<TerminalResult>>,
    last_activity: LogicalTime,
    terminal_value: Option<TerminalResult>,
    terminal_acked: bool,
}

struct PassiveInfo {
    name: String,
    state_hint: StateKind,
    watchers: Vec<Completer<TerminalResult>>,
}

struct TerminalInfo {
    name: String,
    state: StateKind,
    failure: Option<String>,
    result: TerminalResult,
}

enum Slot {
    Active(Box<Instance>),
    Passive(PassiveInfo),
    Terminal(TerminalInfo),
}

enum TimerEntry {
    WorkflowTimer { wf: WorkflowId, seq: u64 },
    RetryStep { wf: WorkflowId, seq: u64 },
}

enum PendingAck {
    Terminal {
        wf: WorkflowId,
        result: TerminalResult,
    },
    StrictReveal {
        wf: WorkflowId,
        reveal: Reveal,
    },
}

// ---------------------------------------------------------------------------
// EngineCore
// ---------------------------------------------------------------------------

/// The engine core for one shard. `!Send` (it owns `!Send` workflow
/// futures); construct it on the thread that will drive it.
pub struct EngineCore {
    shard: usize,
    registry: Arc<Registry>,
    storage: Box<dyn StorageShard>,
    clock: Arc<dyn Clock>,
    entropy: Arc<dyn Entropy>,
    config: EngineConfig,
    cmds: VecDeque<EngineCmd>,
    instances: BTreeMap<WorkflowId, Slot>,
    active_count: usize,
    run_queue: VecDeque<WorkflowId>,
    runnable: BTreeSet<WorkflowId>,
    timers: BTreeMap<(LogicalTime, u64), TimerEntry>,
    timer_counter: u64,
    append_buf: Vec<AppendEntry>,
    unsynced_records: usize,
    unsynced_since: Option<LogicalTime>,
    last_sync_at: LogicalTime,
    force_sync: bool,
    pending_acks: Vec<PendingAck>,
    dispatches: Vec<StepDispatch>,
    storage_failed: Option<StorageError>,
    shutdown: bool,
    last_sweep: LogicalTime,
    metrics: EngineMetrics,
}

impl EngineCore {
    /// Open a shard: load every workflow from storage, queueing every
    /// non-terminal one for recovery replay (performed on the next ticks).
    pub fn open(
        shard: usize,
        registry: Arc<Registry>,
        mut storage: Box<dyn StorageShard>,
        clock: Arc<dyn Clock>,
        entropy: Arc<dyn Entropy>,
        config: EngineConfig,
    ) -> Result<Self, StorageError> {
        let now = clock.now();
        let ids = storage.list()?;
        let mut engine = EngineCore {
            shard,
            registry,
            storage,
            clock,
            entropy,
            config,
            cmds: VecDeque::new(),
            instances: BTreeMap::new(),
            active_count: 0,
            run_queue: VecDeque::new(),
            runnable: BTreeSet::new(),
            timers: BTreeMap::new(),
            timer_counter: 0,
            append_buf: Vec::new(),
            unsynced_records: 0,
            unsynced_since: None,
            last_sync_at: now,
            force_sync: false,
            pending_acks: Vec::new(),
            dispatches: Vec::new(),
            storage_failed: None,
            shutdown: false,
            last_sweep: LogicalTime::ZERO,
            metrics: EngineMetrics::default(),
        };
        for id in ids {
            let readout = engine.storage.read(&id)?;
            engine.install_loaded(id, readout, now);
        }
        Ok(engine)
    }

    /// This shard's index.
    pub fn shard(&self) -> usize {
        self.shard
    }

    /// Engine counters.
    pub fn metrics(&self) -> EngineMetrics {
        self.metrics
    }

    /// Storage counters.
    pub fn storage_stats(&self) -> StorageStats {
        self.storage.stats()
    }

    /// Whether storage has failed permanently (disk error).
    pub fn storage_error(&self) -> Option<&StorageError> {
        self.storage_failed.as_ref()
    }

    /// Number of live (non-terminal, in-memory) workflows.
    pub fn active_workflows(&self) -> usize {
        self.active_count
    }

    /// Queue a command; call [`EngineCore::tick`] to process.
    pub fn submit(&mut self, cmd: EngineCmd) {
        self.cmds.push_back(cmd);
    }

    /// Lifecycle states of all workflows (tests/status).
    pub fn states(&self) -> BTreeMap<WorkflowId, StateKind> {
        self.instances
            .iter()
            .map(|(id, slot)| {
                let k = match slot {
                    Slot::Active(inst) => inst.state.kind(),
                    Slot::Passive(p) => p.state_hint,
                    Slot::Terminal(t) => t.state,
                };
                (id.clone(), k)
            })
            .collect()
    }

    /// Process queued commands, due timers, activations, and group commit.
    /// Returns step dispatches for the driver plus the next wake deadline.
    pub fn tick(&mut self) -> TickOutput {
        let now = self.clock.now();
        loop {
            let mut progressed = false;
            while let Some(cmd) = self.cmds.pop_front() {
                progressed = true;
                self.handle_cmd(cmd, now);
            }
            progressed |= self.fire_due_timers(now);
            while let Some(id) = self.run_queue.pop_front() {
                self.runnable.remove(&id);
                progressed = true;
                self.activate(&id, now);
            }
            self.flush(now);
            if !progressed && self.run_queue.is_empty() && self.cmds.is_empty() {
                break;
            }
            if self.run_queue.is_empty() && self.cmds.is_empty() && !self.timers_due(now) {
                break;
            }
        }
        self.sweep_passivation(now);
        if self.shutdown && self.storage_failed.is_none() {
            // Final housekeeping so a clean shutdown leaves the smallest
            // possible store (quiescence snapshots make old segments dead).
            if let Err(e) = self.storage.maintain() {
                tracing::warn!(error = %e, "shutdown maintenance failed");
            }
        }
        TickOutput {
            dispatches: std::mem::take(&mut self.dispatches),
            next_wake: self.next_wake(now),
        }
    }

    fn timers_due(&self, now: LogicalTime) -> bool {
        self.timers
            .keys()
            .next()
            .map(|(t, _)| *t <= now)
            .unwrap_or(false)
    }

    fn next_wake(&self, now: LogicalTime) -> Option<LogicalTime> {
        let mut wake: Option<LogicalTime> = None;
        let mut consider = |t: LogicalTime| {
            wake = Some(wake.map_or(t, |w: LogicalTime| w.min(t)));
        };
        if let Some((t, _)) = self.timers.keys().next() {
            consider(*t);
        }
        if self.unsynced_records > 0 {
            match self.config.fsync {
                FsyncPolicy::Strict => consider(now),
                FsyncPolicy::Group { max_delay, .. } => {
                    consider(self.unsynced_since.unwrap_or(now) + max_delay)
                }
                FsyncPolicy::Relaxed { interval } => consider(self.last_sync_at + interval),
            }
        }
        if !self.run_queue.is_empty() || !self.cmds.is_empty() {
            consider(now);
        }
        wake
    }

    // -- command handling ---------------------------------------------------

    fn handle_cmd(&mut self, cmd: EngineCmd, now: LogicalTime) {
        match cmd {
            EngineCmd::Start {
                id,
                name,
                input,
                admit,
                terminal,
            } => self.handle_start(id, name, input, admit, terminal, now),
            EngineCmd::Signal {
                id,
                name,
                payload,
                ack,
            } => self.handle_signal(id, name, payload, ack, now),
            EngineCmd::Cancel { id, ack } => self.handle_cancel(id, ack, now),
            EngineCmd::Watch { id, terminal, ack } => match self.instances.get_mut(&id) {
                Some(Slot::Terminal(t)) => {
                    terminal.complete(t.result.clone());
                    ack.complete(Ok(()));
                }
                Some(Slot::Active(inst)) => {
                    if let (Some(res), true) = (&inst.terminal_value, inst.terminal_acked) {
                        terminal.complete(res.clone());
                    } else {
                        inst.watchers.push(terminal);
                    }
                    ack.complete(Ok(()));
                }
                Some(Slot::Passive(p)) => {
                    p.watchers.push(terminal);
                    ack.complete(Ok(()));
                }
                None => {
                    ack.complete(Err(Error::App(format!("unknown workflow `{id}`"))));
                }
            },
            EngineCmd::StepFinished {
                id,
                seq,
                attempt,
                outcome,
            } => self.handle_step_finished(id, seq, attempt, outcome, now),
            EngineCmd::Status { reply } => {
                let entries = self
                    .instances
                    .iter()
                    .map(|(id, slot)| match slot {
                        Slot::Active(inst) => StatusEntry {
                            id: id.clone(),
                            name: inst.start.name.clone(),
                            state: inst.state.kind(),
                            failure: match &inst.state {
                                WorkflowState::Failed(f) => Some(f.to_error().to_string()),
                                _ => None,
                            },
                            records: inst.record_index,
                            passivated: false,
                        },
                        Slot::Passive(p) => StatusEntry {
                            id: id.clone(),
                            name: p.name.clone(),
                            state: p.state_hint,
                            failure: None,
                            records: 0,
                            passivated: true,
                        },
                        Slot::Terminal(t) => StatusEntry {
                            id: id.clone(),
                            name: t.name.clone(),
                            state: t.state,
                            failure: t.failure.clone(),
                            records: 0,
                            passivated: false,
                        },
                    })
                    .collect();
                reply.complete(entries);
            }
            EngineCmd::Metrics { reply } => {
                reply.complete((self.metrics, self.storage.stats()));
            }
            EngineCmd::Tick => {}
            EngineCmd::Shutdown => {
                self.shutdown = true;
                self.snapshot_quiescent(now);
                self.force_sync = true;
            }
        }
    }

    fn handle_start(
        &mut self,
        id: WorkflowId,
        name: String,
        input: Vec<u8>,
        admit: Completer<Result<(), Rejected>>,
        terminal: Completer<TerminalResult>,
        now: LogicalTime,
    ) {
        if self.shutdown || self.storage_failed.is_some() {
            admit.complete(Err(Rejected::Unavailable(
                self.storage_failed
                    .as_ref()
                    .map(|e| e.to_string())
                    .unwrap_or_else(|| "engine shutting down".to_string()),
            )));
            return;
        }
        if self.instances.contains_key(&id) {
            admit.complete(Err(Rejected::AlreadyExists(id.to_string())));
            return;
        }
        let Some(def) = self.registry.get(&name) else {
            admit.complete(Err(Rejected::UnknownWorkflowName(name)));
            return;
        };
        if self.active_count >= self.config.max_active_per_shard {
            self.metrics.backpressure_rejections += 1;
            admit.complete(Err(Rejected::Backpressure {
                shard: self.shard,
                limit: self.config.max_active_per_shard,
            }));
            return;
        }
        if input.len() > self.config.max_payload {
            admit.complete(Err(Rejected::Invalid(
                Error::PayloadTooLarge {
                    size: input.len(),
                    limit: self.config.max_payload,
                    context: "workflow input".to_string(),
                }
                .to_string(),
            )));
            return;
        }
        let seed = self.entropy.next_u64();
        let version = def.version;
        let start = StartInfo {
            name: name.clone(),
            version,
            input: input.clone(),
            seed,
            started_at: now,
        };
        let cell = Rc::new(RefCell::new(InstanceInner::new(
            id.clone(),
            name.clone(),
            version,
            seed,
            self.config.max_payload,
            self.config.retry.clone(),
            now,
        )));
        let fut = (def.factory)(Ctx::from_cell(Rc::clone(&cell)), input.clone());
        let mut inst = Box::new(Instance {
            cell,
            fut: Some(fut),
            state: WorkflowState::Pending,
            reveals: VecDeque::new(),
            resolved_in_history: BTreeSet::new(),
            steps: BTreeMap::new(),
            pending_timers: BTreeMap::new(),
            record_index: 0,
            records_since_snapshot: 0,
            outcome_log: Vec::new(),
            start,
            watchers: vec![terminal],
            last_activity: now,
            terminal_value: None,
            terminal_acked: false,
        });
        self.append_event(
            &id,
            &mut inst,
            JournalEvent::WorkflowStarted {
                name,
                version,
                input,
                seed,
            },
            now,
        );
        self.instances.insert(id.clone(), Slot::Active(inst));
        self.active_count += 1;
        self.metrics.starts += 1;
        tracing::info!(workflow = %id, shard = self.shard, "workflow started");
        self.queue_runnable(&id);
        admit.complete(Ok(()));
    }

    fn handle_signal(
        &mut self,
        id: WorkflowId,
        name: String,
        payload: Vec<u8>,
        ack: Completer<Result<(), Error>>,
        now: LogicalTime,
    ) {
        if payload.len() > self.config.max_payload {
            ack.complete(Err(Error::PayloadTooLarge {
                size: payload.len(),
                limit: self.config.max_payload,
                context: "signal payload".to_string(),
            }));
            return;
        }
        if matches!(self.instances.get(&id), Some(Slot::Passive(_))) {
            if let Err(e) = self.reactivate(&id, now) {
                ack.complete(Err(Error::Storage(e)));
                return;
            }
        }
        match self.instances.remove(&id) {
            Some(Slot::Active(mut inst)) => {
                if inst.state.is_terminal() {
                    self.instances.insert(id, Slot::Active(inst));
                    ack.complete(Err(Error::App("workflow is terminal".to_string())));
                    return;
                }
                self.append_event(
                    &id,
                    &mut inst,
                    JournalEvent::SignalReceived {
                        name: name.clone(),
                        payload: payload.clone(),
                    },
                    now,
                );
                inst.reveals.push_back(QueuedReveal {
                    reveal: Reveal::Signal {
                        name,
                        payload,
                        at: now,
                    },
                    from_history: false,
                });
                inst.last_activity = now;
                self.metrics.signals_delivered += 1;
                self.instances.insert(id.clone(), Slot::Active(inst));
                self.queue_runnable(&id);
                ack.complete(Ok(()));
            }
            Some(slot @ Slot::Terminal(_)) => {
                self.instances.insert(id, slot);
                ack.complete(Err(Error::App("workflow is terminal".to_string())));
            }
            Some(slot @ Slot::Passive(_)) => {
                // reactivate() above failed only via a storage error path.
                self.instances.insert(id, slot);
                ack.complete(Err(Error::App("workflow unavailable".to_string())));
            }
            None => {
                ack.complete(Err(Error::App(format!("unknown workflow `{id}`"))));
            }
        }
    }

    fn handle_cancel(
        &mut self,
        id: WorkflowId,
        ack: Completer<Result<(), Error>>,
        now: LogicalTime,
    ) {
        match self.instances.remove(&id) {
            Some(Slot::Active(mut inst)) => {
                if inst.state.is_terminal() {
                    self.instances.insert(id, Slot::Active(inst));
                    ack.complete(Err(Error::App("workflow is terminal".to_string())));
                    return;
                }
                self.append_event(&id, &mut inst, JournalEvent::WorkflowCancelled, now);
                self.set_state(&mut inst, WorkflowState::Cancelled);
                inst.fut = None;
                inst.terminal_value = Some(Err(Error::Cancelled));
                self.pending_acks.push(PendingAck::Terminal {
                    wf: id.clone(),
                    result: Err(Error::Cancelled),
                });
                // Terminal snapshot lets old segments be reclaimed.
                self.append_terminal_snapshot(&id, &mut inst, TerminalStatus::Cancelled);
                self.metrics.cancellations += 1;
                self.instances.insert(id, Slot::Active(inst));
                ack.complete(Ok(()));
            }
            Some(Slot::Passive(p)) => {
                // Cancelling needs a journaled WorkflowCancelled with a
                // correct record index, so reactivate first.
                self.instances.insert(id.clone(), Slot::Passive(p));
                if self.reactivate(&id, now).is_ok() {
                    self.handle_cancel(id, ack, now);
                } else {
                    ack.complete(Err(Error::App("workflow unavailable".to_string())));
                }
            }
            Some(Slot::Terminal(t)) => {
                self.instances.insert(id, Slot::Terminal(t));
                ack.complete(Err(Error::App("workflow is terminal".to_string())));
            }
            None => {
                ack.complete(Err(Error::App(format!("unknown workflow `{id}`"))));
            }
        }
    }

    fn handle_step_finished(
        &mut self,
        id: WorkflowId,
        seq: u64,
        attempt: u32,
        outcome: Result<Vec<u8>, StepError>,
        now: LogicalTime,
    ) {
        let Some(Slot::Active(mut inst)) = self.instances.remove(&id) else {
            // Passivated/terminal/unknown: result is stale; drop it. (We never
            // passivate with dispatched steps, so this only happens after
            // cancel/failure.)
            return;
        };
        if inst.state.is_terminal() {
            self.instances.insert(id, Slot::Active(inst));
            return;
        }
        let strict = match inst.steps.get_mut(&seq) {
            Some(meta) if meta.dispatched_attempt == Some(attempt) => {
                meta.dispatched_attempt = None;
                meta.opts.fsync_strict
            }
            _ => {
                // Stale (retried elsewhere) or unknown: drop the result.
                self.instances.insert(id, Slot::Active(inst));
                return;
            }
        };
        match outcome {
            Ok(bytes) => {
                self.append_event(
                    &id,
                    &mut inst,
                    JournalEvent::StepCompleted {
                        seq,
                        result: bytes.clone(),
                    },
                    now,
                );
                let reveal = Reveal::StepOk {
                    seq,
                    bytes,
                    at: now,
                };
                if strict {
                    self.pending_acks.push(PendingAck::StrictReveal {
                        wf: id.clone(),
                        reveal,
                    });
                    self.force_sync = true;
                } else {
                    inst.reveals.push_back(QueuedReveal {
                        reveal,
                        from_history: false,
                    });
                    self.queue_runnable(&id);
                }
            }
            Err(step_err) => {
                let (attempts, policy) = match inst.steps.get_mut(&seq) {
                    Some(meta) => {
                        meta.failed_attempts += 1;
                        (
                            meta.failed_attempts,
                            meta.opts
                                .retry
                                .clone()
                                .unwrap_or_else(|| self.config.retry.clone()),
                        )
                    }
                    None => {
                        self.instances.insert(id, Slot::Active(inst));
                        return;
                    }
                };
                let seed = inst.cell.borrow().seed;
                if step_err.is_retryable() && policy.allows_retry(attempts) {
                    let delay = policy.delay_for(attempts, seed, seq);
                    let retry_at = now + delay;
                    self.append_event(
                        &id,
                        &mut inst,
                        JournalEvent::StepFailed {
                            seq,
                            error: step_err,
                            attempt: attempts,
                            retry_at: Some(retry_at),
                        },
                        now,
                    );
                    if let Some(meta) = inst.steps.get_mut(&seq) {
                        meta.pending_retry = Some(retry_at);
                    }
                    self.arm_engine_timer(
                        retry_at,
                        TimerEntry::RetryStep {
                            wf: id.clone(),
                            seq,
                        },
                    );
                    self.metrics.step_retries += 1;
                } else {
                    self.append_event(
                        &id,
                        &mut inst,
                        JournalEvent::StepFailed {
                            seq,
                            error: step_err.clone(),
                            attempt: attempts,
                            retry_at: None,
                        },
                        now,
                    );
                    let reveal = Reveal::StepErr {
                        seq,
                        error: step_err,
                        attempts,
                        at: now,
                    };
                    if strict {
                        self.pending_acks.push(PendingAck::StrictReveal {
                            wf: id.clone(),
                            reveal,
                        });
                        self.force_sync = true;
                    } else {
                        inst.reveals.push_back(QueuedReveal {
                            reveal,
                            from_history: false,
                        });
                        self.queue_runnable(&id);
                    }
                }
            }
        }
        inst.last_activity = now;
        self.instances.insert(id, Slot::Active(inst));
    }

    // -- timers -------------------------------------------------------------

    fn arm_engine_timer(&mut self, at: LogicalTime, entry: TimerEntry) {
        let key = (at, self.timer_counter);
        self.timer_counter += 1;
        self.timers.insert(key, entry);
    }

    fn fire_due_timers(&mut self, now: LogicalTime) -> bool {
        let due: Vec<(LogicalTime, u64)> = self
            .timers
            .range(..=(now, u64::MAX))
            .map(|(k, _)| *k)
            .collect();
        let fired = !due.is_empty();
        for key in due {
            let Some(entry) = self.timers.remove(&key) else {
                continue;
            };
            match entry {
                TimerEntry::WorkflowTimer { wf, seq } => self.fire_workflow_timer(&wf, seq, now),
                TimerEntry::RetryStep { wf, seq } => self.fire_retry(&wf, seq, now),
            }
        }
        fired
    }

    fn fire_workflow_timer(&mut self, wf: &WorkflowId, seq: u64, now: LogicalTime) {
        if matches!(self.instances.get(wf), Some(Slot::Passive(_)))
            && self.reactivate(wf, now).is_err()
        {
            return;
        }
        let Some(Slot::Active(mut inst)) = self.instances.remove(wf) else {
            return;
        };
        if inst.state.is_terminal() || inst.pending_timers.remove(&seq).is_none() {
            self.instances.insert(wf.clone(), Slot::Active(inst));
            return;
        }
        self.append_event(wf, &mut inst, JournalEvent::TimerFired { seq }, now);
        inst.reveals.push_back(QueuedReveal {
            reveal: Reveal::Timer { seq, at: now },
            from_history: false,
        });
        inst.last_activity = now;
        self.metrics.timers_fired += 1;
        self.instances.insert(wf.clone(), Slot::Active(inst));
        self.queue_runnable(wf);
    }

    fn fire_retry(&mut self, wf: &WorkflowId, seq: u64, now: LogicalTime) {
        if matches!(self.instances.get(wf), Some(Slot::Passive(_)))
            && self.reactivate(wf, now).is_err()
        {
            return;
        }
        let Some(Slot::Active(mut inst)) = self.instances.remove(wf) else {
            return;
        };
        if inst.state.is_terminal() {
            self.instances.insert(wf.clone(), Slot::Active(inst));
            return;
        }
        let should_dispatch = match inst.steps.get_mut(&seq) {
            Some(meta) if meta.pending_retry.is_some() => {
                meta.pending_retry = None;
                true
            }
            _ => false,
        };
        if should_dispatch {
            self.dispatch_step(wf, &mut inst, seq);
        }
        self.instances.insert(wf.clone(), Slot::Active(inst));
    }

    // -- activation ---------------------------------------------------------

    fn queue_runnable(&mut self, id: &WorkflowId) {
        if self.runnable.insert(id.clone()) {
            self.run_queue.push_back(id.clone());
        }
    }

    fn activate(&mut self, id: &WorkflowId, now: LogicalTime) {
        let Some(Slot::Active(mut inst)) = self.instances.remove(id) else {
            return;
        };
        let span = tracing::debug_span!("activation", workflow = %id, shard = self.shard, state = ?inst.state.kind());
        let _guard = span.enter();
        if inst.state.is_terminal() || inst.fut.is_none() {
            self.instances.insert(id.clone(), Slot::Active(inst));
            return;
        }
        // Suspended → Running (or stay Recovering while history remains).
        match inst.state.kind() {
            StateKind::Pending
            | StateKind::AwaitingStep
            | StateKind::Sleeping
            | StateKind::Blocked => {
                self.set_state(&mut inst, WorkflowState::Running);
            }
            StateKind::Running | StateKind::Recovering => {}
            StateKind::Completed | StateKind::Failed | StateKind::Cancelled => {}
        }
        inst.last_activity = now;

        loop {
            let poll = {
                let fut = inst.fut.as_mut().expect("checked above");
                let waker = Waker::noop();
                let mut cx = TaskContext::from_waker(waker);
                catch_unwind(AssertUnwindSafe(|| fut.as_mut().poll(&mut cx)))
            };
            // Drain effects produced by this poll.
            let (events, steps, timers, nd, waiting) = {
                let mut cell = inst.cell.borrow_mut();
                (
                    std::mem::take(&mut cell.new_events),
                    std::mem::take(&mut cell.new_steps),
                    std::mem::take(&mut cell.new_timers),
                    cell.nd_error.clone(),
                    cell.waiting.clone(),
                )
            };
            for ev in events {
                self.append_event(id, &mut inst, ev, now);
            }
            for reg in steps {
                self.register_step(id, &mut inst, reg, now);
            }
            for (seq, fire_at) in timers {
                self.register_timer(id, &mut inst, seq, fire_at, now);
            }
            if let Some(nd) = nd {
                self.metrics.nd_failures += 1;
                self.fail_in_memory(id, &mut inst, FailureKind::NonDeterministic(nd));
                break;
            }
            match poll {
                Err(payload) => {
                    let msg = panic_message(payload);
                    self.append_event(
                        id,
                        &mut inst,
                        JournalEvent::WorkflowFailed {
                            error: Error::OrchestrationPanic(msg.clone()),
                        },
                        now,
                    );
                    self.fail_durable(id, &mut inst, FailureKind::OrchestrationPanic(msg));
                    break;
                }
                Ok(Poll::Ready(Ok(output))) => {
                    if self.history_incomplete(&inst) {
                        let nd = crate::error::NonDeterminismError {
                            seq: inst.cell.borrow().next_seq,
                            expected: None,
                            actual: None,
                        };
                        self.metrics.nd_failures += 1;
                        self.fail_in_memory(id, &mut inst, FailureKind::NonDeterministic(nd));
                        break;
                    }
                    self.complete(id, &mut inst, output, now);
                    break;
                }
                Ok(Poll::Ready(Err(err))) => {
                    if self.history_incomplete(&inst) {
                        let nd = crate::error::NonDeterminismError {
                            seq: inst.cell.borrow().next_seq,
                            expected: None,
                            actual: None,
                        };
                        self.metrics.nd_failures += 1;
                        self.fail_in_memory(id, &mut inst, FailureKind::NonDeterministic(nd));
                        break;
                    }
                    self.append_event(
                        id,
                        &mut inst,
                        JournalEvent::WorkflowFailed { error: err.clone() },
                        now,
                    );
                    self.fail_durable(id, &mut inst, FailureKind::Error(err));
                    break;
                }
                Ok(Poll::Pending) => {
                    if let Some(q) = inst.reveals.pop_front() {
                        self.reveal(&mut inst, q);
                        continue;
                    }
                    // Suspend.
                    let target = match waiting {
                        Waiting::Step(_) => WorkflowState::AwaitingStep,
                        Waiting::Timer(_) => WorkflowState::Sleeping,
                        Waiting::Signal(_, _) => WorkflowState::Blocked,
                        Waiting::None => {
                            // The workflow awaited something sqrl does not
                            // control: a determinism bug.
                            self.append_event(
                                id,
                                &mut inst,
                                JournalEvent::WorkflowFailed {
                                    error: Error::App(
                                        "orchestration code awaited a non-sqrl future; \
                                         see docs/determinism-guide.md"
                                            .to_string(),
                                    ),
                                },
                                now,
                            );
                            self.fail_durable(
                                id,
                                &mut inst,
                                FailureKind::Error(Error::App(
                                    "orchestration code awaited a non-sqrl future".to_string(),
                                )),
                            );
                            break;
                        }
                    };
                    self.set_state(&mut inst, target);
                    break;
                }
            }
        }
        self.maybe_snapshot(id, &mut inst, now);
        self.instances.insert(id.clone(), Slot::Active(inst));
    }

    fn history_incomplete(&self, inst: &Instance) -> bool {
        let cell = inst.cell.borrow();
        let unconsumed_cmds = cell.max_cmd_seq.is_some_and(|m| cell.next_seq <= m);
        cell.unrevealed > 0 || unconsumed_cmds || inst.reveals.iter().any(|q| q.from_history)
    }

    fn reveal(&mut self, inst: &mut Instance, q: QueuedReveal) {
        let mut cell = inst.cell.borrow_mut();
        if q.from_history {
            cell.unrevealed = cell.unrevealed.saturating_sub(1);
        }
        match &q.reveal {
            Reveal::StepOk { seq, bytes, at } => {
                cell.wf_time = cell.wf_time.max(*at);
                cell.resolved
                    .insert(*seq, Resolution::StepOk(bytes.clone()));
                inst.outcome_log.push(Outcome::StepOk {
                    seq: *seq,
                    result: bytes.clone(),
                    at: *at,
                });
                inst.resolved_in_history.remove(seq);
                inst.steps.remove(seq);
            }
            Reveal::StepErr {
                seq,
                error,
                attempts,
                at,
            } => {
                cell.wf_time = cell.wf_time.max(*at);
                cell.resolved.insert(
                    *seq,
                    Resolution::StepErr {
                        error: error.clone(),
                        attempts: *attempts,
                    },
                );
                inst.outcome_log.push(Outcome::StepErr {
                    seq: *seq,
                    error: error.clone(),
                    attempts: *attempts,
                    at: *at,
                });
                inst.resolved_in_history.remove(seq);
                inst.steps.remove(seq);
            }
            Reveal::Timer { seq, at } => {
                cell.wf_time = cell.wf_time.max(*at);
                cell.resolved.insert(*seq, Resolution::Timer);
                inst.outcome_log
                    .push(Outcome::TimerFired { seq: *seq, at: *at });
                inst.resolved_in_history.remove(seq);
                inst.pending_timers.remove(seq);
            }
            Reveal::Signal { name, payload, at } => {
                cell.wf_time = cell.wf_time.max(*at);
                cell.signal_buf
                    .entry(name.clone())
                    .or_default()
                    .push_back(payload.clone());
                inst.outcome_log.push(Outcome::Signal {
                    name: name.clone(),
                    payload: payload.clone(),
                    at: *at,
                });
            }
            Reveal::Resumed { at } => {
                cell.wf_time = cell.wf_time.max(*at);
                inst.outcome_log.push(Outcome::Resumed { at: *at });
            }
        }
    }

    fn register_step(
        &mut self,
        id: &WorkflowId,
        inst: &mut Instance,
        reg: StepReg,
        now: LogicalTime,
    ) {
        let seq = reg.seq;
        let entry = inst.steps.entry(seq).or_default();
        entry.name = reg.name;
        entry.opts = reg.opts;
        entry.closure = Some(reg.closure);
        if inst.resolved_in_history.contains(&seq) {
            return; // outcome is already recorded, just not yet revealed
        }
        if entry.dispatched_attempt.is_some() {
            return; // already out (re-poll after spurious wake)
        }
        if let Some(retry_at) = entry.pending_retry {
            if retry_at <= now {
                entry.pending_retry = None;
                self.dispatch_step(id, inst, seq);
            } else {
                self.arm_engine_timer(
                    retry_at,
                    TimerEntry::RetryStep {
                        wf: id.clone(),
                        seq,
                    },
                );
            }
            return;
        }
        self.dispatch_step(id, inst, seq);
    }

    fn dispatch_step(&mut self, id: &WorkflowId, inst: &mut Instance, seq: u64) {
        let Some(meta) = inst.steps.get_mut(&seq) else {
            return;
        };
        let attempt = meta.failed_attempts + 1;
        let Some(closure) = meta.closure.as_mut() else {
            return;
        };
        let fut = match catch_unwind(AssertUnwindSafe(&mut *closure)) {
            Ok(fut) => fut,
            Err(payload) => {
                // The closure itself panicked while creating the future.
                let msg = panic_message(payload);
                meta.dispatched_attempt = Some(attempt);
                self.cmds.push_back(EngineCmd::StepFinished {
                    id: id.clone(),
                    seq,
                    attempt,
                    outcome: Err(StepError::Panic(msg)),
                });
                return;
            }
        };
        meta.dispatched_attempt = Some(attempt);
        self.metrics.step_dispatches += 1;
        tracing::debug!(workflow = %id, seq, attempt, step = %meta.name, "step dispatched");
        self.dispatches.push(StepDispatch {
            workflow: id.clone(),
            seq,
            attempt,
            fut: Box::pin(CatchPanicStep { inner: fut }),
        });
    }

    fn register_timer(
        &mut self,
        id: &WorkflowId,
        inst: &mut Instance,
        seq: u64,
        fire_at: LogicalTime,
        now: LogicalTime,
    ) {
        if inst.resolved_in_history.contains(&seq) {
            return; // TimerFired is in history, will be revealed
        }
        if inst.pending_timers.contains_key(&seq) {
            return; // already armed
        }
        inst.pending_timers.insert(seq, fire_at);
        if fire_at <= now {
            // Due immediately (or overdue after recovery): fire in-line.
            inst.pending_timers.remove(&seq);
            self.append_event(id, inst, JournalEvent::TimerFired { seq }, now);
            inst.reveals.push_back(QueuedReveal {
                reveal: Reveal::Timer { seq, at: now },
                from_history: false,
            });
            self.metrics.timers_fired += 1;
            self.queue_runnable(id);
        } else {
            self.arm_engine_timer(
                fire_at,
                TimerEntry::WorkflowTimer {
                    wf: id.clone(),
                    seq,
                },
            );
        }
    }

    // -- terminal handling --------------------------------------------------

    fn complete(
        &mut self,
        id: &WorkflowId,
        inst: &mut Instance,
        output: Vec<u8>,
        now: LogicalTime,
    ) {
        self.append_event(
            id,
            inst,
            JournalEvent::WorkflowCompleted {
                output: output.clone(),
            },
            now,
        );
        self.append_terminal_snapshot(
            id,
            inst,
            TerminalStatus::Completed {
                output: output.clone(),
            },
        );
        self.set_state(inst, WorkflowState::Completed);
        inst.fut = None;
        inst.terminal_value = Some(Ok(output.clone()));
        self.pending_acks.push(PendingAck::Terminal {
            wf: id.clone(),
            result: Ok(output),
        });
        self.metrics.completions += 1;
        tracing::info!(workflow = %id, shard = self.shard, "workflow completed");
    }

    /// Journaled terminal failure (workflow error / orchestration panic).
    fn fail_durable(&mut self, id: &WorkflowId, inst: &mut Instance, failure: FailureKind) {
        let err = failure.to_error();
        self.set_state(inst, WorkflowState::Failed(failure));
        inst.fut = None;
        inst.terminal_value = Some(Err(err.clone()));
        self.pending_acks.push(PendingAck::Terminal {
            wf: id.clone(),
            result: Err(err),
        });
        self.metrics.failures += 1;
        tracing::warn!(workflow = %id, shard = self.shard, state = ?inst.state.kind(), "workflow failed");
    }

    /// In-memory-only failure (non-determinism): nothing journaled, so a
    /// restart with fixed code replays cleanly. Watchers resolve now (no
    /// durability involved).
    fn fail_in_memory(&mut self, _id: &WorkflowId, inst: &mut Instance, failure: FailureKind) {
        let err = failure.to_error();
        self.set_state(inst, WorkflowState::Failed(failure));
        inst.fut = None;
        inst.terminal_value = Some(Err(err.clone()));
        inst.terminal_acked = true;
        for w in inst.watchers.drain(..) {
            w.complete(Err(err.clone()));
        }
        self.metrics.failures += 1;
    }

    fn set_state(&mut self, inst: &mut Instance, to: WorkflowState) {
        match inst.state.transition(to) {
            Ok(next) => inst.state = next,
            Err(illegal) => {
                // Engine bug: refuse the transition, record it. DST asserts
                // this counter stays zero.
                self.metrics.illegal_transitions += 1;
                tracing::error!(?illegal, workflow = %inst.cell.borrow().id, "illegal state transition refused");
            }
        }
    }

    // -- journaling / snapshots / group commit ------------------------------

    fn append_event(
        &mut self,
        id: &WorkflowId,
        inst: &mut Instance,
        event: JournalEvent,
        now: LogicalTime,
    ) {
        let rec = JournalRecord {
            index: inst.record_index,
            at: now,
            event,
        };
        inst.record_index += 1;
        inst.records_since_snapshot += 1;
        self.append_buf.push(AppendEntry {
            workflow: id.clone(),
            payload: AppendPayload::Record(rec),
        });
        self.metrics.records_appended += 1;
    }

    fn maybe_snapshot(&mut self, id: &WorkflowId, inst: &mut Instance, _now: LogicalTime) {
        if inst.state.is_terminal() || inst.fut.is_none() {
            return;
        }
        if self.history_incomplete(inst) {
            return; // never snapshot mid-replay
        }
        let delta = inst.records_since_snapshot;
        let total = inst.record_index;
        // Amortized cadence: at least `snapshot_every` new records AND at
        // least a quarter of total history since the last snapshot, so total
        // snapshot bytes stay O(history) (ADR 0006).
        if delta < self.config.snapshot_every || delta.saturating_mul(4) < total {
            return;
        }
        self.take_snapshot(id, inst, None);
    }

    /// Snapshot every live workflow that is at a quiescent suspension point
    /// (clean shutdown): their next recovery becomes lazy — O(metadata).
    fn snapshot_quiescent(&mut self, _now: LogicalTime) {
        if self.config.snapshot_every == u64::MAX {
            return; // snapshots disabled
        }
        let ids: Vec<WorkflowId> = self
            .instances
            .iter()
            .filter_map(|(id, slot)| match slot {
                Slot::Active(inst)
                    if !inst.state.is_terminal()
                        && inst.fut.is_some()
                        && inst.reveals.is_empty()
                        && inst.records_since_snapshot > 0
                        && matches!(
                            inst.state.kind(),
                            StateKind::Sleeping | StateKind::Blocked | StateKind::AwaitingStep
                        ) =>
                {
                    Some(id.clone())
                }
                _ => None,
            })
            .collect();
        for id in ids {
            if let Some(Slot::Active(mut inst)) = self.instances.remove(&id) {
                if !self.history_incomplete(&inst) {
                    self.take_snapshot(&id, &mut inst, None);
                }
                self.instances.insert(id, Slot::Active(inst));
            }
        }
    }

    fn take_snapshot(
        &mut self,
        id: &WorkflowId,
        inst: &mut Instance,
        terminal: Option<TerminalStatus>,
    ) {
        let cell = inst.cell.borrow();
        let inflight_steps: BTreeMap<u64, InflightStep> = inst
            .steps
            .iter()
            .map(|(seq, meta)| {
                (
                    *seq,
                    InflightStep {
                        name: meta.name.clone(),
                        failed_attempts: meta.failed_attempts,
                        retry_at: meta.pending_retry,
                    },
                )
            })
            .collect();
        let meta = SnapshotMeta {
            start: Some(inst.start.clone()),
            inflight_steps,
            pending_timers: inst.pending_timers.clone(),
            terminal,
            wf_time: cell.wf_time,
        };
        let body = SnapshotBody {
            cmds: cell.cmds.clone(),
            outcomes: inst.outcome_log.clone(),
        };
        drop(cell);
        let snap = match SnapshotRecord::build(inst.record_index, meta, &body) {
            Ok(s) => s,
            Err(e) => {
                // A snapshot is an optimization; losing one must never lose
                // data. Log and continue with the plain journal.
                tracing::error!(workflow = %id, error = %e, "snapshot encoding failed; skipping");
                return;
            }
        };
        self.append_buf.push(AppendEntry {
            workflow: id.clone(),
            payload: AppendPayload::Snapshot(snap),
        });
        inst.records_since_snapshot = 0;
        self.metrics.snapshots_taken += 1;
    }

    fn append_terminal_snapshot(
        &mut self,
        id: &WorkflowId,
        inst: &mut Instance,
        terminal: TerminalStatus,
    ) {
        // Failed workflows keep their full journal for debugging/fork; only
        // Completed and Cancelled get a compacting terminal snapshot.
        if matches!(terminal, TerminalStatus::Failed { .. }) {
            return;
        }
        let snap = SnapshotRecord {
            upto: inst.record_index,
            meta: SnapshotMeta {
                start: Some(inst.start.clone()),
                terminal: Some(terminal),
                wf_time: inst.cell.borrow().wf_time,
                ..SnapshotMeta::default()
            },
            body: Vec::new(),
        };
        self.append_buf.push(AppendEntry {
            workflow: id.clone(),
            payload: AppendPayload::Snapshot(snap),
        });
        self.metrics.snapshots_taken += 1;
    }

    fn flush(&mut self, now: LogicalTime) {
        if self.storage_failed.is_some() {
            return;
        }
        if !self.append_buf.is_empty() {
            let buf = std::mem::take(&mut self.append_buf);
            let n = buf.len();
            if let Err(e) = self.storage.append(&buf) {
                self.fail_storage(e);
                return;
            }
            self.unsynced_records += n;
            if self.unsynced_since.is_none() {
                self.unsynced_since = Some(now);
            }
        }
        let due = match self.config.fsync {
            FsyncPolicy::Strict => self.unsynced_records > 0,
            FsyncPolicy::Group {
                max_delay,
                max_batch,
            } => {
                self.unsynced_records >= max_batch
                    || (self.unsynced_records > 0
                        && self
                            .unsynced_since
                            .is_some_and(|since| now.saturating_since(since) >= max_delay))
            }
            FsyncPolicy::Relaxed { interval } => {
                self.unsynced_records > 0 && now.saturating_since(self.last_sync_at) >= interval
            }
        } || (self.force_sync && self.unsynced_records > 0);
        if due {
            match self.storage.sync() {
                Ok(()) => {
                    self.unsynced_records = 0;
                    self.unsynced_since = None;
                    self.last_sync_at = now;
                    self.force_sync = false;
                    self.release_acks();
                }
                Err(e) => self.fail_storage(e),
            }
        } else if self.unsynced_records == 0 {
            self.force_sync = false;
            self.release_acks();
        }
    }

    fn release_acks(&mut self) {
        let acks = std::mem::take(&mut self.pending_acks);
        for ack in acks {
            match ack {
                PendingAck::Terminal { wf, result } => {
                    if let Some(Slot::Active(inst)) = self.instances.get_mut(&wf) {
                        inst.terminal_acked = true;
                        for w in inst.watchers.drain(..) {
                            w.complete(result.clone());
                        }
                    }
                }
                PendingAck::StrictReveal { wf, reveal } => {
                    if let Some(Slot::Active(inst)) = self.instances.get_mut(&wf) {
                        inst.reveals.push_back(QueuedReveal {
                            reveal,
                            from_history: false,
                        });
                    }
                    self.queue_runnable(&wf);
                }
            }
        }
    }

    fn fail_storage(&mut self, e: StorageError) {
        tracing::error!(error = %e, shard = self.shard, "storage failed; halting commits");
        self.storage_failed = Some(e.clone());
        // Nothing unsynced can ever be acknowledged.
        let acks = std::mem::take(&mut self.pending_acks);
        for ack in acks {
            if let PendingAck::Terminal { wf, .. } = ack {
                if let Some(Slot::Active(inst)) = self.instances.get_mut(&wf) {
                    for w in inst.watchers.drain(..) {
                        w.complete(Err(Error::Storage(e.clone())));
                    }
                }
            }
        }
    }

    // -- passivation & recovery --------------------------------------------

    fn sweep_passivation(&mut self, now: LogicalTime) {
        // The sweep walks every instance; throttle it so busy shards do not
        // pay O(instances) per tick.
        if now.saturating_since(self.last_sweep) < core::time::Duration::from_millis(50) {
            return;
        }
        self.last_sweep = now;
        // Opportunistic storage maintenance (segment roll bookkeeping + GC of
        // segments fully superseded by durable snapshots).
        if self.storage_failed.is_none() {
            if let Err(e) = self.storage.maintain() {
                tracing::warn!(error = %e, "storage maintenance failed");
            }
        }
        // Convert acked terminals to compact slots.
        let terminal_ids: Vec<WorkflowId> = self
            .instances
            .iter()
            .filter_map(|(id, slot)| match slot {
                Slot::Active(inst) if inst.state.is_terminal() && inst.terminal_acked => {
                    Some(id.clone())
                }
                _ => None,
            })
            .collect();
        for id in terminal_ids {
            if let Some(Slot::Active(inst)) = self.instances.remove(&id) {
                let failure = match &inst.state {
                    WorkflowState::Failed(f) => Some(f.to_error().to_string()),
                    _ => None,
                };
                let result = inst
                    .terminal_value
                    .clone()
                    .unwrap_or_else(|| Err(Error::App("terminal without value".to_string())));
                self.active_count = self.active_count.saturating_sub(1);
                self.instances.insert(
                    id,
                    Slot::Terminal(TerminalInfo {
                        name: inst.start.name.clone(),
                        state: inst.state.kind(),
                        failure,
                        result,
                    }),
                );
            }
        }
        // Passivate idle Sleeping/Blocked instances with nothing in flight.
        let Some(idle_after) = self.config.passivate_after else {
            return;
        };
        let idle_ids: Vec<WorkflowId> = self
            .instances
            .iter()
            .filter_map(|(id, slot)| match slot {
                Slot::Active(inst) => {
                    let idle = now.saturating_since(inst.last_activity) >= idle_after;
                    let quiescent =
                        matches!(inst.state.kind(), StateKind::Sleeping | StateKind::Blocked)
                            && inst.steps.values().all(|m| {
                                m.dispatched_attempt.is_none() && m.pending_retry.is_none()
                            })
                            && inst.reveals.is_empty();
                    if idle && quiescent {
                        Some(id.clone())
                    } else {
                        None
                    }
                }
                _ => None,
            })
            .collect();
        for id in idle_ids {
            if self.unsynced_records > 0 {
                // Only passivate fully-durable instances: reactivation replays
                // from storage, which must not be behind the in-memory state.
                continue;
            }
            if let Some(Slot::Active(inst)) = self.instances.remove(&id) {
                self.active_count = self.active_count.saturating_sub(1);
                self.metrics.passivations += 1;
                let hint = inst.state.kind();
                let mut inst = inst;
                if self.config.snapshot_every != u64::MAX && inst.records_since_snapshot > 0 {
                    // Quiescence snapshot: makes the next reload O(metadata).
                    self.take_snapshot(&id, &mut inst, None);
                }
                self.instances.insert(
                    id,
                    Slot::Passive(PassiveInfo {
                        name: inst.start.name.clone(),
                        state_hint: hint,
                        watchers: inst.watchers,
                    }),
                );
            }
        }
    }

    fn reactivate(&mut self, id: &WorkflowId, now: LogicalTime) -> Result<(), StorageError> {
        let Some(Slot::Passive(p)) = self.instances.remove(id) else {
            return Ok(());
        };
        let readout = match self.storage.read(id) {
            Ok(r) => r,
            Err(e) => {
                self.instances.insert(id.clone(), Slot::Passive(p));
                return Err(e);
            }
        };
        self.metrics.reactivations += 1;
        self.install_loaded_inner(id.clone(), readout, now, true);
        if let Some(Slot::Active(inst)) = self.instances.get_mut(id) {
            inst.watchers.extend(p.watchers);
        } else if let Some(Slot::Terminal(t)) = self.instances.get_mut(id) {
            for w in p.watchers {
                w.complete(t.result.clone());
            }
        }
        Ok(())
    }

    /// Build a slot from persisted state. Live workflows with nothing
    /// actively in flight recover **lazily**: timers are re-armed straight
    /// from snapshot metadata + journal tail, and the workflow stays
    /// passivated until something actually happens to it — recovery cost is
    /// O(metadata), not O(history). Workflows with a bare in-flight step
    /// must materialize now (the step closure only exists in re-run code).
    fn install_loaded(&mut self, id: WorkflowId, readout: JournalReadout, now: LogicalTime) {
        self.install_loaded_inner(id, readout, now, false)
    }

    fn install_loaded_inner(
        &mut self,
        id: WorkflowId,
        readout: JournalReadout,
        now: LogicalTime,
        force_materialize: bool,
    ) {
        if !force_materialize {
            match summarize(&readout) {
                Summary::Terminal { name, status } => {
                    let (state, failure, result) = terminal_parts(status);
                    self.instances.insert(
                        id,
                        Slot::Terminal(TerminalInfo {
                            name,
                            state,
                            failure,
                            result,
                        }),
                    );
                    return;
                }
                Summary::Lazy {
                    name,
                    pending_timers,
                    retries,
                    state_hint,
                } => {
                    for (seq, at) in pending_timers {
                        self.arm_engine_timer(
                            at,
                            TimerEntry::WorkflowTimer {
                                wf: id.clone(),
                                seq,
                            },
                        );
                    }
                    for (seq, at) in retries {
                        self.arm_engine_timer(
                            at,
                            TimerEntry::RetryStep {
                                wf: id.clone(),
                                seq,
                            },
                        );
                    }
                    self.instances.insert(
                        id,
                        Slot::Passive(PassiveInfo {
                            name,
                            state_hint,
                            watchers: Vec::new(),
                        }),
                    );
                    return;
                }
                Summary::Corrupt(msg) => {
                    tracing::error!(workflow = %id, msg, "unloadable workflow journal");
                    self.instances.insert(
                        id,
                        Slot::Terminal(TerminalInfo {
                            name: String::new(),
                            state: StateKind::Failed,
                            failure: Some(msg.clone()),
                            result: Err(Error::App(msg)),
                        }),
                    );
                    return;
                }
                Summary::NeedsCode => {}
            }
        }
        match load_instance(&self.registry, &self.config, readout, &id, now) {
            Loaded::Terminal(info) => {
                self.instances.insert(id, Slot::Terminal(info));
            }
            Loaded::Active(mut inst) => {
                tracing::debug!(workflow = %id, shard = self.shard, "materializing workflow (replay)");
                // Arm pending retries recorded in history.
                let retries: Vec<(u64, LogicalTime)> = inst
                    .steps
                    .iter()
                    .filter_map(|(seq, m)| m.pending_retry.map(|at| (*seq, at)))
                    .collect();
                for (seq, at) in retries {
                    if at > now {
                        self.arm_engine_timer(
                            at,
                            TimerEntry::RetryStep {
                                wf: id.clone(),
                                seq,
                            },
                        );
                    } else if let Some(m) = inst.steps.get_mut(&seq) {
                        // Overdue retry: dispatch as soon as the closure is
                        // re-registered by replayed code.
                        m.pending_retry = None;
                    }
                }
                self.instances.insert(id.clone(), Slot::Active(inst));
                self.active_count += 1;
                self.queue_runnable(&id);
            }
            Loaded::Corrupt(msg) => {
                tracing::error!(workflow = %id, msg, "unloadable workflow journal");
                self.instances.insert(
                    id,
                    Slot::Terminal(TerminalInfo {
                        name: String::new(),
                        state: StateKind::Failed,
                        failure: Some(msg.clone()),
                        result: Err(Error::App(msg)),
                    }),
                );
            }
        }
    }
}

// ---------------------------------------------------------------------------
// Loading persisted history into an Instance
// ---------------------------------------------------------------------------

enum Loaded {
    Active(Box<Instance>),
    Terminal(TerminalInfo),
    Corrupt(String),
}

fn load_instance(
    registry: &Registry,
    config: &EngineConfig,
    readout: JournalReadout,
    id: &WorkflowId,
    now: LogicalTime,
) -> Loaded {
    let mut start: Option<StartInfo> = None;
    let mut reveals: VecDeque<QueuedReveal> = VecDeque::new();
    let mut cmds: BTreeMap<u64, crate::event::CmdDesc> = BTreeMap::new();
    let mut timer_targets: BTreeMap<u64, LogicalTime> = BTreeMap::new();
    let mut steps: BTreeMap<u64, StepRuntime> = BTreeMap::new();
    let pending_timers: BTreeMap<u64, LogicalTime> = BTreeMap::new();
    let mut terminal: Option<(TerminalStatus, LogicalTime)> = None;
    let mut record_index: u64 = 0;
    let mut records_since_snapshot: u64 = 0;

    if let Some(snap) = readout.snapshot {
        let meta = snap.meta.clone();
        record_index = snap.upto;
        start = meta.start.clone();
        if let Some(t) = meta.terminal {
            terminal = Some((t, meta.wf_time));
        }
        let body = match snap.decode_body() {
            Ok(b) => b,
            Err(e) => return Loaded::Corrupt(format!("snapshot body undecodable: {e}")),
        };
        cmds = body.cmds;
        // Note: pending timers are NOT pre-armed here. Arming happens when
        // replayed code re-issues the sleep (register_timer); pre-filling
        // `pending_timers` would make registration believe the wheel entry
        // already exists in this process.
        for (seq, at) in &meta.pending_timers {
            timer_targets.insert(*seq, *at);
        }
        for (seq, inflight) in meta.inflight_steps {
            steps.insert(
                seq,
                StepRuntime {
                    name: inflight.name,
                    failed_attempts: inflight.failed_attempts,
                    pending_retry: inflight.retry_at,
                    ..StepRuntime::default()
                },
            );
        }
        for outcome in body.outcomes {
            let reveal = match outcome {
                Outcome::StepOk { seq, result, at } => Reveal::StepOk {
                    seq,
                    bytes: result,
                    at,
                },
                Outcome::StepErr {
                    seq,
                    error,
                    attempts,
                    at,
                } => Reveal::StepErr {
                    seq,
                    error,
                    attempts,
                    at,
                },
                Outcome::TimerFired { seq, at } => Reveal::Timer { seq, at },
                Outcome::Signal { name, payload, at } => Reveal::Signal { name, payload, at },
                Outcome::Resumed { at } => Reveal::Resumed { at },
            };
            reveals.push_back(QueuedReveal {
                reveal,
                from_history: true,
            });
        }
    }

    for rec in readout.records {
        record_index = record_index.max(rec.index + 1);
        records_since_snapshot += 1;
        let at = rec.at;
        match rec.event {
            JournalEvent::WorkflowStarted {
                name,
                version,
                input,
                seed,
            } => {
                start = Some(StartInfo {
                    name,
                    version,
                    input,
                    seed,
                    started_at: at,
                });
            }
            JournalEvent::StepScheduled { seq, name } => {
                cmds.insert(seq, crate::event::CmdDesc::Step { name: name.clone() });
                steps.entry(seq).or_default().name = name;
            }
            JournalEvent::StepCompleted { seq, result } => {
                steps.remove(&seq);
                reveals.push_back(QueuedReveal {
                    reveal: Reveal::StepOk {
                        seq,
                        bytes: result,
                        at,
                    },
                    from_history: true,
                });
            }
            JournalEvent::StepFailed {
                seq,
                error,
                attempt,
                retry_at,
            } => {
                let meta = steps.entry(seq).or_default();
                meta.failed_attempts = attempt;
                meta.pending_retry = retry_at;
                if retry_at.is_none() {
                    steps.remove(&seq);
                    reveals.push_back(QueuedReveal {
                        reveal: Reveal::StepErr {
                            seq,
                            error,
                            attempts: attempt,
                            at,
                        },
                        from_history: true,
                    });
                }
            }
            JournalEvent::TimerScheduled { seq, fire_at } => {
                cmds.insert(seq, crate::event::CmdDesc::Timer);
                timer_targets.insert(seq, fire_at);
            }
            JournalEvent::TimerFired { seq } => {
                reveals.push_back(QueuedReveal {
                    reveal: Reveal::Timer { seq, at },
                    from_history: true,
                });
            }
            JournalEvent::SignalAwaited { seq, name } => {
                cmds.insert(seq, crate::event::CmdDesc::AwaitSignal { name });
            }
            JournalEvent::SignalReceived { name, payload } => {
                reveals.push_back(QueuedReveal {
                    reveal: Reveal::Signal { name, payload, at },
                    from_history: true,
                });
            }
            JournalEvent::PatchRecorded { seq, id } => {
                cmds.insert(seq, crate::event::CmdDesc::Patch { id });
            }
            JournalEvent::WorkflowCompleted { output } => {
                terminal = Some((TerminalStatus::Completed { output }, at));
            }
            JournalEvent::WorkflowFailed { error } => {
                terminal = Some((
                    TerminalStatus::Failed {
                        failure: FailureKind::Error(error),
                    },
                    at,
                ));
            }
            JournalEvent::WorkflowCancelled => {
                terminal = Some((TerminalStatus::Cancelled, at));
            }
            JournalEvent::WorkflowResumed => {
                // Void the last terminal failure; reset the exhausted step.
                if let Some((TerminalStatus::Failed { .. }, _)) = &terminal {
                    terminal = None;
                }
                // Remove the final StepErr reveal (if any) and reset its
                // attempts so the step re-runs fresh.
                if let Some(pos) = reveals
                    .iter()
                    .rposition(|q| matches!(q.reveal, Reveal::StepErr { .. }))
                {
                    if let Some(q) = reveals.remove(pos) {
                        if let Reveal::StepErr { seq, .. } = q.reveal {
                            steps.insert(seq, StepRuntime::default());
                        }
                    }
                }
                reveals.push_back(QueuedReveal {
                    reveal: Reveal::Resumed { at },
                    from_history: true,
                });
            }
        }
    }

    let Some(start) = start else {
        return Loaded::Corrupt("journal has no WorkflowStarted record".to_string());
    };

    if let Some((status, _)) = terminal {
        let (state, failure, result) = match status {
            TerminalStatus::Completed { output } => (StateKind::Completed, None, Ok(output)),
            TerminalStatus::Failed { failure } => {
                let e = failure.to_error();
                (StateKind::Failed, Some(e.to_string()), Err(e))
            }
            TerminalStatus::Cancelled => (StateKind::Cancelled, None, Err(Error::Cancelled)),
        };
        return Loaded::Terminal(TerminalInfo {
            name: start.name,
            state,
            failure,
            result,
        });
    }

    let Some(def) = registry.get(&start.name) else {
        return Loaded::Corrupt(format!(
            "workflow name `{}` is not registered in this process",
            start.name
        ));
    };

    let mut cell_inner = InstanceInner::new(
        id.clone(),
        start.name.clone(),
        start.version,
        start.seed,
        config.max_payload,
        config.retry.clone(),
        start.started_at,
    );
    for (seq, desc) in &cmds {
        cell_inner.load_cmd(*seq, desc.clone());
    }
    cell_inner.timer_targets = timer_targets;
    cell_inner.unrevealed = reveals.iter().filter(|q| q.from_history).count();
    let cell = Rc::new(RefCell::new(cell_inner));
    let fut = (def.factory)(Ctx::from_cell(Rc::clone(&cell)), start.input.clone());

    let resolved_in_history: BTreeSet<u64> = reveals
        .iter()
        .filter_map(|q| match &q.reveal {
            Reveal::StepOk { seq, .. }
            | Reveal::StepErr { seq, .. }
            | Reveal::Timer { seq, .. } => Some(*seq),
            Reveal::Signal { .. } | Reveal::Resumed { .. } => None,
        })
        .collect();

    Loaded::Active(Box::new(Instance {
        cell,
        fut: Some(fut),
        state: WorkflowState::Recovering,
        reveals,
        resolved_in_history,
        steps,
        pending_timers,
        record_index,
        records_since_snapshot,
        outcome_log: Vec::new(),
        start,
        watchers: Vec::new(),
        last_activity: now,
        terminal_value: None,
        terminal_acked: false,
    }))
}

// ---------------------------------------------------------------------------
// Recovery summaries: what a journal says without running any code
// ---------------------------------------------------------------------------

enum Summary {
    /// The workflow is terminal.
    Terminal {
        name: String,
        status: TerminalStatus,
    },
    /// Nothing actively in flight: recover lazily (arm these timers, park
    /// as Passive).
    Lazy {
        name: String,
        pending_timers: Vec<(u64, LogicalTime)>,
        retries: Vec<(u64, LogicalTime)>,
        state_hint: StateKind,
    },
    /// A bare in-flight step exists — only re-run code can re-create its
    /// closure; materialize now.
    NeedsCode,
    /// The journal is unusable.
    Corrupt(String),
}

fn terminal_parts(status: TerminalStatus) -> (StateKind, Option<String>, TerminalResult) {
    match status {
        TerminalStatus::Completed { output } => (StateKind::Completed, None, Ok(output)),
        TerminalStatus::Failed { failure } => {
            let e = failure.to_error();
            (StateKind::Failed, Some(e.to_string()), Err(e))
        }
        TerminalStatus::Cancelled => (StateKind::Cancelled, None, Err(Error::Cancelled)),
    }
}

/// Decide whether persisted state allows **lazy** recovery.
///
/// Lazy recovery is sound only when the snapshot provably captured the
/// workflow at a quiescent suspension point and nothing happened after it —
/// i.e. the snapshot is the *last* record. The engine writes exactly such
/// snapshots at clean shutdown and at passivation. Any journal tail after
/// the snapshot (a crash happened) forces eager materialization: a torn
/// tail can hide runnable work that only re-running the code rediscovers.
fn summarize(readout: &JournalReadout) -> Summary {
    let Some(snap) = &readout.snapshot else {
        return Summary::NeedsCode;
    };
    if !readout.records.is_empty() {
        return Summary::NeedsCode;
    }
    let Some(start) = &snap.meta.start else {
        return Summary::Corrupt("snapshot has no start info".to_string());
    };
    let name = start.name.clone();
    if let Some(status) = &snap.meta.terminal {
        return Summary::Terminal {
            name,
            status: status.clone(),
        };
    }
    // A bare in-flight step (no scheduled retry) needs its closure, which
    // only re-run code can provide.
    if snap
        .meta
        .inflight_steps
        .values()
        .any(|s| s.retry_at.is_none())
    {
        return Summary::NeedsCode;
    }
    let retries: Vec<(u64, LogicalTime)> = snap
        .meta
        .inflight_steps
        .iter()
        .filter_map(|(seq, s)| s.retry_at.map(|at| (*seq, at)))
        .collect();
    let pending_timers: Vec<(u64, LogicalTime)> = snap
        .meta
        .pending_timers
        .iter()
        .map(|(s, at)| (*s, *at))
        .collect();
    let state_hint = if pending_timers.is_empty() && retries.is_empty() {
        StateKind::Blocked
    } else {
        StateKind::Sleeping
    };
    Summary::Lazy {
        name,
        pending_timers,
        retries,
        state_hint,
    }
}

// ---------------------------------------------------------------------------
// Panic capture for steps
// ---------------------------------------------------------------------------

struct CatchPanicStep {
    inner: BoxStepFut,
}

impl std::future::Future for CatchPanicStep {
    type Output = Result<Vec<u8>, StepError>;

    fn poll(self: Pin<&mut Self>, cx: &mut TaskContext<'_>) -> Poll<Self::Output> {
        let this = self.get_mut();
        match catch_unwind(AssertUnwindSafe(|| this.inner.as_mut().poll(cx))) {
            Ok(p) => p,
            Err(payload) => Poll::Ready(Err(StepError::Panic(panic_message(payload)))),
        }
    }
}

fn panic_message(payload: Box<dyn std::any::Any + Send>) -> String {
    if let Some(s) = payload.downcast_ref::<&str>() {
        (*s).to_string()
    } else if let Some(s) = payload.downcast_ref::<String>() {
        s.clone()
    } else {
        "panic of unknown type".to_string()
    }
}
