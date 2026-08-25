# Launch collateral

Working material for the public launch. Nothing in this directory ships in
any crate; it exists so launch claims stay in the same repository as the
evidence behind them — the house rule (`docs/benchmarks.md`) applies to
marketing too: **no number without a reproduction command.**

| File | What it is |
|---|---|
| `demo.tape` | VHS script that renders the README hero GIF from a real `crash_me` run |
| `show-hn.md` | Show HN submission title + the author's first comment, ready to adapt |
| `dst-blog-post.md` | Section-by-section skeleton of the launch blog post about the DST suite and the two bugs it caught |
| `launch-checklist.md` | Pre-flight gates that must be green before anything above is posted |

## Recording the demo GIF

With [vhs](https://github.com/charmbracelet/vhs):

```bash
vhs docs/marketing/demo.tape        # writes docs/assets/demo.gif
```

Fallback with asciinema + [agg](https://github.com/asciinema/agg):

```bash
cargo build --release -p crash_me
asciinema rec demo.cast -c "cargo run --release -p crash_me"
agg demo.cast docs/assets/demo.gif --font-size 15 --speed 1.25
```

Then replace the text block in the README's "See it survive" section with
the image, keeping the text output beneath it in a `<details>` fold for
accessibility.
