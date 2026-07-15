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

- Each Idea is a complete `idea-snapshot-vNNN.md` with all twelve sections required by `idea-artifact-lifecycle.md`; no patch or delta is registered as the current artifact.
- `node.yaml` and the candidate-set index bind its exact path, version, digest, identity anchor, and lineage.
- Each `idea_id` has been normalized to the canonical format in `idea-id-and-lineage-rules.md`; provisional generator IDs are recorded in `previous_ids`.
- The generator has not scored, ranked, promoted, or rejected the idea.

## Preflight to Evaluator

- Endpoint/metric status, data-method fit, minimal analysis route status, blockers, and repair directions are present.
- Preflight has not assigned novelty, impact, or overall idea quality scores.

## Evaluator to Orchestrator

- Independence status is `valid`.
- The report binds the current snapshot digest, confirms a complete snapshot, reports identity drift, and records `prior_versions_visible: false` and `revision_delta_visible: false`.
- Six dimension scores, simple average, hard gate status, failed gates, fatal flaws, reviewer objections, recommendation, repair direction, and suggested next skill are present.
- The evaluator did not rewrite or generate a replacement idea.

## Orchestrator to Portfolio Assembler

- Every displayed candidate has a complete current snapshot and a qualifying independent evaluation of the same digest.
- Revised, merged, reframed, or salvaged ideas have lineage records.
- The portfolio carries the complete snapshot sections; change history remains subordinate and cannot replace the current Idea.
- Proposal handoff status is available for any idea recommended for downstream proposal workflow.
- Any idea marked `proposal_handoff_status: ready` or `conditional` has a pre-handoff adversarial review summary and no unresolved blocking objection.
- Contradictions between evaluator recommendation and orchestrator decision are resolved or explicitly marked.
