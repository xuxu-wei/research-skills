---
name: perspective-input-builder
description: Use when 生成 Perspective 输入模板，读回用户填写内容并验证，产出结构化 Input Brief 和 Target Outlet Profile，并支持候选张力生成、Generic Profile 缺省。
version: 1.0.0
author: Xuxu Wei
license: MIT
metadata:
  hermes:
    tags: [research-perspective, perspective, input, template, brief]
    related_skills:
      - perspective-orchestrator
---

# perspective-input-builder

## Purpose

将用户的模糊方向或已有材料转化为结构化的 Input Brief + Target Outlet Profile。不替用户发明核心判断，但可在张力缺失时生成候选选项供选择。

## Core Rules

- 不替用户"发明"张力——如果用户给的是主题而非张力，生成 2-4 个候选张力（标注 `system-proposed`），要求用户选择/修改/否定
- 不替用户做价值筛选——如果用户给了一个不值得写的方向，指出问题但不阻拦
- 不替用户发明 thesis——核心判断压不成一句话时追问
- Target outlet 缺失时不阻塞——选择 Generic Profile，并将 outlet-fit 标注为 `provisional`
- 具体期刊/栏目 profile 必须记录来源：`user-provided`、`generic` 或 `retrieved-guidelines`；无法验证投稿指南时不得声明 submission-ready
- 用户提供已有稿件时，可读取但不自动修改
- 所有候选选项必须标注来源（`user-provided` 或 `system-proposed`）

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

### 1. Generate Input Template

在 `00_input/00-perspective-input-template.md` 生成模板文件。模板包含以下 10 个字段：

1. **Working Topic**：文章暂定主题（一句话）
2. **Target Outlet**：目标期刊/平台、栏目类型（Perspective/Viewpoint/Commentary/Opinion/Analysis）、目标读者、字数上限、参考文献上限、是否需摘要、是否允许图表/Box
3. **Field Tension**：当前领域主流看法、误区/盲点/未解决张力、为什么现在值得讨论
4. **Core Thesis**：一句话核心判断、读者应记住的一句话
5. **Contribution Type**：主导类型（Reframing/Synthesis/Critique/Agenda-setting/Translational/Ethical-social/Other）+ 次要
6. **Intended Shift in Reader Understanding**：读者读完后应从什么理解转向什么理解
7. **Evidence Base**：已有证据、证据缺口、可能反证、只能弱表达的主张
8. **Boundary Conditions**：适用场景、不适用场景、最容易被反驳的地方
9. **Authorial Position**：专业身份/视角、方法学/政策立场、潜在利益冲突
10. **Desired Output**：初稿/投稿稿/修改现有稿件、是否需图表建议、是否需 cover letter

### 2. Read Back and Validate

用户填写后读回模板内容，逐字段验证：

| 字段 | 通过条件 | 不通过时动作 |
|------|---------|-------------|
| Field Tension | 存在可识别的张力（不是纯主题描述） | 生成 2-4 个候选张力（标注 system-proposed），用户选择 |
| Core Thesis | 可压缩为一句话，含明确立场 | 追问：写不出来说明判断未成熟 |
| Target Outlet | 至少填写目标期刊或栏目类型 | 不阻塞，选择 Generic Profile |
| Evidence Base | 已标注已有/缺口/反证状态 | 允许缺口存在，标记为 curator 的工作任务 |

### 3. Generate Target Outlet Profile

- 用户指定了目标期刊 → 生成 `target-outlet-profile.md`（含期刊定位、读者、篇幅、结构偏好等），并记录 profile source、guideline source、last checked date（如可得）
- 用户未指定 → 选择最接近的 Generic Profile（见 `perspective-orchestrator/references/generic-outlet-profiles.md`），outlet-fit 标注为 `provisional`

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
- 证据基础状态摘要
- Target outlet 约束
- 边界条件与作者立场
- 待解决问题清单

## Pitfalls

- **替用户发明张力**：用户说"AI in medicine"，不要自己写成"AI 的 clinical workflow integration gap"
- **跳过验证**：即使模板看起来填完了，也要检查每个字段是否达到可消费的质量
- **忽略 authorial position**：作者身份和立场会显著影响 Perspective 的叙事策略选择
- **过度追问**：用户明确说"不确定"的字段，标注为待定并继续，不要卡住流程

## References

- `templates/perspective-input-template.md`：用户填写的输入模板
