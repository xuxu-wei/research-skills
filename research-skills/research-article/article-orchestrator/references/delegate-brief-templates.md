# Delegate Brief Templates

Templates for isolated subagent delegation briefs used by `article-orchestrator` and `article-refinement-controller`.

## General Brief Structure

Every brief must include:

```text
## Task
[One sentence: what to do. Evaluate / audit / review only — do NOT draft, revise, rewrite.]

## Input Files
- [file path]: [description]

## Context
- User goal: [goal]
- Target journal: [journal]
- Study type: [type]
- Reporting standard: [standard]
- Scope limitations: [if any]

## Required Output
- [output file path]
- [output format requirement]

## Prohibited Actions
- Do NOT [action]
- Do NOT [action]

## Evaluation/Review Constraints (if applicable)
- Evaluate only the [artifact type] provided.
- Do not supplement missing information with assumptions.
- If critical information is missing, flag it; do not fill it in.
```

---

## Readiness Triage Brief

```text
## Task
Assess whether this research has the minimum conditions to enter the manuscript writing system. Gate only — do NOT build context, draft, or evaluate.

## Input Files
- Minimal Intake Summary (inline)

## Required Output
- 01_readiness/readiness-report.md

## Prohibited Actions
- Do NOT normalize input (that is context-builder's job)
- Do NOT retrieve literature
- Do NOT audit methods in detail (that is methods-auditor's job)

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
- 06_drafts/supplementary-vNNN.md (if applicable)
- 04_blueprint/article-blueprint.md
- 02_context/article-context-brief.md
- 03_literature/literature-grounding-report.md
- 07_claim-audit/claim-audit-v001.md
- 05_audit/methods-audit-report.md
- Prior evaluation report (if re-evaluation)
- Revision delta (if re-evaluation)

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

## Sub-Delegation
- Call `academic-language-assessor` for the Language & Academic Register dimension
- Use its report to inform scoring, not to replace independent judgment

## Decision Labels
- accept: ready for panel or compositor
- revise: addressable issues present
- reject: unfixable fatal flaw
- stop_no_gain: re-evaluation only, no substantive improvement
```

---

## Review Panel — Individual Reviewer Brief (Blind External Simulation)

```text
## Task
You are a [reviewer role] reviewing this manuscript as if for [target journal]. Review only the manuscript file provided. Do NOT seek additional context.

## Input Files
- 06_drafts/manuscript-vNNN.md
- Target journal: [journal]

## Context
- Reviewer role: [domain_expert | methodology_statistics | evidence_claim | clarity_structure | submission_guard]
- Review scenario: blind mock review for [target journal]

## Required Output
- 10_panel/reviewer-briefs/reviewer-[role].md

## Prohibited Actions
- Do NOT access context brief, blueprint, evaluation reports, or revision history
- Do NOT access other reviewer outputs
- Do NOT draft, revise, or rewrite manuscript text
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
- 05_audit/methods-audit-report.md

## Context
- Panel mode: internal_diagnostic_review
- Reviewer role: methodology_statistics
- Target journal: [journal]

## Required Output
- 10_panel/reviewer-briefs/reviewer-methodology.md

## Prohibited Actions
- Do NOT draft, revise, or rewrite manuscript text
- Do NOT access other reviewer outputs
```
