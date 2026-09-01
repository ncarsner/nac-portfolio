"""
VARIANT 1 — "Instrument Light"

Round 3. Round 2 chose Instrument; the note was "but lighter". This is the direct
translation: the same control-surface character — monospace throughout, hairline
rules, no decoration, colour only where it carries signal — moved onto a near-white
ground. Density is unchanged from the dark original, so this isolates the one
variable that was actually asked about.
"""
import streamlit as st
from content import SITE, KIND_LABEL
from variants import shell

NAME = "Instrument Light — same density, near-white"

CSS = """
<style>
:root { --bg:#fcfcfd; --pan:#f7f8fa; --r:#e1e5ea; --r2:#eef1f4;
        --fg:#10151a; --fg2:#454e58; --m:#8891a0; --m2:#a3abb8;
        --a:#0b5fd0; --ok:#1a7f37; }
.stApp, section[data-testid="stSidebar"] { background:var(--bg); }
.stApp, .stApp p, .stApp div, .stApp span, .stApp h1, .stApp h2, .stApp button {
  font-family: ui-monospace,'SF Mono',SFMono-Regular,Menlo,Consolas,monospace !important; }
section[data-testid="stSidebar"] { background:var(--pan); border-right:1px solid var(--r); }
.who { font-size:12.5px; font-weight:600; color:var(--fg); letter-spacing:.02em; }
.who span { display:block; font-size:10.5px; font-weight:400; color:var(--m);
            margin-top:5px; line-height:1.6; }
.grp { font-size:9px; letter-spacing:.26em; text-transform:uppercase; color:var(--m2);
       margin:20px 0 4px; padding-bottom:4px; border-bottom:1px solid var(--r); }
section[data-testid="stSidebar"] .stButton > button {
  width:100%; text-align:left; justify-content:flex-start; background:transparent;
  border:1px solid transparent; border-radius:3px; padding:3px 7px; min-height:0;
  font-size:12px; color:var(--fg2); font-weight:400; letter-spacing:-.01em; }
section[data-testid="stSidebar"] .stButton > button:hover { background:#eceff3; color:var(--fg); }
section[data-testid="stSidebar"] .stButton > button[kind="primary"],
section[data-testid="stSidebar"] .stButton > button[data-testid="stBaseButton-primary"] {
  background:#e8eef8; border-color:#c9dbf5; color:var(--a); font-weight:600; }
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
.kv { display:flex; gap:10px; font-size:11.5px; padding:4px 0; border-bottom:1px solid var(--r2); }
.kv .k { color:var(--m2); width:62px; flex:none; letter-spacing:.06em;
         text-transform:uppercase; font-size:9.5px; padding-top:2px; }
.kv .v { color:var(--fg2); }
.lk a { display:inline-block; font-size:11.5px; color:var(--a); text-decoration:none;
        border:1px solid var(--r); border-radius:3px; padding:3px 9px; margin:0 6px 6px 0; }
.lk a:hover { border-color:var(--a); background:#f2f6fd; }
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
