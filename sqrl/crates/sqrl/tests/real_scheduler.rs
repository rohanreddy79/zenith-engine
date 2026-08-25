//! End-to-end tests of the production stack: `Sqrl` builder →
//! `RealScheduler` (thread-per-core) → Tokio step pool → `WalStorage` on a
//! real filesystem. The `kill -9` recovery test lives in the workspace
//! `tests` crate (it needs a subprocess binary).

use sqrl::{Ctx, Error, FsyncPolicy, MemoryStorage, Result, Sqrl, WalOptions, WalStorage};
use std::sync::atomic::{AtomicU32, Ordering};
use std::sync::Arc;
use std::time::Duration;

fn wal(dir: &std::path::Path, shards: u32) -> WalStorage {
    WalStorage::open_with(
        Arc::new(sqrl::StdVfs::new(dir.to_path_buf()).unwrap()),
        WalOptions {
            num_shards: shards,
            segment_size: 1024 * 1024,
        },
    )
    .unwrap()
}

#[tokio::test]
async fn workflow_completes_on_real_scheduler_and_tokio_steps() {
    let dir = tempfile::tempdir().unwrap();
    let counter = Arc::new(AtomicU32::new(0));
    let c = Arc::clone(&counter);
    let sqrl = Sqrl::builder()
        .storage(wal(dir.path(), 2))
        .fsync(FsyncPolicy::Strict)
        .register_fn("double", 1, move |ctx: Ctx, n: u64| {
            let c = Arc::clone(&c);
            async move {
                let c2 = Arc::clone(&c);
                let doubled: u64 = ctx
                    .step("double", move || {
                        let c2 = Arc::clone(&c2);
                        async move {
                            c2.fetch_add(1, Ordering::SeqCst);
                            // Prove steps really run on the Tokio pool.
                            tokio::time::sleep(Duration::from_millis(5)).await;
                            Ok::<u64, String>(n * 2)
                        }
                    })
                    .await?;
                ctx.sleep(Duration::from_millis(50)).await?;
                Ok(doubled + 1)
            }
        })
        .build()
        .unwrap();

    let handle = sqrl.start("double", &21u64).await.unwrap();
    let out: u64 = handle.result().await.unwrap();
    assert_eq!(out, 43);
    assert_eq!(counter.load(Ordering::SeqCst), 1);
    sqrl.shutdown();
}

#[tokio::test]
async fn restart_recovers_completed_and_blocked_workflows() {
    let dir = tempfile::tempdir().unwrap();
    let build = |dir: &std::path::Path| {
        Sqrl::builder()
            .storage(wal(dir, 1))
            .fsync(FsyncPolicy::Strict)
            .register_fn("waiter", 1, move |ctx: Ctx, (): ()| async move {
                let v: u64 = ctx.await_signal("go").await?;
                Ok(v * 10)
            })
            .build()
            .unwrap()
    };
    {
        let sqrl = build(dir.path());
        let _h = sqrl
            .start_with_id("wf-blocked", "waiter", &())
            .await
            .unwrap();
        // Give the engine a moment to journal, then shut down (flushes).
        sqrl.shutdown();
    }
    // Fresh process: workflow must be recovered, still blocked, and wake on
    // signal.
    let sqrl = build(dir.path());
    let handle = sqrl.handle("wf-blocked").await.unwrap();
    sqrl.signal("wf-blocked", "go", &7u64).await.unwrap();
    let out: u64 = handle.result().await.unwrap();
    assert_eq!(out, 70);
    sqrl.shutdown();
}

#[tokio::test]
async fn concurrent_workflows_across_shards() {
    let dir = tempfile::tempdir().unwrap();
    let sqrl = Sqrl::builder()
        .storage(wal(dir.path(), 4))
        .register_fn("add", 1, move |ctx: Ctx, n: u64| async move {
            let v: u64 = ctx
                .step("inc", move || async move { Ok::<u64, String>(n + 1) })
                .await?;
            Ok(v)
        })
        .build()
        .unwrap();
    assert_eq!(sqrl.num_shards(), 4);
    let mut handles = Vec::new();
    for i in 0..50u64 {
        handles.push((
            i,
            sqrl.start_with_id(format!("wf-{i}"), "add", &i)
                .await
                .unwrap(),
        ));
    }
    for (i, h) in handles {
        let out: u64 = h.result().await.unwrap();
        assert_eq!(out, i + 1);
    }
    let status = sqrl.status().await;
    assert_eq!(status.len(), 50);
    assert!(status.iter().all(|s| s.state == sqrl::StateKind::Completed));
    sqrl.shutdown();
}

#[tokio::test]
async fn memory_storage_works_for_tests() {
    let sqrl = Sqrl::builder()
        .storage(MemoryStorage::new(2))
        .register_fn("echo", 1, |_ctx: Ctx, s: String| async move {
            Ok::<String, Error>(s)
        })
        .build()
        .unwrap();
    let h = sqrl.start("echo", &"hi".to_string()).await.unwrap();
    let out: String = h.result().await.unwrap();
    assert_eq!(out, "hi");
}

#[tokio::test]
async fn duplicate_id_rejected() {
    let sqrl = Sqrl::builder()
        .storage(MemoryStorage::new(1))
        .register_fn("waiter", 1, |ctx: Ctx, (): ()| async move {
            let v: u64 = ctx.await_signal("never").await?;
            Ok(v)
        })
        .build()
        .unwrap();
    sqrl.start_with_id("dup", "waiter", &()).await.unwrap();
    let err = sqrl.start_with_id("dup", "waiter", &()).await.unwrap_err();
    assert!(
        matches!(err, Error::Rejected(sqrl::Rejected::AlreadyExists(_))),
        "{err:?}"
    );
}

/// Result is only released once durable: under Strict fsync every completed
/// workflow's terminal record has hit the disk before `result()` returns.
#[test]
fn blocking_api_without_any_runtime() {
    let dir = tempfile::tempdir().unwrap();
    let sqrl = Sqrl::builder()
        .storage(wal(dir.path(), 1))
        .fsync(FsyncPolicy::Strict)
        .register_fn("mul", 1, |ctx: Ctx, n: u64| async move {
            let v: u64 = ctx
                .step("mul3", move || async move { Ok::<u64, String>(n * 3) })
                .await?;
            Ok(v)
        })
        .build()
        .unwrap();
    let h = sqrl.start_blocking("mul", &5u64).unwrap();
    let out: u64 = h.result_blocking().unwrap();
    assert_eq!(out, 15);
    sqrl.shutdown();
}
