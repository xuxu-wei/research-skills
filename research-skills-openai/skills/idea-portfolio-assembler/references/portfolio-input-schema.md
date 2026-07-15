# Portfolio Input Schema

This reference defines the minimum input objects required by `idea-portfolio-assembler`.

## Required Inputs

- `research_context_brief`
- `evidence_map_summary`
- `opportunity_map_summary`
- current complete Idea snapshots, node pointers, and SHA-256 digests
- `idea_evaluation_reports`
- `idea_lineage_records`
- `orchestrator_decisions`

## Conditional Inputs

- `methodology_statistics_preflight_reports`: required when ideas involve endpoint, metric, data source, method, statistics, clinical, observational, prediction, experiment, or benchmark design.
- `proposal_handoff_checks`: required when the portfolio may recommend handoff to `proposal-orchestrator`.
- `adversarial_panel_reports`: required for every idea whose proposal handoff status may be `ready` or `conditional`; include all role reports, blocking findings, and dissent.
- `evidence_limitations`: required when evidence confidence is not high or clinical/guideline alignment is unverified.

## Minimum Material Requirements

Do not assemble a final portfolio unless each candidate idea has:

- idea identifier;
- title or short label;
- all twelve complete-snapshot sections;
- matching current node pointer and SHA-256;
- evidence / opportunity reference;
- independent evaluation report that confirms the same digest and complete snapshot;
- hard gate status;
- recommendation from `idea-evaluator`;
- lineage record or parent/source note.
- a completed adversarial panel report with no unresolved blocking finding when the idea is marked `ready` or `conditional` for proposal handoff.

If the complete snapshot, digest match, preserved identity, or independent evaluation is missing, produce `portfolio-assembly-failure-report`.
