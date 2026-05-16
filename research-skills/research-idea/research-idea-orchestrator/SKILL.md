---
name: research-idea-orchestrator
description: 当用户希望把粗糙研究方向、原始 idea、文献/证据材料、funding call、临床/实践问题或数据资产转化为 1-3 个经过评价和排序、可供 PI 审阅的科研 idea portfolio 时使用。本 skill 编排 context building、evidence/opportunity mapping、multi-path generation、methodology/statistics preflight、独立 evaluation、loop control、lineage 和 portfolio assembly。
version: 1.4.0
author: Xuxu Wei
license: MIT
platforms:
  - linux
  - macos
  - windows
metadata:
  hermes:
    tags: [research, idea-generation, orchestration, evaluation, portfolio]
    related_skills:
      - research-context-builder
      - research-opportunity-mapper
      - multi-path-idea-generator
      - methodology-statistics-preflight
      - idea-evaluator
      - idea-adversarial-review-panel
      - idea-portfolio-assembler
      - academic-language-assessor
      - proposal-orchestrator
---

# research-idea-orchestrator

## Purpose

`research-idea-orchestrator` 是 research-idea workflow 主入口。它把宽泛方向、raw idea、证据材料、funding call、临床/实践问题或数据资产，转化为少量可比较、可淘汰、可修订、可交给 PI 审阅的候选 research ideas。

本 skill 只做流程编排、状态管理和 handoff 校验。不直接检索证据、不生成 idea、不评价自己生成的 idea、不做 methodology/statistics preflight、不写 proposal/SAP。

## Core Rules

- 先整理 context，再做 evidence/opportunity mapping。
- Evidence retrieval、source verification 和 Opportunity Map 由 `research-opportunity-mapper`（实际路径 `research/research-opportunity-mapper`）完成。
- Methodology/statistics preflight 由 `methodology-statistics-preflight`（实际路径 `research/methodology-statistics-preflight`）完成。
- Idea generation 和 evaluation 必须隔离；生成或修订同一 idea 的 agent 不得评价它。
- 对任何准备移交 proposal workflow 的 idea，必须先运行 handoff 前 adversarial review；该 review 只攻击风险和移交充分性，不替代 `idea-evaluator` 评分。
- Evaluation 使用六维简单平均：Novelty、Feasibility、Impact、Relevance、Clarity、Completion。
- 保留 lineage：生成、修订、合并、淘汰和晋级都要可追踪。
- 由 orchestrator 统一分配或规范化 `idea_id`；ID、派生后缀和 lineage 必须遵守 `research-idea-orchestrator/references/idea-id-and-lineage-rules.md`。
- 最终输出面向 PI 审阅；若没有合格 idea，不强行包装积极结论。
- 所有面向用户的产物必须为 `.md` 格式。`.yaml` 仅用于 agent-to-agent 中间状态传递。
- Workflow 产物保存到用户 project 目录，不得保存到 skill 包内部。

## Artifact Governance Addendum

- Use `references/artifact-naming-and-directory-rules.md` for numbered project directories from `00_input/` through `10_delegates/`.
- Store current pointers and the human-readable inventory in `09_state/workflow-state.yaml` and `09_state/artifact-index.md`.
- Store round manifests in `09_state/round-<n>-manifest.md` or YAML when needed for agent-to-agent transfer.
- Final portfolio and proposal handoff files live in `07_portfolio/` and `08_handoff/`.
- Call `academic-language-assessor` only for external-facing portfolio or handoff text. Save `07_portfolio/language-assessment-vNNN.md` and `07_portfolio/language-change-log-rNNN.md` when polishing is performed.
- Language QA must not change idea scores, promotion/rejection decisions, or adversarial handoff status.

## Workflow

1. **Evidence confirmation and triage**  
   确认用户是否已有 evidence materials。将用户材料、主题、目标产出、约束和已有 evidence artifacts 传给 `research-opportunity-mapper`。用户没有材料时，由 mapper 负责检索和 mapping。

2. **Research Context Brief**  
   调用 `research-context-builder`，整理领域、目标、对象、数据/方法线索、endpoint/metric、约束、假设和关键缺口。

3. **Evidence and Opportunity Mapping**  
   默认调用 `research-opportunity-mapper`，除非用户明确跳过。下游只需要 mapper 的 Evidence Map、Opportunity Map、Evidence Limitations 和 Handoff Notes；检索日志仅在审计、失败、高风险或用户要求时输出。若搜索方向 >=4，优先使用 `research-opportunity-mapper/scripts/evidence_search.py` 进行聚焦并行检索，而不是在 orchestrator 内维护检索脚本副本。

4. **Multi-path generation**  
   调用 `multi-path-idea-generator`。默认从 3-6 条 generation paths 生成候选 ideas；路径选择依据 Opportunity Map、用户目标和约束。Generation 可以由 orchestrator 内联执行；隔离硬要求只约束 final evaluation。

5. **Methodology/statistics preflight**  
   对临床、观察性、预测模型、实验设计、benchmark、统计分析或 endpoint/data/method fit 不清的 idea，使用隔离子 agent 调用 `methodology-statistics-preflight`。Preflight 子 agent 不得接触 idea-evaluator 的评价结果。

6. **Independent evaluation**  
   使用隔离、独立的 `idea-evaluator` 子 agent。不得在生成/修订同一 idea 的上下文中加载 evaluator 并内联评估。Evaluation brief 必须使用 `references/delegate-brief-templates.md`，并引用 `research-idea-orchestrator` 的 artifact contracts。

7. **Decision and loop control**  
   根据 evaluation 执行 `promote`、`revise`、`reframe`、`merge`、`reject`、`keep_as_backup`。默认最多 3 轮；缺陷明确时定向修复，不随机再生成。每轮更新 round manifest。

8. **Pre-handoff adversarial review**  
   对任何可能标记为 `proposal_handoff_status: ready` 或 `conditional` 的 idea，使用隔离子 agent 调用 `idea-adversarial-review-panel`。Panel 至少覆盖 novelty/gap skeptic、feasibility/method skeptic 和 PI strategy reviewer。若出现 blocking objection，回到 `research-opportunity-mapper`、`methodology-statistics-preflight`、`multi-path-idea-generator` 或 `idea-evaluator`；不得直接移交 proposal。

9. **Portfolio assembly**  
   调用 `idea-portfolio-assembler`，输出 promoted / backup / merged / rejected ideas、score/gate summary、evidence limitations、lineage 和 proposal handoff status。

## Delegation and Runtime Compatibility

优先使用运行时的 `delegate_task` 派发 preflight 和 evaluator 子 agent。若运行时不支持 subagent/delegation，按 `research-idea-orchestrator/references/runtime-delegation.md` 执行 fallback：final independent evaluation 必须延后、标记 pending，或在独立新会话完成；不得把未独立评价的 idea 标为 promoted。

## Handoff to Proposal

只有当 idea 通过独立 evaluation、关键 evidence limitations 已说明、endpoint/metric 和 data/method path 足以支持 readiness triage，且 handoff 前 adversarial review 未发现 blocking objection 时，才建议进入 `proposal-orchestrator`。Proposal workflow 仍必须自行运行 context brief 和 readiness triage。

`proposal-orchestrator` 位于 `research-proposal/` 顶级分类。加载时使用 `skill_view(name="proposal-orchestrator")`。

## File Organization

Workflow 产出的所有文件保存到用户 project 目录下。每个 workflow round 使用独立子目录或编号文件，推荐维护 `00-round-<n>-manifest.md`。

面向用户的最终产物必须为人类可读的 `.md` 文档，包括 Research Context Brief、Evidence Map、Opportunity Map、Generated Idea Set、Preflight Report、Evaluation Report 和 Portfolio。仅当需要 agent-to-agent 状态传递时，才允许 `.yaml` 中间文件。

## References

- `references/delegate-brief-templates.md`：定义派发 generation、preflight 和 evaluation 子 agent 时需要包含的 brief 字段和格式。
- `references/evidence-confirmation-and-routing.md`：定义用户证据材料的确认流程和 evidence mapping 的路由规则。
- `references/loop-control-and-stop-rules.md`：定义 idea 修订循环的最大轮次、定向修复规则和停止条件。
- `references/proposal-handoff-rules.md`：定义 idea portfolio 向 proposal workflow 移交的条件、材料和边界。
- `references/evaluation-rubric.md`：定义 Novelty、Feasibility、Impact、Relevance、Clarity、Completion 六维评价标准的详细锚点。
- `references/if10-evaluation-gate.md`：当用户要求至少1篇 IF>10 论文时，独立 evaluator 需要附加的发表可行性评估门。
- `research-idea-orchestrator/references/artifact-contracts.md`：定义 research-idea workflow 的统一 artifact schema、字段命名和状态值。
- `research-idea-orchestrator/references/idea-id-and-lineage-rules.md`：定义 idea ID、派生 ID、merge ID、previous_ids 和多轮 artifact 命名规则。
- `research-idea-orchestrator/references/workflow-manifest.md`：定义每轮 workflow manifest、文件登记、lineage 和审计字段。
- `research-idea-orchestrator/references/handoff-validation.md`：定义跨 skill handoff 前的最小校验规则。
- `research-idea-orchestrator/references/runtime-delegation.md`：定义 `delegate_task`、并发子 agent 和无委派能力环境的兼容执行规则。
