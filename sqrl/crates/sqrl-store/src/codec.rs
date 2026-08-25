//! WAL record envelope: `[len: u32][crc32c: u32][record_type: u8][format_version: u8][payload]`.
//!
//! * `len` is little-endian and counts `record_type + format_version +
//!   payload` (i.e. `payload.len() + 2`).
//! * `crc32c` (Castagnoli) covers exactly the `len` bytes that follow it.
//! * Every record is checksummed; decoding stops at the first record whose
//!   length, CRC, type, or version is invalid — the WAL's prefix-validity
//!   rule. See `docs/on-disk-format.md`.

use sqrl_core::codec::SQRL_FORMAT_VERSION;
use sqrl_core::event::JournalRecord;
use sqrl_core::snapshot::SnapshotRecord;
use sqrl_core::{StorageError, WorkflowId};

/// Envelope header size in bytes (len + crc + type + version).
pub const HEADER: usize = 4 + 4 + 1 + 1;

/// Maximum accepted record length (type+version+payload). Records claiming
/// more are treated as corruption. Generous: payloads are already limited to
/// ~1 MiB by the engine; snapshots may be larger.
pub const MAX_RECORD_LEN: u32 = 256 * 1024 * 1024;

/// Record types.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
#[repr(u8)]
pub enum RecordType {
    /// A journal event record ([`WalEntry`]).
    Entry = 1,
    /// A snapshot record ([`WalSnapshot`]).
    Snapshot = 2,
    /// A segment header ([`SegmentHeader`]).
    SegmentHeader = 3,
}

impl RecordType {
    fn from_u8(v: u8) -> Option<RecordType> {
        match v {
            1 => Some(RecordType::Entry),
            2 => Some(RecordType::Snapshot),
            3 => Some(RecordType::SegmentHeader),
            _ => None,
        }
    }
}

/// A journal event, as serialized into the WAL.
#[derive(Debug, Clone, PartialEq, serde::Serialize, serde::Deserialize)]
pub struct WalEntry {
    /// Owning workflow.
    pub workflow: WorkflowId,
    /// The record.
    pub record: JournalRecord,
}

/// A snapshot, as serialized into the WAL.
#[derive(Debug, Clone, PartialEq, serde::Serialize, serde::Deserialize)]
pub struct WalSnapshot {
    /// Owning workflow.
    pub workflow: WorkflowId,
    /// The snapshot.
    pub snapshot: SnapshotRecord,
}

/// First record of every segment file.
#[derive(Debug, Clone, PartialEq, serde::Serialize, serde::Deserialize)]
pub struct SegmentHeader {
    /// Magic: always `"sqrl-seg"`.
    pub magic: String,
    /// Segment sequence number (also encoded in the file name).
    pub segment_seq: u64,
    /// Shard index that owns this segment.
    pub shard: u32,
}

/// A decoded WAL record.
#[derive(Debug, Clone, PartialEq)]
pub enum WalRecord {
    /// A journal event.
    Entry(WalEntry),
    /// A snapshot.
    Snapshot(WalSnapshot),
    /// A segment header.
    SegmentHeader(SegmentHeader),
}

/// Encode a record into its checksummed envelope.
pub fn encode(record: &WalRecord) -> Result<Vec<u8>, StorageError> {
    let (ty, payload) = match record {
        WalRecord::Entry(e) => (RecordType::Entry, to_payload(e)?),
        WalRecord::Snapshot(s) => (RecordType::Snapshot, to_payload(s)?),
        WalRecord::SegmentHeader(h) => (RecordType::SegmentHeader, to_payload(h)?),
    };
    let len = (payload.len() + 2) as u32;
    let mut body = Vec::with_capacity(HEADER + payload.len());
    body.extend_from_slice(&len.to_le_bytes());
    body.extend_from_slice(&[0u8; 4]); // crc placeholder
    body.push(ty as u8);
    body.push(SQRL_FORMAT_VERSION);
    body.extend_from_slice(&payload);
    let crc = crc32c::crc32c(&body[8..]);
    body[4..8].copy_from_slice(&crc.to_le_bytes());
    Ok(body)
}

fn to_payload<T: serde::Serialize>(v: &T) -> Result<Vec<u8>, StorageError> {
    rmp_serde::encode::to_vec_named(v).map_err(|e| StorageError::Codec(e.to_string()))
}

/// Why decoding stopped.
#[derive(Debug, Clone, PartialEq)]
pub enum DecodeEnd {
    /// Clean end of data.
    Eof,
    /// Invalid record at this offset (truncation point).
    Invalid {
        /// Byte offset of the invalid record's envelope.
        offset: u64,
        /// Human-readable reason.
        reason: String,
    },
}

/// Try to decode one record from `buf` at `offset` (offset is used only for
/// error reporting). Returns `Ok(None)` on clean EOF (empty remainder),
/// `Ok(Some((record, consumed)))` on success, `Err(end)` on corruption.
pub fn decode_one(buf: &[u8], offset: u64) -> Result<Option<(WalRecord, usize)>, DecodeEnd> {
    if buf.is_empty() {
        return Ok(None);
    }
    if buf.len() < HEADER {
        return Err(DecodeEnd::Invalid {
            offset,
            reason: format!("truncated header: {} bytes", buf.len()),
        });
    }
    let len = u32::from_le_bytes([buf[0], buf[1], buf[2], buf[3]]);
    if !(2..=MAX_RECORD_LEN).contains(&len) {
        return Err(DecodeEnd::Invalid {
            offset,
            reason: format!("implausible record length {len}"),
        });
    }
    let total = 8 + len as usize;
    if buf.len() < total {
        return Err(DecodeEnd::Invalid {
            offset,
            reason: format!("record needs {total} bytes, only {} available", buf.len()),
        });
    }
    let stored_crc = u32::from_le_bytes([buf[4], buf[5], buf[6], buf[7]]);
    let crc = crc32c::crc32c(&buf[8..total]);
    if crc != stored_crc {
        return Err(DecodeEnd::Invalid {
            offset,
            reason: format!("crc mismatch: stored {stored_crc:08x}, computed {crc:08x}"),
        });
    }
    let ty = buf[8];
    let version = buf[9];
    if version > SQRL_FORMAT_VERSION {
        return Err(DecodeEnd::Invalid {
            offset,
            reason: format!(
                "format version {version} is newer than supported {SQRL_FORMAT_VERSION}"
            ),
        });
    }
    let payload = &buf[10..total];
    let record = match RecordType::from_u8(ty) {
        Some(RecordType::Entry) => WalRecord::Entry(from_payload(payload, offset)?),
        Some(RecordType::Snapshot) => WalRecord::Snapshot(from_payload(payload, offset)?),
        Some(RecordType::SegmentHeader) => WalRecord::SegmentHeader(from_payload(payload, offset)?),
        None => {
            return Err(DecodeEnd::Invalid {
                offset,
                reason: format!("unknown record type {ty}"),
            })
        }
    };
    Ok(Some((record, total)))
}

fn from_payload<T: serde::de::DeserializeOwned>(buf: &[u8], offset: u64) -> Result<T, DecodeEnd> {
    rmp_serde::decode::from_slice(buf).map_err(|e| DecodeEnd::Invalid {
        offset,
        reason: format!("payload decode: {e}"),
    })
}

/// Scan a whole buffer, yielding `(offset, record)` pairs and the point where
/// scanning stopped.
pub fn scan(buf: &[u8]) -> (Vec<(u64, WalRecord)>, DecodeEnd) {
    let mut out = Vec::new();
    let mut pos: usize = 0;
    loop {
        match decode_one(&buf[pos..], pos as u64) {
            Ok(None) => return (out, DecodeEnd::Eof),
            Ok(Some((rec, consumed))) => {
                out.push((pos as u64, rec));
                pos += consumed;
            }
            Err(end) => return (out, end),
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use sqrl_core::event::JournalEvent;
    use sqrl_core::LogicalTime;

    fn entry(i: u64) -> WalRecord {
        WalRecord::Entry(WalEntry {
            workflow: WorkflowId::new(format!("wf-{i}")),
            record: JournalRecord {
                index: i,
                at: LogicalTime::from_millis(i * 10),
                event: JournalEvent::StepScheduled {
                    seq: i,
                    name: format!("step-{i}"),
                },
            },
        })
    }

    #[test]
    fn round_trip_single() {
        let rec = entry(1);
        let bytes = encode(&rec).unwrap();
        let (decoded, consumed) = decode_one(&bytes, 0).unwrap().unwrap();
        assert_eq!(decoded, rec);
        assert_eq!(consumed, bytes.len());
    }

    #[test]
    fn scan_stream() {
        let mut buf = Vec::new();
        for i in 0..10 {
            buf.extend_from_slice(&encode(&entry(i)).unwrap());
        }
        let (records, end) = scan(&buf);
        assert_eq!(records.len(), 10);
        assert_eq!(end, DecodeEnd::Eof);
    }

    #[test]
    fn corruption_truncates_at_first_invalid() {
        let mut buf = Vec::new();
        let mut offsets = Vec::new();
        for i in 0..10 {
            offsets.push(buf.len() as u64);
            buf.extend_from_slice(&encode(&entry(i)).unwrap());
        }
        // Flip one byte inside record 4's payload.
        let victim = offsets[4] as usize + HEADER + 3;
        buf[victim] ^= 0xFF;
        let (records, end) = scan(&buf);
        assert_eq!(records.len(), 4, "records before the corruption survive");
        match end {
            DecodeEnd::Invalid { offset, reason } => {
                assert_eq!(offset, offsets[4]);
                assert!(reason.contains("crc"), "reason: {reason}");
            }
            DecodeEnd::Eof => panic!("must detect corruption"),
        }
    }

    #[test]
    fn torn_tail_detected() {
        let mut buf = encode(&entry(0)).unwrap();
        let full = encode(&entry(1)).unwrap();
        let cut = buf.len() as u64;
        buf.extend_from_slice(&full[..full.len() / 2]); // torn write
        let (records, end) = scan(&buf);
        assert_eq!(records.len(), 1);
        assert!(matches!(end, DecodeEnd::Invalid { offset, .. } if offset == cut));
    }

    #[test]
    fn implausible_length_rejected() {
        let mut buf = encode(&entry(0)).unwrap();
        buf[0..4].copy_from_slice(&u32::MAX.to_le_bytes());
        let (records, end) = scan(&buf);
        assert!(records.is_empty());
        assert!(matches!(end, DecodeEnd::Invalid { offset: 0, .. }));
    }

    #[test]
    fn future_format_version_rejected() {
        let mut buf = encode(&entry(0)).unwrap();
        buf[9] = SQRL_FORMAT_VERSION + 1;
        // fix the crc so only the version check trips
        let len = u32::from_le_bytes([buf[0], buf[1], buf[2], buf[3]]) as usize;
        let crc = crc32c::crc32c(&buf[8..8 + len]);
        buf[4..8].copy_from_slice(&crc.to_le_bytes());
        let (records, end) = scan(&buf);
        assert!(records.is_empty());
        assert!(
            matches!(end, DecodeEnd::Invalid { ref reason, .. } if reason.contains("format version")),
            "{end:?}"
        );
    }

    #[test]
    fn snapshot_and_header_round_trip() {
        let snap = WalRecord::Snapshot(WalSnapshot {
            workflow: WorkflowId::new("wf"),
            snapshot: SnapshotRecord {
                upto: 5,
                state: Default::default(),
            },
        });
        let hdr = WalRecord::SegmentHeader(SegmentHeader {
            magic: "sqrl-seg".into(),
            segment_seq: 7,
            shard: 2,
        });
        for rec in [snap, hdr] {
            let bytes = encode(&rec).unwrap();
            let (decoded, _) = decode_one(&bytes, 0).unwrap().unwrap();
            assert_eq!(decoded, rec);
        }
    }
}
