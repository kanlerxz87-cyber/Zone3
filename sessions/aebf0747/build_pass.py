#!/usr/bin/env python3
"""Generates the publication-layer pages for session aebf0747.

Writes:
  index.html                              publication front page (products first)
  dashboard-register.html                 the previous root page, kept unchanged (copied once)
  guides/index.html + 4 guide pages       question-shaped guides (working titles)
  intent-record/index.html                product-intent confirmation record
  publication-pass.html                   this pass: summary, measurement status, flags, verification
  feed.xml                                RSS 2.0 feed of the guides
  sessions/aebf0747/verification.md       verification record (same rows as the page)
  sessions/aebf0747/EXECUTIVE-SUMMARY.md  executive summary (same figures as the page)

Then runs publish_pass.py over the whole tree (disclosure, footer, sponsored links, head markup).

    python3 sessions/aebf0747/build_pass.py
"""
from __future__ import annotations

import datetime as dt
import html
import json
import pathlib
import sys
from email.utils import format_datetime

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))
import publish_pass  # noqa: E402

SITE_URL = "https://kanlerxz87-cyber.github.io/Zone3/"
OBSERVED_ON = "2026-11-17"
PUB_DATE = dt.datetime(2026, 11, 17, 9, 0, tzinfo=dt.timezone.utc)
DISCLOSURE = publish_pass.DISCLOSURE
FRONT_MARK = "<!-- aebf0747-front -->"

INTENT = json.loads((HERE / "intent-record.json").read_text(encoding="utf-8"))
ROWS = INTENT["rows"]
DP = {r["observed_redirect_asin"]: r["observed_redirect_url"] for r in ROWS}


def esc(s: str) -> str:
    return html.escape(s, quote=True)


def prefix_for(rel: str) -> str:
    return publish_pass.prefix_for(rel)


# ---------------------------------------------------------------- shared chrome

NAV = [
    ("index.html", "Home"),
    ("shop/index.html", "Shop"),
    ("guides/index.html", "Guides"),
    ("marketing/comparison.html", "Compare"),
    ("articles/index.html", "Articles"),
]

# The canonical list is shared with the footer publisher so the operational pages stay
# reachable without turning the reader-facing masthead into a wall of dashboard links.
NAV_GROUPS = publish_pass.FOOTER_GROUPS


def masthead(prefix: str, current: str) -> str:
    links = []
    for path, label in NAV:
        cur = ' aria-current="page"' if path == current else ""
        links.append(f'<a href="{prefix}{path}"{cur}>{esc(label)}</a>')
    grouped = []
    primary_paths = {path for path, _label in NAV}
    for group, entries in NAV_GROUPS:
        items = []
        for path, label in entries:
            if path in primary_paths:
                continue
            cur = ' aria-current="page"' if path == current else ""
            items.append(f'<a href="{prefix}{path}"{cur}>{esc(label)}</a>')
        if items:
            grouped.append(
                f'<section class="z3-tools-group"><h3>{esc(group)}</h3>'
                + "".join(items) + "</section>"
            )
    tools = (
        '<details class="z3-nav-tools"><summary>Explore</summary>'
        '<div class="z3-nav-panel" aria-label="Explore pages">'
        + "".join(grouped) + '</div></details>'
    )
    return (
        '<!-- z3:masthead --><header class="z3-mast topbar"><div class="z3-wrap">'
        f'<a class="z3-brand" href="{prefix}index.html">Zone3<small>The kitchen buying desk</small></a>'
        '<nav class="z3-nav" aria-label="Main">' + "".join(links) + tools + '</nav>'
        '</div></header>\n'
    )


def shell(rel: str, title: str, desc: str, body: str, extra_head: str = "") -> str:
    prefix = prefix_for(rel)
    canon = SITE_URL + ("" if rel == "index.html" else rel)
    return (
        "<!doctype html>\n<html lang=\"en\">\n<head>\n"
        '<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        f"<title>{esc(title)}</title>\n"
        f'<meta name="description" content="{esc(desc)}">\n'
        f'<link rel="canonical" href="{canon}">\n'
        '<!-- z3:css --><link rel="stylesheet" href="' + prefix + 'assets/zone3-publication.css">\n'
        '<!-- z3:rss --><link rel="alternate" type="application/rss+xml" title="Zone3 guides" href="' + prefix + 'feed.xml">\n'
        + extra_head +
        "</head>\n<body class=\"z3-body\">\n"
        + masthead(prefix, rel.split("#")[0])
        + '<a class="z3-skip" href="#main">Skip to content</a>\n'
        + '<main id="main" class="z3-main"><div class="z3-wrap">\n'
        + body +
        "\n</div></main>\n</body>\n</html>\n"
    )


def plink(asin: str, label: str | None = None) -> str:
    url = DP[asin]
    return f'<a href="{url}">{esc(label or url)}</a>'


def short_link_for(asin: str) -> str:
    for r in ROWS:
        if r["observed_redirect_asin"] == asin:
            return r["submitted_link"]
    raise KeyError(asin)


def row_by_asin(asin: str) -> dict:
    return next(r for r in ROWS if r["observed_redirect_asin"] == asin)


# ---------------------------------------------------------------- front page

def front_page() -> str:
    air_fryers = [r for r in ROWS if r.get("category_group") == "Air fryers"]
    thermometers = [r for r in ROWS if r.get("category_group") == "Meat thermometers"]
    kinds = {
        "B0CDY277D3": ("Dual-basket air fryer", "z3-product-mark--basket"),
        "B09B7SB46R": ("French-door air fryer oven", "z3-product-mark--oven"),
        "B08DKYBTPH": ("Basket air fryer", "z3-product-mark--basket"),
        "B0DHZTCNR5": ("Digital meat thermometer", "z3-product-mark--thermometer"),
        "B0DZFD6R9Z": ("Wireless meat thermometer", "z3-product-mark--thermometer"),
    }

    def product_card(r: dict, index: int, total: int) -> str:
        label, art = kinds[r["observed_redirect_asin"]]
        title = r["short_name"]
        return (
            '<article class="z3-product-card">'
            f'<div class="z3-product-card__top"><span class="z3-product-card__category">{esc(label)}</span>'
            f'<span class="z3-product-card__number">{index:02d} <i>/ {total:02d}</i></span></div>'
            f'<div class="z3-product-mark {art}" aria-hidden="true"><span>{index:02d}</span></div>'
            f'<h3>{esc(title)}</h3>'
            f'<p class="z3-product-card__meta">Listing opened by a submitted link · checked {OBSERVED_ON}</p>'
            '<div class="z3-product-card__actions">'
            f'<a class="z3-buy-link" href="{r["submitted_link"]}" rel="sponsored">View on Amazon <span aria-hidden="true">↗</span></a><span class="z3-sponsored-chip">Sponsored</span>'
            f'<a class="z3-record-link" href="intent-record/index.html#row-{r["n"]}">Listing details</a>'
            '</div></article>'
        )

    cards = "\n".join(product_card(r, i, len(air_fryers)) for i, r in enumerate(air_fryers, 1))
    thermometer_cards = "\n".join(
        product_card(r, i, len(thermometers)) for i, r in enumerate(thermometers, 1)
    )
    guide_cards = []
    for i, g in enumerate(GUIDES, 1):
        guide_cards.append(
            '<article class="z3-guide-card">'
            f'<span class="z3-guide-card__number">Guide {i:02d}</span>'
            f'<h3>{esc(g["title"])}</h3>'
            f'<p>{esc(g["dek"])}</p>'
            f'<a href="guides/{g["slug"]}.html">Read the guide <span aria-hidden="true">→</span></a>'
            '</article>'
        )

    body = f"""
<section class="z3-home-hero" aria-labelledby="home-title">
  <div class="z3-home-hero__copy">
    <p class="z3-eyebrow">Zone3 · The kitchen buying desk</p>
    <h1 class="z3-home-title" id="home-title">Better questions.<br><em>Better kitchen buys.</em></h1>
    <p class="z3-home-lede">A calmer way to compare the details behind kitchen listings. Start with air fryers, follow the questions that matter, and see what is still worth checking before you choose.</p>
    <div class="z3-home-actions">
      <a class="z3-home-button" href="#air-fryers">Browse air fryers <span aria-hidden="true">↓</span></a>
      <a class="z3-home-text-link" href="guides/index.html">Read the buyer’s guides <span aria-hidden="true">→</span></a>
    </div>
    <p class="z3-home-byline">Useful comparisons, written from the listing details—not pretend hands-on reviews.</p>
  </div>
  <aside class="z3-home-hero__art" aria-label="A preview of the questions covered in our buying guides">
    <span class="z3-art-kicker">The buyer’s notebook</span>
    <span class="z3-art-title">Start with what<br>you actually need.</span>
    <span class="z3-art-rule"></span>
    <span class="z3-art-row"><b>01</b> Form &amp; footprint</span>
    <span class="z3-art-row"><b>02</b> Capacity &amp; layout</span>
    <span class="z3-art-row"><b>03</b> Cleanup &amp; care</span>
    <a href="guides/index.html">Explore the questions <span aria-hidden="true">↗</span></a>
    <span class="z3-art-stamp" aria-hidden="true">Z3<br>FIELD<br>NOTES</span>
  </aside>
</section>

<section class="z3-home-section" id="air-fryers" aria-labelledby="air-fryer-heading">
  <div class="z3-section-heading">
    <div><p class="z3-eyebrow">The starting shelf</p><h2 id="air-fryer-heading">Air fryers to compare</h2></div>
    <a class="z3-section-link" href="marketing/comparison.html">Compare the listings <span aria-hidden="true">→</span></a>
  </div>
  <p class="z3-section-intro">Three listing snapshots, with the details shown plainly and no made-up verdicts. Open a product listing or use the guides to decide what to compare.</p>
  <div class="z3-product-grid">{cards}</div>
  <p class="z3-home-caveat">The product names and listing details below reflect the pages opened by the submitted links on {OBSERVED_ON}. The intended product match and link attribution are not yet confirmed. <a href="intent-record/index.html">See the separate product-intent record</a>.</p>
</section>

<section class="z3-home-section z3-home-section--soft" aria-labelledby="guides-heading">
  <div class="z3-section-heading">
    <div><p class="z3-eyebrow">Read before you decide</p><h2 id="guides-heading">Questions worth asking</h2></div>
    <a class="z3-section-link" href="guides/index.html">All buyer’s guides <span aria-hidden="true">→</span></a>
  </div>
  <p class="z3-section-intro">Practical starting points—not claims about what is trending or what is best.</p>
  <div class="z3-guide-grid">{"".join(guide_cards)}</div>
</section>

<section class="z3-home-section" aria-labelledby="other-tools-heading">
  <div class="z3-section-heading">
    <div><p class="z3-eyebrow">A separate kitchen category</p><h2 id="other-tools-heading">Meat thermometers</h2></div>
    <a class="z3-section-link" href="shop/meat-thermometers/index.html">Browse the category <span aria-hidden="true">→</span></a>
  </div>
  <p class="z3-section-intro">Two observed listings sit outside the air-fryer guide collection. They’re kept in their own category rather than folded into an unrelated comparison.</p>
  <div class="z3-product-grid z3-product-grid--compact">{thermometer_cards}</div>
</section>

<section class="z3-home-review" aria-labelledby="review-heading">
  <div><p class="z3-eyebrow">Help choose what comes next</p><h2 id="review-heading">Good publishing starts with good questions.</h2>
  <p>See the proposed paths, the information we still need, and how each gap could be checked. Suggestions are reviewable proposals—not silent changes.</p></div>
  <div class="z3-review-actions"><a href="suggestions.html">Review suggestions <span aria-hidden="true">→</span></a><a href="decision-queue.html">Open decision queue <span aria-hidden="true">→</span></a><a href="site/answers.html">Known facts &amp; open questions <span aria-hidden="true">→</span></a><a href="flagged.html">See flagged items <span aria-hidden="true">→</span></a></div>
</section>

<section class="z3-home-note" aria-label="Editorial and affiliate note">
  <span class="z3-home-note__label">How we work</span>
  <p>We don’t publish a price, rating, review count, or first-hand verdict unless the permitted source and experience are actually available. That keeps each guide useful without pretending to know more than the listing tells us.</p>
  <a href="executive-summary/index.html">Read the executive summary <span aria-hidden="true">→</span></a>
</section>
"""
    return shell(
        "index.html",
        "Zone3 | Kitchen buying guides, air fryers & kitchen tools",
        "Thoughtful buying guides and comparisons for air fryers and kitchen tools. Read clear, question-led guides and see which listing details still need checking.",
        body,
        extra_head=FRONT_MARK + "\n",
    )


# ---------------------------------------------------------------- guides

def listing_table(rows_html: str, headers: list[str]) -> str:
    th = "".join(f"<th>{esc(h)}</th>" for h in headers)
    return f'<div class="z3-table-wrap"><table class="z3-table"><thead><tr>{th}</tr></thead><tbody>{rows_html}</tbody></table></div>'


GUIDES: list[dict] = [
    {
        "slug": "basket-or-oven-style",
        "title": "Basket or oven-style air fryer: what should you compare?",
        "dek": "Start with the form, then check what the title says about compartments, presets and accessories.",
        "body": """
<h2 class="z3-h2">The short answer</h2>
<p>Read the form from the listing, then count the compartments. The three air-fryer listings we opened on {d} do not use one vocabulary for the form. The 6QT title calls itself an “Air Fryer Oven” and also names “2 Independent 3Qt” baskets, so the word “oven” on its own tells you little.</p>
<h2 class="z3-h2">What the three titles say</h2>
{t1}
<h2 class="z3-h2">A checklist before you choose</h2>
<ol class="z3-prose">
<li>Write down the form word in the title and the form word in the listing’s own product details. Note whether they agree.</li>
<li>Count the cooking compartments. The 6QT title states two baskets. The 8QT title names one basket. The 26QT title names an interior and six accessories, but no compartment count.</li>
<li>Check any preset count against the list of presets. The 26QT title says “24 One-Touch Preset Options”. The 8QT title says “4-in-1”. We did not verify the presets behind either phrase.</li>
<li>Then compare capacity (see the capacity checklist) and cleanup (see the cleanup guide) before you decide.</li>
</ol>
<h2 class="z3-h2">What this guide does not say</h2>
<p>It does not say which form is better. It does not rank the three products. It uses no price, star rating or review count.</p>
<h2 class="z3-h2">Listings this guide is based on</h2>
{links}
""",
        "not_verified": [
            "The full product-details tables and bullet lists of the three listings were not read line by line for this guide.",
            "Preset lists, temperature ranges and the names of the included accessories.",
        ],
        "related": ["capacity-checklist", "cleanup-and-counter-space"],
    },
    {
        "slug": "capacity-checklist",
        "title": "A no-hype checklist for comparing air fryer capacity",
        "dek": "Capacity numbers on listings can measure different things. Check what the number measures before you compare two.",
        "body": """
<h2 class="z3-h2">Three capacity styles on the same listings</h2>
{t2}
<h2 class="z3-h2">The checklist</h2>
<ol class="z3-prose">
<li><strong>Total or per compartment?</strong> The 6QT title gives “6 Quart” and also “2 Independent 3Qt” baskets. Decide which of those two numbers you need before you compare.</li>
<li><strong>Same unit?</strong> All three titles use quarts, written as Qt, QT or Quart. Compare the number, not the spelling.</li>
<li><strong>What food must fit?</strong> A capacity number does not show how much fits in one layer. Check the basket or interior size in the listing’s details before you rely on the number.</li>
<li><strong>Do not turn capacity into servings.</strong> None of the three titles gives a serving count, so this guide does not give one.</li>
<li><strong>Keep the record.</strong> Write the number you read, the page it came from and the date you read it.</li>
</ol>
<h2 class="z3-h2">What this guide does not say</h2>
<p>It gives no capacity ranking and no serving estimate. Basket dimensions, internal volume and cooking area were not verified for any of the three listings.</p>
<h2 class="z3-h2">Listings this guide is based on</h2>
{links}
""",
        "not_verified": [
            "Basket dimensions, internal volume, cooking area and serving counts for all three listings.",
        ],
        "related": ["basket-or-oven-style", "multi-function-questions"],
    },
    {
        "slug": "cleanup-and-counter-space",
        "title": "How to assess cleanup and counter-space trade-offs",
        "dek": "Dishwasher-safe wording is in two of the three titles. Counter space is in none of them. Here is how to check both.",
        "body": """
<h2 class="z3-h2">What the titles say about cleanup</h2>
{t3}
<h2 class="z3-h2">Counter space: what the titles leave out</h2>
<p>None of the three titles gives a width, depth or height. We did not verify any dimension for these listings on this pass. Read the product-details table on each listing, then measure your own counter.</p>
<ul class="z3-prose">
<li>Two compartments mean two baskets to clean. The 6QT title names two.</li>
<li>“French Door” in the 26QT title describes the door style. It does not give a depth. The depth you need has to come from the listing’s dimensions.</li>
<li>Check whether a basket or drawer has to be pulled out in front of the unit, and measure that space as well as the footprint.</li>
</ul>
<h2 class="z3-h2">A cleanup checklist</h2>
<ol class="z3-prose">
<li>Count the parts that touch food. The titles name baskets, and the 26QT title names six accessories.</li>
<li>Check the dishwasher wording for each part, not only for the title’s headline part.</li>
<li>Check where the nonstick coating is. The 6QT and 8QT titles say “Nonstick”, and name the basket. They do not say what else is coated.</li>
</ol>
<h2 class="z3-h2">Listings this guide is based on</h2>
{links}
""",
        "not_verified": [
            "Every dimension and weight for all three listings.",
            "Which parts other than the named baskets are dishwasher-safe.",
        ],
        "related": ["basket-or-oven-style", "capacity-checklist"],
    },
    {
        "slug": "multi-function-questions",
        "title": "Questions to ask before buying a multi-function kitchen appliance",
        "dek": "Multi-function claims are easy to count and hard to test. Ask what each number refers to and what is in the box.",
        "body": """
<h2 class="z3-h2">What the titles claim</h2>
{t4}
<h2 class="z3-h2">Questions to ask</h2>
<ol class="z3-prose">
<li><strong>What does each count mean?</strong> “4-in-1” and “24 One-Touch Preset Options” are counts. Find the list behind each one before you count it as a benefit.</li>
<li><strong>Which setting is the maximum?</strong> The 8QT title gives 450°F as a “Hi-Fry Option”. Check whether that is the top of the range, and what the other settings are.</li>
<li><strong>What is in the box?</strong> The 26QT title says six cooking accessories are included. Check the list of names.</li>
<li><strong>How do the parts clean?</strong> See the cleanup guide.</li>
<li><strong>What is the protection-plan offer?</strong> On the three air-fryer listings we opened on 2026-11-17, the page offers an optional 3-Year Kitchen Protection Plan from Asurion, LLC. It is not a manufacturer statement. We did not read the plan’s terms, so we do not describe them.</li>
<li><strong>Does it replace something you already own?</strong> Write the jobs you do each week and check each one against the function list.</li>
</ol>
<h2 class="z3-h2">What this guide does not say</h2>
<p>It does not say any appliance is good or bad. No appliance was tested for this guide.</p>
<h2 class="z3-h2">Listings this guide is based on</h2>
{links}
""",
        "not_verified": [
            "The preset lists, temperature ranges and accessory names for all three listings.",
            "The terms of the optional protection plan.",
        ],
        "related": ["basket-or-oven-style", "cleanup-and-counter-space"],
    },
]

AIR_ASINS = ["B0CDY277D3", "B09B7SB46R", "B08DKYBTPH"]


def _links_for(asins: list[str]) -> str:
    items = []
    for a in asins:
        r = row_by_asin(a)
        items.append(f'<li>{plink(a, r["short_name"])} — ASIN {a}, observed {OBSERVED_ON}. '
                     f'Submitted link: <a href="{r["submitted_link"]}">{esc(r["submitted_link"])}</a></li>')
    return '<ul class="z3-prose">' + "".join(items) + "</ul>"


def _guide_tables() -> dict:
    t1 = listing_table(
        "<tr><td>" + plink("B0CDY277D3", "CHEFMAN 6 Quart Dual Basket Air Fryer Oven") + "</td>"
        "<td><code>Dual Basket</code>, <code>Air Fryer Oven</code></td>"
        "<td><code>2 Independent 3Qt Nonstick Dishwasher Safe Frying Baskets</code></td></tr>"
        "<tr><td>" + plink("B09B7SB46R", "Emeril Lagasse 26QT French Door Multi-Function Air Fryer Toaster Oven") + "</td>"
        "<td><code>French Door</code>, <code>Multi-Function</code>, <code>Toaster Oven</code></td>"
        "<td><code>Extra Large Interior</code>, <code>Six Cooking Accessories Included</code></td></tr>"
        "<tr><td>" + plink("B08DKYBTPH", "Chefman Air Fryer 8 Qt | TurboFry® 4-in-1 with 450°F Hi-Fry Option for Crispier Results | Bake, Dehydrate, Frozen | XL Nonstick Dishwasher-Safe Basket | Stainless Steel") + "</td>"
        "<td><code>Air Fryer</code>, <code>4-in-1</code></td>"
        "<td><code>XL Nonstick Dishwasher-Safe Basket</code> (one basket named)</td></tr>",
        ["Listing (linked)", "Form words in the title", "Compartment or accessory words in the title"])
    t2 = listing_table(
        "<tr><td>" + plink("B0CDY277D3", "6 Quart / 2 Independent 3Qt") + "</td><td><code>6 Quart</code> and <code>2 Independent 3Qt</code></td><td>Whether 6 Quart is the total or the sum of the two baskets.</td></tr>"
        "<tr><td>" + plink("B09B7SB46R", "26QT") + "</td><td><code>26QT</code></td><td>What the number measures. The title says “Extra Large Interior” without a number.</td></tr>"
        "<tr><td>" + plink("B08DKYBTPH", "8 Qt") + "</td><td><code>8 Qt</code></td><td>Whether it is the basket or the whole appliance.</td></tr>",
        ["Listing (linked)", "Capacity wording in the title", "What the title does not say"])
    t3 = listing_table(
        "<tr><td>" + plink("B0CDY277D3", "CHEFMAN 6 Quart Dual Basket Air Fryer Oven") + "</td><td><code>Dishwasher Safe Frying Baskets</code></td><td>Any statement about parts other than the baskets.</td></tr>"
        "<tr><td>" + plink("B09B7SB46R", "Emeril Lagasse 26QT") + "</td><td>No dishwasher wording in the title</td><td>Whether any part is dishwasher-safe. Check the listing.</td></tr>"
        "<tr><td>" + plink("B08DKYBTPH", "Chefman Air Fryer 8 Qt") + "</td><td><code>XL Nonstick Dishwasher-Safe Basket</code></td><td>Whether the other parts are dishwasher-safe.</td></tr>",
        ["Listing (linked)", "Cleanup wording in the title", "What the title does not say"])
    t4 = listing_table(
        "<tr><td>" + plink("B09B7SB46R", "Emeril Lagasse 26QT") + "</td><td><code>Multi-Function</code>, <code>24 One-Touch Preset Options</code>, <code>Six Cooking Accessories Included</code></td><td>Which 24 presets, and whether each one sets both time and temperature.</td></tr>"
        "<tr><td>" + plink("B08DKYBTPH", "Chefman Air Fryer 8 Qt") + "</td><td><code>4-in-1</code>, <code>Bake, Dehydrate, Frozen</code>, <code>450°F Hi-Fry Option</code></td><td>Which four functions, and whether 450°F is the maximum setting.</td></tr>"
        "<tr><td>" + plink("B0CDY277D3", "CHEFMAN 6 Quart") + "</td><td><code>Hi-Fry</code>, <code>Auto Shutoff</code>, <code>Sync Finish</code></td><td>The title includes “Sync Finish”. We did not verify what it does; check the listing’s product details before you rely on it.</td></tr>",
        ["Listing (linked)", "Function claim in the title", "Question to ask"])
    return {"t1": t1, "t2": t2, "t3": t3, "t4": t4}


def guide_html(g: dict, tables: dict) -> str:
    links = _links_for(AIR_ASINS)
    body = g["body"].replace("{d}", OBSERVED_ON)
    for k, v in tables.items():
        body = body.replace("{" + k + "}", v)
    body = body.replace("{links}", links)
    nv = "".join(f"<li>{esc(x)}</li>" for x in g["not_verified"])
    rel = "".join(f'<li><a class="z3-link" href="{x}.html">{esc(next(y["title"] for y in GUIDES if y["slug"] == x))}</a></li>' for x in g["related"])
    return f"""
<p class="z3-crumbs"><a href="../index.html">Zone3</a> · <a href="index.html">Guides</a></p>
<p class="z3-eyebrow">Guide · working title</p>
<h1 class="z3-h1">{esc(g["title"])}</h1>
<p class="z3-lede">{esc(g["dek"])}</p>
<p class="z3-meta">Observed listings dated {OBSERVED_ON}. The title is a working title from the editorial hypotheses. It is not a claim that people search for it.</p>
<div class="z3-prose">{body}</div>
<h2 class="z3-h2">Not verified in this guide</h2>
<div class="z3-flag"><p>Left out on purpose, and listed on the flagged page:</p><ul class="z3-prose">{nv}</ul></div>
<h2 class="z3-h2">Related guides</h2>
<ul class="z3-prose">{rel}</ul>
<p class="z3-meta"><a class="z3-link" href="../intent-record/index.html">Product-intent record</a> · <a class="z3-link" href="../publication-pass.html#flagged">Flagged for review</a></p>
"""


def guides_pages() -> dict[str, str]:
    tables = _guide_tables()
    out = {}
    for g in GUIDES:
        out[f"guides/{g['slug']}.html"] = shell(
            f"guides/{g['slug']}.html",
            f"{g['title']} — Zone3",
            g["dek"] + " Titles and ASINs are quoted from the listing pages observed on " + OBSERVED_ON + ".",
            guide_html(g, tables),
        )
    cards = "".join(
        '<article class="z3-card">'
        '<span class="z3-tag">Working title</span>'
        f'<h3><a class="z3-link" href="{g["slug"]}.html" style="color:inherit;text-decoration:none">{esc(g["title"])}</a></h3>'
        f'<p>{esc(g["dek"])}</p>'
        f'<a class="z3-link" href="{g["slug"]}.html">Read →</a></article>'
        for g in GUIDES)
    body = f"""
<p class="z3-crumbs"><a href="../index.html">Zone3</a> · Guides</p>
<p class="z3-eyebrow">Guides</p>
<h1 class="z3-h1">Questions to answer before you pick an air fryer</h1>
<p class="z3-lede">Four guides, each built on quotations from the listing titles we opened on {OBSERVED_ON}. Each one says what it does not verify.</p>
<div class="z3-note"><p><strong>Publishing cadence (working setting):</strong> one new guide every 14 days. Each new guide is added to this page, to the sitemap and to the <a href="../feed.xml">RSS feed</a>. The owner can change the cadence. No traffic or search-volume claim is made.</p></div>
<div class="z3-grid">{cards}</div>
"""
    out["guides/index.html"] = shell(
        "guides/index.html", "Guides — Zone3",
        "Four buyer questions about air fryers, answered from the Amazon listing titles observed on " + OBSERVED_ON + ". Working titles; each guide states what it does not verify.",
        body)
    return out


# ---------------------------------------------------------------- intent record

def intent_page() -> str:
    trs = []
    for r in ROWS:
        trs.append(
            f'<tr id="row-{r["n"]}">'
            f'<td>{r["n"]}</td>'
            f'<td><a href="{r["submitted_link"]}">{esc(r["submitted_link"])}</a><br><small>code {esc(r["submitted_code"])} · {r["submitted_code_length"]} characters</small></td>'
            '<td class="z3-blank">not confirmed</td>'
            '<td class="z3-blank">blank</td>'
            '<td class="z3-blank">blank</td>'
            '<td class="z3-blank">blank</td>'
            f'<td><code>{esc(r["observed_redirect_asin"])}</code></td>'
            f'<td><a href="{r["observed_redirect_url"]}">{esc(r["observed_redirect_url"])}</a><br><small>{esc(r["observed_breadcrumb"])}</small></td>'
            f'<td>{esc(r["observed_title"])}</td>'
            f'<td>{r["observed_on"]}</td>'
            f'<td>{esc(r["guide_scope"])}</td>'
            "</tr>")
    body = f"""
<p class="z3-crumbs"><a href="../index.html">Zone3</a> · Product-intent record</p>
<p class="z3-eyebrow">Product-intent confirmation record</p>
<h1 class="z3-h1">What each short link was meant to open, and what it opened</h1>
<p class="z3-lede">Intent and observation are kept in separate columns. The intent columns stay blank until the owner supplies an intended product and an official page confirms it. No intent was confirmed on {OBSERVED_ON}.</p>
<div class="z3-note"><p><strong>Why the codes are not ASINs:</strong> Amazon's Creators API defines an ASIN as a 10-character identifier. Each supplied code is 9 characters. <a href="https://affiliate-program.amazon.com/creatorsapi/docs/en-us/api-reference/operations/get-items">Source: Creators API GetItems, ItemIdType</a>.</p></div>
<div class="z3-note"><p><strong>Selected tracking ID:</strong> <code>{esc(INTENT["selected_tracking_id"])}</code>. Not attached to any link on this site. Attribution on the supplied short links is unverified and needs an enrolled Associates Special Link test (<a href="https://affiliate-program.amazon.com/help/operating/agreement">Operating Agreement Section 1</a>). Flag AE-F-01.</p></div>
<h2 class="z3-h2">Record</h2>
<div class="z3-table-wrap"><table class="z3-table">
<thead><tr>
<th>#</th><th>Submitted link</th>
<th>Intended ASIN</th><th>Official listing URL (intended)</th><th>Confirmation date</th><th>Confirmation source</th>
<th>Observed redirect ASIN</th><th>Observed listing URL and breadcrumb</th><th>Observed page title (verbatim)</th><th>Observed on</th><th>Scope</th>
</tr></thead>
<tbody>{''.join(trs)}</tbody></table></div>
<h2 class="z3-h2">Field rules</h2>
<ul class="z3-prose">{''.join(f"<li>{esc(x)}</li>" for x in INTENT["field_rules"])}</ul>
<h2 class="z3-h2">Sources</h2>
<ul class="z3-prose">{''.join(f'<li><a href="{s["url"]}">{esc(s["label"])}</a> (read {s["read"]})</li>' for s in INTENT["official_sources"])}</ul>
<p class="z3-meta">Prices are not recorded here. Observed listing pages carry prices that this site does not publish.</p>
"""
    return shell("intent-record/index.html", "Product-intent confirmation record — Zone3",
                 "For each submitted short link: the intended ASIN (blank until confirmed), its confirmation fields, and the redirect target observed on " + OBSERVED_ON + " in a separate column.",
                 body)


# ---------------------------------------------------------------- this pass

FLAGS = [
    ("AE-F-01", "needs review · blocked (account)",
     "The selected tracking ID shopnow047c-20 is not on any link on this site, and attribution on the supplied short links has not been tested. The Special Link test needs an enrolled Associates account, which this session does not have. No link was changed.",
     "https://affiliate-program.amazon.com/help/operating/agreement"),
    ("AE-F-02", "needs decision",
     "Five links were supplied; the register held three. Two of the five (B0c8moW59 → B0DHZTCNR5, B0f3GKalj → B0DZFD6R9Z) open meat thermometers, which are outside the air-fryer register. No guide was written for them. Decide the category.",
     "https://www.amazon.com/dp/B0DHZTCNR5"),
    ("AE-F-03", "needs owner input",
     "No intended ASIN is confirmed for any of the five submitted links. Each code is 9 characters, not the 10-character ASIN. The observed redirect targets are recorded separately and are not treated as the intended products.",
     "https://affiliate-program.amazon.com/creatorsapi/docs/en-us/api-reference/operations/get-items"),
    ("AE-F-04", "blocked (decision)",
     "No outbound click counter, self-hosted analytics endpoint or conversion measurement is live. This site is a static GitHub Pages build with no server to receive events, and no endpoint or provider has been chosen. The brief refers to 'five defined events' without listing them, and the repository does not define them either. None were invented.",
     "https://api.github.com/repos/kanlerxz87-cyber/Zone3/pages"),
    ("AE-F-05", "blocked (owner account)",
     "Google Search Console is not set up. Verifying the property needs the owner's Google account, which this session cannot use.",
     "https://search.google.com/search-console"),
    ("AE-F-06", "needs decision",
     "Product photography (S-18) is not decided. The new pages use no images from Amazon and no generated images. Operating Agreement §1 defines “Program Content” as data, images, text and linking tools that Amazon may make available to Associates. Whether any listing image may be used is an owner decision.",
     "https://affiliate-program.amazon.com/help/operating/agreement"),
    ("AE-F-07", "not published",
     "Prices, star ratings, review counts, sales ranks and dimensions are not shown on the new pages. They were not verified in a form this site can publish, and the price-display position is an open repository item.",
     "https://www.amazon.com/dp/B0CDY277D3"),
    ("AE-F-08", "needs decision",
     "About 78 older pages keep their own top navigation. Only the front page, the guides and this pass use the single navigation group. Every page has the shared footer with all dashboard surfaces. Consolidating the older navigation is a decision.",
     "https://kanlerxz87-cyber.github.io/Zone3/publication-pass.html"),
    ("AE-F-09", "not changed",
     "Pages under archive/ are byte-for-byte snapshots of earlier sessions, kept by repository convention. The disclosure and sponsored-link rules were not applied to them.",
     "https://github.com/kanlerxz87-cyber/Zone3/tree/main/archive"),
    ("AE-F-10", "needs decision",
     "The front page is titled 'Zone3' because the catalogue now includes meat thermometers. Earlier pages use 'Air Fryer Field Notes' and 'The Crisp Report'. The brand choice is open. The previous root page is kept unchanged at dashboard-register.html.",
     "https://kanlerxz87-cyber.github.io/Zone3/dashboard-register.html"),
    ("AE-F-11", "working setting",
     "The publishing cadence (one guide every 14 days) is a working setting chosen in this session. It is not a traffic or revenue claim, and the owner can change it.",
     "https://kanlerxz87-cyber.github.io/Zone3/guides/index.html"),
    ("AE-F-12", "limitation",
     "The four guide titles are working titles from the editorial hypotheses. No search-volume, traffic or popularity data was used, because no analytics exist yet. Choosing the next topic from measured queries needs a measurement source (see AE-F-04 and AE-F-05).",
     "https://search.google.com/search-console"),
    ("AE-F-13", "limitation",
     "The guides quote the listing titles and the observed breadcrumb. The full bullet lists and product-details tables of the three air-fryer listings were not read line by line on this pass, so those details are left out.",
     "https://www.amazon.com/dp/B09B7SB46R"),
]

MEASURE = [
    ("Outbound click counter", "Not built", "A counter needs an endpoint that receives events. None exists or has been chosen (AE-F-04).", "https://api.github.com/repos/kanlerxz87-cyber/Zone3/pages"),
    ("Self-hosted analytics endpoint", "Not built", "No endpoint or provider has been chosen (AE-F-04).", "https://api.github.com/repos/kanlerxz87-cyber/Zone3/pages"),
    ("The 'five defined events'", "Not defined", "The brief does not list them and the repository does not define them. Nothing was invented (AE-F-04).", "none — no official source defines them"),
    ("Search Console", "Not set up", "Needs the owner's Google account (AE-F-05).", "https://search.google.com/search-console"),
    ("Special Link validation (one link per product)", "Not run", "Needs an enrolled Associates account. Operating Agreement Section 1 requires the tagged link formats Amazon provides (AE-F-01).", "https://affiliate-program.amazon.com/help/operating/agreement"),
    ("Campaign ledger (clicks, reported orders)", "Empty by design", "No first-party report has been supplied, so nothing is estimated.", "none — no first-party report supplied"),
]

VERIFICATION = [
    ("AE-V-01", "Operating Agreement Section 5 requires the sentence 'As an Amazon Associate I earn from qualifying purchases.', stated clearly and prominently.", "https://affiliate-program.amazon.com/help/operating/agreement", "Confirmed verbatim, read 2026-11-17. The sentence is used unchanged."),
    ("AE-V-02", "Creators API ItemIdType ASIN is a 10-character alphanumeric identifier.", "https://affiliate-program.amazon.com/creatorsapi/docs/en-us/api-reference/operations/get-items", "Confirmed. All five submitted codes are 9 characters (counted in this session)."),
    ("AE-V-03", "Operating Agreement Section 1: links must use the tagged 'Special Link' formats Amazon provides.", "https://affiliate-program.amazon.com/help/operating/agreement", "Confirmed. This is why the supplied short links are not rewritten: the test has not been run."),
    ("AE-V-04", "Google: rel=\"sponsored\" marks advertisements or paid placements (paid links).", "https://developers.google.com/search/docs/crawling-indexing/qualify-outbound-links", "Confirmed, last updated 2025-12-10. Applied to every Amazon product link."),
    ("AE-V-05", "FTC Disclosures 101: 'Place it so it's hard to miss'; disclosures 'are likely to be missed if they appear only on an ABOUT ME or profile page, at the end of posts or videos, or anywhere that requires a person to click MORE'.", "https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers", "Confirmed (November 2019). The disclosure sits under the masthead, and the footer repeats it."),
    ("AE-V-06", "Five submitted short links → five observed listings (ASIN, title, breadcrumb).", "https://www.amazon.com/dp/B0CDY277D3", "Observed 2026-11-17 for all five. Recorded per row in the intent record. An observed redirect is not treated as confirmed intent."),
    ("AE-V-07", "Air-fryer listings sit under 'Air Fryers' (node 17659096011); the two thermometer listings sit under 'Meat'.", "https://www.amazon.com/Air-Fryers/b/ref=dp_bc_5?ie=UTF8&node=17659096011", "Observed breadcrumbs on 2026-11-17; the category page itself was not opened."),
]


def _flags_html() -> str:
    cards = []
    for fid, status, text, src in FLAGS:
        cards.append(
            f'<div class="z3-flag" id="{fid.lower()}"><h3>{fid} · {esc(status)}</h3>'
            f"<p>{esc(text)}</p>"
            f'<p><small>Source: <a href="{src}">{esc(src)}</a></small></p></div>')
    return "".join(cards)


def _verif_rows() -> str:
    return "".join(
        f"<tr><td>{vid}</td><td>{esc(claim)}</td><td><a href=\"{src}\">{esc(src)}</a></td><td>{esc(res)}</td></tr>"
        for vid, claim, src, res in VERIFICATION)


def _measure_rows() -> str:
    return "".join(
        f"<tr><td>{esc(a)}</td><td>{esc(b)}</td><td>{esc(c)}</td>"
        + (f'<td><a href="{d}">{esc(d)}</a></td>' if d.startswith("http") else f'<td class="z3-blank">{esc(d)}</td>')
        + "</tr>"
        for a, b, c, d in MEASURE)


def audit_numbers() -> dict:
    before = json.loads((HERE / "audit-before.json").read_text(encoding="utf-8"))
    after = json.loads((HERE / "audit-after.json").read_text(encoding="utf-8"))
    return {"before": before, "after": after}


def summary_points(n: dict) -> list[str]:
    a = n["after"]
    b = n["before"]
    return [
        f"Disclosure sentence (Operating Agreement Section 5) under the masthead of the published HTML pages: {a['disclosure_above_fold']} of {a['pages']} (before this pass: {b['disclosure']} of {b['pages']}). Footer repeat: {a['footer_disclosure']} of {a['pages']}.",
        f"Amazon product links with rel=\"sponsored\": {a['amazon_links_sponsored']} of {a['amazon_links']} (before: {b['amazon_links_sponsored']} of {b['amazon_links']}). The links that still lack it are Associates policy pages, not product links.",
        "The front page leads with the five supplied products. The previous root page is kept unchanged at dashboard-register.html.",
        "Four question-shaped guides (working titles) quote listing titles only. They use no prices, ratings or popularity claims.",
        "The product-intent record keeps intended ASIN and confirmation fields separate from observed redirect targets. The intended fields are blank: no owner confirmation was supplied.",
        "Two of the five supplied links open meat thermometers, which are outside the air-fryer register. This needs a category decision (AE-F-02).",
        "Not built, and why: the click counter and analytics endpoint, the 'five defined events', Search Console and the Special Link test. Each needs an account, an endpoint or an owner decision (flags AE-F-01 and AE-F-04 to AE-F-05).",
    ]


def pass_page(n: dict) -> str:
    pts = "".join(f"<li>{esc(p)}</li>" for p in summary_points(n))
    a, b = n["after"], n["before"]
    audit_rows = "".join(
        f"<tr><td>{esc(k)}</td><td>{b.get(k, '')}</td><td>{a.get(k, '')}</td></tr>"
        for k in ["pages", "disclosure", "footer_disclosure", "amazon_links", "amazon_links_sponsored", "rss"]
    )
    body = f"""
<p class="z3-crumbs"><a href="index.html">Zone3</a> · This pass</p>
<p class="z3-eyebrow">This pass · {OBSERVED_ON} · session aebf0747</p>
<h1 class="z3-h1">What changed on this pass, and what still needs you</h1>
<p class="z3-lede">Executive summary, measurement status, the flagged-for-review list with sources, and the verification record for every claim this pass makes.</p>
<h2 class="z3-h2" id="summary">Executive summary</h2>
<ul class="z3-prose">{pts}</ul>
<h2 class="z3-h2" id="measurement">Measurement status</h2>
<p class="z3-meta">Nothing on this table is estimated. A blank or 'not built' status means the measurement does not exist yet.</p>
<div class="z3-table-wrap"><table class="z3-table"><thead><tr><th>Item</th><th>Status</th><th>Why</th><th>Source</th></tr></thead><tbody>{_measure_rows()}</tbody></table></div>
<h2 class="z3-h2" id="cadence">Publishing cadence</h2>
<p>Working setting: one new guide every 14 days. Each new guide is added to the guides page, the sitemap and the RSS feed (<a href="feed.xml">feed.xml</a>). This is an operating choice, not a traffic or revenue claim. The owner can change it (AE-F-11).</p>
<h2 class="z3-h2" id="audit">Before and after: site-wide markup</h2>
<p class="z3-meta">Counted by <code>sessions/aebf0747/audit.py</code> over every published HTML file. archive/ is excluded (AE-F-09).</p>
<div class="z3-table-wrap"><table class="z3-table"><thead><tr><th>Measure</th><th>Before</th><th>After</th></tr></thead><tbody>{audit_rows}</tbody></table></div>
<h2 class="z3-h2" id="disclosure">How the disclosure is placed</h2>
<p>The wording is the Operating Agreement Section 5 sentence, unchanged: <em>{esc(DISCLOSURE)}</em> The sentence sits directly under the masthead of each page, so a reader sees it before the first product. The footer repeats it. The footer is an addition, not a substitute, because the FTC says disclosures “are likely to be missed if they appear only on an ABOUT ME or profile page, at the end of posts or videos, or anywhere that requires a person to click MORE” (the page applies the same placement test) (<a href="https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers">FTC Disclosures 101</a>).</p>
<h2 class="z3-h2" id="flagged">Flagged for review</h2>
<p class="z3-meta">Non-blocking. Each flag names its source and what would close it. Nothing here stops the publication of the site.</p>
{_flags_html()}
<h2 class="z3-h2" id="verification">Verification record</h2>
<p class="z3-meta">Every row is checked against the page linked in it, on {OBSERVED_ON}. The same rows are in <code>sessions/aebf0747/verification.md</code>.</p>
<div class="z3-table-wrap"><table class="z3-table"><thead><tr><th>ID</th><th>Claim</th><th>Source</th><th>Result</th></tr></thead><tbody>{_verif_rows()}</tbody></table></div>
<h2 class="z3-h2">Decisions needed from the owner</h2>
<ul class="z3-prose">
<li>Confirm the intended ASIN for each of the five supplied links (AE-F-03), so the intent columns can be filled from an official page.</li>
<li>Run one Special Link test per product in an enrolled Associates account, and check the tracking report for shopnow047c-20 (AE-F-01).</li>
<li>Decide the category for the two thermometer links (AE-F-02).</li>
<li>Choose the measurement set-up: an analytics provider or an endpoint, and the five events (AE-F-04). Then set up Search Console (AE-F-05).</li>
<li>Decide on product photography (AE-F-06), the brand (AE-F-10), and the navigation for the older pages (AE-F-08).</li>
</ul>
<h2 class="z3-h2" id="paths">Suggestions for choosing a path before implementation</h2>
<p class="z3-prose">Each row lists the options and a suggested default. The suggestion is ours, not a fact from a source, and the owner decides.</p>
<div class="z3-tablewrap"><table class="z3-table"><caption>Options and suggested default for each open decision</caption>
<thead><tr><th>Decision (flag)</th><th>Option A</th><th>Option B</th><th>Suggested default</th></tr></thead>
<tbody>
<tr><td>Intended ASIN for each supplied link (AE-F-03)</td><td>Owner names the ASIN and the official listing URL; we record the date and source in the intent record.</td><td>Keep &ldquo;not confirmed&rdquo; and publish only the observed listing values.</td><td>B until the owner confirms an ASIN from a source.</td></tr>
<tr><td>Special Link test in an enrolled account (AE-F-01)</td><td>Owner generates one Special Link per product in Associates Central and checks the tracking report for the tracking ID.</td><td>Keep the supplied short links as they are and flag them (FLG-003).</td><td>A before any claim about attribution. Nothing here says the short links are invalid.</td></tr>
<tr><td>Meat-thermometer links in an air-fryer site (AE-F-02)</td><td>Keep them, labelled &ldquo;outside the air-fryer guides&rdquo; (current).</td><td>Remove them from this site and keep them in a separate list.</td><td>A if the owner wants one catalogue; B if the site must stay air-fryer only.</td></tr>
<tr><td>Measurement and the five events (AE-F-04, AE-F-05)</td><td>Choose an analytics provider or a self-hosted endpoint, then define the events.</td><td>Publish without measurement until the owner decides.</td><td>B. The repo defines no event list, so none is invented here.</td></tr>
<tr><td>Product photography (AE-F-06)</td><td>Use only images the owner has licensed for this use.</td><td>No product images (current).</td><td>B. The <a class=\"z3-link\" href=\"https://affiliate-program.amazon.com/help/operating/agreement\" target=\"_blank\" rel=\"noopener noreferrer\">Operating Agreement &sect;1</a> defines Program Content; no Amazon imagery is used.</td></tr>
<tr><td>Brand and navigation for older pages (AE-F-08, AE-F-10)</td><td>Adopt one brand and merge the older reader sets into one navigation.</td><td>Keep the existing sets and link to them from the footer (current).</td><td>B until the owner chooses a brand.</td></tr>
</tbody></table></div>
"""
    return shell("publication-pass.html", "This pass — executive summary, flags and verification — Zone3",
                 "Executive summary of the publication pass, measurement status, flagged-for-review items with sources, and the verification record for every claim.",
                 body)


# ---------------------------------------------------------------- feed + records

def feed_xml() -> str:
    items = []
    for g in GUIDES:
        link = f"{SITE_URL}guides/{g['slug']}.html"
        items.append(
            "<item>"
            f"<title>{esc(g['title'])}</title>"
            f"<link>{link}</link><guid isPermaLink=\"true\">{link}</guid>"
            f"<pubDate>{format_datetime(PUB_DATE)}</pubDate>"
            f"<description>{esc(g['dek'])}</description>"
            "</item>")
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<rss version="2.0"><channel>'
            "<title>Zone3 guides</title>"
            f"<link>{SITE_URL}guides/index.html</link>"
            "<description>Question-shaped buyer guides. Working titles; every quoted listing title is checked on the date shown.</description>"
            "<language>en</language>"
            f"<lastBuildDate>{format_datetime(PUB_DATE)}</lastBuildDate>"
            + "".join(items) +
            "</channel></rss>\n")


def verification_md() -> str:
    lines = ["# Verification record — session aebf0747", "",
             f"Observed and read on {OBSERVED_ON}. Every row links the page it was checked against.", "",
             "| ID | Claim | Source | Result |", "|---|---|---|---|"]
    for vid, claim, src, res in VERIFICATION:
        lines.append(f"| {vid} | {claim} | <{src}> | {res} |")
    lines += ["", "## Observed short-link redirects (not intent)", "",
              "| Submitted link | Observed ASIN | Observed URL | Observed title |", "|---|---|---|---|"]
    for r in ROWS:
        lines.append(f"| {r['submitted_link']} | {r['observed_redirect_asin']} | <{r['observed_redirect_url']}> | {r['observed_title']} |")
    lines += ["", "## Flags", ""]
    for fid, status, text, src in FLAGS:
        lines.append(f"- **{fid}** ({status}) {text} Source: <{src}>")
    return "\n".join(lines) + "\n"


def exec_summary_md(n: dict) -> str:
    lines = ["# Executive summary — publication pass (session aebf0747)", "",
             f"Date: {OBSERVED_ON}. Branch `arena/aebf0747-zone3`. Live page: {SITE_URL}publication-pass.html", ""]
    lines += [f"- {p}" for p in summary_points(n)]
    lines += ["", "Flags (non-blocking) are listed in `publication-pass.html#flagged` and in `verification.md`.", ""]
    return "\n".join(lines)


# ---------------------------------------------------------------- main

def main() -> int:
    root_index = ROOT / "index.html"
    current = root_index.read_text(encoding="utf-8") if root_index.exists() else ""
    if FRONT_MARK not in current and not (ROOT / "dashboard-register.html").exists():
        (ROOT / "dashboard-register.html").write_text(current, encoding="utf-8")

    pages: dict[str, str] = {"index.html": front_page()}
    pages.update(guides_pages())
    pages["intent-record/index.html"] = intent_page()
    pages["publication-pass.html"] = None  # filled after audit numbers exist
    for rel, text in pages.items():
        if text is None:
            continue
        p = ROOT / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")

    (ROOT / "feed.xml").write_text(feed_xml(), encoding="utf-8")
    (HERE / "verification.md").write_text(verification_md(), encoding="utf-8")

    # Session 1c072a7a (2026-11-19): one canonical owner for the reader front page,
    # guides and catalogue. Historical intent/pass records above remain intact.
    sys.path.insert(0, str(ROOT / "tools"))
    import build_publication
    build_publication.build(check=False)

    # 1. apply the mechanical pass so the audit measures the final markup
    publish_pass.run(ROOT, write=True)
    # 2. measure after
    import audit  # noqa: E402  (same definitions as publish_pass)
    after = audit.measure(ROOT)
    (HERE / "audit-after.json").write_text(json.dumps(after, indent=1) + "\n", encoding="utf-8")
    n = audit_numbers()
    # 3. write the pass page and the summary with those numbers, then apply the pass once more
    (ROOT / "publication-pass.html").write_text(pass_page(n), encoding="utf-8")
    (HERE / "EXECUTIVE-SUMMARY.md").write_text(exec_summary_md(n), encoding="utf-8")
    stats = publish_pass.run(ROOT, write=True)
    print({k: v for k, v in stats.items() if k != "missing_footer_targets"})
    if stats["missing_footer_targets"]:
        print("footer targets missing:", stats["missing_footer_targets"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
