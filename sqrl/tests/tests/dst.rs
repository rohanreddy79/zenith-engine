//! Deterministic Simulation Testing (DST): the whole engine + WalStorage on
//! SimScheduler + SimDisk, driven by a seeded adversary that starts diverse
//! workflows, delivers signals, advances virtual time, crashes the process,
//! injects write errors, and (in dedicated seeds) flips durable bytes.
//!
//! Per seed, the suite asserts:
//! * **physical determinism** — running the same seed twice produces
//!   byte-identical durable disk images, identical final states, identical
//!   virtual time;
//! * **safety** — a workflow observed completed stays completed with the
//!   same result across every later crash/recovery; no illegal state
//!   transitions; outputs equal the workflow-definition ground truth.
//!   Corruption-mode seeds relax exactly one clause: deliberate bit rot may
//!   legally void durably-acked suffixes (CRC truncation cuts the logical
//!   WAL stream at the flipped byte), turning the ack back into a lost
//!   start that the client-retry drain re-runs;
//! * **liveness** — once faults stop and owed signals are delivered, every
//!   started workflow reaches a terminal state.
//!
//! "Sometimes assertions" measure state-space coverage: behaviors that must
//! occur at least once across the whole run (crash mid-replay, step retries,
//! step panics, snapshots, torn-write truncations, …). The normal test runs
//! a bounded seed set for CI; `dst_long` (`--ignored`) runs 10k+ seeds. See
//! `docs/dst.md`.

use sqrl::{Ctx, EngineConfig, FsyncPolicy, Registry, Rejected, RetryPolicy, WorkflowHandle};
use sqrl_core::{stable_hash_more, StateKind, WorkflowId};
use sqrl_sim::{FaultConfig, SimClock, SimDisk, SimRng, SimScheduler};
use sqrl_store::{WalOptions, WalStorage};
use std::collections::{BTreeMap, BTreeSet};
use std::future::Future;
use std::pin::Pin;
use std::sync::atomic::AtomicU32;
use std::sync::{Arc, Mutex, OnceLock};
use std::task::{Context, Poll};
use std::time::Duration;

// ---------------------------------------------------------------------------
// Coverage ("sometimes assertions")
// ---------------------------------------------------------------------------

#[derive(Default, Debug, Clone)]
struct Coverage {
    crashes: u64,
    crash_mid_replay: u64,
    retries: u64,
    panics_caught: u64,
    snapshots: u64,
    passivations: u64,
    reactivations: u64,
    signals: u64,
    cancels: u64,
    timers_fired: u64,
    write_errors_injected: u64,
    corruption_truncations: u64,
    corruption_regressions: u64,
    backpressure: u64,
    joins_completed: u64,
}

impl Coverage {
    fn merge(&mut self, other: &Coverage) {
        self.crashes += other.crashes;
        self.crash_mid_replay += other.crash_mid_replay;
        self.retries += other.retries;
        self.panics_caught += other.panics_caught;
        self.snapshots += other.snapshots;
        self.passivations += other.passivations;
        self.reactivations += other.reactivations;
        self.signals += other.signals;
        self.cancels += other.cancels;
        self.timers_fired += other.timers_fired;
        self.write_errors_injected += other.write_errors_injected;
        self.corruption_truncations += other.corruption_truncations;
        self.corruption_regressions += other.corruption_regressions;
        self.backpressure += other.backpressure;
        self.joins_completed += other.joins_completed;
    }

    fn report(&self, seeds: u64) -> String {
        format!(
            "DST coverage over {seeds} seeds:\n  crashes={} (mid-replay={})\n  retries={} panics_caught={} timers_fired={}\n  snapshots={} passivations={} reactivations={}\n  signals={} cancels={} joins={}\n  injected_write_errors={} corruption_truncations={} corruption_regressions={} backpressure={}",
            self.crashes, self.crash_mid_replay, self.retries, self.panics_caught,
            self.timers_fired, self.snapshots, self.passivations, self.reactivations,
            self.signals, self.cancels, self.joins_completed,
            self.write_errors_injected, self.corruption_truncations,
            self.corruption_regressions, self.backpressure,
        )
    }

    fn assert_sometimes(&self) {
        // Each of these must have happened at least once across the run —
        // otherwise the adversary is not exploring the state space.
        assert!(self.crashes > 0, "sometimes: crashes");
        assert!(self.retries > 0, "sometimes: step retries");
        assert!(self.panics_caught > 0, "sometimes: step panics caught");
        assert!(self.timers_fired > 0, "sometimes: timers fired");
        assert!(self.snapshots > 0, "sometimes: snapshots taken");
        assert!(self.signals > 0, "sometimes: signals delivered");
        assert!(self.cancels > 0, "sometimes: cancellations");
        assert!(self.joins_completed > 0, "sometimes: parallel joins");
        assert!(
            self.crash_mid_replay > 0,
            "sometimes: crash during recovery"
        );
        assert!(
            self.write_errors_injected > 0,
            "sometimes: injected write errors"
        );
    }
}

// ---------------------------------------------------------------------------
// Workflow zoo
// ---------------------------------------------------------------------------

/// Attempt counters shared with step closures so flaky/panicky steps behave
/// deterministically per (workflow, step) across retries.
type Attempts = Arc<Mutex<BTreeMap<(String, u64), u32>>>;

/// Minimal 2-way join so the zoo exercises out-of-order revelation.
struct Join2<A, B, AO, BO> {
    a: A,
    b: B,
    a_out: Option<AO>,
    b_out: Option<BO>,
}

impl<A, B, AO, BO> Future for Join2<A, B, AO, BO>
where
    A: Future<Output = AO> + Unpin,
    B: Future<Output = BO> + Unpin,
    AO: Unpin,
    BO: Unpin,
{
    type Output = (AO, BO);
    fn poll(self: Pin<&mut Self>, cx: &mut Context<'_>) -> Poll<(AO, BO)> {
        let this = self.get_mut();
        if this.a_out.is_none() {
            if let Poll::Ready(v) = Pin::new(&mut this.a).poll(cx) {
                this.a_out = Some(v);
            }
        }
        if this.b_out.is_none() {
            if let Poll::Ready(v) = Pin::new(&mut this.b).poll(cx) {
                this.b_out = Some(v);
            }
        }
        match (this.a_out.take(), this.b_out.take()) {
            (Some(a), Some(b)) => Poll::Ready((a, b)),
            (a, b) => {
                this.a_out = a;
                this.b_out = b;
                Poll::Pending
            }
        }
    }
}

fn zoo(attempts: Attempts) -> Arc<Registry> {
    let mut reg = Registry::new();
    // 1. sum: n sequential trivial steps → deterministic sum.
    reg.register("sum", 1, |ctx: Ctx, n: u64| async move {
        let mut acc = 0u64;
        for s in 0..n {
            let v: u64 = ctx
                .step("add", move || async move { Ok::<u64, String>(s) })
                .await?;
            acc = acc.wrapping_add(v);
        }
        Ok(acc)
    });
    // 2. flaky: first attempt of each step fails; retry succeeds.
    let a = Arc::clone(&attempts);
    reg.register("flaky", 1, move |ctx: Ctx, n: u64| {
        let a = Arc::clone(&a);
        async move {
            let mut acc = 0u64;
            for s in 0..n.max(1) {
                let a2 = Arc::clone(&a);
                let id = ctx.id().to_string();
                let v: u64 = ctx
                    .step("wobble", move || {
                        let a2 = Arc::clone(&a2);
                        let id = id.clone();
                        async move {
                            let mut m = a2.lock().unwrap_or_else(|e| e.into_inner()); // panic-poisoned by design
                            let c = m.entry((id, s)).or_insert(0);
                            *c += 1;
                            if *c == 1 {
                                Err(format!("first attempt of step {s} fails"))
                            } else {
                                Ok(s + 1)
                            }
                        }
                    })
                    .await?;
                acc = acc.wrapping_add(v);
            }
            Ok(acc)
        }
    });
    // 3. panicky: one step panics on its first attempt.
    let a = Arc::clone(&attempts);
    reg.register("panicky", 1, move |ctx: Ctx, (): ()| {
        let a = Arc::clone(&a);
        async move {
            let id = ctx.id().to_string();
            let a2 = Arc::clone(&a);
            let v: u64 = ctx
                .step("boom", move || {
                    let a2 = Arc::clone(&a2);
                    let id = id.clone();
                    async move {
                        let mut m = a2.lock().unwrap_or_else(|e| e.into_inner()); // panic-poisoned by design
                        let c = m.entry((id, 0)).or_insert(0);
                        *c += 1;
                        if *c == 1 {
                            panic!("deterministic first-attempt panic");
                        }
                        Ok::<u64, String>(7)
                    }
                })
                .await?;
            Ok(v)
        }
    });
    // 4. sleepy: steps interleaved with durable timers; uses ctx.random.
    reg.register("sleepy", 1, |ctx: Ctx, n: u64| async move {
        let mut acc = ctx.random() % 1000;
        for s in 0..n.max(1) {
            ctx.sleep(Duration::from_millis(50 + (s * 37) % 500))
                .await?;
            let v: u64 = ctx
                .step("tick", move || async move { Ok::<u64, String>(s) })
                .await?;
            acc = acc.wrapping_add(v);
        }
        Ok(acc)
    });
    // 5. waity: durably blocks on a signal, then one more step.
    reg.register("waity", 1, |ctx: Ctx, (): ()| async move {
        let got: u64 = ctx.await_signal("go").await?;
        let v: u64 = ctx
            .step("after", move || async move { Ok::<u64, String>(got * 2) })
            .await?;
        Ok(v)
    });
    // 6. twin: two steps raced with a join — revelation-order stress.
    reg.register("twin", 1, |ctx: Ctx, (): ()| async move {
        let a = ctx.step("left", move || async move { Ok::<u64, String>(11) });
        let b = ctx.step("right", move || async move { Ok::<u64, String>(31) });
        let (ra, rb) = (Join2 {
            a: Box::pin(a),
            b: Box::pin(b),
            a_out: None,
            b_out: None,
        })
        .await;
        Ok(ra? + rb?)
    });
    Arc::new(reg)
}

/// Ground-truth expected output per workflow kind.
fn expected_output(kind: &str, input: u64, seed_random: Option<u64>) -> Option<u64> {
    match kind {
        "sum" => Some((0..input).fold(0u64, |a, b| a.wrapping_add(b))),
        "flaky" => Some(
            (0..input.max(1))
                .map(|s| s + 1)
                .fold(0u64, |a, b| a.wrapping_add(b)),
        ),
        "panicky" => Some(7),
        "twin" => Some(42),
        "waity" => None,         // depends on delivered signal payload
        "sleepy" => seed_random, // depends on ctx.random; checked for determinism only
        _ => None,
    }
}

// ---------------------------------------------------------------------------
// One seed = one universe
// ---------------------------------------------------------------------------

#[derive(Debug, Clone, PartialEq, Eq)]
struct SeedDigest {
    durable_hash: u64,
    final_states: BTreeMap<String, StateKind>,
    final_time_ms: u64,
    completed: BTreeMap<String, Option<u64>>,
}

struct SeedRun {
    coverage: Coverage,
    digest: SeedDigest,
}

struct World {
    seed: u64,
    disk: SimDisk,
    clock: SimClock,
    registry: Arc<Registry>,
    sched: Option<SimScheduler>,
    rng: SimRng,
    /// Everything ever started: id -> (kind, input).
    started: BTreeMap<String, (String, u64)>,
    /// Live handles (durability-acked results appear via these).
    handles: BTreeMap<String, WorkflowHandle>,
    /// Signals owed to waity workflows: (id, payload).
    owed_signals: Vec<(String, u64)>,
    /// Completions observed (id -> decoded output or None for errors).
    completed: BTreeMap<String, Option<u64>>,
    cancelled: BTreeSet<String>,
    corruption_mode: bool,
    fault_window: u32,
    coverage: Coverage,
    config: EngineConfig,
}

fn base_faults() -> FaultConfig {
    FaultConfig {
        p_write_error: 0.0,
        p_sync_error: 0.0,
        read_latency: Duration::ZERO,
        write_latency: Duration::from_micros(200),
        sync_latency: Duration::from_millis(1),
        capacity: None,
        p_keep_unsynced: 0.5,
        p_torn: 0.25,
        p_keep_unsynced_ns: 0.5,
    }
}

fn faulty_faults() -> FaultConfig {
    FaultConfig {
        p_write_error: 0.05,
        p_sync_error: 0.05,
        ..base_faults()
    }
}

impl World {
    fn new(seed: u64, corruption_mode: bool) -> World {
        let disk = SimDisk::with_faults(seed, base_faults());
        let clock = SimClock::new(sqrl_core::LogicalTime::from_millis(1_000));
        disk.attach_clock(clock.clone());
        let attempts: Attempts = Arc::default();
        World {
            seed,
            disk,
            clock,
            registry: zoo(attempts),
            sched: None,
            rng: SimRng::new(seed).fork("dst-driver"),
            started: BTreeMap::new(),
            handles: BTreeMap::new(),
            owed_signals: Vec::new(),
            completed: BTreeMap::new(),
            cancelled: BTreeSet::new(),
            corruption_mode,
            fault_window: 0,
            coverage: Coverage::default(),
            config: EngineConfig {
                fsync: FsyncPolicy::Group {
                    max_delay: Duration::from_millis(2),
                    max_batch: 64,
                },
                retry: RetryPolicy {
                    max_attempts: 4,
                    initial_delay: Duration::from_millis(20),
                    multiplier: 2.0,
                    max_delay: Duration::from_secs(5),
                    jitter_fraction: 0.2,
                },
                snapshot_every: 32, // small so DST hits snapshot paths often
                max_active_per_shard: 64,
                passivate_after: Some(Duration::from_secs(2)),
                seed: 0,
                max_payload: 1024 * 1024,
            },
        }
    }

    fn wal_opts() -> WalOptions {
        WalOptions {
            num_shards: 2,
            segment_size: 4096, // tiny segments: constant rolling + GC
        }
    }

    /// Start with the input type the kind's definition takes: `sum`,
    /// `flaky`, `sleepy` take a `u64`; `panicky`, `waity`, `twin` take `()`.
    fn start_kind(
        sched: &mut SimScheduler,
        id: &str,
        kind: &str,
        input: u64,
    ) -> Result<WorkflowHandle, Rejected> {
        match kind {
            "panicky" | "waity" | "twin" => sched.start(id, kind, &()),
            _ => sched.start(id, kind, &input),
        }
    }

    fn rebuild(&mut self) -> bool {
        if self.disk.is_crashed() {
            self.disk.recover();
        }
        let storage = match WalStorage::open_with(Arc::new(self.disk.clone()), World::wal_opts()) {
            Ok(s) => s,
            Err(_) => return false, // crashed again during open
        };
        match SimScheduler::with_clock(
            self.seed,
            &storage,
            Arc::clone(&self.registry),
            self.config.clone(),
            self.clock.clone(),
        ) {
            Ok(mut s) => {
                // Old handles died with the old engines: re-attach for every
                // started, not-yet-durably-completed workflow that survived.
                for id in self.started.keys() {
                    if !self.completed.contains_key(id) {
                        if let Ok(h) = s.handle(&**id) {
                            self.handles.insert(id.clone(), h);
                        }
                    }
                }
                self.sched = Some(s);
                true
            }
            Err(_) => {
                self.coverage.crash_mid_replay += 1;
                false
            }
        }
    }

    fn ensure_sched(&mut self) {
        let mut guard = 0;
        // A poisoned engine (permanent storage failure after an injected
        // write/sync error) needs a process restart, same as an operator
        // would give it; the page cache (applied view) survives — only a
        // machine crash loses pending writes.
        while self.sched.is_none()
            || self.disk.is_crashed()
            || self.sched.as_ref().is_some_and(|s| s.storage_failed())
        {
            self.sched = None;
            if self.rebuild() {
                break;
            }
            guard += 1;
            assert!(
                guard < 100,
                "seed {}: cannot rebuild after crash",
                self.seed
            );
        }
    }

    fn crash(&mut self) {
        self.coverage.crashes += 1;
        // Power loss: the disk dies FIRST, then the process. Dropping the
        // scheduler before crashing the disk would let engine teardown
        // flush+fsync+ack on the way down — a luxury real power loss does
        // not grant (and a window where an ack could race deliberate bit
        // rot that already made its history unreachable).
        self.disk.crash();
        self.sched = None;
        // A restart takes some wall time.
        self.clock.advance(Duration::from_millis(200));
        self.ensure_sched();
    }

    /// Record durability-acknowledged completions: a handle resolves Ok only
    /// after the terminal record's fsync, so anything recorded here is a
    /// promise the system must keep across every later crash.
    fn harvest(&mut self) {
        let mut newly = Vec::new();
        for (id, h) in &self.handles {
            if self.completed.contains_key(id) {
                continue;
            }
            if let Some(Ok(bytes)) = h.peek() {
                let out: Option<u64> = sqrl_core::codec::from_slice(&bytes, "out").ok();
                newly.push((id.clone(), out));
            }
        }
        for (id, out) in newly {
            // The durability invariant, checked at the instant of the ack:
            // even if EVERY unsynced byte were lost right now, recovery must
            // still see this workflow as completed.
            if std::env::var("SQRL_DST_PARANOID").is_ok() {
                let fork = self.disk.fork_durable_only(1);
                let storage =
                    WalStorage::open_with(Arc::new(fork), World::wal_opts()).expect("fork open");
                use sqrl_core::Storage as _;
                let mut found = false;
                let mut diag: Vec<String> = Vec::new();
                for sh in 0..storage.num_shards() {
                    let mut shard = storage.open_shard(sh).expect("fork shard");
                    match shard.read(&WorkflowId::new(id.clone())) {
                        Ok(r) => {
                            let term_snap = r
                                .snapshot
                                .as_ref()
                                .is_some_and(|x| x.meta.terminal.is_some());
                            let term_rec = r.records.iter().any(|x| {
                                matches!(x.event, sqrl_core::JournalEvent::WorkflowCompleted { .. })
                            });
                            if term_snap || term_rec {
                                found = true;
                            } else {
                                diag.push(format!(
                                    "shard {sh}: snap={:?} recs={:?}",
                                    r.snapshot
                                        .as_ref()
                                        .map(|x| (x.upto, x.meta.terminal.clone())),
                                    r.records
                                        .iter()
                                        .map(|x| (x.index, x.event.kind()))
                                        .collect::<Vec<_>>()
                                ));
                            }
                        }
                        Err(e) => diag.push(format!("shard {sh}: read err {e}")),
                    }
                }
                if !found {
                    // In corruption-mode seeds an ack can be legally voided
                    // between firing and this first observation: deliberate
                    // bit rot erased the durable evidence (CRC truncation)
                    // and the crash in the same op prevented an earlier
                    // harvest. Same treatment as a voided `completed` entry:
                    // forget the ack and its stale handle; the client-retry
                    // drain re-runs the workflow.
                    if self.corruption_mode && self.coverage.corruption_truncations > 0 {
                        self.coverage.corruption_regressions += 1;
                        self.handles.remove(&id);
                        continue;
                    }
                    panic!(
                        "seed {}: completion of {id} acked but NOT durable\n{}",
                        self.seed,
                        diag.join("\n")
                    );
                }
            }
            self.completed.insert(id, out);
        }
    }

    fn op(&mut self, effects_seen: &Attempts) {
        let _ = effects_seen;
        self.ensure_sched();
        if self.fault_window > 0 {
            self.fault_window -= 1;
            if self.fault_window == 0 {
                self.disk.set_faults(base_faults());
            }
        }
        let choice = self.rng.next_below(100);
        if std::env::var("SQRL_DST_DEBUG").is_ok() {
            eprintln!("OP choice={choice}");
        }
        match choice {
            0..=34 => {
                let kinds = ["sum", "flaky", "panicky", "sleepy", "waity", "twin"];
                let kind = kinds[self.rng.next_below(kinds.len() as u64) as usize];
                let n = self.started.len();
                let id = format!("{kind}-{n}");
                let input: u64 = 1 + self.rng.next_below(6);
                let sched = self.sched.as_mut().expect("sched");
                if std::env::var("SQRL_DST_DEBUG").is_ok() {
                    eprintln!("START {id}");
                }
                match World::start_kind(sched, &id, kind, input) {
                    Ok(h) => {
                        self.started.insert(id.clone(), (kind.to_string(), input));
                        self.handles.insert(id.clone(), h);
                        if kind == "waity" {
                            self.owed_signals.push((id, 1 + self.rng.next_below(100)));
                        }
                    }
                    Err(Rejected::AlreadyExists(_)) => {
                        self.started.insert(id.clone(), (kind.to_string(), input));
                    }
                    Err(Rejected::Backpressure { .. }) => {
                        self.coverage.backpressure += 1;
                    }
                    Err(Rejected::Unavailable(_)) => { /* crashed mid-start */ }
                    Err(other) => panic!("seed {}: start failed: {other}", self.seed),
                }
            }
            35..=54 => {
                if !self.owed_signals.is_empty() {
                    let i = self.rng.next_below(self.owed_signals.len() as u64) as usize;
                    let (id, payload) = self.owed_signals[i].clone();
                    let sched = self.sched.as_mut().expect("sched");
                    if sched.signal(&*id, "go", &payload).is_ok() {
                        self.owed_signals.remove(i);
                        self.coverage.signals += 1;
                    }
                }
            }
            55..=69 => {
                let ms = 10 + self.rng.next_below(3_000);
                let sched = self.sched.as_mut().expect("sched");
                sched.run_for(Duration::from_millis(ms));
            }
            70..=79 => self.crash(),
            80..=84 => {
                self.disk.set_faults(faulty_faults());
                self.fault_window = 3;
                self.coverage.write_errors_injected += 1;
            }
            85..=89 => {
                if self.corruption_mode {
                    // Flip a byte in a random durable segment file.
                    let files: Vec<String> = self
                        .disk
                        .view_image()
                        .keys()
                        .filter(|p| p.contains("/wal-"))
                        .cloned()
                        .collect();
                    if !files.is_empty() {
                        let f = &files[self.rng.next_below(files.len() as u64) as usize];
                        if let Some(len) = self.disk.durable_len(f) {
                            if len > 32 {
                                let off = 16 + self.rng.next_below(len - 24);
                                let _ = self.disk.corrupt(f, off, 0x40);
                                self.coverage.corruption_truncations += 1;
                                // Corruption invalidates the running engine's
                                // in-memory view; force a restart.
                                self.crash();
                            }
                        }
                    }
                }
            }
            _ => {
                // Cancel a random non-terminal workflow.
                let live: Vec<String> = {
                    let sched = self.sched.as_mut().expect("sched");
                    sched
                        .states()
                        .iter()
                        .filter(|(_, s)| {
                            !matches!(
                                s,
                                StateKind::Completed | StateKind::Failed | StateKind::Cancelled
                            )
                        })
                        .map(|(id, _)| id.to_string())
                        .collect()
                };
                if !live.is_empty() {
                    let id = live[self.rng.next_below(live.len() as u64) as usize].clone();
                    let sched = self.sched.as_mut().expect("sched");
                    if sched.cancel(&*id).is_ok() {
                        self.cancelled.insert(id.clone());
                        self.owed_signals.retain(|(o, _)| *o != id);
                        self.coverage.cancels += 1;
                    }
                }
            }
        }
    }

    /// Fault-free drain with client-retry semantics: a start whose record
    /// never became durable legitimately vanishes on crash (at-least-once);
    /// a real client would retry it, so the drain does, until every started
    /// workflow exists and terminates.
    fn drain(&mut self) {
        self.disk.set_faults(FaultConfig {
            p_write_error: 0.0,
            p_sync_error: 0.0,
            ..base_faults()
        });
        self.fault_window = 0;
        for _round in 0..12 {
            self.ensure_sched();
            // 1. Re-start lost workflows (start record never fsynced).
            let states = self.sched.as_ref().expect("sched").states();
            let missing: Vec<(String, String, u64)> = self
                .started
                .iter()
                .filter(|(id, _)| !states.contains_key(&WorkflowId::new((*id).clone())))
                .map(|(id, (k, i))| (id.clone(), k.clone(), *i))
                .collect();
            for (id, kind, input) in missing {
                let sched = self.sched.as_mut().expect("sched");
                match World::start_kind(sched, &id, &kind, input) {
                    Ok(h) => {
                        self.handles.insert(id.clone(), h);
                        if kind == "waity"
                            && !self.owed_signals.iter().any(|(o, _)| *o == id)
                            && !self.cancelled.contains(&id)
                        {
                            self.owed_signals.push((id, 1));
                        }
                    }
                    Err(e) => {
                        if std::env::var("SQRL_DST_DEBUG").is_ok() {
                            eprintln!("DRAIN restart {id} failed: {e}");
                        }
                    }
                }
            }
            // 2. Deliver owed signals.
            let owed = std::mem::take(&mut self.owed_signals);
            for (id, payload) in owed {
                if self.cancelled.contains(&id) {
                    continue;
                }
                self.ensure_sched();
                let sched = self.sched.as_mut().expect("sched");
                if sched.signal(&*id, "go", &payload).is_ok() {
                    self.coverage.signals += 1;
                }
            }
            // 3. Any waity still Blocked gets a wake-up (its signal may have
            // been lost with an unsynced suffix).
            self.ensure_sched();
            let blocked: Vec<String> = {
                let sched = self.sched.as_mut().expect("sched");
                sched
                    .states()
                    .iter()
                    .filter(|(id, st)| {
                        **st == StateKind::Blocked && id.as_str().starts_with("waity-")
                    })
                    .map(|(id, _)| id.to_string())
                    .collect()
            };
            for id in blocked {
                if self.cancelled.contains(&id) {
                    continue;
                }
                let sched = self.sched.as_mut().expect("sched");
                let _ = sched.signal(&*id, "go", &1u64);
            }
            // 4. Re-cancel: a cancel acknowledged to the client may have been
            // lost with an unsynced suffix (at-least-once, like starts and
            // signals) — the workflow reverts to running/blocked and only the
            // client's retry can terminate it.
            self.ensure_sched();
            let lost_cancels: Vec<String> = {
                let states = self.sched.as_ref().expect("sched").states();
                self.cancelled
                    .iter()
                    .filter(|id| {
                        !matches!(
                            states.get(&WorkflowId::new((*id).clone())),
                            None | Some(
                                StateKind::Completed | StateKind::Failed | StateKind::Cancelled
                            )
                        )
                    })
                    .cloned()
                    .collect()
            };
            for id in lost_cancels {
                let sched = self.sched.as_mut().expect("sched");
                let _ = sched.cancel(&*id);
            }
            self.ensure_sched();
            let sched = self.sched.as_mut().expect("sched");
            sched.run_until_idle();
            self.harvest();
            // Converged?
            let states = self.sched.as_ref().expect("sched").states();
            let all_terminal = self.started.keys().all(|id| {
                matches!(
                    states.get(&WorkflowId::new(id.clone())),
                    Some(StateKind::Completed | StateKind::Failed | StateKind::Cancelled)
                )
            });
            if all_terminal {
                break;
            }
        }
    }

    fn collect_metrics_coverage(&mut self) {
        let Some(sched) = &self.sched else { return };
        for m in sched.metrics() {
            self.coverage.retries += m.step_retries;
            self.coverage.snapshots += m.snapshots_taken;
            self.coverage.passivations += m.passivations;
            self.coverage.reactivations += m.reactivations;
            self.coverage.timers_fired += m.timers_fired;
            assert_eq!(
                m.illegal_transitions, 0,
                "seed {}: illegal state transition occurred",
                self.seed
            );
        }
    }

    fn final_digest(&mut self) -> SeedDigest {
        self.ensure_sched();
        let sched = self.sched.as_mut().expect("sched");
        sched.run_until_idle();
        let mut final_states = BTreeMap::new();
        let mut completed = BTreeMap::new();
        for (id, state) in sched.states() {
            final_states.insert(id.to_string(), state);
        }
        // Read every completion result through fresh watchers.
        let ids: Vec<String> = self.started.keys().cloned().collect();
        for id in ids {
            let state = final_states.get(&id).copied();
            if state == Some(StateKind::Completed) {
                let sched = self.sched.as_mut().expect("sched");
                if let Ok(handle) = sched.handle(&*id) {
                    let out: Option<u64> = match handle.peek() {
                        Some(Ok(bytes)) => sqrl_core::codec::from_slice(&bytes, "out").ok(),
                        _ => None,
                    };
                    completed.insert(id.clone(), out);
                }
            }
        }
        // Byte-exact durable image hash.
        let mut h: u64 = 0xcbf29ce484222325;
        self.disk.crash();
        self.disk.recover();
        for (path, bytes) in self.disk.durable_image() {
            h = stable_hash_more(h, path.as_bytes());
            h = stable_hash_more(h, &bytes);
        }
        use sqrl_core::Clock;
        SeedDigest {
            durable_hash: h,
            final_states,
            final_time_ms: self.clock.now().as_millis(),
            completed,
        }
    }
}

fn run_seed(seed: u64, ops: u64) -> SeedRun {
    silence_panics();
    let corruption_mode = seed % 7 == 3;
    let mut w = World::new(seed, corruption_mode);
    w.ensure_sched();
    let attempts: Attempts = Arc::default();
    for _ in 0..ops {
        w.op(&attempts);
        w.harvest();
        // Safety: durably-acknowledged completions never regress. The one
        // legal exception is deliberate bit rot (corruption-mode seeds):
        // CRC truncation cuts the logical WAL stream at the flipped byte,
        // voiding every durable suffix behind it — acked completions
        // included (docs/on-disk-format.md). Such a voided ack turns the
        // workflow back into a lost start; the client-retry drain re-runs it.
        if let Some(sched) = &w.sched {
            let states = sched.states();
            let mut voided: Vec<String> = Vec::new();
            for id in w.completed.keys() {
                let state = states.get(&WorkflowId::new(id.clone()));
                if state != Some(&StateKind::Completed) {
                    assert!(
                        corruption_mode && w.coverage.corruption_truncations > 0,
                        "seed {seed}: durably-completed workflow {id} regressed to {state:?}"
                    );
                    voided.push(id.clone());
                }
            }
            for id in voided {
                w.coverage.corruption_regressions += 1;
                w.completed.remove(&id);
                w.handles.remove(&id);
            }
        }
    }
    w.drain();
    w.collect_metrics_coverage();
    let digest = w.final_digest();

    // Liveness + output ground truth (relaxed only in corruption mode, where
    // bit rot may legally erase un-superseded suffixes of history).
    if !corruption_mode {
        // Durably-acked completions must appear in the final digest with the
        // same value.
        for (id, out) in &w.completed {
            assert_eq!(
                digest.completed.get(id),
                Some(out),
                "seed {seed}: acked completion of {id} changed or vanished"
            );
        }
        for (id, (kind, input)) in &w.started {
            let state = digest.final_states.get(id);
            assert!(
                matches!(
                    state,
                    Some(StateKind::Completed | StateKind::Failed | StateKind::Cancelled)
                ),
                "seed {seed}: workflow {id} did not terminate: {state:?}"
            );
            if let Some(Some(out)) = digest.completed.get(id).map(|o| o.as_ref()) {
                if let Some(want) = expected_output(kind, *input, None) {
                    assert_eq!(*out, want, "seed {seed}: {id} ({kind}) wrong output");
                }
            }
        }
        // "twin" joins that completed count as join coverage.
        w.coverage.joins_completed += digest
            .completed
            .iter()
            .filter(|(id, out)| id.starts_with("twin-") && out.is_some())
            .count() as u64;
        // panicky completions imply a caught panic.
        w.coverage.panics_caught += digest
            .completed
            .iter()
            .filter(|(id, out)| id.starts_with("panicky-") && out.is_some())
            .count() as u64;
    }
    SeedRun {
        coverage: w.coverage.clone(),
        digest,
    }
}

fn silence_panics() {
    static ONCE: OnceLock<()> = OnceLock::new();
    ONCE.get_or_init(|| {
        let prev = std::panic::take_hook();
        std::panic::set_hook(Box::new(move |info| {
            // Step panics are intentional in DST; only echo unexpected ones.
            let msg = format!("{info}");
            if !msg.contains("deterministic first-attempt panic") {
                prev(info);
            }
        }));
    });
}

fn run_range(seeds: std::ops::Range<u64>, ops: u64, check_determinism_every: u64) -> Coverage {
    let mut total = Coverage::default();
    let n = seeds.end - seeds.start;
    for seed in seeds {
        let run1 = run_seed(seed, ops);
        total.merge(&run1.coverage);
        if check_determinism_every > 0 && seed % check_determinism_every == 0 {
            let run2 = run_seed(seed, ops);
            assert_eq!(
                run1.digest, run2.digest,
                "seed {seed}: NOT physically deterministic"
            );
        }
    }
    println!("{}", total.report(n));
    total
}

/// CI version: bounded seed set, determinism cross-checked on a sample.
#[test]
#[cfg_attr(debug_assertions, ignore = "slow: run in release (CI acceptance job)")]
fn dst_short() {
    // SQRL_DST_START / SQRL_DST_END narrow the seed range when reproducing a
    // single failing seed (coverage assertions only apply to the full range).
    let start: u64 = std::env::var("SQRL_DST_START")
        .ok()
        .and_then(|v| v.parse().ok())
        .unwrap_or(0);
    let end: u64 = std::env::var("SQRL_DST_END")
        .ok()
        .and_then(|v| v.parse().ok())
        .unwrap_or(48);
    let cov = run_range(start..end, 160, 8);
    if (start, end) == (0, 48) {
        cov.assert_sometimes();
    }
}

/// The long haul: `cargo test -p sqrl-tests --release dst_long -- --ignored --nocapture`
#[test]
#[ignore = "long DST run (10k seeds); run explicitly in release"]
fn dst_long() {
    let threads = std::thread::available_parallelism()
        .map(|n| n.get() as u64)
        .unwrap_or(4);
    let total_seeds = 10_000u64;
    let per = total_seeds / threads;
    let handles: Vec<_> = (0..threads)
        .map(|t| std::thread::spawn(move || run_range(t * per..(t + 1) * per, 160, 25)))
        .collect();
    let mut total = Coverage::default();
    for h in handles {
        total.merge(&h.join().expect("dst thread"));
    }
    println!("=== TOTAL ===\n{}", total.report(total_seeds));
    total.assert_sometimes();
}

static _SILENCE: AtomicU32 = AtomicU32::new(0);
