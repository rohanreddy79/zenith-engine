//! WAL durability tests on the fault-injecting `SimDisk` plus a real-disk
//! round trip. These pin the property everything else rests on: **synced
//! data survives any crash; recovery truncates cleanly at corruption**.

use sqrl_core::event::{JournalEvent, JournalRecord};
use sqrl_core::snapshot::{SnapshotMeta, SnapshotRecord};
use sqrl_core::storage::{AppendEntry, AppendPayload};
use sqrl_core::{LogicalTime, Storage, StorageError, StorageShard, WorkflowId};
use sqrl_sim::{FaultConfig, SimDisk};
use sqrl_store::{WalOptions, WalStorage};
use std::sync::Arc;

fn rec(wf: &str, index: u64) -> AppendEntry {
    AppendEntry {
        workflow: WorkflowId::new(wf),
        payload: AppendPayload::Record(JournalRecord {
            index,
            at: LogicalTime::from_millis(index * 10),
            event: JournalEvent::StepScheduled {
                seq: index,
                name: format!("step-{index}"),
            },
        }),
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
            body: Vec::new(),
        }),
    }
}

fn open_shard(disk: &SimDisk, opts: WalOptions) -> Box<dyn StorageShard> {
    let store = WalStorage::open_with(Arc::new(disk.clone()), opts).expect("open store");
    store.open_shard(0).expect("open shard")
}

fn small_segments() -> WalOptions {
    WalOptions {
        num_shards: 1,
        segment_size: 2048,
    }
}

#[test]
fn synced_appends_survive_crash() {
    let disk = SimDisk::new(1);
    {
        let mut shard = open_shard(&disk, WalOptions::default());
        shard
            .append(&(0..50).map(|i| rec("wf-a", i)).collect::<Vec<_>>())
            .unwrap();
        shard.sync().unwrap();
    }
    disk.crash();
    disk.recover();
    let mut shard = open_shard(&disk, WalOptions::default());
    let readout = shard.read(&WorkflowId::new("wf-a")).unwrap();
    assert_eq!(readout.records.len(), 50);
    assert_eq!(readout.records[49].index, 49);
    assert!(readout.snapshot.is_none());
}

#[test]
fn unsynced_tail_may_be_lost_but_prefix_survives() {
    for seed in 0..25 {
        let disk = SimDisk::new(seed);
        {
            let mut shard = open_shard(&disk, WalOptions::default());
            shard
                .append(&(0..10).map(|i| rec("wf-a", i)).collect::<Vec<_>>())
                .unwrap();
            shard.sync().unwrap();
            // Unsynced tail: may vanish or tear on crash.
            shard
                .append(&(10..20).map(|i| rec("wf-a", i)).collect::<Vec<_>>())
                .unwrap();
        }
        disk.crash();
        disk.recover();
        let mut shard = open_shard(&disk, WalOptions::default());
        let readout = shard.read(&WorkflowId::new("wf-a")).unwrap();
        let n = readout.records.len();
        assert!(
            (10..=20).contains(&n),
            "seed {seed}: synced prefix must survive, got {n} records"
        );
        // Whatever survived must be a dense prefix.
        for (i, r) in readout.records.iter().enumerate() {
            assert_eq!(r.index, i as u64, "seed {seed}: prefix must be dense");
        }
    }
}

#[test]
fn corruption_truncates_and_reports_offset() {
    let disk = SimDisk::new(2);
    {
        let mut shard = open_shard(&disk, WalOptions::default());
        shard
            .append(&(0..30).map(|i| rec("wf-a", i)).collect::<Vec<_>>())
            .unwrap();
        shard.sync().unwrap();
    }
    // Flip a byte mid-file (in durable content).
    let path = "shard-0/wal-00000000000000000001.sqrl";
    let len = disk.durable_len(path).expect("segment exists");
    disk.corrupt(path, len / 2, 0xA5).unwrap();

    let mut shard = open_shard(&disk, WalOptions::default());
    let readout = shard.read(&WorkflowId::new("wf-a")).unwrap();
    let n = readout.records.len();
    assert!(n < 30, "corruption must drop the tail");
    for (i, r) in readout.records.iter().enumerate() {
        assert_eq!(r.index, i as u64, "surviving prefix must be dense");
    }
    // The store remains writable: resume appending from the valid prefix.
    shard.append(&[rec("wf-a", n as u64)]).unwrap();
    shard.sync().unwrap();
    let readout2 = shard.read(&WorkflowId::new("wf-a")).unwrap();
    assert_eq!(readout2.records.len(), n + 1);
}

#[test]
fn segments_roll_and_reads_span_them() {
    let disk = SimDisk::new(3);
    let mut shard = open_shard(&disk, small_segments());
    shard
        .append(&(0..200).map(|i| rec("wf-a", i)).collect::<Vec<_>>())
        .unwrap();
    shard.sync().unwrap();
    let stats = shard.stats();
    assert!(
        stats.live_segments > 1,
        "2KiB segments must have rolled: {stats:?}"
    );
    let readout = shard.read(&WorkflowId::new("wf-a")).unwrap();
    assert_eq!(readout.records.len(), 200);
    // And recovery across many segments works too.
    drop(shard);
    let mut shard = open_shard(&disk, small_segments());
    let readout = shard.read(&WorkflowId::new("wf-a")).unwrap();
    assert_eq!(readout.records.len(), 200);
}

#[test]
fn snapshot_prunes_reads_and_gc_reclaims_segments() {
    let disk = SimDisk::new(4);
    let mut shard = open_shard(&disk, small_segments());
    shard
        .append(&(0..300).map(|i| rec("wf-a", i)).collect::<Vec<_>>())
        .unwrap();
    shard.sync().unwrap();
    let before = shard.stats().live_segments;
    assert!(before > 2);
    // Snapshot covering everything, synced, then GC.
    shard.append(&[snap("wf-a", 300)]).unwrap();
    shard.sync().unwrap();
    shard.maintain().unwrap();
    let stats = shard.stats();
    assert!(
        stats.live_segments < before,
        "GC must reclaim covered segments: before={before} after={}",
        stats.live_segments
    );
    assert!(stats.segments_deleted > 0);
    let readout = shard.read(&WorkflowId::new("wf-a")).unwrap();
    assert_eq!(readout.snapshot.as_ref().map(|s| s.upto), Some(300));
    assert!(readout.records.is_empty());
    // Restart and confirm the store is still consistent.
    drop(shard);
    let mut shard = open_shard(&disk, small_segments());
    let readout = shard.read(&WorkflowId::new("wf-a")).unwrap();
    assert_eq!(readout.snapshot.as_ref().map(|s| s.upto), Some(300));
    shard.append(&[rec("wf-a", 300)]).unwrap();
    shard.sync().unwrap();
}

#[test]
fn unsynced_snapshot_does_not_enable_gc() {
    let disk = SimDisk::new(5);
    let mut shard = open_shard(&disk, small_segments());
    shard
        .append(&(0..300).map(|i| rec("wf-a", i)).collect::<Vec<_>>())
        .unwrap();
    shard.sync().unwrap();
    let before = shard.stats().live_segments;
    shard.append(&[snap("wf-a", 300)]).unwrap();
    // NO sync: the snapshot is not durable, so nothing may be reclaimed.
    shard.maintain().unwrap();
    assert_eq!(shard.stats().segments_deleted, 0);
    assert_eq!(shard.stats().live_segments, before);
}

#[test]
fn crash_at_every_op_never_loses_synced_data() {
    // Sweep crash points across the entire append/sync/roll/GC sequence.
    // After each crash+recovery, everything acknowledged by a successful
    // sync() before the crash must still be readable.
    let mut explored = 0u64;
    for crash_at in 1..120 {
        let disk = SimDisk::new(1000 + crash_at);
        let mut acked: u64 = 0; // records acknowledged durable
        {
            let mut shard = open_shard(&disk, small_segments());
            disk.crash_after_ops(crash_at);
            'outer: for batch in 0..20u64 {
                let entries: Vec<AppendEntry> = (batch * 10..batch * 10 + 10)
                    .map(|i| rec("wf-a", i))
                    .collect();
                if shard.append(&entries).is_err() {
                    break 'outer;
                }
                if shard.sync().is_err() {
                    break 'outer;
                }
                acked = batch * 10 + 10;
            }
        }
        if !disk.is_crashed() {
            continue; // crash point beyond the workload
        }
        explored += 1;
        disk.recover();
        let mut shard = open_shard(&disk, small_segments());
        if acked == 0 {
            continue;
        }
        let readout = shard
            .read(&WorkflowId::new("wf-a"))
            .expect("acked data must be present");
        assert!(
            readout.records.len() as u64 >= acked,
            "crash_at={crash_at}: {} < acked {acked}",
            readout.records.len()
        );
        for (i, r) in readout.records.iter().enumerate() {
            assert_eq!(r.index, i as u64, "crash_at={crash_at}: dense prefix");
        }
    }
    assert!(
        explored > 50,
        "crash sweep must actually explore ({explored})"
    );
}

#[test]
fn disk_full_surfaces_and_poisons() {
    let cfg = FaultConfig {
        capacity: Some(4096),
        ..FaultConfig::default()
    };
    let disk = SimDisk::with_faults(6, cfg);
    let mut shard = open_shard(&disk, WalOptions::default());
    let mut saw_full = false;
    for batch in 0..100u64 {
        let entries: Vec<AppendEntry> = (batch * 10..batch * 10 + 10)
            .map(|i| rec("wf-a", i))
            .collect();
        match shard.append(&entries) {
            Ok(()) => {}
            Err(StorageError::DiskFull(_)) => {
                saw_full = true;
                break;
            }
            Err(other) => panic!("expected DiskFull, got {other}"),
        }
    }
    assert!(saw_full, "capacity limit must trip");
    // Poisoned: subsequent appends fail fast, never silently succeed.
    assert!(shard.append(&[rec("wf-a", 9999)]).is_err());
    assert!(shard.sync().is_err());
}

#[test]
fn multiple_workflows_interleaved() {
    let disk = SimDisk::new(7);
    let mut shard = open_shard(&disk, small_segments());
    let mut entries = Vec::new();
    for i in 0..50u64 {
        entries.push(rec("wf-a", i));
        entries.push(rec("wf-b", i));
    }
    shard.append(&entries).unwrap();
    shard.sync().unwrap();
    drop(shard);
    let mut shard = open_shard(&disk, small_segments());
    let ids = shard.list().unwrap();
    assert_eq!(ids, vec![WorkflowId::new("wf-a"), WorkflowId::new("wf-b")]);
    for wf in ["wf-a", "wf-b"] {
        let readout = shard.read(&WorkflowId::new(wf)).unwrap();
        assert_eq!(readout.records.len(), 50, "{wf}");
    }
}

#[test]
fn real_filesystem_round_trip() {
    let dir = tempfile::tempdir().unwrap();
    {
        let store = WalStorage::open(dir.path()).unwrap();
        let mut shard = store.open_shard(0).unwrap();
        shard
            .append(&(0..100).map(|i| rec("wf-real", i)).collect::<Vec<_>>())
            .unwrap();
        shard.append(&[snap("wf-real", 40)]).unwrap();
        shard.sync().unwrap();
    }
    // Fresh open from real files.
    let store = WalStorage::open(dir.path()).unwrap();
    let mut shard = store.open_shard(0).unwrap();
    let readout = shard.read(&WorkflowId::new("wf-real")).unwrap();
    assert_eq!(readout.snapshot.as_ref().map(|s| s.upto), Some(40));
    assert_eq!(readout.records.len(), 60);
    assert_eq!(readout.records[0].index, 40);
    let stats = shard.stats();
    assert!(stats.fsyncs >= 1 || stats.records_appended > 0);
}

#[test]
fn same_seed_same_durable_image() {
    // Byte-identical durable state across two identical runs (physical
    // determinism at the storage layer).
    let run = |seed: u64| {
        let disk = SimDisk::new(seed);
        let mut shard = open_shard(&disk, small_segments());
        shard
            .append(&(0..100).map(|i| rec("wf-a", i)).collect::<Vec<_>>())
            .unwrap();
        shard.append(&[snap("wf-a", 50)]).unwrap();
        shard.sync().unwrap();
        shard.maintain().unwrap();
        drop(shard);
        disk.crash();
        disk.recover();
        disk.durable_image()
    };
    assert_eq!(run(42), run(42));
}
