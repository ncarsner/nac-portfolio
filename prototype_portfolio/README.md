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

## Round 3 — open

> Instrument is right. What does **"lighter"** mean?

The note on Instrument was "but lighter", which has two honest readings — lighter
in *colour* or lighter in *weight*. Rather than guess, all three are built. The
skeleton and the block order are identical across them.

| Key | Name | What it changes |
|-----|------|-----------------|
| `1` | **Instrument Light** | Lighter in **colour**. Same density as the dark original, moved onto a near-white ground. Isolates exactly the one variable asked about. |
| `2` | **Instrument Airy** | Lighter in **weight**. Vertical rhythm opened up ~50%, type a notch larger, weights dropped, most hairline rules removed so space separates instead. |
| `3` | **Instrument Slate** | Variant 1's exact density on **warm paper** with a rust signal colour — for when pure white reads harsh on a text-dense page. |

The embedded demos ship light builds too (`demos/*_light.html`), so a running
artifact matches the page instead of punching a dark hole in a light design.

## Run

```
./run
```

One command. `uv` pulls Streamlit into a throwaway env — nothing is installed
into your system Python and there is no venv to clean up.

Then <http://localhost:8501/?variant=1>, or use the bottom bar (`←` / `→` also
cycle, when the browser lets the iframe reach the parent document). Set
`PROTOTYPE_SWITCHER=0` to hide the bar.

## Layout

```
app.py              entry — chrome reset, variant dispatch
.streamlit/         base theme pinned light, so variant CSS is not fighting
                    the viewer's OS dark-mode preference
switcher.py         floating bottom bar
switcher_keys.html  arrow-key handler, iframed at height 1
content.py          FAKE placeholder data — all in memory, nothing persisted
embeds.py           iframes the live demos + SVG screenshot placeholders
demos/              real, working, dependency-free HTML apps, light + dark builds
variants/shell.py   the settled skeleton — running order, shared by all three
variants/v1..v3     one visual treatment each: CSS + its own block renderers
```

`shell.py` exists because rounds 1 and 2 are decided: holding the running order
fixed is what makes each new round an honest comparison.

## Chrome gotcha, recorded so it is not repeated

`header[data-testid="stHeader"]` must **not** be hidden wholesale. The control
that re-opens a collapsed sidebar lives inside it, so hiding the header strands
the sidebar shut with no way back — and Streamlit auto-collapses the sidebar on a
narrow window. Hide the toolbar contents instead and leave the header present but
transparent and click-through. See the comment in `app.py`.

## Caveats, stated plainly

- **All content is invented.** "Sam Rivera" and every project, metric and link is
  placeholder, present only so the layouts are judged at realistic density.
- **The demos are real but local.** `demos/*.html` are working zero-dependency
  apps, iframed. In the real site those iframes point at deployed apps instead —
  the mechanic is identical, which is the part being tested.
- **Screenshots are SVG placeholders**, labelled as such.
- **Streamlit is still on trial.** All three lean on CSS keyed to internal class
  names (`.st-key-*`, `[data-testid="stSidebar"]`). That works today and is
  exactly the kind of thing that breaks on upgrade.

## Reading the result

The useful answer is usually not "1". It is **"1's density with 2's spacing on
3's paper"** — say it that way and that is the design.
