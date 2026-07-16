# Downstream Handoff Rules

## Idea orchestrator and dossier writer

Return map refs, readable opportunities, claim/source locators, evidence limits,
per-claim support status, and Idea direction signals. The orchestrator chooses the deterministic route;
the writer converts relevant evidence into self-contained prose, standard
citations, evidence chains, and Claim-Support rows in a complete dossier.

Do not pass Evidence/Opportunity Maps, limitations, or a reference ledger to
`idea-evaluator`. Evaluation-relevant content must already be in the dossier.

## Preflight and adversarial panel

Provide role-relevant endpoint/data/method/evidence facts and limitations. If an
internal ID appears in a visible report, pair it with a readable label and a
resolvable reference-ledger entry. Preserve each claim's support status; do not
collapse `weak`, `conflicting`, `single-source`, `unverified`, or
`access-limited` into generic support.

## Proposal workflows

Provide evidence summary, exact per-claim support statuses, source limits, and
novelty/gap status as requested by the Proposal role. Do not draft proposal text
or make evaluator decisions.

## Portfolio assembler

Provide map and ledger links plus remaining uncertainties. The portfolio links
the qualifying dossier; it does not duplicate map contents or dossier prose.
