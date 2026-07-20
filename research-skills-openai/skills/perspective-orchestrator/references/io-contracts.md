# I/O Contracts

Artifacts default to Markdown. Use YAML for workflow state and for the explicitly
named structured briefs, fact bundles, repair plans, registers, deltas, and
deterministic checks in this contract.

## Contents

- [Core Input](#core-input)
- [Claim and Evidence](#claim-and-evidence)
- [Architecture and Draft](#architecture-and-draft)
- [Evaluation, Revision, and Finalization](#evaluation-revision-and-finalization)

## Core Input

`00_input/01-input-brief.md` must contain:
- working topic
- field tension
- one-sentence core thesis, or a clearly marked unresolved thesis question
- contribution type
- intended reader shift
- declared readers, assumed prior knowledge, and knowledge that must be introduced
- terminology/disclosure order for reader-critical concepts
- reader reasoning handoff from tension through implications
- provisional source intent and binding constraints for supplied materials
- evidence base summary
- boundary and counterargument families
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
- Binding ID
- source intent and bound proposition
- original-source locator
- evidence strength
- evidence directness
- allowed claim strength
- overclaim risk
- citation risk
- boundary condition
- forbidden use and verification status

`02_evidence/reference-list.md` must contain:
- reference ID
- citation
- DOI/PMID/URL/user-material marker
- Claim IDs supported
- Binding ID, source intent, supported sentence or proposition, and original-source locator
- forbidden extrapolation
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
- reader entry contract and five-function reader reasoning handoff
- terminology/disclosure order
- source Binding IDs, intended uses, allowed propositions, and locators per step
- one authority location per distinct counterargument/boundary family

The orchestrator freezes the skeleton's declared readers, prior knowledge, knowledge
that must be introduced, intended shift, terminology/disclosure order, and
five-function reasoning route as an embedded reader handoff with
`{artifact_id, version, path: null, payload: {...}}`. It is indexed logically but is
not a fictitious file. Copy the bounded payload inline into narrative/language or
target-reader delegate briefs without granting access to the manifest, input brief,
or skeleton.

`04_drafts/perspective-v{N}-paragraph-map.md` must map every paragraph to:
- paragraph number
- argument step
- Claim IDs
- Evidence IDs if used
- Source Binding IDs if used
- terminology introduced/defined
- counterargument/boundary family and authority/local status
- paragraph function
- orphan/unregistered-claim risk if present

## Evaluation, Revision, and Finalization

`05_evaluations/evaluation-report-v{N}.md` must contain:
- eight dimension scores with paragraph evidence
- hard gate result
- anti-pattern scan
- decision route
- must-fix / should-fix / optional issues

`05_evaluations/pre-evaluation-conformance-v{N}.yaml` deterministically checks exact
paragraph coverage, registered Claim IDs, Source Binding IDs, skeleton step mapping,
terminology order, and counterargument/boundary authority families. A failure returns
to the writer/curator before evaluation. The evaluator never reads the check or its
inputs.

After scientific qualification, the editorial cycle additionally requires the
narrative and language assessments, one YAML editorial repair brief, protected-content
register, writer delta, deterministic conformance check, fresh preservation report,
and fresh narrative/language reassessments named in the artifact rules.

`05_evaluations/final-evaluation-report-v{N}.md` reads only the final Perspective,
installed stable rubric, and `10_delegates/minimal-evidence-outlet-facts-v{N}.yaml`.
The facts bundle contains clean reader, outlet, evidence, source-binding, contrary,
and discourse facts but no input brief, skeleton, paragraph map, ledger, readiness,
repair, delta, prior review, score, finding, or decision.

`06_revisions/round-NNN/revision-plan-rNNN.md` must contain issue IDs, action strategy, body-integration strategy, risk, owner, and expected artifact.

`07_panel/perspective-vNNN-standard-panel-summary.md` must retain individual reviewer issue IDs and mark consensus, severity, and route.

When requested, `08_cover-letter/` contains a versioned Cover Letter and matching mechanical quality check bound to the qualifying Perspective's logical identity and version. Any `medical-journal-review` report remains a separate independent report under `08_journal/`; its probability block, when present, is carried unchanged.

`08_final/submission-readiness-report.md` must state `yes`, `no`, `conditional`, or `outlet-targeting-only`.

When a Cover Letter exists, `08_final/cover-letter.md` must be text-identical to the current frozen version under `08_cover-letter/`.

`08_final/package-manifest.md` records package members, their logical source
identities/versions, and proposed canonical-index entries. After composition, the
orchestrator alone writes those entries to `09_state/artifact-index.md`.

All new LLM-facing contracts use logical artifact identity and complete index
membership. They do not require SHA, content hashes, or digests; older optional digest
fields remain readable but never become a gate.
