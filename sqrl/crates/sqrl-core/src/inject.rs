//! Injected entropy and time sources.
//!
//! The engine never reads the wall clock or OS entropy directly. Both are
//! injected behind these traits; the simulator provides seeded/virtual
//! implementations, the real scheduler provides wall-clock/OS ones.

use crate::time::LogicalTime;

/// Source of logical "now". Implementations must be monotonic non-decreasing.
pub trait Clock: Send + Sync {
    /// The current logical time.
    fn now(&self) -> LogicalTime;
}

/// Source of engine-level entropy (workflow seeds). Deterministic under
/// simulation; OS-derived under the real scheduler. Workflow-visible
/// randomness (`ctx.random()`) is *not* drawn from here at runtime — it is
/// derived from the journaled per-workflow seed so that replay is stable.
pub trait Entropy: Send + Sync {
    /// Next 64 random bits.
    fn next_u64(&self) -> u64;
}

/// A splittable, seeded PRNG (SplitMix64). Deterministic, portable, and
/// cheap; used for workflow seeds under simulation, for `ctx.random()`
/// streams, and for retry jitter.
///
/// Not cryptographically secure — documented as such; use a step to obtain
/// secure random material from the OS if needed.
///
/// ```
/// use sqrl_core::DeterministicRng;
/// let a = DeterministicRng::new(42);
/// let b = DeterministicRng::new(42);
/// assert_eq!(a.next_u64(), b.next_u64());
/// ```
#[derive(Debug)]
pub struct DeterministicRng {
    state: core::sync::atomic::AtomicU64,
}

impl DeterministicRng {
    /// Create a new RNG from a seed.
    pub fn new(seed: u64) -> Self {
        DeterministicRng {
            state: core::sync::atomic::AtomicU64::new(seed),
        }
    }

    /// Draw the next 64 random bits.
    pub fn next_u64(&self) -> u64 {
        use core::sync::atomic::Ordering;
        // SplitMix64: state advances by the golden-ratio increment; output is
        // a finalized mix of the new state.
        let s = self
            .state
            .fetch_add(0x9E37_79B9_7F4A_7C15, Ordering::Relaxed)
            .wrapping_add(0x9E37_79B9_7F4A_7C15);
        splitmix64_mix(s)
    }

    /// Draw a value in `[0, bound)`. `bound` must be nonzero.
    pub fn next_below(&self, bound: u64) -> u64 {
        debug_assert!(bound > 0);
        // Multiply-shift bounded sampling (Lemire); slight modulo bias is
        // irrelevant for scheduling/jitter purposes.
        ((u128::from(self.next_u64()) * u128::from(bound)) >> 64) as u64
    }
}

impl Entropy for DeterministicRng {
    fn next_u64(&self) -> u64 {
        DeterministicRng::next_u64(self)
    }
}

/// The SplitMix64 output mix. Exposed so `ctx.random()` can derive the n-th
/// draw of a workflow's stream without storing mutable state (counter-based:
/// `mix(seed + n * GOLDEN)`).
pub fn splitmix64_mix(mut z: u64) -> u64 {
    z = (z ^ (z >> 30)).wrapping_mul(0xBF58_476D_1CE4_E5B9);
    z = (z ^ (z >> 27)).wrapping_mul(0x94D0_49BB_1331_11EB);
    z ^ (z >> 31)
}

/// The SplitMix64 state increment (golden ratio).
pub const SPLITMIX64_GOLDEN: u64 = 0x9E37_79B9_7F4A_7C15;

/// The n-th draw of the deterministic stream identified by `seed`.
pub fn nth_draw(seed: u64, n: u64) -> u64 {
    splitmix64_mix(seed.wrapping_add(SPLITMIX64_GOLDEN.wrapping_mul(n.wrapping_add(1))))
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn deterministic_and_seed_sensitive() {
        let a: Vec<u64> = (0..8)
            .map(|_| DeterministicRng::new(7).next_u64())
            .collect();
        // A fresh RNG restarted from the same seed replays the stream.
        let r = DeterministicRng::new(7);
        let b: Vec<u64> = (0..8).map(|_| r.next_u64()).collect();
        assert_ne!(a[0], b[1]);
        let r2 = DeterministicRng::new(7);
        let c: Vec<u64> = (0..8).map(|_| r2.next_u64()).collect();
        assert_eq!(b, c);
        let r3 = DeterministicRng::new(8);
        assert_ne!(b[0], r3.next_u64());
    }

    #[test]
    fn nth_draw_matches_sequential_stream() {
        let r = DeterministicRng::new(99);
        let seq: Vec<u64> = (0..5).map(|_| r.next_u64()).collect();
        let counter: Vec<u64> = (0..5).map(|n| nth_draw(99, n)).collect();
        assert_eq!(seq, counter);
    }

    #[test]
    fn next_below_in_range() {
        let r = DeterministicRng::new(1);
        for _ in 0..1000 {
            assert!(r.next_below(10) < 10);
        }
    }
}
