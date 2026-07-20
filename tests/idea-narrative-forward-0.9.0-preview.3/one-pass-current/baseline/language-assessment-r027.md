---
review_id: language-assessment-r027
reviewer_skill: academic-language-assessor
reviewer_instance_id: fresh-raw-language-r027
workflow_id: RID-SEPSIS-CSM-20260717-001
round_id: one-pass-current-baseline
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
  - research-skills-openai/skills/academic-language-assessor/references/english-academic-language-conventions.md
  - research-skills-openai/skills/academic-language-assessor/references/chinese-academic-language-conventions.md
  - research-skills-openai/skills/academic-language-assessor/references/discipline-language-conventions.md
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
  - finding_id: LA-R027-001
    severity: major
    category: terminology_and_title_modifier_attachment
    dossier_locator: "H1 title and section 1 Title field"
    current_problem: "稀疏在普通句法中误附到 RCT，且研究对象修饰关系不清。"
    target_state: "稀疏只修饰访视数据，条件只约束 RCT 次要再分析。"
    required_change_or_replacement: "采用报告正文给出的已复核替换标题。"
    content_to_preserve: "候选性质、计划中的跨库检验、RCT 条件性和次要分析性质。"
    acceptance_test: "陌生读者能仅凭标题正确指出稀疏对象、条件对象和计划状态。"
  - finding_id: LA-R027-002
    severity: major
    category: core_term_accessibility_and_consistency
    dossier_locator: "section 1 summary; section 2 objective; section 3 Background; sections 4, 11"
    current_problem: "中央研究对象首次出现时未定义，表征与表示交替使用。"
    target_state: "首次使用即说明对象、组成和用途，后文使用唯一名称。"
    required_change_or_replacement: "按报告正文给出首次定义并统一为候选动态系统表征。"
    content_to_preserve: "知识约束、不确定性、状态与转移及状态—行动—观察区分。"
    acceptance_test: "读者在首次出现处即可复述该对象表示什么、区分什么及为何是候选。"
  - finding_id: LA-R027-003
    severity: major
    category: project_stage_labels
    dossier_locator: "section 1 summary and section 2 objective/approach"
    current_problem: "阶段 I–III 承担证据顺序，却要求读者从后文反推内容。"
    target_state: "每个阶段编号首次出现时同时说明内容、时间和依赖。"
    required_change_or_replacement: "在首次出现处展开阶段 I–II 与条件性阶段 III。"
    content_to_preserve: "24 个月范围、阶段 III 非最低交付及其晚于阶段 II。"
    acceptance_test: "读者无需跳转即可说明各阶段内容、时间边界和前后依赖。"
  - finding_id: LA-R027-004
    severity: major
    category: simulation_validation_terminology
    dossier_locator: "section 1 summary; section 2 objective/approach; sections 3–4; section 7 simulation"
    current_problem: "绝对恢复门与假置信门是项目化简称，且绝对容易被误解。"
    target_state: "以检验对象和预设判定方式命名模拟验证。"
    required_change_or_replacement: "统一改为按预设数值阈值进行的模拟恢复与伪结构控制检验。"
    content_to_preserve: "各模拟情景、恢复与错误控制、校准弃权及不可由预测补偿。"
    acceptance_test: "读者可说明恢复对象、受控错误和预设判定依据。"
  - finding_id: LA-R027-005
    severity: major
    category: projection_terminology
    dossier_locator: "section 1 summary; section 2 approach; sections 3–4; section 7 RCT branch; sections 9–11"
    current_problem: "冻结观测投影门等表达混合内部流程与歧义数学修饰。"
    target_state: "首次表述明确输入、映射固定时点、忠实度检验和随机组间输出。"
    required_change_or_replacement: "使用预先固定的观测变量投影、由实际观测变量投影得到的状态摘要等报告内替换。"
    content_to_preserve: "映射先固定、仅实际访视、忠实度前置及结论不外推。"
    acceptance_test: "首次阅读即可识别投影输入、固定时点、检验位置和比较对象。"
  - finding_id: LA-R027-006
    severity: major
    category: fallback_endpoint_terminology
    dossier_locator: "section 1 summary; section 2 approach; section 7 RCT branch; sections 9, 11–14"
    current_problem: "death-ranked SOFA 与 fallback 不能自足说明三层排序及分支角色。"
    target_state: "首次出现展开三个排序层级，并建立唯一自然中文短称。"
    required_change_or_replacement: "采用独立的死亡分层 SOFA 再分析及报告正文给出的完整首次定义。"
    content_to_preserve: "死亡最差、出院最优、在院 SOFA 排序及与阶段 II 独立。"
    acceptance_test: "短称出现前已给出全部排序层级，且不再出现裸露 fallback/death-ranked。"
  - finding_id: LA-R027-007
    severity: major
    category: g1_label_definition
    dossier_locator: "section 5 timeline/work packages and section 6 public ICU database roles"
    current_problem: "G1 多次控制研究路径后才让读者从表格反推其含义。"
    target_state: "G1 第一次出现即带内容型中文名称。"
    required_change_or_replacement: "首次写为双数据库可观测性与数据支持审计（G1）。"
    content_to_preserve: "事件、转移、医院、锚点、接口、缺失、复杂度及失败后果。"
    acceptance_test: "每个后续 G1 均能唯一回指首次中文定义。"
  - finding_id: LA-R027-008
    severity: major
    category: r0_r1_label_definition
    dossier_locator: "section 7 RCT branch headings and sections 9, 11, 13–14"
    current_problem: "R0/R1 首次用英文项目标签，无法仅凭名称区分检验对象。"
    target_state: "首次用中文科学名称说明对象，编号仅作括号短称。"
    required_change_or_replacement: "采用试验语义与共同锚点合格性检验（R0）及测量一致性、校准与投影忠实度检验（R1）。"
    content_to_preserve: "两组资格、校准、遮蔽检查和各自失败后果。"
    acceptance_test: "只看标题即可区分 R0 与 R1，后文编号均有唯一回指。"
  - finding_id: LA-R027-009
    severity: major
    category: summary_readability
    dossier_locator: "section 1 One-sentence complete-Idea summary"
    current_problem: "一个超长句堆叠研究对象、两阶段验证、条件分支和多组边界。"
    target_state: "保留一个可独立理解的简洁句子，依次交代研究对象、24 个月主验证路径和条件性试验角色。"
    required_change_or_replacement: "重写为一个主干清楚的句子；把分支算法、失败后果和完整边界移出摘要，不用括号或分号堆回原句。"
    content_to_preserve: "两个公共 ICU 数据库、全病程对象、候选性质、24 个月主验证路径及试验分析的条件性。"
    acceptance_test: "修改后只有一个句号结句，目标读者可一次读出研究什么、如何验证以及试验分析为何是条件性的。"
  - finding_id: LA-R027-010
    severity: major
    category: criteria_readability
    dossier_locator: "section 7 R0 paragraph, R1 paragraph, two trial table rows, and RCT-start paragraph"
    current_problem: "来源、资格、阈值、缺失、后果和禁止操作压入同一段或表格单元。"
    target_state: "按材料、核验、资格、阈值和失败后果使用平行可勾选项目。"
    required_change_or_replacement: "按报告正文列出的分组拆分四个精确位置，并合并共同规则。"
    content_to_preserve: "每个阈值、来源限制、排序、缺失、中心、多重性和停止后果。"
    acceptance_test: "原有每项条件都有唯一新位置，每个项目只表达一种核对操作。"
  - finding_id: LA-R027-011
    severity: major
    category: cross_disciplinary_shorthand
    dossier_locator: "sections 4–8 and sections 10–11 at each listed acronym's first reader-visible use"
    current_problem: "多个统计、系统辨识、机器学习和试验缩写未在首次出现时释义。"
    target_state: "首次出现给出中文名称和英文缩写，普通流程动作改用中文。"
    required_change_or_replacement: "采用报告正文列出的 CIF、IPCW、AUPRC、ARI、MAE、FDR、SVD、NMAE、MI、FWER、mITT、CRPS、ESS、MCSE 对应关系。"
    content_to_preserve: "数据库和试验正式名称、数学符号、代码所需缩写及技术含义。"
    acceptance_test: "逐项搜索时，每个首次出现均有中文全称，后续写法唯一。"
  - finding_id: LA-R027-012
    severity: minor
    category: concision_and_repetition
  - finding_id: LA-R027-013
    severity: minor
    category: academic_register
unresolved_issues:
  - LA-R027-001
  - LA-R027-002
  - LA-R027-003
  - LA-R027-004
  - LA-R027-005
  - LA-R027-006
  - LA-R027-007
  - LA-R027-008
  - LA-R027-009
  - LA-R027-010
  - LA-R027-011
  - LA-R027-012
  - LA-R027-013
---

# 学术语言评估报告

**评估编号**：language-assessment-r027  
**目标语言**：中文（zh-CN；正文含较多英文缩写）  
**学科**：重症医学与临床流行病学，结合纵向统计、系统辨识和医学人工智能  
**目标期刊**：未指定  
**范围**：完整的读者可见 dossier；机器前置元数据仅用于确认产物身份，不纳入语言评分  
**评估日期**：2026-07-19

## 总体语言准备度

**级别**：`major_language_revision`  
**建议**：`revise_language`

文本的语法和时态总体稳定，但当前版本不适合直接交给设定的跨学科读者。标题存在关键修饰语误附风险；中央研究对象、阶段名称和多组验证标签在首次出现时没有用自然科学语言说明；方法部分还大量依赖未经释义的中英文缩写。上述问题使读者必须先掌握项目自身的命名体系，才能理解研究对象、证据顺序和随机试验分支，因此术语一致性硬性门槛未通过。

## 评估范围与已评估章节

已评估标题、标题与摘要定位、结构式摘要、背景与研究缺口、研究问题与目标、研究内容与工作包、数据与现有证据、研究设计与方法、关键技术、五条证据链、必需分析、预期产物与证伪标准、解释矩阵、贡献与近邻比较、标题主张支持表、可行性与停止条件以及参考文献。参考文献仅检查格式和正文衔接，不核验科学内容。

读者基线采用交接文件中的设定：可假定读者熟悉重症研究、纵向临床数据、验证、不确定性以及观察性与干预性证据的区别；不可假定其熟悉项目内部词汇、新造标签或所有参与学科的专门缩写。

## 六维评分

| 维度 | 分数（1–10） | 判定 | 依据 |
|---|---:|---|---|
| 语法与句法 | 8 | 通过 | 清楚的语法错误很少；主要问题是修饰语附着和过长句，而非普遍语法失误。 |
| 学术语域与语气 | 5 | 临界 | 论述谨慎，但“门”“冻结”“救回”“开 test”“fallback”等项目流程表达和中英文混写削弱正式学术语域。 |
| 术语质量与一致性 | 3 | 未通过 | 多个承担标题、研究对象、证据阶段和主要分支的核心术语在首次出现时不可由目标读者直接识别；“表征/表示”等名称也未说明是否同义。 |
| 时态与语态 | 9 | 通过 | 计划性研究始终使用将来或条件性表述，未把尚未完成的工作写成既有结果。 |
| 简洁性与冗余 | 4 | 临界 | 多处堆叠条件、限定和否定性边界；相近的禁用主张清单反复出现。 |
| 可读性与衔接 | 4 | 临界 | 摘要和方法关键段落把多个决策、阈值及失败分支压入单句或单个表格单元，跨学科读者难以一次提取主干。 |

## 硬性门槛结果

**总体**：未通过

| 门槛 | 状态 | 说明 |
|---|---|---|
| 语法错误密度 | 通过 | 人工估计不超过 1 个明确语法错误/500 个中文词语单位；修饰语歧义另计入术语与可读性。 |
| 学术语域 | 通过 | 存在大量项目流程简称，但尚未达到两个章节均以口语为主的阈值。 |
| 术语连贯性 | 未通过 | 标题中的“稀疏 RCT”支持错误读法；中央表征、阶段 I–III、模拟检验、G1、R0/R1、投影分支及独立 SOFA 分支均承担核心论证，却未在首次使用时向设定读者说明。 |
| 时态系统性违例 | 通过 | 本 dossier 是计划性产物，使用将来、条件和预设性表述符合学科惯例。 |

## 优点

- 计划、现状和未来结果之间的证据状态区分稳定；“计划产物，不是现有模型或验证结果”等表达能防止时态和证据状态漂移。
- 因果、预测、状态表征和随机试验次要分析之间的语言边界总体明确，没有把预测表现直接写成因果机制。
- 数值阈值、时间窗和失败后果通常给出明确主语与条件，便于后续进行技术核对。
- 标题、摘要、研究问题、目标和解释矩阵围绕同一研究对象展开，宏观指向一致。

## 具体问题

### LA-R027-001（major）：标题中的修饰语附着错误

- **精确位置**：主标题（第 27 行）和 Title 条目（第 31 行）：“脓毒症全病程候选动态系统表征：计划跨数据库检验与条件性稀疏 RCT 次要再分析”。
- **当前问题**：“稀疏”按普通汉语句法首先修饰紧随其后的“RCT”，容易被理解为“样本稀疏的随机试验”；正文实际表达的是随机试验的访视和重复测量稀疏。“全病程候选动态系统表征”也连续堆叠四个修饰成分，读者需要自行判断“全病程”修饰研究对象还是表征范围。
- **目标状态**：标题直接说明候选表征覆盖脓毒症全病程；“稀疏”只修饰访视数据；“满足预设条件后”只修饰 RCT 次要再分析。
- **经重新解析的替换标题**：**“脓毒症全病程的候选动态系统表征：计划开展跨数据库检验，并在满足预设条件后基于稀疏访视数据开展 RCT 次要再分析”**。
- **替换标题的修饰关系复核**：“脓毒症全病程的”限定“候选动态系统表征”；“计划开展”限定“跨数据库检验”；“在满足预设条件后”限定第二项行动；“基于稀疏访视数据”限定“开展 RCT 次要再分析”；“次要”只限定“再分析”。没有修饰语再把“稀疏”附着到 RCT 本身。
- **必须保留**：候选而非既成模型、跨数据库检验仍属计划、RCT 分析有前置条件、数据是稀疏访视、分析是次要再分析。
- **验收测试**：让不掌握项目词汇的读者仅凭标题分别指出“什么是稀疏的”“条件约束哪项行动”“哪项工作尚属计划”；答案应分别为“访视数据”“RCT 次要再分析”“跨数据库检验及后续分析”，且不得出现“稀疏 RCT”的读法。

### LA-R027-002（major）：中央研究对象未在首次出现时定义，且“表征/表示”交替使用

- **精确位置**：One-sentence summary（第 32 行）首次使用“候选动态系统表征”；Structured abstract 的 Objective and hypothesis（第 39 行）改称“候选全病程表示”；Background（第 52 行）、Conjunctive minimum success definition（第 95 行）和 Interpretation matrix（第 370 行）继续使用“表示”；Primary research question（第 60 行）又回到“表征”。
- **当前问题**：对重症医学、临床流行病学和系统辨识的共同读者而言，“候选动态系统表征”不能直接说明其科学指称；“表征”和“表示”又像同义替换，读者无法判断二者是否对应不同对象。
- **目标状态**：在第 32 行第一次使用时，以一句直接定义说明对象、组成和用途；此后选择“候选动态系统表征”作为唯一名称。若作者确实需要区分“表征”与“表示”，必须在首次分化处说明区别。
- **要求的首次定义**：可采用“**一种以患者随时间变化的状态及其转移为核心、以知识约束限定结构、量化不确定性，并区分生理测量、治疗行动和测量过程的候选模型表示（下称‘候选动态系统表征’）**”。随后把第 39、52、95 和 370 行中指向同一对象的“表示”统一为“表征”。
- **必须保留**：知识约束、不确定性、患者时间状态与状态转移、状态—行动—观察的区分、候选和非因果性质。
- **验收测试**：读者在读完第 32 行后即可回答该表征“表示什么、区分什么、为何是候选”；全文每次出现“表征/表示”均能判断是同一对象或有明确定义的不同对象。

### LA-R027-003（major）：阶段 I–III 在承担证据顺序时没有首次定义

- **精确位置**：第 32 行首次出现“阶段 I–II 证据”；第 40 行首次出现“阶段 III”；第 79–88 行才给出日期门，但仍未用一句话说明阶段 I、II、III 各自包含什么。
- **当前问题**：阶段编号决定主要交付、外部检验与 RCT 分支的先后关系，属于核心术语；当前文本要求读者从分散的月份和工作包反推阶段内容。
- **目标状态**：在第 32 行首次出现阶段编号时说明阶段 I 与 II 的内容，在第 40 行首次出现阶段 III 时说明其内容和时间边界。
- **要求的修改**：把第 32 行的“建立阶段 I–II 证据”扩展为“**先完成双数据库可观测性审计、模拟恢复和开发验证，再完成未用于开发的跨数据库外部检验（合称阶段 I–II）**”；把第 40 行的“阶段 III”改为“**24 个月后、以条件性 RCT 次要再分析为内容的阶段 III**”。若项目对阶段 I 和 II 有更严格的既定分界，应使用该分界，但必须在同一首次定义处列明。
- **必须保留**：阶段 I–II 在 24 个月内完成、阶段 III 不属于最低交付、RCT 分支必须晚于阶段 II。
- **验收测试**：首次读到每个阶段编号时，读者无需跳转即可说出该阶段的主要内容、时间边界和与下一阶段的依赖关系。

### LA-R027-004（major）：模拟验证标签使用项目化简称，科学指称不透明

- **精确位置**：第 32 行“绝对模拟恢复门”；第 39 行“绝对恢复/假置信门”；第 41 行“恢复/假置信/弃权记录”；第 50、66、71 行继续使用“绝对门”“假置信门”；第 214–226 行才列出具体模拟与阈值。
- **当前问题**：“绝对”“恢复门”“假置信”不是目标读者可共同识别的标准组合。“绝对”还可能被误解为不依赖模型或场景的绝对证明，而正文实际指预设数值阈值下的模拟恢复、伪结构误判和弃权检验。
- **目标状态**：首次出现时用检验对象和判定方式命名；后文只使用已经定义的短称。
- **要求的修改**：第 32 行使用“**按预设数值阈值进行的模拟恢复与伪结构控制检验**”；第 39 行以后统一为“**模拟恢复与伪结构控制检验**”。若保留“绝对恢复”作为短称，须在首次定义中明确“绝对”仅表示与固定阈值比较，而非证明结构真实。
- **必须保留**：正确指定、零边、过拟合和错设情景；恢复、误判控制、校准与弃权；失败不得由预测分数补偿。
- **验收测试**：读者在第 39 行之前即可说明检验“恢复什么、控制何种错误、按什么判定”；不得把“绝对”解释为模型无关或普遍有效。

### LA-R027-005（major）：RCT 投影分支的核心术语不具备跨学科可读性

- **精确位置**：第 32 行“冻结观测投影门”“投影可观测状态摘要”“随机化再分析”；第 41–42、54、60、67 行重复相近表达；第 242–252 行才说明映射和 estimand；第 314–320 行再次使用缩写式表达。
- **当前问题**：“冻结观测投影门”混合项目流程动作和数学名词；“投影可观测状态摘要”存在“投影是否可观测”与“对可观测变量作投影”两种读法；“有限随机化扰动”不是清楚的统计结果名称。
- **目标状态**：第一次提到该分支时直接说明输入、映射是否预先固定、检验目的以及输出是随机分组间的状态摘要差异。
- **要求的替换**：将首次出现的“冻结观测投影门”改为“**预先固定的观测变量投影及其忠实度检验**”；将“投影可观测状态摘要”统一为“**由实际观测变量投影得到的状态摘要**”；将结果表述为“**该实际访视状态摘要的随机化组间差异**”。后文可在定义后使用“观测投影”“投影状态摘要”。
- **必须保留**：映射在治疗组比较前固定、仅使用实际访视观测变量、忠实度须先通过、结论限于实际访视摘要、不延伸到完整潜在动力学或整个模型。
- **验收测试**：读者能从首次表述确定投影的输入是观测变量、映射何时固定、忠实度在哪里检验、RCT 输出比较什么；句法上不得再支持“摘要本身可观测”这一错误读法。

### LA-R027-006（major）：独立 SOFA 替代分支用英文压缩标签代替定义

- **精确位置**：第 32、41、67 行“death-ranked SOFA”；第 246 行“independent fallback”；第 254 行才完整说明死亡、在院 SOFA 和活着出院的排序；第 347、369、384、428 行又使用压缩标签。
- **当前问题**：“death-ranked SOFA”对中文跨学科读者不自然，也不能说明活着出院者的排序位置；“fallback”把重要的预设替代分析写成内部流程词。
- **目标状态**：首次出现时给出端点的三个排序层级，并为后续建立自然、稳定的中文短称。
- **要求的修改**：第 32 行首次出现时写为“**以死亡为最差层、访视时在院患者按 SOFA 从高到低排序、活着出院为最优层的独立次要临床状态再分析（下称‘独立的死亡分层 SOFA 再分析’）**”；第 246、254、347、369、384、428 行使用该中文短称或“预设替代分支”，不再使用裸露的 `death-ranked` 或 `fallback`。
- **必须保留**：死亡最差、活着出院最优、在院患者按 SOFA 排序、该分支独立于阶段 II、不得称为对阶段 II 的扰动或验证。
- **验收测试**：首次读到短称前，三个排序层级已全部出现；全文短称唯一，且任何位置都不会把替代分支误读为投影验证。

### LA-R027-007（major）：G1 在多次控制研究路径之前没有定义

- **精确位置**：第 84 行首次出现“G1 硬下限”；第 106、112、122、125 行继续使用 G1；第 131 行标题“Public ICU database roles and G1 audit”和第 138–155 行才展示审计内容，但没有给出 G1 的中文全称。
- **当前问题**：G1 决定网格、模块、样本支持和跨数据库路线，是核心验证标签；读者必须从后文表格反推其含义。
- **目标状态**：第 84 行首次出现时给出内容型中文名称，之后才使用 G1。
- **要求的替换**：第 84 行改为“**达到双数据库可观测性与数据支持审计（G1）的预设下限**”；第 131 行标题相应使用“**公共 ICU 数据库角色与双数据库可观测性及数据支持审计（G1）**”。
- **必须保留**：事件、转移、医院、锚点、接口、缺失和复杂度上限；G1 的失败会触发网格调整、备份或停止。
- **验收测试**：G1 的第一次出现同时包含中文全称；其后每个 G1 都能无歧义回指同一组审计内容。

### LA-R027-008（major）：R0/R1 的英文门名没有形成自足的科学名称

- **精确位置**：第 246 行“Gate R0 — trial semantics and common-anchor eligibility”；第 250 行“Gate R1 — measurement invariance, calibration and absolute projection fidelity”；第 317、383、405、435 行随后使用 R0/R1。
- **当前问题**：R0/R1 承担 RCT 分支能否成立的关键判断，但首次名称为英文项目标签，且 R1 中“absolute projection fidelity”延续第 4 条所述“绝对”歧义。
- **目标状态**：首次出现时用中文科学名称说明各自检验的对象，R0/R1 仅作为括号内短称。
- **要求的替换**：第 246 行标题使用“**试验语义与共同锚点合格性检验（R0）**”；第 250 行标题使用“**测量一致性、校准与投影忠实度检验（R1）**”。第 317 行以后首次回指时写“R0 试验语义与共同锚点检验”“R1 投影忠实度检验”。
- **必须保留**：R0 的授权、随机化、中心、访视语义和共同锚点条件；R1 的测量一致性、校准、忠实度和治疗标签遮蔽检查；任一失败的预设后果。
- **验收测试**：不查看第 246–250 行正文，仅看两个标题即可区分 R0 与 R1 检验什么；后文任何 R0/R1 都有唯一回指。

### LA-R027-009（major）：一句式完整摘要缺少可读的主干

- **精确位置**：One-sentence complete-Idea summary（第 32 行）。
- **当前问题**：单句同时承载数据来源、审计条件、四段病程、三种模型属性、阶段 I–II 证据、三个 RCT 前置条件、两个试验访视、投影通过分支、投影失败分支和五类禁止主张。分号不能充分分隔这些不同逻辑层级。
- **目标状态**：遵守 `One-sentence` 字段合同，用一个可独立理解的简洁句子按“研究对象—24 个月主验证路径—条件性试验角色”推进，不让读者先解析分支算法和限制清单。
- **要求的修改**：以一个主干句说明先审计两个公共 ICU 数据库，再构建覆盖全病程的候选动态系统表征并在 24 个月内完成模拟、开发和独立跨数据库检验，最后用条件从句说明只有前述证据和试验资料满足预设要求时才开展访视状态摘要的随机组间比较；把具体投影失败分支、排序算法、完整限制和失败后果保留在相应技术章节及第 14 节，不得用括号或连续分号重新塞回摘要。
- **必须保留**：两个须审计的公共 ICU 数据库、四段病程、知识约束与不确定性、24 个月主验证路径、阶段先后以及试验分析的条件性。具体 D7/D8、投影和独立替代分支仍须在正文原有功能位置完整保留。
- **验收测试**：摘要只有一个句号结句；目标读者可一次读出研究对象、主要验证路径和条件性试验角色；删除分支算法和完整限制后，正文对应位置仍保留这些科学内容。

### LA-R027-010（major）：关键判定标准被压缩成超长段落和表格单元

- **精确位置**：Gate R0 段（第 246 行）、Gate R1 段（第 250 行）、EXIT-SEP 与 XBJ-SCAP 的表格单元（第 258–259 行）以及“RCT 启动前还必须”段（第 335 行）。
- **当前问题**：这些位置都把来源核验、变量资格、数值阈值、缺失处理、分支后果和禁止操作放在同一段或单元内。虽然单项信息明确，但读者难以确认某个条件属于哪个判定层，也难以核对两项试验的共同规则和特异规则。
- **目标状态**：R0、R1、每项试验和启动前要求分别采用平行的项目列表；每一项只表达一个可核对条件，失败后果单列。
- **要求的修改**：第 246 行拆为“所需材料、语义核验、锚点资格、最少锚点数、失败后果”五组；第 250 行拆为“eICU 忠实度、锚点校准、遮蔽的试验支持度、失败后果”四组；第 258–259 行将共同缺失处理移到表前一次定义，仅在各试验单元保留差异；第 335 行改为按授权、访视语义、映射、估计规则和停止条件分列的编号清单。
- **必须保留**：现有每个数值阈值、数据来源限制、死亡/出院排序、缺失处理、中心处理、多重性、禁止填补的字段以及所有停止后果；不得借拆分删除条件。
- **验收测试**：逐项对照原第 246、250、258–259、335 行，所有条件都有唯一的新位置；每个项目只含一种核对操作；读者能独立勾选 R0、R1 和每项试验的通过条件。

### LA-R027-011（major）：跨学科正文大量使用未释义的英文简称和缩写

- **精确位置**：成功定义（第 92–100 行：`proper score`、`label-availability/as-of`、`test`、`zero-update`）；工作包与方法（第 106–112、177–189 行：`CIF`、`IPCW`、`AUPRC`、`adaptation/test`）；模拟恢复（第 214–226 行：`ARI`、`MAE`、`FDR`）；外部检验（第 228–240 行：`test-dominant component`、`full refit`、`transport updating`）；RCT 分支（第 246–261 行：`SVD`、`NMAE`、`MI`、`FWER`、`mITT`、`pooled effect`）；诊断和关键技术（第 263–277 行：`CRPS`、`ESS`、`MCSE`）。
- **当前问题**：这些术语分别属于统计、系统辨识、机器学习和试验分析；目标读者仅被假定“总体熟悉”多学科研究，不能假定掌握每个分支的全部简称。裸露英文还使同一动作出现中文和英文两套名称。
- **目标状态**：每个跨学科术语在正文第一次出现时给出中文名称和英文缩写，之后只使用一种稳定短称；普通动作优先直接用中文。
- **要求的修改**：至少采用以下对应关系并在首次出现时定义：界标时点（landmark）、按当时可用信息（as-of）、不作任何更新（zero update）、累积发生函数（CIF）、逆概率删失加权（IPCW）、精确率—召回率曲线下面积（AUPRC）、调整兰德指数（ARI）、平均绝对误差（MAE）、错误发现率（FDR）、奇异值分解（SVD）、归一化平均绝对误差（NMAE）、多重插补（MI）、族错误率（FWER）、改良意向治疗分析（mITT）、连续秩概率评分（CRPS）、有效样本量（ESS）和 Monte Carlo 标准误（MCSE）。`adaptation/test`、`fallback`、`full refit`、`pooled effect`、`prediction-only` 等普通流程词分别改为“适配区/最终测试区”“预设替代分支”“完整重拟合”“合并效应”“仅预测”。
- **必须保留**：数据库和试验正式名称、通用统计符号、需要与代码或注册表对应的缩写，以及每个术语的原有技术含义。
- **验收测试**：从第 27 行起逐个搜索上述英文简称；每个首次读者可见出现都同时给出中文全称，后续写法唯一；数据库名、试验名和数学符号不被误译。

### LA-R027-012（minor）：相近的否定性边界清单重复出现

- **精确位置**：第 32、42、73、252、320、370、385 和 410 行均列出“潜在动力学/转移边/中介/控制/数字孪生/整个模型”等相近的禁止解释。
- **当前问题**：边界本身必要，但近似逐项复述增加篇幅，并使不同位置真正特异的边界不突出。
- **修改方向**：保留每个论证位置所必需的科学边界，但统一为一个稳定的核心短句，再在各位置只补充该分支特有的限制；不要由语言评估决定删除哪个科学条件。
- **验收测试**：八个位置仍保留各自必要的结论边界，但相同的长清单不再逐字重复；每处新增部分都对应当地分支。

### LA-R027-013（minor）：少数句子带有内部评审或口语式表达

- **精确位置**：第 50 行“最近近邻使‘单个模块新颖’不可成立”；第 224 行“不可调阈重救”；第 416 行“最低角色为具名……”；第 424 行“高严重度未清零不打开 test”。
- **当前问题**：“使……不可成立”“重救”“最低角色”“打开 test”不符合自然、正式的中文科研计划语体。
- **建议替换**：分别改为“现有近邻研究表明，本项目不能把任何单项模块主张为新颖贡献”“不得事后调整阈值以使其通过”“项目至少需要具名的……负责人”“在所有高严重度泄漏问题解决前，不得访问最终测试集”。
- **验收测试**：这些句子不再依赖评审口令、口语动词或裸露英文即可表达相同的科学和程序约束。

## 术语问题汇总

| id | 术语或短语 | 定位 | 读者基线 | 问题 | 建议替换 | 首次定义 | 依据 | 验收测试 |
|---|---|---|---|---|---|---|---|---|
| LA-R027-001 | 条件性稀疏 RCT 次要再分析 | 第 27、31 行 | 不熟悉项目命名 | “稀疏”误附到 RCT | 基于稀疏访视数据、满足预设条件后开展的 RCT 次要再分析 | 标题直接展开 | 汉语修饰语附着 | “稀疏”只能指访视数据 |
| LA-R027-002 | 候选动态系统表征/候选全病程表示 | 第 32、39、52、60、95、370 行 | 多学科、非全领域专家 | 指称未定义且名称交替 | 统一为“候选动态系统表征” | 说明状态、转移、知识约束、不确定性及三类过程 | 核心研究对象必须首次可识别 | 读者可在摘要中复述其对象与作用 |
| LA-R027-003 | 阶段 I–III | 第 32、40、79–88 行 | 不熟悉项目阶段 | 编号承担论证但无内容定义 | 首次出现时写出每阶段内容和时间 | 阶段 I–II 为审计、恢复、开发及外部检验；阶段 III 为 24 个月后的条件性 RCT 再分析 | 项目阶段标签属于核心术语 | 每个编号可唯一回指内容与时序 |
| LA-R027-004 | 绝对恢复/假置信门 | 第 32、39、41、50、66、71、214–226 行 | 熟悉一般验证，不熟悉本项目标签 | 非标准且“绝对”易误读 | 模拟恢复与伪结构控制检验 | 指明预设阈值、恢复对象和误判控制 | 以科学指称替代项目口令 | 读者能说明恢复什么、控制什么 |
| LA-R027-005 | 冻结观测投影门/投影可观测摘要/随机化扰动 | 第 32、41–42、54、60、67、242–252、314–320 行 | 熟悉验证和 RCT，不熟悉项目映射 | 输入、动作和输出关系不清 | 预先固定的观测变量投影及忠实度检验；由实际观测变量投影得到的状态摘要；随机化组间差异 | 首次交代输入、冻结时点、检验和输出 | 复合术语需明确语义中心 | 不再支持“摘要本身可观测”的误读 |
| LA-R027-006 | death-ranked SOFA/fallback | 第 32、41、67、246、254、347、369、384、428 行 | 中文跨学科读者 | 英文压缩标签遗漏排序层级 | 独立的死亡分层 SOFA 再分析；预设替代分支 | 首次列出死亡、在院 SOFA、活着出院三层 | 端点必须首次可识别 | 三层排序在短称前完整出现 |
| LA-R027-007 | G1 | 第 84、106、112、122、125、131–155 行 | 不熟悉项目标签 | 决策标签无全称 | 双数据库可观测性与数据支持审计（G1） | 第 84 行 | 核心验证标签首次定义 | 后续 G1 唯一回指该审计 |
| LA-R027-008 | R0/R1 | 第 246、250、317、383、405、435 行 | 不熟悉项目标签 | 英文标签不自足 | 试验语义与共同锚点合格性检验（R0）；测量一致性、校准与投影忠实度检验（R1） | 各标题 | 核心验证标签首次定义 | 仅凭标题即可区分两项检验 |

## 语言修订优先级

1. **标题与中央研究对象**：先处理 LA-R027-001 和 LA-R027-002；否则读者在进入正文前已形成错误修饰关系或无法识别研究对象。
2. **证据阶段和验证标签**：处理 LA-R027-003、004、007、008，使每个阶段及检验在首次出现时以科学内容命名。
3. **RCT 分支术语**：处理 LA-R027-005 和 LA-R027-006，明确投影输入、检验、输出和独立 SOFA 替代分支。
4. **摘要与方法结构**：处理 LA-R027-009 和 LA-R027-010，重组一句式摘要并拆分判定清单，同时逐项保留条件。
5. **跨学科可访问性和语域**：处理 LA-R027-011 至 013，统一缩写、减少重复和替换内部流程表达。

## 复评状态

本次为基线评估，不是复评；未读取匿名问题清单、先前分数、先前决定、修订稿或差异记录。

## 局限与评估说明

- 仅根据指定 dossier 和读者交接文件评估语言；未读取其他科学材料，也未核验论据、阈值或研究设计是否正确。
- 未指定目标期刊，因此采用生物医学/临床研究与计算方法交叉领域的一般语言惯例。
- 本评估不判断科学有效性、论证质量、新颖性、影响力、可行性或期刊适配性。
- 术语判断以目标读者能否在首次出现时识别科学指称为准；没有因为某个复合短语未见于外部来源就认定其不标准。
- 机器前置元数据和固定字段名称未作为读者语言问题；仅评估这些工作标签是否泄漏到标题、摘要、正文和表格。

## 最终建议

当前版本需要较大语言修订。修订应优先让标题、中央研究对象、阶段名称和验证分支在首次出现时可以由跨学科读者直接解释，再处理句子拆分、缩写和重复。完成上述修改后，应由新的独立评估实例重新评估完整 dossier。
