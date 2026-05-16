# Clarification Policy

## Proceed Status

Use one of three statuses.

### `proceed`

Use when the context is clear enough for downstream evidence mapping or idea generation without high-impact assumptions.

### `proceed_with_assumptions`

Use when missing information can be handled by explicit, auditable assumptions. Record each assumption with confidence, impact if wrong, and whether user confirmation is needed.

### `clarification_stop`

Use only when missing information would likely change one or more of:

- research direction;
- data source;
- endpoint/metric;
- intended output;
- core feasibility route;
- user goal.

## Clarification Questions

Ask no more than 3 questions in one turn.

A good clarification question must:

- resolve a high-impact uncertainty;
- be answerable by the user without extra research;
- change downstream routing or feasibility assessment if answered differently.

Do not ask for information that can be safely assumed and marked as uncertain.

## Question Priority

If multiple gaps exist, prioritize:

1. Intended output.
2. Data source or data availability.
3. Study object / population / system.
4. Endpoint or metric.
5. User constraints or risk preference.

## Failure to Clarify

If the user does not answer, the orchestrator may proceed with assumptions only if the assumptions are explicit and the missing information does not meet `clarification_stop` criteria.
