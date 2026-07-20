---
schema_version: research-idea-content-preservation-check.v1
check_id: content-preservation-I01-001-r040
review_id: content-preservation-review-I01-001-r040
reviewer_skill: idea-narrative-assessor
reviewer_instance_id: fresh-content-preservation-r040
workflow_id: RID-SEPSIS-CSM-20260717-001
round_id: r040
input_artifact_ids:
  - idea-dossier-I01-001-v003
  - idea-dossier-I01-001-v028
  - protected-content-register-I01-001-v003-r003
  - revision-delta-I01-001-v003-to-v028
input_versions:
  - v003
  - v028
  - r003
  - v028
inputs:
  prior_dossier:
    artifact_id: idea-dossier-I01-001-v003
    version: v003
    path: tests/idea-test-0.9.0-preview.1/0.9.0-preview.1/03_ideas/nodes/I01-001/dossiers/idea-dossier-v003.md
  revised_dossier:
    artifact_id: idea-dossier-I01-001-v028
    version: v028
    path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/accepted-v4/idea-dossier-v028.md
  protected_content_register:
    artifact_id: protected-content-register-I01-001-v003-r003
    version: r003
    path: tests/idea-narrative-forward-0.9.0-preview.3/run-001/inputs/protected-content-register-v003.yaml
  revision_delta:
    artifact_id: revision-delta-I01-001-v003-to-v028
    version: v028
    path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/accepted-v4/revision-delta-v003-to-v028.md
files_read:
  - tests/idea-test-0.9.0-preview.1/0.9.0-preview.1/03_ideas/nodes/I01-001/dossiers/idea-dossier-v003.md
  - tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/accepted-v4/idea-dossier-v028.md
  - tests/idea-narrative-forward-0.9.0-preview.3/run-001/inputs/protected-content-register-v003.yaml
  - tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/accepted-v4/revision-delta-v003-to-v028.md
scope:
  mode: content_preservation
  compared:
    - scientific_content
    - evidence_and_resource_status
    - claim_scope_and_strength
  excluded:
    - narrative_quality
    - language_quality
    - scientific_merit
isolation_mode: fresh_subagent
prior_scores_visible: false
source_edits_performed: false
decision: scientific_content_preserved
protected_item_checks:
  - protected_id: PCR-001
    prior_locator: "YAML frontmatter identity_anchor; Research question, objectives, and core hypothesis > Primary research question"
    revised_locator: "YAML frontmatter identity_anchor; Title, summary, audience, and positioning > Positioning and contribution frame; Research question, objectives, and core hypothesis > Primary research question"
    semantic_status: preserved
    evidence: >-
      v028 原样保留研究问题、研究对象、核心证据基础和患者—时间状态及状态转移推断单位。正文仍覆盖发病前在险时段、首次发病、发病后互斥状态演化和结局，并明确核心科学问题不是普通临床预测或泛 ICU 风险分层。
  - protected_id: PCR-002
    prior_locator: "YAML frontmatter identity_anchor.primary_objective; Research question, objectives, and core hypothesis > Objectives"
    revised_locator: "YAML frontmatter identity_anchor.primary_objective; Title, summary, audience, and positioning > One-sentence complete-Idea summary and Positioning and contribution frame; Research content and work packages > Twenty-four-month programme"
    semantic_status: preserved
    evidence: >-
      v028 保留在 24 个月内完成阶段 I–II 的主要目标，并继续以文献与专家知识约束候选结构、以两个公共 ICU 数据库开展系统辨识和跨数据库验证。交付仍定位为高水平论文与可审查科学证据，而非仅产出预测工具。
  - protected_id: PCR-003
    prior_locator: "YAML frontmatter identity_anchor.study_object and primary_unit_of_inference; Research design and methods"
    revised_locator: "YAML frontmatter identity_anchor.study_object and primary_unit_of_inference; Research question, objectives, and core hypothesis > Primary research question; Research design and methods > Protocol specifications for the two primary clinical tasks"
    semantic_status: preserved
    evidence: >-
      v028 明确研究对象仍是纵向、以脓毒症为中心的 ICU 患者系统，包括可比较的未发病在险时段和发病后轨迹；主要推断单位仍是尊重患者与医院聚类的患者—时间状态及状态转移。
  - protected_id: PCR-004
    prior_locator: "Data, materials, and existing evidence base > Current verified-resource versus prospective-gate status; Public ICU database roles and G1 audit"
    revised_locator: "Data, materials, and existing evidence base > Current resource and evidence status; Public ICU database roles and observability audit; Feasibility, resources, risks, alternatives, and stop conditions > Feasibility and resources"
    semantic_status: preserved
    evidence: >-
      MIMIC-IV v3.1 与 eICU-CRD v2.0 仍为两个主数据库，HiRID 或 AmsterdamUMCdb 仍须预先指定并经同等审计后才能作为备份。v028 只把数据库存在与版本列为已核实；团队访问、数据使用协议、可运行提取、项目队列支持和具名人员仍为尚未核实，模型与分析结果仍为尚未生成。
  - protected_id: PCR-005
    prior_locator: "Data, materials, and existing evidence base > Local RCT evidence and present limits"
    revised_locator: "Data, materials, and existing evidence base > Current resource and evidence status and Local RCT evidence; Feasibility, resources, risks, alternatives, and stop conditions > Limitations and boundary conditions, item 6"
    semantic_status: preserved
    evidence: >-
      EXIT-SEP 与 XBJ-SCAP 仍仅是条件性阶段 III 的潜在个体级数据来源。v028 保留现有本地材料仅为衍生清洗或验证报告的状态，并明确其不能替代个体数据授权、原始 CRF、SAP、随机化、中心、访视时序及死亡、住院、出院和转院语义核验。
  - protected_id: PCR-006
    prior_locator: "Research content and work packages; Research design and methods, including Observational target, anchoring, missingness and abstention"
    revised_locator: "Research content and work packages > Twenty-four-month programme, Work packages, and minimum analysis sequence; Data, materials, and existing evidence base > Prespecified variable roles; Research design and methods > Observational target, anchoring and abstention, Absolute simulation and semi-synthetic recovery, and Hospital-based cross-database validation"
    semantic_status: preserved
    evidence: >-
      v028 保留资源与观测支持审计、标签/状态/医院划分、简单基线、绝对模拟恢复、至多一个复杂候选、两项主要任务与两项次要诊断、确定开发结果和外部最终测试的顺序，RCT 分析仍置于阶段 II 之后。Y_t、A_t、M_t、标签与基线协变量继续分开。对齐率 90%、bootstrap 保留率 80%、外部符号一致率 80%、状态对齐 0.70 及区间校准判定均未改变；恢复、转移、边检测、零边、错设和概率校准的数值标准也保持不变。
  - protected_id: PCR-007
    prior_locator: "Research content and work packages > Conjunctive minimum success definition; Research design and methods > Hospital-primary genuine cross-database validation"
    revised_locator: "Research content and work packages > Conjunctive stage-II success definition; Research design and methods > Hospital-based cross-database validation; Feasibility, resources, risks, alternatives, and stop conditions > Limitations and boundary conditions, item 5"
    semantic_status: preserved
    evidence: >-
      v028 仍把双数据库支持、绝对恢复、两项主要任务的概率评分与校准、泄漏清零、不更新参数的外部验证、状态对齐和结构符号一致性作为阶段 II 的合取证据。Brier 非劣性上界 +0.01、校准斜率 0.80–1.20、绝对风险误差 0.02、至少 20 个外部测试医院、状态对齐 0.70 和符号一致率 0.80 均保留；适配集重新校准或仅更新观测模型仍不得替代主要外部验证未达标。
  - protected_id: PCR-008
    prior_locator: "Research design and methods > Protocol locks for the two primary clinical tasks; Mutually exclusive post-onset state/event system"
    revised_locator: "Research design and methods > Protocol specifications for the two primary clinical tasks; Mutually exclusive post-onset state and event system; Data, materials, and existing evidence base > Prespecified variable roles"
    semantic_status: preserved
    evidence: >-
      v028 保留两项主要任务和事件/信息可用双时钟。标本先采集时给药须在后 72 小时内、给药先发生时采集须在后 24 小时内；基线 SOFA、滚动 24 小时最差成分、感染前 48 小时至后 24 小时窗口和首次可排序发病时刻均未改变。ICU 第 12 小时起每 12 小时预测、最多 24 小时且至少 12 小时历史、未来 12 小时首次发病、第 7 日主要时点与第 14 日敏感性、仅首次发病、一次住院总权重为 1、同时间格排序、互斥状态优先级、患者与医院 bootstrap 以及逐项泄漏检查均保持不变。
  - protected_id: PCR-009
    prior_locator: "Structured abstract; Contribution, innovation, impact, application, and closest-work comparison > Contribution and evidence ladder"
    revised_locator: "Structured abstract > Expected result and Contribution and impact; Data, materials, and existing evidence base > Current resource and evidence status; Contribution, innovation, impact, application, and closest-work comparison > Contribution and evidence progression and Representative related research comparison"
    semantic_status: preserved
    evidence: >-
      v028 明确所有模型、模拟恢复、预测、外部测试和 RCT 新分析均为计划或尚未生成。贡献仍限于条件性的证据整合、验证和可复用基准资源；各单项模块已有先例，完整组合缺口仍仅为低至中等置信，并未新增新算法或全球首次主张。
  - protected_id: PCR-010
    prior_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Resources and governance; Risk and automatic alternative matrix; Remaining execution gates; Identity and final stop boundary; Expected outputs, falsification criteria, and interpretations > Falsification and stop criteria"
    revised_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Feasibility and resources, Working assumptions, Limitations and boundary conditions, and Risks, alternatives, and stop conditions"
    semantic_status: preserved
    evidence: >-
      v028 在统一位置保留资源与人员、双数据库支持、标签与泄漏、状态可识别性、非随机缺失与低重叠、主要外部验证、时间进度、试验授权与语义、共同锚点和映射以及文献定位等限制，并为相应失败给出预设替代或停止后果。临床尺度到模拟参数的映射、多类别校准估计量与置信界仍明确为待登记事项，事件或参数下限仍不能替代经验有效样本量和模拟稳定性。两试验方向不一致或区间过宽时仍须分别报告无支持或跨场景适用性有限，不得合并效应或用事后亚组改变结论。
  - protected_id: PCR-011
    prior_locator: "Research content and work packages > Twenty-four-month minimum and dated gates; Feasibility, resources, risks, alternatives, and stop conditions > Identity and final stop boundary"
    revised_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Feasibility and resources; Risks, alternatives, and stop conditions > time progress and RCT rows"
    semantic_status: preserved
    evidence: >-
      v028 明确保留阶段 I–II 必须在 24 个月内完成、阶段 III 位于最低交付之外的边界。阶段 III 仍以阶段 II 合取证据、个体数据授权、原始语义和实际访视指标为前提，任何 RCT 结果均不能补足阶段 II 的资源、模拟恢复、主要任务或外部验证缺口。
  - protected_id: PCR-012
    prior_locator: "Research question, objectives, and core hypothesis > Core hypothesis and non-hypotheses; Feasibility, resources, risks, alternatives, and stop conditions"
    revised_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Limitations and boundary conditions, item 9"
    semantic_status: preserved
    evidence: >-
      v028 仍明确观察性数据和预测表现不支持真实因果网络、治疗因果效应、反事实策略、机制、中介、控制或数字孪生主张；条件性 RCT 次要分析不能验证未测潜在动力学、转移边或整个阶段 II 系统模型。当前计划仍不得表述为已验证模型、临床决策工具、药物平台或无条件临床推广依据。
undeclared_scientific_changes: []
findings: []
unresolved_issues: []
---

# Content-preservation check

## Decision rationale

`scientific_content_preserved`。对 frozen register 的 12 项保护内容逐项比较后，v028 的研究身份、目标、对象、推断单位、数据与证据状态、设计顺序、定量和时间规则、分析分支、限制、停止条件及主张强度均与 v003 保持一致。修订仅改变表述、定义顺序、章节组织和重复内容的位置；revision delta 未声明科学变更，正文比对也未发现未声明的科学变更。

## Protected-content trace

- 研究身份和主要推断单位同时保留在 YAML `identity_anchor` 与主要研究问题中。
- 两项主要任务的双时钟、风险集、互斥状态、校准与概率评分目标、聚类不确定性和泄漏防护仍位于研究设计部分；全部关键数值与时间规则可直接定位。
- 阶段 II 的合取成功定义与三类外部分析角色仍分开表述，适配后的结果不能替代不更新参数的外部验证。
- 资源、证据和结果状态仍区分为已核实、尚未核实和尚未生成；没有把计划性工作写成完成结果。
- 全局限制、未决假设、替代方案和停止后果集中到 `Feasibility, resources, risks, alternatives, and stop conditions`，不支持的主张类别集中到其 `Limitations and boundary conditions` 第 9 项，语义和强度未变。

## Required routing

该 dossier 可进入新的独立叙事与学术语言评估。后续评估不得沿用本次核验结论作为质量评分，也不得据此推定科学设计本身正确。
