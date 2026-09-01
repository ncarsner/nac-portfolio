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

## Round 4 — settled

**Slate** `#1c2128` — the minimal lift off near-black. Now the default.

## Round 5 — open

> Where do the options live, and how loud should they be?

The tone is no longer a prototype variant. Fog and Ash were kept and the choice
handed to the viewer, together with accessibility settings, from a panel in the
sidebar's lower left under Contact. So the only thing still being compared is how
that panel presents itself.

| Key | Name | The bet it makes |
|-----|------|------------------|
| `1` | **Swatches** | Colour chips painted with the ground they select, picked by looking rather than reading, plus labelled toggle rows. |
| `2` | **List** | One row idiom all the way down the sidebar, an icon per option. Nothing new to learn, and it scales if more options land. |
| `3` | **Drawer** | Collapsed to a single "Appearance" line with a summary until opened. The sidebar belongs to the work, not to its own controls. |

### Settings, in all three

- **Ground tone** — Slate (default), Fog, Ash
- **Text size** — Normal, Large, Larger
- **High contrast** — stronger text and borders
- **Readable font** — wider sans instead of monospace
- **Underline links** — do not signal links by colour alone
- **Reduce motion** — stops the live demos animating

State lives in `st.session_state`: in memory, never persisted. Reduce motion is
built into the demos rather than applied as page CSS — an iframe is a separate
document, so the still version is a separate build.

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
app.py              entry — chrome reset, panel dispatch
theme.py            palettes + accessibility settings + the whole stylesheet
page.py             the settled page; takes the options panel as a callable
switcher.py         floating bottom bar (prototype only)
proto_boot.html     sidebar repair + arrow keys, iframed at height 1
content.py          FAKE placeholder data — all in memory, nothing persisted
embeds.py           iframes the live demos + SVG screenshot placeholders
demos/build.py      builds each demo per tone, animated and still
variants/p1..p3     one options-panel presentation each
```

## Streamlit chrome traps, recorded so they are not repeated

Five rounds, five traps. Each was found in a real browser with Playwright, not by
reasoning — three of them survived a fix that was written from a guess.

1. **Never hide `header[data-testid="stHeader"]` or `[data-testid="stToolbar"]`.**
   `stExpandSidebarButton` — the only way to reopen a collapsed sidebar — lives
   inside them. Hide the individual toolbar children instead.
2. **The sidebar-collapsed flag persists in `localStorage`** as
   `stSidebarCollapsed-<base>`, and that read **beats** `initial_sidebar_state`.
   A sidebar collapsed once stays collapsed on every later reload. No CSS can fix
   it; `proto_boot.html` clears the flag on load.
3. **Material icons are ligatures.** A broad `font-family` override (e.g. on
   `.stApp span`) renders them as literal text. `app.py` re-asserts the icon font
   at higher specificity.
4. **Streamlit's markdown CSS outranks a bare class selector**, so `.pr { font-size }`
   silently did nothing and the prose rendered at 16px instead of 12.5px. Every
   size that matters now says `!important`.
5. **A button with `help=` is wrapped in tooltip spans**, so `.stButton > button`
   skips it. Use `.stButton button`. This left the entire options panel unstyled
   while the nav beside it looked correct.
6. **Streamlit's markdown wrapper does not grow with the inner div's padding.**
   Headers overflow their own element container; the default 1rem block gap was
   hiding it, and tightening the gap exposed it. Those containers now carry an
   explicit `min-height`.

## Caveats, stated plainly

- **All content is invented.** "Sam Rivera" and every project, metric and link is
  placeholder, present only so the layouts are judged at realistic density.
- **The demos are real but local.** Working zero-dependency apps, iframed. In the
  real site those iframes point at deployed apps instead.
- **Screenshots are SVG placeholders**, labelled as such.
- **Settings do not persist.** Reload and you are back to Slate. Persisting them
  is a real decision (cookie? localStorage? account?) and a prototype should not
  quietly assume one.
- **Streamlit is still on trial.** Six traps in five rounds, all the same shape:
  depending on internal class names and test ids with no compatibility guarantee.
  Weigh that before promoting any of this.

## Reading the result

Pick a panel, or say what to graft — **"Drawer, but the swatches from 1 inside
it"** is directly actionable.
