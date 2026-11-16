#!/usr/bin/env python3
"""Adds session ab3ed329's flags (AB-F-01..05) to data/flags.json. Idempotent.
Flag text deliberately contains no observed price, rating or review-count value."""
import json, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[2]
p = ROOT / "data/flags.json"
d = json.loads(p.read_text())
ids = {f["id"] for f in d["flags"]}
new = [
 {"id": "AB-F-01", "severity": "High", "category": "Compliance",
  "item": "Other sessions' published pages and archives still display observed Amazon prices, star ratings or review counts",
  "detail": ("Session ab3ed329 removed observed price, rating, review-count and sales values from the public registers "
             "it could change: data/products.json (observed block for all three listings), data/sources.json (S46-S48 "
             "status notes) and quoted text in data/flags.json and data/z3/flags.json. The same values remain in pages "
             "and files owned by other sessions or kept as archives, which this session did not edit under the "
             "COORDINATION.md rule: docs/ (the archived 2026-11-13 build), sessions/3c886b62/ (product, category, "
             "comparison, analysis and verification pages, and its data/products.json), sessions/03bbd050/ (index, "
             "findings, verification), sessions/f2102efa/verification.md, sessions/3c886b62/verification.html, the "
             "51fcb80d and c4e71983 snapshot JSON files and research/ verification logs. Program Policies 2(b) and 6(t) "
             "apply to any display on a Site, including an archive."),
  "action": ("Owner decision for each path: remove the page, or remove the literal values and keep the dated source "
             "link. The archived /docs/ build is the largest exposure. Change requests are logged in COORDINATION.md "
             "(AB Part)."),
  "sources": ["S02", "S01"]},
 {"id": "AB-F-02", "severity": "Low", "category": "Wording",
  "item": "FLG-001 says no product name can be tied to the identifiers, but the Products page shows observed listing titles",
  "detail": ("FLG-001 states that no product name, brand, price, rating or commission can be tied to the submitted "
             "identifiers. The Products page and the product register do show the title of the Amazon listing each "
             "short link opens, with the brand and capacity read from that title. product_name stays null, and each row "
             "says the destination is not confirmed as the submitted product (FLG-002). The two statements agree only if "
             "'observed destination' is read as the identity not being established. The FLG-001 wording should match "
             "the Products page."),
  "action": ("Owner to confirm the intended product for each link. Until then, keep the wording 'observed destination' "
             "everywhere and do not present a listing title as the product identity."),
  "sources": ["S06", "S11", "S14"]},
 {"id": "AB-F-03", "severity": "Medium", "category": "Governance",
  "item": "COORDINATION.md is over 5,000 lines and many claims are still marked in progress",
  "detail": ("The shared task board has grown into one file of more than 5,000 lines. Many claims are still marked "
             "'in progress' from 2026-11-13 and 2026-11-14 with no closing record, and several registry rows read "
             "'unknown' or 'not read'. A new session cannot tell from the board which claims are live. Session "
             "ab3ed329 claimed its own tasks, edited no other session's rows, and found no live conflict with its scope."),
  "action": ("Owner to close or archive stale claims and move completed Parts to archive/. Not changed by this session "
             "because the file is shared by all sessions."),
  "repo_evidence": ("COORDINATION.md: 5,000+ lines; the words 'in progress' appear on 79 lines at the time of the "
                    "2026-11-16 check (sessions/ab3ed329/index.html, method in its Verification table).")},
 {"id": "AB-F-04", "severity": "Low", "category": "Duplication",
  "item": "Duplicate registers and pages: two product registers, two flag registers, several executive summaries and two category paths",
  "detail": ("The repository keeps overlapping copies of the same data and documents. Each copy was correct for the date "
             "it was written, but none of the three gate scripts (check_site.py, verify_site.py, link_report.py) reads "
             "both members of a pair, so the copies can drift apart without a failure. Session ab3ed329 did not merge them."),
  "action": "Owner to choose one canonical file for each register and archive the rest.",
  "repo_evidence": ("data/products.json and data/z3/products.json; data/flags.json and data/z3/flags.json; "
                    "EXECUTIVE-SUMMARY.md, executive-summary.html, executive-summary/index.html and docs/executive-summary*.md; "
                    "category/air-fryers.html and categories/home-kitchen-air-fryers.html.")},
 {"id": "AB-F-05", "severity": "Info", "category": "Correction",
  "item": "Status date and navigation corrected on rebuild (2026-11-16)",
  "detail": ("The generated status date moved from 2026-11-14 to 2026-11-16. Six marketing pages were regenerated because "
             "their navigation predated the Decision Center. sitemap.xml was regenerated: it had omitted analysis.html, "
             "which is a live page. The sitemap lists disclosure.html, which only redirects to content.html; that is "
             "recorded here and left for the owner to decide."),
  "action": "None required. Recorded as a correction to this site.",
  "repo_evidence": ("scripts/build_site.py BUILT constant; marketing/*.html navigation; sitemap.xml; "
                    "sessions/ab3ed329/index.html (correction list).")},
]
added = 0
for f in new:
    if f["id"] not in ids:
        d["flags"].append(f); added += 1
p.write_text(json.dumps(d, indent=2, ensure_ascii=False) + "\n")
print("added", added, "flags; total", len(d["flags"]))
