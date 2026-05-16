# Research Idea Artifact Naming and Directory Rules

Use this file to keep research-idea workflow artifacts ordered, versioned, and traceable across generation rounds, evaluation, adversarial review, portfolio assembly, and proposal handoff.

## Project Directory Layout

```text
<workspace>/research-idea-projects/<project-slug>/
  00_input/          # raw user materials and constraints
  01_context/        # research context brief
  02_evidence/       # evidence, opportunity, and limitation packets
  03_ideas/          # generated and revised idea pools
  04_preflight/      # methodology/statistics preflight reports
  05_evaluations/    # independent idea evaluation reports
  06_adversarial/    # pre-proposal adversarial reviews
  07_portfolio/      # final and interim idea portfolios
  08_handoff/        # proposal handoff packages
  09_state/          # workflow-state.yaml, artifact-index.md, round manifests
  10_delegates/      # isolated subagent briefs and outputs
```

## Directory Rules

- Two-digit prefixes keep filesystem order aligned with workflow order.
- Store all workflow artifacts in the user project directory, not inside the skill package.
- `09_state/workflow-state.yaml` is the authoritative current pointer store.
- `09_state/artifact-index.md` is the human-readable artifact inventory.
- `10_delegates/` stores isolated subagent inputs and outputs for auditability.
- Generated or revised idea artifacts live only in `03_ideas/`; portfolio artifacts live only in `07_portfolio/`; proposal handoff artifacts live only in `08_handoff/`.
- Reviewer-response artifacts, when requested for external-facing handoff, must be saved separately from portfolio or handoff package prose.

## Cross-Package Version Fields

Every artifact registered in `09_state/artifact-index.md` should use the same lineage fields as the proposal, perspective, and article packages where applicable:

```text
current_artifact_path
artifact_version
revision_round
based_on
change_type
status
source_skill
```

For idea-level artifacts, `idea_id`, `previous_ids`, `origin_round`, and `revision_round` remain the canonical lineage fields. For portfolio and handoff artifacts, use monotonically increasing `vNNN` versions so downstream proposal workflows can cite a stable source package.

## Idea And Round Naming

Canonical idea IDs follow `idea-id-and-lineage-rules.md`:

```text
I<round>-<sequence>
I01-001
I01-002-R01
I02-M001
```

Round artifacts use three-digit round folders:

```text
03_ideas/round-001/generated-idea-set.md
03_ideas/round-001/idea-pool.yaml
03_ideas/round-002/revised-idea-set.md
04_preflight/round-001/preflight-I01-001.md
05_evaluations/round-001/idea-evaluation-I01-001.md
06_adversarial/round-002/adversarial-review-I01-001.md
```

## Portfolio And Handoff Naming

```text
07_portfolio/research-idea-portfolio-v001.md
07_portfolio/research-idea-portfolio-v002.md
08_handoff/proposal-handoff-I01-001.md
08_handoff/proposal-handoff-package-v001.md
08_handoff/proposal-handoff-package-v002.md
```

Language assessment is only required for external-facing portfolio or handoff artifacts:

```text
07_portfolio/language-assessment-v001.md
07_portfolio/language-change-log-r001.md
```

Language QA must be performed through `academic-language-assessor` for English, Chinese, or bilingual external-facing portfolio or handoff text. Language QA must not affect idea scores, promotion/rejection decisions, or adversarial handoff status; it only improves portfolio/handoff readability. If a changed portfolio or handoff file is saved after language polishing, create the next `vNNN` version and record `change_type: language_only`.

## Revision Record Naming

Research-idea revisions are idea-level, not manuscript-level, but repair rounds still need traceable records:

```text
03_ideas/round-002/revision-plan-r002.md
03_ideas/round-002/revision-delta-r002.md
```

If an external reviewer response is requested, save it separately:

```text
08_handoff/response-to-reviewers-r002.md
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
