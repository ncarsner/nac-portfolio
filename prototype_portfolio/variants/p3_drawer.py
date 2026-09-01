"""
PANEL 3 — "Drawer"

One "Appearance" row that opens a drawer. Closed by default, showing only a
summary of what is currently active, so the settings occupy a single line until
someone actually wants them.

Bets that a portfolio's sidebar belongs to the work, not to its own controls —
most visitors never touch the theme, and the ones who need accessibility options
are used to looking for exactly this affordance.
"""
import streamlit as st
import theme

NAME = "Drawer — collapsed to one row until opened"

CSS = """
<style>
.st-key-opt_drawer { border-top:1px solid var(--r); margin-top:16px; padding-top:8px; }
.st-key-opt_drawer .stButton button { padding:4px 8px !important; }
.st-key-drawer_body { border-left:2px solid var(--r); margin:4px 0 0 7px; padding-left:8px; }
.st-key-drawer_body [data-testid="stHorizontalBlock"] { gap:4px; }
.st-key-drawer_body button { font-size:calc(11px*var(--s)) !important; }
.drw-sum { font-size:calc(9.5px*var(--s)) !important; color:var(--m2); margin:0;
           padding:1px 0 4px 30px; line-height:1.5 !important; }
</style>
"""

TOGGLES = [
    ("contrast",  "High contrast",   "contrast"),
    ("readable",  "Readable font",   "text_fields"),
    ("underline", "Underline links", "format_underlined"),
]


def _summary(s):
    bits = [theme.PALETTES[s["tone"]]["label"]]
    if s["text"] != "normal":
        bits.append(theme.TEXT_SIZES[s["text"]][0].lower() + " text")
    if s["contrast"]:
        bits.append("high contrast")
    if s["readable"]:
        bits.append("readable font")
    if s["underline"]:
        bits.append("underlined links")
    if not s["motion"]:
        bits.append("reduced motion")
    return " · ".join(bits)


def panel(s):
    st.markdown(CSS, unsafe_allow_html=True)
    st.session_state.setdefault("drawer_open", False)
    open_ = st.session_state.drawer_open

    with st.container(key="opt_drawer"):
        if st.button("Appearance", key="drawer_toggle",
                     icon=f":material/{'expand_more' if open_ else 'chevron_right'}:",
                     help="Theme and accessibility options"):
            st.session_state.drawer_open = not open_
            st.rerun()
        st.markdown(f'<div class="drw-sum">{_summary(s)}</div>', unsafe_allow_html=True)

        if not open_:
            return

        with st.container(key="drawer_body"):
            st.markdown('<div class="opt-row-lbl">Theme</div>', unsafe_allow_html=True)
            for k, p in theme.PALETTES.items():
                if st.button(p["label"], key=f"tone_{k}", help=p["hint"],
                             icon=f':material/{p["icon"]}:',
                             type="primary" if s["tone"] == k else "secondary"):
                    theme.set_opt("tone", k)

            st.markdown('<div class="opt-row-lbl">Text size</div>', unsafe_allow_html=True)
            cols = st.columns(len(theme.TEXT_SIZES))
            for col, (k, (lab, _)) in zip(cols, theme.TEXT_SIZES.items()):
                with col:
                    if st.button(lab, key=f"size_{k}",
                                 type="primary" if s["text"] == k else "secondary"):
                        theme.set_opt("text", k)

            st.markdown('<div class="opt-row-lbl">Accessibility</div>', unsafe_allow_html=True)
            for key, label, icon in TOGGLES:
                if st.button(label, key=f"tg_{key}", icon=f":material/{icon}:",
                             type="primary" if s[key] else "secondary"):
                    theme.toggle(key)
            if st.button("Reduce motion", key="tg_motion", icon=":material/animation:",
                         type="primary" if not s["motion"] else "secondary"):
                theme.toggle("motion")

            if not theme.is_default(s):
                if st.button("Reset to defaults", key="opt_reset",
                             icon=":material/restart_alt:"):
                    theme.reset()
