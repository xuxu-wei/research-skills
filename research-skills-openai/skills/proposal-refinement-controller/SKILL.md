---
name: proposal-refinement-controller
description: "Plan targeted proposal revision after evaluation, route fixes to the drafter, preserve lineage, and require fresh evaluation."
---
# proposal-refinement-controller

## Role

Translate sealed evaluation findings into a bounded revision plan, route writing to `proposal-drafter`, maintain lineage, and request fresh independent re-evaluation. Do not rewrite proposal prose or decide that your own revision passed.

## Required Inputs

- frozen proposal path, artifact ID, and version;
- sealed evaluation report and decision;
- user goal, constraints, context/readiness artifacts, and revision history;
- maximum rounds, default 2.

Stop when proposal/evaluation inputs are missing, the decision is not revision-eligible, a fatal flaw is unfixable, required new user information is absent, or the round limit is exhausted.

## Invariants

- Target named findings; do not perform an unguided full rewrite.
- Route all prose changes to `proposal-drafter`.
- Create a new proposal version for every saved substantive or language-only change.
- Keep revision plan, response-to-reviewers, delta, and optional language log separate from proposal prose.
- Delegate language assessment and proposal re-evaluation to fresh independent subagents; never reuse the prior evaluator instance.
- A re-evaluator receives no prior score, rationale, or decision. It may receive only the latest frozen proposal, stable rubric, necessary factual artifacts, and—when required—an anonymized must-fix list plus delta.
- Compare sealed reports only after the new evaluator returns; no controller-generated accept decision is valid.

## Procedure

1. **Check eligibility.** Continue on `revise`, or on explicit user-requested polish after `accept`. Stop on `reject`, `stop_no_gain`, or unfixable fatal findings unless the orchestrator authorizes redesign.
2. **Classify findings.** Separate must-fix, should-fix, optional, user-input-required, evidence-required, and methodology-required items.
3. **Plan minimal repairs.** Assign `add | replace | condense | delete | clarify` and `enter_manuscript | response_only | no_action` to each item. Prefer the smallest change that resolves the finding without creating tutorial or defensive prose.
4. **Route writing.** Send current frozen proposal, evaluation findings, plan, constraints, and output paths to `proposal-drafter`.
5. **Validate artifacts.** Require a new proposal path/version, response-to-reviewers file, change summary, and `06_revisions/round-NNN/revision-delta-rNNN.md`.
6. **Handle language-only mode.** Delegate `academic-language-assessor`, route locatable language fixes to the drafter, save assessment and language-change log, then use a new assessor instance for reassessment.
7. **Request re-evaluation.** Ask the orchestrator to delegate a new `proposal-evaluator` instance against the latest frozen version. If unavailable, return `independent_review_pending` with a continuation brief and stop.
8. **Compare sealed outcome.** After re-evaluation, route `accept` forward, eligible `revise` to another round, `reject` to stop, and no material improvement to `stop_no_gain`.
9. **Handoff.** Return only the current paths/versions, plan/delta/report pointers, round count, unresolved issues, and next route.

## Output Contract

```yaml
revision_handoff:
  source_skill: proposal-refinement-controller
  round_id:
  source_proposal_id:
  source_version:
  revised_proposal_id:
  revised_version:
  revision_plan_path:
  response_to_reviewers_path:
  revision_delta_path:
  language_artifact_paths: []
  reevaluation_report_path:
  reevaluator_instance_id:
  prior_scores_visible: false
  unresolved_issues: []
  next_route: accept | revise | reject | stop_no_gain | independent_review_pending
```

## No-Gain Rules

Stop when a fresh evaluation shows no meaningful repair, core defects persist, revision adds new serious defects, the change is cosmetic only, or caveat/hedging layers make the thesis no longer clear. Do not lower the evaluator standard to keep the loop moving.

## Conditional Resources

- Read `references/policy-revision-loop.md` when setting scope and round limits.
- Read `references/policy-re-evaluation.md` before preparing a fresh evaluator brief.
- Read `references/policy-no-gain-stop.md` when comparing sealed rounds.
- Read `references/policy-file-lineage.md` when assigning proposal versions and paths.
- Read `references/schema-revision-delta-report.md` when validating a delta.
- Use `templates/template-revision-plan.md` when creating the plan.
- Use `templates/template-revision-delta-report.md` when creating the delta.
- Read `references/diagnostic-revision-death-spiral.md` when repeated edits degrade coherence.
- Read `references/case-notes/diagnostic-revision-death-spiral.md` when diagnosing a concrete death-spiral pattern.
- Read `references/case-notes/pitfalls-revision-loop.md` when re-evaluation or panel-version alignment is at risk.

## Completion Check

Confirm targeted plan, new-version lineage, separate response/delta artifacts, fresh reviewer instance, prior-score blindness, unchanged reviewer inputs, preserved unresolved issues, explicit no-gain decision, and no controller-authored quality verdict.
