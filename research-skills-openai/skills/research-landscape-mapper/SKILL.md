---
name: research-landscape-mapper
description: "Map broad research evidence, conflicts, gaps, opportunities, and novelty; use for field-level synthesis and Deep Research handoffs, not bounded 2-5-paper questions."
---
# research-landscape-mapper

## Role

Act as the single owner of broad retrieval policy. Retrieve, verify, and organize
evidence for the downstream decision. Keep the scientific gap (what knowledge
or evidence cannot yet answer) separate from novelty positioning (how the
proposed direction differs from its closest work). Do not generate/rank Ideas,
score artifacts, draft dossiers, or imply systematic-review completeness
without a protocol.

## Routing

1. Record the evidence-change materiality and route using
   `references/search-routing-rules.md`.
2. Reuse supplied evidence when no material evidence change is required.
3. Use Built-in Search for quick, recent, exact, or targeted verification.
4. For one bounded 2-5-paper full-text question, return a focused synthesis
   request to the parent orchestrator. When invoked as a standalone entry, the
   mapper may dispatch that one request to `focused-literature-synthesizer`.
5. Use Deep Research for major multi-stage, multi-direction, multi-source synthesis.
   If inactive or unknown, emit a self-contained continuation package, return
   `deep_research_handoff_required`, and stop.

Never combine several focused syntheses to imitate a field-level landscape or
novelty search.

For exact biomedical identifiers, use Built-in Search scoped to PubMed/NCBI.

## Procedure

1. Normalize the question, downstream decision, domain, constraints, supplied
   artifacts, freshness, consumer workflow, and output profile:
   `evidence_only | evidence_and_opportunity | idea_landscape`.
2. Select reuse/Search/focused synthesis/landscape mapping and
   `retrieval_mode: auto | built_in_web_search | deep_research` plus
   `exploration_mode: standard | focused | divergent`; these are independent of
   the Idea direction route. Production runs use `auto` unless the researcher
   explicitly selects a mode. A test fixture may force one mode.
3. Plan source classes, bounds, exclusions, queries, and stop condition.
4. Retrieve or emit the Deep Research continuation package.
5. Verify source identity and supporting passages; record citations through
   `references/citation-record-contract.md`, including inferred matches from
   incomplete user clues; record negative, inaccessible, conflicting, and
   access-limited evidence.
6. Label each material claim `supported | weak | conflicting | single-source |
   unverified | access-limited`. Give every internal ID a readable label and
   original source locator suitable for a node reference ledger.
7. Always build an Evidence Map. Build an Opportunity Map only for
   `evidence_and_opportunity` or `idea_landscape`. In the Opportunity Map,
   record `scientific_gap`, `novelty_positioning`, and an evidence-grounded
   `reader_reasoning_handoff` as separate objects.
8. For Idea work, emit evidence-grounded routing signals using
   `references/idea-direction-routing-signals.md`; do not choose or score an Idea.
9. On bounded-exploration remap, scope retrieval to one evolved dossier and
   return evidence/claim synchronization notes. Do not rewrite the dossier or
   introduce objectives, data, methods, or work packages.
10. Return concise pointers, route/mode, freshness, conflicts, limitations,
    unresolved gaps, and downstream consumers, not raw logs by default.
11. For a Deep Research return, separate report acceptance from retrieval
    routing and apply the repair ladder and owner-approval rule in
    `references/deep-research-prompt-rules.md`.

## Artifact Assembly

Write outputs serially in dependency order: required verification log, Evidence
Map, Opportunity Map, reader handoff, then routing signals. For a row-dense
artifact, write headings and metadata, source records in bounded groups,
claim/opportunity records in stable ID order, then limitations and handoff
fields. Keep it unavailable until a read-only check confirms required sections,
resolvable IDs, citations, and no placeholders.

Use one writer per artifact. If it becomes idle or makes no meaningful file
progress, retry only that incomplete artifact once with the same frozen reads
and preserve completed outputs. A passing artifact check completes the task;
do not wait for a separate final message from a stale delegate.

Terminology standardity, naturalness, first-use explanation, and replacement
recommendations belong to `academic-language-assessor`. Do not create a
terminology register or terminology-evidence packet here.

## Outputs

Emit the artifacts selected by the output profile: Evidence Map for every
profile; Opportunity Map for `evidence_and_opportunity`; and Evidence Map,
Opportunity Map, reader-reasoning handoff, and Idea direction signals for
`idea_landscape`. Evidence limitations and concise handoff notes stay inside
those artifacts. Emit a Search/verification log only for audit, conflict,
failure, or explicit request; an insufficiency report when reliable mapping is
impossible; and a Deep Research continuation package when required but inactive.

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
- Run `scripts/validate_deep_research_package.py` before returning a Deep
  Research continuation package.

## Completion Check

Confirm consumer/output profile, materiality/route/mode, source verification,
GB/T 7714—2015 citations with complete links, readable claim labels/locators,
the profile-required maps, distinct scientific-gap and novelty-positioning
objects when applicable, a five-function reader handoff for Idea work, visible
limits/conflicts, optional Idea routing/remap signals, a validated Deep Research
package and pause when applicable, persistence-safe assembly with a final
read-only consistency check, and no unsupported novelty, terminology verdict,
or Idea decision.
