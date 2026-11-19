#!/usr/bin/env python3
"""E41-T1 measurement (session 41e84402, 2026-11-19). Read-only; prints JSON.

Answers, from this checkout only:
  1. does any live (undated) reader page, README line or register field assert a register count
     that the register does not hold?
  2. what does each reader page actually carry (title, description, canonical, robots, og:image,
     JSON-LD, disclosure strip, sponsored product links, chooser, sticky CSS)?
  3. can the per-centimetre analysis (brief S-23) be computed from the data this repository holds?

Dated records are reported separately and never "fixed": a sentence written for another session's
round was true on its own date. Re-run after every register change:
    python3 sessions/41e84402/measure_drift.py > sessions/41e84402/measurement-2026-11-19-drift.json
"""
from __future__ import annotations
import json, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
DATA = json.loads((ROOT / 'data/publication.json').read_text(encoding='utf-8'))
WORDS = {w: i for i, w in enumerate('zero one two three four five six seven eight nine ten eleven twelve '
        'thirteen fourteen fifteen sixteen seventeen eighteen nineteen twenty'.split())}
WORDS['twenty-four'] = 24
COUNTS = {'question-led guides': len(DATA['guides']), 'question-led buyer guides': len(DATA['guides']),
          'decision-readiness questions': len(DATA['questions']), 'canonical reader URLs': len(DATA['indexable_pages'])}
DATED_KEYS = {'review_b9008684', 'meta'}


def visible(html_text: str) -> str:
    html_text = re.sub(r'<script.*?</script>|<style.*?</style>', ' ', html_text, flags=re.S)
    return ' '.join(re.sub(r'<[^>]+>', ' ', html_text).split())


def claims(text: str):
    out = []
    for phrase, expected in COUNTS.items():
        for m in re.finditer(r'\b(\d{1,3}|' + '|'.join(list(WORDS)[1:15]) + r'|twenty-four)\s+' + re.escape(phrase) + r'\b', text, re.I):
            said = WORDS.get(m.group(1).lower(), int(m.group(1)) if m.group(1).isdigit() else None)
            out.append({'phrase': phrase, 'said': said, 'register': expected,
                        'context': text[max(0, m.start() - 60):m.end() + 20]})
    return out


def main() -> int:
    reader = sorted(set(DATA['indexable_pages']) & {p.relative_to(ROOT).as_posix() for p in ROOT.glob('**/*.html')})
    report = {'registers': {**COUNTS, 'products': len(DATA['products']), 'proposals': len(DATA['proposals']),
                            'paths': len(DATA['paths']), 'sources': len(DATA['sources'])},
              'sitemap_urls': len(re.findall(r'<loc>', (ROOT / 'sitemap.xml').read_text())),
              'feed_entries': (ROOT / 'feed.xml').read_text().count('<item>'),
              'search_index_rows': len(json.loads((ROOT / 'assets/publication-search.json').read_text())),
              'count_claims': {}, 'structure': {}, 's23_dimension_check': {}}
    for rel in reader:
        text = visible((ROOT / rel).read_text(encoding='utf-8'))
        found = [c for c in claims(text) if c['said'] != c['register']]
        if found:
            report['count_claims'][rel] = found
    readme = (ROOT / 'README.md').read_text(encoding='utf-8')
    preamble = readme[:readme.index('\n## ')]
    preamble = re.sub(r'<!-- z3:register-facts -->.*?<!-- /z3:register-facts -->', ' ', preamble, flags=re.S)
    bad = [c for c in claims(preamble) if c['said'] != c['register']]
    if bad:
        report['count_claims']['README.md preamble'] = bad
    for key in ('proposals', 'questions', 'paths'):
        for row in DATA[key]:
            bad = [c for c in claims(json.dumps(row, ensure_ascii=False)) if c['said'] != c['register']]
            if bad:
                report['count_claims'][f'data/publication.json {key} {row.get("id")}'] = bad
    for s in DATA['design_prompt']['blocks']:
        bad = [c for c in claims(json.dumps(s, ensure_ascii=False)) if c['said'] != c['register']]
        if bad:
            report['count_claims'][f'data/publication.json design_prompt {s.get("id")}'] = bad
    for rel in reader:
        raw = (ROOT / rel).read_text(encoding='utf-8')
        amz = re.findall(r'<a[^>]*href="https?://www\.amazon\.com[^"]*"[^>]*>', raw)
        report['structure'][rel] = {
            'title_chars': len(re.search(r'<title>(.*?)</title>', raw, re.S).group(1)),
            'meta_description': bool(re.search(r'name="description" content="[^"]{60,165}"', raw)),
            'canonical': bool(re.search(r'rel="canonical"', raw)),
            'robots': (re.search(r'name="robots" content="([^"]+)"', raw) or [0, ''])[1],
            'og_image': 'property="og:image"' in raw,
            'json_ld': raw.count('application/ld+json'),
            'disclosure': bool(re.search(r'p26-disclosure|disclose-bar', raw)),
            'amazon_links': len(amz), 'amazon_links_sponsored': sum(1 for a in amz if 'sponsored' in a),
            'chooser': 'p26-chooser' in raw, 'comparison_anchor': 'id="comparison"' in raw,
            'sticky_compare_cells': '.p26-compare .p26-table tbody th{position:sticky' in (ROOT / 'assets/publication.css').read_text(),
        }
    # S-23: could the capacity-per-centimetre analysis be computed from what is held here?
    regs = ['data/publication.json', 'data/shop/products.json', 'data/z3/products.json', 'data/products.json']
    for rel in regs:
        p = ROOT / rel
        blob = p.read_text(encoding='utf-8') if p.exists() else ''
        fields = sorted({m.group(1) for m in re.finditer(r'"((?:[^"]*dimension[^"]*|[^"]*depth[^"]*|[^"]*width[^"]*|[^"]*height[^"]*))"\s*:', blob, re.I)})
        report['s23_dimension_check'][rel] = {'exists': p.exists(), 'dimension_like_fields': fields[:6]}
    report['drift_found'] = bool(report['count_claims'])
    print(json.dumps(report, indent=1, ensure_ascii=False))
    return 0


if __name__ == '__main__':
    sys.exit(main())
