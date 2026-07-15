---
name: article-orchestrator
description: "Orchestrate full, fast-track, blueprint-only, section-specific, or submission-only article workflows through review and human handoff."
---
# article-orchestrator

## Role

Control article routing, state, delegation, stops, and handoff. Do not retrieve evidence, write prose, score artifacts, or repair sources during assembly.

## Invariants

- Track current pointers under `13_state/`; freeze delegated IDs, paths, versions, digests, scope, and read/write limits.
- Keep every Markdown manuscript complete, identity-bound, immutable, and separately versioned from revisions/deltas.
- Delegate every reviewer/verifier role to a fresh independent subagent; one writer owns each source version and concurrent source writes are forbidden. A changed manuscript requires a fresh evaluator before panel or package.
- Map review wait to `pending_review`, unavailable review to `independent_review_pending`, fatal findings to `blocked`, and no gain to `stopped`; preserve dissent and unresolved issues.
- Stop at verified human sign-off; never submit externally.

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
10. **Revise and re-evaluate.** Controller/drafter writes a complete new manuscript plus separate revision artifacts. Give a fresh evaluator only the latest manuscript/digest, current display assets, stable rubric, necessary facts, and optional anonymous must-fix list. Never expose prior manuscripts, deltas, reports, scores, or decisions; compare sealed rounds and the delta only here.
11. **Panel.** Dispatch one fresh `article-review-panel` subagent per role against the same frozen version; hide evaluator and peer outputs. Aggregate after all return and preserve dissent. Fatal methods findings cap at `not_ready`.
12. **Resolve panel route.** Major or substantive changes return to revision and fresh evaluation. Minor changes that alter prose also create a new version and require fresh evaluation. Unfixable `reject_or_redesign` stops.
13. **Prepare delivery.** Route frontmatter and Cover Letter to their writers. At the existing medical-review point, one fresh `medical-journal-review` may add scoped probability to its same report.
14. **Verify package.** Delegate `article-submission-compositor` against frozen sources. When DOCX-capable document tooling exists, require a synchronized DOCX with native tables, embedded figures, parity checks, and page-render QA. It may format and verify only; it must not repair source content.

## Promotion and Stop Rules

- Stop on failed readiness, clarification, reanalysis, method block, fatal flaw, no gain, incomplete review, or panel redesign/rejection.
- Any unresolved fatal finding prevents `accept`, `promoted`, and ready-for-signoff states.
- Journal instructions, references, table/figure/result consistency, and final declarations are checked only at submission-package verification. Missing verification caps status below `ready_for_author_signoff`.
- The packaged Markdown digest must match the qualifying evaluator. DOCX content drift, required missing assets, unavailable render QA, or manuscript identity drift prevents `human_signoff_required`.

## Conditional Resources

- For any finish/pause/stop, apply `research-idea-orchestrator/references/project-readme-contract.md`.
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
- Read `references/article-docx-delivery-contract.md` only when producing or verifying a user-facing DOCX or its display assets.
- Use `templates/round-manifest.md` when recording a new workflow or revision round.

## Completion Check

Return a concise phase summary with artifact pointers. Confirm complete manuscript/identity, blind fresh read-only review, panel/dissent, applicable DOCX gates, package caps, and human-only handoff.
