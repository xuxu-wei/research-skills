---
schema_version: research-idea-content-preservation-check.v1
check_id: content-preservation-check-I01-001-v044-r074
review_id: content-preservation-review-I01-001-v044-r074
reviewer_skill: idea-narrative-assessor
reviewer_instance_id: idea-narrative-assessor-preservation-r074
workflow_id: RID-SEPSIS-CSM-20260717-001
round_id: r074
input_artifact_ids:
  - idea-dossier-I01-001-v003
  - idea-dossier-I01-001-v044
  - protected-content-register-I01-001-v004-r004
  - revision-delta-I01-001-v003-to-v044
input_versions:
  - v003
  - v044
  - r004
  - v044
inputs:
  prior_dossier:
    artifact_id: idea-dossier-I01-001-v003
    version: v003
    path: tests/idea-test-0.9.0-preview.1/0.9.0-preview.1/03_ideas/nodes/I01-001/dossiers/idea-dossier-v003.md
  revised_dossier:
    artifact_id: idea-dossier-I01-001-v044
    version: v044
    path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v10/idea-dossier-v044.md
  protected_content_register:
    artifact_id: protected-content-register-I01-001-v004-r004
    version: r004
    path: tests/idea-narrative-forward-0.9.0-preview.3/run-001/inputs/protected-content-register-v004.yaml
  revision_delta:
    artifact_id: revision-delta-I01-001-v003-to-v044
    version: v044
    path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v10/revision-delta-v003-to-v044.md
files_read:
  - tests/idea-test-0.9.0-preview.1/0.9.0-preview.1/03_ideas/nodes/I01-001/dossiers/idea-dossier-v003.md
  - tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v10/idea-dossier-v044.md
  - tests/idea-narrative-forward-0.9.0-preview.3/run-001/inputs/protected-content-register-v004.yaml
  - tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v10/revision-delta-v003-to-v044.md
isolation_mode: fresh_subagent
prior_scores_visible: false
source_edits_performed: false
decision: scientific_content_preserved
protected_item_checks:
  - protected_id: PCR-001
    prior_locator: "YAML identity_anchor；Research question, objectives, and core hypothesis > Primary research question"
    revised_locator: "YAML identity_anchor；Background；Research question, objectives, and core hypothesis > Primary research question"
    semantic_status: preserved
    evidence: >-
      研究身份仍是以脓毒症为中心、覆盖发病前在险时段、首次发病、发病后状态演化以及离开 ICU 或死亡结局的候选动态系统表征。修订稿继续把患者—时间状态与转移、模拟重建及跨数据库检验作为核心，而非普通临床预测或泛 ICU 风险分层。
  - protected_id: PCR-002
    prior_locator: "YAML identity_anchor.primary_objective；Research question, objectives, and core hypothesis > Objectives"
    revised_locator: "Research question, objectives, and core hypothesis > Objectives；Background > Significance；Contribution, innovation, impact, application, and closest-work comparison > 正向计划贡献及其证据范围"
    semantic_status: preserved
    evidence: >-
      修订稿明确保留 24 个月主体期限、文献与专家知识约束、纵向公共 ICU 数据、系统辨识、模拟重建和跨数据库检验，并把可审计科学证据、高水平论文及基准资源列为交付方向；同时明确交付不收缩为单一预测工具。
  - protected_id: PCR-003
    prior_locator: "YAML identity_anchor.study_object and primary_unit_of_inference；Research design and methods"
    revised_locator: "Background；Primary research question；两项主要临床任务的预先锁定规范"
    semantic_status: preserved
    evidence: >-
      研究对象仍包括可比较的未发病在险时段与发病后轨迹，主要推断单位仍是患者—时间状态及其转移。主要任务表继续规定一次住院总权重以及患者和医院层级聚类区间。
  - protected_id: PCR-004
    prior_locator: "Data, materials, and existing evidence base > Current verified-resource versus prospective-gate status；Public ICU database roles and G1 audit"
    revised_locator: "Data, materials, and existing evidence base > 现有证据与可用性状态；公共 ICU 数据来源及计划用途；Feasibility, resources, risks, alternatives, and stop conditions > 可行性与资源"
    semantic_status: preserved
    evidence: >-
      文献与专家知识、MIMIC-IV 和 eICU-CRD 仍是核心输入，HiRID 或 AmsterdamUMCdb 仍只是预先指定后方可使用的条件性备份。公开存在和版本与团队访问、数据使用协议、可运行提取、项目队列、具名人员及模型结果继续被分开；后者均未被写成已经具备或已经生成。
  - protected_id: PCR-005
    prior_locator: "Data, materials, and existing evidence base > Local RCT evidence and present limits"
    revised_locator: "Data, materials, and existing evidence base > 条件性随机对照试验资料的当前状态；Feasibility, resources, risks, alternatives, and stop conditions > 可行性与资源"
    semantic_status: preserved
    evidence: >-
      EXIT-SEP 与 XBJ-SCAP 仍只作为 24 个月后条件性次要分析的潜在个体级数据来源。本地材料仍被限定为衍生报告；个体数据授权、原始病例报告表、统计分析计划、随机化、中心、访视时序及生存和住院语义继续标为尚未核验。
  - protected_id: PCR-006
    prior_locator: "Research content and work packages；Research design and methods > Observational target, anchoring and abstention；Absolute simulation and semi-synthetic recovery gate；Hospital-primary genuine cross-database validation"
    revised_locator: "Research content and work packages；Research design and methods > 双数据库可观测性审计与变量角色；观察性估计目标、临床锚定与证据不足时的处理；已知生成机制下的模拟重建性能与错误结构判定；以医院为主要分组单位的跨数据库检验"
    semantic_status: preserved
    evidence: >-
      资源与可观测性审计、标签和状态及医院分组锁定、简单基线、绝对模拟重建与错误结构判定、至多一个复杂候选模型、两项主要任务与两项次要诊断、开发锁定、未触碰的跨数据库检验和条件性试验分析仍按同一依赖顺序出现。生理状态、治疗行动和检测记录过程继续分离。20 个随机种子对齐率 90%、自助法保留率 80%、跨数据库方向一致率 80%、状态对齐 0.70 和区间校准等判定及其删除、合并或限制解释后果均未改变，预测表现仍不能豁免失败。
  - protected_id: PCR-007
    prior_locator: "Research content and work packages > Conjunctive minimum success definition；Research design and methods > Hospital-primary genuine cross-database validation"
    revised_locator: "Research content and work packages > 主体研究的合取成功定义；Research design and methods > 以医院为主要分组单位的跨数据库检验"
    semantic_status: preserved
    evidence: >-
      主体成功仍须同时满足双数据库支持、模拟重建、两项主要任务的概率评分与校准、泄漏清零，以及不更新任何模型参数时的最终跨数据库表现、状态对齐和结构稳定性。适配医院集中的有限参数调整仍须分开报告且不能替代主要外部检验失败，24 个月后的试验分析也不能补足主体失败。
  - protected_id: PCR-008
    prior_locator: "Research design and methods > Protocol locks for the two primary clinical tasks；Mutually exclusive post-onset state/event system"
    revised_locator: "Research design and methods > 两项主要临床任务的预先锁定规范；发病后互斥状态与事件"
    semantic_status: preserved
    evidence: >-
      两项主要任务、临床事件与信息可用时刻、首次发病风险集、延迟进入、互斥状态、竞争终止、当时可见特征、概率评分与校准目标及患者和医院聚类均保留。标本与抗菌药的 72 小时和 24 小时配对、基线 SOFA、滚动 24 小时成分、首次可排序发病时刻、一次住院总权重为 1、同一时间段的行动与下一状态顺序，以及同时间戳无法排序时排除相应转移均保持原义；泄漏审计仍覆盖同段治疗、未来测量频率、重复住院和结局驱动的变量、时间网格或阈值。
  - protected_id: PCR-009
    prior_locator: "Structured abstract；Contribution, innovation, impact, application, and closest-work comparison > Contribution and evidence ladder"
    revised_locator: "Structured abstract；Contribution, innovation, impact, application, and closest-work comparison > 正向计划贡献及其证据范围；代表性相近工作比较"
    semantic_status: preserved
    evidence: >-
      修订稿继续把模型、模拟重建、主要任务、跨数据库检验和试验新分析写成计划产物，而非已有结果。贡献强度仍限于条件性的整合、验证和基准资源价值；单项模块已有先例，完整组合缺口仍只有低至中等置信度，且不主张新算法或全球首次。
  - protected_id: PCR-010
    prior_locator: "Feasibility, resources, risks, alternatives, and stop conditions；Research design and methods；Expected outputs, falsification criteria, and interpretations"
    revised_locator: "Feasibility, resources, risks, alternatives, and stop conditions > 可行性与资源；Working assumptions（待确认规格）；限制与边界条件；运行风险、替代与后果；Research design and methods；Expected outputs, falsification criteria, and interpretations"
    semantic_status: preserved
    evidence: >-
      资源和访问、团队承诺、数据支持、标签与时间、状态及结构可识别范围、非随机缺失和低治疗支持、跨数据库可迁移性、试验数据与访视分析、临床应用及相近工作不确定性在第 14 节形成一次完整限制集合；临床尺度到模拟参数的映射、多类别校准估计量和登记格式继续标为待确认规格，最低事件或参数计数仍不能替代有效支持与模拟稳定性。设计资格、互斥试验分析、失败后的替代或停止后果保留在相应方法小节，结果证伪与结果依赖解释保留在第 11 节；两试验方向不一致或区间过宽时仍只能报告无支持或跨场景适用性有限，且不得用亚组改变主要解释。
  - protected_id: PCR-011
    prior_locator: "Research content and work packages > Twenty-four-month minimum and dated gates；Identity and final stop boundary"
    revised_locator: "Title and summary；Structured abstract；Primary research question；Objectives；工作包及依赖关系 > WP5；Data, materials, and existing evidence base；Research design and methods > 满足预设条件后的随机对照试验访视次要分析；Key techniques and implementation；Evidence chains；Required analyses and evidence；计划产物；正向计划贡献及其证据范围；Title and positioning claim-support table；Feasibility, resources, risks, alternatives, and stop conditions"
    semantic_status: preserved
    evidence: >-
      试验分析仍位于 24 个月最低交付之外，共享前提仍是主体研究合取成功、相应个体数据授权和核心试验语义可核验。方法权威位置先列共享前提，再并列观测映射分析与独立临床状态分析：共同锚点或映射不合格不阻断语义合格时的独立分析，核心语义不合格则停止新访视结局。标题、摘要、问题、目标、工作包、数据状态、实现接口、证据链、所需分析、计划产物、贡献和主张表均只保留各自所需的高层功能，且后续试验结果不能补足主体研究失败。
  - protected_id: PCR-012
    prior_locator: "Research question, objectives, and core hypothesis > Core hypothesis and non-hypotheses；Feasibility, resources, risks, alternatives, and stop conditions"
    revised_locator: "Feasibility, resources, risks, alternatives, and stop conditions > 限制与边界条件；Research design and methods 中与相邻估计目标直接相连的最小边界"
    semantic_status: preserved
    evidence: >-
      第 14 节一次性保留完整禁止主张范围：观察性数据和预测表现不支持治疗因果效应、真实反馈网络、反事实策略、机制、中介或控制；试验访视差异不验证未测潜在动力学、转移关系或整个候选表征；当前计划也不是已验证模型、临床决策工具、药物平台、数字孪生、可控系统或无条件临床推广依据。其他位置只在估计目标和分支解释需要时保留局部边界。
undeclared_scientific_changes: []
findings: []
unresolved_issues: []
---

# Content-preservation check

## Decision rationale

独立逐项比较显示，冻结登记中的 12 项保护内容在 v044 中均可定位，研究身份、对象、证据状态、数值与时间规则、分析分支、失败后果、主张强度和不支持主张范围保持不变。修订增删均属于定义、移动、拆分、合并、重排、桥接和重复内容集中等已许可编辑操作；修订差异未声明科学变更，实际比较也未发现新增数据、方法、结果或证据，未发现主张增强、限制减弱或把计划工作写成已完成的情况。

## Protected-content trace

主要非逐字变化是权威位置的集中：背景按问题链拆分；两项主要任务、模拟重建和跨数据库判定集中在方法小节；条件性试验分析的共享前提、观测映射分支、独立临床状态分支和停止条件集中在同一方法权威位置；资源状态、待确认规格、完整限制和非方法型运行风险集中在第 14 节；结果证伪与结果依赖解释集中在第 11 节。证据链、实现接口和其他强制章节只保留各自功能所需的投影，没有改变完整技术规则的权威含义。

## Required routing

保护内容核验通过。v044 可进入全新的叙事评估和学术语言评估，无须返回科学评审。
