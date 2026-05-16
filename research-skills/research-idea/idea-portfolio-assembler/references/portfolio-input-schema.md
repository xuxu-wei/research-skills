# Portfolio Input Schema

This reference defines the minimum input objects required by `idea-portfolio-assembler`.

## Required Inputs

- `research_context_brief`
- `evidence_map_summary`
- `opportunity_map_summary`
- `idea_pool`
- `idea_evaluation_reports`
- `idea_lineage_records`
- `orchestrator_decisions`

## Conditional Inputs

- `methodology_statistics_preflight_reports`: required when ideas involve endpoint, metric, data source, method, statistics, clinical, observational, prediction, experiment, or benchmark design.
- `proposal_handoff_checks`: required when the portfolio may recommend handoff to `proposal-orchestrator`.
- `evidence_limitations`: required when evidence confidence is not high or clinical/guideline alignment is unverified.

## Minimum Material Requirements

Do not assemble a final portfolio unless each candidate idea has:

- idea identifier;
- title or short label;
- research question or objective;
- evidence / opportunity reference;
- independent evaluation report;
- hard gate status;
- recommendation from `idea-evaluator`;
- lineage record or parent/source note.

If independent evaluation is missing, produce `portfolio-assembly-failure-report`.
