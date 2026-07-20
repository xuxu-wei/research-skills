---
name: article-submission-compositor
description: "Independently verify and assemble a frozen article and qualifying reviews into a package for human sign-off."
---
# article-submission-compositor

## Role

Assemble frozen manuscript, frontmatter, cover letter, figures/tables, supplements, checklists, and review findings into a human-review package. Verify consistency and declared journal requirements. Do not author or repair source content.

## Independent Execution Contract

- Run only in a fresh independent subagent or delegated thread, never in generator, drafter, revision, evaluator, or orchestrator context.
- Require frozen artifact IDs, paths, and versions. Treat every source artifact as read-only.
- Write only faithful package copies (including DOCX), manifest/index, parity/render verification, risk matrix, and human sign-off checklist under `12_package/**`.
- Do not edit, draft, rewrite, polish, repair, fix, re-score, or hide findings in any source artifact.
- Read reviewer outputs only as declared frozen inputs needed to preserve findings; do not reinterpret dissent into consensus.
- Report exact files read, review scope, limitations, and reviewer instance ID.
- If independent execution is unavailable, return `independent_review_pending` with a self-contained continuation brief and stop; never assemble inline or emit a ready status.

## Allowed Inputs and Writes

Read only declared frozen files from `06_drafts/**`, `11_frontmatter/**`, `11_cover-letter/**`, `04_blueprint/**`, `08_evaluations/**`, `07_claim-audit/**`, `05_audit/**`, `10_panel/**`, and `09_revisions/**`. Write only `12_package/**`. DOCX-capable document tooling may perform faithful formatting and render QA; do not call content drafters, architects, evaluators, or reviewers.

## Procedure

1. **Validate provenance.** Confirm the latest manuscript/frontmatter artifact IDs, versions, and paths match the latest qualifying evaluation and the state/index current pointers. Verify complete index membership and uniqueness. Treat unresolvable mismatches as blocking; recoverable mismatches cap status at `ready_for_author_check`.
2. **Inventory artifacts.** Record artifact ID, type, path, version, and `present | missing | incomplete` in the package manifest.
3. **Assemble copies.** Bind the complete canonical Markdown artifact identity. When document tooling is available, generate the primary user-facing DOCX, embed native tables and available figures from the display manifest, and never alter source wording or data.
4. **Map reporting checklist.** Record standard item, manuscript location, and `addressed | partially_addressed | not_addressed | not_applicable`.
5. **Verify package parity.** Compare normalized DOCX headings, body, table cells, and captions with the frozen Markdown/manifest; verify display numbering, callouts, supplements, and result consistency.
6. **Render DOCX.** Render every page to PNG, inspect at 100%, fix formatting-only defects, and re-render. Content drift routes back to faithful composition; required missing assets or unavailable render QA cap status below human sign-off.
7. **Preserve review risk.** Carry forward blueprint risks, audits, evaluation, panel reports, conflicts, dissent, fatal findings, and unresolved issues with stable source references.
   Preserve any `publication_probability_assessment` in the frozen `medical-journal-review` report unchanged; never calculate, reinterpret, or adjust it.
8. **Create human sign-off.** Leave author data/statistics/contribution/declaration/reference/journal/figure confirmations pending; never infer a signature or external submission.
9. **Assign state/status.** Map unavailable review to `independent_review_pending`, DOCX absence to `docx_generation_pending`, unavailable render to `docx_visual_qa_pending`, fatal/blocking findings to `blocked`, and only a synchronized/rendered unchanged package to `human_signoff_required`.

## Review Provenance

Include this block in `submission-readiness-summary.md`:

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
canonical_artifact_ref:
  artifact_id:
  version:
  path:
docx_artifact_ref:
  artifact_id:
  version:
  path:
docx_sync_status: synchronized | content_drift | not_generated
render_qa_status: passed | docx_visual_qa_pending | failed | not_generated
decision:
findings: []
unresolved_issues: []
```

## Blocking Findings and Dissent

The human sign-off checklist must contain:

```yaml
reviewer_dissent_items:
  - dissent_id:
    panel_report_ref:
    severity: fatal | major | minor | informational
    blocking: true | false
    disposition: pending_author_decision | accepted_risk | resolved
    author_acknowledgement: pending
fatal_finding_items:
  - finding_id:
    source_review_ref:
    reviewer_instance_id:
    blocking: true
    disposition: pending_author_decision | routed_to_revision | resolved
    author_acknowledgement: pending
```

Any unresolved blocking dissent or fatal finding caps package status at `blocked`. A resolved fatal finding can proceed only after a fresh independent evaluator confirms the repaired manuscript version. Pending author acknowledgement can never represent signed approval or submission.

## Status Caps

- Missing or partial required artifacts -> `partial` or `blocked`.
- Missing required display assets, DOCX generation, content parity, or render QA -> `docx_generation_pending`, `docx_visual_qa_pending`, or `blocked`; never `human_signoff_required`.
- Unverified journal requirements, references, or result consistency -> at most `ready_for_author_check`.
- Minor/major unresolved revisions -> corresponding pending/required status.
- All gates passed, current/evaluated versions equal, and instructions verified -> `human_signoff_required` with subordinate `ready_for_author_signoff`.
- A package never represents external submission.

## Outputs

Write the verified `manuscript-vNNN.docx`, `submission-package.md`, `package-manifest.md`, `docx-parity-and-render-report.md`, `reporting-checklist-mapping.md`, `submission-readiness-summary.md`, `reviewer-risk-matrix.md`, and `human-signoff-checklist.md` under `12_package/`.

## Conditional Resources

- Read `references/package-assembly-guide.md` when ordering or formatting package components.
- Read `references/reporting-checklist-integration.md` when mapping reporting-standard items.
- Read `references/supplementary-compliance-guide.md` when supplementary items exist or are required.
- Read `article-orchestrator/references/artifact-review-and-submission-contracts.md` for package and sign-off schemas.
- Read `article-orchestrator/references/artifact-naming-and-directory-rules.md` when validating paths and versions.
- Read `article-orchestrator/references/article-docx-delivery-contract.md` whenever generating, synchronizing, or verifying DOCX and display assets.

## Completion Check

Confirm canonical/evaluated logical identity and index-pointer equality, DOCX semantic parity/render pass, display assets, manifest completeness, unchanged carried probability when present, visible dissent/fatal findings, justified caps, unchanged sources, and a final state that still requires human review.
