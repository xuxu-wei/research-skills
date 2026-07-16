# Workflow Manifest

Maintain one audit manifest per round.

```yaml
round_manifest:
  schema_version: research-idea.v3
  workflow_id:
  plugin_version:
  round: 1
  project_directory:
  artifact_index_path: 05_state/artifact-index.md
  user_goal:
  intended_output:
  route_profile: focused_optimization | bounded_exploration
  workflow_status: initialized | preprocessing | artifact_frozen | pending_review | specialist_review_pending | independent_review_pending | clarification_stop | deep_research_handoff_required | revision_required | direction_route_confirmation_required | no_defensible_direction | new_idea_required | panel_pending | packaging_pending | layout_migration_required | blocked | stopped | human_signoff_required | human_direction_selection_required
  current_artifact_version:
  latest_evaluated_version:
  artifacts:
    input: []
    context_brief:
    evidence_packet:
    idea_routing_decision:
    idea_index:
    idea_nodes: []
    idea_dossiers: []
    reference_ledgers: []
    preflight_reports: []
    evaluation_reports: []
    portfolio:
  subagents: []
  decisions: {}
  stop_condition:
  failure_route:
  unresolved_risks: []
  next_action:
```

- Update after generation, remapping, preflight, evaluation, revision, panel,
  and assembly. Preserve failed or invalid delegate outputs.
- Synchronize the artifact index, Idea index, and node pointers without copying
  dossier prose.
- Every changed dossier returns to `artifact_frozen`/`pending_review` and needs a
  fresh evaluation of its exact digest.
- Return `layout_migration_required` for v1/v2 or snapshot layouts; do not edit.
- Preserve component-specific edge outcomes such as `generation_blocked`,
  `evidence_mapping_pending`, `evaluation_failure_stop`, `assembly_blocked`, or
  `proposal_handoff_blocked` in `failure_route`; use a valid pause/terminal
  workflow status and never collapse failure into ready.
- Allow parallel delegation only with one writer per artifact/version and
  read-only reviewer input.

Register every artifact with `artifact_id`, `version_id`, `workflow_id`,
`round_id`, `plugin_version`, `source_skill`, `created_by_instance_id`, `path`,
`based_on`, `change_type`, `status`, `frozen`, and `content_digest`.
