# 0007 — Versioning API: ctx.patched() gates + workflow version tag

## Context
Code changes while workflows are mid-flight. Replaying old journals under
new code must either work or fail loudly — silent corruption is the one
unforgivable outcome.

## Decision
Three mechanisms. (1) Replay validation: every command is checked against
history; divergence is a typed `NonDeterminismError` into
`Failed(NonDeterministic)`, never retried, never journaled — rollback
heals. (2) `ctx.patched("change-id")`: Temporal-style gate. First
evaluation journals `PatchRecorded` and returns true on fresh/live
execution; returns false (consuming no seq) while replaying pre-patch
history; sticky per id per execution. Old histories replay the old branch,
new executions take the new branch, and the gate can be removed once no
pre-patch workflow survives. (3) A `version` tag on `#[workflow]`, journaled
at start for observability and future routing; `sqrl replay --against`
(Phase 3 CLI) replays stored journals against current code pre-deploy.

## Consequences
+ Safe evolution without workflow migration downtime; incompatibility is
  loud, typed, and reversible.
− Patch gates are manual discipline; the CLI replay check is the safety
  net before deploys.
