---
review_id: lang-r075
reviewer_skill: academic-language-assessor
reviewer_instance_id: fresh-subagent-language-v044-r075
workflow_id: RID-SEPSIS-CSM-20260717-001
round_id: r075
input_artifact_ids:
  - idea-dossier-I01-001-v044
  - reader-handoff-forward-001
input_versions:
  - v044
  - v001
scope: complete_idea_dossier
dossier_ref:
  artifact_id: idea-dossier-I01-001-v044
  version: v044
  path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v10/idea-dossier-v044.md
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
  - research-skills-openai/skills/academic-language-assessor/templates/language-assessment-report.md
  - research-skills-openai/skills/academic-language-assessor/scripts/validate_language_assessment.py
  - tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v10/idea-dossier-v044.md
  - tests/idea-narrative-forward-0.9.0-preview.3/run-001/inputs/reader-handoff.yaml
  - research-skills-openai/skills/academic-language-assessor/references/discipline-language-conventions.md
  - research-skills-openai/skills/academic-language-assessor/references/terminology-review.md
  - https://cccf.hrbeu.edu.cn/cn/article/id/b23a14a3-0523-4148-8940-ca843e63bcd5
  - https://pmc.ncbi.nlm.nih.gov/articles/PMC11289657/
  - https://www.nature.com/articles/s41467-025-62121-1
isolation_mode: fresh_subagent
prior_scores_visible: false
source_edits_performed: false
decision: major_language_revision
findings:
  - finding_id: LNG-R075-001
    severity: major
    finding_kind: language
    category: readability_and_stacked_qualification
    dossier_locator:
      - "Title, summary, audience, and positioning：标题及 One-sentence complete-Idea summary（第 27、31–32 行）"
      - "Research question, objectives, and core hypothesis：Primary research question（第 74–76 行）"
      - "Research question, objectives, and core hypothesis：Core hypothesis and non-hypotheses（第 87–91 行）"
      - "Research design and methods：观察性估计目标、临床锚定与证据不足时的处理（第 229–237 行）"
      - "Research design and methods：跨数据库检验与试验访视次要分析（第 253–321 行）"
    current_problem: >-
      标题、摘要单句、主要研究问题以及若干关键方法句把研究对象、四个病程阶段、模型约束、模拟重建、跨数据库检验、聚类要求和条件性试验分析连续嵌套在一个句法链中。第 32 行为 279 个字符，第 76 行为 199 个字符；第 278、294、320 和 321 行分别达到 216、264、383 和 314 个字符。反复出现的“若……并……且……后，才……”限定虽各有信息价值，但主干谓语被延迟，跨学科读者难以先识别主体问题再理解附加条件。
    target_state: >-
      关键入口先用一个完整主句说明研究对象、主要问题或主要分析，再用独立句或清晰分层的项目说明证据条件、失败条件和下游试验分析；所有科学限定均保留，但每个限定只附着于它实际约束的操作或结论。
    required_change_or_replacement: >-
      重组标题、单句摘要、主要研究问题、核心假设及上述长方法句。先陈述主体纵向建模与跨数据库检验，再将“主体研究达到预设标准后”的试验分析作为独立的次级句或副标题；把含两个以上条件层级或两个以上主要谓语的长句拆分，并补出明确主语。不得自行删去数据支持、时间顺序、聚类、模拟重建或试验启动条件。
    content_to_preserve: >-
      24 个月主体研究；发病前、首次发病、发病后和结局四阶段；患者—时间状态及转移；知识约束与不确定性；模拟重建与跨数据库检验；患者和医院聚类；主体研究达标后才启动且分试验报告的访视次要分析；不把预测解释为因果。
    acceptance_test: >-
      由不熟悉项目内部写法但具有读者交接材料所列基础知识的研究者通读标题、摘要和主要研究问题后，能在第一次阅读中分别指出主体研究对象、主要检验和条件性下游分析；这些入口不再以一个句子承载两层以上条件链。逐项核对后，上述必须保留的科学限定仍各自出现且修饰对象明确。
  - finding_id: LNG-R075-002
    severity: major
    finding_kind: language
    category: reader_baseline_and_internal_implementation_vocabulary
    dossier_locator:
      - "Research design and methods：满足预设条件后的随机对照试验访视次要分析，第 276 行"
      - "Key techniques and implementation：第 331–344 行"
      - "Evidence chains：第 346–381 行，尤其第 371 行"
      - "Required analyses and evidence 与 Expected outputs：第 383–405 行"
    current_problem: >-
      普通研究正文使用了未定义的内部实现和文档管理说法：第 276 行的“下游组件”“完整方法权威位置”；第 335–344 行的“引擎”“复杂度注册表”“变量角色注册表”“候选模型流水线”“诊断包”“开发锁定包”“试验访视分析包”“发布包”“执行器”“只读版本/只读模型”“回写参数”“接口压力”；第 371、387–402 行又重复“开发锁定包”“复杂度注册表”“变量角色注册表”。这些词把科学步骤、分析记录、代码或数据访问规则写成软件构建与内部文档术语，而读者交接材料明确不允许假定读者熟悉项目内部词汇。
    target_state: >-
      每个读者可见名称直接说明其科学内容或可复现性功能，例如标签定义与时间处理程序、变量用途表、模型拟合程序及版本记录、最终检验数据访问记录、缺失与治疗支持分析结果；必要的软件实现词在首次出现时说明其输入、输出和研究用途。
    required_change_or_replacement: >-
      在列出的四处逐项把内部短标签改为科学对象、分析操作或记录类型的直述名称；将“完整方法权威位置”改为该节包含完整预设方法的自然表述。若“只读”“锁定”“不回写”等词承载不可变性或隔离要求，应保留该要求，但改写为“不再修改”“仅用于读取”“不据此重新估计主体模型参数”等可直接理解的研究语言。对全文再检查上述全部内部词形及同类词，不只修改示例。
    content_to_preserve: >-
      标签和时间规则的版本化；字段角色唯一性与来源记录；开发后不修改模型；最终检验数据访问隔离；不同试验不共享拟合结果；阴性对照和失败结果仍须报告；所有输入、输出、权限和版本边界。
    acceptance_test: >-
      全文检索并人工复核“组件、权威位置、引擎、注册表、流水线、诊断包、锁定包、分析包、发布包、执行器、只读、回写、接口压力”等词。每处要么改为直接命名科学内容或研究记录的表达，要么在首次出现处给出跨学科读者可理解的功能定义；原有版本、隔离、不可修改和报告义务均未丢失。
  - finding_id: LNG-R075-003
    severity: minor
    finding_kind: terminology
    category: core_term_first_use_and_reader_accessibility
    dossier_locator:
      - "标题及 Title 字段（第 27、31 行）"
      - "One-sentence complete-Idea summary（第 32 行）"
      - "Positioning、Research question、Methods、Contribution 与 Limitations 中的后续简称“候选表征”"
    current_problem: >-
      “脓毒症全病程候选动态系统表征”是标题和主要问题中的核心名称。“动态系统表征”在复杂系统与人工智能文献中可作宽泛技术表述，但临床研究常直接命名具体模型、患者状态或状态转移。第 32 行虽列出病程阶段和患者—时间状态，仍未用一个独立定义明确“表征”究竟指哪些模型对象与关系；对仅具一般跨学科基础的读者，它可能被理解为特征表示、潜在状态、单一模型或整套研究流程。后文简称使用一致，因此这是首次定义精度问题，而不是术语混乱。
    target_state: >-
      首次普通正文先用直述语言说明该名称指向的科学对象和功能，再使用“候选表征”作为可选简称；标题中的范围修饰语应明确附着于患者状态、状态转移和纵向建模对象。
    required_change_or_replacement: >-
      在首次摘要句中加入完整的直述定义，并按该定义检查后文每一次“候选表征”是否仍指同一对象。可保留简称，但不得让简称替代首次定义；不必把公式、变量清单或数值阈值提前到摘要。
    content_to_preserve: >-
      候选性质；脓毒症发病前、首次发病、发病后与结局范围；患者—时间状态及转移；生理状态、治疗行动和检测记录过程的区分；多种简单模型与至多一个复杂实现；模拟重建和跨数据库检验。
    acceptance_test: >-
      标题和首个摘要句经重新解析后，读者能指出“脓毒症全病程”修饰的是所描述的病程范围，“患者—时间状态及其转移”是建模对象，“纵向模型及其状态、转移和观测关系”是名称所指内容。全文检查确认“候选表征”只指这一已定义对象；无需项目词汇表也能理解。
    term_or_phrase: 脓毒症全病程候选动态系统表征（简称“候选表征”）
    recommended_form_or_plain_description: >-
      用于描述并检验脓毒症发病前、首次发病、发病后至结局阶段的患者—时间状态及其转移的一组预先限定的纵向模型，以及这些模型中的状态、转移和观测关系；完整说明后可继续使用“候选表征”作为简称。
    evidence_basis: >-
      定向核查显示，临床研究通常明确使用“state-space model/modelling”并直接说明患者状态、时间演化、观测过程或状态转移：Nature Communications 的 ICU 研究以 state-space model 预测 acuity outcomes and transitions（https://www.nature.com/articles/s41467-025-62121-1）；J. R. Soc. Interface 的研究把 state space model 定义为动态方程与观测方程组成的时间演化模型（https://pmc.ncbi.nlm.nih.gov/articles/PMC11289657/）。中文计算领域综述使用“复杂动态系统表征与建模”，但其摘要把“表征”作为宽泛统一框架而非临床受控术语（https://cccf.hrbeu.edu.cn/cn/article/id/b23a14a3-0523-4148-8940-ca843e63bcd5）。因此不否定该短语的技术用法，但跨学科临床读者需要及时的对象级定义。
    first_use_definition: >-
      本研究所称“候选表征”，是指一组预先限定的纵向模型及其状态、转移和观测关系，用于描述并检验脓毒症发病前、首次发病、发病后至结局阶段的患者—时间状态及其转移。
    competing_forms_and_locators: []
  - finding_id: LNG-R075-004
    severity: minor
    finding_kind: language
    category: unnatural_metaphor_and_collocation
    dossier_locator:
      - "Structured abstract：Contribution and impact（第 42 行）"
      - "Background：Significance 与 Rationale（第 64、68 行）"
      - "Contribution：正向计划贡献及其证据范围（第 432 行）"
    current_problem: >-
      “把候选表征的价值从……推进到……联合判断”“把交付重点……而不是收缩为……”“分离保护时间顺序”“把……预测对象推进为……科学对象”等方向性隐喻和动宾搭配不自然，掩盖了本可直接说明的证据关系或防泄漏作用，并带有项目宣传式语气。
    target_state: >-
      直接陈述增加了哪些评价维度、避免了哪类时间错误，以及研究对象接受哪些检验，不借助“推进、收缩、保护”等抽象空间或进程隐喻。
    required_change_or_replacement: >-
      将上述搭配分别改为“评价同时考虑……”“交付包括……而非仅包括……”“避免较晚获得的信息进入较早预测时点”“将……作为接受模拟重建和跨数据库检验的对象”等直述关系；逐句确认不增强现有证据状态。
    content_to_preserve: >-
      联合评价可重建性、可审计性与跨数据库稳定性；不把交付限于预测工具；区分事件时刻和信息可用时刻；候选对象须接受模拟与跨数据库检验。
    acceptance_test: >-
      四处表述均以可观察的操作、比较或证据关系为谓语，不再依赖“推进/收缩/保护”解释抽象概念，且计划性和条件性语气保持不变。
  - finding_id: LNG-R075-005
    severity: minor
    finding_kind: language
    category: bilingual_drift
    dossier_locator: "Feasibility, resources, risks, alternatives, and stop conditions：第 475 行自由标题“Working assumptions（待确认规格）”"
    current_problem: >-
      目标语言为简体中文，该自由标题同时使用英语和中文括注；“Working assumptions”不是需要保留的数据库名、方法名、缩写或符号，且“assumptions”与“待确认规格”并非完全同义，造成不必要的双语漂移。
    target_state: >-
      使用一个与下表内容一致的中文标题，明确这些项目是尚待确认的分析规格或取值，而非已经成立的研究假设。
    required_change_or_replacement: >-
      删除不必要的英语标题，只保留能准确反映表格功能的中文名称；不改动合同固定的英文标题、标准缩写、数据库名、公式或参考文献题名。
    content_to_preserve: >-
      这些规格尚未验证、其决定时点、允许依据及未解决后果。
    acceptance_test: >-
      该自由标题只使用中文且与表格四列语义一致；全文其余中英混用均限于标准缩写、专名、符号、参考文献或固定脚手架。
  - finding_id: LNG-R075-006
    severity: minor
    finding_kind: language
    category: technical_syntax
    dossier_locator: "Research design and methods：测量一致性、校准与投影重建误差标准，第 302 行"
    current_problem: >-
      “第一奇异轴解释 L_C 的 Frobenius 能量至少 50%”缺少表示比例关系的句法成分，“解释”也可能误读为文字说明，不能立即判断 50% 是能量占比还是其他量。
    target_state: >-
      明确第一奇异轴与 L_C 的 Frobenius 能量占比之间的数学关系。
    required_change_or_replacement: >-
      若原意确为比例阈值，改为“第一奇异轴所解释的 L_C Frobenius 能量占比至少为 50%”；若不是该含义，则由作者按既定公式明确分子、分母和阈值，不由语言修订改变统计定义。
    content_to_preserve: >-
      第一奇异轴、L_C、Frobenius 能量和 50% 阈值。
    acceptance_test: >-
      句子具有完整主谓结构，并明确 50% 所对应的比例；数学符号和既定阈值不变。
  - finding_id: LNG-R075-007
    severity: minor
    finding_kind: language
    category: schedule_notation_clarity
    dossier_locator: "Research content and work packages：24 个月主体研究与日期要求，第 104 行“月 13–18/20”"
    current_problem: >-
      “月 13–18/20”不是清晰的中文时间范围写法，读者无法仅据该单元格判断这是“13–18 月、必要时延至 20 月”、两个并列截止点，还是 13–20 月中的阶段安排。
    target_state: >-
      用完整文字写明该阶段的起止月及第 18 月和第 20 月各自承担的里程碑。
    required_change_or_replacement: >-
      根据既定计划把斜线压缩写法展开为一个无歧义的时间范围和里程碑说明；语言修订不得自行选择尚未确定的截止月。
    content_to_preserve: >-
      开发数据库内、时间外和医院外评价，开发锁定记录，以及月 20 后不得按最终检验结果修改开发内容的要求。
    acceptance_test: >-
      不查阅其他项目材料的读者能从该表行直接说出阶段开始月、常规完成月、最迟锁定月和月 20 后的限制；不再出现“18/20”斜线时间写法。
unresolved_issues:
  - LNG-R075-001
  - LNG-R075-002
  - LNG-R075-003
  - LNG-R075-004
  - LNG-R075-005
  - LNG-R075-006
  - LNG-R075-007
---

# Language Assessment Report

**Assessment ID**: lang-r075  
**Target Language**: Chinese（zh-CN）  
**Discipline**: 重症医学、临床流行病学、纵向统计与系统辨识、医学人工智能的跨学科研究  
**Target Journal**: 未指定  
**Scope**: complete_idea_dossier  
**Date**: 2026-07-19

---

## Overall Language Readiness

**Level**: major_language_revision

**Recommendation**: revise_language

全文语法和时态总体稳定，但关键入口句的限定堆叠，以及面向内部实现的词汇持续进入研究正文，已明显超过局部润色范围。需要在不改变科学条件的前提下重组关键句，并把内部短标签改为跨学科读者可直接理解的研究语言。

---

## Dimension Scores

| Dimension | Score (1–10) | Severity |
|-----------|-------------|----------|
| Grammar & Syntax | 8 | pass |
| Academic Register & Tone | 6 | borderline |
| Terminology Consistency | 7 | borderline |
| Tense & Voice Conventions | 9 | pass |
| Conciseness & Redundancy | 5 | borderline |
| Readability & Flow | 5 | borderline |

---

## Hard Gate Status

**Overall**: pass

| Gate | Status | Detail |
|------|--------|--------|
| Grammar error density | pass | 全文未见超过 1 个明确语法错误/500 中文词的区段；问题主要是句法压缩而非语法失范 |
| Academic register | pass | 未见两个以上章节存在系统性口语或非正式语体；内部实现词汇属于读者适配问题，不构成口语门槛失败 |
| Terminology coherence | pass | 未发现 3 个以上核心概念各有无理由竞争名称；核心简称总体一致，LNG-R075-003 为首次定义精度问题 |
| Tense systematic violation | pass | 计划性动作稳定使用“拟、计划、将、若……则……”等前瞻表达，既有证据与计划产物的时态界线清楚 |

---

## Strengths

- 全文持续区分已有证据、尚未核验内容、尚未生成结果和计划产物，语气未把未来工作写成既成事实。
- 观察性预测、结构解释、因果效应和随机分组比较的语言边界大体稳定，没有依靠强势动词夸大证据状态。
- MIMIC-IV、eICU-CRD、SOFA、CIF、Brier、Monte Carlo、Holm 等专名、缩写与符号使用基本一致，公式附近的中英文混排总体可读。
- 计划类文稿采用前瞻时态，方法定义多使用客观、直接的陈述句，未出现系统性口语、反问或感叹式表达。

---

## Specific Issues

### Chinese Academic Clarity

| finding | location | reader effect | priority |
|---|---|---|---|
| LNG-R075-001 | 标题、摘要、主要研究问题及关键方法句 | 多层条件遮蔽主干，首次阅读难以区分主体研究与条件性延伸 | major |
| LNG-R075-002 | 第 276、331–344、346–405 行 | 内部实现短标签要求读者猜测科学对象或记录类型 | major |
| LNG-R075-004 | 第 42、64、68、432 行 | 抽象方向隐喻弱化了证据关系和防泄漏作用 | minor |
| LNG-R075-007 | 第 104 行 | 斜线时间范围无法唯一解析 | minor |

完整操作要求见 frontmatter；正文仅列证据和优先级。

### Grammar & Syntax

- **LNG-R075-006（minor）**：第 302 行的“解释……能量至少 50%”缺少明确的占比句法，属于局部技术句法问题。
- 其余主要问题是长句负荷和修饰关系，不是高密度语法错误。

### Academic Register & Tone

- **LNG-R075-002（major）**：方法、实现和证据链中反复使用“权威位置、注册表、流水线、包、执行器、回写”等内部实现词，形式虽不口语，但不符合给定跨学科读者基线。
- **LNG-R075-004（minor）**：少量“推进、收缩、保护”等抽象隐喻带来宣传式或翻译式搭配，应改为直接的证据与操作关系。

### Terminology Consistency

| id | term_or_phrase | locator | reader_effect | action_in_frontmatter |
|---|---|---|---|---|
| LNG-R075-003 | 脓毒症全病程候选动态系统表征 | 标题、第 32 行及后续简称 | 首次定义未完全消除“表征”所指层级的歧义 | yes |

全文临时一致性检查覆盖了中心研究对象、主要问题、主要临床任务、跨数据库检验和贡献表述。除 LNG-R075-003 的首次定义精度外，未发现需要报告的核心术语竞争形式，也未创建术语表。

### Tense & Voice Conventions

none。计划、条件、既有证据与预期结果的时间状态总体一致；没有系统性时态错误。

### Conciseness & Redundancy

- **LNG-R075-001（major）**：问题不是简单删去限定，而是把多个局部必要条件压入同一句。修订应先重组，再由科学内容负责人确认每项条件的保留位置。
- “不能替代、不能抵消、不声称、不作解释”等边界表达在多个章节重复，但这些表达可能承担不同局部功能；本报告不决定删除哪一处，只要求避免在同一句内反复叠加同类防御性限定。

### Readability & Flow

- 关键入口句和若干表格单元格达到 199–383 个字符，段内主干识别困难，见 LNG-R075-001。
- **LNG-R075-005（minor）**：自由标题“Working assumptions（待确认规格）”造成可避免的双语漂移。
- **LNG-R075-007（minor）**：时间范围“月 13–18/20”需要展开。

---

## Language Revision Priorities

1. **读者基线与学术表达**：1 项重大问题 — 先将内部实现词汇逐项改为科学对象、操作或记录类型的直述名称。
2. **可读性与限定层级**：1 项重大问题 — 重组标题、摘要、主要问题和关键方法句，保留全部科学条件但拆开句法层级。
3. **术语首次定义**：1 项轻微问题 — 明确“候选表征”所指模型对象及关系，再统一核查全文简称。
4. **局部中文清晰度**：3 项轻微问题 — 修正抽象隐喻、技术句法和时间范围写法。
5. **双语一致性**：1 项轻微问题 — 将非必要的自由英文标题改为中文。

---

## Re-Assessment Status (if applicable)

不适用。本次为依据当前 dossier 与绑定 reader handoff 进行的全新完整评估，未读取匿名问题清单、既往分数、既往决定、旧版本或修订差异。

---

## Assessment Notes

- 已完整读取 dossier 的 frontmatter、标题、全部正文层级、表格、公式附近文字和参考文献，以及 reader handoff 的全部字段。固定的 research-idea.v3 英文脚手架标题和字段标签未计分，也未要求翻译或改名。
- 学科惯例按跨学科临床研究计划处理：重症医学与临床流行病学为主要语域，纵向统计、系统辨识和医学人工智能术语在首次使用时须兼顾非本专业读者。
- 普通通读仅触发“候选动态系统表征”一项定向术语核查。核查读取了两项原始临床研究的题名、摘要/引言与相关方法说明，以及一篇中文计算领域综述的题名和摘要；未检索或保存完整术语清单。
- 本报告只评价语言、读者基线、术语可理解性、双语一致性和行文清晰度，不评价论证质量、方法、创新性、影响或可行性，也未修改源 dossier。
