---
name: idea-evaluator
description: "当候选 research idea 已完成 context、evidence/opportunity mapping、generation 和必要 preflight 后，需要由隔离、独立 evaluator 进行六维评分、hard gate 检查、fatal flaw 判断和 revise/reframe/merge/reject/promote 建议时使用。本 skill 只评价 idea，不生成 idea，不写 proposal，不替代 methodology/statistics preflight。"
---
# Idea Evaluator

## Overview

`idea-evaluator` 是 `research-idea` 技能包中的隔离独立评价 skill。

它接收 candidate idea、Research Context Brief、Evidence Map、Opportunity Map、Preflight Report 和用户约束，对 idea 进行六维评价、hard gate 检查、fatal flaw 判断，并给出下一步建议。

本 skill 只回答：这个 research idea 当前是否足够好，应该 promote、revise、reframe、merge、backup，还是 reject。

本 skill 不生成新 idea，不修订 idea，不写 proposal。

## Independent Execution Contract

- Run this skill only in a fresh, independent subagent or delegated thread. Never run it in the context that generated, drafted, or revised the artifact under review.
- Accept only frozen input artifacts identified by artifact ID, exact file path, and version. Treat every source artifact as read-only.
- Write only review or verification artifacts. Do not draft, rewrite, polish, fix, merge, or otherwise modify the reviewed idea or any source file.
- Do not use hidden reasoning from the parent task, an expected answer or decision, or output from any other reviewer. A fresh re-evaluation must not receive prior scores or the prior decision.
- Report the exact files read and the evaluation scope in the output.
- If a fresh independent subagent/delegated thread cannot be created, return `independent_review_pending` with a self-contained continuation brief and stop. Never fall back to inline self-review.

Every completed report must include:

```yaml
review_id:
reviewer_skill: idea-evaluator
reviewer_instance_id:
workflow_id:
round_id:
input_artifact_ids:
input_versions:
files_read:
review_scope:
isolation_mode: fresh_subagent
prior_scores_visible: false
source_edits_performed: false
decision:
findings:
unresolved_issues:
```

## When to Use

使用本 skill：

- candidate idea 已由 `multi-path-idea-generator` 生成；
- 已有 Evidence Map / Opportunity Map；
- 必要时已完成 `methodology-statistics-preflight`；
- orchestrator 需要独立评价 idea；
- 多个 idea 需要在统一 rubric 下比较；
- revision 后需要重新评价 score delta 和 gate status。

不要使用本 skill：

- 用户只要求生成 idea；
- evidence / opportunity map 尚缺失，且评价依赖证据；
- endpoint/metric、data source 或 minimal analysis route 明显缺失，应先 preflight；
- 用户要求写 proposal、SAP、protocol 或 grant；
- 用户要求完整 proposal peer review。

## Operating Principles

1. **必须隔离独立。** Evaluator 不得是生成该 idea 的同一 agent，也不得参与该 idea 的修订生成。
2. **只评价，不生成。** 本 skill 不提出新 idea，不重写 idea，不包装弱 idea。
3. **证据约束评价。** Novelty、guideline alignment 和 gap validity 必须受 Evidence Map 限制；证据不足时必须降级或标为 unverified。
4. **使用六维简单平均。** Overall score 为 Novelty、Feasibility、Impact、Relevance、Clarity、Completion 的简单平均。
5. **Hard gates 必须执行。** Feasibility、Relevance、Clarity、Completion 的最低门槛均为 3.0。
6. **Fatal flaw 优先。** 若存在不可修复的 data、method、measurement、relevance 或 feasibility blocker，即使 overall score 较高也不得 recommend promote。
7. **给出可操作下一步。** 评价结果必须包含 recommendation、主要理由、reviewer objections 和 targeted repair direction。
8. **不替代 preflight。** 方法学细节不清时，应要求返回 `methodology-statistics-preflight`，而不是自行补写分析方案。

## Inputs

本 skill 通常接收 candidate idea、Research Context Brief、Evidence Map、Opportunity Map、Evidence Limitations、Methodology-Statistics Preflight Report、用户目标与约束、idea lineage 和 orchestrator 指定的 evaluation scope。Fresh re-evaluation 不得接收 prior evaluation、prior scores 或 prior decision；确需核对 must-fix 时，只接收匿名问题清单和 revision delta。

字段定义见 `references/evaluation-input-schema.md`。

## Evaluation Dimensions

使用六个维度：

- Novelty
- Feasibility
- Impact
- Relevance
- Clarity
- Completion

维度定义、评分锚点、hard gates、decision rules 和 fatal flaw 处理见 `references/evaluation-rubric.md` 与 `references/evaluation-policy.md`。

Overall score 使用六维简单平均。不得使用加权平均。

## Hard Gates

必须执行 hard gates：

- Feasibility ≥ 3.0
- Relevance ≥ 3.0
- Clarity ≥ 3.0
- Completion ≥ 3.0

Hard gate 细则见 `references/evaluation-policy.md`。

未通过 hard gate 的 idea 不得直接 recommend promote。

## Decision Scope

本 skill 只允许输出以下 recommendation：

- `promote`
- `revise_then_promote`
- `revise`
- `reframe`
- `merge`
- `keep_as_backup`
- `reject`

具体判定规则见 `references/evaluation-policy.md`。

本 skill 不直接修改 idea pool；orchestrator 负责状态更新、loop control、merge 和 portfolio assembly。

## Workflow

### Phase 1 — Independence Check

确认 evaluation 是独立执行的。若 evaluator 曾生成或修订该 idea，应停止并要求 orchestrator 重新派发给隔离 evaluator。

### Phase 2 — Input Sufficiency Check

检查是否具备评价所需材料。若缺少关键 context、evidence、endpoint/metric、data source 或 minimal analysis route，应输出 evaluation failure report 或建议返回上游 skill。

### Phase 3 — Dimension Scoring

按六维 rubric 独立评分。每个分数必须有简短理由，且受 evidence 和 preflight 结果约束。

### Phase 4 — Hard Gate and Fatal Flaw Check

执行 hard gates，并检查不可修复缺陷。Fatal flaw 规则见 `references/evaluation-policy.md`。

### Phase 5 — Reviewer Objections

列出最可能的 reviewer objections。只列与 idea 质量直接相关的问题，不扩展成完整 peer review。

### Phase 6 — Recommendation and Repair Direction

给出 recommendation、主要理由、targeted repair direction 和 suggested next skill。不得生成新的 idea version。

## Deliverables

默认交付：

1. **Idea Evaluation Report**：六维分数、简单平均 overall、hard gate status、fatal flaws、reviewer objections 和 recommendation。
2. **Targeted Repair Direction**：说明应修复哪个维度，以及应返回哪个上游 skill。
3. **Evaluation Limitation Note**：说明哪些判断受 evidence limitation、preflight limitation 或用户约束不清影响。

若输入不足，交付 **Evaluation Failure Report**，说明缺失材料，以及应返回哪个上游 skill。

## Minimal Common Pitfalls

1. **自评。** 生成 idea 的 agent 不能评价同一 idea。
2. **评价时生成或重写 idea。** 本 skill 只能给 repair direction，不能产出新 idea。
3. **忽略 hard gates。** 未过 gate 的 idea 不得 promote。
4. **证据不足仍高估 novelty。** Evidence 不足时必须降级或标为 unverified。

## Minimal Verification Checklist

- 已确认 evaluator 与 generator 隔离；
- 已使用 Evidence Map 和 Preflight Report，如有；
- 已完成六维评分和简单平均；
- 已执行 hard gates；
- 已检查 fatal flaws；
- 已给出 reviewer objections 和 repair direction；
- 未生成或重写 idea；
- 未写 proposal。

## Delegation Rules

本 skill 必须由 `research-idea-orchestrator` 显式派发到 fresh independent subagent/delegated thread；不得依赖隐式调用。

执行期间不得再调用 idea generator、methodology-statistics-preflight
或 portfolio assembler 共同判断。

子 agent 必须通过具名冻结文件接收完整任务上下文（candidate ideas、context brief、evidence/opportunity map、preflight report、constraints、lineage），不得依赖父任务隐含上下文、预期结论或其他 reviewer 输出。

若发现需要修订，应返回 evaluation report，
由 orchestrator 决定是否进入 revision loop。

## References

- `references/evaluation-input-schema.md`：管理 evaluator 接收的输入字段和最低材料要求。
- `references/evaluation-output-schema.md`：管理 evaluation report 的输出字段、允许值和状态。
- `references/evaluation-rubric.md`：定义 Novelty、Feasibility、Impact、Relevance、Clarity、Completion 六维评价标准。
- `references/evaluation-policy.md`：定义 1–5 分锚点、简单平均、hard gates、decision rules 和 fatal flaw 处理。
- `references/evidence-limitation-rules.md`：定义 evidence 不足、clinical evidence 不足、unverified novelty 和 guideline alignment 的处理。
- `references/evaluator-isolation-policy.md`：定义 evaluator 与 generator 的隔离要求、无效 evaluation 的处理方式。
- `references/downstream-handoff-rules.md`：定义 evaluation report 如何交给 orchestrator、generator、preflight 和 portfolio assembler。
- `research-idea-orchestrator/references/artifact-contracts.md`：定义 idea_evaluation artifact 的统一字段命名和跨 skill 传递约定。
- `research-idea-orchestrator/references/handoff-validation.md`：定义 evaluator 输出交回 orchestrator 前的最小校验规则。
- `templates/idea-evaluation-report.md`：默认 idea evaluation report 模板。
- `templates/evaluation-failure-report.md`：输入不足、隔离失败或无法可靠评价时的失败报告模板。
