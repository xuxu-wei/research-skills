---
name: article-review-panel
description: "Run one isolated article peer-review role on a frozen manuscript; preserve fatal findings, conflicts, and dissent without editing."
---
# article-review-panel

## Role

Execute exactly one assigned manuscript-review role and return one sealed individual report. The orchestrator dispatches roles and aggregates; never run this skill as a large reviewer or panel coordinator.

## Independent Execution Contract

- Run each role in a separate fresh independent subagent or delegated thread, never in generator, drafter, revision, evaluator, or orchestrator context.
- Require frozen manuscript ID/path/version, mode, tier, role, and scope. Treat all sources as read-only.
- Write only the assigned reviewer report. Do not edit, draft, rewrite, polish, repair, or fix sources; do not aggregate panel reports.
- Do not read parent hidden reasoning, expected conclusions, prior evaluations, claim audits, context, unresolved issues, or peer outputs.
- The submission-guard role alone may read the frozen journal adapter under `"04_blueprint/**"`.
- Report exact files read, scope, limitations, and reviewer instance ID.
- If any required role cannot run independently, return `independent_review_pending` with a continuation brief and stop; never fill the role inline or aggregate an incomplete panel.

## Panel Contract

- Mode defaults to `blind_external_simulation`.
- Lightweight tier: methodology/statistics, evidence-claim, submission guard.
- Standard tier: lightweight roles plus clinical/domain significance.
- Full tier: standard roles plus internal diagnostic methodology and evidence-retrieval completeness.
- An outlet-reader simulation is optional only when the selected journal reaches a materially different readership. It tests that outlet-specific interpretation and must not duplicate the completed narrative/language readiness review.
- Dispatch selected roles concurrently against the same frozen manuscript; reviewers cannot see one another.
- The submission guard is mandatory in every tier.

## Individual Review Procedure

1. Validate role, scope, frozen version, allowed files, and forbidden context.
2. Apply only the assigned role rubric.
3. Record strengths, concerns, locatable findings, fatal/blocking status, recommendation, and limitations.
4. Seal the report without peer consultation or source changes.

## Review Report Contract

```yaml
review_id:
reviewer_skill: article-review-panel
reviewer_instance_id:
workflow_id:
round_id:
input_artifact_ids: []
input_versions: []
files_read: []
review_scope: []
isolation_mode: fresh_subagent
prior_scores_visible: false
source_edits_performed: false
decision:
findings: []
unresolved_issues: []
```

## Orchestrator Aggregation Rules

Aggregate only after all required sealed reports return. Preserve reviewer IDs, conflicts, minority findings, and dissent. A methodology fatal flaw caps recommendation at `not_ready`; fatal overclaim requires revision; a submission-guard block prevents ready-for-signoff packaging. Never average away a recommendation separated by two or more levels.

Allowed aggregate levels are `strong_support`, `support_with_minor_revision`, `support_after_major_revision`, `revise_and_resubmit`, `not_ready`, and `reject_or_redesign`. Any prose change after panel creates a new version and requires content preservation, fresh narrative/language readiness, and fresh evaluation before delivery.

## Conditional Resources

- Read `references/reviewer-role-definitions.md` for the assigned role, required inputs, and report focus.
- Read `references/panel-aggregation-guide.md` only when the orchestrator aggregates sealed reports.
- Read `article-orchestrator/references/artifact-review-and-submission-contracts.md` when validating individual and aggregate schemas.
- Read `article-orchestrator/references/delegate-brief-templates.md` when preparing role briefs.
- Read `article-orchestrator/references/delegation-rules-pattern.md` when dispatching concurrent independent roles.

## Completion Check

Confirm one role/one instance, frozen read-only input, no forbidden reports, complete provenance, explicit fatal status, all required roles complete before aggregation, visible dissent, and unchanged source artifacts.
