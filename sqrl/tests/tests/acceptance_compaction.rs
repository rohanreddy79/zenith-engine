//! Snapshot-compaction acceptance test: a workflow with ~100,000 journaled
//! events must replay from its snapshot in **< 10% of the time** of a full
//! journal replay. Both timings are measured on the same machine, same
//! store layout (real filesystem), same workload — the only difference is
//! whether snapshots were taken.

#![allow(clippy::disallowed_methods)] // Instant::now is the measurement here

use sqrl::{Ctx, EngineConfig, FsyncPolicy, Registry};
use sqrl_core::LogicalTime;
use sqrl_core::{StateKind, WorkflowId};
use sqrl_sim::{SimClock, SimScheduler};
use sqrl_store::{StdVfs, WalOptions, WalStorage};
use std::sync::Arc;
use std::time::Instant;

const STEPS: u64 = 50_000; // 2 records per step + start/awaits ≈ 100k records

fn registry() -> Arc<Registry> {
    let mut reg = Registry::new();
    reg.register("counter", 1, |ctx: Ctx, (): ()| async move {
        let mut acc = 0u64;
        for i in 0..STEPS {
            let v: u64 = ctx
                .step("inc", move || async move { Ok::<u64, String>(i) })
                .await?;
            acc = acc.wrapping_add(v);
        }
        // Block so the workflow stays non-terminal: recovery must replay it.
        let _: u64 = ctx.await_signal("finish").await?;
        Ok(acc)
    });
    Arc::new(reg)
}

fn wal(dir: &std::path::Path) -> WalStorage {
    WalStorage::open_with(
        Arc::new(StdVfs::new(dir.to_path_buf()).unwrap()),
        WalOptions {
            num_shards: 1,
            segment_size: 2 * 1024 * 1024,
        },
    )
    .unwrap()
}

fn build_history(dir: &std::path::Path, snapshot_every: u64) -> u64 {
    let cfg = EngineConfig {
        fsync: FsyncPolicy::Relaxed {
            interval: std::time::Duration::from_secs(1),
        },
        snapshot_every,
        ..EngineConfig::default()
    };
    let storage = wal(dir);
    let clock = SimClock::new(LogicalTime::from_millis(1_000));
    let mut sched = SimScheduler::with_clock(7, &storage, registry(), cfg, clock).unwrap();
    sched.start("big", "counter", &()).unwrap();
    sched.run_until_idle();
    assert_eq!(
        sched.states().get(&WorkflowId::new("big")),
        Some(&StateKind::Blocked),
        "workflow must be blocked on the finish signal"
    );
    // Clean shutdown: with snapshots enabled this writes a quiescence
    // snapshot, which is what makes replay-from-snapshot possible at all.
    let records = sched.storage_stats()[0].records_appended;
    sched.shutdown();
    records
}

fn time_recovery(dir: &std::path::Path, snapshot_every: u64) -> std::time::Duration {
    let cfg = EngineConfig {
        snapshot_every,
        ..EngineConfig::default()
    };
    let storage = wal(dir);
    let clock = SimClock::new(LogicalTime::from_millis(10_000_000));
    let t = Instant::now();
    let mut sched = SimScheduler::with_clock(7, &storage, registry(), cfg, clock).unwrap();
    sched.run_until_idle(); // replays to Blocked
    let elapsed = t.elapsed();
    assert_eq!(
        sched.states().get(&WorkflowId::new("big")),
        Some(&StateKind::Blocked),
        "recovery must land back in Blocked"
    );
    elapsed
}

#[test]
#[cfg_attr(
    debug_assertions,
    ignore = "slow + timing-sensitive: run in release (CI acceptance job)"
)]
fn snapshot_replay_is_10x_faster_than_full_replay() {
    // Store A: snapshots every 1000 records (default policy).
    let dir_snap = tempfile::tempdir().unwrap();
    let records_snap = build_history(dir_snap.path(), 1_000);
    // Store B: snapshots disabled — full replay from record 0.
    let dir_full = tempfile::tempdir().unwrap();
    let records_full = build_history(dir_full.path(), u64::MAX);

    assert!(
        records_full >= 100_000,
        "workload must journal >= 100k events, got {records_full}"
    );

    let t_full = time_recovery(dir_full.path(), u64::MAX);
    let t_snap = time_recovery(dir_snap.path(), 1_000);

    // Correctness of the lazy path: the recovered workflow still works.
    {
        let storage = wal(dir_snap.path());
        let clock = SimClock::new(LogicalTime::from_millis(20_000_000));
        let cfg = EngineConfig {
            snapshot_every: 1_000,
            ..EngineConfig::default()
        };
        let mut sched = SimScheduler::with_clock(7, &storage, registry(), cfg, clock).unwrap();
        let handle = sched.handle("big").unwrap();
        sched.signal("big", "finish", &1u64).unwrap();
        sched.run_until_idle();
        let sum: u64 = handle.result_blocking().unwrap();
        let expect: u64 = (0..STEPS).sum();
        assert_eq!(
            sum, expect,
            "lazy-recovered workflow must complete correctly"
        );
    }

    println!(
        "snapshot compaction: {records_snap} records with snapshots -> recovery {t_snap:?}; \
         {records_full} records full replay -> recovery {t_full:?}; \
         ratio {:.2}%",
        100.0 * t_snap.as_secs_f64() / t_full.as_secs_f64()
    );
    assert!(
        t_snap.as_secs_f64() < t_full.as_secs_f64() * 0.10,
        "snapshot replay ({t_snap:?}) must be under 10% of full replay ({t_full:?})"
    );
}
