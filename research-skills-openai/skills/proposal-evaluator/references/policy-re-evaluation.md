# Re-evaluation Policy

Use a fresh isolated evaluator for a revised proposal.

## Allowed inputs

- the latest complete frozen proposal and SHA-256;
- the stable rubric and necessary factual context/evidence; and
- an anonymized must-fix list without scores, rationale, decision, authorship,
  or change narrative, only when fix verification is needed.

Do not provide the prior proposal, revision plan, response, delta, prior report,
score, rationale, or decision. Record `prior_versions_visible: false` and
`revision_delta_visible: false`.

Evaluate the current proposal de novo. The orchestrator alone compares sealed
round reports and the delta to decide improvement or `stop_no_gain`. The
evaluator returns only `accept`, `revise`, or `reject` under the stable gates.
