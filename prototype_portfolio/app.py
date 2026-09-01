"""
PROTOTYPE — portfolio UI variants, round 2.  THROWAWAY CODE. Do not promote as-is.

Round 1 asked what the site's STRUCTURE should be, and answered it: variant B,
"Workbench" — a sidebar cataloguing every artifact, a main pane that runs the
selected one full size. See DECISION.md. That is settled and no longer varies.

Round 2 chose the visual language: "Instrument" — dense, monospace, hairline
rules, no decoration. Round 3 read "but lighter" as near-white and overshot: the
verdict was "too light". Round 4 therefore brackets the MIDDLE of that range
rather than running to either end:

    Instrument is right. How far up from near-black?

Three ground tones on the identical skeleton (variants/shell.py holds the running
order). Density and structure are unchanged from the original Instrument — the
ground tone is the only variable. Switch with ?variant= or the bottom bar:

  1 — Slate  soft charcoal, the minimal lift off near-black
  2 — Fog    mid slate, low contrast; the far end of "lighter" still dark
  3 — Ash    light grey paper, not white; light without the glare

Run:  ./run          (or: uv run --with 'streamlit>=1.42' streamlit run app.py)
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import streamlit as st
import switcher
from variants import v1_slate, v2_fog, v3_ash

VARIANTS = {"1": v1_slate, "2": v2_fog, "3": v3_ash}

st.set_page_config(page_title="Portfolio prototype", layout="wide",
                   initial_sidebar_state="expanded")

# Strip Streamlit chrome — it is not part of any design being evaluated.
#
# CAREFUL. Two traps here, both hit during this prototype:
#
#  1. Do NOT hide header[data-testid="stHeader"], and do NOT hide
#     [data-testid="stToolbar"]. The control that re-opens a collapsed sidebar
#     (stExpandSidebarButton) is rendered INSIDE that toolbar, inside that
#     header. Hiding either one strands the sidebar shut with no way back.
#     Hide the individual toolbar children instead.
#  2. Streamlit persists the collapsed flag in localStorage under
#     "stSidebarCollapsed-<base>", and that read beats initial_sidebar_state —
#     so a sidebar collapsed once stays collapsed on every later reload. CSS
#     cannot fix that; proto_boot.html clears the flag on load.
st.markdown("""
<style>
  header[data-testid="stHeader"] { background: transparent !important; }
  [data-testid="stToolbar"] { background: transparent !important; }

  /* Hide toolbar CHILDREN, never the toolbar itself. */
  #MainMenu, [data-testid="stStatusWidget"], [data-testid="stDecoration"],
  [data-testid="stAppDeployButton"], [data-testid="stAppCreatorAvatar"],
  footer { display: none !important; }

  /* Keep both sidebar controls reachable no matter what else is hidden. */
  [data-testid="stExpandSidebarButton"],
  [data-testid="stSidebarCollapseButton"] {
    display: inline-flex !important; visibility: visible !important;
    opacity: 1 !important; pointer-events: auto !important;
  }

  /* Material icon glyphs are ligatures. A variant that forces font-family on a
     broad selector like `.stApp span` overrides the icon font and the ligature
     renders as literal text ("keyboard_double_arrow_left"). Higher specificity
     than `.stApp span`, so it wins regardless of injection order. */
  .stApp [data-testid="stIconMaterial"], [data-testid="stIconMaterial"] {
    font-family: 'Material Symbols Rounded' !important;
    font-weight: 400 !important; letter-spacing: normal !important;
    font-feature-settings: 'liga' !important;
  }

  [data-testid="stAppViewBlockContainer"], .block-container {
    padding-top: 2.4rem !important; padding-bottom: 1rem !important; }
</style>
""", unsafe_allow_html=True)

active = switcher.current(VARIANTS)
VARIANTS[active].render()
switcher.render({k: m.NAME for k, m in VARIANTS.items()}, active)
