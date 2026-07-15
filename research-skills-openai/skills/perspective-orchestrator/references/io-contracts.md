# I/O Contracts

All artifacts are Markdown unless noted. YAML is reserved for workflow state.

## Core Input

`00_input/01-input-brief.md` must contain:
- working topic
- field tension
- one-sentence core thesis, or a clearly marked unresolved thesis question
- contribution type
- intended reader shift
- evidence base summary
- boundary conditions
- authorial position
- target outlet constraints
- open questions

`00_input/target-outlet-profile.md` must contain:
- outlet/profile name
- profile source: `user-provided`, `generic`, or `retrieved-guidelines`
- guideline source and last checked date if retrieved
- audience, article type, word/reference limits
- structure preferences
- status: `confirmed` or `provisional`

## Claim and Evidence

`01_claims/claim-ledger.md` must contain one row or block per Claim ID:
- Claim ID
- claim text
- claim type
- claim strength
- supported by Evidence IDs
- contrary evidence
- boundary condition
- allowed wording
- forbidden wording
- status
- last modified

`01_claims/claim-evidence-matrix.md` must contain:
- Claim ID
- Evidence ID
- evidence strength
- evidence directness
- allowed claim strength
- overclaim risk
- citation risk
- boundary condition

`02_evidence/reference-list.md` must contain:
- reference ID
- citation
- DOI/PMID/URL/user-material marker
- Claim IDs supported
- supported sentence or proposition
- source verification date
- risk notes

## Architecture and Draft

`03_skeletons/02-argument-skeleton.md` must contain:
- refined thesis
- contribution type
- problem field
- 3-5 argument steps
- Claim IDs and Evidence IDs per step
- contestability constraint per step
- narrative strategy
- counterarguments and boundaries

`04_drafts/perspective-v{N}-paragraph-map.md` must map every paragraph to:
- paragraph number
- argument step
- Claim IDs
- Evidence IDs if used
- paragraph function
- orphan/unregistered-claim risk if present

## Evaluation, Revision, and Finalization

`05_evaluations/evaluation-report-v{N}.md` must contain:
- eight dimension scores with paragraph evidence
- hard gate result
- anti-pattern scan
- decision route
- must-fix / should-fix / optional issues

`06_revisions/round-NNN/revision-plan-rNNN.md` must contain issue IDs, action strategy, body-integration strategy, risk, owner, and expected artifact.

`07_panel/perspective-vNNN-standard-panel-summary.md` must retain individual reviewer issue IDs and mark consensus, severity, and route.

When requested, `08_cover-letter/` contains a versioned Cover Letter and matching mechanical quality check bound to the qualifying Perspective digest. Any `medical-journal-review` report remains a separate independent report in this directory; its probability block, when present, is carried unchanged.

`08_final/submission-readiness-report.md` must state `yes`, `no`, `conditional`, or `outlet-targeting-only`.

When a Cover Letter exists, `08_final/cover-letter.md` must be text-identical to the current frozen version under `08_cover-letter/`.
