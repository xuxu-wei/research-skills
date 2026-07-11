# Schema: Panel Review Report

Use this file as a structural checklist for validating panel review outputs. Do not paste this schema into SKILL.md.

## Individual Reviewer Report Fields

- review_id
- reviewer_skill: proposal-review-panel
- reviewer_instance_id
- workflow_id
- round_id
- input_artifact_ids
- input_versions
- files_read
- isolation_mode: fresh_subagent
- prior_scores_visible: false
- source_edits_performed: false
- reviewer_role
- review_scope
- overall_assessment
- major_strengths
- major_weaknesses
- reviewer_specific_concerns
- must_fix_items
- optional_suggestions
- recommendation
- confidence

## Panel Summary Fields

- proposal_file_path
- proposal_version
- review_scope
- reviewers_included
- individual_review_summaries
- consensus_strengths
- consensus_weaknesses
- reviewer_disagreements
- skeptical_objections
- must_fix_before_submission
- optional_improvements
- unresolved_risks
- likely_reviewer_attack_points
- final_recommendation
- recommendation_rationale
- recommended_next_step
