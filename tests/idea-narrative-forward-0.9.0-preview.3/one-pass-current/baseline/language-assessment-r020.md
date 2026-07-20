---
review_id: language-assessment-r020
reviewer_skill: academic-language-assessor
reviewer_instance_id: academic-language-assessor-r020-fresh
workflow_id: RID-SEPSIS-CSM-20260717-001
round_id: baseline-r020
input_artifact_ids:
  - idea-dossier-I01-001-v003
  - reader-handoff-forward-001
input_versions:
  - v003
  - v001
files_read:
  - research-skills-openai/AGENTS.md
  - research-skills-openai/skills/academic-language-assessor/SKILL.md
  - research-skills-openai/skills/academic-language-assessor/references/language-assessment-rubric.md
  - research-skills-openai/skills/academic-language-assessor/references/language-hard-gates.md
  - research-skills-openai/skills/academic-language-assessor/references/chinese-academic-language-conventions.md
  - research-skills-openai/skills/academic-language-assessor/references/discipline-language-conventions.md
  - research-skills-openai/skills/academic-language-assessor/references/terminology-review.md
  - research-skills-openai/skills/academic-language-assessor/templates/language-assessment-report.md
  - research-skills-openai/skills/academic-language-assessor/scripts/validate_language_assessment.py
  - tests/idea-test-0.9.0-preview.1/0.9.0-preview.1/03_ideas/nodes/I01-001/dossiers/idea-dossier-v003.md
  - tests/idea-narrative-forward-0.9.0-preview.3/run-001/inputs/reader-handoff.yaml
isolation_mode: fresh_subagent
prior_scores_visible: false
source_edits_performed: false
decision: major_language_revision
findings:
  - finding_id: LANG-R020-001
    severity: major
    category: terminology_consistency
    location: "Title, summary, audience, and positioning，第 1 段；Structured abstract，Objective and hypothesis；Research question；Conditional trial-observation projection and independent fallback"
    summary: "三个核心设计术语组在首次出现时缺少跨学科读者可理解的直接定义。"
  - finding_id: LANG-R020-002
    severity: major
    category: readability_flow
    location: "One-sentence complete-Idea summary；Primary research question；Observational target, anchoring and abstention；Gate R0；Gate R1"
    summary: "多个关键句同时承载对象、条件、程序、阈值、降级和否定边界，主干难以一次识别。"
  - finding_id: LANG-R020-003
    severity: major
    category: concision_redundancy
    location: "Core hypothesis and non-hypotheses；Evidence chains；Required analyses and evidence；Falsification and stop criteria；Interpretation matrix；Title and positioning claim-support table"
    summary: "同一组证据边界、失败后果和禁止性主张在多处近义复现，形成全稿性的冗长模式。"
  - finding_id: LANG-R020-004
    severity: minor
    category: academic_register_tone
    location: "Positioning and contribution frame；Research content and work packages；Key techniques and implementation；Evidence chains；Contribution and evidence ladder"
    summary: "面向读者的正文大量沿用“门、防火墙、封印、闭合、阶梯”等流程隐喻，使学术表述呈现内部治理说明书语气。"
  - finding_id: LANG-R020-005
    severity: minor
    category: terminology_consistency
    location: "Public ICU database roles and G1 audit；Research design and methods；Absolute simulation and semi-synthetic recovery gate；Conditional trial-observation projection and independent fallback"
    summary: "多项跨学科缩写及英文短语未在首次出现处展开，且中英文标签并置方式不统一。"
unresolved_issues:
  - LANG-R020-001
  - LANG-R020-002
  - LANG-R020-003
  - LANG-R020-004
  - LANG-R020-005
---

# Language Assessment Report

**Assessment ID**: language-assessment-r020  
**Target Language**: Chinese  
**Discipline**: 重症医学、临床流行病学、纵向统计、系统辨识、系统科学、医学 AI、转化研究  
**Target Journal**: 未指定  
**Scope**: complete dossier；评估全部读者可见正文、标题、表格与参考文献表达。机器前置元数据仅作为结构背景，不计入读者语言评分。  
**Sections Assessed**: 标题与定位、结构式摘要、背景与依据、研究问题与目标、研究内容与工作包、数据与证据基础、研究设计与方法、关键技术、证据链、必需分析、预期产出与证伪标准、贡献与近邻工作比较、可行性与停止条件、参考文献。  
**Date**: 2026-07-19

---

## Overall Language Readiness

**Level**: major_language_revision

**Recommendation**: revise_language

全文具有明确的学术语气，能持续区分计划、现状与允许主张；主要障碍不是基本语法，而是核心术语首次出现时的可理解性、过密的句法负荷、内部流程隐喻以及跨章节重复。术语门槛不通过，因此在面向所述跨学科读者提交前需要系统性语言修订。

---

## Dimension Scores

| Dimension | Score (1–10) | Severity |
|---|---:|---|
| Grammar & Syntax | 8 | pass |
| Academic Register & Tone | 6 | borderline |
| Terminology Consistency | 4 | fail |
| Tense & Voice Conventions | 9 | pass |
| Concision & Redundancy | 4 | fail |
| Readability & Flow | 4 | fail |

---

## Hard Gate Status

**Overall**: fail

| Gate | Status | Detail |
|---|---|---|
| Grammar error density | pass | 通读未见超过每 500 字词单位 3 处明确语法错误的模式；主要问题是句法负荷而非病句密度。 |
| Academic register | pass | 未见两个以上章节系统使用口语；流程隐喻和说明书式措辞影响语域，但未达到口语化门槛。 |
| Terminology coherence | fail | 三组核心设计术语在摘要、研究问题或核心设计关系中首次出现时不可由目标读者直接识别其指称或功能，适用 Idea dossier 的术语可理解性规则。 |
| Tense systematic violation | pass | 计划性动作、当前证据状态与既有研究陈述总体区分清楚；未见方法或结果时态的系统性错用。 |

---

## Strengths

1. 全文稳定使用“计划”“尚未生成”“条件满足时”等表达，能清楚区分拟议工作与既有结果。
2. 对预测、关联、随机化比较和因果解释的动词强度控制较好，较少出现无依据的宣传性表述。
3. Sepsis-3、SOFA、RCT、MIMIC-IV 和 eICU-CRD 等领域通用名称整体使用一致。
4. 日期门、阈值、降级后果和允许解释多以并列结构呈现，局部信息定位较方便。
5. 中文标点、数字、单位和公式符号总体稳定，未见系统性语法或时态问题。

---

## Specific Issues

### Chinese Academic Clarity

#### LANG-R020-002 — 关键句承载过多逻辑层级

- **位置**：`Title, summary, audience, and positioning` 的 `One-sentence complete-Idea summary`；`Primary research question`；`Observational target, anchoring and abstention` 第 1–3 段；`Gate R0` 与 `Gate R1`。
- **原文摘录**：“本研究计划在 24 个月内……任何分支均不支持真实因果网络、连续动力学、控制或数字孪生主张。”
- **问题**：单句同时引入研究对象、数据条件、阶段安排、验证要求、试验分支、替代端点和禁止性解释。读者需要在完成整句后回溯寻找主干；研究问题及 R0/R1 段落也反复出现同类多层嵌套。
- **修订方向**：每句只承担一个主要功能。先陈述研究对象和主要目标，再分别陈述阶段 II 的检验条件、阶段 III 的条件性分支及主张边界；保留必要限定，但把条件、后果和否定边界拆成相邻短句或项目。
- **严重度**：major

#### LANG-R020-003 — 边界声明与失败后果重复密集

- **位置**：`Core hypothesis and non-hypotheses`、五条 `Evidence chain`、`Required analyses and evidence`、`Falsification and stop criteria`、`Interpretation matrix`、`Title and positioning claim-support table`、`Remaining execution gates`。
- **原文摘录**：“预测好不能挽救恢复、零边或错设失败”“有限更新不能替代零更新”“不支持潜在动力学、转移边、中介、控制或整个系统验证”等表述在多个章节近义复现。
- **问题**：这些边界各自具有科学功能，但相同词串和相同否定序列跨章节高频复现，使主要论述被治理性说明淹没。读者难以辨别哪些是新信息、哪些是既有边界的重申。
- **修订方向**：在不决定科学条件取舍的前提下，先删除同一段或同一表中的近义重复；其余位置使用简短、稳定的边界标签或一句局部提醒。哪些章节保留完整边界应由叙事结构审阅另行决定。
- **严重度**：major

#### LANG-R020-004 — 流程隐喻进入读者正文

- **位置**：`Positioning and contribution frame`、`Twenty-four-month minimum and dated gates`、`Candidate variable-role firewall`、`Evidence chains`、`Key techniques and implementation`、`Contribution and evidence ladder`。
- **原文摘录**：“绝对恢复门”“变量角色防火墙”“医院优先外部封印”“五条证据链分别闭合”“单向证据阶梯”。
- **问题**：“门、防火墙、封印、闭合、阶梯”连续构成内部流程管理隐喻。个别隐喻可帮助组织文本，但密集使用会遮蔽具体的统计判定、数据隔离和证据关系，并使正文接近项目操作手册而非跨学科学术论述。
- **修订方向**：优先改为直接说明，例如“预设判定标准”“变量用途隔离规则”“外部测试数据访问隔离”“证据对应关系”；若保留一个组织性比喻，应在首次出现处立即给出其学术含义，后文不再叠加新的比喻体系。
- **严重度**：minor

### Grammar & Syntax

未发现构成独立、可定位语法错误模式的事项。LANG-R020-002 所述长句主要属于信息组织和可读性问题，而非主谓搭配、成分残缺或语法关系错误。

### Academic Register & Tone

LANG-R020-004 所述内部流程隐喻在多个章节持续出现，使语域偏向项目治理说明。除此之外，全文基本保持正式、审慎的学术语气；未见系统性口语、直接对读者说话或感叹式表达。

### Terminology Consistency

#### LANG-R020-001 — 核心术语首次出现不可直接理解

| id | term_or_phrase | locator | reader_baseline | problem | recommended_replacement | first_use_definition | basis | acceptance_test |
|---|---|---|---|---|---|---|---|---|
| LANG-R020-001a | 绝对模拟恢复门／绝对恢复／假置信门 | 一句摘要；结构式摘要 `Objective and hypothesis`；目标 3；`Absolute simulation and semi-synthetic recovery gate` | 读者了解验证与不确定性，但不应被假定熟悉项目自定义判定标签 | “绝对”修饰对象不明，“恢复门”和“假置信”不是跨学科自然术语；在给出模拟指标前，读者无法判断其检验对象与失败含义 | 预设的模拟恢复与错误高置信输出控制标准 | 首次出现时说明：在预先规定的数据生成情景中，候选模型须达到状态、转移和结构恢复阈值，并在空结构或错设情景中避免高置信错误；否则降级 | 读者基线与正文后续表格所给的实际功能 | 不查看后文阈值表，目标读者也能说明该标准检验什么以及失败会导致什么 |
| LANG-R020-001b | 冻结观测投影门／投影可观测状态摘要 | 一句摘要；结构式摘要 `Approach` 与 `Contribution and impact`；主研究问题；目标 4 | 读者了解观察性与干预性证据，但不应被假定熟悉全部系统辨识符号 | 术语在核心摘要和问题中先出现，至方法后段才说明它是由阶段 II 观测模型和试验实测共同指标计算的低维摘要；“投影可观测”还可能被读成对潜状态本身的直接观测 | 由冻结观测模型和试验共同实测指标计算的低维状态摘要 | 首次出现时明确数据来源、摘要维度、冻结含义以及它不等同于潜在状态本身 | 读者基线与后文 `Frozen deterministic mapping` 的定义 | 读者在摘要处即可回答该摘要由什么计算、表示什么、不表示什么 |
| LANG-R020-001c | death-ranked SOFA／death-ranked 投影摘要／trial-specific independent secondary clinical-state reanalysis | 一句摘要；结构式摘要 `Expected result`；`Automatic independent fallback`；`Planned outputs` | 临床读者熟悉 SOFA，但跨学科读者未必熟悉死亡分层排序端点及其英文命名 | 首次出现只给出英文压缩标签，排序规则和与阶段 II 的独立关系延后数个章节；同一分支又以数个中英文名称出现 | 按死亡、住院期摘要及存活出院状态分层排序的试验特异性次要临床状态分析 | 首次出现时简述三层排序，并明确这是投影失败后的独立分析，不用于验证阶段 II 表征 | 读者基线与后文 `Automatic independent fallback` 的直接说明 | 全文采用一个中文主名称；英文仅在首次出现时作为补充，且读者无需跳转即可理解排序与证据边界 |

#### LANG-R020-005 — 缩写和中英文标签未按跨学科读者基线展开

- **位置**：`Public ICU database roles and G1 audit` 至 `Research design and methods`，以及 RCT 投影与分析段落。
- **原文摘录**：“G1”“CIF”“MNAR”“MAR”“ESS”“ARI”“MAE”“FDR”“CRPS”“NMAE”“MI”“FAS”“PPS”“mITT”“FWER”，以及 “zero update / zero-update”“fallback”“prediction-only”“pass/fail”。
- **问题**：部分缩写在单一学科内常见，但目标读者横跨临床、统计、系统辨识与医学 AI，不能假定掌握每一领域的缩写。若干英语流程标签还以空格、连字符或中文译名交替出现。
- **修订方向**：每项非通用缩写在读者正文首次出现时给出中文名称及英文全称，随后只保留一种形式；为零更新、有限更新、替代分析等核心操作选择稳定的中文主名称。公式符号和数据库正式名称可保留。
- **严重度**：minor

### Tense & Voice Conventions

未发现可定位的系统性问题。计划动作主要使用“计划、须、将、才可”等表达，当前未完成状态主要使用“尚未、未提供、待执行”，既有研究使用完成性陈述，三者区分明确。

### Conciseness & Redundancy

主要问题见 LANG-R020-003。另有多处限定语堆叠，例如“一维阶段 II 状态投影”“条件性、次要、访视特异的随机化再分析”“计划性真正外部检验”等。修订时应检查每个修饰语是否在本句承担唯一信息；必要限定应保留，但应避免把证据状态、时间、数据来源、分析层级和否定边界全部压入同一名词短语。

### Readability & Flow

主要问题见 LANG-R020-002。全文宏观章节顺序清楚，但段内经常从研究对象直接跳至判定标准、替代分支和禁止解释，缺少短句式的主题引导。尤其在摘要、研究问题、观测目标与 RCT 投影段落中，应先让读者识别“研究什么”，再说明“在何种条件下如何检验”，最后说明“结果不能支持什么”。

---

## Language Revision Priorities

1. **术语可理解性**：3 组核心术语问题——在标题后摘要、研究问题和核心设计关系的首次出现处，改用直接描述并给出一句定义；统一投影通过与独立替代分析的名称。
2. **可读性与句法负荷**：5 类高负荷位置——拆分一句摘要、研究问题、观测目标、R0 和 R1，使每句只承担一个主要逻辑功能。
3. **简洁性与重复**：6 个以上章节反复出现同类边界——先处理段内和表内近义重复，再由叙事审阅决定完整边界的权威位置。
4. **学术语域**：多处内部流程隐喻——改为统计判定、数据隔离或证据关系的直接学术表述。
5. **跨学科术语格式**：多项缩写和英语流程标签——首次展开并统一中文主名称、英文全称、缩写与连字符形式。

---

## Re-Assessment Status

不适用。本次为全新隔离的基线评估，未提供也未读取匿名问题清单或既往语言评估。

---

## Assessment Notes

- 本报告只评估学术语言，不判断研究设计的科学有效性、可行性、新颖性、影响力、期刊适配性或文献事实准确性。
- 评估采用生物医学/临床研究与计算机科学、AI、工程交叉约定；未指定期刊，因此没有施加期刊特有格式。
- 参考文献仅检查其作为全文组成部分的语言与格式一致性，未核验引文内容。
- 机器前置元数据、固定字段名和公式符号不作为读者语言错误；只有进入标题、摘要、正文、表格或图式说明的内部标签才计入问题。
- 术语判断以给定读者基线和 dossier 中后续可见定义为依据；对于不自然或难以核验的压缩标签，优先建议直接描述，而不另造新术语。
- 全文已完整读取；未修改源 dossier。
