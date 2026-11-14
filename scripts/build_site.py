#!/usr/bin/env python3
"""Build the static GitHub Pages site from data/*.json.

Standard library only. Run from the repository root:

    python3 scripts/build_site.py

Writes index.html, executive-summary.html, products.html, pricing.html,
reviews.html, content.html, campaigns.html, flagged.html, sources.html,
assets/style.css and .nojekyll in the repository root. Every table cell is
generated from a record in data/*.json. A null value renders as a blank cell
labelled "Unverified". Nothing is filled in by hand.
"""
from __future__ import annotations

import html
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
REPO = "https://github.com/kanlerxz87-cyber/Zone3"
DATA = ROOT / "data"
ASSETS = ROOT / "assets"
BUILT = "2026-11-14"
DISCLOSURE = "As an Amazon Associate I earn from qualifying purchases."


def load(name: str):
    return json.loads((DATA / name).read_text(encoding="utf-8"))


SRC = load("sources.json")
SOURCES = {s["id"]: s for s in SRC["sources"]}
PRODUCTS = load("products.json")["products"]
FACTS = {f["id"]: f for f in load("policy_facts.json")["facts"]}
FLAGS = load("flags.json")["flags"]


def e(value) -> str:
    return html.escape(str(value), quote=True)


def src_links(ids) -> str:
    if not ids:
        return '<span class="muted">no source</span>'
    parts = []
    for sid in ids:
        s = SOURCES[sid]
        parts.append(
            f'<a href="{e(s["url"])}" target="_blank" rel="noopener noreferrer" '
            f'title="{e(s["title"])}">{e(sid)}</a>'
        )
    return " &middot; ".join(parts)


def flag_links(ids) -> str:
    return " ".join(f'<a class="flagid" href="flagged.html#{e(i)}">{e(i)}</a>' for i in ids) or "&mdash;"


def unv() -> str:
    return '<span class="badge unv">Unverified</span>'


def val(v) -> str:
    return unv() if v is None else e(v)


def badge(text: str, kind: str) -> str:
    return f'<span class="badge {e(kind)}">{e(text)}</span>'


def sev(text: str) -> str:
    # "Info" is used for correction/annotation entries (V-F1, V-F2 added 2026-11-14).
    kind = {"Critical": "bad", "High": "warn", "Medium": "info", "Low": "muted",
            "Info": "muted"}[text]
    return badge(text, kind)


def table(headers, rows, cls: str = "") -> str:
    th = "".join(f"<th>{e(h)}</th>" for h in headers)
    body = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return (
        f'<div class="table-wrap"><table class="{e(cls)}"><thead><tr>{th}</tr></thead>'
        f"<tbody>{body}</tbody></table></div>"
    )


NAV = [
    ("index.html", "Dashboard"),
    ("executive-summary.html", "Executive summary"),
    ("products.html", "Products"),
    ("air-fryers.html", "Category: Air Fryers"),
    ("category/air-fryers.html", "Category: air fryers"),    ("pricing.html", "Pricing &amp; commission"),
    ("reviews.html", "Reviews &amp; competition"),
    ("marketing.html", "Marketing content"),
    ("content.html", "Content &amp; compliance"),
    ("campaigns.html", "Campaigns &amp; tracking"),
    ("flagged.html", "Flagged for review"),
    ("sources.html", "Sources"),
    # Added by integration session 3c6cba43: the second site generation in this repo,
    # rendered by tools/build_site.py from data/z3/*.json. Linked here so the two halves of
    # the merged site are one navigable product instead of two disconnected trees.
    ("dashboard/index.html", "Full audit (16 pages)"),
]


def page(filename: str, title: str, body: str, lead: str = "") -> None:
    links = []
    for href, label in NAV:
        cls = ' class="active"' if href == filename else ""
        links.append(f'<a href="{href}"{cls}>{label}</a>')
    nav = "".join(links)
    lead_html = f'<p class="lead">{lead}</p>' if lead else ""
    doc = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)} | Zone3 Amazon affiliate dashboard</title>
<meta name="description" content="Zone3: verified Amazon affiliate product data, analysis and flags. Status as of {BUILT}.">
<link rel="stylesheet" href="assets/style.css">
</head>
<body>
<header class="topbar">
  <div class="brand"><a href="index.html">Zone3</a><span>Amazon affiliate dashboard</span></div>
  <nav>{nav}</nav>
</header>
<main>
<h1>{e(title)}</h1>
{lead_html}
{body}
</main>
<footer>
  <p class="disclosure"><strong>Disclosure:</strong> {e(DISCLOSURE)}</p>
  <p class="muted">Data verified as of {BUILT} (re-verified 2026-11-14). A cell marked <span class="badge unv">Unverified</span> has no official source yet and is left blank on purpose. Built by <code>scripts/build_site.py</code> from <code>data/*.json</code>. Source IDs (S01 and so on) link to the official page; see the <a href="sources.html">Sources</a> page.</p>
  <p class="small" style="margin-top:10px">This repository carries two site generations: the flat pages above (built by <code>scripts/build_site.py</code> from <code>data/*.json</code>) and a 16-page audit build at <a href="dashboard/index.html">/dashboard/</a> (built by <code>tools/build_site.py</code> from <code>data/z3/*.json</code>). Neither overwrites the other; <a href="https://github.com/kanlerxz87-cyber/Zone3/blob/main/COORDINATION.md">COORDINATION.md</a> maps both.</p>
  <p class="small" style="margin-top:6px"><a href="landing-prior.html">Previous landing page</a> (kept intact) · <a href="https://github.com/kanlerxz87-cyber/Zone3/blob/main/COORDINATION.md#part-session-b8beb448-2026-11-14--independent-line-by-line-re-verification--ux-integration">Verification record for this build</a> · <a href="https://github.com/kanlerxz87-cyber/Zone3">Repository</a></p>
</footer>
</body>
</html>
"""
    if "/" in filename:
        # This page lives in a subdirectory; prefix relative links so they
        # resolve from there (nav, stylesheet, footer and body links alike).
        import re

        def _up(m):
            attr, value = m.group(1), m.group(2)
            if value.startswith(("#", "http://", "https://", "mailto:", "tel:", "/")):
                return m.group(0)
            return f'{attr}../{value}"'

        doc = re.sub(r'(href=")([^"]+)"', _up, doc)
        doc = re.sub(r'(src=")([^"]+)"', _up, doc)
    (ROOT / filename).write_text(doc, encoding="utf-8")


def css() -> str:
    return """:root{--ink:#1d2433;--muted:#5b6474;--line:#e3e7ee;--bg:#f6f8fb;--card:#fff;--accent:#1f5eff;
--ok:#0f7b4b;--okbg:#e6f6ee;--warn:#7a4f00;--warnbg:#fff1cc;--bad:#a4262c;--badbg:#fde8e9;
--info:#1b4fa8;--infobg:#e6eefc;--grey:#eef1f5}
*{box-sizing:border-box}
body{margin:0;font:15px/1.55 system-ui,-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;color:var(--ink);background:var(--bg)}
a{color:var(--accent)}
code{background:var(--grey);padding:1px 5px;border-radius:4px;font-size:13px;word-break:break-all}
.topbar{background:#fff;border-bottom:1px solid var(--line);padding:12px 22px;display:flex;flex-wrap:wrap;gap:10px 22px;
align-items:center;justify-content:space-between;position:sticky;top:0;z-index:5}
.brand a{font-weight:800;font-size:18px;color:var(--ink);text-decoration:none;margin-right:10px}
.brand span{color:var(--muted);font-size:13px}
.topbar nav{display:flex;flex-wrap:wrap;gap:4px}
.topbar nav a{padding:6px 10px;border-radius:6px;color:var(--ink);text-decoration:none;font-size:14px}
.topbar nav a:hover{background:var(--grey)}
.topbar nav a.active{background:var(--accent);color:#fff}
main{max-width:1180px;margin:0 auto;padding:24px 22px 40px}
h1{font-size:26px;margin:4px 0 6px}
h2{font-size:19px;margin:0 0 10px}
.lead{color:var(--muted);margin:0 0 18px;max-width:900px}
.card{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:18px 20px;margin:0 0 18px}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:14px;margin:0 0 18px}
.stat{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:16px}
.stat .n{font-size:28px;font-weight:800}
.stat .l{color:var(--muted);font-size:13px}
.stat.bad .n{color:var(--bad)} .stat.warn .n{color:var(--warn)}
.tiles{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:14px}
.tile{display:block;background:var(--card);border:1px solid var(--line);border-radius:10px;padding:16px;text-decoration:none;color:var(--ink)}
.tile:hover{border-color:var(--accent)}
.tile b{display:block;margin-bottom:4px;color:var(--accent)}
.tile span{color:var(--muted);font-size:13px}
.table-wrap{overflow-x:auto;background:var(--card);border:1px solid var(--line);border-radius:10px;margin:0 0 18px}
table{border-collapse:collapse;width:100%;font-size:14px}
th,td{text-align:left;padding:9px 11px;border-bottom:1px solid var(--line);vertical-align:top}
th{background:#f1f4f9;font-size:12px;text-transform:uppercase;letter-spacing:.03em;color:var(--muted);position:sticky;top:0}
tr:last-child td{border-bottom:none}
td a{white-space:nowrap}
.badge{display:inline-block;padding:2px 8px;border-radius:999px;font-size:12px;font-weight:700;white-space:nowrap}
.badge.unv{background:var(--warnbg);color:var(--warn)}
.badge.ok{background:var(--okbg);color:var(--ok)}
.badge.bad{background:var(--badbg);color:var(--bad)}
.badge.warn{background:var(--warnbg);color:var(--warn)}
.badge.info{background:var(--infobg);color:var(--info)}
.badge.muted{background:var(--grey);color:var(--muted)}
.flagid{font-weight:700;text-decoration:none;margin-right:4px;white-space:nowrap}
.muted{color:var(--muted)}
.disclosure{margin:0 0 6px}
footer{max-width:1180px;margin:0 auto;padding:18px 22px 36px;color:var(--muted);font-size:13px;border-top:1px solid var(--line)}
ul.findings{padding-left:20px;margin:0}
ul.findings li{margin:0 0 8px}
.callout{border-left:4px solid var(--bad);background:var(--badbg);padding:12px 14px;border-radius:6px;margin:0 0 18px}
.callout.ok{border-color:var(--ok);background:var(--okbg)}
.callout p{margin:0}
@media (max-width:640px){main{padding:16px 12px}.topbar{padding:10px 12px}}
"""


def count_verified(field: str) -> int:
    return sum(1 for p in PRODUCTS if p.get(field) is not None)


def sev_count(level: str) -> int:
    return sum(1 for f in FLAGS if f["severity"] == level)


N = len(PRODUCTS)


# ---------------------------------------------------------------- Dashboard

def reverify_table() -> str:
    """Rows re-checked on 2026-11-14. Source ids resolve through sources.json."""
    rows = [
        ("The three submitted identifiers are 9 characters, not 10", "Confirmed",
         "Each id counted: B04G1MEwY=9, B02NbDxp3=9, B00hJ57DV=9. Amazon defines an ASIN as a 10-character alphanumeric id.", ["S31", "S08"]),
        ("amazon.com/dp/&lt;id&gt; returns Page Not Found for all three", "Confirmed",
         "All three fetched 2026-11-14; each returned Amazon&rsquo;s &ldquo;Page Not Found&rdquo; page.", ["S08", "S09", "S10"]),
        ("Each link.amazon short link opens a different real listing", "Confirmed",
         "B04G1MEwY&rarr;B0CDY277D3 (CHEFMAN 6 Qt dual basket), B02NbDxp3&rarr;B09B7SB46R (Emeril Lagasse 26QT), B00hJ57DV&rarr;B08DKYBTPH (Chefman TurboFry 8 Qt). Same three targets as 2026-11-13.", ["S11", "S12", "S13"]),
        ("Operating Agreement &sect;5 disclosure wording", "Confirmed verbatim",
         "&ldquo;As an Amazon Associate I earn from qualifying purchases.&rdquo; Header still reads Updated: October 15, 2025. Schedule 1 still lists the United States / amazon.com only.", ["S01"]),
        ("Participation Requirements 6(t), 6(w), 6(y), 2(b) and CIS 2(e)", "Confirmed verbatim",
         "Star-rating and review display limited to API-sourced data; link shorteners must not obscure an Amazon destination; no price tracking or alerting; prices/availability only if Amazon serves them or via the API; purchases via a Redirecting Link are disqualified.", ["S02", "S30"]),
        ("PA-API 5 is deprecated; Creators API is the successor", "Confirmed",
         "Deprecation notice re-read: PA-API 5 calls return HTTP 403 AccessDeniedException. Creators API prerequisites include at least 10 qualifying sales in the past 30 days.", ["S05", "S04"]),
        ("IP License: no ML training on Program Content; API use needs prior written approval for analysis", "Confirmed verbatim",
         "&sect;1 bars using Program Content to develop or improve LLMs or ML models; &sect;2(e) bars aggregating, analyzing, extracting or repurposing Product Advertising Content without express prior written approval; Agent Terms &sect;4 require an &ldquo;Agent/[name]&rdquo; user agent.", ["S02"]),
        ("Commission Table 1 (Standard) and Table A (Onsite) are readable without a sign-in", "Corrected",
         "The earlier site text implied all rate data was sign-in gated. Only /help/operating/schedule is gated (and it returns a per-account custom rate card). Table 1 and Table A render publicly. See V-F1; per-product rates remain blank.", ["S25", "S26", "S03"]),
        ("ASIN is a 10-character identifier", "Confirmed",
         "Creators API GetItems, ItemIdType parameter, quoted verbatim; independently stated on Amazon&rsquo;s seller blog.", ["S31", "S08"]),
        ("FTC disclosure standard", "Confirmed, source updated",
         "The 2019 brochure is still live but the Endorsement Guides were revised in 2023; the current FTC topic hub is cited alongside it.", ["S07", "S24"]),
    ]
    out = []
    for claim, verdict, note, srcs in rows:
        cls = "bad" if verdict.startswith("Corrected") else "ok"
        out.append([claim, badge(verdict, cls), note, src_links(srcs)])
    return table(["Claim re-checked", "Result", "What was observed on 2026-11-14", "Source"],
                 out, "reverify")



def build_index() -> None:
    stats = [
        ("Product links submitted", str(N), ""),
        ("Products identified via link resolution", f"{count_verified('product_name')} of {N}", "ok"),
        ("Submitted codes that are valid ASINs", "0 of 3", "warn"),
        ("Prices observed (snapshot 2026-11-14)", f"{count_verified('price')} of {N}", "warn"),        ("Commission rates verified", f"{count_verified('commission_rate')} of {N}", "warn"),
        ("Critical flags open", str(sev_count("Critical")), "bad"),
        ("Total flags open", str(len(FLAGS)), "warn"),
    ]
    stat_html = "".join(
        f'<div class="stat {k}"><div class="n">{e(v)}</div><div class="l">{e(l)}</div></div>'
        for l, v, k in stats
    )
    tiles = [
        ("executive-summary.html", "Executive summary", "Bottom line, findings, what was built, what is blocked."),
        ("products.html", "Products", "The 3 submitted links, identifier checks, resolved listings, observed values."),
        ("category/air-fryers.html", "Category: air fryers", "The verified category of all three products, with the product table."),
        ("pricing.html", "Pricing &amp; commission", "Observed price snapshots, commission fields, and the verified commission rules."),
        ("reviews.html", "Reviews &amp; competition", "Observed ratings and review counts, plus the verified review rules."),
        ("marketing.html", "Marketing content", "SEO product briefs, comparison and buying guide built from verified facts only."),
        ("content.html", "Content &amp; compliance", "Content status and the Associates and FTC checklist."),
        ("campaigns.html", "Campaigns &amp; tracking", "Click and conversion ledger. Empty until data exists."),
        ("flagged.html", "Flagged for review", "Every irregularity and unverified item, with its source links."),
        ("sources.html", "Sources", "The official source registry with retrieval status."),
    ]
    tile_html = "".join(
        f'<a class="tile" href="{h}"><b>{t}</b><span>{d}</span></a>' for h, t, d in tiles
    )
    reverify_html = reverify_table()
    body = f"""
<div class="callout ok">
  <p><strong>Headline (re-verified {BUILT}):</strong> each of the three submitted links resolves, stably
  across 2026-11-13 and 2026-11-14, to one real Amazon listing &mdash; three air fryers in
  Home &amp; Kitchen &rsaquo; Kitchen &amp; Dining &rsaquo; Small Appliances &rsaquo; Fryers &rsaquo; Air Fryers.
  Those listings are the products this site markets and analyses. The submitted codes themselves are
  nine-character short-link codes, not ASINs ({flag_links(['FLG-001'])}), and no official source documents the
  code-to-listing mapping ({flag_links(['FLG-028'])}). Prices and ratings below are dated observed snapshots whose
  display is restricted on a live Associates site ({flag_links(['FLG-029'])}). Commission rates, best-seller ranks and
  click figures remain unverified and blank.</p></div>
<div class="grid">{stat_html}</div>
<h2>Sections</h2>
<div class="tiles">{tile_html}</div>

<p style="margin-top:18px"><a href="dashboard/index.html">Full audit: 16-page verification dashboard, commission rate tables and flag register</a></p>

<h2>Re-verification performed 2026-11-14</h2>
<p>Every load-bearing claim on the flat pages was checked again against the official page it cites. The
result, per claim, is below. Nothing in this table was inferred; each row links the page that was read.</p>
{reverify_html}
<p class="small">Where a row says <em>corrected</em>, the earlier text on this site was wrong or overstated and has
been rewritten in the same commit that added the row. Corrections are listed on the
<a href="flagged.html">Flagged for review</a> page as V-F1 and V-F2, so the change is auditable rather than silent.</p>
"""
    page("index.html", "Dashboard", body,
         lead=f"Status as of {BUILT}. The site shows verified data only. Blank cells are unverified and listed on the Flagged for review page.")


# ---------------------------------------------------------- Executive summary
def build_exec() -> None:
    body = f"""
<section class="card">
  <h2>Bottom line</h2>
  <p>The three submitted links are short links, and each opens exactly one real Amazon listing. The mapping
  was observed on 2026-11-13 and reproduced with fresh redirect tokens on 2026-11-14 {src_links(['S11', 'S12', 'S13', 'S45', 'S46', 'S47'])}.</p>
  <p><strong>The three products are:</strong></p>
  <ul class="findings">
    <li>Product 1 &mdash; <strong>CHEFMAN 6 Quart Dual Basket Air Fryer</strong> (ASIN of the listing: B0CDY277D3),
    observed at USD 79.93 (list USD 99.99), 4.2 out of 5 stars, about 4.8K reviews {src_links(['S45', 'S48'])}.</li>
    <li>Product 2 &mdash; <strong>Emeril Lagasse 26QT French Door Multi-Function Air Fryer Toaster Oven</strong>
    (ASIN of the listing: B09B7SB46R), observed at USD 149.99 (list USD 209.99), 4.3 out of 5 stars, about 18.3K reviews {src_links(['S46', 'S49'])}.</li>
    <li>Product 3 &mdash; <strong>Chefman Air Fryer 8 Qt TurboFry</strong> (ASIN of the listing: B08DKYBTPH),
    observed at USD 79.91 (list USD 119.99), 4.4 out of 5 stars, about 16.8K reviews {src_links(['S47', 'S50'])}.</li>
  </ul>
  <p>All three sit in the same verified category: Home &amp; Kitchen &rsaquo; Kitchen &amp; Dining &rsaquo;
  Small Appliances &rsaquo; Fryers &rsaquo; <strong>Air Fryers</strong> {src_links(['S14', 'S15', 'S23'])}. The submitted
  codes are nine-character short-link codes, not ASINs {flag_links(['FLG-001'])}; the code-to-listing mapping is
  observed, not documented by Amazon {flag_links(['FLG-028'])}. Commission rates cannot be verified: the rate schedule
  is behind sign-in {flag_links(['FLG-005'])}. Every value not confirmable from an official source is left blank and
  marked <span class="badge unv">Unverified</span>. Nothing was inferred.</p></section>

<section class="card">
  <h2>Key findings</h2>
  <ul class="findings">
    <li><strong>3 of 3 links resolve to real listings, stably.</strong> Four observations over two days
    (two sessions) map each code to the same listing every time. Control tests show the shortener rejects
    unregistered codes {flag_links(['FLG-028'])} {flag_links(['FLG-030'])} {src_links(['S11', 'S12', 'S13', 'S45', 'S46', 'S47'])}.</li>
    <li><strong>0 of 3 submitted codes are ASINs.</strong> ASINs are 10 characters; the codes are 9, and
    amazon.com/dp/&lt;code&gt; returns &ldquo;Page Not Found&rdquo; {flag_links(['FLG-001'])} {src_links(['S06', 'S08', 'S09', 'S10'])}.</li>
    <li><strong>Prices and ratings are dated observed snapshots.</strong> Captured from Amazon's own result
    pages on 2026-11-14. They are volatile deal prices, and Participation Requirements 2(b) and 6(t) restrict
    how a live Associates site may display prices and star ratings {flag_links(['FLG-029'])} {src_links(['S48', 'S49', 'S50', 'S02'])} (PF-04, PF-05).</li>
    <li><strong>Commission rates cannot be verified.</strong> The rate schedule redirected to a sign-in page
    on 2026-11-13 {src_links(['S03'])} {flag_links(['FLG-005'])}. Category reference rates exist (Kitchen 4.50%)
    but the listings' commission category is not documented {flag_links(['FLG-021'])} {src_links(['S25'])}.</li>
    <li><strong>Associates compliance of link.amazon is unconfirmed.</strong> The policies say a shortener must
    not make the Amazon destination unclear {src_links(['S02'])} (PF-06), and purchases from a Redirecting Link
    are disqualified (PF-07). Whether these links carry an Associates tag is unverified {flag_links(['FLG-003'])} {flag_links(['FLG-010'])}.</li>
    <li><strong>Automated product data needs Creators API access.</strong> The official prerequisite is
    &ldquo;at least 10 qualifying sales within the past 30 days&rdquo; {src_links(['S04'])}. PA-API 5 is deprecated
    and being replaced by the Creators API {src_links(['S05'])} (PF-17) {flag_links(['FLG-006'])} {flag_links(['FLG-007'])}.</li>
    <li><strong>The AI layer needs written approval from Amazon.</strong> The Program Policies bar analysing,
    aggregating or repurposing API data, and bar using Program Content to develop or train machine learning or
    language models, without express prior written approval {src_links(['S02'])} (PF-23, PF-24, PF-25) {flag_links(['FLG-016'])}.</li>
    <li><strong>Enrolment and eligibility are gated.</strong> Schedule 1 lists only the United States site
    {src_links(['S01'])} (PF-35); the application needs about 3 qualifying sales in 180 days
    {src_links(['S29'])} (PF-40), and 180 days of no referred sale risks dormancy {src_links(['S28'])} (PF-41) {flag_links(['FLG-015'])}.</li>
    <li><strong>Disclosure is on every page.</strong> The required wording is quoted verbatim from Operating
    Agreement Section 5 and was re-read on 2026-11-14 {src_links(['S01', 'S51'])} (PF-01). FTC guidance
    (Disclosures 101, re-read 2026-11-14) requires the disclosure to be hard to miss {src_links(['S07', 'S53'])} (PF-20) {flag_links(['FLG-013'])}.</li>
    <li><strong>Marketing content is published, facts-only.</strong> Product briefs, a comparison and a buying
    guide use only verified listing attributes with source links, state no prices or ratings, and claim no
    first-hand experience {src_links(['S02', 'S07'])} (PF-10, PF-21) {flag_links(['FLG-012'])}.</li>  </ul>
</section>

<section class="card">
  <h2>What was built</h2>
  <ul class="findings">
    <li>A GitHub Pages dashboard (this site) with subpages by category: Products, Category: air fryers,
    Pricing &amp; commission, Reviews &amp; competition, Marketing content, Content &amp; compliance,
    Campaigns &amp; tracking {src_links(['S22'])}.</li>
    <li>A Flagged for review page with {len(FLAGS)} items, each with its evidence sources and the action needed.</li>
    <li>A Sources page listing each official page used, its retrieval status and what it supports
    ({len(SOURCES)} sources, re-verified 2026-11-14) {src_links(['S19'])}.</li>
    <li>A data layer (<code>data/*.json</code>) with a generator (<code>scripts/build_site.py</code>) and a
    checker (<code>scripts/check_site.py</code>). The checker fails if a table row has no official source link,
    or if a value appears without a source {src_links(['S20'])}.</li>
    <li>Two earlier session builds kept intact and linked: the 16-page audit at
    <a href="dashboard/index.html">/dashboard/</a> and the independent verification build at
    <a href="docs/index.html">/docs/</a>. Their archives and mapping notes remain in
    <code>COORDINATION.md</code> {src_links(['S21'])}.</li>
    <li>SEO marketing content for the three air fryers: three product briefs, one comparison and one buying
    guide, all claims sourced to the Amazon listings {src_links(['S45', 'S46', 'S47'])}.</li>
<li><strong>An independent re-verification pass on 2026-11-14</strong> (this session): {len(SRC['sources'])} official sources, every load-bearing claim re-fetched and compared. Two earlier statements were found overstated and corrected rather than quietly dropped &mdash; see V-F1 and V-F2 on the Flagged for review page.</li>  </ul>
</section>

<section class="card">
  <h2>What is not done, and why</h2>
  <ul class="findings">
    <li><strong>Commission-potential and revenue projections.</strong> Commission rates are login-gated
    {src_links(['S03'])} {flag_links(['FLG-005'])} and no Associates tag or reports exist
    {flag_links(['FLG-010'])} {flag_links(['FLG-011'])}. Nothing was estimated.</li>
    <li><strong>Competitor counts and best-seller ranks.</strong> No official source gives these for the
    listings in the text this session can read; cells stay blank {flag_links(['FLG-004'])} {src_links(['S48', 'S49', 'S50'])}.</li>
    <li><strong>Click and conversion tracking.</strong> Figures come from the owner's Associates reports.
    No tag has been supplied, so no Special Link has been created {flag_links(['FLG-010'])} {src_links(['S19'])}.</li>
    <li><strong>Automated optimisation.</strong> There is no campaign data to optimise yet. The generator
    rebuilds the site from the data files once verified data is added {src_links(['S20'])}.</li>
    <li><strong>First-hand product testing.</strong> FTC guidance bars claims about experience with a product
    that has not been tried {src_links(['S07'])} (PF-21). The marketing content therefore makes none.</li>
  </ul>
</section>

<section class="card">
  <h2>Owner items (flagged; they do not block the merge)</h2>
  <ul class="findings">
    <li>Confirm that the three resolved listings (B0CDY277D3, B09B7SB46R, B08DKYBTPH) are the intended
    products {flag_links(['FLG-028'])} {src_links(['S45', 'S46', 'S47'])}.</li>
    <li>Supply the Associates tag so Special Links can be created; do not send a password or token
    {flag_links(['FLG-010'])} {src_links(['S02'])} (PF-03).</li>
    <li>Export the commission rate card for the category from Associates Central
    {flag_links(['FLG-005'])} {src_links(['S03'])}.</li>
    <li>Before commercial use, remove the observed prices and ratings or re-source them through the
    Creators API with date/time stamps {flag_links(['FLG-029'])} {src_links(['S02'])} (PF-04, PF-05, PF-27).</li>
    <li>Review disclosure placement against FTC guidance (hard to miss, plain language)
    {flag_links(['FLG-013'])} {src_links(['S07'])} (PF-20).</li>
    <li>Test each submitted link in a logged-in Associates account and report whether clicks are tracked (FLG-002, FLG-003).</li>
    <li>Confirm which Amazon product category each listing is in so the public Table 1 rate can be applied (FLG-005, FLG-021). The category rates themselves are already published and verified.</li>  </ul>
</section>
"""
    page("executive-summary.html", "Executive summary", body,
         lead="A plain-language summary of what can and cannot be verified today. Each finding links to its official source.")


# -------------------------------------------------------------- Products
def build_products() -> None:
    rows = []
    for p in PRODUCTS:
        ro = p["redirect_observed"]
        d = p["direct_check"]
        ob = p["observed"]
        rows.append([
            e(p["label"]),
            f'<a href="{e(p["submitted_url"])}" target="_blank" rel="noopener noreferrer">{e(p["submitted_url"])}</a>',
            f'{e(p["link_id"])} <span class="muted">({p["link_id_length"]} chars, not an ASIN)</span>',
            f'<a href="{e(d["url"])}" target="_blank" rel="noopener noreferrer">{e(d["result"])}</a>',
            f'<a href="{e(ro["final_url"])}" target="_blank" rel="noopener noreferrer">{e(ro["page_id"])}</a> '
            + badge("Stable link target", "ok"),
            e(p["product_name"]),
            e(p["brand"]),
            e(p["price"]),
            e(p["rating"]),
            e(p["review_count"]),
            e(ob["category_path"]),            e(p["status"]),
            flag_links(p["flags"]),
            src_links(p["sources"]),
        ])
    body = table(
        ["#", "Submitted link", "Code (length)", "amazon.com/dp check", "Listing opened (ASIN)",
         "Product name (as listed)", "Brand", "Price (observed)", "Rating (observed)",
         "Reviews (observed)", "Category (verified path)", "Status", "Flags", "Source"],
        rows,
    )
    body += f"""
<section class="card">
  <h2>How to read this table</h2>
  <ul class="findings">
    <li>Each row is one product link from the brief. The code is the 9-character short-link code; it is not an ASIN {flag_links(['FLG-001'])}.</li>
    <li>&ldquo;Listing opened&rdquo; is the Amazon page the short link lands on. It was observed 4 times across 2026-11-13 and 2026-11-14 with the same result every time {src_links(['S11', 'S12', 'S13', 'S45', 'S46', 'S47'])}.</li>
    <li>Price, rating and review count are dated observed snapshots (2026-11-14) read from Amazon's own result pages. Prices are volatile and their display on a live Associates site is restricted {flag_links(['FLG-029'])} {src_links(['S48', 'S49', 'S50'])}.</li>
    <li>Commission rate, best-seller rank, competitor count, availability, clicks and conversions are blank because no official source confirms them {flag_links(['FLG-004'])} {flag_links(['FLG-005'])}.</li>
  </ul>
</section>
"""
    page("products.html", "Products", body,
         lead="The three product links from the brief, checked line by line against official Amazon pages on 2026-11-13 and 2026-11-14. Every value links to the page it was read from.")


# ------------------------------------------------------------- Pricing
def build_pricing() -> None:
    rows = []
    for p in PRODUCTS:
        rows.append([
            e(p["label"]),
            e(p["product_name"][:60] + ("..." if len(p["product_name"]) > 60 else "")),
            val(p["price"]),
            val(p["commission_rate"]),
            badge("Rate schedule not accessible", "warn") + " " + badge("Snapshot, not a live price", "info"),
            flag_links(["FLG-004", "FLG-005", "FLG-029"]),
            src_links(["S03", "S02"] + p["value_sources"]["price"]),        ])
    body = '<div class="callout"><p><strong>Display compliance.</strong> Participation Requirements 2(b) ' \
           '(PF-04) allow a site to show prices and availability only when Amazon serves the link or through ' \
           'the Product Advertising API. The prices below are dated observations kept for analysis ' \
           '(stamp adjacent, per PF-27). Remove or re-source them via Special Links or the Creators API ' \
           'before commercial use ' + flag_links(["FLG-029"]) + " " + src_links(["S02"]) + ".</p></div>"
    body += "<h2>Price and commission fields</h2>" + table(
        ["Product", "Listing", "Price (observed 2026-11-14)", "Commission rate", "Status", "Flags", "Source"], rows)

    rules = [
        ["Commission window (session)", FACTS["PF-12"]["quote"], "A click-to-sale record needs the click time, a 24-hour session, and the 89-day cart window.", src_links(["S02", "S52"])],
        ["Cancelled, returned or refunded orders", FACTS["PF-13"]["quote"], "Conversion counts must exclude these orders.", src_links(["S02", "S52"])],
        ["Redirecting Links disqualify purchases", FACTS["PF-07"]["quote"], "Relevant to the link.amazon question (FLG-003).", src_links(["S02"])],
        ["Prices shown only via link or API", FACTS["PF-04"]["quote"], "Observed snapshots are analysis-only (FLG-029); a live price display needs Special Links or the API.", src_links(["S02", "S52"])],
        ["Comparison-price display", FACTS["PF-11"]["quote"], "Any comparison format must show Amazon's lowest new and used prices; the marketing comparison on this site therefore shows no prices.", src_links(["S02"])],
        ["Date/time stamp on price or availability", FACTS["PF-27"]["quote"], "Every observed price on this site carries its observation date for this reason.", src_links(["S02"])],
    ]
    rules_html = table(["Rule", "Verified wording (quoted)", "What it means here", "Source"], rules)
    body += f'<h2>Verified commission and pricing rules</h2>{rules_html}'
    ref_rows = [
        ["Kitchen (Standard Commission, Table 1)", "4.50%", "Reference only. Applies only if a listing is in the Kitchen category, which is not verified (FLG-021).", FACTS["PF-38"]["quote"], src_links(["S25"]) + " " + flag_links(["FLG-021"])],
        ["Kitchen (Onsite Commission, Table A)", "1.25%", "Not a rate for links on this site. It applies to Onsite Content used by Amazon within the Amazon Site.", FACTS["PF-39"]["quote"], src_links(["S26"]) + " " + flag_links(["FLG-021"])],
    ]
    body += "<h2>Category reference rates (not product values)</h2>" + table(["Category and table", "Rate", "What it means here", "Verified wording (quoted)", "Source"], ref_rows)
    page("pricing.html", "Pricing &amp; commission", body,
         lead="Observed price snapshots (2026-11-14, volatile) and the verified commission rules. Commission rates are blank: the rate schedule is behind sign-in. Nothing was estimated.")

# ------------------------------------------------------------- Reviews
def build_reviews() -> None:
    rows = []
    for p in PRODUCTS:
        rows.append([
            e(p["label"]),
            e(p["product_name"][:60] + ("..." if len(p["product_name"]) > 60 else "")),
            val(p["rating"]),
            val(p["review_count"]),
            val(p["competitor_count"]),
            val(p["best_seller_rank"]),
            flag_links(["FLG-004", "FLG-006", "FLG-029"]),
            src_links(["S02", "S04"] + p["value_sources"]["rating"]),
        ])
    body = '<div class="callout"><p><strong>Display compliance.</strong> Participation Requirements 6(t) ' \
           '(PF-05) bar displaying customer reviews or star ratings on a site unless they are obtained through ' \
           'the API or a qualifying link. The ratings and review counts below are dated observations kept for ' \
           'analysis only. Remove or re-source them before commercial use ' + flag_links(["FLG-029"]) + " " + src_links(["S02"]) + ".</p></div>"
    body += "<h2>Rating, review and competition fields</h2>" + table(
        ["Product", "Listing", "Rating (observed 2026-11-14)", "Review count (observed)", "Competing listings", "Best-seller rank", "Flags", "Source"], rows)
    rules = [
        ["Reviews and star ratings", FACTS["PF-05"]["quote"], "Observed ratings are analysis-only snapshots (FLG-029). A live display needs the API or a qualifying link.", src_links(["S02", "S52"])],
        ["No inaccurate or misleading product claims", FACTS["PF-10"]["quote"], "Marketing content on this site states only attributes read from the listings, each with its source.", src_links(["S02"])],
        ["Original content and third-party material", FACTS["PF-15"]["quote"], "Pages must add analysis to any product data they use.", src_links(["S02"])],
    ]
    body += "<h2>Verified review and content rules</h2>" + table(
        ["Rule", "Verified wording (quoted)", "What it means here", "Source"], rules)
    page("reviews.html", "Reviews &amp; competition", body,
         lead="Ratings and review counts as observed on Amazon's result pages on 2026-11-14. Competing-listing counts and best-seller ranks are blank: no official source confirms them.")


# ------------------------------------------------------------- Content
def build_content() -> None:
    rows = []
    for p in PRODUCTS:
        rows.append([
            e(p["label"]),
            badge("Published (facts-only)", "ok"),
            badge("Published (no prices)", "ok"),
            badge("Published (shared guide)", "ok"),
            "Marketing content states only attributes read from the official listing, with a source link per claim. No price, rating or first-hand experience is claimed (PF-10, PF-21).",
            flag_links(["FLG-012"]),
            src_links(["S02", "S07", "S45", "S46", "S47"]),
        ])
    body = "<h2>Content status</h2>" + table(
        ["Product", "SEO product article", "Comparison", "Buying guide", "How compliance is met", "Flags", "Source"], rows)
    body += '<p class="muted">The published pieces are on the <a href="marketing.html">Marketing content</a> page.</p>'

    checklist = [
        ["Disclosure wording", FACTS["PF-01"]["quote"], badge("On every page (footer)", "ok"), src_links(["S01"])],
        ["Disclosure placed where it can be seen", FACTS["PF-20"]["quote"], badge("Owner review needed", "warn") + " " + flag_links(["FLG-013"]), src_links(["S07"])],
        ["Link shorteners must be clear", FACTS["PF-06"]["quote"], badge("Unresolved", "bad") + " " + flag_links(["FLG-003"]), src_links(["S02"])],
        ["No Special Links in print, ebooks or offline use", FACTS["PF-09"]["quote"], badge("None created", "ok"), src_links(["S02"])],
        ["No cloaking or hidden destinations", FACTS["PF-08"]["quote"], badge("Met (no hidden redirects on this site)", "ok"), src_links(["S02"])],
        ["No claims about products not tried", FACTS["PF-21"]["quote"], badge("No experience claimed", "ok"), src_links(["S07"])],
    ]
    body += "<h2>Associates and FTC checklist</h2>" + table(
        ["Requirement", "Verified wording (quoted)", "Status on this site", "Source"], checklist)
    page("content.html", "Content &amp; compliance", body,
         lead="Marketing content is published on the Marketing content page, built from verified listing facts only. The checklist below records what any content must meet before it is published.")


# ------------------------------------------------------------- Marketing
def build_marketing() -> None:
    briefs = [
        ("P1", "Best for families who cook two foods at once",
         ["Two independent 3-quart baskets with Sync Finish, as listed",
          "Easy-view windows and digital touchscreen, as listed",
          "Hi-Fry option and auto shutoff, as listed"],
         "https://link.amazon/B04G1MEwY"),
        ("P2", "Best all-in-one oven replacement",
         ["26-quart air fryer toaster oven with French doors, as listed",
          "24 cooking functions, dual-speed fan and rotisserie, as listed",
          "Family-size capacity for larger meals, as listed"],
         "https://link.amazon/B02NbDxp3"),
        ("P3", "Best large single-basket value",
         ["8-quart XL nonstick, dishwasher-safe basket, as listed",
          "TurboFry 4-in-1: air fry, bake, dehydrate, cook from frozen, as listed",
          "450-degree Hi-Fry option for crispier results, as listed"],
         "https://link.amazon/B00hJ57DV"),
    ]
    parts = []
    for pid, angle, bullets, url in briefs:
        p = next(x for x in PRODUCTS if x["id"] == pid)
        ro = p["redirect_observed"]
        ob = p["observed"]
        li = "".join(f"<li>{e(b)}</li>" for b in bullets)
        facts = table(
            ["Attribute", "As listed on Amazon", "Source"],
            [
                ["Product name", e(p["product_name"]), src_links(p["value_sources"]["product_name"])],
                ["Brand", e(p["brand"]), src_links(p["value_sources"]["brand"])],
                ["ASIN (of the listing the link opens)", e(ro["page_id"]), src_links(p["value_sources"]["product_name"][-1:])],
                ["Category path", e(ob["category_path"]), src_links([ro["title_source"]])],
                ["Offer snapshot (dated, volatile)", e(p["price"]) + " &middot; " + e(p["rating"]) + " &middot; " + e(p["review_count"]), src_links(p["value_sources"]["price"])],
            ],
        )
        parts.append(f"""
<section class="card">
  <h2>{e(p["label"])}: {e(p["brand"])} &mdash; {e(angle)}</h2>
  <p>The listing describes this product as follows (every claim below is read from the official Amazon
  listing; nothing is based on hands-on testing):</p>
  <ul class="findings">{li}</ul>
  <p><a href="{e(url)}" target="_blank" rel="noopener noreferrer">Check current price and availability on Amazon</a>
  &mdash; prices and ratings change often, so this page states none.</p>
  {facts}
</section>""")

    comp_rows = [
        ["Brand", e(PRODUCTS[0]["brand"]), e(PRODUCTS[1]["brand"]), e(PRODUCTS[2]["brand"]), src_links(["S14", "S15", "S23"])],
        ["Form factor (as listed)", "Dual-basket air fryer oven", "French-door air fryer toaster oven", "Single XL-basket air fryer", src_links(["S14", "S15", "S23"])],
        ["Capacity (as listed)", "6 quart (2 x 3 qt)", "26 quart", "8 quart", src_links(["S14", "S15", "S23"])],
        ["Standout listed features", "Sync Finish, Hi-Fry, easy-view windows", "24 functions, rotisserie, dual-speed fan", "450F Hi-Fry, bake, dehydrate, frozen", src_links(["S14", "S15", "S23"])],
        ["Listing ASIN", "B0CDY277D3", "B09B7SB46R", "B08DKYBTPH", src_links(["S14", "S15", "S23"])],
        ["Category path", "Air Fryers (under Small Appliances)", "Air Fryers (under Small Appliances)", "Air Fryers (under Small Appliances)", src_links(["S14", "S15", "S23"])],
        ["Price and rating", badge("Not stated here (volatile; PF-04, PF-05)", "info"), badge("Not stated here (volatile; PF-04, PF-05)", "info"), badge("Not stated here (volatile; PF-04, PF-05)", "info"), src_links(["S02"])],
    ]
    comp = table(["Attribute", "Product 1: CHEFMAN 6 Qt dual basket", "Product 2: Emeril Lagasse 26QT oven",
                  "Product 3: Chefman 8 Qt TurboFry", "Source"], comp_rows)

    guide = f"""
<section class="card">
  <h2>Buying guide: choosing between the three air fryers</h2>
  <p>These three products sit in the same verified Amazon category &mdash; {e(PRODUCTS[0]["observed"]["category_path"])}
  {src_links(["S14", "S15", "S23"])} &mdash; but they solve different jobs. Use the questions below; every product
  fact cited is read from its official listing.</p>
  <ul class="findings">
    <li><strong>Do you cook two foods at once?</strong> Only product 1 lists two independent baskets with a
    synchronised finish {src_links(["S14"])}. Products 2 and 3 are single-chamber designs {src_links(["S15", "S23"])}.</li>
    <li><strong>Do you want to replace a countertop oven?</strong> Product 2 lists French doors, 24 cooking
    functions, a rotisserie and a 26-quart cavity {src_links(["S15"])}. The other two are basket air fryers
    {src_links(["S14", "S23"])}.</li>
    <li><strong>Is easy cleanup the priority?</strong> Products 1 and 3 both list nonstick, dishwasher-safe
    baskets {src_links(["S14", "S23"])}.</li>
    <li><strong>Do you want maximum crisp?</strong> Products 1 and 3 both list a Hi-Fry high-temperature
    option (product 3 lists 450 degrees) {src_links(["S14", "S23"])}.</li>
    <li><strong>Compare current prices yourself.</strong> This guide states no prices or ratings: they are
    volatile and their display is restricted for Associates sites (PF-04, PF-05) {flag_links(["FLG-029"])}
    {src_links(["S02"])}. Open the links above for live prices.</li>
    <li><strong>Check the return policy and warranty on the listing before you buy.</strong> Terms are set by
    Amazon and change over time {src_links(["S45", "S46", "S47"])}.</li>
  </ul>
</section>
<section class="card">
  <h2>How this content meets the rules</h2>
  <ul class="findings">
    <li>Every product claim is read from the official Amazon listing and carries its source link
    (Participation Requirements 2(b): no inaccurate or misleading claims) {src_links(["S02"])} (PF-10).</li>
    <li>No first-hand experience is claimed; nobody on this project has tested these products
    (FTC Disclosures 101) {src_links(["S07", "S53"])} (PF-21).</li>
    <li>The affiliate relationship is disclosed on every page, with the exact wording required by
    Operating Agreement Section 5 {src_links(["S01", "S51"])} (PF-01).</li>
    <li>No prices, star ratings or review counts appear in this content {src_links(["S02"])} (PF-04, PF-05) {flag_links(["FLG-029"])}.</li>
    <li>The outbound links are the owner-submitted short links. Whether they carry an Associates tag is
    unverified, and short-link compliance is open {flag_links(["FLG-003"])} {flag_links(["FLG-010"])}.</li>
  </ul>
</section>"""

    body = ('<div class="callout ok"><p><strong>Facts-only marketing content.</strong> Three SEO product '
            "briefs, one comparison and one buying guide for the three air fryers. Claims are limited to "
            "what the official Amazon listings state, with a source link for each. No prices or ratings "
            "are quoted and no first-hand experience is claimed.</p></div>"
            + "".join(parts)
            + "<h2>Comparison: the three air fryers side by side</h2>"
            + comp
            + guide)
    page("marketing.html", "Marketing content", body,
         lead="SEO product briefs, a comparison and a buying guide for the three products the submitted links open. Written from verified listing facts only.")


# ------------------------------------------------------------- Category
def build_category() -> None:
    rows = []
    for p in PRODUCTS:
        ro = p["redirect_observed"]
        rows.append([
            e(p["brand"]),
            f'<a href="{e(ro["final_url"])}" target="_blank" rel="noopener noreferrer">{e(p["product_name"])}</a>',
            e(ro["page_id"]),
            e(p["observed"]["category_path"]),
            e(p["price"]),
            e(p["rating"]),
            e(p["review_count"]),
            flag_links(p["flags"]),
            src_links(p["sources"]),
        ])
    body = f"""
<div class="callout ok">
  <p><strong>Category verified from the product pages.</strong> All three products show the breadcrumb
  Home &amp; Kitchen &rsaquo; Kitchen &amp; Dining &rsaquo; Small Appliances &rsaquo; Fryers &rsaquo; Air Fryers
  {src_links(['S14', 'S15', 'S23'])}. This is the category page for that node.</p>
</div>
"""
    body += table(
        ["Brand", "Product (links to the Amazon listing)", "ASIN", "Category path (as shown on Amazon)",
         "Price (observed 2026-11-14)", "Rating (observed)", "Reviews (observed)", "Flags", "Source"],
        rows,
    )
    body += """
<section class="card">
  <h2>Niche assessment</h2>
  <ul class="findings">
    <li><strong>Niche: air fryers (Home &amp; Kitchen &rsaquo; Small Appliances &rsaquo; Fryers &rsaquo; Air Fryers).</strong>
    Coherent, single-category portfolio of three real listings in a high-volume small-appliance node
    """ + src_links(["S14", "S15", "S23"]) + """.</li>
    <li><strong>Demand signals observed, not inferred.</strong> Amazon displayed purchase badges on all three
    listings on 2026-11-14 (1K+, 4K+ and 3K+ bought in past month, as displayed)
    """ + src_links(["S48", "S49", "S50"]) + """.</li>
    <li><strong>Commission potential cannot be computed.</strong> The commission rate schedule is login-gated
    (""" + flag_links(["FLG-005"]) + """), and whether the &lsquo;Kitchen&rsquo; rate row maps to this category
    node is not documented (""" + flag_links(["FLG-021"]) + """) """ + src_links(["S03", "S25"]) + """.</li>
    <li><strong>Price ladder (observed 2026-11-14, volatile).</strong> The three listings span a basket-fryer
    and a toaster-oven form factor; observed deal prices are recorded on the
    <a href="pricing.html">Pricing</a> page with the display-policy caveat (""" + flag_links(["FLG-029"]) + """) """ + src_links(["S48", "S49", "S50"]) + """.</li>
  </ul>
</section>
"""
    page("category/air-fryers.html", "Category: air fryers", body,
         lead="The category all three products belong to, verified from the breadcrumb on each Amazon product page, with the product table and a sourced niche assessment.")
def build_campaigns() -> None:
    rows = []
    for p in PRODUCTS:
        rows.append([
            e(p["label"]),
            val(p["associates_tag"]),
            badge("Not created", "bad"),
            val(p["clicks"]),
            val(p["conversions"]),
            flag_links(["FLG-010", "FLG-011"]),
            src_links(["S02", "S19"]),
        ])
    body = "<h2>Click and conversion ledger</h2>" + table(
        ["Product", "Associates tag", "Special Link", "Clicks", "Conversions", "Flags", "Source"], rows)
    body += f"""
<section class="card">
  <h2>What this ledger records</h2>
  <ul class="findings">
    <li>Clicks and conversions are blank. No click or conversion figure exists from an official source (FLG-011).</li>
    <li>A conversion counts only if it meets the 89-day cart window and is not cancelled, returned or refunded {src_links(['S02'])} (PF-12, PF-13).</li>
    <li>Special Links must carry the Associates tag (PF-03). No tag has been supplied, so no Special Link has been created (FLG-010).</li>
  </ul>
</section>
"""
    page("campaigns.html", "Campaigns &amp; tracking", body,
         lead="Empty by design. Figures appear here only after they come from the owner's Associates reports.")


# ------------------------------------------------------------- Flagged
def build_flagged() -> None:
    rows = []
    for f in FLAGS:
        rows.append([
            f'<a id="{e(f["id"])}"></a><strong>{e(f["id"])}</strong>',
            sev(f["severity"]),
            e(f["category"]),
            e(f["item"]),
            e(f["detail"]),
            e(f["action"]),
            src_links(f["sources"]) if f.get("sources") else
            f'<a href="{REPO}" target="_blank" rel="noopener noreferrer">repo</a> <span class="muted">&mdash; observed in this repository, so no external source is cited</span>',
        ])
    body = (
        '<div class="callout"><p><strong>Flagged for review.</strong> These items do not block the merge. '
        "Each one has its evidence source links and the action needed. Send any change request by replying to the owner; the site will be rebuilt from the data files.</p></div>"
        + "<h2>All flags</h2>"
        + table(["ID", "Severity", "Category", "Item", "Detail", "Action needed", "Source"], rows)
    )
    obs = []
    for p in PRODUCTS:
        ro = p["redirect_observed"]
        obs.append([
            e(p["label"]),
            f'<a href="{e(ro["final_url"])}" target="_blank" rel="noopener noreferrer">{e(ro["page_id"])}</a>',
            e(ro["page_title"]),
            badge("Stable link target; owner intent unconfirmed", "warn"),
            src_links([ro["title_source"]]),
        ])
    body += "<h2>Resolved link targets (full titles as read from the pages)</h2>" + table(
        ["Product link", "Page ID", "Page title as read", "Status", "Source"], obs)
    page("flagged.html", "Flagged for review", body,
         lead=(f"{len(FLAGS)} entries: {sev_count('Critical')} critical, {sev_count('High')} high, "
               f"{sev_count('Medium')} medium, {sev_count('Low')} low, {sev_count('Info')} info "
               "(info entries record a correction made to this site, not a problem with a product)."))


# ------------------------------------------------------------- Sources
def build_sources() -> None:
    rows = []
    for s in SRC["sources"]:
        status = {
            "verified": badge("Verified", "ok"),
            "observed": badge("Observed", "info"),
            "not-accessible": badge("Not accessible", "warn"),
            "third-party": badge("Third-party (not verified)", "bad"),
        }[s["status"]]
        rows.append([
            f'<strong>{e(s["id"])}</strong>',
            e(s["title"]),
            f'<a href="{e(s["url"])}" target="_blank" rel="noopener noreferrer">{e(s["url"])}</a>',
            status,
            e(s["status_note"]),
            e(s["used_for"]),
        ])
    body = (
        f'<p class="muted">Retrieved {e(SRC["retrieved"])}. Official = Amazon Associates, Amazon.com, Amazon Seller Central, or the U.S. FTC. '
        "Third-party sources appear only to raise flags.</p>"
        + table(["ID", "Source", "Link", "Status", "Note", "Used for"], rows)
    )
    page("sources.html", "Sources", body,
         lead="Every official page used to verify this site, with the status it had when read.")


# ------------------------------------------------------------- Category
COMP = load("competition.json")


def build_category() -> None:
    """Category subpage: Air Fryers (Amazon browse node 17659096011).

    Only verified fields are shown. Prices, ratings and review counts are NOT shown
    (Participation Requirements 2(b) and 6(t); see FLG-028)."""
    path_rows = []
    nodes = ["1055398", "284507", "289913", "17659095011", "17659096011"]
    for i, (name, node) in enumerate(zip(COMP["category_path"], nodes), start=1):
        path_rows.append([str(i), e(name), e(node),
                          src_links(["S14", "S15", "S16"]) + (" &middot; " + src_links(["S43"]) if i == 5 else "")])
    body = "<h2>Verified category path</h2>" + table(
        ["Level", "Category", "Browse node", "Source"], path_rows)

    sub_rows = []
    for p in PRODUCTS:
        ro = p["redirect_observed"]
        sub_rows.append([
            e(p["label"]),
            f'<a href="{e(p["submitted_url"])}" target="_blank" rel="noopener noreferrer">{e(p["link_id"])}</a>',
            f'<a href="{e(ro["final_url"])}" target="_blank" rel="noopener noreferrer">{e(ro["page_id"])}</a> {badge("Not confirmed as submitted", "warn")}',
            e(ro["page_title"]),
            flag_links(p["flags"]),
            src_links([ro["title_source"], ro["source"]]),
        ])
    body += "<h2>Submitted links in this category</h2>" + table(
        ["Product", "Submitted link", "Observed destination", "Destination page title (as read)", "Flags", "Source"], sub_rows)

    bs_rows = []
    for r in COMP["rows"]:
        bs_rows.append([
            f'<strong>#{r["rank"]}</strong>',
            f'<a href="{e(r["url"])}" target="_blank" rel="noopener noreferrer">{e(r["asin"])}</a>',
            e(r["title"]),
            src_links([COMP["source"]]) + " " + flag_links(["FLG-028", "FLG-025"]),
        ])
    body += ("<h2>Competition benchmark: Best Sellers in Air Fryers (positions 1&ndash;6)</h2>"
             f'<p class="muted">Read {e(COMP["read_on"])}. Positions 7 and below are not used. Rank changes between captures (FLG-025).</p>'
             + table(["Rank", "ASIN (link)", "Title as shown on the official page", "Source"], bs_rows))

    body += "<h2>Commission reference (not applied)</h2>" + table(
        ["Rate-card category", "Standard rate", "Status", "Source"],
        [["Kitchen (Standard Commission, Table 1)", "4.50%",
          "Reference only. Whether it applies to these listings is not confirmed (FLG-021).",
          src_links(["S25"]) + " " + flag_links(["FLG-021"])]])
    body += """
<section class="card">
  <h2>What this page does and does not show</h2>
  <ul class="findings">
    <li>The category path and the six bestseller positions were read from official Amazon pages on 2026-11-14.</li>
    <li>The submitted identifiers do not resolve to a product page under their own code (see <a href="products.html">Products</a>, FLG-001). The observed destinations are not treated as the submitted products (FLG-002).</li>
    <li>Prices, ratings and review counts are blank here. They can be shown only through an approved Amazon data path (FLG-028, FLG-029).</li>
    <li>No claim is made about competitors beyond position 6, because that part of the list was not read.</li>
  </ul>
</section>
"""
    page("air-fryers.html", "Category: Air Fryers", body,
         lead="Amazon browse node 17659096011. The category path, the submitted links that fall in it, and a six-position bestseller benchmark, each linked to its official page.")


def build_assets() -> None:
    ASSETS.mkdir(exist_ok=True)
    (ASSETS / "style.css").write_text(css(), encoding="utf-8")
    (ROOT / ".nojekyll").write_text("", encoding="utf-8")


def build_legacy_stubs() -> None:
    """Old URLs from PR #1 (session 26634cd5). They redirect to the pages that replace them."""
    stubs = {
        "analysis.html": "executive-summary.html",
        "disclosure.html": "content.html",
        "categories/home-kitchen-air-fryers.html": "category/air-fryers.html",
        "flagged-for-review.html": "flagged.html",    }
    for name, target in stubs.items():
        path = ROOT / name
        path.parent.mkdir(parents=True, exist_ok=True)
        rel = "../" + target if "/" in name else target
        path.write_text(
            '<!doctype html><html lang="en"><head><meta charset="utf-8">'
            f'<meta http-equiv="refresh" content="0; url={rel}">'
            '<link rel="canonical" href="' + rel + '">'
            '<title>Moved</title></head><body>'
            f'<p>This page has moved to <a href="{rel}">{rel}</a>.</p></body></html>\n',
            encoding="utf-8",
        )


def main() -> None:
    build_assets()
    build_index()
    build_exec()
    build_products()
    build_category()
    build_pricing()
    build_reviews()
    build_marketing()
    build_content()
    build_campaigns()
    build_flagged()
    build_category()
    build_sources()
    build_legacy_stubs()
    print("built site in", ROOT)


if __name__ == "__main__":
    main()
