# Research Idea Naming and Index Rules

Use `idea-artifact-lifecycle.md` as the canonical directory, snapshot, identity,
and review-visibility contract. This file only defines compact names and indexes.

## Project and node names

```text
research-idea-projects/<project-slug>/
03_ideas/idea-tree.yaml
03_ideas/candidate-set-v001.yaml
03_ideas/nodes/I01-001/
03_ideas/nodes/I01-001/node.yaml
03_ideas/nodes/I01-001/snapshots/idea-snapshot-v001.md
03_ideas/nodes/I01-001/snapshots/idea-snapshot-v002.md
03_ideas/nodes/I01-001/revisions/round-001/revision-plan.md
03_ideas/nodes/I01-001/revisions/round-001/revision-delta.md
03_ideas/nodes/I01-001/reviews/preflight-r001.md
03_ideas/nodes/I01-001/reviews/evaluation-r001.md
03_ideas/nodes/I01-001/adversarial/<role>-r001.md
03_ideas/nodes/I01-001/handoff/proposal-handoff-v001.md
04_portfolio/research-idea-portfolio-v001.md
05_state/workflow-state.yaml
05_state/artifact-index.md
05_state/round-001-manifest.md
06_delegates/<review-id>-brief.md
```

Use canonical Idea IDs from `idea-id-and-lineage-rules.md`. A snapshot version
is monotonic within one node. Never recycle a node ID or overwrite a snapshot.

## Node and tree indexes

`node.yaml` is the authoritative current pointer for one Idea. Record the
fields required by `idea-artifact-lifecycle.md` plus `workflow_id`, `round_id`,
`plugin_version`, `source_skill`, `created_by_instance_id`, `based_on`,
`change_type`, `status`, and `frozen` where applicable.

`idea-tree.yaml` contains only node IDs, parent IDs, current versions, paths,
digests, and statuses. Generate it from node files; never copy Idea prose into
it. `candidate-set-vNNN.yaml` is likewise an immutable multi-Idea index, not a
second body representation.

`05_state/artifact-index.md` contains one row per artifact:

```text
| artifact_id | idea_id | role | version | path | digest | based_on | status |
```

Allowed statuses are `current`, `superseded`, `stale_after_revision`,
`partial`, `blocked`, and `final`.

## Version and legacy rules

- A substantive, structural, or saved language change writes the next complete
  snapshot version and invalidates prior reviews.
- A revision plan or delta never becomes the current artifact.
- A user-authorized new research problem creates a new node and may record
  parent IDs; ordinary revisions stay in the same node.
- Detect legacy `03_ideas/round-NNN`, `04_preflight`, `05_evaluations`,
  `06_adversarial`, `08_handoff`, `09_state`, or `10_delegates` layouts as
  read-only and return `layout_migration_required`. Do not auto-migrate them.
