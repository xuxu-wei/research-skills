---
schema_version: research-idea-content-preservation-check.v1
check_id: content-preservation-r015
review_id: content-preservation-r015
reviewer_skill: idea-narrative-assessor
reviewer_instance_id: fresh-scientific-content-preservation-r015
workflow_id: RID-SEPSIS-CSM-20260717-001
round_id: one-pass-current-r015
input_artifact_ids:
  - idea-dossier-I01-001-v003
  - idea-dossier-I01-001-v006
  - protected-content-register-I01-001-v003
  - revision-delta-I01-001-v003-to-v006
input_versions:
  - v003
  - v006
  - v003
  - v006
inputs:
  prior_dossier:
    artifact_id: idea-dossier-I01-001-v003
    version: v003
    path: tests/idea-test-0.9.0-preview.1/0.9.0-preview.1/03_ideas/nodes/I01-001/dossiers/idea-dossier-v003.md
  revised_dossier:
    artifact_id: idea-dossier-I01-001-v006
    version: v006
    path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/revised/idea-dossier-v006.md
  protected_content_register:
    artifact_id: protected-content-register-I01-001-v003
    version: v003
    path: tests/idea-narrative-forward-0.9.0-preview.3/run-001/inputs/protected-content-register.yaml
  revision_delta:
    artifact_id: revision-delta-I01-001-v003-to-v006
    version: v006
    path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/revised/revision-delta-v003-to-v006.md
files_read:
  - tests/idea-test-0.9.0-preview.1/0.9.0-preview.1/03_ideas/nodes/I01-001/dossiers/idea-dossier-v003.md
  - tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/revised/idea-dossier-v006.md
  - tests/idea-narrative-forward-0.9.0-preview.3/run-001/inputs/protected-content-register.yaml
  - tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/revised/revision-delta-v003-to-v006.md
isolation_mode: fresh_subagent
prior_scores_visible: false
source_edits_performed: false
decision: scientific_content_preserved
protected_item_checks:
  - protected_id: PCR-001
    prior_locator: "YAML frontmatter identity_anchor; Research question, objectives, and core hypothesis > Primary research question"
    revised_locator: "YAML frontmatter identity_anchor; Title, summary, audience, and positioning; Research question, objectives, and core hypothesis > 主要研究问题"
    semantic_status: preserved
    evidence: "v006 保留以脓毒症为中心、从发病前在险时段到首次发病、发病后状态演化及结局的候选动态系统表征；主要问题继续要求状态与受限结构的跨医院、跨数据库检验，未改写为普通临床预测或泛 ICU 风险分层。"
  - protected_id: PCR-002
    prior_locator: "YAML frontmatter identity_anchor.primary_objective; Research question, objectives, and core hypothesis > Objectives"
    revised_locator: "YAML frontmatter identity_anchor.primary_objective; Structured abstract > Objective and hypothesis; Research content and work packages"
    semantic_status: preserved
    evidence: "v006 仍以 24 个月完成阶段 I–II 为主要范围，按知识约束、公共 ICU 数据、系统辨识与独立数据库检验形成连续、可审计的科学证据，并把基准、研究资源和论文所需证据置于预测工具之外；未将主要交付缩减为单一预测器。"
  - protected_id: PCR-003
    prior_locator: "YAML frontmatter identity_anchor.study_object and primary_unit_of_inference; Research design and methods"
    revised_locator: "YAML frontmatter identity_anchor.study_object and primary_unit_of_inference; Research question, objectives, and core hypothesis; Research design and methods > 两项主要临床任务的预定协议"
    semantic_status: preserved
    evidence: "v006 的研究对象仍是纵向、脓毒症中心的 ICU 患者系统，包含可比较的未发病在险片段和发病后轨迹；发病前 landmark、发病后状态占用与转移均继续以患者—时间状态及状态转移为推断单位，并保留患者和医院聚类不确定性。"
  - protected_id: PCR-004
    prior_locator: "Data, materials, and existing evidence base > Current verified-resource versus prospective-gate status; Public ICU database roles and G1 audit"
    revised_locator: "Data, materials, and existing evidence base > 资源状态表、数据库角色与审计字段; Feasibility, resources, risks, alternatives, and stop conditions > 可行性与资源"
    semantic_status: preserved
    evidence: "文献与专家先验、MIMIC-IV 和 eICU-CRD 的核心角色以及 HiRID 或 AmsterdamUMCdb 的预指定备份角色均保留。v006 只把数据库存在与版本列为已核验；访问凭证、数据使用协议、提取与校验和、项目风险集支持、具名人员和模型结果仍分别为尚未核验或尚未生成。"
  - protected_id: PCR-005
    prior_locator: "Data, materials, and existing evidence base > Local RCT evidence and present limits"
    revised_locator: "Data, materials, and existing evidence base > 资源状态表及 EXIT-SEP/XBJ-SCAP 段落; Feasibility, resources, risks, alternatives, and stop conditions > 限制与边界条件"
    semantic_status: preserved
    evidence: "v006 继续把 EXIT-SEP 与 XBJ-SCAP 限定为 24 个月之后的条件性个体级试验数据来源；本地材料仍只是衍生清洗和验证报告，明确不能替代个体数据授权、原始 CRF/SAP、随机化、中心、实际访视及生存、住院、出院语义核验。"
  - protected_id: PCR-006
    prior_locator: "Research content and work packages; Research design and methods"
    revised_locator: "Research content and work packages > 时间表、工作包与最低顺序; Research design and methods > 变量角色、模拟恢复、外部验证与条件性试验分析"
    semantic_status: preserved
    evidence: "v006 保留资源与可观测性审计、标签/状态/医院拆分、简单基线、模拟恢复、至多一个复杂候选、两项主要任务和两项次要诊断、开发冻结、独立保留数据库检验及条件性试验分析的固定顺序。患者状态、治疗行动与测量过程仍分离，解释仍受锚定、对齐、可恢复性、跨数据库稳定性和弃权规则限制。"
  - protected_id: PCR-007
    prior_locator: "Research content and work packages > Conjunctive minimum success definition; Research design and methods > Hospital-primary genuine cross-database validation"
    revised_locator: "Research content and work packages > 阶段 II 合取成功定义; Research design and methods > 医院优先的跨数据库外部验证"
    semantic_status: preserved
    evidence: "v006 的阶段 II 成功仍要求两库数据支持、正确/零边/错设场景的绝对阈值、两项主要任务的 proper score 与校准、无高严重度泄漏、独立保留测试中的不更新参数表现、状态对齐和结构符号稳定同时成立。仅用适配集的校准或观测模型更新与主要验证分开，不能替代其失败；阶段 III 不计入合取成功。"
  - protected_id: PCR-008
    prior_locator: "Research design and methods > Protocol locks for the two primary clinical tasks; Mutually exclusive post-onset state/event system"
    revised_locator: "Research design and methods > 两项主要临床任务的预定协议; 发病后互斥状态"
    semantic_status: preserved
    evidence: "两项主要任务、事件与信息可用双时钟、首次发病风险集、延迟进入、互斥发病后状态、竞争终止、as-of 特征顺序、Brier/proper-score 与校准目标、患者和医院聚类以及跨拆分和未来信息泄漏防护均保留。关键数值条件也未改变，包括 12 小时网格与预测期、病程第 7 日、非劣界 +0.01、校准斜率 0.80–1.20 和绝对风险误差≤0.02。"
  - protected_id: PCR-009
    prior_locator: "Structured abstract; Contribution, innovation, impact, application, and closest-work comparison > Contribution and evidence ladder"
    revised_locator: "Structured abstract; Contribution, innovation, impact, application, and closest-work comparison; Title and positioning claim-support table"
    semantic_status: preserved
    evidence: "v006 始终以计划时态描述候选表征、模拟、外部验证和试验分析，并明确模型、恢复、预测、外部测试及新试验结果尚未生成。贡献仍限于条件性的证据整合、验证、基准和研究资源；单项模块已有先例，完整组合缺口仅为低至中等置信，不主张新算法或全球首次。"
  - protected_id: PCR-010
    prior_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Resources and governance; Risk and automatic alternative matrix; Remaining execution gates; Identity and final stop boundary"
    revised_locator: "Feasibility, resources, risks, alternatives, and stop conditions > 可行性与资源; 工作假设与尚待冻结的规范; 限制与边界条件; 风险、替代方案与停止条件"
    semantic_status: preserved
    evidence: "v006 在第 14 节集中保留全部未解决可行性问题：访问与人员承诺、G1 支持、标签和泄漏、模拟可恢复性、非随机缺失与行动重叠、外部可迁移性、时间节点、试验授权与资料语义、共同锚点和观测桥接、最接近工作不确定性。每类风险均保留触发条件、预设替代方案以及停止或缩小主张的后果；这些问题没有被写成已经解决。"
  - protected_id: PCR-011
    prior_locator: "Research content and work packages > Twenty-four-month minimum and dated gates; Identity and final stop boundary"
    revised_locator: "Research content and work packages > 时间表; Feasibility, resources, risks, alternatives, and stop conditions > 第 14 节末最终边界"
    semantic_status: preserved
    evidence: "v006 继续规定阶段 I–II 在 24 个月内完成，阶段 III 位于最低交付之外，并仅在阶段 II 合取成功及相应试验数据、资料语义和观测桥接达到预设条件时开展。后续试验结果仍不能改变阶段 II 失败，也不能绕过资源、模拟恢复、主要任务或独立外部验证要求。"
  - protected_id: PCR-012
    prior_locator: "Research question, objectives, and core hypothesis > Core hypothesis and non-hypotheses; Feasibility, resources, risks, alternatives, and stop conditions"
    revised_locator: "Research question, objectives, and core hypothesis > 核心假设; Expected outputs, falsification criteria, and interpretations; Feasibility, resources, risks, alternatives, and stop conditions > 限制与边界条件"
    semantic_status: preserved
    evidence: "v006 明确保留观察性数据与预测表现不能识别真实因果网络、治疗因果效应、反事实策略、机制、中介或控制的边界；试验次要分析也不验证未测潜在动力学、转移边、观测模型之外的结构或整个系统。当前计划仍被排除为已验证模型、临床决策工具、数字孪生、可控系统、药物平台或无条件临床推广依据。"
undeclared_scientific_changes: []
findings: []
unresolved_issues: []
---

# Content-preservation check

## Decision rationale

v006 对 v003 的改动属于结构重排、术语定义、重复内容集中和自然语言替换。研究身份、核心问题与目的、研究对象和推断单位没有漂移；主要方法顺序、任务定义、阈值、条件分支、停止条件及主张强度均保持不变。修订 delta 声明仅作叙事与语言修复，逐项检查未发现与该声明不一致的科学变更。

全部 12 个保护项均可在 v006 中追踪到等义且同强度的内容。数据库与试验资源状态仍区分已核验、尚未核验和尚未生成；第 14 节继续把未解决的可行性问题、风险触发条件、替代方案和停止后果作为权威表述。计划性验证没有被写成已完成结果，观察性与试验分析的不支持主张边界也未被削弱。

## Protected-content trace

主要移动发生在限制和可行性内容：v003 分散于工作包、方法、证据链和预期结果中的重复限制，在 v006 集中至第 14 节；相邻章节只保留推进相应设计所需的局部限定。两项主要任务的协议、互斥状态、模拟恢复绝对阈值、医院优先的独立外部验证及条件性试验观测桥接仍在方法部分完整保留。

试验层将“投影可观测摘要的有限扰动”统一表述为随机分配组在实际访视一维可观测状态摘要上的有限差异，并继续要求资料语义、共同锚点、冻结映射和全部忠实度阈值先行合格；不合格时仍转为与阶段 II 独立的死亡优先排序 SOFA 复合状态端点。该术语替换没有扩大估计对象或因果解释。

## Required routing

科学内容已保全；v006 可进入新的叙事与语言评估，无需返回科学评审。
