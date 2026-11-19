# Session `b3e82b38` — repo review note (2026-11-19)

Scope of this review pass: the publication register (`data/publication.json`), the release chain
(`tools/publish.py`, `tools/build_publication.py`, `tools/check_publication.py`), and the two PRs
that merged on `main` while this session was claiming (PR #181 and #184, session `07fb37ba`).

Findings:

| ID | Severity | Finding | Disposition |
|---|---|---|---|
| B38-IR-01 | Info | At base `6eb8c18` the executive-brief strip still showed hardcoded “6 question-led buyer guides” and “9 decision-readiness questions” against a register of 8 and 24 — the last surviving hardcoded count, contradicting the register-derived counts policy (`P27-F02`/`P27-F04`). | **Fixed upstream independently** while this claim was being pushed: PR #181 (part Z3-COUNT-01, session `07fb37ba`) derived the strip from the registers and added a consistency gate. This session verified the fix on the new base rather than re-applying it. Closed as resolved-upstream. |
| B38-IR-02 | Info | Decision row DS-03 (“Add FAQPage structured data to a guide”) rests on a now-stale premise: Google deprecated the FAQ rich result on May 7, 2026 and removed its documentation in June 2026 (verified live; source `google-faq-update`). | Not edited — DS-03 belongs to session `b9008684`'s review round. Proposal **B38-P5** records the correction for the reviewer instead, which is the additive path the board rules require. |
| B38-IR-03 | Info | The reader-facing register has no question about budget and none about the accountable publisher identity; both block decisions the register already tracks (hosting migration, imagery, about-page polish). | Filled additively as `B38-Q1` and `B38-Q2`; nothing existing rewritten. |

Nothing else irregular: the 25-check baseline passed at base, the merged upstream diffs match their
coordination records, and no conflict marker or provenance gap was found in the touched files.
