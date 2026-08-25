# 0001 — Sans-executor engine core; thread-per-core real scheduler

## Context
The engine must run byte-identically under a seeded simulator (DST is a
first-class feature) and fast in production. Work-stealing runtimes
introduce cross-thread nondeterminism at every poll; retrofitting
determinism onto a Tokio-first engine is the known failure mode this
project's brief explicitly forbids.

## Decision
`EngineCore` is a passive state machine: no threads, no wall clock, no
entropy, no I/O beyond an exclusively-owned `StorageShard`. Drivers feed it
`EngineCmd`s, call `tick()`, execute emitted step futures, and feed results
back. Production driver: **thread-per-core, shared-nothing** — one engine
core + one storage shard per OS thread, workflows placed by
`fnv1a64(id) % shards`, no orchestration work stealing. Steps (the only
possibly-blocking work) run on a dedicated Tokio multi-thread pool. A
`work-stealing` cargo feature may swap step-dispatch strategy (Phase 2
benchmarks skewed load); orchestration remains thread-per-core.

## Consequences
+ One `SimScheduler` drives the identical engine deterministically; DST
  covers the real logic, not a test double.
+ No cross-core locks on the hot path; per-core WAL preserves per-workflow
  ordering by construction.
− A hot workflow cannot exceed one core (accepted: orchestration is cheap;
  steps parallelize on the pool).
− Skewed workloads can imbalance cores — measured in Phase 2 (W5) and
  recorded here.

## Addendum (Phase 2): the W5 skew measurement

Measured on the acceptance environment (`docs/benchmarks.md`), 2000
5-step workflows, 4 shards, 90% of ids forced onto shard 0:

* **Hash placement**: slowdown ×1.04 vs uniform (7.7 k wf/s), shard
  completions 1850/50/50/50. The imbalance is real but mild — steps (the
  expensive part) run on the shared Tokio pool either way; only replay and
  journaling are pinned.
* **`work-stealing` feature** (least-loaded placement of new workflows):
  slowdown ×0.94 (9.0 k wf/s), shard completions 500/500/500/500 — the
  skew disappears at admission time.

Verdict: the default stays `fnv1a64(id) % shards` — deterministic
placement is what makes `sqrl replay`/offline tools able to find a
workflow's shard from its id alone, and the measured cost is ~4% under an
extreme 90% skew. Deployments with pathological id distributions can opt
into `work-stealing`, trading stable id→shard mapping (the placement map
is rebuilt from shard contents at startup) for even load.
