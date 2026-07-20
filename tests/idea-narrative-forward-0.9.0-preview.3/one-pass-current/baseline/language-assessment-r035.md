---
review_id: language-assessment-I01-001-r035
reviewer_skill: academic-language-assessor
reviewer_instance_id: baseline-language-r035-fresh-subagent
workflow_id: RID-SEPSIS-CSM-20260717-001
round_id: r035
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
  - research-skills-openai/skills/academic-language-assessor/references/chinese-academic-language-conventions.md
  - research-skills-openai/skills/academic-language-assessor/references/discipline-language-conventions.md
  - research-skills-openai/skills/academic-language-assessor/references/terminology-review.md
  - research-skills-openai/skills/academic-language-assessor/templates/language-assessment-report.md
  - research-skills-openai/skills/academic-language-assessor/scripts/validate_language_assessment.py
  - tests/idea-test-0.9.0-preview.1/0.9.0-preview.1/03_ideas/nodes/I01-001/dossiers/idea-dossier-v003.md
  - tests/idea-narrative-forward-0.9.0-preview.3/run-001/inputs/reader-handoff.yaml
isolation_mode: fresh_subagent
prior_scores_visible: false
source_edits_performed: false
decision: major_language_revision
findings:
  - finding_id: LA-R035-001
    severity: major
    category: readability_and_flow
    dossier_locator: "Title, summary, audience, and positioning > One-sentence complete-Idea summary（第 32 行）"
    current_problem: >-
      该句约 303 个中文字符，在一个句法单元中同时承载研究对象、两阶段公共数据库研究、两项试验、多个判定条件、替代分析和禁止性解释；核心名词尚未定义，主谓关系被连续条件和限定语淹没，跨学科读者必须回读才能提取主要目标。
    target_state: >-
      保持“一句话摘要”形式，但先明确研究对象和阶段 I–II 的核心动作，再用一个清楚的条件分句交代阶段 III 的从属关系；读者在首次阅读时即可区分主要研究与条件性扩展。
    required_change_or_replacement: >-
      按“研究对象与目标—公共 ICU 数据中的构建和跨数据库验证—满足预设条件后才开展的 RCT 次要分析”重组为一个主干清楚的句子。把数值阈值、完整失败分支和成串禁止性主张留在相应技术或限制位置；摘要中若必须保留边界，只用一项足以防止实质误读的自然语言限定。不得在摘要中使用尚未定义的项目短称。
    content_to_preserve:
      - 脓毒症发病前、首次发病、发病后演化和结局的全病程边界
      - 阶段 I–II 是核心且拟在 24 个月内完成
      - 跨数据库验证属于核心设计
      - RCT 分析是后续、次要且有条件的扩展
      - 不把观察性预测或表示升级为因果、控制或数字孪生证据
    acceptance_test: >-
      将修订后的一句话单独交给符合 reader handoff 的读者；读者无需查看后文即可准确说出研究对象、主要验证路线和 RCT 分析的条件性角色，且句中没有依赖后文定义才能辨认的核心术语或悬空修饰语。
  - finding_id: LA-R035-002
    severity: major
    category: terminology_reader_access
    dossier_locator:
      - "Title, summary, audience, and positioning > One-sentence complete-Idea summary（第 32 行）"
      - "Structured abstract > Approach、Expected result、Contribution and impact（第 40–42 行）"
      - "Research question, objectives, and core hypothesis（第 60、67 行）"
      - "Research design and methods > Conditional trial-observation projection and independent fallback（第 242–254 行）"
    current_problem: >-
      “观测投影”“冻结观测投影”“投影可观测状态摘要”“投影可观测摘要”“RCT 可观测代理”和“投影忠实度”在核心问题、摘要和贡献处承担不同语法角色，却在首次出现时没有说明分别指映射、映射输出还是一致程度；详细公式直到后文才出现。对不熟悉项目自造短称的目标读者，这些表达无法在首次出现处确定指代。
    target_state: >-
      首次出现时直接说明科学操作及其输出，并稳定区分“从阶段 II 模型到试验观测指标的映射”“由试验实际访视指标计算的低维状态摘要”以及“该摘要与阶段 II 状态表示的一致程度”；后文短称只在定义后使用。
    required_change_or_replacement: >-
      在摘要和研究问题中，以“将冻结的阶段 II 模型按预先确定的规则映射到 RCT 实际访视指标，并由这些指标计算低维状态摘要”替代未定义的紧缩短称。方法部分分别命名映射、输出摘要和一致程度，不再用“投影”一个词根同时承担三种功能；若保留 P_state、P_obs 等符号，应在同一处先给出自然语言定义。这里的直接描述是读者可理解的功能表达，不应再压缩成另一个未经核验的项目术语。
    content_to_preserve:
      - 映射在治疗组比较前确定
      - 映射仅使用试验实际可观测指标
      - 两项试验分别处理
      - 映射不成立时改用与阶段 II 独立的临床状态分析
      - 映射结果不验证完整潜在状态、动力学或系统模型
    acceptance_test: >-
      在标题、摘要、研究问题和首次方法定义四处逐一检查：读者能在当前位置指出哪个短语是映射、哪个是输出、哪个是一致程度；同一概念只保留一个名称；任何后续短称均在首次使用时由同句自然语言定义。
  - finding_id: LA-R035-003
    severity: major
    category: academic_register_and_workflow_vocabulary
    dossier_locator:
      - "Structured abstract（第 38–42 行）"
      - "Background, current state, gap, significance, and rationale（第 46–54 行）"
      - "Research content and work packages（第 77–112 行）"
      - "Key techniques and implementation（第 267–278 行）"
      - "Expected outputs, falsification criteria, and interpretations（第 339–370 行）"
    current_problem: >-
      面向研究者的正文系统性使用“门、冻结、降级、停止、失败产物、防火墙、封印、未触碰、按门实施”等内部控制或项目治理词汇。全文“门”字约 65 次、“冻结”约 49 次、“降级”约 25 次；这些词并非口语错误，但把正式科研说明写成状态机和审计操作记录，且 G1 等项目标签在承担研究设计含义前没有自然语言定义。
    target_state: >-
      读者正文用科学动作和判定功能本身来表述：预先规定的纳入或判定标准、在查看结果前确定的分析方案、未参与开发或调参的外部测试集，以及未满足条件时采用的预设替代分析。内部标签只在确有复用价值且已定义时保留。
    required_change_or_replacement: >-
      逐个按功能改写，而不是机械同义词替换。例如：“绝对模拟恢复门”改为“预先规定的模拟恢复标准”；“真正未触碰的外部检验”改为“在未参与模型开发或参数调整的外部测试集中验证”；“自动降级”改为“未满足标准时按预先规定改用较简单模型或独立临床结局分析”；“变量角色防火墙”改为“预先区分生理测量、治疗、观测过程和结局标签的变量使用规则”；“医院优先外部封印”改为“按医院预先划分并在模型确定前保持隔离的外部测试集”。G1 首次出现时写明它是“双数据库可观测性与样本支持审计”，之后才可使用短称。
    content_to_preserve:
      - 所有实际判定标准和时间顺序
      - 结果访问前预先确定分析的要求
      - 未满足条件时的具体替代路线
      - 外部测试集隔离和数据泄漏防护
      - 不得越级解释的科学边界
    acceptance_test: >-
      对所列位置逐句审查：每个控制性表达均能让读者直接知道科学动作、判定依据和后果；没有任何句子要求读者先学习项目状态机隐喻，且 G1 或其他短称的首次出现均附有自然语言所指。
  - finding_id: LA-R035-004
    severity: major
    category: compound_title_modifier_attachment
    dossier_locator:
      - "文档标题与 Title 字段（第 27、31 行）"
      - "Objectives > 条件性稀疏 RCT 次要再分析（第 67 行）"
    current_problem: >-
      “条件性稀疏 RCT 次要再分析”按普通中文修饰关系容易被理解为“RCT 本身稀疏”或“某种名为条件性稀疏 RCT 的设计”，而正文实际描述的是仅在若干条件满足后，利用稀疏访视数据进行试验次要分析。“条件性”究竟修饰是否开展分析还是分析方法也不清楚。
    target_state: >-
      “稀疏”明确修饰访视或重复测量数据，“仅在条件满足时”明确修饰是否开展次要分析；标题不依赖项目短称来传达这两个关系。
    required_change_or_replacement: >-
      将标题尾部改为“以及仅在预设条件满足时，使用 RCT 的稀疏访视数据开展的次要分析”，或使用语义完全等价且修饰附着同样明确的表达；其中条件修饰“开展”，RCT 明确是数据来源，“稀疏”只修饰访视数据，“次要”只修饰分析。在一句话摘要中用自然语言概括条件为阶段 II 验证结果和试验实际访视数据能否支持预定分析，而不把所有技术判定塞回标题。
    content_to_preserve:
      - RCT 分析是次要分析
      - RCT 分析只在预设条件满足后开展
      - 稀疏性指实际访视或重复测量数据
      - 不把阶段 III 写成阶段 II 的确定组成或补救手段
    acceptance_test: >-
      将修订标题脱离正文交给三类目标读者解析；所有读者均把“稀疏”连接到访视数据，把条件连接到是否开展分析，并且不会把标题理解为一种名为“条件性稀疏 RCT”的试验设计。
  - finding_id: LA-R035-005
    severity: major
    category: bilingual_terminology_coherence
    dossier_locator:
      - "Title, summary, audience, and positioning 与 Structured abstract（第 32–42 行）"
      - "Research content and work packages（第 81–110 行）"
      - "Research design and methods > Hospital-primary genuine cross-database validation、Conditional trial-observation projection and independent fallback（第 228–261 行）"
      - "Evidence chains 与 Required analyses and evidence（第 280–337 行）"
      - "Contribution、claim-support 与 risk tables（第 372–435 行）"
    current_problem: >-
      中文正文反复嵌入 benchmark/resource、proper score、fallback、projection-pass、death-ranked SOFA、trial-specific clinical-state reanalysis、all-randomized/mITT、fidelity 等未统一定义的英文短称；同一功能又在其他位置写成中文，造成中英文漂移。D7/D8 在摘要首次出现时也没有说明是试验规定访视，且其相对随机化或首剂的时间参照仍待核验。zero-update、运输/运输性及目标场景更新的角色混用另列 LA-R035-009，避免把不同操作继续压缩为一个词根。
    target_state: >-
      正文以稳定、可直接理解的中文功能描述为主；确有必要的英文术语或缩写在首次出现处以括号给出一次，并保持后续用法一致。尚未确定的时间或统计细节明确标为待核验，不由语言修订代为选择。
    required_change_or_replacement: >-
      采用直接描述并逐项统一：“可复用的基准数据与分析资源”；“proper scoring rule（指如实报告预测概率时可使期望评分最优的评分规则）”，不猜测一个未经核验的紧缩中文译名；将 fallback 写成“未满足相应标准时，按预先规定改用独立临床状态分析”；将 projection-pass 写成“该映射达到预先规定的一致性和误差标准”；将 fidelity 写成“该摘要与阶段 II 状态表示的一致程度”；将 death-ranked SOFA 写成“死亡置于最差等级、存活者按 SOFA 评分排序的临床状态”；另统一为“试验特异的独立次要临床状态再分析”和“全体随机化受试者分析集”。D7/D8 首次出现时写成“试验规定的 D7/D8 访视”，并明确相对随机化或首剂的具体时间参照待原始方案核验。对每个替换词重新检查读者可理解性和修饰附着，不再创造紧缩短称。
    content_to_preserve:
      - 统计方法和分析集之间的实质区别
      - 死亡、存活住院和活着出院的排序规则
      - D7/D8 时间参照尚未核验这一事实
      - 两项试验不合并及其不同分析集状态
    acceptance_test: >-
      建立仅覆盖所列问题词的核对表：每个概念在首次出现处有一个清楚的中文名称或定义，后文不再无理由切换中英文；替换后逐句解析修饰关系；任何尚未确定的时间或分析选择仍明确显示为待核验而非被润色成既定事实。
  - finding_id: LA-R035-009
    severity: major
    category: terminology_role_separation
    dossier_locator:
      - "Title, summary, audience, and positioning 与 Structured abstract（第 34、39–42 行）"
      - "Research content and work packages（第 86–110 行）"
      - "Research design and methods > Hospital-primary genuine cross-database validation（第 228–240 行）"
      - "Evidence chain: 医院优先、未触碰的计划跨数据库检验（第 306–312 行）"
      - "Interpretation matrix、Contribution 与 risk matrix（第 360–366、376–394、422–431 行）"
    current_problem: >-
      “运输、运输性、运输失败、适配后运输、transport updating”和 zero-update 在不同位置分别表示未经更新时的跨数据库表现、未达到该表现、使用目标数据库适配集进行有限更新，以及在目标数据库重新开发模型；这些功能被同一“运输”词根和未定义英文短称压缩，读者无法稳定判断当前句子说的是被检验的性质、失败结果还是更新操作。
    target_state: >-
      按角色分别直接陈述：冻结模型在不重新估计参数时接受外部验证；该验证达到或未达到预设标准；使用目标数据库适配集只重新校准或只更新观测模型；在目标数据库上完整重新拟合属于模型更新或再开发。正文不再依赖“运输性”作为包办这些功能的短称。
    required_change_or_replacement: >-
      第一次描述不更新性质时写“在另一数据库中不重新估计参数时，模型的预测性能和状态表示是否保持稳定”；失败时写“冻结模型在未更新参数的外部测试中未达到预设标准”；有限更新时分别写“使用预留适配集重新校准”或“仅使用预留适配集更新观测模型”；全模型更新时写“在目标数据库上重新拟合或重新开发模型，不属于外部验证”。zero-update 首次出现如确需保留英文，只能在“不更新模型参数的外部验证（zero-update validation）”之后作为括注，后文优先使用功能性中文。正式文献题名中的 transportability 保持原题，不据此创造正文短称。
    content_to_preserve:
      - 不更新模型参数的外部测试是主要跨数据库验证
      - 仅重新校准、仅更新观测模型与完整重新拟合是不同操作
      - 有限更新后的成功不能替代不更新参数时的失败
      - 适配集与最终测试集的隔离关系
      - 完整重新拟合不属于外部验证
    acceptance_test: >-
      对所列每个“运输/transport/zero-update”实例分类：每句只能落入“不更新参数的外部验证、该验证的通过或失败、有限适配更新、完整重新开发”四个角色之一，且句内直接写出角色；除正式文献题名和首次括注外，读者正文不再用同一紧缩词根替代这些不同功能。
  - finding_id: LA-R035-006
    severity: major
    category: concision_and_redundancy
    dossier_locator:
      - "Title/summary 与 Structured abstract（第 32–42 行）"
      - "Core hypothesis and non-hypotheses（第 69–73 行）"
      - "Evidence chains（第 280–320 行）"
      - "Interpretation matrix（第 360–370 行）"
      - "Title and positioning claim-support table（第 399–410 行）"
      - "Feasibility、risks 与 final stop boundary（第 412–439 行）"
    current_problem: >-
      “不支持因果网络、潜在动力学、转移边、中介、控制、数字孪生或整个模型验证”等限制以高度近似的词串在摘要、假设、方法输出、证据链、解释矩阵、定位表和风险部分重复。重复并未增加新的语言精度，反而使正向研究陈述被防御性限定打断。
    target_state: >-
      每项独特科学限制完整保留，但相同限制不再以近乎逐字相同的长串多次出现；只有在当前位置确实需要防止实质误读时才保留简短、局部相关的限定。语言修改不新增跨章节指针。
    required_change_or_replacement: >-
      先把所列位置中的重复限制按语义聚类，并由叙事修订计划给出每个实例的保留或删除决定；writer 只删除被判为重复的副本，合并同一位置的近义词串，不删除任何独特限制，也不自行改变限制强度。若某一限制被判定为推进当前位置推理所必需，则改成只覆盖该局部误读的短句，不复述完整禁止清单，也不写“见某节”之类指针。
    content_to_preserve:
      - 观察性数据不支持因果、控制或数字孪生主张
      - RCT 次要分析的证据范围
      - 阶段与替代分析之间的条件关系
      - 所有其他独特且科学上必要的限制
      - 原有限定的证据强度
    acceptance_test: >-
      对照语义聚类逐项核验：每项独特限制至少有一个明确保留位置；没有同一完整禁止清单的近乎逐字副本；任何局部重复均有叙事计划记录的必要功能；全文未新增跨章节限制指针，且限制强度没有被语言修订削弱。
  - finding_id: LA-R035-007
    severity: minor
    category: first_use_definition
    dossier_locator: "Background, current state, gap, significance, and rationale 与 Objectives（第 46、60、64 行）"
    current_problem: >-
      landmark 在中文核心叙述中直接出现，虽为纵向预测常用术语，但并非所有重症医学、系统科学和转化研究读者都可在首次出现时立即判断它指重复设定的动态预测时点。
    target_state: >-
      首次出现时用中文说明其功能，后续再使用英文短称。
    required_change_or_replacement: "首次写为“重复设定的动态预测时点（landmark）”，后文保持 landmark 或统一中文称谓。"
    content_to_preserve: "每 12 小时设定预测时点及其历史窗、预测窗的设计。"
    acceptance_test: "首次出现处不查看后文即可知道 landmark 是预测时点而非结局、时间窗或样本。"
  - finding_id: LA-R035-008
    severity: minor
    category: unnatural_literal_or_project_expression
    dossier_locator:
      - "Background, current state, gap, significance, and rationale（第 50 行）"
      - "Contribution, innovation, impact, application, and closest-work comparison（第 387–397 行）"
    current_problem: >-
      “最近近邻”“verified representative neighbor”“closest-work”等表达在中文中不自然，并把文献比较写成项目内部检索标签；它们容易让读者停顿判断是距离度量、研究类别还是最相近既有工作。
    target_state: "统一使用直接的文献功能表达，例如“与本研究最接近的既有研究”或“代表性相关研究”。"
    required_change_or_replacement: >-
      第 50 行改为“与本研究最接近的既有研究表明，单个模块本身并非新颖”；相应小标题和表头统一为“代表性相关研究比较”，仅在机器字段中保留 closest-work 标签。
    content_to_preserve: "文献比较的范围、检索置信度和不得据此声称全球首次的限定。"
    acceptance_test: "读者无需了解项目检索标签即可理解该段在比较既有研究；正文中不再混用三个名称指向同一文献比较功能。"
unresolved_issues:
  - LA-R035-001
  - LA-R035-002
  - LA-R035-003
  - LA-R035-004
  - LA-R035-005
  - LA-R035-009
  - LA-R035-006
  - LA-R035-007
  - LA-R035-008
---

# Language Assessment Report

**Assessment ID**: language-assessment-I01-001-r035  
**Target Language**: Chinese（夹有必要的英文名称与缩写）  
**Discipline**: 重症医学、临床流行病学、纵向统计、系统辨识、系统科学与医学 AI 的跨学科研究构想  
**Target Journal**: 未指定  
**Scope**: 完整 Idea dossier（只读 v003）  
**Date**: 2026-07-19

---

## Overall Language Readiness

**Level**: major_language_revision

**Recommendation**: revise_language

文本的语法和计划时态总体稳定，但核心术语、读者正文中的内部控制词、一句话摘要负荷、中英文短称与重复限定共同造成系统性阅读障碍。尤其是“观测投影/投影可观测摘要”在标题级内容和研究问题中先于定义出现，触发 Idea dossier 的术语可理解性硬门；因此当前文本不能作为语言就绪稿。

---

## Dimension Scores

| Dimension | Score (1–10) | Severity |
|---|---:|---|
| Grammar & Syntax | 8 | pass |
| Academic Register & Tone | 5 | borderline |
| Terminology Consistency | 3 | fail |
| Tense & Voice Conventions | 8 | pass |
| Conciseness & Redundancy | 3 | fail |
| Readability & Flow | 3 | fail |

---

## Hard Gate Status

**Overall**: fail

| Gate | Status | Detail |
|---|---|---|
| Grammar error density | pass | 全文未见达到每 500 词项超过 3 个明确语法错误的系统性模式；中文未按英文词界机械折算。 |
| Academic register | pass | 没有跨两节的系统性口语或非正式语体；主要问题是正式但审计化、状态机化的项目内部语体。 |
| Terminology coherence | fail | 核心“观测投影/投影可观测摘要”在摘要、研究问题和贡献处首次不可理解，并在映射、输出与一致程度三种功能之间变体使用；G1 等项目标签也晚于其实际使用才获得部分语义。 |
| Tense systematic violation | pass | 研究构想、计划任务和预期产物总体使用前瞻性表达，没有把计划结果系统性写成已完成结果。 |

---

## Strengths

1. 研究计划、当前证据状态与尚未生成的结果在时态上大体分开，没有系统性把拟开展工作写成既成事实。
2. Sepsis-3、SOFA、MIMIC-IV、eICU-CRD、EXIT-SEP 与 XBJ-SCAP 等正式名称和数据库标识总体稳定。
3. 定量标准、时间窗和分析分支虽然密集，但大多使用明确数值与条件句，便于后续技术核对。
4. 文本持续区分观察性与随机化证据的语气强度；本评估只确认其语言限定保持一致，不判断这些科学边界本身是否充分。

---

## Specific Issues

### Chinese Academic Clarity

- **LA-R035-001（major）**：第 32 行的一句话摘要把核心对象、多个阶段、方法判定、替代路线和禁止性解释挤入约 303 个中文字符。应保留一句话形式，但恢复清楚的主干与信息顺序。
- **LA-R035-003（major）**：第 38–42、46–54、77–112、267–278、339–370 行的“门、冻结、降级、防火墙、封印、未触碰”等词使科研说明呈现内部审计记录语体；应改写为相应科学动作和决策功能。
- **LA-R035-009（major）**：第 34、39–42、86–110、228–240、306–312、360–394、422–431 行把未经更新时的跨数据库表现、该表现失败和针对目标数据库的更新都写入“运输/运输性”词族；必须按不同功能直接表述。
- **LA-R035-006（major）**：同一组禁止性解释在第 32–42、69–73、280–320、360–370、399–410、412–439 行反复列举。语言修订应去重但不得自行删除独特科学限制或指定其论证位置。

### Grammar & Syntax

未见需要单列为 major 的明确语法错误。主要句法风险来自超长并列和修饰附着，而非主谓不一致或残句：

- 第 32 行的一句话摘要需要重建主干（LA-R035-001）。
- 标题中的“条件性稀疏 RCT”存在修饰对象歧义（LA-R035-004）。
- 第 208–212、230–261 行的长句宜在不改变公式和条件的前提下，以“目的—定义—判定—后果”的顺序拆分；这属于 LA-R035-002、003 和 005 的执行范围。

### Academic Register & Tone

文本没有明显口语化，但多个核心段落使用项目治理语体而非面向跨学科研究者的学术说明。LA-R035-003 给出了按功能改写的具体方向。机器 frontmatter 与固定英文 H2 标题属于合同脚手架，本评估没有将其计为读者正文语言错误。

### Terminology Consistency

| id | term_or_phrase | locator | reader_baseline | problem | recommended_replacement | first_use_definition | basis | acceptance_test |
|---|---|---|---|---|---|---|---|---|
| LA-R035-002 | 观测投影／投影可观测状态摘要／RCT 可观测代理 | 第 32、40–42、60、67、242–254 行 | 熟悉纵向数据与验证，但不熟悉项目自造标签 | 首次出现不能区分映射、输出与一致程度；同一词根承担不同功能 | 直接写“将冻结的阶段 II 模型按预先确定规则映射到 RCT 实际访视指标，并由这些指标计算低维状态摘要” | 同时定义映射、摘要和一致程度，之后才可引入符号 | reader handoff 明确不假定项目短称；详细所指直到第 242–254 行才出现，未用外部来源猜测新标准短称 | 四个首次关键位置都能独立识别三种功能；名称一一对应 |
| LA-R035-004 | 条件性稀疏 RCT 次要再分析 | 第 27、31、67 行 | 熟悉 RCT，但不应猜测修饰关系 | “稀疏”表面修饰 RCT，“条件性”修饰对象不明 | “仅在预设条件满足时，使用 RCT 的稀疏访视数据开展的次要分析” | 摘要用自然语言说明阶段 II 结果与试验实际访视数据是否支持预定分析 | 正文第 167–171、242–261 行显示稀疏性属于访视数据且分析是否开展有前置条件 | 条件只修饰开展，RCT 只修饰数据来源，稀疏只修饰访视数据，次要只修饰分析 |
| LA-R035-005 | death-ranked SOFA、fallback、projection-pass 等 | 第 32–42、228–261、280–337、372–435 行 | 跨学科读者不应掌握未定义项目英文短称 | 中英文漂移，多个词既未定义又有中文变体 | 使用结构化 frontmatter 中列出的直接功能描述；proper scoring rule 保留英文标准名并在首次出现处解释其性质，不猜测紧缩中文译名 | 每个必要英文术语第一次出现时给出中文所指，不确定细节仍标为待核验 | 文本内部可直接证明各词承担的功能；未从单篇文献推定其为标准短称 | 每个概念仅有一个稳定名称，替换本身无新歧义或悬空修饰 |
| LA-R035-009 | 运输／运输性／运输失败／transport updating／zero-update | 第 34、39–42、86–110、228–240、306–312、360–394、422–431 行 | 熟悉外部验证与数据库差异，但不应猜测项目压缩词 | 同一词根混合未经更新时的性质、未达到该性质、有限适配更新和完整重新开发 | 分别写“不更新模型参数的外部验证”“未更新参数的外部测试未达标”“使用预留适配集重新校准／只更新观测模型”“在目标数据库重新拟合或重新开发模型” | zero-update 如需保留，只在第一种功能的完整中文定义后括注一次 | 角色差异由 dossier 第 228–240 行自身明确；正式文献题名中的 transportability 不作为正文短称证据 | 每个实例唯一归入四个角色且句内直写角色；正式题名和首次括注外不再以同一词根代替不同功能 |
| LA-R035-007 | landmark | 第 46、60、64 行 | 部分读者熟悉动态预测，其他读者未必熟悉 | 首次中文核心叙述未说明其功能 | “重复设定的动态预测时点（landmark）” | 在第一次正文使用处定义 | 目标读者跨越临床、系统科学和转化研究 | 首次出现即能区分预测时点、历史窗和预测窗 |
| LA-R035-008 | 最近近邻／closest-work | 第 50、387–397 行 | 熟悉文献比较，不熟悉项目检索标签 | 中文不自然且多名同指 | “与本研究最接近的既有研究”／“代表性相关研究比较” | 不需要另建短称 | 语境是文献比较而非距离度量 | 正文只保留自然中文功能表达 |

本次普通阅读已足以证明核心问题是首次可理解性和角色混用；因此没有为了寻找一个新的紧缩短称而检索外部来源。建议的替换均直接命名科学对象、操作或关系，并已重新检查触发条件、读者基线、证据需要与修饰附着。proper scoring rule 是唯一保留的英文方法名，但已配功能定义而没有猜测一个新的紧缩中文标签；正式文献题名不作正文用词证据。

### Tense & Voice Conventions

计划性 Idea dossier 使用“计划、将、拟、尚未、条件满足时”等前瞻表达是合适的。未发现方法或结果段系统性时态违例。修订时应继续保留“尚未生成”“待核验”“条件满足后”等证据状态，不得因语言流畅而改写成已经验证。

### Conciseness & Redundancy

- LA-R035-001：一句话摘要的信息负荷远超单句可稳定承载的范围。
- LA-R035-006：因果、动力学、控制、数字孪生和系统验证等禁止性解释被成串重复。
- 多个表格与正文重复同一判定与后果；语言修订可以合并近义重复，但涉及科学上是否必须在某推理点保留条件时，应服从独立 narrative repair plan，不由语言评估决定。

### Readability & Flow

- 核心对象与阶段关系在摘要中被技术短称和替代分支压住（LA-R035-001）。
- 读者在理解研究问题前即遇到“冻结观测投影门、投影可观测摘要、G1、zero-update”等概念（LA-R035-002、003、005）。
- 技术方法段可以保留公式与符号，但首次说明需要先写自然语言目的和所指，再给公式与判定标准。

---

## Language Revision Priorities

1. **核心术语与首次定义**：先修复 LA-R035-002、004、005，使标题、摘要和研究问题不依赖项目短称。
2. **一句话摘要**：按主要研究—核心验证—条件性扩展重建单句主干（LA-R035-001）。
3. **读者正文语体与角色分离**：把内部控制词改为具体科学动作、判定依据和后果，并分开不更新验证、验证失败、有限更新和重新开发（LA-R035-003、009）。
4. **删除与去重**：在叙事修订计划明确保留功能后，清除近义限制清单和重复限定（LA-R035-006）。
5. **局部首次定义与自然表达**：完成 landmark 和文献比较称谓的统一（LA-R035-007、008）。

---

## Re-Assessment Status

这是 Idea workflow 的首次独立完整 dossier 语言评估；未读取任何旧问题清单、旧报告、其他 dossier 版本或 revision delta，因此不作历史问题关闭比较。

| Check | Current assessment |
|---|---|
| Listed issues no longer present | 不适用 |
| Listed issues still present | 不适用 |
| New current-text issues | 9（LA-R035-001 至 LA-R035-009） |

---

## Assessment Notes

- 本评估只判断语言、术语可理解性、修饰附着、中英文一致性、限定堆叠和阅读负荷；未判断方法是否正确，也未评价 novelty、impact、feasibility 或论证质量。
- 评估依据为冻结的 v003 完整 dossier 和指定 reader handoff。未读取 preflight、evaluator、narrative report、repair plan、revision delta、state/index/portfolio、其他 dossier 或 sibling Hermes 文件。
- 没有把 machine frontmatter、合同固定字段或数学符号本身当作科研正文错误；只有其项目短称泄漏到读者正文且未定义时才记录问题。
- 对重复限制的最终保留位置和局部必要性，应由 narrative repair plan 决定；语言修订不得借去重削弱科学限制，也不得新增跨章节指针。
