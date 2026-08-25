//! `WalStorage`: the default embedded storage backend.
//!
//! A store directory contains `sqrl.meta` plus one directory per shard;
//! each shard owns a sequence of checksummed, append-only segment files
//! (`wal-<seq>.sqrl`) and a `MANIFEST` listing the live ones. All I/O goes
//! through the [`Vfs`] trait, so the exact same code runs on real disks and
//! on the fault-injecting `SimDisk`.
//!
//! Durability protocol (see `docs/on-disk-format.md`):
//!
//! * appends are buffered writes; [`WalShard::sync`] (fsync) is the only
//!   durability barrier — the engine acknowledges nothing before it,
//! * recovery scans segments in order and truncates at the first invalid
//!   record, logging the byte offset,
//! * the manifest is advisory: if missing or corrupt, recovery falls back to
//!   a directory scan,
//! * a segment becomes GC-eligible only when no workflow's live tail —
//!   records or *synced* snapshot — references it.

use crate::codec::{self, DecodeEnd, SegmentHeader, WalRecord};
use crate::manifest::{self, join, Manifest, StoreMeta};
use sqrl_core::codec::SQRL_FORMAT_VERSION;
use sqrl_core::snapshot::SnapshotRecord;
use sqrl_core::storage::{AppendEntry, AppendPayload, JournalReadout, StorageStats};
use sqrl_core::vfs::{Vfs, VfsError, VfsFile};
use sqrl_core::{Storage, StorageError, StorageShard, WorkflowId};
use std::collections::{BTreeMap, BTreeSet};
use std::sync::Arc;

/// Options for creating/opening a [`WalStorage`].
#[derive(Debug, Clone)]
pub struct WalOptions {
    /// Shards to create (ignored when opening an existing store — the stored
    /// value wins; a mismatch is an error only if the store cannot satisfy
    /// placement).
    pub num_shards: u32,
    /// Roll segments at this size.
    pub segment_size: u64,
}

impl Default for WalOptions {
    fn default() -> Self {
        WalOptions {
            num_shards: 1,
            segment_size: 64 * 1024 * 1024,
        }
    }
}

/// The embedded WAL storage backend.
pub struct WalStorage {
    vfs: Arc<dyn Vfs>,
    meta: StoreMeta,
    opts: WalOptions,
}

impl WalStorage {
    /// Open (or create) a store rooted at `path` on the real filesystem with
    /// default options.
    pub fn open(path: impl Into<std::path::PathBuf>) -> Result<Self, StorageError> {
        WalStorage::open_with(
            Arc::new(crate::vfs_std::StdVfs::new(path)?),
            WalOptions::default(),
        )
    }

    /// Open (or create) a store on any VFS.
    pub fn open_with(vfs: Arc<dyn Vfs>, opts: WalOptions) -> Result<Self, StorageError> {
        vfs.create_dir_all("").map_err(disk_err)?;
        let meta = match manifest::read_meta(vfs.as_ref(), "")? {
            Some(meta) => {
                if meta.format_version > SQRL_FORMAT_VERSION {
                    return Err(StorageError::Corrupt(format!(
                        "store format version {} is newer than supported {}",
                        meta.format_version, SQRL_FORMAT_VERSION
                    )));
                }
                meta
            }
            None => {
                let meta = StoreMeta {
                    format_version: SQRL_FORMAT_VERSION,
                    num_shards: opts.num_shards.max(1),
                };
                manifest::write_meta(vfs.as_ref(), "", &meta)?;
                meta
            }
        };
        Ok(WalStorage { vfs, meta, opts })
    }
}

impl Storage for WalStorage {
    fn num_shards(&self) -> usize {
        self.meta.num_shards as usize
    }

    fn open_shard(&self, shard: usize) -> Result<Box<dyn StorageShard>, StorageError> {
        if shard >= self.meta.num_shards as usize {
            return Err(StorageError::Unsupported(format!(
                "shard {shard} out of range ({} shards)",
                self.meta.num_shards
            )));
        }
        Ok(Box::new(WalShard::open(
            Arc::clone(&self.vfs),
            shard as u32,
            self.opts.clone(),
        )?))
    }
}

// ---------------------------------------------------------------------------

#[derive(Debug, Clone, Copy)]
struct RecLoc {
    index: u64,
    seg: u64,
    offset: u64,
}

#[derive(Debug, Clone, Copy)]
struct SnapLoc {
    seg: u64,
    offset: u64,
    synced: bool,
}

#[derive(Debug, Default)]
struct WfIndex {
    snapshot: Option<SnapLoc>,
    records: Vec<RecLoc>,
}

/// One shard of a [`WalStorage`], exclusively owned by one engine core.
pub struct WalShard {
    vfs: Arc<dyn Vfs>,
    dir: String,
    shard: u32,
    opts: WalOptions,
    manifest: Manifest,
    current_seg: u64,
    current_file: Box<dyn VfsFile>,
    current_offset: u64,
    index: BTreeMap<WorkflowId, WfIndex>,
    poisoned: Option<StorageError>,
    stats: StorageStats,
}

impl WalShard {
    fn open(vfs: Arc<dyn Vfs>, shard: u32, opts: WalOptions) -> Result<Self, StorageError> {
        let dir = format!("shard-{shard}");
        vfs.create_dir_all(&dir).map_err(disk_err)?;
        // Authoritative segment list: manifest if present, else directory
        // scan; tail segments beyond the manifest are merged in (a crash can
        // land between segment creation and the manifest rewrite).
        let scanned = scan_dir_segments(vfs.as_ref(), &dir)?;
        let mut m = match manifest::read_manifest(vfs.as_ref(), &dir)? {
            Some(mut m) => {
                let max = m.segments.iter().copied().max().unwrap_or(0);
                for seg in &scanned {
                    if *seg > max && !m.segments.contains(seg) {
                        tracing::warn!(shard, seg, "adopting tail segment missing from manifest");
                        m.segments.push(*seg);
                    }
                }
                m.segments.sort_unstable();
                // Stale files not in the manifest (e.g. resurrected after a
                // crashed GC) are deleted, best-effort.
                for seg in &scanned {
                    if !m.segments.contains(seg) {
                        tracing::warn!(shard, seg, "deleting stale segment not in manifest");
                        let _ = vfs.delete(&join(&dir, &seg_name(*seg)));
                    }
                }
                m.next_segment_seq = m.next_segment_seq.max(max + 1);
                m
            }
            None => Manifest {
                next_segment_seq: scanned.iter().copied().max().unwrap_or(0) + 1,
                segments: scanned.clone(),
            },
        };

        // Scan all live segments in order, building the per-workflow index.
        let mut index: BTreeMap<WorkflowId, WfIndex> = BTreeMap::new();
        let mut stats = StorageStats::default();
        let mut truncated_from: Option<u64> = None; // first bad segment
        let mut last_valid: Option<(u64, u64)> = None; // (seg, end offset)
        let seg_list = m.segments.clone();
        for (pos, seg) in seg_list.iter().copied().enumerate() {
            if let Some(bad) = truncated_from {
                // Everything after the first invalid record is suspect: the
                // WAL is a single logical stream. Drop later segments.
                tracing::warn!(
                    shard,
                    seg,
                    after_bad = bad,
                    "dropping segment after corruption point"
                );
                let _ = vfs.delete(&join(&dir, &seg_name(seg)));
                m.segments.retain(|s| *s != seg);
                continue;
            }
            let path = join(&dir, &seg_name(seg));
            let buf = match read_all(vfs.as_ref(), &path) {
                Ok(b) => b,
                Err(StorageError::Disk(msg)) if msg.contains("not found") => {
                    // Manifest may list a segment created but never written
                    // (crash between manifest update and file creation).
                    tracing::warn!(shard, seg, "segment listed in manifest but missing on disk");
                    m.segments.retain(|s| *s != seg);
                    continue;
                }
                Err(e) => return Err(e),
            };
            let (records, end) = codec::scan(&buf);
            let mut valid_end = 0u64;
            for (offset, rec) in records {
                match rec {
                    WalRecord::SegmentHeader(h) => {
                        if h.segment_seq != seg || h.magic != "sqrl-seg" {
                            tracing::warn!(shard, seg, "segment header mismatch; truncating");
                            truncated_from = Some(seg);
                            break;
                        }
                    }
                    WalRecord::Entry(e) => {
                        let wf = index.entry(e.workflow.clone()).or_default();
                        wf.records.push(RecLoc {
                            index: e.record.index,
                            seg,
                            offset,
                        });
                        stats.records_appended += 1;
                    }
                    WalRecord::Snapshot(s) => {
                        let wf = index.entry(s.workflow.clone()).or_default();
                        wf.snapshot = Some(SnapLoc {
                            seg,
                            offset,
                            synced: true, // it is on disk and validated
                        });
                        wf.records.retain(|r| r.index >= s.snapshot.upto);
                    }
                }
                valid_end = offset + record_total_len(&buf, offset);
            }
            let cut = match end {
                // A torn tail record (crash mid-append) is dead bytes and
                // MUST be cut off now: if appends resumed after it, the
                // garbage would sit mid-stream and the *next* recovery
                // would read it as corruption and truncate away durably
                // acknowledged history behind it.
                DecodeEnd::Eof => buf.len() as u64 > valid_end,
                DecodeEnd::Invalid { offset, reason } => {
                    tracing::warn!(
                        shard,
                        seg,
                        offset,
                        reason,
                        "WAL corruption: truncating segment at byte offset"
                    );
                    true
                }
            };
            if cut && valid_end > 0 {
                // Truncate the file to the last valid record boundary.
                tracing::warn!(shard, seg, valid_end, "truncating segment tail");
                let mut f = vfs.open(&path, false).map_err(disk_err)?;
                f.truncate(valid_end).map_err(disk_err)?;
                f.sync().map_err(disk_err)?;
                stats.fsyncs += 1;
            }
            if valid_end == 0 {
                // Not even a valid segment header survived (torn create,
                // header mismatch, or corruption at byte 0): the segment is
                // dead — delete it rather than adopting a headerless tail.
                tracing::warn!(shard, seg, "segment has no valid header; deleting");
                let _ = vfs.delete(&join(&dir, &seg_name(seg)));
                m.segments.retain(|s| *s != seg);
                if pos + 1 < seg_list.len() {
                    truncated_from = Some(seg);
                }
            } else {
                last_valid = Some((seg, valid_end));
                if cut && pos + 1 < seg_list.len() {
                    // A cut inside a *sealed* (non-tail) segment breaks the
                    // logical stream like corruption does.
                    truncated_from = Some(seg);
                }
            }
        }

        // Recovery hardening: everything the index now references was read
        // through the page cache and may include a previous process's
        // un-fsynced writes (visible to us, not durable). Acknowledgments
        // will be issued on top of this history, so make ALL of it durable
        // before accepting a single new append — fsync every live segment
        // and the directory. (The moral equivalent of fsync-on-recovery in
        // SQLite/PostgreSQL; found by DST seed 3.)
        for seg in &m.segments {
            let mut f = vfs
                .open(&join(&dir, &seg_name(*seg)), false)
                .map_err(disk_err)?;
            f.sync().map_err(disk_err)?;
            stats.fsyncs += 1;
        }
        vfs.sync_dir(&dir).map_err(disk_err)?;

        // Open (or create) the tail segment for appending.
        let (current_seg, current_file, current_offset) = match last_valid {
            Some((seg, end)) if m.segments.contains(&seg) => {
                let f = vfs
                    .open(&join(&dir, &seg_name(seg)), false)
                    .map_err(disk_err)?;
                (seg, f, end)
            }
            _ => {
                let seg = m.next_segment_seq;
                m.next_segment_seq += 1;
                m.segments.push(seg);
                manifest::write_manifest(vfs.as_ref(), &dir, &m)?;
                let (f, off) = create_segment(vfs.as_ref(), &dir, seg, shard)?;
                (seg, f, off)
            }
        };
        // Persist any manifest repairs made during recovery.
        manifest::write_manifest(vfs.as_ref(), &dir, &m)?;
        stats.live_segments = m.segments.len() as u64;

        Ok(WalShard {
            vfs,
            dir,
            shard,
            opts,
            manifest: m,
            current_seg,
            current_file,
            current_offset,
            index,
            poisoned: None,
            stats,
        })
    }

    fn roll_segment(&mut self) -> Result<(), StorageError> {
        // Seal the old segment: everything in it becomes durable.
        self.current_file.sync().map_err(disk_err)?;
        self.stats.fsyncs += 1;
        self.mark_synced();
        // Manifest first: a crash after this point must still find the new
        // segment (or tolerate its absence — both paths are handled in open).
        let seg = self.manifest.next_segment_seq;
        self.manifest.next_segment_seq += 1;
        self.manifest.segments.push(seg);
        manifest::write_manifest(self.vfs.as_ref(), &self.dir, &self.manifest)?;
        let (f, off) = create_segment(self.vfs.as_ref(), &self.dir, seg, self.shard)?;
        self.current_seg = seg;
        self.current_file = f;
        self.current_offset = off;
        self.stats.live_segments = self.manifest.segments.len() as u64;
        Ok(())
    }

    fn mark_synced(&mut self) {
        for wf in self.index.values_mut() {
            if let Some(s) = &mut wf.snapshot {
                s.synced = true;
            }
        }
    }

    fn read_segment(&mut self, seg: u64) -> Result<Vec<u8>, StorageError> {
        read_all(self.vfs.as_ref(), &join(&self.dir, &seg_name(seg)))
    }
}

impl StorageShard for WalShard {
    fn append(&mut self, entries: &[AppendEntry]) -> Result<(), StorageError> {
        if let Some(e) = &self.poisoned {
            return Err(e.clone());
        }
        let result = (|| -> Result<(), StorageError> {
            let mut batch: Vec<u8> = Vec::new();
            let mut batch_start = self.current_offset;
            for entry in entries {
                // Roll when the current segment is full (flush batch first).
                if self.current_offset + batch.len() as u64 >= self.opts.segment_size {
                    if !batch.is_empty() {
                        self.current_file
                            .write_at(batch_start, &batch)
                            .map_err(disk_err)?;
                        self.current_offset = batch_start + batch.len() as u64;
                        self.stats.bytes_written += batch.len() as u64;
                        batch.clear();
                    }
                    self.roll_segment()?;
                    batch_start = self.current_offset;
                }
                // Serialize straight into the batch buffer: no record clone,
                // no intermediate payload allocation (measured in
                // docs/benchmarks.md, "Profiling findings").
                let offset = batch_start + batch.len() as u64;
                let loc_kind = match &entry.payload {
                    AppendPayload::Record(rec) => {
                        codec::encode_entry_into(&mut batch, &entry.workflow, rec)?;
                        LocKind::Record(rec.index)
                    }
                    AppendPayload::Snapshot(snap) => {
                        codec::encode_snapshot_into(&mut batch, &entry.workflow, snap)?;
                        LocKind::Snapshot(snap.upto)
                    }
                };
                let wf = self.index.entry(entry.workflow.clone()).or_default();
                match loc_kind {
                    LocKind::Record(idx) => {
                        wf.records.push(RecLoc {
                            index: idx,
                            seg: self.current_seg,
                            offset,
                        });
                    }
                    LocKind::Snapshot(upto) => {
                        wf.snapshot = Some(SnapLoc {
                            seg: self.current_seg,
                            offset,
                            synced: false,
                        });
                        wf.records.retain(|r| r.index >= upto);
                    }
                }
                self.stats.records_appended += 1;
            }
            if !batch.is_empty() {
                self.current_file
                    .write_at(batch_start, &batch)
                    .map_err(disk_err)?;
                self.current_offset = batch_start + batch.len() as u64;
                self.stats.bytes_written += batch.len() as u64;
            }
            Ok(())
        })();
        if let Err(e) = &result {
            self.poisoned = Some(e.clone());
        }
        result
    }

    fn sync(&mut self) -> Result<(), StorageError> {
        if let Some(e) = &self.poisoned {
            return Err(e.clone());
        }
        match self.current_file.sync() {
            Ok(()) => {
                self.stats.fsyncs += 1;
                self.mark_synced();
                Ok(())
            }
            Err(e) => {
                let err = disk_err(e);
                self.poisoned = Some(err.clone());
                Err(err)
            }
        }
    }

    fn read(&mut self, workflow: &WorkflowId) -> Result<JournalReadout, StorageError> {
        let Some(wf) = self.index.get(workflow) else {
            return Err(StorageError::UnknownWorkflow(workflow.to_string()));
        };
        let snapshot_loc = wf.snapshot;
        let rec_locs = wf.records.clone();
        // Read each involved segment once.
        let mut segs: BTreeSet<u64> = rec_locs.iter().map(|r| r.seg).collect();
        if let Some(s) = snapshot_loc {
            segs.insert(s.seg);
        }
        let mut seg_data: BTreeMap<u64, Vec<u8>> = BTreeMap::new();
        for seg in segs {
            seg_data.insert(seg, self.read_segment(seg)?);
        }
        let snapshot: Option<SnapshotRecord> = match snapshot_loc {
            None => None,
            Some(loc) => {
                let buf = seg_data
                    .get(&loc.seg)
                    .ok_or_else(|| StorageError::Corrupt("segment vanished".into()))?;
                match codec::decode_one(&buf[loc.offset as usize..], loc.offset) {
                    Ok(Some((WalRecord::Snapshot(s), _))) => Some(s.snapshot),
                    other => {
                        return Err(StorageError::Corrupt(format!(
                            "snapshot record unreadable at seg {} offset {}: {other:?}",
                            loc.seg, loc.offset
                        )))
                    }
                }
            }
        };
        let cut = snapshot.as_ref().map(|s| s.upto).unwrap_or(0);
        let mut records = Vec::with_capacity(rec_locs.len());
        for loc in rec_locs {
            if loc.index < cut {
                continue;
            }
            let buf = seg_data
                .get(&loc.seg)
                .ok_or_else(|| StorageError::Corrupt("segment vanished".into()))?;
            match codec::decode_one(&buf[loc.offset as usize..], loc.offset) {
                Ok(Some((WalRecord::Entry(e), _))) => records.push(e.record),
                other => {
                    return Err(StorageError::Corrupt(format!(
                        "journal record unreadable at seg {} offset {}: {other:?}",
                        loc.seg, loc.offset
                    )))
                }
            }
        }
        records.sort_by_key(|r| r.index);
        Ok(JournalReadout { snapshot, records })
    }

    fn list(&mut self) -> Result<Vec<WorkflowId>, StorageError> {
        Ok(self.index.keys().cloned().collect())
    }

    fn maintain(&mut self) -> Result<(), StorageError> {
        if self.poisoned.is_some() {
            return Ok(());
        }
        // A segment is live if any workflow references it (records or
        // snapshot — synced snapshots free *older* segments; unsynced ones
        // still pin their own), or it is the current tail.
        let mut referenced: BTreeSet<u64> = BTreeSet::new();
        referenced.insert(self.current_seg);
        for wf in self.index.values() {
            for r in &wf.records {
                referenced.insert(r.seg);
            }
            if let Some(s) = &wf.snapshot {
                referenced.insert(s.seg);
                if !s.synced {
                    // Not durable yet: the records it would supersede were
                    // already pruned from the index at append time, but the
                    // segments holding them must survive until the snapshot
                    // is synced. Conservative: pin everything up to the
                    // snapshot's segment.
                    for seg in &self.manifest.segments {
                        if *seg <= s.seg {
                            referenced.insert(*seg);
                        }
                    }
                }
            }
        }
        let dead: Vec<u64> = self
            .manifest
            .segments
            .iter()
            .copied()
            .filter(|s| !referenced.contains(s))
            .collect();
        if dead.is_empty() {
            return Ok(());
        }
        // Rewrite the manifest first: a crash mid-GC must not leave the
        // manifest referencing deleted files as live history.
        self.manifest.segments.retain(|s| !dead.contains(s));
        manifest::write_manifest(self.vfs.as_ref(), &self.dir, &self.manifest)?;
        for seg in dead {
            match self.vfs.delete(&join(&self.dir, &seg_name(seg))) {
                Ok(()) => self.stats.segments_deleted += 1,
                Err(e) => tracing::warn!(seg, error = %e, "segment delete failed (will retry)"),
            }
        }
        let _ = self.vfs.sync_dir(&self.dir);
        self.stats.live_segments = self.manifest.segments.len() as u64;
        Ok(())
    }

    fn stats(&self) -> StorageStats {
        self.stats
    }
}

enum LocKind {
    Record(u64),
    Snapshot(u64),
}

fn seg_name(seq: u64) -> String {
    format!("wal-{seq:020}.sqrl")
}

fn parse_seg_name(name: &str) -> Option<u64> {
    name.strip_prefix("wal-")?
        .strip_suffix(".sqrl")?
        .parse()
        .ok()
}

fn scan_dir_segments(vfs: &dyn Vfs, dir: &str) -> Result<Vec<u64>, StorageError> {
    let mut segs: Vec<u64> = vfs
        .list(dir)
        .map_err(disk_err)?
        .iter()
        .filter_map(|n| parse_seg_name(n))
        .collect();
    segs.sort_unstable();
    Ok(segs)
}

fn create_segment(
    vfs: &dyn Vfs,
    dir: &str,
    seg: u64,
    shard: u32,
) -> Result<(Box<dyn VfsFile>, u64), StorageError> {
    let path = join(dir, &seg_name(seg));
    let mut f = vfs.open(&path, true).map_err(disk_err)?;
    vfs.sync_dir(dir).map_err(disk_err)?;
    let header = codec::encode(&WalRecord::SegmentHeader(SegmentHeader {
        magic: "sqrl-seg".into(),
        segment_seq: seg,
        shard,
    }))?;
    f.write_at(0, &header).map_err(disk_err)?;
    Ok((f, header.len() as u64))
}

fn read_all(vfs: &dyn Vfs, path: &str) -> Result<Vec<u8>, StorageError> {
    let mut f = vfs.open(path, false).map_err(disk_err)?;
    let len = f.len().map_err(disk_err)?;
    let mut buf = vec![0u8; len as usize];
    let mut read = 0usize;
    while read < buf.len() {
        let n = f.read_at(read as u64, &mut buf[read..]).map_err(disk_err)?;
        if n == 0 {
            break;
        }
        read += n;
    }
    buf.truncate(read);
    Ok(buf)
}

fn record_total_len(buf: &[u8], offset: u64) -> u64 {
    let o = offset as usize;
    if buf.len() < o + 4 {
        return 0;
    }
    let len = u32::from_le_bytes([buf[o], buf[o + 1], buf[o + 2], buf[o + 3]]);
    8 + u64::from(len)
}

fn disk_err(e: VfsError) -> StorageError {
    match e {
        VfsError::DiskFull(p) => StorageError::DiskFull(p),
        VfsError::NotFound(p) => StorageError::Disk(format!("not found: {p}")),
        other => StorageError::Disk(other.to_string()),
    }
}
