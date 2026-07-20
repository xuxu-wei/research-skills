---
schema_version: research-idea-content-preservation-check.v1
check_id: content-preservation-I01-001-r113
review_id: content-preservation-I01-001-r113
reviewer_skill: idea-narrative-assessor
reviewer_instance_id: fresh-content-preservation-r113
workflow_id: RID-SEPSIS-CSM-20260717-001
round_id: r113
input_artifact_ids:
  - idea-dossier-I01-001-v051
  - idea-dossier-I01-001-v052
  - protected-content-register-I01-001-v004-r004
  - revision-delta-v051-to-v052
input_versions: [v051, v052, r004, v051-to-v052]
inputs:
  prior_dossier:
    artifact_id: idea-dossier-I01-001-v051
    version: v051
    path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v17/idea-dossier-v051.md
  revised_dossier:
    artifact_id: idea-dossier-I01-001-v052
    version: v052
    path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v18/idea-dossier-v052.md
  protected_content_register:
    artifact_id: protected-content-register-I01-001-v004-r004
    version: r004
    path: tests/idea-narrative-forward-0.9.0-preview.3/run-001/inputs/protected-content-register-v004.yaml
  revision_delta:
    artifact_id: revision-delta-v051-to-v052
    version: v051-to-v052
    path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v18/revision-delta-v051-to-v052.md
files_read:
  - tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v17/idea-dossier-v051.md
  - tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v18/idea-dossier-v052.md
  - tests/idea-narrative-forward-0.9.0-preview.3/run-001/inputs/protected-content-register-v004.yaml
  - tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v18/revision-delta-v051-to-v052.md
isolation_mode: fresh_subagent
prior_scores_visible: false
source_edits_performed: false
decision: scientific_content_preserved
protected_item_checks:
  - protected_id: PCR-001
    prior_locator: "YAML frontmatter identity_anchor, lines 23-28; Research question, objectives, and core hypothesis > Primary research question, line 76"
    revised_locator: "YAML frontmatter identity_anchor, lines 23-28; Research question, objectives, and core hypothesis > Primary research question, line 76"
    semantic_status: preserved
    evidence: "五个身份锚点逐字段完全一致；研究仍以脓毒症为中心，覆盖可比未发病在险时段、首次发病、发病后状态演化和结局，并明确区别于普通临床预测或泛重症监护风险分层。"
  - protected_id: PCR-002
    prior_locator: "YAML frontmatter identity_anchor.primary_objective, line 25; Research question, objectives, and core hypothesis > Objectives, lines 78-85; Research content and work packages, lines 92-130"
    revised_locator: "YAML frontmatter identity_anchor.primary_objective, line 25; Research question, objectives, and core hypothesis > Objectives, lines 78-85; Research content and work packages, lines 92-132"
    semantic_status: preserved
    evidence: "阶段 I-II 在 24 个月内完成、由文献和专家知识约束并用公共重症监护数据开展系统辨识和跨数据库检验、以及交付高水平论文与可审计科学证据而非仅预测工具的三项承诺均保留。"
  - protected_id: PCR-003
    prior_locator: "YAML frontmatter identity_anchor.study_object and primary_unit_of_inference, lines 26 and 28; Research design and methods > Observational target, anchoring, and evidence-qualified interpretation, line 224"
    revised_locator: "YAML frontmatter identity_anchor.study_object and primary_unit_of_inference, lines 26 and 28; Research design and methods > Observational target, anchoring, and evidence-qualified interpretation, line 226"
    semantic_status: preserved
    evidence: "研究对象仍是纵向、以脓毒症为中心的重症监护患者系统；推断单位仍是患者-时间状态和状态转移，并保持患者与医院聚类。"
  - protected_id: PCR-004
    prior_locator: "Data, materials, and existing evidence base > Current resource and result status, lines 132-145; Public intensive-care database roles and support audit, lines 147-181"
    revised_locator: "Data, materials, and existing evidence base > Current resource and result status, lines 134-147; Public intensive-care database roles and support audit, lines 149-183"
    semantic_status: preserved
    evidence: "文献和专家先验、MIMIC-IV、eICU-CRD 及预指定的 HiRID 或 AmsterdamUMCdb 备份角色未变；数据库存在和版本仍为已核验，而访问、协议、可运行提取、项目支持、具名人员和模型结果仍为未核验或未生成。"
  - protected_id: PCR-005
    prior_locator: "Data, materials, and existing evidence base > Current resource and result status, lines 140-143; Local randomized-trial evidence status, lines 183-189"
    revised_locator: "Data, materials, and existing evidence base > Current resource and result status, lines 142-145; Local randomized-trial evidence status, lines 185-191"
    semantic_status: preserved
    evidence: "EXIT-SEP 与 XBJ-SCAP 仍仅是条件性阶段 III 的潜在个体级数据来源；本地衍生报告仍不替代分析授权、原始病例报告表或统计分析计划，以及随机化、中心、访视和生存或住院语义核验。"
  - protected_id: PCR-006
    prior_locator: "Research content and work packages, lines 92-130; Research design and methods, lines 191-296"
    revised_locator: "Research content and work packages, lines 92-132; Research design and methods, lines 193-298"
    semantic_status: preserved
    evidence: "审计、锁定、简单基线、绝对恢复、至多一个复杂候选、两项主要任务与两项次要表征诊断、开发冻结、未触碰外部检验、再到条件性试验分析的顺序未变；状态、治疗和测量过程仍分离。20 个随机种子下 90% 对齐率、80% bootstrap 保留率、80% 外部符号一致率、0.70 状态对齐及区间校准规则与相应删除、合并或限定解释后果均未改变。"
  - protected_id: PCR-007
    prior_locator: "Research content and work packages > Conjunctive minimum success definition, lines 106-118; Research design and methods > Hospital-primary cross-database validation, lines 246-265"
    revised_locator: "Research content and work packages > Conjunctive minimum success definition, lines 108-120; Research design and methods > Hospital-primary cross-database validation, lines 248-267"
    semantic_status: preserved
    evidence: "阶段 II 仍要求数据支持、绝对恢复、两项主要任务的恰当评分规则与校准、信息泄漏清零、未触碰外部库的不更新检验、状态对齐及结构稳定性全部成立；有限适配仍与不更新检验分开，不能补救其失败，阶段 III 也不能补足阶段 II。"
  - protected_id: PCR-008
    prior_locator: "Research design and methods > Protocol locks for the two primary clinical tasks, lines 191-207; Mutually exclusive post-onset state and event system, lines 209-220"
    revised_locator: "Research design and methods > Protocol locks for the two primary clinical tasks, lines 193-209; Mutually exclusive post-onset state and event system, lines 211-222"
    semantic_status: preserved
    evidence: "两项主要任务、事件时钟与可用性时钟、感染配对窗、SOFA 基线及滚动窗、首次可排序发病、首次发病分析、延迟进入、重叠标志时点总权重为 1、互斥状态、竞争终止、as-of 特征、校准与 Brier 目标、聚类及全部泄漏防护均保留。"
  - protected_id: PCR-009
    prior_locator: "Structured abstract, lines 43-48; Data, materials, and existing evidence base > Current resource and result status, lines 132-145; Contribution, innovation, impact, application, and closest-work comparison > Contribution and evidence ladder, lines 400-424"
    revised_locator: "Structured abstract, lines 43-48; Data, materials, and existing evidence base > Current resource and result status, lines 134-147; Contribution, innovation, impact, application, and closest-work comparison > Contribution and evidence ladder, lines 402-426"
    semantic_status: preserved
    evidence: "候选表征、模拟恢复、外部验证和试验新分析仍全部表述为计划中或尚未生成；贡献强度仍限于条件性整合、验证和基准或研究资源增量，完整组合缺口仍为低至中等置信，且未新增全球首次或新算法主张。"
  - protected_id: PCR-010
    prior_locator: "Research design and methods, lines 191-296; Expected outputs, falsification criteria, and interpretations, lines 367-398; Feasibility, resources, risks, alternatives, and stop conditions, lines 434-477"
    revised_locator: "Research design and methods, lines 193-298; Expected outputs, falsification criteria, and interpretations, lines 369-400; Feasibility, resources, risks, alternatives, and stop conditions, lines 436-477"
    semantic_status: preserved
    evidence: "第 14 节仍集中保留资源与访问、团队、支持、标签与泄漏、可恢复性、非随机缺失与低重叠、外部检验、时间、试验语义、观测映射和最接近工作限制，以及两项未决规范；方法资格、互斥分支和停止后果仍在方法权威位置，结果证伪与解释仍在第 11 节。试验方向不一致或区间过宽时的保守解释与不得选择亚组改变主要解释的边界未弱化。"
  - protected_id: PCR-011
    prior_locator: "Research content and work packages > 24-month minimum, dated gates and WP5, lines 92-130; Research design and methods > Conditional trial-observation mapping and independent analysis, lines 267-290; Feasibility, resources, risks, alternatives, and stop conditions, lines 456-477"
    revised_locator: "Research content and work packages > 24-month minimum, dated gates and WP5, lines 92-132; Research design and methods > Conditional trial-observation mapping and independent analysis, lines 269-292; Feasibility, resources, risks, alternatives, and stop conditions, lines 458-477"
    semantic_status: preserved
    evidence: "阶段 III 仍位于 24 个月最低交付之外，且共享前提仍仅为阶段 II 成功、相应试验个体数据可用和核心试验语义可核验。观测映射成立分支与映射不成立但独立分析条件成立分支仍为并列条件路径；核心语义不足仍停止新访视结局分析，任何试验结果仍不能补足阶段 II。"
  - protected_id: PCR-012
    prior_locator: "Research question, objectives, and core hypothesis > Core hypothesis and evidence boundary, lines 87-89; Expected outputs, falsification criteria, and interpretations > Claim-support-interpretation matrix, lines 386-398; Feasibility, resources, risks, alternatives, and stop conditions > Limitations and boundary conditions, line 463"
    revised_locator: "Research question, objectives, and core hypothesis > Core hypothesis and evidence boundary, lines 87-89; Expected outputs, falsification criteria, and interpretations > Claim-support-interpretation matrix, lines 388-400; Feasibility, resources, risks, alternatives, and stop conditions > Limitations and boundary conditions, line 465"
    semantic_status: preserved
    evidence: "观察性数据和预测表现仍不支持真实因果网络、治疗因果效应、反事实策略、机制、中介、控制或数字孪生主张；条件性试验分析仍不能验证未测潜在动力学、转移边或整个系统。计划仍不得表述为已验证模型、临床决策工具、药物平台或无条件临床推广依据。"
undeclared_scientific_changes: []
findings: []
unresolved_issues: []
---

# Content-preservation check

## Decision rationale

`scientific_content_preserved`

v051 与 v052 的五个 `identity_anchor` 值逐字段完全一致。正文的数字记号序列一致，15 个二级章节和 137 个表格行保持不变。逐项核验 PCR-001 至 PCR-012 后，未发现研究身份、主张强度、设计与分析顺序、数据或结果状态、限制、停止条件，或条件性后续路径发生改变。修订 delta 明确声明为编辑性修订，且没有声明科学变更。

## Protected-content trace

- `Structured abstract > Objective and hypothesis`（v052 第 45 行）新增“共同生理锚点变量”“锚点观测值”“锚点预测值”的角色定义；后续替换只澄清变量、实测值与模型输出，没有改变锚定、载荷、尺度、覆盖或观测映射阈值。
- `Research content and work packages > 24 个月最低交付与时间节点`（v052 第 97 行）定义恰当评分规则并指明 Brier 分数或多类别 Brier 分数；原有非劣界、校准范围、置信界和最终测试授权条件均保留。
- `Objectives > Objective 3`（v052 第 82 行）及方法权威位置明确区分零边机制下的虚假结构检查与模型错设下错误高置信结构结论的检查；两类检查的判定阈值、失败后果和不得事后调整阈值的规则均保留。
- 两项次要诊断统一命名为“伪遮蔽重建诊断”和“未来轨迹预测诊断”；前者仍只作用于原已测生理值，两者仍不能改变主要任务、绝对恢复或阶段 II 判定。
- 条件性阶段 III 的共享前提、观测映射分支、独立 SOFA 分支和核心语义不足时停止的关系未改变；本次修订未把任一分支条件提升为整个阶段 III 的共同前提。

## Deterministic validation record

- Register validation: `PASS: protected-content register is valid`。
- Preservation-report validation: 校验器返回 `FAIL: preservation: register source does not match the prior dossier`。该结果源于历史 v1 register 的 `source_artifact` 仍指向 v003，而本次指定的直接 prior dossier 是 v051；合同明确允许历史 v1 register 作为有效血缘记录。本报告保留真实的四个逻辑 artifact 引用，不将 v051 伪记为 v003。
- 可审计替代检查：register 与报告均为 PCR-001 至 PCR-012，顺序一致、无重复、无未知 ID；五个身份锚点逐字段完全一致；两版正文均有 15 个二级章节和 137 个表格行；正文的 711 个数字记号顺序完全一致。各保护项的 prior 与 revised locator 及语义证据见 frontmatter 中的 `protected_item_checks`。

## Required routing

该 dossier 可进入 fresh narrative assessment 和 fresh language assessment。
