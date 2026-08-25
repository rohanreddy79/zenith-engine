//! Implementations of the `sqrl` subcommands.

use crate::derive::{derive, DerivedState};
use crate::render::{
    event_fields_human, record_json, snapshot_summary_human, snapshot_summary_json,
};
use crate::store::Store;
use crate::{CliError, CliResult, OFFLINE_WARNING};
use serde_json::json;
use sqrl_core::storage::{AppendEntry, AppendPayload, JournalReadout};
use sqrl_core::{CmdDesc, JournalEvent, JournalRecord, LogicalTime, WorkflowId};
use std::collections::BTreeSet;
use std::path::Path;

// ---------------------------------------------------------------- status

/// `sqrl status`: one row per workflow across all shards.
pub fn status(data: &Path, json: bool) -> CliResult<()> {
    let mut store = Store::open_existing(data)?;
    let mut rows = Vec::new();
    for idx in 0..store.num_shards() {
        let shard = store.shard(idx)?;
        for id in shard.list()? {
            let readout = shard.read(&id)?;
            let d = derive(&readout);
            rows.push((id, idx, d));
        }
    }
    rows.sort_by(|a, b| a.0.cmp(&b.0));

    if json {
        let items: Vec<_> = rows
            .iter()
            .map(|(id, shard, d)| {
                json!({
                    "id": id.as_str(),
                    "shard": shard,
                    "state": d.state.machine(),
                    "records": d.record_count,
                    "snapshot": d.has_snapshot,
                    "last_event": d.last_event_kind,
                    "last_at_ms": d.last_at.as_millis(),
                })
            })
            .collect();
        println!(
            "{}",
            serde_json::to_string_pretty(&json!(items))
                .map_err(|e| CliError(format!("JSON encoding failed: {e}")))?
        );
        return Ok(());
    }

    if rows.is_empty() {
        println!("store has {} shard(s), no workflows", store.num_shards());
        return Ok(());
    }
    let id_w = rows
        .iter()
        .map(|(id, _, _)| id.as_str().chars().count())
        .max()
        .unwrap_or(8)
        .max("WORKFLOW".len());
    let state_w = rows
        .iter()
        .map(|(_, _, d)| d.state.human().len())
        .max()
        .unwrap_or(5)
        .max("STATE".len());
    println!(
        "{:<id_w$}  {:>5}  {:<state_w$}  {:>7}  {:<17}  LAST-AT",
        "WORKFLOW", "SHARD", "STATE", "RECORDS", "LAST-EVENT"
    );
    for (id, shard, d) in &rows {
        let records = if d.has_snapshot {
            format!("{}+s", d.record_count)
        } else {
            d.record_count.to_string()
        };
        println!(
            "{:<id_w$}  {:>5}  {:<state_w$}  {:>7}  {:<17}  t+{}ms",
            id.as_str(),
            shard,
            d.state.human(),
            records,
            d.last_event_kind.unwrap_or("-"),
            d.last_at.as_millis(),
        );
    }
    Ok(())
}

// ---------------------------------------------------------------- inspect

/// `sqrl inspect`: pretty-print one workflow's snapshot + journal.
pub fn inspect(
    data: &Path,
    id: &str,
    json: bool,
    limit: Option<usize>,
    body: bool,
) -> CliResult<()> {
    let mut store = Store::open_existing(data)?;
    let wf = WorkflowId::new(id);
    let shard_idx = store.shard_index_for(&wf);
    let readout = store.read(&wf)?;

    let skip = limit.map_or(0, |n| readout.records.len().saturating_sub(n));
    let shown = &readout.records[skip..];

    if json {
        let mut snap_json = readout.snapshot.as_ref().map(snapshot_summary_json);
        if body {
            if let (Some(snap), Some(serde_json::Value::Object(map))) =
                (&readout.snapshot, snap_json.as_mut())
            {
                let decoded = snap.decode_body()?;
                map.insert(
                    "body".into(),
                    json!({ "cmds": decoded.cmds.len(), "outcomes": decoded.outcomes.len() }),
                );
            }
        }
        let out = json!({
            "id": id,
            "shard": shard_idx,
            "snapshot": snap_json,
            "skipped_records": skip,
            "records": shown.iter().map(record_json).collect::<Vec<_>>(),
        });
        println!(
            "{}",
            serde_json::to_string_pretty(&out)
                .map_err(|e| CliError(format!("JSON encoding failed: {e}")))?
        );
        return Ok(());
    }

    println!("workflow `{id}` (shard {shard_idx})");
    if let Some(snap) = &readout.snapshot {
        println!("{}", snapshot_summary_human(snap));
        if body {
            let decoded = snap.decode_body()?;
            println!(
                "[snapshot body: {} cmd(s), {} outcome(s)]",
                decoded.cmds.len(),
                decoded.outcomes.len()
            );
        }
    }
    if skip > 0 {
        println!("  … {skip} earlier record(s) not shown (--limit)");
    }
    if shown.is_empty() {
        println!("  (no journal records after the snapshot)");
        return Ok(());
    }
    let idx_w = shown
        .iter()
        .map(|r| r.index.to_string().len())
        .max()
        .unwrap_or(1);
    let at_w = shown
        .iter()
        .map(|r| r.at.as_millis().to_string().len())
        .max()
        .unwrap_or(1);
    for rec in shown {
        let fields = event_fields_human(&rec.event);
        let sep = if fields.is_empty() { "" } else { " " };
        println!(
            "  #{:<idx_w$} t+{:>at_w$}ms {:<17}{sep}{fields}",
            rec.index,
            rec.at.as_millis(),
            rec.event.kind(),
        );
    }
    Ok(())
}

// ---------------------------------------------------------------- surgery

/// Read a workflow and refuse if it is terminal; returns what an appended
/// record should carry.
fn prepare_append(store: &mut Store, id: &str) -> CliResult<(WorkflowId, u64, LogicalTime)> {
    let wf = WorkflowId::new(id);
    let readout = store.read(&wf)?;
    let d = derive(&readout);
    if d.state.is_terminal() {
        return Err(CliError(format!(
            "workflow `{id}` is terminal ({}); refusing to modify it",
            d.state.machine()
        )));
    }
    Ok((wf, d.next_index, d.append_at))
}

fn append_one(store: &mut Store, wf: &WorkflowId, rec: JournalRecord) -> CliResult<()> {
    let idx = store.shard_index_for(wf);
    let shard = store.shard(idx)?;
    shard.append(&[AppendEntry {
        workflow: wf.clone(),
        payload: AppendPayload::Record(rec),
    }])?;
    shard.sync()?;
    Ok(())
}

/// `sqrl signal`: append a `SignalReceived` record.
pub fn signal(data: &Path, id: &str, name: &str, json_arg: &str) -> CliResult<()> {
    eprintln!("{OFFLINE_WARNING}");
    let value: serde_json::Value = serde_json::from_str(json_arg)
        .map_err(|e| CliError(format!("invalid JSON payload: {e}")))?;
    let payload = sqrl_core::codec::to_vec(&value, "signal payload")?;
    let mut store = Store::open_existing(data)?;
    let (wf, index, at) = prepare_append(&mut store, id)?;
    let rec = JournalRecord {
        index,
        at,
        event: JournalEvent::SignalReceived {
            name: name.to_string(),
            payload,
        },
    };
    append_one(&mut store, &wf, rec)?;
    println!(
        "appended SignalReceived name={name:?} to `{id}` at index {index}, t+{}ms \
(logical time reused from the last record — offline tool, no wall clock)",
        at.as_millis()
    );
    Ok(())
}

/// `sqrl cancel`: append a `WorkflowCancelled` record.
pub fn cancel(data: &Path, id: &str) -> CliResult<()> {
    eprintln!("{OFFLINE_WARNING}");
    let mut store = Store::open_existing(data)?;
    let (wf, index, at) = prepare_append(&mut store, id)?;
    let rec = JournalRecord {
        index,
        at,
        event: JournalEvent::WorkflowCancelled,
    };
    append_one(&mut store, &wf, rec)?;
    println!(
        "appended WorkflowCancelled to `{id}` at index {index}, t+{}ms",
        at.as_millis()
    );
    Ok(())
}

/// `sqrl resume`: append a `WorkflowResumed` record to a Failed workflow.
pub fn resume(data: &Path, id: &str) -> CliResult<()> {
    eprintln!("{OFFLINE_WARNING}");
    let mut store = Store::open_existing(data)?;
    let wf = WorkflowId::new(id);
    let readout = store.read(&wf)?;
    let d = derive(&readout);
    if d.state != DerivedState::Failed {
        return Err(CliError(format!(
            "workflow `{id}` is not Failed (derived state: {}); \
resume only voids a terminal failure",
            d.state.human()
        )));
    }
    let rec = JournalRecord {
        index: d.next_index,
        at: d.append_at,
        event: JournalEvent::WorkflowResumed,
    };
    let (index, at) = (d.next_index, d.append_at);
    append_one(&mut store, &wf, rec)?;
    println!(
        "appended WorkflowResumed to `{id}` at index {index}, t+{}ms \
(the engine re-runs the failed step on next start)",
        at.as_millis()
    );
    Ok(())
}

// ---------------------------------------------------------------- fork

/// `sqrl fork`: copy a full journal prefix into a new workflow id.
pub fn fork(data: &Path, id: &str, from_index: u64, new_id: &str) -> CliResult<()> {
    eprintln!("{OFFLINE_WARNING}");
    if from_index == 0 {
        return Err(CliError(
            "--from-index must be >= 1 (a fork needs at least the WorkflowStarted record \
at index 0)"
                .into(),
        ));
    }
    if id == new_id {
        return Err(CliError("--new-id must differ from the source id".into()));
    }
    let mut store = Store::open_existing(data)?;
    let src = WorkflowId::new(id);
    let dst = WorkflowId::new(new_id);
    let readout = store.read(&src)?;
    match readout.records.first() {
        None => {
            return Err(CliError(format!(
                "workflow `{id}` has no journal records to copy (history is snapshot-only)"
            )))
        }
        Some(r) if r.index > 0 => {
            return Err(CliError(format!(
                "cannot fork `{id}`: history before index {} was compacted away by a snapshot; \
only a full prefix (starting at index 0) can be forked",
                r.index
            )))
        }
        Some(_) => {}
    }
    let dst_idx = store.shard_index_for(&dst);
    if store.shard(dst_idx)?.list()?.contains(&dst) {
        return Err(CliError(format!(
            "workflow `{new_id}` already exists; refusing to overwrite"
        )));
    }
    let entries: Vec<AppendEntry> = readout
        .records
        .iter()
        .filter(|r| r.index < from_index)
        .map(|r| AppendEntry {
            workflow: dst.clone(),
            payload: AppendPayload::Record(r.clone()),
        })
        .collect();
    let copied = entries.len();
    let shard = store.shard(dst_idx)?;
    shard.append(&entries)?;
    shard.sync()?;
    println!(
        "forked `{id}` -> `{new_id}` (shard {dst_idx}): copied {copied} record(s), \
indexes 0..{copied} kept as-is, no snapshot"
    );
    Ok(())
}

// ---------------------------------------------------------------- compact

/// `sqrl compact`: run `maintain()` on every shard, print before/after stats.
pub fn compact(data: &Path) -> CliResult<()> {
    eprintln!("{OFFLINE_WARNING}");
    let mut store = Store::open_existing(data)?;
    for idx in 0..store.num_shards() {
        let shard = store.shard(idx)?;
        let before = shard.stats();
        shard.maintain()?;
        let after = shard.stats();
        println!(
            "shard {idx}: live_segments {} -> {}, segments_deleted {} -> {}",
            before.live_segments,
            after.live_segments,
            before.segments_deleted,
            after.segments_deleted
        );
    }
    Ok(())
}

// ---------------------------------------------------------------- replay

/// `sqrl replay`: structural journal validation. Returns `true` when every
/// checked workflow is clean.
pub fn replay(data: &Path, only: Option<&str>) -> CliResult<bool> {
    let mut store = Store::open_existing(data)?;
    let mut targets: Vec<(usize, WorkflowId)> = Vec::new();
    if let Some(id) = only {
        let wf = WorkflowId::new(id);
        let idx = store.shard_index_for(&wf);
        // Existence check with a friendly error.
        store.read(&wf)?;
        targets.push((idx, wf));
    } else {
        for idx in 0..store.num_shards() {
            for id in store.shard(idx)?.list()? {
                targets.push((idx, id));
            }
        }
        targets.sort_by(|a, b| a.1.cmp(&b.1));
    }

    let mut all_ok = true;
    let mut checked = 0usize;
    for (idx, wf) in targets {
        let readout = store.shard(idx)?.read(&wf)?;
        let violations = validate_readout(&readout);
        checked += 1;
        if violations.is_empty() {
            let snap = if readout.snapshot.is_some() {
                " + snapshot"
            } else {
                ""
            };
            println!("{wf}: OK ({} record(s){snap})", readout.records.len());
        } else {
            all_ok = false;
            for v in violations {
                println!("{wf}: VIOLATION: {v}");
            }
        }
    }
    if all_ok {
        println!("replay check passed: {checked} workflow(s) structurally consistent");
    } else {
        println!("replay check FAILED (see violations above)");
    }
    println!(
        "note: this validates journal integrity only; non-determinism against the actual \
workflow code is validated in-process by engine replay"
    );
    Ok(all_ok)
}

/// Structural checks over one workflow's readout.
fn validate_readout(readout: &JournalReadout) -> Vec<String> {
    let mut violations = Vec::new();
    let mut step_seqs: BTreeSet<u64> = BTreeSet::new();
    let mut timer_seqs: BTreeSet<u64> = BTreeSet::new();
    let mut expected_index: u64 = 0;
    let mut last_at = LogicalTime::ZERO;

    if let Some(snap) = &readout.snapshot {
        expected_index = snap.upto;
        last_at = snap.meta.wf_time;
        step_seqs.extend(snap.meta.inflight_steps.keys().copied());
        timer_seqs.extend(snap.meta.pending_timers.keys().copied());
        match snap.decode_body() {
            Ok(body) => {
                for (seq, cmd) in &body.cmds {
                    match cmd {
                        CmdDesc::Step { .. } => {
                            step_seqs.insert(*seq);
                        }
                        CmdDesc::Timer => {
                            timer_seqs.insert(*seq);
                        }
                        CmdDesc::AwaitSignal { .. } | CmdDesc::Patch { .. } => {}
                    }
                }
            }
            Err(e) => violations.push(format!("snapshot body undecodable: {e}")),
        }
    } else {
        match readout.records.first() {
            None => violations.push("empty journal: no snapshot and no records".into()),
            Some(r) => {
                if !matches!(r.event, JournalEvent::WorkflowStarted { .. }) {
                    violations.push(format!(
                        "first record #{} is {}, expected WorkflowStarted",
                        r.index,
                        r.event.kind()
                    ));
                }
            }
        }
    }

    for rec in &readout.records {
        if rec.index != expected_index {
            violations.push(format!(
                "index not dense: expected #{expected_index}, found #{} ({})",
                rec.index,
                rec.event.kind()
            ));
        }
        expected_index = rec.index + 1;
        if rec.at < last_at {
            violations.push(format!(
                "#{}: logical time went backwards (t+{}ms after t+{}ms)",
                rec.index,
                rec.at.as_millis(),
                last_at.as_millis()
            ));
        }
        last_at = last_at.max(rec.at);
        match &rec.event {
            JournalEvent::StepScheduled { seq, .. } => {
                step_seqs.insert(*seq);
            }
            JournalEvent::TimerScheduled { seq, .. } => {
                timer_seqs.insert(*seq);
            }
            JournalEvent::StepCompleted { seq, .. } | JournalEvent::StepFailed { seq, .. } => {
                if !step_seqs.contains(seq) {
                    violations.push(format!(
                        "#{}: {} seq={seq} has no preceding StepScheduled \
(and the seq is not covered by a snapshot)",
                        rec.index,
                        rec.event.kind()
                    ));
                }
            }
            JournalEvent::TimerFired { seq } => {
                if !timer_seqs.contains(seq) {
                    violations.push(format!(
                        "#{}: TimerFired seq={seq} has no preceding TimerScheduled \
(and the seq is not covered by a snapshot)",
                        rec.index
                    ));
                }
            }
            JournalEvent::WorkflowStarted { .. }
            | JournalEvent::SignalAwaited { .. }
            | JournalEvent::SignalReceived { .. }
            | JournalEvent::PatchRecorded { .. }
            | JournalEvent::WorkflowCompleted { .. }
            | JournalEvent::WorkflowFailed { .. }
            | JournalEvent::WorkflowCancelled
            | JournalEvent::WorkflowResumed => {}
        }
    }
    violations
}

// ---------------------------------------------------------------- bench

/// `sqrl bench`: storage-level append/read smoke benchmark.
pub fn bench(data: &Path, workflows: usize, steps: usize) -> CliResult<()> {
    eprintln!("{OFFLINE_WARNING}");
    eprintln!(
        "note: STORAGE-level benchmark (WAL append+fsync+read only, no engine, no workflow \
code); it appends synthetic records — use a scratch directory"
    );
    if workflows == 0 {
        return Err(CliError("--workflows must be >= 1".into()));
    }
    let mut store = Store::open_or_create(data)?;
    let num_shards = store.num_shards();
    // Open (and recover) every shard up-front so the timed section measures
    // appends, not recovery scans.
    for idx in 0..num_shards {
        store.shard(idx)?;
    }
    let ids: Vec<WorkflowId> = (0..workflows)
        .map(|w| WorkflowId::new(format!("bench-{w:06}")))
        .collect();
    let payload = sqrl_core::codec::to_vec(&serde_json::json!({"bench": true}), "bench payload")?;

    const SYNC_EVERY: usize = 32; // periodic durability barrier

    // Benchmark wall-clock timing only; `at` fields below stay synthetic
    // logical times and never read the clock.
    #[allow(clippy::disallowed_methods)]
    let t_append = std::time::Instant::now();
    let mut appended: u64 = 0;
    for (w, id) in ids.iter().enumerate() {
        let mut entries = Vec::with_capacity(1 + 2 * steps);
        let push = |entries: &mut Vec<AppendEntry>, index: u64, event: JournalEvent| {
            entries.push(AppendEntry {
                workflow: id.clone(),
                payload: AppendPayload::Record(JournalRecord {
                    index,
                    // Synthetic logical time: one millisecond per record.
                    at: LogicalTime::from_millis(index),
                    event,
                }),
            });
        };
        push(
            &mut entries,
            0,
            JournalEvent::WorkflowStarted {
                name: "bench".into(),
                version: 1,
                input: payload.clone(),
                seed: w as u64,
            },
        );
        for s in 0..steps {
            let seq = s as u64;
            push(
                &mut entries,
                1 + 2 * seq,
                JournalEvent::StepScheduled {
                    seq,
                    name: "bench-step".into(),
                },
            );
            push(
                &mut entries,
                2 + 2 * seq,
                JournalEvent::StepCompleted {
                    seq,
                    result: payload.clone(),
                },
            );
        }
        appended += entries.len() as u64;
        let shard_idx = id.shard(num_shards);
        let shard = store.shard(shard_idx)?;
        shard.append(&entries)?;
        if (w + 1) % SYNC_EVERY == 0 {
            shard.sync()?;
        }
    }
    for idx in 0..num_shards {
        store.shard(idx)?.sync()?;
    }
    let append_secs = t_append.elapsed().as_secs_f64().max(1e-9);

    #[allow(clippy::disallowed_methods)]
    // Benchmark wall-clock timing only (see above).
    let t_read = std::time::Instant::now();
    let mut read_records: u64 = 0;
    for id in &ids {
        let shard_idx = id.shard(num_shards);
        let readout = store.shard(shard_idx)?.read(id)?;
        read_records += readout.records.len() as u64;
    }
    let read_secs = t_read.elapsed().as_secs_f64().max(1e-9);

    let mut bytes_written: u64 = 0;
    let mut fsyncs: u64 = 0;
    for idx in 0..num_shards {
        let stats = store.shard(idx)?.stats();
        bytes_written += stats.bytes_written;
        fsyncs += stats.fsyncs;
    }

    println!(
        "storage benchmark ({workflows} workflow(s) x {steps} step pair(s), {num_shards} shard(s))"
    );
    println!(
        "  append: {appended} records in {append_secs:.3}s -> {:.0} records/s (with periodic sync, {fsyncs} fsync(s))",
        appended as f64 / append_secs
    );
    println!(
        "  read:   {read_records} records in {read_secs:.3}s -> {:.0} records/s",
        read_records as f64 / read_secs
    );
    println!("  bytes written: {bytes_written}");
    Ok(())
}
