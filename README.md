# Zenith Engine

[![CI](https://github.com/rohanreddy79/zenith-engine/actions/workflows/ci.yml/badge.svg)](https://github.com/rohanreddy79/zenith-engine/actions)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.11%20%7C%203.12%20%7C%203.13-blue)](https://www.python.org/)

**Zenith Engine** is a high-performance asynchronous runtime and distributed task execution framework designed for ultra-low-latency event processing, dynamic worker pooling, and fault-tolerant service orchestration.

---

## Key Features

- **Asynchronous Execution Engine**: Preemptive priority scheduling with lock-free ring buffer dispatch.
- **Two-Tier Storage & Caching**: Fast in-memory LRU cache with automatic TTL expiration and WAL compaction.
- **High-Throughput Networking**: Async connection pooling, TLS 1.3 session resumption, and zero-copy packet framing.
- **Enterprise Security**: Asymmetric JWT/OAuth2 verification with fine-grained RBAC evaluation.
- **Observability**: Built-in Prometheus latency percentiles and structured JSON telemetry.

---

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

---

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
