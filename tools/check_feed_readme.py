#!/usr/bin/env python3
"""Check the published RSS item count and the design brief's measured inventory.

This is a local, deterministic check: no network, credentials, or product-content reads.
The design brief intentionally distinguishes the wider feed-register candidate union from
items actually emitted in feed.xml after the sitemap and noindex filters. The remaining
measured rows (page tree, canonical/OG/description coverage, register totals) are checked
against the same tree and registers so a stale figure fails the release instead of merely
reading as out of date.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / 'README.md'
DESIGN = ROOT / 'DESIGN_PROMPT.md'
FEED = ROOT / 'feed.xml'
README_MARK = 'z3:register-facts'
DESIGN_ROWS = {
    'HTML pages outside `docs/`, `sessions/`, `archive/`': 'html_pages',
    'Indexable reader set (canonical + in `sitemap.xml`)': 'indexable_urls',
    'Question-led guides': 'guides',
    '`sitemap.xml` `<url>` entries': 'sitemap_urls',
    'Feed candidates before sitemap filtering': 'candidate_count',
    'RSS destinations omitted by sitemap filter': 'sitemap_omitted',
    'Published `feed.xml` items': 'feed_count',
    'Source register': 'sources',
    'Flag register': 'flags',
}
# Rows whose cell reads "<matched> / <total>" against the published HTML tree.
DESIGN_RATIO_ROWS = {
    'Pages carrying `rel="canonical"`': 'canonical_pages',
    'Pages carrying `og:image`': 'og_image_pages',
    'Pages with a meta description ≥ 60 characters': 'described_pages',
}
# One row carries four register figures in a single cell.
DESIGN_DESK_ROW = 'Decision-desk rows on the suggestions page'
DESK_PARTS = ('paths', 'proposals', 'questions', 'brief blocks')
SKIP_DIRS = {'docs', 'sessions', 'archive'}
PUBLICATION = ROOT / 'data/publication.json'
FLAGS = ROOT / 'data/flags.json'
DESCRIPTION_MIN = 60

sys.path.insert(0, str(ROOT / 'tools'))
import build_feed  # noqa: E402


def fail(message: str) -> None:
    raise ValueError(message)


def table_count(block: str, label: str) -> int:
    pattern = re.compile(r'^\|\s*' + re.escape(label) + r'\s*\|\s*(\d+)(?:\s+rows?)?\s*\|', re.M)
    found = pattern.findall(block)
    if len(found) != 1:
        fail(f'expected exactly one count row for {label!r}, found {len(found)}')
    return int(found[0])


def ratio_count(block: str, label: str) -> tuple[int, int]:
    pattern = re.compile(r'^\|\s*' + re.escape(label) + r'\s*\|\s*(\d+)\s*/\s*(\d+)\s*\|', re.M)
    found = pattern.findall(block)
    if len(found) != 1:
        fail(f'expected exactly one ratio row for {label!r}, found {len(found)}')
    return int(found[0][0]), int(found[0][1])


def desk_counts(block: str) -> dict[str, int]:
    pattern = re.compile(r'^\|\s*' + re.escape(DESIGN_DESK_ROW) + r'\s*\|([^|]*)\|', re.M)
    found = pattern.findall(block)
    if len(found) != 1:
        fail(f'expected exactly one decision-desk row, found {len(found)}')
    counts = {}
    for part in DESK_PARTS:
        match = re.search(r'(\d+)\s+' + re.escape(part), found[0])
        if match is None:
            fail(f'decision-desk row does not state a number for {part!r}')
        counts[part] = int(match.group(1))
    return counts


def published_pages() -> list[Path]:
    return [
        path for path in ROOT.rglob('*.html')
        if not (set(path.relative_to(ROOT).parts[:-1]) & SKIP_DIRS)
    ]


def measured_tree() -> dict[str, int]:
    pages = published_pages()
    canonical = og_image = described = 0
    for page in pages:
        text = page.read_text(encoding='utf-8', errors='ignore')
        if 'rel="canonical"' in text:
            canonical += 1
        if 'og:image' in text:
            og_image += 1
        match = re.search(r'<meta name="description" content="([^"]*)"', text)
        if match is not None and len(match.group(1)) >= DESCRIPTION_MIN:
            described += 1
    return {
        'html_pages': len(pages),
        'canonical_pages': canonical,
        'og_image_pages': og_image,
        'described_pages': described,
    }


def readme_block() -> str:
    text = README.read_text(encoding='utf-8')
    start = f'<!-- {README_MARK} -->'
    end = f'<!-- /{README_MARK} -->'
    if text.count(start) != 1 or text.count(end) != 1:
        fail(f'{README.name} must contain exactly one {README_MARK} block')
    return text.split(start, 1)[1].split(end, 1)[0]


def design_section() -> str:
    text = DESIGN.read_text(encoding='utf-8')
    matches = list(re.finditer(r'^## 3\..*?(?=^## 4\.)', text, re.M | re.S))
    if len(matches) != 1:
        fail('could not find exactly one measured section 3 in DESIGN_PROMPT.md')
    return matches[0].group(0)


def actual_feed_count() -> int:
    doc = ET.parse(FEED).getroot()
    channel = doc.find('channel')
    if doc.tag != 'rss' or channel is None:
        fail('feed.xml must be an RSS document with a channel')
    return len(channel.findall('item'))


def main() -> int:
    actual = actual_feed_count()
    candidates = build_feed.union_entries(indexable=False)
    candidate_urls = {entry['link'] for entry in candidates}
    if len(candidate_urls) != len(candidates):
        fail('feed candidate union contains duplicate URLs')
    sitemap_urls = build_feed.sitemap_urls()
    sitemap_eligible = [entry for entry in candidates if entry['link'] in sitemap_urls]
    expected, _noindex_drops = build_feed.noindex_targets(sitemap_eligible)
    if len(expected) != actual:
        fail(f'feed.xml has {actual} items but current feed inputs build {len(expected)}')

    readme_count = table_count(readme_block(), 'Published RSS items (XML channel items)')
    if readme_count != actual:
        fail(f'README says {readme_count} published RSS items; feed.xml has {actual}')

    section = design_section()
    publication = json.loads(PUBLICATION.read_text(encoding='utf-8'))
    flag_register = json.loads(FLAGS.read_text(encoding='utf-8'))
    tree = measured_tree()
    if tree['canonical_pages'] != tree['html_pages']:
        fail(
            f'{tree["html_pages"]} published HTML pages but {tree["canonical_pages"]} carry rel="canonical"; '
            'the design brief claims full coverage'
        )
    observed = {
        key: table_count(section, label)
        for label, key in DESIGN_ROWS.items()
    }
    expected_counts = {
        'html_pages': tree['html_pages'],
        'indexable_urls': len(publication['indexable_pages']),
        'guides': len(publication['guides']),
        'sitemap_urls': len(sitemap_urls),
        'candidate_count': len(candidates),
        'sitemap_omitted': len(candidates) - len(sitemap_eligible),
        'feed_count': actual,
        'sources': len(publication['sources']),
        'flags': len(flag_register['flags']),
    }
    for key, expected_value in expected_counts.items():
        if observed[key] != expected_value:
            label = next(label for label, row_key in DESIGN_ROWS.items() if row_key == key)
            fail(f'DESIGN_PROMPT.md says {observed[key]} for {label}; current value is {expected_value}')

    for label, key in DESIGN_RATIO_ROWS.items():
        matched, total = ratio_count(section, label)
        if (matched, total) != (tree[key], tree['html_pages']):
            fail(
                f'DESIGN_PROMPT.md says {matched} / {total} for {label}; '
                f'current value is {tree[key]} / {tree["html_pages"]}'
            )

    desk = desk_counts(section)
    expected_desk = {
        'paths': len(publication['paths']),
        'proposals': len(publication['proposals']),
        'questions': len(publication['questions']),
        'brief blocks': len(publication['design_prompt']['blocks']),
    }
    for part, expected_value in expected_desk.items():
        if desk[part] != expected_value:
            fail(f'DESIGN_PROMPT.md says {desk[part]} {part}; the register has {expected_value}')

    omitted = len(candidates) - len(sitemap_eligible)
    print(
        f'FEED/README/DESIGN COUNTS PASS — {actual} published RSS items; '
        f'{len(candidates)} post-retirement register candidates; {omitted} omitted by the sitemap filter; '
        f'{tree["html_pages"]} HTML pages; {len(publication["indexable_pages"])} indexable URLs; '
        f'{len(publication["guides"])} guides; {len(publication["proposals"])} proposals; '
        f'{len(publication["questions"])} questions; {len(publication["design_prompt"]["blocks"])} brief blocks.'
    )
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except (OSError, ET.ParseError, ValueError) as exc:
        print(f'FEED/README CHECK FAILED: {exc}', file=sys.stderr)
        sys.exit(1)
