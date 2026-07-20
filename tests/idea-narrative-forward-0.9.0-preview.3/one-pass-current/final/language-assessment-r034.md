---
review_id: language-assessment-r034
reviewer_skill: academic-language-assessor
reviewer_instance_id: fresh-language-r034-one-pass-language-r034
workflow_id: RID-SEPSIS-CSM-20260717-001
round_id: editorial-readiness-r034
input_artifact_ids:
  - idea-dossier-I01-001-v024
  - reader-handoff-forward-001
input_versions:
  - v024
  - v001
scope: complete_idea_dossier
dossier_ref:
  artifact_id: idea-dossier-I01-001-v024
  version: v024
  path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/final/idea-dossier-v024.md
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
  - tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/final/idea-dossier-v024.md
  - tests/idea-narrative-forward-0.9.0-preview.3/run-001/inputs/reader-handoff.yaml
isolation_mode: fresh_subagent
prior_scores_visible: false
source_edits_performed: false
decision: major_language_revision
findings:
  - finding_id: LA-R034-001
    severity: major
    category: terminology_modifier_attachment
    dossier_locator:
      - "H1 title"
      - "Title, summary, audience, and positioning > Title"
    current_problem: "“条件性随机对照试验次要分析”把“条件性”置于“随机对照试验”之前，普通句法可将其读成“条件性的随机对照试验”，而不是“满足条件后才开展的次要分析”；该歧义位于标题中的核心证据层。"
    target_state: "条件明确修饰次要分析的开展时点，随机对照试验数据明确作为该分析的证据来源。"
    required_change_or_replacement: "将标题尾部改为“以及预设条件满足后基于随机对照试验数据开展的次要分析”，并同步标题字段；不要把“条件性”继续前置于“随机对照试验”。"
    content_to_preserve: "保留复杂系统模型构建、跨数据库验证、阶段 III 仅在预设条件满足后开展、且属于随机对照试验次要分析这四项既定含义。"
    acceptance_test: "H1 与 Title 字段完全一致；按普通中文句法重读时，“预设条件满足后”只修饰“开展次要分析”，“随机对照试验数据”只说明数据来源，不再存在“条件性试验”读法。"
  - finding_id: LA-R034-002
    severity: major
    category: terminology_standardness_and_first_use
    dossier_locator:
      - "Structured abstract > Approach, Expected result"
      - "Background, current state, gap, significance, and rationale > Rationale"
      - "Research design and methods > 模拟恢复与伪结构控制"
      - "Evidence chains > G1 支持、锚定识别与模拟恢复"
    current_problem: "“伪结构控制（检验）”在摘要和设计依据中被当作已知方法名使用，但首次出现没有说明它具体指空结构、零边和模型错设情景下对虚假边或错误结构接受的控制；目标读者无法仅凭该压缩标签确定其指代。"
    target_state: "首次出现即以描述性表达说明所检验的生成情景和所控制的错误，此后用语保持同一科学指代。"
    required_change_or_replacement: "将首次及核心叙述中的“伪结构控制检验”改为“空结构和模型错设情景下的虚假结构发现控制”，并在首次出现处简短说明其包括零边错误发现以及错误结构被高置信接受或未弃权的检验；技术表内保留现有数值标准。"
    content_to_preserve: "保留零边、独立状态、过拟合、遗漏状态、错误滞后或观测模型等既有情景，以及 FDR、伪边区间、错误接受和弃权的全部既定判据；不得新增方法或阈值。"
    acceptance_test: "摘要首次出现处能够让不熟悉项目标签的读者识别情景与错误对象；读者正文中不再单独出现未定义的“伪结构”标签；技术表中的原有情景和阈值完整保留。"
  - finding_id: LA-R034-003
    severity: major
    category: chinese_terminology_accessibility
    dossier_locator:
      - "Background, current state, gap, significance, and rationale > Significance, Rationale"
      - "Research design and methods > 以医院为主要单位的真正跨数据库验证"
      - "Key techniques and implementation > item 10"
      - "Evidence chains > 医院优先且未用于开发的跨数据库检验"
      - "Feasibility, resources, risks, alternatives, and stop conditions > L6"
      - "Contribution, innovation, impact, application, and closest-work comparison > closest-work table"
    current_problem: "“运输性”“运输失败”“运输更新”和“跨数据库运输”是未定义的直译式表达，并在核心意义、设计依据、结果解释及限制部分分别承担模型无更新外部表现、迁移失败和适配更新等不同功能；跨学科中文读者需要反推其含义。"
    target_state: "用自然中文区分“不作更新时的跨数据库可迁移性”与“为目标数据库进行的适配更新”，首次出现即给出操作性含义。"
    required_change_or_replacement: "核心性质统一写为“跨数据库可迁移性”，首次定义为“模型在未用于开发的数据库中不作更新时仍达到预设的任务表现、状态对齐和结构稳定标准”；“运输失败”改为“跨数据库可迁移性未达到预设标准”，“运输更新”改为“跨数据库适配更新”。文献或既有项目材料的正式题名可原样保留。"
    content_to_preserve: "保留不作任何更新为主要外部检验、仅校准和仅测量关系更新须分开报告、有限更新不能替代主要检验，以及数据库差异可以形成科学结果的全部边界。"
    acceptance_test: "核心正文首次使用“跨数据库可迁移性”时即有上述定义；后文明确区分无更新检验和适配更新；除正式参考文献或材料题名外，不再用单独的“运输/运输性”指代模型跨数据库表现。"
  - finding_id: LA-R034-004
    severity: minor
    category: chinese_academic_clarity
    dossier_locator:
      - "Structured abstract > Expected result"
      - "Expected outputs, falsification criteria, and interpretations > 计划产物 item 5"
    current_problem: "“访视状态排序摘要之随机组间差异”使用文言化结构助词“之”，与全文直接、现代的学术语体不一致。"
    target_state: "同一名词关系使用自然、直接的现代学术中文。"
    required_change_or_replacement: "改为“访视状态排序摘要的随机组间差异”。"
    content_to_preserve: "保留三层排序摘要、随机组间比较和试验分别报告的含义。"
    acceptance_test: "两处均改为“……摘要的随机组间差异”，且未改变统计比较对象。"
  - finding_id: LA-R034-005
    severity: minor
    category: academic_register
    dossier_locator:
      - "Research question, objectives, and core hypothesis > Objectives item 3"
      - "Research design and methods > 以医院为主要单位的真正跨数据库验证"
    current_problem: "“真正外部检验/真正跨数据库验证”带有未界定的评价色彩；同一段实际要表达的是医院层隔离、未用于开发且不作更新的外部检验。"
    target_state: "以可核验的设计属性命名该验证，不依赖“真正”作价值判断。"
    required_change_or_replacement: "按语境改为“独立外部检验”或“医院层隔离且未用于开发的跨数据库验证”，并保持与后文设计定义一致。"
    content_to_preserve: "保留医院优先拆分、最终测试区未参与开发以及不作更新为主要分析的设计属性。"
    acceptance_test: "两处不再出现“真正”；替代语直接陈述隔离、未用于开发或独立外部验证属性，且不扩大验证强度。"
  - finding_id: LA-R034-006
    severity: minor
    category: grammar_and_syntactic_completeness
    dossier_locator: "Research content and work packages > 阶段 II 合取成功定义 > item 5"
    current_problem: "“对齐后主要状态相关或一致性系数至少 0.70”缺少中心语“的相关系数”，使“相关”可被误读为形容词，两个并列指标的句法不对称。"
    target_state: "两个候选指标具有平行、完整的名词结构。"
    required_change_or_replacement: "改为“对齐后主要状态的相关系数或一致性系数至少为 0.70”。"
    content_to_preserve: "保留状态对齐指标、相关或一致性二选一以及 0.70 阈值。"
    acceptance_test: "句中明确出现“相关系数或一致性系数”，阈值仍为 0.70。"
unresolved_issues:
  - LA-R034-001
  - LA-R034-002
  - LA-R034-003
  - LA-R034-004
  - LA-R034-005
  - LA-R034-006
---

# Language Assessment Report

**Assessment ID**: lang-r034  
**Target Language**: Chinese  
**Discipline**: 重症医学、临床流行病学、纵向统计、系统辨识、医学人工智能与转化研究  
**Target Journal**: 未指定  
**Scope**: 完整 Idea dossier  
**Date**: 2026-07-19

---

## Overall Language Readiness

**Level**: major_language_revision

**Recommendation**: revise_language

当前稿的五段研究逻辑、计划时态和绝大多数技术定义均可读；但标题中的条件修饰关系，以及“伪结构控制”和“运输性”两组位于核心叙述链上的术语，仍要求跨学科读者依赖后文反推，触发术语硬门。所需修改均为限定范围的语言修订，不需要改变研究设计、证据强度或数值标准。

---

## Dimension Scores

| Dimension | Score (1–10) | Severity |
|-----------|-------------|----------|
| Grammar & Syntax | 8 | pass |
| Academic Register & Tone | 8 | pass |
| Terminology Consistency | 5 | fail |
| Tense & Voice Conventions | 9 | pass |
| Conciseness & Redundancy | 7 | pass |
| Readability & Flow | 7 | pass |

---

## Hard Gate Status

**Overall**: fail

| Gate | Status | Detail |
|------|--------|--------|
| Grammar error density | pass | 未见超过 3 个明确错误/500 中文词语当量；发现 1 处局部成分缺失 |
| Academic register | pass | 语体整体正式；“真正”两处带评价色彩，但未形成跨节系统性非正式语体 |
| Terminology coherence | fail | 0 个核心概念存在无理由的多名称混用，但 3 个标题或核心设计表达存在误导性修饰或读者不可及问题 |
| Tense systematic violation | pass | 计划性研究使用拟议或将来表达，既有证据与尚未生成结果的时态区分稳定 |

---

## Strengths

- 标题后的单句摘要首先交代研究对象、全病程边界、24 个月主验证和条件性试验层，未把计划结果写成已完成结果。
- Background、Current state、Gap、Significance 和 Rationale 各自采用清楚的主题句，读者无需先理解数值阈值即可识别研究问题与设计理由。
- Sepsis-3、SOFA、EHR、SVD、CIF、AUPRC、IPCW、MNAR、ESS、MI、FWER 和 CRPS 等缩写均在首次实质使用附近给出中文名称、英文名称或功能性说明。
- 阶段 I–III、G1、R0 和 R1 的标签均与具体研究内容相连，没有把插件状态或评审决策写入科研正文。
- 全文稳定区分拟生成产物、已核验数据库或文献事实、项目内衍生材料和尚未生成的研究结果。

---

## Specific Issues

### Chinese Academic Clarity

#### LA-R034-004 — minor

- **位置**：Structured abstract > Expected result；Expected outputs > 计划产物第 5 项。
- **原文**：“访视状态排序摘要之随机组间差异”。
- **问题**：“之”使局部语体文言化，与全文的现代学术中文不一致。
- **修订方向**：统一改为“访视状态排序摘要的随机组间差异”；保留统计比较对象不变。

#### LA-R034-006 — minor

- **位置**：Research content and work packages > 阶段 II 合取成功定义 > 第 5 项。
- **原文**：“对齐后主要状态相关或一致性系数至少 0.70”。
- **问题**：“相关”缺少“系数”中心语，并列结构不完整。
- **修订方向**：改为“对齐后主要状态的相关系数或一致性系数至少为 0.70”。

### Grammar & Syntax

除 LA-R034-006 外，未发现影响理解或达到硬门阈值的明确语法错误。复杂长句大多借助分号、冒号和表格维持层级，未形成普遍的句法失控。

### Academic Register & Tone

#### LA-R034-005 — minor

- **位置**：Objectives 第 3 项；Research design and methods 的跨数据库验证小节标题。
- **原文**：“真正外部检验”“真正跨数据库验证”。
- **问题**：“真正”是评价性强化词，不能直接说明验证为何独立。
- **修订方向**：改用“独立外部检验”或“医院层隔离且未用于开发的跨数据库验证”，把强度建立在可核验设计属性上。

其余语体正式、克制；未见口语、修辞问句、感叹或无证据的宣传性形容词。研究方案中的“锁定”“审计”和“停止”大多指预设分析、数据核验或停止范围，并非插件工作流词泄漏。

### Terminology Consistency

#### LA-R034-001 — major：标题修饰关系

“条件性随机对照试验次要分析”可把“条件性”错误附着到“随机对照试验”。应改为“预设条件满足后基于随机对照试验数据开展的次要分析”，使条件、数据来源和分析类型分别附着到正确语义中心。该修改不改变阶段 III 的条件性或次要分析属性。

#### LA-R034-002 — major：未定义的压缩方法标签

“伪结构控制检验”在摘要即承担核心方法功能，却到技术表才可推断其包括零边、模型错设、错误发现、错误接受和弃权。该表达未核验为目标读者共同标准术语；依据本稿自身的操作定义，直接写成“空结构和模型错设情景下的虚假结构发现控制”更准确。首次出现处应说明错误对象，后文保留现有数值判据。

#### LA-R034-003 — major：直译术语与功能混叠

“运输性”是未解释的直译式中文，并与“运输失败”“运输更新”“跨数据库运输”混用来表示无更新外部表现、失败结论和适配动作。应以“跨数据库可迁移性”命名核心性质，并首次定义其为“不作更新时仍达到预设任务表现、状态对齐与结构稳定标准”；适配动作另称“跨数据库适配更新”。这一区分来自当前设计已经写明的无更新与有限更新两层，不新增科学判断。

| id | term_or_phrase | locator | reader_baseline | problem | recommended_replacement | first_use_definition | basis | acceptance_test |
|---|---|---|---|---|---|---|---|---|
| LA-R034-001 | 条件性随机对照试验次要分析 | H1；Title 字段 | 跨学科 PI，可理解 RCT 和次要分析，但不应猜测修饰关系 | “条件性”可修饰错误的证据对象 | 预设条件满足后基于随机对照试验数据开展的次要分析 | 不需另造标签；短语自身说明条件、数据来源和分析类型 | 中文复合修饰语附着检查；单句摘要所述既定含义 | 普通句法下不存在“条件性试验”读法 |
| LA-R034-002 | 伪结构控制检验 | 摘要 Approach/Expected result；Rationale；方法与证据链 | 熟悉各自领域方法，但不熟悉项目压缩标签 | 无首次定义，且可能被误读为单一标准检验 | 空结构和模型错设情景下的虚假结构发现控制 | 包括零边错误发现及错误结构被高置信接受或未弃权的检验 | 当前稿“模拟恢复与伪结构控制”表已给出的操作对象；未将单一紧缩标签假定为跨学科标准 | 首次出现可识别情景与错误对象；原阈值全部保留 |
| LA-R034-003 | 运输性／运输失败／运输更新 | Significance、Rationale、外部验证方法、证据链、L6、最接近工作表 | 临床、流行病学、系统辨识与 AI 混合读者 | 直译不自然，且把性质、失败和适配动作压在同一词根下 | 跨数据库可迁移性／未达到可迁移性标准／跨数据库适配更新 | 模型在未用于开发的数据库中不作更新时仍达到预设任务表现、状态对齐和结构稳定标准 | 当前稿对不作更新、有限更新及其判据的明确定义；采用透明描述性中文而非未核验压缩标签 | 无更新性质与适配动作词形分开；正式题名外不再出现单独“运输” |

### Tense & Voice Conventions

none。当前为计划性 Idea，不是已完成实证研究；“拟”“计划”“将”“尚未生成”与已发表文献或已核验资源的陈述相互一致，没有把未来分析写成完成结果。

### Conciseness & Redundancy

未发现需要语言评估单独判为阻断的重复。摘要和方法部分存在高信息密度，但大多对应不同研究功能。限制集中在权威限制节；其他位置出现的条件通常直接决定当地任务或分析分支，本报告不替叙事评估决定其跨节保留位置。

### Readability & Flow

五段核心逻辑连续，技术细节总体后置。当前主要阅读负担来自 LA-R034-002 和 LA-R034-003 的压缩术语，而非段落顺序。标题修饰歧义修复后，单句摘要可继续承担跨学科入口，不要求仅因长度而拆成多句。

---

## Language Revision Priorities

1. **标题术语与修饰关系**：1 个 major — 让条件修饰分析开展时点，让随机对照试验数据明确成为证据来源。
2. **核心方法术语**：2 个 major — 用现有操作定义替换“伪结构控制”和“运输性”压缩标签，并在首次出现处给出自然中文定义。
3. **局部语体与句法**：3 个 minor — 删除“真正”的评价强化、把“之”改为“的”、补齐“相关系数”的中心语。

---

## Re-Assessment Status

本次为 Idea 工作流中的全新完整稿评估，未接收匿名问题清单，也未读取旧稿、旧报告、修订记录或既往决定。

| Check | Current assessment |
|--------|--------------------|
| Listed issues no longer present | 不适用；未提供既往问题清单 |
| Listed issues still present | 不适用；未提供既往问题清单 |
| New current-text issues | LA-R034-001 至 LA-R034-006 |

---

## Assessment Notes

- 评估基线采用 reader handoff：读者具备重症研究、纵向数据、验证和观察性/干预性证据的一般知识，但不假定熟悉项目内部词汇或每个参与学科的专门术语。
- 聚焦术语核验仅覆盖普通阅读触发的标题修饰关系、“伪结构控制”和“运输性”三组表达；未建立完整术语表，也未把某一完整复合短语未出现在文献中当作不标准的证据。
- 推荐替换均从当前 dossier 已明示的科学指代和设计层级提取，不评价方法正确性、创新性、影响力或可行性，不调整任何 claim strength、阈值或分析分支。
- 未读取任何旧 dossier、语言或叙事报告、repair plan、revision delta、内容保真报告、preflight、evaluator、状态、索引、portfolio 或 Hermes 同名技能。
