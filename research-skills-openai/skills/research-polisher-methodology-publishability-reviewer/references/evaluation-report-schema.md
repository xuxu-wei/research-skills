# Evaluation report schema

```yaml
research_polisher_evaluation_report:
  artifact_id:
  version:
  plugin_version:
  source_skill: research-polisher-methodology-publishability-reviewer
  based_on: []
  review_id:
  reviewer_skill: research-polisher-methodology-publishability-reviewer
  reviewer_instance_id:
  workflow_id:
  round_id:
  input_artifact_ids: []
  input_versions: []
  input_digests: []
  files_read: []
  review_scope:
  scope_limitations: []
  isolation_mode: fresh_subagent
  raw_strategy_reports_visible: false
  sealed_provenance_visible: false
  strategist_identities_visible: false
  prior_scores_visible: false
  source_edits_performed: false
  portfolio_binding:
    artifact_id:
    version:
    sha256:
  dossier_binding:
    artifact_id:
    version:
    sha256:
  target_requirements:
    status: verified | target_requirements_unverified | not_applicable
    adapter_id:
    version:
    sha256:
    checked_at:
  option_decisions: []
  cross_option_findings: []
  source_level_fatal_findings: []
  specialist_review_requests: []
  pareto_axis_values: []
  unresolved_issues: []
  decision:
```

Each option decision contains:

```yaml
option_decision:
  option_id:
  effort_tier:
  decision: retain | revise | reject | not_assessable
  method_design_compatibility:
  evidence_claim_fit:
  tier_correctness:
  feasibility:
  scientific_significance_potential:
  practical_value_potential:
  dissemination_potential:
  narrative_differentiation:
  publication_positioning:
  target_fit: verified_assessment | not_assessed
  fatal_findings: []
  major_findings: []
  required_repairs: []
  unresolved_issues: []
```

The overall decision must be mechanically consistent: a source-level fatal finding forbids `ready_for_human_selection`; a retained option is required for that state; and a revised portfolio always requires a new reviewer instance and report.
