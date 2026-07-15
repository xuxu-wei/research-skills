# Handoff Validation Rules

## Contents

<!-- toc:start -->
- [Handoff Gates](#handoff-gates)
  - [Step 0 → Step 1: Orchestrator → Readiness Triage](#step-0-step-1-orchestrator-readiness-triage)
  - [Step 1 → Step 2: Readiness Triage → Context Builder](#step-1-step-2-readiness-triage-context-builder)
  - [Step 2 → Step 3: Context Builder → Literature Grounder](#step-2-step-3-context-builder-literature-grounder)
  - [Step 3 → Step 4: Literature Grounder → Architect](#step-3-step-4-literature-grounder-architect)
  - [Step 4 → Step 7: Architect → Methods Auditor](#step-4-step-7-architect-methods-auditor)
  - [Step 7 → Step 8: Methods Auditor → Drafter](#step-7-step-8-methods-auditor-drafter)
  - [Step 8 → Step 9: Drafter → Claim Auditor](#step-8-step-9-drafter-claim-auditor)
  - [Step 9 → Step 10: Claim Auditor → Evaluator](#step-9-step-10-claim-auditor-evaluator)
  - [Step 10 → Step 11: Evaluator → Refinement Controller](#step-10-step-11-evaluator-refinement-controller)
  - [Step 11 → Step 10 (Re-evaluation): Refinement Controller → Evaluator](#step-11-step-10-re-evaluation-refinement-controller-evaluator)
  - [Step 10/11 → Step 12: Evaluator → Review Panel](#step-1011-step-12-evaluator-review-panel)
  - [Step 12 → Step 13: Review Panel → Frontmatter Drafter](#step-12-step-13-review-panel-frontmatter-drafter)
  - [Step 13/13b → Step 14: Frontmatter/Cover Letter → Submission Compositor](#step-1313b-step-14-frontmattercover-letter-submission-compositor)
  - [Step 14 → Human Review: Compositor → Author](#step-14-human-review-compositor-author)
- [Fast-Track Handoff Modifications](#fast-track-handoff-modifications)
- [Failure Handling](#failure-handling)
<!-- toc:end -->

Minimum validation checks at each cross-skill handoff boundary in the research-article workflow.

## Handoff Gates

### Step 0 → Step 1: Orchestrator → Readiness Triage

- `minimal_intake_summary` is non-empty
- `study_topic` is non-empty

### Step 1 → Step 2: Readiness Triage → Context Builder

- `readiness_status ∈ {ready, conditionally_ready}`
- If `conditionally_ready`: `nonblocking_gaps` is populated

### Step 2 → Step 3: Context Builder → Literature Grounder

- `proceed_status ∈ {proceed, proceed_with_assumptions}`
- `study_design.type` is non-empty
- `research_question.primary` is non-empty

### Step 3 → Step 4: Literature Grounder → Architect

- `grounding_confidence ∈ {high, medium}`
- If `grounding_confidence = low`: orchestrator must flag in `scope_limitations`

### Step 4 → Step 7: Architect → Methods Auditor

- `article_blueprint.claim_evidence_matrix` has ≥ 1 entry
- `article_blueprint.results_skeleton.sections` is non-empty
- `article_blueprint.study_type_confirmation.type` is non-empty

### Step 7 → Step 8: Methods Auditor → Drafter

- `audit_status ∈ {pass, conditionally_pass_with_author_verification, requires_methods_clarification}`
- If `audit_status ∈ {requires_reanalysis, methodologically_blocked}`: **BLOCKED** — do not proceed

### Step 8 → Step 9: Drafter → Claim Auditor

- `manuscript_draft.sections` all have `content` non-empty
- `draft_path` is readable
- `supplementary_path` is readable only when Supplementary Index has entries, main text cites supplementary items, or journal/reporting policy requires supplementary material.
- Absence of supplementary material is acceptable when Supplementary Index is empty and no policy or main-text reference requires it.
- Fast-track backfills must have a populated Claim-Evidence Matrix and Evidence Provenance Ledger before claim audit.

### Step 9 → Step 10: Claim Auditor → Evaluator

- `claim_audit_report.recommendation ≠ blocked`
- If `fatal_overclaims` is non-empty and fixable by downscaling, removal, or relocation: route to refinement first, not evaluator.
- If fatal overclaims are unfixable because primary evidence is absent, evidence contradicts the claim, or the author rejects required downscaling: block progression.

### Step 10 → Step 11: Evaluator → Refinement Controller

- `evaluation.decision = revise`
- `evaluation.revision_priorities` is non-empty

### Step 11 → Step 10 (Re-evaluation): Refinement Controller → Evaluator

- New `draft_version` exists
- `revision-delta-rNNN.md` exists but remains sealed from the fresh evaluator
- the revised manuscript is complete, its digest is registered, and the blueprint identity anchor is preserved
- `response-to-reviewers-rNNN.md` exists
- Re-evaluation uses a new fresh independent evaluator with only the current complete manuscript/digest, current displays, necessary facts/rubric, and optional anonymous must-fix list; no prior manuscript, delta, report, score, or decision

### Step 10/11 → Step 12: Evaluator → Review Panel

- `evaluation.decision = accept`
- `evaluation.readiness_level ∈ {submission_ready, minor_revision}`
- `evaluation.isolation_mode = fresh_subagent` and `prior_scores_visible = false`; otherwise return `independent_review_pending` with a continuation brief and do not advance.

### Step 12 → Step 13: Review Panel → Frontmatter Drafter

- `panel_report.aggregated_recommendation ∈ {strong_support, support_with_minor_revision}`
- If methodology reviewer reported fatal flaw: **BLOCKED** — panel recommendation capped at `not_ready`

### Step 13/13b → Step 14: Frontmatter/Cover Letter → Submission Compositor

- All frontmatter items status = `final`
- Abstract word count within journal limit
- Cover letter exists at `11_cover-letter/cover-letter.md` unless the target journal explicitly does not require one
- Cover letter addresses the correct journal
- Biomedical cover letters have a cover-letter-only independent `medical-journal-review` output; if that required review cannot run, return `independent_review_pending` rather than reviewing inline
- Canonical Markdown/evaluation digests match; DOCX parity, required displays, and full-page render QA pass or explicitly cap status below human sign-off.
- The submission compositor/verifier has a fresh independent instance and frozen source artifact IDs, paths, and versions.

### Step 14 → Human Review: Compositor → Author

- `human_signoff_checklist` all items explicitly marked
- `unresolved_items` and `human_review_notes` documented
- `package_status` is explicit
- `ready_for_author_signoff` requires fresh independent evaluation and final compositor/verification, reference verification, result consistency verification, and verified journal requirements.
- Recoverable version mismatches cap status at `ready_for_author_check` and must be listed in human sign-off. Unresolvable version mismatches are blocked until the current artifact pointer is clarified.

## Fast-Track Handoff Modifications

For fast-track entry modes:

- Skipped artifacts must be recorded as `null` in workflow state with `scope_limitation`
- Backfilled artifacts must carry `confidence` and `source: reverse_engineered_from_draft`
- Evaluator and reviewer briefs must include the scope limitation
- If methods details, statistical output, or evidence provenance are missing, package status is capped at `ready_for_author_check`.

## Failure Handling

If a handoff gate fails:
1. Record the failure in `unresolved_issues`
2. Route back to the producing skill or orchestrator
3. Do not silently proceed with incomplete artifacts
