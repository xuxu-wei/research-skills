# Language Assessment Report

**Assessment ID**: language-assessment-I01-001-r010  
**Target Language**: Chinese（zh-CN）  
**Discipline**: 重症医学与临床流行病学为主，涉及纵向统计、系统辨识、医学人工智能与转化研究  
**Target Journal**: 未指定  
**Scope**: 完整 Idea dossier 的读者可见文本，包括标题、一语摘要、结构式摘要、研究背景、研究问题与目标、研究设计与方法、证据链、预期产出、贡献定位、风险与停止条件、表格及参考文献。机器前置元数据和合同固定字段按脚手架处理，不计入语言评分；其用语进入正文时才纳入评估。  
**Date**: 2026-07-18

---

## Provenance

~~~yaml
review_id: language-assessment-I01-001-r010
reviewer_skill: academic-language-assessor
reviewer_instance_id: onepass-baseline-language-r010-fresh
workflow_id: RID-SEPSIS-CSM-20260717-001
round_id: r010
input_artifact_ids:
  - idea-dossier-I01-001-v003
  - reader-handoff-forward-001
input_versions:
  - v003
  - v001
input_artifacts:
  - artifact_id: idea-dossier-I01-001-v003
    version: v003
    path: tests/idea-test-0.9.0-preview.1/0.9.0-preview.1/03_ideas/nodes/I01-001/dossiers/idea-dossier-v003.md
  - artifact_id: reader-handoff-forward-001
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
  - tests/idea-test-0.9.0-preview.1/0.9.0-preview.1/03_ideas/nodes/I01-001/dossiers/idea-dossier-v003.md
  - tests/idea-narrative-forward-0.9.0-preview.3/run-001/inputs/reader-handoff.yaml
isolation_mode: fresh_subagent
prior_scores_visible: false
source_edits_performed: false
decision: major_language_revision
findings:
  - TERM-01
  - TERM-02
  - TERM-03
  - TERM-04
  - TERM-05
  - TERM-06
  - REG-01
  - REG-02
  - CON-01
  - CON-02
  - READ-01
  - READ-02
unresolved_issues:
  - TERM-01
  - TERM-02
  - TERM-03
  - TERM-04
  - TERM-05
  - TERM-06
  - REG-01
  - REG-02
  - CON-01
  - CON-02
  - READ-01
  - READ-02
~~~

## Overall Language Readiness

**Level**: major_language_revision

**Recommendation**: revise_language

文本的基本语法和计划时态总体稳定，但核心研究对象、外部检验和试验投影端点存在首次出现不可直接理解、同一概念多种命名和中英文代码式表达混用的问题。术语硬门未通过，因此当前不能判为可直接提交。主要修订应统一核心术语、在首次出现处给出跨学科读者可理解的定义，并把正文中的流程化隐喻改写为标准研究设计语言。本文不需要全面重写，但需要覆盖全文的系统性语言修订。

## Reader Baseline and Sections Assessed

- 读者可被假定熟悉重症研究、纵向临床数据、验证、不确定性及观察性与干预性证据的一般概念。
- 不能假定读者熟悉项目内部流程词、新造标签、隐喻，或同时掌握系统辨识、纵向统计、临床试验和医学人工智能的全部专门术语。
- 已评估源文第 27–480 行全部读者可见内容。第 1–25 行机器元数据只用于确认文本身份与冻结状态，不按学术语言评分。
- 固定英文标题和字段标签不建议改动；本报告只处理其词汇进入正文、表格或说明文字后的读者影响。

## Dimension Scores

| Dimension | Score (1–10) | Severity | Basis |
|---|---:|---|---|
| Grammar & Syntax | 7 | pass | 未发现密度达到门槛的明确语法错误；主要问题是过度压缩和修饰关系负担，而非句法失范 |
| Academic Register & Tone | 5 | borderline | 总体正式，但多节正文持续采用“门、准入、冻结、降级、挽救、封印、打开 test”等项目流程语言 |
| Terminology Consistency | 3 | fail | 至少三个核心概念存在多种未说明名称，且若干标题或摘要核心术语在首次出现时不能由给定读者基线直接确定所指 |
| Tense & Voice Conventions | 8 | pass | 能稳定区分现有证据、拟议步骤、条件性结果和禁止性解释；未把计划产物写成既有结果 |
| Conciseness & Redundancy | 3 | fail | 限定语、停止条件和禁止性解释在多个读者可见位置高密度重复，且单句内常叠加多层条件 |
| Readability & Flow | 4 | fail | 一语摘要、主要研究问题、投影门及多张表格需要反复回读；跨学科术语缺少及时的普通语言引导 |

## Hard Gate Status

**Overall**: fail

| Gate | Status | Detail |
|---|---|---|
| Grammar error density | pass | 全文未发现可确认的明确语法错误密度超过 3/500 中文词语；长句和名词链问题计入简洁性与可读性，不冒充语法错误 |
| Academic register | pass | 流程化表达跨越多个章节，但正文的主导语域仍是正式而非会话式，未达到“至少两个章节系统性口语化”的门槛 |
| Terminology coherence | fail | “候选动态系统表征”“跨数据库外部检验/可迁移性”“试验投影摘要”三个核心概念均出现多种名称或首次出现不可直接识别；“稀疏 RCT”还支持对稀疏对象的错误理解 |
| Tense systematic violation | pass | 这是前瞻性研究构想，不含既有 Methods/Results 报告；计划、条件和当前证据的时间状态总体一致 |

## Strengths

1. 结构式摘要和正文反复使用“计划”“条件满足时”“尚未生成”等形式，清楚区分拟议工作与既有结果。
2. 对预测、因果、机制、控制和临床应用的语言边界通常明确，没有用结果时态暗示尚未完成的验证。
3. 多数数值阈值、观察时点和条件后果写得具体，避免了“显著提升”“重大突破”等宣传性表述。
4. 表格为复杂的时间安排、状态定义和条件分支提供了可扫描结构；问题主要在单元格内部过密，而非缺少组织。

## Specific Issues

### Chinese Academic Clarity

| id | locator and excerpt | severity | category | explanation | directional repair guidance |
|---|---|---|---|---|---|
| READ-01 | “Title, summary, audience, and positioning”，一语摘要，第 32 行：“本研究计划在 24 个月内……任何分支均不支持……” | major | readability/flow | 单句同时承担研究对象、数据条件、阶段划分、验证方式、试验分支、替代端点和禁止性解释，主干被七层以上的条件与插入语遮蔽。 | 分成研究对象与阶段 II、阶段 III 条件分支、解释边界三组完整句；每句只保留一个主要判断，并在首次出现处解释核心术语。 |
| READ-02 | “Primary research question”，第 60 行；“Core hypothesis”，第 71 行 | major | readability/flow | 主问题把三个子问题、一个条件分支和一个替代分析塞入同一句；核心假设又将审计、参数锁定、恢复、外部稳定和证据链并列，跨学科读者难以确认主谓关系。 | 保留一个总研究问题，随后用平行的子问题或短句展开；把条件、可观察量和失败后果分开陈述。 |
| REG-01 | 第 34、66、71、79–112、191、214–240、278、304、324–335、349–358、412–439 行：“按门实施”“准入”“打开 test”“挽救”“封印”“降级”“闭合”“防火墙”等 | major | academic register | 这些词在执行记录中可以简写，但在标题、摘要、方法与解释段落中持续出现，使文本更像内部运行手册，而不是供跨学科研究者阅读的学术构想。 | 在正文中改用“预设合格标准”“预先确定”“不进入下一分析阶段”“采用预设替代分析”“独立保留数据”等标准表述；确有必要保留的代码式标签只在首次出现时定义。 |
| REG-02 | 第 32、34、39、66、79、100、112、212、230、250、304、337、349–358、439 行：“真正未触碰”“真正外部”“绝对门”“强制”“永不”“不能挽救”等 | minor | register/tone | 反复使用绝对性或防御性措辞增加对抗感，也掩盖了具体的研究规则。部分限制确有必要，但应由条件和后果本身表达强度。 | 用“独立保留的最终测试集”“基于预设绝对阈值的检验”“若不满足则不进入……”等可核查句式代替强调词；保留必要的禁止性边界，但避免连续堆叠。 |
| CON-01 | “Evidence chains”第 282–320 行、“Required analyses”第 322–337 行、“Expected outputs”第 339–370 行、“Contribution”第 372–410 行及“Risks”第 418–439 行 | major | concision/redundancy | 相同的零更新、投影失败、独立 SOFA、不得解释机制和停止条件以近似词序多次出现，造成显著词汇重复。语言评估不能判断这些条件在论证上是否都应保留，但当前重复形式降低信息密度。 | 先统一每项限制的固定短语，再减少同一段或同一表内的近义复述。跨章节保留位置由叙事评估决定，本报告不指定删除哪一处科学条件。 |
| CON-02 | 第 32、50、71、208、246–250、317–318、376–397 行中的斜线并列、复合修饰和连续名词链 | major | concision/readability | “预测/生成分布”“恢复/假置信/弃权记录”“任务/节点级跨库运输”等压缩写法要求读者自行补足逻辑关系；多个限定语堆在名词前，所指边界不清。 | 把斜线关系明确为“以及”“或”“分别”，必要时改为短列表；让每个术语有清楚的中心词，并把条件移到后置从句。 |

### Grammar & Syntax

未发现需要单独列为明确语法错误的实例。长句、修饰附着和名词化负担已在 READ-01、READ-02 与 CON-02 中记录；这些问题影响理解，但不应被夸大为语法硬错误。

### Academic Register & Tone

主要问题见 REG-01 与 REG-02。另有一项轻微格式问题：第 120–129 行资源状态表把 verified、unverified、not generated、project-local derivative 与中文说明混排。若这些不是合同固定值，读者可见层应使用统一中文名称；若属于固定值，应在表前说明其含义，而不是在各行中让读者推断。

### Terminology Consistency

以下仅列影响核心研究对象、主要设计或关键端点的术语，不是全量术语表。

| id | term_or_phrase | locator | reader_baseline | problem | recommended_replacement | first_use_definition | basis | acceptance_test |
|---|---|---|---|---|---|---|---|---|
| TERM-01 | “稀疏 RCT 次要再分析” | 标题第 27、31 行；一语摘要第 32 行 | 熟悉临床试验的一般概念，但不能假定知道此处“稀疏”修饰什么 | 语法附着允许读成“稀疏的随机试验”，而正文实际指 D7/D8 等重复测量或访视稀疏；该歧义位于标题和摘要。 | “访视稀疏的随机对照试验次要分析”或“基于稀疏重复测量的随机对照试验次要分析” | 首次出现即说明稀疏的是访视时点和可用重复测量，而非随机分配或样本本身。 | 标题与第 169–171、242–261 行的实际用法不一致；reader handoff 禁止假定新造标签。 | 标题、摘要和正文均能在不读取方法细节时明确识别稀疏对象，且不再出现悬空的“稀疏 RCT”。 |
| TERM-02 | “投影可观测状态摘要”及“投影可观测摘要”“状态投影”“可观测代理”“投影摘要” | 第 32、41–42、60、67、242–254、314–320、347、368、383–406 行 | 不假定每位读者掌握状态空间模型或奇异值分解 | 首次出现在一语摘要时没有说明由哪些观测、通过何种预定映射得到或其临床排序作用；后文多个名称未说明是否同一对象。 | 选定一个主名称，例如“由预先确定的观测模型计算的一维可观测状态摘要” | 在首次出现处用一句普通语言说明：它由实际访视时可测的共同生理指标，经阶段 II 预先确定的映射计算，用于访视时点的排序比较。 | 首次定义延后至第 248 行，且第 248–252 行同时引入 P_state 与 P_obs；对给定跨学科读者，指代不能在摘要处确定。 | 摘要无需跳到方法部分即可说明该摘要的输入、来源和用途；其后只使用一个主名称，并明确 P_state 与 P_obs 的区别。 |
| TERM-03 | “候选动态系统表征”“候选全病程表示”“候选状态表示”“系统表征”“最小全病程候选表示” | 第 27–42、60–73、92、206–212、370、403–410、439 行 | 熟悉纵向研究，但不假定系统辨识专门训练 | 这些名称围绕核心研究对象交替出现，却没有说明“动态系统表征”“状态表示”和“系统表征”是同一层级还是不同对象。“表征”也未在首次出现处说明是统计模型、状态变量集合还是联合分布。 | 选择一个核心名称，并为确有不同的“状态表示”“观测模型”“任务输出”分别命名 | 首次出现时说明该表征包含患者状态、状态转移及观测与治疗过程的哪些关系，以及本研究只解释哪些可观察或可恢复部分。 | 同一核心对象在标题、摘要、研究问题、方法和解释矩阵中使用至少五种形式，且第 208 行才给出数学对象。 | 读者能从标题后的第一段确定核心对象；全文同层级概念只保留一个名称，任何次级名称均有明确层级定义。 |
| TERM-04 | “跨数据库检验”“真正外部检验”“运输性检验”“跨库验证”“医院外验证”“zero-update”“外部门” | 第 34、38–42、66、71、86–112、228–240、306–312、355、382–407、423–431 行 | 熟悉外部验证的一般概念，但不假定掌握每个子领域的英文缩写或项目标签 | 多个名称有时指独立外部验证，有时指医院级分割，有时指更新后的可迁移性分析；“运输性”在中文普通语境中还可能被理解为物流含义。 | 分别固定为“独立保留数据库上的外部验证”“仅用适配集进行的校准更新”“观测模型更新”“可迁移性分析” | 首次出现时说明 zero-update 是不利用外部测试集重新估计任何参数的验证，并明确它与适配后分析不同。 | 源文自身在第 240 行区分多个更新层级，但标题、摘要和后续表格没有始终维持这一区分。 | 每一名称只对应一种分析；读者能根据名称判断是否使用适配数据、是否更新参数及是否属于主要外部验证。 |
| TERM-05 | “death-ranked SOFA”及“death-ranked 投影可观测摘要” | 第 32、41、67、252–259、317–318、347、368–369、405–406、428 行 | 熟悉 SOFA，但不能假定熟悉该英文复合端点标签 | 英文短语在一语摘要中未经定义，直到方法部分才说明死亡、住院存活和活着出院的排序；中文正文中反复保留英文修饰，增加理解延迟。 | “死亡优先排序的 SOFA 复合状态端点”及相应的“死亡优先排序的可观测状态摘要端点” | 首次出现即依次说明死亡为最差层、住院存活者按指标排序、活着出院为最有利层。 | 第 252、254 行提供了可用的实际定义，但出现过晚，且此前名称不透明。 | 摘要中的首次使用即含简短排序定义；后文中文名称一致，英文仅在确有通行缩写时附注一次。 |
| TERM-06 | “绝对恢复门”“假置信门”“观测投影门”“语义门”“准入门” | 第 32、39–42、66、79–112、214–226、242–254、282–320、349–358 行 | 不熟悉项目内部流程词 | “门”没有说明是统计阈值、资料完整性标准、人工决策点还是分析停止规则；“假置信”尤其不自然，也容易被理解为一般置信区间问题。 | 按实际功能分别使用“基于预设绝对阈值的模拟恢复检验”“错误高置信判断检验”“观测投影合格标准”“试验资料语义核验标准” | 每个标准首次出现时给出评价对象、阈值性质和不满足后的分析后果；G1、R0、R1 如保留，应在正文首次出现时展开。 | reader handoff 明确不允许假定内部流程词；同一个“门”在源文中承担至少四种不同功能。 | 删除标签后，句子仍能直接说明评价什么、怎样判定和未满足时做什么；保留的短标签均只映射到一个已定义标准。 |

### Tense & Voice Conventions

未发现系统性时态或语态问题。计划性步骤通常以“计划”“须”“将”“条件满足时”表达，现有资料则以“提供”“记录”“尚未”等表达。建议修订时继续保留这种证据状态区分，避免为了简洁把拟议结果改成既成事实。

### Conciseness & Redundancy

主要问题见 CON-01 与 CON-02。特别需要避免在同一句内连续使用“仅在……后”“才……”“失败则……”“任何分支均不……”等多层限定。可将合格条件、替代分析和解释边界拆成相邻短句，而不删除任何科学上必需的条件。

### Readability & Flow

除 READ-01 与 READ-02 外，第 246–259 行的 R0、映射、R1、主要估计对象和替代端点连续引入大量符号、缩写与排序规则。建议在公式前先给出一段普通语言路线：资料核验、共同指标资格、预定映射、外部检验、试验比较、替代分析。随后再分别给出公式和阈值。第 269–277、326–335、435 行还集中出现 CIF、MNAR、ESS、ARI、FDR、NMAE、MI、FWER、mITT、SVD 等缩写；只应保留跨全文真正需要的缩写，并在首次读者可见使用处定义。

## Language Revision Priorities

1. **Core terminology**: 6 findings — 先修复标题、一语摘要和主要研究问题中的 TERM-01、TERM-02、TERM-03，再统一外部检验、复合端点和各类合格标准的名称。
2. **Academic register**: 2 findings — 把读者可见正文中的流程化隐喻和强调词替换为明确的评价对象、判定标准与分析后果。
3. **Readability**: 2 findings — 拆分一语摘要和主要研究问题；在公式、缩写与阈值前增加普通语言导引。
4. **Concision**: 2 findings — 减少单句限定语和同一段内的近义复述；跨章节科学条件是否保留应由叙事评估另行决定。
5. **Mixed Chinese-English formatting**: 全文统一缩写首次定义、中文标点、数字与时间单位形式，并减少未定义的英文代码式状态词。

## Re-Assessment Status

| Check | Current assessment |
|---|---|
| Assessment type | baseline |
| Anonymous prior issue list supplied | no |
| Listed issues no longer present | not_applicable |
| Listed issues still present | not_applicable |
| New current-text issues | TERM-01–TERM-06、REG-01–REG-02、CON-01–CON-02、READ-01–READ-02 |

## Recommendation

完成一次覆盖全文的 major language revision 后，再由新的独立评估实例复核。复核重点应是：标题和摘要能否让跨学科读者在首次出现处识别核心研究对象、外部验证和试验端点；同一核心概念是否只保留一个主名称；流程化隐喻是否已改为标准研究语言；长句和缩写密度是否显著下降。无需为本轮语言修订改变研究问题、统计设计或科学主张。

## Assessment Notes and Limitations

- 本报告只评估语言、术语、语域、简洁性和读者可理解性，不评价科学正确性、新颖性、影响、可行性、论证质量或期刊适配性。
- 未指定目标期刊，因此采用生物医学/临床研究与计算机科学/系统辨识的交叉学科一般惯例。
- 中文分词方式会影响“每 500 词”的精确分母；语法硬门仅统计可明确判定的语法错误，不把长句或个人风格偏好计作错误。
- 聚焦术语判断依据给定 reader handoff、首次出现可理解性及全文内部一致性。本报告不主张这些词在所有中文学科文献中均非标准。
- 数学符号、机器前置元数据和固定字段标签本身不构成语言失败；只有其未解释地进入读者可见正文时才记录问题。
- 未编辑或改写源 dossier；所有问题均保持定位式、方向性建议。
