//! Contract coverage for `MemoryStorage`, the in-memory test backend: the
//! same read/list/maintain/snapshot semantics the durable backends honor.

use sqrl_core::event::{JournalEvent, JournalRecord};
use sqrl_core::snapshot::{SnapshotMeta, SnapshotRecord};
use sqrl_core::storage::{AppendEntry, AppendPayload};
use sqrl_core::{LogicalTime, Storage, StorageError, WorkflowId};
use sqrl_store::MemoryStorage;

fn rec(wf: &str, index: u64) -> AppendEntry {
    AppendEntry {
        workflow: WorkflowId::new(wf),
        payload: AppendPayload::Record(JournalRecord {
            index,
            at: LogicalTime::from_millis(index),
            event: JournalEvent::StepScheduled {
                seq: index,
                name: format!("s{index}"),
            },
        }),
    }
}

fn snap(wf: &str, upto: u64) -> AppendEntry {
    AppendEntry {
        workflow: WorkflowId::new(wf),
        payload: AppendPayload::Snapshot(SnapshotRecord {
            upto,
            meta: SnapshotMeta::default(),
            body: vec![1, 2, 3],
        }),
    }
}

#[test]
fn append_read_list_roundtrip_and_sharing() {
    let store = MemoryStorage::new(2);
    let mut s0 = store.open_shard(0).unwrap();
    s0.append(&[rec("a", 0), rec("a", 1), rec("b", 0)]).unwrap();
    s0.sync().unwrap();
    // Clones share state: a second handle over the same store sees it all.
    let mut s0b = store.clone().open_shard(0).unwrap();
    assert_eq!(s0b.read(&WorkflowId::new("a")).unwrap().records.len(), 2);
    assert_eq!(
        s0b.list().unwrap(),
        vec![WorkflowId::new("a"), WorkflowId::new("b")]
    );
    assert!(matches!(
        s0b.read(&WorkflowId::new("zz")),
        Err(StorageError::UnknownWorkflow(_))
    ));
    let stats = s0.stats();
    assert_eq!(stats.records_appended, 3);
    assert_eq!(stats.fsyncs, 1);
    // Out-of-range shard is refused.
    assert!(store.open_shard(2).is_err());
}

#[test]
fn snapshot_cuts_reads_and_maintain_prunes() {
    let store = MemoryStorage::new(1);
    let mut shard = store.open_shard(0).unwrap();
    shard
        .append(&(0..10).map(|i| rec("wf", i)).collect::<Vec<_>>())
        .unwrap();
    shard.append(&[snap("wf", 7)]).unwrap();
    let readout = shard.read(&WorkflowId::new("wf")).unwrap();
    assert_eq!(readout.snapshot.as_ref().map(|s| s.upto), Some(7));
    assert_eq!(readout.records.len(), 3); // 7, 8, 9
    shard.maintain().unwrap();
    let readout = shard.read(&WorkflowId::new("wf")).unwrap();
    assert_eq!(readout.records.len(), 3);
    // Snapshot-only workflows still list and read.
    shard.append(&[snap("ghost", 4)]).unwrap();
    assert!(shard.list().unwrap().contains(&WorkflowId::new("ghost")));
    let ghost = shard.read(&WorkflowId::new("ghost")).unwrap();
    assert!(ghost.records.is_empty());
    assert_eq!(ghost.snapshot.map(|s| s.upto), Some(4));
}
