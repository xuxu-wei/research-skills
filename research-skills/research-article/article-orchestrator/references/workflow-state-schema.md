# Workflow State Schema

## Schema

```yaml
workflow_state:
  schema_version: "research-article.v5"
  project_slug: ""
  created_at: ""
  updated_at: ""
  entry_mode: standard | fast_track_has_draft | fast_track_draft_eval | blueprint_only | section_specific | submission_only
  user_goal: ""
  target_journal: ""
  target_article_type: ""
  study_type: ""
  reporting_standard: ""
  current_phase: input_governance | architecture_governance | writing | quality_control | submission_delivery
  current_step: 0
  phase_gates:
    input_governance: not_started | in_progress | passed | blocked
    architecture_governance: not_started | in_progress | passed | blocked
    writing: not_started | in_progress | passed | blocked
    quality_control: not_started | in_progress | passed | blocked
    submission_delivery: not_started | in_progress | passed | blocked
  artifacts:
    current:
      readiness_report_path: ""
      readiness_status: ""
      context_brief_path: ""
      proceed_status: ""
      literature_grounding_path: ""
      grounding_confidence: ""
      blueprint_path: ""
      methods_audit_path: ""
      audit_status: ""
      draft_path: ""
      draft_version: 0
      draft_status: ""
      supplementary_path: ""
      supplementary_version: 0
      claim_audit_path: ""
      evaluation_report_path: ""
      evaluation_id: ""
      language_assessment_path: ""
      panel_report_path: ""
      frontmatter_path: ""
      cover_letter_path: ""
      cover_letter_review_path: ""
      package_path: ""
      package_status: ""
    registry:
      - artifact_id: ""
        role: ""
        version: ""
        path: ""
        source_skill: ""
        created_step: 0
        status: not_started | draft | final | superseded | blocked | missing
        based_on: []
        change_type: initial | substantive | language_only | formatting_only | backfill | assembly | audit
  revision:
    round: 0
    max_rounds: 2
    history:
      - round: 1
        revision_plan_path: ""
        response_to_reviewers_path: ""
        revision_delta_path: ""
        language_change_log_path: ""
        source_evaluation_id: ""
        previous_draft_path: ""
        updated_draft_path: ""
        outcome: re_evaluate | panel | compositor | stopped
  panel:
    reports:
      - panel_report_path: ""
        panel_id: ""
        draft_ref: ""
        true_isolation: true | false
    panel_mode: ""
    panel_tier: ""
    aggregated_recommendation: ""
  verification:
    true_isolated_evaluation_completed: false
    true_isolated_panel_completed: false
    reference_verification_status: not_started | pass | partial | fail
    result_consistency_status: not_started | pass | partial | fail
    journal_instructions_verified: verified | user_supplied_only | not_checked
    ethics_declarations_status: not_started | complete | incomplete | not_applicable
  scope_limitations: []
  unresolved_issues: []
  human_signoff:
    data_accuracy: false
    statistical_results_verified: false
    author_contributions_verified: false
    ethics_and_consent_verified: false
    conflicts_of_interest_verified: false
    journal_requirements_verified: false
    figure_quality_verified: false
    reference_accuracy_verified: false
    corresponding_author_confirmed: false
    unresolved_issues_acknowledged: false
  workflow_status: in_progress | completed | blocked | stopped_by_user
```

## Field Rules

- `project_slug`: kebab-case, derived from study topic or user-provided name.
- `current_step`: integer matching the step number in the standard workflow (0-14).
- `artifacts.current`: latest pointers only; all historical versions live in `artifacts.registry`.
- `artifacts.registry`: append-only artifact inventory mirrored in `13_state/artifact-index.md`.
- Artifact paths are relative to the project root. Use `""` for not-yet-created; use `null` for intentionally skipped.
- `revision.history`: append-only list of revision round summaries.
- `verification.true_isolated_evaluation_completed`: required before `ready_for_author_signoff`.
- `scope_limitations`: required when steps are skipped, backfilled with low confidence, or evaluated inline.
- `unresolved_issues`: issues that block submission, carried forward across steps. Never silently dropped.
- `human_signoff`: tracks which signoff items have been confirmed. Initially all `false`.

## State File Location

`<project_root>/13_state/workflow-state.yaml`

This is the single authoritative source for current state. No other file should independently track versions or status.
