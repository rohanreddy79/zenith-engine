//! `Ctx`: the workflow's only window onto the world.
//!
//! Orchestration code must obtain **everything** non-deterministic through
//! this type: step execution, time (`now`, `sleep`), randomness (`random`,
//! `uuid`), external input (`await_signal`), identity (`idempotency_key`),
//! and versioning gates (`patched`). Calling `SystemTime::now()`,
//! `rand::random()`, or performing I/O directly inside orchestration code is
//! a bug — see `docs/determinism-guide.md`.

use crate::codec;
use crate::config::StepOptions;
use crate::error::{Error, StepError};
use crate::event::{CmdDesc, JournalEvent};
use crate::id::{stable_hash_more, WorkflowId};
use crate::inject::nth_draw;
use crate::instance::{BoxStepFut, InstanceInner, Issue, Resolution, StepReg, Waiting};
use crate::time::LogicalTime;
use core::fmt::Display;
use core::future::Future;
use core::marker::PhantomData;
use core::pin::Pin;
use core::task::{Context as TaskContext, Poll};
use core::time::Duration;
use serde::{de::DeserializeOwned, Serialize};
use std::cell::RefCell;
use std::rc::Rc;

/// The workflow context. Cheap to clone; `!Send` by design — orchestration
/// code runs on exactly one logical thread of control.
#[derive(Clone)]
pub struct Ctx {
    pub(crate) cell: Rc<RefCell<InstanceInner>>,
}

impl Ctx {
    pub(crate) fn from_cell(cell: Rc<RefCell<InstanceInner>>) -> Self {
        Ctx { cell }
    }

    /// This workflow's id.
    pub fn id(&self) -> WorkflowId {
        self.cell.borrow().id.clone()
    }

    /// The workflow version journaled at start.
    pub fn version(&self) -> u32 {
        self.cell.borrow().version
    }

    /// Deterministic, replay-safe "now": the logical time of the last
    /// journal record this workflow processed. Constant within one
    /// activation; never reads the wall clock.
    pub fn now(&self) -> LogicalTime {
        self.cell.borrow().wf_time
    }

    /// Deterministic 64-bit random value, drawn from the workflow's
    /// journaled seed. The n-th call always returns the same value, live or
    /// replayed. **Not** cryptographically secure — obtain secure entropy
    /// inside a step if needed.
    pub fn random(&self) -> u64 {
        let mut inner = self.cell.borrow_mut();
        let n = inner.rng_counter;
        inner.rng_counter += 1;
        nth_draw(stable_hash_more(inner.seed, b"random"), n)
    }

    /// Deterministic random float in `[0, 1)`.
    pub fn random_f64(&self) -> f64 {
        (self.random() >> 11) as f64 / (1u64 << 53) as f64
    }

    /// Deterministic, replay-stable UUID (version-4 format).
    pub fn uuid(&self) -> String {
        let mut inner = self.cell.borrow_mut();
        let n = inner.uuid_counter;
        inner.uuid_counter += 1;
        let stream = stable_hash_more(inner.seed, b"uuid");
        let hi = nth_draw(stream, n * 2);
        let lo = nth_draw(stream, n * 2 + 1);
        let mut b = [0u8; 16];
        b[..8].copy_from_slice(&hi.to_be_bytes());
        b[8..].copy_from_slice(&lo.to_be_bytes());
        b[6] = (b[6] & 0x0f) | 0x40; // version 4
        b[8] = (b[8] & 0x3f) | 0x80; // RFC 4122 variant
        format!(
            "{:02x}{:02x}{:02x}{:02x}-{:02x}{:02x}-{:02x}{:02x}-{:02x}{:02x}-{:02x}{:02x}{:02x}{:02x}{:02x}{:02x}",
            b[0], b[1], b[2], b[3], b[4], b[5], b[6], b[7], b[8], b[9], b[10], b[11], b[12],
            b[13], b[14], b[15]
        )
    }

    /// A stable idempotency key: identical across replays and across step
    /// retries (the n-th call always yields the same key for this workflow).
    /// Pass it to external effects so an at-least-once re-execution
    /// deduplicates to effectively-once.
    pub fn idempotency_key(&self) -> String {
        let mut inner = self.cell.borrow_mut();
        let n = inner.idem_counter;
        inner.idem_counter += 1;
        let stream = stable_hash_more(inner.seed, b"idem");
        format!(
            "{:016x}{:016x}",
            nth_draw(stream, n * 2),
            nth_draw(stream, n * 2 + 1)
        )
    }

    /// Versioning gate for safe code changes (see
    /// `docs/versioning-and-patching.md`).
    ///
    /// Returns `true` when this execution may take the *new* code path:
    /// always for fresh executions, and on replay only if this patch was
    /// journaled when the history was written. Returns `false` while
    /// replaying history recorded by pre-patch code. The decision is sticky
    /// per id for the lifetime of the execution.
    pub fn patched(&self, id: &str) -> bool {
        let mut inner = self.cell.borrow_mut();
        if let Some(v) = inner.patches.get(id) {
            return *v;
        }
        if inner.nd_error.is_some() {
            return false;
        }
        let seq = inner.next_seq;
        let decision = match inner.cmds.get(&seq) {
            Some(CmdDesc::Patch { id: rid }) if rid == id => {
                inner.next_seq += 1;
                true
            }
            Some(_) => false, // history continues without this patch here
            None => {
                if inner.at_live_frontier(seq) {
                    inner.next_seq += 1;
                    inner.load_cmd(seq, CmdDesc::Patch { id: id.to_string() });
                    inner.new_events.push(JournalEvent::PatchRecorded {
                        seq,
                        id: id.to_string(),
                    });
                    true
                } else {
                    false
                }
            }
        };
        inner.patches.insert(id.to_string(), decision);
        decision
    }

    /// Execute a step: an arbitrary, possibly non-deterministic effect. The
    /// result is journaled; on replay the journaled result is returned
    /// without re-execution. Retried per the engine's default
    /// [`crate::RetryPolicy`].
    ///
    /// The closure must own its captures (`move` + clones): the returned
    /// future runs on the step pool and may be re-created for retries.
    pub fn step<T, E, Fut, F>(&self, name: &str, f: F) -> StepFuture<T>
    where
        T: Serialize + DeserializeOwned,
        E: Display,
        Fut: Future<Output = Result<T, E>> + Send + 'static,
        F: FnMut() -> Fut + Send + 'static,
    {
        self.step_with(name, StepOptions::default(), f)
    }

    /// [`Ctx::step`] with per-step options (retry policy, strict fsync).
    pub fn step_with<T, E, Fut, F>(&self, name: &str, opts: StepOptions, mut f: F) -> StepFuture<T>
    where
        T: Serialize + DeserializeOwned,
        E: Display,
        Fut: Future<Output = Result<T, E>> + Send + 'static,
        F: FnMut() -> Fut + Send + 'static,
    {
        let max_payload = self.cell.borrow().max_payload;
        let closure: Box<dyn FnMut() -> BoxStepFut + Send> = Box::new(move || {
            let fut = f();
            Box::pin(async move {
                match fut.await {
                    Ok(v) => codec::to_vec_limited(&v, max_payload, "step result")
                        .map_err(|e| StepError::ResultNotJournalable(e.to_string())),
                    Err(e) => Err(StepError::App(e.to_string())),
                }
            }) as BoxStepFut
        });
        StepFuture {
            ctx: self.clone(),
            name: name.to_string(),
            opts,
            closure: Some(closure),
            seq: None,
            _t: PhantomData,
        }
    }

    /// Durable sleep: journaled on logical time; survives restarts.
    pub fn sleep(&self, d: Duration) -> SleepFuture {
        SleepFuture {
            ctx: self.clone(),
            target: SleepTarget::Relative(d),
            seq: None,
        }
    }

    /// Durable sleep until an absolute logical time.
    pub fn sleep_until(&self, at: LogicalTime) -> SleepFuture {
        SleepFuture {
            ctx: self.clone(),
            target: SleepTarget::Absolute(at),
            seq: None,
        }
    }

    /// Durably await an external signal by name. Signals are buffered: one
    /// that arrived before the await completes immediately; consumption
    /// order per name is arrival order.
    pub fn await_signal<T: DeserializeOwned>(&self, name: &str) -> SignalFuture<T> {
        SignalFuture {
            ctx: self.clone(),
            name: name.to_string(),
            seq: None,
            _t: PhantomData,
        }
    }
}

/// Future returned by [`Ctx::step`] / [`Ctx::step_with`].
pub struct StepFuture<T> {
    ctx: Ctx,
    name: String,
    opts: StepOptions,
    closure: Option<BoxStepClosure>,
    seq: Option<u64>,
    _t: PhantomData<fn() -> T>,
}

type BoxStepClosure = Box<dyn FnMut() -> BoxStepFut + Send + 'static>;

impl<T: DeserializeOwned> Future for StepFuture<T> {
    type Output = Result<T, Error>;

    fn poll(self: Pin<&mut Self>, _cx: &mut TaskContext<'_>) -> Poll<Self::Output> {
        let this = self.get_mut();
        let mut inner = this.ctx.cell.borrow_mut();
        if inner.nd_error.is_some() {
            return Poll::Pending; // engine fails the workflow after this poll
        }
        if this.seq.is_none() {
            let seq = match inner.issue(CmdDesc::Step {
                name: this.name.clone(),
            }) {
                Issue::Replayed(seq) => seq,
                Issue::Live(seq) => {
                    inner.new_events.push(JournalEvent::StepScheduled {
                        seq,
                        name: this.name.clone(),
                    });
                    seq
                }
                Issue::Diverged => return Poll::Pending,
            };
            // Register the closure either way; the engine dispatches it
            // (live or in-flight after recovery) or discards it when the
            // outcome is already in still-unrevealed history.
            if let Some(closure) = this.closure.take() {
                inner.new_steps.push(StepReg {
                    seq,
                    name: this.name.clone(),
                    opts: this.opts.clone(),
                    closure,
                });
            }
            this.seq = Some(seq);
        }
        let seq = this.seq.expect("seq assigned on first poll");
        match inner.resolved.remove(&seq) {
            Some(Resolution::StepOk(bytes)) => {
                drop(inner);
                Poll::Ready(codec::from_slice(&bytes, "step result"))
            }
            Some(Resolution::StepErr { error, attempts }) => Poll::Ready(Err(Error::StepFailed {
                name: this.name.clone(),
                seq,
                attempts,
                error,
            })),
            Some(Resolution::Timer) => {
                // Engine invariant violation; surface as divergence rather
                // than panicking in production code.
                inner.nd_error = Some(crate::error::NonDeterminismError {
                    seq,
                    expected: None,
                    actual: Some(CmdDesc::Step {
                        name: this.name.clone(),
                    }),
                });
                Poll::Pending
            }
            None => {
                inner.waiting = Waiting::Step(seq);
                Poll::Pending
            }
        }
    }
}

enum SleepTarget {
    Relative(Duration),
    Absolute(LogicalTime),
}

/// Future returned by [`Ctx::sleep`] / [`Ctx::sleep_until`].
pub struct SleepFuture {
    ctx: Ctx,
    target: SleepTarget,
    seq: Option<u64>,
}

impl Future for SleepFuture {
    type Output = Result<(), Error>;

    fn poll(self: Pin<&mut Self>, _cx: &mut TaskContext<'_>) -> Poll<Self::Output> {
        let this = self.get_mut();
        let mut inner = this.ctx.cell.borrow_mut();
        if inner.nd_error.is_some() {
            return Poll::Pending;
        }
        if this.seq.is_none() {
            let computed_fire_at = match this.target {
                SleepTarget::Relative(d) => inner.wf_time + d,
                SleepTarget::Absolute(at) => at,
            };
            match inner.issue(CmdDesc::Timer) {
                Issue::Replayed(seq) => {
                    let recorded = inner.timer_targets.get(&seq).copied();
                    match recorded {
                        Some(at) if at == computed_fire_at => {
                            inner.new_timers.push((seq, at));
                            this.seq = Some(seq);
                        }
                        _ => {
                            inner.nd_error = Some(crate::error::NonDeterminismError {
                                seq,
                                expected: Some(CmdDesc::Timer),
                                actual: Some(CmdDesc::Timer),
                            });
                            return Poll::Pending;
                        }
                    }
                }
                Issue::Live(seq) => {
                    inner.timer_targets.insert(seq, computed_fire_at);
                    inner.new_events.push(JournalEvent::TimerScheduled {
                        seq,
                        fire_at: computed_fire_at,
                    });
                    inner.new_timers.push((seq, computed_fire_at));
                    this.seq = Some(seq);
                }
                Issue::Diverged => return Poll::Pending,
            }
        }
        let seq = this.seq.expect("seq assigned on first poll");
        match inner.resolved.remove(&seq) {
            Some(Resolution::Timer) => Poll::Ready(Ok(())),
            Some(other) => {
                inner.resolved.insert(seq, other);
                inner.waiting = Waiting::Timer(seq);
                Poll::Pending
            }
            None => {
                inner.waiting = Waiting::Timer(seq);
                Poll::Pending
            }
        }
    }
}

/// Future returned by [`Ctx::await_signal`].
pub struct SignalFuture<T> {
    ctx: Ctx,
    name: String,
    seq: Option<u64>,
    _t: PhantomData<fn() -> T>,
}

impl<T: DeserializeOwned> Future for SignalFuture<T> {
    type Output = Result<T, Error>;

    fn poll(self: Pin<&mut Self>, _cx: &mut TaskContext<'_>) -> Poll<Self::Output> {
        let this = self.get_mut();
        let mut inner = this.ctx.cell.borrow_mut();
        if inner.nd_error.is_some() {
            return Poll::Pending;
        }
        if this.seq.is_none() {
            match inner.issue(CmdDesc::AwaitSignal {
                name: this.name.clone(),
            }) {
                Issue::Replayed(seq) => this.seq = Some(seq),
                Issue::Live(seq) => {
                    inner.new_events.push(JournalEvent::SignalAwaited {
                        seq,
                        name: this.name.clone(),
                    });
                    this.seq = Some(seq);
                }
                Issue::Diverged => return Poll::Pending,
            }
        }
        let seq = this.seq.expect("seq assigned on first poll");
        let popped = inner
            .signal_buf
            .get_mut(&this.name)
            .and_then(|q| q.pop_front());
        match popped {
            Some(payload) => {
                drop(inner);
                Poll::Ready(codec::from_slice(&payload, "signal payload"))
            }
            None => {
                inner.waiting = Waiting::Signal(this.name.clone(), seq);
                Poll::Pending
            }
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::retry::RetryPolicy;

    fn ctx() -> Ctx {
        Ctx::from_cell(Rc::new(RefCell::new(InstanceInner::new(
            WorkflowId::new("wf-1"),
            "test".into(),
            1,
            1234,
            1024 * 1024,
            RetryPolicy::default(),
            LogicalTime::from_millis(500),
        ))))
    }

    #[test]
    fn deterministic_entropy_streams() {
        let a = ctx();
        let b = ctx();
        let ra: Vec<u64> = (0..4).map(|_| a.random()).collect();
        let rb: Vec<u64> = (0..4).map(|_| b.random()).collect();
        assert_eq!(ra, rb);
        assert_eq!(a.uuid(), b.uuid());
        assert_eq!(a.idempotency_key(), b.idempotency_key());
        // streams are independent: drawing random does not shift uuid
        let c = ctx();
        let d = ctx();
        let _ = c.random();
        assert_eq!(c.uuid(), d.uuid());
    }

    #[test]
    fn uuid_shape() {
        let u = ctx().uuid();
        assert_eq!(u.len(), 36);
        let parts: Vec<&str> = u.split('-').collect();
        assert_eq!(parts.len(), 5);
        assert!(parts[2].starts_with('4'), "version nibble: {u}");
    }

    #[test]
    fn now_is_wf_time() {
        let c = ctx();
        assert_eq!(c.now(), LogicalTime::from_millis(500));
    }

    #[test]
    fn patched_fresh_execution_is_true_and_journaled() {
        let c = ctx();
        assert!(c.patched("fix-1"));
        assert!(c.patched("fix-1"), "sticky");
        let inner = c.cell.borrow();
        assert_eq!(inner.next_seq, 1);
        assert!(matches!(
            inner.new_events.as_slice(),
            [JournalEvent::PatchRecorded { seq: 0, .. }]
        ));
    }

    #[test]
    fn patched_replaying_old_history_is_false() {
        let c = ctx();
        {
            let mut inner = c.cell.borrow_mut();
            inner.load_cmd(0, CmdDesc::Step { name: "a".into() });
            inner.unrevealed = 1;
        }
        assert!(!c.patched("fix-1"));
        assert!(!c.patched("fix-1"), "sticky");
        let inner = c.cell.borrow();
        assert_eq!(inner.next_seq, 0, "no seq consumed by inactive patch");
        assert!(inner.new_events.is_empty());
    }

    #[test]
    fn patched_replaying_patched_history_is_true() {
        let c = ctx();
        {
            let mut inner = c.cell.borrow_mut();
            inner.load_cmd(0, CmdDesc::Patch { id: "fix-1".into() });
        }
        assert!(c.patched("fix-1"));
        assert_eq!(c.cell.borrow().next_seq, 1);
    }
}
