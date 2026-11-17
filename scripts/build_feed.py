#!/usr/bin/env python3
"""Build feed.xml — the shipped RSS feed (0C4-T5, session 0c4c4cb6, 2026-11-17).

Aggregates every published editorial item across the site's three content layers
into one RSS 2.0 feed at the repository root:

  * Research Desk articles      data/articles.json  -> /articles/<slug>
  * Reader guides (live only)   data/cba81fa5/guides.json -> /site/guides/<file>
  * Field-note feature articles site/articles/*.html (parsed: title, description, Published date)
  * The Crisp Report articles   data/editorial.json -> /read/<slug>.html

Held or rejected guides are excluded by their status field; nothing is invented:
a title, description or date comes only from the record that already carries it.
Item dates are the dates the records state (2026-11-16 for the first cohort).

Discovery: <link rel="alternate" type="application/rss+xml"> is emitted in the
<head> of every page built by scripts/build_site.py, tools/build_i2_site.py and
scripts/build_read.py; robots.txt carries a Feed: hint as well.

Standard library only. Run from the repository root:

    python3 scripts/build_feed.py           # write feed.xml
    python3 scripts/build_feed.py --check   # exit 1 if feed.xml would change
"""
from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys
from datetime import datetime, timezone
from email.utils import format_datetime

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE_BASE = "https://kanlerxz87-cyber.github.io/Zone3"
TITLE_RE = re.compile(r"<title>([^<]*)</title>")
DESC_RE = re.compile(r'<meta name="description" content="([^"]*)"')
PUBLISHED_RE = re.compile(r"Published\s+(\d{4}-\d{2}-\d{2})")


def rfc822(date_str: str) -> str:
    d = datetime.strptime(date_str, "%Y-%m-%d").replace(tzinfo=timezone.utc)
    return format_datetime(d)


def esc(v: str) -> str:
    return (v.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            .replace('"', "&quot;"))


def collect() -> list[dict]:
    items: list[dict] = []

    # 1. Research Desk (root articles/)
    arts = json.loads((ROOT / "data" / "articles.json").read_text(encoding="utf-8"))
    published = arts.get("published")
    for a in arts.get("articles", []):
        items.append({
            "title": a["title"],
            "link": f"{SITE_BASE}/articles/{a['slug']}",
            "guid": f"{SITE_BASE}/articles/{a['slug']}",
            "date": published,
            "description": a.get("dek", ""),
            "category": "Research Desk",
        })

    # 2. Reader guides (site/guides/), live only
    guides = json.loads((ROOT / "data" / "cba81fa5" / "guides.json").read_text(encoding="utf-8"))
    for g in guides.get("guides", []):
        if g.get("status") != "live" or not g.get("href"):
            continue
        fname = g["href"].split("/")[-1]
        items.append({
            "title": g["title"],
            "link": f"{SITE_BASE}/site/guides/{fname}",
            "guid": f"{SITE_BASE}/site/guides/{fname}",
            "date": g.get("published") or g.get("date"),
            "description": g.get("blurb") or g.get("line") or "",
            "category": "Buying guides",
        })

    # 3. Field-note feature articles (site/articles/*.html), parsed from the page itself
    art_dir = ROOT / "site" / "articles"
    if art_dir.exists():
        for p in sorted(art_dir.glob("*.html")):
            if p.name == "index.html":
                continue
            raw = p.read_text(encoding="utf-8")
            tm = TITLE_RE.search(raw)
            dm = DESC_RE.search(raw)
            pm = PUBLISHED_RE.search(raw)
            if not (tm and pm):
                continue  # no invented dates: skip rather than guess
            title = tm.group(1).split(" · ")[0].strip()
            items.append({
                "title": title,
                "link": f"{SITE_BASE}/site/articles/{p.name}",
                "guid": f"{SITE_BASE}/site/articles/{p.name}",
                "date": pm.group(1),
                "description": dm.group(1) if dm else "",
                "category": "Field notes",
            })

    # 4. The Crisp Report (read/)
    editorial = json.loads((ROOT / "data" / "editorial.json").read_text(encoding="utf-8"))
    for a in editorial.get("articles", []):
        items.append({
            "title": a["title"],
            "link": f"{SITE_BASE}/read/{a['slug']}.html",
            "guid": f"{SITE_BASE}/read/{a['slug']}.html",
            "date": a.get("date"),
            "description": a.get("dek", ""),
            "category": "The Crisp Report",
        })

    # Drop anything with no stated date (never invent one), newest first, stable by guid
    items = [i for i in items if i.get("date")]
    items.sort(key=lambda i: (i["date"], i["guid"]), reverse=True)
    return items


def render(items: list[dict]) -> str:
    now = datetime.now(timezone.utc)
    latest = items[0]["date"] if items else now.strftime("%Y-%m-%d")
    channel_desc = (
        "Question-shaped air-fryer guides, comparisons and research articles, "
        "each claim linked to the official page it came from. "
        "As an Amazon Associate we earn from qualifying purchases."
    )
    out = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">',
        "<channel>",
        f"<title>{esc('Zone3 — Air Fryer Research Desk')}</title>",
        f"<link>{SITE_BASE}/</link>",
        f"<description>{esc(channel_desc)}</description>",
        "<language>en-us</language>",
        f"<lastBuildDate>{rfc822(latest)}</lastBuildDate>",
        f'<atom:link href="{SITE_BASE}/feed.xml" rel="self" type="application/rss+xml"/>',
    ]
    for i in items:
        out += [
            "<item>",
            f"<title>{esc(i['title'])}</title>",
            f"<link>{esc(i['link'])}</link>",
            f"<guid isPermaLink=\"true\">{esc(i['guid'])}</guid>",
            f"<pubDate>{rfc822(i['date'])}</pubDate>",
            f"<category>{esc(i['category'])}</category>",
            f"<description>{esc(i['description'])}</description>",
            "</item>",
        ]
    out += ["</channel>", "</rss>", ""]
    return "\n".join(out)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    items = collect()
    text = render(items)
    target = ROOT / "feed.xml"
    current = target.read_text(encoding="utf-8") if target.exists() else None
    if a.check:
        if current != text:
            print(f"STALE: feed.xml needs a rebuild ({len(items)} items)", file=sys.stderr)
            return 1
        print(f"OK: feed.xml current ({len(items)} items)")
        return 0
    target.write_text(text, encoding="utf-8")
    print(f"wrote feed.xml: {len(items)} items")
    return 0


if __name__ == "__main__":
    sys.exit(main())
