//! Property-based tests (proptest):
//! 1. WAL codec round-trip for arbitrary journal records.
//! 2. Replay idempotence: loading the same store twice yields identical
//!    engine state; replaying a journal is side-effect-free on the journal.
//! 3. Snapshot equivalence: a workflow's terminal output is identical with
//!    snapshots enabled and disabled.

use proptest::prelude::*;
use serde::{Deserialize, Serialize};
use sqrl::{Ctx, EngineConfig, FsyncPolicy, Registry};
use sqrl_core::error::StepError;
use sqrl_core::event::{JournalEvent, JournalRecord};
use sqrl_core::{Error, LogicalTime, StateKind, WorkflowId};
use sqrl_sim::{SimClock, SimDisk, SimScheduler};
use sqrl_store::codec::{decode_one, encode, scan, WalEntry, WalRecord};
use sqrl_store::{WalOptions, WalStorage};
use std::collections::BTreeMap;
use std::sync::Arc;
use std::time::Duration;

// ---------------------------------------------------------------------------
// 1. Codec round-trip
// ---------------------------------------------------------------------------

fn arb_step_error() -> impl Strategy<Value = StepError> {
    prop_oneof![
        any::<String>().prop_map(StepError::App),
        any::<String>().prop_map(StepError::Panic),
        any::<String>().prop_map(StepError::ResultNotJournalable),
    ]
}

fn arb_event() -> impl Strategy<Value = JournalEvent> {
    prop_oneof![
        (
            any::<String>(),
            any::<u32>(),
            prop::collection::vec(any::<u8>(), 0..256),
            any::<u64>()
        )
            .prop_map(
                |(name, version, input, seed)| JournalEvent::WorkflowStarted {
                    name,
                    version,
                    input,
                    seed
                }
            ),
        (any::<u64>(), any::<String>())
            .prop_map(|(seq, name)| JournalEvent::StepScheduled { seq, name }),
        (any::<u64>(), prop::collection::vec(any::<u8>(), 0..512))
            .prop_map(|(seq, result)| JournalEvent::StepCompleted { seq, result }),
        (
            any::<u64>(),
            arb_step_error(),
            any::<u32>(),
            any::<Option<u64>>()
        )
            .prop_map(|(seq, error, attempt, retry)| JournalEvent::StepFailed {
                seq,
                error,
                attempt,
                retry_at: retry.map(LogicalTime::from_millis),
            }),
        (any::<u64>(), any::<u64>()).prop_map(|(seq, at)| JournalEvent::TimerScheduled {
            seq,
            fire_at: LogicalTime::from_millis(at)
        }),
        any::<u64>().prop_map(|seq| JournalEvent::TimerFired { seq }),
        (any::<u64>(), any::<String>())
            .prop_map(|(seq, name)| JournalEvent::SignalAwaited { seq, name }),
        (any::<String>(), prop::collection::vec(any::<u8>(), 0..512))
            .prop_map(|(name, payload)| JournalEvent::SignalReceived { name, payload }),
        (any::<u64>(), any::<String>())
            .prop_map(|(seq, id)| JournalEvent::PatchRecorded { seq, id }),
        prop::collection::vec(any::<u8>(), 0..256)
            .prop_map(|output| JournalEvent::WorkflowCompleted { output }),
        Just(JournalEvent::WorkflowFailed {
            error: Error::App("prop".to_string())
        }),
        Just(JournalEvent::WorkflowCancelled),
        Just(JournalEvent::WorkflowResumed),
    ]
}

proptest! {
    #![proptest_config(ProptestConfig::with_cases(256))]

    #[test]
    fn codec_round_trips(
        wf in "[a-zA-Z0-9_-]{1,64}",
        index in any::<u64>(),
        at in any::<u64>(),
        event in arb_event(),
    ) {
        let rec = WalRecord::Entry(WalEntry {
            workflow: WorkflowId::new(wf),
            record: JournalRecord {
                index,
                at: LogicalTime::from_millis(at),
                event,
            },
        });
        let bytes = encode(&rec).unwrap();
        let (back, consumed) = decode_one(&bytes, 0).unwrap().unwrap();
        prop_assert_eq!(&back, &rec);
        prop_assert_eq!(consumed, bytes.len());
        // Concatenated stream scans back losslessly.
        let mut stream = bytes.clone();
        stream.extend_from_slice(&bytes);
        let (records, end) = scan(&stream);
        prop_assert_eq!(records.len(), 2);
        prop_assert_eq!(end, sqrl_store::codec::DecodeEnd::Eof);
    }

    #[test]
    fn corrupting_any_single_byte_never_panics_and_never_misdecodes_silently(
        event in arb_event(),
        flip_at in any::<prop::sample::Index>(),
        xor in 1u8..=255,
    ) {
        let rec = WalRecord::Entry(WalEntry {
            workflow: WorkflowId::new("wf"),
            record: JournalRecord { index: 1, at: LogicalTime::from_millis(1), event },
        });
        let mut bytes = encode(&rec).unwrap();
        let pos = flip_at.index(bytes.len());
        bytes[pos] ^= xor;
        // Must not panic; if it decodes, the CRC must genuinely match (the
        // flip landed in the length prefix making a *shorter* valid record is
        // impossible because CRC covers type+version+payload).
        if let Ok(Some((decoded, _))) = decode_one(&bytes, 0) {
            // The only way a flip survives is a CRC collision, which crc32c
            // makes practically impossible for single-byte flips; anything
            // that decodes must therefore be the original record.
            prop_assert_eq!(decoded, rec, "single-byte flip decoded to a DIFFERENT record");
        } // Ok(None)/Err = detected: good
    }
}

// ---------------------------------------------------------------------------
// 2 & 3. Engine-level properties over generated workloads
// ---------------------------------------------------------------------------

#[derive(Debug, Clone, Serialize, Deserialize)]
enum Op {
    Step(u8),
    Sleep(u16),
    Random,
}

fn arb_program() -> impl Strategy<Value = Vec<Op>> {
    prop::collection::vec(
        prop_oneof![
            (1u8..20).prop_map(Op::Step),
            (1u16..2000).prop_map(Op::Sleep),
            Just(Op::Random),
        ],
        1..12,
    )
}

fn interpreter_registry() -> Arc<Registry> {
    let mut reg = Registry::new();
    reg.register("interp", 1, |ctx: Ctx, ops: Vec<Op>| async move {
        let mut acc: u64 = 0;
        for (i, op) in ops.into_iter().enumerate() {
            match op {
                Op::Step(n) => {
                    let v: u64 = ctx
                        .step("op", move || async move { Ok::<u64, String>(n as u64) })
                        .await?;
                    acc = acc.wrapping_add(v.wrapping_mul(i as u64 + 1));
                }
                Op::Sleep(ms) => ctx.sleep(Duration::from_millis(ms as u64)).await?,
                Op::Random => acc = acc.wrapping_add(ctx.random() % 97),
            }
        }
        Ok(acc)
    });
    Arc::new(reg)
}

fn run_program(ops: &[Op], snapshot_every: u64, seed: u64) -> (u64, SimDisk, SimClock) {
    let disk = SimDisk::new(seed);
    let clock = SimClock::new(LogicalTime::from_millis(1_000));
    let storage = WalStorage::open_with(
        Arc::new(disk.clone()),
        WalOptions {
            num_shards: 1,
            segment_size: 4096,
        },
    )
    .unwrap();
    let cfg = EngineConfig {
        fsync: FsyncPolicy::Strict,
        snapshot_every,
        ..EngineConfig::default()
    };
    let mut sched =
        SimScheduler::with_clock(seed, &storage, interpreter_registry(), cfg, clock.clone())
            .unwrap();
    let handle = sched.start("p-1", "interp", &ops.to_vec()).unwrap();
    sched.run_until_idle();
    let out: u64 = handle.result_blocking().expect("program completes");
    sched.shutdown();
    (out, disk, clock)
}

fn engine_digest(
    disk: &SimDisk,
    clock: &SimClock,
    snapshot_every: u64,
    seed: u64,
) -> (BTreeMap<WorkflowId, StateKind>, Option<u64>) {
    let storage = WalStorage::open_with(
        Arc::new(disk.clone()),
        WalOptions {
            num_shards: 1,
            segment_size: 4096,
        },
    )
    .unwrap();
    let cfg = EngineConfig {
        fsync: FsyncPolicy::Strict,
        snapshot_every,
        ..EngineConfig::default()
    };
    let mut sched =
        SimScheduler::with_clock(seed, &storage, interpreter_registry(), cfg, clock.clone())
            .unwrap();
    sched.run_until_idle();
    let states = sched.states();
    let out = sched
        .handle("p-1")
        .ok()
        .and_then(|h| h.peek())
        .and_then(|r| r.ok())
        .and_then(|bytes| sqrl_core::codec::from_slice::<u64>(&bytes, "out").ok());
    (states, out)
}

proptest! {
    #![proptest_config(ProptestConfig::with_cases(24))]

    /// Replay idempotence: re-opening the same store any number of times
    /// yields the same states and the same preserved result, and replaying
    /// never mutates the journal (byte-identical durable image before/after).
    #[test]
    #[cfg_attr(debug_assertions, ignore = "slow: run in release (CI acceptance job)")]
    fn replay_is_idempotent(ops in arb_program()) {
        let (out, disk, clock) = run_program(&ops, 8, 42);
        disk.crash();
        disk.recover();
        let image_before = disk.durable_image();
        let (states1, out1) = engine_digest(&disk, &clock, 8, 42);
        let (states2, out2) = engine_digest(&disk, &clock, 8, 42);
        prop_assert_eq!(&states1, &states2, "two loads must agree");
        prop_assert_eq!(out1, Some(out), "result preserved");
        prop_assert_eq!(out2, Some(out), "result preserved twice");
        // Replay itself journals nothing new for a terminal workflow.
        disk.crash();
        disk.recover();
        let image_after = disk.durable_image();
        prop_assert_eq!(image_before, image_after, "replay must not mutate the journal");
    }

    /// Snapshot equivalence: identical terminal output with snapshots
    /// enabled (small cadence) and completely disabled.
    #[test]
    #[cfg_attr(debug_assertions, ignore = "slow: run in release (CI acceptance job)")]
    fn snapshot_equivalence(ops in arb_program()) {
        let (with_snap, _, _) = run_program(&ops, 4, 7);
        let (without_snap, _, _) = run_program(&ops, u64::MAX, 7);
        prop_assert_eq!(with_snap, without_snap);
    }
}
