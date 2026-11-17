# S-20 mobile-first audit — reader layer `site/` (2026-11-17, session 82372fd1)

Method: the audit reads the CSS source of record — the `CSS` constant in
`tools/build_i2_site.py` (the only sanctioned path to `site/assets/site.css`) — and computes
target boxes from the box model. These are computations, not browser renders; a phone
spot-check by a human remains the accepted way to confirm feel. WCAG reference:
SC 2.5.8 Target Size (Minimum), 24×24 CSS px with a spacing exception —
https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html ; the 44px figure is
the AAA-level 2.5.5 / platform-guideline target used as the bump value.

## Meets (already present before this session)

- viewport meta on every generated page (line 126 of the generator).
- `-webkit-text-size-adjust: 100%` (base html rule).
- Fluid type: `h1 clamp(30px, 4.4vw, 44px)`, `h2 clamp(22px, 2.6vw, 29px)`; body 16px/1.6.
- Sticky masthead + disclosure bar (`.top{position:sticky}`; disclosure above the fold).
- Wide tables scroll: `.tablewrap{overflow:auto}`.
- ≤700px block already reflowed nav, gutters and the proposal-card grid.

## Deficient → fixed (commit `2ca865e`)

| Control | Before (computed) | After |
|---|---|---|
| `.src` source chips (also the only path from a table row to its evidence) | ~22px tall — below the 24px floor; 2px gaps, so the spacing exception did not apply | `min-height:24px` (all viewports; inline-flex) |
| `.top nav a` | ~39px | `min-height:44px` |
| `.seg` Accept/Reject/Defer labels | ~33px | `min-height:44px` |
| `.btn` (mobile block) | ~43px | `min-height:44px` |
| `scroll-behavior:smooth` | unconditional | guarded by `prefers-reduced-motion: reduce` |
| Mobile table gutters | `11px 14px` cell padding | `9px 10px` in the ≤700px block to reclaim width — font size deliberately NOT reduced |

Rebuild path followed exactly: generator edit → `tools/build_i2_site.py` →
`tools/build_cba81fa5_site.py` → `tools/build_feed.py`; i2_gate, cba lint, verify_site,
check_all_links all green after. Dashboard CSS (`assets/style.css`, `assets/app.css`) was
left alone: it already has sticky table headers (`app.css` line 96) and is an audit surface,
not the shop.
