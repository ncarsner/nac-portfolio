# PROTOTYPE — portfolio UI variants

**Throwaway code.** No tests, no error handling, no abstractions worth keeping.
Written to answer a question, then to be deleted.

## Round 1 — settled

> What should the site's **structure** be?

**Answer: the "Workbench" layout.** A sidebar cataloguing every artifact; a main
pane that runs the selected one full size. Prose is the fallback for things that
cannot run, not the default presentation. Reasoning and the two rejected
structures are in [`../DECISION.md`](../DECISION.md); the losing variants are on
`main`'s history at commit `faa0a8a`, recoverable with:

```
git show faa0a8a:prototype_portfolio/variants/variant_a.py
```

## Round 2 — settled

> The layout is right. What should it **look like**?

**Answer: "Instrument"** — dense, monospace, hairline rules, no decoration,
colour only where it carries signal. The rejected treatments (Editorial, Console)
are in history at `ce5b8ba`.

## Round 3 — overshot

Read "but lighter" as near-white. Verdict: **too light.** Kept in history at
`0870c92`.

## Round 4 — settled

**Slate** `#1c2128` — the minimal lift off near-black. Now the default.

## Round 5 — settled

**Drawer.** Collapsed to a single "Appearance" line with a summary of what is
active, so the sidebar belongs to the work until someone wants the controls. The
rejected panels (Swatches, List) are in history at `0727b25`.

## Round 6-7 — refinements

Nothing is being compared any more, so the prototype's variant bar is gone.

### The sidebar, bottom to top

- **Mode** and **Text size** are **always visible** — the two controls people
  actually reach for.
- **Appearance Options** (collapsed) holds what is set once and forgotten: the
  colour base and the accessibility toggles.

### Two palette axes, generated not hardcoded

| Axis | Values |
|------|--------|
| **Mode** | dark (default), mid, light — icons only: moon, half-disc, sun |
| **Colour base** | blue (default), green, silver, gold, magenta |

That is fifteen combinations, so the palette is **generated**. Each mode is a
ramp of (saturation, lightness) targets per token; each base supplies a hue and a
saturation multiplier — silver is simply a base whose multiplier is near zero.
Every combination is therefore internally consistent: picking a new base can
never produce a page whose borders and text stop relating to its background.
See `MODE_SPEC` / `BASES` in `theme.py`; changing the whole look is a table edit.

The base selector is a connected strip of five chips, each painted with the
accent **that base actually yields in the current mode** — so in light mode the
chips are dark, because that is what you will get.

### Text size

Ten-point steps rather than fifteen, and more of them:
**80 / 90 / 100 / 110 / 120 / 130 / 140 / 150%**, default 100%.

`100%` is what used to be `90%` — the old default read too large at this density,
so the whole scale was rebased (`TEXT_BASE = 0.90`) rather than just relabelled.
The ends disable rather than wrap.

The middle cell is both the readout and the reset: it shows the current size and
returns to 100% when selected. The `+`/`-` steps are relative to that, so the
number and the control that restores it are one object rather than two. Its
accessible name and tooltip change when it is already at the default — there is
no point offering a reset to the value you are on.

### Contact row

GitHub, email, LinkedIn and resume as inline 24x24 SVG using `currentColor`, so
they follow the palette and scale with the text-size setting. GitHub and LinkedIn
are the official brand marks; email is an envelope and resume is a document.

The four tiles are `flex:1`, so they distribute evenly across the full sidebar
width with equal margins at either end, at every text size. Their element
container carries a `min-height` — without it the next section's `border-top` is
drawn straight across the icons (trap 6 below, in a second costume).

### Daily quote

The headline under the name rotates through five widely published quotations
(placeholders — swap them for lines that are actually yours). It changes **once a
day, not once a reload**: the index is seeded from the ordinal date, so there is
no storage, no cookie, no session state, and every visitor sees the same line on
the same day. That is what makes it read as a publication rather than a slot
machine.

### Settings

| Setting | Default | Effect |
|---------|---------|--------|
| Mode | **dark** | dark / mid / light |
| Colour base | **blue** | blue / green / silver / gold / magenta |
| Text size | **100%** | eight steps, 80-150% |
| Reduce motion | **on** | stops the live demos animating |
| High contrast | off | pushes text to the extremes, rules to 2px |
| Readable font | off | wider sans instead of monospace |
| Underline links | off | do not signal links by colour alone |

**Reduced motion is on by default; high contrast is not.** Motion is the one
where the default costs nothing — a still page reads the same to everyone, so
there is no reason to make anyone opt out of it. High contrast genuinely changes
the look the design settled on over four rounds, so it stays opt-in.

Note `motion` is stored as *"motion is allowed"*, so reduced motion is
`motion=False`. Worth knowing before reading `DEFAULTS`.

State lives in `st.session_state`: in memory, never persisted.

## Accessibility notes

Streamlit derives a button's accessible name from its visible label, so an
icon-only button has **no accessible name at all** — a screen reader announces
"button" and nothing else. There is no Python-side aria-* API. So `a11y.py`
publishes a label map into a hidden element and `proto_boot.html` copies it onto
the real controls, re-applying after every rerun via a `MutationObserver`.

- Every icon-only control has an `aria-label` including its current value
  ("Increase text size. Currently 100%").
- Mode and colour base are each a `radiogroup` with `aria-checked`, so they
  announce as one choice rather than N unrelated switches.
- Toggles carry `aria-pressed`; the disclosure carries `aria-expanded`.
- Icon spans are `aria-hidden`, so ligature names are never announced.
- Contact links are icon-only and carry `aria-label` + `title`; their SVGs are
  `aria-hidden` and `focusable="false"`.
- Nav items get a real description instead of the decorative `●`/`○`, and the
  selected one carries `aria-current`.
- The live demo iframe gets a title; the helper iframe is `aria-hidden` and out
  of the tab order.
- A visually hidden `role="status"` region announces the settings summary
  whenever anything changes.

All additive: if the script never runs the page still works, it is just less well
described.

**Not done:** verified by inspecting the accessibility tree in the DOM, not by
driving a real screen reader. Keyboard focus order and contrast ratios across all
fifteen mode x base combinations have not been audited — with silver and gold in
light mode being the obvious risks. Both are worth doing before this ships.

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
theme.py            the palette generator + settings + the whole stylesheet
page.py             the settled page
panel.py            always-visible mode/size + the Appearance Options disclosure
quotes.py           the daily headline, seeded from the date
icons.py            inline SVG for the contact row
a11y.py             accessible names, published for proto_boot.html to apply
proto_boot.html     sidebar repair + the accessible-name pass, iframed at height 1
content.py          FAKE placeholder data — all in memory, nothing persisted
embeds.py           iframes the live demos + SVG screenshot placeholders
demos/build.py      builds each demo per mode, animated and still
```

## Streamlit chrome traps, recorded so they are not repeated

Nine now, across seven rounds. Each was found in a real browser with Playwright,
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
6. **The markdown wrapper does not grow with the inner div's padding**, so the
   content overflows its element container and the NEXT block is drawn on top of
   it. It bit the group headers first and the contact row later — where it showed
   up as a rule sliced through the icons. Every such container carries an
   explicit `min-height`.
7. **A button wrapper is shrink-to-fit**, so `width:100%` on the button resolves
   against the icon's own width.
8. **`section[data-testid="stSidebar"] .stButton button` outranks a bare
   `.st-key-<key> button`**, so per-control overrides need the sidebar prefix or
   they silently do nothing. Same family as trap 4, and just as quiet.
9. **CSS unicode escapes get mangled** on the way through the f-string that
   builds the stylesheet — `quotes:'\201C'` rendered as `·C`. Use literal
   characters in `content:`.

## Caveats, stated plainly

- **All content is invented**, quotes included. "Sam Rivera", every project,
  metric and link, and the five quotations are placeholders, present only so the
  layout is judged at realistic density.
- **The demos follow the mode, not the colour base.** Building them for all
  fifteen combinations would mean sixty files for little gain, and a genuinely
  third-party embedded app would keep its own branding anyway.
- **The demos are real but local.** Working zero-dependency apps, iframed. In the
  real site those iframes point at deployed apps instead.
- **Screenshots are SVG placeholders**, labelled as such.
- **Settings do not persist.** Reload and you are back to dark / blue / 100%.
  Persisting them is a real decision (cookie? localStorage? account?) and a
  prototype should not quietly assume one.
- **Streamlit is still on trial.** Nine traps in seven rounds, all the same
  shape: depending on internal class names and test ids with no compatibility
  guarantee. The accessibility layer is the sharpest case — it exists only
  because there is no supported way to set an aria attribute, and it would break
  the day Streamlit changes its DOM.
