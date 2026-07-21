---
name: research-landscape-mapper
description: "Map broad research evidence, conflicts, gaps, opportunities, and novelty; use for field-level synthesis and Deep Research handoffs, not bounded 2-5-paper questions."
---
# research-landscape-mapper

## Role

Act as the single owner of broad retrieval policy. Retrieve, verify, and organize
evidence into separate Evidence and Opportunity Maps, limitations, and handoff
signals. Keep the scientific gap (what knowledge or evidence cannot yet answer)
separate from novelty positioning (how the proposed direction differs from its
closest work). Do not generate/rank Ideas, score artifacts, draft dossiers, or
imply systematic-review completeness without a protocol.

## Routing

1. Record the evidence-change materiality and route using
   `references/search-routing-rules.md`.
2. Reuse supplied evidence when no material evidence change is required.
3. Use Built-in Search for quick, recent, exact, or targeted verification.
4. Dispatch one bounded 2-5-paper synthesis to
   `focused-literature-synthesizer` when close full-text reading is needed.
5. Use Deep Research for major multi-stage, multi-direction, multi-source synthesis.
   If inactive or unknown, emit a self-contained continuation package, return
   `deep_research_handoff_required`, and stop.

Never combine several focused syntheses to imitate a field-level landscape or
novelty search.

For exact biomedical identifiers, use Built-in Search scoped to PubMed/NCBI.
Local scripts are never the default; use them only as reproducibility fallbacks.

## Procedure

1. Normalize the question, downstream decision, domain, constraints, supplied
   artifacts, freshness, and output need.
2. Select reuse/Search/focused synthesis/landscape mapping and
   `retrieval_mode: standard | focused | divergent`; this is independent of the
   Idea direction route.
3. Plan source classes, bounds, exclusions, queries, and stop condition.
4. Retrieve or emit the Deep Research continuation package.
5. Verify source identity and supporting passages; record citations through
   `references/citation-record-contract.md`, including inferred matches from
   incomplete user clues; record negative, inaccessible, conflicting, and
   access-limited evidence.
6. Label each material claim `supported | weak | conflicting | single-source |
   unverified | access-limited`. Give every internal ID a readable label and
   original source locator suitable for a node reference ledger.
7. Build distinct Evidence and Opportunity Maps with stable citations. In the
   Opportunity Map, record `scientific_gap`, `novelty_positioning`, and an
   evidence-grounded `reader_reasoning_handoff` as separate objects.
8. For Idea work, emit evidence-grounded routing signals using
   `references/idea-direction-routing-signals.md`; do not choose or score an Idea.
9. On bounded-exploration remap, scope retrieval to one evolved dossier and
   return evidence/claim synchronization notes. Do not rewrite the dossier or
   introduce objectives, data, methods, or work packages.
10. Return concise pointers, route/mode, freshness, conflicts, limitations,
    unresolved gaps, and downstream consumers, not raw logs by default.

Terminology standardity, naturalness, first-use explanation, and replacement
recommendations belong to `academic-language-assessor`. Do not create a
terminology register or terminology-evidence packet here.

## Outputs

Evidence Map, Opportunity Map, Evidence Limitations, and Handoff Notes. Emit a
Search/verification log only for audit, conflict, failure, or explicit request;
an insufficiency report when reliable mapping is impossible; and a Deep
Research continuation package when required but inactive.

Never send maps as project inputs to `idea-evaluator`. The writer must integrate
all evaluation-relevant facts and normal citations into the complete dossier.

## Conditional Resources

- Read `references/exploration-strategy-rules.md` when selecting route or mode.
- Read `references/search-routing-rules.md` for retrieval-path selection and
  evidence-change materiality.
- Read `references/citation-record-contract.md` whenever recording citations or
  resolving incomplete citation clues.
- Read `references/focused-search-routing.md` for focused retrieval.
- Read `references/divergent-search-routing.md` for divergent retrieval.
- Read `references/iterative-literature-search.md` for iterative retrieval.
- Read `references/evidence-source-priority.md` when selecting sources.
- Read `references/evidence-confidence-rules.md` when grading claims.
- Read `references/chinese-literature-access-rules.md` for Chinese literature.
- Read `references/opportunity-type-taxonomy.md` when classifying gaps.
- Read `references/design-pattern-strategy-routing.md` when interpreting designs.
- Read `references/research-article-clue-extraction.md` when extracting article clues.
- Read `references/idea-direction-routing-signals.md` for initial Idea routing or
  per-direction remapping.
- Read `references/evidence-map-schema.md`, `references/opportunity-map-schema.md`,
  and `references/downstream-handoff-rules.md` when writing maps/handoffs.
- Read `references/deep-research-prompt-rules.md` only for Deep Research.
- Use `templates/evidence-map.md` for an Evidence Map.
- Use `templates/opportunity-map.md` for an Opportunity Map.
- Use `templates/evidence-insufficiency-report.md` on evidence insufficiency.
- Use `templates/source-verification-log.md` when a verification log is required.
- Use `templates/deep-research-request.md` when Deep Research requires a
  continuation request.
- Use `templates/deep-research-follow-up-guide.md` after creating that request.
- Run `scripts/evidence_search.py` only on explicit reproducible-batch request.

## Completion Check

Confirm materiality/route/mode, source verification, GB/T 7714—2015 citations
with complete links, readable claim labels/locators,
separate maps, distinct scientific-gap and novelty-positioning objects, a
five-function reader handoff for Idea work, visible limits/conflicts, optional
Idea routing/remap signals, correct Deep Research pause, and no unsupported
novelty, terminology verdict, or Idea decision.
