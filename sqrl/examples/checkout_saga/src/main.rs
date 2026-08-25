//! # checkout_saga — the flagship sqrl example
//!
//! A three-step checkout saga, written as an ordinary async Rust function:
//!
//! ```text
//! reserve-inventory  →  2 s cooling-off timer  →  charge-card  →  schedule-shipping
//! ```
//!
//! sqrl journals every step result, timer, and idempotency key to an
//! embedded write-ahead log (`./checkout-data`). Kill this process at any
//! point and rerun it: the workflow resumes from the last completed step —
//! completed steps are **not** re-executed, and the payment is protected by
//! a replay-stable idempotency key.
//!
//! Run with: `cargo run -p checkout_saga`

use serde::{Deserialize, Serialize};
use sqrl::{Ctx, FsyncPolicy, Sqrl, WalStorage};
use std::collections::HashMap;
use std::sync::{LazyLock, Mutex};
use std::time::Duration;

/// The workflow input. Anything `Serialize + DeserializeOwned` works.
#[derive(Debug, Clone, Serialize, Deserialize)]
struct Order {
    sku: String,
    qty: u32,
    amount_cents: u64,
}

/// The workflow output, returned once the saga completes.
#[derive(Debug, Serialize, Deserialize)]
struct Receipt {
    receipt_id: String,
    sku: String,
    qty: u32,
    amount_cents: u64,
    reservation: String,
    charge_id: String,
    idempotency_key: String,
    tracking: String,
}

// ---------------------------------------------------------------------------
// Mock payment gateway
// ---------------------------------------------------------------------------

/// Charges already made, keyed by idempotency key. A real gateway (Stripe
/// etc.) keeps this table server-side; the contract is identical: charging
/// twice with the same key returns the original charge instead of billing
/// the card again.
static PAYMENT_LEDGER: LazyLock<Mutex<HashMap<String, String>>> =
    LazyLock::new(|| Mutex::new(HashMap::new()));

/// Mock "charge the card" API. Prints the idempotency key it was called
/// with and dedupes on it, so at-least-once step execution (sqrl's
/// guarantee) still yields exactly one charge.
fn charge_card(idempotency_key: &str, amount_cents: u64) -> Result<String, String> {
    let mut ledger = PAYMENT_LEDGER.lock().map_err(|e| e.to_string())?;
    if let Some(existing) = ledger.get(idempotency_key) {
        println!(
            "[payments] key {idempotency_key}: duplicate — returning existing charge \
             {existing}, card NOT billed again"
        );
        return Ok(existing.clone());
    }
    let charge_id = format!("ch_{}", &idempotency_key[..12]);
    println!("[payments] key {idempotency_key}: charging {amount_cents} cents -> {charge_id}");
    ledger.insert(idempotency_key.to_string(), charge_id.clone());
    Ok(charge_id)
}

// ---------------------------------------------------------------------------
// The workflow
// ---------------------------------------------------------------------------

/// Durable checkout saga. The `#[sqrl::workflow]` macro turns this function
/// into a registerable definition: pass the identifier `checkout` straight
/// to `.register(...)` below.
///
/// Orchestration code (this function body, outside the step closures) must
/// be deterministic — it re-runs on recovery with journaled step results
/// substituted in. Side effects and ambient time belong *inside* steps.
#[sqrl::workflow(name = "checkout", version = 1)]
async fn checkout(ctx: &Ctx, order: Order) -> sqrl::Result<Receipt> {
    // Step 1: reserve inventory. Step closures must own their captures
    // (clone before the closure, and again into the async block) because a
    // step may be retried.
    let sku = order.sku.clone();
    let qty = order.qty;
    let reservation: String = ctx
        .step("reserve-inventory", move || {
            let sku = sku.clone();
            async move {
                println!("[reserve-inventory] holding {qty} x {sku}");
                Ok::<_, String>(format!("resv-{sku}-{qty}"))
            }
        })
        .await?;

    // A *durable* timer: journaled, and honored across process restarts. If
    // the process dies during these 2 seconds, the restarted process picks
    // the timer back up — it does not restart from zero.
    println!("[checkout] payment cooling-off: durable 2 s timer (survives restarts)");
    ctx.sleep(Duration::from_secs(2)).await?;

    // Step 2: charge the card. `ctx.idempotency_key()` is drawn from the
    // workflow's journaled seed: the n-th call returns the *same* key on
    // every replay, so even if we crash after charging but before the step
    // result is journaled, the re-executed charge dedupes at the gateway.
    let key = ctx.idempotency_key();
    let amount = order.amount_cents;
    let key_for_step = key.clone();
    let charge_id: String = ctx
        .step("charge-card", move || {
            let key = key_for_step.clone();
            async move { charge_card(&key, amount) }
        })
        .await?;

    // Step 3: schedule shipping.
    let resv = reservation.clone();
    let tracking: String = ctx
        .step("schedule-shipping", move || {
            let resv = resv.clone();
            async move {
                println!("[schedule-shipping] booking carrier for {resv}");
                Ok::<_, String>(format!("track-{resv}"))
            }
        })
        .await?;

    Ok(Receipt {
        // Deterministic, replay-stable UUID — same value live or replayed.
        receipt_id: ctx.uuid(),
        sku: order.sku,
        qty: order.qty,
        amount_cents: order.amount_cents,
        reservation,
        charge_id,
        idempotency_key: key,
        tracking,
    })
}

// ---------------------------------------------------------------------------
// main
// ---------------------------------------------------------------------------

fn main() -> Result<(), Box<dyn std::error::Error>> {
    println!("=== sqrl checkout saga ===");

    // Embedded WAL storage on a local directory — no server, no database.
    // A real service would pick a stable data path (e.g. /var/lib/myapp);
    // ./checkout-data keeps the demo's journal easy to find and inspect.
    let sqrl = Sqrl::builder()
        .storage(WalStorage::open("./checkout-data")?)
        .fsync(FsyncPolicy::default_group())
        .register(checkout)
        .build()?;

    // A workflow id can only ever be started once per data directory, and
    // ./checkout-data persists across runs — so derive a unique order id.
    // Ambient wall-clock is fine here: determinism rules only apply to
    // orchestration code, and this is plain `main`.
    #[allow(clippy::disallowed_methods)] // unique demo id in main(), not orchestration code
    let nanos = std::time::SystemTime::now()
        .duration_since(std::time::UNIX_EPOCH)?
        .as_nanos();
    let order_id = format!("order-{nanos}");

    let order = Order {
        sku: "sqrl-plush".to_string(),
        qty: 2,
        amount_cents: 4_995,
    };
    println!(
        "[main] starting workflow `{order_id}`: {} x {} for {} cents",
        order.qty, order.sku, order.amount_cents
    );

    let handle = sqrl.start_with_id_blocking(order_id, "checkout", &order)?;
    // Blocks until the saga's terminal record is *durable* on disk.
    let receipt: Receipt = handle.result_blocking()?;

    println!("[main] saga complete — receipt:");
    println!("         receipt_id:  {}", receipt.receipt_id);
    println!("         order:       {} x {}", receipt.qty, receipt.sku);
    println!("         amount:      {} cents", receipt.amount_cents);
    println!("         reservation: {}", receipt.reservation);
    println!("         charge:      {}", receipt.charge_id);
    println!("         tracking:    {}", receipt.tracking);

    // Show the idempotency dedupe in action: replaying the charge with the
    // same key (what an at-least-once redelivery would do) is a no-op.
    println!("[main] replaying the charge with the same idempotency key:");
    let again = charge_card(&receipt.idempotency_key, receipt.amount_cents)?;
    assert_eq!(again, receipt.charge_id, "same key must yield same charge");

    sqrl.shutdown(); // flush + fsync every shard
    println!("=== done (journal kept in ./checkout-data) ===");
    Ok(())
}
