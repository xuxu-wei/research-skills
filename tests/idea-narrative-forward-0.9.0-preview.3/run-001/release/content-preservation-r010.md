---
schema_version: research-idea-content-preservation-check.v1
check_id: content-preservation-I01-001-r010
review_id: content-preservation-review-I01-001-r010
reviewer_skill: idea-narrative-assessor
reviewer_instance_id: fresh-scientific-content-preservation-reviewer-r010-20260718
workflow_id: RID-SEPSIS-CSM-20260717-001
round_id: r010
input_artifact_ids: [idea-dossier-I01-001-v011, idea-dossier-I01-001-v012, protected-content-register-I01-001-v011, revision-delta-I01-001-v011-to-v012]
input_versions: [v011, v012, v011, v011-to-v012]
inputs:
  prior_dossier:
    artifact_id: idea-dossier-I01-001-v011
    version: v011
    path: tests/idea-narrative-forward-0.9.0-preview.3/run-001/release/idea-dossier-v011.md
  revised_dossier:
    artifact_id: idea-dossier-I01-001-v012
    version: v012
    path: tests/idea-narrative-forward-0.9.0-preview.3/run-001/release/idea-dossier-v012.md
  protected_content_register:
    artifact_id: protected-content-register-I01-001-v011
    version: v011
    path: tests/idea-narrative-forward-0.9.0-preview.3/run-001/release/protected-content-register-v011.yaml
  revision_delta:
    artifact_id: revision-delta-I01-001-v011-to-v012
    version: v011-to-v012
    path: tests/idea-narrative-forward-0.9.0-preview.3/run-001/release/revision-delta-v011-to-v012.md
files_read:
  - tests/idea-narrative-forward-0.9.0-preview.3/run-001/release/idea-dossier-v011.md
  - tests/idea-narrative-forward-0.9.0-preview.3/run-001/release/idea-dossier-v012.md
  - tests/idea-narrative-forward-0.9.0-preview.3/run-001/release/protected-content-register-v011.yaml
  - tests/idea-narrative-forward-0.9.0-preview.3/run-001/release/revision-delta-v011-to-v012.md
isolation_mode: fresh_subagent
prior_scores_visible: false
source_edits_performed: false
decision: scientific_content_preserved
protected_item_checks:
  - protected_id: PCR-001
    prior_locator: "frontmatter identity_anchor; Primary research question"
    revised_locator: "frontmatter identity_anchor; Primary research question"
    semantic_status: preserved
    evidence: "三项依赖问题及发病前—首次发病—发病后—结局连续体、跨数据库状态/结构检验和仅在阶段 II 成功后开展的试验比较均原意保留。"
  - protected_id: PCR-002
    prior_locator: "frontmatter identity_anchor; Structured abstract > Objective and hypothesis; 三阶段导航"
    revised_locator: "frontmatter identity_anchor; Structured abstract > Objective and hypothesis; 三阶段导航"
    semantic_status: preserved
    evidence: "24 个月内完成阶段 I–II、阶段 II 的四类工作及 24 月后条件性阶段 III 均保持；仅将长句拆分。"
  - protected_id: PCR-003
    prior_locator: "Core hypothesis"
    revised_locator: "Core hypothesis"
    semantic_status: preserved
    evidence: "共同指标/事件支持、预先固定尺度/状态数/滞后/锚定、至多一个受限复杂模型及恢复与外部稳定性条件逐项相同，未增强主张。"
  - protected_id: PCR-004
    prior_locator: "Title, summary, audience, and positioning; Contribution and evidence ladder"
    revised_locator: "Title, summary, audience, and positioning; Contribution and evidence ladder"
    semantic_status: preserved
    evidence: "定位仍限于有界证据整合、预设跨数据库验证、研究基准与资源建设；没有把组件先例改写为方法创新。"
  - protected_id: PCR-005
    prior_locator: "Research identity and final boundary"
    revised_locator: "Research identity and final boundary"
    semantic_status: preserved
    evidence: "研究身份五个锚点及取消连续体、替换证据基础或推断单位即须另立研究的边界逐字保持。"
  - protected_id: PCR-006
    prior_locator: "frontmatter identity_anchor > study_object and primary_unit_of_inference"
    revised_locator: "frontmatter identity_anchor > study_object and primary_unit_of_inference"
    semantic_status: preserved
    evidence: "研究对象、未发病风险区间、发病后轨迹、患者—时间状态与转移推断单位及患者/医院聚类均未改变。"
  - protected_id: PCR-007
    prior_locator: "三阶段导航; Research content and work packages"
    revised_locator: "三阶段导航; Research content and work packages"
    semantic_status: preserved
    evidence: "阶段 I、II、III 的月份、任务、最低交付边界和阶段 III 不改变阶段 II 成败的限制均保持。"
  - protected_id: PCR-008
    prior_locator: "Protocol locks for the two primary clinical tasks > 人群"
    revised_locator: "Protocol locks for the two primary clinical tasks > 人群"
    semantic_status: preserved
    evidence: "成人、首个合格 ICU 入住、至少 12 小时历史、未发病风险集及新发/延迟进入与左截断规则均逐项保留。"
  - protected_id: PCR-009
    prior_locator: "Mutually exclusive post-onset state and event system"
    revised_locator: "Mutually exclusive post-onset state and event system"
    semantic_status: preserved
    evidence: "六状态固定优先级、无法排序处理、事件时间敏感性，以及出院不等于恢复、转院不作普通删失均相同。"
  - protected_id: PCR-010
    prior_locator: "Resources and governance"
    revised_locator: "Feasibility and resources"
    semantic_status: preserved
    evidence: "两个主要数据库、最多 4 维/3 切换/1 复杂候选、两主要任务/两次要诊断及排除事项完整迁移，范围未扩张。"
  - protected_id: PCR-011
    prior_locator: "Hospital-based cross-database validation"
    revised_locator: "Hospital-based cross-database validation; Working assumptions and pending specifications"
    semantic_status: preserved
    evidence: "待冻结医院规模指标、接口完整性、eICU 医院标识符、种子 20260717、30%/70% 医院分配和两类验证分报均保留；分散条件被合并明示。"
  - protected_id: PCR-012
    prior_locator: "Conditional trial observation mapping and secondary analyses > Analysis targets"
    revised_locator: "Conditional trial observation mapping and secondary analyses > Analysis targets"
    semantic_status: preserved
    evidence: "两试验分开不合并；EXIT-SEP 1,817/1,760 与第 7 日、XBJ-SCAP 710/675 降级及第 8 日和敏感性人群均未改变。"
  - protected_id: PCR-013
    prior_locator: "Title, summary, audience, and positioning; Interpretation of the planned evidence"
    revised_locator: "Title, summary, audience, and positioning; Interpretation of the planned evidence"
    semantic_status: preserved
    evidence: "任务表现、模拟恢复、跨数据库稳定性与试验组间差异继续分别报告且不得互相替代或合并。"
  - protected_id: PCR-014
    prior_locator: "Public ICU databases and planned roles"
    revised_locator: "Public ICU databases and planned roles"
    semantic_status: preserved
    evidence: "MIMIC-IV v3.1、eICU-CRD v2.0 及 HiRID/AmsterdamUMCdb 的开发、外部和备份角色与启用条件未变。"
  - protected_id: PCR-015
    prior_locator: "Public ICU databases and planned roles > 共同概念层和双数据库审计"
    revised_locator: "Public ICU databases and planned roles > 共同概念层和双数据库审计"
    semantic_status: preserved
    evidence: "共同变量四项核验条件、数据库特异变量限制，以及拟合前样本/事件/转移/医院/跨院患者/接口/治疗覆盖审计均保持。"
  - protected_id: PCR-016
    prior_locator: "Current feasibility and evidence status"
    revised_locator: "Current feasibility and evidence status"
    semantic_status: preserved
    evidence: "数据库存在已核验与访问、协议、提取和项目审计未核验/尚未生成的层级未变，仍禁止以官方规模替代项目计数。"
  - protected_id: PCR-017
    prior_locator: "Trial data considered for conditional stage III analyses"
    revised_locator: "Trial data considered for conditional stage III analyses"
    semantic_status: preserved
    evidence: "EXIT-SEP 与 XBJ-SCAP 的随机数、分析集、死亡/状态及 SOFA、乳酸、白细胞、C 反应蛋白非缺失计数全部逐数一致。"
  - protected_id: PCR-018
    prior_locator: "frontmatter identity_anchor > core_data_or_evidence_base; Evidence chains"
    revised_locator: "frontmatter identity_anchor > core_data_or_evidence_base; Evidence chains"
    semantic_status: preserved
    evidence: "文献/专家先验、纵向公共 ICU 数据及有条件可用的两个随机试验个体数据仍构成同一核心证据基础。"
  - protected_id: PCR-019
    prior_locator: "Variable-role separation"
    revised_locator: "Variable-role separation"
    semantic_status: preserved
    evidence: "Y、A、M、标签专用变量和 B 的角色、禁止混用及双重用途字段独立副本/可用时间规则均逐格相同。"
  - protected_id: PCR-020
    prior_locator: "Resources and governance; Current feasibility and evidence status"
    revised_locator: "Feasibility and resources; Current feasibility and evidence status"
    semantic_status: preserved
    evidence: "六类最低人员角色保持，且具名人员和工时仍为未核验，角色定义不等于人员承诺。"
  - protected_id: PCR-021
    prior_locator: "Trial semantics and common-observation eligibility"
    revised_locator: "Trial semantics and common-observation eligibility"
    semantic_status: preserved
    evidence: "个体授权、原始 CRF/SAP、字典/持有人确认及分组、分析集、中心、访视、生存住院语义核验条件完整保留。"
  - protected_id: PCR-022
    prior_locator: "Current feasibility and evidence status"
    revised_locator: "Current feasibility and evidence status; Limitations and boundary conditions > item 6"
    semantic_status: preserved
    evidence: "本地材料仍仅是衍生报告；共同指标/单位/访视映射未核验，WBC/CRP 仅为候选，未核验单位或不存在变量不得纳入。"
  - protected_id: PCR-023
    prior_locator: "Protocol locks > 主要发病前任务"
    revised_locator: "Protocol locks > 主要发病前任务"
    semantic_status: preserved
    evidence: "12 小时动态时点、12–24 小时历史、未来 12 小时首次发病 CIF、原因别模型及主要/次要评价指标均相同。"
  - protected_id: PCR-024
    prior_locator: "Protocol locks > 主要发病后任务"
    revised_locator: "Protocol locks > 主要发病后任务"
    semantic_status: preserved
    evidence: "第 7 日有利状态概率、两状态分报、互斥多状态/Aalen–Johansen、第 14 日敏感性及校准指标未变。"
  - protected_id: PCR-025
    prior_locator: "Protocol locks > 事件时间和信息可用时间"
    revised_locator: "Protocol locks > 事件时间和信息可用时间"
    semantic_status: preserved
    evidence: "72/24 小时感染配对、SOFA 基线与 24 小时窗、感染前 48 至后 24 小时、首次满足和后到信息不回填均逐项一致。"
  - protected_id: PCR-026
    prior_locator: "Protocol locks > 竞争事件、顺序、敏感性标签和泄漏审计"
    revised_locator: "Protocol locks > 竞争事件、顺序、敏感性标签和泄漏审计"
    semantic_status: preserved
    evidence: "竞争终止/删失、IPCW/界限、同窗时间顺序、两种标签敏感性定义与全部泄漏检查内容均保持。"
  - protected_id: PCR-027
    prior_locator: "Mutually exclusive post-onset state and event system > state definitions"
    revised_locator: "Mutually exclusive post-onset state and event system > state definitions"
    semantic_status: preserved
    evidence: "恢复、恶化/新发器官衰竭和持续脓毒症的 SOFA、24 小时、器官支持及重复记录规则逐字保持。"
  - protected_id: PCR-028
    prior_locator: "Observational model target, anchoring, and reporting"
    revised_locator: "Observational model target, anchoring, and reporting"
    semantic_status: preserved
    evidence: "联合分布、X/Y/A/M/B/S 含义和发病风险、占用/转移、锚点预测、关系符号/滞后输出均相同，未改为边方向。"
  - protected_id: PCR-029
    prior_locator: "Observational model target, anchoring, and reporting > anchoring constraints"
    revised_locator: "Observational model target, anchoring, and reporting > anchoring constraints"
    semantic_status: preserved
    evidence: "每维至少 2 锚点、首载荷 +1、交叉载荷、4 维/3 机制、1–2 窗、无瞬时循环与 20 种子对齐均不变。"
  - protected_id: PCR-030
    prior_locator: "Observational model target, anchoring, and reporting > missingness and treatment coverage"
    revised_locator: "Observational model target, anchoring, and reporting > missingness and treatment coverage"
    semantic_status: preserved
    evidence: "缺失随机和选择模型两并列基线、五个偏移值、临界点及状态/医院/时间层行动概率和有效样本量均保持。"
  - protected_id: PCR-031
    prior_locator: "Simulation and semi-synthetic recovery study"
    revised_locator: "Simulation and semi-synthetic recovery study"
    semantic_status: preserved
    evidence: "外部结果隔离、全部数据生成机制/交叉因素和恢复、误差、覆盖、结构、错设、校准评价未变；仅统一 Monte Carlo 中文名称。"
  - protected_id: PCR-032
    prior_locator: "Hospital-based cross-database validation > cross-hospital patient handling"
    revised_locator: "Hospital-based cross-database validation > cross-hospital patient handling"
    semantic_status: preserved
    evidence: "先定医院、跨分区患者全排除、单分组首个记录、结局前报告和验证优先连通分量敏感性四步顺序相同。"
  - protected_id: PCR-033
    prior_locator: "Hospital-based cross-database validation > external analysis sequence"
    revised_locator: "Hospital-based cross-database validation > external analysis sequence"
    semantic_status: preserved
    evidence: "冻结内容及不更新、适配集再校准、适配集观测层更新的三层顺序和全模型重拟合定性均逐字保留。"
  - protected_id: PCR-034
    prior_locator: "Minimum success definition: all required evidence"
    revised_locator: "Minimum success definition: all required evidence"
    semantic_status: preserved
    evidence: "两库队列、模拟恢复/错设识别、两项任务、无高严重度问题及外部任务/对齐/结构五类证据仍须全部满足。"
  - protected_id: PCR-035
    prior_locator: "Conditional trial observation mapping and secondary analyses > eligibility"
    revised_locator: "Conditional trial observation mapping and secondary analyses > eligibility"
    semantic_status: preserved
    evidence: "阶段 II 完成冻结、试验授权语义、共同锚点资格、禁用变量及不得试验特异重估权重的条件均保持。"
  - protected_id: PCR-036
    prior_locator: "Pre-specified deterministic observation mapping"
    revised_locator: "Pre-specified deterministic observation mapping"
    semantic_status: preserved
    evidence: "MIMIC 冻结标准化/截断、SVD 两投影公式、并列选轴、SOFA 定向及不使用试验分组/结局、两试验独立映射均一致。"
  - protected_id: PCR-037
    prior_locator: "External projection fidelity assessment; Operational thresholds > 观测映射外部忠实度"
    revised_locator: "External projection fidelity assessment; Risks, alternatives, and stop conditions > 观测映射外部忠实度"
    semantic_status: preserved
    evidence: "eICU 先验评价与禁用试验调参保持；50%、0.70、0.50、0.20、0.80–1.20、0.90–0.98、80%、60% 九项失败阈值逐项相同。"
  - protected_id: PCR-038
    prior_locator: "Conditional trial observation mapping and secondary analyses > Analysis targets"
    revised_locator: "Conditional trial observation mapping and secondary analyses > Analysis targets"
    semantic_status: preserved
    evidence: "死亡/住院 P_obs/出院排序、概率指数、独立 SOFA、插补与敏感性、Holm 0.05 家族和亚组交互限制均保留；仅澄清主要结局状态标签。"
  - protected_id: PCR-039
    prior_locator: "Secondary representation diagnostics"
    revised_locator: "Secondary representation diagnostics"
    semantic_status: preserved
    evidence: "遮蔽重建和未来轨迹两诊断、各自评分及变量/状态/医院/观测密度分层与主要任务分报均相同。"
  - protected_id: PCR-040
    prior_locator: "Protocol locks > 不确定性"
    revised_locator: "Protocol locks > 不确定性"
    semantic_status: preserved
    evidence: "患者与医院层级自助法 95% 区间、发病前总权重 1、发病后分层和有效转移数均逐格相同。"
  - protected_id: PCR-041
    prior_locator: "Operational thresholds > 模拟运行充分性、状态与转移恢复、结构与错设识别"
    revised_locator: "Risks, alternatives, and stop conditions > 模拟运行充分性、状态与转移恢复、结构与错设识别"
    semantic_status: preserved
    evidence: "1,000/0.02、0.80、90%、0.05、0.90–0.98、0.80/0.10、0.05 和 80%/0.05 的全部准入阈值原值保留。"
  - protected_id: PCR-042
    prior_locator: "Operational thresholds > 概率校准和结构稳定性、两项主要临床任务、外部结果"
    revised_locator: "Risks, alternatives, and stop conditions > 概率校准和结构稳定性、两项主要临床任务、外部结果"
    semantic_status: preserved
    evidence: "校准、绝对误差、Brier +0.01、种子匹配、自助保留、符号一致、状态对齐和外部失败后果全部未改。"
  - protected_id: PCR-043
    prior_locator: "Operational thresholds > 事件、转移和复杂度支持; 外部医院与跨分区患者支持"
    revised_locator: "Risks, alternatives, and stop conditions > 事件、转移和复杂度支持; 外部医院与跨分区患者支持"
    semantic_status: preserved
    evidence: "20/10 事件与转移、2 锚点、30% 实测、70% 医院/80% 患者、20 医院和 10% 跨分区排除阈值均保持。"
  - protected_id: PCR-044
    prior_locator: "Structured abstract > Expected result; Planned outputs; Current feasibility and evidence status"
    revised_locator: "Structured abstract > Expected result; Planned outputs; Current feasibility and evidence status"
    semantic_status: preserved
    evidence: "所有标签、审计、模型、模拟、任务、诊断、外部及试验分析仍明确为计划/拟生成/尚未生成，未出现完成性主张。"
  - protected_id: PCR-045
    prior_locator: "Title and positioning claim-support table"
    revised_locator: "Title and positioning claim-support table"
    semantic_status: preserved
    evidence: "一个拟构建对象和资源定位仍为有界获得支持，跨数据库、条件性试验和一维摘要三项仍为限定支持；仅移除英文内部标签。"
  - protected_id: PCR-046
    prior_locator: "Contribution and evidence ladder; Interpretation of the planned evidence; Required analyses and evidence"
    revised_locator: "Contribution and evidence ladder; Interpretation of the planned evidence; Required analyses and evidence"
    semantic_status: preserved
    evidence: "逐估计对象按目标、评价量、效应量和区间报告三种支持状态、保留全部模型层及五层证据分报的要求未变。"
  - protected_id: PCR-047
    prior_locator: "Conditional trial observation mapping and secondary analyses; Scientific and interpretive boundaries"
    revised_locator: "Conditional trial observation mapping and secondary analyses; Limitations and boundary conditions"
    semantic_status: preserved
    evidence: "两类试验分析仍是发表后次要/探索性；一维摘要仅支持对应访视差异，独立 SOFA 仅支持临床状态且与阶段 II 无关。"
  - protected_id: PCR-048
    prior_locator: "Representative closest-work comparison; Current feasibility and evidence status"
    revised_locator: "Representative closest-work comparison; Current feasibility and evidence status"
    semantic_status: preserved
    evidence: "模块先例高置信、完整组合缺口低至中等置信及有界检索不能证明全球不存在相关工作的强度保持。"
  - protected_id: PCR-049
    prior_locator: "Current feasibility and evidence status; 尚待冻结的方法规范"
    revised_locator: "Working assumptions and pending specifications; Current feasibility and evidence status"
    semantic_status: preserved
    evidence: "原分散列出的临床尺度映射、多类别校准估计量、Brier 上置信限和阈值登记均仍为尚未冻结；医院指标一并集中列示，未改为已确定。"
  - protected_id: PCR-050
    prior_locator: "尚待冻结的方法规范"
    revised_locator: "Working assumptions and pending specifications > 医院规模四分位分层指标; 主要临床任务 Brier 差值的 95% 上置信限构造"
    semantic_status: preserved
    evidence: "医院指标的审计后/结果隔离下冻结及种子和 30%/70% 固定项、上置信限月 6 前冻结与 +0.01/方向/校准/禁止替代均在唯一完整清单保持。"
  - protected_id: PCR-051
    prior_locator: "Operational thresholds > 月 0–3 数据与人员; 月 4–6 双数据库审计"
    revised_locator: "Risks, alternatives, and stop conditions > 月 0–3 数据与人员; 月 4–6 双数据库审计"
    semantic_status: preserved
    evidence: "访问/人员/双库失败的备份与停止，以及 12→24 小时→事件时间、减维/备份和无两库支持停止的顺序与后果均相同。"
  - protected_id: PCR-052
    prior_locator: "Operational thresholds > 依赖双数据库审计的阈值登记"
    revised_locator: "Working assumptions and pending specifications > 依赖双数据库审计的阈值登记表; Risks, alternatives, and stop conditions"
    semantic_status: preserved
    evidence: "月 6 前按临床容许误差、开发库自助法和隔离先导模拟登记，以及既有阈值只可收紧、拟合前补齐的约束均保持。"
  - protected_id: PCR-053
    prior_locator: "Operational thresholds > event/transition complexity, recovery, structure, and stability rows"
    revised_locator: "Risks, alternatives, and stop conditions > event/transition complexity, recovery, structure, and stability rows"
    semantic_status: preserved
    evidence: "未达数据/恢复/结构/稳定阈值时的简化、降级、不解释、淘汰复杂候选、禁用预测替代和再校准边界均逐项保留。"
  - protected_id: PCR-054
    prior_locator: "Operational thresholds > 标签与数据分组"
    revised_locator: "Risks, alternatives, and stop conditions > 标签与数据分组"
    semantic_status: preserved
    evidence: "高严重度泄漏的来源、修正信息时间/删变量/重建标签和未解决前不得访问外部结果均相同。"
  - protected_id: PCR-055
    prior_locator: "Operational thresholds > 非随机缺失与治疗行动覆盖及重叠"
    revised_locator: "Risks, alternatives, and stop conditions > 非随机缺失与治疗行动覆盖及重叠"
    semantic_status: preserved
    evidence: "缺失敏感区间、行动 5%/95%、有效样本量 20% 及合并/删除、政策特异和停止解释后果未变。"
  - protected_id: PCR-056
    prior_locator: "Operational thresholds > 两项主要临床任务; 外部结果; Scientific and interpretive boundaries > item 2"
    revised_locator: "Risks, alternatives, and stop conditions > 两项主要临床任务; 外部结果; Limitations and boundary conditions > item 2"
    semantic_status: preserved
    evidence: "主要任务失败不可被次要诊断/试验/复杂模型替代，不更新验证优先且有限更新仅说明更新后适用性的边界保持。"
  - protected_id: PCR-057
    prior_locator: "Operational thresholds > 外部医院与跨分区患者支持"
    revised_locator: "Risks, alternatives, and stop conditions > 外部医院与跨分区患者支持"
    semantic_status: preserved
    evidence: "独立数据保管人不释放表现的支持核验、启用备份，以及仍不足时降级并禁称医院稳健/完整系统端点均相同。"
  - protected_id: PCR-058
    prior_locator: "Operational thresholds > 开发冻结与时间"
    revised_locator: "Risks, alternatives, and stop conditions > 开发冻结与时间"
    semantic_status: preserved
    evidence: "月 12 封存简单层、月 20 不访问外部、月 24 记最低端点未完成并无论成败封存阶段 II 的后果逐项保留。"
  - protected_id: PCR-059
    prior_locator: "Operational thresholds > 试验语义与分析集; 共同观测变量; 观测映射外部忠实度"
    revised_locator: "Risks, alternatives, and stop conditions > 试验语义与分析集; 共同观测变量; 观测映射外部忠实度"
    semantic_status: preserved
    evidence: "授权/语义、锚点资格或忠实度失败时的分支停止、禁推字段/轨迹、禁用组间结果恢复及有条件 SOFA 备选均保持。"
  - protected_id: PCR-060
    prior_locator: "Operational thresholds > 随机试验结果与多重性"
    revised_locator: "Risks, alternatives, and stop conditions > 随机试验结果与多重性"
    semantic_status: preserved
    evidence: "方向不一、区间宽、Holm 无支持或缺失敏感时如实报告，且不得选亚组改结论、不得合并试验、只报告交互均相同。"
  - protected_id: PCR-061
    prior_locator: "Public ICU databases and planned roles > time interval; Analysis targets > sparse trial visits"
    revised_locator: "Limitations and boundary conditions > item 8"
    semantic_status: preserved
    evidence: "12 小时主方案、动态测量不无条件前值延续及实测时间记录，与两组稀疏访视仅作访视特异/离散分析且不插值，合并至唯一权威位置。"
  - protected_id: PCR-062
    prior_locator: "Scientific and interpretive boundaries > item 6"
    revised_locator: "Limitations and boundary conditions > item 6"
    semantic_status: preserved
    evidence: "XBJ-SCAP 肺炎入组不等于确认 Sepsis-3、缺患者字段、D-二聚体单位待核验和不得推测/构造均保持；仅规范中英文术语。"
  - protected_id: PCR-063
    prior_locator: "Scientific and interpretive boundaries > item 1"
    revised_locator: "Limitations and boundary conditions > item 1"
    semantic_status: preserved
    evidence: "观察性关联/预测不识别治疗因果、真实反馈网络或反事实策略，阴性对照/时间反转也不证明正确的边界逐字保持。"
  - protected_id: PCR-064
    prior_locator: "Scientific and interpretive boundaries > items 3–4"
    revised_locator: "Limitations and boundary conditions > items 3–4"
    semantic_status: preserved
    evidence: "试验不验证潜在动力学、转移边、中介、个体控制或完整系统，且独立 SOFA 与阶段 II 无关的限制均保持。"
  - protected_id: PCR-065
    prior_locator: "Scientific and interpretive boundaries > item 5; Operational thresholds > 最接近工作与应用定位"
    revised_locator: "Limitations and boundary conditions > item 5; Risks, alternatives, and stop conditions > 最接近工作与应用定位"
    semantic_status: preserved
    evidence: "不支持新算法、首次、全球不存在、专利空白、数字孪生或控制主张，及须另行系统综述/引文/专利/非英语检索的边界保持。"
  - protected_id: PCR-066
    prior_locator: "Scientific and interpretive boundaries > items 4–5; Operational thresholds > 最接近工作与应用定位"
    revised_locator: "Limitations and boundary conditions > items 4–5; Risks, alternatives, and stop conditions > 最接近工作与应用定位"
    semantic_status: preserved
    evidence: "不支持已验证临床工具、药物平台或无条件国际推广，应用需前瞻安全/效用/治理及 XueBiJing 监管谨慎边界均保持。"
  - protected_id: PCR-067
    prior_locator: "Scientific and interpretive boundaries > item 2; Hospital-based cross-database validation"
    revised_locator: "Limitations and boundary conditions > item 2; Hospital-based cross-database validation"
    semantic_status: preserved
    evidence: "再校准/观测层更新不能冒充不更新验证成功，全模型重拟合为新开发研究的禁止主张未变。"
  - protected_id: PCR-068
    prior_locator: "Scientific and interpretive boundaries > item 7; 三阶段导航"
    revised_locator: "Limitations and boundary conditions > item 7; 三阶段导航"
    semantic_status: preserved
    evidence: "阶段 III 不能补足阶段 II 的资源、模拟、主要任务或外部失败，且不改变阶段 II 成败的边界保持。"
  - protected_id: PCR-069
    prior_locator: "Scientific and interpretive boundaries > item 6; Operational thresholds > 试验语义与分析集"
    revised_locator: "Limitations and boundary conditions > items 6 and 8; Risks, alternatives, and stop conditions > 试验语义与分析集"
    semantic_status: preserved
    evidence: "未核验/不存在字段、单位与访视语义不得推测或构造轨迹，XBJ-SCAP 不得写成确认 Sepsis-3 的边界完整保留。"
  - protected_id: PCR-070
    prior_locator: "Conditional trial observation mapping and secondary analyses; Operational thresholds > 随机试验结果与多重性"
    revised_locator: "Conditional trial observation mapping and secondary analyses; Risks, alternatives, and stop conditions > 随机试验结果与多重性"
    semantic_status: preserved
    evidence: "两试验不得合并为共同效应/机制，选择亚组不得改变主要结论，亚组仅报告治疗—亚组交互均未变。"
  - protected_id: PCR-071
    prior_locator: "Structured abstract > Expected result; Planned outputs; Current feasibility and evidence status"
    revised_locator: "Structured abstract > Expected result; Planned outputs; Current feasibility and evidence status"
    semantic_status: preserved
    evidence: "候选模型、模拟、临床任务、外部验证与试验分析仍为尚未生成/计划产物，没有新增完成、有效、恢复成功、外部稳定或治疗差异主张。"
  - protected_id: PCR-072
    prior_locator: "Scientific and interpretive boundaries > item 5; Representative closest-work comparison"
    revised_locator: "Limitations and boundary conditions > item 5; Representative closest-work comparison"
    semantic_status: preserved
    evidence: "有界检索不是系统综述、缺 PRISMA 双筛/引文穷举/专利检索及未覆盖数据库和预印本/术语遗漏风险均逐项保留。"
undeclared_scientific_changes: []
findings: []
unresolved_issues: []
---

# Content-preservation check

## Decision rationale

v012 保持了 v011 的研究身份、主要问题、研究对象、核心证据基础和推断单位。两项主要临床任务的估计目标，状态与事件定义，观察模型、模拟、外部验证和条件性试验分析方法，以及所有数值阈值、验证顺序、失败后果和证据强度均未改变。修订说明声明本轮只有语言与结构调整；逐项比较与该声明一致。

五项尚待冻结的方法规范在 v011 中分散于“尚待冻结的方法规范”、可行性状态表、模拟与校准方法、阈值登记和外部验证段落。v012 将它们集中为一份完整清单，并分别明示既有的决定时点、可使用信息和未解决后果。清单中的内容均可追溯到 v011 已有的拟合前冻结、外部结果隔离、模型准入或停止条件，没有新增数据、方法、估计目标、阈值或证据。72 个受保护项目均具有相同含义和强度，未发现未声明的科学变更、身份漂移、可行性问题隐藏或不受支持的结果主张。

## Protected-content trace

- PCR-010 与 PCR-020 的资源和范围要求由原“Resources and governance”迁至“Feasibility and resources”，内容完整保留。
- PCR-049、PCR-050 与 PCR-052 的待冻结规范由分散陈述集中至“Working assumptions and pending specifications”；可行性表只保留状态摘要，阈值登记和停止条件仍在后续权威表中保留。
- PCR-061 将公共 ICU 时间间隔段和试验稀疏访视段合并至“Limitations and boundary conditions”第 8 项；12 小时方案、前值延续限制、实测时间记录和不得连续插值均完整保留。
- PCR-062 将 D-dimer 首次出现规范为“D-二聚体（D-dimer）”，未改变单位待核验及不得推测字段的限制。
- 摘要、医院分组和主要结局状态段落仅拆句或澄清修饰范围；医院指标仍待冻结，固定种子、30%/70% 医院分配、外部数据隔离和主要结局排序均未改变。

## Required routing

科学内容已保存。v012 可进入新的独立叙述与语言评估；不需要返回科学审查。
