# sqrl — Final Report

**What this is.** `sqrl` is a deterministic-first, embedded, single-node
durable execution library for Rust — "the SQLite of durable execution".
Workflows are plain `async fn`s; every step result, timer, and signal is
journaled through a checksummed, segmented WAL; a crash at any instant
replays the journal and resumes without re-executing completed steps. The
same production engine runs unmodified under Deterministic Simulation
Testing, where an entire multi-crash history is a pure function of a seed.

Everything below was produced in this repository; every number has a
reproduction command. Anything that could not be executed in the
development sandbox is marked **UNVERIFIED** with the exact steps a human
needs (the same list is maintained at the top of `docs/PLAN.md`).

## What was built

| Crate | Contents |
|---|---|
| `sqrl-core` | Sans-executor engine: journal/replay state machine, `Ctx` (steps, durable timers, signals, replay-safe time/entropy, idempotency keys, `patched` gates), typed `NonDeterminismError`, retry with deterministic jitter, snapshots + lazy recovery, passivation, backpressure, `validate_history` |
| `sqrl-store` | Embedded WAL: `[len][crc32c][type][fmt_version][payload]` records, 64 MiB segments + MANIFEST, group commit (`Strict`/`Group`/`Relaxed` + per-step override), snapshot-gated GC, truncate-at-first-invalid recovery with fsync-on-recovery hardening; plus `MemoryStorage` |
| `sqrl-sim` | The deterministic substrate: seeded RNG/clock/executor and `SimDisk` (kept/dropped/torn unsynced writes, pending namespace ops, byte flips, disk-full, injected errors, latency) |
| `sqrl` | Facade: builder, thread-per-core `RealScheduler` (+ optional `work-stealing` placement), Tokio step pool, blocking + async API, `replay_check`, optional `otel` feature |
| `sqrl-macros` | `#[workflow]` (unit-struct witness + `::run`) and `#[step]`, with compiling doctests |
| `sqrl-store-sqlite` | Second backend: one SQLite file, WAL mode + `synchronous=FULL`, one transaction per sync barrier — tested |
| `sqrl-store-postgres` | Third backend, same contract on PostgreSQL (`synchronous_commit=on`) — implemented, **UNVERIFIED** (no server in sandbox) |
| `sqrl-cli` | `status`, `inspect`, `signal`, `cancel`, `resume`, `fork`, `compact`, `replay` (structural pre-deploy check), `bench` — offline surgeon over a stopped store, integration-tested |
| `tests/`, `benches/`, `bench-harness/`, `fuzz/`, `examples/` | DST + acceptance suites, criterion micro benches, workload harness (W1–W5, latency, mem), 3 fuzz targets, 4 runnable examples |
| `docs/` | architecture, on-disk format, determinism guide, versioning & patching, DST, benchmarks, honest comparison, 7 ADRs, this report |

## Acceptance criteria — pass/fail with evidence

Reproduction prefix for everything:
`cd sqrl && SQRL_DST_PARANOID=1 cargo test --workspace --release -- --include-ignored --skip dst_long`
(186 tests, 0 failures at time of writing).

### Phase 1 (core durable loop) — all PASS

| Criterion | Evidence |
|---|---|
| Crash at every boundary → effectively-once completion | `acceptance_sim.rs::crash_at_every_boundary_saga_completes_effectively_once` (SimDisk sweep over every disk op) + two real `kill -9` subprocess tests (`acceptance_real.rs`) — PASS |
| Durable sleep across restart | sim (virtual time) + real 2 s sleep with SIGKILL mid-sleep — PASS |
| Signal wakes blocked workflow after restart | sim + real — PASS |
| Snapshot recovery ≪ full replay | `acceptance_compaction.rs`: 100k-event workflow, snapshot recovery measured at 3.8–4.6% of full-replay time across runs (gate: <10%), printed by the test — PASS |
| Non-determinism → typed error, no retry loop, heals on rollback | `engine_loop.rs` ND tests + DST — PASS |
| WAL corruption → truncate at logged offset, resume | `wal_recovery.rs::corruption_truncates_and_reports_offset` + DST corruption seeds — PASS |
| Lints/docs | `cargo fmt --check`, `clippy --all-targets --all-features -D warnings` (0 warnings), `cargo doc --no-deps` clean (one known cargo bin/lib name-collision notice) — PASS |
| Docs + ADRs | `docs/architecture.md`, `on-disk-format.md`, `determinism-guide.md`; ADRs 0001–0007 — PASS |

### Phase 2 (benchmarks & profiling) — PASS except comparisons (UNVERIFIED)

All numbers with environment + commands in `docs/benchmarks.md`. Headlines
(4-vCPU virtualized Xeon, virtio disk — treat as order-of-magnitude):

* W1 (5000×5 steps): ~8.2 k workflows/s group commit, ~3.4 k strict.
* W3: 1 M steps in one workflow, 10.1 k steps/s sustained, no history cap.
* W4: kill -9 with 1000 in-flight steps → resumed in 26 ms.
* Latency: p50 0.71 ms Strict; group commit's 2 ms window dominates
  sequential latency (p50 2.8 ms) — documented as a finding, not hidden.
* Memory: ~1.9 KiB per passivated workflow.
* Profiling round: append-path allocation elimination, encode −46%,
  single-append fsync path −19%, byte-identical on-disk output (pinned by
  test). Before/after in `docs/benchmarks.md`.
* W5 skew + `work-stealing`: ADR 0001 addendum (×1.04 skew cost by
  default; work-stealing flattens it entirely).
* Nightly bench + fuzz CI: `.github/workflows/sqrl-nightly.yml`.
* **UNVERIFIED**: DBOS/Temporal/Restate comparison runs (no npm/docker in
  sandbox). Scripts: `bench-harness/comparisons/*.sh`.

### Phase 3 (robustness & ergonomics) — PASS except noted

| Criterion | Evidence |
|---|---|
| DST ≥10,000 seeds with fault injection | **PASS** — `dst_long`: 10,000 seeds, 89 s, paranoid ack-durability oracle enabled; coverage report in `docs/dst.md` (171 k crashes, 70 k mid-replay, 68 k caught panics, 11 k corruption truncations, all assertions green). Found two real storage bugs during development (fsync-on-recovery; torn-tail truncation) — both fixed and pinned by regression tests |
| Property tests | **PASS** — codec round-trip, single-byte-flip detection, replay idempotence, snapshot equivalence (`tests/tests/props.rs`) |
| Fuzz targets zero crashes | **PASS** (smoke) — 3 targets (WAL decoder, manifest parser, replay engine), 60 s each: 6.0 M / 2.2 M / 56 K execs, zero crashes; scheduled 5-min CI job for continuous fuzzing |
| SQLite backend real + tested | **PASS** — 9 integration tests |
| Postgres backend | implemented; **UNVERIFIED** (env-gated tests; docker one-liner in crate docs) |
| Versioning & patching | **PASS** — `ctx.patched`, workflow versions, `sqrl::replay_check`, `sqrl replay` CLI, `docs/versioning-and-patching.md` |
| CLI with tests | **PASS** — 9 commands, 10 integration tests |
| Observability | **PASS** (compile-verified) — tracing spans throughout; `otel` feature builds clean; runtime OTLP export **UNVERIFIED** (no collector) |
| Examples | **PASS** — checkout_saga, crash_me, long_running_counter, ai_agent_loop |
| README + honest comparison | **PASS** — `README.md`, `docs/comparison.md` (includes where sqrl loses) |
| Coverage ≥85% core+store | **PASS** — `cargo llvm-cov` over the release acceptance suite: 86.14% regions / 85.39% functions / 85.02% lines |
| Publish dry-run | **PASS with caveat** — `cargo package --workspace` verifies all 15 tarballs; `sqrl-core` and `sqrl-macros` pass full `cargo publish --dry-run`; dependent crates resolve only after those publish (normal first-release ordering) |
| MSRV | **PASS** — 1.85 verified locally (`cargo +1.85 check`, default + `work-stealing` + postgres); `otel` needs 1.88 (documented) |

## UNVERIFIED items and how a human verifies them

1. **Comparison benchmarks** — on a networked machine:
   `bench-harness/comparisons/dbos_sqlite.sh`, `temporal_dev.sh`,
   `restate.sh`; each prints `<system> workflows/s <value>` for the same
   W1-shaped workload.
2. **PostgreSQL backend** —
   `docker run --rm -e POSTGRES_PASSWORD=pw -p 5432:5432 postgres:16` then
   `SQRL_POSTGRES_URL=postgres://postgres:pw@localhost:5432/postgres cargo test -p sqrl-store-postgres`.
3. **otel runtime export** — run any OTLP collector, call
   `sqrl::otel::init("http://localhost:4317")`, observe spans/metrics.
4. **macOS CI legs & CI itself** — push and watch `.github/workflows/ci.yml`.
5. **Publish chain** — `cargo publish -p sqrl-core && -p sqrl-macros && …`
   in dependency order (each subsequent dry-run turns green as its deps
   land on crates.io).

## Known limitations (by design or honestly admitted)

* **Single node.** No distribution, no leader election, no replication.
  The scaling story is SQLite's: many independent stores.
* **At-least-once steps.** A step whose result was not yet fsynced may
  re-execute after a crash; `ctx.idempotency_key()` is the tool. sqrl
  never claims exactly-once side effects — nothing can.
* **Bit rot truncates.** Corruption inside the WAL truncates history at
  the flipped byte (logged, resumed). Records behind a corrupted byte are
  lost unless superseded by a snapshot; there is no per-record redundancy.
* **Group commit trades sequential latency for throughput** (p50 2.8 ms vs
  0.7 ms Strict at these settings) — configure per workload; per-step
  `fsync_strict` exists for the critical writes.
* **A hot workflow is bounded by one core** (orchestration); steps
  parallelize on the pool. `work-stealing` moves placement, not a running
  workflow.
* **Absolute benchmark numbers are from a shared 4-vCPU cloud VM**; the
  relative comparisons are the durable part.
* **DST never triggers backpressure organically** (adversary load sits
  under the default cap; `backpressure=0` in the coverage report) — the
  path is covered by a dedicated engine test instead.
* **Metrics counters reset per process** — DST's per-incarnation metric
  collection undercounts totals across crashes (coverage floors still
  trip; documented in the harness).

## Prioritized next work

1. **Run the UNVERIFIED items** (Postgres tests, comparison scripts, otel
   against a collector) — highest information per hour.
2. **Continuous fuzzing budget** — the scheduled 5-min job is a smoke
   test; hours-long runs on the replay-engine target would say more.
3. **DST adversary depth** — drive backpressure organically (burst
   starts), add reordered-network-style signal storms, longer op programs
   (`ops` is 160; the harness scales).
4. **io_uring / O_DIRECT experiment for the WAL** — the fsync floor
   dominates Strict throughput; a ring-based writer could batch better on
   NVMe.
5. **Cross-version replay corpus** — pin serialized journals from 0.1.0
   and replay them in CI forever (format stability regression net).
6. **Multi-process readers** — `sqrl-cli` currently requires a stopped
   store; a read-only snapshot-isolation mode would make `status` safe on
   a live one.
7. **Structured step-result diffing for `replay_check`** — today ND
   reports expected-vs-actual command descriptors; payload-level diffs
   would make patch review faster.

## Final state

* Branch: `claude/sqrl-durable-execution-uhrcgc`; every phase committed
  incrementally with conventional messages; each commit left the tree
  green.
* Full release acceptance at HEAD: **186 passed / 0 failed** (incl. the
  31-point crash sweep, both real `kill -9` tests, dst_short with the
  paranoid oracle, property tests, CLI, SQLite backend, macros).
* `dst_long` at HEAD: **10,000 / 10,000 seeds green in 89 s**.
* `cargo fmt --check` / `clippy -D warnings` (all targets, all features) /
  `cargo doc` / MSRV 1.85 check: clean.
