# Loop Control Rules

## Revision Limits

- Standard mode default: one revision round.
- Standard mode maximum: two revision rounds unless the user explicitly asks to continue.
- Full mode after panel: one major panel revision maximum.
- Minor panel patch does not count as a major panel revision if it changes no claims, evidence, or argument structure.
- Full mode editorial quality cycle: one normalized editorial repair round by default; a second round requires a clear remaining actionable finding and no scientific change.
- Any editorial repair that changes science exits the editorial cycle and restarts scientific revision, applicable panel routing, editorial assessment, and final evaluation for the new version.

## Stop Conditions

Stop and produce a diagnostic report when any condition holds:
- evaluator or panel finds a fatal flaw that cannot be fixed without replacing the thesis
- caveat budget leaves the thesis without a contribution
- two consecutive revisions do not improve hard-gate scores or reduce must-fix count
- a revision introduces new unregistered central claims
- evidence remains insufficient after approved retrieval/handoff
- user declines required thesis/outlet/evidence changes
- the frozen scientific version's writer instance is unavailable for required editorial repair
- editorial conformance, content preservation, or fresh narrative/language reassessment cannot complete independently
- two editorial passes repeat the same actionable finding without measurable closure

## Death Spiral Pattern

Flag a death spiral when revisions repeatedly add caveats, weaken claims, and expand background without increasing contribution sufficiency or evidence-claim match.

Required action: choose one of `narrow_thesis`, `downgrade_claim_strength`, `split_claim`, or `stop_no_gain`.

The blind final evaluator never receives loop history. A non-accept final decision
routes by the current-text finding and creates a new version; it does not authorize an
inline compositor fix.
