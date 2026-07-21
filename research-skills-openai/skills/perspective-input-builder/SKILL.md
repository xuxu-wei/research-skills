---
name: perspective-input-builder
description: "Normalize a Perspective thesis, audience, outlet, evidence, and constraints into an input brief and target-outlet profile."
---
# perspective-input-builder

## Purpose

将用户的模糊方向或已有材料转化为结构化的 Input Brief + Target Outlet Profile。不替用户发明核心判断，但可在张力缺失时生成候选选项供选择。

## Core Rules

- 不替用户"发明"张力——如果用户给的是主题而非张力，生成 2-4 个候选张力（标注 `system-proposed`），要求用户选择/修改/否定
- 不替用户做价值筛选——如果用户给了一个不值得写的方向，指出问题但不阻拦
- 不替用户发明 thesis——核心判断压不成一句话时追问
- Target outlet 缺失时不阻塞——选择 Generic Profile，并将 outlet-fit 标注为 `provisional`
- 具体期刊/栏目 profile 必须记录来源：`user-provided`、`generic` 或 `retrieved-guidelines`；无法验证投稿指南时不得声明 ready for human sign-off
- 明确目标读者已经知道什么、不能假定什么，以及文章希望读者完成的认识转变；不得以“专业读者”替代具体先验知识
- 只为会影响理解顺序的核心概念记录术语披露顺序，不生成穷尽式术语表
- 用户材料或文献线索必须记录预期用途和允许支撑的命题；未经 curator 核验，不得把初步用途当作已验证的引文绑定
- 用户提供已有稿件时，可读取但不自动修改
- 所有候选选项必须标注来源（`user-provided` 或 `system-proposed`）
- 输入完整性只记录只读路径和简单的未修改确认；不得计算、报告或持久化
  SHA、content hash、checksum 或 digest

## I/O Contract

```
Allowed Inputs:
  - 用户自然语言描述（方向、张力、判断、材料）
  - 00-perspective-input-template.md（用户填写后）
  - 用户明确提供的 existing draft / outline / prior notes

Required Outputs:
  - 01-input-brief.md
  - target-outlet-profile.md（或 Generic Profile）
  - assumption-log.md

Conditional Output:
  - 00-perspective-input-template.md（仅在现有输入不足、必须交由用户补填时生成）

May Read:
  - 用户明确提供的 existing manuscript, outline, notes, or review comments
  - 用户填写的 00-perspective-input-template.md

May Write:
  - 00_input/ 目录下文件

Must Not Read:
  - 任何非用户显式指定的项目目录文件（不得主动扫描项目目录）

Must Not Write:
  - 任何 00_input/ 目录外的文件

May Call:
  - 无外部 skill

Must Not Call:
  - 任何评价型 skill

Failure Modes:
  - 用户只给主题无张力 → 生成 2-4 候选张力(system-proposed)，不自行判定
  - 用户拒绝所有候选张力 → 停止，等待用户重新输入
  - 核心判断无法压缩 → 返回用户追问，不替用户发明 thesis

Escalation Route:
  - 方向性分歧无法调和 → 上报 orchestrator
```

## Procedure

### 1. Normalize or Request Missing Input

输入已足以形成可识别张力、核心判断和读者转变时，直接整理下列 14 个字段；
不要额外生成一份已代填的输入模板。只有缺失信息确实需要用户填写时，才在
`00_input/00-perspective-input-template.md` 生成模板并暂停等待。字段为：

1. **Working Topic**：文章暂定主题（一句话）
2. **Target Outlet**：目标期刊/平台、栏目类型（Perspective/Viewpoint/Commentary/Opinion/Analysis）、目标读者、字数上限、参考文献上限、是否需摘要、是否允许图表/Box
3. **Field Tension**：当前领域主流看法、误区/盲点/未解决张力、为什么现在值得讨论
4. **Core Thesis**：一句话核心判断、读者应记住的一句话
5. **Contribution Type**：主导类型（Reframing/Synthesis/Critique/Agenda-setting/Translational/Ethical-social/Other）+ 次要
6. **Intended Shift in Reader Understanding**：读者读完后应从什么理解转向什么理解
7. **Reader Baseline**：目标读者、可假定的先验知识、必须解释的概念、预期认识转变
8. **Terminology and Disclosure Order**：核心概念首次出现、定义顺序、可接受简称或需要避免的歧义
9. **Reader Reasoning Handoff**：领域张力 → 核心判断 → 论证步骤 → 最强反方与边界 → 影响的预期阅读路径
10. **Source Intent and Binding**：材料或来源线索的预期功能、允许支撑的命题、所需定位信息和禁止外推
11. **Evidence Base**：已有证据、证据缺口、可能反证、只能弱表达的主张
12. **Boundary Conditions and Counterargument Families**：适用/不适用场景、最强反方，以及不得混并的边界或反方家族
13. **Authorial Position**：专业身份/视角、方法学/政策立场、潜在利益冲突
14. **Desired Output**：初稿/投稿稿/修改现有稿件、是否需图表建议、是否需 cover letter

### 2. Read Back and Validate

用户填写后读回模板内容，逐字段验证：

| 字段 | 通过条件 | 不通过时动作 |
|------|---------|-------------|
| Field Tension | 存在可识别的张力（不是纯主题描述） | 生成 2-4 个候选张力（标注 system-proposed），用户选择 |
| Core Thesis | 可压缩为一句话，含明确立场 | 追问：写不出来说明判断未成熟 |
| Target Outlet | 至少填写目标期刊或栏目类型 | 不阻塞，选择 Generic Profile |
| Reader Baseline | 列出可假定与必须解释的知识 | 缺失时标记为 provisional，不自行假定专科知识 |
| Reader Reasoning Handoff | 五个功能均有目标，或明确标注待 architect 完成 | 缺少关键认识转变时追问 |
| Terminology Order | 核心概念在依赖它的论证前得到说明 | 记录待 architect 排序，不生成术语清单 |
| Source Intent and Binding | 每条用户材料/来源线索有预期功能与允许命题 | 标记 `provisional` 并交 curator 核验 |
| Evidence Base | 已标注已有/缺口/反证状态 | 允许缺口存在，标记为 curator 的工作任务 |

### 3. Generate Target Outlet Profile

- 用户指定了目标期刊 → 生成 `target-outlet-profile.md`（含期刊定位、读者、篇幅、结构偏好等），并记录 profile source、guideline source、last checked date（如可得）
- 用户未指定 → 选择最接近的 Generic Profile（见 `../perspective-orchestrator/references/generic-outlet-profiles.md`），outlet-fit 标注为 `provisional`

### 4. Generate Assumption Log

记录 input-builder 过程中做出的隐含假设：

```markdown
## Assumption Log

A1: [假设内容]
  - Basis: [用户表述 / system-inferred]
  - Risk if wrong: [影响]
  - Validation: [如何验证]

A2: ...
```

### 5. Produce Input Brief

将验证后的信息整理为 `01-input-brief.md`，包含：
- 精炼后的核心判断（如已具备）
- 张力类型与具体描述
- 贡献类型锚定
- 目标读者、可假定的先验知识与必须解释的知识
- 核心术语及其依赖顺序，不建立穷尽式术语表
- 领域张力、核心判断、论证、反方/边界和影响之间的 reader-reasoning handoff
- 用户材料和来源线索的 provisional source-intent/binding 约束
- 证据基础状态摘要
- Target outlet 约束
- 边界/反方家族与作者立场
- 待解决问题清单

## Execution Order

读取唯一获准的项目输入后，只先判断张力、核心判断和读者转变是否足以继续。
如果确实需要用户补填，只生成 `00_input/00-perspective-input-template.md`，暂停并返回
`next_route: clarification_required`，不要建立三个正常产物。否则立即建立
`01-input-brief.md`、`target-outlet-profile.md` 和 `assumption-log.md` 三个必要文件，
再逐项补全和验证。未知内容写为 `provisional` 或待核验；不得为追求完整而延迟
首次写入、扩大检索，或生成不需要用户填写的模板副本。

## Pitfalls

- **替用户发明张力**：用户只给出主题 X 时，不要自行把它改写成某个具体的实施缺口或价值冲突
- **跳过验证**：即使模板看起来填完了，也要检查每个字段是否达到可消费的质量
- **忽略 authorial position**：作者身份和立场会显著影响 Perspective 的叙事策略选择
- **过度追问**：用户明确说"不确定"的字段，标注为待定并继续，不要卡住流程

## References

- Use `templates/perspective-input-template.md` only when producing the conditional user-fill template.
