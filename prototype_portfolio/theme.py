"""
PROTOTYPE — runtime theme + accessibility settings.

Rounds 1-4 settled the layout (Workbench), the visual language (Instrument) and
the ground tone (Slate). Those are no longer prototype variants; the tone is now
a CHOICE THE VIEWER MAKES, so the palette moves from three hardcoded modules into
one table applied at render time.

Everything lives in st.session_state — in memory, never persisted. Persistence is
the thing a prototype checks, not something it depends on.
"""
import streamlit as st

# --- ground tones ---------------------------------------------------------
# `icon` is a Material Symbols name; Streamlit resolves ":material/<name>:".
PALETTES = {
    "slate": dict(
        label="Slate", icon="dark_mode", hint="Soft charcoal. The default.",
        swatch="#1c2128", on_swatch="#dfe4ea",
        tok=dict(bg="#1c2128", pan="#191e24", r="#333b45", r2="#262d35",
                 fg="#dfe4ea", fg2="#adb7c2", m="#7d8894", m2="#68727d",
                 a="#6cb6ff", ok="#57ab5a", hv="#232a32", sel="#1f2a38",
                 selb="#2f4257", code="#171c22"),
        hc=dict(fg="#ffffff", fg2="#e6ebf0", m="#b8c2cc", m2="#a4aeb9",
                r="#5a6673", r2="#46505c", a="#9ecfff"),
    ),
    "fog": dict(
        label="Fog", icon="gradient", hint="Mid slate, softer contrast.",
        swatch="#2b323b", on_swatch="#e8ecf1",
        tok=dict(bg="#2b323b", pan="#272e36", r="#454e5a", r2="#39414b",
                 fg="#e8ecf1", fg2="#c2cad3", m="#94a0ad", m2="#7f8b98",
                 a="#8cc6ff", ok="#6cc26c", hv="#333b45", sel="#33404f",
                 selb="#465871", code="#242a32"),
        hc=dict(fg="#ffffff", fg2="#eef2f6", m="#c0c9d2", m2="#adb6c0",
                r="#6b7684", r2="#59636f", a="#b3daff"),
    ),
    "ash": dict(
        label="Ash", icon="light_mode", hint="Grey paper. Light without glare.",
        swatch="#dfe3e7", on_swatch="#1a1f26",
        tok=dict(bg="#dfe3e7", pan="#d7dce1", r="#bcc4cc", r2="#ccd3d9",
                 fg="#1a1f26", fg2="#3f4954", m="#6b7681", m2="#828d98",
                 a="#0d4f9c", ok="#26703a", hv="#d2d8de", sel="#cbd6e4",
                 selb="#a9bcd4", code="#d5dae0"),
        hc=dict(fg="#000000", fg2="#1a2028", m="#3d474f", m2="#4d5760",
                r="#8b96a1", r2="#a3adb6", a="#06316b"),
    ),
}

TEXT_SIZES = {"normal": ("Normal", 1.00), "large": ("Large", 1.15), "larger": ("Larger", 1.32)}

MONO = "ui-monospace,'SF Mono',SFMono-Regular,Menlo,Consolas,monospace"
READABLE = "'Atkinson Hyperlegible',Verdana,'DejaVu Sans',ui-sans-serif,system-ui,sans-serif"

DEFAULTS = dict(tone="slate", text="normal", contrast=False,
                readable=False, motion=True, underline=False)


def state():
    for k, v in DEFAULTS.items():
        st.session_state.setdefault(f"opt_{k}", v)
    return {k: st.session_state[f"opt_{k}"] for k in DEFAULTS}


def set_opt(key, value):
    st.session_state[f"opt_{key}"] = value
    st.rerun()


def toggle(key):
    st.session_state[f"opt_{key}"] = not st.session_state[f"opt_{key}"]
    st.rerun()


def reset():
    for k, v in DEFAULTS.items():
        st.session_state[f"opt_{k}"] = v
    st.rerun()


def is_default(s):
    return all(s[k] == v for k, v in DEFAULTS.items())


def css(s):
    """The whole page stylesheet, derived from the current settings."""
    p = PALETTES[s["tone"]]
    tok = dict(p["tok"])
    if s["contrast"]:
        tok.update(p["hc"])

    scale = TEXT_SIZES[s["text"]][1]
    ff = READABLE if s["readable"] else MONO
    # A readable face needs more air than a condensed mono at the same size.
    lh = 1.95 if s["readable"] else 1.85
    trk = ".005em" if s["readable"] else "0"
    bw = "2px" if s["contrast"] else "1px"
    ul = "underline" if s["underline"] else "none"

    vars_ = " ".join(f"--{k}:{v};" for k, v in tok.items())
    motion = "" if s["motion"] else """
*, *::before, *::after { transition:none !important; animation:none !important;
  scroll-behavior:auto !important; }"""

    return f"""
<style>
:root {{ {vars_} --s:{scale}; --ff:{ff}; --bw:{bw}; }}
.stApp, section[data-testid="stSidebar"] {{ background:var(--bg); }}
.stApp, .stApp p, .stApp div, .stApp span, .stApp h1, .stApp h2, .stApp button,
.stApp pre, .stApp code, .stApp input {{
  font-family: var(--ff) !important; letter-spacing:{trk}; }}
.stApp [data-testid="stIconMaterial"] {{ font-family:'Material Symbols Rounded' !important; }}
section[data-testid="stSidebar"] {{ background:var(--pan); border-right:var(--bw) solid var(--r); }}
[data-testid="stExpandSidebarButton"] svg, [data-testid="stSidebarCollapseButton"] svg {{
  fill:var(--m) !important; color:var(--m) !important; }}

.who {{ font-size:calc(12.5px*var(--s)) !important; font-weight:600 !important; color:var(--fg); }}
.who span {{ display:block; font-size:calc(10.5px*var(--s)) !important; font-weight:400 !important; color:var(--m);
            margin-top:5px; line-height:1.6 !important; }}
.grp {{ font-size:calc(9px*var(--s)) !important; letter-spacing:.26em; text-transform:uppercase;
       color:var(--m2); margin:0; padding:16px 0 4px;
       border-bottom:1px solid var(--r); }}
/* NOTE: `.stButton button`, not `.stButton > button`. A button given help= is
   wrapped in tooltip spans, so the direct-child combinator silently skips every
   button carrying a tooltip — which was the entire options panel. */
section[data-testid="stSidebar"] .stButton button {{
  width:100%; text-align:left; justify-content:flex-start; background:transparent;
  border:1px solid transparent; border-radius:3px; padding:3px 7px; min-height:0;
  font-size:calc(12px*var(--s)) !important; color:var(--fg2); font-weight:400 !important; }}
section[data-testid="stSidebar"] .stButton button:hover {{ background:var(--hv); color:var(--fg); }}
section[data-testid="stSidebar"] .stButton button[kind="primary"],
section[data-testid="stSidebar"] .stButton button[data-testid="stBaseButton-primary"] {{
  background:var(--sel); border-color:var(--selb); color:var(--a); font-weight:600 !important; }}
section[data-testid="stSidebar"] .stButton button:focus-visible {{
  outline:2px solid var(--a); outline-offset:2px; }}
/* Streamlit's default 1rem block gap undoes the density the whole design argues
   for; the sidebar is a list, not a stack of cards. */
section[data-testid="stSidebar"] [data-testid="stVerticalBlock"] {{ gap:6px !important; }}
/* Streamlit's markdown wrapper does NOT grow with the inner div's padding — the
   header overflows its own element container by exactly its top padding, and the
   next control sits on top of it. The default 1rem block gap was hiding that;
   tightening the gap exposed it. Give those containers an explicit floor. */
section[data-testid="stSidebar"] [data-testid="stElementContainer"]:has(.grp) {{
  min-height:calc(44px*var(--s)) !important; }}
section[data-testid="stSidebar"] [data-testid="stElementContainer"]:has(.opt-row-lbl) {{
  min-height:calc(30px*var(--s)) !important; }}
section[data-testid="stSidebar"] [data-testid="stElementContainer"]:has(.opt-hint) {{
  min-height:calc(34px*var(--s)) !important; }}
section[data-testid="stSidebar"] [data-testid="stElementContainer"]:has(.drw-sum) {{
  min-height:calc(24px*var(--s)) !important; }}

.hd {{ display:flex; align-items:baseline; gap:10px; padding-bottom:9px;
      border-bottom:var(--bw) solid var(--r); }}
.hd h2 {{ font-size:calc(15px*var(--s)) !important; margin:0; font-weight:600 !important; color:var(--fg); }}
.hd .meta {{ font-size:calc(10.5px*var(--s)) !important; color:var(--m); letter-spacing:.1em;
            text-transform:uppercase; }}
.hd .st {{ font-size:calc(10.5px*var(--s)) !important; color:var(--ok); letter-spacing:.1em;
          text-transform:uppercase; margin-left:auto; }}
.hd .st:before {{ content:"● "; }}
.sub {{ color:var(--fg2); font-size:calc(12.5px*var(--s)) !important; margin:0; padding:11px 0 0;
       line-height:{lh}; max-width:78ch; }}
.strip {{ display:flex; margin:0; padding:16px 0 0; border-top:1px solid var(--r2);
         border-bottom:1px solid var(--r2); flex-wrap:wrap; }}
.strip div {{ padding:9px 20px 9px 0; margin-right:20px; border-right:1px solid var(--r2); }}
.strip div:last-child {{ border-right:none; }}
.strip b {{ display:block; font-size:calc(15px*var(--s)) !important; font-weight:600 !important; color:var(--fg); }}
.strip span {{ font-size:calc(9px*var(--s)) !important; letter-spacing:.2em; text-transform:uppercase;
              color:var(--m2); }}
.lbl {{ font-size:calc(9px*var(--s)) !important; letter-spacing:.26em; text-transform:uppercase;
       color:var(--m2); margin:0; padding:24px 0 7px; display:flex; align-items:center; gap:9px; }}
.lbl:after {{ content:""; flex:1; height:1px; background:var(--r2); }}
.pr {{ font-size:calc(12.5px*var(--s)) !important; line-height:{lh}; color:var(--fg2);
      max-width:82ch; margin:0; padding:0 0 12px; }}
.code {{ background:var(--code); border:1px solid var(--r); border-radius:4px;
        padding:11px 13px; font-size:calc(11.5px*var(--s)) !important; line-height:1.65 !important;
        color:var(--fg2); overflow-x:auto; margin:0 0 9px; white-space:pre;
        font-family:{MONO} !important; }}
.code.cmd {{ color:var(--a); }}
.kv {{ display:flex; gap:10px; font-size:calc(11.5px*var(--s)) !important; padding:4px 0;
      border-bottom:1px solid var(--r2); }}
.kv .k {{ color:var(--m2); width:66px; flex:none; letter-spacing:.06em;
         text-transform:uppercase; font-size:calc(9.5px*var(--s)) !important; padding-top:2px; }}
.kv .v {{ color:var(--fg2); }}
.lk a, .stApp a {{ color:var(--a); text-decoration:{ul}; }}
.lk a {{ display:inline-block; font-size:calc(11.5px*var(--s)) !important;
        border:1px solid var(--r); border-radius:3px; padding:3px 9px; margin:0 6px 6px 0; }}
.lk a:hover {{ border-color:var(--a); background:var(--hv); }}
.wrap {{ padding-bottom:140px; }}

/* ---- options panel, shared bits ---- */
.opt-hint {{ font-size:calc(9.5px*var(--s)) !important; color:var(--m2); line-height:1.55 !important;
            margin:0; padding:2px 0 8px; }}
.opt-row-lbl {{ font-size:calc(9px*var(--s)) !important; letter-spacing:.2em; text-transform:uppercase;
               color:var(--m2); margin:0; padding:12px 0 3px; }}
{motion}
</style>
"""
