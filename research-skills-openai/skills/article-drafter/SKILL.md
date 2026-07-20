---
name: article-drafter
description: "Draft or revise one complete manuscript from an approved content plan or YAML repair brief while preserving science."
---
# article-drafter

## Role

Draft or revise the complete manuscript body and supplements from an approved
blueprint. Do not design architecture, retrieve evidence, audit claims, score
quality, or write frontmatter.

## Invariants

- Draft Methods -> Results -> Introduction -> Discussion and follow the selected
  Results organization mode.
- Trace every claim and display callout to the claim-evidence matrix, evidence
  provenance ledger, and display manifest. Do not invent claims, data, tables,
  figures, or citations.
- Every saved Markdown version is complete and independently readable. Keep
  revision plans, responses, and deltas separate; never save changed sections as
  the current manuscript.
- In revision mode, apply only the approved plan. A saved substantive or
  language change creates a new version and requires fresh evaluation.
- Keep reviewer-response language out of manuscript prose.
- Use one complete, authoritative limitations account in the location frozen by
  the blueprint. Omit those limitations everywhere else unless one directly
  advances the immediate reasoning and omitting it would distort that reasoning;
  do not replace omitted repetition with a pointer.
- Explain the research problem and primary answer before introducing technical
  machinery, thresholds, failure branches, or internal project vocabulary.

## I/O Contract

Read approved `02_context/**`, `03_literature/**`, `04_blueprint/**`,
`05_audit/**`, and exactly one assigned revision plan or
`editorial-repair-brief-rNNN.yaml`. In editorial repair mode, also read the
current complete manuscript and `protected-content-register.yaml`; do not read
the raw narrative/language reports that produced the brief. Write only versioned
canonical Markdown/supplements and, when DOCX-capable document tooling is
available and a user-facing draft is requested, the synchronized same-version
DOCX under `06_drafts/**`. Do not read evaluations, claim audits, or panel
reports and do not write their directories.

## Procedure

1. Validate the blueprint, full section-content plan, context, grounding,
   methods audit, identity anchor, display assets, supplement index, and optional
   revision plan or editorial brief.
2. Draft Methods with design, setting/sample, exposure/intervention, outcomes,
   variables, and statistical methods actually supported by the sources.
3. Draft Results in skeleton order. Map each paragraph to its claim/evidence and
   display; report estimates and uncertainty without interpretation.
4. Draft Introduction as background -> current state -> unresolved gap -> why it
   matters -> study rationale/objective using grounded citations and the declared
   reader baseline.
5. Draft Discussion around the contribution and primary answer: answer first,
   literature context, implications/generalizability, one authoritative complete
   limitations account, and conclusion.
6. Draft each indexed supplement as an independently readable artifact with
   consistent captions, numbering, and main-text cross-references.
7. In revision mode, execute every included action at its locator and output a
   complete next Markdown version. For a long artifact, the same writer may make
   bounded section passes, but it must retain the complete source and protected
   content, perform a final whole-document concordance pass, and never emit
   fragments as the current artifact. Return an action-conformance table; leave
   the controller to maintain the separate response and delta.
8. For a user-facing DOCX, use available document tooling to create a faithful
   same-version transform with native tables and embedded available figures;
   bind the display manifest and return parity/render status without changing
   scientific content.

## Outputs and Stops

- `06_drafts/manuscript-vNNN.md`: canonical complete IMRaD content.
- `06_drafts/supplementary-vNNN.md`: matched supplement when applicable.
- `06_drafts/manuscript-vNNN.docx`: primary user-facing draft when tooling is
  available and requested by the workflow.
- Stop for missing blueprint/results/method facts or required source assets;
  mark unknowns rather than fabricate. Return `docx_generation_pending` when
  only document generation is unavailable.

## Conditional Resources

- Read `references/section-templates.md` for the declared study type.
- Read `references/writing-style-guide.md` for language/section conventions.
- Read `references/supplementary-materials-guide.md` when supplements exist.
- Read `article-orchestrator/references/artifact-contracts.md` for draft schemas.
- Read `article-orchestrator/references/artifact-naming-and-directory-rules.md` for paths and versions.
- Read `article-orchestrator/references/evidence-provenance-ledger-schema.md` for claim/evidence linkage.
- Read `article-orchestrator/references/article-docx-delivery-contract.md` only for DOCX or display-asset work.

## Completion Check

Confirm complete IMRaD sections, preserved identity, supported claims, Results
order, section-function handoffs, single-location limitation policy,
display/supplement consistency, every brief action executed or explicitly
blocked, versioned lineage, no reviewer prose, and DOCX parity/render routing
when applicable.
