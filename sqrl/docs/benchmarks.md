# Benchmarks

**Rule of the house: no number without a reproduction command.** Every
number below was produced by the exact command shown, on the environment
described. Anything not runnable in the development environment is marked
**UNVERIFIED** with the script a human needs.

## Environment (all recorded numbers)

| | |
|---|---|
| CPU | Intel Xeon @ 2.80 GHz, 4 vCPU (virtualized) |
| RAM | 15 GiB |
| Disk | virtio (`/dev/vda`), ext4, non-rotational; **cloud-virtualized — fsync latency is NOT representative of local NVMe** |
| OS / kernel | Linux 6.18.44 |
| Rust | 1.94.1 (release profile, debug symbols on) |
| Commit | see `git log` — numbers are refreshed per release |

Caveat honesty: this is a shared 4-vCPU VM. Treat absolute numbers as
order-of-magnitude; the *relative* comparisons (fsync policies, snapshot
vs full replay, skew) are the meaningful part. Nightly CI re-runs these on
`ubuntu-latest` and uploads artifacts (`.github/workflows/sqrl-nightly.yml`).

## Micro-benchmarks (criterion)

```bash
cargo bench -p sqrl-benches
```

_(results table maintained per release; see nightly artifacts for the
latest run — recorded numbers for the current commit below)_

<!-- BENCH:MICRO -->

## Workloads (bench-harness)

Each command prints one JSON report (throughput, p50/p99/p999 latency, RSS,
fsyncs, write amplification). All were run in `--release`.

```bash
cargo build --release -p sqrl-bench-harness
H=./target/release/sqrl-bench-harness

$H w1 --workflows 5000 --steps 5             # start-locally (DBOS-shaped)
$H w1 --workflows 5000 --steps 5 --fsync strict
$H w2 --parents 100 --children 10            # saga fan-out
$H w3 --steps 1000000                        # 1M-step long-runner (no history cap)
$H w4 --workflows 1000                       # kill -9 with N in-flight, time-to-resumed
$H w5 --workflows 2000 --steps 5             # skew: uniform vs 90%-on-shard-0
cargo run --release -p sqrl-bench-harness --features sqrl/work-stealing -- w5 --workflows 2000 --steps 5
$H latency --samples 2000 --fsync group      # per-commit latency percentiles
$H latency --samples 2000 --fsync strict
$H mem --workflows 10000                     # memory per passivated workflow
```

<!-- BENCH:WORKLOADS -->

## Comparison targets

The W1-shaped comparison scripts live in `bench-harness/comparisons/`
(`dbos_sqlite.sh`, `temporal_dev.sh`, `restate.sh`), each using the target
project's own tooling.

**UNVERIFIED in this environment**: the development sandbox has no npm
registry access for `@dbos-inc/dbos-sdk` / Temporal / Restate toolchains
and no docker. A human can run each script directly on a networked machine;
they print `<system> workflows/s <value>` for the same N×M workload as
`w1`. Results belong in this section when produced.

## Profiling findings & optimization rounds

<!-- BENCH:PROFILING -->

## Write amplification

Reported by every harness run (`write_amp_bytes_per_step`,
`fsyncs_per_step`). Structural expectations: ~2 records per step
(`StepScheduled` + `StepCompleted`), ~10 B envelope + ~90–130 B named-mode
MessagePack per record, plus amortized snapshot bytes (factor ≈ 5× over a
workflow's lifetime at the default cadence — ADR 0006).
