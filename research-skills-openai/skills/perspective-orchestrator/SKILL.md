---
name: perspective-orchestrator
description: "Orchestrate a Perspective, Viewpoint, or Commentary from thesis and evidence through review, revision, panel, and human delivery."
---
# perspective-orchestrator

## Role

Control Perspective workflow state, routing, delegation, stop decisions, and final handoff. Do not edit the claim ledger, draft/revise prose, score artifacts, or repair source text during final composition.

## Invariants

- Track state and decisions under `09_state/`.
- Keep `01_claims/claim-ledger.md` read-only except for writes by `perspective-claim-evidence-curator`; other roles submit change requests.
- Store drafts as `04_drafts/perspective-vNNN.md`; every saved change creates a version and lineage record.
- Delegate evaluator, every panel role, language assessor, medical journal reviewer, and final compositor/verifier to fresh independent subagents.
- Use registry states: review wait -> `pending_review`; unavailable reviewer -> `independent_review_pending`; fatal -> `blocked`; unfixable/no gain -> `stopped`; verified package -> `human_signoff_required`.
- Phase delegation is allowed, but each source artifact/version has one writer; never run concurrent source writes.
- A changed draft cannot reach panel, final composition, or a ready state until a new `perspective-evaluator` instance evaluates the frozen new version without prior scores or decisions.
- Preserve fatal findings, unresolved issues, conflicts, and dissent in the final artifact index and report.
- Stop at human sign-off; do not submit externally.

## Modes

| Mode | Route and output |
|---|---|
| `lite` | Input -> provisional claims/evidence -> architecture -> early feasibility; no full retrieval or ready status |
| `standard` | Input -> claims/evidence -> architecture -> draft -> evaluation -> one revision loop by default |
| `full` | Standard plus panel, language QA, final independent composition/verification |

## Workflow Kernel

1. **Initialize.** Create layout, state, decision log, mode, goal, target, pointers, and unresolved issues.
2. **Build input.** Route input normalization and outlet profile to `perspective-input-builder`; ask only for blocking thesis choices.
3. **Curate claims and evidence.** Route ledger, claim-evidence matrix, discourse baseline, contrary evidence, citation risks, and limits to `perspective-claim-evidence-curator`; route broad evidence to `research-opportunity-mapper` in standard/full mode.
4. **Architect.** Route the argument chain and paragraph plan to `perspective-argument-architect`; approved claim changes return to the curator.
5. **Draft.** Route frozen architecture and claim artifacts to `perspective-drafter`; require a new version plus paragraph map and prohibit unregistered claims.
6. **Evaluate.** Delegate a fresh `perspective-evaluator`. Route `accept` forward; route revision, argument/evidence rebuild, thesis redesign, or outlet retargeting to the owning upstream role; stop on `reject_not_salvageable`.
7. **Revise and re-evaluate.** Save the new version, plan, response, and delta in `06_revisions/round-NNN/`; give a fresh evaluator only the latest draft, stable rubric, necessary facts, and optional anonymous must-fix list. Seal prior drafts/deltas. Compare sealed rounds here; stop on no gain or round limit.
8. **Panel.** Dispatch counter-position, evidence, and narrative roles of `perspective-review-panel` concurrently in fresh subagents; add conditional roles only when triggered. Hide evaluator and peer reports; aggregate after all return and preserve dissent.
9. **Resolve panel route.** Strong support proceeds; major/substantive changes return to revision and fresh evaluation; not-ready returns upstream; unfixable redesign/rejection stops.

### STEP 8.5: Panel Minor Revision Patch

Route minor/editorial must-fix items through controller/drafter, save a new draft/map/delta, and use a fresh evaluator without prior scores. Proceed only after `accept`; substantive changes use major revision and no changed draft goes directly to the compositor.

### STEP 9: Final Compositor

1. If requested, route frozen qualifying inputs to `article-cover-letter`; freeze its versioned pair under `08_cover-letter/`.
2. At the existing medical-review point, use one fresh `medical-journal-review` for biomedical review or requested publication probability; its same report holds any estimate.
3. Run fresh language assessment; saved changes require a new version and evaluation.
4. Give frozen sources, optional letter, and review to a fresh compositor; it may copy/verify only and cannot recalculate probability.
5. Write the final manuscript, optional identical letter, logs, and reports under `08_final/`.

## Delegated Brief and Return Contract

Every reviewer brief records workflow/round, skill/scope, frozen IDs/versions/paths, allowed files, output path, prohibited reads/writes, and failure route. Reports use standard review identity, files-read, isolation, prior-score, source-edit, decision, finding, and unresolved-issue fields. Subtasks return only a concise phase summary with artifact pointers, versions, decisions, unresolved issues, and `next_route`.

## Promotion and Stop Rules

- Stop on blocking input/readiness gaps, insufficient evidence, unfixable fatal flaw, exhausted caveat budget, no-gain revision, incomplete independent review, or panel redesign/rejection.
- Any unresolved fatal finding prevents `accept`, `promoted`, and ready-for-signoff states.
- The latest final draft version must match the latest qualifying evaluator report.

## Conditional Resources

- For any finish/pause/stop, apply `research-idea-orchestrator/references/project-readme-contract.md`.
- Read `references/workflow-modes.md` when selecting lite, standard, or full mode.
- Read `references/workflow-manifest-schema.md` for workflow state.
- Read `references/decision-log-schema.md` for overrides, user decisions, or accepted risks.
- Read `references/artifact-naming-and-directory-rules.md` for paths, versions, or the index.
- Read `references/io-contracts.md` when validating a component handoff.
- Read `references/delegate-brief-templates.md` for evaluator, panel, assessor, or compositor briefs.
- Read `references/loop-control-rules.md` for revision or no-gain decisions.
- Read `references/panel-decision-routing.md` for panel aggregation and routing.
- Read `references/generic-outlet-profiles.md` only when the user has not selected an outlet.
- Read `references/anti-patterns.md` during final workflow verification.

## Completion Check

Confirm state/log consistency, curator-only ledger writes, blind fresh review, version/evaluator pairing, panel/dissent, status caps, and human-only handoff.
