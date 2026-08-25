# Launch pre-flight

Gates that must be green before the README hero, Show HN post, or blog
post go public. The first commenter will try to falsify every claim
within the hour — clear these first. (The verification steps live in
`docs/PLAN.md`'s UNVERIFIED list and `docs/FINAL_REPORT.md`.)

- [ ] Run the comparison benchmarks for real
      (`bench-harness/comparisons/*.sh`; needs npm + docker) — or delete
      every comparative claim before launch. Never ship "UNVERIFIED"
      into a headline.
- [ ] Verify the Postgres backend against a real server (one docker
      command, in the crate docs).
- [ ] Let the fuzzers run overnight, not 60 seconds; refresh the numbers
      in `docs/dst.md`.
- [ ] Record `docs/assets/demo.gif` with `docs/marketing/demo.tape`;
      swap it into the README's "See it survive" section.
- [ ] Publish crates in dependency order (sqrl-core → sqrl-sim →
      sqrl-store → sqrl-macros → sqrl → backends → cli); confirm docs.rs
      renders for each.
- [ ] Claim a domain, make a logo (the squirrel burying an acorn *is*
      the product metaphor), set the GitHub social-preview image.
- [ ] Add `SECURITY.md` with a disclosure address; label 5–10
      `good first issue`s so launch-day visitors have a door in.
- [ ] Block out launch week: issue-triage speed in the first 72 hours is
      the strongest community signal there is.
