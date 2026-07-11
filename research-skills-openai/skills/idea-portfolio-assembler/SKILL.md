---
name: idea-portfolio-assembler
description: "Assemble evaluated research ideas into a PI-review portfolio with rankings, lineage, limitations, dissent, and proposal-handoff status without rescoring or rewriting candidates."
---
# Idea Portfolio Assembler

## Overview

`idea-portfolio-assembler` 是 `research-idea` 技能包中的最终组合整理 skill。

它接收已完成 evaluation 的 idea pool、evaluation reports、preflight reports、evidence / opportunity map、lineage records 和 orchestrator decision，生成面向 PI 审阅的 **Research Idea Portfolio**。

本 skill 只回答：经过前面流程后，哪些 ideas 应呈现给 PI，排序如何，证据与评价依据是什么，下一步应如何推进。

本 skill 不重新生成 idea，不重新评分，不修改 hard gate，不写 proposal，也不设计完整研究方案。

## When to Use

使用本 skill：

- orchestrator 已完成 1–3 轮 idea generation / revision / evaluation；
- 至少一个 idea 被 recommend `promote`、`revise_then_promote` 或 `keep_as_backup`；
- 需要向 PI 呈现最终候选 idea portfolio；
- 需要汇总 rejected、merged、backup ideas 及原因；
- 需要整理 proposal handoff status；
- 没有 promoted idea，但需要输出 no-promoted-idea report。

不要使用本 skill：

- candidate ideas 尚未经过隔离独立 evaluation；
- 需要继续生成新 idea；
- 需要修改 idea 分数或 gate status；
- 需要判断 promote/reject；
- 需要写 proposal、SAP、protocol 或 grant。

## Operating Principles

1. **只组装，不评价。** 不改分、不新增评分、不推翻 `idea-evaluator` 的判断。
   不从材料中推断新的质量判断，不解决 reviewer 分歧，也不得把带 fatal flaw、adversarial panel unresolved blocking finding 或 `independent_review_pending` 的 idea 提升为 promoted/ready。此类 idea 的 workflow state 必须分别机械映射为 `blocked` 或 `independent_review_pending`；通过全部门禁的 portfolio 只能进入 `human_signoff_required`。
2. **面向 PI 审阅。** 输出应清晰、结构化、可讨论，而不是机器 schema dump。
3. **保留评价依据。** 每个候选 idea 必须附带 evaluation summary、hard gate status、evidence limitation 和 main reviewer objections。
4. **保留 lineage。** 必须说明 idea 的来源、parent ideas、revision / merge / reframe 关系。
5. **区分 promoted、backup、merged、rejected。** 不只展示 winner，也保留淘汰和备选轨迹。
6. **不粉饰失败。** 若没有 promoted idea，输出 no-promoted-idea report，不强行构造积极结论。
7. **handoff 条件必须明确。** 只有满足 proposal handoff minimum 的 idea 才能标为 ready for `proposal-orchestrator`。

## Inputs

本 skill 通常接收：

- Research Context Brief；
- Evidence Map / Opportunity Map；
- Evidence Limitations；
- generated / revised idea pool；
- Methodology-Statistics Preflight Reports；
- independent Idea Evaluation Reports；
- idea lineage records；
- orchestrator decisions；
- proposal handoff check；
- adversarial panel role reports、blocking findings 与 dissent（任何可能标为 ready/conditional 的 idea 必需）；
- user constraints and intended output。

字段定义见 `references/portfolio-input-schema.md`。

## Workflow

### Phase 1 — Input Completeness Check

检查是否已有 context、evidence / opportunity summary、idea pool、independent evaluation reports、gate status、lineage records 和 handoff status。

若缺失独立 evaluation，不得组装最终 portfolio，应输出 assembly failure report。

### Phase 2 — Candidate Grouping

将 ideas 分为 `promoted`、`revise_then_promote`、`backup`、`merged`、`rejected` 和 `evaluation_failed`。

分组规则见 `references/portfolio-policy.md`。

### Phase 3 — Ranking and Selection

根据 orchestrator decision、evaluation report、gate status、distinctiveness 和 PI relevance 排序。

本 skill 可以呈现排序，但不得重新打分或修改 evaluation recommendation。

排序规则见 `references/portfolio-policy.md`。

### Phase 4 — Promoted Idea Package Assembly

为每个最终候选 idea 整理 PI 审阅版 promoted idea package，包括 research question、endpoint / metric、data source、minimal analysis、value / novelty claim、evidence summary、evaluation summary、主要风险和 proposal handoff status。

字段与展示规则见 `references/promoted-idea-package-rules.md`。

### Phase 5 — Lineage and Decision Trace

整理最终候选 idea 的来源和演化轨迹，并摘要 rejected / merged / backup ideas 的原因。

规则见 `references/lineage-summary-rules.md`。

### Phase 6 — No-Promoted-Idea Handling

若没有 idea 达到 portfolio 展示标准，输出 no-promoted-idea report。不得强行推荐未过 gate 的 idea。

规则见 `references/no-promoted-idea-report-rules.md`。

### Phase 7 — Final Portfolio Output

使用 `templates/research-idea-portfolio.md` 输出 PI 审阅版 Research Idea Portfolio。

## Deliverables

默认交付：

1. **Research Idea Portfolio**：面向 PI 审阅的最终组合文档。
2. **Ranked Candidate Ideas**：1–3 个最终候选 idea，附 evaluation summary、gate status 和 handoff status。
3. **Rejected / Merged / Backup Summary**：说明未进入最终候选的 ideas 及原因。
4. **Lineage Summary**：说明 idea 生成、修订、合并和淘汰轨迹。
5. **Remaining Uncertainties and PI Decision Points**：明确仍需 PI 确认的事项。
6. **Proposal Handoff Summary**：标明哪些 ideas 已满足进入 `proposal-orchestrator` 的最低条件。

若没有可推荐 idea，交付 `No-Promoted-Idea Report`。

若缺失必要输入，交付 `Portfolio Assembly Failure Report`。

## Evaluation Boundary

本 skill 不执行 idea evaluation。

禁止行为：

- 修改 evaluator 给出的六维分数；
- 修改 hard gate status；
- 将 failed gate idea 包装成 promoted idea；
- 生成新的 reviewer objections；
- 自行决定 promote / reject；
- 用 portfolio 排版替代独立 evaluation。

若发现 evaluation 缺失、冲突或明显无效，应标记 evaluation issue，并交回 `research-idea-orchestrator` 处理。

## Minimal Common Pitfalls

1. **重新评价 idea。** 本 skill 只能整理已有 evaluation。
2. **只展示 winner。** 必须保留 rejected / merged / backup 摘要。
3. **把 portfolio 写成 proposal。** 本 skill 不写完整研究方案。

## Minimal Verification Checklist

- 已使用 independent evaluation reports；
- 已区分 promoted、backup、merged、rejected ideas；
- 已保留 score、gate、reviewer objections 和 evidence limitations；
- 已生成 lineage summary；
- 已标明 proposal handoff status；
- 未重新评分；
- 未生成新 idea；
- 未写 proposal。

## References

- Read `references/portfolio-input-schema.md` when its named guidance or contract applies: ：管理 portfolio assembly 所需输入字段和最低材料要求。
- Read `references/portfolio-output-schema.md` when its named guidance or contract applies: ：管理最终 portfolio、failure report 和 no-promoted report 的输出字段。
- Read `references/portfolio-policy.md` when its named guidance or contract applies: ：定义候选分组、排序、proposal handoff status 和 assembly failure 处理规则。
- Read `references/promoted-idea-package-rules.md` when its named guidance or contract applies: ：定义 PI 审阅版 promoted idea package 的组成和 handoff 状态。
- Read `references/lineage-summary-rules.md` when its named guidance or contract applies: ：定义 idea lineage、parent IDs、revision / merge / reframe 轨迹的摘要规则。
- Read `references/no-promoted-idea-report-rules.md` when its named guidance or contract applies: ：定义没有 promoted idea 时的输出规则。
- `research-idea-orchestrator/references/artifact-contracts.md`：定义 portfolio package、lineage 和 evaluation artifact 的统一字段命名。
- `research-idea-orchestrator/references/workflow-manifest.md`：定义 portfolio assembly 需回写的 round manifest 字段。
- Use `templates/research-idea-portfolio.md` when producing its named artifact: ：PI 审阅版 Research Idea Portfolio 模板。
- Use `templates/no-promoted-idea-report.md` when producing its named artifact: ：无 promoted idea 时的报告模板。
- Use `templates/portfolio-assembly-failure-report.md` when producing its named artifact: ：portfolio 组装失败时的报告模板。
