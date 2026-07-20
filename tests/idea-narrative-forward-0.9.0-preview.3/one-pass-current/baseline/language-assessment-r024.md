---
review_id: language-assessment-r024
reviewer_skill: academic-language-assessor
reviewer_instance_id: fresh-raw-language-r024
workflow_id: RID-SEPSIS-CSM-20260717-001
round_id: baseline-r024
input_artifact_ids:
  - idea-dossier-I01-001-v003
  - reader-handoff-forward-001
input_versions:
  - v003
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
  - tests/idea-test-0.9.0-preview.1/0.9.0-preview.1/03_ideas/nodes/I01-001/dossiers/idea-dossier-v003.md
  - tests/idea-narrative-forward-0.9.0-preview.3/run-001/inputs/reader-handoff.yaml
isolation_mode: fresh_subagent
prior_scores_visible: false
source_edits_performed: false
decision: major_language_revision
findings:
  - finding_id: L-R024-01
    severity: major
    category: terminology
    locator: 标题、One-sentence complete-Idea summary、Objective 4
    summary: “稀疏”在标题中按常规句法修饰 RCT，而正文意图是说明试验访视或重复测量稀疏；“随机化再分析”还可能被误解为重新随机化。
  - finding_id: L-R024-02
    severity: major
    category: terminology
    locator: 标题、One-sentence complete-Idea summary、Structured abstract、Primary research question
    summary: 核心研究对象在“候选动态系统表征”“候选全病程表示”和“候选模型”之间变化，首用处没有用跨学科读者可直接理解的语言说明其指称和功能。
  - finding_id: L-R024-03
    severity: major
    category: terminology
    locator: One-sentence complete-Idea summary、Conditional trial-observation projection、Evidence chains
    summary: “投影可观测状态摘要”“随机化扰动”和“death-ranked SOFA”等核心输出名称在首用处不透明，且后文又改称“可观测代理”等近义名称。
  - finding_id: L-R024-04
    severity: major
    category: register_and_terminology
    locator: 全文多节，尤见日期门、G1 审计、外部检验、RCT 分支和定位表
    summary: 大量流程标签、英文状态词、未展开缩写和中英混合短语进入读者正文，超过所给跨学科读者的共同知识基线。
  - finding_id: L-R024-05
    severity: major
    category: readability
    locator: One-sentence complete-Idea summary、Primary research question、Gate R0–R1 段落
    summary: 多个核心入口句同时承载研究对象、数据条件、阶段条件、替代分支和禁限主张，修饰层级过多，读者难以一次确定主干。
  - finding_id: L-R024-06
    severity: minor
    category: concision
    locator: Core hypothesis and non-hypotheses、Evidence chains、Interpretation matrix、Contribution、Falsification、Risk matrix
    summary: 关于不能据此声称因果网络、控制、数字孪生或整体模型验证的限定近似逐字重复，且“候选、条件性、计划性、次要、有限”等限定经常叠加。
  - finding_id: L-R024-07
    severity: minor
    category: syntax_and_register
    locator: 标题及全文多处
    summary: “计划跨数据库检验”“真正未触碰”“按门实施”“救回/挽救”“防火墙”“证据阶梯”等表达含有名词堆叠、直译、口语化动词或不必要隐喻。
unresolved_issues:
  - L-R024-01
  - L-R024-02
  - L-R024-03
  - L-R024-04
  - L-R024-05
  - L-R024-06
  - L-R024-07
---

# Language Assessment Report

**Assessment ID**: language-assessment-r024  
**Target Language**: Chinese（zh-CN）  
**Discipline**: 重症医学与临床流行病学为主要应用领域，结合纵向统计、系统辨识、系统科学和医学 AI  
**Target Journal**: 未指定  
**Scope**: 原始 Idea dossier 的全部读者可见内容，包括标题、摘要、研究背景、问题与目标、研究内容、数据与证据基础、设计与方法、技术实现、证据链、预期产出、解释边界、贡献定位、风险与停止条件及参考文献；机器前置字段和固定合同字段不纳入正文语言评分  
**Sections assessed**: 全文所有读者可见章节  
**Date**: 2026-07-19

---

## Overall Language Readiness

**Level**: major_language_revision

**Recommendation**: revise_language

全文的计划性时态和基本句法总体稳定，但标题中存在会改变研究对象理解的修饰歧义，多个核心术语在首用处不能让所设跨学科读者直接识别指称或功能。正文还大量保留项目流程标签、英文状态词和未展开缩写，并在重要入口句中堆叠过多条件。因而当前文本需要系统性的语言修订，而不是局部校对。

---

## Dimension Scores

| Dimension | Score (1–10) | Severity |
|---|---:|---|
| Grammar & Syntax | 7 | pass |
| Academic Register & Tone | 5 | borderline |
| Terminology Consistency | 3 | fail |
| Tense & Voice Conventions | 9 | pass |
| Conciseness & Redundancy | 4 | fail |
| Readability & Flow | 4 | fail |

---

## Hard Gate Status

**Overall**: fail

| Gate | Status | Detail |
|---|---|---|
| Grammar error density | pass | 未见超过阈值的明确语法错误；按完整正文句估计不高于 2 处/500 个中文词语单位，表格中的体例性短语不按残句计 |
| Academic register | pass | 正文主导语体仍为正式学术语体；流程化措辞和中英混排广泛存在，但没有两个章节达到以口语表达为主的硬门阈值 |
| Terminology coherence | fail | 至少 3 个核心名称在标题或摘要首用时具有误导性或不可直接理解：“条件性稀疏 RCT 次要再分析”“候选动态系统表征”“投影可观测状态摘要/随机化扰动” |
| Tense systematic violation | pass | 作为计划性 Idea，拟开展的工作主要使用“计划、须、若、将、才”等前瞻或条件表达；没有把尚未实施的研究系统写成既成结果 |

术语硬门失败限制了整体结论。其余维度的低分用于说明修订范围，并不构成额外硬门失败。

---

## Strengths

1. 对既有事实、当前资源状态、计划行动和条件性输出大体作了语言上的区分；“计划交付”“尚未生成”“若执行成功”等表述与 Idea 阶段相符。
2. 预测、观察性关联、随机分组比较和因果机制之间的主张边界多处使用明确否定句表达，没有用完成时态暗示模型已经建立或验证。
3. 标题层级和表格定位充分，绝大多数问题可以准确定位到章节、段落或表格行。
4. 在方法正文中，生理测量、治疗行动、测量过程和标签的角色最终得到显式区分，为采用更直接、更稳定的核心术语提供了基础。

---

## Specific Issues

### Chinese Academic Clarity

#### L-R024-01 — 标题修饰关系指向错误（major）

- **位置**：标题；“One-sentence complete-Idea summary”；Objective 4。
- **原文**：“条件性稀疏 RCT 次要再分析”。
- **问题**：按普通中文名词短语的就近修饰规则，“稀疏”首先修饰“RCT”，容易被理解为试验本身稀少或设计稀疏；后文实际说明的是 D7/D8 等访视及重复测量稀疏。“随机化再分析”也可能被理解为再次随机分配，而正文意图是利用原随机分组开展次要分析。该歧义出现在标题中，直接影响研究组成的识别。
- **修订方向**：显式写出“稀疏”的承载对象，例如“基于稀疏访视数据的条件性 RCT 次要分析”；将“随机化再分析”改为“基于随机分组的次要分析”或同等明确表述。标题和摘要应采用同一名称。
- **验收标准**：不了解项目内部命名的读者只读标题即可判断“稀疏”指访视/测量数据，且不会把分析理解为重新随机化。

#### L-R024-02 — 核心研究对象首用定义不足且名称漂移（major）

- **位置**：标题；完整 Idea 单句摘要；Structured abstract 的 Objective and hypothesis；Primary research question；全文后续“表征/表示/模型”用法。
- **原文**：“脓毒症全病程候选动态系统表征”“知识约束、不确定性感知候选动态系统表征”“候选全病程表示”。
- **问题**：“动态系统表征”的语义中心是“表征”，但临床读者无法从标题判断它是患者状态模型、变量表示、生成模型还是对真实系统的描述。“候选”究竟修饰“动态系统”还是“表征”也不够稳定。单句摘要继续叠加“知识约束、不确定性感知”，没有及时说明该对象用什么信息描述什么随时间变化的对象、产生何种输出。后文又在“表征”“表示”“模型”之间切换。
- **修订方向**：确定一个跨学科可理解的主名称；如保留“表征”，应在摘要首次出现时用一个短同位语说明其功能，例如它是“分别描述患者生理状态、治疗行动和测量过程随时间变化的候选模型”。“不确定性感知”宜改成可观察的动作表述，如“显式量化不确定性”。
- **验收标准**：目标读者在首次出现处即可回答该术语指什么、描述什么对象、用于何种分析；全文不再以“表征/表示/模型”无标记互换同一核心概念。

#### L-R024-03 — RCT 核心输出名称在首用处不可解（major）

- **位置**：完整 Idea 单句摘要；Structured abstract 的 Expected result 和 Contribution and impact；Primary research question；Gate R0–R1；Projection-pass estimand。
- **原文**：“投影可观测状态摘要”“投影可观测摘要的有限随机化扰动”“death-ranked SOFA 临床状态再分析”；后文又使用“RCT 可观测代理 P_obs”。
- **问题**：“投影”“可观测”“状态”“摘要”连续堆叠，读者无法在摘要中判断被投影的对象、投影所得量以及该量在试验中的作用。“随机化扰动”可能指随机噪声、干预导致的动力学扰动或随机分组差异。英文 “death-ranked” 首用时没有解释排序规则。其详细定义推迟到方法中，超过了核心输出术语应在首用处可识别的要求。
- **修订方向**：首用处先用描述性名称，例如“由阶段 II 模型映射到试验实际访视指标的一维综合评分”；将“随机化扰动”改为“随机分组间差异”或与预定估计量一致的标准表达；首次使用 death-ranked SOFA 时直接说明死亡、在院存活和存活出院的排序。随后再引入唯一、稳定的简称。
- **验收标准**：只读摘要的读者能够说明分析比较的具体量及组间比较的含义，且不会把它理解为潜在动力学受到验证。

#### L-R024-04 — 项目流程词和未定义中英混合表达广泛进入正文（major）

- **位置**：Positioning；日期门和合取成功定义；G1 审计表；跨库检验；RCT 两级分支；证据链；定位支持表；风险矩阵；Identity and final stop boundary。
- **代表性原文**：“绝对恢复门”“假置信门”“按门实施”“data-access no-go”“zero update”“adaptation-only observation-layer update”“projection-pass”“fallback”“supported/qualified/unsupported”“new_idea_required”。同时，DUA、CRF、SAP、CIF、IPCW、ARI、FDR、ESS、SVD、NMAE、MCSE、mITT、MI、FWER、CRPS 等缩写多未在首次出现处展开。
- **问题**：这些词有的属于内部决策或状态标签，有的是未经翻译的英文短语，有的是某一参与学科内常用但不能由全部目标读者共同假定的缩写。它们与中文句法混合后，使读者需要先还原项目内部流程，才能理解研究计划。固定机器字段可保留，但这里的问题发生在正文、表格、标题和图表预定标签中。
- **修订方向**：正文优先使用直接描述，例如“预设判定标准”“未达到标准时改用……”“预先隔离的最终测试集”“仅用适配数据更新校准参数”；必须保留的英文术语或缩写在首次出现时给出中文名称、英文全称和缩写，之后只用一种形式。将内部状态值留在机器字段或附录映射表中，不让其承担正文论述。
- **验收标准**：每个缩写在首次读者可见处可展开；正文不依赖 no-go、fallback、pass、supported、new_idea_required 等内部标签才能成立；同一概念的中英文形式保持一致。

#### L-R024-05 — 核心入口句负载过高（major）

- **位置**：完整 Idea 单句摘要；Primary research question；Gate R0、Frozen deterministic mapping、Gate R1 段落。
- **原文特征**：单句摘要把 24 个月目标、两类数据源、四段病程、两类判定标准、阶段 I–III、两个 RCT、投影成功与失败分支及六类禁限主张压入一个句子；研究问题也在一个问句中嵌入三层编号与条件分支。
- **问题**：主语和主要动作被连续的介词结构、条件从句和并列限定隔开。读者必须在看到句末后回读，才能确定阶段 II 的主要目标与阶段 III 的附加分析。方法段落中的公式可以保留精确性，但公式前后的说明同样需要先给语义主干。
- **修订方向**：把单句摘要限定为“研究对象—主要动作—主要输出”，把阶段 III 条件分支和禁限主张分成后续短句；研究问题可保留三项子问题，但先给出一句总问题。每个 RCT 判定标准段先用一句话说明目的，再列条件。
- **验收标准**：标题后的首段不需回读即可区分阶段 II 主研究与阶段 III 条件性附加分析；单句不同时承担超过一个主要条件分支。

### Grammar & Syntax

未见高密度、系统性的主谓搭配或句子残缺问题。主要局部问题来自压缩式名词结构和直译，而不是基础语法。例如：

- 标题中的“计划跨数据库检验”把“计划”和“检验”直接并置；若“计划”表示研究状态，“计划开展跨数据库检验”更清楚。
- “时间外、医院外和未触碰数据库外测试”中的三个并列项结构不平行，“未触碰数据库外”还可能被理解为“数据库之外”。宜分别写明时间外验证、医院外验证和预先隔离的外部数据库测试。
- “允许图无同 bin 瞬时循环”等高度压缩表达省略关系词，建议恢复为完整判断句。

这些问题已计入 L-R024-07，尚未达到语法硬门阈值。

### Academic Register & Tone

正文总体保持正式、审慎的研究计划语气，但以下表达削弱学术语体：

- “不得调阈救回”“预测好不能挽救”“不重救”使用口语化的“救回/挽救”；可改为“不得据此改变预设阈值或推翻未通过判定”。
- “真正未触碰”带有口语强调和英文直译色彩；“预先隔离且在模型冻结前不可访问”更可核验。
- “变量角色防火墙”“证据阶梯”是项目隐喻。正文已有“显式分离生理状态、治疗行动和观察过程”的准确说法，应以直接描述代替隐喻。

由于主导语体仍为技术性学术语体，本维度未触发非正式语体硬门。

### Terminology Consistency

| id | term_or_phrase | locator | reader_baseline | problem | recommended_replacement | first_use_definition | basis | acceptance_test |
|---|---|---|---|---|---|---|---|---|
| L-R024-01 | 条件性稀疏 RCT 次要再分析 | 标题、单句摘要、Objective 4 | 熟悉 RCT，但不熟悉项目内部命名 | “稀疏”修饰对象错误；“随机化再分析”可能被理解为重新随机化 | 基于稀疏访视数据的条件性 RCT 次要分析 | 条件满足后，利用两项 RCT 的实际稀疏访视数据，分别开展基于原随机分组的次要分析 | 中文修饰关系及 dossier 后文对 D7/D8 访视的说明 | 标题能唯一指向访视/测量稀疏和原随机分组的次要分析 |
| L-R024-02 | 候选动态系统表征 | 标题、摘要、研究问题 | 临床与方法学跨学科读者，不假定系统辨识专门知识 | 指称与功能未在首用处说明，且与“表示/模型”漂移 | 选定一个直接主名称；可考虑“候选动态状态模型”或保留“表征”并立即解释 | 描述患者生理状态、治疗行动和测量过程从发病前到结局如何随时间变化的候选模型 | 读者交接基线、语义中心分析及正文后续角色定义 | 首用处可回答“是什么、描述什么、产生什么输出”，全文名称稳定 |
| L-R024-03 | 投影可观测状态摘要；随机化扰动；death-ranked SOFA | 单句摘要、研究问题、RCT 方法 | 熟悉试验与纵向数据，但不假定投影模型细节 | 术语成分堆叠，比较量和排序规则延迟定义，“扰动”存在多义 | 一维可观测综合评分；随机分组间差异；将死亡列为最差等级的 SOFA 综合结局 | 由冻结模型把试验实际访视指标映射为一维评分，并比较随机分组间的评分分布 | 语义中心分析及 dossier 后文公式、排序定义 | 摘要单独阅读即可识别评分来源、排序和比较对象 |
| L-R024-04 | 门、no-go、fallback、zero-update 及未展开缩写 | 日期门、外部检验、RCT 分支、证据链、风险矩阵 | 仅可假定一般重症研究、纵向数据、验证和不确定性知识 | 内部流程标签和学科缩写超出共同基线 | 预设判定标准、停止条件、替代分析、不更新模型的外部评估；首次展开缩写 | 在首次出现处用一句直接中文说明判定动作、失败后果或统计量功能 | reader handoff 与正文用法 | 任一参与学科读者无需项目词表即可理解正文主干 |

未进行外部术语检索：以上问题可由中文修饰关系、首用定义完整性、同一 dossier 的后文释义和明确给定的读者知识基线直接判定。修订若决定保留新命名，需另以领域标准或至少两个独立研究群体的稳定用法核验；核验不足时优先采用直接描述。

### Tense & Voice Conventions

计划性时态使用恰当。已知事实使用现在时或完成性表述，计划步骤使用“计划、须、若、才、将”，未生成结果明确写为“尚未生成”或“待 G1”。少量“阶段 II 成功是……”属于对预设判定规则的现在时定义，不构成把计划写成完成结果。无需系统性调整时态。

### Conciseness & Redundancy

#### L-R024-06 — 限定语和否定边界重复（minor）

“不支持潜在动力学、转移边、中介、控制或整个系统模型”“不能挽救主要任务/恢复门/外部门失败”等边界在摘要、非假设、RCT 方法、证据链、解释矩阵、贡献定位、风险和停止条件中多次近似重复。语言修订可先统一为一套准确表述，再在确有局部解释需要的地方保留短版；本评估不决定哪些科学边界可删除，也不指定跨章节安放位置。

“候选、计划性、条件性、次要、有限、实际访视、投影可观测”等限定经常同时位于同一名词前。应把关键限定改写为条件句或后置说明，使语义中心先出现。

### Readability & Flow

章节总顺序可辨识，但首屏在读者掌握核心对象之前即引入阶段、判定标准、试验简称和禁止性结论。建议先稳定回答三件事：研究对象是什么、阶段 II 要做什么、何种结果属于成功；再引入阶段 III 的条件分支。表格数量较多且同一信息在正文、证据链、解释矩阵和风险矩阵间往返，导致阅读路径反复。语言层面可通过短主题句、平行结构和统一术语降低负担；是否合并或移动科学内容应由后续内容结构评审决定。

---

## Language Revision Priorities

1. **标题与核心术语**：修正“稀疏”的修饰对象；统一并定义研究对象和 RCT 输出名称；这是解除术语硬门的首要条件。
2. **读者可达性**：把流程标签、英文状态词和未展开缩写改为标准中文或首次完整定义，尤其处理摘要、研究问题和阶段判定表。
3. **句子结构**：拆分单句摘要、总研究问题及 R0/R1 长段，先给语义主干，再列条件和例外。
4. **一致性**：统一“表征/表示/模型”“次要再分析/二次分析”“跨数据库检验/验证”等同指或近同指表达；若概念有意不同，应在首次并列时明确差别。
5. **简洁与语体**：减少逐字重复的禁限清单和限定堆叠，以直接说明替代“门、防火墙、阶梯、救回、真正未触碰”等流程化、隐喻性或口语化表达。

---

## Re-Assessment Status

本报告是基线评估，不是复评；未读取匿名问题清单、既往分数、既往决定、旧版本文本或修订差异。

| Check | Current assessment |
|---|---|
| Listed issues no longer present | 不适用 |
| Listed issues still present | 不适用 |
| New current-text issues | L-R024-01 至 L-R024-07，均来自当前冻结文本的独立全篇评估 |

---

## Assessment Notes

- **独立性**：评估在新的独立实例中完成；未查看任何既往语言/叙事评估、修订计划、修订版 dossier、差异报告、保留性报告、评估者报告、预期发现、测试脚本或工作流状态。
- **完整性**：完整读取并评估了 v003 dossier 的全部读者可见内容。对标题中的三个复合短语以及标题、摘要、研究问题、研究对象、贡献和核心设计关系中的角色型核心术语逐一检查了语义中心、修饰关系、首用指称与功能、读者知识基线、标准性或翻译自然度、流程用语、限定叠加、重复、计划性时态、简洁性和连贯性；工作笔记未作为术语清单写入报告，只报告触发问题的项目。
- **体例边界**：机器前置字段、固定合同标题和字段标签视为技术支架；只有当相同语言进入标题、摘要、正文、表格或预定图题时才作为问题。表格单元格允许体例性省略，不按正文残句机械计错。
- **约定选择**：采用中文学术语言、临床/生物医学研究、计算机科学/AI 与一般科学的交叉约定；未指定期刊，因此未应用期刊专属格式。
- **角色边界**：本报告只判断语言是否清楚、标准、一致且适合目标读者，不评价研究的科学有效性、论证质量、新颖性、影响、可行性或期刊适配度。

