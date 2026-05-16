# Handoff Validation Rules

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
- `revision-delta-rNNN.md` exists
- `response-to-reviewers-rNNN.md` exists
- Re-evaluation uses fresh isolated subagent (no shared context with prior evaluation)

### Step 10/11 → Step 12: Evaluator → Review Panel

- `evaluation.decision = accept`
- `evaluation.readiness_level ∈ {submission_ready, minor_revision}`
- `evaluation.independence_status = true_isolated`; otherwise route is degraded and cannot advance beyond `ready_for_author_check`.

### Step 12 → Step 13: Review Panel → Frontmatter Drafter

- `panel_report.aggregated_recommendation ∈ {strong_support, support_with_minor_revision}`
- If methodology reviewer reported fatal flaw: **BLOCKED** — panel recommendation capped at `not_ready`

### Step 13/13b → Step 14: Frontmatter/Cover Letter → Submission Compositor

- All frontmatter items status = `final`
- Abstract word count within journal limit
- Cover letter exists at `11_cover-letter/cover-letter.md` unless the target journal explicitly does not require one
- Cover letter addresses the correct journal
- Biomedical cover letters have a cover-letter-only `medical-journal-review` output or an explicit `delegate_unavailable` limitation
- References, table/figure/result consistency, journal instructions, and ethics/declarations checks are complete or explicitly capped.

### Step 14 → Human Review: Compositor → Author

- `human_signoff_checklist` all items explicitly marked
- `unresolved_items` and `human_review_notes` documented
- `package_status` is explicit
- `ready_for_author_signoff` requires true isolated evaluation, reference verification, result consistency verification, and verified journal requirements.
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
