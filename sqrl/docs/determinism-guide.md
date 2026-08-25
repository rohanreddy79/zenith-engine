# The determinism guide

sqrl replays your workflow function over its own journal to recover after a
crash. That only works if the function is a **pure function of its input
plus the journaled outcomes**. This page is the contract.

## The one rule

> Orchestration code (the body of a `#[sqrl::workflow]` function, outside of
> step closures) must get **everything** non-deterministic through `Ctx`.

Inside **steps**, anything goes — steps exist precisely to hold wall-clock
time, network calls, randomness, filesystem access, and every other effect.
Their results are journaled; on replay the journaled result is returned and
the step body never runs again.

## Allowed in orchestration code

| Need | Use |
|---|---|
| Current time | `ctx.now()` (logical time of the last processed record) |
| Waiting | `ctx.sleep(d)` / `ctx.sleep_until(t)` — durable, survives restarts |
| Randomness | `ctx.random()` / `ctx.random_f64()` — seeded, replay-stable |
| Unique ids | `ctx.uuid()` — replay-stable UUIDv4-format |
| Dedup keys for effects | `ctx.idempotency_key()` — stable across retries **and** replays |
| External input | `ctx.await_signal::<T>(name)` |
| Any effect | `ctx.step(name, closure)` / `ctx.step_with` |
| Changing the code | `ctx.patched("change-id")` (see `versioning-and-patching.md`) |
| Pure computation | anything deterministic: arithmetic, collections, serde, `match`… |

## Bugs in orchestration code (each one will corrupt replay)

* `std::time::SystemTime::now()`, `Instant::now()`, `chrono::Utc::now()` —
  time moves between runs. Use `ctx.now()`.
* `rand::random()`, `Uuid::new_v4()`, `HashMap`/`HashSet` **iteration**
  (randomly seeded ordering!) — use `ctx.random()`, `ctx.uuid()`,
  `BTreeMap`/`BTreeSet` or sort before iterating.
* Reading files, environment variables, config that can change, global
  mutable state, channels from other threads — wrap in a step.
* `tokio::time::sleep`, or awaiting **any non-sqrl future** — the engine
  controls the workflow's suspension points; awaiting a foreign future
  deadlocks and is failed loudly with an explanatory error.
* `std::thread::sleep` — blocks the whole engine core.
* Branching on anything above.

sqrl enforces some of this mechanically: the workspace clippy config
(`clippy.toml`, `disallowed-methods`) bans ambient time/sleep everywhere and
the engine fails a workflow that parks on a foreign future. The rest is on
you — and on the replay validator.

## What happens when you get it wrong

Every command your code issues during replay is checked against the journal:
step names, command kinds, timer targets, signal names, patch ids, and the
overall command count. A mismatch raises a **typed `NonDeterminismError`**
(`expected` vs `actual` at the diverging seq). The workflow moves to
`Failed(NonDeterministic)` and is *never* retried automatically — you will
not get a retry loop, and the failure is not journaled, so rolling back the
code and restarting heals the workflow.

Two important nuances:

* **`ctx.random()` / `ctx.uuid()` / `ctx.now()` are not validated** — they
  are deterministic by construction (derived from the journaled seed and
  record timestamps). If you branch on them, both runs branch identically.
* **Batched crash windows**: a crash can lose the tail of the journal. Code
  re-runs from the last durable prefix; steps whose results were lost simply
  re-execute (at-least-once). That is not non-determinism; it is the
  contract.

## Effectively-once: the idempotency pattern

sqrl guarantees **at-least-once** step execution — never exactly-once (no
system can promise exactly-once side effects on external services; anyone
who says otherwise is hiding a window). The pattern:

```rust
let key = ctx.idempotency_key();          // stable across retries + replays
let charge = ctx
    .step("charge", move || {
        let key = key.clone();
        async move { payment_api.charge(&order, &key).await }
    })
    .await?;
```

If the process dies after the charge succeeded but before the result was
journaled, the step re-executes — with the **same key** — and the payment
provider deduplicates. That is "effectively-once", and it is the strongest
honest guarantee.

## Step closures own their captures

Step futures run on the step pool and may be re-created for retries, so the
closure must be `move` and own what it uses (clone `Arc`s/values in):

```rust
let e = Arc::clone(&client);
ctx.step("fetch", move || {
    let e = Arc::clone(&e);            // clone again into the future
    async move { e.get(url).await.map_err(|x| x.to_string()) }
}).await?;
```

## Concurrency inside a workflow

`join!`/`select!` over sqrl futures are fine: outcomes are revealed to your
code one at a time **in journal order, live and replayed alike**, so races
resolve identically after a crash. Each workflow still has exactly one
logical thread of control — there is no parallelism inside orchestration,
only interleaving; parallelism belongs to steps.
