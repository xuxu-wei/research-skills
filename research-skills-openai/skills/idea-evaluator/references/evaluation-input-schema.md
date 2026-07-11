# Evaluation Input Schema

定义 `idea-evaluator` 的最低输入要求。

## Required Inputs

- candidate idea
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
- anonymous must-fix list and revision delta for revised ideas, only when needed; never prior scores, findings, or decision
- portfolio context for comparison
- target journal or funding context, if provided

## Input Sufficiency Rule

If missing information prevents defensible scoring, return `evaluation-failure-report.md` rather than guessing.

Every input artifact must be frozen and identified by artifact ID, exact path, and version. If the evaluator is not running in a fresh independent subagent/delegated thread, return `independent_review_pending` with a continuation brief and stop.
