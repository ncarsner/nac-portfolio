"""
The options panel — "Drawer", chosen in round 5.

Collapsed to a single "Appearance" line with a summary of what is active, so the
sidebar belongs to the work until someone actually wants the controls.

Two refinements on the chosen design:
  * the three modes are ICON ONLY, joined into one segmented control. Dark, mid
    and light are legible from a moon / half / sun without reading anything, and
    the colour names were arbitrary. The names survive only for screen readers.
  * text size is a Word-style stepper — minus, current size, plus — over five
    fixed steps rather than three named presets.

Every icon-only control carries an accessible name; see a11y.py.
"""
import streamlit as st
import a11y
import theme

CSS = """
<style>
.st-key-opt_drawer { border-top:1px solid var(--r); padding-top:8px; }
.st-key-opt_drawer .stButton button { padding:4px 8px !important; }
.st-key-drawer_body { border-left:2px solid var(--r); margin:4px 0 0 7px; padding-left:8px; }
.drw-sum { font-size:calc(9.5px*var(--s)) !important; color:var(--m2); margin:0;
           padding:1px 0 4px 30px; line-height:1.5 !important; }
</style>
"""

TOGGLES = [
    ("contrast",  "High contrast",   "contrast",
     "Stronger text and borders."),
    ("readable",  "Readable font",   "text_fields",
     "A wider sans face instead of monospace."),
    ("underline", "Underline links", "format_underlined",
     "Do not signal links by colour alone."),
]


def _modes(s):
    """Three icon-only buttons, joined into one segmented control."""
    with st.container(key="mode_seg"):
        cols = st.columns(len(theme.PALETTES))
        for col, (k, p) in zip(cols, theme.PALETTES.items()):
            with col:
                if st.button("", key=f"tone_{k}", icon=f':material/{p["icon"]}:',
                             type="primary" if s["tone"] == k else "secondary"):
                    theme.set_opt("tone", k)


def _size(s):
    """Minus / current / plus, the Word idiom. Ends disable rather than wrap —
    wrapping from largest back to smallest would be a nasty surprise."""
    i = s["text_idx"]
    with st.container(key="size_seg"):
        dec, val, inc = st.columns([1, 1.4, 1])
        with dec:
            if st.button("", key="size_dec", icon=":material/text_decrease:",
                         disabled=i == 0):
                theme.step_text(-1)
        with val:
            st.markdown(f'<p class="seg-val">{theme.text_pct(i)}</p>',
                        unsafe_allow_html=True)
        with inc:
            if st.button("", key="size_inc", icon=":material/text_increase:",
                         disabled=i == len(theme.TEXT_STEPS) - 1):
                theme.step_text(1)


def render(s):
    st.markdown(CSS, unsafe_allow_html=True)
    st.session_state.setdefault("drawer_open", False)
    open_ = st.session_state.drawer_open

    with st.container(key="opt_drawer"):
        if st.button("Appearance", key="drawer_toggle",
                     icon=f":material/{'expand_more' if open_ else 'chevron_right'}:"):
            st.session_state.drawer_open = not open_
            st.rerun()
        st.markdown(f'<div class="drw-sum">{theme.summary(s)}</div>',
                    unsafe_allow_html=True)

        if open_:
            with st.container(key="drawer_body"):
                st.markdown('<div class="opt-row-lbl">Mode</div>', unsafe_allow_html=True)
                _modes(s)
                st.markdown('<div class="opt-row-lbl">Text size</div>', unsafe_allow_html=True)
                _size(s)
                st.markdown('<div class="opt-row-lbl">Accessibility</div>',
                            unsafe_allow_html=True)
                for key, label, icon, hint in TOGGLES:
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

    # Accessible names for the icon-only controls, plus the live announcement.
    a11y.emit(s, drawer_open=open_)
