#!/usr/bin/env python3
"""One-off (ded63349): make the root-index and flagged comparisons in build_cba81fa5_site.py
compare marked text with marked text, so --check and write agree."""
import pathlib

p = pathlib.Path(__file__).resolve().parent.parent / "tools" / "build_cba81fa5_site.py"
raw = p.read_text(encoding="utf-8")

subs = [
    # root index: mark the expected text before comparison; write the marked text once
    ('        band = render_frontdoor(raw)\n        if FD_START in raw:\n            want = patch_text(raw, FD_START, FD_END, band, include_end=True)',
     '        band = render_frontdoor(raw)\n        if FD_START in raw:\n            # ded63349: mark before compare — the file on disk is post-sponsored, so the\n            # expected text must be too (otherwise --check always reports a stale region).\n            want = mark_sponsored(patch_text(raw, FD_START, FD_END, band, include_end=True))'),
    ('                root_index.write_text(mark_sponsored(want), encoding="utf-8")',
     '                root_index.write_text(want, encoding="utf-8")'),
    # flagged block: same treatment
    ('            want = patch_text(raw, start, "</main>", flagged_block())',
     '            want = mark_sponsored(patch_text(raw, start, "</main>", flagged_block()))'),
    ('                fl.write_text(mark_sponsored(want), encoding="utf-8")',
     '                fl.write_text(want, encoding="utf-8")'),
]
for old, new in subs:
    assert old in raw, old[:60]
    raw = raw.replace(old, new, 1)

p.write_text(raw, encoding="utf-8")
print("root + flagged comparisons now mark-consistent")
