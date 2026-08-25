//! SQLite storage backend for `sqrl`: journals and snapshots in a single
//! SQLite database file.
//!
//! # Layout (schema version 1, `PRAGMA user_version = 1`)
//!
//! * `meta(key TEXT PRIMARY KEY, value BLOB)` — `format_version` (the logical
//!   record encoding version, [`sqrl_core::codec::SQRL_FORMAT_VERSION`]) and
//!   `num_shards`, both stored as decimal ASCII.
//! * `journal(shard, workflow, idx, at, event, PRIMARY KEY(workflow, idx))`
//!   plus an index on `(shard, workflow)` — one row per
//!   [`sqrl_core::JournalRecord`]; `event` is the record's
//!   [`sqrl_core::JournalEvent`] as self-describing MessagePack
//!   ([`sqrl_core::codec`], same logical encoding as the WAL backend), `idx`
//!   and `at` (logical milliseconds) are lifted into columns.
//! * `snapshots(workflow PRIMARY KEY, shard, upto, meta, body)` — the
//!   **latest** snapshot only (a new snapshot replaces the previous one);
//!   `meta` is MessagePack of [`sqrl_core::SnapshotMeta`], `body` is the raw
//!   bytes of [`sqrl_core::SnapshotRecord::body`].
//!
//! Workflow→shard placement is the caller's concern (as with every backend:
//! `num_shards` is a property of the data). The `shard` column is stored and
//! filtered on by `read`/`list` anyway, as defense in depth.
//!
//! # Durability mapping
//!
//! [`sqrl_core::StorageShard::append`] buffers rows **in memory**;
//! [`sqrl_core::StorageShard::sync`] — the durability barrier — writes every
//! buffered row in one SQLite transaction and commits. Connections run
//! `PRAGMA journal_mode=WAL` with **`PRAGMA synchronous=FULL`**: under
//! `synchronous=NORMAL` a WAL-mode commit survives a process crash
//! (`kill -9`) but *not* power loss or an OS crash, because the WAL is not
//! fsynced per commit. `sqrl`'s contract is stronger — everything appended
//! before a successful `sync()` must survive *any* crash — so this backend
//! pays one fsync per commit (`FULL`), the honest mapping of the barrier.
//! The tradeoff: each `sync()` costs a device fsync (comparable to the WAL
//! backend's explicit fsync), instead of `NORMAL`'s deferred, batched WAL
//! syncs. No explicit `wal_checkpoint` is needed for durability; SQLite's
//! automatic checkpointing keeps the WAL file bounded.
//!
//! A failed append or commit **poisons** the shard (mirroring the WAL
//! backend's `WalShard`): subsequent `append`/`sync` calls return the stored
//! error rather than silently dropping the durability guarantee. Reads still
//! work on a poisoned shard, and `maintain` becomes a no-op.
//!
//! As in the WAL and in-memory backends, rows that are appended but not yet
//! synced *are* visible to `read`/`list` on the same shard handle (they are
//! overlaid from the buffer) — but they are not durable and are lost when
//! the process dies before `sync`.
//!
//! # Concurrency
//!
//! [`SqliteStorage`] holds no connection of its own: every
//! [`sqrl_core::Storage::open_shard`] call opens a **fresh**
//! `rusqlite::Connection` to the same file (WAL mode, `busy_timeout=5000`),
//! so per-core shards never share a connection. As everywhere in `sqrl`,
//! each shard must be opened by at most one engine core.

#![forbid(unsafe_code)]
#![deny(missing_docs)]

use rusqlite::{params, Connection, OptionalExtension, TransactionBehavior};
use sqrl_core::codec::{self, SQRL_FORMAT_VERSION};
use sqrl_core::snapshot::{SnapshotMeta, SnapshotRecord};
use sqrl_core::storage::{AppendEntry, AppendPayload, JournalReadout, StorageStats};
use sqrl_core::{
    JournalEvent, JournalRecord, LogicalTime, Storage, StorageError, StorageShard, WorkflowId,
};
use std::collections::{BTreeMap, BTreeSet};
use std::path::{Path, PathBuf};
use std::time::Duration;

/// Schema version written to `PRAGMA user_version`.
const SCHEMA_VERSION: i64 = 1;

const SCHEMA: &str = "\
CREATE TABLE IF NOT EXISTS meta (
    key   TEXT PRIMARY KEY,
    value BLOB NOT NULL
);
CREATE TABLE IF NOT EXISTS journal (
    shard    INTEGER NOT NULL,
    workflow TEXT    NOT NULL,
    idx      INTEGER NOT NULL,
    at       INTEGER NOT NULL,
    event    BLOB    NOT NULL,
    PRIMARY KEY (workflow, idx)
);
CREATE INDEX IF NOT EXISTS journal_by_shard ON journal (shard, workflow);
CREATE TABLE IF NOT EXISTS snapshots (
    workflow TEXT PRIMARY KEY,
    shard    INTEGER NOT NULL,
    upto     INTEGER NOT NULL,
    meta     BLOB    NOT NULL,
    body     BLOB    NOT NULL
);
";

/// SQLite-backed [`Storage`]: the whole store is one database file.
///
/// ```
/// use sqrl_core::Storage;
/// use sqrl_store_sqlite::SqliteStorage;
/// let dir = tempfile::tempdir().unwrap();
/// let store = SqliteStorage::open(dir.path().join("store.sqrl.db"), 2).unwrap();
/// assert_eq!(store.num_shards(), 2);
/// let shard = store.open_shard(0).unwrap();
/// drop(shard);
/// ```
#[derive(Debug, Clone)]
pub struct SqliteStorage {
    path: PathBuf,
    num_shards: u32,
}

impl SqliteStorage {
    /// Open (or create) the store at `path` (a database file; missing parent
    /// directories are created).
    ///
    /// * **Creating** a new store: `num_shards` (minimum 1; `0` is clamped
    ///   to 1) is persisted in the `meta` table and becomes a permanent
    ///   property of the data.
    /// * **Opening** an existing store: the *stored* shard count always
    ///   wins. Pass `0` ("use the stored value") or the exact stored value;
    ///   any other nonzero value returns [`StorageError::Unsupported`],
    ///   because workflow→shard placement is persisted implicitly and cannot
    ///   be re-derived under a different shard count.
    pub fn open(path: impl Into<PathBuf>, num_shards: u32) -> Result<Self, StorageError> {
        let path = path.into();
        if let Some(parent) = path.parent() {
            if !parent.as_os_str().is_empty() {
                std::fs::create_dir_all(parent).map_err(io_err)?;
            }
        }
        let mut conn = open_conn(&path)?;
        let stored = setup(&mut conn, num_shards)?;
        Ok(SqliteStorage {
            path,
            num_shards: stored,
        })
    }

    /// The database file this store operates on.
    pub fn path(&self) -> &Path {
        &self.path
    }
}

impl Storage for SqliteStorage {
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
        let conn = open_conn(&self.path)?;
        Ok(Box::new(SqliteShard {
            conn,
            shard: shard as i64,
            buf: Vec::new(),
            poisoned: None,
            stats: StorageStats::default(),
        }))
    }
}

/// Open a connection with the pragmas every connection needs. `journal_mode`
/// is persistent in the file; `synchronous` and `busy_timeout` are
/// per-connection. See the crate docs for why `synchronous=FULL`.
fn open_conn(path: &Path) -> Result<Connection, StorageError> {
    let conn = Connection::open(path).map_err(db_err)?;
    conn.busy_timeout(Duration::from_millis(5000))
        .map_err(db_err)?;
    conn.pragma_update(None, "journal_mode", "WAL")
        .map_err(db_err)?;
    conn.pragma_update(None, "synchronous", "FULL")
        .map_err(db_err)?;
    Ok(conn)
}

/// Create the schema on first open, or validate + read the stored metadata.
/// Runs in one `BEGIN IMMEDIATE` transaction so concurrent creators
/// serialize. Returns the effective (stored) shard count.
fn setup(conn: &mut Connection, requested: u32) -> Result<u32, StorageError> {
    let tx = conn
        .transaction_with_behavior(TransactionBehavior::Immediate)
        .map_err(db_err)?;
    let version: i64 = tx
        .query_row("PRAGMA user_version", [], |r| r.get(0))
        .map_err(db_err)?;
    let stored = match version {
        0 => {
            // Brand-new (or still-empty) database: create everything.
            tx.execute_batch(SCHEMA).map_err(db_err)?;
            let n = requested.max(1);
            tx.execute(
                "INSERT OR REPLACE INTO meta (key, value) VALUES ('format_version', ?1)",
                params![u32::from(SQRL_FORMAT_VERSION).to_string().into_bytes()],
            )
            .map_err(db_err)?;
            tx.execute(
                "INSERT OR REPLACE INTO meta (key, value) VALUES ('num_shards', ?1)",
                params![n.to_string().into_bytes()],
            )
            .map_err(db_err)?;
            tx.pragma_update(None, "user_version", SCHEMA_VERSION)
                .map_err(db_err)?;
            n
        }
        SCHEMA_VERSION => {
            let format = read_meta_u32(&tx, "format_version")?;
            if format > u32::from(SQRL_FORMAT_VERSION) {
                return Err(StorageError::Corrupt(format!(
                    "store format version {format} is newer than supported {SQRL_FORMAT_VERSION}"
                )));
            }
            let stored = read_meta_u32(&tx, "num_shards")?;
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
        v => {
            return Err(StorageError::Corrupt(format!(
                "unsupported sqlite store schema version {v} (supported: {SCHEMA_VERSION})"
            )))
        }
    };
    tx.commit().map_err(db_err)?;
    Ok(stored)
}

fn read_meta_u32(conn: &Connection, key: &str) -> Result<u32, StorageError> {
    let value: Option<Vec<u8>> = conn
        .query_row("SELECT value FROM meta WHERE key = ?1", params![key], |r| {
            r.get(0)
        })
        .optional()
        .map_err(db_err)?;
    let value =
        value.ok_or_else(|| StorageError::Corrupt(format!("meta key `{key}` is missing")))?;
    std::str::from_utf8(&value)
        .ok()
        .and_then(|s| s.parse::<u32>().ok())
        .ok_or_else(|| StorageError::Corrupt(format!("meta key `{key}` is not a decimal integer")))
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

/// One shard of a [`SqliteStorage`]: its own connection, an in-memory append
/// buffer, and the poisoning flag required by the durability contract.
struct SqliteShard {
    conn: Connection,
    shard: i64,
    buf: Vec<PendingRow>,
    poisoned: Option<StorageError>,
    stats: StorageStats,
}

impl SqliteShard {
    /// Insert every buffered row inside one committed transaction; returns
    /// the blob bytes written. Does not touch `self.buf` or the stats — the
    /// caller settles those based on the outcome.
    fn commit_buffered(&mut self) -> Result<u64, StorageError> {
        let shard = self.shard;
        let tx = self
            .conn
            .transaction_with_behavior(TransactionBehavior::Immediate)
            .map_err(db_err)?;
        let mut bytes = 0u64;
        {
            let mut ins_rec = tx
                .prepare_cached(
                    "INSERT OR REPLACE INTO journal (shard, workflow, idx, at, event) \
                     VALUES (?1, ?2, ?3, ?4, ?5)",
                )
                .map_err(db_err)?;
            let mut ins_snap = tx
                .prepare_cached(
                    "INSERT OR REPLACE INTO snapshots (workflow, shard, upto, meta, body) \
                     VALUES (?1, ?2, ?3, ?4, ?5)",
                )
                .map_err(db_err)?;
            for row in &self.buf {
                match row {
                    PendingRow::Record {
                        workflow,
                        idx,
                        at,
                        event,
                    } => {
                        ins_rec
                            .execute(params![shard, workflow.as_str(), idx, at, event])
                            .map_err(db_err)?;
                        bytes += event.len() as u64;
                    }
                    PendingRow::Snapshot {
                        workflow,
                        upto,
                        meta,
                        body,
                    } => {
                        ins_snap
                            .execute(params![workflow.as_str(), shard, upto, meta, body])
                            .map_err(db_err)?;
                        bytes += (meta.len() + body.len()) as u64;
                    }
                }
            }
        }
        // `synchronous=FULL`: this commit fsyncs the WAL — the barrier.
        tx.commit().map_err(db_err)?;
        Ok(bytes)
    }

    fn read_snapshot(&self, workflow: &WorkflowId) -> Result<Option<SnapshotRecord>, StorageError> {
        let row: Option<(i64, Vec<u8>, Vec<u8>)> = self
            .conn
            .query_row(
                "SELECT upto, meta, body FROM snapshots WHERE workflow = ?1 AND shard = ?2",
                params![workflow.as_str(), self.shard],
                |r| Ok((r.get(0)?, r.get(1)?, r.get(2)?)),
            )
            .optional()
            .map_err(db_err)?;
        match row {
            None => Ok(None),
            Some((upto, meta, body)) => {
                let upto = u64_col("snapshots.upto", upto)?;
                let meta: SnapshotMeta =
                    codec::from_slice(&meta, "snapshot meta").map_err(codec_err)?;
                Ok(Some(SnapshotRecord { upto, meta, body }))
            }
        }
    }

    fn read_records(
        &self,
        workflow: &WorkflowId,
    ) -> Result<BTreeMap<u64, JournalRecord>, StorageError> {
        let mut stmt = self
            .conn
            .prepare_cached(
                "SELECT idx, at, event FROM journal \
                 WHERE workflow = ?1 AND shard = ?2 ORDER BY idx",
            )
            .map_err(db_err)?;
        let rows = stmt
            .query_map(params![workflow.as_str(), self.shard], |r| {
                Ok((
                    r.get::<_, i64>(0)?,
                    r.get::<_, i64>(1)?,
                    r.get::<_, Vec<u8>>(2)?,
                ))
            })
            .map_err(db_err)?;
        let mut out = BTreeMap::new();
        for row in rows {
            let (idx, at, event) = row.map_err(db_err)?;
            let index = u64_col("journal.idx", idx)?;
            let at = u64_col("journal.at", at)?;
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

impl StorageShard for SqliteShard {
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
            // by an earlier sync, so the barrier holds trivially. No commit
            // happens, so no fsync is counted.
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
        // WAL/mem parity — appended data is visible before `sync`, with the
        // same last-wins semantics the committed inserts would have.
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
        let mut ids: BTreeSet<WorkflowId> = BTreeSet::new();
        {
            let mut stmt = self
                .conn
                .prepare_cached(
                    "SELECT workflow FROM journal WHERE shard = ?1 \
                     UNION SELECT workflow FROM snapshots WHERE shard = ?1",
                )
                .map_err(db_err)?;
            let rows = stmt
                .query_map(params![self.shard], |r| r.get::<_, String>(0))
                .map_err(db_err)?;
            for row in rows {
                ids.insert(WorkflowId::new(row.map_err(db_err)?));
            }
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
            .conn
            .execute(
                "DELETE FROM journal WHERE shard = ?1 AND idx < \
                 (SELECT s.upto FROM snapshots s \
                  WHERE s.workflow = journal.workflow AND s.shard = ?1)",
                params![self.shard],
            )
            .map_err(db_err)?;
        self.stats.segments_deleted += deleted as u64;
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
// Error plumbing: internal `thiserror` type, mapped to `StorageError` at the
// trait boundary.

/// Internal error classification for this backend.
#[derive(Debug, thiserror::Error)]
enum SqliteError {
    /// An underlying SQLite call failed.
    #[error("sqlite: {0}")]
    Sqlite(#[from] rusqlite::Error),
    /// A filesystem operation preparing the database path failed.
    #[error("io: {0}")]
    Io(#[from] std::io::Error),
    /// A `u64` does not fit SQLite's signed 64-bit INTEGER column.
    #[error("{what} value {value} exceeds SQLite's INTEGER range")]
    IntRange {
        /// Which column the value was destined for.
        what: &'static str,
        /// The out-of-range value.
        value: u64,
    },
}

impl From<SqliteError> for StorageError {
    fn from(e: SqliteError) -> Self {
        match e {
            SqliteError::Sqlite(err) => classify_sqlite(&err),
            SqliteError::Io(err) => StorageError::Disk(err.to_string()),
            e @ SqliteError::IntRange { .. } => StorageError::Unsupported(e.to_string()),
        }
    }
}

fn classify_sqlite(err: &rusqlite::Error) -> StorageError {
    use rusqlite::ffi::ErrorCode;
    let msg = err.to_string();
    match err {
        rusqlite::Error::SqliteFailure(f, _) => match f.code {
            ErrorCode::DiskFull => StorageError::DiskFull(msg),
            ErrorCode::DatabaseCorrupt | ErrorCode::NotADatabase => StorageError::Corrupt(msg),
            _ => StorageError::Disk(msg),
        },
        rusqlite::Error::FromSqlConversionFailure(..)
        | rusqlite::Error::IntegralValueOutOfRange(..)
        | rusqlite::Error::InvalidColumnType(..) => StorageError::Corrupt(msg),
        _ => StorageError::Disk(msg),
    }
}

fn db_err(e: rusqlite::Error) -> StorageError {
    SqliteError::from(e).into()
}

fn io_err(e: std::io::Error) -> StorageError {
    SqliteError::from(e).into()
}

fn codec_err(e: sqrl_core::Error) -> StorageError {
    match e {
        sqrl_core::Error::Codec { context, message } => {
            StorageError::Codec(format!("{context}: {message}"))
        }
        other => StorageError::Codec(other.to_string()),
    }
}

/// Checked `u64` → SQLite INTEGER; values above `i64::MAX` are rejected (they
/// would break `ORDER BY idx` / `idx >= cut` comparisons).
fn i64_col(what: &'static str, value: u64) -> Result<i64, StorageError> {
    i64::try_from(value).map_err(|_| SqliteError::IntRange { what, value }.into())
}

/// Checked SQLite INTEGER → `u64`; negative stored values mean tampering.
fn u64_col(what: &'static str, value: i64) -> Result<u64, StorageError> {
    u64::try_from(value)
        .map_err(|_| StorageError::Corrupt(format!("negative {what} value {value} in store")))
}
