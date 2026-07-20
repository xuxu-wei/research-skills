---
review_id: language-assessment-I01-001-r011
reviewer_skill: academic-language-assessor
reviewer_instance_id: fresh-academic-language-assessor-r011-20260718
workflow_id: RID-SEPSIS-CSM-20260717-001
round_id: r011
input_artifact_ids:
  - idea-dossier-I01-001-v012
  - reader-handoff-forward-001
input_versions:
  - v012
  - v001
files_read:
  - AGENTS.md
  - research-skills/research/academic-language-assessor/SKILL.md
  - research-skills-openai/AGENTS.md
  - research-skills-openai/skills/academic-language-assessor/SKILL.md
  - research-skills-openai/skills/academic-language-assessor/references/language-assessment-rubric.md
  - research-skills-openai/skills/academic-language-assessor/references/language-hard-gates.md
  - research-skills-openai/skills/academic-language-assessor/references/chinese-academic-language-conventions.md
  - research-skills-openai/skills/academic-language-assessor/references/discipline-language-conventions.md
  - research-skills-openai/skills/academic-language-assessor/references/terminology-review.md
  - research-skills-openai/skills/academic-language-assessor/templates/language-assessment-report.md
  - tests/idea-narrative-forward-0.9.0-preview.3/run-001/release/idea-dossier-v012.md
  - tests/idea-narrative-forward-0.9.0-preview.3/run-001/inputs/reader-handoff.yaml
isolation_mode: fresh_subagent
prior_scores_visible: false
source_edits_performed: false
decision:
  overall_language_readiness: minor_language_revision
  recommendation: polish
  hard_gate_status: pass
findings:
  - id: L001
    severity: major
    dimension: terminology_consistency
    location: "跨学科概念桥，第 2 段，第 5 句；试验语义与共同观测变量资格，第 2 段"
    summary: “共同实测生理指标”及其相邻术语的集合关系在首次出现处不够明确。
  - id: L002
    severity: minor
    dimension: terminology_consistency
    location: "跨学科概念桥，第 2 段，第 2 句；结构式摘要 Background and gap，第 1 段"
    summary: “任务表现”对临床与跨学科读者不如“临床预测任务的性能”明确。
  - id: L003
    severity: minor
    dimension: terminology_consistency
    location: "结构式摘要 Objective and hypothesis，第 1 段，第 5 句；Core hypothesis，第 1 段"
    summary: “受限复杂模型”“受限复杂候选模型”和“复杂候选”之间的命名不统一，且“受限”修饰对象不清。
  - id: L004
    severity: minor
    dimension: academic_register_tone
    location: "One-sentence complete-Idea summary，第 1 段；三阶段导航，阶段 II；Limitations and boundary conditions，第 7 项"
    summary: “24 个月最低交付”带有产品交付或内部项目管理色彩，不符合全文的临床研究语体。
  - id: L005
    severity: minor
    dimension: academic_register_tone
    location: "Risks, alternatives, and stop conditions 表，‘试验语义与分析集’至‘观测映射外部忠实度’三行"
    summary: “分支不成立”“禁止恢复”“允许输出”“字段边界”等状态式标签泄漏到读者正文。
  - id: L006
    severity: minor
    dimension: conciseness_redundancy
    location: "结构式摘要 Background and gap，第 1 段，第 4—10 句"
    summary: 同一条目连续插入多项术语释义，重复“预定／预设”并显著增加信息密度。
  - id: L007
    severity: minor
    dimension: readability_flow
    location: "结构式摘要 Objective and hypothesis，第 1 段，第 6 句；Hospital-based cross-database validation，第 1 段末句"
    summary: “按未参与开发医院开展的验证”是压缩过度的多层修饰结构。
unresolved_issues:
  - L001
  - L002
  - L003
  - L004
  - L005
  - L006
  - L007
---

# Language Assessment Report

**Assessment ID**: language-assessment-I01-001-r011  
**Target Language**: Chinese（含必要的英文缩写、数据库名、文献题名和合同固定英文标题）  
**Discipline**: 重症医学与临床流行病学为主，涉及纵向统计、系统辨识和医学人工智能  
**Target Journal**: 未指定  
**Scope**: 完整 dossier  
**Date**: 2026-07-18

## Overall Language Readiness

**Level**: `minor_language_revision`  
**Recommendation**: `polish`

全文语法稳定、语体克制，方法与计划结果的时态边界清楚。当前问题不需要全面重写，主要需要统一核心术语、去除少量内部状态式措辞，并降低摘要及若干关键句的限定语密度。核心科学条件是否必须保留不属于本次评估范围；以下建议只涉及其语言表达。

## Scope and sections assessed

已完整评估从中文标题、定位与摘要、背景与研究问题、工作包、数据与方法、实现职责、证据链、必要分析、预期产物、贡献与最接近工作、可行性与限制、风险和停止条件，到参考文献的全部可呈现文本。YAML frontmatter、合同固定英文标题与字段标签作为结构性支架读取，但不计入读者正文的语言评分；仅检查其用语是否泄漏到正文。参考文献仅检查语言和格式一致性，不核验文献事实或科学结论。

## Dimension Scores

| Dimension | Score (1–10) | Severity | Evidence summary |
|---|---:|---|---|
| Grammar & Syntax | 9 | pass | 未发现影响理解的明确语法错误；少数压缩式名词短语属于自然度和可读性问题。 |
| Academic Register & Tone | 7 | pass | 整体正式、审慎，无宣传性或口语化表达；“最低交付”和风险表中的状态式标签偏内部项目语体。 |
| Terminology Consistency | 6 | borderline | 核心概念大多有定义，但共同指标术语族、复杂候选模型名称及“任务表现”仍需统一或改为更自然的描述。 |
| Tense & Voice Conventions | 9 | pass | 已知事实、既有研究、拟议方法和计划产物的证据状态区分稳定；Idea dossier 使用计划性表达符合文本类型。 |
| Conciseness & Redundancy | 5 | borderline | “预先／预设／冻结／隔离／共同／实际”等限定词在摘要和方法段落中频繁叠加，部分定义在多处近义复现。 |
| Readability & Flow | 6 | borderline | 总体层次清楚，但摘要、核心假设和风险表若干句或单元承载过多条件，跨学科读者需要回读。 |

## Hard Gate Status

**Overall**: `pass`

| Gate | Status | Detail |
|---|---|---|
| Grammar error density | pass | 完整阅读未发现达到阈值的明确语法错误；可计数的清晰错误约为 0/500 中文词语。中文分词边界不唯一，因此该数值仅用于门槛判断。 |
| Academic register | pass | 无两个以上章节以口语或非正式语体为主；内部状态式措辞局限于少量定位语和风险表。 |
| Terminology coherence | pass | 未发现 3 个核心概念各自以无理由的不同名称交替使用。共同指标术语族存在一处重要的集合关系不清，但后文形式化定义使其尚未达到不可辨认或误导的门槛。 |
| Tense systematic violation | pass | 本文是拟议研究构想而非已完成研究报告，方法使用现在时或计划性表达适当；没有把拟生成结果写成既成发现。 |

## Strengths

1. 全文持续区分“计划”“尚未生成”“已核验”“未核验”和“条件满足后”，证据状态表达准确，没有把拟议分析写成已完成结果。
2. 对预测、模拟恢复、跨数据库验证和随机试验组间比较的语言边界反复保持一致，未以因果或机制词汇替代预测与关联表述。
3. 主要英文缩写和术语大多在首次进入正文时给出中文对应或解释，如 SOFA、CIF、IPCW、ARI 和 MCSE；数据库名、数值、数学符号和中英文标点总体一致。
4. 章节顺序与段落衔接明确，读者能够沿研究问题、设计、证据和限制逐层阅读；表格标题及列名通常能说明各项内容的功能。
5. 语气克制，没有“重大突破”“填补空白”等无证据的宣传性用语，也没有不必要的修辞、情绪性表达或口语化问句。

## Specific Issues

### Chinese Academic Clarity and terminology

#### L001 — 共同指标术语族的首次关系不够明确

- **Severity**: major
- **Location**: “Title, summary, audience, and positioning”中“跨学科概念桥”第 2 段第 5 句；“Trial semantics and common-observation eligibility”第 2 段；另见“Current feasibility and evidence status”表“阶段 II 与试验间的共同生理观测指标”一行。
- **Original**: “条件性试验分析则把试验共同实测的生理指标经阶段 II 预先锁定的观测映射合成为一维状态摘要……”；后文又使用“共同观测变量”“共同变量集合”“生理观测锚点”“共同生理观测指标”。
- **Issue**: 首次出现的“试验共同实测的生理指标”可能被理解为“两项试验彼此共同测得的指标”，而形式化段落表达的是“每项试验中实际测得、且属于阶段 II 保留锚点的指标”。相邻名称可能表示上位集合、候选集合和合格子集，但首次出现处没有说明其关系。该概念直接连接阶段 II 与阶段 III，是跨学科读者理解设计所必需的核心术语。
- **Directional repair**: 在首次出现处用直接描述明确“共同”是指哪两类数据或变量集合之间的交集；随后为总体集合、候选集合和通过资格核验的集合各固定一个名称。无需提前搬入公式、阈值或完整变量清单。
- **Category**: ambiguous_term_mapping / first_use_clarity

#### L002 — “任务表现”过于宽泛

- **Severity**: minor
- **Location**: “跨学科概念桥”第 2 段第 2 句；“Structured abstract—Background and gap”第 1 段第 4 句；“Significance”第 1 段第 1 句及后续多处。
- **Original**: “任务表现衡量模型能否预测未来 12 小时首次发病或第 7 日状态。”
- **Issue**: “任务表现”近似英文 *task performance* 的直译。对重症医学和临床流行病学读者，它未在短语本身说明是临床预测任务的预测性能、校准表现，还是任务完成情况。
- **Directional repair**: 在首次出现处使用“临床预测任务的性能”或更具体的“首次发病与第 7 日状态预测性能”；后文需要总称时保持同一名称。
- **Category**: unnatural_technical_term

#### L003 — 复杂候选模型名称不统一，修饰关系含混

- **Severity**: minor
- **Location**: “Structured abstract—Objective and hypothesis”第 1 段第 5 句；“Core hypothesis”第 1 段；“Work packages and minimum route”表 WP2 行及其后执行顺序。
- **Original**: “至多一个受限复杂模型”“至多一个受限复杂候选模型”“至多一个复杂候选”。
- **Issue**: “受限”可能修饰模型复杂度、参数约束或候选数量；三个名称的语义范围也不完全相同。后文已分别规定复杂度上限和候选数量，因此可用自然语言直接表达二者，而不必压缩成“受限复杂”。
- **Directional repair**: 澄清此处需要表达的是“符合预设复杂度上限”还是其他约束，并固定一个全称；若两层限制均指向同一模型，可直接说明“至多保留一个符合预设复杂度上限的复杂候选模型”。
- **Category**: modifier_scope / term_variation

#### L004 — “24 个月最低交付”带有内部项目管理色彩

- **Severity**: minor
- **Location**: “One-sentence complete-Idea summary”第 1 段末；“三阶段导航”阶段 II；“Twenty-four-month minimum deliverable and dated milestones”第 1 段；“Limitations and boundary conditions”第 7 项。
- **Original**: “24 个月最低交付”“阶段 I–II 共同构成 24 个月最低交付”。
- **Issue**: “交付”在产品和工作流语境中常指交付物或内部验收，在临床研究构想中不如“必须完成的研究范围”“最低完成目标”自然。该词反复进入摘要和限制段，会使文本呈现内部项目管理语体。
- **Directional repair**: 选用一个学术研究语境下的名称，分别表达时间边界与必须完成的研究内容；避免把“最低范围”和具体产物都称为“交付”。
- **Category**: internal_workflow_language

#### L005 — 风险表出现状态机式标签

- **Severity**: minor
- **Location**: “Risks, alternatives, and stop conditions”表，“试验语义与分析集”“共同观测变量”“观测映射外部忠实度”三行的“替代方案与停止后果”列。
- **Original**: “分支停止”“允许输出”“字段边界”“一维状态摘要：分支不成立”“禁止恢复”。
- **Issue**: 这些短标签像内部流程状态或控制命令，不是面向研究者的自然学术表达；其中“禁止恢复”还可能被临床读者误读为患者恢复，而实际所指是不得重新启用分析路径。
- **Directional repair**: 改为完整的研究行动或解释边界，例如说明“停止该项分析”“此时仅报告……”“不得因组间差异较好而重新启用该分析”。保留原停止条件和后果，不改变设计。
- **Category**: machine_internal_language_leakage

### Conciseness and readability

#### L006 — 摘要中连续定义造成限定语和信息堆叠

- **Severity**: minor
- **Location**: “Structured abstract—Background and gap”第 1 段第 4—10 句。
- **Original**: 从“这些研究尚不能回答一个总问题……”到“本文所称预设结构稳定性……”。
- **Issue**: 同一项目先提出总问题，再连续定义“共同生理锚点预测”“关系的正负符号与时间滞后”“状态对齐”“预设结构稳定性”。“预定／预设”“状态／结构”“跨数据库”反复出现，摘要的主问题被定义链打断。
- **Directional repair**: 保留必要定义，但把主问题与术语释义分成更短的句群；合并重复的“本文所称／是指”结构，并优先保留跨学科读者在摘要中必须知道的功能性解释。是否在其他章节保留同一科学边界由相应叙事评估决定，本报告不指定删除位置。
- **Category**: qualifier_stacking / definition_density

#### L007 — “按未参与开发医院开展的验证”修饰层级过密

- **Severity**: minor
- **Location**: “Structured abstract—Objective and hypothesis”第 1 段第 6 句；“Hospital-based cross-database validation”第 1 段末句；“Planned outputs”表“临床任务与表征诊断结果”一行。
- **Original**: “按未参与开发医院开展的验证”。
- **Issue**: “按—医院—开展—验证”的结构与“未参与开发”定语叠加后，读者需要回读才能确定这是“在未纳入模型开发的医院中验证”，而不是“按医院开发验证”。
- **Directional repair**: 展开为介词结构，明确医院与模型开发之间的关系，并在全文统一该表达。
- **Category**: stacked_modifier / readability

### Grammar & Syntax

未发现需要单列的明确语法错误。L003 和 L007 是修饰范围与自然度问题，不计入语法错误密度。

### Academic Register & Tone

除 L004、L005 外未见系统性口语、宣传或过度防御性措辞。YAML frontmatter、英文合同标题和 `Input / Transformation / Output / Supports` 等固定字段作为结构性支架处理，不据此判定机器术语泄漏。

### Tense & Voice Conventions

未发现需要修订的系统性时态或语态问题。拟议设计使用“将”“拟”“须”“若……则……”与现在时定义相结合，符合尚未实施的研究构想；既有材料和当前核验状态也有明确区分。

## Focused Terminology Review

本次只审查普通阅读已触发的核心术语，不建立全量术语表，也不判断方法本身是否适当。

| id | term_or_phrase | locator | reader_baseline | problem | recommended_replacement | first_use_definition | basis | acceptance_test |
|---|---|---|---|---|---|---|---|---|
| T001 | 试验共同实测的生理指标／共同观测变量／共同变量集合／生理观测锚点 | 跨学科概念桥第 2 段；试验语义与共同观测变量资格第 2 段 | 熟悉临床研究与纵向数据，但不熟悉项目自定标签 | “共同”的参照集合不明，相邻术语间的上位、候选与合格子集关系未在首次出现处呈现 | 用直接描述指出“每项试验中实际测得且属于阶段 II 保留锚点的指标”，再固定集合名称 | 首次出现只需说明交集两端和用途，不必提前给公式或阈值 | dossier 后文的 (C_r) 定义与 reader handoff | 跨学科读者仅读标题、摘要和概念桥即可说清“共同”指什么，且能区分总体、候选与合格集合 |
| T002 | 共同生理锚点预测 | Structured abstract—Background and gap 第 1 段；Observational model target 第 1 段 | 不要求精通潜变量模型 | 语法上可能指“用于预测的锚点”或“对锚点指标的预测” | “共同生理锚点指标的预测值（或预测结果）” | 首次出现即说明它是对哪些指标所作的预测 | dossier 自身给出的后置定义；无需外部术语核验 | 名称本身不再产生两种修饰关系，后文使用同一形式 |
| T003 | 受限复杂模型／受限复杂候选模型／复杂候选 | Structured abstract—Objective and hypothesis；Core hypothesis；WP2 | 熟悉模型复杂度和验证，但不熟悉项目候选层级 | “受限”的修饰对象及三个名称的同一性不清 | “符合预设复杂度上限的复杂候选模型”或经作者确认的等义直接描述 | 首次出现说明复杂度受何种预设上限约束，并说明最多保留一个 | dossier 已给出维度、切换机制和候选数量上限 | 全文只有一个全称和必要简称，读者能区分“复杂度上限”与“候选数量上限” |
| T004 | 任务表现 | 跨学科概念桥第 2 段及后续多处 | 临床、流行病学、统计与医学 AI 混合读者 | 过宽，且接近英文直译 | “临床预测任务的性能”或直接列出两项预测性能 | 首次出现注明所指两项任务及评价对象 | dossier 该句自身已给出未来 12 小时和第 7 日两项任务 | 脱离上下文时仍能判断该词指模型的临床预测性能，而非项目任务完成情况 |

## Language Revision Priorities

1. **Terminology consistency**: 3 组核心术语问题 — 先明确共同指标术语族的集合关系，再统一复杂候选模型名称和预测任务用语。
2. **Academic register**: 2 组内部语体问题 — 将“最低交付”和风险表中的状态式标签改为研究范围、分析行动与解释边界的自然表述。
3. **Concision and readability**: 2 组局部密度问题 — 拆分摘要定义链，展开“未参与开发医院”等多层修饰语；不得借语言精简擅自删除科学条件。

## Re-Assessment Status

不适用。本次为针对 v012 完整 dossier 的全新独立评估；未提供匿名既往问题清单，也未读取先前文本、修订差异、既往语言报告或其他评审产物。

## Assessment Notes and limitations

- 评估依据 reader handoff 指定的跨学科研究者基线：可假定读者熟悉重症研究、纵向临床数据、验证与不确定性，但不可假定其了解项目自定标签或每个参与学科的技术细节。
- 主要采用生物医学／临床研究语体惯例，并在模型描述、算法符号和实验计划处兼顾计算机科学与工程的现在时惯例。未指定目标期刊，因此未施加期刊特有格式。
- focused terminology review 仅由文内可观察到的含混、直译和命名变化触发。上述建议依据 dossier 内部定义与读者基线提出；未以外部检索判断科学术语的真实性、标准性或方法有效性。
- 本报告不评价模型设计、阈值、统计方法、可行性、创新性或文献结论，也不判断重复出现的科学边界应在哪一章节保留。
