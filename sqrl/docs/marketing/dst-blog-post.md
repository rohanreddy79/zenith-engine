# Launch blog post — skeleton

**Audience:** engineers who will pass it around and cite it in internal
design docs. First person, ~2,500 words, code and real logs throughout.
Both bug stories below are real, from this repository's history — keep
them exactly accurate (`docs/dst.md` is the source of truth).

## Title candidates

1. We simulated 10,000 crashing universes and found the bugs that eat
   your data
2. kill -9 is the easy part
3. Your recovery code is lying to you (ours was, twice)

## Sections

### 1. Cold open: the demo

The `crash_me` GIF, three sentences of setup. Then the turn: *"This demo
is easy. What's hard is knowing it still works when the disk tears a
write in half at the worst possible instant. Here's how we tried to
prove it — and the two bugs the proof found."*

### 2. Why deterministic simulation

The engine is a passive state machine — no threads, clock, entropy, or
I/O of its own. Drivers inject all of it, so the same production code
runs under a seeded scheduler + virtual clock + simulated disk, and an
entire multi-crash history becomes a pure function of one seed. A
failure at seed 311 reproduces in milliseconds, forever. Credit prior
art honestly: FoundationDB, TigerBeetle, Antithesis.

### 3. A disk meaner than any real disk

SimDisk's crash model: every unsynced write independently kept, dropped,
or torn; creates/renames/deletes pending until directory fsync; deletes
that resurrect; deliberate bit flips. *"If your recovery survives this
on 10,000 seeds, ext4 is a gentle friend."*

### 4. The paranoid oracle

The idea worth stealing: checking end-state consistency isn't enough —
check the **acknowledgment contract** itself. At every completion ack,
fork the disk keeping only durably-written bytes (as if power died at
that exact instant), re-run full recovery on the fork, and assert the
promised result is still recoverable. Durability stops being a vibe and
becomes an assertion that runs tens of thousands of times per CI run
(`SQRL_DST_PARANOID`).

### 5. Bug #1: recovery trusted the page cache

The seed-3 story. Process A appends records and dies before fsync.
Process B starts and reads the WAL — and sees A's unfsynced writes,
because reads go through the page cache. B builds state on them and
acknowledges results on top... then power fails, and bytes nobody ever
fsynced vanish — taking acknowledged history with them. Fix: fsync every
live segment plus the directory at open, before accepting a single
append (the discipline SQLite and PostgreSQL learned decades ago). Show
the failing seed's log.

### 6. Bug #2: the torn tail was a time bomb for the *next* crash

The subtle one. A crash tears the last record. Recovery correctly stops
*reading* at the tear — but adopted the file *end* as the append offset,
entombing garbage bytes mid-stream. Everything works fine... until the
following recovery reads that garbage, classifies it as corruption, and
truncates — destroying durably-acknowledged records written *after* it.
The damage lands one full crash-cycle away from the cause. Fix: cut the
torn tail at the last valid record boundary before accepting appends.

### 7. Confession: our simulator lied to us first

The meta-lesson that buys the post its credibility: bug #2 hid for a
while because the simulated disk's `truncate()` never actually shrank
files — recovery's cuts silently didn't stick *in simulation*. The test
rig is code too, and it can lie. The simulator's own crash semantics are
now pinned by tests.

### 8. The numbers

Paste the real coverage block from `docs/dst.md`: 10,000 seeds in 89 s —
171k crashes (70k mid-recovery), 68k caught panics, 80k injected I/O
errors, 11k corruption truncations, every seed byte-identical on re-run.
Every number keeps its one-line repro command.

### 9. What this doesn't prove

Simulation validates the logic above the syscall layer — not kernels or
firmware that lie about fsync. Single node only. At-least-once. Listing
what you *can't* claim is what makes the rest believable.

### 10. Run it yourself

```bash
SQRL_DST_PARANOID=1 cargo test -p sqrl-tests --release dst_long -- --ignored --nocapture
```

Ten thousand universes on a laptop, about ninety seconds. End on the
invitation, not a sales line.
