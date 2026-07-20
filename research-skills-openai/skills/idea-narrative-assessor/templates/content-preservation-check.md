---
schema_version: research-idea-content-preservation-check.v1
check_id: "<check-id>"
review_id: "<review-id>"
reviewer_skill: idea-narrative-assessor
reviewer_instance_id: "<fresh-instance-id>"
workflow_id: "<workflow-id>"
round_id: "<round-id>"
input_artifact_ids: ["<prior-id>", "<revised-id>", "<register-id>", "<delta-id>"]
input_versions: ["<prior-version>", "<revised-version>", "<register-version>", "<delta-version>"]
inputs:
  prior_dossier:
    artifact_id: "<artifact-id>"
    version: "<version>"
    path: "<prior-dossier-path>"
  revised_dossier:
    artifact_id: "<artifact-id>"
    version: "<version>"
    path: "<revised-dossier-path>"
  protected_content_register:
    artifact_id: "<artifact-id>"
    version: "<version>"
    path: "<protected-register-path>"
  revision_delta:
    artifact_id: "<artifact-id>"
    version: "<version>"
    path: "<revision-delta-path>"
files_read:
  - "<prior-dossier-path>"
  - "<revised-dossier-path>"
  - "<protected-register-path>"
  - "<revision-delta-path>"
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
# Repeat exactly once for every protected_id in the frozen register. Do not add IDs.
undeclared_scientific_changes: []
findings: []
unresolved_issues: []
---

# Content-preservation check

## Decision rationale

<Explain the preservation decision without judging scientific quality.>

## Protected-content trace

<Record any nontrivial moves, consolidation, or wording changes and their revised
locations.>

## Required routing

<State whether the dossier may proceed to fresh narrative/language assessment or must
return to scientific review.>
