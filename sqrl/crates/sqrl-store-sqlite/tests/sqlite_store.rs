//! Storage-contract tests for the SQLite backend, mirroring the applicable
//! parts of the WAL backend's durability suite (`sqrl-store`'s
//! `wal_recovery.rs`): synced data survives reopen, unsynced buffered data
//! does not, snapshots supersede journal rows, `maintain` only prunes rows
//! covered by a *committed* snapshot, shards are isolated, and the stored
//! shard count wins on reopen.
//!
//! Notes on coverage:
//! * I/O fault injection (torn writes, disk full mid-commit) is not testable
//!   here — SQLite owns the file I/O and there is no `SimDisk` seam. The
//!   poisoning branch is instead exercised through a real append failure
//!   (an index that does not fit SQLite's signed INTEGER).
//! * Engine-level parity is covered by the storage contract itself; these
//!   tests stay at the storage layer (no engine driver dependency).

use sqrl_core::event::{JournalEvent, JournalRecord};
use sqrl_core::snapshot::{SnapshotMeta, SnapshotRecord};
use sqrl_core::storage::{AppendEntry, AppendPayload};
use sqrl_core::{LogicalTime, Storage, StorageError, StorageShard, WorkflowId};
use sqrl_store_sqlite::SqliteStorage;
use std::path::Path;

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

fn snapshot(upto: u64) -> SnapshotRecord {
    SnapshotRecord {
        upto,
        meta: SnapshotMeta {
            wf_time: LogicalTime::from_millis(upto),
            ..SnapshotMeta::default()
        },
        body: vec![0xAB, 0xCD, upto as u8],
    }
}

fn snap(wf: &str, upto: u64) -> AppendEntry {
    AppendEntry {
        workflow: WorkflowId::new(wf),
        payload: AppendPayload::Snapshot(snapshot(upto)),
    }
}

fn open_shard(path: &Path, num_shards: u32, shard: usize) -> Box<dyn StorageShard> {
    let store = SqliteStorage::open(path, num_shards).expect("open store");
    store.open_shard(shard).expect("open shard")
}

#[test]
fn synced_appends_survive_reopen_unsynced_do_not() {
    let dir = tempfile::tempdir().unwrap();
    let path = dir.path().join("store.db");
    {
        let mut shard = open_shard(&path, 1, 0);
        shard
            .append(&(0..50).map(|i| rec("wf-a", i)).collect::<Vec<_>>())
            .unwrap();
        shard.sync().unwrap();
        // Unsynced tail: buffered in memory only.
        shard
            .append(&(50..60).map(|i| rec("wf-a", i)).collect::<Vec<_>>())
            .unwrap();
        // In-process, unsynced appends are visible (WAL/mem parity)...
        let readout = shard.read(&WorkflowId::new("wf-a")).unwrap();
        assert_eq!(readout.records.len(), 60);
    } // dropped without sync
      // ...but they are not durable: a fresh store sees only synced data.
    let mut shard = open_shard(&path, 0, 0);
    let readout = shard.read(&WorkflowId::new("wf-a")).unwrap();
    assert!(readout.snapshot.is_none());
    assert_eq!(readout.records, (0..50).map(record).collect::<Vec<_>>());
}

#[test]
fn snapshot_supersedes_and_maintain_prunes() {
    let dir = tempfile::tempdir().unwrap();
    let path = dir.path().join("store.db");
    let wf = WorkflowId::new("wf-a");
    let mut shard = open_shard(&path, 1, 0);
    shard
        .append(&(0..100).map(|i| rec("wf-a", i)).collect::<Vec<_>>())
        .unwrap();
    shard.append(&[snap("wf-a", 60)]).unwrap();
    shard.sync().unwrap();

    let readout = shard.read(&wf).unwrap();
    assert_eq!(readout.snapshot, Some(snapshot(60)));
    assert_eq!(readout.records, (60..100).map(record).collect::<Vec<_>>());

    // maintain deletes exactly the superseded rows (idx < 60).
    shard.maintain().unwrap();
    assert_eq!(shard.stats().segments_deleted, 60);
    let readout = shard.read(&wf).unwrap();
    assert_eq!(readout.snapshot.as_ref().map(|s| s.upto), Some(60));
    assert_eq!(readout.records.len(), 40);

    // A newer snapshot replaces the old one (latest-only), and maintain
    // prunes the newly-covered rows.
    shard.append(&[snap("wf-a", 80)]).unwrap();
    shard.sync().unwrap();
    shard.maintain().unwrap();
    assert_eq!(shard.stats().segments_deleted, 80);
    let readout = shard.read(&wf).unwrap();
    assert_eq!(readout.snapshot, Some(snapshot(80)));
    assert_eq!(readout.records, (80..100).map(record).collect::<Vec<_>>());

    // Reopen: still consistent.
    drop(shard);
    let mut shard = open_shard(&path, 0, 0);
    let readout = shard.read(&wf).unwrap();
    assert_eq!(readout.snapshot, Some(snapshot(80)));
    assert_eq!(readout.records, (80..100).map(record).collect::<Vec<_>>());
    // Nothing left to prune on the fresh handle.
    shard.maintain().unwrap();
    assert_eq!(shard.stats().segments_deleted, 0);
}

#[test]
fn unsynced_snapshot_does_not_enable_gc() {
    let dir = tempfile::tempdir().unwrap();
    let path = dir.path().join("store.db");
    let wf = WorkflowId::new("wf-a");
    let mut shard = open_shard(&path, 1, 0);
    shard
        .append(&(0..100).map(|i| rec("wf-a", i)).collect::<Vec<_>>())
        .unwrap();
    shard.sync().unwrap();
    // Snapshot appended but NOT synced: it must not free any journal rows.
    shard.append(&[snap("wf-a", 100)]).unwrap();
    shard.maintain().unwrap();
    assert_eq!(shard.stats().segments_deleted, 0);
    // The unsynced snapshot is visible in-process...
    let readout = shard.read(&wf).unwrap();
    assert_eq!(readout.snapshot.as_ref().map(|s| s.upto), Some(100));
    assert!(readout.records.is_empty());
    // ...but after "crash" (drop without sync) the journal is intact and the
    // snapshot is gone.
    drop(shard);
    let mut shard = open_shard(&path, 0, 0);
    let readout = shard.read(&wf).unwrap();
    assert!(readout.snapshot.is_none());
    assert_eq!(readout.records.len(), 100);
}

#[test]
fn multi_workflow_multi_shard_isolation() {
    let dir = tempfile::tempdir().unwrap();
    let path = dir.path().join("store.db");
    {
        let store = SqliteStorage::open(&path, 2).unwrap();
        assert_eq!(store.num_shards(), 2);
        let mut s0 = store.open_shard(0).unwrap();
        let mut s1 = store.open_shard(1).unwrap();
        let mut entries = Vec::new();
        for i in 0..10 {
            entries.push(rec("wf-a", i));
            if i < 5 {
                entries.push(rec("wf-b", i));
            }
        }
        s0.append(&entries).unwrap();
        s0.sync().unwrap();
        s1.append(&(0..7).map(|i| rec("wf-c", i)).collect::<Vec<_>>())
            .unwrap();
        s1.sync().unwrap();

        assert_eq!(
            s0.list().unwrap(),
            vec![WorkflowId::new("wf-a"), WorkflowId::new("wf-b")]
        );
        assert_eq!(s1.list().unwrap(), vec![WorkflowId::new("wf-c")]);
        // Shard filtering is defense in depth: another shard's workflow is
        // unknown here.
        assert!(matches!(
            s0.read(&WorkflowId::new("wf-c")),
            Err(StorageError::UnknownWorkflow(_))
        ));
        assert!(matches!(
            s1.read(&WorkflowId::new("wf-a")),
            Err(StorageError::UnknownWorkflow(_))
        ));
        assert_eq!(s0.read(&WorkflowId::new("wf-a")).unwrap().records.len(), 10);
        assert_eq!(s0.read(&WorkflowId::new("wf-b")).unwrap().records.len(), 5);
    }
    // Reopen (stored shard count) and confirm placement survived.
    let store = SqliteStorage::open(&path, 0).unwrap();
    assert_eq!(store.num_shards(), 2);
    let mut s1 = store.open_shard(1).unwrap();
    assert_eq!(
        s1.read(&WorkflowId::new("wf-c")).unwrap().records,
        (0..7).map(record).collect::<Vec<_>>()
    );
}

#[test]
fn unknown_workflow_errors() {
    let dir = tempfile::tempdir().unwrap();
    let path = dir.path().join("store.db");
    let mut shard = open_shard(&path, 1, 0);
    assert!(shard.list().unwrap().is_empty());
    match shard.read(&WorkflowId::new("nope")) {
        Err(StorageError::UnknownWorkflow(id)) => assert_eq!(id, "nope"),
        other => panic!("expected UnknownWorkflow, got {other:?}"),
    }
}

#[test]
fn stored_num_shards_wins_and_mismatch_is_rejected() {
    let dir = tempfile::tempdir().unwrap();
    let path = dir.path().join("store.db");
    {
        let store = SqliteStorage::open(&path, 3).unwrap();
        assert_eq!(store.num_shards(), 3);
    }
    // 0 = "use stored"; the exact stored value is also accepted.
    assert_eq!(SqliteStorage::open(&path, 0).unwrap().num_shards(), 3);
    let store = SqliteStorage::open(&path, 3).unwrap();
    assert_eq!(store.num_shards(), 3);
    // Any other nonzero value is a contract violation.
    match SqliteStorage::open(&path, 2) {
        Err(StorageError::Unsupported(_)) => {}
        other => panic!("expected Unsupported, got {other:?}"),
    }
    // Out-of-range shard index.
    match store.open_shard(3) {
        Err(StorageError::Unsupported(_)) => {}
        Err(other) => panic!("expected Unsupported, got {other:?}"),
        Ok(_) => panic!("expected Unsupported, got a shard"),
    }
}

#[test]
fn double_open_same_store_works() {
    // Two `SqliteStorage` values over the same file coexist (WAL mode +
    // busy_timeout); real fault-injected poisoning is not testable here, so
    // this covers the "store stays usable from a second handle" half.
    let dir = tempfile::tempdir().unwrap();
    let path = dir.path().join("store.db");
    let store1 = SqliteStorage::open(&path, 1).unwrap();
    let store2 = SqliteStorage::open(&path, 0).unwrap();
    let mut a = store1.open_shard(0).unwrap();
    let mut b = store2.open_shard(0).unwrap();
    a.append(&(0..10).map(|i| rec("wf-a", i)).collect::<Vec<_>>())
        .unwrap();
    a.sync().unwrap();
    assert_eq!(b.read(&WorkflowId::new("wf-a")).unwrap().records.len(), 10);
    b.append(&(0..3).map(|i| rec("wf-b", i)).collect::<Vec<_>>())
        .unwrap();
    b.sync().unwrap();
    assert_eq!(
        a.list().unwrap(),
        vec![WorkflowId::new("wf-a"), WorkflowId::new("wf-b")]
    );
}

#[test]
fn failed_append_poisons_shard() {
    // A record index above i64::MAX cannot be stored in an INTEGER column;
    // the append is rejected and the shard is poisoned, mirroring WalShard.
    let dir = tempfile::tempdir().unwrap();
    let path = dir.path().join("store.db");
    let mut shard = open_shard(&path, 1, 0);
    shard.append(&[rec("wf-a", 0)]).unwrap();
    shard.sync().unwrap();
    match shard.append(&[rec("wf-a", u64::MAX)]) {
        Err(StorageError::Unsupported(_)) => {}
        other => panic!("expected Unsupported, got {other:?}"),
    }
    // Poisoned: subsequent appends and syncs fail fast with the stored error.
    assert!(shard.append(&[rec("wf-a", 1)]).is_err());
    assert!(shard.sync().is_err());
    // Reads still work on a poisoned shard, and a fresh store handle over the
    // same file is unaffected.
    assert_eq!(
        shard.read(&WorkflowId::new("wf-a")).unwrap().records.len(),
        1
    );
    let mut fresh = open_shard(&path, 0, 0);
    fresh.append(&[rec("wf-a", 1)]).unwrap();
    fresh.sync().unwrap();
    assert_eq!(
        fresh.read(&WorkflowId::new("wf-a")).unwrap().records.len(),
        2
    );
}

#[test]
fn stats_counters_map_as_documented() {
    let dir = tempfile::tempdir().unwrap();
    let path = dir.path().join("store.db");
    let mut shard = open_shard(&path, 1, 0);
    let stats = shard.stats();
    assert_eq!(stats, Default::default());

    shard
        .append(&(0..10).map(|i| rec("wf-a", i)).collect::<Vec<_>>())
        .unwrap();
    assert_eq!(shard.stats().records_appended, 10);
    assert_eq!(shard.stats().fsyncs, 0);
    shard.sync().unwrap();
    let stats = shard.stats();
    assert_eq!(stats.fsyncs, 1);
    assert!(stats.bytes_written > 0);

    // An empty sync is a no-op barrier: no commit, no fsync counted.
    shard.sync().unwrap();
    assert_eq!(shard.stats().fsyncs, 1);

    shard.append(&[snap("wf-a", 10)]).unwrap();
    shard.sync().unwrap();
    let stats = shard.stats();
    assert_eq!(stats.records_appended, 11);
    assert_eq!(stats.fsyncs, 2);

    shard.maintain().unwrap();
    let stats = shard.stats();
    assert_eq!(stats.segments_deleted, 10);
    assert_eq!(stats.live_segments, 0);
}
