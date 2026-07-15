# Workflow Manifest

Each research-idea run should maintain one manifest per round. The manifest is the workflow-level audit trail; individual artifacts keep content-level lineage.

## Required Fields

```yaml
round_manifest:
  schema_version: "research-idea.v2"
  workflow_id: ""
  plugin_version: ""
  round: 1
  project_directory: ""
  artifact_index_path: "05_state/artifact-index.md"
  user_goal: ""
  intended_output: ""
  selected_strategy: ""
  workflow_status: initialized | preprocessing | artifact_frozen | pending_review | independent_review_pending | revision_required | panel_pending | packaging_pending | blocked | stopped | human_signoff_required
  current_artifact_version: ""
  latest_evaluated_version: ""
  idea_id_namespace:
    canonical_format: "I<round>-<sequence>"
    round_prefix: "I01"
    next_sequence: 1
    normalized_provisional_ids: []
    reserved_or_retired_ids: []
  artifacts:
    input: []
    context_brief: ""
    evidence_packet: ""
    candidate_set_index: ""
    idea_nodes: []
    preflight_reports: []
    evaluation_reports: []
    portfolio: ""
  subagents:
    - role: ""
      skill: ""
      task_boundary: ""
      isolation_required: true
      isolation_confirmed: true | false | not_applicable
      output_ref: ""
  decisions:
    promoted: []
    revise: []
    reframe: []
    merged: []
    rejected: []
    backup: []
  stop_condition: accept_stop | portfolio_stop | no_gain_stop | clarification_stop | reject_stop | evaluation_failure_stop | not_stopped
  unresolved_risks: []
  next_action: ""
```

## Rules

- Create or update the manifest after every generation, preflight, evaluation, and assembly step.
- Maintain the idea ID namespace according to `references/idea-id-and-lineage-rules.md`; do not recycle rejected, backup, or superseded IDs.
- Record failed or invalid subagent outputs; do not overwrite them silently.
- Record the reason for skipping evidence mapping, preflight, or evaluation.
- Store the manifest as `05_state/round-NNN-manifest.md`; use YAML only for agent-to-agent transfer.
- Keep `05_state/artifact-index.md`, node current pointers, and `idea-tree.yaml` synchronized without copying Idea prose into indexes.
- Any changed Idea writes a complete snapshot in the same node and returns to `artifact_frozen`/`pending_review`; panel or portfolio assembly requires a fresh evaluation of that exact digest.
- Return `layout_migration_required` for a legacy layout and do not modify it.
- Permit parallel delegated phases only when each source artifact/version has one writer; reviewer inputs are read-only.

## Canonical Runtime Artifact Record

Every created or revised artifact must register `artifact_id`, `version_id`, `workflow_id`, `round_id`, `plugin_version`, `source_skill`, `created_by_instance_id`, `path`, `based_on`, `change_type`, `status`, `frozen`, and `content_digest`. Workflow-specific aliases such as `idea_id` may supplement but never replace these fields.
