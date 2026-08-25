# 0005 — At-least-once + idempotency keys; never "exactly-once"

## Context
A step's effect and its journal record cannot be committed atomically —
the effect lives in an external system. Any claim of exactly-once side
effects hides a window between effect and acknowledgment.

## Decision
sqrl promises **at-least-once step execution** and provides
`ctx.idempotency_key()` — stable across retries and replays — so external
effects can deduplicate ("effectively-once"). Documentation states this
everywhere results are described; the crash-at-every-boundary acceptance
test asserts exactly this contract (step may re-run; keyed effect dedupes
to one).

## Consequences
+ Honest, testable semantics; the recovery path never needs distributed
  transactions.
− Users must thread keys into external calls for dedup; the docs and the
  flagship example model the pattern.
