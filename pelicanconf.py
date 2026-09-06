"""Portfolio — Pelican configuration.

The site is a Workbench: a catalogue of artifacts beside a stage that presents
the selected one. Each artifact is one Markdown file in content/artifacts/ and
gets its own URL, which is what makes them linkable and crawlable.

Pelican's `category` carries the artifact's KIND. The five kinds are ordered
deliberately in KIND_ORDER below; that order is the catalogue's order.
"""
import json
from pathlib import Path

AUTHOR = "Nicholas Carsner"
SITENAME = "Nicholas Carsner"
SITESUBTITLE = "Analyst, Orchestrator, Consultant"
SITEURL = ""
PATH = "content"
TIMEZONE = "US/Central"
DEFAULT_LANG = "en"
THEME = "theme"

# One Markdown file per artifact; one URL per artifact.
ARTICLE_PATHS = ["artifacts"]
ARTICLE_URL = "artifacts/{slug}/"
ARTICLE_SAVE_AS = "artifacts/{slug}/index.html"

# Nothing else generates a page. No tags, no archives, no author pages, and no
# feeds — the blog next door owns feeds.
PAGE_PATHS = []
DIRECT_TEMPLATES = ["index"]
CATEGORY_SAVE_AS = ""
CATEGORIES_SAVE_AS = ""
TAG_SAVE_AS = ""
TAGS_SAVE_AS = ""
AUTHOR_SAVE_AS = ""
AUTHORS_SAVE_AS = ""
ARCHIVES_SAVE_AS = ""
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

DEFAULT_PAGINATION = False
RELATIVE_URLS = True
MARKDOWN = {
    "extension_configs": {
        "markdown.extensions.fenced_code": {},
        "markdown.extensions.tables": {},
        "markdown.extensions.meta": {},
    },
    "output_format": "html5",
}

_root = Path(__file__).parent


def _load(name, default):
    p = _root / "data" / name
    try:
        return json.loads(p.read_text())
    except (OSError, ValueError):
        return default


# The catalogue's order, and the label each kind shows.
KIND_ORDER = ["app", "tool", "package", "site", "writing"]
KIND_LABEL = {"app": "Apps", "tool": "Tools", "package": "Packages",
              "site": "Sites", "writing": "Writing"}

# The three most recent posts from the blog, fetched at build time by
# tools/syndicate.py. Cached in the repo so a network failure cannot blank the
# section: the last good fetch is what ships.
SYNDICATED = _load("syndicated.json", [])
QUOTES = _load("quotes.json", [])

CONTACT = [
    ("GitHub", "https://github.com/ncarsner"),
    ("Email", "mailto:nicholascarsner@gmail.com"),
    ("LinkedIn", "https://www.linkedin.com/in/nicholascarsner/"),
]

JINJA_GLOBALS = {
    "KIND_ORDER": KIND_ORDER,
    "KIND_LABEL": KIND_LABEL,
    "SYNDICATED": SYNDICATED,
    "QUOTES": QUOTES,
    "CONTACT": CONTACT,
}
