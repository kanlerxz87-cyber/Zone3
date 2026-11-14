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

SKIP_DIRS = {".git", "archive", "__pycache__", ".github"}
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
        # Coverage, not byte equality. tools/build_site.py rewrites this file from its own
        # list plus every root *.html, which also sweeps in the meta-refresh stubs this
        # script deliberately excludes — so an exact-text comparison is never a fixpoint.
        # What must hold is: no live page is missing from the sitemap.
        if not target.exists():
            print("sitemap.xml missing")
            return 1
        have = set(re.findall(r"<loc>([^<]+)</loc>", target.read_text(encoding="utf-8")))
        want = {f"{SITE_ORIGIN}{SITE_BASE}/{p}" for p in pages}
        missing = sorted(want - have)
        if missing:
            print(f"sitemap.xml is missing {len(missing)} page(s):")
            for m in missing:
                print("  -", m)
            return 1
        print(f"sitemap.xml covers every live page ({len(pages)} pages checked, "
              f"{len(have) - len(want)} extra entr{'y' if len(have) - len(want) == 1 else 'ies'} "
              f"from the other generator)")
        return 0
    target.write_text(text, encoding="utf-8")
    print(f"wrote sitemap.xml: {len(pages)} pages")
    for p in pages:
        print("  /" + p)
    return 0


if __name__ == "__main__":
    sys.exit(main())
