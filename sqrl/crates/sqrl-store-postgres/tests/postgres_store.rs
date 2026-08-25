//! Storage-contract tests for the PostgreSQL backend, mirroring the SQLite
//! backend's suite. **Gated**: they need a real server and are skipped
//! unless `SQRL_POSTGRES_URL` is set (see the crate docs for a one-line
//! docker invocation). Each test run wipes the `sqrl` schema first so runs
//! are independent.

use sqrl_core::event::{JournalEvent, JournalRecord};
use sqrl_core::snapshot::{SnapshotMeta, SnapshotRecord};
use sqrl_core::storage::{AppendEntry, AppendPayload};
use sqrl_core::{LogicalTime, Storage, StorageError, WorkflowId};
use sqrl_store_postgres::PostgresStorage;

fn url() -> Option<String> {
    std::env::var("SQRL_POSTGRES_URL").ok()
}

/// Drop and recreate a clean slate for one test. Serializes tests through
/// postgres itself; `cargo test -p sqrl-store-postgres -- --test-threads=1`
/// is recommended (the tests share one schema).
fn fresh(url: &str) -> PostgresStorage {
    let mut client = postgres::Client::connect(url, postgres::NoTls).expect("connect");
    client
        .batch_execute("DROP SCHEMA IF EXISTS sqrl CASCADE")
        .expect("drop schema");
    PostgresStorage::connect(url, 2).expect("create store")
}

fn record(index: u64) -> JournalRecord {
    JournalRecord {
        index,
        at: LogicalTime::from_millis(index.saturating_mul(10)),
        event: JournalEvent::StepScheduled {
            seq: index,
            name: format!("step-{index}"),
        },
    }
}

fn rec(wf: &str, index: u64) -> AppendEntry {
    AppendEntry {
        workflow: WorkflowId::new(wf),
        payload: AppendPayload::Record(record(index)),
    }
}

fn snap(wf: &str, upto: u64) -> AppendEntry {
    AppendEntry {
        workflow: WorkflowId::new(wf),
        payload: AppendPayload::Snapshot(SnapshotRecord {
            upto,
            meta: SnapshotMeta {
                wf_time: LogicalTime::from_millis(upto),
                ..SnapshotMeta::default()
            },
            body: vec![0xAB, 0xCD, upto as u8],
        }),
    }
}

macro_rules! gated {
    () => {
        match url() {
            Some(u) => u,
            None => {
                eprintln!("SQRL_POSTGRES_URL not set; skipping");
                return;
            }
        }
    };
}

#[test]
fn synced_rows_survive_reopen() {
    let url = gated!();
    let store = fresh(&url);
    {
        let mut shard = store.open_shard(0).unwrap();
        shard
            .append(&(0..20).map(|i| rec("wf-a", i)).collect::<Vec<_>>())
            .unwrap();
        shard.sync().unwrap();
    }
    // A brand-new storage handle (fresh connections): everything synced is
    // there; nothing extra.
    let store2 = PostgresStorage::connect(&url, 0).expect("reopen");
    assert_eq!(store2.num_shards(), 2);
    let mut shard = store2.open_shard(0).unwrap();
    let readout = shard.read(&WorkflowId::new("wf-a")).unwrap();
    assert_eq!(readout.records.len(), 20);
    assert!(readout.snapshot.is_none());
}

#[test]
fn unsynced_rows_visible_on_handle_but_not_durable() {
    let url = gated!();
    let store = fresh(&url);
    let mut shard = store.open_shard(0).unwrap();
    shard
        .append(&(0..5).map(|i| rec("wf-b", i)).collect::<Vec<_>>())
        .unwrap();
    // Visible through the same handle before sync...
    assert_eq!(
        shard.read(&WorkflowId::new("wf-b")).unwrap().records.len(),
        5
    );
    assert_eq!(shard.list().unwrap().len(), 1);
    // ...but a separate handle (fresh connection) sees nothing.
    let mut other = store.open_shard(0).unwrap();
    assert!(matches!(
        other.read(&WorkflowId::new("wf-b")),
        Err(StorageError::UnknownWorkflow(_))
    ));
}

#[test]
fn snapshot_supersedes_and_maintain_prunes() {
    let url = gated!();
    let store = fresh(&url);
    let mut shard = store.open_shard(1).unwrap();
    shard
        .append(&(0..10).map(|i| rec("wf-c", i)).collect::<Vec<_>>())
        .unwrap();
    shard.append(&[snap("wf-c", 8)]).unwrap();
    shard.sync().unwrap();
    let readout = shard.read(&WorkflowId::new("wf-c")).unwrap();
    assert_eq!(readout.snapshot.as_ref().map(|s| s.upto), Some(8));
    assert_eq!(readout.records.len(), 2); // 8 and 9
    shard.maintain().unwrap();
    // Superseded rows are physically gone; the readout is unchanged.
    let readout = shard.read(&WorkflowId::new("wf-c")).unwrap();
    assert_eq!(readout.records.len(), 2);
    assert_eq!(shard.stats().segments_deleted, 8);
}

#[test]
fn unsynced_snapshot_does_not_enable_pruning() {
    let url = gated!();
    let store = fresh(&url);
    let mut shard = store.open_shard(0).unwrap();
    shard
        .append(&(0..6).map(|i| rec("wf-d", i)).collect::<Vec<_>>())
        .unwrap();
    shard.sync().unwrap();
    shard.append(&[snap("wf-d", 6)]).unwrap(); // buffered, unsynced
    shard.maintain().unwrap();
    // All six committed rows must still be there for a fresh handle.
    let mut other = store.open_shard(0).unwrap();
    assert_eq!(
        other.read(&WorkflowId::new("wf-d")).unwrap().records.len(),
        6
    );
}

#[test]
fn shards_are_isolated_and_stored_count_wins() {
    let url = gated!();
    let store = fresh(&url);
    {
        let mut s0 = store.open_shard(0).unwrap();
        s0.append(&[rec("wf-e", 0)]).unwrap();
        s0.sync().unwrap();
    }
    let mut s1 = store.open_shard(1).unwrap();
    assert!(matches!(
        s1.read(&WorkflowId::new("wf-e")),
        Err(StorageError::UnknownWorkflow(_))
    ));
    assert!(s1.list().unwrap().is_empty());
    // Wrong shard count on reopen is refused.
    assert!(matches!(
        PostgresStorage::connect(&url, 5),
        Err(StorageError::Unsupported(_))
    ));
}

#[test]
fn oversized_index_poisons_shard() {
    let url = gated!();
    let store = fresh(&url);
    let mut shard = store.open_shard(0).unwrap();
    let bad = AppendEntry {
        workflow: WorkflowId::new("wf-f"),
        payload: AppendPayload::Record(JournalRecord {
            index: u64::MAX,
            at: LogicalTime::from_millis(0),
            event: JournalEvent::StepScheduled {
                seq: 0,
                name: "x".into(),
            },
        }),
    };
    assert!(shard.append(&[bad]).is_err());
    // Poisoned: further appends and syncs refuse.
    assert!(shard.append(&[rec("wf-f", 0)]).is_err());
    assert!(shard.sync().is_err());
}
