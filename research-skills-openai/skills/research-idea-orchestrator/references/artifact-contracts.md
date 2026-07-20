# Research-Idea Artifact Contracts

## Contents

<!-- toc:start -->
- [Global fields](#global-fields)
- [Research context](#research-context)
- [Evidence, opportunity, and route](#evidence-opportunity-and-route)
- [Idea dossier, node, index, and ledger](#idea-dossier-node-index-and-ledger)
- [Methodology preflight](#methodology-preflight)
- [Editorial readiness and preservation](#editorial-readiness-and-preservation)
- [Independent evaluation](#independent-evaluation)
- [Downstream journal-review and portfolio contracts](#downstream-journal-review-and-portfolio-contracts)
<!-- toc:end -->

This reference defines shared `research-idea.v3` field names. User-facing prose
belongs in Markdown; YAML carries pointers, state, and lineage.

## Global fields

For every persisted artifact, the workflow artifact index records
`schema_version`, `plugin_version`, `source_skill`, artifact/version/workflow/
round IDs, path, `based_on`, and `change_type`. Self-contained artifacts
repeat fields required by their schema; mutable node/state pointers need not.
Use `unknown` or `not_applicable` instead of invented facts. Store artifacts in
the user's project, never in the plugin package.

## Research context

```yaml
research_context_brief:
  schema_version: research-idea.v3
  artifact_id:
  input_type: problem
  problem_subtype: broad_direction | raw_idea | clinical_problem | practical_problem | data_asset | method_asset | funding_call | literature_material | mixed | unclear
  research_domain:
  user_goal:
  intended_output:
  target_reader_profile: {disciplines: [], intended_use: ""}
  reader_prior_knowledge:
    assumed_known: []
    requires_first_use_explanation: []
  reader_reasoning_chain:
    background: ""
    current_state: ""
    gap: ""
    significance: ""
    rationale: ""
  gap_type:
  study_object:
  setting_or_context:
  available_data: {summary: "", access_status: not_specified, limitations: []}
  available_methods: {summary: "", maturity: not_specified}
  endpoint_or_metric: {known_items: [], status: unclear, notes: ""}
  constraints: {time: "", resources: "", collaboration: ""}
  known_facts: []
  assumptions: []
  uncertainties: []
  direction_clarity: clear | underdefined | ambiguous
  direction_clarity_rationale:
  proceed_status: proceed | proceed_with_assumptions | clarification_stop
  downstream_needs: {}
```

## Evidence, opportunity, and route

```yaml
evidence_packet:
  schema_version: research-idea.v3
  artifact_id:
  evidence_status: user_provided | auto_retrieved | mixed | skipped | not_verified
  evidence_map_ref:
  opportunity_map_ref:
  core_findings: []
  limitations: []
  scientific_gap:
    unanswered_problem:
    missing_knowledge_or_evidence:
    consequence:
    supporting_sources: []
  novelty_positioning:
    closest_work: []
    overlap:
    differentiation:
    novelty_risk:
  reader_reasoning_handoff:
    background:
    current_state:
    gap:
    significance:
    rationale:

idea_routing_decision:
  schema_version: research-idea.v3
  artifact_id:
  direction_clarity: clear | underdefined | ambiguous
  current_direction_value: supported | uncertain | unsupported
  evidence_confidence: high | moderate | low
  distinct_supported_directions: []
  route: focused_optimization | bounded_exploration | direction_route_confirmation_required | no_defensible_direction
  rationale:
```

Internal evidence/opportunity IDs require a human-readable label and a ledger
entry. They must not appear as evidence in the dossier.

## Idea dossier, node, index, and ledger

The authoritative body is
`03_ideas/nodes/<idea-id>/dossiers/idea-dossier-vNNN.md`. Follow
`idea-artifact-lifecycle.md` and `idea-dossier-contract.md`.

```yaml
idea_dossier_frontmatter:
  schema_version: research-idea.v3
  plugin_version:
  artifact_id:
  workflow_id:
  idea_id:
  version_id: v001
  path: 03_ideas/nodes/<idea-id>/dossiers/idea-dossier-v001.md
  parent_idea_ids: []
  based_on: []
  source_skill: multi-path-idea-generator
  created_round: 1
  change_type: create | revise | evidence_claim_sync | editorial_reposition | editorial_repair
  identity_anchor: {primary_research_question: "", primary_objective: "", study_object: "", core_data_or_evidence_base: "", primary_unit_of_inference: ""}
  frozen: true

idea_node:
  current_dossier_id:
  current_version:
  current_path:
  reference_ledger_path: <idea-node>/references/reference-ledger.md
  parent_idea_ids: []
  lineage_id:
  route_profile: focused_optimization | bounded_exploration
  identity_anchor: {primary_research_question: "", primary_objective: "", study_object: "", core_data_or_evidence_base: "", primary_unit_of_inference: ""}
  identity_status: preserved | drifted
  qualifying_evaluation_ref:

idea_index_entry:
  idea_id:
  dossier_id:
  node_path:
  dossier_path:
  dossier_version:
  parent_idea_ids: []
  lineage_id:
  route_profile: focused_optimization | bounded_exploration
  remap_status: not_required | required | complete | structural_revision_required
  status:
```

`reference_ledger` is the node-level Markdown navigation table defined in
`reference-ledger-contract.md`; it is not reviewer evidence.

## Methodology preflight

```yaml
methodology_statistics_preflight:
  schema_version: research-idea.v3
  preflight_id:
  idea_id:
  dossier_ref:
  endpoint_or_metric_status: clear | partially_clear | unclear | invalid | not_applicable
  data_method_fit: strong | acceptable | weak | invalid | not_applicable
  minimal_analysis_route_status: clear | partially_clear | unclear | invalid
  feasibility_blockers: []
  recommendation: pass | revise_endpoint_or_metric | revise_data_source | revise_method | revise_analysis_route | needs_clarification | blocked | out_of_scope
  idea_handoff_decision: proceed | proceed_with_assumptions | clarification_stop
  working_assumptions: []
  repair_directions: []
```

## Editorial readiness and preservation

```yaml
narrative_assessment:
  input_dossier: {artifact_id: "", version: "", path: ""}
  reader_handoff: {artifact_id: embedded-reader-handoff, version: embedded, path: null}
  files_read: []
  decision: narrative_ready | minor_narrative_revision | major_narrative_revision | clarification_required
  findings: []
  repair_plan_pairing: same_assessment_id_and_source_assessment

language_assessment:
  dossier_ref: {artifact_id: "", version: "", path: ""}
  reader_handoff: {artifact_id: embedded-reader-handoff, version: embedded, path: null}
  scope: complete_idea_dossier
  decision: submission_ready | minor_language_revision | major_language_revision | needs_professional_editing | clarification_required | independent_review_pending
  terminology_findings: []

editorial_repair_writer_brief:
  schema_version: research-idea-editorial-repair-writer-brief.v1
  brief_id:
  source_artifact: {artifact_id: "", version: "", path: ""}
  protected_content_register: {register_id: "", version: "", path: ""}
  source_review_binding:
    narrative_assessment: {artifact_id: "", version: "", path: ""}
    narrative_repair_plan: {artifact_id: "", version: "", path: ""}
    language_assessment: {artifact_id: "", version: "", path: ""}
  included_repair_item_ids: []
  omitted_reported_nonblocking_findings: []
  included_nonblocking_finding_rationale: {}
  writer_access:
    allowed_reads: []
    forbidden_reads: []
    allowed_writes: {complete_dossier: {}, revision_delta: {}}
  overlap_dispositions: []
  all_overlaps_resolved: false
  normalized_repair_actions:
    - {repair_item_id: "", source_item_ids: [], addresses_finding_ids: [], locator: "", operation: "", problem: "", target: "", required_function_or_term: "", content_to_preserve: {protected_ids: []}, delete_move_disposition: "", destination: null, dependencies: [], acceptance_test: ""}
  mandatory_whole_dossier_checks: {}
  execution_and_handoff:
    single_complete_target_dossier: true
    partial_artifacts_forbidden: true
    pre_freeze_action_compliance_required: true
    delta_after_dossier_freeze_only: true

content_preservation_review:
  old_dossier_ref: {artifact_id: "", version: "", path: ""}
  new_dossier_ref: {artifact_id: "", version: "", path: ""}
  protected_register_ref: {artifact_id: "", version: "", path: ""}
  decision: scientific_content_preserved | editorial_scope_violation | identity_drift_detected | scientific_change_declared
```

## Independent evaluation

```yaml
idea_evaluation:
  schema_version: research-idea.v3
  review_id:
  reviewer_skill: idea-evaluator
  reviewer_instance_id:
  workflow_id:
  round_id:
  idea_id:
  input_artifact_ids: []
  input_versions: []
  files_read: []
  review_scope: complete_idea_dossier
  isolation_mode: fresh_subagent
  prior_scores_visible: false
  prior_versions_visible: false
  revision_delta_visible: false
  source_edits_performed: false
  reviewed_dossier_ref: {artifact_id: "", version: "", path: ""}
  complete_dossier_confirmed: true
  dossier_only_input_confirmed: true
  identity_drift_detected: false
  historical_identity_drift_assessed: false
  evidence_chain_checks: {}
  claim_support_checks: {}
  dimension_scores: {}
  overall_score_simple_average: 0
  hard_gates: {}
  fatal_flaws: []
  findings:
    - title:
      dossier_locator:
      severity:
      rationale:
  decision: promote | revise_then_promote | revise | reframe | keep_as_backup | reject
  repair_directions: []
  limitations: []
  unresolved_issues: []
```

`files_read` lists project artifacts and must contain exactly the current
dossier path. Skill instructions and rubric references are not project inputs.

## Downstream journal-review and portfolio contracts

Read `journal-review-and-portfolio-artifacts.md` only when creating, reviewing,
or packaging a candidate journal match, medical journal review, lineage record,
or portfolio navigation entry.
