# Proposal Drafter Handoffs

Return only the handoff for the active mode and artifact pointers, not drafting logs.

## Required inputs by mode

- `background_path_options`: approved context/readiness; goal/output; evidence/limits; structure/call; reader, gap, source-intent, constraints, research-content/route/key-problem map; target options reference.
- `planning_only`: the same approved foundations; target plan/proposal references; frozen user selection or explicit/binding path authority.
- `write_full_proposal`: frozen v2 content plan; context/reader fields; allowed facts/evidence; binding structure/call; target proposal identity; all applicable instance IDs.
- `scientific_revision`: current/target proposal identities, controller repair plan, allowed facts/evidence, and constraints.
- `editorial_repair`: only normalized repair brief, current complete proposal, and protected-content register.
- `formatting_only`: current complete proposal, binding format, and target identity.

Stop with an input-gap report when required facts, context, readiness, or authority are missing. Never invent data, endpoints, sample size, evidence, feasibility, or user resources.

## Candidate background paths

```yaml
background_path_options_handoff:
  source_skill: proposal-drafter
  mode: background_path_options
  candidate_planner_instance_id:
  options_artifact_id:
  options_path: 04_drafts/proposal-background-path-options-vNNN.yaml
  options_version:
  option_count: 2 | 3
  recommendation: null
  ranking: null
  selection_status: human_background_path_selection_required
  next_route: user_background_path_selection
```

When only one route is defensible, return a clarification stop with `options_artifact_id: null`, `next_route: user_acceptance_or_additional_organizing_constraint`, and a normalized `sole_path_candidate` containing `primary_mode`, `organizing_axis`, `one_sentence_argument_logic`, opening, current-status units, mappings, synthesis, and evidence requirements. This handoff is not formal-planning authority. If the user accepts it, the orchestrator copies that exact outline into a frozen `proposal-background-path-selection.v1` artifact with `selection_mode: sole_path_acceptance`, `options_ref: null`, and `user_authorization_text` preserving the user's acceptance before dispatching the formal planner.

## Formal content planning

```yaml
planning_handoff:
  source_skill: proposal-drafter
  mode: planning_only
  planner_instance_id:
  candidate_planner_instance_id:
  content_plan_artifact_id:
  content_plan_path: 04_drafts/proposal-content-plan-vNNN.yaml
  content_plan_version:
  content_plan_schema: proposal-content-plan.v2
  background_selection_source: user | user_explicit | binding_constraint
  background_selection_mode: option_selection | sole_path_acceptance | bypass
  user_authorization_text:
  selected_path_ref:
  based_on: []
  binding_constraints_covered: []
  unresolved_inputs: []
  next_route: write_full_proposal
```

## Writing and revision

```yaml
draft_handoff:
  source_skill: proposal-drafter
  mode: write_full_proposal | scientific_revision | editorial_repair | formatting_only
  writer_instance_id:
  candidate_planner_instance_id:
  planner_instance_id:
  content_plan_path:
  proposal_artifact_id:
  proposal_file_path:
  proposal_version:
  based_on: []
  change_type: initial | substantive | structural | editorial_only | formatting_only
  response_to_reviewers_path:
  editorial_action_execution_path:
  change_summary: []
  assumptions: []
  unresolved_issues: []
  next_route: scientific_evaluation | editorial_action_validation | re-evaluation | final_evaluation
```
