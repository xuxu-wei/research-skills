---
name: perspective-argument-architect
description: "Design a contestable Perspective argument chain, contribution, narrative, paragraph plan, and claim mapping before prose drafting."
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

### 8. State Implications and Boundaries

如果观点成立意味着什么？适用边界在哪里？

### 9. Submit Claim Change Requests (if needed)

如发现 claim-ledger 需要变更 → 提交 change request 至 `01_claims/change-requests/`。

## Contestability Constraints (五选一)

替代僵硬的可证伪条件，适用于不同类型 Perspective：

| 约束类型 | 定义 | 适用 |
|---------|------|------|
| 可证伪条件 | 什么证据会推翻该主张 | 经验性、机制性主张 |
| 可争议点 | 强反方会如何质疑 | 概念性、框架性主张 |
| 边界条件 | 什么情境下不成立 | 所有类型 |
| 替代解释 | 更简单/保守的解释 | 因果推断类 |
| 实施限制 | 实践约束是什么 | 转化性、政策类 |

每步至少选一种，多选鼓励。

## Pitfalls

- **论证跳跃**：步骤间缺少逻辑桥接
- **伪论点**：某步看起来像论证实为知识展示
- **strawman**：反方观点不是最强版本
- **框架代论证**：对仗结构先行，证据后填

## References

- Read `references/contribution-types.md` when its named guidance or contract applies.
- Read `references/tension-taxonomy.md` when its named guidance or contract applies.
- Read `references/argument-chain-template.md` when its named guidance or contract applies.
- Read `references/contestability-constraints.md` when its named guidance or contract applies.
