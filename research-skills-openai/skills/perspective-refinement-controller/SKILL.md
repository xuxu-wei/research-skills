---
name: perspective-refinement-controller
description: "Normalize Perspective findings into one writer interface, verify preservation, and require fresh review."
---
# perspective-refinement-controller

## Purpose

控制 Perspective 的科学修订与后续编辑修复循环。将 scientific evaluator 反馈转化为定向修订计划，或将独立 narrative/language findings 规范化为单一 YAML repair brief；调度 drafter 执行修订，检查计划一致性与科学内容保留，再触发全新复评。

## Core Rules

- 修订必须针对 evaluator 具体问题，不做无目标全文重写
- 每轮修订由新隔离 evaluator 复评
- 修订策略标注（追加/替换/浓缩/删减/澄清）+ 入文策略（入正文/仅入回应/不处理）
- 减法优先
- 科学冻结前，语言问题只能作为当前 `scientific_revision` plan 的有界动作；科学冻结后不存在独立 `language_polishing` 路由，所有 narrative/language 变更必须进入单一 YAML brief、same-writer repair 和完整下游复验。
- 最多 2 轮常规修订；重构走独立路由
- Caveat budget：非硬停，触发三选一
- 核心主张经限定后无贡献 → 硬停
- 科学修订通过后先冻结当前版本；narrative 与 language assessment 必须并行、独立并针对同一版本
- 编辑修复只接收一个规范化 YAML brief，并由当前科学版本的同一 `writer_instance_id` 执行
- 每次编辑修复后依次完成 deterministic conformance、fresh content-preservation check、fresh narrative/language reassessment；缺一不可
- Final evaluator 的隔离包只含 final Perspective、installed stable rubric 和 minimal evidence/outlet facts；controller 不把任何 repair/history artifact 传给它

## I/O Contract

```
Allowed Inputs: evaluation-report, draft, argument-skeleton(只读), claim-ledger(只读), claim-evidence-matrix(只读); editorial 模式另含 narrative repair plan, language assessment, protected-content register
Required Outputs: revision-plan, delta-report, 01_claims/change-requests/refinement-request-v{N}.md(如需); editorial 模式另含 editorial-repair-brief-rNNN.yaml 与 editorial-conformance-check-rNNN.yaml
May Read: 05_evaluations/, 04_drafts/, 03_skeletons/, 01_claims/(只读)
May Write: 06_revisions/, 01_claims/change-requests/
Must Not Read: 07_panel/, 10_delegates/
Must Not Write: claim-ledger, draft(交 drafter), narrative/language/preservation/evaluation report
May Call: perspective-drafter(修订), perspective-evaluator(显式派发 fresh independent instance)
Must Not Call: panel reviewer, architect/curator(通过routing上报)
```

## Procedure

选择且只执行一个模式：`scientific_revision` 或 `editorial_repair`。

## Scientific Revision Mode

### 1. Confirm Revisability
检查不可修复 fatal flaw → 停止。确认 decision 为 revise 类型。

### 2. Build Revision Plan
提取 must-fix/should-fix/optional。每条规划修改策略 + 入文策略。检查 caveat budget 风险。

### 3. Coordinate Draft Update
将评审意见规范化为可执行 revision plan，再调度 drafter（修订模式）→ perspective-v{N+1}.md + perspective-v{N+1}-paragraph-map.md + response。Drafter 只读当前 draft 与该 plan，不读取原始 evaluator/panel report。

### 4. Generate Delta Report
已处理/未处理/新引入/核心主张变化。

### 5. Delegate Re-evaluation
制备新隔离包并冻结 artifact IDs、路径和版本 → 显式派发新的 fresh independent `perspective-evaluator` subagent/delegated thread。仅提供最新版完整 draft、稳定 rubric、必要事实材料和可选匿名 must-fix 清单；不得提供旧 draft、revision delta、prior scores 或 prior decision。若无法创建独立实例，返回 `independent_review_pending` 和续跑 brief 后停止，不得 inline self-review。

### 6. Compare and Route

`accept` 只表示科学版本可进入 panel 或 editorial qualification；不等于最终语言、叙事、outlet 或投稿就绪。

## Editorial Repair Mode

1. **Freeze.** 绑定一个已完成科学修订和适用 panel route 的 Perspective `{artifact_id, version, path}`、其 `writer_instance_id`、reader handoff 和 protected-content register。新产物不要求 digest。
2. **Receive parallel assessments.** 接收同一冻结版本的 `research-narrative-assessor` repair plan 与 `academic-language-assessor` report。两者必须来自 fresh instances，互不读取，也不含 evaluator/panel 输出。
3. **Normalize.** 按 `references/editorial-repair-contract.md` 将所有 actionable items 去重、拆分冲突操作、建立依赖，并写入一个 `editorial-repair-brief-rNNN.yaml`。无法在不改变科学内容的情况下合并时，返回科学修订或 clarification。
4. **Same-writer repair.** 只向当前科学版本的同一 writer instance 派发冻结稿、单一 brief 和 protected register。若该 writer 不可用，返回 `editorial_repair_pending`，不得换 writer 近似执行。
5. **Conformance.** 对 writer delta 和新 paragraph map 做确定性检查：每个 action 恰有一个 disposition、依赖无环、没有未声明操作、source bindings/claim IDs/authority families 仍完整。该检查可读取 skeleton/ledger/map，但其输出不得传给 final evaluator。
6. **Preservation and reassessment.** fresh preservation instance 只读 prior/revised/register/delta；通过后，fresh narrative 与 language reassessors 针对 revised version 并行运行，不读旧报告或 delta。
7. **Final handoff.** 只有 conformance pass、`scientific_content_preserved`、`narrative_ready` 和 `submission_ready` 同时成立，才冻结版本并请求 orchestrator 派发 minimal-input final evaluator。

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

当限定堆叠使目标读者无法稳定识别 thesis、适用范围或贡献时，依据科学含义三选一：收窄 thesis / 降低 claim strength / 拆分主张。不得使用跨领域统一的限定层数阈值。
硬停：经限定后无明确贡献。

## Stop Conditions
- fatal flaw / caveat budget硬停 / 死亡螺旋 / 主张漂移 / 无增益 / 达最大轮次
- editorial action 需要改变科学主张、证据状态、source binding、scope 或 authority-family 含义
- same writer 不可用、assessment 隔离失败、conformance 失败或内容保留未通过

## References
- Read `references/revision-rules.md` when its named guidance or contract applies.
- Read `references/death-spiral-patterns.md` when its named guidance or contract applies.
- Read `references/delta-report-template.md` when its named guidance or contract applies.
- Read `references/refinement-routing-table.md` when its named guidance or contract applies.
- Always read `references/editorial-repair-contract.md` in editorial-repair mode.
- Use `templates/editorial-repair-brief.yaml` for the single normalized writer brief.
- Use `templates/editorial-conformance-check.yaml` for the deterministic post-repair check.
