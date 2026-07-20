---
review_id: language-assessment-I01-001-r019
reviewer_skill: academic-language-assessor
reviewer_instance_id: fresh-onepass-language-r019
workflow_id: RID-SEPSIS-CSM-20260717-001
round_id: r019
input_artifact_ids:
  - idea-dossier-I01-001-v007
  - reader-handoff-forward-001
input_versions:
  - v007
  - v001
files_read:
  - path: AGENTS.md
    role: repository instructions
  - path: research-skills-openai/AGENTS.md
    role: plugin-subtree instructions
  - path: research-skills-openai/skills/academic-language-assessor/SKILL.md
    role: assessor instructions
  - path: research-skills-openai/skills/academic-language-assessor/references/language-assessment-rubric.md
    role: scoring rubric
  - path: research-skills-openai/skills/academic-language-assessor/references/language-hard-gates.md
    role: hard-gate rules
  - path: research-skills-openai/skills/academic-language-assessor/templates/language-assessment-report.md
    role: report template
  - path: research-skills-openai/skills/academic-language-assessor/references/chinese-academic-language-conventions.md
    role: Chinese-language conventions
  - path: research-skills-openai/skills/academic-language-assessor/references/discipline-language-conventions.md
    role: biomedical and technical discipline conventions
  - path: research-skills-openai/skills/academic-language-assessor/references/terminology-review.md
    role: focused terminology review
  - path: research-skills-openai/skills/academic-language-assessor/scripts/validate_language_assessment.py
    role: report validator
  - path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/revised/idea-dossier-v007.md
    role: frozen assessed artifact
  - path: tests/idea-narrative-forward-0.9.0-preview.3/run-001/inputs/reader-handoff.yaml
    role: target-reader handoff
isolation_mode: fresh_subagent
prior_scores_visible: false
source_edits_performed: false
decision: major_language_revision
findings:
  - finding_id: L-001
    severity: major
    category: terminology
    locator: "Title, summary, audience, and positioning；Structured abstract；Research question, objectives, and core hypothesis"
  - finding_id: L-002
    severity: major
    category: readability_and_flow
    locator: "Research content and work packages；Research design and methods；Required analyses and evidence"
  - finding_id: L-003
    severity: minor
    category: terminology
    locator: "One-sentence complete-Idea summary；Approach；医院优先的跨数据库外部验证"
  - finding_id: L-004
    severity: minor
    category: grammar_and_syntax
    locator: "标题；One-sentence complete-Idea summary；Contribution, innovation, impact, application, and closest-work comparison"
  - finding_id: L-005
    severity: minor
    category: academic_register_and_tone
    locator: "Research content and work packages，阈值说明段"
  - finding_id: L-006
    severity: minor
    category: conciseness_and_redundancy
    locator: "Expected result；研究目标 3；模拟恢复检验；Evidence chains；Required analyses and evidence；计划产物"
  - finding_id: L-007
    severity: minor
    category: terminology
    locator: "Research content and work packages，24 个月后行；条件性试验观测桥接与独立替代端点；Required analyses and evidence"
unresolved_issues:
  - L-001
  - L-002
  - L-003
  - L-004
  - L-005
  - L-006
  - L-007
---

# Language Assessment Report

**Assessment ID**: language-assessment-I01-001-r019  
**Target Language**: Chinese  
**Discipline**: 重症医学、临床流行病学、纵向统计、系统辨识、系统科学、医学人工智能与转化研究  
**Target Journal**: 未指定  
**Scope**: complete dossier；评估全部读者可见正文、表格与参考文献表达。机器前置元数据和契约固定标题仅作为结构脚手架，不作为中文正文缺陷。  
**Sections assessed**: 标题与定位、结构式摘要、背景与研究缺口、研究问题与目标、工作包、数据与证据基础、研究设计与方法、关键技术、五条证据链、必需分析、预期产物与证伪标准、贡献与最接近工作、主张支持表、可行性与停止条件、参考文献。  
**Date**: 2026-07-19

---

## Overall Language Readiness

**Level**: major_language_revision

**Recommendation**: revise_language

全文语法和学术语体总体稳定，未达到需要专业编辑的程度。主要制约来自一个位于摘要和研究问题中的核心跨学科术语未在首次出现时提供可理解定义，以及多处跨段落、跨表格的长句和限定条件堆叠。前者触发 Idea dossier 的核心术语可理解性门槛；后者构成全稿层面的阅读负担。因此建议在不改变研究设计、阈值和条件分支的前提下进行一次结构化语言修订。

---

## Dimension Scores

| Dimension | Score (1–10) | Severity |
|-----------|-------------|----------|
| Grammar & Syntax | 8 | pass |
| Academic Register & Tone | 8 | pass |
| Terminology Consistency | 5 | fail |
| Tense & Voice Conventions | 9 | pass |
| Conciseness & Redundancy | 5 | borderline |
| Readability & Flow | 5 | borderline |

---

## Hard Gate Status

**Overall**: fail

| Gate | Status | Detail |
|------|--------|--------|
| Grammar error density | pass | 未发现成组的明确语法错误；孤立修饰关系问题明显低于每 500 词语单位 3 处的阈值。 |
| Academic register | pass | 正文整体保持正式、审慎的科研语体；未见两个以上章节以口语语体为主。 |
| Terminology coherence | fail | “观测桥接”是摘要、研究问题和阶段 III 设计中的核心关系，但首次出现时未说明桥接的输入、映射对象和输出；其完整解释延后至方法部分。对所给跨学科读者，这不属于及时定义。其他核心术语总体稳定，未见三个核心概念各自无理由换名。 |
| Tense systematic violation | pass | 方案性动作、既有证据、尚未生成结果和条件性未来分析的时间状态区分一致；未见方法或结果语态的系统性误用。 |

---

## Strengths

1. 全文持续区分“已核验”“尚未核验”“尚未生成”和“条件满足后开展”，计划性语气与证据状态匹配，没有把预期结果写成既成事实。
2. 因果、预测、结构恢复和随机化比较的措辞边界清楚，普遍使用“候选”“条件性”“不支持”等强度适当的表达，避免宣传性语言。
3. 数字、时间窗、阈值、缩写和数学符号的格式大体一致；中文标点与英文数据库名、方法名之间的排布基本稳定。
4. 表格标题和段落主题明确，读者可以定位人群、估计对象、停止条件、替代方案及各证据层的允许解释。
5. “候选动态系统表征”在定位段中被明确限定为统计研究对象，并说明仅解释经锚定、模拟恢复和跨数据库检验支持的部分；这一核心概念的语义边界清楚。

---

## Specific Issues

### Chinese Academic Clarity

#### L-001 — 核心术语首次出现时对跨学科读者不可直接理解

- **位置**：`Title, summary, audience, and positioning` 的 one-sentence summary；`Structured abstract` 的 Expected result；`Research question, objectives, and core hypothesis` 的主要研究问题。
- **原文**：“若试验资料语义和观测桥接均合格”；“一维可观测状态摘要”。
- **问题**：“观测桥接”承担阶段 III 是否可进入主要分支的关键作用，但摘要没有说明它连接的是阶段 II 观测模型与试验目标访视的实测生理锚点，也没有说明输出为何种摘要。完整说明直到 `条件性试验观测桥接与独立替代端点` 才出现。重症医学、系统辨识、统计与转化研究读者并不共享这一项目内缩略标签，首次阅读摘要时无法据此识别其输入、作用和输出。“一维可观测状态摘要”虽有描述性成分，但其方向和与潜在状态投影的关系同样延后。
- **修订方向**：首次出现时采用直接描述，例如先说明“观测桥接”是“检验阶段 II 观测模型能否把试验目标访视至少两个同义同单位的实测生理锚点可靠映射为预先规定的一维摘要”。同一句或紧随其后的句子说明摘要数值方向及其仅代表实际访视可观测信息。后文可使用短称，但不要把完整操作公式提前塞入摘要。
- **严重度**：major。
- **验收标准**：未参与项目的任一目标学科读者仅阅读标题、摘要和研究问题，即能说清桥接的输入、连接关系、输出和合格后的用途；无需等待方法章节，也不会把它理解为跨数据库模型迁移、潜在状态验证或因果桥接。

#### L-002 — 长句与限定条件堆叠形成跨章节阅读障碍

- **位置**：`Research content and work packages` 的“阶段 II 成功必须同时满足”段；`Research design and methods` 的非随机缺失与弃权段、观测桥接合格标准段及两项试验表；`Required analyses and evidence` 的试验启动前要求段。
- **原文示例**：“阶段 II 成功必须同时满足：（1）……（5）……”；“观测桥接须先在阶段 II 独立保留 eICU 测试集……合格须同时满足……”；“试验分析启动前还须形成：个体数据授权与原始 CRF、SAP……”
- **问题**：这些句子同时承载前置条件、多个数值阈值、例外、禁止项和失败后果，部分句子跨越一整段或一个高密度表格单元。读者需要反复回看才能区分“进入分析的条件”“统计合格标准”和“失败后的替代分支”。这是多个核心章节中的系统性模式，而非单个长句。
- **修订方向**：保留全部科学条件和数值，不判断哪些条件可删。把每一段先改成一句说明目的的主题句，再按“前置资格—合格指标—失败后果”分组；一个编号项只表达一个判定单位。表格单元中将分析集、缺失处理、敏感性分析和停止条件分成短句或子项。
- **严重度**：major。
- **验收标准**：每个条件都能独立定位到“前置资格、评价指标或失败分支”之一；同一句不再同时引入三个以上逻辑层级；所有阈值、时间点和替代分支保持不变。

### Grammar & Syntax

#### L-004 — “访视稀疏随机对照试验”的修饰关系含混

- **位置**：主标题、one-sentence summary、Gap、Contribution and impact 及贡献比较章节中的同类表达。
- **原文**：“访视稀疏随机对照试验”。
- **问题**：“访视稀疏”直接置于“随机对照试验”前，容易被读成试验本身稀疏，而实际含义是可用访视时间点或重复测量较少。该压缩表达在标题中尤其影响首次理解。
- **修订方向**：改为“访视时间点稀疏的随机对照试验”或“重复测量稀疏的随机对照试验”，并根据正文已固定的设计含义选择其中一个；全稿保持同一表述。
- **严重度**：minor。

### Academic Register & Tone

#### L-005 — 项目内部文种名称泄入中文正文

- **位置**：`Research content and work packages` 中紧随阶段 II 成功标准之后的阈值说明段。
- **原文**：“本 dossier 中的硬阈值只能收紧，不能放宽。”
- **问题**：`dossier` 是项目文种或流程标签，不是此处必需的学科术语，也不属于固定标题。它与周围中文科研语体不一致，且读者交接明确不假定项目内部词汇知识。
- **修订方向**：改为“本研究方案中的预设阈值只能收紧，不能放宽”或同等自然的中文表述。
- **严重度**：minor。

### Terminology Consistency

| id | term_or_phrase | locator | reader_baseline | problem | recommended_replacement | first_use_definition | basis | acceptance_test |
|---|---|---|---|---|---|---|---|---|
| L-001 | 观测桥接；一维可观测状态摘要 | one-sentence summary；Structured abstract；主要研究问题 | 了解验证、不确定性和观察性与干预性证据，但不熟悉新造标签，且不具备所有参与学科的细节知识 | 核心关系在摘要和研究问题中先用短称，输入、映射对象与输出到方法章节才说明 | 观测模型至试验访视实测指标的映射检验；后文可保留“观测桥接”短称 | 首次出现时用一句话说明输入为同义同单位实测生理锚点、依据为预先确定的阶段 II 观测模型、输出为一维可观测摘要，并说明其用途和方向 | 当前冻结文本的普通语言可理解性审查；未进行外部术语来源核验，因此优先建议直接描述而非另造名称 | 摘要独立阅读即可识别输入、连接关系、输出和边界 |
| L-003 | 独立保留数据库；第二数据库独立保留测试集；独立保留最终测试集 | one-sentence summary；Approach；医院优先的跨数据库外部验证 | 熟悉外部验证的一般概念 | 首处表述可能指整库均为保留数据，后文实际设计是外部数据库内再划分适配集和测试集 | 外部数据库中的独立保留测试集 | 首次出现时写明“外部数据库按医院划分为适配集与独立保留测试集” | 同一冻结文本内部的指称范围比较 | 全文每次提到主要外部验证时都明确指向测试子集，不再暗示整库保留 |
| L-007 | CRF；SAP | 24 个月后工作包；条件性试验观测桥接；试验启动前要求 | 跨重症医学、统计、系统辨识、系统科学与医学人工智能的混合读者 | 缩写首次出现时未展开；非临床试验方法读者未必熟悉 | 病例报告表（CRF）；统计分析计划（SAP） | 在首次读者可见正文中展开一次，后文使用缩写 | 读者交接要求不得假定每个参与学科的细节知识 | 首次出现后可仅凭正文准确解释两个缩写 |

#### L-003 — 外部验证对象的范围命名不完全一致

- **位置**：one-sentence summary、Structured abstract 的 Approach、`医院优先的跨数据库外部验证`。
- **原文**：“在独立保留数据库上”；“外部数据库按医院预先分为适配集和独立保留测试集”；“独立保留最终测试集”。
- **问题**：首处将整个数据库写成“独立保留数据库”，后文却明确只有其中的测试子集保持独立保留。对于外部验证设计，这是对象范围的实际差别。
- **修订方向**：首次统一写成“在外部数据库的独立保留测试集上”，并在首次方法说明中明确外部数据库包含适配集和测试集。后文统一用“独立保留测试集”。
- **严重度**：minor。

#### L-007 — 临床试验文件缩写未在首次使用时展开

- **位置**：`Research content and work packages` 的 24 个月后行；随后在条件性试验方法、启动要求和限制中重复出现。
- **原文**：“原始 CRF/SAP”。
- **问题**：该缩写对临床试验研究者较常见，但目标读者还包括系统辨识、系统科学和医学人工智能研究者，不能假定全部读者已经掌握。
- **修订方向**：首次写为“原始病例报告表（CRF）和统计分析计划（SAP）”，后文再用缩写。
- **严重度**：minor。

### Tense & Voice Conventions

未发现需要单列的时态或语态问题。中文方案文本一致使用“计划”“须”“将”“尚未”等标记区分未来动作、必要条件与当前证据；文献事实和项目待办也保持分离。建议修订时继续保留这种证据状态标记。

### Conciseness & Redundancy

#### L-006 — “错误结构被高置信支持的误判率”反复使用且句法压缩过度

- **位置**：Structured abstract 的 Expected result；研究目标 3；模拟恢复检验；第二条 Evidence chain；Required analyses and evidence；计划产物。
- **原文**：“错误结构被高置信支持的误判率”。
- **问题**：连续的“被—支持—误判率”名词化结构使修饰范围不清，读者可能短暂误解为“错误结构本身具有高置信支持”，而不是“错误结构被误判为受到高置信支持”。该长语块多次重复，放大了阅读负担。
- **修订方向**：首次完整写为“错误结构被误判为具有高置信支持的比例”，如确需短称，可在首次定义后统一使用“错误结构高置信误判率”。不要改变现有阈值或判定含义。
- **严重度**：minor。

### Readability & Flow

L-002 是本维度的主要问题。另有若干可在同一次修订中处理的局部模式：连续表格中常把“资格、方法、敏感性分析、停止规则”写入同一单元；多个段落以长串名词而非动作主干开头。建议优先显露句子主语与判定动作，例如分别使用“进入条件是……”“合格要求是……”“不合格时……”；这能提高可扫读性而不改变科学内容。

---

## Language Revision Priorities

1. **Terminology Consistency**：3 项 — 在摘要和研究问题首次定义“观测桥接”及一维摘要，统一外部测试对象名称，并展开 CRF、SAP。
2. **Readability & Flow**：1 个跨章节模式 — 将资格、阈值和失败分支分层表达，拆分高密度长句与表格单元，保留全部条件。
3. **Conciseness & Redundancy**：1 项 — 重写并统一“错误结构高置信误判”这一长语块，降低重复名词化。
4. **Grammar & Syntax / Register**：2 项 — 消除“访视稀疏”的修饰歧义，并将正文中的 `dossier` 改为自然中文。

---

## Re-Assessment Status

本次为当前冻结文本的全新独立评估，不是基于匿名问题清单的复评；未比较任何先前分数、决定、文本版本或修订差异。

---

## Assessment Notes

- 本评估只判断学术语言，不判断研究设计的科学有效性、统计方法是否正确、创新性、可行性、影响力或期刊适配性。
- 全稿已按 complete dossier 范围阅读。参考文献仅检查语言与格式表现；未读取其链接来源，也未核验引文内容。
- 目标期刊未指定，因此采用中文生物医学、临床研究和技术研究的一般正式写作约定。英文契约固定标题及前置元数据未计入中文正文评分；只有项目内部词汇进入读者可见正文时才记录问题。
- 中文“词”边界不能与英文量表机械等同；语法门槛依据明确错误在全部读者可见正文中的密度和分布判断。未见接近门槛的模式。
- 针对 L-001 的定向术语审查受冻结输入边界限制，未调用外部术语来源。结论仅基于目标读者画像、首次出现位置及文本自身后续定义；因此建议使用直接描述，而不是宣称某一替代名称具有外部标准地位。
- 所有修订方向均要求保留原有研究对象、阈值、时间点、条件分支和停止规则；未建议修改来源文本本身。
