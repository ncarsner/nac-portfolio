"""
VARIANT 2 — "Instrument Airy"

Round 3, second reading of "lighter". If the note meant lighter in *weight* rather
than lighter in colour, this is it: the same near-white ground and the same
monospace character, but the vertical rhythm opened up roughly half again, type a
notch larger, weights dropped, and most of the hairline rules removed so space
does the separating instead.
"""
import streamlit as st
from content import SITE, KIND_LABEL
from variants import shell

NAME = "Instrument Airy — lighter weight, open rhythm"

CSS = """
<style>
:root { --bg:#fcfcfd; --pan:#f7f8fa; --r:#e1e5ea; --r2:#eef1f4;
        --fg:#10151a; --fg2:#454e58; --m:#8891a0; --m2:#a3abb8;
        --a:#0b5fd0; --ok:#1a7f37; }
.stApp, section[data-testid="stSidebar"] { background:var(--bg); }
.stApp, .stApp p, .stApp div, .stApp span, .stApp h1, .stApp h2, .stApp button {
  font-family: ui-monospace,'SF Mono',SFMono-Regular,Menlo,Consolas,monospace !important; }
section[data-testid="stSidebar"] { background:var(--pan); border-right:1px solid var(--r); }
.who { font-size:13.5px; font-weight:500; color:var(--fg); letter-spacing:.02em; }
.who span { display:block; font-size:10.5px; font-weight:400; color:var(--m);
            margin-top:9px; line-height:1.8; }
.grp { font-size:9px; letter-spacing:.3em; text-transform:uppercase; color:var(--m2);
       margin:34px 0 10px; }
section[data-testid="stSidebar"] .stButton > button {
  width:100%; text-align:left; justify-content:flex-start; background:transparent;
  border:1px solid transparent; border-radius:4px; padding:6px 8px; min-height:0;
  font-size:12.5px; color:var(--fg2); font-weight:400; letter-spacing:-.01em; }
section[data-testid="stSidebar"] .stButton > button:hover { background:#eceff3; color:var(--fg); }
section[data-testid="stSidebar"] .stButton > button[kind="primary"],
section[data-testid="stSidebar"] .stButton > button[data-testid="stBaseButton-primary"] {
  background:#e8eef8; border-color:#c9dbf5; color:var(--a); font-weight:600; }
.hd { display:flex; align-items:baseline; gap:16px; padding-bottom:0; }
.hd h2 { font-size:19px !important; margin:0; font-weight:500; color:var(--fg);
         letter-spacing:.01em; }
.hd .meta { font-size:10.5px; color:var(--m); letter-spacing:.1em; text-transform:uppercase; }
.hd .st { font-size:10.5px; color:var(--ok); letter-spacing:.1em; text-transform:uppercase;
          margin-left:auto; }
.hd .st:before { content:"● "; }
.sub { color:var(--fg2); font-size:14px; margin:18px 0 0; line-height:2.0; max-width:70ch; font-weight:300; }
.strip { display:flex; gap:52px; margin:38px 0 0; }
.strip div { padding:0; }
.strip b { display:block; font-size:19px; font-weight:400; color:var(--fg); letter-spacing:-.01em; }
.strip span { display:block; margin-top:8px; font-size:9px; letter-spacing:.24em; text-transform:uppercase; color:var(--m2); }
.lbl { font-size:9px; letter-spacing:.3em; text-transform:uppercase; color:var(--m2);
       margin:46px 0 16px; }
.pr { font-size:13.5px; line-height:2.05; color:var(--fg2); max-width:72ch; margin:0 0 22px;
      font-weight:300; }
.kv { display:flex; gap:14px; font-size:12.5px; padding:11px 0; }
.kv .k { color:var(--m2); width:66px; flex:none; letter-spacing:.06em;
         text-transform:uppercase; font-size:9.5px; padding-top:2px; }
.kv .v { color:var(--fg2); }
.lk a { display:inline-block; font-size:11.5px; color:var(--a); text-decoration:none;
        border:none; border-bottom:1px solid #cfd8e4; border-radius:0; padding:2px 0;
        margin:0 22px 8px 0; }
.lk a:hover { border-bottom-color:var(--a); }
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
    shell.stage(a, height=470, placeholder_tint="#1b4f96")

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
