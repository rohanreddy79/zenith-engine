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

Recorded (current commit, environment above; criterion means):

| Benchmark | Time | Rate |
|---|---:|---:|
| `wal-codec/encode-64B` | 372 ns | ~2.7 M records/s |
| `wal-codec/decode-64B` | 784 ns | ~1.3 M records/s |
| `wal-codec/encode-1024B` | 3.57 µs | ~290 MB/s payload |
| `wal-codec/decode-1024B` | 7.67 µs | ~135 MB/s payload |
| `wal-append/1×64B, no sync` | 1.80 µs | — |
| `wal-append/1×64B + fsync` | 203 µs | fsync-bound (virtio) |
| `wal-append/256×64B, no sync` | 340 µs | ~750 k records/s |
| `wal-append/256×64B + fsync` | 892 µs | ~290 k records/s |
| `wal-append/256×1KiB, no sync` | 3.34 ms | ~77 k records/s |
| `wal-append/256×1KiB + fsync` | 6.45 ms | ~40 k records/s |
| `replay-read/10k records` | 8.47 ms | ~1.18 M records/s |
| `replay-read/100k records` | 87.9 ms | ~1.14 M records/s |
| `snapshot/build 10k outcomes` | 4.14 ms | ~2.4 M outcomes/s |
| `snapshot/decode 10k outcomes` | 7.61 ms | ~1.3 M outcomes/s |
| `snapshot/build 100k outcomes` | 55.8 ms | ~1.8 M outcomes/s |
| `snapshot/decode 100k outcomes` | 82.7 ms | ~1.2 M outcomes/s |

The single-record fsync cost (~200 µs on this virtio disk; local NVMe is
typically 20–80 µs, battery-backed controllers less) is the floor Strict
mode pays per step; group commit amortizes it across a batch — visible in
`256×64B + fsync` at ~3.5 µs/record.

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

Recorded (current commit, environment above):

| Workload | Result | Notes |
|---|---|---|
| **W1** 5000×5 steps, Group | **~8.2 k workflows/s** (25 k–41 k steps/s; run-to-run ±10%) | write amp 263 B/step, 0.05 fsyncs/step |
| **W1** same, Strict | **~3.4 k workflows/s** | 0.52 fsyncs/step — fsync-bound, as designed |
| **W2** saga fan-out 100×10 | 10.5 k workflows/s | 1100 workflows, 13.5 k records, 194 fsyncs |
| **W3** 1 M steps, one workflow | 10.1 k steps/s sustained, RSS 234 MiB | validates *no history cap*; write amp 411 B/step incl. snapshots |
| **W4** kill -9 with 1000 in-flight | **time-to-resumed 26 ms** | all 1000 redispatched after recovery |
| **W5** 90% skew, hash placement | 7.7 k workflows/s, slowdown ×1.04 | steps run on the shared pool, so orchestration skew barely bites |
| **W5** 90% skew, `work-stealing` | 9.0 k workflows/s, perfectly even shards | least-loaded placement flattens 1850/50/50/50 → 500/500/500/500 |
| **latency** sequential, Group | p50 2.8 ms, p99 3.4 ms | dominated by the 2 ms group window — see below |
| **latency** sequential, Strict | **p50 0.71 ms, p99 1.2 ms** | one fsync on the critical path beats waiting for a batch |
| **mem** 10 k idle workflows | 1.7 KiB active / 1.9 KiB passivated per workflow | all 10 k passivated by the sweep |

Two honest surprises worth calling out:

* **Group commit hurts *sequential* latency.** A lone workflow's commit
  waits out the 2 ms `max_delay` window (p50 2.8 ms) while Strict fsyncs
  immediately (p50 0.7 ms). Group commit wins when commits queue up behind
  each other (W1: 2.7× the Strict throughput at 1/10th the fsyncs); for
  latency-sensitive low-concurrency work, configure `FsyncPolicy::Strict`
  or a smaller `max_delay`.
* **Hash-placement skew is mild here** (×1.04) because steps execute on the
  shared Tokio pool; only orchestration (replay, journaling) is pinned.
  The `work-stealing` feature still removes it entirely — see the ADR 0001
  addendum.

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

### Round 1: append-path allocations (this commit)

No `perf` in the dev sandbox, so this round is code-inspection + criterion
A/B (hypothesis, change, measured delta) rather than sampled profiles.

**Finding.** Every appended record paid: a full `JournalRecord` clone
(payload `Vec` included) to build the owned `WalEntry`, an intermediate
MessagePack payload `Vec`, a copy of that payload into the envelope `Vec`,
and a copy of the envelope into the batch buffer — three allocations and
three copies per record on the hottest write path.

**Change.** `codec::encode_entry_into` / `encode_snapshot_into` serialize
*borrowed* mirror structs (identical field names → byte-identical output,
pinned by `borrowed_encoders_are_byte_identical_to_owned`) directly into
the destination buffer, patching `len`/`crc32c` in place; `WalShard::append`
now encodes straight into its batch. Zero clones, zero intermediate
buffers, on-disk bytes unchanged.

**Measured** (criterion, same session, before → after):

| Benchmark | Before | After | Δ |
|---|---:|---:|---:|
| `encode-64B` | 709 ns | 388 ns | **−46%** |
| `encode-1024B` | 6.19 µs | 3.70 µs | **−41%** |
| `append-1×64B-nosync` | 3.63 µs | 2.73 µs | −24% |
| `append-1×64B-fsync` | 239 µs | 202 µs | −19% |
| `append-256×1KiB-nosync` | 6.85 ms | 4.62 ms | −36% |
| W1 Strict end-to-end | 3.06 k wf/s | 3.2–3.6 k wf/s | ~+10% |
| W1 Group end-to-end | 7.6 k wf/s | 7.9–8.5 k wf/s | within ±10% noise |

Decode paths were untouched; their ±4–16% criterion deltas across runs are
code-layout/VM noise (the recorded table uses the final run). End-to-end
W1 under group commit is fsync/scheduling-bound, so the micro win mostly
disappears there — reported as such rather than claimed.

## Write amplification

Reported by every harness run (`write_amp_bytes_per_step`,
`fsyncs_per_step`). Structural expectations: ~2 records per step
(`StepScheduled` + `StepCompleted`), ~10 B envelope + ~90–130 B named-mode
MessagePack per record, plus amortized snapshot bytes (factor ≈ 5× over a
workflow's lifetime at the default cadence — ADR 0006).
