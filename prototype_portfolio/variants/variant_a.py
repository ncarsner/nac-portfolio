"""
VARIANT A — "Index"

Thesis: your reader is a peer or a hiring engineer who already knows what they
are looking for. Give them the whole inventory on one screen, in one column, with
no hero and no scrolling ceremony. Live demos are one click deep, never in the way.

Structurally: flat list. No cards, no grid, no sidebar, no images above the fold.
"""
import streamlit as st
from content import SITE, ARTIFACTS, TIMELINE, KIND_LABEL
import embeds

NAME = "Index — dense text-first listing"

CSS = """
<style>
.blk { max-width: 780px; margin: 0 auto; padding-bottom: 120px; }
.blk, .blk * { font-family: ui-monospace, SFMono-Regular, Menlo, monospace; }
.hd { display:flex; justify-content:space-between; align-items:baseline;
      border-bottom:1px solid var(--r); padding-bottom:10px; margin-bottom:8px; }
.hd h1 { font-size:15px; margin:0; font-weight:600; letter-spacing:.02em; }
.hd .loc { font-size:12px; color:var(--m); }
.lede { font-size:13px; color:var(--m); line-height:1.7; margin:14px 0 6px; }
.lnks { font-size:12px; margin:10px 0 30px; }
.lnks a { color:var(--a); text-decoration:none; margin-right:16px; border-bottom:1px solid transparent; }
.lnks a:hover { border-bottom-color:var(--a); }
.sec { font-size:10px; letter-spacing:.22em; text-transform:uppercase; color:var(--m);
       margin:34px 0 4px; padding-bottom:6px; border-bottom:1px solid var(--r); }
.row { display:grid; grid-template-columns:58px 1fr; gap:14px;
       padding:11px 0; border-bottom:1px solid var(--r2); }
.row:hover { background:var(--hv); }
.yr { color:var(--m); font-size:12px; padding-top:1px; }
.nm { font-size:13px; font-weight:600; }
.nm .kind { color:var(--m); font-weight:400; font-size:11px; margin-left:8px;
            border:1px solid var(--r); border-radius:3px; padding:1px 5px; }
.ol { font-size:12.5px; color:var(--m); line-height:1.6; margin-top:3px; }
.mt { font-size:11px; color:var(--m2); margin-top:5px; }
.mt a { color:var(--a); text-decoration:none; }
.mt a:hover { text-decoration:underline; }
.mt .sep { opacity:.4; margin:0 7px; }
.tl { display:grid; grid-template-columns:104px 1fr; gap:14px; padding:9px 0;
      border-bottom:1px solid var(--r2); font-size:12.5px; }
.tl .co { color:var(--m); }
:root { --r:#2a2f36; --r2:#1e2228; --m:#8b949e; --m2:#6e7681; --a:#79b8ff; --hv:#14181d; }
@media (prefers-color-scheme: light) {
  :root { --r:#d8dee4; --r2:#eaeef2; --m:#57606a; --m2:#8c959f; --a:#0969da; --hv:#f6f8fa; }
}
</style>
"""


def _row(a):
    links = " <span class='sep'>·</span> ".join(
        f"<a href='{u}' target='_blank'>{k.lower()}</a>" for k, u in a["links"].items()
    )
    tags = " ".join(a["tags"])
    return f"""
<div class="row">
  <div class="yr">{a['year']}</div>
  <div>
    <div class="nm">{a['name']}<span class="kind">{KIND_LABEL[a['kind']]}</span></div>
    <div class="ol">{a['one_liner']}</div>
    <div class="mt">{tags} <span class="sep">·</span> {a['role']} <span class="sep">·</span> {a['status']}
      <span class="sep">·</span> {links}</div>
  </div>
</div>"""


def render():
    st.markdown(CSS, unsafe_allow_html=True)
    s = SITE

    head = f"""<div class="blk">
  <div class="hd"><h1>{s['name']} — {s['role'].lower()}</h1><div class="loc">{s['location']}</div></div>
  <div class="lede">{s['blurb']}</div>
  <div class="lnks">{''.join(f"<a href='{u}' target='_blank'>{k.lower()}</a>" for k, u in s['links'].items())}</div>
  <div class="sec">Work · {len(ARTIFACTS)} items</div>
  {''.join(_row(a) for a in ARTIFACTS)}
</div>"""
    st.markdown(head, unsafe_allow_html=True)

    # Live demos stay collapsed — the index is the point, the demo is the follow-up.
    st.markdown('<div class="blk"><div class="sec">Run it</div></div>', unsafe_allow_html=True)
    for a in ARTIFACTS:
        if a.get("embed"):
            with st.expander(f"{a['name']} — {a['one_liner']}", expanded=False):
                embeds.render(st, a["embed"])
        elif a.get("install"):
            with st.expander(f"{a['name']} — {a['one_liner']}", expanded=False):
                st.code(a["install"], language="bash")
                st.code(a["sample"], language="python")

    tl = "".join(
        f"<div class='tl'><div class='co'>{when}</div><div><b>{role}</b>, {org}"
        f"<div class='ol'>{note}</div></div></div>"
        for when, role, org, note in TIMELINE
    )
    st.markdown(
        f'<div class="blk"><div class="sec">Positions</div>{tl}'
        f'<div class="mt" style="margin-top:26px">Last updated 2026 · built with too much monospace</div></div>',
        unsafe_allow_html=True,
    )
