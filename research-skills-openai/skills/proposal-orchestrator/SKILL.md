---
name: proposal-orchestrator
description: "Orchestrate proposal planning, review, reader readiness, and handoff."
---
# proposal-orchestrator

## Role

Control state, routing, stops, and handoff. Do not retrieve, draft/revise proposal or SAP prose, score, or repair sources.

## Invariants

- Maintain `10_state/workflow-state.yaml` and complete `10_state/artifact-index.md` rows. Bind inputs by logical ID/version/path/scope; require no LLM-facing digest and tolerate legacy digest metadata.
- Never overwrite a frozen proposal. Each substantive, structural, editorial, language, or formatting save creates a complete new version and lineage.
- Use fresh independent instances for readiness, methods/statistics preflight, evaluation, narrative/language assessment, preservation/reassessment, medical-journal review, SAP evaluation, and panel roles. Unavailable independence returns `independent_review_pending`; never self-review inline.
- A new full proposal uses distinct candidate-planner, formal-planner, and writer instances; only a user-explicit path or fully binding structure may bypass candidates. Record that authority in `proposal-content-plan.v2`. One writer owns each version; concurrent writes are forbidden.
- Keep one authoritative `Assumptions, feasibility, and risks` location. Record conditional method assumptions once there. Allow a local limitation only when omission distorts adjacent logic, without a pointer.
- A changed proposal needs fresh evaluation of that exact complete version before journal review, panel, packaging, or sign-off. Preserve fatal findings, unresolved issues, conflicts, and dissent; never submit externally.

## Entry Routes

`standard` is full. `existing_draft` records state/scope; `draft_and_external_review` validates provenance or reevaluates; `package_only` validates frozen artifacts. Record skips as `null` with `evaluation_scope_limitation`.

## Workflow

1. **Normalize and triage.** Record mode, goal, output, constraints, SAP request, issues, and pointers. Build missing context; route stale/conflicting/gap/call evidence to `research-landscape-mapper` with `consumer_workflow: proposal` and `output_profile: evidence_and_opportunity`. Pause on a deep-research round until its report is accepted. Fresh readiness triage continues when ready, asks only blockers, follows idea/method routes, and stops when not proposalizable.
2. **Select a background path, then plan and write.** Apply `references/proposal-background-path-workflow.md`. Default to two or three neutral supported options with `recommendation: null` and `ranking: null`, then pause for the user's choice. If only one path is defensible, pause for acceptance or another organizing constraint; acceptance creates a frozen `sole_path_acceptance` selection artifact with no options reference. User-explicit or binding paths bypass options; rejection of all or a hybrid starts another candidate round. A new planner writes v2; a third instance writes `04_drafts/proposal-vNNN.md`. Their IDs are pairwise distinct.
3. **Repair science/methods.** A fresh evaluator returns `accept | revise | reject`; revision creates a complete proposal plus response/delta. For `[evidence]`, reuse on `none`, use search or focused synthesis on `bounded`, and remap only on `major`; then re-evaluate. Complete methods and SAP (`sap-writer` → fresh evaluator → `sap-refinement-controller`) before editorial freeze.
4. **Freeze reader/protected content.** After scientific/method eligibility, freeze a reader handoff containing only target reader, prior knowledge, definition needs, reasoning chain, gap type, and binding constraints. Freeze a protected register from the eligible proposal, including absent categories.
5. **Assess and normalize.** Fresh `research-narrative-assessor` and `academic-language-assessor` instances run concurrently on only the proposal and reader handoff, without scientific/history/peer outputs or authority over scientific merit. Normalize included actions into one repair brief with provenance, locators, protections, and acceptance criteria; exclude scientific choices/conflicts.
6. **Repair editorial actions.** One drafter receives only that brief, current complete proposal, and protected register—never raw assessor/reviewer reports. Bounded section passes use the same writer and one complete target.
7. **Validate and reassess.** Before freeze, every action needs evidence or an explicit block; omissions return to the same writer. After freeze, fresh instances perform preservation and narrative/language reassessment. Preservation failure/scientific drift returns to step 3; editorial defects start a bounded new round.
8. **Run blind final evaluation.** A fresh evaluator sees only the final proposal, rubric/gates, and minimal call/facts—never old drafts, context/readiness, path options/selection, plan, repair/delta/editorial artifacts, prior review material, search history, or deep-research files.
9. **Match/review journals.** Only after `final_scientific` acceptance, build a score-free `journal-candidate-brief-vNNN.yaml` from the final proposal and verified current journal facts. A fresh `medical-journal-review` sees only final proposal and brief—no evaluator/readiness/repair/editorial/panel outputs. Journal findings never alter evaluator scores.
10. **Optional panel and package.** Run selected fresh panel roles on the same final proposal; otherwise record `panel_mode: none`, `panel_tier: none`, and `panel_summary_path: null`. Blind roles see no history or peers. Preserve dissent; substantive fixes repeat step 3. The assembler only packages matched frozen artifacts.

## States, Stops, and Returns

Use `human_background_path_selection_required` while waiting for the user's path choice, `pending_review` while waiting for review, `independent_review_pending` when unavailable, `blocked` for fatal blockage, `stopped` for unfixable/no-gain work, and `human_signoff_required` after verified packaging. Only the orchestrator derives `stop_no_gain`. Stop on failed readiness, one-path clarification, user path selection, blocking facts/evidence, fatal flaw, SAP/data/endpoint mismatch, or no gain. Package identity must match the latest qualifying final evaluation and complete index row.

Return only a concise phase summary and artifact pointers, including status, decisions, unresolved issues, and next route. Translate internal workflow status values into natural language in every user-facing summary; do not display machine state identifiers.

## Required Resources

- Read `references/workflow-state-schema.md` and `references/artifact-naming-and-directory-rules.md` when creating or checking state, lineage, paths, identity, or index rows.
- For candidate selection and resume, read `references/proposal-background-path-workflow.md`; before dispatch, also read `references/delegate-background-path-options-brief.md`. Before other delegation, read `references/delegate-brief-templates.md` and `references/delegation-rules-pattern.md`; also read `references/editorial-and-journal-routing.md` for editorial/journal work or `references/reviewer-brief-templates.md` for panel roles.
- Read `references/proposal-writing-methodology.md` only when long drafting guidance is needed. Apply `research-idea-orchestrator/references/project-readme-contract.md` to any finish/pause/stop.
- Use `templates/template-proposal-background-path-selection.yaml`, `templates/template-proposal-reader-handoff.yaml`, and `templates/template-journal-candidate-brief.yaml` when creating those artifacts.

## Completion Check

Confirm every invariant, exact-version review, preserved issues/dissent, matched packaging, and human-only handoff.
