//! Journal events: the per-workflow, append-only, typed event log.
//!
//! Everything the engine needs to reconstruct a workflow after a crash is a
//! record in this log. Records are serialized self-describing MessagePack
//! (see [`crate::codec`]) inside checksummed WAL envelopes (see
//! `docs/on-disk-format.md`).

use crate::error::{Error, StepError};
use crate::time::LogicalTime;
use serde::{Deserialize, Serialize};

/// One record in a workflow's journal.
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct JournalRecord {
    /// Per-workflow record index, starting at 0 and dense. Redundant with
    /// journal position; used to validate continuity and to address records
    /// (`sqrl fork --from-seq`).
    pub index: u64,
    /// Logical time the record was appended (the activation time of the
    /// engine when it processed the causing input). `ctx.now()` returns this
    /// timeline during replay.
    pub at: LogicalTime,
    /// The event.
    pub event: JournalEvent,
}

/// A typed journal event.
///
/// `seq` fields are **command sequence numbers**: orchestration code issues
/// commands (steps, timers, signal awaits, patches) numbered 0,1,2,… in
/// program order; replay validates that the code issues the same command
/// stream the journal recorded.
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub enum JournalEvent {
    /// The workflow was created.
    WorkflowStarted {
        /// Registered workflow name.
        name: String,
        /// Registered workflow version at start time.
        version: u32,
        /// Serialized input payload.
        input: Vec<u8>,
        /// Seed for the workflow's deterministic entropy stream
        /// (`ctx.random()`, `ctx.uuid()`, retry jitter).
        seed: u64,
    },
    /// A step command was issued and is about to be executed.
    StepScheduled {
        /// Command sequence number.
        seq: u64,
        /// Step name as passed to `ctx.step`.
        name: String,
    },
    /// A step attempt succeeded; `result` is the serialized return value.
    /// On replay the recorded result is returned without re-execution.
    StepCompleted {
        /// Command sequence number.
        seq: u64,
        /// Serialized step result.
        result: Vec<u8>,
    },
    /// A step attempt failed. If `retry_at` is set, the engine re-dispatches
    /// the step at that logical time; if `None`, the failure is final and
    /// surfaces to orchestration code.
    StepFailed {
        /// Command sequence number.
        seq: u64,
        /// The attempt's error.
        error: StepError,
        /// 1-based attempt number that failed.
        attempt: u32,
        /// When to retry, or `None` if the failure is final.
        retry_at: Option<LogicalTime>,
    },
    /// A durable timer was armed to fire at `fire_at` (logical time).
    TimerScheduled {
        /// Command sequence number.
        seq: u64,
        /// Logical fire time.
        fire_at: LogicalTime,
    },
    /// The timer armed at `seq` fired.
    TimerFired {
        /// Command sequence number of the corresponding `TimerScheduled`.
        seq: u64,
    },
    /// Orchestration code began awaiting a signal by name.
    SignalAwaited {
        /// Command sequence number.
        seq: u64,
        /// Signal name.
        name: String,
    },
    /// An external signal arrived (buffered until awaited; consumption order
    /// per name is arrival order).
    SignalReceived {
        /// Signal name.
        name: String,
        /// Serialized signal payload.
        payload: Vec<u8>,
    },
    /// A `ctx.patched(id)` gate evaluated to *active* for the first time.
    /// (An inactive gate journals nothing and consumes no `seq` — see
    /// `docs/versioning-and-patching.md`.)
    PatchRecorded {
        /// Command sequence number.
        seq: u64,
        /// Patch identifier.
        id: String,
    },
    /// The workflow function returned `Ok`; `output` is serialized.
    WorkflowCompleted {
        /// Serialized workflow output.
        output: Vec<u8>,
    },
    /// The workflow failed terminally.
    WorkflowFailed {
        /// The failure.
        error: Error,
    },
    /// The workflow was cancelled.
    WorkflowCancelled,
    /// A failed workflow was explicitly resumed (`sqrl resume`): the terminal
    /// failure is void; the failed step's attempt counter is reset.
    WorkflowResumed,
}

impl JournalEvent {
    /// The command descriptor of this event, if it is a command record.
    pub fn cmd_desc(&self) -> Option<(u64, CmdDesc)> {
        match self {
            JournalEvent::StepScheduled { seq, name } => {
                Some((*seq, CmdDesc::Step { name: name.clone() }))
            }
            JournalEvent::TimerScheduled { seq, .. } => Some((*seq, CmdDesc::Timer)),
            JournalEvent::SignalAwaited { seq, name } => {
                Some((*seq, CmdDesc::AwaitSignal { name: name.clone() }))
            }
            JournalEvent::PatchRecorded { seq, id } => {
                Some((*seq, CmdDesc::Patch { id: id.clone() }))
            }
            JournalEvent::WorkflowStarted { .. }
            | JournalEvent::StepCompleted { .. }
            | JournalEvent::StepFailed { .. }
            | JournalEvent::TimerFired { .. }
            | JournalEvent::SignalReceived { .. }
            | JournalEvent::WorkflowCompleted { .. }
            | JournalEvent::WorkflowFailed { .. }
            | JournalEvent::WorkflowCancelled
            | JournalEvent::WorkflowResumed => None,
        }
    }

    /// Short kind name for logs and `sqrl inspect`.
    pub fn kind(&self) -> &'static str {
        match self {
            JournalEvent::WorkflowStarted { .. } => "WorkflowStarted",
            JournalEvent::StepScheduled { .. } => "StepScheduled",
            JournalEvent::StepCompleted { .. } => "StepCompleted",
            JournalEvent::StepFailed { .. } => "StepFailed",
            JournalEvent::TimerScheduled { .. } => "TimerScheduled",
            JournalEvent::TimerFired { .. } => "TimerFired",
            JournalEvent::SignalAwaited { .. } => "SignalAwaited",
            JournalEvent::SignalReceived { .. } => "SignalReceived",
            JournalEvent::PatchRecorded { .. } => "PatchRecorded",
            JournalEvent::WorkflowCompleted { .. } => "WorkflowCompleted",
            JournalEvent::WorkflowFailed { .. } => "WorkflowFailed",
            JournalEvent::WorkflowCancelled => "WorkflowCancelled",
            JournalEvent::WorkflowResumed => "WorkflowResumed",
        }
    }
}

/// What a command *is*, for replay validation and non-determinism reporting.
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub enum CmdDesc {
    /// `ctx.step(name, …)`
    Step {
        /// Step name.
        name: String,
    },
    /// `ctx.sleep` / `ctx.sleep_until`
    Timer,
    /// `ctx.await_signal(name)`
    AwaitSignal {
        /// Signal name.
        name: String,
    },
    /// `ctx.patched(id)` (recorded only when the gate is active)
    Patch {
        /// Patch id.
        id: String,
    },
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::codec;

    #[test]
    fn record_round_trip() {
        let rec = JournalRecord {
            index: 3,
            at: LogicalTime::from_millis(1234),
            event: JournalEvent::StepFailed {
                seq: 2,
                error: StepError::App("boom".into()),
                attempt: 1,
                retry_at: Some(LogicalTime::from_millis(2000)),
            },
        };
        let bytes = codec::to_vec(&rec, "test").unwrap();
        let back: JournalRecord = codec::from_slice(&bytes, "test").unwrap();
        assert_eq!(rec, back);
    }

    #[test]
    fn cmd_desc_extraction() {
        let e = JournalEvent::StepScheduled {
            seq: 5,
            name: "charge".into(),
        };
        assert_eq!(
            e.cmd_desc(),
            Some((
                5,
                CmdDesc::Step {
                    name: "charge".into()
                }
            ))
        );
        assert_eq!(JournalEvent::WorkflowCancelled.cmd_desc(), None);
    }
}
