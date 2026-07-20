---
schema_version: research-idea-content-preservation-check.v1
check_id: content-preservation-I01-001-r131
review_id: idea-narrative-assessor-preservation-I01-001-r131
reviewer_skill: idea-narrative-assessor
reviewer_instance_id: fresh-content-preservation-reviewer-r131
workflow_id: RID-SEPSIS-CSM-20260717-001
round_id: r131
input_artifact_ids:
  - idea-dossier-I01-001-v056
  - idea-dossier-I01-001-v057
  - protected-content-register-I01-001-v056-v008
  - revision-delta-I01-001-v056-to-v057
input_versions: [v056, v057, v008, v056-to-v057]
inputs:
  prior_dossier:
    artifact_id: idea-dossier-I01-001-v056
    version: v056
    path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v22/idea-dossier-v056.md
  revised_dossier:
    artifact_id: idea-dossier-I01-001-v057
    version: v057
    path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v23/idea-dossier-v057.md
  protected_content_register:
    artifact_id: protected-content-register-I01-001-v056-v008
    version: v008
    path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v22/protected-content-register-v008.yaml
  revision_delta:
    artifact_id: revision-delta-I01-001-v056-to-v057
    version: v056-to-v057
    path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v23/revision-delta-v056-to-v057.md
files_read:
  - tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v22/idea-dossier-v056.md
  - tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v22/protected-content-register-v008.yaml
  - tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v23/idea-dossier-v057.md
  - tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v23/revision-delta-v056-to-v057.md
isolation_mode: fresh_subagent
prior_scores_visible: false
source_edits_performed: false
decision: scientific_content_preserved
protected_item_checks:
  - protected_id: PCR-001
    prior_locator: "frontmatter > identity_anchor"
    revised_locator: "frontmatter > identity_anchor"
    semantic_status: preserved
    evidence: "五个 identity_anchor 值逐字符一致，研究问题、目标、对象、证据基础和推断单位均未改变。"
  - protected_id: PCR-002
    prior_locator: "Research question, objectives, and core hypothesis > Primary research question; Objectives"
    revised_locator: "Research question, objectives, and core hypothesis > Primary research question; Objectives"
    semantic_status: preserved
    evidence: "重症监护全病程范围、四项目标、阶段 II 达标后才启动的分试验延伸、非因果边界和科学交付均保留；变化仅区分候选动态表征、候选复杂模型和待检验结构关系。"
  - protected_id: PCR-003
    prior_locator: "Research question, objectives, and core hypothesis > Core hypothesis and evidence boundary"
    revised_locator: "Research question, objectives, and core hypothesis > Core hypothesis and evidence boundary"
    semantic_status: preserved
    evidence: "共同变量和事件支持、分析前固定、绝对恢复与错设检查、允许的不变量及非因果估计边界均保留。"
  - protected_id: PCR-004
    prior_locator: "Research design and methods > Observational target, anchoring, and evidence-qualified interpretation"
    revised_locator: "Research design and methods > Observational target, anchoring, and evidence-qualified interpretation"
    semantic_status: preserved
    evidence: "研究对象、患者—时间状态与转移的推断单位、患者和医院聚类、X/Y/A/M/B/S 角色、联合分布及派生目标均一致。"
  - protected_id: PCR-005
    prior_locator: "Research design and methods > Protocol locks for the two primary clinical tasks"
    revised_locator: "Research design and methods > Protocol locks for the two primary clinical tasks"
    semantic_status: preserved
    evidence: "成人队列、首个停留与首次发病、可见历史、延迟进入、权重、互斥终止和删失敏感性规则均未改变。"
  - protected_id: PCR-006
    prior_locator: "Research design and methods > Mutually exclusive post-onset state and event system"
    revised_locator: "Research design and methods > Mutually exclusive post-onset state and event system"
    semantic_status: preserved
    evidence: "12 小时赋值、固定优先级、不可排序时规则、吸收/终末状态、恢复复发和持续脓毒症转移均保留。"
  - protected_id: PCR-007
    prior_locator: "Data, materials, and existing evidence base > Variable roles"
    revised_locator: "Data, materials, and existing evidence base > Variable roles"
    semantic_status: preserved
    evidence: "生理、治疗、测量、标签和基线角色及 SOFA/行动副本隔离、接口与患者状态分离、禁止伪测量等边界均一致。"
  - protected_id: PCR-008
    prior_locator: "Data, materials, and existing evidence base > Public intensive-care database roles and support audit"
    revised_locator: "Data, materials, and existing evidence base > Public intensive-care database roles and support audit"
    semantic_status: preserved
    evidence: "MIMIC 开发角色、eICU 适配和隔离测试角色、月 0–3 备份规则、共同概念审计及数据库特异信息的探索性角色均保留。"
  - protected_id: PCR-009
    prior_locator: "Data, materials, and existing evidence base > Public intensive-care database roles and support audit > audit table"
    revised_locator: "Data, materials, and existing evidence base > Public intensive-care database roles and support audit > audit table"
    semantic_status: preserved
    evidence: "访问/支持审计以及 20/10 事件与转移、30% 密度、70% 医院、80% 患者、维度/状态上限和 12→24 小时→事件时间规则全部保留。"
  - protected_id: PCR-010
    prior_locator: "Data, materials, and existing evidence base > Current resource and result status"
    revised_locator: "Data, materials, and existing evidence base > Current resource and result status"
    semantic_status: preserved
    evidence: "数据库存在与版本已核验，而访问、提取、支持审计、模型、恢复、预测和外部结果均未完成；最接近工作置信边界不变。"
  - protected_id: PCR-011
    prior_locator: "Data, materials, and existing evidence base > Local randomized-trial evidence status"
    revised_locator: "Data, materials, and existing evidence base > Local randomized-trial evidence status"
    semantic_status: preserved
    evidence: "EXIT-SEP 与 XBJ-SCAP 的样本量、非缺失数、缺失字段、D-二聚体不确定性及衍生证据限制逐项保留。"
  - protected_id: PCR-012
    prior_locator: "Data, materials, and existing evidence base > Current resource and result status > trial rows"
    revised_locator: "Data, materials, and existing evidence base > Current resource and result status > trial rows"
    semantic_status: preserved
    evidence: "授权、原始材料、随机化/中心/访视与结局语义、共同锚点和单位仍待核验，数据持有人确认要求不变。"
  - protected_id: PCR-013
    prior_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Feasibility and resources"
    revised_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Feasibility and resources"
    semantic_status: preserved
    evidence: "六类必需职责、人员承诺未核验、两个数据库/四维/三状态/两任务/两诊断/一个复杂模型上限及排除工作均保留。"
  - protected_id: PCR-014
    prior_locator: "Research content and work packages > Work packages and minimum route"
    revised_locator: "Research content and work packages > Work packages and minimum route"
    semantic_status: preserved
    evidence: "资源审计至冻结模型外部验证再到条件性试验分析的完整先后顺序，以及简单表征、备份或停止后果均未改变。"
  - protected_id: PCR-015
    prior_locator: "Research content and work packages > Conjunctive minimum success definition"
    revised_locator: "Research content and work packages > Conjunctive minimum success definition"
    semantic_status: preserved
    evidence: "数据支持、模拟、两项主要任务、泄漏、医院支持、冻结模型验证、对齐、符号一致、适配与阶段 III 的全部合取条件均保留。"
  - protected_id: PCR-016
    prior_locator: "Research design and methods > Protocol locks for the two primary clinical tasks > primary pre-onset task column"
    revised_locator: "Research design and methods > Protocol locks for the two primary clinical tasks > primary pre-onset task column"
    semantic_status: preserved
    evidence: "未来 12 小时累计发生风险、标志时点、历史窗、指标、自助区间及 +0.01、0.80–1.20、0.02 和泄漏门槛均一致。"
  - protected_id: PCR-017
    prior_locator: "Research design and methods > Protocol locks for the two primary clinical tasks > primary post-onset task column"
    revised_locator: "Research design and methods > Protocol locks for the two primary clinical tasks > primary post-onset task column"
    semantic_status: preserved
    evidence: "第 7 日有利集合、组成分报、多状态/Aalen–Johansen、14 日敏感性、延迟进入、指标、聚类区间及同一门槛均保留。"
  - protected_id: PCR-018
    prior_locator: "Research design and methods > Protocol locks for the two primary clinical tasks > event clock and information-availability clock"
    revised_locator: "Research design and methods > Protocol locks for the two primary clinical tasks > event clock and information-availability clock"
    semantic_status: preserved
    evidence: "72/24 小时感染配对、SOFA 基线与滚动窗、−48/+24 小时发病窗、可用时钟和仅两种敏感标签均未改变。"
  - protected_id: PCR-019
    prior_locator: "Research design and methods > Mutually exclusive post-onset state and event system > state definitions"
    revised_locator: "Research design and methods > Mutually exclusive post-onset state and event system > state definitions"
    semantic_status: preserved
    evidence: "恢复、恶化、器官支持、退出、转院和死亡的阈值、时刻与变量角色均一致。"
  - protected_id: PCR-020
    prior_locator: "Research design and methods > Observational target, anchoring, and evidence-qualified interpretation"
    revised_locator: "Research design and methods > Observational target, anchoring, and evidence-qualified interpretation"
    semantic_status: preserved
    evidence: "每维至少两锚点、首载荷 +1、稀疏约束、四维/三状态/一至两窗、20 种子对齐及可解释目标均保留。"
  - protected_id: PCR-021
    prior_locator: "Research design and methods > Observational target, anchoring, and evidence-qualified interpretation > missingness and action support"
    revised_locator: "Research design and methods > Observational target, anchoring, and evidence-qualified interpretation > missingness and action support"
    semantic_status: preserved
    evidence: "显式测量模型、−1/−0.5/0/+0.5/+1 SD 网格、临界点、5%/95% 行动比例、20% 有效样本量和不估计治疗作用规则均一致。"
  - protected_id: PCR-022
    prior_locator: "Research design and methods > Absolute simulation and semi-synthetic recovery criteria > simulation regimen"
    revised_locator: "Research design and methods > Absolute simulation and semi-synthetic recovery criteria > simulation regimen"
    semantic_status: preserved
    evidence: "月 7–10、至少 1,000 次或 MCSE≤0.02、生成机制及全部交叉情景均保留，隔离测试结果仍不可用于模拟。"
  - protected_id: PCR-023
    prior_locator: "Research design and methods > Absolute simulation and semi-synthetic recovery criteria > continuous branch"
    revised_locator: "Research design and methods > Absolute simulation and semi-synthetic recovery criteria > continuous branch"
    semantic_status: preserved
    evidence: "X_b/估计矩阵、同一评估行、d_b 个非负典型相关、失败记 r_b=0、不得结果驱动删除、L 公式及 L≥0.80 均完全一致。"
  - protected_id: PCR-024
    prior_locator: "Research design and methods > Absolute simulation and semi-synthetic recovery criteria > recovery criteria table"
    revised_locator: "Research design and methods > Absolute simulation and semi-synthetic recovery criteria > recovery criteria table"
    semantic_status: preserved
    evidence: "ARI、对齐、转移误差/覆盖、符号/滞后、边检测、零边、错设、校准阈值与失败动作全部保留。"
  - protected_id: PCR-025
    prior_locator: "Research design and methods > Hospital-primary cross-database validation > partition and cross-hospital-patient rules"
    revised_locator: "Research design and methods > Hospital-primary cross-database validation > partition and cross-hospital-patient rules"
    semantic_status: preserved
    evidence: "种子 20260717 的 30%/70% 医院分区、患者排除、结局前报告、二部图敏感性、支持门槛、备份和主张限制均一致。"
  - protected_id: PCR-026
    prior_locator: "Research design and methods > Hospital-primary cross-database validation > four update operations"
    revised_locator: "Research design and methods > Hospital-primary cross-database validation > four update operations"
    semantic_status: preserved
    evidence: "冻结模型外部验证明确不重新校准或更新参数；其后仅校准、仅观测层和全模型重拟合的顺序、角色、测试资料禁用及失败解释均保留。"
  - protected_id: PCR-027
    prior_locator: "Research design and methods > 试验观测映射和独立分析 > 共享前提"
    revised_locator: "Research design and methods > 试验观测映射和独立分析 > 共享前提"
    semantic_status: preserved
    evidence: "阶段 II 全部达标、授权和原始语义核验仍是共享前提；锚点数与忠实度仍只属于映射分支，两个试验仍分开且从属。"
  - protected_id: PCR-028
    prior_locator: "Research design and methods > 试验观测映射和独立分析 > 观测映射成立时的有序访视结局分析及外部忠实度判定"
    revised_locator: "Research design and methods > 试验观测映射和独立分析 > 观测映射成立时的有序访视结局分析及外部忠实度判定"
    semantic_status: preserved
    evidence: "锚点资格、冻结标准化/SVD/符号、eICU 忠实度全部阈值、盲态试验阈值及映射失格规则均保留。"
  - protected_id: PCR-029
    prior_locator: "Research design and methods > 试验观测映射和独立分析 > 分层标准化概率指数"
    revised_locator: "Research design and methods > 试验观测映射和独立分析 > 分层标准化概率指数"
    semantic_status: preserved
    evidence: "结局排序、theta_PI 完整公式、合并组层权重、并列半分、方向、区间/检验、次要量角色和分试验估计均完全一致。"
  - protected_id: PCR-030
    prior_locator: "Research design and methods > 试验观测映射和独立分析 > 观测映射不成立但独立分析条件成立时的分析; 核心语义不足时停止"
    revised_locator: "Research design and methods > 试验观测映射和独立分析 > 观测映射不成立但独立分析条件成立时的分析; 核心语义不足时停止"
    semantic_status: preserved
    evidence: "映射失败时独立 SOFA 分支仍可按自身条件运行，核心语义不足则停止新访视分析；互斥分支未被合并为共享门槛。"
  - protected_id: PCR-031
    prior_locator: "Research design and methods > 试验观测映射和独立分析 > EXIT-SEP and XBJ-SCAP trial table"
    revised_locator: "Research design and methods > 试验观测映射和独立分析 > EXIT-SEP and XBJ-SCAP trial table"
    semantic_status: preserved
    evidence: "两试验人群/访视、分析集、插补与偏移、界限、结构性缺失、Holm 0.05、交互和禁止伪轨迹规则均保留。"
  - protected_id: PCR-032
    prior_locator: "Research design and methods > Secondary representation diagnostics"
    revised_locator: "Research design and methods > Secondary representation diagnostics"
    semantic_status: preserved
    evidence: "伪遮蔽与未来轨迹诊断的指标、分层及不得改变主要决定的边界均未改变。"
  - protected_id: PCR-033
    prior_locator: "Required analyses and evidence; Research design and methods > 试验观测映射和独立分析"
    revised_locator: "Required analyses and evidence; Research design and methods > 试验观测映射和独立分析"
    semantic_status: preserved
    evidence: "阶段 II 的资源、审计、单元测试、隔离、基线、模拟、对照、任务、四种操作和合取表，以及试验特异证据均完整保留。"
  - protected_id: PCR-034
    prior_locator: "Expected outputs, falsification criteria, and interpretations > Falsification and stop criteria > clocks, leakage, and data support"
    revised_locator: "Expected outputs, falsification criteria, and interpretations > Falsification and stop criteria > clocks, leakage, and data support"
    semantic_status: preserved
    evidence: "未来信息/跨拆分泄漏失败、修正或删除、隔离测试阻断、支持不足时简化/备份/停止的后果均保留。"
  - protected_id: PCR-035
    prior_locator: "Expected outputs, falsification criteria, and interpretations > Falsification and stop criteria > recovery, missingness, action support, and external result"
    revised_locator: "Expected outputs, falsification criteria, and interpretations > Falsification and stop criteria > recovery, missingness, action support, and external result"
    semantic_status: preserved
    evidence: "恢复/覆盖/零边/错设失败、缺失敏感性、行动支持、冻结模型验证失败及有限适配不得修复主结论均保留。"
  - protected_id: PCR-036
    prior_locator: "Expected outputs, falsification criteria, and interpretations > Falsification and stop criteria > trial criteria"
    revised_locator: "Expected outputs, falsification criteria, and interpretations > Falsification and stop criteria > trial criteria"
    semantic_status: preserved
    evidence: "映射忠实度失败、独立 SOFA 资格、核心语义停止、方向不一致/区间过宽和禁止亚组修复均未改变。"
  - protected_id: PCR-037
    prior_locator: "Expected outputs, falsification criteria, and interpretations > Falsification and stop criteria > time"
    revised_locator: "Expected outputs, falsification criteria, and interpretations > Falsification and stop criteria > time"
    semantic_status: preserved
    evidence: "月 12 封存简单表征、月 20 不访问隔离测试集、月 24 阶段 II 最低端点未完成的后果保持一致。"
  - protected_id: PCR-038
    prior_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Risks, alternatives, and stop conditions"
    revised_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Risks, alternatives, and stop conditions"
    semantic_status: preserved
    evidence: "数据库/支持、团队、隔离、跨院、试验、时间和最接近工作变化的触发条件、备选与停止后果均完整保留。"
  - protected_id: PCR-039
    prior_locator: "Title, summary, audience, and positioning; Structured abstract"
    revised_locator: "Title, summary, audience, and positioning; Structured abstract"
    semantic_status: preserved
    evidence: "标题和摘要仍为候选动态表征与计划检验；所有输出保持待生成，条件性贡献和从属试验延伸的主张强度未提高。"
  - protected_id: PCR-040
    prior_locator: "Contribution, innovation, impact, application, and closest-work comparison > Contribution and evidence ladder"
    revised_locator: "Contribution, innovation, impact, application, and closest-work comparison > Contribution and evidence ladder"
    semantic_status: preserved
    evidence: "数据可追溯、状态/任务、冻结模型外部验证和试验差异的逐级证据要求及缺失的因果/应用证据均保留。"
  - protected_id: PCR-041
    prior_locator: "Contribution, innovation, impact, application, and closest-work comparison > Verified representative closest-work comparison"
    revised_locator: "Contribution, innovation, impact, application, and closest-work comparison > Verified representative closest-work comparison"
    semantic_status: preserved
    evidence: "各类先例、有界检索截至日期、组件高置信和组合低至中等置信，以及非新算法/非全球首次边界均未改变。"
  - protected_id: PCR-042
    prior_locator: "Expected outputs, falsification criteria, and interpretations > Interpretation matrix"
    revised_locator: "Expected outputs, falsification criteria, and interpretations > Interpretation matrix"
    semantic_status: preserved
    evidence: "简单模型、模拟、冻结模型验证、有限适配、任务、两类试验分支及全合取的允许/禁止解释逐行保留。"
  - protected_id: PCR-043
    prior_locator: "Research design and methods > 试验观测映射和独立分析; Evidence chain: 有前置条件的随机试验次要分析"
    revised_locator: "Research design and methods > 试验观测映射和独立分析; Evidence chain: 有前置条件的随机试验次要分析"
    semantic_status: preserved
    evidence: "试验结果仍为分开、次要、条件性且不计入阶段 II；只能支持试验内预设有序访视结局差异，不支持合并效应或共同机制。"
  - protected_id: PCR-044
    prior_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Working assumptions > continuous latent-state recovery row"
    revised_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Working assumptions > continuous latent-state recovery row"
    semantic_status: preserved
    evidence: "连续恢复的唯一计算定义、两位负责人、月 7 前截止、失败或事后改定义的后果和简单路线均完整保留。"
  - protected_id: PCR-045
    prior_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Working assumptions > trial probability-index row"
    revised_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Working assumptions > trial probability-index row"
    semantic_status: preserved
    evidence: "唯一 theta_PI 估计目标、并列半分、层与权重、具名统计负责人、治疗标签前确认和未确认时停止均一致。"
  - protected_id: PCR-046
    prior_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Working assumptions > clinical-scale-to-simulation mapping row"
    revised_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Working assumptions > clinical-scale-to-simulation mapping row"
    semantic_status: preserved
    evidence: "月 7 前仅据临床容许范围、开发审计和不含隔离测试结果的先导模拟固定映射；未解决则不启动恢复且复杂模型不晋级。"
  - protected_id: PCR-047
    prior_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Working assumptions > multicategory-calibration row"
    revised_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Working assumptions > multicategory-calibration row"
    semantic_status: preserved
    evidence: "月 6 前固定估计量/置信界/登记形式、固定 Brier 与校准阈值、只能收紧、未解决则不判定成功且不访问测试集均保留。"
  - protected_id: PCR-048
    prior_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Limitations and boundary conditions > 1. Resources, access, and team status"
    revised_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Limitations and boundary conditions > 1. 资源、访问与团队状态"
    semantic_status: preserved
    evidence: "数据库存在不等于访问/提取、职责不等于承诺、项目级样本与支持未审计及官方规模不能代替项目计数，完整保留于限制权威位置。"
  - protected_id: PCR-049
    prior_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Limitations and boundary conditions > 2. Labels, clocks, and leakage"
    revised_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Limitations and boundary conditions > 2. 标签、时钟与信息泄漏"
    semantic_status: preserved
    evidence: "Sepsis-3 无唯一 EHR 时刻、标签依赖、时间戳/双重用途/测量/重复住院/跨拆分泄漏及高严重度门槛完整保留。"
  - protected_id: PCR-050
    prior_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Limitations and boundary conditions > 3. State recoverability and structural scope"
    revised_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Limitations and boundary conditions > 3. 状态可恢复性与待检验结构关系范围"
    semantic_status: preserved
    evidence: "允许重参数化、模拟不等于真实识别、预测不能替代恢复/对齐/覆盖证据及失败状态/边的删除、合并或限定均保留。"
  - protected_id: PCR-051
    prior_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Limitations and boundary conditions > 4. Nonrandom missingness and low action overlap"
    revised_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Limitations and boundary conditions > 4. 非随机缺失与低行动重叠"
    semantic_status: preserved
    evidence: "缺失敏感性方法不能识别未测真值，以及低重叠/低有效样本量只支持政策特异关联而非治疗效应，完整保留。"
  - protected_id: PCR-052
    prior_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Limitations and boundary conditions > 5. Cross-database evidence"
    revised_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Limitations and boundary conditions > 5. 跨数据库证据"
    semantic_status: preserved
    evidence: "数据库差异与接口缺失、冻结模型外部验证的主要证据角色、两类有限适配和全模型重拟合的分离及不得修复主失败均保留。"
  - protected_id: PCR-053
    prior_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Limitations and boundary conditions > 6. Time and delivery boundary"
    revised_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Limitations and boundary conditions > 6. 时间与交付边界"
    semantic_status: preserved
    evidence: "24 个月边界、月 12/20/24 后果、阶段 III 从属及后续试验不能补足阶段 I–II 证据均完整保留。"
  - protected_id: PCR-054
    prior_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Limitations and boundary conditions > 7. Trial data and semantics"
    revised_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Limitations and boundary conditions > 7. 试验数据与语义"
    semantic_status: preserved
    evidence: "两试验仅为条件性个体数据来源、衍生报告不能替代授权与原始语义、稀疏/人群/字段差异及禁止伪轨迹和合并效应均保留。"
  - protected_id: PCR-055
    prior_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Limitations and boundary conditions > 8. Common physiological anchor variables and observation mapping"
    revised_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Limitations and boundary conditions > 8. 共同生理锚点变量与观测映射"
    semantic_status: preserved
    evidence: "WBC/CRP 仍仅为备选、D-二聚体单位未核验、无映射忠实度结果、映射结局范围及独立 SOFA 边界均完整保留。"
  - protected_id: PCR-056
    prior_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Limitations and boundary conditions > 9. Closest-work uncertainty"
    revised_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Limitations and boundary conditions > 9. 最接近工作不确定性"
    semantic_status: preserved
    evidence: "非系统综述、未穷尽的来源、术语/预印本影响、组合缺口低至中等置信及组件已有先例完整保留。"
  - protected_id: PCR-057
    prior_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Limitations and boundary conditions > 10. Regulatory applicability"
    revised_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Limitations and boundary conditions > 10. 监管适用范围"
    semantic_status: preserved
    evidence: "2026 Surviving Sepsis Campaign 的监管谨慎边界及不得据条件性试验分析作无条件国际推广均保留。"
  - protected_id: PCR-058
    prior_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Limitations and boundary conditions > 11. Complete prohibited claims"
    revised_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Limitations and boundary conditions > 11. 完整禁止主张"
    semantic_status: preserved
    evidence: "因果网络/效应/策略/机制/中介/控制/数字孪生、试验不能验证整体系统、非已验证工具/平台/推广及禁止亚组修复全部保留。"
  - protected_id: PCR-059
    prior_locator: "Research content and work packages > 24 个月最低交付与时间节点"
    revised_locator: "Research content and work packages > 24 个月最低交付与时间节点"
    semantic_status: preserved
    evidence: "签署仅表示职责、人员承诺未核验、独立保管人控制月 18–20 前访问和月 20 后不得据测试结果修改均保留。"
  - protected_id: PCR-060
    prior_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Working assumptions > closing qualification"
    revised_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Working assumptions > closing qualification"
    semantic_status: preserved
    evidence: "事件/参数下限仅为筛选、仍需经验有效样本/模拟/聚类支持、待定规范须按时固定且不得事后补写数值，均未改变。"
  - protected_id: PCR-061
    prior_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Limitations and boundary conditions > 11. Complete prohibited claims"
    revised_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Limitations and boundary conditions > 11. 完整禁止主张"
    semantic_status: preserved
    evidence: "真实因果网络、治疗因果效应、反事实策略、机制、中介、控制和数字孪生仍明确列为不支持主张。"
  - protected_id: PCR-062
    prior_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Limitations and boundary conditions > 11. Complete prohibited claims; Contribution and evidence ladder"
    revised_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Limitations and boundary conditions > 11. 完整禁止主张; Contribution and evidence ladder"
    semantic_status: preserved
    evidence: "不得称已验证模型、临床决策工具、药物平台、临床有效或无条件推广，且缺失的识别/干预/前瞻安全效用/治理证据仍明确。"
  - protected_id: PCR-063
    prior_locator: "Contribution, innovation, impact, application, and closest-work comparison > Verified representative closest-work comparison"
    revised_locator: "Contribution, innovation, impact, application, and closest-work comparison > Verified representative closest-work comparison"
    semantic_status: preserved
    evidence: "不支持新算法、全球首次、领域首次或专利不存在；更强新颖性需新检索，当前仅为低至中等置信的条件性整合与验证。"
  - protected_id: PCR-064
    prior_locator: "Expected outputs, falsification criteria, and interpretations > Interpretation matrix; Research design and methods > 试验观测映射和独立分析"
    revised_locator: "Expected outputs, falsification criteria, and interpretations > Interpretation matrix; Research design and methods > 试验观测映射和独立分析"
    semantic_status: preserved
    evidence: "试验访视差异仍不能验证潜在动力学、转移边、测量模型外结构或整个系统；无合并机制且亚组不得修复主要解释。"
undeclared_scientific_changes: []
findings: []
unresolved_issues: []
---

# Content-preservation check

## Decision rationale

决定为 `scientific_content_preserved`。冻结清单中的 64 个受保护项目均在 v057 中可追溯且语义、条件性和主张强度不变；七类内容覆盖均为源稿存在，未出现漏项或新增类别。五个机器可读身份锚点逐字符一致。修订差异声明为编辑性术语澄清，实际文本也只区分了总体候选动态表征、候选复杂模型、潜在状态表征、待检验结构关系，以及按时间留出、按医院留出、隔离测试集和冻结模型外部验证等不同角色；没有声明或引入科学变更。

研究阶段、工作包先后关系、共享前提与互斥分支、四种跨数据库操作、四项工作假设、失败后果、证据层级和不支持主张均保持原义。正文中的阿拉伯数字及其出现次数一致；两条显示公式、公式中的变量、阈值、方向和失败记值均一致。第 14 节仍按原顺序保留 11 个完整限制族，并继续作为完整限制与边界条件的权威位置。

## Protected-content trace

- 总体研究对象从“候选动态系统表征”等表述统一为“候选动态表征”；这未改变重症监护期间的发病前风险、首次发病、发病后状态、转移和结局范围。
- 拟合的复杂方法统一称为“候选复杂模型”，模型输出称为“潜在状态表征”，边、符号、滞后、依赖与稳定性统一称为“待检验结构关系”；可恢复性门槛和非因果边界未改变。
- “时间外/医院外”统一为“按时间留出的验证/按医院留出的验证”；第二数据库未参与开发的测试资料统一为“隔离测试集”。
- 原“不更新外部检验”统一为“冻结模型外部验证”，并在方法权威位置明确定义为不重新校准或更新参数；仅校准适配、仅观测层适配和全模型重拟合仍是后续三个独立操作，且不能修复冻结模型外部验证失败。
- WBC、CRP 等非核心“候选变量”用“备选变量”表述；其资格、单位、证据状态和映射门槛未改变。

## Required routing

该 dossier 可进入全新的 narrative assessment 和 language assessment；不需要返回科学审查。
