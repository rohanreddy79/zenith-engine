# Deterministic Simulation Testing (DST)

DST is a first-class feature of sqrl, not a test-suite afterthought: the
entire production engine — `EngineCore`, `WalStorage`, group commit,
snapshots, passivation, recovery — runs unmodified on a seeded,
single-threaded simulated substrate (`sqrl-sim`), where a whole multi-crash
history is a pure function of `(seed, workload)`.

## The substrate

| Real | Simulated | Determinism source |
|---|---|---|
| OS threads + Tokio steps | `SimExecutor` | seeded choice among ready tasks |
| Wall clock | `SimClock` | virtual time, advances only on demand |
| OS entropy | `DeterministicRng` | SplitMix64, forkable streams |
| Disk (`StdVfs`) | `SimDisk` | seeded fault resolution |

`SimDisk` models durability *worse* than any real filesystem: unsynced data
writes are independently kept, dropped, or torn on crash; unsynced
creates/renames/deletes are independently kept or dropped (renames stay
atomic, deletes can resurrect their file); fsync of a file persists content
but not its name (that needs the directory fsync). Storage code that
survives this model on thousands of seeds is correct on ext4/xfs/apfs.

## The suite (`tests/tests/dst.rs`)

A seeded adversary drives a zoo of six workflow shapes (sequential steps,
flaky steps that fail their first attempt, panicking steps, timer-heavy
sleepers, signal waiters, parallel joins) with a random program of: starts,
signal deliveries, virtual-time advances, **process crashes** (drop engines,
resolve unsynced writes by seed, restart over the surviving bytes), injected
write/fsync error windows, cancellations — and, in dedicated corruption
seeds, byte flips in durable segment files.

Assertions per seed:

* **Physical determinism** — the same seed is re-run and must produce a
  byte-identical durable disk image, identical final workflow states,
  identical completion outputs, and identical final virtual time.
* **Safety** — a workflow observed `Completed` never regresses across later
  crashes; final outputs equal per-kind ground truth; the engine's
  illegal-transition counter stays zero.
* **Liveness** — after the fault program ends, owed signals are delivered
  and every started workflow reaches `Completed`/`Failed`/`Cancelled`.

Corruption seeds relax only the safety assertion that history suffixes
survive (bit rot legitimately truncates un-superseded records — that *is*
the contract) while still requiring no crashes, no hangs, and clean
truncation.

## Sometimes assertions (state-space coverage)

Counters that must be nonzero across the run — otherwise the adversary
stopped exploring: crashes, crash-during-recovery, step retries, caught
step panics, timer fires, snapshots, signal deliveries, cancellations,
parallel joins, injected write errors. The suite prints the full coverage
report; the acceptance numbers for the current commit are recorded below.

## Running it

```bash
# CI version (~48 seeds, determinism cross-checked on a sample), < 30 s:
cargo test -p sqrl-tests --release dst_short -- --nocapture

# The long haul (10,000 seeds across all cores):
cargo test -p sqrl-tests --release dst_long -- --ignored --nocapture
```

Reproduce any failure by its seed: every assertion message includes it, and
`run_seed(seed, ops)` replays that exact universe.

## Recorded results

_(updated per release; see `docs/FINAL_REPORT.md` for the acceptance run)_
