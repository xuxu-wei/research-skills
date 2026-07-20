# Schema: Proposal Evaluation Report

The report should include the following fields. This file defines structure only; it is not a scoring rubric.

## Required Fields

- review_id
- reviewer_skill: proposal-evaluator
- reviewer_instance_id
- workflow_id
- round_id
- input_artifact_ids
- input_versions
- reviewed_proposal_ref
  - artifact_id
  - version
  - path
- files_read
- review_scope
- evaluation_stage: initial_scientific | scientific_reassessment | final_scientific
- isolation_mode: fresh_subagent
- prior_scores_visible: false
- prior_versions_visible: false
- revision_delta_visible: false
- readiness_report_visible: false
- repair_artifacts_visible: false
- prior_evaluation_visible: false
- source_edits_performed: false
- complete_artifact_confirmed: true
- evaluation_id
- proposal_file_path
- proposal_version
- evaluation_type: initial | re-evaluation
- evaluator_role
- overall_decision: accept | revise | reject
- overall_rationale
- dimension_scores
  - novelty
  - feasibility
  - impact
  - relevance
  - clarity
  - completion
- weighted_overall
- hard_gate_status
  - clarity_gate
  - feasibility_gate
  - completion_gate
  - genre_fit_gate
  - no_fatal_flaws_gate
- fatal_flaws
- major_strengths
- major_weaknesses
- reviewer_defensibility_concerns
- revision_priorities
- unresolved_issues
- if_re_evaluation
  - anonymized_must_fix_list_used: true | false
  - prior_versions_visible: false
  - revision_delta_visible: false

For `final_scientific`, `anonymized_must_fix_list_used` must be `false`, and the files-read list may contain only the revised final proposal, stable rubric/gates, and minimal call/factual inputs.
