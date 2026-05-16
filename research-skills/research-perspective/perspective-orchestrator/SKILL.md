---
name: perspective-orchestrator
description: Use when 编排 Perspective/Viewpoint/Commentary 文章从核心观点到终稿的完整生产流程，包括输入模板、claim 管理、论证架构、起草、独立评价、定向修订、模拟 Panel、终稿合规，并支持 Lite / Standard / Full 三种模式。
version: 1.1.0
author: Xuxu Wei
license: MIT
metadata:
  hermes:
    tags: [research-perspective, perspective, commentary, viewpoint, article-writing, argumentation]
    related_skills:
      - perspective-input-builder
      - perspective-claim-evidence-curator
      - perspective-argument-architect
      - perspective-drafter
      - perspective-evaluator
      - perspective-refinement-controller
      - perspective-review-panel
      - perspective-final-compositor
      - research-opportunity-mapper
      - academic-language-assessor
---

# perspective-orchestrator

## Purpose

编排 Perspective 文章从核心观点到终稿的完整生产流程。不承担"内容判断的最终来源"，但负责流程编排、状态管理、决策路由、delegate 隔离和用户交互。

**Perspective 的本质**：不是综述，不是研究论文。是对领域中的一个重要问题提出有判断力的解释、重新框定或行动方向。核心任务是"这些发现意味着什么？领域正在误解什么？下一步真正重要的问题是什么？"

## Core Rules

### 角色边界

Orchestrator **可以做**：
- 调用并约束构建型模块（input-builder、curator、architect、drafter、refinement-controller）
- 制备 delegate 隔离包并派发隔离子 agent
- 收集外部评价结果并合成
- 执行决策路由（evaluator 结果 → 修订/接受/拒绝/重构；panel 结果 → 终稿/回修订/停止）
- 审核 claim change request 并交 curator 执行
- 在关键决策点向用户暴露选项，等待确认
- 维护文件状态、版本 lineage、workflow-manifest.yaml、decision-log.md

Orchestrator **不可以做**：
- 独立评价任何构建产物（没有 evaluator 报告时不得做质量判断）
- 替代 evaluator 或 panel reviewer 做评分
- 直接修改 claim-ledger、skeleton、draft
- 创建未经外部评价支持的新质量判断

**如果必须推翻外部评价结论**：必须在 decision-log.md 中记录被推翻的建议、推翻原因、接受的风险、用户确认状态。对于实质性问题，必须获取用户确认。

### Claim-Ledger 治理

`claim-ledger.md` 是 source of truth，默认只读。仅 `perspective-claim-evidence-curator` 拥有直接写入权。其他模块提交 change request → orchestrator 审核 → curator 执行合并。

### 构建与评价隔离

- 构建型模块（input-builder、curator、architect、drafter、refinement-controller）：orchestrator 内联执行
- 评价型模块（evaluator、panel reviewers、final-compositor）：通过当前运行时的 delegation adapter 派发隔离实例（Hermes 使用 `delegate_task`；Codex 使用独立子代理/隔离 brief）
- 同一 evaluator 实例不得既生成又评价；panel reviewer 之间互不知晓

### 文件中心制

所有组件通过项目目录下的具名文件传递状态。项目目录必须位于当前 workspace 内或用户显式指定的可写目录，推荐 `<workspace>/research-perspective-projects/<project-name>/`。不得硬编码宿主机专属路径。

### 面向用户的产物

所有面向用户的产物为 `.md` 格式。`.yaml` 仅用于 agent-to-agent 状态传递。

## Artifact And Language Governance

- Use `references/artifact-naming-and-directory-rules.md` for numbered project directories from `00_input/` through `10_delegates/`.
- Drafts live in `04_drafts/`; revision plans, reviewer responses, deltas, and language change logs live in `06_revisions/round-NNN/`; final submission-facing files live in `08_final/`.
- Draft names use `04_drafts/perspective-vNNN.md`; substantive edits create a new draft version.
- The body must not contain reviewer-response language. Use `06_revisions/round-NNN/response-to-reviewers-rNNN.md` for point-by-point responses.
- Revision records use `06_revisions/round-NNN/revision-plan-rNNN.md`, `response-to-reviewers-rNNN.md`, and `revision-delta-rNNN.md`; the revised draft itself remains in `04_drafts/`.
- Call `academic-language-assessor` before final composition and after any language polishing pass. Save `05_evaluations/language-assessment-vNNN.md` and `06_revisions/round-NNN/language-change-log-rNNN.md`.
- If a language-only polishing pass saves a changed draft, create a new `perspective-vNNN.md` and record `change_type: language_only` in workflow state.

## Three Modes

| 模式 | 触发条件 | 执行步骤 | 产出 |
|------|---------|---------|------|
| **Lite** | "帮我理一下思路""这个方向能不能写" | STEP 1 → STEP 2-lite → STEP 3 | input-brief, provisional claim-ledger, provisional claim-evidence-matrix, argument-skeleton, early-feasibility-report |
| **Standard** | "帮我写一篇 Perspective 初稿" | STEP 1 → 2 → 3 → 4 → 5 → 6(1轮) | draft-v1/v2, full claim-ledger, evaluation-report, delta-report, response |
| **Full** | "这篇要投 X 刊"或要求投稿前审查 | 完整 1→9 | final manuscript + compositor report + submission-readiness |

Lite Mode 中 curator 仅做 provisional claim-ledger 和最小 claim-evidence-matrix，不启动完整证据检索。Standard Mode 中 refinement 默认 1 轮。Full Mode 是完整投稿前流程。

## Workflow

### STEP 0: Project Initialization

1. 确定项目名称和目录：默认 `<workspace>/research-perspective-projects/<project-name>/`，或用户显式指定的可写目录
2. 创建目录结构（00_input/, 01_claims/, 02_evidence/, 03_skeletons/, 04_drafts/, 05_evaluations/, 06_revisions/, 07_panel/, 08_final/, 09_state/, 10_delegates/）
3. 创建 `workflow-manifest.yaml`（初始状态）
4. 创建 `decision-log.md`（空日志）
5. 确定运行模式（根据用户意图判断 Lite / Standard / Full）

### STEP 1: Input Building

1. 加载 `perspective-input-builder`
2. 在 `00_input/` 下生成 `00-perspective-input-template.md`
3. 用户填写模板（或提供自然语言描述）
4. Input-builder 读回验证：
   - 无张力时：生成 2-4 个候选张力（标注 `system-proposed`），用户选择/修改/否定
   - 核心判断无法压缩为一句话：追问用户
   - 无 target outlet：选择 Generic Profile，不阻塞流程
5. 产出：`01-input-brief.md` + `target-outlet-profile.md` + `assumption-log.md`
6. 若 Lite Mode → 进入 STEP 2-lite，生成 provisional claim-ledger 与最小 claim-evidence-matrix 后再到 STEP 3

### STEP 2: Claim and Evidence Preparation

1. 加载 `perspective-claim-evidence-curator`
2. Curator 从 Input Brief 抽取候选 claims
3. 创建初始 `claim-ledger.md`（01_claims/ 目录）
4. 为每条 claim 匹配证据，标注二维强度（strength + directness）
5. 产出文件：claim-ledger.md, claim-evidence-matrix.md, existing-discourse-baseline.md, reference-list.md
6. 主动寻找反证 → `contrary-evidence-log.md`
7. 标注引用风险 → `citation-risk-log.md`
8. 若证据不足：
   - Lite Mode：标注 `gap`，不触发检索
   - Standard/Full Mode：调用 `research-opportunity-mapper`（A/B 路径）
9. Curator 是 claim-ledger 的唯一写入者

**STEP 2-lite 最小要求**：至少生成 `claim-ledger.md`、`claim-evidence-matrix.md`、`evidence-limitations.md`、`existing-discourse-baseline.md`。所有条目可标注 `provisional`，但不得省略 architect 所需输入。

### STEP 3: Argument Architecture

1. 加载 `perspective-argument-architect`
2. 输入：Input Brief + claim-ledger（只读）+ claim-evidence-matrix（只读）+ existing-discourse-baseline（只读）+ evidence-limitations（只读）
3. Architect 构建：问题场 → 贡献类型锚定 → 3-5 步论证链 → 叙事策略
4. 每步论证链必须标注：论证功能、映射 Claim ID、可争议约束（五选一）、证据配给
5. 产出 `02-argument-skeleton.md`
6. 如有 claim 变更需求：architect 提交 change request → orchestrator 审核 → curator 执行合并
7. 若 Lite Mode → 产出 `early-feasibility-report.md`，流程结束

### STEP 4: Drafting

1. 加载 `perspective-drafter`（起草模式）
2. 输入：Argument Skeleton + claim-ledger（只读）+ target-outlet-profile
3. 约束：严格按 Skeleton 结构推进，每段映射到 argument step + claim ID
4. 产出：`perspective-v001.md` + `perspective-v001-paragraph-map.md`
5. 禁止新增未登记 claim

### STEP 5: Independent Evaluation

1. 制备 delegate 隔离包：`10_delegates/evaluator-v001/`
   - 复制(input-brief, argument-skeleton, draft, paragraph-map, claim-ledger, claim-evidence-matrix, target-outlet-profile, existing-discourse-baseline)
   - 生成 README.md（白名单 + 边界声明）
2. 通过 delegation adapter 派发隔离 `perspective-evaluator` 实例
3. Evaluator 执行八维评分 + hard gates + 反模式检测 + 决策建议
4. 产出 `perspective-v001.md`
5. 路由决策：
   - `accept` → STEP 7（或 Standard Mode 则结束）
   - `minor_revision` → STEP 6（1轮）
   - `major_revision_draft` → STEP 6（≤2轮）
   - `argument_rebuild` → STEP 3
   - `evidence_rebuild` → STEP 2
   - `thesis_redesign` → STEP 1（需用户确认）
   - `outlet_retarget` → 更新 outlet profile（需用户确认）
   - `reject_not_salvageable` → 停止，输出诊断

### STEP 6: Refinement Loop

1. 加载 `perspective-refinement-controller`
2. 构建 revision plan（每条标注修改策略 + 入文策略）
3. 调度 `perspective-drafter`（修订模式）：
   - 产出：draft-v{N+1} + paragraph-map + response-to-reviewers + delta-report
4. 制备新 delegate 隔离包 → 派发新 evaluator 实例（隔离）
5. Re-evaluation → 决策路由
6. 停止条件：
   - Caveat budget 风险 → 三选一（收窄 thesis / 降低 claim strength / 拆分主张），记录 decision-log
   - 核心主张经限定后无贡献 → 硬停，路由 reject_not_salvageable
   - 死亡螺旋 → stop_no_gain
   - 达到最大轮次 → 记录 unresolved issues

### STEP 7: Independent Review Panel

1. 制备 3 份隔离包：
   - `panel-counter-position/`：draft + skeleton
   - `panel-02_evidence/`：draft + claim-evidence-matrix + claim-ledger + contrary-evidence-log
   - `panel-narrative/`：draft + target-outlet-profile（不含 skeleton）
2. 根据触发条件追加 conditional reviewer：methodology/statistics（方法、统计、因果、预测或 benchmark 主张）、practicing-clinician（临床、公共卫生或实践场景）、outlet-fit editor（明确 target outlet 或栏目）
3. 通过 delegation adapter 并行派发默认 3 个 + conditional reviewers
4. 各 reviewer 之间互不知晓，均不接触 evaluator reports
5. 每个 reviewer 须说明：如果 target outlet 更宽/更窄，建议是否会改变

### STEP 8: Panel Synthesis and Routing

1. Orchestrator 收集默认 3 份及所有 conditional individual review
2. 合成 panel-summary（共识问题：≥2 reviewer 指出 → 自动升级 must-fix）
3. 决策路由：
   - `strong_support` → STEP 9
   - `support_with_minor_revision` → STEP 8.5 → STEP 9
   - `support_after_major_revision` → STEP 6（major_revision_draft，≤1 轮 panel→revise→panel）
   - `not_ready` → STEP 3 或 STEP 4
   - `reject_or_redesign` → 停止

### STEP 8.5: Panel Minor Revision Patch

- 仅处理 panel must-fix items 标记为 minor/editorial 的条目
- 执行者：refinement-controller + drafter（修订模式）
- 约束：不新增 01_claims/evidence，仅局部段落级修改
- 产出 mini-delta-report
- 若触及实质性论证 → 升级为 major_revision，路由回 STEP 6

### STEP 9: Final Compositor

1. 制备隔离包：`10_delegates/final-compositor/`
   - 复制(draft-final, claim-ledger, claim-evidence-matrix, citation-risk-log, contrary-evidence-log, evidence-limitations, target-outlet-profile, panel-summary, reference-list)
2. 通过 delegation adapter 派发隔离 `perspective-final-compositor`
3. 五项审计：journal-fit / citation / title-abstract / anti-pattern / claim-consistency
4. Compositor 仅做非实质编辑，发现实质问题 → return route，不直接修
5. 产出：`08_final/final-perspective.md` + `final-edit-log.md` + `final-compositor-report.md` + `submission-readiness-report.md`

## Stop Conditions

- Readiness 不通过（Lite Mode 产出 early-feasibility-report）
- 不可修复 fatal flaw
- 证据不足且用户不补充
- 修订无增益（stop_no_gain）
- 核心主张经限定后无贡献
- Panel reject_or_redesign
- 用户在任何关键决策点选择停止

## Delegation Rules

- 所有 evaluator、panel reviewer、final-compositor 通过 delegation adapter 派发；Hermes 使用 `delegate_task`，Codex 使用独立子代理/隔离 brief
- 每次派发前制备独立隔离包（复制文件，不用软链接）
- Brief 必须含白名单 + 明确任务边界
- 子 agent brief 中声明："只评价/审计，不修订，不拓宽范围"
- 子 agent 输出必须声明实际读取文件清单；若运行时无法强制文件白名单，orchestrator 必须在 brief 和 manifest 中记录这是软隔离并降低可信度
- Delegate 模板见 `references/delegate-brief-templates.md`

## Pitfalls

- **构建自评**：不要自行判断 draft 质量——必须经过独立 evaluator
- **隔离泄漏**：delegate 包必须复制文件，不可暴露父目录路径
- **Lite Mode 过重**：Lite 中 curator 不做完整检索
- **claim-ledger 旁路**：任何非 curator 模块不得直接修改 ledger
- **Panel 污染**：panel reviewer 绝不可接触 evaluator reports
- **Final compositor 越权**：compositor 不可做实质修改
- **Mode 降级缺失**：发现上游缺陷时停止当前模式，不强行进入下一阶段

## References

- `references/delegate-brief-templates.md`：所有 delegate 子 agent 的 brief 模板
- `references/loop-control-rules.md`：修订循环停止条件与路由规则
- `references/panel-decision-routing.md`：Panel → 下一步路由表
- `references/anti-patterns.md`：跨组件共享的反模式清单
- `references/workflow-manifest-schema.md`：manifest.yaml 结构定义
- `references/decision-log-schema.md`：decision-log.md 结构定义
- `references/workflow-modes.md`：Lite/Standard/Full 模式定义与触发条件
- `references/io-contracts.md`：所有组件 I/O 合约汇总
- `references/generic-outlet-profiles.md`：Generic Profile 完整约束定义
