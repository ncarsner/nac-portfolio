"""
PROTOTYPE — portfolio UI variants, round 2.  THROWAWAY CODE. Do not promote as-is.

Round 1 asked what the site's STRUCTURE should be, and answered it: variant B,
"Workbench" — a sidebar cataloguing every artifact, a main pane that runs the
selected one full size. See DECISION.md. That is settled and no longer varies.

Round 2 chose the visual language: "Instrument" — dense, monospace, hairline
rules, no decoration. The note on it was "but lighter", which has two readings,
so round 3 builds both and a middle option:

    Instrument is right. What does "lighter" mean?

Three treatments of the identical skeleton (variants/shell.py holds the running
order, so the comparison is honest). Switch with ?variant= or the bottom bar:

  1 — Instrument Light  lighter in COLOUR: same density, near-white ground
  2 — Instrument Airy   lighter in WEIGHT: open rhythm, larger type, few rules
  3 — Instrument Slate  same as 1 but on warm paper, rust signal colour

Run:  ./run          (or: uv run --with 'streamlit>=1.42' streamlit run app.py)
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import streamlit as st
import switcher
from variants import v1_light, v2_airy, v3_slate

VARIANTS = {"1": v1_light, "2": v2_airy, "3": v3_slate}

st.set_page_config(page_title="Portfolio prototype", layout="wide",
                   initial_sidebar_state="expanded")

# Strip Streamlit chrome — it is not part of any design being evaluated.
#
# NOTE: do NOT hide header[data-testid="stHeader"] wholesale. The control that
# re-opens a collapsed sidebar lives inside that header, so hiding it strands the
# sidebar shut with no way back (it also auto-collapses on a narrow window).
# Hide the toolbar contents instead and leave the header itself present but
# transparent and click-through.
st.markdown("""
<style>
  header[data-testid="stHeader"] {
    background: transparent !important; height: auto !important;
    pointer-events: none;
  }
  header[data-testid="stHeader"] * { pointer-events: auto; }
  [data-testid="stToolbar"], [data-testid="stAppToolbar"], [data-testid="stDecoration"],
  [data-testid="stStatusWidget"], #MainMenu, footer { display: none !important; }

  /* Keep both sidebar controls reachable and visible. */
  [data-testid="stSidebarCollapseButton"],
  [data-testid="stSidebarCollapsedControl"],
  [data-testid="stExpandSidebarButton"] {
    display: flex !important; visibility: visible !important; opacity: 1 !important;
  }

  [data-testid="stAppViewBlockContainer"], .block-container {
    padding-top: 2.4rem !important; padding-bottom: 1rem !important; }
</style>
""", unsafe_allow_html=True)

active = switcher.current(VARIANTS)
VARIANTS[active].render()
switcher.render({k: m.NAME for k, m in VARIANTS.items()}, active)
