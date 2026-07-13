---
name: research-polisher-plan-assembler
description: "Assemble sealed Research Polisher reports into an anonymous portfolio without scoring, inventing options, or hiding dissent."
---
# research-polisher-plan-assembler

## Purpose

Mechanically assemble Research Polisher artifacts without judging, scoring, ranking, rewriting, or selecting an option. Run in candidate-portfolio, revision-brief, specialist-findings, or final-selection mode as directed by the orchestrator.

## Inputs and Writes

Treat the research dossier and source research as read-only. Read only the artifacts required for the selected mode:

- `candidate_portfolio`: three sealed strategy reports plus dossier/evidence lineage;
- `revision_brief`: current anonymous portfolio, its independent evaluation, and the sealed provenance index used only to map affected anonymous options back to perspectives and tiers;
- `specialist_findings`: requested specialist reports plus their frozen input lineage;
- `selection_dossier`: latest anonymous portfolio plus its current independent evaluation and recorded unresolved issues.

Write only the declared assembler outputs under `04_portfolios/`, `05_evaluations/`, `06_revisions/`, or `07_delivery/`. Never modify source research, evidence, strategy reports, specialist reports, or evaluation reports.

## Candidate Portfolio Procedure

1. Verify three distinct strategist instance IDs, one for each required perspective.
2. Verify each report references the same frozen dossier/evidence digests and accounts for all three effort tiers.
3. Reject partial, stale, identity-overlapping, or peer-visible report sets.
4. Normalize option fields and assign anonymous portfolio option IDs.
5. Group substantively equivalent options without creating a hybrid. Keep disagreements, incompatibilities, limitations, and `no_defensible_option` cells.
6. Write an evaluator-visible anonymous `research_polisher_candidate_portfolio-vNNN` and a separate sealed provenance index.

The anonymous portfolio must omit reviewer identities, raw report paths, prior decisions, scores, and cluster frequency. The sealed index retains the complete source mapping for lineage verification.

## Revision Brief Procedure

Mechanically convert evaluator `revise` findings into an anonymous must-fix list grouped by affected option, perspective, and tier. Use the sealed provenance index only for routing; do not copy identities, raw paths, cluster frequency, or provenance into the brief. Copy finding scope and required evidence; do not reinterpret severity, propose repairs, or reveal scores, decisions, identities, or raw reports.

## Specialist Findings Procedure

Verify that every specialist report answers a question explicitly requested by the current final evaluation and is bound to the same dossier and portfolio digest. Produce `research_polisher_specialist_findings_bundle` containing only the requested question, affected anonymous option IDs, source-grounded findings, limitations, and input digests. Remove reviewer identity, scores, decisions, raw report paths, and unrelated findings. This bundle may be read only by a new final-reviewer instance; it cannot itself promote a portfolio.

## Selection Dossier Procedure

1. Verify the evaluation covers the current portfolio version and source digest.
2. Copy per-option decisions and findings without softening them.
3. Preserve rejected and not-assessable options in an appendix.
4. Present retained options across declared axes: effort, feasibility, methodological risk, scientific-significance potential, practical-value potential, dissemination potential, and publication positioning.
5. Mechanically identify non-dominated retained options. Do not apply weights, compute an aggregate score, or name an automatic winner.
6. Carry all dissent, target-verification limits, fatal findings, unresolved issues, and lineage into the dossier.

Set `selection_status: human_strategy_selection_required` only when at least one option is retained, all current options are adjudicated, and no unresolved source-level fatal finding exists.

## Prohibited Actions

- Do not invent, combine, extend, repair, or rewrite a strategy.
- Do not score, rank, promote, reject, or change an evaluator decision.
- Do not infer consensus from duplicate count or hide minority options.
- Do not expose raw strategy reports, raw specialist reports, or sealed provenance to the final reviewer.
- Do not remove a limitation, dissent item, fatal finding, or unknown target requirement.
- Do not emit a human-selection status for a stale or incompletely reviewed portfolio.

## Failure States

- Missing perspective or tier -> `assembly_blocked_incomplete_matrix`.
- Dossier/evidence digest mismatch -> `assembly_blocked_stale_input`.
- Reviewer identity reuse or peer visibility -> `assembly_blocked_isolation_failure`.
- Current evaluation missing or stale -> `independent_review_pending`.
- No retained option -> `no_defensible_option`.

Return the failure report and missing requirements; never fill a gap with invented content.

## Output

Return only a concise phase summary and pointers to the new artifact and sealed lineage. Follow `references/assembly-contract.md` for schemas and sanitization checks.

## Conditional Resource

- Read `references/assembly-contract.md` before creating or validating a candidate portfolio, sealed provenance index, revision brief, Pareto view, or selection dossier.

## Verification

Confirm matrix completeness, source/digest consistency, identity separation, anonymous evaluator input, complete sealed lineage, sanitized specialist findings when used, visible dissent, current evaluation coverage, zero source edits, zero new strategies, and no automatic winner.
