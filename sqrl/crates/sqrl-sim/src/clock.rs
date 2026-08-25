//! Virtual clock.

use sqrl_core::{Clock, LogicalTime};
use std::sync::atomic::{AtomicU64, Ordering};
use std::sync::Arc;

/// A shared virtual clock. Time only moves when something advances it: the
/// [`crate::SimExecutor`] jumping to the next timer, or the
/// [`crate::SimDisk`] charging I/O latency.
///
/// ```
/// use sqrl_sim::SimClock;
/// use sqrl_core::{Clock, LogicalTime};
/// use core::time::Duration;
/// let c = SimClock::new(LogicalTime::from_millis(100));
/// c.advance(Duration::from_secs(1));
/// assert_eq!(c.now(), LogicalTime::from_millis(1_100));
/// ```
#[derive(Debug, Clone)]
pub struct SimClock {
    millis: Arc<AtomicU64>,
}

impl SimClock {
    /// Create a clock starting at `start`.
    pub fn new(start: LogicalTime) -> Self {
        SimClock {
            millis: Arc::new(AtomicU64::new(start.as_millis())),
        }
    }

    /// Advance by a duration (millisecond resolution, rounding up).
    pub fn advance(&self, d: core::time::Duration) {
        self.millis.fetch_add(
            sqrl_core::time::duration_to_millis_ceil(d),
            Ordering::SeqCst,
        );
    }

    /// Move the clock forward to `to`. Ignored if `to` is in the past
    /// (virtual time never goes backwards).
    pub fn advance_to(&self, to: LogicalTime) {
        self.millis.fetch_max(to.as_millis(), Ordering::SeqCst);
    }
}

impl Default for SimClock {
    fn default() -> Self {
        SimClock::new(LogicalTime::ZERO)
    }
}

impl Clock for SimClock {
    fn now(&self) -> LogicalTime {
        LogicalTime::from_millis(self.millis.load(Ordering::SeqCst))
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use core::time::Duration;

    #[test]
    fn never_goes_backwards() {
        let c = SimClock::default();
        c.advance_to(LogicalTime::from_millis(50));
        c.advance_to(LogicalTime::from_millis(10));
        assert_eq!(c.now(), LogicalTime::from_millis(50));
        c.advance(Duration::from_millis(5));
        assert_eq!(c.now(), LogicalTime::from_millis(55));
    }
}
