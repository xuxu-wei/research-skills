---
name: proposal-drafter
description: "Plan neutral proposal-background paths and content, then use a separate writer for one complete proposal."
---
# proposal-drafter

## Role

Generate proposal-background path options, plan selected proposal content, or write/revise prose in the selected mode. Keep candidate planning, formal planning, and writing in separate fresh instances. Do not choose for the user, decide readiness, review, write an SAP, or certify the output.

## Required Inputs

- Candidate/formal planning requires approved readiness, evidence limits, reader/constraint fields, a target artifact reference, and the route authority appropriate to the mode.
- Writing/revision requires a frozen plan or repair authority, allowed evidence, binding format, source/target identities, and instance IDs. `editorial_repair` receives only its normalized brief, current proposal, and protected register.
- See `references/proposal-drafter-handoffs.md` for the exact mode inputs and return fields.

Stop with an input-gap report when required facts, context, or readiness authority are missing. Never invent data, endpoints, sample size, evidence findings, feasibility, or user resources.

## Invariants

- Every mode requires an explicit target path/version. User/funder structure wins over the bundled template.
- New full proposals default to `background_path_options`, then user selection, a different `planning_only` instance, and a third `write_full_proposal` instance. All IDs differ. Skip candidates only for a user-explicit path or fully binding structure and record `selection_source: user_explicit | binding_constraint`; a user-explicit bypass also preserves the exact authorization text in the v2 plan.
- Offer two or three materially different, evidence-supportable paths without score, rank, recommendation, or weak foil. If only one is defensible, return its normalized functional outline and ask the user to accept it or add an organizing constraint; create no valid options artifact and stop. User acceptance is frozen by the orchestrator as a `sole_path_acceptance` selection artifact before formal planning. A requested hybrid starts a new coherence-checked candidate round.
- Formal planning writes only `proposal-content-plan.v2`. Historical v1 remains readable; replace an unwritten v1 through a fresh v2 planner, but do not migrate an existing draft merely for targeted revision.
- Bind source intents, constraints, section functions, and reader handoffs; keep question, aims, work, methods, outputs, and innovation traceable. Distinguish facts, claims, assumptions, and unknowns; never inflate certainty, novelty, or feasibility.
- Every `04_drafts/proposal-vNNN.md` is complete and independently readable. Never overwrite a prior proposal or register a plan, response, delta, or changed section as the current proposal.
- Keep reviewer-response language out of proposal prose.
- Keep one authoritative `Assumptions, feasibility, and risks` location. Elsewhere state only a boundary needed to avoid distorting adjacent logic, without a pointer.
- Editorial repair cannot alter scientific meaning/strength. One writer owns one complete target and reads no raw reviews, old proposals, deltas, scores, findings, or hidden rationale.

## Procedure

1. **Select mode.** Use `background_path_options`, `planning_only`, `write_full_proposal`, `scientific_revision`, `editorial_repair`, or `formatting_only`.
2. **Generate candidate paths.** Apply the background reference and options template; return two or three neutral paths, or the one-path clarification, then stop.
3. **Plan selected prose.** Verify frozen option-selection, sole-path-acceptance, or bypass authority; write the complete `proposal-content-plan.v2` background and section contract, then stop.
4. **Separate instances.** In `write_full_proposal`, require a frozen v2 plan and a writer ID different from both planning IDs; stop on missing, legacy-unmigrated, or self-authored planning authority.
5. **Establish state.** Record source identity, new path/version, sources, assumptions, scope, and unresolved items outside proposal prose.
6. **Select structure.** Use the user/funder structure, else `templates/template-proposal.md`. When binding content is unavailable, retain its heading only if required and record the gap outside the prose; do not fabricate.
7. **Draft the argument.** Realize the planned problem -> knowledge -> gap -> significance -> rationale chain and selected systematic/progressive function; another language or binding template need not use fixed labels.
8. **Discipline evidence.** Ground claims and boundaries; do not substitute a literature list for gap logic. Match superlatives to evidence and do not invent application urgency for theory-led work.
9. **Revise science narrowly.** In `scientific_revision`, apply the controller's `add | replace | condense | delete | clarify` operation and `enter_proposal | response_only | no_action` destination for every finding.
10. **Repair editorial actions in isolation.** Execute every included brief action with the same writer against one complete target; record action-level execution evidence or an explicit block while preserving protected content. Do not independently include, exclude, or resolve conflicts.
11. **Write artifacts.** Save a clean new proposal; keep response/delta and editorial execution artifacts separate.
12. **Handoff.** Return current identity/path/version, lineage, plan/change pointers, unresolved items, and specified route; never a quality verdict.

## Output Contract

Use `references/proposal-drafter-handoffs.md`. Candidate mode returns only an options selection/clarification stop; formal planning returns only a v2 plan handoff; writing/revision returns only the complete-artifact handoff. Return artifact pointers, not drafting logs.

## Conditional Resources

- Read `proposal-orchestrator/references/artifact-naming-and-directory-rules.md` for proposal, revision, state, or index paths.
- Read `references/proposal-drafter-handoffs.md` before returning any mode.
- Read `references/proposal-background-argumentation.md` for every candidate path round, v2 background plan, and new full-proposal background.
- Use `templates/template-proposal-background-path-options.yaml` in `background_path_options`. Read `templates/template-proposal.md` only without a user/funder structure; use `templates/template-proposal-content-plan.yaml` for every new full-proposal plan.
- Read `references/rules-proposal-writing.md` for section scope and prohibited inventions.
- Read `references/rules-literature-integration.md` when integrating evidence into gap and rationale prose.
- Read `references/rules-claims-discipline.md` for novelty, feasibility, impact, or method claims.
- Read `references/policy-file-maintenance.md` for versions, lineage, and change summaries.
- Read `references/proposal-genre-awareness.md` when prose risks becoming tutorial, narrative, or reviewer response.
- Read `references/proposal-writing-principles.md` for persuasive style after satisfying the core contract.
- For full proposal drafting only, use `references/proposal-writing-methodology.md` to locate the plugin-level long-form method.
- Read `references/anti-pattern-checklist.md` immediately before handoff.

## Completion Check

Confirm the mode's stop/authority, distinct IDs, identity/version, selected-path conformance, complete grounded output, lineage, unresolved items, and no self-evaluation.
