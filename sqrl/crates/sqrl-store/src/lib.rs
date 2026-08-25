//! Storage backends for `sqrl`.
//!
//! * [`MemoryStorage`] — in-memory, for tests and examples.
//! * [`WalStorage`] — the default embedded backend: checksummed, segmented
//!   write-ahead log with manifest, snapshots, group commit, and
//!   truncate-on-corruption recovery. Runs on real disks ([`StdVfs`]) and on
//!   the fault-injecting simulator disk (`sqrl-sim::SimDisk`).
//!
//! On-disk format: `docs/on-disk-format.md`.
#![forbid(unsafe_code)]
#![deny(missing_docs)]

pub mod codec;
pub mod manifest;
mod mem;
mod vfs_std;
mod wal;

pub use mem::MemoryStorage;
pub use vfs_std::StdVfs;
pub use wal::{WalOptions, WalShard, WalStorage};
