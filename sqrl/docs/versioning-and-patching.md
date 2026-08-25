# Versioning and patching workflows

Workflow code changes while workflows are running. This page is the safe
procedure. The mechanisms behind it are ADR 0007.

## What happens if you just change the code

On the next replay (restart, passivation reload, signal to a recovering
workflow), sqrl validates every command your code issues against the
journal. If the code now takes a different path — a step renamed, added,
removed, reordered; a sleep duration changed; a signal name changed — the
workflow fails with a **typed `NonDeterminismError`** telling you the seq,
what the journal expected, and what the code did. It is *not* retried (no
loop), and the failure is *not* journaled — deploying the old code again
heals the workflow. New workflows, and workflows whose replay never crosses
the changed region, are unaffected.

## The patch gate: `ctx.patched`

To change code while old histories are still replaying, gate the change:

```rust
if ctx.patched("charge-in-two-phases-2026-08") {
    // NEW code path (fresh executions take this)
    let auth = ctx.step("authorize", …).await?;
    let capture = ctx.step("capture", …).await?;
} else {
    // OLD code path (pre-patch histories replay this)
    let charge = ctx.step("charge", …).await?;
}
```

Semantics:

* **Fresh executions** (and live continuation past the end of history):
  the gate journals `PatchRecorded` and returns `true` — new path.
* **Replaying pre-patch history**: returns `false`, consumes no command
  seq — the old branch replays exactly as recorded.
* **Replaying post-patch history**: the journaled `PatchRecorded` matches
  and the gate returns `true` again.
* The decision is **sticky per id** within an execution: every call with
  the same id returns the same answer.

Rollout procedure:

1. Deploy with the gate and both branches. Old workflows keep replaying the
   old branch; new workflows take the new one.
2. Once no pre-patch workflow can still exist (all completed / cancelled),
   delete the old branch **but keep the `ctx.patched(...)` call** (its
   `PatchRecorded` is in post-patch histories).
3. Once no workflow started while the gate existed survives, delete the
   call too.

## The `version` tag

`#[sqrl::workflow(name = "checkout", version = 2)]` journals the version at
start. v1 treats it as observability metadata (it shows in `sqrl status` /
`inspect` and in `WorkflowStarted`); it does not route. Bump it whenever
behavior changes so operators can tell which era a stored workflow belongs
to.

## Pre-deploy validation: `sqrl replay`

`sqrl replay --data <dir>` (Phase 3 CLI) replays every non-terminal stored
journal against the *current* binary's registered workflows and reports any
`NonDeterminismError` before you deploy — the mechanical answer to "will
this code change strand anything?".

## What never needs a gate

* Changing code **inside a step closure** (the journaled result is replayed;
  the body doesn't re-run) — as long as inputs/outputs stay compatible.
* Pure refactors that don't change the command sequence (renaming local
  variables, extracting functions, logging).
* Changing retry policies or fsync options (they affect scheduling, not the
  command stream).
* Adding **new** workflows.

## What always needs a gate

Adding/removing/reordering/renaming steps, timers, signal awaits; changing
a sleep duration; changing anything that decides *which* commands are
issued, including branches on `ctx.random()`/input interpretation changes.
