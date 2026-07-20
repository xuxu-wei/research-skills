# Workflow Manifest Schema

Create `09_state/workflow-manifest.yaml` at project initialization.

## Contents

- [Manifest Schema](#manifest-schema)
- [Rules](#rules)

## Manifest Schema

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
  current_draft_version: string
  latest_evaluated_version: string | null
  revision_round: integer
  panel_round: integer
  status: initialized | preprocessing | artifact_frozen | pending_review | independent_review_pending | revision_required | panel_pending | editorial_assessment_pending | editorial_repair_pending | preservation_pending | editorial_reassessment_pending | final_evaluation_pending | specialist_review_pending | packaging_pending | outlet_targeting_only | blocked | stopped | human_signoff_required

artifacts:
  input_brief: {artifact_id: string, version: string, path: path}
  target_outlet_profile: {artifact_id: string, version: string, path: path}
  claim_ledger: {artifact_id: string, version: string, path: path}
  claim_evidence_matrix: {artifact_id: string, version: string, path: path}
  argument_skeleton: {artifact_id: string, version: string, path: path}
  reader_reasoning_handoff:
    artifact_id: string
    version: string
    path: null
    payload:
      declared_readers: [string]
      assumed_prior_knowledge: [string]
      knowledge_to_introduce: [string]
      intended_reader_shift: string
      terminology_disclosure_order:
        - concept: string
          depends_on: [string]
          introduce_before_or_at: string
      reasoning_route:
        tension: string
        core_judgment: string
        argument: string
        counterposition_or_boundary: string
        implication: string
  current_draft: {artifact_id: string, version: string, path: path}
  current_paragraph_map: {artifact_id: string, version: string, path: path}
  pre_evaluation_conformance: {artifact_id: string, version: string, path: path}
  latest_evaluation: {artifact_id: string, version: string, path: path}
  panel_summary: {artifact_id: string, version: string, path: path}
  protected_content_register: {artifact_id: string, version: string, path: path}
  narrative_assessment: {artifact_id: string, version: string, path: path}
  language_assessment: {artifact_id: string, version: string, path: path}
  editorial_repair_brief: {artifact_id: string, version: string, path: path}
  editorial_conformance_check: {artifact_id: string, version: string, path: path}
  content_preservation_report: {artifact_id: string, version: string, path: path}
  narrative_reassessment: {artifact_id: string, version: string, path: path}
  language_reassessment: {artifact_id: string, version: string, path: path}
  final_evaluation: {artifact_id: string, version: string, path: path}
  candidate_journal_match_brief: {artifact_id: string, version: string, path: path}
  cover_letter: {artifact_id: string, version: string, path: path}
  cover_letter_quality_check: {artifact_id: string, version: string, path: path}
  medical_journal_review: {artifact_id: string, version: string, path: path}
  final_manuscript: {artifact_id: string, version: string, path: path}

decisions:
  latest_decision_id: string
  user_confirmation_required: boolean
  unresolved_issues_count: integer

lineage:
  drafts:
    - artifact_id: string
      version: string
      path: path
      workflow_id: string
      round_id: string
      plugin_version: string
      source_skill: string
      created_by_instance_id: string
      writer_instance_id: string
      based_on:
        - {artifact_id: string, version: string, path: path}
      change_type: initial | revision | panel_patch | editorial_repair | language_only | formatting_only
      status: current | superseded | stale_after_revision | blocked | final
      frozen: boolean
      evaluation: {artifact_id: string, version: string, path: path}
      delta_report: {artifact_id: string, version: string, path: path}
```

## Rules

- Update manifest after every route decision.
- Every present file-backed artifact, lineage link, evaluation, and delta uses exactly
  `{artifact_id, version, path}`. Omit an unavailable optional entry or set the whole
  entry to `null`; never substitute a bare path.
- Never overwrite prior draft/evaluation paths.
- Reviewer-class tasks require `delegation_mode: fresh_subagent` and `isolation_level: hard`.
- If fresh delegation is unavailable, set `status: independent_review_pending`, save a self-contained continuation brief, and stop. Do not record soft isolation or continue with inline review.
- Every text change creates a new draft version and returns to `artifact_frozen`/`pending_review`; panel and final composition require a fresh evaluation of that exact version.
- Editorial repair additionally requires the frozen scientific writer identity, single normalized brief, deterministic conformance, fresh content preservation, and fresh narrative/language reassessment before final evaluation.
- Copy the complete embedded reader-handoff payload into an applicable delegate brief; delegates do not read the workflow manifest, input brief, or skeleton to reconstruct it.
- Final evaluation binds only the final Perspective and clean minimal evidence/outlet facts; no repair, plan, ledger, map, readiness, state, or prior-review artifact enters its isolation package.
- Fatal findings set `blocked`. Parallel phases retain one writer per source artifact/version; reviewers and the final compositor read frozen source artifacts only.
- New LLM-facing state and lineage use `{artifact_id, version, path}` plus complete artifact-index membership. Read legacy `version_id`, `current_artifact_path`, or `content_digest` fields when present, normalize only the first two to `version` and `path`, and never validate, copy forward, or gate on a digest.
