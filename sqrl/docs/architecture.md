# sqrl architecture

sqrl is an in-process durable-execution engine. This document describes how
the pieces fit; the on-disk format is in `on-disk-format.md`, the rules for
workflow code in `determinism-guide.md`, and individual decisions in
`adr/`.

## Layering

```
┌────────────────────────────────────────────────────────────┐
│ sqrl (facade)          Sqrl builder · RealScheduler        │
│                        (thread-per-core + Tokio step pool) │
├──────────────┬─────────────────────────────────────────────┤
│ sqrl-macros  │ sqrl-sim   SimScheduler · SimExecutor       │
│ #[workflow]  │            SimClock · SimRng · SimDisk      │
├──────────────┴─────────────────────────────────────────────┤
│ sqrl-core    EngineCore (sans-executor) · Ctx · replay     │
│              journal events · state machine · retry        │
│              Clock/Entropy/Vfs/Storage traits              │
├────────────────────────────────────────────────────────────┤
│ sqrl-store   WalStorage (segments, manifest, snapshots,    │
│              group commit, GC) · MemoryStorage · StdVfs    │
└────────────────────────────────────────────────────────────┘
```

**The engine core is sans-executor** (ADR 0001): `EngineCore` owns one
shard's workflows, journals, timer wheel, and group-commit state, but
contains no threads, no wall clock, and no ambient entropy. A *driver* feeds
it commands (`EngineCmd`), calls `tick()`, executes the step futures it
emits, and feeds results back:

* `SimScheduler` (sqrl-sim) drives any number of shards on one seeded
  thread under virtual time — this is what deterministic simulation testing
  runs on.
* `RealScheduler` (sqrl facade) gives each shard its own OS thread
  (shared-nothing, `hash(workflow_id) % N` placement) and executes step
  futures on a dedicated Tokio multi-thread runtime. The orchestration path
  never touches Tokio.

The same engine code runs under both. That inversion — engine as a pure
state machine, scheduling as a pluggable driver — is what makes byte-level
determinism testable.

## The durable loop

A workflow is an async fn `(ctx, input) -> Result<Output>`. Orchestration
code issues **commands** through `Ctx` (steps, timers, signal awaits, patch
gates), numbered densely `0, 1, 2, …` in program order. Everything the
engine learns back — step results, timer fires, signal arrivals — is an
**outcome**.

1. Commands are journaled when first issued (`StepScheduled`,
   `TimerScheduled`, `SignalAwaited`, `PatchRecorded`).
2. Effects execute *outside* the engine (step pool); their results come back
   as `EngineCmd::StepFinished`.
3. Outcomes are journaled (`StepCompleted`, `StepFailed`, `TimerFired`,
   `SignalReceived`) and then **revealed** to the workflow.
4. On restart, the journal is read back and the same code re-runs from the
   top; commands are matched against history instead of re-journaled, and
   outcomes are served from history instead of re-executed.

### The revelation rule

Outcomes reach orchestration code through an ordered queue, **one outcome
per poll, in journal order — even during live execution**. A live run is
therefore a replay of its own journal as the journal forms. This is what
makes `select!`-style races deterministic across crash/recovery: the order
in which two racing outcomes became visible is exactly the order of their
journal records, live and replayed alike.

### Non-determinism detection

During replay, every command the code issues is validated against the
recorded command at the same seq (kind, step name, signal name, timer
target). Any mismatch — including the code issuing new commands while
unrevealed history remains, or completing while history continues — raises
a typed `NonDeterminismError`; the workflow moves to
`Failed(NonDeterministic)` and is **never retried automatically**. The
failure is deliberately *not* journaled: rolling the code back (or gating
the change with `ctx.patched`) and restarting heals the workflow. See
`versioning-and-patching.md`.

## Lifecycle state machine

```
Pending ──► Running ◄──────────────┐
              │  ▲                 │
              │  └─ AwaitingStep ──┤   (step result)
              ├──── Sleeping ──────┤   (durable timer)
              ├──── Blocked ───────┘   (signal)
              ├──► Completed ▪
              ├──► Failed ▪ ──► Recovering   (explicit `sqrl resume` only)
              └──► Cancelled ▪
   any non-terminal ──► Recovering ──► (state per history)
```

The transition function is an exhaustive match with no wildcard arms
(`sqrl-core/src/state.rs`); an illegal transition is a typed error, counted
in metrics (DST asserts the counter stays zero), never a panic.

## Failure semantics

| Failure | Behavior (all tested) |
|---|---|
| Crash mid-workflow | Replay from latest snapshot + journal; in-flight steps re-dispatch; at-least-once execution. |
| Code drift on replay | Typed `NonDeterminismError`, `Failed(NonDeterministic)`, no retry loop, not journaled (heals on rollback). |
| Poison step | Retries per `RetryPolicy` (exponential backoff, deterministic jitter from the journaled seed); exhaustion → `Failed`, full journal retained. |
| Duplicate side effect | Expected under at-least-once; `ctx.idempotency_key()` is stable across retries and replays for dedup. |
| Disk full / write error | Store poisons itself; nothing is acknowledged durable after a failed fsync; new starts rejected `Unavailable`. |
| Memory pressure | Bounded live workflows per shard (`Rejected::Backpressure`); idle Sleeping/Blocked workflows passivate (LRU by idle time) and replay on demand. |
| Clock jumps | Timers live on journaled logical time from the injected clock; wall time only enters through the driver. |
| Torn write / bit rot | CRC per record; recovery truncates at the first invalid record (offset logged) and resumes from the valid prefix. |
| Panic in a step | Caught at the step boundary, journaled `StepFailed`, retried per policy. |
| Panic in orchestration | `WorkflowFailed(OrchestrationPanic)` — a bug in the workflow definition, journaled terminally. |

## Group commit and durability acknowledgment

Appends are buffered; `sync()` (fsync) is the only durability barrier.
`FsyncPolicy`:

* `Strict` — fsync every commit batch.
* `Group { max_delay, max_batch }` (default 2 ms / 256) — fsync when the
  batch fills or the oldest unsynced record ages out.
* `Relaxed { interval }` — periodic fsync; a power failure may lose up to
  `interval` of *acknowledged-to-code* progress but never breaks prefix
  consistency.

Two things wait for the durability barrier regardless of policy: workflow
terminal results (`handle.result()` resolves only once the terminal record
is synced) and steps marked `StepOptions::fsync_strict` (the workflow does
not proceed past them until their record is durable). Ordinary step
completions are revealed to the workflow before fsync — a crash simply
replays them, which at-least-once semantics permit.

## Snapshots and passivation

A snapshot is **compacted history**, not a serialized continuation (Rust
futures cannot be serialized — ADR 0006): the command table, the ordered
revelation stream, in-flight step/timer state, and start info. Replay from a
snapshot re-runs the workflow function from the top but serves everything
from one record instead of decoding the whole journal. Cadence is amortized
(at least `snapshot_every` new records *and* ≥ ¼ of total history since the
last snapshot) so total snapshot bytes stay linear in history — there is no
cap on journal length. Completed/cancelled workflows write a terminal
snapshot so their segments can be reclaimed; failed workflows keep their
full journal for debugging and `sqrl fork`.

Passivated workflows (idle past `passivate_after`) drop all in-memory state;
a signal or timer reactivates them via ordinary recovery replay.

## Determinism boundary

Everything inside `sqrl-core` draws time from `Clock`, entropy from
`Entropy`, and disk from `Vfs`/`Storage`. The clippy `disallowed-methods`
config bans `SystemTime::now`, `Instant::now`, and `thread::sleep`
workspace-wide; the few legitimate uses (the real scheduler and clock
implementations, benches, real-time tests) carry explicit annotated allows.
