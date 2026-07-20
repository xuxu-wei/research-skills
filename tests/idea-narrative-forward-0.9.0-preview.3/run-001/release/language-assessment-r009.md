---
review_id: language-assessment-I01-001-r009
reviewer_skill: academic-language-assessor
reviewer_instance_id: fresh-language-assessor-r009
workflow_id: RID-SEPSIS-CSM-20260717-001
round_id: r009
input_artifact_ids:
  - idea-dossier-I01-001-v011
  - reader-handoff-forward-001
input_versions:
  - v011
  - v001
files_read:
  - path: AGENTS.md
    sections: complete file
  - path: research-skills-openai/AGENTS.md
    sections: complete file
  - path: research-skills-openai/skills/academic-language-assessor/SKILL.md
    sections: complete file
  - path: research-skills-openai/skills/academic-language-assessor/references/language-assessment-rubric.md
    sections: complete file
  - path: research-skills-openai/skills/academic-language-assessor/references/language-hard-gates.md
    sections: complete file
  - path: research-skills-openai/skills/academic-language-assessor/references/chinese-academic-language-conventions.md
    sections: complete file
  - path: research-skills-openai/skills/academic-language-assessor/references/discipline-language-conventions.md
    sections: complete file; Biomedical / Clinical Research, Social Sciences, General Science, and cross-cutting rules applied
  - path: research-skills-openai/skills/academic-language-assessor/references/terminology-review.md
    sections: complete file
  - path: research-skills-openai/skills/academic-language-assessor/templates/language-assessment-report.md
    sections: complete file
  - path: tests/idea-narrative-forward-0.9.0-preview.3/run-001/inputs/reader-handoff.yaml
    sections: complete file
  - path: tests/idea-narrative-forward-0.9.0-preview.3/run-001/release/idea-dossier-v011.md
    sections: complete dossier, including title through references; machine frontmatter treated as non-reader-facing scaffolding
isolation_mode: fresh_subagent
prior_scores_visible: false
source_edits_performed: false
decision: major_language_revision
findings:
  - id: LANG-001
    severity: major
    category: academic_register
    locator: Title and positioning claim-support table, lines 415-426
    summary: Reader-facing prose exposes English status codes and document-control language instead of using only natural scientific Chinese.
  - id: LANG-002
    severity: major
    category: readability
    locator: Authoritative limitations / 尚待冻结的方法规范 and Current feasibility and evidence status, lines 432-451
    summary: The two-item pending-specification list and the later broader list do not give readers one complete account of what remains to be specified.
  - id: LANG-003
    severity: major
    category: concision
    locator: Structured abstract lines 60-64; Hospital-based cross-database validation lines 246-255; Operational thresholds lines 469-489
    summary: Repeated qualifier chains and multiple conditions within single sentences create sustained processing burden across sections.
  - id: LANG-004
    severity: minor
    category: readability
    locator: dated milestones line 123; hospital-based validation line 246; analysis targets line 289
    summary: Several sentences or labels have unclear modifier scope or imperfect parallelism despite remaining interpretable.
  - id: LANG-005
    severity: minor
    category: chinese_english_consistency
    locator: milestones and work packages lines 121 and 135; simulation line 242; feasibility lines 450 and 460
    summary: Monte Carlo and D-dimer appear in English forms without a consistent Chinese-first bilingual introduction.
unresolved_issues:
  - LANG-001
  - LANG-002
  - LANG-003
  - LANG-004
  - LANG-005
---

# 学术语言评估报告

**评估编号：** language-assessment-I01-001-r009  
**目标语言：** 中文（简体）  
**学科：** 重症医学与临床流行病学，涉及纵向统计、系统辨识和医学人工智能  
**目标期刊：** 未指定  
**范围：** 完整构想 dossier 的读者可见文本，包括标题、摘要、研究背景、问题与目标、工作包、数据与方法、证据链、预期产物、贡献定位、可行性与停止条件、参考文献。机器 frontmatter 与合同固定的英文标题或字段标签仅作为结构，不计入正文语言评分；但由这些结构进入正文或表格的状态代码计入评估。  
**目标读者基线：** 可假定读者熟悉重症研究、纵向临床数据、验证、不确定性及观察性与干预性证据的区别；不假定其熟悉项目内部词汇、新造标签或全部交叉学科细节。  
**日期：** 2026-07-18

## 总体语言就绪度

**等级：** `major_language_revision`  
**建议：** `revise_language`

全文语法稳定，核心概念大多在首次使用附近获得解释，且没有触发任何语言硬门槛。当前不能进入语言就绪状态，主要原因不是科学术语错误，而是三种跨章节模式共同增加阅读负担：读者可见的英文状态代码和文档控制措辞、限定语与前置条件反复叠加，以及待明确方法规范的范围在两个相邻位置表述不一致。这些问题需要系统性语言修订，但不要求替作者选择任何尚未确定的科学或统计方案。

## 维度评分

| 维度 | 得分（1–10） | 判定 |
|---|---:|---|
| 语法与句法 | 8 | 通过 |
| 学术语域与语气 | 7 | 通过 |
| 术语质量与一致性 | 7 | 通过 |
| 时态与语态惯例 | 9 | 通过 |
| 简洁性与冗余 | 5 | 临界 |
| 可读性与连贯性 | 6 | 临界 |

## 语言硬门槛

**总体：** 通过

| 门槛 | 状态 | 依据 |
|---|---|---|
| 明确语法错误密度 | 通过 | 通读未发现达到每 500 个词语单位 3 个以上的明确语法错误；所见问题主要是搭配、修饰范围和句法负荷，而非语法错误。 |
| 非正式语域 | 通过 | 未见两个以上章节系统使用口语、感叹、直接对读者说话或修辞问句；问题是文档控制语域，不是口语化。 |
| 术语连贯性 | 通过 | 未发现 3 个以上核心概念被无理由地用多套名称指代；“共同观测指标”“共同生理锚点”等相邻名称已说明不同层级。 |
| 时态系统性违规 | 通过 | 本文为前瞻性研究构想，计划、条件和拟生成结果的表述总体一致；没有把拟开展工作写成已经完成的结果。 |

## 优点

1. 标题中的“候选动态系统模型”采用可理解的描述性名称，并在“跨学科概念桥”中立即说明其表示对象和变量角色；没有依赖新造隐喻。
2. “状态占用概率”“共同生理锚点预测”“状态对齐”“预设结构稳定性”“观测映射”和“一维状态摘要”均在首次出现附近或紧随其后的段落中给出读者可识别的含义。后续公式属于渐进补充，而不是用公式替代初始解释。
3. 对因果、预测、模型恢复、外部验证和随机试验组间比较的证据强度区分明确，未使用“重大突破”“首次”等宣传性措辞。
4. 缩略语 CIF、IPCW、ARI、MCSE 等均有全称或语境说明；SOFA 和 Sepsis-3 的引入也符合重症医学文本惯例。
5. “尚待冻结的方法规范”中列出的两项内容本身表述清楚：每项都区分了待确定部分、已经固定的数量或判定方向，以及必须完成确定的时间点。语言修订不应替作者选择医院规模指标或置信限构造。

## 具体问题

### 中文学术表达清晰度

#### LANG-001：读者可见文本暴露状态代码和文档控制措辞

- **位置：** “Title and positioning claim-support table”，第 417–426 行；相关措辞还见“Required analyses and evidence”，第 356–367 行。
- **原文示例：** “获得支持（`supported`）”“限定支持（`qualified`）”“无可主张增量（`none`）”；“交付验收须包含”“阶段 II 证据核对表”。
- **严重度：** major
- **类别：** 学术语域、内部工作词汇泄漏
- **问题：** 中文名称已经足以表达证据状态，紧随其后的英文代码值不增加科学含义，却使正文呈现为内部状态记录。后段密集使用“验收记录”“审计包”“签署”等项目控制措辞，也使科学要求与内部管理动作混在同一语域中。机器 frontmatter 和合同固定英文标题不属于本 finding；这里仅针对进入读者可见表格与正文的表达。
- **修订方向：** 在读者可见内容中只保留自然中文的证据状态；把“验收”“签署”等改写为可观察的科学产物或核验要求，例如说明需报告什么、由谁独立核验以及何种证据构成完成。不要改动合同固定标题或 frontmatter 字段。
- **验收标准：** 标题、摘要、正文和表格中不再出现裸露的状态代码；研究者可仅凭自然中文理解每一证据状态和核验要求。

#### LANG-002：待明确方法规范的范围没有形成一份完整、对应的说明

- **位置：** “尚待冻结的方法规范”，第 434–437 行；“Current feasibility and evidence status”，第 448 行。
- **原文示例：** 前一处只列“医院规模分层指标”和“主要临床任务的 95% 上置信限构造”；后一处另列“临床尺度到模拟参数的映射、多类别校准估计量、95% 上置信限构造和阈值登记表”。
- **严重度：** major
- **类别：** 可读性、待明确事项表述
- **问题：** 读者无法判断“尚待冻结的方法规范”是否是完整清单，也无法从后一处得知另外三类事项各自究竟待确定什么、哪些量已经固定、何时以及依据什么完成确定。这里的问题是待明确事项的表达范围不清，不是要求评估者确定方法。
- **修订方向：** 用一份统一清单逐项写明：（1）尚待确定的具体对象；（2）已固定且不得因外部结果改变的数量、方向或边界；（3）允许作出决定的时间点与可用信息；（4）未按时确定时如何报告或停止。若某项只是材料名称而不是独立方法选择，也应明确说明。
- **验收标准：** 相邻两处列出的待明确事项一一对应；读者无需推断即可识别全部待确定项及其决定边界，同时文本不替作者选定任何方案。

#### LANG-003：限定语和前置条件跨章节重复堆叠

- **位置：** “Structured abstract”第 60–64 行；“Hospital-based cross-database validation”第 246–255 行；“Operational thresholds, alternatives, and stop conditions”第 469–489 行。
- **原文示例：** “预先设定”“预先隔离”“未参与开发”“冻结”“不更新模型”“只有……才……”在同一段或相邻句中多次成组出现；外部验证段落把分层条件、确定时间、结局隔离和数据保管责任压入同一句。
- **严重度：** major
- **类别：** 简洁性、可读性
- **问题：** 这些条件多数有科学或治理功能，但反复使用完整限定链会遮蔽每句的主要动作。问题不是某项条件是否应保留，而是条件在句内的层级和重复形式使跨学科读者需要多次回读。
- **修订方向：** 每段先陈述一个主要动作，再以短句列出时间边界、数据隔离和失败后果；对已经定义的中性概念使用稳定简称。仅合并词语重复，不判断不同位置的科学条件是否可删除，也不规定哪些推理位置必须保留限定。
- **验收标准：** 每个长句原则上只承担一个主要动作和一组直接条件；所有原有科学边界仍可定位，但读者不必解析连续三层以上的前置限定。

#### LANG-004：局部修饰范围和标签所指不够准确

- **位置与原文：**
  - 第 123 行：“第二数据库中不更新模型的验证结果，以及只使用适配数据进行再校准或观测层更新的结果；聚类不确定性、状态对齐，以及……分层分布图”。
  - 第 246 行：“按具体定义尚未冻结的医院规模指标四分位和接口完整性分层”。
  - 第 289 行：“主要变量按以下顺序定义”，随后实际说明的是结局状态的排序规则。
- **严重度：** minor
- **类别：** 句法、可读性
- **问题：** 第 123 行的并列项层级不齐；第 246 行中“尚未冻结”究竟修饰“指标”还是“具体定义”需要回读；第 289 行“主要变量”不能准确概括死亡、住院摘要和存活出院的有序组合。
- **修订方向：** 把不同层级的产物改为平行列项；将“尚未确定的是指标的具体定义”单独成句；用直接描述排序对象的标签替代泛称“主要变量”。
- **验收标准：** 每个修饰语只有一个明确被修饰对象，表格或段落标签与随后定义的对象一致。

#### LANG-005：少数中英文术语未采用一致的中文首次引入方式

- **位置：** 第 121、135、242、450、460 行。
- **原文示例：** “Monte Carlo 与半合成模拟”“Monte Carlo 标准误”“D-dimer 单位仍待核验”。
- **严重度：** minor
- **类别：** 中英文一致性
- **问题：** “Monte Carlo”在前部工作包中先以英文出现，到模拟方法段仍未给出中文名称；“D-dimer”也与中文医学正文的常见中文名称不一致。对统计或临床单一领域读者，这通常不妨碍理解；对本文规定的跨学科读者，中文首次引入更自然。
- **修订方向：** 首次写作“蒙特卡洛（Monte Carlo）模拟”和“蒙特卡洛标准误（MCSE）”；若 `D-dimer` 不是必须原样保留的数据字段名，则首次写作“D-二聚体（D-dimer）”，后文统一一种形式。若它是原始字段名，应明确标注为字段名而非正文术语。
- **验收标准：** 同一术语只在首次出现时给出中英文对应，后续形式一致；数据库字段名与正文科学术语能够区分。

### 语法与句法

未发现影响理解的明确语法错误模式。LANG-004 所列问题属于修饰范围、并列层级与标签精度，不构成语法硬门槛失败。

### 学术语域与语气

除 LANG-001 外，全文保持正式、审慎的研究构想语气。没有口语、直接称呼读者、感叹句或宣传性断言。LANG-001 应通过将项目控制词转换为科学核验要求来修订，而不是提高主张强度。

### 术语质量与一致性

普通阅读对以下核心术语触发了定向检查，结果均通过：

| 核心术语 | 定位 | 读者基线 | 检查结果 | 依据 | 验收标准 |
|---|---|---|---|---|---|
| 候选动态系统模型 | 标题；第 48 行 | 重症、流行病学、纵向统计、系统辨识和医学人工智能交叉读者 | 通过 | “动态系统模型”是描述性语义中心；第 48 行立即说明患者状态随时间变化与转移，并区分治疗和测量信息 | 首次解释继续保留，且不改成新造隐喻 |
| 状态占用概率 | 第 48、60、220 行 | 同上 | 通过 | 首次出现即说明为指定时点处于各状态的概率，并与观察频率区分 | 后文持续保持与“观察到的状态比例”的区别 |
| 观测映射／一维状态摘要 | 第 50、224、269–289 行 | 同上 | 通过 | 第 50 行已说明其输入、功能和数值方向；后续公式属于渐进细化 | 首次说明继续包含输入、用途和方向；不要求在摘要中提前给出完整公式 |

未发现需要外部核验的可疑新造核心术语，因此没有开展全面术语表或外部术语检索。当前术语问题为 `none`；LANG-005 是中英文引入方式问题，不是核心术语的语义失真。

### 时态与语态惯例

全文按研究构想使用“计划”“拟”“将”“若……则……”等表达，并把当前证据、计划产物和未来结果分开。未见方法或结果章节的系统性时态误用。中文主动和无主句式的搭配总体符合临床与统计研究计划文本惯例。

### 简洁性与冗余

主要问题见 LANG-003。全文多次完整复述阶段 II 成功、外部数据隔离、冻结时点和阶段 III 条件。评估只确认词语重复与限定堆叠造成语言负担；不同章节中的科学条件是否具有各自必要的论证功能，不属于本次语言评估。

### 可读性与连贯性

章节依赖关系总体清楚，三阶段导航和证据类型区分对读者有帮助。可读性下降主要发生在长表格前后的高密度条件句、外部验证分组规则和停止条件。LANG-002、LANG-003 与 LANG-004 修订后，跨学科读者应能更快分辨“已固定内容”“尚待明确内容”“触发条件”和“后果”。

## 语言修订优先级

1. **学术语域：** 1 项 major——移除读者可见的英文状态代码，把内部验收措辞改为自然的科学核验表述。
2. **待明确事项的清晰度：** 1 项 major——合并并对齐全部待确定方法事项，逐项说明已固定内容、决定时点与未完成后果，不选择方案。
3. **简洁性与可读性：** 1 项 major——重组限定链和长条件句，同时完整保留科学边界。
4. **局部句法与标签精度：** 1 项 minor——修复并列层级、修饰范围和“主要变量”等泛称。
5. **中英文一致性：** 1 项 minor——统一“蒙特卡洛”和“D-二聚体”的首次双语引入。

## 复评状态

本次不是基于匿名问题清单的复评；未读取任何既有语言报告、既有评分、修订差异或工作状态。

| 检查 | 当前评估 |
|---|---|
| 已不再出现的既列问题 | 不适用 |
| 仍存在的既列问题 | 不适用 |
| 当前文本中新记录的问题 | 5 项：LANG-001 至 LANG-005 |

## 评估说明与限制

- 本报告只评估学术语言、术语可理解性、限定语密度、中英文一致性、读者知识基线和读者可见的内部工作词汇；不判断方法、阈值、估计量、样本量、模型结构、因果解释或随机试验分析选择是否科学正确。
- 对第 436–437 行明确保留待确定的医院规模指标和 95% 上置信限构造，本报告不选择方案；只评价其待明确状态是否清楚。对第 448 行新增但未逐项解释的待确定内容，也仅要求写清决定对象和边界。
- 英文合同标题、frontmatter 字段、数学符号和代码标识作为结构处理，没有因其本身是英文而记为正文语言问题。
- 未读取任何 prior dossier、修订差异、受保护内容登记、内容保留报告、叙事评估、预检报告、旧语言报告或工作状态文件；结论仅基于本报告 frontmatter 所列文件。
- 未改动评估对象或其他源文件。
