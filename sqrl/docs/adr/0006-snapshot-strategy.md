# 0006 — Snapshots: compacted history with lazy meta/body split

## Context
Rust cannot serialize a suspended future, so "snapshot the continuation"
is impossible. Long-lived workflows (millions of events) are first-class:
no history cap, bounded recovery cost.

## Decision
A snapshot is the workflow's history compacted to what replay needs, in two
parts: **meta** (start info, in-flight steps, pending timers, terminal
status — bytes, not history-sized) and **body** (command table + ordered
revelation stream, stored as one pre-serialized blob, decoded only on
materialization). Cadence is amortized — at least `snapshot_every` new
records AND ≥¼ of total history since the last snapshot — so lifetime
snapshot bytes stay O(history). Quiescent workflows are additionally
snapshotted at clean shutdown and at passivation. **Lazy recovery**: a
workflow whose last record is a snapshot with no bare in-flight steps
recovers as passivated — timers re-armed from meta, body untouched, no code
run — in O(meta); it materializes (full replay from the snapshot) only when
something happens to it. Any journal tail after the snapshot forces eager
materialization (a torn tail can hide runnable work). Completed/cancelled
workflows write terminal snapshots so segments GC; failed workflows keep
full journals for fork/debug.

## Consequences
+ Clean-shutdown restart and passivation reload are O(metadata) per
  workflow regardless of history length (measured: >10× vs full replay in
  the acceptance test).
+ Segment GC bounds disk usage without a history cap.
− Crash (unclean) recovery of an active workflow remains O(history-since-
  snapshot) replay — fundamental to replay-based recovery.
− Write amplification from snapshot cadence (~5× lifetime bytes at the
  default factor); measured in Phase-2 benchmarks, tunable, disable-able.
