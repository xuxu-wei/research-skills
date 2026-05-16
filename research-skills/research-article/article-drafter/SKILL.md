---
name: article-drafter
description: Draft manuscript body text from the article blueprint, context brief, literature grounding report, and methods audit report. Follow study-type-specific templates and Results organization mode. Also organize supplementary materials per the Supplementary Index. In revision mode, apply targeted revisions.
version: 0.1.0
author: Xuxu Wei
license: MIT
metadata:
  hermes:
    tags: [research-article, drafting, manuscript, writing, supplementary]
    related_skills:
      - article-orchestrator
      - article-architect
      - article-context-builder
      - article-literature-grounder
      - article-refinement-controller
      - academic-language-assessor
---

# article-drafter

## Purpose

Draft the manuscript body text (Methods, Results, Introduction, Discussion) from the article blueprint. Organize supplementary materials per the Supplementary Index. In revision mode, apply targeted revisions specified by the refinement controller.

This skill does NOT design architecture, audit claims, evaluate quality, or write frontmatter. It writes what the blueprint specifies.

## Core Rules

- Draft in order: Methods → Results → Introduction → Discussion.
- Methods first anchors the draft in what was actually done.
- Follow the Results organization mode from the blueprint. Do not override it.
- Every claim in the manuscript must trace to the claim-evidence matrix.
- Every display item reference must trace to the EDP.
- Supplementary materials must follow the Supplementary Index; each item must be independently readable.
- Do not introduce new claims not in the blueprint.
- In revision mode, only apply changes specified in the revision plan. Do not freelance.
- In language polishing mode, fix language without changing substance. Log every change.
- The manuscript body must NOT contain reviewer-response language (e.g., "As suggested by the reviewer...").

## I/O Contract

```yaml
io_contract:
  allowed_inputs:
    - article_blueprint
    - article_context_brief
    - literature_grounding_report
    - methods_audit_report
    - revision_plan (in revision mode)
  required_outputs:
    - manuscript_draft (versioned)
    - supplementary_materials_draft (versioned, if applicable)
  may_read:
    - "04_blueprint/**"
    - "02_context/**"
    - "03_literature/**"
    - "05_audit/**"
    - "09_revisions/**"
  may_write:
    - "06_drafts/manuscript-v*.md"
    - "06_drafts/supplementary-v*.md"
  must_not_read:
    - "08_evaluations/**"
    - "07_claim-audit/**"
    - "10_panel/**"
  must_not_write:
    - "08_evaluations/**"
    - "07_claim-audit/**"
    - "04_blueprint/**"
  may_call:
    - academic-language-assessor
  must_not_call:
    - article-evaluator
    - article-claim-auditor
  failure_modes:
    - "blueprint missing results_skeleton → request architect rework via orchestrator"
    - "context_brief missing key variable definitions → flag in draft notes, do not fabricate"
    - "supplementary_index incomplete → flag missing items, draft what is planned"
  escalation_route: "article-orchestrator"
```

## Procedure

### Step 1: Load and Verify Inputs

Confirm all required inputs are present and internally consistent. Flag any gaps before drafting begins.

### Step 2: Draft Methods

Draft the Methods section following the study-type-specific template:

- Study design statement
- Setting and participants
- Interventions / exposures
- Outcomes (primary, secondary)
- Statistical methods
- Ethics statement

Refer to `references/section-templates.md` for study-type-specific Methods templates.

### Step 3: Draft Results

Draft Results following the `results_skeleton` from the blueprint:

- Each paragraph maps to one `results_skeleton` entry
- Each display item is referenced at the correct location
- Effect estimates include CIs; p-values are reported precisely (not "p < 0.05" alone)
- No interpretation in Results (interpretation belongs in Discussion)

### Step 4: Draft Introduction

Draft Introduction using the context brief and literature grounding:

- Known → Gap → This study (3-paragraph structure default)
- Ground all claims in literature references from the grounding report
- End with the study objective, not a summary of results

### Step 5: Draft Discussion

Draft Discussion using the contribution statement as anchor:

- Principal findings (mirror primary endpoint)
- Strengths and limitations (draw from reviewer risk preview and methods audit)
- Interpretation in context of existing literature
- Implications and generalizability
- Conclusion paragraph

### Step 6: Organize Supplementary Materials

For each item in the Supplementary Index:

1. Draft content following the item type template
2. Ensure cross-references from the main text are consistent
3. Supplementary methods must be independently readable
4. Supplementary figure/table captions follow main-text format
5. Do not introduce new core claims in supplementary materials

### Step 7: Language Preflight (Optional)

Optionally call `academic-language-assessor` for a pre-delivery language check. Address critical/major issues before handoff.

### Revision Mode

When a revision plan is provided:
1. Apply only the changes specified in the revision plan
2. Track all changes in the revision delta
3. In language polishing mode: fix language, log every change, do not change substance
4. Output new manuscript version with incremented version number

## Output

- `06_drafts/manuscript-vNNN.md`: The manuscript body (Introduction, Methods, Results, Discussion)
- `06_drafts/supplementary-vNNN.md`: Supplementary materials (if applicable)
- Version number matches across both files

## Study-Type-Aware Drafting

The `references/section-templates.md` provides study-type-specific templates for: RCT, observational cohort, case-control, cross-sectional, diagnostic accuracy, prediction model, systematic review, mechanistic experimental, qualitative, mixed methods, AI/ML.

## Pitfalls

- Do not draft Introduction first. Methods → Results → Introduction → Discussion.
- Do not add interpretation to Results. Interpretation lives in Discussion.
- Do not introduce display items not in the EDP.
- Do not omit supplementary materials that the Supplementary Index requires.
- In revision mode, do not make unrequested changes.
- Do not embed reviewer-response language in the manuscript body.

## Verification

- All sections present and non-empty
- Methods section includes study design, participants, outcomes, and statistical methods
- Results follows the `results_skeleton` paragraph order
- Every display item reference matches the EDP
- Discussion principal findings mirror the primary endpoint
- Supplementary materials match the Supplementary Index
- Version number consistent between manuscript and supplementary files
- No reviewer-response language in manuscript body

## References

- `references/section-templates.md`: Study-type-specific section templates and paragraph structures.
- `references/writing-style-guide.md`: Academic writing conventions, tense usage, reporting standards alignment.
- `references/supplementary-materials-guide.md`: Supplementary content drafting rules and format requirements.
- `article-orchestrator/references/artifact-contracts.md`: Canonical manuscript draft and supplementary materials schemas.
- `article-orchestrator/references/artifact-naming-and-directory-rules.md`: Directory, naming, and version rules.
- `article-orchestrator/references/evidence-provenance-ledger-schema.md`: EPL linkage rules for drafter.
