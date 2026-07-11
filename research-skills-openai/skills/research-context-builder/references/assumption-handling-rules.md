# Assumption Handling Rules

## Purpose

Assumptions allow early research workflows to proceed without excessive interruption. They must remain visible and auditable.

## Assumption Categories

| Category | Examples | Handling |
|---|---|---|
| Low-impact assumption | intended output likely paper; broad field inferred from terms | proceed with assumption |
| Medium-impact assumption | likely data source; likely population/system; likely endpoint class | proceed with assumption or ask one question if routing changes |
| High-impact assumption | data source unknown; target population unknown; endpoint could change study type | clarify or mark downstream risk |
| Direction-changing assumption | different answer would change research direction, data source, endpoint/metric, or intended output | `clarification_stop` |

## Required Assumption Fields

Each assumption should record:

- assumption text;
- confidence: `high`, `medium`, or `low`;
- impact if wrong: `high`, `medium`, or `low`;
- whether user confirmation is needed.

## Wording

Use neutral wording. Do not present assumptions as facts.

Acceptable:

- “Assumption: the intended output is a journal paper; confidence medium.”
- “Uncertainty: endpoint is not specified; downstream preflight should review metric feasibility.”

Unacceptable:

- “The study will use EHR data” when the user has not said so.
- “This is feasible” before preflight or evaluation.
