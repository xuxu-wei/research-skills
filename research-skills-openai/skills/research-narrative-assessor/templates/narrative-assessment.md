---
schema_version: research-narrative-assessment.v1
assessment_id: "<assessment-id>"
review_id: "<review-id>"
reviewer_skill: research-narrative-assessor
reviewer_instance_id: "<fresh-instance-id>"
workflow_id: "<workflow-id>"
round_id: "<round-id>"
profile: "<idea | proposal | perspective | article>"
input_artifact_ids: ["<artifact-id>"]
input_versions: ["<version>"]
input_artifact: {artifact_id: "<artifact-id>", version: "<version>", path: "<path>"}
input_component_refs: []
reader_handoff: {artifact_id: "embedded-reader-handoff", version: "embedded", path: null}
files_read: ["<artifact-path>"]
isolation_mode: fresh_subagent
prior_scores_visible: false
source_edits_performed: false
decision: major_narrative_revision
findings:
  - finding_id: NAR-001
    severity: major
    category: reader_reasoning_chain
    artifact_locator:
      section_heading: "<heading>"
      subsection_heading: null
      content_anchor: "<recognizable paragraph, table, or function>"
    observed_evidence: "<what the artifact does>"
    current_reader_effect: "<effect on declared readers>"
    target_function: "<reader-facing function required>"
unresolved_issues: []
---

# Narrative assessment

## Overall judgment

<Explain the decision and the reader's route without evaluating scientific merit.>

## Findings

<Explain each structured finding without drafting replacement prose.>

## Preserved strengths

<Identify functions that repair must retain.>

## Handoff

See the paired YAML repair plan for executable actions.
