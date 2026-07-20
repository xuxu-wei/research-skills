# Idea Identity and Lineage Rules

Load this reference when assigning an Idea ID, writing a new dossier version,
or checking identity drift.

## Stable node identity

- Assign one stable machine `idea_id` when a node is created, and always pair it
  with the dossier's human-readable title in user-facing navigation.
- Keep every ordinary revision in that node. Increment the complete dossier
  version (`v001`, `v002`, ...) and never encode revision state in the Idea ID.
- Bind each version to its exact path, `based_on`, round, and change
  type in `node.yaml` and the immutable Idea index.
- Never recycle an ID, rename a reviewed node, or treat a title change as a new
  Idea.

## Identity boundary

Compare the current dossier with the node's frozen identity anchors:

- primary research question;
- primary objective;
- study object;
- core data or evidence base;
- primary unit of inference.

Narrowing, clarification, analysis completion, evidence alignment, or supported
title/audience repositioning is a new version of the same node. Replacing an
anchor returns `new_idea_required`; do not revise in place, auto-fork, or merge
nodes.

Only an explicit user-started Idea workflow may create a derived node and set
`parent_idea_ids`. Route-authorized bounded exploration may create independent
sibling nodes, but it does not infer parentage or merge lineage.

## Minimum lineage record

```yaml
idea_id:
version_id:
path:
based_on: []
created_round:
change_type: create | revise | evidence_claim_sync | editorial_reposition | editorial_repair
parent_idea_ids: []
lineage_id:
identity_status: preserved | drifted
```

Reviewer briefs bind the current dossier ID, version, and path. A stale,
missing, or mismatched logical reference cannot qualify the node. Legacy digest
fields are optional and do not participate in Idea validation.
