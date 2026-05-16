---
name: sap-writer
description: Draft and maintain a Statistical Analysis Plan file after methodology/statistics
  preflight has passed. Produces SAP content aligned with the proposal, endpoint or
  metric definitions, data structure, analysis population, primary analysis, missing
  data plan, sensitivity analyses, clinical data constraints, prespecified hypothesis
  tests, exploratory/post hoc analysis boundaries, and reproducibility requirements.
  Does not evaluate its own SAP.
version: 1.0.0
author: Xuxu Wei
license: MIT
metadata:
  hermes:
    tags:
    - research-proposal
    - SAP
    - statistical-analysis-plan
    - statistics
    - methodology
    - endpoint
    - analysis-plan
    related_skills:
    - proposal-orchestrator
    - proposal-drafter
    - methodology-statistics-preflight
    - sap-evaluator
    - sap-refinement-controller
    - proposal-package-assembler
---

# sap-writer

## When to Use

当用户明确要求生成 SAP、统计分析计划、protocol 中的统计分析部分，或 proposal 需要附带 SAP 文件时，使用本 skill。

本 skill 必须在 `research/methodology-statistics-preflight` 通过后运行。若 preflight 未通过，不得强行撰写完整 SAP。

本 skill 只负责编写和维护 SAP 文件，不评价 SAP 质量，不替代 `sap-evaluator`。

## Core Principles

- SAP 是可选分支，不是 proposal 主流程的默认组成部分。
- 只有用户明确要求 SAP 或 SAP review 时才运行。
- 必须以 `sap_file_path` 为中心创建或维护 SAP 文件。
- SAP 必须与 proposal、context brief、endpoint、数据结构和 preflight report 对齐。
- 不补造 endpoint、sample size、analysis population、数据结构或统计模型。
- 临床医学 SAP 必须区分 prespecified confirmatory analyses、secondary supportive analyses、post hoc analyses 和 exploratory analyses。
- 基于数据发现形成的分析不得伪装成预设假设；必须标注触发来源、解释限制和验证需求。
- 临床数据 SAP 必须说明数据来源、观察窗口、索引日期/基线、随访、结局确认、编码/测量规则和关键偏倚风险。
- 调用 SAP 撰写时，必须根据研究问题主动识别可能重要的临床特征，并制定描述性统计计划来描绘研究人群；即使这些特征不进入主要模型，也应说明其临床意义和是否仅用于描述。
- 不评价自己生成的 SAP。
- 不在本 SKILL.md 中内嵌 schema、template、reference 正文、rubric 或代码；只引用对应文件路径。

## Inputs

通常由 `proposal-orchestrator` 提供：

- user request confirming SAP is required；
- proposal context brief；
- `proposal_file_path`，如已有 proposal；
- `proposal_version`，如适用；
- methodology/statistics preflight report；
- endpoint、outcome、metric 或 analysis target；
- available data description；
- clinical data source description, coding systems, measurement windows, index date or baseline definition, follow-up structure, if applicable；
- clinically important baseline, disease, severity, treatment, comorbidity, care-context, and socioeconomic features suggested by the research question, if available；
- study population or analysis population；
- prespecified hypotheses or analysis questions, if available；
- known or planned post hoc/exploratory questions, if applicable；
- user goal and target output；
- funding call、protocol requirement 或 reporting requirement，如有；
- existing `sap_file_path`，如为修订任务；
- SAP evaluation report，如为修订任务。

若缺少 preflight report，或 preflight 未允许进入 SAP，应停止并返回 SAP-blocking issue。

## Outputs

本 skill 输出：

- new or updated `sap_file_path`；
- `sap_version`；
- SAP change summary；
- assumptions and unresolved SAP issues；
- handoff note for `sap-evaluator`。

不得输出 SAP evaluation decision。

## Procedure

### 1. Confirm SAP Authorization

先确认用户是否明确要求 SAP、SAP review、protocol 统计部分或完整统计分析计划。

若用户未明确要求 SAP，应返回 scope mismatch，并交回 orchestrator。

### 2. Confirm Preflight Status

检查是否已有 `research/methodology-statistics-preflight` 输出。

只有 preflight 结论允许继续时，才能撰写完整 SAP。

若存在以下情况，应停止并报告 SAP-blocking issues：

- endpoint、outcome 或 metric 未定义；
- analysis population 不清；
- 数据结构不足以支持主要分析；
- primary analysis route 不明确；
- 关键 confounding、missingness 或 measurement 问题未处理；
- preflight 明确返回 blocked 或 needs_clarification。

### 3. Establish SAP File State

初稿任务必须创建并返回 `sap_file_path`。

修订任务必须读取并维护现有 `sap_file_path`，或生成明确版本化的新 SAP 文件路径。

必须记录：`sap_file_path`、`sap_version`、source proposal or context、preflight report reference、change summary、unresolved SAP issues。

### 4. Draft SAP

SAP 初稿应覆盖以下核心内容：

- study objective and analysis objective；
- estimand or analysis target, including population, endpoint, exposure/comparator, time window, intercurrent event handling, and summary measure when applicable；
- prespecified hypotheses and decision rules；
- endpoint、outcome、metric definitions；
- clinical data source, data provenance, measurement windows, and variable derivation rules；
- clinically important feature inventory and descriptive statistics plan；
- study population and analysis sets；
- exposure、intervention、predictor、comparator or grouping variables；
- covariates and adjustment strategy；
- primary analysis；
- secondary prespecified analyses, if applicable；
- post hoc and exploratory analyses, if applicable, clearly separated from prespecified analyses；
- missing data plan；
- sensitivity analyses；
- subgroup analyses，如适用；
- multiplicity control，如适用；
- sample size or power considerations，如适用且信息充分；
- software and reproducibility notes；
- assumptions, limitations, and unresolved issues。

对于临床医学数据分析，还必须覆盖：

- study design context: trial, observational cohort, case-control, cross-sectional, diagnostic, prediction, registry/EHR, claims, or mixed source；
- index date, baseline window, exposure assessment window, outcome assessment window, and follow-up/censoring rules；
- clinical endpoint ascertainment, coding systems, adjudication or proxy definitions, and validation status；
- confounding, selection bias, immortal time, informative censoring, competing risk, clustering/repeated measures, and site/provider effects when relevant；
- clinically meaningful effect size or interpretation threshold when available；
- patient-level privacy, reproducibility, and data access constraints if they affect execution。

临床特征描述性统计计划必须覆盖：

- demographics: age, sex/gender, race/ethnicity or region when relevant and appropriate；
- disease context: diagnosis, disease duration, severity/stage, baseline risk, prior events, baseline symptoms/function, biomarkers or laboratory values；
- treatment/care context: prior treatment, concomitant therapy, care setting, site/provider, calendar period, protocol deviations or treatment era；
- comorbidities and competing risks likely to affect prognosis, treatment selection, follow-up, or outcome ascertainment；
- data availability and missingness for key clinical features；
- descriptive summary format by total cohort and clinically meaningful groups when useful。

这些临床特征不应自动纳入调整模型；SAP 必须区分 `descriptive only`、`candidate covariate/confounder`、`effect modifier/subgroup`、`stratification factor` 和 `not available/unresolved`。

若信息不足，应标记为 unresolved issue，不得自行补造。

### 5. Maintain Alignment

SAP 必须与 proposal research question、aims/objectives、endpoint/metric、data availability、preflight report、用户约束和目标产出一致。

如 SAP 与 proposal 不一致，应标记 alignment issue，而不是隐式修改研究问题。

### 6. Revise SAP

当收到 `sap-evaluator` 或 orchestrator 提供的 revision request 时，只针对明确问题修订。

常见修订目标包括 endpoint definition、primary analysis、analysis population、missing data plan、sensitivity analysis、confounding control、reproducibility 或与 proposal 文件不一致。

每轮修订必须输出 change summary 和 unresolved SAP issues。

### 7. Handoff

完成后，将 SAP 文件交回 `proposal-orchestrator` 或 `sap-evaluator`。

handoff 至少包括：

- `sap_file_path`
- `sap_version`
- linked `proposal_file_path`，如有
- preflight report reference
- change summary
- unresolved SAP issues
- recommended next step: SAP evaluation or re-evaluation

不得自行宣布 SAP accept、reject 或 ready for submission。

## Delegation Rules

本 skill 通常不直接派发子 agent。

若发现需要方法学预检、SAP 评价或统计学审查，应交回 `proposal-orchestrator` 调度相应独立子 agent。

不得自行调用或模拟 methodology/statistics preflight、SAP evaluation、proposal evaluation、proposal review panel 或 skeptical review。

## Stop Conditions

以下情况应停止 SAP drafting 或 revision：

- 用户未明确要求 SAP；
- 缺少 methodology/statistics preflight report；
- preflight 未通过；
- endpoint、metric 或 outcome 无法定义；
- analysis population 无法确定；
- 数据结构无法支持主要分析；
- primary analysis route 缺失；
- 修订要求与 proposal、preflight report 或数据条件冲突；
- 继续写作需要补造关键统计信息。

## Pitfalls

- 不要在用户未要求时生成 SAP。
- 不要跳过 methodology/statistics preflight。
- 不要补造 endpoint、sample size、analysis population 或统计模型。
- 不要评价自己写出的 SAP。
- 不要让 SAP 与 proposal 研究问题脱节。
- 不要把无法确定的分析细节写成确定方案。
- 不要用通用统计话术掩盖 data-method mismatch。
- 不要在 preflight blocked 时强行写完整 SAP。
- 不要把 SAP evaluation 混入 SAP writing。

## Verification

完成前检查：

- 用户是否明确要求 SAP；
- preflight 是否已完成且允许进入 SAP；
- 是否存在明确 `sap_file_path`；
- 是否记录 `sap_version`；
- 是否与 proposal 或 context brief 对齐；
- endpoint、analysis population 和 primary analysis 是否明确；
- 是否主动列出研究问题相关的临床重要特征，并为研究人群特征制定描述性统计计划；
- missing data 和 sensitivity analysis 是否处理；
- prespecified hypotheses 是否与 primary/secondary analyses 对齐；
- post hoc / exploratory analyses 是否单独标注，且未被写成 confirmatory inference；
- 临床数据来源、窗口、结局确认、混杂/偏倚控制是否明确；
- unresolved SAP issues 是否明确列出；
- 是否未输出 SAP evaluation decision；
- 是否准备好交给 `sap-evaluator`。

## References

- `references/rules-sap-writing.md`：定义 SAP 写作范围、必要组成部分和不得补造的信息类型。
- `references/rules-endpoint-analysis-alignment.md`：定义 endpoint、analysis target、primary analysis 与研究问题之间的一致性要求。
- `references/rules-missing-data-sensitivity.md`：定义 missing data、sensitivity analysis 和 robustness check 的写作规则。
- `references/rules-clinical-data-analysis.md`：定义临床医学数据分析 SAP 的数据来源、时间窗口、结局确认、偏倚控制和解释边界。
- `references/rules-clinical-feature-descriptives.md`：定义临床重要特征识别和描述性统计计划，避免把描述性特征自动误用为调整变量。
- `references/rules-prespecified-vs-exploratory.md`：定义预设假设分析、secondary/supportive、post hoc 和 exploratory 分析的分隔规则。
- `references/policy-sap-file-maintenance.md`：定义 `sap_file_path`、版本 lineage、change summary 和 unresolved SAP issues 的维护规则。
- `references/schema-sap.md`：定义 SAP 文件结构要求，仅供输出校验使用。
- `templates/template-sap.md`：定义 SAP 文件的推荐输出结构。
