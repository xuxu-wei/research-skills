---
name: idea-adversarial-review-panel
description: "Independently challenge a frozen promoted idea in one assigned novelty, feasibility, or strategy role before proposal handoff."
---
# Idea Adversarial Review Panel

## Overview

`idea-adversarial-review-panel` is a pre-handoff review layer for ideas that may move from `research-idea` into `research-proposal`.

It answers one question: what would make this idea fail when a PI, funder, reviewer, or proposal workflow tries to turn it into an executable proposal?

This skill does not generate ideas, assign six-dimension scores, revise ideas, draft proposal text, or override `idea-evaluator` decisions.

## Independent Execution Contract

- Run each reviewer role only in its own fresh, independent subagent or delegated thread. Never run a role in the context that generated, drafted, or revised the artifact under review.
- Accept only frozen input artifacts identified by artifact ID, exact file path, and version. Treat every source artifact as read-only.
- Write only individual review or verification artifacts. Do not draft, rewrite, polish, fix, merge, reframe, or otherwise modify the reviewed idea or any source file.
- Do not use hidden reasoning from the parent task, an expected answer or decision, prior evaluator output, or output from any other reviewer.
- Report the exact files read and the assigned review scope in every individual output.
- If fresh independent subagents/delegated threads cannot be created, return `independent_review_pending` with a self-contained continuation brief and stop. Never use soft isolation or inline self-review.

Every individual reviewer report must include:

```yaml
review_id:
reviewer_skill: idea-adversarial-review-panel
reviewer_instance_id:
reviewer_role:
workflow_id:
round_id:
input_artifact_ids:
input_versions:
files_read:
review_scope:
isolation_mode: fresh_subagent
prior_scores_visible: false
source_edits_performed: false
decision:
findings:
unresolved_issues:
```

## When to Use

Use this skill when:

- `research-idea-orchestrator` is considering `proposal_handoff_status: ready` or `conditional`;
- an idea has passed independent `idea-evaluator` review but still carries material evidence, feasibility, strategy, or positioning risk;
- the user asks for a skeptical pre-proposal attack on promoted ideas.

Do not use this skill when:

- an idea lacks independent evaluation;
- the task is ordinary idea generation or scoring;
- the user asks for full proposal peer review.

## Core Rules

1. **Handoff gate only.** This panel reviews proposal handoff readiness, not overall idea quality.
2. **No re-scoring.** Do not change `idea-evaluator` scores or hard gates.
3. **No rewriting.** Do not revise, merge, reframe, or draft proposal sections.
4. **Reviewer isolation.** Each reviewer role must run in a distinct fresh independent subagent/delegated thread; this is mandatory, not a best-effort option.
5. **Blocking objections are routes, not edits.** Return a routing recommendation to the orchestrator.
6. **Evidence discipline.** Do not invent missing evidence; send evidence gaps back to `research-opportunity-mapper`.

## Reviewer Roles

Default roles are defined in `references/reviewer-role-definitions.md`:

- novelty/gap skeptic;
- feasibility/method skeptic;
- PI strategy reviewer.

## Inputs

- Research Context Brief;
- Evidence Map / Opportunity Map;
- Evidence Limitations;
- Methodology-Statistics Preflight Report, if available;
- workflow-state confirmation that independent idea evaluation completed, without evaluator scores, findings, or decision;
- promoted or conditionally promoted idea package;
- proposal handoff check;
- user constraints and intended proposal output.

## Workflow

### Phase 1 - Input and Independence Check

Confirm that each idea has an independent `idea-evaluator` report and that reviewer roles did not generate or revise the idea.

### Phase 2 - Prepare Reviewer Briefs

The orchestrator prepares one frozen, role-specific brief per reviewer. Each reviewer receives only the files needed for its role and the explicit task boundary: attack handoff readiness, do not rewrite, do not draft, do not score.

### Phase 3 - Run Adversarial Reviews

The orchestrator explicitly dispatches the three reviewer roles in parallel, one fresh subagent/delegated thread per role. Wait for every required role to finish before synthesis. If any required role cannot be delegated, return `independent_review_pending` and stop.

### Phase 4 - Aggregate Objections

Only the orchestrator may aggregate after all individual reviewer outputs have returned. Preserve every conflicting or minority finding; do not fabricate consensus.

Group findings as:

- `blocking`: must return upstream before proposal handoff;
- `major`: may hand off only as `conditional` with explicit issue owner;
- `minor`: record in portfolio and proposal handoff notes;
- `not_blocking`: concern acknowledged but does not affect handoff.

### Phase 5 - Handoff Decision

Return exactly one panel recommendation:

- `handoff_ready`;
- `conditional_handoff`;
- `return_to_evidence_mapping`;
- `return_to_methodology_preflight`;
- `return_to_generation_or_reframe`;
- `return_to_independent_evaluation`;
- `do_not_handoff`.

## Deliverables

1. **Individual Adversarial Review Reports**: one isolated artifact per reviewer role.
2. **Idea Adversarial Review Report**: orchestrator-produced synthesis of role findings, blocking objections, unresolved risks, dissent, and recommendation.
3. **Handoff Risk Register**: concise list of risks to carry into `proposal-orchestrator`.
4. **Routing Recommendation**: next skill and reason.

## Delegation Rules

This skill should be invoked by `research-idea-orchestrator` before marking an idea ready for `proposal-orchestrator`.

Reviewer subagents must receive complete task context as frozen, named artifacts and must not rely on hidden parent task context, evaluator output, or another reviewer's output.

Reviewer subagents must not call `multi-path-idea-generator`, `idea-evaluator`, `proposal-drafter`, or `proposal-orchestrator`.

If a reviewer finds a problem that requires revision or proposal work, it must return a route recommendation rather than performing the work.

## Stop Conditions

- Missing independent idea evaluation report.
- Missing promoted idea package.
- Missing Evidence Map / Opportunity Map when novelty or gap claims are central.
- Any required reviewer cannot run in a fresh independent subagent/delegated thread. Return `independent_review_pending`; do not issue a handoff recommendation.

## Verification

- Every reviewed idea has an independent evaluation report.
- All three reviewer roles ran in distinct fresh subagents and returned individual reports before synthesis.
- Reviewer instance IDs are pairwise distinct and dissent remains visible.
- Blocking objections have an owner and upstream route.
- No idea scores were changed.
- No proposal text was drafted.

## References

- Read `references/reviewer-role-definitions.md` when its named guidance or contract applies: defines the three default adversarial reviewer roles.
- `research-idea-orchestrator/references/artifact-contracts.md`: shared artifact fields and status values.
- `research-idea-orchestrator/references/handoff-validation.md`: handoff validation rules.
