---
review_id: language-assessment-r031
reviewer_skill: academic-language-assessor
reviewer_instance_id: fresh-language-r031
workflow_id: RID-SEPSIS-CSM-20260717-001
round_id: r031
input_artifact_ids:
  - idea-dossier-I01-001-v023
  - reader-handoff-forward-001
input_versions:
  - v023
  - v001
scope: complete_idea_dossier
dossier_ref:
  artifact_id: idea-dossier-I01-001-v023
  version: v023
  path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/revised/idea-dossier-v023.md
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
  - tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/revised/idea-dossier-v023.md
  - tests/idea-narrative-forward-0.9.0-preview.3/run-001/inputs/reader-handoff.yaml
  - "https://pmc.ncbi.nlm.nih.gov/articles/PMC5543372/"
  - "https://pmc.ncbi.nlm.nih.gov/articles/PMC10337434/"
isolation_mode: fresh_subagent
prior_scores_visible: false
source_edits_performed: false
decision: major_language_revision
findings:
  - finding_id: LANG-R031-01
    severity: major
    category: terminology_and_title_accessibility
    dossier_locator:
      - "Title, summary, audience, and positioning — title and One-sentence complete-Idea summary"
      - "Research question, objectives, and core hypothesis — Primary research question"
      - "Identity boundary — opening sentence"
    current_problem: >-
      核心研究对象“候选动态系统表征”在标题和一句话摘要中直接出现，但没有说明它具体指患者状态、状态转移及其观测关系的候选表示；“知识约束且量化不确定性的”和“知识约束、不确定性感知的”又以压缩复合修饰语包围该术语。重症医学或临床流行病学读者须到后文公式与状态定义处才能确定其指称，标题中的“全病程”也未立即展开为发病前在险时段、首次发病、发病后状态和结局。
    target_state: >-
      标题的语义中心直接命名被表征的对象，所有范围、证据状态与计划性修饰语均有唯一归属；一句话摘要首次使用短称前，以自然中文说明该对象包含患者状态、状态转移和观测关系，并明确“全病程”的四段范围。
    required_change_or_replacement: >-
      将标题中心改为直接描述性表达，例如“对脓毒症发病前至结局过程中的患者状态及其转移进行候选动态表征”，并保留冒号后“计划开展跨数据库检验”和满足条件后开展分试验 RCT 次要再分析的计划性限定。摘要首句先写“用随时间变化的患者状态、状态转移及其与观测数据的关系来描述……”，再引入“候选动态表征”短称；把“知识约束且量化不确定性的”改成主谓关系清楚的“受知识约束并显式量化不确定性的”。最终标题可采用等义措辞，但不得重新形成修饰对象不明的长名词串。
    content_to_preserve: >-
      保留候选而非既有成果的证据状态；保留发病前在险时段、首次发病、发病后状态和结局的范围；保留跨数据库检验、预设条件、稀疏实际访视、分试验次要再分析以及不主张因果或控制作用的边界。
    acceptance_test: >-
      一名仅具 reader_handoff 所列通识背景的读者，从标题和一句话摘要即可回答“被动态表示的对象是什么、覆盖哪四段、哪些工作只是计划、RCT 分析何时才发生”；逐一回读标题中的“候选”“跨数据库”“满足预设条件后”“基于稀疏访视数据”和“次要再分析”，每个修饰语只能附着于预期语义中心。
  - finding_id: LANG-R031-02
    severity: major
    category: first_use_core_term_accessibility
    dossier_locator:
      - "Structured abstract — Objective and hypothesis, Approach, Expected result"
      - "Research question, objectives, and core hypothesis — Core hypothesis"
      - "Conditional trial observation mapping and independent alternative analysis — opening paragraph through Estimand after a successful observation mapping"
    current_problem: >-
      “阶段 I–II”“阶段 III”先于阶段内容说明出现；“共同锚点”在核心假设中承担尺度固定和跨数据库可比性的关键作用，却未在首用处说明其为两个数据库中定义、单位和时间语义可比的生理测量；“观测变量投影”“投影状态摘要”在结构式摘要中承担阶段 III 的主要分支，却要到后文 SVD 公式后读者才能知道它是使用阶段 II 冻结权重、由试验实际访视变量计算的一维分数。项目短标签和数学化短称因此替代了首用定义。
    target_state: >-
      结构式摘要在每个项目阶段标签和核心技术短称第一次承担论证功能时，同句或紧邻句说明其科学内容与用途；后文才使用阶段号、锚点、投影和投影状态摘要等短称。
    required_change_or_replacement: >-
      在 Objective/Approach 首次出现阶段号时，用括注或同位语分别概括阶段 I（审计、标签、基线、模拟和开发验证）、阶段 II（冻结后的独立跨数据库检验）和阶段 III（条件性分试验 RCT 次要再分析）。将“共同锚点”首用改为“两个数据库中定义、单位和时间语义可比、用于固定状态尺度的生理测量（共同锚点）”。在 Approach 首次写“观测变量投影”时补充其为“使用阶段 II 冻结权重，由试验实际访视测量计算的一维分数”，并在首次写“投影状态摘要”时说明该词指含死亡、在院分数和活着出院层级的排序摘要；公式和阈值仍留在方法部分。
    content_to_preserve: >-
      保留三个阶段的现有顺序和 24 个月边界、共同锚点的既定技术用途、冻结权重、实际第 7 日或第 8 日访视、R0/R1 合格条件、死亡与活着出院层级，以及投影不合格时使用独立死亡分层 SOFA 分支的规则。
    acceptance_test: >-
      结构式摘要中每个阶段号第一次出现时均能映射到具体工作；“共同锚点”“观测变量投影”和“投影状态摘要”第一次出现后，重症医学、临床流行病学和系统辨识读者均无需跳到公式即可说出其指称和在决策分支中的作用；后文所有短称与该首用定义一致。
  - finding_id: LANG-R031-03
    severity: major
    category: readability_and_qualifier_stacking
    dossier_locator:
      - "Title, summary, audience, and positioning — One-sentence complete-Idea summary and Positioning and contribution frame"
      - "Structured abstract — Background and gap through Contribution and impact"
      - "Background, current state, gap, significance, and rationale — Rationale"
      - "Research question, objectives, and core hypothesis — Primary research question and Core hypothesis"
      - "Evidence chain: 条件性随机试验观测投影或独立临床状态再分析 — Method / analysis / processing"
      - "Limitations and boundary conditions — items 1, 2, 4, and 5"
    current_problem: >-
      关键入口和边界段落反复把研究对象、时间顺序、数据条件、验证状态、替代分支和解释限制压入同一句。完整正文中有 35 个非表格正文行超过 120 个字母或数字字符；典型句包括 240 字符的一句话摘要、含三个编号分支的主问题，以及同时列出映射、缺失、多重性和亚组规则的试验证据链方法句。多个“预设、冻结、独立、实际、条件性、试验特异、访视特异”限定语连续前置，使读者需要回读以确定条件作用于哪项分析。
    target_state: >-
      每个句子承担一个主要修辞动作；先陈述主干，再用后续短句说明条件、例外和解释边界。必要的科学条件全部保留，但相邻限定语按对象分组，替代分支采用平行句式或项目符号。
    required_change_or_replacement: >-
      将列出的入口段和限制段逐一拆分：一句话摘要至少按研究对象、阶段 I–II 工作和条件性阶段 III 三个逻辑单元重写；主问题保留总问句，但将三个判定分支改为语法平行的分项；Rationale 与 Core hypothesis 分开“方法为何需要”“什么结果算支持”“什么结果不改变主判定”；试验证据链方法句把映射合格分支、替代分支、缺失处理和多重性规则分句；每条 limitations 先给单一主题句，再列具体边界。不得删除任何必要条件，若条件是否可合并属于科学选择，则只调整句法位置而不代替作者作选择。
    content_to_preserve: >-
      保留所有数据来源、时间窗、阶段顺序、阈值、合格与不合格分支、独立外部检验要求、缺失和多重性处理以及因果、控制、临床推广和新颖性边界。
    acceptance_test: >-
      对每个列出的段落逐句标注主语、谓语、对象和条件后，不再出现一个条件可能同时修饰两个不同分析对象的情况；每句只需一次顺序阅读即可确定主干；所有原有科学条件均可在修订段中逐项找到，且没有因追求简短而被删除或弱化。
  - finding_id: LANG-R031-04
    severity: minor
    category: grammar_and_modifier_attachment
    dossier_locator:
      - "Title, summary, audience, and positioning — One-sentence complete-Idea summary: ‘知识约束且量化不确定性的’"
      - "Primary research question: ‘知识约束、不确定性感知的’"
      - "Observational estimand, anchoring, missingness, and support — paragraph beginning ‘非随机缺失的主要拟合’"
      - "Feasibility and resources — ‘动物实验、完成新的随机试验、因果机制和控制分析’"
      - "Working assumptions and specifications still to be frozen — ‘主要与备份数据库角色’"
    current_problem: >-
      局部并列成分词性不平行或修饰关系不完整：“知识约束”与“量化不确定性/不确定性感知”并列方式不自然；“显式测量过程的随机缺失或选择模型基线”不能唯一显示“显式”修饰测量过程还是模型；“动物实验、完成新的随机试验、因果机制和控制分析”混列名词与动宾短语；“主要与备份数据库角色”可误读为“主要角色”。
    target_state: >-
      并列项采用相同句法形式，修饰语紧邻其语义中心，模型之间的主次或并列关系由谓语明确表达。
    required_change_or_replacement: >-
      采用“受知识约束并显式量化不确定性的”；在缺失段先由作者确认现有模型关系，再写成“主要拟合显式建模测量过程，并以……为基线”或等义的无歧义结构；将资源段改为“不包括动物实验、新随机试验、因果机制研究或控制分析”；将表格短语改为“主要数据库与备份数据库的角色”。
    content_to_preserve: >-
      保留知识约束、不确定性量化、缺失模型的既定主次关系和全部研究范围排除项；不得借句法修订改变模型选择。
    acceptance_test: >-
      每个并列项词性和层级一致；“显式”及“基线”各自只有一个可能的修饰对象；资源段四个排除类别结构平行；“主要数据库”不再可能被读成“主要角色”。
  - finding_id: LANG-R031-05
    severity: minor
    category: chinese_english_terminology_consistency
    dossier_locator:
      - "Available local evidence for the two randomized trials — XBJ-SCAP paragraph"
      - "Common trial-analysis rules — XBJ-SCAP row"
      - "Observational estimand, anchoring, missingness, and support — missingness paragraph"
      - "Key techniques and implementation — item 6"
      - "Required analyses and evidence — item 5"
    current_problem: >-
      XBJ-SCAP 人群首次写成“操作性 sepsis-like 人群”，后文才写“操作性类脓毒症（sepsis-like）”；“模式混合（pattern-mixture）delta”没有给出 delta 的中文功能，后文又缩为“delta 与 tipping-point”。中文名称、英文名称与短称的定义顺序不一致，跨学科读者需自行匹配。
    target_state: >-
      首次出现时先给稳定中文名称，再给英文或符号短称；后文只使用已定义的同一中文短称或同一英文短称。
    required_change_or_replacement: >-
      在 XBJ-SCAP 段首次写“操作性类脓毒症（sepsis-like）人群”，后文保持一致；将首次缺失分析表述改为“模式混合偏移量（delta）”和“临界点分析（tipping-point analysis）”或领域内等义标准中文，并在后续三处统一用法。
    content_to_preserve: >-
      保留该人群的操作性而非确诊性质、各样本数、既定 delta 水平以及所有临界点分析规则。
    acceptance_test: >-
      每个英文短称在首次出现处都有唯一中文对应；全文搜索 sepsis-like、delta 和 tipping-point 时，不再出现先用英文后补中文或同一概念采用多个未定义形式的情况。
  - finding_id: LANG-R031-06
    severity: minor
    category: internal_workflow_language_leakage
    dossier_locator:
      - "References 22–25 — parenthetical notes and local material descriptions"
    current_problem: >-
      “本次修订未读取参与者级工作簿”等措辞把编辑过程和文件操作带入面向研究者的参考文献；本地路径式名称与“只读质量控制材料”也混合了证据类型说明和内部文件状态。它们不是机器 frontmatter，而是读者可见正文，因此造成语体和证据来源说明层级不一致。
    target_state: >-
      参考文献只保留可识别的材料名称、日期、证据类型及其学术用途或未纳入范围，以中性的来源说明表达，不叙述编辑实例做过或未做过什么。
    required_change_or_replacement: >-
      将“本次修订未读取参与者级工作簿”改为中性的范围说明，例如“参与者级工作簿未纳入本 dossier 的证据基础”，并把本地路径或“只读”状态移至非读者正文的来源记录；若路径必须保留，则与正式引文信息分栏或括注，不与证据判断混成一句。
    content_to_preserve: >-
      保留这些材料为项目本地衍生、并非原始 CRF/SAP/EDC 审计或独立同行评审材料的限定，以及参与者级工作簿未作为当前证据基础的事实。
    acceptance_test: >-
      References 22–25 不再出现“本次修订”“读取”“只读”等编辑或文件操作措辞；读者仍能明确识别材料类型、证据局限和是否纳入当前证据基础。
unresolved_issues:
  - LANG-R031-01
  - LANG-R031-02
  - LANG-R031-03
  - LANG-R031-04
  - LANG-R031-05
  - LANG-R031-06
---

# Language Assessment Report

Use logical artifact identity (`artifact_id`, `version`, and `path`) and
`files_read` for provenance. Do not add SHA, content-hash, or digest fields.
For `complete_idea_dossier`, the dossier reference and reader handoff are
required. A file-backed handoff must occur in `files_read`; an embedded handoff
uses `path: null` and is not added as a fictitious file or input artifact.
Validate this file with `scripts/validate_language_assessment.py` before handoff.

**Assessment ID**: language-assessment-r031  
**Target Language**: Chinese（zh-CN，含必要的英文缩写和方法名）  
**Discipline**: 重症医学与临床流行病学为主要应用语境，结合纵向统计、系统辨识、医学人工智能与工程方法  
**Target Journal**: 未指定  
**Scope**: complete_idea_dossier；从标题、一句话摘要和结构式摘要至正文表格、限制、停止条件与参考文献的全部读者可见内容  
**Date**: 2026-07-19

---

## Overall Language Readiness

**Level**: major_language_revision

**Recommendation**: revise_language

全文保持正式、审慎的学术语体，时态与计划性证据状态也基本稳定；但标题与结构式摘要中的核心对象、阶段标签和试验投影短称没有在首用处达到给定跨学科读者基线，触发术语可理解性硬门失败。关键入口、方法链和限制段还系统性使用长句与限定语堆叠。问题可以通过定向语言修订解决，尚不需要整篇专业代写或重构科学内容。

---

## Dimension Scores

| Dimension | Score (1–10) | Severity |
|-----------|-------------|----------|
| Grammar & Syntax | 7 | pass |
| Academic Register & Tone | 8 | pass |
| Terminology Consistency | 4 | fail |
| Tense & Voice Conventions | 9 | pass |
| Conciseness & Redundancy | 5 | borderline |
| Readability & Flow | 5 | borderline |

---

## Hard Gate Status

**Overall**: fail

| Gate | Status | Detail |
|------|--------|--------|
| Grammar error density | pass | 完整 dossier 中识别出 4 组明确但局部的句法、并列或修饰附着问题；正文约含 18,962 个汉字，未见接近每 500 词超过 3 个明确语法错误的密度。中文没有由本 rubric 规定的统一“词”切分，因此该计数仅用于排除高密度错误，不伪装成精确分词率。 |
| Academic register | pass | 正文各节均以正式学术语体为主；仅 References 22–25 出现局部编辑流程措辞，不构成两个以上章节的系统性口语或非学术语体。 |
| Terminology coherence | fail | 至少三组承担标题、核心假设或主要设计分支的术语在首用处对给定跨学科读者不可自足：“候选动态系统表征”、阶段 I–II/III 以及“观测变量投影/投影状态摘要”；“共同锚点”也延迟说明。问题是首用可理解性而非全文随机换名。 |
| Tense systematic violation | pass | 计划工作持续使用将来、条件或拟开展表达；已核验事实、现有证据与尚未生成结果在时态和证据状态上有稳定区分。 |

---

## Strengths

1. 语体总体克制、正式，避免了口语问答、感叹、夸张形容词和无条件推广措辞。
2. “拟开展、计划、条件满足时、尚未核验、尚未生成”等证据状态表达稳定，未把计划工作写成既有结果。
3. 多数缩写在首次出现处给出全称，例如 SOFA、IPCW、CIF、AUPRC、ESS、MCSE、ARI、MAE、FDR、SVD、NMAE、MI、FWER 和 mITT；数学符号在后文使用中也保持稳定。
4. 对计划性研究使用现在时、将来时和条件句，对已有数据库、文献与试验事实使用现在时或过去时，符合生物医学与计算方法交叉领域的常见写法。
5. 标题层级、表格和分项结构为长篇技术内容提供了明确导航；问题主要发生在句内负荷，而不是全文缺少结构。

---

## Specific Issues

### Chinese Academic Clarity (if applicable)

#### LANG-R031-01 — major：标题核心术语与复合修饰语

- **Location**: `Title, summary, audience, and positioning` 的标题与 `One-sentence complete-Idea summary`；`Primary research question`；`Identity boundary` 首句。
- **Original**: “脓毒症全病程的候选动态系统表征”；“知识约束且量化不确定性的候选动态系统表征”；“知识约束、不确定性感知的 ICU 患者候选动态系统表征”。
- **Issue**: “表征”的对象未在首用处说明，且名词化与形容词化修饰语堆叠。标题可被理解为“脓毒症自身的全病程表征”，而正文实际需要读者把范围展开为发病前在险时段、首次发病、发病后状态和结局，并把状态、转移和观测关系识别为被表示对象。
- **Deletion-or-revision direction**: 改用直接动词结构，明确“对哪些对象进行动态表征”；摘要随后才引入短称。删除不能增加范围或证据状态的压缩形容词，必要限定改为谓语。
- **Severity**: major。

#### LANG-R031-02 — major：项目阶段与试验投影术语延迟定义

- **Location**: `Structured abstract` 的 Objective/Approach/Expected result；`Core hypothesis`；`Conditional trial observation mapping and independent alternative analysis`。
- **Original**: “阶段 I–II”“阶段 III”“共同锚点”“观测变量投影”“投影状态摘要”。
- **Issue**: 这些短称在标题之后最重要的读者入口承担设计逻辑，却要到里程碑或公式段才获得指称。给定读者可具备一般验证和纵向数据知识，但不能假定熟悉项目阶段号或项目自定义映射短称。
- **Deletion-or-revision direction**: 首次出现先用一句自然中文说明阶段内容或术语功能，再括注短称；公式、输入清单和阈值可继续渐进披露，无须塞入摘要。
- **Severity**: major。

#### LANG-R031-03 — major：长句与限定语堆叠

- **Location**: 一句话摘要、Positioning、结构式摘要、Rationale、Primary research question、Core hypothesis、条件性试验证据链方法句，以及 Limitations items 1/2/4/5。
- **Original pattern**: 一个句子同时容纳研究对象、两个以上阶段、多个合格条件、替代分支和解释边界；反复连续前置“预设、冻结、独立、实际、条件性、试验特异、访视特异”等限定语。
- **Issue**: 本次诊断性行计数发现 35 个非表格正文行超过 120 个字母或数字字符。中文不能机械套用英文 35/40 词阈值，但这些关键句确实需要回读才能判断条件附着。篇章主题清楚，句内信息层级不清楚。
- **Deletion-or-revision direction**: 按“主干—条件—替代—解释边界”拆句；必要条件不得删除。仅在同一科学条件被近距离逐字重复且不改变限定范围时删除一次，其余通过分句和后置说明降低堆叠。
- **Severity**: major。

#### LANG-R031-04 — minor：局部并列与修饰附着

- **Location and direction**:
  - “知识约束且量化不确定性的”与“知识约束、不确定性感知的”改为平行谓语，如“受知识约束并显式量化不确定性的”。
  - “非随机缺失的主要拟合采用显式测量过程的随机缺失或选择模型基线”须先确认现有模型关系，再把“显式”“基线”的修饰中心写明；语言评估不代替作者选择模型。
  - “动物实验、完成新的随机试验、因果机制和控制分析”改为四个同层级名词短语。
  - “主要与备份数据库角色”改为“主要数据库与备份数据库的角色”。
- **Severity**: minor。

### Grammar & Syntax

LANG-R031-04 所列四组问题是全文主要的明确句法或搭配问题。其余长句主要属于可读性和修饰层级问题，并非普遍不合语法。未观察到主谓一致、时态构成或句子残缺等高密度错误。

### Academic Register & Tone

#### LANG-R031-06 — minor：内部编辑/文件操作语言进入参考文献

- **Location**: References 22–25。
- **Original**: “项目本地只读质量控制材料”“本次修订未读取参与者级工作簿”及与引文混写的本地路径。
- **Issue**: 这些词描述编辑实例和文件状态，而不是以研究者可理解的方式描述证据来源、局限和纳入范围。
- **Direction**: 用“材料类型—证据局限—是否纳入当前证据基础”的中性顺序表达；编辑过程与文件操作状态留在非读者来源记录。
- **Severity**: minor。

除该局部问题外，没有发现口语、直接称呼读者、修辞性问句、感叹、促销性词汇或两个以上章节的非正式语体。

### Terminology Consistency

| id | term_or_phrase | locator | reader_baseline | problem | recommended_replacement | first_use_definition | basis | acceptance_test |
|---|---|---|---|---|---|---|---|---|
| T-R031-01 | 候选动态系统表征 | 标题；一句话摘要；Primary research question | 跨重症医学、临床流行病学、纵向统计、系统辨识和医学 AI 的通识读者 | 使用一致但首用指称不自足；“全病程”和多个属性修饰语掩盖了被表示对象 | 对脓毒症发病前至结局过程中的患者状态及其转移进行候选动态表征（或等义直接表达） | “用随时间变化的患者状态、状态转移及其与观测数据的关系来描述发病前至结局过程，以下称候选动态表征” | reader_handoff；dossier 后文的 $X_t/Y_t/A_t/M_t$ 定义；代表性研究更直接使用 switching state-space model、physiological states/patient state representations 与 dynamic sepsis phenotypes/transition modeling，而非依赖未解释的总括标签：[Ghassemi et al.](https://pmc.ncbi.nlm.nih.gov/articles/PMC5543372/)、[Boussina et al.](https://pmc.ncbi.nlm.nih.gov/articles/PMC10337434/) | 标题修饰语附着唯一；摘要读完即可说出表示对象和四段范围 |
| T-R031-02 | 阶段 I–II；阶段 III | Structured abstract 的 Objective/Approach；后文 Twenty-four-month minimum | 同上；不得假定项目阶段词汇 | 首次出现早于阶段内容映射 | 首用时写明“开发与独立跨数据库检验阶段（阶段 I–II）”和“条件性分试验 RCT 次要再分析阶段（阶段 III）”，并在紧邻句补足各阶段内容 | 阶段 I=审计、标签、基线、模拟和开发验证；阶段 II=冻结后的独立跨数据库检验；阶段 III=24 个月后的条件性试验次要再分析 | reader_handoff 禁止假定项目内部词汇；dossier 在里程碑段才给出完整映射 | 阶段号首次出现处可独立解释，无需跳转到里程碑 |
| T-R031-03 | 共同锚点 | Core hypothesis；Observational estimand；R0 锚点资格 | 具备一般纵向数据知识，但不具备所有参与学科的细节 | 在核心假设中先用，后文才分散说明跨数据库、载荷、单位与时间语义 | “两个数据库中定义、单位和时间语义可比、用于固定状态尺度的生理测量（共同锚点）” | 使用推荐表达首用；后文再给每维数量、载荷和覆盖阈值 | dossier 的 G1 审计表、anchoring 段和 R0 资格段 | 首用后读者能回答什么可成为锚点及其用途；数值细节仍可后置 |
| T-R031-04 | 观测变量投影；投影状态摘要 | Structured abstract Approach/Expected result；Primary research question；Frozen deterministic observation mapping；Estimand | 具备一般验证和不确定性知识，不默认熟悉该项目映射 | 摘要先给短称，SVD 公式后才说明可计算对象；“连接实际访视”也未明确连接方式 | “使用阶段 II 冻结权重、由试验实际访视测量计算的一维分数（观测变量投影）”；“由死亡层、在院投影分数和活着出院层构成的排序摘要（投影状态摘要）” | 两个推荐解释分别置于 Approach 和首次 estimand 概述处 | dossier 后文 $P_{obs}$ 公式与死亡/在院/出院排序定义；术语为项目特定映射，宜采用直接描述而非另造短标签 | 摘要读者无需公式即可说明输入、权重来源、输出和排序层级 |
| T-R031-05 | 操作性 sepsis-like 人群 | Available local evidence；XBJ-SCAP analysis row | 中文主文读者 | 英文先出现，中文对应后出现 | 操作性类脓毒症（sepsis-like）人群 | 在首个 XBJ-SCAP 段采用推荐形式 | dossier 内部前后用法比较；该术语不是核心研究对象，不需外部标准性主张 | 全文首次中英文映射明确，后文形式一致 |
| T-R031-06 | pattern-mixture delta；tipping-point | Missingness paragraph；Key techniques item 6；Required analyses item 5 | 部分读者不具备缺失数据方法细节 | delta 未说明是偏移量，后文中英文短称交替 | 模式混合偏移量（delta）；临界点分析（tipping-point analysis） | 首次缺失分析段给出中文功能与英文短称 | dossier 内部定义顺序和 reader_handoff | 后文搜索三个位置只出现同一已定义形式 |

focused terminology review 没有把“找不到完整标题字符串”当作不标准证据。T-R031-01 的两篇代表性研究仅用于确认该领域存在更直接的模型、状态、表型和转移命名；本报告不据此断言总括短语在学界不存在，也不评价所提方法是否正确。

### Tense & Voice Conventions

none。计划性 Idea 使用将来、条件和拟开展表达是合适的，不应按已完成研究的 Methods/Results 过去时规则误判。表格和定义使用现在时，现有试验与文献事实使用现在或过去时，未见系统性冲突。

### Conciseness & Redundancy

主要问题为 LANG-R031-03。重复出现的“预设、冻结、独立、条件性”等词往往承担真实限定，因此本报告不判断应删除哪一项科学条件。语言修订应优先拆句、把限定语后置到其对象旁，并只删除同一局部语义单元中的近距离逐字重复。跨章节保留必要边界不因词汇重复而被判为科学冗余。

### Readability & Flow

主要问题同为 LANG-R031-03。篇章级顺序和标题导航清楚；阻碍集中在关键句内部，而不是段落缺少主题。修订后应优先复读标题、一句话摘要、结构式摘要、主问题、核心假设、试验映射和 limitations，因为这些位置决定跨学科读者是否能建立完整阅读路径。

---

## Language Revision Priorities

1. **Terminology accessibility**: 2 个 major findings — 先重写标题语义中心，并在结构式摘要为研究对象、阶段、共同锚点和试验投影建立首用定义。
2. **Readability & flow**: 1 个 major finding — 按主干、条件、替代分支和解释边界拆分关键长句，同时逐项保留科学限定。
3. **Grammar & modifier attachment**: 1 个 minor finding — 修复不平行并列和语义中心不明的局部短语。
4. **Chinese-English consistency**: 1 个 minor finding — 统一 sepsis-like、delta 和 tipping-point 的首次中英文映射与后续短称。
5. **Academic register**: 1 个 minor finding — 将 References 22–25 的编辑/文件操作措辞改为中性证据来源说明。

---

## Re-Assessment Status (if applicable)

不适用。本次为针对 v023 的全新完整 dossier 评估，没有读取匿名旧问题清单、旧分数、旧决定、旧版本、修订差异或其他 reviewer 报告。

| Check | Current assessment |
|--------|--------------------|
| Listed issues no longer present | 不适用；未提供且未读取旧问题清单 |
| Listed issues still present | 不适用；未进行旧问题核对 |
| New current-text issues | 6 个当前文本 findings：LANG-R031-01 至 LANG-R031-06 |

---

## Assessment Notes

- 本次只评估语言：语法、学术语体、术语首用与一致性、中英文对应、复合修饰语附着、内部流程语言泄漏、限定语堆叠、时态、简洁性和可读性。没有评价论证质量、科学有效性、新颖性、影响、可行性、期刊适配或统计设计优劣。
- 适用惯例为中文学术写作，并结合生物医学/临床研究、计算机科学/AI/工程和通用科学的交叉规范；未指定期刊，因此没有施加期刊特有格式。
- 完整读取了 v023 的所有读者可见部分，包括标题、一句话摘要、结构式摘要、背景、问题与假设、工作包、数据与材料、设计与方法、实现、证据链、所需分析、预期产物与证伪标准、贡献与近邻比较、标题支持表、可行性、风险、限制、停止条件、身份边界和参考文献。机器 frontmatter 仅作为脚手架读取，不计入语言评分；其中列出的旧产物路径没有被打开。
- reader_handoff 全文已读取，并据此采用跨重症医学、临床流行病学、纵向统计、系统辨识、医学 AI 与转化研究的通识基线；不假定项目内部词汇或每个参与学科的详细专长。
- 术语外部核对仅在普通阅读触发后进行，并限于 dossier 自身列出的两篇代表性原始研究。核对用于选择直接、可理解的命名方式，不用于评估科学主张。
- 未读取任何 sibling-platform skill、原始或旧版 dossier、既有 narrative/language 报告、repair plan、revision delta、preservation report、preflight、evaluator、portfolio、state/index 或父级推理；也未推断预期决定。
- 受评 dossier 与 reader handoff 均保持只读；本 reviewer 只创建本 Language Assessment Report。
