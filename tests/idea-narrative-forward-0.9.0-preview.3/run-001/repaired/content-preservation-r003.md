---
schema_version: research-idea-content-preservation-check.v1
check_id: content-preservation-check-I01-001-r003
review_id: content-preservation-I01-001-r003
reviewer_skill: idea-narrative-assessor
reviewer_instance_id: "/root/v006_preservation"
workflow_id: RID-SEPSIS-CSM-20260717-001
round_id: r003
input_artifact_ids: ["idea-dossier-I01-001-v005", "idea-dossier-I01-001-v006", "protected-content-register-I01-001-v005", "revision-delta-I01-001-v005-to-v006"]
input_versions: ["v005", "v006", "v005", "v001"]
inputs:
  prior_dossier:
    artifact_id: idea-dossier-I01-001-v005
    version: v005
    path: tests/idea-narrative-forward-0.9.0-preview.3/run-001/final/idea-dossier-v005.md
  revised_dossier:
    artifact_id: idea-dossier-I01-001-v006
    version: v006
    path: tests/idea-narrative-forward-0.9.0-preview.3/run-001/repaired/idea-dossier-v006.md
  protected_content_register:
    artifact_id: protected-content-register-I01-001-v005
    version: v005
    path: tests/idea-narrative-forward-0.9.0-preview.3/run-001/final/protected-content-register-v005.yaml
  revision_delta:
    artifact_id: revision-delta-I01-001-v005-to-v006
    version: v001
    path: tests/idea-narrative-forward-0.9.0-preview.3/run-001/repaired/revision-delta-v005-to-v006.md
files_read:
  - tests/idea-narrative-forward-0.9.0-preview.3/run-001/final/idea-dossier-v005.md
  - tests/idea-narrative-forward-0.9.0-preview.3/run-001/repaired/idea-dossier-v006.md
  - tests/idea-narrative-forward-0.9.0-preview.3/run-001/final/protected-content-register-v005.yaml
  - tests/idea-narrative-forward-0.9.0-preview.3/run-001/repaired/revision-delta-v005-to-v006.md
isolation_mode: fresh_subagent
prior_scores_visible: false
source_edits_performed: false
decision: scientific_content_preserved
protected_item_checks:
  - protected_id: PCR-V005-001
    prior_locator: "YAML identity_anchor; Title, summary, audience, and positioning; Primary research question"
    revised_locator: "YAML identity_anchor; Title, summary, audience, and positioning; Primary research question; Research identity and final boundary"
    semantic_status: preserved
    evidence: "v006 原样保留五项 identity_anchor；标题、摘要、主要问题和最终边界仍以脓毒症发病前、首次发病、发病后与结局连续体为对象，并仍规定阶段 I–II 在 24 个月内完成。标题中的‘计划性’改为‘预先设定的’，未改变研究身份或核心问题。"
  - protected_id: PCR-V005-002
    prior_locator: "YAML identity_anchor; Research design and methods"
    revised_locator: "YAML identity_anchor; Primary research question; Research design and methods; Research identity and final boundary"
    semantic_status: preserved
    evidence: "v006 的 study_object 与 primary_unit_of_inference 和 v005 相同；主要问题、两项任务的方案锁定、观测模型目标和最终边界继续限定纵向脓毒症 ICU 患者系统、患者—时间状态与状态转移，并继续处理患者与医院层级聚类。"
  - protected_id: PCR-V005-003
    prior_locator: "Data, materials, and existing evidence base; Current feasibility and evidence status"
    revised_locator: "Data, materials, and existing evidence base; Feasibility, resources, risks, alternatives, and stop conditions > Current feasibility and evidence status"
    semantic_status: preserved
    evidence: "v006 保留文献与专家先验、MIMIC-IV v3.1、eICU-CRD v2.0、备份数据库及条件性 EXIT-SEP/XBJ-SCAP 数据来源；试验人数与缺失计数未变。访问凭证和具名人员仍为未核验，双数据库实际支持与新分析结果仍为尚未生成，试验授权和语义仍须核验。"
  - protected_id: PCR-V005-004
    prior_locator: "Research content and work packages; Research design and methods; Scientific falsification criteria"
    revised_locator: "Research content and work packages; Research design and methods; Expected outputs, falsification criteria, and interpretations > Scientific falsification criteria; Feasibility, resources, risks, alternatives, and stop conditions > Operational thresholds, alternatives, and stop conditions"
    semantic_status: preserved
    evidence: "v006 保留阶段 I–II 后才进入条件性阶段 III 的顺序、两项主要任务及其估计目标、模拟恢复与错设情景、按医院隔离的跨数据库验证、观测映射和试验分析方法。所有数值阈值、比较方向、失败后果及阶段依赖仍在，原科学证伪条件也逐项保留；变化仅为标题直释、职责重排和阈值分项展示。"
  - protected_id: PCR-V005-005
    prior_locator: "Structured abstract; Contribution and evidence ladder; Current feasibility and evidence status"
    revised_locator: "Structured abstract; Expected outputs, falsification criteria, and interpretations > Planned outputs; Contribution, innovation, impact, application, and closest-work comparison > Contribution and evidence ladder; Feasibility, resources, risks, alternatives, and stop conditions > Current feasibility and evidence status"
    semantic_status: preserved
    evidence: "v006 将模型、模拟恢复、临床任务、外部验证和试验分析继续标为拟议工作或‘计划生成’，并明确本项目尚无新分析结果。证据层级仍分开报告，claim-support 表中的 supported/qualified 状态及有界检索置信范围未提升，也未加入完成性结果。"
  - protected_id: PCR-V005-006
    prior_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Authoritative limitations, feasibility findings, interpretation boundaries, alternatives, and stop conditions"
    revised_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Authoritative limitations, feasibility findings, interpretation boundaries, alternatives, and stop conditions"
    semantic_status: preserved
    evidence: "v006 仍把该小节指定为限制、可行性发现、解释边界、替代方案和停止条件的唯一完整权威位置。当前状态表、七项科学与解释边界、资源上限，以及每一项操作阈值、替代方案和停止后果均保留；阶段 III 仍位于 24 个月最低交付之外且不能补足阶段 II 任一必要条件的失败。"
  - protected_id: PCR-V005-007
    prior_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Scientific and interpretive boundaries; Research identity and final boundary"
    revised_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Scientific and interpretive boundaries; Research identity and final boundary"
    semantic_status: preserved
    evidence: "v006 继续明确观察性关联和预测表现不识别治疗因果效应、真实反馈网络或反事实策略；试验分支不验证未测潜在动力学、状态转移边、中介机制、个体控制或完整动态系统，也不支持无条件国际临床推广。新算法、全球首次、数字孪生、控制模型、已验证临床决策工具和药物平台等主张仍被排除。"
undeclared_scientific_changes: []
findings: []
unresolved_issues: []
---

# Content-preservation check

## Decision rationale

决定为 `scientific_content_preserved`。冻结 register 中七项受保护内容均可在 v006 中定位，语义、条件性、证据状态与主张强度保持不变。revision delta 声明 `scientific_change: false`、`method_change: false`、`threshold_change: false` 和 `claim_strength_change: false`；逐项比对未发现与该声明冲突的变更。此结论仅涉及内容保存，不评价叙事、语言或科学质量。

## Protected-content trace

- 研究身份和问题在 YAML 锚点、主要问题与最终边界中原样维持；标题措辞由“计划性”改为“预先设定的”。
- 研究对象、推断单位和聚类处理在主要问题、方案锁定和观测模型部分保持；跨时间、未参与开发医院和跨数据库三类验证被展开说明。
- 数据来源、样本计数和可用性状态保持；未核验、尚未生成和条件性状态没有被改写为已具备或已完成。
- 方法、估计目标、数值阈值、失败后果和阶段依赖保持；实现职责、证据链与验收记录经过重排，但没有增删科学承诺。
- 计划产物和证据层级仍以计划或条件性结果表述，贡献定位和支持状态未增强。
- 限制、可行性、解释边界、替代方案和停止条件集中于同一权威小节；重复表述的删减未删除任何登记内容。
- 因果、机制、完整系统、数字孪生、控制和无条件临床应用等不受支持的主张类别继续明确排除。

## Required routing

v006 可进入全新的叙事评估和语言评估；本次核验不替代这两项独立评估。
