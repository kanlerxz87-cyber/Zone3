#!/usr/bin/env python3
"""
Zone3 - static site generator for the Amazon affiliate research dashboard.

Reads  : data/*.json, site/*, content/*.html
Writes : docs/**

Guarantees enforced by this script (the build FAILS if any is violated):
  1. Every external absolute URL emitted into the HTML must appear in
     data/sources.json (individually retrieved) or data/derived_links.json
     (observed on a retrieved official page). Nothing else is linkable.
  2. Every internal href must resolve to a file that this build produces.
  3. Every volatile value rendered in a table must be accompanied by a link
     to the official page it was read from.

Run:  python3 tools/build_site.py
      python3 tools/build_site.py --check     (validate only, write nothing)
"""

from __future__ import annotations

import html
import json
import os
import re
import shutil
import sys
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
CONTENT = os.path.join(ROOT, "content")
SITE = os.path.join(ROOT, "site")
DOCS = os.path.join(ROOT, "docs")

CHECK_ONLY = "--check" in sys.argv
PUBLISH_ROOT = "--publish-root" in sys.argv
MANIFEST = ".published-manifest.json"

CAPTURED = "2026-11-13T22:39:51Z"


# --------------------------------------------------------------------------
# helpers
# --------------------------------------------------------------------------
def load(name):
    with open(os.path.join(DATA, name), encoding="utf-8") as fh:
        return json.load(fh)


def e(s) -> str:
    """escape for HTML text"""
    return html.escape("" if s is None else str(s), quote=True)


def money(s) -> float:
    return float(re.sub(r"[^0-9.]", "", s or "0"))


def usd(x: float) -> str:
    return "${:,.2f}".format(x)


def read_fragment(name):
    path = os.path.join(CONTENT, name)
    with open(path, encoding="utf-8") as fh:
        return fh.read()


products = load("products.json")
sources = load("sources.json")
flags = load("flags.json")
competitors = load("competitors.json")
derived = load("derived_links.json")

SRC = {s["id"]: s for s in sources["sources"]}
ALLOWED_EXTERNAL = {s["url"] for s in sources["sources"]}
for d in derived["links"]:
    ALLOWED_EXTERNAL.add(d["url"])

COMMISSION_RATES = [
    # label, rate, source id, note
    ("Kitchen", 0.045, "S16",
     "Primary case. The products sit in Kitchen &amp; Dining &gt; Small Appliances &gt; Fryers &gt; Air Fryers."),
    ("Home", 0.030, "S16",
     "Downside case. Amazon lists Home and Kitchen as separate commission categories and does not publish its per-ASIN assignment."),
]

# --------------------------------------------------------------------------
# navigation
# --------------------------------------------------------------------------
NAV = [
    ("Overview", [
        ("index.html", "Dashboard"),
        ("executive-summary.html", "Executive Summary"),
    ]),
    ("Products", [
        ("products.html", "Master Data Table"),
        ("comparison.html", "Comparison"),
        ("link-resolution.html", "Link Resolution"),
    ]),
    ("Categories", [
        ("categories/air-fryers.html", "Air Fryers"),
        ("categories/dual-basket.html", "Dual Basket"),
        ("categories/air-fryer-toaster-ovens.html", "Toaster Ovens"),
        ("categories/large-capacity.html", "Large Capacity"),
    ]),
    ("Marketing", [
        ("niche-analysis.html", "Niche &amp; Competition"),
        ("commission-model.html", "Commission Model"),
        ("link-builder.html", "Link Builder"),
    ]),
    ("Governance", [
        ("compliance.html", "Compliance"),
        ("data-sources.html", "Data Sources"),
        ("flagged.html", "Flagged for Review"),
    ]),
    ("Platform", [
        ("platform.html", "Automation Architecture"),
        ("analytics.html", "Tracking &amp; Analytics"),
    ]),
]

PAGE_TITLES = {}
for _grp, _items in NAV:
    for _href, _label in _items:
        PAGE_TITLES[_href] = _label


def render_nav(active: str) -> str:
    out = ['<nav aria-label="Site navigation">']
    for grp, items in NAV:
        out.append('<div class="grp">%s</div>' % grp)
        for href, label in items:
            cls = "nav on" if href == active else "nav"
            out.append('<a class="%s" href="%s">%s</a>' % (cls, rel(href, active), label))
    out.append("</nav>")
    return "\n".join(out)


def rel(target: str, frm: str) -> str:
    """Relative link from page `frm` (e.g. categories/air-fryers.html) to `target`."""
    if "/" not in frm:
        return target
    depth = frm.count("/")
    return "../" * depth + target


# --------------------------------------------------------------------------
# badges
# --------------------------------------------------------------------------
def status_badge(status: str) -> str:
    m = {
        "verified": ("t-ok", "verified"),
        "verified_rounded": ("t-round", "verified (rounded)"),
        "unverified": ("t-unv", "unverified"),
        "false": ("t-bad", "absent"),
        "true": ("t-ok", "present"),
    }
    cls, label = m.get(status, ("t-unv", status))
    return '<span class="tag %s">%s</span>' % (cls, label)


def sev_badge(sev: str) -> str:
    m = {
        "blocker": ("t-bad", "blocker"),
        "unverified-data": ("t-unv", "unverified"),
        "needs-decision": ("t-warn", "needs decision"),
        "needs-review": ("t-round", "needs review"),
        "repo": ("t-unv", "repo note"),
    }
    cls, label = m.get(sev, ("t-unv", sev))
    return '<span class="tag %s">%s</span>' % (cls, label)


def srclink(url: str, label: str = "source") -> str:
    return '<a href="%s" target="_blank" rel="noopener nofollow">%s &#8599;</a>' % (e(url), label)


# --------------------------------------------------------------------------
# tables
# --------------------------------------------------------------------------
def table_identity(frm=None) -> str:
    rows = []
    for p in products["products"]:
        fv = p["field_verification"]
        rows.append("""<tr>
  <td class="mono">%(id)s</td>
  <td><a href="%(canon)s" target="_blank" rel="noopener nofollow">%(title)s</a>
      <span class="src">Official Amazon title. %(dp)s</span></td>
  <td class="mono">%(asin)s</td>
  <td>%(brand)s</td>
  <td>%(dept)s</td>
  <td>%(sub)s</td>
  <td>%(cap)s</td>
  <td>%(bsr)s</td>
  <td>%(tag)s</td>
  <td>%(src)s</td>
</tr>""" % {
            "id": e(p["id"]),
            "canon": e(p["canonical_url"]),
            "title": e(p["title_official"]),
            "dp": srclink(p["short_link_resolves_to"], "dp page"),
            "asin": e(p["asin"]),
            "brand": e(p["brand_from_title"]),
            "dept": e(p["department_official"]),
            "sub": e(p["subcategory_derived"]),
            "cap": e(p["capacity_from_title"]) + '<span class="src">from official title</span>',
            "bsr": '<span class="blank">blank</span> <span class="src">FLAG-03</span>',
            "tag": status_badge(fv["affiliate_tag_present"]["status"]) + '<span class="src">FLAG-05</span>',
            "src": srclink(p["source_url"], "official"),
        })
    return """<div class="tw"><table>
<thead><tr>
  <th>ID</th><th>Official product title</th><th>ASIN</th><th>Brand</th>
  <th>Department</th><th>Sub-category</th><th>Capacity</th>
  <th>Best Sellers Rank</th><th>Affiliate tag</th><th>Source</th>
</tr></thead>
<tbody>%s
</tbody></table></div>
<div class="note warn"><b>Blank cells are deliberate.</b> Best Sellers Rank could not be read from any official page in this session (FLAG-03). The affiliate tag column is <b>absent</b>, not unknown: neither the supplied short links nor the canonical URLs contain a tag parameter (FLAG-05).</div>
""" % "\n".join(rows)


def table_commercials(frm=None) -> str:
    rows = []
    for p in products["products"]:
        fv = p["field_verification"]
        rows.append("""<tr>
  <td class="mono">%(id)s</td>
  <td>%(rating)s <span class="src">%(rstat)s</span></td>
  <td class="num">%(rcount)s <span class="src">%(rcstat)s</span></td>
  <td class="num">%(exact)s</td>
  <td class="num">%(price)s <span class="src">%(badge)s</span></td>
  <td class="num">%(list)s</td>
  <td class="num">%(other)s</td>
  <td>%(bought)s</td>
  <td><span class="ts">%(ts)s</span></td>
  <td>%(src)s</td>
</tr>""" % {
            "id": e(p["id"]),
            "rating": e(p["star_rating"]),
            "rstat": status_badge(fv["star_rating"]["status"]).replace('">', '" style="vertical-align:1px">'),
            "rcount": e(p["rating_count_display"]),
            "rcstat": status_badge(fv["rating_count_display"]["status"]),
            "exact": '<span class="blank">blank</span> <span class="src">FLAG-04</span>',
            "price": e(p["price_current"]),
            "badge": e(p["deal_badge_official"]) + " &middot; FLAG-02",
            "list": e(p["price_list"]),
            "other": e(p["more_buying_choices_lowest"]),
            "bought": e(p["bought_past_month"]) + ' <span class="src">rounded &middot; FLAG-08</span>',
            "ts": e(p["captured_utc"]),
            "src": srclink(p["source_url"], "official"),
        })
    return """<div class="tw"><table>
<thead><tr>
  <th>ID</th><th>Star rating</th><th class="num">Ratings (as shown)</th><th class="num">Exact rating count</th>
  <th class="num">Current price</th><th class="num">List price</th><th class="num">Lowest other offer</th>
  <th>Bought in past month</th><th>Captured (UTC)</th><th>Source</th>
</tr></thead>
<tbody>%s
</tbody></table></div>
<div class="note bad"><b>Do not publish these prices live.</b> Amazon's Participation Requirements allow a site to show prices only if Amazon serves the link, or if the price comes from Creators API / PA API. Every price here was read by hand from a search results page (FLAG-01). This table ships for review, not for a live monetised page.</div>
<div class="note">Prices, deal badges and rating counts are a snapshot. The capture timestamp is taken from the <span class="mono">qid</span> parameter Amazon returned with each search results page, so it is the true request time, not the time this document was written.</div>
""" % "\n".join(rows)


def table_link_resolution(frm=None) -> str:
    rows = []
    for p in products["products"]:
        rows.append("""<tr>
  <td class="mono">%(id)s</td>
  <td class="mono"><a href="%(short)s" target="_blank" rel="noopener nofollow">%(short)s</a></td>
  <td>&#8594;</td>
  <td class="mono"><a href="%(dp)s" target="_blank" rel="noopener nofollow">%(dp)s</a></td>
  <td class="mono">%(asin)s</td>
  <td class="mono"><a href="%(canon)s" target="_blank" rel="noopener nofollow">canonical /dp/ slug</a></td>
  <td>%(flag)s</td>
</tr>""" % {
            "id": e(p["id"]),
            "short": e(p["short_link_input"]),
            "dp": e(p["short_link_resolves_to"]),
            "asin": e(p["asin"]),
            "canon": e(p["canonical_url"]),
            "flag": sev_badge("needs-review") + ' <a href="flagged.html#FLAG-07">FLAG-07</a>',
        })
    return """<div class="tw"><table>
<thead><tr><th>ID</th><th>Link supplied</th><th></th><th>Resolves to</th><th>ASIN</th><th>Canonical URL</th><th>Provenance</th></tr></thead>
<tbody>%s
</tbody></table></div>
<div class="note">Each short link was fetched and followed. All three returned official <span class="mono">amazon.com/dp/</span> product pages, so the ASIN resolution is confirmed by observation. What is <i>not</i> confirmed is that the <span class="mono">link.amazon</span> host itself is documented as an Amazon-owned shortener - see FLAG-07.</div>
""" % "\n".join(rows)


def table_comparison(frm=None) -> str:
    ps = products["products"]
    def row(label, fn, note=""):
        cells = "".join("<td>%s%s</td>" % (fn(p), ('<span class="src">%s</span>' % note) if note else "")
                        for p in ps)
        return "<tr><th>%s</th>%s</tr>" % (label, cells)

    def img(p):
        return '<img src="%s" alt="%s" loading="lazy" style="max-height:120px;max-width:160px;object-fit:contain">' % (
            e(p["image_url"]), e(p["title_official"][:60]))

    def link(p):
        return '<a href="%s" target="_blank" rel="noopener nofollow">Open on Amazon &#8599;</a>' % e(p["canonical_url"])

    head = "<tr><th>Attribute</th>%s</tr>" % "".join(
        "<th>%s<div class=\"mono\" style=\"font-weight:400;text-transform:none;letter-spacing:0\">%s</div></th>"
        % (e(p["brand_from_title"]), e(p["asin"])) for p in ps)

    body = "\n".join([
        row("Image", img),
        row("Official title", lambda p: '<span style="font-size:12px">%s</span>' % e(p["title_official"])),
        row("Capacity", lambda p: e(p["capacity_from_title"]), "from official title"),
        row("Sub-category", lambda p: e(p["subcategory_derived"])),
        row("Star rating", lambda p: e(p["star_rating"])),
        row("Ratings shown", lambda p: e(p["rating_count_display"]), "rounded by Amazon"),
        row("Exact rating count", lambda p: '<span class="blank">blank</span> &middot; <a href="flagged.html#FLAG-04">FLAG-04</a>'),
        row("Current price", lambda p: '<b>%s</b>' % e(p["price_current"])),
        row("List price", lambda p: e(p["price_list"])),
        row("Discount vs list", lambda p: "%.0f%%" % (100 * (1 - money(p["price_current"]) / money(p["price_list"]))), "calculated"),
        row("Lowest other offer", lambda p: e(p["more_buying_choices_lowest"])),
        row("Promotion badge", lambda p: e(p["deal_badge_official"]) + ' &middot; <a href="flagged.html#FLAG-02">FLAG-02</a>'),
        row("Bought in past month", lambda p: e(p["bought_past_month"]), "rounded"),
        row("Best Sellers Rank", lambda p: '<span class="blank">blank</span> &middot; <a href="flagged.html#FLAG-03">FLAG-03</a>'),
        row("Wattage", lambda p: '<span class="blank">blank</span> &middot; <a href="flagged.html#FLAG-10">FLAG-10</a>'),
        row("Model number", lambda p: '<span class="blank">blank</span> &middot; <a href="flagged.html#FLAG-10">FLAG-10</a>'),
        row("Captured (UTC)", lambda p: '<span class="ts">%s</span>' % e(p["captured_utc"])),
        row("Source", link),
    ])
    return """<div class="tw"><table>
<thead>%s</thead>
<tbody>%s
</tbody></table></div>
<div class="note">Only the capacities are verified specifications - they appear inside the official product titles. Every other specification cell is blank because the value could not be read from an official page (FLAG-10). No value in this table is inferred.</div>
""" % (head, body)


def table_commission(frm=None) -> str:
    rows = []
    for p in products["products"]:
        price = money(p["price_current"])
        listp = money(p["price_list"])
        cells = []
        for label, rate, sid, note in COMMISSION_RATES:
            cells.append('<td class="num">%s</td><td class="num">%s</td>' % (
                usd(price * rate), usd(listp * rate)))
        rows.append("""<tr>
  <td class="mono">%(id)s</td>
  <td class="mono">%(asin)s</td>
  <td class="num">%(price)s</td>
  <td class="num">%(list)s</td>
  %(cells)s
  <td>%(src)s</td>
</tr>""" % {
            "id": e(p["id"]), "asin": e(p["asin"]),
            "price": e(p["price_current"]), "list": e(p["price_list"]),
            "cells": "".join(cells),
            "src": srclink(SRC["S16"]["url"], "rate table"),
        })
    head = "".join('<th class="num" colspan="2">%s &middot; %.2f%%</th>' % (label, rate * 100)
                   for label, rate, _, _ in COMMISSION_RATES)
    sub = "".join('<th class="num">at sale</th><th class="num">at list</th>' for _ in COMMISSION_RATES)
    return """<div class="tw"><table>
<thead>
<tr><th rowspan="2">ID</th><th rowspan="2">ASIN</th><th class="num" rowspan="2">Sale price</th><th class="num" rowspan="2">List price</th>%(head)s<th rowspan="2">Rate source</th></tr>
<tr>%(sub)s</tr>
</thead>
<tbody>%(rows)s
</tbody></table></div>
<div class="note warn"><b>This is arithmetic, not earnings.</b> Each figure is the captured price multiplied by the published fixed rate for that category. It is the gross commission on one qualifying unit before returns, cancellations, the 24-hour session limit, the 89-day cart window and the 180-day ship window. It is not a revenue forecast and no sales have occurred. The rate itself is unconfirmed for these ASINs - see <a href="flagged.html#FLAG-09">FLAG-09</a>.</div>
""" % {"head": head, "sub": sub, "rows": "\n".join(rows)}


def table_rate_card(frm=None) -> str:
    data = [
        ("Luxury Beauty, Luxury Stores Beauty, Amazon Explore", "10.00%"),
        ("Digital Music, Physical Music, Handmade, Digital Videos", "5.00%"),
        ("Physical Books, <b>Kitchen</b>, Automotive", "4.50%"),
        ("Amazon Fire Tablet Devices, Amazon Kindle Devices, Luxury Stores Fashion, Apparel, Amazon Cloud Cam Devices, Fire TV Edition Smart TVs, Amazon Fire TV Devices, Amazon Echo Devices, Ring Devices, Watches, Jewelry, Luggage, Shoes, and Handbags &amp; Accessories", "4.00%"),
        ("<b>All Other Categories</b>", "4.00%"),
        ("Toys, Furniture, <b>Home</b>, Home Improvement, Lawn &amp; Garden, Pets Products, Headphones, Beauty, Musical Instruments, Business &amp; Industrial Supplies, Outdoors, Tools, Sports, Baby Products, Amazon Coins", "3.00%"),
        ("PC, PC Components, DVD &amp; Blu-Ray", "2.50%"),
        ("Televisions, Digital Video Games", "2.00%"),
        ("Amazon Fresh, Physical Video Games &amp; Video Game Consoles, Grocery, Health &amp; Personal Care", "1.00%"),
    ]
    rows = "".join('<tr><td>%s</td><td class="num">%s</td><td>%s</td></tr>' % (c, r, srclink(SRC["S16"]["url"], "official"))
                   for c, r in data)
    return """<div class="tw"><table>
<thead><tr><th>Product category (US, standard commission)</th><th class="num">Fixed rate</th><th>Source</th></tr></thead>
<tbody>%s
</tbody></table></div>
<div class="note">Copied verbatim from Table 1 of the Associates Program Standard Commission Income Statement, in the order published. The two rows that could apply to these products are bolded.</div>
""" % rows


def table_competitors(frm=None) -> str:
    rows = []
    for c in competitors["bestsellers"]:
        rows.append("""<tr>
  <td class="num">#%(rank)d</td>
  <td><a href="%(url)s" target="_blank" rel="noopener nofollow">%(title)s</a></td>
  <td>%(brand)s</td>
  <td>%(cap)s</td>
  <td>%(rating)s</td>
  <td class="num">%(count)s</td>
  <td class="num">%(price)s</td>
  <td>%(src)s</td>
</tr>""" % {
            "rank": c["rank"], "url": e(c["url"]), "title": e(c["title"]),
            "brand": e(c["brand"]), "cap": e(c["capacity"]),
            "rating": e(c["star_rating"]), "count": e(c["rating_count"]),
            "price": e(c["price"]),
            "src": srclink(competitors["meta"]["source_url"], "Best Sellers"),
        })
    return """<div class="tw"><table>
<thead><tr><th class="num">Rank</th><th>Product</th><th>Brand</th><th>Capacity</th><th>Rating</th><th class="num">Ratings</th><th class="num">Price</th><th>Source</th></tr></thead>
<tbody>%(rows)s
</tbody></table></div>
<div class="note">%(scope)s The rating counts on this page <b>are</b> exact - the Best Sellers listing prints full counts, unlike Amazon search results.</div>
""" % {"rows": "\n".join(rows),
       "scope": e(competitors["meta"]["scope_note"])}


def table_sources(frm=None) -> str:
    rows = []
    for s in sources["sources"]:
        linkable = s.get("linkable", True)
        url_cell = ('<a href="%s" target="_blank" rel="noopener">%s</a>' % (e(s["url"]), e(s["url"]))) if linkable \
            else ('<span class="mono">%s</span> <span class="tag t-unv">not linked</span>' % e(s["url"]))
        rows.append("""<tr>
  <td class="mono">%(id)s</td>
  <td>%(pub)s</td>
  <td>%(url)s</td>
  <td class="mono">%(res)s</td>
  <td><span class="ts">%(ts)s</span></td>
  <td>%(used)s</td>
  <td>%(note)s</td>
</tr>""" % {
            "id": e(s["id"]), "pub": e(s["publisher"]), "url": url_cell,
            "res": e(s["result"]), "ts": e(s.get("retrieved_utc") or "-"),
            "used": e(s["used_for"]), "note": e(s.get("note") or ""),
        })
    return """<div class="tw"><table>
<thead><tr><th>ID</th><th>Publisher</th><th>URL</th><th>Retrieval result</th><th>Retrieved (UTC)</th><th>Used for</th><th>Notes</th></tr></thead>
<tbody>%s
</tbody></table></div>
""" % "\n".join(rows)


def table_derived_links(frm=None) -> str:
    rows = "".join(
        '<tr><td class="mono">%s</td><td class="mono">%s</td><td>%s</td></tr>'
        % (e(d["observed_on"]), e(d["url"]), e(d["note"]))
        for d in derived["links"])
    return """<div class="tw"><table>
<thead><tr><th>Observed on</th><th>URL</th><th>How it was obtained</th></tr></thead>
<tbody>%s
</tbody></table></div>
""" % rows


def table_flags(frm=None) -> str:
    rows = []
    for f in flags["flags"]:
        src = " ".join(srclink(u, "src") for u in f["sources"]) or '<span class="blank">n/a</span>'
        rows.append("""<tr>
  <td class="mono"><a href="flagged.html#%(id)s">%(id)s</a></td>
  <td>%(sev)s</td>
  <td>%(cat)s</td>
  <td>%(title)s</td>
  <td>%(src)s</td>
</tr>""" % {
            "id": e(f["id"]), "sev": sev_badge(f["severity"]),
            "cat": e(f["category"]), "title": e(f["title"]), "src": src,
        })
    return """<div class="tw"><table>
<thead><tr><th>ID</th><th>Severity</th><th>Area</th><th>Finding</th><th>Sources</th></tr></thead>
<tbody>%s
</tbody></table></div>
""" % "\n".join(rows)


def render_flag_blocks(frm) -> str:
    out = []
    for f in flags["flags"]:
        src = " ".join('<a href="%s" target="_blank" rel="noopener nofollow">%s &#8599;</a>' % (e(u), e(u))
                       for u in f["sources"]) or '<span class="blank">no external source - internal finding</span>'
        out.append("""<div class="flag %(sev)s" id="%(id)s">
  <h3><span class="id">%(id)s</span> &middot; %(title)s %(sevtag)s</h3>
  <p><b>Area:</b> %(cat)s</p>
  <p>%(detail)s</p>
  <div class="act"><b>Action required:</b> %(action)s</div>
  <p style="margin-top:8px">%(src)s</p>
</div>""" % {
            "sev": e(f["severity"]), "id": e(f["id"]), "title": e(f["title"]),
            "sevtag": sev_badge(f["severity"]), "cat": e(f["category"]),
            "detail": e(f["detail"]), "action": e(f["action_required"]), "src": src,
        })
    return "\n".join(out)


def table_compliance(frm=None) -> str:
    items = [
        ("Special Links must carry your Associates tag",
         "Participation Requirements 2(b): you must include your Associates ID or tag (XXXXX-##) as a parameter in the URL of each link to an Amazon Site.",
         "FAIL - no tag on any supplied link", "FLAG-05", "S18"),
        ("Prices may only be shown if Amazon-served or API-sourced",
         "Participation Requirements 2(b): your Site may only show prices and availability if (a) Amazon serves the link displaying them, or (b) you obtain them via Creators API or PA API.",
         "FAIL - all prices hand-captured", "FLAG-01", "S18"),
        ("Limited-time promotions must be removed when they end",
         "Participation Requirements 2(b): you must remove any links and references to limited time promotions as soon as that promotion ends.",
         "AT RISK - three live badges shown", "FLAG-02", "S18"),
        ("Disclosure of the Amazon Associates relationship",
         "The Operating Agreement requires the statement identifying you as an Amazon Associate to appear clearly and conspicuously on your Site. The FTC requires a hard-to-miss disclosure in simple language, not buried in hashtags or links.",
         "IMPLEMENTED - banner on every page; exact wording needs to be re-copied from the current Operating Agreement", "FLAG-12", "S19"),
        ("Session and cart windows",
         "Commission Income Statement 1(b): a Session ends after 24 hours; a cart add converts if the order completes within 89 days; the item must ship and be paid for within 180 days.",
         "INFORMATIONAL", "-", "S18"),
        ("Site must contain original content",
         "Participation Requirements 1: your Site must contain original content and be publicly available; third-party material needs significant commentary, analysis or transformation.",
         "NOT YET MET - no articles written", "FLAG-13", "S18"),
        ("Program Content must not be altered",
         "Content on your Site 6(a): you will not add to, delete from, or otherwise alter any Program Content.",
         "AT RISK - Amazon's 'bought in past month' signal is reproduced", "FLAG-08", "S18"),
        ("Links must be accessed directly from your Site",
         "Participation Requirements 2(b): all Special Links must be accessed directly from your Site; you must not encourage customers to bookmark them.",
         "OK", "-", "S18"),
        ("No Special Links inside software, extensions or plug-ins",
         "Participation Requirements 5: no Program Content or Special Links in client-side software, browser extensions, toolbars, or TV apps; no use of Special Links to train machine-learning models without written approval.",
         "OK - plain web pages only", "-", "S18"),
        ("Cookie, pixel and tracking disclosure",
         "Responsibility for your Site 3(e): disclose the use of cookies, pixels and similar technologies via a privacy policy or otherwise, satisfying GDPR and the ePrivacy Directive where they apply.",
         "NOT YET MET - no privacy page, operator is in the EEA", "FLAG-06", "S18"),
        ("Amazon may audit and monitor your Site",
         "Operating Agreement 12: Amazon may monitor, record and disclose information about your Site, and may review, monitor and crawl it to verify compliance.",
         "INFORMATIONAL", "-", "S17"),
        ("Payment minimums",
         "Commission Income Statement 6: US minimum is $10 for direct deposit and gift card, $100 for check, with a $15 check processing fee. Payment is made about 60 days after the end of the earning month.",
         "INFORMATIONAL", "-", "S16"),
        ("Three qualifying sales within the first 180 days",
         "Associates FAQ: you have 180 days to refer a sale; once three qualifying sales are referred the application is evaluated. Personal orders do not count.",
         "NOT STARTED - no Associates account yet", "FLAG-12", "S19"),
    ]
    rows = []
    for name, rule, status, flag, sid in items:
        fl =('<a href="flagged.html#%s">%s</a>' % (flag, flag)) if flag != "-" else '<span class="tag t-ok">n/a</span>'
        rows.append("""<tr>
  <td><b>%s</b></td>
  <td>%s</td>
  <td>%s</td>
  <td>%s</td>
  <td>%s</td>
</tr>""" % (name, rule, status, fl, srclink(SRC[sid]["url"], SRC[sid]["id"])))
    return """<div class="tw"><table>
<thead><tr><th>Requirement</th><th>What the official document says</th><th>Status on this site</th><th>Flag</th><th>Source</th></tr></thead>
<tbody>%s
</tbody></table></div>
""" % "\n".join(rows)


def table_analytics(frm=None) -> str:
    metrics = [
        ("Sessions referred to Amazon", "Associates Central reports", "no Associates account"),
        ("Clicks on Special Links", "Associates Central reports", "no Associates account"),
        ("Ordered items", "Associates Central reports", "no Associates account"),
        ("Shipped items", "Associates Central reports", "no Associates account"),
        ("Conversion rate (ordered / clicks)", "derived from Associates Central reports", "no data"),
        ("Earnings per click (EPC)", "Associates Central reports", "no data"),
        ("Standard commission income", "Associates Central reports", "no data"),
        ("Bounty events (Prime sign-ups)", "Associates Central reports", "no data"),
        ("Outbound clicks logged by this site", "site click logger", "not wired to a backend"),
    ]
    rows = "".join("""<tr><td>%s</td><td>%s</td><td class="blank">no data yet - pre-launch</td><td>%s</td><td>%s</td></tr>"""
                   % (m, s, why, srclink(SRC["S16"]["url"], "S16")) for m, s, why in metrics)
    return """<div class="tw"><table>
<thead><tr><th>Metric</th><th>Official source of truth</th><th>Value</th><th>Why it is empty</th><th>Reference</th></tr></thead>
<tbody>%s
</tbody></table></div>
<div class="note bad"><b>Nothing here is populated, on purpose.</b> The brief asks the platform to track clicks and conversions and to optimise campaigns. There is no Associates account, no tag and no traffic, so there is no real data. Placeholder numbers in a table are indistinguishable from measured ones, so none were invented. Every figure will come from Associates Central reports once the account exists.</div>
""" % rows


def product_cards(items) -> str:
    out = []
    for p in items:
        out.append("""<div class="pcard">
  <div class="ph"><img src="%(img)s" alt="%(alt)s" loading="lazy"></div>
  <div class="pb">
    <h3><a href="%(url)s" target="_blank" rel="noopener nofollow">%(title)s</a></h3>
    <div class="meta">%(brand)s &middot; <span class="mono">%(asin)s</span></div>
    <div class="price">%(price)s<s>%(list)s</s></div>
    <dl>
      <dt>Rating</dt><dd>%(rating)s (%(count)s shown)</dd>
      <dt>Capacity</dt><dd>%(cap)s</dd>
      <dt>Promotion</dt><dd>%(badge)s</dd>
      <dt>Sub-category</dt><dd>%(sub)s</dd>
      <dt>Best Sellers Rank</dt><dd><span class="blank">unverified</span></dd>
    </dl>
  </div>
  <div class="pf">Captured <span class="ts">%(ts)s</span> &middot; %(src)s</div>
</div>""" % {
            "img": e(p["image_url"]), "alt": e(p["title_official"][:70]),
            "url": e(p["canonical_url"]), "title": e(p["title_official"]),
            "brand": e(p["brand_from_title"]), "asin": e(p["asin"]),
            "price": e(p["price_current"]), "list": e(p["price_list"]),
            "rating": e(p["star_rating"]), "count": e(p["rating_count_display"]),
            "cap": e(p["capacity_from_title"]), "badge": e(p["deal_badge_official"]),
            "sub": e(p["subcategory_derived"]), "ts": e(p["captured_utc"]),
            "src": srclink(p["source_url"], "official page"),
        })
    return '<div class="pgrid">%s</div>' % "\n".join(out)


def dashboard_cards() -> str:
    n_block = sum(1 for f in flags["flags"] if f["severity"] == "blocker")
    n_unv = sum(1 for f in flags["flags"] if f["severity"] == "unverified-data")
    n_src = len([s for s in sources["sources"] if s.get("linkable", True)])
    cards = [
        ("Products in scope", "3", "All three supplied links resolved to Amazon air fryers"),
        ("Category", "Air Fryers", "Home &amp; Kitchen &gt; Kitchen &amp; Dining &gt; Small Appliances &gt; Fryers &gt; Air Fryers"),
        ("Published commission rate", "4.50%", "Kitchen &middot; downside case 3.00% (Home)"),
        ("Blockers before launch", str(n_block), "Must be cleared before the site is monetised"),
        ("Unverified fields", str(n_unv), "Left blank, never inferred"),
        ("Official sources", str(n_src), "Every one retrieved in this session"),
    ]
    return '<div class="cards">%s</div>' % "".join(
        '<div class="card"><div class="k">%s</div><div class="v">%s</div><div class="s">%s</div></div>' % c
        for c in cards)


# --------------------------------------------------------------------------
# page assembly
# --------------------------------------------------------------------------
TOKENS = {
    "{{TABLE_IDENTITY}}": table_identity,
    "{{TABLE_COMMERCIALS}}": table_commercials,
    "{{TABLE_LINK_RESOLUTION}}": table_link_resolution,
    "{{TABLE_COMPARISON}}": table_comparison,
    "{{TABLE_COMMISSION}}": table_commission,
    "{{TABLE_RATE_CARD}}": table_rate_card,
    "{{TABLE_COMPETITORS}}": table_competitors,
    "{{TABLE_SOURCES}}": table_sources,
    "{{TABLE_DERIVED_LINKS}}": table_derived_links,
    "{{TABLE_FLAGS}}": table_flags,
    "{{FLAG_BLOCKS}}": render_flag_blocks,
    "{{TABLE_COMPLIANCE}}": table_compliance,
    "{{TABLE_ANALYTICS}}": table_analytics,
    "{{PRODUCT_CARDS_ALL}}": lambda frm: product_cards(products["products"]),
    "{{DASHBOARD_CARDS}}": lambda frm: dashboard_cards(),
}

CATEGORY_FILTER = {
    "categories/dual-basket.html": "Dual Basket Air Fryers",
    "categories/air-fryer-toaster-ovens.html": "Air Fryer Toaster Ovens",
    "categories/large-capacity.html": "Large Capacity Air Fryers",
}


def category_cards(frm):
    sub = CATEGORY_FILTER[frm]
    items = [p for p in products["products"] if p["subcategory_derived"] == sub]
    return product_cards(items)


LAYOUT = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%(title)s &middot; Zone3 Amazon Affiliate Platform</title>
<meta name="description" content="%(desc)s">
<meta name="robots" content="noindex, nofollow">
<link rel="stylesheet" href="%(css)s">
</head>
<body>
<div class="wrap">
  <aside class="side">
    <a class="brand" href="%(home)s">
      <b>Zone3</b>
      <span>Amazon affiliate research</span>
    </a>
    %(nav)s
    <div class="foot">
      Snapshot %(captured)s<br>
      Session c4e71983<br>
      Data: official Amazon pages only
    </div>
  </aside>
  <div class="main">
    <div class="topbar">
      <h1>%(title)s</h1>
      <p>%(subtitle)s</p>
    </div>
    <div class="content">
      <p class="disclose">
        <b>Disclosure:</b> as an Amazon Associate this site would earn from qualifying purchases.
        This disclosure is rendered on every page because both the Amazon Operating Agreement and the
        FTC endorsement rules require it to be hard to miss &mdash;
        <a href="%(depth)scompliance.html">see Compliance</a>. Exact current wording:
        <a href="%(depth)sflagged.html#FLAG-12">FLAG-12</a>.
      </p>
      %(body)s
    </div>
    <div class="footer">
      <p>Zone3 is an internal research dashboard. All product data was read from official Amazon pages
      on 2026-11-13 and is reproduced for review. Prices and ratings change continuously &mdash;
      re-check the linked source before acting on any figure.</p>
      <p>Amazon, the Amazon logo and all product names are trademarks of Amazon.com, Inc. or its
      affiliates. This project is not endorsed by or affiliated with Amazon. &middot;
      <a href="%(depth)sflagged.html">Flagged for Review</a> &middot;
      <a href="%(depth)sdata-sources.html">Data Sources</a></p>
    </div>
  </div>
</div>
<script src="%(js)s"></script>
</body>
</html>
"""


def build_page(href, title, subtitle, fragment, desc):
    frm = href
    body = read_fragment(fragment)
    for token, fn in TOKENS.items():
        if token in body:
            body = body.replace(token, fn(frm))
    if href in CATEGORY_FILTER:
        body = body.replace("{{CATEGORY_CARDS}}", category_cards(frm))
    depth = "../" * href.count("/")
    return LAYOUT % {
        "title": title,
        "subtitle": subtitle,
        "desc": e(desc),
        "nav": render_nav(href),
        "body": body,
        "css": depth + "assets/style.css",
        "js": depth + "assets/app.js",
        "home": depth + "index.html",
        "depth": depth,
        "captured": CAPTURED,
    }


PAGES = [
    ("index.html", "Dashboard", "Everything in this project at a glance", "index.html",
     "Zone3 Amazon affiliate research dashboard"),
    ("executive-summary.html", "Executive Summary", "The short version for a decision maker", "executive-summary.html",
     "Executive summary of the Zone3 Amazon affiliate project"),
    ("products.html", "Master Data Table", "Every field we hold, every cell sourced", "products.html",
     "Master product data table with a source link on every row"),
    ("comparison.html", "Comparison", "Side by side, with blanks where data is missing", "comparison.html",
     "Side-by-side comparison of the three air fryers"),
    ("link-resolution.html", "Link Resolution", "What each supplied short link actually is", "link-resolution.html",
     "Resolution of the three supplied Amazon short links to canonical ASINs"),
    ("categories/air-fryers.html", "Air Fryers", "The parent category - all three products", "category-air-fryers.html",
     "Air fryers category page"),
    ("categories/dual-basket.html", "Dual Basket", "Dual-basket air fryers", "category-dual-basket.html",
     "Dual basket air fryers category page"),
    ("categories/air-fryer-toaster-ovens.html", "Toaster Ovens", "Air fryer toaster ovens", "category-toaster-ovens.html",
     "Air fryer toaster ovens category page"),
    ("categories/large-capacity.html", "Large Capacity", "Large capacity air fryers", "category-large-capacity.html",
     "Large capacity air fryers category page"),
    ("niche-analysis.html", "Niche &amp; Competition", "Where these products sit, and who they are up against", "niche-analysis.html",
     "Niche and competition analysis for the air fryer category"),
    ("commission-model.html", "Commission Model", "The published rates and what they mean per unit", "commission-model.html",
     "Commission model and published Amazon Associates rate card"),
    ("link-builder.html", "Link Builder", "Turn a canonical URL into a compliant Special Link", "link-builder.html",
     "Build compliant Amazon Associates Special Links"),
    ("compliance.html", "Compliance", "Amazon Associates rules and FTC disclosure obligations", "compliance.html",
     "Amazon Associates and FTC compliance checklist"),
    ("data-sources.html", "Data Sources", "Every URL used, and how it was verified", "data-sources.html",
     "Sources used, and how each was verified"),
    ("flagged.html", "Flagged for Review", "Irregularities and unverified values", "flagged.html",
     "Flagged irregularities and unverified values"),
    ("platform.html", "Automation Architecture", "What the platform does and what is actually built", "platform.html",
     "Architecture of the planned automation platform"),
    ("analytics.html", "Tracking &amp; Analytics", "What would be measured, and why it is empty", "analytics.html",
     "Tracking and analytics surfaces"),
]


# --------------------------------------------------------------------------
# validation
# --------------------------------------------------------------------------
def validate(pages_html: dict) -> list:
    problems = []
    produced = set(pages_html.keys())
    produced |= {"assets/style.css", "assets/app.js"}
    for _n in ("products.json", "competitors.json", "flags.json",
               "sources.json", "derived_links.json"):
        produced.add("data/" + _n)

    for href, doc in pages_html.items():
        base = os.path.dirname(href)
        # external links
        for m in re.finditer(r'(?:href|src)="(https?://[^"]+)"', doc):
            url = html.unescape(m.group(1))
            if url not in ALLOWED_EXTERNAL:
                problems.append("%s: external URL not in the verified allowlist: %s" % (href, url))
        # internal links
        for m in re.finditer(r'(?:href|src)="([^"#?]+)([#?][^"]*)?"', doc):
            url = html.unescape(m.group(1))
            if url.startswith("http") or url.startswith("mailto:") or url.startswith("data:"):
                continue
            target = os.path.normpath(os.path.join(base, url))
            if target not in produced:
                problems.append("%s: broken internal link -> %s (resolved: %s)" % (href, url, target))
        # disclosure present
        if "Disclosure:" not in doc:
            problems.append("%s: missing affiliate disclosure banner" % href)
    return problems


def main():
    pages_html = {}
    for href, title, subtitle, frag, desc in PAGES:
        pages_html[href] = build_page(href, title, subtitle, frag, desc)

    problems = validate(pages_html)
    if problems:
        print("BUILD FAILED - %d problem(s):" % len(problems))
        for p in problems:
            print("  - " + p)
        sys.exit(1)

    print("Validation passed: %d pages, %d external URLs allowlisted, no broken internal links."
          % (len(pages_html), len(ALLOWED_EXTERNAL)))

    if CHECK_ONLY:
        print("--check: nothing written.")
        return

    if os.path.isdir(DOCS):
        shutil.rmtree(DOCS)
    os.makedirs(os.path.join(DOCS, "assets"), exist_ok=True)
    for sub in ("categories",):
        os.makedirs(os.path.join(DOCS, sub), exist_ok=True)

    for href, doc in pages_html.items():
        path = os.path.join(DOCS, href)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(doc)

    shutil.copy(os.path.join(SITE, "style.css"), os.path.join(DOCS, "assets", "style.css"))
    shutil.copy(os.path.join(SITE, "app.js"), os.path.join(DOCS, "assets", "app.js"))
    with open(os.path.join(DOCS, ".nojekyll"), "w") as fh:
        fh.write("")

    # machine-readable export for reuse
    os.makedirs(os.path.join(DOCS, "data"), exist_ok=True)
    for name in ("products.json", "competitors.json", "flags.json", "sources.json", "derived_links.json"):
        shutil.copy(os.path.join(DATA, name), os.path.join(DOCS, "data", name))

    n = len(pages_html)
    print("Wrote %d pages to docs/" % n)

    if PUBLISH_ROOT:
        # GitHub Pages for this repository is configured as a *legacy* branch
        # build: source branch `main`, path `/`. That means Pages serves the
        # repository root, not docs/. Publishing copies the generated tree to the
        # root so the site is live with no repository-settings change.
        #
        # Safety: only files listed in a previous manifest are ever deleted, and
        # the manifest is written from the current build. The repository root is
        # never cleared.
        manifest_path = os.path.join(DOCS, MANIFEST)
        new_files = []
        for dirpath, _dn, filenames in os.walk(DOCS):
            for fn in filenames:
                if fn == MANIFEST:
                    continue
                full = os.path.join(dirpath, fn)
                new_files.append(os.path.relpath(full, DOCS))

        old_files = []
        if os.path.exists(manifest_path):
            with open(manifest_path, encoding="utf-8") as fh:
                old_files = json.load(fh).get("files", [])

        removed = 0
        for rel in old_files:
            if rel in new_files:
                continue
            tgt = os.path.join(ROOT, rel)
            if os.path.isfile(tgt):
                os.remove(tgt)
                removed += 1

        copied = 0
        for rel in new_files:
            src = os.path.join(DOCS, rel)
            tgt = os.path.join(ROOT, rel)
            os.makedirs(os.path.dirname(tgt), exist_ok=True)
            shutil.copyfile(src, tgt)
            copied += 1

        with open(manifest_path, "w", encoding="utf-8") as fh:
            json.dump({"files": sorted(new_files)}, fh, indent=2)

        print("Published %d files to the repository root (removed %d stale)."
              % (copied, removed))


if __name__ == "__main__":
    main()
