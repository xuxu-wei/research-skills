# Research-Article Artifact Contracts

Canonical schemas for artifacts passed between `research-article` skills.

## Global Rules

- Every machine-readable artifact includes `schema_version`, `plugin_version`, `artifact_id`, `source_skill`, `status`, and lineage fields when applicable. Read `plugin_version` from the plugin manifest/registry at workflow start.
- Use Markdown for user-facing deliverables; use YAML blocks for agent-to-agent state transfer.
- Use `unknown`, `unclear`, `not_specified`, or `not_applicable` instead of inventing facts.
- Store workflow artifacts in the user's project directory, not inside the skill package.
- Artifact IDs follow `<type>-<NNN>` or the round-specific pattern documented in `artifact-naming-and-directory-rules.md`.
- Every readiness, audit, evaluation, panel-reviewer, panel-aggregate, and submission-verification report includes the standard independent-review fields: `review_id`, `reviewer_skill`, `reviewer_instance_id`, `workflow_id`, `round_id`, `input_artifact_ids`, `input_versions`, `files_read`, `review_scope`, `isolation_mode: fresh_subagent`, `prior_scores_visible: false`, `source_edits_performed: false`, `decision`, `findings`, and `unresolved_issues`.
- If independent execution is unavailable, emit `independent_review_pending` plus a continuation brief instead of a report decision.

## Minimal Intake Summary

```yaml
minimal_intake_summary:
  study_topic: ""
  apparent_study_type: ""
  available_materials:
    protocol_or_sap: true | false
    primary_results: true | false
    tables_figures: true | false
    statistical_outputs: true | false
    methods_description: true | false
    references: true | false
  stated_target_journal: ""
  obvious_missing_items: []
```

## Article Readiness Report

```yaml
article_readiness_report:
  schema_version: "research-article.v5"
  artifact_id: "readiness-001"
  source_skill: "article-readiness-triage"
  review_id: "review-001"
  reviewer_instance_id: ""
  workflow_id: ""
  round_id: "intake"
  input_artifact_ids: []
  input_versions: []
  files_read: []
  review_scope: []
  isolation_mode: fresh_subagent
  prior_scores_visible: false
  source_edits_performed: false
  readiness_status: ready | conditionally_ready | not_ready | wrong_article_type
  recommended_article_type: original_article | brief_report | research_letter | methods_article | data_descriptor | case_report | review | other
  minimum_inputs_present:
    research_question: true | false
    study_design: true | false
    primary_results: true | false
    methods_details: true | false
    figures_tables: true | false
    references: true | false
  blocking_gaps: []
  nonblocking_gaps: []
  target_journal_realism:
    stated_target: ""
    realism_assessment: realistic | ambitious_but_possible | mismatch
    mismatch_details: ""
  recommended_route: blueprint | methods_preflight | data_analysis | literature_review | stop
```

## Article Context Brief

```yaml
article_context_brief:
  schema_version: "research-article.v5"
  artifact_id: "context-001"
  source_skill: "article-context-builder"
  study_design:
    type: ""
    subtype: ""
    phase: ""
  reporting_standard_selection:
    primary_standard: ""
    primary_source: EQUATOR | journal | field_standard | no_exact_match
    extensions: []
    supplementary_standards: []
    journal_override: ""
    mapping_confidence: high | medium | low
    no_exact_match: true | false
    rationale: ""
  target_journal:
    name: ""
    article_type: ""
    figure_table_limits: ""
    abstract_structure: ""
    reporting_requirements: []
  research_question:
    primary: ""
    secondary: []
    framework: ""
  study_object:
    population_or_sample: ""
    setting: ""
    time_period: ""
    sample_size: ""
  data_summary:
    data_sources: []
    data_types: []
    data_completeness: complete | partially_complete | with_missing | unknown
    known_limitations: []
  results_summary:
    primary_findings: []
    secondary_findings: []
    negative_or_null_findings: []
    robustness_checks_done: []
  methods_summary:
    study_design_details: ""
    variable_definitions: ""
    statistical_approach: ""
    pre_registration: registered | not_registered | not_applicable | unknown
    protocol_or_sap: ""
  assumptions: []
  uncertainties: []
  proceed_status: proceed | proceed_with_assumptions | clarification_stop
```

## Literature Grounding Report

```yaml
literature_grounding_report:
  schema_version: "research-article.v5"
  artifact_id: "lit-ground-001"
  source_skill: "article-literature-grounder"
  search_protocol:
    databases_searched: []
    search_queries: []
    date_searched: ""
    inclusion_logic: ""
    exclusion_logic: ""
    source_priority: []
  coverage_assessment:
    seminal_literature_covered: yes | partial | no | unclear
    recent_literature_covered: yes | partial | no | unclear
    conflicting_literature_checked: yes | partial | no
    prior_reviews_guidelines_covered: yes | partial | no | unclear
  novelty_position:
    gap_type: evidence_gap | methodological_gap | population_gap | replication | extension | confirmation | refutation
    what_this_study_adds: ""
    novelty_claim_confidence: high | medium | low
    novelty_claim_risk: high | medium | low
  competing_evidence: []
  citation_risk:
    missing_seminal_work: []
    overreliance_on_low_quality_sources: []
    outdated_references: []
  grounding_confidence: high | medium | low
```

## Article Blueprint

```yaml
article_blueprint:
  schema_version: "research-article.v5"
  artifact_id: "blueprint-001"
  source_skill: "article-architect"
  contribution:
    type: evidence | method | data | theory | refutation | replication | synthesis | other
    statement: ""
    one_sentence_takeaway: ""
  study_type_confirmation:
    type: ""
    subtype: ""
    reporting_standard: ""
  core_question_and_answer:
    research_question: ""
    main_answer: ""
    answer_strength: definitive | strong | moderate | suggestive | exploratory
  claim_evidence_matrix: []
  evidence_provenance_ledger_ref: "04_blueprint/evidence-provenance-ledger.md"
  evidence_display_plan: []
  supplementary_index:
    items: []
    journal_limits:
      max_supplementary_items: 0
      max_supplementary_files: 0
      supplementary_file_format: ""
      data_availability_policy: ""
      code_availability_policy: ""
  results_skeleton:
    organization_mode: norm_driven | argument_driven | hybrid | artifact_driven | theory_driven | evidence_synthesis_driven
    sections: []
  journal_adapter:
    target_journal: ""
    source_checked_date: ""
    source_documents: []
    confidence: high | medium | low
  reviewer_risk_preview: []
```

## Methods Audit Report

```yaml
methods_audit_report:
  schema_version: "research-article.v5"
  artifact_id: "methods-audit-001"
  source_skill: "article-methods-statistics-auditor"
  review_id: "review-002"
  reviewer_instance_id: ""
  workflow_id: ""
  round_id: "pre-draft"
  input_artifact_ids: []
  input_versions: []
  files_read: []
  review_scope: []
  isolation_mode: fresh_subagent
  prior_scores_visible: false
  source_edits_performed: false
  audit_status: pass | conditionally_pass_with_author_verification | requires_methods_clarification | requires_reanalysis | methodologically_blocked
  audit_scope:
    design_audit_possible: true | false
    statistical_audit_possible: true | false
    limitations: []
  findings: []
  unfixable_by_writing: []
  recommendation: proceed_to_drafting | fix_methods_text | requires_reanalysis | requires_data_collection | stop
```

## Manuscript Draft

```yaml
manuscript_draft:
  schema_version: "research-article.v5"
  artifact_id: "manuscript-v001"
  source_skill: "article-drafter"
  version: 1
  blueprint_ref: "04_blueprint/article-blueprint.md"
  sections:
    introduction: {content: "", word_count: 0}
    methods: {content: "", word_count: 0, reporting_items_covered: []}
    results: {content: "", word_count: 0}
    discussion: {content: "", word_count: 0}
  display_items: []
  reporting_checklist_mapping: []
  unresolved_issues: []
  drafting_assumptions: []
```

## Claim Audit Report

```yaml
claim_audit_report:
  schema_version: "research-article.v5"
  artifact_id: "claim-audit-001"
  source_skill: "article-claim-auditor"
  review_id: "review-003"
  reviewer_instance_id: ""
  workflow_id: ""
  round_id: ""
  input_artifact_ids: []
  input_versions: []
  files_read: []
  review_scope: []
  isolation_mode: fresh_subagent
  prior_scores_visible: false
  source_edits_performed: false
  claim_evaluations: []
  overall_assessment:
    total_claims: 0
    fatal_overclaims:
      - claim_id: ""
        fixability: fixable_by_downscaling | fixable_by_removal | fixable_by_relocation | unfixable
        route: refinement_then_reaudit | stop
        rationale: ""
  recommendation: pass | downscale_and_proceed | revise_and_reaudit | blocked
```

## Article Evaluation Report

```yaml
article_evaluation:
  schema_version: "research-article.v5"
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
  source_edits_performed: false
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
  schema_version: "research-article.v5"
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
  schema_version: "research-article.v5"
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
  schema_version: "research-article.v5"
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
  schema_version: "research-article.v5"
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
  schema_version: "research-article.v5"
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
  schema_version: "research-article.v5"
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
  status: ready_for_author_signoff | ready_for_author_check | minor_revision_pending | major_revision_required | blocked | partial
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
