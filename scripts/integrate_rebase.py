#!/usr/bin/env python3
"""Integration resolver for session 145b8df7's rebase onto a moving `main`.

Same discipline `scripts/resolve_rebase.py` established, with this session's Part marker:

  COORDINATION.md   main's entire board, then this session's Part appended verbatim.
  data/flags.json   union: main's flags in main's order, then this session's new ids.
  data/sources.json union with renumbering: main's register wins any id collision, and this
                    session's S59-S68 entries are renumbered to the first free ids, in order.
                    Every reference to those ids in this session's own files is rewritten by
                    scripts/renumber_sources.py so nothing dangles.
  generated HTML    main's version, then regenerated from the merged data by the project's own
                    builders -- so the committed output is what a builder emits, not a merge.

Marker detection is anchored at line start, because the board's prose quotes the string
"<<<<<<<" while describing this exact hazard.
"""
from __future__ import annotations
import json
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
MARKER = re.compile(r"^(<{7}|>{7})( |$)", re.M)
PART = "# Part: session `145b8df7`"
MINE_NEW = [f"S{n}" for n in range(59, 69)]          # ids this session appended


def git(*a: str) -> str:
    return subprocess.run(["git", "-C", str(ROOT), *a], capture_output=True, text=True, check=True).stdout


def conflicted() -> list[str]:
    return [l for l in git("diff", "--name-only", "--diff-filter=U").splitlines() if l]


def resolve_coordination() -> str:
    base = git("show", ":2:COORDINATION.md")
    mine = git("show", ":3:COORDINATION.md")
    if PART not in mine:
        raise SystemExit("this session's Part is not on the branch side -- refusing to guess")
    part = mine[mine.index(PART):]
    for name, text in (("main side", base), ("this Part", part)):
        if MARKER.search(text):
            raise SystemExit(f"{name} still carries conflict markers")
    out = base.rstrip() + "\n\n" + part
    (ROOT / "COORDINATION.md").write_text(out, encoding="utf-8")
    return f"COORDINATION.md: main's board ({len(base.splitlines())} lines) + this Part ({len(part.splitlines())} lines)"


def _side(stage: int, path: str) -> dict:
    return json.loads(git("show", f":{stage}:{path}"))


def _free_ids(n: int, taken: set[str]) -> list[str]:
    out, k = [], 10 ** 6
    while len(out) < n:
        cand = f"S{k}"
        if cand not in taken:
            out.append(cand)
        k += 1
    return out


def resolve_sources() -> tuple[str, dict]:
    """main wins every id it already holds; this session's ten entries move, in order, to the
    first consecutive ids above main's maximum, and the mapping is returned so every reference
    in this session's own files is rewritten to match. No reference is left pointing at main's
    same-numbered-but-different document."""
    base, mine = _side(2, "data/sources.json"), _side(3, "data/sources.json")
    by_id = {s["id"]: s for s in base["sources"]}
    taken = set(by_id)
    nums = [int(re.sub(r"\D", "", i)) for i in taken if re.sub(r"\D", "", i)]
    nxt = (max(nums) if nums else 0) + 1
    mapping: dict[str, str] = {}
    added = []
    for s in mine["sources"]:
        if s["id"] in MINE_NEW:
            while f"S{nxt}" in taken:
                nxt += 1
            new = f"S{nxt}"
            nxt += 1
            mapping[s["id"]] = new
            s = dict(s, id=new,
                     status_note=s.get("status_note", "") +
                     f" [Id renumbered from {s['id']} on integration onto main, where that id "
                     f"already names a different document.]")
            taken.add(new)
            added.append(s)
        elif s["id"] not in by_id:
            added.append(s)
    for s in added:
        by_id[s["id"]] = s
    order = [x["id"] for x in base["sources"]] + [x["id"] for x in added]
    base["sources"] = [by_id[i] for i in order]
    base["retrieved"] = ("2026-11-16 — union: main's register plus session 145b8df7's dated re-verification "
                         "entries (renumbered where main had already taken an id)")
    (ROOT / "data/sources.json").write_text(json.dumps(base, indent=2, ensure_ascii=False) + "\n",
                                            encoding="utf-8")
    return (f"data/sources.json: main's {len(order) - len(added)} + this session's {len(added)} "
            f"= {len(order)}; renumbered {mapping}"), mapping


def resolve_flags() -> str:
    base, mine = _side(2, "data/flags.json"), _side(3, "data/flags.json")
    have = {f["id"] for f in base["flags"]}
    add = [f for f in mine["flags"] if f["id"] not in have]
    base["flags"].extend(add)
    (ROOT / "data/flags.json").write_text(json.dumps(base, indent=2, ensure_ascii=False) + "\n",
                                          encoding="utf-8")
    return f"data/flags.json: main's {len(base['flags']) - len(add)} + {len(add)} new = {len(base['flags'])}"


def take_main(path: str) -> str:
    (ROOT / path).write_text(git("show", f":2:{path}"), encoding="utf-8")
    return f"{path}: main's version kept (regenerable / another session's scope)"


def take_mine(path: str) -> str:
    raw = git("show", f":3:{path}")
    if MARKER.search(raw):
        raise SystemExit(f"{path}: branch side carries markers")
    (ROOT / path).write_text(raw, encoding="utf-8")
    return f"{path}: this session's new file kept"


def main() -> int:
    files = conflicted()
    if not files:
        print("nothing to resolve")
        return 0
    report, mapping = [], {}
    for f in files:
        if f == "COORDINATION.md":
            report.append(resolve_coordination())
        elif f == "data/sources.json":
            r, mapping = resolve_sources()
            report.append(r)
        elif f == "data/flags.json":
            report.append(resolve_flags())
        elif f.startswith(("read/", "assets/", "data/editorial.json", "data/suggestions.json",
                           "scripts/build_read.py", "scripts/integrate_rebase.py")):
            report.append(take_mine(f))
        elif f.endswith((".html", ".xml")) or f in {
                "scripts/build_site.py", "tools/build_site.py", "scripts/build_marketing.py",
                "data/products.json", "data/policy_facts.json", "data/marketing.json"}:
            report.append(take_main(f))
        elif f in {"EXECUTIVE-SUMMARY.md", "README.md"}:
            report.append(take_main(f) + " — this session's section re-applied after the rebase")
        else:
            report.append(take_main(f))
    if mapping:
        (ROOT / ".git" / "Z14_SOURCE_RENUMBER.json").write_text(json.dumps(mapping, indent=1))
        report.append("renumber map written for scripts/renumber_sources.py: " + json.dumps(mapping))
    print("\n".join(report))
    return 0


if __name__ == "__main__":
    sys.exit(main())
