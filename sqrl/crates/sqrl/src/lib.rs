//! `sqrl` — embedded, deterministic-first durable execution for Rust.
//!
//! Define workflows as async Rust functions; sqrl journals every step,
//! timer, and signal to an embedded write-ahead log, and if the process is
//! `kill -9`'d at any point, workflows resume from their last completed step
//! on restart. No server, no database, no cluster.
//!
//! ```no_run
//! use sqrl::{Ctx, FsyncPolicy, Result, Sqrl, WalStorage};
//! use std::time::Duration;
//!
//! #[sqrl::workflow(name = "greet", version = 1)]
//! async fn greet(ctx: &Ctx, name: String) -> Result<String> {
//!     let upper: String = ctx
//!         .step("upcase", move || {
//!             let name = name.clone();
//!             async move { Ok::<_, String>(name.to_uppercase()) }
//!         })
//!         .await?;
//!     ctx.sleep(Duration::from_secs(1)).await?;
//!     Ok(format!("hello, {upper}"))
//! }
//!
//! # fn main() -> Result<(), Box<dyn std::error::Error>> {
//! let sqrl = Sqrl::builder()
//!     .storage(WalStorage::open("./data")?)
//!     .fsync(FsyncPolicy::default_group())
//!     .register(greet)
//!     .build()?;
//! let handle = sqrl.start_blocking("greet", &"world".to_string())?;
//! let greeting: String = handle.result_blocking()?;
//! # Ok(()) }
//! ```
//!
//! **Guarantees**: at-least-once step execution plus idempotency helpers
//! ("effectively-once"). sqrl never claims exactly-once side effects — see
//! `docs/determinism-guide.md` and the README.
#![forbid(unsafe_code)]
#![deny(missing_docs)]

mod real;

pub use real::{OsEntropy, RealScheduler, SystemClock};
pub use sqrl_core::engine::{EngineCmd, Scheduler, StatusEntry};
pub use sqrl_core::sync::{promise, Completer, Waiter};
pub use sqrl_core::{
    codec, typed_def, Clock, Ctx, EngineConfig, Entropy, Error, FailureKind, FsyncPolicy,
    JournalEvent, JournalRecord, LogicalTime, NonDeterminismError, Registry, Rejected, Result,
    RetryPolicy, StateKind, StepError, StepOptions, Storage, TerminalResult, WorkflowDef,
    WorkflowDefProvider, WorkflowHandle, WorkflowId, SQRL_FORMAT_VERSION,
};
pub use sqrl_macros::{step, workflow};
pub use sqrl_store::{MemoryStorage, StdVfs, WalOptions, WalStorage};

use serde::Serialize;
use sqrl_core::handle::TerminalResult as RawTerminal;
use std::sync::Arc;

/// Builder for [`Sqrl`].
pub struct SqrlBuilder {
    storage: Option<Arc<dyn Storage>>,
    config: EngineConfig,
    registry: Registry,
    step_threads: Option<usize>,
}

impl SqrlBuilder {
    /// Set the storage backend ([`WalStorage`] for production,
    /// [`MemoryStorage`] for tests).
    pub fn storage(mut self, storage: impl Storage) -> Self {
        self.storage = Some(Arc::new(storage));
        self
    }

    /// Set the fsync policy (default: group commit, 2 ms / 256 records).
    pub fn fsync(mut self, policy: FsyncPolicy) -> Self {
        self.config.fsync = policy;
        self
    }

    /// Set the default step retry policy.
    pub fn retry(mut self, policy: RetryPolicy) -> Self {
        self.config.retry = policy;
        self
    }

    /// Journal records between automatic snapshots (default 1000).
    pub fn snapshot_every(mut self, records: u64) -> Self {
        self.config.snapshot_every = records;
        self
    }

    /// Maximum serialized payload size (default 1 MiB).
    pub fn max_payload(mut self, bytes: usize) -> Self {
        self.config.max_payload = bytes;
        self
    }

    /// Maximum live workflows per shard before backpressure (default 100k).
    pub fn max_active_per_shard(mut self, n: usize) -> Self {
        self.config.max_active_per_shard = n;
        self
    }

    /// Passivate idle workflows after this duration (`None` disables).
    pub fn passivate_after(mut self, after: Option<std::time::Duration>) -> Self {
        self.config.passivate_after = after;
        self
    }

    /// Threads in the step pool (default: available parallelism).
    pub fn step_threads(mut self, n: usize) -> Self {
        self.step_threads = Some(n);
        self
    }

    /// Register a `#[sqrl::workflow]` function.
    pub fn register<P: WorkflowDefProvider>(mut self, _witness: P) -> Self {
        self.registry.register_def(P::workflow_def());
        self
    }

    /// Register a workflow from a plain async closure/function.
    pub fn register_fn<I, O, F, Fut>(mut self, name: &str, version: u32, f: F) -> Self
    where
        I: serde::de::DeserializeOwned + 'static,
        O: Serialize + 'static,
        F: Fn(Ctx, I) -> Fut + Send + Sync + 'static,
        Fut: std::future::Future<Output = Result<O>> + 'static,
    {
        self.registry.register(name, version, f);
        self
    }

    /// Register a pre-built definition.
    pub fn register_def(mut self, def: WorkflowDef) -> Self {
        self.registry.register_def(def);
        self
    }

    /// Start the engine: opens all shards, recovers every non-terminal
    /// workflow, spawns core threads and the step pool.
    pub fn build(self) -> Result<Sqrl> {
        let storage = self
            .storage
            .ok_or_else(|| Error::App("SqrlBuilder: storage is required".to_string()))?;
        let step_threads = self.step_threads.unwrap_or_else(|| {
            std::thread::available_parallelism()
                .map(|n| n.get())
                .unwrap_or(2)
        });
        let sched =
            RealScheduler::start(storage, Arc::new(self.registry), self.config, step_threads)?;
        Ok(Sqrl { sched })
    }
}

/// The sqrl runtime: a handle to the thread-per-core engine.
///
/// Cheaply shareable behind an `Arc`; dropping the last handle shuts the
/// engine down (flushing and fsyncing first).
pub struct Sqrl {
    sched: RealScheduler,
}

impl Sqrl {
    /// Start building a runtime.
    pub fn builder() -> SqrlBuilder {
        SqrlBuilder {
            storage: None,
            config: EngineConfig::default(),
            registry: Registry::new(),
            step_threads: None,
        }
    }

    /// Start a workflow under an explicit unique id. The returned future is
    /// runtime-agnostic (await it from Tokio or anywhere else).
    pub async fn start_with_id<I: Serialize>(
        &self,
        id: impl Into<WorkflowId>,
        name: &str,
        input: &I,
    ) -> Result<WorkflowHandle> {
        let (id, admit, handle) = self.submit_start(id.into(), name, input)?;
        admit.await.map_err(Error::Rejected)?;
        let _ = id;
        Ok(handle)
    }

    /// Start a workflow with a generated id (`<name>-<random>`).
    pub async fn start<I: Serialize>(&self, name: &str, input: &I) -> Result<WorkflowHandle> {
        let id = WorkflowId::new(format!("{name}-{:016x}", OsEntropy::new().next_u64()));
        self.start_with_id(id, name, input).await
    }

    /// Blocking variant of [`Sqrl::start`] for non-async callers.
    pub fn start_blocking<I: Serialize>(&self, name: &str, input: &I) -> Result<WorkflowHandle> {
        let id = WorkflowId::new(format!("{name}-{:016x}", OsEntropy::new().next_u64()));
        self.start_with_id_blocking(id, name, input)
    }

    /// Blocking variant of [`Sqrl::start_with_id`].
    pub fn start_with_id_blocking<I: Serialize>(
        &self,
        id: impl Into<WorkflowId>,
        name: &str,
        input: &I,
    ) -> Result<WorkflowHandle> {
        let (_, admit, handle) = self.submit_start(id.into(), name, input)?;
        admit.wait_blocking().map_err(Error::Rejected)?;
        Ok(handle)
    }

    fn submit_start<I: Serialize>(
        &self,
        id: WorkflowId,
        name: &str,
        input: &I,
    ) -> Result<(WorkflowId, Waiter<Result<(), Rejected>>, WorkflowHandle)> {
        let input = codec::to_vec(input, "workflow input")?;
        let (admit_c, admit_w) = promise::<Result<(), Rejected>>();
        let (term_c, term_w) = promise::<RawTerminal>();
        self.sched.submit_cmd(EngineCmd::Start {
            id: id.clone(),
            name: name.to_string(),
            input,
            admit: admit_c,
            terminal: term_c,
        });
        Ok((id.clone(), admit_w, WorkflowHandle::new(id, term_w)))
    }

    /// Deliver a signal to a workflow (`ctx.await_signal` receives it).
    pub async fn signal<P: Serialize>(
        &self,
        id: impl Into<WorkflowId>,
        name: &str,
        payload: &P,
    ) -> Result<()> {
        let payload = codec::to_vec(payload, "signal payload")?;
        let (ack_c, ack_w) = promise::<Result<()>>();
        self.sched.submit_cmd(EngineCmd::Signal {
            id: id.into(),
            name: name.to_string(),
            payload,
            ack: ack_c,
        });
        ack_w.await
    }

    /// Blocking variant of [`Sqrl::signal`].
    pub fn signal_blocking<P: Serialize>(
        &self,
        id: impl Into<WorkflowId>,
        name: &str,
        payload: &P,
    ) -> Result<()> {
        let payload = codec::to_vec(payload, "signal payload")?;
        let (ack_c, ack_w) = promise::<Result<()>>();
        self.sched.submit_cmd(EngineCmd::Signal {
            id: id.into(),
            name: name.to_string(),
            payload,
            ack: ack_c,
        });
        ack_w.wait_blocking()
    }

    /// Cancel a workflow.
    pub async fn cancel(&self, id: impl Into<WorkflowId>) -> Result<()> {
        let (ack_c, ack_w) = promise::<Result<()>>();
        self.sched.submit_cmd(EngineCmd::Cancel {
            id: id.into(),
            ack: ack_c,
        });
        ack_w.await
    }

    /// Attach a handle to an existing workflow (running or terminal).
    pub async fn handle(&self, id: impl Into<WorkflowId>) -> Result<WorkflowHandle> {
        let id = id.into();
        let (term_c, term_w) = promise::<RawTerminal>();
        let (ack_c, ack_w) = promise::<Result<()>>();
        self.sched.submit_cmd(EngineCmd::Watch {
            id: id.clone(),
            terminal: term_c,
            ack: ack_c,
        });
        ack_w.await?;
        Ok(WorkflowHandle::new(id, term_w))
    }

    /// Blocking variant of [`Sqrl::handle`].
    pub fn handle_blocking(&self, id: impl Into<WorkflowId>) -> Result<WorkflowHandle> {
        let id = id.into();
        let (term_c, term_w) = promise::<RawTerminal>();
        let (ack_c, ack_w) = promise::<Result<()>>();
        self.sched.submit_cmd(EngineCmd::Watch {
            id: id.clone(),
            terminal: term_c,
            ack: ack_c,
        });
        ack_w.wait_blocking()?;
        Ok(WorkflowHandle::new(id, term_w))
    }

    /// Status of every workflow across all shards.
    pub async fn status(&self) -> Vec<StatusEntry> {
        let mut waiters = Vec::new();
        self.sched.broadcast(|| {
            let (c, w) = promise::<Vec<StatusEntry>>();
            waiters.push(w);
            EngineCmd::Status { reply: c }
        });
        let mut all = Vec::new();
        for w in waiters {
            all.extend(w.await);
        }
        all
    }

    /// Number of shards (engine cores).
    pub fn num_shards(&self) -> usize {
        self.sched.num_shards()
    }

    /// Shut down: flush + fsync every shard, stop core threads and the step
    /// pool. Dropping `Sqrl` does the same implicitly.
    pub fn shutdown(self) {
        self.sched.shutdown();
    }
}
