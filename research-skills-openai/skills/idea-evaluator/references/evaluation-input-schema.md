# Evaluation Input Schema

定义 `idea-evaluator` 的最低输入要求。

## Required Inputs

- current complete `idea-snapshot-vNNN.md`, its node ID, version, path, and SHA-256
- Research Context Brief
- Evidence Map or explicit evidence limitation
- Opportunity Map or explicit reason for absence
- user goal and intended output
- available data / data source, if relevant
- endpoint or metric, if relevant
- generation path and lineage
- independence statement from orchestrator

## Conditional Inputs

- Methodology-Statistics Preflight Report
- anonymous must-fix list for a revised Idea, only when needed
- portfolio context for comparison
- target journal or funding context, if provided

## Input Sufficiency Rule

If missing information prevents defensible scoring, return `evaluation-failure-report.md` rather than guessing.

Every input must be frozen and identified by artifact ID, exact path, version, and digest. A re-evaluator must not read prior snapshots, deltas, reports, scores, or decisions. If fresh delegation is unavailable, return `independent_review_pending` with a continuation brief and stop.
