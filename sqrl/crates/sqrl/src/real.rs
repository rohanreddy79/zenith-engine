//! `RealScheduler`: the production thread-per-core driver.
//!
//! N executor threads (default: available cores), each exclusively owning
//! one [`EngineCore`] and one storage shard — shared-nothing, no work
//! stealing of orchestration. Workflows shard by `hash(id) % N`. Step
//! futures are the only thing that leaves a core: they run on a dedicated
//! Tokio multi-thread runtime (the *step pool*), and their results come back
//! as engine commands. The orchestration path itself never touches Tokio.
//!
//! With the `work-stealing` cargo feature the step pool is shared and sized
//! to all cores; without it each dispatch still lands on the shared pool but
//! the pool is sized per configuration. (Orchestration is thread-per-core in
//! both modes; the feature exists for Phase-2 skew benchmarking.)

use sqrl_core::engine::{EngineCmd, EngineCore, Scheduler};
use sqrl_core::{Clock, EngineConfig, Entropy, LogicalTime, Registry, Storage, StorageError};
use std::sync::atomic::{AtomicU64, Ordering};
use std::sync::{mpsc, Arc};
use std::thread::{self, JoinHandle, Thread};
use std::time::Duration;

/// Wall-clock [`Clock`] for production.
pub struct SystemClock;

impl Clock for SystemClock {
    fn now(&self) -> LogicalTime {
        // Justified ambient time: this IS the production clock injection
        // point. Everything downstream consumes LogicalTime.
        #[allow(clippy::disallowed_methods)]
        let ms = std::time::SystemTime::now()
            .duration_since(std::time::UNIX_EPOCH)
            .map(|d| d.as_millis() as u64)
            .unwrap_or(0);
        LogicalTime::from_millis(ms)
    }
}

/// OS-ish entropy for workflow seeds: hashes ASLR/allocation addresses,
/// wall-clock nanos, thread id, and a counter through SipHash. Not
/// cryptographic (documented); workflow seeds only need uniqueness.
pub struct OsEntropy {
    counter: AtomicU64,
}

impl OsEntropy {
    /// New entropy source.
    pub fn new() -> Self {
        OsEntropy {
            counter: AtomicU64::new(0),
        }
    }
}

impl Default for OsEntropy {
    fn default() -> Self {
        OsEntropy::new()
    }
}

impl Entropy for OsEntropy {
    fn next_u64(&self) -> u64 {
        use std::hash::{BuildHasher, Hash, Hasher};
        // RandomState carries process-wide random keys seeded by the OS.
        let state = std::collections::hash_map::RandomState::new();
        let mut h = state.build_hasher();
        // Justified ambient time: this IS the production entropy injection
        // point.
        #[allow(clippy::disallowed_methods)]
        std::time::SystemTime::now()
            .duration_since(std::time::UNIX_EPOCH)
            .map(|d| d.subsec_nanos())
            .unwrap_or(0)
            .hash(&mut h);
        self.counter.fetch_add(1, Ordering::Relaxed).hash(&mut h);
        std::thread::current().id().hash(&mut h);
        h.finish()
    }
}

struct CoreHandle {
    tx: mpsc::Sender<EngineCmd>,
    thread: Thread,
}

impl CoreHandle {
    fn send(&self, cmd: EngineCmd) {
        if self.tx.send(cmd).is_ok() {
            self.thread.unpark();
        }
    }
}

/// The production scheduler. Created via `Sqrl::builder()`.
pub struct RealScheduler {
    cores: Vec<CoreHandle>,
    joins: Vec<JoinHandle<()>>,
    step_rt: Option<tokio::runtime::Runtime>,
}

impl RealScheduler {
    /// Spawn `num_shards` core threads over `storage` plus the step pool.
    pub fn start(
        storage: Arc<dyn Storage>,
        registry: Arc<Registry>,
        config: EngineConfig,
        step_threads: usize,
    ) -> Result<Self, StorageError> {
        let num_shards = storage.num_shards();
        let step_rt = tokio::runtime::Builder::new_multi_thread()
            .worker_threads(step_threads.max(1))
            .thread_name("sqrl-step")
            .enable_all()
            .build()
            .map_err(|e| StorageError::Unsupported(format!("step pool: {e}")))?;
        let step_handle = step_rt.handle().clone();

        let mut cores = Vec::with_capacity(num_shards);
        let mut joins = Vec::with_capacity(num_shards);
        // Two-phase: spawn threads, wait for each to report open() result so
        // storage errors surface at build time, not first use.
        for shard in 0..num_shards {
            let (tx, rx) = mpsc::channel::<EngineCmd>();
            let (ready_tx, ready_rx) = mpsc::channel::<Result<(), StorageError>>();
            let storage = Arc::clone(&storage);
            let registry = Arc::clone(&registry);
            let config = config.clone();
            let step_handle = step_handle.clone();
            let self_tx = tx.clone();
            let join = thread::Builder::new()
                .name(format!("sqrl-core-{shard}"))
                .spawn(move || {
                    let shard_storage = match storage.open_shard(shard) {
                        Ok(s) => s,
                        Err(e) => {
                            let _ = ready_tx.send(Err(e));
                            return;
                        }
                    };
                    let engine = EngineCore::open(
                        shard,
                        registry,
                        shard_storage,
                        Arc::new(SystemClock),
                        Arc::new(OsEntropy::new()),
                        config,
                    );
                    let mut engine = match engine {
                        Ok(e) => e,
                        Err(e) => {
                            let _ = ready_tx.send(Err(e));
                            return;
                        }
                    };
                    let _ = ready_tx.send(Ok(()));
                    core_loop(&mut engine, &rx, &self_tx, &step_handle);
                })
                .map_err(|e| StorageError::Unsupported(format!("spawn core thread: {e}")))?;
            match ready_rx.recv() {
                Ok(Ok(())) => {}
                Ok(Err(e)) => return Err(e),
                Err(_) => {
                    return Err(StorageError::Unsupported(
                        "core thread died during startup".to_string(),
                    ))
                }
            }
            cores.push(CoreHandle {
                tx,
                thread: join.thread().clone(),
            });
            joins.push(join);
        }
        Ok(RealScheduler {
            cores,
            joins,
            step_rt: Some(step_rt),
        })
    }

    /// Route a command to its shard.
    pub fn submit_cmd(&self, cmd: EngineCmd) {
        let shard = cmd
            .workflow()
            .map(|id| id.shard(self.cores.len()))
            .unwrap_or(0);
        self.cores[shard].send(cmd);
    }

    /// Broadcast a command factory to every shard (status, shutdown).
    pub fn broadcast(&self, mut make: impl FnMut() -> EngineCmd) {
        for core in &self.cores {
            core.send(make());
        }
    }

    /// Number of shards.
    pub fn num_shards(&self) -> usize {
        self.cores.len()
    }

    /// Stop all cores (flushing and fsyncing first) and the step pool.
    pub fn shutdown(mut self) {
        self.shutdown_inner();
    }

    fn shutdown_inner(&mut self) {
        self.broadcast(|| EngineCmd::Shutdown);
        for join in self.joins.drain(..) {
            let _ = join.join();
        }
        if let Some(rt) = self.step_rt.take() {
            // Shutting a Tokio runtime down blocks and panics inside another
            // runtime's context; hand it to a plain thread either way.
            let done = thread::Builder::new()
                .name("sqrl-step-shutdown".to_string())
                .spawn(move || rt.shutdown_timeout(Duration::from_secs(5)));
            if let Ok(j) = done {
                let _ = j.join();
            }
        }
    }
}

impl Drop for RealScheduler {
    fn drop(&mut self) {
        if !self.joins.is_empty() {
            self.shutdown_inner();
        }
    }
}

impl Scheduler for RealScheduler {
    fn num_shards(&self) -> usize {
        self.cores.len()
    }

    fn submit(&self, cmd: EngineCmd) {
        self.submit_cmd(cmd);
    }
}

fn core_loop(
    engine: &mut EngineCore,
    rx: &mpsc::Receiver<EngineCmd>,
    self_tx: &mpsc::Sender<EngineCmd>,
    step_handle: &tokio::runtime::Handle,
) {
    let clock = SystemClock;
    let mut shutting_down = false;
    loop {
        let mut received = false;
        while let Ok(cmd) = rx.try_recv() {
            if matches!(cmd, EngineCmd::Shutdown) {
                shutting_down = true;
            }
            engine.submit(cmd);
            received = true;
        }
        let out = engine.tick();
        let dispatched = !out.dispatches.is_empty();
        for d in out.dispatches {
            let tx = self_tx.clone();
            let me = thread::current();
            let (wf, seq, attempt, fut) = (d.workflow, d.seq, d.attempt, d.fut);
            step_handle.spawn(async move {
                let outcome = fut.await;
                if tx
                    .send(EngineCmd::StepFinished {
                        id: wf,
                        seq,
                        attempt,
                        outcome,
                    })
                    .is_ok()
                {
                    me.unpark();
                }
            });
        }
        if shutting_down && out.next_wake.is_none() && !dispatched && !received {
            // Fully flushed and idle: exit. (In-flight steps keep next_wake
            // logic irrelevant — their results can no longer be journaled
            // after this point, which at-least-once semantics permit.)
            return;
        }
        if received || dispatched {
            continue;
        }
        match out.next_wake {
            Some(at) => {
                let now = clock.now();
                if at > now {
                    thread::park_timeout(at - now);
                }
            }
            None => {
                if shutting_down {
                    return;
                }
                thread::park();
            }
        }
    }
}
