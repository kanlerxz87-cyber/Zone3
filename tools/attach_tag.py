#!/usr/bin/env python3
"""Attach the Associates tracking ID to every outbound Amazon product link.

Session 5d460e79, 2026-11-19. Fixes audit finding 5D4-F01.

WHY THIS EXISTS
---------------
Program Policies, Participation Requirements 2(b) (read 2026-11-19, source S02) says:

    "you must include your Associates ID or "tag" (appearing as XXXXX-##, or such
     other format as we may designate) as a parameter in the URL of each link you
     place on your Site to an Amazon Site."

On the base commit this site placed Amazon product links that carried no tag
parameter at all: the submitted https://link.amazon/<token> short links, and the
bare https://www.amazon.com/dp/<ASIN> evidence links. tools/build_shop.py even
*failed the build* if a tag= appeared. The site could therefore send a reader to
Amazon and attribute nothing.

WHAT THIS DOES NOT CLAIM
------------------------
Attaching the parameter makes the link carry the selected tracking ID. It does not
prove the ID belongs to an enrolled account, and it does not prove Amazon credits
the click. Those two checks need a logged-in Associates workflow and stay flagged
(FLG-003, 0C4-F-04). This script never asserts either.

REWRITE RULES — conservative on purpose
---------------------------------------
  * Only product destinations are touched: link.amazon short links, and
    amazon.<tld>/dp/<ASIN> or /gp/product/<ASIN> pages.
  * Help, policy, browse-node and search pages are left alone; they are not
    product links and tagging them serves no purpose.
  * An existing param named `tag` is NEVER overwritten. If a link already carries a
    different tag, it is reported as a conflict and left byte-for-byte intact, so a
    foreign tag can never be silently captured or destroyed.
  * Everything else in the URL (query params, fragments, path) is preserved.
  * `rel` is untouched here; scripts/mark_sponsored.py and tools/apply_sponsored.py
    own that attribute. This module only edits the href.

    python3 tools/attach_tag.py            # rewrite in place, print a summary
    python3 tools/attach_tag.py --check    # exit 1 if any product link is untagged
    python3 tools/attach_tag.py --report   # print per-link JSON, write nothing
"""
from __future__ import annotations

import argparse
import html
import json
import re
import sys
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

ROOT = Path(__file__).resolve().parents[1]
SKIP_DIRS = {'archive', 'sessions', 'docs', 'node_modules', '.git', '.github'}

PRODUCT_HREF = re.compile(
    r'https?://(?:[^"\']*\.)?'
    r'(?:link\.amazon/[^"\']+'
    r'|amazon\.[a-z]{2,3}(?::\d+)?/(?:[^"\']*/)?(?:dp|gp/product)/[A-Z0-9]{10}(?:[^"\']*)?)',
    re.I,
)
ANCHOR_RE = re.compile(r'<a\b[^>]*>', re.I)
HREF_RE = re.compile(r'href="([^"]+)"', re.I)


def load_tag() -> str:
    """Read the selected tracking ID from the shop config, the one place it is declared."""
    cfg = json.loads((ROOT / 'data' / 'shop' / 'config.json').read_text(encoding='utf-8'))
    tag = (cfg.get('associates_tracking_id') or '').strip()
    if not re.fullmatch(r'[A-Za-z0-9._-]{3,24}-[0-9]{2,3}', tag):
        raise SystemExit(f'refusing to run: tracking ID {tag!r} does not look like an Associates tag')
    return tag


def retag(href: str, tag: str) -> tuple[str, str]:
    """Return (new_href, status). Status is one of: tagged, already, conflict, skipped.

    The href arrives HTML-escaped (`&amp;`) or raw. It is unescaped before parsing and
    re-escaped on output, so a query string keeps whatever form the source page used and
    an `&amp;` is never double-encoded into a broken parameter.
    """
    decoded = html.unescape(href)
    if not PRODUCT_HREF.fullmatch(decoded.split('#', 1)[0]):
        return href, 'skipped'
    escaped = '&amp;' in href or '&#38;' in href
    parts = urlsplit(decoded)
    pairs = parse_qsl(parts.query, keep_blank_values=True)
    for key, value in pairs:
        if key.lower() == 'tag':
            return href, 'already' if value == tag else 'conflict'
    pairs.append(('tag', tag))
    rebuilt = urlunsplit((parts.scheme, parts.netloc, parts.path, urlencode(pairs), parts.fragment))
    if escaped:
        rebuilt = rebuilt.replace('&', '&amp;')
    return rebuilt, 'tagged'


def process_page(text: str, tag: str) -> tuple[str, list[str]]:
    """Rewrite hrefs inside <a> tags only. Returns (new_text, audit rows)."""
    rows: list[str] = []

    def patch_anchor(m: re.Match) -> str:
        anchor = m.group(0)
        href_m = HREF_RE.search(anchor)
        if not href_m:
            return anchor
        new_href, status = retag(href_m.group(1), tag)
        if status == 'conflict':
            rows.append(f'CONFLICT kept as-is: {href_m.group(1)}')
            return anchor
        if status != 'tagged':
            return anchor
        rows.append(f'tagged: {new_href}')
        return anchor[: href_m.start(1)] + new_href + anchor[href_m.end(1):]

    return ANCHOR_RE.sub(patch_anchor, text), rows


def live_pages() -> list[Path]:
    pages = []
    for path in sorted(ROOT.rglob('*.html')):
        if path.relative_to(ROOT).parts[0] in SKIP_DIRS:
            continue
        pages.append(path)
    return pages


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--check', action='store_true', help='fail if any product link is untagged; write nothing')
    ap.add_argument('--report', action='store_true', help='print per-link JSON; write nothing')
    args = ap.parse_args()

    tag = load_tag()
    changed_pages = 0
    counts = {'tagged': 0, 'already': 0, 'conflict': 0}
    report: dict[str, list[str]] = {}

    for path in live_pages():
        rel = path.relative_to(ROOT).as_posix()
        original = path.read_text(encoding='utf-8')
        updated, rows = process_page(original, tag)
        if rows:
            report[rel] = rows
        for row in rows:
            key = 'conflict' if row.startswith('CONFLICT') else 'tagged'
            counts[key] += 1
        # count already-tagged links so --check reports reality rather than silence
        for href in HREF_RE.findall(original):
            if PRODUCT_HREF.fullmatch(href.split('#', 1)[0]):
                _, status = retag(href, tag)
                if status == 'already':
                    counts['already'] += 1
        if updated != original:
            changed_pages += 1
            if not args.check and not args.report:
                path.write_text(updated, encoding='utf-8')

    if args.report:
        print(json.dumps({'tag': tag, 'counts': counts, 'pages': report}, indent=2, ensure_ascii=False))
        return 0

    if args.check:
        if counts['conflict']:
            print(f'FAIL: {counts["conflict"]} product link(s) carry a foreign tag and were not overwritten')
            return 1
        if counts['tagged']:
            print(f'FAIL: {counts["tagged"]} product link(s) across {changed_pages} page(s) carry no tracking ID')
            return 1
        print(f'OK: {counts["already"]} product link(s) carry tag {tag}; no foreign tags')
        return 0

    print(f'tag {tag}: attached to {counts["tagged"]} link(s) across {changed_pages} page(s); '
          f'{counts["already"]} already carried it; {counts["conflict"]} conflict(s) left untouched')
    return 0


if __name__ == '__main__':
    sys.exit(main())
