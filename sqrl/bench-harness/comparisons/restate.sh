#!/usr/bin/env bash
# Restate single-node W1 comparison.
# Usage: ./restate.sh [N_WORKFLOWS] [M_STEPS]
set -euo pipefail
N="${1:-1000}"; M="${2:-5}"
restate-server &
RESTATE_PID=$!
trap 'kill $RESTATE_PID' EXIT
sleep 5
work=$(mktemp -d); cd "$work"
npm init -y >/dev/null
npm install @restatedev/restate-sdk >/dev/null
cat > svc.mjs <<JS
import * as restate from "@restatedev/restate-sdk";
const M = ${M};
restate.endpoint().bind(restate.service({
  name: "bench",
  handlers: {
    wf: async (ctx, i) => {
      let acc = 0;
      for (let s = 0; s < M; s++) acc += await ctx.run("step-" + s, () => s * 2);
      return acc;
    },
  },
})).listen(9080);
JS
node svc.mjs &
SVC_PID=$!
trap 'kill $RESTATE_PID $SVC_PID' EXIT
sleep 2
restate deployments register --yes http://localhost:9080
t0=$(date +%s.%N)
seq 0 $((N-1)) | xargs -P 64 -I{} curl -s -X POST "http://localhost:8080/bench/wf" -H 'content-type: application/json' -d '{}' -o /dev/null
t1=$(date +%s.%N)
echo "restate workflows/s $(echo "$N / ($t1 - $t0)" | bc -l | cut -c1-8)"
