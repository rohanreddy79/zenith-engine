# sqrl — Project Plan & Progress Tracker

> Source of truth for progress. Check items off as they land; every checked item
> has passing tests behind it. UNVERIFIED items (things that could not be run in
> this environment) are listed at the top once they exist.

## UNVERIFIED items

1. **Comparison benchmarks (DBOS / Temporal / Restate)** — the sandbox has
   no npm registry access or docker. Exact scripts:
   `bench-harness/comparisons/*.sh`; see docs/benchmarks.md §Comparison.
2. **macOS CI legs** — CI matrix includes macOS, but this environment is
   Linux-only; the jobs run on GitHub Actions.
3. **PostgreSQL storage backend** — fully implemented
   (`sqrl-store-postgres`, same contract mapping as the SQLite backend) but
   no Postgres server/docker here: its integration tests are gated on
   `SQRL_POSTGRES_URL` and were not executed. Verify:
   `docker run --rm -e POSTGRES_PASSWORD=pw -p 5432:5432 postgres:16` then
   `SQRL_POSTGRES_URL=postgres://postgres:pw@localhost:5432/postgres cargo test -p sqrl-store-postgres`.
4. **CI itself** — workflow files are written but this repository's Actions
   runs happen on push; not observable from the sandbox.
5. **otel runtime export** — the `otel` feature compiles clean (build +
   clippy) but was never pointed at a live OTLP collector. Verify with any
   collector and `sqrl::otel::init`.
6. **Full crates.io publish chain** — `cargo package --workspace` verifies
   all 15 tarballs against a local overlay registry, and `sqrl-core` /
   `sqrl-macros` pass a real `cargo publish --dry-run`; crates depending on
   them can only resolve after those are actually published (normal
   first-release ordering).

(MSRV 1.85 was verified locally with `cargo +1.85 check` for the default
features, `work-stealing`, and the Postgres backend; the `otel` feature
needs rustc 1.88 — see README §Toolchain.)

---

## Phase 0 — Working method

- [x] `docs/PLAN.md` created (this file)
- [x] Workspace scaffolded (all crates, examples, benches, tests compile as stubs)
- [x] Licenses (MIT + Apache-2.0), `rust-toolchain.toml` (pinned stable), `.gitignore`
- [x] CI workflow (`.github/workflows/ci.yml` at repo root, workspace under `sqrl/`)
- [x] Clippy `disallowed-methods` config enforcing injected time/entropy
- [x] Decision log complete (`docs/adr/0001`–`0007`): thread-per-core vs
      work-stealing, WAL format, fsync policy, serialization format,
      at-least-once semantics, snapshot strategy, versioning API
      (skew-benchmark addendum to 0001 lands in Phase 2)

## Phase 1 — MVP: the core durable loop

Ordering constraint honored: **simulator before executor**.

### 1.1 sqrl-sim (deterministic substrate — built FIRST)
- [x] `SimRng`: seeded, forkable deterministic RNG (SplitMix64)
- [x] `SimClock`: virtual time, manual/auto advance
- [x] `SimScheduler`: seeded single-threaded driver over EngineCore shards +
      `SimExecutor` (seeded task ordering, virtual time)
- [x] `SimDisk`: in-memory VFS implementing `sqrl-core::vfs::Vfs` with fault
      injection: crash (lose/tear unsynced writes, resurrect deletes, atomic
      renames), bit flip, disk-full, injected I/O errors, virtual latency
- [x] Test: two runs with the same seed produce byte-identical traces
- [x] Test: crash semantics — unsynced writes may vanish; synced writes never do

### 1.2 sqrl-core (engine)
- [x] Journal event types (all listed in §2.1) with versioned serialization
- [x] `Clock` / `Entropy` / `Scheduler` / `vfs::Vfs` traits (injection points)
- [x] Lifecycle state machine, exhaustive match, typed `IllegalTransition` error
- [x] `Ctx`: `step`, `step_with`, `sleep`, `sleep_until`, `await_signal`, `now`,
      `random`, `random_f64`, `uuid`, `idempotency_key`, `patched`
- [x] Replay engine: ordered revelation queue, command/event matching,
      snapshot-aware, lazy recovery from quiescence snapshots
- [x] `NonDeterminismError` (typed, expected-vs-actual) → `Failed(NonDeterministic)`,
      never a retry loop
- [x] `RetryPolicy`: exponential backoff + deterministic jitter; max attempts → Failed
- [x] Panic in step → caught (`catch_unwind` at step boundary) → `StepFailed`
- [x] Panic in orchestration → `Error::OrchestrationPanic`
- [x] Durable timers on logical time
- [x] Signals: buffered, journaled, durable across restart
- [x] Snapshot meta/body split + amortized compaction cadence + shutdown &
      passivation quiescence snapshots
- [x] Payload size limit (default 1 MiB) with clear error
- [x] Unit tests for every module (+16 engine end-to-end tests)

### 1.3 sqrl-store
- [x] `Storage`/`StorageShard` traits (append batch, sync barrier, read, list,
      maintain, stats)
- [x] `MemoryStorage` (tests)
- [x] WAL record codec: `[len u32][crc32c u32][type u8][fmt_version u8][payload]`
- [x] Segmented log (roll at configurable size, default 64 MiB)
- [x] `MANIFEST` (atomic rewrite: tmp + fsync + rename + dir fsync), checksummed,
      degrades to directory scan when missing/corrupt
- [x] Group commit: `FsyncPolicy::{Strict, Group{max_delay,max_batch}, Relaxed{interval}}`,
      per-step override (`StepOptions::fsync_strict`)
- [x] Snapshots + segment GC (durable-snapshot gated)
- [x] Recovery: truncate at first invalid record, log byte offset, fall back to
      snapshot
- [x] Disk-full / write error → `StorageError::{Disk,DiskFull}`, poison shard,
      backpressure
- [x] Runs on both `StdVfs` (real files) and `SimDisk` (120-point crash sweep)

### 1.4 sqrl-macros
- [x] `#[workflow(name, version)]` proc macro
- [x] `#[step]` helper macro (validation marker)
- [x] Expansion/unit tests for the macros (19) + facade integration test

### 1.5 RealScheduler (only after engine green on SimScheduler)
- [x] Thread-per-core executor: N threads, per-core engine + storage shard,
      `fnv1a64(workflow_id) % N` sharding
- [x] Step pool (Tokio multi-thread, steps only) behind a clear boundary
- [x] Bounded in-flight workflows per core + `Rejected::Backpressure`
- [x] Passivation: idle eviction with quiescence snapshot, reload on demand

### 1.6 Examples
- [x] `examples/checkout_saga`
- [x] `examples/crash_me` (kill -9 recovery demo)

### Phase 1 acceptance gate
- [x] crash-at-every-boundary test (SimDisk sweep over every disk op + real
      subprocess kill -9 tests)
- [x] Durable sleep survives restart (sim virtual time + real 2s sleep w/ SIGKILL)
- [x] Signal wakes durably blocked workflow after restart (sim + real)
- [x] Snapshot compaction: 100k-event workflow recovers from snapshot in 4.6%
      of full-replay time (6.95ms vs 150.3ms, printed by the test)
- [x] Non-determinism detection test (changed step name → typed error, no loop,
      heals on rollback)
- [x] WAL corruption test (byte flips → truncate at offset + resume + complete)
- [x] `cargo test --workspace`, `clippy -D warnings`, `fmt --check`,
      `cargo doc --no-deps` all green
- [x] `docs/architecture.md`, `docs/on-disk-format.md`, `docs/determinism-guide.md`
- [x] ADRs for all §0.8 decisions (0001–0007)

## Phase 2 — Benchmarking & profiling

- [x] Criterion benches written (`benches/benches/micro.rs`: codec, append±fsync,
      replay read, snapshot build/decode); latency percentiles + memory-per-
      passivated-workflow live in bench-harness (`latency`, `mem`) — numbers
      recorded in docs/benchmarks.md as runs complete
- [x] bench-harness workloads implemented: W1 start-locally, W2 saga fan-out
      (signal-based, deadlock-free), W3 long-runner, W4 kill -9 recovery,
      W5 skew, + latency, + mem
- [x] `work-stealing` cargo feature (least-loaded placement, startup-rebuilt
      routing map); skew comparison recorded with W5 results
- [x] Comparison scripts written (`bench-harness/comparisons/`): DBOS SQLite,
      Temporal dev, Restate — UNVERIFIED here (no npm/docker in sandbox);
      exact scripts provided, see docs/benchmarks.md
- [x] Profiling round (no `perf` in sandbox: code-inspection hypothesis +
      criterion A/B): append-path allocations; findings + measured deltas in
      `docs/benchmarks.md`
- [x] Metrics per run: workflows/s, steps/s, p50/p99/p999, RSS, write
      amplification (bytes/step), fsyncs/step, recovery time — all in the
      harness JSON and recorded in docs/benchmarks.md
- [x] `docs/benchmarks.md` with hardware/OS/kernel/disk + exact commands
- [x] ≥1 optimization round with before/after numbers (encode −46%,
      append −19…36%, W1 Strict ~+10%)
- [x] Skew result recorded in thread-per-core ADR (0001 addendum)
- [x] Nightly benchmark CI job (`.github/workflows/sqrl-nightly.yml`,
      artifacts, non-gating) + scheduled 5-min fuzz job

## Phase 3 — Robustness & ergonomics

- [x] DST suite (`tests/`): 10,000 seeds, fault injection; asserts physical
      determinism (same seed ⇒ byte-identical durable image), safety (durably
      acked completions never regress — incl. a paranoid durable-only-fork
      oracle at every ack, `SQRL_DST_PARANOID`), liveness (client-retry drain
      converges); sometimes-assertions + coverage report; ~1.5s CI version +
      `--ignored` 10k version (89 s); `docs/dst.md` (found and pinned two
      real storage bugs: fsync-on-recovery, torn-tail truncation)
- [x] proptest: journal codec round-trip + single-byte-flip detection, replay
      idempotence (incl. journal-untouched-by-replay), snapshot-equivalence
- [x] cargo-fuzz targets: WAL record decoder, manifest parser, replay engine —
      smoke-run clean (60s each: 6.0M/2.2M/56K execs, zero crashes); longer
      runs + 5-min scheduled CI job configured
- [x] `sqrl-store-sqlite` (real, tested: 9 integration tests)
- [x] `sqrl-store-postgres` implemented; UNVERIFIED (no docker/Postgres —
      tests gated on `SQRL_POSTGRES_URL`)
- [x] Versioning & patching: `ctx.patched("id")`, workflow `version`,
      `sqrl_core::engine::validate_history` + `sqrl::replay_check` (pre-deploy
      CI check), CLI structural `replay`, `docs/versioning-and-patching.md`
- [x] CLI: `status`, `inspect`, `replay`, `fork`, `resume`, `cancel`, `signal`,
      `compact`, `bench` — with integration tests (10)
- [x] Observability: tracing spans throughout; optional `otel` feature
      (OTLP traces + metrics; compiles clean, runtime export UNVERIFIED)
- [x] Examples: `ai_agent_loop`, `long_running_counter`
- [x] README rewrite (quickstart, guarantees, comparison link);
      `docs/comparison.md` (honest, includes where sqrl loses)
- [x] Release engineering: cargo-release config, SemVer policy, on-disk format
      version policy, CHANGELOG, packaging verified (see UNVERIFIED #6 for
      the publish-chain caveat), MSRV verified locally + in CI

### Phase 3 acceptance gate ("0.1.0 ready")
- [x] DST ≥10,000 seeds with fault injection; coverage report in docs/dst.md
- [x] Fuzz targets zero crashes (3 targets, 60s smoke: 6.0M/2.2M/56K execs)
- [x] Coverage ≥85% on sqrl-core and sqrl-store (cargo llvm-cov over the
      release acceptance suite): 86.14% regions / 85.39% functions /
      85.02% lines
- [x] All CLI commands integration-tested
- [x] All examples build (workspace members; run in CI)
- [x] Publish packaging verified for all crates; full dry-run green for the
      dependency roots (see UNVERIFIED #6)
- [x] PLAN.md fully checked, UNVERIFIED list at top

## Final deliverable

- [x] `docs/FINAL_REPORT.md`: what was built, every acceptance criterion with
      pass/fail + evidence, UNVERIFIED items + human verification steps, known
      limitations, prioritized next steps
