#!/usr/bin/env python3
"""0C4-T3 — mark every outbound product link rel="sponsored" (idempotent).

The brief: "Keep every outbound product link marked as sponsored." Google's
outbound-links guidance (developers.google.com/search/docs/crawling-indexing/
qualify-outbound-links) asks for rel="sponsored" on paid/affiliate links; the
Operating Agreement requires the Associates disclosure to stay intact, so this
script only ever adds a rel token and never rewrites link text, href or any
disclosure sentence.

Targets (product links only):
  * href starting https://link.amazon/          (the submitted short links)
  * href on an amazon.com host whose path contains /dp/ or /gp/product/

Run AFTER every HTML generator (scripts/build_site.py, tools/build_i2_site.py,
tools/build_cba81fa5_site.py, scripts/build_marketing.py, scripts/build_read.py,
scripts/build_5a56c084.py, tools/build_site.py) and BEFORE scripts/build_sitemap.py.
scripts/check_site.py fails if any target link on its page set is missing the
token, so a generator that regenerates a page without this step cannot land
silently.

Standard library only. Run from the repository root:

    python3 scripts/mark_sponsored.py            # rewrite in place, print summary
    python3 scripts/mark_sponsored.py --check    # exit 1 if anything would change
"""
from __future__ import annotations

import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SKIP_DIRS = {".git", "archive", "node_modules", ".venv", "venv"}

ANCHOR_RE = re.compile(r"<a\b[^>]*>", re.I)
HREF_RE = re.compile(r'href="([^"]+)"', re.I)
REL_RE = re.compile(r'\brel="([^"]*)"', re.I)


def is_product_link(href: str) -> bool:
    if href.startswith("https://link.amazon/"):
        return True
    if not href.startswith(("https://www.amazon.com/", "https://amazon.com/")):
        return False
    path = href.split("?", 1)[0]
    return "/dp/" in path or "/gp/product/" in path


def fix_tag(tag: str) -> str | None:
    """Return the tag with 'sponsored' merged into rel, or None if unchanged."""
    m = HREF_RE.search(tag)
    if not m or not is_product_link(m.group(1)):
        return None
    rel_m = REL_RE.search(tag)
    if rel_m:
        tokens = rel_m.group(1).split()
        if "sponsored" in tokens:
            return None
        tokens.append("sponsored")
        new_rel = " ".join(tokens)
        return tag[: rel_m.start(1)] + new_rel + tag[rel_m.end(1) :]
    # no rel attribute yet: insert one right after the tag name
    name_m = re.match(r"<a(\s+)", tag, re.I)
    if not name_m:
        return None
    pos = name_m.end()
    return tag[:pos] + 'rel="sponsored" ' + tag[pos:]


def process(text: str) -> tuple[str, int]:
    count = 0

    def repl(m: re.Match) -> str:
        nonlocal count
        new = fix_tag(m.group(0))
        if new is not None:
            count += 1
            return new
        return m.group(0)

    return ANCHOR_RE.sub(repl, text), count


def main() -> int:
    check_only = "--check" in sys.argv
    changed_files = 0
    changed_links = 0
    for path in sorted(ROOT.rglob("*.html")):
        rel_parts = path.relative_to(ROOT).parts
        if rel_parts[0] in SKIP_DIRS:
            continue
        original = path.read_text(encoding="utf-8")
        updated, n = process(original)
        if n:
            changed_links += n
            changed_files += 1
            if not check_only:
                path.write_text(updated, encoding="utf-8")
    if check_only:
        if changed_links:
            print(f"FAIL: {changed_links} product link(s) across {changed_files} page(s) missing rel=sponsored")
            return 1
        print("OK: every outbound product link already carries rel=sponsored")
        return 0
    print(f"marked rel=sponsored on {changed_links} link(s) across {changed_files} page(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
