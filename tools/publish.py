#!/usr/bin/env python3
"""One reproducible build/release command for the existing Zone3 tree.

    python3 tools/publish.py           # rebuild all retained layers, then run ALL gates
    python3 tools/publish.py --check   # checks only; no HTML generation

No network, credentials, clicks to Amazon, report fabrication or account changes. Current
reader pages have one owner (build_publication); all older evidence bodies are retained.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUILDERS = [
    ['python3', 'scripts/build_site.py'],
    ['python3', 'tools/build_i2_site.py'],
    ['python3', 'tools/build_cba81fa5_site.py'],
    ['python3', 'tools/build_shop.py'],
    ['python3', 'tools/build_measurement.py'],
    ['python3', 'tools/build_brief_status.py'],
    ['python3', 'scripts/build_marketing.py'],
    ['python3', 'scripts/build_read.py'],
    ['python3', 'scripts/build_5a56c084.py'],
    ['python3', 'tools/build_site.py'],
    # Retains original intent/pass records, delegates current reader pages to build_publication.
    ['python3', 'sessions/aebf0747/build_pass.py'],
    ['python3', 'sessions/aebf0747/publish_pass.py'],
    ['python3', 'tools/measure_pass.py'],
    ['python3', 'tools/build_feed.py'],
    # README carries the shipped RSS XML count, so refresh the canonical pages and README only
    # after the feed has reached its final, sitemap-filtered state.
    ['python3', 'tools/build_publication.py'],
    # 4B0-T2: the owner-supplied Associates ID goes on every product-detail link, after every
    # builder has written its HTML and before the sponsored-token pass, which leaves it alone.
    ['python3', 'tools/attach_associates_tag.py'],
    ['python3', 'scripts/mark_sponsored.py'],
    # 5D4-F01: product links must carry the selected Associates tag (Program Policies 2(b)).
    # Runs after every generator and after mark_sponsored, before the sitemap snapshot.
    ['python3', 'tools/attach_tag.py'],
    ['python3', 'scripts/build_sitemap.py'],
]
CHECKS = [
    ['python3', 'scripts/check_site.py'],
    ['python3', 'tools/verify_site.py'],
    ['python3', 'tools/link_report.py', '--strict'],
    ['python3', 'tools/i2_gate.py'],
    ['python3', 'scripts/build_sitemap.py', '--check'],
    ['python3', 'tools/build_feed.py', '--check'],
    ['python3', 'scripts/cba81fa5_test_no_repr_output.py'],
    ['python3', 'tools/cba81fa5_lint.py'],
    ['python3', 'scripts/check_all_links.py'],
    ['python3', 'tools/build_shop.py', '--check'],
    ['python3', 'sessions/aebf0747/publish_pass.py', '--check'],
    ['python3', 'tools/measure_pass.py', '--check'],
    ['python3', 'tools/build_measurement.py', '--check'],
    ['python3', 'tools/build_brief_status.py', '--check'],
    ['python3', 'tools/build_cba81fa5_site.py', '--check'],
    ['python3', 'scripts/mark_sponsored.py', '--check'],
    ['python3', 'tools/attach_associates_tag.py', '--check'],
    ['python3', 'scripts/test_attach_associates_tag.py'],
    ['python3', 'tools/apply_sponsored.py', '--check'],
    ['python3', 'tools/add_disclosure_banner.py', '--check'],
    ['python3', 'tools/build_publication.py', '--check'],
    ['python3', 'tools/check_feed_readme.py'],
    ['python3', 'tools/check_publication.py'],
    # 5D4-F01 gate: no product link may leave the build without the tracking ID.
    ['python3', 'tools/attach_tag.py', '--check'],
    ['python3', 'sessions/5d460e79/test_attach_tag.py'],
    ['python3', 'sessions/5d460e79/test_counts.py'],
    # 9E-T2 gate: every registered listing has an indexable, sourced, tagged, sponsored page
    # that the front page, its category page and the comparison table all link to.
    ['python3', 'sessions/9ed0552a/test_product_pages.py'],
    ['python3', 'sessions/9ed0552a/test_product_pages.py', '--self-test'],
    ['python3', 'sessions/5d460e79/test_decision_record.py'],
    ['python3', 'tools/analytics_endpoint.py', '--self-test'],
    ['python3', 'sessions/1c072a7a/test_collector.py'],
    ['node', 'sessions/38650305/test_measure.js'],
    ['node', 'sessions/1c072a7a/test_measure.cjs'],
    ['node', '--check', 'assets/publication.js'],
]


def run(check_only: bool, report: str | None = None) -> int:
    results = []
    for command in ([] if check_only else BUILDERS) + CHECKS:
        proc = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
        output = proc.stdout + proc.stderr
        results.append({'command': ' '.join(command), 'exit_code': proc.returncode, 'output': output})
        print(('PASS ' if proc.returncode == 0 else 'FAIL ') + ' '.join(command), flush=True)
        if proc.returncode:
            print(output, flush=True)
            if command in BUILDERS:
                break  # never run later builders on a half-built tree
    if report:
        path = ROOT / report
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(results, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    failed = sum(r['exit_code'] != 0 for r in results)
    print(f'{len(results)} commands checked; {failed} failed. Structural checks do not verify every historical factual claim.', flush=True)
    return int(bool(failed))


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--check', action='store_true')
    ap.add_argument('--report', help='optional repository-relative JSON verification record')
    args = ap.parse_args()
    sys.exit(run(args.check, args.report))
