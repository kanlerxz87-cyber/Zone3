#!/usr/bin/env python3
"""Strict release gate for the current publication, not a semantic fact-check claim.

Checks provenance structure, actual shared disclosure markup, no unsupported product
figures, separate intent fields, honest authorship, one measurement runtime, canonical
indexing, guide feed coverage and retained dashboard access. Inherited gates still run.
"""
from __future__ import annotations

import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
import publication_chrome as chrome
import build_publication

OFFICIAL = {'www.amazon.com', 'amazon.com', 'affiliate-program.amazon.com', 'www.ftc.gov',
            'developers.google.com', 'docs.github.com', 'www.foodsafety.gov', 'github.com'}
SKIP = {'.git', 'archive', 'docs', 'sessions', 'node_modules', '.preview', '.local', '__pycache__'}


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.attrs = []
        self.rows = []
        self.row = None
        self.in_tbody = False
        self.text = []
        self.ignore = 0
        self.duplicates = set()
        self.ids = set()

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.attrs.append((tag, attrs))
        if attrs.get('id'):
            if attrs['id'] in self.ids:
                self.duplicates.add(attrs['id'])
            self.ids.add(attrs['id'])
        if tag in {'script', 'style'}:
            self.ignore += 1
        if tag == 'tbody':
            self.in_tbody = True
        if tag == 'tr' and self.in_tbody:
            self.row = []
        if tag == 'a' and self.row is not None:
            self.row.append(attrs.get('href', ''))

    def handle_endtag(self, tag):
        if tag == 'tr' and self.row is not None:
            self.rows.append(self.row)
            self.row = None
        if tag == 'tbody':
            self.in_tbody = False
        if tag in {'script', 'style'}:
            self.ignore = max(0, self.ignore - 1)

    def handle_data(self, data):
        if not self.ignore:
            self.text.append(data)


def check() -> list[str]:
    errors = []
    def need(condition, label):
        if not condition:
            errors.append(label)

    data = json.loads((ROOT / 'data/publication.json').read_text())
    source_ids = {s['id'] for s in data['sources']} | {p['id'] for p in data['products']}
    need(len(data['products']) == 5, 'exactly the five supplied products must be registered')
    need(len({p['submitted_link'] for p in data['products']}) == 5, 'duplicate submitted product')
    inherited = {p['submitted_link']: p for p in json.loads((ROOT / 'data/shop/products.json').read_text())['products']}
    for p in data['products']:
        need(p['submitted_link'] in inherited, f'{p["id"]}: unknown supplied link')
        need(p['observed_listing_url'] == 'https://www.amazon.com/dp/' + p['observed_asin'], f'{p["id"]}: malformed official observed URL')
        need(bool(re.fullmatch('[A-Z0-9]{10}', p['observed_asin'])), f'{p["id"]}: malformed observed ASIN')
        for key in ('price', 'rating', 'review_count', 'tested_performance'):
            need(p[key] is None, f'{p["id"]}: unsupported {key} must remain empty')
        for key in ('intended_asin', 'official_listing_url', 'intent_confirmed_on', 'intent_confirmation_source'):
            need(p[key] == inherited[p['submitted_link']][key], f'{p["id"]}: intended field drifted from the confirmation register ({key})')
        if p['intended_asin']:
            need(all(p[k] for k in ('official_listing_url', 'intent_confirmed_on', 'intent_confirmation_source')), f'{p["id"]}: incomplete intent confirmation')
    for source in data['sources']:
        need(urlsplit(source['url']).scheme == 'https' and urlsplit(source['url']).hostname in OFFICIAL, f'{source["id"]}: source must use an actual approved official hostname')
        need(bool(source['checked_on'] and source['scope']), f'{source["id"]}: missing verification date/scope')
    for guide in data['guides']:
        for section in guide['sections']:
            need(bool(section.get('source_ids')), f'{guide["slug"]}: section lacks source context')
            need(all(s in source_ids for s in section.get('source_ids', [])), f'{guide["slug"]}: unknown section source')
        need(all(slug in {g['slug'] for g in data['guides']} for slug in guide['related']), f'{guide["slug"]}: unknown related guide')

    # b580d790 (2026-11-19): a reviewer must be able to act on every proposal and every
    # open question without guessing. Each needs a concrete next action, the facts that
    # action would settle, and an explicit statement of who can unblock it.
    for proposal in data['proposals']:
        need(bool(proposal.get('next_action')), f'{proposal["id"]}: no concrete next action for the reviewer')
        need(len(proposal.get('discoveries', [])) >= 2, f'{proposal["id"]}: needs the missing facts the action would reveal')
        need(isinstance(proposal.get('owner_input_needed'), bool), f'{proposal["id"]}: who-must-act flag missing')
    for question in data['questions']:
        for key in ('known', 'missing', 'discovery', 'default'):
            need(bool(question.get(key)), f'{question["id"]}: incomplete decision-readiness field {key}')
        need(isinstance(question.get('owner_input_needed'), bool), f'{question["id"]}: who-can-unblock flag missing')
    need(bool(data['meta'].get('reverified')), 'publication must state the date its sources were last re-checked')

    current = {rel for rel in build_publication.outputs() if rel.endswith('.html') and rel != 'publication-prior.html'}
    # --- E41-T6 (session 41e84402): 121 of the 164 rows in data/flags.json carry no status at all,
    # which is why the review page cannot be split into open / resolved / historical (S-11). No status
    # is asserted onto a historical row from here; what can be done is stop the backlog growing —
    # any row that records the date it was raised must also record a status.
    for f in json.loads((ROOT / 'data/flags.json').read_text(encoding='utf-8'))['flags']:
        if f.get('raised'):
            need(bool(str(f.get('status', '')).strip()), f"{f['id']}: a dated flag row must carry a status (E41-B01)")

    # --- E41-T4 (session 41e84402, 2026-11-19): counts in prose cannot be maintained, only derived.
    # Session 07fb37ba's gate above compares the executive-brief totals to the registers. This part
    # closes the rest of the measured drift: a reader-facing sentence, a README line or a register
    # field that states how many guides/questions/pages there are must agree with the register, or
    # say nothing at all. Dated records (another session's review round, the meta notes) are excluded:
    # a record written on a date is that date's truth and must not be quietly rewritten.
    cats = {}
    for prod in data['products']:
        cats[prod['category']] = cats.get(prod['category'], 0) + 1
    counts = {  # exact register labels only, and the numeral must sit right in front of them
        'question-led guides': len(data['guides']),
        'question-led buyer guides': len(data['guides']),
        'decision-readiness questions': len(data['questions']),
        'canonical reader URLs': len(data['indexable_pages']),
        'air-fryer listings': cats.get('air-fryers', 0),
        'meat-thermometer listings': cats.get('meat-thermometers', 0),
        'thermometer listings': cats.get('meat-thermometers', 0),
        'kitchen categories': len(cats),
    }
    words = {'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5, 'six': 6, 'seven': 7, 'eight': 8,
             'nine': 9, 'ten': 10, 'eleven': 11, 'twelve': 12, 'thirteen': 13, 'fourteen': 14,
             'fifteen': 15, 'sixteen': 16, 'seventeen': 17, 'eighteen': 18, 'nineteen': 19, 'twenty': 20,
             'twenty-four': 24}

    # A qualifier and a line break between the number and the label must not hide the claim:
    # "eight practical\nquestion-led guides" is still a count claim about the guide register. Only a short
    # closed list of descriptive adjectives is allowed in the gap, so a roadmap sentence about shipping
    # "eight new guides" is not mistaken for a statement about what the register holds.
    NUMBER = r'(\d{1,3}|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|twenty-four)'
    GAP = r'(?:\s+(?:practical|published|current|dated|scoped|working|question-led|buyer))*\s+'

    def claims(text: str, label: str) -> None:
        for phrase, expected in counts.items():
            pat = re.compile(NUMBER + GAP + re.escape(phrase) + r'\b', re.I | re.S)
            for m in pat.finditer(text):
                said = words.get(m.group(1).lower(), None)
                if said is None and m.group(1).isdigit():
                    said = int(m.group(1))
                if said is not None and said != expected:
                    need(False, f'{label}: states {said} {phrase}; the register holds {expected}. Derive it or make the sentence count-neutral')

    readme = (ROOT / 'README.md').read_text(encoding='utf-8')
    facts = re.search(r'<!-- z3:register-facts -->(.*?)<!-- /z3:register-facts -->', readme, re.S)
    need(bool(facts), 'README.md must carry the generated z3:register-facts block')
    if facts:
        rows = dict(re.findall(r'\| ([^|]+?) \| (\d+) \|', facts.group(1)))
        expect = {'Question-led guides': len(data['guides']), 'Indexable reader URLs': len(data['indexable_pages']),
                  'Supplied product links': len(data['products']), 'Open decision-readiness questions': len(data['questions']),
                  'Suggestions on the desk': len(data['proposals']), 'Paths a reviewer can choose': len(data['paths']),
                  'Design-brief blocks': len(data['design_prompt']['blocks']), 'Scoped official references': len(data['sources'])}
        for key, value in expect.items():
            need(rows.get(key) == str(value), f'README register-facts row {key!r}: README says {rows.get(key)}, register says {value}')
        # Current-state prose is everything outside the generated block and outside a dated section:
        # a release record or session log is allowed to state what was true when it was written, a
        # description of what the repository holds today is not. Scanning only the intro paragraph left
        # the ownership bullets unchecked, which is where the counts kept getting retyped.
        DATED = re.compile(r'^#{2,3}\s+.*(record|history|log|session|update|archive)', re.I | re.S)

        def current_state(text: str) -> str:
            keep, live = [], True
            for line in text.split('\n'):
                if line.startswith('## '):
                    live = not DATED.search(line + '\n')
                keep.append(line if live else '')
            return '\n'.join(keep)

        prose = readme.replace(facts.group(0), '')
        claims(current_state(prose), 'README.md current-state prose')
    for key in ('proposals', 'questions', 'paths'):
        for row in data[key]:
            claims(json.dumps(row, ensure_ascii=False), f'data/publication.json {key} {row.get("id", "?")}')
    claims(json.dumps(data['design_prompt'], ensure_ascii=False), 'data/publication.json design_prompt')
    for rel in sorted(current):
        if not rel.endswith('.html') or rel == 'publication-prior.html':
            continue
        html_text = (ROOT / rel).read_text(encoding='utf-8')
        visible = ' '.join(re.sub(r'<[^>]+>', ' ', html_text).split())
        round_pos = html_text.find('id="review-round-')
        if round_pos != -1:  # the dated round keeps its own wording; check only the copy around it
            visible = ' '.join(re.sub(r'<[^>]+>', ' ', html_text[:round_pos] + html_text[html_text.find('</section>', round_pos):]).split())
        claims(visible, rel)

    pages = [p for p in ROOT.rglob('*.html') if not any(part in SKIP for part in p.relative_to(ROOT).parts)]
    indexable = set(data['indexable_pages'])
    indexed = set()
    row_count = 0
    for path in sorted(pages):
        rel = path.relative_to(ROOT).as_posix()
        raw = path.read_text(encoding='utf-8')
        parsed = Page()
        parsed.feed(raw)
        header = re.search(r'<header\b[^>]*\bp26-header\b.*?</header>', raw, re.S)
        banner = re.search(r'<aside\b[^>]*\bp26-disclosure\b.*?</aside>', raw, re.S)
        main = re.search(r'<main\b', raw)
        need(header is not None and banner is not None and main is not None, f'{rel}: missing shared masthead/disclosure/main')
        if header and banner and main:
            need(header.end() <= banner.start() < main.start(), f'{rel}: disclosure must be under masthead before content')
            need(chrome.DISCLOSURE in banner.group(), f'{rel}: disclosure sentence not inside banner')
            need(not re.search(r'\bhidden\b|display\s*:\s*none|<button\b', banner.group(), re.I), f'{rel}: disclosure hidden or dismissable')
            need(sum(tag == 'header' and 'p26-header' in attrs.get('class', '').split() for tag, attrs in parsed.attrs) == 1, f'{rel}: duplicate masthead')
        footer = re.search(r'<footer\b[^>]*\bp26-footer\b.*?</footer>', raw, re.S)
        need(footer is not None and chrome.DISCLOSURE in footer.group(), f'{rel}: missing footer disclosure')
        scripts = [a.get('src', '') for tag, a in parsed.attrs if tag == 'script' and a.get('src')]
        need(sum(src.endswith('/measure.js') for src in scripts) == 1, f'{rel}: exactly one measurement runtime required')
        need(not any(src.endswith('/track.js') for src in scripts), f'{rel}: retired tracker still active')
        canonicals = [a.get('href') for tag, a in parsed.attrs if tag == 'link' and a.get('rel') == 'canonical']
        need(canonicals == [chrome.canonical(rel)], f'{rel}: canonical must be unique and normalized')
        robots = [a.get('content', '') for tag, a in parsed.attrs if tag == 'meta' and a.get('name') == 'robots']
        need(len(robots) == 1, f'{rel}: one explicit indexing policy required')
        if robots and 'noindex' not in robots[0]:
            indexed.add(rel)
        if rel not in current:
            continue
        if rel == 'executive-brief.html':
            summary = re.search(r'<div class="p26-summary-strip">(.*?)</div><section', raw, re.S)
            values = re.findall(r'<b>(\d+)</b><span>(.*?)</span>', summary.group(1) if summary else '')
            expected = [
                (str(len(data['products'])), 'submitted product links'),
                (str(len(data['guides'])), 'question-led buyer guides'),
                (str(len(data['questions'])), 'decision-readiness questions'),
                (str(len(json.loads((ROOT / 'data/shop/campaign-ledger.json').read_text())['rows'])), 'campaign evidence rows'),
            ]
            need(values == expected, f'{rel}: summary counts must match the product, guide, question, and campaign registers (expected {expected}, got {values})')
        need(not parsed.duplicates, f'{rel}: duplicate HTML ids {parsed.duplicates}')
        need(sum(tag == 'h1' for tag, _ in parsed.attrs) == 1, f'{rel}: exactly one main heading required')
        text = ' '.join(parsed.text)
        for pattern in (r'\$\s*\d', r'\d(?:\.\d)?\s*(?:stars|out of 5)', r'\b\d[\d,]*\s+(?:reviews|ratings)\b', r'\bwe tested\b', r'\bin our test kitchen\b'):
            need(not re.search(pattern, text, re.I), f'{rel}: prohibited unsupported figure/claim ({pattern})')
        for row in parsed.rows:
            row_count += 1
            need(any(urlsplit(h).scheme == 'https' and urlsplit(h).hostname in OFFICIAL for h in row), f'{rel}: each current table row needs an official HTTPS source')
        for tag, attrs in parsed.attrs:
            if tag == 'a':
                host = urlsplit(attrs.get('href', '')).hostname or ''
                if host in {'www.amazon.com', 'amazon.com', 'link.amazon'}:
                    need('sponsored' in attrs.get('rel', '').split(), f'{rel}: unsponsored product/source link')
            if tag == 'img':
                src = attrs.get('src', '')
                need(not urlsplit(src).scheme, f'{rel}: images must be local approved editorial assets')
                need((path.parent / src).is_file(), f'{rel}: missing image {src}')
                need(bool(attrs.get('alt')), f'{rel}: image needs an honest alt description')
                need(bool(attrs.get('width') and attrs.get('height')), f'{rel}: image dimensions required to reduce layout shift')
        if rel.startswith('guides/') and rel != 'guides/index.html':
            schemas = re.findall(r'<script type="application/ld\+json">(.*?)</script>', raw, re.S)
            article = json.loads(schemas[0]) if schemas else {}
            need(article.get('@type') == 'Article' and article.get('author', {}).get('@type') == 'Organization', f'{rel}: actual publisher organization required; no fictional person')
            need('not a hands-on review' in text.lower(), f'{rel}: guide must state its evidence limit')
            need(article.get('dateModified') == data['meta']['updated'], f'{rel}: date/schema drift')

    need(indexed == indexable, f'Index policy drift: extra={indexed-indexable}, missing={indexable-indexed}')
    # b580d790 (2026-11-19): search engines must be able to tell these pages apart.
    # Two indexable pages sharing a title or a description was a real defect (B79-F-01).
    seen_titles: dict[str, str] = {}
    seen_descs: dict[str, str] = {}
    for rel in sorted(indexable):
        raw = (ROOT / rel).read_text(encoding='utf-8')
        title_match = re.search(r'<title>(.*?)</title>', raw, re.S)
        desc_match = re.search(r'<meta name="description" content="([^"]*)"', raw)
        title = (title_match.group(1).strip() if title_match else '')
        desc = (desc_match.group(1).strip() if desc_match else '')
        need(bool(title) and 20 <= len(title) <= 85, f'{rel}: unique, reasonably sized title required')
        need(bool(desc) and 60 <= len(desc) <= 165, f'{rel}: unique, reasonably sized meta description required')
        need(title not in seen_titles, f'{rel}: duplicate title also used by {seen_titles.get(title)}')
        need(desc not in seen_descs, f'{rel}: duplicate description also used by {seen_descs.get(desc)}')
        seen_titles[title] = rel
        seen_descs[desc] = rel
    sitemap = ET.parse(ROOT / 'sitemap.xml')
    urls = [x.text for x in sitemap.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}loc')]
    need(set(urls) == {chrome.canonical(p) for p in indexable} and len(urls) == len(indexable), 'sitemap must contain exactly the canonical reader set, without noindex pages or duplicates')
    feed_urls = [x.text for x in ET.parse(ROOT / 'feed.xml').findall('.//item/link')]
    for guide in data['guides']:
        url = chrome.BASE + 'guides/' + guide['slug'] + '.html'
        need(feed_urls.count(url) == 1 and url in urls, f'{guide["slug"]}: guide must appear once in feed and sitemap')
    prior = (ROOT / 'publication-prior.html').read_text()
    need(prior.count('<!-- c17d25fd:shopfront -->') == 1 and 'id="decision-heading"' in prior, 'completed C3/C17 composition and decision handoff must remain reachable in the previous edition')
    need('flagged.html#C3-F-01' in prior and 'noindex,follow' in prior, 'historical edition needs its provenance caveat and noindex policy')
    need('C3-F-01' in {f['id'] for f in json.loads((ROOT / 'data/flags.json').read_text())['flags']}, 'upstream provenance finding must be retained')
    root = (ROOT / 'index.html').read_text()
    for _, links in chrome.WORKSPACE_GROUPS:
        for rel, label in links:
            need(root.count('href="' + rel + '"') >= 2, f'{rel}: dashboard must be directly reachable from one nav group AND footer')
    cfg = json.loads((ROOT / 'data/shop/measurement.json').read_text())
    events = [e['name'] for e in cfg['events']]
    need(events == ['page_view', 'outbound_click', 'guide_view', 'intent_view', 'flag_view'], 'single five-event schema must be versioned if changed')
    ledger = json.loads((ROOT / 'data/shop/campaign-ledger.json').read_text())
    need(ledger['rows'] == [], 'no authorized first-party campaign report was supplied; ledger must stay empty')
    need(not cfg['enabled'] and not cfg['endpoint_url'], 'no durable endpoint evidence exists in this release; production must remain off')
    print(f'Publication gate: {len(pages)} current HTML pages, {len(current)} rendered reader/workspace pages, {row_count} official-source table rows, {len(indexed)} indexable URLs, {len(feed_urls)} feed entries')
    return errors


if __name__ == '__main__':
    problems = check()
    for problem in problems:
        print('FAIL ' + problem)
    print('PUBLICATION ' + ('FAIL' if problems else 'PASS'))
    sys.exit(int(bool(problems)))
