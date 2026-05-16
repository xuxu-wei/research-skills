# Portfolio Policy

This file consolidates grouping, ranking, proposal handoff, and assembly failure rules for `idea-portfolio-assembler`.

## Grouping Categories

- `promoted`: ideas recommended as `promote` and passing required gates.
- `revise_then_promote`: promising ideas with limited repair needs.
- `backup`: ideas worth retaining but not prioritized.
- `merged`: ideas absorbed into another idea.
- `rejected`: ideas rejected by evaluator or orchestrator decision.
- `evaluation_failed`: ideas with missing, invalid, or non-isolated evaluation.

## Assembly Rules

- Include 1-3 final candidate ideas when available.
- Do not include more than 3 promoted ideas unless the user explicitly asks.
- Preserve rejected, merged, and backup summaries for auditability.
- Never convert a backup or rejected idea into promoted status.
- Never hide failed gate status.

## Ranking Rules

Rank ideas for presentation, but do not rescore them.

Use these signals in order:

1. orchestrator decision;
2. `idea-evaluator` recommendation;
3. hard gate status;
4. overall score from evaluator;
5. relevance to user goal and intended output;
6. distinctiveness from other final candidates;
7. proposal handoff readiness;
8. severity of remaining uncertainty.

Do not rank a failed-gate idea above a passed-gate idea unless it is explicitly marked as a high-risk backup by the orchestrator.

## Proposal Handoff Status

An idea is handoff-ready only when it has:

- research question;
- endpoint or metric;
- data source or evidence base;
- minimal experiment or analysis route;
- feasibility gate pass;
- clarity gate pass;
- completion gate pass;
- no fatal unresolved preflight blocker.

Handoff status values:

- `ready`: minimum conditions met.
- `conditional`: ready only after named PI decision or limited repair.
- `not_ready`: one or more required elements missing or failed.

Do not write the proposal. Only summarize handoff readiness and required next inputs.

## Assembly Failure

Use an assembly failure report when a reliable portfolio cannot be assembled.

Failure triggers:

- missing independent evaluation reports;
- evaluation appears non-isolated or invalid;
- missing idea pool;
- missing lineage records for revised or merged ideas;
- missing context sufficient to interpret idea relevance;
- contradictory decisions between orchestrator and evaluator without resolution.

Do not assemble a final portfolio when a failure trigger blocks reliable presentation.
