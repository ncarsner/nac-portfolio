"""
PANEL 1 — "Swatches"

Tone as three colour chips in a row, each painted with the actual ground it
selects, so the choice is shown rather than described. Accessibility below it as
labelled toggle rows with a check-box icon carrying the state.

Bets that a colour choice should be made by looking at colour, and that the
compact row keeps the panel from crowding the nav above it.
"""
import streamlit as st
import theme

NAME = "Swatches — colour chips + toggle rows"

# Paint each chip with the ground it selects. Keyed CSS is the only way to reach
# an individual Streamlit button.
# A chip carries its own label rather than being an empty coloured box: an
# unlabelled control in an accessibility panel would be a poor joke.
CSS = "<style>" + "".join(
    f'.st-key-tone_{k} button {{ background:{p["swatch"]} !important;'
    f' color:{p["on_swatch"]} !important; width:100% !important;'
    f' border:2px solid var(--r) !important; border-radius:4px !important;'
    f' height:34px; justify-content:center !important; padding:0 !important;'
    f' font-size:calc(10.5px*var(--s)) !important; letter-spacing:.06em; }}'
    f'.st-key-tone_{k} button:hover {{ border-color:var(--a) !important; }}'
    f'.st-key-tone_{k} button[kind="primary"],'
    f'.st-key-tone_{k} button[data-testid="stBaseButton-primary"] {{'
    f' border-color:var(--a) !important; box-shadow:0 0 0 2px var(--sel); }}'
    for k, p in theme.PALETTES.items()
) + """
.st-key-tone_row [data-testid="stHorizontalBlock"] { gap:6px; }
.st-key-size_row [data-testid="stHorizontalBlock"] { gap:4px; }
.st-key-size_row button { justify-content:center !important; font-size:calc(10px*var(--s)) !important; }
</style>"""

TOGGLES = [
    ("contrast",  "High contrast",  "contrast",           "Stronger text and borders."),
    ("readable",  "Readable font",  "text_fields",        "Wider sans instead of monospace."),
    ("underline", "Underline links","format_underlined",  "Do not signal links by colour alone."),
]


def panel(s):
    st.markdown(CSS, unsafe_allow_html=True)
    st.markdown('<div class="grp">Appearance</div>', unsafe_allow_html=True)

    with st.container(key="tone_row"):
        cols = st.columns(len(theme.PALETTES))
        for col, (k, p) in zip(cols, theme.PALETTES.items()):
            with col:
                if st.button(p["label"], key=f"tone_{k}", help=p["hint"],
                             type="primary" if s["tone"] == k else "secondary"):
                    theme.set_opt("tone", k)
    st.markdown(f'<div class="opt-hint">{theme.PALETTES[s["tone"]]["label"]} — '
                f'{theme.PALETTES[s["tone"]]["hint"]}</div>', unsafe_allow_html=True)

    st.markdown('<div class="grp">Accessibility</div>', unsafe_allow_html=True)
    st.markdown('<div class="opt-row-lbl">Text size</div>', unsafe_allow_html=True)
    with st.container(key="size_row"):
        cols = st.columns(len(theme.TEXT_SIZES))
        for col, (k, (lab, _)) in zip(cols, theme.TEXT_SIZES.items()):
            with col:
                if st.button(lab, key=f"size_{k}",
                             type="primary" if s["text"] == k else "secondary"):
                    theme.set_opt("text", k)

    for key, label, icon, hint in TOGGLES:
        on = s[key]
        if st.button(label, key=f"tg_{key}", help=hint,
                     icon=f":material/{'check_box' if on else 'check_box_outline_blank'}:",
                     type="primary" if on else "secondary"):
            theme.toggle(key)

    on = not s["motion"]
    if st.button("Reduce motion", key="tg_motion", help="Stop the live demos animating.",
                 icon=f":material/{'check_box' if on else 'check_box_outline_blank'}:",
                 type="primary" if on else "secondary"):
        theme.toggle("motion")

    if not theme.is_default(s):
        if st.button("Reset", key="opt_reset", icon=":material/restart_alt:"):
            theme.reset()
