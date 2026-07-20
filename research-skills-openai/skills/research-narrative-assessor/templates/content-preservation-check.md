---
schema_version: research-content-preservation-check.v1
check_id: "<check-id>"
review_id: "<review-id>"
reviewer_skill: research-narrative-assessor
reviewer_instance_id: "<fresh-instance-id>"
workflow_id: "<workflow-id>"
round_id: "<round-id>"
profile: "<idea | proposal | perspective | article>"
input_artifact_ids: ["<prior-id>", "<revised-id>", "<register-id>", "<delta-id>"]
input_versions: ["<prior-version>", "<revised-version>", "<register-version>", "<delta-version>"]
inputs:
  prior_artifact: {artifact_id: "<id>", version: "<version>", path: "<path>"}
  revised_artifact: {artifact_id: "<id>", version: "<version>", path: "<path>"}
  protected_content_register: {artifact_id: "<id>", version: "<version>", path: "<path>"}
  revision_delta: {artifact_id: "<id>", version: "<version>", path: "<path>"}
files_read: ["<prior-path>", "<revised-path>", "<register-path>", "<delta-path>"]
isolation_mode: fresh_subagent
prior_scores_visible: false
source_edits_performed: false
decision: scientific_content_preserved
protected_item_checks:
  - protected_id: PCR-001
    prior_locator: "<locator>"
    revised_locator: "<locator>"
    semantic_status: preserved
    evidence: "<comparison evidence>"
undeclared_scientific_changes: []
findings: []
unresolved_issues: []
---

# Content-preservation check

## Decision rationale

<Explain the preservation decision without judging scientific quality.>

## Protected-content trace

<Record nontrivial moves, consolidation, and family-authority locations.>

## Required routing

<State whether the artifact may proceed to fresh narrative and language assessment or
must return to scientific review.>
