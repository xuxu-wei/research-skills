# Research Idea Naming and Index Rules

Use `idea-artifact-lifecycle.md` as the canonical storage contract.

```text
03_ideas/idea-index-v001.yaml
03_ideas/nodes/I01-001/node.yaml
03_ideas/nodes/I01-001/dossiers/idea-dossier-v001.md
03_ideas/nodes/I01-001/references/reference-ledger.md
03_ideas/nodes/I01-001/revisions/round-001/revision-plan.md
03_ideas/nodes/I01-001/revisions/round-001/revision-delta.md
03_ideas/nodes/I01-001/revisions/round-001/protected-content-register.yaml
03_ideas/nodes/I01-001/revisions/round-001/editorial-repair-writer-brief-r001.yaml
03_ideas/nodes/I01-001/reviews/preflight-r001.md
03_ideas/nodes/I01-001/reviews/narrative-assessment-r001.md
03_ideas/nodes/I01-001/reviews/narrative-repair-plan-r001.yaml
03_ideas/nodes/I01-001/reviews/language-assessment-r001.md
03_ideas/nodes/I01-001/reviews/content-preservation-r001.md
03_ideas/nodes/I01-001/reviews/evaluation-r001.md
03_ideas/nodes/I01-001/reviews/candidate-journal-match-r001.yaml
03_ideas/nodes/I01-001/reviews/medical-journal-review-r001.md
03_ideas/nodes/I01-001/adversarial/<role>-r001.md
03_ideas/nodes/I01-001/handoff/proposal-handoff-v001.md
04_portfolio/research-idea-portfolio-v001.md
05_state/{workflow-state.yaml,artifact-index.md,idea-routing-decision-v001.yaml,round-001-manifest.md}
06_delegates/<review-id>-brief.md
```

- Use canonical Idea IDs from `idea-id-and-lineage-rules.md`. Dossier versions
  are monotonic within a node; never recycle an ID or overwrite a version.
- `node.yaml` is the current pointer. `idea-index-vNNN.yaml` is an immutable
  multi-node index containing IDs, paths, versions, route, and status,
  never dossier prose.
- Register every artifact in `05_state/artifact-index.md` with artifact/Idea ID,
  role, version, path, `based_on`, and status. Validate unique ID/version pairs,
  path existence, complete version history, resolved ancestry, reviewer input
  versions, and consistent current pointers.
- Any saved content change creates the next complete dossier and invalidates the
  prior review. Revision plans and deltas never become current artifacts.
- An editorial-repair writer brief is an orchestrator-owned, frozen YAML
  interface. Register it as lineage, but never treat it as dossier content or a
  reviewer output.
- A candidate journal-match brief is also orchestrator-owned and frozen. It is
  an unscored, unranked reviewer input; the paired medical journal review is a
  separate fresh reviewer output. Bind both by Idea logical reference without a
  SHA or digest.
- Recognize v1/v2 and snapshot/stage layouts as read-only; return
  `layout_migration_required` without automatic migration.
