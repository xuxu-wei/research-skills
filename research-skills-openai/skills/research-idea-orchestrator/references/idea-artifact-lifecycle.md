# Idea Artifact Lifecycle

Load this contract whenever an Idea is created, revised, reviewed, packaged, or
resumed. It is the canonical `research-idea.v3` persistence model.

## Layout

```text
research-idea-projects/<project-slug>/
  00_input/
  01_context/
  02_evidence/
  03_ideas/
    idea-index-vNNN.yaml
    nodes/<idea-id>/
      node.yaml
      dossiers/idea-dossier-vNNN.md
      references/reference-ledger.md
      revisions/round-NNN/{revision-plan.md,revision-delta.md}
      reviews/{preflight-rNNN.md,evaluation-rNNN.md}
      adversarial/
      handoff/
  04_portfolio/
  05_state/
  06_delegates/
```

- Keep nodes physically flat. Express an explicitly user-created derivation
  through `parent_idea_ids`; never create a child during ordinary revision.
- Keep Idea-specific artifacts in their node. Project context, evidence, index,
  portfolio, state, and delegate records may span nodes.
- Treat `research-idea.v1`, `research-idea.v2`, round/stage layouts, and snapshot
  layouts as read-only. Return `layout_migration_required`; never rewrite or
  migrate them automatically.

## Dossier and index

`dossiers/idea-dossier-vNNN.md` is the sole authoritative Idea body. Follow
`idea-dossier-contract.md`. Store its SHA-256 in `node.yaml`, the immutable
`idea-index-vNNN.yaml`, and reviewer briefs; do not embed a file's own digest.

The index contains only node ID, current dossier ID/version/path/digest,
lineage, route profile, and status. It must not copy dossier prose.

The orchestrator is the sole writer of node, index, ledger, and workflow-state
metadata. Content writers return proposed entries and digests for validation.

Every revision writes a complete next dossier plus a separate delta. A patch,
changed-section list, delta, map, or portfolio is never the current Idea.

## Node state and identity

Keep `node.yaml` concise:

```yaml
schema_version: research-idea.v3
idea_id:
current_dossier_id:
current_version:
current_path:
current_digest: "sha256:"
reference_ledger_path: <idea-node>/references/reference-ledger.md
parent_idea_ids: []
lineage_id:
route_profile: focused_optimization | bounded_exploration
identity_anchor:
  primary_research_question:
  primary_objective:
  study_object:
  core_data_or_evidence_base:
  primary_unit_of_inference:
identity_status: preserved | drifted
qualifying_evaluation_ref:
```

Clarifying or narrowing the same research identity is a revision. Changing only
the title, target audience, contribution framing, or editorial packaging is not
identity drift, but it is a substantive dossier change and requires a new
version plus fresh evaluation. Replacing an identity anchor returns
`new_idea_required`; do not revise in place or auto-create a child.

## Review and promotion gates

- Bind each reviewer brief to the exact current dossier ID, version, path, and
  digest.
- `idea-evaluator` receives exactly that dossier as its only project artifact;
  it receives no map, ledger, preflight, prior version, delta, must-fix list, or
  prior report. The dossier must therefore carry all facts and citations needed
  for evaluation.
- The orchestrator may compare sealed rounds and deltas only after a fresh
  evaluation returns.
- A qualifying report records `reviewed_dossier_digest`,
  `complete_dossier_confirmed`, and `dossier_only_input_confirmed`.
- Package by linking the qualifying dossier, not by rewriting it. A digest
  mismatch, incomplete dossier, identity drift, stale review, or unresolved
  blocking finding prevents promotion.
