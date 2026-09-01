"""
PROTOTYPE — portfolio UI variants.  THROWAWAY CODE. Do not promote as-is.

Question this answers: what should a software engineer's personal portfolio look
like, when the site has to host already-built things (apps, packages, sites)
alongside static text and images?

Three variants of the whole site, switchable via ?variant= and the floating
bottom bar:
  A — Index      dense text-first listing, demos one click deep
  B — Workbench  two-pane app shell, the selected artifact runs full size
  C — Dispatch   long-form narrative scroll, artifacts inline as evidence

Run:  ./run          (or: uv run --with 'streamlit>=1.42' streamlit run app.py)
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import streamlit as st
import switcher
from variants import variant_a, variant_b, variant_c

VARIANTS = {"A": variant_a, "B": variant_b, "C": variant_c}

st.set_page_config(page_title="Portfolio prototype", layout="wide",
                   initial_sidebar_state="expanded")

# Strip Streamlit chrome — it is not part of any design being evaluated.
st.markdown("""
<style>
  header[data-testid="stHeader"], #MainMenu, footer { display:none !important; }
  [data-testid="stAppViewBlockContainer"], .block-container {
    padding-top: 2.6rem !important; padding-bottom: 1rem !important; }
  [data-testid="stExpander"] details { border-radius:8px; }
</style>
""", unsafe_allow_html=True)

active = switcher.current(VARIANTS)
VARIANTS[active].render()
switcher.render({k: m.NAME for k, m in VARIANTS.items()}, active)
