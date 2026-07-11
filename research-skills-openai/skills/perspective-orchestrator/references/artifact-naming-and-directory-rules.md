# Perspective Artifact Naming and Directory Rules

## Contents

<!-- toc:start -->
- [Project Directory Layout](#project-directory-layout)
- [Directory Rules](#directory-rules)
- [Cross-Package Version Fields](#cross-package-version-fields)
- [Draft Naming](#draft-naming)
- [Revision Naming](#revision-naming)
- [Evaluation And Panel Naming](#evaluation-and-panel-naming)
- [Language QA Naming](#language-qa-naming)
- [Final Naming](#final-naming)
- [Artifact Index](#artifact-index)
<!-- toc:end -->

Use this file to keep Perspective/Viewpoint/Commentary workflow artifacts ordered, versioned, and separate across drafting, evaluation, revision, panel review, and final composition.

## Project Directory Layout

```text
<workspace>/research-perspective-projects/<project-slug>/
  00_input/       # input brief, target outlet profile, assumptions
  01_claims/      # claim ledger, claim-evidence matrix, claim change records
  02_evidence/    # evidence maps, limitations, references
  03_skeletons/   # argument skeleton and feasibility report
  04_drafts/      # perspective-vNNN.md and paragraph maps
  05_evaluations/ # independent evaluation reports
  06_revisions/   # revision rounds, reviewer responses, deltas
  07_panel/       # panel reports and reviewer briefs
  08_final/       # final perspective and compositor reports
  09_state/       # workflow-manifest.yaml, decision-log.md, artifact-index.md
  10_delegates/   # isolated subagent briefs and outputs
```

## Directory Rules

- Two-digit prefixes keep filesystem order aligned with workflow order.
- Drafts belong only in `04_drafts/`.
- Reviewer responses, revision plans, and revision deltas belong only in `06_revisions/round-NNN/`.
- Final submission-facing files belong only in `08_final/`.
- `09_state/workflow-manifest.yaml` stores current pointers and revision lineage.
- `09_state/artifact-index.md` is the human-readable inventory.

## Cross-Package Version Fields

Every artifact registered in `09_state/artifact-index.md` should include the shared lineage fields used across research-idea, research-proposal, and research-article workflows where applicable:

```text
current_artifact_path
artifact_version
revision_round
based_on
change_type
status
plugin_version
source_skill
```

## Draft Naming

```text
04_drafts/perspective-v001.md
04_drafts/perspective-v001-paragraph-map.md
04_drafts/perspective-v002.md
04_drafts/perspective-v002-paragraph-map.md
```

Substantive changes create a new `perspective-vNNN.md`. Language-only polishing may create a new draft version with `change_type: language_only` in workflow state when a modified file is saved.

## Revision Naming

```text
06_revisions/round-001/revision-plan-r001.md
06_revisions/round-001/response-to-reviewers-r001.md
06_revisions/round-001/revision-delta-r001.md
```

The revised perspective remains in `04_drafts/`; the revision directory records why and how it changed.

## Evaluation And Panel Naming

```text
05_evaluations/evaluation-report-v001.md
05_evaluations/evaluation-report-v002.md
07_panel/perspective-v002-standard-panel-summary.md
```

Evaluation and panel files must name the draft version they reviewed. If the draft changes substantively afterward, those reports are stale until refreshed.

## Language QA Naming

```text
05_evaluations/language-assessment-v001.md
06_revisions/round-001/language-change-log-r001.md
```

Language assessment reports are separate artifacts. The orchestrator must explicitly delegate `academic-language-assessor` to a fresh independent subagent for English, Chinese, or bilingual perspective text before final composition and after any language polishing pass. Language polishing must not be embedded in reviewer responses. If a changed perspective file is saved after language polishing, create the next draft version and record `change_type: language_only`.

## Final Naming

```text
08_final/final-perspective.md
08_final/final-edit-log.md
08_final/final-compositor-report.md
08_final/submission-readiness-report.md
```

## Artifact Index

`09_state/artifact-index.md` should contain one row per artifact:

```text
| artifact_id | role | version | path | source_skill | created_step | based_on | status |
```

Allowed statuses:

```text
current | superseded | stale_after_revision | partial | blocked | final
```
