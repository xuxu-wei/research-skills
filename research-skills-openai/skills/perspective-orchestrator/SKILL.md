---
name: perspective-orchestrator
description: "Orchestrate Perspective, Viewpoint, or Commentary writing from thesis and evidence through independent evaluation, revision, panel review, and final human-review delivery."
---
# perspective-orchestrator

## Role

Control Perspective workflow state, routing, delegation, stop decisions, and final handoff. Do not edit the claim ledger, draft/revise prose, score artifacts, or repair source text during final composition.

## Invariants

- Track current state in `09_state/workflow-manifest.yaml` and decisions in `09_state/decision-log.md`.
- Keep `01_claims/claim-ledger.md` read-only except for writes by `perspective-claim-evidence-curator`; other roles submit change requests.
- Store drafts as `04_drafts/perspective-vNNN.md`; any saved substantive or language-only change creates a new version and lineage record.
- Delegate evaluator, every panel role, language assessor, medical journal reviewer, and final compositor/verifier to fresh independent subagents.
- If independent execution is unavailable, return `independent_review_pending` with a self-contained continuation brief and stop.
- A changed draft cannot reach panel, final composition, or a ready state until a new `perspective-evaluator` instance evaluates the frozen new version without prior scores or decisions.
- Preserve fatal findings, unresolved issues, conflicts, and dissent in the final artifact index and report.
- Stop at a package for human review and sign-off; do not submit externally.

## Modes

| Mode | Route and output |
|---|---|
| `lite` | Input -> provisional claims/evidence -> architecture -> early feasibility; no full retrieval or ready status |
| `standard` | Input -> claims/evidence -> architecture -> draft -> evaluation -> one revision loop by default |
| `full` | Standard plus panel, language QA, final independent composition/verification |

## Workflow Kernel

1. **Initialize.** Create numbered project directories, state, decision log, entry mode, user goal, target outlet, artifact pointers, and unresolved issues.
2. **Build input.** Route input normalization and outlet profile to `perspective-input-builder`; ask only for blocking thesis choices.
3. **Curate claims and evidence.** Route claim ledger, claim-evidence matrix, discourse baseline, contrary evidence, citation risks, and limitations to `perspective-claim-evidence-curator`. Route broad evidence needs to `research-opportunity-mapper` in standard/full mode.
4. **Architect.** Route the argument chain and paragraph plan to `perspective-argument-architect`; approved claim changes return to the curator.
5. **Draft.** Route frozen architecture and claim artifacts to `perspective-drafter`; require a new version plus paragraph map and prohibit unregistered claims.
6. **Evaluate.** Delegate a fresh `perspective-evaluator`. Route `accept` forward; route revision, argument/evidence rebuild, thesis redesign, or outlet retargeting to the owning upstream role; stop on `reject_not_salvageable`.
7. **Revise and re-evaluate.** Route evaluation findings through `perspective-refinement-controller` and the drafter. Create a new version, revision plan, response, and delta in `06_revisions/round-NNN/`, then delegate a fresh evaluator using only the latest draft, stable rubric, necessary factual artifacts, and optionally an anonymized must-fix list plus delta. Compare sealed rounds only here; stop on no gain or exhausted round limit.
8. **Panel.** Treat `perspective-review-panel` as a role contract. Dispatch counter-position, evidence, and narrative roles concurrently in separate fresh subagents; add methodology/statistics, clinician, or outlet-fit roles only when triggered. Do not expose evaluator or peer reports. Aggregate only after every required role returns and preserve dissent.
9. **Resolve panel route.** Strong support proceeds; major/substantive changes return to revision and fresh evaluation; not-ready returns upstream; unfixable redesign/rejection stops.

### STEP 8.5: Panel Minor Revision Patch

- Route only minor/editorial must-fix items through `perspective-refinement-controller` and `perspective-drafter`.
- Save a new `perspective-vNNN.md`, paragraph map, mini-delta, artifact ID, and version.
- Freeze the changed draft and delegate a fresh independent `perspective-evaluator` that cannot see prior scores or decisions.
- Proceed only after `accept`; otherwise route to the corresponding revision or upstream rebuild.
- 不得让 panel minor patch 直接进入 final compositor. If the patch changes substantive argumentation, upgrade it to major revision.

### STEP 9: Final Compositor

1. When biomedical journal review is applicable, first delegate a fresh `medical-journal-review`; route blocking substantive findings back before composition.
2. Delegate `academic-language-assessor` against the frozen final draft. Any saved polishing change creates a new version and fresh evaluation requirement.
3. Delegate `perspective-final-compositor` against frozen draft, claims, evidence, outlet, panel, and reference artifacts. It may assemble and verify only; it must not repair source prose.
4. Write final manuscript, edit log, compositor report, and submission-readiness report under `08_final/`.

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

- Stop on blocking input/readiness gaps, insufficient evidence, unfixable fatal flaw, exhausted caveat budget, no-gain revision, incomplete independent review, or panel redesign/rejection.
- Any unresolved fatal finding prevents `accept`, `promoted`, and ready-for-signoff states.
- The latest final draft version must match the latest qualifying evaluator report.

## Conditional Resources

- Read `references/workflow-modes.md` when selecting lite, standard, or full mode.
- Read `references/workflow-manifest-schema.md` when creating or validating workflow state.
- Read `references/decision-log-schema.md` when recording an override, user decision, or accepted risk.
- Read `references/artifact-naming-and-directory-rules.md` when creating paths, versions, or the artifact index.
- Read `references/io-contracts.md` when validating a component handoff.
- Read `references/delegate-brief-templates.md` when preparing evaluator, panel, assessor, or compositor briefs.
- Read `references/loop-control-rules.md` when a revision loop starts or no-gain is possible.
- Read `references/panel-decision-routing.md` when aggregating and routing panel outcomes.
- Read `references/generic-outlet-profiles.md` only when the user has not selected an outlet.
- Read `references/anti-patterns.md` during final workflow verification.

## Completion Check

Confirm state and decision-log consistency, curator-only ledger writes, unique reviewer instance IDs, prior-score blindness, new-version/new-evaluator pairing, complete panel membership, visible dissent, justified status caps, and human-review-only final handoff.
