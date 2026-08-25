# sqrl — Project Plan & Progress Tracker

> Source of truth for progress. Check items off as they land; every checked item
> has passing tests behind it. UNVERIFIED items (things that could not be run in
> this environment) are listed at the top once they exist.

## UNVERIFIED items

_(populated as encountered; each entry links to the doc section with exact
reproduction instructions for a human)_

---

## Phase 0 — Working method

- [x] `docs/PLAN.md` created (this file)
- [x] Workspace scaffolded (all crates, examples, benches, tests compile as stubs)
- [x] Licenses (MIT + Apache-2.0), `rust-toolchain.toml` (pinned stable), `.gitignore`
- [x] CI workflow (`.github/workflows/ci.yml` at repo root, workspace under `sqrl/`)
- [x] Clippy `disallowed-methods` config enforcing injected time/entropy
- [ ] Decision log complete (`docs/adr/`): thread-per-core vs work-stealing, WAL
      format, fsync policy, serialization format, at-least-once semantics,
      snapshot strategy, versioning API

## Phase 1 — MVP: the core durable loop

Ordering constraint honored: **simulator before executor**.

### 1.1 sqrl-sim (deterministic substrate — built FIRST)
- [ ] `SimRng`: seeded, splittable deterministic RNG
- [ ] `SimClock`: virtual time, manual/auto advance
- [ ] `SimScheduler`: seeded single-threaded executor, virtual time, deterministic
      task ordering; implements the `Scheduler` trait from `sqrl-core`
- [ ] `SimDisk`: in-memory VFS implementing `sqrl-core::vfs::Vfs` with fault
      injection: crash (lose unsynced writes), torn write, bit flip/corruption,
      disk-full, slow I/O
- [ ] Test: two runs with the same seed produce byte-identical traces
- [ ] Test: crash semantics — unsynced writes may vanish; synced writes never do

### 1.2 sqrl-core (engine)
- [ ] Journal event types (all listed in §2.1) with versioned serialization
- [ ] `Clock` / `Rng` / `Scheduler` / `vfs::Vfs` traits (injection points)
- [ ] Lifecycle state machine, exhaustive match, typed `IllegalTransition` error
- [ ] `Ctx`: `step`, `step_with`, `sleep`, `sleep_until`, `await_signal`, `now`,
      `random`, `uuid`, `idempotency_key`, `patched`
- [ ] Replay engine: journal cursor, command/event matching, snapshot-aware
- [ ] `NonDeterminismError` (typed, expected-vs-actual) → `Failed(NonDeterministic)`,
      never a retry loop
- [ ] `RetryPolicy`: exponential backoff + deterministic jitter; max attempts → Failed
- [ ] Panic in step → caught (`catch_unwind` at step-pool boundary) → `StepFailed`
- [ ] Panic in orchestration → `WorkflowError::OrchestrationPanic`
- [ ] Durable timers on logical time
- [ ] Signals: buffered, journaled, durable across restart
- [ ] Snapshot state (command-result table) + compaction trigger every K events
- [ ] Payload size limit (default 1 MiB) with clear error
- [ ] Unit tests for every module

### 1.3 sqrl-store
- [ ] `Storage` trait (append batch, read journal, snapshots, sync, list)
- [ ] `MemoryStorage` (tests)
- [ ] WAL record codec: `[len u32][crc32c u32][type u8][fmt_version u8][payload]`
- [ ] Segmented log (roll at configurable size, default 64 MiB)
- [ ] `MANIFEST` (atomic rewrite: tmp + fsync + rename + dir fsync), checksummed
- [ ] Group commit: `FsyncPolicy::{Strict, Group{max_delay,max_batch}, Relaxed{interval}}`,
      per-step override
- [ ] Snapshots + segment GC once all workflows have newer snapshots
- [ ] Recovery: truncate at first invalid record, log byte offset, fall back to
      snapshot
- [ ] Disk-full / write error → `StorageError::Disk`, halt commits, backpressure
- [ ] Runs on both `StdVfs` (real files) and `SimDisk`

### 1.4 sqrl-macros
- [ ] `#[workflow(name, version)]` proc macro
- [ ] `#[step]` helper macro
- [ ] Expansion/unit tests for the macros

### 1.5 RealScheduler (only after engine green on SimScheduler)
- [ ] Thread-per-core executor: N threads, per-core run queue, per-core WAL segment,
      `hash(workflow_id) % N` sharding
- [ ] Step pool (Tokio multi-thread, steps only) behind a clear boundary
- [ ] Bounded in-flight workflows per core + `Rejected::Backpressure`
- [ ] Passivation: LRU idle eviction, reload from snapshot+journal

### 1.6 Examples
- [ ] `examples/checkout_saga`
- [ ] `examples/crash_me` (kill -9 recovery demo)

### Phase 1 acceptance gate
- [ ] crash-at-every-boundary test (SimDisk + real subprocess kill -9)
- [ ] Durable sleep survives restart (sim virtual time + real 2s sleep w/ kill)
- [ ] Signal wakes durably blocked workflow after restart
- [ ] Snapshot compaction: 100k-event workflow replays from snapshot in <10% of
      full-replay time (measured, printed)
- [ ] Non-determinism detection test (changed step order → typed error, no loop)
- [ ] WAL corruption test (random byte flips → truncate + resume)
- [ ] `cargo test --workspace`, `clippy -D warnings`, `fmt --check`,
      `cargo doc --no-deps` all green
- [ ] `docs/architecture.md`, `docs/on-disk-format.md`, `docs/determinism-guide.md`
- [ ] ADRs for all §0.8 decisions

## Phase 2 — Benchmarking & profiling

- [ ] Criterion benches: step-commit latency (p50/p99/p999) per FsyncPolicy; WAL
      append throughput; replay throughput; snapshot write/restore; memory per
      passivated workflow
- [ ] bench-harness workloads: W1 start-locally, W2 saga fan-out, W3 long-runner
      (1M steps), W4 recovery, W5 skew (thread-per-core vs work-stealing)
- [ ] `work-stealing` cargo feature + skew comparison
- [ ] Comparison targets: DBOS Transact (SQLite mode), Temporal dev server,
      Restate single-node — run what's installable, otherwise UNVERIFIED + exact
      scripts
- [ ] Profiling round: flamegraph, allocation profile, fsync counts; findings +
      driven optimizations in `docs/benchmarks.md`
- [ ] Metrics per run: workflows/s, steps/s, p50/p99/p999, RSS, CPU, write
      amplification (bytes/step), fsyncs/step, recovery time
- [ ] `docs/benchmarks.md` with hardware/OS/kernel/disk/commit + exact commands
- [ ] ≥1 optimization round with before/after numbers
- [ ] Skew result recorded in thread-per-core ADR
- [ ] Nightly benchmark CI job (artifacts, non-gating)

## Phase 3 — Robustness & ergonomics

- [ ] DST suite (`tests/`): thousands of seeds, fault injection; asserts physical
      determinism (same seed ⇒ byte-identical journal), safety (no acked step
      lost, no double completion, no illegal transition), liveness (terminates
      when faults stop); sometimes-assertions + coverage report; 30s CI version
      + long `--ignored` version; `docs/dst.md`
- [ ] proptest: journal codec round-trip, replay idempotence, snapshot-equivalence
- [ ] cargo-fuzz targets: WAL record decoder, manifest parser, replay engine
      (10 min local each; 5 min scheduled CI job) — or UNVERIFIED if nightly
      toolchain unavailable
- [ ] `sqrl-store-sqlite` (real, tested)
- [ ] `sqrl-store-postgres` (tested if docker Postgres available, else UNVERIFIED)
- [ ] Versioning & patching: `ctx.patched("id")`, workflow `version`,
      `sqrl replay --against`, `docs/versioning-and-patching.md`
- [ ] CLI: `status`, `inspect`, `replay`, `fork`, `resume`, `cancel`, `signal`,
      `compact`, `bench` — all with integration tests
- [ ] Observability: tracing spans; optional `opentelemetry` feature
- [ ] Examples: `ai_agent_loop`, `long_running_counter`
- [ ] README rewrite (10-line quickstart, guarantees, comparison link);
      `docs/comparison.md` (honest, includes where sqrl loses)
- [ ] Release engineering: cargo-release config, SemVer policy, on-disk format
      version policy, CHANGELOG, `cargo publish --dry-run` green, MSRV in CI

### Phase 3 acceptance gate ("0.1.0 ready")
- [ ] DST ≥10,000 seeds with fault injection; coverage report in docs/dst.md
- [ ] Fuzz targets zero crashes
- [ ] Line coverage ≥85% on sqrl-core and sqrl-store (cargo llvm-cov), in CI
- [ ] All CLI commands integration-tested
- [ ] All examples build & run in CI
- [ ] `cargo publish --dry-run` green for all publishable crates
- [ ] PLAN.md fully checked, UNVERIFIED list at top

## Final deliverable

- [ ] `docs/FINAL_REPORT.md`: what was built, every acceptance criterion with
      pass/fail + evidence, UNVERIFIED items + human verification steps, known
      limitations, prioritized next steps
