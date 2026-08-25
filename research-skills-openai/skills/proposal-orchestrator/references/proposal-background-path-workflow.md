# Proposal Background Path Workflow

## Default candidate route

After readiness, enter planning and launch a fresh `proposal-drafter` in `background_path_options` mode. It may write only `04_drafts/proposal-background-path-options-vNNN.yaml`. Require two or three materially distinct, evidence-supportable options, `recommendation: null`, `ranking: null`, and `selection_status: human_background_path_selection_required`. Do not manufacture alternatives when only one is defensible; return the smallest request asking the user to accept the sole path or add an organizing constraint, together with a normalized functional outline of that sole path. Do not freeze a valid options artifact for this case.

Report each option's ID, mode, one-sentence logic, evidence burden, strengths, tradeoffs, and loss-of-focus risk neutrally. Do not order or recommend. Set workflow state to `human_background_path_selection_required` and stop. In the user-facing summary, describe this pause in natural language rather than exposing the machine state value.

Skip this route only when the user has explicitly fixed the background/current-status path or a binding funder structure removes all meaningful structural freedom. The formal content plan then records `selection_source: user_explicit | binding_constraint`, `selection_mode: bypass`, the selected logical path reference, and the user's exact authorization text when the source is `user_explicit`.

## Human selection and recovery

After a user selects an option, the orchestrator writes `04_drafts/proposal-background-path-selection-vNNN.yaml` from `../templates/template-proposal-background-path-selection.yaml`. Record the selected option, local modifications, rejected options, `selection_source: user`, and the exact logical options reference/version. The reference must resolve to the frozen options artifact, and the selected option ID must occur exactly once in it. The later v2 plan points `selected_path_ref` to this frozen selection artifact and preserves the authorization text exactly.

If the candidate planner found only one defensible path and the user accepts it, the orchestrator writes the same selection artifact with `selection_mode: sole_path_acceptance`, `selected_option_id: null`, `options_ref: null`, and `accepted_sole_path` copied from the normalized clarification handoff. Preserve the user's exact authorization in `user_authorization_text` and record any local modifications. The frozen selection artifact itself is the selected-path authority; the v2 content plan points `selected_path_ref` to that artifact. The clarification handoff alone is never planning authority.

- A selected option with local modifications proceeds to formal planning.
- If the user rejects all options, obtain the smallest new organizing constraint and start a new candidate round.
- If the user requests a hybrid, start a new candidate round that tests the combined path end to end. Never concatenate options directly for planning or writing.

## Formal plan and writer separation

After option selection, sole-path acceptance, or an explicit/binding bypass, launch a new `proposal-drafter` in `planning_only` mode. It writes only `proposal-content-plan.v2` at `04_drafts/proposal-content-plan-vNNN.yaml`, including `background_argumentation`, selected-path authority, the applicable user authorization text, reader chain, source intents, binding constraints, and section functions/handoffs, then stops.

A third fresh `proposal-drafter` writes one complete proposal. Candidate planner, formal planner, and writer IDs must be pairwise distinct. New full proposals cannot use v1. If a v1 plan has not yet produced prose, replace it through a fresh v2 planner. Targeted revision of an existing drafted proposal does not require migration.
