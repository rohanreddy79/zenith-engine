//! Workflow identity and stable hashing.

use core::fmt;
use serde::{Deserialize, Serialize};

/// Identifies one workflow execution. User-supplied, unique per data
/// directory.
///
/// ```
/// use sqrl_core::WorkflowId;
/// let id = WorkflowId::new("order-123");
/// assert_eq!(id.as_str(), "order-123");
/// ```
#[derive(Debug, Clone, PartialEq, Eq, PartialOrd, Ord, Hash, Serialize, Deserialize)]
#[serde(transparent)]
pub struct WorkflowId(String);

impl WorkflowId {
    /// Create a workflow id from a string.
    pub fn new(id: impl Into<String>) -> Self {
        WorkflowId(id.into())
    }

    /// The id as a string slice.
    pub fn as_str(&self) -> &str {
        &self.0
    }

    /// Stable shard assignment for this id.
    ///
    /// Uses [`stable_hash`], which is part of the on-disk contract: shard
    /// assignment must not change across sqrl versions, platforms, or process
    /// restarts (see `docs/on-disk-format.md`).
    pub fn shard(&self, num_shards: usize) -> usize {
        debug_assert!(num_shards > 0);
        (stable_hash(self.0.as_bytes()) % num_shards as u64) as usize
    }
}

impl fmt::Display for WorkflowId {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        f.write_str(&self.0)
    }
}

impl From<&str> for WorkflowId {
    fn from(s: &str) -> Self {
        WorkflowId::new(s)
    }
}

impl From<String> for WorkflowId {
    fn from(s: String) -> Self {
        WorkflowId(s)
    }
}

/// FNV-1a 64-bit hash. Deliberately *not* `std::hash` based: `HashMap`'s
/// hasher is unspecified and randomly keyed, while shard assignment and
/// deterministic seeds require a hash that is stable across processes,
/// platforms, and versions of this library.
pub fn stable_hash(bytes: &[u8]) -> u64 {
    const OFFSET: u64 = 0xcbf2_9ce4_8422_2325;
    const PRIME: u64 = 0x0000_0100_0000_01b3;
    let mut h = OFFSET;
    for &b in bytes {
        h ^= u64::from(b);
        h = h.wrapping_mul(PRIME);
    }
    h
}

/// Extend a stable hash with more bytes (for composite keys such as
/// `(workflow id, step seq, attempt)`).
pub fn stable_hash_more(seed: u64, bytes: &[u8]) -> u64 {
    const PRIME: u64 = 0x0000_0100_0000_01b3;
    let mut h = seed;
    for &b in bytes {
        h ^= u64::from(b);
        h = h.wrapping_mul(PRIME);
    }
    h
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn stable_hash_is_stable() {
        // Golden values: these must NEVER change (shard assignment is
        // persisted implicitly in the on-disk layout).
        assert_eq!(stable_hash(b""), 0xcbf2_9ce4_8422_2325);
        assert_eq!(stable_hash(b"a"), 0xaf63_dc4c_8601_ec8c);
        assert_eq!(stable_hash(b"order-123"), stable_hash(b"order-123"));
        assert_ne!(stable_hash(b"order-123"), stable_hash(b"order-124"));
    }

    #[test]
    fn shard_in_range() {
        for n in 1..8 {
            for i in 0..100 {
                let id = WorkflowId::new(format!("wf-{i}"));
                assert!(id.shard(n) < n);
            }
        }
    }
}
