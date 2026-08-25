//! Workflow handles: observe a workflow's terminal result from any thread or
//! async runtime.

use crate::codec;
use crate::error::Error;
use crate::id::WorkflowId;
use crate::sync::Waiter;
use serde::de::DeserializeOwned;

/// The raw terminal outcome of a workflow: serialized output or error.
pub type TerminalResult = Result<Vec<u8>, Error>;

/// A handle to one workflow execution.
///
/// The handle resolves only once the terminal record is **durable** per the
/// engine's fsync policy — a completed `result()` means the completion
/// survives `kill -9`.
#[derive(Clone)]
pub struct WorkflowHandle {
    id: WorkflowId,
    waiter: Waiter<TerminalResult>,
}

impl core::fmt::Debug for WorkflowHandle {
    fn fmt(&self, f: &mut core::fmt::Formatter<'_>) -> core::fmt::Result {
        f.debug_struct("WorkflowHandle")
            .field("id", &self.id)
            .finish_non_exhaustive()
    }
}

impl WorkflowHandle {
    /// Build a handle (engine-internal).
    pub fn new(id: WorkflowId, waiter: Waiter<TerminalResult>) -> Self {
        WorkflowHandle { id, waiter }
    }

    /// The workflow's id.
    pub fn id(&self) -> &WorkflowId {
        &self.id
    }

    /// Await the typed result. Runtime-agnostic: awaitable from Tokio, the
    /// simulator, or any executor.
    pub async fn result<O: DeserializeOwned>(&self) -> Result<O, Error> {
        let raw = self.waiter.clone().await?;
        codec::from_slice(&raw, "workflow output")
    }

    /// Block the current thread for the typed result. Never call from async
    /// code.
    pub fn result_blocking<O: DeserializeOwned>(&self) -> Result<O, Error> {
        let raw = self.waiter.wait_blocking()?;
        codec::from_slice(&raw, "workflow output")
    }

    /// The terminal outcome if already resolved.
    pub fn peek(&self) -> Option<TerminalResult> {
        self.waiter.peek()
    }
}
