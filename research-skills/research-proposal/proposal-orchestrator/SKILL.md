---
name: proposal-orchestrator
description: Orchestrate research-proposal workflow from an existing idea or draft through context normalization, evidence mapping, readiness triage, proposal drafting, independent evaluation, targeted revision, optional SAP branch, blind or context-aware review panel, and final package assembly.
version: 0.8.0
author: Xuxu Wei
license: MIT
metadata:
  hermes:
    tags: [research-proposal, proposal, orchestration, evaluation, revision, peer-review, SAP]
    related_skills:
      - research-opportunity-mapper
      - proposal-context-brief-builder
      - proposal-readiness-triage
      - proposal-drafter
      - proposal-evaluator
      - proposal-refinement-controller
      - methodology-statistics-preflight
      - sap-writer
      - sap-evaluator
      - sap-refinement-controller
      - proposal-review-panel
      - proposal-package-assembler
      - academic-language-assessor
---

# proposal-orchestrator

## Purpose

Use this skill when the user has an existing research idea, promoted idea package, clinical or practical problem, funding call, data opportunity, proposal draft, proposal evaluation request, optional SAP request, or mock review request.

This skill is the workflow controller. It does not generate raw ideas, retrieve evidence directly, draft proposal text, evaluate its own outputs, revise SAP content, or replace specialist skills.

## Core Rules

- Maintain a workflow state using `references/workflow-state-schema.md`.
- Maintain project directories and artifact names using `references/artifact-naming-and-directory-rules.md`.
- Run `proposal-context-brief-builder` before readiness triage in the standard path.
- Fast-track entry is allowed only when a minimal workflow state is created and skipped artifacts are recorded.
- Use `research-opportunity-mapper` when evidence is missing, stale, conflicting, or required for novelty, gap, guideline, clinical, or funding-call claims.
- Run independent `proposal-readiness-triage` before first full drafting unless fast-track mode explicitly skips it.
- Proposal work is file-centered: track `proposal_file_path`, `proposal_version`, state updates, evaluation reports, revision history, and unresolved issues.
- Do not overwrite proposal versions. Substantive edits create a new `04_drafts/proposal-vNNN.md`; `10_state/workflow-state.yaml` records the current version and `10_state/artifact-index.md` records the human-readable inventory.
- Use `academic-language-assessor` for English, Chinese, or bilingual language quality evaluation before final package assembly and after any language polishing pass.
- Evaluation and review must be isolated: use `delegate_task` for readiness triage, proposal evaluation, SAP evaluation, SAP re-evaluation, and every review-panel reviewer.
- `proposal-drafter` writes or revises; `proposal-evaluator` evaluates; `proposal-refinement-controller` manages revision loops. Do not merge these roles.
- SAP is optional and runs only when explicitly requested or required by the target output. `methodology-statistics-preflight` must precede `sap-writer`.
- `proposal-package-assembler` assembles existing artifacts only. It must not clean, rewrite, patch, re-score, or hide unresolved issues.

## Workflow State

At workflow start, create or update the state fields defined in `references/workflow-state-schema.md`.

Also create the project directory layout and artifact index defined in `references/artifact-naming-and-directory-rules.md`.

Minimum state required for every entry path:

- `entry_mode`
- `user_goal`
- `target_output`
- `context_brief_path` or `context_missing: true`
- `proposal_file_path` and `proposal_version`, if a draft already exists
- `sap_requested`
- `unresolved_issues`

If fast-track mode skips context brief or readiness triage, set the missing artifact path to `null` and add `evaluation_scope_limitation`. Downstream evaluator or reviewer briefs must include that limitation.

## Entry Paths

### Standard Entry

Use when the user starts from an idea, promoted idea package, data opportunity, funding call, or broad proposal request.

Run the full sequence:

`context brief -> evidence gate -> readiness triage -> draft -> independent evaluation -> revision loop if needed -> optional SAP -> review panel if requested/appropriate -> final package`

### Fast-Track Entry

Use when the user provides existing proposal artifacts.

- Existing proposal draft only: create minimal workflow state, ask only for blocking missing user goal or target output, then route to drafting revision or evaluation. Do not silently invent context.
- Proposal plus evaluation report: create state, record skipped context/readiness artifacts, then route to `proposal-refinement-controller` or review panel.
- Proposal plus all evaluator/panel materials: create state, record artifact versions, then route to final package assembly.

Skipped steps are not backfilled unless the user requests them, but the limitation must remain visible in state and final package.

## Steps

### 1. Build Context Brief

Call `proposal-context-brief-builder` to normalize input type, user goal, target output, constraints, evidence status, SAP request status, assumptions, and critical unknowns.

State updates:

- set `context_brief_path`;
- set `context_missing: false`;
- update `target_output`, `sap_requested`, and `unresolved_issues`.

### 2. Evidence Mapping Gate

Call `research-opportunity-mapper` before readiness triage when evidence is absent, outdated, conflicting, clinically or otherwise high-stakes, or needed for novelty/gap/guideline/funding-call claims.

Reuse an existing valid Evidence Map when scope and source limitations match. Do not repeat retrieval for no gain.

State updates:

- set `evidence_map_path`;
- set `evidence_limitations_path`;
- add unresolved evidence gaps.

### 3. Readiness Triage

Use `delegate_task` to assign an isolated `proposal-readiness-triage` subagent.

Use the Readiness Triage Brief in `references/delegate-brief-templates.md`. The brief must say: readiness gate only; do not write proposal; do not replace drafter.

State updates:

- set `readiness_report_path`;
- route according to readiness decision.

### 4. Handle Readiness Decision

- `ready_for_proposal`: continue to drafting.
- `needs_clarification`: ask the minimum blocking questions.
- `needs_idea_refinement`: return to `research-idea-orchestrator`.
- `needs_methodology_preflight`: run `methodology-statistics-preflight` if it blocks drafting or SAP.
- `not_proposalizable_yet`: stop with readiness report and state snapshot.

### 5. Draft Proposal File

Call `proposal-drafter`.

State updates:

- set `proposal_file_path`;
- set `proposal_version`;
- set `proposal_status: drafted`;
- record assumptions and unresolved drafting issues.

### 6. Independent Proposal Evaluation

Use `delegate_task` to assign an isolated `proposal-evaluator` subagent. Do not evaluate inline.

Use the Proposal Evaluation Brief in `references/delegate-brief-templates.md`. The evaluator receives proposal file path, context brief when available, readiness report when available, evidence artifacts, user goal, constraints, version, and any scope limitation.

Decision labels must align with `proposal-evaluator`: `accept`, `revise`, `reject`, or `stop_no_gain`.

State updates:

- set `evaluation_report_path`;
- set `proposal_status: evaluated`;
- copy revision priorities and unresolved issues.

If the evaluator returns `accept` with revision priorities, ask the user whether to enter a polish revision round or proceed. Default: if any priority is tagged `[substance]`, run one targeted revision round before review panel.

### 7. Proposal Revision Loop

When proposal evaluation returns `revise`, call `proposal-refinement-controller`.

Default maximum: 2 rounds. Each round must include:

- targeted revision plan;
- updated proposal plus separate response-to-reviewers file;
- version lineage and delta report;
- isolated independent re-evaluation by `proposal-evaluator`.

State updates:

- increment `revision_round`;
- append `revision_history`;
- update `proposal_file_path`, `proposal_version`, `evaluation_report_path`, `proposal_status`, and unresolved issues.

Language polishing is a traceable revision mode: save `05_evaluations/language-assessment-vNNN.md`, route fixes to `proposal-drafter`, save `06_revisions/round-NNN/language-change-log-rNNN.md`, and create a new proposal version with `change_type: language_only` if a changed draft is saved.

### 8. Optional SAP Branch

Run only when `sap_requested: true` or target output explicitly requires SAP.

Sequence:

1. Run `methodology-statistics-preflight`.
2. If preflight blocks SAP, set `sap_status: preflight_blocked` and stop SAP branch.
3. Call `sap-writer`.
4. Use `delegate_task` for isolated `sap-evaluator`.
5. If `sap-evaluator` returns `revise`, call `sap-refinement-controller`.

State updates:

- set `sap_status`;
- set `sap_file_path`, `sap_version`, `sap_evaluation_report_path`;
- increment `sap_revision_round` through `sap-refinement-controller`;
- preserve unresolved SAP issues.

### 9. Proposal Review Panel

Use after proposal evaluation passes, after revision loop reaches accept, or when the user explicitly requests mock review.

Default panel mode is `blind_mock_review`.

In `blind_mock_review`, individual reviewers receive only:

- `proposal_file_path`;
- `proposal_version`;
- user goal and target output;
- funding call or review scenario, if available;
- reviewer role and scope.

Do not give individual reviewers the context brief, proposal evaluation report, revision delta report, or unresolved issues. Those materials are held by the orchestrator for aggregation context only.

If the user explicitly asks for an internal advisory review that uses background context, set `panel_mode: context_aware_internal_review` and label the output as internal advisory review, not blind/mock peer review.

Use `delegate_task(tasks=[...])` to dispatch all reviewers at once. Default panel tier is `standard_panel` with 5 reviewers. `lightweight_panel` has 3 reviewers and must include a domain expert, methodology/statistics reviewer, and submission-guard reviewer. `full_panel` has 7 reviewers. For medicine, clinical practice, or public health, use `practicing-clinician reviewer` as the domain expert role.

State updates:

- set `panel_summary_path`;
- set `panel_reviewed_proposal_version`;
- set `panel_mode`;
- set `panel_tier`;
- record reviewer dissent and must-fix items.

### 10. Handle Panel Decision

Route based on panel final recommendation:

- `strong_support`: proceed to final package.
- `support_with_minor_revision`: proceed to final package only if the package marks minor revision as pending; otherwise run a narrow polish revision.
- `support_after_major_revision`: default route is Step 7 proposal revision loop. Exception: if the user only wants a current-state handoff package, proceed to final package and mark "major revision required before submission".
- `revise_and_resubmit`: return to Step 7, then run proposal evaluator gate again. Skip a second panel only when the user explicitly chooses panel-only mock iteration.
- `not_ready`: return to Step 5 or Step 4 depending on the defect.
- `reject_or_redesign`: stop current workflow and recommend return to `research-idea-orchestrator`.

Before final package, if SAP was not run but panel explicitly requires SAP, route to Step 8.

### 11. Submission-Clean Proposal

If the final package requires a submission-clean proposal, do not ask `proposal-package-assembler` to patch the proposal.

Route cleanup findings from submission-guard reviewer or archival cleanup checks to `proposal-refinement-controller` and `proposal-drafter`. The drafter must produce a clean proposal version and response/change summary. Then run independent evaluation if substantive text changed.

State updates:

- set `proposal_status: submission_clean` only after the clean version exists.

### 12. Final Package

Call `proposal-package-assembler` with the final workflow state, proposal path/version, readiness/evaluation/revision/panel materials, unresolved issues, and optional SAP materials.

Final package must distinguish:

- ready for human submission review;
- delivered with minor revision pending;
- delivered with major revision required;
- blocked or partial package.

## Handling Evidence-Related Feedback

After evaluation or review, scan all `[evidence]` tagged revision priorities and must-fix items.

Ask whether to:

- call `research-opportunity-mapper`;
- generate an external DeepSearch prompt;
- mark the claim as evidence pending and continue.

If evidence mapping is run, pass the Evidence Map and Evidence Limitations to the next drafting or revision step. Evidence retrieval does not consume an additional proposal revision round by itself, but any text change still belongs to the current revision scope.

## Delegation Minimum

Every isolated subagent brief must include user goal, target output, task boundary, required file paths/versions, relevant artifacts, scope limitations, and explicit prohibited actions.

Evaluation/review briefs must say: evaluate or review only; do not draft, revise, rewrite, or broaden scope.

## Stop Conditions

Stop or route back when readiness fails, blocking user facts are missing, idea refinement is needed, evidence limitations block responsible drafting, evaluator finds unfixable fatal flaws, revision produces no gain, SAP cannot align with endpoint/data/preflight, or workflow state is insufficient to support the requested downstream action.

## Pitfalls

- Do not proceed with implicit state; record skipped artifacts and limitations.
- Do not give blind review panel members context brief or prior evaluation materials.
- Do not route major panel revision directly to final package unless the user asks for a current-state handoff.
- Do not package a changed proposal version that has not passed the required evaluation path.
- Do not let `proposal-package-assembler` perform proposal cleanup or rewrite.
- Do not start SAP without explicit SAP request or target-output requirement.

## Verification

- Workflow state exists and contains the required fields for the selected entry mode.
- Project directory follows artifact naming and directory rules.
- Every evaluator/reviewer was delegated to an isolated subagent.
- Proposal and SAP version lineage are current.
- Panel mode and reviewer input policy are explicit.
- Panel tier is explicit and matches the reviewer set.
- Final package status is explicit: ready, minor pending, major required, blocked, or partial.
- No unresolved issue was hidden or silently dropped.

## References

- `references/workflow-state-schema.md`: defines the workflow state and artifact registry required across entry paths, revisions, SAP, panel, and package assembly.
- `references/artifact-naming-and-directory-rules.md`: defines project layout, versioned filenames, round directories, current pointers, and artifact index rules.
- `references/delegate-brief-templates.md`: provides evaluator and reviewer delegation brief templates, including blind review input restrictions.
- `references/delegation-rules-pattern.md`: documents the standard isolation and delegation pattern used across evaluator/reviewer skills.
- `references/proposal-writing-methodology.md`: background writing methodology derived from approved proposal examples; use as drafting context, not as workflow state.
