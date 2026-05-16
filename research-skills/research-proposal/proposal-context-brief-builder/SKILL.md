---
name: proposal-context-brief-builder
description: Build a concise proposal context brief from a raw research idea, promoted
  idea package, funding call, clinical problem, data opportunity, or user constraints.
  Extracts known facts, assumptions, missing information, and proposal-relevant constraints
  for downstream readiness triage and drafting.
version: 1.0.0
author: Xuxu Wei
license: MIT
metadata:
  hermes:
    tags:
    - research-proposal
    - context-brief
    - proposal
    - research-idea
    - triage
    - drafting
    related_skills:
    - proposal-orchestrator
    - research-opportunity-mapper
    - proposal-readiness-triage
    - proposal-drafter
    - proposal-evaluator
    - proposal-refinement-controller
    - methodology-statistics-preflight
    - sap-writer
    - sap-evaluator
    - sap-refinement-controller
    - proposal-review-panel
    - proposal-package-assembler
---

# proposal-context-brief-builder

## When to Use

当用户提供 raw research idea、promoted idea package、funding call、临床问题、数据机会、组会方向、已有文献摘要或研究约束，并需要进入 proposal readiness triage 或 proposal drafting 前，使用本 skill。

本 skill 的任务是整理上下文，而不是判断 idea 是否 proposal-ready，也不是撰写 proposal。

## Core Principles

- 只提取和组织用户已提供的信息，不补造关键事实。
- 明确区分 confirmed facts、assumptions、unknowns 和 constraints。
- 输出应足够支持 `proposal-readiness-triage` 判断是否可进入 proposal drafting。
- 不进行最终 readiness 判断。
- 不评价 proposal 质量。
- 不生成 proposal 正文。
- 不在本 SKILL.md 中内嵌 schema、template、reference 正文、rubric 或代码；只引用对应文件路径。

## Inputs

可接受以下输入：

- raw research idea；
- promoted idea package；
- research-idea workflow 输出；
- funding call 或申请要求；
- 临床、工程、社会或方法学问题；
- 数据集、队列、实验平台或系统机会；
- 已有文献摘要、evidence summary 或用户上传材料摘要；
- 用户目标、目标产出、时间、资源、伦理、协作或方法限制；
- 用户是否明确要求 SAP、protocol 或统计分析计划。

## Procedure

### 1. Identify Input Type

先判断输入属于哪一类或哪几类：

- raw idea；
- promoted idea package；
- funding call；
- clinical / practical problem；
- data opportunity；
- literature-driven topic；
- method-driven topic；
- user constraint-driven topic。

若输入混合多种类型，应全部记录，不强行归为单一类型。

### 2. Extract Core Research Context

从输入中提取 proposal 相关信息：

- research domain；
- working title，如可推断；
- research question；
- hypothesis or objective；
- target population、system、dataset 或 study object；
- intervention、exposure、predictor 或 comparison，如适用；
- endpoint、outcome、metric 或 deliverable；
- proposed method or design；
- available data or required data；
- intended output；
- user goal；
- timeline、resource、ethics、collaboration 或 feasibility constraints。

无法从输入中确认的信息，标记为 unknown，不要自行补全。

### 3. Separate Facts, Assumptions, and Unknowns

将内容分为：

- confirmed facts：用户明确给出的事实；
- reasonable assumptions：为组织 brief 所需、但未被用户确认的轻量假设；
- critical unknowns：会影响 readiness triage、drafting、methodology 或 SAP 的缺口；
- non-critical unknowns：暂不阻断下一步的缺口。

critical unknowns 应写成可供 triage 判断的问题，而不是直接向用户提问。

### 4. Extract Constraints

整理所有已知约束：

- target output；
- field or topic boundary；
- available data；
- unavailable data；
- method preference or prohibition；
- sample size or cohort limits；
- time and resource limits；
- ethical, privacy, regulatory or IRB constraints；
- collaborator or reviewer expectations；
- target journal, grant, protocol or institutional requirement；
- SAP requirement, if explicitly requested。

若用户没有明确要求 SAP，应记录 `sap_requested: false`，不得默认启动 SAP 分支。

### 5. Prepare Downstream Brief

生成可供 `proposal-readiness-triage` 使用的 context brief。

brief 应支持下游判断：

- idea 是否足够明确；
- proposal drafting 是否可以开始；
- 是否需要用户澄清；
- 是否应回到 research-idea workflow；
- 是否存在 methodology concern；
- 是否存在 SAP 分支需求。

本 skill 不做这些判断，只准备材料。

### 6. Handoff

将 context brief 交给 `proposal-readiness-triage`。

handoff 内容至少包括：

- input type；
- normalized idea summary；
- known context；
- user goal；
- intended output；
- constraints；
- available data；
- proposed or implied methods；
- outcomes / endpoints / metrics；
- assumptions；
- critical unknowns；
- SAP requested status；
- source notes。

## Output

输出一个 concise proposal context brief。

输出应简洁、结构化、可被下游 agent 直接使用。不要输出完整 proposal，不要输出长篇文献综述。

## Delegation Rules

本 skill 通常不需要派发子 agent。

如输入材料很长、来源复杂，或包含多份上传材料，可请求 orchestrator 先进行材料摘要或证据整理；但本 skill 本身不执行 evaluation，也不派发 readiness、methodology 或 review 子 agent。

## Stop Conditions

以下情况应停止 context brief 构建并返回问题说明：

- 用户输入完全没有 research idea 或研究方向；
- 输入只包含行政性请求，无法转化为研究上下文；
- 用户目标与 research proposal 无关；
- 材料不足到无法形成最小 idea summary。

若仍能形成最小 idea summary，应继续生成 context brief，并把缺口标记为 critical unknowns。

## Pitfalls

- 不要把模糊 idea 改写成看似成熟的研究问题。
- 不要补造数据来源、endpoint、sample size 或方法细节。
- 不要进行 readiness 判定。
- 不要评价 novelty、impact 或 feasibility。
- 不要生成 proposal 正文。
- 不要默认用户需要 SAP。
- 不要删除用户给出的限制条件。
- 不要把假设写成 confirmed facts。
- 不要输出过长背景综述。

## Verification

完成前检查：

- 是否明确 input type；
- 是否提取了 research question 或 objective，若缺失则标记 unknown；
- 是否记录 target population、system、dataset 或 study object；
- 是否记录 available data 和 data gaps；
- 是否记录 intended output 和 user goal；
- 是否区分 facts、assumptions 和 unknowns；
- 是否标明 critical unknowns；
- 是否记录 SAP requested status；
- 是否避免了 readiness 判断和 proposal drafting。

## References

- `references/fields-context-brief.md`：定义 context brief 应包含的字段和字段解释。
- `references/accepted-input-types.md`：定义本 skill 可接受的输入类型及其处理方式。
- `references/schema-proposal-context-brief.md`：定义 proposal context brief 的结构要求，仅供输出校验使用。
- `templates/template-proposal-context-brief.md`：定义 proposal context brief 的输出格式。
