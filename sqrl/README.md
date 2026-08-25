# sqrl

**Embedded, deterministic-first durable execution for Rust.** Think "the
SQLite of durable execution": `cargo add sqrl`, write workflows as async
functions, and if your process is `kill -9`'d at any point, every workflow
resumes from its last completed step on restart. No server. No Postgres. No
cluster. One directory of checksummed files.

```rust
use sqrl::{Ctx, Result, Sqrl, WalStorage};
use std::time::Duration;

#[sqrl::workflow(name = "checkout", version = 1)]
async fn checkout(ctx: &Ctx, order: Order) -> Result<Receipt> {
    let hold = ctx.step("reserve", move || reserve(order.clone())).await?;
    ctx.sleep(Duration::from_secs(30)).await?;          // durable timer
    let key = ctx.idempotency_key();                    // stable across retries & replays
    let charge = ctx.step("charge", move || charge_card(hold.clone(), key.clone())).await?;
    ctx.step("ship", move || schedule_shipping(charge.clone())).await?;
    Ok(Receipt::from(charge))
}

fn main() -> anyhow::Result<()> {
    let sqrl = Sqrl::builder()
        .storage(WalStorage::open("./data")?)
        .register(checkout)
        .build()?;
    let handle = sqrl.start_blocking("checkout", &order_123)?;
    let receipt: Receipt = handle.result_blocking()?;   // resolves once durable
    Ok(())
}
```

Kill the process anywhere in that saga — mid-step, mid-sleep, mid-fsync —
restart, and it finishes. `examples/crash_me` demonstrates it live with a
real SIGKILL.

## What you get

- **Durable steps** — every `ctx.step` result is journaled to an embedded,
  checksummed write-ahead log; on replay, recorded results are returned
  without re-execution.
- **Durable timers & signals** — `ctx.sleep(30 days)` and
  `ctx.await_signal::<T>("approval")` survive any number of restarts.
- **Deterministic-first** — time, randomness, UUIDs, and idempotency keys
  are injected and replay-stable. Incompatible code changes are caught as a
  **typed `NonDeterminismError`** (never a retry loop), with
  `ctx.patched("id")` gates for safe migrations.
- **Deterministic Simulation Testing** — the exact production engine runs
  under a seeded simulator with crash/torn-write/bit-rot/disk-full
  injection. The test suite kills the "process" at *every* disk operation
  of a saga and proves it always completes, effectively-once.
- **Thread-per-core** — shared-nothing engine cores, group-commit fsync
  (2 ms / 256 records by default, `Strict` when you need it), snapshot
  compaction with **no cap on journal length**, passivation of idle
  workflows, backpressure, retries with deterministic jittered backoff.
- **No runtime dependencies** — local disk by default. Optional SQLite
  backend (`sqrl-store-sqlite`); Tokio is used only inside the step pool.

## Guarantees — read this

sqrl guarantees **at-least-once step execution** plus **idempotency
helpers**: after a crash, a step whose result wasn't yet durable will run
again, and `ctx.idempotency_key()` gives you a stable key so the external
effect deduplicates to *effectively-once*. sqrl **never claims
exactly-once side effects** — no system honestly can. Completion results
(`handle.result()`) are released only after fsync. Details:
[`docs/determinism-guide.md`](docs/determinism-guide.md).

## What sqrl is not

Single-node, Rust-only, no web UI, no worker fleets, no multi-tenancy. If
you need HA, horizontal scale-out, or polyglot SDKs, use Temporal, Restate,
or DBOS — the honest comparison, including where sqrl loses, is in
[`docs/comparison.md`](docs/comparison.md).

## Learn more

- [`docs/architecture.md`](docs/architecture.md) — engine design (sans-executor core, revelation rule, state machine)
- [`docs/determinism-guide.md`](docs/determinism-guide.md) — what is/isn't allowed in orchestration code
- [`docs/on-disk-format.md`](docs/on-disk-format.md) — the WAL format (`SQRL_FORMAT_VERSION`), stability policy
- [`docs/versioning-and-patching.md`](docs/versioning-and-patching.md) — evolving workflow code safely
- [`docs/dst.md`](docs/dst.md) — the simulation-testing story
- [`docs/benchmarks.md`](docs/benchmarks.md) — measured numbers with reproduction commands
- [`docs/adr/`](docs/adr/) — every non-obvious design decision
- [`examples/`](examples/) — checkout saga, kill -9 demo, AI-agent loop, long-running counter

## License

MIT OR Apache-2.0.
