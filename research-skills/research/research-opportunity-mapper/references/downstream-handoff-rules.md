# Downstream Handoff Rules

Use this file to prepare outputs for downstream skills.

## To multi-path-idea-generator

Provide opportunity map, opportunity types, recommended generation paths, novelty risk, evidence limitations, and constraints relevant to generation.

Do not provide scores or promote/reject decisions.

## To methodology-statistics-preflight

Provide endpoint or metric concerns, data source concerns, method fit concerns, feasibility concerns, and evidence limitations affecting analysis design.

## To isolated idea-evaluator

Provide evidence summary, claim support status, evidence confidence, novelty verification, guideline alignment when applicable, and evidence limitations.

The evaluator must be isolated and independent. The mapper must not score or decide.

## To proposal-context-brief-builder or proposal-orchestrator

Provide evidence summary, Opportunity Map, claim support status, novelty/gap verification, funding-call or guideline alignment when applicable, source limitations, and reuse decision.

If the current input is a raw proposal request without evidence, recommend proposal readiness triage only after the evidence limitations and key opportunity claims are explicit.

Do not draft proposal aims, methods text, or review decisions.

## To proposal-evaluator

Provide evidence summary, supported and unsupported claims, reviewer-facing evidence risks, novelty/gap verification status, and source limitations.

The evaluator must remain independent. The mapper must not decide accept/revise/reject.

## To idea-portfolio-assembler

Provide evidence map reference, opportunity map reference, remaining uncertainties, source limitations, and source verification log when emitted.
