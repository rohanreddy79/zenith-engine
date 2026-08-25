//! Snapshots: compacted workflow history.
//!
//! Rust cannot serialize a suspended future, so a sqrl snapshot is **not** a
//! continuation — it is the workflow's history compacted to exactly what
//! replay needs (ADR 0006), split in two parts:
//!
//! * [`SnapshotMeta`] — small: start info, in-flight steps, pending timers,
//!   terminal status, workflow time. Enough to *recover* a workflow (re-arm
//!   its timers, know what is in flight) without touching the rest.
//! * the **body** ([`SnapshotBody`], stored as raw bytes) — the command
//!   descriptors and the ordered *revelation stream* of outcomes. Decoded
//!   only when the workflow must actually run again (lazy materialization);
//!   an idle workflow recovers in O(meta), not O(history).
//!
//! The revelation stream keeps outcome order so `select!`-style races replay
//! identically. Replaying from a snapshot re-runs orchestration code from
//! the top, serving commands from the body instead of decoding the journal.
//! Journal records with `index < upto` are dead and their segments become
//! GC-eligible once the snapshot is fsync-durable.

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
    /// Cheap-to-decode recovery metadata.
    pub meta: SnapshotMeta,
    /// Serialized [`SnapshotBody`] (self-describing MessagePack), decoded
    /// lazily on materialization.
    #[serde(with = "serde_bytes_compat")]
    pub body: Vec<u8>,
}

// rmp-serde encodes Vec<u8> efficiently either way; this module keeps the
// field explicit for format documentation purposes.
mod serde_bytes_compat {
    use serde::{Deserializer, Serializer};
    pub fn serialize<S: Serializer>(v: &[u8], s: S) -> Result<S::Ok, S::Error> {
        s.serialize_bytes(v)
    }
    pub fn deserialize<'de, D: Deserializer<'de>>(d: D) -> Result<Vec<u8>, D::Error> {
        serde_bytes_like(d)
    }
    fn serde_bytes_like<'de, D: Deserializer<'de>>(d: D) -> Result<Vec<u8>, D::Error> {
        struct V;
        impl<'de> serde::de::Visitor<'de> for V {
            type Value = Vec<u8>;
            fn expecting(&self, f: &mut core::fmt::Formatter<'_>) -> core::fmt::Result {
                f.write_str("bytes")
            }
            fn visit_bytes<E: serde::de::Error>(self, v: &[u8]) -> Result<Vec<u8>, E> {
                Ok(v.to_vec())
            }
            fn visit_byte_buf<E: serde::de::Error>(self, v: Vec<u8>) -> Result<Vec<u8>, E> {
                Ok(v)
            }
            fn visit_seq<A: serde::de::SeqAccess<'de>>(
                self,
                mut seq: A,
            ) -> Result<Vec<u8>, A::Error> {
                let mut out = Vec::with_capacity(seq.size_hint().unwrap_or(0));
                while let Some(b) = seq.next_element::<u8>()? {
                    out.push(b);
                }
                Ok(out)
            }
        }
        d.deserialize_byte_buf(V)
    }
}

/// Recovery metadata: everything needed to resume *scheduling* a workflow
/// (not to run its code).
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize, Default)]
pub struct SnapshotMeta {
    /// Start info: (name, version, input, seed, started_at).
    pub start: Option<StartInfo>,
    /// Steps scheduled but not resolved: seq → (name, failed attempts so
    /// far, next retry time if a retry was pending).
    pub inflight_steps: BTreeMap<u64, InflightStep>,
    /// Timers armed but not fired: seq → fire_at.
    pub pending_timers: BTreeMap<u64, LogicalTime>,
    /// Terminal status, if the workflow finished.
    pub terminal: Option<TerminalStatus>,
    /// Logical time of the last record covered by the snapshot.
    pub wf_time: LogicalTime,
}

/// The replay state proper: decoded only when the workflow materializes.
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize, Default)]
pub struct SnapshotBody {
    /// Every command descriptor issued so far, by command seq.
    pub cmds: BTreeMap<u64, CmdDesc>,
    /// The revelation stream, in original order.
    pub outcomes: Vec<Outcome>,
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

impl SnapshotRecord {
    /// Build a record from meta + body (serializing the body).
    pub fn build(
        upto: u64,
        meta: SnapshotMeta,
        body: &SnapshotBody,
    ) -> Result<Self, crate::error::Error> {
        let body = crate::codec::to_vec(body, "snapshot body")?;
        Ok(SnapshotRecord { upto, meta, body })
    }

    /// Decode the body (materialization).
    pub fn decode_body(&self) -> Result<SnapshotBody, crate::error::Error> {
        if self.body.is_empty() {
            return Ok(SnapshotBody::default());
        }
        crate::codec::from_slice(&self.body, "snapshot body")
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn snapshot_round_trip_with_lazy_body() {
        let mut cmds = BTreeMap::new();
        cmds.insert(0, CmdDesc::Step { name: "a".into() });
        cmds.insert(1, CmdDesc::Timer);
        let body = SnapshotBody {
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
        };
        let meta = SnapshotMeta {
            start: Some(StartInfo {
                name: "wf".into(),
                version: 1,
                input: vec![1, 2],
                seed: 42,
                started_at: LogicalTime::from_millis(5),
            }),
            inflight_steps: BTreeMap::new(),
            pending_timers: BTreeMap::new(),
            terminal: None,
            wf_time: LogicalTime::from_millis(100),
        };
        let rec = SnapshotRecord::build(7, meta.clone(), &body).unwrap();
        let bytes = crate::codec::to_vec(&rec, "snapshot").unwrap();
        let back: SnapshotRecord = crate::codec::from_slice(&bytes, "snapshot").unwrap();
        assert_eq!(back.upto, 7);
        assert_eq!(back.meta, meta);
        assert_eq!(back.decode_body().unwrap(), body);
    }

    #[test]
    fn empty_body_decodes_to_default() {
        let rec = SnapshotRecord {
            upto: 0,
            meta: SnapshotMeta::default(),
            body: Vec::new(),
        };
        assert_eq!(rec.decode_body().unwrap(), SnapshotBody::default());
    }
}
