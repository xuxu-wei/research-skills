# Evaluation Gates

## Non-Compensatory Gates

- `methods_support_primary_claim`
- `primary_evidence_exists`
- `no_fatal_overclaim`
- `no_fatal_scientific_flaw`
- `language_baseline_passes`

## Decision Rules

- Fatal scientific gate failure -> `reject`.
- Fatal overclaim -> `revise` or `reject` depending on fixability.
- Language baseline failure -> at least `revise`.
- Inline or degraded evaluation may guide revision but cannot support `ready_for_author_signoff`.
- `accept` requires all hard gates passing and no unresolved critical issue.
