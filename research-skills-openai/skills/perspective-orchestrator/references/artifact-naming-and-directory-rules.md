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
- [Editorial Quality Cycle Naming](#editorial-quality-cycle-naming)
- [Final Evaluation And Journal Review Naming](#final-evaluation-and-journal-review-naming)
- [Cover Letter Naming](#cover-letter-naming)
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
  08_journal/     # clean candidate journal facts and isolated medical review
  08_cover-letter/# versioned Cover Letter and mechanical check
  08_final/       # final perspective, optional Cover Letter copy, compositor reports
  09_state/       # workflow-manifest.yaml, decision-log.md, artifact-index.md
  10_delegates/   # isolated subagent briefs and outputs
```

## Directory Rules

- Two-digit prefixes keep filesystem order aligned with workflow order.
- Drafts belong only in `04_drafts/`.
- Reviewer responses, revision plans, and revision deltas belong only in `06_revisions/round-NNN/`.
- Final submission-facing files belong only in `08_final/`.
- Versioned Cover Letter materials belong only in `08_cover-letter/`; a current frozen letter may be copied unchanged into `08_final/`.
- Clean concrete journal matching and applicable medical-journal-review artifacts belong in `08_journal/`; they never contain evaluator material.
- `09_state/workflow-manifest.yaml` stores current pointers and revision lineage.
- `09_state/artifact-index.md` is the human-readable inventory.

## Cross-Package Version Fields

Every artifact registered in `09_state/artifact-index.md` should include the shared lineage fields used across research-idea, research-proposal, and research-article workflows where applicable:

```text
artifact_id
version
path
workflow_id
round_id
revision_round
based_on
change_type
status
plugin_version
source_skill
created_by_instance_id
writer_instance_id
frozen
```

Legacy readers may accept `version_id` and `current_artifact_path`, normalize them to
`version` and `path`, and never write them into new state. `content_digest`, `sha`, and
similar fields are also legacy read-only metadata; new LLM-facing artifacts and
indexes omit them and no workflow gate depends on them.

## Draft Naming

```text
04_drafts/perspective-v001.md
04_drafts/perspective-v001-paragraph-map.md
04_drafts/perspective-v002.md
04_drafts/perspective-v002-paragraph-map.md
```

Substantive changes create a new `perspective-vNNN.md`. Before scientific freeze, a
language-only action inside the current scientific revision plan may create a new
draft version with `change_type: language_only`. After scientific freeze, every
language mutation is `change_type: editorial_repair` and must use the normalized
same-writer editorial route.

Each draft lineage entry records `writer_instance_id`. Editorial repair must reuse the
writer instance bound to the current frozen scientific version.

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
05_evaluations/pre-evaluation-conformance-v002.yaml
07_panel/perspective-v002-standard-panel-summary.md
```

Evaluation and panel files must name the draft version they reviewed. If the draft changes substantively afterward, those reports are stale until refreshed.
The deterministic conformance file may read the skeleton, ledger, and paragraph map,
but it is not a review and is never included in an evaluator isolation package.

## Language QA Naming

```text
05_evaluations/language-assessment-v001.md
06_revisions/round-001/language-change-log-r001.md
```

Language assessment reports are separate artifacts. Before scientific freeze, the
orchestrator may include a bounded language action in the current scientific revision
plan and record `change_type: language_only`. After scientific freeze, there is no
standalone language-polishing route: fresh language assessment feeds the single YAML
editorial brief, the same writer repairs, and conformance, preservation, parallel
reassessment, and final evaluation repeat. Language changes never hide in a reviewer
response.

## Editorial Quality Cycle Naming

```text
05_evaluations/narrative-assessment-vNNN-r001.md
05_evaluations/narrative-repair-plan-vNNN-r001.yaml
05_evaluations/language-assessment-vNNN-r001.md
06_revisions/round-NNN/protected-content-register-rNNN.yaml
06_revisions/round-NNN/editorial-repair-brief-rNNN.yaml
06_revisions/round-NNN/editorial-revision-delta-rNNN.yaml
06_revisions/round-NNN/editorial-conformance-check-rNNN.yaml
05_evaluations/content-preservation-vNNN.md
05_evaluations/narrative-reassessment-vNNN.md
05_evaluations/language-reassessment-vNNN.md
```

Assessment and reassessment artifacts name the exact Perspective version reviewed.
The writer receives only the normalized brief, frozen source, and protected-content
register. The final evaluator receives none of these files.

## Final Evaluation And Journal Review Naming

```text
10_delegates/minimal-evidence-outlet-facts-vNNN.yaml
05_evaluations/final-evaluation-report-vNNN.md
08_journal/candidate-journal-match-brief-vNNN.yaml
08_journal/medical-journal-review-vNNN.md
```

The final evaluator reads exactly the Perspective and minimal facts bundle. Journal
matching and medical review occur separately and contain no evaluator scores,
findings, gates, decisions, or repair history.

## Cover Letter Naming

```text
08_cover-letter/cover-letter-v001.md
08_cover-letter/cover-letter-quality-check-v001.md
08_final/cover-letter.md
```

A changed Perspective logical version/current pointer, target outlet, or core argument makes the letter and its review stale. The final copy must be text-identical to the current frozen letter.

Legacy projects may contain
`08_cover-letter/medical-journal-cover-letter-review-v001.md`; accept it as read-only
history but do not create it in new runs. Current medical editorial and cover-letter
observations remain together in the isolated
`08_journal/medical-journal-review-vNNN.md` report.

## Final Naming

```text
08_final/final-perspective.md
08_final/cover-letter.md              # only when a Cover Letter exists
08_final/package-manifest.md
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

The index is complete only when every required artifact role for the selected mode has
one resolvable logical identity and exactly one current pointer where the role is
single-current. An embedded reader handoff uses `path: null` and is not listed as a
file read. No digest is required.
