---
name: proposal-readiness-triage
description: "Independently triage proposal-drafting readiness, identify blockers, and route clarification, refinement, or preflight."
---
# proposal-readiness-triage

## Independent Execution Contract

- Run this skill only in a fresh independent subagent or delegated thread. Never run it in the context that generated, drafted, or revised the artifact being assessed.
- Require frozen input artifact IDs, file paths, and versions before assessment. Treat all source artifacts as read-only.
- Write only a readiness review report. Do not draft, rewrite, polish, fix, or otherwise modify any assessed source.
- Do not use the parent task's hidden reasoning, expected answer, or any other evaluator/reviewer output.
- Report the exact files read and the assessment scope in the review report.
- If a fresh independent execution context cannot be created, return `independent_review_pending` with a self-contained continuation brief and stop. Never fall back to inline review, and never emit a passing or ready decision.

### Required Review Report Provenance

Every report must contain: `review_id`, `reviewer_skill`, `reviewer_instance_id`, `workflow_id`, `round_id`, `input_artifact_ids`, `input_versions`, `files_read`, `isolation_mode: fresh_subagent`, `prior_scores_visible: false`, `source_edits_performed: false`, `decision`, `findings`, and `unresolved_issues`.

## When to Use

Use this skill after `proposal-context-brief-builder` has created a proposal context brief and before any full proposal drafting begins.

This skill determines whether the idea is ready for proposal drafting, needs clarification, should return to idea refinement, requires methodology preflight, or is not proposalizable yet.

## Core Principles

- This is an evaluator gate, not a drafting skill.
- Do not write proposal text, aims, background, methods, or SAP.
- Do not invent missing data, endpoints, methods, populations, or constraints.
- Base the decision only on the user input, context brief, available evidence summary, and stated constraints.
- If critical information is missing, identify the minimum missing information instead of guessing.
- If the idea is too immature, route it back to research-idea workflow rather than polishing it into a proposal.
- Evaluation / gate decisions should be made by an isolated independent subagent when called from an orchestrator.

## Inputs

Expected inputs:

- user original idea or promoted idea package;
- proposal context brief;
- intended output, if known;
- user goal and constraints;
- available data or evidence summary, if any;
- SAP requested status, if known.

If the context brief is absent, request `proposal-context-brief-builder` first unless the user explicitly provided an equivalent structured brief.

## Procedure

### 1. Confirm Scope

Check that the task is to assess readiness for proposal drafting. If the user asks for drafting, evaluation, SAP writing, or review, return a routing note to the orchestrator instead of performing those tasks.

### 2. Check Minimum Proposal-Readiness Criteria

Assess whether the idea has enough information for proposal drafting:

- research domain or problem area;
- answerable research question or objective;
- target population, system, dataset, material, or study object;
- core hypothesis, aim, or value claim;
- intended output or use case;
- available or obtainable data, experiment, corpus, system, or evidence path;
- endpoint, outcome, metric, deliverable, or evaluation target;
- plausible method or study design;
- major user constraints;
- known data-access, resource, method, collaboration, or feasibility blockers.

Use `references/criteria-readiness-triage.md` for the detailed criteria.

### 3. Identify Blocking Gaps

Classify missing information as:

- blocking: prevents responsible proposal drafting;
- important but non-blocking: can be handled during drafting;
- optional: useful but not needed for the next step.

Do not ask many questions. If clarification is needed, return the smallest set of questions that would unblock the next step.

### 4. Screen for Fatal Flaws

Check whether the idea has an unrecoverable flaw that prevents proposal drafting, such as an unanswerable question, impossible data requirement, undefined primary target, user-goal mismatch, or method-object mismatch.

Use `references/criteria-fatal-flaws.md` for the fatal flaw categories.

### 5. Decide Route

Return exactly one primary decision:

- `ready_for_proposal`
- `needs_clarification`
- `needs_idea_refinement`
- `needs_methodology_preflight`
- `not_proposalizable_yet`

Use `needs_methodology_preflight` only when a methods, endpoint, data-method fit, or SAP-related uncertainty must be examined before drafting or before an explicitly requested SAP branch.

### 6. Prepare Handoff

Return a concise readiness report for `proposal-orchestrator`.

The report should include:

- decision;
- rationale;
- pass / concern status for each readiness area;
- blocking gaps;
- fatal flaws, if any;
- minimal clarification questions, if needed;
- recommended next skill;
- notes for downstream drafting or preflight.

Use `templates/template-readiness-report.md` for output formatting and `references/schema-readiness-report.md` for field requirements.

## Decision Rules

Return `ready_for_proposal` only if the idea is sufficiently specified for proposal drafting without inventing key facts.

Return `needs_clarification` when a small number of user answers would make the idea draftable.

Return `needs_idea_refinement` when the idea is too vague, too broad, or still requires idea generation, narrowing, comparison, or restructuring.

Return `needs_methodology_preflight` when the main uncertainty is methodological and should be checked by `methodology-statistics-preflight`.

If the main blocker is missing, stale, conflicting, or unverified evidence rather than methods readiness, recommend returning to `research-opportunity-mapper` before drafting.

Return `not_proposalizable_yet` when there is a fatal flaw or the current input cannot responsibly support proposal drafting.

## Delegation Rules

本 skill 本身应由 `proposal-orchestrator` 显式派发到 fresh、隔离的子 agent 或 delegated thread。

子 agent 必须接收完整任务上下文（user original idea、context brief、
evidence artifacts/limitations、user goal、constraints、target output）——
不得依赖父会话隐含上下文。

执行期间不得再调用 drafter、sap-writer、review panel 或其他 evaluator 共同判断。

若发现需要修订或澄清，应返回 readiness report，由 orchestrator 决定路由。

## Pitfalls

- Do not write a proposal.
- Do not improve the idea to make it pass.
- Do not confuse a clear topic with an answerable research question.
- Do not treat missing endpoint, data, or study object as minor if they determine feasibility.
- Do not default to SAP-related routing unless SAP is requested or methodology uncertainty blocks the proposal.
- Do not ask broad exploratory questions when one or two targeted questions would suffice.
- Do not mark an idea ready just because it sounds important.

## Verification

Before returning, check:

- Is there exactly one primary decision?
- Are blocking gaps separated from non-blocking gaps?
- Is the recommended next skill explicit?
- Did the report avoid drafting proposal content?
- Did the report avoid inventing missing facts?
- If the decision is `ready_for_proposal`, can `proposal-drafter` begin without fabricating core details?

## References

- `references/criteria-readiness-triage.md`: detailed readiness criteria and pass / concern / fail guidance.
- `references/criteria-fatal-flaws.md`: fatal flaw categories that can block proposal drafting.
- Read `references/policy-idea-to-proposal-boundary.md` when its named guidance or contract applies: boundary between idea refinement and proposal drafting.
- `references/schema-readiness-report.md`: required fields for the readiness report.
- `templates/template-readiness-report.md`: concise output format for the readiness report.
