---
schema_version: research-idea-content-preservation-check.v1
check_id: content-preservation-I01-001-r002
review_id: content-preservation-review-I01-001-r002
reviewer_skill: idea-narrative-assessor
reviewer_instance_id: idea-narrative-assessor-preservation-r002-20260718
workflow_id: RID-SEPSIS-CSM-20260717-001
round_id: r002
input_artifact_ids:
  - idea-dossier-I01-001-v004
  - idea-dossier-I01-001-v005
  - protected-content-register-I01-001-v004
  - revision-delta-I01-001-v004-to-v005
input_versions:
  - v004
  - v005
  - v004
  - v001
inputs:
  prior_dossier:
    artifact_id: idea-dossier-I01-001-v004
    version: v004
    path: tests/idea-narrative-forward-0.9.0-preview.3/run-001/revised/idea-dossier-v004.md
  revised_dossier:
    artifact_id: idea-dossier-I01-001-v005
    version: v005
    path: tests/idea-narrative-forward-0.9.0-preview.3/run-001/final/idea-dossier-v005.md
  protected_content_register:
    artifact_id: protected-content-register-I01-001-v004
    version: v004
    path: tests/idea-narrative-forward-0.9.0-preview.3/run-001/revised/protected-content-register-v004.yaml
  revision_delta:
    artifact_id: revision-delta-I01-001-v004-to-v005
    version: v001
    path: tests/idea-narrative-forward-0.9.0-preview.3/run-001/final/revision-delta-v004-to-v005.md
files_read:
  - tests/idea-narrative-forward-0.9.0-preview.3/run-001/revised/idea-dossier-v004.md
  - tests/idea-narrative-forward-0.9.0-preview.3/run-001/final/idea-dossier-v005.md
  - tests/idea-narrative-forward-0.9.0-preview.3/run-001/revised/protected-content-register-v004.yaml
  - tests/idea-narrative-forward-0.9.0-preview.3/run-001/final/revision-delta-v004-to-v005.md
isolation_mode: fresh_subagent
prior_scores_visible: false
source_edits_performed: false
decision: scientific_content_preserved
protected_item_checks:
  - protected_id: PCR-V004-001
    prior_locator: "YAML identity_anchor; Title, summary, audience, and positioning; Primary research question"
    revised_locator: "YAML identity_anchor; Title, summary, audience, and positioning; Primary research question"
    semantic_status: preserved
    evidence: >-
      v004 与 v005 的五项 identity_anchor 值完全一致；标题、完整 Idea 摘要和主要研究问题继续限定为覆盖发病前、首次发病、发病后和结局的脓毒症候选动态系统模型，阶段 I–II 仍须在 24 个月内完成，阶段 III 仍为条件性安排，未改写为普通临床预测或泛 ICU 风险研究。
  - protected_id: PCR-V004-002
    prior_locator: "YAML identity_anchor; Research design and methods"
    revised_locator: "YAML identity_anchor; Research design and methods"
    semantic_status: preserved
    evidence: >-
      study_object 与 primary_unit_of_inference 未变；Research design and methods 的对象、患者—时间状态、状态转移、患者聚类和医院聚类规定逐项保持，系统边界及主要推断单位没有扩张、缩减或替换。
  - protected_id: PCR-V004-003
    prior_locator: "Data, materials, and existing evidence base; Feasibility, resources, risks, alternatives, and stop conditions > Current feasibility and evidence status"
    revised_locator: "Data, materials, and existing evidence base; Feasibility, resources, risks, alternatives, and stop conditions > Current feasibility and evidence status"
    semantic_status: preserved
    evidence: >-
      文献与专家先验、MIMIC-IV、eICU-CRD、备份数据库以及条件性 EXIT-SEP 和 XBJ-SCAP 数据来源均未改变。v005 仍将团队访问凭证、数据使用协议、双数据库实际支持、试验个体数据授权和试验语义列为未核验或尚未生成，未把条件性资源写成已经具备。
  - protected_id: PCR-V004-004
    prior_locator: "Research content and work packages; Research design and methods; Expected outputs, falsification criteria, and interpretations > Scientific falsification criteria"
    revised_locator: "Research content and work packages; Research design and methods; Expected outputs, falsification criteria, and interpretations > Scientific falsification criteria"
    semantic_status: preserved
    evidence: >-
      阶段顺序、两项主要任务、估计目标、模拟恢复、医院级跨数据库验证、条件性试验映射、全部数值阈值和科学证伪标准均逐段保持。唯一相关措辞变更只是将指向科学证伪标准的导航由“第 11 节”替换为现有小节标题，不改变标准本身、章节职责或阶段依赖关系。
  - protected_id: PCR-V004-005
    prior_locator: "Structured abstract; Contribution, innovation, impact, application, and closest-work comparison > Contribution and evidence ladder; Feasibility, resources, risks, alternatives, and stop conditions > Current feasibility and evidence status"
    revised_locator: "Structured abstract; Contribution, innovation, impact, application, and closest-work comparison > Contribution and evidence ladder; Feasibility, resources, risks, alternatives, and stop conditions > Current feasibility and evidence status"
    semantic_status: preserved
    evidence: >-
      模型、恢复、外部验证和试验分析仍明确表述为计划产物或尚未生成的结果；贡献仍限定为条件性的证据整合、验证、研究基准和可复用资源，完整组合缺口仍仅获低至中等置信支持，现有证据和可行性主张均未增强。
  - protected_id: PCR-V004-006
    prior_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Authoritative limitations, feasibility findings, interpretation boundaries, alternatives, and stop conditions"
    revised_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Authoritative limitations, feasibility findings, interpretation boundaries, alternatives, and stop conditions"
    semantic_status: preserved
    evidence: >-
      该小节在 v005 中仍是限制、可行性发现、解释边界、替代方案和停止条件的唯一权威位置；全部操作阈值、触发后果和风险条目保持不变，阶段 III 仍不能补足阶段 II 的失败。导航替换没有移动、删除或弱化任何限制、假设、应对方案或停止条件。
  - protected_id: PCR-V004-007
    prior_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Scientific and interpretive boundaries; Feasibility, resources, risks, alternatives, and stop conditions > Research identity and final boundary"
    revised_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Scientific and interpretive boundaries; Feasibility, resources, risks, alternatives, and stop conditions > Research identity and final boundary"
    semantic_status: preserved
    evidence: >-
      v005 继续明确排除由观察性或预测证据推断治疗因果效应、真实反馈网络、反事实策略、机制、控制或数字孪生；试验分支仍不验证未测动力学、完整动态系统或无条件临床应用，且主要推断单位或连续体一旦改变仍须重新界定研究身份。
undeclared_scientific_changes: []
findings: []
unresolved_issues: []
---

# Content-preservation check

## Decision rationale

v004 与 v005 的逐段对照仅发现两类变化：frontmatter 中版本身份、创建轮次和逻辑血缘随新版本更新；正文将权威限制小节内指向科学证伪标准的“第 11 节”改为可直接核对的 “Scientific falsification criteria” 小节标题。修订 delta 将该动作记录为 `replace`，并明确科学内容、方法、阈值和主张强度均未改变。冻结 register 的七项保护内容在 v005 中均可定位，意义、条件性和证据强度保持一致。

## Protected-content trace

- 研究身份、对象、范围和推断单位保留在 v005 的 `identity_anchor`、完整 Idea 摘要、主要研究问题及研究设计中。
- 数据与资源状态保留在 “Data, materials, and existing evidence base” 和 “Current feasibility and evidence status”；未核验资源没有被写成已具备。
- 方法、估计目标、模拟恢复、跨数据库验证、数值阈值和科学证伪标准位于原有同名章节，正文内容未变。
- 限制、可行性发现、解释边界、替代方案和停止条件继续集中在唯一权威小节；该小节中的导航现在直接指向 “Scientific falsification criteria”。
- 禁止因果、机制、控制、数字孪生、完整动态系统验证和无条件临床应用等主张的边界未变。

## Required routing

该 dossier 可进入由新的独立实例开展的叙事与学术语言评估；本次核验不对叙事质量或语言准备度作出判断。
