---
name: proposal-package-assembler
description: "Assemble evaluated proposal, review, revision, panel, issue, and optional SAP artifacts without rewriting."
---
# proposal-package-assembler

## Purpose

Use this skill when proposal drafting, evaluation, revision, optional review, and optional SAP branches are complete enough to assemble a final handoff package.

This skill summarizes and organizes existing artifacts. It does not rewrite proposal content, clean proposal artifacts, patch files, re-evaluate proposal/SAP quality, generate new reviewer comments, or hide unresolved issues.

## Inputs

Usually supplied by `proposal-orchestrator`:

- workflow state following `proposal-orchestrator/references/workflow-state-schema.md`;
- complete current proposal logical identity: `artifact_id`, `proposal_file_path`, and `proposal_version`;
- proposal context brief, if available;
- readiness report, if available;
- latest proposal evaluation report;
- revision history and delta reports, if any;
- proposal review panel summary and reviewer dissent, if any;
- editorial readiness, action-execution, preservation, and reassessment records, if editorial repair occurred;
- score-free journal candidate brief and fresh medical-journal review, if the journal route occurred;
- submission-clean proposal path, only if already produced by drafter/refinement;
- unresolved issues and user-confirmation-needed items;
- user goal, target output, and format/funding requirements;
- optional SAP materials only when SAP branch was requested.

If final proposal path, latest evaluation report, or workflow state is missing, return a missing-input or partial-package report.

## Workflow

1. Confirm package scope: proposal only, proposal + review, proposal + SAP, or proposal + SAP + review.
2. Verify required inputs: workflow state, proposal path/version, latest evaluation, unresolved issue status.
3. Preserve lineage: record initial, revised, panel-reviewed, submission-clean, and final versions when available.
4. Summarize existing reports: readiness, latest evaluation, revision status, editorial action execution/preservation/fresh reassessment, score-free journal matching, fresh medical-journal review, panel recommendation, skeptical objections, submission-guard findings, and conflicts, when present.
5. Add optional SAP section only when SAP branch was requested.
6. List unresolved issues: blocking issues, major risks, minor issues, reviewer dissent, user confirmation, human expert review.
7. Verify that any editorial repair has complete action execution, successful content preservation, and fresh narrative/language reassessment, and that any journal route binds the same final proposal without evaluator-score leakage.
8. Require the package proposal `{artifact_id, version, path}` to equal the logical proposal reference recorded by the latest qualifying evaluation and require complete artifact-index entries. A mismatch, incomplete index, or partial proposal blocks ready. Legacy digest fields may be preserved but are never required or compared. Then derive status mechanically from valid reviews and unresolved issues; do not create a quality judgment.
9. Recommend next human review steps based only on existing artifacts.

## Submission-Clean Boundary

If submission-clean cleanup is required, do not perform it here.

Route cleanup findings to `proposal-refinement-controller` and `proposal-drafter` before package assembly. The package may include a submission-clean proposal only when a clean file path and version are already present in workflow state.

`references/archival-cleanup.md` is a handoff guide for the cleanup step before packaging, not permission for this assembler to patch or rewrite proposal files.

## Output

Default output: **Final Proposal Package** with:

- final/current proposal path and version;
- package status;
- included materials;
- readiness and latest evaluation summary;
- revision history summary;
- proposal review panel summary, if any;
- editorial preservation/readiness summary, if applicable;
- journal candidate and medical-journal-review summary, if applicable;
- submission-clean status, if any;
- unresolved issues and risks;
- next human review steps;
- optional SAP section when requested.

Partial output is allowed when materials are missing; state missing pieces and limitations clearly.

## Boundaries

- Do not create or rewrite proposal text.
- Do not patch submission artifacts.
- Do not re-score, re-review, or decide evaluator/report conflicts.
- Do not independently infer readiness. Copy or mechanically derive status from existing valid reviews, version coverage, and recorded unresolved issues; conflicting or missing evidence yields `partial` or `blocked` rather than an assembler judgment.
- Do not add SAP materials unless SAP branch was requested.
- Do not remove fatal flaws, unresolved issues, reviewer dissent, or skeptical objections.
- Any unresolved credible fatal or blocking finding mechanically caps package status at `blocked`; never emit a ready, minor-pending, or promoted status.
- Missing required independent review yields `independent_review_pending`, not a ready package.
- Do not emit `human_signoff_required` when latest changed proposal/SAP versions lack required independent evaluation.
- Do not infer scientific quality from narrative/language polish or journal fit, and do not let journal findings rewrite evaluator scores.

## References

- `references/archival-cleanup.md`: pre-packaging cleanup handoff guide for drafter/refinement, not an assembler-side editing procedure.
- Read `references/rules-final-package.md` when its named guidance or contract applies: defines package assembly rules, included materials, and presentation order.
- Read `references/policy-unresolved-issues.md` when its named guidance or contract applies: defines how unresolved issues are recorded without hiding or softening them.
- Read `references/policy-package-scope.md` when its named guidance or contract applies: defines package material boundaries and prevents scope creep.
- Read `references/policy-file-lineage.md` when its named guidance or contract applies: defines lineage tracking from proposal to final package.
- Read `references/schema-final-proposal-package.md` when its named guidance or contract applies: defines Final Proposal Package structure.
- Use `templates/template-final-proposal-package.md` when producing its named artifact: output template for the final package.
