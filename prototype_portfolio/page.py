"""
PROTOTYPE — the settled page.

Rounds 1-4 fixed all of this, so it no longer varies:
  layout   Workbench — sidebar catalogue, main pane runs the selected artifact
  language Instrument — dense, monospace, hairline rules, no decoration
  tone     Slate by default, now switchable by the viewer

The only thing still under evaluation is how the OPTIONS PANEL presents itself,
so render() takes a `panel` callable and the variants supply just that.
"""
import html as _html

import streamlit as st
from content import SITE, ARTIFACTS, KIND_LABEL, get
import embeds
import theme

ORDER = ["app", "package", "site", "writing"]


def selection():
    st.session_state.setdefault("wb_sel", ARTIFACTS[0]["id"])
    return get(st.session_state.wb_sel)


def pre(code, cls=""):
    return f'<pre class="code {cls}"><code>{_html.escape(code)}</code></pre>'


def _nav():
    for kind in ORDER:
        items = [a for a in ARTIFACTS if a["kind"] == kind]
        if not items:
            continue
        st.markdown(f'<div class="grp">{KIND_LABEL[kind]}s</div>', unsafe_allow_html=True)
        for a in items:
            sel = a["id"] == st.session_state.wb_sel
            dot = "● " if a.get("embed") else "○ "
            if st.button(dot + a["name"], key=f"nav_{a['id']}",
                         type="primary" if sel else "secondary"):
                st.session_state.wb_sel = a["id"]
                st.rerun()


def _stage(a, s):
    if a.get("embed"):
        embeds.render(st, a["embed"], tone=s["tone"], motion=s["motion"])
    elif a.get("install"):
        st.markdown(pre(a["install"], "cmd") + pre(a["sample"]), unsafe_allow_html=True)
    else:
        tint = {"slate": "#24405f", "fog": "#3a5372", "ash": "#31506f"}[s["tone"]]
        st.image(embeds.placeholder(a["name"], a["one_liner"][:64], a=tint), width="stretch")


def _facts(a):
    f = [("Role", a["role"]), ("Year", a["year"]), ("Status", a["status"])]
    if a["stack"]:
        f.append(("Stack", ", ".join(a["stack"])))
    f.append(("Tags", ", ".join(a["tags"])))
    return f


def render(panel):
    """panel: callable taking the settings dict, drawn in the sidebar's lower left."""
    s = theme.state()
    st.markdown(theme.css(s), unsafe_allow_html=True)
    a = selection()

    with st.sidebar:
        st.markdown(f'<div class="who">{SITE["name"]}<span>{SITE["tagline"]}</span></div>',
                    unsafe_allow_html=True)
        _nav()
        st.markdown('<div class="grp">Contact</div>', unsafe_allow_html=True)
        st.markdown(" · ".join(f"[{k.lower()}]({u})" for k, u in SITE["links"].items()),
                    unsafe_allow_html=True)
        panel(s)   # <- the part still being prototyped

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

    label = "Running now" if a.get("embed") else "Use it" if a.get("install") else "Preview"
    st.markdown(f'<div class="lbl">{label}</div>', unsafe_allow_html=True)
    _stage(a, s)

    left, right = st.columns([1.7, 1], gap="large")
    with left:
        st.markdown('<div class="lbl">Notes</div>', unsafe_allow_html=True)
        for p in a["prose"]:
            st.markdown(f'<p class="pr">{p}</p>', unsafe_allow_html=True)
        st.markdown('<div class="lk">' + "".join(
            f"<a href='{u}' target='_blank'>{k} →</a>" for k, u in a["links"].items()
        ) + "</div>", unsafe_allow_html=True)
    with right:
        st.markdown('<div class="lbl">Facts</div>', unsafe_allow_html=True)
        st.markdown("".join(
            f'<div class="kv"><span class="k">{k}</span><span class="v">{v}</span></div>'
            for k, v in _facts(a)), unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
