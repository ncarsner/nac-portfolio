"""
VARIANT 3 — "Console"

Visual thesis: be memorable rather than tasteful. High contrast, thick rules,
hard edges, no rounding, no shadows, no gradients. Heavy grotesk at two extreme
sizes — very large or very small, nothing in between. One loud accent doing all
the work.

Title block: oversized, uppercase, sitting on a hard rule. Metrics: a bordered
grid of hard cells. Bets that a portfolio's real failure mode is being forgotten,
not being disliked.
"""
import streamlit as st
from content import SITE, KIND_LABEL
from variants import shell

NAME = "Console — high-contrast, hard edges, loud accent"

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;700&display=swap');
:root { --bg:#101014; --pan:#08080a; --ink:#f2f2f0; --fg2:#a8a8a4;
        --m:#6b6b68; --line:#f2f2f0; --a:#d6ff3f; --r:#2b2b31; }
.stApp, section[data-testid="stSidebar"] { background:var(--bg); }
.stApp, .stApp p, .stApp div, .stApp span, .stApp button {
  font-family:'Space Grotesk',ui-sans-serif,system-ui,'Helvetica Neue',sans-serif !important; }
section[data-testid="stSidebar"] { background:var(--pan); border-right:2px solid var(--line); }
.who { font-size:16px; font-weight:700; color:var(--ink); text-transform:uppercase;
       letter-spacing:.02em; line-height:1.15; }
.who span { display:block; font-size:11px; font-weight:400; color:var(--m);
            margin-top:9px; line-height:1.55; text-transform:none; letter-spacing:0; }
.grp { font-size:9px; letter-spacing:.22em; text-transform:uppercase; color:var(--bg);
       background:var(--a); margin:22px 0 6px; padding:3px 7px; font-weight:700;
       display:inline-block; }
section[data-testid="stSidebar"] .stButton > button {
  width:100%; text-align:left; justify-content:flex-start; background:transparent;
  border:2px solid transparent; border-radius:0 !important; padding:5px 8px; min-height:0;
  font-size:12.5px; color:var(--fg2); font-weight:500; text-transform:uppercase;
  letter-spacing:.03em; }
section[data-testid="stSidebar"] .stButton > button:hover { border-color:var(--r); color:var(--ink); }
section[data-testid="stSidebar"] .stButton > button[kind="primary"],
section[data-testid="stSidebar"] .stButton > button[data-testid="stBaseButton-primary"] {
  background:var(--a); border-color:var(--a); color:#101014; font-weight:700; }
.hd { border-bottom:2px solid var(--line); padding-bottom:14px; }
.hd h2 { font-size:52px !important; margin:8px 0 0; font-weight:700; color:var(--ink);
         text-transform:uppercase; letter-spacing:-.035em; line-height:.94; }
.kicker { font-size:10px; letter-spacing:.2em; text-transform:uppercase; font-weight:700; }
.kicker .tag { background:var(--a); color:#101014; padding:2px 7px; margin-right:7px; }
.kicker .yr { color:var(--m); }
.sub { color:var(--fg2); font-size:15px; margin:16px 0 0; line-height:1.55;
       max-width:56ch; font-weight:400; }
.strip { display:flex; margin:24px 0 0; border:2px solid var(--line); }
.strip div { flex:1; padding:14px 16px; border-right:2px solid var(--line); }
.strip div:last-child { border-right:none; }
.strip b { display:block; font-size:26px; font-weight:700; color:var(--a);
           letter-spacing:-.03em; line-height:1; }
.strip span { display:block; font-size:9px; letter-spacing:.18em; text-transform:uppercase;
              color:var(--m); margin-top:8px; font-weight:500; }
.lbl { font-size:9px; letter-spacing:.22em; text-transform:uppercase; color:#101014;
       background:var(--a); margin:34px 0 12px; padding:3px 8px; display:inline-block;
       font-weight:700; }
.pr { font-size:14.5px; line-height:1.72; color:var(--fg2); max-width:64ch; margin:0 0 16px; }
.kv { display:flex; gap:12px; padding:8px 0; border-bottom:1px solid var(--r); }
.kv .k { color:var(--m); width:64px; flex:none; font-size:9px; letter-spacing:.18em;
         text-transform:uppercase; font-weight:700; padding-top:3px; }
.kv .v { color:var(--fg2); font-size:13.5px; }
.lk a { display:inline-block; font-size:11.5px; color:var(--ink); text-decoration:none;
        border:2px solid var(--line); padding:5px 12px; margin:0 8px 8px 0;
        text-transform:uppercase; letter-spacing:.08em; font-weight:700; }
.lk a:hover { background:var(--a); border-color:var(--a); color:#101014; }
.wrap { padding-bottom:130px; }
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
        f'<div class="hd"><div class="kicker"><span class="tag">{KIND_LABEL[a["kind"]]}</span>'
        f'<span class="tag">{a["status"]}</span><span class="yr">{a["year"]}</span></div>'
        f'<h2>{a["name"]}</h2></div>'
        f'<p class="sub">{a["one_liner"]}</p>',
        unsafe_allow_html=True,
    )
    if a.get("metrics"):
        st.markdown('<div class="strip">' + "".join(
            f"<div><b>{v}</b><span>{k}</span></div>" for k, v in a["metrics"].items()
        ) + "</div>", unsafe_allow_html=True)

    st.markdown(f'<div class="lbl">{shell.stage_label(a)}</div>', unsafe_allow_html=True)
    shell.stage(a, height=470, placeholder_tint="#3d4a12")

    left, right = st.columns([1.7, 1], gap="large")
    with left:
        st.markdown('<div class="lbl">Notes</div>', unsafe_allow_html=True)
        for p in a["prose"]:
            st.markdown(f'<p class="pr">{p}</p>', unsafe_allow_html=True)
        st.markdown(f'<div class="lk">{shell.links_html(a, "")}</div>', unsafe_allow_html=True)
    with right:
        st.markdown('<div class="lbl">Facts</div>', unsafe_allow_html=True)
        st.markdown("".join(
            f'<div class="kv"><span class="k">{k}</span><span class="v">{v}</span></div>'
            for k, v in shell.facts(a)), unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
