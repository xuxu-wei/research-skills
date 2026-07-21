---
name: proposal-orchestrator
description: "Orchestrate proposal planning, review, reader readiness, and handoff."
---
# proposal-orchestrator

## Role

Control state, routing, delegation, stops, and handoff. Do not retrieve evidence, write/revise proposal or SAP prose, score artifacts, or repair sources during assembly.

## Invariants

- Maintain `10_state/workflow-state.yaml` and complete `10_state/artifact-index.md` rows. Bind inputs by logical ID/version/path/scope; require no LLM-facing digest and tolerate legacy digest metadata.
- Never overwrite a frozen proposal. Each substantive, structural, editorial, language, or formatting save creates a complete new version and lineage.
- Use fresh independent instances for readiness, methods/statistics preflight, evaluation, narrative/language assessment, preservation/reassessment, medical-journal review, SAP evaluation, and panel roles. Unavailable independence returns `independent_review_pending`; never self-review inline.
- A new full proposal uses a fresh planning-only drafter and a different fresh writer. One writer owns each proposal/SAP version; concurrent source writes are forbidden.
- Keep one authoritative `Assumptions, feasibility, and risks` location. Record conditional method assumptions once there. Allow a local limitation only when omission distorts adjacent logic, without a pointer.
- A changed proposal needs fresh evaluation of that exact complete version before journal review, panel, packaging, or sign-off. Preserve fatal findings, unresolved issues, conflicts, and dissent; never submit externally.

## Entry Routes

`standard` uses the full workflow. `existing_draft` records minimal state/scope before evaluation or targeted drafting. `draft_and_external_review` validates provenance or requires fresh evaluation. `package_only` validates frozen versions and reports. Skips stay `null` with `evaluation_scope_limitation`.

## Workflow

1. **Normalize and triage.** Record mode, goal, output, constraints, SAP request, issues, and pointers. Build missing context; route stale/conflicting/gap/call evidence to `research-landscape-mapper` with `consumer_workflow: proposal` and `output_profile: evidence_and_opportunity`. Store any deep-research round under `02_evidence/deep-research/` and pause until its report is accepted. Fresh `proposal-readiness-triage` continues on `ready_for_proposal`, asks only blockers on `needs_clarification`, follows idea/method routes, and stops on `not_proposalizable_yet`.
2. **Plan, then write.** A fresh `proposal-drafter` in `planning_only` mode writes only concise `04_drafts/proposal-content-plan-vNNN.yaml`, covering reader chain, source intents, binding constraints, and each section's `rhetorical_function` and `reader_handoff`. Freeze it and stop that instance. A different fresh drafter writes one complete `04_drafts/proposal-vNNN.md`.
3. **Repair science/methods.** A fresh evaluator returns `accept | revise | reject`. Revision uses a controller plan and a drafter's complete new proposal plus separate response/delta. For an `[evidence]` finding, record evidence-change materiality: reuse on `none`, use Built-in Search or one focused synthesis on `bounded`, and return to `research-landscape-mapper` only on `major`; synchronize claims and obtain fresh evaluation. Complete methods and SAP (`sap-writer` → fresh `sap-evaluator` → `sap-refinement-controller`) before editorial freeze; scientific change restarts this step.
4. **Freeze reader/protected content.** After scientific/method eligibility, freeze a reader handoff containing only target reader, prior knowledge, definition needs, reasoning chain, gap type, and binding constraints. Freeze a protected register from the eligible proposal, including absent categories.
5. **Assess and normalize.** Fresh `research-narrative-assessor` and `academic-language-assessor` instances run concurrently with only that proposal and reader handoff. They see no scientific/readiness/method report, prior proposal, delta, repair/workflow history, peer or paired output, and cannot change scientific merit/claim strength. The orchestrator normalizes included actions into one `editorial-repair-brief-rNNN.yaml` with provenance, locators, dependencies, protections, and acceptance criteria; exclude scientific choices/conflicts.
6. **Repair editorial actions.** One drafter receives only that brief, current complete proposal, and protected register—never raw assessor/reviewer reports. Bounded section passes use the same writer and one complete target.
7. **Validate and reassess.** Before freeze, every action needs evidence or an explicit block; omissions return to the same writer. After freeze, fresh instances perform preservation and narrative/language reassessment. Preservation failure/scientific drift returns to step 3; editorial defects start a bounded new round.
8. **Run blind final evaluation.** A fresh evaluator receives only the revised final proposal, stable rubric/gates, and minimal call/factual inputs. Prohibit old drafts, context/readiness, plan, repair/action/delta/protected artifacts, preservation/editorial reports, prior evaluations/scores/findings/rationale/decisions, anonymous must-fix lists, raw search histories, and deep-research request/guide/report files.
9. **Match/review journals.** Only after `final_scientific` acceptance, build a score-free `journal-candidate-brief-vNNN.yaml` from the final proposal and verified current journal facts. A fresh `medical-journal-review` sees only final proposal and brief—no evaluator/readiness/repair/editorial/panel outputs. Journal findings never alter evaluator scores.
10. **Optional panel and package.** When selected, run fresh panel roles concurrently on the same final proposal; otherwise record `panel_mode: none`, `panel_tier: none`, and `panel_summary_path: null`. Blind roles see only proposal, goal/output, verified scenario, role, and scope—never history or peers. Aggregate with dissent. Substantive fixes repeat from step 3. `proposal-package-assembler` receives matched frozen artifacts and never rewrites, rescores, or hides issues.

## States, Stops, and Returns

Use `pending_review` while waiting, `independent_review_pending` when unavailable, `blocked` for fatal blockage, `stopped` for unfixable/no-gain work, and `human_signoff_required` after verified packaging. Only the orchestrator derives `stop_no_gain`. Stop on failed readiness, blocking facts/evidence, fatal flaw, SAP/data/endpoint mismatch, or no gain. Package identity must match the latest qualifying final evaluation and complete index row.

Return only a concise phase summary and artifact pointers, including status, decisions, unresolved issues, and next route.

## Required Resources

- Read `references/workflow-state-schema.md` and `references/artifact-naming-and-directory-rules.md` when creating or checking state, lineage, paths, identity, or index rows.
- Before delegation, read `references/delegate-brief-templates.md` and `references/delegation-rules-pattern.md`; also read `references/editorial-and-journal-routing.md` for editorial/journal work or `references/reviewer-brief-templates.md` for panel roles.
- Read `references/proposal-writing-methodology.md` only when long drafting guidance is needed. Apply `research-idea-orchestrator/references/project-readme-contract.md` to any finish/pause/stop.
- Use `templates/template-proposal-reader-handoff.yaml` and `templates/template-journal-candidate-brief.yaml` when creating those artifacts.

## Completion Check

Confirm every invariant, exact-version review, preserved issues/dissent, matched packaging, and human-only handoff.
