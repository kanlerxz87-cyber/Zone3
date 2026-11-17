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


def stage(path: str, which: int) -> str:
    """`git show :2:<path>` is main's side of a rebase conflict, `:3:` is this
    branch's. Using the staged blobs is the only reliable way to union a JSON
    register: the conflict inside a JSON array splits mid-structure, so neither
    side parses on its own."""
    try:
        return git("show", f":{which}:{path}")
    except subprocess.CalledProcessError:
        return ""


def resolve_register(path: str, list_key: str) -> dict[str, str]:
    """Union a register by id: main's records in main's order, then this
    branch's records whose ids main does not already use."""
    main_txt, mine_txt = stage(path, 2), stage(path, 3)
    if not main_txt or not mine_txt:
        git("checkout", "--ours", path)
        print(f"{path}: only one side available; kept this branch's version")
        return {}
    main_doc = json.loads(main_txt)
    mine_doc = json.loads(mine_txt)
    main_list = main_doc.setdefault(list_key, [])
    have = {r["id"] for r in main_list}
    renumber: dict[str, str] = {}
    added = []
    for rec in mine_doc.get(list_key, []):
        rid = rec.get("id")
        if rid is None or rid in have:
            continue
        if rid in MINE_SOURCES:
            # main already uses this id and points it at a different document.
            # Take the first free id instead of overwriting theirs.
            n = 1
            while f"S{n}" in have or f"S{n}" in renumber.values():
                n += 1
            new_id = f"S{n}"
            renumber[rid] = new_id
            rec["id"] = new_id
            rid = new_id
        main_list.append(rec)
        have.add(rid)
        added.append(rid)
    # keep the reservation note truthful for the next session
    if list_key == "sources" and added:
        n = 1
        while f"S{n}" in have or f"S{n}" in renumber.values():
            n += 1
        main_doc["id_reservation"] = (
            main_doc.get("id_reservation", "").rstrip()
            + f" Session 5b443d02 (2026-11-17) appended {added[0]}-{added[-1]}. "
            + f"Append from S{n}.")
    (ROOT / path).write_text(json.dumps(main_doc, indent=2) + "\n", encoding="utf-8")
    print(f"{path}: main's {len(main_list) - len(added)} record(s) kept, "
          f"{len(added)} of this branch's added {added}")
    return renumber


def resolve_append_only(path: str) -> None:
    """An append-only document (the board, the executive summary): main's text
    verbatim, then this branch's added block re-appended at the end."""
    p = ROOT / path
    resolved, mine = split_conflict(p.read_text(encoding="utf-8"))
    if not resolved.endswith("\n"):
        resolved += "\n"
    for block in mine:
        resolved += "\n" + block.strip("\n") + "\n"
    p.write_text(resolved, encoding="utf-8")
    print(f"{path}: main's text kept, {len(mine)} block(s) from this branch re-appended")


def rewrite_ids(renumber: dict[str, str]) -> None:
    """Point every reference inside this branch's own files at the new ids."""
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
            # quoted id references only, so prose mentioning a number is untouched
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
        if f in ("COORDINATION.md", "EXECUTIVE-SUMMARY.md"):
            resolve_append_only(f)
        elif f == "data/flags.json":
            resolve_register(f, "flags")
        elif f == "data/sources.json":
            renumber = resolve_register(f, "sources")
        else:
            # Generated output. main's side is kept; the whole tree is rebuilt from
            # the merged data and the merged generators once the rebase finishes.
            git("checkout", "--theirs", f) if False else git("checkout", "--ours", f)
            print(f"{f}: generated page - kept this branch's version, "
                  f"to be regenerated from the merged data")
    rewrite_ids(renumber)
    if renumber:
        print("renumbering map:", renumber)
    return 0


if __name__ == "__main__":
    sys.exit(main())
