---
name: research-opportunity-mapper
description: "Build source-grounded evidence and opportunity maps. Use for broad retrieval, claim verification, novelty positioning, evidence limits, and research gaps."
---
# research-opportunity-mapper

## Role

Act as the plugin's single owner of broad retrieval policy. Retrieve, verify, and organize evidence for downstream decisions; produce separate Evidence and Opportunity Maps, limitations, and handoff notes. Do not generate/rank ideas, score artifacts, draft downstream prose, or imply systematic-review completeness without a separate protocol.

## Routing

1. **Supplied sources:** use when files, URLs, citations, or a reusable in-scope Evidence Map are sufficient; verify identifiers and source membership.
2. **Built-in Search:** default for quick, recent, exact, or targeted retrieval. State scope/recency, query primary or authoritative sources, open them, verify identity and supporting passages, and stop at decision sufficiency or low expected gain.
3. **Deep Research:** use for multi-stage, multi-direction, multi-source synthesis. If active, run the approved plan; if inactive or unknown, return `deep_research_handoff_required` with a self-contained continuation package and stop. Do not imitate Deep Research with ordinary chat.

For exact biomedical identifiers, use built-in Search scoped to PubMed/NCBI. Local scripts are never the default ChatGPT route.

## Procedure

1. Normalize question, downstream decision, domain, constraints, supplied artifacts, freshness, and output needs.
2. Select supplied/Search/Deep Research route and `standard | focused | divergent` exploration mode.
3. Plan queries, source classes, source priority, date/language/geography bounds, exclusions, and stop condition.
4. Retrieve, or emit and stop at the Deep Research continuation package.
5. Triage relevance, authority, study type, recency, access, conflicts, and source identity.
6. Label each material claim `supported | weak | conflicting | single-source | unverified | access-limited`; never fill gaps from memory or snippets alone.
7. Build distinct Evidence and Opportunity Maps with stable citations/identifiers.
8. Return concise artifact pointers, route/mode, freshness, negative searches, conflicts, limitations, unresolved gaps, and downstream consumers—not raw logs by default.

## Deep Research Continuation Contract

Include workflow/round IDs, `handoff_status: deep_research_handoff_required`, research question, downstream decision, mode, scope, dates, languages/geographies, required/preferred/excluded sources, queries, claims to verify, evidence fields, citation requirements, current evidence summary, included artifact IDs, limitations, and return contract. The returned report must contain plan summary, cited findings, evidence table, conflicts, inaccessible/negative searches, remaining gaps, and stable source links/IDs.

## Outputs

- Evidence Map, Opportunity Map, Evidence Limitations, and Handoff Notes.
- Search log only for audit, dispute, failure, or explicit request.
- Source Verification Log for conflicting/high-volume/user-requested verification.
- Evidence Insufficiency Report when reliable mapping is impossible.
- Deep Research Continuation Package when required but inactive.

## Conditional Resources

- Read routing references when selecting mode/route: `references/exploration-strategy-rules.md`, `references/search-routing-rules.md`, `references/focused-search-routing.md`, `references/divergent-search-routing.md`, `references/iterative-literature-search.md`.
- Read source/claim rules when prioritizing and grading evidence: `references/evidence-source-priority.md`, `references/evidence-confidence-rules.md`, `references/chinese-literature-access-rules.md`.
- Read opportunity/design references when interpreting gaps: `references/opportunity-type-taxonomy.md`, `references/design-pattern-strategy-routing.md`, `references/research-article-clue-extraction.md`.
- Read schemas and handoff rules when creating maps: `references/evidence-map-schema.md`, `references/opportunity-map-schema.md`, `references/downstream-handoff-rules.md`.
- Read `references/deep-research-prompt-rules.md` when Deep Research is selected.
- Use output templates when producing named artifacts: `templates/evidence-map.md`, `templates/opportunity-map.md`, `templates/evidence-insufficiency-report.md`, `templates/source-verification-log.md`, `templates/deep-research-prompt-template.md`.
- Run `scripts/evidence_search.py` only when the user explicitly requests reproducible local batch retrieval in Codex.

## Completion Check

Confirm recorded route/mode, live verification or freshness limitation, opened sources for material claims, separate maps, visible conflict/access limits, self-contained Deep Research pause when needed, and no unsupported novelty/gap conclusion.
