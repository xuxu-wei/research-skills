# Context Brief Schema

This file defines the structured object produced by `research-context-builder`. The canonical shared contract is `research-idea-orchestrator/references/artifact-contracts.md`.

## Research Context Brief

```yaml
research_context_brief:
  schema_version: "research-idea.v2"
  artifact_id: "context-001"
  source_skill: "research-context-builder"
  created_round: 1
  input_type: broad_direction | raw_idea | clinical_problem | practical_problem | data_asset | method_asset | funding_call | literature_material | mixed_input | unclear
  research_domain: ""
  user_goal: ""
  intended_output: paper | grant | protocol | pilot_study | long_term_program | internal_decision | unspecified
  target_audience_or_reviewer: ""
  available_data:
    summary: ""
    access_status: available | likely_available | uncertain | unavailable | not_specified
    limitations: []
  available_methods:
    summary: ""
    maturity: established | emerging | speculative | not_specified
  study_object: ""
  setting_or_context: ""
  endpoint_or_metric:
    known_items: []
    status: clear | partially_clear | unclear | not_applicable
    notes: ""
  constraints:
    time: ""
    resources: ""
    collaboration: ""
  risk_preference: low | medium | high | unspecified
  evidence_materials_provided:
    status: yes | no | unclear
    material_types: []
    notes: ""
  known_facts: []
  assumptions:
    - assumption: ""
      confidence: high | medium | low
      impact_if_wrong: high | medium | low
      needs_user_confirmation: true | false
  uncertainties:
    - uncertainty: ""
      expected_downstream_impact: high | medium | low
      suggested_resolution: ""
  clarification_questions: []
  proceed_status: proceed | proceed_with_assumptions | clarification_stop
  downstream_needs:
    evidence_opportunity_mapping: required | optional | not_needed
    multi_path_idea_generation: required | optional | not_needed
    methodology_statistics_preflight: required | optional | not_needed
    isolated_independent_evaluation: required | optional | not_needed
    proposal_orchestrator_triage: required | optional | not_needed
```

## Minimal Valid Output

A valid Research Context Brief must include:

- `input_type`
- `research_domain`, even if marked unclear
- `user_goal`, even if marked unspecified
- `intended_output`
- `study_object`, if inferable
- `available_data` status
- `endpoint_or_metric` status
- `assumptions`
- `uncertainties`
- `proceed_status`
- `downstream_needs`

Use `unclear`, `unspecified`, or `not_specified` rather than inventing facts.
