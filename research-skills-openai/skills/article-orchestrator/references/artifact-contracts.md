# Research-Article Artifact Contracts

## Contents

<!-- toc:start -->
- [Global Rules](#global-rules)
- [Minimal Intake Summary](#minimal-intake-summary)
- [Article Readiness Report](#article-readiness-report)
- [Article Context Brief](#article-context-brief)
- [Literature Grounding Report](#literature-grounding-report)
- [Methods Audit Report](#methods-audit-report)
- [Manuscript Draft](#manuscript-draft)
- [Claim Audit Report](#claim-audit-report)
<!-- toc:end -->

Canonical schemas for artifacts passed between `research-article` skills.

## Global Rules

- Every machine-readable artifact includes `schema_version`, `plugin_version`, `artifact_id`, `source_skill`, `status`, and lineage fields when applicable. Read `plugin_version` from the plugin manifest/registry at workflow start.
- Use Markdown for user-facing deliverables; use YAML blocks for agent-to-agent state transfer.
- Use `unknown`, `unclear`, `not_specified`, or `not_applicable` instead of inventing facts.
- Store workflow artifacts in the user's project directory, not inside the skill package.
- Artifact IDs follow `<type>-<NNN>` or the round-specific pattern documented in `artifact-naming-and-directory-rules.md`.
- LLM-facing provenance uses `{artifact_id, version, path}`, complete index membership, and a unique current pointer. Do not require or store SHA-256/content digests. Legacy v6 digest fields may be read and ignored during migration; v7 producers do not write them.
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
  complete_material_inventory:
    - artifact_id: ""
      version: ""
      path: ""
      material_role: semantic_authority | protocol | technical_report | result_output | table | figure | code | references | other
      readiness_relevant: true | false
  semantic_authority:
    artifact_id: ""
    version: ""
    path: ""
    governs: []
    compatible_assets_retained: []
  stated_target_journal: ""
  obvious_missing_items: []
```

## Article Readiness Report

```yaml
article_readiness_report:
  schema_version: "research-article.v7"
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
  material_inventory_coverage: []
  semantic_authority_applied: {}
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
  schema_version: "research-article.v7"
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
    complete_material_inventory: []
    semantic_authority: {}
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
  reader_context:
    target_reader_profile: []
    reader_prior_knowledge: []
    knowledge_asymmetries: []
    terms_requiring_definition: []
    reader_reasoning_chain: []
    source_intent_coverage: []
    binding_constraints: []
    gap_type: knowledge | evidence | method | implementation | mixed | not_applicable
  proceed_status: proceed | proceed_with_assumptions | clarification_stop
```

## Literature Grounding Report

```yaml
literature_grounding_report:
  schema_version: "research-article.v7"
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

## Methods Audit Report

```yaml
methods_audit_report:
  schema_version: "research-article.v7"
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
  working_assumptions:
    - assumption_id: ""
      bounded_assumption: ""
      falsifier: ""
      consequence_if_false: ""
      verification_required: ""
      authoritative_manuscript_location: ""
  recommendation: proceed_to_drafting | fix_methods_text | requires_reanalysis | requires_data_collection | stop
```

## Manuscript Draft

```yaml
manuscript_draft:
  schema_version: "research-article.v7"
  artifact_id: "manuscript-v001"
  source_skill: "article-drafter"
  version: 1
  artifact_completeness: complete
  blueprint_ref: "04_blueprint/article-blueprint.md"
  identity_anchor_ref: "04_blueprint/article-blueprint.md#manuscript_identity_anchor"
  display_manifest_ref: "04_blueprint/display-asset-manifest.yaml"
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

Register the canonical Markdown artifact ID, version, path, index membership, and unique current pointer in workflow state. A current manuscript must contain complete Introduction, Methods, Results, and Discussion sections; a revision delta or changed-section extract is never a manuscript version.

## Claim Audit Report

```yaml
claim_audit_report:
  schema_version: "research-article.v7"
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

For evaluation, revision, panel, cover-letter, and submission contracts, read `artifact-review-and-submission-contracts.md`.
