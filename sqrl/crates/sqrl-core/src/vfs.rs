//! Virtual filesystem abstraction.
//!
//! `sqrl-store`'s WAL runs against this trait rather than `std::fs` directly,
//! so the exact same storage code runs on real disks (`sqrl-store::StdVfs`)
//! and on the simulated, fault-injecting disk (`sqrl-sim::SimDisk`). This is
//! the moral equivalent of SQLite's VFS layer.
//!
//! Paths are relative, `/`-separated, and interpreted within a root chosen by
//! the VFS implementation.

use core::fmt;
use thiserror::Error;

/// Errors surfaced by VFS operations.
#[derive(Debug, Clone, PartialEq, Eq, Error)]
pub enum VfsError {
    /// The file or directory does not exist.
    #[error("not found: {0}")]
    NotFound(String),
    /// The device is out of space.
    #[error("disk full while writing {0}")]
    DiskFull(String),
    /// An injected or real I/O failure.
    #[error("i/o error on {path}: {message}")]
    Io {
        /// Path the operation targeted.
        path: String,
        /// Description of the failure.
        message: String,
    },
}

impl VfsError {
    /// Helper to build an [`VfsError::Io`].
    pub fn io(path: impl Into<String>, message: impl fmt::Display) -> Self {
        VfsError::Io {
            path: path.into(),
            message: message.to_string(),
        }
    }
}

/// A virtual filesystem: the only way storage code touches disk.
pub trait Vfs: Send + Sync + 'static {
    /// Open a file, creating it if `create` is true. Opening a missing file
    /// with `create == false` is [`VfsError::NotFound`].
    fn open(&self, path: &str, create: bool) -> Result<Box<dyn VfsFile>, VfsError>;
    /// True if the file exists.
    fn exists(&self, path: &str) -> Result<bool, VfsError>;
    /// Delete a file. Deleting a missing file is [`VfsError::NotFound`].
    fn delete(&self, path: &str) -> Result<(), VfsError>;
    /// Atomically rename `from` to `to`, replacing `to` if it exists. Used
    /// for the manifest's atomic-rewrite protocol.
    fn rename(&self, from: &str, to: &str) -> Result<(), VfsError>;
    /// List file names (not full paths) directly under `dir`. Returns an
    /// empty list for a missing directory. Order is unspecified; callers
    /// must sort.
    fn list(&self, dir: &str) -> Result<Vec<String>, VfsError>;
    /// Create a directory (and parents). Idempotent.
    fn create_dir_all(&self, dir: &str) -> Result<(), VfsError>;
    /// Durably persist directory metadata (entries created by
    /// rename/create/delete). On real disks this is `fsync` of the directory
    /// fd; on the sim disk it commits pending namespace operations.
    fn sync_dir(&self, dir: &str) -> Result<(), VfsError>;
}

/// An open file handle.
pub trait VfsFile: Send {
    /// Read up to `buf.len()` bytes at `offset`; returns bytes read (short
    /// reads only at end of file).
    fn read_at(&mut self, offset: u64, buf: &mut [u8]) -> Result<usize, VfsError>;
    /// Write all of `data` at `offset`, extending the file if needed.
    /// Not durable until [`VfsFile::sync`] returns.
    fn write_at(&mut self, offset: u64, data: &[u8]) -> Result<(), VfsError>;
    /// Current length in bytes.
    fn len(&mut self) -> Result<u64, VfsError>;
    /// True if the file is empty.
    fn is_empty(&mut self) -> Result<bool, VfsError> {
        Ok(self.len()? == 0)
    }
    /// Truncate the file to `len` bytes.
    fn truncate(&mut self, len: u64) -> Result<(), VfsError>;
    /// Durably persist all previous writes (fsync). After `sync` returns Ok,
    /// the data must survive a crash / power loss.
    fn sync(&mut self) -> Result<(), VfsError>;
}
