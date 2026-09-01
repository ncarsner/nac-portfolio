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

## Round 2 — open

> The layout is right. What should it **look like**?

Three treatments of the identical skeleton. They differ in typography, density,
colour, and how the title block and metrics are handled — nothing else.

| Key | Name | The bet it makes |
|-----|------|------------------|
| `1` | **Instrument** — dark, dense, monospace | This is a control surface, not a brochure. Hairline rules, no decoration, colour only where it carries signal. Density itself is the credential. |
| `2` | **Editorial** — light, airy, serif display | The opposite bet. Large serif type, comfortable measures, whitespace doing the structural work instead of borders. Space, not density, signals seniority. |
| `3` | **Console** — high contrast, hard edges | Be memorable rather than tasteful. Thick rules, no rounding, two extreme type sizes, one loud accent. A portfolio's real failure mode is being forgotten. |

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
switcher.py         floating bottom bar
switcher_keys.html  arrow-key handler, iframed at height 1
content.py          FAKE placeholder data — all in memory, nothing persisted
embeds.py           iframes the live demos + SVG screenshot placeholders
demos/              real, working, dependency-free HTML apps
variants/shell.py   the settled skeleton — running order, shared by all three
variants/v1..v3     one visual language each: CSS + its own block renderers
```

`shell.py` exists because round 1 is decided: holding the running order fixed is
what makes round 2 an honest comparison. Everything visual still belongs to the
variant, so any of them can still throw out the entire look.

## Caveats, stated plainly

- **All content is invented.** "Sam Rivera" and every project, metric and link is
  placeholder, present only so the layouts are judged at realistic density.
- **The demos are real but local.** `demos/*.html` are working zero-dependency
  apps, iframed. In the real site those iframes point at deployed apps instead —
  the mechanic is identical, which is the part being tested.
- **Screenshots are SVG placeholders**, labelled as such.
- **Variants 2 and 3 pull webfonts from Google Fonts.** Offline they fall back to
  system serif / sans and will look noticeably flatter.
- **Streamlit is still on trial.** All three lean on CSS keyed to internal class
  names (`.st-key-*`, `[data-testid="stSidebar"]`). That works today and is
  exactly the kind of thing that breaks on upgrade.

## Reading the result

The useful answer is usually not "2". It is **"Editorial's type at Instrument's
density"** — say it that way and that is the design.
