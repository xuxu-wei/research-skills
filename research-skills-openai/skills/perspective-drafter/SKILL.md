---
name: perspective-drafter
description: "Draft or revise a versioned Perspective from approved argument and claim artifacts, keeping reviewer responses separate."
---
# perspective-drafter

## Purpose

将论证骨架转化为可发表的 Perspective 文章。严格按骨架施工，不自行扩展主题。每段承担明确的论证功能。修订模式产出双文件（修订稿 + response-to-reviewers）。

## Core Rules

- 严格按 Argument Skeleton 的结构推进，不扩展新论点
- 每段映射到 argument step + claim ID + evidence ID（如涉及证据）
- 无法映射的段落标记 `[orphan paragraph risk]`
- 禁止新增未在 claim-ledger 中登记的 claim
- 开场用具体锚点，不用泛化背景
- 立场校准：有判断力但克制
- 减法优先：每句话要么推进论证，要么删除
- 语言润色模式只能处理 `academic-language-assessor` 或 revision plan 指定的语言问题；保存 `06_revisions/round-NNN/language-change-log-rNNN.md`，不得新增 claim。
- 证据选择而非罗列：每步只用最关键证据

## I/O Contract

```
Allowed Inputs:
  - 02-argument-skeleton.md
  - claim-ledger.md（只读）
  - claim-evidence-matrix.md（只读）
  - target-outlet-profile.md
  - evidence-map.md（只读）
  - [修订模式额外] revision-plan.md + 当前 draft + 前次 evaluation report

Required Outputs:
  - 起草: perspective-v{N}.md + perspective-v{N}-paragraph-map.md
  - 修订: perspective-v{N+1}.md + perspective-v{N+1}-paragraph-map.md + 06_revisions/round-NNN/response-to-reviewers-rNNN.md

May Read:
  - 03_skeletons/ 目录
  - 01_claims/ 目录（只读）
  - 02_evidence/ 目录（只读）
  - 00_input/ 目录

May Write:
  - 04_drafts/ 目录
  - 06_revisions/ 目录

Must Not Read:
  - 07_panel/ 目录
  - 10_delegates/ 目录

Must Not Write:
  - claim-ledger.md
  - argument-skeleton.md
  - 任何 evaluation 文件

May Call:
  - 无外部 skill

Must Not Call:
  - 任何评价型 skill

Failure Modes:
  - 出现 skeleton 未覆盖的论证需求 → 标记 [unregistered claim risk]，上报 orchestrator
  - 篇幅超标 → 标注超标段落，请求用户确认
  - 修订导致 caveat budget 风险 → 标记每条新增限定

Escalation Route:
  - 超出 skeleton 范围的论证需求 → 上报 orchestrator
```

## Modes

### Fresh Draft Mode

输入：Argument Skeleton + claim-ledger + target-outlet-profile
输出：perspective-v{N}.md + perspective-v{N}-paragraph-map.md

典型结构：
1. Opening anchor — 具体张力、悖论或意外事实
2. Problem statement — 当前框架/做法的盲区
3. Central thesis — 核心判断
4. Argument chain — 逐步推进，每段承担一步
5. Proposed framework/reframing — 新视角
6. Implications — 对研究/实践/政策的影响
7. Boundaries and counterarguments — 克制与诚实
8. Conclusion — 回到开场张力，展示化解

### Revision Mode

输入：当前 draft + Revision Plan（含每条修改的入文策略标注）
输出双文件：
- perspective-v{N+1}.md + perspective-v{N+1}-paragraph-map.md（修订后稿件）
- 06_revisions/round-NNN/response-to-reviewers-rNNN.md（点对点回复）

每条修改标注入文策略：
- `入正文`：直接修改 draft
- `仅入回应`：只写入 response 文件
- `不处理`：记录原因

修订策略：追加 / 替换 / 浓缩 / 删减 / 澄清。减法优先。

## Paragraph Mapping

每段在 paragraph-map 中记录：

```markdown
Paragraph N
- Function: [Opening tension / Problem statement / Thesis / Argument Step N / ...]
- Argument step: [Step{N} from skeleton]
- Claim ID: [C{N}]
- Evidence used: [E{N} 或 none]
- Risk: [anti-pattern risk 或 none]
```

## Style Constraints

- 立场语言："We argue that..." "Current evidence suggests..." "A more useful framing may be..."
- 禁止："毫无疑问..." "唯一正确方向是..." "所有现有研究都忽略了..." "这将彻底改变..."
- 不要教学式修辞问句（"你是否想过……？"）
- 不要叙事化临床场景开场（除非 narrative strategy 明确要求）
- 篇幅控制：严格遵守 target-outlet-profile 中的上限

## Pitfalls

- **迷你综述化**：主题组织替代论证组织
- **caveat creep**：核心主张被限定蚕食
- **未登记新 claim**：起草中产生新主张未上报
- **orphan paragraph**：某段不推进任何论证步骤
- **过度引用**：证据展示替代论证推进
- **开场空泛**："Recent years have seen growing interest in..."

## References

- Read `references/narrative-strategies.md` when its named guidance or contract applies: ：3 种叙事策略及结构模板
- Read `references/stance-calibration.md` when its named guidance or contract applies: ：立场强度语言校准
- Read `references/style-guidelines.md` when its named guidance or contract applies: ：篇幅控制、段落功能标注、减法规则
