# Workflow Manifest Schema

Create `09_state/workflow-manifest.yaml` at project initialization.

```yaml
project:
  workflow_id: string
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
  latest_evaluated_version: integer | null
  revision_round: integer
  panel_round: integer
  status: initialized | preprocessing | artifact_frozen | pending_review | independent_review_pending | revision_required | panel_pending | packaging_pending | blocked | stopped | human_signoff_required

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
    - artifact_id: string
      version_id: string
      workflow_id: string
      round_id: string
      plugin_version: string
      source_skill: string
      created_by_instance_id: string
      path: path
      based_on: []
      change_type: initial | revision | panel_patch | language_only | formatting_only
      status: current | superseded | stale_after_revision | blocked | final
      frozen: boolean
      content_digest: sha256
      evaluation: path
      delta_report: path
```

Rules:
- Update manifest after every route decision.
- Never overwrite prior draft/evaluation paths.
- Reviewer-class tasks require `delegation_mode: fresh_subagent` and `isolation_level: hard`.
- If fresh delegation is unavailable, set `status: independent_review_pending`, save a self-contained continuation brief, and stop. Do not record soft isolation or continue with inline review.
- Every text change creates a new draft version and returns to `artifact_frozen`/`pending_review`; panel and final composition require a fresh evaluation of that exact version.
- Fatal findings set `blocked`. Parallel phases retain one writer per source artifact/version; reviewers and the final compositor read frozen source artifacts only.
