//! Engine configuration.

use crate::codec::DEFAULT_MAX_PAYLOAD;
use crate::retry::RetryPolicy;
use core::time::Duration;
use serde::{Deserialize, Serialize};

/// When appended records are fsynced (ADR 0003).
#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
pub enum FsyncPolicy {
    /// fsync on every commit batch. Safest; slowest.
    Strict,
    /// Group commit (default): fsync when `max_batch` records are pending or
    /// `max_delay` has elapsed since the oldest unsynced record, whichever
    /// comes first.
    Group {
        /// Maximum time a record waits for its durability barrier.
        max_delay: Duration,
        /// Maximum records per fsync batch.
        max_batch: usize,
    },
    /// Periodic fsync only. **Records acknowledged between intervals are
    /// lost on power failure** (up to `interval` worth); workflow-internal
    /// consistency is still preserved (prefix durability). Use only when
    /// that loss is acceptable.
    Relaxed {
        /// fsync interval.
        interval: Duration,
    },
}

impl FsyncPolicy {
    /// The default group-commit policy: 2 ms / 256 records.
    pub fn default_group() -> Self {
        FsyncPolicy::Group {
            max_delay: Duration::from_millis(2),
            max_batch: 256,
        }
    }
}

impl Default for FsyncPolicy {
    fn default() -> Self {
        FsyncPolicy::default_group()
    }
}

/// Per-step options for `ctx.step_with`.
#[derive(Debug, Clone, PartialEq, Default, Serialize, Deserialize)]
pub struct StepOptions {
    /// Override the engine's default retry policy for this step.
    pub retry: Option<RetryPolicy>,
    /// Force `FsyncPolicy::Strict` semantics for this step's records: the
    /// workflow does not proceed past the step until its `StepCompleted` /
    /// `StepFailed` record is durable. Use for durability-critical effects
    /// (e.g. a payment capture).
    pub fsync_strict: bool,
}

impl StepOptions {
    /// Options with a specific retry policy.
    pub fn with_retry(retry: RetryPolicy) -> Self {
        StepOptions {
            retry: Some(retry),
            fsync_strict: false,
        }
    }

    /// Options that force strict fsync for this step.
    pub fn strict_fsync() -> Self {
        StepOptions {
            retry: None,
            fsync_strict: true,
        }
    }
}

/// Engine-wide configuration.
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct EngineConfig {
    /// Fsync policy (see [`FsyncPolicy`]).
    pub fsync: FsyncPolicy,
    /// Default retry policy for steps.
    pub retry: RetryPolicy,
    /// Journal records per workflow between automatic snapshots.
    pub snapshot_every: u64,
    /// Maximum serialized payload size (inputs, outputs, step results,
    /// signals).
    pub max_payload: usize,
    /// Maximum live (non-terminal, in-memory) workflows per shard before
    /// `start` is rejected with backpressure.
    pub max_active_per_shard: usize,
    /// Passivate a workflow after this much logical idle time (evict its
    /// in-memory state; it is replayed on demand). `None` disables
    /// passivation.
    pub passivate_after: Option<Duration>,
    /// Base seed for engine entropy. Fixed by the simulator; randomized by
    /// the real builder.
    pub seed: u64,
}

impl Default for EngineConfig {
    fn default() -> Self {
        EngineConfig {
            fsync: FsyncPolicy::default(),
            retry: RetryPolicy::default(),
            snapshot_every: 1_000,
            max_payload: DEFAULT_MAX_PAYLOAD,
            max_active_per_shard: 100_000,
            passivate_after: Some(Duration::from_secs(300)),
            seed: 0,
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn defaults_match_spec() {
        let c = EngineConfig::default();
        assert_eq!(c.snapshot_every, 1_000);
        assert_eq!(c.max_payload, 1024 * 1024);
        assert_eq!(
            c.fsync,
            FsyncPolicy::Group {
                max_delay: Duration::from_millis(2),
                max_batch: 256
            }
        );
    }
}
