# Output and isolation contract

## Allowed assessment inputs

- one frozen current artifact identified by artifact ID, version, and path; or one
  contract-defined frozen reader bundle identified by one bundle artifact ID/version/
  manifest path plus its declared component artifact IDs, versions, and paths;
- one declared reader-reasoning handoff, file-backed or embedded in the brief;
- the selected profile; and
- this skill's own instructions, references, and templates.

Do not read earlier versions, deltas, preflight or evaluation reports, language
reports, panel outputs, workflow state, artifact indexes, or parent reasoning. An
embedded handoff is not a fictitious file in `files_read`.

## Assessment report

Write `narrative-assessment-rNNN.md`. Required provenance fields are:

```yaml
assessment_id:
review_id:
reviewer_skill: research-narrative-assessor
reviewer_instance_id:
workflow_id:
round_id:
profile: idea | proposal | perspective | article
input_artifact_ids: []
input_versions: []
input_artifact: {artifact_id: "", version: "", path: ""}
input_component_refs: []
reader_handoff: {artifact_id: "", version: "", path: null}
files_read: []
isolation_mode: fresh_subagent
prior_scores_visible: false
source_edits_performed: false
decision: narrative_ready | minor_narrative_revision | major_narrative_revision | clarification_required | independent_review_pending
findings: []
unresolved_issues: []
```

Finding severities are exactly `minor`, `major`, or `clarification`. Finding
categories are exactly:

- `reader_reasoning_chain`
- `section_function`
- `progressive_disclosure`
- `core_element_alignment`
- `authority_and_repetition`
- `counterargument_boundary_authority`
- `navigation_and_backtracking`
- `reader_baseline`

For a single-file artifact, `input_component_refs` is empty. For an Article reader
bundle it includes the current manuscript, current canonical frontmatter, and only the
referenced displays needed to interpret the prose; every component path occurs in
`files_read`.

Each finding needs a stable ID, heading plus recognizable content anchor, observed
evidence, current reader effect, and target function. Do not draft replacement prose.

## YAML repair plan

Always write `narrative-repair-plan-rNNN.yaml`, including when the artifact is ready.
Allowed operations are exactly `replace`, `define`, `move`, `split`, `merge`,
`delete`, `reorder`, `add_bridge`, and `consolidate`.

Each action requires `action_id`, `addresses_findings`, `priority`,
`artifact_locator`, `operation`, `current_problem`, `target_state`,
`required_content_or_function`, `content_to_preserve`,
`content_to_remove_or_move`, `destination_if_moved`, `dependencies`, and
`acceptance_test`. Include `verified_term_replacement: null`; the orchestrator may
populate that field only from a source-supported language-assessment action when it
normalizes the final writer brief. Dependencies may reference only action IDs and must
be acyclic.

Every major finding has an action. `narrative_ready` has empty findings and actions.
For `clarification_required`, list exact missing or conflicting facts under
`clarifications_required`; actions may remain empty.
For `independent_review_pending`, emit no findings or repair actions and return a
self-contained continuation brief.

The plan states a needed definition function and placement only. Exact terminology
replacement, translation, standardity evidence, and first-use wording come from the
language assessor.

For limitation repair, never replace omitted repetitions with pointers. For a
Perspective, every action involving a counterargument or boundary names its family and
the single authority location for that family.
