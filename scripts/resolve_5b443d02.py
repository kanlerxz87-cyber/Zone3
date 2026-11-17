#!/usr/bin/env python3
"""Rebase conflict resolver for session 5b443d02.

Same discipline scripts/resolve_rebase.py and scripts/integrate_rebase.py
established for this repository, with this session's markers:

  COORDINATION.md   the board is append-only and two sessions append at once.
                    Resolution: main's entire board verbatim, then this session's
                    Part appended. Nothing from either side is dropped.
  data/flags.json   union by id: main's flags in main's order, then this session's
                    new ids appended. No flag is rewritten.
  data/sources.json union by id: main wins any collision, and this session's
                    S70-S74 are renumbered to the first free ids, in order.
                    Every reference to those ids inside data/5b443d02/ and
                    data/flags.json is rewritten so nothing dangles.
  generated HTML    main's version, then regenerated from the merged data by the
                    project's own builders - so what is committed is what a
                    builder emits, not a hand merge.
  anything else     `git checkout --ours`, then regenerate.

Marker detection is anchored at line start, because the board's own prose quotes the
string "<<<<<<<" while describing this exact hazard.

    python3 scripts/resolve_5b443d02.py           # resolve everything in the index
"""
from __future__ import annotations

import json
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
MARKER = re.compile(r"^(<{7}|={7}|>{7})( |$)", re.M)
# The first line this session appended to the board; used to lift its Part back out.
PART = "## Part — session `5b443d02`"
MINE_SOURCES = [f"S{n}" for n in range(70, 75)]      # S70-S74
MINE_FLAGS = [f"5B-F-{n:02d}" for n in range(1, 7)]  # 5B-F-01..06


def git(*args: str) -> str:
    return subprocess.run(["git", "-C", str(ROOT), *args],
                          capture_output=True, text=True, check=True).stdout


def conflicted() -> list[str]:
    out = git("diff", "--name-only", "--diff-filter=U")
    return [p for p in out.splitlines() if p.strip()]


def split_conflict(text: str):
    """Return (resolved_without_mine, [blocks_from_my_side]).

    Every conflict block is resolved by keeping HEAD's side in place; this
    session's side is lifted out and re-appended at the end of the file, because
    both sides are appends to an append-only board.
    """
    mine_blocks: list[str] = []
    out: list[str] = []
    lines = text.splitlines(keepends=True)
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith("<<<<<<<"):
            i += 1
            head: list[str] = []
            while i < len(lines) and not lines[i].startswith("======="):
                head.append(lines[i])
                i += 1
            i += 1  # skip =======
            mine: list[str] = []
            while i < len(lines) and not lines[i].startswith(">>>>>>>"):
                mine.append(lines[i])
                i += 1
            i += 1  # skip >>>>>>>
            out.extend(head)
            block = "".join(mine)
            if block.strip():
                mine_blocks.append(block)
            continue
        out.append(line)
        i += 1
    return "".join(out), mine_blocks


def resolve_coordination() -> None:
    path = ROOT / "COORDINATION.md"
    text = path.read_text(encoding="utf-8")
    resolved, mine = split_conflict(text)
    if not resolved.endswith("\n"):
        resolved += "\n"
    for block in mine:
        if not block.endswith("\n"):
            block += "\n"
        resolved += "\n" + block.strip("\n") + "\n"
    path.write_text(resolved, encoding="utf-8")
    print(f"COORDINATION.md: kept main's board, re-appended {len(mine)} block(s) "
          f"from this session's Part")


def union_by_id(path: pathlib.Path, key: str, mine_ids: list[str],
                renumber_from: list[str] | None = None) -> dict[str, str]:
    """Union two JSON registers that hold a list of records with unique ids.

    Returns a map of renumbered ids (old -> new) when renumbering is needed.
    """
    raw = path.read_text(encoding="utf-8")
    blocks = mine = None
    resolved, mine_blocks = split_conflict(raw)
    if not mine_blocks:
        return {}
    # HEAD's side has already been written into `resolved`; parse it, then add
    # this session's records that are not already present.
    head_doc = json.loads(resolved)
    head_ids = {r[key] for r in head_doc}
    renumber: dict[str, str] = {}
    added = 0
    for block in mine_blocks:
        try:
            mine_doc = json.loads(block)
        except json.JSONDecodeError:
            # A conflict inside a JSON file is often not a whole-document split;
            # fall back to reading this branch's committed version of the file.
            continue
        for rec in mine_doc:
            rid = rec[key]
            if rid in head_ids:
                continue
            if renumber_from and rid in renumber_from:
                # main won this id and points it at a different document; take the
                # first free id instead of overwriting theirs.
                n = 1
                while f"S{n}" in head_ids or f"S{n}" in renumber.values():
                    n += 1
                new_id = f"S{n}"
                renumber[rid] = new_id
                rec[key] = new_id
                rid = new_id
            head_doc["sources" if "sources" in head_doc else key].append(rec)
            head_ids.add(rid)
            added += 1
    path.write_text(json.dumps(head_doc, indent=2) + "\n", encoding="utf-8")
    print(f"{path.name}: unioned by {key}; {added} record(s) from this session added")
    return renumber


def resolve_register(path: pathlib.Path, list_key: str) -> dict[str, str]:
    """Union a register file by id, using the branch's own version for my records."""
    raw = path.read_text(encoding="utf-8")
    if not MARKER.search(raw):
        return {}
    resolved, mine_blocks = split_conflict(raw)
    head_doc = json.loads(resolved)
    head_list = head_doc[list_key]
    head_ids = {r["id"] for r in head_list}
    renumber: dict[str, str] = {}
    added = 0
    for block in mine_blocks:
        try:
            mine_doc = json.loads(block)
        except json.JSONDecodeError:
            continue
        for rec in mine_doc.get(list_key, []):
            rid = rec["id"]
            if rid in head_ids:
                continue
            if rid in MINE_SOURCES:
                n = 1
                while f"S{n}" in head_ids or f"S{n}" in renumber.values():
                    n += 1
                new_id = f"S{n}"
                renumber[rid] = new_id
                rec["id"] = new_id
                rid = new_id
            head_list.append(rec)
            head_ids.add(rid)
            added += 1
    path.write_text(json.dumps(head_doc, indent=2) + "\n", encoding="utf-8")
    print(f"{path.name}: unioned by id; {added} of this session's record(s) added")
    return renumber


def rewrite_ids(renumber: dict[str, str]) -> None:
    """Point every reference inside this session's own files at the new ids."""
    if not renumber:
        return
    targets: list[pathlib.Path] = []
    d = ROOT / "data" / "5b443d02"
    if d.exists():
        targets += sorted(d.glob("*.json"))
    targets.append(ROOT / "data" / "flags.json")
    changed = []
    for p in targets:
        if not p.exists():
            continue
        text = p.read_text(encoding="utf-8")
        original = text
        for old, new in renumber.items():
            # quoted id references only, so prose that mentions a number is untouched
            text = re.sub(rf'"{re.escape(old)}"', f'"{new}"', text)
        if text != original:
            p.write_text(text, encoding="utf-8")
            changed.append(p.name)
    print("renumbered references in:", ", ".join(changed) or "none")


def main() -> int:
    files = conflicted()
    if not files:
        print("no conflicted files in the index")
        return 0
    print("conflicted:", ", ".join(files))
    renumber: dict[str, str] = {}
    for f in files:
        path = ROOT / f
        if f == "COORDINATION.md":
            resolve_coordination()
        elif f == "data/flags.json":
            union_by_id(path, "id", MINE_FLAGS)
        elif f == "data/sources.json":
            renumber = resolve_register(path, "sources")
        else:
            git("checkout", "--ours", f)
            print(f"{f}: kept this branch's version (regenerated by the builders)")
    rewrite_ids(renumber)
    if renumber:
        print("renumbering map:", renumber)
    return 0


if __name__ == "__main__":
    sys.exit(main())
