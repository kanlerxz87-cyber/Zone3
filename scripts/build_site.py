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
DATA = ROOT / "data"
ASSETS = ROOT / "assets"
BUILT = "2026-11-13"
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
    kind = {"Critical": "bad", "High": "warn", "Medium": "info", "Low": "muted"}[text]
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
    ("pricing.html", "Pricing &amp; commission"),
    ("reviews.html", "Reviews &amp; competition"),
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
  <p class="muted">Data verified as of {BUILT}. A cell marked <span class="badge unv">Unverified</span> has no official source yet and is left blank on purpose. Built by <code>scripts/build_site.py</code> from <code>data/*.json</code>. Source IDs (S01 and so on) link to the official page; see the <a href="sources.html">Sources</a> page.</p>
</footer>
</body>
</html>
"""
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
def build_index() -> None:
    stats = [
        ("Product links submitted", str(N), ""),
        ("Product identifiers verified (ASIN)", f"{count_verified('asin')} of {N}", "bad"),
        ("Prices verified", f"{count_verified('price')} of {N}", "warn"),
        ("Commission rates verified", f"{count_verified('commission_rate')} of {N}", "warn"),
        ("Critical flags open", str(sev_count("Critical")), "bad"),
        ("Total flags open", str(len(FLAGS)), "warn"),
    ]
    stat_html = "".join(
        f'<div class="stat {k}"><div class="n">{e(v)}</div><div class="l">{e(l)}</div></div>'
        for l, v, k in stats
    )
    tiles = [
        ("executive-summary.html", "Executive summary", "Bottom line, findings, what was built, what is blocked."),
        ("products.html", "Products", "The 3 submitted links, identifier checks, redirect results."),
        ("pricing.html", "Pricing &amp; commission", "Price and commission fields, plus the verified commission rules."),
        ("reviews.html", "Reviews &amp; competition", "Ratings and competitor fields, a dated category benchmark, plus the verified review rules."),
        ("content.html", "Content &amp; compliance", "Article status and the Associates and FTC checklist."),
        ("campaigns.html", "Campaigns &amp; tracking", "Click and conversion ledger. Empty until data exists."),
        ("flagged.html", "Flagged for review", "Every irregularity and unverified item, with its source links."),
        ("sources.html", "Sources", "The official source registry with retrieval status."),
    ]
    tile_html = "".join(
        f'<a class="tile" href="{h}"><b>{t}</b><span>{d}</span></a>' for h, t, d in tiles
    )
    body = f"""
<div class="callout">
  <p><strong>Headline:</strong> none of the three submitted Amazon links can be verified as a product listing.
  The identifiers are nine characters long and the amazon.com product pages for them return &ldquo;Page Not Found&rdquo;.
  The short links open three different products (two CHEFMAN air fryers and one Emeril Lagasse air fryer toaster oven) that are not confirmed as the submitted products. Those values are left blank.</p>
</div>
<div class="grid">{stat_html}</div>
<h2>Sections</h2>
<div class="tiles">{tile_html}</div>
"""
    page("index.html", "Dashboard", body,
         lead=f"Status as of {BUILT}. The site shows verified data only. Blank cells are unverified and listed on the Flagged for review page.")


# ---------------------------------------------------------- Executive summary
def build_exec() -> None:
    body = f"""
<section class="card">
  <h2>Bottom line</h2>
  <p>The three Amazon links in the brief cannot be verified as product listings. Their identifiers are nine characters long.
  Amazon&rsquo;s official Creators API documentation shows ASIN values of ten characters {src_links(['S06'])}.
  The amazon.com product page for each identifier returns &ldquo;Page Not Found&rdquo; {src_links(['S08', 'S09', 'S10'])}.
  The short links open Amazon product pages, but for three different products (two CHEFMAN air fryers and one Emeril Lagasse air fryer toaster oven), which are not confirmed as the submitted products {src_links(['S11', 'S12', 'S13', 'S14', 'S15', 'S16'])}.</p>
  <p>As the brief requires, every product name, price, rating, review count, commission rate, niche score and click or conversion figure is left blank and marked <span class="badge unv">Unverified</span>. No value was inferred.</p>
</section>

<section class="card">
  <h2>Key findings</h2>
  <ul class="findings">
    <li><strong>0 of {N} product identifiers are confirmed.</strong> The identifiers are nine characters, and the amazon.com pages for them do not exist {flag_links(['FLG-001'])} {src_links(['S06', 'S08', 'S09', 'S10'])}.</li>
    <li><strong>The short links resolve to other products.</strong> Each link ended on a different product page, with the parameters <code>lv=shuf</code> and <code>plpRedirect=mhFallback</code>. The mapping was the same on two fetches. These are recorded as observed only {flag_links(['FLG-002'])} {src_links(['S11', 'S12', 'S13'])}.</li>
    <li><strong>Associates compliance of link.amazon is unconfirmed.</strong> The policies say a shortener must not make the Amazon destination unclear {src_links(['S02'])} (PF-06), and purchases from a Redirecting Link are disqualified (PF-07). Whether link.amazon redirects without a click has to be tested in a logged-in Associates account {flag_links(['FLG-003'])}.</li>
    <li><strong>Commission rates cannot be verified.</strong> The rate schedule redirected to a sign-in page on 2026-11-13 {src_links(['S03'])} {flag_links(['FLG-005'])}.</li>
    <li><strong>Automated product data needs Creators API access.</strong> The official prerequisite is &ldquo;at least 10 qualifying sales within the past 30 days&rdquo; {src_links(['S04'])}. Prices and reviews may be shown only through a Special Link or the API {src_links(['S02'])} (PF-04, PF-05) {flag_links(['FLG-006'])}.</li>
    <li><strong>The AI layer needs written approval from Amazon.</strong> The Creators API terms bar analysing, aggregating or repurposing its data, and bar using Program Content to develop or train machine learning or language models, without express prior written approval {src_links(['S02'])} (PF-23, PF-24, PF-25) {flag_links(['FLG-016'])}.</li>
    <li><strong>Eligibility for a Norway-based owner is not stated.</strong> Schedule 1 of the Operating Agreement lists only the United States site, amazon.com {src_links(['S01'])} (PF-35) {flag_links(['FLG-015'])}.</li>
    <li><strong>PA-API 5 is deprecated.</strong> The official notice says it is being replaced by the Creators API {src_links(['S05'])} (PF-17). Another session branch cites PA-API 5 as the sanctioned source {flag_links(['FLG-007'])}.</li>
    <li><strong>Disclosure is on every page.</strong> The required wording is quoted from the Operating Agreement, Section 5 {src_links(['S01'])} (PF-01). Placement for FTC purposes still needs owner review {flag_links(['FLG-013'])}.</li>
  </ul>
</section>

<section class="card">
  <h2>What was built</h2>
  <ul class="findings">
    <li>A GitHub Pages site (this site) with a landing dashboard and category pages: Products, Pricing &amp; commission, Reviews &amp; competition, Content &amp; compliance, Campaigns &amp; tracking.</li>
    <li>A Flagged for review page with {len(FLAGS)} items, each with its evidence sources and the action needed.</li>
    <li>The earlier session&rsquo;s site from PR #1 is merged in. Its scripts, data and HTML are archived under <code>archive/26634cd5/</code>, and its old <code>analysis.html</code> and category URLs redirect to the pages that replace them.</li>
    <li>A Sources page that lists each official page used, its retrieval status, and what it supports.</li>
    <li>A data layer (<code>data/*.json</code>) with a generator (<code>scripts/build_site.py</code>) and a checker (<code>scripts/check_site.py</code>). The checker fails if a table row has no official source link, or if a value appears without a source.</li>
  </ul>
</section>

<section class="card">
  <h2>What is not done, and why</h2>
  <ul class="findings">
    <li><strong>Product research, niche identification, competition and commission-potential analysis.</strong> These need product data, which needs verified identifiers (FLG-001) and Creators API access (FLG-006). Nothing was estimated.</li>
    <li><strong>SEO articles, comparisons and buying guides.</strong> Product claims must be accurate (PF-10), and the first-hand experience the FTC describes (PF-21) has not happened. These are blocked (FLG-012).</li>
    <li><strong>Click and conversion tracking.</strong> Figures come from the owner&rsquo;s Associates reports. No tag has been supplied (FLG-010), and no reports were available (FLG-011).</li>
    <li><strong>Automated optimisation.</strong> There is no data to optimise. The generator can rebuild the site once verified data is added.</li>
  </ul>
</section>

<section class="card">
  <h2>Owner items (flagged; they do not block the merge)</h2>
  <ul class="findings">
    <li>Give the intended product URL or 10-character ASIN for each of the three products (FLG-001).</li>
    <li>Test each submitted link in a logged-in Associates account and report whether clicks are tracked (FLG-002, FLG-003).</li>
    <li>Export the commission rate card for the product category from Associates Central (FLG-005).</li>
    <li>Confirm Associates enrolment and supply the Associates tag, not a password or token (FLG-010).</li>
  </ul>
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
        rows.append([
            e(p["label"]),
            f'<a href="{e(p["submitted_url"])}" target="_blank" rel="noopener noreferrer">{e(p["submitted_url"])}</a>',
            f'{e(p["link_id"])} <span class="muted">({p["link_id_length"]} chars)</span>',
            val(p["asin"]),
            f'<a href="{e(d["url"])}" target="_blank" rel="noopener noreferrer">{e(d["result"])}</a>',
            f'<a href="{e(ro["final_url"])}" target="_blank" rel="noopener noreferrer">{e(ro["page_id"])}</a> {badge("Not confirmed", "warn")}',
            val(p["product_name"]),
            e(p["status"]),
            flag_links(p["flags"]),
            src_links(p["sources"]),
        ])
    body = table(
        ["#", "Submitted link", "Identifier (length)", "ASIN", "amazon.com/dp check", "Observed redirect (not used as this product)", "Product name", "Status", "Flags", "Source"],
        rows,
    )
    body += f"""
<section class="card">
  <h2>How to read this table</h2>
  <ul class="findings">
    <li>Each row is one product link from the brief. An identifier is counted only when a product page under that identifier exists and matches it.</li>
    <li>&ldquo;Observed redirect&rdquo; is the page the short link opened on 2026-11-13. It is not treated as the submitted product, because the submitted identifier does not resolve to it.</li>
    <li>Product name, brand, price, rating and availability are blank because they cannot be confirmed (see <a href="pricing.html">Pricing</a> and <a href="reviews.html">Reviews</a>).</li>
  </ul>
</section>
"""
    page("products.html", "Products", body,
         lead="The three product links from the brief, checked line by line against official Amazon pages. Nothing is shown as a verified product until its identifier resolves.")


# ------------------------------------------------------------- Pricing
def build_pricing() -> None:
    rows = []
    for p in PRODUCTS:
        rows.append([
            e(p["label"]),
            val(p["price"]),
            val(p["commission_rate"]),
            badge("Blocked: no product record", "bad") + " " + badge("Schedule not accessible", "warn"),
            flag_links(["FLG-004", "FLG-005"]),
            src_links(["S03", "S02", p["direct_check"]["source"]]),
        ])
    body = "<h2>Price and commission fields</h2>" + table(
        ["Product", "Price", "Commission rate", "Status", "Flags", "Source"], rows)

    rules = [
        ["Commission window (session)", FACTS["PF-12"]["quote"], "A click-to-sale record needs the click time, a 24-hour session, and the 89-day cart window.", src_links(["S02"])],
        ["Cancelled, returned or refunded orders", FACTS["PF-13"]["quote"], "Conversion counts must exclude these orders.", src_links(["S02"])],
        ["Redirecting Links disqualify purchases", FACTS["PF-07"]["quote"], "Relevant to the link.amazon question (FLG-003).", src_links(["S02"])],
        ["Prices shown only via link or API", FACTS["PF-04"]["quote"], "Price cells stay blank until one of these two routes is available.", src_links(["S02"])],
        ["Comparison-price display", FACTS["PF-11"]["quote"], "Any future comparison table must show lowest new and used prices from Amazon.", src_links(["S02"])],
    ]
    rules_html = table(["Rule", "Verified wording (quoted)", "What it means here", "Source"], rules)
    body += f'<h2>Verified commission and pricing rules</h2>{rules_html}'
    ref_rows = [
        ["Kitchen (Standard Commission, Table 1)", "4.50%", "Reference only. Applies only if a listing is in the Kitchen category, which is not verified (FLG-021).", FACTS["PF-38"]["quote"], src_links(["S25"]) + " " + flag_links(["FLG-021"])],
        ["Kitchen (Onsite Commission, Table A)", "1.25%", "Not a rate for links on this site. It applies to Onsite Content used by Amazon within the Amazon Site.", FACTS["PF-39"]["quote"], src_links(["S26"]) + " " + flag_links(["FLG-021"])],
    ]
    body += "<h2>Category reference rates (not product values)</h2>" + table(["Category and table", "Rate", "What it means here", "Verified wording (quoted)", "Source"], ref_rows)
    page("pricing.html", "Pricing &amp; commission", body,
         lead="Price and commission fields are blank because the source needed to fill them (the commission rate schedule, and the Creators API) is not available to this session. The rules below are verified.")


# ------------------------------------------------------------- Reviews
def build_reviews() -> None:
    rows = []
    for p in PRODUCTS:
        rows.append([
            e(p["label"]),
            val(p["rating"]),
            val(p["review_count"]),
            val(p["competitor_count"]),
            val(p["best_seller_rank"]),
            flag_links(["FLG-004", "FLG-006"]),
            src_links(["S02", "S04", p["direct_check"]["source"]]),
        ])
    body = "<h2>Rating, review and competition fields</h2>" + table(
        ["Product", "Rating", "Review count", "Competing listings", "Best-seller rank", "Flags", "Source"], rows)
    rules = [
        ["Reviews and star ratings", FACTS["PF-05"]["quote"], "Ratings and review counts are blank. They can only come from the API.", src_links(["S02"])],
        ["No inaccurate or misleading product claims", FACTS["PF-10"]["quote"], "Competition statements cannot be made until product data is verified.", src_links(["S02"])],
        ["Original content and third-party material", FACTS["PF-15"]["quote"], "Pages must add analysis to any product data they use.", src_links(["S02"])],
    ]
    body += "<h2>Verified review and content rules</h2>" + table(
        ["Rule", "Verified wording (quoted)", "What it means here", "Source"], rules)
    body += build_benchmark()
    page("reviews.html", "Reviews &amp; competition", body,
         lead="Ratings, review counts and competition data for the submitted links are blank. No review or star rating from Amazon is shown on this site (PF-05). A dated category benchmark is published below from the official Best Sellers page, with prices and ratings withheld by policy.")


# ------------------------------------------------------------- Competition benchmark
def build_benchmark() -> str:
    """Competition benchmark surfaced as-is (integration session ecbfe91b, E-T5).

    Rows come from data/c4e71983-competitors.json: session c4e71983's capture of Amazon's
    official Best Sellers page for Air Fryers (2026-11-13), re-checked live 2026-11-14 by
    session ecbfe91b. Identity and rank fields are shown with their official source links.
    Price, star rating and review count are blanked on purpose (Program Policies 2(b) and
    the ratings rule PF-05) and published as a flag instead of a value (FLG-022).
    """
    comp = load("c4e71983-competitors.json")
    rows = []
    for b in comp["bestsellers"]:
        rows.append([
            e(b["rank"]),
            f'<a href="{e(b["url"])}" target="_blank" rel="noopener noreferrer" '
            f'title="Official Amazon product page">{e(b["asin"])}</a>',
            e(b["title"]),
            e(b["brand"]),
            e(b["capacity"]),
            badge("Not displayed (policy)", "warn"),
            badge("Not displayed (policy)", "warn"),
            badge("Not displayed (policy)", "warn"),
            flag_links(["FLG-022"]),
            src_links(["S30"]),
        ])
    intro = (
        '<div class="callout"><p><strong>How to read this table.</strong> '
        "Captured 2026-11-13 from Amazon&rsquo;s official Best Sellers page for Air Fryers "
        f'{src_links(["S30"])} and re-checked live 2026-11-14. This is the category of the three '
        "<em>observed redirect targets</em>, which are not confirmed as the submitted products "
        f'{flag_links(["FLG-002"])} &middot; {src_links(["S11"])}&ndash;{src_links(["S13"])}. '
        "Ranks are a dated snapshot: positions 2 and 3 swapped between the capture and the re-check, "
        "so no rank here is a live value. Prices, star ratings and review counts are withheld by policy "
        f'(Program Policies 2(b) and PF-05) {src_links(["S02"])} {flag_links(["FLG-022"])}; the captured '
        "values stay in <code>data/c4e71983-competitors.json</code> for internal analysis only. "
        "Every row links to its official Amazon product page and to the capture source.</p></div>"
    )
    return intro + "<h2>Competition benchmark &mdash; Air Fryers best sellers (dated snapshot)</h2>" + table(
        ["Rank (2026-11-13)", "ASIN", "Product", "Brand", "Capacity", "Price", "Rating", "Review count", "Flags", "Source"],
        rows)


# ------------------------------------------------------------- Content
def build_content() -> None:
    rows = []
    for p in PRODUCTS:
        rows.append([
            e(p["label"]),
            badge("Not written", "bad"),
            badge("Not written", "bad"),
            badge("Not written", "bad"),
            "Product facts are unverified (FLG-001, FLG-004). Writing now would present an unconfirmed product as the one in the brief. PF-10 forbids misleading product claims.",
            flag_links(["FLG-012"]),
            src_links(["S02", "S07"]),
        ])
    body = "<h2>Content status</h2>" + table(
        ["Product", "SEO product article", "Comparison", "Buying guide", "Why it is blocked", "Flags", "Source"], rows)

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
         lead="No article, comparison or buying guide has been written yet. The checklist below records what any content must meet before it is published.")


# ------------------------------------------------------------- Campaigns
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
            src_links(f["sources"]) if f["sources"] else '<span class="muted">internal (repo)</span>',
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
            badge("No: not the submitted product", "warn"),
            src_links([ro["title_source"]]),
        ])
    body += "<h2>Observed redirect targets (full titles as read, not confirmed)</h2>" + table(
        ["Product link", "Page ID", "Page title as read", "Confirmed?", "Source"], obs)
    page("flagged.html", "Flagged for review", body,
         lead=f"{len(FLAGS)} flags: {sev_count('Critical')} critical, {sev_count('High')} high, {sev_count('Medium')} medium, {sev_count('Low')} low.")


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
        f'<p class="muted">Retrieved {e(SRC["retrieved"])}. Official = Amazon Associates, Amazon.com (including Sell on Amazon), Amazon Seller Central, or the U.S. FTC. '
        "Third-party sources appear only to raise flags.</p>"
        + table(["ID", "Source", "Link", "Status", "Note", "Used for"], rows)
    )
    page("sources.html", "Sources", body,
         lead="Every official page used to verify this site, with the status it had when read.")


def build_assets() -> None:
    ASSETS.mkdir(exist_ok=True)
    (ASSETS / "style.css").write_text(css(), encoding="utf-8")
    (ROOT / ".nojekyll").write_text("", encoding="utf-8")


def build_legacy_stubs() -> None:
    """Old URLs from PR #1 (session 26634cd5). They redirect to the pages that replace them."""
    stubs = {
        "analysis.html": "executive-summary.html",
        "disclosure.html": "content.html",
        "categories/home-kitchen-air-fryers.html": "products.html",
    }
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
    build_pricing()
    build_reviews()
    build_content()
    build_campaigns()
    build_flagged()
    build_sources()
    build_legacy_stubs()
    print("built site in", ROOT)


if __name__ == "__main__":
    main()
