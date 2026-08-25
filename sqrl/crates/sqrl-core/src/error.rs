//! Error types for the sqrl engine.
//!
//! Library errors are typed (`thiserror`); orchestration-visible errors are
//! serializable so they can be journaled and replayed deterministically.

use crate::event::CmdDesc;
use crate::state::StateKind;
use serde::{Deserialize, Serialize};
use thiserror::Error;

/// The error type returned by workflow orchestration code and by workflow
/// handles.
#[derive(Debug, Clone, PartialEq, Eq, Error, Serialize, Deserialize)]
pub enum Error {
    /// A step exhausted its retry policy (or hit a non-retryable error).
    #[error("step `{name}` (seq {seq}) failed after {attempts} attempt(s): {error}")]
    StepFailed {
        /// Step name as passed to `ctx.step`.
        name: String,
        /// Command sequence number of the step.
        seq: u64,
        /// Number of attempts made.
        attempts: u32,
        /// The final attempt's error.
        error: StepError,
    },
    /// The workflow was cancelled.
    #[error("workflow cancelled")]
    Cancelled,
    /// Replay diverged from the journal: the code is no longer the code that
    /// wrote the history. See `docs/versioning-and-patching.md`.
    #[error(transparent)]
    NonDeterminism(#[from] NonDeterminismError),
    /// An application-level error raised by orchestration code.
    #[error("workflow error: {0}")]
    App(String),
    /// Orchestration code panicked. This is a bug in the workflow definition
    /// (steps catch panics; orchestration must not panic).
    #[error("orchestration code panicked: {0}")]
    OrchestrationPanic(String),
    /// A payload exceeded the configured size limit.
    #[error("payload too large: {size} bytes exceeds limit of {limit} bytes in {context}; store the blob externally and journal a reference")]
    PayloadTooLarge {
        /// Actual serialized size.
        size: usize,
        /// Configured limit.
        limit: usize,
        /// What was being serialized (step result, input, signal, ...).
        context: String,
    },
    /// A payload failed to serialize or deserialize.
    #[error("serialization error in {context}: {message}")]
    Codec {
        /// What was being (de)serialized.
        context: String,
        /// Codec error message.
        message: String,
    },
    /// The underlying storage failed.
    #[error("storage error: {0}")]
    Storage(#[from] StorageError),
}

impl Error {
    /// Construct an application-level workflow error.
    pub fn app(msg: impl Into<String>) -> Self {
        Error::App(msg.into())
    }
}

/// Convenience alias used by workflow code.
pub type Result<T, E = Error> = core::result::Result<T, E>;

/// The journaled outcome of a failed step attempt.
#[derive(Debug, Clone, PartialEq, Eq, Error, Serialize, Deserialize)]
pub enum StepError {
    /// The step returned an application error (retryable per policy).
    #[error("{0}")]
    App(String),
    /// The step panicked (caught at the step boundary; retryable per policy).
    #[error("step panicked: {0}")]
    Panic(String),
    /// The step result could not be serialized, or exceeded the payload
    /// limit. Not retryable: retrying would deterministically fail again.
    #[error("step result not journalable: {0}")]
    ResultNotJournalable(String),
}

impl StepError {
    /// Whether the retry policy may retry this error.
    pub fn is_retryable(&self) -> bool {
        match self {
            StepError::App(_) | StepError::Panic(_) => true,
            StepError::ResultNotJournalable(_) => false,
        }
    }
}

/// Replay diverged from journaled history.
///
/// Raised when the workflow code, replayed over its own journal, issues a
/// command that does not match what the journal recorded at the same
/// sequence number — i.e. the code changed incompatibly since the history
/// was written. The workflow is moved to `Failed(NonDeterministic)` and is
/// **never** retried automatically.
#[derive(Debug, Clone, PartialEq, Eq, Error, Serialize, Deserialize)]
#[error("non-deterministic replay at seq {seq}: journal recorded {expected:?}, code issued {actual:?}; gate code changes with ctx.patched() (docs/versioning-and-patching.md)")]
pub struct NonDeterminismError {
    /// Sequence number at which replay diverged.
    pub seq: u64,
    /// What the journal recorded at this sequence number (`None`: the journal
    /// ended but the code issued more commands than history explains, or the
    /// code completed while history had more commands).
    pub expected: Option<CmdDesc>,
    /// What the replaying code issued (`None`: the code completed/stopped
    /// while the journal recorded further commands).
    pub actual: Option<CmdDesc>,
}

/// Storage-level failures.
#[derive(Debug, Clone, PartialEq, Eq, Error, Serialize, Deserialize)]
pub enum StorageError {
    /// A disk write or fsync failed. After this error the store halts new
    /// commits: nothing is acknowledged as durable once an fsync has failed.
    #[error("disk error: {0}")]
    Disk(String),
    /// The disk is full.
    #[error("disk full: {0}")]
    DiskFull(String),
    /// Stored data failed validation (checksum mismatch, bad magic, ...).
    /// Recovery truncates to the last valid record; this error is returned
    /// only when corruption makes the store unusable (e.g. corrupt manifest
    /// with no fallback).
    #[error("corrupt store: {0}")]
    Corrupt(String),
    /// Codec failure while encoding/decoding storage records.
    #[error("storage codec error: {0}")]
    Codec(String),
    /// The requested workflow does not exist in this store.
    #[error("unknown workflow: {0}")]
    UnknownWorkflow(String),
    /// The store was asked to do something it does not support.
    #[error("unsupported storage operation: {0}")]
    Unsupported(String),
}

/// Admission-control rejection.
#[derive(Debug, Clone, PartialEq, Eq, Error, Serialize, Deserialize)]
pub enum Rejected {
    /// The target shard is at its configured in-flight workflow limit.
    #[error("backpressure: shard {shard} is at its in-flight limit of {limit}")]
    Backpressure {
        /// Shard that rejected the work.
        shard: usize,
        /// The configured limit.
        limit: usize,
    },
    /// A workflow with this id already exists.
    #[error("workflow `{0}` already exists")]
    AlreadyExists(String),
    /// No workflow is registered under this name.
    #[error("no workflow registered under name `{0}`")]
    UnknownWorkflowName(String),
    /// The engine is shutting down or storage has failed permanently.
    #[error("engine unavailable: {0}")]
    Unavailable(String),
}

/// An illegal lifecycle state transition was attempted.
///
/// This is a typed error, never a panic, in production code (see
/// `docs/architecture.md` §state machine). Hitting it indicates an engine
/// bug; DST asserts it never occurs.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Error, Serialize, Deserialize)]
#[error("illegal workflow state transition: {from:?} -> {to:?}")]
pub struct IllegalTransition {
    /// State the workflow was in.
    pub from: StateKind,
    /// State the transition attempted to reach.
    pub to: StateKind,
}
