//! Store metadata and per-shard manifests, written with the
//! atomic-rewrite protocol: write `<name>.tmp`, fsync it, rename over
//! `<name>`, fsync the directory. Both files are checksummed; a corrupt or
//! missing manifest degrades to a directory scan, never to data loss.

use sqrl_core::vfs::Vfs;
use sqrl_core::StorageError;

/// Magic prefix of the store meta file.
pub const META_MAGIC: &[u8; 8] = b"sqrlmeta";
/// Magic prefix of shard manifests.
pub const MANIFEST_MAGIC: &[u8; 8] = b"sqrlmnfs";

/// Store-wide metadata (`sqrl.meta` at the store root). Immutable after
/// creation.
#[derive(Debug, Clone, PartialEq, Eq, serde::Serialize, serde::Deserialize)]
pub struct StoreMeta {
    /// On-disk format version (see `docs/on-disk-format.md`).
    pub format_version: u8,
    /// Number of shards; fixed at creation. Workflow→shard placement uses
    /// `WorkflowId::shard(num_shards)`, so this must never change.
    pub num_shards: u32,
}

/// A shard's manifest: the authoritative list of live segments.
#[derive(Debug, Clone, PartialEq, Eq, Default, serde::Serialize, serde::Deserialize)]
pub struct Manifest {
    /// Live segment sequence numbers, ascending.
    pub segments: Vec<u64>,
    /// Next segment sequence number to allocate.
    pub next_segment_seq: u64,
}

fn encode_magic(magic: &[u8; 8], payload: &[u8]) -> Vec<u8> {
    let mut out = Vec::with_capacity(16 + payload.len());
    out.extend_from_slice(magic);
    out.extend_from_slice(&(payload.len() as u32).to_le_bytes());
    let crc = crc32c::crc32c(payload);
    out.extend_from_slice(&crc.to_le_bytes());
    out.extend_from_slice(payload);
    out
}

fn decode_magic<'a>(magic: &[u8; 8], buf: &'a [u8]) -> Result<&'a [u8], StorageError> {
    if buf.len() < 16 || &buf[..8] != magic {
        return Err(StorageError::Corrupt("bad magic".into()));
    }
    let len = u32::from_le_bytes([buf[8], buf[9], buf[10], buf[11]]) as usize;
    let crc_stored = u32::from_le_bytes([buf[12], buf[13], buf[14], buf[15]]);
    if buf.len() < 16 + len {
        return Err(StorageError::Corrupt(format!(
            "truncated: need {} bytes, have {}",
            16 + len,
            buf.len()
        )));
    }
    let payload = &buf[16..16 + len];
    if crc32c::crc32c(payload) != crc_stored {
        return Err(StorageError::Corrupt("crc mismatch".into()));
    }
    Ok(payload)
}

/// Atomically (re)write a checksummed file: tmp + fsync + rename + dir fsync.
pub fn write_atomic(
    vfs: &dyn Vfs,
    dir: &str,
    name: &str,
    magic: &[u8; 8],
    payload: &[u8],
) -> Result<(), StorageError> {
    let final_path = join(dir, name);
    let tmp_path = join(dir, &format!("{name}.tmp"));
    let bytes = encode_magic(magic, payload);
    let mut f = vfs
        .open(&tmp_path, true)
        .map_err(|e| StorageError::Disk(e.to_string()))?;
    f.truncate(0).map_err(disk)?;
    f.write_at(0, &bytes).map_err(disk)?;
    f.sync().map_err(disk)?;
    drop(f);
    vfs.rename(&tmp_path, &final_path).map_err(disk)?;
    vfs.sync_dir(dir).map_err(disk)?;
    Ok(())
}

/// Read + validate a checksummed file. `Ok(None)` when the file is missing.
pub fn read_validated(
    vfs: &dyn Vfs,
    dir: &str,
    name: &str,
    magic: &[u8; 8],
) -> Result<Option<Vec<u8>>, StorageError> {
    let path = join(dir, name);
    match vfs.exists(&path) {
        Ok(false) => return Ok(None),
        Ok(true) => {}
        Err(e) => return Err(StorageError::Disk(e.to_string())),
    }
    let mut f = vfs.open(&path, false).map_err(disk)?;
    let len = f.len().map_err(disk)?;
    let mut buf = vec![0u8; len as usize];
    let n = f.read_at(0, &mut buf).map_err(disk)?;
    buf.truncate(n);
    let payload = decode_magic(magic, &buf)?;
    Ok(Some(payload.to_vec()))
}

/// Write the store meta file.
pub fn write_meta(vfs: &dyn Vfs, root: &str, meta: &StoreMeta) -> Result<(), StorageError> {
    let payload =
        rmp_serde::encode::to_vec_named(meta).map_err(|e| StorageError::Codec(e.to_string()))?;
    write_atomic(vfs, root, "sqrl.meta", META_MAGIC, &payload)
}

/// Read the store meta file, if present.
pub fn read_meta(vfs: &dyn Vfs, root: &str) -> Result<Option<StoreMeta>, StorageError> {
    match read_validated(vfs, root, "sqrl.meta", META_MAGIC)? {
        None => Ok(None),
        Some(payload) => rmp_serde::decode::from_slice(&payload)
            .map(Some)
            .map_err(|e| StorageError::Corrupt(format!("meta decode: {e}"))),
    }
}

/// Write a shard manifest.
pub fn write_manifest(vfs: &dyn Vfs, dir: &str, m: &Manifest) -> Result<(), StorageError> {
    let payload =
        rmp_serde::encode::to_vec_named(m).map_err(|e| StorageError::Codec(e.to_string()))?;
    write_atomic(vfs, dir, "MANIFEST", MANIFEST_MAGIC, &payload)
}

/// Read a shard manifest; `Ok(None)` when missing **or corrupt** (the caller
/// falls back to a directory scan — a corrupt manifest must degrade, not
/// fail recovery).
pub fn read_manifest(vfs: &dyn Vfs, dir: &str) -> Result<Option<Manifest>, StorageError> {
    match read_validated(vfs, dir, "MANIFEST", MANIFEST_MAGIC) {
        Ok(None) => Ok(None),
        Ok(Some(payload)) => match rmp_serde::decode::from_slice(&payload) {
            Ok(m) => Ok(Some(m)),
            Err(e) => {
                tracing::warn!(dir, error = %e, "corrupt manifest payload; falling back to directory scan");
                Ok(None)
            }
        },
        Err(StorageError::Corrupt(reason)) => {
            tracing::warn!(
                dir,
                reason,
                "corrupt manifest; falling back to directory scan"
            );
            Ok(None)
        }
        Err(other) => Err(other),
    }
}

pub(crate) fn join(dir: &str, name: &str) -> String {
    if dir.is_empty() {
        name.to_string()
    } else {
        format!("{dir}/{name}")
    }
}

fn disk(e: sqrl_core::vfs::VfsError) -> StorageError {
    match e {
        sqrl_core::vfs::VfsError::DiskFull(p) => StorageError::DiskFull(p),
        other => StorageError::Disk(other.to_string()),
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use sqrl_sim::SimDisk;

    #[test]
    fn meta_round_trip() {
        let disk = SimDisk::new(1);
        let meta = StoreMeta {
            format_version: 1,
            num_shards: 4,
        };
        write_meta(&disk, "", &meta).unwrap();
        assert_eq!(read_meta(&disk, "").unwrap(), Some(meta));
    }

    #[test]
    fn manifest_round_trip_and_corruption_degrades() {
        let disk = SimDisk::new(2);
        let m = Manifest {
            segments: vec![1, 2, 5],
            next_segment_seq: 6,
        };
        write_manifest(&disk, "shard-0", &m).unwrap();
        assert_eq!(read_manifest(&disk, "shard-0").unwrap(), Some(m.clone()));
        // Corrupt one byte: read degrades to None (dir-scan fallback), not Err.
        disk.corrupt("shard-0/MANIFEST", 20, 0x55).unwrap();
        assert_eq!(read_manifest(&disk, "shard-0").unwrap(), None);
    }

    #[test]
    fn atomic_rewrite_survives_crash_with_old_or_new() {
        for seed in 0..30 {
            let disk = SimDisk::new(seed);
            let m1 = Manifest {
                segments: vec![1],
                next_segment_seq: 2,
            };
            write_manifest(&disk, "s", &m1).unwrap();
            let m2 = Manifest {
                segments: vec![1, 2],
                next_segment_seq: 3,
            };
            // Crash at a random point during the second rewrite.
            disk.crash_after_ops(1 + seed % 6);
            let _ = write_manifest(&disk, "s", &m2);
            disk.recover();
            let read = read_manifest(&disk, "s").unwrap();
            assert!(
                read == Some(m1.clone()) || read == Some(m2.clone()),
                "seed {seed}: manifest must be old or new, got {read:?}"
            );
        }
    }

    #[test]
    fn missing_files_read_as_none() {
        let disk = SimDisk::new(3);
        assert_eq!(read_meta(&disk, "").unwrap(), None);
        assert_eq!(read_manifest(&disk, "nope").unwrap(), None);
    }
}
