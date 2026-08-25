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
