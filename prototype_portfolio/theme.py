"""
PROTOTYPE — runtime theme + accessibility settings.

The palette has two independent axes, so it is GENERATED rather than written out
fifteen times:

  mode   how light the page is        dark / mid / light
  base   which hue the neutrals and the accent are built from
                                      blue / green / silver / gold / magenta

Each mode is a ramp of (saturation, lightness) targets per token; each base
supplies a hue and a saturation multiplier. Silver is simply a base whose
multiplier is near zero. That keeps every combination internally consistent —
picking a new base can never produce a page whose borders and text stop relating
to its background.

Everything lives in st.session_state — in memory, never persisted.
"""
import colorsys

import streamlit as st


def _hex(h, s, l):
    """h in degrees, s and l in percent."""
    r, g, b = colorsys.hls_to_rgb((h % 360) / 360.0, max(0, min(100, l)) / 100.0,
                                  max(0, min(100, s)) / 100.0)
    return "#%02x%02x%02x" % (round(r * 255), round(g * 255), round(b * 255))


# token -> (saturation, lightness) per mode. Order is the whole design in a table.
MODE_SPEC = {
    "dark": dict(bg=(14, 12), pan=(14, 10), r=(12, 24), r2=(12, 17),
                 fg=(10, 90), fg2=(10, 73), m=(8, 55), m2=(8, 45),
                 hv=(14, 16), sel=(28, 19), selb=(30, 32), code=(14, 9),
                 a=(95, 70), tint=(50, 30)),
    "mid":  dict(bg=(12, 20), pan=(12, 18), r=(11, 32), r2=(11, 25),
                 fg=(12, 93), fg2=(11, 80), m=(9, 63), m2=(9, 54),
                 hv=(12, 24), sel=(24, 26), selb=(28, 40), code=(12, 17),
                 a=(95, 77), tint=(50, 36)),
    "light": dict(bg=(12, 89), pan=(12, 85), r=(12, 72), r2=(12, 80),
                  fg=(18, 11), fg2=(14, 27), m=(10, 45), m2=(10, 56),
                  hv=(12, 84), sel=(30, 82), selb=(32, 66), code=(12, 85),
                  a=(85, 32), tint=(50, 30)),
}

# High contrast pushes text to the extremes and strengthens the rules.
MODE_HC = {
    "dark":  dict(fg=(0, 100), fg2=(6, 94), m=(6, 78), m2=(6, 70),
                  r=(14, 42), r2=(14, 34), a=(100, 80)),
    "mid":   dict(fg=(0, 100), fg2=(6, 95), m=(7, 80), m2=(7, 72),
                  r=(14, 48), r2=(14, 40), a=(100, 84)),
    "light": dict(fg=(0, 0), fg2=(10, 10), m=(10, 28), m2=(10, 34),
                  r=(14, 48), r2=(14, 58), a=(95, 24)),
}

# Status green stays semantic, so it does not follow the base hue.
MODE_OK = {"dark": "#57ab5a", "mid": "#6cc26c", "light": "#26703a"}

MODES = {
    "dark":  dict(label="Dark",  icon="dark_mode",         hint="Soft charcoal. The default."),
    "mid":   dict(label="Mid",   icon="brightness_medium", hint="Mid slate, softer contrast."),
    "light": dict(label="Light", icon="light_mode",        hint="Grey paper. Light without glare."),
}

# hue in degrees, and how much of the mode's saturation to actually use.
BASES = {
    "blue":    dict(label="Blue",    h=212, mul=1.00),
    "green":   dict(label="Green",   h=148, mul=0.92),
    "silver":  dict(label="Silver",  h=215, mul=0.22),
    "gold":    dict(label="Gold",    h=42,  mul=1.00),
    "magenta": dict(label="Magenta", h=318, mul=0.92),
}


def palette(mode, base, contrast=False):
    spec = dict(MODE_SPEC[mode])
    if contrast:
        spec.update(MODE_HC[mode])
    h, mul = BASES[base]["h"], BASES[base]["mul"]
    tok = {k: _hex(h, s * mul, l) for k, (s, l) in spec.items()}
    tok["ok"] = MODE_OK[mode]
    return tok


def swatch(base, mode):
    """The colour shown on a base selector — the accent as it will actually
    appear in the current mode, not an abstract hue."""
    s, l = MODE_SPEC[mode]["a"]
    b = BASES[base]
    return _hex(b["h"], s * b["mul"], l)


# --- text size ------------------------------------------------------------
# 100% is what used to be 90%: the old default read too large at this density.
# Ten-point steps rather than fifteen, and more of them, so the adjustment is
# fine enough to actually land on a comfortable size.
TEXT_BASE = 0.90
TEXT_PCTS = [80, 90, 100, 110, 120, 130, 140, 150]
TEXT_DEFAULT = TEXT_PCTS.index(100)


def text_scale(idx):
    return TEXT_BASE * TEXT_PCTS[idx] / 100.0


def text_pct(idx):
    return f"{TEXT_PCTS[idx]}%"


MONO = "ui-monospace,'SF Mono',SFMono-Regular,Menlo,Consolas,monospace"
READABLE = "'Atkinson Hyperlegible',Verdana,'DejaVu Sans',ui-sans-serif,system-ui,sans-serif"

# Reduced motion is on by default; high contrast is not. Motion is the one where
# the default costs nothing — a still page reads the same to everyone, so there is
# no reason to make anyone opt out of it. High contrast genuinely changes the look
# the design settled on over four rounds, so it stays opt-in.
# Note `motion` is stored as "motion is allowed", so reduced motion is motion=False.
DEFAULTS = dict(mode="dark", base="blue", text_idx=TEXT_DEFAULT, contrast=False,
                readable=False, motion=False, underline=False)


def state():
    for k, v in DEFAULTS.items():
        st.session_state.setdefault(f"opt_{k}", v)
    return {k: st.session_state[f"opt_{k}"] for k in DEFAULTS}


def set_opt(key, value):
    st.session_state[f"opt_{key}"] = value
    st.rerun()


def step_text(delta):
    i = st.session_state["opt_text_idx"] + delta
    st.session_state["opt_text_idx"] = max(0, min(len(TEXT_PCTS) - 1, i))
    st.rerun()


def reset_text():
    """Back to 100%. The +/- steps are relative to this."""
    st.session_state["opt_text_idx"] = TEXT_DEFAULT
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


def summary(s):
    """Human sentence describing the active settings; also the screen-reader
    announcement whenever anything changes."""
    bits = [f'{MODES[s["mode"]]["label"]} mode',
            f'{BASES[s["base"]]["label"].lower()} base',
            f'text {text_pct(s["text_idx"])}']
    if s["contrast"]:
        bits.append("high contrast")
    if s["readable"]:
        bits.append("readable font")
    if s["underline"]:
        bits.append("underlined links")
    if not s["motion"]:
        bits.append("reduced motion")
    return " · ".join(bits)


def css(s):
    """The whole page stylesheet, derived from the current settings."""
    tok = palette(s["mode"], s["base"], s["contrast"])
    scale = text_scale(s["text_idx"])
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
section[data-testid="stSidebar"] [data-testid="stElementContainer"]:has(.contact) {{
  min-height:calc(50px*var(--s)) !important; }}
section[data-testid="stSidebar"] [data-testid="stElementContainer"]:has(.quote) {{
  min-height:calc(58px*var(--s)) !important; }}

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
/* Screen-reader-only: present to assistive tech, invisible on screen. Used for
   the live status announcement and any label an icon-only control needs. */
.sr-only {{ position:absolute !important; width:1px; height:1px; padding:0;
  margin:-1px; overflow:hidden; clip:rect(0 0 0 0); white-space:nowrap; border:0; }}

/* A joined segmented control: buttons butted together into one object, so they
   read as a single choice rather than as separate switches. Keyed on the
   container keys — there is no class to hang this on. */
.st-key-mode_seg [data-testid="stHorizontalBlock"],
.st-key-size_seg [data-testid="stHorizontalBlock"] {{ gap:0 !important; }}
.st-key-mode_seg [data-testid="stColumn"],
.st-key-size_seg [data-testid="stColumn"] {{ min-width:0 !important; }}
/* the button's wrapper is shrink-to-fit, so `width:100%` on the button alone
   resolves against the icon's own width. Widen every box in the chain. */
.st-key-mode_seg [data-testid="stColumn"] > div,
.st-key-size_seg [data-testid="stColumn"] > div,
.st-key-mode_seg [data-testid="stElementContainer"],
.st-key-size_seg [data-testid="stElementContainer"],
.st-key-mode_seg .stButton,
.st-key-size_seg .stButton {{ width:100% !important; display:block !important; }}
.st-key-mode_seg .stButton button,
.st-key-size_seg .stButton button {{
  width:100% !important; justify-content:center !important; padding:0 !important;
  height:calc(30px*var(--s)); border-radius:0 !important;
  border:1px solid var(--r) !important; margin-left:-1px !important;
  background:transparent !important; }}
.st-key-mode_seg [data-testid="stColumn"]:first-child .stButton button,
.st-key-size_seg [data-testid="stColumn"]:first-child .stButton button {{
  border-radius:4px 0 0 4px !important; margin-left:0 !important; }}
.st-key-mode_seg [data-testid="stColumn"]:last-child .stButton button,
.st-key-size_seg [data-testid="stColumn"]:last-child .stButton button {{
  border-radius:0 4px 4px 0 !important; }}
.st-key-mode_seg .stButton button:hover,
.st-key-size_seg .stButton button:hover {{ background:var(--hv) !important; z-index:1; }}
.st-key-mode_seg .stButton button[kind="primary"],
.st-key-mode_seg .stButton button[data-testid="stBaseButton-primary"] {{
  background:var(--sel) !important; border-color:var(--a) !important; z-index:2; }}
.st-key-size_seg .stButton button:disabled {{ opacity:.35 !important; }}
.st-key-mode_seg [data-testid="stIconMaterial"],
.st-key-size_seg [data-testid="stIconMaterial"] {{
  font-size:calc(17px*var(--s)) !important; color:var(--fg2); }}
.st-key-mode_seg .stButton button[data-testid="stBaseButton-primary"]
  [data-testid="stIconMaterial"] {{ color:var(--a); }}
/* The middle cell of the size strip is the current value AND the reset control:
   the +/- steps are relative to the 100% it returns to, so the number and the
   thing that restores it are the same object. */
/* Needs the sidebar prefix: `section[...] .stButton button` outranks a bare
   `.st-key-* button`, so without it the font-size here silently does nothing. */
section[data-testid="stSidebar"] .st-key-size_reset button {{
  font-variant-numeric:tabular-nums; font-size:calc(11.5px*var(--s)) !important;
  color:var(--fg2) !important; letter-spacing:.04em; }}
section[data-testid="stSidebar"] .st-key-size_reset button:hover {{
  color:var(--a) !important; }}
/* the value cell sits flush between the two buttons */
.st-key-size_seg [data-testid="stColumn"]:nth-child(2) [data-testid="stElementContainer"] {{
  min-height:0 !important; }}

.opt-hint {{ font-size:calc(9.5px*var(--s)) !important; color:var(--m2); line-height:1.55 !important;
            margin:0; padding:2px 0 8px; }}
.opt-row-lbl {{ font-size:calc(9px*var(--s)) !important; letter-spacing:.2em; text-transform:uppercase;
               color:var(--m2); margin:0; padding:12px 0 3px; }}
{motion}

/* --- base-colour palette: five joined chips, a real connected strip --- */
.st-key-base_seg [data-testid="stHorizontalBlock"] {{ gap:0 !important; }}
.st-key-base_seg [data-testid="stColumn"] {{ min-width:0 !important; }}
.st-key-base_seg [data-testid="stColumn"] > div,
.st-key-base_seg [data-testid="stElementContainer"],
.st-key-base_seg .stButton {{ width:100% !important; display:block !important; }}
.st-key-base_seg .stButton button {{
  width:100% !important; padding:0 !important; height:calc(26px*var(--s));
  border-radius:0 !important; border:1px solid var(--r) !important;
  margin-left:-1px !important; box-shadow:none !important; }}
.st-key-base_seg [data-testid="stColumn"]:first-child .stButton button {{
  border-radius:4px 0 0 4px !important; margin-left:0 !important; }}
.st-key-base_seg [data-testid="stColumn"]:last-child .stButton button {{
  border-radius:0 4px 4px 0 !important; }}
.st-key-base_seg .stButton button:hover {{ z-index:1; filter:brightness(1.12); }}
.st-key-base_seg .stButton button[data-testid="stBaseButton-primary"] {{
  z-index:2; outline:2px solid var(--fg); outline-offset:-3px; }}

/* --- daily quote under the name --- */
.quote {{ margin:0; padding:8px 0 2px; }}
/* Literal characters, not CSS \201C escapes — those get mangled on the way
   through the f-string and render as "·C" / "·D". */
.quote q {{ display:block; font-size:calc(11px*var(--s)) !important; color:var(--fg2);
  line-height:1.65 !important; font-style:italic; quotes:none; }}
.quote q::before {{ content:"“"; }}
.quote q::after  {{ content:"”"; }}
.quote cite {{ display:block; font-size:calc(9.5px*var(--s)) !important; color:var(--m2);
  font-style:normal; letter-spacing:.08em; text-transform:uppercase; padding-top:5px; }}

/* --- contact row: icon links --- */
.contact {{ display:flex; justify-content:space-between; gap:8px; padding:5px 0 3px; }}
.contact a {{ flex:1 1 0; min-width:0; display:inline-flex; align-items:center;
  justify-content:center; height:calc(38px*var(--s)); border:1px solid var(--r);
  border-radius:5px; color:var(--m); text-decoration:none !important; }}
.contact a:hover {{ color:var(--a); border-color:var(--a); background:var(--hv); }}
.contact a:focus-visible {{ outline:2px solid var(--a); outline-offset:2px; }}
.contact svg {{ width:calc(20px*var(--s)); height:calc(20px*var(--s)); fill:currentColor;
  display:block; }}
</style>
"""
