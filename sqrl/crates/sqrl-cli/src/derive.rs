//! Structural state derivation: what state a workflow is in, computed from
//! its journal alone (no workflow code is run).

use sqrl_core::snapshot::TerminalStatus;
use sqrl_core::storage::JournalReadout;
use sqrl_core::{JournalEvent, LogicalTime};
use std::collections::BTreeSet;

/// Workflow state derived structurally from the journal.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum DerivedState {
    /// Terminal: completed.
    Completed,
    /// Terminal: failed (resumable with `sqrl resume`).
    Failed,
    /// Terminal: cancelled.
    Cancelled,
    /// A step was scheduled but never resolved; the engine re-dispatches it
    /// on next start.
    InFlight,
    /// A durable timer is armed and unfired.
    Sleeping,
    /// Nothing pending in the journal: blocked on a signal or idle.
    Idle,
}

impl DerivedState {
    /// Human-facing label for `status`.
    pub fn human(self) -> &'static str {
        match self {
            DerivedState::Completed => "completed",
            DerivedState::Failed => "failed",
            DerivedState::Cancelled => "cancelled",
            DerivedState::InFlight => "in-flight (recovering on next start)",
            DerivedState::Sleeping => "sleeping",
            DerivedState::Idle => "blocked/idle",
        }
    }

    /// Stable machine-facing label for `--json`.
    pub fn machine(self) -> &'static str {
        match self {
            DerivedState::Completed => "completed",
            DerivedState::Failed => "failed",
            DerivedState::Cancelled => "cancelled",
            DerivedState::InFlight => "in-flight",
            DerivedState::Sleeping => "sleeping",
            DerivedState::Idle => "idle",
        }
    }

    /// Whether this is a terminal state.
    pub fn is_terminal(self) -> bool {
        matches!(
            self,
            DerivedState::Completed | DerivedState::Failed | DerivedState::Cancelled
        )
    }
}

/// Everything `status` and the surgery commands need to know about a journal.
pub struct Derived {
    /// Derived state (see [`DerivedState`]).
    pub state: DerivedState,
    /// Number of journal-tail records (excludes snapshot-covered history).
    pub record_count: usize,
    /// Whether a snapshot is present.
    pub has_snapshot: bool,
    /// Kind of the last record, if the tail is non-empty.
    pub last_event_kind: Option<&'static str>,
    /// Logical time of the last record (or the snapshot's `wf_time`).
    pub last_at: LogicalTime,
    /// Index for the next appended record (last index + 1, or `upto`).
    pub next_index: u64,
    /// Logical time to stamp on appended surgery records. The offline tool
    /// must not read the wall clock, so it reuses the last logical time.
    pub append_at: LogicalTime,
}

/// Derive a workflow's state from its journal readout.
pub fn derive(readout: &JournalReadout) -> Derived {
    let mut terminal: Option<DerivedState> = None;
    let mut pending_steps: BTreeSet<u64> = BTreeSet::new();
    let mut final_failed_steps: BTreeSet<u64> = BTreeSet::new();
    let mut pending_timers: BTreeSet<u64> = BTreeSet::new();

    if let Some(snap) = &readout.snapshot {
        pending_steps = snap.meta.inflight_steps.keys().copied().collect();
        pending_timers = snap.meta.pending_timers.keys().copied().collect();
        terminal = snap.meta.terminal.as_ref().map(|t| match t {
            TerminalStatus::Completed { .. } => DerivedState::Completed,
            TerminalStatus::Failed { .. } => DerivedState::Failed,
            TerminalStatus::Cancelled => DerivedState::Cancelled,
        });
    }

    for rec in &readout.records {
        match &rec.event {
            JournalEvent::StepScheduled { seq, .. } => {
                pending_steps.insert(*seq);
            }
            JournalEvent::StepCompleted { seq, .. } => {
                pending_steps.remove(seq);
            }
            JournalEvent::StepFailed { seq, retry_at, .. } => {
                // A retryable failure keeps the step in flight; a final one
                // resolves it (the failure surfaces to orchestration code).
                if retry_at.is_none() {
                    pending_steps.remove(seq);
                    final_failed_steps.insert(*seq);
                }
            }
            JournalEvent::TimerScheduled { seq, .. } => {
                pending_timers.insert(*seq);
            }
            JournalEvent::TimerFired { seq } => {
                pending_timers.remove(seq);
            }
            JournalEvent::WorkflowCompleted { .. } => terminal = Some(DerivedState::Completed),
            JournalEvent::WorkflowFailed { .. } => terminal = Some(DerivedState::Failed),
            JournalEvent::WorkflowCancelled => terminal = Some(DerivedState::Cancelled),
            JournalEvent::WorkflowResumed => {
                // Resume voids the terminal failure and resets the failed
                // step's attempt counter: that step is in flight again.
                terminal = None;
                pending_steps.append(&mut final_failed_steps);
            }
            JournalEvent::WorkflowStarted { .. }
            | JournalEvent::SignalAwaited { .. }
            | JournalEvent::SignalReceived { .. }
            | JournalEvent::PatchRecorded { .. } => {}
        }
    }

    let state = terminal.unwrap_or({
        if !pending_steps.is_empty() {
            DerivedState::InFlight
        } else if !pending_timers.is_empty() {
            DerivedState::Sleeping
        } else {
            DerivedState::Idle
        }
    });

    let (next_index, last_at, last_event_kind) = match readout.records.last() {
        Some(rec) => (rec.index + 1, rec.at, Some(rec.event.kind())),
        None => match &readout.snapshot {
            Some(snap) => (snap.upto, snap.meta.wf_time, None),
            None => (0, LogicalTime::ZERO, None),
        },
    };

    Derived {
        state,
        record_count: readout.records.len(),
        has_snapshot: readout.snapshot.is_some(),
        last_event_kind,
        last_at,
        next_index,
        append_at: last_at,
    }
}
