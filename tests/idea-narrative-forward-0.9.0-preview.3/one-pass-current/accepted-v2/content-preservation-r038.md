---
schema_version: research-idea-content-preservation-check.v1
check_id: content-preservation-I01-001-r038
review_id: content-preservation-I01-001-r038
reviewer_skill: idea-narrative-assessor
reviewer_instance_id: fresh-preservation-r038
workflow_id: RID-SEPSIS-CSM-20260717-001
round_id: r038
input_artifact_ids:
  - idea-dossier-I01-001-v003
  - idea-dossier-I01-001-v026
  - protected-content-register-I01-001-v003-r002
  - revision-delta-I01-001-v003-to-v026
input_versions:
  - v003
  - v026
  - r002
  - v003-to-v026
inputs:
  prior_dossier:
    artifact_id: idea-dossier-I01-001-v003
    version: v003
    path: tests/idea-test-0.9.0-preview.1/0.9.0-preview.1/03_ideas/nodes/I01-001/dossiers/idea-dossier-v003.md
  revised_dossier:
    artifact_id: idea-dossier-I01-001-v026
    version: v026
    path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/accepted-v2/idea-dossier-v026.md
  protected_content_register:
    artifact_id: protected-content-register-I01-001-v003-r002
    version: r002
    path: tests/idea-narrative-forward-0.9.0-preview.3/run-001/inputs/protected-content-register-v002.yaml
  revision_delta:
    artifact_id: revision-delta-I01-001-v003-to-v026
    version: v003-to-v026
    path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/accepted-v2/revision-delta-v003-to-v026.md
files_read:
  - tests/idea-test-0.9.0-preview.1/0.9.0-preview.1/03_ideas/nodes/I01-001/dossiers/idea-dossier-v003.md
  - tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/accepted-v2/idea-dossier-v026.md
  - tests/idea-narrative-forward-0.9.0-preview.3/run-001/inputs/protected-content-register-v002.yaml
  - tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/accepted-v2/revision-delta-v003-to-v026.md
scope:
  comparison_inputs: exactly_the_four_declared_artifacts
  preferred_prior_available: false
  prior_fallback_used: tests/idea-test-0.9.0-preview.1/0.9.0-preview.1/03_ideas/nodes/I01-001/dossiers/idea-dossier-v003.md
  procedural_resources_read:
    - AGENTS.md
    - research-skills-openai/AGENTS.md
    - research-skills-openai/skills/idea-narrative-assessor/SKILL.md
    - research-skills-openai/skills/idea-narrative-assessor/references/content-preservation-contract.md
    - research-skills-openai/skills/idea-narrative-assessor/templates/content-preservation-check.md
    - research-skills-openai/skills/idea-narrative-assessor/scripts/validate_narrative_outputs.py
  excluded_material_read: false
isolation_mode: fresh_subagent
prior_scores_visible: false
source_edits_performed: false
decision: editorial_scope_violation
protected_item_checks:
  - protected_id: PCR-001
    prior_locator: "YAML identity_anchor; Primary research question"
    revised_locator: "YAML identity_anchor; Primary research question; Scientific interpretation boundaries"
    semantic_status: preserved
    evidence: >-
      v026 保留以脓毒症为中心、覆盖发病前、首次发病、发病后恢复或恶化、器官衰竭、活着出 ICU 与死亡结局的候选动态复杂系统研究身份，并明确普通已发病预后模型或泛 ICU 风险模型构成新的研究问题。
  - protected_id: PCR-002
    prior_locator: "YAML identity_anchor.primary_objective; Objectives"
    revised_locator: "YAML identity_anchor.primary_objective; One-sentence complete-Idea summary; Twenty-four-month minimum and dated criteria; Positioning and contribution frame"
    semantic_status: preserved
    evidence: >-
      v026 保留在 24 个月内完成阶段 I–II、由文献和专家知识约束候选结构、用两个公共 ICU 数据库开展系统辨识与跨数据库验证的目标，并把高水平论文和可核查科学证据而非单一预测工具作为交付方向。
  - protected_id: PCR-003
    prior_locator: "YAML identity_anchor.study_object and primary_unit_of_inference; Research design and methods"
    revised_locator: "YAML identity_anchor.study_object and primary_unit_of_inference; Core hypothesis; Protocol specifications for the two primary clinical tasks"
    semantic_status: preserved
    evidence: >-
      v026 的研究对象仍是含未发病在险时段和发病后轨迹的纵向脓毒症 ICU 患者系统，主要推断单位仍为患者—时间状态及状态转移，并保留患者层和医院层聚类不确定性处理。
  - protected_id: PCR-004
    prior_locator: "Current verified-resource versus prospective-gate status; Public ICU database roles and G1 audit"
    revised_locator: "Current evidence and prospective requirements; Public ICU database roles and G1 audit; Current resources and working assumptions"
    semantic_status: preserved
    evidence: >-
      v026 保留 MIMIC-IV 与 eICU-CRD 为主数据库、HiRID 或 AmsterdamUMCdb 为预指定条件性备份，并明确数据库存在与版本已核验，而访问凭证、DUA、可运行提取、项目队列、具名人员和模型结果仍未核验或尚未生成。
  - protected_id: PCR-005
    prior_locator: "Local RCT evidence and present limits"
    revised_locator: "Local randomized-trial evidence and present status; Current resources and working assumptions; trial-data risk row"
    semantic_status: preserved
    evidence: >-
      v026 仍只把 EXIT-SEP 与 XBJ-SCAP 作为条件性阶段 III 的潜在个体级数据来源，并明确本地衍生报告不能替代个体数据授权、原始 CRF 或 SAP、随机化与分析集、中心或分层、访视时序及生存和住院语义核验。
  - protected_id: PCR-006
    prior_locator: "Research content and work packages; Observational target, anchoring and abstention"
    revised_locator: "Work packages and minimum route; Observational target, anchoring, missingness and abstention; Prespecified simulation and semi-synthetic recovery assessment; Complete risk, limitation and prespecified response matrix"
    semantic_status: preserved
    evidence: >-
      v026 保留资源与 G1、标签和状态及医院划分、简单基线、绝对模拟恢复与虚假关系或错误高置信检查、至多一个复杂候选、两项主要任务和两项次要诊断、开发方案确定、未参与开发的外部测试、最后才进入条件性试验分析的顺序。Y_t、A_t 与 M_t 继续分离；90%、80%、80%、0.70 和区间校准触发规则及预测表现不得豁免这些规则均完整保留。
  - protected_id: PCR-007
    prior_locator: "Conjunctive minimum success definition; Hospital-primary genuine cross-database validation"
    revised_locator: "Conjunctive minimum success definition; Hospital-primary cross-database validation; external-validation risk row; Scientific interpretation boundaries"
    semantic_status: preserved
    evidence: >-
      v026 保留数据支持、绝对恢复、两项主要任务的严格适当评分与校准、泄漏清零、不更新参数的外部表现、状态对齐和结构稳定性的合取标准；重新校准、只更新观测模型和完整重新开发均与主要外部验证分开，且不能补足不更新参数或阶段 II 的失败。
  - protected_id: PCR-008
    prior_locator: "Protocol locks for the two primary clinical tasks; Mutually exclusive post-onset state/event system"
    revised_locator: "Protocol specifications for the two primary clinical tasks; Mutually exclusive post-onset state/event system"
    semantic_status: preserved
    evidence: >-
      v026 完整保留两项主要任务、事件时间与信息可用时间、首次发病风险集、延迟进入、互斥状态、竞争终止、当时可用特征、校准与严格适当评分、患者和医院聚类。标本与抗菌药 72 小时或 24 小时配对、baseline SOFA、滚动 24 小时成分、首次可排序发病时刻、首次发病与住院总权重、A_t 与下一状态排序、同时间戳边排除以及指定泄漏检查均保持原义。
  - protected_id: PCR-009
    prior_locator: "Structured abstract; Contribution and evidence ladder"
    revised_locator: "Structured abstract Expected result; Positioning and contribution frame; Contribution and evidence ladder; Representative related-study comparison"
    semantic_status: preserved
    evidence: >-
      v026 明确所有模型、恢复、外部验证和试验新分析均为拟生成产物；贡献继续限定为条件性的证据整合、跨数据库验证与可复用基准资源，各单项模块已有先例，完整组合缺口仅为低至中等置信，且不声称新算法或全球首次。
  - protected_id: PCR-010
    prior_locator: "Feasibility, resources, risks, alternatives, and stop conditions; Remaining execution gates; Falsification and stop criteria"
    revised_locator: "Feasibility, resources, risks, alternatives, and stop conditions"
    semantic_status: changed
    evidence: >-
      v026 第 14 节保留了资源与访问、人员、G1、泄漏、状态恢复、MNAR 与低重叠、外部验证、时间节点、试验语义、模型—试验指标映射、相关研究检索以及试验不一致时不得选择亚组挽救等大部分限制和处置。然而，该权威位置不再明确列出 v003 的三项未决限制：临床尺度到模拟参数的映射；精确多类别校准估计量、置信界与阈值登记；事件或参数筛选下限不能替代经验有效样本量与模拟稳定性。delta 将 PCR-010 声明为完整保留，但未声明这些限制的删除，因此限制集合被无声明地削弱。
  - protected_id: PCR-011
    prior_locator: "Twenty-four-month minimum and dated gates; Identity and final stop boundary"
    revised_locator: "Scientific interpretation boundaries"
    semantic_status: preserved
    evidence: >-
      v026 明确保留阶段 I–II 必须在 24 个月内完成，阶段 III 位于最低交付之外且仅在阶段 II 成功及试验数据、语义和映射满足条件时开展；任何后续试验结果均不能挽救阶段 II 失败或绕过前置要求。
  - protected_id: PCR-012
    prior_locator: "Core hypothesis and non-hypotheses; Feasibility, resources, risks, alternatives, and stop conditions"
    revised_locator: "Scientific interpretation boundaries"
    semantic_status: preserved
    evidence: >-
      v026 的权威边界继续排除由观察性数据或预测表现支持真实因果网络、治疗因果效应、反事实策略、机制、中介、控制或数字孪生，也排除用条件性试验分析验证未测潜在动力学、状态转移边、中介、整个阶段 II 系统模型或个体控制；当前计划仍不得写成已验证模型、临床决策工具、药物平台或无条件临床推广依据。
undeclared_scientific_changes:
  - protected_id: PCR-010
    change: >-
      权威限制位置删除了三项原本明确标为仍未解决且必须显式保留的执行限制，从而弱化了对模拟参数化、校准方案完备性和经验样本支持的限定。
findings:
  - finding_id: CPF-038-001
    protected_id: PCR-010
    severity: blocking
    issue: >-
      v026 未完整保留 PCR-010 所覆盖的全部关键限制，且 revision delta 把该项记为完整保留，未声明科学内容变化。
    required_action: >-
      在第 14 节权威位置恢复临床尺度到模拟参数映射、精确多类别校准估计量与置信界及阈值登记、以及筛选下限不替代经验有效样本量与模拟稳定性的明确限制；随后由新的独立实例重新核验。若有意删除这些限制，应将变化明确声明并返回科学审查。
unresolved_issues: []
---

# Content-preservation check

## Decision rationale

结论为 `editorial_scope_violation`。PCR-001 至 PCR-009、PCR-011 和 PCR-012 均可在 v026 中追踪到相同含义、状态或主张强度；PCR-010 只有部分保留。被删去的三项内容在 v003 中是明确的未决执行限制，删除会弱化对模型可恢复性、校准方案和有效样本支持的科学约束，超出仅作措辞、定义、重排或合并的编辑范围。revision delta 没有声明这一变化，反而将 PCR-010 记录为完整保留。

## Protected-content trace

大多数科学内容被移动到更清楚的局部方法段或第 14 节权威限制位置，核心研究身份、数据状态、协议数值、合取成功标准、试验条件与解释边界均保持可追踪。唯一阻断位于 PCR-010：v003 `Remaining execution gates` 中关于临床尺度到模拟参数映射、精确多类别校准估计量与置信界及阈值登记、以及筛选下限不能替代经验有效样本量与模拟稳定性的明确限制，在 v026 第 14 节及其他位置均未得到同义保留。

## Required routing

v026 不能直接进入新的叙事或语言评估。应先恢复 PCR-010 缺失的三项限制并生成新版本及相应修订说明，再由新的独立实例执行科学内容保真核验；若删除是有意的科学变更，则须明确声明并返回科学审查。
