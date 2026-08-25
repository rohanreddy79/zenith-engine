//! `SimDisk`: an in-memory [`Vfs`] with crash, torn-write, corruption,
//! disk-full, i/o-error, and slow-i/o fault injection.
//!
//! ## Durability model (deliberately harsher than real filesystems)
//!
//! * File data written via [`sqrl_core::vfs::VfsFile::write_at`] is
//!   **pending** until `sync()` on that file returns `Ok`.
//! * Namespace operations (create, delete, rename) are **pending** until
//!   `sync_dir()` of the parent directory returns `Ok`.
//! * On [`SimDisk::crash`], every pending item is independently kept,
//!   dropped, or (for data writes) **torn** — a prefix survives — chosen by
//!   the seeded RNG. There is no ordering guarantee between unsynced writes,
//!   matching worst-case page writeback.
//!
//! Storage code that survives this model on thousands of seeds is correct on
//! ext4/xfs/apfs, which are strictly kinder.

use crate::clock::SimClock;
use crate::rng::SimRng;
use sqrl_core::vfs::{Vfs, VfsError, VfsFile};
use std::collections::BTreeMap;
use std::sync::{Arc, Mutex, MutexGuard};
use std::time::Duration;

/// Probability/latency knobs for background fault injection. All faults are
/// drawn from the disk's seeded RNG, so a given seed produces a fixed fault
/// sequence.
#[derive(Debug, Clone)]
pub struct FaultConfig {
    /// Probability that any mutating op returns an I/O error.
    pub p_write_error: f64,
    /// Probability that a `sync` / `sync_dir` returns an I/O error (the data
    /// stays pending — like a failed fsync).
    pub p_sync_error: f64,
    /// Virtual latency charged per read op.
    pub read_latency: Duration,
    /// Virtual latency charged per write op.
    pub write_latency: Duration,
    /// Virtual latency charged per sync op.
    pub sync_latency: Duration,
    /// Total capacity in bytes; writes that would exceed it fail with
    /// [`VfsError::DiskFull`]. `None` = unbounded.
    pub capacity: Option<u64>,
    /// On crash: probability an unsynced data write survives intact.
    pub p_keep_unsynced: f64,
    /// On crash: probability a surviving unsynced write is torn (prefix
    /// only). Applied after `p_keep_unsynced`.
    pub p_torn: f64,
    /// On crash: probability an unsynced namespace op survives.
    pub p_keep_unsynced_ns: f64,
}

impl Default for FaultConfig {
    fn default() -> Self {
        FaultConfig {
            p_write_error: 0.0,
            p_sync_error: 0.0,
            read_latency: Duration::ZERO,
            write_latency: Duration::ZERO,
            sync_latency: Duration::ZERO,
            capacity: None,
            p_keep_unsynced: 0.5,
            p_torn: 0.25,
            p_keep_unsynced_ns: 0.5,
        }
    }
}

#[derive(Debug, Clone, Default)]
struct FileState {
    /// Content as of the last successful `sync`.
    durable: Vec<u8>,
    /// Writes since the last sync, in order.
    pending: Vec<(u64, Vec<u8>)>,
    /// Whether the *name* is durable (parent dir synced since creation).
    name_durable: bool,
}

impl FileState {
    /// The applied view (what reads see pre-crash).
    fn view(&self) -> Vec<u8> {
        let mut v = self.durable.clone();
        for (off, data) in &self.pending {
            apply_write(&mut v, *off, data);
        }
        v
    }
}

fn apply_write(buf: &mut Vec<u8>, off: u64, data: &[u8]) {
    let off = off as usize;
    let end = off + data.len();
    if buf.len() < end {
        buf.resize(end, 0);
    }
    buf[off..end].copy_from_slice(data);
}

/// Counters for assertions and benchmarks.
#[derive(Debug, Clone, Copy, Default, PartialEq, Eq)]
pub struct DiskStats {
    /// Mutating ops (writes, truncates, ns ops) attempted.
    pub write_ops: u64,
    /// Successful file syncs.
    pub syncs: u64,
    /// Successful dir syncs.
    pub dir_syncs: u64,
    /// Read ops.
    pub read_ops: u64,
    /// Bytes written (accepted).
    pub bytes_written: u64,
    /// Injected errors so far.
    pub injected_errors: u64,
}

#[derive(Debug)]
enum NsOp {
    Create(String),
    /// Deleted file's state is carried so an un-persisted delete can
    /// resurrect it on crash recovery.
    Delete(String, FileState),
    /// Overwritten target state is carried so an un-persisted rename can
    /// restore both names on crash recovery.
    Rename {
        from: String,
        to: String,
        overwritten: Option<FileState>,
    },
}

struct DiskState {
    files: BTreeMap<String, FileState>,
    /// Names present as of the last relevant `sync_dir`, mapped to their
    /// durable content at crash-resolution time. Rebuilt on crash.
    pending_ns: Vec<NsOp>,
    faults: FaultConfig,
    rng: SimRng,
    clock: Option<SimClock>,
    stats: DiskStats,
    /// Mutating-op counter for crash-point scheduling.
    op_count: u64,
    crash_at_op: Option<u64>,
    crashed: bool,
    op_log: Vec<String>,
}

impl DiskState {
    fn used_bytes(&self) -> u64 {
        self.files
            .values()
            .map(|f| f.view().len() as u64)
            .sum::<u64>()
    }

    fn charge(&mut self, d: Duration) {
        if let Some(c) = &self.clock {
            c.advance(d);
        }
    }

    fn check_crashed(&self, path: &str) -> Result<(), VfsError> {
        if self.crashed {
            Err(VfsError::io(path, "simulated crash: process is dead"))
        } else {
            Ok(())
        }
    }

    /// Count a mutating op; returns Err if this op hits the crash point.
    fn mutating_op(&mut self, path: &str) -> Result<(), VfsError> {
        self.check_crashed(path)?;
        self.op_count += 1;
        self.stats.write_ops += 1;
        if let Some(at) = self.crash_at_op {
            if self.op_count >= at {
                self.crashed = true;
                return Err(VfsError::io(path, "simulated crash at scheduled op"));
            }
        }
        let (p_err, lat) = (self.faults.p_write_error, self.faults.write_latency);
        self.charge(lat);
        if self.rng.chance(p_err) {
            self.stats.injected_errors += 1;
            return Err(VfsError::io(path, "injected write error"));
        }
        Ok(())
    }
}

/// The simulated disk. Cheap to clone; all clones view the same disk.
#[derive(Clone)]
pub struct SimDisk {
    state: Arc<Mutex<DiskState>>,
}

impl SimDisk {
    /// A disk with no background faults (crash still available via
    /// [`SimDisk::crash`]).
    pub fn new(seed: u64) -> Self {
        SimDisk::with_faults(seed, FaultConfig::default())
    }

    /// A disk with the given fault configuration.
    pub fn with_faults(seed: u64, faults: FaultConfig) -> Self {
        SimDisk {
            state: Arc::new(Mutex::new(DiskState {
                files: BTreeMap::new(),
                pending_ns: Vec::new(),
                faults,
                rng: SimRng::new(seed).fork("sim-disk"),
                clock: None,
                stats: DiskStats::default(),
                op_count: 0,
                crash_at_op: None,
                crashed: false,
                op_log: Vec::new(),
            })),
        }
    }

    /// Attach a clock so I/O latency advances virtual time.
    pub fn attach_clock(&self, clock: SimClock) {
        self.lock().clock = Some(clock);
    }

    /// Replace the fault configuration.
    pub fn set_faults(&self, faults: FaultConfig) {
        self.lock().faults = faults;
    }

    /// Schedule a crash: once `n` further mutating ops have been attempted,
    /// the disk "loses power" (that op and everything after fails).
    pub fn crash_after_ops(&self, n: u64) {
        let mut s = self.lock();
        let at = s.op_count + n.max(1);
        s.crash_at_op = Some(at);
    }

    /// Immediately crash: all subsequent operations fail until
    /// [`SimDisk::recover`].
    pub fn crash(&self) {
        self.lock().crashed = true;
    }

    /// Whether the disk is currently crashed.
    pub fn is_crashed(&self) -> bool {
        self.lock().crashed
    }

    /// Mutating ops attempted so far (for scheduling crash points).
    pub fn op_count(&self) -> u64 {
        self.lock().op_count
    }

    /// Resolve the crash: every pending (unsynced) item is kept, dropped, or
    /// torn per the seeded RNG; the disk becomes usable again, containing
    /// only what "survived power loss".
    pub fn recover(&self) {
        let mut s = self.lock();
        // Resolve namespace ops first (they gate file existence).
        let ops: Vec<NsOp> = std::mem::take(&mut s.pending_ns);
        for op in ops {
            let keep = s.rng.chance(s.faults.p_keep_unsynced_ns);
            match op {
                NsOp::Create(path) => {
                    if keep {
                        if let Some(f) = s.files.get_mut(&path) {
                            f.name_durable = true;
                        }
                    } else if let Some(f) = s.files.get(&path) {
                        if !f.name_durable {
                            s.files.remove(&path);
                        }
                    }
                }
                NsOp::Delete(path, old) => {
                    if !keep {
                        // The delete never hit disk: the file resurrects with
                        // its pre-delete state (pendings resolved below).
                        s.files.entry(path).or_insert(old);
                    }
                }
                NsOp::Rename {
                    from,
                    to,
                    overwritten,
                } => {
                    if keep {
                        if let Some(f) = s.files.get_mut(&to) {
                            f.name_durable = true;
                        }
                    } else {
                        // The rename never hit disk: move the file back and
                        // restore the overwritten target, if any.
                        if let Some(f) = s.files.remove(&to) {
                            s.files.insert(from, f);
                        }
                        if let Some(old) = overwritten {
                            s.files.insert(to, old);
                        }
                    }
                }
            }
        }
        // Resolve pending data writes per file.
        let (p_keep, p_torn) = (s.faults.p_keep_unsynced, s.faults.p_torn);
        let paths: Vec<String> = s.files.keys().cloned().collect();
        for path in paths {
            let pending = {
                let f = s
                    .files
                    .get_mut(&path)
                    .expect("file listed from state must exist");
                std::mem::take(&mut f.pending)
            };
            for (off, data) in pending {
                let keep = s.rng.chance(p_keep);
                if !keep {
                    continue;
                }
                let torn = s.rng.chance(p_torn);
                let kept: Vec<u8> = if torn && !data.is_empty() {
                    let n = s.rng.next_below(data.len() as u64) as usize;
                    data[..n].to_vec()
                } else {
                    data
                };
                let f = s
                    .files
                    .get_mut(&path)
                    .expect("file listed from state must exist");
                apply_write(&mut f.durable, off, &kept);
            }
        }
        s.crashed = false;
        s.crash_at_op = None;
        s.op_log.push("recover".to_string());
    }

    /// Flip bits at `offset` in the *durable* content of `path`
    /// (`durable[offset] ^= xor`). For corruption tests.
    pub fn corrupt(&self, path: &str, offset: u64, xor: u8) -> Result<(), VfsError> {
        let mut s = self.lock();
        let f = s
            .files
            .get_mut(path)
            .ok_or_else(|| VfsError::NotFound(path.to_string()))?;
        let off = offset as usize;
        if off >= f.durable.len() {
            return Err(VfsError::io(
                path,
                format!(
                    "corrupt offset {off} beyond durable len {}",
                    f.durable.len()
                ),
            ));
        }
        f.durable[off] ^= xor;
        Ok(())
    }

    /// Durable length of a file (what would survive a crash right now, if
    /// every pending write were dropped).
    pub fn durable_len(&self, path: &str) -> Option<u64> {
        self.lock().files.get(path).map(|f| f.durable.len() as u64)
    }

    /// A byte-exact snapshot of durable state: path → durable content, for
    /// files whose names are durable. Used by DST for byte-identical
    /// comparisons.
    pub fn durable_image(&self) -> BTreeMap<String, Vec<u8>> {
        let s = self.lock();
        s.files
            .iter()
            .filter(|(_, f)| f.name_durable)
            .map(|(p, f)| (p.clone(), f.durable.clone()))
            .collect()
    }

    /// A byte-exact snapshot of the *applied view* (durable + pending).
    pub fn view_image(&self) -> BTreeMap<String, Vec<u8>> {
        let s = self.lock();
        s.files.iter().map(|(p, f)| (p.clone(), f.view())).collect()
    }

    /// Disk stats.
    pub fn stats(&self) -> DiskStats {
        self.lock().stats
    }

    /// The op log (for determinism assertions).
    pub fn op_log(&self) -> Vec<String> {
        self.lock().op_log.clone()
    }

    fn lock(&self) -> MutexGuard<'_, DiskState> {
        self.state.lock().expect("sim disk lock poisoned")
    }
}

impl Vfs for SimDisk {
    fn open(&self, path: &str, create: bool) -> Result<Box<dyn VfsFile>, VfsError> {
        let mut s = self.lock();
        s.check_crashed(path)?;
        if !s.files.contains_key(path) {
            if !create {
                return Err(VfsError::NotFound(path.to_string()));
            }
            s.mutating_op(path)?;
            s.files.insert(path.to_string(), FileState::default());
            s.pending_ns.push(NsOp::Create(path.to_string()));
            s.op_log.push(format!("create {path}"));
        }
        Ok(Box::new(SimFile {
            disk: self.clone(),
            path: path.to_string(),
        }))
    }

    fn exists(&self, path: &str) -> Result<bool, VfsError> {
        let s = self.lock();
        s.check_crashed(path)?;
        Ok(s.files.contains_key(path))
    }

    fn delete(&self, path: &str) -> Result<(), VfsError> {
        let mut s = self.lock();
        s.mutating_op(path)?;
        let f = s
            .files
            .get(path)
            .ok_or_else(|| VfsError::NotFound(path.to_string()))?;
        if f.name_durable {
            // The view no longer sees the file, but until sync_dir the
            // delete is undecided: a crash may resurrect it.
            let old = s.files.remove(path).expect("checked contains_key above");
            s.pending_ns.push(NsOp::Delete(path.to_string(), old));
        } else {
            // Name never durable: create+delete cancel out entirely.
            s.files.remove(path);
            s.pending_ns
                .retain(|op| !matches!(op, NsOp::Create(p) if p == path));
        }
        s.op_log.push(format!("delete {path}"));
        Ok(())
    }

    fn rename(&self, from: &str, to: &str) -> Result<(), VfsError> {
        let mut s = self.lock();
        s.mutating_op(from)?;
        if !s.files.contains_key(from) {
            return Err(VfsError::NotFound(from.to_string()));
        }
        let f = s.files.remove(from).expect("checked contains_key above");
        let overwritten = s.files.insert(to.to_string(), f);
        s.pending_ns.push(NsOp::Rename {
            from: from.to_string(),
            to: to.to_string(),
            overwritten,
        });
        s.op_log.push(format!("rename {from} -> {to}"));
        Ok(())
    }

    fn list(&self, dir: &str) -> Result<Vec<String>, VfsError> {
        let s = self.lock();
        s.check_crashed(dir)?;
        let prefix = if dir.is_empty() || dir.ends_with('/') {
            dir.to_string()
        } else {
            format!("{dir}/")
        };
        let mut out: Vec<String> = s
            .files
            .keys()
            .filter_map(|p| {
                let rest = p.strip_prefix(&prefix)?;
                if rest.is_empty() || rest.contains('/') {
                    None
                } else {
                    Some(rest.to_string())
                }
            })
            .collect();
        out.sort();
        Ok(out)
    }

    fn create_dir_all(&self, dir: &str) -> Result<(), VfsError> {
        let s = self.lock();
        s.check_crashed(dir)?;
        // Directories are implicit in this namespace model.
        Ok(())
    }

    fn sync_dir(&self, dir: &str) -> Result<(), VfsError> {
        let mut s = self.lock();
        s.check_crashed(dir)?;
        s.op_count += 1;
        if let Some(at) = s.crash_at_op {
            if s.op_count >= at {
                s.crashed = true;
                return Err(VfsError::io(dir, "simulated crash at scheduled op"));
            }
        }
        let lat = s.faults.sync_latency;
        s.charge(lat);
        if s.rng.chance(s.faults.p_sync_error) {
            s.stats.injected_errors += 1;
            return Err(VfsError::io(dir, "injected dir-sync error"));
        }
        let prefix = if dir.is_empty() || dir.ends_with('/') {
            dir.to_string()
        } else {
            format!("{dir}/")
        };
        // Commit namespace ops touching this directory's direct children.
        let mut remaining = Vec::new();
        let ops = std::mem::take(&mut s.pending_ns);
        for op in ops {
            let touches = |p: &str| {
                p.strip_prefix(&prefix)
                    .map(|rest| !rest.contains('/'))
                    .unwrap_or(false)
            };
            let committed = match &op {
                NsOp::Create(p) | NsOp::Delete(p, _) => touches(p),
                NsOp::Rename { from, to, .. } => touches(from) || touches(to),
            };
            if committed {
                match op {
                    NsOp::Create(p) | NsOp::Rename { to: p, .. } => {
                        if let Some(f) = s.files.get_mut(&p) {
                            f.name_durable = true;
                        }
                    }
                    NsOp::Delete(_, _) => { /* removal is now final */ }
                }
            } else {
                remaining.push(op);
            }
        }
        s.pending_ns = remaining;
        s.stats.dir_syncs += 1;
        s.op_log.push(format!("sync_dir {dir}"));
        Ok(())
    }
}

/// An open handle to a file on [`SimDisk`].
pub struct SimFile {
    disk: SimDisk,
    path: String,
}

impl VfsFile for SimFile {
    fn read_at(&mut self, offset: u64, buf: &mut [u8]) -> Result<usize, VfsError> {
        let mut s = self.disk.lock();
        s.check_crashed(&self.path)?;
        s.stats.read_ops += 1;
        let lat = s.faults.read_latency;
        s.charge(lat);
        let f = s
            .files
            .get(&self.path)
            .ok_or_else(|| VfsError::NotFound(self.path.clone()))?;
        let view = f.view();
        let off = offset as usize;
        if off >= view.len() {
            return Ok(0);
        }
        let n = buf.len().min(view.len() - off);
        buf[..n].copy_from_slice(&view[off..off + n]);
        Ok(n)
    }

    fn write_at(&mut self, offset: u64, data: &[u8]) -> Result<(), VfsError> {
        let mut s = self.disk.lock();
        s.mutating_op(&self.path)?;
        if let Some(cap) = s.faults.capacity {
            let new_end = offset + data.len() as u64;
            let cur = s
                .files
                .get(&self.path)
                .map(|f| f.view().len() as u64)
                .unwrap_or(0);
            let growth = new_end.saturating_sub(cur);
            if s.used_bytes() + growth > cap {
                return Err(VfsError::DiskFull(self.path.clone()));
            }
        }
        let bytes = data.len() as u64;
        let f = s
            .files
            .get_mut(&self.path)
            .ok_or_else(|| VfsError::NotFound(self.path.clone()))?;
        f.pending.push((offset, data.to_vec()));
        s.stats.bytes_written += bytes;
        s.op_log
            .push(format!("write {} @{offset} +{bytes}", self.path));
        Ok(())
    }

    fn len(&mut self) -> Result<u64, VfsError> {
        let s = self.disk.lock();
        s.check_crashed(&self.path)?;
        let f = s
            .files
            .get(&self.path)
            .ok_or_else(|| VfsError::NotFound(self.path.clone()))?;
        Ok(f.view().len() as u64)
    }

    fn truncate(&mut self, len: u64) -> Result<(), VfsError> {
        let mut s = self.disk.lock();
        s.mutating_op(&self.path)?;
        let f = s
            .files
            .get_mut(&self.path)
            .ok_or_else(|| VfsError::NotFound(self.path.clone()))?;
        // Truncation is modeled as immediately collapsing pending state:
        // apply pending, cut, and store as a single pending rewrite.
        let mut v = f.view();
        v.truncate(len as usize);
        f.pending.clear();
        f.pending.push((0, v.clone()));
        // A truncate also implicitly bounds durable content: a crash may
        // still resurrect the longer durable tail — callers must sync after
        // truncate, which the WAL recovery path does.
        s.op_log.push(format!("truncate {} to {len}", self.path));
        Ok(())
    }

    fn sync(&mut self) -> Result<(), VfsError> {
        let mut s = self.disk.lock();
        s.check_crashed(&self.path)?;
        s.op_count += 1;
        if let Some(at) = s.crash_at_op {
            if s.op_count >= at {
                s.crashed = true;
                return Err(VfsError::io(&self.path, "simulated crash at scheduled op"));
            }
        }
        let lat = s.faults.sync_latency;
        s.charge(lat);
        if s.rng.chance(s.faults.p_sync_error) {
            s.stats.injected_errors += 1;
            return Err(VfsError::io(&self.path, "injected fsync error"));
        }
        let f = s
            .files
            .get_mut(&self.path)
            .ok_or_else(|| VfsError::NotFound(self.path.clone()))?;
        // fsync makes the file's *content* durable (durable := applied view,
        // including any truncation), but not its directory entry.
        let v = f.view();
        f.durable = v;
        f.pending.clear();
        s.stats.syncs += 1;
        s.op_log.push(format!("sync {}", self.path));
        Ok(())
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    fn write_all(disk: &SimDisk, path: &str, data: &[u8]) {
        let mut f = disk.open(path, true).unwrap();
        f.write_at(0, data).unwrap();
    }

    #[test]
    fn synced_data_survives_crash() {
        let disk = SimDisk::new(1);
        write_all(&disk, "wal/seg-0", b"hello");
        disk.open("wal/seg-0", false).unwrap().sync().unwrap();
        disk.sync_dir("wal").unwrap();
        disk.crash();
        disk.recover();
        let mut f = disk.open("wal/seg-0", false).unwrap();
        let mut buf = [0u8; 5];
        assert_eq!(f.read_at(0, &mut buf).unwrap(), 5);
        assert_eq!(&buf, b"hello");
    }

    #[test]
    fn unsynced_data_can_vanish() {
        let mut cfg = FaultConfig::default();
        cfg.p_keep_unsynced = 0.0; // always drop unsynced
        cfg.p_keep_unsynced_ns = 0.0;
        let disk = SimDisk::with_faults(2, cfg);
        write_all(&disk, "f", b"doomed");
        disk.crash();
        disk.recover();
        assert!(!disk.exists("f").unwrap(), "unsynced create must vanish");
    }

    #[test]
    fn unsynced_data_can_be_torn() {
        let mut cfg = FaultConfig::default();
        cfg.p_keep_unsynced = 1.0;
        cfg.p_torn = 1.0;
        cfg.p_keep_unsynced_ns = 1.0;
        let disk = SimDisk::with_faults(3, cfg);
        write_all(&disk, "f", &[7u8; 100]);
        disk.crash();
        disk.recover();
        let n = disk.durable_len("f").unwrap();
        assert!(n < 100, "write must be torn, got len {n}");
    }

    #[test]
    fn crash_after_ops_fires() {
        let disk = SimDisk::new(4);
        write_all(&disk, "a", b"x"); // create+write = 2 mutating ops
        disk.crash_after_ops(1);
        let mut f = disk.open("a", false).unwrap();
        assert!(f.write_at(1, b"y").is_err(), "op at crash point must fail");
        assert!(disk.is_crashed());
        assert!(disk.open("a", false).is_err());
    }

    #[test]
    fn disk_full() {
        let mut cfg = FaultConfig::default();
        cfg.capacity = Some(10);
        let disk = SimDisk::with_faults(5, cfg);
        let mut f = disk.open("f", true).unwrap();
        f.write_at(0, &[0u8; 8]).unwrap();
        match f.write_at(8, &[0u8; 8]) {
            Err(VfsError::DiskFull(_)) => {}
            other => panic!("expected DiskFull, got {other:?}"),
        }
    }

    #[test]
    fn corruption_flips_durable_bytes() {
        let disk = SimDisk::new(6);
        write_all(&disk, "f", b"abcd");
        disk.open("f", false).unwrap().sync().unwrap();
        disk.corrupt("f", 1, 0xFF).unwrap();
        let mut f = disk.open("f", false).unwrap();
        let mut buf = [0u8; 4];
        f.read_at(0, &mut buf).unwrap();
        assert_eq!(buf[0], b'a');
        assert_ne!(buf[1], b'b');
    }

    #[test]
    fn latency_advances_clock() {
        let clock = SimClock::default();
        let mut cfg = FaultConfig::default();
        cfg.write_latency = Duration::from_millis(3);
        cfg.sync_latency = Duration::from_millis(10);
        let disk = SimDisk::with_faults(7, cfg);
        disk.attach_clock(clock.clone());
        write_all(&disk, "f", b"x"); // create + write = 2 mutating ops => 6ms
        disk.open("f", false).unwrap().sync().unwrap(); // +10ms
        use sqrl_core::Clock;
        assert_eq!(clock.now().as_millis(), 16);
    }

    #[test]
    fn same_seed_same_crash_resolution() {
        let run = |seed: u64| {
            let disk = SimDisk::new(seed);
            for i in 0..20u8 {
                write_all(&disk, &format!("f{i}"), &[i; 64]);
            }
            disk.crash();
            disk.recover();
            disk.durable_image()
        };
        assert_eq!(run(11), run(11));
        // and at least one nearby seed resolves differently
        assert!((12..22).any(|s| run(s) != run(11)));
    }

    #[test]
    fn rename_is_atomic_across_crash() {
        for seed in 0..20 {
            let disk = SimDisk::new(seed);
            write_all(&disk, "manifest.tmp", b"v2");
            disk.open("manifest.tmp", false).unwrap().sync().unwrap();
            disk.sync_dir("").unwrap();
            disk.rename("manifest.tmp", "manifest").unwrap();
            // no sync_dir: rename durability is undecided
            disk.crash();
            disk.recover();
            let has_new = disk.exists("manifest").unwrap();
            let has_old = disk.exists("manifest.tmp").unwrap();
            assert!(
                has_new ^ has_old,
                "seed {seed}: rename must resolve to exactly one name (new={has_new}, old={has_old})"
            );
        }
    }
}
