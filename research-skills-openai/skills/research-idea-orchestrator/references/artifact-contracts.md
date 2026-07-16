# Research-Idea Artifact Contracts

## Contents

<!-- toc:start -->
- [Global fields](#global-fields)
- [Research context](#research-context)
- [Evidence, opportunity, and route](#evidence-opportunity-and-route)
- [Idea dossier, node, index, and ledger](#idea-dossier-node-index-and-ledger)
- [Methodology preflight](#methodology-preflight)
- [Independent evaluation](#independent-evaluation)
- [Lineage and portfolio navigation](#lineage-and-portfolio-navigation)
<!-- toc:end -->

This reference defines shared `research-idea.v3` field names. User-facing prose
belongs in Markdown; YAML carries pointers, state, and lineage.

## Global fields

For every persisted artifact, the workflow artifact index records
`schema_version`, `plugin_version`, `source_skill`, artifact/version/workflow/
round IDs, path, digest, `based_on`, and `change_type`. Self-contained artifacts
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
  target_audience_or_reviewer:
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
  evidence_limitations_ref:
  core_findings: []
  limitations: []

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
  parent_idea_ids: []
  based_on: []
  source_skill: multi-path-idea-generator
  created_round: 1
  change_type: create | revise | evidence_claim_sync | editorial_reposition
  identity_anchor:
    primary_research_question:
    primary_objective:
    study_object:
    core_data_or_evidence_base:
    primary_unit_of_inference:
  frozen: true

idea_node:
  current_dossier_id:
  current_version:
  current_path:
  current_digest: "sha256:"
  reference_ledger_path: <idea-node>/references/reference-ledger.md
  parent_idea_ids: []
  lineage_id:
  route_profile: focused_optimization | bounded_exploration
  identity_anchor:
    primary_research_question:
    primary_objective:
    study_object:
    core_data_or_evidence_base:
    primary_unit_of_inference:
  identity_status: preserved | drifted
  qualifying_evaluation_ref:

idea_index_entry:
  idea_id:
  dossier_id:
  node_path:
  dossier_path:
  dossier_version:
  dossier_digest: "sha256:"
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
  repair_directions: []
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
  reviewed_dossier_digest: "sha256:"
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

## Lineage and portfolio navigation

```yaml
idea_lineage_record:
  schema_version: research-idea.v3
  lineage_id:
  idea_id:
  parent_idea_ids: []
  route_profile: focused_optimization | bounded_exploration
  change_type: create | revise | evidence_claim_sync | editorial_reposition
  decision_history: []

portfolio_navigation_entry:
  idea_id:
  title:
  dossier_ref:
  dossier_version:
  dossier_digest: "sha256:"
  evaluation_ref:
  reference_ledger_ref:
  status:
  fatal_or_blocking_findings: []
  dissent: []
  unresolved_issues: []
  next_human_action:
```

The portfolio links the qualifying dossier and never serializes its body again.
