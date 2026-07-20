---
schema_version: research-idea-content-preservation-check.v1
check_id: content-preservation-I01-001-v003-to-v034-r051
review_id: content-preservation-review-I01-001-r051
reviewer_skill: idea-narrative-assessor
reviewer_instance_id: fresh-content-preservation-reviewer-r051
workflow_id: RID-SEPSIS-CSM-20260717-001
round_id: r051
input_artifact_ids:
  - idea-dossier-I01-001-v003
  - idea-dossier-I01-001-v034
  - protected-content-register-I01-001-v003-r003
  - revision-delta-I01-001-v003-to-v034
input_versions: [v003, v034, r003, v003-to-v034]
inputs:
  prior_dossier:
    artifact_id: idea-dossier-I01-001-v003
    version: v003
    path: tests/idea-test-0.9.0-preview.1/0.9.0-preview.1/03_ideas/nodes/I01-001/dossiers/idea-dossier-v003.md
  revised_dossier:
    artifact_id: idea-dossier-I01-001-v034
    version: v034
    path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current/idea-dossier-v034.md
  protected_content_register:
    artifact_id: protected-content-register-I01-001-v003-r003
    version: r003
    path: tests/idea-narrative-forward-0.9.0-preview.3/run-001/inputs/protected-content-register-v003.yaml
  revision_delta:
    artifact_id: revision-delta-I01-001-v003-to-v034
    version: v003-to-v034
    path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current/revision-delta-v003-to-v034.md
files_read:
  - tests/idea-test-0.9.0-preview.1/0.9.0-preview.1/03_ideas/nodes/I01-001/dossiers/idea-dossier-v003.md
  - tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current/idea-dossier-v034.md
  - tests/idea-narrative-forward-0.9.0-preview.3/run-001/inputs/protected-content-register-v003.yaml
  - tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current/revision-delta-v003-to-v034.md
isolation_mode: fresh_subagent
prior_scores_visible: false
source_edits_performed: false
decision: scientific_content_preserved
protected_item_checks:
  - protected_id: PCR-001
    prior_locator: "YAML frontmatter identity_anchor; Research question, objectives, and core hypothesis > Primary research question"
    revised_locator: "YAML frontmatter identity_anchor（第 17–22 行）；Research question, objectives, and core hypothesis > Primary research question（第 68–70 行）"
    semantic_status: preserved
    evidence: >-
      v034 的 identity_anchor 原样保留以脓毒症为中心、覆盖发病前、发病、发病后和结局连续体的研究问题，以及研究对象和患者—时间状态/转移推断单位。主问题正文再次写明“覆盖发病前、首次发病、发病后和结局连续体”并检验医院和数据库间的患者状态与候选结构；第 56–60 行把待解决问题界定为表征恢复、患者时间任务和隔离外部检验，而非普通预测或泛 ICU 风险分层。
  - protected_id: PCR-002
    prior_locator: "YAML frontmatter identity_anchor.primary_objective; Research question, objectives, and core hypothesis > Objectives"
    revised_locator: "YAML frontmatter identity_anchor.primary_objective（第 19 行）；Structured abstract > Objective and hypothesis（第 39 行）；Objectives（第 72–77 行）；Work packages and minimum route（第 110–120 行）"
    semantic_status: preserved
    evidence: >-
      v034 第 19 行保留“construct and validate ... with stage II completed within 24 months”；第 39 行把 24 个月目标明确为双库队列审计、模型恢复与跨数据库检验。四项目标和 WP1–WP4 仍从文献/知识约束、双库审计、系统恢复、两项主要任务与两项次要诊断推进到未触碰跨库检验；第 42、357–367 行把交付限定为整合、验证、基准评测、可复用资源和可审计证据，而非仅产出预测工具。
  - protected_id: PCR-003
    prior_locator: "YAML frontmatter identity_anchor.study_object and primary_unit_of_inference; Research design and methods"
    revised_locator: "YAML frontmatter identity_anchor.study_object / primary_unit_of_inference（第 20、22 行）；Title, summary, audience, and positioning（第 32 行）；Protocol locks for the two primary clinical tasks（第 165–179 行）"
    semantic_status: preserved
    evidence: >-
      v034 frontmatter 保留“longitudinal sepsis-centered ICU patient system”、可比较的未发病在险时段与发病后轨迹，以及尊重患者和医院聚类的患者—时间状态及状态转移。第 32 行仍覆盖发病前在险时段、首次发病、发病后互斥状态和结局；第 173、177 行规定重叠评估点每次住院总权重为 1，并按患者和医院聚类计算不确定性。
  - protected_id: PCR-004
    prior_locator: "Data, materials, and existing evidence base > Current verified-resource versus prospective-gate status; Public ICU database roles and G1 audit"
    revised_locator: "Current verified-resource versus prospective status（第 124–134 行）；Public ICU database roles and G1 audit（第 136–145 行）；Working assumptions > 数据与团队 / 结果状态（第 388、395 行）"
    semantic_status: preserved
    evidence: >-
      v034 第 128–130 行保留 MIMIC-IV 与 eICU-CRD 为两个主库、HiRID 或 AmsterdamUMCdb 为须预指定和审计的条件性备份，并明确只有数据库存在、版本和文献已核验；团队凭证、数据使用协议、可运行提取、项目队列支持及 G1 结果尚未核验或生成。第 133、384、388、395 行又明确只有角色规范而无具名人员承诺，候选模型、模拟、外部测试和试验新分析结果均未生成，没有把未来资源或结果写成现状。
  - protected_id: PCR-005
    prior_locator: "Data, materials, and existing evidence base > Local RCT evidence and present limits"
    revised_locator: "Current verified-resource versus prospective status（第 131–133 行）；Local RCT evidence（第 157–161 行）；Working assumptions > 试验授权与语义（第 393 行）；Limitations and boundary conditions（第 403–404 行）"
    semantic_status: preserved
    evidence: >-
      v034 第 131–132 行把 EXIT-SEP 与 XBJ-SCAP 材料限定为衍生清洗/验证报告和条件性阶段 III 输入，明确它们不是原始病例报告表、统计分析计划或独立审计，且个体数据授权、随机化、中心、访视时序及生存/住院/出院语义均未核验。第 159–161 行仅陈述衍生报告中的稀疏访视与字段缺口；第 393、403–404 行再次规定须以原始试验材料或数据持有人确认，不能用现有材料替代授权和原始语义核验。
  - protected_id: PCR-006
    prior_locator: "Research content and work packages; Research design and methods, including Observational target, anchoring, missingness and abstention"
    revised_locator: "Work packages and minimum route（第 110–120 行）；Candidate variable-role firewall（第 147–155 行）；Observational target, anchoring, missingness and abstention（第 194–204 行）；Risks, alternatives, and stop conditions（第 411–418 行）"
    semantic_status: preserved
    evidence: >-
      v034 第 120 行保持单向顺序：资源/G1、标签/状态/医院拆分、竞争风险与多状态基线、线性状态空间、绝对模拟检验、至多一个复杂方案、两项主要任务和两项次要诊断、开发冻结、未触碰外部检验，最后才是条件性试验分析。第 151–155、196–200 行继续分离生理状态、治疗行动和观察过程。第 202–204 行保留锚定和弃权约束，以及 20 种子对齐率<90%、bootstrap 保留率<80%、外部符号一致率<80%、状态对齐<0.70 或区间未校准时删除、合并或标为数据库/照护政策特异；第 414 行明确较好预测不得豁免恢复、错误发现率、覆盖、零边或错设情景失败。
  - protected_id: PCR-007
    prior_locator: "Research content and work packages > Conjunctive minimum success definition; Research design and methods > Hospital-primary genuine cross-database validation"
    revised_locator: "Conjunctive minimum success definition（第 98–108 行）；Hospital-primary genuine cross-database validation（第 220–230 行）；Limitations and boundary conditions（第 402 行）；Risks, alternatives, and stop conditions（第 416、423 行）"
    semantic_status: preserved
    evidence: >-
      v034 第 100–106 行仍把阶段 II 成功定义为数据支持、正确/零边/错设生成情景的绝对判定、两项主要任务的 Brier 与校准、泄漏清零、未触碰测试区不作更新表现、状态对齐和结构符号一致的合取结果，并保留 +0.01、0.80–1.20、0.02、20 家医院、0.70 和 0.80 等硬数值。第 230 行按不作更新、只校准、只更新观测层的顺序分开报告；第 402、416 行明确有限更新或全模型重拟合不能替代不作更新失败；第 423 行明确阶段 III 不能补足阶段 II 的资源、恢复、主要任务或未触碰外部检验失败。
  - protected_id: PCR-008
    prior_locator: "Research design and methods > Protocol locks for the two primary clinical tasks; Mutually exclusive post-onset state/event system"
    revised_locator: "Protocol locks for the two primary clinical tasks（第 165–179 行）；Mutually exclusive post-onset state/event system（第 181–192 行）；Conjunctive minimum success definition（第 100–108 行）"
    semantic_status: preserved
    evidence: >-
      v034 保留两项主要任务及 event/availability 双时钟、首次发病风险集、delayed entry、竞争终止、as-of 特征和患者/医院聚类。第 170 行完整保留标本先于给药时 72 小时、给药先于采集时 24 小时的配对规则，基线 SOFA=0 或入 ICU 前 24 小时最低可计算值、滚动 24 小时最差组件、感染前 48 小时至后 24 小时窗口和首个可排序 onset；第 173、175 行保留仅首次发病、重叠评估点每住院总权重 1、A_t 与下一状态排序及排除无法排序同时间戳边。第 179 行逐项检查同格行动、未来测量频率、跨拆分患者/住院与插补、重叠权重及结局驱动的变量、网格或阈值；第 183–192 行保留互斥后发病状态及优先级；第 104–106、176–177 行保留 proper score/校准目标和聚类不确定性。
  - protected_id: PCR-009
    prior_locator: "Structured abstract; Contribution, innovation, impact, application, and closest-work comparison > Contribution and evidence ladder"
    revised_locator: "Structured abstract（第 38–42 行）；Contribution, innovation, impact, application, and closest-work comparison（第 355–367 行）；Title and positioning claim-support table（第 369–378 行）"
    semantic_status: preserved
    evidence: >-
      v034 第 41 行明确所有模型、恢复、外部检验和试验分析均为计划产物而非现有模型或结果；第 42、357–367 行只把可能贡献表述为条件性的整合、验证、基准评测、可复用资源和方法治理。第 367、378 行承认单项模块已有先例，完整证据连接缺口只有低至中等置信，并明确不主张新算法或全球首次，保持原有证据状态和主张强度。
  - protected_id: PCR-010
    prior_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Resources and governance; Risk and automatic alternative matrix; Remaining execution gates; Identity and final stop boundary; Expected outputs, falsification criteria, and interpretations > Falsification and stop criteria"
    revised_locator: "Feasibility, resources, risks, alternatives, and stop conditions（第 380–423 行），尤其 Working assumptions（第 386–395 行）、Limitations and boundary conditions（第 397–405 行）和 Risks, alternatives, and stop conditions（第 407–423 行）"
    semantic_status: preserved
    evidence: >-
      v034 第 14 节集中保留访问/协议/提取、具名团队和数据保管、G1 支持、标签与泄漏、状态恢复、MNAR 与低重叠、不作更新外部检验、时间节点、试验授权与语义、共同锚点/观测连接及最接近工作不确定性。第 390–392 行明确临床尺度到模拟参数的映射、精确多类别校准估计量、置信界和阈值登记表仍未解决；第 389 行保留事件或参数筛选下限不能替代经验有效样本量和模拟稳定性。第 409–421 行为每类失败列明触发、替代与停止/降级结果；第 419 行规定两试验方向不一致或区间过宽只报告无支持或适用性有限，不得选择亚组挽救结论。其他章节仅保留与相邻论证直接相连的短边界，未另设相互冲突的权威限制清单。
  - protected_id: PCR-011
    prior_locator: "Research content and work packages > Twenty-four-month minimum and dated gates; Identity and final stop boundary"
    revised_locator: "Twenty-four-month minimum and dated criteria（第 85–96 行）；Risks, alternatives, and stop conditions 末段（第 423 行）"
    semantic_status: preserved
    evidence: >-
      v034 第 87–96 行规定阶段 I–II 的双库审计、恢复与跨数据库检验在 24 个月内完成，试验分析位于 24 个月后。第 423 行明确月 24 无论成功或降级均封存阶段 II，阶段 III 只有在阶段 II 成功且相应试验数据、语义和观测连接满足预设条件时才能开展；任何试验结果都不能补足资源、恢复、主要任务或未触碰外部检验失败，也不能绕过这些要求。
  - protected_id: PCR-012
    prior_locator: "Research question, objectives, and core hypothesis > Core hypothesis and non-hypotheses; Feasibility, resources, risks, alternatives, and stop conditions"
    revised_locator: "Limitations and boundary conditions（第 397–405 行）；Working assumptions > 结果状态（第 395 行）；Structured abstract（第 41–42 行）"
    semantic_status: preserved
    evidence: >-
      v034 第 400 行明确观察性目标和预测表现不支持真实因果网络、治疗因果效应、反事实策略、机制、中介、控制或数字孪生主张；第 403 行明确试验分支不验证未测潜在动力学、转移边、完整系统模型或因果机制，独立 SOFA 分支与阶段 II 无关。第 395、404–405 行又规定计划产物不得写成已验证结果，也不支持已验证临床决策工具、药物平台或无条件国际临床推广，保持全部不支持主张类别和条件性边界。
undeclared_scientific_changes: []
findings: []
unresolved_issues: []
---

# Content-preservation check

## Decision rationale

`scientific_content_preserved`。冻结 register 的 12 个 protected item 均在 v034 中有可定位的正文或 frontmatter 证据，且研究身份、数据与结果状态、数值和时间规则、分析分支、失败解释、主张强度、关键限制、条件性要求以及不越级和不挽救规则均保持原意。修订主要采用重排、合并、定义和自然语言替换；未发现新增数据、方法、结果或证据，也未发现限制弱化、计划工作结果化或研究身份漂移。revision delta 未声明科学变更；本决定依据上述 v003—v034 实际文本比较，而非该声明本身。

## Protected-content trace

- 身份与目标由 v034 frontmatter、研究问题、目标和 24 个月时间表共同保留。
- 资源现状和未生成结果移至 `Current verified-resource versus prospective status` 与第 14 节 `Working assumptions`，仍明确区分已核验数据库存在和未核验的团队访问、授权、提取、人员及结果。
- 设计、数值规则和失败响应分别保留在时间表、主要任务协议、状态系统、缺失与弃权、绝对恢复、跨数据库检验和条件性试验分析中；没有用概括性文字替代 register 中列出的阈值或分支。
- 完整限制、未解决方法细节和停止后果集中在第 14 节；局部章节仅保留解释相邻设计所需的短限定。外部有限更新、试验独立分支或亚组结果均不能挽救上游失败。
- 贡献定位继续限定为计划中的条件性整合、验证、基准评测与可复用资源；未升级为新算法、全球首次、因果机制、数字孪生、临床决策工具或药物平台。

## Required routing

v034 可进入新的叙事与语言评估；无需因内容保存问题返回科学审查。
