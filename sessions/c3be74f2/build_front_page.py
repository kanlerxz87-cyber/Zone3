#!/usr/bin/env python3
"""Build the marker-bounded C3 publication front page.

This pass intentionally owns only the inner <main> of the root page plus the matching
CSS classes. It reads the dated product-intent record, preserves the site-wide masthead,
disclosure strip, measurement markers and footer, and can be rerun after the older
front-page generator.

Usage:
    python3 sessions/c3be74f2/build_front_page.py
    python3 sessions/c3be74f2/build_front_page.py --check
"""
from __future__ import annotations

import html
import json
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PAGE = ROOT / "index.html"
RECORD = ROOT / "sessions" / "aebf0747" / "intent-record.json"
MARKER = "<!-- c3be74f2:front -->"


def esc(value: str) -> str:
    return html.escape(value, quote=True)


def product_card(row: dict, group: str) -> str:
    scope = "Air-fryer guide shelf" if group == "Air fryers" else "Separate category decision"
    return f'''<article class="c3-product-card">
  <p class="c3-card-kicker">{esc(scope)}</p>
  <h3>{esc(row["short_name"])}</h3>
  <p class="c3-asin"><span>Observed listing ASIN</span> <code>{esc(row["observed_redirect_asin"])}</code></p>
  <p class="c3-card-note">Intent is not confirmed. The observation and the intended-product fields stay separate.</p>
  <div class="c3-card-actions">
    <a class="c3-button c3-button-dark" href="{esc(row["submitted_link"])}" rel="sponsored">Open submitted Amazon link <span aria-hidden="true">↗</span></a>
    <a class="c3-text-link" href="{esc(row["observed_redirect_url"])}" rel="sponsored">Listing source <span aria-hidden="true">↗</span></a>
  </div>
  <a class="c3-record-link" href="intent-record/index.html#row-{esc(str(row["n"]))}">Read the confirmation record</a>
</article>'''


def front_main(record: dict) -> str:
    rows = record["rows"]
    observed_on = record["observed_on"]
    air = [r for r in rows if r["category_group"] == "Air fryers"]
    thermometers = [r for r in rows if r["category_group"] != "Air fryers"]
    air_cards = "".join(product_card(row, "Air fryers") for row in air)
    thermometer_cards = "".join(product_card(row, "Meat thermometers") for row in thermometers)

    return f'''<!-- c3be74f2:front -->
<main class="z3-main c3-front"><div class="z3-wrap">
  <section class="c3-hero" aria-labelledby="c3-front-title">
    <div class="c3-hero-copy">
      <p class="z3-eyebrow">Zone3 / kitchen decision notes</p>
      <h1 class="z3-h1" id="c3-front-title">A clearer brief for your next kitchen-tool decision.</h1>
      <p class="c3-dek">Start with the question you are trying to answer — capacity, layout, cleanup or functions — then read the listing with a record of what is known and what still needs confirmation.</p>
      <div class="c3-hero-actions">
        <a class="c3-button c3-button-accent" href="#questions">Start with a buyer question <span aria-hidden="true">↓</span></a>
        <a class="c3-button c3-button-line" href="#listing-desk">Browse the listing desk</a>
      </div>
      <p class="c3-fineprint">We have not tested these products. No price, rating, review count, performance forecast or product ranking is published here.</p>
    </div>
    <figure class="c3-hero-art">
      <img src="assets/zone3-kitchen-notes-hero.png" alt="Abstract editorial illustration of a kitchen worktop and a small checklist card.">
      <figcaption>Kitchen Notes · a reader-first guide collection</figcaption>
    </figure>
  </section>

  <section class="c3-status-strip" aria-label="Current record status">
    <div><strong>5</strong><span>submitted Amazon links</span></div>
    <div><strong>3</strong><span>observed air-fryer listings</span></div>
    <div><strong>2</strong><span>observed thermometer listings, held apart from the guide cluster</span></div>
    <div><strong>{esc(observed_on)}</strong><span>date of the recorded observations</span></div>
  </section>

  <section class="c3-section" id="questions" aria-labelledby="questions-title">
    <div class="c3-section-heading">
      <p class="z3-eyebrow">Start with the job, not the product grid</p>
      <h2 class="z3-h2" id="questions-title">Four buyer questions to take into the listing</h2>
      <p>These are working editorial questions, not claims about search demand or product superiority.</p>
    </div>
    <div class="c3-question-grid">
      <a class="c3-question" href="guides/basket-or-oven-style.html"><span>01</span><h3>Basket or oven-style?</h3><p>Separate form words from the compartments and accessories the title actually names.</p><b>Read the comparison questions <i aria-hidden="true">→</i></b></a>
      <a class="c3-question" href="guides/capacity-checklist.html"><span>02</span><h3>What does capacity mean here?</h3><p>Check whether a number is total capacity, per compartment, or an unanswered detail.</p><b>Use the capacity checklist <i aria-hidden="true">→</i></b></a>
      <a class="c3-question" href="guides/cleanup-and-counter-space.html"><span>03</span><h3>What has to fit and clean up?</h3><p>Use listing wording for care claims; measure your own countertop before deciding.</p><b>Check fit and cleanup <i aria-hidden="true">→</i></b></a>
      <a class="c3-question" href="guides/multi-function-questions.html"><span>04</span><h3>What do the function counts mean?</h3><p>Look behind a preset or function number before treating it as a benefit.</p><b>Ask the function questions <i aria-hidden="true">→</i></b></a>
    </div>
    <p class="c3-underlink"><a href="guides/index.html">See all four guides and the working publishing cadence <span aria-hidden="true">→</span></a></p>
  </section>

  <section class="c3-section c3-listing-desk" id="listing-desk" aria-labelledby="listing-desk-title">
    <div class="c3-section-heading c3-heading-row">
      <div><p class="z3-eyebrow">The listing desk</p><h2 class="z3-h2" id="listing-desk-title">Listings observed from the submitted links</h2></div>
      <p>Each card names an observed listing, not an owner-confirmed intended product. The direct listing link is the source; the submitted Amazon link is kept separately.</p>
    </div>
    <div class="c3-group-label"><span>Air-fryer guide shelf</span><p>Three observed listings currently support the air-fryer question set.</p></div>
    <div class="c3-products">{air_cards}</div>
    <div class="c3-group-label c3-group-label-warn"><span>Separate category decision</span><p>Two observed thermometer listings are not folded into the air-fryer guide cluster.</p></div>
    <div class="c3-products c3-products-thermo">{thermometer_cards}</div>
  </section>

  <section class="c3-section c3-decision-section" aria-labelledby="c3-decision-title">
    <div class="c3-section-heading">
      <p class="z3-eyebrow">A decision before a recommendation</p>
      <h2 class="z3-h2" id="c3-decision-title">What this record can answer — and what it cannot</h2>
    </div>
    <div class="c3-table-wrap"><table class="c3-decision-table">
      <thead><tr><th>Decision question</th><th>Current record</th><th>Best next move</th><th>Official context</th></tr></thead>
      <tbody>
        <tr><td>What was each submitted link meant to promote?</td><td>Observed destinations are recorded; the intended ASIN fields remain unconfirmed.</td><td><a href="intent-record/index.html">Review the confirmation record</a></td><td><a href="https://affiliate-program.amazon.com/creatorsapi/docs/en-us/api-reference/operations/get-items">Amazon Creators API: ASIN identifier</a></td></tr>
        <tr><td>Which air-fryer layout fits my kitchen?</td><td>Listing-title language is organized into four buyer-question guides. No product has been tested or ranked.</td><td><a href="guides/index.html">Choose a guide question</a></td><td><a href="https://www.ftc.gov/business-guidance/resources/advertising-marketing/endorsements-influencers-reviews">FTC endorsement guidance</a></td></tr>
        <tr><td>Should thermometers become their own editorial category?</td><td>Two observed listings sit outside the present air-fryer guide shelf.</td><td><a href="decision-queue.html">Review the category decision</a></td><td><a href="https://www.amazon.com/dp/B0DHZTCNR5" rel="sponsored">Observed thermometer listing</a></td></tr>
        <tr><td>Which site improvement should be implemented next?</td><td>Ideas, blockers and discovery steps are deliberately separated from verified findings.</td><td><a href="suggestions.html">Open suggestions for review</a></td><td><a href="https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers">FTC disclosure guidance</a></td></tr>
      </tbody>
    </table></div>
  </section>

  <section class="c3-trust-panel" aria-labelledby="c3-trust-title">
    <div><p class="z3-eyebrow">The publishing boundary</p><h2 class="z3-h2" id="c3-trust-title">Useful first. Careful with the rest.</h2></div>
    <div class="c3-trust-points"><p><b>Source-linked:</b> listing observations and policy references point back to their official pages.</p><p><b>Blank by design:</b> intent, price, ratings, reviews, traffic, sales and conversion values are not filled in from inference.</p><p><b>Disclosure in view:</b> the Amazon Associate statement appears under the masthead and again in the footer.</p></div>
    <div class="c3-trust-actions"><a class="c3-button c3-button-dark" href="sources/index.html">Browse sources</a><a class="c3-button c3-button-line" href="flagged.html">See flagged items</a></div>
  </section>
</div></main>
<!-- /c3be74f2:front -->'''


def render() -> str:
    raw = PAGE.read_text(encoding="utf-8")
    record = json.loads(RECORD.read_text(encoding="utf-8"))
    new_main = front_main(record)
    if not re.search(r'<main\b[^>]*class="[^"]*z3-main', raw, re.I):
        raise RuntimeError("index.html no longer has the expected z3-main root; refusing to overwrite")
    # On a repeat run consume the C3 markers as well as the main. That keeps this pass
    # idempotent while still accepting a root page freshly regenerated by aebf0747.
    main_pattern = (r'(?:<!-- c3be74f2:front -->\s*)?'
                    r'<main\b[^>]*class="[^"]*z3-main[^"]*"[^>]*>.*?</main>'
                    r'(?:\s*<!-- /c3be74f2:front -->)?')
    replaced, count = re.subn(main_pattern, new_main, raw, count=1, flags=re.S | re.I)
    if count != 1:
        raise RuntimeError(f"expected one root main replacement; got {count}")
    replaced = re.sub(r'<title>.*?</title>', '<title>Zone3 — Kitchen decision notes and source-linked buyer guides</title>', replaced, count=1, flags=re.S | re.I)
    replaced = re.sub(
        r'<meta\s+name="description"\s+content="[^"]*">',
        '<meta name="description" content="Source-linked kitchen buyer questions, five observed Amazon listing destinations, and a clear record of what remains unconfirmed.">',
        replaced,
        count=1,
        flags=re.I,
    )
    return replaced


def main() -> None:
    check = "--check" in sys.argv
    updated = render()
    current = PAGE.read_text(encoding="utf-8")
    if check:
        if updated != current:
            print("C3 front page is stale; rerun sessions/c3be74f2/build_front_page.py")
            raise SystemExit(1)
        print("C3 front page is current")
        return
    if updated != current:
        PAGE.write_text(updated, encoding="utf-8")
        print("C3 front page updated")
    else:
        print("C3 front page already current")


if __name__ == "__main__":
    main()
