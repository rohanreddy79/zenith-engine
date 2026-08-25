//! `SimScheduler`: the deterministic driver for [`sqrl_core::EngineCore`].
//!
//! Runs any number of engine shards, any storage backend, and all step
//! futures on one thread under virtual time with seeded scheduling. The same
//! engine code that runs here runs under the real thread-per-core scheduler;
//! only the driver differs. Crash/restart cycles (via `SimDisk`) reuse the
//! same clock and seed lineage, so a whole multi-crash history is a pure
//! function of `(seed, workload)`.

use crate::clock::SimClock;
use crate::executor::SimExecutor;
use crate::rng::SimRng;
use sqrl_core::engine::{EngineCmd, EngineCore, EngineMetrics, TickOutput};
use sqrl_core::handle::TerminalResult;
use sqrl_core::storage::StorageStats;
use sqrl_core::sync::promise;
use sqrl_core::{
    Clock, DeterministicRng, EngineConfig, Error, LogicalTime, Registry, Rejected, StateKind,
    Storage, StorageError, WorkflowHandle, WorkflowId,
};
use std::cell::RefCell;
use std::collections::{BTreeMap, VecDeque};
use std::rc::Rc;
use std::sync::{Arc, Mutex};
use std::time::Duration;

type CmdQueue = Arc<Mutex<VecDeque<(usize, EngineCmd)>>>;

/// Deterministic single-threaded scheduler driving one engine core per
/// storage shard. See the crate docs for the determinism contract.
pub struct SimScheduler {
    exec: SimExecutor,
    clock: SimClock,
    engines: Vec<Rc<RefCell<EngineCore>>>,
    queue: CmdQueue,
    scheduled_wakes: BTreeMap<u64, ()>,
    num_shards: usize,
}

impl SimScheduler {
    /// Open engines over `storage` (one per shard). `seed` fixes every
    /// scheduling and entropy decision.
    pub fn new(
        seed: u64,
        storage: &dyn Storage,
        registry: Arc<Registry>,
        config: EngineConfig,
    ) -> Result<Self, StorageError> {
        let clock = SimClock::new(LogicalTime::from_millis(1_000));
        SimScheduler::with_clock(seed, storage, registry, config, clock)
    }

    /// Like [`SimScheduler::new`] but sharing an existing clock — used for
    /// crash/restart cycles where time must keep flowing.
    pub fn with_clock(
        seed: u64,
        storage: &dyn Storage,
        registry: Arc<Registry>,
        config: EngineConfig,
        clock: SimClock,
    ) -> Result<Self, StorageError> {
        let exec = SimExecutor::with_clock(
            SimRng::new(seed).fork("sim-sched").next_u64(),
            clock.clone(),
        );
        let entropy = Arc::new(DeterministicRng::new(
            SimRng::new(seed).fork("sim-entropy").next_u64(),
        ));
        let num_shards = storage.num_shards();
        let mut engines = Vec::with_capacity(num_shards);
        for shard in 0..num_shards {
            let core = EngineCore::open(
                shard,
                Arc::clone(&registry),
                storage.open_shard(shard)?,
                Arc::new(clock.clone()),
                Arc::clone(&entropy) as Arc<dyn sqrl_core::Entropy>,
                config.clone(),
            )?;
            engines.push(Rc::new(RefCell::new(core)));
        }
        Ok(SimScheduler {
            exec,
            clock,
            engines,
            queue: Arc::new(Mutex::new(VecDeque::new())),
            scheduled_wakes: BTreeMap::new(),
            num_shards,
        })
    }

    /// The scheduler's clock.
    pub fn clock(&self) -> SimClock {
        self.clock.clone()
    }

    /// Current virtual time.
    pub fn now(&self) -> LogicalTime {
        self.clock.now()
    }

    /// Number of shards.
    pub fn num_shards(&self) -> usize {
        self.num_shards
    }

    fn shard_of(&self, cmd: &EngineCmd) -> usize {
        cmd.workflow()
            .map(|id| id.shard(self.num_shards))
            .unwrap_or(0)
    }

    /// Queue a command for the owning shard.
    pub fn submit(&self, cmd: EngineCmd) {
        let shard = self.shard_of(&cmd);
        self.queue
            .lock()
            .expect("sim queue lock poisoned")
            .push_back((shard, cmd));
    }

    /// Start a workflow; runs the sim until admission is decided.
    /// Returns the handle on success.
    pub fn start(
        &mut self,
        id: impl Into<WorkflowId>,
        name: &str,
        input: &impl serde::Serialize,
    ) -> Result<WorkflowHandle, Rejected> {
        let id = id.into();
        let input = sqrl_core::codec::to_vec(input, "workflow input")
            .map_err(|e| Rejected::Invalid(e.to_string()))?;
        let (admit_c, admit_w) = promise::<Result<(), Rejected>>();
        let (term_c, term_w) = promise::<TerminalResult>();
        self.submit(EngineCmd::Start {
            id: id.clone(),
            name: name.to_string(),
            input,
            admit: admit_c,
            terminal: term_c,
        });
        self.run_until_idle();
        match admit_w.peek() {
            Some(Ok(())) => Ok(WorkflowHandle::new(id, term_w)),
            Some(Err(rej)) => Err(rej),
            None => Err(Rejected::Unavailable(
                "admission not decided (engine stuck?)".to_string(),
            )),
        }
    }

    /// Attach a handle to an existing workflow.
    pub fn handle(&mut self, id: impl Into<WorkflowId>) -> Result<WorkflowHandle, Error> {
        let id = id.into();
        let (term_c, term_w) = promise::<TerminalResult>();
        let (ack_c, ack_w) = promise::<Result<(), Error>>();
        self.submit(EngineCmd::Watch {
            id: id.clone(),
            terminal: term_c,
            ack: ack_c,
        });
        self.run_until_idle();
        match ack_w.peek() {
            Some(Ok(())) => Ok(WorkflowHandle::new(id, term_w)),
            Some(Err(e)) => Err(e),
            None => Err(Error::App("watch not acknowledged".to_string())),
        }
    }

    /// Deliver a signal; runs the sim until acknowledged.
    pub fn signal(
        &mut self,
        id: impl Into<WorkflowId>,
        name: &str,
        payload: &impl serde::Serialize,
    ) -> Result<(), Error> {
        let payload = sqrl_core::codec::to_vec(payload, "signal payload")?;
        let (ack_c, ack_w) = promise::<Result<(), Error>>();
        self.submit(EngineCmd::Signal {
            id: id.into(),
            name: name.to_string(),
            payload,
            ack: ack_c,
        });
        self.run_until_idle();
        ack_w
            .peek()
            .unwrap_or_else(|| Err(Error::App("signal not acknowledged".to_string())))
    }

    /// Cancel a workflow.
    pub fn cancel(&mut self, id: impl Into<WorkflowId>) -> Result<(), Error> {
        let (ack_c, ack_w) = promise::<Result<(), Error>>();
        self.submit(EngineCmd::Cancel {
            id: id.into(),
            ack: ack_c,
        });
        self.run_until_idle();
        ack_w
            .peek()
            .unwrap_or_else(|| Err(Error::App("cancel not acknowledged".to_string())))
    }

    /// Lifecycle states across all shards.
    pub fn states(&self) -> BTreeMap<WorkflowId, StateKind> {
        let mut all = BTreeMap::new();
        for eng in &self.engines {
            all.extend(eng.borrow().states());
        }
        all
    }

    /// Combined engine metrics.
    pub fn metrics(&self) -> Vec<EngineMetrics> {
        self.engines.iter().map(|e| e.borrow().metrics()).collect()
    }

    /// Combined storage stats.
    pub fn storage_stats(&self) -> Vec<StorageStats> {
        self.engines
            .iter()
            .map(|e| e.borrow().storage_stats())
            .collect()
    }

    /// Drive everything — engines, steps, timers, fsync deadlines — until the
    /// whole system is quiescent (no runnable work and no armed deadline
    /// except workflows blocked on external input). Virtual time advances as
    /// needed. Returns the number of engine ticks performed.
    pub fn run_until_idle(&mut self) -> u64 {
        let mut ticks = 0u64;
        loop {
            let mut progress = false;
            // 1. Deliver queued commands.
            {
                let mut q = self.queue.lock().expect("sim queue lock poisoned");
                while let Some((shard, cmd)) = q.pop_front() {
                    self.engines[shard].borrow_mut().submit(cmd);
                    progress = true;
                }
            }
            // 2. Tick engines; spawn dispatched steps; schedule wake tasks.
            let mut engine_deadline: Option<LogicalTime> = None;
            for (shard, eng) in self.engines.iter().enumerate() {
                let TickOutput {
                    dispatches,
                    next_wake,
                } = eng.borrow_mut().tick();
                ticks += 1;
                for d in dispatches {
                    progress = true;
                    let queue = Arc::clone(&self.queue);
                    let wf = d.workflow.clone();
                    let (seq, attempt, fut) = (d.seq, d.attempt, d.fut);
                    self.exec.spawn(async move {
                        let outcome = fut.await;
                        queue.lock().expect("sim queue lock poisoned").push_back((
                            shard,
                            EngineCmd::StepFinished {
                                id: wf,
                                seq,
                                attempt,
                                outcome,
                            },
                        ));
                    });
                }
                if let Some(w) = next_wake {
                    engine_deadline = Some(engine_deadline.map_or(w, |d: LogicalTime| d.min(w)));
                }
            }
            // An engine deadline becomes an executor timer via a no-op wake
            // task, so virtual time stops exactly there.
            if let Some(deadline) = engine_deadline {
                let key = deadline.as_millis();
                if deadline > self.now() && !self.scheduled_wakes.contains_key(&key) {
                    self.scheduled_wakes.insert(key, ());
                    let sleeper = self.exec.sleep_until(deadline);
                    self.exec.spawn(async move {
                        sleeper.await;
                    });
                } else if deadline <= self.now() {
                    progress = true; // due now: tick again next iteration
                }
            }
            self.scheduled_wakes = self
                .scheduled_wakes
                .split_off(&(self.now().as_millis() + 1));
            // 3. One executor scheduling step (a task poll or a virtual time
            // advance). Steps may enqueue commands, picked up next iteration.
            let exec_progress = self.exec.step();
            if !progress && !exec_progress {
                let queue_empty = self
                    .queue
                    .lock()
                    .expect("sim queue lock poisoned")
                    .is_empty();
                if queue_empty {
                    return ticks;
                }
            }
        }
    }

    /// Run for a bounded amount of virtual time (advancing the clock at the
    /// end if the system went idle earlier).
    pub fn run_for(&mut self, d: Duration) {
        let target = self.now() + d;
        while self.now() < target {
            self.run_until_idle();
            if self.now() < target {
                // Nothing left to do before target: jump.
                self.clock.advance_to(target);
                self.run_until_idle();
                break;
            }
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use sqrl_core::Ctx;
    use std::sync::atomic::{AtomicU32, Ordering};

    // A tiny in-memory Storage for scheduler unit tests (the real WAL-backed
    // sim tests live in the workspace `tests` crate).
    mod mem {
        use sqrl_core::snapshot::SnapshotRecord;
        use sqrl_core::storage::{AppendEntry, AppendPayload, JournalReadout, StorageStats};
        use sqrl_core::{JournalRecord, Storage, StorageError, StorageShard, WorkflowId};
        use std::collections::BTreeMap;
        use std::sync::{Arc, Mutex};

        #[derive(Default)]
        pub struct State {
            journals: BTreeMap<WorkflowId, Vec<JournalRecord>>,
            snapshots: BTreeMap<WorkflowId, SnapshotRecord>,
        }

        #[derive(Clone, Default)]
        pub struct Mem(pub Arc<Mutex<State>>);

        impl Storage for Mem {
            fn num_shards(&self) -> usize {
                1
            }
            fn open_shard(&self, _: usize) -> Result<Box<dyn StorageShard>, StorageError> {
                Ok(Box::new(MemShard(self.clone())))
            }
        }

        pub struct MemShard(Mem);

        impl StorageShard for MemShard {
            fn append(&mut self, entries: &[AppendEntry]) -> Result<(), StorageError> {
                let mut s = self.0 .0.lock().unwrap();
                for e in entries {
                    match &e.payload {
                        AppendPayload::Record(r) => s
                            .journals
                            .entry(e.workflow.clone())
                            .or_default()
                            .push(r.clone()),
                        AppendPayload::Snapshot(sn) => {
                            s.snapshots.insert(e.workflow.clone(), sn.clone());
                        }
                    }
                }
                Ok(())
            }
            fn sync(&mut self) -> Result<(), StorageError> {
                Ok(())
            }
            fn read(&mut self, wf: &WorkflowId) -> Result<JournalReadout, StorageError> {
                let s = self.0 .0.lock().unwrap();
                let snapshot = s.snapshots.get(wf).cloned();
                let cut = snapshot.as_ref().map(|x| x.upto).unwrap_or(0);
                Ok(JournalReadout {
                    snapshot,
                    records: s
                        .journals
                        .get(wf)
                        .map(|v| v.iter().filter(|r| r.index >= cut).cloned().collect())
                        .unwrap_or_default(),
                })
            }
            fn list(&mut self) -> Result<Vec<WorkflowId>, StorageError> {
                Ok(self.0 .0.lock().unwrap().journals.keys().cloned().collect())
            }
            fn maintain(&mut self) -> Result<(), StorageError> {
                Ok(())
            }
            fn stats(&self) -> StorageStats {
                StorageStats::default()
            }
        }
    }

    fn registry(counter: Arc<AtomicU32>) -> Arc<Registry> {
        let mut reg = Registry::new();
        reg.register("wf", 1, move |ctx: Ctx, n: u64| {
            let counter = Arc::clone(&counter);
            async move {
                let c = Arc::clone(&counter);
                let doubled: u64 = ctx
                    .step("double", move || {
                        let c = Arc::clone(&c);
                        async move {
                            c.fetch_add(1, Ordering::SeqCst);
                            Ok::<u64, String>(n * 2)
                        }
                    })
                    .await?;
                ctx.sleep(Duration::from_secs(30)).await?;
                Ok(doubled + 1)
            }
        });
        Arc::new(reg)
    }

    #[test]
    fn full_stack_workflow_completes_under_sim() {
        let counter = Arc::new(AtomicU32::new(0));
        let store = mem::Mem::default();
        let mut sim = SimScheduler::new(
            7,
            &store,
            registry(Arc::clone(&counter)),
            EngineConfig::default(),
        )
        .unwrap();
        let handle = sim.start("wf-1", "wf", &21u64).unwrap();
        sim.run_until_idle();
        let out: u64 = handle.result_blocking().unwrap();
        assert_eq!(out, 43);
        assert_eq!(counter.load(Ordering::SeqCst), 1);
        assert!(
            sim.now() >= LogicalTime::from_millis(31_000),
            "virtual 30s sleep elapsed"
        );
    }

    #[test]
    fn same_seed_same_metrics_and_time() {
        let run = |seed: u64| {
            let counter = Arc::new(AtomicU32::new(0));
            let store = mem::Mem::default();
            let mut sim =
                SimScheduler::new(seed, &store, registry(counter), EngineConfig::default())
                    .unwrap();
            for i in 0..10 {
                sim.start(format!("wf-{i}"), "wf", &(i as u64)).unwrap();
            }
            sim.run_until_idle();
            (sim.now(), sim.metrics())
        };
        assert_eq!(run(11), run(11));
    }
}
