//! Phase-1 acceptance tests on the deterministic simulator: the full stack
//! (engine → WalStorage → SimDisk) under crash injection.
//!
//! The flagship test sweeps a crash point across *every* disk operation of a
//! checkout saga — before and after every journal append and fsync — and
//! proves the workflow always completes after restart with each step
//! executed at least once and the idempotency-keyed effect deduplicating to
//! exactly one.

use sqrl::{Ctx, EngineConfig, FsyncPolicy, Registry, Rejected, RetryPolicy};
use sqrl_core::{LogicalTime, StateKind, WorkflowId};
use sqrl_sim::{SimClock, SimDisk, SimScheduler};
use sqrl_store::{WalOptions, WalStorage};
use std::collections::BTreeSet;
use std::sync::{Arc, Mutex};
use std::time::Duration;

#[derive(Default, Debug)]
struct Effects {
    reserves: u32,
    charges: Vec<String>, // idempotency keys observed by the charge effect
    ships: u32,
}

type SharedEffects = Arc<Mutex<Effects>>;

fn saga_registry(effects: SharedEffects) -> Arc<Registry> {
    let mut reg = Registry::new();
    reg.register("checkout", 1, move |ctx: Ctx, amount: u64| {
        let effects = Arc::clone(&effects);
        async move {
            let e1 = Arc::clone(&effects);
            let hold: u64 = ctx
                .step("reserve", move || {
                    let e1 = Arc::clone(&e1);
                    async move {
                        e1.lock().unwrap().reserves += 1;
                        Ok::<u64, String>(1)
                    }
                })
                .await?;
            ctx.sleep(Duration::from_secs(30)).await?;
            let key = ctx.idempotency_key();
            let e2 = Arc::clone(&effects);
            let charge: u64 = ctx
                .step("charge", move || {
                    let e2 = Arc::clone(&e2);
                    let key = key.clone();
                    async move {
                        // The external effect: recorded under its
                        // idempotency key (at-least-once execution, but the
                        // key dedupes to effectively-once).
                        e2.lock().unwrap().charges.push(key.clone());
                        Ok::<u64, String>(amount)
                    }
                })
                .await?;
            let e3 = Arc::clone(&effects);
            ctx.step("ship", move || {
                let e3 = Arc::clone(&e3);
                async move {
                    e3.lock().unwrap().ships += 1;
                    Ok::<u64, String>(1)
                }
            })
            .await?;
            Ok(hold + charge)
        }
    });
    Arc::new(reg)
}

fn wal_opts() -> WalOptions {
    WalOptions {
        num_shards: 1,
        segment_size: 8192, // small: crashes also hit segment rolls
    }
}

fn strict_cfg() -> EngineConfig {
    EngineConfig {
        fsync: FsyncPolicy::Strict,
        retry: RetryPolicy::no_retries(),
        ..EngineConfig::default()
    }
}

/// Run the saga to completion on `disk`, restarting after every crash.
/// Returns the workflow output. Panics if it cannot complete within a
/// bounded number of restarts (liveness).
fn drive_to_completion(
    disk: &SimDisk,
    clock: &SimClock,
    seed: u64,
    registry: Arc<Registry>,
    cfg: &EngineConfig,
) -> Result<u64, sqrl::Error> {
    for _restart in 0..200 {
        if disk.is_crashed() {
            disk.recover();
        }
        let storage = match WalStorage::open_with(Arc::new(disk.clone()), wal_opts()) {
            Ok(s) => s,
            Err(_) => continue, // crashed during open: recover and retry
        };
        let mut sched = match SimScheduler::with_clock(
            seed,
            &storage,
            Arc::clone(&registry),
            cfg.clone(),
            clock.clone(),
        ) {
            Ok(s) => s,
            Err(_) => continue,
        };
        let handle = match sched.start("saga-1", "checkout", &500u64) {
            Ok(h) => h,
            Err(Rejected::AlreadyExists(_)) => match sched.handle("saga-1") {
                Ok(h) => h,
                Err(_) => continue,
            },
            Err(Rejected::Unavailable(_)) => continue,
            Err(other) => panic!("unexpected admission error: {other}"),
        };
        sched.run_until_idle();
        if std::env::var("SQRL_SWEEP_DEBUG").is_ok() {
            eprintln!(
                "  drive: restart={_restart} ops={} crashed={} states={:?} now={}",
                disk.op_count(),
                disk.is_crashed(),
                sched.states(),
                sched.now()
            );
        }
        if disk.is_crashed() {
            continue;
        }
        if let Some(result) = handle.peek() {
            return result.map(|bytes| {
                sqrl_core::codec::from_slice::<u64>(&bytes, "output").expect("decode")
            });
        }
        // Idle, not crashed, not terminal: nothing further can happen.
        panic!("saga stuck non-terminal without a crash");
    }
    panic!("saga did not complete within 200 restarts (liveness violation)");
}

/// How many disk ops one clean run needs (bounds the crash sweep).
fn clean_run_ops() -> u64 {
    eprintln!("sweep: clean run starting");
    let effects: SharedEffects = Arc::default();
    let disk = SimDisk::new(999);
    let clock = SimClock::new(LogicalTime::from_millis(1_000));
    let out = drive_to_completion(&disk, &clock, 7, saga_registry(effects), &strict_cfg())
        .expect("clean run completes");
    assert_eq!(out, 501);
    eprintln!("sweep: clean run done, ops={}", disk.op_count());
    disk.op_count()
}

#[test]
#[cfg_attr(debug_assertions, ignore = "slow: run in release (CI acceptance job)")]
fn crash_at_every_boundary_saga_completes_effectively_once() {
    let max_ops = clean_run_ops();
    assert!(max_ops > 20, "sweep must have real coverage, got {max_ops}");
    // Optional range override for bisection: SQRL_SWEEP_START/SQRL_SWEEP_END.
    let start: u64 = std::env::var("SQRL_SWEEP_START")
        .ok()
        .and_then(|v| v.parse().ok())
        .unwrap_or(1);
    let end: u64 = std::env::var("SQRL_SWEEP_END")
        .ok()
        .and_then(|v| v.parse().ok())
        .unwrap_or(max_ops);
    let mut crash_points_hit = 0u64;
    for crash_at in start..=end.min(max_ops) {
        eprintln!("sweep: crash_at={crash_at}/{max_ops}");
        let effects: SharedEffects = Arc::default();
        let disk = SimDisk::new(31); // fixed disk seed: loss pattern varies per op point
        let clock = SimClock::new(LogicalTime::from_millis(1_000));
        disk.crash_after_ops(crash_at);
        let out = drive_to_completion(
            &disk,
            &clock,
            7,
            saga_registry(Arc::clone(&effects)),
            &strict_cfg(),
        )
        .unwrap_or_else(|e| panic!("crash_at={crash_at}: saga failed: {e}"));
        assert_eq!(out, 501, "crash_at={crash_at}");
        let e = effects.lock().unwrap();
        assert!(e.reserves >= 1, "crash_at={crash_at}: reserve ran");
        assert!(e.ships >= 1, "crash_at={crash_at}: ship ran");
        assert!(!e.charges.is_empty(), "crash_at={crash_at}: charge ran");
        // At-least-once execution, effectively-once effect: every re-execution
        // presented the SAME idempotency key.
        let unique: BTreeSet<&String> = e.charges.iter().collect();
        assert_eq!(
            unique.len(),
            1,
            "crash_at={crash_at}: idempotency key must dedupe {:?}",
            e.charges
        );
        crash_points_hit += 1;
    }
    println!(
        "crash-at-every-boundary: {crash_points_hit} crash points swept over {max_ops} disk ops"
    );
}

#[test]
fn durable_sleep_survives_crash_mid_sleep() {
    let effects: SharedEffects = Arc::default();
    let registry = saga_registry(Arc::clone(&effects));
    let disk = SimDisk::new(5);
    let clock = SimClock::new(LogicalTime::from_millis(1_000));
    let cfg = strict_cfg();

    // Phase 1: start, run only until the workflow is sleeping (reserve done,
    // 30s timer armed).
    {
        let storage = WalStorage::open_with(Arc::new(disk.clone()), wal_opts()).unwrap();
        let mut sched = SimScheduler::with_clock(
            7,
            &storage,
            Arc::clone(&registry),
            cfg.clone(),
            clock.clone(),
        )
        .unwrap();
        let _h = sched.start("saga-1", "checkout", &500u64).unwrap();
        // run_until_idle advances time; instead run only the immediate work:
        // the saga reaches Sleeping the moment nothing else is runnable at
        // the current instant. We freeze before the timer by crashing here.
        sched.run_for(Duration::from_secs(5));
        let asleep = sched
            .states()
            .get(&WorkflowId::new("saga-1"))
            .copied()
            .unwrap();
        // Depending on run_for's jump the workflow may already have finished
        // its sleep; require we caught it asleep for this scenario.
        assert_eq!(asleep, StateKind::Sleeping, "must crash mid-sleep");
    }
    disk.crash();
    disk.recover();

    // Phase 2: restart. Timer must re-arm from the journal and fire at its
    // original logical time (start + ~30s), not restart + 30s.
    let storage = WalStorage::open_with(Arc::new(disk.clone()), wal_opts()).unwrap();
    let mut sched = SimScheduler::with_clock(7, &storage, registry, cfg, clock.clone()).unwrap();
    let handle = sched.handle("saga-1").unwrap();
    sched.run_until_idle();
    let out: u64 = handle.result_blocking().unwrap();
    assert_eq!(out, 501);
    use sqrl_core::Clock;
    let done_at = clock.now();
    assert!(
        done_at >= LogicalTime::from_millis(31_000) && done_at < LogicalTime::from_millis(40_000),
        "timer fired at original schedule, done at {done_at}"
    );
    assert_eq!(effects.lock().unwrap().reserves, 1, "reserve not re-run");
}

#[test]
fn signal_wakes_blocked_workflow_after_crash_restart() {
    let mut reg = Registry::new();
    reg.register("waiter", 1, |ctx: Ctx, (): ()| async move {
        let v: u64 = ctx.await_signal("go").await?;
        Ok(v * 2)
    });
    let registry = Arc::new(reg);
    let disk = SimDisk::new(6);
    let clock = SimClock::new(LogicalTime::from_millis(1_000));
    {
        let storage = WalStorage::open_with(Arc::new(disk.clone()), wal_opts()).unwrap();
        let mut sched = SimScheduler::with_clock(
            7,
            &storage,
            Arc::clone(&registry),
            strict_cfg(),
            clock.clone(),
        )
        .unwrap();
        sched.start("w-1", "waiter", &()).unwrap();
        sched.run_until_idle();
        assert_eq!(
            sched.states().get(&WorkflowId::new("w-1")),
            Some(&StateKind::Blocked)
        );
    }
    disk.crash();
    disk.recover();
    let storage = WalStorage::open_with(Arc::new(disk.clone()), wal_opts()).unwrap();
    let mut sched = SimScheduler::with_clock(7, &storage, registry, strict_cfg(), clock).unwrap();
    let handle = sched.handle("w-1").unwrap();
    sched.signal("w-1", "go", &21u64).unwrap();
    sched.run_until_idle();
    let out: u64 = handle.result_blocking().unwrap();
    assert_eq!(out, 42);
}

#[test]
fn wal_corruption_truncates_and_workflow_still_completes() {
    let effects: SharedEffects = Arc::default();
    let registry = saga_registry(Arc::clone(&effects));
    let disk = SimDisk::new(8);
    let clock = SimClock::new(LogicalTime::from_millis(1_000));
    // Run the full saga to completion.
    let out = drive_to_completion(&disk, &clock, 7, Arc::clone(&registry), &strict_cfg()).unwrap();
    assert_eq!(out, 501);
    // Corrupt the tail of the newest segment: the completion records get
    // truncated away; on restart the workflow resumes from the last valid
    // prefix and re-completes.
    let mut segs: Vec<String> = disk
        .view_image()
        .keys()
        .filter(|p| p.starts_with("shard-0/wal-"))
        .cloned()
        .collect();
    segs.sort();
    let tail = segs.last().expect("segments exist").clone();
    let len = disk.durable_len(&tail).unwrap();
    disk.corrupt(&tail, len - 3, 0xFF).unwrap();

    let before = effects.lock().unwrap().charges.len();
    let out2 = drive_to_completion(&disk, &clock, 7, registry, &strict_cfg()).unwrap();
    assert_eq!(out2, 501);
    let e = effects.lock().unwrap();
    // Steps whose records were truncated may re-execute (at-least-once), but
    // the idempotency key still dedupes.
    let unique: BTreeSet<&String> = e.charges.iter().collect();
    assert_eq!(
        unique.len(),
        1,
        "one logical charge, {before} then {:?}",
        e.charges
    );
}

#[test]
fn nondeterminism_detected_on_sim_stack_without_retry_loop() {
    let disk = SimDisk::new(10);
    let clock = SimClock::new(LogicalTime::from_millis(1_000));
    let v1 = {
        let mut reg = Registry::new();
        reg.register("wf", 1, |ctx: Ctx, (): ()| async move {
            let _: u64 = ctx
                .step("original", move || async move { Ok::<u64, String>(1) })
                .await?;
            let v: u64 = ctx.await_signal("never").await?;
            Ok(v)
        });
        Arc::new(reg)
    };
    {
        let storage = WalStorage::open_with(Arc::new(disk.clone()), wal_opts()).unwrap();
        let mut sched =
            SimScheduler::with_clock(7, &storage, v1, strict_cfg(), clock.clone()).unwrap();
        sched.start("wf-1", "wf", &()).unwrap();
        sched.run_until_idle();
    }
    disk.crash();
    disk.recover();
    let v2 = {
        let mut reg = Registry::new();
        reg.register("wf", 2, |ctx: Ctx, (): ()| async move {
            let _: u64 = ctx
                .step("renamed", move || async move { Ok::<u64, String>(1) })
                .await?;
            let v: u64 = ctx.await_signal("never").await?;
            Ok(v)
        });
        Arc::new(reg)
    };
    let storage = WalStorage::open_with(Arc::new(disk.clone()), wal_opts()).unwrap();
    let mut sched = SimScheduler::with_clock(7, &storage, v2, strict_cfg(), clock).unwrap();
    let handle = sched.handle("wf-1").unwrap();
    sched.run_until_idle();
    match handle.peek() {
        Some(Err(sqrl::Error::NonDeterminism(nd))) => assert_eq!(nd.seq, 0),
        other => panic!("expected NonDeterminism, got {other:?}"),
    }
    assert_eq!(
        sched.states().get(&WorkflowId::new("wf-1")),
        Some(&StateKind::Failed)
    );
    let m = &sched.metrics()[0];
    assert_eq!(m.nd_failures, 1, "failed exactly once — no retry loop");
}
