---
review_id: language-assessment-I01-001-r092
reviewer_skill: academic-language-assessor
reviewer_instance_id: fresh-language-assessor-r092
workflow_id: RID-SEPSIS-CSM-20260717-001
round_id: r092
input_artifact_ids:
  - idea-dossier-I01-001-v048
input_versions:
  - v048
scope: complete_idea_dossier
dossier_ref:
  artifact_id: idea-dossier-I01-001-v048
  version: v048
  path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v14/idea-dossier-v048.md
reader_handoff:
  artifact_id: embedded-reader-handoff
  version: embedded
  path: null
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
  - research-skills-openai/skills/academic-language-assessor/scripts/scan_idea_language_candidates.py
  - research-skills-openai/skills/academic-language-assessor/scripts/validate_language_assessment.py
  - tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v14/idea-dossier-v048.md
isolation_mode: fresh_subagent
prior_scores_visible: false
source_edits_performed: false
decision: major_language_revision
findings:
  - finding_id: LA-R092-001
    severity: major
    finding_kind: terminology
    category: 核心术语的首次定义与全篇一致性
    dossier_locator:
      - Structured abstract，Objective and hypothesis（第45行）
      - Title, summary, audience, and positioning（第40行）
      - Research question, objectives, and core hypothesis（第87行）
      - Research content and work packages（第99、109、121、126行）
      - "Evidence chain: 数据支持、锚定与已知生成机制恢复（第313行）"
    current_problem: >-
      核心假设使用“至多一个受限复杂候选可恢复规定的不变量”，但“受限复杂候选”没有明确绑定到前文的“候选动态复杂系统模型”，“规定的不变量”也未定义。后文实际列举的是状态占用、转移概率、共同生理指标预测以及关系的符号或滞后；跨学科读者在摘要处可能把“不变量”理解为数学意义上的系统不变量，也无法判断三种候选称谓是否指同一模型。
    target_state: >-
      在摘要首次陈述核心假设时，直接说明候选模型受到哪些约束、须恢复哪些预先规定的状态、转移和结构量，并只在完成这一定义后使用一个稳定的简称；不同于复杂候选的简单后备模型应继续明确区分。
    required_change_or_replacement: >-
      将第45行相应分句改为直接描述，例如“至多保留一个满足预设复杂度与锚定约束的候选模型；该模型须在已知生成机制的模拟中恢复预先规定的状态、转移和结构量，并在外部数据库中达到规定的校准、状态对齐和结构稳定标准”。在第40行给出模型组成后明确一个简称，随后逐处核对并统一“复杂候选”“受限复杂候选”等称谓；不要用另一个未定义的短标签替换。
    content_to_preserve: >-
      保留知识约束、显式表示不确定性、最多准入一个较复杂候选、简单模型后备路线、已知生成机制下的恢复检验、外部数据库检验以及不作因果解释的边界。
    acceptance_test: >-
      第45行不再出现未定义的“规定的不变量”或身份不明的“受限复杂候选”；第40行已把唯一简称绑定到模型的科学组成；对第33、37、38、40、44–46、62、66、76、81、87、99、101、106、109、121、126、242、272、293、307、313、360、368、378、384、405、415、427、432、443和447行进行全篇核对后，同一候选模型只保留已定义的全称与一个简称，简单后备模型仍与之明确区分。
    term_or_phrase: 受限复杂候选／规定的不变量
    recommended_form_or_plain_description: >-
      满足预设复杂度与锚定约束的候选模型，以及该模型须恢复的预先规定状态、转移和结构量
    evidence_basis: >-
      dossier 第40行给出模型组成，第87、224–230和236–244行给出实际待恢复或检验的量；全文没有给“规定的不变量”下定义。该内部对照已能证实摘要短语与后文科学对象不对应，因此采用直接描述，无需另立或外部核验一个新短标签。
    first_use_definition: >-
      本研究的候选模型联合表示患者生理状态及其转移，并区分治疗行动与测量过程；较复杂候选只有在预设约束下恢复规定的状态、转移和结构量后才可进入外部检验。
    competing_forms_and_locators:
      - “脓毒症全病程动态复杂系统模型／动态复杂系统模型”：第33、37、38行
      - “候选动态复杂系统模型”：第40、44、45、62、76、81、106、272、307、384、405行
      - “复杂候选（含切换或非线性复杂候选）”：第46、66、87、99、109、121、126、242、293、360、368、378、427、432、443行
      - “受限复杂候选”：第45、313行
      - “跨数据库动态复杂系统模型”：第101行
  - finding_id: LA-R092-002
    severity: minor
    finding_kind: terminology
    category: 外部评价与模型更新术语
    dossier_locator:
      - Structured abstract，Contribution and impact（第48行）
      - 二十四个月最低交付与时间节点（第101行）
      - 合取式最低成功定义（第112行）
      - 工作包与最低执行顺序（第123行）
      - 医院优先的跨数据库评估（第258行）
      - "Evidence chain: 按医院隔离的跨数据库评估（第326行）"
      - Required analyses and evidence（第347行）
      - 证伪标准与结果解释矩阵（第370、379–380行）
      - Title and positioning claim-support table（第416行）
      - 限制与边界条件（第442行）
    current_problem: >-
      “未更新外部性能评估”在摘要中先于定义出现，字面上容易被理解为“评估没有更新”，而非“模型参数不在测试数据上更新”；“未更新评估”进一步省略了被保持不变的对象。“观测层更新”到第258行才说明为保持状态与转移模型不变的局部更新，临床与流行病学读者此前难以确定其操作范围。
    target_state: >-
      第一次出现时直接说明是否允许在测试数据或适配区重新估计哪些参数，并为“不经模型更新的外部性能评估”和“仅更新观测方程”各保留一个含义稳定的称谓。
    required_change_or_replacement: >-
      在第48行使用“不在外部测试数据上重新拟合或调整参数的性能评估”这一直述；在第101行首次出现后续更新类别时写明“仅用适配区重新校准结局，或仅重新估计观测方程而保持状态与转移模型不变”。定义后可分别简称为“不经模型更新的外部评估”和“观测方程更新”，并在其余所列位置统一。
    content_to_preserve: >-
      保留测试数据不参与模型选择、适配区可用于预先规定的重新校准或局部更新、全模型再开发单独报告，以及任何更新后改善不能替代原模型外部表现失败的限制。
    acceptance_test: >-
      第48行已明确“不更新”的对象是模型参数；第101行已明确两类适配区更新各自改变和保持不变的部分；第112、123、258、326、347、370、379–380、416和442行只使用定义后的稳定称谓，且全文核对没有将不经更新的评估、重新校准、观测方程更新和全模型再开发混为一类。
    term_or_phrase: 未更新外部性能评估／观测层更新
    recommended_form_or_plain_description: >-
      不在外部测试数据上重新拟合或调整模型参数的性能评估；仅用适配区重新估计观测方程且保持状态与转移模型不变的更新
    evidence_basis: >-
      dossier 第258行已经给出两项操作的实际含义，足以作为全篇用语的依据；建议采用这些直接描述，而不是引入新的紧缩术语。
    first_use_definition: >-
      不经模型更新的外部评估是指固定模型后不在测试数据上重新拟合或调整任何参数；观测方程更新仅使用适配区重新估计观测方程，状态与转移模型保持不变。
    competing_forms_and_locators:
      - “未更新外部性能评估”：第48、101、112、258、326、370、379、442行
      - “未更新评估”：第123、347、380、416行
      - “观测层更新”：第101、123、258、326、347、380、442行
      - “基于适配区的更新／适配区更新”：第258、326、380、442行
  - finding_id: LA-R092-003
    severity: minor
    finding_kind: language
    category: 读者入口句的简洁性与局部可读性
    dossier_locator: Title, summary, audience, and positioning，One-sentence complete-Idea summary（第38行）
    current_problem: >-
      单句同时承载研究问题、四类病程对象、知识与数据来源、模拟和外部评价、阶段 I–II 范围、三类产物及阶段 III 条件，且以“模型贯通病程”这一拟人化搭配连接多个长名词组。核心问题与最低交付需要回读才能分辨。
    target_state: >-
      在保持单句合同的前提下，以一个清晰主句呈现核心问题，用不超过两个附加分句交代阶段 I–II 的验证路径和阶段 III 的条件性位置。
    required_change_or_replacement: >-
      保留“研究什么—如何在阶段 I–II 检验—何时才开展试验次要分析”三层信息，删减来源和产物清单中可在后文获得的细目；把“贯通”改为“统一表示”或同等直接的科学动词，并避免连续使用“以……完成……从而形成……并……”的链式结构。修改后仍须恰为一个句子。
    content_to_preserve: >-
      保留发病前、首次发病、发病后互斥状态和结局的全病程范围，24个月阶段 I–II，知识与公共重症监护数据约束，已知生成机制模拟，隔离的跨数据库评价，以及阶段 III 仅在主体研究达标后开展。
    acceptance_test: >-
      第38行仍为一个句子，只有一个明确主句和至多两个附加分句；读者无需回读即可分别指出核心研究问题、阶段 I–II 的主要验证路径和阶段 III 的启动条件；“贯通”不再承担未说明的技术含义。
  - finding_id: LA-R092-004
    severity: minor
    finding_kind: terminology
    category: 条件性试验分析的自然中文表达
    dossier_locator:
      - Title, summary, audience, and positioning（第38行）
      - Structured abstract，Approach（第46行）
      - 主要研究问题与研究目标（第76、83行）
      - Research content and work packages（第93、124、126行）
      - Research design and methods（第260行）
      - "Evidence chain: 条件性分试验次要结果（第330、335行）"
      - Required analyses and evidence（第350行）
    current_problem: >-
      “分试验次要分析／用途／结果”是紧缩且不自然的中文构词，既可能表示“把一次试验拆分后分析”，也可能表示“分别分析不同试验”。只有到第262行“且两项试验彼此独立”后，预期含义才明确。
    target_state: >-
      每次出现都直接表达“两项试验分别分析且不合并”，无需读者依赖项目内短标签推断。
    required_change_or_replacement: >-
      按句法位置将“分试验次要分析”改为“分别针对每项试验开展的次要分析”或“按试验分别开展的次要分析”；相应将“分试验次要用途／结果”改为“各试验分别承担的次要用途／分别报告的次要结果”。
    content_to_preserve: >-
      保留阶段 II 达标后的条件性、两个随机试验互相独立、方案分别预先规定、结果不合并以及不参与阶段 II 判定。
    acceptance_test: >-
      第38、46、76、83、93、124、126、260、330、335和350行均不再出现“分试验”这一压缩构词；每处都能独立说明各试验分别分析，全文没有把两项试验写成合并分析。
    term_or_phrase: 分试验次要分析
    recommended_form_or_plain_description: 按试验分别开展的次要分析
    evidence_basis: >-
      dossier 第262、274–279和332–335行明确规定两项试验彼此独立、分别执行且结果不合并；推荐形式直接复述这一既定关系，不依赖外部术语判断。
    first_use_definition: >-
      主体研究达到预设标准后，才分别针对每项试验按各自预先规定的方案开展次要分析，两项试验结果不合并。
    competing_forms_and_locators:
      - “分试验次要分析”：第38、46、76、93、124、126、260、350行
      - “分试验次要用途”：第83、335行
      - “分试验次要结果”：第330行
  - finding_id: LA-R092-005
    severity: minor
    finding_kind: language
    category: 学术语体中的宣传性措辞
    dossier_locator:
      - Title, summary, audience, and positioning，One-sentence complete-Idea summary（第38行）
      - Background, current state, gap, significance, and rationale，Significance（第66行）
      - Expected outputs, falsification criteria, and interpretations，计划产物（第363行）
    current_problem: >-
      “高水平论文”“高水平论文素材”评价的是预期声望或质量，而不是可检验的科学产物；该修饰语在结果尚未生成的计划文本中带有宣传色彩，并重复三次。
    target_state: >-
      以中性的产物名称和可审计属性描述论文交付，不预判发表层级或质量。
    required_change_or_replacement: >-
      删除“高水平”，按语境保留“论文”“论文素材”或改为“面向同行评议的论文稿件”；不要增加期刊层级、影响力或类似未经证实的评价词。
    content_to_preserve: >-
      保留形成论文、可审计科学证据和可复用研究资源这一计划性产物目标。
    acceptance_test: >-
      第38、66和363行不再使用“高水平”或同类声望性修饰语，且仍明确论文与研究资源是预期产物而非既得成果。
  - finding_id: LA-R092-006
    severity: minor
    finding_kind: terminology
    category: 失败结果的可读命名
    dossier_locator:
      - Structured abstract，Expected result（第47行）
      - 二十四个月最低交付与时间节点（第101行）
      - 工作包与最低执行顺序（第123行）
      - Key techniques and implementation（第298行）
      - Expected outputs，计划产物（第361行）
      - Contribution，贡献与证据层级（第396行）
      - Title and positioning claim-support table（第416行）
    current_problem: >-
      “失败图”没有说明是模型失配诊断图、未达标指标图、失败情景汇总，还是流程图。该短标签反复作为交付物出现，却没有首次定义，跨学科读者无法据此判断图中应呈现的科学对象。
    target_state: >-
      用直接描述指出图表呈现哪些未达到预设标准的情景、指标及后果；若需要简称，只在定义后使用一个不会与流程故障混淆的名称。
    required_change_or_replacement: >-
      第47行首次出现时改为“展示模型在预设模拟或外部评价中未达到标准的情景、指标及后果的图表”；后文可统一简写为“未达标结果图表”，并按具体语境保留模拟失配、外部适用性或其他不同对象。
    content_to_preserve: >-
      保留成功与失败结果均保存、失败不被预测表现掩盖、未达标结果用于审计与限制解释的要求。
    acceptance_test: >-
      第47行已经说明图表的对象与用途；第101、123、298、361、396和416行使用同一已定义称谓或更具体的对象名称，读者可以从每处文字判断图表记录的是哪类未达标结果。
    term_or_phrase: 失败图
    recommended_form_or_plain_description: 展示未达到预设标准的情景、指标及其分析后果的图表
    evidence_basis: >-
      dossier 第298行同时提到“模型未满足项”，第313、327、348、360–370和378–384行说明失败结果及其解释后果；这些内容足以支持直接描述，但全文没有定义“失败图”这一短标签。
    first_use_definition: >-
      未达标结果图表汇总模型在预设模拟或外部评价中未达到的标准、对应情景及其对后续解释的限制。
    competing_forms_and_locators: []
unresolved_issues:
  - LA-R092-001
  - LA-R092-002
  - LA-R092-003
  - LA-R092-004
  - LA-R092-005
  - LA-R092-006
---

# Language Assessment Report

**Assessment ID**: language-assessment-I01-001-r092  
**Target Language**: Chinese  
**Discipline**: 重症医学、临床流行病学、纵向统计、系统辨识、医学人工智能与转化研究的跨学科交叉  
**Target Journal**: 未指定  
**Scope**: 完整 Idea dossier；读者信息来自 dossier 内嵌说明  
**Date**: 2026-07-20

---

## Overall Language Readiness

**Level**: major_language_revision

**Recommendation**: revise_language

文本整体语法可靠、学术语体稳定，计划性时态也使用得当；当前主要障碍不是基础中文能力，而是摘要中的核心模型与恢复对象被压缩为未定义短语，外部评价类别又晚于首次使用才解释。完成有界的术语统一与入口句精简后，无需全篇专业重写。

---

## Dimension Scores

| Dimension | Score (1–10) | Severity |
|-----------|-------------|----------|
| Grammar & Syntax | 9 | pass |
| Academic Register & Tone | 8 | pass |
| Terminology Consistency | 5 | fail |
| Tense & Voice Conventions | 9 | pass |
| Conciseness & Redundancy | 6 | borderline |
| Readability & Flow | 6 | borderline |

---

## Hard Gate Status

**Overall**: fail

| Gate | Status | Detail |
|------|--------|--------|
| Grammar error density | pass | 全篇未发现明确、无争议的语法错误；远低于每 500 词 3 个的阈值 |
| Academic register | pass | 无任何章节以口语为主；仅有 3 处宣传性修饰语，见 LA-R092-005 |
| Terminology coherence | fail | 一处位于核心假设的短语“受限复杂候选可恢复规定的不变量”在首次出现时既未绑定模型身份，也未说明恢复对象；后文对象清单与“不变量”的通常读法不一致，触发完整 Idea 对核心术语可理解性的扩展规则 |
| Tense systematic violation | pass | 研究计划、预期产物、条件性后续分析和既有证据的时间状态区分一致；未把计划工作系统性写成已完成结果 |

---

## Strengths

- 计划性、条件性和既有证据的时间状态区分稳定，尤其在结构式摘要、方法与限制部分没有把预期结果写成已获结果。
- 生理测量、治疗行动、测量过程、标签与基线协变量的中文命名在定义后保持稳定，数学符号集中在方法部分并与中文解释相邻。
- 因果、预测、关联与外部适用性的限定语总体准确，未使用口语、感叹或直接面向读者的表达。
- 数据库、试验、临床量表和统计指标的英文缩写大多在首次正文使用时给出中文名称或具有明确领域身份；版本号和稳定标识符没有被误当作正文术语。

---

## Specific Issues

### Chinese Academic Clarity

- **LA-R092-003（minor）**：第38行的一句式摘要在一个句子内堆叠问题、材料、阶段、产物与条件，且“模型贯通病程”不够直接。应在保持一句话的前提下压缩为核心问题、阶段 I–II 检验路径和阶段 III 条件三层。
- **LA-R092-005（minor）**：第38、66、363行的“高水平论文（素材）”属于预判质量的宣传性修饰；改为中性的“论文（素材）”或“面向同行评议的论文稿件”。
- **LA-R092-004（minor）**：“分试验”容易被理解为拆分单项试验；应直接写成“按试验分别开展”。

### Grammar & Syntax

未发现需要单列的语法或句法错误。当前长句问题属于信息密度与局部可读性，而非缺少主句、搭配错误或成分残缺。

### Academic Register & Tone

- **LA-R092-005** 是唯一可执行的语体问题。其余正文保持正式、克制的计划语言，没有系统性口语表达。

### Terminology Consistency

| id | term_or_phrase | locator | reader_effect | action_in_frontmatter |
|---|---|---|---|---|
| LA-R092-001 | 受限复杂候选／规定的不变量 | 第40、45、87、99、109、121、126、313行及全篇列明位置 | 摘要中无法确定模型身份和待恢复的科学对象，并可能误读为数学不变量 | yes |
| LA-R092-002 | 未更新外部性能评估／观测层更新 | 第48、101、112、123、258、326、347、370、379–380、416、442行 | 无法在首次出现时判断更新的是评估、模型参数还是观测方程 | yes |
| LA-R092-004 | 分试验次要分析 | 第38、46、76、83、93、124、126、260、330、335、350行 | 可能被理解为拆分一项试验，而不是两项试验分别分析 | yes |
| LA-R092-006 | 失败图 | 第47、101、123、298、361、396、416行 | 无法判断交付图表呈现的失配、未达标指标或分析后果 | yes |

### Tense & Voice Conventions

无可执行问题。作为研究构想，全文以“拟、计划、须、若……则……”表述未来工作，以“已有、尚未、未提供”区分当前证据；这种用法符合临床研究与计算方法交叉领域的计划文本惯例。

### Conciseness & Redundancy

- **LA-R092-003**：一句式摘要的来源与产物清单可以删减，详细内容在后续章节均有展开。
- **LA-R092-005**：“高水平”重复三次且不增加科学信息，应删除。
- 全篇多次出现条件和限制，但多数承担局部判定功能；本评估没有决定哪些科学边界应跨章节删除或移动。

### Readability & Flow

- **LA-R092-001** 和 **LA-R092-002** 是最影响跨学科读者局部阅读的两处：科学操作在后文写得明确，但入口处先出现紧缩标签。
- **LA-R092-003** 影响第一轮阅读的主线提取。除此之外，各段和表格的主题基本集中，未发现需要语言评估介入的章节顺序或论证结构问题。

---

## Language Revision Priorities

1. **核心术语**：1 项 major、3 项 minor — 先在摘要直接说明模型、恢复对象和不经模型更新的外部评价，再统一全篇简称。
2. **读者入口可读性**：1 项 minor — 在一句话合同内压缩摘要，保留主问题、主体研究和条件性后续分析。
3. **学术语体**：1 项 minor — 删除“高水平”等预判质量的修饰语。

---

## Re-Assessment Status (if applicable)

不适用。本次是对 v048 完整 dossier 的全新独立评估，没有接收或查看先前问题清单、分数、决定、旧版本或修订差异。

---

## Assessment Notes

- 读者基线按 dossier 第39行处理：具备重症医学、临床流行病学、纵向统计、系统辨识、医学人工智能或转化研究中的至少一项专业背景，但不能假设同时熟悉所有子领域和项目内简称。
- 只读扫描共返回 12 个读者入口候选、65 个混合语言／版本／内部标记候选和 139 个条件或后果陈述候选；三组均逐项检查，没有抽样或在发现首个问题后停止。入口与后果组中有读者依据的问题合并进入 LA-R092-001、002、003、004、005、006；其余项目分别属于清楚的普通条件句、已定义的科学术语、标准数据库／试验标识、数学符号、版本号、文献标识符或文件名，不单列为问题。
- 对 LA-R092-001、002、004和006执行了聚焦术语核验，包括首次使用、复合标题修饰关系、自由正文与固定结构的区分，以及相关称谓的全篇一致性。现有 dossier 后文已经给出预期科学对象或操作，因此替换建议采用这些直接描述；未开展外部检索，也未建立术语表或证据包。
- 固定的 research-idea.v3 标题、结构式摘要字段、证据链字段和 Claim-Support 表头仅作为定位结构，不参与评分，也没有被要求翻译或改名。
- 本评估只判断语言、术语和局部可读性；没有判断论证结构、研究价值、新颖性、可行性、方法正确性或期刊适配度，也没有修改 dossier。
- 首次批量加载评估规范时终端输出发生截断，随后已分别完整补读 language-hard-gates、中文与学科约定、terminology review、模板、扫描器和 validator；首次整篇显示 dossier 时也发生截断，随后已按带行号的 1–170、171–340和341–499行连续补读到文件末尾。只读扫描输出未截断。
