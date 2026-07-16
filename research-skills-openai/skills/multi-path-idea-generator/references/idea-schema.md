# Idea Dossier and Index Schema

Use the orchestrator's v3 lifecycle and dossier contracts as canonical.

Each Idea produces:

1. one flat `03_ideas/nodes/<idea-id>/` directory;
2. concise `node.yaml` with current dossier pointer/digest, identity, route, and
   `reference_ledger_path`;
3. one complete `dossiers/idea-dossier-vNNN.md`;
4. one `<idea-node>/references/reference-ledger.md`; and
5. one immutable `idea_index` entry with path, version, digest, route, lineage,
   and status only. Identity anchors remain authoritative in `node.yaml`.

Normalize provisional IDs before handoff. New root Ideas have no parents.
Revisions, including title/audience/editorial repositioning, stay in the same
node. A user-authorized new research identity may create a child node.
