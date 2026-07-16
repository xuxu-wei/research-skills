# Loop Control and Stop Rules

Load this reference when recording a round, comparing sealed reviews, or
deciding whether another writer/evaluator cycle is allowed.

## Focused optimization

- Allow at most three complete writer -> fresh evaluator rounds.
- Every substantive repair writes the next full dossier version in the same
  node plus a separate revision delta.
- Give each evaluator only the current dossier. Compare the new sealed report
  with earlier sealed reports and the delta only after it returns.
- Continue only when a specific fix is feasible and likely to improve a
  blocking dimension. Do not regenerate broadly in response to a narrow defect.
- Stop early on a qualifying dossier, a fatal flaw, identity drift, owner input
  that changes the route, or no defensible gain.

## Bounded exploration

For each of two or three route-authorized directions, allow exactly:

1. one complete initial dossier;
2. one bounded optimization and new complete version;
3. one direction-specific evidence/opportunity remap;
4. one evidence-and-claim synchronization version when needed; and
5. one terminal fresh dossier-only evaluation.

Remap synchronization cannot add objectives, data, methods, or work packages.
If structural repair is needed, return `revision_required`. After all terminal
evaluations, stop at `human_direction_selection_required`; do not optimize a
second time, select a winner, merge directions, or enter Proposal.

## Required round record

Record round and route, input/output dossier pointers and digests, writer and
reviewer instance IDs, change type, sealed decision, fatal/blocking findings,
dissent, unresolved issues, and next route. Keep reports and deltas outside the
dossier.

## Stop states

- `human_signoff_required`: focused dossier passed all current gates.
- `human_direction_selection_required`: bounded exploration reached terminal review.
- `independent_review_pending`: fresh delegation is unavailable.
- `new_idea_required`: an identity anchor would change.
- `no_defensible_direction`: evidence supports no route.
- `direction_route_confirmation_required`: low, conflicting, or ambiguous route signals.
- `blocked`: fatal flaw, digest mismatch, stale review, or unresolved blocking finding.
- `stopped`: round limit or no defensible gain.

Never convert any stop state to ready merely because the round limit was reached.
