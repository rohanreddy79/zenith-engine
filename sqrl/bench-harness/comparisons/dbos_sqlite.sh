#!/usr/bin/env bash
# DBOS Transact (embedded SQLite mode) W1 comparison.
# Usage: ./dbos_sqlite.sh [N_WORKFLOWS] [M_STEPS]
set -euo pipefail
N="${1:-1000}"; M="${2:-5}"
work=$(mktemp -d)
cd "$work"
npm init -y >/dev/null
npm install @dbos-inc/dbos-sdk better-sqlite3 >/dev/null
cat > bench.mjs <<JS
import { DBOS } from "@dbos-inc/dbos-sdk";
const N = ${N}, M = ${M};
class Bench {
  static async step(i) { return i * 2; }
  static async wf(id) {
    let acc = 0;
    for (let s = 0; s < M; s++) acc += await DBOS.runStep(() => Bench.step(s), { name: "step-" + s });
    return acc;
  }
}
DBOS.registerWorkflow(Bench, "wf");
// system database: local sqlite file (no Postgres)
DBOS.setConfig({ name: "bench", systemDatabaseUrl: "sqlite://" + process.cwd() + "/dbos.sqlite" });
await DBOS.launch();
const t0 = performance.now();
const handles = [];
for (let i = 0; i < N; i++) handles.push(DBOS.startWorkflow(Bench, { workflowID: "wf-" + i }).wf(i));
await Promise.all((await Promise.all(handles)).map(h => h.getResult()));
const dt = (performance.now() - t0) / 1000;
console.log("dbos workflows/s", (N / dt).toFixed(1));
await DBOS.shutdown();
JS
node bench.mjs
