---
name: proposal-refinement-controller
description: "Normalize proposal findings into one writer interface, verify preservation, and require fresh review."
---
# proposal-refinement-controller

## Role

Turn sealed scientific findings into a bounded revision plan, or materialize the orchestrator's editorial decisions as one protected brief. Route prose to `proposal-drafter`, maintain lineage, validate execution, and request fresh independent reassessment. Do not select actions, resolve conflicts, rewrite prose, or decide that revision passed.

## Required Inputs

- frozen proposal path, artifact ID, and version;
- scientific revision: sealed evaluation/decision, goal, constraints, allowed context/readiness facts, and history;
- editorial repair: approved included IDs and conflict/exclusion decisions, frozen narrative/language actions, reader handoff, constraints, protected register, and target paths;
- maximum rounds, default 2.

Stop when proposal/evaluation inputs are missing, the decision is not revision-eligible, a fatal flaw is unfixable, required user information is absent, or the round limit is exhausted.

## Invariants

- Target named findings; do not perform an unguided full rewrite. Route all prose changes to `proposal-drafter`.
- Every saved substantive, structural, editorial-only, language-only, or formatting-only change creates a new version. Keep plan, response, delta, and action-execution artifacts outside prose.
- Delegate assessment, preservation, reassessment, and re-evaluation to fresh independent instances; never reuse the prior assessor/evaluator.
- A non-final scientific re-evaluator receives only the latest frozen proposal, stable rubric, necessary facts, and optionally an anonymized must-fix list. The final evaluator receives no list. Neither receives prior proposals, context/readiness, repair/delta/editorial artifacts, scores, rationale, or decisions.
- Compare sealed reports only after new evaluation; the controller cannot accept or derive `stop_no_gain`.
- Keep scientific and editorial modes separate. Editorial actions cannot change novelty, feasibility, impact, methods, estimands, endpoints, evidence, claim strength, or substantive risk posture.
- Materialize one `editorial-repair-brief-rNNN.yaml` without expanding the orchestrator's decision. The writer reads only it, the complete proposal, and protected register—not raw or other review reports.
- Use one editorial writer for bounded section passes and one complete target. Validate every action before freeze.
- After editorial repair, require fresh preservation plus fresh narrative/language reassessments by instances different from the original assessors and writer.

## Procedure

1. **Select mode and eligibility.** Use `scientific_revision` for `revise`; use `editorial_repair` only after scientific/method eligibility and parallel narrative/language assessment. Stop on `reject`, `stop_no_gain`, unfixable fatal findings, or scientific choices disguised as editorial actions.
2. **Classify findings.** Separate must-fix, should-fix, optional, user-input-required, evidence-required, and methodology-required items.
3. **Plan minimal scientific repairs.** Assign each finding `add | replace | condense | delete | clarify` and `enter_proposal | response_only | no_action`. Prefer the smallest effective change.
4. **Route scientific writing.** Give `proposal-drafter` the current frozen proposal, controller-authored plan, constraints, and output paths; keep the raw report outside proposal prose.
5. **Validate scientific artifacts.** Require a new proposal path/version, response file, change summary, and `06_revisions/round-NNN/revision-delta-rNNN.md`.
6. **Materialize editorial normalization.** After both action sets are sealed, receive the orchestrator's decisions. Read records only to preserve fields, deduplicate approved overlaps, and order dependencies. Add no action or conflict decision. Write `templates/template-editorial-repair-brief.yaml`.
7. **Route protected editorial writing.** Give one drafter only the brief, current complete proposal, and protected register. Keep the same writer for bounded passes and one complete target.
8. **Validate action conformance before freeze.** Compare brief, complete target, and `editorial-action-execution-rNNN.yaml`. Every included action needs evidence or an explicit block; return omissions to the same writer. This is contract validation, not scoring.
9. **Preserve and reassess.** After freeze, delegate fresh preservation and separate fresh narrative/language reassessments. Preservation failure or scientific change returns to scientific review; remaining editorial actions start a new editorial round.
10. **Request final evaluation.** Ask the orchestrator for a fresh evaluator using only the latest complete frozen proposal, stable rubric, and minimal call/factual inputs. If unavailable, return `independent_review_pending` with a continuation brief and stop.
11. **Return sealed results.** Give the orchestrator the fresh decision and current-round facts. Only it compares rounds, derives `stop_no_gain`, and routes `accept | revise | reject`.
12. **Handoff.** Return only current identities/paths/versions, plan/editorial pointers, round count, unresolved issues, and next route.

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
  reader_handoff_path:
  protected_content_register_path:
  editorial_repair_brief_path:
  editorial_action_execution_path:
  preservation_report_path:
  narrative_reassessment_path:
  language_reassessment_path:
  reevaluation_report_path:
  reevaluator_instance_id:
  prior_scores_visible: false
  unresolved_issues: []
  next_route: accept | revise | reject | stop_no_gain | independent_review_pending
```

## No-Gain Rules

Report scientific no-gain evidence when fresh evaluation shows no meaningful repair, core defects persist, new serious defects appear, or an editorial change leaves the scientific finding. Only the orchestrator stops for no gain. In editorial repair, stop or ask for clarification when actions require scientific change, preservation repeatedly fails, or fresh reassessment shows no functional gain. Never lower evaluator/assessor standards.

## Conditional Resources

- Read `references/policy-revision-loop.md` when setting scope and round limits.
- Read `references/policy-re-evaluation.md` before preparing a fresh evaluator brief.
- Read `references/policy-no-gain-stop.md` when comparing sealed rounds.
- Read `references/policy-file-lineage.md` when assigning proposal versions and paths.
- Read `references/schema-revision-delta-report.md` when validating a delta.
- Use `templates/template-revision-plan.md` and `templates/template-revision-delta-report.md` for their named artifacts.
- Read `references/policy-editorial-repair.md` before materializing or validating editorial repair.
- Use `templates/template-protected-content-register.yaml`, `templates/template-editorial-repair-brief.yaml`, and `templates/template-editorial-action-execution.yaml` for their named artifacts.
- Read `references/diagnostic-revision-death-spiral.md` when repeated edits degrade coherence.
- Read `references/case-notes/diagnostic-revision-death-spiral.md` when diagnosing a concrete death-spiral pattern.
- Read `references/case-notes/pitfalls-revision-loop.md` when re-evaluation or panel-version alignment is at risk.

## Completion Check

Confirm mode separation, targeted scientific plan or one materialized editorial brief, protected content, same-writer/complete-target repair, action conformance before freeze, fresh preservation/reassessment, new-version lineage, separate response/delta artifacts, final-evaluator isolation, preserved unresolved issues, orchestrator-owned no-gain routing, and no controller verdict.
