# PROTOTYPE — portfolio UI variants

**Throwaway code.** No tests, no error handling, no abstractions worth keeping.
Written to answer a question, then to be deleted.

## Round 1 — settled

> What should the site's **structure** be?

**Answer: the "Workbench" layout.** A sidebar cataloguing every artifact; a main
pane that runs the selected one full size. Prose is the fallback for things that
cannot run, not the default presentation. Reasoning and the two rejected
structures are in [`../DECISION.md`](../DECISION.md); the losing variants are on
this branch at commit `1c8761e`, recoverable with:

```
git show 1c8761e:prototype_portfolio/variants/variant_a.py
```

## Round 2 — settled

> The layout is right. What should it **look like**?

**Answer: "Instrument"** — dense, monospace, hairline rules, no decoration,
colour only where it carries signal. The rejected treatments (Editorial, Console)
are in history at `dc71f07`.

## Round 3 — overshot

Read "but lighter" as near-white. Verdict: **too light.** Kept in history at
`bfcc34d`.

## Round 4 — open

> Instrument is right. **How far up from near-black?**

Rather than run to either end again, this brackets the middle of the range. The
original Instrument ground was `#0a0c0f`; round 3 was `#fcfcfd`. Density,
structure and block order are unchanged — the ground tone is the only variable.

| Key | Name | Ground | What it is |
|-----|------|--------|------------|
| `1` | **Slate** | `#1c2128` | The minimal lift off near-black. Still unmistakably a dark interface, just no longer a void. |
| `2` | **Fog** | `#2b323b` | The far end of "lighter" while still dark. Text contrast comes down to match, so the page reads soft and even rather than punchy. |
| `3` | **Ash** | `#dfe3e7` | The other reading — light, but with the white taken out. Grey paper and ink-grey text, light without the glare. |

The embedded demos are built once per tone by `demos/build.py`, so a running
artifact shares the page's ground instead of punching a hole in it. Edit the
`PALETTES` table there and re-run `python3 demos/build.py`.

## Run

```
./run
```

One command. `uv` pulls Streamlit into a throwaway env — nothing is installed
into your system Python and there is no venv to clean up.

Then <http://localhost:8501/?variant=1>, or use the bottom bar (`←` / `→` also
cycle). Set `PROTOTYPE_SWITCHER=0` to hide the bar.

## Layout

```
app.py              entry — chrome reset, variant dispatch
.streamlit/         base theme pinned, so variant CSS is not fighting the
                    viewer's OS dark-mode preference
switcher.py         floating bottom bar
proto_boot.html     sidebar repair + arrow keys, iframed at height 1
content.py          FAKE placeholder data — all in memory, nothing persisted
embeds.py           iframes the live demos + SVG screenshot placeholders
demos/build.py      builds each demo once per page tone
demos/*.html        generated — real, working, dependency-free apps
variants/shell.py   the settled skeleton — running order, shared by all three
variants/v1..v3     one ground tone each: CSS + its own block renderers
```

## Streamlit chrome traps, recorded so they are not repeated

All three were hit during this prototype and cost a round each. Verified fixed in
a real browser via Playwright, not by reasoning.

1. **Never hide `header[data-testid="stHeader"]` or `[data-testid="stToolbar"]`.**
   The control that re-opens a collapsed sidebar (`stExpandSidebarButton`) is
   rendered *inside* that toolbar, inside that header. Hiding either strands the
   sidebar shut with no way back. Hide the individual toolbar children instead.
2. **Streamlit persists the sidebar-collapsed flag in `localStorage`** under
   `stSidebarCollapsed-<base>`, and that read **beats** `initial_sidebar_state`.
   So a sidebar collapsed once stays collapsed on every later reload, forever.
   No CSS can fix it — `proto_boot.html` clears the flag on load.
3. **Material icons are ligatures.** Forcing `font-family` on a broad selector
   like `.stApp span` overrides the icon font and the glyph renders as literal
   text (`keyboard_double_arrow_left`). `app.py` re-asserts the icon font at
   higher specificity.

## Caveats, stated plainly

- **All content is invented.** "Sam Rivera" and every project, metric and link is
  placeholder, present only so the layouts are judged at realistic density.
- **The demos are real but local.** They are working zero-dependency apps,
  iframed. In the real site those iframes point at deployed apps instead — the
  mechanic is identical, which is the part being tested.
- **Screenshots are SVG placeholders**, labelled as such.
- **Code blocks are hand-rolled**, not `st.code`, precisely so the Streamlit base
  theme cannot leak into a variant's palette.
- **Streamlit is still on trial.** Everything above leans on CSS keyed to
  internal class names and test ids. It works today and is exactly the kind of
  thing that breaks on upgrade — three separate traps in four rounds is data.

## Reading the result

If none is right, the answer is likely a number plus a nudge — **"Slate but two
steps lighter"** is directly actionable.
