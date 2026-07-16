---
name: idea-adversarial-review-panel
description: "Independently challenge a frozen promoted idea in one assigned novelty, feasibility, or strategy role before proposal handoff."
---
# Idea Adversarial Review Panel

## Role

Challenge a qualifying focused Idea's Proposal-handoff readiness from one
assigned role. Do not generate/revise Ideas, assign six-dimension scores, alter
evaluator decisions, or draft proposal text.

## Independent Execution Contract

- Run each role in a distinct fresh subagent/delegated thread, never a context
  that generated, revised, or evaluated the Idea.
- Accept frozen IDs, versions, exact paths, and digests. Inputs are read-only;
  write only one role report.
- Do not read prior evaluator scores/findings/decisions, another reviewer output,
  expected conclusions, or parent hidden reasoning.
- Do not draft, rewrite, polish, fix, merge, or reframe the dossier.
- Report exact files read, assigned scope, reviewer instance ID, and digest.
- If a fresh instance is unavailable, return `independent_review_pending` with a
  continuation brief and stop; never review inline.

## Roles and Inputs

Dispatch novelty/gap skeptic, feasibility/method skeptic, and PI-strategy
reviewer concurrently. Read `references/reviewer-role-definitions.md` for role
scope. Each may receive the frozen dossier and only role-necessary context,
maps, evidence limits, preflight, user constraints, workflow confirmation that
evaluation completed without its findings/scores, and the node reference ledger.

## Procedure

1. Validate current dossier digest, qualifying evaluation completion, role
   isolation, and role-specific frozen inputs.
2. Attack handoff readiness only. Do not rescore or repair.
3. Give every finding a human-readable title and `dossier_locator`. If an
   internal ID is necessary, display `ID: human-readable label` and verify that
   it resolves through the supplied ledger; never show a naked ID.
4. Classify findings `blocking | major | minor | not_blocking` and return an
   upstream route plus unresolved issues.
5. The orchestrator waits for all roles, verifies their instance IDs are
   pairwise distinct, then aggregates without suppressing conflict or dissent.

## Role Report

```yaml
review_id:
reviewer_skill: idea-adversarial-review-panel
reviewer_instance_id:
reviewer_role:
workflow_id:
round_id:
input_artifact_ids: []
input_versions: []
files_read: []
reviewed_dossier_digest: "sha256:"
review_scope:
isolation_mode: fresh_subagent
prior_scores_visible: false
prior_versions_visible: false
revision_delta_visible: false
evaluator_findings_visible: false
peer_outputs_visible: false
source_edits_performed: false
decision:
findings:
  - title:
    dossier_locator:
    internal_reference_with_label:
    severity:
    rationale:
unresolved_issues: []
```

Allowed recommendations: `handoff_ready`, `conditional_handoff`,
`return_to_evidence_mapping`, `return_to_methodology_preflight`,
`return_to_generation_or_reframe`, `return_to_independent_evaluation`, or
`do_not_handoff`.

## Stops and Handoff

Stop on missing qualifying evaluation, digest mismatch, incomplete role inputs,
or unavailable delegation. Blocking findings route upstream; reviewers never
perform the repair. This panel is not used to preselect a bounded-exploration
winner; that route stops for human direction selection.

## Conditional Resources

- Read `references/reviewer-role-definitions.md` when assigning or executing a role.
- Read `research-idea-orchestrator/references/idea-dossier-contract.md` when
  locating dossier claims/evidence chains.
- Read `research-idea-orchestrator/references/reference-ledger-contract.md` when
  a report needs an internal identifier.
- Read `research-idea-orchestrator/references/artifact-contracts.md` for shared fields.
- Read `research-idea-orchestrator/references/handoff-validation.md` before return.

## Completion Check

Confirm this role used a fresh instance, frozen digest, all visibility fields
false, no evaluator/peer leakage,
readable located findings, resolvable IDs, visible dissent, no source edits or
scores, and a justified recommendation; the orchestrator checks all three IDs.
