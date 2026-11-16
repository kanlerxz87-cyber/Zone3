#!/usr/bin/env python3
"""AB-F-01 (session ab3ed329, 2026-11-16): remove observed Amazon price, rating,
review-count and sales literals from PUBLIC registers.

Basis: Associates Program Policies, Participation Requirements 2(b) (prices and
availability may be shown only via a Special Link Amazon serves, or Creators API /
PA API data) and 6(t) (customer reviews and star ratings may not be displayed unless
obtained through Creators API / PA API). The registers are served by GitHub Pages,
so the literals were publicly visible.

What it does (idempotent):
  1. data/products.json  observed_2026_11_14.{price, other_offers, rating,
                         review_count, sales_note} -> null, with a note.
  2. data/sources.json   S46-S48 status_note -> wording without values.
  3. data/flags.json and data/z3/flags.json: product price / rating / count
                         literals inside flag text -> "[... withheld]".
It does NOT touch commission rates or bounty amounts (permitted official data).
It prints every replacement so the change can be reviewed.
"""
import json, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
PRICE = r"79\.93|149\.99|79\.91|69\.97|99\.99|209\.99|119\.99|57\.45|92\.99|49\.54"
RATING = r"4\.2 out of 5(?: stars?)?|4\.3 out of 5(?: stars?)?|4\.4 out of 5(?: stars?)?"
COUNT = r"\(4\.8K\)|\(18\.3K\)|\(16\.8K\)|\b1K\+ bought|\b4K\+ bought|\b3K\+ bought"
PRICE_RE = re.compile(r"\$?(?<![\d.])(?:" + PRICE + r")(?!\d)")
RATING_RE = re.compile(r"(?:" + RATING + r")")
COUNT_RE = re.compile(r"(?:" + COUNT + r")")
LOG = []

def scrub_text(s, where):
    if not isinstance(s, str):
        return s
    out = s
    for rx, label in ((RATING_RE, "[rating withheld]"), (COUNT_RE, "[count withheld]"),
                      (PRICE_RE, "[price withheld]")):
        def rep(m, label=label):
            LOG.append((where, m.group(0), label))
            return label
        out = rx.sub(rep, out)
    return out

def walk_scrub(o, where):
    if isinstance(o, dict):
        return {k: walk_scrub(v, f"{where}.{k}") for k, v in o.items()}
    if isinstance(o, list):
        return [walk_scrub(v, f"{where}[{i}]") for i, v in enumerate(o)]
    return scrub_text(o, where)

NOTE_ADD = (" AB-F-01 (2026-11-16, session ab3ed329): the observed price, other-offer, rating, "
            "review-count and sales-note values were removed from this public file under Program "
            "Policies 2(b) and 6(t). The dated observation is in git history; no value is displayed.")

def main():
    # 1. products.json
    p = ROOT / "data/products.json"
    d = json.loads(p.read_text())
    for prod in d["products"]:
        obs = prod.get("observed_2026_11_14")
        if isinstance(obs, dict):
            for k in ("price", "other_offers", "rating", "review_count", "sales_note"):
                if obs.get(k) is not None:
                    LOG.append(("products.json", f"{prod['id']}.{k}", "null"))
                    obs[k] = None
            if NOTE_ADD.strip() not in obs.get("note", ""):
                obs["note"] = obs.get("note", "") + NOTE_ADD
    p.write_text(json.dumps(d, indent=2, ensure_ascii=False) + "\n")

    # 2. sources.json S46-S48
    p = ROOT / "data/sources.json"
    d = json.loads(p.read_text())
    for s in d["sources"]:
        if s.get("id") in ("S46", "S47", "S48"):
            pid = s["url"].split("k=")[-1]
            new = (f"Fetched 2026-11-14 (observed). Price, rating, review-count and sales values for "
                   f"{pid} are withheld from this public register under Program Policies 2(b) and 6(t) "
                   f"(AB-F-01; FLG-023). The page URL is the source.")
            if s.get("status_note") != new:
                LOG.append(("sources.json", s["id"] + ".status_note", "reworded"))
                s["status_note"] = new
    p.write_text(json.dumps(d, indent=2, ensure_ascii=False) + "\n")

    # 3. flag registers
    for rel in ("data/flags.json", "data/z3/flags.json"):
        p = ROOT / rel
        raw = json.loads(p.read_text())
        new = walk_scrub(raw, rel)
        p.write_text(json.dumps(new, indent=2, ensure_ascii=False) + "\n")

    for where, val, label in LOG:
        print(f"{where}: {val!r} -> {label}")
    print(f"replacements: {len(LOG)}")

if __name__ == "__main__":
    sys.exit(main())
