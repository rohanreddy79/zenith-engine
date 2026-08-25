//! Deterministic simulation testing (DST) harness for `sqrl`.
//!
//! Provides the seeded substrate the whole engine runs on under test:
//!
//! * [`SimClock`] — virtual time,
//! * [`SimRng`] — seeded, forkable randomness,
//! * [`SimExecutor`] — single-threaded, seeded, virtual-time task executor,
//! * [`SimDisk`] — in-memory [`sqrl_core::vfs::Vfs`] with crash, torn-write,
//!   corruption, disk-full, and slow-I/O fault injection.
//!
//! Two runs with the same seed produce byte-identical traces and disk
//! images; that property is what the DST suite asserts across thousands of
//! seeds.
//!
//! Unlike the production crates, this crate may panic (`expect`) on internal
//! invariant violations: it is test infrastructure, and a loud failure *is*
//! the desired behavior under DST.
#![forbid(unsafe_code)]
#![deny(missing_docs)]

mod clock;
mod disk;
mod executor;
mod rng;

pub use clock::SimClock;
pub use disk::{DiskStats, FaultConfig, SimDisk, SimFile};
pub use executor::{SimExecutor, SimSleep, TaskId, TraceEntry};
pub use rng::SimRng;
