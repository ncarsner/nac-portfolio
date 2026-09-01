"""
PROTOTYPE — self-contained live demos.

The portfolio needs to host *running* things, not just descriptions of them.
These are real, working, dependency-free HTML apps embedded via
st.components.v1.html. In the real site each of these slots would instead be an
iframe pointed at the deployed app (or the app's own bundle).
"""
import base64
from pathlib import Path as _Path


def _svg_data_uri(svg: str) -> str:
    return "data:image/svg+xml;base64," + base64.b64encode(svg.encode()).decode()


def placeholder(label: str, sub: str, a: str = "#1f6feb", b: str = "#0b1220", w=1200, h=675) -> str:
    """A stand-in for a real screenshot. Marked so nobody mistakes it for artwork."""
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}">
  <defs>
    <linearGradient id="g" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="{a}"/><stop offset="100%" stop-color="{b}"/>
    </linearGradient>
    <pattern id="p" width="40" height="40" patternUnits="userSpaceOnUse">
      <path d="M40 0H0V40" fill="none" stroke="rgba(255,255,255,.07)" stroke-width="1"/>
    </pattern>
  </defs>
  <rect width="{w}" height="{h}" fill="url(#g)"/>
  <rect width="{w}" height="{h}" fill="url(#p)"/>
  <text x="56" y="{h/2 - 6}" font-family="ui-monospace,SFMono-Regular,Menlo,monospace"
        font-size="46" fill="#fff" opacity=".95">{label}</text>
  <text x="56" y="{h/2 + 38}" font-family="ui-monospace,SFMono-Regular,Menlo,monospace"
        font-size="21" fill="#fff" opacity=".55">{sub}</text>
  <text x="56" y="{h - 44}" font-family="ui-monospace,SFMono-Regular,Menlo,monospace"
        font-size="16" fill="#fff" opacity=".35">PLACEHOLDER — real screenshot goes here</text>
</svg>"""
    return _svg_data_uri(svg)


DEMOS_DIR = _Path(__file__).parent / "demos"

# id -> (file stem, default height). In the real site these become URLs of deployed
# apps; the mechanic (an iframe holding a running thing) is identical either way.
# Each demo is built once per page tone by demos/build.py, so a running artifact
# shares the page's ground instead of punching a hole in it.
EMBEDS = {
    "regex_lab": ("regex_lab", 430),
    "deploy_board": ("deploy_board", 400),
}

TONES = ("slate", "fog", "ash")


def render(st, key, height=None, tone="slate"):
    """Render a live demo in an iframe. Returns True if something was drawn."""
    if key not in EMBEDS:
        return False
    stem, h = EMBEDS[key]
    if tone not in TONES:
        tone = "slate"
    st.iframe(DEMOS_DIR / f"{stem}_{tone}.html", height=height or h)
    return True
