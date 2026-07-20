---
schema_version: research-idea-content-preservation-check.v1
check_id: content-preservation-check-I01-001-r028
review_id: content-preservation-r028
reviewer_skill: idea-narrative-assessor
reviewer_instance_id: fresh-preservation-r028b
workflow_id: RID-SEPSIS-CSM-20260717-001
round_id: r028
input_artifact_ids:
  - idea-dossier-I01-001-v003
  - idea-dossier-I01-001-v023
  - protected-content-register-I01-001-v003
  - revision-delta-I01-001-v003-to-v023
input_versions:
  - v003
  - v023
  - v003
  - v003-to-v023
inputs:
  prior_dossier:
    artifact_id: idea-dossier-I01-001-v003
    version: v003
    path: tests/idea-test-0.9.0-preview.1/0.9.0-preview.1/03_ideas/nodes/I01-001/dossiers/idea-dossier-v003.md
  revised_dossier:
    artifact_id: idea-dossier-I01-001-v023
    version: v023
    path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/revised/idea-dossier-v023.md
  protected_content_register:
    artifact_id: protected-content-register-I01-001-v003
    version: v003
    path: tests/idea-narrative-forward-0.9.0-preview.3/run-001/inputs/protected-content-register.yaml
  revision_delta:
    artifact_id: revision-delta-I01-001-v003-to-v023
    version: v003-to-v023
    path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/revised/revision-delta-v003-to-v023.md
files_read:
  - tests/idea-test-0.9.0-preview.1/0.9.0-preview.1/03_ideas/nodes/I01-001/dossiers/idea-dossier-v003.md
  - tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/revised/idea-dossier-v023.md
  - tests/idea-narrative-forward-0.9.0-preview.3/run-001/inputs/protected-content-register.yaml
  - tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/revised/revision-delta-v003-to-v023.md
isolation_mode: fresh_subagent
prior_scores_visible: false
source_edits_performed: false
decision: editorial_scope_violation
protected_item_checks:
  - protected_id: PCR-001
    prior_locator: "YAML frontmatter > identity_anchor; Research question, objectives, and core hypothesis > Primary research question"
    revised_locator: "YAML frontmatter > identity_anchor; Research question, objectives, and core hypothesis > Primary research question; Feasibility, resources, risks, alternatives, and stop conditions > Identity boundary"
    semantic_status: preserved
    evidence: >-
      前后版本的五项 identity_anchor 值逐项相同。修订版的主要问题和身份边界仍以知识约束、量化不确定性的脓毒症候选动态系统表征为中心，覆盖可比较的发病前在险时段、首次发病、发病后持续脓毒症、生理恢复、恶化或新器官衰竭、活着离开 ICU、转院及死亡；并明确普通预测或通用 ICU 风险分层不构成该研究身份。
  - protected_id: PCR-002
    prior_locator: "YAML frontmatter > identity_anchor.primary_objective; Research question, objectives, and core hypothesis > Objectives"
    revised_locator: "YAML frontmatter > identity_anchor.primary_objective; Research question, objectives, and core hypothesis > Objectives; Research content and work packages > Twenty-four-month minimum and dated milestones"
    semantic_status: preserved
    evidence: >-
      primary_objective 原样保留阶段 II 在 24 个月内完成。四项目标仍包括可追溯标签与双时钟、双数据库审计约束的状态表征、预设生成场景中的恢复与伪结构控制、未参与开发数据库的独立检验，以及条件性试验再分析；文献和专家知识、公共 ICU 数据、系统辨识职责、可审计证据、可复用基准和高水平论文方向均被保留，未把交付缩减为预测工具。
  - protected_id: PCR-003
    prior_locator: "YAML frontmatter > identity_anchor.study_object and identity_anchor.primary_unit_of_inference; Research design and methods"
    revised_locator: "YAML frontmatter > identity_anchor.study_object and identity_anchor.primary_unit_of_inference; Research design and methods > Prespecified protocol for the two primary clinical tasks; Observational estimand, anchoring, missingness, and support"
    semantic_status: preserved
    evidence: >-
      研究对象和主要推断单位在前后 frontmatter 中逐字相同。修订版仍以纵向、脓毒症为中心的 ICU 患者系统为对象，同时纳入未发病在险时段和发病后轨迹；两项临床任务、状态占用和转移均以患者—时间状态及状态转移为单位，并保留患者层与医院层聚类自助法、不让患者跨数据拆分及患者总权重约束。
  - protected_id: PCR-004
    prior_locator: "Data, materials, and existing evidence base > Current verified-resource versus prospective-gate status; Public ICU database roles and G1 audit"
    revised_locator: "Data, materials, and existing evidence base > Current resource and evidence status; Public ICU database roles and observability audit; Feasibility, resources, risks, alternatives, and stop conditions > Feasibility and resources"
    semantic_status: preserved
    evidence: >-
      文献和专家先验、MIMIC-IV v3.1 与 eICU-CRD v2.0 的主要角色以及 HiRID 或 AmsterdamUMCdb 的预先指定条件性备份均保留。修订版只把数据库存在与版本列为已核验；团队凭证、数据使用协议、下载与可运行提取、确切版本和校验和、G1 队列与事件支持、具名人员和工时仍为尚未核验，模型、模拟恢复、预测、外部测试和新试验分析仍为尚未生成，没有把计划资源或结果改写成现有能力或证据。
  - protected_id: PCR-005
    prior_locator: "Data, materials, and existing evidence base > Local RCT evidence and present limits"
    revised_locator: "Data, materials, and existing evidence base > Current resource and evidence status; Available local evidence for the two randomized trials; Feasibility, resources, risks, alternatives, and stop conditions > Working assumptions and specifications still to be frozen; Limitations and boundary conditions"
    semantic_status: preserved
    evidence: >-
      EXIT-SEP 与 XBJ-SCAP 仍只作为阶段 III 的条件性个体级试验来源。修订版完整保留 EXIT-SEP 的 1,817、1,760、395、57、SOFA 1,750/1,542/1,296 和乳酸 855 至 223，以及 XBJ-SCAP 的 710、675、617、671、658、SOFA 703/628/610、WBC 704/634/614、CRP 579/503/467 和 28 日状态 675 等计数，同时继续把本地材料限定为衍生清洗或质量控制证据；个体数据授权、原始病例报告表或统计分析计划、随机化、中心、访视时序以及生存、住院、出院和转院语义仍须由原始资料核验。
  - protected_id: PCR-006
    prior_locator: "Research content and work packages; Research design and methods"
    revised_locator: "Research content and work packages > Work packages and fixed sequence; Research design and methods > Candidate variable-role separation; Simulation recovery and false-structure control using prespecified thresholds; Hospital-primary independent cross-database validation; Conditional trial observation mapping and independent alternative analysis"
    semantic_status: preserved
    evidence: >-
      固定顺序仍为资源与 G1 审计、标签/状态/医院拆分、竞争风险与多状态基线、线性状态空间模型、模拟恢复与伪结构控制、至多一个复杂候选、两项主要任务与两项次要诊断、开发冻结、独立保留外部检验，最后才是条件性试验分析。生理测量 Y_t、治疗行动 A_t、测量过程 M_t、标签和基线 B 继续分离；只解释锚定和多随机种子对齐后得到支持的状态占用、转移、锚点预测及预设符号或滞后，并以恢复、区间校准、外部运输和数据支持不足触发合并、删除、降级或弃权。
  - protected_id: PCR-007
    prior_locator: "Research content and work packages > Conjunctive minimum success definition; Research design and methods > Hospital-primary genuine cross-database validation"
    revised_locator: "Research content and work packages > Conjunctive minimum success definition; Research design and methods > Hospital-primary independent cross-database validation; Feasibility, resources, risks, alternatives, and stop conditions > Risks, alternatives, and stop conditions"
    semantic_status: preserved
    evidence: >-
      阶段 II 的五项合取条件均保留：两库队列及事件、转移、医院和锚点支持；复杂候选在正确、零边和错设场景中的全部阈值；两项主要任务 Brier 差值上侧 95% 界不超过 +0.01、校准斜率 0.80–1.20、绝对风险误差不超过 0.02；高严重度泄漏清零；以及至少 20 个最终测试医院、不更新检验、状态对齐至少 0.70 和结构符号一致率至少 0.80。修订版也保留适配区学得的校准或观测模型更新与不更新结果分开、完整重拟合只属更新或开发、更新成功不能替代不更新失败，以及阶段 III 不能改变或补足阶段 II 判定。
  - protected_id: PCR-008
    prior_locator: "Research design and methods > Protocol locks for the two primary clinical tasks; Mutually exclusive post-onset state/event system"
    revised_locator: "Research design and methods > Prespecified protocol for the two primary clinical tasks; Mutually exclusive post-onset state and event system; Observational estimand, anchoring, missingness, and support; Conditional trial observation mapping and independent alternative analysis; Feasibility, resources, risks, alternatives, and stop conditions > Risks, alternatives, and stop conditions"
    semantic_status: preserved
    evidence: >-
      两项主要任务的完整协议仍可逐项追踪：临床事件与信息可用双时钟；标本先发生时抗菌药须在其后 72 小时内、抗菌药先发生时标本须在其后 24 小时内；基线 SOFA=0 或取入 ICU 前 24 小时最低可计算值；滚动 24 小时窗取最差组件，感染前 48 小时至后 24 小时内相对基线增加至少 2 分，并取首个可排序满足时刻。修订版继续只分析首次发病，重叠界标窗口的单次 ICU 住院总权重为 1；采用 12 小时界标、最多 24 小时历史和未来 12 小时首次发病 CIF，第 7 日有利状态占用为发病后主要估计对象，第 14 日为敏感性分析。死亡、转院、活着离开 ICU、恶化或新器官衰竭、生理恢复和持续脓毒症保持互斥及原优先顺序；同一时间格先定义 A_t 再定义下一状态，无法排序的同时间戳转移被排除。泄漏检查仍覆盖同时间格未来行动、未来测量频率、重复患者或住院跨集合、跨拆分处理及结局驱动的变量、时间格或阈值。锚点密度 30%、医院覆盖 70%、患者覆盖 80%、K 不超过 4、状态体制不超过 3、1 或 2 个时间格滞后、至少 1,000 次重复或 MCSE 不超过 0.02、ARI 或典型相关至少 0.80、转移 MAE 不超过 0.05、覆盖率 0.90–0.98、边灵敏度至少 0.80、FDR 不超过 0.10、零边误判不超过 0.05、错设识别至少 80%、高置信错误结构不超过 0.05、行动比例 5%–95% 与加权 ESS 至少为名义样本 20% 等数值均保留。外部医院 30%/70% 划分、固定种子 20260717、跨分区患者排除及 10% 支持边界仍在。试验 R0/R1 的至少两个锚点、第一奇异轴能量至少 50%、相关至少 0.70、NMAE 不超过 0.50、截距不超过 0.20 个标准差、斜率 0.80–1.20、覆盖率 0.90–0.98、锚点校准和 80% 范围内与 60% 可计算访视要求亦逐项保留；投影失败仍自动转入与阶段 II 独立的死亡分层 SOFA 分支。
  - protected_id: PCR-009
    prior_locator: "Structured abstract > Background and gap; Contribution, innovation, impact, application, and closest-work comparison > Contribution and evidence ladder; Verified representative closest-work comparison"
    revised_locator: "Structured abstract > Background and gap; Contribution, innovation, impact, application, and closest-work comparison > Contribution and evidence ladder; Representative closest-work comparison; Title and positioning claim-support table"
    semantic_status: changed
    evidence: >-
      计划性证据状态、尚无模型或结果、条件性整合/验证/基准/资源贡献、各模块已有先例、不主张新算法或全球首次等内容均保留，详细 closest-work 部分也继续把完整组合缺口限定为截至 2026-07-17 的有界检索结论和低至中等置信。然而，原摘要只陈述“有界检索在低至中等置信度下未建立一个已发表代表性架构，并不证明全球不存在”；修订摘要改为“既有研究……却仍缺少……连贯证据”，删除了有界检索、已发表代表性架构、低至中等置信和不证明全球不存在四项限定。后文恢复这些限定不能消除摘要本身形成的更强文献缺口主张，因此该保护项的主张强度发生未申明变化。
  - protected_id: PCR-010
    prior_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Resources and governance; Risk and automatic alternative matrix; Remaining execution gates; Identity and final stop boundary"
    revised_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Feasibility and resources; Working assumptions and specifications still to be frozen; Limitations and boundary conditions; Risks, alternatives, and stop conditions; Identity boundary"
    semantic_status: preserved
    evidence: >-
      第 14 节仍是完整限制与停止逻辑的唯一权威位置，并集中保留资源和访问、具名团队与数据保管、G1 数据支持、标签和泄漏、状态可恢复性与伪结构、非随机缺失和行动重叠、独立外部运输、时间节点、试验授权与语义、共同锚点与投影，以及最接近工作不确定性。九项尚待冻结的选择和十项风险表覆盖原有触发条件、允许替代方案及停止或降级结果，包括 20 个医院、每个外部自由参数 10 个事件或转移、70% 医院与 80% 患者锚点覆盖、跨分区排除超过 10%、行动比例 5%–95%、加权 ESS 20%、月 12/20/24 节点和试验资料语义失败等界限；其他章节仅保留与局部估计对象、分析分支、证伪解释或主张范围直接相连的最小边界。
  - protected_id: PCR-011
    prior_locator: "Research content and work packages > Twenty-four-month minimum and dated gates; Feasibility, resources, risks, alternatives, and stop conditions > Identity and final stop boundary"
    revised_locator: "Research content and work packages > Twenty-four-month minimum and dated milestones; Feasibility, resources, risks, alternatives, and stop conditions > Working assumptions and specifications still to be frozen; Risks, alternatives, and stop conditions; Identity boundary"
    semantic_status: preserved
    evidence: >-
      阶段 I–II 必须在 24 个月内完成，月 0–3、4–6、7–12、13–18/20 和 21–24 的时序与冻结关系均保留；阶段 III 明确位于 24 个月最低交付之后，且只有阶段 II 完成、个体级试验资料和语义合格、观测映射满足预设要求后才能启动。月 24 无独立保留外部结果仍判阶段 II 最低端点未完成；阶段 III 不改变该判定，也不能绕过资源、恢复、两项主要任务或独立外部检验要求。
  - protected_id: PCR-012
    prior_locator: "Research question, objectives, and core hypothesis > Core hypothesis and non-hypotheses; Feasibility, resources, risks, alternatives, and stop conditions"
    revised_locator: "Research design and methods > Observational estimand, anchoring, missingness, and support; Contribution, innovation, impact, application, and closest-work comparison > Title and positioning claim-support table; Feasibility, resources, risks, alternatives, and stop conditions > Limitations and boundary conditions"
    semantic_status: preserved
    evidence: >-
      修订版继续把观察性估计对象限定为实际照护与测量政策下的联合预测和生成分布，明确不包含 do(A_t) 干预效应或反事实策略。第 14 节完整保留观察性数据、预测表现与联合建模不能支持真实因果网络、治疗因果效应、机制、中介、控制或数字孪生主张；条件性试验再分析也只支持实际访视投影摘要或独立临床状态的随机化组间差异，不能验证未测潜在动力学、转移边、潜在靶点、观测模型外结构或整个候选系统。已验证模型、临床决策工具、药物平台、全球首次和无条件临床推广仍明确列为当前不受支持的主张。
undeclared_scientific_changes:
  - change_id: USC-R028-001
    protected_id: PCR-009
    change_type: strengthened_closest_work_gap_claim
    prior_scope: >-
      截至 2026-07-17 的有界检索只在低至中等置信度下未建立一个已发表的完整代表性架构，且不能证明全球不存在相近工作。
    revised_scope: >-
      修订版结构化摘要无条件陈述既有研究仍缺少该连贯证据，未在该陈述中保留有界检索、代表性已发表工作、低至中等置信或非全球不存在性限定。
    declaration_status: not_declared_in_revision_delta
findings:
  - finding_id: CPS-R028-001
    protected_id: PCR-009
    category: claim_strength
    finding: >-
      结构化摘要将受有界检索和低至中等置信约束的负向最接近工作结论改写成无限定的证据缺口陈述，强于源摘要。详细正文中的后置限定不能修正摘要读者已经接收到的更强主张。
    required_disposition: >-
      将摘要的文献缺口陈述恢复到与源文件相同的有界检索、置信水平和非全球不存在性范围，然后由新的独立审阅者重新执行内容保全检查。
unresolved_issues: []
---

# Content-preservation check

## Decision rationale

决定为 `editorial_scope_violation`。研究身份没有漂移，修订说明也明确声明没有科学变更；两份完整 dossier 的逐项比较表明，研究对象、两项主要估计对象、协议时钟、全部数值和时间阈值、外部检验隔离、条件性试验分支、证据状态、可行性发现、限制和停止条件均可在修订版中追踪到相同含义。唯一未通过项是 PCR-009：修订版结构化摘要删除了原负向最接近工作结论的有界检索、低至中等置信和非全球不存在性限定，形成未在 revision delta 中申明的主张强化。该变化不改变研究身份，因此不属于 `identity_drift_detected`；revision delta 又明确写明 `scientific_change_declared: false`，因此不属于 `scientific_change_declared`。

## Protected-content trace

- PCR-001 至 PCR-008、PCR-010 至 PCR-012 均保持原含义、证据状态和条件性。技术细节虽然从重复位置合并至方法或第 14 节，但所有关键参数、估计对象、门槛和失败后果仍有可识别的新位置。
- PCR-009 的计划性结果状态、条件性贡献、模块已有先例和“不主张新算法或全球首次”边界在详细正文中保留；问题仅位于 `Structured abstract > Background and gap` 的更强负向文献缺口表述。
- revision delta 把此次工作声明为纯编辑修复，并声明主张强度未变；它没有申明上述摘要级强化。

## Required routing

当前 dossier 不得直接进入新的叙事与学术语言评估。应先把结构化摘要中的最接近工作缺口主张恢复为源文件的有界检索、低至中等置信和非全球不存在性范围，保留其余已核验内容不变；修订后须由新的独立审阅者重新进行内容保全检查，再决定后续评估路线。
