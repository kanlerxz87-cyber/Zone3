#!/usr/bin/env python3
"""Build the Atom feed for the reader-site guide set (session 82372fd1, 2026-11-17).

Why this exists. The publishing-cadence brief asks that each new guide reach "the existing
sitemap and feed". The sitemap half is covered (scripts/build_sitemap.py --check is a gate);
the feed half had no implementation before 2026-11-16T20:00Z — a repo-wide search for
"rss|feed.xml" found only this brief text. This script adds the missing half:

  * feed.xml  — an Atom feed whose entries are exactly the guides with status "live" in
                data/cba81fa5/guides.json (the register the guide surfaces already read).
                Nothing is hand-typed into the feed, so a rebuild cannot drift from it.
  * head link — a <link rel="alternate"> in the heads of site/index.html and
                site/guides/index.html, injected between sentinel comments in the same
                self-healing style tools/build_cba81fa5_site.py uses for its regions: an
                i2/cba rebuild drops the region, and running this script again restores it.
                The site/** HTML stays owned by its generators; this script never edits
                anything outside the sentinel region it owns.

Rules this builder enforces (same family as tools/i2_gate.py G6/G7):
  * no money amount, star rating, review count or Amazon-hosted image may appear in the
    feed text — the register blurbs are the only body text, and they are scanned too;
  * every entry link is an absolute https URL under the published Pages base;
  * dates come from the register, never from "today", so output is deterministic and
    --check is meaningful;
  * the script fails rather than silently emitting a partial feed (a missing guide page
    file, a malformed date, an unexpected status value).

Usage:  python3 tools/build_feed.py            # write feed.xml + head links
        python3 tools/build_feed.py --check    # exit 1 if the tree differs from a rebuild
Build order: run AFTER tools/build_cba81fa5_site.py and scripts/build_sitemap.py. The
README chain lists it as the last build step. Idempotent: running it twice changes nothing.
"""
from __future__ import annotations

import datetime as dt
import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = "https://kanlerxz87-cyber.github.io/Zone3"
GUIDES = ROOT / "data" / "cba81fa5" / "guides.json"
FEED = ROOT / "feed.xml"
HEAD_TARGETS = [ROOT / "site" / "index.html", ROOT / "site" / "guides" / "index.html"]

REGION_START = "<!-- 82372fd1 feed link — generated region, do not hand-edit -->"
REGION_END = "<!-- /82372fd1 feed link -->"


def head_line(target: Path) -> str:
    import os
    rel = os.path.relpath(FEED, target.parent).replace("\\", "/")
    return (
        '<link rel="alternate" type="application/atom+xml" '
        f'title="Air Fryer Field Notes — new buying guides" href="{rel}">'
    )

# Prohibited content patterns, mirroring the reader gates. A match anywhere in the feed
# is a build failure, not a warning.
FORBIDDEN = [
    (re.compile(r"\$\s?\d"), "a money amount ($NN) — Program Policies 2(b)/6(t): prices come from Amazon's own rendering, not the feed"),
    (re.compile(r"(?:\d+(?:\.\d+)?|★)\s*(?:out of 5|stars)", re.I), "a star rating — not reproducible without an official feed"),
    (re.compile(r"\d[\d,]*\s+(?:ratings?|reviews?)", re.I), "a review count — same rule as prices"),
    (re.compile(r"amazon\.com/images|media-amazon\.com", re.I), "an Amazon-hosted image URL — Program Content may not be republished in a feed"),
    (re.compile(r"https?://link\.amazon/", re.I), "a submitted short link used as an outbound link — unresolved compliance status, see FLG-003"),
]

DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def fail(msg: str) -> "NoReturn":  # type: ignore[valid-type]
    print(f"FEED BUILD FAILED: {msg}")
    sys.exit(1)


def load_entries() -> list[dict]:
    reg = json.loads(GUIDES.read_text(encoding="utf-8"))
    entries = []
    for g in reg.get("guides", []):
        status = g.get("status")
        if status == "live":
            for key in ("href", "title", "blurb", "published"):
                if not g.get(key):
                    fail(f"live guide {g.get('href')!r} is missing {key!r} in {GUIDES.name}")
            if not DATE_RE.match(g["published"]):
                fail(f"guide {g['href']} has a non-ISO date {g['published']!r}")
            page = ROOT / "site" / g["href"]
            if not page.exists():
                fail(f"live guide {g['href']!r} is not on disk at site/{g['href']}")
            entries.append(g)
        elif status not in ("held", "rejected", "planned"):
            fail(f"guide {g.get('href') or g.get('title')!r} has unknown status {status!r}")
    if not entries:
        fail("no live guides in the register — an empty feed would misrepresent the site")
    # newest first; ties keep register order for determinism
    entries.sort(key=lambda g: g["published"], reverse=True)
    return entries


def iso(d: str) -> str:
    return f"{d}T00:00:00Z"


def check_text(where: str, text: str) -> None:
    for rx, why in FORBIDDEN:
        m = rx.search(text)
        if m:
            fail(f"{where} would contain {why} -> {m.group(0)!r}")


def build_feed() -> str:
    entries = load_entries()
    latest = max(g["published"] for g in entries)
    x = []
    x.append('<?xml version="1.0" encoding="UTF-8"?>')
    x.append('<feed xmlns="http://www.w3.org/2005/Atom">')
    x.append("  <title>Air Fryer Field Notes — buying guides</title>")
    x.append(
        "  <subtitle>One question per guide, answered from the Amazon listing text. Every "
        "specification links the page it was read from; nothing here claims a test that was "
        "not run, and no price, rating or review count is reproduced.</subtitle>"
    )
    x.append(f'  <link rel="self" href="{BASE}/feed.xml"/>')
    x.append(f'  <link href="{BASE}/site/index.html"/>')
    x.append(f"  <id>{BASE}/feed.xml</id>")
    x.append(f"  <updated>{iso(latest)}</updated>")
    x.append("  <author><name>Air Fryer Field Notes desk</name></author>")
    x.append(f'  <generator uri="{BASE}/tools/build_feed.py">tools/build_feed.py</generator>')
    for g in entries:
        url = f"{BASE}/site/{g['href']}"
        title = html.escape(g["title"], quote=True)
        blurb = html.escape(g["blurb"], quote=False)
        summary = html.escape(re.sub(r"<[^>]+>", "", g["blurb"]), quote=False)
        check_text(f"entry {g['href']}", g["title"] + " " + g["blurb"])
        src = html.escape(g.get("source_note", "").strip(), quote=False) if g.get("source_note") else ""
        body = f"<p>{blurb}</p><p>Published {g['published']}. Sources are cited on the page.</p>"
        if src:
            body += f"<p>{src}</p>"
        x.append("  <entry>")
        x.append(f"    <title>{title}</title>")
        x.append(f'    <link href="{url}"/>')
        x.append(f"    <id>{url}</id>")
        x.append(f"    <updated>{iso(g['published'])}</updated>")
        x.append(f"    <summary>{summary}</summary>")
        x.append(f"    <content type=\"html\">{html.escape(body)}</content>")
        x.append("  </entry>")
    x.append("</feed>")
    x.append("")
    return "\n".join(x)


def patch_head(raw: str, target: Path) -> str:
    """Idempotent sentinel-region injection into <head>. Replaces the region if present;
    inserts it before </head> otherwise. Never touches the rest of the file."""
    region = f"{REGION_START}\n{head_line(target)}\n{REGION_END}"
    pat = re.compile(
        re.escape(REGION_START) + r".*?" + re.escape(REGION_END), re.S
    )
    if pat.search(raw):
        new = pat.sub(region, raw)  # already present: a no-op replace keeps it idempotent
    else:
        if "</head>" not in raw:
            fail(f"{target.relative_to(ROOT)} has no </head> to inject before")
        new = raw.replace("</head>", f"{region}\n</head>", 1)
    if REGION_START not in new:
        fail(f"head patch for {target.relative_to(ROOT)} produced no region — anchors drifted")
    return new


def render_all() -> dict[Path, str]:
    out = {FEED: build_feed()}
    for t in HEAD_TARGETS:
        raw = t.read_text(encoding="utf-8")
        out[t] = patch_head(raw, t)
    for p, s in out.items():
        if p.name == "feed.xml":
            for rx, why in FORBIDDEN:
                m = rx.search(s)
                if m:
                    fail(f"feed.xml would contain {why} -> {m.group(0)!r}")
    return out


def main() -> None:
    check = "--check" in sys.argv[1:]
    if check and len(sys.argv) - 1 > 1:
        fail("usage: build_feed.py [--check]")
    out = render_all()
    if check:
        drift = [str(p.relative_to(ROOT)) for p, s in out.items() if p.read_text(encoding="utf-8") != s]
        if drift:
            print("FEED CHECK FAILED — rebuild would change:", *drift, sep="\n  ")
            sys.exit(1)
        n = open(FEED, encoding="utf-8").read().count("<entry>")
        print(f"FEED OK — already current; {n} live guide entries")
        return
    for p, s in out.items():
        p.write_text(s, encoding="utf-8")
    today = dt.date.today().isoformat()  # recorded nowhere in the output; used only for the log line
    n = out[FEED].count("<entry>")
    print(f"built feed.xml ({n} entries) + head link in {len(HEAD_TARGETS)} reader index pages [{today}]")


if __name__ == "__main__":
    main()
