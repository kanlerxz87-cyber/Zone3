#!/usr/bin/env python3
"""Session 1dddf8c0 — 1dd-T3 phase 2.

Cleans the residuals left by phase 1: artifacts from blanket replacement,
remaining root-page HTML cells, the root flag register, the historical
snapshot JSON files, and the frozen archive/c4e71983 copy. Same policy basis:
Amazon Associates Program Policies Participation Requirements 2(b) and 6(t).
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
W = "Withheld"

GLOBAL = [
    "$79.93", "$79.91", "$149.99", "$99.99", "$209.99", "$119.99",
    "$57.45", "$92.99", "$49.54", "$39.97", "$89.99", "$99.95", "$129.95",
    "$57.91", "$39.99", "$199.95", "$69.97", "$130", "$97.49", "$51.94",
    "$2.40", "$3.60", "$6.75", "$4.50",
    "4.2★", "4.3★", "4.4★", "4.2 / 5", "4.3 / 5", "4.4 / 5",
    "4.8K", "18.3K", "16.8K", "39.9K",
    "10,984", "22,768", "4,015", "7,552", "52,301", "4,859", "18,320", "16,863", "392",
    "1K+", "3K+", "4K+", "8K+",
    "Limited time deal", "Early Black Friday Deal",
    "33.4%", "28.6%", "20.1%",
]

def sub(s, pairs, label):
    for old, new in pairs:
        if old in s:
            s = s.replace(old, new)
        else:
            print(f"  [warn] not found ({label}): {old[:70]}")
    return s

# ---------------------------------------------------------------------------
# 1. Fix phase-1 artifacts: "Withheld bought in past month"
# ---------------------------------------------------------------------------
for rel in ["research/252122ff-verification-log.md",
            "sessions/3c886b62/docs/RESEARCH.md",
            "sessions/3c886b62/docs/VERIFICATION.md"]:
    p = ROOT / rel
    s = p.read_text(encoding="utf-8").replace("Withheld bought in past month", "Withheld (demand signal)")
    p.write_text(s, encoding="utf-8")
    print(f"[1] artifact fixed: {rel}")

# ---------------------------------------------------------------------------
# 2. Root executive summary badge figures
# ---------------------------------------------------------------------------
p = ROOT / "EXECUTIVE-SUMMARY.md"
s = p.read_text(encoding="utf-8")
s = sub(s, [
    ('Amazon\'s "bought in past month" badges (`1K+`, `4K+`, `3K+`) were published in prose on a page that withholds prices for exactly that reason.',
     'Amazon\'s "bought in past month" badge figures were published in prose on a page that withholds prices for exactly that reason.'),
], "EXECUTIVE-SUMMARY.md")
p.write_text(s, encoding="utf-8")
print("[2] EXECUTIVE-SUMMARY.md badge figures withheld")

# ---------------------------------------------------------------------------
# 3. Root docs HTML residuals
# ---------------------------------------------------------------------------
HTML2 = {
    "docs/analysis.html": [
        ('<td><span class="badge warn">Limited time deal</span></td>',
         '<td><span class="badge warn">Promotion badge withheld</span></td>'),
        ('<td><span class="badge warn">Early Black Friday Deal</span></td>',
         '<td><span class="badge warn">Promotion badge withheld</span></td>'),
        ('<td class="num"><strong>39.9K</strong></td>',
         '<td class="num"><strong>Withheld</strong></td>'),
        ('<p class="src-note">¹ Computed = review count (K) × rating. ² Weighted average = Σ(reviews×rating) ÷ Σreviews = 172.77 ÷ 39.9 = 4.33, shown as 4.31 using unrounded display values; both derived strictly from the verified cells. Amazon rounds displayed counts (4.8K/18.3K/16.8K), so combined figures inherit that rounding.</p>',
         '<p class="src-note">¹ Computed = review count (K) × rating. ² Weighted average computed from the withheld display values (Amazon Policies 2(b)/6(t)); both derived strictly from the verified cells. Amazon rounds displayed counts, so combined figures inherit that rounding.</p>'),
        ('Largest review base (18.3K) and highest absolute discount ($60 off list) — the natural "premium pick" headline for a buying guide; the two Chefman units anchor budget picks.',
         'Largest review base and highest absolute discount of the three (values withheld per Amazon Policies 2(b)/6(t)) — the natural "premium pick" headline for a buying guide; the two Chefman units anchor budget picks.'),
        ('at capture (2026-11-13) all three carried promotion badges ("Limited time deal" ×2, "Early Black Friday Deal" ×1) with 20–33% off list —',
         'at capture (2026-11-13) all three carried promotion badges with discounts off list (values withheld per Amazon Policies 2(b)) —'),
    ],
    "docs/content.html": [
        ('<tr><td>Deal badge at capture</td><td><span class="badge warn">Limited time deal</span></td><td><span class="badge warn">Early Black Friday Deal</span></td>',
         '<tr><td>Deal badge at capture</td><td><span class="badge warn">Promotion badge withheld</span></td><td><span class="badge warn">Promotion badge withheld</span></td>'),
        ('<tr><td>Budget / dual-zone — CHEFMAN 6 Qt</td><td class="num">4.2★</td>',
         '<tr><td>Budget / dual-zone — CHEFMAN 6 Qt</td><td class="num"><span class="badge unv">Withheld</span></td>'),
        ('<tr><td>Premium / capacity — Emeril 26QT</td><td class="num">4.3★</td>',
         '<tr><td>Premium / capacity — Emeril 26QT</td><td class="num"><span class="badge unv">Withheld</span></td>'),
        ('<tr><td>Value / simplicity — Chefman 8 Qt</td><td class="num">4.4★</td>',
         '<tr><td>Value / simplicity — Chefman 8 Qt</td><td class="num"><span class="badge unv">Withheld</span></td>'),
        ('At capture (2026-11-13) all three units carried deal badges with 20–33% off list — Amazon was running "Limited time deal" and "Early Black Friday Deal" promotions.',
         'At capture (2026-11-13) all three units carried promotion badges with discounts off list (values withheld per Amazon Policies 2(b)).'),
    ],
    "docs/executive-summary.html": [
        ('<li><strong>Promotion-driven conversion window.</strong> All three carried deal badges at capture (two "Limited time deal", one "Early Black Friday Deal") — timely hooks, but volatile (<a href="flagged.html#F5">F5</a>).</li>',
         '<li><strong>Promotion-driven conversion window.</strong> All three carried promotion badges at capture (badge names withheld per Amazon Policies 2(b)) — timely hooks, but volatile (<a href="flagged.html#F5">F5</a>).</li>'),
    ],
    "docs/index.html": [
        ('<div class="card"><div class="k">Avg. rating (weighted)</div><div class="v">4.3 <small>/ 5</small></div><div class="sub">39.9K reviews combined</div></div>',
         '<div class="card"><div class="k">Avg. rating (weighted)</div><div class="v">Withheld <small>/ 5</small></div><div class="sub">Combined review count withheld (6(t))</div></div>'),
    ],
    "docs/sources.html": [
        ('<td>Discounts −20.1% / −28.6% / −33.4%</td>',
         '<td>Discounts withheld (derived from withheld prices)</td>'),
        ('<td>Combined reviews 39.9K · combined velocity 8K+</td>',
         '<td>Combined reviews and velocity withheld</td>'),
    ],
}
for rel, pairs in HTML2.items():
    p = ROOT / rel
    s = p.read_text(encoding="utf-8")
    s = sub(s, pairs, rel)
    p.write_text(s, encoding="utf-8")
    print(f"[3] redacted {rel}")

# ---------------------------------------------------------------------------
# 4. Flag registers (values inside flag text)
# ---------------------------------------------------------------------------
p = ROOT / "data/flags.json"
s = p.read_text(encoding="utf-8")
for v in ["4.8K", "18.3K", "16.8K", "10,984", "22,768", "52,301"]:
    s = s.replace(v, W)
p.write_text(s, encoding="utf-8")
print("[4] data/flags.json redacted")

p = ROOT / "sessions/3c886b62/data/flags.json"
s = p.read_text(encoding="utf-8")
s = s.replace("Amazon displays '4.8K', '18.3K' and '16.8K' rather than exact counts. These are Amazon's own rounded figures, recorded verbatim, not exact integers.",
              "Amazon displays rounded counts rather than exact integers. The observed rounded figures are withheld per 6(t).")
for v in ["4.8K", "18.3K", "16.8K"]:
    s = s.replace(v, W)
p.write_text(s, encoding="utf-8")
print("[4] sessions/3c886b62/data/flags.json redacted")

# ---------------------------------------------------------------------------
# 5. Root historical snapshot JSON files
# ---------------------------------------------------------------------------
for rel in ["data/c4e71983-commercial-snapshot.json",
            "data/c4e71983-competitors.json",
            "data/z3-51fcb80d-snapshot.json"]:
    p = ROOT / rel
    s = p.read_text(encoding="utf-8")
    orig = s
    for v in GLOBAL:
        s = s.replace(v, W)
    if s != orig:
        p.write_text(s, encoding="utf-8")
        print(f"[5] redacted {rel}")

# ---------------------------------------------------------------------------
# 6. Frozen archive/c4e71983 copy (HTML + MD)
# ---------------------------------------------------------------------------
ARCHIVE_REWRITES = {
    "archive/c4e71983/EXECUTIVE-SUMMARY.md": [
        ("The band above $130 is the thinnest part of the captured top six — and it is where the $149.99 unit sits.",
         "The upper price band is the thinnest part of the captured top six, and the premium unit sits in it."),
        ("volume, with Prime bounties, or by steering traffic toward the $149.99 unit. Nothing can earn yet:",
         "volume, with Prime bounties, or by steering traffic toward the premium unit. Nothing can earn yet:"),
    ],
    "archive/c4e71983/research/niche-analysis.md": [
        ("4.2–4.4. Meanwhile the $149.99 unit — the most expensive thing on this page — shows the strongest",
         "a narrow high band. Meanwhile the premium unit — the most expensive thing on this page — shows the strongest"),
        ("just 126 ratings. The $149.99 promoted unit has 18.3K ratings shown. That is the least contested",
         "a thin sample. The promoted premium unit has a large rating count shown. That is the least contested"),
        ("**d. Two products are priced identically.** At $79.91 and $79.93 they are two cents apart, despite",
         "**d. Two products are priced almost identically.** Despite"),
        ("16.8K ratings) is objectively the stronger of the two on the captured data. That makes it the natural",
         "the larger rating count) is objectively the stronger of the two on the captured data. That makes it the natural"),
        ("All three products were discounted at capture, two with a *Limited time deal* badge and one with an\n*Early Black Friday Deal* badge — consistent with mid-November. Discount depth vs list:",
         "All three products were discounted at capture, with promotion badges on all three — consistent with mid-November. Discount depth vs list:"),
    ],
}

import os
count = 0
for dirpath, _dirs, files in os.walk(ROOT / "archive/c4e71983"):
    for fn in files:
        if not fn.endswith((".html", ".md")):
            continue
        rel = os.path.relpath(os.path.join(dirpath, fn), ROOT).replace(os.sep, "/")
        p = ROOT / rel
        s = p.read_text(encoding="utf-8")
        orig = s
        s = sub(s, ARCHIVE_REWRITES.get(rel, []), rel)
        for v in GLOBAL:
            s = s.replace(v, W)
        if s != orig:
            p.write_text(s, encoding="utf-8")
            count += 1
print(f"[6] {count} archive files redacted")

print("phase 2 done")
