//! Child process for the real `kill -9` acceptance tests.
//!
//! Usage: `crash_child <data-dir> <scenario>` where scenario is `saga`
//! (5 slow steps, each appending to `<data-dir>/effects.log`) or `sleeper`
//! (a durable 2-second `ctx.sleep`). The parent test SIGKILLs this process
//! mid-workflow, re-runs it, and asserts recovery semantics.
//!
//! Prints `RESULT:<value>` on success.

use sqrl::{Ctx, FsyncPolicy, Result, Sqrl, WalStorage};
use std::io::Write;
use std::path::{Path, PathBuf};
use std::time::Duration;

fn append_effect(dir: &Path, line: &str) {
    let mut f = std::fs::OpenOptions::new()
        .create(true)
        .append(true)
        .open(dir.join("effects.log"))
        .expect("open effects.log");
    // O_APPEND single-line writes are atomic enough for this test.
    writeln!(f, "{line}").expect("append effect");
    f.sync_all().expect("sync effects.log");
}

fn main() {
    let mut args = std::env::args().skip(1);
    let dir = PathBuf::from(args.next().expect("usage: crash_child <dir> <scenario>"));
    let scenario = args.next().expect("usage: crash_child <dir> <scenario>");

    let effects_dir = dir.clone();
    let effects_dir2 = dir.clone();
    let sqrl = Sqrl::builder()
        .storage(WalStorage::open(dir.join("wal")).expect("open wal"))
        .fsync(FsyncPolicy::Strict)
        .register_fn("saga", 1, move |ctx: Ctx, (): ()| {
            let dir = effects_dir.clone();
            async move {
                let mut total = 0u64;
                for step_no in 0..5u64 {
                    let dir = dir.clone();
                    let v: u64 = ctx
                        .step(&format!("step-{step_no}"), move || {
                            let dir = dir.clone();
                            async move {
                                append_effect(&dir, &format!("step-{step_no}"));
                                // Slow enough that SIGKILL lands mid-run.
                                // Real blocking sleep inside a step is fine —
                                // steps are where wall-clock effects live.
                                #[allow(clippy::disallowed_methods)]
                                std::thread::sleep(Duration::from_millis(150));
                                Ok::<u64, String>(step_no + 1)
                            }
                        })
                        .await?;
                    total += v;
                }
                Ok(total)
            }
        })
        .register_fn("sleeper", 1, move |ctx: Ctx, (): ()| {
            let dir = effects_dir2.clone();
            async move {
                let started = ctx.now();
                ctx.sleep(Duration::from_secs(2)).await?;
                let woke = ctx.now();
                let dir = dir.clone();
                ctx.step("after-sleep", move || {
                    let dir = dir.clone();
                    async move {
                        append_effect(&dir, "woke");
                        Ok::<(), String>(())
                    }
                })
                .await?;
                Ok::<(u64, u64), sqrl::Error>((started.as_millis(), woke.as_millis()))
            }
        })
        .build()
        .expect("build sqrl");

    let id = format!("{scenario}-wf");
    let handle = match sqrl.start_with_id_blocking(&*id, &scenario, &()) {
        Ok(h) => h,
        Err(sqrl::Error::Rejected(sqrl::Rejected::AlreadyExists(_))) => {
            eprintln!("crash_child: attaching to existing workflow {id}");
            sqrl.handle_blocking(&*id).expect("attach")
        }
        Err(e) => panic!("start failed: {e}"),
    };
    let result: Result<serde_json::Value> = match scenario.as_str() {
        "saga" => handle.result_blocking::<u64>().map(|v| v.into()),
        "sleeper" => handle
            .result_blocking::<(u64, u64)>()
            .map(|(a, b)| serde_json::json!([a, b])),
        other => panic!("unknown scenario {other}"),
    };
    match result {
        Ok(v) => {
            println!("RESULT:{v}");
            sqrl.shutdown();
        }
        Err(e) => {
            eprintln!("workflow failed: {e}");
            std::process::exit(2);
        }
    }
}
