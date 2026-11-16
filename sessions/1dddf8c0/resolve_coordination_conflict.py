#!/usr/bin/env python3
"""Resolve COORDINATION.md append-append conflicts per the board's own convention
(see dff4acde / ecbfe91b entries): keep both sides in full, main's (HEAD) content
first, then this session's, then strip all conflict markers.
"""
from pathlib import Path

p = Path("COORDINATION.md")
lines = p.read_text(encoding="utf-8").splitlines(keepends=True)


def find_region(lines, start):
    eq = next(i for i in range(start, len(lines)) if lines[i].startswith("======="))
    end = next(i for i in range(eq, len(lines)) if lines[i].startswith(">>>>>>>"))
    return eq, end


out = []
i = 0
regions = 0
while i < len(lines):
    l = lines[i]
    if l.startswith("<<<<<<< "):
        eq, end = find_region(lines, i)
        out.extend(lines[i + 1 : eq])
        out.extend(lines[eq + 1 : end])
        regions += 1
        i = end + 1
    else:
        out.append(l)
        i += 1

p.write_text("".join(out), encoding="utf-8")
leftover = [l for l in out if l.startswith(("<<<<<<< ", ">>>>>>> "))]
print(f"resolved {regions} conflict regions; leftover markers: {len(leftover)}")
for l in leftover:
    print("  leftover:", l.rstrip())
