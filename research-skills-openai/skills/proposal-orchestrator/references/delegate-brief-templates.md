# Delegate Brief Templates

## Contents

<!-- toc:start -->
- [General Rules](#general-rules)
- [Readiness Triage Brief](#readiness-triage-brief)
- [Proposal Planning Brief](#proposal-planning-brief)
- [Full Proposal Writer Brief](#full-proposal-writer-brief)
- [Proposal Evaluation Brief](#proposal-evaluation-brief)
- [Final Proposal Evaluation Brief](#final-proposal-evaluation-brief)
- [Editorial Assessment and Repair Briefs](#editorial-assessment-and-repair-briefs)
  - [Parallel narrative assessment](#parallel-narrative-assessment)
  - [Parallel academic-language assessment](#parallel-academic-language-assessment)
  - [Editorial writer](#editorial-writer)
  - [Preservation and reassessment](#preservation-and-reassessment)
- [Medical Journal Review Brief](#medical-journal-review-brief)
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
- Use logical artifact identity (`artifact_id`, `version`, `path`) and complete index coverage. Do not require, compute, compare, or persist SHA/digest fields; tolerate legacy digest fields as inert metadata.

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

## Proposal Planning Brief

```text
You are a fresh proposal-drafter instance in planning_only mode.

Write only 04_drafts/proposal-content-plan-vNNN.yaml. Do not draft proposal prose and do not continue as the writer.

Input:
- Context brief: {{context_brief_path}}
- Reader and reasoning fields: {{reader_handoff_fields}}
- Evidence artifacts and limitations: {{evidence_artifacts_or_limitations}}
- User/funder structure: {{required_structure}}
- Source-intent coverage: {{source_intent_coverage}}
- Binding constraints: {{binding_constraints}}
- Target plan logical identity/path/version: {{content_plan_ref}}

Task:
1. Bind every required source intent and constraint.
2. Plan a continuous problem -> current knowledge -> gap -> significance -> design rationale chain.
3. Give every section a rhetorical function and reader handoff.
4. Identify the one authoritative Assumptions, feasibility, and risks section.
5. Write the concise YAML plan using proposal-drafter/templates/template-proposal-content-plan.yaml, return its logical reference, and stop.
```

## Full Proposal Writer Brief

```text
You are a fresh proposal-drafter instance in write_full_proposal mode.

Critical separation rule: planner_instance_id={{planner_instance_id}} and writer_instance_id={{writer_instance_id}} must differ. Read the frozen plan; do not revise or evaluate it.

Input:
- Frozen content plan: {{content_plan_ref}}
- Context brief and reader fields: {{context_and_reader_ref}}
- Evidence and factual artifacts: {{evidence_and_facts}}
- Binding target/call requirements: {{binding_constraints}}
- Target complete proposal logical identity/path/version: {{target_proposal_ref}}

Write one complete proposal. Keep assumptions, feasibility, risks, and conditional method assumptions in one authoritative location. Keep unresolved workflow items outside reader-facing prose. Return the draft handoff without a verdict or digest.
```

## Proposal Evaluation Brief

```text
You are an isolated proposal-evaluator subagent.

Critical independence rule: you did not draft this proposal. Evaluate only.
Do not revise or rewrite the proposal.

Input:
- evaluation_stage: {{evaluation_stage}}
- proposal_file_path: {{proposal_file_path}}
- proposal_version: {{proposal_version}}
- proposal_artifact_id: {{proposal_artifact_id}}
- Stable rubric and gates: {{stable_rubric_and_gates}}
- Minimal call requirements or factual inputs only: {{minimal_call_or_factual_inputs}}
- Anonymized must-fix issue list for non-final scientific reassessment only: {{anonymized_must_fix_list_or_none}}
- Forbidden: old proposal, context/readiness report, repair brief, revision delta, preservation/editorial report, prior evaluation, score, finding, rationale, or decision
- Prior scores, overall rationale, and decision visible: false
- Readiness report visible: false
- Repair artifacts visible: false
- Prior evaluation visible: false

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

## Final Proposal Evaluation Brief

```text
You are a fresh proposal-evaluator instance conducting final_scientific evaluation.

Allowed inputs only:
- Revised final complete proposal: {{final_proposal_ref}}
- Stable rubric and gates: {{stable_rubric_and_gates}}
- Minimal call requirements or factual inputs: {{minimal_call_or_factual_inputs}}

Forbidden: old drafts, context brief, readiness report, content plan, repair brief, action-execution report, protected register, revision delta, preservation report, narrative/language reports, anonymous must-fix list, prior evaluation, scores, findings, rationale, or decision.

Evaluate de novo. Check significance, the gap-to-rationale chain, progressive disclosure, section function, terminology burden, scientific alignment, feasibility, impact, relevance, and completion. Prose polish may affect Clarity only and cannot raise Novelty, Feasibility, or Impact without substantive support in the current proposal. Return accept | revise | reject using the proposal-evaluator report template. Do not compute or record a digest.
```

## Editorial Assessment and Repair Briefs

### Parallel narrative assessment

```text
You are a fresh research-narrative-assessor instance.
Read only the frozen current proposal and frozen proposal reader handoff. Do not read scientific evaluator/readiness/method reports, prior proposals, deltas, workflow state, repair history, language output, or hidden expected conclusions. Assess reader chain, progressive disclosure, section function/handoffs, definition order, repetition, and backtracking. Do not judge or change novelty, feasibility, impact, methods, evidence strength, or claim strength. Write only the narrative assessment and executable action output.
```

### Parallel academic-language assessment

```text
You are a fresh academic-language-assessor instance.
Read only the same frozen current proposal and frozen proposal reader handoff. Do not read scientific evaluator/readiness/method reports, prior proposals, deltas, workflow state, repair history, narrative output, or hidden expected conclusions. Assess academic language and terminology at locatable points without judging scientific merit. Write only the language report and actions. Do not compute or record a digest.
```

### Editorial writer

```text
You are one proposal-drafter instance in editorial_repair mode.
Allowed files only: {{editorial_repair_brief_path}}, {{current_complete_proposal_path}}, {{protected_content_register_path}}.
Forbidden: raw narrative/language reports, scientific evaluator/readiness/method reports, old proposals, deltas, scores, findings, or hidden rationale.

Execute every included action against one complete target proposal. You may make bounded sequential section passes, but remain the same writer and do not emit competing partial targets. Preserve every registered scientific meaning and claim strength. Return the complete target plus editorial-action-execution-rNNN.yaml; do not evaluate your work.
```

### Preservation and reassessment

```text
Use a fresh research-narrative-assessor preservation instance to compare the source proposal, repaired proposal, protected-content register, and action execution record. This checks preservation only. Then run different fresh narrative and academic-language reassessment instances against only the repaired proposal and reader handoff; they must not see the source proposal, raw prior reports, repair brief, action record, delta, or one another's output.
```

## Medical Journal Review Brief

```text
You are a fresh medical-journal-review instance.

Allowed inputs only:
- Final proposal logical reference: {{final_proposal_ref}}
- Score-free concrete journal candidate brief: {{journal_candidate_brief_ref}}

Forbidden: proposal evaluator scores/findings/decision, readiness report, scientific or editorial repair history, narrative/language reports, panel reports, hidden expected conclusions, and unsupported journal facts.

Review the final proposal's journal fit and medical research defensibility under the medical-journal-review contract. Preserve uncertainty and source dates. Write only the fresh review report. Do not change proposal evaluator scores or proposal text.
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
