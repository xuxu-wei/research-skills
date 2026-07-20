# fields-context-brief

Purpose: define the fields that should appear in a proposal context brief.

Keep the brief concise. Mark absent or uncertain fields as `unknown`; do not invent details.

## Required Fields

- `brief_id`: short identifier if available; otherwise assign a simple working identifier.
- `input_types`: one or more accepted input types.
- `source_summary`: where the idea came from, such as user input, promoted idea package, funding call, data opportunity, clinical problem, or literature summary.
- `normalized_idea_summary`: concise restatement of the idea without upgrading vague claims into mature research questions.
- `research_domain`: field, discipline, clinical area, technical area, or application domain.
- `working_title`: optional short title if directly inferable.
- `research_question_or_objective`: known question or objective; use `unknown` if absent.
- `hypothesis_or_value_claim`: hypothesis, expected contribution, or practical value claim if present.
- `target_population_or_study_object`: population, system, dataset, tissue, model, organization, technology, or phenomenon under study.
- `exposure_intervention_predictor_or_comparison`: relevant exposure, intervention, predictor, comparator, or contrast if applicable.
- `endpoint_outcome_metric_or_deliverable`: endpoint, outcome, metric, benchmark, artifact, or deliverable if stated.
- `available_data_or_materials`: datasets, cohorts, documents, instruments, infrastructure, specimens, software, or access rights already available.
- `required_data_or_materials`: data or resources required but not confirmed.
- `proposed_or_implied_methods`: study design, statistical approach, experimental method, computational method, qualitative method, or evaluation strategy if present.
- `intended_output`: paper, grant, protocol, pilot study, internal proposal, thesis chapter, product research, or unspecified.
- `user_goal`: what the user wants to accomplish with the proposal.
- `constraints`: known limits on time, resources, data access, collaborators, tools, methods, geography, sample, or target venue.
- `target_reader_profile`: the primary decision-maker or reviewer group and any secondary reader whose understanding materially affects success.
- `reader_prior_knowledge`: concepts, domain facts, and methods the target reader can reasonably be expected to know; use `unknown` when not supplied.
- `terms_requiring_definition`: specialized or cross-disciplinary terms that must be defined before the reader needs them, with the reason each term is unfamiliar or ambiguous.
- `reader_reasoning_chain`: ordered handoff from the reader's starting knowledge through the problem, current knowledge, gap, significance, and rationale for the proposed design.
- `gap_type`: one or more of `empirical`, `methodological`, `conceptual`, `translational`, `implementation`, `policy`, `evidence`, `mixed`, or `unknown`; do not infer a gap from topic breadth alone.
- `source_intent_coverage`: one record per supplied source or instruction, stating its intended use, relevant requirements, coverage status, and any unresolved interpretation.
- `binding_constraints`: non-negotiable source, call, user, source-bound compliance, format, scope, eligibility, or deliverable requirements. Keep preferences separate.
- `sap_requested`: true only if the user explicitly asks for SAP, SAP review, protocol/SAP output, or statistical analysis plan content.
- `confirmed_facts`: facts explicitly supplied by the user or source material.
- `reasonable_assumptions`: light organizational assumptions needed to prepare the brief; do not treat them as facts.
- `critical_unknowns`: missing information likely to affect readiness triage, drafting, methodology, feasibility, or SAP.
- `non_critical_unknowns`: missing information that can wait until later stages.
- `source_notes`: short notes on source quality, conflicting inputs, or materials used.
- `handoff_notes`: concise guidance for the next skill, usually `proposal-readiness-triage`.

## Field Rules

- Prefer short phrases over long prose.
- Preserve source intent at requirement level; a source being listed does not prove that its requirements are covered.
- Order the reader reasoning chain by dependency, not by the order in which source material arrived.
- Define only terms that burden the stated reader; do not create a general glossary.
- Do not add literature claims unless the user supplied them or a prior evidence summary exists.
- Do not resolve contradictions silently; list them in `source_notes`.
- Do not ask the user questions here unless no minimal idea summary can be formed.
- Do not make readiness decisions in this file or in the brief.
