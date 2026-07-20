---
review_id: language-assessment-r002
reviewer_skill: academic-language-assessor
reviewer_instance_id: academic-language-assessor-blind-20260720-r002
workflow_id: RID-SEPSIS-CSM-20260717-001
round_id: blind-baseline-r002
input_artifact_ids:
  - idea-dossier-I01-001-v003
input_versions:
  - v003
scope: complete_idea_dossier
dossier_ref:
  artifact_id: idea-dossier-I01-001-v003
  version: v003
  path: "E:/BaiduNetdiskWorkspace/Jupyter/my_repos/xuxu-hermes/research-skills/tests/idea-test-0.9.0-preview.1/0.9.0-preview.1/03_ideas/nodes/I01-001/dossiers/idea-dossier-v003.md"
reader_handoff:
  artifact_id: embedded-reader-handoff
  version: embedded
  path: null
  target_language: Chinese
  discipline: biomedical-clinical-informatics
  primary_audience: 重症医学、临床流行病学、纵向统计、系统辨识、医学 AI 与转化研究共同体
  prior_knowledge: 熟悉临床研究和本专业常用缩写，但不假定熟悉项目自定义标签、软件状态词或未定义的中英混合短语
files_read:
  - "E:/BaiduNetdiskWorkspace/Jupyter/my_repos/xuxu-hermes/research-skills/tests/idea-test-0.9.0-preview.1/0.9.0-preview.1/03_ideas/nodes/I01-001/dossiers/idea-dossier-v003.md"
isolation_mode: fresh_subagent
prior_scores_visible: false
source_edits_performed: false
decision: major_language_revision
coverage_receipt:
  reader_entry:
    status: completed
    reviewed_count: 14
    basis: 逐一检查扫描器界定的标题、标题字段、完整构想摘要、受众与定位、结构式摘要五项、主要问题、核心假设及非假设入口单元；每个单元均读至句末。
  core_scientific_role:
    status: completed
    reviewed_count: 8
    basis: 对全文实际出现的核心研究对象、任务与结局、验证和更新操作、失败输出、条件性试验部分及贡献名称进行了读者可识别性核对。
  terminology_concordance:
    status: completed
    reviewed_count: 12
    basis: 对扫描器和通读触发的 12 个概念簇完成首次使用、复合标题、跨位置形式及全文一致性核对；仅保留经语境确认的问题。
  local_language:
    status: completed
    reviewed_count: 298
    basis: 检查全部 298 个非固定脚手架的标题、段落、列表项、表格行和参考文献单元，覆盖语法、语体、时态、局部清晰度与局部重复。
findings:
  - finding_id: LA-001
    severity: major
    finding_kind: terminology
    finding_level: meso
    finding_scope: concept_cluster
    scientific_role: conditional-rct-data-property
    normalized_locator: title-summary-objective-and-rct-chain
    failure_mode: misplaced-sparsity-modifier
    fingerprint: meso|conditional-rct-data-property|title-summary-objective-and-rct-chain|misplaced-sparsity-modifier
    category: 复合标题与研究设计术语
    dossier_locator:
      - H1 与 Title 字段（第 27、31 行）
      - One-sentence complete-Idea summary 与 Positioning（第 32、34 行）
      - Primary research question 与 Objective 4（第 60、67 行）
      - 第五条 Evidence chain 标题及 Contribution 段（第 314、376、397、405 行）
    current_problem: >-
      “稀疏”在“条件性稀疏 RCT 次要再分析”等复合短语中直接修饰 RCT，容易被理解为随机试验设计、样本或随机化本身稀疏；正文实际说明的是两项试验只有少量离散访视的重复测量。该误读发生在标题、摘要和主要问题等核心入口。
    target_state: >-
      “稀疏”只修饰重复测量或访视数据，并在首次入口明确该数据性质如何限制分析，不再让其修饰 RCT。
    required_change_or_replacement: >-
      将标题及同类短语统一改为“基于稀疏重复测量的条件性 RCT 次要再分析”或等义的直接描述；将“实际稀疏 RCT 访视”改为“RCT 中少数预定访视的实测数据”。首次出现时用一句直接说明界定离散访视及不能推断连续轨迹。
    content_to_preserve: >-
      保留次要分析、条件性启动、两项试验分开报告、D7/D8 实际访视、投影失败替代分析以及不插值连续轨迹的全部限定。
    acceptance_test: >-
      全文检索不再出现“稀疏 RCT”或让“稀疏”附着于试验本身的结构；每一处均明确修饰“重复测量”或“访视数据”，且标题替换后的修饰关系无歧义。
    term_or_phrase: 条件性稀疏 RCT 次要再分析
    recommended_form_or_plain_description: 基于少量离散访视重复测量的条件性 RCT 次要再分析
    evidence_basis: >-
      dossier 第 54 行把实际限制写为“重复测量稀疏”，第 261 行明确仅支持访视特异或离散变化且不插值为连续轨迹；因此可用文件自身的直接描述修复，无须创造新术语。
    first_use_definition: 两项 RCT 仅在少数预定访视提供重复测量，因此再分析限于 D7/D8 的访视特异结局，不把这些数据解释为连续轨迹。
    competing_forms_and_locators:
      - “条件性稀疏 RCT 次要再分析”——第 27、31、34、67、314、376、397、405 行
      - “实际稀疏 RCT 访视”——第 60 行
      - “重复测量稀疏”——第 54 行
      - “稀疏 D1/D4/D7 或 D0/D4/D8”——第 261 行
  - finding_id: LA-002
    severity: major
    finding_kind: terminology
    finding_level: meso
    finding_scope: concept_cluster
    scientific_role: validation-and-stopping-criteria
    normalized_locator: entry-units-dated-plan-methods-and-interpretation
    failure_mode: generic-gate-metaphor
    fingerprint: meso|validation-and-stopping-criteria|entry-units-dated-plan-methods-and-interpretation|generic-gate-metaphor
    category: 判定标准与停止条件术语
    dossier_locator:
      - One-sentence summary、Structured abstract 与 Core hypothesis（第 32、39–42、71 行）
      - Twenty-four-month minimum and dated gates 表（第 79、83–88 行）
      - Absolute simulation 与 RCT projection 方法（第 214–226、242–254 行）
      - Required analyses、Falsification 与 Interpretation（第 326、353、355–358、368–370 行）
    current_problem: >-
      “门”同时指资源准入、数据审计、模拟恢复阈值、错误高置信排除、外部验证、试验语义核验、投影适用性、泄漏判定和停止条件。一个项目化隐喻承载多种不同科学操作，且在摘要首次出现时没有说明判定对象，跨学科读者可能把一组预设标准误读为单一测试或流程状态。
    target_state: >-
      每个判定名称直接说明所核对的对象、判定标准及科学后果；R0/R1 等短标签只能在完整名称之后使用。
    required_change_or_replacement: >-
      按功能分别改写：“资源门”改为“资源与人员准入条件”，“审计与协议门”改为“数据审计及方案定稿条件”，“绝对恢复/假置信门”改为“预设模拟恢复与错误高置信排除标准”，“真正外部门”改为“不更新模型的独立数据库验证标准”，“试验语义门”改为“试验变量与访视语义核验条件”，“观测投影门/R1”改为“观测投影适用性与忠实度判定标准”。其他“门”也按其实际对象改为“标准”“条件”或“判定”。
    content_to_preserve: >-
      保留全部数值阈值、预先确定的时间点、自动替代路线、停止条件、不得用较好预测或随机化差异补救失败的限制，以及 R0/R1 的逻辑顺序。
    acceptance_test: >-
      全文读者可见内容中不再单独依赖“门”解释科学操作；每个保留的 R0/R1 短标签均在首次出现处与完整的核验或判定名称绑定，且所有原阈值和后果仍可定位。
    term_or_phrase: 资源门、恢复门、外部门、语义门、投影门及其他“门”式标签
    recommended_form_or_plain_description: 按实际功能写明资源准入条件、数据审计条件、模拟恢复判定标准、外部验证标准、试验语义核验条件或投影适用性与忠实度标准
    evidence_basis: >-
      dossier 自身在第 83–88、218–226 和 246–250 行分别列出不同输入、阈值和后果，证明这些标签对应的是多种不同操作，而非一个可共用名称的单一概念。
    first_use_definition: 本研究在预定时间点分别核对资源可用性、模拟恢复、独立数据库验证、试验语义和观测投影适用性；每组标准只决定其对应分析能否继续或应采用何种替代分析。
    competing_forms_and_locators:
      - “绝对模拟恢复门”“冻结观测投影门”——第 32、40 行
      - “绝对恢复/假置信门”“主要任务门”“外部门”——第 39、71、304 行
      - “资源门”“审计与协议门”“恢复与准入门”“开发冻结门”“真正外部门”“条件性 RCT 门”——第 83–88 行
      - “Gate R0”“Gate R1”“投影 fidelity 门”——第 110、246、250、276 行
      - “泄漏门”“符号门”“合取门”——第 304、355、370 行
  - finding_id: LA-003
    severity: major
    finding_kind: terminology
    finding_level: meso
    finding_scope: concept_cluster
    scientific_role: randomized-projected-visit-endpoint
    normalized_locator: summary-question-objective-projection-method-and-evidence
    failure_mode: mapping-score-and-endpoint-role-collapse
    fingerprint: meso|randomized-projected-visit-endpoint|summary-question-objective-projection-method-and-evidence|mapping-score-and-endpoint-role-collapse
    category: 核心结局与映射术语
    dossier_locator:
      - One-sentence summary、Expected result 与 Contribution（第 32、41、42 行）
      - Primary research question 与 Objective 4（第 60、67 行）
      - Conditional trial-observation projection 方法（第 242–252 行）
      - 第五条 Evidence chain 与 Planned outputs（第 314–320、347 行）
      - Contribution ladder 与 claim-support 表（第 383、406 行）
    current_problem: >-
      “冻结观测投影”“投影可观测状态摘要”“投影可观测摘要”“投影摘要”和 P_obs 在不同位置交替指计算映射、由实测锚点得到的一维评分、含死亡与出院排序的序数结局以及该结局上的组间比较。首次使用早于公式和排序定义，读者可能误以为潜在状态已被直接观测，或无法判断随机化比较的具体结局。
    target_state: >-
      分别命名固定计算映射、一维观测评分、访视特异序数结局和随机化组间比较；首次入口即可识别输入、输出和结局排序。
    required_change_or_replacement: >-
      将映射写为“使用阶段 II 最终观测方程把 D7/D8 共同生理指标映射为一维评分的预先固定计算式”；将 P_obs 写为“由 D7/D8 实测共同生理指标计算的一维评分（P_obs）”；将主要结局写为“死亡最差、仍住院者按 P_obs 排序、存活出院最优的访视特异序数结局”；将推断写为“治疗分配对该序数结局分布的组间差异”。定义后可使用 P_obs，但不得再用一个“投影摘要”同时代替上述四种角色。
    content_to_preserve: >-
      保留共同锚点资格、固定权重、SVD 计算、数值方向、eICU 忠实度检验、死亡和出院排序、probabilistic index、治疗组遮蔽以及不验证完整潜在状态或系统模型的边界。
    acceptance_test: >-
      从摘要到方法的每一处都能唯一判断其所指为映射、P_obs 分数、序数结局或组间比较；首次使用包含直接定义，全文一致性检查不再发现这些角色由同一未限定短语替代。
    term_or_phrase: 冻结观测投影／投影可观测状态摘要／投影可观测摘要
    recommended_form_or_plain_description: 由 D7/D8 实测共同生理指标按预先固定计算式得到的一维评分，以及将死亡、该评分和存活出院按预定顺序组合的访视特异序数结局
    evidence_basis: >-
      dossier 第 248 行给出计算式和 P_obs，第 250 行给出适用性与忠实度条件，第 252 行给出死亡、P_obs 和活着出院的排序；这些内部定义足以支持直接描述，但不支持在定义前使用含混的项目短标签。
    first_use_definition: 若阶段 II 和试验数据条件满足，将用预先固定的观测方程把 D7/D8 实测共同生理指标计算为一维评分，并分析死亡最差、仍住院者按该评分排序、存活出院最优的访视特异序数结局。
    competing_forms_and_locators:
      - “冻结观测投影门”“冻结观测投影”——第 32、40、60 行
      - “投影可观测状态摘要”——第 32、41、252 行
      - “投影可观测摘要”“投影摘要”——第 42、60、67、317–319、347、368、383、406 行
      - “RCT 可观测代理 P_obs”——第 248、250、252 行
      - “冻结 SVD 映射”“RCT 冻结投影器”——第 276、317 行
  - finding_id: LA-004
    severity: minor
    finding_kind: terminology
    finding_level: meso
    finding_scope: concept_cluster
    scientific_role: independent-rct-fallback-endpoint
    normalized_locator: summary-objective-method-evidence-and-output
    failure_mode: delayed-hybrid-endpoint-definition
    fingerprint: meso|independent-rct-fallback-endpoint|summary-objective-method-evidence-and-output|delayed-hybrid-endpoint-definition
    category: 替代结局术语
    dossier_locator:
      - One-sentence summary 与 Expected result（第 32、41 行）
      - Objective 4（第 67 行）
      - Automatic independent fallback（第 254 行）
      - Evidence chain、Planned outputs 与 interpretation tables（第 317–318、347、369、384、428 行）
    current_problem: >-
      “death-ranked SOFA”和“trial-specific independent secondary clinical-state reanalysis”在首次出现时以中英混合短标签代替结局结构，直至方法段才说明死亡、仍住院者 SOFA 和活着出院的排序。读者虽可在后文恢复含义，但在摘要和目标处需猜测其是死亡预测、SOFA 插补还是序数复合结局。
    target_state: >-
      首次出现即用中文直接说明三层排序，并在后文使用稳定的中文描述指代该独立替代结局。
    required_change_or_replacement: >-
      首次出现改为“以死亡为最差、仍住院者按 SOFA 由高到低排序、存活出院为最优的试验特异次要序数临床结局再分析”；后续可简称“该独立序数临床结局”，并把英文项目标签改为同一中文描述。
    content_to_preserve: >-
      保留该分析与阶段 II 表征相互独立、仅在投影分析不能进行且核心试验语义可核验时启动、两项试验分开分析及不得称为阶段 II 扰动或验证的限制。
    acceptance_test: >-
      摘要首次使用即给出三层排序；全文不再出现未解释的“death-ranked SOFA”或英文固定状态标签，且每处都明确该结局与阶段 II 表征独立。
    term_or_phrase: death-ranked SOFA；trial-specific independent secondary clinical-state reanalysis
    recommended_form_or_plain_description: 以死亡最差、仍住院者按 SOFA 排序、存活出院最优的试验特异次要序数临床结局再分析
    evidence_basis: >-
      dossier 第 254 行已直接定义三层排序和独立性，故可用该定义替代项目短标签，无须外部术语来源。
    first_use_definition: 投影分析不能进行而试验语义仍可核验时，改用死亡最差、仍住院者按 SOFA 由高到低排序、存活出院最优的试验特异次要序数临床结局。
    competing_forms_and_locators:
      - “death-ranked SOFA”——第 32、41、67、317、347、384、428 行
      - “trial-specific independent secondary clinical-state reanalysis”——第 254 行
      - “trial-specific clinical-state 再分析”——第 318 行
      - “独立 SOFA 分支／端点”——第 42、88、110、125、254、276、356、369 行
  - finding_id: LA-005
    severity: minor
    finding_kind: terminology
    finding_level: meso
    finding_scope: concept_cluster
    scientific_role: central-dynamic-system-representation
    normalized_locator: title-abstract-objectives-evidence-and-interpretation
    failure_mode: inconsistent-core-object-naming
    fingerprint: meso|central-dynamic-system-representation|title-abstract-objectives-evidence-and-interpretation|inconsistent-core-object-naming
    category: 核心研究对象命名
    dossier_locator:
      - H1、Title、summary 与 Primary question（第 27、31、32、60 行）
      - Objective and hypothesis 与 Objective 2（第 39、65 行）
      - Success definition、Evidence chains 与 Interpretation（第 92、287、311、352、367、370 行）
      - Contribution 与 closest-work 表（第 376、392、393、403 行）
    current_problem: >-
      同一核心研究对象在“候选动态系统表征”“候选全病程表示”“候选状态表示”“候选系统表征”“候选表示”和“候选架构”之间切换；“复杂候选”有时又省略“模型”。读者能大致恢复指代，但难以判断这些名称是否表示同一总体对象、其中一个模型候选或研究框架。
    target_state: >-
      为总体研究对象保留一个定义清楚的名称，并把框架、具体模型候选和拟合模型作为不同角色另行命名。
    required_change_or_replacement: >-
      统一以“候选动态系统表征”指总体研究对象，并在首次使用处给出直接定义；需要指具体方法时写“受限的复杂模型候选”，需要指研究安排时写“研究框架”，需要指拟合对象时写“模型”。把仅为词形变化的“候选全病程表示／候选状态表示／候选表示”改为统一形式，同时保留真正不同的科学角色。
    content_to_preserve: >-
      保留候选和计划状态、患者时间状态及转移的推断单位、状态—行动—观察分工、复杂模型可自动降级，以及只有通过预设标准后才能解释结构的限定。
    acceptance_test: >-
      全文一致性检查确认总体对象只使用“候选动态系统表征”；“研究框架”“模型候选”和“模型”各自只用于对应角色，且首次定义不依赖另一个未定义短标签。
    term_or_phrase: 候选动态系统表征及其“表示／架构／复杂候选”变体
    recommended_form_or_plain_description: 候选动态系统表征（对患者时变状态、状态转移、生理测量、治疗行动和测量过程进行知识约束的统计表示）
    evidence_basis: >-
      标题和主要问题确立“候选动态系统表征”为主名，第 208–210 行描述其统计对象和可解释范围；因此可以统一名称，同时把“模型候选”和“研究框架”保留给不同角色。
    first_use_definition: 候选动态系统表征是对患者时变状态与转移、生理测量、治疗行动和测量过程进行知识约束的统计表示，其结构解释须满足预设恢复与外部验证标准。
    competing_forms_and_locators:
      - “候选动态系统表征”——第 27、31、32、60 行
      - “候选全病程表示”“候选状态表示”——第 39、65 行
      - “计划跨数据库候选系统表征”——第 92、311 行
      - “候选表示”“最小全病程候选表示”——第 287、370 行
      - “候选架构”“复杂候选”——第 50、39、40、71、85、95 行
  - finding_id: LA-006
    severity: major
    finding_kind: terminology
    finding_level: meso
    finding_scope: concept_cluster
    scientific_role: external-validation-update-regimes
    normalized_locator: abstract-work-packages-methods-evidence-and-risk
    failure_mode: bilingual-regime-name-inconsistency
    fingerprint: meso|external-validation-update-regimes|abstract-work-packages-methods-evidence-and-risk|bilingual-regime-name-inconsistency
    category: 外部验证与参数更新术语
    dossier_locator:
      - Structured abstract Approach（第 40 行）
      - Success definition 与 Work packages（第 98、109 行）
      - Public ICU database roles（第 134 行）
      - Hospital-primary validation（第 230–240 行）
      - 第四条 Evidence chain（第 306–312 行）
      - Falsification、Contribution 与 risk matrix（第 355、365–366、382、404、423、427 行）
    current_problem: >-
      外部数据库分区和更新层级在“适配区／adaptation”“最终测试区／test／untouched final test”“零更新／zero update／zero-update”“仅校准／adaptation-only calibration”“仅观测层更新／adaptation-only observation-layer update／decoder adaptation”以及“transport updating/development”之间切换。多个核心验证操作因中英变体和角色省略而难以稳定对应。
    target_state: >-
      数据分区与四种模型更新操作分别采用一个中文主名，首次出现时直接定义是否使用最终检验数据、允许更新哪些参数以及是否仍属于外部验证。
    required_change_or_replacement: >-
      统一使用“适配医院组”“独立最终检验医院组”“不更新模型的外部检验”“仅更新校准参数的外部检验”“仅更新观测模型参数的外部检验”“全模型重新拟合（运输性再开发，不属于外部验证）”。如确需英文短语，只能在中文完整定义后括注一次，不再与中文形式交替使用。
    content_to_preserve: >-
      保留医院优先分区、跨分区患者处理、最终检验医院不参与模型选择或参数估计、执行顺序、有限更新不能替代不更新模型检验，以及全模型重拟合不属于外部验证的全部规则。
    acceptance_test: >-
      全文每一数据分区和更新层级均可唯一映射到上述六个名称；不再混用 adaptation/test/zero-update/decoder adaptation 等未定义变体，且各层允许的数据用途和外部验证地位仍明确。
    term_or_phrase: adaptation/test/zero update/calibration/observation-layer update/transport updating
    recommended_form_or_plain_description: 适配医院组、独立最终检验医院组、不更新模型的外部检验、仅校准参数更新、仅观测模型参数更新及全模型运输性再开发
    evidence_basis: >-
      dossier 第 230–240 行已经规定分区比例、数据隔离及更新顺序；这些操作可直接按“使用哪组数据、更新哪些参数、是否属于外部验证”描述，无须保留多套混合标签。
    first_use_definition: 外部数据库预先分为适配医院组和独立最终检验医院组；最终检验依次报告不更新模型、仅更新校准参数和仅更新观测模型参数的结果，全模型重新拟合仅属于运输性再开发。
    competing_forms_and_locators:
      - “适配区／adaptation”——第 40、98、109、134、230、234、237、240、308–312 行
      - “最终测试区／未触碰 test／untouched final test”——第 40、98、230、240、382 行
      - “零更新／zero update／zero-update”——第 40、87、98、109、240、250、309、355、365–366、382、404、427 行
      - “仅校准／adaptation-only calibration”——第 40、87、109、240、309 行
      - “仅观测层更新／adaptation-only observation-layer update／adaptation-only decoder”——第 40、87、109、240、309 行
      - “full refit／transport updating/development”——第 240、310、312 行
  - finding_id: LA-007
    severity: minor
    finding_kind: language
    finding_level: meso
    scientific_role: project-status-and-output-labels
    normalized_locator: positioning-status-tables-branch-labels-and-final-boundary
    failure_mode: raw-internal-token-leakage
    fingerprint: meso|project-status-and-output-labels|positioning-status-tables-branch-labels-and-final-boundary|raw-internal-token-leakage
    category: 中英混合语体与项目内部标签
    dossier_locator:
      - Positioning 与 dated plan（第 34、83、87 行）
      - Current verified-resource table（第 120–129 行）
      - Conditional RCT method 与 evidence chain（第 242、246、252、254、317–318 行）
      - Contribution 与 claim-support table（第 376、383–384、397、403–410 行）
      - Identity and final stop boundary（第 439 行）
    current_problem: >-
      普通中文正文和自由表格中直接暴露项目内部或软件状态词，例如“benchmark/resource”“data-access no-go”“verified/unverified/not generated/project-local derivative”“projection-pass/fallback/stop”“supported/qualified/unsupported”“editorial_repositioning/scientific_discovery”“identity_status/new_idea_required”。这些不是固定脚手架，也未作为标准术语定义，导致正式科研语体在多处切换为内部状态记录。
    target_state: >-
      普通正文和自由标签使用自然中文与标准科学术语；必要缩写、数据库名、数学符号和合同固定标签保留不动。
    required_change_or_replacement: >-
      将上述自由文本分别改为“基准数据与可复用资源”“因数据访问不足而停止该路线”“已核验／未核验／尚未生成／项目内衍生材料”“投影标准通过的分析／独立替代分析／停止分析”“有充分支持／仅在限定条件下支持／不支持”“编辑性重新定位／科学发现”“研究身份保持不变／需作为新的研究构想处理”。只修改普通 prose 和自由表格，不翻译合同固定标题、字段或公式标识。
    content_to_preserve: >-
      保留每个状态的证据含义、条件性、停止后果、研究身份边界及所有标准缩写和数据库专名；不得把“未核验”润色成“已完成”。
    acceptance_test: >-
      对读者可见的普通正文和自由标签进行全文检查后，上述内部状态词均已被自然中文替代或在首次出现处有标准定义；ICU、RCT、SOFA、EHR、数据库名、数学符号以及合同固定脚手架未被误改。
  - finding_id: LA-008
    severity: minor
    finding_kind: language
    finding_level: micro
    finding_scope: occurrence
    scientific_role: complete-idea-summary
    normalized_locator: section-one-one-sentence-summary
    failure_mode: overloaded-multi-branch-sentence
    fingerprint: micro|complete-idea-summary|section-one-one-sentence-summary|overloaded-multi-branch-sentence
    category: 可读性与句法负荷
    dossier_locator: Section 1 One-sentence complete-Idea summary（第 32 行）
    current_problem: >-
      单句同时承载数据来源与审计、四阶段病程、两类验证、阶段条件、两个试验及访视、投影失败替代路线和六项禁止主张；多个长定语与条件链竞争，读者难以一次识别“构建—验证—条件性再分析”三项主要动作。
    target_state: >-
      在保持“一句话”字段约束的前提下，以三个并列且层级清楚的动作组织信息，核心对象、验证方式和条件性试验分析均可一次识别。
    required_change_or_replacement: >-
      将该句重组为“构建……；按预设恢复标准并在独立数据库中检验……；仅在……时再分析……”的平行结构，删除可移至相应正文的实现细节，并把非因果边界压缩为一个不歧义的末尾分句。同步采用 LA-001、LA-002、LA-003 和 LA-004 的直接术语，但仍保持一个完整句子。
    content_to_preserve: >-
      保留 24 个月阶段 I–II、两个须确认访问和完成可观测性审计的公共 ICU 数据库、发病前至结局范围、独立数据库检验、EXIT-SEP D7 与 XBJ-SCAP D8、条件性启动、独立替代结局及不支持因果网络、连续动力学、控制或数字孪生的边界。
    acceptance_test: >-
      修订后仍只有一个句号终止的一句话；主句具有三个平行动词结构，每个条件只附着于其对应动作，且没有未定义的项目短标签或超过两层的嵌套条件。
  - finding_id: LA-009
    severity: minor
    finding_kind: language
    finding_level: meso
    finding_scope: concept_cluster
    scientific_role: interpretation-boundary
    normalized_locator: summary-background-methods-evidence-and-claim-tables
    failure_mode: near-verbatim-boundary-repetition
    fingerprint: meso|interpretation-boundary|summary-background-methods-evidence-and-claim-tables|near-verbatim-boundary-repetition
    category: 简洁性与重复
    dossier_locator:
      - Summary、Contribution 与 non-hypotheses（第 32、42、54、73 行）
      - Projection method 与 secondary diagnostics（第 252、254、261、265 行）
      - Evidence chains 与 interpretation matrix（第 296、304、312、319–320、368–370 行）
      - Contribution/closest-work/claim-support（第 376、385、393–410 行）
    current_problem: >-
      “不验证潜在动力学、转移边、中介、控制或整个系统模型”及“不构成因果网络、数字孪生或临床工具”等边界以近乎同一长清单在多个相邻与后续单元重复。科学限制本身必要，但词面反复增加长度并遮蔽各处的局部结论。
    target_state: >-
      每个局部单元保留与其结论直接相关的边界，同时由经批准的叙事位置保留完整限制；语言评估不指定哪一个推理位置承担完整版本。
    required_change_or_replacement: >-
      标记上述近似重复清单供叙事评估确定完整限制的权威位置；在该位置确定后，将其他位置改为只陈述该局部结果不能支持的最近一层推断，或采用不削弱含义的简短边界。不得自行删除任何科学上不同的限制，也不得添加跨节指针来替代必要说明。
    content_to_preserve: >-
      保留预测与因果、可观测摘要与潜在状态、适配后运输与天然稳健、独立 SOFA 结局与阶段 II 表征、研究候选与数字孪生或控制等所有实质区别。
    acceptance_test: >-
      经叙事位置确认后，完整限制仍至少在批准位置存在；其余每处仅保留局部必要边界，全文不再出现三处以上近乎逐字相同的长清单，且任何允许的主张强度均未扩大。
  - finding_id: LA-010
    severity: minor
    finding_kind: language
    finding_level: micro
    finding_scope: occurrence
    scientific_role: clinical-guideline-boundary
    normalized_locator: background-rationale-final-sentence
    failure_mode: misattached-jurisdiction-modifier
    fingerprint: micro|clinical-guideline-boundary|background-rationale-final-sentence|misattached-jurisdiction-modifier
    category: 修饰语附着与句法清晰度
    dossier_locator: Background, current state, gap, significance, and rationale 第五段末句（第 54 行）
    current_problem: >-
      “SSC 2026 对未获当地监管批准辖区使用 XueBiJing 的建议仍谨慎”使“未获当地监管批准”表面附着于“辖区”，并缺少明确的处所结构；读者需要回读才能判断所指是“在尚未批准该用法的辖区使用 XueBiJing”。
    target_state: >-
      明确辖区、监管批准状态和使用行为之间的修饰关系，同时保持引文所支持的谨慎程度。
    required_change_or_replacement: >-
      改为“SSC 2026 对在尚未获得当地监管批准的辖区使用 XueBiJing 持谨慎态度”或同等直接结构；不要把“谨慎”强化为“禁止”，也不要改变后句的临床推广边界。
    content_to_preserve: >-
      保留 SSC 2026 引文、当地监管批准的条件、XueBiJing 专名及不支持无条件国际临床推广的结论。
    acceptance_test: >-
      修订句含明确的“在……辖区使用……”处所结构，修饰语只附着于监管批准状态，且建议强度仍为谨慎而非禁止。
unresolved_issues:
  - LA-001
  - LA-002
  - LA-003
  - LA-004
  - LA-005
  - LA-006
  - LA-007
  - LA-008
  - LA-009
  - LA-010
---

# Language Assessment Report

**Assessment ID**: language-assessment-r002  
**Target Language**: Chinese，保留规范的英文缩写、数据库名、方法名和数学符号  
**Discipline**: 重症医学、临床流行病学、纵向统计、系统辨识与医学 AI 交叉研究  
**Target Journal**: 未指定  
**Scope**: complete_idea_dossier  
**Date**: 2026-07-20

---

## Overall Language Readiness

**Level**: major_language_revision

**Recommendation**: revise_language

核心科学计划仍可辨认，语法和前瞻性时态总体稳定；但标题和主要入口中的“稀疏 RCT”修饰关系、多个研究判定的“门”式项目标签、RCT 投影结局的角色混用，以及外部验证更新层级的中英混称，妨碍跨学科读者准确识别核心设计与结局。修订需要系统统一术语和入口表述，而不是仅做局部校对。

---

## Dimension Scores

| Dimension | Score (1–10) | Severity |
|-----------|-------------|----------|
| Grammar & Syntax | 8 | pass |
| Academic Register & Tone | 7 | pass |
| Terminology Consistency | 4 | fail |
| Tense & Voice Conventions | 9 | pass |
| Conciseness & Redundancy | 5 | borderline |
| Readability & Flow | 5 | borderline |

---

## Hard Gate Status

**Overall**: fail

| Gate | Status | Detail |
|------|--------|--------|
| Grammar error density | pass | 1 个明确的局部修饰语附着问题；按全文规模远低于每 500 词 3 个错误 |
| Academic register | pass | 无系统性口语表达；问题主要是内部状态词和中英混合术语，不构成非正式语体硬性失败 |
| Terminology coherence | fail | 3 个核心命名簇存在竞争形式或角色混用（研究对象、RCT 投影结局、外部验证更新层级）；标题“稀疏 RCT”另触发完整构想的误导性核心术语规则 |
| Tense systematic violation | pass | 这是前瞻性研究构想，计划、条件和将来行动的时态与研究状态一致 |

---

## Strengths

- 全文持续把计划产物与已生成结果分开，并反复限制预测、因果、控制和数字孪生主张的强度。
- 前瞻性行动、条件性分析和停止后果的时态一致，没有把未完成工作写成既成结果。
- Sepsis-3、SOFA、ICU、RCT、数据库专名和数学符号总体稳定；固定脚手架也未被误当作语言问题。
- 表格中的阈值、时间点和分析顺序大多采用平行结构，便于定位具体操作。

---

## Specific Issues

### Chinese Academic Clarity

LA-001、LA-002、LA-003、LA-006 和 LA-007 是主要清晰度问题：复合修饰语、项目化判定标签、核心结局角色以及未定义的中英混合状态词使读者需要跨节回查。LA-008 和 LA-009 分别涉及入口句负荷和近似重复限制。完整替换、保留内容与验收条件均记录在前置结构化发现中。

### Grammar & Syntax

LA-010 是一个局部修饰语附着问题。除此之外未发现达到硬性阈值的明确语法错误模式；长句的主要代价计入可读性，而非语法错误密度。

### Academic Register & Tone

LA-007 记录了普通中文正文向内部状态记录语体的反复切换。正文没有系统性口语、宣传性断言或不当感叹表达。

### Terminology Consistency

| id | term_or_phrase | locator | reader_effect | action_in_frontmatter |
|---|---|---|---|---|
| LA-001 | 条件性稀疏 RCT 次要再分析 | 标题、摘要、主要问题、目标与第五条证据链 | 可能把稀疏性误附着于试验设计或样本，而非重复测量 | yes |
| LA-002 | 多种“门”式判定标签 | 摘要、日期计划、方法、停止条件与解释表 | 无法仅凭标签识别所判定的对象和后果 | yes |
| LA-003 | 冻结观测投影／投影可观测摘要 | 摘要、问题、方法、证据链与贡献表 | 映射、分数、序数结局和组间比较互相混用 | yes |
| LA-004 | death-ranked SOFA 等替代结局标签 | 摘要、目标、方法、证据链与输出 | 定义延后且中英混合，需猜测结局结构 | yes |
| LA-005 | 候选动态系统表征及“表示／架构”变体 | 标题、摘要、目标、证据链与解释表 | 总体研究对象、框架和模型候选边界不稳定 | yes |
| LA-006 | 外部验证分区与更新层级 | 摘要、工作包、方法、证据链与风险表 | 同一层级的中英变体难以稳定映射 | yes |

未把规范缩写、数据库名、数学符号、引文标识或合同固定脚手架列为术语问题。

### Tense & Voice Conventions

未发现系统性时态或语态问题。计划、条件、假设和停止动作与前瞻性 Idea 状态相符。

### Conciseness & Redundancy

LA-009 记录了跨多处近似重复的解释边界；完整限制应保留，但具体保留位置需由叙事评估确定。LA-008 的入口摘要还因过多条件和细节集中于一个句子而失去简洁性。

### Readability & Flow

LA-008 是最明显的局部句法负荷；LA-003、LA-006 和 LA-007 的术语切换进一步增加回读。这里不评价五段推理链、章节顺序或跨节披露安排。

---

## Language Revision Priorities

1. **Terminology**: 4 个主要问题 — 先修复标题修饰关系、将不同科学判定改为功能性名称、分开 RCT 映射/评分/结局/比较，并统一外部验证更新层级。
2. **Terminology**: 2 个次要问题 — 统一核心研究对象名称，并在首次出现处直接定义独立 SOFA 序数结局。
3. **Academic register**: 1 个问题 — 将自由文本中的项目内部状态词改为自然中文，同时保留规范缩写和固定脚手架。
4. **Readability and concision**: 2 个问题 — 在不改变单句字段约束和科学边界的前提下重组摘要，并在叙事位置获批后压缩近似重复限制。
5. **Grammar**: 1 个问题 — 修正监管辖区句的修饰语附着。

---

## Re-Assessment Status (if applicable)

不适用。本次是未接触既往问题清单、评分、决定、版本差异或修订记录的完整构想盲审。

---

## Assessment Notes

- 唯一读取的项目研究产物是 frontmatter `files_read` 所列 v003 dossier；嵌入式读者交接来自该 dossier 的 Primary audience，不对应另一文件。
- 目标语言按中文处理，英文仅在规范缩写、专名、标准方法名、公式和必要的一次性括注中保留。固定的 research-idea.v3 标题、字段、Evidence-chain 标签和 Claim-Support 表头未评分、未建议翻译。
- 学科约定按生物医学/临床研究为主、兼顾医学 AI 与纵向统计处理；未指定期刊，因此未施加期刊专属格式。
- 所有六个维度、四项硬性判定和四个完整构想覆盖步骤均已完成。未评价科学有效性、创新性、影响力、可行性、论证结构或期刊适配性。
- 术语替换均来自 dossier 已有的直接操作定义，不需要检索外部术语来源；本报告没有把扫描器候选清单持久化为术语表。
