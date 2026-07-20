# schema-proposal-context-brief

Purpose: define the expected structure of a proposal context brief for downstream skills.

This is a structural guide, not executable code. Use it to keep outputs consistent and compact.

## Canonical Structure

The artifact has one root mapping, `proposal_context_brief`. Its child fields are:

- `brief_id`
- `input_types`
- `source_summary`
- `normalized_idea_summary`
- `research_domain`
- `working_title`
- `research_question_or_objective`
- `hypothesis_or_value_claim`
- `target_population_or_study_object`
- `exposure_intervention_predictor_or_comparison`
- `endpoint_outcome_metric_or_deliverable`
- `available_data_or_materials`
- `required_data_or_materials`
- `proposed_or_implied_methods`
- `intended_output`
- `user_goal`
- `constraints`
- `target_reader_profile`
- `reader_prior_knowledge`
- `terms_requiring_definition`
- `reader_reasoning_chain`
- `gap_type`
- `source_intent_coverage`
- `binding_constraints`
- `sap_requested`
- `confirmed_facts`
- `reasonable_assumptions`
- `critical_unknowns`
- `non_critical_unknowns`
- `source_notes`
- `handoff_notes`

## Value Conventions

Use `unknown` when a field is absent.

Use `not_applicable` only when a field is truly irrelevant to the input type.

Use concise lists for constraints, unknowns, facts, and assumptions.

Use ordered entries for `reader_reasoning_chain`. Each entry should name the reasoning function and the understanding handed to the next step.

Each `source_intent_coverage` record should contain `source_id`, `intent_or_requirement`, `coverage_status`, and `notes`. Use `confirmed`, `partial`, `not_applicable`, or `unresolved` for `coverage_status`.

Each `binding_constraints` record should contain `constraint_id`, `source_id`, `requirement`, and `applies_to`. Do not downgrade a binding requirement to a preference.

Use `sap_requested: true` only when the user explicitly asks for SAP, SAP review, protocol/SAP content, or statistical analysis plan content.

## Validation Checks

A valid brief should:

- identify at least one input type;
- include a normalized idea summary or state why one cannot be formed;
- clearly distinguish confirmed facts from assumptions;
- identify critical unknowns that may affect readiness triage;
- identify the target reader, reader baseline, terminology burden, and a complete ordered reader reasoning chain, or mark them unknown;
- state a supported gap type or `unknown`;
- account for every supplied source intent and preserve every binding constraint;
- record intended output and user goal when available;
- avoid final readiness, novelty, impact, or feasibility judgments.

## Invalid Patterns

- Treating assumptions as confirmed facts.
- Inventing endpoints, datasets, sample size, or methods.
- Returning a full proposal instead of a context brief.
- Performing readiness triage in the brief.
- Defaulting SAP to requested without explicit user instruction.
- Claiming source coverage merely because a source was named.
- Treating a reader preference as a binding requirement, or vice versa.
