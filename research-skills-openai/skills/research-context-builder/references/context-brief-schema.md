# Context Brief Schema

Use this object for `research-idea.v3` context normalization.

```yaml
research_context_brief:
  schema_version: research-idea.v3
  artifact_id:
  source_skill: research-context-builder
  created_round: 1
  input_type: problem
  problem_subtype: broad_direction | raw_idea | clinical_problem | practical_problem | data_asset | method_asset | funding_call | literature_material | mixed | unclear
  research_domain:
  user_goal:
  intended_output: paper | grant | protocol | pilot_study | long_term_program | internal_decision | unspecified
  target_audience_or_reviewer:
  target_reader_profile:
    disciplines: []
    intended_use:
  reader_prior_knowledge:
    assumed_known: []
    requires_first_use_explanation: []
  reader_reasoning_chain:
    background:
    current_state:
    gap:
    significance:
    rationale:
  gap_type: knowledge | evidence | theory | method | measurement | data | validation | implementation | mixed | unclear
  study_object:
  setting_or_context:
  available_data:
    summary:
    access_status: available | likely_available | uncertain | unavailable | not_specified
    limitations: []
  available_methods:
    summary:
    maturity: established | emerging | speculative | not_specified
  endpoint_or_metric:
    known_items: []
    status: clear | partially_clear | unclear | not_applicable
    notes:
  constraints: {time: "", resources: "", collaboration: ""}
  evidence_materials_provided: {status: unclear, material_types: [], notes: ""}
  known_facts: []
  assumptions: []
  uncertainties: []
  direction_clarity: clear | underdefined | ambiguous
  direction_clarity_rationale:
  proceed_status: proceed | proceed_with_assumptions | clarification_stop
  downstream_needs:
    evidence_opportunity_mapping: required | optional | not_needed
    idea_direction_routing: required | optional | not_needed
    idea_dossier_generation: required | optional | not_needed
    methodology_statistics_preflight: required | optional | not_needed
    isolated_independent_evaluation: required | optional | not_needed
    proposal_orchestrator_triage: required | optional | not_needed
```

A valid brief includes goal/output, domain, object when inferable, data and
endpoint status, a target-reader profile, prior-knowledge boundaries, all five
reader-reasoning functions, gap type, assumptions/uncertainties, direction
clarity with rationale, proceed status, and downstream needs. When proceeding,
each reasoning function must contain either usable context or an explicit
unresolved need; do not leave a silent blank. The chain describes what a reader
must understand. It does not establish scientific value or novelty.
