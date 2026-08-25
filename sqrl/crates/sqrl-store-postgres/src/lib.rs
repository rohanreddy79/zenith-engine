//! PostgreSQL storage backend for `sqrl`: journals and snapshots in a
//! shared PostgreSQL database (schema `sqrl`).
//!
//! # Layout (schema version 1, `sqrl.meta` key `schema_version`)
//!
//! * `sqrl.meta(key TEXT PRIMARY KEY, value TEXT)` — `schema_version`,
//!   `format_version` (the logical record encoding version,
//!   [`sqrl_core::codec::SQRL_FORMAT_VERSION`]) and `num_shards`, stored as
//!   decimal ASCII.
//! * `sqrl.journal(shard, workflow, idx, at, event, PRIMARY KEY(workflow,
//!   idx))` plus an index on `(shard, workflow)` — one row per
//!   [`sqrl_core::JournalRecord`]; `event` is the record's
//!   [`sqrl_core::JournalEvent`] as self-describing MessagePack
//!   ([`sqrl_core::codec`], the same logical encoding as the WAL and SQLite
//!   backends), `idx` and `at` (logical milliseconds) lifted into columns.
//! * `sqrl.snapshots(workflow PRIMARY KEY, shard, upto, meta, body)` — the
//!   **latest** snapshot only (a new snapshot replaces the previous one).
//!
//! Workflow→shard placement is the caller's concern (as with every backend:
//! `num_shards` is a property of the data). The `shard` column is stored and
//! filtered on by `read`/`list` anyway, as defense in depth.
//!
//! # Durability mapping
//!
//! [`sqrl_core::StorageShard::append`] buffers rows **in memory**;
//! [`sqrl_core::StorageShard::sync`] — the durability barrier — writes every
//! buffered row in one transaction and commits. Every connection runs with
//! `synchronous_commit = on` (set explicitly at open, defending against a
//! weaker database/role default): a committed transaction is then WAL-flushed
//! to disk before the commit returns, which is exactly the barrier the
//! contract requires. A failed append or commit **poisons** the shard
//! (mirroring the WAL backend's `WalShard`): subsequent `append`/`sync`
//! calls return the stored error rather than silently dropping the
//! durability guarantee. Reads still work on a poisoned shard, and
//! `maintain` becomes a no-op.
//!
//! As in the other backends, rows appended but not yet synced are visible to
//! `read`/`list` on the same shard handle (overlaid from the buffer) but are
//! not durable and are lost if the process dies before `sync`.
//!
//! # Concurrency
//!
//! [`PostgresStorage`] holds no connection of its own: every
//! [`sqrl_core::Storage::open_shard`] call opens a **fresh**
//! [`postgres::Client`], so per-core shards never share a connection. As
//! everywhere in `sqrl`, each shard must be opened by at most one engine
//! core. Schema creation serializes concurrent creators with a transaction
//! scoped advisory lock.
//!
//! # Verification status
//!
//! **UNVERIFIED in the development environment** (no PostgreSQL server, no
//! docker): the integration tests are gated behind `SQRL_POSTGRES_URL` and
//! skip otherwise. To run them against a real server:
//!
//! ```bash
//! docker run --rm -e POSTGRES_PASSWORD=pw -p 5432:5432 postgres:16
//! SQRL_POSTGRES_URL=postgres://postgres:pw@localhost:5432/postgres \
//!     cargo test -p sqrl-store-postgres
//! ```
#![forbid(unsafe_code)]
#![deny(missing_docs)]

use postgres::error::SqlState;
use postgres::{Client, NoTls};
use sqrl_core::codec::{self, SQRL_FORMAT_VERSION};
use sqrl_core::snapshot::{SnapshotMeta, SnapshotRecord};
use sqrl_core::storage::{AppendEntry, AppendPayload, JournalReadout, StorageStats};
use sqrl_core::{
    JournalEvent, JournalRecord, LogicalTime, Storage, StorageError, StorageShard, WorkflowId,
};
use std::collections::{BTreeMap, BTreeSet};

/// Schema version stored under `sqrl.meta['schema_version']`.
const SCHEMA_VERSION: u32 = 1;

/// Advisory lock key serializing schema creation (arbitrary fixed value:
/// "sqrl" as ASCII, spelled in hex).
const SETUP_LOCK_KEY: i64 = 0x7371_726c;

const SCHEMA: &str = "\
CREATE SCHEMA IF NOT EXISTS sqrl;
CREATE TABLE IF NOT EXISTS sqrl.meta (
    key   TEXT PRIMARY KEY,
    value TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS sqrl.journal (
    shard    BIGINT NOT NULL,
    workflow TEXT   NOT NULL,
    idx      BIGINT NOT NULL,
    at       BIGINT NOT NULL,
    event    BYTEA  NOT NULL,
    PRIMARY KEY (workflow, idx)
);
CREATE INDEX IF NOT EXISTS journal_by_shard ON sqrl.journal (shard, workflow);
CREATE TABLE IF NOT EXISTS sqrl.snapshots (
    workflow TEXT PRIMARY KEY,
    shard    BIGINT NOT NULL,
    upto     BIGINT NOT NULL,
    meta     BYTEA  NOT NULL,
    body     BYTEA  NOT NULL
);
";

/// PostgreSQL-backed [`Storage`]: the whole store is the `sqrl` schema of
/// one database.
///
/// Create with [`PostgresStorage::connect`]; each
/// [`Storage::open_shard`] opens its own connection.
#[derive(Debug, Clone)]
pub struct PostgresStorage {
    url: String,
    num_shards: u32,
}

impl PostgresStorage {
    /// Connect to `url` (a `postgres://` connection string) and open (or
    /// create) the store's schema.
    ///
    /// * **Creating** a new store: `num_shards` (minimum 1; `0` is clamped
    ///   to 1) is persisted in `sqrl.meta` and becomes a permanent property
    ///   of the data.
    /// * **Opening** an existing store: the *stored* shard count always
    ///   wins. Pass `0` ("use the stored value") or the exact stored value;
    ///   any other nonzero value returns [`StorageError::Unsupported`],
    ///   because workflow→shard placement is persisted implicitly and cannot
    ///   be re-derived under a different shard count.
    pub fn connect(url: impl Into<String>, num_shards: u32) -> Result<Self, StorageError> {
        let url = url.into();
        let mut client = open_client(&url)?;
        let stored = setup(&mut client, num_shards)?;
        Ok(PostgresStorage {
            url,
            num_shards: stored,
        })
    }

    /// The connection string this store operates on.
    pub fn url(&self) -> &str {
        &self.url
    }
}

impl Storage for PostgresStorage {
    fn num_shards(&self) -> usize {
        self.num_shards as usize
    }

    fn open_shard(&self, shard: usize) -> Result<Box<dyn StorageShard>, StorageError> {
        if shard >= self.num_shards as usize {
            return Err(StorageError::Unsupported(format!(
                "shard {shard} out of range ({} shards)",
                self.num_shards
            )));
        }
        let client = open_client(&self.url)?;
        Ok(Box::new(PostgresShard {
            client,
            shard: shard as i64,
            buf: Vec::new(),
            poisoned: None,
            stats: StorageStats::default(),
        }))
    }
}

/// Open a connection with the settings every connection needs. See the crate
/// docs for why `synchronous_commit = on` is set explicitly.
fn open_client(url: &str) -> Result<Client, StorageError> {
    let mut client = Client::connect(url, NoTls).map_err(db_err)?;
    client
        .batch_execute("SET synchronous_commit = on")
        .map_err(db_err)?;
    Ok(client)
}

/// Create the schema on first open, or validate + read the stored metadata.
/// Runs in one transaction holding an advisory lock so concurrent creators
/// serialize. Returns the effective (stored) shard count.
fn setup(client: &mut Client, requested: u32) -> Result<u32, StorageError> {
    let mut tx = client.transaction().map_err(db_err)?;
    tx.execute("SELECT pg_advisory_xact_lock($1)", &[&SETUP_LOCK_KEY])
        .map_err(db_err)?;
    tx.batch_execute(SCHEMA).map_err(db_err)?;
    let version = read_meta_u32(&mut tx, "schema_version")?;
    let stored = match version {
        None => {
            // Brand-new store: persist the metadata.
            let n = requested.max(1);
            for (key, value) in [
                ("schema_version", SCHEMA_VERSION.to_string()),
                ("format_version", u32::from(SQRL_FORMAT_VERSION).to_string()),
                ("num_shards", n.to_string()),
            ] {
                tx.execute(
                    "INSERT INTO sqrl.meta (key, value) VALUES ($1, $2) \
                     ON CONFLICT (key) DO NOTHING",
                    &[&key, &value],
                )
                .map_err(db_err)?;
            }
            n
        }
        Some(SCHEMA_VERSION) => {
            let format = read_meta_u32(&mut tx, "format_version")?
                .ok_or_else(|| StorageError::Corrupt("meta key `format_version` missing".into()))?;
            if format > u32::from(SQRL_FORMAT_VERSION) {
                return Err(StorageError::Corrupt(format!(
                    "store format version {format} is newer than supported {SQRL_FORMAT_VERSION}"
                )));
            }
            let stored = read_meta_u32(&mut tx, "num_shards")?
                .ok_or_else(|| StorageError::Corrupt("meta key `num_shards` missing".into()))?;
            if stored == 0 {
                return Err(StorageError::Corrupt("stored num_shards is 0".into()));
            }
            if requested != 0 && requested != stored {
                return Err(StorageError::Unsupported(format!(
                    "store was created with {stored} shard(s); cannot open with {requested} \
                     (pass 0 to use the stored value)"
                )));
            }
            stored
        }
        Some(v) => {
            return Err(StorageError::Corrupt(format!(
                "unsupported postgres store schema version {v} (supported: {SCHEMA_VERSION})"
            )))
        }
    };
    tx.commit().map_err(db_err)?;
    Ok(stored)
}

fn read_meta_u32(
    tx: &mut postgres::Transaction<'_>,
    key: &str,
) -> Result<Option<u32>, StorageError> {
    let row = tx
        .query_opt("SELECT value FROM sqrl.meta WHERE key = $1", &[&key])
        .map_err(db_err)?;
    match row {
        None => Ok(None),
        Some(row) => {
            let value: String = row.get(0);
            value.parse::<u32>().map(Some).map_err(|_| {
                StorageError::Corrupt(format!("meta key `{key}` is not a decimal integer"))
            })
        }
    }
}

// ---------------------------------------------------------------------------

/// One buffered (appended but not yet committed) row, pre-encoded so codec
/// errors surface at `append` time, like the WAL backend.
enum PendingRow {
    Record {
        workflow: WorkflowId,
        idx: i64,
        at: i64,
        event: Vec<u8>,
    },
    Snapshot {
        workflow: WorkflowId,
        upto: i64,
        meta: Vec<u8>,
        body: Vec<u8>,
    },
}

/// One shard of a [`PostgresStorage`]: its own connection, an in-memory
/// append buffer, and the poisoning flag required by the durability
/// contract.
struct PostgresShard {
    client: Client,
    shard: i64,
    buf: Vec<PendingRow>,
    poisoned: Option<StorageError>,
    stats: StorageStats,
}

impl PostgresShard {
    /// Insert every buffered row inside one committed transaction; returns
    /// the blob bytes written. Does not touch `self.buf` or the stats — the
    /// caller settles those based on the outcome.
    fn commit_buffered(&mut self) -> Result<u64, StorageError> {
        let shard = self.shard;
        let mut tx = self.client.transaction().map_err(db_err)?;
        let mut bytes = 0u64;
        for row in &self.buf {
            match row {
                PendingRow::Record {
                    workflow,
                    idx,
                    at,
                    event,
                } => {
                    tx.execute(
                        "INSERT INTO sqrl.journal (shard, workflow, idx, at, event) \
                         VALUES ($1, $2, $3, $4, $5) \
                         ON CONFLICT (workflow, idx) DO UPDATE \
                         SET shard = EXCLUDED.shard, at = EXCLUDED.at, \
                             event = EXCLUDED.event",
                        &[&shard, &workflow.as_str(), idx, at, event],
                    )
                    .map_err(db_err)?;
                    bytes += event.len() as u64;
                }
                PendingRow::Snapshot {
                    workflow,
                    upto,
                    meta,
                    body,
                } => {
                    tx.execute(
                        "INSERT INTO sqrl.snapshots (workflow, shard, upto, meta, body) \
                         VALUES ($1, $2, $3, $4, $5) \
                         ON CONFLICT (workflow) DO UPDATE \
                         SET shard = EXCLUDED.shard, upto = EXCLUDED.upto, \
                             meta = EXCLUDED.meta, body = EXCLUDED.body",
                        &[&workflow.as_str(), &shard, upto, meta, body],
                    )
                    .map_err(db_err)?;
                    bytes += (meta.len() + body.len()) as u64;
                }
            }
        }
        // `synchronous_commit = on`: this commit flushes the server WAL to
        // disk before returning — the durability barrier.
        tx.commit().map_err(db_err)?;
        Ok(bytes)
    }

    fn read_snapshot(
        &mut self,
        workflow: &WorkflowId,
    ) -> Result<Option<SnapshotRecord>, StorageError> {
        let row = self
            .client
            .query_opt(
                "SELECT upto, meta, body FROM sqrl.snapshots \
                 WHERE workflow = $1 AND shard = $2",
                &[&workflow.as_str(), &self.shard],
            )
            .map_err(db_err)?;
        match row {
            None => Ok(None),
            Some(row) => {
                let upto = u64_col("snapshots.upto", row.get(0))?;
                let meta: Vec<u8> = row.get(1);
                let body: Vec<u8> = row.get(2);
                let meta: SnapshotMeta =
                    codec::from_slice(&meta, "snapshot meta").map_err(codec_err)?;
                Ok(Some(SnapshotRecord { upto, meta, body }))
            }
        }
    }

    fn read_records(
        &mut self,
        workflow: &WorkflowId,
    ) -> Result<BTreeMap<u64, JournalRecord>, StorageError> {
        let rows = self
            .client
            .query(
                "SELECT idx, at, event FROM sqrl.journal \
                 WHERE workflow = $1 AND shard = $2 ORDER BY idx",
                &[&workflow.as_str(), &self.shard],
            )
            .map_err(db_err)?;
        let mut out = BTreeMap::new();
        for row in rows {
            let index = u64_col("journal.idx", row.get(0))?;
            let at = u64_col("journal.at", row.get(1))?;
            let event: Vec<u8> = row.get(2);
            let event: JournalEvent =
                codec::from_slice(&event, "journal event").map_err(codec_err)?;
            out.insert(
                index,
                JournalRecord {
                    index,
                    at: LogicalTime::from_millis(at),
                    event,
                },
            );
        }
        Ok(out)
    }
}

impl StorageShard for PostgresShard {
    fn append(&mut self, entries: &[AppendEntry]) -> Result<(), StorageError> {
        if let Some(e) = &self.poisoned {
            return Err(e.clone());
        }
        match encode_rows(entries) {
            Ok(mut rows) => {
                self.stats.records_appended += entries.len() as u64;
                self.buf.append(&mut rows);
                Ok(())
            }
            Err(e) => {
                // Mirror `WalShard`: a failed append poisons the shard — the
                // batch was not accepted (none of it is buffered) and the
                // engine must halt commits.
                self.poisoned = Some(e.clone());
                Err(e)
            }
        }
    }

    fn sync(&mut self) -> Result<(), StorageError> {
        if let Some(e) = &self.poisoned {
            return Err(e.clone());
        }
        if self.buf.is_empty() {
            // Nothing pending: everything previously appended was committed
            // by an earlier sync, so the barrier holds trivially.
            return Ok(());
        }
        match self.commit_buffered() {
            Ok(bytes) => {
                self.buf.clear();
                self.stats.fsyncs += 1;
                self.stats.bytes_written += bytes;
                Ok(())
            }
            Err(e) => {
                // The transaction rolled back: nothing partial is durable.
                // Poison so nothing is ever acknowledged after a failed
                // barrier. (Buffered rows stay in memory; reads may still
                // see them, like unsynced WAL appends.)
                self.poisoned = Some(e.clone());
                Err(e)
            }
        }
    }

    fn read(&mut self, workflow: &WorkflowId) -> Result<JournalReadout, StorageError> {
        let mut snapshot = self.read_snapshot(workflow)?;
        let mut by_idx = self.read_records(workflow)?;
        // Overlay buffered (appended but unsynced) rows, in append order:
        // parity with the WAL/mem/SQLite backends — appended data is visible
        // before `sync`, with the same last-wins semantics the committed
        // upserts would have.
        for row in &self.buf {
            match row {
                PendingRow::Record {
                    workflow: wf,
                    idx,
                    at,
                    event,
                } if wf == workflow => {
                    let event: JournalEvent =
                        codec::from_slice(event, "journal event").map_err(codec_err)?;
                    // Non-negative by construction (checked in `encode_rows`).
                    let index = *idx as u64;
                    by_idx.insert(
                        index,
                        JournalRecord {
                            index,
                            at: LogicalTime::from_millis(*at as u64),
                            event,
                        },
                    );
                }
                PendingRow::Snapshot {
                    workflow: wf,
                    upto,
                    meta,
                    body,
                } if wf == workflow => {
                    let meta: SnapshotMeta =
                        codec::from_slice(meta, "snapshot meta").map_err(codec_err)?;
                    snapshot = Some(SnapshotRecord {
                        upto: *upto as u64,
                        meta,
                        body: body.clone(),
                    });
                }
                _ => {}
            }
        }
        let cut = snapshot.as_ref().map(|s| s.upto).unwrap_or(0);
        let records: Vec<JournalRecord> = by_idx.into_values().filter(|r| r.index >= cut).collect();
        if snapshot.is_none() && records.is_empty() {
            return Err(StorageError::UnknownWorkflow(workflow.to_string()));
        }
        Ok(JournalReadout { snapshot, records })
    }

    fn list(&mut self) -> Result<Vec<WorkflowId>, StorageError> {
        let rows = self
            .client
            .query(
                "SELECT workflow FROM sqrl.journal WHERE shard = $1 \
                 UNION SELECT workflow FROM sqrl.snapshots WHERE shard = $1",
                &[&self.shard],
            )
            .map_err(db_err)?;
        let mut ids: BTreeSet<WorkflowId> = BTreeSet::new();
        for row in rows {
            let id: String = row.get(0);
            ids.insert(WorkflowId::new(id));
        }
        for row in &self.buf {
            let (PendingRow::Record { workflow, .. } | PendingRow::Snapshot { workflow, .. }) = row;
            ids.insert(workflow.clone());
        }
        // BTreeSet iterates in `Ord` order: sorted, deduplicated.
        Ok(ids.into_iter().collect())
    }

    fn maintain(&mut self) -> Result<(), StorageError> {
        if self.poisoned.is_some() {
            return Ok(());
        }
        // Delete journal rows superseded by a *committed* snapshot. Buffered
        // (unsynced) snapshots live only in `self.buf` and cannot enable
        // deletion — an unsynced snapshot must never free journal data.
        let deleted = self
            .client
            .execute(
                "DELETE FROM sqrl.journal j USING sqrl.snapshots s \
                 WHERE j.shard = $1 AND s.shard = $1 \
                   AND s.workflow = j.workflow AND j.idx < s.upto",
                &[&self.shard],
            )
            .map_err(db_err)?;
        self.stats.segments_deleted += deleted;
        Ok(())
    }

    fn stats(&self) -> StorageStats {
        // Mapping: `fsyncs` = committed sync transactions; `records_appended`
        // = entries accepted by `append`; `bytes_written` = blob bytes
        // committed; `segments_deleted` = superseded journal rows deleted by
        // `maintain`; `live_segments` = 0 (no segment files here).
        self.stats
    }
}

/// Encode a batch up front (all-or-nothing): codec or range errors surface
/// at `append` time with nothing partially buffered.
fn encode_rows(entries: &[AppendEntry]) -> Result<Vec<PendingRow>, StorageError> {
    let mut rows = Vec::with_capacity(entries.len());
    for entry in entries {
        match &entry.payload {
            AppendPayload::Record(r) => {
                let event = codec::to_vec(&r.event, "journal event").map_err(codec_err)?;
                rows.push(PendingRow::Record {
                    workflow: entry.workflow.clone(),
                    idx: i64_col("journal.idx", r.index)?,
                    at: i64_col("journal.at", r.at.as_millis())?,
                    event,
                });
            }
            AppendPayload::Snapshot(s) => {
                let meta = codec::to_vec(&s.meta, "snapshot meta").map_err(codec_err)?;
                rows.push(PendingRow::Snapshot {
                    workflow: entry.workflow.clone(),
                    upto: i64_col("snapshots.upto", s.upto)?,
                    meta,
                    body: s.body.clone(),
                });
            }
        }
    }
    Ok(rows)
}

// ---------------------------------------------------------------------------
// Error plumbing.

fn db_err(e: postgres::Error) -> StorageError {
    let msg = e.to_string();
    match e.code() {
        Some(&SqlState::DISK_FULL) => StorageError::DiskFull(msg),
        Some(&SqlState::DATA_CORRUPTED) | Some(&SqlState::INDEX_CORRUPTED) => {
            StorageError::Corrupt(msg)
        }
        _ => StorageError::Disk(msg),
    }
}

fn codec_err(e: sqrl_core::Error) -> StorageError {
    match e {
        sqrl_core::Error::Codec { context, message } => {
            StorageError::Codec(format!("{context}: {message}"))
        }
        other => StorageError::Codec(other.to_string()),
    }
}

/// Checked `u64` → BIGINT; values above `i64::MAX` are rejected (they would
/// break `ORDER BY idx` / `idx >= cut` comparisons).
fn i64_col(what: &'static str, value: u64) -> Result<i64, StorageError> {
    i64::try_from(value).map_err(|_| {
        StorageError::Unsupported(format!("{what} value {value} exceeds BIGINT range"))
    })
}

/// Checked BIGINT → `u64`; negative stored values mean tampering.
fn u64_col(what: &'static str, value: i64) -> Result<u64, StorageError> {
    u64::try_from(value)
        .map_err(|_| StorageError::Corrupt(format!("negative {what} value {value} in store")))
}
