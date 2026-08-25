//! The pluggable storage interface.
//!
//! Storage is shard-oriented to match the thread-per-core engine: a
//! [`Storage`] is a factory of [`StorageShard`]s; each engine core owns
//! exactly one shard exclusively (shared-nothing). Appends are buffered;
//! [`StorageShard::sync`] is the durability barrier — nothing is
//! acknowledged durable to users until `sync` returned `Ok`.

use crate::error::StorageError;
use crate::event::JournalRecord;
use crate::id::WorkflowId;
use crate::snapshot::SnapshotRecord;

/// One unit of appended data.
#[derive(Debug, Clone, PartialEq)]
pub struct AppendEntry {
    /// The workflow this entry belongs to.
    pub workflow: WorkflowId,
    /// Journal record or snapshot.
    pub payload: AppendPayload,
}

/// Payload of an [`AppendEntry`].
#[derive(Debug, Clone, PartialEq)]
#[allow(clippy::large_enum_variant)]
pub enum AppendPayload {
    /// A journal record.
    Record(JournalRecord),
    /// A snapshot (compaction point).
    Snapshot(SnapshotRecord),
}

/// Result of reading one workflow's persisted history.
#[derive(Debug, Clone, PartialEq, Default)]
pub struct JournalReadout {
    /// Latest durable snapshot, if any.
    pub snapshot: Option<SnapshotRecord>,
    /// Journal records after the snapshot (`index >= snapshot.upto`), in
    /// order. When `snapshot` is `None`, this is the full journal.
    pub records: Vec<JournalRecord>,
}

/// Storage counters for metrics and benchmarks.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Default)]
pub struct StorageStats {
    /// Total records appended.
    pub records_appended: u64,
    /// Total bytes handed to the underlying files (write amplification
    /// numerator).
    pub bytes_written: u64,
    /// Number of fsync (durability barrier) calls that reached the device.
    pub fsyncs: u64,
    /// Number of live segments (WAL backends).
    pub live_segments: u64,
    /// Number of segments deleted by GC so far.
    pub segments_deleted: u64,
}

/// One engine core's exclusive storage handle.
pub trait StorageShard: Send {
    /// Buffer entries for append, in order. Not durable until [`Self::sync`].
    /// An `Err` means the entries were not accepted (the store may be
    /// failed); the engine halts commits and applies backpressure.
    fn append(&mut self, entries: &[AppendEntry]) -> Result<(), StorageError>;

    /// Durability barrier: everything previously appended survives a crash
    /// once this returns `Ok`. A failed sync poisons the shard: subsequent
    /// appends must fail rather than silently drop the durability guarantee.
    fn sync(&mut self) -> Result<(), StorageError>;

    /// Read one workflow's snapshot + journal tail.
    fn read(&mut self, workflow: &WorkflowId) -> Result<JournalReadout, StorageError>;

    /// All workflow ids present in this shard.
    fn list(&mut self) -> Result<Vec<WorkflowId>, StorageError>;

    /// Opportunistic maintenance: roll segments, GC segments fully covered
    /// by snapshots. Called by the engine between activations.
    fn maintain(&mut self) -> Result<(), StorageError>;

    /// Storage counters.
    fn stats(&self) -> StorageStats;
}

/// A storage backend: factory of per-core shards.
///
/// `num_shards` is a property of the *data*, not of the current process: a
/// WAL directory created with N shards must always be opened with N shards
/// (workflow→shard assignment is persisted implicitly by placement).
pub trait Storage: Send + Sync + 'static {
    /// Number of shards in this store.
    fn num_shards(&self) -> usize;
    /// Open shard `shard` (0-based). Each shard must be opened at most once
    /// per process; the shard is exclusively owned by one engine core.
    fn open_shard(&self, shard: usize) -> Result<Box<dyn StorageShard>, StorageError>;
}
