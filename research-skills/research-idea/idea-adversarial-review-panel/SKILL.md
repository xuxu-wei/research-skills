---
name: idea-adversarial-review-panel
description: Use when promoted or conditionally promoted research ideas need a pre-proposal adversarial review before handoff to proposal-orchestrator. Runs isolated reviewer roles that attack novelty/gap validity, feasibility/method fit, and PI-level strategic value without re-scoring, rewriting, or drafting proposals.
version: 1.0.0
author: Xuxu Wei
license: MIT
metadata:
  hermes:
    tags: [research-idea, adversarial-review, handoff, proposal-readiness, review-panel]
    category: research-idea
    related_skills:
      - research-idea-orchestrator
      
      - research-opportunity-mapper
      - methodology-statistics-preflight
      - idea-evaluator
      - idea-portfolio-assembler
      - proposal-orchestrator
---

# Idea Adversarial Review Panel

## Overview

`idea-adversarial-review-panel` is a pre-handoff review layer for ideas that may move from `research-idea` into `research-proposal`.

It answers one question: what would make this idea fail when a PI, funder, reviewer, or proposal workflow tries to turn it into an executable proposal?

This skill does not generate ideas, assign six-dimension scores, revise ideas, draft proposal text, or override `idea-evaluator` decisions.

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
4. **Reviewer isolation.** Each reviewer role must run as an isolated subagent where runtime supports delegation.
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
- independent Idea Evaluation Report;
- promoted or conditionally promoted idea package;
- proposal handoff check;
- user constraints and intended proposal output.

## Workflow

### Phase 1 - Input and Independence Check

Confirm that each idea has an independent `idea-evaluator` report and that reviewer roles did not generate or revise the idea.

### Phase 2 - Prepare Reviewer Briefs

Each reviewer receives only the files needed for its role and the explicit task boundary: attack handoff readiness, do not rewrite, do not draft, do not score.

### Phase 3 - Run Adversarial Reviews

Dispatch the three reviewer roles in parallel when runtime supports delegation. If delegation is unavailable, mark the panel as soft-isolated and lower confidence.

### Phase 4 - Aggregate Objections

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

1. **Idea Adversarial Review Report**: role findings, blocking objections, unresolved risks, and recommendation.
2. **Handoff Risk Register**: concise list of risks to carry into `proposal-orchestrator`.
3. **Routing Recommendation**: next skill and reason.

## Delegation Rules

This skill should be invoked by `research-idea-orchestrator` before marking an idea ready for `proposal-orchestrator`.

Reviewer subagents must receive complete task context and must not rely on hidden parent conversation context.

Reviewer subagents must not call `multi-path-idea-generator`, `idea-evaluator`, `proposal-drafter`, or `proposal-orchestrator`.

If a reviewer finds a problem that requires revision or proposal work, it must return a route recommendation rather than performing the work.

## Stop Conditions

- Missing independent idea evaluation report.
- Missing promoted idea package.
- Missing Evidence Map / Opportunity Map when novelty or gap claims are central.
- Reviewer isolation cannot be established and the user requires hard isolation.

## Verification

- Every reviewed idea has an independent evaluation report.
- All three reviewer roles ran or were explicitly marked unavailable.
- Blocking objections have an owner and upstream route.
- No idea scores were changed.
- No proposal text was drafted.

## References

- `references/reviewer-role-definitions.md`: defines the three default adversarial reviewer roles.
- `research-idea-orchestrator/references/artifact-contracts.md`: shared artifact fields and status values.
- `research-idea-orchestrator/references/handoff-validation.md`: handoff validation rules.

