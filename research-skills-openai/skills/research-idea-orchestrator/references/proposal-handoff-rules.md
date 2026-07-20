# Proposal Handoff Rules

Use this file when `research-idea-orchestrator` decides whether a candidate idea can be handed to `proposal-orchestrator`.

## Minimum Handoff Package

A promoted idea package should include:

- research question or objective;
- target population, system, dataset, material, or study object;
- endpoint, outcome, metric, deliverable, or evaluation target;
- evidence summary and Evidence Map reference;
- Opportunity Map reference;
- methodology/statistics preflight status when relevant;
- independent idea evaluation summary;
- pre-handoff adversarial review summary;
- the current dossier logical reference and its Section 14 authority locator;
- unresolved finding locators and decision status, without copying limitation text;
- user constraints and intended proposal output.

## Ready for Proposal

Mark an idea as ready for proposal workflow only when:

- its route is `focused_optimization`, including a direction that the user
  selected from bounded exploration and explicitly resumed as focused work;
- a fresh independent `idea-evaluator` recommends `promote`; a
  `revise_then_promote` dossier must first be revised and freshly re-evaluated;
- no unresolved fatal flaw blocks drafting;
- the dossier's Section 14 authority is complete and linked without duplicating its text;
- endpoint/metric and data/method path are clear enough for `proposal-readiness-triage`;
- `idea-adversarial-review-panel` returns `handoff_ready` or `conditional_handoff`, with no unresolved blocking objection;
- required user constraints are recorded.

## Return Before Handoff

Do not hand off directly to proposal drafting when:

- evidence is missing or stale and should return to `research-opportunity-mapper`;
- endpoint, metric, data source, or minimal analysis route is unclear and should return to `methodology-statistics-preflight`;
- the idea remains too broad and should return to `multi-path-idea-generator` or `idea-evaluator`;
- adversarial review finds a blocking novelty, feasibility, strategy, or reviewer-defensibility objection;
- critical user choices would change the research direction.
- the bounded-exploration directions have not yet received a human selection.

## Handoff Target

Send proposal-ready ideas to `proposal-orchestrator`, not directly to `proposal-drafter`. The proposal workflow must still run context brief building and readiness triage before drafting.
