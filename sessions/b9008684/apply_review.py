#!/usr/bin/env python3
"""One-time additive edit (session b9008684, task B9-T3).

Adds to data/publication.json, without touching any existing key:
  * two new official sources fetched live on 2026-11-19 (google-structured-data,
    google-page-experience) — recorded in sessions/b9008684/verification-2026-11-19.md;
  * the `review_b9008684` review round: design-prompt feed suggestions, the article
    slate (working titles), organic-traffic actions and the decision-support register.

Idempotent: re-running on an already-updated file changes nothing. The six P26
proposals, nine P26 questions and every product/guide row are left untouched.
Review-only: nothing in this block is implemented by publishing it.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PATH = ROOT / 'data' / 'publication.json'

NEW_SOURCES = [
    {
        'id': 'google-structured-data',
        'title': 'Google Search Central: introduction to structured data',
        'url': 'https://developers.google.com/search/docs/appearance/structured-data/intro-structured-data',
        'checked_on': '2026-11-19',
        'scope': 'Intro read: rich results; do not mark up content that is not visible to the user; no empty pages held only for structured data.',
    },
    {
        'id': 'google-page-experience',
        'title': 'Google Search Central: understanding page experience',
        'url': 'https://developers.google.com/search/docs/appearance/page-experience',
        'checked_on': '2026-11-19',
        'scope': 'Self-assessment list read: Core Web Vitals, secure serving, mobile display, no excessive ads, no intrusive interstitials, distinguishable main content.',
    },
]

REVIEW = {
    'round_id': 'B9-ROUND-2026-11-19',
    'session': 'b9008684',
    'date': '2026-11-19',
    'intro': 'A dated review round, kept separate from the six standing proposals above. Every card is review-only: choosing an option saves a note in this browser and implements nothing. Each suggestion carries the sentence it would add to the design prompt and what evidence would change the decision.',
    'design_feed': [
        {
            'id': 'D9-01',
            'status': 'Ready — needs approval only',
            'area': 'Editorial design',
            'title': 'Ship a dated seasonal strip, not a hype banner',
            'why': 'Late November through December is when the thermometer guides and the hosting checklist are naturally useful, and a calendar fact needs no demand claim. A restrained strip that says what today is and links the three guides that answer it makes the site feel tended rather than generated.',
            'feeds_prompt': 'Carry one restrained, dated seasonal strip that connects existing guides to the current cooking season; it states calendar facts only, never demand, popularity or trend claims.',
            'falsifier': 'If the strip dates badly or its guides draw no measurable engagement after the season, retire it — a stale strip is worse than none.',
            'basis': 'food-safety',
        },
        {
            'id': 'D9-02',
            'status': 'Ready — needs approval only',
            'area': 'Editorial',
            'title': 'Approve the article slate below, one guide at a time',
            'why': 'The reading room grows credibility by rhythm, not volume: one new question-shaped guide at a time, each through the same publishing gate, each linked from two existing guides so the cluster stays one hop wide.',
            'feeds_prompt': 'Grow the reading room one question-shaped guide at a time; every new guide keeps the same evidence limits, related-links mesh, schema, canonical URL, sitemap and RSS entry as the current six.',
            'falsifier': 'A drafted guide that cannot cite its sources, or that repeats a question the room already answers, does not ship.',
            'basis': 'google-reviews',
        },
        {
            'id': 'D9-03',
            'status': 'Proposed — needs sourced Q&A pairs first',
            'area': 'Findability',
            'title': 'Add FAQPage structured data only where every answer is already sourced and visible',
            'why': 'Article schema ships today. An FAQ block earns rich results only when the answers are actually on the page, and Google is explicit that invisible or empty-page markup is out of bounds — so the constraint is the editor, not the schema.',
            'feeds_prompt': 'Add a short FAQ block to a guide only when every answer is already stated and sourced in that guide, and mark it up with FAQPage structured data; never mark up content the page does not show.',
            'falsifier': 'If an answer needs a fact the register cannot source, the question is dropped, not inferred.',
            'basis': 'google-structured-data',
        },
        {
            'id': 'D9-04',
            'status': 'Proposed — needs a layout audit first',
            'area': 'Mobile and page experience',
            'title': 'Port the mobile pass into the reader template: type scale, tap targets, a sticky way to reach the comparison',
            'why': 'The research layer already ships a clamped type scale, 44-pixel tap targets and a sticky quick-compare bar; the reader template should carry the same discipline so long guides keep the comparison one thumb-reach away.',
            'feeds_prompt': 'Keep a mobile-first type scale, 44-pixel minimum tap targets, and a sticky way to reach the format comparison from long guides.',
            'falsifier': 'If the sticky bar overlaps content or traps scrolling on any viewport, simplify it rather than patch it.',
            'basis': 'google-page-experience',
        },
        {
            'id': 'D9-05',
            'status': 'Blocked — needs the owner’s imagery decision (S-18)',
            'area': 'Visual',
            'title': 'Decide the product-imagery route before any photography ships',
            'why': 'Three routes exist and they need different permissions: keep labelled generic art (no new permissions), authorized Amazon-served or API imagery if API access is ever established, or original photography of owned units provided by the owner. The default stands until someone chooses.',
            'feeds_prompt': 'Use labelled generic art until authorized exact-product assets exist; when real imagery arrives, label its source and date next to the listing facts it illustrates.',
            'falsifier': 'Unpublished while blocked; the decision record names the route before any image changes.',
            'basis': 'amazon-policies',
        },
        {
            'id': 'D9-06',
            'status': 'Proposed — needs an internal-linking look first',
            'area': 'Information architecture',
            'title': 'Group the reading room by the decision a reader is facing',
            'why': 'The six guides already answer a sequence — format, capacity, cleanup, functions, thermometer, hosting — but the index presents them as one flat grid. A visible grouping makes the hub structure the buyer can feel, not just the links the crawler sees.',
            'feeds_prompt': 'Group the reading room by the decision a reader is facing, not by product type alone, so every guide is one visible hop from its two neighbours.',
            'falsifier': 'If readers still arrive on cards without context after grouping, revisit the grouping rather than adding navigation.',
            'basis': None,
        },
        {
            'id': 'D9-07',
            'status': 'Ready — process rule',
            'area': 'Process',
            'title': 'Keep review mode review-only, and give every suggestion a falsifier',
            'why': 'This round’s cards each carry a “what would change our mind” line; future decision surfaces should keep the same select/save/export pattern with no implementation path, so a review can never quietly become a change.',
            'feeds_prompt': 'Every suggestion shows what evidence would change the decision; a review choice never implements itself.',
            'falsifier': 'If any future page lets a review action publish, spend or reconfigure, that page fails review.',
            'basis': 'ftc',
        },
    ],
    'article_slate': [
        {
            'id': 'AS-01',
            'category': 'Meat thermometers',
            'title': 'Where does the probe go? Turkey, ham and roasts, checked the boring way.',
            'angle': 'Probe placement, rest times and the safe minimum temperatures as the factual spine; the thermometer listings appear as tools, not verdicts.',
            'pairs': [['instant-read-or-wireless-thermometer', 'Instant-read or wireless'], ['holiday-kitchen-checklist', 'The hosting checklist']],
            'provenance': 'The safe-temperature chart on FoodSafety.gov (poultry 165°F; 145°F plus a 3-minute rest for whole cuts), read 2026-11-19.',
            'seasonal': 'Timed to late-November through December cooking; stated as a calendar fact, never as a demand claim.',
        },
        {
            'id': 'AS-02',
            'category': 'Air fryers',
            'title': 'Can one air fryer cover a holiday table — or do you need two drawers?',
            'angle': 'Capacity and format questions under one roof: what a quart number can and cannot tell you about fitting a real meal, and when two independent baskets change the plan.',
            'pairs': [['basket-or-oven-style', 'Basket or oven-style'], ['capacity-checklist', 'The capacity checklist']],
            'provenance': 'Listing format wording for the three air-fryer destinations, observed 2026-11-19; no performance claim.',
            'seasonal': 'Same calendar window as AS-01; demand wording stays out.',
        },
        {
            'id': 'AS-03',
            'category': 'Air fryers',
            'title': 'Sync Finish, two baskets, one dinner: what the setting promises and what to check.',
            'angle': 'Reads a named listing feature as a listing claim: what “Sync Finish” says it does, what the manual defines, and the three checks before relying on it for one shared dinner.',
            'pairs': [['basket-or-oven-style', 'Basket or oven-style'], ['multi-function-questions', 'Multi-function questions']],
            'provenance': 'SHOP-01’s listing title names Sync Finish; the feature description stays a listing claim, not a test result.',
        },
        {
            'id': 'AS-04',
            'category': 'Air fryers',
            'title': 'What actually fits on the counter? Measure before you believe the quart number.',
            'angle': 'A measuring checklist: depth, width, ventilation clearance and door swing, with prompts to check the exact model’s manual — the numbers that matter are in the reader’s kitchen, not the listing.',
            'pairs': [['cleanup-and-counter-space', 'Cleanup and counter space'], ['capacity-checklist', 'The capacity checklist']],
            'provenance': 'Extends the shipped cleanup-and-counter-space guide; dimensions stay unverified and the guide says so.',
        },
        {
            'id': 'AS-05',
            'category': 'Air fryers',
            'title': 'Do presets change dinner, or just the label?',
            'angle': 'Follow-up to the multi-function guide: what a preset count claims, what a preset usually is, and why the manual matters more than the number on the box.',
            'pairs': [['multi-function-questions', 'Multi-function questions'], ['basket-or-oven-style', 'Basket or oven-style']],
            'provenance': 'SHOP-02’s listing title names 24 one-touch presets; the count is listing wording, not an endorsement.',
        },
        {
            'id': 'AS-06',
            'category': 'Meat thermometers',
            'title': 'Wireless range claims: what “unlimited range” can and cannot promise.',
            'angle': 'Connectivity claims read carefully: what WiFi range wording describes, what the app requirements add, and the checks to run before hosting day.',
            'pairs': [['instant-read-or-wireless-thermometer', 'Instant-read or wireless'], ['holiday-kitchen-checklist', 'The hosting checklist']],
            'provenance': 'SHOP-05’s listing title names WiFi unlimited range; the claim stays a listing claim.',
        },
        {
            'id': 'AS-07',
            'category': 'Air fryers',
            'title': 'Reading an air-fryer listing: five claims to separate from evidence.',
            'angle': 'The anti-slop flagship: teach the reader the method this site uses — listing claim, manual, independent evidence — so any shop page can be read with the same five questions.',
            'pairs': [['basket-or-oven-style', 'Basket or oven-style'], ['capacity-checklist', 'The capacity checklist'], ['multi-function-questions', 'Multi-function questions']],
            'provenance': 'Google’s review-quality guidance (expertise, evidence, pros and cons from original research) and the FTC’s rule against talking about experience you do not have.',
            'basis': 'google-reviews',
        },
    ],
    'traffic_intro': 'Organic traffic is earned, not claimed. What the site can automate now, what is blocked on an account or a host, and the standing rules that keep promotion compliant.',
    'traffic_actions': [
        {
            'action': 'Ship every new guide through the findability checklist: unique title and meta description, canonical URL, sitemap entry, RSS entry, and links from at least two existing guides.',
            'status': 'Automated for current templates; carries over to approved new guides.',
            'needs': 'Nothing — the renderer already emits all of it.',
            'basis': 'google-canonical',
        },
        {
            'action': 'Verify Search Console, submit the sitemap, and collect the first query report.',
            'status': 'Blocked — needs the owner’s Search Console account.',
            'needs': 'Owner verification; the query report then becomes the topic-selection input.',
            'basis': 'search-console',
        },
        {
            'action': 'Enable production measurement on a durable host and count guide arrivals and outbound clicks per page.',
            'status': 'Blocked — needs a durable, commercially suitable host (GitHub Pages’ limits put business use out of bounds).',
            'needs': 'Host decision, deployment, and a privacy review of that host’s logging.',
            'basis': 'github-limits',
        },
        {
            'action': 'If paid search is ever used: ads must land on this site — never directly or indirectly on an Amazon Site — and must avoid prohibited placements. The project currently runs none.',
            'status': 'Standing rule, restated for the traffic plan.',
            'needs': 'Nothing while no ads run.',
            'basis': 'amazon-policies',
        },
        {
            'action': 'Keep the one-guide-review-every-14-days cadence, and move topic choice to measured queries once a query report exists.',
            'status': 'Operating plan, not a forecast.',
            'needs': 'The Search Console report above; until then topics stay labelled editorial hypotheses.',
            'basis': 'google-reviews',
        },
    ],
    'decision_intro': 'The decision-support register: for each pending decision, what is already in hand, what is missing, how to discover it, and the safe default if it never arrives. Companion to the nine standing evidence questions above.',
    'decision_rows': [
        {
            'id': 'DS-01',
            'decision': 'Approve the next guide from the slate.',
            'have': 'Six shipped guides; the seven-title slate below, each with provenance.',
            'missing': 'Editorial approval and, later, measured query evidence.',
            'discovery': 'Search Console query report once verified; meanwhile, review the slate on this page.',
            'default': 'Publish one slate guide at a time through the publishing gate, starting with the thermometer temperature guide — its factual spine is already sourced.',
            'basis': 'search-console',
        },
        {
            'id': 'DS-02',
            'decision': 'Choose the product-imagery route (S-18).',
            'have': 'Labelled generated context art and original generic diagrams; a written no-scraping rule.',
            'missing': 'The owner’s route decision; authorized exact-product assets on any other route.',
            'discovery': 'Owner decision; the API route applies only if authorized API access is established.',
            'default': 'Keep labelled generic art.',
            'basis': 'amazon-policies',
        },
        {
            'id': 'DS-03',
            'decision': 'Add FAQPage structured data to a guide.',
            'have': 'Article schema with an Organization author, shipped and gated.',
            'missing': 'Sourced, visible Q&A pairs per guide.',
            'discovery': 'Draft pairs from existing guide sections; validate markup before shipping.',
            'default': 'No FAQ schema until every answer is sourced and visible on the page.',
            'basis': 'google-structured-data',
        },
        {
            'id': 'DS-04',
            'decision': 'Port the mobile pass into the reader template.',
            'have': 'The pattern already shipped in the research layer (clamped type, 44px targets, sticky bar).',
            'missing': 'An audit of the reader template at narrow widths.',
            'discovery': 'Layout audit at 320/390/768 px plus a tap-target check.',
            'default': 'Port the pattern during the next template change rather than as a standalone release.',
            'basis': 'google-page-experience',
        },
        {
            'id': 'DS-05',
            'decision': 'Publish the seasonal strip (D9-01).',
            'have': 'The calendar fact; three relevant guides; copy drafted into the design-prompt feed.',
            'missing': 'Approval of the strip copy.',
            'discovery': 'Review the proposed prompt sentence and the three linked guides.',
            'default': 'Publish only after review; the strip stays undated and unshipped otherwise.',
            'basis': 'food-safety',
        },
        {
            'id': 'DS-06',
            'decision': 'Turn production measurement on.',
            'have': 'One five-event runtime and a hardened self-hosted collector; production off, ledger empty.',
            'missing': 'A durable host, its privacy review, and deployment verification.',
            'discovery': 'Host decision, deploy, run the delivery tests; then enable with an evidence-backed release.',
            'default': 'Stays off; no arrival counts are claimed until then.',
            'basis': 'github-pages',
        },
        {
            'id': 'DS-07',
            'decision': 'Validate attribution before scaling links.',
            'have': 'The supplied tracking ID recorded, unvalidated; five observed destinations; intended ASINs still blank.',
            'missing': 'One enrolled-workflow test per product: destination and tracking report.',
            'discovery': 'Owner logs into Associates and validates one Special Link per product.',
            'default': 'No scaled link changes; the short links keep their unresolved review status.',
            'basis': 'amazon-policies',
        },
        {
            'id': 'DS-08',
            'decision': 'Choose the next topic from evidence instead of instinct.',
            'have': 'No Search Console property, no query report, an empty campaign ledger — honestly stated.',
            'missing': 'A verified property, a first query report, and an authorized Associates report.',
            'discovery': 'Owner verification and report authorization; the decision-support register updates once they arrive.',
            'default': 'Topics stay labelled editorial hypotheses; nothing claims popularity or search volume.',
            'basis': 'search-console',
        },
    ],
    'prompt_intro': 'Lines this round would append to the design prompt if approved. Copying or appending them is an approval step for the reviewer; nothing is applied by reading this page.',
    'prompt_lines': 'Publish on a dated seasonal rhythm without ever claiming demand: a restrained seasonal strip names the calendar fact and links the guides that answer it. Grow the reading room one question-shaped guide at a time; each new guide keeps the same evidence limits, related-links mesh, Article schema, canonical URL, sitemap and RSS entry as the current six. Add FAQPage structured data only when every answer is already visible and sourced on the page. Keep the mobile-first type scale and 44-pixel tap targets, and make the format comparison reachable from long guides. Use labelled generic art until authorized exact-product assets exist, and label real imagery with its source and date when it arrives. Group the reading room by the decision a reader is facing. Every suggestion shows what evidence would change the decision; a review choice never implements itself. If paid search is ever used it lands on this site — never directly or indirectly on an Amazon Site — and organic findability starts with Search Console verification and a first-party query report.',
}


def main() -> int:
    data = json.loads(PATH.read_text(encoding='utf-8'))
    changed = False
    existing = {s['id'] for s in data['sources']}
    for source in NEW_SOURCES:
        if source['id'] not in existing:
            data['sources'].append(source)
            changed = True
    if 'review_b9008684' not in data:
        data['review_b9008684'] = REVIEW
        changed = True
    if changed:
        PATH.write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
        print('publication.json updated: +2 sources, +review_b9008684')
    else:
        print('publication.json already carries the review round; nothing changed')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
