# Article Editorial Readiness Contracts

Use these schemas after scientific repair and before final article evaluation. The
narrative and language reviewers assess the same frozen reader bundle independently;
their raw reports remain sealed from writers and the evaluator.

```yaml
protected_content_register:
  schema_version: "research-article.v7"
  artifact_id: "protected-content-001"
  source_artifact_refs: []
  identity_anchor: {}
  primary_question_and_answer: {}
  study_object_and_boundary: {}
  data_and_material_availability: []
  methods_estimands_and_validation_logic: []
  claims_and_strength: []
  evidence_status: []
  critical_assumptions: []
  critical_limitations: []
  prohibited_upgrades: []
  source_intent_coverage: []
  binding_constraints: []

editorial_repair_brief:
  schema_version: "research-article.v7"
  artifact_id: "editorial-brief-r001"
  target_artifacts: []
  protected_content_register_ref: ""
  actions:
    - action_id: ""
      source_review: narrative | language
      addresses_findings: []
      priority: critical | major | minor
      artifact_owner: article-drafter | article-frontmatter-drafter
      artifact_locator: ""
      operation: replace | define | move | split | merge | delete | reorder | add_bridge | consolidate
      current_problem: ""
      target_state: ""
      required_content_or_function: ""
      verified_term_replacement: null
      content_to_preserve: []
      content_to_remove_or_move: []
      destination_if_moved: null
      dependencies: []
      acceptance_test: ""
  overlap_resolutions: []
  excluded_actions: []
  validation_status: passed | failed

content_preservation_report:
  schema_version: "research-article.v7"
  artifact_id: "content-preservation-r001"
  source_artifact_refs: []
  revised_artifact_refs: []
  protected_content_register_ref: ""
  decision: scientific_content_preserved | editorial_scope_violation | identity_drift_detected | scientific_change_declared
  protected_item_locations: []
  unsupported_claims_introduced: []
  unresolved_issues: []
```

Every critical or major finding maps to an executable action. A fresh writer can
identify the artifact/location, target function or verified term change, protected and
removed/moved content, dependencies, and observable acceptance test without reading a
raw report. Keep limitations complete at one authoritative location and omit them
elsewhere unless the limitation itself advances the immediate reasoning and omission
would distort it; never add a pointer in place of omitted repetition.
