# Loop Control Rules

## Revision Limits

- Standard mode default: one revision round.
- Standard mode maximum: two revision rounds unless the user explicitly asks to continue.
- Full mode after panel: one major panel revision maximum.
- Minor panel patch does not count as a major panel revision if it changes no claims, evidence, or argument structure.

## Stop Conditions

Stop and produce a diagnostic report when any condition holds:
- evaluator or panel finds a fatal flaw that cannot be fixed without replacing the thesis
- caveat budget leaves the thesis without a contribution
- two consecutive revisions do not improve hard-gate scores or reduce must-fix count
- a revision introduces new unregistered central claims
- evidence remains insufficient after approved retrieval/handoff
- user declines required thesis/outlet/evidence changes

## Death Spiral Pattern

Flag a death spiral when revisions repeatedly add caveats, weaken claims, and expand background without increasing contribution sufficiency or evidence-claim match.

Required action: choose one of `narrow_thesis`, `downgrade_claim_strength`, `split_claim`, or `stop_no_gain`.

