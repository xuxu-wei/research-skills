---
name: perspective-drafter
description: "Draft or revise one complete Perspective from approved argument artifacts or one YAML repair brief."
---
# perspective-drafter

## Purpose

将论证骨架转化为可发表的 Perspective 文章。严格按骨架施工，不自行扩展主题。每段承担明确的论证功能。修订模式产出双文件（修订稿 + response-to-reviewers）。

## Core Rules

- 严格按 Argument Skeleton 的结构推进，不扩展新论点
- 每段映射到 argument step + claim ID + evidence ID（如涉及证据）
- 每次引文使用映射到 source Binding ID，并保持其 source intent、允许命题、locator 与 claim-strength 边界
- 无法映射的段落标记 `[orphan paragraph risk]`
- 禁止新增未在 claim-ledger 中登记的 claim
- 开场用具体锚点，不用泛化背景
- 立场校准：有判断力但克制
- 减法优先：每句话要么推进论证，要么删除
- 科学冻结前，revision mode 只能处理当前 scientific revision plan 明列的语言问题；科学冻结后，任何语言改动都只能来自单一 `editorial-repair-brief-rNNN.yaml`，由原 writer 执行并重跑全部 editorial/final gates。不得新增 claim。
- 证据选择而非罗列：每步只用最关键证据
- 按 skeleton 的 reader baseline 和 terminology order 披露概念；不得生成新的术语裁决或改变已核验含义
- 每个 counterargument/boundary family 只在其 authority location 完整阐释；其他位置仅在紧邻推理必需时保留自包含局部边界，不得写指针或重复完整阐释
- 每个 draft handoff 记录 `writer_instance_id`；editorial repair 必须由产生当前科学版本的同一 writer instance 执行，否则返回 `editorial_repair_pending`

## I/O Contract

```
Allowed Inputs:
  - 02-argument-skeleton.md
  - claim-ledger.md（只读）
  - claim-evidence-matrix.md（只读）
  - target-outlet-profile.md
  - evidence-map.md（只读）
  - [科学修订模式额外] controller 生成的 revision-plan.md + 当前 draft；不得读取原始 evaluation 或 panel report
  - [editorial repair 额外] 当前冻结 draft + 单一 editorial-repair-brief-rNNN.yaml + protected-content-register-rNNN.yaml

Required Outputs:
  - 起草: perspective-v{N}.md + perspective-v{N}-paragraph-map.md
  - 修订: perspective-v{N+1}.md + perspective-v{N+1}-paragraph-map.md + 06_revisions/round-NNN/response-to-reviewers-rNNN.md
  - editorial repair: perspective-v{N+1}.md + perspective-v{N+1}-paragraph-map.md + editorial-revision-delta-rNNN.yaml

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
  - 科学修订时的原始 evaluator/panel reports（只使用 controller 规范化的 revision plan）
  - editorial repair 时的原始 narrative/language assessment、旧 evaluation、旧 repair plan 或其他 reviewer 报告

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

## Execution Order

Fresh Draft Mode 必须由同一 writer 渐进写入同一对输出文件：

1. 先只从 skeleton 定向读取 thesis、reader contract、section/step 标题及其 Claim ID/Binding ID 集合，并读取 outlet 篇幅；不要先载入完整 matrix 或 evidence bundle。
2. 立即建立 `04_drafts/perspective-v{N}.md` 和 `04_drafts/perspective-v{N}-paragraph-map.md`：前者先写标题、功能性 section 标题、opening anchor 与 central thesis，后者登记已写段落和待完成 section。这是同一版本的过程检查点，未完成前不得冻结或交给 evaluator。
3. 同一 writer 一次只完成一个 section：按该 section 的 Claim ID/Binding ID 定向读取 ledger、matrix 与 evidence locator，写回正文后立即更新 paragraph map，再处理下一节。若合并读取被截断，改用按 Claim ID/Binding ID 的定向读取；不得等到把全部输入装入内存后才首次写入，也不得拆给多个 writer。
4. 全部 section 完成后，按 paragraph map 复核引用过的 claim/binding、术语顺序、authority location、篇幅和 orphan 风险，清除过程标记；只有两份完整文件可以进入 conformance 或 evaluation。

Revision 与 Editorial Repair 先从冻结稿建立新的完整版本，再由同一 writer 按 action 依赖和 section 逐项修改，并同步 map、response 或 delta；旧版本保持不变，未完成的新版本不得交接。

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

输入：当前 draft + controller 规范化的 Revision Plan（含每条修改的入文策略标注；不含原始评审报告）
输出双文件：
- perspective-v{N+1}.md + perspective-v{N+1}-paragraph-map.md（修订后稿件）
- 06_revisions/round-NNN/response-to-reviewers-rNNN.md（点对点回复）

每条修改标注入文策略：
- `入正文`：直接修改 draft
- `仅入回应`：只写入 response 文件
- `不处理`：记录原因

修订策略：追加 / 替换 / 浓缩 / 删减 / 澄清。减法优先。

### Editorial Repair Mode

只在科学修订完成、当前版本冻结、并由独立 narrative 与 language assessment 生成单一 YAML repair brief 后使用。

1. 核对 `writer_instance_id` 与当前科学版本 writer 完全一致。
2. 只执行 brief 中声明的 action；按依赖顺序处理 narrative 与 language action，不读取原始评审。
3. 对每个 action 记录 `applied | not_applied_with_reason`、源/目标 locator、实际 operation 和 acceptance-test 结果。
4. 遵守 protected-content register；不得改变 thesis、scope、claim strength、evidence status、source binding、反方/边界家族或 authority location 的科学含义。
5. 任何需要科学变化的 action 标为 `scientific_change_required` 并停止，不得以编辑性修改实现。

## Paragraph Mapping

每段在 paragraph-map 中记录：

```markdown
Paragraph N
- Function: [Opening tension / Problem statement / Thesis / Argument Step N / ...]
- Argument step: [Step{N} from skeleton]
- Claim ID: [C{N}]
- Evidence used: [E{N} 或 none]
- Source binding IDs: [B{N} 或 none]
- Terminology introduced/defined: [term/function 或 none]
- Counterargument/boundary family: [family ID + authority/local/none]
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
- **binding drift**：引文仍在，但被用于 binding 未授权的命题或强度
- **editorial science drift**：编辑修复改变了 claim、evidence status、scope 或反方/边界含义
- **开场空泛**："Recent years have seen growing interest in..."

## References

- Read `references/narrative-strategies.md` when its named guidance or contract applies: ：3 种叙事策略及结构模板
- Read `references/stance-calibration.md` when its named guidance or contract applies: ：立场强度语言校准
- Read `references/style-guidelines.md` when its named guidance or contract applies: ：篇幅控制、段落功能标注、减法规则
