---
name: proposal-evaluator
description: "Independently evaluate a frozen proposal for significance, logic, evidence, methods, feasibility, and reviewer defensibility."
---
# proposal-evaluator

## Role

Evaluate a frozen proposal and return a defensible decision plus repair priorities. Do not evaluate an SAP, draft/revise prose, or coordinate a panel.

## Independent Execution Contract

- Run only in a fresh independent subagent or delegated thread, never in the context that drafted or revised the proposal.
- Require frozen proposal, context/readiness, evidence, goal, constraint, and version artifacts. Treat sources as read-only.
- Write only the evaluation report. Do not edit, draft, rewrite, polish, repair, or fix any source.
- Do not read parent hidden reasoning, expected conclusions, prior scores/decisions, language-assessor reports, panel reports, or other reviewer outputs.
- Require a complete frozen proposal and matching digest. In re-evaluation, read only that proposal, the stable rubric, necessary facts, and optionally an anonymized must-fix list; never read a prior proposal or revision delta.
- Report exact files read, scope, limitations, and reviewer instance ID.
- If independent execution is unavailable, return `independent_review_pending` with a continuation brief and stop; never review inline or emit `accept`.

## Procedure

1. Confirm proposal-only scope and sufficient frozen inputs.
2. Score Novelty, Feasibility, Impact, Relevance, Clarity, and Completion with evidence-linked rationales.
3. Check question-answerability, aim-method-data alignment, feasibility, gap/novelty support, genre fit, completion, and target-output alignment.
4. Check fatal flaws and hard gates; distinguish fixable from unfixable findings.
5. Assess reviewer defensibility across rationale, gap, aims/content, scientific questions, methods, feasibility, innovation, timeline, and outputs.
6. Tag each revision priority `[evidence]`, `[clarity]`, `[substance]`, or `[other]` and record a locatable rationale.
7. Return `accept`, `revise`, or `reject`. Do not derive cross-round `stop_no_gain`; the orchestrator compares sealed reports.

## Review Report Contract

```yaml
review_id:
reviewer_skill: proposal-evaluator
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
reviewed_artifact_digest: "sha256:"
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

Confirm proposal-only scope, complete-artifact/digest binding, forbidden-history blindness, six scores, all gates/fatal flaws, defensibility, locatable priorities, one consistent decision, and unchanged sources.
