# Research-Article Review and Submission Contracts

## Contents

<!-- toc:start -->
- [Article Evaluation Report](#article-evaluation-report)
- [Revision Artifacts](#revision-artifacts)
- [Panel Report](#panel-report)
- [Cover Letter](#cover-letter)
- [Submission Package](#submission-package)
<!-- toc:end -->

## Article Evaluation Report

```yaml
article_evaluation:
  schema_version: "research-article.v6"
  artifact_id: "eval-001"
  evaluation_id: "eval-001"
  review_id: "eval-001"
  reviewer_skill: "article-evaluator"
  reviewer_instance_id: ""
  workflow_id: ""
  round_id: ""
  input_artifact_ids: []
  input_versions: []
  files_read: []
  review_scope: []
  isolation_mode: fresh_subagent
  prior_scores_visible: false
  prior_versions_visible: false
  revision_delta_visible: false
  source_edits_performed: false
  reviewed_artifact_digest: "sha256:"
  complete_artifact_confirmed: true
  identity_drift_detected: false
  source_skill: "article-evaluator"
  draft_ref: "06_drafts/manuscript-v001.md"
  draft_version: 1
  dimension_scores:
    scientific_validity: 0
    evidence_claim_alignment: 0
    reporting_completeness: 0
    journal_fit: 0
    clarity_structure: 0
    language_academic_register: 0
    contribution_significance: 0
  noncompensatory_gates: []
  gate_failures:
    fatal_scientific: []
    reporting: []
    genre_rhetoric: []
    language_baseline: []
  supplementary_audit:
    critical_evidence_buried: []
    missing_supplementary_content: []
    orphan_supplementary_content: []
    journal_limit_compliance: pass | fail | not_checked
    data_code_availability_compliance: pass | fail | partial | not_checked
  overall_assessment:
    readiness_level: submission_ready | minor_revision | major_revision | not_ready | methodologically_blocked
  revision_priorities:
    - issue_id: ""
      category: evidence | clarity | substance | language | reporting | other
      severity: critical | major | minor
      location: ""
      description: ""
      suggested_fix: ""
      entry_strategy: enter_manuscript | response_only | decline
  reviewer_defensibility_concerns: []
  decision: accept | revise | reject
  decision_rationale: ""
```

## Revision Artifacts

```yaml
revision_plan:
  schema_version: "research-article.v6"
  artifact_id: "revision-plan-r001"
  source_skill: "article-refinement-controller"
  round: 1
  based_on_evaluation: "eval-001"
  manuscript_version: "manuscript-v001.md"
  target_version: "manuscript-v002.md"
  revision_mode:
    primary: textual_revision | structural_revision | evidence_relinking | reporting_completion | claim_downscaling | methods_detailing | journal_retargeting | language_polishing
    secondary: []
  revision_allowed: yes | no | conditional
  required_external_action: ""
  items:
    - concern_id: ""
      action: enter_manuscript | response_only | decline
      description: ""
      location: ""
      claim_ids: []

response_to_reviewers:
  schema_version: "research-article.v6"
  artifact_id: "response-to-reviewers-r001"
  source_skill: "article-refinement-controller"
  round: 1
  manuscript_version: "manuscript-v002.md"
  evaluation_ref: "eval-001"
  responses:
    - concern_id: ""
      concern_summary: ""
      action: revised | response_only | declined
      manuscript_location: ""
      response_text: ""
      change_summary: ""
  unresolved_issues: []
  new_issues_introduced: []

revision_delta:
  schema_version: "research-article.v6"
  artifact_id: "revision-delta-r001"
  source_skill: "article-refinement-controller"
  round: 1
  previous_manuscript: "manuscript-v001.md"
  updated_manuscript: "manuscript-v002.md"
  evaluator_concerns:
    addressed: []
    partially_addressed: []
    not_addressed_with_reason: []
  new_issues_introduced: []
  substantive_changes:
    methods_changed: false
    results_changed: false
    primary_claim_strength_changed: false
    contribution_statement_changed: false
  new_assumptions_requiring_author_confirmation: []
  recommended_next_step: re_evaluate | panel | compositor
```

## Panel Report

```yaml
panel_report:
  schema_version: "research-article.v6"
  artifact_id: "panel-001"
  panel_id: "panel-001"
  source_skill: "article-orchestrator"
  aggregation_owner: "article-orchestrator"
  workflow_id: ""
  round_id: ""
  input_artifact_ids: []
  input_versions: []
  reviewer_report_refs: []
  panel_mode: blind_external_simulation | internal_diagnostic_review
  panel_tier: lightweight | standard | full
  draft_ref: "06_drafts/manuscript-v001.md"
  reviewer_isolation_status: fresh_subagents_complete
  reviewers: []  # each entry carries the standard independent-review fields
  aggregated_recommendation: strong_support | support_with_minor_revision | support_after_major_revision | revise_and_resubmit | not_ready | reject_or_redesign
  aggregation_rules_applied: []
  consensus_summary: ""
  dissenting_opinions:
    - dissent_id: ""
      reviewer_instance_id: ""
      finding: ""
      severity: fatal | major | minor | informational
      blocking: true | false
      disposition: unresolved | accepted_risk | routed_to_revision | resolved
      owner: ""
      human_signoff_ref: ""
  must_fix_items: []
  suggestion_items: []
```

## Cover Letter

```yaml
cover_letter:
  schema_version: "research-article.v6"
  artifact_id: "cover-letter-001"
  source_skill: "article-cover-letter"
  target_journal: ""
  manuscript_title: ""
  status: draft | final | blocked
  word_count: 0
  editorial_case:
    problem: ""
    delta_from_prior_work: ""
    contribution_type: reframes_problem | strengthens_inference | clarifies_decision | enables_measurement | defines_boundaries | reorganizes_evidence | enables_research
    journal_fit: ""
    credibility_basis: []
    editor_decision_help: ""
  disclosures:
    ethics: ""
    trial_registration: ""
    data_code_availability: ""
    conflicts_of_interest: ""
    related_submissions: ""
  quality_check_ref: "11_cover-letter/cover-letter-quality-check.md"
  biomedical_review_ref: ""
  cover_letter_review_status: not_applicable | complete | delegate_unavailable
```

## Submission Package

```yaml
submission_package:
  schema_version: "research-article.v6"
  artifact_id: "package-001"
  package_id: "package-001"
  review_id: "submission-verification-001"
  reviewer_skill: "article-submission-compositor"
  reviewer_instance_id: ""
  workflow_id: ""
  round_id: "final"
  input_artifact_ids: []
  input_versions: []
  files_read: []
  review_scope: []
  isolation_mode: fresh_subagent
  prior_scores_visible: false
  source_edits_performed: false
  status: ready_for_author_signoff | ready_for_author_check | docx_generation_pending | docx_visual_qa_pending | minor_revision_pending | major_revision_required | blocked | partial
  journal_requirements_verified: verified | user_supplied_only | not_checked
  isolation_gate:
    true_isolated_evaluation_completed: true | false
    true_isolated_panel_completed: true | false | not_applicable
    fresh_compositor_verifier_completed: true | false
    action_if_unmet: independent_review_pending
  pre_submission_verification:
    references_verified: pass | partial | fail | not_checked
    table_figure_result_consistency: pass | partial | fail | not_checked
    journal_instructions_verified: verified | user_supplied_only | not_checked
    ethics_declarations_complete: complete | incomplete | not_applicable
  canonical_markdown_ref: "06_drafts/manuscript-v001.md"
  canonical_content_digest: "sha256:"
  docx_ref: "12_package/manuscript-v001.docx"
  docx_content_digest: "sha256:"
  display_manifest_ref: "04_blueprint/display-asset-manifest.yaml"
  docx_sync_status: synchronized | content_drift | not_generated
  render_qa_status: passed | docx_visual_qa_pending | failed | not_generated
  contents:
    manuscript: ""
    supplementary: ""
    abstract: ""
    key_points: ""
    title: ""
    cover_letter: "11_cover-letter/cover-letter.md"
    cover_letter_quality_check: "11_cover-letter/cover-letter-quality-check.md"
    medical_cover_letter_review: ""
    reporting_checklist_mapping: ""
    reviewer_risk_matrix: ""
    human_signoff_checklist: ""
    submission_readiness_summary: ""
  supplementary_compliance:
    supplementary_required: true | false
    requirement_source: supplementary_index | main_text_reference | reporting_guideline | journal_policy | not_required
    item_count_within_limit: true | false
    file_format_matches_journal_spec: true | false
    data_availability_statement_present: true | false
    code_availability_statement_present: true | false
    supplementary_references_included: true | false | not_applicable
    supplementary_cross_referenced: true | false
  unresolved_items: []
  human_review_notes: []
```
