#!/usr/bin/env python3
"""Apply session 9fef7647's 2026-11-14 live re-verification to data/*.json.

Run from the repository root: python3 scripts/update_data_2026_11_14.py

Every value written here was read from an official page fetched live on
2026-11-14 (amazon.com short-link resolutions and search result pages,
affiliate-program.amazon.com Operating Agreement and Program Policies,
ftc.gov Disclosures 101). Nothing is inferred.
"""
from __future__ import annotations

import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "data"


def load(name):
    return json.loads((DATA / name).read_text(encoding="utf-8"))


def save(name, obj):
    (DATA / name).write_text(json.dumps(obj, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")


# ---------------------------------------------------------------- sources
src = load("sources.json")
src["retrieved"] = "2026-11-13; re-verified 2026-11-14"
src["retrieved_by"] = (
    "Session 7f84fea4 (branch arena/7f84fea4-zone3), merged with session 26634cd5; "
    "S30-S38 added by session 9fef7647 (branch arena/9fef7647-zone3) on 2026-11-14."
)
new_sources = [
    {
        "id": "S30",
        "title": "Re-check 2026-11-14: link.amazon/B04G1MEwY resolves to amazon.com/dp/B0CDY277D3",
        "url": "https://link.amazon/B04G1MEwY",
        "publisher": "Link as submitted by the owner",
        "status": "observed",
        "status_note": "Fetched 2026-11-14 with a fresh redirect token (srctok-1e229870efde5acf). Final URL: https://www.amazon.com/dp/B0CDY277D3?lv=shuf&btn_type=ss&gaOptInStatus=true&btn_ref=srctok-1e229870efde5acf&channelId=704&plpRedirect=mhFallback . Title of the destination page as served: \"Amazon.com: CHEFMAN 6 Quart Dual Basket Air Fryer Oven with Easy View Windows, Sync Finish, Hi-Fry, Auto Shutoff, 2 Independent 3Qt Nonstick Dishwasher Safe Frying Baskets, Digital Double Air Fryer - Black : Home & Kitchen\". Same destination as S11 (2026-11-13).",
        "used_for": "Product 1 identity: the listing this submitted link opens (FLG-022).",
    },
    {
        "id": "S31",
        "title": "Re-check 2026-11-14: link.amazon/B02NbDxp3 resolves to amazon.com/dp/B09B7SB46R",
        "url": "https://link.amazon/B02NbDxp3",
        "publisher": "Link as submitted by the owner",
        "status": "observed",
        "status_note": "Fetched 2026-11-14 with a fresh redirect token (srctok-534f5e7952f396b2). Final URL: https://www.amazon.com/dp/B09B7SB46R?lv=shuf&btn_type=ss&gaOptInStatus=true&btn_ref=srctok-534f5e7952f396b2&channelId=704&plpRedirect=mhFallback . Title of the destination page as served: \"Amazon.com: Emeril Lagasse 26QT French Door Multi-Function Air Fryer Toaster Oven | 26QT air fryer oven with French doors, 24 cooking functions, dual-speed fan and rotisserie for easy family meals. : Home & Kitchen\". Same destination as S12 (2026-11-13).",
        "used_for": "Product 2 identity: the listing this submitted link opens (FLG-022).",
    },
    {
        "id": "S32",
        "title": "Re-check 2026-11-14: link.amazon/B00hJ57DV resolves to amazon.com/dp/B08DKYBTPH",
        "url": "https://link.amazon/B00hJ57DV",
        "publisher": "Link as submitted by the owner",
        "status": "observed",
        "status_note": "Fetched 2026-11-14 with a fresh redirect token (srctok-76c3adaeb8708b44). Final URL: https://www.amazon.com/dp/B08DKYBTPH?lv=shuf&btn_type=ss&gaOptInStatus=true&btn_ref=srctok-76c3adaeb8708b44&channelId=704&plpRedirect=mhFallback&th=1 . Title of the destination page as served: \"Amazon.com: Chefman Air Fryer 8 Qt | TurboFry\u00ae 4-in-1 with 450\u00b0F Hi-Fry Option for Crispier Results | Bake, Dehydrate, Frozen | XL Nonstick Dishwasher-Safe Basket | Stainless Steel : Home & Kitchen\". Same destination as S13/S23 (2026-11-13).",
        "used_for": "Product 3 identity: the listing this submitted link opens (FLG-022).",
    },
    {
        "id": "S33",
        "title": "Amazon.com search results for B0CDY277D3 (price, rating, review count observed 2026-11-14)",
        "url": "https://www.amazon.com/s?k=B0CDY277D3",
        "publisher": "Amazon.com",
        "status": "observed",
        "status_note": "Fetched 2026-11-14. Result 1 for B0CDY277D3 as displayed: 4.2 out of 5 stars, (4.8K) reviews, 1K+ bought in past month, price USD 79.93 (deal; List: USD 99.99), More Buying Choices from USD 57.45. Values are a volatile snapshot (FLG-023).",
        "used_for": "Product 1 observed price, rating, review count, sales note.",
    },
    {
        "id": "S34",
        "title": "Amazon.com search results for B09B7SB46R (price, rating, review count observed 2026-11-14)",
        "url": "https://www.amazon.com/s?k=B09B7SB46R",
        "publisher": "Amazon.com",
        "status": "observed",
        "status_note": "Fetched 2026-11-14. Result 1 for B09B7SB46R as displayed: 4.3 out of 5 stars, (18.3K) reviews, 4K+ bought in past month, price USD 149.99 (deal labelled Early Black Friday Deal; List: USD 209.99), More Buying Choices from USD 92.99. Values are a volatile snapshot (FLG-023).",
        "used_for": "Product 2 observed price, rating, review count, sales note.",
    },
    {
        "id": "S35",
        "title": "Amazon.com search results for B08DKYBTPH (price, rating, review count observed 2026-11-14)",
        "url": "https://www.amazon.com/s?k=B08DKYBTPH",
        "publisher": "Amazon.com",
        "status": "observed",
        "status_note": "Fetched 2026-11-14. Result 1 for B08DKYBTPH as displayed: 4.4 out of 5 stars, (16.8K) reviews, 3K+ bought in past month, price USD 79.91 (deal; List: USD 119.99), More Buying Choices from USD 49.54, +1 other color/pattern. Values are a volatile snapshot (FLG-023).",
        "used_for": "Product 3 observed price, rating, review count, sales note.",
    },
    {
        "id": "S36",
        "title": "Re-check 2026-11-14: Associates Program Operating Agreement (Section 5 disclosure wording)",
        "url": "https://affiliate-program.amazon.com/help/operating/agreement",
        "publisher": "Amazon Associates",
        "status": "verified",
        "status_note": "Fetched 2026-11-14. Page states: Updated October 15, 2025. Section 5 read in full and compared to the PF-01 quote in data/policy_facts.json: identical wording (\"As an Amazon Associate I earn from qualifying purchases.\").",
        "used_for": "Re-verification of PF-01, PF-02, PF-35 wording.",
    },
    {
        "id": "S37",
        "title": "Re-check 2026-11-14: Associates Program Policies",
        "url": "https://affiliate-program.amazon.com/help/operating/policies",
        "publisher": "Amazon Associates",
        "status": "verified",
        "status_note": "Fetched 2026-11-14. Page states: Updated April 14, 2026. Commission Income Statement Section 1 read and compared to PF-12/PF-13: identical (24-hour session; 89-day cart completion; 180-day ship/pay).",
        "used_for": "Re-verification of PF-03 to PF-15 session and price/rating display rules.",
    },
    {
        "id": "S38",
        "title": "Re-check 2026-11-14: FTC Disclosures 101 for Social Media Influencers",
        "url": "https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers",
        "publisher": "U.S. Federal Trade Commission",
        "status": "verified",
        "status_note": "Fetched 2026-11-14. Page dated November 2019. \"When to Disclose\" and \"How to Disclose\" sections compared to PF-19/PF-20: identical wording.",
        "used_for": "Re-verification of PF-19, PF-20, PF-21 wording.",
    },
]
have = {s["id"] for s in src["sources"]}
for s in new_sources:
    if s["id"] not in have:
        src["sources"].append(s)
save("sources.json", src)

# ---------------------------------------------------------------- products
prod = load("products.json")
prod["retrieved"] = "2026-11-13; re-verified 2026-11-14"
prod["note"] = (
    "Null means UNVERIFIED: the value could not be confirmed from an official source and is "
    "intentionally blank. Nothing has been inferred. A non-null value must carry a source ID "
    "(checked by scripts/check_site.py). Values filled on 2026-11-14 describe the Amazon listing "
    "each submitted link opens (observed live on 2026-11-13 and again on 2026-11-14); the "
    "9-character submitted codes are short-link codes, not ASINs (FLG-001, FLG-022)."
)

observed = {
    "P1": {
        "product_name": "CHEFMAN 6 Quart Dual Basket Air Fryer Oven with Easy View Windows, Sync Finish, Hi-Fry, Auto Shutoff, 2 Independent 3Qt Nonstick Dishwasher Safe Frying Baskets, Digital Double Air Fryer - Black",
        "brand": "CHEFMAN",
        "price": "USD 79.93 (observed 2026-11-14; list USD 99.99)",
        "rating": "4.2 out of 5 (observed 2026-11-14)",
        "review_count": "4.8K as displayed (observed 2026-11-14)",
        "obs": {
            "date": "2026-11-14",
            "price": "USD 79.93 (deal shown; List: USD 99.99)",
            "other_offers": "More Buying Choices from USD 57.45 (2+ used & new offers)",
            "rating": "4.2 out of 5 stars",
            "review_count": "(4.8K) as displayed by Amazon",
            "sales_note": "1K+ bought in past month, as displayed",
            "category_path": "Home & Kitchen > Kitchen & Dining > Small Appliances > Fryers > Air Fryers (breadcrumb on the product page)",
            "sources": ["S30", "S33", "S14"],
        },
        "sources": ["S08", "S11", "S14", "S02", "S30", "S33"],
        "value_sources": {"product_name": ["S30", "S33", "S14"], "brand": ["S14"], "price": ["S33"], "rating": ["S33"], "review_count": ["S33"]},
        "flags": ["FLG-001", "FLG-002", "FLG-004", "FLG-022", "FLG-023"],
    },
    "P2": {
        "product_name": "Emeril Lagasse 26QT French Door Multi-Function Air Fryer Toaster Oven | 26QT air fryer oven with French doors, 24 cooking functions, dual-speed fan and rotisserie for easy family meals.",
        "brand": "Emeril Lagasse",
        "price": "USD 149.99 (observed 2026-11-14; list USD 209.99)",
        "rating": "4.3 out of 5 (observed 2026-11-14)",
        "review_count": "18.3K as displayed (observed 2026-11-14)",
        "obs": {
            "date": "2026-11-14",
            "price": "USD 149.99 (deal labelled Early Black Friday Deal; List: USD 209.99)",
            "other_offers": "More Buying Choices from USD 92.99 (2+ used & new offers)",
            "rating": "4.3 out of 5 stars",
            "review_count": "(18.3K) as displayed by Amazon",
            "sales_note": "4K+ bought in past month, as displayed",
            "category_path": "Home & Kitchen > Kitchen & Dining > Small Appliances > Fryers > Air Fryers (breadcrumb on the product page)",
            "sources": ["S31", "S34", "S15"],
        },
        "sources": ["S09", "S12", "S15", "S02", "S31", "S34"],
        "value_sources": {"product_name": ["S31", "S34", "S15"], "brand": ["S15"], "price": ["S34"], "rating": ["S34"], "review_count": ["S34"]},
        "flags": ["FLG-001", "FLG-002", "FLG-004", "FLG-022", "FLG-023"],
    },
    "P3": {
        "product_name": "Chefman Air Fryer 8 Qt | TurboFry\u00ae 4-in-1 with 450\u00b0F Hi-Fry Option for Crispier Results | Bake, Dehydrate, Frozen | XL Nonstick Dishwasher-Safe Basket | Stainless Steel",
        "brand": "Chefman",
        "price": "USD 79.91 (observed 2026-11-14; list USD 119.99)",
        "rating": "4.4 out of 5 (observed 2026-11-14)",
        "review_count": "16.8K as displayed (observed 2026-11-14)",
        "obs": {
            "date": "2026-11-14",
            "price": "USD 79.91 (deal shown; List: USD 119.99)",
            "other_offers": "More Buying Choices from USD 49.54 (3+ used & new offers)",
            "rating": "4.4 out of 5 stars",
            "review_count": "(16.8K) as displayed by Amazon",
            "sales_note": "3K+ bought in past month, as displayed",
            "category_path": "Home & Kitchen > Kitchen & Dining > Small Appliances > Fryers > Air Fryers (breadcrumb on the product page)",
            "sources": ["S32", "S35", "S23"],
        },
        "sources": ["S10", "S13", "S16", "S02", "S32", "S35"],
        "value_sources": {"product_name": ["S32", "S35", "S23"], "brand": ["S23"], "price": ["S35"], "rating": ["S35"], "review_count": ["S35"]},
        "flags": ["FLG-001", "FLG-002", "FLG-004", "FLG-022", "FLG-023"],
    },
}

for p in prod["products"]:
    upd = observed[p["id"]]
    ro = p["redirect_observed"]
    ro["reverified"] = "2026-11-14 (same destination with a fresh redirect token; see S30-S32)"
    ro["confirmed_as_submitted_product_note"] = (
        "false means: no official source states what the owner intended by the code. "
        "The redirect itself is stable (4 observations over 2026-11-13 and 2026-11-14), "
        "so this listing is used as the product the submitted link opens (FLG-022, FLG-024)."
    )
    p["product_name"] = upd["product_name"]
    p["brand"] = upd["brand"]
    p["price"] = upd["price"]
    p["rating"] = upd["rating"]
    p["review_count"] = upd["review_count"]
    p["observed"] = upd["obs"]
    p["value_sources"] = upd["value_sources"]
    p["flags"] = upd["flags"]
    p["sources"] = upd["sources"]
    p["status"] = (
        "The submitted code is a 9-character short-link code, not an ASIN (FLG-001). "
        "The link resolves, stably across 2026-11-13 and 2026-11-14, to the Amazon listing "
        f"{ro['page_id']}; the values in this row describe that listing as observed on 2026-11-14 "
        "(FLG-022). Commission rate, best-seller rank, competitor count, clicks and conversions "
        "remain unverified and blank (FLG-004, FLG-005, FLG-010, FLG-011)."
    )
save("products.json", prod)

# ---------------------------------------------------------------- flags
fl = load("flags.json")
fl["retrieved"] = "2026-11-13; updated 2026-11-14"
by_id = {f["id"]: f for f in fl["flags"]}

by_id["FLG-002"]["detail"] += (
    " Update 2026-11-14 (session 9fef7647): all three links were re-fetched with fresh redirect "
    "tokens and each resolved to the same listing as on 2026-11-13 (S30-S32). The 'not confirmed' "
    "wording now refers only to the owner's intent (which product was meant by the code), not to "
    "the stability of the mapping, which has been observed 4 times over 2 days (FLG-022, FLG-024)."
)
by_id["FLG-004"]["detail"] += (
    " Update 2026-11-14 (session 9fef7647): price, rating and review count are now shown as dated "
    "snapshots observed on Amazon's own search pages (S33-S35). They are volatile deal prices and "
    "their display on a live Associates site is restricted by Participation Requirements 2(b) and "
    "6(t) (PF-04, PF-05) - see FLG-023. Competitor count, best-seller rank, availability, clicks "
    "and conversions remain unverified and blank."
)
by_id["FLG-001"]["action"] += (
    " Update 2026-11-14: the listing each link opens is now recorded (FLG-022); the request for "
    "owner confirmation of intent stands."
)
by_id["FLG-021"]["detail"] += (
    " Update 2026-11-14: the category breadcrumb is now observed on each product page "
    "(Home & Kitchen > Kitchen & Dining > Small Appliances > Fryers > Air Fryers; S30-S32). "
    "Whether the commission schedule's 'Kitchen' category maps to this node is still not "
    "documented in any public source, so the reference rate stays a reference only."
)

new_flags = [
    {
        "id": "FLG-022",
        "severity": "High",
        "category": "Product identity",
        "item": "Product identity rests on observed short-link redirects, not on documented identifiers",
        "detail": (
            "The three submitted codes are 9 characters and are not ASINs (FLG-001). Each submitted "
            "link resolves to exactly one Amazon listing, and the mapping was identical across 4 "
            "observations on 2026-11-13 and 2026-11-14 (S11-S13, S30-S32). Control tests on the "
            "shortener (recorded in COORDINATION.md, Z-V10 to Z-V14) show the codes are registered "
            "short codes: junk codes of the same length are rejected with 403/404. No official "
            "Amazon source documents the code-to-listing registry, so the association is recorded "
            "as observed, and this site treats each listing as the product its submitted link opens. "
            "If the owner intended different products, the tables must be re-pointed."
        ),
        "action": "Owner: confirm that the three listings recorded here are the intended products.",
        "sources": ["S11", "S12", "S13", "S30", "S31", "S32", "S14", "S15", "S23"],
    },
    {
        "id": "FLG-023",
        "severity": "Medium",
        "category": "Display compliance",
        "item": "Observed prices and star ratings are shown for analysis only; display on a live Associates site is restricted",
        "detail": (
            "Participation Requirements 2(b) (PF-04) allow a site to show prices and availability only "
            "when Amazon serves the link or through the Product Advertising API, and 6(t) (PF-05) bars "
            "displaying customer reviews or star ratings unless obtained through the API or a "
            "qualifying link. The prices and ratings on this site are dated observations (2026-11-14, "
            "S33-S35) kept for analysis, with a date stamp adjacent per PF-27. Before this site is "
            "used commercially, remove these values or re-source them via Special Links or the "
            "Creators API. Prices are also volatile deal prices (Z-F5 in COORDINATION.md)."
        ),
        "action": "Remove or re-source observed prices/ratings via API or Special Links before commercial use.",
        "sources": ["S02", "S33", "S34", "S35"],
    },
    {
        "id": "FLG-024",
        "severity": "Low",
        "category": "Cross-session record",
        "item": "Earlier builds disagreed on whether the links resolve; re-verification 2026-11-14 settles the factual part",
        "detail": (
            "The root build (sessions 7f84fea4/33226b37) recorded that the submitted identifiers "
            "select no product page; the /docs/ build (session 79f85104, Z-F6) recorded that all three "
            "short links resolve to real listings, with control evidence Z-V10 to Z-V14. Session "
            "9fef7647 re-fetched all three links on 2026-11-14 and reproduced the /docs/ result "
            "exactly (S30-S32). Both earlier statements are true of different things: the codes are "
            "not ASINs (they select nothing at amazon.com/dp/), and the links resolve stably to "
            "three listings. This site now states both."
        ),
        "action": "No action needed unless the owner disputes the resolved products (FLG-022).",
        "sources": ["S08", "S09", "S10", "S30", "S31", "S32"],
    },
]
have = {f["id"] for f in fl["flags"]}
for f in new_flags:
    if f["id"] not in have:
        fl["flags"].append(f)
save("flags.json", fl)

print("data updated:", len(src["sources"]), "sources,", len(fl["flags"]), "flags")
