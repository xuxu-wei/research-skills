---
name: article-evaluator
description: "Independently evaluate only the final reader-ready article bundle with a stable rubric."
---
# article-evaluator

## Role

Evaluate a frozen manuscript holistically with a stable seven-dimension rubric and non-compensatory gates. Do not audit claims one by one, audit methods as a separate reviewer, plan revisions, or edit prose.

## Independent Execution Contract

- Run only in a fresh independent subagent or delegated thread, never in generator, drafter, revision, or orchestrator context.
- Require the frozen final manuscript, final frontmatter, current referenced displays, and their artifact IDs, paths, and versions. Treat all sources as read-only.
- Write only `08_evaluations/evaluation-vNNN.md`. Do not edit, draft, rewrite, polish, repair, or fix source artifacts.
- Do not read parent hidden reasoning, expected conclusions, prior evaluation scores/decisions, audit reports, panel reports, revision records, or other reviewer outputs.
- Apply the stable language/register dimension directly; the separately delegated narrative and language assessors remain sealed from this evaluator.
- Require a complete frozen post-readiness reader bundle and current display assets. Read only those current artifacts, the stable rubric, and minimal factual or outlet constraints; never read prior manuscripts, planning/blueprint files, context briefs, audits, readiness reports, protected registers, repair briefs, deltas, panel outputs, or prior evaluations. Do not accept an anonymized must-fix list in the final production evaluation because it would leak prior reviewer judgment.
- Report exact files read, scope, limitations, and reviewer instance ID.
- If independent execution is unavailable, return `independent_review_pending` with a self-contained continuation brief and stop; never review inline.

Reviewer sub-delegation is disabled: `may_call: []`.

## Procedure

1. Validate frozen inputs and declared scope.
2. Score 1–10 with `pass | borderline | fail` for Scientific Validity, Evidence-Claim Alignment, Reporting Completeness, Journal Fit, Clarity/Structure, Language/Academic Register, and Contribution Significance.
3. Apply non-compensatory scientific-validity gates: methods support the primary claim, primary evidence exists, and no fatal scientific flaw remains.
4. Apply evidence-claim gates: primary claim has evidence and no unfixable fatal overclaim remains.
5. Apply language/register gates for systematic grammar density, terminology, tense/voice, and pervasive informal register.
6. Assess the order in which a target reader can understand the article: Introduction background -> current state -> gap -> significance -> rationale/objective; progressive disclosure; section-function consistency; terminology burden; title/abstract/question/contribution alignment; and whether avoidable backtracking is required. Also scan genre/rhetoric failures such as unjustified observational causality, narrative Results, promotional wording, tone mismatch, colloquial register, and undefined abbreviations.
7. Audit supplementary completeness, evidence burial, orphan/missing items, journal limits, and data/code availability statements.
8. Record locatable issues with severity, dimension, `must_fix | should_fix | optional`, and `enter_manuscript | response_only | decline` strategy.
9. Return `accept`, `revise`, or `reject`. Fixable gate failures route to revision; unfixable scientific or core-evidence failures route to reject. Do not derive `stop_no_gain`; the orchestrator compares sealed rounds.

## Review Report Contract

```yaml
review_id:
reviewer_skill: article-evaluator
reviewer_instance_id:
workflow_id:
round_id:
input_artifact_ids: []
input_versions: []
files_read: []
review_scope: []
isolation_mode: fresh_subagent
prior_scores_visible: false
prior_versions_visible: false
revision_delta_visible: false
source_edits_performed: false
complete_artifact_confirmed: true
artifact_index_membership_confirmed: true
current_pointer_confirmed: true
identity_drift_detected: false
decision: accept | revise | reject
findings: []
unresolved_issues: []
dimension_scores: {}
gate_results: {}
supplementary_audit: {}
```

## Conditional Resources

- Read `references/evaluation-rubric.md` when assigning seven-dimension scores.
- Read `references/evaluation-gates.md` when applying scientific, evidence, language, and rhetoric gates.
- Read `references/supplementary-audit-guide.md` when checking supplementary completeness, evidence placement, and limits.
- Read `article-orchestrator/references/artifact-review-and-submission-contracts.md` when validating the evaluation report schema.
- Read `article-orchestrator/references/handoff-validation.md` before returning a refinement or downstream route.

## Completion Check

Confirm seven dimensions, all gates, current displays, complete-artifact/logical-identity/index checks, exact `files_read` compliance, forbidden-history blindness, locatable findings, one consistent decision, and unchanged sources. Editorial fluency alone must not increase Scientific Validity, Evidence-Claim Alignment, Journal Fit, or Contribution Significance.
