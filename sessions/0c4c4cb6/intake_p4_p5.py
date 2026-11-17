#!/usr/bin/env python3
"""0C4-T2 — intake the two additional submitted links from the 2026-11-17 brief.

Adds to the canonical registers, additive only (no existing row, ID or value changed):

  data/sources.json   S70-S75  (six official-page captures, 2026-11-17)
  data/products.json  P4, P5   (same schema as P1-P3) + a product_intent block on
                      P1-P5 keeping the INTENDED identifier/URL separate from the
                      OBSERVED redirect target (brief: "Do not merge the two fields")
  data/flags.json     0C4-F-01..03

Observations recorded 2026-11-17 UTC by session 0c4c4cb6 (fetch tool):
  https://link.amazon/B0c8moW59 -> https://www.amazon.com/dp/B0DHZTCNR5 (ThermoMaven 1 s meat thermometer)
  https://link.amazon/B0f3GKalj -> https://www.amazon.com/dp/B0DZFD6R9Z (CHEF iQ Sense meat thermometer)
  https://www.amazon.com/dp/B0c8moW59 -> Amazon "Page Not Found"
  https://www.amazon.com/dp/B0f3GKalj -> Amazon "Page Not Found"
  https://www.amazon.com/dp/B0DHZTCNR5 -> live listing, title/breadcrumb as recorded
  https://www.amazon.com/dp/B0DZFD6R9Z -> live listing, title/breadcrumb as recorded

Price, rating and review-count values visible on those pages are deliberately NOT
recorded (Program Policies 2(b)/6(t); the refusal rule every prior session applied).
"""
from __future__ import annotations

import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
DATA = ROOT / "data"


def load(name: str):
    return json.loads((DATA / name).read_text(encoding="utf-8"))


def save(name: str, obj) -> None:
    # indent=2 + ensure_ascii=False matches the pre-existing formatting of data/*.json,
    # so an additive edit never rewrites untouched lines (checked against git diff).
    (DATA / name).write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


# ---------------------------------------------------------------- sources S70-S75
src = load("sources.json")
existing = {s["id"] for s in src["sources"]}
assert not (existing & {"S70", "S71", "S72", "S73", "S74", "S75"}), "S70-S75 already taken"

new_sources = [
    {
        "id": "S70",
        "title": "Intake 2026-11-17: link.amazon/B0c8moW59 resolves to amazon.com/dp/B0DHZTCNR5",
        "url": "https://link.amazon/B0c8moW59",
        "publisher": "Link as submitted by the owner (2026-11-17 brief)",
        "status": "observed",
        "status_note": (
            "Fetched 2026-11-17 by session 0c4c4cb6. Final URL "
            "https://www.amazon.com/dp/B0DHZTCNR5?lv=shuf&btn_type=ss&gaOptInStatus=true&_encoding=UTF8"
            "&sp_csd=d2lkZ2V0TmFtZT1zcF9waG9uZV9ob21lcGFnZV9ibGVuZGVk&language=en_US"
            "&content-id=amzn1.sym.4582c56b-139d-4168-9db2-822c68889360&ie=UTF8"
            "&btn_ref=srctok-633f9dc54185b50f&channelId=500&plpRedirect=mhFallback. "
            "The submitted code is 9 characters, so it is not an ASIN (S31, S45; class FLG-001/0C4-F-01). "
            "A link observation, not proof of owner intent (0C4-F-02)."
        ),
        "used_for": "Product 4 destination for the intake register and the product-intent record.",
    },
    {
        "id": "S71",
        "title": "Control check 2026-11-17: amazon.com/dp/B0c8moW59 returns Page Not Found",
        "url": "https://www.amazon.com/dp/B0c8moW59",
        "publisher": "Amazon.com (official)",
        "status": "observed",
        "status_note": (
            "Fetched 2026-11-17 by session 0c4c4cb6: Amazon served its 'Sorry! We couldn't find that page' "
            "error page (document title 'Page Not Found'). Same control result as S08-S10 for the first three "
            "submitted tokens. A 9-character code cannot be a 10-character ASIN (S31, S45)."
        ),
        "used_for": "P4 direct_check row on products.html.",
    },
    {
        "id": "S72",
        "title": "Direct listing check 2026-11-17: amazon.com/dp/B0DHZTCNR5 serves the ThermoMaven listing",
        "url": "https://www.amazon.com/dp/B0DHZTCNR5",
        "publisher": "Amazon.com (official)",
        "status": "observed",
        "status_note": (
            "Fetched 2026-11-17 by session 0c4c4cb6, independently of the short link. Page title served: "
            "'Amazon.com: ThermoMaven 1 Sec Professional Digital Meat Thermometer, \u00b10.5\u2109 Accuracy | "
            "NIST&NSF Certified Food Thermometer, Auto-Rotate Bright LED Screen, Highly Waterproof for Grill "
            "BBQ Camping, Black : Home & Kitchen'. Breadcrumb: Home & Kitchen > Kitchen & Dining > Kitchen "
            "Utensils & Gadgets > Thermometers & Timers > Meat. Price and rating were visible on the page and "
            "are deliberately NOT recorded (Program Policies 2(b)/6(t))."
        ),
        "used_for": "P4 redirect title_source and category_path; 0C4-F-03 category-scope flag.",
    },
    {
        "id": "S73",
        "title": "Intake 2026-11-17: link.amazon/B0f3GKalj resolves to amazon.com/dp/B0DZFD6R9Z",
        "url": "https://link.amazon/B0f3GKalj",
        "publisher": "Link as submitted by the owner (2026-11-17 brief)",
        "status": "observed",
        "status_note": (
            "Fetched 2026-11-17 by session 0c4c4cb6. Final URL "
            "https://www.amazon.com/dp/B0DZFD6R9Z?lv=shuf&sbo=RZvfv%2F%2FHxDF%2BO5021pAnSA%3D%3D"
            "&btn_type=ss&gaOptInStatus=true&language=en_US&btn_ref=srctok-101536bcd8e0be02"
            "&channelId=500&plpRedirect=mhFallback&th=1. The submitted code is 9 characters, so it is not "
            "an ASIN (S31, S45; class FLG-001/0C4-F-01). A link observation, not proof of owner intent "
            "(0C4-F-02)."
        ),
        "used_for": "Product 5 destination for the intake register and the product-intent record.",
    },
    {
        "id": "S74",
        "title": "Control check 2026-11-17: amazon.com/dp/B0f3GKalj returns Page Not Found",
        "url": "https://www.amazon.com/dp/B0f3GKalj",
        "publisher": "Amazon.com (official)",
        "status": "observed",
        "status_note": (
            "Fetched 2026-11-17 by session 0c4c4cb6: Amazon served its 'Sorry! We couldn't find that page' "
            "error page (document title 'Page Not Found'). Same control result as S08-S10 and S71."
        ),
        "used_for": "P5 direct_check row on products.html.",
    },
    {
        "id": "S75",
        "title": "Direct listing check 2026-11-17: amazon.com/dp/B0DZFD6R9Z serves the CHEF iQ listing",
        "url": "https://www.amazon.com/dp/B0DZFD6R9Z",
        "publisher": "Amazon.com (official)",
        "status": "observed",
        "status_note": (
            "Fetched 2026-11-17 by session 0c4c4cb6, independently of the short link. Page title served: "
            "'Amazon.com: CHEF iQ Sense | Smart Wireless Meat Thermometer | 3 Ultra-Thin Probes | WiFi "
            "Unlimited Range | 1000\u00b0F Heat Safe | 5 Sensors | BBQ, Grill, Oven, Smoker, Air Fryer | Gen3: "
            "Home & Kitchen'. Breadcrumb: Home & Kitchen > Kitchen & Dining > Kitchen Utensils & Gadgets > "
            "Thermometers & Timers > Meat. Price and rating were visible on the page and are deliberately NOT "
            "recorded (Program Policies 2(b)/6(t))."
        ),
        "used_for": "P5 redirect title_source and category_path; 0C4-F-03 category-scope flag.",
    },
]
src["sources"].extend(new_sources)
src["retrieved"] = (
    "2026-11-17 \u2014 union: earlier sessions' dated entries through S69 plus session 0c4c4cb6's "
    "S70-S75 intake captures of the two additional submitted links named in the 2026-11-17 brief"
)
src["id_reservation"] = (
    "S01-S59 are held by earlier sessions (main@110). S60-S69 are claimed by session 145b8df7. "
    "S70-S75 are claimed by session 0c4c4cb6 (2026-11-17 intake of link.amazon/B0c8moW59 and "
    "link.amazon/B0f3GKalj). A session appending later must start at S76, or renumber its own entries "
    "and then read back every reference target \u2014 an id-existence check will not catch a collision, "
    "because both ids exist and point at different documents."
)
save("sources.json", src)

# ---------------------------------------------------------------- flags 0C4-F-01..03
flags = load("flags.json")
existing_f = {f["id"] for f in flags["flags"]}
assert not any(i.startswith("0C4-F-") for i in existing_f), "0C4-F-* already present"

new_flags = [
    {
        "id": "0C4-F-01",
        "severity": "High",
        "category": "Product identifiers",
        "item": "The two additional submitted identifiers (B0c8moW59, B0f3GKalj) are 9 characters and are not ASINs",
        "detail": (
            "The 2026-11-17 brief added two more product links. Each carries a 9-character token. Amazon's "
            "Creators API documents the ASIN as a 10-character identifier (S31), corroborated by Amazon's own "
            "seller-education blog (S45), and amazon.com/dp/<token> returned Amazon's 'Page Not Found' page "
            "for both tokens on 2026-11-17 (S71, S74). This extends the class already recorded as FLG-001 "
            "for the first three submitted links; it is registered separately so the original flag's history "
            "is untouched."
        ),
        "action": (
            "Owner: provide the intended product page URL or 10-character ASIN for products 4 and 5. "
            "This session cannot infer it from the redirects."
        ),
        "sources": ["S31", "S45", "S71", "S74", "S70", "S73"],
        "date": "2026-11-17",
        "session": "0c4c4cb6",
        "status": "open",
    },
    {
        "id": "0C4-F-02",
        "severity": "High",
        "category": "Redirect behaviour",
        "item": "Products 4 and 5 open listings that are not confirmed as the intended products",
        "detail": (
            "link.amazon/B0c8moW59 opened amazon.com/dp/B0DHZTCNR5 (ThermoMaven 1 s meat thermometer) and "
            "link.amazon/B0f3GKalj opened amazon.com/dp/B0DZFD6R9Z (CHEF iQ Sense meat thermometer) on "
            "2026-11-17 (S70, S73); each destination page was then fetched directly and served the same "
            "title (S72, S75). Whether those listings are the products the owner meant is not documented "
            "by any source read \u2014 the same gap recorded for products 1-3 as FLG-002. The intended-ASIN "
            "and observed-redirect fields are kept separate in data/products.json (product_intent vs "
            "redirect_observed) and are not merged."
        ),
        "action": (
            "Owner: confirm in writing which listing each of the five submitted links is meant to promote; "
            "record the confirmation date in the product_intent block."
        ),
        "sources": ["S70", "S72", "S73", "S75"],
        "date": "2026-11-17",
        "session": "0c4c4cb6",
        "status": "open",
    },
    {
        "id": "0C4-F-03",
        "severity": "Medium",
        "category": "Category scope",
        "item": "Products 4 and 5 are meat thermometers, outside the air-fryer cluster the site's content targets",
        "detail": (
            "Both new destination pages serve the breadcrumb Home & Kitchen > Kitchen & Dining > Kitchen "
            "Utensils & Gadgets > Thermometers & Timers > Meat (S72, S75). Every published guide, comparison "
            "and article on this site is written about air fryers, whose breadcrumb is Small Appliances > "
            "Fryers > Air Fryers (S14-S16). The CHEF iQ listing title does mention 'Air Fryer' as one use "
            "scenario, but the listing category is Thermometers. This is a content-scope decision, not a "
            "data error: it answers open question 757-Q-13 (three products vs the air-fryer category) with a "
            "third option \u2014 a kitchen-gadgets scope \u2014 that the owner has not ruled on."
        ),
        "action": (
            "Owner decision needed before marketing copy for products 4-5 is written: keep the site "
            "air-fryer-only (then products 4-5 need their own surface or stay listed-but-unpromoted), or "
            "widen the editorial scope to kitchen gadgets. Do not silently fold meat thermometers into the "
            "air-fryer guides."
        ),
        "sources": ["S72", "S75", "S14", "S15", "S16"],
        "date": "2026-11-17",
        "session": "0c4c4cb6",
        "status": "open",
    },
]
flags["flags"].extend(new_flags)
flags["retrieved"] = (
    "2026-11-17 \u2014 union: earlier sessions' register through F65-F-06 plus session 0c4c4cb6's "
    "0C4-F-01..03 (P4/P5 intake)"
)
save("flags.json", flags)

# ---------------------------------------------------------------- products P4/P5 + intent
prod = load("products.json")
ids = {p["id"] for p in prod["products"]}
assert not (ids & {"P4", "P5"}), "P4/P5 already present"

P4_TITLE = (
    "Amazon.com: ThermoMaven 1 Sec Professional Digital Meat Thermometer, \u00b10.5\u2109 Accuracy | "
    "NIST&NSF Certified Food Thermometer, Auto-Rotate Bright LED Screen, Highly Waterproof for Grill BBQ "
    "Camping, Black : Home & Kitchen"
)
P5_TITLE = (
    "Amazon.com: CHEF iQ Sense | Smart Wireless Meat Thermometer | 3 Ultra-Thin Probes | WiFi Unlimited "
    "Range | 1000\u00b0F Heat Safe | 5 Sensors | BBQ, Grill, Oven, Smoker, Air Fryer | Gen3: Home & Kitchen"
)
CRUMB = (
    "Home & Kitchen > Kitchen & Dining > Kitchen Utensils & Gadgets > Thermometers & Timers > Meat "
    "(breadcrumb on the product page)"
)

new_products = [
    {
        "id": "P4",
        "label": "Product link 4",
        "submitted_url": "https://link.amazon/B0c8moW59",
        "link_id": "B0c8moW59",
        "link_id_length": 9,
        "asin": None,
        "direct_check": {
            "url": "https://www.amazon.com/dp/B0c8moW59",
            "result": "Page Not Found",
            "source": "S71",
        },
        "redirect_observed": {
            "final_url": (
                "https://www.amazon.com/dp/B0DHZTCNR5?lv=shuf&btn_type=ss&gaOptInStatus=true&_encoding=UTF8"
                "&sp_csd=d2lkZ2V0TmFtZT1zcF9waG9uZV9ob21lcGFnZV9ibGVuZGVk&language=en_US"
                "&content-id=amzn1.sym.4582c56b-139d-4168-9db2-822c68889360&ie=UTF8"
                "&btn_ref=srctok-633f9dc54185b50f&channelId=500&plpRedirect=mhFallback"
            ),
            "page_id": "B0DHZTCNR5",
            "page_title": P4_TITLE,
            "confirmed_as_submitted_product": False,
            "source": "S70",
            "title_source": "S72",
            "brand": "ThermoMaven",
            "capacity": None,
            "brand_capacity_note": (
                "Brand read from the destination page title (S70, S72). No capacity is stated in that title, "
                "so the capacity cell stays blank. Not confirmed as the submitted product (0C4-F-02)."
            ),
            "reverified": "2026-11-17: short link capture (S70) and independent direct fetch of the destination (S72), same title both times.",
            "note": (
                "Recorded only as the page the submitted link opens. Whether the owner intended that product "
                "is not documented by any source read (0C4-F-02, FLG-002 class)."
            ),
        },
        "product_intent": None,  # filled below for every product
        "product_name": None,
        "brand": None,
        "price": None,
        "rating": None,
        "review_count": None,
        "competitor_count": None,
        "best_seller_rank": None,
        "commission_rate": None,
        "availability": None,
        "clicks": None,
        "conversions": None,
        "associates_tag": None,
        "status": "Link does not resolve to a product page under its own identifier",
        "flags": ["0C4-F-01", "0C4-F-02", "0C4-F-03", "FLG-001", "FLG-002"],
        "sources": ["S02", "S31", "S45", "S70", "S71", "S72"],
        "observed_2026_11_17": {
            "date": "2026-11-17",
            "price": None,
            "other_offers": None,
            "rating": None,
            "review_count": None,
            "sales_note": None,
            "category_path": CRUMB,
            "sources": ["S70", "S72"],
            "note": (
                "Dated observation read from Amazon.com pages on 2026-11-17 by session 0c4c4cb6. Kept as "
                "research evidence only. NOT used as product identity and NOT displayed as price, rating or "
                "review facts on any page: Participation Requirements 2(b) and 6(t) bar that without an "
                "Amazon-served link or API data (PF-04, PF-05). Price and rating were visible on the fetched "
                "pages and were deliberately not copied into this file."
            ),
        },
        "value_sources_2026_11_17": {
            "product_name": ["S72"],
            "brand": ["S72"],
            "price": [],
            "rating": [],
            "review_count": [],
        },
    },
    {
        "id": "P5",
        "label": "Product link 5",
        "submitted_url": "https://link.amazon/B0f3GKalj",
        "link_id": "B0f3GKalj",
        "link_id_length": 9,
        "asin": None,
        "direct_check": {
            "url": "https://www.amazon.com/dp/B0f3GKalj",
            "result": "Page Not Found",
            "source": "S74",
        },
        "redirect_observed": {
            "final_url": (
                "https://www.amazon.com/dp/B0DZFD6R9Z?lv=shuf&sbo=RZvfv%2F%2FHxDF%2BO5021pAnSA%3D%3D"
                "&btn_type=ss&gaOptInStatus=true&language=en_US&btn_ref=srctok-101536bcd8e0be02"
                "&channelId=500&plpRedirect=mhFallback&th=1"
            ),
            "page_id": "B0DZFD6R9Z",
            "page_title": P5_TITLE,
            "confirmed_as_submitted_product": False,
            "source": "S73",
            "title_source": "S75",
            "brand": "CHEF iQ",
            "capacity": None,
            "brand_capacity_note": (
                "Brand read from the destination page title (S73, S75). No capacity is stated in that title, "
                "so the capacity cell stays blank. Not confirmed as the submitted product (0C4-F-02)."
            ),
            "reverified": "2026-11-17: short link capture (S73) and independent direct fetch of the destination (S75), same title both times.",
            "note": (
                "Recorded only as the page the submitted link opens. Whether the owner intended that product "
                "is not documented by any source read (0C4-F-02, FLG-002 class)."
            ),
        },
        "product_intent": None,
        "product_name": None,
        "brand": None,
        "price": None,
        "rating": None,
        "review_count": None,
        "competitor_count": None,
        "best_seller_rank": None,
        "commission_rate": None,
        "availability": None,
        "clicks": None,
        "conversions": None,
        "associates_tag": None,
        "status": "Link does not resolve to a product page under its own identifier",
        "flags": ["0C4-F-01", "0C4-F-02", "0C4-F-03", "FLG-001", "FLG-002"],
        "sources": ["S02", "S31", "S45", "S73", "S74", "S75"],
        "observed_2026_11_17": {
            "date": "2026-11-17",
            "price": None,
            "other_offers": None,
            "rating": None,
            "review_count": None,
            "sales_note": None,
            "category_path": CRUMB,
            "sources": ["S73", "S75"],
            "note": (
                "Dated observation read from Amazon.com pages on 2026-11-17 by session 0c4c4cb6. Kept as "
                "research evidence only. NOT used as product identity and NOT displayed as price, rating or "
                "review facts on any page: Participation Requirements 2(b) and 6(t) bar that without an "
                "Amazon-served link or API data (PF-04, PF-05). Price and rating were visible on the fetched "
                "pages and were deliberately not copied into this file."
            ),
        },
        "value_sources_2026_11_17": {
            "product_name": ["S75"],
            "brand": ["S75"],
            "price": [],
            "rating": [],
            "review_count": [],
        },
    },
]

# product-intent confirmation record for EVERY submitted link (brief: "For each submitted
# link..."). intended_* stays null until the owner confirms; the observed redirect target
# lives only in redirect_observed and is never copied here.
def intent_block() -> dict:
    return {
        "intended_asin": None,
        "intended_listing_url": None,
        "confirmation_date": None,
        "source": None,
        "confirmed_by": None,
        "status": "unconfirmed",
        "recorded": "2026-11-17",
        "recorded_by": "session 0c4c4cb6",
        "note": (
            "Product-intent confirmation record. These four fields (intended ASIN, official listing URL, "
            "confirmation date, source) are filled ONLY by an owner confirmation and stay blank until then. "
            "The page this link currently opens is recorded separately in redirect_observed and must never "
            "be merged into this block: an observed redirect is not evidence of intent (FLG-002, 0C4-F-02)."
        ),
    }


for p in prod["products"]:
    p["product_intent"] = intent_block()
for np in new_products:
    np["product_intent"] = intent_block()
    prod["products"].append(np)

prod["retrieved"] = (
    "2026-11-17 \u2014 five submitted links: P1-P3 from the original brief (re-verified through 2026-11-16) "
    "plus P4/P5 added by session 0c4c4cb6 from the 2026-11-17 brief (S70-S75). Every product now carries a "
    "product_intent block (owner-confirmation fields, all blank) separate from redirect_observed."
)
save("products.json", prod)

print("OK: S70-S75 added; P4/P5 added; product_intent added to P1-P5; 0C4-F-01..03 added.")
print("counts:", len(src["sources"]), "sources,", len(prod["products"]), "products,", len(flags["flags"]), "flags")
