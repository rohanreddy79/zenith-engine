#!/usr/bin/env bash
# Temporal dev server W1 comparison.
# Usage: ./temporal_dev.sh [N_WORKFLOWS] [M_STEPS]
set -euo pipefail
N="${1:-1000}"; M="${2:-5}"
temporal server start-dev --headless --db-filename "$(mktemp -u)".db &
TEMPORAL_PID=$!
trap 'kill $TEMPORAL_PID' EXIT
sleep 5
work=$(mktemp -d); cd "$work"
npm init -y >/dev/null
npm install @temporalio/client @temporalio/worker @temporalio/workflow @temporalio/activity >/dev/null
mkdir -p src
cat > src/workflows.mjs <<JS
import { proxyActivities } from "@temporalio/workflow";
const { step } = proxyActivities({ startToCloseTimeout: "10s" });
export async function wf(m) { let acc = 0; for (let s = 0; s < m; s++) acc += await step(s); return acc; }
JS
cat > src/bench.mjs <<JS
import { Worker } from "@temporalio/worker";
import { Client } from "@temporalio/client";
const N = ${N}, M = ${M};
const worker = await Worker.create({
  workflowsPath: new URL("./workflows.mjs", import.meta.url).pathname,
  activities: { step: async (i) => i * 2 },
  taskQueue: "bench",
});
const run = worker.run();
const client = new Client();
const t0 = performance.now();
const handles = await Promise.all(
  Array.from({ length: N }, (_, i) =>
    client.workflow.start("wf", { args: [M], taskQueue: "bench", workflowId: "wf-" + i })));
await Promise.all(handles.map(h => h.result()));
const dt = (performance.now() - t0) / 1000;
console.log("temporal workflows/s", (N / dt).toFixed(1));
worker.shutdown(); await run;
JS
node src/bench.mjs
