#!/usr/bin/env python3
"""Write sitemap.xml for the whole GitHub Pages site.

This repository carries more than one site generation (the root flat pages built by
scripts/build_site.py, the 16-page audit built by tools/build_site.py, /docs/, the
directory pages and the per-session page sets). The two generators each used to write
sitemap.xml from their own output only, so whichever ran last de-listed the other's
pages — recorded as flag V-F4. This script is the single place the sitemap is produced
from: it walks the checked-in tree, so the file always matches what Pages actually serves.

    python3 scripts/build_sitemap.py            # rewrite sitemap.xml
    python3 scripts/build_sitemap.py --check    # exit 1 if sitemap.xml is out of date

Excluded on purpose:
  * archive/**   — byte-for-byte snapshots of other sessions' sites, kept for the record.
                   They are not part of the live site and contain unresolved links (V-F5).
  * meta-refresh redirect stubs (analysis.html, disclosure.html,
    categories/home-kitchen-air-fryers.html, flagged-for-review.html) — old URLs kept so
    existing links do not break; search engines should index the destination instead.
"""
from __future__ import annotations

import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE_ORIGIN = "https://kanlerxz87-cyber.github.io"
SITE_BASE = "/Zone3"

SKIP_DIRS = {".git", "archive", "__pycache__", ".github",
             # 81bc99d0 (2026-11-16): /docs/ and /sessions/ are audit snapshots that render
             # historical product price/rating/review values captured before Program Policies
             # 2(b)/6(t) barred displaying them without an Amazon-served link or Creators/PA API
             # data (71-F-04). They are kept in the repository as the audit record but are not
             # part of the public, indexable marketing site, so they are excluded from the sitemap.
             "docs", "sessions", "node_modules", ".preview", ".local"}
# Pages whose entire content is a meta-refresh to another page.
REDIRECT_STUBS = {
    "analysis.html",
    "disclosure.html",
    "categories/home-kitchen-air-fryers.html",
    "flagged-for-review.html",
}


def is_redirect_stub(path: pathlib.Path) -> bool:
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return False
    return "http-equiv" in text and "refresh" in text


def collect() -> list[str]:
    """Every indexable HTML page, as a site-relative URL path ('' for the root)."""
    pages: set[str] = set()
    for path in ROOT.rglob("*.html"):
        rel = path.relative_to(ROOT).as_posix()
        if any(part in SKIP_DIRS for part in path.relative_to(ROOT).parts):
            continue
        if rel in REDIRECT_STUBS or is_redirect_stub(path):
            continue
        # A single publication is indexed. Research dashboards and earlier reader
        # editions stay accessible with noindex,follow, not in the search sitemap.
        text = path.read_text(encoding="utf-8")
        if re.search(r'<meta[^>]*name=["\']robots["\'][^>]*content=["\'][^"\']*noindex', text, re.I):
            continue
        pages.add("" if rel == "index.html" else rel.removesuffix("/index.html") + "/"
                  if rel.endswith("/index.html") else rel)
    return sorted(pages)


def render(pages: list[str]) -> str:
    body = "".join(
        f"  <url><loc>{SITE_ORIGIN}{SITE_BASE}/{p}</loc></url>\n" for p in pages
    )
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{body}</urlset>\n"
    )


def main() -> int:
    pages = collect()
    text = render(pages)
    target = ROOT / "sitemap.xml"
    if "--check" in sys.argv:
        if not target.exists() or target.read_text(encoding="utf-8") != text:
            print("sitemap.xml is stale: must match exactly the indexable canonical page set")
            return 1
        print(f"sitemap.xml is current: {len(pages)} indexable pages; no noindex pages or extras")
        return 0
    target.write_text(text, encoding="utf-8")
    print(f"wrote sitemap.xml: {len(pages)} pages")
    for p in pages:
        print("  /" + p)
    return 0


if __name__ == "__main__":
    sys.exit(main())
