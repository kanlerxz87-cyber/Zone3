#!/usr/bin/env python3
"""B38-T3 (session b3e82b38, 2026-11-19) — additive batch-3 register entries.

Appends, idempotently, to data/publication.json:
  - one source row `google-faq-update` (fetched live by this session on 2026-11-19)
  - five proposals `B38-P1…P5`
  - four questions `B38-Q1…Q4`
  - one design_prompt block `b38-batch3`
No existing row is rewritten, reordered or deleted. Running twice is a no-op.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REG = ROOT / 'data' / 'publication.json'

SOURCE = {
    "id": "google-faq-update",
    "title": "Google Search documentation updates — FAQ rich result deprecated May 2026, documentation removed June 2026",
    "url": "https://developers.google.com/search/updates",
    "checked_on": "2026-11-19",
    "scope": "Fetched live 19 Nov 2026 by session b3e82b38: the May 2026 entry “Deprecating the FAQ rich result feature” (“This feature will no longer appear in Google Search starting May 7, 2026”) and the June 2026 entry “Removing documentation for the FAQ rich result feature”. The former FAQ-page documentation URL now redirects to this updates page.",
}

PROPOSALS = [
    {
        "id": "B38-P1",
        "priority": "Now",
        "area": "Voice & anti-slop",
        "title": "Publish the house style as a page, and enforce it with a banned-phrase lint in the gate.",
        "why": "The design prompt's voice block already bans a list of words, but nothing published shows the rule and nothing automated enforces it. The 'AI slop' feel comes from repeatable tells — breathless adjectives, invented urgency, vague superlatives — and the release chain that already catches unsupported figures and claims is the right place to catch those too.",
        "next": "Draft the style page from the existing voice rules, then extend the check chain with a lint that fails on banned phrases across generated pages; add each banned phrase with a dated reason.",
        "evidence_needed": ["P26-Q7", "E61-Q8"],
        "source": "google-helpful",
        "status": "Proposed",
        "owner_input_needed": False,
        "next_action": "Write the style page from the design prompt's voice block, add a banned-phrase lint step to the release checks, run the full gate, and record the decision before publishing either.",
        "discoveries": [
            "Which phrases the current eight guides already avoid, so the lint starts from observed practice rather than taste",
            "Whether any existing sentence fails the proposed ban list — those would need a rewrite decision before the lint ships",
        ],
    },
    {
        "id": "B38-P2",
        "priority": "Now",
        "area": "Trust design",
        "title": "Promote the evidence line into a visible badge system on every card, table and guide.",
        "why": "Every product card carries a source line and every guide states its evidence limit, but both sit in small print a skimming reader never sees. A consistent two-level badge — what was checked, and what was not — turns the site's biggest honesty feature into its most visible design element, which is what separates a considered publication from generated filler.",
        "next": "Define the badge vocabulary from what the register can actually support (listing-checked date vs no hands-on testing vs unverified), render it from register dates in the shared card, table and guide renderers, and document it in the design prompt.",
        "evidence_needed": ["E61-Q2", "P26-Q6"],
        "source": "google-reviews",
        "status": "Proposed",
        "owner_input_needed": False,
        "next_action": "Add the badge markup to the shared renderers, driven by register dates and evidence levels, verify through the publication gate at desktop and mobile widths, and record the design decision.",
        "discoveries": [
            "Which evidence levels the register supports without inventing a claim (listing-checked, untested, unverified)",
            "Whether badges survive small screens without pushing the sponsored disclosure or evidence line out of view",
        ],
    },
    {
        "id": "B38-P3",
        "priority": "Next",
        "area": "Editorial slate",
        "title": "Approve the follow-on slate: four more question-shaped working titles.",
        "why": "The first slate (AS-01–07) covers holiday tables, probe placement, sync finish, counter space, presets, range and listing claims. Four repeatable reader situations are still uncovered: the weeknight household-size question (“Cooking for two on a Tuesday: is a double-basket air fryer overkill?”), thermometer accuracy specs (“What does ±0.5° on the box actually promise?”), home verification (“The ice-water check: what a thermometer owner can confirm with nothing but a cup of water”) and reheating (“Reheating leftovers: when does the air fryer earn its counter space?”). Each is a working title — an editorial hypothesis, not a popularity, search-volume or demand claim.",
        "next": "Owner picks which titles, if any, ship; each new guide follows the one-guide-per-review cadence through the same publishing gate as the current eight.",
        "evidence_needed": ["DS-01", "E61-Q1"],
        "source": "google-helpful",
        "status": "Proposed",
        "owner_input_needed": True,
        "next_action": "Pick the first title, draft it to the existing guide template with every section sourced from the register, run all gates, and record the decision before publishing.",
        "discoveries": [
            "Which of the four titles the owner wants first, and in what order",
            "Whether the listing wording of the five registered products supports enough sourced sections for the chosen title",
        ],
    },
    {
        "id": "B38-P4",
        "priority": "Next",
        "area": "Decision support",
        "title": "Publish the next review date, and close the loop from proposal to decision to outcome.",
        "why": "The register tells a reviewer what is open, but not when the next review is due or what happened to earlier choices. A due date derived from the 14-day cadence, and a visible outcome link for adopted proposals, would turn the review page from a suggestion list into an accountable workflow.",
        "next": "Derive the next review date from the register's updated date plus the cadence, render it with an explicit overdue state, and add an outcome field linking adopted proposals to their decision records.",
        "evidence_needed": ["E61-Q1", "E61-Q8"],
        "source": "search-console",
        "status": "Proposed",
        "owner_input_needed": False,
        "next_action": "Add the derived due date (with an overdue state, not a silently stale one) and the outcome-link field to the renderers, then record the decision before publishing.",
        "discoveries": [
            "Whether a cadence-derived due date misleads once missed — which is why it needs a visible overdue state rather than a stale date",
            "Which proposals already have a decision record an outcome link could point to",
        ],
    },
    {
        "id": "B38-P5",
        "priority": "Now",
        "area": "Traffic",
        "title": "Correct the FAQ plan before DS-03 ships: FAQ rich results no longer exist in Google Search.",
        "why": "Decision row DS-03 still offers “Add FAQPage structured data to a guide” as a choice. Google deprecated the FAQ rich result on May 7, 2026 and removed its documentation in June 2026, so the structured-data part of that plan can no longer pay off in Google Search. Reader-first FAQ blocks remain worth considering; shipping FAQPage markup while expecting a Google rich result would bake a stale premise into the site.",
        "next": "Keep the sourced-answer requirement of D9-03, drop the rich-result expectation, and decide FAQ blocks on reader utility alone; if markup is ever added, record what non-Google consumer it serves.",
        "evidence_needed": ["DS-03", "P26-Q4"],
        "source": "google-faq-update",
        "status": "Proposed",
        "owner_input_needed": False,
        "next_action": "Amend the DS-03 decision row's context with the deprecation dates before any FAQ work starts, then record the corrected decision.",
        "discoveries": [
            "Whether any current guide already has three or more sourced answers that would make an FAQ block worth shipping for readers alone",
            "What non-Google consumer of FAQPage markup, if any, the site would be serving before any markup is added",
        ],
    },
]

QUESTIONS = [
    {
        "id": "B38-Q1",
        "question": "What recurring budget, if any, is approved for hosting, a custom domain, imagery and tooling?",
        "known": "Nothing in the repository records a budget, an invoice or a spending approval. Everything shipped so far runs on free tiers and self-made assets.",
        "missing": "An approved amount, what it may be spent on, and who approves exceptions. Without it, hosting migration, photography and tooling choices have no constraint to reason against.",
        "discovery": "Owner decision: write the amount, its scope and the date into a decision record; then price the durable-host and imagery options against it.",
        "default": "No spend. Free tiers, self-made assets and no paid tooling until a dated approval exists.",
        "blocks": "Hosting migration (E61-Q7), imagery route (DS-02), original testing (P27-Q4)",
        "source": "github-pages",
        "owner_input_needed": True,
        "answer_form": "An amount, a scope list and a date — or an explicit zero-budget approval.",
    },
    {
        "id": "B38-Q2",
        "question": "What accountable publisher name and contact should the site publish for disclosure purposes?",
        "known": "The site publishes “Zone3 Editorial” as an organizational byline and states no hands-on testing. No legal entity, personal name or contact route is published anywhere.",
        "missing": "The name the owner is willing to publish and a working contact route, checked against the Associates rule on Amazon trademarks in identifiers (Participation Requirements 1(g)).",
        "discovery": "Owner records the name and contact in a decision record; the agent verifies it embeds no Amazon trademark and updates the about page and disclosure block from it.",
        "default": "Keep the organizational byline. Publish no invented persons and no personal data.",
        "blocks": "About/authorship polish, social republishing (E61-P8), the endorsement-context review (S-24)",
        "source": "ftc",
        "owner_input_needed": True,
        "answer_form": "A published name plus a working contact route, with the trademark check result noted.",
    },
    {
        "id": "B38-Q3",
        "question": "Which listing wording may be reproduced verbatim, and when must it be paraphrased?",
        "known": "Product cards use short listing-derived chips and titles, observed by hand and dated. The Associates policies restrict price display to Amazon-served links or licensed APIs and treat Program Content as Amazon-sourced.",
        "missing": "A written rule naming which text fields (title, feature chips, description sentences) may be quoted verbatim versus paraphrased, and who approves it.",
        "discovery": "Re-read Participation Requirements 2(a)–(b) and the PA-API licence terms, draft the rule, and have the owner approve it into the decision record before any more verbatim listing text is added.",
        "default": "Paraphrase by default; quote only short factual identifiers (titles, feature names) with a dated source link.",
        "blocks": "Product cards, comparison tables, any new catalogue row (E61-P9)",
        "source": "amazon-policies",
        "owner_input_needed": True,
        "answer_form": "A one-page rule naming allowed and forbidden text fields, with a date.",
    },
    {
        "id": "B38-Q4",
        "question": "How many new guides per review cycle are wanted, and what capacity limits apply?",
        "known": "The cadence is one guide reviewed every 14 days and eight guides exist. Nothing records how much verification and drafting effort one guide actually costs, or how many the owner wants per cycle.",
        "missing": "A capacity commitment per cycle, and a measured sense of effort per guide from the last two shipped guides.",
        "discovery": "Owner states the wanted number; the agent measures the real gate, verification and drafting steps from the last two guides and records both in the decision record.",
        "default": "Keep one guide per 14-day cycle until measured evidence says otherwise.",
        "blocks": "Article-slate commitments (AS-01–07, B38-P3), cadence promises (D9-01)",
        "source": "google-helpful",
        "owner_input_needed": True,
        "answer_form": "A number per cycle plus a dated effort note, or an explicit keep-the-cadence decision.",
    },
]

PROMPT_BLOCK = {
    "id": "b38-batch3",
    "heading": "Batch-3 directions (session b3e82b38)",
    "text": "Treat honesty as the design language. Render a two-level evidence badge — what was checked and when, what was not — on every card, comparison table and guide header, from register dates. Publish the house style as a page and enforce it with a banned-phrase lint in the release gate. Derive the next review date from the cadence and show it with an overdue state. Write FAQ blocks for readers only, never for a Google rich result, which was deprecated in May 2026. Grow the reading room with question-shaped working titles like the four in B38-P3, one per review cycle, through the same gate as every other guide. Every date and count on every page comes from the register — typed copy goes stale, derived copy cannot.",
    "basis": "google-helpful",
}


def main() -> int:
    data = json.loads(REG.read_text(encoding='utf-8'))
    source_ids = {s['id'] for s in data['sources']}
    proposal_ids = {p['id'] for p in data['proposals']}
    question_ids = {q['id'] for q in data['questions']}
    block_ids = {b['id'] for b in data['design_prompt']['blocks']}
    if (SOURCE['id'] in source_ids
            and all(p['id'] in proposal_ids for p in PROPOSALS)
            and all(q['id'] in question_ids for q in QUESTIONS)
            and PROMPT_BLOCK['id'] in block_ids):
        print('B38 batch already applied; nothing to do.')
        return 0

    # Referential integrity before writing: every evidence_needed id and every basis must
    # resolve to a row that exists after this batch, and no id may collide.
    known_refs = {q['id'] for q in data['questions']} | {d['id'] for d in data.get('review_b9008684', {}).get('decision_rows', [])}
    new_ids = {SOURCE['id']} | {p['id'] for p in PROPOSALS} | {q['id'] for q in QUESTIONS} | {PROMPT_BLOCK['id']}
    assert not (new_ids & (source_ids | proposal_ids | question_ids | block_ids)), 'id collision'
    assert all(r in known_refs for p in PROPOSALS for r in p['evidence_needed']), 'unknown evidence ref'
    assert all(p['source'] in (source_ids | {SOURCE['id']}) for p in PROPOSALS), 'unknown proposal basis'
    assert all(q['source'] in source_ids for q in QUESTIONS), 'unknown question basis'
    assert PROMPT_BLOCK['basis'] in source_ids, 'unknown prompt basis'
    # Union guard (reconciliation with session d3493182, PR #182): totals moved while this
    # batch was in flight (21 proposals / 32 questions on main). Guard only against the
    # original pre-batch state so a double-apply on the original tree cannot corrupt it.
    assert (len(data['sources']), len(data['proposals']), len(data['questions'])) in {
        (14, 15, 24), (14, 21, 32)}, 'unexpected register totals for the B38 delta'

    data['sources'].append(SOURCE)
    data['proposals'].extend(PROPOSALS)
    data['questions'].extend(QUESTIONS)
    data['design_prompt']['blocks'].append(PROMPT_BLOCK)
    REG.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'B38 batch applied: {len(data["sources"])} sources, {len(data["proposals"])} proposals, {len(data["questions"])} questions, {len(data["design_prompt"]["blocks"])} prompt blocks.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
