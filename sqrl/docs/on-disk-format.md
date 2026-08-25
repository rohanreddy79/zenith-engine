# sqrl on-disk format

**`SQRL_FORMAT_VERSION` = 1.** The on-disk format is versioned
independently of the crate version. Any change to the encodings described
here requires a format-version bump and a documented migration path; a
migration tool is a hard requirement before any crate 1.0 (see
`CONTRIBUTING.md`).

## Directory layout

```
<store root>/
  sqrl.meta                     # store metadata (atomic, checksummed)
  shard-0/
    MANIFEST                    # live segment list (atomic, checksummed)
    wal-00000000000000000001.sqrl
    wal-00000000000000000002.sqrl
    ...
  shard-1/
    ...
```

The shard count is fixed at store creation (`sqrl.meta`); workflow→shard
placement is `fnv1a64(id) % num_shards` (`WorkflowId::shard`). The FNV-1a
function is part of this format contract — golden values are pinned in
`sqrl-core/src/id.rs` tests — because placement is persisted implicitly by
which shard directory holds a workflow's records.

## WAL record envelope

Every record in every segment:

```
offset  size  field
0       4     len        u32 LE = payload length + 2
4       4     crc32c     u32 LE, Castagnoli, over bytes [8, 8+len)
8       1     record_type   1 = journal entry, 2 = snapshot, 3 = segment header
9       1     format_version   currently 1
10      len-2 payload    self-describing MessagePack (rmp-serde, named mode)
```

Rules:

* `len` outside `[2, 256 MiB]` ⇒ corruption.
* `format_version` greater than the reader's ⇒ refuse (never guess).
* CRC mismatch, unknown type, or undecodable payload ⇒ corruption.
* **Prefix validity**: scanning stops at the first invalid record; the file
  is truncated there (offset logged) and later segments are dropped — the
  WAL is one logical stream. Data acknowledged durable is always in the
  valid prefix because acknowledgment happens only after fsync.

## Payloads

Payload encoding is rmp-serde **named** mode (struct fields and enum
variants by name): self-describing, order-insensitive, tolerant of added
optional fields (ADR 0004).

* Type 1 (`Entry`): `{ workflow, record: { index, at, event } }` where
  `index` is the dense per-workflow record index, `at` is logical
  milliseconds, and `event` is one of the `JournalEvent` variants
  (`WorkflowStarted{name,version,input,seed}`, `StepScheduled{seq,name}`,
  `StepCompleted{seq,result}`, `StepFailed{seq,error,attempt,retry_at}`,
  `TimerScheduled{seq,fire_at}`, `TimerFired{seq}`,
  `SignalAwaited{seq,name}`, `SignalReceived{name,payload}`,
  `PatchRecorded{seq,id}`, `WorkflowCompleted{output}`,
  `WorkflowFailed{error}`, `WorkflowCancelled`, `WorkflowResumed`).
* Type 2 (`Snapshot`): `{ workflow, snapshot: { upto, state } }` — the
  journal's `SnapshotTaken { seq, state }` in its stored form. Records with
  `index < upto` are superseded. `state` is the compacted history
  (`SnapshotState`): start info, command table, ordered outcome stream,
  in-flight steps/timers, optional terminal status, workflow time.
* Type 3 (`SegmentHeader`): `{ magic: "sqrl-seg", segment_seq, shard }` —
  always the first record of a segment; a mismatch invalidates the file.

User payloads (workflow inputs/outputs, step results, signal payloads) are
themselves rmp-serde named encodings of the user's types, embedded as byte
strings inside events; they are size-limited (default 1 MiB) at write time.

## Segments

Append-only, rolled at `segment_size` (default 64 MiB). Roll protocol:
fsync the old segment → rewrite MANIFEST including the new seq → create the
file + fsync the directory → write its header. A crash anywhere in that
sequence is recoverable: a manifest entry without a file is skipped with a
warning; a file not yet in the manifest is adopted if its seq is beyond the
manifest's max (and deleted as stale otherwise, which also handles files
resurrected by a crashed GC).

## MANIFEST and sqrl.meta

Both use the atomic-rewrite protocol — write `<name>.tmp`, fsync it, rename
over the target, fsync the directory — and carry
`[magic 8B][len u32][crc32c u32][payload]`. A missing **or corrupt**
manifest degrades to a directory scan; it is advisory metadata, never the
only copy of truth. `sqrl.meta` (`{ format_version, num_shards }`) is
written once at creation.

## Garbage collection

A segment is deleted only when nothing references it: no workflow has
journal records or its latest snapshot there, and it is not the current
tail. Snapshots enable GC only once **fsync-durable** — an unsynced
snapshot pins every segment up to its own. The manifest is rewritten before
files are unlinked, so a crash mid-GC leaves stale files (cleaned on next
open), never dangling manifest entries treated as live history.

## Durability contract

* `fsync` of a segment file makes its *content* durable; file creation and
  rename durability additionally require the directory fsync — both are
  modeled exactly this way by `SimDisk`, and the store is tested against
  worst-case reordering/tearing of everything unsynced.
* Nothing is acknowledged to users (workflow terminal results, strict-step
  progression) before the relevant fsync returns.
* After a failed fsync the shard is poisoned: all subsequent appends fail
  (no fsync-retry gambling).
