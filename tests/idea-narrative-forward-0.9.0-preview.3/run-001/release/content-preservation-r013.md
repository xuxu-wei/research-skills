---
schema_version: research-idea-content-preservation-check.v1
check_id: content-preservation-I01-001-r013
review_id: content-preservation-review-I01-001-r013
reviewer_skill: idea-narrative-assessor
reviewer_instance_id: fresh-content-preservation-r013
workflow_id: RID-SEPSIS-CSM-20260717-001
round_id: r013
input_artifact_ids:
  - idea-dossier-I01-001-v012
  - idea-dossier-I01-001-v013
  - protected-content-register-I01-001-v012
  - revision-delta-I01-001-v012-to-v013
input_versions: [v012, v013, v012, v012-to-v013]
inputs:
  prior_dossier:
    artifact_id: idea-dossier-I01-001-v012
    version: v012
    path: tests/idea-narrative-forward-0.9.0-preview.3/run-001/release/idea-dossier-v012.md
  revised_dossier:
    artifact_id: idea-dossier-I01-001-v013
    version: v013
    path: tests/idea-narrative-forward-0.9.0-preview.3/run-001/release/idea-dossier-v013.md
  protected_content_register:
    artifact_id: protected-content-register-I01-001-v012
    version: v012
    path: tests/idea-narrative-forward-0.9.0-preview.3/run-001/release/protected-content-register-v012.yaml
  revision_delta:
    artifact_id: revision-delta-I01-001-v012-to-v013
    version: v012-to-v013
    path: tests/idea-narrative-forward-0.9.0-preview.3/run-001/release/revision-delta-v012-to-v013.md
files_read:
  - tests/idea-narrative-forward-0.9.0-preview.3/run-001/release/idea-dossier-v012.md
  - tests/idea-narrative-forward-0.9.0-preview.3/run-001/release/idea-dossier-v013.md
  - tests/idea-narrative-forward-0.9.0-preview.3/run-001/release/protected-content-register-v012.yaml
  - tests/idea-narrative-forward-0.9.0-preview.3/run-001/release/revision-delta-v012-to-v013.md
isolation_mode: fresh_subagent
prior_scores_visible: false
source_edits_performed: false
decision: scientific_content_preserved
protected_item_checks:
  - protected_id: PCR-001
    prior_locator: "frontmatter identity_anchor; Research question, objectives, and core hypothesis > Primary research question"
    revised_locator: "frontmatter identity_anchor; Research question, objectives, and core hypothesis > Primary research question"
    semantic_status: preserved
    evidence: "三项研究问题仍覆盖全病程连续体、患者—时间状态与转移、跨数据库稳定性以及仅在阶段 II 成功后开展的试验观测映射；仅将试验输入统一定义为每项试验的合格共同指标。"
  - protected_id: PCR-002
    prior_locator: "frontmatter identity_anchor; Structured abstract > Objective and hypothesis"
    revised_locator: "frontmatter identity_anchor; Structured abstract > Objective and hypothesis; Research content and work packages > Twenty-four-month required study objectives and dated milestones"
    semantic_status: preserved
    evidence: "阶段 I–II 仍须在 24 个月内完成，范围仍含模型开发、恢复检验、两项主要预测任务和跨数据库验证；阶段 III 仍安排在该完成标准之后并具有条件性。"
  - protected_id: PCR-003
    prior_locator: "Research question, objectives, and core hypothesis > Core hypothesis"
    revised_locator: "Research question, objectives, and core hypothesis > Core hypothesis"
    semantic_status: preserved
    evidence: "核心假设仍以双数据库支持及预先固定尺度、状态数、滞后和锚定为前提，且仍限定至多一个复杂候选模型；新术语“受预设约束”明确了原有约束来源，没有增强假设。"
  - protected_id: PCR-004
    prior_locator: "Title, summary, audience, and positioning > Positioning and contribution frame; Contribution and evidence ladder"
    revised_locator: "Title, summary, audience, and positioning > Positioning and contribution frame; Contribution, innovation, impact, application, and closest-work comparison > Contribution and evidence ladder"
    semantic_status: preserved
    evidence: "研究仍定位为有界证据整合、预设跨数据库验证、基准和资源建设；增量仍来自五层证据的依赖式连接，而非宣称方法组件本身新颖。"
  - protected_id: PCR-005
    prior_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Research identity and final boundary"
    revised_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Research identity and final boundary"
    semantic_status: preserved
    evidence: "研究问题、目标、对象、核心证据基础和患者—时间状态与转移推断单位仍共同界定身份；取消连续体、替换证据基础或改变推断单位仍要求另立研究。"
  - protected_id: PCR-006
    prior_locator: "frontmatter identity_anchor > study_object and primary_unit_of_inference"
    revised_locator: "frontmatter identity_anchor > study_object and primary_unit_of_inference"
    semantic_status: preserved
    evidence: "研究对象仍是纵向、以脓毒症为中心的 ICU 患者系统，推断单位仍为患者—时间状态与状态转移，并继续处理患者及医院聚类。"
  - protected_id: PCR-007
    prior_locator: "Title, summary, audience, and positioning > 三阶段导航; Research content and work packages"
    revised_locator: "Title, summary, audience, and positioning > 三阶段导航; Research content and work packages"
    semantic_status: preserved
    evidence: "阶段 I 的月 0–6、阶段 II 的月 3–24、工作范围及阶段 III 的 24 月后条件启动均未改变；“最低交付”改为“必须完成的研究范围”未改变时间或成败边界。"
  - protected_id: PCR-008
    prior_locator: "Research design and methods > Protocol locks for the two primary clinical tasks > 人群"
    revised_locator: "Research design and methods > Protocol locks for the two primary clinical tasks > 人群"
    semantic_status: preserved
    evidence: "发病前成人首个合格 ICU 入住、至少 12 小时历史及未发病风险集规则，以及发病后首次新发、延迟进入、分层和左截断规则均原样保留。"
  - protected_id: PCR-009
    prior_locator: "Research design and methods > Mutually exclusive post-onset state and event system"
    revised_locator: "Research design and methods > Mutually exclusive post-onset state and event system"
    semantic_status: preserved
    evidence: "六类互斥状态、12 小时间隔、固定优先级、同刻处理和事件时间敏感性分析均保留；出 ICU 与生理恢复仍不等同，转院仍非普通独立删失。"
  - protected_id: PCR-010
    prior_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Resources and governance"
    revised_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Feasibility and resources"
    semantic_status: preserved
    evidence: "两个主要数据库、最多 4 个状态维度、最多 3 个切换机制、至多一个复杂候选模型以及两项主要预测任务和两项次要诊断的范围均未改变；排除事项仍相同。"
  - protected_id: PCR-011
    prior_locator: "Research design and methods > Hospital-based cross-database validation"
    revised_locator: "Research design and methods > Hospital-based cross-database validation"
    semantic_status: preserved
    evidence: "医院级分层、固定种子 20260717、30% 适配与 70% 预先隔离验证分配均保留；同库未参与开发医院验证与跨数据库验证仍分开报告。"
  - protected_id: PCR-012
    prior_locator: "Research design and methods > Conditional trial observation mapping and secondary analyses > Analysis targets"
    revised_locator: "Research design and methods > Conditional trial observation mapping and secondary analyses > Analysis targets"
    semantic_status: preserved
    evidence: "两试验仍分开分析；EXIT-SEP 的 1,817/1,760 与第 7 日，以及 XBJ-SCAP 的 710/675、改良意向治疗降级条件、第 8 日和敏感性人群均保留。"
  - protected_id: PCR-013
    prior_locator: "Title, summary, audience, and positioning > four evidence classes; Interpretation of the planned evidence"
    revised_locator: "Title, summary, audience, and positioning > four evidence classes; Expected outputs, falsification criteria, and interpretations > Interpretation of the planned evidence"
    semantic_status: preserved
    evidence: "预测任务、模拟恢复、跨数据库稳定性和随机试验组间差异仍被明确为回答不同问题的四类证据，并继续要求分别报告、不得互相替代。"
  - protected_id: PCR-014
    prior_locator: "Data, materials, and existing evidence base > Public ICU databases and planned roles"
    revised_locator: "Data, materials, and existing evidence base > Public ICU databases and planned roles"
    semantic_status: preserved
    evidence: "MIMIC-IV v3.1、eICU-CRD v2.0 和预先指定的 HiRID 或 AmsterdamUMCdb 的开发、外部及备份角色与审计前提均未改变。"
  - protected_id: PCR-015
    prior_locator: "Data, materials, and existing evidence base > Public ICU databases and planned roles > 共同概念层 and 双数据库审计"
    revised_locator: "Data, materials, and existing evidence base > Public ICU databases and planned roles > 共同概念层 and 双数据库审计"
    semantic_status: preserved
    evidence: "共同概念层仍只纳入语义、单位、时间戳和可用时间均经核验的变量；拟合前审计的样本、事件、转移、医院、覆盖、接口及治疗行动项目均保留。"
  - protected_id: PCR-016
    prior_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Current feasibility and evidence status"
    revised_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Current feasibility and evidence status"
    semantic_status: preserved
    evidence: "数据库存在、版本和文献仍标为已核验，而访问、协议、提取与校验仍未核验；项目样本、事件、转移、医院和接口计数仍标为尚未生成。"
  - protected_id: PCR-017
    prior_locator: "Data, materials, and existing evidence base > Trial data considered for conditional stage III analyses"
    revised_locator: "Data, materials, and existing evidence base > Trial data considered for conditional stage III analyses"
    semantic_status: preserved
    evidence: "EXIT-SEP 和 XBJ-SCAP 的随机例数、分析集、死亡或状态信息、SOFA 及候选实验室指标的既有计数均未改变。"
  - protected_id: PCR-018
    prior_locator: "frontmatter identity_anchor > core_data_or_evidence_base; Evidence chains > 数据支持、锚定与模拟恢复"
    revised_locator: "frontmatter identity_anchor > core_data_or_evidence_base; Evidence chains > 数据支持、锚定与模拟恢复"
    semantic_status: preserved
    evidence: "核心证据仍由文献与专家先验、纵向公共 ICU 数据及满足个体数据和语义资格后才可用的两项随机试验数据组成。"
  - protected_id: PCR-019
    prior_locator: "Data, materials, and existing evidence base > Variable-role separation"
    revised_locator: "Data, materials, and existing evidence base > Variable-role separation"
    semantic_status: preserved
    evidence: "生理测量、治疗、测量过程、标签和基线协变量的角色仍分离；治疗非锚点、未测非正常、接口缺失非生理状态及双重用途字段独立处理均保留。"
  - protected_id: PCR-020
    prior_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Resources and governance; Current feasibility and evidence status"
    revised_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Feasibility and resources; Current feasibility and evidence status"
    semantic_status: preserved
    evidence: "最低人员角色清单未改变，且具名人员和可用工时仍标为未核验；角色定义仍明确不等于人员承诺。"
  - protected_id: PCR-021
    prior_locator: "Research design and methods > Trial semantics and common-observation eligibility"
    revised_locator: "Research design and methods > Trial semantics and common-observation eligibility"
    semantic_status: preserved
    evidence: "阶段 III 启动前仍须具备个体级授权、原始试验文件或持有人确认，并核验分组、分析集、中心、访视窗及死亡、住院、出院和转院语义。"
  - protected_id: PCR-022
    prior_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Current feasibility and evidence status"
    revised_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Current feasibility and evidence status"
    semantic_status: preserved
    evidence: "现有试验材料仍仅为衍生报告，不能替代授权和原始文件；共同指标、单位和访视映射仍未核验，白细胞与 C 反应蛋白仍只是候选。"
  - protected_id: PCR-023
    prior_locator: "Research design and methods > Protocol locks for the two primary clinical tasks > 主要发病前任务"
    revised_locator: "Research design and methods > Protocol locks for the two primary clinical tasks > 主要发病前任务"
    semantic_status: preserved
    evidence: "第 12 小时起每 12 小时预测、最多 24 小时且至少 12 小时历史、未来 12 小时首次发病 CIF、原因别风险模型及 Brier 与校准指标均未改变。"
  - protected_id: PCR-024
    prior_locator: "Research design and methods > Protocol locks for the two primary clinical tasks > 主要发病后任务"
    revised_locator: "Research design and methods > Protocol locks for the two primary clinical tasks > 主要发病后任务"
    semantic_status: preserved
    evidence: "第 7 日有利状态概率、恢复与存活离开 ICU 分报、互斥多状态与 Aalen–Johansen、第 14 日敏感性及主要和次要评价均保留。"
  - protected_id: PCR-025
    prior_locator: "Research design and methods > Protocol locks for the two primary clinical tasks > 事件时间 and 信息可用时间"
    revised_locator: "Research design and methods > Protocol locks for the two primary clinical tasks > 事件时间 and 信息可用时间"
    semantic_status: preserved
    evidence: "培养与抗菌药 72/24 小时配对、基线 SOFA、感染前 48 至后 24 小时窗、首次满足发病时间及较晚可用时间规则均原样保留。"
  - protected_id: PCR-026
    prior_locator: "Research design and methods > Protocol locks for the two primary clinical tasks > competing events, ordering, sensitivity labels, and leakage audit"
    revised_locator: "Research design and methods > Protocol locks for the two primary clinical tasks > competing events, ordering, sensitivity labels, and leakage audit"
    semantic_status: preserved
    evidence: "竞争终止、行政删失、IPCW、时间 t 可用信息、同窗治疗与下一边界生理、两种标签敏感性及全部泄漏审计项目均保留。"
  - protected_id: PCR-027
    prior_locator: "Research design and methods > Mutually exclusive post-onset state and event system > state definitions"
    revised_locator: "Research design and methods > Mutually exclusive post-onset state and event system > state definitions"
    semantic_status: preserved
    evidence: "生理恢复、恶化或新发器官衰竭、持续脓毒症的 SOFA、24 小时、器官支持和事件记录定义均未改变。"
  - protected_id: PCR-028
    prior_locator: "Research design and methods > Observational model target, anchoring, and reporting"
    revised_locator: "Research design and methods > Observational model target, anchoring, and reporting"
    semantic_status: preserved
    evidence: "联合分布中的 X、Y、M、A、B、S 角色及输出的发病风险、状态占用、转移、锚点预测和关系符号/滞后均保留，并继续说明后两者不是结构边方向。"
  - protected_id: PCR-029
    prior_locator: "Research design and methods > Observational model target, anchoring, and reporting > anchoring constraints"
    revised_locator: "Research design and methods > Observational model target, anchoring, and reporting > anchoring constraints"
    semantic_status: preserved
    evidence: "每维至少两个共同指标、第一个载荷 +1、交叉载荷规则、4 维/3 机制上限、1 或 2 个窗口滞后、无同窗循环及 20 个种子对齐均未改变。"
  - protected_id: PCR-030
    prior_locator: "Research design and methods > Observational model target, anchoring, and reporting > missingness and treatment coverage"
    revised_locator: "Research design and methods > Observational model target, anchoring, and reporting > missingness and treatment coverage"
    semantic_status: preserved
    evidence: "缺失随机与选择模型并列基线、五档模式混合偏移、临界点分析及按状态/医院/时间层报告行动概率和有效样本量均保留。"
  - protected_id: PCR-031
    prior_locator: "Research design and methods > Simulation and semi-synthetic recovery study"
    revised_locator: "Research design and methods > Simulation and semi-synthetic recovery study"
    semantic_status: preserved
    evidence: "模拟在不读取最终外部结果下进行，数据生成机制、交叉变化因素及状态、转移、结构、错设和校准评价范围均未改变。"
  - protected_id: PCR-032
    prior_locator: "Research design and methods > Hospital-based cross-database validation > cross-hospital patient handling"
    revised_locator: "Research design and methods > Hospital-based cross-database validation > cross-hospital patient handling"
    semantic_status: preserved
    evidence: "先分医院再识别跨院患者、混合分区患者全部排除、不按患者重分组、单组保留首次入住、表现前报告和连通分量敏感性规则均保留。"
  - protected_id: PCR-033
    prior_locator: "Research design and methods > Hospital-based cross-database validation > external analysis sequence"
    revised_locator: "Research design and methods > Hospital-based cross-database validation > external analysis sequence"
    semantic_status: preserved
    evidence: "冻结对象及不更新模型、仅适配数据再校准、仅适配数据更新观测层的顺序未改变；全模型重拟合仍另列为模型更新研究。"
  - protected_id: PCR-034
    prior_locator: "Research content and work packages > Minimum success definition: all required evidence"
    revised_locator: "Research content and work packages > Minimum success definition: all required evidence"
    semantic_status: preserved
    evidence: "阶段 II 成功仍要求队列、模拟恢复、两项主要预测任务、无高严重度时间/分组问题和预先隔离外部稳定性五类证据同时满足，任一失败仍不成功。"
  - protected_id: PCR-035
    prior_locator: "Research design and methods > Conditional trial observation mapping and secondary analyses > eligibility"
    revised_locator: "Research design and methods > Conditional trial observation mapping and secondary analyses > Trial semantics and common-observation eligibility"
    semantic_status: preserved
    evidence: "阶段 II 冻结与授权/语义前提均保留；新定义的“合格共同指标”逐项重述原有构念、标本、单位、访视、直接实测和禁用变量条件，未扩大资格。"
  - protected_id: PCR-036
    prior_locator: "Research design and methods > Pre-specified deterministic observation mapping"
    revised_locator: "Research design and methods > Pre-specified deterministic observation mapping"
    semantic_status: preserved
    evidence: "MIMIC 冻结标准化、1/99 百分位截断、SVD 公式、并列选轴、SOFA 符号方向、禁止使用治疗组或结局及分试验映射均未改变。"
  - protected_id: PCR-037
    prior_locator: "Research design and methods > External projection fidelity assessment; Operational thresholds > 观测映射外部忠实度"
    revised_locator: "Research design and methods > External projection fidelity assessment; Feasibility, resources, risks, alternatives, and stop conditions > Risks, alternatives, and stop conditions > 观测映射外部忠实度"
    semantic_status: preserved
    evidence: "eICU 先验评价顺序及 50%、0.70、0.50、0.20、0.80–1.20、0.90–0.98、80% 和 60% 的全部忠实度阈值均原样保留。"
  - protected_id: PCR-038
    prior_locator: "Research design and methods > Analysis targets"
    revised_locator: "Research design and methods > Conditional trial observation mapping and secondary analyses > Analysis targets"
    semantic_status: preserved
    evidence: "死亡、P_obs、存活出院排序与概率指数不变；SOFA 临床状态分析明确为不使用阶段 II 映射，缺失敏感性、Holm 家族和交互限定均保留。"
  - protected_id: PCR-039
    prior_locator: "Research design and methods > Secondary representation diagnostics"
    revised_locator: "Research design and methods > Secondary representation diagnostics"
    semantic_status: preserved
    evidence: "遮蔽后重建和未来轨迹两项诊断的 MAE、RMSE、对数评分、覆盖、CRPS、负对数似然、校准及分层报告均未改变。"
  - protected_id: PCR-040
    prior_locator: "Research design and methods > Protocol locks > 不确定性"
    revised_locator: "Research design and methods > Protocol locks for the two primary clinical tasks > 不确定性"
    semantic_status: preserved
    evidence: "患者与医院层级自助法 95% 区间、发病前重叠窗口总权重为 1，以及发病后新发/延迟进入分层和有效转移数均保留。"
  - protected_id: PCR-041
    prior_locator: "Operational thresholds > 模拟运行充分性; 状态与转移恢复; 结构与错设识别"
    revised_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Risks, alternatives, and stop conditions > 模拟运行充分性; 状态与转移恢复; 结构与错设识别"
    semantic_status: preserved
    evidence: "1,000 次或 MCSE 0.02、ARI/典型相关 0.80、种子匹配 90%、转移 MAE 0.05、覆盖 0.90–0.98 及全部结构与错设阈值均未改变。"
  - protected_id: PCR-042
    prior_locator: "Operational thresholds > 概率校准和结构稳定性; 两项主要临床任务; 外部结果"
    revised_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Risks, alternatives, and stop conditions > 概率校准和结构稳定性; 两项主要预测任务; 外部结果"
    semantic_status: preserved
    evidence: "校准 0.80–1.20/0.02、Brier 上限 +0.01、90%/80% 稳定性、外部符号 80%、状态对齐 0.70 和不更新外部失败后果均保留。"
  - protected_id: PCR-043
    prior_locator: "Operational thresholds > 事件、转移和复杂度支持; 外部医院与跨分区患者支持"
    revised_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Risks, alternatives, and stop conditions > 事件、转移和复杂度支持; 外部医院与跨分区患者支持"
    semantic_status: preserved
    evidence: "开发/外部 20/10 事件或转移、每维 2 锚点、30% 实测、70% 医院/80% 患者、20 家医院及跨分区 10% 阈值均未改变。"
  - protected_id: PCR-044
    prior_locator: "Structured abstract > Expected result; Planned outputs; Current feasibility and evidence status"
    revised_locator: "Structured abstract > Expected result; Expected outputs, falsification criteria, and interpretations > Planned outputs; Feasibility, resources, risks, alternatives, and stop conditions > Current feasibility and evidence status"
    semantic_status: preserved
    evidence: "标签、审计、模型、模拟、预测任务、诊断、外部验证和试验分析仍全部标为计划生成或尚未生成，未出现完成性表述。"
  - protected_id: PCR-045
    prior_locator: "Title and positioning claim-support table"
    revised_locator: "Title and positioning claim-support table"
    semantic_status: preserved
    evidence: "候选模型、预设跨数据库验证、条件性随机试验分析和一维摘要组间差异仍分别受原设计和资格条件限定，支持强度未提高。"
  - protected_id: PCR-046
    prior_locator: "Contribution and evidence ladder; Interpretation of the planned evidence"
    revised_locator: "Contribution, innovation, impact, application, and closest-work comparison > Contribution and evidence ladder; Expected outputs, falsification criteria, and interpretations > Interpretation of the planned evidence"
    semantic_status: preserved
    evidence: "各估计对象仍须按估计目标、评价量、效应量和不确定区间报告支持状态，五层结果仍要求完整保留且不得合并为总体成功。"
  - protected_id: PCR-047
    prior_locator: "Research design and methods > Conditional trial observation mapping and secondary analyses; Scientific and interpretive boundaries"
    revised_locator: "Research design and methods > Conditional trial observation mapping and secondary analyses; Feasibility, resources, risks, alternatives, and stop conditions > Limitations and boundary conditions"
    semantic_status: preserved
    evidence: "一维摘要与 SOFA 分析仍为发表后次要或探索性分析；一维摘要仍限实际第 7/8 日，SOFA 仍只支持访视特异临床状态且与阶段 II 模型无关。"
  - protected_id: PCR-048
    prior_locator: "Representative closest-work comparison; Current feasibility and evidence status"
    revised_locator: "Contribution, innovation, impact, application, and closest-work comparison > Representative closest-work comparison; Feasibility, resources, risks, alternatives, and stop conditions > Current feasibility and evidence status"
    semantic_status: preserved
    evidence: "截至 2026-07-17 的检索仍仅对组件先例给出高置信、对完整组合缺口给出低至中等置信，并明确不是全球不存在相关工作的证明。"
  - protected_id: PCR-049
    prior_locator: "Current feasibility and evidence status"
    revised_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Working assumptions and pending specifications; Current feasibility and evidence status"
    semantic_status: preserved
    evidence: "临床尺度映射、多类别校准估计量、Brier 上置信限构造和阈值登记仍未冻结，且仍须在不接触外部结果的时点完成。"
  - protected_id: PCR-050
    prior_locator: "Authoritative limitations... > 尚待冻结的方法规范"
    revised_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Working assumptions and pending specifications"
    semantic_status: preserved
    evidence: "医院规模指标和 Brier 上置信限构造仍只在权威限制节列示一次；冻结时点、可用信息、固定分层/种子/30%–70% 分配及 +0.01 判定均未改变。"
  - protected_id: PCR-051
    prior_locator: "Operational thresholds > 月 0–3 数据与人员; 月 4–6 双数据库审计"
    revised_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Risks, alternatives, and stop conditions > 月 0–3 数据与人员; 月 4–6 双数据库审计"
    semantic_status: preserved
    evidence: "访问和人员失败后的备份/停止路线，以及双库不支持时改 24 小时、事件时间、简化或停止系统端点的完整顺序和后果均保留。"
  - protected_id: PCR-052
    prior_locator: "Operational thresholds > 依赖双数据库审计的阈值登记"
    revised_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Working assumptions and pending specifications; Risks, alternatives, and stop conditions > 依赖双数据库审计的阈值登记"
    semantic_status: preserved
    evidence: "月 6 前按临床容许误差、开发数据和未接触外部结果的先导模拟登记，既有阈值只能收紧且未登记不得拟合的规定均保留。"
  - protected_id: PCR-053
    prior_locator: "Operational thresholds > event/transition complexity, recovery, structure, and stability rows"
    revised_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Risks, alternatives, and stop conditions > 事件、转移和复杂度支持; 状态与转移恢复; 结构与错设识别; 概率校准和结构稳定性"
    semantic_status: preserved
    evidence: "未达支持、恢复或稳定阈值后的降维、合并/删除、简单模型降级、禁止解释、淘汰复杂候选和禁止用预测分数或再校准修复结构失败均保留。"
  - protected_id: PCR-054
    prior_locator: "Operational thresholds > 标签与数据分组"
    revised_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Risks, alternatives, and stop conditions > 标签与数据分组"
    semantic_status: preserved
    evidence: "高严重度泄漏触发项、修正可用时间/删除变量/重建标签及未解决时不得访问外部验证结果的后果均未改变。"
  - protected_id: PCR-055
    prior_locator: "Operational thresholds > 非随机缺失与治疗行动覆盖及重叠"
    revised_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Risks, alternatives, and stop conditions > 非随机缺失与治疗行动覆盖及重叠"
    semantic_status: preserved
    evidence: "五档缺失偏移、行动发生率 5%/95%、有效样本量 20% 触发，以及敏感区间、合并/删除、政策特异和停止解释后果均保留。"
  - protected_id: PCR-056
    prior_locator: "Operational thresholds > 两项主要临床任务; 外部结果"
    revised_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Risks, alternatives, and stop conditions > 两项主要预测任务; 外部结果"
    semantic_status: preserved
    evidence: "任一主要预测任务不达 Brier 与校准标准仍不获支持，次要诊断、试验或复杂模型仍不得替代；不更新外部验证仍为主要依据。"
  - protected_id: PCR-057
    prior_locator: "Operational thresholds > 外部医院与跨分区患者支持"
    revised_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Risks, alternatives, and stop conditions > 外部医院与跨分区患者支持"
    semantic_status: preserved
    evidence: "医院、事件/转移、锚点覆盖或跨分区排除不足时的独立保管人核验、备份库和进一步降级后不得称医院稳健或完整系统端点均保留。"
  - protected_id: PCR-058
    prior_locator: "Operational thresholds > 开发冻结与时间"
    revised_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Risks, alternatives, and stop conditions > 开发冻结与时间"
    semantic_status: preserved
    evidence: "月 12 封存简单模型、月 20 不访问外部结果、月 24 记录阶段 II 预定目标未完成及无论成功或降级均封存阶段 II 的后果均保留；仅改写交付用语。"
  - protected_id: PCR-059
    prior_locator: "Operational thresholds > 试验语义与分析集; 共同观测变量; 观测映射外部忠实度"
    revised_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Risks, alternatives, and stop conditions > 试验语义与分析集; 每项试验的合格共同指标; 观测映射外部忠实度"
    semantic_status: preserved
    evidence: "授权/语义失败、少于两个合格锚点、指标不一致或映射失败时停止一维摘要，且仅在 SOFA 等语义可核验时采用 SOFA 分析的全部分支条件均保留。"
  - protected_id: PCR-060
    prior_locator: "Operational thresholds > 随机试验结果与多重性"
    revised_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Risks, alternatives, and stop conditions > 随机试验结果与多重性"
    semantic_status: preserved
    evidence: "方向不一致、宽区间、Holm 后无支持或缺失敏感时如实报告不确定性，不得挑选亚组，两试验不得合并且亚组仅报告交互的规定均保留。"
  - protected_id: PCR-061
    prior_locator: "Data, materials, and existing evidence base > time interval; Research design and methods > sparse trial visits"
    revised_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Limitations and boundary conditions > item 8"
    semantic_status: preserved
    evidence: "12 小时主间隔、动态测量不无条件前值延续、保存实测及间隔信息，以及试验稀疏访视只作访视特异或离散变化且不插值连续轨迹均保留在权威限制位置。"
  - protected_id: PCR-062
    prior_locator: "Scientific and interpretive boundaries > XBJ-SCAP"
    revised_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Limitations and boundary conditions > item 6"
    semantic_status: preserved
    evidence: "XBJ-SCAP 入组仍不等同确认 Sepsis-3，患者级变量缺失和 D-dimer 单位待核验仍明确，相关字段仍禁止推测或构造。"
  - protected_id: PCR-063
    prior_locator: "Scientific and interpretive boundaries > item 1"
    revised_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Limitations and boundary conditions > item 1"
    semantic_status: preserved
    evidence: "观察性状态、治疗、测量和预测仍不识别治疗因果效应、真实反馈或反事实策略，阴性对照和时间反转仍不能证明模型正确。"
  - protected_id: PCR-064
    prior_locator: "Scientific and interpretive boundaries > items 3-4"
    revised_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Limitations and boundary conditions > items 3-4"
    semantic_status: preserved
    evidence: "试验分支仍不支持未测动力学、状态转移边、中介、控制或完整系统验证；SOFA 分析仍明确与阶段 II 模型无关。"
  - protected_id: PCR-065
    prior_locator: "Scientific and interpretive boundaries > item 5; Operational thresholds > 最接近工作与应用定位"
    revised_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Limitations and boundary conditions > item 5; Risks, alternatives, and stop conditions > 最接近工作与应用定位"
    semantic_status: preserved
    evidence: "新算法、全球首次、全球不存在、专利空白、数字孪生和控制主张仍不受支持；提出相关主张前仍须扩展系统、引文、专利和非英语检索。"
  - protected_id: PCR-066
    prior_locator: "Scientific and interpretive boundaries > items 4-5; Operational thresholds > 最接近工作与应用定位"
    revised_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Limitations and boundary conditions > items 4-5; Risks, alternatives, and stop conditions > 最接近工作与应用定位"
    semantic_status: preserved
    evidence: "已验证临床工具、药物平台和无条件国际推广仍不受支持；临床应用前的前瞻性安全、效用、治理及监管边界均保留。"
  - protected_id: PCR-067
    prior_locator: "Scientific and interpretive boundaries > item 2; Hospital-based cross-database validation"
    revised_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Limitations and boundary conditions > item 2; Research design and methods > Hospital-based cross-database validation"
    semantic_status: preserved
    evidence: "再校准、观测层更新或全模型重拟合仍不能替代不更新模型的外部验证；全模型重拟合仍属于新的开发研究。"
  - protected_id: PCR-068
    prior_locator: "Scientific and interpretive boundaries > item 7"
    revised_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Limitations and boundary conditions > item 7"
    semantic_status: preserved
    evidence: "阶段 III 仍在阶段 I–II 的 24 个月目标之后，且仍不能补足资源、模拟恢复、主要预测任务或外部验证失败。"
  - protected_id: PCR-069
    prior_locator: "Scientific and interpretive boundaries > item 6; Operational thresholds > 试验语义与分析集"
    revised_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Limitations and boundary conditions > item 6; Risks, alternatives, and stop conditions > 试验语义与分析集"
    semantic_status: preserved
    evidence: "未核验字段、单位、访视和连续轨迹仍禁止推测或构造，XBJ-SCAP 仍不得无条件写为确认 Sepsis-3。"
  - protected_id: PCR-070
    prior_locator: "Conditional trial observation mapping and secondary analyses; Operational thresholds > 随机试验结果与多重性"
    revised_locator: "Research design and methods > Conditional trial observation mapping and secondary analyses; Feasibility, resources, risks, alternatives, and stop conditions > Risks, alternatives, and stop conditions > 随机试验结果与多重性"
    semantic_status: preserved
    evidence: "两试验继续分开报告且不得合并为共同效应或机制；亚组仍只报告治疗—亚组交互并不得改变主要结论。"
  - protected_id: PCR-071
    prior_locator: "Structured abstract > Expected result; Current feasibility and evidence status"
    revised_locator: "Structured abstract > Expected result; Feasibility, resources, risks, alternatives, and stop conditions > Current feasibility and evidence status"
    semantic_status: preserved
    evidence: "候选模型、模拟、主要预测任务、外部验证和试验分析仍明确为计划或尚未生成，未新增完成、有效、恢复、稳定或治疗差异的结果主张。"
  - protected_id: PCR-072
    prior_locator: "Scientific and interpretive boundaries > item 5; Representative closest-work comparison"
    revised_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Limitations and boundary conditions > item 5; Contribution, innovation, impact, application, and closest-work comparison > Representative closest-work comparison"
    semantic_status: preserved
    evidence: "有界检索仍不支持系统综述完整性或全面新颖性；未实施的方法、未覆盖的数据库和预印本/术语遗漏风险均继续明确列出。"
undeclared_scientific_changes: []
findings: []
unresolved_issues: []
---

# Content-preservation check

## Decision rationale

v013 对 v012 的变更均属于获准的编辑操作：定义并统一“合格共同指标”“主要预测任务”“受预设约束的复杂候选模型”和“SOFA 临床状态分析”，拆分结构摘要中的高负担长段，改写 24 个月范围用语和风险表句式，并替换证据链字段标签。逐项比较冻结 register 的 72 个条目后，未发现研究身份、对象、范围、人群、推断单位、数据角色、估计目标、阈值、验证顺序、证据状态、限制、替代方案或停止后果发生改变，也未发现新增方法、数据、结果或强化主张。

## Protected-content trace

所有 72 个受保护条目均可在 v013 中追踪。主要非平凡改动有三类：试验共同实测生理指标被定义为每项试验各自的“合格共同指标”，其构念、标本、单位、访视、直接实测和禁用变量资格与 v012 一致；“主要临床任务”统一为“主要预测任务”，两个估计目标和全部评分、校准及失败阈值不变；独立 SOFA 分析统一为“SOFA 临床状态分析”，并更明确地说明其不依赖阶段 II 观测映射。权威限制与风险位置仍集中在第 14 节，全部数值阈值、条件性和禁止替代规则均保留。

## Required routing

该 dossier 的科学内容已保留，可进入新的叙事与学术语言评估。
