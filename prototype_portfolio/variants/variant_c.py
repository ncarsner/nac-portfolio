"""
VARIANT C — "Dispatch"

Thesis: what distinguishes one engineer from another is reasoning, not a list of
repos. So the page is an essay in reverse-chronological order. Each entry argues
something, and the artifact — screenshot, running demo, code — appears inline as
evidence for the argument, always visible, never behind a click.

Structurally: long-form single-column editorial scroll. No sidebar, no catalog,
no cards. Wide margins, serif body text, media in the flow.
"""
import streamlit as st
from content import SITE, ARTIFACTS, TIMELINE, KIND_LABEL
import embeds

NAME = "Dispatch — narrative long-scroll"

CSS = """
<style>
.dp { max-width: 660px; margin: 0 auto; padding-bottom: 130px; }
.dp .nm { font-size:12px; letter-spacing:.24em; text-transform:uppercase;
          color:var(--m2); margin-bottom:44px; }
.dp h1 { font-family:Georgia,'Iowan Old Style',serif; font-size:41px; line-height:1.18;
         letter-spacing:-.02em; font-weight:500; margin:0 0 22px; }
.dp .op { font-family:Georgia,'Iowan Old Style',serif; font-size:18.5px; line-height:1.72;
          color:var(--fg2); margin:0 0 16px; }
.dp .op em { color:var(--fg); font-style:italic; }
.rule { height:1px; background:var(--r); margin:52px 0; }
.ent { margin: 0 0 20px; }
.mh { display:flex; align-items:baseline; gap:11px; margin-bottom:9px; }
.mh .d { font-size:11px; letter-spacing:.16em; text-transform:uppercase; color:var(--m2);
         font-family:ui-monospace,Menlo,monospace; }
.mh .t { font-size:10px; letter-spacing:.1em; text-transform:uppercase; color:var(--m2);
         border:1px solid var(--r); border-radius:999px; padding:1px 8px; }
.ent h2 { font-family:Georgia,'Iowan Old Style',serif; font-size:27px; line-height:1.25;
          font-weight:500; letter-spacing:-.015em; margin:0 0 14px; }
.ent p { font-family:Georgia,'Iowan Old Style',serif; font-size:17px; line-height:1.78;
         color:var(--fg2); margin:0 0 17px; }
.cap { font-size:11.5px; color:var(--m2); margin:9px 0 26px; line-height:1.6;
       font-family:ui-monospace,Menlo,monospace; }
.cap b { color:var(--m); font-weight:500; }
.fl { font-size:12.5px; font-family:ui-monospace,Menlo,monospace; margin:4px 0 0; }
.fl a { color:var(--a); text-decoration:none; margin-right:15px; }
.fl a:hover { text-decoration:underline; }
.bio { display:grid; grid-template-columns:118px 1fr; gap:15px; padding:12px 0;
       border-top:1px solid var(--r2); font-size:13.5px; }
.bio .w { color:var(--m2); font-family:ui-monospace,Menlo,monospace; font-size:11.5px; padding-top:3px; }
.bio .n { color:var(--m); font-size:12.5px; margin-top:3px; line-height:1.6; }
.ft { margin-top:46px; font-size:13px; color:var(--m); line-height:1.9; }
.ft a { color:var(--a); text-decoration:none; margin-right:16px; }
:root { --r:#2a2f36; --r2:#1e2228; --m:#8b949e; --m2:#6e7681; --a:#79b8ff;
        --fg:#e6edf3; --fg2:#bcc6d1; }
@media (prefers-color-scheme: light) {
  :root { --r:#dfe3e8; --r2:#eef1f4; --m:#57606a; --m2:#8c959f; --a:#0969da;
          --fg:#161a1d; --fg2:#3b4249; }
}
</style>
"""

# The narrative only carries so much weight — a few entries, chosen, not all of them.
FEATURED = ["deploy-board", "ledgerkit", "regex-lab", "schema-drift", "gridpaper"]


def render():
    st.markdown(CSS, unsafe_allow_html=True)
    s = SITE

    st.markdown(
        f"""<div class="dp">
  <div class="nm">{s['name']} · {s['location']}</div>
  <h1>{s['tagline']}</h1>
  <p class="op">I have spent seven years finding out that most engineering problems are
    <em>modelling</em> problems wearing a costume. The framework rarely matters. What
    matters is whether the shape of the data admits the bug you are trying to prevent.</p>
  <p class="op">What follows is the work that taught me that, newest first — with the
    reasoning attached, because the reasoning is the part that transfers.</p>
</div>""",
        unsafe_allow_html=True,
    )

    for aid in FEATURED:
        a = next(x for x in ARTIFACTS if x["id"] == aid)
        st.markdown('<div class="dp"><div class="rule"></div>', unsafe_allow_html=True)
        st.markdown(
            f"""<div class="ent">
  <div class="mh"><span class="d">{a['year']}</span>
    <span class="t">{KIND_LABEL[a['kind']]}</span>
    <span class="t">{a['status']}</span></div>
  <h2>{a['one_liner']}</h2>
  {''.join(f'<p>{p}</p>' for p in a['prose'])}
</div></div>""",
            unsafe_allow_html=True,
        )

        # Evidence, inline and always visible.
        if a.get("embed"):
            embeds.render(st, a["embed"], height=440)
            cap = f"<b>{a['name']}</b> — running here, live. {', '.join(a['stack'])}."
        elif a.get("install"):
            st.code(a["sample"], language="python")
            cap = f"<b>{a['name']}</b> — {a['install']}. {', '.join(a['stack'])}."
        else:
            st.image(embeds.placeholder(a["name"], a["one_liner"][:64], a="#2b3444"),
                     width='stretch')
            cap = f"<b>{a['name']}</b> — {', '.join(a['stack']) or a['role']}."

        links = "".join(f"<a href='{u}' target='_blank'>{k} ↗</a>" for k, u in a["links"].items())
        st.markdown(
            f'<div class="dp"><div class="cap">{cap}</div><div class="fl">{links}</div></div>',
            unsafe_allow_html=True,
        )

    bios = "".join(
        f'<div class="bio"><div class="w">{w}</div><div><b>{r}</b> · {o}'
        f'<div class="n">{n}</div></div></div>'
        for w, r, o, n in TIMELINE
    )
    st.markdown(
        f"""<div class="dp"><div class="rule"></div>
  <p class="op" style="font-size:16px">{s['blurb']}</p>
  {bios}
  <div class="ft">Say hello.<br/>
    {''.join(f"<a href='{u}' target='_blank'>{k}</a>" for k, u in s['links'].items())}
  </div>
</div>""",
        unsafe_allow_html=True,
    )
