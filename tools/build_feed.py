#!/usr/bin/env python3
"""Build the root RSS feed as the UNION of both guide registers (session 82372fd1, 2026-11-17).

Why this shape. The publishing-cadence brief asks that each new guide reach "the existing
sitemap and feed". On 2026-11-17 two sessions independently built feeds against one path:
session aebf0747 published an RSS feed.xml covering the four /guides/ pages, and this
session built an Atom feed.xml covering the live reader guides under site/guides/ — the
collision is recorded as flag G82-F-04. The merge keeps BOTH content sets:

  * format: RSS 2.0, because every head link, footer link and autodiscovery marker that the
    published tree already points at feed.xml declares type="application/rss+xml";
  * entries: the union of
      (a) data/feed/entries-shop.json — aebf0747's four /guides/ items, re-homed verbatim
          with its published dates,
      (b) data/cba81fa5/guides.json — the reader guides with status "live",
      (c) data/articles.json — Research Desk articles under /articles/ (0c4c4cb6),
      (d) site/articles/*.html — field-note features with a stated Published date (0c4c4cb6), and
      (e) data/editorial.json — The Crisp Report articles under /read/ (0c4c4cb6);
    so no session's published page silently loses its feed entry;
  * determinism: dates come from the registers, never from "today" — so --check is a real
    gate (it fails when a rebuild would change anything);
  * head links: sessions/aebf0747/publish_pass.py injects the z3:rss alternate link on every
    published page after any generator run. As a backstop for exactly the case where a
    reader-site rebuild lands after that pass and drops it, this script also ensures a
    rel="alternate" feed link on site/index.html and site/guides/index.html inside its own
    sentinel region — and it does nothing if such a link is already present.
  * content rules: no money amount, star rating, review count, Amazon-hosted image URL or
    submitted short link may appear; a page listed as live must exist on disk.

Usage:  python3 tools/build_feed.py            # write feed.xml (+ backstop links if needed)
        python3 tools/build_feed.py --check    # exit 1 if the tree differs from a rebuild
Chain position: AFTER tools/build_shop.py and sessions/aebf0747/publish_pass.py, BEFORE
scripts/build_sitemap.py (see README). Idempotent.
"""
from __future__ import annotations

import datetime as dt
import html
import json
import re
import sys
from email.utils import parsedate_to_datetime
from pathlib import Path
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parent.parent
BASE = "https://kanlerxz87-cyber.github.io/Zone3"
GUIDES = ROOT / "data" / "cba81fa5" / "guides.json"
SHOPREG = ROOT / "data" / "feed" / "entries-shop.json"
FEED = ROOT / "feed.xml"
BACKSTOP_TARGETS = [ROOT / "site" / "index.html", ROOT / "site" / "guides" / "index.html"]

REGION_START = "<!-- 82372fd1 feed link — generated region, do not hand-edit -->"
REGION_END = "<!-- /82372fd1 feed link -->"

FORBIDDEN = [
    (re.compile(r"\$\s?\d"), "a money amount ($NN) — Program Policies 2(b)/6(t): prices come from Amazon's own rendering, not the feed"),
    (re.compile(r"(?:\d+(?:\.\d+)?|★)\s*(?:out of 5|stars)", re.I), "a star rating — not reproducible without an official feed"),
    (re.compile(r"\d[\d,]*\s+(?:ratings?|reviews?)", re.I), "a review count — same rule as prices"),
    (re.compile(r"amazon\.com/images|media-amazon\.com", re.I), "an Amazon-hosted image URL — Program Content may not be republished in a feed"),
    (re.compile(r"https?://link\.amazon/", re.I), "a submitted short link used as an outbound link — unresolved compliance status, see FLG-003"),
]


def fail(msg: str):
    print(f"FEED BUILD FAILED: {msg}")
    sys.exit(1)


def rfc822(iso: str) -> str:
    d = dt.date.fromisoformat(iso)
    return d.strftime("%a, %d %b %Y 00:00:00 +0000")


def union_entries() -> list[dict]:
    """Entries from both registers, newest first. Deterministic tie-break: link, then title."""
    out: list[dict] = []

    shop = json.loads(SHOPREG.read_text(encoding="utf-8"))
    for x in shop["entries"]:
        for key in ("title", "link", "pubDate_rfc822", "pubDate_iso", "description"):
            if not x.get(key):
                fail(f"shop register entry missing {key!r}")
        # keep the published rfc822 byte-for-byte; it must agree with the ISO date
        pub = parsedate_to_datetime(x["pubDate_rfc822"])
        if pub.date().isoformat() != x["pubDate_iso"]:
            fail(f"shop entry {x['title']!r}: rfc822 date disagrees with pubDate_iso")
        if not x["link"].startswith(BASE + "/guides/"):
            fail(f"shop entry link outside the published guides path: {x['link']}")
        rel = x["link"][len(BASE) + 1:]
        if not (ROOT / rel).exists():
            fail(f"shop entry page {rel!r} is not on disk")
        out.append({"date": x["pubDate_iso"], "sort_key": x["pubDate_rfc822"], "rfc": x["pubDate_rfc822"],
                    "title": x["title"], "link": x["link"], "description": x["description"]})

    reg = json.loads(GUIDES.read_text(encoding="utf-8"))
    for g in reg.get("guides", []):
        status = g.get("status")
        if status == "live":
            for key in ("href", "title", "blurb", "published"):
                if not g.get(key):
                    fail(f"live guide {g.get('href')!r} is missing {key!r} in {GUIDES.name}")
            if not re.match(r"^\d{4}-\d{2}-\d{2}$", g["published"]):
                fail(f"guide {g['href']} has a non-ISO date {g['published']!r}")
            page = ROOT / "site" / g["href"]
            if not page.exists():
                fail(f"live guide {g['href']!r} is not on disk at site/{g['href']}")
            blurb = re.sub(r"<[^>]+>", "", g["blurb"])
            out.append({"date": g["published"], "sort_key": g["published"],
                        "rfc": rfc822(g["published"]), "title": g["title"],
                        "link": f"{BASE}/site/{g['href']}", "description": blurb})
        elif status not in ("held", "rejected", "planned"):
            fail(f"guide {g.get('href') or g.get('title')!r} has unknown status {status!r}")

    # (c) Research Desk articles — root articles/ from data/articles.json (session 0c4c4cb6,
    # unioned 2026-11-17 so no desk's published page silently loses its feed entry).
    arts_path = ROOT / "data" / "articles.json"
    if arts_path.exists():
        arts = json.loads(arts_path.read_text(encoding="utf-8"))
        cohort = arts.get("published")  # desk-level publish date; per-article override if present
        for a in arts.get("articles", []):
            slug = a.get("slug")
            published = a.get("published") or a.get("date") or cohort
            if not slug or not published or not a.get("title"):
                fail(f"research-desk article {a.get('title') or slug!r} is missing slug/published/title")
            if not re.match(r"^\d{4}-\d{2}-\d{2}$", str(published)):
                fail(f"research-desk article {slug} has a non-ISO date {published!r}")
            page = ROOT / "articles" / slug
            if not page.exists():
                fail(f"research-desk article {slug!r} is not on disk at articles/{slug}")
            out.append({"date": str(published), "sort_key": str(published),
                        "rfc": rfc822(str(published)), "title": a["title"],
                        "link": f"{BASE}/articles/{slug}",
                        "description": re.sub(r"<[^>]+>", "", a.get("dek") or a.get("description") or a.get("blurb") or "")})

    # (d) Field-note feature articles — site/articles/*.html parsed from the page itself
    # (title, description and the stated "Published YYYY-MM-DD"; no stated date = skip, never guess).
    art_dir = ROOT / "site" / "articles"
    if art_dir.exists():
        pub_re = re.compile(r"Published\s+(\d{4}-\d{2}-\d{2})")
        for page in sorted(art_dir.glob("*.html")):
            if page.name == "index.html":
                continue
            raw = page.read_text(encoding="utf-8", errors="replace")
            tm = re.search(r"<title>(.*?)</title>", raw, re.S)
            dm = re.search(r'<meta name="description" content="([^"]*)"', raw)
            pm = pub_re.search(raw)
            if not (tm and pm):
                continue
            out.append({"date": pm.group(1), "sort_key": pm.group(1),
                        "rfc": rfc822(pm.group(1)), "title": html.unescape(tm.group(1)).split(" |")[0].strip(),
                        "link": f"{BASE}/site/articles/{page.name}",
                        "description": html.unescape(dm.group(1)) if dm else ""})

    # (e) The Crisp Report — read/ from data/editorial.json (session 0c4c4cb6 union).
    ed_path = ROOT / "data" / "editorial.json"
    if ed_path.exists():
        ed = json.loads(ed_path.read_text(encoding="utf-8"))
        for a in ed.get("articles", []):
            slug = a.get("slug")
            date = a.get("date")
            if not slug or not date or not a.get("title"):
                fail(f"crisp-report article {a.get('title') or slug!r} is missing slug/date/title")
            if not re.match(r"^\d{4}-\d{2}-\d{2}$", str(date)):
                fail(f"crisp-report article {slug} has a non-ISO date {date!r}")
            page = ROOT / "read" / f"{slug}.html"
            if not page.exists():
                fail(f"crisp-report article {slug!r} is not on disk at read/{slug}.html")
            out.append({"date": str(date), "sort_key": str(date),
                        "rfc": rfc822(str(date)), "title": a["title"],
                        "link": f"{BASE}/read/{slug}.html",
                        "description": re.sub(r"<[^>]+>", "", a.get("dek") or a.get("summary") or a.get("description") or "")})

    # Canonical publication registry: add new guides and update the four existing
    # entries' current title/dek while retaining their original publication dates.
    publication = json.loads((ROOT / "data/publication.json").read_text(encoding="utf-8"))
    by_url = {entry["link"]: entry for entry in out}
    for guide in publication["guides"]:
        url = f"{BASE}/guides/{guide['slug']}.html"
        if not (ROOT / "guides" / f"{guide['slug']}.html").is_file():
            fail(f"publication guide missing: {url}")
        if url in by_url:
            by_url[url]["title"] = guide["title"]
            by_url[url]["description"] = guide["dek"]
        else:
            entry = {"date": guide["published"], "sort_key": guide["published"],
                     "rfc": rfc822(guide["published"]), "title": guide["title"],
                     "link": url, "description": guide["dek"]}
            out.append(entry)
            by_url[url] = entry
    if len({entry["link"] for entry in out}) != len(out):
        fail("duplicate article URL in the unified feed")

    if not out:
        fail("all registers empty — a feed with no entries would misrepresent the site")
    out.sort(key=lambda e: (e["date"], e["link"], e["title"]), reverse=True)
    return out


def noindex_targets(entries: list[dict]) -> tuple[list[dict], list[str]]:
    """Drop feed entries whose destination page is deliberately noindex (5D4-F02, 2026-11-19).

    A feed that advertises pages the sitemap excludes and the site marks noindex sends a
    crawler and a subscriber to two different versions of the site. On the base commit 19 of
    27 items pointed at noindex,follow pages (the /read/ archive, the site/ field notes and
    the /articles/ desk), all of which scripts/build_sitemap.py skips on purpose.

    The entry is dropped only when the destination page exists on disk AND declares
    noindex. A missing file is left to the existing live-existence check above, so this
    function cannot silently hide a broken link.
    """
    keep, dropped = [], []
    for e in entries:
        link = e['link']
        if not link.startswith(BASE + '/'):
            keep.append(e)
            continue
        rel = link[len(BASE) + 1:]
        target = ROOT / rel
        if target.is_dir():
            target = target / 'index.html'
        if not target.exists():
            keep.append(e)  # let the existing existence rule report it
            continue
        text = target.read_text(encoding='utf-8', errors='replace')
        if re.search(r'<meta[^>]*name=["\']robots["\'][^>]*content=["\'][^"\']*noindex', text, re.I):
            dropped.append(link)
            continue
        keep.append(e)
    return keep, dropped


def build_feed() -> str:
    entries = union_entries()
    entries, dropped = noindex_targets(entries)
    if dropped:
        print(f'feed: excluded {len(dropped)} noindex destination(s) that the sitemap also excludes')
    if not entries:
        fail('every candidate entry points at a noindex page — refusing to publish an empty feed')
    for e in entries:
        blob = e["title"] + " " + e["description"]
        for rx, why in FORBIDDEN:
            m = rx.search(blob)
            if m:
                fail(f"entry {e['title'][:40]!r} would contain {why} -> {m.group(0)!r}")
    x = []
    x.append('<?xml version="1.0" encoding="UTF-8"?>')
    x.append('<rss version="2.0"><channel><title>Zone3 guides</title>')
    # Canonical form matches sitemap.xml and the page's rel=canonical (5D4-F02).
    x.append(f'<link>{BASE}/guides/</link>')
    x.append(
        "<description>Question-led kitchen buying guides and archived research notes — the canonical /guides/ pages, "
        "the Air Fryer Field Notes buying guides, the Research Desk articles and The Crisp Report field notes. "
        "Working titles; every quoted listing title is checked on the date shown; no price, rating or review "
        "count is reproduced and no traffic or ranking claim is made.</description>"
    )
    x.append("<language>en</language>")
    x.append(f"<lastBuildDate>{entries[0]['rfc']}</lastBuildDate>")
    for e in entries:
        x.append("<item>")
        x.append(f"<title>{html.escape(e['title'])}</title>")
        x.append(f"<link>{e['link']}</link>")
        x.append(f'<guid isPermaLink="true">{e["link"]}</guid>')
        x.append(f"<pubDate>{e['rfc']}</pubDate>")
        x.append(f"<description>{html.escape(e['description'])}</description>")
        x.append("</item>")
    x.append("</channel></rss>")
    x.append("")
    doc = "\n".join(x)
    ET.fromstring(doc)  # must be valid XML before it is ever written
    for rx, why in FORBIDDEN:
        m = rx.search(doc)
        if m:
            fail(f"feed.xml would contain {why} -> {m.group(0)!r}")
    return doc


def head_region(target: Path) -> str:
    import os
    rel = os.path.relpath(FEED, target.parent).replace("\\", "/")
    return (
        f"{REGION_START}\n"
        '<link rel="alternate" type="application/rss+xml" title="Zone3 guides" '
        f'href="{rel}">\n'
        f"{REGION_END}"
    )


def patch_head(raw: str, target: Path) -> str:
    """Backstop only: if the page already carries any rss alternate (e.g. the z3:rss marker
    from sessions/aebf0747/publish_pass.py, which runs earlier in the chain), leave it alone.
    Otherwise ensure this script's own region. Never touches the rest of the file."""
    pat = re.compile(re.escape(REGION_START) + r".*?" + re.escape(REGION_END), re.S)
    if re.search(r'<link rel="alternate" type="application/rss\+xml"', raw):
        return pat.sub("", raw)  # another injector owns this page; drop any stale region
    region = head_region(target)
    if pat.search(raw):
        new = pat.sub(region, raw)
    else:
        if "</head>" not in raw:
            fail(f"{target.relative_to(ROOT)} has no </head> to inject before")
        new = raw.replace("</head>", f"{region}\n</head>", 1)
    return new


def render_all() -> dict[Path, str]:
    out = {FEED: build_feed()}
    for t in BACKSTOP_TARGETS:
        raw = t.read_text(encoding="utf-8")
        out[t] = patch_head(raw, t)
    return out


def main() -> None:
    check = "--check" in sys.argv[1:]
    if check and len(sys.argv) - 1 > 1:
        fail("usage: build_feed.py [--check]")
    out = render_all()
    n = out[FEED].count("<item>")
    if check:
        drift = [str(p.relative_to(ROOT)) for p, s in out.items() if p.read_text(encoding="utf-8") != s]
        if drift:
            print("FEED CHECK FAILED — rebuild would change:", *drift, sep="\n  ")
            sys.exit(1)
        print(f"FEED OK — already current; {n} entries (union of both registers)")
        return
    changed = sum(1 for p, s in out.items() if p != FEED and p.read_text(encoding="utf-8") != s)
    for p, s in out.items():
        p.write_text(s, encoding="utf-8")
    print(f"built feed.xml ({n} entries) [{dt.date.today().isoformat()}] backstop links touched: {changed}")


if __name__ == "__main__":
    main()
