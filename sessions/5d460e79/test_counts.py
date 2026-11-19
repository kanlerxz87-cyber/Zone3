#!/usr/bin/env python3
"""Gate: no reader-facing count may be typed into the publication generator.

Session 5d460e79, 2026-11-19. Fixes audit finding 5D4-F02/F03.

WHY
---
On the base commit, `executive-brief.html` advertised "6 question-led buyer guides"
and "9 decision-readiness questions" while `data/publication.json` held 8 and 24.
Two paragraphs on `suggestions/index.html` said "the current six guides" against a
register of eight. Every one of those numbers was a literal typed into
`tools/build_publication.py`, so nothing failed when the register grew.

WHAT THIS CHECKS
----------------
1. Counted nouns in the generator's prose must not be preceded by a typed numeral.
   "six guides", "9 questions", "<b>6</b>", "Seven ways" are all failures unless the
   number is produced by numeral()/len().
2. The rendered pages must agree with the register: the executive-brief summary strip
   is parsed and each figure compared with len(products)/len(guides)/len(questions).

Exit 1 on any mismatch so tools/publish.py blocks the release.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2] if (Path(__file__).resolve().parents[2] / 'data').exists() else Path('/home/user/Zone3')
GEN = ROOT / 'tools' / 'build_publication.py'
DATA = json.loads((ROOT / 'data' / 'publication.json').read_text(encoding='utf-8'))
NUMERAL_WORDS = ('one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve')

failures: list[str] = []

# --- 1. source-level: typed counts in prose -------------------------------------
source = GEN.read_text(encoding='utf-8')
# Strip the NUMERALS table and its helper, which legitimately contain the words.
# Remove what legitimately holds numerals: the NUMERALS table, the numeral() helper,
# Python comments (which may quote a historical number as an example), and any HTML
# attribute value (data-* hooks, aria labels, ids) where a digit is not a reader-facing count.
scan = re.sub(r'NUMERALS = \{.*?\}', '', source, flags=re.S)
scan = re.sub(r'def numeral\(.*?\n\n', '', scan, flags=re.S)
scan = re.sub(r'^\s*#.*$', '', scan, flags=re.M)
scan = re.sub(r'="[^"]*"', '=""', scan)
# SVG path/diagram data is geometry, not prose: 'm-88 28h88' contains sequences the
# word-numeral rule would otherwise read as text. Strip SVG bodies entirely.
scan = re.sub(r'<svg\b.*?</svg>', '', scan, flags=re.S)

COUNTED_NOUNS = (r'guides?|questions?|proposals?|products?|ways|titles|paths|sources?'
                 r'|rows?|pages?|events?|listings?|categories|blocks?|steps?')

typed = []
# typed word-numeral directly before a counted noun: "six guides", "seven ways".
# A cadence is not a count: "review one guide every 14 days" is an operating instruction,
# so the pattern is skipped when the numeral is followed by a repeat interval.
for m in re.finditer(rf'\b(?:{NUMERAL_WORDS})\s+(?:{COUNTED_NOUNS})\b', scan, re.I):
    tail = scan[m.end():m.end() + 40]
    if re.match(r'\s+(?:every|per|a|an)\b', tail, re.I):
        continue
    line = scan[:m.start()].count('\n') + 1
    typed.append(f'line {line}: "{m.group(0)}"')
# typed digit before a counted noun: "9 questions" (but not inside an attribute or CSS)
for m in re.finditer(rf'(?<![\w.-])(\d{{1,2}})\s+(?:{COUNTED_NOUNS})\b', scan):
    line = scan[:m.start()].count('\n') + 1
    typed.append(f'line {line}: "{m.group(0)}"')
for row in typed:
    failures.append(f'typed count in build_publication.py — {row}')

# --- 2. rendered page must agree with the register ------------------------------
brief = ROOT / 'executive-brief.html'
if not brief.exists():
    failures.append('executive-brief.html is missing; run tools/build_publication.py')
else:
    html = brief.read_text(encoding='utf-8')
    strip = re.search(r'<div class="p26-summary-strip">(.*?)</div>\s*</div>', html, re.S)
    if not strip:
        failures.append('executive-brief.html: summary strip not found')
    else:
        found = {label: value for value, label in
                 re.findall(r'<b>([^<]+)</b><span>([^<]+)</span>', strip.group(1))}
        expected = {
            'submitted product links': len(DATA['products']),
            'question-led buyer guides': len(DATA['guides']),
            'decision-readiness questions': len(DATA['questions']),
        }
        for label, want in expected.items():
            got = found.get(label)
            if got is None:
                failures.append(f'executive-brief.html: no figure for "{label}"')
            elif got.strip() != str(want):
                failures.append(f'executive-brief.html: "{label}" says {got.strip()}, register holds {want}')

# --- 3. the suggestions page must not state a stale guide count -----------------
sugg = ROOT / 'suggestions' / 'index.html'
if sugg.exists():
    text = sugg.read_text(encoding='utf-8')
    for m in re.finditer(rf'current\s+({NUMERAL_WORDS}|\d+)\s+guides', text, re.I):
        word = m.group(1).lower()
        words = dict(zip(NUMERAL_WORDS.split('|'), range(1, 13)))
        stated = int(word) if word.isdigit() else words.get(word)
        if stated != len(DATA['guides']):
            failures.append(f'suggestions/index.html: says "current {word} guides", register holds {len(DATA["guides"])}')

# --- 4. the two indexable "front" URLs must not be near-duplicates -----------------
# 5D4-F04: index.html and shop/index.html were 65% the same words, both index,follow and
# both in sitemap.xml. 0.40 is well clear of a normal shared masthead/footer.
import difflib


def _visible(path: Path) -> list[str]:
    if not path.exists():
        return []
    t = path.read_text(encoding='utf-8')
    for pat in (r'<header.*?</header>', r'<footer.*?</footer>', r'<nav.*?</nav>',
                r'<script.*?</script>', r'<style.*?</style>'):
        t = re.sub(pat, '', t, flags=re.S)
    return re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', t)).lower().split()


_home, _shop = _visible(ROOT / 'index.html'), _visible(ROOT / 'shop' / 'index.html')
if _home and _shop:
    ratio = difflib.SequenceMatcher(None, _home, _shop).ratio()
    if ratio > 0.40:
        failures.append(f'index.html and shop/index.html are {ratio:.0%} the same words; '
                        f'they must do different jobs (threshold 40%)')

# --- 5. every indexable page must be reachable, and the comparison well-linked ------
# 5D4-F05 (corrected): shop/products/index.html is not an orphan — it is linked from the
# catalogue, both category pages and the masthead. What the check below enforces is the
# weaker, true property: no indexable page may have zero inbound internal links.

def _inbound(rel: str) -> int:
    needle = rel
    count = 0
    for f in ROOT.rglob('*.html'):
        if f.relative_to(ROOT).parts[0] in {'archive', 'sessions', 'docs', 'node_modules', '.git'}:
            continue
        if f.relative_to(ROOT).as_posix() == rel:
            continue
        if needle in f.read_text(encoding='utf-8', errors='replace'):
            count += 1
    return count


for _rel in DATA['indexable_pages']:
    if _rel in {'index.html'}:
        continue
    _n = _inbound(_rel)
    if _n == 0:
        failures.append(f'{_rel} is indexable but no other page links to it')

# --- 6. the front page must keep a direct, tagged route to every product -----------
# Caught during this session: removing the duplicated product cards to fix 5D4-F04
# stripped every Amazon link from the front page, leaving the site's main entry point
# with no conversion path at all. Distinctness must never be bought with reachability.
_home_text = (ROOT / 'index.html').read_text(encoding='utf-8') if (ROOT / 'index.html').exists() else ''
if _home_text:
    _tagged = set(re.findall(r'href="https://www\.amazon\.com/dp/([A-Z0-9]{10})\?tag=' + re.escape(
        json.loads((ROOT / 'data' / 'shop' / 'config.json').read_text(encoding='utf-8'))['associates_tracking_id']), _home_text))
    _want = {p['observed_asin'] for p in DATA['products']}
    _missing = _want - _tagged
    if _missing:
        failures.append(f'index.html is missing a tagged product link for: {", ".join(sorted(_missing))}')
    if 'rel="sponsored' not in _home_text:
        failures.append('index.html product links are not marked rel=sponsored')

if failures:
    print(f'FAIL: {len(failures)} count/drift problem(s)')
    for f in failures[:20]:
        print(' -', f)
    sys.exit(1)
print(f'PASS: counts — {len(DATA["guides"])} guides, {len(DATA["questions"])} questions, '
      f'{len(DATA["products"])} products; no typed numerals in prose')
