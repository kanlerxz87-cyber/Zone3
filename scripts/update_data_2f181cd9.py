#!/usr/bin/env python3
"""Session 2f181cd9 integration: add this session's sources, flags and the two new
products to the shared registers, then rewrite the shared copy that says "three" where
five links now exist.

Everything here is additive or a targeted string replacement. No existing ID is
renumbered, no other session's entry is removed, and nothing that could not be verified
from an official source is filled in.

    python3 scripts/update_data_2f181cd9.py
"""
from __future__ import annotations

import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
SESSION = "2f181cd9"
DATE = "2026-11-17"


def load(name: str):
    return json.loads((DATA / name).read_text(encoding="utf-8"))


def save(name: str, obj) -> None:
    (DATA / name).write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


# ------------------------------------------------------------------ sources
def add_sources() -> None:
    shared = load("sources.json")
    mine = load("2f/verification.json")
    have = {s["id"] for s in shared["sources"]}
    added = 0
    for s in mine["sources"]:
        if s["id"] in have:
            raise SystemExit(f"source id collision on {s['id']}")
        shared["sources"].append({
            "id": s["id"],
            "title": s["title"],
            "url": s["url"],
            "publisher": s.get("publisher", "Amazon (official)"),
            "status": s.get("status", "observed"),
            "status_note": s.get("status_note", f"Read {DATE} by session {SESSION}."),
            "used_for": s.get("used_for", ""),
            "session": SESSION,
        })
        added += 1
    shared["retrieved"] = (
        shared["retrieved"]
        + f" | {DATE}: session {SESSION} appended S70-S82 (the two new submitted links, their destinations "
        "and direct-identifier checks, the three original links re-fetched, and the Operating Agreement, "
        "Program Policies, Table 1 and the ASIN definition re-read)."
    )
    shared["id_reservation"] = (
        "S01-S59 are held by earlier sessions (main@110). S60-S69 are claimed by session 145b8df7 for its "
        "2026-11-16 re-verification captures. S70-S82 are claimed by session 2f181cd9 (2026-11-17) for the "
        "five-link intake and policy re-reads. All three ranges are NOT free: a session rebasing onto an older "
        "main must append from S83, or renumber its own entries and then read back every reference target -- an "
        "id-existence check will not catch a collision, because both ids exist and point at different documents."
    )
    save("sources.json", shared)
    print(f"sources: +{added} (now {len(shared['sources'])})")


# ------------------------------------------------------------------ flags
FLAGS_ADD = [
    {
        "id": "F-2F-01",
        "severity": "High",
        "category": "Scope (owner decision)",
        "item": "Two of the five submitted links open listings in a category the site is not written for",
        "detail": (
            "The brief for this session supplies five product links. Three open air-fryer listings under "
            "Home & Kitchen > Kitchen & Dining > Small Appliances > Fryers > Air Fryers (browse node 17659096011). "
            "The two added this session, link.amazon/B0c8moW59 and link.amazon/B0f3GKalj, open meat-thermometer "
            "listings under Home & Kitchen > Kitchen & Dining > Kitchen Utensils & Gadgets > Thermometers & Timers "
            "> Meat (browse node 289810): B0DHZTCNR5 (ThermoMaven 1 Sec Professional Digital Meat Thermometer) and "
            "B0DZFD6R9Z (CHEF iQ Sense Smart Wireless Meat Thermometer, Gen3). The site name, navigation, category "
            "pages, comparison and article plan are all air-fryer specific. No source read in this project states "
            "the owner's intent for any of the five links, so this is published as a decision for the owner "
            "(SUG-2F-01 on sessions/2f181cd9/decision-lab.html) rather than acted on."
        ),
        "action": (
            "Owner decision: pick one of the three scope paths in SUG-2F-01 (one publication with two category "
            "hubs, two microsites, or air fryers only with the two thermometer links held unpublished), and record "
            "the intended ASIN for each link with a confirmation date in the intake register."
        ),
        "date": DATE,
        "session": SESSION,
        "status": "open",
        "sources": ["S70", "S71", "S72", "S73", "S76", "S77", "S78"],
        "repo_evidence": "sessions/2f181cd9/intake.html — the five-link intake register, intended and observed columns separate",
    },
    {
        "id": "F-2F-02",
        "severity": "Medium",
        "category": "Product identity",
        "item": "Both new identifiers are nine characters, so neither is an ASIN, and both direct /dp/ checks return Page Not Found",
        "detail": (
            "Amazon defines an ASIN as a 10-character alphanumeric unique identifier (Creators API GetItems, "
            "ItemIdType table, read 2026-11-17). B0c8moW59 and B0f3GKalj are nine characters, and "
            "amazon.com/dp/B0c8moW59 and amazon.com/dp/B0f3GKalj each return Amazon's Page Not Found page, exactly "
            "as the first three identifiers do. The nine-character tokens are short-link identifiers, and the "
            "listing they open is an observed destination, not a confirmed identity."
        ),
        "action": "No action by the site. Fill the intended_* columns of the intake register when the owner confirms the five ASINs.",
        "date": DATE,
        "session": SESSION,
        "status": "open",
        "sources": ["S74", "S75", "S82"],
        "repo_evidence": "sessions/2f181cd9/intake.html",
    },
    {
        "id": "F-2F-03",
        "severity": "High",
        "category": "Revenue",
        "item": "No link on the site carries an Associates tag, including the two new links",
        "detail": (
            "Participation Requirements 2(b) requires the Associates tag as a URL parameter on every link to an "
            "Amazon Site. The two new submitted links contain no tag, and no tag has been supplied for the site, "
            "so five of five links can be clicked without earning anything."
        ),
        "action": "Supply the tag, build one Special Link per product, test one end to end, then scale (SUG-2F-06).",
        "date": DATE,
        "session": SESSION,
        "status": "open",
        "sources": ["S80"],
        "repo_evidence": "sessions/2f181cd9/intake.html and data/2f/intake.json",
    },
    {
        "id": "F-2F-04",
        "severity": "Medium",
        "category": "Commission",
        "item": "No commission rate can be stated for any of the five listings",
        "detail": (
            "The published Standard Commission Income Statement Table 1 (read 2026-11-17) gives Kitchen 4.50%, "
            "Home 3.00% and All Other Categories 4.00%. No official page read in this project maps a browse node "
            "to a Table 1 category, and the two new listings sit in a different part of the tree from the first "
            "three, so the question is now sharper rather than answered: the same table may or may not apply to "
            "both groups."
        ),
        "action": (
            "Read the classification back through the Creators API once access exists, or take the realised rate "
            "from the owner's own Associates reports. Do not publish a per-product rate until then."
        ),
        "date": DATE,
        "session": SESSION,
        "status": "open",
        "sources": ["S81", "S72", "S73"],
        "repo_evidence": "sessions/2f181cd9/questions.html#Q2F-04",
    },
    {
        "id": "F-2F-05",
        "severity": "Medium",
        "category": "Compliance",
        "item": "Outbound product links are marked rel=\"sponsored\" on 6 links and not on the rest of the site",
        "detail": (
            "A repository-wide scan on 2026-11-17 counted 6 outbound links carrying rel=sponsored against more "
            "than 2,300 that do not, so the same class of link is marked two different ways depending on which "
            "generator built the page. The brief requires every outbound product link to be marked as sponsored. "
            "This session's own pages mark every outbound Amazon link with rel=\"sponsored noopener noreferrer\"."
        ),
        "action": (
            "Cross-scope change request: change the link helper in each generator so every outbound product link "
            "carries rel=\"sponsored\", then rebuild. Suggestion SUG-2F-07 on sessions/2f181cd9/decision-lab.html."
        ),
        "date": DATE,
        "session": SESSION,
        "status": "open",
        "sources": ["S79", "S80"],
        "repo_evidence": "grep -c 'rel=\"[^\"]*sponsored' across the published pages, run 2026-11-17",
    },
    {
        "id": "F-2F-06",
        "severity": "Medium",
        "category": "Information architecture",
        "item": "The reader's path runs through an operations dashboard, and the page set is large",
        "detail": (
            "The root page opens with a hero and then a status callout, statistics about the verification "
            "process, and a site map listing 78 pages including per-session archives and superseded builds. The "
            "brief asks for a publication front page with every dashboard surface reachable from the footer and a "
            "single navigation group."
        ),
        "action": "Owner decision between the two paths in SUG-2F-02; then consolidate the page set as in SUG-2F-10.",
        "date": DATE,
        "session": SESSION,
        "status": "open",
        "sources": ["S79"],
        "repo_evidence": "index.html at the base commit, and the design diagnosis on sessions/2f181cd9/design-direction.html",
    },
    {
        "id": "F-2F-07",
        "severity": "Low",
        "category": "Design",
        "item": "Four visual languages are published on one domain",
        "detail": (
            "assets/style.css, assets/front-door.css, assets/read.css and site/assets each define their own "
            "palette, type stack and card shape, so following an internal link can arrive at a page that looks "
            "like a different website."
        ),
        "action": "Adopt one token set and rebuild every surface against it (SUG-2F-03).",
        "date": DATE,
        "session": SESSION,
        "status": "open",
        "sources": ["S79"],
        "repo_evidence": "the four stylesheets in this repository, and the diagnosis table on sessions/2f181cd9/design-direction.html",
    },
    {
        "id": "F-2F-08",
        "severity": "Low",
        "category": "Editorial",
        "item": "Product pages carry no photography",
        "detail": (
            "Every product block is typographic. Imagery is the single largest visual upgrade available, and it "
            "is constrained: images must be Amazon-served Program Content or the owner's own photographs. "
            "Generated or copied photography is not an option."
        ),
        "action": "Pick a path in SUG-2F-04 once the tag or the products are available.",
        "date": DATE,
        "session": SESSION,
        "status": "open",
        "sources": ["S79", "S80"],
        "repo_evidence": "marketing/product-*.html at the base commit",
    },
    {
        "id": "F-2F-09",
        "severity": "Low",
        "category": "Content accuracy (cross-scope)",
        "item": "Copy that says 'three air fryers' remains on surfaces this session does not own",
        "detail": (
            "This session updated the shared copy in scripts/build_site.py so that products.html, pricing.html, "
            "reviews.html, campaigns.html, content.html and the executive summary read correctly for five links. "
            "Surfaces owned by other generators still say three, including the front-door band injected into "
            "index.html by tools/build_cba81fa5_site.py ('Which of these three air fryers fits your kitchen?'), "
            "the /read/ pages built by scripts/build_read.py, the /site/ pages built by tools/build_i2_site.py and "
            "tools/build_cba81fa5_site.py, and the marketing pages under /marketing/ that compare three listings. "
            "Left as written rather than half-updated: the marketing comparison genuinely covers three air fryers, "
            "and the front-door band is an injected region this session does not generate."
        ),
        "action": (
            "Change request for the owner or the next integration session: decide the scope (F-2F-01) and then "
            "regenerate or re-word those surfaces in one pass, so the site never mixes 'three' and 'five'."
        ),
        "date": DATE,
        "session": SESSION,
        "status": "open",
        "sources": ["S70", "S71"],
        "repo_evidence": "grep -rn 'three air fryers|three listings' across the generated pages, run 2026-11-17",
    },
    {
        "id": "F-2F-10",
        "severity": "Info",
        "category": "Method",
        "item": "This session's sandbox could only reach the network through the page-fetch tool",
        "detail": (
            "Command-line fetches to amazon.com and link.amazon were refused at the connection layer in this "
            "session's sandbox, so every observation was taken through the page-fetch tool instead. Each "
            "observation names the exact URL that was fetched, so it can be repeated by hand. This is recorded "
            "because it is a difference in method from earlier sessions, which used command-line fetches."
        ),
        "action": "No action. Noted so a reviewer knows how the observations were taken.",
        "date": DATE,
        "session": SESSION,
        "status": "open",
        "sources": ["S70"],
        "repo_evidence": "sessions/2f181cd9/index.html",
    },
]


def add_flags() -> None:
    shared = load("flags.json")
    have = {f["id"] for f in shared["flags"]}
    added = 0
    for f in FLAGS_ADD:
        if f["id"] in have:
            raise SystemExit(f"flag id collision on {f['id']}")
        shared["flags"].append(f)
        added += 1
    shared["note"] = (
        shared["note"]
        + f" Session {SESSION} ({DATE}) added F-2F-01 to F-2F-10: the five-link intake (two links open a second "
        "category), the missing Associates tag, the unverifiable per-product commission rate, the rel=sponsored "
        "inconsistency, the information-architecture and design findings, and a method note. All are published on "
        "flagged.html; none blocks the merge."
    )
    save("flags.json", shared)
    print(f"flags: +{added} (now {len(shared['flags'])})")


# ------------------------------------------------------------------ products
def add_products() -> None:
    products = load("products.json")
    have = {p["id"] for p in products["products"]}
    if "P4" in have or "P5" in have:
        print("products: P4/P5 already present, skipping")
        return
    intake = {l["id"]: l for l in load("2f/intake.json")["links"]}
    for pid in ("P4", "P5"):
        l = intake[pid]
        o = l["observed"]
        products["products"].append({
            "id": pid,
            "label": f"Product link {pid[1]}",
            "submitted_url": l["submitted_url"],
            "link_id": l["link_id"],
            "link_id_length": l["link_id_length"],
            "asin": None,
            "direct_check": {
                "url": l["direct_check"]["url"],
                "result": l["direct_check"]["result"],
                "source": l["direct_check"]["source"][0],
            },
            "redirect_observed": {
                "final_url": o["final_url"],
                "page_id": o["page_id"],
                "page_title": o["page_title"],
                "confirmed_as_submitted_product": False,
                "source": o["source"][0],
                "title_source": o["source"][-1],
                "brand": "ThermoMaven" if pid == "P4" else "CHEF iQ",
                "capacity": "Not stated in the listing title",
                "brand_capacity_note": (
                    "Read from the destination page title. Not confirmed as the submitted product (FLG-002, "
                    "F-2F-02). This listing is a meat thermometer, not an air fryer (F-2F-01)."
                ),
                "reverified": f"{DATE}, first observation by session {SESSION}.",
                "note": (
                    "Recorded only as the page the submitted link opens. Whether the owner intended that product "
                    "is not documented by any source read (FLG-002, FLG-035, F-2F-01)."
                ),
            },
            "category_observed": l["category_observed"],
            "browse_node_observed": l["browse_node_observed"],
            "content_status": {
                "brief": "Not written",
                "comparison": "Not written",
                "buying_guide": "Not written",
                "note": (
                    "No brief, comparison or buying guide has been written for this link. The marketing section "
                    "covers the three air-fryer listings only; extending it to this category is part of the scope "
                    "decision in F-2F-01 and SUG-2F-01."
                ),
            },
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
            "status": (
                "Link opens a meat-thermometer listing, not an air fryer. Observed destination recorded; intent "
                "unconfirmed (F-2F-01). No Associates tag, so no Special Link exists (F-2F-03)."
            ),
            "flags": ["F-2F-01", "F-2F-02", "F-2F-03", "FLG-001", "FLG-002", "FLG-035"],
            "sources": ["S80", "S82", l["direct_check"]["source"][0]] + o["source"],
        })
    products["note"] = (
        products["note"]
        + f" INTEGRATION ({DATE}, session {SESSION}): P4 and P5 added for the two links supplied in this "
        "session's brief. Both open meat-thermometer listings, so the register now spans two categories - see "
        "F-2F-01. Intended ASIN, product name, brand, price, rating, review count, rank, commission rate and "
        "availability stay null for them exactly as for P1-P3: no official source ties those values to a "
        "submitted nine-character token."
    )
    save("products.json", products)
    print(f"products: +2 (now {len(products['products'])})")


def main() -> int:
    add_sources()
    add_flags()
    add_products()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
