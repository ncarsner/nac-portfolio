"""
PANEL 2 — "List"

Everything as full-width icon + label rows, styled exactly like the artifact nav
above it. Tone options carry a contextual icon (moon / gradient / sun) rather
than a colour chip; toggles carry their own subject icon and show state through
the same selected treatment the nav uses.

Bets that one consistent row idiom down the whole sidebar beats a second visual
language for settings — nothing new to learn, and it scales if more options land.
"""
import streamlit as st
import theme

NAME = "List — one row idiom, icon per option"

CSS = """
<style>
.st-key-opt_list .stButton button { padding:4px 8px !important; }
.st-key-opt_list [data-testid="stIconMaterial"] {
  font-size:calc(15px*var(--s)) !important; margin-right:2px; }
.st-key-opt_list .stButton button[kind="primary"] [data-testid="stIconMaterial"],
.st-key-opt_list .stButton button[data-testid="stBaseButton-primary"] [data-testid="stIconMaterial"] {
  color:var(--a) !important; }
</style>
"""

TOGGLES = [
    ("contrast",  "High contrast",   "contrast",          "Stronger text and borders."),
    ("readable",  "Readable font",   "text_fields",       "Wider sans instead of monospace."),
    ("underline", "Underline links", "format_underlined", "Do not signal links by colour alone."),
]


def panel(s):
    st.markdown(CSS, unsafe_allow_html=True)
    with st.container(key="opt_list"):
        st.markdown('<div class="grp">Theme</div>', unsafe_allow_html=True)
        for k, p in theme.PALETTES.items():
            if st.button(p["label"], key=f"tone_{k}", help=p["hint"],
                         icon=f':material/{p["icon"]}:',
                         type="primary" if s["tone"] == k else "secondary"):
                theme.set_opt("tone", k)

        st.markdown('<div class="grp">Accessibility</div>', unsafe_allow_html=True)
        for k, (lab, _) in theme.TEXT_SIZES.items():
            if st.button(f"Text: {lab}", key=f"size_{k}",
                         icon=":material/format_size:",
                         type="primary" if s["text"] == k else "secondary"):
                theme.set_opt("text", k)

        for key, label, icon, hint in TOGGLES:
            if st.button(label, key=f"tg_{key}", help=hint, icon=f":material/{icon}:",
                         type="primary" if s[key] else "secondary"):
                theme.toggle(key)

        if st.button("Reduce motion", key="tg_motion", icon=":material/animation:",
                     help="Stop the live demos animating.",
                     type="primary" if not s["motion"] else "secondary"):
            theme.toggle("motion")

        if not theme.is_default(s):
            if st.button("Reset to defaults", key="opt_reset", icon=":material/restart_alt:"):
                theme.reset()
