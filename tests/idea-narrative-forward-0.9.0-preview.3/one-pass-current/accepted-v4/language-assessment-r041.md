---
review_id: language-assessment-r041
reviewer_skill: academic-language-assessor
reviewer_instance_id: fresh-language-r041
workflow_id: RID-SEPSIS-CSM-20260717-001
round_id: r041
input_artifact_ids:
  - idea-dossier-I01-001-v028
  - reader-handoff-forward-001
input_versions:
  - v028
  - v001
scope: complete_idea_dossier
dossier_ref:
  artifact_id: idea-dossier-I01-001-v028
  version: v028
  path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/accepted-v4/idea-dossier-v028.md
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
  - tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/accepted-v4/idea-dossier-v028.md
  - tests/idea-narrative-forward-0.9.0-preview.3/run-001/inputs/reader-handoff.yaml
isolation_mode: fresh_subagent
prior_scores_visible: false
source_edits_performed: false
decision: major_language_revision
findings:
  - finding_id: LANG-R041-01
    severity: major
    category: terminology_first_use
    dossier_locator: "Title, summary, audience, and positioning，第 32 行；Structured abstract，第 39–42 行；Primary research question，第 74 行；Objectives，第 81 行；Core hypothesis，第 85 行；首次完整说明见 Conjunctive stage-II success definition，第 101–109 行"
    current_problem: "“阶段 II”在一句话摘要、摘要、研究问题和核心假设中承担是否启动 RCT 次要分析及是否支持核心结论的关键作用，但首次出现时没有说明该阶段包含哪些科学工作或达标条件。读者交接明确禁止假定读者熟悉项目内部阶段标签；读者必须前进到第 101–109 行才能确定其指向。"
    target_state: "在第一次面向读者的使用处直接说明该阶段所指的科学工作和达标条件，之后才使用一个稳定的简称。"
    required_change_or_replacement: "将首次用法改为直接表述，例如：“只有双数据库数据支持、模拟恢复检验、两项主要任务、泄漏检查和不更新参数的跨数据库外部验证均达到预设标准时（下文简称‘阶段 II 达标’），才……”。后文统一使用“阶段 II 达标”，避免未定义的“阶段 II 结果”“阶段 II 证据成立”等变体。"
    content_to_preserve: "保留 24 个月边界、五类标准的实质内容、RCT 分试验且有条件启动，以及 RCT 结果不能补足前述证据缺口的边界。"
    acceptance_test: "目标读者在首次看到阶段简称的同一句中即可指出其五类科学判定对象；全文只保留一个已定义的阶段简称，且不需要跳到第 101 行以后才能理解摘要和研究问题。"
  - finding_id: LANG-R041-02
    severity: major
    category: terminology_naturalness
    dossier_locator: "Positioning and contribution frame，第 34 行；Structured abstract，第 39–42 行；Objectives，第 80 行；Absolute simulation and semi-synthetic recovery，第 222–234 行；Evidence chain: 数据支持、锚定识别与绝对恢复，第 295–300 行；Expected outputs，第 346 行；Falsification criteria，第 356 行"
    current_problem: "“绝对模拟恢复”“绝对恢复”和“模拟恢复”交替出现。“绝对”在首次使用时既可能修饰模拟，也可能修饰恢复，且没有指出被恢复的是状态、转移、结构还是概率。方法段直到第 224–234 行才表明实际操作是在模拟与半合成数据中按预设数值阈值检验多个量的恢复能力。该压缩标签对跨学科读者不自然，也使同一核心方法的名称漂移。"
    target_state: "首次出现即以普通科学语言说明数据类型、待检验对象和绝对阈值的作用；后文使用一个简短且稳定的名称。"
    required_change_or_replacement: "首次改为“在模拟和半合成数据中，按预设绝对阈值检验状态、转移、结构和概率的恢复能力（下文简称‘模拟恢复检验’）”；后文按语义使用“模拟恢复检验”或“预设恢复标准”，删除孤立的“绝对恢复”和“绝对模拟恢复”。"
    content_to_preserve: "保留正确指定、零边、过拟合和错设生成情景，以及状态、转移、边、覆盖、概率校准和不作解释的全部数值标准。"
    acceptance_test: "首次用语在不依赖项目词汇表的情况下同时回答“用什么数据检验”“恢复什么”“按什么标准判断”；全文不再以“绝对恢复”单独指代这一组操作。"
  - finding_id: LANG-R041-03
    severity: major
    category: reader_facing_workflow_vocabulary
    dossier_locator: "Positioning and contribution frame，第 34 行；Structured abstract，第 42 行；Core hypothesis，第 85 行；最低分析顺序，第 122 行；Evidence chains，第 286–321 行；Contribution and evidence progression，第 365–375 行；Title and positioning claim-support table，第 389–397 行"
    current_problem: "“合取证据”“五条证据链”“输入层—转换层—输出层”“任务效度”“失败图”“弃权项目清单”“外部分析角色”等表达把内部组织方式写入了核心科学叙述。部分词虽能猜测，但没有稳定的领域指向；例如“合取证据”实际意为五类标准必须同时满足，“弃权”实际意为不作结构解释，“失败图”实际意为未达标结果及其图表。它们在摘要、核心假设和贡献段中增加了读者翻译负担。"
    target_state: "核心段落直接说出证据对象、必须同时满足的关系、未达标时不作何种解释，以及三种外部分析各自做什么；内部组织标签不承担科学含义。"
    required_change_or_replacement: "将“合取证据/合取结论”改为“必须同时满足的五类证据/只有五类标准均满足时才作出的结论”；将“证据链”在正文中改为各项研究工作及其判定依据的直接名称；将“任务效度”改为“两项主要任务的预测与校准表现”；将“失败图”改为“未达标结果及其图表”；将“弃权”改为“不作相应结构解释”；将“外部分析角色”改为“三种外部分析方式”。第 286–321 行若为固定结构标题，可保留结构，但不应把这些标签带入摘要、假设或贡献主张。"
    content_to_preserve: "保留五类标准必须同时满足、各研究部分相互衔接但分别判定、三种外部分析分开报告，以及未达标时限制解释范围的含义。"
    acceptance_test: "摘要、研究问题、核心假设和贡献段不再要求读者把内部组织标签反译为科学操作；每个替换短语都能直接指出对象、操作或判定后果。"
  - finding_id: LANG-R041-04
    severity: minor
    category: title_modifier_attachment
    dossier_locator: "主标题与 Title 字段，第 27 行和第 31 行"
    current_problem: "“脓毒症全病程候选动态系统表征”连续叠加疾病范围、病程范围、证据状态和方法属性，“候选”可被读成修饰“动态系统”或“表征”；“利用 RCT 稀疏访视数据开展次要分析”虽可理解，但标题整体过长，核心研究对象不易一次识别。"
    target_state: "使“候选”明确修饰表征，使“动态”明确描述表征的时间性质，使“稀疏”明确修饰 RCT 访视数据，并保留条件性次要分析的证据状态。"
    required_change_or_replacement: "可改为“脓毒症全病程 ICU 患者系统的候选动态表征：跨数据库验证计划及满足预设条件后基于 RCT 稀疏访视数据的次要分析”。若保留原词序，也须通过“的”结构或断句消除修饰关系歧义。"
    content_to_preserve: "保留脓毒症全病程、ICU 患者系统、候选而非已验证、跨数据库验证为计划、RCT 访视稀疏、次要分析有预设前置条件。"
    acceptance_test: "逐层解析修饰关系时，“候选”只指向表征，“动态”只指向表征的纵向性质，“稀疏”只指向访视数据，“满足预设条件后”只限定 RCT 次要分析。"
  - finding_id: LANG-R041-05
    severity: minor
    category: bilingual_lexical_consistency
    dossier_locator: "Conjunctive stage-II success definition，第 111 行；Public ICU database roles and observability audit，第 149–164 行；Protocol specifications，第 188 行；Observational target，第 220 行；Trial-specific mapping，第 264–265 行；Key techniques，第 276、280、283 行；Working assumptions 与 Limitations，第 410、416 行"
    current_problem: "目标语言为中文，但普通叙述中交替使用 dossier、ICU stay、bootstrap、pattern-mixture delta、sepsis-like 等英文词；其中一些未在首次出现处给出中文功能说明，同一类概念又在其他位置使用中文。标准缩写和方法名可以保留，但当前混用削弱了中文文本的一致性。"
    target_state: "标准缩写和专名保留；一般叙述优先使用中文。确有必要保留的英文方法名在首次出现时给出中文功能说明，之后统一一种形式。"
    required_change_or_replacement: "将正文中的 dossier 改为“本研究方案”；ICU stay 改为“ICU 入住记录”；bootstrap 首次写作“自助法（bootstrap）”后使用“自助法”；pattern-mixture delta 首次写作“模式混合敏感性分析的偏移参数 δ（pattern-mixture delta）”；sepsis-like 改为“符合操作性类脓毒症标准的人群”。数据库名、RCT、SOFA、CRF、SAP、WBC、CRP 和数学符号可保留。"
    content_to_preserve: "保留标准缩写、数据库和试验专名、统计方法身份、分析集定义及所有数值。"
    acceptance_test: "除已定义的标准缩写、专名和数学符号外，正文不再出现未说明的通用英文词；同一概念在首次双语定义后只使用一种形式。"
  - finding_id: LANG-R041-06
    severity: major
    category: readability_qualifier_stacking
    dossier_locator: "One-sentence complete-Idea summary，第 32 行；Primary research question，第 74 行；Core hypothesis，第 85 行；Working assumptions，第 409–410 行"
    current_problem: "这些核心句把研究对象、多个前置条件、三至五个并列操作、例外和结论塞入单句。第 74 行的主问题同时包含三层编号与“仅在……时……否则……”分支；第 85 行在一个若—则结构之后又引入五类判定和两个排除条件。语法基本成立，但读者需反复回看限定语归属。"
    target_state: "每个核心句先给出一个明确主命题，再以并列分句或编号分别表达条件、研究任务和未达标后果；限定语紧邻其所限定的操作。"
    required_change_or_replacement: "在不删减科学条件的前提下，将第 74 行改为一个总问题加三个独立子问题，并把 RCT 的“满足条件时/否则”分支放在第三个子问题内；将第 85 行拆为“前置条件—可检验假设—不改变主判定的次要结果”三句。第 409–410 行把已确定内容、待登记内容和未登记后果分别成句。第 32 行受一句话摘要格式约束时，至少删除已在首用定义中吸收的内部简称，并用分号只分隔两条主线。"
    content_to_preserve: "保留所有前置条件、三项研究问题、五类证据的共同要求、两项次要诊断和 RCT 结果不改变主要判定，以及两项工作假设的登记时点。"
    acceptance_test: "每个并列条件都能唯一对应一个动词或结论；第 74、85、409、410 行不再包含跨越两个以上层级的嵌套限定，且拆分后没有删除任何科学边界。"
  - finding_id: LANG-R041-07
    severity: minor
    category: grammar_and_collocation
    dossier_locator: "Structured abstract，第 38 行；Current state，第 52 行；Trial 表，第 264–265 行；Risks, alternatives, and stop conditions，第 437 行"
    current_problem: "存在数处局部搭配或句法压缩：“有界检索尚未建立……代表性架构”把检索写成架构的建立者；“其中心、年代、采样和数据接口并不等价”搭配生硬；“目标为 1,817 名全体随机化受试者分析集”缺少清晰主干；“不作未受影响基线”省略必要成分；“区间不能排除无支持”不能明确指向零差异还是证据不足。"
    target_state: "主语与动作匹配，分析集句有明确系词，基线句说明未受何种影响，不确定区间的统计含义直接表达。"
    required_change_or_replacement: "第 38 行用“现有有界检索尚未发现……”；第 52 行用“这些数据库在收治中心、数据年代、采样方式和数据接口方面存在差异”；第 264 行用“目标分析集为全部 1,817 名随机化受试者”，第 265 行作同构修改；将“不作未受影响基线”改为“不视为未受干预影响的基线”；第 437 行按原意改为“不确定区间仍与无组间差异相容”或直接说明尚不能支持何种方向性差异。"
    content_to_preserve: "保留有界检索的范围限制、数据库异质性、全体随机化分析集优先、随机化后测量不能作为未受干预基线，以及结果不确定时不作肯定结论。"
    acceptance_test: "所列五类句子均有明确主语、谓语和指向；修改不新增关于检索、数据库或试验结果的事实判断。"
  - finding_id: LANG-R041-08
    severity: minor
    category: terminology_consistency
    dossier_locator: "Positioning and contribution frame，第 34 行；Rationale，第 66 行；Objectives，第 78 行；Twenty-four-month programme，第 91 行；Key techniques，第 275 行；Evidence chain: 信息可用时钟、风险集与互斥病程，第 288–293 行"
    current_problem: "同一核心时间设计先后称为“全病程时钟”“双时钟”“标签可用性时钟”“事件与信息可用双时钟”。“全病程时钟”像比喻且没有明确对应两个时间量；“标签可用性时钟”又可能只指第二个时间量。首次使用和后续简称之间缺少稳定映射。"
    target_state: "首次直接命名两个时间量，随后只在确实同时指二者时使用“事件—信息双时刻”或已定义的“双时刻设计”；只指第二个时间量时使用“标签信息可用时刻”。"
    required_change_or_replacement: "第 34 行改为“事件发生时刻与信息可用时刻”；第 66 行首次定义“分别记录事件发生时刻与信息可用时刻的双时刻设计”；后文同时指二者时统一用“双时刻设计”，只指标签可用性时用“标签信息可用时刻”，删除“全病程时钟”。"
    content_to_preserve: "保留事件发生与信息可用必须分开记录、后录入信息不得回填，以及特征查询只使用预测时点前可用信息。"
    acceptance_test: "每个“时刻/时钟”用法都能唯一判断是指事件发生、信息可用还是两者；全文不再出现未定义的“全病程时钟”。"
unresolved_issues:
  - LANG-R041-01
  - LANG-R041-02
  - LANG-R041-03
  - LANG-R041-04
  - LANG-R041-05
  - LANG-R041-06
  - LANG-R041-07
  - LANG-R041-08
---

# Language Assessment Report

**Assessment ID**: language-assessment-r041  
**Target Language**: Chinese  
**Discipline**: 重症医学、临床流行病学、纵向统计、系统辨识、医学 AI 与转化研究  
**Target Journal**: 未指定  
**Scope**: complete_idea_dossier  
**Date**: 2026-07-19

---

## Overall Language Readiness

**Level**: major_language_revision

**Recommendation**: revise_language

全文的时态、事实状态和大多数技术符号较稳定，但核心摘要、研究问题和贡献段仍依赖未及时定义的阶段标签、压缩术语和内部组织词汇。术语门槛因此未通过；修订应集中在首次定义、直接描述和句法拆分，不需要改变科学设计。

---

## Dimension Scores

| Dimension | Score (1–10) | Severity |
|-----------|-------------|----------|
| Grammar & Syntax | 7 | pass |
| Academic Register & Tone | 6 | borderline |
| Terminology Consistency | 4 | fail |
| Tense & Voice Conventions | 9 | pass |
| Conciseness & Redundancy | 4 | borderline |
| Readability & Flow | 5 | borderline |

---

## Hard Gate Status

**Overall**: fail

| Gate | Status | Detail |
|------|--------|--------|
| Grammar error density | pass | 明确句法或搭配错误约 8 处，按全文篇幅折算低于 1/500 词，未超过 3/500 词阈值 |
| Academic register | pass | 语体总体正式；内部组织词汇与中英文混用影响适切性，但未形成两个章节中的系统性口语语体 |
| Terminology coherence | fail | “阶段 II”与“绝对模拟恢复”均在摘要或核心设计中首次出现时对既定跨学科读者不可直接理解；“全病程时钟/双时钟/标签可用性时钟”另有名称漂移 |
| Tense systematic violation | pass | 计划性研究始终以“拟、计划、须、若、尚未”等前瞻表达陈述，未把计划写成已完成结果 |

术语门槛失败依据是核心术语在首次面向读者的使用处不可及，而不是因为未在外部来源中检索到某个完整复合短语。

---

## Strengths

1. 全文能够稳定区分“已核实”“尚未核实”“尚未生成”和“计划产物”，没有用完成时态夸大研究状态。
2. `Y_t`、`A_t`、`M_t`、`B`、`S` 等符号在定义后保持一致，生理测量、治疗行动、观测过程和标签的语言边界总体清楚。
3. 对观察性关联、随机化比较、预测表现和因果解释的限制多用直接否定句表达，语气克制。
4. 大量操作定义、阈值和停止条件具有可定位的表格或段落，便于后续作局部语言修订。

---

## Specific Issues

### Chinese Academic Clarity

- **LANG-R041-03（major）**：第 34、42、85、286–321、365–375、389–397 行中的“合取证据”“证据链”“输入层—转换层—输出层”“任务效度”“失败图”“弃权项目清单”“外部分析角色”把内部组织方式带入核心科学叙述。按 frontmatter 中的对应关系改为直接说明证据对象、判定关系和未达标后果。
- **LANG-R041-06（major）**：第 32、74、85、409–410 行堆叠前置条件、分支和排除条件。保留全部科学边界，但把总命题、子问题、达标条件和未达标后果拆开表达。
- **LANG-R041-04（minor）**：第 27、31 行的标题存在连续前置修饰。建议采用 frontmatter 中给出的标题，或用同等直接的“的”结构明确每个修饰语的归属。
- **LANG-R041-05（minor）**：正文中的 dossier、ICU stay、bootstrap、pattern-mixture delta、sepsis-like 需按首次中文说明后统一形式；标准缩写、专名和公式不属于该问题。

### Grammar & Syntax

- **LANG-R041-07（minor）**：第 38、52、264–265、437 行存在主语—动作错配、名词堆叠或成分省略。建议逐项采用 frontmatter 中的局部替换；这些修改不涉及方法选择。
- 除上述局部问题外，未发现达到硬门槛密度的明确语法错误。

### Academic Register & Tone

- **LANG-R041-03（major）** 同时影响学术语体：问题不是口语化，而是核心段落使用了面向内部组织的短标签。固定机器字段或固定结构标题本身不计入此项；只有它们进入摘要、假设、贡献、正文或面向读者的表格内容时才需改写。
- “挽救结论”（第 420 行）和“影子评价”（第 385 行）不是阻断项，但在处理 LANG-R041-03 时宜分别改为“不以事后亚组选择改变结论”和“在实际运行环境中进行被动评价”，前提是后者与作者所指研究类型一致。

### Terminology Consistency

| id | term_or_phrase | locator | reader_baseline | problem | recommended_replacement | first_use_definition | basis | acceptance_test |
|---|---|---|---|---|---|---|---|---|
| LANG-R041-01 | 阶段 II | 第 32、39–42、74、81、85 行；定义迟至第 101–109 行 | 不假定熟悉项目阶段标签 | 核心启动条件和结论边界在首次出现时不可识别 | 阶段 II 达标 | “双数据库数据支持、模拟恢复检验、两项主要任务、泄漏检查和不更新参数的跨数据库外部验证均达到预设标准（下文简称‘阶段 II 达标’）” | reader handoff 的首次定义要求；dossier 第 103–109 行自己的五类标准。替换为直接描述，未使用外部来源 | 首次使用即可列出五类判定对象，后文仅用一个简称 |
| LANG-R041-02 | 绝对模拟恢复／绝对恢复／模拟恢复 | 第 34、39、80、222–234、295–300、346、356 行 | 具有统计或系统辨识背景，但不熟悉新造标签 | “绝对”的修饰对象和恢复对象均不清楚，名称又漂移 | 模拟恢复检验／预设恢复标准 | “在模拟和半合成数据中，按预设绝对阈值检验状态、转移、结构和概率的恢复能力” | dossier 第 224–234 行的操作与阈值。替换直接命名数据、对象和标准，未使用外部来源 | 首用同时回答数据、对象和判断标准；不再单用“绝对恢复” |
| LANG-R041-03 | 合取证据、证据链、任务效度、弃权、失败图、外部分析角色 | 第 34、42、85、122、286–321、365–375、389–397 行 | 不假定熟悉项目内部工作词汇 | 多个短标签需要读者反译为具体证据、性能或不解释的后果 | 必须同时满足的五类证据；两项主要任务的预测与校准表现；不作相应结构解释；未达标结果及其图表；三种外部分析方式 | 不保留新的总括短标签；在每处直接命名对象、操作或判定后果 | reader handoff 禁止假定内部词汇；dossier 各方法与输出段已提供直接指称内容。未使用外部来源 | 摘要、假设和贡献段无需项目词汇表即可理解 |
| LANG-R041-04 | 脓毒症全病程候选动态系统表征 | 第 27、31 行 | 多学科研究者，不假定共享同一表征学习术语 | 连续修饰使“候选”的依附对象不唯一 | 脓毒症全病程 ICU 患者系统的候选动态表征 | 由紧随标题的一句话摘要直接说明该表征覆盖发病前、首次发病、发病后状态和结局 | dossier 的 study object 与第 32 行范围说明。替换直接命名对象和属性，未使用外部来源 | 候选、动态、稀疏和条件性修饰分别只有一个语法依附对象 |
| LANG-R041-08 | 全病程时钟／双时钟／标签可用性时钟／事件与信息可用双时钟 | 第 34、66、78、91、275、288–293 行 | 熟悉纵向临床数据，但不熟悉新造比喻 | 同一设计的名称漂移，且“全病程时钟”没有指出两个时间量 | 事件发生时刻与信息可用时刻；双时刻设计；标签信息可用时刻 | “分别记录事件发生时刻与信息可用时刻的双时刻设计” | dossier 第 48、66、189–190 行的直接定义。替换直接命名两个时间量，未使用外部来源 | 每处都能判断指一个时刻还是两个时刻，不再出现“全病程时钟” |

术语复核只针对上表触发项。没有生成完整术语清单，也没有检索外部来源；推荐项均为依据 dossier 自身操作性说明形成的直接描述，而不是另一个需要外部标准性证明的紧缩标签。

### Tense & Voice Conventions

未发现系统性时态或语态问题。计划、条件、未完成状态与拟议结果的表达保持一致；修订时应继续保留“拟、计划、只有……时、尚未”等证据状态标记。

### Conciseness & Redundancy

- **LANG-R041-06（major）**：核心问题不是单纯篇幅长，而是同一句内限定语过多。应在原位置拆分句法，不由本次语言评估决定哪些科学条件可删除或移至其他章节。
- 第 103–109、323–338、340–361、399–438 行多次复现数据支持、恢复、外部验证和 RCT 前置条件。可在后续语言修订中消除近似逐字重复，但本报告不指定删除哪个论证位置，也不改变 authoritative limitations 的内容归属。

### Readability & Flow

- **LANG-R041-01、LANG-R041-02、LANG-R041-03** 使读者在摘要和核心假设中提前遇到后文才可解释的简称；先完成首次定义和直接描述，再处理句长。
- **LANG-R041-06** 的句法拆分是主要可读性修复。第 254–256 行的公式段可以保留技术密度，但应在公式前后各用一句普通中文说明输入、输出和达标含义。
- **LANG-R041-07** 的局部搭配修复可消除不必要的回读。

---

## Language Revision Priorities

1. **核心术语首次定义**：2 个 major 术语问题 — 在摘要首用处直接说明阶段范围与模拟恢复操作，后文统一简称。
2. **面向读者的学术表达**：1 个 major 词汇模式 — 把内部组织标签替换为具体证据、性能指标和判定后果。
3. **核心句可读性**：1 个 major 句法模式 — 将研究问题、核心假设和工作假设拆为主命题、条件和后果。
4. **标题与时间术语**：2 个 minor 问题 — 明确复合修饰关系，并统一两个时间量的名称。
5. **中英文与局部搭配**：2 个 minor 问题 — 首次双语定义后统一用词，修正所列主语—动作和分析集句法。

---

## Re-Assessment Status (if applicable)

本次为 Idea dossier 的全新全稿评估，没有接收或读取既往问题清单。

| Check | Current assessment |
|--------|--------------------|
| Listed issues no longer present | 不适用 |
| Listed issues still present | 不适用 |
| New current-text issues | 8：LANG-R041-01 至 LANG-R041-08 |

---

## Assessment Notes

- 本评估只判断语言、术语可及性、语体、简洁性与可读性；不判断研究问题质量、方法正确性、可行性、创新性、影响或期刊适配。
- 读者基线以文件化 reader handoff 为准：可假定一般重症研究、纵向数据、验证、不确定性和观察性与干预性证据知识；不可假定项目内部阶段标签、新造短语或跨所有学科的详细专长。
- 目标文本为中文、跨重症医学与定量方法学研究方案；未指定期刊。
- 按任务限定，仅使用 frontmatter 所列文件。没有读取其他 dossier 版本、原稿、修订记录、其他评估报告、测试脚本或 Hermes 平台材料，也没有使用外部来源。
- 固定机器元数据和固定结构标签不因使用英文而自动计分；只有它们进入面向研究者的摘要、正文、表格内容或贡献叙述时才构成 LANG-R041-03 或 LANG-R041-05 所述问题。
- 源 dossier 与 reader handoff 均未修改。
