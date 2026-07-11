---
name: article-submission-compositor
description: "Assemble the final submission package: manuscript, frontmatter, cover letter, figures/tables, supplementary materials, reporting checklist mapping, reviewer risk matrix, and human sign-off checklist. Verify supplementary compliance with journal limits."
---
# article-submission-compositor

## Purpose

Assemble the final submission package from all artifacts produced by upstream skills. Verify supplementary compliance with journal limits, check format consistency, and produce the human sign-off checklist. This is the gate before author submission.

This skill does NOT rewrite, polish, patch, re-score, hide unresolved issues, or create new content. It assembles existing artifacts and verifies they meet journal requirements.

## Core Rules

- Assemble only. Do not clean, rewrite, or improve.
- Every unresolved issue from upstream must be listed in the sign-off checklist — never silently dropped.
- Package status can never exceed `ready_for_author_signoff`. The author is the final gate.
- If journal requirements were not independently verified, the package cannot exceed `ready_for_author_check`.
- Supplementary compliance must be explicitly checked: item count, format, cross-references, data/code availability.
- Manuscript body, supplementary materials, and frontmatter versions must be consistent.
- `ready_for_author_signoff` requires a true isolated evaluation, verified references, table/figure/result consistency, verified journal instructions, and complete ethics/declarations checks.

## Independent Execution Contract

- Run only in a fresh independent subagent or delegated thread. Never perform final verification in the generator, drafter, revision, evaluator, or orchestrator context.
- Receive frozen artifact IDs, file paths, and versions. Treat every source artifact as read-only.
- Write only package copies, the package manifest/index, verification reports, and the human sign-off checklist. Do not edit, rewrite, polish, or fix any source artifact.
- Do not access parent hidden reasoning or expected answers. Read reviewer outputs only as frozen, declared inputs needed to verify and preserve their findings; never reinterpret them to hide dissent.
- Report `files_read` and `review_scope` in the verification report, together with the standard review identity and isolation fields.
- If a fresh independent subagent or delegated thread cannot be established, return `independent_review_pending` plus a self-contained continuation brief and stop. Never verify or assemble inline, and never emit a ready status.

```yaml
review_id:
reviewer_skill: article-submission-compositor
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

## I/O Contract

```yaml
io_contract:
  allowed_inputs:
    - manuscript_draft (final version)
    - supplementary_materials (final version)
    - frontmatter (abstract, key points, titles, highlights)
    - cover_letter
    - cover_letter_quality_check
    - medical_cover_letter_review (for biomedical manuscripts)
    - article_blueprint (EDP, supplementary_index, journal_adapter, reviewer_risk_preview)
    - evaluation_report (latest)
    - claim_audit_report
    - methods_audit_report
    - panel_report (if available)
    - revision_history (if applicable)
  required_outputs:
    - submission_package
    - human_signoff_checklist
  may_read:
    - "06_drafts/**"
    - "11_frontmatter/**"
    - "11_cover-letter/**"
    - "04_blueprint/**"
    - "08_evaluations/**"
    - "07_claim-audit/**"
    - "05_audit/**"
    - "10_panel/**"
    - "09_revisions/**"
  may_write:
    - "12_package/**"
  must_not_read: []
  must_not_write:
    - "06_drafts/**"
    - "04_blueprint/**"
    - "11_frontmatter/**"
    - "11_cover-letter/**"
  may_call: []
  must_not_call:
    - article-drafter
    - article-evaluator
    - article-architect
  failure_modes:
    - "artifact version mismatch → flag in sign-off checklist, use latest versions, record discrepancy"
    - "supplementary item missing → list in sign-off checklist, do not fabricate"
    - "journal requirements not fully verifiable → cap status at ready_for_author_check"
    - "independent evaluation or fresh compositor subagent unavailable → return independent_review_pending and stop; do not emit a ready status"
    - "reference or result consistency verification incomplete → cap status at ready_for_author_check or blocked"
  escalation_route: "article-orchestrator"
```

Version mismatch handling:
- Recoverable mismatch: use the `13_state/workflow-state.yaml` current pointer, cap status at `ready_for_author_check`, and record the discrepancy in human sign-off.
- Unresolvable mismatch: block until the current artifact pointer is clarified.

## Procedure

### Step 1: Collect and Verify Artifacts

Confirm all required artifacts exist and are the correct versions. Check version consistency across manuscript, supplementary, frontmatter, and cover letter.

Record the package manifest:

```yaml
package_manifest:
  package_version: "1"
  artifacts:
    - artifact_id: ""
      type: manuscript | supplementary | abstract | key_points | title_options | cover_letter | figures | tables | reporting_checklist | data_availability_statement | code_availability_statement | reviewer_risk_matrix | human_signoff_checklist
      path: ""
      version: ""
      status: present | missing | incomplete
```

Record final-verification isolation metadata in `submission-readiness-summary.md`:

```yaml
review_id:
reviewer_skill: article-submission-compositor
reviewer_instance_id:
workflow_id:
round_id:
input_artifact_ids: []
input_versions: []
files_read: []
review_scope: []
isolation_mode: fresh_subagent
prior_scores_visible: false
source_edits_performed: false
decision:
findings: []
unresolved_issues: []
```

### Step 2: Assemble Manuscript Package

Combine manuscript body, frontmatter, and cover letter into the journal's required format:
- Title page (title, authors, affiliations, corresponding author, word count)
- Abstract + Key Points
- Manuscript body
- References
- Tables (if embedded)
- Figures (if embedded)
- Supplementary materials reference
- Cover letter as a separate submission artifact, not embedded in the manuscript body unless the journal explicitly requires it

### Step 3: Reporting Checklist Mapping

Map manuscript content to the reporting standard items:

```yaml
reporting_checklist_mapping:
  standard: ""
  items:
    - item_id: ""
      description: ""
      manuscript_location: ""
      status: addressed | partially_addressed | not_addressed | not_applicable
  completion_rate: 0.0
```

### Step 4: Pre-Submission Verification

Run four verification checks before final status assignment:

```yaml
pre_submission_verification:
  reference_verification:
    status: pass | partial | fail | not_checked
    unverified_references: []
    metadata_mismatches: []
  table_figure_result_consistency:
    status: pass | partial | fail | not_checked
    mismatches: []
  journal_instruction_verification:
    status: verified | user_supplied_only | not_checked
    checked_date: ""
    unresolved_requirements: []
  ethics_declarations:
    status: complete | incomplete | not_applicable
    missing_items: []
```

### Step 5: Supplementary Compliance Check

```yaml
supplementary_compliance:
  supplementary_required: true | false
  requirement_source: supplementary_index | main_text_reference | reporting_guideline | journal_policy | not_required
  item_count_within_limit: true | false
  file_format_matches_journal_spec: true | false
  data_availability_statement_present: true | false
  code_availability_statement_present: true | false
  supplementary_references_included_in_main_reference_list: true | false | not_applicable
  supplementary_content_cross_referenced_from_main_text: true | false
  missing_items: []
  over_limit_items: []
```

Missing supplementary material blocks only when `supplementary_required: true`. If no supplementary item is planned, cited, or required by journal/reporting policy, absence of a supplementary file is valid.

### Step 6: Final Reviewer Risk Matrix

Compile the reviewer risk matrix from the blueprint's reviewer risk preview, updated with evaluation and panel findings:

```yaml
reviewer_risk_matrix:
  - risk_id: "R001"
    concern: ""
    severity: likely_fatal | major_concern | minor_concern | stylistic
    status: addressed | partially_addressed | not_addressed | accepted_risk
    manuscript_location: ""
    response_prepared: true | false
```

### Step 7: Human Sign-Off Checklist

```yaml
human_signoff_required:
  data_accuracy: pending                  # author must confirm
  statistical_results_verified: pending
  author_contributions_verified: pending
  ethics_and_consent_verified: pending
  conflicts_of_interest_verified: pending
  journal_requirements_verified: pending
  figure_quality_verified: pending
  reference_accuracy_verified: pending
  corresponding_author_confirmed: pending
  unresolved_issues_acknowledged: pending
  reviewer_dissent_items:
    - dissent_id: ""
      panel_report_ref: ""
      severity: fatal | major | minor | informational
      blocking: true | false
      disposition: pending_author_decision | accepted_risk | resolved
      author_acknowledgement: pending
  fatal_finding_items:
    - finding_id: ""
      source_review_ref: ""
      reviewer_instance_id: ""
      blocking: true
      disposition: pending_author_decision | routed_to_revision | resolved
      author_acknowledgement: pending
```

Every panel dissent item must appear in `reviewer_dissent_items` and every fatal finding from any audit, evaluation, or panel report must appear in `fatal_finding_items`, each with a stable ID, source reference, disposition, and author acknowledgement. Any unresolved blocking dissent or fatal finding caps package status at `blocked`; neither may be reduced to the generic acknowledgement field.

Any dissent or fatal item with `author_acknowledgement: pending` prevents any state beyond `ready_for_author_signoff`. A resolved fatal item may reach that human-review state only after fresh independent re-evaluation confirms the repair; it is never treated as author-signed or externally submitted. This workflow defines no automatic post-signoff or submission state.

### Step 8: Determine Package Status

```yaml
package_status:
  ready_for_author_signoff           # all verifiable gates passed + journal requirements verified
  ready_for_author_check             # all verifiable gates passed, but journal requirements unverified
  minor_revision_pending             # minor issues remain
  major_revision_required            # major issues remain, revision limit reached
  blocked                            # blocking issue unresolved
  partial                            # material incomplete
```

## Output

Write to `12_package/`:
- `submission-package.md`: The assembled manuscript with all components
- `reporting-checklist-mapping.md`: Reporting standard item mapping
- `submission-readiness-summary.md`: Verification status and status caps
- `reviewer-risk-matrix.md`: Final risk matrix
- `human-signoff-checklist.md`: Sign-off items for author confirmation

## Pitfalls

- Do not rewrite, polish, or improve manuscript text during assembly.
- Do not hide unresolved issues. The sign-off checklist is an honesty document.
- Do not mark `ready_for_author_signoff` if journal requirements are unverified.
- Do not proceed with version-mismatched artifacts without flagging.
- Do not fabricate missing supplementary items.
- The compositor is the assembler, not the author. Final responsibility stays with the human.

## Verification

- All artifacts in manifest present or explicitly marked as missing
- Version consistency across manuscript, supplementary, frontmatter, and cover letter
- Reporting checklist mapping complete with locations
- Supplementary compliance checked for all six items
- Reviewer risk matrix updated with final status
- Every human sign-off item listed, none skipped
- Package status does not exceed justified level
- No unreported unresolved issues

## References

- `references/package-assembly-guide.md`: Journal-specific assembly rules, file format requirements, and component ordering.
- `references/reporting-checklist-integration.md`: How to map manuscript content to reporting standard items.
- `references/supplementary-compliance-guide.md`: Journal-specific supplementary limits and format requirements.
- `article-orchestrator/references/artifact-contracts.md`: Canonical submission package and sign-off checklist schemas.
- `article-orchestrator/references/artifact-naming-and-directory-rules.md`: Directory, naming, and version rules.
