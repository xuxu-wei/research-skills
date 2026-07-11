# Proposal Workflow State Schema

Use this file as the shared artifact registry for `proposal-orchestrator`.
Every entry path, skipped step, revision loop, SAP branch, review panel, and final package must update this state explicitly.

## Required Fields

- `workflow_id`: stable identifier for the proposal workflow.
- `project_root`: writable project directory containing all workflow artifacts.
- `artifact_index_path`: path to `10_state/artifact-index.md`.
- `entry_mode`: one of `standard`, `existing_draft`, `draft_and_external_review`, `package_only`.
- `workflow_status`: one of `initialized`, `preprocessing`, `artifact_frozen`, `pending_review`, `independent_review_pending`, `revision_required`, `panel_pending`, `packaging_pending`, `blocked`, `stopped`, `human_signoff_required`.
- `user_goal`: user's stated purpose for the proposal workflow.
- `target_output`: grant proposal, protocol, internal review package, mock review, SAP bundle, or other target.
- `context_brief_path`: path to the proposal context brief, or `null` if intentionally skipped.
- `context_missing`: `true` when fast-track mode proceeds without a context brief.
- `evaluation_scope_limitation`: limitation note required when `context_missing: true` or key context is absent.
- `evidence_map_path`: path to evidence map, or `null`.
- `evidence_limitations_path`: path to evidence limitations, or `null`.
- `readiness_report_path`: path to readiness report, or `null` if skipped in fast-track mode.
- `proposal_file_path`: current proposal file path.
- `proposal_version`: current proposal version.
- `proposal_status`: one of `not_started`, `drafted`, `evaluated`, `revision_needed`, `revision_complete`, `panel_reviewed`, `submission_clean`, `packaged`, `stopped`.
- `evaluation_report_path`: latest proposal evaluation report, or `null`.
- `evaluated_proposal_version`: exact proposal version read by the latest qualifying evaluator, or `null`.
- `revision_round`: integer count of proposal revision rounds completed.
- `revision_history`: list of proposal revision entries.
- `sap_requested`: boolean.
- `sap_status`: one of `not_requested`, `preflight_needed`, `preflight_blocked`, `drafted`, `evaluated`, `revision_needed`, `accepted`, `stopped`.
- `sap_file_path`: current SAP file path, or `null`.
- `sap_version`: current SAP version, or `null`.
- `sap_evaluation_report_path`: latest SAP evaluation report, or `null`.
- `sap_revision_round`: integer count of SAP revision rounds completed.
- `panel_summary_path`: proposal review panel summary path, or `null`.
- `panel_reviewed_proposal_version`: proposal version reviewed by the panel, or `null`.
- `panel_mode`: one of `blind_mock_review`, `context_aware_internal_review`, or `none`.
- `panel_tier`: one of `lightweight_panel`, `standard_panel`, `full_panel`, or `none`.
- `unresolved_issues`: list of unresolved issue records.
- `final_package_path`: final package path, or `null`.

## Artifact Registry

`workflow-state.yaml` must include an artifact registry that mirrors `10_state/artifact-index.md`:

- `artifact_id`
- `role`: context, evidence, readiness, proposal, evaluation, revision_plan, response, delta, sap, panel, package.
- `version`
- `path`
- `source_skill`
- `created_step`
- `based_on`: previous artifact IDs or paths.
- `status`: current, superseded, stale_after_revision, partial, blocked, final.

See `artifact-naming-and-directory-rules.md` for directory and filename rules.

## Revision Entry

Each `revision_history` item must include:

- `from_version`
- `to_version`
- `from_proposal_file_path`
- `to_proposal_file_path`
- `revision_plan_path`
- `delta_report_path`
- `response_to_reviewers_path`
- `re_evaluation_report_path`
- `decision_after_re_evaluation`

## Unresolved Issue Record

Each `unresolved_issues` item must include:

- `id`
- `source`: readiness, evaluator, review_panel, SAP, user, package.
- `category`: evidence, clarity, substance, SAP, user_confirmation, human_expert_review, other.
- `severity`: blocking, major, minor.
- `description`
- `status`: open, deferred, accepted_risk, resolved.
- `owner`: user, drafter, orchestrator, methodology_reviewer, human_expert, unknown.

## Fast-Track Rule

Fast-track entry may skip earlier artifacts, but it must not leave state implicit.
When a context brief or readiness report is skipped, set the corresponding field to `null`, set the limitation flag or note, and ensure downstream evaluator or reviewer briefs include the reduced-scope limitation.

## Package Rule

`proposal-package-assembler` may assemble from this state but must not silently change it.
If a submission-clean proposal is required, the state must first be updated by `proposal-drafter` or `proposal-refinement-controller`, then package assembly may proceed.
Any changed proposal or SAP creates a new version and returns to `artifact_frozen`/`pending_review`; panel, packaging, and human sign-off require fresh evaluation of the exact current version. Fatal findings set `blocked`, and reviewer unavailability sets `independent_review_pending`. Parallel phases must retain one writer per source artifact/version; reviewer inputs are read-only.
