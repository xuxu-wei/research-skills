---
name: proposal-context-brief-builder
description: "Normalize proposal inputs, reader needs, source intent, constraints, and gaps."
---
# proposal-context-brief-builder

## Role

Normalize supplied proposal context for readiness triage, planning, and drafting. Capture what the intended reader must understand and every binding source requirement without deciding readiness, evaluating quality, retrieving evidence, or drafting proposal prose.

## Procedure

1. Classify all applicable input types: raw/promoted idea, funding call, practical problem, data/literature/method opportunity, existing draft, or constraint-led request.
2. Extract domain, working title, question/objective, population/system/data object, intervention/exposure/predictor/comparison, endpoints/metrics/deliverables, design/method, available/required data, output, goal, and constraints.
3. Record `target_reader_profile`, `reader_prior_knowledge`, `terms_requiring_definition`, and an ordered `reader_reasoning_chain` from the reader's entry point through problem, current knowledge, gap, significance, and design rationale. Mark unknowns rather than assuming expert knowledge.
4. Classify `gap_type` only from supplied material or a cited evidence map. Use `unknown` when the gap is not established; do not convert a topic into a gap.
5. Build `source_intent_coverage` for every supplied call, template, instruction, prior artifact, or user requirement. Record the intended use and whether coverage is confirmed, partial, not applicable, or unresolved. Record non-negotiable format, content, eligibility, scope, and deliverable requirements separately as `binding_constraints`.
6. Separate confirmed facts, lightweight assumptions, critical unknowns, and non-critical unknowns. Never promote an assumption to fact.
7. Record target format, scope boundaries, available/unavailable data, method preferences/prohibitions, sample/cohort limits, time/resources/access/collaboration, and funder/journal requirements.
8. Record `sap_requested: false` unless the user or target output explicitly requires an SAP.
9. Produce a concise structured brief that lets `proposal-readiness-triage` judge clarity, drafting readiness, clarification needs, idea-refinement route, method concerns, and SAP branch without making those decisions here.

## Output Contract

```yaml
proposal_context_brief:
  brief_id:
  input_types: []
  source_summary:
  normalized_idea_summary:
  research_domain:
  working_title:
  research_question_or_objective:
  hypothesis_or_value_claim:
  target_population_or_study_object:
  exposure_intervention_predictor_or_comparison:
  endpoint_outcome_metric_or_deliverable: []
  available_data_or_materials: []
  required_data_or_materials: []
  proposed_or_implied_methods: []
  intended_output:
  user_goal:
  constraints: []
  target_reader_profile:
  reader_prior_knowledge: []
  terms_requiring_definition: []
  reader_reasoning_chain: []
  gap_type: unknown
  source_intent_coverage: []
  binding_constraints: []
  confirmed_facts: []
  reasonable_assumptions: []
  critical_unknowns: []
  non_critical_unknowns: []
  sap_requested: false
  source_notes: []
  handoff_notes: []
```

Keep unresolved input gaps inside `critical_unknowns` or `non_critical_unknowns`. Return only the canonical brief and its artifact pointer; do not return a readiness verdict or long background review.

## Stop Rules

Stop only when no research direction can be extracted, the request is unrelated to a proposal, or even a minimal idea summary is impossible. Otherwise preserve gaps as critical unknowns.

## Conditional Resources

- Read `references/accepted-input-types.md` when classifying mixed inputs.
- Read `references/fields-context-brief.md` when extracting and naming fields.
- Read `references/schema-proposal-context-brief.md` when validating the output.
- Use `templates/template-proposal-context-brief.md` when writing the brief artifact.

## Completion Check

Confirm input types, goal/output, question/object, data and method facts, reader baseline and reasoning chain, gap type, complete source-intent coverage, binding constraints, facts/assumptions/unknowns separation, explicit SAP status, concise handoff, and no readiness or quality decision.
