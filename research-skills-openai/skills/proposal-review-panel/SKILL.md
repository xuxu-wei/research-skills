---
name: proposal-review-panel
description: "Run an isolated multi-reviewer proposal review panel for a proposal file after proposal evaluation has passed or when the user explicitly requests mock review. Supports blind mock review by default and context-aware internal advisory review only when explicitly selected."
---
# proposal-review-panel

## Independent Execution Contract

- Run each selected reviewer role as a separate instance of this skill in its own fresh independent subagent or delegated thread. Never run a role in the context that generated, drafted, or revised the proposal being reviewed, and never run the panel as one large reviewer.
- Require frozen input artifact IDs, file paths, and versions before review. Treat all source artifacts as read-only.
- Write only the assigned individual review report. The orchestrator alone aggregates sealed reports into a panel summary. Do not draft, rewrite, polish, fix, or otherwise modify any reviewed source.
- Do not use the parent task's hidden reasoning or expected answer. Individual reviewers must not receive any other evaluator/reviewer output.
- Every individual reviewer report must list the exact files read and its review scope.
- If fresh independent execution cannot be created for every selected reviewer role, return `independent_review_pending` with a self-contained continuation brief and stop. Never fall back to inline review, and never emit a supportive/final recommendation.

### Required Review Report Provenance

Every individual review must contain: `review_id`, `reviewer_skill`, `reviewer_instance_id`, `workflow_id`, `round_id`, `input_artifact_ids`, `input_versions`, `files_read`, `isolation_mode: fresh_subagent`, `prior_scores_visible: false`, `source_edits_performed: false`, `decision`, `findings`, and `unresolved_issues`.

## When to Use

Use this skill when a proposal file has passed `proposal-evaluator` gate, or when the user explicitly requests mock review, grant review simulation, peer-review simulation, internal advisory review, or pre-submission critique.

This skill simulates a multi-role reviewer panel. It does not draft, revise, or directly modify the proposal.

## Review Modes

### blind_mock_review

Default mode. Individual reviewers review only the proposal file and review scenario.

Do not pass individual reviewers:

- proposal context brief;
- proposal evaluation report;
- revision delta report;
- unresolved issues;
- other reviewer reports.

This mode best simulates outside reviewers who judge the proposal as submitted.

### context_aware_internal_review

Use only when the user explicitly asks for internal advisory review using background materials.

The report must be labeled `context_aware_internal_review`, not blind/mock peer review. Briefs must state which extra materials were provided and how that limits comparison to real external review.

## Core Principles

- Every individual reviewer must run as an isolated subagent.
- Reviewers must not see each other's scores, comments, or conclusions before writing their own reports.
- Panel size must be explicit: `lightweight_panel` (3 reviewers), `standard_panel` (5 reviewers, default), or `full_panel` (7 reviewers).
- Every panel tier includes a domain expert, methodology/statistics reviewer, and submission-guard reviewer.
- Medicine, clinical practice, or public health proposals must use `practicing-clinician reviewer` as the domain expert role.
- The orchestrator-owned panel summary must preserve dissent, minority objections, and high-severity reviewer concerns.
- This skill defines role-specific review execution and aggregation policy; the orchestrator aggregates sealed reports and does not change the proposal file.

## Inputs

Usually supplied by `proposal-orchestrator`:

- `proposal_file_path`
- `proposal_version`
- user goal and target output
- review scenario or funding call, if any
- review mode: `blind_mock_review` by default
- panel tier: `standard_panel` by default
- optional `sap_file_path` only when user explicitly requests proposal + SAP review

For `blind_mock_review`, hold context brief, evaluation report, revision delta report, and unresolved issues at the orchestrator level only; do not pass them to individual reviewers.

## Outputs

- one assigned individual reviewer report per fresh instance;
- orchestrator-owned panel summary report after all sealed reports return;
- consensus strengths and weaknesses;
- reviewer disagreements;
- skeptical objections;
- submission-guard cleanup findings;
- must-fix items with category tags;
- optional improvements;
- final recommendation;
- recommended next step.

Do not output a revised proposal.

## Must-Fix Item Classification

Every must-fix item in individual reports and panel summary must include one prefix:

- `[evidence]`: claim lacks evidence, citation, or data support.
- `[clarity]`: wording or structure is unclear but content is otherwise sound.
- `[substance]`: substantive problem in method, scope, feasibility, logic, endpoint, or design.
- `[other]`: does not fit the above categories.

## Panel Tiers

### lightweight_panel

Use for fast pre-submission critique, early mock review, or when the user asks for a smaller panel.

Three reviewers:

- domain expert reviewer (`narrow-domain reviewer`, or `practicing-clinician reviewer` for medicine, clinical practice, or public health);
- methodology / statistics reviewer;
- submission-guard reviewer.

### standard_panel

Default tier for proposal mock review.

Five reviewers:

- broad-field reviewer;
- domain expert reviewer (`narrow-domain reviewer`, or `practicing-clinician reviewer` for medicine, clinical practice, or public health);
- methodology / statistics reviewer;
- skeptical reviewer;
- submission-guard reviewer.

### full_panel

Use for high-stakes grant, protocol, or submission-readiness review.

Seven reviewers:

- broad-field reviewer;
- domain expert reviewer (`narrow-domain reviewer`, or `practicing-clinician reviewer` for medicine, clinical practice, or public health);
- methodology / statistics reviewer;
- cross-disciplinary senior reviewer;
- translational / end-user reviewer;
- skeptical reviewer;
- submission-guard reviewer.

The skeptical reviewer may be disabled only when the user explicitly requests that, but disabling it downgrades the panel confidence. The submission-guard reviewer must not be removed.

## Procedure

### 1. Confirm Review Scope

Set:

- review mode: `blind_mock_review` or `context_aware_internal_review`;
- review scope: proposal only, proposal + SAP, grant-style, paper-style, protocol-style, or internal advisory;
- panel tier: `lightweight_panel`, `standard_panel`, or `full_panel`;
- reviewer set.

If the proposal has not passed proposal evaluation and the user did not explicitly request early mock review, stop and return a scope issue.

### 2. Prepare Reviewer Briefs

Use `proposal-orchestrator/references/delegate-brief-templates.md`.

For blind review, every brief must include only:

- reviewer role and primary concerns;
- `proposal_file_path`;
- `proposal_version`;
- user goal and target output;
- funding call or review scenario;
- review scope;
- explicit independence rules;
- explicit forbidden-context note.

For context-aware internal review, list every extra material provided and label the mode clearly.

### 3. Orchestrator Delegates Independent Reviews

The orchestrator creates one fresh independent subagent or delegated thread per selected reviewer role and starts all reviewer tasks in parallel. An individual reviewer instance must not spawn or coordinate other reviewers.

The orchestrator waits for all reviewer tasks before aggregation. Reviewers produce individual reports independently and cannot see one another's work.

### 4. Assigned Reviewer Produces Its Individual Review

Each reviewer returns a report that includes:

- reviewer role;
- overall assessment;
- major strengths;
- major weaknesses;
- role-specific concerns;
- must-fix items;
- optional suggestions;
- recommendation;
- confidence or limitation note.

Mark reports as low confidence when they ignore role boundaries or rely on forbidden context.

### 5. Orchestrator Aggregates Panel Findings

After every sealed report returns, the orchestrator creates a panel summary that separates:

- consensus strengths;
- consensus weaknesses;
- reviewer disagreements;
- skeptical objections;
- submission-guard cleanup findings;
- must-fix before submission;
- optional improvements;
- unresolved risks;
- likely reviewer attack points.

The orchestrator uses `references/policy-panel-aggregation-format.md` to consolidate duplicated must-fix items into actionable grouped findings.

### 6. Orchestrator Produces Final Recommendation

Return one recommendation:

- `strong_support`
- `support_with_minor_revision`
- `support_after_major_revision`
- `revise_and_resubmit`
- `not_ready`
- `reject_or_redesign`

A credible `FATAL` or blocking finding forbids `strong_support` and `support_with_minor_revision`. If fixable, route to major revision or revise-and-resubmit; if the required repair cannot be completed from available artifacts, return `not_ready`; if unfixable, return `reject_or_redesign`.

Explain the rationale and next step. Do not directly revise the proposal.

### 7. Orchestrator Handoff

Return to `proposal-orchestrator`:

- panel summary report;
- individual reviewer report paths or summaries;
- final recommendation;
- must-fix items;
- skeptical objections;
- submission-guard cleanup findings;
- unresolved issues;
- recommended next step.

## Delegation Rules

The following must each be assigned to a separate fresh independent subagent or delegated thread:

- each individual reviewer;
- skeptical review;
- submission-guard review;
- methodology/statistics review;
- translational/end-user review;
- practicing-clinician review when applicable.

Only the orchestrator may synthesize reviewer outputs, and it must not rewrite reviewer opinions into false consensus.

## Stop Conditions

- Missing `proposal_file_path`.
- Proposal file cannot be read.
- Proposal has not passed evaluator gate and user did not request early mock review.
- User requests SAP review but SAP file is missing.
- Reviewer brief lacks review goal, role, or independence rules.
- Reviewer independence cannot be preserved.

## Pitfalls

- Do not pass context brief or previous evaluation materials to blind reviewers.
- Do not delete skeptical reviewer unless user explicitly asks.
- Do not delete submission-guard reviewer.
- Do not average away serious dissent.
- Do not directly modify proposal files.
- Do not treat polite support as submission readiness.
- Do not review SAP unless requested.

## Verification

- Review mode is explicit.
- `proposal_file_path` and `proposal_version` are present.
- Every reviewer ran independently.
- Default panel includes skeptical and submission-guard reviewers.
- Default tier is `standard_panel` with five reviewers.
- Lightweight tier has exactly three reviewers and includes domain expert, methodology/statistics, and submission-guard.
- Full tier has seven reviewers.
- Medical/clinical/public-health proposals use practicing-clinician reviewer as the domain expert role.
- Individual reviewer reports were collected.
- Panel summary preserves disagreements and high-severity concerns.
- Final recommendation is explicit.
- Proposal file was not modified.

## References

- `references/roles-reviewer-panel.md`: defines reviewer roles, default reviewer set, mandatory submission-guard reviewer, and clinical reviewer rule.
- `references/policy-reviewer-independence.md`: defines isolation, forbidden context, and independent report requirements.
- `references/delegation-concurrency-rules.md`: defines one-batch concurrent dispatch for independent panel reviewers.
- `references/policy-panel-aggregation.md`: defines aggregation, dissent preservation, and recommendation labels.
- `references/policy-panel-aggregation-format.md`: defines consolidated must-fix grouping and deduplication format.
- `references/policy-skeptical-review.md`: defines skeptical reviewer responsibilities and output boundaries.
- `references/schema-panel-review-report.md`: defines individual and panel report fields.
- `templates/template-individual-review-report.md`: output template for one reviewer report.
- `templates/template-panel-summary-report.md`: output template for panel summary.
