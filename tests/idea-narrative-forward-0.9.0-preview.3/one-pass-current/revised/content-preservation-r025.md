---
schema_version: research-idea-content-preservation-check.v1
check_id: content-preservation-I01-001-r025
review_id: content-preservation-review-I01-001-r025
reviewer_skill: idea-narrative-assessor
reviewer_instance_id: "/root/fresh_preservation_r025"
workflow_id: RID-SEPSIS-CSM-20260717-001
round_id: one-pass-current-r025
input_artifact_ids:
  - idea-dossier-I01-001-v003
  - idea-dossier-I01-001-v022
  - protected-content-register-I01-001-v003
  - revision-delta-I01-001-v003-to-v022
input_versions:
  - v003
  - v022
  - v003
  - v022
inputs:
  prior_dossier:
    artifact_id: idea-dossier-I01-001-v003
    version: v003
    path: tests/idea-test-0.9.0-preview.1/0.9.0-preview.1/03_ideas/nodes/I01-001/dossiers/idea-dossier-v003.md
  revised_dossier:
    artifact_id: idea-dossier-I01-001-v022
    version: v022
    path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/revised/idea-dossier-v022.md
  protected_content_register:
    artifact_id: protected-content-register-I01-001-v003
    version: v003
    path: tests/idea-narrative-forward-0.9.0-preview.3/run-001/inputs/protected-content-register.yaml
  revision_delta:
    artifact_id: revision-delta-I01-001-v003-to-v022
    version: v022
    path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/revised/revision-delta-v003-to-v022.md
files_read:
  - tests/idea-test-0.9.0-preview.1/0.9.0-preview.1/03_ideas/nodes/I01-001/dossiers/idea-dossier-v003.md
  - tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/revised/idea-dossier-v022.md
  - tests/idea-narrative-forward-0.9.0-preview.3/run-001/inputs/protected-content-register.yaml
  - tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/revised/revision-delta-v003-to-v022.md
isolation_mode: fresh_subagent
prior_scores_visible: false
source_edits_performed: false
decision: scientific_content_preserved
protected_item_checks:
  - protected_id: PCR-001
    prior_locator: "YAML frontmatter identity_anchor; Research question, objectives, and core hypothesis > Primary research question"
    revised_locator: "YAML frontmatter identity_anchor; Title, summary, audience, and positioning > One-sentence complete-Idea summary; Research question, objectives, and core hypothesis > Primary research question; Research design and methods > Mutually exclusive post-onset state and event system"
    semantic_status: preserved
    evidence: >-
      前后版本的五项 identity_anchor 值逐字一致。v022 的摘要、主要研究问题和互斥状态表仍覆盖未发病在险时段、首次发病、持续脓毒症、生理恢复、恶化或新器官衰竭、存活离开 ICU、转院或无法继续观察及死亡；研究对象仍是候选动态状态模型，而不是普通风险分层。
  - protected_id: PCR-002
    prior_locator: "YAML frontmatter identity_anchor.primary_objective; Research question, objectives, and core hypothesis > Objectives"
    revised_locator: "YAML frontmatter identity_anchor.primary_objective; Title, summary, audience, and positioning; Structured abstract > Objective and hypothesis; Research question, objectives, and core hypothesis > Objectives; Research content and work packages > Twenty-four-month minimum and dated decision points"
    semantic_status: preserved
    evidence: >-
      primary_objective 逐字保留阶段 II 在 24 个月内完成的目标。v022 仍以文献与专家知识约束模型，使用公共 ICU 数据完成系统辨识所需的状态模型构建、绝对恢复和跨数据库检验，并把可审计验证、基准数据与可复用研究资源列为交付；身份边界明确禁止把项目改成普通预测。
  - protected_id: PCR-003
    prior_locator: "YAML frontmatter identity_anchor.study_object and primary_unit_of_inference; Research design and methods"
    revised_locator: "YAML frontmatter identity_anchor.study_object and primary_unit_of_inference; Research question, objectives, and core hypothesis > Primary research question and Core hypothesis; Research design and methods > Protocol locks for the two primary clinical tasks; Observational target, anchoring and abstention"
    semantic_status: preserved
    evidence: >-
      study_object 与 primary_unit_of_inference 逐字一致。v022 保留纵向、以脓毒症为中心的未发病在险时段和发病后轨迹；12 小时患者—时间状态及状态转移仍是推断单位，重叠窗口总权重为 1，并继续以患者和医院为聚类层级进行自助法推断。
  - protected_id: PCR-004
    prior_locator: "Data, materials, and existing evidence base > Current verified-resource versus prospective-gate status; Public ICU database roles and G1 audit"
    revised_locator: "Data, materials, and existing evidence base > Current resource and evidence status; Public ICU database roles and data-support audit; Feasibility, resources, risks, alternatives, and stop conditions > Working assumptions; Limitations and boundary conditions"
    semantic_status: preserved
    evidence: >-
      v022 仍以文献与专家知识、MIMIC-IV v3.1 和 eICU-CRD v2.0 为核心输入，并规定 HiRID 或 AmsterdamUMCdb 只能在查看最终测试结果前作为预先指定的条件性备份。仅数据库存在、版本和文献为已核验；访问凭证、数据使用协议、可运行提取、项目队列支持和具名人员仍为尚未核验，模型、模拟恢复、预测和外部结果仍为尚未生成。概述中的 24 个月计划不改变这些当前证据状态。
  - protected_id: PCR-005
    prior_locator: "Data, materials, and existing evidence base > Local RCT evidence and present limits"
    revised_locator: "Data, materials, and existing evidence base > Current resource and evidence status; Local randomized-trial evidence; Research design and methods > Conditional mapping from trial observations and independent alternative; Feasibility, resources, risks, alternatives, and stop conditions > Working assumptions; Limitations and boundary conditions"
    semantic_status: preserved
    evidence: >-
      EXIT-SEP 与 XBJ-SCAP 仍只在阶段 II 成功后的阶段 III 作为条件性个体数据来源，且两项试验分开分析。v022 保留本地材料的项目衍生性质和全部样本及非缺失计数，并明确这些材料不能替代个体数据授权、原始 CRF/SAP、随机化与分析集、中心或分层、实际访视相对随机化和首剂的时序，以及死亡、住院、存活出院和转院语义核验。
  - protected_id: PCR-006
    prior_locator: "Research content and work packages; Research design and methods"
    revised_locator: "Research content and work packages > Work packages and minimum route; Data, materials, and existing evidence base > Variable roles; Research design and methods; Evidence chains"
    semantic_status: preserved
    evidence: >-
      v022 的最低顺序仍是资源与可观测性审计，标签、状态和医院分组锁定，竞争风险、多状态与线性基线，绝对恢复和不当高置信度检查，至多一个复杂候选，两项主要任务和两项次要诊断，冻结，预先隔离的跨数据库检验，最后才进入条件性试验分析。Y_t、A_t、M_t 和标签副本继续分离；只解释满足固定尺度、排列与符号对齐、恢复、外部稳定性和低支持时不输出结论规则的量。
  - protected_id: PCR-007
    prior_locator: "Research content and work packages > Conjunctive minimum success definition; Research design and methods > Hospital-primary genuine cross-database validation"
    revised_locator: "Research content and work packages > Conjunctive minimum success definition; Research design and methods > Hospital-based cross-database validation; Feasibility, resources, risks, alternatives, and stop conditions > Limitations and boundary conditions; Risks, alternatives, and stop conditions"
    semantic_status: preserved
    evidence: >-
      阶段 II 仍须同时满足双库数据支持、绝对恢复、两项主要任务的 proper score 与校准、无未解决高严重度泄漏、预先隔离外部测试中的不更新模型表现、状态对齐和结构符号稳定。数值标准保持为 Brier 差值单侧 95% 上限不超过 +0.01、校准斜率 0.80–1.20、绝对风险误差不超过 0.02、至少 20 个测试医院、状态相关或一致性至少 0.70、符号一致率至少 0.80。仅校准或仅测量模型更新继续与不更新模型分开报告且不能替代其失败；阶段 III 不能补足阶段 II。
  - protected_id: PCR-008
    prior_locator: "Research design and methods > Protocol locks for the two primary clinical tasks; Mutually exclusive post-onset state/event system"
    revised_locator: "Research design and methods > Protocol locks for the two primary clinical tasks; Mutually exclusive post-onset state and event system; Observational target, anchoring and abstention; Research content and work packages > Conjunctive minimum success definition; Required analyses and evidence"
    semantic_status: preserved
    evidence: >-
      v022 完整保留两项任务和双重时间规则：标本先采时抗菌药须在 72 小时内，给药在先时标本须在 24 小时内；无已记录慢性器官功能障碍者基线 SOFA=0，有记录者取入 ICU 前 24 小时最低可计算值；各成分取滚动 24 小时最差值，SOFA 增加至少 2 分须位于感染前 48 小时至后 24 小时，发病取首个可排序时刻。仍从 ICU 第 12 小时起每 12 小时观察，使用此前 12–24 小时的 as-of 历史预测未来 12 小时首次发病；发病后主要终点为第 7 日，第 14 日为敏感性分析。仅首次发病进入主分析，重叠窗口每次住院总权重为 1；延迟进入、互斥状态、竞争终止及患者和医院聚类均未改变。同窗内仍以观察时点前可用特征、[t,t+12h) 新治疗 A_t 和下一边界实测生理值定义顺序，无法排序的同时间戳关系不用于相应转移。泄漏审计仍覆盖发病后信息、尚不可用的培养或抗菌药、同窗未来治疗、未来测量频率、跨组插补或标准化、患者或 ICU 停留跨组、重叠窗口权重及结局决定的变量、时间网格或阈值；高严重度项未清除时不开放最终测试。
  - protected_id: PCR-009
    prior_locator: "Structured abstract; Contribution, innovation, impact, application, and closest-work comparison > Contribution and evidence ladder"
    revised_locator: "Structured abstract > Expected result and Contribution and impact; Data, materials, and existing evidence base > Current resource and evidence status; Contribution, innovation, impact, application, and closest-work comparison > Contribution and evidence levels; Verified representative closest-work comparison; Title and positioning claim-support table"
    semantic_status: preserved
    evidence: >-
      v022 明确模型、模拟恢复、预测、外部测试和试验新分析均尚未生成，摘要中的标签协议、审计、模型诊断、外部结果及试验比较全部是计划产物。贡献仍限定为条件性的整合、验证、基准数据和可复用研究资源；各单项模块已有先例的判断仍为高置信度，完整组合缺口仍仅为低至中等置信度，并明确不主张新算法、全球首次或方法首创。
  - protected_id: PCR-010
    prior_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Resources and governance; Risk and automatic alternative matrix; Remaining execution gates; Identity and final stop boundary"
    revised_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Feasibility and resources; Working assumptions; Limitations and boundary conditions; Risks, alternatives, and stop conditions"
    semantic_status: preserved
    evidence: >-
      v022 第 14 节集中保留访问、数据使用协议、可运行提取、人员承诺、实际数据支持、标签与泄漏、状态恢复、MNAR 与治疗重叠、外部运输、试验授权及语义、共同指标与评分映射、时间节点和最接近工作不确定性。它保留相应触发与后果：月 3、6、12、20、24 的停止或降级；12 小时不足时改为 24 小时或事件时间；恢复或假结构失败时合并、删除或改用简单模型；外部不更新模型失败不得由有限更新改写；试验映射失败改用独立 SOFA，核心语义失败则停止新状态结局；较强新颖性主张须另行检索。其他章节仅保留定义相邻估计目标或操作所需的局部限定，没有削弱第 14 节的权威限制。
  - protected_id: PCR-011
    prior_locator: "Research content and work packages > Twenty-four-month minimum and dated gates; Identity and final stop boundary"
    revised_locator: "Research content and work packages > Twenty-four-month minimum and dated decision points; Conjunctive minimum success definition; Feasibility, resources, risks, alternatives, and stop conditions > Limitations and boundary conditions; Risks, alternatives, and stop conditions"
    semantic_status: preserved
    evidence: >-
      v022 仍把阶段 I–II 定为 24 个月最低交付，并保留月 0–3、4–6、7–12、13–18/20、21–24 和 24 个月后的先后时段。阶段 III 只在阶段 II 成功且试验授权、原始文件与语义、共同指标及映射条件满足后开展；第 14 节明确任何试验结果都不能补足资源、绝对恢复、主要任务、泄漏或外部检验失败，月 24 封存阶段 II。
  - protected_id: PCR-012
    prior_locator: "Research question, objectives, and core hypothesis > Core hypothesis and non-hypotheses; Feasibility, resources, risks, alternatives, and stop conditions"
    revised_locator: "Structured abstract > Contribution and impact; Research design and methods > Observational target, anchoring and abstention; Conditional mapping from trial observations and independent alternative; Feasibility, resources, risks, alternatives, and stop conditions > Limitations and boundary conditions"
    semantic_status: preserved
    evidence: >-
      v022 保留观察性联合分布、预测表现和状态对齐不能识别治疗因果效应、真实反馈网络或反事实策略的边界；条件性试验分析不验证未测潜在状态、连续动力学、转移关系、中介、机制、控制或整个候选模型。它还明确禁止把当前项目称为已验证模型、真实因果网络、数字孪生、可控系统、临床决策工具或药物平台，并保留不支持无条件临床推广的限定。
undeclared_scientific_changes: []
findings: []
unresolved_issues: []
---

# Content-preservation check

## Decision rationale

独立逐项核对 v003 的每个登记位置与 v022 的对应内容后，12 项受保护内容均保持原研究身份、含义、证据状态、条件性和主张强度。v022 对标题、术语、段落顺序和限制条件的位置作了编辑性调整，但未改变研究问题、主要推断单位、数据来源角色、任务定义、数值阈值、时间规则、泄漏防护、外部检验规则或条件性试验分支。revision delta 将本次修订声明为 `scientific_change: false`；该声明与上述独立语义比较一致，未发现未声明的科学变更。

## Protected-content trace

身份锚点保留在 frontmatter，并在研究问题和第 14 节身份边界中再次明确。精确的任务、时间和泄漏规则保留在 `Protocol locks for the two primary clinical tasks`、`Mutually exclusive post-onset state and event system` 及合取成功标准中。恢复、外部测试和试验映射的全部数值标准保留在各自方法小节。原稿分散的资源状态、可恢复性、缺失与重叠、外部运输、试验语义、临床解释及最接近工作限制，被集中到第 14 节；相邻方法段只保留定义估计目标和操作分支所需的局部限定。

## Required routing

判定为 `scientific_content_preserved`。v022 可以进入新的独立叙事与学术语言评估；本检查不评价科学设计是否正确，也不构成后续评估结论。
