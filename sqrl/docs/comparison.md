# sqrl vs. the field — an honest comparison

sqrl's bet is narrow: **durable execution as an embedded library** — the way
SQLite bet on "database as a library". If you need what the server-based
systems provide, use them; this page is explicit about where sqrl loses.

|  | **sqrl** | **Temporal** | **Restate** | **DBOS Transact** | **Hatchet** |
|---|---|---|---|---|---|
| Deployment | `cargo add sqrl`, in-process | server cluster (+DB: Cassandra/MySQL/PG) | single server binary (own log store) | library + system DB (Postgres, or SQLite embedded) | server (+Postgres, RabbitMQ) |
| Runtime deps | **none** (local disk) | Temporal cluster | restate-server | Postgres (or embedded SQLite) | Postgres + broker |
| Languages | Rust only (v1) | Go/Java/TS/Python/.NET/PHP/Ruby | TS/Java/Kotlin/Python/Go/Rust | TS/Python/Go | Python/TS/Go |
| Distribution / HA | **none** — single node | multi-node, multi-region, HA | single-node (v1 replication evolving) | HA via the database | via Postgres |
| Horizontal worker scale-out | no | yes | yes | yes | yes |
| Multi-tenancy, RBAC, namespaces | no | yes | limited | partial (Conductor) | yes |
| Web UI / observability suite | no (CLI only) | full UI | UI | Conductor UI | UI |
| Determinism model | replay + typed `NonDeterminismError`, patch gates | replay + patching APIs | journaled promises | checkpointed steps | event-driven tasks |
| Deterministic simulation testing of the engine itself | **first-class** (seeded, byte-identical) | no public equivalent | internal testing | no | no |
| Durable timers / signals | yes | yes | yes | yes (sleep, events) | yes |
| Recovery granularity | last completed step | last completed event | last journal entry | last completed step | task retry |
| Guarantee | **at-least-once + idempotency keys** (documented; never "exactly-once") | same, marketed variously | same | same | at-least-once |
| Latency floor | in-process fn call + local fsync | network RTT × several + DB writes | network RTT + disk | DB round trips | queue round trips |
| Offline / edge | **yes** — single binary, works with no network | no | no | with SQLite, partially | no |
| Journal length | unbounded (snapshot compaction) | capped history (continue-as-new) | bounded per invocation | table growth | n/a |
| Maturity | **new; pre-1.0** | battle-tested, years in prod | production, funded team | production, funded team | production |

## Where sqrl loses, stated plainly

* **No distribution.** One node. If the machine dies and its disk is gone,
  the workflows are gone (optional shared-Postgres backend is future work,
  and even then: one *process group*, not a cluster).
* **No polyglot SDKs.** Rust or nothing in v1 (the core is FFI-able by
  design, but nothing is built).
* **No multi-tenant primitives.** No namespaces, RBAC, per-tenant quotas,
  schedules-as-a-service, or a web dashboard. A CLI inspector is all the
  tooling there is.
* **No worker fleets.** Steps run in *your* process's step pool. You cannot
  add machines to drain a backlog.
* **Young.** The systems above have years of production scar tissue. sqrl
  has a DST suite and a fuzzer.

## Where sqrl wins

* **Zero operational surface.** No server, no database, no docker-compose.
  The failure domain is your process and one directory of checksummed files.
* **Latency.** A step commit is a function call plus a local (group)
  fsync — not a network round trip to an orchestrator.
* **Edge/offline.** Workflows keep executing with no network at all.
* **Testability.** The same engine bytes run under seeded simulation;
  crash-at-every-disk-op is a test you can actually write (we did).
* **Rust-native ergonomics.** Workflows are async fns; no separate worker
  topology, task queues, or YAML.

If you outgrow sqrl — you need HA, fleets, tenants, dashboards — Temporal or
Restate is the right move, and sqrl's journal is small and readable enough
to migrate away from. That is a feature.
