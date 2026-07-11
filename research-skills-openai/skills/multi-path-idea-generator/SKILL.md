---
name: multi-path-idea-generator
description: "Generate a diverse, non-duplicative set of research ideas from approved context and opportunity maps using selected generation paths; do not evaluate or rank candidates."
---
# Multi-Path Idea Generator

## Overview

`multi-path-idea-generator` 是 `research-idea` 技能包中的候选 idea 生成器。

它接收 Research Context Brief、Opportunity Map、用户约束和 generation paths，输出一组结构化候选 research ideas，供后续 methodology/statistics preflight、隔离独立 evaluation 和 portfolio assembly 使用。

本 skill 只回答：可以从哪些不同路径生成候选 research ideas？

本 skill 不回答：这些 ideas 是否值得推进？

## When to Use

使用本 skill：

- orchestrator 已有 Research Context Brief 与 Opportunity Map；
- 需要从多个路径生成候选 research ideas；
- 需要根据 opportunity type 选择 generation paths；
- 需要对既有 idea 做定向扩展、重构、补全或变体生成；
- evaluation 后需要针对弱项进行 targeted generation。

不要使用本 skill：

- 上下文尚未构建；
- evidence / opportunity map 尚未形成，且该任务依赖证据；
- 用户只要求评价 idea；
- 用户要求写 proposal、SAP、protocol 或 grant；
- 需要方法学/统计可行性判断。

## Operating Principles

1. **只生成，不评价。** 本 skill 不评分、不排序、不判断 promote/reject。
2. **路径驱动。** 每个 idea 必须标明 generation path 和 supporting opportunity。
3. **保留全部路径。** 默认支持全部 10 条 generation paths；orchestrator 可指定全部、部分或 targeted paths。
4. **可建议路径。** 若 orchestrator 未指定 paths，本 skill 可根据 opportunity type、用户目标和约束提出路径建议。
5. **证据约束。** Novelty claim 不得超过 Evidence Map 支持范围；未验证内容必须标注不确定性。
6. **避免重复。** 不生成仅换标题或措辞的近似 idea。
7. **保留 lineage。** 扩展、合并、重构或修订已有 idea 时，必须保留 parent 信息。
8. **evaluation 必须隔离。** 本 skill 生成的 idea 必须交回 orchestrator，由 orchestrator 派发给隔离、独立的 `idea-evaluator` 子 agent。

## Workflow

### Phase 1 — Validate Readiness

检查 Research Context Brief、Opportunity Map、用户约束和 existing idea pool 是否足以支持生成。若关键输入不足，输出 generation failure report。

### Phase 2 — Select or Accept Paths

若 orchestrator 已指定 paths，按指定路径生成。若未指定，本 skill 可提出 recommended paths，但不替代 orchestrator 的全局循环控制。

### Phase 3 — Generate Candidate Ideas

每条路径生成少量候选 idea。每个 idea 必须包含 research question、endpoint/metric、data source 或 evidence base、minimal experiment / analysis route、主要风险和不确定性。

### Phase 4 — Duplicate and Scope Control

检查候选 idea 是否与 existing idea pool 过度相似。近似重复 idea 应合并、改写为实质变体，或丢弃并说明原因。

### Phase 5 — Handoff

输出 generated idea set、generation rationale、lineage notes、uncertainty notes 和 downstream needs。不得给分或排序。

### Phase 6 — Contract Validation

按 `research-idea-orchestrator/references/artifact-contracts.md` 的 Candidate Idea contract 检查字段命名，并按 `research-idea-orchestrator/references/handoff-validation.md` 检查是否可交给 preflight 或 evaluator。

## Deliverables

默认交付：

1. **Generated Idea Set**：按路径生成的候选 ideas；
2. **Generation Rationale**：每个 idea 来源于哪个 opportunity 与 path；
3. **Lineage Notes**：新 idea 与已有 idea 的关系；
4. **Uncertainty Notes**：证据不足、novelty 未验证或 feasibility 未确认之处；
5. **Downstream Needs**：是否建议进入 methodology/statistics preflight 或 independent evaluation。

若输入不足，交付：

- **Generation Failure Report**：说明缺少哪些上下文或 opportunity，建议返回哪个上游 skill。

## Evaluation Isolation Rule

本 skill 不执行 evaluation。若用户要求评价、排序、选择最佳 idea、判断是否值得做或是否进入 proposal，本 skill 必须停止评价行为，并标记：

- `evaluation_needed: true`
- `handoff_to: idea-evaluator`
- `must_be_isolated: true`

评价必须由 `research-idea-orchestrator` 派发给隔离、独立的 `idea-evaluator` 子 agent。生成当前 idea 的 agent 不得自评。

## Minimal Common Pitfalls

1. 生成后直接评价。
2. 脱离 Evidence Map 声称 novelty。
3. 产生近似重复 idea。

## Minimal Verification Checklist

- 已使用 Research Context Brief 和 Opportunity Map；
- 每个 idea 标明 generation path 与 supporting opportunity；
- 每个 idea 具备 research question、endpoint/metric、data source 或 evidence base、minimal experiment / analysis route；
- 已标注主要不确定性；
- 未执行 evaluation；
- 已标记需要隔离独立 evaluation。

## References

- `research-idea-orchestrator/references/artifact-contracts.md`：定义 Candidate Idea、Lineage Record 和跨 skill handoff 的统一字段命名。
- `research-idea-orchestrator/references/handoff-validation.md`：定义 generator 输出交给 preflight、evaluator 和 assembler 前的最小校验规则。
- Read `references/idea-schema.md` when its named guidance or contract applies: ：管理候选 idea 的字段、必填项和允许值。
- Read `references/generation-paths.md` when its named guidance or contract applies: ：定义 10 类 generation paths 的目的、适用场景和输出要求。
- Read `references/path-selection-rules.md` when its named guidance or contract applies: ：定义如何根据 opportunity type、用户目标、约束和 repair direction 选择路径。
- Read `references/novelty-claim-rules.md` when its named guidance or contract applies: ：定义 novelty claim 如何受 Evidence Map 限制，以及何时必须标注 unverified。
- Read `references/duplicate-control-rules.md` when its named guidance or contract applies: ：定义近似重复 idea 的识别、合并、丢弃和 lineage 记录规则。
- Read `references/generation-quality-gates.md` when its named guidance or contract applies: ：定义 idea 进入 idea pool 前的最低完整性要求。
- Read `references/downstream-handoff-rules.md` when its named guidance or contract applies: ：定义交付给 preflight、evaluator 和 portfolio assembler 的内容要求。
- Use `templates/generated-idea-set.md` when producing its named artifact: ：候选 idea 生成结果模板。
- Use `templates/generation-failure-report.md` when producing its named artifact: ：输入不足或无法可靠生成时的失败报告模板。
