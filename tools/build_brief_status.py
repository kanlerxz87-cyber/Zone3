#!/usr/bin/env python3
"""Build brief-status/index.html from data/shop/brief-status.json (build 38650305).

Every row shows two columns that are never merged: what the brief claims, and what this checkout
shows. A row whose status is not in the vocabulary, or whose flag ID is not in data/shop/flags.json,
fails the build.

    python3 tools/build_brief_status.py           # write the page
    python3 tools/build_brief_status.py --check   # exit 1 if the page is stale or the register is invalid
"""
from __future__ import annotations

import html
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
REG = ROOT / "data" / "shop" / "brief-status.json"
FLAGS = ROOT / "data" / "shop" / "flags.json"
PAGE = ROOT / "brief-status" / "index.html"


def _load_mod(rel_path: str, name: str):
    import importlib.util
    spec = importlib.util.spec_from_file_location(name, ROOT / rel_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def postprocess(text: str, rel: str) -> str:
    """Apply the same post-passes the chain runs on every page, in memory, so --check is exact."""
    pp = _load_mod("sessions/aebf0747/publish_pass.py", "publish_pass_38")
    mp = _load_mod("tools/measure_pass.py", "measure_pass_38")
    existing = {p.relative_to(ROOT).as_posix() for p in ROOT.rglob("*") if p.is_file()}
    text, _ = pp.apply(text, rel, existing)
    return mp.apply(text, rel)
CANON = "https://kanlerxz87-cyber.github.io/Zone3/brief-status/"
CLASS = {
    "Verified here": "ok",
    "Partly here": "warn",
    "Not found here": "warn",
    "Conflict": "bad",
    "Blocked (owner)": "bad",
    "Not measured": "muted",
}


def load() -> tuple[dict, list[str]]:
    reg = json.loads(REG.read_text(encoding="utf-8"))
    flag_ids = {f["id"] for f in json.loads(FLAGS.read_text(encoding="utf-8"))["flags"]}
    errors = []
    vocab = set(reg["_meta"]["status_vocabulary"])
    for row in reg["rows"]:
        if row["our_status"] not in vocab:
            errors.append(f"{row['id']}: status '{row['our_status']}' not in vocabulary")
        if row["flag"] and row["flag"] not in flag_ids:
            errors.append(f"{row['id']}: flag {row['flag']} not in flags.json")
    return reg, errors


def cell_link(url: str) -> str:
    if not url:
        return "<span class=\"muted\">none given in the brief</span>"
    return f'<a href="{html.escape(url)}" rel="noopener">{html.escape(url)}</a>'


def page(reg: dict) -> str:
    rows = []
    counts: dict[str, int] = {}
    for r in reg["rows"]:
        counts[r["our_status"]] = counts.get(r["our_status"], 0) + 1
        flag = (f'<a href="../shop/flagged/index.html">{html.escape(r["flag"])}</a>'
                if r["flag"] else "—")
        rows.append(
            "<tr>"
            f"<td><strong>{html.escape(r['id'])}</strong><br><span class=\"muted\">{html.escape(r['priority'])}</span></td>"
            f"<td>{html.escape(r['item'])}</td>"
            f"<td>{html.escape(r['brief_says'])}</td>"
            f"<td>{html.escape(r['this_repo_shows'])}</td>"
            f"<td><span class=\"st st-{CLASS.get(r['our_status'], 'muted')}\">{html.escape(r['our_status'])}</span></td>"
            f"<td>{flag}</td>"
            f"<td class=\"src\">{cell_link(r['brief_link'])}</td>"
            "</tr>"
        )
    summary = " · ".join(f"{html.escape(k)} {v}" for k, v in counts.items())
    vocab = "".join(
        f"<li><strong>{html.escape(k)}</strong> — {html.escape(v)}</li>"
        for k, v in reg["_meta"]["status_vocabulary"].items()
    )
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Brief status — what the brief claims, and what this site shows</title>
<meta name="description" content="Each row of the brief (S-04 to S-25, SG-27 to SG-30) next to what this repository shows, measured on 2026-11-17, with the flag for any gap.">
<link rel="canonical" href="{CANON}">
<link rel="stylesheet" href="../assets/zone3-publication.css">
<style>
.st{{font-weight:600;white-space:nowrap}}
.st-ok{{color:#14532d}} .st-warn{{color:#92400e}} .st-bad{{color:#991b1b}} .st-muted{{color:#475569}}
.reg td{{vertical-align:top}}
.reg .src{{word-break:break-all;font-size:.85em}}
</style>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="masthead">
  <div class="wrap masthead-row">
    <a class="brand" href="../index.html">Zone3 Kitchen (working name)</a>
    <span class="tagline">Brief status</span>
  </div>
</header>
<main id="main" class="wrap">
<p class="eyebrow">Re-measured 2026-11-19 (session 8aa259bb, branch arena/8aa259bb-zone3) · first measured 2026-11-17 (branch arena/38650305-zone3)</p>
<h1>The brief's rows, next to what this site shows</h1>
<p class="lede">The brief lists status labels for S-04 to S-25 and names SG-27 to SG-30. Several of those labels cannot be matched to anything in this repository. This page keeps the two columns apart: what the brief says, and what was measured here. It does not copy one into the other.</p>
<p><strong>Counts:</strong> {summary}</p>

<h2>How to read the statuses</h2>
<ul>{vocab}</ul>

<h2>Register</h2>
<div class="table-wrap"><table class="data reg">
<thead><tr>
<th scope="col">Row</th><th scope="col">Brief item</th><th scope="col">Brief says</th><th scope="col">This repo shows</th><th scope="col">Our status</th><th scope="col">Flag</th><th scope="col">Link from the brief</th>
</tr></thead>
<tbody>{"".join(rows)}</tbody>
</table></div>

<h2>Limits of this page</h2>
<ul>
<li>The brief's labels cite the owner's Zone4 decision log. On 2026-11-19 each cited D-number was checked against its recorded or open status in the public Zone4 repository (main). The 'Brief says' column is still quoted, not independently verified, and the Zone4 log is not an official source.</li>
<li>Some links in the last column are the brief's own, and point to the Zone4 repository or to a page that is not an official source for the row. They are shown as given, not as verification.</li>
<li>Nothing on this page changes the site. The owner decides which open rows to act on; see the <a href="../shop/flagged/index.html">flagged list</a>.</li>
</ul>
<p class="muted">Generated by <code>tools/build_brief_status.py</code> from <code>data/shop/brief-status.json</code>.</p>
</main>
</body>
</html>
"""


def main() -> int:
    reg, errors = load()
    if errors:
        print("REGISTER INVALID:\n  " + "\n  ".join(errors))
        return 1
    text = postprocess(page(reg), "brief-status/index.html")
    current = PAGE.read_text(encoding="utf-8") if PAGE.exists() else None
    if "--check" in sys.argv:
        if current != text:
            print("STALE: brief-status/index.html")
            return 1
        print(f"brief status current · {len(reg['rows'])} rows")
        return 0
    PAGE.parent.mkdir(parents=True, exist_ok=True)
    if current != text:
        PAGE.write_text(text, encoding="utf-8")
        print("wrote brief-status/index.html")
    else:
        print("no changes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
