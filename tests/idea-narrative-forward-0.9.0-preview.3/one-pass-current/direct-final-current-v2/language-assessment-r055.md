---
review_id: language-assessment-r055
reviewer_skill: academic-language-assessor
reviewer_instance_id: fresh-language-v035-r055
workflow_id: RID-SEPSIS-CSM-20260717-001
round_id: r055
input_artifact_ids:
  - idea-dossier-I01-001-v035
  - reader-handoff-forward-001
input_versions:
  - v035
  - v001
scope: complete_idea_dossier
dossier_ref:
  artifact_id: idea-dossier-I01-001-v035
  version: v035
  path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v2/idea-dossier-v035.md
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
  - tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v2/idea-dossier-v035.md
  - tests/idea-narrative-forward-0.9.0-preview.3/run-001/inputs/reader-handoff.yaml
isolation_mode: fresh_subagent
prior_scores_visible: false
source_edits_performed: false
decision: major_language_revision
findings:
  - finding_id: L055-T01
    severity: major
    category: terminology_first_use
    dossier_locator: "Structured abstract—Objective and hypothesis（‘双库可观测性审计’）；Research content and work packages—月 4–6 判定时点及‘公共重症监护数据库角色与 G1 审计’"
    current_problem: >-
      “双库可观测性审计”在首次出现时没有说明审计对象；后文实际枚举的是队列、事件与转移、医院、跨院患者、变量语义与单位、时间戳、接口、缺失和样本支持。对包含系统辨识研究者的读者群，“可观测性”还可能被读成形式化系统可观测性，因而该核心阶段标签的词面范围与后文操作范围不一致。
    target_state: >-
      首次出现即用直接描述说明审计检查哪些数据条件、这些条件决定什么，随后才使用 G1 短标签；不得让读者依靠后文表格反推“可观测性”的项目内含义。
    required_change_or_replacement: >-
      在首次出现处直接说明：先检查两库能否构造所需队列、事件和转移，变量的语义、单位与时间是否可比，以及医院、患者和生理测量是否提供足够统计支持；如需保留短标签，再注明“下文简称 G1 审计”。后续可保留 G1，但不要以未解释的“可观测性”单独承载上述多项功能。
    content_to_preserve: >-
      G1 的时间位置、全部审计字段、硬性支持规则、模型复杂度上限及不满足时的替代或停止条件。
    acceptance_test: >-
      跨学科读者在 Structured abstract 首次遇到该阶段时即可说出主要审计对象及其决策功能；全篇检查 G1、双库审计和可观测性审计的用法，确保都回指同一已定义操作，且不暗示已完成形式化系统可观测性证明。
  - finding_id: L055-T02
    severity: major
    category: terminology_first_use
    dossier_locator: "Structured abstract—Objective and hypothesis（‘共同锚点’、‘锚定限制’）；Research design and methods—‘观察性目标、锚定与拒绝解释’；条件性试验观测端点—R0"
    current_problem: >-
      “共同锚点”“生理锚点”“锚定限制”和“锚点预测”承担模型尺度、方向、跨库可比性和 RCT 映射等核心功能，但摘要首次使用时未说明“锚点”是何种观测量，也未说明它与普通共同变量、共同模块或结局标签的区别。定义性信息分散到数据库审计、潜在状态和 R0 段落之后。
    target_state: >-
      在首次使用“锚点”之前，以可由临床、流行病学和统计读者共同理解的直接描述交代其观测性质、跨库要求及在潜在状态尺度/方向中的作用；后续各复合形式保持同一语义核心。
    required_change_or_replacement: >-
      在首次使用处增加直接定义，说明这些量是跨数据库具有可审计语义、单位和可用时间的实测生理变量，并用于固定潜在状态的尺度或方向；同时明确普通共同变量、共同模块、标签和 RCT 共同集与这些生理变量的包含或排除关系。只有完成该说明后才使用“共同锚点”等短式。
    content_to_preserve: >-
      每个维度至少两个锚点、载荷和符号约束、覆盖阈值、共同集 C_r 的排除规则、单位与时间审计，以及 RCT 映射资格。
    acceptance_test: >-
      从摘要到 R0 做全篇一致性检查；读者无需跳到公式段即可识别锚点的观测对象和功能，且“共同锚点”“生理锚点”“锚点预测”不再与普通共同变量、标签或结局混淆。
  - finding_id: L055-T03
    severity: major
    category: terminology_definition
    dossier_locator: "Research content and work packages—月 4–6 判定时点与 G1 审计表（‘状态维度 K’、‘状态模式数’）；Research design and methods—‘观察性目标、锚定与拒绝解释’"
    current_problem: >-
      文中并列规定“状态维度 K≤4”和“状态模式数≤3”，但没有定义两者的对象或关系；读者无法安全判断“模式”是离散状态、切换体制、聚类类别，还是每个潜在维度的取值。该未定义差异直接进入复杂度上限、模拟与停止条件。
    target_state: >-
      首次并列出现时明确两个数量各自计数什么、彼此如何区别，并让后续表格与方法段只沿用该定义。
    required_change_or_replacement: >-
      不替作者选择模型含义；请用直接描述补足定义。若“模式”意指离散切换体制，应明确写出它是与连续潜在状态维度 K 不同的离散体制数；若意指其他对象，则据实命名该对象，并同步修改所有“状态模式数”用法。
    content_to_preserve: >-
      K≤4、另一数量≤3 的既定上限、G1 触发的降维规则、候选模型比较和模拟判定逻辑。
    acceptance_test: >-
      任一目标读者都能分别回答 K 和另一数量计数什么；全篇“状态”“状态维度”“状态模式”和“多状态”的每次使用均可归入已定义对象，不需根据公式或背景知识猜测。
  - finding_id: L055-T04
    severity: major
    category: terminology_concordance
    dossier_locator: "标题与 One-sentence summary（‘随机试验次要分析’）；Structured abstract—Background and gap（‘RCT 表型—治疗二次分析’）；Objectives—目标 4；条件性试验观测端点首段（‘次要或探索性分析’）；References 之外的全文相关用法"
    current_problem: >-
      同一阶段 III 工作在“次要分析”“二次分析”“次要或探索性分析”之间切换。这些词分别可能指次要终点分析、既有数据的再次分析和探索性分析；差异出现在标题、摘要和核心设计中，读者无法确认它描述的是数据来源、终点层级还是推断地位。
    target_state: >-
      先用直接文字分别说明分析使用既有 RCT 个体数据、端点是否在原试验后提出、以及其确认性或探索性地位，再为同一分析性质保留一个稳定名称。
    required_change_or_replacement: >-
      在标题或摘要首次出现处采用不依赖术语猜测的描述，例如明确为“基于既有随机试验个体数据、在原结果后提出的条件性分析”；随后依据作者确认的统计地位，分别使用“二次分析”“次要终点分析”或“探索性分析”，不得把三者当作可互换短语。
    content_to_preserve: >-
      阶段 III 的条件性、两项试验分开、端点在原试验结果之后提出、R0/R1 分支、原 28 日终点独立复现及因果解释边界。
    acceptance_test: >-
      标题、摘要、目标 4、条件性试验观测端点、证据链、计划输出和限制段完成全篇 concordance；每个名称都唯一对应数据再利用、终点层级或探索性地位中的一个概念，不再交叉替代。
  - finding_id: L055-R01
    severity: major
    category: readability_qualifier_stacking
    dossier_locator: "One-sentence complete-Idea summary；Primary research question；两项主要临床任务表—‘临床事件时刻’；R0、预先固定的确定性映射与 R1；两项试验表；RCT 证据链；待确认的工作假设第 4 项；研究身份保持不变段"
    current_problem: >-
      多处把对象、时间、资格条件、例外分支、阈值、禁止事项和解释边界压入一个长句或单个表格单元。限定语层层前置，主语和主要动作被延迟；读者必须反复回读才能判断哪一条件修饰哪一分析、数据集或端点。
    target_state: >-
      每个句群先陈述一个主要对象和动作，再按时间、资格、分析分支和边界分句；所有限定仍保留，但修饰关系在句法上唯一。
    required_change_or_replacement: >-
      将所列位置按“对象/目的—进入条件—执行动作—失败分支—解释边界”拆分；表格单元可使用编号短句。避免连续使用多个“且”“并”“若……则……否则……”把两个以上决策层嵌套在同一句中。
    content_to_preserve: >-
      所有时间窗、样本集、阈值、数据隔离规则、R0/R1 条件、两种端点选择规则、停止条件和不作因果解释的限定。
    acceptance_test: >-
      所列每个句群均能在首次阅读中识别唯一主语、主要动作和条件层级；任一限定都能明确归属到对应数据、模型、端点或结论，且拆句前后的数值和分支逐项一致。
  - finding_id: L055-T05
    severity: minor
    category: terminology_concordance
    dossier_locator: "Structured abstract（‘能否被找回’、‘状态恢复’）；互斥的发病后状态与事件系统（‘生理恢复’）；预设模拟与半合成数据判定标准；证伪标准"
    current_problem: >-
      “恢复/找回”同时表示患者生理改善和模拟中对潜在状态、转移概率或参数的统计重建；摘要中的“被找回”又偏口语。复合词虽提供部分区分，但跨段阅读时仍会把临床状态与模型性能混在同一词根下。
    target_state: >-
      “生理恢复”只指患者状态；模拟性能按对象使用“状态重建准确度”“转移概率估计误差”或文中已给出的具体统计量，并保持摘要与判定表一致。
    required_change_or_replacement: >-
      删除“被找回”这一口语化表达；对模拟中的状态、转移和参数分别使用直接描述，不以一个“恢复”词概括不同评估量。保留临床状态名称“生理恢复”。
    content_to_preserve: >-
      调整兰德指数、典型相关、平均绝对误差、覆盖率、错误边和错设情景等全部判定量及患者生理恢复的操作定义。
    acceptance_test: >-
      全篇检索“恢复”和“找回”；每个保留实例都能唯一判定为临床状态或已明确对象的模拟评估，不再由上下文猜测。
  - finding_id: L055-C01
    severity: minor
    category: chinese_academic_clarity
    dossier_locator: "Structured abstract—Contribution and impact（‘随机分配对该端点的有限扰动’）；观察性目标、锚定与拒绝解释（‘相关关系只描述为数据支持较低且依赖照护政策’）；医院优先的跨数据库验证首句（‘在任何按结局选择之前’）"
    current_problem: >-
      三处分别出现不自然隐喻、谓语搭配不完整和介词结构生硬。“随机分配”不自然地“扰动”端点；“相关关系描述为数据支持较低”缺少清晰的报告动作；“任何按结局选择”使条件范围难以立即解析。
    target_state: >-
      使用文中已有的直接科学动作词：比较组间差异、说明证据支持程度与照护政策依赖性、以及说明医院划分发生在任何基于结局的选择之前。
    required_change_or_replacement: >-
      将“有限扰动”改为对端点组间差异的直接表述；把“相关关系只描述为……”改为“仅报告该关联，并明确其……限制”的句式；把医院划分的先后关系改成主谓明确的时间句。
    content_to_preserve: >-
      随机化只支持端点组间差异的边界、治疗重叠不足时的降级解释、医院划分不得使用结局的隔离规则。
    acceptance_test: >-
      三处均不再依赖工程隐喻或省略谓语，且与解释矩阵、限制段和医院隔离规则中的直接表述一致。
  - finding_id: L055-C02
    severity: minor
    category: conciseness_redundancy
    dossier_locator: "Structured abstract—Contribution and impact；Core hypothesis and non-hypotheses；Expected outputs—证伪标准与解释矩阵；Contribution and closest-work comparison；限制与边界条件；研究身份保持不变段"
    current_problem: >-
      “不构成因果网络/机制/控制/数字孪生/临床工具”等否定边界及外部验证失败不能由适配后结果补偿的限定，以近同词串多次出现；反复堆列同一组否定名词增加篇幅并掩盖各节真正新增的信息。
    target_state: >-
      保留每一处承担的科学边界，但在同一局部段落中删除近同重复，避免一再复制整组否定名词；不得由语言编辑自行决定哪些跨节边界在论证上可删除。
    required_change_or_replacement: >-
      做一次全篇重复语句 concordance，优先压缩同段、相邻表格或同一节内的近逐字重复；跨节是否保留由叙事评估决定。每次保留时只列与该节输出直接相关的边界。
    content_to_preserve: >-
      观察性设计、外部验证和条件性 RCT 各自的因果与模型解释边界，全部失败分支，以及限制章节中的权威限制清单。
    acceptance_test: >-
      全篇逐项核对边界含义均在，但同一局部不再重复相同否定词串；未通过语言编辑删除科学上不同的条件，也未增加跨节指针代替必要说明。
  - finding_id: L055-M01
    severity: suggestion
    category: chinese_english_structural_drift
    dossier_locator: "读者可见的二级标题（如 ‘Structured abstract’、‘Research design and methods’、‘Evidence chains’）及各 Evidence chain 中的 ‘Input/Method / analysis / processing/Output/Supports’ 标签"
    current_problem: >-
      正文为中文，但大量结构标题和证据链字段保留英文；对 zh-CN 目标文本形成持续的界面层语言切换。若这些名称是固定 schema 标签，则它们不属于作者可自由改写的术语错误。
    target_state: >-
      读者可见层的结构语言与中文正文一致，同时保留机器或 schema 所需的固定标识。
    required_change_or_replacement: >-
      若标题可编辑，统一为标准中文学术标题；若属于合同固定标签，不要求作者改名，而应由模板或呈现层提供相邻中文显示名。
    content_to_preserve: >-
      原有章节拓扑、证据链四个字段的机器语义及任何合同固定标识。
    acceptance_test: >-
      zh-CN 阅读界面不要求读者在每个章节层级切换语言；固定字段仍可被现有 schema 和验证器识别。
unresolved_issues:
  - L055-T01
  - L055-T02
  - L055-T03
  - L055-T04
  - L055-R01
  - L055-T05
  - L055-C01
  - L055-C02
---

# Language Assessment Report

**Assessment ID**: language-assessment-r055  
**Target Language**: Chinese（zh-CN）  
**Discipline**: 重症医学与临床流行病学为主，结合纵向统计、系统辨识和医学人工智能  
**Target Journal**: 未指定  
**Scope**: complete_idea_dossier  
**Date**: 2026-07-19

---

## Overall Language Readiness

**Level**: major_language_revision

**Recommendation**: revise_language

全文语法和时态总体稳定，但核心方法标签的首次定义、分析地位术语的一致性及长句中的限定语附着尚不足以支持跨学科读者安全、顺畅地理解。术语硬门槛未通过，因此当前不宜判为可提交。

---

## Dimension Scores

| Dimension | Score (1–10) | Severity |
|-----------|-------------|----------|
| Grammar & Syntax | 8 | pass |
| Academic Register & Tone | 6 | borderline |
| Terminology Consistency | 4 | fail |
| Tense & Voice Conventions | 9 | pass |
| Conciseness & Redundancy | 4 | fail |
| Readability & Flow | 4 | fail |

---

## Hard Gate Status

**Overall**: fail

| Gate | Status | Detail |
|------|--------|--------|
| Grammar error density | pass | 全篇通读约为不超过 1 个明确语法或搭配错误/500 个中文词语单位，未达到 >3/500 的失败阈值 |
| Academic register | pass | 正式学术语体占主导；项目流程词和少数工程隐喻影响自然度，但未形成两个章节中的系统性口语语体 |
| Terminology coherence | fail | 4 个核心概念存在首次不可辨、潜在误读或名称漂移：双库可观测性审计、锚点体系、状态维度与状态模式、RCT 分析地位 |
| Tense systematic violation | pass | 作为研究构想与计划，未来或计划性表达与尚未生成结果的状态一致；未发现把计划工作系统写成已完成结果的时态错误 |

---

## Strengths

- 全文持续区分计划、尚未核验和已核验状态，时态与研究构想的前瞻性质一致。
- RCT、SOFA、IPCW、MNAR、ESS、ARI、FDR、CRPS 和 SVD 均在首次正文使用处给出英文全称或可辨定义，缩写格式总体一致。
- 数据可用时刻、临床事件时刻、观察性关系、随机化组间差异和因果解释边界使用明确，未出现宣传性或“首次”措辞。
- 多数数值、单位、时间窗和阈值的中文与英文符号混排一致，表格中的比较关系可定位。
- “投影观测摘要端点”和“独立 SOFA 临床状态端点”虽为项目特定名称，但摘要和方法段均给出直接的对象、排序及适用条件，没有仅以缩写替代解释。

---

## Specific Issues

### Chinese Academic Clarity

- **L055-C01（minor）**：见 Structured abstract—Contribution and impact、观察性目标段和医院优先验证首句。“有限扰动”“相关关系只描述为……”及“在任何按结局选择之前”分别造成不自然隐喻、搭配不完整和修饰范围迟滞。改用“组间差异”“报告该关联并说明限制”和主谓明确的先后句；不改变随机化、支持度和数据隔离边界。
- **L055-R01（major）**：摘要研究问题、标签定义、R0/R1、两项试验表、RCT 证据链和工作假设中持续出现限定堆叠。按对象、条件、动作、失败分支和解释边界拆句，并逐项核对阈值与分支。
- **L055-M01（suggestion）**：中文正文中持续穿插英文结构标题与 Evidence chain 字段。若为固定 schema，不作为作者语言错误；建议由模板或呈现层提供中文显示名。

### Grammar & Syntax

未见达到硬门槛的系统语法错误。局部主要是搭配和修饰范围问题，已列入 L055-C01 与 L055-R01；不应把长句本身机械计为语法错误。

### Academic Register & Tone

- 全文保持正式、审慎的科研计划语体，无口语对话、修辞问句、感叹或宣传性形容。
- “被找回”“拒绝解释”“有限扰动”“资格”“路线”等词在方法判断中带有项目流程或工程操作色彩。L055-T05 与 L055-C01 要求优先改为具体的科学对象、操作或报告后果；“资格”和“路线”只有在确指进入条件或计划分支时保留。

### Terminology Consistency

| id | term_or_phrase | locator | reader_baseline | problem | recommended_replacement | first_use_definition | basis | acceptance_test |
|---|---|---|---|---|---|---|---|---|
| L055-T01 | 双库可观测性审计 / G1 审计 | Structured abstract；月 4–6 判定点；G1 审计节 | 熟悉验证与纵向临床数据，但不假定熟悉项目内流程词 | 词面可能指形式化系统可观测性，后文实际覆盖队列、变量、接口、时间和统计支持 | 先直接列明审计对象与决策功能，再保留 G1 短标签 | 说明检查队列/事件可构造性、变量语义与时间可比性及医院/患者/测量支持 | dossier 内部标签与后文枚举范围不一致；无需外部证据 | 全篇 G1 用法均回指同一直接定义，不暗示形式化证明 |
| L055-T02 | 共同锚点 / 生理锚点 / 锚定限制 / 锚点预测 | Structured abstract；G1；观察性目标；R0 | 不假定每位读者具备潜变量锚定专长 | 首次使用时不知锚点是什么观测量，也不知与共同变量、标签和结局的边界 | 先描述为具有跨库可审计语义、单位和时间、用于固定潜在状态尺度或方向的实测生理变量 | 同句给出观测性质、跨库条件和模型功能 | dossier 后文载荷、单位、时间和排除规则已足以直接界定 | 摘要即可识别对象与功能；各复合形式语义一致 |
| L055-T03 | 状态维度 K / 状态模式数 | 月 4–6 判定点；G1 表；观察性目标段 | 熟悉纵向模型，但不假定详细系统辨识模型 | 两个数量并列受限却未说明各自计数对象 | 依据作者意图直接命名第二个对象；若是离散体制，明确与连续维度 K 区分 | 首次并列时定义两者及关系 | dossier 内部缺少定义，无法由直接文字安全判断 | 任一读者可分别说明两数量计数什么；全篇不混用 |
| L055-T04 | 次要分析 / 二次分析 / 次要或探索性分析 | 标题、摘要、目标 4、条件性试验观测端点及后续相关段落 | 熟悉观察性与干预证据的一般区别 | 三个词可能分别表示端点层级、既有数据再分析和推断地位，却被交替用于同一阶段 | 先直接说明数据再利用、端点提出时间和确认/探索地位，再各用一个稳定名称 | 标题或摘要首次出现即交代三项属性 | dossier 内部用法已显示名称漂移；无需外部术语检索 | 标题至限制段完成全篇 concordance，每个名称只承担一个概念 |
| L055-T05 | 恢复 / 找回 | Structured abstract；生理恢复状态；模拟判定表；证伪标准 | 可理解临床恢复和模型评估，但不应依赖上下文拆义 | 同一词根同时指患者改善与统计重建，“找回”偏口语 | 患者保留“生理恢复”；模拟按对象写状态重建、转移概率误差或具体指标 | 摘要首次提及模拟目标时直接区分 | dossier 自身已在判定表区分统计量 | 全篇检索后每一实例可唯一归类 |

未进行外部术语检索：上述结论均来自 dossier 自身的首次使用、后文直接定义和全篇用法对照，外部证据不会改变当前“先定义对象和功能”的修订要求。未生成术语登记表或证据包。

### Tense & Voice Conventions

计划性陈述稳定使用“计划”“须”“将”“若……则……”和未来条件式；已核验文献或数据状态使用现在时/完成状态，尚未生成结果明确标为“未核验”或“尚未生成”。未发现系统性时态或语态违规。

### Conciseness & Redundancy

- **L055-C02（minor）**：因果、机制、控制、数字孪生、临床工具等否定边界以近同词串在摘要、假设、解释矩阵、贡献、限制和末段反复出现。语言层面应先压缩同段或同节的近逐字重复；跨节保留位置由叙事评估决定，语言评估不删除科学上不同的限定。
- “预先确定”“隔离外部测试”“不进行任何参数更新”等重复多为设计约束，不宜仅因高频而删除；应在拆句后检查每次是否有明确修饰对象。

### Readability & Flow

- **L055-R01（major）** 是主要可读性障碍。尤其 R0/R1 和两项试验表同时承载时间、语义、缺失、分层、阈值和停止分支，句法层级多于读者一次可稳定保持的层级。
- 全篇结构顺序可识别，表格也提供了定位；问题主要位于句内和表格单元内，而非章节无序。

---

## Language Revision Priorities

1. **Terminology first use and concordance**：4 个阻断性概念组——先补直接定义，再对标题、摘要、目标、方法、证据链和限制做全篇一致性检查。
2. **Readability and qualifier attachment**：1 个系统性长句问题——按对象、条件、动作、失败分支和解释边界拆句，并逐项回核数值与分支。
3. **Chinese academic clarity**：3 处局部不自然表达，加上“恢复/找回”的跨域词义重叠——用具体科学动作和对象替代隐喻或流程词。
4. **Concision**：压缩同段、同节的近逐字边界清单；不由语言编辑决定跨节科学限定的去留。
5. **Structural language display**：若英文标题为固定 schema，由模板或呈现层提供中文显示名。

---

## Re-Assessment Status (if applicable)

不适用。本次为 Idea dossier 的全新独立完整评估，未读取匿名问题清单、先前分数、先前决定、先前版本或修订差异。

---

## Assessment Notes

- 只评估语言，不判断研究论证、方法有效性、创新性、可行性、期刊适配或科学结论质量。
- 研究者 handoff 指定 zh-CN，读者可假定熟悉重症研究、纵向临床数据、验证、不确定性及观察性与干预性证据的一般区别，但不得假定熟悉项目内部流程词、新造标签或所有参与学科的细节。
- 采用生物医学/临床研究为主、计算机科学与系统辨识为辅的语言惯例；本稿是计划性 Idea dossier，不以已完成研究的 Methods/Results 过去时要求误判其未来式。
- 完成了非持久化的 whole-dossier concordance：比较了中央研究对象、主要任务、跨数据库条件、两种 RCT 分析分支和核心方法标签的全部读者可见名称；未生成术语登记表。
- 未进行 focused verification 或互联网检索。所有术语问题都可由 dossier 的直接描述、首次出现位置和后文定义安全判断；当前修订不依赖外部证据结论。
- 未读取原稿、repair plan、revision delta、preflight、content-preservation、先前语言/叙事/评估、workflow state、portfolio 或 Hermes sibling source；未编辑冻结 dossier。
