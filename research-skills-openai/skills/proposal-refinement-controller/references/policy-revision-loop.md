# Revision Loop Policy

## Purpose

Control proposal revision after an independent `proposal-evaluator` returns `revise`.

## Default Limit

- Default maximum: 2 scientific revision rounds.
- Additional rounds require explicit orchestrator approval and a clear reason.
- Editorial repair uses a separate `editorial_round` counter with the same default ceiling. Continue only when remaining actions are specific, executable without scientific change, and likely to improve fresh reassessment.

## Revision Priority Order

1. Fatal or near-fatal weaknesses that are repairable.
2. Hard gate failures that can be fixed without inventing new facts.
3. Research question, aims, and method alignment.
4. Feasibility and reviewer defensibility.
5. Completion gaps.
6. Clarity and structure.
7. Style and formatting.

## Revision Classes

- `must_fix`: required before re-evaluation.
- `should_fix`: important but not necessarily blocking.
- `optional`: improves quality but should not dominate the round.
- `blocked`: cannot be fixed without new user input or new evidence.

## Loop Decision

After each revision and re-evaluation:

- `accept`: pass gate and return to orchestrator.
- `revise`: continue only if remaining defects are specific and likely fixable.
- `reject`: stop if fatal flaw is not repairable.
- `stop_no_gain`: orchestrator-only route derived after comparing sealed reports; it is never an evaluator decision or input hint.
