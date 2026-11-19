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

    current = {rel for rel in build_publication.outputs() if rel.endswith('.html')}
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
    sitemap = ET.parse(ROOT / 'sitemap.xml')
    urls = [x.text for x in sitemap.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}loc')]
    need(set(urls) == {chrome.canonical(p) for p in indexable} and len(urls) == len(indexable), 'sitemap must contain exactly the canonical reader set, without noindex pages or duplicates')
    feed_urls = [x.text for x in ET.parse(ROOT / 'feed.xml').findall('.//item/link')]
    for guide in data['guides']:
        url = chrome.BASE + 'guides/' + guide['slug'] + '.html'
        need(feed_urls.count(url) == 1 and url in urls, f'{guide["slug"]}: guide must appear once in feed and sitemap')
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
