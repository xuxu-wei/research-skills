# Proposal Workflow State Schema

## Contents

<!-- toc:start -->
- [Required Fields](#required-fields)
- [Canonical Runtime Artifact Record](#canonical-runtime-artifact-record)
- [Artifact Registry](#artifact-registry)
- [Revision Entry](#revision-entry)
- [Unresolved Issue Record](#unresolved-issue-record)
- [Fast-Track Rule](#fast-track-rule)
- [Package Rule](#package-rule)
<!-- toc:end -->

Use this file as the shared artifact registry for `proposal-orchestrator`.
Every entry path, skipped step, revision loop, SAP branch, review panel, and final package must update this state explicitly.

## Required Fields

- `workflow_id`: stable identifier for the proposal workflow.
- `plugin_version`: exact installable plugin version that created the current state.
- `project_root`: writable project directory containing all workflow artifacts.
- `artifact_index_path`: path to `10_state/artifact-index.md`.
- `entry_mode`: one of `standard`, `existing_draft`, `draft_and_external_review`, `package_only`.
- `workflow_status`: one of `initialized`, `preprocessing`, `planning`, `writing`, `artifact_frozen`, `pending_review`, `independent_review_pending`, `revision_required`, `editorial_review_pending`, `editorial_repair_required`, `journal_review_pending`, `panel_pending`, `packaging_pending`, `blocked`, `stopped`, `human_signoff_required`.
- `user_goal`: user's stated purpose for the proposal workflow.
- `target_output`: grant proposal, protocol, internal review package, mock review, SAP bundle, or other target.
- `context_brief_path`: path to the proposal context brief, or `null` if intentionally skipped.
- `context_missing`: `true` when fast-track mode proceeds without a context brief.
- `evaluation_scope_limitation`: limitation note required when `context_missing: true` or key context is absent.
- `evidence_map_path`: path to evidence map, or `null`.
- `evidence_limitations_path`: path to evidence limitations, or `null`.
- `readiness_report_path`: path to readiness report, or `null` if skipped in fast-track mode.
- `content_plan_path`: current `04_drafts/proposal-content-plan-vNNN.yaml`, or `null` only when an existing-draft mode records why planning is skipped.
- `content_plan_version`: logical version of the current content plan, or `null`.
- `planner_instance_id`: fresh planning-mode drafter instance, or `null` when planning is legitimately skipped.
- `writer_instance_id`: writer of the current proposal; for a new full proposal it must differ from `planner_instance_id`.
- `proposal_file_path`: current proposal file path.
- `proposal_version`: current proposal version.
- `proposal_status`: one of `not_started`, `planned`, `drafted`, `evaluated`, `revision_needed`, `revision_complete`, `editorial_repair_needed`, `editorial_ready`, `final_evaluated`, `journal_reviewed`, `panel_reviewed`, `submission_clean`, `packaged`, `stopped`.
- `evaluation_report_path`: latest proposal evaluation report, or `null`.
- `evaluation_stage`: `initial_scientific`, `scientific_reassessment`, `final_scientific`, or `null`.
- `evaluated_proposal_version`: exact proposal version read by the latest qualifying evaluator, or `null`.
- `revision_round`: integer count of proposal revision rounds completed.
- `revision_history`: list of proposal revision entries.
- `reader_handoff_path`: frozen minimal proposal reader handoff, or `null` before editorial readiness.
- `protected_content_register_path`: register frozen from the scientifically eligible proposal, or `null`.
- `narrative_assessment_path`: current narrative assessment, or `null`.
- `language_assessment_path`: current academic-language assessment, or `null`.
- `editorial_repair_brief_path`: normalized included-action brief, or `null`.
- `editorial_action_execution_path`: writer execution record for the current repair, or `null`.
- `content_preservation_report_path`: fresh preservation report for the current editorial repair, or `null`.
- `narrative_reassessment_path`: fresh reassessment of the repaired proposal, or `null`.
- `language_reassessment_path`: fresh reassessment of the repaired proposal, or `null`.
- `editorial_round`: integer count of completed editorial repair rounds.
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
- `journal_candidate_brief_path`: score-free candidate brief built from the final proposal and verified journal facts, or `null`.
- `medical_journal_review_path`: fresh medical-journal review of the final proposal and candidate brief, or `null`.
- `unresolved_issues`: list of unresolved issue records.
- `final_package_path`: final package path, or `null`.

## Canonical Runtime Artifact Record

Each proposal, SAP, review, revision, panel, and package artifact must register `artifact_id`, `role`, `version_id`, `workflow_id`, `round_id`, `revision_round`, `plugin_version`, `source_skill`, `created_step`, `created_by_instance_id`, `current_artifact_path`, `based_on`, `change_type`, `status`, and `frozen`. Fields such as `proposal_version` and `sap_version` remain workflow pointers to the canonical `version_id`; role-specific `version` and `path` aliases must equal `version_id` and `current_artifact_path`.

Legacy states may contain `content_digest`, `sha256`, or similarly named digest fields. Readers must tolerate and preserve them when round-tripping legacy state, but no LLM-facing brief, handoff, evaluation, match, or promotion rule may require, compute, compare, or add them. Current identity and coverage checks use `{artifact_id, version_id, current_artifact_path}` plus a complete artifact-index entry; role-specific `version` and `path` fields are equal-value aliases.

## Artifact Registry

`workflow-state.yaml` must include an artifact registry that mirrors `10_state/artifact-index.md`:

- `artifact_id`
- `role`: context, reader_handoff, evidence, readiness, content_plan, proposal, evaluation, revision_plan, response, delta, narrative_assessment, language_assessment, protected_content_register, editorial_repair_brief, editorial_action_execution, content_preservation, narrative_reassessment, language_reassessment, journal_candidate_brief, medical_journal_review, sap, panel, package.
- `version_id`
- `workflow_id`
- `round_id`
- `revision_round`
- `current_artifact_path`
- `source_skill`
- `created_step`
- `created_by_instance_id`
- `based_on`: previous artifact IDs or paths.
- `change_type`
- `status`: current, superseded, stale_after_revision, partial, blocked, final.
- `plugin_version`
- `frozen`: explicit boolean.

This registry and `10_state/artifact-index.md` use the same complete row. A missing key is an incomplete index; use explicit `null` or an empty list where a field is not applicable.

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
- `editorial_repair_brief_path`, when applicable
- `editorial_action_execution_path`, when applicable
- `content_preservation_report_path`, when applicable

## Unresolved Issue Record

Each `unresolved_issues` item must include:

- `id`
- `source`: readiness, evaluator, narrative_assessor, language_assessor, content_preservation, medical_journal_review, review_panel, SAP, user, package.
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
Any changed proposal or SAP creates a new version and returns to `artifact_frozen`/`pending_review`; panel, journal review, packaging, and human sign-off require fresh evaluation of the exact current logical proposal version. Fatal findings set `blocked`, and reviewer unavailability sets `independent_review_pending`. Parallel phases must retain one writer per source artifact/version; reviewer inputs are read-only. Editorial repair may use sequential section passes only within the same writer task and one complete not-yet-frozen target.
