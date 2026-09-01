"""
PROTOTYPE — portfolio, round 5.  THROWAWAY CODE. Do not promote as-is.

Settled in earlier rounds (see ../DECISION.md and the git log):
  round 1  LAYOUT    Workbench — sidebar catalogue, main pane runs the artifact
  round 2  LANGUAGE  Instrument — dense, monospace, hairline rules
  round 4  TONE      Slate, now the default

Round 5 turns the tone from a prototype variant into a real control: the viewer
picks it, alongside accessibility settings, from a panel in the sidebar's lower
left under Contact. theme.py holds the palettes and settings; page.py renders
the settled page and takes the panel as a callable.

So the only thing still under evaluation is the panel itself:

    Where do the options live, and how loud should they be?

  1 — Swatches  colour chips you pick by looking, plus toggle rows
  2 — List      one row idiom all the way down, an icon per option
  3 — Drawer    collapsed to a single line until opened

Run:  ./run          (or: uv run --with 'streamlit>=1.42' streamlit run app.py)
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import streamlit as st
import page
import switcher
from variants import p1_swatches, p2_list, p3_drawer

VARIANTS = {"1": p1_swatches, "2": p2_list, "3": p3_drawer}

st.set_page_config(page_title="Portfolio prototype", layout="wide",
                   initial_sidebar_state="expanded")

# Strip Streamlit chrome — it is not part of any design being evaluated.
#
# CAREFUL. Three traps here, all hit during this prototype:
#
#  1. Do NOT hide header[data-testid="stHeader"], and do NOT hide
#     [data-testid="stToolbar"]. The control that re-opens a collapsed sidebar
#     (stExpandSidebarButton) is rendered INSIDE that toolbar, inside that
#     header. Hiding either one strands the sidebar shut with no way back.
#  2. Streamlit persists the collapsed flag in localStorage under
#     "stSidebarCollapsed-<base>", and that read beats initial_sidebar_state —
#     so a sidebar collapsed once stays collapsed on every later reload. CSS
#     cannot fix that; proto_boot.html clears the flag on load.
#  3. Material icons are ligatures. Forcing font-family on a broad selector like
#     `.stApp span` overrides the icon font and the glyph renders as literal
#     text. The rule below re-asserts it at higher specificity.
st.markdown("""
<style>
  header[data-testid="stHeader"] { background: transparent !important; }
  [data-testid="stToolbar"] { background: transparent !important; }

  /* Hide toolbar CHILDREN, never the toolbar itself. */
  #MainMenu, [data-testid="stStatusWidget"], [data-testid="stDecoration"],
  [data-testid="stAppDeployButton"], [data-testid="stAppCreatorAvatar"],
  footer { display: none !important; }

  [data-testid="stExpandSidebarButton"],
  [data-testid="stSidebarCollapseButton"] {
    display: inline-flex !important; visibility: visible !important;
    opacity: 1 !important; pointer-events: auto !important;
  }

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
page.render(VARIANTS[active].panel)
switcher.render({k: m.NAME for k, m in VARIANTS.items()}, active)
