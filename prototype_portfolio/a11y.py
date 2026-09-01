"""
Screen-reader layer.

Streamlit gives a button its accessible name from its visible label, so an
icon-only button has none at all — a screen reader announces "button" and
nothing else. That is exactly the control an accessibility panel must not get
wrong, and there is no Python-side API for aria-*.

So Python publishes a label map into a hidden element and proto_boot.html copies
it onto the real controls, re-applying on every rerun via a MutationObserver.
Same mechanism supplies iframe titles and image alt text.

Everything here is additive: if the script never runs, the page still works —
it is just less well described.
"""
import html
import json

import streamlit as st
from content import ARTIFACTS, KIND_LABEL
import theme


def _labels(s, drawer_open):
    """key (a Streamlit widget key) -> accessible name."""
    lab = {
        "drawer_toggle": ("Hide appearance options" if drawer_open
                          else "Show appearance options"),
        "size_dec": f"Decrease text size. Currently {theme.text_pct(s['text_idx'])}",
        "size_inc": f"Increase text size. Currently {theme.text_pct(s['text_idx'])}",
        "opt_reset": "Reset all appearance options to defaults",
        "tg_motion": "Reduce motion. Stops the live demos animating",
        "tg_contrast": "High contrast. Stronger text and borders",
        "tg_readable": "Readable font. A wider sans face instead of monospace",
        "tg_underline": "Underline links, so links are not signalled by colour alone",
    }
    for k, p in theme.PALETTES.items():
        lab[f"tone_{k}"] = f'{p["label"]} mode. {p["hint"]}'
    # The ● / ○ prefix on a nav item is decorative — it would be announced as a
    # bullet character. Say what it actually means.
    for a in ARTIFACTS:
        runs = "Runs live in the page. " if a.get("embed") else ""
        lab[f"nav_{a['id']}"] = (f'{a["name"]}. {KIND_LABEL[a["kind"]]}, {a["year"]}. '
                                 f'{runs}{a["one_liner"]}')
    return lab


def _pressed(s):
    """key -> aria-pressed / aria-checked state for the toggles and the modes."""
    pr = {
        "tg_contrast": s["contrast"],
        "tg_readable": s["readable"],
        "tg_underline": s["underline"],
        "tg_motion": not s["motion"],
        "drawer_toggle": None,          # expanded, handled separately
    }
    for k in theme.PALETTES:
        pr[f"tone_{k}"] = s["tone"] == k
    return {k: v for k, v in pr.items() if v is not None}


def emit(s, drawer_open=False):
    """Publish the map, and announce the current settings politely."""
    payload = {
        "labels": _labels(s, drawer_open),
        "pressed": _pressed(s),
        "expanded": {"drawer_toggle": drawer_open},
        # Modes are one choice, not three independent switches.
        "radiogroup": ["tone_" + k for k in theme.PALETTES],
        "current": {f"nav_{st.session_state.get('wb_sel')}": True},
        "demoTitle": "Live demo, running in the page",
        "imageAlt": "Placeholder screenshot standing in for a real one",
    }
    data = html.escape(json.dumps(payload), quote=True)
    st.markdown(
        f'<div id="proto-a11y-data" data-a11y="{data}" hidden></div>'
        f'<div id="proto-status" class="sr-only" role="status" aria-live="polite">'
        f'{html.escape(theme.summary(s))}</div>',
        unsafe_allow_html=True,
    )
