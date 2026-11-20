#!/usr/bin/env python3
"""Re-apply this session's additive register entries after a rebase (session 2e0d5c15).

Why this exists. The register files conflict every time another session lands work, and
hand-resolving them is how conflict markers ended up in the published tree (flag 2E0-F03).
This script is deterministic and idempotent: it appends the five decision-desk entries and
three flag rows only if their ids are absent, and it never rewrites an existing row.

    python3 sessions/2e0d5c15/apply_additions.py
"""
from __future__ import annotations

import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
PUB = ROOT / 'data' / 'publication.json'
FLAGS = ROOT / 'data' / 'flags.json'

PROPOSALS = [
 {"id":"2E0-P1","priority":"Next","area":"Content",
  "title":"Publish the day-after guide: reheating in an air fryer, and the one number that decides it.",
  "why":"The seasonal cluster covers the meal; nothing covers the days after it. USDA's Food Safety and Inspection Service publishes a single figure a reader can act on with a thermometer — leftovers reach 165°F as measured with a food thermometer — and the FoodSafety.gov chart this site already cites repeats it for leftovers and casseroles. That is a question-shaped article with no product claim inside it.",
  "next":"Open the FSIS 'Leftovers and Food Safety' page and the FoodSafety.gov chart, record both as register sources with the date read, confirm the reheat figure and the two-hour refrigeration rule are unchanged, then draft through the same gate as the current guides.",
  "evidence_needed":["food-safety"],"source":"food-safety","status":"Proposed",
  "next_action":"Add the FSIS leftovers page and the FSIS food-thermometer factsheet to data/publication.json sources, write the guide with the 165°F reheat rule, the 40–140°F danger zone and the two-hour refrigeration rule quoted and dated, link it from the thermometer and air-fryer category pages, and let the build add it to the feed and sitemap.",
  "discoveries":["Whether FSIS has changed the 165°F reheat figure or the two-hour rule since its page was last updated.","Whether anyone reaches the site with a reheating question — not measurable until Search Console ownership is verified."],
  "owner_input_needed":False,"reviewable_now":True},
 {"id":"2E0-P2","priority":"Next","area":"Findability",
  "title":"Describe the breadcrumb trail in structured data on every guide.",
  "why":"Each guide already shows The edit / Buying guides / category above its title. Google's structured-data documentation describes BreadcrumbList as the machine-readable form of exactly that trail, so it states nothing a page does not already show and needs no new evidence.",
  "next":"Add one BreadcrumbList block beside the existing Article block in the guide template, keep the visible trail as its source of truth, then validate one deployed URL in Google's Rich Results Test and record what it returns.",
  "evidence_needed":["google-structured-data"],"source":"google-structured-data","status":"Proposed",
  "next_action":"Render BreadcrumbList JSON-LD on guides/*.html from the same three labels the visible trail uses, add a check in tools/check_publication.py that the markup and the trail agree, and re-run the release gate.",
  "discoveries":["Whether Google still returns breadcrumb rich results for pages of this kind.","Whether the markup can drift from the visible trail without a gate noticing."],
  "owner_input_needed":False,"reviewable_now":True},
]

QUESTIONS = [
 {"id":"2E0-Q1",
  "question":"Who re-measures the registers on every release, and what makes a re-measure line trustworthy?",
  "known":"This register's method says it: append a dated line, never rewrite a dated record. In practice four cells still closed on a figure the registers do not hold, after an integration session had recorded them as fixed (EE-F-02, corrected here as 2E0-F01).",
  "missing":"A named owner for the re-measure step at release, and a rule that no row may close on a figure that disagrees with its register on the day of the merge.",
  "discovery":"Run the read-only scripts (sessions/8aa259bb/measure_brief_rows.py, sessions/41e84402/measure_drift.py) before every pull request, read the last sentence of each row against the register, and append a dated correction where they disagree.",
  "default":"Append, never rewrite; a row whose last line contradicts the register is listed on the Flagged page until it is corrected.",
  "blocks":"Nothing; the release gate runs whether or not the question is answered",
  "source":"google-helpful","owner_input_needed":True},
 {"id":"2E0-Q2",
  "question":"Should the four pages that still carry malformed HTML be repaired or retired?",
  "known":"Measured on this tree: four published pages carry stray end tags — category/kitchen.html, site/flagged.html, site/guides/air-fryer-oven-vs-basket.html, site/guides/index.html — each an unclosed inline element inside a list or a table. A related defect on two other pages (an unescaped <token> and <short-id> that dropped a word from the rendered sentence) was fixed in its generators during this pass. All four remaining pages are noindex,follow, none is in the sitemap or the feed, and none is written by the current reader generator.",
  "missing":"An owner decision on whether these surfaces are kept as history, repaired inside their own generator, or removed — and who does the repair.",
  "discovery":"List each page's inbound links from the reader set, then repair through the generator that writes it; a hand edit is overwritten by the next build.",
  "default":"Leave them live and noindex; they carry the disclosure and break no reader path.",
  "blocks":"Nothing","source":"google-page-experience","owner_input_needed":True},
 {"id":"2E0-Q3",
  "question":"Should the release gate refuse a merge-conflict marker anywhere in the published tree?",
  "known":"Measured 2026-11-20: two occurrences of merge debris were live on main — a stray marker line in COORDINATION.md and a bare '=======' line in assets/publication.css — and no gate noticed either; the release checks read structure, links, provenance and claims, not the absence of merge debris. The marker recurred once inside this session's own rebase. Both occurrences were removed by this pass (flag 2E0-F03).",
  "missing":"An owner decision on whether that check belongs in the gate, and how broadly to scope it (the published files only, or sessions/ and docs/ too).",
  "discovery":"Run a one-line scan over the tree before every release; it takes under a second and prints the file, the line and the marker.",
  "default":"Scan and fix by hand until the check is adopted; nothing is published with a marker knowingly.",
  "blocks":"Nothing","source":"google-helpful","owner_input_needed":True},
]

FLAG_ROWS = [
 {"id":"2E0-F01","severity":"Medium","category":"Register",
  "item":"Re-measure lines that contradicted the registers survived a pass that recorded them as fixed",
  "detail":"Flag EE-F-02 (session ee10b024) records rows S-04, S-05, S-09, S-24, SG-28 and SG-29 as re-measured and fixed in place. Read on 2026-11-20, four cells still ended with a figure their registers do not hold: SG-29 closed with '18 URLs on the merged tree' while sitemap.xml and data/publication.json listed 20 when this pass began (and 27 after the same day's merges); S-07 closed with 'ten question-led guides' and S-24 with 'ten published guides' while the register held 11, then 13; S-13 closed with 'nine question-shaped guides' against the same 11-then-13. Two cells contradicted themselves: SG-29 states '20 canonical reader URLs' earlier in the same cell, and S-24 states 'all eleven guides' before the 'ten' sentence. Every earlier sentence is a dated record and is kept.",
  "action":"CORRECTED 2026-11-20 by session 2e0d5c15: one dated correction sentence appended to each of S-07, S-13, S-24 and SG-29, naming the count measured on the merged tree at the time of the pass; no earlier text rewritten; _meta.rechecks entry added. The residual risk is procedural, not editorial: nothing in the release gate compares a row's last measured sentence with its register, so the same drift can recur. Published for review as question 2E0-Q1.",
  "repo_evidence":"data/shop/brief-status.json; data/publication.json; sitemap.xml; feed.xml; sessions/2e0d5c15/verification-2026-11-20.md",
  "sources":[],"date":"2026-11-20","raised":"2026-11-20","session":"2e0d5c15","status":"fixed"},
 {"id":"2E0-F02","severity":"Low","category":"HTML integrity",
  "item":"Six published noindex pages carried malformed HTML nesting, two of them losing a word from the rendered sentence",
  "detail":"Measured 2026-11-20 by parsing every published page (outside archive/, docs/ and sessions/) with Python's html.parser: six reported stray end tags — articles/what-an-amazon-affiliate-link-has-to-look-like.html, category/kitchen.html, products/index.html, site/flagged.html, site/guides/air-fryer-oven-vs-basket.html and site/guides/index.html. Two of the six wrote a placeholder unescaped into the markup (<token> in the article's prose and <short-id> on products/index.html), so a browser read each as an unknown element and the word vanished from the rendered sentence ('a direct /dp/ Page Not Found response does not mean the short link is broken'). All six carry robots noindex,follow, none is listed in sitemap.xml or feed.xml, and none is produced by the current reader generator (tools/build_publication.py). The reader set and every indexable page parsed clean before and after this pass. No browser-measured rendering defect is claimed, because none was measured.",
  "action":"PARTLY FIXED 2026-11-20 by session 2e0d5c15. The two unescaped-placeholder defects were fixed in the generators that write them, not by hand: scripts/build_5a56c084.py now escapes article prose before substituting source markers, and tools/build_site.py writes &lt;short-id&gt;. The nesting audit (sessions/2e0d5c15/nesting_audit.py) then reported 4 pages instead of 6 and all release gates passed. The four that remain — category/kitchen.html, site/flagged.html, site/guides/air-fryer-oven-vs-basket.html, site/guides/index.html — carry unclosed inline elements inside list and table cells; each belongs to an older generator owned by a finished pass, so they are published for review rather than hand-edited. The keep / repair / retire decision is question 2E0-Q2.",
  "repo_evidence":"sessions/2e0d5c15/nesting_audit.py; scripts/build_5a56c084.py; tools/build_site.py; sessions/2e0d5c15/verification-2026-11-20.md",
  "sources":[],"date":"2026-11-20","raised":"2026-11-20","session":"2e0d5c15","status":"needs review"},
 {"id":"2E0-F03","severity":"Medium","category":"Repository hygiene",
  "item":"Merge-conflict debris was live in two published files: the shared board and the site stylesheet",
  "detail":"Two occurrences of the same defect class were live on main. (1) COORDINATION.md carried a stray marker line (the tail of a conflict resolution: '>>>>>>> c126257 …') with no matching opening marker — on the file every parallel session reads before claiming work. (2) assets/publication.css carried a bare '=======' line inside the served stylesheet, likewise left by a merge. None of the release checks looks for merge debris: they read structure, links, provenance and claims. A tree-wide scan over *.html, *.md, *.json, *.py, *.css and *.js found no other occurrence and no generated page affected.",
  "action":"FIXED 2026-11-20 by session 2e0d5c15: both marker lines deleted with the surrounding content of both sessions untouched, and the full gate re-run. The marker recurred several times during this session's own rebases, which is the argument for a check rather than another manual sweep; question 2E0-Q3 asks the owner whether the gate should refuse this class, and how broadly to scope it.",
  "repo_evidence":"COORDINATION.md; assets/publication.css; sessions/2e0d5c15/verification-2026-11-20.md",
  "sources":[],"date":"2026-11-20","raised":"2026-11-20","session":"2e0d5c15","status":"fixed"},
]


def main() -> int:
    pub = json.loads(PUB.read_text(encoding='utf-8'))
    flags = json.loads(FLAGS.read_text(encoding='utf-8'))
    added = []
    have_p = {row['id'] for row in pub['proposals']}
    for row in PROPOSALS:
        if row['id'] not in have_p:
            pub['proposals'].append(row)
            added.append(row['id'])
    have_q = {row['id'] for row in pub['questions']}
    for row in QUESTIONS:
        if row['id'] not in have_q:
            pub['questions'].append(row)
            added.append(row['id'])
    have_f = {row['id'] for row in flags['flags']}
    for row in FLAG_ROWS:
        if row['id'] not in have_f:
            flags['flags'].append(row)
            added.append(row['id'])
    if added:
        PUB.write_text(json.dumps(pub, indent=1, ensure_ascii=False) + '\n', encoding='utf-8')
        FLAGS.write_text(json.dumps(flags, indent=1, ensure_ascii=False) + '\n', encoding='utf-8')
    print(f"applied {len(added)} rows: {', '.join(added) if added else 'nothing to add'}")
    print(f"register: {len(pub['proposals'])} proposals, {len(pub['questions'])} questions, "
          f"{len(pub['indexable_pages'])} indexable pages, {len(flags['flags'])} flags")
    return 0


if __name__ == '__main__':
    sys.exit(main())
