---
schema_version: research-idea-content-preservation-check.v1
check_id: content-preservation-I01-001-v003-to-v039-r063
review_id: content-preservation-r063
reviewer_skill: idea-narrative-assessor
reviewer_instance_id: preserve-v039-r063-fresh-20260719
workflow_id: RID-SEPSIS-CSM-20260717-001
round_id: direct-final-current-v6-r063
input_artifact_ids:
  - idea-dossier-I01-001-v003
  - idea-dossier-I01-001-v039
  - protected-content-register-I01-001-v003-r003
  - revision-delta-I01-001-v003-to-v039
input_versions:
  - v003
  - v039
  - r003
  - v003-to-v039
inputs:
  prior_dossier:
    artifact_id: idea-dossier-I01-001-v003
    version: v003
    path: tests/idea-test-0.9.0-preview.1/0.9.0-preview.1/03_ideas/nodes/I01-001/dossiers/idea-dossier-v003.md
  revised_dossier:
    artifact_id: idea-dossier-I01-001-v039
    version: v039
    path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v6/idea-dossier-v039.md
  protected_content_register:
    artifact_id: protected-content-register-I01-001-v003-r003
    version: r003
    path: tests/idea-narrative-forward-0.9.0-preview.3/run-001/inputs/protected-content-register-v003.yaml
  revision_delta:
    artifact_id: revision-delta-I01-001-v003-to-v039
    version: v003-to-v039
    path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v6/revision-delta-v003-to-v039.md
files_read:
  - tests/idea-test-0.9.0-preview.1/0.9.0-preview.1/03_ideas/nodes/I01-001/dossiers/idea-dossier-v003.md
  - tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v6/idea-dossier-v039.md
  - tests/idea-narrative-forward-0.9.0-preview.3/run-001/inputs/protected-content-register-v003.yaml
  - tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v6/revision-delta-v003-to-v039.md
isolation_mode: fresh_subagent
prior_scores_visible: false
source_edits_performed: false
decision: editorial_scope_violation
protected_item_checks:
  - protected_id: PCR-001
    prior_locator: "YAML frontmatter identity_anchor; Research question, objectives, and core hypothesis > Primary research question"
    revised_locator: "YAML frontmatter identity_anchor; Research question, objectives, and core hypothesis > Primary research question; Research design and methods > Mutually exclusive post-onset state and event system"
    semantic_status: preserved
    evidence: >-
      v039 的 identity_anchor 保持同一核心问题，正文仍以脓毒症为中心覆盖未发病在险时段、首次发病、发病后状态及结局；互斥状态仍包括持续脓毒症、生理恢复、恶化或新器官衰竭、活着离开 ICU、转院或无法继续观察和死亡。Identity and final stop boundary 还明确把改成普通预测列为需要另立研究构想的变化，因此研究身份和问题未漂移。
  - protected_id: PCR-002
    prior_locator: "YAML frontmatter identity_anchor.primary_objective; Research question, objectives, and core hypothesis > Objectives"
    revised_locator: "Title, summary, audience, and positioning > One-sentence complete-Idea summary, Primary audience, and Positioning and contribution frame; Expected outputs, falsification criteria, and interpretations > Planned outputs"
    semantic_status: changed
    evidence: >-
      v039 保留了 24 个月完成阶段 I–II、文献与专家先验、公共 ICU 数据、系统辨识角色、模拟重建、跨数据库检验、全过程状态表征以及可审计证据、基准和研究资源，也明确当前计划不是临床决策工具。但是，冻结条目还要求“高水平论文”作为交付方向；v039 的计划产物、目标和定位均未陈述论文为计划交付物。“当前不预设具体期刊”只限定受众和投稿定位，不能追踪到“高水平论文”这一交付承诺。delta 对 PCR-002 的说明同样没有给出可替代正文证据。
  - protected_id: PCR-003
    prior_locator: "YAML frontmatter identity_anchor.study_object and primary_unit_of_inference; Research design and methods"
    revised_locator: "YAML frontmatter identity_anchor; Title, summary, audience, and positioning > One-sentence complete-Idea summary; Research design and methods > Observational target, anchoring and conditions for non-interpretation"
    semantic_status: preserved
    evidence: >-
      v039 保持纵向、以脓毒症为中心的 ICU 患者系统，同时保留可比较的发病前在险时段和发病后轨迹。摘要把候选表征定义为量化患者—时间状态及转移不确定性的研究对象，frontmatter 与主要任务的不确定性规范继续要求尊重患者和医院聚类。
  - protected_id: PCR-004
    prior_locator: "Data, materials, and existing evidence base > Current verified-resource versus prospective-gate status; Public ICU database roles and G1 audit"
    revised_locator: "Data, materials, and existing evidence base > Current resource and evidence status; Public ICU database roles and G1 audit; Feasibility, resources, risks, alternatives, and stop conditions > Feasibility and resources"
    semantic_status: preserved
    evidence: >-
      v039 保留文献与专家先验、MIMIC-IV、eICU-CRD 及须在月 0–3 预先指定的 HiRID 或 AmsterdamUMCdb 备份。资源表只把数据库存在、版本和文献列为已有公开资料支持；团队凭证、数据使用协议、下载、存储和提取尚未核验，实际队列、事件、转移、医院、锚点与接口支持以及模型、模拟和检验结果尚未生成，具名人员与工时仍无可核验承诺。正文没有把这些状态写成已具备。
  - protected_id: PCR-005
    prior_locator: "Data, materials, and existing evidence base > Local RCT evidence and present limits"
    revised_locator: "Data, materials, and existing evidence base > Current resource and evidence status; Local randomized-trial evidence and present limits; Research design and methods > Randomized-trial observation bridge and independent clinical-state analysis under prespecified conditions"
    semantic_status: preserved
    evidence: >-
      EXIT-SEP 与 XBJ-SCAP 在 v039 中仍只是 24 个月最低交付之后、共享前提满足时的个体数据来源。本地报告仍被标为项目内衍生资料，且正文逐项说明它们不能替代个体数据授权、原始 CRF/SAP、随机化、分析集、中心、D0/D1/D7/D8 相对首剂时序以及死亡、住院、出院和转院语义核验。
  - protected_id: PCR-006
    prior_locator: "Research content and work packages; Research design and methods, including Observational target, anchoring, missingness and abstention"
    revised_locator: "Research content and work packages > Work packages and minimum route; Research design and methods > Candidate variable-role separation rules; Observational target, anchoring and conditions for non-interpretation; Simulation and semi-synthetic reconstruction criteria; Hospital-primary cross-database validation"
    semantic_status: preserved
    evidence: >-
      v039 保留固定顺序：资源与 G1、标签/状态/医院分配锁定、竞争风险与多状态基线、线性状态空间模型、模拟重建、至多一个复杂候选、两项主要任务和两项次要诊断、开发冻结、最终检验医院集，之后才是条件性试验分析。Y_t、A_t 与 M_t 仍分离。删除、合并或限制解释规则的全部数值未变：20 个种子对齐率低于 90%、自助法保留率低于 80%、最终检验医院集符号一致率低于 80%、状态对齐低于 0.70 或区间未校准时采取处置；较好的预测表现不能抵消。模拟部分还保留每情景至少 1,000 次或 Monte Carlo 标准误不超过 0.02，以及状态、转移、边检测、零边、错设和概率校准的原阈值与后果。
  - protected_id: PCR-007
    prior_locator: "Research content and work packages > Conjunctive minimum success definition; Research design and methods > Hospital-primary genuine cross-database validation"
    revised_locator: "Research content and work packages > Conjunctive minimum success definition; Research design and methods > Quantitative criteria for stage II; Hospital-primary cross-database validation; Feasibility, resources, risks, alternatives, and stop conditions > Global limitations and boundary conditions"
    semantic_status: preserved
    evidence: >-
      v039 将阶段 II 保持为五类证据的合取：两库与 G1 支持、复杂候选的模拟重建、两项主要任务的严格适当评分与校准、无高严重度泄漏，以及最终检验医院集中不更新任何参数时的任务表现、状态对齐和结构稳定。数值标准仍包括 Brier 差值上侧 95% 界不超过 +0.01、校准斜率 0.80–1.20、绝对风险误差不超过 0.02、至少 20 个合格最终检验医院、状态相关或一致性至少 0.70、符号一致率至少 0.80。四种参数处理状态分开报告，适配医院集上的有限重估不能替代不更新参数时未满足；阶段 III 明确不计入或补足阶段 II。
  - protected_id: PCR-008
    prior_locator: "Research design and methods > Protocol locks for the two primary clinical tasks; Mutually exclusive post-onset state/event system"
    revised_locator: "Research design and methods > Protocol specifications for the two primary clinical tasks; Mutually exclusive post-onset state and event system; Quantitative criteria for stage II"
    semantic_status: preserved
    evidence: >-
      两项主要任务、临床事件时刻与标签可用时刻、首次发病风险集、延迟进入、互斥状态、竞争终止、可用时刻约束、严格适当评分、校准以及患者与医院聚类均保留。关键时序与数值逐项一致：标本先发生时抗菌药在其后 72 小时内，给药先发生时标本在其后 24 小时内；基线 SOFA 使用入 ICU 前 24 小时规则；成分取滚动 24 小时最差值，增加至少 2 分发生在感染前 48 小时至后 24 小时并取首次可排序时刻；从 ICU 第 12 小时起每 12 小时分析，使用最多 24 小时且至少 12 小时历史，预测未来 12 小时；只分析首次发病，重叠时间标志点每次住院总权重为 1。A_t 与下一状态仍按同一时间窗排序，同一时间戳无法排序者不用于该边；泄漏检查继续覆盖同窗治疗、未来测量频率、重复住院、跨分配处理以及由结局决定的变量、时间方案和阈值。
  - protected_id: PCR-009
    prior_locator: "Structured abstract; Contribution, innovation, impact, application, and closest-work comparison > Contribution and evidence ladder"
    revised_locator: "Structured abstract; Data, materials, and existing evidence base > Current resource and evidence status; Contribution, innovation, impact, application, and closest-work comparison > Contribution and evidence ladder; Verified representative closest-work comparison"
    semantic_status: preserved
    evidence: >-
      v039 明确模型、模拟、重建、预测、跨数据库检验和试验新分析结果均尚未生成。贡献仍限于条件性的证据整合、验证、基准与研究资源；各模块已有先例，完整组合缺口仅为低至中等置信。标题、定位、最接近工作和主张表均不声称全球首次或新算法。
  - protected_id: PCR-010
    prior_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Resources and governance; Risk and automatic alternative matrix; Remaining execution gates; Identity and final stop boundary; Expected outputs, falsification criteria, and interpretations > Falsification and stop criteria"
    revised_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Feasibility and resources; Working assumptions and unresolved specifications; Global limitations and boundary conditions; Risks, alternatives, and stop conditions; Remaining execution requirements; Identity and final stop boundary"
    semantic_status: preserved
    evidence: >-
      第 14 节仍集中保留访问与数据使用协议、具名团队、G1、标签与泄漏、模拟重建、非随机缺失与低重叠、最终检验时不更新参数、月 12/20/24 节点、试验数据和核心语义、共同锚点与观测映射、最接近工作不确定性及对应的替代和停止后果。待定规范仍包括临床容许尺度到模拟参数的映射，以及多类别校准的精确估计量、置信区间和阈值登记；筛选用事件或参数下限明确不能替代经验有效样本量和模拟稳定性。两试验方向不一致或区间过宽时仍只能分试验报告无支持或跨场景适用性有限，且不得选择亚组改变结论。
  - protected_id: PCR-011
    prior_locator: "Research content and work packages > Twenty-four-month minimum and dated gates; Identity and final stop boundary"
    revised_locator: "Research content and work packages > Twenty-four-month minimum and dated decisions; Research design and methods > Randomized-trial observation bridge and independent clinical-state analysis under prespecified conditions; Feasibility, resources, risks, alternatives, and stop conditions > Global limitations and boundary conditions; Identity and final stop boundary"
    semantic_status: preserved
    evidence: >-
      v039 保留阶段 I–II 的 24 个月最低交付和位于其后的阶段 III。两种新访视分析的共享前提被单列为阶段 II 成功并冻结、相应试验个体数据分析授权，以及随机化/分析集、中心或分层、实际 D7/D8 时序和死亡/住院/活着出院/转院语义可核验。共同锚点与 R1 只决定一维投影摘要分支；它们未被提升为整个组件的共享前提。观测桥接不成立但 SOFA 和共享语义可核验时，独立临床状态分析仍可开展；核心语义不可核验时两种新访视结局都停止，只复现原终点或继续数据审计。正文多处明确任何试验结果均不能补足阶段 II 的资源、模拟重建、主要任务或跨数据库检验要求。
  - protected_id: PCR-012
    prior_locator: "Research question, objectives, and core hypothesis > Core hypothesis and non-hypotheses; Feasibility, resources, risks, alternatives, and stop conditions"
    revised_locator: "Research question, objectives, and core hypothesis > Core hypothesis and non-hypotheses; Expected outputs, falsification criteria, and interpretations > Interpretation matrix; Feasibility, resources, risks, alternatives, and stop conditions > Global limitations and boundary conditions"
    semantic_status: preserved
    evidence: >-
      v039 保留观察性数据和预测表现不能识别治疗因果效应、真实反馈网络、反事实策略、机制、中介或控制的边界；随机试验次要分析也不验证未测潜在动力学、转移边或候选表征整体。数字孪生、已验证模型、临床决策工具、药物平台和无条件临床推广均继续列为当前不支持的主张。
undeclared_scientific_changes:
  - change_id: USC-R063-001
    protected_id: PCR-002
    description: >-
      冻结目标中的“高水平论文作为交付方向”未在 v039 正文中保留，revision delta 又声明没有科学变化，因此该删除没有得到声明或授权。
findings:
  - finding_id: CPF-R063-001
    severity: blocking
    protected_id: PCR-002
    finding: >-
      v039 未提供“高水平论文”为计划交付方向的正文证据；受众、期刊未预设、可审计证据、基准和资源不能替代这一明确交付承诺。
    required_resolution: >-
      若该交付方向仍属冻结目标，应在目标、定位或计划产物的权威位置明确恢复；若拟取消，则须声明为科学目标或交付范围变化并返回相应科学审查。任何实质性修订后都需要新的独立内容保全复核。
unresolved_issues: []
---

# Content-preservation check

## Decision rationale

PCR-001 及 PCR-003 至 PCR-012 均能在 v039 正文中以相同含义、状态和主张强度追踪。共享试验前提、投影摘要分支、独立临床状态分支、整个试验组件的停止条件、阶段 III 不得补足阶段 II、两试验结果不得用亚组改变结论，以及全部登记的数值与时序规则均保持不变。资源、证据和可行性事项也继续区分已有公开资料支持、尚未核验、尚未生成和项目内衍生资料。

PCR-002 只有部分保留。v039 保留 24 个月阶段 I–II、知识与公共数据库输入、系统辨识与跨数据库验证、全过程状态表征、可审计证据、基准和资源，但没有把冻结条目所列的“高水平论文”写成计划交付方向。由于 revision delta 声明没有科学变化，这一遗漏构成未声明的编辑范围越界，而不是研究身份漂移。

## Protected-content trace

- 主要协议和数值规则被移至 `Research design and methods` 的协议、模拟重建、阶段 II 定量标准和跨数据库检验小节；含义与后果保持不变。
- 随机试验的共享前提、R0/R1、一维投影摘要、独立临床状态分析及整体停止条件被集中到同一方法小节；投影专属条件没有被提升为共享前提，独立分支也没有因投影失败而消失。
- 资源、未决规范、全局边界、风险及停止条件集中到 `Feasibility, resources, risks, alternatives, and stop conditions`；未发现把尚未核验或尚未生成事项改写为已完成。
- 唯一不能在正文中追踪的保护内容是 PCR-002 的“高水平论文作为交付方向”。revision delta 不能替代缺失的正文陈述。

## Required routing

v039 目前不得直接进入新的叙事或语言评估。应先恢复 PCR-002 的交付方向，或把取消该方向明确声明为需要科学审查的范围变化；完成任何实质性修订后，再由新的独立 reviewer 重新执行内容保全检查。
