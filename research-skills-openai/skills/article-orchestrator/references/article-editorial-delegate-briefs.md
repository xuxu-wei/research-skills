# Article Editorial Delegate Briefs

Use these briefs only after the scientific draft and provisional frontmatter are
frozen.

## Narrative and Language Readiness

Dispatch in parallel to fresh instances against the same frozen reader bundle. Do not
provide either reviewer with the other's report, scientific audits, evaluations,
revision history, or expected findings.

```text
## Task
Assess the frozen article reader bundle for [narrative structure and reader reasoning | academic language and triggered terminology verification]. Review only; do not edit the source or judge scientific quality.

## Input Files
- 06_drafts/manuscript-vNNN.md
- 11_frontmatter/frontmatter-vNNN.md
- Current referenced displays needed to understand the text
- Frozen target-reader handoff and outlet constraints only

## Required Output
- 09_revisions/editorial/round-NNN/[narrative-assessment-rNNN.md and narrative-repair-plan-rNNN.yaml | language-assessment-rNNN.md]

## Prohibited Actions
- Do NOT read scientific audits, evaluations, prior drafts, revision deltas, other reviewer outputs, or expected answers
- Do NOT change claim strength, methods, evidence status, or feasibility judgments
- Do NOT edit the article
```

## Editorial Repair and Preservation

```text
## Writer Task
Execute the assigned actions in the single validated YAML editorial brief. Preserve every protected scientific item and return one complete new artifact version plus action conformance. Do not read raw assessor reports.

## Writer Inputs
- Current complete owned artifact
- 09_revisions/editorial/round-NNN/editorial-repair-brief-rNNN.yaml
- 09_revisions/editorial/round-NNN/protected-content-register.yaml

## Preservation Task
Independently compare the old and revised reader bundle against the protected register. Return only content-preservation-rNNN.md; do not edit sources or read assessor/evaluator outputs.

## Preservation Decisions
- scientific_content_preserved
- editorial_scope_violation
- identity_drift_detected
- scientific_change_declared
```
