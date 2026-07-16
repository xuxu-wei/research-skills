---
name: research-opportunity-mapper
description: "Build source-grounded evidence and opportunity maps for broad retrieval, claim checks, novelty, evidence limits, and research gaps."
---
# research-opportunity-mapper

## Role

Act as the single owner of broad retrieval policy. Retrieve, verify, and organize evidence into
separate Evidence and Opportunity Maps, limitations, and handoff signals. Do not
generate/rank Ideas, score artifacts, draft dossiers, or imply systematic-review
completeness without a protocol.

## Routing

1. Use supplied sources when they are sufficient and verify membership/identity.
2. Use Built-in Search for quick, recent, exact, or targeted retrieval; open them,
   prioritizing primary or authoritative sources, and stop at decision sufficiency.
3. Use Deep Research for multi-stage, multi-direction, multi-source synthesis.
   If inactive or unknown, emit a self-contained continuation package, return
   `deep_research_handoff_required`, and stop.

For exact biomedical identifiers, use Built-in Search scoped to PubMed/NCBI.
Local scripts are never the default; use them only as reproducibility fallbacks.

## Procedure

1. Normalize the question, downstream decision, domain, constraints, supplied
   artifacts, freshness, and output need.
2. Select supplied/Search/Deep Research and `retrieval_mode: standard | focused
   | divergent`; this is independent of the Idea direction route.
3. Plan source classes, bounds, exclusions, queries, and stop condition.
4. Retrieve or emit the Deep Research continuation package.
5. Verify source identity and supporting passages; record negative, inaccessible,
   conflicting, and access-limited evidence.
6. Label each material claim `supported | weak | conflicting | single-source |
   unverified | access-limited`. Give every internal ID a readable label and
   original source locator suitable for a node reference ledger.
7. Build distinct Evidence and Opportunity Maps with stable citations.
8. For Idea work, emit evidence-grounded routing signals using
   `references/idea-direction-routing-signals.md`; do not choose or score an Idea.
9. On bounded-exploration remap, scope retrieval to one evolved dossier and
   return evidence/claim synchronization notes. Do not rewrite the dossier or
   introduce objectives, data, methods, or work packages.
10. Return concise pointers, route/mode, freshness, conflicts, limitations,
    unresolved gaps, and downstream consumers, not raw logs by default.

## Outputs

Evidence Map, Opportunity Map, Evidence Limitations, and Handoff Notes. Emit a
Search/verification log only for audit, conflict, failure, or explicit request;
an insufficiency report when reliable mapping is impossible; and a Deep
Research continuation package when required but inactive.

Never send maps as project inputs to `idea-evaluator`. The writer must integrate
all evaluation-relevant facts and normal citations into the complete dossier.

## Conditional Resources

- Read `references/exploration-strategy-rules.md` when selecting route or mode.
- Read `references/search-routing-rules.md` for retrieval-path selection.
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
- Use `templates/deep-research-prompt-template.md` for a continuation package.
- Run `scripts/evidence_search.py` only on explicit reproducible-batch request.

## Completion Check

Confirm route/mode, source verification, readable claim labels/locators,
separate maps, visible limits/conflicts, optional Idea routing/remap signals,
correct Deep Research pause, and no unsupported novelty or Idea decision.
