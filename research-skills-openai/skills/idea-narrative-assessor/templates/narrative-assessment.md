---
schema_version: research-idea-narrative-assessment.v1
assessment_id: "<assessment-id>"
review_id: "<review-id>"
reviewer_skill: idea-narrative-assessor
reviewer_instance_id: "<fresh-instance-id>"
workflow_id: "<workflow-id>"
round_id: "<round-id>"
input_artifact_ids: ["<artifact-id>"]
input_versions: ["<version>"]
input_dossier:
  artifact_id: "<artifact-id>"
  version: "<version>"
  path: "<path>"
reader_handoff:
  artifact_id: embedded-reader-handoff
  version: embedded
  path: null
files_read:
  - "<path>"
isolation_mode: fresh_subagent
prior_scores_visible: false
forbidden_project_artifacts_read: false
source_edits_performed: false
decision: major_narrative_revision
findings:
  - finding_id: NAR-001
    severity: major
    category: "<category>"
    dossier_locator:
      section_heading: "<heading>"
      subsection_heading: "<subheading-or-null>"
      content_anchor: "<recognizable opening phrase, table, or paragraph function>"
    observed_evidence: "<what the dossier does>"
    current_reader_effect: "<effect on the declared reader>"
    target_function: "<reader-facing function that must be achieved>"
unresolved_issues: []
---

# Narrative assessment

## Overall judgment

<Explain the decision and the reader's current route through the dossier.>

## Findings

<Explain each structured finding without drafting replacement dossier prose.>

## Preserved strengths

<Identify narrative functions that should remain intact during repair.>

## Handoff

See the paired `narrative-repair-plan-rNNN.yaml` for executable actions.
