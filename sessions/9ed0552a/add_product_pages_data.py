#!/usr/bin/env python3
"""9E-T2 data step (session 9ed0552a, 2026-11-20).

Adds, for each of the five registered listings, the fields the new reader-facing product
page needs, registers the five page URLs as indexable, and records the shipped decision
in the suggestions register.

Every value added here is either a URL slug, an editorial question, or a restatement of a
fact already held in this file or in data/shop/products.json with its own observation date.
No price, rating, review count, rank, commission or performance figure is introduced, and no
intended-ASIN field is filled: those stay blank and separate from the observed redirect.

Idempotent: running it twice leaves the file unchanged.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA_PATH = ROOT / "data" / "publication.json"

# slug, page title, meta description, standfirst/takeaway, questions, read-next guides.
# The title gains " | Zone3 Kitchen" in <title>, so each stays inside the 20-85 character
# gate; each description is unique and inside the 60-165 character gate.
PAGES = {
    "SHOP-01": {
        "slug": "chefman-6-quart-dual-basket-air-fryer",
        "title": "Chefman 6-quart dual-basket air fryer: a listing note",
        "description": "What the Chefman 6-quart dual-basket listing names, what it leaves open, and the questions to settle before two baskets earn counter space.",
        "takeaway": "The listing describes two independent 3-quart baskets that can be set to finish together. Whether that is the right shape for your dinners is the question this page helps you settle.",
        "questions": [
            "Do the meals you cook on repeat need two separate timings, or would one wider basket do the same job?",
            "Does the sync-finish wording cover the meals you actually cook, and does the manual say what happens when the two baskets hold different foods?",
            "Which parts does the listing call dishwasher safe, and does the care section of the manual agree?",
            "How much clearance does the manual ask for around the vents, and where would that leave you on your counter?",
        ],
        "related": ["basket-or-oven-style", "capacity-checklist", "cleanup-and-counter-space"],
    },
    "SHOP-02": {
        "slug": "emeril-lagasse-26qt-french-door-air-fryer-oven",
        "title": "Emeril Lagasse 26QT French-door air fryer oven: a listing note",
        "description": "What the Emeril Lagasse 26QT French-door listing names, what it leaves open, and how to check door swing and interior space before you buy.",
        "takeaway": "The listing describes a French-door oven with a 26QT label, a preset count and six included accessories. Door swing and usable interior are the two questions it cannot answer for you.",
        "questions": [
            "How far in front of the unit does the door travel when it opens, and is that floor space clear on your counter?",
            "What usable interior height and depth does the manual state, and would the roast you have in mind fit?",
            "Do the six included accessories cover the cooking you actually do, and where will they live when they are not in the oven?",
            "Would you rather reach into a door or pull out a basket on a normal weeknight?",
        ],
        "related": ["basket-or-oven-style", "cleanup-and-counter-space", "holiday-kitchen-checklist"],
    },
    "SHOP-03": {
        "slug": "chefman-turbofry-8-qt-air-fryer",
        "title": "Chefman TurboFry 8 Qt air fryer: a listing note",
        "description": "What the Chefman TurboFry 8 Qt listing names, what an 8-quart label does not settle, and how to test one basket against your usual dinner.",
        "takeaway": "The listing describes a single-basket air fryer with an 8-quart capacity. A capacity label describes a volume, not the size of one layer of food, so measure before you count servings.",
        "questions": [
            "Will the food you cook most often fit in a single layer, or will you be cooking in batches?",
            "What are the basket's internal dimensions, as opposed to the exterior size printed in the detail table?",
            "Do you routinely cook two different dishes that need separate timings?",
            "Which parts go in the dishwasher, per the care instructions?",
        ],
        "related": ["capacity-checklist", "how-do-you-know-its-done", "cleanup-and-counter-space"],
    },
    "SHOP-04": {
        "slug": "thermomaven-digital-meat-thermometer",
        "title": "ThermoMaven digital meat thermometer: a listing note",
        "description": "What the ThermoMaven digital thermometer listing names, what its title claims, and the manual questions to settle before you rely on a reading.",
        "takeaway": "The title makes speed, accuracy and certification claims. This page keeps them as the listing’s wording and points to the checks a reader can actually run.",
        "questions": [
            "Where does the manual say to place the probe in a whole chicken, and how deep does it need to go?",
            "Can the accuracy figure be checked at home, and what does an ice-water test show before you trust a reading?",
            "How long does a reading take in practice, and is the display readable in your kitchen light?",
            "What exactly does the certification wording on the title cover, and who issued it?",
        ],
        "related": ["thermometer-ice-water-check", "thermometer-numbers-on-the-label", "where-does-the-probe-go"],
    },
    "SHOP-05": {
        "slug": "chef-iq-sense-wireless-meat-thermometer",
        "title": "CHEF iQ Sense wireless meat thermometer: a listing note",
        "description": "What the CHEF iQ Sense listing names, what a wireless probe still leaves open, and the app, range and battery questions to settle first.",
        "takeaway": "The title names three probes, a WiFi range claim and five sensors. What it cannot tell you is what the app needs, how long a probe lasts and what a dropped connection does to a reading.",
        "questions": [
            "What does the app need before the first reading: an account, a phone version, a network?",
            "How long does a charged probe last, and how is it charged or replaced?",
            "What probe limits does the instruction sheet state for oven, grill and air-fryer use?",
            "What happens to a reading if the connection drops in the middle of a cook?",
        ],
        "related": ["instant-read-or-wireless-thermometer", "thermometer-numbers-on-the-label", "where-does-the-probe-go"],
    },
}

DECISION = {
    "id": "9E-P1",
    "priority": "Now",
    "area": "Shop structure",
    "title": "Give each registered listing its own reader-facing page, not just a card in a category.",
    "why": "Five products were reachable only as cards inside two category pages and one comparison table, so every product-intent search landed on a category page. A buyer comparing one model wants that model’s page, with its own source record.",
    "next": "Read the page for any listing, then check its official Amazon link against the register.",
    "evidence_needed": ["P26-Q1"],
    "source": "google-reviews",
    "status": "Adopted & shipped 2026-11-20",
    "next_action": "Shipped in this session: build_publication emits shop/<category>/<slug>.html per listing, links them from the front page, the category cards and the comparison table, and adds them to the sitemap, the search index and the indexing policy. The gate is sessions/9ed0552a/test_product_pages.py.",
    "discoveries": [
        "Whether a per-model page changes what search engines can tell apart, once real query data exists.",
        "Which listing the owner wants validated first, once account access exists.",
    ],
    "owner_input_needed": False,
    "reviewable_now": True,
    "outcome": "Adopted 2026-11-20 by session 9ed0552a; shipped in sessions/9ed0552a/review.md with the gate sessions/9ed0552a/test_product_pages.py.",
}


def main() -> int:
    data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    by_id = {p["id"]: p for p in data["products"]}
    changed = []

    for pid, page in PAGES.items():
        product = by_id[pid]
        if product.get("slug") != page["slug"]:
            product["slug"] = page["slug"]
            changed.append(f"{pid}.slug")
        if product.get("page") != page:
            product["page"] = page
            changed.append(f"{pid}.page")

    rels = [f'shop/{by_id[pid]["category"]}/{PAGES[pid]["slug"]}.html' for pid in PAGES]
    for rel in rels:
        if rel not in data["indexable_pages"]:
            data["indexable_pages"].append(rel)
            changed.append(f"indexable:{rel}")

    if not any(p.get("id") == DECISION["id"] for p in data["proposals"]):
        data["proposals"].append(DECISION)
        changed.append(DECISION["id"])

    if changed:
        DATA_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"{DATA_PATH.name}: {len(changed)} change(s) — {', '.join(changed) if changed else 'already current'}")
    print(f"products with page data: {sum(1 for p in data['products'] if p.get('page'))}; indexable: {len(data['indexable_pages'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
