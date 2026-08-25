# Changelog

All notable changes to this project will be documented in this file.
Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/);
versioning: SemVer (crate API) + `SQRL_FORMAT_VERSION` (on-disk format,
see `docs/on-disk-format.md`).

## [Unreleased]

### Added
- **Core durable loop** (`sqrl-core`): sans-executor `EngineCore` with
  journaled steps, durable timers, signals, retries (deterministic jittered
  backoff), snapshots (meta/body split, amortized cadence, lazy recovery),
  passivation, backpressure, group commit, typed `NonDeterminismError` with
  `ctx.patched()` migration gates, exhaustive lifecycle state machine.
- **Embedded WAL** (`sqrl-store`): checksummed record envelope
  (`SQRL_FORMAT_VERSION` 1), segmented log with atomic manifest,
  truncate-on-corruption recovery, durable-snapshot-gated GC, `StdVfs` and
  `MemoryStorage`; runs identically on the simulator disk.
- **Deterministic simulation** (`sqrl-sim`): seeded virtual-time executor,
  fault-injecting `SimDisk` (crash/torn write/bit rot/disk-full/latency),
  `SimScheduler` driving the production engine byte-identically per seed.
- **Facade** (`sqrl`): builder, thread-per-core `RealScheduler` with Tokio
  step pool, async + blocking APIs, `work-stealing` placement feature.
- **Macros** (`sqrl-macros`): `#[sqrl::workflow]`, `#[sqrl::step]`.
- Examples: `checkout_saga`, `crash_me` (live kill -9 demo),
  `ai_agent_loop`, `long_running_counter`.
- Acceptance tests: crash-at-every-disk-op sweep, real SIGKILL recovery,
  snapshot recovery <10% of full replay, non-determinism detection, WAL
  corruption resume; DST suite with multi-seed fault injection and
  physical-determinism assertions; fuzz targets (WAL decoder, manifest,
  replay).
- Workspace scaffold: crates `sqrl`, `sqrl-core`, `sqrl-sim`, `sqrl-store`,
  `sqrl-store-sqlite`, `sqrl-store-postgres`, `sqrl-macros`, `sqrl-cli`,
  benches, bench-harness, examples, tests.
