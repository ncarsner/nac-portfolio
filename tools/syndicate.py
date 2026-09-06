"""Fetch the three most recent posts from the blog and cache them.

The blog stays a separate property (ADR 0005); the portfolio renders only each
post's title and date and links out. The cache is committed so a network failure
at build time cannot blank the Writing section — the last good fetch ships.
"""
import json
import sys
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

FEED = "https://ncarsner.github.io/feeds/all.atom.xml"
COUNT = 3
NS = {"a": "http://www.w3.org/2005/Atom"}
DEST = Path(__file__).parent.parent / "data" / "syndicated.json"


def fetch():
    with urllib.request.urlopen(FEED, timeout=20) as r:
        return ET.fromstring(r.read())


def main():
    try:
        root = fetch()
    except Exception as exc:                      # network, DNS, malformed feed
        if DEST.exists():
            print(f"  feed unreachable ({exc.__class__.__name__}); keeping cache")
            return 0
        print(f"  feed unreachable ({exc.__class__.__name__}) and no cache", file=sys.stderr)
        return 1

    posts = []
    for entry in root.findall("a:entry", NS)[:COUNT]:
        title = entry.findtext("a:title", "", NS).strip()
        updated = entry.findtext("a:updated", "", NS)[:10]
        link = entry.find("a:link", NS)
        posts.append({
            "title": title,
            "date": updated,
            "url": link.get("href") if link is not None else FEED,
        })

    DEST.write_text(json.dumps(posts, indent=2) + "\n")
    print(f"  {len(posts)} posts cached to {DEST.name}")
    for p in posts:
        print(f"    {p['date']}  {p['title']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
