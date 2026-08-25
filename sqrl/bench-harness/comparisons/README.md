# Comparison harnesses (DBOS, Temporal, Restate)

These scripts run the W1-shaped workflow-throughput comparison against other
durable-execution systems **using each project's own tooling**. They are
provided so a human can reproduce the comparison on real hardware; see
`docs/benchmarks.md` for which of them were actually run for the recorded
numbers and which are marked UNVERIFIED.

Each script prints `<system> workflows/s <value>` on success.

- `dbos_sqlite.sh` — DBOS Transact (TypeScript) with its embedded SQLite
  system database. Requires: node >= 20, npm.
- `temporal_dev.sh` — Temporal dev server (`temporal server start-dev`) +
  a Go/TS worker. Requires: temporal CLI, node.
- `restate.sh` — restate-server single node + a TS service. Requires:
  restate-server, restate CLI, node.

All three intentionally mirror sqrl's W1: N concurrent workflows x M trivial
steps, measured end-to-end from first start to last completion.
