//! `sqrl` — offline inspector/surgeon for a sqrl WAL data directory.
//!
//! This binary opens the store *directly* (no engine): it must only be run
//! while no engine process has the data directory open, because opening a
//! shard performs recovery-repair (torn tails are truncated). Mutating
//! commands print a one-line warning to stderr as a reminder.
#![forbid(unsafe_code)]

mod commands;
mod derive;
mod render;
mod store;

use clap::{Parser, Subcommand};
use std::path::PathBuf;
use std::process::ExitCode;

/// One-line reminder printed (to stderr) by every mutating command.
pub const OFFLINE_WARNING: &str = "warning: sqrl is an offline tool — make sure NO engine process \
has this data directory open (opening a shard performs recovery-repair)";

/// The CLI's error type: a plain message printed to stderr by `main`.
#[derive(Debug)]
pub struct CliError(pub String);

impl std::fmt::Display for CliError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.write_str(&self.0)
    }
}

impl From<sqrl_core::StorageError> for CliError {
    fn from(e: sqrl_core::StorageError) -> Self {
        CliError(e.to_string())
    }
}

impl From<sqrl_core::Error> for CliError {
    fn from(e: sqrl_core::Error) -> Self {
        CliError(e.to_string())
    }
}

/// Result alias used by all command functions.
pub type CliResult<T> = Result<T, CliError>;

/// Offline inspector/surgeon for a sqrl WAL data directory.
#[derive(Parser)]
#[command(
    name = "sqrl",
    version,
    about = "Offline inspector/surgeon for a sqrl WAL data directory",
    long_about = "Offline inspector/surgeon for a sqrl WAL data directory.\n\n\
IMPORTANT: run this only while no engine process has the store open. Opening \
a shard performs recovery-repair (torn WAL tails are truncated), and \
concurrent access from two processes corrupts the store."
)]
struct Cli {
    /// Path to the sqrl data directory (required).
    #[arg(long, global = true, value_name = "DIR")]
    data: Option<PathBuf>,

    #[command(subcommand)]
    command: Cmd,
}

#[derive(Subcommand)]
enum Cmd {
    /// Show every workflow in the store with its derived state.
    ///
    /// State is derived structurally from the journal (no workflow code is
    /// run): terminal events / snapshot terminal status win (a later
    /// WorkflowResumed voids them); otherwise an unresolved StepScheduled
    /// means "in-flight", a pending timer means "sleeping", else
    /// "blocked/idle".
    Status {
        /// Emit machine-readable JSON instead of a table.
        #[arg(long)]
        json: bool,
    },
    /// Pretty-print one workflow's snapshot summary and journal records.
    Inspect {
        /// Workflow id.
        id: String,
        /// Emit machine-readable JSON instead of the human listing.
        #[arg(long)]
        json: bool,
        /// Show only the last N records.
        #[arg(long, value_name = "N")]
        limit: Option<usize>,
        /// Also decode the snapshot body and report cmd/outcome counts.
        #[arg(long)]
        body: bool,
    },
    /// Append a SignalReceived record to a workflow's journal.
    ///
    /// The JSON argument is parsed and re-encoded as self-describing
    /// MessagePack (the engine's payload codec). The new record's logical
    /// time reuses the last record's `at`: this offline tool never reads the
    /// wall clock, so the workflow's logical timeline stays consistent.
    /// Refused if the workflow is terminal.
    Signal {
        /// Workflow id.
        id: String,
        /// Signal name.
        name: String,
        /// Signal payload as a JSON document (e.g. '{"approved":true}').
        json: String,
    },
    /// Append a WorkflowCancelled record. Refused if already terminal.
    Cancel {
        /// Workflow id.
        id: String,
    },
    /// Append a WorkflowResumed record to a *Failed* workflow.
    ///
    /// Only allowed when the derived state is Failed (from a WorkflowFailed
    /// event or a snapshot terminal Failed status, not voided by a later
    /// resume). The engine picks the workflow back up on next start with the
    /// failed step's attempt counter reset.
    Resume {
        /// Workflow id.
        id: String,
    },
    /// Copy a journal prefix into a brand-new workflow id.
    ///
    /// Copies records with index < N (never the snapshot — only a full,
    /// uncompacted prefix can be forked; refused when history before a
    /// snapshot is gone). Record indexes and logical times are kept as-is;
    /// the copy is appended to the shard the new id hashes to.
    Fork {
        /// Source workflow id.
        id: String,
        /// Copy records with index strictly below this (must be >= 1).
        #[arg(long, value_name = "N")]
        from_index: u64,
        /// Id for the forked workflow (must not exist yet).
        #[arg(long, value_name = "NEWID")]
        new_id: String,
    },
    /// Run storage maintenance (segment roll + GC) on every shard.
    Compact,
    /// Structural replay validation of journal integrity.
    ///
    /// Checks, per workflow: record indexes are dense and ascending from the
    /// snapshot's `upto` (or 0); every StepCompleted/StepFailed/TimerFired
    /// has a preceding matching Scheduled with the same seq (or the seq is
    /// covered by the snapshot); logical time never goes backwards. This is
    /// journal *integrity* only — full non-determinism validation against the
    /// actual workflow code runs in-process during engine replay, not here.
    Replay {
        /// Validate only this workflow id (default: all workflows).
        #[arg(long)]
        id: Option<String>,
    },
    /// Storage-level smoke benchmark (APPENDS synthetic records).
    ///
    /// Appends N workflows x (WorkflowStarted + M StepScheduled/StepCompleted
    /// pairs) across all shards with periodic sync, then reads them back.
    /// This measures WAL append+fsync and read throughput only — no engine,
    /// no workflow code (the CLI has no engine dependency). It writes
    /// synthetic records into the store: point --data at a scratch directory.
    Bench {
        /// Number of synthetic workflows to append.
        #[arg(long, default_value_t = 100, value_name = "N")]
        workflows: usize,
        /// Number of step (Scheduled+Completed) pairs per workflow.
        #[arg(long, default_value_t = 10, value_name = "M")]
        steps: usize,
    },
}

// Top-level entry point: per workspace standards this is the only place
// where errors may terminate the process; command functions return Result.
fn main() -> ExitCode {
    // `sqrl status | head` closes stdout early, which makes `println!`
    // panic with a backtrace. Turn that broken-pipe print failure into the
    // conventional quiet SIGPIPE exit (128 + 13) instead.
    let default_hook = std::panic::take_hook();
    std::panic::set_hook(Box::new(move |info| {
        let msg = info
            .payload()
            .downcast_ref::<String>()
            .map(String::as_str)
            .or_else(|| info.payload().downcast_ref::<&str>().copied())
            .unwrap_or("");
        if msg.contains("Broken pipe") {
            std::process::exit(141);
        }
        default_hook(info);
    }));
    let cli = Cli::parse();
    match run(cli) {
        Ok(code) => code,
        Err(e) => {
            eprintln!("error: {e}");
            ExitCode::FAILURE
        }
    }
}

fn run(cli: Cli) -> CliResult<ExitCode> {
    let data = cli
        .data
        .ok_or_else(|| CliError("--data <DIR> is required".into()))?;
    match cli.command {
        Cmd::Status { json } => commands::status(&data, json)?,
        Cmd::Inspect {
            id,
            json,
            limit,
            body,
        } => commands::inspect(&data, &id, json, limit, body)?,
        Cmd::Signal { id, name, json } => commands::signal(&data, &id, &name, &json)?,
        Cmd::Cancel { id } => commands::cancel(&data, &id)?,
        Cmd::Resume { id } => commands::resume(&data, &id)?,
        Cmd::Fork {
            id,
            from_index,
            new_id,
        } => commands::fork(&data, &id, from_index, &new_id)?,
        Cmd::Compact => commands::compact(&data)?,
        Cmd::Replay { id } => {
            let all_ok = commands::replay(&data, id.as_deref())?;
            if !all_ok {
                return Ok(ExitCode::FAILURE);
            }
        }
        Cmd::Bench { workflows, steps } => commands::bench(&data, workflows, steps)?,
    }
    Ok(ExitCode::SUCCESS)
}
