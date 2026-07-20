---
name: article-architect
description: "Plan reader-facing manuscript sections, handoffs, claims, evidence, and displays."
---
# article-architect

## Role

Design the frozen scientific and reader-facing architecture that constrains article drafting and downstream audits. Do not draft prose, retrieve literature, audit methods, or evaluate manuscript quality.

## Inputs and Writes

Read approved readiness, context, literature-grounding, and result artifacts. Write only `04_blueprint/article-blueprint.md`; do not read or write drafts, evaluations, or claim-audit reports.

## Procedure

1. Define one contribution statement: known baseline, study addition, contribution type/strength, and concise takeaway.
2. Confirm study type and freeze an identity anchor: central question, primary contribution, main answer, study object, core evidence basis, source-intent coverage, and binding constraints.
3. Build a claim-evidence matrix with claim ID/type, section, evidence IDs, inference type, target wording strength, and overclaim risk.
4. Seed the evidence provenance ledger with evidence ID/type, mapped claims, source, verification status, risk, and notes; never invent evidence.
5. Select and justify one Results organization mode: norm-, argument-, hybrid-, artifact-, theory-, or evidence-synthesis-driven.
6. Build an evidence-display plan and `04_blueprint/display-asset-manifest.yaml` with stable IDs, source paths and versions, captions, callouts, placement, availability, and main/supplement status.
7. Build the supplementary index with stable IDs, content, claim/display links, main-text cross-reference, reporting/journal requirements, limits, format, and availability policies.
8. Build a full section-content plan before any prose is written. For title/abstract, Introduction, Methods, Results, and Discussion, state the section's rhetorical function, reader question answered, required content, prior-knowledge assumption, definition order, handoff to the next section, and content that belongs elsewhere. The Introduction must support background -> current state -> gap -> significance -> rationale/objective; Results must lead with the primary answer; Discussion must answer the question before qualification.
9. Build the paragraph-level Results skeleton with claims, display items, key numbers, and transitions.
10. Select the single authoritative location for each analytical assumption and for the article's complete limitations account. Other sections omit those limitations unless one is necessary to advance the immediate reasoning and omission would distort it; never insert navigation pointers in their place.
11. Record a journal adapter with verified or explicitly unverified article type, word/abstract/display/reference limits, structural requirements, and supplementary policy.
12. Record a reviewer-risk preview with concern, severity, section/claim, and possible pre-emptive action; do not convert it into a score or let defensive review language displace the article's positive argument.

## Output Contract

```yaml
article_blueprint:
  contribution_statement: {}
  study_type_confirmation: {}
  core_qa: {}
  manuscript_identity_anchor: {}
  claim_evidence_matrix: []
  evidence_provenance_ledger: {}
  evidence_display_plan: {}
  display_asset_manifest_ref: "04_blueprint/display-asset-manifest.yaml"
  supplementary_index: {}
  reader_profile: {}
  section_content_plan: []
  authoritative_content_locations: []
  results_skeleton: []
  journal_adapter: {}
  reviewer_risk_preview: []
  unresolved_issues: []
```

Return only a concise phase summary and the blueprint artifact pointer.

## Conditional Resources

- Read `references/results-organization-modes.md` when selecting and justifying the Results organization mode.
- Read `references/claim-taxonomy.md` when classifying claims, inference types, or wording strength.
- Read `article-orchestrator/references/artifact-contracts.md` when validating blueprint, display, ledger, or supplementary schemas.
- Read `article-orchestrator/references/evidence-provenance-ledger-schema.md` when seeding ledger granularity and fields.
- Read `article-orchestrator/references/artifact-naming-and-directory-rules.md` when assigning paths and versions.
- Read `article-orchestrator/references/handoff-validation.md` before handing the blueprint to the drafter or auditor.
- Read `article-orchestrator/references/article-docx-delivery-contract.md` when defining display assets for a DOCX-capable workflow.

## Completion Check

Confirm every claim maps to evidence, every display has a carrier/location, every supplementary item has cross-references, the full section plan supports the declared reader reasoning chain, terms appear after the concepts they name, the Results mode is justified, authoritative assumption/limitation locations are unambiguous, journal constraints show verification status, risks are specific, and no quality verdict or prose draft was produced.
