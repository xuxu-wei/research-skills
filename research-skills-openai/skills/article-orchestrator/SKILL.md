---
name: article-orchestrator
description: "Orchestrate article drafting, independent review, revision, and human-review packaging. Use for full, fast-track, blueprint-only, section-specific, or submission-only workflows."
---
# article-orchestrator

## Role

Control article routing, state, delegation, stops, and handoff. Do not retrieve evidence, write prose, score artifacts, or repair sources during assembly.

## Invariants

- Track current pointers in `13_state/workflow-state.yaml` and inventory in `13_state/artifact-index.md`.
- Freeze every delegated input with artifact ID, path, version, and scope limitation.
- Never overwrite `06_drafts/manuscript-vNNN.md`; every saved text change creates a new version and lineage record.
- Delegate readiness triage, methods/statistics audit, claim audit, evaluation, every panel role, language assessment, medical journal review, and submission verification to fresh independent subagents.
- Use registry states: review wait -> `pending_review`; unavailable reviewer -> `independent_review_pending`; fatal -> `blocked`; unfixable/no gain -> `stopped`; verified package -> `human_signoff_required`.
- Phase delegation is allowed, but each source artifact/version has one writer; never run concurrent writes to the same source.
- A changed manuscript cannot reach panel, packaging, or readiness until a fresh `article-evaluator` evaluates its frozen new version without prior scores.
- Preserve fatal findings, unresolved issues, conflicts, and dissent through final packaging.
- Stop at human sign-off; do not submit externally.

## Entry Routing

| Mode | Required route |
|---|---|
| `standard` | Intake -> triage -> context -> grounding -> blueprint -> methods audit -> draft -> claim audit -> evaluation loop -> panel -> delivery |
| `fast_track_draft` | Intake -> Step 1 (independent readiness triage) -> minimal backfill -> claim audit/evaluation |
| `fast_track_draft_and_evaluation` | Intake -> triage -> validate external review provenance -> refinement/panel, or fresh evaluation when provenance is insufficient |
| `blueprint_only` | Intake through methods audit, then stop for user review |
| `section_specific` | Scoped intake -> minimal context -> drafter; never emit manuscript-ready or submission-ready status |
| `submission_only` | Intake -> submission triage -> current-version evaluation gate -> delivery; if evaluation is missing/stale, run claim audit and fresh evaluation first |

Mark fast-track backfill `confidence: low` and `scope_limitation: fast_track_backfill`.

## Workflow Kernel

1. **Initialize.** Create state, directory layout, artifact index, entry mode, user goal, target journal, current phase/step, artifact pointers, and unresolved issues.
2. **Triage.** Delegate `article-readiness-triage`. Continue only on `ready` or `conditionally_ready`; stop on `not_ready` or `wrong_article_type`.
3. **Normalize.** Route to `article-context-builder`; stop when blocking clarification is required.
4. **Ground.** Route literature work to `article-literature-grounder`; it may call `research-opportunity-mapper` when evidence is missing, stale, or conflicting.
5. **Architect.** Route blueprint, claim-evidence matrix, evidence provenance ledger, display plan, supplementary index, results skeleton, and journal adapter to `article-architect`.
6. **Audit methods.** Delegate `methodology-statistics-preflight` when quick feasibility screening is needed, then delegate `article-methods-statistics-auditor`. Stop on `requires_reanalysis` or `methodologically_blocked`.
7. **Draft.** Route Methods -> Results -> Introduction -> Discussion and supplementary organization to `article-drafter`.
8. **Audit claims.** Delegate `article-claim-auditor`. Route fixable downscaling or repair through `article-refinement-controller` and `article-drafter`, then use a fresh claim auditor; stop on unfixable fatal overclaims.
9. **Evaluate.** In parallel, delegate a fresh `article-evaluator` and, when language QA is in scope, `academic-language-assessor`. Keep their reports sealed from one another. Route `accept` forward, `revise` to revision, and `reject` to stop.
10. **Revise and re-evaluate.** Route findings through `article-refinement-controller`; the drafter writes a new version plus revision plan, response, and delta under `09_revisions/round-NNN/`. Delegate a fresh evaluator using only the latest draft, stable rubric, necessary factual artifacts, and optionally an anonymized must-fix list plus delta. Compare sealed rounds only in this orchestrator; stop after two rounds by default or on `stop_no_gain`.
11. **Panel.** Treat `article-review-panel` as a role contract. Dispatch one fresh subagent per selected role concurrently against the same frozen version; do not expose evaluator or peer outputs. Aggregate only after all required roles return, preserving dissent. A fatal methods finding caps the recommendation at `not_ready`.
12. **Resolve panel route.** Major or substantive changes return to revision and fresh evaluation. Minor changes that alter prose also create a new version and require fresh evaluation. Unfixable `reject_or_redesign` stops.
13. **Prepare delivery.** Route frontmatter to `article-frontmatter-drafter`, cover letter to `article-cover-letter`, and biomedical cover-letter review to a fresh `medical-journal-review` instance.
14. **Verify package.** Delegate `article-submission-compositor` against frozen sources. It may assemble and verify only; it must not rewrite, patch, re-score, or hide issues.

## Delegated Brief and Return Contract

Every reviewer brief includes workflow/round IDs, scope, frozen IDs/versions/paths, allowed files, output path, prohibited reads/writes, and failure route. Require standard identity, files-read, isolation, prior-score, source-edit, decision, finding, and unresolved-issue fields.

Subtasks return a phase summary with status, artifact pointers/versions, decisions, unresolved issues, and `next_route`.

## Promotion and Stop Rules

- Stop on failed readiness, blocking clarification, required reanalysis, methodological block, unfixable claim/fatal flaw, no-gain revision, incomplete independent review, or panel redesign/rejection.
- Any unresolved fatal finding prevents `accept`, `promoted`, and ready-for-signoff states.
- Journal instructions, references, table/figure/result consistency, and final declarations are checked only at submission-package verification. Missing verification caps status below `ready_for_author_signoff`.
- The latest packaged manuscript version must match the latest qualifying evaluator report.

## Conditional Resources

- Read `references/workflow-state-schema.md` when creating or validating workflow state.
- Read `references/artifact-naming-and-directory-rules.md` when creating paths, versions, or the artifact index.
- Read `references/artifact-contracts.md` for intake through claim-audit schemas.
- Read `references/artifact-review-and-submission-contracts.md` for evaluation, revision, panel, cover-letter, and package schemas.
- Read `references/handoff-validation.md` before any cross-skill handoff.
- Read `references/delegate-brief-templates.md` when preparing auditor, evaluator, panel, or compositor briefs.
- Read `references/delegation-rules-pattern.md` when selecting isolation and dispatch behavior.
- Read `references/loop-control-rules.md` when a revision loop starts or a no-gain decision is possible.
- Read `references/evidence-confirmation-and-routing.md` when a finding is tagged `[evidence]`.
- Read `references/evidence-provenance-ledger-schema.md` when creating or validating the evidence provenance ledger.
- Use `templates/round-manifest.md` when recording a new workflow or revision round.

## Completion Check

Confirm state and index consistency, unique reviewer instance IDs, prior-score blindness, read-only reviewer scope, new-version/new-evaluator pairing, complete panel membership, visible dissent, package status caps, and a human-review-only final state.
