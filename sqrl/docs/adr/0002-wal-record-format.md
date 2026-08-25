# 0002 — WAL record format

## Context
A single WAL bug loses user data. The format must detect torn writes and
bit rot at record granularity, be versioned from day one, and be scannable
without an index.

## Decision
`[len: u32 LE][crc32c: u32 LE][record_type: u8][format_version: u8][payload]`
with crc32c (Castagnoli, hardware-accelerated) over everything after the
CRC field; `len` bounded to 256 MiB; three record types (entry, snapshot,
segment header); every segment begins with a checksummed header carrying
its own sequence number. Recovery is prefix-valid: scanning stops at the
first invalid record, truncates there (byte offset logged), and drops later
segments — the WAL is one logical stream.

## Consequences
+ Every corruption class in the DST fault model (tear, flip, hole,
  resurrection) is detected and converted to a clean truncation.
+ Format version rejection is per-record: future formats never get
  half-read.
− 10 bytes fixed overhead per record (measured in write-amplification
  benchmarks; acceptable).
