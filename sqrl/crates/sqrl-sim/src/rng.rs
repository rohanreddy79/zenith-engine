//! Seeded RNG for the simulation.

use sqrl_core::{stable_hash_more, DeterministicRng};

/// The simulation's seeded RNG. A thin wrapper over
/// [`sqrl_core::DeterministicRng`] that supports labeled forking so
/// independent components (scheduler choices, disk faults, workload
/// generation) consume independent streams — adding a draw in one component
/// does not perturb the others.
#[derive(Debug)]
pub struct SimRng {
    seed: u64,
    inner: DeterministicRng,
}

impl SimRng {
    /// Create from a seed.
    pub fn new(seed: u64) -> Self {
        SimRng {
            seed,
            inner: DeterministicRng::new(seed),
        }
    }

    /// The seed this RNG was created with.
    pub fn seed(&self) -> u64 {
        self.seed
    }

    /// Next 64 random bits.
    pub fn next_u64(&self) -> u64 {
        self.inner.next_u64()
    }

    /// Uniform draw in `[0, bound)`; `bound > 0`.
    pub fn next_below(&self, bound: u64) -> u64 {
        self.inner.next_below(bound)
    }

    /// `true` with probability `p` (clamped to `[0,1]`).
    pub fn chance(&self, p: f64) -> bool {
        let p = p.clamp(0.0, 1.0);
        ((self.next_u64() >> 11) as f64 / (1u64 << 53) as f64) < p
    }

    /// Fork an independent stream identified by `label`. Deterministic:
    /// same parent seed + same label ⇒ same child stream.
    pub fn fork(&self, label: &str) -> SimRng {
        SimRng::new(stable_hash_more(
            self.seed ^ 0x5eed_f0f0_1234_abcd,
            label.as_bytes(),
        ))
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn forks_are_deterministic_and_independent() {
        let a = SimRng::new(1);
        let b = SimRng::new(1);
        assert_eq!(a.fork("disk").next_u64(), b.fork("disk").next_u64());
        assert_ne!(a.fork("disk").next_u64(), b.fork("sched").next_u64());
        // consuming the parent does not shift the forks
        let _ = a.next_u64();
        assert_eq!(a.fork("disk").next_u64(), b.fork("disk").next_u64());
    }

    #[test]
    fn chance_extremes() {
        let r = SimRng::new(9);
        assert!(!r.chance(0.0));
        assert!(r.chance(1.0));
    }
}
