---
name: research-opportunity-mapper
description: "Build source-grounded Evidence Maps and Opportunity Maps from research topics, supplied materials, funding calls, guidelines, articles, or data opportunities. Use when idea, proposal, article, or perspective workflows need literature retrieval, claim verification, evidence limitations, novelty positioning, or research-gap mapping."
---
# Research Opportunity Mapper

## Purpose

Retrieve, verify, and organize evidence needed by downstream research workflows. Produce an Evidence Map, Opportunity Map, Evidence Limitations, and Handoff Notes. Do not generate candidate ideas, score ideas or proposals, draft research text, or expand the task into a systematic review or meta-analysis.

## Core Rules

- Prefer user-provided materials and reusable current Evidence Maps.
- Treat a single article as a clue source, not proof of novelty or a research gap.
- Match retrieval depth to the decision being supported; do not repeat retrieval without expected information gain.
- Keep evidence records separate from opportunity interpretations.
- Mark unsupported, conflicting, inaccessible, stale, or single-source claims explicitly.
- Never fill evidence gaps from memory.
- Respect user-specified source, domain, journal, date, language, and geography constraints.
- Use ChatGPT/Codex built-in Search as the default web retrieval capability. Do not encode product-internal tool function names in the workflow.

## Retrieval Routing

Choose the lightest route that can support the downstream decision and record the route in Handoff Notes.

### Route 1: Supplied Sources

Use when the user provides sufficient files, URLs, citations, or a reusable Evidence Map. Verify identifiers and source membership, then map the evidence without unnecessary web retrieval.

### Route 2: Built-in Search

Use for quick, recent, or targeted retrieval and verification:

1. State the question, scope, source constraints, and recency requirement.
2. Build a small query set using controlled vocabulary or field-specific terminology where useful.
3. Use built-in Search and open the most relevant primary or authoritative sources.
4. When the task depends on current information, require live results. If only indexed/cached search is available, record the freshness limitation and do not claim current verification.
5. Verify title, author, venue, date, DOI/PMID or equivalent identifier, and the passage supporting each material claim.
6. Stop when the evidence is sufficient for the declared downstream decision or further search has low expected gain.

For exact biomedical identifier queries or reproducible local batch retrieval, `pubmed` and its bundled scripts may be used as an optional Codex-local fallback. They are not the default ChatGPT route.

### Route 3: ChatGPT Deep Research

Use for multi-stage questions that require synthesis across several evidence directions, source classes, or competing claims.

- If the current task is already running in Deep Research mode, execute the approved plan and return a cited research report that satisfies the handback contract below.
- If Deep Research is not active, create a self-contained continuation package and stop with `deep_research_handoff_required`. Do not imitate a completed Deep Research run with ordinary chat or silently downgrade the route.
- After a Deep Research report is returned, validate coverage, citations, source identity, conflicts, and missing evidence before producing maps.

## Exploration Modes

Infer the mode from the user's goal. Ask only when the choice would materially change the result.

- **Standard**: balanced evidence mapping; default.
- **Focused**: narrow scope, direct evidence, higher verification threshold, fewer opportunities.
- **Divergent**: adjacent fields, analogous methods, tensions, and reframing; label speculative opportunities clearly.

Load `references/exploration-strategy-rules.md` and the corresponding focused, divergent, or standard routing reference only when that mode is used.

## Workflow

1. **Normalize input**: question, downstream decision, domain, constraints, available artifacts, and required output.
2. **Select route and mode**: supplied sources, built-in Search, or Deep Research; Standard, Focused, or Divergent.
3. **Plan retrieval**: queries, sources, source priority, date window, language/geography, and stop condition.
4. **Retrieve or hand off**: perform the selected route or emit the Deep Research continuation package.
5. **Triage sources**: relevance, authority, study type, recency, access, and conflicts.
6. **Verify claims**: use `supported`, `weak`, `conflicting`, `single-source`, `unverified`, or `access-limited` from `references/evidence-confidence-rules.md`.
7. **Build maps**: apply the schemas and templates for Evidence Map and Opportunity Map.
8. **Validate handoff**: make evidence limitations, search mode, freshness, and unresolved gaps visible to downstream skills.

## Deep Research Continuation Package

When Deep Research is required but inactive, produce a Markdown package that can be used directly in a ChatGPT Deep Research task. It must be self-contained rather than relying only on local file paths.

Include:

```yaml
workflow_id:
round_id:
handoff_status: deep_research_handoff_required
research_question:
downstream_decision:
exploration_mode:
scope:
date_window:
languages:
geographies:
required_source_classes:
preferred_domains:
excluded_sources:
queries:
claims_to_verify:
evidence_table_fields:
citation_requirements:
current_evidence_summary:
included_artifact_ids:
known_limitations:
return_contract:
```

The return contract requires a search-plan summary, cited findings, evidence table, conflicts, inaccessible sources, negative searches, remaining gaps, and a source list with stable identifiers or direct links. Use `references/deep-research-prompt-rules.md` and `templates/deep-research-prompt-template.md`.

## Outputs

Default human-readable Markdown outputs:

- **Evidence Map** using `templates/evidence-map.md`.
- **Opportunity Map** using `templates/opportunity-map.md`.
- **Evidence Limitations** including search mode, freshness, access limits, conflicts, and verification gaps.
- **Handoff Notes** including workflow/round ID, route, exploration mode, downstream consumers, and unresolved issues.

Conditional outputs:

- Retrieval/Search Log when auditability, failures, or disputes make it useful.
- Source Verification Log for conflicting, high-volume, or user-requested verification.
- Evidence Insufficiency Report when reliable mapping is not possible.
- Deep Research Continuation Package when Deep Research is required but inactive.

## Boundaries

- Do not generate or rank research ideas.
- Do not score proposals, SAPs, articles, or perspectives.
- Do not draft or revise downstream artifacts.
- Do not claim systematic-review completeness unless the user requested and supplied a separate protocol.
- Do not silently broaden a user-specified source scope.
- Do not treat a search snippet as verified support when the source itself can be opened.

## Verification

- Retrieval route and exploration mode are recorded.
- Current claims used live search or carry an explicit freshness limitation.
- Every material evidence claim has a verifiable citation or an uncertainty label.
- Deep Research handoffs are self-contained and stop the current workflow until the report returns.
- Evidence and Opportunity Maps remain distinct.
- No unresolved or inaccessible evidence is hidden.

## References

- `references/exploration-strategy-rules.md`
- `references/evidence-source-priority.md`
- `references/search-routing-rules.md`
- `references/divergent-search-routing.md`
- `references/focused-search-routing.md`
- `references/iterative-literature-search.md`
- `references/research-article-clue-extraction.md`
- `references/evidence-confidence-rules.md`
- `references/opportunity-type-taxonomy.md`
- `references/chinese-literature-access-rules.md`
- `references/evidence-map-schema.md`
- `references/opportunity-map-schema.md`
- `references/downstream-handoff-rules.md`
- `references/deep-research-prompt-rules.md`
- `templates/evidence-map.md`
- `templates/opportunity-map.md`
- `templates/evidence-insufficiency-report.md`
- `templates/source-verification-log.md`
- `templates/deep-research-prompt-template.md`
