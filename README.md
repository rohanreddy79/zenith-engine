# This repository

Two projects live here:

| Project | What it is | Where |
|---|---|---|
| **🐿️ [sqrl](sqrl/)** | Embedded, deterministic-first **durable execution for Rust** — "the SQLite of durable execution" | [`sqrl/`](sqrl/) &middot; [README](sqrl/README.md) &middot; [docs](sqrl/docs/) |
| **Zenith Engine** | High-performance asynchronous runtime and task execution framework for Python | [`src/zenith/`](src/zenith/) &middot; [below](#zenith-engine) |

---

# 🐿️ sqrl

**Workflows that survive `kill -9`, embedded in your Rust process.**
`cargo add sqrl`, write workflows as plain async functions, and if the
process dies at any instant, every workflow resumes from its last
completed step on restart. No server. No cluster. One directory of
checksummed files.

Real output from `cargo run --release -p crash_me`, which SIGKILLs its own
worker mid-workflow and restarts it:

```text
[parent] run 1: spawning worker; killing it with SIGKILL in ~600 ms
[worker] executing step 1
[worker] executing step 2
[worker] executing step 3
[parent] killed worker mid-workflow (signal: 9 (SIGKILL))

[parent] run 2: respawning worker; it should RESUME, not restart
[worker] found an existing WAL: recovering `crash-demo`
[worker] executing step 3    <- was in flight at the kill: runs again (at-least-once)
[worker] executing step 4
[worker] executing step 5

=== SUCCESS: workflow survived kill -9 and resumed from its last completed step ===
```

Steps 1–2 did **not** re-execute — their results replayed from the journal.

- Durable steps, timers, and signals journaled through a crc32c-checksummed WAL; nothing acknowledged before fsync
- The exact production engine tested in **10,000 seeded crash-injecting simulated universes** per CI run ([what that caught →](sqrl/docs/dst.md))
- Typed non-determinism detection, snapshot compaction with no history cap, thread-per-core with group commit
- Honest semantics: at-least-once + stable idempotency keys — never a false exactly-once claim

**Start here → [`sqrl/README.md`](sqrl/README.md)** &middot; [architecture](sqrl/docs/architecture.md) &middot; [benchmarks with repro commands](sqrl/docs/benchmarks.md) &middot; [honest comparison vs Temporal/DBOS/Restate](sqrl/docs/comparison.md)

---

# Zenith Engine

[![CI](https://github.com/rohanreddy79/zenith-engine/actions/workflows/ci.yml/badge.svg)](https://github.com/rohanreddy79/zenith-engine/actions)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.11%20%7C%203.12%20%7C%203.13-blue)](https://www.python.org/)

**Zenith Engine** is a high-performance asynchronous runtime and distributed task execution framework designed for ultra-low-latency event processing, dynamic worker pooling, and fault-tolerant service orchestration.

## Key Features

- **Asynchronous Execution Engine**: Preemptive priority scheduling with lock-free ring buffer dispatch.
- **Two-Tier Storage & Caching**: Fast in-memory LRU cache with automatic TTL expiration and WAL compaction.
- **High-Throughput Networking**: Async connection pooling, TLS 1.3 session resumption, and zero-copy packet framing.
- **Enterprise Security**: Asymmetric JWT/OAuth2 verification with fine-grained RBAC evaluation.
- **Observability**: Built-in Prometheus latency percentiles and structured JSON telemetry.

## Quickstart

```python
import asyncio
from zenith.core.engine import AsyncEngine, EngineConfig

async def main():
    config = EngineConfig(max_workers=16, queue_capacity=5000)
    engine = AsyncEngine(config=config)
    await engine.start()
    
    result = await engine.submit(lambda: "Task completed successfully!")
    print(result)
    
    await engine.shutdown()

if __name__ == "__main__":
    asyncio.run(main())
```

## Architecture

```
+-------------------------------------------------------------+
|                        Zenith Engine                        |
+-------------------------------------------------------------+
|   Event Dispatcher   |   Priority Scheduler   | Worker Pool  |
+-------------------------------------------------------------+
|   LRU / WAL Cache    |   Async HTTP/TCP       | Telemetry    |
+-------------------------------------------------------------+
```

## License

MIT License. Copyright (c) Rohan Reddy Jakkam.
