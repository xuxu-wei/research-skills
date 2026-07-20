---
name: proposal-evaluator
description: "Evaluate only the final reader-ready proposal with a stable rubric."
---
# proposal-evaluator

## Role

Evaluate a frozen proposal and return a defensible decision plus repair priorities. Do not evaluate an SAP, draft/revise prose, or coordinate a panel.

## Independent Execution Contract

- Run only in a fresh independent subagent or delegated thread, never in the context that drafted or revised the proposal.
- Require the frozen proposal plus the stable rubric and only minimal call requirements or factual inputs needed to judge it. Treat sources as read-only; do not read context/readiness reports or other reviewer outputs.
- Write only the evaluation report. Do not edit, draft, rewrite, polish, repair, or fix any source.
- Do not read parent hidden reasoning, expected conclusions, prior scores/decisions, language-assessor reports, panel reports, or other reviewer outputs.
- Require one complete frozen proposal bound by logical artifact ID, path, and version. Do not require, compute, or persist a hash or digest; accept a legacy digest field only as ignored metadata.
- In non-final scientific reassessment, an optional anonymized must-fix list may be allowed. In final evaluation, read only the revised final proposal, stable rubric, and minimal call/factual inputs—never an anonymized list or any old draft, context/readiness report, repair brief, delta, preservation/editorial report, or prior evaluation.
- Report exact files read, scope, limitations, and reviewer instance ID.
- If independent execution is unavailable, return `independent_review_pending` with a continuation brief and stop; never review inline or emit `accept`.

## Procedure

1. Confirm proposal-only scope and sufficient frozen inputs.
2. Score Novelty, Feasibility, Impact, Relevance, Clarity, and Completion with evidence-linked rationales. Editorial polish may affect Clarity only; it cannot raise Novelty, Feasibility, or Impact without new substantive support in the proposal.
3. Check question-answerability, aim-method-data alignment, feasibility, gap/novelty support, genre fit, completion, and target-output alignment.
4. For Clarity, trace the target reader's chain from problem through current knowledge, gap, significance, and design rationale. Check progressive disclosure, each section's rhetorical function and handoff, and terminology burden. Fail the Clarity gate when significance is missing or the gap-to-rationale transition is broken.
5. Confirm assumptions, feasibility, risks, and conditional method assumptions have one authoritative location; do not demand duplicated limitations unless a local boundary is necessary to prevent distortion of the immediately connected logic.
6. Check fatal flaws and hard gates; distinguish fixable from unfixable findings.
7. Assess reviewer defensibility across rationale, gap, aims/content, scientific questions, methods, feasibility, innovation, timeline, and outputs.
8. Tag each revision priority `[evidence]`, `[clarity]`, `[substance]`, or `[other]` and record a locatable rationale.
9. Return `accept`, `revise`, or `reject`. Do not derive cross-round `stop_no_gain`; the orchestrator compares sealed reports.

## Review Report Contract

```yaml
review_id:
reviewer_skill: proposal-evaluator
reviewer_instance_id:
workflow_id:
round_id:
input_artifact_ids: []
input_versions: []
reviewed_proposal_ref:
  artifact_id:
  version:
  path:
files_read: []
review_scope: []
evaluation_stage: initial_scientific | scientific_reassessment | final_scientific
isolation_mode: fresh_subagent
prior_scores_visible: false
prior_versions_visible: false
revision_delta_visible: false
readiness_report_visible: false
repair_artifacts_visible: false
prior_evaluation_visible: false
source_edits_performed: false
complete_artifact_confirmed: true
decision: accept | revise | reject
findings: []
unresolved_issues: []
dimension_scores: {}
hard_gates: {}
fatal_flaws: []
revision_priorities: []
```

## Conditional Resources

- Read `references/rubric-proposal-evaluation.md` when scoring the six dimensions.
- Read `references/gates-proposal-hard-gates.md` when applying minimum gates.
- Read `references/criteria-fatal-flaws.md` when classifying fatal findings and fixability.
- Read `references/policy-reviewer-defensibility.md` when assessing likely review attacks.
- Read `references/policy-re-evaluation.md` when preparing a fresh evaluation scope.
- Read `references/schema-proposal-evaluation-report.md` when validating report fields.
- Use `templates/template-proposal-evaluation-report.md` when producing the report.

## Completion Check

Confirm proposal-only scope, logical artifact binding, forbidden-history blindness, final-stage input minimization when applicable, six scores with editorial/scientific separation, reader-chain clarity, all gates/fatal flaws, defensibility, locatable priorities, one consistent decision, and unchanged sources.
