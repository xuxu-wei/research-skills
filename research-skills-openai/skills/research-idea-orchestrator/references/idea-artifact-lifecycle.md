# Idea Artifact Lifecycle

Use this contract when creating, revising, reviewing, packaging, or resuming an
Idea. It is the canonical `research-idea.v2` persistence model.

## Node layout

```text
research-idea-projects/<project-slug>/
  00_input/
  01_context/
  02_evidence/
  03_ideas/
    idea-tree.yaml
    candidate-set-vNNN.yaml
    nodes/<idea-id>/
      node.yaml
      snapshots/idea-snapshot-vNNN.md
      revisions/round-NNN/{revision-plan.md,revision-delta.md}
      reviews/{preflight-rNNN.md,evaluation-rNNN.md}
      adversarial/
      handoff/
  04_portfolio/
  05_state/
  06_delegates/
```

- Keep nodes physically flat. Derive the logical tree from `parent_idea_ids` in
  `node.yaml`; `idea-tree.yaml` is a generated index, not another Idea body.
- Keep every Idea-specific artifact inside its node. Context, evidence,
  candidate-set indexes, portfolios, workflow state, and delegate audit trails
  remain project-level because they can span several Ideas.
- A revision writes the next snapshot in the same node. It never creates a
  child. Only a user-authorized new Idea workflow may create a new node with
  parent IDs.
- Treat the legacy round/stage layout as read-only. Return
  `layout_migration_required`; do not migrate or rewrite it automatically.

## Complete Markdown snapshot

`snapshots/idea-snapshot-vNNN.md` is the sole authoritative Idea body. Use short
YAML frontmatter for `schema_version`, `plugin_version`, `artifact_id`,
`idea_id`, `version_id`, `parent_idea_ids`, `based_on`, `source_skill`,
`created_round`, `status`, and `frozen`. Store its SHA-256 in `node.yaml`, the
candidate-set index, and reviewer briefs; never embed a file's own digest in
that file.

Write these non-empty Markdown sections in this order:

1. `## One-sentence summary`
2. `## Research question and objectives`
3. `## Research content and work packages`
4. `## Core hypothesis`
5. `## Scientific significance`
6. `## Relevance, impact, and innovation`
7. `## Potential applications`
8. `## Data, materials, and evidence base`
9. `## Research methods`
10. `## Required analyses and evidence`
11. `## Feasibility, resources, and constraints`
12. `## Risks, assumptions, uncertainties, and stop conditions`

The one-sentence summary describes the complete current Idea without depending
on a parent or delta. Reject comparative-only summaries such as "this version
adds", "compared with the prior version", or "the revision changes". Keep all
change descriptions in `revision-delta.md`.

## Node state and identity

Keep `node.yaml` concise: current snapshot ID/version/path/digest, parent IDs,
lineage, status, qualifying evaluation reference, and an identity anchor with
the primary research question, primary objective, study object, core data or
evidence base, and primary unit of inference.

Allow narrower operationalization or clarification inside the same identity.
Replacing the primary question, objective, study object, evidence basis, or
unit of inference with a different research problem sets
`identity_status: drifted` and returns `new_idea_required`. Do not promote,
revise in place, or create a child automatically.

## Complete-artifact gates

- A generator or reviser must emit a complete snapshot plus a separate delta.
  Reject patches, changed sections, or deltas registered as the current Idea.
- Bind reviewer briefs to the exact current snapshot ID, version, path, and
  digest. Initial review may also receive frozen context/evidence and necessary
  preflight facts.
- A fresh re-reviewer receives only the current complete snapshot, stable
  rubric, necessary factual artifacts, and an anonymized must-fix list. It must
  not read prior snapshots, revision deltas, prior reports, scores, or decisions.
- A qualifying report records `reviewed_snapshot_digest`,
  `complete_snapshot_confirmed`, `identity_drift_detected`,
  `prior_versions_visible: false`, and `revision_delta_visible: false`.
- The orchestrator may compare sealed rounds and deltas only after the fresh
  report returns.
- A portfolio copies or faithfully organizes the qualifying snapshot's full
  sections, binds its digest and lineage, and keeps change history subordinate.
  It must not substitute scores, novelty changes, or a revision narrative for
  the complete Idea.
