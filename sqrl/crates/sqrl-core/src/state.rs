//! The workflow lifecycle state machine.
//!
//! States and legal transitions are exactly those of `docs/architecture.md`:
//!
//! ```text
//! Pending → Running → AwaitingStep → Running → …
//! Running → Sleeping → Running          (timer)
//! Running → Blocked  → Running          (signal)
//! any non-terminal → Recovering → Running   (restart)
//! terminals: Completed, Failed, Cancelled
//! ```
//!
//! The transition function is an exhaustive `match` with **no wildcard
//! arms**; an illegal transition is a typed [`IllegalTransition`] error,
//! never a panic.

use crate::error::{Error, IllegalTransition, NonDeterminismError};
use serde::{Deserialize, Serialize};

/// Why a workflow is in the `Failed` state.
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub enum FailureKind {
    /// A step exhausted retries, or orchestration code returned an error.
    Error(Error),
    /// Replay diverged from journaled history. Never retried automatically.
    NonDeterministic(NonDeterminismError),
    /// Orchestration code panicked.
    OrchestrationPanic(String),
}

impl FailureKind {
    /// The user-facing error for this failure.
    pub fn to_error(&self) -> Error {
        match self {
            FailureKind::Error(e) => e.clone(),
            FailureKind::NonDeterministic(e) => Error::NonDeterminism(e.clone()),
            FailureKind::OrchestrationPanic(msg) => Error::OrchestrationPanic(msg.clone()),
        }
    }
}

/// Lifecycle state of a workflow instance.
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub enum WorkflowState {
    /// Created; first activation has not run yet.
    Pending,
    /// Orchestration code is runnable or running.
    Running,
    /// Suspended awaiting a step result.
    AwaitingStep,
    /// Suspended on a durable timer.
    Sleeping,
    /// Suspended awaiting an external signal.
    Blocked,
    /// Being replayed after a restart or reactivation.
    Recovering,
    /// Terminal: completed successfully.
    Completed,
    /// Terminal: failed.
    Failed(FailureKind),
    /// Terminal: cancelled.
    Cancelled,
}

/// Data-free discriminant of [`WorkflowState`], used in errors and metrics.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, Serialize, Deserialize)]
#[allow(missing_docs)]
pub enum StateKind {
    Pending,
    Running,
    AwaitingStep,
    Sleeping,
    Blocked,
    Recovering,
    Completed,
    Failed,
    Cancelled,
}

impl WorkflowState {
    /// The discriminant of this state.
    pub fn kind(&self) -> StateKind {
        match self {
            WorkflowState::Pending => StateKind::Pending,
            WorkflowState::Running => StateKind::Running,
            WorkflowState::AwaitingStep => StateKind::AwaitingStep,
            WorkflowState::Sleeping => StateKind::Sleeping,
            WorkflowState::Blocked => StateKind::Blocked,
            WorkflowState::Recovering => StateKind::Recovering,
            WorkflowState::Completed => StateKind::Completed,
            WorkflowState::Failed(_) => StateKind::Failed,
            WorkflowState::Cancelled => StateKind::Cancelled,
        }
    }

    /// True for `Completed`, `Failed`, `Cancelled`.
    pub fn is_terminal(&self) -> bool {
        match self {
            WorkflowState::Completed | WorkflowState::Failed(_) | WorkflowState::Cancelled => true,
            WorkflowState::Pending
            | WorkflowState::Running
            | WorkflowState::AwaitingStep
            | WorkflowState::Sleeping
            | WorkflowState::Blocked
            | WorkflowState::Recovering => false,
        }
    }

    /// Validate and perform a transition, returning the new state or a typed
    /// error. Exhaustive over `(from, to)` with no wildcard arms.
    pub fn transition(&self, to: WorkflowState) -> Result<WorkflowState, IllegalTransition> {
        use StateKind as K;
        let from_kind = self.kind();
        let to_kind = to.kind();
        let legal = match (from_kind, to_kind) {
            // Pending: first activation starts running, may be recovered
            // (crash between creation and first activation), or cancelled.
            (K::Pending, K::Running) => true,
            (K::Pending, K::Recovering) => true,
            (K::Pending, K::Cancelled) => true,
            (K::Pending, K::Pending)
            | (K::Pending, K::AwaitingStep)
            | (K::Pending, K::Sleeping)
            | (K::Pending, K::Blocked)
            | (K::Pending, K::Completed)
            | (K::Pending, K::Failed) => false,

            // Running: may suspend, terminate, or be recovered.
            (K::Running, K::AwaitingStep) => true,
            (K::Running, K::Sleeping) => true,
            (K::Running, K::Blocked) => true,
            (K::Running, K::Completed) => true,
            (K::Running, K::Failed) => true,
            (K::Running, K::Cancelled) => true,
            (K::Running, K::Recovering) => true,
            (K::Running, K::Running) | (K::Running, K::Pending) => false,

            // Suspended states resume to Running, terminate, or recover.
            (K::AwaitingStep, K::Running) => true,
            (K::AwaitingStep, K::Recovering) => true,
            (K::AwaitingStep, K::Cancelled) => true,
            (K::AwaitingStep, K::Failed) => true, // storage failure while suspended
            (K::AwaitingStep, K::Pending)
            | (K::AwaitingStep, K::AwaitingStep)
            | (K::AwaitingStep, K::Sleeping)
            | (K::AwaitingStep, K::Blocked)
            | (K::AwaitingStep, K::Completed) => false,

            (K::Sleeping, K::Running) => true,
            (K::Sleeping, K::Recovering) => true,
            (K::Sleeping, K::Cancelled) => true,
            (K::Sleeping, K::Failed) => true,
            (K::Sleeping, K::Pending)
            | (K::Sleeping, K::AwaitingStep)
            | (K::Sleeping, K::Sleeping)
            | (K::Sleeping, K::Blocked)
            | (K::Sleeping, K::Completed) => false,

            (K::Blocked, K::Running) => true,
            (K::Blocked, K::Recovering) => true,
            (K::Blocked, K::Cancelled) => true,
            (K::Blocked, K::Failed) => true,
            (K::Blocked, K::Pending)
            | (K::Blocked, K::AwaitingStep)
            | (K::Blocked, K::Sleeping)
            | (K::Blocked, K::Blocked)
            | (K::Blocked, K::Completed) => false,

            // Recovering: replay finishes into Running (or straight into a
            // suspended state when history ends suspended), terminates if
            // history says so or replay itself fails.
            (K::Recovering, K::Running) => true,
            (K::Recovering, K::AwaitingStep) => true,
            (K::Recovering, K::Sleeping) => true,
            (K::Recovering, K::Blocked) => true,
            (K::Recovering, K::Completed) => true,
            (K::Recovering, K::Failed) => true,
            (K::Recovering, K::Cancelled) => true,
            (K::Recovering, K::Pending) | (K::Recovering, K::Recovering) => false,

            // Terminals: no way out — except Failed, which an explicit
            // `sqrl resume` moves back into Recovering.
            (K::Failed, K::Recovering) => true,
            (K::Failed, K::Pending)
            | (K::Failed, K::Running)
            | (K::Failed, K::AwaitingStep)
            | (K::Failed, K::Sleeping)
            | (K::Failed, K::Blocked)
            | (K::Failed, K::Completed)
            | (K::Failed, K::Failed)
            | (K::Failed, K::Cancelled) => false,

            (K::Completed, K::Pending)
            | (K::Completed, K::Running)
            | (K::Completed, K::AwaitingStep)
            | (K::Completed, K::Sleeping)
            | (K::Completed, K::Blocked)
            | (K::Completed, K::Recovering)
            | (K::Completed, K::Completed)
            | (K::Completed, K::Failed)
            | (K::Completed, K::Cancelled) => false,

            (K::Cancelled, K::Pending)
            | (K::Cancelled, K::Running)
            | (K::Cancelled, K::AwaitingStep)
            | (K::Cancelled, K::Sleeping)
            | (K::Cancelled, K::Blocked)
            | (K::Cancelled, K::Recovering)
            | (K::Cancelled, K::Completed)
            | (K::Cancelled, K::Failed)
            | (K::Cancelled, K::Cancelled) => false,
        };
        if legal {
            Ok(to)
        } else {
            Err(IllegalTransition {
                from: from_kind,
                to: to_kind,
            })
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    fn all_states() -> Vec<WorkflowState> {
        vec![
            WorkflowState::Pending,
            WorkflowState::Running,
            WorkflowState::AwaitingStep,
            WorkflowState::Sleeping,
            WorkflowState::Blocked,
            WorkflowState::Recovering,
            WorkflowState::Completed,
            WorkflowState::Failed(FailureKind::Error(Error::app("x"))),
            WorkflowState::Cancelled,
        ]
    }

    #[test]
    fn happy_path() {
        let s = WorkflowState::Pending;
        let s = s.transition(WorkflowState::Running).unwrap();
        let s = s.transition(WorkflowState::AwaitingStep).unwrap();
        let s = s.transition(WorkflowState::Running).unwrap();
        let s = s.transition(WorkflowState::Sleeping).unwrap();
        let s = s.transition(WorkflowState::Running).unwrap();
        let s = s.transition(WorkflowState::Completed).unwrap();
        assert!(s.is_terminal());
    }

    #[test]
    fn recovery_from_all_non_terminals() {
        for s in all_states() {
            let r = s.transition(WorkflowState::Recovering);
            // Every non-terminal state except Recovering itself is
            // recoverable; among terminals only Failed (explicit resume) is.
            let expect_ok = (!s.is_terminal() && s.kind() != StateKind::Recovering)
                || s.kind() == StateKind::Failed;
            assert_eq!(r.is_ok(), expect_ok, "{s:?} -> Recovering");
        }
    }

    #[test]
    fn terminals_are_sticky() {
        for from in [WorkflowState::Completed, WorkflowState::Cancelled] {
            for to in all_states() {
                assert!(
                    from.transition(to.clone()).is_err(),
                    "{from:?} -> {to:?} must be illegal"
                );
            }
        }
        // Failed is sticky except for explicit resume (-> Recovering).
        let failed = WorkflowState::Failed(FailureKind::OrchestrationPanic("p".into()));
        for to in all_states() {
            let ok = to.kind() == StateKind::Recovering;
            assert_eq!(
                failed.transition(to.clone()).is_ok(),
                ok,
                "Failed -> {to:?}"
            );
        }
    }

    #[test]
    fn illegal_transition_is_typed() {
        let err = WorkflowState::Completed
            .transition(WorkflowState::Running)
            .unwrap_err();
        assert_eq!(err.from, StateKind::Completed);
        assert_eq!(err.to, StateKind::Running);
    }
}
