# Downstream Handoff Rules

Use this file to decide where the preflight report should go next.

## Handoff Decisions

- `pass` → proceed to the downstream task that requested preflight.
- `revise_endpoint_or_metric` → return to idea refinement, proposal drafting, measurement refinement, or user clarification.
- `revise_data_source` → return to data opportunity mapping, proposal drafting, SAP preparation, or user clarification.
- `revise_method` → return to method refinement, proposal drafting, protocol planning, or user clarification.
- `revise_analysis_route` → return to method/statistical planning or SAP preparation.
- `needs_clarification` → ask user for the smallest set of required missing facts.
- `blocked` → stop the current workflow or require major redesign.
- `out_of_scope` → route to the appropriate writing, evaluation, literature, or review skill.

## Suggested Skill Handoffs

- Idea-level quality judgment → `idea-evaluator`.
- Proposal readiness or drafting → `proposal-orchestrator` or `proposal-drafter`.
- Proposal quality evaluation → `proposal-evaluator`.
- SAP writing → `sap-writer`, only after preflight passes.
- SAP evaluation → `sap-evaluator`.
- Multi-reviewer assessment → `proposal-review-panel`.
- User clarification → upstream orchestrator.

## Isolation Requirement

The agent performing this preflight should not also perform the downstream evaluator role for the same artifact. Evaluation and review tasks must remain isolated.

## Idea-specific handoff

For an Idea, preserve the general preflight decision above and add:

- `proceed`: no required methodological repair remains;
- `proceed_with_assumptions`: a minimal viable route exists and the scientific
  writer may write under every explicitly recorded bounded assumption;
- `clarification_stop`: an unresolved detail crosses the boundary in
  `working-assumption-rules.md` and must not be guessed.

The writer records each accepted working assumption once in the dossier's
authoritative assumptions section. It remains a research risk, not an
established fact. A false assumption that would invalidate the core route must
not be handed off as `proceed_with_assumptions`.
