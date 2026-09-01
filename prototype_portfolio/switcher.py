"""
PROTOTYPE — the floating variant switcher.

Deliberately styled to look like debug chrome, not part of any design being
evaluated. Hidden when PROTOTYPE_SWITCHER=0, so a stray deploy can't ship it.
"""
import os
from pathlib import Path

import streamlit as st

SHOW = os.environ.get("PROTOTYPE_SWITCHER", "1") != "0"

_CSS = """
<style>
.st-key-proto_switcher {
  position: fixed; bottom: 20px; left: 50%; transform: translateX(-50%);
  z-index: 999999; width: auto !important;
  background: #101317; border: 1px solid #3a4048; border-radius: 999px;
  padding: 6px 8px; box-shadow: 0 10px 34px rgba(0,0,0,.5);
}
.st-key-proto_switcher [data-testid="stHorizontalBlock"] { gap: 2px; align-items: center; }
.st-key-proto_switcher .stButton > button {
  background: transparent; color: #d6dbe1; border: none; border-radius: 999px;
  padding: 2px 12px; font-size: 17px; line-height: 1.4; min-height: 0;
}
.st-key-proto_switcher .stButton > button:hover { background: #262c33; color: #fff; }
.st-key-proto_switcher p {
  color: #d6dbe1 !important; font-size: 12px !important; margin: 0 !important;
  white-space: nowrap; letter-spacing: .04em;
  font-family: ui-monospace, SFMono-Regular, Menlo, monospace !important;
  text-align: center; padding: 0 6px;
}
.st-key-proto_switcher p .k { color: #6e7681; }
</style>
"""



def current(variants, default=None):
    """Read the active variant key from ?variant=, falling back to the first."""
    keys = list(variants)
    v = st.query_params.get("variant", default or keys[0])
    if isinstance(v, list):
        v = v[0]
    v = (v or "").upper()
    return v if v in keys else keys[0]


def _go(key):
    st.query_params["variant"] = key
    st.rerun()


def render(variants, active):
    """variants: dict of {key: label}. Draws the fixed bottom bar."""
    if not SHOW:
        return
    st.markdown(_CSS, unsafe_allow_html=True)
    keys = list(variants)
    i = keys.index(active)

    with st.container(key="proto_switcher"):
        left, mid, right = st.columns([1, 7, 1], vertical_alignment="center")
        with left:
            if st.button("‹", key="proto_prev", help="Previous variant (←)"):
                _go(keys[(i - 1) % len(keys)])
        with mid:
            st.markdown(
                f'<p><b>{active}</b> — {variants[active]}'
                f'<span class="k">   ·   {i + 1}/{len(keys)}   ·   ← →</span></p>',
                unsafe_allow_html=True,
            )
        with right:
            if st.button("›", key="proto_next", help="Next variant (→)"):
                _go(keys[(i + 1) % len(keys)])

    st.iframe(Path(__file__).parent / "switcher_keys.html", height=1)
