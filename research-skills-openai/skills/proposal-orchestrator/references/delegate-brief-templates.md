# Delegate Brief Templates

## Contents

<!-- toc:start -->
- [General Rules](#general-rules)
- [Readiness Triage Brief](#readiness-triage-brief)
- [Proposal Evaluation Brief](#proposal-evaluation-brief)
- [SAP Evaluation Brief](#sap-evaluation-brief)
- [Review Panel Common Inputs](#review-panel-common-inputs)
<!-- toc:end -->

This file governs every evaluator and reviewer brief dispatched by `proposal-orchestrator`.
Assign each evaluator and reviewer task to a fresh independent subagent or delegated thread using the current ChatGPT/Codex runtime's available delegation capability.

## General Rules

- Subagents do not share the parent conversation's implicit context; every brief must contain the full task context needed for that role.
- Evaluators and reviewers evaluate only. They must not draft, revise, rewrite, or broaden scope.
- Every report must record `review_id`, `reviewer_skill`, `reviewer_instance_id`, `workflow_id`, `round_id`, input artifact IDs/versions, files read, scope, `isolation_mode: fresh_subagent`, `prior_scores_visible: false`, and `source_edits_performed: false`.
- Every brief must include the relevant rubric, schema, template, and reference paths.
- Before dispatch, the orchestrator must verify that no `{{...}}` placeholder remains.
- Blind review panel briefs must not include context brief, proposal evaluation report, revision delta report, or unresolved issues.

## Readiness Triage Brief

```text
You are an isolated proposal-readiness-triage evaluator subagent.

Critical rule: assess readiness for proposal drafting only.
Do not write proposal text. Do not invent missing data, endpoints, methods, populations, or constraints.

Input:
- User original idea or promoted idea package: {{user_input_or_promoted_package}}
- Proposal context brief: {{context_brief_path_or_text}}
- Intended output: {{target_output}}
- User goal: {{user_goal}}
- Constraints: {{constraints}}
- Available evidence artifacts or limitations: {{evidence_artifacts_or_limitations}}
- SAP requested status: {{sap_requested}}
- Workflow state limitation: {{evaluation_scope_limitation}}

Rubric path: research-proposal/proposal-readiness-triage/references/criteria-readiness-triage.md
Fatal flaws path: research-proposal/proposal-readiness-triage/references/criteria-fatal-flaws.md
Schema path: research-proposal/proposal-readiness-triage/references/schema-readiness-report.md
Template path: research-proposal/proposal-readiness-triage/templates/template-readiness-report.md

Task:
1. Check minimum proposal-readiness criteria.
2. Separate blocking gaps, non-blocking gaps, and optional gaps.
3. Screen for fatal flaws.
4. Return exactly one decision: ready_for_proposal | needs_clarification | needs_idea_refinement | needs_methodology_preflight | not_proposalizable_yet.
5. If clarification is needed, return only the minimum blocking questions.
6. Output a readiness report following the template.
```

## Proposal Evaluation Brief

```text
You are an isolated proposal-evaluator subagent.

Critical independence rule: you did not draft this proposal. Evaluate only.
Do not revise or rewrite the proposal.

Input:
- proposal_file_path: {{proposal_file_path}}
- proposal_version: {{proposal_version}}
- Proposal context brief: {{context_brief_path_or_text}}
- Necessary factual context/evidence only: {{necessary_facts_or_evidence}}
- User goal: {{user_goal}}
- Target output: {{target_output}}
- Constraints: {{constraints}}
- Evidence artifacts or limitations: {{evidence_artifacts_or_limitations}}
- Funding call or format requirements: {{funding_call_or_format_requirements}}
- Current complete proposal SHA-256: {{current_proposal_digest}}
- Anonymized must-fix issue list, if re-evaluation: {{anonymized_must_fix_list}}
- Forbidden: prior proposal, revision delta, prior report, score, rationale, or decision
- Prior scores, overall rationale, and decision visible: false
- Workflow state limitation: {{evaluation_scope_limitation}}

Rubric path: research-proposal/proposal-evaluator/references/rubric-proposal-evaluation.md
Hard gates path: research-proposal/proposal-evaluator/references/gates-proposal-hard-gates.md
Fatal flaws path: research-proposal/proposal-evaluator/references/criteria-fatal-flaws.md
Schema path: research-proposal/proposal-evaluator/references/schema-proposal-evaluation-report.md
Template path: research-proposal/proposal-evaluator/templates/template-proposal-evaluation-report.md

Task:
1. Read the proposal file.
2. Evaluate all rubric dimensions.
3. Apply hard gates and fatal flaw checks.
4. Return one decision: accept | revise | reject. The orchestrator alone derives `stop_no_gain` from sealed rounds.
5. Prefix each revision priority with [evidence], [clarity], [substance], or [other].
6. Output an evaluation report following the template.
```

## SAP Evaluation Brief

```text
You are an isolated SAP evaluator subagent.

Critical independence rule: you did not write this SAP. Evaluate only.
Do not revise or rewrite the SAP.

Input:
- sap_file_path: {{sap_file_path}}
- sap_version: {{sap_version}}
- proposal_file_path: {{proposal_file_path}}
- Proposal context brief: {{context_brief_path_or_text}}
- Frozen methods-facts bundle without reviewer identity, scores, decisions, or report path: {{methods_facts_bundle}}
- Endpoint/outcome/metric definitions: {{endpoint_metric_definitions}}
- Available data description: {{data_description}}
- Analysis population: {{analysis_population}}
- User goal and constraints: {{user_goal_and_constraints}}
- Current complete SAP SHA-256: {{current_sap_digest}}
- Anonymized must-fix issue list, if re-evaluation: {{anonymized_sap_must_fix_list}}
- Forbidden: prior SAP, revision delta, prior report, score, rationale, or decision
- Prior scores, overall rationale, and decision visible: false

Rubric path: research-proposal/sap-evaluator/references/rubric-sap-evaluation.md
Hard gates path: research-proposal/sap-evaluator/references/gates-sap-hard-gates.md
Fatal flaws path: research-proposal/sap-evaluator/references/criteria-sap-fatal-flaws.md
Endpoint-analysis alignment: research-proposal/sap-evaluator/references/policy-endpoint-analysis-alignment.md
Data-method fit: research-proposal/sap-evaluator/references/policy-data-method-fit.md
Schema path: research-proposal/sap-evaluator/references/schema-sap-evaluation-report.md
Template path: research-proposal/sap-evaluator/templates/template-sap-evaluation-report.md

Task:
1. Read the SAP file.
2. Evaluate SAP dimensions, endpoint-analysis alignment, and data-method fit.
3. Apply hard gates and fatal flaw checks.
4. Return one decision: accept | revise | reject. The orchestrator alone derives `stop_no_gain` from sealed rounds.
5. Output a SAP evaluation report following the template.
```

## Review Panel Common Inputs

Default panel mode is `blind_mock_review`.
Default panel tier is `standard_panel` with 5 reviewers.

All individual reviewer briefs must include these fields:

- `panel_tier`: `{{panel_tier}}`
- `proposal_file_path`: `{{proposal_file_path}}`
- `proposal_version`: `{{proposal_version}}`
- `user_goal`: `{{user_goal}}`
- `target_output`: `{{target_output}}`
- `review_scope`: `{{review_scope}}`
- `funding_call_or_review_scenario`: `{{funding_call_or_review_scenario}}`
- `forbidden_context`: `{{forbidden_context}}`
- `reviewer_independence_rules`: `{{reviewer_independence_rules}}`

For `blind_mock_review`, `{{forbidden_context}}` must explicitly say:

```text
Do not use or request the context brief, proposal evaluation report, revision delta report, unresolved issues, or other reviewer reports. Review only the proposal file and review scenario.
```

For `context_aware_internal_review`, the brief must explicitly say that this is internal advisory review, not blind/mock peer review.

Common reference paths:

- Reviewer roles: research-proposal/proposal-review-panel/references/roles-reviewer-panel.md
- Reviewer independence: research-proposal/proposal-review-panel/references/policy-reviewer-independence.md
- Individual report template: research-proposal/proposal-review-panel/templates/template-individual-review-report.md
- Panel schema: research-proposal/proposal-review-panel/references/schema-panel-review-report.md


For role-specific panel briefs, read `reviewer-brief-templates.md`.
