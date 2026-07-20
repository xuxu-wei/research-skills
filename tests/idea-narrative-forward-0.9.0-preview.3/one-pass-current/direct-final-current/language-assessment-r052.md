---
review_id: language-assessment-I01-001-r052
reviewer_skill: academic-language-assessor
reviewer_instance_id: fresh-academic-language-assessor-r052
workflow_id: RID-SEPSIS-CSM-20260717-001
round_id: r052
input_artifact_ids:
  - idea-dossier-I01-001-v034
  - reader-handoff-forward-001
input_versions:
  - v034
  - v001
scope: complete_idea_dossier
dossier_ref:
  artifact_id: idea-dossier-I01-001-v034
  version: v034
  path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current/idea-dossier-v034.md
reader_handoff:
  artifact_id: reader-handoff-forward-001
  version: v001
  path: tests/idea-narrative-forward-0.9.0-preview.3/run-001/inputs/reader-handoff.yaml
files_read:
  - AGENTS.md
  - research-skills-openai/skills/academic-language-assessor/SKILL.md
  - research-skills-openai/skills/academic-language-assessor/references/language-assessment-rubric.md
  - research-skills-openai/skills/academic-language-assessor/references/language-hard-gates.md
  - research-skills-openai/skills/academic-language-assessor/references/chinese-academic-language-conventions.md
  - research-skills-openai/skills/academic-language-assessor/references/discipline-language-conventions.md
  - research-skills-openai/skills/academic-language-assessor/references/terminology-review.md
  - research-skills-openai/skills/academic-language-assessor/templates/language-assessment-report.md
  - research-skills-openai/skills/academic-language-assessor/scripts/validate_language_assessment.py
  - tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current/idea-dossier-v034.md
  - tests/idea-narrative-forward-0.9.0-preview.3/run-001/inputs/reader-handoff.yaml
isolation_mode: fresh_subagent
prior_scores_visible: false
source_edits_performed: false
decision: major_language_revision
findings:
  - finding_id: LANG-R052-001
    severity: major
    category: terminology_coherence
    dossier_locator:
      - "Title, summary, audience, and positioning > One-sentence complete-Idea summary"
      - "Structured abstract > Approach"
      - "Research design and methods > Hospital-primary genuine cross-database validation"
      - "Evidence chains > 医院优先且未触碰的跨数据库检验"
      - "Feasibility, resources, risks, alternatives, and stop conditions > Limitations and boundary conditions"
    current_problem: >-
      核心外部评价概念在“真正未触碰”“未触碰测试”“完全隔离”“不作更新”和“有限更新”之间切换。“未触碰”是非学术化隐喻，且有时指测试数据未参与开发，有时又与模型不更新连写；数据隔离和评价时不更新模型是两个不同条件，现有标签使跨学科读者需要反推二者的边界。
    target_state: >-
      分别用稳定的描述性表达命名数据隔离条件和模型更新条件，并在首次出现处明确二者的关系，随后全篇保持同一用法。
    required_change_or_replacement: >-
      对数据隔离统一使用“未参与模型开发、模型选择或阈值设定的独立外部测试数据（或测试区）”；对主要分析统一使用“不利用适配区或测试区数据更新模型的外部评价”。删除“真正”和“未触碰”隐喻，不把“数据未参与开发”与“模型不更新”压缩成同一短标签。
    content_to_preserve:
      - 外部数据库按医院分为适配区和测试区
      - 测试区不参与变量、时间方案、状态数、锚点、分区、更新层级或阈值选择
      - 不更新模型、仅校准、仅更新观测层三种分析须分开报告
    acceptance_test: >-
      首次描述外部检验时，读者能分别回答哪些数据未参与开发以及哪一种分析不使用外部数据更新模型；正文不再以“真正未触碰”“未触碰测试”或“完全隔离”代替这两个条件，且三种外部分析名称前后一致。
  - finding_id: LANG-R052-002
    severity: major
    category: terminology_coherence
    dossier_locator:
      - "Structured abstract > Approach and Expected result"
      - "Research question, objectives, and core hypothesis > Primary research question and Objective 4"
      - "Research design and methods > Conditional trial-observation projection and independent clinical-state analysis"
      - "Expected outputs, falsification criteria, and interpretations > Interpretation matrix"
      - "Contribution, innovation, impact, application, and closest-work comparison > evidence-level table"
    current_problem: >-
      同一个替代试验结局被称为“试验特异性等级结局”“独立等级结局”“独立临床等级结局”“独立 SOFA 等级结局”和“独立试验临床状态”。其中“SOFA 等级结局”还会使读者误以为结局只由 SOFA 构成，而实际定义同时包含死亡、住院期间 SOFA 排序和存活出院。
    target_state: >-
      为该结局采用一个能直接说明对象和范围的中文名称，在首次出现时完整定义三个等级组成，之后只使用该名称或一个明确对应的已定义简称。
    required_change_or_replacement: >-
      统一为“试验特异性临床等级结局分析”，首次定义为“死亡为最差等级，访视时住院存活者按 SOFA 由高到低排序，访视前存活出院者为最佳等级；该结局与阶段 II 表征无关”。不得单独改称“SOFA 等级结局”或“临床状态差异”。
    content_to_preserve:
      - 死亡、住院期间 SOFA 和存活出院的固定排序
      - 每项试验分别分析
      - 该替代结局仅在观测连接不成立但试验核心语义可核验时使用
      - 该分析与阶段 II 表征无关
    acceptance_test: >-
      摘要、研究问题、方法、结果解释、贡献表和风险表对该结局使用同一名称；首次定义同时包含三个等级和与阶段 II 无关的限定，后续没有“独立 SOFA 等级结局”“独立临床状态差异”等竞争标签。
  - finding_id: LANG-R052-003
    severity: major
    category: terminology_accessibility
    dossier_locator:
      - "Structured abstract > Objective and hypothesis; Expected result; Contribution and impact"
      - "Background, current state, gap, significance, and rationale > Rationale"
      - "Research question, objectives, and core hypothesis > Objectives 2-3 and Core hypothesis"
      - "Research design and methods > Absolute simulation and semi-synthetic recovery criteria"
      - "Evidence chains > 数据支持、锚定与绝对恢复"
    current_problem: >-
      “绝对恢复”“绝对模拟检验”“绝对判定”与“错误结构高置信判断”承担核心假设和模型选择功能，但这些压缩标签不是跨重症医学、临床流行病学、纵向统计和系统辨识读者都能直接理解的标准表达。“绝对”容易被读成完全恢复，而“错误结构高置信判断”的修饰关系不清楚。
    target_state: >-
      首次出现时直接说明检验对象、绝对阈值的作用以及空结构或错设情形下要控制的错误；如需短称，使用一个与该直接说明明确对应的描述性短语。
    required_change_or_replacement: >-
      首次表述改为“在预设数据生成情景下，按固定阈值评价状态、转移和结构恢复，并量化空结构或错设情形下错误地以高置信度判断存在结构的频率”。后文可统一简称“预设阈值的模拟恢复检验”，不要继续使用“绝对恢复”或“错误结构高置信判断”作为独立名词。
    content_to_preserve:
      - 正确、零边、过拟合和错设生成情景
      - 状态、转移、符号或滞后、覆盖率及错误发现的固定阈值
      - 空结构或错设情形下错误高置信结论的控制
      - 未达标时删除、合并、降级或停止结构解释的既定后果
    acceptance_test: >-
      摘要首次出现处无需项目词汇表即可说明检验的对象和失败含义；后文只保留一个稳定短称，且“错误地以高置信度判断存在结构”的施事、对象和错误性质没有修饰歧义。
  - finding_id: LANG-R052-004
    severity: major
    category: academic_register_internal_workflow_leakage
    dossier_locator:
      - "Title, summary, audience, and positioning > Positioning and contribution frame"
      - "Research content and work packages > dated-criteria table and minimum route"
      - "Key techniques and implementation > items 2-10"
      - "Contribution, innovation, impact, application, and closest-work comparison > opening paragraph and claim-support table"
      - "Feasibility, resources, risks, alternatives, and stop conditions > Working assumptions and risk table"
    current_problem: >-
      “研究治理设计”“准入”“自动降级”“打开测试区”“封存”“防火墙”“审计器”“投影器”“预编码”和“失败分支”等流程化或软件化词汇反复进入面向研究者的正文。它们把科学条件和预设分析选择写成内部状态转换，降低了中文学术语体的自然度，并与读者不得预先熟悉项目内部工作词汇的基线不符。
    target_state: >-
      用自然科学语言直接陈述条件、分析动作和后果；保留必要的预先固定、数据隔离、记录归档和替代分析含义，但不使用系统状态或软件组件隐喻。
    required_change_or_replacement: >-
      将“研究治理设计”改为“预先规定的分析、判定与停止规则”；将“准入/自动降级”改为“满足标准后继续评价/未满足时改用预先规定的简化模型”；将“打开测试区”改为“开始独立外部评价”；将“封存”改为“固定并归档”；将“变量角色防火墙”改为“变量用途隔离规则”；将“审计器/投影器/预编码/失败分支”分别改为其实际执行的审计程序、计算方法、预先规定的分析规则或替代分析方案。
    content_to_preserve:
      - 所有日期、阈值和停止条件
      - 独立数据保管与测试数据隔离
      - 复杂模型与简化模型之间的预设选择规则
      - 条件性试验分析的两种互斥方案
    acceptance_test: >-
      所列章节中的每个流程标签均被可直接执行的科学动作或条件替代；读者无需理解“准入、降级、封存、分支”等内部状态词也能准确复述何时继续、何时改用其他模型、何时停止以及何时归档结果。
  - finding_id: LANG-R052-005
    severity: major
    category: readability_qualifier_stacking
    dossier_locator:
      - "Structured abstract > Approach"
      - "Research question, objectives, and core hypothesis > Primary research question"
      - "Research design and methods > 试验语义与共同锚点资格判定（R0）"
      - "Research design and methods > 测量不变性、校准和绝对投影忠实度判定（R1）"
    current_problem: >-
      核心研究问题把阶段 II 的三个目标、阶段 III 的启动条件、观测摘要比较和替代结局压入一个问句；摘要 Approach 以及 R0/R1 段落也把目的、输入、资格、阈值和失败后果堆叠在少数长句中。语法虽基本成立，但跨学科读者需要回读才能确认每个条件修饰哪一分析对象。
    target_state: >-
      每个句子承担一个主要功能，先说明科学对象或目的，再说明资格条件、实施规则和失败后果；阶段 II 与条件性阶段 III 的问题在语法上分开。
    required_change_or_replacement: >-
      将 Primary research question 拆为阶段 II 主问题和条件性试验问题两个问句。将摘要 Approach 拆为外部评价、试验观测摘要和替代结局三个连续句。将 R0/R1 各自拆成“目的与输入—资格或阈值—不满足时后果”，或使用紧凑表格列出标准；不得删除任何科学条件。
    content_to_preserve:
      - 阶段 II 的全病程、任务和跨库稳定性目标
      - 阶段 III 仅在阶段 II 与试验语义满足时启动
      - 观测投影摘要的来源、访视和随机组比较
      - R0/R1 的全部资格、阈值和替代或停止后果
    acceptance_test: >-
      主研究问题可独立读出阶段 II 与阶段 III 两个问题；摘要和 R0/R1 中每句只有一个主动作，所有条件都有无歧义的修饰对象，且数值、访视、变量资格和失败后果完整保留。
  - finding_id: LANG-R052-006
    severity: minor
    category: mixed_chinese_english_and_first_use
    dossier_locator:
      - "Data, materials, and existing evidence base > Public ICU database roles and G1 audit"
      - "Research design and methods > Protocol locks for the two primary clinical tasks"
      - "Research design and methods > Observational target, anchoring, missingness and abstention"
      - "Research design and methods > Absolute simulation and semi-synthetic recovery criteria"
      - "Required analyses and evidence > items 4-6"
    current_problem: >-
      正文在已有自然中文表达时仍反复切换到 onset、ICU stay、bootstrap、pattern-mixture delta、tipping-point、canonical correlation 和 proper scoring rule。部分术语首次出现没有中文功能说明，降低了跨学科读者的可及性；“首次新发 onset”还形成中英文语义重复。
    target_state: >-
      以中文为主，在首次出现处给出必要英文或缩写，并在后文保持一种写法；暂未确认统一中文译名的术语应直接说明其统计功能。
    required_change_or_replacement: >-
      使用“首次发病”“ICU 停留（或重症监护停留）”“自助法（bootstrap）”“模式混合模型的 δ 位移分析”“选择模型临界点分析”“典型相关系数”；proper scoring rule 若继续保留英文，应在首次出现处说明其用于评价概率预测分布质量且预期预测分布使期望评分最优，不用未确认的压缩中文标签替代。
    content_to_preserve: >-
      保留所有统计量、分析功能、符号、阈值以及尚待方法学负责人确认中文译名的事实。
    acceptance_test: >-
      所列英文术语均在首次读者使用处有中文对象或功能说明，后文不再在中文与英文形式之间无规则切换，且“首次新发 onset”等重复形式消失。
  - finding_id: LANG-R052-007
    severity: minor
    category: chinese_lexical_naturalness
    dossier_locator:
      - "Background, current state, gap, significance, and rationale > Gap"
      - "Research question, objectives, and core hypothesis > Core hypothesis and non-hypotheses"
      - "Title and positioning claim-support table > 计划跨数据库检验 row"
    current_problem: >-
      “这些孤立能力”“五条证据链分别闭合到”和“不作更新首先”等搭配不符合自然中文学术表达；“孤立能力”把研究方法拟人化，“闭合到”缺少自然的支配关系，“不作更新首先”语序不完整。
    target_state: >-
      使用主谓关系明确、无直译痕迹的学术中文，直接说明已有研究、分析与证据对象之间的对应关系。
    required_change_or_replacement: >-
      分别改为“这些分别建立的方法或证据仍不能回答……”“五类分析分别对应数据边界、可恢复不变量……”“以不更新模型的外部评价为首要分析”，并检查相邻句是否仍保留原限定。
    content_to_preserve: >-
      保留既有工作分散、五类证据对象分别对应以及不更新模型的外部评价优先于有限更新的含义。
    acceptance_test: >-
      三处语句均具有明确主语、谓语和宾语，删除拟人化或直译搭配后不改变证据范围和分析优先级。
unresolved_issues:
  - LANG-R052-001
  - LANG-R052-002
  - LANG-R052-003
  - LANG-R052-004
  - LANG-R052-005
  - LANG-R052-006
  - LANG-R052-007
---

# Language Assessment Report

**Assessment ID**: language-assessment-I01-001-r052  
**Target Language**: Chinese (zh-CN)  
**Discipline**: 重症医学、临床流行病学、纵向统计、系统辨识与医学人工智能交叉研究  
**Target Journal**: 未指定  
**Scope**: complete_idea_dossier  
**Date**: 2026-07-19

---

## Overall Language Readiness

**Level**: major_language_revision

**Recommendation**: revise_language

正文的语法、计划时态和因果限定总体稳定，但三个核心概念存在跨章节命名漂移或压缩标签歧义，触发术语一致性硬门槛。流程化隐喻和长句限定堆叠进一步增加跨学科读者负担。问题可通过定向语言修订解决，不需要专业编辑重写全文。

---

## Dimension Scores

| Dimension | Score (1–10) | Severity |
|---|---:|---|
| Grammar & Syntax | 8 | pass |
| Academic Register & Tone | 6 | borderline |
| Terminology Consistency | 4 | fail |
| Tense & Voice Conventions | 9 | pass |
| Conciseness & Redundancy | 5 | borderline |
| Readability & Flow | 5 | borderline |

---

## Hard Gate Status

**Overall**: fail

| Gate | Status | Detail |
|---|---|---|
| Grammar error density | pass | 约 0–1 个明确语法错误/500 个中文词语单位；主要问题是搭配和信息密度，不是系统性语法错误 |
| Academic register | pass | 语体总体正式；流程化隐喻分布较广，但没有达到口语或非正式语体占主导的门槛 |
| Terminology coherence | fail | 3 个核心概念存在竞争标签或不可及压缩标签：外部数据隔离与不更新评价、替代试验等级结局、预设阈值的模拟恢复与错误高置信结论控制 |
| Tense systematic violation | pass | 作为研究构想，全文以计划、条件和未来执行时态为主，未把计划工作系统性写成已完成结果 |

---

## Strengths

- 研究状态表达一致：摘要、资源表、方法和限制均把模型、模拟、外部评价和试验分析写为计划或尚未生成，没有系统性时态错置。
- 因果语言总体审慎，预测、观察性关系、随机分配组间差异和因果机制之间的边界表达清楚。
- 多数常见缩写在首次读者使用处得到定义，例如 HMM、MDP、MPC、RL、SOFA、CIF、MNAR、ESS、ARI 和 NMAE。
- 表格较好地承载了日期、阈值、状态定义和风险后果，数值格式与比较方向基本一致。

---

## Specific Issues

### Chinese Academic Clarity

- `LANG-R052-004`：多个章节使用“准入、自动降级、封存、防火墙、投影器、失败分支”等内部流程词或隐喻。应改为明确的科学条件、分析动作和停止后果。严重度：major。
- `LANG-R052-005`：Primary research question、摘要 Approach 及 R0/R1 段落把对象、条件、阈值和后果堆叠在长句中。应按功能拆句或改为标准表格。严重度：major。
- `LANG-R052-007`：“孤立能力”“闭合到”“不作更新首先”属于不自然搭配，应改为主谓宾明确的中文表达。严重度：minor。

### Grammar & Syntax

未见达到硬门槛的系统性语法错误。局部问题主要是 `LANG-R052-007` 所列搭配和 `LANG-R052-005` 所列过度从属结构，而不是句法规则普遍失控。

### Academic Register & Tone

正文没有口语、感叹或宣传式断言，整体保持正式语体。主要偏差是 `LANG-R052-004` 中的软件组件和流程状态隐喻，以及“真正未触碰”中的防御性加强词“真正”。这些表达应改为可验证的研究动作。

### Terminology Consistency

仅记录触发 focused review 的核心术语；未生成完整术语清单，也未进行外部检索。三个问题都可用直接描述性表达安全判断，术语标准性不会改变本次决定。

| id | term_or_phrase | locator | reader_baseline | problem | recommended_replacement | first_use_definition | basis | acceptance_test |
|---|---|---|---|---|---|---|---|---|
| LANG-R052-001 | 真正未触碰／未触碰测试／完全隔离／不作更新 | summary；abstract Approach；Hospital-primary validation；Evidence chains | 熟悉外部验证，但不熟悉项目短标签 | 混合了测试数据未参与开发和评价时不更新模型两个条件 | 分别使用“未参与开发的独立外部测试数据”和“不利用外部数据更新模型的评价” | 首次同时说明数据隔离范围和三种更新分析 | dossier 已给出两类操作的完整含义，直接描述即可，无需外部标准性检索 | 两个条件可分别复述，全篇无竞争隐喻 |
| LANG-R052-002 | 试验特异性等级结局／独立等级结局／独立临床等级结局／独立 SOFA 等级结局／临床状态差异 | abstract；primary question；trial methods；interpretation；contribution | 熟悉临床复合或等级结局，但不熟悉项目标签 | 同一三层结局使用至少五种名称，“SOFA 等级结局”还遗漏死亡和出院构成 | “试验特异性临床等级结局分析” | 死亡最差、住院存活者按 SOFA 排序、存活出院最佳，并与阶段 II 无关 | dossier 自身的操作定义足以支持描述性名称，无需外部验证 | 所有核心位置只使用一个名称及其明确定义 |
| LANG-R052-003 | 绝对恢复／绝对模拟检验／绝对判定／错误结构高置信判断 | abstract；Rationale；Objectives；simulation criteria；Evidence chains | 熟悉模拟与模型验证，但不应假定熟悉项目术语 | “绝对”与“错误结构高置信判断”的语义和修饰关系不透明 | “预设阈值的模拟恢复检验”，首次用完整描述 | 在预设生成情景下评价恢复，并量化空结构或错设下错误高置信结论 | 检验对象和阈值已在 dossier 中展开，直接描述优于另造短标签 | 摘要首次出现即可识别对象、标准和失败含义 |

### Tense & Voice Conventions

pass。本文是研究构想而非完成研究，使用“计划、须、将、若……则……”符合预研究文本惯例。资源和结果状态也持续标为待核验或尚未生成。

### Conciseness & Redundancy

同一组资格条件和证据边界在摘要、研究问题、证据链、贡献表和限制部分以相近词串重复。语言修订应优先消除重复标签与防御性加强词，但不应由语言评审决定删除哪个科学条件或改变权威限制位置。最明显的压缩对象是“真正未触碰”“条件性的……增量”“复杂模型备选方案”和多种“冻结／分支”短语。

### Readability & Flow

宏观章节顺序清楚，表格也提供了良好定位；主要障碍集中在核心问句和 R0/R1 技术段落。按照 `LANG-R052-005` 将“目的—资格—阈值—后果”分开后，读者应能不回读地确认条件所属的阶段和分析对象。

---

## Language Revision Priorities

1. **Terminology coherence**: 3 个核心概念 — 分离数据隔离与模型不更新，统一替代试验结局名称，并用描述性语言替代“绝对恢复／错误结构高置信判断”。
2. **Academic register**: 1 个系统性模式 — 把流程状态词和软件隐喻改为科学条件、动作与后果。
3. **Readability**: 4 个高负担位置 — 拆分主研究问题、摘要 Approach 和 R0/R1 段落，同时保留所有限定。
4. **Mixed-language consistency**: 1 个跨方法段落模式 — 统一 onset、ICU stay、bootstrap 等中英文形式并补足首次功能说明。
5. **Chinese lexical naturalness**: 3 个局部搭配 — 修正直译和语序问题。

---

## Re-Assessment Status

不适用。本次为完整 Idea dossier 的全新独立评审，没有读取匿名问题列表、既往语言报告、旧版本或修订差异。

---

## Assessment Notes

- 评审仅覆盖 v034 完整 dossier 与文件化 reader handoff；没有读取原稿、修订计划、修订差异、预检、内容保留报告、既往语言／叙事／科学评估或工作流状态。
- 未指定目标期刊，因此采用中文重症医学、临床流行病学、纵向统计和系统辨识交叉研究的一般规范。
- 没有开展外部 focused terminology verification。所有触发术语都可依据 dossier 已写明的操作对象改为直接描述性表达；外部标准性结论不会改变硬门槛或决定。
- 本报告不评价研究问题、方法、阈值、可行性、创新性或证据强度，只评价语言可读性、术语、语体、时态和表达一致性。
