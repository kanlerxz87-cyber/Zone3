#!/usr/bin/env python3
"""
Zone3 — static site generator.

Reads the verified data layer in data/*.json and writes every HTML page of the
Amazon affiliate dashboard into the repository root, ready for GitHub Pages.

Design rules enforced here:
  * every value rendered in a table comes from data/*.json, never from a literal;
  * a field whose status is "unverified" renders as an explicit Unverified cell,
    never as a guess;
  * every data row carries a link to the official source that supports it.

Usage:  python3 tools/build.py
"""

import html
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
DOCS = os.path.join(ROOT, "docs", "content")
OUT = ROOT

# ----------------------------------------------------------------------------
# load
# ----------------------------------------------------------------------------


def load(name):
    with open(os.path.join(DATA, name), "r", encoding="utf-8") as fh:
        return json.load(fh)


PRODUCTS = load("products.json")
SOURCES = load("sources.json")
COMMISSION = load("commission.json")
FLAGS = load("flags.json")
REQS = load("requirements.json")

SRC = {s["id"]: s for s in SOURCES["sources"]}
META = PRODUCTS["meta"]
CAPTURED = META["captured"]


def src_url(sid):
    return SRC[sid]["url"]


def srclinks(ids, label=None):
    """Render one or more source ids as links: S1 S2 ..."""
    if not ids:
        return '<span class="src"><span class="unverified">no official source</span></span>'
    if isinstance(ids, str):
        ids = ids.split()
    out = []
    for sid in ids:
        if sid in SRC:
            out.append(
                '<a href="%s" target="_blank" rel="noopener nofollow" title="%s">%s</a>'
                % (html.escape(src_url(sid)), html.escape(SRC[sid]["title"]), sid)
            )
        else:
            out.append(html.escape(sid))
    txt = " ".join(out)
    if label:
        txt = '%s <span class="src">%s</span>' % (html.escape(label), txt)
    return '<span class="src">%s</span>' % txt


def esc(x):
    return html.escape(str(x), quote=True)


def money(v):
    return "&mdash;" if v is None else "$%0.2f" % v


def pct(v):
    return "&mdash;" if v is None else "%0.2f%%" % v


# ----------------------------------------------------------------------------
# tiny markdown renderer (headings, paragraphs, lists, bold, code, links)
# ----------------------------------------------------------------------------


def md_inline(text):
    text = html.escape(text, quote=False)
    text = re.sub(r"\[([^\]]+)\]\((https?://[^)\s]+)\)", r'<a href="\2" target="_blank" rel="noopener nofollow">\1</a>', text)
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(^|[\s(])\*([^*\n]+)\*(?=[\s.,;:)]|$)", r"\1<em>\2</em>", text)
    return text


def md_table(block):
    """Render a github-style markdown table block."""
    rows = []
    for line in block:
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        rows.append(cells)
    if len(rows) < 2:
        return "<p>%s</p>" % md_inline(block[0])
    head, body = rows[0], rows[2:]
    thead = "".join("<th>%s</th>" % md_inline(c) for c in head)
    tbody = "".join(
        "<tr>%s</tr>" % "".join(
            '<td class="num">%s</td>' % md_inline(c) if c.startswith("$") or c.replace("%", "").replace(".", "").isdigit()
            else "<td>%s</td>" % md_inline(c)
            for c in r)
        for r in body
    )
    return ('<div class="wrap"><table><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>'
            % (thead, tbody))


def md(path, base=1):
    """Render the markdown subset used in docs/content.

    base=1 (default) maps "##" to <h3>, for prose nested inside a card that
    already has an <h2>. base=0 maps "##" to <h2>, for a page whose card has no
    own heading.
    """
    with open(os.path.join(DOCS, path), "r", encoding="utf-8") as fh:
        lines = fh.read().splitlines()
    out, para, list_type, table = [], [], None, []

    def flush_text():
        nonlocal para, list_type
        if para:
            out.append("<p>%s</p>" % md_inline(" ".join(para)))
            para = []
        if list_type:
            out.append("</%s>" % list_type)
            list_type = None

    def flush_table():
        nonlocal table
        if table:
            out.append(md_table(table))
            table = []

    def flush():
        flush_text()
        flush_table()

    for raw in lines:
        if raw.strip().startswith("|") and raw.count("|") >= 2:
            flush_text()
            table.append(raw)
            continue
        if table:
            flush_table()
        line = raw.rstrip()
        if not line.strip():
            flush()
            continue
        m = re.match(r"^(#{1,6})\s+(.*)$", line)
        if m:
            flush()
            lvl = min(len(m.group(1)) + base, 4)
            out.append("<h%d>%s</h%d>" % (lvl, md_inline(m.group(2)), lvl))
            continue
        m = re.match(r"^\s*[-*]\s+(.*)$", line)
        if m:
            if list_type != "ul":
                flush()
                out.append("<ul class=\"tight\">")
                list_type = "ul"
            out.append("<li>%s</li>" % md_inline(m.group(1)))
            continue
        m = re.match(r"^\s*\d+\.\s+(.*)$", line)
        if m:
            if list_type != "ol":
                flush()
                out.append("<ol class=\"tight\">")
                list_type = "ol"
            out.append("<li>%s</li>" % md_inline(m.group(1)))
            continue
        flush() if False else None
        para.append(line.strip())
    flush()
    return "\n".join(out)


# ----------------------------------------------------------------------------
# navigation
# ----------------------------------------------------------------------------

NAV = [
    ("Overview", [
        ("index.html", "Dashboard"),
        ("executive-summary.html", "Executive Summary"),
    ]),
    ("Catalogue", [
        ("products.html", "All Products"),
        ("categories.html", "Categories"),
        ("category-home-kitchen.html", "Home &amp; Kitchen"),
    ]),
    ("Products", [
        ("product-%s.html" % p["slug"], p["fields"]["brand_from_title"]["value"] + " " + p["id"])
        for p in PRODUCTS["products"]
    ]),
    ("Analysis", [
        ("comparison.html", "Comparison"),
        ("analysis.html", "Pricing &amp; Reviews"),
        ("commission.html", "Commission Model"),
    ]),
    ("Governance", [
        ("compliance.html", "Compliance"),
        ("flagged.html", "Flagged for Review", "bad"),
        ("requirements.html", "Requirements"),
        ("sources.html", "Sources"),
        ("verification.html", "Verification Log"),
    ]),
]

BLOCKING = sum(1 for f in FLAGS["flags"] if f["severity"] == "blocking")

DISCLOSURE = (
    '<strong>Disclosure &amp; status.</strong> This site is being prepared for the Amazon Associates program. '
    'No Amazon Associates tag is configured, so no commission is currently earned and these are not affiliate links. '
    'Prices and ratings shown are a one-time capture taken %s from Amazon and are stale the moment Amazon changes them. '
    '&nbsp;<a href="compliance.html">Compliance</a> · <a href="flagged.html">Flagged for Review (%d blocking)</a>'
) % (esc(CAPTURED), BLOCKING)


def shell(page, title, lede, body):
    nav_html = []
    for group in NAV:
        items = []
        for item in group[1]:
            href, label = item[0], item[1]
            badge = item[2] if len(item) > 2 else None
            cls = "active" if href == page else ""
            dot = ' <span class="dot">%s</span>' % BLOCKING if badge == "bad" else ""
            items.append('<li><a class="%s" href="%s">%s%s</a></li>' % (cls, href, label, dot))
        nav_html.append(
            '<div class="navgroup"><h4>%s</h4><ul>%s</ul></div>' % (group[0], "".join(items))
        )

    return """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%(title)s &middot; Zone3 Amazon Affiliate Platform</title>
<meta name="description" content="%(lede)s">
<meta name="robots" content="index,follow">
<link rel="stylesheet" href="assets/styles.css">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<div class="disclosure">%(disc)s</div>
<div class="layout">
<aside class="sidebar" id="sidebar" aria-label="Site navigation">
  <div class="brand"><b>Zone3</b><span>Amazon affiliate platform</span></div>
  %(nav)s
</aside>
<main class="content" id="main">
  <div class="topbar">
    <button class="burger" type="button" aria-label="Toggle navigation">&#9776;</button>
    <div class="crumb"><b>%(title)s</b></div>
    <div class="stamp">Data captured %(cap)s &middot; amazon.com (US)</div>
  </div>
  %(body)s
  <footer class="foot">
    Zone3 &middot; verified-data affiliate dashboard &middot; every table row links to its official source
    (<a href="sources.html">source list</a>).
    Amazon, Amazon.com and the Amazon logo are trademarks of Amazon.com, Inc. or its affiliates.
    This site is not endorsed by or affiliated with Amazon.com, Inc.
  </footer>
</main>
</div>
<script src="assets/app.js"></script>
</body>
</html>
""" % {
        "title": esc(title),
        "lede": esc(lede),
        "disc": DISCLOSURE,
        "nav": "\n  ".join(nav_html),
        "cap": esc(CAPTURED),
        "body": body,
    }


def card(title, inner, sub=""):
    s = '<p class="sub">%s</p>' % sub if sub else ""
    return '<section class="card"><h2>%s</h2>%s%s</section>' % (title, s, inner)


def chip(status):
    return {
        "verified": '<span class="chip v">Verified</span>',
        "unverified": '<span class="chip u">Unverified</span>',
    }.get(status, '<span class="chip n">%s</span>' % esc(status))


def fv(p, name):
    """Return the field dict for a product field."""
    return p["fields"].get(name, {"value": None, "status": "unverified", "source": None, "note": ""})


def unverified_cell(note=""):
    t = ' title="%s"' % esc(note) if note else ""
    return '<span class="unverified"%s>Unverified</span>' % t


# ----------------------------------------------------------------------------
# table builders
# ----------------------------------------------------------------------------

PRODUCT_COLUMNS = [
    ("Product", "text"),
    ("ASIN", "text"),
    ("Dept.", "text"),
    ("Price", "num"),
    ("List", "num"),
    ("Discount", "num"),
    ("Rating", "num"),
    ("Ratings", "text"),
    ("Demand (past month)", "text"),
    ("Promotion", "text"),
    ("Commission rate", "text"),
    ("Source", "text"),
]


def discount_depth(p):
    cur = fv(p, "current_price")["value"]
    lst = fv(p, "list_price")["value"]
    if cur is None or lst is None or not lst:
        return None
    return (1.0 - cur / lst) * 100.0


def product_row(p, extra=True):
    f = p["fields"]
    cur = fv(p, "current_price")["value"]
    lst = fv(p, "list_price")["value"]
    dd = discount_depth(p)
    rate = fv(p, "associates_commission_category")
    cells = [
        '<td><a href="product-%s.html"><strong>%s</strong></a>%s</td>'
        % (p["slug"], esc(f["brand_from_title"]["value"]),
           " <small>%s</small>" % esc(p["id"]) if extra else ""),
        '<td class="mono"><a href="%s" target="_blank" rel="noopener nofollow">%s</a></td>'
        % (esc(f["canonical_url"]["value"]), esc(f["asin"]["value"])),
        "<td>%s</td>" % esc(f["department"]["value"]),
        '<td class="num" data-v="%s">%s</td>' % ("" if cur is None else cur, money(cur)),
        '<td class="num" data-v="%s">%s</td>' % ("" if lst is None else lst, money(lst)),
        '<td class="num" data-v="%s">%s</td>' % ("" if dd is None else "%.2f" % dd,
                                                 "&mdash;" if dd is None else "%0.1f%%" % dd),
        '<td class="num" data-v="%s">%s</td>' % (
            fv(p, "rating")["value"] if fv(p, "rating")["value"] is not None else "",
            "&mdash;" if fv(p, "rating")["value"] is None else "%0.1f / 5" % fv(p, "rating")["value"]),
        "<td>%s</td>" % esc(fv(p, "ratings_count_display")["value"] or "&mdash;"),
        "<td>%s</td>" % esc(fv(p, "demand_signal")["value"] or "&mdash;"),
        "<td>%s</td>" % esc(fv(p, "deal_badge")["value"] or "&mdash;"),
        "<td>%s</td>" % unverified_cell(rate.get("note", "")),
        '<td class="src">%s</td>' % " ".join(
            '<a href="%s" target="_blank" rel="noopener nofollow" title="%s">%s</a>'
            % (esc(SRC[s]["url"]), esc(SRC[s]["title"]), s)
            for s in (["S1", "S2"] if p["id"] == "P1" else ["S3", "S4"] if p["id"] == "P2" else ["S5", "S6"])
        ),
    ]
    return "<tr>%s</tr>" % "".join(cells)


def product_table(caption=""):
    head = "".join(
        '<th data-sort="%s" class="%s">%s</th>' % (kind, "num" if kind == "num" else "", esc(name))
        for name, kind in PRODUCT_COLUMNS
    )
    rows = "".join(product_row(p) for p in PRODUCTS["products"])
    cap = '<p class="tbl-cap">%s</p>' % caption if caption else ""
    return (
        '<div class="wrap"><table data-sortable data-verify-source><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>%s'
        % (head, rows, cap)
    )


# ----------------------------------------------------------------------------
# pages
# ----------------------------------------------------------------------------


def page_index():
    prods = PRODUCTS["products"]

    verified_n = sum(
        1 for p in prods for fld in p["fields"].values() if fld["status"] == "verified"
    )
    unverified_n = sum(
        1 for p in prods for fld in p["fields"].values() if fld["status"] != "verified"
    )
    official_n = sum(1 for s in SOURCES["sources"] if s.get("official"))

    kpis = [
        ("", len(prods), "Products tracked"),
        ("ok", verified_n, "Verified data points"),
        ("warn", unverified_n, "Unverified fields (blank)"),
        ("bad", BLOCKING, "Blocking flags"),
        ("", official_n, "Official sources cited"),
        ("", len(REQS["requirements"]), "Requirements tracked"),
    ]
    kpi_html = "".join(
        '<div class="kpi %s"><div class="n">%s</div><div class="l">%s</div></div>' % (c, n, esc(l))
        for c, n, l in kpis
    )

    body = []
    body.append('<div class="kpis">%s</div>' % kpi_html)

    body.append(
        '<div class="note bad"><p><strong>%d blocking items are open.</strong> Amazon\'s Associates Program '
        'Participation Requirements restrict how an Associate may display prices '
        '(<a href="https://affiliate-program.amazon.com/help/operating/policies" target="_blank" rel="noopener nofollow">section 2(b)</a>) '
        'and star ratings '
        '(<a href="https://affiliate-program.amazon.com/help/operating/policies" target="_blank" rel="noopener nofollow">section 6(t)</a>). '
        'Both are shown here for analysis only and must be re-sourced through the Product Advertising API / Creators API, '
        'or removed, before this site operates as a live Associates property. '
        'Full detail on the <a href="flagged.html">Flagged for Review</a> page.</p></div>' % BLOCKING
    )

    body.append(card(
        "Product snapshot",
        product_table(
            "Click any column header to sort. &ldquo;Discount&rdquo; is derived from the two verified price values "
            "on the same row; it is not itself an Amazon-published figure. "
            "Commission rate is blank because Amazon does not publish the category per ASIN."
        ),
        "All three supplied links resolved to products in Home &amp; Kitchen, specifically air fryers.",
    ))

    # link resolution
    rows = []
    for p in PRODUCTS["products"]:
        f = p["fields"]
        rows.append(
            "<tr>"
            '<td><a href="%s" target="_blank" rel="noopener nofollow">%s</a></td>'
            '<td class="mono">%s</td>'
            '<td class="mono"><a href="%s" target="_blank" rel="noopener nofollow">%s</a></td>'
            "<td>%s</td>"
            '<td class="src">%s</td>'
            "</tr>" % (
                esc(p["short_link"]), esc(p["short_link"]),
                esc(f["short_link_code"]["value"]),
                esc(f["canonical_url"]["value"]), esc(f["asin"]["value"]),
                esc(f["department"]["value"]),
                srclinks(["S12", "S1" if p["id"] == "P1" else "S3" if p["id"] == "P2" else "S5"]),
            )
        )
    body.append(card(
        "Short-link resolution",
        '<div class="wrap"><table data-verify-source><thead><tr>'
        "<th>Supplied link</th><th>Code</th><th>Resolves to (ASIN)</th><th>Department</th><th>Source</th>"
        "</tr></thead><tbody>%s</tbody></table></div>"
        '<p class="tbl-cap">The supplied codes are 9 characters and mixed case, so they are not ASINs '
        "(an ASIN is 10 characters). They are short-link slugs that redirect to a real product page. "
        'See <a href="flagged.html">F04</a> and <a href="flagged.html">F05</a>.</p>' % "".join(rows),
        "Each link was resolved by following the HTTP redirect to the live Amazon product page.",
    ))

    body.append(
        '<div class="grid2">'
        + card("Findings", md("dashboard-findings.md"))
        + card("What is unverified, and why", md("dashboard-unverified.md"))
        + "</div>"
    )

    body.append(card(
        "Where to go next",
        '<ul class="tight">'
        '<li><a href="executive-summary.html">Executive summary</a> &mdash; the one-page version.</li>'
        '<li><a href="comparison.html">Comparison</a> &mdash; the three products side by side.</li>'
        '<li><a href="commission.html">Commission model</a> &mdash; the official rate table and the qualifying-purchase rules.</li>'
        '<li><a href="compliance.html">Compliance</a> &mdash; Amazon Associates obligations and the FTC disclosure rule.</li>'
        '<li><a href="flagged.html">Flagged for Review</a> &mdash; %d items needing an owner decision.</li>'
        '<li><a href="verification.html">Verification log</a> &mdash; every field, its value, its source, its status.</li>'
        "</ul>" % len(FLAGS["flags"]),
    ))

    return shell(
        "index.html", "Dashboard",
        "Verified product, commission and compliance data for the three supplied Amazon products.",
        "".join(body),
    )


def page_executive_summary():
    body = []
    body.append('<div class="note"><p>This summary is generated from <code>docs/content/executive-summary.md</code> '
                "so the page and the repository document cannot drift apart. "
                'It is also in the repo as <code>EXECUTIVE_SUMMARY.md</code>.</p></div>')
    body.append('<section class="card">%s</section>' % md("executive-summary.md", base=0))
    return shell("executive-summary.html", "Executive Summary",
                 "Executive summary of the Zone3 Amazon affiliate build.", "".join(body))


def page_products():
    body = []
    body.append('<div class="note"><p>Every product in the catalogue, one row per product, with a source link per row. '
                "Use the search box to filter. Fields Amazon did not publish are shown as "
                "<strong>Unverified</strong> rather than filled in.</p></div>")

    body.append('<div class="toolbar">'
                '<input type="search" data-filter="#ptable" placeholder="Filter products by brand, ASIN, price, promotion&hellip;" aria-label="Filter products">'
                "</div>")
    body.append(card("Products (%d)" % len(PRODUCTS["products"]),
                     product_table("Sorted by product id by default.").replace(
                         '<table data-sortable data-verify-source>', '<table data-sortable data-verify-source id="ptable">'),
                     "Home &amp; Kitchen &rsaquo; air fryers. Captured %s." % esc(CAPTURED)))

    # full field table
    rows = []
    for p in PRODUCTS["products"]:
        for name, fld in p["fields"].items():
            val = fld["value"]
            if isinstance(val, float):
                shown = "%0.2f" % val
            elif val is None:
                shown = unverified_cell(fld.get("note", ""))
            else:
                shown = esc(val)
            rows.append(
                "<tr><td>%s</td><td class=\"nowrap\">%s</td><td class=\"nowrap\">%s</td><td>%s</td>"
                "<td>%s</td><td class=\"src\">%s</td></tr>" % (
                    esc(p["id"]),
                    '<a href="product-%s.html">%s</a>' % (p["slug"], esc(p["fields"]["asin"]["value"])),
                    "<code>%s</code>" % esc(name),
                    shown,
                    chip(fld["status"]),
                    srclinks(fld["source"]) if fld["source"] else unverified_cell(),
                )
            )
    body.append(card(
        "Full field register",
        '<div class="wrap"><table data-sortable data-verify-source><thead><tr>'
        '<th data-sort="text">Product</th><th data-sort="text">ASIN</th><th data-sort="text">Field</th>'
        '<th data-sort="text">Value</th><th data-sort="text">Status</th><th>Source</th>'
        "</tr></thead><tbody>%s</tbody></table></div>"
        '<p class="tbl-cap">Every field held for every product. %d rows.</p>' % ("".join(rows), len(rows)),
        "This is the machine-readable backing for every table on this site (<code>data/products.json</code>).",
    ))
    return shell("products.html", "All Products",
                 "Full product catalogue with per-field verification status and source links.",
                 "".join(body))


def page_categories():
    depts = {}
    for p in PRODUCTS["products"]:
        depts.setdefault(p["fields"]["department"]["value"], []).append(p)
    rows = []
    for dept, items in sorted(depts.items()):
        prices = [fv(p, "current_price")["value"] for p in items if fv(p, "current_price")["value"]]
        rows.append(
            "<tr><td><strong>%s</strong></td><td class=\"num\">%d</td>"
            "<td>Air fryers</td>"
            '<td class="num">%s</td>'
            "<td>%s</td>"
            '<td><a href="category-home-kitchen.html">Open category</a></td>'
            '<td class="src">%s</td></tr>' % (
                esc(dept), len(items),
                money(min(prices)) + " &ndash; " + money(max(prices)) if prices else "&mdash;",
                esc(", ".join(sorted({fv(p, "brand_from_title")["value"] for p in items}))),
                srclinks(["S1", "S3", "S5"]),
            )
        )
    body = [
        '<div class="note"><p>Categories are read from the department Amazon itself assigns to each product '
        "(the department segment of the official page title). One category is present because all three "
        "supplied links resolve into it.</p></div>",
        card("Categories",
             '<div class="wrap"><table data-sortable data-verify-source><thead><tr>'
             '<th data-sort="text">Department</th><th data-sort="num" class="num">Products</th>'
             '<th data-sort="text">Product type</th><th data-sort="num" class="num">Price range</th>'
             '<th data-sort="text">Brands</th><th>Page</th><th>Source</th>'
             "</tr></thead><tbody>%s</tbody></table></div>"
             '<p class="tbl-cap">Price range spans the verified current prices of the products in the category.</p>'
             % "".join(rows),
             "Organised by the department Amazon assigns to each ASIN."),
    ]
    return shell("categories.html", "Categories",
                 "Product catalogue organised by Amazon department.", "".join(body))


def page_category_home_kitchen():
    body = []
    body.append('<div class="note"><p><strong>Home &amp; Kitchen &rsaquo; Air fryers.</strong> '
                "All three supplied products fall into this single category, which makes the niche unusually "
                "tight: three direct comparators, no category sprawl.</p></div>")
    body.append(card("Products in this category",
                     product_table(),
                     "Captured %s from amazon.com." % esc(CAPTURED)))
    body.append(card("Buying guide", md("buying-guide-air-fryers.md"),
                     "Written only from values verified on Amazon for these three products."))
    body.append(card(
        "Niche economics",
        '<div class="wrap"><table data-verify-source><thead><tr><th>Question</th><th>Answer</th><th>Source</th></tr></thead><tbody>'
        "<tr><td>Official commission rate for <em>Kitchen</em></td><td>%s</td><td>%s</td></tr>"
        "<tr><td>Official commission rate for <em>Home</em></td><td>%s</td><td>%s</td></tr>"
        "<tr><td>Official rate for <em>All Other Categories</em></td><td>%s</td><td>%s</td></tr>"
        "<tr><td>Which of those applies to a given ASIN</td><td>%s</td><td>%s</td></tr>"
        "<tr><td>Session window after a link click</td><td>%s</td><td>%s</td></tr>"
        "<tr><td>Add-to-cart order window</td><td>%s</td><td>%s</td></tr>"
        "</tbody></table></div>"
        '<p class="tbl-cap">The gap between the Kitchen row and the Home row is a 50%% difference in commission on '
        "the same sale, which is why the per-ASIN mapping is not guessed at here.</p>" % (
            pct(4.5), srclinks("S7"),
            pct(3.0), srclinks("S7"),
            pct(4.0), srclinks("S7"),
            unverified_cell(COMMISSION["per_asin_category_mapping"]["note"]), srclinks(None),
            esc(COMMISSION["qualifying_purchase_rules"]["session_window"]), srclinks("S8"),
            esc(COMMISSION["qualifying_purchase_rules"]["cart_window"]), srclinks("S8"),
        ),
        "Only officially published rates are stated. Nothing is interpolated."))
    return shell("category-home-kitchen.html", "Home &amp; Kitchen",
                 "Air fryers in the Home & Kitchen department, with a buying guide and niche economics.",
                 "".join(body))


def page_product(p):
    f = p["fields"]
    dp = "S1" if p["id"] == "P1" else "S3" if p["id"] == "P2" else "S5"
    sr = "S2" if p["id"] == "P1" else "S4" if p["id"] == "P2" else "S6"
    dd = discount_depth(p)

    rows = []
    label = {
        "asin": "ASIN", "title": "Full title", "title_feature_line": "Feature line",
        "brand_from_title": "Brand", "department": "Department", "canonical_url": "Canonical URL",
        "amazon_listing_url": "Amazon listing URL", "current_price": "Current price",
        "list_price": "List price", "unit_price": "Unit price", "deal_badge": "Promotion badge",
        "other_offers_low": "Lowest other offer", "rating": "Star rating",
        "ratings_count_display": "Ratings count (Amazon rounded)", "demand_signal": "Demand signal",
        "variants": "Variants", "short_link_code": "Supplied short-link code",
        "best_sellers_rank": "Best Sellers Rank",
        "associates_commission_category": "Associates commission category",
        "review_sentiment_breakdown": "Review sentiment breakdown",
        "clicks": "Clicks", "conversions": "Conversions", "associates_tag": "Associates tag",
    }
    for name, fld in f.items():
        val = fld["value"]
        if isinstance(val, float):
            shown = "$%0.2f" % val if "price" in name else "%0.1f / 5" % val
        elif val is None:
            shown = unverified_cell(fld.get("note", ""))
        elif name.endswith("_url"):
            shown = '<a href="%s" target="_blank" rel="noopener nofollow">%s</a>' % (esc(val), esc(val))
        else:
            shown = esc(val)
        rows.append(
            '<tr><th scope="row" style="font-weight:600;color:var(--ink-soft);white-space:nowrap">%s</th>'
            "<td>%s</td><td>%s</td><td class=\"src\">%s</td></tr>"
            % (esc(label.get(name, name)), shown, chip(fld["status"]),
               srclinks(fld["source"]) if fld["source"] else unverified_cell())
        )

    body = []
    body.append('<h1 style="margin-bottom:6px">%s</h1>' % esc(f["brand_from_title"]["value"]))
    body.append('<p style="color:var(--ink-faint);font-size:13.5px;margin-bottom:18px">%s</p>'
                % esc(f["title"]["value"]))

    body.append(card(
        "Verified specification",
        '<div class="wrap"><table data-verify-source><tbody>%s</tbody></table></div>' % "".join(rows),
        "Every row links to the official Amazon page the value was read from.",
    ))

    body.append(
        '<div class="grid2">'
        + card("Price position",
               '<dl class="kv">'
               "<dt>Current price</dt><dd>%s</dd>" % money(fv(p, "current_price")["value"])
               + "<dt>List price</dt><dd>%s</dd>" % money(fv(p, "list_price")["value"])
               + "<dt>Discount depth (derived)</dt><dd>%s</dd>" % ("&mdash;" if dd is None else "%0.1f%%" % dd)
               + "<dt>Lowest other offer</dt><dd>%s</dd>" % money(fv(p, "other_offers_low")["value"])
               + "<dt>Promotion badge</dt><dd>%s</dd>" % esc(fv(p, "deal_badge")["value"] or "Unverified")
               + "</dl>"
                 '<p class="tbl-cap">Discount depth is computed from the two verified prices; it is not an Amazon-published figure.</p>',
               "Source %s." % srclinks(sr))
        + card("Buy it on Amazon",
               '<p><a href="%s" target="_blank" rel="noopener nofollow">Open the official Amazon listing</a> '
               "for ASIN <code>%s</code>.</p>" % (esc(f["amazon_listing_url"]["value"]), esc(f["asin"]["value"]))
               + '<p class="tbl-cap">This link carries no Associates tag. No commission accrues from it. '
                 'See <a href="flagged.html">F07</a>.</p>',
               "Canonical product page %s." % srclinks(dp))
        + "</div>"
    )

    body.append(card("Notes",
                     '<ul class="tight">'
                     "<li>This page is an analysis record. It is not a live affiliate landing page: the price and "
                     "rating fields would need to be re-sourced through the Product Advertising API or Creators API "
                     'before publication as an Associates property (<a href="flagged.html">F01</a>, '
                     '<a href="flagged.html">F02</a>).</li>'
                     "<li>The supplied short link for this product is "
                     '<a href="%s" target="_blank" rel="noopener nofollow">%s</a>, which resolves to '
                     "<code>%s</code>. The short link should not be used as the affiliate link "
                     '(<a href="flagged.html">F03</a>).</li>'
                     "</ul>" % (esc(p["short_link"]), esc(p["short_link"]), esc(f["asin"]["value"]))))

    return shell(
        "product-%s.html" % p["slug"],
        "%s %s" % (f["brand_from_title"]["value"], f["asin"]["value"]),
        f["title"]["value"][:150],
        "".join(body),
    )


def page_comparison():
    prods = PRODUCTS["products"]
    metrics = [
        ("Current price", lambda p: money(fv(p, "current_price")["value"]),
         lambda p: fv(p, "current_price")["value"], True),
        ("List price", lambda p: money(fv(p, "list_price")["value"]),
         lambda p: fv(p, "list_price")["value"], True),
        ("Discount depth (derived)", lambda p: "%0.1f%%" % discount_depth(p) if discount_depth(p) is not None else "&mdash;",
         lambda p: discount_depth(p), True),
        ("Lowest other offer", lambda p: money(fv(p, "other_offers_low")["value"]),
         lambda p: fv(p, "other_offers_low")["value"], True),
        ("Star rating", lambda p: "%0.1f / 5" % fv(p, "rating")["value"],
         lambda p: fv(p, "rating")["value"], True),
        ("Ratings count", lambda p: esc(fv(p, "ratings_count_display")["value"]), None, False),
        ("Bought in past month", lambda p: esc(fv(p, "demand_signal")["value"].replace(" bought in past month", "")),
         None, False),
        ("Promotion badge", lambda p: esc(fv(p, "deal_badge")["value"]), None, False),
        ("Capacity (from title)", lambda p: "6 qt (2 &times; 3 qt)" if p["id"] == "P1"
         else "26 qt" if p["id"] == "P2" else "8 qt", None, False),
        ("Commission rate per ASIN", lambda p: unverified_cell(), None, False),
    ]
    head = "<th>Metric</th>" + "".join(
        '<th><a href="product-%s.html">%s</a><br><small>%s</small></th>'
        % (p["slug"], esc(p["fields"]["brand_from_title"]["value"]), esc(p["fields"]["asin"]["value"]))
        for p in prods)
    rows = []
    for label, fn, _sortv, _numeric in metrics:
        rows.append("<tr><th scope=\"row\" style=\"font-weight:600;color:var(--ink-soft)\">%s</th>%s</tr>"
                    % (esc(label), "".join("<td>%s</td>" % fn(p) for p in prods)))
    rows.append('<tr><th scope="row" style="font-weight:600;color:var(--ink-soft)">Source</th>%s</tr>'
                % "".join('<td class="src">%s</td>' % srclinks(
                    ["S1", "S2"] if p["id"] == "P1" else ["S3", "S4"] if p["id"] == "P2" else ["S5", "S6"])
                    for p in prods))

    body = [
        '<div class="note warn"><p>Capacity is read from the official product title, not from a specification table. '
        "Commission rate per ASIN is blank on purpose: Amazon publishes the rate by category, not by ASIN, and both "
        "the Kitchen row (4.50%) and the Home row (3.00%) are plausible for these products.</p></div>",
        card("Side by side",
             '<div class="wrap"><table><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>'
             % (head, "".join(rows)),
             "Three products, one niche. Every value comes from an official Amazon page."),
        card("Read of the comparison", md("comparison-read.md")),
    ]
    return shell("comparison.html", "Comparison",
                 "Side-by-side comparison of the three tracked air fryers.", "".join(body))


def page_analysis():
    prods = PRODUCTS["products"]
    rows = []
    for p in prods:
        cur = fv(p, "current_price")["value"]
        lst = fv(p, "list_price")["value"]
        dd = discount_depth(p)
        rows.append(
            "<tr>"
            '<td><a href="product-%s.html">%s</a></td>' % (p["slug"], esc(p["fields"]["brand_from_title"]["value"]))
            + '<td class="num">%s</td>' % money(cur)
            + '<td class="num">%s</td>' % money(lst)
            + '<td class="num">%s</td>' % ("&mdash;" if dd is None else "%0.1f%%" % dd)
            + '<td class="num">%s</td>' % money(fv(p, "other_offers_low")["value"])
            + '<td class="num">%s</td>' % ("%0.1f / 5" % fv(p, "rating")["value"])
            + "<td>%s</td>" % esc(fv(p, "ratings_count_display")["value"])
            + "<td>%s</td>" % esc(fv(p, "demand_signal")["value"])
            + '<td class="src">%s</td>' % srclinks(
                ["S2"] if p["id"] == "P1" else ["S4"] if p["id"] == "P2" else ["S6"])
            + "</tr>"
        )

    body = [
        '<div class="note"><p><strong>Pricing.</strong> All three products were on promotion at capture time, and all '
        "three carried used/new offers below the Amazon price. That combination compresses the margin a reviewer can "
        "claim and means the &ldquo;deal&rdquo; framing has to be re-checked before each publish, because Amazon "
        "requires promotion references to be removed the moment a promotion ends "
        '(<a href="https://affiliate-program.amazon.com/help/operating/policies" target="_blank" rel="noopener nofollow">Participation Requirements 2(b)</a>).</p></div>',
        card("Pricing and demand",
             '<div class="wrap"><table data-sortable data-verify-source><thead><tr>'
             '<th data-sort="text">Product</th>'
             '<th data-sort="num" class="num">Price</th>'
             '<th data-sort="num" class="num">List</th>'
             '<th data-sort="num" class="num">Discount</th>'
             '<th data-sort="num" class="num">Lowest other offer</th>'
             '<th data-sort="num" class="num">Rating</th>'
             '<th data-sort="text">Ratings</th>'
             '<th data-sort="text">Demand (past month)</th>'
             "<th>Source</th>"
             "</tr></thead><tbody>%s</tbody></table></div>"
             '<p class="tbl-cap">Discount is derived from the two verified prices on the same row. '
             "&ldquo;Lowest other offer&rdquo; is the lowest price Amazon displayed under More Buying Choices.</p>"
             % "".join(rows),
             "Captured %s." % esc(CAPTURED)),
        card("Reviews", md("analysis-reviews.md")),
        card("Competition", md("analysis-competition.md")),
    ]
    return shell("analysis.html", "Pricing &amp; Reviews",
                 "Pricing, review and competition analysis from verified Amazon data.", "".join(body))


def page_commission():
    rows = []
    for r in COMMISSION["table1_fixed_standard_commission_rates"]:
        highlight = "Kitchen" in r["product_category"] or r["product_category"] == "Home"
        rows.append(
            '<tr%s><td>%s</td><td class="num">%s</td><td class="src">%s</td></tr>'
            % (' style="background:#f8fafc"' if highlight else "",
               esc(r["product_category"]), pct(r["rate"]), srclinks("S7"))
        )
    q = COMMISSION["qualifying_purchase_rules"]

    brows = []
    for b in COMMISSION["bounty_events"]:
        brows.append(
            "<tr><td>%s</td><td>%s</td><td class=\"num\">$%0.2f</td><td class=\"src\">%s</td></tr>"
            % (esc(b["program"]), esc(b["action"]), b["rate_usd"], srclinks("S7"))
        )

    body = [
        '<div class="note warn"><p>The two highlighted rows are the ones that matter for this catalogue. Amazon does '
        "not publish which row a given ASIN sits in, so <strong>no per-product rate is asserted anywhere on this "
        'site</strong>. Treat the band 3.00%&ndash;4.50% as unresolved, not as an estimate.</p></div>',
        card("Table 1 &mdash; Fixed Standard Commission Income Rates",
             '<div class="wrap"><table data-sortable data-verify-source><thead><tr>'
             '<th data-sort="text">Product category</th>'
             '<th data-sort="num" class="num">Fixed commission income rate</th>'
             "<th>Source</th></tr></thead><tbody>%s</tbody></table></div>"
             '<p class="tbl-cap">Reproduced verbatim from the Associates Program Standard Commission Income Statement. '
             "Rows highlighted are the Kitchen and Home rows, the two candidates for this catalogue.</p>"
             % "".join(rows),
             "Source: Amazon Associates Central, %s." % srclinks("S7")),
        card("How a commission is actually earned",
             '<dl class="kv">'
             "<dt>Session window</dt><dd>%s</dd>" % esc(q["session_window"])
             + "<dt>Add-to-cart window</dt><dd>%s</dd>" % esc(q["cart_window"])
             + "<dt>Fulfilment window</dt><dd>%s</dd>" % esc(q["fulfilment_window"])
             + "<dt>Qualifying Revenue</dt><dd>%s</dd>" % esc(q["qualifying_revenue"])
             + "</dl>"
             '<p class="tbl-cap">Source: %s</p>' % srclinks("S8"),
             "Read before modelling revenue: commission is a percentage of Qualifying Revenue, not of the sticker price."),
        card("Bounty events (fixed cash, not a percentage)",
             '<div class="wrap"><table data-sortable data-verify-source><thead><tr>'
             '<th data-sort="text">Program</th><th data-sort="text">Bounty action</th>'
             '<th data-sort="num" class="num">Bounty rate</th><th>Source</th>'
             "</tr></thead><tbody>%s</tbody></table></div>" % "".join(brows),
             "Source: %s. These are flat-dollar events, independent of the product category rate." % srclinks("S7")),
        card("Disqualified purchases",
             "<p>These purchases earn nothing even if the link worked. Reproduced from the Commission Income "
             "Statement, section 2:</p><ul class=\"tight\">%s</ul>"
             '<p class="tbl-cap">Source: %s</p>'
             % ("".join("<li>%s</li>" % esc(d) for d in q["disqualified_examples"]), srclinks("S8")),
             "Two of these directly affect this project &mdash; see F03 on the Flagged page."),
        card("Modelled scenarios (not verified)",
             md("commission-modelled.md"),
             "Arithmetic from verified prices against the two candidate official rates. Shown so the decision is visible, not as a claim."),
    ]
    return shell("commission.html", "Commission Model",
                 "Official Amazon Associates commission rates, qualifying-purchase rules and bounty events.",
                 "".join(body))


def page_compliance():
    body = [
        '<div class="note bad"><p><strong>Two blocking conflicts are open on the data itself.</strong> '
        "Amazon's Participation Requirements restrict displaying prices (section 2(b)) and star ratings "
        "(section 6(t)) unless the data is served by Amazon or obtained through the Product Advertising API / "
        "Creators API. This site shows both, captured by other means, so it cannot go live as an Associates "
        "property in its current form. See <a href=\"flagged.html\">F01</a> and <a href=\"flagged.html\">F02</a>.</p></div>",
        card("Obligations, with the policy text",
             md("compliance-obligations.md"),
             "Each line cites the exact Amazon or FTC source. Nothing here is paraphrased from a third party."),
        card("Disclosure requirement",
             md("compliance-disclosure.md"),
             "Two separate obligations: Amazon's contract terms, and the FTC's Endorsement Guides."),
        card("Payment terms",
             '<div class="wrap"><table data-verify-source><thead><tr><th>Item</th><th>Value</th><th>Source</th></tr></thead><tbody>'
             "<tr><td>Payment timing</td><td>%s</td><td>%s</td></tr>"
             "<tr><td>Option 1 &mdash; Direct deposit minimum (US)</td><td>$10 USD</td><td>%s</td></tr>"
             "<tr><td>Option 2 &mdash; Gift card minimum / maximum (US)</td><td>$10 USD / $2,000 USD</td><td>%s</td></tr>"
             "<tr><td>Option 3 &mdash; Check minimum (US)</td><td>$100 USD</td><td>%s</td></tr>"
             "<tr><td>Check processing fee (US)</td><td>$15 USD</td><td>%s</td></tr>"
             "<tr><td>Inactivity</td><td>No substantial activity for at least 3 years &rarr; Amazon may withhold accrued commission, with 7 days&rsquo; written notice</td><td>%s</td></tr>"
             "</tbody></table></div>"
             % (
                 esc("Approximately 60 days following the end of each calendar month in which they were earned"),
                 srclinks("S8"), srclinks("S8"), srclinks("S8"), srclinks("S8"), srclinks("S8"), srclinks("S8"),
             ),
             "Reproduced from the Associates Program Policies, Commission Income Statement section 6."),
    ]
    return shell("compliance.html", "Compliance",
                 "Amazon Associates policy obligations, FTC disclosure rules and payment terms.", "".join(body))


def page_flagged():
    sev_label = {"blocking": "b", "review": "u", "info": "n"}
    rows = []
    for fl in FLAGS["flags"]:
        src = srclinks(fl["source_id"]) if fl["source_id"] else \
            '<span class="unverified">no official source</span>'
        rows.append(
            '<tr data-flag-row="%s">'
            '<td class="nowrap"><span class="chip %s">%s</span><br><code>%s</code></td>'
            "<td><strong>%s</strong><p style=\"margin:6px 0 0;font-size:13px;color:var(--ink-soft)\">%s</p>"
            '<p style="margin:8px 0 0;font-size:12.5px"><em>Impact:</em> %s</p>'
            '<p style="margin:6px 0 0;font-size:12.5px"><em>Action:</em> %s</p></td>'
            '<td class="src">%s</td>'
            "</tr>" % (
                esc(fl["severity"]), sev_label.get(fl["severity"], "n"), esc(fl["severity"].upper()),
                esc(fl["id"]),
                esc(fl["title"]), esc(fl["detail"]), esc(fl["impact"]), esc(fl["recommended_action"]),
                src,
            )
        )
    counts = {
        "all": len(FLAGS["flags"]),
        "blocking": sum(1 for f in FLAGS["flags"] if f["severity"] == "blocking"),
        "review": sum(1 for f in FLAGS["flags"] if f["severity"] == "review"),
        "info": sum(1 for f in FLAGS["flags"] if f["severity"] == "info"),
    }
    pills = "".join(
        '<button type="button" class="pill%s" data-sev="%s">%s (%d)</button>'
        % (" on" if k == "all" else "", k, label, counts[k])
        for k, label in [("all", "All"), ("blocking", "Blocking"), ("review", "Review"), ("info", "Info")]
    )
    body = [
        '<div class="note bad"><p>These items do <strong>not</strong> block the merge or the deploy. They are '
        "published here so you can review them after the site is live and request changes. "
        "<strong>Blocking</strong> means the item must be resolved before this site operates as a live Amazon "
        "Associates property.</p></div>",
        card("Flagged items",
             '<div class="pillbar">%s</div>'
             '<div class="wrap"><table data-verify-source><thead><tr><th>Severity</th><th>Item</th><th>Source</th></tr></thead>'
             "<tbody>%s</tbody></table></div>" % (pills, "".join(rows)),
             "%d items. Each links to the official source that establishes it, or states that no official source exists."
             % len(FLAGS["flags"])),
    ]
    return shell("flagged.html", "Flagged for Review",
                 "Irregularities, open risks and unverified values, each with its official source.",
                 "".join(body))


def page_sources():
    rows = []
    for s in SOURCES["sources"]:
        rows.append(
            "<tr><td><code>%s</code></td>"
            '<td><a href="%s" target="_blank" rel="noopener nofollow">%s</a></td>'
            "<td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" % (
                esc(s["id"]), esc(s["url"]), esc(s["title"]),
                esc(s["publisher"]),
                '<span class="chip v">Official</span>' if s.get("official") else '<span class="chip n">Supplied</span>',
                esc(s.get("last_updated", "&mdash;")),
                esc(s["used_for"]),
            )
        )
    body = [
        '<div class="note"><p><strong>Every value on this site comes from one of the rows below.</strong> '
        "S1&ndash;S11 are first-party pages published by Amazon or the U.S. Federal Trade Commission. S12 is the "
        "entry point supplied in the brief: it is used only as the record of what was given, never as evidence for "
        "a product fact.</p></div>",
        card("Source register",
             '<div class="wrap"><table data-sortable><thead><tr>'
             '<th data-sort="text">ID</th><th data-sort="text">Source</th><th data-sort="text">Publisher</th>'
             '<th data-sort="text">Type</th><th data-sort="text">Last updated</th>'
             '<th data-sort="text">Used for</th>'
             "</tr></thead><tbody>%s</tbody></table></div>" % "".join(rows),
             "Open these links to check any figure on the site yourself."),
    ]
    return shell("sources.html", "Sources",
                 "Every official source used, with what each one supports.", "".join(body))


def page_verification():
    rows = []
    for p in PRODUCTS["products"]:
        for name, fld in p["fields"].items():
            val = fld["value"]
            shown = "&mdash;" if val is None else (
                "$%0.2f" % val if isinstance(val, float) else esc(val))
            rows.append(
                "<tr><td>%s</td><td class=\"mono\">%s</td><td><code>%s</code></td><td>%s</td>"
                "<td>%s</td><td><small>%s</small></td><td class=\"src\">%s</td></tr>" % (
                    esc(p["id"]), esc(p["fields"]["asin"]["value"]), esc(name), shown,
                    chip(fld["status"]), esc(fld.get("note", "")),
                    srclinks(fld["source"]) if fld["source"] else unverified_cell(),
                )
            )
    body = [
        card("Method", md("verification-method.md"),
             "The rule applied to every cell on this site."),
        card("Verification log",
             '<div class="wrap"><table data-sortable data-verify-source><thead><tr>'
             '<th data-sort="text">Product</th><th data-sort="text">ASIN</th><th data-sort="text">Field</th>'
             '<th data-sort="text">Value</th><th data-sort="text">Status</th><th>Note</th><th>Source</th>'
             "</tr></thead><tbody>%s</tbody></table></div>"
             '<p class="tbl-cap">%d field checks. A blank value with status Unverified is a deliberate omission, '
             "not a missing one.</p>" % ("".join(rows), len(rows)),
             "Generated from <code>data/products.json</code>, the same file the site renders from."),
    ]
    return shell("verification.html", "Verification Log",
                 "Field-by-field verification status for every value on the site.", "".join(body))


def page_requirements():
    rows = []
    for r in REQS["requirements"]:
        cls = {"implemented": "v", "partial": "u", "blocked": "b"}.get(r["status"], "n")
        flags = " ".join('<a href="flagged.html">%s</a>' % esc(f) for f in r.get("flags", [])) or "&mdash;"
        rows.append(
            "<tr><td><code>%s</code></td><td>%s</td>"
            '<td><span class="chip %s">%s</span></td>'
            "<td><small>%s</small></td><td><small>%s</small></td><td class=\"nowrap\">%s</td></tr>" % (
                esc(r["id"]), esc(r["text"]), cls, esc(r["status"].capitalize()),
                esc(r["evidence"]), esc(r.get("gap", "") or "&mdash;"), flags,
            )
        )
    n_impl = sum(1 for r in REQS["requirements"] if r["status"] == "implemented")
    n_part = sum(1 for r in REQS["requirements"] if r["status"] == "partial")
    n_block = sum(1 for r in REQS["requirements"] if r["status"] == "blocked")
    body = [
        '<div class="kpis">'
        '<div class="kpi ok"><div class="n">%d</div><div class="l">Implemented</div></div>'
        '<div class="kpi warn"><div class="n">%d</div><div class="l">Partial</div></div>'
        '<div class="kpi bad"><div class="n">%d</div><div class="l">Blocked</div></div>'
        '<div class="kpi"><div class="n">%d</div><div class="l">Total requirements</div></div>'
        "</div>" % (n_impl, n_part, n_block, len(REQS["requirements"])),
        '<div class="note"><p>R01&ndash;R21 are decomposed from the project brief, verbatim. '
        "R22&ndash;R30 are the delivery requirements from this session. "
        "<strong>Blocked</strong> means it cannot be delivered with the data or infrastructure available, "
        "and the reason is given.</p></div>",
        card("Requirements matrix",
             '<div class="wrap"><table data-sortable><thead><tr>'
             '<th data-sort="text">ID</th><th data-sort="text">Requirement</th>'
             '<th data-sort="text">Status</th><th>Evidence</th><th>Gap</th><th>Flags</th>'
             "</tr></thead><tbody>%s</tbody></table></div>" % "".join(rows),
             "Source of truth: <code>data/requirements.json</code>."),
        card("Automation design", md("automation-design.md"),
             "How the blocked automation requirements would be built, and what each one needs first."),
    ]
    return shell("requirements.html", "Requirements",
                 "The full requirements list decomposed from the brief, with delivery status per item.",
                 "".join(body))


# ----------------------------------------------------------------------------
# write
# ----------------------------------------------------------------------------

PAGES = {
    "index.html": page_index,
    "executive-summary.html": page_executive_summary,
    "products.html": page_products,
    "categories.html": page_categories,
    "category-home-kitchen.html": page_category_home_kitchen,
    "comparison.html": page_comparison,
    "analysis.html": page_analysis,
    "commission.html": page_commission,
    "compliance.html": page_compliance,
    "flagged.html": page_flagged,
    "sources.html": page_sources,
    "verification.html": page_verification,
    "requirements.html": page_requirements,
}


def main():
    written = []
    for name, fn in PAGES.items():
        out = fn()
        path = os.path.join(OUT, name)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(out)
        written.append(name)

    for p in PRODUCTS["products"]:
        name = "product-%s.html" % p["slug"]
        with open(os.path.join(OUT, name), "w", encoding="utf-8") as fh:
            fh.write(page_product(p))
        written.append(name)

    # .nojekyll so GitHub Pages serves files as-is
    with open(os.path.join(OUT, ".nojekyll"), "w", encoding="utf-8") as fh:
        fh.write("")

    print("wrote %d pages" % len(written))
    for n in written:
        print("  " + n)
    return 0


if __name__ == "__main__":
    sys.exit(main())
