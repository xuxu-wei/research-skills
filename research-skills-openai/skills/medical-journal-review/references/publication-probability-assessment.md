# Publication Probability Assessment

Load this contract only inside an existing `medical-journal-review` call when probability is requested or the frozen target and artifact inputs support an estimate. Keep the result in that review report; do not create another artifact, reviewer, round, stage, state, or promotion rule.

## Schema

```yaml
publication_probability_assessment:
  assessment_scope: cover_letter_only | full_artifact | full_submission_package
  target_outlet:
  article_type:
  benchmark_status: verified_public | user_supplied | heuristic_only | unavailable
  benchmark_sources:
    - url:
      checked_at:
      source_type:
      applicable_scope:
      benchmark_value:
  editorial_screen_pass_probability:
    central_estimate:
    plausible_interval:
  acceptance_given_external_review:
    central_estimate:
    plausible_interval:
  eventual_acceptance_probability:
    central_estimate:
    plausible_interval:
  confidence: high | moderate | low | not_estimable
  upward_drivers: []
  downward_drivers: []
  fatal_or_blocking_factors: []
  domain_scope_limitations: []
  limitations: []
```

## Estimation Rules

- `eventual_acceptance_probability` means acceptance of this submission by the named target outlet, not eventual publication somewhere.
- Give a central estimate and a plausible interval for each estimable stage. Use probabilities or percentages consistently.
- Keep stages mathematically coherent: the overall central estimate should approximate editorial-screen pass multiplied by acceptance conditional on external review. Derive a conservative overall interval from the stage uncertainty; explain material departures.
- These are decision-support estimates, not calibrated forecasts. Base them on the frozen artifact, target/article type, visible strengths and defects, and the best applicable benchmark.
- High estimates never neutralize fatal, blocking, stale-input, incomplete-review, or isolation findings. Low estimates alone do not block delivery of a technically complete package.

## Benchmarks and Search

- For a named outlet, use built-in Search for current public journal, publisher, or other authoritative benchmark facts. Record URL, check date, source type, stated population/article type, reported value, and why it applies.
- Do not create a benchmark-search artifact. Search evidence and its applicability stay inside `benchmark_sources` and the report narrative.
- Prefer verified public figures; use user-supplied figures only with provenance. If no suitable public value exists, use a deliberately wide heuristic interval, set `benchmark_status: heuristic_only`, and normally use low confidence.
- If target, article type, artifact content, or decision-relevant evidence is insufficient, set unavailable fields to `null`, `benchmark_status: unavailable`, `confidence: not_estimable`, and explain what is missing. Never fabricate precision.

## Scope and Confidence

- `cover_letter_only`: judge only the editorial case visible in the letter. An overall interval is allowed, but confidence should normally be low because scientific quality and package completeness are not fully observed.
- `full_artifact`: use the complete current Article or Perspective plus supplied displays and evidence.
- `full_submission_package`: use the complete qualifying artifact and the assembled, current submission materials.
- A non-medical estimate is permitted, but list the reviewer skill's domain mismatch, unavailable field-specific benchmarks, and any transfer assumptions in `domain_scope_limitations`.
- Keep upward/downward drivers separate from fatal/blocking factors. Make interval width and confidence reflect benchmark fit, input completeness, reviewer domain, and unresolved dissent.
