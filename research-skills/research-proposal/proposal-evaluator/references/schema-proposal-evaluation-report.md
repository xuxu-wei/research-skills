# Schema: Proposal Evaluation Report

The report should include the following fields. This file defines structure only; it is not a scoring rubric.

## Required Fields

- evaluation_id
- proposal_file_path
- proposal_version
- evaluation_type: initial | re-evaluation
- evaluator_role
- overall_decision: accept | revise | reject | stop_no_gain
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
  - previous_version_compared
  - resolved_issues
  - persistent_issues
  - new_issues
  - delta_assessment
