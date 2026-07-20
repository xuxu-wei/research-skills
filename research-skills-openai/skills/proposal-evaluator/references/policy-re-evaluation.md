# Re-evaluation Policy

Use a fresh isolated evaluator for a revised proposal.

## Allowed inputs

- the latest complete frozen proposal bound by logical artifact ID, path, and version;
- the stable rubric and necessary factual context/evidence; and
- an anonymized must-fix list without scores, rationale, decision, authorship,
  or change narrative, only when fix verification is needed.

Do not provide the prior proposal, revision plan, response, delta, prior report,
score, rationale, or decision. Record `prior_versions_visible: false` and
`revision_delta_visible: false`.

For `final_scientific`, do not provide an anonymized must-fix list. Provide only the revised final proposal, stable rubric, and minimal call/factual inputs. Explicitly exclude context/readiness reports, editorial repair briefs, action execution or preservation reports, narrative/language reports, and every prior evaluation artifact.

Do not require, compute, or persist a SHA or digest. A legacy digest field may be read as inert metadata but is not an input requirement, matching key, or report field.

Evaluate the current proposal de novo. The orchestrator alone compares sealed
round reports and the delta to decide improvement or `stop_no_gain`. The
evaluator returns only `accept`, `revise`, or `reject` under the stable gates.
