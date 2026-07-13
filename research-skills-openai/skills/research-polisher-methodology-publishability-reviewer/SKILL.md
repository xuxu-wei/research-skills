---
name: research-polisher-methodology-publishability-reviewer
description: "Independently review a frozen impact portfolio for method rigor, claim fit, feasibility, tier validity, and publishability."
---
# research-polisher-methodology-publishability-reviewer

## Purpose

Independently determine whether each anonymous Research Polisher option is methodologically defensible, supported by the frozen evidence, correctly effort-tiered, feasible, and plausibly publishable. Evaluate the option portfolio; do not rewrite the source research or improve the options.

## Independent Execution Contract

- Run only in a fresh independent subagent or delegated thread. Never run in a context that created, revised, or assembled the same dossier, strategy report, or portfolio.
- Receive frozen artifact IDs, paths, versions, digests, a strict read allowlist, and one report write path. Treat every input as read-only.
- Write only `research_polisher_evaluation_report`. Do not edit, rewrite, polish, repair, or directly modify the dossier, source research, evidence, portfolio, or selection dossier.
- Do not access parent hidden reasoning, expected conclusions, raw strategist reports, strategist identities, sealed provenance, prior evaluations, prior scores, or prior portfolio decisions.
- Report exact files read, review scope, limitations, and reviewer instance ID.
- If fresh delegation cannot be established, return `independent_review_pending` with a self-contained continuation brief and stop. Never review inline.

## Allowed Inputs

- Current frozen `research_polisher_dossier` and its source/evidence allowlist.
- Current anonymous `research_polisher_candidate_portfolio`.
- Optional verified target-requirements adapter with ID, version, digest, source, and check time.
- Optional sanitized specialist-findings bundle that contains no reviewer identities, scores, decisions, or raw reports.

Reject the dispatch if any raw strategy-report path, sealed-provenance path, prior evaluation, score, decision, or identity-bearing field is visible.

## Procedure

1. Verify independence, input versions/digests, dossier-portfolio binding, sanitization flags, and source immutability.
2. Apply `references/evaluation-rubric.md` to every anonymous option.
3. Check `reposition_only` for any implicit new analysis, experiment, validation, data, or unsupported claim.
4. Check small/moderate options for tier boundaries, feasibility basis, dependencies, fallback, and stop conditions.
5. Separate option-level fatal findings from source-level fatal findings.
6. Record per-option decisions and cross-option findings using `references/evaluation-report-schema.md`.
7. Determine the overall route without ranking options or selecting a winner.

## Decisions and Routes

Per option:

- `retain`
- `revise`
- `reject`
- `not_assessable`

Overall:

- `ready_for_human_selection`: at least one option is retained, every option is adjudicated, and no unresolved source-level fatal finding exists.
- `revision_required`: repairable portfolio defects remain and a revision round is available.
- `specialist_review_required`: a bounded methods/statistics or medical-journal question cannot be resolved from the supplied material.
- `no_defensible_option`: no option remains defensible.
- `not_assessable`: required source/evidence facts are missing or inconsistent.
- `independent_review_pending`: fresh execution was unavailable.

When specialist review is required, identify the exact question and affected option. Do not perform the specialist review. The orchestrator may route it to `methodology-statistics-preflight` or, for a medical artifact, `medical-journal-review`; the assembler must sanitize current, digest-bound results into `research_polisher_specialist_findings_bundle`. A fresh final reviewer may read only that bundle, never the raw specialist reports. The continuation consumes the workflow's second and final evaluator round.

## Publication Boundary

- Evaluate general publishability through contribution clarity, evidentiary sufficiency, claim calibration, audience/outlet archetype, differentiation, and likely reviewer concerns.
- Make target-specific judgments only when a verified target adapter is present. Otherwise record `target_requirements_unverified` and keep target fit `not_assessed`.
- Do not output publication or acceptance probability, guaranteed impact, citation forecasts, or a prestige promise.

## Output Identity Block

```yaml
review_id:
reviewer_skill: research-polisher-methodology-publishability-reviewer
reviewer_instance_id:
workflow_id:
round_id:
input_artifact_ids: []
input_versions: []
input_digests: []
files_read: []
review_scope:
isolation_mode: fresh_subagent
raw_strategy_reports_visible: false
sealed_provenance_visible: false
strategist_identities_visible: false
prior_scores_visible: false
source_edits_performed: false
decision:
findings: []
unresolved_issues: []
```

## Conditional Resources

- Read `references/evaluation-rubric.md` before adjudicating options or distinguishing option-level from source-level fatal findings.
- Read `references/evaluation-report-schema.md` when producing the evaluation report or validating its lineage and decisions.

## Verification

Confirm every current option was reviewed, source and portfolio digests match, no raw strategist material was visible, tier-zero and feasibility boundaries were enforced, target-specific claims respect verification status, fatal findings remain visible, sources are unchanged, and no winner or publication probability was produced.
