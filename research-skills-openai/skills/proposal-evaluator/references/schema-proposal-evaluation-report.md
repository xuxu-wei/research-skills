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
- files_read
- review_scope
- isolation_mode: fresh_subagent
- prior_scores_visible: false
- prior_versions_visible: false
- revision_delta_visible: false
- source_edits_performed: false
- reviewed_artifact_digest
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
