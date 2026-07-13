# Strategy report schema

```yaml
research_polisher_strategy_report:
  artifact_id:
  version:
  plugin_version:
  source_skill: research-polisher-strategy-reviewer
  based_on: []
  review_id:
  reviewer_skill: research-polisher-strategy-reviewer
  reviewer_instance_id:
  workflow_id:
  round_id:
  review_perspective: scientific_significance | practical_value | dissemination_editorial
  input_artifact_ids: []
  input_versions: []
  input_digests: []
  files_read: []
  review_scope:
  scope_limitations: []
  isolation_mode: fresh_subagent
  peer_outputs_visible: false
  prior_scores_visible: false
  source_edits_performed: false
  existing_contribution:
  evidence_ceiling:
  strategy_options: []
  cross_tier_conflicts: []
  unresolved_issues: []
  decision:
```

`strategy_options` contains exactly one record for each required tier. A proposed record is:

```yaml
strategy_option:
  provisional_option_id:
  effort_tier:
  status: proposed
  feasibility: certain | high
  plan:
    proposed_repositioning:
    value_mechanism:
    scientific_significance_delta:
    practical_value_delta:
    dissemination_impact_delta:
    story_arc:
    target_audiences: []
    outlet_archetypes: []
    claim_delta: []
    existing_evidence_ids: []
    evidence_dependencies: []
    added_work_items: []
    feasibility_basis:
    dependencies:
      data: []
      resources: []
      technical: []
      time: []
    incompatible_with: []
    risks: []
    unknowns: []
    fallback:
    stop_condition:
    target_requirements_status: verified | target_requirements_unverified | not_applicable
```

or:

```yaml
strategy_option:
  effort_tier:
  status: no_defensible_option
  reason:
  plan: null
  missing_or_infeasible_dependencies: []
  clarification_needed: []
```

For `reposition_only`, `added_work_items` must be an empty list and every `claim_delta` must be a wording, emphasis, audience, or scope change supported by an existing evidence ID.
