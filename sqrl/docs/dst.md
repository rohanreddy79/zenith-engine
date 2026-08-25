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

### The paranoid durability oracle (`SQRL_DST_PARANOID=1`)

On every newly observed completion acknowledgment, the harness forks the
disk's **durable-only** state (as if every unsynced byte and namespace op
were lost at that instant — the harshest legal crash), re-opens the store
from the fork, and requires the workflow's terminal evidence (a terminal
snapshot or `WorkflowCompleted` record) to be recoverable. This checks the
acknowledgment contract itself, not just end-state consistency, and is how
the torn-tail recovery data-loss bug was caught. It roughly doubles the
run's cost; the acceptance runs below have it enabled.

## Sometimes assertions (state-space coverage)

Counters that must be nonzero across the run — otherwise the adversary
stopped exploring: crashes, crash-during-recovery, step retries, caught
step panics, timer fires, snapshots, signal deliveries, cancellations,
parallel joins, injected write errors. The suite prints the full coverage
report; the acceptance numbers for the current commit are recorded below.

## Running it

```bash
# CI version (48 seeds, determinism cross-checked on a sample), ~1.5 s:
SQRL_DST_PARANOID=1 cargo test -p sqrl-tests --release dst_short -- --nocapture

# The long haul (10,000 seeds across all cores), ~90 s on 4 vCPUs:
SQRL_DST_PARANOID=1 cargo test -p sqrl-tests --release dst_long -- --ignored --nocapture
```

Reproduce any failure by its seed: every assertion message includes it, and
`SQRL_DST_START=<seed> SQRL_DST_END=<seed+1>` narrows `dst_short` to that
exact universe (`SQRL_DST_DEBUG=1` traces the adversary's ops).

## Recorded results

`dst_long`, 10,000 seeds, paranoid oracle enabled — run on the acceptance
environment (4-vCPU Xeon, see `docs/benchmarks.md`), 89 s wall:

```
DST coverage over 10000 seeds:
  crashes=171185 (mid-replay=70729)
  retries=31366 panics_caught=68349 timers_fired=59382
  snapshots=97392 passivations=1324 reactivations=2190
  signals=70773 cancels=88234 joins=79665
  injected_write_errors=80390 corruption_truncations=11141
  corruption_regressions=32669 backpressure=0
```

Every seed passed physical determinism, safety, liveness, and the paranoid
ack-durability oracle. (`backpressure=0`: the adversary's per-shard load
stays under the default in-flight cap; backpressure is covered by a
dedicated acceptance test instead.)

## Bugs this suite has caught (kept as regression evidence)

* **Torn-tail recovery data loss** (seed 3): recovery adopted a torn tail
  record's bytes as the append offset; the garbage later read as
  corruption and truncated away durably-acknowledged history behind it.
  Fixed in `WalShard::open`; pinned by
  `torn_tail_is_cut_at_open_so_later_appends_stay_recoverable`.
* **fsync-on-recovery gap** (seed 3, earlier): recovery trusted page-cache
  reads of a previous process's unfsynced writes and acknowledged on top of
  them. Fixed by fsyncing all live segments + directory at open.
* **Simulator truncate infidelity** (seed 3): `SimDisk` truncates never
  shrank files, so recovery cuts silently didn't stick — masking and then
  revealing the above once fixed.
* **Recovery livelock** (sweep): a poisoned engine kept reporting a stale
  group-commit deadline, spinning its driver forever. Fixed by
  `tick_poisoned()` + `next_wake` guard.
