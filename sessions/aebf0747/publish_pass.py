#!/usr/bin/env python3
"""Idempotent publication pass for every current public HTML page.

One masthead, a disclosure immediately beneath it, one shared footer, sponsored Amazon
product links, local search, and explicit reader-vs-research indexing. Historical page
bodies/evidence are retained. docs/, sessions/ and archive/ remain historical snapshots.
Run after any HTML generator; --check fails if the final chrome would drift.

The disclosure rule implements the brief's placement requirement; it is not a legal
certification or a claim that a byte offset proves visibility in every viewport.
"""
from __future__ import annotations

import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools'))
import publication_chrome as chrome

SKIP_TOP = {'.git', 'archive', 'docs', 'sessions', 'node_modules', '__pycache__', '.preview', '.local'}
DISCLOSURE = chrome.DISCLOSURE
SITE_URL = chrome.BASE
PRODUCT_HOST = re.compile(
    r'^(?:[a-z0-9-]+\.)*(?:amazon\.(?:com|co\.uk|de|fr|ca|com\.au|co\.jp|in|com\.br|com\.mx|'
    r'es|it|nl|se|pl|sa|ae|com\.tr|eg|sg|cn)|link\.amazon\.com|link\.amazon|amzn\.to|a\.co|amzlinks\.in)$'
)
NON_PRODUCT_HOSTS = ('affiliate-program.amazon.com',)
FOOTER_GROUPS = chrome.WORKSPACE_GROUPS
RE_STRIP = re.compile(r'<!-- z3:strip -->.*?<!-- /z3:strip -->\n?', re.S)
RE_FOOT = re.compile(r'<!-- z3:footer -->.*?<!-- /z3:footer -->\n?', re.S)
RE_MAST = re.compile(r'<!-- p26:masthead -->.*?<!-- /p26:masthead -->\n?', re.S)
RE_SEARCH = re.compile(r'<!-- p26:search -->.*?<!-- /p26:search -->\n?', re.S)
RE_ASSETS = re.compile(r'<!-- p26:assets -->.*?<!-- /p26:assets -->\n?', re.S)
RE_REFERENCE = re.compile(r'<!-- p26:reference -->.*?<!-- /p26:reference -->\n?', re.S)
RE_INDEX = re.compile(r'<!-- p26:indexing -->.*?<!-- /p26:indexing -->\n?', re.S)

prefix_for = chrome.prefix_for
strip_block = chrome.strip_block
footer_block = chrome.footer_block


def top_masthead_end(text: str) -> int:
    body = re.search(r'<body\b[^>]*>', text, re.I)
    if not body:
        raise ValueError('no <body>')
    start = body.end()
    main = re.search(r'<main\b', text[start:], re.I)
    limit = start + (main.start() if main else min(len(text) - start, 20000))
    header = re.search(r'<header\b', text[start:limit], re.I)
    if header:
        close = re.search(r'</header\s*>', text[start + header.start():], re.I)
        if close:
            return start + header.start() + close.end()
    return start


def _sponsor_anchor(tag: str) -> str:
    href_m = re.search(r'''\shref\s*=\s*(["'])(.*?)\1''', tag, re.I)
    if not href_m:
        return tag
    host_m = re.match(r'^(?:https?:)?//([^/?#]+)', href_m.group(2).strip(), re.I)
    if not host_m:
        return tag
    host = host_m.group(1).lower().split('@')[-1].split(':')[0]
    if any(host == h or host.endswith('.' + h) for h in NON_PRODUCT_HOSTS) or not PRODUCT_HOST.fullmatch(host):
        return tag
    rel_m = re.search(r'''\srel\s*=\s*(["'])(.*?)\1''', tag, re.I)
    if rel_m:
        tokens = rel_m.group(2).split()
        if 'sponsored' in tokens:
            return tag
        tokens.append('sponsored')
        return tag[:rel_m.start()] + f' rel="{" ".join(tokens)}"' + tag[rel_m.end():]
    return tag[:-2] + ' rel="sponsored"/>' if tag.endswith('/>') else tag[:-1] + ' rel="sponsored">'


def apply(text: str, rel: str, existing: set[str]) -> tuple[str, list[str]]:
    prefix = prefix_for(rel)
    for pattern in (RE_STRIP, RE_FOOT, RE_MAST, RE_SEARCH, RE_ASSETS, RE_INDEX, RE_REFERENCE):
        text = pattern.sub('', text)
    # Replace duplicated chrome, not the historical page's main content.
    text = re.sub(r'<footer\b.*?</footer\s*>', '', text, flags=re.S | re.I)
    text = text.replace('<!-- z3:masthead -->', '')
    body = re.search(r'<body\b[^>]*>', text, re.I)
    if not body:
        raise ValueError(f'{rel}: no body element')
    main = re.search(r'<main\b[^>]*>', text[body.end():], re.I)
    if main:
        main_start = body.end() + main.start()
        main_tag = main.group(0)
        id_match = re.search(r'''\bid=["']([^"']+)["']''', main_tag, re.I)
        main_id = id_match.group(1) if id_match else 'p26-content'
        if not id_match:
            new_tag = main_tag[:-1] + ' id="p26-content">'
            text = text[:main_start] + new_tag + text[main_start + len(main_tag):]
        preamble = text[body.end():main_start]
        # These mark the retained shopper edition's content owner, not old chrome.
        ownership = list(dict.fromkeys(re.findall(r'<!-- (?:c3be74f2:front|c17d25fd:shopfront) -->', preamble)))
        preamble = re.sub(r'<header\b.*?</header\s*>', '', preamble, flags=re.S | re.I)
        preamble = re.sub(r'<a\b[^>]*class=["\'][^"\']*\bskip\b[^"\']*["\'][^>]*>.*?</a>', '', preamble, flags=re.S | re.I)
        # The inherited pre-main blocks were inspected: header + duplicate disclosure only.
        # Their testing/affiliate caveats are repeated in the shared footer and source pages.
        if DISCLOSURE in preamble:
            preamble = ''
        preamble = re.sub(r'<!--.*?-->', '', preamble, flags=re.S).strip()
        opening = chrome.masthead(prefix, rel, existing, main_id) + strip_block(prefix) + ''.join(ownership)
        text = text[:body.end()] + '\n' + opening + (preamble + '\n' if preamble else '') + text[main_start:].lstrip()
    else:
        # Legacy redirect stubs still get an above-content disclosure and a working skip link.
        main_id = 'p26-content'
        rest = text[body.end():]
        rest = re.sub(r'<header\b.*?</header\s*>', '', rest, flags=re.S | re.I).strip()
        rest = re.sub(r'</body\s*>', '</main></body>', rest, count=1, flags=re.I)
        text = text[:body.end()] + '\n' + chrome.masthead(prefix, rel, existing, main_id) + strip_block(prefix) + f'<main id="{main_id}">' + rest

    if rel.startswith('site/'):
        # Preserve the source-read date originally stated only in the old /site/ footer,
        # and clearly distinguish the earlier edition from the current front page.
        reference = ('<!-- p26:reference --><aside class="p26-reference">Earlier reader edition: '
                     'original source-read date <strong>2026-11-16</strong>. '
                     f'<a href="{prefix}index.html">Current publication</a> · '
                     f'<a href="{prefix}executive-brief.html">Current operational status</a>.'
                     '</aside><!-- /p26:reference -->\n')
        text = re.sub(r'(<main\b[^>]*>)', lambda m: m.group(1) + reference, text, count=1, flags=re.I)
    if rel == 'publication-prior.html':
        reference = ('<!-- p26:reference --><aside class="p26-reference">'
                     'Previous shopper edition (C3/C17/3301), preserved from the completed 19 Nov 2026 passes. '
                     'Its listing/source observations retain their original dates; old operational statements are historical. '
                     '<a href="index.html">Current publication</a> · '
                     '<a href="executive-brief.html">Current status</a> · '
                     '<a href="flagged.html#C3-F-01">Inherited provenance caveat</a>.'
                     '</aside><!-- /p26:reference -->\n')
        text = re.sub(r'(<main\b[^>]*>)', lambda m: m.group(1) + reference, text, count=1, flags=re.I)
    if (not chrome.is_indexable(rel) and not rel.startswith('site/')
            and rel not in {'publication-prior.html', 'executive-brief.html', 'suggestions/index.html',
                            'measurement/index.html', 'intent-record/index.html'}):
        reference = ('<!-- p26:reference --><aside class="p26-reference">Research workspace: '
                     'this page retains dated material from earlier passes. '
                     f'<a href="{prefix}executive-brief.html">Current implementation status</a> · '
                     f'<a href="{prefix}measurement/index.html">Current measurement definition</a> · '
                     f'<a href="{prefix}flagged.html#P26-F05">Historical verification limits</a>.'
                     '</aside><!-- /p26:reference -->\n')
        text = re.sub(r'(<main\b[^>]*>)', lambda m: m.group(1) + reference, text, count=1, flags=re.I)
    foot, missing = footer_block(prefix, existing)
    tail = chrome.search_block(prefix) + foot
    text = re.sub(r'</body\s*>', lambda _: tail + '</body>', text, count=1, flags=re.I)
    text = re.sub(r'<a\b[^>]*>', lambda m: _sponsor_anchor(m.group(0)), text, flags=re.I)

    if not re.search(r'<meta[^>]+name=["\']description["\']', text, re.I):
        title = re.search(r'<title>([^<]*)</title>', text, re.I)
        description = (title.group(1).strip() if title else rel).replace('"', '&quot;')
        text = re.sub(r'</head\s*>', lambda _: f'<meta name="description" content="{description}">\n</head>', text, count=1, flags=re.I)
    # Do not canonicalize different audit content to an unrelated reader page. Keep its own
    # normalized URL and explicitly exclude it from indexing instead.
    text = re.sub(r'<meta\b[^>]*name=["\']robots["\'][^>]*>\n?', '', text, flags=re.I)
    text = re.sub(r'<link\b[^>]*rel=["\']canonical["\'][^>]*>\n?', '', text, flags=re.I)
    indexing = 'index,follow,max-image-preview:large' if chrome.is_indexable(rel) else 'noindex,follow'
    tags = ''
    if 'zone3-publication.css' not in text:
        tags += f'<!-- z3:css --><link rel="stylesheet" href="{prefix}assets/zone3-publication.css">\n'
    if 'application/rss+xml' not in text:
        tags += f'<!-- z3:rss --><link rel="alternate" type="application/rss+xml" title="Zone3 Kitchen guides" href="{prefix}feed.xml">\n'
    tags += f'<!-- p26:indexing --><meta name="robots" content="{indexing}"><link rel="canonical" href="{chrome.canonical(rel)}"><!-- /p26:indexing -->\n'
    tags += f'<!-- p26:assets --><link rel="stylesheet" href="{prefix}assets/publication.css"><script src="{prefix}assets/publication.js" defer></script><!-- /p26:assets -->\n'
    # The measurement pass owns the last head block. Insert before it so either pass
    # can be checked independently after the full chain without reordering the head.
    measure = re.search(r'<!-- z3:measure -->', text)
    if measure:
        text = text[:measure.start()] + tags + text[measure.start():]
    else:
        text = re.sub(r'</head\s*>', lambda _: tags + '</head>', text, count=1, flags=re.I)
    return text, missing


def targets(root: pathlib.Path):
    for p in sorted(root.rglob('*.html')):
        rel = p.relative_to(root).as_posix()
        if rel.split('/')[0] not in SKIP_TOP:
            yield p, rel


def run(root: pathlib.Path = ROOT, write: bool = True) -> dict:
    existing = {p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file()}
    stats = {'pages': 0, 'changed': 0, 'missing_footer_targets': set()}
    for p, rel in targets(root):
        stats['pages'] += 1
        old = p.read_text(encoding='utf-8')
        new, missing = apply(old, rel, existing)
        stats['missing_footer_targets'].update(missing)
        if new != old:
            stats['changed'] += 1
            if write:
                p.write_text(new, encoding='utf-8')
    stats['missing_footer_targets'] = sorted(stats['missing_footer_targets'])
    return stats


if __name__ == '__main__':
    check = '--check' in sys.argv
    result = run(write=not check)
    print(result)
    sys.exit(int(check and bool(result['changed'])))
