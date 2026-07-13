# Assembly contract

## Contents

- Matrix input check
- Candidate portfolio
- Sealed provenance index
- Revision brief
- Specialist findings bundle
- Selection dossier

## Matrix input check

Require exactly these perspectives:

- `scientific_significance`
- `practical_value`
- `dissemination_editorial`

Each report must account for `reposition_only`, `small_extension`, and `moderate_extension` with either an option or `no_defensible_option`. Require three distinct reviewer instance IDs and identical dossier/evidence digests.

## Candidate portfolio

```yaml
research_polisher_candidate_portfolio:
  artifact_id:
  version:
  plugin_version:
  source_skill: research-polisher-plan-assembler
  workflow_id:
  round_id:
  based_on_dossier:
    artifact_id:
    version:
    sha256:
  evidence_artifact_ids: []
  matrix_completeness:
    perspectives_present: []
    tiers_accounted: 9
  options: []
  no_defensible_cells: []
  conflicts: []
  dissent: []
  unresolved_issues: []
  target_requirements_status:
  sanitization:
    reviewer_identities_visible: false
    raw_report_paths_visible: false
    prior_scores_visible: false
    prior_decisions_visible: false
    cluster_frequency_visible: false
```

Each anonymous option preserves its tier, positioning, value mechanism, claim delta, evidence IDs, added work, feasibility basis, dependencies, risks, unknowns, incompatibilities, fallback, and stop condition. Do not expose its originating perspective or reviewer.

## Sealed provenance index

```yaml
sealed_provenance:
  artifact_id:
  version:
  plugin_version:
  source_skill: research-polisher-plan-assembler
  based_on: []
  portfolio_artifact_id:
  portfolio_version:
  source_report_bindings:
    - anonymous_option_id:
      review_id:
      reviewer_instance_id:
      review_perspective:
      raw_report_path:
      raw_report_sha256:
      source_cell:
  cluster_bindings: []
  dissent_bindings: []
  access_scope: orchestrator_and_lineage_validator_only
```

Never place this index in the final-reviewer allowlist.

## Revision brief

Include artifact ID/version, plugin version, `source_skill: research-polisher-plan-assembler`, `based_on`, current portfolio/evaluation IDs and digests, affected anonymous options/tiers/perspectives, anonymized must-fix findings, required evidence, unchanged options, and the required new portfolio version. Exclude scores, evaluator identity, overall decision, and raw review prose not needed for repair.

## Specialist findings bundle

```yaml
research_polisher_specialist_findings_bundle:
  artifact_id:
  version:
  plugin_version:
  source_skill: research-polisher-plan-assembler
  based_on: []
  dossier_binding: {}
  portfolio_binding: {}
  requested_questions: []
  affected_anonymous_option_ids: []
  findings: []
  limitations: []
  sanitization:
    reviewer_identities_visible: false
    raw_report_paths_visible: false
    scores_visible: false
    decisions_visible: false
```

Bind every finding to a requested question and current input digest. Do not include unrequested specialist commentary. A new final-reviewer instance may read this bundle, but not the raw specialist reports.

## Selection dossier

```yaml
research_polisher_selection_dossier:
  artifact_id:
  version:
  plugin_version:
  source_skill: research-polisher-plan-assembler
  based_on: []
  workflow_id:
  dossier_binding: {}
  portfolio_binding: {}
  evaluation_binding: {}
  selection_status:
  retained_options: []
  pareto_axes: []
  non_dominated_option_ids: []
  rejected_options: []
  not_assessable_options: []
  no_defensible_tiers: []
  conflicts: []
  dissent: []
  source_level_fatal_findings: []
  target_requirements_status:
  unresolved_issues: []
  next_human_actions: []
```

An option is non-dominated only when no other retained option is no worse on every comparable declared axis and strictly better on at least one. Keep qualitative values when the evaluator did not provide comparable ordered values; do not fabricate numeric scores.
