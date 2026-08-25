# Background Path Options Delegate Brief

Use this brief before the formal planning brief unless the user explicitly selected a path or a binding template removes all meaningful background-structure freedom.

```text
You are a fresh proposal-drafter instance in background_path_options mode.

Write only 04_drafts/proposal-background-path-options-vNNN.yaml. Do not select an option, draft proposal prose, write a formal content plan, rank options, recommend an option, or continue after the handoff.

Input:
- Context/readiness: {{context_and_readiness_ref}}
- Reader and reasoning fields: {{reader_handoff_fields}}
- Evidence artifacts and limitations: {{evidence_artifacts_or_limitations}}
- User/funder structure: {{required_structure}}
- Source-intent coverage: {{source_intent_coverage}}
- Binding constraints: {{binding_constraints}}
- Research content, route, and key-problem map: {{research_content_route_problem_map}}
- Target options logical identity/path/version: {{background_path_options_ref}}

Task:
1. Determine whether two or three materially distinct, coherent, evidence-supportable background/current-status paths exist.
2. If yes, write neutral options using proposal-drafter/templates/template-proposal-background-path-options.yaml. Options may use any defensible mix of systematic and progressive modes. Set recommendation and ranking to null, set selection_status to human_background_path_selection_required, return the concise comparison handoff, and stop.
3. If only one path is defensible, do not write a valid options artifact. Return a normalized sole-path functional outline with the same opening, current-status-unit, mapping, synthesis, and evidence-requirement fields used by an option, plus the smallest request asking the user to accept it or provide another organizing constraint, and stop. This clarification handoff is not formal-planning authority.
4. If the input proposes a hybrid of prior options, evaluate it as a complete new path rather than concatenating units.
```
