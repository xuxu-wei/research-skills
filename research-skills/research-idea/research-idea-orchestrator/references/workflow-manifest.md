# Workflow Manifest

Each research-idea run should maintain one manifest per round. The manifest is the workflow-level audit trail; individual artifacts keep content-level lineage.

## Required Fields

```yaml
round_manifest:
  schema_version: "research-idea.v1"
  round: 1
  project_directory: ""
  artifact_index_path: "09_state/artifact-index.md"
  user_goal: ""
  intended_output: ""
  selected_strategy: ""
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
    generated_idea_set: ""
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
- Store the manifest in the user project directory as `09_state/round-<n>-manifest.md` or YAML only when used for agent-to-agent transfer.
- Keep `09_state/artifact-index.md` synchronized with generated idea, preflight, evaluation, adversarial, portfolio, handoff, and language QA artifacts.
