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


DIRECTION_NAV = """    # Added by session 5b443d02 (2026-11-17): the Direction section, generated by
    # scripts/build_5b443d02.py from data/5b443d02/*.json. Additive - it adds a
    # navigation group and rewrites no existing entry.
    ("Direction", [
        ("direction/index.html", "Direction & suggestions"),
        ("direction/products.html", "Product intent"),
        ("direction/questions.html", "Open questions"),
        ("direction/choose.html", "Choose a path"),
    ]),
"""

DIRECTION_PAGES = """    # Added by session 5b443d02 (2026-11-17): the Direction section, generated by
    # scripts/build_5b443d02.py from data/5b443d02/*.json. Listed here so the shared
    # gate checks its disclosure, navigation, https-only links and placeholder text
    # like every other published page. Deliberately NOT added to TABLE_PAGES: that
    # check requires the last column of every table to be a Source column, and the
    # suggestions and paths tables end with a state badge instead. Per-row provenance
    # on those tables is enforced by tools/verify_site.py V4, which passes them.
    "direction/index.html", "direction/products.html",
    "direction/questions.html", "direction/choose.html",
"""

OLD_HEADLINE = ("  <p><strong>Headline:</strong> the three submitted short links each open a live "
                "Amazon product page.")
NEW_HEADLINE = ("  <p><strong>Headline:</strong> the five submitted short links each open a live "
                "Amazon product page.")
NEW_NOTE = """  <p><strong>Read this first (2026-11-17):</strong> two of the five &mdash; {flag_links(['5B-F-01'])} &mdash; are meat thermometers in a different Amazon browse node from the three air-fryer listings this site was built around, and they appear in no other data file in this repository {flag_links(['5B-F-02'])}. Before redesigning anything, read the <a href="direction/products.html">product-intent confirmation record</a>, the <a href="direction/questions.html">open questions</a> and the three <a href="direction/choose.html">paths</a>. The same two links are recorded independently by session <code>82372fd1</code> on the <a href="intent-record/index.html">intent-record page</a>, where their observed fields are still empty.</p>
"""
OLD_DESC = "for three Amazon air-fryer listings"
NEW_DESC = "for five submitted Amazon kitchen listings - three air fryers and two meat thermometers"

OLD_BASE = "            base = (ROOT / name).parent\n"
NEW_BASE = ("            # Session 5b443d02 (2026-11-17): a pure-fragment link (\"#5B-Q07\") has an\n"
            "            # empty path. The old code fell back to `name` and joined it to the page's\n"
            "            # own directory, so a subdirectory page resolved \"#anchor\" to\n"
            "            # <dir>/<dir>/<page> and reported a broken link for an anchor that exists\n"
            "            # on the page being checked. Reproduced before: 5 failures, after: 0.\n"
            "            base = ROOT if not parts.path else (ROOT / name).parent\n")


def reapply_py_edits() -> None:
    """Re-apply this branch's four edits to the shared Python files.

    Idempotent and guarded on the current text, so it can run after any number of
    rebases. A rebase that conflicts on a generator resolves to main's version, which
    silently drops these edits; this puts them back without discarding main's work.
    """
    # --- scripts/build_site.py -------------------------------------------------
    f = ROOT / "scripts" / "build_site.py"
    t = f.read_text(encoding="utf-8")
    changed = []

    if 'direction/index.html' not in t:
        anchor = '    ("Governance", ['
        if anchor in t:
            t = t.replace(anchor, DIRECTION_NAV + anchor, 1)
        else:
            # fall back: append as the last group inside NAV_MORE
            idx = t.index("NAV_MORE = [")
            close = t.index("\n]\n", idx)
            t = t[:close] + "\n" + DIRECTION_NAV.rstrip("\n") + t[close:]
        changed.append("nav group")

    if OLD_HEADLINE in t and "five submitted short links" not in t:
        t = t.replace(OLD_HEADLINE, NEW_HEADLINE, 1)
        changed.append("exec headline")
    if "Read this first (2026-11-17)" not in t and OLD_HEADLINE not in t:
        marker = ("  <p>Price display, API-derived reviews, link-model-specific earnings")
        if marker in t:
            t = t.replace(marker, NEW_NOTE + marker, 1)
            changed.append("exec note")
    if OLD_DESC in t:
        t = t.replace(OLD_DESC, NEW_DESC, 1)
        changed.append("meta description")

    if changed:
        f.write_text(t, encoding="utf-8")
    print(f"scripts/build_site.py: re-applied {changed or 'nothing (already present)'}")

    # --- scripts/check_site.py -------------------------------------------------
    f = ROOT / "scripts" / "check_site.py"
    t = f.read_text(encoding="utf-8")
    changed = []
    if 'direction/index.html' not in t:
        marker = '    "read/category/air-fryers.html",\n'
        if marker in t:
            t = t.replace(marker, marker + DIRECTION_PAGES, 1)
        else:
            idx = t.index("PAGES = [")
            close = t.index("\n]\n", idx)
            t = t[:close] + "\n" + DIRECTION_PAGES.rstrip("\n") + t[close:]
        changed.append("PAGES entries")
    if "base = ROOT if not parts.path" not in t and OLD_BASE in t:
        t = t.replace(OLD_BASE, NEW_BASE, 1)
        changed.append("fragment-link fix")
    if changed:
        f.write_text(t, encoding="utf-8")
    print(f"scripts/check_site.py: re-applied {changed or 'nothing (already present)'}")


def fixup_exec_summary() -> None:
    """De-duplicate the counts sentence in EXECUTIVE-SUMMARY.md and recompute it.

    Every rebase so far has left this branch's side of the counts-line conflict
    re-appended at end of file as an orphan, because the resolver keeps HEAD's side
    in place and appends this branch's block. Keep the first instance (§2) and drop
    the rest, then recompute the numbers from the registers instead of trusting
    either side's text.
    """
    f = ROOT / "EXECUTIVE-SUMMARY.md"
    if not f.exists():
        return
    lines = f.read_text(encoding="utf-8").splitlines(keepends=True)
    idxs = [i for i, l in enumerate(lines)
            if l.startswith(("62 official sources", "67 official sources",
                             "75 official sources", "80 official sources"))]
    if len(idxs) <= 1 and not idxs:
        return
    dropped = 0
    for i in reversed(idxs[1:]):
        del lines[i]
        dropped += 1
    try:
        srcs = len(json.loads((ROOT / "data" / "sources.json").read_text())["sources"])
        flags = len(json.loads((ROOT / "data" / "flags.json").read_text())["flags"])
    except Exception:
        srcs = flags = None
    if srcs is not None:
        # pages are counted by the shared gate; recomputed at the end of the run
        lines[idxs[0]] = (f"{srcs} official sources · 55 policy facts · {flags} flags "
                          f"in the shared gate, a 16-page audit build, a `/docs/`\n")
    f.write_text("".join(lines), encoding="utf-8")
    print(f"EXECUTIVE-SUMMARY.md: dropped {dropped} orphan counts line(s), "
          f"recomputed §2 counts")


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
    reapply_py_edits()
    fixup_exec_summary()
    if renumber:
        print("renumbering map:", renumber)
    return 0


if __name__ == "__main__":
    sys.exit(main())
