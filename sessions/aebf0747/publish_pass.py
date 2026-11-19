#!/usr/bin/env python3
"""Mechanical publication pass for the Zone3 GitHub Pages tree (session aebf0747).

Applies four rules to every published HTML page (all *.html except .git/ and archive/):

  1. DISCLOSURE ABOVE THE FOLD. The Associates sentence from Operating Agreement Section 5
     is placed directly under the top masthead. If the page already carries the sentence
     within the first 2,500 characters after its masthead, no second copy is added.
     [Sources: AE-S01 Operating Agreement s.5; AE-S04 FTC Disclosures 101: "Place it so
     it's hard to miss" and disclosures "likely to be missed" at the end of a page.]

  2. DISCLOSURE REPEATED IN THE FOOTER, with the dashboard surfaces listed as links.
     Legacy <footer> elements are left as they are; the shared footer is appended before
     </body> inside markers.

  3. rel="sponsored" ON EVERY OUTBOUND AMAZON PRODUCT LINK. Only the rel attribute is
     changed; href, text and target are not. Hosts: amazon.* retail domains, link.amazon.*,
     amzn.to, a.co, amzlinks.in. Excluded: affiliate-program.amazon.com (Associates policy
     pages, not product links). [Source: AE-S03 Google: rel="sponsored" for paid links.]

  4. HEAD MARKUP: the shared stylesheet and the RSS autodiscovery link.

Every insertion is wrapped in markers (<!-- z3:... -->), so re-running the script replaces
rather than duplicates. Run it AFTER any generator that rewrites HTML.

    python3 sessions/aebf0747/publish_pass.py            # apply to the tree
    python3 sessions/aebf0747/publish_pass.py --check    # exit 1 if a rerun would change files
"""
from __future__ import annotations

import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
SKIP_TOP = {".git", "archive", "docs", "sessions", "node_modules", "__pycache__"}  # docs/ and sessions/ excluded from the 83-page set
DISCLOSURE = "As an Amazon Associate I earn from qualifying purchases."
SITE_URL = "https://kanlerxz87-cyber.github.io/Zone3/"

PRODUCT_HOST = re.compile(
    r"^(?:[a-z0-9-]+\.)*(?:amazon\.(?:com|co\.uk|de|fr|ca|com\.au|co\.jp|in|com\.br|com\.mx|"
    r"es|it|nl|se|pl|sa|ae|com\.tr|eg|sg|cn)|link\.amazon\.com|link\.amazon|amzn\.to|a\.co|amzlinks\.in)$"
)
NON_PRODUCT_HOSTS = ("affiliate-program.amazon.com",)

# Surfaces reachable from the footer. Each path must exist; missing ones are dropped and reported.
FOOTER_GROUPS = [
    ("Read", [
        ("index.html", "Front page"),
        ("guides/index.html", "Guides"),
        ("articles/index.html", "Research Desk articles"),
        ("read/index.html", "The Crisp Report"),
        ("site/index.html", "Reader site"),
    ]),
    ("Products and pricing", [
        ("intent-record/index.html", "Product-intent record"),
        ("products/index.html", "Products"),
        ("pricing/index.html", "Pricing"),
        ("commission/index.html", "Commission"),
        ("reviews/index.html", "Reviews"),
        ("niches/index.html", "Niches"),
    ]),
    ("Governance", [
        ("publication-pass.html", "This pass and flagged for review"),
        ("measurement/index.html", "Measurement (counter off)"),
        ("brief-status/index.html", "Brief status"),
        ("executive-summary/index.html", "Executive summary"),
        ("compliance/index.html", "Compliance"),
        ("agent-terms/index.html", "Agent terms"),
        ("methodology/index.html", "Methodology"),
        ("requirements/index.html", "Requirements"),
        ("sources/index.html", "Sources"),
        ("verification.html", "Verification log"),
        ("flagged/index.html", "Flagged (all items)"),
    ]),
    ("Dashboards", [
        ("dashboard/index.html", "Dashboard"),
        ("dashboard-register.html", "Register (previous front page)"),
        ("analysis.html", "Analysis"),
        ("decision-center.html", "Decision center"),
        ("decision-queue.html", "Decision queue"),
        ("products.html", "Products register"),
        ("air-fryers.html", "Air-fryer category"),
        ("pricing.html", "Pricing & commission"),
        ("reviews.html", "Reviews & competition"),
        ("content.html", "Content & compliance"),
        ("content-topics.html", "Editorial topics"),
        ("campaigns.html", "Campaign tracking register"),
        ("campaigns/index.html", "Campaigns"),
        ("content/index.html", "Content dashboard"),
        ("measurement.html", "Measurement status"),
        ("measurement/index.html", "Measurement dashboard"),
        ("executive-summary.html", "Executive summary"),
        ("executive-summary/index.html", "Executive summary hub"),
        ("sources.html", "Sources register"),
        ("flagged.html", "Flagged register"),
        ("verification.html", "Verification log"),
        ("repo-review/index.html", "Repo review"),
        ("suggestions.html", "Suggestions"),
        ("design-brief.html", "Design brief"),
    ]),
    ("Feeds", [
        ("feed.xml", "RSS feed"),
        ("sitemap.xml", "Sitemap"),
    ]),
]

RE_STRIP = re.compile(r"<!-- z3:strip -->.*?<!-- /z3:strip -->\n?", re.S)
RE_FOOT = re.compile(r"<!-- z3:footer -->.*?<!-- /z3:footer -->\n?", re.S)


def prefix_for(rel: str) -> str:
    depth = rel.count("/")
    return "../" * depth


def strip_block(prefix: str) -> str:
    return (
        '<!-- z3:strip -->\n'
        '<div class="z3-strip" role="note" aria-label="Affiliate disclosure">'
        '<div class="z3-wrap"><p><strong>Disclosure:</strong> ' + DISCLOSURE +
        ' Links to Amazon are marked sponsored. '
        '<a href="' + prefix + 'publication-pass.html#disclosure">How disclosure is handled</a></p></div></div>\n'
        '<!-- /z3:strip -->\n'
    )


def footer_block(prefix: str, existing: set[str]) -> tuple[str, list[str]]:
    missing: list[str] = []
    groups_html = []
    for title, links in FOOTER_GROUPS:
        items = []
        for path, label in links:
            if path in existing:
                items.append(f'<a href="{prefix}{path}">{label}</a>')
            else:
                missing.append(path)
        if items:
            groups_html.append(f'<div><h4>{title}</h4><nav aria-label="{title}">' + "".join(items) + "</nav></div>")
    body = (
        '<!-- z3:footer -->\n'
        '<footer class="z3-foot" role="contentinfo"><div class="z3-wrap">'
        '<p class="z3-disc">' + DISCLOSURE + '</p>'
        '<p class="z3-foot-small">Links to Amazon are marked sponsored. This site is not operated by Amazon. '
        'Titles, ASINs and breadcrumbs are as observed on the dates shown; no price, rating or forecast is published here.</p>'
        '<div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:18px">'
        + "".join(groups_html) +
        '</div></div></footer>\n'
        '<!-- /z3:footer -->\n'
    )
    return body, missing


def top_masthead_end(html: str) -> int:
    """Index just after the top-level masthead (first <header> before <main>), else after <body>."""
    m_body = re.search(r"<body\b[^>]*>", html, re.I)
    if not m_body:
        raise ValueError("no <body>")
    start = m_body.end()
    m_main = re.search(r"<main\b", html[start:], re.I)
    limit = start + (m_main.start() if m_main else min(len(html) - start, 20000))
    m_hdr = re.search(r"<header\b", html[start:limit], re.I)
    if m_hdr:
        close = re.search(r"</header\s*>", html[start + m_hdr.start():], re.I)
        if close:
            return start + m_hdr.start() + close.end()
    return start


def _sponsor_anchor(tag: str) -> str:
    href_m = re.search(r"""\shref\s*=\s*(["'])(.*?)\1""", tag, re.I)
    if not href_m:
        return tag
    href = href_m.group(2).strip()
    host_m = re.match(r"^(?:https?:)?//([^/?#]+)", href, re.I)
    if not host_m:
        return tag
    host = host_m.group(1).lower().split("@")[-1].split(":")[0]
    if any(host == h or host.endswith("." + h) for h in NON_PRODUCT_HOSTS):
        return tag
    if not PRODUCT_HOST.match(host):
        return tag
    rel_m = re.search(r"""\srel\s*=\s*(["'])(.*?)\1""", tag, re.I)
    if rel_m:
        tokens = rel_m.group(2).split()
        if "sponsored" in tokens:
            return tag
        tokens.append("sponsored")
        return tag[:rel_m.start()] + f' rel="{" ".join(tokens)}"' + tag[rel_m.end():]
    if tag.endswith("/>"):
        return tag[:-2] + ' rel="sponsored"/>'
    return tag[:-1] + ' rel="sponsored">'


def apply(html: str, rel: str, existing: set[str]) -> tuple[str, list[str]]:
    prefix = prefix_for(rel)
    # 0. remove previous strip/footer so reruns replace rather than stack
    html = RE_STRIP.sub("", html)
    html = RE_FOOT.sub("", html)

    # 1. disclosure under the masthead
    end = top_masthead_end(html)
    window = html[end:end + 2500]
    if DISCLOSURE not in window:
        html = html[:end] + strip_block(prefix) + html[end:]

    # 2. footer before </body>
    foot, missing = footer_block(prefix, existing)
    if re.search(r"</body\s*>", html, re.I):
        html = re.sub(r"</body\s*>", lambda _m: foot + "</body>", html, count=1, flags=re.I)
    else:
        html = html + foot

    # 3. sponsored product links (attribute only)
    html = re.sub(r"<a\b[^>]*>", lambda m: _sponsor_anchor(m.group(0)), html, flags=re.I)

    # 4a. every page has a description (S-04): add a plain one from the title when missing
    if not re.search(r'<meta[^>]+name=["\']description["\']', html, re.I):
        t_m = re.search(r"<title>([^<]*)</title>", html, re.I)
        title_txt = (t_m.group(1).strip() if t_m else rel).replace('"', "&quot;")
        desc_tag = (f'<!-- z3:desc --><meta name="description" content="{title_txt}. '
                    f'Published by Zone3; checked on the date shown in the page.">\n')
        if t_m:
            html = html[:t_m.end()] + "\n" + desc_tag.rstrip("\n") + html[t_m.end():]
        else:
            html = re.sub(r"</head\s*>", lambda _m: desc_tag + "</head>", html, count=1, flags=re.I)

    # 4. head markup
    head_add = ""
    if "zone3-publication.css" not in html:
        head_add += f'<!-- z3:css --><link rel="stylesheet" href="{prefix}assets/zone3-publication.css">\n'
    if "application/rss+xml" not in html:
        head_add += (f'<!-- z3:rss --><link rel="alternate" type="application/rss+xml" '
                     f'title="Zone3 guides" href="{prefix}feed.xml">\n')
    if head_add:
        if re.search(r"</head\s*>", html, re.I):
            html = re.sub(r"</head\s*>", lambda _m: head_add + "</head>", html, count=1, flags=re.I)
        else:
            html = re.sub(r"<body\b", lambda m: head_add + m.group(0), html, count=1, flags=re.I)
    return html, missing


def targets(root: pathlib.Path):
    for p in sorted(root.rglob("*.html")):
        rel = p.relative_to(root).as_posix()
        if rel.split("/")[0] in SKIP_TOP:
            continue
        yield p, rel


def run(root: pathlib.Path = ROOT, write: bool = True) -> dict:
    existing = {p.relative_to(root).as_posix() for p in root.rglob("*") if p.is_file()}
    stats = {"pages": 0, "changed": 0, "missing_footer_targets": set()}
    for p, rel in targets(root):
        stats["pages"] += 1
        old = p.read_text(encoding="utf-8", errors="replace")
        new, missing = apply(old, rel, existing)
        stats["missing_footer_targets"].update(missing)
        if new != old:
            stats["changed"] += 1
            if write:
                p.write_text(new, encoding="utf-8")
    stats["missing_footer_targets"] = sorted(stats["missing_footer_targets"])
    return stats


if __name__ == "__main__":
    check = "--check" in sys.argv
    result = run(write=not check)
    print({k: v for k, v in result.items()})
    if check and result["changed"]:
        sys.exit(1)
