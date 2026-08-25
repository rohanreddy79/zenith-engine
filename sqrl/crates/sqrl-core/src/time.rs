//! Logical time.
//!
//! Everything in the orchestration path is stamped with [`LogicalTime`]: a
//! millisecond-resolution timestamp produced by the injected clock
//! (`crate::inject::Clock`). Under the real scheduler this tracks the wall clock; under
//! simulation it is virtual. Workflow code must never read the wall clock
//! directly — see `docs/determinism-guide.md`.

use core::fmt;
use core::ops::{Add, Sub};
use core::time::Duration;
use serde::{Deserialize, Serialize};

/// A logical timestamp: milliseconds since the Unix epoch on the injected
/// clock's timeline.
///
/// ```
/// use sqrl_core::LogicalTime;
/// use core::time::Duration;
/// let t = LogicalTime::from_millis(1_000);
/// assert_eq!(t + Duration::from_secs(2), LogicalTime::from_millis(3_000));
/// ```
#[derive(
    Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Hash, Default, Serialize, Deserialize,
)]
#[serde(transparent)]
pub struct LogicalTime(u64);

impl LogicalTime {
    /// The zero timestamp.
    pub const ZERO: LogicalTime = LogicalTime(0);
    /// The maximum representable timestamp.
    pub const MAX: LogicalTime = LogicalTime(u64::MAX);

    /// Build from milliseconds since the epoch.
    pub const fn from_millis(ms: u64) -> Self {
        LogicalTime(ms)
    }

    /// Milliseconds since the epoch.
    pub const fn as_millis(self) -> u64 {
        self.0
    }

    /// Saturating addition of a duration (millisecond resolution; sub-ms
    /// durations round up to 1ms so that a nonzero sleep never becomes a
    /// zero-length sleep).
    pub fn saturating_add(self, d: Duration) -> Self {
        LogicalTime(self.0.saturating_add(duration_to_millis_ceil(d)))
    }

    /// Saturating difference between two timestamps.
    pub fn saturating_since(self, earlier: LogicalTime) -> Duration {
        Duration::from_millis(self.0.saturating_sub(earlier.0))
    }
}

/// Convert a [`Duration`] to whole milliseconds, rounding up, saturating.
pub fn duration_to_millis_ceil(d: Duration) -> u64 {
    let ms = d.as_millis();
    let rounded = if d.subsec_nanos() % 1_000_000 != 0 {
        ms + 1
    } else {
        ms
    };
    u64::try_from(rounded).unwrap_or(u64::MAX)
}

impl Add<Duration> for LogicalTime {
    type Output = LogicalTime;
    fn add(self, rhs: Duration) -> LogicalTime {
        self.saturating_add(rhs)
    }
}

impl Sub<LogicalTime> for LogicalTime {
    type Output = Duration;
    fn sub(self, rhs: LogicalTime) -> Duration {
        self.saturating_since(rhs)
    }
}

impl fmt::Display for LogicalTime {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "t+{}ms", self.0)
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn add_and_sub() {
        let t = LogicalTime::from_millis(10);
        assert_eq!((t + Duration::from_millis(5)).as_millis(), 15);
        assert_eq!(LogicalTime::from_millis(15) - t, Duration::from_millis(5));
        // saturating, never panics
        assert_eq!(LogicalTime::ZERO - t, Duration::ZERO);
        assert_eq!(LogicalTime::MAX + Duration::from_secs(1), LogicalTime::MAX);
    }

    #[test]
    fn sub_millisecond_durations_round_up() {
        assert_eq!(duration_to_millis_ceil(Duration::from_nanos(1)), 1);
        assert_eq!(duration_to_millis_ceil(Duration::from_millis(2)), 2);
        assert_eq!(duration_to_millis_ceil(Duration::ZERO), 0);
    }
}
