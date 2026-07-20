# Readiness Report Schema

Use the canonical `article_readiness_report` schema in `article-orchestrator/references/artifact-contracts.md`.

## Required Fields

- `readiness_status`: `ready`, `conditionally_ready`, `not_ready`, or `wrong_article_type`.
- `recommended_article_type`: manuscript genre that best matches the available study material.
- `minimum_inputs_present`: explicit true/false/not_applicable flags for research question, design, results, methods, figures/tables, and references.
- `blocking_gaps`: gaps that make writing irresponsible or impossible.
- `nonblocking_gaps`: gaps that can be handled during writing with assumptions or author confirmation.
- `target_journal_realism`: realism label plus rationale.
- `recommended_route`: next workflow route.
- `material_inventory_coverage`: every declared readiness-relevant file marked `read`, `excluded_with_reason`, or `unreadable`.
- `semantic_authority_applied`: the authority artifact and the exact conflicts it governs, without excluding compatible result assets.

## Gate Rules

- Missing primary results, undefined study design, or no research question must return `not_ready`. "Missing primary results" means no supplied executed result artifact can support the primary result; it does not mean raw data or independent re-execution is unavailable.
- `conditionally_ready` requires at least one explicit mitigation in `nonblocking_gaps`.
