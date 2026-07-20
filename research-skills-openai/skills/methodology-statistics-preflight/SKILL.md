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

1. **Confirm scope**：ensure the task is methodology/statistics preflight, not writing or full evaluation.
2. **Check minimum information**：question/object, endpoint/metric, data route, and method/design/analysis route.
3. **Assess endpoint/metric**：clarity, measurability, alignment with question, and support by data/conditions.
4. **Assess data-method fit**：whether data, variables, labels, measurements, sample, timing, or controls can support the method.
5. **Assess minimal analysis route**：whether at least one executable route exists without expanding into a full SAP.
6. **Apply domain checks selectively**：clinical/observational, prediction/ML, experiment, benchmark, methods study, qualitative/mixed methods.
7. **Identify blockers and repairs**：state blockers, repair directions, and downstream handoff.

## Outputs

Before writing the output, classify each actionable uncertainty as a
`required_repair`, `working_assumption`, or `nonblocking_advice`. For Idea
workflows, apply `references/working-assumption-rules.md` and assign a separate
Idea handoff decision.

Default output: **Methodology-Statistics Preflight Report** with:

- decision;
- endpoint/metric status;
- data-method fit status;
- minimal analysis route status;
- feasibility blockers;
- repair directions;
- downstream handoff.

For Idea inputs, also report `idea_handoff_decision` as `proceed`,
`proceed_with_assumptions`, or `clarification_stop`, plus structured working
assumptions when applicable. This does not replace the general preflight
decision used by other workflows.

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

本 skill 本身应由 `research-idea-orchestrator` 或 `proposal-orchestrator`
显式派发到新的独立子代理执行。

执行期间不得再调用 idea-evaluator、proposal-drafter、sap-writer 或其他 evaluator 共同判断。

子 agent 必须接收完整任务上下文（idea、context brief、evidence/opportunity map、
endpoint/metric、data route、method）——不得依赖父会话隐含上下文。

若发现需要修订，应返回 preflight report，由 orchestrator 决定是否进入 revision loop。

## References

- Read `references/working-assumption-rules.md` for Idea findings that might
  proceed under an explicit, testable assumption.

- Read `references/preflight-schema.md` when its named guidance or contract applies: ：定义 preflight report 的结构字段、评估维度和输出格式。
- Read `references/endpoint-metric-checks.md` when its named guidance or contract applies: ：规范 endpoint、outcome 和 metric 的清晰度、可测量性和与 study design 对齐的检查规则。
- Read `references/data-method-fit-rules.md` when its named guidance or contract applies: ：定义数据特征与统计/实验方法匹配度的检查规则。
- Read `references/minimal-analysis-route-rules.md` when its named guidance or contract applies: ：定义在资源或数据受限条件下最小可行分析路径的评估规则。
- Read `references/feasibility-blockers.md` when its named guidance or contract applies: ：定义样本量、数据可得性和资源等维度的可行性阻断检查。
- Read `references/domain-specific-checks.md` when its named guidance or contract applies: ：按领域（临床、ML/工程、观察性研究、benchmark 等）分类的专项检查规则。
- Read `references/downstream-handoff-rules.md` when its named guidance or contract applies: ：定义 preflight report 如何交给下游 skill 及 handoff 材料要求。
- Use `templates/template-methodology-statistics-preflight-report.md` when producing its named artifact: ：Methodology-Statistics Preflight Report 的输出模板。
- Use `templates/template-preflight-failure-report.md` when producing its named artifact: ：preflight 检查失败时的输出报告模板。
