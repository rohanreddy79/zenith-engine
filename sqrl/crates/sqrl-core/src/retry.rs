//! Step retry policy: exponential backoff with deterministic jitter.

use crate::inject::nth_draw;
use crate::time::duration_to_millis_ceil;
use core::time::Duration;
use serde::{Deserialize, Serialize};

/// Retry policy for steps.
///
/// Backoff for attempt `n` (1-based) is
/// `min(initial * multiplier^(n-1), max_delay)` plus jitter in
/// `[0, jitter_fraction * delay]`. Jitter is drawn deterministically from the
/// workflow's journaled seed (keyed by step seq and attempt) so that a replay
/// computes the identical schedule.
///
/// ```
/// use sqrl_core::RetryPolicy;
/// use core::time::Duration;
/// let p = RetryPolicy::default();
/// assert_eq!(p.max_attempts, 3);
/// let d1 = p.delay_for(1, 42, 0);
/// let d2 = p.delay_for(1, 42, 0);
/// assert_eq!(d1, d2); // deterministic
/// assert!(d1 >= Duration::from_millis(100));
/// ```
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct RetryPolicy {
    /// Maximum attempts (including the first). `1` disables retries.
    pub max_attempts: u32,
    /// Delay before the second attempt.
    pub initial_delay: Duration,
    /// Backoff multiplier.
    pub multiplier: f64,
    /// Upper bound on the computed delay (pre-jitter).
    pub max_delay: Duration,
    /// Fraction of the delay added as jitter, in `[0, 1]`.
    pub jitter_fraction: f64,
}

impl Default for RetryPolicy {
    fn default() -> Self {
        RetryPolicy {
            max_attempts: 3,
            initial_delay: Duration::from_millis(100),
            multiplier: 2.0,
            max_delay: Duration::from_secs(60),
            jitter_fraction: 0.2,
        }
    }
}

impl RetryPolicy {
    /// A policy that never retries.
    pub fn no_retries() -> Self {
        RetryPolicy {
            max_attempts: 1,
            ..RetryPolicy::default()
        }
    }

    /// Whether another attempt is allowed after `failed_attempts` failures.
    pub fn allows_retry(&self, failed_attempts: u32) -> bool {
        failed_attempts < self.max_attempts
    }

    /// Deterministic delay before the retry that follows failed attempt
    /// number `attempt` (1-based). `seed` is the workflow's journaled seed;
    /// `step_seq` keys the jitter stream per step.
    pub fn delay_for(&self, attempt: u32, seed: u64, step_seq: u64) -> Duration {
        let base_ms = duration_to_millis_ceil(self.initial_delay) as f64;
        let exp = self.multiplier.powi(attempt.saturating_sub(1) as i32);
        let capped = (base_ms * exp).min(duration_to_millis_ceil(self.max_delay) as f64);
        // Deterministic jitter: n-th draw of a stream keyed by (seed, step, attempt).
        let stream = seed ^ step_seq.rotate_left(17);
        let draw = nth_draw(stream, u64::from(attempt));
        let unit = (draw >> 11) as f64 / (1u64 << 53) as f64; // [0,1)
        let jitter = capped * self.jitter_fraction.clamp(0.0, 1.0) * unit;
        Duration::from_millis((capped + jitter) as u64)
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn backoff_grows_and_caps() {
        let p = RetryPolicy {
            max_attempts: 10,
            initial_delay: Duration::from_millis(100),
            multiplier: 2.0,
            max_delay: Duration::from_millis(500),
            jitter_fraction: 0.0,
        };
        assert_eq!(p.delay_for(1, 0, 0), Duration::from_millis(100));
        assert_eq!(p.delay_for(2, 0, 0), Duration::from_millis(200));
        assert_eq!(p.delay_for(3, 0, 0), Duration::from_millis(400));
        assert_eq!(p.delay_for(4, 0, 0), Duration::from_millis(500)); // capped
    }

    #[test]
    fn jitter_is_deterministic_and_bounded() {
        let p = RetryPolicy::default();
        for attempt in 1..5 {
            let a = p.delay_for(attempt, 7, 3);
            let b = p.delay_for(attempt, 7, 3);
            assert_eq!(a, b);
            let nojit = RetryPolicy {
                jitter_fraction: 0.0,
                ..p.clone()
            }
            .delay_for(attempt, 7, 3);
            assert!(a >= nojit);
            assert!(a.as_millis() as f64 <= nojit.as_millis() as f64 * 1.2 + 1.0);
        }
    }

    #[test]
    fn retries_exhaust() {
        let p = RetryPolicy::default(); // max 3
        assert!(p.allows_retry(1));
        assert!(p.allows_retry(2));
        assert!(!p.allows_retry(3));
        assert!(!RetryPolicy::no_retries().allows_retry(1));
    }
}
