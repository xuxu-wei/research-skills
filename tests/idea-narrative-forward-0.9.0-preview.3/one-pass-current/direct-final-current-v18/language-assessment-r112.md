---
review_id: language-assessment-I01-001-r112
reviewer_skill: academic-language-assessor
reviewer_instance_id: fresh-academic-language-assessor-r112
workflow_id: RID-SEPSIS-CSM-20260717-001
round_id: r112
input_artifact_ids:
  - idea-dossier-I01-001-v052
input_versions:
  - v052
scope: complete_idea_dossier
dossier_ref:
  artifact_id: idea-dossier-I01-001-v052
  version: v052
  path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v18/idea-dossier-v052.md
reader_handoff:
  artifact_id: embedded-reader-handoff
  version: embedded
  path: null
files_read:
  - AGENTS.md
  - research-skills-openai/skills/academic-language-assessor/SKILL.md
  - research-skills-openai/skills/academic-language-assessor/references/language-assessment-rubric.md
  - research-skills-openai/skills/academic-language-assessor/references/language-hard-gates.md
  - research-skills-openai/skills/academic-language-assessor/references/terminology-review.md
  - research-skills-openai/skills/academic-language-assessor/references/chinese-academic-language-conventions.md
  - research-skills-openai/skills/academic-language-assessor/references/discipline-language-conventions.md
  - research-skills-openai/skills/academic-language-assessor/references/common-l1-interference-patterns.md
  - research-skills-openai/skills/academic-language-assessor/templates/language-assessment-report.md
  - research-skills-openai/skills/academic-language-assessor/scripts/scan_idea_language_candidates.py
  - research-skills-openai/skills/academic-language-assessor/scripts/validate_language_assessment.py
  - tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v18/idea-dossier-v052.md
isolation_mode: fresh_subagent
prior_scores_visible: false
source_edits_performed: false
decision: major_language_revision
coverage_receipt:
  reader_entry:
    status: completed
    reviewed_count: 12
    basis: 已逐一检查标题、完整研究构想摘要、受众与定位、结构式摘要、主要研究问题及核心假设的全部扫描入口，未在发现首个问题后停止。
  core_scientific_role:
    status: completed
    reviewed_count: 10
    basis: 已按跨学科课题负责人视角核查研究对象、主要任务与结局、动态表征、测量、验证、条件性试验延伸、负向结果及解释边界等实际出现的核心科学角色。
  terminology_concordance:
    status: completed
    reviewed_count: 5
    basis: 已对由读者入口或全篇用法触发的五个概念簇完成首用、复合修饰关系及全文一致性核查；仅保留下列经语义确认的问题。
  local_language:
    status: completed
    reviewed_count: 15
    basis: 已覆盖全部 15 个二级章节及其中的正文、表格、列表和参考文献，检查语法、语域、时态、局部清晰度和重复表达。
findings:
  - finding_id: LANG-R112-001
    severity: major
    finding_kind: terminology
    finding_level: meso
    finding_scope: concept_cluster
    scientific_role: state-system
    normalized_locator: abstract-hypothesis-and-state-definitions
    failure_mode: scientific-role-conflation
    fingerprint: meso|state-system|abstract-hypothesis-and-state-definitions|scientific-role-conflation
    category: 术语一致性与科学对象辨识
    dossier_locator:
      - 第 45 行，Structured abstract—Objective and hypothesis
      - 第 76 行，Primary research question
      - 第 89 行，Core hypothesis and evidence boundary
      - 第 203 行，Protocol locks 表“同一时间窗内顺序”
      - 第 213–228 行，Mutually exclusive post-onset state and event system 与 Observational target
      - 第 238–246 行，Absolute simulation and semi-synthetic recovery criteria
    current_problem: >-
      “状态”及其派生表达同时指发病后互斥临床状态、动态系统中的潜在生理状态 X(t)，并在第 203 行把“下一边界实测生理值”称为“后继状态”；摘要和核心假设中的“状态占用率、转移概率”又没有说明属于哪一类状态。跨学科读者因此可能把第 7 日主要临床结局、潜在状态恢复指标和观测生理值理解为同一对象，从而对主要结局、动态表征及结构稳定性主张形成实质性错误理解。
    target_state: >-
      全篇分别使用“发病后互斥临床状态”“潜在生理状态 X(t)”和“观测生理值 Y(t)”；每个“状态占用率”“转移概率”“状态恢复”或“状态对齐”都明确限定其对象，不能依赖远距离上下文猜测。
    required_change_or_replacement: >-
      在结构式摘要首次并列这些角色时直接说明三者的区别；把第 203 行“下一边界实测生理值为后继状态”改为“下一时间边界的实测生理值作为后继观测 Y(t+1)”或与实际模型一致的同等直接表述；随后将未加限定的“状态占用率、转移概率、状态恢复、状态对齐”分别改为“互斥临床状态占用概率/临床状态转移概率”或“潜在生理状态占用概率/潜在状态转移、恢复或对齐”，以实际所指角色为准。
    content_to_preserve: >-
      保留患者—时间状态与状态转移作为推断单位、发病后互斥临床状态作为主要任务对象、X(t) 与 Y(t) 的模型角色分离、允许的重参数化以及非因果解释边界。
    acceptance_test: >-
      从标题后的首个读者入口到解释矩阵逐项检索“状态”“占用”“转移”“恢复”“对齐”和“后继状态”；每一处均能在本句或紧邻定义中唯一识别为互斥临床状态、潜在生理状态或观测生理值，且第 7 日主要结局与潜在状态结构指标不再共用无修饰的“状态占用率”或“转移概率”。
    term_or_phrase: 状态、状态占用率、转移概率、后继状态
    recommended_form_or_plain_description: 发病后互斥临床状态；潜在生理状态 X(t)；观测生理值 Y(t)；并按对象限定相应占用、转移、恢复与对齐指标
    evidence_basis: >-
      dossier 内部的变量角色表、互斥临床状态定义和 X(t)/Y(t) 定义已明确展示三个不同科学角色，无须另造术语；问题来自同一词头跨角色复用及核心入口缺少限定。直接描述各对象比另设缩写或项目标签更适合重症医学、流行病学、统计、系统辨识和医学人工智能共同读者。
    first_use_definition: >-
      建议在结构式摘要首次出现相关指标时写明：“发病后互斥临床状态用于第 7 日临床任务；潜在生理状态 X(t) 是动态表征中的未观测状态；实测生理值记为 Y(t)，用于观测和锚定。”随后只使用带对象限定的指标名称。
    competing_forms_and_locators:
      - “状态占用率、转移概率”——第 45、89、228 行，未限定临床状态或潜在状态
      - “患者状态”——第 76 行，可同时指临床状态与潜在状态
      - “后继状态”——第 203 行，语法上实际承接“实测生理值”
      - “发病后状态/互斥状态”——第 62、80、112、211–222 行，指临床事件定义
      - “潜在患者状态 X(t)”——第 226 行，指动态系统中的未观测状态
  - finding_id: LANG-R112-002
    severity: major
    finding_kind: terminology
    finding_level: micro
    finding_scope: occurrence
    scientific_role: simulation-recovery-metric
    normalized_locator: absolute-recovery-table
    failure_mode: undefined-summary-statistic
    fingerprint: micro|simulation-recovery-metric|absolute-recovery-table|undefined-summary-statistic
    category: 主要测量名称
    dossier_locator: 第 238 行，Absolute simulation and semi-synthetic recovery criteria 表“状态恢复”
    current_problem: >-
      “连续主要典型相关至少 0.80”不是可唯一计算的标准统计量名称：“主要”没有说明取第一典型相关系数、若干系数的汇总量，还是预先指定维度的相关。该阈值承担复杂候选状态恢复的准入判定，现有表述会让读者对主要恢复测量及其通过条件形成不同且实质性的理解；邻近文本不能消除这一歧义。
    target_state: >-
      明确连续潜在状态恢复所采用的唯一统计量、比较对象和多维汇总规则，使 0.80 阈值对应一个可重复计算的量。
    required_change_or_replacement: >-
      由方法负责人确认预先指定的统计量后写出全称和计算对象；例如，若实际规则是第一典型相关系数，应写为“对齐后的真实连续潜在状态与估计连续潜在状态之间的第一典型相关系数至少为 0.80”。若采用平均值、最小值或逐维条件，则须直接写出该汇总方式，不能保留“连续主要典型相关”。
    content_to_preserve: >-
      保留离散状态使用调整兰德指数、连续状态使用典型相关类指标、阈值 0.80，以及未达到标准时合并或删除状态或改用简单表征的后果。
    acceptance_test: >-
      第 238 行给出一个无须读者猜测即可计算的连续状态恢复统计量；统计量名称、比较对象、维度处理和 0.80 阈值在方法、合取标准及后续解释中一致。
    term_or_phrase: 连续主要典型相关
    recommended_form_or_plain_description: 明确写出连续潜在状态之间所采用的预先指定典型相关系数及多维汇总规则
    evidence_basis: >-
      “典型相关系数”是可识别的统计术语，但“连续主要典型相关”没有形成唯一统计定义；dossier 也未在其他位置说明“主要”的计算含义。此处需要直接命名既定统计量，而不是另造简写。
    first_use_definition: >-
      在第 238 行首次给出该恢复标准时，用一句话注明比较的真实与估计状态、采用第几个或何种汇总的典型相关系数，以及阈值应用方式。
    competing_forms_and_locators: []
  - finding_id: LANG-R112-003
    severity: minor
    finding_kind: language
    finding_level: micro
    finding_scope: occurrence
    scientific_role: reader-entry-summary
    normalized_locator: complete-idea-summary
    failure_mode: overloaded-coordination
    fingerprint: micro|reader-entry-summary|complete-idea-summary|overloaded-coordination
    category: 中文学术清晰度
    dossier_locator: 第 38 行，One-sentence complete-Idea summary
    current_problem: >-
      “以文献和专家先验及两个……数据库”把知识来源与数据来源并入同一“以”字结构，后续又连续串联主体构建、证据形成、条件性试验分析和非因果边界。科学角色可从本句恢复，但首读需要回看各成分的支配关系。
    target_state: >-
      在保持单句格式的前提下，清楚区分先验来源、数据来源、主体研究动作、条件性延伸和解释边界。
    required_change_or_replacement: >-
      将开头改为“本研究计划在 24 个月内，基于文献与专家先验，并使用两个须经访问和可观测性审计的公共重症监护数据库，构建……，再通过预设模拟重建和跨数据库检验形成可审计证据”；分号后改用“仅在主体研究达到标准后，才……”引出试验延伸，并以“所有预测和观察性表征均作非因果解释”收束。修改时同步采用 LANG-R112-001 中区分后的状态名称。
    content_to_preserve: >-
      保留 24 个月、文献与专家先验、两个待审计公共数据库、全病程覆盖、模拟与跨数据库证据、试验延伸的条件性以及非因果解释边界；仍须是一句话。
    acceptance_test: >-
      修改后仍为一个完整句子；跨学科读者可在一次阅读中分别指出先验、数据、主体动作、条件性动作和解释限制，且没有删除任何现有条件。
  - finding_id: LANG-R112-004
    severity: minor
    finding_kind: language
    finding_level: meso
    finding_scope: concept_cluster
    scientific_role: misspecification-diagnostic
    normalized_locator: repeated-diagnostic-label
    failure_mode: nominalization-stack
    fingerprint: meso|misspecification-diagnostic|repeated-diagnostic-label|nominalization-stack
    category: 简洁性与术语表达
    dossier_locator:
      - 第 82、103 行，Objectives 与时间节点表
      - 第 243 行，恢复标准表
      - 第 306、325、357、381 行，实施表、证据链、必需分析与停止标准
    current_problem: >-
      “模型错设下错误高置信结构结论的检查”以连续名词堆叠表达一个本可直接陈述的诊断动作，并在多个章节近乎逐字重复。它是支持性诊断而非中央对象，含义可恢复，但反复解码增加阅读负担。
    target_state: >-
      用一致、直接的主谓表达说明：模型错设时，检查方法是否仍错误地产生高置信度结构结论。
    required_change_or_replacement: >-
      首次完整写为“检查模型错设时是否仍错误地给出高置信度的结构结论”；表格短标签可统一为“模型错设时的高置信度结构误判”，后续不得在同一语义下交替使用现有名词串和新标签。
    content_to_preserve: >-
      保留模型错设情景、错误结构结论、高置信度、识别失配、停止解释及淘汰复杂候选等全部判定内容和阈值。
    acceptance_test: >-
      全文检索现有名词串不再出现；首次出现处给出直接动作描述，表格短标签与该描述唯一对应，所有阈值和失败后果保持不变。
  - finding_id: LANG-R112-005
    severity: minor
    finding_kind: language
    finding_level: meso
    finding_scope: concept_cluster
    scientific_role: conditional-trial-methods
    normalized_locator: mapping-and-analysis-criteria
    failure_mode: stacked-criteria-sentences
    fingerprint: meso|conditional-trial-methods|mapping-and-analysis-criteria|stacked-criteria-sentences
    category: 可读性与局部行文
    dossier_locator:
      - 第 279 行，观测映射外部忠实度与试验覆盖标准
      - 第 289–290 行，两项试验的缺失、死亡与分析表格单元格
      - 第 363 行，试验次要分析启动条件
    current_problem: >-
      三处把资格、计算、多个阈值、缺失处理、敏感性分析和停止后果压入单个长句或单个超长表格句群。均属于条件性次要分析，技术含义可从邻近文本恢复，但跨学科读者难以一次辨认“先检查什么、满足什么、失败后做什么”。
    target_state: >-
      保持原有表格结构和全部条件，将资格、计算、判定与失败后果按执行顺序分成短句或编号分句。
    required_change_or_replacement: >-
      第 279 行至少分为“外部忠实度指标”“试验资料覆盖指标”“映射失败条件”三句；第 289–290 行在各原表格单元格内用编号或分号依次列出死亡/出院处理、缺失插补、偏移与临界点分析、转院或未知状态处理；第 363 行先写授权与原始语义核验，再另句列出分析前需固定的参数。不得改变表格行列、数值阈值或条件顺序。
    content_to_preserve: >-
      保留所有样本集、访视日、共同生理锚点变量要求、忠实度与覆盖阈值、死亡和出院排序、多重插补、偏移与临界点分析、中心处理、多重性和停止规则。
    acceptance_test: >-
      三处均可按“资格—计算—判定—后果”的顺序逐项标注；没有任何阈值、例外、样本集或停止条件丢失，表格行列与原合同格式保持不变。
unresolved_issues:
  - LANG-R112-001
  - LANG-R112-002
  - LANG-R112-003
  - LANG-R112-004
  - LANG-R112-005
---

# Language Assessment Report

**Assessment ID**: language-assessment-I01-001-r112  
**Target Language**: Chinese  
**Discipline**: 重症医学与临床流行病学，交叉纵向统计、系统辨识和医学人工智能  
**Target Journal**: 未指定  
**Scope**: 完整研究构想 dossier  
**Date**: 2026-07-20

---

## Overall Language Readiness

**Level**: major_language_revision

**Recommendation**: revise_language

---

## Dimension Scores

| Dimension | Score (1–10) | Severity |
|-----------|-------------|----------|
| Grammar & Syntax | 9 | pass |
| Academic Register & Tone | 9 | pass |
| Terminology Consistency | 5 | borderline |
| Tense & Voice Conventions | 9 | pass |
| Conciseness & Redundancy | 6 | borderline |
| Readability & Flow | 6 | borderline |

---

## Hard Gate Status

**Overall**: fail

| Gate | Status | Detail |
|------|--------|--------|
| Grammar error density | pass | 未见明确且无争议的语法错误超过每 500 个中文词语当量 3 个；第 38 行列为清晰度问题，不计作明确语法错误 |
| Academic register | pass | 未见两个及以上章节系统使用口语或宣传性语域 |
| Terminology coherence | fail | 不是由三个不相关的小问题拼接；一个中央“状态”概念簇在摘要、核心假设和方法中跨临床状态、潜在状态与观测值混用，足以使主要结局与主要方法产生实质性误读 |
| Tense systematic violation | pass | 全文为前瞻性研究计划，计划时态和条件式表达与研究阶段一致 |

---

## Strengths

1. 全文持续使用计划性和条件性表述，并明确区分尚未生成的结果、待审计资源与已有证据，研究状态表达稳定。
2. 预测、观察性表征、随机试验次要分析和因果解释之间的边界在摘要、方法、解释矩阵和局限性中均有清楚限制。
3. 缩写、数据库名称、变量符号、时间单位和数值阈值总体一致；“共同生理锚点变量”“锚点观测值”“锚点预测值”均有可定位定义。
4. 大多数表格采用“输入—方法—输出—后果”的直接表达，便于跨学科课题负责人核对计划依赖关系。

---

## Specific Issues

### Chinese Academic Clarity (if applicable)

- **LANG-R112-003（minor）**：第 38 行的知识来源、数据来源和三类研究动作采用叠加协调结构；问题局限于读者入口句，可在保持单句合同的前提下重排。
- **LANG-R112-005（minor）**：第 279、289–290、363 行的条件性试验方法句承载过多资格、阈值和后果；应在原有表格与内容边界内按执行顺序拆分。

### Grammar & Syntax

未发现达到独立语法 finding 阈值的系统性错误。第 38 行的问题属于成分支配关系不够直接，已列入 LANG-R112-003。

### Academic Register & Tone

未发现需单列的语域问题。计划性成果与贡献均使用条件限制，没有把目标写成已经取得的结果。

### Terminology Consistency

| id | term_or_phrase | locator | reader_effect | action_in_frontmatter |
|---|---|---|---|---|
| LANG-R112-001 | 状态、状态占用率、转移概率、后继状态 | 第 45、76、89、203、213–228、238–246 行 | 可能把主要临床结局、潜在动态状态和观测生理值误认为同一科学对象 | yes |
| LANG-R112-002 | 连续主要典型相关 | 第 238 行 | 无法确定 0.80 阈值对应的具体统计量和汇总规则 | yes |

### Tense & Voice Conventions

未发现问题。作为研究计划，全文使用“计划”“须”“若……则……”和将来执行语气恰当；没有把拟开展方法系统写成已完成研究。

### Conciseness & Redundancy

- **LANG-R112-004（minor）**：支持性错设诊断被写成重复的名词串；改为一次完整动作说明和一个一致短标签即可。

### Readability & Flow

- **LANG-R112-003（minor）**影响完整研究构想摘要的首次阅读，但各科学角色仍可从本句恢复。
- **LANG-R112-005（minor）**影响条件性次要分析的局部执行顺序识别，不影响主体阶段 I–II 的中央研究对象。

---

## Language Revision Priorities

1. **术语一致性**：2 项——先区分临床状态、潜在状态与观测值，再明确连续状态恢复统计量；完成后做全篇一致性核查。
2. **中文学术清晰度与可读性**：2 项——重排完整研究构想摘要的并列关系，并按执行顺序拆分条件性试验方法中的长句。
3. **简洁性**：1 项——把重复的错设诊断名词串统一改为直接动作表述。

---

## Re-Assessment Status (if applicable)

不适用。本次为隔离的全新完整 dossier 评估，未读取或比较任何旧版本、修订说明或既往评估。

---

## Assessment Notes

本评估以跨学科课题负责人为目标读者，假定其熟悉重症医学研究、临床流行病学和常见统计评价，但不要求其从系统辨识专门语境自行推断未限定的“状态”类别。未指定目标期刊，因此采用中文综合科学写作与生物医学、统计和工程交叉研究的一般惯例。评估仅涉及语言可理解性、术语、语域、时态、简洁性和局部行文；没有判断方法是否科学有效、研究是否新颖或项目是否可行。
