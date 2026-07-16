# Evaluation Input Schema

Required project input: exactly one current complete
`dossiers/idea-dossier-vNNN.md`, bound by artifact/Idea ID, version, exact path,
and SHA-256, plus an orchestrator independence statement.

The dossier itself must contain all 15 sections, identity anchor, normal
citations/references, complete evidence chains, Claim-Support table, constraints,
and evidence limitations needed for defensible scoring.

Forbidden project inputs include context, Evidence/Opportunity Maps, preflight,
reference ledger, node/index, citation URLs, prior dossiers, deltas, must-fix
lists, reports, scores, decisions, and portfolio context. Do not browse.

If the dossier alone is insufficient, return an evaluation-failure report; do
not request or open another project artifact. If fresh delegation is unavailable,
return `independent_review_pending` and stop.

Assess identity only within the current dossier: frontmatter anchor versus body,
or whether a proposed repair would replace an anchor. Historical drift remains
unassessed because prior versions are forbidden.
