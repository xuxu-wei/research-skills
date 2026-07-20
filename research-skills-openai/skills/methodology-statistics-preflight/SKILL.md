---
name: methodology-statistics-preflight
description: "Independently preflight a frozen research plan for endpoint, data-method, and feasibility problems."
---
# methodology-statistics-preflight

## Purpose

Use this skill when a research idea, proposal, protocol, SAP draft, benchmark, experiment, or analysis plan needs a methodology/statistics feasibility preflight before downstream evaluation, drafting, or SAP writing.

This skill only answers: is there a minimally viable endpoint/metric, data-method fit, and analysis route, and what needs repair?

It does not judge novelty, impact, fundability, publication value, or overall idea/proposal quality. It does not write proposal, SAP, protocol, or grant text.

## Inputs

Usually supplied by an orchestrator or user:

- research question, objective, hypothesis, or task;
- target population, system, dataset, sample, material, or study object;
- endpoint, outcome, metric, benchmark, or analysis target;
- available data or data acquisition route;
- proposed method, design, model, or analysis route;
- user constraints such as time, resources, data access, or collaboration;
- intended downstream task.

If the minimum information is missing, return clarification needs or failure; do not invent missing endpoint, data, variables, sample size, or method.

## Workflow

1. **Confirm scope**: ensure the task is methodology/statistics preflight, not writing or full evaluation.
2. **Check minimum information**: question/object, endpoint/metric, data route, and method/design/analysis route.
3. **Assess endpoint/metric**: clarity, measurability, alignment with question, and support by data/conditions.
4. **Assess data-method fit**: whether data, variables, labels, measurements, sample, timing, or controls can support the method.
5. **Assess minimal analysis route**: whether at least one executable route exists without expanding into a full SAP.
6. **Apply domain checks selectively**: clinical/observational, prediction/ML, experiment, benchmark, methods study, qualitative/mixed methods.
7. **Identify blockers and repairs**: state blockers, repair directions, and downstream handoff.

## Outputs

Before writing the output, classify each actionable uncertainty as a
`required_repair`, `working_assumption`, or `nonblocking_advice`. Apply
`references/working-assumption-rules.md` whenever any workflow might proceed under an
unconfirmed detail, and assign a generic handoff decision.

Default output: **Methodology-Statistics Preflight Report** with:

- decision;
- endpoint/metric status;
- data-method fit status;
- minimal analysis route status;
- feasibility blockers;
- repair directions;
- downstream handoff.

Every completed report also gives `handoff_decision` as `proceed`,
`proceed_with_assumptions`, or `clarification_stop`. This does not replace the
general preflight decision.

`proceed_with_assumptions` is valid only when the report explicitly and conditionally
accepts each specific bounded working assumption. Each assumption must be plausible,
verifiable at a named point, and non-identity-changing if false. The downstream writer
records it once in the artifact's authoritative `Assumptions` location and nowhere
else. Generic language such as "details will be resolved later" cannot support a
conditional pass.

Allowed decisions: `pass`, `revise_endpoint_or_metric`, `revise_data_source`, `revise_method`, `revise_analysis_route`, `needs_clarification`, `blocked`, `out_of_scope`.

Failure output: use the failure template when the input is out of scope or too incomplete for useful preflight.

Every report must include this provenance block:

```yaml
review_id:
reviewer_skill: methodology-statistics-preflight
reviewer_instance_id:
workflow_id:
round_id:
input_artifact_ids:
input_versions:
files_read:
isolation_mode: fresh_subagent
prior_scores_visible: false
source_edits_performed: false
decision:
findings:
unresolved_issues:
```

## Boundaries

- Do not score Novelty, Impact, Relevance, or overall value.
- Do not write a full SAP or protocol.
- Do not force clinical rules onto non-clinical work.
- Do not act as idea evaluator, proposal evaluator, SAP evaluator, proposal drafter, SAP writer, or review panel.

## Independent Execution Contract

- Run this skill only in a fresh independent subagent or delegated thread. Never perform the preflight in an agent context that generated or revised the same idea, proposal, protocol, SAP, or analysis plan.
- Receive frozen artifact IDs, file paths, and versions. Treat source artifacts as read-only and write only the Methodology-Statistics Preflight Report.
- Do not draft, rewrite, polish, repair, or directly modify the assessed artifacts.
- Do not use parent-thread hidden reasoning, expected conclusions, prior reviewer outputs, or prior scores. Report only evidence available in the frozen inputs.
- Report the exact files read, assessment scope, limitations, and independent reviewer instance identifier.
- If a fresh subagent cannot be created, return `independent_review_pending` with a self-contained continuation brief and stop. Never fall back to inline review.

## Delegation Rules

This skill must be explicitly delegated by the requesting upstream orchestrator to a
fresh independent subagent.

Do not call a downstream evaluator, drafter, or writer to co-decide the preflight.

The subagent must receive the complete frozen task context: current artifact, relevant
context and evidence, endpoint or metric, data route, method, and intended handoff. It
must not rely on hidden parent context.

If revision is needed, return the preflight report so the orchestrator can choose the next route.

## References

- Read `references/working-assumption-rules.md` for any finding that might
  proceed under an explicit, testable assumption.

- Read `references/preflight-schema.md` for the report fields and decision contract.
- Read `references/endpoint-metric-checks.md` for endpoint and metric checks.
- Read `references/data-method-fit-rules.md` for data-method compatibility checks.
- Read `references/minimal-analysis-route-rules.md` for the minimum viable route boundary.
- Read `references/feasibility-blockers.md` for feasibility blocking conditions.
- Read `references/domain-specific-checks.md` for selectively applied domain checks.
- Read `references/downstream-handoff-rules.md` for routing and handoff requirements.
- Use `templates/template-methodology-statistics-preflight-report.md` for a completed report.
- Use `templates/template-preflight-failure-report.md` when useful preflight cannot be completed.
