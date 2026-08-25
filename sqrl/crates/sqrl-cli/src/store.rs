//! Store access: open a WAL data directory and hand out shard handles.
//!
//! Shards are opened lazily and at most once per process (the `Storage`
//! contract); the CLI keeps every opened shard for the lifetime of the
//! command.

use crate::{CliError, CliResult};
use sqrl_core::storage::JournalReadout;
use sqrl_core::{Storage, StorageError, StorageShard, WorkflowId};
use sqrl_store::WalStorage;
use std::path::Path;

/// An opened store plus its lazily-opened shards.
pub struct Store {
    storage: WalStorage,
    shards: Vec<Option<Box<dyn StorageShard>>>,
}

impl Store {
    /// Open an existing store; refuse to create one on a wrong/empty path.
    pub fn open_existing(data: &Path) -> CliResult<Self> {
        if !data.join("sqrl.meta").is_file() {
            return Err(CliError(format!(
                "no sqrl store at `{}` (missing sqrl.meta)",
                data.display()
            )));
        }
        Self::open_raw(data)
    }

    /// Open a store, creating it if the directory is empty (bench only).
    pub fn open_or_create(data: &Path) -> CliResult<Self> {
        Self::open_raw(data)
    }

    fn open_raw(data: &Path) -> CliResult<Self> {
        let storage = WalStorage::open(data)?;
        let n = storage.num_shards();
        Ok(Store {
            storage,
            shards: (0..n).map(|_| None).collect(),
        })
    }

    /// Number of shards in the store (a property of the data).
    pub fn num_shards(&self) -> usize {
        self.storage.num_shards()
    }

    /// The shard index a workflow id is placed on.
    pub fn shard_index_for(&self, id: &WorkflowId) -> usize {
        id.shard(self.num_shards())
    }

    /// Open (once) and return shard `idx`.
    pub fn shard(&mut self, idx: usize) -> CliResult<&mut dyn StorageShard> {
        let slot = self
            .shards
            .get_mut(idx)
            .ok_or_else(|| CliError(format!("shard {idx} out of range")))?;
        if slot.is_none() {
            *slot = Some(self.storage.open_shard(idx)?);
        }
        match slot {
            Some(s) => Ok(s.as_mut()),
            None => Err(CliError(format!("shard {idx} failed to open"))),
        }
    }

    /// Read one workflow's journal from its home shard.
    pub fn read(&mut self, id: &WorkflowId) -> CliResult<JournalReadout> {
        let idx = self.shard_index_for(id);
        self.shard(idx)?.read(id).map_err(|e| match e {
            StorageError::UnknownWorkflow(w) => {
                CliError(format!("workflow `{w}` not found in store"))
            }
            other => CliError(other.to_string()),
        })
    }
}
