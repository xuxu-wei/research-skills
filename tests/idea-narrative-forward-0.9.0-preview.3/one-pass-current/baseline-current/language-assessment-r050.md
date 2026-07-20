---
review_id: language-assessment-r050
reviewer_skill: academic-language-assessor
reviewer_instance_id: fresh-baseline-language-r050
workflow_id: RID-SEPSIS-CSM-20260717-001
round_id: r050
input_artifact_ids:
  - idea-dossier-I01-001-v003
  - reader-handoff-forward-001
input_versions:
  - v003
  - v001
scope: complete_idea_dossier
dossier_ref:
  artifact_id: idea-dossier-I01-001-v003
  version: v003
  path: tests/idea-test-0.9.0-preview.1/0.9.0-preview.1/03_ideas/nodes/I01-001/dossiers/idea-dossier-v003.md
reader_handoff:
  artifact_id: reader-handoff-forward-001
  version: v001
  path: tests/idea-narrative-forward-0.9.0-preview.3/run-001/inputs/reader-handoff.yaml
files_read:
  - AGENTS.md
  - research-skills-openai/AGENTS.md
  - research-skills-openai/skills/academic-language-assessor/SKILL.md
  - research-skills-openai/skills/academic-language-assessor/references/language-assessment-rubric.md
  - research-skills-openai/skills/academic-language-assessor/references/language-hard-gates.md
  - research-skills-openai/skills/academic-language-assessor/references/terminology-review.md
  - research-skills-openai/skills/academic-language-assessor/templates/language-assessment-report.md
  - research-skills-openai/skills/academic-language-assessor/scripts/validate_language_assessment.py
  - tests/idea-narrative-forward-0.9.0-preview.3/run-001/inputs/reader-handoff.yaml
  - tests/idea-test-0.9.0-preview.1/0.9.0-preview.1/03_ideas/nodes/I01-001/dossiers/idea-dossier-v003.md
isolation_mode: fresh_subagent
prior_scores_visible: false
source_edits_performed: false
decision: major_language_revision
findings:
  - finding_id: LANG-R050-001
    severity: major
    category: terminology_modifier_attachment
    dossier_locator: "Title, lines 27 and 31"
    current_problem: >-
      “条件性稀疏 RCT 次要再分析”按通常修饰关系会把“稀疏”理解为 RCT 本身的属性，而正文实际指 D7/D8 等试验访视和重复测量稀疏；标题因而使核心研究对象产生实质性歧义。
    target_state: >-
      标题直接说明稀疏的是 RCT 访视数据，并让“条件性”明确限定次要分析的启动条件。
    required_change_or_replacement: >-
      将标题改为“脓毒症全病程候选动态系统表征：计划跨数据库检验与基于 RCT 稀疏访视数据的条件性次要分析”，并在一句话摘要中说明该分析仅在预设条件满足后启动。
    content_to_preserve: >-
      保留计划性跨数据库检验、RCT 分析的次要性质、访视稀疏性及分析启动的条件限制。
    acceptance_test: >-
      让未读正文的跨学科目标读者仅凭标题回答“什么是稀疏的”和“什么受条件限制”；答案必须分别是“RCT 访视数据”和“次要分析的启动”，且不得理解为 RCT 数量少或试验设计稀疏。
  - finding_id: LANG-R050-002
    severity: major
    category: terminology_first_use
    dossier_locator: "Title/summary line 32; Structured abstract lines 41-42; Primary research question line 60; Objective 4 line 67"
    current_problem: >-
      核心短语“投影可观测状态摘要”在一句话摘要中先于其科学对象、输入和映射方式出现，直到方法部分第 248-252 行才可判定其含义；“随机化扰动”又可能被理解为对潜在系统的物理或机制扰动，而正文实际限定为随机分配组间对访视摘要的比较。
    target_state: >-
      首次出现即用直接描述说明数据来源、计算方式、维度、访视和推断功能，之后才使用稳定短称；涉及试验比较时避免把组间对比写成系统机制扰动。
    required_change_or_replacement: >-
      在一句话摘要首次出现处改为“由冻结的阶段 II 观测模型根据 D7/D8 实测指标确定性计算的一维状态摘要（下称‘观测投影摘要’）”，并将该处及摘要、研究问题和目标中的“随机化扰动”改为“随机分配组间的访视摘要差异”。若作者确实意指超出组间差异的科学操作，须由试验统计负责人先确认后再定词。
    content_to_preserve: >-
      保留冻结映射、试验分别分析、实际 D7/D8 访视、条件性启动以及不支持潜在动力学或因果机制的边界。
    acceptance_test: >-
      首次出现后的读者能够不查阅方法部分说明该摘要由哪些观测数据、通过何种冻结关系、在何时计算以及用于何种比较；全文不得在定义前出现短称，也不得用“扰动”暗示正文明确排除的系统机制结论。
  - finding_id: LANG-R050-003
    severity: major
    category: terminology_first_use
    dossier_locator: "Title/summary line 32; Structured abstract line 41; Objective 4 line 67; Automatic independent fallback line 254; Planned outputs line 347"
    current_problem: >-
      “death-ranked SOFA”在摘要和目标中作为核心失败分支出现，但首次使用没有说明死亡、住院存活和存活出院的排序规则；中英混合的紧缩标签也不属于读者交接中可假定的共同知识。
    target_state: >-
      首次使用以中文直接陈述复合等级结局的三层排序和试验特异性，随后只用普通指代，不依赖项目自造短标签。
    required_change_or_replacement: >-
      首次出现时改为“死亡列为最差等级、访视时仍住院存活者按 SOFA 评分由高到低排序、访视前存活出院者列为最佳等级的试验特异性次要临床状态分析”；后文可用“该等级结局”指代。只有在作者提供跨学科读者可识别的标准术语依据时，才保留更短的专名。
    content_to_preserve: >-
      保留死亡优先排序、SOFA 仅用于住院存活者、存活出院为最有利等级、试验分别报告以及该分支与阶段 II 表征独立。
    acceptance_test: >-
      目标读者在术语首次出现处即可复述三类结局的完整顺序，并能明确该分析不是对阶段 II 表征的扰动或验证；不得要求读者跳到第 254 行才能理解。
  - finding_id: LANG-R050-004
    severity: major
    category: project_internal_vocabulary
    dossier_locator: "Title/summary line 32; Structured abstract lines 39-42; Objectives lines 64-67; dated criteria and minimum route lines 77-112; simulation criteria lines 214-226"
    current_problem: >-
      “阶段 I–II”“阶段 III”“G1”“绝对恢复/假置信门”及大量以“门”命名的短标签在首次读者接触时未先说明其证据内容和判定功能。读者交接明确不允许假定项目内部流程词汇或新标签，因此这些标签在核心摘要和设计说明中的裸用构成可访问性障碍。
    target_state: >-
      先用标准科研语言说明每个阶段包含的研究工作，以及每项标准决定何种准入、停止或降级；短标签仅在同句直接定义后作为后续索引。
    required_change_or_replacement: >-
      首次提及阶段时写明“公共 ICU 数据上的队列审计、模型恢复与跨数据库检验（阶段 I–II）”和“其后开展的 RCT 次要分析（阶段 III）”；将一般正文中的“门”按功能改为“预设准入标准”“预设判定标准”或“停止标准”；首次出现 G1 时写为“双库可观测性、事件支持与接口审计（G1）”；首次出现“绝对恢复/假置信”时写为“在预设模拟情景中对状态与转移恢复、区间覆盖和错误结构高置信判断进行的绝对判定标准”。R0/R1 标签亦须遵循先定义后简称。
    content_to_preserve: >-
      保留阶段顺序、所有预设阈值、不可越级规则、失败后果和自动降级路线，不改变任何研究设计。
    acceptance_test: >-
      对所有阶段和短标签执行首次出现检查：每个标签前或同句均有科学内容及判定功能的直接说明；抽取摘要给未见项目材料的目标读者时，读者无需内部词汇表即可说明各阶段和标准的作用。
  - finding_id: LANG-R050-005
    severity: major
    category: terminology_consistency
    dossier_locator: "Title lines 27 and 31; summary line 32; Structured abstract line 39; Background line 50; Primary research question line 60; Objective 2 line 65; minimum success line 92; observational target lines 208-212; Contribution line 376"
    current_problem: >-
      中心研究对象交替被称为“候选动态系统表征”“候选全病程表示”“候选状态表示”“候选架构”“候选系统表征”和“复杂表示”，而正文没有说明哪些是同一整体的短称、哪些是潜在状态层或复杂候选子模型。跨学科读者因此可能把同一对象误解为多个不同分析对象。
    target_state: >-
      为整体研究对象固定一个规范名称；只有在确指子组件时才使用不同术语，并在首次出现处说明其从属关系。
    required_change_or_replacement: >-
      以标题中的“脓毒症全病程候选动态系统表征”为整体对象的首次全称，后文统一用“该候选表征”；若“状态表征”专指 X_t 层、而“复杂候选”专指通过准入的非线性或切换模型，则在首次出现处分别写明“候选表征中的潜在状态层”和“候选表征的复杂模型备选方案”，不得把这些短称无标记地用于整体对象。
    content_to_preserve: >-
      保留整体表征、潜在状态层、基线模型和复杂候选模型之间原有的设计差异，以及“候选”与“计划”限定。
    acceptance_test: >-
      全文术语扫描显示整体对象只有一个规范全称和一个已声明短称；每个其他“表示/表征/架构/候选”用语均能明确归入整体对象或具体子组件，不再要求读者猜测同指关系。
  - finding_id: LANG-R050-006
    severity: minor
    category: cross_disciplinary_accessibility
    dossier_locator: "Background lines 50-54; minimum success lines 94-100; Work packages lines 106-112; methods lines 208-226 and 242-261; Key techniques lines 269-278"
    current_problem: >-
      HMM、MDP、MPC、RL、CIF、ARI、MNAR、ESS、NMAE 等跨学科缩写，以及 benchmark/resource、data-access no-go、proper score、zero-update、prediction-only 等英文短语，常在中文正文中未展开即密集出现。各词对单一专业读者可能熟悉，但不符合“不得假定每个参与学科的详细专长”的读者基线。
    target_state: >-
      每个必要缩写首次出现时给出中文功能名称和英文全称或缩写；普通流程词优先使用自然中文，数据库名、模型正式名称和数学符号除外。
    required_change_or_replacement: >-
      至少改为“隐马尔可夫模型（HMM）”“马尔可夫决策过程（MDP）”“模型预测控制（MPC）”“强化学习（RL）”“累积发生函数（CIF）”“调整兰德指数（ARI）”“非随机缺失（MNAR）”“有效样本量（ESS）”“归一化平均绝对误差（NMAE）”；将 benchmark/resource、data-access no-go、zero-update 和 prediction-only 分别改为“基准评测与可复用资源”“因数据访问不足而停止”“不作更新”和“仅作预测”。“proper score”应写出英文全称 proper scoring rule，并由纵向统计负责人确认最终中文译名。
    content_to_preserve: >-
      保留必要的国际缩写、正式数据库或模型名称、数学符号和技术精度。
    acceptance_test: >-
      对所有大写缩写和英文流程短语执行首次出现检查；除数据库专名和数学符号外，每个必要术语均在首次出现处获得跨学科可理解的功能说明，且同一概念之后只保留一种中英文形式。
  - finding_id: LANG-R050-007
    severity: minor
    category: concision_and_readability
    dossier_locator: "One-sentence summary line 32; Primary research question line 60; observational target lines 208-212; cross-database validation lines 230-240; closest-work synthesis line 397"
    current_problem: >-
      多个核心句同时承载研究对象、前置条件、分支、推断边界和否定性限定，并叠加斜线、括号、英文短称与数学符号；语法虽大体成立，但跨学科读者需要回读才能恢复主谓关系和条件层级。
    target_state: >-
      每个句群先陈述主命题，再按“条件—操作—结果—边界”顺序展开；一句话摘要保留单句合同形式，但减少嵌套并使用清楚的分号层级。
    required_change_or_replacement: >-
      将第 32 行组织为不超过三个顶层分句：阶段 I–II 的研究计划；RCT 次要分析的启动条件和两种分支；所有分支的推断边界。第 60 行保留三项编号但让每项只含一个谓语中心。第 208 行的概率式单列展示，并紧接一句非数学释义。第 230-240 行保留编号规则，但把分区、患者排除、支持判定和分析层级各自限定在单一段落功能内。
    content_to_preserve: >-
      保留所有前置条件、自动失败分支、阈值、推断限制和合同要求，不通过删去科学限定来换取简短。
    acceptance_test: >-
      目标读者可在一次阅读后分别标出每个句群的主命题、条件、操作、结果和边界；一句话摘要不超过三个顶层分句，公式后的文字解释不依赖符号即可理解。
  - finding_id: LANG-R050-008
    severity: minor
    category: lexical_repetition
    dossier_locator: "claim-boundary passages at lines 32, 42, 73, 252, 320, 385, 406 and 439; failure-language passages at lines 112, 296, 304, 312, 320, 347 and 351-358"
    current_problem: >-
      “不支持潜在动力学、转移边、中介、控制或整个模型”等边界清单及“失败不得由其他结果挽救”的句式在多个相邻论证功能中近乎逐字重复，削弱信息密度并放大文档长度。
    target_state: >-
      保留每个科学上必要位置的边界，但在同一局部功能内合并近义清单和重复否定句；跨章节保留位置的选择由叙事评估决定。
    required_change_or_replacement: >-
      先由叙事负责人确定每个边界必须出现的论证位置；语言修订仅在各已确定位置内合并重复词组，使用一次完整边界陈述加一次局部特异限定，不新增跨章节指针，也不自行删除科学条件。
    content_to_preserve: >-
      保留预测与因果的区分、投影摘要与潜在系统的区分、阶段 II 与 RCT 分支的独立性、失败后果和禁止挽救规则。
    acceptance_test: >-
      每个保留位置都含其论证所需的独特边界；同一段或相邻段不再重复五项以上的相同否定清单，且任何合并都未改变研究设计或允许主张。
unresolved_issues:
  - LANG-R050-001
  - LANG-R050-002
  - LANG-R050-003
  - LANG-R050-004
  - LANG-R050-005
  - LANG-R050-006
  - LANG-R050-007
  - LANG-R050-008
---

# Language Assessment Report

**Assessment ID**: language-assessment-r050  
**Target Language**: Chinese  
**Discipline**: 重症医学、临床流行病学、纵向统计、系统辨识、医学 AI 与转化研究  
**Target Journal**: 未指定  
**Scope**: complete_idea_dossier  
**Date**: 2026-07-19

---

## Overall Language Readiness

**Level**: major_language_revision

**Recommendation**: revise_language

全文语法和计划性时态总体稳定，但术语首次出现和一致性未达到所给跨学科读者基线。标题修饰歧义、未解释的核心短标签、项目内部阶段/判定标签及中心对象多种名称共同触发术语硬门槛；这些问题可通过有边界的语言修订解决，尚未显示需要全面专业代写的语法或语域模式。

---

## Dimension Scores

| Dimension | Score (1–10) | Severity |
|-----------|-------------|----------|
| Grammar & Syntax | 8 | pass |
| Academic Register & Tone | 8 | pass |
| Terminology Consistency | 3 | fail |
| Tense & Voice Conventions | 9 | pass |
| Conciseness & Redundancy | 5 | borderline |
| Readability & Flow | 4 | fail |

---

## Hard Gate Status

**Overall**: fail

| Gate | Status | Detail |
|------|--------|--------|
| Grammar error density | pass | 按硬门槛所列“明确且无争议的语法错误”计为 0/500 词当量；修饰歧义归入术语与可读性，不重复计为语法错误 |
| Academic register | pass | 无章节由口语、缩约、感叹或直接对话主导；英文流程短语的问题归入术语可访问性 |
| Terminology coherence | fail | 至少 5 个核心概念或标签簇受影响：标题中的“稀疏”修饰对象、观测投影摘要、SOFA 排序失败分支、阶段/判定标签、整体候选表征的多种名称 |
| Tense systematic violation | pass | 计划工作稳定使用将来或计划表达，既有证据使用现在时或过去时；Methods/Results 不存在与研究状态矛盾的系统性时态 |

---

## Strengths

- 计划产物、既有证据和未来条件之间的时态区分清楚，反复避免把未生成结果写成完成性结论。
- 因果、预测、投影摘要和完整潜在系统之间的主张边界在多数位置表达明确。
- 表格、编号和小标题为长篇技术内容提供了稳定导航，主要方法顺序可追踪。
- 数学符号在定义后保持稳定，X_t、Y_t、A_t、M_t、B 和 S 的角色未发生明显名称漂移。

---

## Specific Issues

### Chinese Academic Clarity (if applicable)

本报告未发现装饰性比喻或情绪化宣传语成为主要问题。主要中文清晰度问题是项目内部“门/阶段”标签、中英混排的压缩术语、标题修饰关系和多层条件句。固定合同标题和机器元数据未作为作者语言错误处理。

### Grammar & Syntax

未发现达到单独报告阈值的明确语法错误。第 27/31 行标题中的“稀疏”修饰歧义属于术语组合和修饰附着问题，见 LANG-R050-001。

### Academic Register & Tone

- **LANG-R050-006（minor）**：第 50-54、94-112、208-278 行的未展开英文缩写和流程短语使中文学术语体接近技术备忘录。按该条给出的首次出现替换清单处理；数据库专名、数学符号和必要国际缩写可在定义后保留。
- 未发现口语化、直接称呼读者、感叹或修辞问句形成系统模式，故语域硬门槛通过。

### Terminology Consistency

| id | term_or_phrase | locator | reader_baseline | problem | recommended_replacement | first_use_definition | basis | acceptance_test |
|---|---|---|---|---|---|---|---|---|
| LANG-R050-001 | 条件性稀疏 RCT 次要再分析 | Title, lines 27 and 31 | 不假定内部标签或所有学科细节 | “稀疏”通常附着于 RCT，而正文指访视数据 | 基于 RCT 稀疏访视数据的条件性次要分析 | 摘要中说明满足预设条件后才启动 | 第 54、242-261 行明确稀疏对象为实际访视/重复测量 | 盲读标题能正确指出稀疏对象和条件对象 |
| LANG-R050-002 | 投影可观测状态摘要；随机化扰动 | line 32; lines 41-42, 60, 67 | 可假定一般验证知识，不假定项目新标签 | 首用未说明输入、映射和功能；“扰动”可能误指机制操作 | 观测投影摘要；随机分配组间的访视摘要差异 | 由冻结观测模型根据 D7/D8 实测指标确定性计算的一维状态摘要 | 第 248-252 行给出映射与组间比较边界 | 定义前无短称；读者能复述输入、操作、访视和比较 |
| LANG-R050-003 | death-ranked SOFA | line 32; lines 41, 67, 254, 347 | 不假定新造英文标签 | 首用不含三类结局排序 | 直接写出死亡、住院存活者 SOFA 和存活出院的三级顺序 | 死亡最差、住院存活者按 SOFA 由高到低、存活出院最佳的试验特异性次要临床状态分析 | 第 254 行已有完整功能定义 | 首用处即可复述完整顺序和与阶段 II 的独立性 |
| LANG-R050-004 | 阶段 I–II、阶段 III、G1、绝对恢复/假置信门 | lines 32, 39-42, 64-112, 214-226 | 不假定内部流程词汇 | 核心摘要先用标签，后给内容；“门”未区分准入、判定和停止功能 | 先写研究工作或判定功能，再在括号中引入短标签 | 见结构化 finding 中的四项直接定义 | 读者交接明确禁止假定项目内部词汇 | 每个标签同句完成内容和功能定义 |
| LANG-R050-005 | 候选动态系统表征等六种同指形式 | lines 27-65, 92, 208-212, 376 | 跨学科共同体 | 整体对象、状态层和复杂模型的名称边界不清 | 整体统一为“该候选表征”，子组件明示从属关系 | 首次全称为“脓毒症全病程候选动态系统表征” | 标题和对象定义已提供可用规范全称 | 术语扫描只见一个整体规范名，其他名称均有从属说明 |
| LANG-R050-006 | HMM/MDP/MPC/RL/CIF/ARI/MNAR/ESS/NMAE 等 | lines 50-54, 94-112, 208-278 | 不假定每个学科的详细专长 | 缩写跨学科且首次出现未展开 | 首次出现给出中文功能名和英文缩写 | 见结构化 finding 中的逐项展开 | 缩写含义可由正文方法功能确定；proper scoring rule 的中文译名须由统计负责人确认 | 所有必要缩写首次出现均有功能说明且后续形式一致 |

推荐标题已重新解析：“基于 RCT 稀疏访视数据的”整体修饰“条件性次要分析”，“稀疏”直接修饰“访视数据”，未把歧义移动到试验本身或研究对象。

### Tense & Voice Conventions

none。全文作为预研究 Idea，计划性工作使用“计划”“将”“须”“若……则……”等形式；既有文献与资源现状使用现在时或完成性陈述，未发现系统性时态冲突。

### Conciseness & Redundancy

- **LANG-R050-008（minor）**：第 32、42、73、252、320、385、406、439 行的主张边界清单，以及第 112、296、304、312、320、347、351-358 行的失败不可挽救句式存在近乎逐字重复。只做局部语言合并；由叙事评估决定哪些论证位置必须保留，语言评估不指定跨章节删留。

### Readability & Flow

- **LANG-R050-007（minor）**：第 32、60、208-212、230-240、397 行同时叠加条件、分支、符号和否定限定。按“主命题—条件—操作—结果—边界”顺序重组；一句话摘要保持单句合同形式，但限制为不超过三个顶层分句。
- **LANG-R050-004（major）**同时影响流程可读性：裸用阶段名和判定标签迫使读者后向检索定义。完成首次出现定义后再复查段间衔接。

---

## Language Revision Priorities

1. **核心术语与标题**：5 项 major — 先修正标题修饰关系，再为观测投影摘要、SOFA 排序失败分支、阶段/判定标签和整体研究对象建立可直接理解的首次定义与统一短称。
2. **跨学科可访问性**：1 项 minor — 展开必要缩写，将一般流程英文改为自然中文；proper scoring rule 的最终中文译名由纵向统计负责人确认。
3. **可读性**：1 项 minor — 在不删除条件的前提下重组超载句，显式呈现条件层级。
4. **简洁性**：1 项 minor — 在叙事负责人确定保留位置后，局部合并重复的边界和失败清单。

---

## Re-Assessment Status (if applicable)

不适用。本报告是对 v003 完整 dossier 的 fresh baseline assessment，未接收或读取既往问题清单、分数、决定、修订记录或其他 dossier 版本。

---

## Assessment Notes

- 本次只评估学术语言、术语可访问性和表达一致性；未判断研究设计、统计阈值、可行性、创新性或文献主张是否科学成立。
- 读者基线来自绑定的 `reader-handoff-forward-001@v001`：可假定一般重症研究、纵向数据、验证和不确定性知识，但不可假定项目内部词汇、新标签或每个参与学科的详细专长。
- 未读取任何历史 narrative、language、repair、preflight、evaluator、其他 dossier、Hermes Skill 或测试输出；未编辑源 dossier。
- 未检索外部术语来源。所有触发项都可依据标题修饰关系、读者基线及 dossier 后文已有直接定义判定；本报告不以“未检得完整短语”证明术语非标准。对可能影响科学含义的“随机化扰动”以及 proper scoring rule 中文译名，已明确要求相应统计负责人确认，未作猜测。
- 英文合同标题、机器 frontmatter 和固定字段标签视为结构性脚手架；未要求作者翻译或改名。若其本身需面向中文读者本地化，应作为非阻断的 schema 设计事项单独处理。

