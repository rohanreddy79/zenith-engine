//! Rendering helpers: payload previews, event field formatting (human and
//! JSON), and small string utilities.

use serde_json::{json, Value};
use sqrl_core::snapshot::SnapshotRecord;
use sqrl_core::{JournalEvent, JournalRecord, LogicalTime};
use std::fmt::Write as _;

/// Max payload preview width in human output.
pub const PAYLOAD_PREVIEW: usize = 60;
/// Max hex bytes shown for an undecodable payload.
const HEX_PREVIEW_BYTES: usize = 64;

/// Truncate a string to `max_chars` characters, appending `…` when cut.
pub fn truncate_str(s: &str, max_chars: usize) -> String {
    if s.chars().count() <= max_chars {
        s.to_string()
    } else {
        let cut: String = s.chars().take(max_chars.saturating_sub(1)).collect();
        format!("{cut}…")
    }
}

fn hex_string(bytes: &[u8]) -> String {
    let mut s = String::with_capacity(bytes.len() * 2);
    for b in bytes {
        let _ = write!(s, "{b:02x}");
    }
    s
}

/// Decode a payload for human display: self-describing MessagePack decodes
/// into a JSON value; anything else falls back to a hex preview.
pub fn payload_human(bytes: &[u8]) -> String {
    match sqrl_core::codec::from_slice::<Value>(bytes, "payload") {
        Ok(v) => truncate_str(&v.to_string(), PAYLOAD_PREVIEW),
        Err(_) => {
            let shown = &bytes[..bytes.len().min(HEX_PREVIEW_BYTES)];
            let mut s = format!("0x{}", hex_string(shown));
            if bytes.len() > HEX_PREVIEW_BYTES {
                let _ = write!(s, "… ({} bytes)", bytes.len());
            }
            s
        }
    }
}

/// Decode a payload for JSON output; undecodable payloads become an object
/// with a hex preview.
pub fn payload_json(bytes: &[u8]) -> Value {
    match sqrl_core::codec::from_slice::<Value>(bytes, "payload") {
        Ok(v) => v,
        Err(_) => json!({
            "_undecodable_hex": hex_string(&bytes[..bytes.len().min(HEX_PREVIEW_BYTES)]),
            "_len": bytes.len(),
        }),
    }
}

fn fmt_at(at: LogicalTime) -> String {
    format!("t+{}ms", at.as_millis())
}

/// Human rendering of an event's relevant fields (payloads decoded and
/// truncated).
pub fn event_fields_human(event: &JournalEvent) -> String {
    match event {
        JournalEvent::WorkflowStarted {
            name,
            version,
            input,
            seed,
        } => format!(
            "name={name:?} version={version} seed={seed} input={}",
            payload_human(input)
        ),
        JournalEvent::StepScheduled { seq, name } => format!("seq={seq} name={name:?}"),
        JournalEvent::StepCompleted { seq, result } => {
            format!("seq={seq} result={}", payload_human(result))
        }
        JournalEvent::StepFailed {
            seq,
            error,
            attempt,
            retry_at,
        } => {
            let retry = match retry_at {
                Some(t) => format!("retry_at={}", fmt_at(*t)),
                None => "final".to_string(),
            };
            format!(
                "seq={seq} attempt={attempt} {retry} error={}",
                truncate_str(&error.to_string(), PAYLOAD_PREVIEW)
            )
        }
        JournalEvent::TimerScheduled { seq, fire_at } => {
            format!("seq={seq} fire_at={}", fmt_at(*fire_at))
        }
        JournalEvent::TimerFired { seq } => format!("seq={seq}"),
        JournalEvent::SignalAwaited { seq, name } => format!("seq={seq} name={name:?}"),
        JournalEvent::SignalReceived { name, payload } => {
            format!("name={name:?} payload={}", payload_human(payload))
        }
        JournalEvent::PatchRecorded { seq, id } => format!("seq={seq} id={id:?}"),
        JournalEvent::WorkflowCompleted { output } => {
            format!("output={}", payload_human(output))
        }
        JournalEvent::WorkflowFailed { error } => format!(
            "error={}",
            truncate_str(&error.to_string(), PAYLOAD_PREVIEW)
        ),
        JournalEvent::WorkflowCancelled | JournalEvent::WorkflowResumed => String::new(),
    }
}

/// JSON rendering of an event's fields (payloads decoded where possible).
pub fn event_fields_json(event: &JournalEvent) -> Value {
    match event {
        JournalEvent::WorkflowStarted {
            name,
            version,
            input,
            seed,
        } => json!({
            "name": name, "version": version, "seed": seed,
            "input": payload_json(input),
        }),
        JournalEvent::StepScheduled { seq, name } => json!({ "seq": seq, "name": name }),
        JournalEvent::StepCompleted { seq, result } => {
            json!({ "seq": seq, "result": payload_json(result) })
        }
        JournalEvent::StepFailed {
            seq,
            error,
            attempt,
            retry_at,
        } => json!({
            "seq": seq, "attempt": attempt,
            "error": error.to_string(),
            "retry_at_ms": retry_at.map(LogicalTime::as_millis),
        }),
        JournalEvent::TimerScheduled { seq, fire_at } => {
            json!({ "seq": seq, "fire_at_ms": fire_at.as_millis() })
        }
        JournalEvent::TimerFired { seq } => json!({ "seq": seq }),
        JournalEvent::SignalAwaited { seq, name } => json!({ "seq": seq, "name": name }),
        JournalEvent::SignalReceived { name, payload } => {
            json!({ "name": name, "payload": payload_json(payload) })
        }
        JournalEvent::PatchRecorded { seq, id } => json!({ "seq": seq, "id": id }),
        JournalEvent::WorkflowCompleted { output } => json!({ "output": payload_json(output) }),
        JournalEvent::WorkflowFailed { error } => json!({ "error": error.to_string() }),
        JournalEvent::WorkflowCancelled | JournalEvent::WorkflowResumed => json!({}),
    }
}

/// JSON rendering of one journal record.
pub fn record_json(rec: &JournalRecord) -> Value {
    json!({
        "index": rec.index,
        "at_ms": rec.at.as_millis(),
        "kind": rec.event.kind(),
        "fields": event_fields_json(&rec.event),
    })
}

/// One-line human summary of a snapshot record's metadata.
pub fn snapshot_summary_human(snap: &SnapshotRecord) -> String {
    let terminal = match &snap.meta.terminal {
        Some(sqrl_core::snapshot::TerminalStatus::Completed { .. }) => "completed",
        Some(sqrl_core::snapshot::TerminalStatus::Failed { .. }) => "failed",
        Some(sqrl_core::snapshot::TerminalStatus::Cancelled) => "cancelled",
        None => "none",
    };
    let start = match &snap.meta.start {
        Some(s) => format!("{}@v{}", s.name, s.version),
        None => "?".to_string(),
    };
    format!(
        "[snapshot upto={} start={} terminal={} inflight_steps={} pending_timers={} wf_time={}]",
        snap.upto,
        start,
        terminal,
        snap.meta.inflight_steps.len(),
        snap.meta.pending_timers.len(),
        fmt_at(snap.meta.wf_time),
    )
}

/// JSON summary of a snapshot record's metadata.
pub fn snapshot_summary_json(snap: &SnapshotRecord) -> Value {
    let terminal = snap.meta.terminal.as_ref().map(|t| match t {
        sqrl_core::snapshot::TerminalStatus::Completed { .. } => "completed",
        sqrl_core::snapshot::TerminalStatus::Failed { .. } => "failed",
        sqrl_core::snapshot::TerminalStatus::Cancelled => "cancelled",
    });
    json!({
        "upto": snap.upto,
        "start": snap.meta.start.as_ref().map(|s| json!({ "name": s.name, "version": s.version })),
        "terminal": terminal,
        "inflight_steps": snap.meta.inflight_steps.len(),
        "pending_timers": snap.meta.pending_timers.len(),
        "wf_time_ms": snap.meta.wf_time.as_millis(),
    })
}
