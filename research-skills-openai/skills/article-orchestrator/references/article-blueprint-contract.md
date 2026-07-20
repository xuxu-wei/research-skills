# Article Blueprint Contract

Use this schema when `article-architect` creates or validates the pre-drafting
blueprint.

```yaml
article_blueprint:
  schema_version: "research-article.v7"
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
  manuscript_identity_anchor:
    central_question: ""
    primary_contribution: ""
    main_answer: ""
    study_object: ""
    core_evidence_basis: ""
    source_intent_coverage: []
    binding_constraints: []
  claim_evidence_matrix: []
  evidence_provenance_ledger_ref: "04_blueprint/evidence-provenance-ledger.md"
  evidence_display_plan: []
  display_asset_manifest_ref: "04_blueprint/display-asset-manifest.yaml"
  supplementary_index:
    items: []
    journal_limits:
      max_supplementary_items: 0
      max_supplementary_files: 0
      supplementary_file_format: ""
      data_availability_policy: ""
      code_availability_policy: ""
  reader_profile: {}
  section_content_plan:
    - section_id: ""
      rhetorical_function: ""
      reader_question_answered: ""
      required_content: []
      prior_knowledge_assumed: []
      definitions_before_use: []
      handoff_to_next_section: ""
      content_that_belongs_elsewhere: []
  authoritative_content_locations:
    - content_family: analytical_assumptions | limitations | other
      location: ""
      exception_rule: "omit elsewhere unless directly necessary to advance immediate reasoning and omission would distort it"
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
