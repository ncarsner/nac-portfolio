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

## Round 5 — settled

**Drawer.** Collapsed to a single "Appearance" line with a summary of what is
active, so the sidebar belongs to the work until someone wants the controls. The
rejected panels (Swatches, List) are in history at `4fb9bc0`.

## Round 6 — refinements

Nothing is being compared any more, so the prototype's variant bar is gone.

- **Three modes, icons only.** A moon, a half-disc and a sun, joined into one
  segmented control. Dark / mid / light is legible without reading anything and
  the colour names were arbitrary; the names survive only as accessible names.
- **Word-style text sizing.** Minus, current size, plus, over five fixed steps
  (90 / 100 / 115 / 130 / 145%). The ends disable rather than wrap — wrapping
  from largest back to smallest would be a nasty surprise — and five steps is
  enough range to matter while keeping either end two clicks away.
- **Screen-reader text throughout.** See below.

### Settings

- **Mode** — dark (default), mid, light
- **Text size** — five steps, 90% to 145%
- **High contrast** — stronger text and borders
- **Readable font** — wider sans instead of monospace
- **Underline links** — do not signal links by colour alone
- **Reduce motion** — stops the live demos animating

State lives in `st.session_state`: in memory, never persisted. Reduce motion is
built into the demos rather than applied as page CSS — an iframe is a separate
document, so the still version is a separate build.

## Accessibility notes

Streamlit derives a button's accessible name from its visible label, so an
icon-only button has **no accessible name at all** — a screen reader announces
"button" and nothing else. There is no Python-side aria-* API. So `a11y.py`
publishes a label map into a hidden element and `proto_boot.html` copies it onto
the real controls, re-applying after every rerun via a `MutationObserver`.

What that buys:

- Every icon-only control has an `aria-label` that includes its current value
  ("Increase text size. Currently 100%").
- The three modes are a `radiogroup` with `aria-checked`, so they announce as one
  choice rather than three unrelated switches.
- Toggles carry `aria-pressed`; the drawer carries `aria-expanded`.
- Icon spans are `aria-hidden`, so the ligature name is never announced.
- Nav items get a real description instead of the decorative `●`/`○` bullet, and
  the selected one carries `aria-current`.
- The live demo iframe gets a title; the helper iframe is `aria-hidden` and
  removed from the tab order.
- A visually hidden `role="status"` region announces the settings summary
  whenever anything changes.

It is all additive: if the script never runs the page still works, it is just
less well described.

**Not done:** this has been verified by inspecting the accessibility tree in the
DOM, not by driving an actual screen reader. Keyboard focus order and contrast
ratios have not been audited either. Both are worth doing before this ships.

## Run

```
./run
```

One command. `uv` pulls Streamlit into a throwaway env — nothing is installed
into your system Python and there is no venv to clean up. Then
<http://localhost:8501>.

## Layout

```
app.py              entry — chrome reset
theme.py            palettes + settings + the whole stylesheet, derived per render
page.py             the settled page
panel.py            the options drawer
a11y.py             accessible names, published for proto_boot.html to apply
proto_boot.html     sidebar repair + the accessible-name pass, iframed at height 1
content.py          FAKE placeholder data — all in memory, nothing persisted
embeds.py           iframes the live demos + SVG screenshot placeholders
demos/build.py      builds each demo per mode, animated and still
```

## Streamlit chrome traps, recorded so they are not repeated

Seven now, across six rounds. Each was found in a real browser with Playwright,
not by reasoning — several survived a fix written from a guess.

1. **Never hide `header[data-testid="stHeader"]` or `[data-testid="stToolbar"]`.**
   `stExpandSidebarButton` — the only way to reopen a collapsed sidebar — lives
   inside them.
2. **The sidebar-collapsed flag persists in `localStorage`** as
   `stSidebarCollapsed-<base>` and **beats** `initial_sidebar_state`, so a
   sidebar collapsed once stays collapsed forever. No CSS can fix it.
3. **Material icons are ligatures.** A broad `font-family` override renders them
   as literal text.
4. **Streamlit's markdown CSS outranks a bare class selector**, so font sizes
   silently did nothing. Every size that matters says `!important`.
5. **A button with `help=` is wrapped in tooltip spans**, so `.stButton > button`
   skips it. Use `.stButton button`.
6. **The markdown wrapper does not grow with the inner div's padding**, so
   headers overflow their element container. Those containers carry a `min-height`.
7. **A button wrapper is shrink-to-fit**, so `width:100%` on the button resolves
   against the icon's own width. Widen every box in the chain.

## Caveats, stated plainly

- **All content is invented.** "Sam Rivera" and every project, metric and link is
  placeholder, present only so the layout is judged at realistic density.
- **The demos are real but local.** Working zero-dependency apps, iframed. In the
  real site those iframes point at deployed apps instead.
- **Screenshots are SVG placeholders**, labelled as such.
- **Settings do not persist.** Reload and you are back to dark at 100%.
  Persisting them is a real decision (cookie? localStorage? account?) and a
  prototype should not quietly assume one.
- **Streamlit is still on trial.** Seven traps in six rounds, all the same shape:
  depending on internal class names and test ids with no compatibility guarantee.
  The accessibility layer is the sharpest case — it exists only because there is
  no supported way to set an aria attribute, and it would break the day Streamlit
  changes its DOM.
