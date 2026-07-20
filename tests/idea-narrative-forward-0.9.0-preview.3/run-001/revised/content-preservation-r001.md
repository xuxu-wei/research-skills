---
schema_version: research-idea-content-preservation-check.v1
check_id: content-preservation-check-I01-001-r001
review_id: content-preservation-review-I01-001-r001
reviewer_skill: idea-narrative-assessor
reviewer_instance_id: fresh-content-preservation-I01-001-r001
workflow_id: RID-SEPSIS-CSM-20260717-001
round_id: r001
input_artifact_ids:
  - idea-dossier-I01-001-v003
  - idea-dossier-I01-001-v004
  - protected-content-register-I01-001-v003
  - revision-delta-I01-001-v003-to-v004
input_versions:
  - v003
  - v004
  - v003
  - v001
inputs:
  prior_dossier:
    artifact_id: idea-dossier-I01-001-v003
    version: v003
    path: tests/idea-test-0.9.0-preview.1/0.9.0-preview.1/03_ideas/nodes/I01-001/dossiers/idea-dossier-v003.md
  revised_dossier:
    artifact_id: idea-dossier-I01-001-v004
    version: v004
    path: tests/idea-narrative-forward-0.9.0-preview.3/run-001/revised/idea-dossier-v004.md
  protected_content_register:
    artifact_id: protected-content-register-I01-001-v003
    version: v003
    path: tests/idea-narrative-forward-0.9.0-preview.3/run-001/inputs/protected-content-register.yaml
  revision_delta:
    artifact_id: revision-delta-I01-001-v003-to-v004
    version: v001
    path: tests/idea-narrative-forward-0.9.0-preview.3/run-001/revised/revision-delta-v003-to-v004.md
files_read:
  - tests/idea-test-0.9.0-preview.1/0.9.0-preview.1/03_ideas/nodes/I01-001/dossiers/idea-dossier-v003.md
  - tests/idea-narrative-forward-0.9.0-preview.3/run-001/revised/idea-dossier-v004.md
  - tests/idea-narrative-forward-0.9.0-preview.3/run-001/inputs/protected-content-register.yaml
  - tests/idea-narrative-forward-0.9.0-preview.3/run-001/revised/revision-delta-v003-to-v004.md
isolation_mode: fresh_subagent
prior_scores_visible: false
source_edits_performed: false
decision: scientific_content_preserved
protected_item_checks:
  - protected_id: PCR-001
    prior_locator:
      section_heading: "YAML frontmatter identity_anchor; Research question, objectives, and core hypothesis"
      subsection_heading: "Primary research question"
      content_anchor: "sepsis-centered pre-onset, onset, post-onset, and outcome continuum"
    revised_locator:
      section_heading: "YAML frontmatter identity_anchor; Research question, objectives, and core hypothesis; Feasibility, resources, risks, alternatives, and stop conditions"
      subsection_heading: "Primary research question; Research identity and final boundary"
      content_anchor: "发病前—首次发病—发病后—结局连续体；普通临床预测将被重新界定为另一项研究"
    semantic_status: preserved
    evidence: >-
      v003 与 v004 的 identity_anchor.primary_research_question、primary_objective、study_object 和
      primary_unit_of_inference 逐字相同。v004 的主要研究问题仍覆盖发病前、首次发病、发病后和结局，
      并以患者—时间状态、状态转移及跨数据库稳定性为中心；第 14 节明确把改成普通临床预测列为另一项研究，
      因而没有把研究身份收窄为一般风险分层或单一预测任务。
  - protected_id: PCR-002
    prior_locator:
      section_heading: "YAML frontmatter identity_anchor; Research question, objectives, and core hypothesis; Research content and work packages"
      subsection_heading: "Objectives; Twenty-four-month minimum and dated gates"
      content_anchor: "construct and validate the sepsis complex-system model, with stage II completed within 24 months"
    revised_locator:
      section_heading: "Structured abstract; Research question, objectives, and core hypothesis; Research content and work packages"
      subsection_heading: "Objective and hypothesis; Objectives; Twenty-four-month minimum and dated gates"
      content_anchor: "24 个月内完成阶段 I–II；双数据库审计、模型恢复和跨数据库验证"
    semantic_status: preserved
    evidence: >-
      v003 将 24 个月内完成阶段 I–II 的构建、系统辨识和跨数据库检验作为主要目标。
      v004 继续以文献与专家知识约束模型，在 24 个月内完成双数据库审计、模型构建与恢复检验、
      两项主要任务和跨数据库验证；结构化摘要及贡献部分把交付表述为可审计证据路线、研究基准和可复用资源，
      没有把目标改成仅产出预测工具。论文传播形式的简化没有改变该科学目标或交付证据范围。
  - protected_id: PCR-003
    prior_locator:
      section_heading: "YAML frontmatter identity_anchor; Research design and methods"
      subsection_heading: "Protocol locks for the two primary clinical tasks; Observational target, anchoring and abstention"
      content_anchor: "patient-time state and state transition, with patient and hospital clustering respected"
    revised_locator:
      section_heading: "YAML frontmatter identity_anchor; Research question, objectives, and core hypothesis; Research design and methods"
      subsection_heading: "Primary research question; Protocol locks for the two primary clinical tasks; Observational model target, anchoring, and reporting"
      content_anchor: "纵向、以脓毒症为中心的 ICU 患者系统；患者—时间状态及状态转移；患者和医院聚类"
    semantic_status: preserved
    evidence: >-
      v004 frontmatter 原样保留纵向脓毒症 ICU 患者系统、可比较的未发病在险时段和发病后轨迹，
      主要研究问题继续以患者—时间状态和状态转移为对象。两项任务的风险集覆盖未发病时段、首次发病、
      延迟进入和发病后轨迹，不确定性仍按患者和医院层级处理，推断单位及聚类边界均未改变。
  - protected_id: PCR-004
    prior_locator:
      section_heading: "Data, materials, and existing evidence base"
      subsection_heading: "Current verified-resource versus prospective-gate status; Public ICU database roles and G1 audit"
      content_anchor: "数据库存在与版本已核验；访问、DUA、可运行提取、队列支持、人员与结果未核验或未生成"
    revised_locator:
      section_heading: "Data, materials, and existing evidence base; Feasibility, resources, risks, alternatives, and stop conditions"
      subsection_heading: "Public ICU databases and planned roles; Current feasibility and evidence status"
      content_anchor: "双数据库审计将在模型拟合前生成；访问与人员未核验，项目计数和结果尚未生成"
    semantic_status: preserved
    evidence: >-
      v003 只核验 MIMIC-IV 与 eICU-CRD 的存在和版本，明确团队访问凭证、数据使用协议、提取、
      项目队列支持、具名人员及模型结果未核验或未生成。v004 第 6 节仍将双数据库审计写为模型拟合前的未来工作，
      各审计字段均标为“待审计”；第 14 节逐项保留访问与人员“未核验”、项目计数与模型/验证结果“尚未生成”，
      并保留 HiRID 或 AmsterdamUMCdb 的条件性备份角色。一句话摘要中的“本研究计划……经审计”受未来计划语境约束，
      且没有覆盖上述明确状态，因此未把资源或验证写成当前已经具备。
  - protected_id: PCR-005
    prior_locator:
      section_heading: "Data, materials, and existing evidence base"
      subsection_heading: "Local RCT evidence and present limits"
      content_anchor: "EXIT-SEP 与 XBJ-SCAP 本地衍生报告不替代个体数据授权和原始试验语义核验"
    revised_locator:
      section_heading: "Data, materials, and existing evidence base; Feasibility, resources, risks, alternatives, and stop conditions"
      subsection_heading: "Trial data considered for conditional stage III analyses; Current feasibility and evidence status"
      content_anchor: "项目内衍生清洗或验证报告不能替代个体数据授权、原始病例报告表或统计分析计划及试验语义核验"
    semantic_status: preserved
    evidence: >-
      v004 仍只把 EXIT-SEP 与 XBJ-SCAP 作为阶段 III 的条件性个体数据来源，并将现有本地材料称为项目内衍生清洗或验证报告。
      第 14 节明确这些材料不能替代个体数据授权、原始病例报告表或统计分析计划、随机分组、中心、实际访视以及生存和住院语义核验；
      相关失败仍导致停止新状态端点。证据资格和未核验状态与 v003 相同。
  - protected_id: PCR-006
    prior_locator:
      section_heading: "Research content and work packages; Research design and methods"
      subsection_heading: "Work packages and minimum route; Observational target, anchoring and abstention; Hospital-primary genuine cross-database validation"
      content_anchor: "资源审计到条件性试验分析的固定顺序；状态、行动与观测过程分离；解释受恢复、运输和弃权约束"
    revised_locator:
      section_heading: "Research content and work packages; Research design and methods; Feasibility, resources, risks, alternatives, and stop conditions"
      subsection_heading: "Work packages and minimum route; Variable-role separation; Operational thresholds, alternatives, and stop conditions"
      content_anchor: "固定执行顺序；生理测量、治疗行动和测量过程分离；恢复、对齐、外部验证与不报告条件"
    semantic_status: preserved
    evidence: >-
      v004 原顺序保留为资源与可观测性审计、标签/状态/医院分组锁定、简单基线、模拟恢复、至多一个复杂候选、
      两项主要任务和两项次要诊断、开发冻结、跨数据库验证，最后才进入条件性试验映射。
      生理测量、治疗行动和测量过程继续分开；第 14 节完整保留锚定、恢复、错设识别、状态对齐、运输性和不报告或降级条件。
      没有增加新的数据、方法或结果。
  - protected_id: PCR-007
    prior_locator:
      section_heading: "Research content and work packages; Research design and methods"
      subsection_heading: "Conjunctive minimum success definition; Hospital-primary genuine cross-database validation"
      content_anchor: "阶段 II 合取成功；有限更新不能替代零更新失败；阶段 III 不补足阶段 II"
    revised_locator:
      section_heading: "Research content and work packages; Feasibility, resources, risks, alternatives, and stop conditions"
      subsection_heading: "Conjunctive minimum success definition; Scientific and interpretive boundaries; Operational thresholds, alternatives, and stop conditions"
      content_anchor: "五类证据共同构成阶段 II 成功；不更新模型的验证为主要依据；阶段 III 不补足失败"
    semantic_status: preserved
    evidence: >-
      v004 继续把双库数据支持、模拟恢复与错设识别、两项主要任务的适当评分和校准、无高严重度泄漏、
      预先隔离外部数据上的任务表现/状态对齐/结构稳定性规定为合取条件。第 14 节保留 Brier 非劣、校准、
      外部状态对齐和结构符号阈值，并明确再校准或观测层更新不能替代不更新模型的外部验证失败；
      阶段 III 仍不能补足阶段 II 的任何失败。
  - protected_id: PCR-008
    prior_locator:
      section_heading: "Research design and methods"
      subsection_heading: "Protocol locks for the two primary clinical tasks; Mutually exclusive post-onset state/event system"
      content_anchor: "双时钟、首次发病、延迟进入、竞争终止、as-of 信息、校准与聚类约束"
    revised_locator:
      section_heading: "Research design and methods; Feasibility, resources, risks, alternatives, and stop conditions"
      subsection_heading: "Protocol locks for the two primary clinical tasks; Mutually exclusive post-onset state and event system; Operational thresholds, alternatives, and stop conditions"
      content_anchor: "事件时间与信息可用时间、首次发病和延迟进入、互斥状态、竞争事件、评分校准及数据泄漏条件"
    semantic_status: preserved
    evidence: >-
      v004 两项主要任务表逐项保留事件时间与信息可用时间、12 小时动态预测时点、首次发病风险集、
      延迟进入、互斥发病后状态、竞争终止、只使用当时可用信息、Brier/多类别 Brier 与绝对校准目标，
      以及患者和医院层级不确定性。数据泄漏审计及“不解决高严重度问题则不访问外部验证结果”的后果也保留，
      因而这些设计承诺没有因压缩而改变。
  - protected_id: PCR-009
    prior_locator:
      section_heading: "Structured abstract; Contribution, innovation, impact, application, and closest-work comparison"
      subsection_heading: "Expected result; Contribution and evidence ladder; Verified representative closest-work comparison"
      content_anchor: "所有模型、恢复、外部验证和试验分析均为计划；整合与验证增量为条件性且非全球首次"
    revised_locator:
      section_heading: "Structured abstract; Contribution, innovation, impact, application, and closest-work comparison; Feasibility, resources, risks, alternatives, and stop conditions"
      subsection_heading: "Expected result; Contribution and evidence ladder; Representative closest-work comparison; Current feasibility and evidence status"
      content_anchor: "拟生成的结果，不是现有发现；条件性的整合与验证增量；新结果尚未生成"
    semantic_status: preserved
    evidence: >-
      v004 结构化摘要明确候选模型、模拟恢复、外部验证和试验次要分析均为拟生成结果而非现有发现；
      第 14 节再次记录所有相关结果尚未生成。贡献仍限于条件性的证据整合、验证、研究基准和资源增量，
      明确各组成方法已有先例、完整组合缺口仅为低至中等置信，并继续排除新算法或全球首次主张。
  - protected_id: PCR-010
    prior_locator:
      section_heading: "Feasibility, resources, risks, alternatives, and stop conditions"
      subsection_heading: "Resources and governance; Risk and automatic alternative matrix; Remaining execution gates; Identity and final stop boundary"
      content_anchor: "全局资源、可行性、解释限制、替代方案和停止条件"
    revised_locator:
      section_heading: "Feasibility, resources, risks, alternatives, and stop conditions"
      subsection_heading: "Authoritative limitations, feasibility findings, interpretation boundaries, alternatives, and stop conditions"
      content_anchor: "唯一权威位置：当前状态、科学解释边界、资源治理、阈值、替代方案和停止后果"
    semantic_status: preserved
    evidence: >-
      v004 第 14 节建立唯一权威小节，并集中保留资源与访问、具名团队、双数据库支持、标签与数据泄漏、
      状态和结构恢复、非随机缺失与低支持度、外部运输、时间节点、试验数据与语义、共同观测变量与映射、
      最接近工作不确定性。对应表格为每类触发条件给出降级、替代或停止后果；其他章节只保留直接界定相邻设计的最小条件，
      未发现关键限制被删除、弱化或改成无条件表述。
  - protected_id: PCR-011
    prior_locator:
      section_heading: "Research content and work packages; Feasibility, resources, risks, alternatives, and stop conditions"
      subsection_heading: "Twenty-four-month minimum and dated gates; Identity and final stop boundary"
      content_anchor: "阶段 I–II 在 24 个月内完成；阶段 III 位于最低交付之外且不能补足阶段 II"
    revised_locator:
      section_heading: "Research content and work packages; Feasibility, resources, risks, alternatives, and stop conditions"
      subsection_heading: "Twenty-four-month minimum and dated gates; Scientific and interpretive boundaries; Research identity and final boundary"
      content_anchor: "阶段 I–II 构成 24 个月最低交付；阶段 III 安排在其后且永不补足合取失败"
    semantic_status: preserved
    evidence: >-
      v004 明确阶段 I–II 是 24 个月最低交付，阶段 III 位于 24 个月以后，只有阶段 II 成功并满足个体数据、
      试验语义和共同观测映射条件时才可开展。第 11 节和第 14 节均说明随机试验结果不能补强或补足阶段 II 在资源、
      模拟恢复、主要任务或外部验证方面的失败，时间边界和从属关系不变。
  - protected_id: PCR-012
    prior_locator:
      section_heading: "Research question, objectives, and core hypothesis; Feasibility, resources, risks, alternatives, and stop conditions"
      subsection_heading: "Core hypothesis and non-hypotheses; Interpretation matrix"
      content_anchor: "观察性和随机试验证据不支持因果网络、机制、控制、数字孪生或临床应用主张"
    revised_locator:
      section_heading: "Feasibility, resources, risks, alternatives, and stop conditions"
      subsection_heading: "Scientific and interpretive boundaries; Operational thresholds, alternatives, and stop conditions"
      content_anchor: "不识别治疗因果效应、真实反馈网络或反事实策略；不验证潜在动力学、转移边、中介、控制或完整系统"
    semantic_status: preserved
    evidence: >-
      v004 第 14 节明确观察性状态、治疗行动、测量过程关联和预测表现不识别治疗因果效应、真实反馈网络或反事实策略；
      任一随机试验分支也不验证未测潜在动力学、状态转移边、中介机制、个体控制或完整动态系统。
      同处继续排除新算法、全球首次、数字孪生、控制模型、已验证临床决策工具、药物平台和无条件国际推广，
      因而不受支持的主张类别没有被缩减或弱化。
undeclared_scientific_changes: []
findings: []
unresolved_issues: []
---

# Content-preservation check

## Decision rationale

受保护内容注册表中的 12 项内容在 v004 均可追溯，研究身份、科学问题、数据与证据状态、设计顺序、
分析和验证承诺、主张强度、限制、替代方案及停止条件与 v003 保持一致。修订将“候选动态系统表征”
改为定义更明确的“候选动态系统模型”，重排背景与方法说明，并把重复限制集中到第 14 节；这些变化没有
新增数据、方法、结果或证据，也没有把条件性要素改成无条件要素。

修订说明声明本轮没有科学内容、方法、阈值或主张强度变化。逐项比较支持这一声明。特别是，v004 的
双数据库审计仍是模型拟合前的计划步骤，访问、队列支持、人员及模型或验证结果继续标为未核验或尚未生成；
因此摘要中的简写没有改变当前可行性状态。

## Protected-content trace

- 研究名称中的“表征”改为“模型”，但 frontmatter 身份锚点未变，正文也继续把它限定为候选、计划性模型。
- 两项主要临床任务、模拟恢复、跨数据库验证和随机试验观测映射的技术细节仍位于方法部分；数值阈值、
  降级规则和停止后果集中到第 14 节的唯一权威小节。
- 资源现状、随机试验数据资格、最接近工作不确定性及不受支持的因果、机制、控制和临床应用主张均在第 14 节集中保留。
- 不更新模型的外部验证仍是阶段 II 的主要跨数据库依据；有限更新和阶段 III 均不能补足其失败。

## Required routing

该 dossier 可进入新的、独立的叙事与学术语言复评。此结论只确认科学内容保真，不评价研究方法是否正确，
也不评价叙事质量或最终科学准备度。
