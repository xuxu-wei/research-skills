---
name: proposal-context-brief-builder
description: "Normalize an idea, package, draft, funding call, or data opportunity into a proposal context brief with constraints and open facts."
---
# proposal-context-brief-builder

## Role

Normalize supplied proposal context for readiness triage and drafting. Do not decide readiness, evaluate quality, retrieve evidence, or draft proposal prose.

## Procedure

1. Classify all applicable input types: raw/promoted idea, funding call, practical problem, data/literature/method opportunity, existing draft, or constraint-led request.
2. Extract domain, working title, question/objective, population/system/data object, intervention/exposure/predictor/comparison, endpoints/metrics/deliverables, design/method, available/required data, output, goal, and constraints.
3. Separate confirmed facts, lightweight assumptions, critical unknowns, and non-critical unknowns. Never promote an assumption to fact.
4. Record target format, scope boundaries, available/unavailable data, method preferences/prohibitions, sample/cohort limits, time/resources/access/collaboration, and funder/journal requirements.
5. Record `sap_requested: false` unless the user or target output explicitly requires an SAP.
6. Produce a concise structured brief that lets `proposal-readiness-triage` judge clarity, drafting readiness, clarification needs, idea-refinement route, method concerns, and SAP branch without making those decisions here.

## Output Contract

```yaml
proposal_context_brief:
  input_types: []
  normalized_idea_summary:
  user_goal:
  target_output:
  research_question_or_objective:
  population_system_or_data_object:
  endpoints_metrics_or_deliverables: []
  design_or_methods: []
  available_data: []
  constraints: []
  confirmed_facts: []
  assumptions: []
  critical_unknowns: []
  noncritical_unknowns: []
  sap_requested: false
  source_notes: []
```

Return only the brief, unresolved input gaps, and its artifact pointer; do not return a readiness verdict or long background review.

## Stop Rules

Stop only when no research direction can be extracted, the request is unrelated to a proposal, or even a minimal idea summary is impossible. Otherwise preserve gaps as critical unknowns.

## Conditional Resources

- Read `references/accepted-input-types.md` when classifying mixed inputs.
- Read `references/fields-context-brief.md` when extracting and naming fields.
- Read `references/schema-proposal-context-brief.md` when validating the output.
- Use `templates/template-proposal-context-brief.md` when writing the brief artifact.

## Completion Check

Confirm input types, goal/output, question/object, data and method facts, constraints, facts/assumptions/unknowns separation, explicit SAP status, concise handoff, and no readiness or quality decision.
