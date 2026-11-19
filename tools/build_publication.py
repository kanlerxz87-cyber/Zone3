#!/usr/bin/env python3
"""Render the canonical Zone3 Kitchen publication from data/publication.json.

No remote calls, paid APIs, account access or generative claims are hidden in this build.
Unknown product/intent/performance fields stay empty. The existing publication entry point
calls this module after rendering its historical records, so the documented build has one
owner for the reader front page. --check compares final, postprocessed output byte for byte.
"""
from __future__ import annotations

import argparse
import datetime as _dt
import importlib.util
import json
import re
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
import publication_chrome as chrome

DATA = json.loads((ROOT / 'data/publication.json').read_text(encoding='utf-8'))
PRODUCTS = {p['id']: p for p in DATA['products']}
GUIDES = {g['slug']: g for g in DATA['guides']}
SOURCES = {s['id']: s for s in DATA['sources']}
REVERIFIED = DATA['meta']['reverified']
esc = chrome.esc
icon = chrome.icon
NUMERALS = {1: 'One', 2: 'Two', 3: 'Three', 4: 'Four', 5: 'Five', 6: 'Six', 7: 'Seven', 8: 'Eight',
            9: 'Nine', 10: 'Ten', 11: 'Eleven', 12: 'Twelve', 13: 'Thirteen', 14: 'Fourteen',
            15: 'Fifteen', 16: 'Sixteen', 17: 'Seventeen', 18: 'Eighteen', 19: 'Nineteen', 20: 'Twenty'}


def numeral(n: int) -> str:
    """Spell a count out where prose reads better; fall back to digits beyond the table."""
    return NUMERALS.get(n, str(n))


def human_date(iso: str) -> str:
    """One date format for reader-facing copy, derived from the register rather than typed in."""
    d = _dt.date.fromisoformat(iso)
    return f'{d.day} {d:%b} {d.year}'


# Every "read on" / "updated on" label in the reader layer is derived from the register date, so a
# data refresh cannot leave a page asserting a stale check date. Previously these were typed.
READ_ON = human_date(DATA['meta']['updated'])  # register-owned: the day the reader-facing sources were read
GUIDE_N = len(DATA['guides'])


def load_module(path: str, name: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def source_link(source_id: str, label: str | None = None) -> str:
    if source_id in PRODUCTS:
        p = PRODUCTS[source_id]
        return f'<a href="{p["observed_listing_url"]}" rel="sponsored noopener">{esc(label or p["brand"] + " listing")}</a>'
    s = SOURCES[source_id]
    return f'<a href="{esc(s["url"])}">{esc(label or s["title"])}</a>'


# b580d790 (2026-11-19): buyer decision aids. Every sentence below is derived from the
# listing wording already stored for the product, or it is an explicitly labelled
# editorial question. No price, rating, test result or performance claim is introduced.
DECISION = {
    'SHOP-01': {
        'fits': 'You want to cook two different things at once and set them to finish together.',
        'not': 'You need one wide cooking surface for a single large item.',
        'ask': 'Does the sync-finish feature cover the meals you actually cook?',
    },
    'SHOP-02': {
        'fits': 'You would rather reach into a French-door oven than pull out a basket.',
        'not': 'Counter depth or door swing is already tight in your kitchen.',
        'ask': 'How much space does the door need in front of the unit?',
    },
    'SHOP-03': {
        'fits': 'One basket, one temperature, and the food all wants the same treatment.',
        'not': 'You routinely cook two different dishes at the same time.',
        'ask': 'Will the food you cook most often fit in a single layer?',
    },
    'SHOP-04': {
        'fits': 'You want a handheld spot check and will read the model instructions first.',
        'not': 'You need continuous readings while the food rests or roasts.',
        'ask': 'Where does the manual say to place the probe for a whole chicken?',
    },
    'SHOP-05': {
        'fits': 'You want readings on a phone and do not mind an app and a connection.',
        'not': 'You want no pairing, no account and no battery to manage.',
        'ask': 'What do the app requirements and probe limits say for your setup?',
    },
}

def format_art(kind: str, label: str = '') -> str:
    """Original generic format diagrams. Never presented as photographs of the exact SKU."""
    shapes = {
        'dual': '<rect x="65" y="38" width="190" height="166" rx="29" fill="#333f38"/><rect x="79" y="53" width="162" height="37" rx="12" fill="#263029"/><path d="M152 103v84" stroke="#7b867a"/><rect x="79" y="102" width="64" height="83" rx="15" fill="#414f44"/><rect x="163" y="102" width="64" height="83" rx="15" fill="#414f44"/><rect x="103" y="115" width="17" height="81" rx="6" fill="#b47c55"/><rect x="187" y="115" width="17" height="81" rx="6" fill="#b47c55"/><path d="M130 70h60" stroke="#b4bdac" stroke-linecap="round" stroke-width="3"/>',
        'basket': '<rect x="86" y="30" width="150" height="176" rx="37" fill="#313c35"/><path d="M88 108h145" stroke="#72816e"/><rect x="103" y="45" width="116" height="43" rx="18" fill="#27312b"/><path d="M143 65h36" stroke="#b4bdac" stroke-width="3" stroke-linecap="round"/><rect x="147" y="125" width="26" height="80" rx="9" fill="#b47c55"/><path d="M117 187h17m54 0h17" stroke="#657461" stroke-linecap="round"/>',
        'oven': '<rect x="45" y="48" width="230" height="150" rx="12" fill="#7e827b"/><rect x="57" y="61" width="206" height="28" rx="4" fill="#39443c"/><circle cx="83" cy="75" r="8" fill="#b47c55"/><circle cx="235" cy="75" r="8" fill="#b47c55"/><rect x="60" y="100" width="200" height="82" rx="4" fill="#29372e"/><path d="M160 100v82" stroke="#9ba392"/><path d="M144 110v58m32-58v58" stroke="#c2c5b7" stroke-width="5" stroke-linecap="round"/><path d="M80 126h48m64 0h48M80 148h48m64 0h48" stroke="#78846e"/><path d="M65 201v7m190-7v7" stroke="#384039" stroke-width="7"/>',
        'probe': '<g transform="rotate(-25 160 120)"><path d="M179 120h91" stroke="#868f83" stroke-width="6" stroke-linecap="round"/><path d="m270 120 15-1-15 5" fill="#868f83"/><rect x="44" y="89" width="139" height="61" rx="25" fill="#34463b"/><rect x="76" y="103" width="59" height="29" rx="5" fill="#c8d0b8"/><circle cx="155" cy="118" r="6" fill="#b47c55"/></g>',
        'wireless': '<rect x="77" y="116" width="166" height="80" rx="19" fill="#3c493e"/><path d="M86 134h148" stroke="#7b896f"/><path d="m98 45 19 101m40-113 3 113m60-104-19 104" stroke="#8b9586" stroke-width="5" stroke-linecap="round"/><path d="m98 45 6 32m53-44 1 33m62-24-6 32" stroke="#35483c" stroke-width="9" stroke-linecap="round"/><circle cx="159" cy="172" r="5" fill="#c9cfb8"/>',
    }
    return f'<svg class="p26-product-svg" viewBox="0 0 320 240" role="img" aria-label="{esc(label or "Generic " + kind + " format illustration; not product photography")}"><ellipse cx="160" cy="213" rx="107" ry="9" fill="#d7d9cc"/>{shapes[kind]}</svg>'


def guide_art(kind: str) -> str:
    if kind == 'hosting':
        return '<div class="p26-guide-art p26-art-hosting"><img src="../assets/img/publication-kitchen.jpg" alt="AI-generated editorial kitchen still life; not product testing" width="1536" height="1024" loading="lazy"></div>'
    artwork = {
        'formats': '<rect x="42" y="51" width="79" height="104" rx="15"/><rect x="170" y="56" width="113" height="94" rx="8"/><path d="M51 80h61m-30 15v44m100-55h88m-45 14v41m-10-38v31m20-31v31"/>',
        'capacity': '<rect x="73" y="43" width="174" height="121" rx="29"/><path d="M88 66h144m-72 9v69m-28-46v41m56-41v41"/><path d="M55 31v146m-8-138 8-8 8 8m-16 130 8 8 8-8M70 188h180m-173-8-7 8 7 8m166-16 7 8-7 8"/>',
        'counter': '<path d="M39 141h242M49 148v40m222-40v40"/><rect x="70" y="60" width="91" height="79" rx="8"/><path d="M80 84h70m-37 14v29M182 70v69m0-58 53-22m-53 27 53 42M52 40h215m-207-8-8 8 8 8m199-16 8 8-8 8"/>',
        'functions': '<rect x="76" y="29" width="167" height="157" rx="13"/><path d="M96 52h126M99 82h16m-16 28h16m-16 28h16m-16 28h16M132 82h88m-88 28h88m-88 28h88m-88 28h58"/>',
        'thermometer': '<path d="m85 38 26 97m17-109 26 99m32-99-7 98m51-88-27 99"/><rect x="86" y="121" width="137" height="63" rx="13"/><circle cx="154" cy="153" r="10"/>',
    }
    return f'<div class="p26-guide-art p26-art-{esc(kind)}"><svg viewBox="0 0 320 220" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{artwork[kind]}</svg><span>THE ZONE3 FIELD GUIDE</span></div>'


def fits_block(p: dict) -> str:
    """Two-sided fit note. Each side names the format fact and then asks the buyer to check it.

    This is deliberately not a verdict: the listing wording supports the format difference,
    and nothing here is presented as a test result or a recommendation of one model.
    """
    d = DECISION[p['id']]
    return ('<div class="p26-fits"><p><span>Fits you if</span>' + esc(d['fits']) + '</p>'
            '<p><span>Not for you if</span>' + esc(d['not']) + '</p>'
            '<p class="p26-ask">' + esc(d['ask']) + '</p></div>')


def product_card(p: dict, prefix: str = '', compare: bool = False) -> str:
    # All external product destinations are unchanged supplied links, not claimed validated links.
    chips = ''.join(f'<span>{esc(x)}</span>' for x in p['features'])
    return f'''<article class="p26-product-card" id="{p['id']}" data-product-card data-category="{p['category']}">
<div class="p26-product-art p26-art-{p['format']}"><span class="p26-product-kind">{esc('Air fryer' if p['category']=='air-fryers' else 'Meat thermometer')}</span>{format_art(p['format'])}<span class="p26-art-caption">FORMAT ILLUSTRATION</span></div>
<div class="p26-product-copy"><p class="p26-overline">{esc(p['brand'])}</p><h3>{esc(p['name'])}</h3><p>{esc(p['description'])}</p><div class="p26-features">{chips}</div>{fits_block(p)}
<a class="p26-product-cta" href="{p['submitted_link']}" rel="sponsored noopener">View on Amazon {icon('external')}</a>
<div class="p26-card-source"><span>Sponsored</span><details><summary>Listing & source</summary><p>Title and destination observed <time datetime="{p['observed_on']}">{human_date(REVERIFIED)}</time>. {source_link(p['id'], 'Official Amazon listing')} · ASIN <code>{p['observed_asin']}</code>. Features above are listing wording, not test results. Intended product and attribution remain unconfirmed: <a href="{prefix}intent-record/index.html">intent record</a> · <a href="{prefix}flagged.html#FLG-003">link review</a>.</p></details></div></div></article>'''


def guide_card(g: dict, prefix: str = '', art: bool = True, compact: bool = False) -> str:
    artwork = guide_art(g['art']).replace('src="../assets/', f'src="{prefix}assets/') if art else ''
    if compact:
        return f'''<a class="p26-choice" href="{prefix}guides/{g['slug']}.html"><span class="p26-overline">{esc(g['type'])}</span><strong>{esc(g['short_title'])}</strong><span class="p26-choice-go">Read the guide {icon('arrow')}</span></a>'''
    return f'''<article class="p26-guide-card">{artwork}<div class="p26-guide-copy"><p class="p26-overline">{esc(g['type'])}</p><h3><a href="{prefix}guides/{g['slug']}.html">{esc(g['short_title'])}</a></h3><p>{esc(g['dek'])}</p><a class="p26-text-link" href="{prefix}guides/{g['slug']}.html">Read the guide {icon('arrow')}</a></div></article>'''


def follow(prefix: str = '') -> str:
    return f'''<section class="p26-follow" aria-labelledby="p26-follow-title"><div class="p26-follow-icon">{icon('rss')}</div><div><p class="p26-overline">GOOD QUESTIONS, DELIVERED DIFFERENTLY</p><h2 id="p26-follow-title">Your next good kitchen read.</h2><p>Follow the feed for new guides. No email address, no sign-up form, no noise.</p></div><a class="p26-button p26-button-outline" href="{prefix}feed.xml">Follow by RSS {icon('arrow')}</a></section>'''


def shell(rel: str, title: str, description: str, body: str, article: dict | None = None) -> str:
    prefix = chrome.prefix_for(rel)
    canonical = chrome.canonical(rel)
    schema: dict = {'@context': 'https://schema.org', '@type': 'WebPage', 'name': title, 'description': description, 'url': canonical, 'isPartOf': {'@type': 'WebSite', 'name': 'Zone3 Kitchen', 'url': chrome.BASE}}
    if rel == 'index.html':
        schema.update({'@type': 'WebSite', 'name': 'Zone3 Kitchen', 'publisher': {'@type': 'Organization', 'name': 'Zone3 Editorial', 'url': chrome.BASE + 'about.html'}})
    if article:
        schema.update({'@type': 'Article', 'headline': article['title'], 'datePublished': article['published'], 'dateModified': DATA['meta']['updated'], 'author': {'@type': 'Organization', 'name': 'Zone3 Editorial', 'url': chrome.BASE + 'about.html'}, 'publisher': {'@type': 'Organization', 'name': 'Zone3 Editorial', 'url': chrome.BASE + 'about.html'}, 'mainEntityOfPage': canonical})
    jsonld = json.dumps(schema, ensure_ascii=False).replace('<', '\\u003c')
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)} | Zone3 Kitchen</title><meta name="description" content="{esc(description)}">
<link rel="canonical" href="{canonical}"><meta property="og:type" content="{'article' if article else 'website'}"><meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(description)}"><meta property="og:url" content="{canonical}"><meta property="og:site_name" content="Zone3 Kitchen"><meta property="og:image" content="{chrome.BASE}assets/img/publication-kitchen.jpg"><meta property="og:image:width" content="1536"><meta property="og:image:height" content="1024"><meta property="og:image:alt" content="AI-generated editorial kitchen still life; illustrative only, not a product photograph"><meta name="twitter:card" content="summary_large_image"><meta name="twitter:image:alt" content="AI-generated editorial kitchen still life; illustrative only, not a product photograph"><meta name="theme-color" content="#283f32">
<link rel="icon" href="{prefix}assets/favicon.svg" type="image/svg+xml"><script type="application/ld+json">{jsonld}</script>
<!-- aebf0747-front -->
</head><body class="p26-body"><main class="p26-main" id="main">{body}</main></body></html>
'''


def home() -> str:
    cards = ''.join(product_card(p) for p in DATA['products'])
    guides = ''.join(guide_card(GUIDES[x]) for x in ['basket-or-oven-style', 'capacity-checklist', 'cleanup-and-counter-space'])
    # "Just added" is whatever the register says shipped in this edition, so a new guide reaches the
    # front-page reading room without anyone hand-editing the front page.
    latest = [g for g in DATA['guides'] if g['published'] == DATA['meta']['updated']] or DATA['guides'][-2:]
    return shell('index.html', 'A more considered kitchen starts here', 'Practical air fryer and meat thermometer buying guides. Compare the formats, ask better questions, and make room for tools that fit your kitchen.', f'''
<div class="p26-container"><div class="p26-edition"><span>THE EVERYDAY KITCHEN EDIT</span><span>NOVEMBER 2026 <i aria-hidden="true">/</i> VOL. 01</span></div>
<section class="p26-hero" aria-labelledby="p26-hero-title"><div class="p26-hero-copy"><p class="p26-overline"><span class="p26-dot"></span> FEWER TABS. BETTER QUESTIONS.</p><h1 id="p26-hero-title">Good food.<br>Thoughtful tools.<br><em>Your kitchen.</em></h1><p>You don’t need another “must-have”. You need to know what fits your space, your meals, and the way you cook. Let’s start there.</p><div class="p26-hero-actions"><a class="p26-button" href="#products">Explore the shortlist {icon('arrow')}</a><a class="p26-text-link" href="guides/index.html">Find a buying guide</a></div><div class="p26-hero-note"><span class="p26-mini-mark">z3.</span><p>Practical buying guides.<br><strong>No made-up tests. No pretend winners.</strong></p></div></div>
<figure class="p26-hero-figure"><img src="assets/img/publication-kitchen.jpg" alt="AI-generated editorial still life of roasted vegetables in a warm, sunlit kitchen; not product testing" width="1536" height="1024" fetchpriority="high"><figcaption>THE KITCHEN, CONSIDERED. <span>AI-generated editorial image</span></figcaption><a class="p26-hero-story" href="guides/basket-or-oven-style.html"><span class="p26-overline">START WITH THE BIG QUESTION</span><strong>Basket or oven?<br>Let dinner decide.</strong><span class="p26-story-arrow">{icon('arrow')}</span></a></figure></section>
<div class="p26-principles"><p>{icon('check')} Buyer questions first</p><p>{icon('check')} Sources within reach</p><p>{icon('check')} A reason to choose—or not to buy</p></div>
<section class="p26-section" id="products" aria-labelledby="p26-products-heading"><div class="p26-section-heading"><div><p class="p26-overline">MEET THE SHORTLIST</p><h2 id="p26-products-heading">Make a little room for possibility.</h2></div><a class="p26-text-link" href="shop/products/index.html">Compare the details {icon('arrow')}</a></div><p class="p26-section-dek">Three air fryers. Two thermometers. Start with the format that makes sense for you.</p>
<div class="p26-filter-row" role="group" aria-label="Filter products"><button type="button" class="p26-filter is-active" data-filter="all" aria-pressed="true">All tools <span>5</span></button><button type="button" class="p26-filter" data-filter="air-fryers" aria-pressed="false">Air fryers <span>3</span></button><button type="button" class="p26-filter" data-filter="meat-thermometers" aria-pressed="false">Thermometers <span>2</span></button><span class="p26-filter-note">A shortlist, not a ranking.</span></div><p class="p26-sr-only" id="p26-filter-status" aria-live="polite"></p><div class="p26-products-grid">{cards}</div><p class="p26-fine p26-product-footnote">Listing-based introductions, not hands-on reviews. Format illustrations are not photographs of the listed models. Supplied links are <a href="flagged.html#FLG-003">under attribution review</a>; no current price or rating is reproduced.</p></section>
</div>
<section class="p26-start"><div class="p26-container p26-start-grid"><div><p class="p26-overline">A BETTER PLACE TO START</p><h2>Your counter.<br>Your cooking.<br><em>Your call.</em></h2></div><div><p>Before you compare features, pick the question that sounds like your kitchen.</p><a href="guides/basket-or-oven-style.html"><span><b>01</b> Do I need one basket, two, or an oven?</span>{icon('arrow')}</a><a href="guides/capacity-checklist.html"><span><b>02</b> How much space will my food actually get?</span>{icon('arrow')}</a><a href="guides/instant-read-or-wireless-thermometer.html"><span><b>03</b> Spot check or connected thermometer?</span>{icon('arrow')}</a></div></div></section>
<div class="p26-container"><section class="p26-section" id="guides" aria-labelledby="p26-guides-heading"><div class="p26-section-heading"><div><p class="p26-overline">THE READING ROOM</p><h2 id="p26-guides-heading">Good questions. Useful answers.</h2></div><a class="p26-text-link" href="guides/index.html">All the guides {icon('arrow')}</a></div><div class="p26-guides-grid">{guides}</div><p class="p26-latest">Just added to this edition <span>· {READ_ON}</span> {' · '.join(f'<a class="p26-text-link" href="guides/{g["slug"]}.html">{esc(g["short_title"])}</a>' for g in latest)}</p></section>
<section class="p26-seasonal"><div class="p26-seasonal-art">{guide_art('functions')}</div><div><p class="p26-overline">THE HOSTING-SEASON EDIT</p><h2>More people at the table.<br>Not necessarily more tools.</h2><p>Start with your menu, work out the bottleneck, and build a shortlist from there. A kitchen checklist for the season of “is there room for one more?”</p><a class="p26-text-link" href="guides/holiday-kitchen-checklist.html">Make a meal-first plan {icon('arrow')}</a></div><span class="p26-seasonal-number" aria-hidden="true">03</span></section>
<section class="p26-editor-note"><span class="p26-mini-mark">z3.</span><div><p class="p26-overline">A NOTE FROM THE EDITORIAL DESK</p><h2>Useful beats breathless. Every time.</h2><p>We turn product-listing details into questions you can use. We tell you when we haven’t tested something. And if the information isn’t there, we won’t make it up.</p><a class="p26-text-link" href="about.html">How we put a guide together {icon('arrow')}</a></div></section>{follow()}</div>''')


def guide_index() -> str:
    cards = ''.join(guide_card(g, '../') for g in DATA['guides'])
    return shell('guides/index.html', 'Buying guides for a more considered kitchen', f'{numeral(GUIDE_N)} practical, question-led guides to air fryer formats, capacity, cleanup, meat thermometers and hosting-season shopping.', f'''<div class="p26-container"><div class="p26-page-intro"><p class="p26-overline">THE READING ROOM</p><h1>Before you add<br><em>anything to the counter.</em></h1><p>Small questions that make a shopping decision clearer. No “ultimate” lists. No best-ever claims. Just a useful place to start.</p></div><div class="p26-guides-grid p26-guides-all">{cards}</div>{follow('../')}</div>''')


def guide_page(g: dict) -> str:
    sections = []
    toc = []
    for n, section in enumerate(g['sections'], 1):
        toc.append(f'<a href="#section-{n}"><span>0{n}</span>{esc(section["heading"])}</a>')
        paragraphs = ''.join(f'<p>{esc(x)}</p>' for x in section.get('paragraphs', []))
        checklist = '<ul class="p26-checklist">' + ''.join(f'<li>{esc(x)}</li>' for x in section['checklist']) + '</ul>' if section.get('checklist') else ''
        sources = ' · '.join(source_link(x) for x in section['source_ids'])
        sections.append(f'<section id="section-{n}"><h2>{esc(section["heading"])}</h2>{paragraphs}{checklist}<p class="p26-source-note">Source context: {sources}. Read {READ_ON}. Shopping prompts are editorial suggestions.</p></section>')
    product_rows = ''.join(f'<tr><th scope="row">{esc(PRODUCTS[x]["brand"] + " " + PRODUCTS[x]["name"])}</th><td>{esc(PRODUCTS[x]["format_text"])}</td><td><a href="{PRODUCTS[x]["observed_listing_url"]}" rel="sponsored noopener">Amazon listing</a><br><small>{READ_ON} · title only</small></td></tr>' for x in g['products'])
    unknowns = ''.join(f'<li>{esc(x)}</li>' for x in g['unknowns'])
    related = ''.join(guide_card(GUIDES[x], '../', art=False) for x in g['related'])
    body = f'''<div class="p26-container"><nav class="p26-breadcrumb" aria-label="Breadcrumb"><a href="../index.html">The edit</a><span>/</span><a href="index.html">Buying guides</a><span>/</span>{esc(g['category'])}</nav><header class="p26-article-heading"><p class="p26-overline">{esc(g['category'])} <span> / </span> {esc(g['type'])}</p><h1>{esc(g['title'])}</h1><p class="p26-article-dek">{esc(g['dek'])}</p><div class="p26-byline"><span class="p26-author-avatar">z3.</span><p>By <a href="../about.html#authorship">Zone3 Editorial</a><br><span>Published {human_date(g['published'])} · Updated {READ_ON} · Sources re-checked {human_date(REVERIFIED)}</span></p><span class="p26-byline-kind">Listing-based guide<br>Not a hands-on review</span></div></header><div class="p26-article-layout"><aside class="p26-article-aside"><p class="p26-overline">IN THIS GUIDE</p>{''.join(toc)}<a href="#the-shortlist"><span>04</span>The relevant shortlist</a><p class="p26-aside-note">AI-assisted, source-linked editorial. No independent product testing is claimed.</p></aside><article class="p26-article"><div class="p26-takeaway"><p class="p26-overline">THE SHORT ANSWER</p><p>{esc(g['takeaway'])}</p></div>{''.join(sections)}<section id="the-shortlist"><h2>The listings behind the questions.</h2><p>These are title-based introductions, not recommendations based on testing. Every row links its official listing.</p><div class="p26-table-scroll" role="region" aria-label="Relevant product listings" tabindex="0"><table class="p26-table"><thead><tr><th scope="col">Product</th><th scope="col">Format named in listing</th><th scope="col">Source</th></tr></thead><tbody>{product_rows}</tbody></table></div><a class="p26-button" href="../shop/{g['category_slug'] if g['category_slug'] != 'everyday-kitchen' else 'products'}/index.html">Explore the shortlist {icon('arrow')}</a></section><section class="p26-unknowns"><h2>What we haven’t established.</h2><ul>{unknowns}</ul><p>We leave unsupported values out rather than filling the gaps. <a href="../flagged.html">See the review register</a> or <a href="../intent-record/index.html">the product-intent record</a>.</p></section></article></div><section class="p26-section"><div class="p26-section-heading"><div><p class="p26-overline">KEEP THE GOOD QUESTIONS COMING</p><h2>Next on your reading list.</h2></div></div><div class="p26-guides-grid">{related}</div></section>{follow('../')}</div>'''
    return shell(f'guides/{g["slug"]}.html', g['title'], g['dek'], body, article=g)


def comparison_table(products: list[dict], prefix: str) -> str:
    rows = []
    for p in products:
        clean = esc(p['cleanup_title_wording']) if p['cleanup_title_wording'] else ''
        rows.append(f'<tr><th scope="row">{esc(p["brand"] + " " + p["name"])}</th><td>{esc(p["format_text"])}</td><td>{clean}</td><td class="blank" aria-label="Unverified: no independent testing"></td><td><span class="p26-status">Listing only · untested</span><br><a href="{prefix}flagged.html#P26-F04">Evidence gap</a></td><td>{source_link(p["id"], "Amazon listing")}<br><small>{human_date(REVERIFIED)}</small></td></tr>')
    return '<div class="p26-table-scroll" role="region" aria-label="Source-linked product comparison" tabindex="0"><table class="p26-table"><caption>Listing wording, not a performance ranking. Blank cells are unverified; source checks are limited to title and destination.</caption><thead><tr><th scope="col">Product</th><th scope="col">Format</th><th scope="col">Cleanup wording in title</th><th scope="col">Tested performance</th><th scope="col">Evidence status</th><th scope="col">Official source</th></tr></thead><tbody>' + ''.join(rows) + '</tbody></table></div>'


def chooser(prefix: str, category: str) -> str:
    """Three-question format chooser. It narrows to a guide; it never names a winner."""
    if category == 'air-fryers':
        questions = [
            ('How many things do you cook at once?',
             ['Two dishes, different timings', 'One big batch', 'I want an oven, not a basket'],
             ['basket-or-oven-style']),
            ('What matters most on the counter?',
             ['A compact footprint', 'Room for a large interior', 'Easy parts to wash'],
             ['cleanup-and-counter-space']),
            ('How do you read a capacity label?',
             ['Quarts is enough for me', 'I need internal dimensions', 'I am not sure yet'],
             ['capacity-checklist']),
        ]
    elif category == 'meat-thermometers':
        questions = [
            ('Spot check or continuous reading?',
             ['A quick spot check', 'A reading while it cooks', 'Still deciding'],
             ['instant-read-or-wireless-thermometer']),
            ('Do you want an app?',
             ['Yes, phone readings', 'No, keep it simple', 'Show me the trade-off'],
             ['instant-read-or-wireless-thermometer']),
            ('What are you cooking next?',
             ['A roast or whole bird', 'Everyday pan cooking', 'A holiday table'],
             ['holiday-kitchen-checklist']),
        ]
    else:
        questions = [
            ('What are you actually choosing?',
             ['An air fryer', 'A meat thermometer'],
             ['basket-or-oven-style', 'instant-read-or-wireless-thermometer']),
            ('Basket, two baskets, or oven?',
             ['One basket', 'Two baskets', 'An oven'],
             ['basket-or-oven-style']),
            ('What should we check together?',
             ['Capacity and dimensions', 'Cleanup and counter space', 'App and connection needs'],
             ['capacity-checklist', 'cleanup-and-counter-space']),
        ]
    blocks = []
    for n, (question, answers, slugs) in enumerate(questions, 1):
        opts = ''.join(
            '<a class="p26-choice" href="' + prefix + 'guides/' + slugs[min(i, len(slugs) - 1)] + '.html">'
            + '<span class="p26-overline">' + esc(a) + '</span>'
            + '<span class="p26-choice-go">Go ' + icon('arrow') + '</span></a>'
            for i, a in enumerate(answers))
        blocks.append(f'<div class="p26-chooser-step"><p class="p26-overline">QUESTION 0{n}</p><h3>{esc(question)}</h3><div class="p26-choice-list">{opts}</div></div>')
    return ('<section class="p26-section p26-chooser" id="chooser"><div class="p26-section-heading"><div>'
            '<p class="p26-overline">THREE QUESTIONS, NO SCORE</p><h2>Which one is for you?</h2></div></div>'
            '<p class="p26-section-dek">This narrows the field to the guide that answers your question. It does not rank the products, '
            'and it cannot tell you what will fit your kitchen. Nothing you choose here is sent anywhere.</p>'
            '<div class="p26-chooser-grid">' + ''.join(blocks) + '</div></section>')

def catalogue(category: str = 'all', compare: bool = False) -> tuple[str, str]:
    ps = [p for p in DATA['products'] if category == 'all' or p['category'] == category]
    rel = 'shop/products/index.html' if compare else 'shop/index.html' if category == 'all' else f'shop/{category}/index.html'
    prefix = chrome.prefix_for(rel)
    if category == 'air-fryers':
        eyebrow, title, intro = 'THE COUNTERTOP SHORTLIST', 'Start with the format.<br><em>Then the features.</em>', 'Three air-fryer listings. Compare one basket, two independent baskets and a French-door oven format. No model is named a winner.'
        related_slugs = ['basket-or-oven-style', 'capacity-checklist', 'cleanup-and-counter-space']
        doc_title, doc_desc = 'Air fryers: basket, dual-basket and oven formats compared', 'Three air-fryer listings compared by cooking format, compartment layout and listing wording. No model is named a winner and no price or rating is shown.'
    elif category == 'meat-thermometers':
        eyebrow, title, intro = 'THE TEMPERATURE-TOOL SHORTLIST', 'A better question<br><em>for your next reading.</em>', 'Two thermometer listings. Compare the reading workflow, check the exact model instructions and keep advertised claims separate from independent evidence.'
        related_slugs = ['instant-read-or-wireless-thermometer', 'holiday-kitchen-checklist']
        doc_title, doc_desc = 'Meat thermometers: wireless or instant-read compared', 'Two meat-thermometer listings compared by reading workflow and app requirements, with the questions to check against each model instruction sheet.'
    elif compare:
        eyebrow, title, intro = 'THE PRODUCT SHORTLIST', 'Not more tools.<br><em>The right questions.</em>', 'Five products, two kitchen categories. Explore the formats and check the questions that matter before you choose.'
        related_slugs = ['basket-or-oven-style', 'instant-read-or-wireless-thermometer', 'holiday-kitchen-checklist']
        doc_title, doc_desc = 'Compare all five listings side by side', 'All five shortlisted listings in one table: brand, format, listed features and the official Amazon listing for each. Unverified cells are left blank, not guessed.'
    else:
        eyebrow, title, intro = 'THE PRODUCT SHORTLIST', 'Not more tools.<br><em>The right questions.</em>', 'Five products, two kitchen categories. Explore the formats and check the questions that matter before you choose.'
        related_slugs = ['basket-or-oven-style', 'instant-read-or-wireless-thermometer', 'holiday-kitchen-checklist']
        doc_title, doc_desc = 'Kitchen shortlist: three air fryers, two thermometers', 'Five source-linked kitchen listings: three air-fryers and two meat thermometers. See the format each one uses before you compare features.'
    table = comparison_table(ps, prefix)
    cards = ''.join(product_card(p, prefix) for p in ps)
    chooser_html = '' if compare else chooser(prefix, category)
    guides = ''.join(guide_card(GUIDES[x], prefix, art=False) for x in related_slugs)
    body = f'''<div class="p26-container"><div class="p26-page-intro"><p class="p26-overline">{eyebrow}</p><h1>{title}</h1><p>{intro}</p><div class="p26-category-links"><a href="{prefix}shop/index.html">All tools</a><a href="{prefix}shop/air-fryers/index.html">Air fryers</a><a href="{prefix}shop/meat-thermometers/index.html">Thermometers</a><a href="{prefix}shop/products/index.html">Compare details</a></div></div>{'' if compare else chooser_html}{table if compare else '<div class="p26-products-grid">'+cards+'</div>'}<p class="p26-fine">Product names and formats are listing wording observed {REVERIFIED}. No independent performance, prices, ratings or availability are asserted. Illustrations show generic formats, not the exact products.</p><section class="p26-section" id="comparison"><div class="p26-section-heading"><div><p class="p26-overline">PUT THE DETAILS SIDE BY SIDE</p><h2>{'A few important limits.' if compare else 'Different formats. Clearer questions.'}</h2></div></div>{'<p>Intended ASINs, account ownership and Special Link attribution are still unconfirmed. Blank performance and cleanup cells are unverified—not zero or a negative finding.</p>' if compare else table}<p class="p26-fine">Keep intended product and observed destination separate: <a href="{prefix}intent-record/index.html">confirmation record</a>. The supplied short links’ exact compliance status remains unresolved: <a href="{prefix}flagged.html#FLG-003">FLG-003</a>.</p></section><section class="p26-section"><h2>Read before you decide.</h2><div class="p26-guides-grid">{guides}</div></section>{follow(prefix)}</div>'''
    return rel, shell(rel, doc_title, doc_desc, body)


def review_round_html() -> str:
    """Dated review round (session b9008684, 2026-11-19). Additive and review-only:
    every card joins the existing local save/export record via data-decision-id and
    implements nothing. Returns '' when the round is absent so older data still builds."""
    r = DATA.get('review_b9008684')
    if not r:
        return ''
    prefix = '../'

    def chooser(pid: str) -> str:
        return (f'<label for="decision-{pid}">Your review <span>(does not implement changes)</span></label>'
                f'<select id="decision-{pid}" data-decision-id="{pid}"><option value="unreviewed">Not reviewed</option>'
                f'<option value="shortlist">Shortlist for next review</option>'
                f'<option value="defer">Defer until evidence arrives</option>'
                f'<option value="reject">Do not pursue</option></select>')

    def basis_link(item: dict) -> str:
        b = item.get('basis')
        return source_link(b) if b else 'Editorial judgement — no external rule claimed'

    design_cards = []
    for s in r['design_feed']:
        design_cards.append(
            f'<article class="p26-proposal"><div class="p26-proposal-top"><span class="p26-status">{esc(s["status"])} · {esc(s["area"])}</span><span>{esc(s["id"])}</span></div>'
            f'<h3>{esc(s["title"])}</h3><p>{esc(s["why"])}</p>'
            f'<p><strong>Adds to the design prompt:</strong> “{esc(s["feeds_prompt"])}”</p>'
            f'<p><strong>What would change our mind:</strong> {esc(s["falsifier"])}</p>'
            f'<p class="p26-fine">Basis: {basis_link(s)}</p>{chooser(s["id"])}</article>')

    slate_cards = []
    for s in r['article_slate']:
        pairs = ' · '.join(f'<a href="{prefix}guides/{slug}.html">{esc(label)}</a>' for slug, label in s.get('pairs', []))
        season = f'<p class="p26-fine">{esc(s["seasonal"])}</p>' if s.get('seasonal') else ''
        basis_note = f' Basis: {source_link(s["basis"])}.' if s.get('basis') else ''
        slate_cards.append(
            f'<article class="p26-proposal"><div class="p26-proposal-top"><span class="p26-status">Proposed · {esc(s["category"])}</span><span>{esc(s["id"])}</span></div>'
            f'<h3>“{esc(s["title"])}”</h3><p>{esc(s["angle"])}</p>'
            + (f'<p class="p26-fine">Pairs with: {pairs}</p>' if pairs else '')
            + f'<p class="p26-fine">Provenance: {esc(s.get("provenance", ""))}.{basis_note}</p>{season}'
            + '<p class="p26-fine"><strong>Working title — an editorial hypothesis.</strong> Not a popularity, search-volume or demand claim. Publication goes through the same publishing gate as the current six guides.</p>'
            + chooser(s['id']) + '</article>')

    traffic_rows = ''.join(
        f'<tr><th scope="row">{esc(t["action"])}</th><td>{esc(t["status"])}</td><td>{esc(t["needs"])}</td><td>{source_link(t["basis"])}</td></tr>'
        for t in r['traffic_actions'])
    decision_rows = ''.join(
        f'<tr id="{d["id"]}"><th scope="row"><small>{d["id"]}</small><br>{esc(d["decision"])}</th><td>{esc(d["have"])}</td><td>{esc(d["missing"])}</td><td>{esc(d["discovery"])}</td><td>{esc(d["default"])}</td><td>{source_link(d["basis"])}</td></tr>'
        for d in r['decision_rows'])
    return (f'<section class="p26-section" id="review-round-b9"><div class="p26-section-heading"><div>'
            f'<p class="p26-overline">REVIEW ROUND · {esc(r["date"])} · SESSION {esc(r["session"])}</p>'
            f'<h2>Seven ways to make the shop feel more published — and what each one needs.</h2></div></div>'
            f'<div class="p26-review-note"><strong>Review mode only, again.</strong> {esc(r["intro"])} '
            f'Each card joins the same local save/export record as the proposals above; nothing here is implemented by reading, choosing or saving it.</div>'
            f'<div class="p26-proposals-grid">{"".join(design_cards)}</div>'
            f'<p class="p26-fine">{esc(r["prompt_intro"])}</p>'
            f'<div class="p26-prompt">{esc(r["prompt_lines"])}</div>'
            f'<h3>The article slate: seven working titles.</h3>'
            f'<p class="p26-fine">Every title below is question-shaped and backed by the provenance noted on its card. A working title is an editorial hypothesis — not a popularity, search-volume or demand claim — and each ships, or does not ship, through the same publishing gate as the current six guides.</p>'
            f'<div class="p26-proposals-grid">{"".join(slate_cards)}</div>'
            f'<h3>Organic traffic: what can run now, what is blocked.</h3>'
            f'<p class="p26-fine">{esc(r["traffic_intro"])}</p>'
            f'<div class="p26-table-scroll" tabindex="0" role="region" aria-label="Organic-traffic actions and their basis"><table class="p26-table">'
            f'<thead><tr><th scope="col">Action</th><th scope="col">Status today</th><th scope="col">What it needs</th><th scope="col">Basis</th></tr></thead>'
            f'<tbody>{traffic_rows}</tbody></table></div>'
            f'<h3>The decision-support register.</h3>'
            f'<p class="p26-fine">{esc(r["decision_intro"])}</p>'
            f'<div class="p26-table-scroll" tabindex="0" role="region" aria-label="Decision support: what we have, what is missing, how to discover it, the safe default"><table class="p26-table p26-question-table">'
            f'<thead><tr><th scope="col">Decision</th><th scope="col">What we already have</th><th scope="col">What we still don’t have</th><th scope="col">How to discover it</th><th scope="col">Safe default</th><th scope="col">Basis</th></tr></thead>'
            f'<tbody>{decision_rows}</tbody></table></div></section>')


def suggestions() -> str:
    cards = []
    for p in DATA['proposals']:
        refs = ' · '.join(f'<a href="#{qid}">{qid}</a>' for qid in p['evidence_needed'])
        need_owner = ('<span class="p26-status p26-status-owner">Needs your input</span>' if p.get('owner_input_needed')
                      else '<span class="p26-status">Agent can proceed</span>')
        discovers = ''.join(f'<li>{esc(x)}</li>' for x in p.get('discoveries', []))
        cards.append(f'''<article class="p26-proposal" data-proposal data-priority="{p['priority']}"><div class="p26-proposal-top"><span class="p26-status">{esc(p['priority'])} · {esc(p['area'])}</span><span>{p['id']}</span></div><h3>{esc(p['title'])}</h3><p>{esc(p['why'])}</p><p><strong>Next discovery step:</strong> {esc(p['next'])}</p><p><strong>If you say go, this is exactly what happens:</strong> {esc(p.get('next_action', ''))}</p><details class="p26-proposal-extra"><summary>What it would tell us</summary><ul>{discovers}</ul></details><p class="p26-fine">{need_owner} · Evidence to close: {refs}<br>Basis: {source_link(p['source'])}</p><label for="decision-{p['id']}">Your review <span>(does not implement changes)</span></label><select id="decision-{p['id']}" data-decision-id="{p['id']}"><option value="unreviewed">Not reviewed</option><option value="shortlist">Shortlist for next review</option><option value="defer">Defer until evidence arrives</option><option value="reject">Do not pursue</option></select></article>''')

    paths = []
    for p in DATA['paths']:
        needs = ' · '.join(f'<a href="#{q}">{q}</a>' for q in p['needs']) or 'Nothing external — this one is a build decision, not an evidence request.'
        ribbon = '<span class="p26-ribbon">In the recommended order</span>' if p['recommended'] else ''
        changes = ''.join(f'<li>{esc(x)}</li>' for x in p['changes'])
        paths.append(f'''<article class="p26-path" data-path><div class="p26-path-top"><p class="p26-overline">PATH {p['sequence']:02d}</p>{ribbon}</div><h3>{esc(p['name'])}</h3><p class="p26-path-pitch">{esc(p['pitch'])}</p><div class="p26-path-grid"><div><p class="p26-overline">WHAT A READER WOULD SEE</p><ul>{changes}</ul></div><div class="p26-path-facts"><p class="p26-overline">NEEDS FIRST</p><p>{needs}</p><p class="p26-overline">WHAT IT UNBLOCKS</p><p>{esc(p['unblocks'])}</p><p class="p26-overline">WHAT IT CANNOT DELIVER</p><p>{esc(p['cannot'])}</p><p class="p26-overline">COST / RISK</p><p>{esc(p['cost'])}<br>{esc(p['risk'])}</p></div></div><p class="p26-fine">Basis: {source_link(p['basis'])} · Gate status: <span class="p26-status">{esc(p['status'])}</span></p><label for="decision-{p['id']}">Your review <span>(choosing a path here implements nothing)</span></label><select id="decision-{p['id']}" data-decision-id="{p['id']}"><option value="unreviewed">Not reviewed</option><option value="shortlist">Take this path next</option><option value="defer">Defer until evidence arrives</option><option value="reject">Do not pursue</option></select></article>''')
    ordered = sorted(DATA['paths'], key=lambda x: x['sequence'])
    now_ids = ' → '.join(f"PATH {p['sequence']:02d}" for p in ordered if p['recommended'])
    later = ' · '.join(esc(p['name']) for p in ordered if not p['recommended'])
    sequence_note = f'''<div class="p26-sequence"><p class="p26-overline">THE ORDER WE WOULD WORK IN, AND WHY</p><p><strong>{now_ids}</strong> — polish the shop, prove the links, then switch on measurement. <strong>Then decide:</strong> {later}. The first path needs nothing from anyone; the next two are stopped by account and hosting decisions, and the last two are stopped by evidence and budget. Choosing here records a preference in this browser; it starts no work.</p></div>'''

    rows = []
    for q in DATA['questions']:
        who = q.get('answer_by') or ('You (account holder)' if q.get('owner_input_needed') else 'Agent, then confirm')
        rows.append(f'<tr id="{q["id"]}"><th scope="row"><small>{q["id"]}</small><br>{esc(q["question"])}</th><td>{esc(q["known"])}</td><td>{esc(q["missing"])}</td><td><span class="p26-owner">{esc(who)}</span><br><small>{esc(q.get("answer_form", ""))}</small></td><td>{esc(q["discovery"])}</td><td>{esc(q["default"])}</td><td>{source_link(q["source"])}</td></tr>')

    intake = DATA['suggestion_intake']
    intake_rows = ''.join(f'<div class="p26-intake-row"><dt>{esc(field)}</dt><dd>{esc(hint)}</dd></div>' for field, hint in intake['fields'])

    blocks = []
    for block in DATA['design_prompt']['blocks']:
        bid = f'prompt-{block["id"]}'
        blocks.append(f'''<div class="p26-prompt-block" id="{bid}"><div class="p26-prompt-head"><h3>{esc(block['heading'])}</h3><button type="button" class="p26-text-button" data-copy-from="{bid}">Copy this block</button></div><p>{esc(block['text'])}</p><p class="p26-fine">Basis: {source_link(block['basis'])}</p></div>''')

    review = review_round_html()
    body = f'''<div class="p26-container"><div class="p26-page-intro"><p class="p26-overline">BEHIND THE SITE / SUGGESTIONS &amp; DECISIONS</p><h1>A good next step<br><em>starts with the evidence.</em></h1><p>Choose a path, see what is missing, and leave an honest note about it — without accidentally implementing anything.</p></div><div class="p26-review-note"><strong>Review mode only.</strong> Choices are saved only when you press Save, in this browser. They do not publish pages, spend money, change accounts or activate tracking. Both the paths and the individual proposals are included in what you save and export. <a href="../suggestions.html">Open the full historical suggestions register</a>.</div><section class="p26-section" id="paths"><div class="p26-section-heading"><div><p class="p26-overline">{len(DATA['paths'])} PATHS, ONE DECISION AT A TIME</p><h2>Pick a direction, not a feature.</h2></div></div><p class="p26-section-dek">Each path is a bundle of the smaller proposals below, with its dependencies named: what it needs before it can be done honestly, what it buys the reader, and what it still cannot claim afterwards.</p>{sequence_note}<div class="p26-paths-grid">{''.join(paths)}</div></section><section class="p26-section" id="proposals"><div class="p26-section-heading"><div><p class="p26-overline">{len(DATA['proposals'])} PROPOSALS, {len(DATA['questions'])} OPEN QUESTIONS</p><h2>Choose what deserves the next look.</h2></div></div><div class="p26-filter-row" role="group" aria-label="Filter suggestions"><button type="button" class="p26-filter is-active" data-proposal-filter="all" aria-pressed="true">All suggestions</button><button type="button" class="p26-filter" data-proposal-filter="Now" aria-pressed="false">Now</button><button type="button" class="p26-filter" data-proposal-filter="Next" aria-pressed="false">Next</button><button type="button" class="p26-filter" data-proposal-filter="Later" aria-pressed="false">Later</button></div><div class="p26-proposals-grid">{''.join(cards)}</div><div class="p26-review-actions"><button type="button" class="p26-button" data-save-review>Save this review {icon('check')}</button><button type="button" class="p26-button p26-button-outline" data-export-review>Export review JSON</button><button type="button" class="p26-text-button" data-reset-review>Clear saved choices</button><p id="p26-review-status" role="status" aria-live="polite">No changes will be implemented from this page.</p></div><noscript><p>JavaScript is off. You can still read every path, suggestion and evidence question; saving and exporting a local review require JavaScript.</p></noscript></section><section class="p26-section" id="questions"><p class="p26-overline">THE DECISION-READINESS REGISTER</p><h2>What do we know? Who holds the rest?</h2><p>Every open question in one table, with the answer as far as it exists, the person or system who can actually supply the rest, and what a complete answer would look like. These are unanswered operational questions, not an invitation to invent answers. Where a fact cannot be confirmed from an official source it is left blank and flagged. Official references explain the applicable rule or context; repository status and safe defaults are our own observations, not certifications by those third parties.</p><p class="p26-fine">Re-verified <time datetime="2026-11-19">{human_date(REVERIFIED)}</time>: the Associates Operating Agreement §5, Program Policies Participation Requirements 1(f)/(g) and 2(a)–(b), the Google outbound-link guidance and the FTC influencer-disclosure guide were re-read for this pass, and three product listings were re-opened; the record is in <a href="../sessions/6b68afc8/verification-2026-11-19.md">sessions/6b68afc8/verification-2026-11-19.md</a>. Nothing on this page changed as a result.</p><div class="p26-table-scroll" tabindex="0" role="region" aria-label="Decision questions, answer owners, evidence gaps and discovery actions"><table class="p26-table p26-question-table"><thead><tr><th scope="col">Question</th><th scope="col">Known / answer so far</th><th scope="col">Missing information</th><th scope="col">Who can answer · what counts as an answer</th><th scope="col">How to discover it</th><th scope="col">Safe default</th><th scope="col">Official basis</th></tr></thead><tbody>{''.join(rows)}</tbody></table></div></section>{review}<section class="p26-section" id="intake"><div class="p26-intake"><div><p class="p26-overline">HOW TO ADD ONE</p><h2>{esc(intake['title'])}</h2><p>{esc(intake['note'])}</p></div><dl class="p26-intake-list">{intake_rows}</dl></div></section><section class="p26-section" id="design-prompt"><p class="p26-overline">THE NEXT DESIGN BRIEF</p><h2>A prompt worth building from.</h2><p>{esc(DATA['design_prompt']['intro'])} It is a proposed direction grounded in the limits above — not an instruction to treat missing evidence as confirmed.</p><div class="p26-prompt" id="p26-design-prompt">{''.join(blocks)}</div><div class="p26-prompt-actions"><button type="button" class="p26-button p26-button-outline" data-copy-prompt>Copy the whole brief</button><span id="p26-copy-status" role="status"></span></div></section><section class="p26-section"><h2>The publishing gate.</h2><ol class="p26-pipeline"><li><strong>Discover</strong><span>Use authorized first-party inputs. Keep provenance and capture date.</span></li><li><strong>Draft</strong><span>Question-led, source-linked copy. Missing facts stay absent.</span></li><li><strong>Check</strong><span>Disclosures, sponsored links, intent, API permissions, unsupported claims, feed and sitemap.</span></li><li><strong>Approve</strong><span>Require real evidence and account authority for gated capabilities.</span></li><li><strong>Measure</strong><span>Use real query, click and report evidence—not forecasts—to choose the next question.</span></li></ol></section></div>'''
    return shell(
        'suggestions/index.html',
        'Suggestions, missing information and decision review',
        f'Review {len(DATA["paths"])} paths and {len(DATA["proposals"])} proposals against {len(DATA["questions"])} open questions{", plus the " + DATA["review_b9008684"]["date"] + " review round" if DATA.get("review_b9008684") else ""}, each with its answer owner, discovery action and safe default, plus a {len(DATA["design_prompt"]["blocks"])}-block design brief. Saving a review never implements changes.',
        body,
    )


def about() -> str:
    return shell('about.html', 'Useful beats breathless: our editorial approach', 'Who publishes Zone3 Kitchen, how we use AI, what our guides do and do not establish, and how affiliate links work.', f'''<div class="p26-container p26-narrow"><div class="p26-page-intro"><p class="p26-overline">ABOUT ZONE3 KITCHEN</p><h1>Useful beats<br><em>breathless.</em></h1><p>A small kitchen publication built around a simple idea: a better shopping question is more useful than another must-have list.</p></div><div class="p26-prose"><section id="authorship"><h2>Who is speaking?</h2><p><strong>Zone3 Editorial</strong> is the publisher byline for this site, not a fictional named reviewer. The guides are AI-assisted and based on the official pages linked in the text. We have not performed hands-on product testing or claimed professional credentials.</p><p>Publication byline, source capture date and the limits of the evidence appear on each guide. A listing claim remains a listing claim. It is not independent confirmation of accuracy, durability, certification, cooking results or suitability.</p></section><section><h2>What you can expect from a guide.</h2><ul><li>A real buying question, not a manufactured urgency.</li><li>The product format and features the linked listing actually names.</li><li>Practical prompts for the measurements, manuals and trade-offs you should check.</li><li>Visible unknowns rather than invented values, prices or review scores.</li><li>A useful next read, and permission not to buy.</li></ul><p>Google’s <a href="{SOURCES['google-reviews']['url']}">review guidance</a> calls for original evidence and support for “best” recommendations. Until such evidence exists, we publish buying questions—not tested rankings.</p></section><section id="disclosure"><h2>Our affiliate relationship, plainly.</h2><p><strong>{chrome.DISCLOSURE}</strong></p><p>We may earn a commission if a qualifying purchase follows an eligible Amazon link. Outbound product links are labelled sponsored and identify Amazon as the destination. This website is not operated, sponsored or endorsed by Amazon.</p><p>The selected tracking ID, <code>shopnow047c-20</code>, was supplied in the brief. We have not verified its account assignment or attribution. The exact compliance status of the submitted short links remains <a href="flagged.html#FLG-003">unresolved (FLG-003)</a>; we do not call them invalid. Intended ASINs remain separate from observed redirect destinations in the <a href="intent-record/index.html">confirmation record</a>.</p><p>Official references: {source_link('amazon-agreement')} · {source_link('amazon-policies')} · {source_link('ftc')}.</p></section><section id="imagery"><h2>The pictures are context, not proof.</h2><p>The kitchen still life is an AI-generated editorial image. The format drawings are original generic diagrams. Neither depicts evidence from product testing or promises the exact appearance of a listed model. No Amazon product photograph is scraped or republished in this publication.</p></section><section><h2>How the next topic is chosen.</h2><p>{esc(DATA['meta']['cadence'])} Search demand, trending status, conversions and revenue are unverified. The next topics are editorial hypotheses until dated authorized reports exist.</p><p><a href="suggestions/index.html">Review the proposed next steps</a> · <a href="privacy.html">Privacy & measurement</a> · <a href="sources.html">The full source register</a>.</p></section></div>{follow()}</div>''')


def privacy() -> str:
    return shell('privacy.html', 'Privacy and measurement, without the fine-print maze', 'The five first-party events, no cookies or visitor profiles, production status, local review storage and the limits of static hosting.', f'''<div class="p26-container p26-narrow"><div class="p26-page-intro"><p class="p26-overline">PRIVACY & MEASUREMENT / UPDATED 19 NOV 2026</p><h1>Count the questions.<br><em>Not the people.</em></h1><p>No advertising pixels, no visitor profiles, no invented conversion numbers.</p></div><div class="p26-prose"><h2>Production collection is not active.</h2><p>The production endpoint is not configured. The first-party counter therefore makes no analytics request. A real same-origin collector is available in the development preview for testing only; preview tests are not campaign results.</p><h2>What the counter is built to measure.</h2><p>One active runtime schema defines five events: <code>page_view</code>, <code>outbound_click</code>, <code>guide_view</code>, <code>intent_view</code> and <code>flag_view</code>. These are site events, not unique people, sessions or purchases. A click does not prove an order or commission.</p><p>When enabled, it sends only an allowed event, a page path without query string or fragment, and—for outbound clicks only—an approved Amazon host and public product token. The collector assigns the UTC day and stores daily aggregate counts. It does not keep raw event rows, IP addresses, user agents, referrers or visitor identifiers. Requests omit credentials and referrer information. Like any web request, the connection necessarily exposes an IP address to the receiving host and may include browser-supplied headers such as User-Agent. They are not event-body fields, and this collector does not log or store them.</p><p>Global Privacy Control, Do Not Track, or Save-Data disables the counter. Analytics writes no cookies, localStorage, sessionStorage or fingerprint. The browser makes no request if configuration is missing or invalid.</p><h2>Other local browser behaviour.</h2><p>Search runs locally after downloading a public search index; search text is not sent to analytics. Suggestions are saved in <code>localStorage</code> only when you explicitly press Save. That record contains proposal choices and a save date, not an identity, and is not sent to a server. You can clear it on the suggestions page. Export downloads a JSON file to your device.</p><h2>The hosting and retailer limits.</h2><p>{source_link('github-pages')} states that GitHub logs visitor IP addresses for security. Our code cannot prevent hosting-provider logs. If you open Amazon, that site handles the visit under its own policies. An external collector host or reverse proxy must also be configured not to retain request logs; this code cannot certify an undeployed host.</p><p>The reference collector retains aggregate counts for 90 UTC days, rejects unapproved origins and oversized/invalid payloads, and exposes totals only with a server-side read token. The reference has a global write ceiling as a basic abuse guard; it is not a bot-detection or unique-session system.</p><h2>Orders belong in authorized reports.</h2><p>No visitor-level Amazon sub-tag is assigned. The campaign ledger stays empty until authorized first-party evidence is available, with timestamp, source, channel, eligible sessions, clicks, reported orders and provenance. {source_link('amazon-policies')} governs Associates links and reporting, including its end-user restriction in Participation Requirements 2(b).</p><p>See <a href="measurement/index.html">the current measurement configuration</a> and <a href="suggestions/index.html#P26-Q3">what is still needed for production</a>.</p></div></div>''')


def executive() -> str:
    rows = [
        ('Publication', 'Shipped', f'One buyer-first front page, catalogue and {numeral(GUIDE_N).lower()} question-led guides; shared navigation, disclosure, RSS and canonical indexing.', 'google-reviews'),
        ('Five submitted products', 'Observed, not intent-confirmed', f'Three air-fryer and two thermometer destinations re-opened {READ_ON}; title and breadcrumb checks only. Intent fields remain blank.', 'amazon-agreement'),
        ('Affiliate attribution', 'Unverified', 'Tracking ID supplied by the brief; enrolled-workflow destination and report checks are still required. FLG-003 remains unresolved.', 'amazon-policies'),
        ('Measurement', 'Built and locally testable; production off', 'One five-event runtime and a hardened self-hosted aggregate collector. No durable production host was supplied.', 'github-pages'),
        ('Traffic & conversion', 'No evidence yet', 'No Search Console query report, authorized Associates report, measured conversion score or revenue forecast.', 'search-console'),
        ('Decision desk', 'Published for review', f'{len(DATA["paths"])} paths and {len(DATA["proposals"])} proposals against {len(DATA["questions"])} open questions, each with an answer owner, a discovery action and a safe default; a {len(DATA["design_prompt"]["blocks"])}-block design brief is copy-ready. Choosing a path saves a local note and implements nothing.', 'amazon-policies'),
        ('Review workflow', 'Shipped', 'Local review, export, clear-choices, per-block copy and the publishing-gate order are live on the suggestions page. No account, spend or publication action is wired to it.', 'ftc'),
        ('Automation', 'Gated', 'Build, provenance structure, disclosure, sponsored links, feed/sitemap and tests are automated. Missing account permissions and research evidence are not fabricated.', 'amazon-policies'),
        ('Commercial hosting', 'Needs review', 'GitHub Pages limits restrict business/commercial-transaction-oriented hosting. Technical deployment does not establish policy approval.', 'github-limits'),
    ]
    table = ''.join(f'<tr><th scope="row">{esc(a)}</th><td>{esc(b)}</td><td>{esc(c)}</td><td>{source_link(s)}</td></tr>' for a,b,c,s in rows)
    return shell('executive-brief.html', 'Executive brief: what shipped, what is still unverified', 'A concise evidence-based summary of the publication, five product destinations, analytics, affiliate attribution, automation gates and remaining decisions.', f'''<div class="p26-container"><div class="p26-page-intro"><p class="p26-overline">EXECUTIVE BRIEF / 19 NOV 2026</p><h1>A publication first.<br><em>A trustworthy machine beneath it.</em></h1><p>The buyer experience is rebuilt. The missing account access, performance evidence and production host are visible gaps—not made-up accomplishments.</p></div><div class="p26-summary-strip"><div><b>5</b><span>submitted product links</span></div><div><b>6</b><span>question-led buyer guides</span></div><div><b>9</b><span>decision-readiness questions</span></div><div><b>0</b><span>campaign evidence rows</span></div></div><section class="p26-section"><h2>Important details, at a glance.</h2><div class="p26-table-scroll" tabindex="0" role="region" aria-label="Executive brief with official references"><table class="p26-table"><thead><tr><th scope="col">Area</th><th scope="col">Status</th><th scope="col">What that means</th><th scope="col">Official basis</th></tr></thead><tbody>{table}</tbody></table></div><p class="p26-fine">The source column explains the applicable rule or decision basis; shipped-code assertions are repository observations, not claims verified by those third parties. Current verification scope: <a href="sessions/b580d790/verification-2026-11-19.md">19 Nov 2026 verification record</a> · <a href="sessions/1c072a7a/verification-2026-11-19.md">earlier 19 Nov 2026 record</a>. Historical claims retain their original dates and have not all been re-verified in this pass.</p></section><section class="p26-section"><h2>The recommended order of work.</h2><ol class="p26-checklist"><li>Confirm product intent and validate one Special Link per product in an authorized enrolled workflow.</li><li>Resolve durable, commercially suitable hosting and deploy the collector; verify privacy controls and delivery.</li><li>Verify Search Console and obtain first-party query and Associates reports.</li><li>Review one guide every 14 days, choosing new questions from measured evidence once it exists.</li><li>Only then evaluate authorized API enrichment, original testing and campaign optimization.</li></ol><a class="p26-button" href="suggestions/index.html">Review the suggestions {icon('arrow')}</a> <a class="p26-text-link" href="flagged.html">All flagged items</a></section></div>''')


def previous_edition() -> str:
    """Preserve the completed C3/C17 shopper edition, using their untouched renderers.

    Both legacy entry points protect their original z3-main ownership. Compose them on a
    scratch page, never on the current p26 root; the canonical shell pass then gives the
    historical edition its own noindex URL and the same current navigation/disclosure.
    """
    legacy = load_module('sessions/aebf0747/build_pass.py', 'publication_legacy_base')
    c3 = load_module('sessions/c3be74f2/build_front_page.py', 'publication_legacy_c3')
    c17 = load_module('sessions/c17d25fd/build_shopfront.py', 'publication_legacy_c17')
    with tempfile.TemporaryDirectory(prefix='zone3-previous-') as directory:
        scratch = Path(directory) / 'index.html'
        scratch.write_text(legacy.front_page(), encoding='utf-8')
        for module in (c3, c17):
            module.PAGE = scratch
            scratch.write_text(module.render(), encoding='utf-8')
        raw = scratch.read_text(encoding='utf-8')
        if c17.render() != raw:
            raise ValueError('Retained C17 edition is not idempotent')
    raw = raw.replace('<title>Zone3 |', '<title>Previous shopper edition — Zone3 |', 1)
    raw = re.sub(r'(<meta property="og:url" content=")[^"]*(">)', lambda m: m[1] + chrome.canonical('publication-prior.html') + m[2], raw)
    return raw


def outputs() -> dict[str, str]:
    pages = {'publication-prior.html': previous_edition(), 'index.html': home(), 'guides/index.html': guide_index(), 'suggestions/index.html': suggestions(), 'about.html': about(), 'privacy.html': privacy(), 'executive-brief.html': executive()}
    pages.update({f'guides/{g["slug"]}.html': guide_page(g) for g in DATA['guides']})
    for cat, cmp in [('all', False), ('air-fryers', False), ('meat-thermometers', False), ('all', True)]:
        rel, doc = catalogue(cat, cmp)
        pages[rel] = doc
    existing = {p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*') if p.is_file()} | set(pages)
    pp = load_module('sessions/aebf0747/publish_pass.py', 'publication_postprocess')
    mp = load_module('tools/measure_pass.py', 'publication_measure')
    for rel in pages:
        pages[rel], missing = pp.apply(pages[rel], rel, existing)
        pages[rel] = mp.apply(pages[rel], rel)
        if missing:
            raise ValueError('Missing workspace destinations: ' + ', '.join(missing))
    search = [{'title': g['title'], 'description': g['dek'], 'kind': g['category'], 'path': f'guides/{g["slug"]}.html'} for g in DATA['guides']]
    search += [{'title': p['brand'] + ' ' + p['name'], 'description': p['description'], 'kind': 'Product shortlist', 'path': f'shop/{p["category"]}/index.html#{p["id"]}'} for p in DATA['products']]
    pages['assets/publication-search.json'] = json.dumps(search, ensure_ascii=False, indent=2) + '\n'
    return pages


def build(check: bool = False) -> int:
    stale = []
    for rel, text in outputs().items():
        path = ROOT / rel
        if not path.exists() or path.read_text(encoding='utf-8') != text:
            stale.append(rel)
            if not check:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(text, encoding='utf-8')
    print(f'Publication: {len(outputs()) - 1} pages; ' + ('current' if not stale else ('STALE ' if check else 'updated ') + ', '.join(stale)))
    return int(check and bool(stale))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    sys.exit(build(parser.parse_args().check))
