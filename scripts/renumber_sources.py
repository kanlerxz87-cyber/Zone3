#!/usr/bin/env python3
"""Rewrite this session's source-id references after the integration renumber.

Reads the mapping written by scripts/integrate_rebase.py and applies it ONLY to files that
this session owns outright, plus the two targeted regions in shared files. main's own
references to the ids it already held (e.g. S59 = the FTC Consumer Reviews Rule Q&A) are
never touched, so a blanket replace could not be used.

  data/editorial.json      whole file (created by this session)
  scripts/build_read.py    whole file (created by this session)
  data/flags.json          only inside the Z14-F-* entries
  COORDINATION.md          only from this session's Part marker to end of file

    python3 scripts/renumber_sources.py            # apply
    python3 scripts/renumber_sources.py --check    # report, write nothing
"""
from __future__ import annotations
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
MAPFILE = ROOT / ".git" / "Z14_SOURCE_RENUMBER.json"
PART = "# Part: session `145b8df7`"


def main() -> int:
    if not MAPFILE.exists():
        print("no renumber map present — nothing to do")
        return 0
    mapping = json.loads(MAPFILE.read_text())
    if not mapping:
        print("empty renumber map — nothing to do")
        return 0
    check = "--check" in sys.argv
    changed: list[str] = []

    def sub(text: str) -> str:
        # longest old ids first so S6 never rewrites inside S68
        for old in sorted(mapping, key=lambda x: -len(x)):
            text = re.sub(rf"\b{old}\b", mapping[old], text)
        return text

    for rel in ("data/editorial.json", "scripts/build_read.py"):
        p = ROOT / rel
        if not p.exists():
            continue
        new = sub(p.read_text(encoding="utf-8"))
        if new != p.read_text(encoding="utf-8"):
            changed.append(rel)
            if not check:
                p.write_text(new, encoding="utf-8")

    fp = ROOT / "data/flags.json"
    if fp.exists():
        d = json.loads(fp.read_text())
        n = 0
        for f in d["flags"]:
            if f["id"].startswith("Z14-F"):
                out = []
                for s in f.get("sources", []):
                    if s in mapping:
                        out.append(mapping[s]); n += 1
                    else:
                        out.append(s)
                f["sources"] = out
        if n:
            changed.append(f"data/flags.json ({n} refs in Z14-F-* entries)")
            if not check:
                fp.write_text(json.dumps(d, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    cp = ROOT / "COORDINATION.md"
    if cp.exists():
        raw = cp.read_text(encoding="utf-8")
        if PART in raw:
            head, tail = raw.split(PART, 1)
            new_tail = sub(tail)
            if new_tail != tail:
                changed.append("COORDINATION.md (this Part only)")
                if not check:
                    cp.write_text(head + PART + new_tail, encoding="utf-8")

    print(("would rewrite: " if check else "rewrote: ") + ", ".join(changed))
    print("mapping:", json.dumps(mapping))
    return 0


if __name__ == "__main__":
    sys.exit(main())
