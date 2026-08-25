//! `MemoryStorage`: an in-memory backend for tests and examples. Everything
//! is "durable" the moment it is appended; `sync` only counts.

use sqrl_core::snapshot::SnapshotRecord;
use sqrl_core::storage::{AppendEntry, AppendPayload, JournalReadout, StorageStats};
use sqrl_core::{JournalRecord, Storage, StorageError, StorageShard, WorkflowId};
use std::collections::BTreeMap;
use std::sync::{Arc, Mutex, MutexGuard};

#[derive(Default)]
struct ShardState {
    journals: BTreeMap<WorkflowId, Vec<JournalRecord>>,
    snapshots: BTreeMap<WorkflowId, SnapshotRecord>,
    stats: StorageStats,
}

/// In-memory storage; cheap to clone (all clones share state), so a test can
/// "restart" an engine against the same store.
///
/// ```
/// use sqrl_store::MemoryStorage;
/// use sqrl_core::Storage;
/// let store = MemoryStorage::new(2);
/// assert_eq!(store.num_shards(), 2);
/// let shard = store.open_shard(0).unwrap();
/// drop(shard);
/// ```
#[derive(Clone)]
pub struct MemoryStorage {
    shards: Arc<Vec<Mutex<ShardState>>>,
}

impl MemoryStorage {
    /// Create with `num_shards` shards (min 1).
    pub fn new(num_shards: usize) -> Self {
        let n = num_shards.max(1);
        MemoryStorage {
            shards: Arc::new((0..n).map(|_| Mutex::new(ShardState::default())).collect()),
        }
    }
}

impl Storage for MemoryStorage {
    fn num_shards(&self) -> usize {
        self.shards.len()
    }

    fn open_shard(&self, shard: usize) -> Result<Box<dyn StorageShard>, StorageError> {
        if shard >= self.shards.len() {
            return Err(StorageError::Unsupported(format!(
                "shard {shard} out of range"
            )));
        }
        Ok(Box::new(MemShard {
            store: self.clone(),
            shard,
        }))
    }
}

struct MemShard {
    store: MemoryStorage,
    shard: usize,
}

impl MemShard {
    fn state(&self) -> MutexGuard<'_, ShardState> {
        match self.store.shards[self.shard].lock() {
            Ok(g) => g,
            Err(poisoned) => poisoned.into_inner(),
        }
    }
}

impl StorageShard for MemShard {
    fn append(&mut self, entries: &[AppendEntry]) -> Result<(), StorageError> {
        let mut s = self.state();
        for e in entries {
            match &e.payload {
                AppendPayload::Record(r) => {
                    s.journals
                        .entry(e.workflow.clone())
                        .or_default()
                        .push(r.clone());
                }
                AppendPayload::Snapshot(snap) => {
                    s.snapshots.insert(e.workflow.clone(), snap.clone());
                }
            }
            s.stats.records_appended += 1;
        }
        Ok(())
    }

    fn sync(&mut self) -> Result<(), StorageError> {
        self.state().stats.fsyncs += 1;
        Ok(())
    }

    fn read(&mut self, workflow: &WorkflowId) -> Result<JournalReadout, StorageError> {
        let s = self.state();
        let snapshot = s.snapshots.get(workflow).cloned();
        let cut = snapshot.as_ref().map(|sn| sn.upto).unwrap_or(0);
        let records: Vec<JournalRecord> = s
            .journals
            .get(workflow)
            .map(|v| v.iter().filter(|r| r.index >= cut).cloned().collect())
            .unwrap_or_default();
        if snapshot.is_none() && records.is_empty() {
            return Err(StorageError::UnknownWorkflow(workflow.to_string()));
        }
        Ok(JournalReadout { snapshot, records })
    }

    fn list(&mut self) -> Result<Vec<WorkflowId>, StorageError> {
        let s = self.state();
        let mut ids: Vec<WorkflowId> = s.journals.keys().cloned().collect();
        for id in s.snapshots.keys() {
            if !s.journals.contains_key(id) {
                ids.push(id.clone());
            }
        }
        ids.sort();
        Ok(ids)
    }

    fn maintain(&mut self) -> Result<(), StorageError> {
        // Drop journal records fully covered by snapshots.
        let mut s = self.state();
        let cuts: Vec<(WorkflowId, u64)> = s
            .snapshots
            .iter()
            .map(|(id, sn)| (id.clone(), sn.upto))
            .collect();
        for (id, cut) in cuts {
            if let Some(v) = s.journals.get_mut(&id) {
                v.retain(|r| r.index >= cut);
            }
        }
        Ok(())
    }

    fn stats(&self) -> StorageStats {
        self.state().stats
    }
}
