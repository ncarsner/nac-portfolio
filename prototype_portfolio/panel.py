"""
The options panel.

Round 6 refinement: the two controls people actually reach for — mode and text
size — are ALWAYS VISIBLE. Everything else lives behind "Appearance Options",
collapsed, because it is set once and then forgotten.

Inside that section, the colour base is a connected strip of five chips painted
with the accent each one produces in the current mode, so the choice is made by
looking rather than by reading a name.
"""
import streamlit as st
import a11y
import theme

CSS = """
<style>
.st-key-opt_always { border-top:1px solid var(--r); padding-top:10px; }
.st-key-opt_drawer .stButton button { padding:4px 8px !important; }
.st-key-drawer_body { border-left:2px solid var(--r); margin:4px 0 0 7px; padding-left:8px; }
.drw-sum { font-size:calc(9.5px*var(--s)) !important; color:var(--m2); margin:0;
           padding:1px 0 4px 30px; line-height:1.5 !important; }
</style>
"""

TOGGLES = [
    ("contrast",  "High contrast",   "contrast"),
    ("readable",  "Readable font",   "text_fields"),
    ("underline", "Underline links", "format_underlined"),
]


def _modes(s):
    with st.container(key="mode_seg"):
        for col, (k, m) in zip(st.columns(len(theme.MODES)), theme.MODES.items()):
            with col:
                if st.button("", key=f"mode_{k}", icon=f':material/{m["icon"]}:',
                             type="primary" if s["mode"] == k else "secondary"):
                    theme.set_opt("mode", k)


def _size(s):
    """Minus / current / plus. Ends disable rather than wrap — wrapping from the
    largest size back to the smallest would be a nasty surprise."""
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
                         disabled=i == len(theme.TEXT_PCTS) - 1):
                theme.step_text(1)


def _bases(s):
    """Five chips, joined, each painted with the accent it actually yields in
    the current mode."""
    st.markdown(
        "<style>" + "".join(
            f'.st-key-base_{k} button {{ background:{theme.swatch(k, s["mode"])} !important; }}'
            for k in theme.BASES
        ) + "</style>", unsafe_allow_html=True)
    with st.container(key="base_seg"):
        for col, (k, b) in zip(st.columns(len(theme.BASES)), theme.BASES.items()):
            with col:
                if st.button("", key=f"base_{k}",
                             type="primary" if s["base"] == k else "secondary"):
                    theme.set_opt("base", k)


def render(s):
    st.markdown(CSS, unsafe_allow_html=True)
    st.session_state.setdefault("drawer_open", False)
    open_ = st.session_state.drawer_open

    # Always visible: the two controls people actually reach for.
    with st.container(key="opt_always"):
        st.markdown('<div class="opt-row-lbl">Mode</div>', unsafe_allow_html=True)
        _modes(s)
        st.markdown('<div class="opt-row-lbl">Text size</div>', unsafe_allow_html=True)
        _size(s)

    # Set-once-and-forget: behind a disclosure.
    with st.container(key="opt_drawer"):
        if st.button("Appearance Options", key="drawer_toggle",
                     icon=f":material/{'expand_more' if open_ else 'chevron_right'}:"):
            st.session_state.drawer_open = not open_
            st.rerun()
        st.markdown(f'<div class="drw-sum">{theme.summary(s)}</div>',
                    unsafe_allow_html=True)

        if open_:
            with st.container(key="drawer_body"):
                st.markdown('<div class="opt-row-lbl">Colour base</div>',
                            unsafe_allow_html=True)
                _bases(s)
                st.markdown('<div class="opt-row-lbl">Accessibility</div>',
                            unsafe_allow_html=True)
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

    a11y.emit(s, drawer_open=open_)
