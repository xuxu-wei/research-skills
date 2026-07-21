# Loop Control and Stop Rules

Load this reference when recording a round, comparing sealed reviews, or
deciding whether another writer/evaluator cycle is allowed.

## Focused optimization

- Allow at most three complete scientific writer -> editorial readiness ->
  fresh evaluator rounds.
- Every substantive repair writes the next full dossier version in the same
  node plus a separate revision delta.
- Give each evaluator only the current, editorially ready dossier. Compare the new sealed report
  with earlier sealed reports and the delta only after it returns.
- Continue only when a specific fix is feasible and likely to improve a
  blocking dimension. Do not regenerate broadly in response to a narrow defect.
- A localized low-impact minor execution deviation is recorded for owner
  prioritization and does not start correction, reproduction, or extra testing.
- Stop early on a qualifying dossier, a fatal flaw, identity drift, owner input
  that changes the route, or no defensible gain.
- After the final effective current-version evaluation, an applicable
  biomedical or clinical journal review is a terminal companion review. It does
  not consume an evaluator round and its report is never fed to the evaluator.
  Any accepted substantive change creates a new dossier version and invalidates
  the candidate match and medical review as well as the prior evaluation.

## Bounded exploration

For each of two or three route-authorized directions, allow exactly:

1. one complete initial dossier;
2. one bounded optimization and new complete version;
3. one evidence-change assessment; call `research-landscape-mapper` only for a
   `major` core-claim, novelty-position, landscape, or material-conflict change;
4. one evidence-and-claim synchronization version when retrieval changed
   evidence; and
5. fresh editorial readiness and one terminal fresh dossier-only evaluation.

Bounded citation or single-claim checks use Built-in Search, or one
`focused-literature-synthesizer` task when 2-5 papers require close synthesis.
Editorial changes reuse evidence. Synchronization cannot add objectives, data,
methods, or work packages.
If structural repair is needed, return `revision_required`. After all terminal
  evaluations, stop at `human_direction_selection_required`; do not optimize a
  second time, select a winner, merge directions, or enter Proposal.

For each final current biomedical or clinical direction, complete its candidate
journal match and fresh medical review before portfolio assembly. These reviews
do not rank directions and cannot be used to select an exploration winner.

## Required round record

Record round and route, input/output dossier logical references, writer and
reviewer instance IDs, change type, sealed decision, fatal/blocking findings,
dissent, unresolved issues, and next route. Keep reports and deltas outside the
dossier.

## Stop states

- `human_signoff_required`: focused dossier passed all current gates.
- `human_direction_selection_required`: bounded exploration reached terminal review.
- `independent_review_pending`: fresh delegation is unavailable.
- `specialist_review_pending`: an applicable final current dossier has a frozen
  candidate journal-match brief and awaits its fresh medical journal review.
- `new_idea_required`: an identity anchor would change.
- `no_defensible_direction`: evidence supports no route.
- `direction_route_confirmation_required`: low, conflicting, or ambiguous route signals.
- `editorial_review_pending`: fresh narrative/language assessment has not returned.
- `editorial_revision_required`: critical/major readiness findings or a
  professional-editing requirement remains unresolved; minor findings stay
  visible but do not alone force another repair round.
- `clarification_stop`: required information for a readiness judgment is
  missing; resume with a fresh assessment after that information is supplied.
- `blocked`: fatal flaw, invalid artifact reference, stale review, or unresolved blocking finding.
- `stopped`: round limit or no defensible gain.

Never convert any stop state to ready merely because the round limit was reached.
