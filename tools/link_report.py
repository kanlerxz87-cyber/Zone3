#!/usr/bin/env python3
"""
Zone3 provenance coverage report.

Answers one question for a reviewer: *for every value shown on the site, is there
an official source behind it?* Reads the datasets (not the HTML — tools/verify_site.py
audits the HTML) and reports coverage per table, per page and per field family.

Usage
    python3 tools/link_report.py            # human-readable report
    python3 tools/link_report.py --json     # machine-readable
    python3 tools/link_report.py --strict   # exit 1 if any table is <100% covered
"""
from __future__ import annotations
import argparse, json, pathlib, sys, collections

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "z3"

TABLES = [
    ("products", "intake & verification", "products.json", ["table", "attributes_table", "affiliate_link_table"]),
    ("policies", "compliance register", "policies.json", ["required_blocks", "prohibitions", "economics"]),
    ("pricing", "pricing analysis", "pricing.json", ["price_rows", "rules", "gate"]),
    ("reviews", "review analysis", "reviews.json", ["review_rows", "integrity", "sentiment_design"]),
    ("niches", "niche analysis", "niches.json", ["scoring_inputs", "candidate_niches", "category_rules"]),
    ("campaigns", "campaign operations", "campaigns.json", ["ledger", "schema", "optimiser"]),
    ("content", "content generation", "content.json", ["inventory", "templates", "grounding", "seo"]),
    ("requirements", "traceability", "requirements.json", ["matrix"]),
    ("agent_terms", "agent governance", "agent_terms.json", ["table", "model_rules", "api"]),
    ("flags", "flagged for review", "flags.json", ["table"]),
]

# Field families the brief asked for that have no official source at all.
UNRESOLVABLE = {
    "product identity": "3 SKUs × 12 attribute fields = 36 cells",
    "per-category commission": "category rate card (Table 1) is public at the Associates help node (re-verified 2026-11-14); what is unresolvable is each listing's category, so no rate attaches to a product row (FLG-021)",
    "trend / demand rank": "no official Amazon endpoint for affiliates",
    "conversion rate": "not published to affiliates; derivable only from own logs",
    "competition density": "no official Amazon endpoint for affiliates",
    "clicks / orders / revenue": "no campaign live; Amazon reports in-account only",
}


def load(name):
    return json.loads((DATA / name).read_text(encoding="utf-8"))


def report():
    rows, all_srcs, all_flags = [], set(), set()
    for page, label, fname, keys in TABLES:
        d = load(fname)
        tot = src = flagged = anchored = blank = cells = 0
        for k in keys:
            spec = d.get(k) or {}
            for r in spec.get("rows", []):
                tot += 1
                if r.get("sources"):
                    src += 1
                    all_srcs.update(r["sources"])
                if r.get("flags"):
                    flagged += 1
                    all_flags.update(r["flags"])
                if r.get("self_attested"):
                    anchored += 1
                cols = [c["key"] for c in spec.get("columns", [])]
                for c in cols:
                    v = r.get(c)
                    cells += 1
                    if v is None or v == "":
                        blank += 1
            cells += 0
        covered = src + flagged + anchored
        rows.append({
            "page": page, "label": label, "rows": tot, "with_official_source": src,
            "with_flag": flagged, "repo_anchored": anchored,
            "cells": cells, "cells_blank_by_design": blank,
            "coverage_pct": round(100 * min(covered, tot) / tot, 1) if tot else 100.0,
        })
    return rows, all_srcs, all_flags


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--strict", action="store_true")
    a = ap.parse_args()

    rows, srcs, flags = report()
    sources_known = {s["id"] for s in load("sources.json")["sources"]}
    flags_known = {r["id"] for r in load("flags.json")["table"]["rows"]}

    out = {
        "tables": rows,
        "totals": {
            "table_rows": sum(r["rows"] for r in rows),
            "cells": sum(r["cells"] for r in rows),
            "blank_cells": sum(r["cells_blank_by_design"] for r in rows),
            "distinct_sources_cited": len(srcs),
            "distinct_flags_cited": len(flags),
        },
        "integrity": {
            "dangling_source_refs": sorted(srcs - sources_known),
            "dangling_flag_refs": sorted(flags - flags_known),
            "uncited_sources": sorted(sources_known - srcs),
            "unreferenced_flags": sorted(flags_known - flags),
        },
        "unresolvable_field_families": UNRESOLVABLE,
    }
    if a.json:
        print(json.dumps(out, indent=2))
    else:
        print("ZONE3 PROVENANCE COVERAGE\n" + "=" * 96)
        print(f"{'page':<12}{'rows':>6}{'w/ source':>11}{'w/ flag':>9}{'anchored':>10}"
              f"{'cells':>7}{'blank':>7}{'coverage':>10}  label")
        print("-" * 96)
        for r in rows:
            print(f"{r['page']:<12}{r['rows']:>6}{r['with_official_source']:>11}"
                  f"{r['with_flag']:>9}{r['repo_anchored']:>10}{r['cells']:>7}"
                  f"{r['cells_blank_by_design']:>7}{r['coverage_pct']:>9.1f}%  {r['label']}")
        t = out["totals"]
        print("=" * 96)
        print(f"TOTALS  rows={t['table_rows']}  cells={t['cells']}  "
              f"blank-by-design={t['blank_cells']}  sources={t['distinct_sources_cited']}  "
              f"flags={t['distinct_flags_cited']}")
        i = out["integrity"]
        print(f"INTEGRITY  dangling source refs={i['dangling_source_refs'] or 'none'}  "
              f"dangling flag refs={i['dangling_flag_refs'] or 'none'}")
        print(f"           uncited sources={i['uncited_sources'] or 'none'}  "
              f"unreferenced flags={i['unreferenced_flags'] or 'none'}")
        print("\nUNRESOLVABLE FROM ANY OFFICIAL SOURCE (left blank, never estimated):")
        for k, v in UNRESOLVABLE.items():
            print(f"  - {k:<26} {v}")

    bad = [r for r in rows if r["coverage_pct"] < 100]
    dangling = bool(out["integrity"]["dangling_source_refs"] or out["integrity"]["dangling_flag_refs"])
    if a.strict and (bad or dangling):
        print("\nSTRICT FAIL: " + (f"under-covered tables: {[r['page'] for r in bad]} " if bad else "")
              + ("dangling references" if dangling else ""), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
