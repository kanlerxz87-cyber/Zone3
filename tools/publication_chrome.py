#!/usr/bin/env python3
"""One shared reader masthead, disclosure, footer and search dialog.

This is presentation code, not a source-verification engine. All historical tools remain
reachable. The main nav has exactly one group for research/dashboard destinations.
"""
from __future__ import annotations

import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = 'https://kanlerxz87-cyber.github.io/Zone3/'
DISCLOSURE = 'As an Amazon Associate I earn from qualifying purchases.'

# Keep all previous shared-footer destinations and all current flat research surfaces.
WORKSPACE_GROUPS = [
    ('Start here', [
        ('executive-brief.html', 'Executive brief'),
        ('suggestions/index.html', 'Suggestions & decisions'),
        ('flagged.html', 'Flagged for review'),
        ('measurement/index.html', 'Measurement status (current)'),
        ('intent-record/index.html', 'Product-intent record'),
    ]),
    ('Research desk', [
        ('dashboard/index.html', 'Research dashboard'),
        ('dashboard-register.html', 'Previous front-page register'),
        ('products.html', 'Product evidence'),
        ('analysis.html', 'Original analysis'),
        ('air-fryers.html', 'Original air-fryer category'),
        ('measurement.html', 'Original measurement page'),
        ('sources.html', 'Source register (S-IDs)'),
        ('verification.html', 'Verification log'),
        ('pricing.html', 'Pricing & commission'),
        ('reviews.html', 'Reviews & competition'),
        ('campaigns.html', 'Campaign ledger'),
        ('content.html', 'Content & compliance'),
        ('content-topics.html', 'Topic proposals'),
        ('suggestions.html', 'Historical suggestions register'),
        ('decision-center.html', 'Decision center'),
        ('decision-queue.html', 'Decision queue'),
        ('design-brief.html', 'Original design brief'),
        ('direction/index.html', 'Earlier design directions'),
    ]),
    ('Reference', [
        ('publication-pass.html', 'Previous publication pass'),
        ('publication-prior.html', 'Previous shopper edition (C3/C17)'),
        ('brief-status/index.html', 'Brief status'),
        ('executive-summary/index.html', 'Research executive summary'),
        ('executive-summary.html', 'Full executive summary'),
        ('compliance/index.html', 'Compliance register'),
        ('agent-terms/index.html', 'Agent terms'),
        ('methodology/index.html', 'Research methodology'),
        ('requirements/index.html', 'Requirements'),
        ('sources/index.html', 'Research source register'),
        ('flagged/index.html', 'Research flag register'),
        ('products/index.html', 'Research product register'),
        ('pricing/index.html', 'Research pricing register'),
        ('commission/index.html', 'Commission register'),
        ('reviews/index.html', 'Research reviews register'),
        ('niches/index.html', 'Niche research'),
        ('campaigns/index.html', 'Research campaign register'),
        ('content/index.html', 'Research content register'),
        ('repo-review/index.html', 'Repository review'),
        ('articles/index.html', 'Research Desk articles'),
        ('read/index.html', 'The Crisp Report archive'),
        ('site/index.html', 'Field Notes archive'),
    ]),
]


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def prefix_for(rel: str) -> str:
    return '../' * rel.count('/')


def canonical(rel: str) -> str:
    return BASE + ('' if rel == 'index.html' else rel[:-10] if rel.endswith('/index.html') else rel)


def is_indexable(rel: str) -> bool:
    data = json.loads((ROOT / 'data/publication.json').read_text(encoding='utf-8'))
    return rel in data['indexable_pages']


def icon(name: str, cls: str = '') -> str:
    paths = {
        'arrow': '<path d="M5 12h14M13 6l6 6-6 6"/>',
        'external': '<path d="M7 17 17 7M7 7h10v10"/>',
        'search': '<circle cx="10.5" cy="10.5" r="6.5"/><path d="m16 16 4.5 4.5"/>',
        'close': '<path d="m6 6 12 12M6 18 18 6"/>',
        'menu': '<path d="M4 6h16M4 12h16M4 18h16"/>',
        'rss': '<path d="M5 4a15 15 0 0 1 15 15M5 10a9 9 0 0 1 9 9"/><circle cx="5" cy="19" r="1"/>',
        'check': '<path d="m5 12 4 4L19 6"/>',
        'bookmark': '<path d="M6 4h12v17l-6-4-6 4z"/>',
    }
    return f'<svg class="p26-icon {esc(cls)}" viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">{paths[name]}</svg>'


def brand(prefix: str) -> str:
    # Use the actual visible brand/tagline as the accessible name (WCAG 2.5.3).
    return f'<a class="p26-brand" href="{prefix}index.html">zone<span>3</span><i aria-hidden="true"></i><small> KITCHEN, CONSIDERED.</small></a>'


def workspace_links(prefix: str, existing: set[str], full: bool = True) -> str:
    groups = WORKSPACE_GROUPS if full else WORKSPACE_GROUPS[:1]
    return ''.join(
        f'<div class="p26-menu-group"><span class="p26-overline">{esc(title)}</span>'
        + ''.join(f'<a href="{prefix}{path}">{esc(label)}</a>' for path, label in links if path in existing)
        + '</div>' for title, links in groups
    )


def masthead(prefix: str, rel: str, existing: set[str], main_id: str = 'main') -> str:
    items = [
        ('index.html', 'The edit'),
        ('guides/index.html', 'Buying guides'),
        ('shop/air-fryers/index.html', 'Air fryers'),
        ('shop/meat-thermometers/index.html', 'Thermometers'),
    ]
    links = ''.join(f'<a href="{prefix}{path}"' + (' aria-current="page"' if path == rel else '') + f'>{label}</a>' for path, label in items)
    return (
        '<!-- p26:masthead -->\n'
        f'<a class="p26-skip" href="#{esc(main_id)}">Skip to content</a>'
        '<header class="p26-header topbar">'
        '<div class="p26-header-inner">' + brand(prefix)
        + '<button class="p26-menu-toggle" type="button" aria-expanded="false" aria-controls="p26-primary">' + icon('menu') + '<span>Menu</span></button>'
        + '<nav class="p26-nav" id="p26-primary" aria-label="Main">' + links
        + '<details class="p26-workspace"><summary>Behind the site <span aria-hidden="true">⌄</span></summary>'
        + '<div class="p26-workspace-panel">' + workspace_links(prefix, existing) + '</div></details></nav>'
        + f'<a class="p26-search-trigger" href="{prefix}guides/index.html" data-search-open aria-label="Find a guide">' + icon('search') + '</a>'
        + '</div></header>\n<!-- /p26:masthead -->\n'
    )


def strip_block(prefix: str) -> str:
    return (
        '<!-- z3:strip -->\n'
        '<aside class="p26-disclosure z3-strip disclose-bar" aria-label="Affiliate disclosure"><div class="p26-container">'
        '<span class="p26-disclosure-label">A NOTE ON OUR LINKS</span>'
        f'<p>{DISCLOSURE} <a href="{prefix}about.html#disclosure">How we work</a></p>'
        '</div></aside>\n<!-- /z3:strip -->\n'
    )


def search_block(prefix: str) -> str:
    return (
        '<!-- p26:search -->\n'
        f'<dialog class="p26-search-dialog" id="p26-search" aria-labelledby="p26-search-title" data-search-index="{prefix}assets/publication-search.json" data-root="{prefix}">'
        '<div class="p26-search-heading"><h2 id="p26-search-title">What are you deciding?</h2>'
        '<button type="button" data-search-close aria-label="Close search">' + icon('close') + '</button></div>'
        '<label for="p26-query">Search the guides and product shortlist</label>'
        '<input id="p26-query" type="search" placeholder="Try capacity, cleanup, or thermometer…" autocomplete="off" maxlength="100">'
        '<p class="p26-fine">Search stays in your browser. No query is sent to analytics.</p>'
        '<div id="p26-search-results" aria-live="polite"></div></dialog>\n<!-- /p26:search -->\n'
    )


def footer_block(prefix: str, existing: set[str]) -> tuple[str, list[str]]:
    needed = {p for _, links in WORKSPACE_GROUPS for p, _ in links}
    missing = sorted(needed - existing)
    return (
        '<!-- z3:footer -->\n'
        '<footer class="p26-footer z3-foot" role="contentinfo"><div class="p26-container">'
        '<div class="p26-footer-top"><div>' + brand(prefix)
        + '<p>A considered kitchen starts<br>with a good question.</p></div>'
        + '<div class="p26-footer-links"><div><h2>Find your next read</h2>'
        + f'<a href="{prefix}guides/index.html">All buying guides</a><a href="{prefix}shop/air-fryers/index.html">Air fryers</a><a href="{prefix}shop/meat-thermometers/index.html">Meat thermometers</a><a href="{prefix}shop/index.html">The product shortlist</a></div>'
        + f'<div><h2>About Zone3</h2><a href="{prefix}about.html">Our editorial approach</a><a href="{prefix}about.html#disclosure">Affiliate disclosure</a><a href="{prefix}style.html">How we write</a><a href="{prefix}privacy.html">Privacy & measurement</a><a href="{prefix}feed.xml">Follow by RSS</a></div>'
        + f'<div><h2>Behind the site</h2><a href="{prefix}suggestions/index.html">Suggestions & decisions</a><a href="{prefix}executive-brief.html">Executive brief</a><a href="{prefix}flagged.html">Flagged for review</a><a href="{prefix}measurement/index.html">Measurement status</a></div></div></div>'
        + '<details class="p26-research-tools"><summary>All research tools & source registers <span aria-hidden="true">+</span></summary><div class="p26-tools-grid">'
        + workspace_links(prefix, existing) + '</div></details>'
        + f'<div class="p26-footer-bottom"><p class="foot-disclose">{DISCLOSURE} All outbound Amazon product links are marked sponsored.</p>'
        + '<p>AI-assisted, source-linked editorial. No independent product testing has been performed. Not operated or endorsed by Amazon.</p>'
        + '<p class="p26-amazon-notice">CERTAIN CONTENT THAT APPEARS ON THIS SITE COMES FROM AMAZON. THIS CONTENT IS PROVIDED “AS IS” AND IS SUBJECT TO CHANGE OR REMOVAL AT ANY TIME.</p>'
        + f'<p class="p26-copyright">© 2026 Zone3 Kitchen <span>Fewer tabs. More considered choices.</span><a href="{prefix}sitemap.xml">Sitemap</a></p>'
        + '</div></div></footer>\n<!-- /z3:footer -->\n', missing
    )
