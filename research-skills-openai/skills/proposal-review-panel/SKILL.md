---
name: proposal-review-panel
description: "Independently review a frozen proposal from one assigned panel role after evaluation or in an early advisory review."
---
# proposal-review-panel

## Role

Execute exactly one assigned proposal-review role and return one sealed individual report. This skill is not a multi-reviewer coordinator: the orchestrator dispatches roles and aggregates reports.

## Independent Execution Contract

- Run each selected reviewer role in a different fresh independent subagent or delegated thread; never run in the context that generated, drafted, or revised the proposal.
- Require frozen logical input artifact IDs, paths, versions, review mode, role, and scope. Treat all source artifacts as read-only; do not require or compute hashes/digests.
- Write only the assigned individual review report. Do not edit, draft, rewrite, polish, repair, or fix the proposal or SAP.
- Do not read parent hidden reasoning, expected conclusions, context/readiness reports, evaluator outputs, repair/delta/editorial artifacts, medical-journal-review outputs, or another panel member's work.
- Report exact files read, review scope, limitations, and reviewer instance ID.
- If any required role cannot run independently, return `independent_review_pending` with a self-contained continuation brief and stop; never fall back to inline review or emit a panel recommendation.

Every individual report includes `review_id`, `reviewer_skill`, `reviewer_instance_id`, `workflow_id`, `round_id`, `input_artifact_ids`, `input_versions`, `files_read`, `isolation_mode: fresh_subagent`, `prior_scores_visible: false`, `source_edits_performed: false`, `decision`, `findings`, and `unresolved_issues`.

## Modes and Inputs

- `blind_mock_review` is default. Read only frozen proposal logical identity, user goal/target output, verified funding call or review scenario, assigned role, and scope. Do not read context brief, readiness/evaluation reports, revision or editorial artifacts, journal-review findings, unresolved-issue list, or peer reports.
- `context_aware_internal_review` is allowed only when explicitly selected. Label it internal advisory review and list every extra background file read.
- SAP review is allowed only when explicitly requested and a frozen SAP version is supplied.

Stop when the proposal is missing/unreadable, the role or scope is absent, SAP was requested but missing, or an early panel was not explicitly requested before the evaluator gate.

## Panel Tiers

The orchestrator selects and concurrently dispatches roles:

- `lightweight_panel` (3): domain expert, methodology/statistics, submission guard.
- `standard_panel` (5, default): broad field, domain expert, methodology/statistics, skeptical, submission guard.
- `full_panel` (7): standard roles plus cross-disciplinary senior and translational/end-user.

For medicine, clinical practice, or public health, use practicing-clinician as the domain expert. The submission guard is mandatory. Disabling the skeptical role requires explicit user direction and lowers panel confidence.

## Individual Review Procedure

1. Validate frozen inputs, mode, role, scope, and forbidden context.
2. Apply only the assigned role rubric from `references/roles-reviewer-panel.md`.
3. Record strengths, weaknesses, role-specific concerns, attack points, and limitations.
4. Tag every must-fix item `[evidence]`, `[clarity]`, `[substance]`, or `[other]`; mark credible fatal/blocking findings explicitly.
5. Return one recommendation from `strong_support`, `support_with_minor_revision`, `support_after_major_revision`, `revise_and_resubmit`, `not_ready`, or `reject_or_redesign`.
6. Seal the report without consulting peers or changing source files.

## Orchestrator Aggregation Contract

After every selected role returns, the orchestrator—not this reviewer instance—aggregates sealed reports. It must:

- preserve reviewer identity, conflicts, minority objections, skeptical findings, and dissent;
- deduplicate only identical actionable items without deleting provenance;
- prevent `strong_support` or `support_with_minor_revision` when any credible fatal/blocking finding remains;
- route fixable fatal findings to major revision/re-evaluation, unavailable repairs to `not_ready`, and unfixable flaws to `reject_or_redesign`;
- never expose an individual report to another reviewer.

## Conditional Resources

- Read `references/roles-reviewer-panel.md` for the assigned role and tier membership.
- Read `references/policy-reviewer-independence.md` when validating allowed and forbidden context.
- Read `references/delegation-concurrency-rules.md` only when the orchestrator prepares concurrent dispatch.
- Read `references/policy-panel-aggregation.md` only when the orchestrator aggregates sealed reports.
- Read `references/policy-panel-aggregation-format.md` only when grouping must-fix items with provenance.
- Read `references/policy-skeptical-review.md` for the skeptical role.
- Read `references/schema-panel-review-report.md` when validating report fields.
- Use `templates/template-individual-review-report.md` for an assigned reviewer output.
- Use `templates/template-panel-summary-report.md` only for orchestrator-owned aggregation after all reports are sealed.
- Read `proposal-orchestrator/references/reviewer-brief-templates.md` when preparing role-specific reviewer briefs.

## Completion Check

Confirm one role/one instance, logically frozen read-only inputs, no forbidden reports read, locatable findings, explicit fatal status, complete provenance, unchanged sources, no digest requirement, and no fabricated consensus.
