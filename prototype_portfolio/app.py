"""
PROTOTYPE — portfolio UI variants, round 2.  THROWAWAY CODE. Do not promote as-is.

Round 1 asked what the site's STRUCTURE should be, and answered it: variant B,
"Workbench" — a sidebar cataloguing every artifact, a main pane that runs the
selected one full size. See DECISION.md. That is settled and no longer varies.

Round 2 asks the remaining question:

    The layout is right. What should it LOOK like?

Three treatments of the identical skeleton (variants/shell.py holds the running
order, so the comparison is honest). Switch with ?variant= or the bottom bar:

  1 — Instrument  dark, dense, monospace; colour only where it carries signal
  2 — Editorial   light, warm, serif display; whitespace instead of borders
  3 — Console     high contrast, hard edges, one loud accent

Run:  ./run          (or: uv run --with 'streamlit>=1.42' streamlit run app.py)
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import streamlit as st
import switcher
from variants import v1_instrument, v2_editorial, v3_console

VARIANTS = {"1": v1_instrument, "2": v2_editorial, "3": v3_console}

st.set_page_config(page_title="Portfolio prototype", layout="wide",
                   initial_sidebar_state="expanded")

# Strip Streamlit chrome — it is not part of any design being evaluated.
st.markdown("""
<style>
  header[data-testid="stHeader"], #MainMenu, footer { display:none !important; }
  [data-testid="stAppViewBlockContainer"], .block-container {
    padding-top: 2.4rem !important; padding-bottom: 1rem !important; }
</style>
""", unsafe_allow_html=True)

active = switcher.current(VARIANTS)
VARIANTS[active].render()
switcher.render({k: m.NAME for k, m in VARIANTS.items()}, active)
