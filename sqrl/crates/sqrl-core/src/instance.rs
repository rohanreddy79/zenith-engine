//! Per-workflow replay state shared between the engine and [`crate::Ctx`].
//!
//! One `InstanceInner` cell exists per live workflow, owned jointly (via
//! `Rc<RefCell<…>>`) by the engine core and the `Ctx` handed to orchestration
//! code. Orchestration code *issues commands* against it; the engine *reveals
//! outcomes* into it, one activation at a time, in journal order — which is
//! exactly what makes replay deterministic even for `select!`-style races.

use crate::config::StepOptions;
use crate::error::{NonDeterminismError, StepError};
use crate::event::{CmdDesc, JournalEvent};
use crate::id::WorkflowId;
use crate::retry::RetryPolicy;
use crate::time::LogicalTime;
use std::collections::{BTreeMap, VecDeque};
use std::future::Future;
use std::pin::Pin;

/// A boxed, type-erased step future: resolves to serialized result bytes or
/// a journalable step error. Must be `Send` — steps run on the step pool.
pub type BoxStepFut = Pin<Box<dyn Future<Output = Result<Vec<u8>, StepError>> + Send + 'static>>;

/// A boxed step factory. `FnMut` so retries can re-create the future.
pub type StepClosure = Box<dyn FnMut() -> BoxStepFut + Send + 'static>;

/// A step registration produced by `ctx.step` on its first poll.
pub struct StepReg {
    /// Command seq.
    pub seq: u64,
    /// Step name.
    pub name: String,
    /// Per-step options.
    pub opts: StepOptions,
    /// The factory for the step's future.
    pub closure: StepClosure,
}

/// A resolved command outcome, consumable exactly once by its future.
#[derive(Debug, Clone, PartialEq)]
pub enum Resolution {
    /// Step succeeded with serialized result bytes.
    StepOk(Vec<u8>),
    /// Step failed terminally.
    StepErr {
        /// The final error.
        error: StepError,
        /// Attempts made.
        attempts: u32,
    },
    /// Timer fired.
    Timer,
}

/// What the workflow future was waiting on when it last returned `Pending`.
#[derive(Debug, Clone, PartialEq)]
pub enum Waiting {
    /// Nothing recorded (either running or just polled).
    None,
    /// Awaiting the step with this seq.
    Step(u64),
    /// Sleeping on the timer with this seq.
    Timer(u64),
    /// Blocked on a signal by name (seq of the await command).
    Signal(String, u64),
}

/// Result of issuing a command against history.
#[derive(Debug, Clone, PartialEq)]
pub enum Issue {
    /// The command matches history at this seq (replay); do not journal.
    Replayed(u64),
    /// The command is new (live); journal it.
    Live(u64),
    /// Replay diverged; the error has been recorded on the cell.
    Diverged,
}

/// The shared per-workflow cell. Crate-internal: users interact through
/// [`crate::Ctx`].
pub struct InstanceInner {
    /// Workflow id.
    pub id: WorkflowId,
    /// Registered name.
    pub name: String,
    /// Version journaled at start.
    pub version: u32,
    /// Journaled deterministic seed.
    pub seed: u64,
    /// Payload size limit.
    pub max_payload: usize,
    /// Default retry policy (engine config).
    pub default_retry: RetryPolicy,
    /// Workflow-visible logical time (time of the last processed record).
    pub wf_time: LogicalTime,
    /// Next command seq the orchestration code will issue.
    pub next_seq: u64,
    /// Every command descriptor known (history + live), by seq.
    pub cmds: BTreeMap<u64, CmdDesc>,
    /// Highest seq present in `cmds`.
    pub max_cmd_seq: Option<u64>,
    /// Recorded fire times for timers (validation + re-arming).
    pub timer_targets: BTreeMap<u64, LogicalTime>,
    /// Revealed-but-unconsumed outcomes.
    pub resolved: BTreeMap<u64, Resolution>,
    /// Revealed-but-unconsumed signals, per name, in arrival order
    /// (payload bytes).
    pub signal_buf: BTreeMap<String, VecDeque<Vec<u8>>>,
    /// Sticky `ctx.patched` decisions.
    pub patches: BTreeMap<String, bool>,
    /// Number of history outcomes not yet revealed (engine-maintained).
    /// While nonzero, the code is replaying and must not diverge.
    pub unrevealed: usize,
    /// Deterministic draw counters (reset per execution incarnation; replay
    /// re-runs code from the top so streams realign).
    pub rng_counter: u64,
    /// Counter for `ctx.uuid()`.
    pub uuid_counter: u64,
    /// Counter for `ctx.idempotency_key()`.
    pub idem_counter: u64,
    /// Events to journal, drained by the engine after each poll.
    pub new_events: Vec<JournalEvent>,
    /// Step registrations, drained by the engine after each poll.
    pub new_steps: Vec<StepReg>,
    /// Timer arm requests `(seq, fire_at)`, drained after each poll.
    pub new_timers: Vec<(u64, LogicalTime)>,
    /// What the future is waiting on (best effort, set by primitives).
    pub waiting: Waiting,
    /// Replay divergence detected inside a `Ctx` call.
    pub nd_error: Option<NonDeterminismError>,
}

impl InstanceInner {
    /// Fresh cell for a new or recovering workflow.
    #[allow(clippy::too_many_arguments)]
    pub fn new(
        id: WorkflowId,
        name: String,
        version: u32,
        seed: u64,
        max_payload: usize,
        default_retry: RetryPolicy,
        started_at: LogicalTime,
    ) -> Self {
        InstanceInner {
            id,
            name,
            version,
            seed,
            max_payload,
            default_retry,
            wf_time: started_at,
            next_seq: 0,
            cmds: BTreeMap::new(),
            max_cmd_seq: None,
            timer_targets: BTreeMap::new(),
            resolved: BTreeMap::new(),
            signal_buf: BTreeMap::new(),
            patches: BTreeMap::new(),
            unrevealed: 0,
            rng_counter: 0,
            uuid_counter: 0,
            idem_counter: 0,
            new_events: Vec::new(),
            new_steps: Vec::new(),
            new_timers: Vec::new(),
            waiting: Waiting::None,
            nd_error: None,
        }
    }

    /// Record a known command (loading history).
    pub fn load_cmd(&mut self, seq: u64, desc: CmdDesc) {
        self.max_cmd_seq = Some(self.max_cmd_seq.map_or(seq, |m| m.max(seq)));
        self.cmds.insert(seq, desc);
    }

    /// True when the code is at the live frontier for `seq`: nothing left to
    /// reveal and no recorded command at or beyond `seq`.
    pub fn at_live_frontier(&self, seq: u64) -> bool {
        self.unrevealed == 0 && self.max_cmd_seq.is_none_or(|m| seq > m)
    }

    /// Issue a command: match against history or go live. On divergence the
    /// error is recorded in `nd_error` and `Issue::Diverged` is returned.
    pub fn issue(&mut self, actual: CmdDesc) -> Issue {
        let seq = self.next_seq;
        match self.cmds.get(&seq) {
            Some(recorded) if *recorded == actual => {
                self.next_seq += 1;
                Issue::Replayed(seq)
            }
            Some(recorded) => {
                self.nd_error = Some(NonDeterminismError {
                    seq,
                    expected: Some(recorded.clone()),
                    actual: Some(actual),
                });
                Issue::Diverged
            }
            None => {
                if self.at_live_frontier(seq) {
                    self.next_seq += 1;
                    self.load_cmd(seq, actual);
                    Issue::Live(seq)
                } else {
                    // History still has unrevealed outcomes or later
                    // commands, yet the code is issuing something the journal
                    // never recorded at this position.
                    self.nd_error = Some(NonDeterminismError {
                        seq,
                        expected: None,
                        actual: Some(actual),
                    });
                    Issue::Diverged
                }
            }
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    fn inner() -> InstanceInner {
        InstanceInner::new(
            WorkflowId::new("wf"),
            "test".into(),
            1,
            42,
            1024,
            RetryPolicy::default(),
            LogicalTime::ZERO,
        )
    }

    #[test]
    fn live_issue_records_command() {
        let mut i = inner();
        let r = i.issue(CmdDesc::Step { name: "a".into() });
        assert_eq!(r, Issue::Live(0));
        assert_eq!(i.next_seq, 1);
        assert_eq!(i.cmds.get(&0), Some(&CmdDesc::Step { name: "a".into() }));
    }

    #[test]
    fn replay_matches_history() {
        let mut i = inner();
        i.load_cmd(0, CmdDesc::Step { name: "a".into() });
        let r = i.issue(CmdDesc::Step { name: "a".into() });
        assert_eq!(r, Issue::Replayed(0));
        assert!(i.nd_error.is_none());
    }

    #[test]
    fn divergence_on_name_change() {
        let mut i = inner();
        i.load_cmd(0, CmdDesc::Step { name: "a".into() });
        let r = i.issue(CmdDesc::Step { name: "b".into() });
        assert_eq!(r, Issue::Diverged);
        let nd = i.nd_error.expect("nd error must be recorded");
        assert_eq!(nd.seq, 0);
        assert_eq!(nd.expected, Some(CmdDesc::Step { name: "a".into() }));
        assert_eq!(nd.actual, Some(CmdDesc::Step { name: "b".into() }));
    }

    #[test]
    fn divergence_on_kind_change() {
        let mut i = inner();
        i.load_cmd(0, CmdDesc::Timer);
        let r = i.issue(CmdDesc::Step { name: "a".into() });
        assert_eq!(r, Issue::Diverged);
    }

    #[test]
    fn new_command_mid_replay_diverges() {
        let mut i = inner();
        i.load_cmd(0, CmdDesc::Step { name: "a".into() });
        i.unrevealed = 1; // outcome for step 0 still unrevealed
        i.next_seq = 1;
        let r = i.issue(CmdDesc::Step { name: "x".into() });
        assert_eq!(r, Issue::Diverged);
    }
}
