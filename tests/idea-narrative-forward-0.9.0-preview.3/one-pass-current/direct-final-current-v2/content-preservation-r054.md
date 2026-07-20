---
schema_version: research-idea-content-preservation-check.v1
check_id: content-preservation-I01-001-r054
review_id: content-preservation-review-I01-001-r054
reviewer_skill: idea-narrative-assessor
reviewer_instance_id: fresh-content-preservation-reviewer-r054
workflow_id: RID-SEPSIS-CSM-20260717-001
round_id: r054
input_artifact_ids:
  - idea-dossier-I01-001-v003
  - idea-dossier-I01-001-v035
  - protected-content-register-I01-001-v003-r003
  - revision-delta-I01-001-v003-to-v035
input_versions: [v003, v035, r003, v035]
inputs:
  prior_dossier:
    artifact_id: idea-dossier-I01-001-v003
    version: v003
    path: tests/idea-test-0.9.0-preview.1/0.9.0-preview.1/03_ideas/nodes/I01-001/dossiers/idea-dossier-v003.md
  revised_dossier:
    artifact_id: idea-dossier-I01-001-v035
    version: v035
    path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v2/idea-dossier-v035.md
  protected_content_register:
    artifact_id: protected-content-register-I01-001-v003-r003
    version: r003
    path: tests/idea-narrative-forward-0.9.0-preview.3/run-001/inputs/protected-content-register-v003.yaml
  revision_delta:
    artifact_id: revision-delta-I01-001-v003-to-v035
    version: v035
    path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v2/revision-delta-v003-to-v035.md
files_read:
  - tests/idea-test-0.9.0-preview.1/0.9.0-preview.1/03_ideas/nodes/I01-001/dossiers/idea-dossier-v003.md
  - tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v2/idea-dossier-v035.md
  - tests/idea-narrative-forward-0.9.0-preview.3/run-001/inputs/protected-content-register-v003.yaml
  - tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v2/revision-delta-v003-to-v035.md
isolation_mode: fresh_subagent
prior_scores_visible: false
source_edits_performed: false
decision: scientific_content_preserved
protected_item_checks:
  - protected_id: PCR-001
    prior_locator: "YAML frontmatter identity_anchor; Research question, objectives, and core hypothesis > Primary research question"
    revised_locator: "YAML frontmatter lines 17-22; title and summary lines 27-32; Primary research question line 70; identity boundary line 471"
    semantic_status: preserved
    evidence: >-
      v035 保留原核心问题、研究对象及患者—时间状态与状态转移推断单位，并在第 32、70 行继续覆盖可比较的发病前在险时段、首次发病、发病后互斥状态和结局；第 471 行明确把取消该连续体或改成普通预测列为必须另建研究构想的身份变化。因此研究身份没有改成泛 ICU 风险分层或普通临床预测。
  - protected_id: PCR-002
    prior_locator: "YAML frontmatter identity_anchor.primary_objective; Research question, objectives, and core hypothesis > Objectives"
    revised_locator: "YAML frontmatter line 19; summary and objective lines 32 and 39; dated stages lines 89-122; positioning lines 34 and 384"
    semantic_status: preserved
    evidence: >-
      v035 第 32、39 行仍以文献和专家先验及两个公共 ICU 数据库为基础，要求在 24 个月内完成候选模型构建、预设生成情景检验和隔离跨数据库验证；第 89-122 行保留阶段 I-II 的顺序和交付，第 34、384 行把贡献限定为证据整合、验证、基准结果和可复用资源，而不是仅产出预测工具。
  - protected_id: PCR-003
    prior_locator: "YAML frontmatter identity_anchor.study_object and primary_unit_of_inference; Research design and methods"
    revised_locator: "YAML frontmatter lines 20 and 22; research question line 70; protocol lines 189-199; observational target lines 220-226; identity boundary line 471"
    semantic_status: preserved
    evidence: >-
      v035 第 70 行保留以脓毒症为中心的纵向发病前在险时段和发病后轨迹，第 189-199 行以患者时间段组织两项主要任务并在第 198 行规定患者和医院聚类，第 220-226 行继续以患者状态、状态占用和状态转移为推断对象；第 471 行再次固定患者—时间状态与转移及两层聚类。
  - protected_id: PCR-004
    prior_locator: "Data, materials, and existing evidence base > Current verified-resource versus prospective-gate status; Public ICU database roles and G1 audit"
    revised_locator: "Current resource and result status lines 126-165; feasibility and resources lines 424-426"
    semantic_status: preserved
    evidence: >-
      v035 第 130-139 行逐项区分数据库存在和版本已核验、团队访问与数据使用协议未核验、双库项目队列和 G1 支持尚未生成、具名人员未核验以及模型和分析结果尚未生成；第 143-145 行仍指定 MIMIC-IV 与 eICU-CRD 为主库、HiRID 或 AmsterdamUMCdb 为预先指定的条件性备份。第 424-426 行再次保留这些未具备状态，没有把资源可行性润色成已取得凭证、可运行提取、人员承诺或结果。
  - protected_id: PCR-005
    prior_locator: "Data, materials, and existing evidence base > Local RCT evidence and present limits"
    revised_locator: "Current resource status lines 133-135; local RCT evidence lines 177-181; pending assumptions line 435; limitations line 446"
    semantic_status: preserved
    evidence: >-
      v035 第 133-135、446 行明确 EXIT-SEP 与 XBJ-SCAP 的本地材料只是衍生清洗或验证报告，不能替代个体数据授权、原始病例报告表和统计分析计划，也未核验随机化、中心、实际访视及生存、住院和出院语义；第 435 行把这些内容连同共同锚点和 R0/R1 结果保留为治疗组比较前必须确认的事项。
  - protected_id: PCR-006
    prior_locator: "Research content and work packages; Research design and methods, including Observational target, anchoring, missingness and abstention"
    revised_locator: "Work packages and execution order lines 112-122; variable roles lines 167-175; observational target and abstention lines 218-226; simulation criteria lines 228-242"
    semantic_status: preserved
    evidence: >-
      v035 第 122 行保留资源与 G1、标签/状态/医院划分、简单基线、预设模拟判定、至多一个复杂候选、两主两次任务、开发设定、隔离外部测试和条件性试验的单向顺序；第 167-175 行分离 Y_t、A_t、M_t、标签和 B。第 222-226 行保留锚定、K≤4、状态模式≤3、1 或 2 个时间段滞后、20 个固定种子及对齐/弃权规则：对齐率<90%、自助抽样保留率<80%、外部符号一致率<80%、状态对齐<0.70 或区间未校准时删除、合并或限定为数据库/政策特异，预测表现不得改变处理。第 230-242 行保留每个核心情景至少 1,000 次或蒙特卡洛标准误≤0.02、全部生成情景、恢复/边检测/零边/错设/校准阈值及各自未达标处理。
  - protected_id: PCR-007
    prior_locator: "Research content and work packages > Conjunctive minimum success definition; Research design and methods > Hospital-primary genuine cross-database validation"
    revised_locator: "Conjunctive cross-database criteria lines 100-110; external split and three analyses lines 244-256; limitations line 445; risk response line 462; final stage boundary line 469"
    semantic_status: preserved
    evidence: >-
      v035 第 102-108 行仍把数据支持、复杂模型的预设模拟判定、两项主要任务的 Brier/proper-score 与校准、无高严重度泄漏，以及不更新参数的隔离外部测试、至少 20 家医院、状态对齐≥0.70 和符号一致率≥0.80 设为合取条件；第 256 行分开不更新参数、仅重新校准和仅更新观测层三种结果。第 445、462 行明定适配后成功不能替代不更新参数的外部测试未达标，第 469 行明定阶段 III 不能补偿阶段 II。
  - protected_id: PCR-008
    prior_locator: "Research design and methods > Protocol locks for the two primary clinical tasks; Mutually exclusive post-onset state/event system"
    revised_locator: "Primary-task protocol lines 185-203; mutually exclusive state/event system lines 205-216"
    semantic_status: preserved
    evidence: >-
      v035 第 189-199 行保留成年首个合格 ICU stay、至少 12 小时可见历史、首次发病与 delayed entry、event/availability 双时间、每 12 小时 landmark、此前最多 24 小时历史、未来 12 小时首次发病、第 7 日主要范围和第 14 日敏感性、竞争终止、Brier/校准及患者与医院聚类。第 190 行完整保留标本先时 72 小时内给药、给药先时 24 小时内采集、基线 SOFA、滚动 24 小时成分、感染前 48 小时至后 24 小时窗口和首个可排序发病时刻；第 193、195 行保留只分析首次发病、每次住院重叠 landmark 总权重为 1、A_t 与下一状态排序及同时间戳无法排序的转移排除。第 201-203 行保留两种标签敏感性和所有未来信息/跨分区泄漏检查，第 207-216 行保留状态互斥、优先级、定义和可用时间。
  - protected_id: PCR-009
    prior_locator: "Structured abstract; Contribution, innovation, impact, application, and closest-work comparison > Contribution and evidence ladder"
    revised_locator: "Positioning lines 34 and 38-42; current-result status line 138; planned outputs lines 352-358; contribution and closest-work lines 382-405; claim-support lines 411-418"
    semantic_status: preserved
    evidence: >-
      v035 第 138 行明确当前没有模型、模拟、恢复、预测、外部测试或 RCT 新分析结果，第 34、384 行只提出条件性的证据整合、验证、基准结果、可复用资源和规范价值。第 399-405 行继续说明各单项模块已有先例且完整组合缺口只有低至中等置信，第 416-418 行把全球或方法“首次”、已形成因果网络、可控系统、数字孪生、临床工具或药物平台列为不受支持的主张；计划工作没有被写成已完成证据。
  - protected_id: PCR-010
    prior_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Resources and governance; Risk and automatic alternative matrix; Remaining execution gates; Identity and final stop boundary; Expected outputs, falsification criteria, and interpretations > Falsification and stop criteria"
    revised_locator: "Feasibility, pending assumptions, limitations, and risk/stop authority location lines 422-469"
    semantic_status: preserved
    evidence: >-
      v035 第 424-437 行集中保留资源、访问、人员承诺、G1 支持、临床尺度到模拟参数映射，以及精确多类别校准估计量、置信界和阈值登记等未解决事项，并保留事件/参数筛选下限不得替代经验有效样本量与模拟稳定性。第 439-451 行集中保留标签不确定性、数据库差异、观察性因果与 MNAR 边界、模拟覆盖限制、隔离外部测试条件、试验授权/语义/稀疏访视、closest-work 和监管限制。第 453-467 行为访问、跨分区患者、泄漏、结构不可恢复、MNAR/重叠、外部测试、RCT 锚点/投影、核心语义、试验不一致或不精确、时间超限及 novelty 外推逐项给出触发条件、替代方案和停止或限缩后果；其中方向不一致或区间过宽时只报告无支持或跨场景适用性有限，不选择亚组补偿总体证据。
  - protected_id: PCR-011
    prior_locator: "Research content and work packages > Twenty-four-month minimum and dated gates; Identity and final stop boundary"
    revised_locator: "Dated stages lines 87-110; final stage boundary line 469"
    semantic_status: preserved
    evidence: >-
      v035 第 89-98 行保留阶段 I-II 的 24 个月最低交付、顺序日期和阶段 III 位于其后的条件；第 469 行明确阶段 III 只有在阶段 II 达到跨数据库判定标准且试验数据、语义和观测联系满足预设条件时才可开展，任何 RCT 结果都不能补偿阶段 II 的资源、模拟判定、主要任务或外部验证未达标，并要求月 24 停止继续调整和保存阶段 II 结果。
  - protected_id: PCR-012
    prior_locator: "Research question, objectives, and core hypothesis > Core hypothesis and non-hypotheses; Feasibility, resources, risks, alternatives, and stop conditions"
    revised_locator: "Observational target line 220; interpretation matrix lines 370-378; limitations lines 443, 448, and 451"
    semantic_status: preserved
    evidence: >-
      v035 第 220 行明定观察性目标不估计 do(A_t)、因果反馈边或反事实策略；第 376-378 行将 RCT 两端点和完整阶段 II 结果的允许解释限制为端点组间差异或候选模型获得规定层面的支持。第 443、448、451 行集中排除真实因果网络、治疗因果效应、反事实策略、未测潜在动力学、转移边、机制、中介、控制、数字孪生、临床决策工具、药物平台和无条件临床推广，并明确条件性 RCT 次要分析不验证整个系统模型。
undeclared_scientific_changes: []
findings: []
unresolved_issues: []
---

# Content-preservation check

## Decision rationale

`scientific_content_preserved`。对 frozen register 的 12 个 `protected_id` 逐项比较 v003 与 v035 后，v035 中均可找到同义、同强度且满足指定 disposition 的正文证据。研究身份、对象、推断单位、资源与结果状态、设计顺序、全部关键数值和时间规则、两项主要任务的协议、外部验证分支、条件性 RCT 分支、失败解释、主张边界、集中限制、未解决方法细节及“后续试验不得补偿阶段 II 未达标”规则均未发生科学改变。revision delta 仅用于确认其未声明科学变更，本判定依据上列 v035 实际文本。

## Protected-content trace

- 研究身份与阶段目标由 v003 的“候选动态系统表征”改用“纵向患者状态与转移候选模型”表述，但 v035 frontmatter、第 32、70、471 行保留相同的发病前—首次发病—发病后—结局连续体、24 个月阶段 I-II、证据基础和推断单位。
- 原分散的状态/行动/观测分离、模拟判定、两项主要任务、跨数据库验证与 RCT 条件分支在 v035 第 167-331 行重排并定义；所有阈值、时间窗、数据分区、失败后处理和不得补偿规则仍可逐项追踪。
- 资源状态、待确认规格、关键限制、风险替代及停止条件集中到 v035 第 422-469 行；局部章节保留的限定仅用于紧邻的设计与解释，不改变第 439-451 行作为全局限制位置的含义或强度。
- RCT 术语改为“投影观测摘要端点”和“独立 SOFA 临床状态端点”，但 R0、固定 SVD 映射、R1 全部阈值、死亡/在院存活/存活出院排序、分试验分析、缺失与多重性处理、独立分支及不支持的主张均保持不变。

## Required routing

v035 的科学内容保全检查通过，可进入新的独立叙事评估和学术语言评估；本报告不判定方法正确性、叙事质量或语言质量。
