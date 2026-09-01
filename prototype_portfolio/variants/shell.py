"""
PROTOTYPE round 2 — the settled layout, expressed once.

Round 1 decided the SKELETON (variant B, "Workbench"): a sidebar cataloguing
every artifact, a main pane that runs the selected one full size. That is no
longer in question, so it lives here as a fixed running order and every variant
draws exactly these blocks, in exactly this sequence:

    sidebar : identity → grouped artifact nav → contact
    main    : title block → metrics → stage (the artifact, running) → notes | facts

What each variant is free to change is everything about how those blocks LOOK —
typography, density, colour, and how the title block and metrics are treated.
Each variant therefore owns its own CSS and its own renderers for the blocks;
this module only holds the running order and the bits with no visual opinion,
so the three stay honestly comparable.
"""
import streamlit as st
from content import SITE, ARTIFACTS, KIND_LABEL, get
import embeds

ORDER = ["app", "package", "site", "writing"]


def selection():
    """The selected artifact. In-memory only — nothing is persisted."""
    st.session_state.setdefault("wb_sel", ARTIFACTS[0]["id"])
    return get(st.session_state.wb_sel)


def nav(label_fn=None, marker=True):
    """Sidebar artifact list, grouped by kind. Styling comes from the variant CSS."""
    for kind in ORDER:
        items = [a for a in ARTIFACTS if a["kind"] == kind]
        if not items:
            continue
        st.markdown(f'<div class="grp">{KIND_LABEL[kind]}s</div>', unsafe_allow_html=True)
        for a in items:
            sel = a["id"] == st.session_state.wb_sel
            dot = ("● " if a.get("embed") else "○ ") if marker else ""
            text = label_fn(a) if label_fn else a["name"]
            if st.button(dot + text, key=f"nav_{a['id']}",
                         type="primary" if sel else "secondary"):
                st.session_state.wb_sel = a["id"]
                st.rerun()


def stage(a, height=470, placeholder_tint="#1f6feb"):
    """Run the artifact. This is the block round 1 was won on — never a thumbnail."""
    if a.get("embed"):
        embeds.render(st, a["embed"], height=height)
    elif a.get("install"):
        st.code(a["install"], language="bash")
        st.code(a["sample"], language="python")
    else:
        st.image(embeds.placeholder(a["name"], a["one_liner"][:64], a=placeholder_tint),
                 width="stretch")


def stage_label(a):
    return "Running now" if a.get("embed") else "Use it" if a.get("install") else "Preview"


def facts(a):
    f = [("Role", a["role"]), ("Year", a["year"]), ("Status", a["status"])]
    if a["stack"]:
        f.append(("Stack", ", ".join(a["stack"])))
    f.append(("Tags", ", ".join(a["tags"])))
    return f


def links_html(a, arrow="↗"):
    return "".join(f"<a href='{u}' target='_blank'>{k} {arrow}</a>"
                   for k, u in a["links"].items())


def contact_md():
    return " · ".join(f"[{k.lower()}]({u})" for k, u in SITE["links"].items())
