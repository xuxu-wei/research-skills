# Delegate Brief Templates

## Contents

<!-- toc:start -->
- [General Brief Structure](#general-brief-structure)
- [Readiness Triage Brief](#readiness-triage-brief)
- [Methods-Statistics Auditor Brief](#methods-statistics-auditor-brief)
- [Claim Auditor Brief](#claim-auditor-brief)
- [Evaluator Brief](#evaluator-brief)
- [Review Panel — Individual Reviewer Brief (Blind External Simulation)](#review-panel-individual-reviewer-brief-blind-external-simulation)
- [Review Panel — Methodology Reviewer Brief (Internal Diagnostic)](#review-panel-methodology-reviewer-brief-internal-diagnostic)
- [Submission Compositor / Verifier Brief](#submission-compositor-verifier-brief)
<!-- toc:end -->

Templates for isolated subagent delegation briefs used by `article-orchestrator` and `article-refinement-controller`.

## General Brief Structure

Every brief must include:

```text
## Task
[One sentence: what to do. Evaluate / audit / review only — do NOT draft, revise, rewrite.]

## Input Files
- [artifact ID] [version] [file path]: [description]

## Context
- User goal: [goal]
- Target journal: [journal]
- Study type: [type]
- Reporting standard: [standard]
- Scope limitations: [if any]

## Required Output
- [output file path]
- [output format requirement]
- Standard reviewer provenance block with reviewer instance, frozen inputs, files read, isolation mode, decision, findings, and unresolved issues

## Prohibited Actions
- Do NOT [action]
- Do NOT [action]
- Do NOT edit, rewrite, polish, or fix source artifacts
- Do NOT access parent hidden reasoning, expected answers, prior scores or decisions, or other reviewer outputs

## Evaluation/Review Constraints (if applicable)
- Evaluate only the [artifact type] provided.
- Do not supplement missing information with assumptions.
- If critical information is missing, flag it; do not fill it in.
- If a fresh independent subagent cannot run, return `independent_review_pending` with a continuation brief and stop; never review inline.
```

---

## Readiness Triage Brief

```text
## Task
Assess whether this research has the minimum conditions to enter the manuscript writing system. Gate only — do NOT build context, draft, or evaluate.

## Input Files
- Frozen Minimal Intake Summary
- Every readiness-relevant path declared in its complete material inventory

## Required Output
- 01_readiness/readiness-report.md

## Prohibited Actions
- Do NOT normalize input (that is context-builder's job)
- Do NOT retrieve literature
- Do NOT audit methods in detail (that is methods-auditor's job)
- Do NOT treat absent raw data/code as absent results when a supplied technical report, table, figure, or executed output establishes the primary result
- Do NOT discard compatible assets merely because another file is the declared semantic authority

## Decision Framework
- ready: can proceed to context building
- conditionally_ready: proceed with nonblocking gaps noted
- not_ready: stop, return blocking gaps
- wrong_article_type: recommend alternative article type
```

---

## Methods-Statistics Auditor Brief

```text
## Task
Audit the study methods and statistical approach BEFORE drafting. Determine if there are unfixable flaws that would block manuscript writing. Audit only — do NOT suggest rewrites, draft methods text, or evaluate overall quality.

## Input Files
- 02_context/article-context-brief.md
- Protocol or SAP (if available)
- Statistical outputs (if available)
- Tables/figures (if available)

## Context
- User goal: [goal]
- Target journal: [journal]
- Study design type: [type]
- Reporting standard: [standard]

## Required Output
- 05_audit/methods-audit-report.md

## Prohibited Actions
- Do NOT draft or revise manuscript text
- Do NOT evaluate overall manuscript quality
- Do NOT perform new statistical analyses
- Do NOT claim a method is wrong unless the evidence is clear
- When uncertain, use "requires_author_verification" or "potential_issue"

## Key Questions to Answer
1. Does the study design support the primary inference?
2. Is the primary endpoint clearly defined and pre-specified?
3. Is sample size adequate or post-hoc power reported?
4. Is the primary statistical model appropriate?
5. Are missing data, confounding, multiplicity adequately handled?
6. Are any methodological flaws unfixable by writing alone?
```

---

## Claim Auditor Brief

```text
## Task
Audit every core claim in the manuscript against its supporting evidence. Claim-level only — do NOT evaluate overall manuscript quality, structure, or journal fit.

## Input Files
- 06_drafts/manuscript-vNNN.md
- 04_blueprint/article-blueprint.md (for Claim-Evidence Matrix and Evidence Provenance Ledger)
- 06_drafts/supplementary-vNNN.md (if applicable)

## Context
- User goal: [goal]
- Target journal: [journal]
- Scope limitations: [if fast-track backfill]

## Required Output
- 07_claim-audit/claim-audit-v001.md

## Prohibited Actions
- Do NOT draft, revise, or rewrite text
- Do NOT evaluate overall manuscript quality
- Do NOT evaluate journal fit
- Do NOT audit methods
- Do NOT assess language quality

## For Each Claim, Judge
1. Evidence support: strong | moderate | weak | absent
2. Inference validity: valid | overstated | invalid
3. Wording: appropriate | overclaimed | underclaimed
4. Boundary clarity: clear | vague | missing
5. Required action: retain | strengthen | downscale | remove | move_to_discussion | move_to_supplementary
```

---

## Evaluator Brief

```text
## Task
Evaluate the manuscript independently across seven dimensions with non-compensatory gates. Evaluate only — do NOT draft, revise, or rewrite.

## Input Files
- 06_drafts/manuscript-vNNN.md
- 11_frontmatter/frontmatter-vNNN.md
- 06_drafts/supplementary-vNNN.md (if applicable)
- 04_blueprint/display-asset-manifest.yaml and current available assets
- Stable rubric and minimal factual or outlet constraints needed to interpret the final artifact

## Context
- User goal: [goal]
- Target journal: [journal]
- Scope limitations: [if any]

## Required Output
- 08_evaluations/manuscript-vNNN-evaluation.md (or -re-evaluation.md)

## Prohibited Actions
- Do NOT draft, revise, or rewrite manuscript text
- Do NOT perform supplementary analysis
- Do NOT substitute for claim-auditor or methods-auditor
- Do NOT lower standards to push the workflow forward
- Do NOT read any prior evaluation report, score, or decision
- Do NOT read any prior manuscript or revision delta
- Do NOT read context briefs, blueprints/plans, audits, narrative/language reports, repair plans/briefs, protected-content registers, preservation reports, panel reports, or anonymous must-fix lists

## Sub-Delegation
- None. The orchestrator completed sealed narrative/language readiness before this evaluation and exposes none of those reports.

## Decision Labels
- accept: ready for panel or compositor
- revise: addressable issues present
- reject: unfixable fatal flaw
```

---

## Review Panel — Individual Reviewer Brief (Blind External Simulation)

```text
## Task
You are a [reviewer role] reviewing this manuscript as if for [target journal]. Review only the frozen role-specific files listed below. Do NOT seek additional context.

## Input Files
- 06_drafts/manuscript-vNNN.md
- 04_blueprint/journal-adapter.md (submission_guard only)
- Target journal: [journal]

## Context
- Reviewer role: [domain_expert | methodology_statistics | evidence_claim | clarity_structure | submission_guard]
- Review scenario: blind mock review for [target journal]

## Required Output
- 10_panel/reviewer-briefs/reviewer-[role].md

## Prohibited Actions
- Do NOT access context brief, evaluation reports, or revision history
- Do NOT access blueprint files unless the assigned role is submission_guard, which receives only the frozen journal adapter
- Do NOT access other reviewer outputs
- Do NOT draft, revise, or rewrite manuscript text
- Do NOT edit, polish, or fix the source manuscript
```

---

## Review Panel — Methodology Reviewer Brief (Internal Diagnostic)

```text
## Task
You are the methodology/statistics reviewer. In internal diagnostic mode, you have access to protocol-level information to distinguish "the manuscript is unclear" from "the study design has a real problem."

## Input Files
- 06_drafts/manuscript-vNNN.md
- 02_context/article-context-brief.md
- Protocol or SAP (if available)
- Statistical output tables (if available)

## Context
- Panel mode: internal_diagnostic_review
- Reviewer role: methodology_statistics
- Target journal: [journal]

## Required Output
- 10_panel/reviewer-briefs/reviewer-methodology.md

## Prohibited Actions
- Do NOT draft, revise, or rewrite manuscript text
- Do NOT access other reviewer outputs
- Do NOT edit, polish, or fix the source manuscript
```

---

## Submission Compositor / Verifier Brief

```text
## Task
Assemble faithful package copies, including the primary DOCX when document tooling is available, and verify the final frozen artifact set. Do not modify any source artifact.

## Input Files
- Frozen artifact IDs, versions, and paths for the complete final manuscript, display-asset manifest/assets, supplementary materials, frontmatter, cover letter, audits, evaluations, panel report, revision history, and journal adapter

## Required Output
- 12_package/submission-package.md
- 12_package/manuscript-vNNN.docx
- 12_package/docx-parity-and-render-report.md
- 12_package/submission-readiness-summary.md
- 12_package/human-signoff-checklist.md
- Standard reviewer provenance block

## Prohibited Actions
- Do NOT edit, rewrite, polish, patch, or fix source artifacts
- Do NOT re-score or reinterpret upstream review findings
- Do NOT hide dissent or unresolved issues
- Do NOT emit a ready status when independent evaluation or fresh final verification is incomplete
- Do NOT emit `human_signoff_required` when Markdown/DOCX parity, required assets, or full-page render QA is incomplete

## Failure Route
- If a fresh independent compositor/verifier cannot run, return `independent_review_pending` with this completed continuation brief and stop.
```
