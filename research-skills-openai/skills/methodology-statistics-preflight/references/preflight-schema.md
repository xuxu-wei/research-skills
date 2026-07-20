# Preflight Report Schema

This file defines the required structure for a Methodology-Statistics Preflight Report. It is a documentation schema, not executable code.

## Required Fields

- `preflight_subject`: concise description of the evaluated idea, proposal, protocol, SAP draft, design, benchmark, or analysis plan.
- `input_type`: one of `idea`, `proposal`, `protocol`, `sap_draft`, `study_design`, `experiment`, `benchmark`, `analysis_plan`, `mixed`, `unclear`.
- `downstream_task`: intended next step, such as `idea_evaluation`, `proposal_drafting`, `sap_writing`, `sap_evaluation`, `protocol_review`, `panel_review`, `user_clarification`.
- `preflight_decision`: one of:
  - `pass`
  - `revise_endpoint_or_metric`
  - `revise_data_source`
  - `revise_method`
  - `revise_analysis_route`
  - `needs_clarification`
  - `blocked`
  - `out_of_scope`
- `decision_rationale`: brief explanation for the decision.
- `endpoint_metric_status`: status and comments on endpoint / metric / benchmark clarity.
- `data_method_fit_status`: status and comments on whether the data can support the proposed design or method.
- `minimal_analysis_route_status`: whether a minimal route exists, is unclear, or is absent.
- `feasibility_blockers`: list of blockers or `none_identified`.
- `repair_directions`: practical, minimal repair actions.
- `handoff_recommendation`: recommended next workflow or skill.
- `limitations`: uncertainty and missing information affecting the preflight.
- `handoff_decision`: `proceed`, `proceed_with_assumptions`, or
  `clarification_stop` for every input type;
- `finding_class` on every actionable finding: `required_repair`,
  `working_assumption`, or `nonblocking_advice`;
- `working_assumptions`: an empty list unless the handoff is
  `proceed_with_assumptions`; each item follows `working-assumption-rules.md`.

`proceed_with_assumptions` requires at least one specific accepted working assumption.
Each must be recorded once in the downstream artifact's authoritative `Assumptions`
location. Generic unresolved-detail language is invalid.

## Status Values

Use short status labels when helpful:

- `adequate`
- `partially_adequate`
- `unclear`
- `inadequate`
- `not_applicable`

## Boundary Rules

The report must not include:

- Novelty score or novelty judgment;
- Impact score or impact judgment;
- overall research value score;
- accept / reject funding recommendation;
- full SAP;
- full proposal;
- full protocol;
- generated statistical code.
