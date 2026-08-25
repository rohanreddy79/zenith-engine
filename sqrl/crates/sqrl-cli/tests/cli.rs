//! Integration tests: run the built `sqrl` binary against stores seeded
//! directly through the sqrl-store API.

use sqrl_core::storage::{AppendEntry, AppendPayload, JournalReadout};
use sqrl_core::{JournalEvent, JournalRecord, LogicalTime, StepError, Storage, WorkflowId};
use sqrl_store::WalStorage;
use std::path::Path;
use std::process::{Command, Output};

const BIN: &str = env!("CARGO_BIN_EXE_sqrl");

fn sqrl(dir: &Path, args: &[&str]) -> Output {
    Command::new(BIN)
        .arg("--data")
        .arg(dir)
        .args(args)
        .output()
        .expect("failed to run sqrl binary")
}

fn stdout(out: &Output) -> String {
    String::from_utf8_lossy(&out.stdout).into_owned()
}

fn stderr(out: &Output) -> String {
    String::from_utf8_lossy(&out.stderr).into_owned()
}

fn entry(id: &str, index: u64, at_ms: u64, event: JournalEvent) -> AppendEntry {
    AppendEntry {
        workflow: WorkflowId::new(id),
        payload: AppendPayload::Record(JournalRecord {
            index,
            at: LogicalTime::from_millis(at_ms),
            event,
        }),
    }
}

fn started(input: &[u8], seed: u64) -> JournalEvent {
    JournalEvent::WorkflowStarted {
        name: "demo".into(),
        version: 1,
        input: input.to_vec(),
        seed,
    }
}

/// Seed a single-shard store with:
/// * `wf-signal` — started, one completed step, awaiting a signal (idle),
/// * `wf-failed` — started, one finally-failed step, WorkflowFailed.
fn seed_store(dir: &Path) {
    let storage = WalStorage::open(dir).expect("open store");
    let mut shard = storage.open_shard(0).expect("open shard");
    let input = sqrl_core::codec::to_vec(&serde_json::json!({"n": 1}), "input").expect("encode");
    let entries = vec![
        entry("wf-signal", 0, 100, started(&input, 7)),
        entry(
            "wf-signal",
            1,
            100,
            JournalEvent::StepScheduled {
                seq: 0,
                name: "step-a".into(),
            },
        ),
        entry(
            "wf-signal",
            2,
            150,
            JournalEvent::StepCompleted {
                seq: 0,
                result: input.clone(),
            },
        ),
        entry(
            "wf-signal",
            3,
            150,
            JournalEvent::SignalAwaited {
                seq: 1,
                name: "go".into(),
            },
        ),
        entry("wf-failed", 0, 100, started(&input, 8)),
        entry(
            "wf-failed",
            1,
            100,
            JournalEvent::StepScheduled {
                seq: 0,
                name: "boom".into(),
            },
        ),
        entry(
            "wf-failed",
            2,
            200,
            JournalEvent::StepFailed {
                seq: 0,
                error: StepError::App("boom".into()),
                attempt: 1,
                retry_at: None,
            },
        ),
        entry(
            "wf-failed",
            3,
            200,
            JournalEvent::WorkflowFailed {
                error: sqrl_core::Error::App("boom".into()),
            },
        ),
    ];
    shard.append(&entries).expect("append");
    shard.sync().expect("sync");
}

fn read_journal(dir: &Path, id: &str) -> JournalReadout {
    let storage = WalStorage::open(dir).expect("open store");
    let mut shard = storage.open_shard(0).expect("open shard");
    shard.read(&WorkflowId::new(id)).expect("read journal")
}

fn state_of(json: &serde_json::Value, id: &str) -> String {
    json.as_array()
        .expect("status JSON is an array")
        .iter()
        .find(|row| row["id"] == id)
        .unwrap_or_else(|| panic!("workflow {id} missing from status"))["state"]
        .as_str()
        .expect("state is a string")
        .to_string()
}

#[test]
fn status_reports_derived_states() {
    let tmp = tempfile::tempdir().expect("tempdir");
    seed_store(tmp.path());

    let out = sqrl(tmp.path(), &["status", "--json"]);
    assert!(out.status.success(), "stderr: {}", stderr(&out));
    let json: serde_json::Value = serde_json::from_str(&stdout(&out)).expect("valid JSON");
    assert_eq!(state_of(&json, "wf-signal"), "idle");
    assert_eq!(state_of(&json, "wf-failed"), "failed");

    // Human table lists both ids.
    let out = sqrl(tmp.path(), &["status"]);
    assert!(out.status.success());
    let text = stdout(&out);
    assert!(text.contains("wf-signal"), "table output: {text}");
    assert!(text.contains("wf-failed"), "table output: {text}");
    assert!(text.contains("blocked/idle"), "table output: {text}");
}

#[test]
fn inspect_prints_event_kinds_and_payloads() {
    let tmp = tempfile::tempdir().expect("tempdir");
    seed_store(tmp.path());

    let out = sqrl(tmp.path(), &["inspect", "wf-signal"]);
    assert!(out.status.success(), "stderr: {}", stderr(&out));
    let text = stdout(&out);
    for kind in [
        "WorkflowStarted",
        "StepScheduled",
        "StepCompleted",
        "SignalAwaited",
    ] {
        assert!(text.contains(kind), "missing {kind} in: {text}");
    }
    // MessagePack payloads decode to JSON for display.
    assert!(text.contains("{\"n\":1}"), "payload not decoded: {text}");

    let out = sqrl(tmp.path(), &["inspect", "wf-signal", "--json"]);
    assert!(out.status.success());
    let json: serde_json::Value = serde_json::from_str(&stdout(&out)).expect("valid JSON");
    assert_eq!(json["records"][0]["kind"], "WorkflowStarted");
    assert_eq!(json["records"][0]["fields"]["input"]["n"], 1);

    // --limit shows only the tail.
    let out = sqrl(tmp.path(), &["inspect", "wf-signal", "--limit", "1"]);
    let text = stdout(&out);
    assert!(!text.contains("WorkflowStarted"), "limit ignored: {text}");
    assert!(text.contains("SignalAwaited"), "tail missing: {text}");
}

#[test]
fn signal_round_trips_through_the_journal() {
    let tmp = tempfile::tempdir().expect("tempdir");
    seed_store(tmp.path());

    let out = sqrl(
        tmp.path(),
        &["signal", "wf-signal", "go", r#"{"approved":true}"#],
    );
    assert!(out.status.success(), "stderr: {}", stderr(&out));

    let readout = read_journal(tmp.path(), "wf-signal");
    assert_eq!(readout.records.len(), 5);
    let last = readout.records.last().expect("has records");
    assert_eq!(last.index, 4);
    // Logical time is reused from the previous record (no wall clock).
    assert_eq!(last.at, LogicalTime::from_millis(150));
    match &last.event {
        JournalEvent::SignalReceived { name, payload } => {
            assert_eq!(name, "go");
            let value: serde_json::Value =
                sqrl_core::codec::from_slice(payload, "payload").expect("decode payload");
            assert_eq!(value, serde_json::json!({"approved": true}));
        }
        other => panic!("expected SignalReceived, got {other:?}"),
    }
}

#[test]
fn signal_refused_on_terminal_workflow() {
    let tmp = tempfile::tempdir().expect("tempdir");
    seed_store(tmp.path());

    let out = sqrl(tmp.path(), &["signal", "wf-failed", "go", "{}"]);
    assert!(!out.status.success(), "signal on terminal must fail");
    assert!(
        stderr(&out).contains("terminal"),
        "stderr: {}",
        stderr(&out)
    );
    // Journal unchanged.
    assert_eq!(read_journal(tmp.path(), "wf-failed").records.len(), 4);
}

#[test]
fn cancel_appends_then_refuses_when_terminal() {
    let tmp = tempfile::tempdir().expect("tempdir");
    seed_store(tmp.path());

    let out = sqrl(tmp.path(), &["cancel", "wf-signal"]);
    assert!(out.status.success(), "stderr: {}", stderr(&out));
    let readout = read_journal(tmp.path(), "wf-signal");
    let last = readout.records.last().expect("has records");
    assert_eq!(last.index, 4);
    assert!(matches!(last.event, JournalEvent::WorkflowCancelled));

    // Now terminal: a second cancel is refused.
    let out = sqrl(tmp.path(), &["cancel", "wf-signal"]);
    assert!(!out.status.success());
    assert!(
        stderr(&out).contains("terminal"),
        "stderr: {}",
        stderr(&out)
    );
}

#[test]
fn resume_works_only_on_failed_workflows() {
    let tmp = tempfile::tempdir().expect("tempdir");
    seed_store(tmp.path());

    // Not failed: refused.
    let out = sqrl(tmp.path(), &["resume", "wf-signal"]);
    assert!(!out.status.success(), "resume on non-failed must fail");
    assert!(
        stderr(&out).contains("not Failed"),
        "stderr: {}",
        stderr(&out)
    );

    // Failed: allowed.
    let out = sqrl(tmp.path(), &["resume", "wf-failed"]);
    assert!(out.status.success(), "stderr: {}", stderr(&out));
    let readout = read_journal(tmp.path(), "wf-failed");
    let last = readout.records.last().expect("has records");
    assert_eq!(last.index, 4);
    assert!(matches!(last.event, JournalEvent::WorkflowResumed));

    // The failed step is in flight again.
    let out = sqrl(tmp.path(), &["status", "--json"]);
    let json: serde_json::Value = serde_json::from_str(&stdout(&out)).expect("valid JSON");
    assert_eq!(state_of(&json, "wf-failed"), "in-flight");
}

#[test]
fn fork_copies_a_full_prefix() {
    let tmp = tempfile::tempdir().expect("tempdir");
    seed_store(tmp.path());

    let out = sqrl(
        tmp.path(),
        &[
            "fork",
            "wf-signal",
            "--from-index",
            "2",
            "--new-id",
            "wf-fork",
        ],
    );
    assert!(out.status.success(), "stderr: {}", stderr(&out));
    assert!(
        stdout(&out).contains("copied 2 record(s)"),
        "stdout: {}",
        stdout(&out)
    );

    let readout = read_journal(tmp.path(), "wf-fork");
    assert!(readout.snapshot.is_none());
    assert_eq!(readout.records.len(), 2);
    assert_eq!(readout.records[0].index, 0);
    assert_eq!(readout.records[1].index, 1);
    assert!(matches!(
        readout.records[0].event,
        JournalEvent::WorkflowStarted { .. }
    ));

    // Refuses to overwrite an existing workflow.
    let out = sqrl(
        tmp.path(),
        &[
            "fork",
            "wf-signal",
            "--from-index",
            "2",
            "--new-id",
            "wf-fork",
        ],
    );
    assert!(!out.status.success());
    assert!(
        stderr(&out).contains("already exists"),
        "stderr: {}",
        stderr(&out)
    );
}

#[test]
fn compact_exits_cleanly() {
    let tmp = tempfile::tempdir().expect("tempdir");
    seed_store(tmp.path());

    let out = sqrl(tmp.path(), &["compact"]);
    assert!(out.status.success(), "stderr: {}", stderr(&out));
    assert!(
        stdout(&out).contains("live_segments"),
        "stdout: {}",
        stdout(&out)
    );
}

#[test]
fn replay_passes_then_flags_an_index_gap() {
    let tmp = tempfile::tempdir().expect("tempdir");
    seed_store(tmp.path());

    let out = sqrl(tmp.path(), &["replay"]);
    assert!(out.status.success(), "stderr: {}", stderr(&out));
    let text = stdout(&out);
    assert!(text.contains("wf-signal: OK"), "stdout: {text}");
    assert!(text.contains("wf-failed: OK"), "stdout: {text}");

    // Corrupt a third workflow: StepCompleted appended with an index gap.
    {
        let storage = WalStorage::open(tmp.path()).expect("open store");
        let mut shard = storage.open_shard(0).expect("open shard");
        let input =
            sqrl_core::codec::to_vec(&serde_json::json!({"n": 3}), "input").expect("encode");
        let entries = vec![
            entry("wf-corrupt", 0, 100, started(&input, 9)),
            entry(
                "wf-corrupt",
                1,
                100,
                JournalEvent::StepScheduled {
                    seq: 0,
                    name: "step".into(),
                },
            ),
            // Gap: index jumps from 1 to 5.
            entry(
                "wf-corrupt",
                5,
                120,
                JournalEvent::StepCompleted {
                    seq: 0,
                    result: input.clone(),
                },
            ),
        ];
        shard.append(&entries).expect("append");
        shard.sync().expect("sync");
    }

    let out = sqrl(tmp.path(), &["replay"]);
    assert!(!out.status.success(), "replay must fail on the gap");
    let text = stdout(&out);
    assert!(text.contains("wf-corrupt: VIOLATION"), "stdout: {text}");
    assert!(text.contains("expected #2, found #5"), "stdout: {text}");

    // Scoped to a clean workflow, replay still passes.
    let out = sqrl(tmp.path(), &["replay", "--id", "wf-signal"]);
    assert!(out.status.success(), "stderr: {}", stderr(&out));
}

#[test]
fn bench_reports_throughput() {
    let tmp = tempfile::tempdir().expect("tempdir");

    let out = sqrl(tmp.path(), &["bench", "--workflows", "4", "--steps", "2"]);
    assert!(out.status.success(), "stderr: {}", stderr(&out));
    let text = stdout(&out);
    assert!(text.contains("records/s"), "stdout: {text}");
    assert!(text.contains("bytes written"), "stdout: {text}");

    // The synthetic journals are structurally valid.
    let out = sqrl(tmp.path(), &["replay"]);
    assert!(out.status.success(), "stderr: {}", stderr(&out));
}
