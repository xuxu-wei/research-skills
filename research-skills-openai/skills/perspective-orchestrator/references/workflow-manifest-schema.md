# Workflow Manifest Schema

Create `09_state/workflow-manifest.yaml` at project initialization.

```yaml
project:
  name: string
  root: string
  mode: lite | standard | full
  plugin_version: string
  created_at: ISO-8601
  delegation_mode: fresh_subagent | unavailable
  isolation_level: hard | pending

state:
  current_step: string
  current_route: string
  current_draft_version: integer
  revision_round: integer
  panel_round: integer
  status: active | independent_review_pending | stopped | complete

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
- Reviewer-class tasks require `delegation_mode: fresh_subagent` and `isolation_level: hard`.
- If fresh delegation is unavailable, set `status: independent_review_pending`, save a self-contained continuation brief, and stop. Do not record soft isolation or continue with inline review.
