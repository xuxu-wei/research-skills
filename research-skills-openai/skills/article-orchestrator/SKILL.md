---
name: article-orchestrator
description: "Orchestrate full, fast-track, blueprint-only, section-specific, or submission-only article workflows through review and human handoff."
---
# article-orchestrator

## Role

Control article routing, state, delegation, stops, and handoff. Do not retrieve evidence, write prose, score artifacts, or repair sources during assembly.

## Invariants

- Track current pointers and inventory under `13_state/`; freeze every delegated input with artifact ID, path, version, and scope.
- Never overwrite `06_drafts/manuscript-vNNN.md`; every saved change creates a version and lineage record.
- Delegate readiness triage, methods/statistics audit, claim audit, evaluation, every panel role, language assessment, medical journal review, and submission verification to fresh independent subagents.
- Use registry states: review wait -> `pending_review`; unavailable reviewer -> `independent_review_pending`; fatal -> `blocked`; unfixable/no gain -> `stopped`; verified package -> `human_signoff_required`.
- Phase delegation is allowed, but each source artifact/version has one writer; never run concurrent source writes.
- A changed manuscript cannot reach panel, packaging, or readiness until a fresh `article-evaluator` evaluates its frozen new version without prior scores.
- Preserve fatal findings, unresolved issues, conflicts, and dissent through final packaging.
- Stop at human sign-off; do not submit externally.

## Entry Routing

| Mode | Required route |
|---|---|
| `standard` | Intake -> triage -> context -> grounding -> blueprint -> methods audit -> draft -> claim audit -> evaluation loop -> panel -> delivery |
| `fast_track_draft` | Intake -> readiness triage -> minimal backfill -> claim audit/evaluation |
| `fast_track_draft_and_evaluation` | Intake -> triage -> validate review provenance -> refinement/panel or fresh evaluation |
| `blueprint_only` | Intake through methods audit, then stop for user review |
| `section_specific` | Scoped intake -> minimal context -> drafter; never emit manuscript-ready or submission-ready status |
| `submission_only` | Intake -> submission triage -> current evaluation gate -> delivery; stale review returns to claim audit/evaluation |

Mark fast-track backfill `confidence: low` and `scope_limitation: fast_track_backfill`.

## Workflow Kernel

1. **Initialize.** Create state, layout, index, mode, goal, target, current step, pointers, and unresolved issues.
2. **Triage.** Delegate `article-readiness-triage`. Continue only on `ready` or `conditionally_ready`; stop on `not_ready` or `wrong_article_type`.
3. **Normalize.** Route to `article-context-builder`; stop when blocking clarification is required.
4. **Ground.** Route literature to `article-literature-grounder`; it may call `research-opportunity-mapper` for missing, stale, or conflicting evidence.
5. **Architect.** Route blueprint, claims, provenance, displays, supplements, results skeleton, and journal adapter to `article-architect`.
6. **Audit methods.** Delegate `methodology-statistics-preflight` when quick feasibility screening is needed, then delegate `article-methods-statistics-auditor`. Stop on `requires_reanalysis` or `methodologically_blocked`.
7. **Draft.** Route Methods -> Results -> Introduction -> Discussion and supplementary organization to `article-drafter`.
8. **Audit claims.** Delegate `article-claim-auditor`. Route fixable repairs through controller/drafter, then use a fresh auditor; stop on fatal overclaims.
9. **Evaluate.** In parallel, delegate a fresh `article-evaluator` and optional `academic-language-assessor`; keep reports sealed. Route `accept`, `revise`, or `reject`.
10. **Revise and re-evaluate.** Controller/drafter writes a new version, plan, response, and delta under `09_revisions/round-NNN/`. Use a fresh evaluator with latest draft, stable rubric, necessary facts, and optional anonymous must-fix list plus delta. Compare sealed rounds only here; stop after two rounds or `stop_no_gain`.
11. **Panel.** Dispatch one fresh `article-review-panel` subagent per role against the same frozen version; hide evaluator and peer outputs. Aggregate after all return and preserve dissent. Fatal methods findings cap at `not_ready`.
12. **Resolve panel route.** Major or substantive changes return to revision and fresh evaluation. Minor changes that alter prose also create a new version and require fresh evaluation. Unfixable `reject_or_redesign` stops.
13. **Prepare delivery.** Route frontmatter to `article-frontmatter-drafter`, cover letter to `article-cover-letter`, and biomedical cover-letter review to a fresh `medical-journal-review` instance.
14. **Verify package.** Delegate `article-submission-compositor` against frozen sources. It may assemble and verify only; it must not rewrite, patch, re-score, or hide issues.

## Delegated Brief and Return Contract

Every reviewer brief includes workflow/round, scope, frozen IDs/versions/paths, allowed files, output path, prohibited reads/writes, and failure route. Require standard review identity and isolation fields.

Subtasks return a phase summary with status, artifact pointers/versions, decisions, unresolved issues, and `next_route`.

## Promotion and Stop Rules

- Stop on failed readiness, clarification, reanalysis, method block, fatal flaw, no gain, incomplete review, or panel redesign/rejection.
- Any unresolved fatal finding prevents `accept`, `promoted`, and ready-for-signoff states.
- Journal instructions, references, table/figure/result consistency, and final declarations are checked only at submission-package verification. Missing verification caps status below `ready_for_author_signoff`.
- The latest packaged manuscript version must match the latest qualifying evaluator report.

## Conditional Resources

- Read `references/workflow-state-schema.md` for workflow state.
- Read `references/artifact-naming-and-directory-rules.md` for paths, versions, or the index.
- Read `references/artifact-contracts.md` for intake through claim-audit schemas.
- Read `references/artifact-review-and-submission-contracts.md` for evaluation, revision, panel, cover-letter, and package schemas.
- Read `references/handoff-validation.md` before cross-skill handoff.
- Read `references/delegate-brief-templates.md` for auditor, evaluator, panel, or compositor briefs.
- Read `references/delegation-rules-pattern.md` for isolation and dispatch.
- Read `references/loop-control-rules.md` for revision or no-gain decisions.
- Read `references/evidence-confirmation-and-routing.md` when a finding is tagged `[evidence]`.
- Read `references/evidence-provenance-ledger-schema.md` when creating or validating the evidence provenance ledger.
- Use `templates/round-manifest.md` when recording a new workflow or revision round.

## Completion Check

Confirm state and index consistency, unique reviewer instance IDs, prior-score blindness, read-only reviewer scope, new-version/new-evaluator pairing, complete panel membership, visible dissent, package status caps, and a human-review-only final state.
