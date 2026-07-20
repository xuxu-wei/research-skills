# Portfolio Policy

## Focused optimization

Mechanically group outcomes as promoted, revise-then-promote, backup, rejected,
or evaluation-failed using orchestrator decisions, evaluator decision/gates,
and panel status. Do not rescore. Show the candidate journal match and medical
review in separate adjacent fields; neither changes the evaluator score or
decision. `human_signoff_required` requires a current
logical-reference-matched `promote` decision and no unresolved blocking finding;
`revise_then_promote` remains `revision_required` until a revised dossier earns
a fresh qualifying evaluation of the same logical dossier reference.

## Bounded exploration

Present two or three directions in orchestrator order. Do not rank, merge,
recommend, or select a winner. Require one terminal fresh evaluation per current
dossier and, for each applicable biomedical or clinical dossier, its current
candidate journal match and fresh medical review. Journal fit cannot rank the
directions. Return `human_direction_selection_required`. Proposal handoff is
forbidden until the user selects a direction and it resumes focused processing.

## Failure

Return assembly failure for stale/missing/non-isolated evaluation,
stale/missing applicable medical review, scored/ranked or evaluator-contaminated
candidate journal match, logical-reference or identity mismatch, hidden dissent,
incomplete dossier, or contradictory sealed
state. Never force a positive result.
