//! Core engine for `sqrl`: deterministic workflow orchestration, journal
//! events, replay, and the workflow lifecycle state machine.
//!
//! This crate is **sans-executor**: it contains no threads, no wall clock,
//! and no ambient entropy. Time comes from an injected [`Clock`], entropy
//! from an injected [`Entropy`] source, disk from the [`vfs::Vfs`] trait, and
//! scheduling from a driver (`sqrl-sim`'s deterministic simulator or the real
//! thread-per-core scheduler in the `sqrl` facade). That inversion is what
//! makes deterministic simulation testing a first-class feature.
#![forbid(unsafe_code)]
#![deny(missing_docs)]

pub mod codec;
pub mod config;
pub mod error;
pub mod event;
pub mod id;
pub mod inject;
pub mod retry;
pub mod snapshot;
pub mod state;
pub mod storage;
pub mod time;
pub mod vfs;

pub use codec::SQRL_FORMAT_VERSION;
pub use config::{EngineConfig, FsyncPolicy, StepOptions};
pub use error::{
    Error, IllegalTransition, NonDeterminismError, Rejected, Result, StepError, StorageError,
};
pub use event::{CmdDesc, JournalEvent, JournalRecord};
pub use id::{stable_hash, WorkflowId};
pub use inject::{Clock, DeterministicRng, Entropy};
pub use retry::RetryPolicy;
pub use snapshot::{SnapshotRecord, SnapshotState};
pub use state::{FailureKind, StateKind, WorkflowState};
pub use storage::{AppendEntry, AppendPayload, JournalReadout, Storage, StorageShard};
pub use time::LogicalTime;
