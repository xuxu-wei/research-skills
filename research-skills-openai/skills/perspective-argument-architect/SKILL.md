---
name: perspective-argument-architect
description: "Plan a reader-facing Perspective argument, paragraphs, handoffs, and claims."
---
# perspective-argument-architect

## Purpose

将核心判断展开为可检验的论证骨架。这是 Perspective 独有的步骤——它不问"做什么研究"，而问"用什么论证结构来讲这个故事"。

输出一份"施工图"：drafter 按图施工，evaluator 按图检验。

## Core Rules

- 论证链 3-5 步，每步映射至少一个 Claim ID
- 每步标注论证功能——不是"这步讲什么主题"，而是"这步推进了论证链的哪一环"
- 每步标注至少一种可争议约束（五选一）
- 每个主要 section 须声明论证功能
- 不得依赖纯 illustrative 证据支撑论证步骤（除非显式标注 `[illustrative only]`）
- 保留 Input Brief 的 declared readers、prior knowledge 和 intended shift，并把它们落实为可追踪的 reader-reasoning handoff
- 核心概念必须按依赖关系排序，在读者需要使用概念前完成首次解释；不创建独立术语裁决
- 每个 Evidence ID 只能按 curator 核验的 source intent、允许命题、强度和 locator 使用；需要改变用途时提交 change request
- 每个不同的反方或边界家族指定一个权威阐释位置；其他位置原则上省略，只有紧邻推理会因省略而失真时才保留自包含的局部边界，且不得用指针代替
- 不直接修改 claim-ledger——如有变更需求，提交 change request

## I/O Contract

```
Allowed Inputs:
  - 01-input-brief.md
  - target-outlet-profile.md
  - claim-ledger.md（只读）
  - claim-evidence-matrix.md（只读）
  - existing-discourse-baseline.md（只读）
  - evidence-limitations.md（只读）

Required Outputs:
  - 02-argument-skeleton.md
  - 如有 claim 变更: 01_claims/change-requests/architect-request-v{N}.md

May Read:
  - 00_input/ 目录
  - 01_claims/ 目录（只读）
  - 02_evidence/ 目录（只读）

May Write:
  - 03_skeletons/ 目录
  - 01_claims/change-requests/ 目录

Must Not Read:
  - 任何 draft 文件
  - 任何 evaluation 文件

Must Not Write:
  - claim-ledger.md
  - claim-evidence-matrix.md
  - 任何 draft 文件

May Call:
  - 无外部 skill

Must Not Call:
  - 任何评价型 skill
  - drafter

Failure Modes:
  - 论证链某步无法匹配证据 → 标注证据缺口，建议降低对应 claim strength
  - 论证链无法闭合 → 回报 orchestrator

Escalation Route:
  - claim-ledger 与 thesis 严重冲突 → 上报 orchestrator
```

## Procedure

### 1. Refine Core Thesis

从 Input Brief 提取核心判断，进一步精炼为一句话 thesis。

同时冻结 reader entry contract：目标读者、可假定的先验知识、不能假定的知识、预期认识转变。若这些信息互相冲突，返回 input-builder。

### 2. Anchor Contribution Type

从 6 种类型中确定主导类型并声明次要类型：
- Reframing: 重新定义一个问题
- Synthesis: 整合分散证据提出新解释
- Critique: 批判当前方法/政策/理论的缺陷
- Agenda-setting: 提出未来研究或行动路线
- Translational: 将科学发现转化为临床/政策/实践意义
- Ethical/social: 指出技术或实践背后的伦理/社会/制度问题

### 3. Build Problem Field

不堆砌文献——画"讨论格局"：
- 当前主流叙事是什么？
- 盲点在哪里？
- 为什么现在需要新视角？

### 4. Design Argument Chain (3-5 Steps)

每步记录：

```markdown
### Step N: [主张简述]
- Argument function: [这一步推进了什么？]
- Claim ID: [C{N}]
- Evidence: [E{N}] — Evidence strength: [...] Directness: [...]
- Source binding: [Binding ID] — Intended function: [...] Allowed proposition: [...] Locator: [...]
- Contestability constraint (至少一种):
  - Falsifiable condition: [什么证据会推翻？] 或
  - Debatable point: [强反方如何质疑？] 或
  - Boundary condition: [什么情境下不成立？] 或
  - Alternative explanation: [更简单/保守的解释？] 或
  - Implementation limit: [实践约束是什么？]
- Vulnerability: [最容易被攻击的环节]
- Competing hypothesis: [替代解释]
```

### 5. Select Narrative Strategy

- 揭露盲区型：建立读者的默认假设，然后打破它
- 连接孤岛型：展示两个看似无关领域的深层统一性
- 教训叙事型：从一个失败/缺失出发，推导结构性原因

### 6. Design Opening Anchor

用什么具体张力、悖论或意外事实开场？不是泛化背景介绍。

### 7. Pre-embed Counterarguments

预期的最强反对意见及处理策略——不 strawman。

为每个科学上不同的反方或边界分配 `family_id` 和唯一 authority location。不要把不同家族压缩为一个通用 limitations 段，也不要在其他位置放置“见限制部分”一类指针。

### 8. State Implications and Boundaries

如果观点成立意味着什么？适用边界在哪里？

### 8.5. Bind Reader Reasoning and Terminology Order

- 将 `field tension -> thesis -> ordered argument steps -> strongest counterarguments/boundaries -> implications` 的每个功能绑定到具体 step 或 section。
- 列出只对目标读者构成理解门槛的核心概念、依赖关系、首次解释位置和允许简称。
- 检查每个 source binding 的 intended function、允许命题、claim strength 与 locator；不得用来源声望替代命题绑定。

### 9. Submit Claim Change Requests (if needed)

如发现 claim-ledger 需要变更 → 提交 change request 至 `01_claims/change-requests/`。

## Execution Order

- 先只读 Input Brief 与 claim ledger，立即建立 `03_skeletons/02-argument-skeleton.md`，写入 thesis、reader entry contract、3–5 个带 Claim ID 的步骤标题和 unresolved questions；在读取完整 matrix 或 evidence bundle 前必须先保存这一检查点。
- 同一 architect 一次只补全一个 argument step：按该步的 Claim ID/Binding ID 定向读取 matrix、discourse 与 limitations，写回后再处理下一步。
- 最后补全叙述策略、反方/边界权威位置、reader handoff 和术语披露顺序。若合并读取被截断，改用按 Claim ID/Binding ID 的定向读取；不得把全部输入重新装入内存后才首次写入，也不得拆给多个 architect。完成后按 I/O contract 验证整份 skeleton。

## Contestability Constraints (五选一)

按主张类型选择可证伪条件、可争议点、边界条件、替代解释或实施限制；每步至少一种。完整定义见对应 reference。

## Pitfalls

- **论证跳跃**：步骤间缺少逻辑桥接
- **伪论点**：某步看起来像论证实为知识展示
- **strawman**：反方观点不是最强版本
- **框架代论证**：对仗结构先行，证据后填
- **读者基线漂移**：一段按专科读者写，下一段又从基础概念重新教学
- **来源改作他用**：同一引文从背景线索被无声升级为核心因果或效果证据
- **限制重复或指针化**：同一反方在多处完整复述，或用“见后文限制”代替必要的局部边界

## References

- Read `references/contribution-types.md` when its named guidance or contract applies.
- Read `references/tension-taxonomy.md` when its named guidance or contract applies.
- Read `references/argument-chain-template.md` when its named guidance or contract applies.
- Read `references/contestability-constraints.md` before Procedure Step 4.
