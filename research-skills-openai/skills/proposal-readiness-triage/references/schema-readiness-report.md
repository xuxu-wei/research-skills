# Readiness Report Field Requirements

This file defines the required fields for a proposal readiness report. It is a structural guide, not executable code.

## Required Fields

### independent_review_metadata

- `review_id`
- `reviewer_skill: proposal-readiness-triage`
- `reviewer_instance_id`
- `workflow_id`
- `round_id`
- `input_artifact_ids`
- `input_versions`
- `files_read`
- `review_scope`
- `isolation_mode: fresh_subagent`
- `prior_scores_visible: false`
- `source_edits_performed: false`

### decision

One of:

- `ready_for_proposal`
- `needs_clarification`
- `needs_idea_refinement`
- `needs_methodology_preflight`
- `not_proposalizable_yet`

### decision_rationale

Brief explanation of why this decision was selected.

### criterion_status

For each core readiness criterion, include:

- criterion name;
- status: `pass`, `concern`, or `fail`;
- brief reason.

### blocking_gaps

List missing or defective items that block the next step.

### non_blocking_gaps

List useful but non-blocking missing details.

### fatal_flaws

List fatal flaws if present. Use an empty list if none are identified.

### minimal_clarification_questions

Only include questions that would change the route decision or unblock drafting.

### recommended_next_skill

One of:

- `proposal-drafter`
- `proposal-context-brief-builder`
- `research-opportunity-mapper`
- `methodology-statistics-preflight`
- `research-idea-orchestrator`
- `idea-evaluator`
- `stop`

### downstream_notes

Short notes for the next skill. Do not include proposal prose.

### sap_notes

Record whether SAP was explicitly requested and whether SAP-specific preflight is needed.

## Style Requirements

- Be concise.
- Use direct language.
- Do not draft proposal sections.
- Do not invent missing facts.
- Separate blocking and non-blocking issues.
