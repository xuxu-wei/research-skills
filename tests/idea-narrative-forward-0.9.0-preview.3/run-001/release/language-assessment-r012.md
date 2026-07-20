---
review_id: language-assessment-I01-001-r012
reviewer_skill: academic-language-assessor
reviewer_instance_id: fresh-v012-language-r012
workflow_id: RID-SEPSIS-CSM-20260717-001
round_id: r012
input_artifact_ids:
  - idea-dossier-I01-001-v012
  - reader-handoff-forward-001
input_versions:
  - v012
  - v001
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
  - tests/idea-narrative-forward-0.9.0-preview.3/run-001/release/idea-dossier-v012.md
  - tests/idea-narrative-forward-0.9.0-preview.3/run-001/inputs/reader-handoff.yaml
isolation_mode: fresh_subagent
prior_scores_visible: false
source_edits_performed: false
decision: major_language_revision
findings:
  - finding_id: L001
    severity: major
    category: terminology
    locator: Title, summary, audience, and positioning; paragraph beginning "研究中的四类证据"
  - finding_id: L002
    severity: minor
    category: terminology
    locator: Title, summary, audience, and positioning; paragraph beginning "研究中的四类证据"
  - finding_id: L003
    severity: minor
    category: terminology
    locator: Structured abstract; Objective and hypothesis
  - finding_id: L004
    severity: minor
    category: academic_register
    locator: Title, summary, audience, and positioning; One-sentence complete-Idea summary
  - finding_id: L005
    severity: minor
    category: academic_register
    locator: Feasibility, resources, risks, alternatives, and stop conditions; Risks, alternatives, and stop conditions table
  - finding_id: L006
    severity: minor
    category: readability
    locator: Structured abstract; Background and gap
  - finding_id: L007
    severity: minor
    category: grammar_syntax
    locator: Structured abstract; Objective and hypothesis
  - finding_id: L008
    severity: minor
    category: terminology
    locator: Structured abstract; Expected result
unresolved_issues:
  - L001
  - L002
  - L003
  - L004
  - L005
  - L006
  - L007
  - L008
---

# Language Assessment Report

**Assessment ID**: lang-I01-001-r012  
**Target Language**: Chinese  
**Discipline**: 重症医学、临床流行病学、纵向统计、系统辨识、系统科学、医学人工智能与转化研究  
**Target Journal**: 未指定  
**Scope**: 完整 Idea dossier；评估面向研究者的正文、表格和参考文献格式，不把机器前置元数据及合同固定标题本身作为学术语言  
**Sections assessed**: 全部 15 个 H2，包括标题与定位、结构化摘要、背景—现状—缺口—意义—依据、研究问题与目标、工作包、数据与证据、研究设计与方法、实现、证据链、必需分析、预期产物与证伪、贡献与近邻工作、主张支持表、可行性与边界、参考文献  
**Date**: 2026-07-18

---

## Overall Language Readiness

**Level**: major_language_revision

**Recommendation**: revise_language

全文已形成正式、较一致的中文学术语域，语法、时态和中英文缩写使用总体可靠。不过，阶段 III 的核心输入在前部被称为“试验共同实测的生理指标”等形式，修饰关系既可理解为“两项试验共同具有”，也可理解为“每项试验分别与阶段 II 锚点重合”。该歧义出现在设计桥接、研究问题和贡献链条中，直到方法部分定义每项试验各自的 \(C_r\) 才消除。它会改变目标读者对核心设计关系的理解，因此触发术语硬门；其余问题均为可定点修复的局部语言问题。

## Dimension Scores

| Dimension | Score (1–10) | Severity |
|-----------|-------------|----------|
| Grammar & Syntax | 8 | pass |
| Academic Register & Tone | 7 | pass |
| Terminology Consistency | 5 | fail |
| Tense & Voice Conventions | 9 | pass |
| Conciseness & Redundancy | 7 | pass |
| Readability & Flow | 6 | borderline |

## Hard Gate Status

**Overall**: fail

| Gate | Status | Detail |
|------|--------|--------|
| Grammar error density | pass | 中文不宜机械按空格分词；全文仅见少数可明确定位的搭配问题，按全文规模明显低于每 500 词 3 处的阈值 |
| Academic register | pass | 未见两个以上章节以口语为主；风险表中的项目管理式标签属于局部语域问题，不构成系统性口语化 |
| Terminology coherence | fail | 一个核心设计关系在首次及多次前部使用时存在实质性双重解读：每项试验与阶段 II 指标的交集，还是两项试验彼此共有的指标 |
| Tense systematic violation | pass | 计划、既有证据和拟生成结果的时间状态区分稳定，未见方法或结果时态的系统性误用 |

## Strengths

1. 计划、既有事实和尚未生成的结果区分明确，例如结构化摘要将产物表述为“计划产物”和“拟生成的结果”，没有用完成时态暗示已经验证。
2. 缩写和符号大多在首次使用时定义，SOFA、CIF、IPCW、ARI、MCSE 及 \(P_{state}\)、\(P_{obs}\) 的中英文或数学对应关系保持一致。
3. “状态占用概率”与“观察到的状态比例”、“关系符号与时间滞后”与“结构边方向”等容易混淆的概念得到显式区分。
4. 正文总体采用克制的学术语气，避免了“首次”“突破”等宣传性表述，并保持观察性、模拟、外部验证和随机试验证据的语言强度差异。
5. 限制、工作假设和风险条件集中在一个权威章节，前部正文没有大面积重复相同限定语，明显改善了行文连续性。

## Specific Issues

### Chinese Academic Clarity

#### L004 — “24 个月最低交付”带有项目内部交付语域（minor）

- **Locator:** “Title, summary, audience, and positioning”，One-sentence complete-Idea summary；三阶段导航；“Research content and work packages”，首段及后续相关表述。
- **Original:** “24 个月最低交付”“阶段 II 最低端点未完成”。
- **Issue:** “交付”和“最低端点”在此更像项目管理或内部状态用语，不如研究目标、完成标准或预定研究产物自然。该措辞多次出现在面向跨学科研究者的核心说明中。
- **Directional repair:** 在不改变时间边界和必要条件的前提下，统一改为“24 个月内必须完成的研究目标”“24 个月最低完成标准”或语境相符的“预定研究产物”；将“最低端点未完成”改为“阶段 II 的预定目标未完成”。
- **Acceptance test:** 核心正文不再用“交付”或“最低端点”指代科学研究目标；24 个月边界、阶段 I–II 范围及未完成后果均仍明确存在。

#### L005 — 风险表中的状态标签削弱学术自然度（minor）

- **Locator:** “Feasibility, resources, risks, alternatives, and stop conditions” → “Risks, alternatives, and stop conditions”表，尤其“试验语义与分析集”“共同观测变量”“观测映射外部忠实度”等行。
- **Original:** “分支停止”“允许输出”“字段边界”“一维状态摘要：分支不成立”“禁止恢复”“任务后果”“禁止替代”。
- **Issue:** 这些冒号前标签把科学条件和分析后果写成状态机式短语。内容本身可以保留，但标签密集出现时会使研究者像在阅读内部流程规则，而不是研究方案。
- **Directional repair:** 将标签改写为完整的功能性句子，例如直接说明“若……则不开展一维状态摘要分析”“仍可复现原终点或报告数据审计”“不得依据随机分组结果重新调整阈值”。不删除阈值、边界、备选方案或停止后果。
- **Acceptance test:** 表中每项后果可作为自然中文独立阅读；所有原有触发条件、禁止事项和备选路径逐项保留，且不新增科学判断。

#### L006 — 结构化摘要首项定义密度过高（minor）

- **Locator:** “Structured abstract” → “Background and gap”整条。
- **Original:** 同一条目连续引入“共同生理锚点预测”“关系的正负符号与时间滞后”“状态对齐”“预设结构稳定性”并逐一定义。
- **Issue:** 缺口陈述与四个技术定义竞争同一阅读位置。跨学科读者需要在尚未进入目标和方法前保留多个新概念，降低摘要的可读性。
- **Directional repair:** 保留缺口和所有必要定义，但将该条拆为较短的缺口句与定义句；先说模型需检验什么，再按使用顺序解释最少必要术语。不要把公式、阈值或实现细节前移。
- **Acceptance test:** 读者可在首读中分别指出现有证据缺口和待检验对象；每个必要术语仍在首次使用处或紧邻处得到解释，且没有改变科学含义。

### Grammar & Syntax

#### L007 — “按未参与开发医院开展的验证”修饰关系生硬（minor）

- **Locator:** “Structured abstract” → “Objective and hypothesis”；同类形式还见于“Research content and work packages”里月 13–18 里程碑、跨数据库验证段和计划产物表。
- **Original:** “按未参与开发医院开展的验证”。
- **Issue:** “按”同时承担分组依据和实施地点两种可能关系，“未参与开发医院”也缺少结构助词，形成堆叠修饰。
- **Directional repair:** 根据既有设计关系统一写成“在未参与开发的医院中开展的验证”或“基于未参与开发医院的验证”；不要改变医院分组、适配集或外部验证的设计。
- **Acceptance test:** 全文同类表达语法关系一致，读者无需判断“按”修饰医院划分还是验证行为。

除此之外，未发现影响理解的系统性语法错误、残句或指代断裂。

### Academic Register & Tone

除 L004 和 L005 外，全文保持正式、审慎的研究语域。未见口语、感叹、面向读者的直接指令或无依据的宣传性形容词。

### Terminology Consistency

| id | term_or_phrase | locator | reader_baseline | problem | recommended_replacement | first_use_definition | basis | acceptance_test |
|---|---|---|---|---|---|---|---|---|
| L001 | “试验共同实测的生理指标”“共同实测生理指标”“共同观测变量” | 概念桥、结构化摘要、Gap、Rationale、主要研究问题第 3 项、目标 4、Evidence chain；方法部分 Trial semantics 才定义 \(C_r\) | 熟悉重症研究与纵向数据，但不应假设熟悉项目自定简称 | “共同”既可能表示两项试验彼此共有，也可能表示每项试验分别与阶段 II 锚点重合；不同简称又使交集关系在核心段落中不稳定 | 首次使用时采用“每项试验中与阶段 II 生理锚点重合、且在相应访视实际测得的指标”，后文统一使用一个简短形式，如“每项试验的合格共同指标” | “该指标集合按试验分别确定，指该试验实际测得且与阶段 II 锚点在临床构念、标本、单位和访视时间上相符的指标；不要求两项试验使用同一组指标。” | 前部短语存在可验证的修饰歧义，而方法部分明确把集合写为每项试验各自的 \(C_r\)；采用直接描述即可消除歧义，无需另造术语或外部标准性主张 | 标题之后的概念桥、摘要、Gap、Rationale、研究问题、目标和证据链均明确“按试验分别求与阶段 II 锚点的交集”；抽查任一处不会被理解成“两项试验必须共有同一组指标” |
| L002 | “任务表现”“两项主要临床任务” | 概念桥、结构化摘要、Gap、假设、成功定义、工作包和结果解释 | 跨学科读者熟悉预测与校准，但“任务”也可指研究工作包 | 简称在部分位置没有提示这里专指两项预测任务的评分与校准，而非项目执行表现 | 在首次出现及易混位置使用“预测任务表现”或“两项主要预测任务”；固定后再简写 | “两项主要预测任务分别是未来 12 小时首次发病风险和发病后第 7 日状态概率预测；表现由预定评分与校准指标评价。” | 文内实际评价对象是 Brier 分数和校准；直接补足“预测”即可对应既有内容 | 首次定义同时给出两个预测对象和评价维度；“任务表现”不再可能指工作包进度或资源执行情况 |
| L003 | “受限复杂模型”“至多一个复杂候选” | Structured abstract 的 Objective and hypothesis；Core hypothesis；里程碑、工作包及执行顺序 | 读者理解受约束模型，但“受限复杂”可指能力受限或复杂度受限 | 中文组合不自然，且未稳定保留“候选模型”这个语义中心 | 统一为“至多一个受预设约束的复杂候选模型” | 首次出现时用紧邻短语概括约束来自双数据库审计、锚定、状态数和滞后预设，无需重列全部阈值 | 这是中文搭配和指称稳定性问题，不涉及选择模型类型 | 所有核心位置保留“候选模型”语义中心，并清楚表达“复杂模型受到预设约束”，而不是“模型能力受限” |
| L008 | “独立 SOFA 临床状态分析” | Structured abstract 的 Expected result 首次出现；Objectives 4；工作包、方法与风险表 | 读者理解 SOFA，但“独立”所独立于何者并不自然显现 | 直到方法后部才说明它“不使用阶段 II 的观测映射”，首次出现时可能被理解为独立样本、独立验证或统计独立性 | 首次写为“不依赖阶段 II 观测映射的 SOFA 临床状态分析”，定义后可简写为“SOFA 临床状态分析” | “该分析沿用预设的死亡、住院和存活出院排序，但不使用阶段 II 观测映射。” | 依据正文后部已经给出的关系作前置澄清，不新增方法选择 | 首次出现即可判断“独立”指与观测映射分离；后续简称单一且不暗示统计独立性 |

L001 为核心设计关系，且其双重解读会改变读者对阶段 III 输入集合的理解，因此定为 major 并触发术语硬门。L002、L003 和 L008 均可通过统一称谓与首次定义局部修复，不单独触发硬门。

### Tense & Voice Conventions

未发现需修订的问题。既有文献和数据库事实采用事实性表述；研究活动、输出和结果采用“计划”“拟”“将”等未完成状态；尚未生成的结果没有被写成既成发现。中文主动与无主句使用符合方案文本习惯。

### Conciseness & Redundancy

除 L004 的重复项目管理式短语和 L006 的摘要定义拥挤外，未见需要语言评估器决定删除的实质性重复。方法与风险部分重复出现某些指标名称，主要用于局部可执行性，是否保留属于叙事功能判断，本报告不作跨章节删除决定。

### Readability & Flow

主要问题为 L006 的摘要定义密度以及 L007 的堆叠修饰。技术方法段的公式、阈值和表格虽密集，但均位于相应技术章节，且多数术语在使用前后得到解释；不以技术密度本身判为语言错误。

## Language Revision Priorities

1. **Terminology — L001:** 首先消除“共同实测指标”的双重解读，并在所有核心段落统一为“每项试验分别与阶段 II 锚点重合”的关系；这是解除术语硬门的必要条件。
2. **Terminology — L002、L003、L008:** 统一“预测任务”“受预设约束的复杂候选模型”和“不依赖阶段 II 观测映射的 SOFA 分析”的首次定义与后续简称。
3. **Academic register — L004、L005:** 把项目管理式交付/状态标签改为自然的研究目标与分析后果句，同时逐项保存原有边界和停止条件。
4. **Readability and syntax — L006、L007:** 拆分摘要中的定义串，并清理“按未参与开发医院开展”的修饰关系。

## Re-Assessment Status

本次为新鲜独立评估，未提供匿名既往问题清单，因此不执行问题关闭对照。

| Check | Current assessment |
|--------|--------------------|
| Listed issues no longer present | not applicable |
| Listed issues still present | not applicable |
| New current-text issues | L001–L008 |

## Assessment Notes

- 本报告只评价中文学术语言与目标读者可理解性，不判断模型、阈值、估计量、RCT 数据、创新性、影响力或可行性是否科学正确。
- 未指定目标期刊，因此采用重症医学、临床流行病学和方法学研究的一般中文学术方案语体；不强制某一期刊的格式偏好。
- 术语核查仅针对普通阅读中实际触发的四组表达。L001 的问题可由文内定义与中文修饰歧义直接确认，建议使用不产生双解的描述性表达；本次无需建立完整术语表，也不据单篇论文宣称某一简称为领域标准。
- 机器前置元数据、英文合同标题和字段标签未作为面向研究者的语言缺陷；其内容也未被要求翻译或改名。
- 未读取旧 dossier、revision delta、preflight、narrative report、既往 language report 或 evaluation，亦未修改 assessed dossier。
