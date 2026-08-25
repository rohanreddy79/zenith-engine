# 0003 — Fsync policy and group commit

## Context
Per-record fsync caps throughput at disk-sync latency; no fsync at all
loses acknowledged data. Different steps have different durability worth.

## Decision
Buffered appends with `sync()` as the only durability barrier, governed by
`FsyncPolicy`: `Strict` (every batch), `Group { max_delay: 2ms, max_batch:
256 }` (default), `Relaxed { interval }` (documented loss window). Group
commit falls out of the engine's tick batching: one fsync covers every
record appended across all workflows on the shard since the last barrier.
Invariants independent of policy: workflow terminal results and
`StepOptions::fsync_strict` steps are acknowledged only after fsync;
ordinary step results are revealed to code pre-fsync (a crash replays them
— at-least-once permits it); after a failed fsync the shard poisons itself
— nothing is ever re-acknowledged on a maybe-failed disk.

## Consequences
+ Throughput scales with batch size; durability-critical steps opt into
  strictness per call site.
− `Relaxed` genuinely loses up to `interval` of acknowledged work on power
  failure; documented loudly, never default.
