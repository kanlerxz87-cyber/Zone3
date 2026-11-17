#!/usr/bin/env python3
"""Build the /shop/ section from data/shop/*.json and run the publishing gate.

Usage:
  python3 tools/build_shop.py           # write shop/** and append missing sitemap URLs, then check
  python3 tools/build_shop.py --check   # check only (no writes); exit 1 on any failure

Only data/shop/*.json is read as content. Every page carries the Associates disclosure
(Operating Agreement Section 5, verbatim) under the masthead and in the footer. Every link to
amazon.com or link.amazon is marked rel="sponsored". Table rows for products, findings,
sources and flags must each contain an https source link. No price, star rating or review
figure is written anywhere in the section.
"""
from __future__ import annotations

import html
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "shop"
SHOP = ROOT / "shop"
SITEMAP = ROOT / "sitemap.xml"

CFG = json.loads((DATA / "config.json").read_text(encoding="utf-8"))
PRODUCTS = json.loads((DATA / "products.json").read_text(encoding="utf-8"))
SOURCES = json.loads((DATA / "sources.json").read_text(encoding="utf-8"))
FLAGS = json.loads((DATA / "flags.json").read_text(encoding="utf-8"))
DECISIONS = json.loads((DATA / "decisions.json").read_text(encoding="utf-8"))
LEDGER = json.loads((DATA / "campaign-ledger.json").read_text(encoding="utf-8"))

DISCLOSURE = CFG["associates_disclosure"]
ORIGIN = CFG["site_origin"].rstrip("/")
BASE = CFG["base_path"].rstrip("/")  # "/Zone3/shop"
CHECKED = CFG["checked_on"]
CHECKED_HUMAN = "17 Nov 2026"
OFFICIAL_HOSTS = {
    "affiliate-program.amazon.com", "www.amazon.com", "amazon.com", "link.amazon",
    "developers.google.com", "www.ftc.gov", "ftc.gov", "github.com", "docs.github.com",
    # Added by session 3c96f21d (2026-11-17): the two documentation hosts the measurement
    # layer cites - Mozilla MDN for the web APIs the counter uses, and Cloudflare's own
    # documentation for the Worker the collector variant targets. Both are official for the
    # thing they document; neither is a product-fact source.
    "developer.mozilla.org", "developers.cloudflare.com",
}
SPONSORED_HOSTS = {"www.amazon.com", "amazon.com", "link.amazon"}

NAV = [
    ("index.html", "Shop home"),
    ("air-fryers/index.html", "Air fryers"),
    ("meat-thermometers/index.html", "Meat thermometers"),
    ("products/index.html", "All products"),
    ("findings/index.html", "Findings"),
    ("decisions/index.html", "Decisions"),
    ("flagged/index.html", "Flagged for review"),
    ("sources/index.html", "Sources"),
    ("executive-summary/index.html", "Executive summary"),
    ("campaigns/index.html", "Campaign ledger"),
    ("disclosure/index.html", "Disclosure"),
]

PAGES: dict[str, dict] = {}  # path -> {"title","desc","body","depth"}


def e(s) -> str:
    return html.escape("" if s is None else str(s), quote=True)


def prefix(depth: int) -> str:
    return "../" * depth


def canonical(path: str) -> str:
    return f"{ORIGIN}{BASE}/{path}".replace("index.html", "")


def nav_html(depth: int, active: str) -> str:
    p = prefix(depth)
    items = []
    for href, label in NAV:
        cls = ' class="active" aria-current="page"' if href == active else ""
        items.append(f'<a href="{p}{href}"{cls}>{e(label)}</a>')
    return "\n".join(items)


def footer_html(depth: int) -> str:
    p = prefix(depth)
    links = "".join(f'<li><a href="{p}{href}">{e(label)}</a></li>' for href, label in NAV)
    return f"""<footer class="site-footer">
  <div class="wrap">
    <aside class="disclosure disclosure-footer" role="note" aria-label="Affiliate disclosure">
      <strong>Affiliate disclosure.</strong> {e(DISCLOSURE)} Links marked <em>Sponsored</em> go to Amazon.
    </aside>
    <div class="foot-grid">
      <div>
        <p class="foot-title">{e(CFG["site_name"])}</p>
        <p class="muted">Product facts are taken from the linked Amazon pages and their checked dates. Unverified values are left blank and flagged. {e(CFG["site_name_status"])}</p>
      </div>
      <div>
        <p class="foot-title">All pages</p>
        <ul class="foot-links">{links}</ul>
      </div>
      <div>
        <p class="foot-title">Related</p>
        <ul class="foot-links">
          <li><a href="{p}../index.html">Repository front page</a></li>
          <li><a href="https://github.com/kanlerxz87-cyber/Zone3">Source repository</a></li>
        </ul>
        <p class="muted small">Last checked {e(CHECKED_HUMAN)}.</p>
      </div>
    </div>
  </div>
</footer>"""


def page(path: str, title: str, desc: str, body: str) -> None:
    depth = path.count("/")
    PAGES[path] = {"title": title, "desc": desc, "body": body, "depth": depth}


def render(path: str, rec: dict) -> str:
    depth = rec["depth"]
    p = prefix(depth)
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(rec["title"])}</title>
<meta name="description" content="{e(rec["desc"])}">
<link rel="canonical" href="{e(canonical(path))}">
<link rel="stylesheet" href="{p}assets/shop.css">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="masthead">
  <div class="wrap masthead-row">
    <a class="brand" href="{p}index.html">{e(CFG["site_name"])}</a>
    <span class="tagline">Kitchen products, linked to Amazon and checked against their listings</span>
  </div>
  <nav class="wrap topnav" aria-label="Main">
    {nav_html(depth, path)}
  </nav>
</header>
<aside class="disclosure disclosure-top" role="note" aria-label="Affiliate disclosure">
  <div class="wrap"><strong>Affiliate disclosure.</strong> {e(DISCLOSURE)} Links marked <em>Sponsored</em> go to Amazon.</div>
</aside>
<main id="main" class="wrap">
{rec["body"]}
</main>
{footer_html(depth)}
</body>
</html>
"""


# ---------- link helpers -------------------------------------------------

def sponsored(url: str, text: str, extra_cls: str = "") -> str:
    cls = f' class="{extra_cls}"' if extra_cls else ""
    return (f'<a{cls} href="{e(url)}" rel="sponsored noopener" target="_blank">'
            f'{e(text)}</a>')


def plain(url: str, text: str) -> str:
    host = re.sub(r"^https?://([^/]+).*", r"\1", url)
    if host in SPONSORED_HOSTS:
        return sponsored(url, text)
    return f'<a href="{e(url)}">{e(text)}</a>'


def unverified_cell() -> str:
    return '<span class="pill pill-warn">Unverified</span>'


def disclosure_inline() -> str:
    return f'<p class="disclosure-inline"><strong>Affiliate disclosure.</strong> {e(DISCLOSURE)}</p>'


CAT_TITLE = {c["slug"]: c["title"] for c in CFG["categories"]}
CAT_BLURB = {c["slug"]: c["blurb"] for c in CFG["categories"]}


def product_short_token(p: dict) -> str:
    return p["submitted_link"].rsplit("/", 1)[-1]


def fmt_date(iso: str) -> str:
    if not iso:
        return ""
    y, m, d = iso.split("-")
    months = "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split()
    return f"{int(d)} {months[int(m) - 1]} {y}"


# ---------- pages --------------------------------------------------------

def build_pages() -> None:
    PAGES.clear()
    n_products = len(PRODUCTS["products"])
    n_intended = sum(1 for p in PRODUCTS["products"] if p["intended_asin"])
    n_flags = len(FLAGS["flags"])
    n_open_decisions = len(DECISIONS["decisions"])
    n_sources = len(SOURCES["sources"])

    # ---- landing (products first) ----
    cards = []
    for p in PRODUCTS["products"]:
        cards.append(f"""<article class="card">
  <p class="kicker">{e(CAT_TITLE[p["category"]])}</p>
  <h3>{e(p["observed_title"])}</h3>
  <p class="meta">Observed ASIN <code>{e(p["observed_redirect_asin"])}</code> · checked {e(CHECKED_HUMAN)}</p>
  <p class="card-cta">{sponsored(p["submitted_link"], "View on Amazon", "btn")} <span class="sponsored-tag">Sponsored</span></p>
</article>""")
    cat_tiles = []
    for c in CFG["categories"]:
        count = sum(1 for p in PRODUCTS["products"] if p["category"] == c["slug"])
        cat_tiles.append(f"""<a class="tile" href="{c["slug"]}/index.html">
  <span class="tile-count">{count} listings</span>
  <span class="tile-title">{e(c["title"])}</span>
  <span class="tile-blurb">{e(c["blurb"])}</span>
</a>""")
    landing = f"""<section class="hero">
  <p class="kicker">Front page · {n_products} listings · {len(CFG["categories"])} categories</p>
  <h1>Air fryers and meat thermometers, each linked to its Amazon listing</h1>
  <p class="lede">Every product below opens its Amazon page through the submitted link. The title and ASIN shown are what that page reported when we checked it on {e(CHECKED_HUMAN)}. Anything we could not confirm is left blank and marked.</p>
</section>
<section class="block" aria-labelledby="products-h">
  <h2 id="products-h">The products</h2>
  <div class="grid">
{chr(10).join(cards)}
  </div>
</section>
<section class="block" aria-labelledby="cats-h">
  <h2 id="cats-h">Browse by category</h2>
  <div class="tiles">
{chr(10).join(cat_tiles)}
  </div>
</section>
<section class="block status" aria-labelledby="status-h">
  <h2 id="status-h">What is still open</h2>
  <p>We have not yet confirmed which ASIN the requester meant for any of the {n_products} links ({n_intended} of {n_products} confirmed). The Special Link test has not been run. No click or sales figures are published.</p>
  <p class="actions">
    <a class="btn-ghost" href="flagged/index.html">See {n_flags} items flagged for review</a>
    <a class="btn-ghost" href="decisions/index.html">See {n_open_decisions} decisions for you</a>
    <a class="btn-ghost" href="findings/index.html">Read the findings</a>
  </p>
</section>
"""
    page("index.html",
         f"{CFG['site_name']} — air fryers and meat thermometers linked to Amazon",
         "Five Amazon listings in two categories, each linked through the submitted link with its observed ASIN and what is still unverified.",
         landing)

    # ---- category pages ----
    for c in CFG["categories"]:
        rows = []
        for p in [x for x in PRODUCTS["products"] if x["category"] == c["slug"]]:
            rows.append(f"""<tr>
  <td>{sponsored(p["submitted_link"], p["observed_title"])}<br><span class="muted small">{e(p["id"])} · submitted {e(product_short_token(p))}</span></td>
  <td>{sponsored(p["observed_redirect_listing_url"], p["observed_redirect_asin"])}</td>
  <td>{unverified_cell()}</td>
  <td>{sponsored(p["source_url"], "Amazon listing")}</td>
  <td>{e(CHECKED_HUMAN)}</td>
</tr>""")
        body = f"""<section class="page-head">
  <p class="kicker"><a href="../index.html">Shop home</a> / {e(c["title"])}</p>
  <h1>{e(c["title"])}</h1>
  <p class="lede">{e(c["blurb"])}</p>
</section>
{disclosure_inline()}
<section class="block">
  <div class="table-wrap">
  <table class="data" data-rule="source">
    <thead><tr><th>Product (observed title)</th><th>Observed ASIN</th><th>Intended ASIN</th><th>Source</th><th>Checked</th></tr></thead>
    <tbody>
{chr(10).join(rows)}
    </tbody>
  </table>
  </div>
  <p class="small muted">The intended ASIN column is blank because the requester has not stated one for any link (FLG-S02). The observed ASIN is the page the submitted link opened. It is not treated as the intended product.</p>
</section>"""
        page(f"{c['slug']}/index.html",
             f"{c['title']} — Zone3 Kitchen",
             f"{c['title']}: {len([x for x in PRODUCTS['products'] if x['category'] == c['slug']])} Amazon listings with observed ASINs and the intended-ASIN status.",
             body)

    # ---- all products (register) ----
    rows = []
    for p in PRODUCTS["products"]:
        token = product_short_token(p)
        rows.append(f"""<tr>
  <td>{e(p["id"])}</td>
  <td>{sponsored(p["submitted_link"], token)}</td>
  <td>{len(token)} characters</td>
  <td>{unverified_cell()}</td>
  <td>{unverified_cell()}</td>
  <td>{unverified_cell()}</td>
  <td>{sponsored(p["observed_redirect_listing_url"], p["observed_redirect_asin"])}</td>
  <td>{e(p["observed_title"])}</td>
  <td>{e(fmt_date(p["observed_on"]))}</td>
  <td>{sponsored(p["source_url"], "Amazon listing")}</td>
</tr>""")
    body = f"""<section class="page-head">
  <p class="kicker"><a href="../index.html">Shop home</a> / Register</p>
  <h1>All products</h1>
  <p class="lede">One row per submitted link. The left block is the intent record: the requester's intended ASIN and its confirmation. It is blank until confirmed. The right block holds the observed redirect target, kept separate.</p>
</section>
{disclosure_inline()}
<section class="block">
  <div class="table-wrap">
  <table class="data wide" data-rule="source">
    <thead><tr>
      <th>ID</th><th>Submitted link</th><th>Token length</th>
      <th>Intended ASIN</th><th>Official listing URL (intended)</th><th>Intent confirmed (date and source)</th>
      <th>Observed redirect ASIN</th><th>Observed listing title</th><th>Observed on</th><th>Source</th>
    </tr></thead>
    <tbody>
{chr(10).join(rows)}
    </tbody>
  </table>
  </div>
  <p class="small muted">A 10-character ASIN is the Creators API definition (SH-S03). Each submitted token is 9 characters, so none is an ASIN. Intended-ASIN fields stay blank until the requester supplies a value and it is checked against the official listing.</p>
</section>"""
    page("products/index.html", "All products — intent record and observed redirects",
         "Register of the five submitted Amazon links: submitted token, intended-ASIN status and the observed redirect target, kept in separate columns.",
         body)

    # ---- findings ----
    findings = [
        ("F1", "All five submitted links opened, and each resolved to an Amazon listing page.", "Observed on " + CHECKED_HUMAN, "SH-S06 to SH-S10", "https://link.amazon/B04G1MEwY"),
        ("F2", "None of the five submitted tokens is a 10-character ASIN (each is 9 characters).", "Verified (counted; definition checked)", "SH-S03", "https://affiliate-program.amazon.com/creatorsapi/docs/en-us/api-reference/operations/get-items"),
        ("F3", "No intended ASIN is confirmed for any product.", "Unverified (left blank)", "FLG-S02", "https://affiliate-program.amazon.com/help/operating/agreement"),
        ("F4", "The disclosure sentence on every page is the Operating Agreement Section 5 sentence, verbatim.", "Verified (Agreement header: Updated October 15, 2025)", "SH-S01", "https://affiliate-program.amazon.com/help/operating/agreement"),
        ("F5", "The disclosure appears under the masthead and in the footer of every page, and beside each product table.", "Built; checked by the build gate", "SH-S05", "https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers"),
        ("F6", "Every link to amazon.com or link.amazon is marked rel=\"sponsored\".", "Built; checked by the build gate", "SH-S04", "https://developers.google.com/search/docs/crawling-indexing/qualify-outbound-links"),
        ("F7", "No price, star rating or review count is shown anywhere in this section.", "Design decision. Participation Requirement 2(b) is cited from earlier records and was not re-read on this date", "FLG-S07", "https://affiliate-program.amazon.com/help/operating/policies"),
        ("F8", "Commission Income Statement Sections 2(e) and 2(g) disqualify purchases referred by redirecting links or links not properly formatted.", "Verified (chunk 1 of 11 read)", "SH-S02", "https://affiliate-program.amazon.com/help/operating/policies"),
        ("F9", "The Special Link test (one link per product in the Associates workflow) has not been run.", "Not done (no account access)", "FLG-S04", "https://affiliate-program.amazon.com/help/operating/policies"),
        ("F10", "The tracking ID shopnow047c-20 is recorded as user-selected and is not embedded in any link.", "Recorded; ownership unverified", "FLG-S05", "https://affiliate-program.amazon.com/help/operating/agreement"),
        ("F11", "No click counter or self-hosted analytics endpoint is live. The host logs visitor IP addresses for security, so 'privacy-preserving' cannot be claimed for the host itself.", "Not built (decision needed)", "SH-S16", "https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages"),
        ("F12", "The campaign ledger is empty. No authorized first-party report has been obtained.", "Done (empty by design)", "SH-S02", "https://affiliate-program.amazon.com/help/operating/policies"),
        ("F13", "No product photography is used.", "Decision open", "FLG-S08", "https://affiliate-program.amazon.com/help/operating/agreement"),
    ]
    src_by_id = {s["id"]: s for s in SOURCES["sources"]}
    rows = []
    for fid, text, status, src, url in findings:
        rows.append(f"""<tr>
  <td>{e(fid)}</td><td>{e(text)}</td><td>{e(status)}</td>
  <td>{plain(url, src)}</td>
</tr>""")
    body = f"""<section class="page-head">
  <p class="kicker"><a href="../index.html">Shop home</a> / Analysis</p>
  <h1>Findings</h1>
  <p class="lede">What was checked, what was found, and what is still open. Each row links to an official page or to the flag that explains it.</p>
</section>
<section class="block">
  <div class="table-wrap">
  <table class="data" data-rule="source">
    <thead><tr><th>ID</th><th>Finding</th><th>Status</th><th>Source</th></tr></thead>
    <tbody>
{chr(10).join(rows)}
    </tbody>
  </table>
  </div>
</section>"""
    page("findings/index.html", "Findings — what the shop checks show",
         "Findings from checking the five Amazon links and the disclosure, sponsored-link and measurement requirements, with status for each.",
         body)

    # ---- decisions ----
    drows = []
    for d in DECISIONS["decisions"]:
        opts = "<ol class=\"opts\">" + "".join(f"<li>{e(o)}</li>" for o in d["options"]) + "</ol>"
        srcs = " · ".join(plain(s["url"], s["label"]) for s in d.get("sources", [])) or '<span class="muted">No external source applies.</span>'
        drows.append(f"""<tr>
  <td>{e(d["id"])}</td><td>{e(d["question"])}</td><td>{opts}</td>
  <td>{e(d["suggested"])}</td><td>{e(d["needs"])}</td><td>{srcs}</td>
</tr>""")
    qrows = []
    for q in DECISIONS["questions"]:
        srcs = " · ".join(plain(s["url"], s["label"]) for s in q.get("sources", [])) or '<span class="muted">No external source applies.</span>'
        qrows.append(f"""<tr>
  <td>{e(q["question"])}</td><td>{e(q["have"])}</td><td>{e(q["missing"])}</td>
  <td>{e(q["how_to_find"])}</td><td>{srcs}</td>
</tr>""")
    body = f"""<section class="page-head">
  <p class="kicker"><a href="../index.html">Shop home</a> / Suggestions</p>
  <h1>Decisions and suggestions</h1>
  <p class="lede">Choose a path for each item. Suggestions are labelled as suggestions. Nothing here has been carried out beyond what the findings page records.</p>
</section>
<section class="block">
  <h2>Decisions</h2>
  <div class="table-wrap">
  <table class="data">
    <thead><tr><th>ID</th><th>Question</th><th>Options</th><th>Suggested</th><th>Needs</th><th>Source</th></tr></thead>
    <tbody>
{chr(10).join(drows)}
    </tbody>
  </table>
  </div>
</section>
<section class="block">
  <h2>Questions and information still missing</h2>
  <p class="small muted">Written from what the repository and the five links already show, against what is still missing.</p>
  <div class="table-wrap">
  <table class="data">
    <thead><tr><th>Question</th><th>What we have</th><th>What is missing</th><th>How to find it</th><th>Source</th></tr></thead>
    <tbody>
{chr(10).join(qrows)}
    </tbody>
  </table>
  </div>
</section>"""
    page("decisions/index.html", "Decisions and suggestions — choose the path",
         "Options for each open decision, the questions still unanswered, and what information would settle them.",
         body)

    # ---- flagged ----
    frows = []
    for f in FLAGS["flags"]:
        srcs = "<br>".join(plain(s["url"], s["label"]) for s in f["sources"])
        frows.append(f"""<tr>
  <td>{e(f["id"])}</td><td>{e(f["severity"])}</td><td>{e(f["status"])}</td>
  <td>{e(f["issue"])}</td><td>{e(f["impact"])}</td><td>{e(f["what_we_did"])}</td>
  <td>{srcs}</td><td>{e(f["claim_not_made"])}</td>
</tr>""")
    body = f"""<section class="page-head">
  <p class="kicker"><a href="../index.html">Shop home</a> / Review</p>
  <h1>Flagged for review</h1>
  <p class="lede">Items that could not be confirmed or that need a decision. Flags do not block publishing. Each one has its source link, so the owner can review it and request changes.</p>
</section>
<section class="block">
  <div class="table-wrap">
  <table class="data" data-rule="source">
    <thead><tr><th>ID</th><th>Severity</th><th>Status</th><th>Issue</th><th>Impact</th><th>What was done</th><th>Sources</th><th>Claim not made</th></tr></thead>
    <tbody>
{chr(10).join(frows)}
    </tbody>
  </table>
  </div>
</section>"""
    page("flagged/index.html", "Flagged for review — shop build",
         f"{n_flags} items flagged for review, each with its source link and what this build did not claim.",
         body)

    # ---- sources ----
    srows = []
    for s in SOURCES["sources"]:
        srows.append(f"""<tr>
  <td>{e(s["id"])}</td><td>{e(s["publisher"])}</td>
  <td>{plain(s["url"], s["title"])}</td>
  <td>{e(fmt_date(s["checked_on"]))}</td><td>{e(s["read"])}</td><td>{e(s["supports"])}</td>
</tr>""")
    body = f"""<section class="page-head">
  <p class="kicker"><a href="../index.html">Shop home</a> / Sources</p>
  <h1>Sources</h1>
  <p class="lede">Official pages used on this site. The Amazon listing and short-link rows are observed records, not policy documents.</p>
</section>
<section class="block">
  <div class="table-wrap">
  <table class="data" data-rule="source">
    <thead><tr><th>ID</th><th>Publisher</th><th>Source</th><th>Checked</th><th>What was read</th><th>What it supports</th></tr></thead>
    <tbody>
{chr(10).join(srows)}
    </tbody>
  </table>
  </div>
  <p class="small muted">{n_sources} sources. Clauses not re-read on the check date are named in the row that cites them.</p>
</section>"""
    page("sources/index.html", "Sources — official pages used",
         f"{n_sources} official sources and observed Amazon records, with what was read on {CHECKED_HUMAN}.",
         body)

    # ---- executive summary ----
    body = f"""<section class="page-head">
  <p class="kicker"><a href="../index.html">Shop home</a> / Summary</p>
  <h1>Executive summary</h1>
  <p class="lede">What the shop is, what is verified, what is not, and what is needed next.</p>
</section>
{disclosure_inline()}
<section class="block prose">
  <h2>What it is</h2>
  <p>A product page for the five Amazon listings submitted on {e(CHECKED_HUMAN)}: three air fryers and two meat thermometers. Each product links to its listing through the submitted link. Each page carries the Associates disclosure, and each outbound Amazon link is marked sponsored.</p>
  <h2>What is verified</h2>
  <ul>
    <li>All five submitted links open to an Amazon listing. The observed ASINs are B0CDY277D3, B09B7SB46R, B08DKYBTPH, B0DHZTCNR5 and B0DZFD6R9Z (see <a href="../products/index.html">All products</a>).</li>
    <li>Each submitted token is 9 characters, so none is an ASIN under the 10-character definition (<a href="https://affiliate-program.amazon.com/creatorsapi/docs/en-us/api-reference/operations/get-items">Creators API</a>).</li>
    <li>The disclosure sentence matches <a href="https://affiliate-program.amazon.com/help/operating/agreement">Operating Agreement Section 5</a> verbatim.</li>
  </ul>
  <h2>What is not verified or not done</h2>
  <ul>
    <li>Intended ASIN: {n_intended} of {n_products} confirmed. The rest are blank.</li>
    <li>Special Link test: not run. No account access. The tracking ID is not embedded in any link.</li>
    <li>Click counter and self-hosted analytics endpoint: not built. GitHub Pages cannot host a collection endpoint, and the five events were not defined in the brief.</li>
    <li>Prices, ratings and review counts: not shown.</li>
    <li>Campaign ledger: empty. No conversion or revenue figure is shown, and none is forecast.</li>
  </ul>
  <h2>What is needed from you</h2>
  <ol>
    <li>The intended ASIN for each link (DEC-02).</li>
    <li>Access, or a run of the Special Link test (DEC-01).</li>
    <li>The five event definitions and a hosting choice, if click counting is wanted (DEC-03).</li>
    <li>Confirmation of the tracking ID's account and marketplace (FLG-S05).</li>
  </ol>
  <p>Full list: <a href="../decisions/index.html">Decisions</a>, <a href="../flagged/index.html">Flagged for review</a>, <a href="../sources/index.html">Sources</a>.</p>
</section>"""
    page("executive-summary/index.html", "Executive summary — Zone3 Kitchen",
         "What the shop is, what is verified, what is not, and what is needed next.",
         body)

    # ---- campaigns (empty ledger) ----
    cols = "".join(f"<tr><td><code>{e(c['key'])}</code></td><td>{e(c['meaning'])}</td></tr>" for c in LEDGER["columns"])
    body = f"""<section class="page-head">
  <p class="kicker"><a href="../index.html">Shop home</a> / Measurement</p>
  <h1>Campaign ledger</h1>
  <p class="lede">{e(LEDGER["_meta"]["status"])} {e(LEDGER["_meta"]["no_forecast"])}</p>
</section>
<section class="block prose">
  <h2>Rule for adding a row</h2>
  <p>{e(LEDGER["_meta"]["rule"])}</p>
  <p>Source of truth: {e(LEDGER["_meta"]["source_of_truth"])}. Rows so far: {len(LEDGER["rows"])}.</p>
</section>
<section class="block">
  <h2>Columns</h2>
  <div class="table-wrap">
  <table class="data">
    <thead><tr><th>Column</th><th>Meaning</th></tr></thead>
    <tbody>{cols}</tbody>
  </table>
  </div>
  <p class="small muted">No row is shown because no authorized report has been obtained. Commission record basis: <a href="https://affiliate-program.amazon.com/help/operating/policies">Commission Income Statement</a>.</p>
</section>"""
    page("campaigns/index.html", "Campaign ledger — empty by design",
         "The campaign ledger has no rows. Rows are added only from authorized first-party reports.",
         body)

    # ---- disclosure page ----
    body = f"""<section class="page-head">
  <p class="kicker"><a href="../index.html">Shop home</a> / Disclosure</p>
  <h1>Affiliate disclosure</h1>
</section>
<section class="block prose">
  <p class="disclosure-box"><strong>{e(DISCLOSURE)}</strong></p>
  <p>This sentence is the wording in Section 5 of the <a href="https://affiliate-program.amazon.com/help/operating/agreement">Associates Program Operating Agreement</a>, which asks for it to be stated clearly and prominently on the site.</p>
  <p>Links marked <em>Sponsored</em> lead to Amazon product pages and are marked <code>rel="sponsored"</code>, as <a href="https://developers.google.com/search/docs/crawling-indexing/qualify-outbound-links">Google's guidance</a> describes for paid links.</p>
  <p>The <a href="https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers">FTC's guidance</a> asks that a relationship be disclosed where it is hard to miss, placed with the endorsement itself. The disclosure is therefore shown under the masthead, next to each product table, and in the footer.</p>
</section>"""
    page("disclosure/index.html", "Affiliate disclosure — Zone3 Kitchen",
         "The Amazon Associates disclosure used on this site, with the sponsored-link rule and the FTC guidance it follows.",
         body)


# ---- sitemap ------------------------------------------------------------

def sitemap_urls() -> list[str]:
    urls = []
    for path in PAGES:
        url = canonical(path)
        urls.append(url)
    return urls


def write_sitemap(check_only: bool) -> list[str]:
    text = SITEMAP.read_text(encoding="utf-8")
    existing = set(re.findall(r"<loc>([^<]+)</loc>", text))
    missing = [u for u in sitemap_urls() if u not in existing]
    if missing and not check_only:
        add = "".join(f"  <url><loc>{e(u)}</loc></url>\n" for u in missing)
        text = text.replace("</urlset>", add + "</urlset>")
        SITEMAP.write_text(text, encoding="utf-8")
    return missing


# ---- writing ------------------------------------------------------------

CSS = """/* Zone3 Kitchen shop: publication layout, no build step. */
:root{--ink:#1d211e;--muted:#5d6661;--paper:#faf8f3;--card:#ffffff;--line:#e3ded2;--accent:#1f6b55;--accent-2:#0f3d31;--warn-bg:#fff1c9;--warn-ink:#6b4a00;--disc-bg:#f4efe1;--disc-line:#d9cfb4;--radius:10px;--max:1080px;}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--paper);color:var(--ink);font:17px/1.6 system-ui,-apple-system,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif}
a{color:var(--accent-2)}
a:focus-visible,.btn:focus-visible,.btn-ghost:focus-visible{outline:3px solid #f2b705;outline-offset:2px}
.wrap{max-width:var(--max);margin:0 auto;padding:0 20px}
.skip{position:absolute;left:-999px}
.skip:focus{left:12px;top:8px;background:#fff;padding:6px 10px;z-index:9}
.masthead{background:var(--accent-2);color:#fff}
.masthead-row{display:flex;flex-wrap:wrap;align-items:baseline;justify-content:space-between;gap:6px 16px;padding-top:18px;padding-bottom:6px}
.brand{font:700 1.5rem/1.2 Georgia,"Times New Roman",serif;color:#fff;text-decoration:none;letter-spacing:.01em}
.tagline{font-size:.9rem;color:#cfe3dc}
.topnav{display:flex;flex-wrap:wrap;gap:4px 4px;padding-top:6px;padding-bottom:14px}
.topnav a{color:#e7f2ee;text-decoration:none;padding:6px 10px;border-radius:999px;font-size:.92rem}
.topnav a:hover{background:rgba(255,255,255,.12)}
.topnav a.active{background:#fff;color:var(--accent-2);font-weight:600}
.disclosure{font-size:.95rem;border-bottom:1px solid var(--disc-line)}
.disclosure-top{background:var(--disc-bg);padding:10px 0}
.disclosure-top .wrap{color:var(--ink)}
.disclosure-inline{background:var(--disc-bg);border:1px solid var(--disc-line);border-radius:var(--radius);padding:10px 14px;margin:18px auto;max-width:var(--max);font-size:.95rem}
.disclosure-box{background:var(--disc-bg);border:1px solid var(--disc-line);border-radius:var(--radius);padding:14px 18px;font-size:1.05rem}
main{padding-top:28px;padding-bottom:28px;min-height:60vh}
.hero{padding:8px 0 10px}
.hero h1,.page-head h1{font:700 2.2rem/1.2 Georgia,"Times New Roman",serif;margin:.2rem 0 .5rem;letter-spacing:-.01em}
.page-head{padding:6px 0 4px}
.kicker{font-size:.8rem;text-transform:uppercase;letter-spacing:.08em;color:var(--accent);font-weight:700;margin:0 0 6px}
.kicker a{color:var(--accent)}
.lede{font-size:1.08rem;color:var(--muted);max-width:70ch;margin:.2rem 0 0}
.block{margin:30px 0}
.block h2{font:700 1.35rem/1.3 Georgia,"Times New Roman",serif;margin:0 0 12px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:16px}
.card{background:var(--card);border:1px solid var(--line);border-radius:var(--radius);padding:18px;display:flex;flex-direction:column;gap:6px}
.card h3{font-size:1.02rem;line-height:1.35;margin:0;font-weight:650;display:-webkit-box;-webkit-line-clamp:4;-webkit-box-orient:vertical;overflow:hidden}
.card .meta{color:var(--muted);font-size:.88rem;margin:0}
.card-cta{margin:auto 0 0;display:flex;flex-wrap:wrap;gap:8px;align-items:center;padding-top:8px}
.btn{display:inline-block;background:var(--accent);color:#fff!important;text-decoration:none;padding:10px 16px;border-radius:8px;font-weight:600;font-size:.95rem;min-height:44px;line-height:24px}
.btn:hover{background:var(--accent-2)}
.btn-ghost{display:inline-block;border:1px solid var(--accent-2);color:var(--accent-2);text-decoration:none;padding:9px 14px;border-radius:8px;margin:0 8px 8px 0;min-height:44px;line-height:24px}
.btn-ghost:hover{background:var(--accent-2);color:#fff}
.sponsored-tag{font-size:.75rem;text-transform:uppercase;letter-spacing:.06em;color:var(--muted);border:1px solid var(--line);border-radius:4px;padding:2px 6px}
.tiles{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:16px}
.tile{display:flex;flex-direction:column;gap:4px;background:var(--card);border:1px solid var(--line);border-radius:var(--radius);padding:20px;text-decoration:none;color:var(--ink)}
.tile:hover{border-color:var(--accent)}
.tile-count{font-size:.8rem;color:var(--accent);font-weight:700;text-transform:uppercase;letter-spacing:.06em}
.tile-title{font:700 1.2rem/1.3 Georgia,"Times New Roman",serif}
.tile-blurb{color:var(--muted);font-size:.95rem}
.status{background:var(--card);border:1px solid var(--line);border-radius:var(--radius);padding:18px 20px}
.status h2{margin-top:0}
.actions{margin:12px 0 0}
.table-wrap{overflow-x:auto;background:var(--card);border:1px solid var(--line);border-radius:var(--radius)}
table.data{border-collapse:collapse;width:100%;font-size:.93rem}
table.data.wide{min-width:1100px}
table.data th,table.data td{text-align:left;vertical-align:top;padding:10px 12px;border-bottom:1px solid var(--line)}
table.data th{background:#f1eee6;font-size:.82rem;text-transform:uppercase;letter-spacing:.04em;color:#3c4640;position:sticky;top:0}
table.data tr:last-child td{border-bottom:0}
table.data td a{word-break:break-word}
.pill{display:inline-block;font-size:.8rem;border-radius:999px;padding:2px 10px;font-weight:600}
.pill-warn{background:var(--warn-bg);color:var(--warn-ink)}
.muted{color:var(--muted)}
.small{font-size:.86rem}
code{font:.9em ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;background:#efece4;padding:1px 5px;border-radius:4px}
.opts{margin:0;padding-left:18px}
.opts li{margin-bottom:6px}
.prose{max-width:72ch}
.prose h2{margin-top:24px}
.site-footer{background:#e9e5d9;border-top:1px solid var(--line);padding:26px 0 34px;margin-top:20px}
.foot-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:22px;margin-top:18px}
.foot-title{font-weight:700;margin:0 0 6px}
.foot-links{list-style:none;padding:0;margin:0;columns:1}
.foot-links li{margin:2px 0}
.disclosure-footer{border:0;background:transparent;padding:0;margin:0}
@media (max-width:640px){.hero h1,.page-head h1{font-size:1.7rem}.tagline{display:none}body{font-size:16px}}
"""


def write_all() -> None:
    SHOP.mkdir(exist_ok=True)
    (SHOP / "assets").mkdir(exist_ok=True)
    (SHOP / "assets" / "shop.css").write_text(CSS, encoding="utf-8")
    for path, rec in PAGES.items():
        out = SHOP / path
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(render(path, rec), encoding="utf-8")


# ---- checks -------------------------------------------------------------

class PageScan(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.anchors: list[dict] = []
        self.text_chunks: list[str] = []
        self.in_table = 0
        self.tables: list[dict] = []
        self._cur_row = None
        self._cur_table = None
        self._in_tbody = False
        self._cur_anchor = None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "table":
            self._cur_table = {"rows": [], "head": True, "rule": a.get("data-rule")}
            self.tables.append(self._cur_table)
            self.in_table += 1
        elif tag == "tbody":
            self._in_tbody = True
            if self._cur_table is not None:
                self._cur_table["head"] = False
        elif tag == "tr":
            self._cur_row = {"anchors": [], "in_tbody": self._in_tbody}
            if self._cur_table is not None:
                self._cur_table["rows"].append(self._cur_row)
        elif tag == "a":
            rec = {"href": a.get("href", ""), "rel": a.get("rel", "") or "", "text": ""}
            self.anchors.append(rec)
            self._cur_anchor = rec
            if self._cur_row is not None:
                self._cur_row["anchors"].append(rec)

    def handle_endtag(self, tag):
        if tag == "table":
            self.in_table -= 1
            self._cur_table = None
        elif tag == "tbody":
            self._in_tbody = False
        elif tag == "tr":
            self._cur_row = None
        elif tag == "a":
            self._cur_anchor = None

    def handle_data(self, data):
        self.text_chunks.append(data)
        if self._cur_anchor is not None:
            self._cur_anchor["text"] += data


PRICE_RE = re.compile(r"[$£€]\s?\d|\d(?:\.\d+)?\s?(?:out of|★|stars?\b)", re.I)


def check_all(paths: list[str]) -> list[str]:
    problems: list[str] = []
    # product record rules
    for p in PRODUCTS["products"]:
        if not re.fullmatch(r"https://link\.amazon/[A-Za-z0-9]+", p["submitted_link"]):
            problems.append(f"{p['id']}: submitted link is not a link.amazon short link")
        if not re.fullmatch(r"[A-Z0-9]{10}", p["observed_redirect_asin"]):
            problems.append(f"{p['id']}: observed ASIN is not 10 characters")
        if p["observed_redirect_listing_url"] != p["source_url"]:
            problems.append(f"{p['id']}: observed listing URL and source URL differ")
        if p["intended_asin"]:
            for k in ("official_listing_url", "intent_confirmed_on", "intent_confirmation_source"):
                if not p[k]:
                    problems.append(f"{p['id']}: intended ASIN set without {k}")
        if p["intended_asin"] and p["intended_asin"] == p["observed_redirect_asin"] and not p["intent_confirmation_source"]:
            problems.append(f"{p['id']}: observed ASIN copied into intended field without confirmation")
    # the 9-character token count stated in the findings must match the data
    for p in PRODUCTS["products"]:
        token = p["submitted_link"].rsplit("/", 1)[-1]
        if len(token) != 9:
            problems.append(f"{p['id']}: submitted token is {len(token)} characters; findings say 9")
    # the intent field must not be filled from redirects in this build
    for p in PRODUCTS["products"]:
        if p["intended_asin"]:
            problems.append(f"{p['id']}: intended ASIN is filled; this build expects blank until confirmed")
    # source register: every row has an https url
    for s in SOURCES["sources"]:
        if not s["url"].startswith("https://"):
            problems.append(f"{s['id']}: source url is not https")
    for f in FLAGS["flags"]:
        if not f["sources"]:
            problems.append(f"{f['id']}: flag has no source link")
        for s in f["sources"]:
            if not s["url"].startswith("https://"):
                problems.append(f"{f['id']}: source url is not https")

    existing_paths = set()
    all_files = []
    for path in paths:
        fp = SHOP / path
        if not fp.exists():
            problems.append(f"{path}: missing file")
            continue
        existing_paths.add(path)
        all_files.append(path)
    for path in all_files:
        text = (SHOP / path).read_text(encoding="utf-8")
        scan = PageScan()
        scan.feed(text)
        # disclosure: exact sentence at least twice (masthead strip and footer)
        n = text.count(html.escape(DISCLOSURE, quote=False))
        if n < 2:
            problems.append(f"{path}: disclosure sentence appears {n} time(s); needs at least 2")
        # sponsored rule on Amazon links
        for a in scan.anchors:
            href = a["href"]
            host = re.sub(r"^https?://([^/]+).*", r"\1", href) if href.startswith("http") else ""
            if host in SPONSORED_HOSTS and "sponsored" not in a["rel"].split():
                problems.append(f"{path}: Amazon link without rel=sponsored: {href}")
            if host in SPONSORED_HOSTS and "noopener" not in a["rel"].split():
                problems.append(f"{path}: Amazon link without noopener: {href}")
            if href.startswith("http") and host not in OFFICIAL_HOSTS:
                problems.append(f"{path}: outbound link to non-official host: {href}")
            if "tag=" in href:
                problems.append(f"{path}: tracking tag embedded in a link (not permitted in this build): {href}")
            # internal links resolve
            if not href.startswith(("http", "mailto:", "#")):
                target = (SHOP / path).parent / href.split("#")[0]
                if href.startswith("../index.html"):
                    target = (SHOP / path).parent / href
                if href.split("#")[0] and not target.resolve().exists():
                    problems.append(f"{path}: broken internal link {href}")
        # price / rating patterns
        visible = " ".join(scan.text_chunks)
        m = PRICE_RE.search(visible)
        if m:
            problems.append(f"{path}: price or rating pattern found: {m.group(0)!r}")
        # table rows: each body row needs an https source link
        for t in scan.tables:
            if t.get("rule") != "source":
                continue
            for r in t["rows"]:
                if not r["in_tbody"]:
                    continue
                hrefs = [a["href"] for a in r["anchors"] if a["href"].startswith("https://")]
                if not hrefs:
                    problems.append(f"{path}: table row without an https source link")
    # sitemap
    sm = SITEMAP.read_text(encoding="utf-8")
    for path in paths:
        if canonical(path) not in sm:
            problems.append(f"sitemap.xml: missing {canonical(path)}")
    return problems


def main() -> int:
    check_only = "--check" in sys.argv
    build_pages()
    if not check_only:
        write_all()
        added = write_sitemap(check_only=False)
        if added:
            print(f"sitemap: added {len(added)} URL(s)")
    else:
        pass
    problems = check_all(list(PAGES.keys()))
    if problems:
        print("FAILED checks:")
        for p in problems:
            print("  -", p)
        return 1
    print(f"OK: {len(PAGES)} pages; disclosure, sponsored links, source rows, sitemap and links all pass.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
