//! End-to-end benchmark harness for sqrl (workloads W1–W5 + latency + memory).
//!
//! Every run prints a single JSON object with throughput, latency
//! percentiles, RSS, fsync counts, and write amplification, so results in
//! `docs/benchmarks.md` are reproducible with one command. Comparison
//! harnesses for DBOS/Temporal/Restate live in `comparisons/`.

#![allow(clippy::disallowed_methods)] // wall-clock measurement is the point here

use clap::{Parser, Subcommand};
use serde::Serialize;
use sqrl::{Ctx, Error, FsyncPolicy, Sqrl, StdVfs, WalOptions, WalStorage, WorkflowId};
use std::path::PathBuf;
use std::sync::Arc;
use std::time::{Duration, Instant};

#[derive(Parser)]
#[command(
    name = "sqrl-bench-harness",
    about = "sqrl workload benchmarks (W1-W5)"
)]
struct Args {
    #[command(subcommand)]
    workload: Workload,
    /// Data directory (default: a temp dir, removed afterwards).
    #[arg(long, global = true)]
    data: Option<PathBuf>,
    /// Fsync policy: strict | group | relaxed
    #[arg(long, global = true, default_value = "group")]
    fsync: String,
    /// Storage/engine shards (default: available cores).
    #[arg(long, global = true)]
    shards: Option<u32>,
}

#[derive(Subcommand)]
enum Workload {
    /// W1: N concurrent workflows x M trivial steps (start-locally shape).
    W1 {
        #[arg(long, default_value_t = 1000)]
        workflows: u64,
        #[arg(long, default_value_t = 5)]
        steps: u64,
    },
    /// W2: saga fan-out — parents each spawning K child workflows.
    W2 {
        #[arg(long, default_value_t = 100)]
        parents: u64,
        #[arg(long, default_value_t = 10)]
        children: u64,
    },
    /// W3: one workflow with N steps (no history cap; snapshot compaction).
    W3 {
        #[arg(long, default_value_t = 1_000_000)]
        steps: u64,
    },
    /// W4: crash with N in-flight workflows; measure time-to-fully-resumed.
    W4 {
        #[arg(long, default_value_t = 1000)]
        workflows: u64,
    },
    /// W5: skew — most traffic hashing to few shards; run uniform vs skewed.
    W5 {
        #[arg(long, default_value_t = 2000)]
        workflows: u64,
        #[arg(long, default_value_t = 5)]
        steps: u64,
        /// Fraction of workflows forced onto shard 0.
        #[arg(long, default_value_t = 0.9)]
        skew: f64,
    },
    /// Per-step commit latency percentiles under the chosen fsync policy.
    Latency {
        #[arg(long, default_value_t = 2000)]
        samples: u64,
    },
    /// Memory per passivated (idle) workflow.
    Mem {
        #[arg(long, default_value_t = 10_000)]
        workflows: u64,
    },
}

#[derive(Serialize)]
struct Report {
    workload: String,
    params: serde_json::Value,
    elapsed_s: f64,
    workflows_per_s: Option<f64>,
    steps_per_s: Option<f64>,
    p50_ms: Option<f64>,
    p99_ms: Option<f64>,
    p999_ms: Option<f64>,
    rss_mb: f64,
    fsyncs: u64,
    records_appended: u64,
    bytes_written: u64,
    write_amp_bytes_per_step: Option<f64>,
    fsyncs_per_step: Option<f64>,
    recovery_ms: Option<f64>,
    extra: serde_json::Value,
}

fn rss_mb() -> f64 {
    std::fs::read_to_string("/proc/self/status")
        .ok()
        .and_then(|s| {
            s.lines().find(|l| l.starts_with("VmRSS:")).and_then(|l| {
                l.split_whitespace()
                    .nth(1)
                    .and_then(|kb| kb.parse::<f64>().ok())
            })
        })
        .map(|kb| kb / 1024.0)
        .unwrap_or(-1.0)
}

fn percentile(sorted: &[f64], p: f64) -> f64 {
    if sorted.is_empty() {
        return 0.0;
    }
    let idx = ((sorted.len() as f64 - 1.0) * p).round() as usize;
    sorted[idx.min(sorted.len() - 1)]
}

fn parse_fsync(s: &str) -> FsyncPolicy {
    match s {
        "strict" => FsyncPolicy::Strict,
        "relaxed" => FsyncPolicy::Relaxed {
            interval: Duration::from_millis(500),
        },
        _ => FsyncPolicy::default_group(),
    }
}

struct Env {
    dir: PathBuf,
    _tmp: Option<tempfile::TempDir>,
    fsync: FsyncPolicy,
    shards: u32,
}

impl Env {
    fn new(args: &Args) -> Env {
        let (dir, tmp) = match &args.data {
            Some(d) => (d.clone(), None),
            None => {
                let t = tempfile::tempdir().expect("tempdir");
                (t.path().to_path_buf(), Some(t))
            }
        };
        Env {
            dir,
            _tmp: tmp,
            fsync: parse_fsync(&args.fsync),
            shards: args.shards.unwrap_or_else(|| {
                std::thread::available_parallelism()
                    .map(|n| n.get() as u32)
                    .unwrap_or(4)
            }),
        }
    }

    fn storage(&self) -> WalStorage {
        WalStorage::open_with(
            Arc::new(StdVfs::new(self.dir.clone()).expect("vfs")),
            WalOptions {
                num_shards: self.shards,
                segment_size: 64 * 1024 * 1024,
            },
        )
        .expect("open store")
    }
}

fn register_stepper(b: sqrl::SqrlBuilder) -> sqrl::SqrlBuilder {
    b.register_fn("stepper", 1, |ctx: Ctx, m: u64| async move {
        let mut acc = 0u64;
        for s in 0..m {
            let v: u64 = ctx
                .step("s", move || async move { Ok::<u64, String>(s) })
                .await?;
            acc = acc.wrapping_add(v);
        }
        Ok(acc)
    })
}

fn collect_stats(sqrl: &Sqrl) -> (u64, u64, u64) {
    let stats = sqrl.stats_blocking();
    let mut fsyncs = 0;
    let mut records = 0;
    let mut bytes = 0;
    for (_m, s) in stats {
        fsyncs += s.fsyncs;
        records += s.records_appended;
        bytes += s.bytes_written;
    }
    (fsyncs, records, bytes)
}

fn report(mut r: Report) {
    r.rss_mb = rss_mb();
    println!("{}", serde_json::to_string_pretty(&r).expect("json"));
}

fn main() {
    let args = Args::parse();
    // W4 child mode: start workflows with a hanging step, print READY, hang.
    if std::env::var("SQRL_W4_CHILD").is_ok() {
        w4_child(&args);
        return;
    }
    match &args.workload {
        Workload::W1 { workflows, steps } => w1(&args, *workflows, *steps),
        Workload::W2 { parents, children } => w2(&args, *parents, *children),
        Workload::W3 { steps } => w3(&args, *steps),
        Workload::W4 { workflows } => w4(&args, *workflows),
        Workload::W5 {
            workflows,
            steps,
            skew,
        } => w5(&args, *workflows, *steps, *skew),
        Workload::Latency { samples } => latency(&args, *samples),
        Workload::Mem { workflows } => mem(&args, *workflows),
    }
}

fn w1(args: &Args, n: u64, m: u64) {
    let env = Env::new(args);
    let sqrl = register_stepper(Sqrl::builder().storage(env.storage()).fsync(env.fsync))
        .build()
        .expect("build");
    let t0 = Instant::now();
    let mut handles = Vec::with_capacity(n as usize);
    let mut starts = Vec::with_capacity(n as usize);
    for i in 0..n {
        starts.push(Instant::now());
        handles.push(
            sqrl.start_with_id_blocking(format!("w1-{i}"), "stepper", &m)
                .expect("start"),
        );
    }
    let mut lat: Vec<f64> = Vec::with_capacity(n as usize);
    for (i, h) in handles.iter().enumerate() {
        let _: u64 = h.result_blocking().expect("result");
        lat.push(starts[i].elapsed().as_secs_f64() * 1000.0);
    }
    let elapsed = t0.elapsed().as_secs_f64();
    lat.sort_by(f64::total_cmp);
    let (fsyncs, records, bytes) = collect_stats(&sqrl);
    let total_steps = (n * m) as f64;
    report(Report {
        workload: "w1".into(),
        params: serde_json::json!({"workflows": n, "steps": m, "fsync": args.fsync, "shards": env.shards}),
        elapsed_s: elapsed,
        workflows_per_s: Some(n as f64 / elapsed),
        steps_per_s: Some(total_steps / elapsed),
        p50_ms: Some(percentile(&lat, 0.50)),
        p99_ms: Some(percentile(&lat, 0.99)),
        p999_ms: Some(percentile(&lat, 0.999)),
        rss_mb: 0.0,
        fsyncs,
        records_appended: records,
        bytes_written: bytes,
        write_amp_bytes_per_step: Some(bytes as f64 / total_steps),
        fsyncs_per_step: Some(fsyncs as f64 / total_steps),
        recovery_ms: None,
        extra: serde_json::json!({}),
    });
    sqrl.shutdown();
}

fn w2(args: &Args, parents: u64, children: u64) {
    use std::sync::OnceLock;
    static SQRL: OnceLock<Sqrl> = OnceLock::new();
    let env = Env::new(args);
    // Parent-child pattern without blocking the step pool: a parent step
    // fire-and-forgets K child workflows, then the parent durably collects
    // one "child-done" signal per child. Children report back via a final
    // step that delivers the signal.
    let builder = register_stepper(Sqrl::builder().storage(env.storage()).fsync(env.fsync))
        .register_fn("parent", 1, move |ctx: Ctx, k: u64| async move {
            let me = ctx.id().to_string();
            ctx.step("spawn-children", move || {
                let me = me.clone();
                async move {
                    let sqrl = SQRL.get().expect("engine");
                    for c in 0..k {
                        let id = format!("{me}-child-{c}");
                        match sqrl.start_with_id_blocking(&*id, "child", &(me.clone(), 3u64)) {
                            Ok(_) => {}
                            Err(Error::Rejected(sqrl::Rejected::AlreadyExists(_))) => {}
                            Err(e) => return Err(e.to_string()),
                        }
                    }
                    Ok::<u64, String>(k)
                }
            })
            .await?;
            let mut sum = 0u64;
            for _ in 0..k {
                let v: u64 = ctx.await_signal("child-done").await?;
                sum = sum.wrapping_add(v);
            }
            Ok(sum)
        })
        .register_fn(
            "child",
            1,
            move |ctx: Ctx, (parent, m): (String, u64)| async move {
                let mut acc = 0u64;
                for s in 0..m {
                    let v: u64 = ctx
                        .step("s", move || async move { Ok::<u64, String>(s) })
                        .await?;
                    acc = acc.wrapping_add(v);
                }
                let acc2 = acc;
                ctx.step("notify-parent", move || {
                    let parent = parent.clone();
                    async move {
                        let sqrl = SQRL.get().expect("engine");
                        sqrl.signal_blocking(&*parent, "child-done", &acc2)
                            .map_err(|e| e.to_string())?;
                        Ok::<(), String>(())
                    }
                })
                .await?;
                Ok(acc)
            },
        );
    let sqrl = builder.build().expect("build");
    // Set before any parent runs.
    let sqrl = SQRL.get_or_init(|| sqrl);
    let t0 = Instant::now();
    let mut handles = Vec::new();
    for p in 0..parents {
        handles.push(
            sqrl.start_with_id_blocking(format!("w2-{p}"), "parent", &children)
                .expect("start"),
        );
    }
    for h in handles {
        let _: u64 = h.result_blocking().expect("parent result");
    }
    let elapsed = t0.elapsed().as_secs_f64();
    let (fsyncs, records, bytes) = collect_stats(sqrl);
    let total_wf = parents + parents * children;
    report(Report {
        workload: "w2".into(),
        params: serde_json::json!({"parents": parents, "children": children, "fsync": args.fsync}),
        elapsed_s: elapsed,
        workflows_per_s: Some(total_wf as f64 / elapsed),
        steps_per_s: None,
        p50_ms: None,
        p99_ms: None,
        p999_ms: None,
        rss_mb: 0.0,
        fsyncs,
        records_appended: records,
        bytes_written: bytes,
        write_amp_bytes_per_step: None,
        fsyncs_per_step: None,
        recovery_ms: None,
        extra: serde_json::json!({"total_workflows": total_wf}),
    });
}

fn w3(args: &Args, steps: u64) {
    let env = Env::new(args);
    let sqrl = register_stepper(Sqrl::builder().storage(env.storage()).fsync(env.fsync))
        .build()
        .expect("build");
    let t0 = Instant::now();
    let h = sqrl
        .start_with_id_blocking("w3-long", "stepper", &steps)
        .expect("start");
    let out: u64 = h.result_blocking().expect("result");
    assert_eq!(out, (0..steps).fold(0u64, |a, b| a.wrapping_add(b)));
    let elapsed = t0.elapsed().as_secs_f64();
    let (fsyncs, records, bytes) = collect_stats(&sqrl);
    report(Report {
        workload: "w3".into(),
        params: serde_json::json!({"steps": steps, "fsync": args.fsync}),
        elapsed_s: elapsed,
        workflows_per_s: None,
        steps_per_s: Some(steps as f64 / elapsed),
        p50_ms: None,
        p99_ms: None,
        p999_ms: None,
        rss_mb: 0.0,
        fsyncs,
        records_appended: records,
        bytes_written: bytes,
        write_amp_bytes_per_step: Some(bytes as f64 / steps as f64),
        fsyncs_per_step: Some(fsyncs as f64 / steps as f64),
        recovery_ms: None,
        extra: serde_json::json!({"note": "validates no history cap"}),
    });
    sqrl.shutdown();
}

fn w4_registry(b: sqrl::SqrlBuilder) -> sqrl::SqrlBuilder {
    b.register_fn("hanging", 1, |ctx: Ctx, (): ()| async move {
        let v: u64 = ctx
            .step("hang", move || async move {
                // In-flight forever (until the process is killed).
                loop {
                    tokio::time::sleep(Duration::from_secs(3600)).await;
                    if false {
                        break;
                    }
                }
                Ok::<u64, String>(0)
            })
            .await?;
        Ok(v)
    })
}

fn w4_child(args: &Args) {
    let n: u64 = std::env::var("SQRL_W4_N").expect("N").parse().expect("N");
    let env = Env::new(args);
    let sqrl = w4_registry(Sqrl::builder().storage(env.storage()).fsync(env.fsync))
        .build()
        .expect("build");
    for i in 0..n {
        sqrl.start_with_id_blocking(format!("w4-{i}"), "hanging", &())
            .expect("start");
    }
    println!("READY");
    // Park forever; the parent SIGKILLs us.
    loop {
        std::thread::sleep(Duration::from_secs(3600));
    }
}

fn w4(args: &Args, n: u64) {
    use std::io::BufRead;
    let data = args
        .data
        .clone()
        .unwrap_or_else(|| std::env::temp_dir().join(format!("sqrl-w4-{}", std::process::id())));
    let _ = std::fs::remove_dir_all(&data);
    // Phase 1: child starts N workflows with hanging steps, then dies hard.
    let mut child = std::process::Command::new(std::env::current_exe().expect("exe"))
        .args(["w4", "--workflows", &n.to_string()])
        .args(["--data", data.to_str().expect("utf8 path")])
        .args(["--fsync", &args.fsync])
        .env("SQRL_W4_CHILD", "1")
        .env("SQRL_W4_N", n.to_string())
        .stdout(std::process::Stdio::piped())
        .spawn()
        .expect("spawn child");
    let mut reader = std::io::BufReader::new(child.stdout.take().expect("stdout"));
    let mut line = String::new();
    loop {
        line.clear();
        reader.read_line(&mut line).expect("child output");
        if line.trim() == "READY" {
            break;
        }
    }
    child.kill().expect("SIGKILL");
    let _ = child.wait();

    // Phase 2: recover; "fully resumed" = every workflow is back in
    // AwaitingStep with its hanging step re-dispatched.
    let env = Env {
        dir: data.clone(),
        _tmp: None,
        fsync: parse_fsync(&args.fsync),
        shards: args.shards.unwrap_or_else(|| {
            std::thread::available_parallelism()
                .map(|x| x.get() as u32)
                .unwrap_or(4)
        }),
    };
    let t0 = Instant::now();
    let sqrl = w4_registry(Sqrl::builder().storage(env.storage()).fsync(env.fsync))
        .build()
        .expect("recover");
    let resumed_in;
    loop {
        let status = sqrl.status_blocking();
        let awaiting = status
            .iter()
            .filter(|s| s.state == sqrl::StateKind::AwaitingStep)
            .count() as u64;
        if awaiting >= n {
            resumed_in = t0.elapsed();
            break;
        }
        if t0.elapsed() > Duration::from_secs(120) {
            panic!("recovery did not complete: {awaiting}/{n} resumed");
        }
        std::thread::sleep(Duration::from_millis(10));
    }
    let (fsyncs, records, bytes) = collect_stats(&sqrl);
    report(Report {
        workload: "w4".into(),
        params: serde_json::json!({"workflows": n, "fsync": args.fsync}),
        elapsed_s: resumed_in.as_secs_f64(),
        workflows_per_s: Some(n as f64 / resumed_in.as_secs_f64()),
        steps_per_s: None,
        p50_ms: None,
        p99_ms: None,
        p999_ms: None,
        rss_mb: 0.0,
        fsyncs,
        records_appended: records,
        bytes_written: bytes,
        write_amp_bytes_per_step: None,
        fsyncs_per_step: None,
        recovery_ms: Some(resumed_in.as_secs_f64() * 1000.0),
        extra: serde_json::json!({"meaning": "kill -9 with N in-flight steps -> all redispatched"}),
    });
    drop(sqrl);
    let _ = std::fs::remove_dir_all(&data);
}

fn w5(args: &Args, n: u64, m: u64, skew: f64) {
    let run = |skewed: bool| -> (f64, Vec<u64>) {
        let env = Env::new(args);
        let shards = env.shards as usize;
        let sqrl = register_stepper(Sqrl::builder().storage(env.storage()).fsync(env.fsync))
            .build()
            .expect("build");
        // Pre-compute ids: skewed = `skew` fraction of ids hash to shard 0.
        let mut ids = Vec::with_capacity(n as usize);
        let mut counter = 0u64;
        for i in 0..n {
            if skewed && (i as f64 / n as f64) < skew {
                loop {
                    let id = format!("hot-{counter}");
                    counter += 1;
                    if WorkflowId::new(&*id).shard(shards) == 0 {
                        ids.push(id);
                        break;
                    }
                }
            } else {
                ids.push(format!("uni-{i}"));
            }
        }
        let t0 = Instant::now();
        let handles: Vec<_> = ids
            .iter()
            .map(|id| {
                sqrl.start_with_id_blocking(&**id, "stepper", &m)
                    .expect("start")
            })
            .collect();
        for h in handles {
            let _: u64 = h.result_blocking().expect("result");
        }
        let elapsed = t0.elapsed().as_secs_f64();
        let per_shard: Vec<u64> = sqrl
            .stats_blocking()
            .iter()
            .map(|(m, _)| m.completions)
            .collect();
        sqrl.shutdown();
        (elapsed, per_shard)
    };
    let (t_uniform, shard_uniform) = run(false);
    let (t_skewed, shard_skewed) = run(true);
    report(Report {
        workload: "w5".into(),
        params: serde_json::json!({"workflows": n, "steps": m, "skew": skew, "fsync": args.fsync}),
        elapsed_s: t_skewed,
        workflows_per_s: Some(n as f64 / t_skewed),
        steps_per_s: None,
        p50_ms: None,
        p99_ms: None,
        p999_ms: None,
        rss_mb: 0.0,
        fsyncs: 0,
        records_appended: 0,
        bytes_written: 0,
        write_amp_bytes_per_step: None,
        fsyncs_per_step: None,
        recovery_ms: None,
        extra: serde_json::json!({
            "uniform_elapsed_s": t_uniform,
            "skewed_elapsed_s": t_skewed,
            "skew_slowdown": t_skewed / t_uniform,
            "uniform_per_shard_completions": shard_uniform,
            "skewed_per_shard_completions": shard_skewed,
        }),
    });
}

fn latency(args: &Args, samples: u64) {
    let env = Env::new(args);
    let sqrl = register_stepper(Sqrl::builder().storage(env.storage()).fsync(env.fsync))
        .build()
        .expect("build");
    let mut lat = Vec::with_capacity(samples as usize);
    let t0 = Instant::now();
    for i in 0..samples {
        let t = Instant::now();
        let h = sqrl
            .start_with_id_blocking(format!("lat-{i}"), "stepper", &1u64)
            .expect("start");
        let _: u64 = h.result_blocking().expect("result");
        lat.push(t.elapsed().as_secs_f64() * 1000.0);
    }
    let elapsed = t0.elapsed().as_secs_f64();
    lat.sort_by(f64::total_cmp);
    let (fsyncs, records, bytes) = collect_stats(&sqrl);
    report(Report {
        workload: "latency".into(),
        params: serde_json::json!({"samples": samples, "fsync": args.fsync, "note": "1-step workflow, sequential: start->durable result"}),
        elapsed_s: elapsed,
        workflows_per_s: Some(samples as f64 / elapsed),
        steps_per_s: None,
        p50_ms: Some(percentile(&lat, 0.50)),
        p99_ms: Some(percentile(&lat, 0.99)),
        p999_ms: Some(percentile(&lat, 0.999)),
        rss_mb: 0.0,
        fsyncs,
        records_appended: records,
        bytes_written: bytes,
        write_amp_bytes_per_step: Some(bytes as f64 / samples as f64),
        fsyncs_per_step: Some(fsyncs as f64 / samples as f64),
        recovery_ms: None,
        extra: serde_json::json!({}),
    });
    sqrl.shutdown();
}

fn mem(args: &Args, n: u64) {
    let env = Env::new(args);
    let sqrl = Sqrl::builder()
        .storage(env.storage())
        .fsync(env.fsync)
        .passivate_after(Some(Duration::from_millis(300)))
        .register_fn("idler", 1, |ctx: Ctx, (): ()| async move {
            let v: u64 = ctx.await_signal("wake").await?;
            Ok(v)
        })
        .build()
        .expect("build");
    let rss_before = rss_mb();
    for i in 0..n {
        sqrl.start_with_id_blocking(format!("mem-{i}"), "idler", &())
            .expect("start");
    }
    let rss_active = rss_mb();
    // Wait for passivation (idle > 300ms + sweep interval).
    let t0 = Instant::now();
    let passivated_all;
    loop {
        std::thread::sleep(Duration::from_millis(200));
        let status = sqrl.status_blocking();
        let passivated = status.iter().filter(|s| s.passivated).count() as u64;
        if passivated >= n {
            passivated_all = true;
            break;
        }
        if t0.elapsed() > Duration::from_secs(60) {
            passivated_all = false;
            break;
        }
    }
    let rss_passive = rss_mb();
    report(Report {
        workload: "mem".into(),
        params: serde_json::json!({"workflows": n}),
        elapsed_s: t0.elapsed().as_secs_f64(),
        workflows_per_s: None,
        steps_per_s: None,
        p50_ms: None,
        p99_ms: None,
        p999_ms: None,
        rss_mb: 0.0,
        fsyncs: 0,
        records_appended: 0,
        bytes_written: 0,
        write_amp_bytes_per_step: None,
        fsyncs_per_step: None,
        recovery_ms: None,
        extra: serde_json::json!({
            "rss_before_mb": rss_before,
            "rss_active_mb": rss_active,
            "rss_passivated_mb": rss_passive,
            "active_kb_per_workflow": (rss_active - rss_before) * 1024.0 / n as f64,
            "passivated_kb_per_workflow": (rss_passive - rss_before) * 1024.0 / n as f64,
            "all_passivated": passivated_all,
        }),
    });
    sqrl.shutdown();
}
