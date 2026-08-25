//! Snapshots: compacted workflow history.
//!
//! Rust cannot serialize a suspended future, so a sqrl snapshot is **not** a
//! continuation — it is the workflow's history compacted to exactly what
//! replay needs (ADR 0006):
//!
//! * the command descriptors ever issued (for non-determinism validation),
//! * the *revelation stream*: outcomes (step results, timer fires, signal
//!   arrivals) in their original order — order matters so that `select!`-style
//!   races replay identically,
//! * in-flight work to resurrect (unfinished steps with attempt counts,
//!   armed timers),
//! * start info and terminal status.
//!
//! Replaying from a snapshot re-runs orchestration code from the top, serving
//! commands from the snapshot instead of decoding the full journal. Old
//! journal records before a snapshot are dead and their segments become
//! GC-eligible.

use crate::error::StepError;
use crate::event::CmdDesc;
use crate::state::FailureKind;
use crate::time::LogicalTime;
use serde::{Deserialize, Serialize};
use std::collections::BTreeMap;

/// A snapshot record as stored (WAL record type 2, `SnapshotTaken` in the
/// journal's logical schema: `{ seq, state }` where `seq` is [`Self::upto`]).
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct SnapshotRecord {
    /// Journal records with `index < upto` are covered by this snapshot.
    pub upto: u64,
    /// The compacted state.
    pub state: SnapshotState,
}

/// Compacted history of one workflow.
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize, Default)]
pub struct SnapshotState {
    /// Start info: (name, version, input, seed, started_at).
    pub start: Option<StartInfo>,
    /// Every command descriptor issued so far, by command seq.
    pub cmds: BTreeMap<u64, CmdDesc>,
    /// The revelation stream, in original order.
    pub outcomes: Vec<Outcome>,
    /// Steps scheduled but not resolved: seq → (name, failed attempts so
    /// far, next retry time if a retry was pending).
    pub inflight_steps: BTreeMap<u64, InflightStep>,
    /// Timers armed but not fired: seq → fire_at.
    pub pending_timers: BTreeMap<u64, LogicalTime>,
    /// Terminal status, if the workflow finished.
    pub terminal: Option<TerminalStatus>,
    /// Logical time of the last record covered by the snapshot (workflow
    /// time resumes from here).
    pub wf_time: LogicalTime,
}

/// Start information for a workflow.
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct StartInfo {
    /// Registered workflow name.
    pub name: String,
    /// Workflow version at start.
    pub version: u32,
    /// Serialized input.
    pub input: Vec<u8>,
    /// Deterministic entropy seed.
    pub seed: u64,
    /// Logical start time.
    pub started_at: LogicalTime,
}

/// One entry of the revelation stream.
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub enum Outcome {
    /// A step resolved successfully.
    StepOk {
        /// Command seq.
        seq: u64,
        /// Serialized result.
        result: Vec<u8>,
        /// Logical time of resolution.
        at: LogicalTime,
    },
    /// A step failed terminally (retries exhausted or non-retryable).
    StepErr {
        /// Command seq.
        seq: u64,
        /// Final error.
        error: StepError,
        /// Total attempts made.
        attempts: u32,
        /// Logical time of resolution.
        at: LogicalTime,
    },
    /// A timer fired.
    TimerFired {
        /// Command seq.
        seq: u64,
        /// Logical fire time.
        at: LogicalTime,
    },
    /// A signal arrived (order across signals is arrival order).
    Signal {
        /// Signal name.
        name: String,
        /// Serialized payload.
        payload: Vec<u8>,
        /// Logical arrival time.
        at: LogicalTime,
    },
    /// The workflow was resumed after a terminal failure (`sqrl resume`).
    Resumed {
        /// Logical resume time.
        at: LogicalTime,
    },
}

/// An unresolved step at snapshot time.
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct InflightStep {
    /// Step name.
    pub name: String,
    /// Failed attempts so far.
    pub failed_attempts: u32,
    /// If a retry was scheduled, its fire time.
    pub retry_at: Option<LogicalTime>,
}

/// Terminal status stored in a snapshot.
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub enum TerminalStatus {
    /// Completed with serialized output.
    Completed {
        /// Serialized output.
        output: Vec<u8>,
    },
    /// Failed.
    Failed {
        /// The failure.
        failure: FailureKind,
    },
    /// Cancelled.
    Cancelled,
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::codec;

    #[test]
    fn snapshot_round_trip() {
        let mut cmds = BTreeMap::new();
        cmds.insert(0, CmdDesc::Step { name: "a".into() });
        cmds.insert(1, CmdDesc::Timer);
        let snap = SnapshotRecord {
            upto: 7,
            state: SnapshotState {
                start: Some(StartInfo {
                    name: "wf".into(),
                    version: 1,
                    input: vec![1, 2],
                    seed: 42,
                    started_at: LogicalTime::from_millis(5),
                }),
                cmds,
                outcomes: vec![
                    Outcome::StepOk {
                        seq: 0,
                        result: vec![9],
                        at: LogicalTime::from_millis(6),
                    },
                    Outcome::TimerFired {
                        seq: 1,
                        at: LogicalTime::from_millis(100),
                    },
                ],
                inflight_steps: BTreeMap::new(),
                pending_timers: BTreeMap::new(),
                terminal: None,
                wf_time: LogicalTime::from_millis(100),
            },
        };
        let bytes = codec::to_vec(&snap, "snapshot").unwrap();
        let back: SnapshotRecord = codec::from_slice(&bytes, "snapshot").unwrap();
        assert_eq!(snap, back);
    }
}
