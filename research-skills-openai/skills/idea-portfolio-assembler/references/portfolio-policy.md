# Portfolio Policy

## Focused optimization

Mechanically group outcomes as promoted, revise-then-promote, backup, rejected,
or evaluation-failed using orchestrator decisions, evaluator decision/gates,
and panel status. Do not rescore. `human_signoff_required` requires a current
digest-matched `promote` decision and no unresolved blocking finding;
`revise_then_promote` remains `revision_required` until a revised dossier earns
a fresh qualifying evaluation.

## Bounded exploration

Present two or three directions in orchestrator order. Do not rank, merge,
recommend, or select a winner. Require one terminal fresh evaluation per current
dossier and return `human_direction_selection_required`. Proposal handoff is
forbidden until the user selects a direction and it resumes focused processing.

## Failure

Return assembly failure for stale/missing/non-isolated evaluation, digest or
identity mismatch, hidden dissent, incomplete dossier, or contradictory sealed
state. Never force a positive result.
