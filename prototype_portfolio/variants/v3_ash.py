"""
VARIANT 3 — "Ash"

The other reading of 'too light': keep a light interface, but take the white
out of it. A grey paper ground with ink-grey text — light enough to read as a
light theme, dim enough that a dense monospace page is not glaring.

Round 4. Round 2 chose Instrument; "but lighter" was read as near-white and came
back "too light". So this round brackets the middle of that range instead of
running to either end. Density, structure and block order are unchanged from the
original Instrument — the ground tone is the only variable.
"""
import streamlit as st
from content import SITE, KIND_LABEL
from variants import shell

NAME = "Ash — light grey paper, not white"

CSS = """
<style>
:root { --bg:#dfe3e7; --pan:#d7dce1; --r:#bcc4cc; --r2:#ccd3d9;
        --fg:#1a1f26; --fg2:#3f4954; --m:#6b7681; --m2:#828d98;
        --a:#0d4f9c; --ok:#26703a; --hv:#d2d8de; --sel:#cbd6e4; --selb:#a9bcd4;
        --code:#d5dae0; }
.stApp, section[data-testid="stSidebar"] { background:var(--bg); }
.stApp, .stApp p, .stApp div, .stApp span, .stApp h1, .stApp h2, .stApp button,
.stApp pre, .stApp code {
  font-family: ui-monospace,'SF Mono',SFMono-Regular,Menlo,Consolas,monospace !important; }
section[data-testid="stSidebar"] { background:var(--pan); border-right:1px solid var(--r); }
[data-testid="stExpandSidebarButton"] svg, [data-testid="stSidebarCollapseButton"] svg {
  fill:var(--m) !important; color:var(--m) !important; }
.who { font-size:12.5px; font-weight:600; color:var(--fg); letter-spacing:.02em; }
.who span { display:block; font-size:10.5px; font-weight:400; color:var(--m);
            margin-top:5px; line-height:1.6; }
.grp { font-size:9px; letter-spacing:.26em; text-transform:uppercase; color:var(--m2);
       margin:20px 0 4px; padding-bottom:4px; border-bottom:1px solid var(--r); }
section[data-testid="stSidebar"] .stButton > button {
  width:100%; text-align:left; justify-content:flex-start; background:transparent;
  border:1px solid transparent; border-radius:3px; padding:3px 7px; min-height:0;
  font-size:12px; color:var(--fg2); font-weight:400; letter-spacing:-.01em; }
section[data-testid="stSidebar"] .stButton > button:hover { background:var(--hv); color:var(--fg); }
section[data-testid="stSidebar"] .stButton > button[kind="primary"],
section[data-testid="stSidebar"] .stButton > button[data-testid="stBaseButton-primary"] {
  background:var(--sel); border-color:var(--selb); color:var(--a); font-weight:600; }
.hd { display:flex; align-items:baseline; gap:10px; padding-bottom:9px;
      border-bottom:1px solid var(--r); }
.hd h2 { font-size:15px !important; margin:0; font-weight:600; color:var(--fg);
         letter-spacing:.01em; }
.hd .meta { font-size:10.5px; color:var(--m); letter-spacing:.1em; text-transform:uppercase; }
.hd .st { font-size:10.5px; color:var(--ok); letter-spacing:.1em; text-transform:uppercase;
          margin-left:auto; }
.hd .st:before { content:"● "; }
.sub { color:var(--fg2); font-size:12.5px; margin:11px 0 0; line-height:1.7; max-width:78ch; }
.strip { display:flex; margin:16px 0 0; border-top:1px solid var(--r2);
         border-bottom:1px solid var(--r2); }
.strip div { padding:9px 20px 9px 0; margin-right:20px; border-right:1px solid var(--r2); }
.strip div:last-child { border-right:none; }
.strip b { display:block; font-size:15px; font-weight:600; color:var(--fg); letter-spacing:-.01em; }
.strip span { font-size:9px; letter-spacing:.2em; text-transform:uppercase; color:var(--m2); }
.lbl { font-size:9px; letter-spacing:.26em; text-transform:uppercase; color:var(--m2);
       margin:24px 0 7px; display:flex; align-items:center; gap:9px; }
.lbl:after { content:""; flex:1; height:1px; background:var(--r2); }
.pr { font-size:12.5px; line-height:1.85; color:var(--fg2); max-width:82ch; margin:0 0 12px; }
.code { background:var(--code); border:1px solid var(--r); border-radius:4px;
        padding:11px 13px; font-size:11.5px; line-height:1.65; color:var(--fg2);
        overflow-x:auto; margin:0 0 9px; white-space:pre; }
.code.cmd { color:var(--a); }
.kv { display:flex; gap:10px; font-size:11.5px; padding:4px 0; border-bottom:1px solid var(--r2); }
.kv .k { color:var(--m2); width:62px; flex:none; letter-spacing:.06em;
         text-transform:uppercase; font-size:9.5px; padding-top:2px; }
.kv .v { color:var(--fg2); }
.lk a { display:inline-block; font-size:11.5px; color:var(--a); text-decoration:none;
        border:1px solid var(--r); border-radius:3px; padding:3px 9px; margin:0 6px 6px 0; }
.lk a:hover { border-color:var(--a); background:var(--hv); }
.wrap { padding-bottom:120px; }
</style>
"""


def render():
    st.markdown(CSS, unsafe_allow_html=True)
    a = shell.selection()

    with st.sidebar:
        st.markdown(f'<div class="who">{SITE["name"]}<span>{SITE["tagline"]}</span></div>',
                    unsafe_allow_html=True)
        shell.nav()
        st.markdown('<div class="grp">Contact</div>', unsafe_allow_html=True)
        st.markdown(shell.contact_md(), unsafe_allow_html=True)

    st.markdown('<div class="wrap">', unsafe_allow_html=True)
    st.markdown(
        f'<div class="hd"><h2>{a["name"]}</h2>'
        f'<span class="meta">{KIND_LABEL[a["kind"]]} · {a["year"]}</span>'
        f'<span class="st">{a["status"]}</span></div>'
        f'<p class="sub">{a["one_liner"]}</p>',
        unsafe_allow_html=True,
    )
    if a.get("metrics"):
        st.markdown('<div class="strip">' + "".join(
            f"<div><b>{v}</b><span>{k}</span></div>" for k, v in a["metrics"].items()
        ) + "</div>", unsafe_allow_html=True)

    st.markdown(f'<div class="lbl">{shell.stage_label(a)}</div>', unsafe_allow_html=True)
    shell.stage(a, placeholder_tint="#31506f", tone="ash")

    left, right = st.columns([1.7, 1], gap="large")
    with left:
        st.markdown('<div class="lbl">Notes</div>', unsafe_allow_html=True)
        for p in a["prose"]:
            st.markdown(f'<p class="pr">{p}</p>', unsafe_allow_html=True)
        st.markdown(f'<div class="lk">{shell.links_html(a, "→")}</div>', unsafe_allow_html=True)
    with right:
        st.markdown('<div class="lbl">Facts</div>', unsafe_allow_html=True)
        st.markdown("".join(
            f'<div class="kv"><span class="k">{k}</span><span class="v">{v}</span></div>'
            for k, v in shell.facts(a)), unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
