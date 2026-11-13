#!/usr/bin/env python3
"""
Zone3 niche scorer.

Turns a set of candidate niches into a ranked list. The weights and the
formula are declared here so a ranking change is auditable in a diff. The
formula is THIS PLATFORM'S choice — it is not an Amazon-supplied score, and the
site labels it as such wherever it appears.

    niche_score = 0.25*commission_index
                + 0.20*demand_index
                + 0.20*review_motiveability
                + 0.15*content_gap
                + 0.10*price_band_fit
                + 0.10*(1 - competition_index)

Hard rule enforced here, and the reason this file matters more than its formula:
a term may only be scored from a sourced value. A missing input does NOT default
to 0 and does NOT get imputed — it yields `insufficient_data`, the candidate is
excluded from the ranking, and the reason is reported. Imputing a neutral score
would silently invent a rank order, which is exactly what the site refuses to
publish.

Inputs come from Creators API-derived features (see data/niches.json). With no
valid ASINs and no API credentials, `--publish` produces an empty ranking, which
is the correct answer, not a failure.

Usage
    python3 tools/niche_score.py --fixture           # exercise the maths, never publish
    python3 tools/niche_score.py --in data/niche-candidates.json --publish data/niches.json
"""
from __future__ import annotations
import argparse, json, pathlib, statistics, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent

WEIGHTS = {
    "commission_index": 0.25,
    "demand_index": 0.20,
    "review_motiveability": 0.20,
    "content_gap": 0.15,
    "price_band_fit": 0.10,
    "competition_index": 0.10,   # inverted: lower competition is better
}
INVERTED = {"competition_index"}
REQUIRED = set(WEIGHTS)


def zscores(vals):
    """Population z-score. Returns {} if the column is degenerate or incomplete."""
    clean = [v for v in vals if isinstance(v, (int, float))]
    if len(clean) < 2:
        return {}
    mu = statistics.fmean(clean)
    sd = statistics.pstdev(clean)
    if sd == 0:
        return {v: 0.0 for v in clean}
    return {v: (v - mu) / sd for v in clean}


def score(candidates):
    """candidates: [{niche, commission_index, demand_index, ...}]

    Returns (ranked, excluded). `excluded` carries the precise missing inputs.
    """
    complete, excluded = [], []
    for c in candidates:
        missing = sorted(k for k in REQUIRED if not isinstance(c.get(k), (int, float)))
        if missing:
            excluded.append({"niche": c.get("niche"), "status": "insufficient_data",
                             "missing_inputs": missing,
                             "note": "not scored; no neutral default was substituted"})
        else:
            complete.append(c)

    ranked = []
    if len(complete) >= 2:
        tables = {k: zscores([c[k] for c in complete]) for k in REQUIRED}
        for c in complete:
            total, terms = 0.0, {}
            for k, w in WEIGHTS.items():
                z = tables[k].get(c[k])
                if z is None:
                    continue
                if k in INVERTED:
                    z = -z
                terms[k] = round(w * z, 4)
                total += w * z
            ranked.append({"niche": c["niche"], "niche_score": round(total, 4),
                           "terms": terms, "status": "scored"})
    elif complete:
        ranked = [{"niche": c["niche"], "niche_score": None, "status": "not_ranked",
                   "note": "a single candidate cannot be z-scored; ranking needs >=2"}
                  for c in complete]

    ranked.sort(key=lambda r: (r["niche_score"] is None, -(r["niche_score"] or 0)))
    # A tie must be reported as a tie. Assigning rank 1 to one of two equal scores
    # would fabricate a preference the inputs do not support.
    EPS = 1e-9
    prev_score, prev_rank = None, 0
    for i, r in enumerate(ranked, 1):
        sc = r.get("niche_score")
        if sc is None:
            continue
        if prev_score is not None and abs(sc - prev_score) < EPS:
            r["rank"] = prev_rank          # equal score -> equal rank
            r["tied_with_above"] = True
        else:
            r["rank"] = i
            prev_rank = i
        prev_score = sc
    n_ranked = sum(1 for r in ranked if r.get("niche_score") is not None)
    if n_ranked >= 2 and len({r["niche_score"] for r in ranked
                             if r.get("niche_score") is not None}) == 1:
        for r in ranked:
            r["note"] = ("all scored candidates are tied at the same value; a tie is not a "
                         "ranking and no order is implied")
    return ranked, excluded


# Synthetic values. Exists only to prove the arithmetic and the exclusion rule.
# Never written to any published page; tools/build_site.py does not read it.
FIXTURE = [
    {"niche": "fixture-alpha", "commission_index": 1.4, "demand_index": 0.8,
     "review_motiveability": 0.5, "content_gap": 1.1, "price_band_fit": 0.6,
     "competition_index": 0.2},
    {"niche": "fixture-beta", "commission_index": 0.2, "demand_index": 1.3,
     "review_motiveability": 1.0, "content_gap": 0.3, "price_band_fit": 1.2,
     "competition_index": 1.6},
    {"niche": "fixture-gamma-partial", "commission_index": 0.9, "demand_index": 0.4,
     "review_motiveability": 0.7},           # three inputs absent on purpose
]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="infile", help="JSON array of candidate dicts")
    ap.add_argument("--fixture", action="store_true")
    ap.add_argument("--publish", metavar="PATH", help="write the ranking table JSON")
    a = ap.parse_args()

    if a.fixture:
        cands = FIXTURE
    elif a.infile:
        cands = json.loads((ROOT / a.infile).read_text() if not pathlib.Path(a.infile).is_absolute()
                           else pathlib.Path(a.infile).read_text())
    else:
        cand_path = ROOT / "data" / "niche-candidates.json"
        cands = json.loads(cand_path.read_text()) if cand_path.exists() else []

    ranked, excluded = score(cands)
    out = {"ranked": ranked, "excluded": excluded, "weights": WEIGHTS,
           "formula": "declared in tools/niche_score.py; platform-defined, not Amazon-supplied",
           "note": ("An empty ranking is the correct output when inputs are unavailable. "
                    "Missing inputs are never imputed with a neutral value.")}
    text = json.dumps(out, indent=2) + "\n"
    if a.publish:
        p = ROOT / a.publish if not pathlib.Path(a.publish).is_absolute() else pathlib.Path(a.publish)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")
        print(f"wrote {p.relative_to(ROOT)}")
    print(text)
    if not ranked and cands:
        print(f"\n{len(excluded)} candidate(s) excluded for insufficient data.", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
