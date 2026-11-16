#!/usr/bin/env python3
"""Post-build integrator for the reader site (session cba81fa5, 2026-11-16).

Why this exists. The reader site under site/ is emitted by tools/build_i2_site.py (session
59d84c55). Two of those surfaces — the landing page and the buying-guides index — list guides
that this session published, and a plain rebuild of the reader site would silently drop them.
Rather than fork their generator, this script owns exactly two regions and regenerates them
from data/cba81fa5/guides.json, so the guide list is data-driven and a rebuild is repairable:

    python3 tools/build_i2_site.py && python3 tools/build_cba81fa5_site.py && python3 scripts/build_sitemap.py

Regions owned (replaced wholesale, everything else in the file is untouched):
  site/index.html          from "<h2>Buying guides</h2>" up to the "<h2>Side by side</h2>" anchor
  site/guides/index.html   from "<h2>The guide plan</h2>" up to "<h2>The rule every guide follows</h2>"
  site/site-index.json     every guide href in the register, plus the governance pages

Usage:  python3 tools/build_cba81fa5_site.py [--check]
        --check  exits 1 (and prints the diff size) if a rebuild would change anything.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
DATA = ROOT / "data" / "cba81fa5"

GUIDES = json.loads((DATA / "guides.json").read_text(encoding="utf-8"))
SOURCES = json.loads((DATA / "sources.json").read_text(encoding="utf-8"))
SRC = {s["id"]: s for s in SOURCES["sources"]}
for s in json.loads((ROOT / "data" / "i2" / "sources.json").read_text(encoding="utf-8")).get("sources", []):
    SRC.setdefault(s["id"], s)


def src_tag(sid: str) -> str:
    s = SRC.get(sid)
    if not s:
        return f'<span class="mono">{sid}</span>'
    return (f'<a class="src" href="{s["url"]}" target="_blank" rel="noopener noreferrer" '
            f'title="{s.get("title", s["url"])}">{sid}</a>')


def src_row(ids) -> str:
    return " ".join(src_tag(i) for i in ids)


def landing_block() -> str:
    live = [g for g in GUIDES["guides"] if g["status"] == "live"]
    cards = "\n".join(
        f'  <a class="card" href="{g["href"]}"><b>{g["title"].split(":")[0] if len(g["title"]) > 46 else g["title"]}</b>'
        f'<span>{g["blurb"]}</span></a>'
        for g in live
    )
    snap = GUIDES["category_snapshot"]
    return (
        f'<h2>{GUIDES["landing_heading"]}</h2>\n'
        f'<p>{GUIDES["landing_intro"]}</p>\n'
        f'<div class="cards">\n{cards}\n'
        f'  <a class="card" href="guides/index.html"><b>All guides</b><span>The plan, what is live, and what stays unpublished and why.</span></a>\n'
        f'</div>\n\n'
        f'<h2>{snap["heading"]}</h2>\n'
        f'<p>{snap["body"]}\n{src_row(snap["sources"])}</p>\n\n'
    )


def note_and_rules(n_live: int, n_held: int) -> str:
    rules = "\n".join(f"  <li>{r}</li>" for r in GUIDES["rules"])
    return (
        f'<div class="note">\n  <h3>Why {n_live} {word(n_live)} live and {n_held} do not</h3>\n'
        '  <p>A guide goes live once every sentence in it traces to a listing or an official page, the house lint '
        'passes, and each source link has been re-read the same day. The {held} rows are held because the question '
        'needs either a number the listings do not state or a test nobody has run; a row marked &ldquo;will not '
        'publish&rdquo; is a topic this site is not permitted to write, and it stays listed here rather than being '
        'quietly dropped. Every page carries its reviewer note: an agent research desk, no human editor yet '
        '(question Q-5 on the <a href="../answers.html">open-questions register</a>, decision D-10 on the '
        '<a href="../decisions.html">board</a>).</p>\n</div>\n'
        '<h2>The rule every guide follows</h2>\n'
        f'<p class="small">{GUIDES["rules_intro"]}</p>\n'
        f'<ul>\n{rules}\n</ul>\n\n'
    )


def word(n: int) -> str:
    return "guide is" if n == 1 else "guides are"


def guides_index_block() -> str:
    gs = GUIDES["guides"]
    n_live = sum(1 for g in gs if g["status"] == "live")
    n_held = len(gs) - n_live
    rows = []
    for g in gs:
        if g["status"] == "live":
            rows.append(
                f'<tr><td class="lead-cell"><a href="{g["href"].split("/")[-1]}">{g["title"]}</a></td>'
                f'<td><span class="badge b-ok">Live</span> <span class="small">{g["published"]}</span></td>'
                f'<td>{src_row(g["sources"])}</td></tr>'
            )
        else:
            label = "Held" if g["status"] == "held" else "Will not publish"
            rows.append(
                f'<tr><td class="lead-cell">{g["title"]}</td>'
                f'<td><span class="badge b-mute">{label}</span></td>'
                f'<td><span class="blank"><span class="blank-dot"></span>{label}</span>'
                f'<span class="blank-why">{g["reason"]}</span></td></tr>'
            )
    tail = note_and_rules(n_live, n_held).format(held="Held" if n_held else "no")
    return (
        '<div class="tablewrap"><table>\n<caption>The guide plan</caption>\n'
        '<div class="tablewrap"><table><caption>Every guide, published or not, with the register it was read from</caption>'
        '<thead><tr><th>Question this guide answers</th><th>Status</th><th>Provenance</th></tr></thead>'
        f'<tbody>{"".join(rows)}</tbody></table></div>\n' + tail
    )


def patch(path: pathlib.Path, start: str, end: str, new: str, back: str | None = None) -> str:
    t = path.read_text(encoding="utf-8")
    i, j = t.find(start), t.find(end)
    if back and i > 0:
        k = t.rfind(back, 0, i)
        if k > 0:
            i = k
    if i < 0 or j < 0 or j <= i:
        raise SystemExit(f"FAIL: anchors {start!r} / {end!r} not both found in {path.name}")
    return t[:i] + new + t[j:]


def build_index_json() -> str:
    idx_path = SITE / "site-index.json"
    data = json.loads(idx_path.read_text(encoding="utf-8")) if idx_path.exists() else {"pages": []}
    want = set(data.get("pages", []))
    for g in GUIDES["guides"]:
        if g["href"]:
            want.add(g["href"])
    for extra in ("answers.html", "style-guide.html"):
        if (SITE / extra).exists():
            want.add(extra)
    data["pages"] = sorted(want)
    data["built"] = GUIDES["built"]
    return json.dumps(data, indent=1) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()

    targets = [
        (SITE / "index.html", "<h2>Buying guides</h2>", "<h2>Side by side</h2>", landing_block(), None),
        (SITE / "guides" / "index.html", "<caption>The guide plan</caption>", "</main>",
         guides_index_block(), '<div class="tablewrap">'),
    ]
    changed = []
    for path, start, end, new, back in targets:
        want = patch(path, start, end, new, back)
        have = path.read_text(encoding="utf-8")
        if want != have:
            changed.append(path.relative_to(ROOT).as_posix())
            if not a.check:
                path.write_text(want, encoding="utf-8")

    idx_path = SITE / "site-index.json"
    want_idx = build_index_json()
    if idx_path.read_text(encoding="utf-8") != want_idx:
        changed.append("site/site-index.json")
        if not a.check:
            idx_path.write_text(want_idx, encoding="utf-8")

    if a.check and changed:
        print("STALE: rebuild needed -> " + ", ".join(changed), file=sys.stderr)
        return 1
    print(("WOULD REWRITE " if a.check else "WROTE ") + (", ".join(changed) or "nothing (already current)"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
