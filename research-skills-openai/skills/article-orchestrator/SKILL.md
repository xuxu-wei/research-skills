---
name: article-orchestrator
description: "Orchestrate research-article workflow from existing research data, results, and study design information through input governance, architecture governance, evidence-constrained drafting, multi-layer quality control, and submission package assembly. Entry paths: Standard (full pipeline), Fast-Track (existing draft), Blueprint-Only, Section-Specific, Submission-Only."
---
# article-orchestrator

## Purpose

Use this skill when the user has existing research data, results, and study design background information and wants to produce a manuscript package for final human review and sign-off.

This skill is the workflow controller. It does not generate raw ideas, retrieve evidence directly, draft manuscript text, evaluate its own outputs, revise manuscript content, or replace specialist skills.

## Core Rules

- Maintain a workflow state using `references/workflow-state-schema.md`.
- Maintain project directories and artifact names using `references/artifact-naming-and-directory-rules.md`.
- Run `article-readiness-triage` BEFORE `article-context-builder`. A Minimal Intake Summary (orchestrator inline) precedes triage.
- Fast-track entry is allowed only when a minimal workflow state is created and skipped artifacts are recorded as `scope_limitation`.
- Fast-track entry must pass minimum backfill gates for context, CEM, EPL, methods/statistical scope, and claim audit before any downstream readiness label is assigned.
- Use `research-opportunity-mapper` for evidence retrieval when evidence is missing, stale, or conflicting.
- Explicitly delegate `methodology-statistics-preflight` to a fresh independent subagent for quick feasibility screening before `article-methods-statistics-auditor`.
- Explicitly delegate `academic-language-assessor` to a fresh independent subagent for English, Chinese, or bilingual language quality evaluation during evaluation and refinement.
- Manuscript work is file-centered: track `draft_path`, `draft_version`, state updates, evaluation reports, revision history, and unresolved issues.
- Do not overwrite manuscript versions. Substantive edits create a new `06_drafts/manuscript-vNNN.md`; language polishing or formatting that saves a changed draft also creates a new version and records `change_type: language_only` or `change_type: formatting_only`.
- `13_state/workflow-state.yaml` records the current version; `13_state/artifact-index.md` records the human-readable inventory.
- Run readiness triage, methods/statistics audit, claim audit, evaluation, every panel reviewer, and submission verification in fresh independent subagents or delegated threads. Never substitute inline review.
- `article-drafter` writes or revises; `article-evaluator` evaluates; `article-refinement-controller` manages revision loops. Do not merge these roles.
- `article-submission-compositor` assembles existing artifacts only. It must not clean, rewrite, patch, re-score, or hide unresolved issues.
- Supplementary materials are planned by `article-architect`, organized by `article-drafter`, reviewed by `article-evaluator`, and compliance-checked by `article-submission-compositor`.
- Revision records (revision-plan, response-to-reviewers, revision-delta, language-change-log when applicable) are saved in `09_revisions/round-NNN/` separate from drafts.
- Reference verification, table/figure/result consistency, journal instruction verification, and ethics/declarations checks are mandatory pre-submission verification gates. If any are unavailable or partial, final status is capped below `ready_for_author_signoff`.

## Orchestrator-Owned Contract References

This skill owns the contract references for the research-article package. Read `references/artifact-contracts.md`, `references/artifact-naming-and-directory-rules.md`, and `references/handoff-validation.md` directly when their contracts are needed. Include the relevant frozen contract excerpts in a delegated brief when the subagent cannot read the files by path. Do not introduce a `_shared` skill.

## Workflow State

At workflow start, create or update the state fields defined in `references/workflow-state-schema.md`.

Also create the project directory layout and artifact index defined in `references/artifact-naming-and-directory-rules.md`.

Minimum state required for every entry path:

- `entry_mode`
- `user_goal`
- `target_journal`
- `current_phase`
- `current_step`
- `artifacts` (may be empty for standard entry)
- `unresolved_issues`

If fast-track mode skips steps, set the missing artifact paths to `null` and add `scope_limitation`. Downstream evaluator or reviewer briefs must include that limitation.

## Entry Paths

### Standard Entry

Use when the user provides research data, results, and study design information and wants to go through the full pipeline.

Run the full 15-step sequence (see Steps section).

### Fast-Track: Has Draft

Use when the user provides an existing manuscript draft.

Run Step 0 (Minimal Intake Summary) → backfill → Step 9 (Claim Audit) or Step 10 (Evaluation).

Backfill mechanism (orchestrator inline):
1. Parse manuscript to extract: research design, population, variables, statistical methods
2. Infer claim map from Results and Discussion paragraphs
3. Infer evidence map from numerical results and citations
4. Build minimal context brief (source: reverse_engineered_from_draft)
5. All backfilled artifacts marked `confidence: low` and `scope_limitation: fast_track_backfill`
6. Run minimum handoff validation before Step 9/10; if methods/statistical output or evidence provenance is missing, cap downstream package status at `ready_for_author_check`

### Fast-Track: Draft + Evaluation

Use when the user has a draft and an external evaluation report.

Route to Step 11 (Refinement) or Step 12 (Review Panel), depending on evaluation decision.

### Blueprint-Only Entry

Use when the user wants to review the article architecture before drafting.

Run Step 0 through Step 7. Stop and present the blueprint for user confirmation.

### Section-Specific Entry

Use when the user only needs drafting or revision of specific sections.

Run Step 0 → minimal context → route to `article-drafter` in section-specific mode.

### Submission-Only Entry

Use when the user has a final manuscript and only needs submission materials.

Run Step 0 → minimal context → route to Step 13 (Frontmatter Drafting).

## Steps

### Step 0: Minimal Intake Summary (orchestrator inline)

Extract the minimum information needed for readiness triage.

Do NOT perform full context normalization — that is Step 2.

Output `minimal_intake_summary`:

- study_topic
- apparent_study_type (rough classification)
- available_materials (protocol, primary results, tables/figures, statistical outputs, methods description, references)
- stated_target_journal
- obvious_missing_items

### Phase 1: Input Governance

#### Step 1: Article Readiness Triage

Explicitly delegate `article-readiness-triage` to a fresh independent subagent or delegated thread with frozen input identity. If that is unavailable, record `independent_review_pending`, emit a continuation brief, and stop.

Input: `minimal_intake_summary`.

The triage must answer: can this research be written into a manuscript? What article type? Are there blocking gaps? Is the target journal realistic?

State updates:
- set `readiness_report_path`
- set `readiness_status`
- route according to readiness decision

Route:
- `ready` or `conditionally_ready` → continue to Step 2
- `not_ready` → stop, return blocking gaps
- `wrong_article_type` → recommend alternative article type, stop

#### Step 2: Context Brief + Reporting Standard Selection

Call `article-context-builder`.

Internal three-step process: Normalize → Classify → Gate.

Reporting standard mapping must support: multi-standard use, extension priority, journal override, hybrid design main+supplementary, and `no_exact_guideline_found`.

State updates:
- set `context_brief_path`
- set `proceed_status`
- update `study_type`, `reporting_standard`, `target_journal`

#### Step 3: Literature Grounding

Call `article-literature-grounder`.

Must produce a searchable, auditable literature grounding report with search protocol, coverage assessment, novelty position, competing evidence, and citation risk.

State updates:
- set `literature_grounding_path`
- set `grounding_confidence`

### Phase 2: Architecture Governance

#### Step 4: Article Blueprint

Call `article-architect`.

Produces: Contribution Statement, Study Type Confirmation, Core Q&A, Claim-Evidence Matrix, Evidence Display Plan, Supplementary Index, Results Skeleton, Journal Adapter, Reviewer Risk Preview.

State updates:
- set `blueprint_path`

#### Step 5: Claim-Evidence Matrix + Evidence Provenance Ledger

Done by `article-architect` as part of Step 4 blueprint.

#### Step 6: Evidence Display Plan + Supplementary Index

Done by `article-architect` as part of Step 4 blueprint.

The Supplementary Index records every item planned for supplementary materials: type, supporting claims, main-text reference location, journal requirement status.

#### Step 7: Methods / Statistics Audit

Explicitly delegate `article-methods-statistics-auditor` to a fresh independent subagent or delegated thread with frozen input identities and versions. If that is unavailable, record `independent_review_pending`, emit a continuation brief, and stop.

Input: context brief, protocol/SAP (if available), statistical outputs (recommended), tables/figures (optional).

Audit must answer: does the study design support the primary inference? Are there unfixable methodological flaws?

State updates:
- set `methods_audit_path`
- set `audit_status`

Route:
- `pass` or `conditionally_pass_with_author_verification` → continue
- `requires_methods_clarification` → continue with flag
- `requires_reanalysis` → stop, inform user
- `methodologically_blocked` → stop

### Phase 3: Writing

#### Step 8: Manuscript Drafting + Supplementary Organization

Call `article-drafter`.

Drafting order: Methods → Results → Introduction → Discussion.
Then organize supplementary materials per the Supplementary Index.

State updates:
- set `draft_path`, `draft_version`
- set `draft_status: drafted`
- set `supplementary_path`

### Phase 4: Quality Control

#### Step 9: Claim-Level Audit

Explicitly delegate `article-claim-auditor` to a fresh independent subagent or delegated thread with frozen input identities and versions. If that is unavailable, record `independent_review_pending`, emit a continuation brief, and stop.

Audit each claim for evidence support, inference validity, wording appropriateness, and boundary clarity.

Route:
- `pass` → continue to Step 10
- `downscale_and_proceed` → Step 11 (claim downscaling)
- `revise_and_reaudit` → Step 11, then repeat claim audit
- `blocked` with fixable fatal overclaims → Step 11 (claim downscaling/removal), then repeat claim audit
- `blocked` with unfixable fatal overclaims → stop; writing cannot responsibly repair the claim

State updates:
- set `claim_audit_path`

#### Step 10: Independent Evaluation

Explicitly delegate `article-evaluator` to a fresh independent subagent or delegated thread with frozen input identities and versions. For re-evaluation, create a new evaluator instance that has not seen the prior score or decision. It reads only the latest draft, stable rubric, and necessary factual artifacts. If delegation is unavailable, record `independent_review_pending`, emit a continuation brief, and stop.

The orchestrator separately delegates `academic-language-assessor` to a fresh independent subagent. The language assessor and article evaluator do not read one another's reports; the orchestrator compares their sealed reports after both return.

Seven-dimension scoring with non-compensatory gates on Scientific Validity, Evidence-Claim Alignment, and Language Baseline.

Evaluator decision labels: `accept`, `revise`, `reject`. After a re-evaluator returns, the orchestrator compares the sealed current and prior reports plus the revision delta; only the orchestrator may derive `stop_no_gain`.

State updates:
- set `evaluation_report_path`
- set `evaluation_id`
- set `draft_status: evaluated`

Route:
- `accept` → Step 12 (Review Panel) or Step 13 (Frontmatter)
- `revise` → Step 11 (Refinement)
- `reject` → stop
- orchestrator-derived `stop_no_gain` after sealed-report comparison → stop

#### Step 11: Targeted Refinement

When evaluation returns `revise`, call `article-refinement-controller`.

Default maximum: 2 rounds. Each round produces three files in `09_revisions/round-NNN/`:
- `revision-plan-rNNN.md`
- `response-to-reviewers-rNNN.md`
- `revision-delta-rNNN.md`

Revision modes include: textual_revision, structural_revision, evidence_relinking, reporting_completion, claim_downscaling, methods_detailing, journal_retargeting, language_polishing.

Modes `analysis_required` and `study_redesign_required` must NOT be processed — stop and inform user.

Manuscript body must NOT contain reviewer-response language.

Language polishing: explicitly delegate a fresh `academic-language-assessor` subagent → save `08_evaluations/language-assessment-vNNN.md` → drafter fixes → save `09_revisions/round-NNN/language-change-log-rNNN.md` → delegate a new assessor instance. If a changed draft is saved, create a new manuscript version with `change_type: language_only`.

After every changed manuscript version, explicitly delegate a fresh `article-evaluator` instance. Give it the latest frozen draft, stable rubric, necessary factual artifacts, and—only when must-fix verification is required—an anonymized issue list plus revision delta. Do not provide prior scores or decisions. Once the report is sealed, compare rounds at the orchestrator level and route to accept, another permitted revision, or `stop_no_gain`.

State updates:
- increment `revision_round`
- append `revision_history`
- update `draft_path`, `draft_version`, `evaluation_report_path`

#### Step 12: Mock Review Panel

Use after evaluation passes, revision reaches accept, or user explicitly requests mock review.

Default panel mode: `blind_external_simulation`.

Panel tiers: `lightweight` (3 reviewers), `standard` (5), `full` (7).

Use `article-review-panel` as the role/rubric contract, not as one large reviewer. The orchestrator directly creates one fresh independent subagent or delegated thread per selected reviewer role and dispatches all roles concurrently against the same frozen manuscript version. Reviewers cannot see evaluation reports or one another's output. Wait for every required role to finish before orchestrator aggregation; preserve dissent and conflicts verbatim. If any required role cannot run independently, return `independent_review_pending` and do not aggregate inline.

Panel aggregation rule: if methodology reviewer reports fatal flaw, `aggregated_recommendation` CANNOT exceed `not_ready`.

State updates:
- set `panel_report_path`
- set `panel_mode`, `panel_tier`

Route panel decision:
- `strong_support` → Step 13
- `support_with_minor_revision` → Step 13 (mark minor pending)
- `support_after_major_revision` → Step 11 (revision loop)
- `revise_and_resubmit` → Step 11 + re-evaluation gate
- `not_ready` → Step 8 or Step 4
- `reject_or_redesign` → stop, suggest return to study design

### Phase 5: Submission Delivery

#### Step 13: Frontmatter Drafting

Call `article-frontmatter-drafter`.

Produces: Abstract, Key Points, Title alternatives, Running title, Highlights, Graphical abstract text.

Constrained by: Blueprint contribution statement, Evaluation report, Panel report, Journal Adapter.

Must NOT modify manuscript body, introduce claims not in the manuscript, or draft the cover letter.

State updates:
- set `frontmatter_path`

#### Step 13b: Cover Letter Drafting

Call `article-cover-letter`.

Produces: cover letter, cover-letter quality check, and biomedical cover-letter-only medical journal review when applicable.

For biomedical manuscripts, after `article-cover-letter` returns, the orchestrator explicitly delegates a fresh `medical-journal-review` subagent for a cover-letter-only review and records the apparent article tier. The delegate receives only the frozen cover letter.

State updates:
- set `cover_letter_path`
- set `cover_letter_review_path` when applicable

#### Step 14: Submission Compositor

Explicitly delegate `article-submission-compositor` to a fresh independent subagent or delegated thread with frozen source artifact identities and versions.

Assembles: final manuscript, frontmatter, cover letter, figures/tables, supplementary materials, reporting checklist mapping, submission checklist, reviewer risk matrix (final), human sign-off checklist.

Performs supplementary compliance check: item count, file format, data/code availability statements.

Also performs pre-submission verification:
- reference verification
- table/figure/result consistency
- journal instruction verification
- ethics and declarations checklist

Package status: `ready_for_author_signoff` | `ready_for_author_check` | `minor_revision_pending` | `major_revision_required` | `blocked` | `partial`.

Must NOT rewrite, patch, re-score, or hide unresolved issues.

If a fresh compositor/verifier cannot be established, record `independent_review_pending`, emit a continuation brief, and stop without a ready package status.

State updates:
- set `package_path`
- set `package_status`

## Handling Evidence-Related Feedback

After evaluation or review, scan all `[evidence]` tagged revision priorities and must-fix items.

Ask whether to:
- call `research-opportunity-mapper`
- generate an external search prompt
- mark the claim as evidence-pending and continue

Evidence retrieval does not consume a revision round by itself.

## Delegation Minimum

Every independent subagent brief must include: user goal, target output, task boundary, frozen artifact IDs and required file paths/versions, relevant artifacts, scope limitations, and explicit prohibited actions.

Evaluation/review briefs must say: evaluate or review only; do not draft, revise, rewrite, or broaden scope.

Every review output must record `review_id`, `reviewer_skill`, `reviewer_instance_id`, `workflow_id`, `round_id`, `input_artifact_ids`, `input_versions`, `files_read`, `review_scope`, `isolation_mode: fresh_subagent`, `prior_scores_visible: false`, `source_edits_performed: false`, `decision`, `findings`, and `unresolved_issues`.

## Stop Conditions

Stop or route back when:
- Readiness fails (blocking gaps)
- Context builder requires clarification (blocking user facts missing)
- Methods audit finds requires_reanalysis or methodologically_blocked
- Claim auditor finds fatal overclaims
- Evaluator finds unfixable fatal flaws
- Revision produces no gain (stop_no_gain)
- Panel recommends reject_or_redesign
- Workflow state insufficient to support requested downstream action

## Pitfalls

- Do not proceed with implicit state; record skipped artifacts and limitations.
- Do not skip readiness triage even in fast-track mode.
- Do not give blind review panel members context brief, evaluation report, or unresolved issues.
- Do not route major panel revision directly to compositor.
- Do not package a changed manuscript version that has not passed the required evaluation.
- Do not let `article-submission-compositor` perform manuscript cleanup or rewrite.
- Do not write revision plans without the entry strategy classification (`enter_manuscript` / `response_only` / `decline`).
- Do not embed reviewer-response language in manuscript body.

## Verification

- Workflow state exists and contains the required fields for the selected entry mode.
- Project directory follows `references/artifact-naming-and-directory-rules.md`.
- `13_state/artifact-index.md` is current.
- Every evaluator, auditor, triage reviewer, panel role, and final compositor/verifier ran in a fresh independent subagent or delegated thread.
- Every re-evaluator has a new instance ID and `prior_scores_visible: false`; cross-round comparison occurred only after its report was sealed.
- Every required panel reviewer completed before aggregation, and dissent remains visible.
- Manuscript, supplementary, and revision version lineages are current.
- Panel mode and reviewer input policy are explicit.
- Revision records are in `09_revisions/round-NNN/`, separate from drafts.
- Package status is explicit and no unresolved issue was hidden or silently dropped.

## References

- `references/workflow-state-schema.md`: Workflow state schema and artifact registry.
- `references/artifact-naming-and-directory-rules.md`: Project directory layout, file naming, version rules, artifact index format.
- `references/artifact-contracts.md`: Canonical YAML schemas for all cross-skill artifacts.
- `references/handoff-validation.md`: Minimum validation checks at each cross-skill handoff boundary.
- `references/delegate-brief-templates.md`: Evaluator, reviewer, and auditor delegation brief templates.
- `references/delegation-rules-pattern.md`: Standard isolation and delegation pattern.
- `references/loop-control-rules.md`: Revision loop limits, targeted repair rules, and stop conditions.
- `references/evidence-confirmation-and-routing.md`: Evidence material confirmation and routing rules.
- `references/evidence-provenance-ledger-schema.md`: EPL schema, shared between architect, drafter, and claim-auditor.
