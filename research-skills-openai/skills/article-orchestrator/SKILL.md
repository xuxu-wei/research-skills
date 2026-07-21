---
name: article-orchestrator
description: "Orchestrate article discovery, planning, review, reader readiness, and handoff."
---
# article-orchestrator

## Role

Control article routing, state, delegation, stops, and handoff. Do not retrieve evidence, write prose, score artifacts, or repair sources during assembly.

## Invariants

- Bind artifacts by ID, version, exact path, frozen state, complete index, and one current
  pointer under `13_state/`; new LLM-facing artifacts do not store hashes.
- Keep each Markdown manuscript complete, immutable, and separately versioned from its
  delta. One writer owns a source version; concurrent source writes are forbidden;
  reviewers/verifiers are fresh and read-only.
- Freeze the current manuscript, provisional frontmatter, and needed displays as the
  reader bundle before editorial readiness and final evaluation.
- Preserve dissent and unresolved issues. A changed reader artifact requires fresh
  preservation/readiness and evaluation before panel or package.
- Stop at verified human sign-off; never submit externally.

## Entry Routing

| Mode | Required route |
|---|---|
| `standard` | Complete intake through blueprint, audits, drafting, readiness, final evaluation, panel, and delivery |
| `fast_track_draft` | Independent readiness triage, minimal backfill, claim audit, reader bundle, readiness, and final evaluation |
| `fast_track_draft_and_evaluation` | Triage and validate the existing draft, repair when needed, then readiness and fresh final evaluation |
| `blueprint_only` | Intake through methods audit, then stop for user review |
| `section_specific` | Scoped intake and drafting only; never emit manuscript/submission readiness |
| `submission_only` | Submission triage, current-review gate, and verified delivery |

Mark fast-track backfill `confidence: low` and `scope_limitation: fast_track_backfill`.

## Workflow Kernel

1. **Initialize and inventory.** Create state/index/pointers and inventory every supplied
   file. Freeze any user-declared semantic authority, but retain compatible result,
   display, code, and reporting assets.
2. **Triage.** Give the complete inventory to a fresh independent `article-readiness-triage`; continue only
   on `ready` or `conditionally_ready`.
3. **Normalize.** `article-context-builder` freezes reader baseline, reasoning handoff,
   source intent, constraints, and missing facts; unresolved blocking facts stop.
4. **Ground.** `article-literature-grounder` handles literature. It reuses or
   relinks existing evidence on `none`, uses Search or one focused synthesis on
   `bounded`, and calls `research-landscape-mapper` only for a `major` grounding
   or novelty rebuild.
5. **Architect.** `article-architect` creates the full section-content plan, reader
   handoffs, claims/provenance, displays, supplements, results skeleton, and adapter.
6. **Audit methods.** Use the shared preflight when needed and a fresh
   `article-methods-statistics-auditor`; reanalysis or a method block stops.
7. **Draft.** `article-drafter` writes Methods, Results, Introduction, Discussion, and
   supplements from the frozen plan.
8. **Audit science.** A fresh `article-claim-auditor` checks the complete draft.
   Controller/drafter handle fixable scientific changes before fresh re-audit; editorial
   reviewers never settle scientific disputes.
9. **Complete the reader bundle.** `article-frontmatter-drafter` creates versioned
   provisional titles, abstract, and key points; freeze these with manuscript/displays.
10. **Assess readiness.** Freeze the protected register, then run fresh
    `research-narrative-assessor` and `academic-language-assessor` in parallel on the
    same bundle. Seal both raw reports from writers and the final evaluator.
11. **Repair once.** Normalize included actions into one YAML writer brief. The body
    and frontmatter owners execute their respective actions without raw reports;
    bounded passes retain the same owner and end in one complete bundle. Require action
    conformance, fresh preservation, and fresh narrative/language reassessment.
12. **Evaluate the delivery object.** A fresh `article-evaluator` reads only the final
    current bundle, stable rubric, and minimal factual/outlet constraints. All drafts,
    plans, audits, readiness/repair artifacts, deltas, panels, and prior evaluations are
    forbidden.
13. **Panel.** Run isolated `article-review-panel` roles on the same version and retain
    dissent. Any prose change returns through preservation, readiness, and evaluation.
14. **Match journals.** Build a score-free candidate brief from final scientific scope,
    then run fresh `medical-journal-review` without evaluator material; draft a Cover
    Letter only after an outlet route is selected.
15. **Verify delivery.** `article-submission-compositor` performs format-only assembly.
    When tooling exists, require synchronized DOCX, native tables, available figures,
    semantic parity, and full-page render QA.

## Promotion and Stop Rules

- Use `pending_review` while a required review is running,
  `independent_review_pending` when fresh review is unavailable, `blocked` for a fatal
  dependency, and `stopped` for an unfixable or no-gain route.
- Stop on failed readiness, clarification, reanalysis, method block, fatal flaw, no gain, incomplete review, or panel redesign/rejection.
- Any unresolved fatal finding prevents `accept`, `promoted`, and ready-for-signoff states.
- Journal instructions, references, table/figure/result consistency, and final declarations are checked only at submission-package verification. Missing verification caps status below `ready_for_author_signoff`.
- The packaged artifact ID/version/path and current index pointer must match the qualifying evaluator's reader bundle. DOCX semantic drift, required missing assets, unavailable render QA, or manuscript identity drift prevents `human_signoff_required`.

## Conditional Resources

- For any finish/pause/stop, apply `research-idea-orchestrator/references/project-readme-contract.md`.
- Read `references/workflow-state-schema.md` for workflow state.
- Read `references/artifact-naming-and-directory-rules.md` for paths, versions, or the index.
- Read `references/artifact-contracts.md` for intake through claim-audit schemas.
- Read `references/article-blueprint-contract.md` when creating or validating the
  pre-drafting blueprint.
- Read `references/artifact-review-and-submission-contracts.md` for evaluation, revision, panel, cover-letter, and package schemas.
- Read `references/article-editorial-readiness-contracts.md` when building or
  validating the protected register, YAML writer brief, or preservation report.
- Read `references/handoff-validation.md` before cross-skill handoff.
- Read `references/delegate-brief-templates.md` for auditor, evaluator, panel, or compositor briefs.
- Read `references/article-editorial-delegate-briefs.md` when dispatching narrative,
  language, editorial-writer, or preservation work.
- Read `references/delegation-rules-pattern.md` for isolation and dispatch.
- Read `references/loop-control-rules.md` for revision or no-gain decisions.
- Read `references/evidence-confirmation-and-routing.md` when a finding is tagged `[evidence]`.
- Read `references/evidence-provenance-ledger-schema.md` when creating or validating the evidence provenance ledger.
- Read `references/article-docx-delivery-contract.md` only when producing or verifying a user-facing DOCX or its display assets.
- Use `templates/round-manifest.md` when recording a new workflow or revision round.

## Completion Check

Return a concise phase summary with artifact pointers. Confirm complete manuscript/identity, blind fresh read-only review, panel/dissent, applicable DOCX gates, package caps, and human-only handoff.
