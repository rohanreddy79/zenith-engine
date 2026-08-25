# Contributing to sqrl

Thanks for your interest! A few ground rules keep this durability-critical
codebase safe to change.

## Engineering standards

- Rust stable (pinned in `rust-toolchain.toml`), edition 2021. MSRV: **1.85**,
  checked in CI. MSRV bumps are minor-version changes.
- `#![forbid(unsafe_code)]` in every crate. No exceptions without an ADR.
- `#![deny(missing_docs)]` on public crates; every public item has a doc
  comment, ideally with a compiling doctest.
- Errors: `thiserror` library errors. No `unwrap()`/`expect()` outside tests
  and the CLI's top level.
- The orchestration path must not depend on Tokio. Tokio is allowed only in the
  step pool and `RealScheduler`, behind clear boundaries.
- No ambient entropy in engine code: no `SystemTime::now()`, `Instant::now()`,
  `rand`, `Uuid::new_v4()` outside the injected `Clock`/`Rng`. Enforced via
  clippy `disallowed-methods` (see `clippy.toml`); legitimate uses carry an
  `#[allow]` with a written justification.
- Every non-obvious design decision gets an ADR in `docs/adr/`
  (Context / Decision / Consequences).

## Workflow

1. Tests first or alongside; never merge with failing or skipped tests.
2. `cargo test --workspace && cargo clippy --workspace --all-targets -- -D warnings && cargo fmt --all --check && cargo doc --no-deps` must pass.
3. Conventional commits: `feat:`, `fix:`, `test:`, `docs:`, `bench:`, `chore:`.
   One logical change per commit.

## SemVer policy

- Crate API follows Cargo SemVer. Pre-1.0: breaking API changes bump the minor
  version.
- The **on-disk format is versioned independently** (`SQRL_FORMAT_VERSION`,
  documented in `docs/on-disk-format.md`). Any format change requires a format
  version bump and a documented migration path; before any 1.0 release a
  migration tool is required.
- Durability guarantees are part of the public API: weakening any documented
  guarantee is a breaking change regardless of code compatibility.

## Releasing

Releases use `cargo-release` (config in `release.toml`). `CHANGELOG.md` follows
Keep-a-Changelog. Every publishable crate must pass `cargo publish --dry-run`.
