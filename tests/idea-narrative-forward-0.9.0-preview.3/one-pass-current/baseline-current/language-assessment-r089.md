---
review_id: language-assessment-r089
reviewer_skill: academic-language-assessor
reviewer_instance_id: academic-language-assessor-r089-fresh
workflow_id: RID-SEPSIS-CSM-20260717-001
round_id: baseline-current
input_artifact_ids:
  - idea-dossier-I01-001-v003
input_versions:
  - v003
scope: complete_idea_dossier
dossier_ref:
  artifact_id: idea-dossier-I01-001-v003
  version: v003
  path: tests/idea-test-0.9.0-preview.1/0.9.0-preview.1/03_ideas/nodes/I01-001/dossiers/idea-dossier-v003.md
reader_handoff: {artifact_id: embedded-reader-handoff, version: embedded, path: null}
files_read:
  - research-skills-openai/AGENTS.md
  - research-skills-openai/skills/academic-language-assessor/SKILL.md
  - research-skills-openai/skills/academic-language-assessor/references/language-assessment-rubric.md
  - research-skills-openai/skills/academic-language-assessor/references/language-hard-gates.md
  - research-skills-openai/skills/academic-language-assessor/references/chinese-academic-language-conventions.md
  - research-skills-openai/skills/academic-language-assessor/references/discipline-language-conventions.md
  - research-skills-openai/skills/academic-language-assessor/references/terminology-review.md
  - research-skills-openai/skills/academic-language-assessor/templates/language-assessment-report.md
  - research-skills-openai/skills/academic-language-assessor/scripts/scan_idea_language_candidates.py
  - tests/idea-test-0.9.0-preview.1/0.9.0-preview.1/03_ideas/nodes/I01-001/dossiers/idea-dossier-v003.md
isolation_mode: fresh_subagent
prior_scores_visible: false
source_edits_performed: false
decision: major_language_revision
findings:
  - finding_id: LA-R089-001
    severity: major
    finding_kind: terminology
    category: 核心研究对象的名称与首次定义
    dossier_locator: 标题；Title, summary, audience, and positioning 中 Title、One-sentence complete-Idea summary 与 Positioning and contribution frame；Structured abstract 中 Objective and hypothesis；Research question, objectives, and core hypothesis 中 Primary research question 与 Core hypothesis；Interpretation matrix；Contribution and evidence ladder
    current_problem: “候选动态系统表征”及其多个变体是全篇主语，却没有在读者入口说明它具体描述什么、可估计什么以及哪些模型类别仍待审计后确定；“表征”“系统”“候选”叠加后，跨学科读者无法仅凭标题和摘要区分它是纵向预测模型、多状态模型、状态空间模型还是已经识别的生理系统。
    target_state: 标题和首次摘要使用无需项目词表即可识别研究对象与时间范围的直接描述；后文若保留简称，应在首次出现时说明其观测性、候选性与模型类别尚未锁定。
    required_change_or_replacement: 将标题中的核心对象改为“用于描述脓毒症发病前风险、首次发病及发病后互斥状态转移的候选纵向模型”或同等直接描述；在摘要首次定义后，全篇用一个短称（如“候选纵向模型”）指代，不再交替使用“候选全病程表示”“候选架构”“候选系统表征”“复杂候选”等未界定形式。标题必须保持研究对象、计划性跨数据库评估和条件性试验次要分析三个修饰关系清楚，不得把“条件性”误附着到跨数据库评估。
    content_to_preserve: 保留发病前风险、首次发病、发病后互斥状态与结局的时间范围；保留观察性而非因果的边界；保留多状态、线性状态空间及至多一个受限复杂模型均可能成为最终模型的设计弹性；保留“候选”和“计划”限定。
    acceptance_test: 从标题起逐项检索“候选动态系统表征”“候选全病程表示”“候选架构”“候选系统表征”“复杂候选”和“跨库系统表征”；除首次定义中用于说明旧称外，正文只保留一个已定义短称。让未看方法部分的目标读者仅凭标题与一句摘要即可回答研究对象、时间范围、观测性边界和模型类别尚未最终确定这四点。
    term_or_phrase: 候选动态系统表征
    recommended_form_or_plain_description: 用于描述脓毒症发病前风险、首次发病及发病后互斥状态转移的候选纵向模型
    evidence_basis: 这是由 dossier 已明确列出的研究对象、两项主要任务和模型候选类别组成的直接描述，不依赖未核验的新术语；Focused Terminology Review 要求在无法证明紧凑标签为跨学科标准术语时优先使用可直接识别对象、操作与作用的描述。未以“检索不到整句”作为非标准证据。
    first_use_definition: 本研究拟构建一个候选纵向模型，用于在观察到的照护和测量条件下描述 ICU 患者从脓毒症发病前风险到首次发病及发病后互斥状态转移；具体模型类别将在双数据库审计后从预设的多状态模型、线性状态空间模型或至多一个受限复杂模型中确定。
    competing_forms_and_locators:
      - “脓毒症全病程候选动态系统表征”——标题、Title、Primary research question
      - “候选全病程表示”——Structured abstract / Objective and hypothesis
      - “候选架构”——Background, current state, gap, significance, and rationale 第 3 段
      - “受限复杂候选”“复杂候选”——Structured abstract、Core hypothesis、Work packages、Absolute simulation、Interpretation matrix
      - “跨库系统表征”“跨数据库候选系统表征”——Twenty-four-month minimum and dated gates、Conjunctive minimum success definition、Risk matrix
  - finding_id: LA-R089-002
    severity: major
    finding_kind: terminology
    category: 判定标准与分析后果的项目内部词汇
    dossier_locator: One-sentence complete-Idea summary；Structured abstract 全部字段；Twenty-four-month minimum and dated gates；Conjunctive minimum success definition；Public ICU database roles and G1 audit；Absolute simulation and semi-synthetic recovery gate；Hospital-primary genuine cross-database validation；Conditional trial-observation projection and independent fallback；Falsification and stop criteria；Risk and automatic alternative matrix
    current_problem: “门、过门、降级、准入、封印、清零、救回、失败图、防火墙”等项目管理或软件隐喻同时承担资格条件、统计判据、停止规则、替代分析和报告状态等不同功能；G1、R0、R1 等项目标签在进入方法细节前未给出科学内容。普通词“失败”也在模型不满足判据、数据不合格、分析停止和结果无支持之间切换，读者必须反推其具体后果。
    target_state: 每处均直接写明判定对象、预先规定的数值或语义标准、未满足时受影响的分析以及后续允许的替代分析；项目阶段标签只可在完整科学名称之后作为括号内短称。
    required_change_or_replacement: 用“预先规定的判定标准”“最低数据支持条件”“不满足标准时停止该模型的结构解释”“改用预设的多状态或线性模型”“在外部测试前冻结分析方案”“报告未满足标准的中心或亚组”等直接表述替换隐喻。首次出现 G1 时写作“双数据库可观测性与样本支持审计（G1）”；首次出现 R0、R1 时分别写出“试验语义与共同测量变量资格核验（R0）”和“测量一致性、校准与投影误差核验（R1）”。
    content_to_preserve: 保留所有日期、阈值、先后顺序、停止条件、替代分析和禁止性解释；不得因语言修改放宽或合并不同科学标准。
    acceptance_test: 全篇检索“门”“过门”“降级”“准入”“封印”“清零”“救回”“挽救”“失败图”“失败产物”“防火墙”“G1”“R0”“R1”；每个保留项均在同句或紧邻句明确写出判定对象和科学后果，G1/R0/R1 的首次读者可见用法均有完整名称。不得留下只靠这些短称才能理解的资格、停止或解释规则。
    term_or_phrase: 门、降级、准入、封印、防火墙及 G1/R0/R1
    recommended_form_or_plain_description: 预先规定的判定标准、最低数据支持条件、未满足标准时停止相应分析或改用预设的较简单模型，以及冻结后独立进行的外部评估
    evidence_basis: dossier 自身已在日期表、模拟表和试验分支中给出各词对应的具体标准与后果，因此可直接展开而无需另造术语；Focused Terminology Review 要求对控制纳入、替代分析、停止或解释后果的紧凑标签明确写出触发条件、受影响对象和科学后果。
    first_use_definition: 本研究为数据支持、模型恢复、外部性能和试验投影分别预先规定判定标准；若某项标准未满足，则只停止受该标准约束的分析或改用预设的较简单分析，并单独报告原因与结果。
    competing_forms_and_locators:
      - “绝对模拟恢复门”“假置信门”“绝对门”——One-sentence summary、Structured abstract、Absolute simulation、Falsification criteria
      - “资源门”“审计与协议门”“恢复与准入门”“开发冻结门”“真正外部门”“条件性 RCT 门”——Twenty-four-month minimum and dated gates
      - “试验语义门”“冻结观测投影门”“观测投影门”“fidelity 门”——Structured abstract、Background、Conditional trial-observation projection
      - “G1”“硬门”——Public ICU database roles and G1 audit、Required analyses、Remaining execution gates
      - “R0”“R1”——Conditional trial-observation projection、Evidence chain、Claim-support table、Risk matrix
      - “自动降级”“准入候选”“封印”“泄漏清零”“失败图”“变量角色防火墙”“不能挽救/救回”——摘要、工作包、外部评估、关键技术、证据链、风险表
  - finding_id: LA-R089-003
    severity: major
    finding_kind: terminology
    category: 外部性能评估与模型更新的名称
    dossier_locator: "标题；One-sentence complete-Idea summary；Structured abstract / Approach、Contribution and impact；Conjunctive minimum success definition；Hospital-primary genuine cross-database validation；Evidence chain: 医院优先、未触碰的计划跨数据库检验；Interpretation matrix；Contribution and evidence ladder；Title and positioning claim-support table；Risk matrix"
    current_problem: “计划跨数据库检验”“真正未触碰”“未触碰运输性检验”“zero update”“外部检验”“跨库运输”“适配后运输”“transport updating/development”交替出现，既可能指冻结模型在新数据库中的直接性能评估，也可能指使用适配集后的重校准、观测层更新或全模型重拟合；这会模糊核心贡献究竟是外部评估还是模型更新。
    target_state: 把冻结模型在新数据库上的直接评估与使用适配数据后的模型更新分开命名，并在摘要首次出现时说明两者的证据含义不同。
    required_change_or_replacement: 统一使用“未更新外部性能评估（通常称外部验证）”描述冻结模型直接在 eICU 最终测试区上的评估；分别使用“基于适配集的重新校准”“基于适配集的观测层更新”和“全模型重新拟合”描述后续操作。删除“真正”“天然稳健”“运输”等不能直接说明操作的修饰词，除非“可迁移性”被明确界定为评估目标而非更新结果。
    content_to_preserve: 保留医院级分区、最终测试区不参与开发、跨分区患者排除、零更新结果优先、有限更新不能替代零更新失败以及全模型重拟合不属于外部验证的边界。
    acceptance_test: 全篇检索“跨数据库检验”“外部检验”“运输”“transport”“zero update/zero-update”“有限更新”“更新”“重拟合”；每处必须归入且只归入“未更新外部性能评估、重新校准、观测层更新、全模型重拟合”四类之一。摘要、方法、证据链、解释矩阵和贡献表对同一操作使用同一名称，并明确后三类不能替代第一类。
    term_or_phrase: 跨数据库检验、未触碰运输性检验、zero update 与 transport updating
    recommended_form_or_plain_description: 未更新外部性能评估；基于适配集的重新校准；基于适配集的观测层更新；全模型重新拟合
    evidence_basis: TRIPOD 说明外部验证是在新数据中使用原模型生成预测并与观察结局比较，并把验证后基于验证数据的调整称为模型更新；TRIPOD+AI 为减少歧义更倾向用模型“评估”描述性能检验。来源：https://doi.org/10.1136/bmj.g7594 ；https://www.tripod-statement.org/ ；https://pmc.ncbi.nlm.nih.gov/articles/PMC11019967/
    first_use_definition: 未更新外部性能评估是指不利用最终测试区重新估计任何参数，直接用冻结模型生成预测并评估其性能；重新校准、观测层更新和全模型重新拟合均利用适配数据，必须作为模型更新分别报告。
    competing_forms_and_locators:
      - “计划跨数据库检验”“真正未触碰的跨数据库检验”——标题、One-sentence summary、Structured abstract / Approach
      - “未触碰运输性检验”“跨库运输”“数据库级运输/描述”——Positioning、Core hypothesis、Hospital-primary genuine cross-database validation
      - “zero update/zero-update”“零更新外部检验”——Structured abstract、Conjunctive success、Hospital-primary validation、Interpretation matrix
      - “adaptation-only calibration”“仅校准更新”——Structured abstract、Hospital-primary validation、Evidence chain
      - “observation-layer update”“仅观测层更新”“decoder adaptation”——Structured abstract、Hospital-primary validation、Evidence chain、Risk matrix
      - “transport updating/development”“适配后运输”——Hospital-primary validation、Interpretation matrix
  - finding_id: LA-R089-004
    severity: major
    finding_kind: terminology
    category: 随机试验次要结局与效应量的名称
    dossier_locator: "标题；One-sentence complete-Idea summary；Structured abstract / Expected result、Contribution and impact；Objectives 第 4 项；Conditional trial-observation projection and independent fallback；Evidence chain: 条件性稀疏 RCT 观测投影或独立临床状态再分析；Planned outputs；Interpretation matrix；Contribution and evidence ladder；Title and positioning claim-support table；Risk matrix"
    current_problem: “投影可观测状态摘要”“投影摘要”“随机化扰动”“death-ranked SOFA”“independent fallback”“trial-specific clinical-state reanalysis”同时指向结局变量、排序规则、估计量、组间比较和替代分析。“扰动”还容易被系统辨识读者理解为对潜在动力学或机制施加的输入，虽然后文反复否认这一解释，摘要入口仍支持误读。
    target_state: 分别直接命名结局的组成与排序、统计汇总量、随机分配组间比较以及投影不合格时的替代结局；避免以“扰动”暗示机制或动态系统被干预。
    required_change_or_replacement: 投影分支写为“D7/D8 层级复合结局的组间差异：死亡列为最不利，访视时存活在院者按冻结投影分数排序，访视前存活出院列为最有利；以概率指数或胜率汇总”。替代分支写为“D7/D8 SOFA 层级复合结局的独立次要分析：同样排列死亡、存活在院的 SOFA 与存活出院”。结果名称统一为“随机分配组间差异”或在明确 estimand 后称“治疗分配效应”，不用“随机化扰动”“fallback”或裸露的 death-ranked。
    content_to_preserve: 保留每项试验分开分析、实际 D7/D8 访视、死亡与出院的排序、投影权重冻结、概率指数/胜率、中心或分层因素、缺失处理、投影失败后与阶段 II 独立以及不支持潜在动力学、转移边、中介或控制的边界。
    acceptance_test: 在标题、摘要、目标、方法、证据链、预期输出、解释矩阵和贡献表中逐项核对：每个 RCT 分支均明确写出人群、访视、层级复合结局、死亡/出院处理、组间汇总量和与阶段 II 的关系。全篇不再用“扰动”“death-ranked”“fallback”“投影摘要”单独承担上述任一信息；对推荐替换再作修饰关系检查，D7/D8 必须修饰访视而非人群或模型。
    term_or_phrase: 投影可观测状态摘要的随机化扰动；death-ranked SOFA；independent fallback
    recommended_form_or_plain_description: D7/D8 层级复合结局的随机分配组间差异，以概率指数或胜率汇总；投影分支按冻结投影分数排列存活在院者，独立次要分支按 SOFA 排列存活在院者，死亡最不利、访视前存活出院最有利
    evidence_basis: ICH E9(R1) 要求明确人群、治疗条件、结局变量、汇总量和中间事件的处理，支持用这些要素而非“扰动”命名估计目标；优先级复合结局和胜率/胜比方法以临床重要性排序结局组成。来源：https://www.ema.europa.eu/en/documents/scientific-guideline/ich-e9-r1-addendum-estimands-and-sensitivity-analysis-clinical-trials-guideline-statistical-principles-clinical-trials-step-5_en.pdf ；https://pubmed.ncbi.nlm.nih.gov/21900289/ 。推荐形式是对 dossier 已冻结排序规则的直接描述，不额外改变估计量。
    first_use_definition: 条件满足时，每项试验分别比较随机分配组在实际 D7 或 D8 的层级复合结局：死亡为最不利，访视时存活在院者按冻结投影分数由差到好排序，访视前存活出院为最有利，并以概率指数或胜率汇总；投影不满足预设标准时，改用同一排序框架下的 SOFA 独立次要分析。
    competing_forms_and_locators:
      - “投影可观测状态摘要”“投影可观测摘要”“投影摘要”——One-sentence summary、Objectives、Projection-pass estimand、Evidence chain、Interpretation matrix
      - “访视特异随机化扰动”“有限随机化扰动”“随机化投影摘要扰动”——摘要、Primary research question、Evidence chain、Contribution ladder
      - “death-ranked 投影可观测摘要”“death-ranked SOFA”——One-sentence summary、Evidence chain、Planned outputs、Risk matrix
      - “独立 SOFA 分支”“independent fallback”“trial-specific independent secondary clinical-state reanalysis”——摘要、Conditional trial-observation projection、Evidence chain、Claim-support table
  - finding_id: LA-R089-005
    severity: major
    finding_kind: terminology
    category: 未定义缩写和中英混排的技术名称
    dossier_locator: One-sentence complete-Idea summary；Structured abstract；Background 第 2–5 段；Current verified-resource table；Public ICU database roles；Protocol locks；Mutually exclusive state system；Observational target；Absolute simulation；Conditional trial-observation projection；Secondary representation diagnostics；Key techniques；Required analyses；References 之前的全部读者正文与表格
    current_problem: 大量英文缩写或裸露英文词在首次读者可见用法处没有中文全称、英文全称或功能解释，包括 RCT、SOFA、EHR、MPC、MDP、RL、CIF、DUA、CRF、SAP、MAR、MNAR、IPCW、ESS、ARI、MAE、FDR、MCSE、NMAE、SVD、CRPS、MI、mITT、FAS、PPS 等；同一段还混用 test、adaptation、loading、coverage、baseline、fallback、proper score 等英文普通词。跨学科读者不应被假定熟悉所有相邻领域缩写。
    target_state: 每个保留缩写在摘要和主文的首次出现处分别给出自然中文名称及英文全称；仅出现少于三次且不便于阅读的缩写直接改写为中文；数学符号可保留，但其科学角色必须在邻近正文说明。
    required_change_or_replacement: 至少采用以下标准全称或直接描述：随机对照试验（randomized controlled trial, RCT）、序贯器官衰竭评估（Sequential Organ Failure Assessment, SOFA）、电子健康记录（electronic health record, EHR）、模型预测控制（model predictive control, MPC）、马尔可夫决策过程（Markov decision process, MDP）、强化学习（reinforcement learning, RL）、累积发生函数（cumulative incidence function, CIF）、数据使用协议（data use agreement, DUA）、病例报告表（case report form, CRF）、统计分析计划（statistical analysis plan, SAP）、随机缺失（missing at random, MAR）、非随机缺失（missing not at random, MNAR）、删失逆概率加权（inverse probability of censoring weighting, IPCW）、有效样本量（effective sample size, ESS）、调整兰德指数（adjusted Rand index, ARI）、平均绝对误差（mean absolute error, MAE）、错误发现率（false discovery rate, FDR）、蒙特卡洛标准误（Monte Carlo standard error, MCSE）、归一化平均绝对误差（normalized mean absolute error, NMAE）、奇异值分解（singular value decomposition, SVD）、连续分级概率评分（continuous ranked probability score, CRPS）、多重插补（multiple imputation, MI）、修正意向治疗（modified intention-to-treat, mITT）、全分析集（full analysis set, FAS）和符合方案集（per-protocol set, PPS）。将 test、adaptation、loading、coverage、baseline、fallback、proper score 分别改为最终测试区、适配区、载荷、区间覆盖率、基线、预设替代分析、恰当评分规则或更具体的评分名称。
    content_to_preserve: 保留数据库名、试验名、变量符号、标准统计方法名称与公式；不得把不同缩写合并为同一概念，也不得翻译合同固定字段或参考文献题名。
    acceptance_test: 从标题至 References 前进行大小写缩写与连续英文词扫描；每个保留缩写在结构化摘要和主文首次出现处分别有全称，少于三次的非必要缩写已展开。逐项检查 RCT、SOFA、EHR、MPC、MDP、RL、CIF、DUA、CRF、SAP、MAR、MNAR、IPCW、ESS、ARI、MAE、FDR、MCSE、NMAE、SVD、CRPS、MI、mITT、FAS、PPS 及 test、adaptation、loading、coverage、baseline、fallback、proper score，不得依赖项目词表理解。
    term_or_phrase: 未定义缩写与裸露英文方法词
    recommended_form_or_plain_description: 在首次出现处使用“自然中文名称（标准英文全称，缩写）”，后续只在确有重复收益时使用缩写；英文普通词改为具体中文操作名称
    evidence_basis: Chinese Academic Language Conventions 要求中英文术语和缩写一致，Discipline Language Conventions 要求非通用缩写在摘要与主文首次出现时定义且使用少于三次时不宜缩写；所列英文扩展均为相关领域的标准全称，中文形式采用直接科学描述而非项目自造短称。
    first_use_definition: 结构化摘要首次提及试验与结局时写作“随机对照试验（randomized controlled trial, RCT）”和“序贯器官衰竭评估（Sequential Organ Failure Assessment, SOFA）”；其余缩写在各自首次进入正文时按同一格式定义。
    competing_forms_and_locators: []
  - finding_id: LA-R089-006
    severity: major
    finding_kind: language
    category: 一句摘要的句法负荷与信息顺序
    dossier_locator: Title, summary, audience, and positioning / One-sentence complete-Idea summary
    current_problem: 该句在一个主句中连续嵌入数据资格、四段病程、两类模型限定、两个阶段的证据、两个试验与访视、投影资格、替代分支和六项禁止性解释；核心研究动作直到长串前置修饰后才出现，读者必须多次回读才能区分阶段 II 主体与阶段 III 条件分支。
    target_state: 保持一句话合同，但按“核心研究对象与数据—阶段 II 主要评估—阶段 III 条件性次要分析—解释边界”的顺序组织成平行分句，每个分句只有一个主要动作。
    required_change_or_replacement: 重写为一个句号结束的单句，先直接说明候选纵向模型描述什么，再说明未更新外部性能评估，随后用一个明确条件从句说明两项试验的层级复合结局分析，最后用一个短分句保留非因果与非控制边界；删除可在结构化摘要展开的阈值、阶段编号重复和内部短称。
    content_to_preserve: 保留 24 个月阶段 I–II、两个需审计的公共 ICU 数据库、发病前至结局范围、知识约束与不确定性、未更新外部评估、EXIT-SEP D7、XBJ-SCAP D8、投影不合格时的 SOFA 独立分析，以及不支持因果网络、连续动力学、控制或数字孪生的边界。
    acceptance_test: 修改后仍为一个句号结束的单句；分号不超过 3 个；每个分号分隔的分句只有一个限定谓语；阶段 III 条件必须以“仅当……时”开始，替代分析必须以“不满足时……”明确引出；目标读者可在不读后文的情况下分别标出阶段 II 主体、阶段 III 条件分支与解释边界。
  - finding_id: LA-R089-007
    severity: minor
    finding_kind: language
    category: 主要研究问题的并列层级与可读性
    dossier_locator: Research question, objectives, and core hypothesis / Primary research question
    current_problem: 单个问句把候选模型属性、四段病程、医院与数据库评估、投影资格、稀疏访视、随机试验比较和替代分析全部嵌套在“使其……随后仅在……否则……”结构中；三个编号分项的语法层级并不平行，第三项远长于前两项。
    target_state: 保持一个研究问题，但以一个总问句统领三个语法平行、长度接近的任务短语，并把投影不合格时的替代分析写成第三项内部的清楚条件。
    required_change_or_replacement: 将主干改为“该候选模型能否同时……、……并……？”；三项分别使用“描述”“评估”“比较”作为主要动词。第三项先写每项试验实际访视的层级复合结局组间比较，再用单一条件从句说明投影不合格时改用 SOFA 独立次要分析；删除在前文已定义的修饰词堆叠。
    content_to_preserve: 保留不混淆预测与因果、四段病程、医院和数据库层面的评估、实际稀疏访视、投影资格、两试验分开分析及与阶段 II 独立的替代分支。
    acceptance_test: 最终文本仍只有一个问号和一个主要研究问题；三个编号项各有一个明确主要动词且句法平行；第三项的条件和替代后果均在该项内闭合，不依赖后文补足；未引入新的未定义短称。
  - finding_id: LA-R089-008
    severity: minor
    finding_kind: language
    category: 限定语与禁止性解释的近义重复
    dossier_locator: Structured abstract / Contribution and impact；Core hypothesis and non-hypotheses；Conditional trial-observation projection；Evidence chains 中各 Limits and failure conditions；Falsification and stop criteria；Interpretation matrix；Contribution and evidence ladder；Title and positioning claim-support table；Risk matrix；Identity and final stop boundary
    current_problem: “不能挽救”“不支持潜在动力学、转移边、中介、控制或整个模型”“有限更新不能替代零更新失败”“阶段 III 不补足阶段 II”等边界以近乎相同的长串形式在摘要、方法、证据链、解释矩阵和风险表反复出现；同时“条件性、次要、访视特异、有限、独立”等限定语多次叠加，削弱局部重点。
    target_state: 每个局部段落保留与其科学角色直接相关的一条精确边界，避免同一边界在相邻句或同一表格中近义复述；不同科学条件仍分别保留，不由语言评估决定最终放置位置。
    required_change_or_replacement: 对上述定位做近义重复核对，缩短重复的禁止性清单并删除同一局部范围内的复述；将限定语贴近其修饰对象，避免连续四个以上前置限定。由后续叙事评估决定各完整边界最终保留在哪一处，本修改只处理词句重复，不移动或删除科学上不同的条件。
    content_to_preserve: 保留预测不等于因果、外部更新不替代未更新评估、试验替代分支与阶段 II 独立、随机试验结果不验证潜在动力学或控制、阶段 III 不补足阶段 II 失败等全部不同边界。
    acceptance_test: 对“不能挽救/不得挽救/不可救回”“不支持潜在动力学”“有限更新不能替代”“阶段 III 不补足/不计入”进行全文对照；同一局部段落或同一表格不再重复同义边界，连续前置限定语不超过 3 个；每一种科学边界至少保留一处完整、可定位表述，且不得用跨节指针代替必要的局部限制。
unresolved_issues:
  - LA-R089-001
  - LA-R089-002
  - LA-R089-003
  - LA-R089-004
  - LA-R089-005
  - LA-R089-006
  - LA-R089-007
  - LA-R089-008
---

# Language Assessment Report

**Assessment ID**: language-assessment-r089
**Target Language**: Chinese (zh-CN)
**Discipline**: 重症医学、临床流行病学、纵向统计、系统辨识、系统科学、医学 AI 与转化研究的跨学科研究
**Target Journal**: 未指定
**Scope**: complete_idea_dossier
**Date**: 2026-07-20

---

## Overall Language Readiness

**Level**: major_language_revision

**Recommendation**: revise_language

---

## Dimension Scores

| Dimension | Score (1–10) | Severity |
|-----------|-------------|----------|
| Grammar & Syntax | 9 | pass |
| Academic Register & Tone | 7 | pass |
| Terminology Consistency | 3 | fail |
| Tense & Voice Conventions | 9 | pass |
| Conciseness & Redundancy | 4 | borderline |
| Readability & Flow | 4 | borderline |

---

## Hard Gate Status

**Overall**: fail

| Gate | Status | Detail |
|------|--------|--------|
| Grammar error density | pass | 完整通读未发现达到阈值的明确语法错误；中文词边界未作机械归一，保守估计仍低于每 500 词 1 处 |
| Academic register | pass | 全篇保持正式研究语体；项目管理与软件隐喻按术语和可读性问题处理，不构成两节以上的口语化语体 |
| Terminology coherence | fail | 至少 3 个核心概念影响入口理解或科学后果：核心研究对象、外部性能评估与模型更新、随机试验次要结局；另有项目阶段标签和未定义缩写扩大读者障碍 |
| Tense systematic violation | pass | 作为计划性 Idea，未来与条件语气使用一致；未把未完成工作系统性写成既成结果 |

---

## Strengths

- 计划产物、现有证据和未生成结果区分清楚，整体没有把拟开展工作写成已完成研究。
- 对预测、因果、机制、控制和临床推广的边界用语基本谨慎，未出现宣传性首创主张。
- 多数方法表格保持平行列结构，数值标准、触发条件和后果通常可以定位。
- 中文句法本身稳定，未见成片语病；主要阅读负担来自术语、缩写和信息密度，而非基础语法。

---

## Specific Issues

### Chinese Academic Clarity

- LA-R089-006（major）：一句摘要在单句合同内承载过多条件和分支，主线出现过晚。
- LA-R089-007（minor）：主要研究问题的三个编号项层级不平行，第三项负荷明显过高。
- LA-R089-008（minor）：相同禁止性解释和限定语在多个相邻功能区近义重复。

### Grammar & Syntax

未发现需要单列的基础语法错误。句法风险集中在信息过载和嵌套层级，已由 LA-R089-006 与 LA-R089-007 记录。

### Academic Register & Tone

没有口语化硬门问题。LA-R089-002 所列“门、封印、防火墙、救回”等虽非口语，却以项目管理或软件隐喻替代科学程序名称，降低正式跨学科表达的精确度。

### Terminology Consistency

| id | term_or_phrase | locator | reader_effect | action_in_frontmatter |
|---|---|---|---|---|
| LA-R089-001 | 候选动态系统表征 | 标题、摘要、研究问题、贡献与解释部分 | 不能从入口确定研究对象和模型类别 | yes |
| LA-R089-002 | 门、降级、准入、封印、防火墙及 G1/R0/R1 | 日期标准、模拟、外部评估和试验分支 | 无法区分资格条件、失败状态与后续分析 | yes |
| LA-R089-003 | 跨数据库检验、zero update 与 transport updating | 摘要、外部评估、解释矩阵和贡献表 | 混淆冻结模型评估与利用适配数据的模型更新 | yes |
| LA-R089-004 | 投影摘要的随机化扰动与 death-ranked SOFA | 摘要、试验方法、证据链和输出 | 混淆结局、排序规则、估计量和机制性“扰动” | yes |
| LA-R089-005 | 未定义缩写与裸露英文方法词 | 摘要至方法和表格 | 跨学科读者须猜测相邻领域缩写 | yes |

### Tense & Voice Conventions

计划性 Idea 使用“计划、须、若、仅当、不得”等前瞻与条件表达，和未生成状态一致；没有系统性时态或语态问题。

### Conciseness & Redundancy

LA-R089-008 是主要问题：必要边界本身应保留，但同义长串在多个相邻功能位置反复出现。LA-R089-006 的一句摘要也因限定语叠加而显著失去简洁性。

### Readability & Flow

LA-R089-006 与 LA-R089-007 使读者入口需要回读；LA-R089-001 至 LA-R089-005 又在标题、摘要和研究问题进入技术细节前引入未定义概念。局部表格通常清楚，但不能补偿入口段落的高认知负荷。

---

## Language Revision Priorities

1. **核心术语**：5 组问题——先用直接科学描述统一研究对象、判定标准、外部性能评估和随机试验结局，再定义必要缩写。
2. **读者入口**：2 处问题——在不改变一句摘要和一个研究问题的合同下，重排主句和条件分支。
3. **简洁性**：1 组问题——压缩近义边界和限定语，同时保留所有科学上不同的停止与解释条件。

---

## Re-Assessment Status (if applicable)

不适用。本次是原始完整 dossier 的独立首次语言评估，未读取任何既往问题清单、评分、修订稿或差异材料。

| Check | Current assessment |
|--------|--------------------|
| Listed issues no longer present | 不适用 |
| Listed issues still present | 不适用 |
| New current-text issues | LA-R089-001 至 LA-R089-008 |

---

## Assessment Notes

- 读者先验按 embedded handoff 执行：各读者在本领域有研究训练，但不假定理解其他领域缩写、项目阶段标签或自造复合术语；标题、摘要和研究问题必须先建立主线。
- 适用规范选择为中文学术语言、重症/临床研究、纵向统计与计算机科学/系统辨识的交叉规范；未指定期刊，故未施加期刊专属格式。
- 候选扫描器已对完整 Idea dossier 运行；其 reader-entry 与 consequence 组中的所有紧凑标签均完成内存判定。标准且已及时解释的统计或临床概念未仅因专业性而报告；合同固定标题、字段和 Claim-Support 表头未评分、翻译或改名。
- 聚焦术语核验仅用于“外部性能评估/模型更新”和“随机试验层级复合结局/估计目标”，采用 TRIPOD、TRIPOD+AI、ICH E9(R1) 与优先级复合结局方法来源；未把完整标题短语检索不到当作非标准证据。
- 初次并行加载规范资源时，工具输出在 discipline-language-conventions.md 中段发生上下文截断；随后对 rubric、hard gates、Chinese conventions、discipline conventions、terminology review 和 template 分别完整补读，其中 discipline conventions 按第 1–120、121–240、241–248 行分段。dossier 共 480 行，按第 1–120、121–240、241–360、361–480 行完整分段读取。没有任何一段因截断而未补读。
- files_read 如前置元数据所列。embedded reader handoff 的 path 为 null，未伪造文件记录。未读取 prior assessment、repair plan、writer brief、revised dossier、evaluation、测试脚本或预期结论；未读取 dossier 所引用的项目本地材料。候选 scanner 与 validator 仅按 Skill 合同执行，不读取其测试文件。
- 本报告只评估语言，不判断科学有效性、可行性、新颖性、影响力或期刊适配；未修改 dossier。
