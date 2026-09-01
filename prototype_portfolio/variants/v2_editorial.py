"""
VARIANT 2 — "Editorial"

Visual thesis: the opposite bet from Instrument. Light, warm, generous, low
density. Serif display type at a large scale, comfortable measures, whitespace
doing the structural work instead of borders. Reads as a considered publication
rather than a tool.

Title block: large, quiet, no pills — status and kind demoted to a single line of
small caps. Metrics: widely spaced numerals, no boxes. Bets that restraint of a
different kind — space, not density — is what signals seniority.
"""
import streamlit as st
from content import SITE, KIND_LABEL
from variants import shell

NAME = "Editorial — light, airy, serif display"

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;1,6..72,400&display=swap');
:root { --bg:#faf8f4; --pan:#f4f1eb; --r:#e2ddd3; --r2:#ece8e0;
        --fg:#1c1a17; --fg2:#4a463f; --m:#8b857a; --a:#9a4a2f; }
.stApp, section[data-testid="stSidebar"] { background:var(--bg); }
.stApp, .stApp p, .stApp div, .stApp span, .stApp button {
  font-family:'Newsreader',Georgia,'Iowan Old Style',serif !important; }
section[data-testid="stSidebar"] { background:var(--pan); border-right:1px solid var(--r); }
.who { font-size:19px; font-weight:500; color:var(--fg); letter-spacing:-.015em; }
.who span { display:block; font-size:13.5px; font-weight:400; color:var(--m);
            margin-top:8px; line-height:1.65; font-style:italic; }
.grp { font-size:9.5px; letter-spacing:.24em; text-transform:uppercase; color:var(--m);
       margin:30px 0 8px; font-family:ui-sans-serif,system-ui,sans-serif !important; }
section[data-testid="stSidebar"] .stButton > button {
  width:100%; text-align:left; justify-content:flex-start; background:transparent;
  border:none; border-radius:0; padding:5px 0; min-height:0; font-size:15px;
  color:var(--fg2); font-weight:400; letter-spacing:-.01em; }
section[data-testid="stSidebar"] .stButton > button:hover { color:var(--a); background:transparent; }
section[data-testid="stSidebar"] .stButton > button[kind="primary"],
section[data-testid="stSidebar"] .stButton > button[data-testid="stBaseButton-primary"] {
  background:transparent; border:none; color:var(--fg); font-weight:500; font-style:italic; }
.hd h2 { font-size:40px !important; margin:6px 0 0; font-weight:400; color:var(--fg);
         letter-spacing:-.028em; line-height:1.12; }
.kicker { font-size:10px; letter-spacing:.24em; text-transform:uppercase; color:var(--m);
          font-family:ui-sans-serif,system-ui,sans-serif !important; }
.sub { color:var(--fg2); font-size:19px; margin:16px 0 0; line-height:1.6;
       max-width:44ch; font-style:italic; }
.strip { display:flex; gap:56px; margin:40px 0 8px; }
.strip b { display:block; font-size:31px; font-weight:400; color:var(--fg);
           letter-spacing:-.03em; line-height:1; }
.strip span { display:block; font-size:9.5px; letter-spacing:.2em; text-transform:uppercase;
              color:var(--m); margin-top:9px;
              font-family:ui-sans-serif,system-ui,sans-serif !important; }
.lbl { font-size:9.5px; letter-spacing:.24em; text-transform:uppercase; color:var(--m);
       margin:46px 0 14px; font-family:ui-sans-serif,system-ui,sans-serif !important; }
.pr { font-size:17px; line-height:1.78; color:var(--fg2); max-width:60ch; margin:0 0 19px; }
.kv { padding:10px 0; border-bottom:1px solid var(--r2); }
.kv .k { display:block; color:var(--m); font-size:9.5px; letter-spacing:.18em;
         text-transform:uppercase; margin-bottom:4px;
         font-family:ui-sans-serif,system-ui,sans-serif !important; }
.kv .v { color:var(--fg2); font-size:15px; }
.lk a { display:inline-block; font-size:15px; color:var(--a); text-decoration:none;
        border-bottom:1px solid #d8c4ba; padding:1px 0; margin:0 20px 8px 0; }
.lk a:hover { border-bottom-color:var(--a); }
.wrap { padding-bottom:130px; max-width:1080px; }
</style>
"""


def render():
    st.markdown(CSS, unsafe_allow_html=True)
    a = shell.selection()

    with st.sidebar:
        st.markdown(f'<div class="who">{SITE["name"]}<span>{SITE["tagline"]}</span></div>',
                    unsafe_allow_html=True)
        shell.nav(marker=False)
        st.markdown('<div class="grp">Contact</div>', unsafe_allow_html=True)
        st.markdown(shell.contact_md(), unsafe_allow_html=True)

    st.markdown('<div class="wrap">', unsafe_allow_html=True)
    st.markdown(
        f'<div class="hd"><div class="kicker">{KIND_LABEL[a["kind"]]} &nbsp;·&nbsp; '
        f'{a["year"]} &nbsp;·&nbsp; {a["status"]}</div>'
        f'<h2>{a["name"]}</h2></div>'
        f'<p class="sub">{a["one_liner"]}</p>',
        unsafe_allow_html=True,
    )
    if a.get("metrics"):
        st.markdown('<div class="strip">' + "".join(
            f"<div><b>{v}</b><span>{k}</span></div>" for k, v in a["metrics"].items()
        ) + "</div>", unsafe_allow_html=True)

    st.markdown(f'<div class="lbl">{shell.stage_label(a)}</div>', unsafe_allow_html=True)
    shell.stage(a, height=470, placeholder_tint="#8b6f5a")

    left, right = st.columns([1.7, 1], gap="large")
    with left:
        st.markdown('<div class="lbl">Notes</div>', unsafe_allow_html=True)
        for p in a["prose"]:
            st.markdown(f'<p class="pr">{p}</p>', unsafe_allow_html=True)
        st.markdown(f'<div class="lk">{shell.links_html(a)}</div>', unsafe_allow_html=True)
    with right:
        st.markdown('<div class="lbl">Facts</div>', unsafe_allow_html=True)
        st.markdown("".join(
            f'<div class="kv"><span class="k">{k}</span><span class="v">{v}</span></div>'
            for k, v in shell.facts(a)), unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
