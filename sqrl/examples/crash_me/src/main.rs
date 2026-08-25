//! # crash_me — kill -9 recovery, live
//!
//! This example is its own crash-test harness. The default (parent) mode:
//!
//! 1. wipes the demo data dir, then spawns *this same binary* as a worker
//!    child (`CRASH_ME_CHILD=1`) running a 5-step workflow (~200 ms/step),
//! 2. SIGKILLs the child ~600 ms in — mid-workflow, no cleanup, no flush,
//! 3. respawns the worker: it attaches to the same workflow id, replays the
//!    journal, and finishes from where the crash left off. Steps completed
//!    before the kill do **not** run again (watch the step numbers).
//!
//! The one step that was *in flight* when the kill landed may print twice:
//! sqrl guarantees at-least-once step execution (pair it with idempotency
//! keys for effectively-once side effects — see the checkout_saga example).
//!
//! Run with: `cargo run -p crash_me`

use sqrl::{Ctx, Error, FsyncPolicy, Rejected, Sqrl, WalStorage};
use std::io::Write;
use std::path::PathBuf;
use std::time::Duration;

/// Fixed workflow id: both worker runs address the same durable execution.
const WORKFLOW_ID: &str = "crash-demo";
const STEPS: u32 = 5;
const STEP_MS: u64 = 200;

/// Shared WAL directory — the whole point is that run 2 reopens run 1's log.
fn data_dir() -> PathBuf {
    std::env::temp_dir().join("sqrl-crash-me")
}

/// Print + flush. The child gets SIGKILLed with no chance to flush stdio,
/// so every line is pushed out eagerly (matters when output is piped).
fn say(msg: &str) {
    let mut out = std::io::stdout().lock();
    let _ = writeln!(out, "{msg}");
    let _ = out.flush();
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    if std::env::var("CRASH_ME_CHILD").is_ok() {
        child()
    } else {
        parent()
    }
}

// ---------------------------------------------------------------------------
// Parent: orchestrates the crash
// ---------------------------------------------------------------------------

fn parent() -> Result<(), Box<dyn std::error::Error>> {
    let dir = data_dir();
    let _ = std::fs::remove_dir_all(&dir); // fresh demo on every run
    say("=== sqrl crash_me: kill -9 recovery demo ===");
    say(&format!("data dir: {}", dir.display()));

    // Run 1: spawn the worker and kill -9 it mid-workflow.
    say("\n[parent] run 1: spawning worker; killing it with SIGKILL in ~600 ms");
    let mut worker = std::process::Command::new(std::env::current_exe()?)
        .env("CRASH_ME_CHILD", "1")
        .spawn()?;
    // Real wall-clock wait in the demo supervisor (not orchestration code).
    #[allow(clippy::disallowed_methods)] // supervisor timing, not workflow logic
    std::thread::sleep(Duration::from_millis(600));
    worker.kill()?; // SIGKILL: no destructors, no flush, no goodbye
    let status = worker.wait()?;
    say(&format!(
        "[parent] killed worker mid-workflow ({status}) — completed steps are already \
         fsynced in the WAL"
    ));

    // Run 2: respawn the worker, no kill. It must recover and finish.
    say("\n[parent] run 2: respawning worker; it should RESUME, not restart");
    let status = std::process::Command::new(std::env::current_exe()?)
        .env("CRASH_ME_CHILD", "1")
        .status()?;
    if !status.success() {
        return Err(format!("run 2 failed: {status}").into());
    }
    say("\n=== SUCCESS: workflow survived kill -9 and resumed from its last completed step ===");
    Ok(())
}

// ---------------------------------------------------------------------------
// Child: the worker that actually runs the workflow
// ---------------------------------------------------------------------------

fn child() -> Result<(), Box<dyn std::error::Error>> {
    // Detect a prior run *before* opening the engine — recovery itself is
    // automatic inside `build()` (which replays every non-terminal workflow
    // found in the WAL); this check exists only for tidy log ordering.
    let recovering = std::fs::read_dir(data_dir())
        .map(|mut d| d.next().is_some())
        .unwrap_or(false);
    if recovering {
        say(&format!(
            "[worker] found an existing WAL: recovering `{WORKFLOW_ID}` — completed steps \
             replay from the journal and will NOT re-execute (the step that was in flight \
             when the kill landed may run a second time: at-least-once)"
        ));
    }

    // Strict fsync: every journal record is durable before the engine
    // acknowledges it, so the kill window loses as little as possible.
    let sqrl = Sqrl::builder()
        .storage(WalStorage::open(data_dir())?)
        .fsync(FsyncPolicy::Strict)
        .register_fn("five-steps", 1, |ctx: Ctx, (): ()| async move {
            let mut done = 0u32;
            for n in 1..=STEPS {
                done = ctx
                    .step("work", move || async move {
                        say(&format!("[worker] executing step {n}"));
                        // Simulate ~200 ms of real work. A blocking sleep is
                        // fine *inside a step* for a demo — steps run on a
                        // dedicated pool, and real steps do I/O anyway.
                        #[allow(clippy::disallowed_methods)] // simulated work inside a step
                        std::thread::sleep(Duration::from_millis(STEP_MS));
                        Ok::<u32, String>(n)
                    })
                    .await?;
            }
            Ok::<u32, Error>(done)
        })
        .build()?;

    // Start the fixed id — or, after the crash, attach to the existing
    // execution. A workflow id can only be started once; `AlreadyExists` is
    // exactly how a restarted process discovers it has work in flight (the
    // engine already resumed it during `build()` — attaching just gets a
    // handle to await the result on).
    let handle = match sqrl.start_with_id_blocking(WORKFLOW_ID, "five-steps", &()) {
        Ok(h) => {
            say(&format!(
                "[worker] fresh start: workflow `{WORKFLOW_ID}` begins"
            ));
            h
        }
        Err(Error::Rejected(Rejected::AlreadyExists(_))) => {
            say(&format!("[worker] attached to in-flight `{WORKFLOW_ID}`"));
            sqrl.handle_blocking(WORKFLOW_ID)?
        }
        Err(e) => return Err(e.into()),
    };

    let done: u32 = handle.result_blocking()?;
    say(&format!(
        "[worker] workflow finished: {done}/{STEPS} steps completed"
    ));
    sqrl.shutdown();
    Ok(())
}
