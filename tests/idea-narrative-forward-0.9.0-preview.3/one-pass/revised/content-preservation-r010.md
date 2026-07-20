---
schema_version: research-idea-content-preservation-check.v1
check_id: content-preservation-I01-001-r010
review_id: content-preservation-I01-001-r010
reviewer_skill: idea-narrative-assessor
reviewer_instance_id: fresh-content-preservation-reviewer-r010
workflow_id: RID-SEPSIS-CSM-20260717-001
round_id: r010
input_artifact_ids:
  - idea-dossier-I01-001-v003
  - idea-dossier-I01-001-v004
  - protected-content-register-I01-001-v003
  - revision-delta-I01-001-v003-to-v004
input_versions:
  - v003
  - v004
  - v003
  - v003-to-v004
inputs:
  prior_dossier:
    artifact_id: idea-dossier-I01-001-v003
    version: v003
    path: tests/idea-test-0.9.0-preview.1/0.9.0-preview.1/03_ideas/nodes/I01-001/dossiers/idea-dossier-v003.md
  revised_dossier:
    artifact_id: idea-dossier-I01-001-v004
    version: v004
    path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass/revised/idea-dossier-v004.md
  protected_content_register:
    artifact_id: protected-content-register-I01-001-v003
    version: v003
    path: tests/idea-narrative-forward-0.9.0-preview.3/run-001/inputs/protected-content-register.yaml
  revision_delta:
    artifact_id: revision-delta-I01-001-v003-to-v004
    version: v003-to-v004
    path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass/revised/revision-delta-v003-to-v004.md
files_read:
  - tests/idea-test-0.9.0-preview.1/0.9.0-preview.1/03_ideas/nodes/I01-001/dossiers/idea-dossier-v003.md
  - tests/idea-narrative-forward-0.9.0-preview.3/one-pass/revised/idea-dossier-v004.md
  - tests/idea-narrative-forward-0.9.0-preview.3/run-001/inputs/protected-content-register.yaml
  - tests/idea-narrative-forward-0.9.0-preview.3/one-pass/revised/revision-delta-v003-to-v004.md
isolation_mode: fresh_subagent
prior_scores_visible: false
source_edits_performed: false
decision: scientific_content_preserved
protected_item_checks:
  - protected_id: PCR-001
    prior_locator: "YAML frontmatter identity_anchor; Research question, objectives, and core hypothesis > Primary research question"
    revised_locator: "YAML frontmatter identity_anchor; Research question, objectives, and core hypothesis > Primary research question; Title, summary, audience, and positioning"
    semantic_status: preserved
    evidence: >-
      v004 继续以脓毒症为中心的发病前、首次发病、发病后互斥状态演化及结局连续体为研究身份，并明确研究对象是知识约束、不确定性感知的候选动态系统表征，而非普通临床预测或泛 ICU 风险分层。
  - protected_id: PCR-002
    prior_locator: "YAML frontmatter identity_anchor.primary_objective; Research question, objectives, and core hypothesis > Objectives"
    revised_locator: "YAML frontmatter identity_anchor.primary_objective; Research question, objectives, and core hypothesis > Objectives; Research content and work packages"
    semantic_status: preserved
    evidence: >-
      v004 保留在 24 个月内完成阶段 I–II 的主要目标，继续以文献和专家先验及公共 ICU 数据开展候选结构构建、系统辨识和跨数据库验证；交付仍指向可审计的科学证据、验证结果及基准或资源，而不缩减为单一预测工具。
  - protected_id: PCR-003
    prior_locator: "YAML frontmatter identity_anchor.study_object and primary_unit_of_inference; Research design and methods"
    revised_locator: "YAML frontmatter identity_anchor.study_object and primary_unit_of_inference; Structured abstract > Objective and hypothesis; Research design and methods > Protocol locks for the two primary clinical tasks; Observational target, anchoring and abstention"
    semantic_status: preserved
    evidence: >-
      v004 的研究对象仍是包含未发病在险时段与发病后轨迹的纵向脓毒症 ICU 患者系统；主要推断单位仍为患者—时间状态及状态转移，并继续采用患者层和医院层聚类不确定性处理。
  - protected_id: PCR-004
    prior_locator: "Data, materials, and existing evidence base > Current verified-resource versus prospective-gate status; Public ICU database roles and G1 audit"
    revised_locator: "Data, materials, and existing evidence base > Current verified-resource versus prospective-gate status; Public ICU database roles and G1 audit; Feasibility, resources, risks, alternatives, and stop conditions > Authoritative assumptions and limitations, items 1–2"
    semantic_status: preserved
    evidence: >-
      v004 保留文献和专家先验、MIMIC-IV、eICU-CRD 及预先指定备份数据库的输入角色；数据库公开存在与版本仍为已核验，而团队访问、数据使用协议、可运行提取、项目队列支持、具名人员及模型结果仍明确为未核验或尚未生成。
  - protected_id: PCR-005
    prior_locator: "Data, materials, and existing evidence base > Local RCT evidence and present limits"
    revised_locator: "Data, materials, and existing evidence base > Current verified-resource versus prospective-gate status; Local RCT evidence and present limits; Research design and methods > Conditional trial-observation projection and independent alternative analysis; Feasibility, resources, risks, alternatives, and stop conditions > Authoritative assumptions and limitations, items 8–9"
    semantic_status: preserved
    evidence: >-
      EXIT-SEP 与 XBJ-SCAP 在 v004 中仍只是条件性阶段 III 的潜在个体数据来源；本地材料仍限定为衍生清洗或验证材料，不能替代个体数据授权、原始病例报告表、统计分析计划，以及随机化、中心、访视时序和生存或住院语义核验。
  - protected_id: PCR-006
    prior_locator: "Research content and work packages; Research design and methods"
    revised_locator: "Research content and work packages > Work packages and minimum route; Research design and methods; Evidence chains"
    semantic_status: preserved
    evidence: >-
      v004 保留资源与 G1 审计、标签和状态及医院拆分锁定、简单基线、模拟恢复与错误高置信判断检验、至多一个复杂候选、两项主要任务与两项次要诊断、开发版本锁定、零更新外部验证、条件性试验分析的固定顺序；生理状态、治疗行动和测量过程仍相互分离，解释仍受锚定、对齐、恢复、外部稳定性和弃权规则约束。
  - protected_id: PCR-007
    prior_locator: "Research content and work packages > Conjunctive minimum success definition; Research design and methods > Hospital-primary genuine cross-database validation"
    revised_locator: "Research content and work packages > Conjunctive minimum success definition; Research design and methods > Hospital-primary genuine cross-database validation; Feasibility, resources, risks, alternatives, and stop conditions > Authoritative interpretation boundaries"
    semantic_status: preserved
    evidence: >-
      阶段 II 成功在 v004 中仍要求数据支持、模拟恢复、两项主要任务的严格适当评分与校准、无高严重度泄漏、独立最终测试集零更新表现、状态对齐和结构符号稳定同时成立；适配后校准或观测模型更新继续单独报告且不能替代零更新失败，阶段 III 也不能补足阶段 II。
  - protected_id: PCR-008
    prior_locator: "Research design and methods > Protocol locks for the two primary clinical tasks; Mutually exclusive post-onset state/event system"
    revised_locator: "Research design and methods > Protocol locks for the two primary clinical tasks; Mutually exclusive post-onset state/event system; Required analyses and evidence"
    semantic_status: preserved
    evidence: >-
      v004 逐项保留两项主要任务、临床事件与标签可用性双时钟、每 12 小时评估、首次发病风险集、延迟进入、互斥发病后状态、竞争终止、截至评估时点的特征约束、严格适当评分和校准目标、患者与医院聚类处理，以及未来信息和跨拆分泄漏防护。
  - protected_id: PCR-009
    prior_locator: "Structured abstract; Contribution, innovation, impact, application, and closest-work comparison > Contribution and evidence ladder"
    revised_locator: "Structured abstract; Contribution, innovation, impact, application, and closest-work comparison > Contribution and evidence ladder; Verified representative closest-work comparison; Title and positioning claim-support table; Feasibility, resources, risks, alternatives, and stop conditions > Authoritative assumptions and limitations, items 10–11"
    semantic_status: preserved
    evidence: >-
      v004 仍把模型、模拟恢复、主要任务、外部验证和试验新分析表述为尚未生成的计划产物；贡献强度仍限于条件性的证据整合、验证及基准或资源，各单项模块已有先例，完整组合缺口的负向判断仍只有低至中等置信度，并明确排除新算法或全球首次主张。
  - protected_id: PCR-010
    prior_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Resources and governance; Risk and automatic alternative matrix; Remaining execution gates; Identity and final stop boundary"
    revised_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Resources and governance; Authoritative assumptions and limitations; Authoritative interpretation boundaries; Risk and automatic alternative matrix; Remaining execution gates"
    semantic_status: preserved
    evidence: >-
      v004 在第 14 节一次性汇总资源与访问、人员承诺、G1 支持、标签与泄漏、状态可恢复性、MNAR 与低重叠、外部可迁移性、时间节点、试验资料语义、共同锚点与观测映射及最接近工作不确定性；风险表同时保留每项触发条件及相应替代、缩减或停止后果，其他章节仅保留直接约束局部分析的必要限定。
  - protected_id: PCR-011
    prior_locator: "Research content and work packages > Twenty-four-month minimum and dated gates; Identity and final stop boundary"
    revised_locator: "Research content and work packages > Twenty-four-month minimum and dated gates; Feasibility, resources, risks, alternatives, and stop conditions > Authoritative assumptions and limitations, item 7; Authoritative interpretation boundaries; Identity and final stop boundary"
    semantic_status: preserved
    evidence: >-
      v004 继续要求阶段 I–II 在 24 个月内完成，并把阶段 III 置于最低交付之外；阶段 III 只有在阶段 II 成功且试验数据、资料语义和观测映射均满足预设条件时才能开展，任何试验结果都不得替代阶段 II 的资源、模拟恢复、主要任务或零更新外部验证要求。
  - protected_id: PCR-012
    prior_locator: "Research question, objectives, and core hypothesis > Core hypothesis and non-hypotheses; Feasibility, resources, risks, alternatives, and stop conditions"
    revised_locator: "Research question, objectives, and core hypothesis > Core hypothesis and non-hypotheses; Contribution, innovation, impact, application, and closest-work comparison > Title and positioning claim-support table; Feasibility, resources, risks, alternatives, and stop conditions > Authoritative interpretation boundaries"
    semantic_status: preserved
    evidence: >-
      v004 完整保留观察性数据和预测表现不能识别治疗因果效应、真实反馈网络或反事实策略的边界，也保留随机分配不能验证未测靶点、潜在连续动力学、转移边、中介、个体控制或整个阶段 II 模型的限制；当前计划仍不得表述为已验证临床模型、临床决策工具、药物平台、可控系统、数字孪生或无条件临床建议。
undeclared_scientific_changes: []
findings: []
unresolved_issues: []
---

# Content-preservation check

## Decision rationale

判定为 `scientific_content_preserved`。冻结注册表中的 12 个受保护条目均在 v004 中有明确定位，其研究身份、目标、对象与推断单位、输入状态、设计顺序、定量标准、证据强度、关键限制、替代分析和停止条件均与 v003 保持一致。修订说明将全部变化声明为编辑性调整；逐项比较未发现新增数据、方法、结果或证据，也未发现未声明的科学变化。

## Protected-content trace

主要非平凡移动是把 PCR-010、PCR-011 和 PCR-012 所涵盖的完整假设、限制、解释边界、替代方案与停止条件集中至第 14 节，同时在方法、证据链和主张审计位置保留直接决定当地分析的最短限定。试验部分把模型状态投影与试验可计算的一维可观测状态摘要明确区分，并将映射不合格后的独立 SOFA 分析改用完整中文名称；这些术语调整未改变共同锚点资格、映射公式、绝对标准、估计目标、分析集、缺失处理、多重性控制或停止规则。跨数据库部分改用“零更新外部验证”“适配后校准”和“观测模型更新”等名称，但医院优先分区、跨分区患者处理、独立最终测试、支持标准及合取判定保持不变。

## Required routing

v004 可进入新的独立叙事评估与学术语言评估；无需返回科学审查。
