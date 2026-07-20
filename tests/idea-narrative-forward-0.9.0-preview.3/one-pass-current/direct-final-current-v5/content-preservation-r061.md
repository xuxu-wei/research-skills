---
schema_version: research-idea-content-preservation-check.v1
check_id: content-preservation-check-I01-001-v003-to-v038-r061
review_id: content-preservation-I01-001-r061
reviewer_skill: idea-narrative-assessor
reviewer_instance_id: fresh-content-preservation-reviewer-r061
workflow_id: RID-SEPSIS-CSM-20260717-001
round_id: r061
input_artifact_ids:
  - idea-dossier-I01-001-v003
  - idea-dossier-I01-001-v038
  - protected-content-register-I01-001-v003-r003
  - revision-delta-I01-001-v003-to-v038
input_versions:
  - v003
  - v038
  - r003
  - v003-to-v038
inputs:
  prior_dossier:
    artifact_id: idea-dossier-I01-001-v003
    version: v003
    path: tests/idea-test-0.9.0-preview.1/0.9.0-preview.1/03_ideas/nodes/I01-001/dossiers/idea-dossier-v003.md
  revised_dossier:
    artifact_id: idea-dossier-I01-001-v038
    version: v038
    path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v5/idea-dossier-v038.md
  protected_content_register:
    artifact_id: protected-content-register-I01-001-v003-r003
    version: r003
    path: tests/idea-narrative-forward-0.9.0-preview.3/run-001/inputs/protected-content-register-v003.yaml
  revision_delta:
    artifact_id: revision-delta-I01-001-v003-to-v038
    version: v003-to-v038
    path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v5/revision-delta-v003-to-v038.md
files_read:
  - tests/idea-test-0.9.0-preview.1/0.9.0-preview.1/03_ideas/nodes/I01-001/dossiers/idea-dossier-v003.md
  - tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v5/idea-dossier-v038.md
  - tests/idea-narrative-forward-0.9.0-preview.3/run-001/inputs/protected-content-register-v003.yaml
  - tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v5/revision-delta-v003-to-v038.md
isolation_mode: fresh_subagent
prior_scores_visible: false
source_edits_performed: false
decision: editorial_scope_violation
protected_item_checks:
  - protected_id: PCR-001
    prior_locator: "YAML frontmatter identity_anchor; Research question, objectives, and core hypothesis > Primary research question; Research design and methods > Mutually exclusive post-onset state/event system"
    revised_locator: "YAML frontmatter identity_anchor; Research question, objectives, and core hypothesis > Primary research question; Research design and methods > Mutually exclusive post-onset state and event system"
    semantic_status: preserved
    evidence: >-
      前后版本的身份锚点逐项一致。v038 的主要问题仍以脓毒症为中心，覆盖未发病在险时段、首次发病、发病后状态演化和结局；互斥状态表仍列出持续脓毒症、生理恢复、恶化或新器官衰竭、活着出 ICU、转院或无法继续观察及死亡，没有把研究缩成普通预测或一般 ICU 风险分层。
  - protected_id: PCR-002
    prior_locator: "YAML frontmatter identity_anchor.primary_objective; Research question, objectives, and core hypothesis > Objectives; Expected outputs, falsification criteria, and interpretations > Planned outputs"
    revised_locator: "YAML frontmatter identity_anchor.primary_objective; Title, summary, audience, and positioning; Research question, objectives, and core hypothesis > Objectives; Expected outputs, falsification criteria, and interpretations > Planned outputs"
    semantic_status: preserved
    evidence: >-
      v038 保留在 24 个月内完成阶段 I–II 的目标，以文献和专家先验约束候选表征，使用 MIMIC-IV 与 eICU-CRD 开展模拟重建、临床任务和跨数据库检验；计划产物末尾明确以高水平学术论文和可审计科学证据为方向，而不是只形成预测工具。
  - protected_id: PCR-003
    prior_locator: "YAML frontmatter identity_anchor.study_object and primary_unit_of_inference; Research design and methods"
    revised_locator: "YAML frontmatter identity_anchor.study_object and primary_unit_of_inference; Research design and methods opening; Protocol specifications for the two primary clinical tasks"
    semantic_status: preserved
    evidence: >-
      研究对象仍为纵向、以脓毒症为中心的 ICU 患者系统，包含可比较的发病前在险时段及发病后轨迹。v038 方法节明确以患者—时间状态和状态转移为主要推断单位，并由患者层与医院层自助法及聚类处理尊重两级相关性。
  - protected_id: PCR-004
    prior_locator: "Data, materials, and existing evidence base > Current verified-resource versus prospective-gate status; Public ICU database roles and G1 audit"
    revised_locator: "Data, materials, and existing evidence base > Current resource and evidence status; Public ICU database roles and G1 observability audit; Feasibility, resources, risks, alternatives, and stop conditions > 可行性与资源"
    semantic_status: preserved
    evidence: >-
      v038 仍把 MIMIC-IV v3.1 与 eICU-CRD v2.0 作为两个主要公共数据库，并只允许在月 0–3 预先指定 HiRID 或 AmsterdamUMCdb 作为备选。公开存在与版本有资料支持，但团队访问资格、数据使用协议、存储、可运行提取、确切校验和、项目人群支持、具名人员和工时均为尚未核验，模型、模拟和跨数据库结果为尚未生成；这些状态没有被写成已经具备。
  - protected_id: PCR-005
    prior_locator: "Data, materials, and existing evidence base > Local RCT evidence and present limits"
    revised_locator: "Data, materials, and existing evidence base > Current resource and evidence status; Local randomized-trial evidence and present limits; Feasibility, resources, risks, alternatives, and stop conditions > 可行性与资源"
    semantic_status: preserved
    evidence: >-
      EXIT-SEP 与 XBJ-SCAP 在 v038 中仍只是位于 24 个月后、条件性可用的阶段 III 数据来源。本地材料仍明确为项目内衍生清洗或验证报告；个体数据授权、原始病例报告表和统计分析计划、随机化与中心、实际访视相对首剂时序，以及死亡、住院、出院和转院语义均须另行核验，衍生报告不能替代这些证据。
  - protected_id: PCR-006
    prior_locator: "Research content and work packages; Research design and methods, including Observational target, anchoring and abstention and Absolute simulation and semi-synthetic recovery gate"
    revised_locator: "Research content and work packages > Work packages and minimum route; Research design and methods > Observational target, anchoring, missingness, and evidence-based non-interpretation; Simulation and semi-synthetic reconstruction criteria under known generating mechanisms"
    semantic_status: preserved
    evidence: >-
      v038 固定顺序仍为资源与可观测性审计、标签/状态/医院分配锁定、简单基线、已知生成机制下的模拟重建和错误结构支持检查、至多一个复杂候选模型、两项主要任务与两项次要表征诊断、开发冻结、跨数据库最终检验，随后才可能进入试验分析。Y_t、A_t 与 M_t 继续分离。状态或边的 20 个种子对齐率低于 90%、自助法保留率低于 80%、外部符号一致率低于 80%、状态对齐低于 0.70 或区间未校准时，仍须删除、合并或限为特定数据库/照护政策解释；预测表现不能改变该处理。模拟部分还保留至少 1,000 次或 Monte Carlo 标准误不超过 0.02，以及状态、转移、边、零边和错设情景的全部数值标准和相应停止处理。
  - protected_id: PCR-007
    prior_locator: "Research content and work packages > Conjunctive minimum success definition; Research design and methods > Hospital-primary genuine cross-database validation"
    revised_locator: "Research content and work packages > Conjunctive minimum success definition; Research design and methods > Hospital-primary cross-database external validation; Expected outputs, falsification criteria, and interpretations > Falsification criteria"
    semantic_status: preserved
    evidence: >-
      阶段 II 在 v038 中仍要求数据支持、正确/零边/错设情景的模拟重建、两项主要任务的 Brier 或多类别 Brier 与校准、高严重度泄漏清零、不更新任何模型参数的跨数据库表现、状态对齐和结构符号一致性同时达到标准。主要数值仍为 Brier 差值上侧 95% 界不超过 +0.01、校准斜率 0.80–1.20、绝对风险误差不超过 0.02、最终检验医院至少 20 家、状态对齐至少 0.70 和符号一致率至少 0.80。两种适配医院集参数重估与不更新参数的结果分开报告，适配改善不能替代前者失败；阶段 III 明确不计入阶段 II 的合取结果。
  - protected_id: PCR-008
    prior_locator: "Research design and methods > Protocol locks for the two primary clinical tasks; Mutually exclusive post-onset state/event system"
    revised_locator: "Research design and methods > Protocol specifications for the two primary clinical tasks; Mutually exclusive post-onset state and event system"
    semantic_status: preserved
    evidence: >-
      v038 保留全部协议承诺：标本先于抗菌药时为 72 小时内、给药先时为 24 小时内；无慢性器官障碍记录者基线 SOFA 为 0，有记录者取入 ICU 前 24 小时最低可计算值；SOFA 成分滚动 24 小时取最差，相对基线增加至少 2 分且位于感染前 48 小时至后 24 小时，取首次可排序发病时刻。仍只分析首次发病，重叠界标在每个 ICU 住院段内总权重为 1；保留延迟进入、互斥状态、竞争终止、严格的当时可见特征约束、同窗 A_t 与下一状态顺序及无法排序同时间戳记录的排除。两项主要任务、校准与严格适当概率评分、患者和医院聚类不确定性也未变；泄漏检查仍覆盖同窗治疗、未来测量频率、重复住院或跨集合记录，以及结局驱动的变量、时间方案或阈值。
  - protected_id: PCR-009
    prior_locator: "Structured abstract; Contribution, innovation, impact, application, and closest-work comparison > Contribution and evidence ladder"
    revised_locator: "Structured abstract; Data, materials, and existing evidence base > Current resource and evidence status; Contribution, innovation, impact, application, and closest-work comparison > Contribution and evidence ladder and 已核验的代表性最接近工作比较; Title and positioning claim-support table"
    semantic_status: preserved
    evidence: >-
      v038 继续把候选模型、模拟重建、主要任务、跨数据库最终检验和试验新分析列为尚未生成。贡献仅在未来条件满足时成为证据整合、验证、可复用基准和研究资源；各模块已有先例，完整组合的负向检索结论仅为低至中等置信度。新算法、全球首次和已经完成的验证均被明确列为无支持或禁止的主张。
  - protected_id: PCR-010
    prior_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Resources and governance; Risk and automatic alternative matrix; Remaining execution gates; Identity and final stop boundary; Expected outputs, falsification criteria, and interpretations > Falsification and stop criteria"
    revised_locator: "Feasibility, resources, risks, alternatives, and stop conditions > 可行性与资源; 限制与适用边界; 工作假设、尚待确定的规范与执行要求; 风险、替代与停止条件; 研究身份与最终停止边界"
    semantic_status: unclear
    evidence: >-
      第 14 节集中保留了访问与人员、G1、时间和泄漏、模拟重建、非随机缺失和低支持度、不更新参数的跨数据库检验、日期、试验授权与语义、共同锚点与投影、最接近工作置信度，以及临床尺度到模拟参数映射、多类别校准估计量/置信界/登记格式和经验有效样本量等未决事项。风险表也保留了投影不满足时改作独立临床状态分析以及方向不一致或区间过宽时不得选择亚组改变结论。然而同节最后的全局边界又说只有实际访视变量能够形成一维投影摘要时才开展阶段 III，与前述失败替代相冲突，因此该权威位置不能给出唯一的阶段 III 失败处置含义。
  - protected_id: PCR-011
    prior_locator: "Research content and work packages > Twenty-four-month minimum and dated gates; Research design and methods > Conditional trial-observation projection and independent fallback; Feasibility, resources, risks, alternatives, and stop conditions > Identity and final stop boundary"
    revised_locator: "Research content and work packages > Twenty-four-month minimum and dated decision points; Research design and methods > 随机对照试验语义、确定性投影与独立临床状态分析; Feasibility, resources, risks, alternatives, and stop conditions > 研究身份与最终停止边界"
    semantic_status: changed
    evidence: >-
      24 个月阶段 I–II 时限、阶段 III 位于最低交付之外，以及任何试验结果都不能抵消资源、模拟重建、主要任务或跨数据库检验未满足项目，均已保留。但 v003 和 v038 的试验技术小节都规定：阶段 II 成功且核心试验语义可核验后，若共同锚点或 R1 不满足，则仍开展独立临床状态分析。v038 第 14 节最终边界却把整个阶段 III 限定为“实际访视变量能够按阶段 II 观测方程形成一维投影摘要时开展”，从而在全局权威位置排除了同稿预设的投影失败分支。这不是同义改写。
  - protected_id: PCR-012
    prior_locator: "Research question, objectives, and core hypothesis > Core hypothesis and non-hypotheses; Feasibility, resources, risks, alternatives, and stop conditions"
    revised_locator: "Research question, objectives, and core hypothesis > Core hypothesis and non-hypotheses; Expected outputs, falsification criteria, and interpretations > Interpretation matrix; Feasibility, resources, risks, alternatives, and stop conditions > 限制与适用边界"
    semantic_status: preserved
    evidence: >-
      v038 明确限制观察性目标，不据此识别治疗因果作用、真实反馈网络、反事实政策、机制、中介或个体控制；随机对照试验分析也不能验证未测潜在动力学、转移边、完整观测模型、候选表征及其模型实现或控制规律。当前计划仍不得表述为已验证模型、临床决策工具、药物平台、数字孪生或无条件临床推广依据。
undeclared_scientific_changes:
  - >-
    v038 在第 14 节“研究身份与最终停止边界”把阶段 III 的启动条件收窄为实际访视变量能够形成一维投影摘要，因而与原稿及同稿技术规范所保留的“投影不成立但核心试验语义可核验时开展独立临床状态分析”分支冲突；revision delta 将 v038 声明为纯编辑修改，没有声明这一科学条件变化。
findings:
  - finding_id: PRES-R061-001
    category: assumptions_limitations_and_contingencies
    severity: major
    protected_ids:
      - PCR-010
      - PCR-011
    prior_locator: "Research design and methods > Conditional trial-observation projection and independent fallback; Feasibility, resources, risks, alternatives, and stop conditions > Identity and final stop boundary"
    revised_locator: "Feasibility, resources, risks, alternatives, and stop conditions > 研究身份与最终停止边界"
    observed_change: >-
      最终全局边界新增“实际访视变量能够按阶段 II 观测方程形成一维投影摘要时才开展阶段 III”的成功条件。
    scientific_effect: >-
      该条件排除了原先在共同锚点或 R1 不满足、但 SOFA 与核心试验语义仍可核验时预定的独立临床状态分析，并与 v038 自身技术小节和风险表冲突。读者无法确定投影失败究竟触发独立分析还是终止整个阶段 III。
    required_resolution: >-
      使第 14 节最终边界与技术规范一致：阶段 II 成功和核心试验数据/语义是两条试验分支的共同前提；只有一维投影摘要分支要求 R0/R1 成立，投影条件不满足时按预定规则进入独立临床状态分析；核心语义失败才停止新状态端点。修订后须由新的独立实例重新作内容保存核查。
unresolved_issues:
  - PRES-R061-001 remains unresolved in idea-dossier-I01-001-v038.
---

# Content-preservation check

## Decision rationale

独立逐项比较显示，研究身份、24 个月阶段 I–II 目标、研究对象和推断单位、数据与资源状态、两项主要任务、全部数值与时间标准、跨数据库检验顺序、不得用适配结果或试验结果补偿前序失败的规则、证据强度和不支持的主张类别均在 v038 正文中可追踪。PCR-001 至 PCR-009 及 PCR-012 保持原义。

但是，v038 在第 14 节的最终全局边界新增了一个与原稿和同稿技术规范不一致的阶段 III 资格条件：它要求实际访视变量能够形成一维投影摘要后才开展阶段 III，而原设计在投影条件不满足但核心试验语义可核验时仍开展独立临床状态分析。该差异没有在 revision delta 中声明为科学变更，且改变了预设失败分支。因此判定为 `editorial_scope_violation`，而不是研究身份漂移或已声明的科学变更。

## Protected-content trace

v038 将资源与证据状态统一到数据材料节和第 14 节，将数值性方法标准集中到方法节，并把全局限制、未决规范、风险、替代与停止条件集中到第 14 节。除上述阶段 III 最终边界冲突外，这些移动和合并均保留了原数值、时间、失败解释和主张强度。

需要修正的唯一实质点位于 `Feasibility, resources, risks, alternatives, and stop conditions > 研究身份与最终停止边界`。应把两条试验分支的共同前提与一维投影分支特有的 R0/R1 条件分开，并明确共同锚点或 R1 不满足时的独立临床状态分析仍然存在；只有核心试验语义失败时才停止新状态端点。

## Required routing

v038 目前不能直接进入新的叙事与语言评估。应先修正第 14 节的阶段 III 最终边界，使其与冻结的失败分支一致，并在正文发生实质修改后交由新的独立内容保存核查实例重新评估。
