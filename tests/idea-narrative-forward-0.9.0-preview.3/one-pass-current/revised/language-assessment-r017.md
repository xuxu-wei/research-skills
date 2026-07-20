---
review_id: language-assessment-I01-001-r017
reviewer_skill: academic-language-assessor
reviewer_instance_id: fresh-onepass-language-r017
workflow_id: RID-SEPSIS-CSM-20260717-001
round_id: one-pass-editorial-readiness-r017
input_artifact_ids:
  - idea-dossier-I01-001-v006
  - reader-handoff-forward-001
input_versions:
  - v006
  - v001
files_read:
  - AGENTS.md
  - research-skills-openai/AGENTS.md
  - research-skills-openai/skills/academic-language-assessor/SKILL.md
  - research-skills-openai/skills/academic-language-assessor/references/language-assessment-rubric.md
  - research-skills-openai/skills/academic-language-assessor/references/language-hard-gates.md
  - research-skills-openai/skills/academic-language-assessor/references/chinese-academic-language-conventions.md
  - research-skills-openai/skills/academic-language-assessor/references/discipline-language-conventions.md
  - research-skills-openai/skills/academic-language-assessor/references/terminology-review.md
  - research-skills-openai/skills/academic-language-assessor/templates/language-assessment-report.md
  - research-skills-openai/skills/academic-language-assessor/scripts/validate_language_assessment.py
  - tests/idea-narrative-forward-0.9.0-preview.3/run-001/inputs/reader-handoff.yaml
  - tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/revised/idea-dossier-v006.md
isolation_mode: fresh_subagent
prior_scores_visible: false
source_edits_performed: false
decision: major_language_revision
findings:
  - id: L017-001
    severity: major
    category: terminology
    locator: "Structured abstract > Expected result；Research question；Research design and methods > 条件性试验观测桥接"
  - id: L017-002
    severity: major
    category: terminology
    locator: "Structured abstract > Expected result；Research objectives 3；Research content and work packages；模拟恢复检验"
  - id: L017-003
    severity: major
    category: academic_register_and_flow
    locator: "Title, summary, audience, and positioning；Research content and work packages；Research design and methods；Feasibility"
  - id: L017-004
    severity: minor
    category: mixed_language_terminology
    locator: "Research objectives；Data；Research design and methods；Required analyses"
  - id: L017-005
    severity: minor
    category: concision
    locator: "One-sentence complete-Idea summary；Research design and methods > 医院优先的跨数据库外部验证"
  - id: L017-006
    severity: minor
    category: terminology_and_register
    locator: "Positioning and contribution frame；Research content and work packages；Evidence chains"
unresolved_issues:
  - L017-001
  - L017-002
  - L017-003
  - L017-004
  - L017-005
  - L017-006
---

# Language Assessment Report

**Assessment ID**: language-assessment-I01-001-r017  
**Target Language**: Chinese  
**Discipline**: 重症医学、临床流行病学、纵向统计、系统辨识、系统科学、医学人工智能与转化研究  
**Target Journal**: 未指定  
**Scope**: 完整 Idea dossier（机器前置元数据仅作来源核对，不计入面向读者的语言评分）  
**Sections assessed**: 全部 15 个 H2 章节及第三节的五个 H3 子节  
**Date**: 2026-07-18

## Overall Language Readiness

**Level**: major_language_revision

**Recommendation**: revise_language

文本的中文语法总体稳定，五段背景逻辑也可连续阅读；但摘要和核心方法中仍有会改变读者理解的术语歧义，并且项目内部缩写、控制性措辞与未定义的中英混合方法词在多节重复出现。因核心设计术语在首次出现时尚不能由跨学科读者获得唯一、自然的解释，术语硬门不通过。

## Dimension Scores

| Dimension | Score (1–10) | Severity |
|---|---:|---|
| Grammar & Syntax | 9 | pass |
| Academic Register & Tone | 6 | borderline |
| Terminology Consistency | 5 | fail |
| Tense & Voice Conventions | 9 | pass |
| Conciseness & Redundancy | 5 | borderline |
| Readability & Flow | 5 | borderline |

## Hard Gate Status

**Overall**: fail

| Gate | Status | Detail |
|---|---|---|
| Grammar error density | pass | 未发现达到阈值的明确语法错误；零散问题主要属于搭配和可读性，而非语法错误 |
| Academic register | pass | 全文保持正式语体；问题是项目控制语言泄漏，而非口语化 |
| Terminology coherence | fail | 摘要层的“实际访视共同生理指标”和方法层的“错误高置信判断”不能让目标读者获得唯一指向；未定义的 `G1` 又参与主要判定 |
| Tense systematic violation | pass | 作为前瞻性研究构想，计划、条件和既有证据的时态与语气区分稳定 |

## Strengths

- Background、Current state、Gap、Significance 和 Rationale 各自使用了相应的陈述功能，段落衔接清楚。
- “计划产物”与“现有结果”在摘要、数据证据表和预期产物中有明确区分，语气强度总体一致。
- 状态、行动、测量过程和标签的符号及中文名称前后一致；公式中的 `X_t`、`Y_t`、`A_t`、`M_t` 也有就地说明。
- 条件句通常明确给出条件、动作和后果，未使用宣传性形容词或修辞性比喻。
- 标题、研究问题和主要目标均保持“脓毒症全病程候选动态系统表征”的同一研究对象。

## Specific Issues

### Chinese Academic Clarity

#### L017-001 — 核心试验输入的修饰关系有歧义（major）

- **位置**：`Structured abstract > Expected result`：“由实际访视共同生理指标和阶段 II 预定观测模型计算”；`Research question`：“实际访视中可测的共同生理指标”；`Research design and methods > 条件性试验观测桥接` 首段。
- **问题**：“共同”可被理解为“两个试验共同拥有的指标”，也可被理解为“每项试验分别与阶段 II 锚点重合的指标”。后文 `C_r` 的定义采用后一含义，但摘要和研究问题没有及时说明。该歧义直接影响读者对阶段 III 数据输入和两项试验是否合并的理解。
- **修改方向**：在摘要和研究问题首次出现处改为直接描述，例如“每项试验在目标访视实际测得、且与阶段 II 预先确定的生理锚点同义同单位的指标”；保留后文“每项试验分别确定 `C_r` 和映射”的技术定义。不要新增尚未确定的指标名称。
- **验收**：读者仅看标题、摘要和研究问题即可判断：（1）两项试验分别分析；（2）指标交集按试验分别与阶段 II 锚点确定；（3）不是要求两项试验拥有同一组指标。

#### L017-002 — “错误高置信判断”不能表明错误发生在哪一层（major）

- **位置**：`Structured abstract > Expected result`、研究目标 3、月 7–12 工作包、`基于预设绝对阈值的模拟恢复检验`、第二条 Evidence chain、`Required analyses and evidence`。
- **问题**：该短语可能表示“对错误作出高置信识别”，也可能表示“错误结构被模型高置信支持”。模拟表中的“错误结构高置信比例≤0.05”显示目标应为后者，但正文缩略语义相反，目标读者必须向后查找才能确定。
- **修改方向**：首次出现时写明“错误结构被高置信支持的误判率”，并在后文统一使用“高置信误判率”或同一完整表达；不要改变现有阈值、场景或判定方向。
- **验收**：每次出现均能明确主语是“错误结构”、事件是“被高置信支持”、评价量是“误判比例”，且与表中 `≤0.05` 的方向一致。

#### L017-003 — 项目内部控制语言系统性进入科研正文（major）

- **位置与例句**：
  - `Positioning and contribution frame`：“可证伪的分析治理”；
  - `Research content and work packages`：“达到 G1 数据与可观测性最低标准”“阶段 II 合取成功”“不开放最终外部测试”；
  - `Research design and methods > 条件性试验观测桥接`：“普通语言路线为”；
  - 多节反复使用“冻结候选”“冻结映射”“冻结分析包”“冻结医院角色”“打开测试集”等控制性搭配。
- **问题**：`G1` 未在正文定义；“合取成功”和“分析治理”属于项目内部逻辑或管理表达；“普通语言路线为”是写作过程提示，不是科研内容。“冻结”在少数预注册语境中可以精确，但当前同时指代预先规定、定稿、禁止再估计、限制数据访问和保存版本，迫使读者自行恢复不同含义。
- **修改方向**：删除 `G1` 标签，直接写“月 6 数据与可观测性最低标准”；把“合取成功”写成“全部必要条件均满足”；删除“普通语言路线为”并直接陈述步骤；把“分析治理”写成“预先规定的分析与失败判定方案”。逐处按实际动作将“冻结”改为“预先确定”“在查看测试结果前定稿”“不再重新估计”或“由独立保管人限制访问”，仅在确实指版本封存时保留“封存”。
- **验收**：正文不再出现未定义的 `G1`、“普通语言路线”“合取成功”或“分析治理”；每一处版本、参数、访问或预注册动作均用能说明具体动作和时间点的科研表达，不依赖项目内部状态词。

#### L017-005 — 长句和并列条件增加一次阅读负担（minor）

- **位置**：`One-sentence complete-Idea summary`；`Research design and methods > 医院优先的跨数据库外部验证` 中以“主要剔除或敏感性分析后”开头的句子；两项试验表的“缺失、死亡与分析”单元格。
- **问题**：这些句子在同一语法层级中同时承载研究对象、数据条件、验证方式、时间边界、失败分支和解释边界。信息均有必要，但主干动词被连续条件和并列项推迟。
- **修改方向**：保持合同要求的一句话摘要，但先陈述“构建并外部验证什么”，再用一个清楚的条件分句说明试验分析；正文长句拆成“判定条件—处理动作—不能推出什么”的短句。表格单元格可用分号分开死亡、缺失和界限分析。
- **验收**：摘要只需一次阅读即可分别识别主要目标、24 个月边界和条件性阶段 III；正文每句最多承担一个判定或一个处理动作，不删除任何科学条件。

### Grammar & Syntax

未发现构成独立语法错误模式的问题。个别名词串和修饰范围问题归入术语、简洁性与可读性，而非语法错误。

### Academic Register & Tone

除 L017-003 外，整体语体正式、克制。没有宣传性形容词、口语化表达或修辞性提问。需要修订的是内部项目管理措辞，而不是降低科学边界的谨慎程度。

### Terminology Consistency

| id | term_or_phrase | locator | reader_baseline | problem | recommended_replacement | first_use_definition | basis | acceptance_test |
|---|---|---|---|---|---|---|---|---|
| T017-01 | 实际访视共同生理指标 | Structured abstract > Expected result；Research question | 可假定熟悉临床试验和纵向数据，但不可假定熟悉项目内桥接定义 | “共同”的比较集合不明确 | 每项试验在目标访视实际测得、且与阶段 II 预先确定锚点同义同单位的生理指标 | 同一句说明“每项试验分别确定” | dossier 后文 `C_r` 的既有定义；不需要增加科学选择 | 摘要即可排除“两个试验必须共享同一指标集”的读法 |
| T017-02 | 错误高置信判断 | 摘要、目标 3、模拟恢复、证据链 | 可假定熟悉模拟验证，不可假定熟悉项目缩写 | 既可读为正确识别错误，也可读为错误结构获高置信支持 | 错误结构被高置信支持的误判率 | 在首次出现处说明事件和比例方向 | dossier 模拟表已有 `≤0.05` 的操作含义 | 所有表述均与阈值方向一致，且无需向后查表 |
| T017-03 | G1 | 月 4–6 工作包；Feasibility 的工作假设表 | 不可假定熟悉项目内部标签 | 未定义内部标签参与关键判定 | 月 6 数据与可观测性最低标准 | 不另设缩写 | reader handoff 明确排除项目内部词汇 | 删除 `G1` 后仍能唯一定位判定时点和内容 |
| T017-04 | landmark / stay / proper score | 研究目标、数据审计、主要任务和证据链 | 跨学科读者不一定熟悉全部英文方法简称 | 首次出现无中文指向，且中英文形态未统一 | 地标时点评估（landmark analysis）；ICU 住院记录（stay）；适当评分规则（proper scoring rule，如 Brier 分数） | 各自在首次面向读者出现处定义一次，后文固定使用中文简称 | 采用直接、可解释的中英文对应；本次隔离评估未检索外部来源 | 首次出现可理解，后文不再无规则切换英文词形 |
| T017-05 | pattern-mixture delta / selection tipping-point / sepsis-like | 观察性目标；试验表；XBJ-SCAP 证据描述 | 临床与系统读者可能不熟悉统计英语，统计读者也不能据英文碎片判断具体操作 | 英文短语未定义，`delta`、`tipping-point` 又在后文缩写；`sepsis-like` 与中文操作人群混用 | 模式混合模型的 δ 偏移分析；选择模型的临界点分析；符合预设操作性脓毒症判定的人群 | 首次出现给中英文或符号对应，随后统一一种中文形式 | 直接描述 dossier 已规定的分析，不选择新的统计方案 | 后文每个简称均可追溯到首次定义，且不改变 δ 网格或人群定义 |

#### L017-004 — 中英混合方法词缺少首次定义（minor）

除表中 T017-04 和 T017-05 外，`bootstrap` 也应在首次出现时写作“自助法（bootstrap）”，此后统一用“自助法”。数学符号、数据库名、试验名、CRF、SAP、SOFA、WBC、CRP、ICU 等可保持原形式；它们不构成本次问题。

### Tense & Voice Conventions

none。文本是前瞻性研究构想，不应机械套用已完成研究 Methods 的过去时要求；当前以“计划、须、若……则……”表达未来动作，以现在时陈述定义与既有事实，使用合理。

### Conciseness & Redundancy

L017-005 是主要问题。限制和失败条件集中在最后一个权威章节，其他技术段落中出现的条件大多直接推进局部判定；本评估不决定这些条件是否可以删除或移动。

### Readability & Flow

#### L017-006 — 省略中心名词的技术名词串降低自然度（minor）

- **位置与例句**：“至多一个受限复杂候选”“复杂候选”“失败图”“阶段 I–II 的最低交付期”“任务表现”。
- **问题**：这些表达依赖项目上下文补全“模型”“未达标结果”“必须完成的研究阶段”或“预测与校准表现”，跨学科读者可能获得不同指向。
- **修改方向**：按上下文补全中心词，例如“至多一个复杂度受限的候选模型”“显示未达预设标准项目的结果图”“24 个月内必须完成阶段 I–II”“主要临床任务的预测与校准表现”。若“失败图”已有特定图形定义，则需在首次出现处给出该定义，而不是另造短标签。
- **验收**：这些短语在脱离前一句时仍能指出对象和评价内容；同一对象后文使用同一中心名词。

## Language Revision Priorities

1. **核心术语**：先消除“共同生理指标”和“错误高置信判断”的两类歧义，使摘要、研究问题和模拟判定无需向后查找定义。
2. **科研语体**：移除 `G1`、“合取成功”“普通语言路线”和“分析治理”，并按具体科学动作改写多义的“冻结”。
3. **中英术语**：为 `landmark`、`stay`、`proper score`、模式混合与临界点分析提供一次中英文对应，后文统一中文形式。
4. **句法负担**：在不删除条件和边界的前提下，缩短摘要以外的多条件长句，并补全“复杂候选”“失败图”等省略中心词的名词串。

## Re-Assessment Status

不适用。本次为对 v006 的全新独立评估，未读取匿名既往问题清单、旧稿、修订差异或任何既往评估结果。

## Assessment Notes

- 本评估只判断中文学术语言、术语可理解性与阅读负担，不判断模型、阈值、数据、因果边界、新颖性、影响力或可行性是否科学正确。
- 未指定目标期刊，因此按生物医学、临床研究与技术方法交叉领域的一般规范评估。
- 按隔离要求未进行外部检索；术语建议优先采用 dossier 已明确的操作含义和直接描述性中文。需要作者作科学或统计选择的内容没有在本报告中替作者决定。
- 机器前置元数据、合同固定的英文 H2 标题和数学符号未作为面向读者的语言错误；仅当相同词汇进入正文并影响理解时才记录。
- 来源 dossier 保持只读；本评估未对其进行任何修改。
