//! End-to-end tests of `EngineCore` through its public API, using a
//! test-local in-memory storage and a manually driven mini-scheduler.
//! (The full seeded simulator lives in `sqrl-sim`; these tests pin down the
//! engine's core semantics deterministically by hand.)

use sqrl_core::engine::{EngineCmd, EngineCore, StepDispatch};
use sqrl_core::error::Rejected;
use sqrl_core::snapshot::SnapshotRecord;
use sqrl_core::state::StateKind;
use sqrl_core::storage::{AppendEntry, AppendPayload, JournalReadout, StorageShard, StorageStats};
use sqrl_core::sync::{promise, Waiter};
use sqrl_core::{
    Clock, Ctx, DeterministicRng, EngineConfig, Error, FsyncPolicy, JournalRecord, LogicalTime,
    Registry, RetryPolicy, StorageError, TerminalResult, WorkflowId,
};
use std::collections::BTreeMap;
use std::future::Future;
use std::pin::Pin;
use std::sync::atomic::{AtomicU32, Ordering};
use std::sync::{Arc, Mutex};
use std::task::{Context, Poll, Waker};
use std::time::Duration;

// ---------------------------------------------------------------------------
// Test infrastructure
// ---------------------------------------------------------------------------

#[derive(Default)]
struct MemState {
    journals: BTreeMap<WorkflowId, Vec<JournalRecord>>,
    snapshots: BTreeMap<WorkflowId, SnapshotRecord>,
    syncs: u64,
    fail_appends: bool,
}

#[derive(Clone, Default)]
struct MemStore(Arc<Mutex<MemState>>);

impl MemStore {
    fn shard(&self) -> Box<dyn StorageShard> {
        Box::new(MemShard(self.clone()))
    }

    fn records(&self, id: &str) -> Vec<JournalRecord> {
        self.0
            .lock()
            .unwrap()
            .journals
            .get(&WorkflowId::new(id))
            .cloned()
            .unwrap_or_default()
    }

    fn event_kinds(&self, id: &str) -> Vec<String> {
        self.records(id)
            .iter()
            .map(|r| r.event.kind().to_string())
            .collect()
    }

    fn set_fail_appends(&self, v: bool) {
        self.0.lock().unwrap().fail_appends = v;
    }
}

struct MemShard(MemStore);

impl StorageShard for MemShard {
    fn append(&mut self, entries: &[AppendEntry]) -> Result<(), StorageError> {
        let mut s = self.0 .0.lock().unwrap();
        if s.fail_appends {
            return Err(StorageError::Disk("injected append failure".into()));
        }
        for e in entries {
            match &e.payload {
                AppendPayload::Record(r) => {
                    s.journals
                        .entry(e.workflow.clone())
                        .or_default()
                        .push(r.clone());
                }
                AppendPayload::Snapshot(snap) => {
                    s.snapshots.insert(e.workflow.clone(), snap.clone());
                }
            }
        }
        Ok(())
    }

    fn sync(&mut self) -> Result<(), StorageError> {
        self.0 .0.lock().unwrap().syncs += 1;
        Ok(())
    }

    fn read(&mut self, workflow: &WorkflowId) -> Result<JournalReadout, StorageError> {
        let s = self.0 .0.lock().unwrap();
        let snapshot = s.snapshots.get(workflow).cloned();
        let cut = snapshot.as_ref().map(|sn| sn.upto).unwrap_or(0);
        let records = s
            .journals
            .get(workflow)
            .map(|v| v.iter().filter(|r| r.index >= cut).cloned().collect())
            .unwrap_or_default();
        Ok(JournalReadout { snapshot, records })
    }

    fn list(&mut self) -> Result<Vec<WorkflowId>, StorageError> {
        let s = self.0 .0.lock().unwrap();
        let mut ids: Vec<WorkflowId> = s.journals.keys().cloned().collect();
        for id in s.snapshots.keys() {
            if !ids.contains(id) {
                ids.push(id.clone());
            }
        }
        ids.sort();
        Ok(ids)
    }

    fn maintain(&mut self) -> Result<(), StorageError> {
        Ok(())
    }

    fn stats(&self) -> StorageStats {
        StorageStats::default()
    }
}

#[derive(Clone)]
struct TestClock(Arc<Mutex<u64>>);

impl TestClock {
    fn new() -> Self {
        TestClock(Arc::new(Mutex::new(1_000)))
    }
    fn advance(&self, ms: u64) {
        *self.0.lock().unwrap() += ms;
    }
}

impl Clock for TestClock {
    fn now(&self) -> LogicalTime {
        LogicalTime::from_millis(*self.0.lock().unwrap())
    }
}

struct Harness {
    engine: EngineCore,
    clock: TestClock,
    store: MemStore,
    /// Steps captured but deliberately not executed yet.
    held: Vec<StepDispatch>,
    hold_steps: bool,
}

fn poll_to_completion<T>(mut fut: Pin<Box<dyn Future<Output = T> + Send>>) -> T {
    let waker = Waker::noop();
    let mut cx = Context::from_waker(waker);
    for _ in 0..1000 {
        if let Poll::Ready(v) = fut.as_mut().poll(&mut cx) {
            return v;
        }
    }
    panic!("test step future did not complete in 1000 polls");
}

impl Harness {
    fn new(registry: Registry, config: EngineConfig) -> Self {
        let store = MemStore::default();
        Harness::with_store(registry, config, store, TestClock::new())
    }

    fn with_store(
        registry: Registry,
        config: EngineConfig,
        store: MemStore,
        clock: TestClock,
    ) -> Self {
        let engine = EngineCore::open(
            0,
            Arc::new(registry),
            store.shard(),
            Arc::new(clock.clone()),
            Arc::new(DeterministicRng::new(7)),
            config,
        )
        .expect("open engine");
        Harness {
            engine,
            clock,
            store,
            held: Vec::new(),
            hold_steps: false,
        }
    }

    /// Restart: drop the engine, reopen from the same store (crash without
    /// fsync loss — the WAL-level loss cases are covered by sqrl-store +
    /// sqrl-sim tests).
    fn restart(self, registry: Registry, config: EngineConfig) -> Self {
        Harness::with_store(registry, config, self.store.clone(), self.clock.clone())
    }

    /// Tick until quiescent, executing dispatched steps inline.
    fn run(&mut self) {
        for _ in 0..10_000 {
            let out = self.engine.tick();
            let mut progressed = !out.dispatches.is_empty();
            for d in out.dispatches {
                if self.hold_steps {
                    self.held.push(d);
                    continue;
                }
                let outcome = poll_to_completion(d.fut);
                self.engine.submit(EngineCmd::StepFinished {
                    id: d.workflow,
                    seq: d.seq,
                    attempt: d.attempt,
                    outcome,
                });
            }
            if let Some(wake) = out.next_wake {
                let now = self.clock.now();
                if wake <= now {
                    progressed = true;
                } else {
                    break; // caller decides whether to advance time
                }
            }
            if !progressed && out.next_wake.is_none() {
                break;
            }
        }
    }

    /// Run, advancing the virtual clock over timer/fsync deadlines, until
    /// fully idle.
    fn run_to_idle(&mut self) {
        for _ in 0..10_000 {
            self.run();
            let out = self.engine.tick();
            for d in out.dispatches {
                let outcome = poll_to_completion(d.fut);
                self.engine.submit(EngineCmd::StepFinished {
                    id: d.workflow,
                    seq: d.seq,
                    attempt: d.attempt,
                    outcome,
                });
                continue;
            }
            match out.next_wake {
                Some(wake) => {
                    let now = self.clock.now();
                    if wake > now {
                        self.clock.advance(wake.as_millis() - now.as_millis());
                    }
                }
                None => return,
            }
        }
        panic!("engine did not go idle");
    }

    fn start(
        &mut self,
        id: &str,
        name: &str,
        input: impl serde::Serialize,
    ) -> Waiter<TerminalResult> {
        let (admit_c, admit_w) = promise::<Result<(), Rejected>>();
        let (term_c, term_w) = promise::<TerminalResult>();
        self.engine.submit(EngineCmd::Start {
            id: WorkflowId::new(id),
            name: name.to_string(),
            input: sqrl_core::codec::to_vec(&input, "test input").unwrap(),
            admit: admit_c,
            terminal: term_c,
        });
        self.run();
        admit_w
            .peek()
            .expect("admission decided")
            .expect("admitted");
        term_w
    }

    fn try_start(&mut self, id: &str, name: &str) -> Result<(), Rejected> {
        let (admit_c, admit_w) = promise::<Result<(), Rejected>>();
        let (term_c, _term_w) = promise::<TerminalResult>();
        self.engine.submit(EngineCmd::Start {
            id: WorkflowId::new(id),
            name: name.to_string(),
            input: sqrl_core::codec::to_vec(&(), "test input").unwrap(),
            admit: admit_c,
            terminal: term_c,
        });
        self.run();
        admit_w.peek().expect("admission decided")
    }

    fn signal(
        &mut self,
        id: &str,
        name: &str,
        payload: impl serde::Serialize,
    ) -> Result<(), Error> {
        let (ack_c, ack_w) = promise::<Result<(), Error>>();
        self.engine.submit(EngineCmd::Signal {
            id: WorkflowId::new(id),
            name: name.to_string(),
            payload: sqrl_core::codec::to_vec(&payload, "signal").unwrap(),
            ack: ack_c,
        });
        self.run();
        ack_w.peek().expect("ack decided")
    }

    fn cancel(&mut self, id: &str) -> Result<(), Error> {
        let (ack_c, ack_w) = promise::<Result<(), Error>>();
        self.engine.submit(EngineCmd::Cancel {
            id: WorkflowId::new(id),
            ack: ack_c,
        });
        self.run();
        ack_w.peek().expect("ack decided")
    }

    fn watch(&mut self, id: &str) -> Waiter<TerminalResult> {
        let (term_c, term_w) = promise::<TerminalResult>();
        let (ack_c, ack_w) = promise::<Result<(), Error>>();
        self.engine.submit(EngineCmd::Watch {
            id: WorkflowId::new(id),
            terminal: term_c,
            ack: ack_c,
        });
        self.run();
        ack_w.peek().expect("ack decided").expect("workflow known");
        term_w
    }

    fn state_of(&self, id: &str) -> StateKind {
        *self
            .engine
            .states()
            .get(&WorkflowId::new(id))
            .expect("workflow exists")
    }

    fn decode<O: serde::de::DeserializeOwned>(w: &Waiter<TerminalResult>) -> Result<O, Error> {
        let raw = w.peek().expect("terminal resolved")?;
        sqrl_core::codec::from_slice(&raw, "output")
    }
}

fn strict_config() -> EngineConfig {
    EngineConfig {
        fsync: FsyncPolicy::Strict,
        ..EngineConfig::default()
    }
}

// ---------------------------------------------------------------------------
// Workflows under test
// ---------------------------------------------------------------------------

fn two_step_registry(counter: Arc<AtomicU32>) -> Registry {
    let mut reg = Registry::new();
    reg.register("double-sum", 1, move |ctx: Ctx, input: u64| {
        let counter = Arc::clone(&counter);
        async move {
            let c1 = Arc::clone(&counter);
            let a: u64 = ctx
                .step("double", move || {
                    let c1 = Arc::clone(&c1);
                    async move {
                        c1.fetch_add(1, Ordering::SeqCst);
                        Ok::<u64, String>(input * 2)
                    }
                })
                .await?;
            let c2 = Arc::clone(&counter);
            let b: u64 = ctx
                .step("add-ten", move || {
                    let c2 = Arc::clone(&c2);
                    async move {
                        c2.fetch_add(1, Ordering::SeqCst);
                        Ok::<u64, String>(a + 10)
                    }
                })
                .await?;
            Ok(b)
        }
    });
    reg
}

// ---------------------------------------------------------------------------
// Tests
// ---------------------------------------------------------------------------

#[test]
fn two_steps_complete_and_journal() {
    let executions = Arc::new(AtomicU32::new(0));
    let mut h = Harness::new(two_step_registry(Arc::clone(&executions)), strict_config());
    let term = h.start("wf-1", "double-sum", 21u64);
    h.run_to_idle();
    let out: u64 = Harness::decode::<u64>(&term).expect("completed");
    assert_eq!(out, 52); // 21*2 + 10
    assert_eq!(executions.load(Ordering::SeqCst), 2);
    assert_eq!(h.state_of("wf-1"), StateKind::Completed);
    assert_eq!(
        h.store.event_kinds("wf-1"),
        vec![
            "WorkflowStarted",
            "StepScheduled",
            "StepCompleted",
            "StepScheduled",
            "StepCompleted",
            "WorkflowCompleted",
        ]
    );
}

#[test]
fn crash_between_steps_resumes_without_reexecuting_step_one() {
    let executions = Arc::new(AtomicU32::new(0));
    let mut h = Harness::new(two_step_registry(Arc::clone(&executions)), strict_config());
    h.hold_steps = true; // capture dispatches instead of executing them
    let _term = h.start("wf-1", "double-sum", 21u64);
    // Execute exactly the first dispatched step, then "crash".
    assert_eq!(h.held.len(), 1, "exactly step 1 dispatched");
    if let Some(d) = h.held.pop() {
        let outcome = poll_to_completion(d.fut);
        h.engine.submit(EngineCmd::StepFinished {
            id: d.workflow,
            seq: d.seq,
            attempt: d.attempt,
            outcome,
        });
    }
    h.hold_steps = true;
    h.run(); // journal step-1 completion, dispatch step 2 into held
    let kinds_before = h.store.event_kinds("wf-1");
    assert!(
        kinds_before.contains(&"StepCompleted".to_string()),
        "step 1 must be journaled before crash, got {kinds_before:?}"
    );
    let exec_before = executions.load(Ordering::SeqCst);

    // Crash: drop engine (held step 2 vanishes with the process).
    let executions2 = Arc::new(AtomicU32::new(0));
    let reg2 = two_step_registry(Arc::clone(&executions2));
    let mut h = h.restart(reg2, strict_config());
    let term = h.watch("wf-1");
    h.run_to_idle();

    let out: u64 = Harness::decode::<u64>(&term).expect("completed after recovery");
    assert_eq!(out, 52);
    // Step 1 must NOT re-execute after recovery; step 2 runs at least once.
    let exec_after = executions2.load(Ordering::SeqCst);
    assert_eq!(exec_before, 1, "exactly step 1 ran before crash");
    assert_eq!(exec_after, 1, "exactly step 2 ran after recovery");
    assert_eq!(h.state_of("wf-1"), StateKind::Completed);
}

#[test]
fn completed_workflow_survives_restart_as_terminal() {
    let executions = Arc::new(AtomicU32::new(0));
    let mut h = Harness::new(two_step_registry(Arc::clone(&executions)), strict_config());
    let _term = h.start("wf-1", "double-sum", 1u64);
    h.run_to_idle();
    let mut h = h.restart(
        two_step_registry(Arc::new(AtomicU32::new(0))),
        strict_config(),
    );
    let term = h.watch("wf-1");
    let out: u64 = Harness::decode(&term).expect("still completed");
    assert_eq!(out, 12);
    assert_eq!(executions.load(Ordering::SeqCst), 2, "no re-execution");
}

#[test]
fn retry_with_backoff_then_success() {
    let attempts = Arc::new(AtomicU32::new(0));
    let mut reg = Registry::new();
    let a = Arc::clone(&attempts);
    reg.register("flaky", 1, move |ctx: Ctx, (): ()| {
        let a = Arc::clone(&a);
        async move {
            let a2 = Arc::clone(&a);
            let v: u32 = ctx
                .step("might-fail", move || {
                    let n = a2.fetch_add(1, Ordering::SeqCst) + 1;
                    async move {
                        if n < 3 {
                            Err(format!("attempt {n} fails"))
                        } else {
                            Ok(n)
                        }
                    }
                })
                .await?;
            Ok(v)
        }
    });
    let cfg = EngineConfig {
        retry: RetryPolicy {
            max_attempts: 5,
            initial_delay: Duration::from_millis(100),
            multiplier: 2.0,
            max_delay: Duration::from_secs(10),
            jitter_fraction: 0.0,
        },
        ..strict_config()
    };
    let mut h = Harness::new(reg, cfg);
    let term = h.start("wf-r", "flaky", ());
    h.run_to_idle();
    let out: u32 = Harness::decode(&term).expect("eventually succeeds");
    assert_eq!(out, 3);
    assert_eq!(attempts.load(Ordering::SeqCst), 3);
    let kinds = h.store.event_kinds("wf-r");
    assert_eq!(
        kinds.iter().filter(|k| k.as_str() == "StepFailed").count(),
        2,
        "two failed attempts journaled: {kinds:?}"
    );
    assert_eq!(h.engine.metrics().step_retries, 2);
}

#[test]
fn retries_exhaust_into_failed_state() {
    let mut reg = Registry::new();
    reg.register("doomed", 1, move |ctx: Ctx, (): ()| async move {
        let v: u32 = ctx
            .step("always-fails", move || async move {
                Err::<u32, _>("nope".to_string())
            })
            .await?;
        Ok(v)
    });
    let cfg = EngineConfig {
        retry: RetryPolicy {
            max_attempts: 3,
            jitter_fraction: 0.0,
            ..RetryPolicy::default()
        },
        ..strict_config()
    };
    let mut h = Harness::new(reg, cfg);
    let term = h.start("wf-d", "doomed", ());
    h.run_to_idle();
    let err = Harness::decode::<u32>(&term).expect_err("must fail");
    match err {
        Error::StepFailed { name, attempts, .. } => {
            assert_eq!(name, "always-fails");
            assert_eq!(attempts, 3);
        }
        other => panic!("expected StepFailed, got {other:?}"),
    }
    assert_eq!(h.state_of("wf-d"), StateKind::Failed);
    // Full journal retained (no terminal snapshot for Failed).
    assert!(h
        .store
        .event_kinds("wf-d")
        .contains(&"WorkflowFailed".to_string()));
}

#[test]
fn durable_timer_fires_after_virtual_time_advance() {
    let mut reg = Registry::new();
    reg.register("sleeper", 1, move |ctx: Ctx, (): ()| async move {
        let before = ctx.now();
        ctx.sleep(Duration::from_secs(60)).await?;
        let after = ctx.now();
        Ok(after.saturating_since(before).as_millis() as u64)
    });
    let mut h = Harness::new(reg, strict_config());
    let term = h.start("wf-s", "sleeper", ());
    h.run();
    assert_eq!(h.state_of("wf-s"), StateKind::Sleeping);
    assert!(term.peek().is_none(), "must still be sleeping");
    h.run_to_idle(); // advances virtual time to the timer
    let slept: u64 = Harness::decode(&term).expect("completed");
    assert!(slept >= 60_000, "slept {slept}ms");
}

#[test]
fn durable_timer_survives_restart() {
    let mk_reg = || {
        let mut reg = Registry::new();
        reg.register("sleeper", 1, move |ctx: Ctx, (): ()| async move {
            ctx.sleep(Duration::from_secs(60)).await?;
            Ok(ctx.now().as_millis())
        });
        reg
    };
    let mut h = Harness::new(mk_reg(), strict_config());
    let _term = h.start("wf-s", "sleeper", ());
    h.run();
    assert_eq!(h.state_of("wf-s"), StateKind::Sleeping);
    // Crash while sleeping; restart; timer must re-arm and fire.
    let mut h = h.restart(mk_reg(), strict_config());
    let term = h.watch("wf-s");
    h.run_to_idle();
    let fired_at: u64 = Harness::decode(&term).expect("completed after restart");
    assert!(fired_at >= 61_000, "timer fired at logical {fired_at}");
    let kinds = h.store.event_kinds("wf-s");
    assert_eq!(
        kinds
            .iter()
            .filter(|k| k.as_str() == "TimerScheduled")
            .count(),
        1,
        "timer scheduled exactly once across restart: {kinds:?}"
    );
}

#[test]
fn signal_wakes_blocked_workflow_including_after_restart() {
    let mk_reg = || {
        let mut reg = Registry::new();
        reg.register("waiter", 1, move |ctx: Ctx, (): ()| async move {
            let v: u64 = ctx.await_signal("go").await?;
            Ok(v * 10)
        });
        reg
    };
    let mut h = Harness::new(mk_reg(), strict_config());
    let _term = h.start("wf-w", "waiter", ());
    h.run();
    assert_eq!(h.state_of("wf-w"), StateKind::Blocked);
    // Crash while blocked; restart; then signal.
    let mut h = h.restart(mk_reg(), strict_config());
    let term = h.watch("wf-w");
    h.run();
    assert_eq!(h.state_of("wf-w"), StateKind::Blocked);
    h.signal("wf-w", "go", 7u64).expect("signal accepted");
    h.run_to_idle();
    let out: u64 = Harness::decode(&term).expect("completed");
    assert_eq!(out, 70);
}

#[test]
fn early_signal_is_buffered() {
    let mut reg = Registry::new();
    reg.register("later", 1, move |ctx: Ctx, (): ()| async move {
        ctx.sleep(Duration::from_secs(5)).await?;
        let v: u64 = ctx.await_signal("data").await?;
        Ok(v)
    });
    let mut h = Harness::new(reg, strict_config());
    let term = h.start("wf-b", "later", ());
    h.run();
    // Signal arrives while the workflow is still sleeping.
    h.signal("wf-b", "data", 42u64).expect("accepted");
    h.run_to_idle();
    let out: u64 = Harness::decode(&term).expect("completed");
    assert_eq!(out, 42);
}

#[test]
fn nondeterministic_code_change_is_detected_and_not_retried() {
    // v1: step "a" then blocks on a signal (so history ends non-terminal).
    let mut reg1 = Registry::new();
    reg1.register("wf", 1, move |ctx: Ctx, (): ()| async move {
        let _: u32 = ctx
            .step("a", move || async move { Ok::<u32, String>(1) })
            .await?;
        let _: u32 = ctx.await_signal("never").await?;
        Ok(0u32)
    });
    let mut h = Harness::new(reg1, strict_config());
    let _term = h.start("wf-nd", "wf", ());
    h.run();
    assert_eq!(h.state_of("wf-nd"), StateKind::Blocked);

    // "Deploy" incompatible code: step renamed without a patch gate.
    let mut reg2 = Registry::new();
    reg2.register("wf", 2, move |ctx: Ctx, (): ()| async move {
        let _: u32 = ctx
            .step("renamed", move || async move { Ok::<u32, String>(1) })
            .await?;
        let _: u32 = ctx.await_signal("never").await?;
        Ok(0u32)
    });
    let mut h = h.restart(reg2, strict_config());
    let term = h.watch("wf-nd");
    h.run_to_idle();
    let err = Harness::decode::<u32>(&term).expect_err("must fail");
    match err {
        Error::NonDeterminism(nd) => {
            assert_eq!(nd.seq, 0);
            assert!(
                format!("{nd}").contains("patched"),
                "error teaches the fix: {nd}"
            );
        }
        other => panic!("expected NonDeterminism, got {other:?}"),
    }
    assert_eq!(h.state_of("wf-nd"), StateKind::Failed);
    assert_eq!(
        h.engine.metrics().nd_failures,
        1,
        "failed exactly once, no loop"
    );
    // Nothing journaled about the failure: fixing the code + restarting heals.
    assert!(!h
        .store
        .event_kinds("wf-nd")
        .contains(&"WorkflowFailed".to_string()));
    let mut reg1b = Registry::new();
    reg1b.register("wf", 1, move |ctx: Ctx, (): ()| async move {
        let _: u32 = ctx
            .step("a", move || async move { Ok::<u32, String>(1) })
            .await?;
        let v: u32 = ctx.await_signal("never").await?;
        Ok(v)
    });
    let mut h = h.restart(reg1b, strict_config());
    h.run();
    assert_eq!(
        h.state_of("wf-nd"),
        StateKind::Blocked,
        "healed after rollback"
    );
}

#[test]
fn patched_gate_allows_code_evolution() {
    // Old code: step a, then block. New code: patched gate adds step b first
    // for NEW executions only.
    let old_reg = || {
        let mut reg = Registry::new();
        reg.register("wf", 1, move |ctx: Ctx, (): ()| async move {
            let _: u32 = ctx
                .step("a", move || async move { Ok::<u32, String>(1) })
                .await?;
            let v: u32 = ctx.await_signal("go").await?;
            Ok(v)
        });
        reg
    };
    let new_reg = || {
        let mut reg = Registry::new();
        reg.register("wf", 2, move |ctx: Ctx, (): ()| async move {
            if ctx.patched("add-step-b") {
                let _: u32 = ctx
                    .step("b", move || async move { Ok::<u32, String>(9) })
                    .await?;
            }
            let _: u32 = ctx
                .step("a", move || async move { Ok::<u32, String>(1) })
                .await?;
            let v: u32 = ctx.await_signal("go").await?;
            Ok(v)
        });
        reg
    };
    let mut h = Harness::new(old_reg(), strict_config());
    let _term = h.start("old-wf", "wf", ());
    h.run();
    // Deploy new code; old workflow must replay fine (gate returns false)...
    let mut h = h.restart(new_reg(), strict_config());
    let old_term = h.watch("old-wf");
    h.run();
    assert_eq!(h.state_of("old-wf"), StateKind::Blocked);
    // ...and a new workflow takes the new path.
    let new_term = h.start("new-wf", "wf", ());
    h.run();
    h.signal("old-wf", "go", 5u64).unwrap();
    h.signal("new-wf", "go", 6u64).unwrap();
    h.run_to_idle();
    assert_eq!(Harness::decode::<u32>(&old_term).unwrap(), 5);
    assert_eq!(Harness::decode::<u32>(&new_term).unwrap(), 6);
    let new_kinds = h.store.event_kinds("new-wf");
    assert!(new_kinds.contains(&"PatchRecorded".to_string()));
    // New workflow survives a restart under new code (patched history replays).
    let mut h = h.restart(new_reg(), strict_config());
    let term = h.watch("new-wf");
    assert_eq!(Harness::decode::<u32>(&term).unwrap(), 6);
}

#[test]
fn cancel_stops_workflow_and_journals() {
    let mut reg = Registry::new();
    reg.register("waiter", 1, move |ctx: Ctx, (): ()| async move {
        let v: u64 = ctx.await_signal("never").await?;
        Ok(v)
    });
    let mut h = Harness::new(reg, strict_config());
    let term = h.start("wf-c", "waiter", ());
    h.run();
    h.cancel("wf-c").expect("cancel accepted");
    h.run_to_idle();
    match Harness::decode::<u64>(&term) {
        Err(Error::Cancelled) => {}
        other => panic!("expected Cancelled, got {other:?}"),
    }
    assert_eq!(h.state_of("wf-c"), StateKind::Cancelled);
    assert!(h
        .store
        .event_kinds("wf-c")
        .contains(&"WorkflowCancelled".to_string()));
    assert!(h.cancel("wf-c").is_err(), "double cancel rejected");
}

#[test]
fn step_panic_is_caught_and_retried_per_policy() {
    let attempts = Arc::new(AtomicU32::new(0));
    let a = Arc::clone(&attempts);
    let mut reg = Registry::new();
    reg.register("panicky", 1, move |ctx: Ctx, (): ()| {
        let a = Arc::clone(&a);
        async move {
            let a2 = Arc::clone(&a);
            let v: u32 = ctx
                .step("boom", move || {
                    let n = a2.fetch_add(1, Ordering::SeqCst) + 1;
                    async move {
                        if n < 2 {
                            panic!("kaboom attempt {n}");
                        }
                        Ok::<u32, String>(n)
                    }
                })
                .await?;
            Ok(v)
        }
    });
    let cfg = EngineConfig {
        retry: RetryPolicy {
            max_attempts: 3,
            jitter_fraction: 0.0,
            ..RetryPolicy::default()
        },
        ..strict_config()
    };
    let mut h = Harness::new(reg, cfg);
    let prev = std::panic::take_hook();
    std::panic::set_hook(Box::new(|_| {})); // silence expected panic output
    let term = h.start("wf-p", "panicky", ());
    h.run_to_idle();
    std::panic::set_hook(prev);
    let out: u32 = Harness::decode(&term).expect("recovered from panic");
    assert_eq!(out, 2);
    let kinds = h.store.event_kinds("wf-p");
    assert!(kinds.contains(&"StepFailed".to_string()), "{kinds:?}");
}

#[test]
fn backpressure_rejects_when_shard_full() {
    let mut reg = Registry::new();
    reg.register("waiter", 1, move |ctx: Ctx, (): ()| async move {
        let v: u64 = ctx.await_signal("never").await?;
        Ok(v)
    });
    let cfg = EngineConfig {
        max_active_per_shard: 2,
        ..strict_config()
    };
    let mut h = Harness::new(reg, cfg);
    h.try_start("wf-1", "waiter").expect("admitted");
    h.try_start("wf-2", "waiter").expect("admitted");
    match h.try_start("wf-3", "waiter") {
        Err(Rejected::Backpressure { limit: 2, .. }) => {}
        other => panic!("expected backpressure, got {other:?}"),
    }
    assert_eq!(h.engine.metrics().backpressure_rejections, 1);
    assert!(matches!(
        h.try_start("wf-1", "waiter"),
        Err(Rejected::AlreadyExists(_))
    ));
    assert!(matches!(
        h.try_start("wf-4", "nope"),
        Err(Rejected::UnknownWorkflowName(_))
    ));
}

#[test]
fn storage_failure_halts_commits_and_rejects_starts() {
    let mut reg = Registry::new();
    reg.register("wf", 1, move |ctx: Ctx, (): ()| async move {
        let v: u32 = ctx
            .step("s", move || async move { Ok::<u32, String>(1) })
            .await?;
        Ok(v)
    });
    let mut h = Harness::new(reg, strict_config());
    h.store.set_fail_appends(true);
    let (admit_c, admit_w) = promise::<Result<(), Rejected>>();
    let (term_c, term_w) = promise::<TerminalResult>();
    h.engine.submit(EngineCmd::Start {
        id: WorkflowId::new("wf-x"),
        name: "wf".to_string(),
        input: sqrl_core::codec::to_vec(&(), "in").unwrap(),
        admit: admit_c,
        terminal: term_c,
    });
    h.run();
    // Admission may succeed (append is buffered), but the flush must fail and
    // poison the engine: the terminal watcher errors with Storage, and new
    // starts are rejected.
    let _ = admit_w.peek();
    assert!(
        h.engine.storage_error().is_some(),
        "storage must be poisoned"
    );
    if let Some(res) = term_w.peek() {
        assert!(matches!(res, Err(Error::Storage(_))));
    }
    match h.try_start("wf-y", "wf") {
        Err(Rejected::Unavailable(_)) => {}
        other => panic!("expected Unavailable, got {other:?}"),
    }
}

#[test]
fn idempotency_key_stable_across_replay() {
    let keys: Arc<Mutex<Vec<String>>> = Arc::new(Mutex::new(Vec::new()));
    let mk_reg = |keys: Arc<Mutex<Vec<String>>>| {
        let mut reg = Registry::new();
        reg.register("keyed", 1, move |ctx: Ctx, (): ()| {
            let keys = Arc::clone(&keys);
            async move {
                let key = ctx.idempotency_key();
                keys.lock().unwrap().push(key.clone());
                let _: u32 = ctx
                    .step("a", move || async move { Ok::<u32, String>(1) })
                    .await?;
                let _: u32 = ctx.await_signal("go").await?;
                Ok(0u32)
            }
        });
        reg
    };
    let mut h = Harness::new(mk_reg(Arc::clone(&keys)), strict_config());
    let _term = h.start("wf-k", "keyed", ());
    h.run();
    let mut h = h.restart(mk_reg(Arc::clone(&keys)), strict_config());
    h.run();
    let observed = keys.lock().unwrap().clone();
    assert_eq!(observed.len(), 2, "orchestration ran twice (live + replay)");
    assert_eq!(observed[0], observed[1], "key stable across replay");
    let _ = h; // keep alive to end
}
