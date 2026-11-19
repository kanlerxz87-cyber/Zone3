#!/usr/bin/env python3
"""Apply the C17 shop-first presentation after the C3 evidence/decision front-page pass.

The input remains the existing dated product-intent record and registered guide list.
This post-pass owns only the root <main>, title and description; it preserves the masthead,
above-the-fold disclosure, measurement markers, and the footer generated upstream.

Run after `sessions/c3be74f2/build_front_page.py`:
    python3 sessions/c17d25fd/build_shopfront.py [--check]
"""
from __future__ import annotations

import html
import json
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[1]
RECORD = ROOT / "sessions" / "aebf0747" / "intent-record.json"
PAGE = ROOT / "index.html"
MARKER = "<!-- c17d25fd:shopfront -->"

# Pull the existing guide register rather than creating a second topic list.
sys.path.insert(0, str(ROOT / "sessions" / "aebf0747"))
import build_pass as publication  # noqa: E402


def e(value: object) -> str:
    return html.escape("" if value is None else str(value), quote=True)


def product_card(row: dict, idx: int, total: int) -> str:
    name = row["short_name"]
    cat = row["category_group"]
    kind = {
        "B0CDY277D3": ("Dual-basket", "basket"),
        "B09B7SB46R": ("French-door oven", "oven"),
        "B08DKYBTPH": ("Basket air fryer", "basket"),
        "B0DHZTCNR5": ("Digital thermometer", "thermometer"),
        "B0DZFD6R9Z": ("Wireless thermometer", "thermometer"),
    }.get(row["observed_redirect_asin"], (cat, "basket"))
    href = e(row["submitted_link"])
    source = e(row["observed_redirect_url"])
    row_id = e(row["n"])
    return f'''<article class="z3-product-card">
  <div class="z3-product-card__top"><span class="z3-product-card__category">{e(kind[0])}</span><span class="z3-product-card__number">{idx:02d} <i>/ {total:02d}</i></span></div>
  <div class="z3-product-mark z3-product-mark--{e(kind[1])}" aria-hidden="true"><span>{idx:02d}</span></div>
  <h3>{e(name)}</h3>
  <p class="z3-product-card__meta">Observed destination · ASIN <code>{e(row['observed_redirect_asin'])}</code> · checked {e(row['observed_on'])}</p>
  <div class="z3-product-card__actions">
    <a class="z3-buy-link" href="{href}" rel="sponsored">Open supplied Amazon link <span aria-hidden="true">↗</span></a><span class="z3-sponsored-chip">Sponsored</span>
  </div>
  <div class="z3-product-card__source"><a href="{source}" rel="sponsored">Listing source · Sponsored <span aria-hidden="true">↗</span></a><a class="z3-record-link" href="intent-record/index.html#row-{row_id}">Product-intent record</a></div>
</article>'''


def decision_table() -> str:
    rows = [
        (
            "Which product was each link meant to promote?",
            "Observed destinations are recorded; intended-product fields remain unconfirmed.",
            '<a href="intent-record/index.html">Review the confirmation record</a>',
            '<a href="https://affiliate-program.amazon.com/creatorsapi/docs/en-us/api-reference/operations/get-items">Amazon Creators API identifier reference</a>',
        ),
        (
            "Which air-fryer layout suits my kitchen?",
            "The guide set compares listing language; it does not rank tested products.",
            '<a href="guides/index.html">Choose a buyer question</a>',
            '<a href="https://www.amazon.com/dp/B0CDY277D3" rel="sponsored">Listing 1</a> · <a href="https://www.amazon.com/dp/B09B7SB46R" rel="sponsored">Listing 2</a> · <a href="https://www.amazon.com/dp/B08DKYBTPH" rel="sponsored">Listing 3</a>',
        ),
        (
            "Are the submitted links confirmed Special Links?",
            "No enrolled-account destination and tracking-report test is recorded.",
            '<a href="flagged.html#FLG-003">See the unresolved link-status flag</a>',
            '<a href="https://affiliate-program.amazon.com/help/operating/agreement">Amazon Associates Operating Agreement</a>',
        ),
        (
            "Should thermometers become their own editorial category?",
            "Two observed listings sit outside the present air-fryer guide shelf.",
            '<a href="decision-queue.html">Review the category decision</a>',
            '<a href="https://www.amazon.com/dp/B0DHZTCNR5" rel="sponsored">Listing 1</a> · <a href="https://www.amazon.com/dp/B0DZFD6R9Z" rel="sponsored">Listing 2</a>',
        ),
        (
            "Which site change should happen next?",
            "Suggestions, missing information, and implementation decisions are kept separate.",
            '<a href="suggestions.html">Review proposals and discovery actions</a>',
            '<a href="https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers">FTC disclosure guidance</a>',
        ),
    ]
    body = "".join(
        f"<tr><td>{q}</td><td>{state}</td><td>{next_step}</td><td>{source}</td></tr>"
        for q, state, next_step, source in rows
    )
    return (
        '<div class="z3-table-wrap"><table class="z3-table z3-decision-table">'
        '<thead><tr><th>Question</th><th>What the record says</th><th>Next step</th><th>Official context</th></tr></thead>'
        f"<tbody>{body}</tbody></table></div>"
    )


def front_main(record: dict) -> str:
    rows = record["rows"]
    air = [r for r in rows if r["category_group"] == "Air fryers"]
    thermometers = [r for r in rows if r["category_group"] == "Meat thermometers"]
    air_cards = "".join(product_card(row, i, len(air)) for i, row in enumerate(air, 1))
    thermometer_cards = "".join(product_card(row, i, len(thermometers)) for i, row in enumerate(thermometers, 1))
    guide_cards = "".join(
        '<article class="z3-guide-card">'
        f'<span class="z3-guide-card__number">Guide {i:02d}</span>'
        f'<h3>{e(g["title"])}</h3><p>{e(g["dek"])}</p>'
        f'<a href="guides/{e(g["slug"])}.html">Read the guide <span aria-hidden="true">→</span></a>'
        '</article>'
        for i, g in enumerate(publication.GUIDES, 1)
    )
    return f'''{MARKER}
<main id="main" class="z3-main c3-front c17-front"><div class="z3-wrap">
  <section class="c3-hero z3-home-hero" aria-labelledby="home-title">
    <div class="c3-hero-copy">
      <p class="z3-eyebrow">Zone3 · The kitchen buying desk</p>
      <h1 class="z3-home-title" id="home-title">Find your next kitchen buy in the details.</h1>
      <p class="z3-home-lede">Browse the listings, compare the details that matter to you, and follow a short buyer guide before you choose. No made-up rankings. No pretend hands-on reviews.</p>
      <div class="z3-home-actions">
        <a class="z3-home-button" href="#air-fryers">Browse air fryers <span aria-hidden="true">↓</span></a>
        <a class="z3-home-text-link" href="#buyer-guides">Read the buyer’s guides <span aria-hidden="true">→</span></a>
      </div>
      <p class="z3-home-byline">Three air-fryer listings and two kitchen-tool listings, kept in separate shelves.</p>
    </div>
    <figure class="c3-hero-art z3-home-hero__image">
      <img src="assets/zone3-kitchen-notes-hero.png" alt="Abstract editorial illustration of a kitchen worktop and a small checklist card.">
      <figcaption>Kitchen Notes · questions to take into the listing</figcaption>
    </figure>
  </section>

  <span id="products" class="z3-anchor-alias"></span><span id="listing-desk" class="z3-anchor-alias"></span>
  <section class="z3-home-section" id="air-fryers" aria-labelledby="air-fryer-heading">
    <div class="z3-section-heading"><div><p class="z3-eyebrow">The starting shelf</p><h2 id="air-fryer-heading">Three air-fryer listings to compare</h2></div><a class="z3-section-link" href="marketing/comparison.html">Compare the details <span aria-hidden="true">→</span></a></div>
    <p class="z3-section-intro">Listing snapshots, not product verdicts. Read what each destination page says, then decide which details matter in your kitchen.</p>
    <div class="z3-product-grid">{air_cards}</div>
    <p class="z3-home-caveat">Product names and observed ASINs describe the pages opened by the supplied links on {e(record['observed_on'])}; they are not confirmation of owner intent. The supplied-link Special Link test is still open. <a href="intent-record/index.html">See the separate product-intent record</a>.</p>
  </section>

  <section class="z3-home-section z3-home-section--soft" id="buyer-guides" aria-labelledby="guides-heading">
    <span id="questions" class="z3-anchor-alias"></span>
    <div class="z3-section-heading"><div><p class="z3-eyebrow">Read before you decide</p><h2 id="guides-heading">Questions worth asking</h2></div><a class="z3-section-link" href="guides/index.html">All buyer’s guides <span aria-hidden="true">→</span></a></div>
    <p class="z3-section-intro">These are editorial hypotheses, not claims about trending searches or product superiority.</p>
    <div class="z3-guide-grid">{guide_cards}</div>
  </section>

  <section class="z3-home-section" aria-labelledby="thermometer-heading">
    <div class="z3-section-heading"><div><p class="z3-eyebrow">A separate category</p><h2 id="thermometer-heading">Meat thermometers</h2></div><a class="z3-section-link" href="shop/meat-thermometers/index.html">Browse this category <span aria-hidden="true">→</span></a></div>
    <p class="z3-section-intro">Two observed listings sit outside the air-fryer guide collection and remain separate until the editorial scope is chosen.</p>
    <div class="z3-product-grid z3-product-grid--compact">{thermometer_cards}</div>
  </section>

  <section class="z3-home-section z3-home-decision" aria-labelledby="decision-heading">
    <div class="z3-section-heading"><div><p class="z3-eyebrow">Known facts · open questions · next steps</p><h2 id="decision-heading">What can we answer before recommending?</h2></div></div>
    {decision_table()}
  </section>

  <section class="z3-home-review" aria-labelledby="review-heading">
    <div><p class="z3-eyebrow">Help choose what comes next</p><h2 id="review-heading">Good publishing starts with good questions.</h2>
    <p>Review the ideas, missing information, and discovery actions before any proposal is implemented. Suggestions are not approvals.</p></div>
    <div class="z3-review-actions"><a href="suggestions.html">Review suggestions <span aria-hidden="true">→</span></a><a href="decision-queue.html">Open decision queue <span aria-hidden="true">→</span></a><a href="site/answers.html">Known facts &amp; open questions <span aria-hidden="true">→</span></a><a href="flagged.html">See flagged items <span aria-hidden="true">→</span></a></div>
  </section>

  <section class="z3-home-note" aria-label="Editorial and affiliate note"><span class="z3-home-note__label">How we work</span>
    <p>We don’t publish a price, rating, review count, or first-hand verdict unless the permitted source and experience are actually available. The Amazon Associate disclosure remains visible above and below the page.</p>
    <a href="executive-summary/index.html">Read the executive summary <span aria-hidden="true">→</span></a>
  </section>
</div></main>
<!-- /c17d25fd:shopfront -->'''


def render() -> str:
    raw = PAGE.read_text(encoding="utf-8")
    record = json.loads(RECORD.read_text(encoding="utf-8"))
    new_main = front_main(record)
    if "<!-- aebf0747-front -->" not in raw:
        raise RuntimeError("expected the aebf0747 root publication marker; refusing to patch another page")
    main_pattern = (
        r'(?:<!-- (?:c3be74f2:front|c17d25fd:shopfront) -->\s*)?'
        r'<main\b[^>]*class="[^"]*z3-main[^"]*"[^>]*>.*?</main>'
        r'(?:\s*<!-- /(?:c3be74f2:front|c17d25fd:shopfront) -->)?'
    )
    updated, count = re.subn(main_pattern, new_main, raw, count=1, flags=re.S | re.I)
    if count != 1:
        raise RuntimeError(f"expected one publication <main> region; found {count}")
    updated = re.sub(
        r"<title>.*?</title>",
        "<title>Zone3 | Kitchen buying guides, air fryers &amp; kitchen tools</title>",
        updated,
        count=1,
        flags=re.S | re.I,
    )
    updated = re.sub(
        r'<meta\s+name="description"\s+content="[^"]*">',
        '<meta name="description" content="Question-led kitchen buying guides and source-linked comparisons for air fryers and kitchen tools. See what is observed and what still needs confirmation.">',
        updated,
        count=1,
        flags=re.I,
    )
    return updated


def main() -> int:
    check = "--check" in sys.argv
    current = PAGE.read_text(encoding="utf-8")
    updated = render()
    if check:
        if current != updated:
            print("C17 shopfront is stale; rerun sessions/c17d25fd/build_shopfront.py")
            return 1
        print("C17 shopfront is current")
        return 0
    if updated != current:
        PAGE.write_text(updated, encoding="utf-8")
        print("C17 shopfront updated")
    else:
        print("C17 shopfront already current")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
