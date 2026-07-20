# Evaluation Gates

## Non-Compensatory Gates

- `methods_support_primary_claim`
- `primary_evidence_exists`
- `no_fatal_overclaim`
- `no_fatal_scientific_flaw`
- `language_baseline_passes`
- `reader_reasoning_chain_complete`
- `section_functions_hold`

## Decision Rules

- Fatal scientific gate failure -> `reject`.
- Fatal overclaim -> `revise` or `reject` depending on fixability.
- Language baseline failure -> at least `revise`.
- Missing significance, a broken gap-to-rationale transition, or a title/abstract/core-question mismatch -> `reader_reasoning_chain_complete: false` and at least `revise`.
- If fresh independent evaluation is unavailable, return `independent_review_pending` with a continuation brief and stop. No inline or degraded evaluation decision may be produced.
- `accept` requires all hard gates passing and no unresolved critical issue.
