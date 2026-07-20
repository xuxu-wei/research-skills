---
name: proposal-drafter
description: "Plan proposal section functions, then use a separate writer instance for one complete proposal."
---
# proposal-drafter

## Role

Plan proposal content or write/revise prose in the selected mode. Keep planning and writing in separate fresh instances. Do not decide readiness, review, write an SAP, or certify the output.

## Required Inputs

- `planning_only`: approved context/readiness or fast-track limitation; goal/output; evidence/limits; supplied structure/call; reader, gap, source-intent, constraints, and target plan/proposal references.
- `write_full_proposal`: frozen content plan; context/reader fields; allowed facts/evidence; binding structure/call; target proposal identity; planner/writer instance IDs.
- `scientific_revision`: current/target proposal identities, controller repair plan, allowed facts/evidence, and constraints.
- `editorial_repair`: only the normalized editorial repair brief, current complete proposal, and protected-content register.
- `formatting_only`: current complete proposal, binding format, and target proposal identity.

Stop with an input-gap report when required facts, context, or readiness authority are missing. Never invent data, endpoints, sample size, evidence findings, feasibility, or user resources.

## Invariants

- Writing requires an explicit target `proposal_file_path`/version; planning requires a content-plan path/version and target proposal reference.
- Prefer the user's required structure; otherwise use the bundled template.
- Run `planning_only` first for a new full proposal. It writes only `04_drafts/proposal-content-plan-vNNN.yaml`, then stops. A different fresh instance performs `write_full_proposal`; the planner never becomes the writer.
- In the content plan, bind source intents and constraints, and state every section's rhetorical function and reader handoff.
- Keep question, aims, work packages, methods, outputs, and innovation claims mutually traceable.
- Distinguish facts, supported claims, assumptions, and unresolved items. Quantify success only when supported; never strengthen uncertainty, novelty, or feasibility.
- Every `04_drafts/proposal-vNNN.md` is complete and independently readable. Never overwrite a prior proposal or register a plan, response, delta, or changed section as the current proposal.
- Keep reviewer-response language out of proposal prose.
- Keep one authoritative `Assumptions, feasibility, and risks` location; record each accepted conditional method assumption once there. State a limitation elsewhere only when it advances the immediate reasoning and omission would distort the connected design choice; state it locally without a pointer.
- Keep scientific revision separate from editorial repair. Editorial repair cannot change scientific meaning or claim strength. Its one writer may make bounded sequential section passes but owns one complete target and emits no competing partial drafts. It reads no raw narrative/language reports, evaluator/readiness reports, old proposals, deltas, scores, findings, or hidden rationale.

## Procedure

1. **Select mode.** Use `planning_only`, `write_full_proposal`, `scientific_revision`, `editorial_repair`, or `formatting_only`.
2. **Plan initial prose.** In `planning_only`, bind reader chain, gap type, source intents, constraints, evidence, and required structure. Write `templates/template-proposal-content-plan.yaml` with each section's rhetorical function and reader handoff, then stop.
3. **Separate instances.** In `write_full_proposal`, require a frozen plan and a writer ID different from the planner ID; stop on missing or self-authored planning authority.
4. **Establish state.** Record source identity, new path/version, sources, assumptions, scope, and unresolved items outside proposal prose.
5. **Select structure.** Use the user/funder structure, else `templates/template-proposal.md`. When binding content is unavailable, retain its heading only if required and record the gap outside the prose; do not fabricate.
6. **Draft the argument.** Realize the plan's problem -> current knowledge -> gap -> significance -> rationale chain with reader-calibrated progressive disclosure. Make every section perform its function and reader handoff.
7. **Discipline evidence.** Ground claims, expose decision-relevant boundaries, do not substitute a literature list for gap logic, and define terms before use.
8. **Revise science narrowly.** In `scientific_revision`, apply the controller's `add | replace | condense | delete | clarify` operation and `enter_proposal | response_only | no_action` destination for every finding.
9. **Repair editorial actions in isolation.** Execute every included brief action with the same writer against one complete target; record action-level execution evidence or an explicit block while preserving protected content. Do not independently include, exclude, or resolve conflicts.
10. **Write artifacts.** Save a clean new proposal; keep response/delta and editorial execution artifacts separate.
11. **Handoff.** Return current identity/path/version, lineage, plan/change pointers, unresolved items, and specified route; never a quality verdict.

## Output Contract

Planning mode returns:

```yaml
planning_handoff:
  source_skill: proposal-drafter
  mode: planning_only
  planner_instance_id:
  content_plan_artifact_id:
  content_plan_path: 04_drafts/proposal-content-plan-vNNN.yaml
  content_plan_version:
  based_on: []
  binding_constraints_covered: []
  unresolved_inputs: []
  next_route: write_full_proposal
```

Writing and revision modes return:

```yaml
draft_handoff:
  source_skill: proposal-drafter
  mode: write_full_proposal | scientific_revision | editorial_repair | formatting_only
  writer_instance_id:
  planner_instance_id:
  content_plan_path:
  proposal_artifact_id:
  proposal_file_path:
  proposal_version:
  based_on: []
  change_type: initial | substantive | structural | editorial_only | formatting_only
  response_to_reviewers_path:
  editorial_action_execution_path:
  change_summary: []
  assumptions: []
  unresolved_issues: []
  next_route: scientific_evaluation | editorial_action_validation | re-evaluation | final_evaluation
```

Return only the concise handoff and artifact pointers, not drafting logs.

## Conditional Resources

- Read `proposal-orchestrator/references/artifact-naming-and-directory-rules.md` for proposal, revision, state, or index paths.
- Read `templates/template-proposal.md` only without a user/funder structure; use `templates/template-proposal-content-plan.yaml` for every new full-proposal plan.
- Read `references/rules-proposal-writing.md` for section scope and prohibited inventions.
- Read `references/rules-literature-integration.md` when integrating evidence into gap and rationale prose.
- Read `references/rules-claims-discipline.md` for novelty, feasibility, impact, or method claims.
- Read `references/policy-file-maintenance.md` for versions, lineage, and change summaries.
- Read `references/proposal-genre-awareness.md` when prose risks becoming tutorial, narrative, or reviewer response.
- Read `references/proposal-writing-principles.md` for persuasive style after satisfying the core contract.
- For full proposal drafting only, use `references/proposal-writing-methodology.md` to locate the plugin-level long-form method.
- Read `references/anti-pattern-checklist.md` immediately before handoff.

## Completion Check

For planning, confirm a concise frozen plan, reader/gap/source-intent/constraint coverage, per-section function/handoff, and a separate next writer. For writing, confirm identity/path/version, grounded and aligned claims, progressive disclosure, one authoritative assumptions/feasibility/risks location, user-structure precedence, complete prose, separate repair artifacts, preserved unresolved items, lineage, action conformance when applicable, and no self-evaluation.
