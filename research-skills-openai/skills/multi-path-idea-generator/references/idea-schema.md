# Idea Snapshot Schema

Use `research-idea-orchestrator/references/idea-artifact-lifecycle.md` as the
canonical `research-idea.v2` body, node, identity, and storage contract. Use
`artifact-contracts.md` for shared field names.

Each generated Idea must produce:

1. one flat `03_ideas/nodes/<idea-id>/` directory;
2. one concise `node.yaml` with current path/digest and identity anchor;
3. one complete `snapshots/idea-snapshot-v001.md` with all twelve sections; and
4. one entry in the immutable candidate-set index containing only identity,
   path, version, digest, opportunity IDs, generation paths, and status.

Normalize provisional IDs before any downstream handoff. Record a prior ID in
lineage metadata, not by copying the Idea body. `parent_idea_ids` are empty for
new root Ideas and may be populated only for a user-authorized new Idea node.
Revisions stay inside the existing node.
