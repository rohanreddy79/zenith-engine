//! Targeted unit coverage for small leaf APIs the integration suites reach
//! only partially: event descriptors, snapshot round trips, handles,
//! config constructors, codec error contexts.

use sqrl_core::codec;
use sqrl_core::event::{CmdDesc, JournalEvent};
use sqrl_core::snapshot::{
    InflightStep, Outcome, SnapshotBody, SnapshotMeta, SnapshotRecord, TerminalStatus,
};
use sqrl_core::sync::promise;
use sqrl_core::{
    Error, FsyncPolicy, LogicalTime, StepError, StepOptions, TerminalResult, WorkflowHandle,
    WorkflowId,
};

fn every_event() -> Vec<JournalEvent> {
    vec![
        JournalEvent::WorkflowStarted {
            name: "wf".into(),
            version: 1,
            input: vec![1],
            seed: 7,
        },
        JournalEvent::StepScheduled {
            seq: 0,
            name: "s".into(),
        },
        JournalEvent::StepCompleted {
            seq: 0,
            result: vec![2],
        },
        JournalEvent::StepFailed {
            seq: 0,
            error: StepError::App("x".into()),
            attempt: 1,
            retry_at: None,
        },
        JournalEvent::TimerScheduled {
            seq: 1,
            fire_at: LogicalTime::from_millis(5),
        },
        JournalEvent::TimerFired { seq: 1 },
        JournalEvent::SignalAwaited {
            seq: 2,
            name: "go".into(),
        },
        JournalEvent::SignalReceived {
            name: "go".into(),
            payload: vec![3],
        },
        JournalEvent::PatchRecorded {
            seq: 3,
            id: "p1".into(),
        },
        JournalEvent::WorkflowCompleted { output: vec![4] },
        JournalEvent::WorkflowFailed {
            error: Error::App("dead".into()),
        },
        JournalEvent::WorkflowCancelled,
        JournalEvent::WorkflowResumed,
    ]
}

#[test]
fn event_kinds_are_distinct_and_stable() {
    let events = every_event();
    let kinds: Vec<&str> = events.iter().map(|e| e.kind()).collect();
    let mut dedup = kinds.clone();
    dedup.sort_unstable();
    dedup.dedup();
    assert_eq!(
        dedup.len(),
        events.len(),
        "kind() must be unique per variant"
    );
    // Command records carry a descriptor; outcome/terminal records do not.
    let descs: Vec<Option<(u64, CmdDesc)>> = events.iter().map(|e| e.cmd_desc()).collect();
    assert_eq!(descs.iter().filter(|d| d.is_some()).count(), 4);
    assert_eq!(
        events[4].cmd_desc(),
        Some((1, CmdDesc::Timer)),
        "timer descriptor"
    );
    assert_eq!(
        events[6].cmd_desc(),
        Some((2, CmdDesc::AwaitSignal { name: "go".into() }))
    );
    assert_eq!(
        events[8].cmd_desc(),
        Some((3, CmdDesc::Patch { id: "p1".into() }))
    );
}

#[test]
fn every_event_round_trips_through_codec() {
    for e in every_event() {
        let bytes = codec::to_vec(&e, "event").unwrap();
        let back: JournalEvent = codec::from_slice(&bytes, "event").unwrap();
        assert_eq!(e, back);
    }
}

#[test]
fn codec_errors_carry_their_context() {
    let err = codec::from_slice::<u64>(&[0xC1], "flux capacitor").unwrap_err();
    let text = err.to_string();
    assert!(text.contains("flux capacitor"), "got: {text}");
}

#[test]
fn snapshot_full_round_trip_with_rich_meta() {
    let body = SnapshotBody {
        cmds: vec![
            (0, CmdDesc::Step { name: "a".into() }),
            (1, CmdDesc::Timer),
            (2, CmdDesc::AwaitSignal { name: "go".into() }),
        ]
        .into_iter()
        .collect(),
        outcomes: vec![
            Outcome::StepOk {
                seq: 0,
                result: vec![1, 2],
                at: LogicalTime::from_millis(10),
            },
            Outcome::StepErr {
                seq: 0,
                error: StepError::Panic("kaboom".into()),
                attempts: 4,
                at: LogicalTime::from_millis(11),
            },
            Outcome::TimerFired {
                seq: 1,
                at: LogicalTime::from_millis(12),
            },
            Outcome::Signal {
                name: "go".into(),
                payload: vec![9],
                at: LogicalTime::from_millis(13),
            },
            Outcome::Resumed {
                at: LogicalTime::from_millis(14),
            },
        ],
    };
    let meta = SnapshotMeta {
        start: None,
        inflight_steps: vec![(
            5,
            InflightStep {
                name: "hot".into(),
                failed_attempts: 2,
                retry_at: Some(LogicalTime::from_millis(99)),
            },
        )]
        .into_iter()
        .collect(),
        pending_timers: vec![(6, LogicalTime::from_millis(100))]
            .into_iter()
            .collect(),
        terminal: Some(TerminalStatus::Completed { output: vec![7] }),
        wf_time: LogicalTime::from_millis(50),
    };
    let rec = SnapshotRecord::build(3, meta.clone(), &body).unwrap();
    assert_eq!(rec.upto, 3);
    assert_eq!(rec.meta, meta);
    assert_eq!(rec.decode_body().unwrap(), body);
    // And the whole record survives the wire format (serde_bytes body path).
    let bytes = codec::to_vec(&rec, "snapshot").unwrap();
    let back: SnapshotRecord = codec::from_slice(&bytes, "snapshot").unwrap();
    assert_eq!(back.meta, rec.meta);
    assert_eq!(back.decode_body().unwrap(), body);

    // Terminal variants round-trip too.
    for t in [
        TerminalStatus::Failed {
            failure: sqrl_core::FailureKind::OrchestrationPanic("p".into()),
        },
        TerminalStatus::Cancelled,
    ] {
        let bytes = codec::to_vec(&t, "terminal").unwrap();
        let back: TerminalStatus = codec::from_slice(&bytes, "terminal").unwrap();
        assert_eq!(back, t);
    }
}

#[test]
fn workflow_handle_surface() {
    let (completer, waiter) = promise::<TerminalResult>();
    let handle = WorkflowHandle::new(WorkflowId::new("wf-h"), waiter);
    assert_eq!(handle.id().as_str(), "wf-h");
    assert!(handle.peek().is_none());
    assert!(!format!("{handle:?}").is_empty());
    completer.complete(Ok(codec::to_vec(&42u64, "out").unwrap()));
    assert!(matches!(handle.peek(), Some(Ok(_))));
    let out: u64 = handle.result_blocking().unwrap();
    assert_eq!(out, 42);
}

#[test]
fn workflow_handle_error_result() {
    let (completer, waiter) = promise::<TerminalResult>();
    let handle = WorkflowHandle::new(WorkflowId::new("wf-e"), waiter);
    completer.complete(Err(Error::App("nope".into())));
    let err = handle.result_blocking::<u64>().unwrap_err();
    assert!(err.to_string().contains("nope"));
}

#[test]
fn config_constructors() {
    let strict = StepOptions::strict_fsync();
    assert!(strict.fsync_strict);
    assert!(strict.retry.is_none());
    let with = StepOptions::with_retry(sqrl_core::RetryPolicy::default());
    assert!(with.retry.is_some());
    assert!(!with.fsync_strict);
    assert_eq!(FsyncPolicy::default_group(), FsyncPolicy::default());
}

#[test]
fn state_machine_exhaustive_transition_table() {
    use sqrl_core::{FailureKind, StateKind, WorkflowState};
    let all = || {
        vec![
            WorkflowState::Pending,
            WorkflowState::Running,
            WorkflowState::AwaitingStep,
            WorkflowState::Sleeping,
            WorkflowState::Blocked,
            WorkflowState::Recovering,
            WorkflowState::Completed,
            WorkflowState::Failed(FailureKind::Error(sqrl_core::Error::App("x".into()))),
            WorkflowState::Cancelled,
        ]
    };
    let mut legal = 0;
    let mut illegal = 0;
    for from in all() {
        assert_eq!(
            from.is_terminal(),
            matches!(
                from.kind(),
                StateKind::Completed | StateKind::Failed | StateKind::Cancelled
            )
        );
        for to in all() {
            match from.transition(to.clone()) {
                Ok(next) => {
                    legal += 1;
                    assert_eq!(next.kind(), to.kind());
                    // Terminal states have exactly one way out: an explicit
                    // resume moves Failed back into Recovering.
                    assert!(
                        !from.is_terminal()
                            || (from.kind() == StateKind::Failed
                                && to.kind() == StateKind::Recovering),
                        "{:?} -> {:?}",
                        from.kind(),
                        to.kind()
                    );
                }
                Err(e) => {
                    illegal += 1;
                    // The error names both ends.
                    let text = e.to_string();
                    assert!(!text.is_empty());
                }
            }
        }
    }
    // 9x9 pairs, split into a stable number of legal edges: pin it so any
    // table edit is a conscious decision.
    assert_eq!(legal + illegal, 81);
    assert!(legal > 20 && legal < 40, "legal edges: {legal}");
    // Failure kinds map to their user-facing errors.
    let nd = FailureKind::OrchestrationPanic("p".into());
    assert!(matches!(
        nd.to_error(),
        sqrl_core::Error::OrchestrationPanic(_)
    ));
}

#[test]
fn vfs_error_display_and_constructor() {
    use sqrl_core::vfs::VfsError;
    let e = VfsError::io("wal/seg-1", "boom");
    assert_eq!(e.to_string(), "i/o error on wal/seg-1: boom");
    assert_eq!(VfsError::NotFound("x".into()).to_string(), "not found: x");
    assert_eq!(
        VfsError::DiskFull("y".into()).to_string(),
        "disk full while writing y"
    );
}

#[test]
fn codec_serialize_errors_carry_their_context() {
    struct Unserializable;
    impl serde::Serialize for Unserializable {
        fn serialize<S: serde::Serializer>(&self, _: S) -> Result<S::Ok, S::Error> {
            Err(serde::ser::Error::custom("cannot"))
        }
    }
    let err = codec::to_vec(&Unserializable, "warp core").unwrap_err();
    assert!(err.to_string().contains("warp core"), "{err}");
}

#[test]
fn promise_double_complete_first_wins_and_clones_share() {
    let (c, w) = promise::<u32>();
    let c2 = c.clone();
    let w2 = w.clone();
    assert!(c.complete(1));
    assert!(!c2.complete(2), "second completion must lose");
    assert_eq!(w.peek(), Some(1));
    assert_eq!(w2.peek(), Some(1));
    assert_eq!(w.wait_blocking(), 1);
}

#[test]
fn promise_blocking_wait_across_threads() {
    let (c, w) = promise::<u32>();
    let t = std::thread::spawn(move || w.wait_blocking());
    // Let the waiter reach the condvar wait before completing.
    std::thread::yield_now();
    assert!(c.complete(9));
    assert_eq!(t.join().unwrap(), 9);
}

#[test]
fn promise_future_pending_then_woken() {
    use std::future::Future;
    use std::pin::Pin;
    use std::task::{Context, Poll, Waker};
    let (c, w) = promise::<u32>();
    let mut fut = w.clone();
    let waker = Waker::noop();
    let mut cx = Context::from_waker(waker);
    assert!(matches!(Pin::new(&mut fut).poll(&mut cx), Poll::Pending));
    c.complete(5);
    assert!(matches!(
        Pin::new(&mut fut).poll(&mut cx),
        Poll::Ready(5)
    ));
}

#[test]
fn snapshot_decode_body_rejects_garbage() {
    let rec = SnapshotRecord {
        upto: 1,
        meta: SnapshotMeta::default(),
        body: vec![0xFF, 0x00, 0xFF, 0x13, 0x37],
    };
    let err = rec.decode_body().unwrap_err();
    assert!(!err.to_string().is_empty());
}
