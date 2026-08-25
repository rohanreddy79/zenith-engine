# Show HN draft

Submit the repository URL (not a text post) with the title below, then
immediately post the author comment. Personalize the first-person voice
before posting — this is the maintainer speaking, and HN reads generic
copy as spam.

## Title (76 chars)

> Show HN: Sqrl – durable execution embedded in your Rust process, no server

## Author's first comment

> Hi HN — I built sqrl because I wanted Temporal-style durable execution
> (workflows that survive crashes and resume from their last completed
> step) without running a Temporal-style cluster. sqrl is a Rust library:
> you write plain async fns, every step result / timer / signal is
> journaled to a checksummed WAL in a local directory, and after kill -9
> the journal replays — completed steps return from history instead of
> re-executing. Like SQLite, the "deployment" is a directory.
>
> The part I'm proudest of is the testing. The production engine is a
> sans-io state machine, so the exact same code runs under a deterministic
> simulator: seeded scheduler, virtual clock, and a simulated disk that is
> meaner than any real one (unsynced writes independently kept, dropped,
> or torn on crash; deletes that resurrect; byte flips). The CI suite runs
> 10,000 seeded multi-crash universes in ~90s, and at every completion
> acknowledgment it forks a copy of the disk containing only the durably
> written bytes and re-runs recovery against it — "if power died at this
> exact instant, is the thing we just promised still there?" That oracle
> caught two real data-loss bugs before release (a recovery path that
> trusted the page cache, and a torn-tail bug where garbage from one crash
> poisoned the *next* recovery). Both are written up in docs/dst.md.
>
> Honest limitations: single node only (the scaling story is SQLite's:
> many independent stores). Steps are at-least-once — the ctx gives you
> stable idempotency keys, but I will never claim exactly-once side
> effects. Group commit trades ~2ms of latency for 10x fewer fsyncs, and
> that tradeoff is configurable per step.
>
> Numbers (4 shared vCPUs, repro commands in docs/benchmarks.md): ~8k
> workflows/s under group commit, a 1M-step single workflow with no
> history cap, 26ms to re-dispatch 1,000 in-flight workflows after
> kill -9.
>
> Would love feedback on the API and on holes in the testing story —
> that's the part I most want to be wrong about early.

## Launch-day mechanics

- Post Tuesday–Thursday, 8–10am ET. Never ask anyone to upvote —
  voting-ring detection is real and unforgiving.
- Stay at the keyboard for six hours. Answer every technical question,
  concede every fair criticism, and thank whoever finds a bug: that
  thread becomes the best marketing asset of the launch.
- Same week: r/rust, a "new crates" PR to This Week in Rust, lobste.rs.
