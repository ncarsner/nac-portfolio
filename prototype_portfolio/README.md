# PROTOTYPE — portfolio UI variants

**Throwaway code.** No tests, no error handling, no abstractions worth keeping.
Written to answer one question, then to be deleted.

## The question

> What should a software engineer's personal portfolio look like, when the site
> has to host **already-built things** — apps, packages, sites — alongside static
> text and images?

Three variants of the *whole site*, switchable via `?variant=` and the floating
bottom bar. They disagree about structure, not colour.

| Key | Name | The bet it makes |
|-----|------|------------------|
| `A` | **Index** — dense text-first listing | Your reader is a peer who already knows what they want. One column, no hero, whole inventory on one screen. Demos are one click deep, never in the way. |
| `B` | **Workbench** — two-pane live artifact viewer | The portfolio *is* an app. Sidebar catalogs everything; the main pane runs the selected artifact full size. Prose is the fallback, not the default. |
| `C` | **Dispatch** — narrative long-scroll | What distinguishes one engineer from another is reasoning. The page is an essay, newest first, with artifacts inline as evidence — always visible, never behind a click. |

## Run

```
./run
```

One command. `uv` pulls Streamlit into a throwaway env — nothing is installed
into your system Python and there is no venv to clean up.

Then: <http://localhost:8501/?variant=A> — or use the bottom bar (`←` / `→` also
cycle, when the browser lets the iframe reach the parent document).

Set `PROTOTYPE_SWITCHER=0` to hide the bar.

## Layout

```
app.py              entry — chrome reset, variant dispatch
switcher.py         floating bottom bar (shared by all variants)
switcher_keys.html  arrow-key handler, iframed at height 1
content.py          FAKE placeholder data — all in memory, nothing persisted
embeds.py           iframes the live demos + SVG screenshot placeholders
demos/              real, working, dependency-free HTML apps
variants/           variant_a.py / variant_b.py / variant_c.py
```

Each variant owns its **entire** CSS and layout. Nothing is shared but the data
and the demo files — deliberately, so any variant can throw out the whole shape.

## Caveats, stated plainly

- **All content is invented.** "Sam Rivera" and every project, metric and link is
  placeholder, present only so the layouts are judged at realistic density.
- **The demos are real but local.** `demos/*.html` are working zero-dependency
  apps, iframed. In the real site those iframes point at deployed apps instead —
  the mechanic is identical, which is the part being tested.
- **Screenshots are SVG placeholders**, labelled as such.
- **Nothing mutates anything.** Read-only by design.
- **Streamlit is on trial here too.** These variants push it past its comfort
  zone (fixed positioning, custom typography, chrome removal) via CSS that keys
  off internal class names like `.st-key-*`. That works today and is exactly the
  kind of thing that breaks on upgrade — worth weighing when you pick.

## Reading the result

The useful answer is usually not "B". It is **"the sidebar from B with the prose
from C"** — that combination is the design you actually want. Say it that way.

Once a variant wins: fold it into real code (rewritten properly — this was
written under prototype constraints), and move this whole directory onto a
throwaway branch rather than into main.
