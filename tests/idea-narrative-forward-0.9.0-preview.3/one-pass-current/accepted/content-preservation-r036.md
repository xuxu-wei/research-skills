---
schema_version: research-idea-content-preservation-check.v1
check_id: content-preservation-check-I01-001-r036
review_id: content-preservation-review-I01-001-r036
reviewer_skill: idea-narrative-assessor
reviewer_instance_id: fresh-subagent-accepted-preservation-r036
workflow_id: RID-SEPSIS-CSM-20260717-001
round_id: editorial-repair-v025
input_artifact_ids:
  - idea-dossier-I01-001-v003
  - idea-dossier-I01-001-v025
  - protected-content-register-I01-001-v003
  - revision-delta-I01-001-v003-to-v025
input_versions:
  - v003
  - v025
  - v003
  - v003-to-v025
inputs:
  prior_dossier:
    artifact_id: idea-dossier-I01-001-v003
    version: v003
    path: tests/idea-test-0.9.0-preview.1/0.9.0-preview.1/03_ideas/nodes/I01-001/dossiers/idea-dossier-v003.md
  revised_dossier:
    artifact_id: idea-dossier-I01-001-v025
    version: v025
    path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/accepted/idea-dossier-v025.md
  protected_content_register:
    artifact_id: protected-content-register-I01-001-v003
    version: v003
    path: tests/idea-narrative-forward-0.9.0-preview.3/run-001/inputs/protected-content-register.yaml
  revision_delta:
    artifact_id: revision-delta-I01-001-v003-to-v025
    version: v003-to-v025
    path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/accepted/revision-delta-v003-to-v025.md
files_read:
  - tests/idea-test-0.9.0-preview.1/0.9.0-preview.1/03_ideas/nodes/I01-001/dossiers/idea-dossier-v003.md
  - tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/accepted/idea-dossier-v025.md
  - tests/idea-narrative-forward-0.9.0-preview.3/run-001/inputs/protected-content-register.yaml
  - tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/accepted/revision-delta-v003-to-v025.md
isolation_mode: fresh_subagent
prior_scores_visible: false
source_edits_performed: false
decision: editorial_scope_violation
protected_item_checks:
  - protected_id: PCR-001
    prior_locator: "YAML frontmatter identity_anchor; Research question, objectives, and core hypothesis > Primary research question"
    revised_locator: "YAML frontmatter identity_anchor; Title, summary, audience, and positioning > One-sentence complete-Idea summary; Feasibility, resources, risks, alternatives, and stop conditions > Identity and final boundary"
    semantic_status: preserved
    evidence: >-
      v025 保留以脓毒症为中心、从尚未发病和首次发病到发病后状态及恢复、持续恶化、器官衰竭、出 ICU 或死亡的全过程研究身份；最终边界仍明确排除已发病病例预后模型和泛 ICU 风险模型。
  - protected_id: PCR-002
    prior_locator: "YAML frontmatter identity_anchor.primary_objective; Research question, objectives, and core hypothesis > Objectives"
    revised_locator: "YAML frontmatter identity_anchor.primary_objective; Title, summary, audience, and positioning > Positioning and contribution frame; Research content and work packages; Expected outputs, falsification criteria, and interpretations > Planned outputs"
    semantic_status: preserved
    evidence: >-
      文献和专家知识约束候选结构、公共 ICU 数据中的系统辨识与跨数据库验证、阶段 I–II 在 24 个月内完成，以及以高水平论文、可复核证据和可复用资源为交付方向均被保留，未改写为只产出预测工具。
  - protected_id: PCR-003
    prior_locator: "YAML frontmatter identity_anchor.study_object and primary_unit_of_inference; Research design and methods"
    revised_locator: "YAML frontmatter identity_anchor.study_object and primary_unit_of_inference; Research question, objectives, and core hypothesis > Primary research question; Research design and methods > Observational target, anchoring and abstention"
    semantic_status: preserved
    evidence: >-
      v025 的研究对象仍是含可比未发病在险时段和发病后轨迹的纵向脓毒症 ICU 患者系统；患者—时间状态和状态转移仍是主要推断单位，患者与医院聚类仍进入不确定性处理。
  - protected_id: PCR-004
    prior_locator: "Data, materials, and existing evidence base > Current verified-resource versus prospective-gate status; Public ICU database roles and G1 audit"
    revised_locator: "Structured abstract > Approach; Data, materials, and existing evidence base > Current evidence and prospective requirements; Public ICU database roles and G1 support assessment"
    semantic_status: preserved
    evidence: >-
      v025 保留文献和专家先验、MIMIC-IV 与 eICU-CRD 的主要角色，以及 HiRID 或 AmsterdamUMCdb 的预先指定条件性备份角色。数据库存在和版本仍为已核验，而团队访问、DUA、可运行提取、项目样本支持、具名人员和模型结果仍分别标为未核验或尚未生成。
  - protected_id: PCR-005
    prior_locator: "Data, materials, and existing evidence base > Local RCT evidence and present limits"
    revised_locator: "Data, materials, and existing evidence base > Current evidence and prospective requirements; Local RCT evidence and present status; Feasibility, resources, risks, alternatives, and stop conditions > Working assumptions and complete limitations"
    semantic_status: preserved
    evidence: >-
      EXIT-SEP 与 XBJ-SCAP 仍仅是条件性阶段 III 的潜在个体级数据来源；两份本地材料仍被限定为衍生清洗或验证报告，不能替代个体数据授权、原始 CRF/SAP、随机化、中心、访视时序及生存和去向语义核验。
  - protected_id: PCR-006
    prior_locator: "Research content and work packages; Research design and methods"
    revised_locator: "Research content and work packages > Work packages and minimum route; Research design and methods > Observational target, anchoring and abstention; Absolute simulation and semi-synthetic recovery assessment; Hospital-primary cross-database validation; Conditional mapping to RCT visit measurements and independent clinical-state analysis"
    semantic_status: changed
    evidence: >-
      v025 保留资源与样本支持、标签和状态、简单基线、绝对恢复、至多一个复杂候选、两项主要任务和两项次要诊断、独立外部测试及条件性试验分析的顺序，也保留状态、行动和观测过程分离；但 v003 在弃权规则中明确规定“bootstrap 保留<80%”即删除、合并或标记为数据库或照护政策特异，v025 仅写成 bootstrap 保留“未达到预设数值”，且全文没有给出该数值，因而把一个可执行的定量科学判定改成了未定义条件。
  - protected_id: PCR-007
    prior_locator: "Research content and work packages > Conjunctive minimum success definition; Research design and methods > Hospital-primary genuine cross-database validation"
    revised_locator: "Research content and work packages > Conjunctive minimum success definition; Research design and methods > Hospital-primary cross-database validation; Feasibility, resources, risks, alternatives, and stop conditions > Risks, bounded alternatives, and stopping rules"
    semantic_status: preserved
    evidence: >-
      阶段 II 成功仍是数据支持、绝对恢复、两项主要任务的 proper score 与校准、泄漏控制、不更新参数的独立外部测试、状态对齐和结构稳定性的合取结果。有限适配结果仍被分开报告且不能替代外部测试失败，阶段 III 仍不计入阶段 II 成功。
  - protected_id: PCR-008
    prior_locator: "Research design and methods > Protocol locks for the two primary clinical tasks; Mutually exclusive post-onset state/event system"
    revised_locator: "Research design and methods > Protocol specifications for the two primary clinical tasks; Mutually exclusive post-onset state/event system"
    semantic_status: preserved
    evidence: >-
      v025 保留标本在先时 72 小时内给药、给药在先时 24 小时内采样的配对规则，基线 SOFA、滚动 24 小时成分和首个可排序发病时刻；也保留只分析首次发病、一次住院重叠 landmark 总权重为 1、delayed entry、互斥状态、竞争终止、as-of 约束、proper score 和校准目标、患者与医院聚类、同时间段 A_t 与下一状态排序、不可排序同时间戳边排除，以及未来信息和跨划分泄漏检查。
  - protected_id: PCR-009
    prior_locator: "Structured abstract; Contribution, innovation, impact, application, and closest-work comparison > Contribution and evidence ladder"
    revised_locator: "Structured abstract; Data, materials, and existing evidence base > Current evidence and prospective requirements; Contribution, innovation, impact, application, and closest-work comparison"
    semantic_status: preserved
    evidence: >-
      模型、模拟恢复、外部验证和试验新分析仍全部是计划产物或尚未生成；贡献仍限于条件性的整合、验证与基准资源增量。v025 仍说明各模块已有先例，并把完整组合缺口限定为截至 2026-07-17 的有界检索所支持的低至中等置信判断，没有改成全球首次或新算法主张。
  - protected_id: PCR-010
    prior_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Resources and governance; Risk and automatic alternative matrix; Remaining execution gates; Identity and final stop boundary; Expected outputs, falsification criteria, and interpretations > Falsification and stop criteria"
    revised_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Working assumptions and complete limitations; Risks, bounded alternatives, and stopping rules; Identity and final boundary"
    semantic_status: changed
    evidence: >-
      v025 把资源与访问、团队承诺、G1 支持、标签与泄漏、可恢复性、MNAR 与低重叠、外部验证、时间、试验数据与语义、共同锚点和映射、相关研究检索不确定性及主要停止后果集中到第 14 节；然而 v003 明确规定试验方向不一致或区间过宽时只能报告“无支持/运输有限”，且不得挑选亚组挽救，v025 的权威限制与停止规则均没有保留这一失败解释。该规则的消失使统计不确定或跨试验不一致结果的允许解释范围变宽。
  - protected_id: PCR-011
    prior_locator: "Research content and work packages > Twenty-four-month minimum and dated gates; Identity and final stop boundary"
    revised_locator: "Research content and work packages > Twenty-four-month minimum and dated decisions; Feasibility, resources, risks, alternatives, and stop conditions > Working assumptions and complete limitations; Identity and final boundary"
    semantic_status: preserved
    evidence: >-
      阶段 I–II 仍须在 24 个月内形成最低交付；阶段 III 仍位于最低交付之外，且只有阶段 II 成功并满足试验数据、语义和访视映射条件时才开展。v025 仍明确后续试验不能绕过或补救资源、恢复、主要任务和外部验证失败。
  - protected_id: PCR-012
    prior_locator: "Research question, objectives, and core hypothesis > Core hypothesis and non-hypotheses; Feasibility, resources, risks, alternatives, and stop conditions"
    revised_locator: "Research question, objectives, and core hypothesis > Core hypothesis and non-hypotheses; Feasibility, resources, risks, alternatives, and stop conditions > Working assumptions and complete limitations; Identity and final boundary"
    semantic_status: preserved
    evidence: >-
      v025 仍明确观察性数据和预测表现不能识别真实因果网络、治疗因果效应、反事实策略、机制、中介、控制或数字孪生；条件性试验次要分析不能验证未测潜在动力学、转移边或整个系统模型，且当前计划不是已验证模型、临床决策工具、药物平台或无条件推广依据。
undeclared_scientific_changes:
  - change_id: USC-R036-001
    protected_id: PCR-006
    change: >-
      删除了状态或边的 bootstrap 保留率低于 80% 时触发删除、合并或特异性标记的明确数值，改成 dossier 内未定义的“预设数值”。
  - change_id: USC-R036-002
    protected_id: PCR-010
    change: >-
      删除了试验方向不一致或区间过宽时只允许报告无支持或运输有限、不得以亚组选择挽救的解释规则。
findings:
  - finding_id: CP-R036-001
    classification: undeclared_scientific_omission
    protected_ids: [PCR-006]
    prior_evidence: "v003, Research design and methods > Observational target, anchoring and abstention: bootstrap 保留<80% 触发删除、合并或特异性标记。"
    revised_evidence: "v025 同名小节只写 bootstrap 保留未达到“预设数值”，全文未给出该数值。"
    required_route: "恢复原有 80% 判定，或把任何有意阈值变化声明为科学变更并返回科学审查。"
  - finding_id: CP-R036-002
    classification: undeclared_scientific_omission
    protected_ids: [PCR-010]
    prior_evidence: "v003, Expected outputs, falsification criteria, and interpretations > Falsification and stop criteria: 方向不一致或区间宽只报告无支持/运输有限，不挑亚组挽救。"
    revised_evidence: "v025 的第 14 节权威限制、风险表和试验分析规则没有这一解释边界。"
    required_route: "在第 14 节权威位置恢复该失败解释，不在其他章节重复；如有意改变解释规则，则声明科学变更并返回科学审查。"
unresolved_issues: []
---

# Content-preservation check

## Decision rationale

v025 没有改变研究身份、核心问题、对象、主要数据来源、阶段关系或禁止升级的主张，PCR-001 至 PCR-005、PCR-007 至 PCR-009、PCR-011 和 PCR-012 均可直接追溯且保持原有含义和强度。但是，PCR-006 的一个明确数值弃权规则被压缩成 dossier 内未定义的条件，PCR-010 的一项试验失败解释被删除；revision delta 又把全部修改声明为纯编辑操作。因此本轮返回 `editorial_scope_violation`，不能以内容保真通过处理。

## Protected-content trace

完整限制已集中到 `Feasibility, resources, risks, alternatives, and stop conditions`，其他章节中的局部限定主要用于直接定义相邻估计对象、数据状态或设计选择；未发现身份漂移、结果被写成已完成、阶段 III 被写成阶段 II 的补救，或因果、控制和数字孪生主张升级。需要恢复的两项内容分别是 `Observational target, anchoring and abstention` 中 bootstrap 保留率的 80% 数值，以及第 14 节唯一权威位置中对试验方向不一致或区间过宽结果的允许解释和亚组边界。

## Required routing

该 dossier 不得直接进入 fresh narrative/language assessment 或 idea evaluation。应在不改变其他科学内容的前提下恢复上述两项原有规则，生成新的完整 dossier 与 revision delta，再由另一 fresh content-preservation reviewer 核验；若任一变化是有意的科学修改，则必须明确声明并返回科学审查。
