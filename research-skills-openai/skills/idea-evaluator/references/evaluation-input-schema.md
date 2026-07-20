# Evaluation Input Schema

Required project input: exactly one current complete
`dossiers/idea-dossier-vNNN.md`, bound by artifact/Idea ID, version, exact path,
plus an orchestrator independence statement. Do not require or persist a
content hash for the Idea dossier.

The dossier itself must contain all 15 sections, identity anchor, normal
citations/references, complete evidence chains, Claim-Support table, constraints,
and evidence limitations needed for defensible scoring.

Forbidden project inputs include context, Evidence/Opportunity Maps, preflight,
reference ledger, node/index, citation URLs, prior dossiers, deltas, must-fix
lists, reports, scores, decisions, and portfolio context. Do not browse while
scoring. After the evaluation is frozen, official journal scope and article-type
pages are permitted under `journal-matching-contract.md`; they are web sources,
not project inputs.

If the dossier alone is insufficient, return an evaluation-failure report; do
not request or open another project artifact. If fresh delegation is unavailable,
return `independent_review_pending` and stop.

Assess identity only within the current dossier: frontmatter anchor versus body,
or whether a proposed repair would replace an anchor. Historical drift remains
unassessed because prior versions are forbidden.
