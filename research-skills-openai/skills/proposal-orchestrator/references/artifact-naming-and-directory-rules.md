# Proposal Artifact Naming and Directory Rules

## Contents

<!-- toc:start -->
- [Project Root](#project-root)
- [Directory Layout](#directory-layout)
- [Cross-Package Version Fields](#cross-package-version-fields)
- [Planning and Reader Naming](#planning-and-reader-naming)
- [Proposal Version Naming](#proposal-version-naming)
- [Revision Round Naming](#revision-round-naming)
- [Language QA Naming](#language-qa-naming)
- [Editorial Repair Naming](#editorial-repair-naming)
- [Evaluation Naming](#evaluation-naming)
- [SAP Naming](#sap-naming)
- [Panel Naming](#panel-naming)
- [Journal Matching and Review Naming](#journal-matching-and-review-naming)
- [Final Package Naming](#final-package-naming)
- [Artifact Index](#artifact-index)
<!-- toc:end -->

Use this file to keep proposal workflow artifacts readable across fast-track entry, multiple revision rounds, SAP branches, review panels, language polishing, and final packaging.

## Project Root

Default project root:

```text
<workspace>/research-proposal-projects/<project-slug>/
```

The user may provide another writable project directory. Do not store workflow artifacts inside the skill package.

## Directory Layout

```text
00_input/       # raw user inputs and imported drafts
01_context/     # proposal context brief
02_evidence/    # evidence and opportunity materials
03_readiness/   # readiness triage
04_drafts/      # proposal-content-plan-vNNN.yaml, proposal-vNNN.md, and current pointer notes
05_evaluations/ # scientific, narrative, language, preservation, and reassessment reports
06_revisions/   # revision rounds, reviewer responses, deltas
07_sap/         # SAP drafts, evaluations, SAP revision rounds
08_panel/       # panel reports and reviewer briefs
09_package/     # final proposal package
10_state/       # workflow-state.yaml, artifact-index.md
11_delegates/   # isolated subagent briefs and outputs
```

Rules:

- Two-digit prefixes keep filesystem order aligned with workflow order.
- `10_state/workflow-state.yaml` is the artifact registry and current pointer store.
- `10_state/artifact-index.md` is the human-readable file inventory.
- `04_drafts/current-proposal.md` may be a copy or pointer note, but it must never be the only copy of a versioned proposal.
- Prior versions must not be overwritten.
- Drafts live only in `04_drafts/`; reviewer responses, revision plans, revision deltas, and language change logs live only in `06_revisions/round-NNN/`; final package files live only in `09_package/`.

## Cross-Package Version Fields

Every artifact registered in `10_state/artifact-index.md` should include the shared lineage fields used across research-idea, research-perspective, and research-article workflows where applicable:

```text
current_artifact_path
artifact_id
version_id
workflow_id
round_id
revision_round
based_on
change_type
status
plugin_version
source_skill
created_by_instance_id
frozen
```

Do not require or generate SHA/digest fields in LLM-facing artifacts. Legacy rows or state records that already contain digest fields remain readable and may be preserved unchanged, but current identity uses `artifact_id`, `version_id`, and `current_artifact_path` with complete index coverage.

Role-specific contracts that use the shorter field `version` serialize the same value as canonical `version_id`; the values must match. They are not separate version axes.

## Planning and Reader Naming

```text
04_drafts/proposal-content-plan-v001.yaml
01_context/proposal-reader-handoff-v001.yaml
```

The planning instance writes only the content plan. Its `planner_instance_id` must differ from the `writer_instance_id` that creates a new full proposal. The reader handoff is a frozen minimal projection of reader, gap, terminology, reasoning-chain, and binding-constraint fields; it is not a review report.

## Proposal Version Naming

Use monotonically increasing version labels:

```text
04_drafts/proposal-v001.md
04_drafts/proposal-v002.md
04_drafts/proposal-v003.md
```

Version rules:

- Initial draft is `proposal-v001.md`.
- Every substantive revision creates the next proposal version.
- Language-only or formatting-only saved drafts create the next version with `change_type: language_only` or `change_type: formatting_only` in workflow state.
- Archival-cleanup passes may create `proposal-vNNN-clean.md` only after the source version is recorded.
- The proposal body should not contain version metadata; version identity belongs in filenames and workflow state.
- `proposal_version` must match the filename version label.

## Revision Round Naming

Each revision round gets its own directory:

```text
06_revisions/round-001/
06_revisions/round-002/
```

Each round should contain:

```text
06_revisions/round-001/revision-plan-r001.md
06_revisions/round-001/response-to-reviewers-r001.md
06_revisions/round-001/revision-delta-r001.md
```

The updated proposal remains in `04_drafts/proposal-vNNN.md`; the round directory records why and how it changed.

## Language QA Naming

Language assessment and language-only revision records are separate artifacts. After scientific/method eligibility, run a fresh `academic-language-assessor` in parallel with a fresh `research-narrative-assessor`; after any editorial change, use different fresh instances for reassessment before final evaluation and packaging:

```text
05_evaluations/language-assessment-v001.md
06_revisions/round-001/language-change-log-r001.md
```

Language polishing must not embed reviewer-response language in the proposal body.
If a changed proposal file is saved after language polishing, create the next proposal version and record `change_type: language_only` in `10_state/workflow-state.yaml`.

## Editorial Repair Naming

Run narrative and language assessment in parallel after scientific/method eligibility:

```text
05_evaluations/proposal-vNNN-narrative-assessment-rNNN.md
05_evaluations/proposal-vNNN-language-assessment-rNNN.md
06_revisions/round-NNN/protected-content-register-rNNN.yaml
06_revisions/round-NNN/editorial-repair-brief-rNNN.yaml
06_revisions/round-NNN/editorial-action-execution-rNNN.yaml
05_evaluations/proposal-vNNN-content-preservation-rNNN.md
05_evaluations/proposal-vNNN-narrative-reassessment-rNNN.md
05_evaluations/proposal-vNNN-language-reassessment-rNNN.md
```

The writer receives only the repair brief, source proposal, and protected register. The repaired proposal remains `04_drafts/proposal-vNNN.md` and is frozen only after all included actions are accounted for.

## Evaluation Naming

Evaluation files should include the proposal version evaluated:

```text
05_evaluations/proposal-v001-evaluation.md
05_evaluations/proposal-v002-re-evaluation.md
```

Rules:

- Do not reuse an evaluation report for a different proposal version.
- If a proposal changes substantively after evaluation, its evaluation status is stale until re-evaluated.

## SAP Naming

SAP files use independent version labels:

```text
07_sap/sap-v001.md
07_sap/sap-v002.md
07_sap/sap-v001-evaluation.md
07_sap/round-001/sap-revision-delta-r001.md
```

SAP versions must remain linked to the proposal version they support in `workflow-state.yaml`.

## Panel Naming

Panel outputs should record proposal version, panel tier, and mode:

```text
08_panel/proposal-v003-standard-blind-panel-summary.md
08_panel/proposal-v003-lightweight-blind-broad-field-review.md
08_panel/proposal-v003-full-context-aware-methodology-review.md
```

Rules:

- `panel_reviewed_proposal_version` must equal the proposal version in panel filenames.
- If the proposal changes after panel review, the panel result applies only to the reviewed version.

## Journal Matching and Review Naming

After final scientific evaluation:

```text
08_panel/journal-candidate-brief-vNNN.yaml
08_panel/proposal-vNNN-medical-journal-review.md
```

The candidate brief is score-free and derives only from the final proposal and verified current journal facts. The fresh medical-journal reviewer cannot read evaluator scores/findings, readiness reports, repair history, editorial reports, or panel outputs.

## Final Package Naming

Final package files live in `09_package/`:

```text
09_package/final-proposal-package.md
09_package/final-artifact-index.md
```

Package status must be one of `human_signoff_required`, `independent_review_pending`, `partial`, `blocked`, `minor_revision_pending`, or `major_revision_required`, derived mechanically from valid upstream artifacts and unresolved issues.

## Artifact Index

`10_state/artifact-index.md` should contain one row per artifact:

```text
| artifact_id | role | version_id | workflow_id | round_id | revision_round | current_artifact_path | source_skill | created_step | created_by_instance_id | based_on | change_type | status | plugin_version | frozen |
```

An index is complete only when every artifact has every column, `version_id` and `current_artifact_path` agree with any role-specific `version` and `path` aliases, and `frozen` is an explicit boolean. Fields that do not apply, such as an initial artifact's `round_id`, `revision_round`, or `based_on`, use explicit `null` or an empty list rather than disappearing. This full row is also the schema of the mirrored registry in `workflow-state.yaml`.

Required statuses:

```text
current | superseded | stale_after_revision | partial | blocked | final
```

The artifact index is the human-readable counterpart to `workflow-state.yaml`.
