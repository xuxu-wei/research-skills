# Research-Idea Artifact Contracts

This is the canonical contract for artifacts passed between `research-idea` skills.

## Global Rules

- Every machine-readable artifact should include `schema_version`, `source_skill`, `created_round`, and `artifact_id`.
- Use Markdown for user-facing deliverables and YAML only for agent-to-agent state transfer.
- Use `unknown`, `unclear`, `not_specified`, or `not_applicable` instead of inventing facts.
- Use the same identifiers across artifacts: `idea_id`, `opportunity_id`, `evaluation_id`, `preflight_id`, and `lineage_id`.
- Canonical `idea_id` values must follow `references/idea-id-and-lineage-rules.md`.
- Store workflow artifacts in the user's project directory, not inside the skill package.

## Research Context Brief

```yaml
research_context_brief:
  schema_version: "research-idea.v1"
  artifact_id: "context-001"
  source_skill: "research-context-builder"
  created_round: 1
  input_type: broad_direction | raw_idea | clinical_problem | practical_problem | data_asset | method_asset | funding_call | literature_material | mixed_input | unclear
  research_domain: ""
  user_goal: ""
  intended_output: paper | grant | protocol | pilot_study | long_term_program | internal_decision | unspecified
  target_audience_or_reviewer: ""
  study_object: ""
  setting_or_context: ""
  available_data:
    summary: ""
    access_status: available | likely_available | uncertain | unavailable | not_specified
    limitations: []
  available_methods:
    summary: ""
    maturity: established | emerging | speculative | not_specified
  endpoint_or_metric:
    known_items: []
    status: clear | partially_clear | unclear | not_applicable
    notes: ""
  constraints:
    time: ""
    resources: ""
    ethics_or_regulatory: ""
    collaboration: ""
  risk_preference: low | medium | high | unspecified
  evidence_materials_provided:
    status: yes | no | unclear
    material_types: []
    notes: ""
  known_facts: []
  assumptions: []
  uncertainties: []
  proceed_status: proceed | proceed_with_assumptions | clarification_stop
  downstream_needs:
    evidence_opportunity_mapping: required | optional | not_needed
    multi_path_idea_generation: required | optional | not_needed
    methodology_statistics_preflight: required | optional | not_needed
    isolated_independent_evaluation: required | optional | not_needed
    proposal_orchestrator_triage: required | optional | not_needed
```

## Evidence and Opportunity Artifacts

`research-opportunity-mapper` owns these artifacts. The research-idea workflow consumes their summaries and limitations.

```yaml
evidence_packet:
  schema_version: "research-idea.v1"
  artifact_id: "evidence-001"
  source_skill: "research-opportunity-mapper"
  created_round: 1
  evidence_status: user_provided | auto_retrieved | mixed | skipped | not_verified
  evidence_map_ref: ""
  opportunity_map_ref: ""
  evidence_limitations_ref: ""
  handoff_notes_ref: ""
  source_types: []
  core_findings: []
  limitations: []
  manual_verification_needed: []

opportunity:
  opportunity_id: "O001"
  type: gap | value | method | data | metric | failure | theory | benchmark | taxonomy | implementation | other
  description: ""
  supporting_evidence_ids: []
  evidence_confidence: high | moderate | low | speculative | not_verified
  why_it_matters: ""
  feasibility_concerns: ""
  novelty_risk: low | medium | high | unverified
  guideline_alignment: aligned | partially_aligned | conflicting | not_applicable | unverified
  recommended_generation_paths: []
```

## Candidate Idea

```yaml
idea:
  schema_version: "research-idea.v1"
  idea_id: "I01-001"
  previous_ids: []
  source_skill: "multi-path-idea-generator"
  created_round: 1
  origin_round: 1
  revision_round: 0
  status: draft | promoted | revise | reframe | merge | reject | backup | evaluation_failed
  title: ""
  one_sentence_summary: ""
  research_question: ""
  hypothesis_or_objective: ""
  endpoint_or_metric: ""
  data_source_or_evidence_base: ""
  minimal_experiment_or_analysis: ""
  value_claim: ""
  novelty_claim:
    text: ""
    confidence: high | moderate | low | speculative | unverified
  supporting_opportunity_ids: []
  generation_paths: []
  assumptions_and_uncertainties: []
  risks_or_objections: []
  lineage:
    lineage_id: "L-I01-001"
    parent_idea_ids: []
    variant_type: original | expanded | refined | merged | reframed | salvaged
    changes_from_parent: []
```

## Methodology-Statistics Preflight

```yaml
methodology_statistics_preflight:
  schema_version: "research-idea.v1"
  preflight_id: "P001"
  source_skill: "methodology-statistics-preflight"
  created_round: 1
  idea_id: "I01-001"
  endpoint_or_metric_status: clear | partially_clear | unclear | invalid | not_applicable
  data_method_fit: strong | acceptable | weak | invalid | not_applicable
  minimal_analysis_route_status: clear | partially_clear | unclear | invalid
  main_methodological_risks: []
  feasibility_blockers: []
  recommendation: pass | revise_endpoint_or_metric | revise_data_source | revise_method | revise_analysis_route | needs_clarification | blocked | out_of_scope
  repair_directions: []
```

## Idea Evaluation

```yaml
idea_evaluation:
  schema_version: "research-idea.v1"
  evaluation_id: "E001"
  source_skill: "idea-evaluator"
  created_round: 1
  idea_id: "I01-001"
  independence_status: valid | invalid
  evaluator_generation_involvement: none | generated | revised | unknown
  input_sufficiency_status: sufficient | insufficient
  dimension_scores:
    novelty: 0
    feasibility: 0
    impact: 0
    relevance: 0
    clarity: 0
    completion: 0
  overall_score_simple_average: 0
  hard_gate_status: pass | fail
  failed_gates: []
  fatal_or_unfixable_flaws: []
  reviewer_objections: []
  recommendation: promote | revise_then_promote | revise | reframe | merge | keep_as_backup | reject
  targeted_repair_direction: ""
  suggested_next_skill: ""
  evaluation_limitations: []
```

## Lineage Record

```yaml
idea_lineage_record:
  schema_version: "research-idea.v1"
  lineage_id: "L-I01-001"
  idea_id: "I01-001"
  parent_idea_ids: []
  generation_paths: []
  variant_type: original | expanded | refined | merged | reframed | salvaged | backup
  changes_from_parent: []
  evaluation_delta:
    previous_overall: null
    current_overall: null
    delta: null
  decision_history:
    - round: 1
      decision: draft | promote | revise | reframe | merge | reject | backup
      reason: ""
```

## Portfolio Package

```yaml
promoted_idea_package:
  schema_version: "research-idea.v1"
  artifact_id: "portfolio-package-001"
  source_skill: "idea-portfolio-assembler"
  created_round: 1
  idea_id: "I01-001"
  title: ""
  research_question: ""
  hypothesis_or_objective: ""
  endpoint_or_metric: ""
  data_source_or_evidence_base: ""
  minimal_experiment_or_analysis: ""
  value_claim: ""
  novelty_claim: ""
  evidence_summary: ""
  evidence_limitations: []
  evaluation_summary: ""
  hard_gate_status: pass | fail
  main_risks_or_reviewer_objections: []
  proposal_handoff_status: ready | conditional | not_ready
  remaining_uncertainties: []
```
