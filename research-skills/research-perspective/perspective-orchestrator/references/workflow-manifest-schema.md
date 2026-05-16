# Workflow Manifest Schema

Create `workflow-manifest.yaml` at project initialization.

```yaml
project:
  name: string
  root: string
  mode: lite | standard | full
  created_at: ISO-8601
  runtime_adapter: hermes-delegate-task | codex-subagent | manual
  isolation_level: hard | soft

state:
  current_step: string
  current_route: string
  current_draft_version: integer
  revision_round: integer
  panel_round: integer
  status: active | stopped | complete

artifacts:
  input_brief: path
  target_outlet_profile: path
  claim_ledger: path
  claim_evidence_matrix: path
  argument_skeleton: path
  current_draft: path
  current_paragraph_map: path
  latest_evaluation: path
  panel_summary: path
  final_manuscript: path

decisions:
  latest_decision_id: string
  user_confirmation_required: boolean
  unresolved_issues_count: integer

lineage:
  drafts:
    - version: integer
      path: path
      basis: fresh | revision | panel_patch
      evaluation: path
      delta_report: path
```

Rules:
- Update manifest after every route decision.
- Never overwrite prior draft/evaluation paths.
- If isolation is only soft, record it in `runtime_adapter` and `isolation_level`.

