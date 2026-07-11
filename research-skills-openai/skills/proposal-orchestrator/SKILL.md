---
name: proposal-orchestrator
description: "Orchestrate proposal drafting, independent evaluation, revision, optional SAP, panel review, and human-review packaging. Use from an idea, funding call, data opportunity, or existing proposal."
---
# proposal-orchestrator

## Role

Control proposal workflow state, routing, delegation, stop decisions, and final handoff. Do not retrieve evidence, draft or revise proposal/SAP text, score artifacts, or repair source files during assembly.

## Invariants

- Track current pointers in `10_state/workflow-state.yaml` and inventory in `10_state/artifact-index.md`.
- Freeze every delegated input with artifact ID, path, version, and scope limitation.
- Never overwrite `04_drafts/proposal-vNNN.md`; every saved substantive or language-only change creates a new version and lineage record.
- Delegate readiness triage, methodology/statistics preflight, proposal/SAP evaluation, every panel role, and language assessment to fresh independent subagents.
- If independent execution is unavailable, return `independent_review_pending` with a self-contained continuation brief and stop.
- A changed proposal cannot reach panel or packaging until a new `proposal-evaluator` instance evaluates the frozen new version without prior scores or decisions.
- Preserve fatal findings, unresolved issues, conflicts, and panel dissent through final assembly.
- Stop at a package for human review and sign-off; do not submit externally.

## Entry Routing

| Mode | Required route |
|---|---|
| `standard` | Context -> evidence gate -> readiness -> draft -> evaluation loop -> optional SAP -> panel -> package |
| `existing_draft` | Minimal state -> scope-gap record -> evaluation or targeted drafting -> normal downstream gates |
| `draft_and_external_review` | Minimal state -> validate external review provenance -> revision/panel, or fresh evaluation when provenance is insufficient |
| `package_only` | Validate frozen versions and qualifying independent reports -> package; never infer missing readiness |

Skipped artifacts remain `null` with `evaluation_scope_limitation`; do not silently backfill or hide them.

## Workflow Kernel

1. **Initialize.** Record entry mode, user goal, target output, current artifact pointers, SAP request, constraints, and unresolved issues.
2. **Normalize.** Route to `proposal-context-brief-builder` unless a valid frozen brief already matches scope.
3. **Map evidence.** Route broad, stale, conflicting, novelty/gap, guideline, clinical, or funding-call evidence to `research-opportunity-mapper`; reuse a valid map when scope matches.
4. **Triage.** Delegate `proposal-readiness-triage`. Continue on `ready_for_proposal`; ask only blocking questions on `needs_clarification`; route to idea refinement or independent methodology preflight when requested; stop on `not_proposalizable_yet`.
5. **Draft.** Route initial or targeted proposal writing to `proposal-drafter`.
6. **Evaluate.** Delegate a fresh `proposal-evaluator`. Route `accept` forward, `revise` to revision, and `reject` to stop. Do not treat evaluator output as a drafting instruction without a revision plan.
7. **Revise and re-evaluate.** Route findings through `proposal-refinement-controller`; `proposal-drafter` writes a new proposal plus revision plan, response, and delta under `06_revisions/round-NNN/`. Delegate a fresh evaluator using the latest proposal, stable rubric, necessary facts, and optionally an anonymized must-fix list plus delta. Compare sealed rounds only here; stop after two rounds by default or on `stop_no_gain`.
8. **Run optional SAP.** Only when explicitly requested or required by the target output: delegate `methodology-statistics-preflight`, route writing to `sap-writer`, delegate `sap-evaluator`, and route fixable findings through `sap-refinement-controller` plus a fresh SAP evaluator.
9. **Panel.** Treat `proposal-review-panel` as a role contract. Dispatch one fresh subagent per selected role concurrently against the same frozen proposal. Blind reviewers receive neither context/evaluation/delta/unresolved-issue files nor peer outputs. Aggregate only after all required roles return and preserve dissent.
10. **Resolve panel route.** A credible fatal/blocking finding overrides supportive labels. Substantive fixes return to revision and fresh evaluation; unfixable findings stop. If panel requires SAP, run the SAP branch before assembly.
11. **Language QA.** Delegate `academic-language-assessor` against the frozen final proposal. Any saved polishing change creates a new version and requires fresh proposal evaluation.
12. **Assemble.** Route frozen evaluated artifacts to `proposal-package-assembler`. It aggregates only and must not rewrite, clean, re-score, or hide unresolved issues.

## Delegated Brief and Return Contract

Every reviewer brief includes workflow/round IDs, reviewer skill and scope, frozen artifact IDs/versions/paths, allowed files, output path, prohibited reads/writes, and failure route. Every review report includes:

```yaml
review_id:
reviewer_skill:
reviewer_instance_id:
workflow_id:
round_id:
input_artifact_ids: []
input_versions: []
files_read: []
isolation_mode: fresh_subagent
prior_scores_visible: false
source_edits_performed: false
decision:
findings: []
unresolved_issues: []
```

Subtasks return only a concise phase summary plus artifact pointers:

```yaml
phase_summary:
  phase:
  status:
  artifact_ids: []
  artifact_paths: []
  versions: []
  decisions: []
  unresolved_issues: []
  next_route:
```

## Promotion and Stop Rules

- Stop on failed readiness, blocking user facts, blocked evidence, unfixable fatal flaw, SAP/data/endpoint mismatch, no-gain revision, or incomplete independent review.
- Any unresolved fatal finding prevents `accept`, `promoted`, and ready-for-signoff states.
- `support_with_minor_revision` may be packaged only as revision-pending unless the change is completed and freshly evaluated.
- A major panel change never routes directly to a ready package.
- The latest packaged proposal version must match the latest qualifying evaluator report.

## Conditional Resources

- Read `references/workflow-state-schema.md` when creating or validating workflow state.
- Read `references/artifact-naming-and-directory-rules.md` when creating paths, versions, or the artifact index.
- Read `references/delegate-brief-templates.md` for readiness, proposal evaluation, SAP evaluation, and common panel inputs.
- Read `references/reviewer-brief-templates.md` only when dispatching role-specific panel reviewers.
- Read `references/delegation-rules-pattern.md` when selecting isolation and dispatch behavior.
- Read `references/proposal-writing-methodology.md` only when the drafter needs long-form proposal methodology guidance.

## Completion Check

Confirm state/index consistency, unique reviewer instance IDs, prior-score blindness, read-only reviewer scope, new-version/new-evaluator pairing, explicit SAP status, complete panel membership, visible dissent, justified package status, and human-review-only final handoff.
