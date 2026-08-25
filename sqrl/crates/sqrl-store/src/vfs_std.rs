//! `StdVfs`: the real-filesystem implementation of [`Vfs`], rooted at a
//! directory. Paths handed to the VFS are relative, `/`-separated, and are
//! resolved strictly inside the root.

use sqrl_core::vfs::{Vfs, VfsError, VfsFile};
use sqrl_core::StorageError;
use std::fs;
use std::io::{Read, Seek, SeekFrom, Write};
use std::path::{Component, Path, PathBuf};

/// Real-filesystem VFS rooted at a directory (created if missing).
pub struct StdVfs {
    root: PathBuf,
}

impl StdVfs {
    /// Create a VFS rooted at `root`.
    pub fn new(root: impl Into<PathBuf>) -> Result<Self, StorageError> {
        let root = root.into();
        fs::create_dir_all(&root).map_err(|e| StorageError::Disk(e.to_string()))?;
        Ok(StdVfs { root })
    }

    fn resolve(&self, path: &str) -> Result<PathBuf, VfsError> {
        let rel = Path::new(path);
        for comp in rel.components() {
            match comp {
                Component::Normal(_) | Component::CurDir => {}
                _ => {
                    return Err(VfsError::io(
                        path,
                        "absolute or parent-relative paths are not allowed",
                    ))
                }
            }
        }
        Ok(self.root.join(rel))
    }
}

fn map_io(path: &str, e: std::io::Error) -> VfsError {
    match e.kind() {
        std::io::ErrorKind::NotFound => VfsError::NotFound(path.to_string()),
        std::io::ErrorKind::StorageFull | std::io::ErrorKind::QuotaExceeded => {
            VfsError::DiskFull(path.to_string())
        }
        _ => VfsError::io(path, e),
    }
}

impl Vfs for StdVfs {
    fn open(&self, path: &str, create: bool) -> Result<Box<dyn VfsFile>, VfsError> {
        let full = self.resolve(path)?;
        if let Some(parent) = full.parent() {
            fs::create_dir_all(parent).map_err(|e| map_io(path, e))?;
        }
        let file = fs::OpenOptions::new()
            .read(true)
            .write(true)
            .create(create)
            .open(&full)
            .map_err(|e| map_io(path, e))?;
        Ok(Box::new(StdFile {
            file,
            path: path.to_string(),
        }))
    }

    fn exists(&self, path: &str) -> Result<bool, VfsError> {
        Ok(self.resolve(path)?.exists())
    }

    fn delete(&self, path: &str) -> Result<(), VfsError> {
        let full = self.resolve(path)?;
        fs::remove_file(full).map_err(|e| map_io(path, e))
    }

    fn rename(&self, from: &str, to: &str) -> Result<(), VfsError> {
        let f = self.resolve(from)?;
        let t = self.resolve(to)?;
        fs::rename(f, t).map_err(|e| map_io(from, e))
    }

    fn list(&self, dir: &str) -> Result<Vec<String>, VfsError> {
        let full = self.resolve(dir)?;
        let rd = match fs::read_dir(full) {
            Ok(rd) => rd,
            Err(e) if e.kind() == std::io::ErrorKind::NotFound => return Ok(Vec::new()),
            Err(e) => return Err(map_io(dir, e)),
        };
        let mut out = Vec::new();
        for entry in rd {
            let entry = entry.map_err(|e| map_io(dir, e))?;
            if entry.file_type().map_err(|e| map_io(dir, e))?.is_file() {
                out.push(entry.file_name().to_string_lossy().into_owned());
            }
        }
        out.sort();
        Ok(out)
    }

    fn create_dir_all(&self, dir: &str) -> Result<(), VfsError> {
        let full = self.resolve(dir)?;
        fs::create_dir_all(full).map_err(|e| map_io(dir, e))
    }

    fn sync_dir(&self, dir: &str) -> Result<(), VfsError> {
        let full = self.resolve(dir)?;
        // Directory fsync: required for rename/create/delete durability on
        // Linux. On platforms where opening a directory for sync is not
        // supported this becomes a no-op with a warning.
        match fs::File::open(&full) {
            Ok(d) => d.sync_all().map_err(|e| map_io(dir, e)),
            Err(e) => {
                tracing::warn!(dir, error = %e, "directory fsync unavailable");
                Ok(())
            }
        }
    }
}

struct StdFile {
    file: fs::File,
    path: String,
}

impl VfsFile for StdFile {
    fn read_at(&mut self, offset: u64, buf: &mut [u8]) -> Result<usize, VfsError> {
        self.file
            .seek(SeekFrom::Start(offset))
            .map_err(|e| map_io(&self.path, e))?;
        let mut read = 0usize;
        while read < buf.len() {
            match self.file.read(&mut buf[read..]) {
                Ok(0) => break,
                Ok(n) => read += n,
                Err(e) if e.kind() == std::io::ErrorKind::Interrupted => continue,
                Err(e) => return Err(map_io(&self.path, e)),
            }
        }
        Ok(read)
    }

    fn write_at(&mut self, offset: u64, data: &[u8]) -> Result<(), VfsError> {
        self.file
            .seek(SeekFrom::Start(offset))
            .map_err(|e| map_io(&self.path, e))?;
        self.file.write_all(data).map_err(|e| map_io(&self.path, e))
    }

    fn len(&mut self) -> Result<u64, VfsError> {
        Ok(self
            .file
            .metadata()
            .map_err(|e| map_io(&self.path, e))?
            .len())
    }

    fn truncate(&mut self, len: u64) -> Result<(), VfsError> {
        self.file.set_len(len).map_err(|e| map_io(&self.path, e))
    }

    fn sync(&mut self) -> Result<(), VfsError> {
        self.file.sync_all().map_err(|e| map_io(&self.path, e))
    }
}
