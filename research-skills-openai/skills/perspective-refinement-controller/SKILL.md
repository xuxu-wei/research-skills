---
name: perspective-refinement-controller
description: "Plan and control targeted Perspective revision after independent evaluation, route writing to the drafter, preserve lineage, and require fresh re-evaluation."
---
# perspective-refinement-controller

## Purpose

控制 Perspective 修订循环。将 evaluator 反馈转化为定向修订计划，调度 drafter 执行修订，管理版本 lineage，触发独立 re-evaluation，执行八路决策路由。

## Core Rules

- 修订必须针对 evaluator 具体问题，不做无目标全文重写
- 每轮修订由新隔离 evaluator 复评
- 修订策略标注（追加/替换/浓缩/删减/澄清）+ 入文策略（入正文/仅入回应/不处理）
- 减法优先
- language_polishing 模式必须先由 orchestrator 显式派发 fresh independent `academic-language-assessor`，保存 `05_evaluations/language-assessment-vNNN.md`；修订后保存 `06_revisions/round-NNN/language-change-log-rNNN.md`。
- 最多 2 轮常规修订；重构走独立路由
- Caveat budget：非硬停，触发三选一
- 核心主张经限定后无贡献 → 硬停

## I/O Contract

```
Allowed Inputs: evaluation-report, draft, argument-skeleton(只读), claim-ledger(只读), claim-evidence-matrix(只读)
Required Outputs: revision-plan, delta-report, 01_claims/change-requests/refinement-request-v{N}.md(如需)
May Read: 05_evaluations/, 04_drafts/, 03_skeletons/, 01_claims/(只读)
May Write: 06_revisions/, 01_claims/change-requests/
Must Not Read: 07_panel/, 10_delegates/
Must Not Write: claim-ledger, draft(交 drafter)
May Call: perspective-drafter(修订), perspective-evaluator(显式派发 fresh independent instance)
Must Not Call: panel reviewer, architect/curator(通过routing上报)
```

## Procedure

### 1. Confirm Revisability
检查不可修复 fatal flaw → 停止。确认 decision 为 revise 类型。

### 2. Build Revision Plan
提取 must-fix/should-fix/optional。每条规划修改策略 + 入文策略。检查 caveat budget 风险。

### 3. Coordinate Draft Update
调度 drafter（修订模式）→ perspective-v{N+1}.md + perspective-v{N+1}-paragraph-map.md + response。

### 4. Generate Delta Report
已处理/未处理/新引入/核心主张变化。

### 5. Delegate Re-evaluation
制备新隔离包并冻结 artifact IDs、路径和版本 → 显式派发新的 fresh independent `perspective-evaluator` subagent/delegated thread。不得提供 prior scores 或 prior decision；确需核对 must-fix 时仅提供匿名问题清单和 revision delta。若无法创建独立实例，返回 `independent_review_pending` 和续跑 brief 后停止，不得 inline self-review。

### 6. Compare and Route

## Eight-Route Decision

| Route | 触发 | 处理 |
|-------|------|------|
| accept | pre-panel hard gates 全部通过 | → Panel |
| minor_revision | 表述/措辞 | drafter, 1轮 |
| major_revision_draft | 部分论证不足 | drafter, ≤2轮 |
| argument_rebuild | 论证链跳跃 | → architect |
| evidence_rebuild | 证据不足 | → curator |
| thesis_redesign | 核心判断问题 | → input-builder+用户确认 |
| outlet_retarget | outlet 不匹配 | → 更新profile+用户确认 |
| reject_not_salvageable | 不可修复 | → 停止 |

Panel major revision limit (≤1轮) 仅适用于 major_revision_draft。

## Caveat Budget Protocol

>2层限定 → 三选一：收窄 thesis / 降低 claim strength / 拆分主张。
硬停：经限定后无明确贡献。

## Stop Conditions
- fatal flaw / caveat budget硬停 / 死亡螺旋 / 主张漂移 / 无增益 / 达最大轮次

## References
- Read `references/revision-rules.md` when its named guidance or contract applies.
- Read `references/death-spiral-patterns.md` when its named guidance or contract applies.
- Read `references/delta-report-template.md` when its named guidance or contract applies.
- Read `references/refinement-routing-table.md` when its named guidance or contract applies.
