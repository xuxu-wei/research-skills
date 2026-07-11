# Handoff Validation

Use these checks before passing artifacts between research-idea skills.

## Context Builder to Mapper or Generator

- `user_goal`, `intended_output`, `research_domain`, and `proceed_status` are present.
- Data, method, and endpoint fields use explicit unknown values when missing.
- Assumptions and uncertainties are separated from confirmed facts.

## Mapper to Generator or Evaluator

- Evidence Map and Opportunity Map are present, or absence is explicitly justified.
- Evidence limitations are attached when evidence confidence is not high.
- Clinical or guideline-related claims are marked `unverified` unless current evidence exists.

## Generator to Preflight or Evaluator

- Each idea has `idea_id`, research question, endpoint/metric, data source or evidence base, minimal route, value claim, novelty claim, supporting opportunity IDs, generation path, risks, assumptions, and lineage.
- Each `idea_id` has been normalized to the canonical format in `idea-id-and-lineage-rules.md`; provisional generator IDs are recorded in `previous_ids`.
- The generator has not scored, ranked, promoted, or rejected the idea.

## Preflight to Evaluator

- Endpoint/metric status, data-method fit, minimal analysis route status, blockers, and repair directions are present.
- Preflight has not assigned novelty, impact, or overall idea quality scores.

## Evaluator to Orchestrator

- Independence status is `valid`.
- Six dimension scores, simple average, hard gate status, failed gates, fatal flaws, reviewer objections, recommendation, repair direction, and suggested next skill are present.
- The evaluator did not rewrite or generate a replacement idea.

## Orchestrator to Portfolio Assembler

- Every displayed candidate has an independent evaluation report.
- Revised, merged, reframed, or salvaged ideas have lineage records.
- Proposal handoff status is available for any idea recommended for downstream proposal workflow.
- Any idea marked `proposal_handoff_status: ready` or `conditional` has a pre-handoff adversarial review summary and no unresolved blocking objection.
- Contradictions between evaluator recommendation and orchestrator decision are resolved or explicitly marked.
