#!/usr/bin/env python3
"""Generate the static GitHub Pages site from data/*.json.

Every product row is rendered from data/products.json. Any value that is null
(not confirmed from an official source) is rendered as a blank cell marked
"Unverified" — values are never inferred or filled in.
"""
import html
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
products_doc = json.loads((DATA / "products.json").read_text(encoding="utf-8"))
sources_doc = json.loads((DATA / "sources.json").read_text(encoding="utf-8"))
flags_doc = json.loads((DATA / "flags.json").read_text(encoding="utf-8"))

PRODUCTS = products_doc["products"]
SOURCES = {s["id"]: s for s in sources_doc["sources"]}
FLAGS = {f["id"]: f for f in flags_doc["flags"]}
RETRIEVED = products_doc["retrieved"]
DISCLOSURE = "As an Amazon Associate I earn from qualifying purchases."
CATEGORY = products_doc["category"]

VERIFIED_FIELDS = ["title", "brand", "capacity", "category", "asin"]
UNVERIFIED_FIELDS = ["price", "rating", "review_count", "availability", "commission_rate"]
FIELD_LABEL = {
    "title": "Title", "brand": "Brand", "capacity": "Capacity", "category": "Category",
    "asin": "ASIN", "price": "Price", "rating": "Rating", "review_count": "Review count",
    "availability": "Availability", "commission_rate": "Commission rate",
}


def esc(v):
    return html.escape(str(v), quote=True)


def badge_unverified():
    return '<span class="badge unv">Unverified</span>'


def cell(value):
    """Render a verified value, or a blank 'Unverified' cell if None."""
    if value is None:
        return '<td class="blank">' + badge_unverified() + "</td>"
    return "<td>" + esc(value) + "</td>"


def src_links(ids):
    out = []
    for sid in ids:
        s = SOURCES[sid]
        out.append(f'<a href="{esc(s["url"])}" target="_blank" rel="noopener">{esc(sid)} ↗</a>')
    return " · ".join(out) if out else "—"


def flag_links(ids):
    return " ".join(f'<a class="flagref" href="{{P}}flagged.html#{esc(i)}">{esc(i)}</a>' for i in ids) or "—"


def page(title, body, prefix="", active=""):
    nav_items = [
        ("index.html", "Dashboard", "home"),
        ("categories/home-kitchen-air-fryers.html", "Home & Kitchen › Air Fryers", "cat"),
        ("analysis.html", "Analysis & Findings", "analysis"),
        ("flagged.html", "Flagged for Review", "flagged"),
        ("sources.html", "Sources", "sources"),
    ]
    nav = "".join(
        f'<a href="{prefix}{href}" class="{"on" if key == active else ""}">{esc(label)}</a>'
        for href, label, key in nav_items
    )
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)} · Zone3 Affiliate Dashboard</title>
<link rel="stylesheet" href="{prefix}assets/style.css">
</head>
<body>
<header class="top">
  <div class="brand"><a href="{prefix}index.html">Zone3</a><span>Amazon affiliate dashboard</span></div>
  <nav>{nav}</nav>
</header>
<main>
{body}
</main>
<footer>
  <p class="disclosure"><strong>Affiliate disclosure:</strong> {esc(DISCLOSURE)} Links on this site may earn a commission on qualifying purchases. This disclosure is required by the Amazon Associates Operating Agreement, Section 5 (<a href="https://affiliate-program.amazon.com/help/operating/agreement" target="_blank" rel="noopener">source</a>).</p>
  <p>Data retrieved {esc(RETRIEVED)} from official sources only. Blank cells are unverified and are listed on the <a href="{prefix}flagged.html">Flagged for Review</a> page. Prices and ratings change; check the live Amazon listing.</p>
</footer>
<script src="{prefix}assets/app.js"></script>
</body>
</html>
"""


def product_table():
    rows = []
    for i, p in enumerate(PRODUCTS, 1):
        rows.append(f"""<tr>
<td>{esc(p['id'])}</td>
<td class="ptitle"><a href="{esc(p['product_url'])}" target="_blank" rel="noopener">{esc(p['title'])}</a><div class="small">Short link: <a href="{esc(p['short_link'])}" target="_blank" rel="noopener">{esc(p['short_link'])} ↗</a></div></td>
{cell(p['brand'])}{cell(p['capacity'])}{cell(p['category'])}{cell(p['asin'])}
{cell(p['price'])}{cell(p['rating'])}{cell(p['review_count'])}{cell(p['availability'])}{cell(p['commission_rate'])}
<td class="small">{src_links(p['source_ids'])}</td>
<td class="small">{flag_links(p['flags'])}</td>
</tr>""")
    return f"""<div class="tablewrap"><table class="data" id="products">
<thead><tr>
<th>ID</th><th>Product (title as listed)</th><th>Brand</th><th>Capacity</th><th>Category</th><th>ASIN</th>
<th>Price</th><th>Rating</th><th>Reviews</th><th>Availability</th><th>Commission rate</th>
<th>Official source(s)</th><th>Flags</th>
</tr></thead>
<tbody>
{''.join(rows)}
</tbody></table></div>"""


def claims_table():
    rows = []
    for p in PRODUCTS:
        for c in p["listing_claims"]:
            rows.append(f"<tr><td>{esc(p['id'])} · {esc(p['brand'])} {esc(p['capacity'])}</td><td>{esc(c)}</td><td class=\"small\">{src_links(p['source_ids'][:1])}</td></tr>")
    return f"""<div class="tablewrap"><table class="data">
<thead><tr><th>Product</th><th>Claim printed on the listing (not independently tested)</th><th>Source</th></tr></thead>
<tbody>{''.join(rows)}</tbody></table></div>"""


def build_index():
    body = f"""
<section class="hero">
  <h1>Amazon affiliate dashboard</h1>
  <p>Three supplied Amazon products, verified line by line against Amazon and FTC sources. Anything not confirmed is left blank and flagged.</p>
</section>

<section class="kpis">
  <div class="kpi"><div class="num">{len(PRODUCTS)}</div><div>products in 1 category</div></div>
  <div class="kpi"><div class="num">{len(PRODUCTS) * len(VERIFIED_FIELDS)}</div><div>verified product fields</div></div>
  <div class="kpi warn"><div class="num">{len(PRODUCTS) * len(UNVERIFIED_FIELDS)}</div><div>unverified fields (blank)</div></div>
  <div class="kpi warn"><div class="num">{len(FLAGS)}</div><div>items flagged for review</div></div>
</section>

<section class="card">
  <h2>Executive summary</h2>
  <ul class="summary">
    <li><strong>What was reviewed.</strong> Three Amazon links were supplied. All three resolve to Amazon.com air fryer / multi-cooker listings in the Home &amp; Kitchen category. The titles, brands, capacities and ASINs were confirmed from the redirected pages.</li>
    <li><strong>What is verified.</strong> Product title, brand, capacity, category and ASIN for each product (see the <a href="categories/home-kitchen-air-fryers.html">category table</a>). The Amazon Associates disclosure wording and the FTC disclosure standard were confirmed from official pages.</li>
    <li><strong>What is not verified.</strong> Price, rating, review count, availability, and the Kitchen commission rate. Amazon's product pages and the official rate schedule could not be read in this session, so these cells are blank.</li>
    <li><strong>Key irregularities.</strong> The short-link codes are not the ASINs they resolve to. The resolved links carry no Associate tag. The owner's Associates country and eligibility for US listings are unconfirmed. Details are on the <a href="flagged.html">Flagged for Review</a> page.</li>
    <li><strong>Scope.</strong> This is a verified static dashboard for the three supplied products. The automated research, live pricing, content generation and click tracking described in the brief are not built, because no verified data source for them was accessible. See flag F7.</li>
  </ul>
</section>

<section class="grid2">
  <a class="card linkcard" href="categories/home-kitchen-air-fryers.html">
    <h3>Home &amp; Kitchen › Air Fryers</h3>
    <p>The full product table with ASIN, source links and unverified fields.</p>
  </a>
  <a class="card linkcard" href="analysis.html">
    <h3>Analysis &amp; Findings</h3>
    <p>What the verified data shows, what it cannot show, and the verification log.</p>
  </a>
  <a class="card linkcard warnlink" href="flagged.html">
    <h3>Flagged for Review</h3>
    <p>Irregularities and unverified items, each with its source link and a requested action.</p>
  </a>
  <a class="card linkcard" href="sources.html">
    <h3>Sources</h3>
    <p>Every official source used, with what was verified from each.</p>
  </a>
</section>
"""
    return page("Dashboard", body, "", "home")


def build_category():
    body = f"""
<nav class="crumbs"><a href="../index.html">Dashboard</a> › {esc(CATEGORY['name'])}</nav>
<h1>Home &amp; Kitchen › Air Fryers</h1>
<p class="lede">Products supplied for this site. A blank cell with an <span class="badge unv">Unverified</span> label has no value confirmed from an official source. Click a source link to check it yourself.</p>

<section class="card">
  <h2>Product table</h2>
  {product_table()}
  <p class="small">Verified fields: title, brand, capacity, category, ASIN (from the Amazon redirect or product URL). Unverified: price, rating, review count, availability, commission rate. Commission is calculated as a percentage of qualifying revenue under the Amazon Associates Commission Income Statement, and no commission figure is shown here because the official rate schedule could not be read.</p>
</section>

<section class="card">
  <h2>Listing claims</h2>
  <p>These claims are printed in the listing titles. They were not tested.</p>
  {claims_table()}
</section>

<section class="card">
  <h2>Comparison (verified fields only)</h2>
  <div class="tablewrap"><table class="data">
    <thead><tr><th>ID</th><th>Brand</th><th>Capacity</th><th>Type (from title)</th><th>Price</th></tr></thead>
    <tbody>
      <tr><td>P1</td><td>CHEFMAN</td><td>6 Quart</td><td>Dual-basket air fryer oven</td><td class="blank">{badge_unverified()}</td></tr>
      <tr><td>P2</td><td>Emeril Lagasse</td><td>26QT</td><td>French-door multi-function air fryer toaster oven</td><td class="blank">{badge_unverified()}</td></tr>
      <tr><td>P3</td><td>Chefman</td><td>8 Qt</td><td>4-in-1 air fryer (TurboFry)</td><td class="blank">{badge_unverified()}</td></tr>
    </tbody>
  </table></div>
  <p class="small">Type is taken from the listing title. Capacity is shown in the unit printed on each listing (Qt or QT); the units were not converted.</p>
</section>
"""
    return page("Home & Kitchen › Air Fryers", body, "../", "cat")


def build_analysis():
    unv_cells = len(PRODUCTS) * len(UNVERIFIED_FIELDS)
    ver_cells = len(PRODUCTS) * len(VERIFIED_FIELDS)
    rows = []
    for k in VERIFIED_FIELDS:
        rows.append(f'<tr><td>{esc(FIELD_LABEL[k])}</td><td><span class="badge ok">Verified</span></td><td>{len(PRODUCTS)} of {len(PRODUCTS)}</td></tr>')
    for k in UNVERIFIED_FIELDS:
        rows.append(f'<tr><td>{esc(FIELD_LABEL[k])}</td><td><span class="badge unv">Unverified</span></td><td>0 of {len(PRODUCTS)}</td></tr>')
    body = f"""
<nav class="crumbs"><a href="index.html">Dashboard</a> › Analysis &amp; Findings</nav>
<h1>Analysis &amp; Findings</h1>
<p class="lede">Only findings supported by a verified source are listed. Where the data cannot support a conclusion, this page says so.</p>

<section class="kpis">
  <div class="kpi"><div class="num">{ver_cells}</div><div>verified cells</div></div>
  <div class="kpi warn"><div class="num">{unv_cells}</div><div>unverified cells (blank)</div></div>
</section>

<section class="card">
  <h2>Findings</h2>
  <ol class="findings">
    <li><strong>All three supplied products are air fryers or air-fryer ovens.</strong> Titles state this for P1, P2, and P3 (<a href="{esc(PRODUCTS[0]['product_url'])}" target="_blank" rel="noopener">P1 ↗</a>, <a href="{esc(PRODUCTS[1]['product_url'])}" target="_blank" rel="noopener">P2 ↗</a>, <a href="{esc(PRODUCTS[2]['product_url'])}" target="_blank" rel="noopener">P3 ↗</a>).</li>
    <li><strong>Two brands, one category.</strong> Two brands (CHEFMAN/Chefman ×2, Emeril Lagasse ×1) and one category, Home &amp; Kitchen, appear on the listings.</li>
    <li><strong>Sizes differ widely.</strong> Printed capacities are 6 Quart, 26QT and 8 Qt. The 26QT model is a French-door multi-function oven, not a basket fryer.</li>
    <li><strong>Commission potential cannot be calculated.</strong> Commission = qualifying revenue × category rate, and the Commission Income Statement says rates are a percentage of qualifying revenue (<a href="https://affiliate-program.amazon.com/help/operating/policies" target="_blank" rel="noopener">source ↗</a>). Price and the Kitchen rate are both unverified, so no dollar figure is given.</li>
    <li><strong>Demand, trend and competition were not measured.</strong> No verified sales-rank, search-volume or review-count data was accessible. These findings are left blank rather than estimated.</li>
    <li><strong>Attribution is not yet in place.</strong> The resolved links carry no Associate tag (flag F2). Until tagged links are created, no commission can be attributed to an account.</li>
  </ol>
</section>

<section class="card">
  <h2>Verification log</h2>
  <p>Each row is a field type across the three products. "Verified" means the value was read from an official Amazon page or policy page.</p>
  <div class="tablewrap"><table class="data">
    <thead><tr><th>Field</th><th>Status</th><th>Products verified</th></tr></thead>
    <tbody>{''.join(rows)}</tbody>
  </table></div>
</section>

<section class="card">
  <h2>Compliance checklist</h2>
  <ul>
    <li><span class="badge ok">Verified</span> Associates disclosure "As an Amazon Associate I earn from qualifying purchases." must appear on the site (Operating Agreement, Section 5) — <a href="https://affiliate-program.amazon.com/help/operating/agreement" target="_blank" rel="noopener">S7 ↗</a>. It is in every page footer.</li>
    <li><span class="badge ok">Verified</span> FTC: disclose any material connection, including affiliate relationships, placed with the endorsement and hard to miss (FTC Disclosures 101) — <a href="https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers" target="_blank" rel="noopener">S10 ↗</a>.</li>
    <li><span class="badge unv">Unverified</span> Commission rates and the Associates country eligibility — see flags F3 and F5.</li>
  </ul>
</section>
"""
    return page("Analysis & Findings", body, "", "analysis")


def build_flagged():
    rows = []
    for f in flags_doc["flags"]:
        src = src_links(f["sources"]) if f["sources"] else "—"
        rows.append(f"""<tr id="{esc(f['id'])}">
<td><strong>{esc(f['id'])}</strong></td>
<td><span class="badge {'warn' if f['type'] in ('Irregularity', 'Scope gap') else 'unv'}">{esc(f['type'])}</span></td>
<td>{esc(f['item'])}</td>
<td>{esc(f['detail'])}</td>
<td class="small">{src}</td>
<td>{esc(f['action'])}</td>
</tr>""")
    body = f"""
<nav class="crumbs"><a href="index.html">Dashboard</a> › Flagged for Review</nav>
<h1>Flagged for Review</h1>
<p class="lede">These items are published for owner review. They do not block the site. Each item links to the source it relates to, and each has a requested action.</p>
<section class="card">
  <div class="tablewrap"><table class="data">
    <thead><tr><th>ID</th><th>Type</th><th>Item</th><th>Detail</th><th>Source(s)</th><th>Requested action</th></tr></thead>
    <tbody>{''.join(rows)}</tbody>
  </table></div>
</section>
<section class="card">
  <h2>Unverified reference (not used in any table)</h2>
  <p>Secondary, non-official sites report a 4.5% Kitchen commission rate. They are listed here only so the owner can compare them against the official schedule. They are not official sources and are not used anywhere on the site.</p>
  <ul>
    <li><a href="https://geniuslink.com/blog/amazon-affiliate-commission-rates-historical-guide/" target="_blank" rel="noopener">geniuslink.com — historical rate guide ↗</a> (non-official)</li>
    <li><a href="https://sellersonar.com/blog/amazon-affiliate-program/" target="_blank" rel="noopener">sellersonar.com — rates guide ↗</a> (non-official)</li>
  </ul>
</section>
"""
    return page("Flagged for Review", body, "", "flagged").replace("{P}", "")


def build_sources():
    rows = []
    for s in sources_doc["sources"]:
        rows.append(f"""<tr>
<td><strong>{esc(s['id'])}</strong></td>
<td>{esc(s['title'])}</td>
<td class="small"><a href="{esc(s['url'])}" target="_blank" rel="noopener">{esc(s['url'])} ↗</a></td>
<td>{esc(s['publisher'])}</td>
<td>{esc(s['verified'])}</td>
<td><span class="badge {'ok' if s['status'].startswith('Fetched') and 'partial' not in s['status'] else 'unv'}">{esc(s['status'])}</span></td>
</tr>""")
    body = f"""
<nav class="crumbs"><a href="index.html">Dashboard</a> › Sources</nav>
<h1>Sources</h1>
<p class="lede">Retrieved {esc(RETRIEVED)}. Every row links to the official page it describes. Retrieval status shows what could actually be read.</p>
<section class="card">
  <div class="tablewrap"><table class="data">
    <thead><tr><th>ID</th><th>Source</th><th>URL</th><th>Publisher</th><th>What was verified</th><th>Status</th></tr></thead>
    <tbody>{''.join(rows)}</tbody>
  </table></div>
</section>
"""
    return page("Sources", body, "", "sources")


def main():
    out = {
        ROOT / "index.html": build_index(),
        ROOT / "categories" / "home-kitchen-air-fryers.html": build_category(),
        ROOT / "analysis.html": build_analysis(),
        ROOT / "flagged.html": build_flagged(),
        ROOT / "sources.html": build_sources(),
    }
    for path, text in out.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        print("wrote", path.relative_to(ROOT))
    # flag references inside product rows point to flagged.html#Fx
    for path in out:
        p = path
        t = p.read_text(encoding="utf-8")
        if "{P}" in t:
            p.write_text(t.replace("{P}", "../" if p.parent != ROOT else ""), encoding="utf-8")
    (ROOT / ".nojekyll").write_text("", encoding="utf-8")


if __name__ == "__main__":
    main()
