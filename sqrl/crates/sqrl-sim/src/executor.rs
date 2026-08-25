//! The deterministic, seeded, single-threaded, virtual-time executor.
//!
//! Tasks are polled one at a time. When several tasks are ready, the next one
//! is chosen by the seeded RNG — so one seed explores one interleaving,
//! different seeds explore different interleavings, and the same seed always
//! replays the same schedule. When no task is ready, virtual time jumps to
//! the earliest armed timer. There are no threads and no wall clock.

use crate::clock::SimClock;
use crate::rng::SimRng;
use sqrl_core::LogicalTime;
use std::collections::{BTreeMap, BTreeSet};
use std::future::Future;
use std::pin::Pin;
use std::sync::{Arc, Mutex};
use std::task::{Context, Poll, Waker};
use std::time::Duration;

type BoxFut = Pin<Box<dyn Future<Output = ()> + Send + 'static>>;

/// Identifier of a spawned task.
pub type TaskId = u64;

/// One entry of the execution trace: `(virtual time ms, task id)` for each
/// poll. Byte-identical traces across runs are the determinism criterion.
pub type TraceEntry = (u64, TaskId);

#[derive(Default)]
struct WakeQueue {
    woken: Mutex<Vec<TaskId>>,
}

struct SimWaker {
    id: TaskId,
    queue: Arc<WakeQueue>,
}

impl std::task::Wake for SimWaker {
    fn wake(self: Arc<Self>) {
        self.queue
            .woken
            .lock()
            .expect("sim waker lock poisoned")
            .push(self.id);
    }
}

struct Inner {
    tasks: BTreeMap<TaskId, Option<BoxFut>>, // None while being polled
    ready: BTreeSet<TaskId>,
    timers: BTreeMap<(u64, u64), Waker>, // (fire_at_ms, timer_id) -> waker
    next_task: TaskId,
    next_timer: u64,
    trace: Vec<TraceEntry>,
    polls: u64,
}

/// The deterministic executor. Cheap to clone (shared handle).
#[derive(Clone)]
pub struct SimExecutor {
    clock: SimClock,
    rng: Arc<SimRng>,
    queue: Arc<WakeQueue>,
    inner: Arc<Mutex<Inner>>,
}

impl SimExecutor {
    /// Create an executor with its own clock, seeded from `seed`.
    pub fn new(seed: u64) -> Self {
        SimExecutor::with_clock(seed, SimClock::default())
    }

    /// Create an executor sharing an existing clock.
    pub fn with_clock(seed: u64, clock: SimClock) -> Self {
        SimExecutor {
            clock,
            rng: Arc::new(SimRng::new(seed).fork("sim-executor")),
            queue: Arc::new(WakeQueue::default()),
            inner: Arc::new(Mutex::new(Inner {
                tasks: BTreeMap::new(),
                ready: BTreeSet::new(),
                timers: BTreeMap::new(),
                next_task: 0,
                next_timer: 0,
                trace: Vec::new(),
                polls: 0,
            })),
        }
    }

    /// The executor's clock.
    pub fn clock(&self) -> SimClock {
        self.clock.clone()
    }

    /// Current virtual time.
    pub fn now(&self) -> LogicalTime {
        use sqrl_core::Clock;
        self.clock.now()
    }

    /// Spawn a task; it becomes ready immediately.
    pub fn spawn(&self, fut: impl Future<Output = ()> + Send + 'static) -> TaskId {
        let mut inner = self.lock();
        let id = inner.next_task;
        inner.next_task += 1;
        inner.tasks.insert(id, Some(Box::pin(fut)));
        inner.ready.insert(id);
        id
    }

    /// A future that completes when virtual time reaches `now + d`.
    pub fn sleep(&self, d: Duration) -> SimSleep {
        self.sleep_until(self.now() + d)
    }

    /// A future that completes when virtual time reaches `at`.
    pub fn sleep_until(&self, at: LogicalTime) -> SimSleep {
        SimSleep {
            exec: self.clone(),
            at,
            timer: None,
        }
    }

    /// Poll tasks (and advance virtual time over timers) until no task is
    /// ready and no timer is armed. Returns the number of polls performed.
    pub fn run_until_idle(&self) -> u64 {
        let start_polls = self.lock().polls;
        loop {
            if !self.step() {
                break;
            }
        }
        self.lock().polls - start_polls
    }

    /// Perform one scheduling step: poll one ready task, or advance time to
    /// the next timer. Returns false when fully idle.
    pub fn step(&self) -> bool {
        self.step_bounded(None)
    }

    /// Like [`SimExecutor::step`], but never advances virtual time beyond
    /// `limit`: if the only remaining work is timers past the limit, returns
    /// false without advancing.
    pub fn step_bounded(&self, limit: Option<LogicalTime>) -> bool {
        // Phase 1: pick work while holding the lock.
        let (id, mut fut) = {
            let mut inner = self.lock();
            self.drain_wakes(&mut inner);
            if inner.ready.is_empty() {
                // Advance virtual time to the earliest timer, fire everything
                // due at that instant.
                let Some((&(fire_at, _), _)) = inner.timers.iter().next() else {
                    return false;
                };
                if let Some(limit) = limit {
                    if fire_at > limit.as_millis() {
                        return false;
                    }
                }
                self.clock.advance_to(LogicalTime::from_millis(fire_at));
                let now = fire_at;
                let due: Vec<(u64, u64)> = inner
                    .timers
                    .range(..=(now, u64::MAX))
                    .map(|(k, _)| *k)
                    .collect();
                for key in due {
                    if let Some(w) = inner.timers.remove(&key) {
                        w.wake();
                    }
                }
                self.drain_wakes(&mut inner);
                if inner.ready.is_empty() {
                    // Timers may have woken already-completed tasks; nothing
                    // runnable, but maybe more timers remain.
                    return !inner.timers.is_empty() || {
                        self.drain_wakes(&mut inner);
                        !inner.ready.is_empty()
                    };
                }
            }
            // Seeded choice among ready tasks.
            let idx = self.rng.next_below(inner.ready.len() as u64) as usize;
            let id = *inner
                .ready
                .iter()
                .nth(idx)
                .expect("ready set indexed in range");
            inner.ready.remove(&id);
            let Some(slot) = inner.tasks.get_mut(&id) else {
                return true; // task already finished; treat as progress
            };
            let Some(fut) = slot.take() else {
                return true;
            };
            let t = {
                use sqrl_core::Clock;
                self.clock.now().as_millis()
            };
            inner.trace.push((t, id));
            inner.polls += 1;
            (id, fut)
        };

        // Phase 2: poll without holding the lock (the task may re-enter the
        // executor: spawn, sleep, wake).
        let waker = Waker::from(Arc::new(SimWaker {
            id,
            queue: Arc::clone(&self.queue),
        }));
        let mut cx = Context::from_waker(&waker);
        let poll = fut.as_mut().poll(&mut cx);

        // Phase 3: put the task back or drop it.
        let mut inner = self.lock();
        match poll {
            Poll::Ready(()) => {
                inner.tasks.remove(&id);
            }
            Poll::Pending => {
                if let Some(slot) = inner.tasks.get_mut(&id) {
                    *slot = Some(fut);
                }
            }
        }
        true
    }

    /// The execution trace so far: `(virtual time, task id)` per poll.
    pub fn trace(&self) -> Vec<TraceEntry> {
        self.lock().trace.clone()
    }

    /// Number of live (not yet completed) tasks.
    pub fn live_tasks(&self) -> usize {
        self.lock().tasks.len()
    }

    fn drain_wakes(&self, inner: &mut Inner) {
        let woken: Vec<TaskId> = self
            .queue
            .woken
            .lock()
            .expect("sim waker lock poisoned")
            .drain(..)
            .collect();
        for id in woken {
            if inner.tasks.contains_key(&id) {
                inner.ready.insert(id);
            }
        }
    }

    fn lock(&self) -> std::sync::MutexGuard<'_, Inner> {
        self.inner.lock().expect("sim executor lock poisoned")
    }

    fn register_timer(&self, at: LogicalTime, waker: Waker) -> u64 {
        let mut inner = self.lock();
        let id = inner.next_timer;
        inner.next_timer += 1;
        inner.timers.insert((at.as_millis(), id), waker);
        id
    }

    fn refresh_timer_waker(&self, at: LogicalTime, timer_id: u64, waker: &Waker) {
        let mut inner = self.lock();
        if let Some(w) = inner.timers.get_mut(&(at.as_millis(), timer_id)) {
            w.clone_from(waker);
        }
    }
}

/// Future returned by [`SimExecutor::sleep`] / [`SimExecutor::sleep_until`].
pub struct SimSleep {
    exec: SimExecutor,
    at: LogicalTime,
    timer: Option<u64>,
}

impl Future for SimSleep {
    type Output = ();

    fn poll(self: Pin<&mut Self>, cx: &mut Context<'_>) -> Poll<()> {
        let this = self.get_mut();
        if this.exec.now() >= this.at {
            return Poll::Ready(());
        }
        match this.timer {
            None => {
                this.timer = Some(this.exec.register_timer(this.at, cx.waker().clone()));
            }
            Some(id) => {
                this.exec.refresh_timer_waker(this.at, id, cx.waker());
            }
        }
        Poll::Pending
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::sync::atomic::{AtomicU64, Ordering};

    fn workload(exec: &SimExecutor, log: Arc<Mutex<Vec<String>>>) {
        for i in 0..5u64 {
            let e = exec.clone();
            let log = Arc::clone(&log);
            exec.spawn(async move {
                for j in 0..3u64 {
                    e.sleep(Duration::from_millis(10 * (i % 3) + 1)).await;
                    log.lock().unwrap().push(format!("task{i}.{j}"));
                }
            });
        }
    }

    fn run_and_trace(seed: u64) -> (Vec<TraceEntry>, Vec<String>) {
        let exec = SimExecutor::new(seed);
        let log = Arc::new(Mutex::new(Vec::new()));
        workload(&exec, Arc::clone(&log));
        exec.run_until_idle();
        assert_eq!(exec.live_tasks(), 0);
        let log = Arc::try_unwrap(log).unwrap().into_inner().unwrap();
        (exec.trace(), log)
    }

    #[test]
    fn same_seed_identical_trace() {
        let (t1, l1) = run_and_trace(42);
        let (t2, l2) = run_and_trace(42);
        assert_eq!(t1, t2);
        assert_eq!(l1, l2);
        assert!(!t1.is_empty());
    }

    #[test]
    fn different_seed_different_schedule() {
        let (_, l1) = run_and_trace(1);
        let mut any_diff = false;
        for seed in 2..12 {
            let (_, l) = run_and_trace(seed);
            if l != l1 {
                any_diff = true;
                break;
            }
        }
        assert!(
            any_diff,
            "10 different seeds all produced the same schedule"
        );
    }

    #[test]
    fn virtual_time_advances_to_timers() {
        let exec = SimExecutor::new(7);
        let hits = Arc::new(AtomicU64::new(0));
        let h = Arc::clone(&hits);
        let e = exec.clone();
        exec.spawn(async move {
            e.sleep(Duration::from_secs(3600)).await; // one virtual hour
            h.store(e.now().as_millis(), Ordering::SeqCst);
        });
        exec.run_until_idle();
        assert_eq!(hits.load(Ordering::SeqCst), 3_600_000);
    }

    #[test]
    fn sleep_zero_completes() {
        let exec = SimExecutor::new(7);
        let done = Arc::new(AtomicU64::new(0));
        let d = Arc::clone(&done);
        let e = exec.clone();
        exec.spawn(async move {
            e.sleep(Duration::ZERO).await;
            d.store(1, Ordering::SeqCst);
        });
        exec.run_until_idle();
        assert_eq!(done.load(Ordering::SeqCst), 1);
    }

    #[test]
    fn tasks_interleave_rather_than_run_to_completion() {
        // With several ready tasks the seeded scheduler interleaves them:
        // across a few seeds we must observe at least one interleaved order.
        let mut interleaved = false;
        for seed in 0..10 {
            let exec = SimExecutor::new(seed);
            let log = Arc::new(Mutex::new(Vec::new()));
            for i in 0..3u64 {
                let e = exec.clone();
                let log = Arc::clone(&log);
                exec.spawn(async move {
                    log.lock().unwrap().push((i, 0));
                    e.sleep(Duration::from_millis(1)).await;
                    log.lock().unwrap().push((i, 1));
                });
            }
            exec.run_until_idle();
            let log = log.lock().unwrap();
            let first_seconds = log.iter().position(|&(_, p)| p == 1).unwrap();
            if first_seconds < 2 {
                continue; // a task finished before all firsts ran — fine
            }
            interleaved = true;
        }
        assert!(interleaved);
    }
}
