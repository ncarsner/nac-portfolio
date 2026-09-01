"""
VARIANT B — "Workbench"

Thesis: the portfolio IS the app. A sidebar catalogs every artifact; the main
pane runs the selected one at full size. Prose is the fallback for things that
cannot run, not the default presentation.

Structurally: two-pane app shell with persistent navigation and selection state.
The bet is that a working thing on screen outsells a paragraph about it.
"""
import streamlit as st
from content import SITE, ARTIFACTS, KIND_LABEL, get
import embeds

NAME = "Workbench — two-pane live artifact viewer"

CSS = """
<style>
section[data-testid="stSidebar"] { border-right:1px solid var(--r); }
section[data-testid="stSidebar"] > div { padding-top:18px; }
.wb { padding-bottom:120px; }
.who { font-size:15px; font-weight:650; letter-spacing:-.01em; }
.who span { display:block; font-size:11.5px; font-weight:400; color:var(--m);
            margin-top:3px; line-height:1.5; }
.grp { font-size:9.5px; letter-spacing:.2em; text-transform:uppercase; color:var(--m2);
       margin:20px 0 7px; }
section[data-testid="stSidebar"] .stButton > button {
  width:100%; text-align:left; justify-content:flex-start; background:transparent;
  border:1px solid transparent; border-radius:7px; padding:6px 10px; min-height:0;
  font-size:13px; color:var(--fg); font-weight:450; line-height:1.35; }
section[data-testid="stSidebar"] .stButton > button:hover { background:var(--hv); border-color:var(--r); }
section[data-testid="stSidebar"] .stButton > button[kind="primary"],
section[data-testid="stSidebar"] .stButton > button[data-testid="stBaseButton-primary"] {
  background:var(--sel); border-color:var(--a); color:var(--fg); font-weight:600; }
.ttl { display:flex; align-items:baseline; gap:12px; flex-wrap:wrap; }
.ttl h2 { font-size:26px; margin:0; letter-spacing:-.02em; font-weight:680; }
.pill { font-size:10px; letter-spacing:.1em; text-transform:uppercase; color:var(--m);
        border:1px solid var(--r); border-radius:999px; padding:2px 9px; }
.pill.live { color:#2ea043; border-color:#2ea04366; background:#2ea04314; }
.sub { color:var(--m); font-size:14px; margin:9px 0 0; line-height:1.6; max-width:62ch; }
.mets { display:flex; gap:0; margin:20px 0 4px; border:1px solid var(--r); border-radius:9px;
        overflow:hidden; }
.met { flex:1; padding:11px 14px; border-right:1px solid var(--r); }
.met:last-child { border-right:none; }
.met b { display:block; font-size:18px; font-weight:640; letter-spacing:-.02em;
         font-family:ui-monospace,Menlo,monospace; }
.met span { font-size:10px; letter-spacing:.12em; text-transform:uppercase; color:var(--m2); }
.stagelbl { font-size:9.5px; letter-spacing:.2em; text-transform:uppercase; color:var(--m2);
            margin:26px 0 8px; display:flex; align-items:center; gap:9px; }
.stagelbl:after { content:""; flex:1; height:1px; background:var(--r); }
.fact { display:flex; gap:9px; font-size:12.5px; padding:6px 0; border-bottom:1px solid var(--r2); }
.fact .k { color:var(--m2); width:74px; flex:none; }
.pr { font-size:14px; line-height:1.75; color:var(--fg2); max-width:66ch; margin:0 0 13px; }
.lk a { display:inline-block; font-size:12.5px; color:var(--a); text-decoration:none;
        border:1px solid var(--r); border-radius:7px; padding:5px 12px; margin:0 7px 7px 0; }
.lk a:hover { border-color:var(--a); background:var(--hv); }
:root { --r:#2a2f36; --r2:#1e2228; --m:#8b949e; --m2:#6e7681; --a:#79b8ff;
        --hv:#161b22; --sel:#1f6feb26; --fg:#e6edf3; --fg2:#c9d1d9; }
@media (prefers-color-scheme: light) {
  :root { --r:#d8dee4; --r2:#eaeef2; --m:#57606a; --m2:#8c959f; --a:#0969da;
          --hv:#f6f8fa; --sel:#0969da1a; --fg:#1f2328; --fg2:#32383f; }
}
</style>
"""

ORDER = ["app", "package", "site", "writing"]


def render():
    st.markdown(CSS, unsafe_allow_html=True)
    st.session_state.setdefault("wb_sel", ARTIFACTS[0]["id"])

    with st.sidebar:
        st.markdown(
            f'<div class="who">{SITE["name"]}<span>{SITE["tagline"]}</span></div>',
            unsafe_allow_html=True,
        )
        for kind in ORDER:
            items = [a for a in ARTIFACTS if a["kind"] == kind]
            if not items:
                continue
            st.markdown(f'<div class="grp">{KIND_LABEL[kind]}s</div>', unsafe_allow_html=True)
            for a in items:
                sel = a["id"] == st.session_state.wb_sel
                mark = "● " if a.get("embed") else "○ "
                if st.button(mark + a["name"], key=f"wb_{a['id']}",
                             type="primary" if sel else "secondary"):
                    st.session_state.wb_sel = a["id"]
                    st.rerun()
        st.markdown('<div class="grp">Contact</div>', unsafe_allow_html=True)
        st.markdown(
            " · ".join(f"[{k.lower()}]({u})" for k, u in SITE["links"].items()),
            unsafe_allow_html=True,
        )

    a = get(st.session_state.wb_sel)
    st.markdown('<div class="wb">', unsafe_allow_html=True)

    live = "live" if a.get("embed") else ""
    st.markdown(
        f'<div class="ttl"><h2>{a["name"]}</h2>'
        f'<span class="pill {live}">{a["status"]}</span>'
        f'<span class="pill">{KIND_LABEL[a["kind"]]}</span>'
        f'<span class="pill">{a["year"]}</span></div>'
        f'<p class="sub">{a["one_liner"]}</p>',
        unsafe_allow_html=True,
    )

    if a.get("metrics"):
        st.markdown(
            '<div class="mets">'
            + "".join(f'<div class="met"><b>{v}</b><span>{k}</span></div>'
                      for k, v in a["metrics"].items())
            + "</div>",
            unsafe_allow_html=True,
        )

    # The main event: run the thing.
    if a.get("embed"):
        st.markdown('<div class="stagelbl">Running now</div>', unsafe_allow_html=True)
        embeds.render(st, a["embed"], height=470)
    elif a.get("install"):
        st.markdown('<div class="stagelbl">Use it</div>', unsafe_allow_html=True)
        st.code(a["install"], language="bash")
        st.code(a["sample"], language="python")
    else:
        st.markdown('<div class="stagelbl">Preview</div>', unsafe_allow_html=True)
        st.image(embeds.placeholder(a["name"], a["one_liner"][:64]), width='stretch')

    left, right = st.columns([1.65, 1], gap="large")
    with left:
        st.markdown('<div class="stagelbl">Notes</div>', unsafe_allow_html=True)
        for p in a["prose"]:
            st.markdown(f'<p class="pr">{p}</p>', unsafe_allow_html=True)
        st.markdown(
            '<div class="lk">'
            + "".join(f"<a href='{u}' target='_blank'>{k} ↗</a>" for k, u in a["links"].items())
            + "</div>",
            unsafe_allow_html=True,
        )
    with right:
        st.markdown('<div class="stagelbl">Facts</div>', unsafe_allow_html=True)
        facts = [("Role", a["role"]), ("Year", a["year"]), ("Status", a["status"])]
        if a["stack"]:
            facts.append(("Stack", ", ".join(a["stack"])))
        facts.append(("Tags", ", ".join(a["tags"])))
        st.markdown(
            "".join(f'<div class="fact"><span class="k">{k}</span><span>{v}</span></div>'
                    for k, v in facts),
            unsafe_allow_html=True,
        )

    st.markdown("</div>", unsafe_allow_html=True)
