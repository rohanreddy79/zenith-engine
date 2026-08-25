//! Criterion micro-benchmarks for sqrl's storage and replay hot paths.
//!
//! End-to-end workload benchmarks (throughput, latency percentiles, recovery,
//! skew) live in `bench-harness/`; these isolate the WAL codec, append/fsync
//! path, replay decode, and snapshot round trip. See `docs/benchmarks.md` for
//! recorded results + reproduction commands.

use criterion::{criterion_group, criterion_main, BatchSize, Criterion, Throughput};
use sqrl_core::event::{JournalEvent, JournalRecord};
use sqrl_core::snapshot::{Outcome, SnapshotBody, SnapshotMeta, SnapshotRecord};
use sqrl_core::storage::{AppendEntry, AppendPayload};
use sqrl_core::{LogicalTime, Storage, StorageShard, WorkflowId};
use sqrl_store::{StdVfs, WalOptions, WalStorage};
use std::sync::Arc;

fn record(i: u64, payload: usize) -> AppendEntry {
    AppendEntry {
        workflow: WorkflowId::new("bench-wf"),
        payload: AppendPayload::Record(JournalRecord {
            index: i,
            at: LogicalTime::from_millis(i),
            event: JournalEvent::StepCompleted {
                seq: i,
                result: vec![0xAB; payload],
            },
        }),
    }
}

fn open_shard(dir: &std::path::Path) -> Box<dyn StorageShard> {
    WalStorage::open_with(
        Arc::new(StdVfs::new(dir.to_path_buf()).unwrap()),
        WalOptions {
            num_shards: 1,
            segment_size: 64 * 1024 * 1024,
        },
    )
    .unwrap()
    .open_shard(0)
    .unwrap()
}

fn bench_codec(c: &mut Criterion) {
    let mut g = c.benchmark_group("wal-codec");
    for payload in [64usize, 1024] {
        let rec = sqrl_store::codec::WalRecord::Entry(sqrl_store::codec::WalEntry {
            workflow: WorkflowId::new("bench-wf"),
            record: JournalRecord {
                index: 1,
                at: LogicalTime::from_millis(1),
                event: JournalEvent::StepCompleted {
                    seq: 1,
                    result: vec![0xAB; payload],
                },
            },
        });
        let encoded = sqrl_store::codec::encode(&rec).unwrap();
        g.throughput(Throughput::Bytes(encoded.len() as u64));
        g.bench_function(format!("encode-{payload}B"), |b| {
            b.iter(|| sqrl_store::codec::encode(std::hint::black_box(&rec)).unwrap())
        });
        g.bench_function(format!("decode-{payload}B"), |b| {
            b.iter(|| {
                sqrl_store::codec::decode_one(std::hint::black_box(&encoded), 0)
                    .unwrap()
                    .unwrap()
            })
        });
    }
    g.finish();
}

fn bench_append(c: &mut Criterion) {
    let mut g = c.benchmark_group("wal-append");
    g.sample_size(20);
    for (name, batch, payload) in [
        ("1x64B", 1usize, 64usize),
        ("256x64B", 256, 64),
        ("256x1KiB", 256, 1024),
    ] {
        let dir = tempfile::tempdir().unwrap();
        let mut shard = open_shard(dir.path());
        let entries: Vec<AppendEntry> = (0..batch as u64).map(|i| record(i, payload)).collect();
        g.throughput(Throughput::Elements(batch as u64));
        g.bench_function(format!("append-{name}-nosync"), |b| {
            b.iter(|| shard.append(std::hint::black_box(&entries)).unwrap())
        });
        let dir2 = tempfile::tempdir().unwrap();
        let mut shard2 = open_shard(dir2.path());
        g.bench_function(format!("append-{name}-fsync"), |b| {
            b.iter(|| {
                shard2.append(std::hint::black_box(&entries)).unwrap();
                shard2.sync().unwrap();
            })
        });
    }
    g.finish();
}

fn bench_replay_read(c: &mut Criterion) {
    // Journal read+decode throughput: the "full replay" storage path.
    let mut g = c.benchmark_group("replay-read");
    g.sample_size(10);
    for n in [10_000u64, 100_000] {
        let dir = tempfile::tempdir().unwrap();
        {
            let mut shard = open_shard(dir.path());
            for chunk in (0..n).collect::<Vec<_>>().chunks(1024) {
                let entries: Vec<AppendEntry> = chunk.iter().map(|i| record(*i, 64)).collect();
                shard.append(&entries).unwrap();
            }
            shard.sync().unwrap();
        }
        g.throughput(Throughput::Elements(n));
        g.bench_function(format!("read-{n}-records"), |b| {
            b.iter_batched(
                || open_shard(dir.path()),
                |mut shard| shard.read(&WorkflowId::new("bench-wf")).unwrap(),
                BatchSize::PerIteration,
            )
        });
    }
    g.finish();
}

fn bench_snapshot(c: &mut Criterion) {
    let mut g = c.benchmark_group("snapshot");
    g.sample_size(10);
    for n in [10_000u64, 100_000] {
        let body = SnapshotBody {
            cmds: (0..n)
                .map(|i| {
                    (
                        i,
                        sqrl_core::CmdDesc::Step {
                            name: format!("step-{}", i % 16),
                        },
                    )
                })
                .collect(),
            outcomes: (0..n)
                .map(|i| Outcome::StepOk {
                    seq: i,
                    result: vec![0xAB; 64],
                    at: LogicalTime::from_millis(i),
                })
                .collect(),
        };
        g.throughput(Throughput::Elements(n));
        g.bench_function(format!("build-{n}-outcomes"), |b| {
            b.iter(|| {
                SnapshotRecord::build(n, SnapshotMeta::default(), std::hint::black_box(&body))
                    .unwrap()
            })
        });
        let rec = SnapshotRecord::build(n, SnapshotMeta::default(), &body).unwrap();
        g.bench_function(format!("decode-body-{n}-outcomes"), |b| {
            b.iter(|| std::hint::black_box(&rec).decode_body().unwrap())
        });
    }
    g.finish();
}

criterion_group!(
    benches,
    bench_codec,
    bench_append,
    bench_replay_read,
    bench_snapshot
);
criterion_main!(benches);
