---
review_id: language-assessment-r023
reviewer_skill: academic-language-assessor
reviewer_instance_id: fresh-language-r023
workflow_id: RID-SEPSIS-CSM-20260717-001
round_id: r023
input_artifact_ids:
  - idea-dossier-I01-001-v021
  - reader-handoff-forward-001
input_versions:
  - v021
  - v001
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
  - tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/revised/idea-dossier-v021.md
  - tests/idea-narrative-forward-0.9.0-preview.3/run-001/inputs/reader-handoff.yaml
isolation_mode: fresh_subagent
prior_scores_visible: false
source_edits_performed: false
decision: major_language_revision
findings:
  - finding_id: LANG-R023-01
    severity: major
    category: terminology_and_reader_baseline
    section: title_and_one_sentence_summary
    locator: "标题；Title, summary, audience, and positioning，第 1–2 个项目符号"
    excerpt: "条件性稀疏 RCT 次要再分析；试验数据、语义和观测映射均合格"
    issue: "标题中的‘稀疏’在句法上修饰 RCT，容易被理解为试验设计稀疏，而正文实际指访视和重复测量稀疏；‘次要再分析’也不如‘二次分析’自然。摘要首次提到‘观测映射’时未说明其输入、输出或作用，跨学科读者无法在核心定位处立即识别该分支的含义。"
    direction: "标题改用直接描述访视数据的标准表达，并在一句话摘要首次出现映射概念时说明：冻结的观测模型利用试验中共同实测的生理指标计算一维摘要。"
  - finding_id: LANG-R023-02
    severity: minor
    category: terminology_and_reader_baseline
    section: objectives_and_core_design
    locator: "Research question, objectives, and core hypothesis，Objectives 第 1 项；Structured abstract，Objective and hypothesis"
    excerpt: "landmark 风险集；错误高置信输出控制标准"
    issue: "两个承担核心设计作用的术语在首次出现时都高度压缩。‘landmark’直到方法表才由时间安排间接说明；‘错误高置信输出’直到模拟表才获得可操作含义。读者交接明确说明不能假定读者精通所有参与学科。"
    direction: "首次使用时分别写为‘标志时点（landmark）风险集’并给出一句功能定义，以及‘在无真实结构或模型错设时仍给出高置信错误结论’。后文可保留较短形式。"
  - finding_id: LANG-R023-03
    severity: minor
    category: register_and_workflow_language
    section: work_packages_methods_and_required_analyses
    locator: "Research content and work packages 的时间表与阶段 II 判定段；Hospital-primary cross-database validation；Required analyses and evidence"
    excerpt: "G1 审计的硬下限；改锁；准入；严重泄漏未清零；未触碰最终测试区；合取结论表"
    issue: "一组压缩的流程词、直译词和内部简称进入面向研究者的正文。它们虽可从上下文推断，但会使临床与方法学混合读者反复解码，并削弱自然学术中文的连贯性。"
    direction: "改为含义完整的科学表述，例如‘双库数据支持审计的预设最低标准’、‘在拟合前重新预先确定’、‘进入后续分析’、‘解决全部高严重度泄漏问题’、‘封存的外部测试集’和‘全部条件同时满足的结论表’。"
  - finding_id: LANG-R023-04
    severity: minor
    category: concision_and_redundancy
    section: full_dossier
    locator: "一句话摘要、Structured abstract、Research content and work packages、Conditional trial-observation mapping、Evidence chains、Required analyses and evidence、Planned outputs、Limitations 第 8–9 与 12 项"
    excerpt: "只有在阶段 II 完成、试验语义和观测映射合格时才进入 RCT 分支，以及该分支不能补足或验证阶段 II 的近同义说明"
    issue: "同一条件边界以近同义长句在多个段落重复出现，且常与其他限定语堆叠。必要的局部边界应保留，但当前词汇层面的重复已增加阅读负担。"
    direction: "逐段保留完成该段局部功能所需的最短限定，删去不增加新限定的近同义复述；不在语言修订中决定哪些科学条件可被删除。"
  - finding_id: LANG-R023-05
    severity: minor
    category: readability_and_flow
    section: summary_question_and_trial_mapping
    locator: "One-sentence complete-Idea summary；Primary research question；Conditional trial-observation mapping and independent analysis 的‘试验语义与共同锚点资格’和‘测量不变性、校准和绝对投影忠实度’段"
    excerpt: "一句中连续承载研究对象、数据审计、全病程范围、模拟检验、外部检验、条件分支和时间边界"
    issue: "多处句子同时承载四个以上动作、条件或否定边界，主干被分号、并列结构和嵌套条件拉长。信息本身可定位，但首次阅读需要回看句首。"
    direction: "以‘研究拟做什么—如何检验—何时进入条件分支’为顺序拆成短句；方法段按资格、验证、失败后的替代分析分别成句。"
  - finding_id: LANG-R023-06
    severity: minor
    category: mixed_language_and_provenance_wording
    section: work_packages_methods_and_references
    locator: "阶段 II 判定段；方法表与 Key techniques；References 第 3、22–25、38 条"
    excerpt: "本 dossier；ICU stay；bootstrap；delta；partial；本次 v003 未读取 participant-level 工作簿；search-through date"
    issue: "中文正文和参考文献说明中，中英文术语的翻译、大小写和说明方式不统一；第 23、25 条还保留与当前 v021 读者无关的旧版本读取记录。这些写法造成明显的编制过程痕迹。"
    direction: "首次使用时给出一致的中文名称和英文括注，随后统一形式；将‘本 dossier’改为‘本研究方案’；参考文献说明只保留读者理解来源性质所需的信息，用自然中文表述并删除与当前文本无关的旧版本读取记录。"
unresolved_issues:
  - LANG-R023-01
  - LANG-R023-02
  - LANG-R023-03
  - LANG-R023-04
  - LANG-R023-05
  - LANG-R023-06
---

# 学术语言评估报告

**评估编号**：language-assessment-r023  
**目标语言**：简体中文（保留必要的英文缩写与数据库、方法名称）  
**学科**：重症医学与临床流行病学为主要应用领域，涉及纵向统计、系统辨识和医学人工智能  
**目标期刊**：未指定  
**范围**：完整评估 `idea-dossier-I01-001-v021` 中从标题至参考文献的全部读者可见文本。机器 YAML 元数据以及合同固定的标题或字段标签只作为结构支架，不计入语言缺陷；其措辞若进入正文，则纳入评估。  
**评估日期**：2026-07-19

## 总体语言成熟度

**结论**：`major_language_revision`  
**建议**：`revise_language`

文本的语法、正式程度和计划性时态总体可靠，但标题层的核心 RCT 分支名称及其“观测映射”在首次出现时对既定跨学科读者不够明确。这一问题位于标题和一句话摘要，因而触发核心术语的非补偿性门槛。全文还存在流程性压缩词、中英文混用、限定语堆叠和近同义边界反复陈述，需要系统但不涉及研究论证改写的语言修订。

## 六项评分

| 维度 | 分数（1–10） | 判定 |
|---|---:|---|
| 语法与句法 | 9 | 通过 |
| 学术语域与语气 | 7 | 通过 |
| 术语质量与一致性 | 5 | 未通过 |
| 时态与语态规范 | 9 | 通过 |
| 简洁性与冗余控制 | 5 | 临界 |
| 可读性与行文衔接 | 6 | 临界 |

## 非补偿性语言门槛结果

**总体**：未通过

| 门槛 | 状态 | 说明 |
|---|---|---|
| 明确语法错误密度 | 通过 | 未记录明确、无争议且影响句法成立的语法错误；错误密度明显低于每 500 词 3 处的门槛。中文分词未作机械计数。 |
| 学术语域 | 通过 | 全文不以口语为主，也未在两个以上章节形成系统性非正式语域；“清零”“改锁”等属于局部流程化措辞，另列为语言问题。 |
| 术语连贯与可理解性 | **未通过** | 标题核心短语“条件性稀疏 RCT 次要再分析”可能使“稀疏”错误地指向试验本身；一句话摘要中的“观测映射”没有在首次出现时交代输入、输出或功能。根据既定读者基线，这一标题与摘要层问题足以阻止直接交付。 |
| 计划状态下的时态与语态 | 通过 | 研究尚属 Idea；“拟、计划、须、将、若……则……”贯穿方法和产物描述，现有事实与计划动作也基本分开。未见把计划研究系统性写成既成结果。 |

## 已做得较好的语言方面

1. 全文始终把计划产物与已有结果区分开，尤其在结构化摘要中明确写出“以上均为计划产物，而非现有模型或验证结果”。
2. RCT、SOFA、IPCW、MNAR、MAR、ESS、MCSE、ARI、MAE、FDR、CRF、SAP、MI、FWER 等多数缩写在首次使用时给出中英文全称。
3. 因果、预测、生成和随机化比较的用词边界总体稳定，没有在语言层面把预测性描述写成既定因果结论。
4. 表格、编号和条件句使复杂方案仍具有可定位性；方法参数和停止条件通常有明确主语、时间点和动作。

## 具体问题

### 中文学术表达与术语

#### LANG-R023-01｜重大｜标题核心术语与首次定义

- **位置**：标题；“Title, summary, audience, and positioning”的标题与一句话摘要。
- **原文**：“条件性稀疏 RCT 次要再分析”；“试验数据、语义和观测映射均合格”。
- **问题**：“稀疏”在标题中直接修饰 RCT，可能被读为试验设计或随机化本身稀疏；方法部分显示实际含义是重复测量和访视数据稀疏。“次要再分析”也同时叠加了“次要”和“再分析”，不如通行的“二次分析”直接。“观测映射”在一句话摘要首次出现时没有交代从什么映射到什么、用于何种比较。
- **修订方向**：标题可改为“基于稀疏访视数据的条件性 RCT 二次分析”一类直接描述；一句话摘要在首次出现时说明“使用冻结的观测模型，将试验中共同实测的生理指标转换为一维摘要”。具体名称可在不改变研究设计的前提下调整。

#### LANG-R023-02｜轻微｜跨学科核心设计词首次出现过度压缩

- **位置**：“Objectives”第 1 项；结构化摘要“Objective and hypothesis”。
- **原文**：“landmark 风险集”；“错误高置信输出控制标准”。
- **问题**：前者直到方法表才由“每 12 小时设 landmark”获得间接说明，后者直到模拟表才说明其判断对象。两词都参与核心研究问题和设计关系，不能假定所有目标读者已掌握其特定含义。
- **修订方向**：首次写作“标志时点（landmark）风险集”，并用短语说明这是在各预定评估时点尚未发病的人群；将后者展开为“在无真实结构或模型错设时仍给出高置信错误结论的比例”，后文再使用短称。

术语问题的集中核对如下：

| id | 术语或短语 | 定位 | 读者基线 | 问题 | 建议替代表达 | 首次使用说明 | 依据 | 验收标准 |
|---|---|---|---|---|---|---|---|---|
| LANG-R023-01 | 条件性稀疏 RCT 次要再分析；观测映射 | 标题与一句话摘要 | 熟悉重症研究和验证，但不精通所有参与学科 | 修饰关系含混；核心映射无输入、输出和功能说明 | 基于稀疏访视数据的条件性 RCT 二次分析；共同实测指标到一维摘要的冻结映射 | 同句说明使用冻结观测模型把共同实测生理指标转换为一维摘要 | 读者交接；正文后续方法对“稀疏”和映射功能的说明 | 不了解系统辨识或试验映射的临床研究者，仅凭标题与一句话摘要即可说清数据为何“稀疏”、映射使用什么以及产生什么 |
| LANG-R023-02 | landmark 风险集；错误高置信输出 | Objectives；Structured abstract | 不假定详细的纵向统计或模拟研究专长 | 首次出现早于功能说明 | 标志时点（landmark）风险集；在空结构或错设情景中的高置信错误结论 | 分别给出人群构成和错误判断对象 | 读者交接；正文后续操作定义 | 首次出现处无需跳读方法表即可识别术语的对象与作用 |

未检索外部术语来源；上述判断针对首次可理解性和中文修饰关系，不据此断言某一术语在全部文献中不存在。

### 语法与句法

未发现需要单列的明确语法错误。主要句法问题属于句子过长和条件嵌套，见 LANG-R023-05。

### 学术语域与编制过程措辞

#### LANG-R023-03｜轻微｜压缩流程词和直译词进入正文

- **位置**：工作包时间表、阶段 II 判定、跨数据库验证和必需分析。
- **原文**：“G1 审计的硬下限”“改锁”“准入”“严重泄漏未清零”“未触碰最终测试区”“合取结论表”。
- **问题**：这些词在正式程度上并非口语化，但带有内部操作简写或英文直译痕迹。它们跨多个章节出现，使读者需要先还原流程含义再理解科学内容。
- **修订方向**：用完整动作和对象替换，例如“达到双库数据支持审计的预设最低标准”“在拟合前重新预先确定”“符合进入后续分析的条件”“解决全部高严重度泄漏问题”“封存的外部测试集”“全部条件同时满足的结论表”。保留合同固定字段名称，不修改机器元数据。

#### LANG-R023-06｜轻微｜中英文形式和来源说明不统一

- **位置**：阶段 II 判定段、方法表、Key techniques 和参考文献第 3、22–25、38 条。
- **原文**：“本 dossier”“ICU stay”“bootstrap”“delta”“partial”“本次 v003 未读取 participant-level 工作簿”“search-through date”。
- **问题**：有些术语只有英文，有些只有缩写，有些在后文才给中文功能说明；参考文献中的旧版本读取记录属于编制过程痕迹，且与当前 v021 的读者理解无直接关系。
- **修订方向**：首次使用时统一为中文名称加英文括注，后续固定一种形式；“本 dossier”改为“本研究方案”。参考文献说明只保留来源类型、日期和证据层级等读者所需信息，并以自然中文表述。

### 时态与语态

未发现系统性问题。计划动作主要使用“拟、计划、须、将、若……则……”，已有材料和当前状态主要使用“已核验、未核验、尚未生成”，符合计划性 Idea 的时间状态。个别命令式表达出现在操作规程和停止条件中，功能恰当。

### 简洁性与重复

#### LANG-R023-04｜轻微｜同一边界反复以长限定句出现

- **位置**：一句话摘要、结构化摘要、工作包、试验映射、证据链、必需分析、计划产物和限制第 8–9、12 项。
- **问题**：“阶段 II 必须先完成”“试验语义与映射必须合格”“试验分支不能补足或验证阶段 II”在多个位置以近同义方式重复。每处可能承担局部限定作用，但不少句子没有增加新的条件或读者信息。
- **修订方向**：语言修订只删除词汇层面的近同义复述；各段仍保留完成其局部功能所必需的最短边界。是否需要跨章节保留某一科学条件，应由叙事评估而非本报告决定。

### 可读性与行文衔接

#### LANG-R023-05｜轻微｜条件、动作和否定边界堆叠

- **位置**：一句话摘要、主要研究问题、试验语义与共同锚点资格段、测量不变性与投影忠实度段。
- **问题**：一句话摘要连续承载研究对象、数据审计、全病程范围、两类检验、条件分支和 24 个月边界；试验映射段也在单句内叠加授权、来源核验、时间语义、变量资格和禁止项。主干准确，但首次阅读需要回看。
- **修订方向**：按“研究拟做什么—如何检验—满足何种条件后进入试验分支”拆句。方法段分别陈述资格、外部验证、试验内可计算性和失败后的替代分析。

## 语言修订优先级

1. **标题与一句话摘要的核心术语**：先明确“稀疏”修饰的是访视数据，并就地解释观测映射的输入、输出和作用。
2. **目标与核心假设中的首次定义**：为 landmark 风险集和错误高置信结论提供跨学科读者可立即理解的短定义。
3. **自然学术中文**：系统替换“改锁、准入、清零、未触碰、合取”等压缩流程词，并统一中英文术语形式。
4. **限定语和句长**：缩短一句话摘要及试验映射段，删除不增加新信息的边界复述。
5. **参考文献说明**：删除旧版本读取记录等编制痕迹，统一中文来源说明。

## 当前复评状态

不适用。本次是对 v021 当前文本的独立完整评估；未提供匿名问题清单，也未读取任何既往语言评分、决定、报告、旧版 dossier 或修订差异。因此不报告“已解决、仍存在或新增”问题的跨版本比较。

## 评估说明与限制

- 约定集采用中文学术表达规范，并以生物医学／临床研究规范为主；统计、系统辨识和医学人工智能术语按跨学科读者基线评估。未指定期刊，因此未应用期刊特定格式。
- 完整评估了标题、摘要、背景、问题与目标、工作包、数据与材料、研究设计与方法、技术、证据链、必需分析、计划产物、贡献定位、可行性、限制、风险和参考文献中的读者可见语言。
- 机器前置元数据及合同固定的英文标题或字段标签不作为语言错误；只评估这些表达进入正文后的可理解性。
- 未对研究问题、方法可行性、阈值合理性、证据质量、新颖性或科学论证作判断。
- 未进行外部术语检索；术语结论限于当前文本、提供的读者基线以及适用的中文和学科语言规范。
- 评估期间未修改源 dossier，也未读取任务明确排除的任何旧版 dossier、先前语言报告、叙事报告、修订计划、差异报告、保留报告、预检、评估材料、预期发现、测试脚本或运行状态文件。
