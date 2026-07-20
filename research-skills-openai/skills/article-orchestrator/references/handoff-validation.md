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
  - [Step 9 → Step 10: Claim Auditor → Frontmatter and Editorial Readiness](#step-9-step-10-claim-auditor-frontmatter-and-editorial-readiness)
  - [Step 10 → Step 11: Editorial Readiness → Refinement Controller](#step-10-step-11-editorial-readiness-refinement-controller)
  - [Step 11 → Step 12: Editorial Repair → Final Evaluator](#step-11-step-12-editorial-repair-final-evaluator)
  - [Step 12 → Step 13: Evaluator → Review Panel](#step-12-step-13-evaluator-review-panel)
  - [Step 13 → Step 14: Review Panel → Outlet Review and Delivery](#step-13-step-14-review-panel-outlet-review-and-delivery)
  - [Step 14 → Step 15: Frontmatter/Cover Letter → Submission Compositor](#step-14-step-15-frontmattercover-letter-submission-compositor)
  - [Step 15 → Human Review: Compositor → Author](#step-15-human-review-compositor-author)
- [Fast-Track Handoff Modifications](#fast-track-handoff-modifications)
- [Failure Handling](#failure-handling)
<!-- toc:end -->

Minimum validation checks at each cross-skill handoff boundary in the research-article workflow.

## Handoff Gates

### Step 0 → Step 1: Orchestrator → Readiness Triage

- `minimal_intake_summary` is non-empty
- `study_topic` is non-empty
- every supplied readiness-relevant file appears in `complete_material_inventory`
- any sole semantic authority states what conflicts it governs and retains compatible result/display/reporting assets

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
- `article_blueprint.section_content_plan` covers every reader-facing section and declares reader handoffs
- authoritative locations for analytical assumptions and the complete limitations account are explicit
- `article_blueprint.study_type_confirmation.type` is non-empty

### Step 7 → Step 8: Methods Auditor → Drafter

- `audit_status ∈ {pass, conditionally_pass_with_author_verification}`
- A conditional pass contains a specific bounded working assumption, falsifier, consequence if false, later verification, and one authoritative Assumptions location.
- `requires_methods_clarification` returns for clarification before drafting; it is not a conditional pass.
- If `audit_status ∈ {requires_reanalysis, methodologically_blocked}`: **BLOCKED** — do not proceed

### Step 8 → Step 9: Drafter → Claim Auditor

- `manuscript_draft.sections` all have `content` non-empty
- `draft_path` is readable
- `supplementary_path` is readable only when Supplementary Index has entries, main text cites supplementary items, or journal/reporting policy requires supplementary material.
- Absence of supplementary material is acceptable when Supplementary Index is empty and no policy or main-text reference requires it.
- Fast-track backfills must have a populated Claim-Evidence Matrix and Evidence Provenance Ledger before claim audit.

### Step 9 → Step 10: Claim Auditor → Frontmatter and Editorial Readiness

- `claim_audit_report.recommendation ≠ blocked`
- If `fatal_overclaims` is non-empty and fixable by downscaling, removal, or relocation: route to refinement first, not evaluator.
- If fatal overclaims are unfixable because primary evidence is absent, evidence contradicts the claim, or the author rejects required downscaling: block progression.
- a complete versioned provisional frontmatter bundle is frozen and agrees with the current manuscript
- `protected-content-register.yaml` binds the current manuscript/frontmatter and includes identity, claims/strength, evidence state, critical assumptions/limitations, source intent, binding constraints, and prohibited claim upgrades

### Step 10 → Step 11: Editorial Readiness → Refinement Controller

- fresh narrative and language reviewers assessed the same frozen reader bundle in parallel
- raw reports are sealed from writers and the final evaluator
- every critical/major included finding maps to at least one executable action in one validated `editorial-repair-brief-rNNN.yaml`
- the brief identifies owner, exact locator, operation, required function/content, verified term replacement when applicable, preservation/removal/move instructions, dependencies, and acceptance test

### Step 11 → Step 12: Editorial Repair → Final Evaluator

- New `draft_version` exists
- New complete `frontmatter_version` exists when frontmatter changed
- `revision-delta-rNNN.md` exists but remains sealed from the fresh evaluator
- action conformance passed; missing major actions return to the same writer before freeze
- content preservation decision is `scientific_content_preserved`
- fresh narrative/language reassessment has no unresolved major finding
- the revised bundle is complete, its logical identities and unique current pointers are registered, and the identity anchor is preserved
- the final evaluator receives only the current manuscript, frontmatter, referenced displays, stable rubric, and minimal factual/outlet constraints; no prior manuscript, blueprint/plan, assessment, repair brief, protected register, delta, audit, report, score, or decision

### Step 12 → Step 13: Evaluator → Review Panel

- `evaluation.decision = accept`
- `evaluation.readiness_level ∈ {submission_ready, minor_revision}`
- `evaluation.isolation_mode = fresh_subagent` and `prior_scores_visible = false`; otherwise return `independent_review_pending` with a continuation brief and do not advance.

### Step 13 → Step 14: Review Panel → Outlet Review and Delivery

- `panel_report.aggregated_recommendation ∈ {strong_support, support_with_minor_revision}`
- If methodology reviewer reported fatal flaw: **BLOCKED** — panel recommendation capped at `not_ready`
- any panel-requested prose change creates a new artifact version and returns through preservation, fresh editorial readiness, and fresh final evaluation
- journal candidates are based on verified current scope facts and the final artifact; fresh `medical-journal-review` receives no evaluator scores or findings

### Step 14 → Step 15: Frontmatter/Cover Letter → Submission Compositor

- All frontmatter items status = `final`
- Abstract word count within journal limit
- A current versioned Cover Letter and matching mechanical check exist under `11_cover-letter/` unless the target journal explicitly does not require one
- Cover letter addresses the correct journal
- When biomedical review applies or probability was requested, the current Cover Letter has one fresh `medical-journal-review` report; any probability block stays inside that report and cannot override blocking gates
- Canonical Markdown/frontmatter artifact IDs, versions, paths, index membership, and current pointers match the evaluation; DOCX semantic parity, required displays, and full-page render QA pass or explicitly cap status below human sign-off.
- The submission compositor/verifier has a fresh independent instance and frozen source artifact IDs, paths, and versions.

### Step 15 → Human Review: Compositor → Author

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
