//! PostgreSQL storage backend for `sqrl`.
//!
//! Implements the same [`sqrl_core::Storage`] contract as the embedded WAL
//! and the SQLite backend, on a shared PostgreSQL database: journal rows +
//! latest-snapshot rows per workflow, with `append` buffering in memory and
//! `sync` committing one transaction (PostgreSQL's `synchronous_commit=on`
//! makes a commit the fsync barrier the contract requires).
//!
//! **Verification status**: this environment has no PostgreSQL server or
//! docker, so the backend's integration tests are gated behind the
//! `SQRL_POSTGRES_URL` environment variable and are otherwise skipped —
//! the backend is marked UNVERIFIED in `docs/PLAN.md` until run against a
//! real server:
//!
//! ```bash
//! docker run --rm -e POSTGRES_PASSWORD=pw -p 5432:5432 postgres:16
//! SQRL_POSTGRES_URL=postgres://postgres:pw@localhost:5432/postgres \
//!     cargo test -p sqrl-store-postgres
//! ```
#![forbid(unsafe_code)]
#![deny(missing_docs)]
