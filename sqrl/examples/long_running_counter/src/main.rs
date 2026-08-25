//! # long_running_counter — snapshot compaction under a long history
//!
//! A workflow that executes 5 000 iterations of a trivial step, producing a
//! 10 000+-record journal. With `.snapshot_every(1_000)` the engine
//! periodically journals a *snapshot* of the workflow's state, so recovery
//! replays only `snapshot + records-after-snapshot` instead of the whole
//! history (and a completed workflow gets a compacting terminal snapshot).
//!
//! The demo prints the evidence:
//! 1. the live journal length right before completion (10 000+ records),
//! 2. how long a *fresh process* (same store dir, new engine) takes to
//!    attach to the workflow and fetch its result — milliseconds, because
//!    recovery loads the newest snapshot rather than re-running the journal.
//!
//! Run with: `cargo run -p long_running_counter`

use sqrl::{Ctx, Error, Sqrl, StateKind, WalStorage};
use std::future::Future;
use std::path::Path;
use std::pin::pin;
use std::sync::Arc;
use std::task::{Context, Poll, Wake, Waker};
use std::time::Duration;

const ITERS: u64 = 5_000;
const WF_ID: &str = "counter-demo";

// ---------------------------------------------------------------------------
// A 20-line executor
// ---------------------------------------------------------------------------

/// sqrl's async APIs are runtime-agnostic; most have `*_blocking` variants,
/// but `Sqrl::status()` does not — so we drive it with a minimal park/unpark
/// executor instead of pulling in a runtime.
struct ThreadWaker(std::thread::Thread);

impl Wake for ThreadWaker {
    fn wake(self: Arc<Self>) {
        self.0.unpark();
    }
}

fn block_on<F: Future>(fut: F) -> F::Output {
    let mut fut = pin!(fut);
    let waker: Waker = Arc::new(ThreadWaker(std::thread::current())).into();
    let mut cx = Context::from_waker(&waker);
    loop {
        match fut.as_mut().poll(&mut cx) {
            Poll::Ready(v) => return v,
            Poll::Pending => std::thread::park(),
        }
    }
}

// ---------------------------------------------------------------------------
// Engine setup
// ---------------------------------------------------------------------------

/// Both "processes" of the demo (before and after the reopen) build the
/// engine the same way — as a real deployment would on every boot.
fn engine(dir: &Path) -> sqrl::Result<Sqrl> {
    Sqrl::builder()
        .storage(WalStorage::open(dir)?)
        // Snapshot roughly every 1 000 journal records (amortized: the
        // engine also waits until the delta is a quarter of total history,
        // keeping cumulative snapshot bytes O(history)).
        .snapshot_every(1_000)
        .register_fn("counter", 1, |ctx: Ctx, iters: u64| async move {
            let mut total = 0u64;
            for i in 0..iters {
                // A trivial step: 2 journal records each (scheduled +
                // completed), so `iters` iterations => 2 * iters records.
                total += ctx
                    .step("tick", move || async move { Ok::<u64, String>(i + 1) })
                    .await?;
            }
            // Hold the workflow open (non-terminal) until main() has read
            // the journal length via status(), then finish on a signal.
            ctx.await_signal::<()>("finish").await?;
            Ok::<u64, Error>(total)
        })
        .build()
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let dir = std::env::temp_dir().join(format!("sqrl-counter-{}", std::process::id()));
    println!("=== sqrl long_running_counter: snapshot compaction ===");
    println!("data dir: {}", dir.display());

    // Phase 1: run the 5 000-step workflow and watch the journal grow. ----
    // (Wall-clock timing lives in main(), never in orchestration code.)
    #[allow(clippy::disallowed_methods)] // demo timing in main()
    let t_run = std::time::Instant::now();
    let sqrl = engine(&dir)?;
    let handle = sqrl.start_with_id_blocking(WF_ID, "counter", &ITERS)?;
    println!("[phase 1] running {ITERS} step iterations...");

    // Poll status() until every step is done and the workflow blocks on the
    // final signal, printing the journal length as it climbs.
    let mut last_printed = 0u64;
    let journal_len = loop {
        let entries = block_on(sqrl.status());
        let entry = entries
            .iter()
            .find(|e| e.id.as_str() == WF_ID)
            .ok_or("workflow missing from status()")?;
        if entry.state == StateKind::Blocked {
            break entry.records; // all steps journaled; exact final count
        }
        if entry.records >= last_printed + 2_500 {
            last_printed = entry.records;
            println!("[phase 1]   journal: {} records so far", entry.records);
        }
        #[allow(clippy::disallowed_methods)] // status poll interval in main()
        std::thread::sleep(Duration::from_millis(100));
    };
    println!("[phase 1] all steps done: journal holds {journal_len} records for `{WF_ID}`");

    sqrl.signal_blocking(WF_ID, "finish", &())?;
    let total: u64 = handle.result_blocking()?;
    println!(
        "[phase 1] completed in {:.1?}: sum of 1..={ITERS} = {total}",
        t_run.elapsed()
    );
    sqrl.shutdown(); // flush + fsync, drop all in-memory state

    // Phase 2: fresh engine, same dir — how fast is recovery? ------------
    #[allow(clippy::disallowed_methods)] // demo timing in main()
    let t_reopen = std::time::Instant::now();
    let sqrl2 = engine(&dir)?; // recovery happens inside build()
    let h2 = sqrl2.handle_blocking(WF_ID)?; // attach to existing workflow
    let recovered: u64 = h2.result_blocking()?; // fetch its durable result
    let reopen_ms = t_reopen.elapsed().as_millis();

    println!("[phase 2] fresh engine on the same dir: reopen + attach + result = {reopen_ms} ms");
    println!(
        "[phase 2] recovered result: {recovered} (matches: {})",
        recovered == total
    );
    println!(
        "[phase 2] why so fast: recovery loads the newest snapshot and replays only the \
         records after it — here a compacting terminal snapshot, not the {journal_len}-record \
         journal. Without snapshots, reopening would re-run all {journal_len} records."
    );
    sqrl2.shutdown();

    std::fs::remove_dir_all(&dir)?;
    println!("=== done (data dir removed) ===");
    Ok(())
}
