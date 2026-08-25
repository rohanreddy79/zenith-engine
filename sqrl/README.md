# sqrl

> **Status: under construction (Phase 1).** This README is a stub; the full
> quickstart, guarantees, and comparison land in Phase 3.

`sqrl` is a deterministic-first, embedded, single-node **durable execution
library** for Rust — the SQLite of durable execution. `cargo add sqrl`, define
workflows as async Rust functions, and if the process is `kill -9`'d at any
point the workflow resumes from its last completed step on restart. No external
server, no Postgres, no cluster.

- **Deterministic-first**: orchestration code is a pure function of inputs +
  journaled step results; all entropy is injected.
- **Embedded WAL**: checksummed, segmented append-only journal on local disk.
- **Deterministic Simulation Testing** is a first-class feature.
- **Guarantee**: at-least-once step execution + idempotency helpers
  ("effectively-once"). `sqrl` never claims exactly-once.

See `docs/PLAN.md` for progress and `docs/` for design documents.

License: MIT OR Apache-2.0.
