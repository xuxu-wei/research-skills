---
schema_version: research-idea-content-preservation-check.v1
check_id: "content-preservation-I01-001-r070"
review_id: "content-preservation-review-I01-001-r070"
reviewer_skill: idea-narrative-assessor
reviewer_instance_id: "fresh-content-preservation-verifier-r070"
workflow_id: "RID-SEPSIS-CSM-20260717-001"
round_id: "r070"
input_artifact_ids:
  - "idea-dossier-I01-001-v003"
  - "idea-dossier-I01-001-v043"
  - "protected-content-register-I01-001-v003-r003"
  - "revision-delta-I01-001-v003-to-v043"
input_versions: ["v003", "v043", "r003", "v043"]
inputs:
  prior_dossier:
    artifact_id: "idea-dossier-I01-001-v003"
    version: "v003"
    path: "tests/idea-test-0.9.0-preview.1/0.9.0-preview.1/03_ideas/nodes/I01-001/dossiers/idea-dossier-v003.md"
  revised_dossier:
    artifact_id: "idea-dossier-I01-001-v043"
    version: "v043"
    path: "tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v9/idea-dossier-v043.md"
  protected_content_register:
    artifact_id: "protected-content-register-I01-001-v003-r003"
    version: "r003"
    path: "tests/idea-narrative-forward-0.9.0-preview.3/run-001/inputs/protected-content-register-v003.yaml"
  revision_delta:
    artifact_id: "revision-delta-I01-001-v003-to-v043"
    version: "v043"
    path: "tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v9/revision-delta-v003-to-v043.md"
files_read:
  - "tests/idea-test-0.9.0-preview.1/0.9.0-preview.1/03_ideas/nodes/I01-001/dossiers/idea-dossier-v003.md"
  - "tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v9/idea-dossier-v043.md"
  - "tests/idea-narrative-forward-0.9.0-preview.3/run-001/inputs/protected-content-register-v003.yaml"
  - "tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v9/revision-delta-v003-to-v043.md"
  - "research-skills-openai/skills/idea-narrative-assessor/SKILL.md"
  - "research-skills-openai/skills/idea-narrative-assessor/references/content-preservation-contract.md"
  - "research-skills-openai/skills/idea-narrative-assessor/templates/content-preservation-check.md"
  - "research-skills-openai/skills/idea-narrative-assessor/templates/protected-content-register.yaml"
isolation_mode: fresh_subagent
prior_scores_visible: false
source_edits_performed: false
decision: scientific_content_preserved
protected_item_checks:
  - protected_id: PCR-001
    prior_locator: "YAML frontmatter identity_anchor; Research question, objectives, and core hypothesis > Primary research question"
    revised_locator: "YAML frontmatter identity_anchor; Research question, objectives, and core hypothesis > Primary research question; Feasibility, resources, risks, alternatives, and stop conditions 末段研究构想身份边界"
    semantic_status: preserved
    evidence: >-
      v043 的 identity_anchor 保留同一核心问题、研究对象和推断单位；主问题仍逐项覆盖可比的发病前在险时段、首次发病、发病后状态演化和结局，并把模拟重建及跨数据库检验置于普通预测之上。末段明确规定，取消该连续范围或把研究收缩为普通预测时须作为新的研究构想处理。
  - protected_id: PCR-002
    prior_locator: "YAML frontmatter identity_anchor.primary_objective; Research question, objectives, and core hypothesis > Objectives; frozen register source_context_locator authorization"
    revised_locator: "Title, summary, audience, and positioning > One-sentence complete-Idea summary and Positioning and contribution frame; Research content and work packages > 二十四个月主体计划与日期节点; Expected outputs, falsification criteria, and interpretations > 计划产物"
    semantic_status: preserved
    evidence: >-
      v043 明确把阶段 I–II 规定为 24 个月主体研究，以文献和专家先验、MIMIC-IV 与 eICU-CRD 构建候选表征并完成模拟和跨数据库检验；定位段直接保留“高水平论文和可审计科学证据”的交付方向以及“不得收缩为只产出一个预测工具”的边界，计划产物另列完整科学叙事、协议、代码、审计、基准和资源。高水平论文与非单一预测器要求属于冻结 register 已授权的恢复内容。
  - protected_id: PCR-003
    prior_locator: "YAML frontmatter identity_anchor.study_object and primary_unit_of_inference; Research design and methods"
    revised_locator: "YAML frontmatter identity_anchor.study_object and primary_unit_of_inference; Title, summary, audience, and positioning > One-sentence complete-Idea summary; Research design and methods 开篇"
    semantic_status: preserved
    evidence: >-
      v043 仍以纵向、脓毒症为中心的 ICU 患者系统为对象，包含可比的未发病在险时段和发病后轨迹；正文明确主要推断单位为患者—时间状态及状态转移，并在不确定性估计中同时保留患者和医院聚类。
  - protected_id: PCR-004
    prior_locator: "Data, materials, and existing evidence base > Current verified-resource versus prospective-gate status; Public ICU database roles and G1 audit"
    revised_locator: "Data, materials, and existing evidence base 开篇; 现有资源、证据与待核验状态; 公共 ICU 数据库角色与数据支持边界; Feasibility and resources"
    semantic_status: preserved
    evidence: >-
      v043 保留文献与专家先验、MIMIC-IV 和 eICU-CRD 纵向数据为核心输入，并只允许预先指定 HiRID 或 AmsterdamUMCdb 作为条件性备份。状态表继续区分数据库存在和版本已有资料支持，与团队访问、DUA、提取、项目队列、具名人员及模型结果尚未核验或尚未生成，未把任何待核验资源写成已经具备。
  - protected_id: PCR-005
    prior_locator: "Data, materials, and existing evidence base > Local RCT evidence and present limits"
    revised_locator: "Data, materials, and existing evidence base > 现有资源、证据与待核验状态; 随机对照试验现有证据与边界; Feasibility, resources, risks, alternatives, and stop conditions > Limitations and boundary conditions 第 8 项"
    semantic_status: preserved
    evidence: >-
      v043 仍只把 EXIT-SEP 与 XBJ-SCAP 作为条件性阶段 III 的潜在个体级数据来源。本地资料被明确限定为项目内衍生的清洗和验证材料，只能支持稀疏访视与字段缺口描述，不能替代个体数据授权、原始 CRF、SAP、随机化、中心、实际访视时序及生存、住院和出院语义核验。
  - protected_id: PCR-006
    prior_locator: "Research content and work packages; Research design and methods, including Observational target, anchoring, missingness and abstention"
    revised_locator: "Research content and work packages > 工作包与最低执行顺序; Research design and methods > 观察性目标、锚定、缺失与不作解释规则; 模拟重建性能与错误结构高置信度支持率的判定标准; 医院优先的跨数据库检验与参数处理状态"
    semantic_status: preserved
    evidence: >-
      v043 保留“资源与可观测性审计→标签、状态和医院分区→简单基线→模拟重建→至多一个复杂候选→两项主要任务和两项次要诊断→冻结→跨数据库检验→条件性试验分析”的单向顺序，并继续分开生理状态、治疗行动和测量过程。正文逐项保留删除、合并或限制解释的条件：20 个随机种子对齐率低于 90%、自助法保留率低于 80%、外部符号一致率低于 80%、状态对齐低于 0.70 或区间未校准；较好的预测表现不能改变这些判定。锚定、可重建性、跨数据库表现及不作解释规则的作用均未改变。
  - protected_id: PCR-007
    prior_locator: "Research content and work packages > Conjunctive minimum success definition; Research design and methods > Hospital-primary genuine cross-database validation"
    revised_locator: "Research content and work packages > 阶段 II 的合取成功定义; Research design and methods > 两项主要临床任务的协议规范; 医院优先的跨数据库检验与参数处理状态; Expected outputs, falsification criteria, and interpretations > 证伪标准"
    semantic_status: preserved
    evidence: >-
      v043 的五项合取定义仍同时要求双数据库数据支持、正确生成与无真实结构及错设情景下的模拟标准、两项主要任务的 Brier 或多类别 Brier 与校准、无高严重度泄漏，以及最终检验医院集上不更新任何模型参数时的任务、状态对齐和结构稳定性。两类仅用适配医院集重新估计参数的结果须分开报告且不能替代前者失败；阶段 III 明确不能计入或补足阶段 II。
  - protected_id: PCR-008
    prior_locator: "Research design and methods > Protocol locks for the two primary clinical tasks; Mutually exclusive post-onset state/event system"
    revised_locator: "Research design and methods > 两项主要临床任务的协议规范; 发病后互斥状态与事件系统"
    semantic_status: preserved
    evidence: >-
      v043 直接保留标本在先时其后 72 小时内给药、给药在先时其后 24 小时内采集，基线 SOFA=0 或取入 ICU 前 24 小时最低可计算值，滚动 24 小时取最差成分，并要求相对基线增加至少 2 分发生在感染前 48 小时至后 24 小时且使用首次可排序时刻。正文仍只分析首次发病，重叠评估时点使每个 ICU 住院段总权重为 1；每 12 小时时点按标签可用时刻取信息，将同一时间片新治疗与下一边界生理状态排序，并排除同时间戳且无法排序的边。延迟进入、互斥状态、竞争终止、校准与适当评分、患者和医院聚类，以及同窗治疗、未来测量频率、重复住院、跨分区处理和结局驱动变量、时间网格或数值标准的泄漏检查均被明确保留。
  - protected_id: PCR-009
    prior_locator: "Structured abstract; Contribution, innovation, impact, application, and closest-work comparison > Contribution and evidence ladder"
    revised_locator: "Structured abstract; Data, materials, and existing evidence base > 现有资源、证据与待核验状态; Contribution, innovation, impact, application, and closest-work comparison > 贡献、影响与证据层级 and 代表性最接近工作比较"
    semantic_status: preserved
    evidence: >-
      v043 将候选模型、模拟重建、跨数据库检验和试验新分析全部写为拟开展、预期或尚未生成；贡献仍限定为条件性的证据整合、验证、基准和可复用资源。正文明确各单项模块已有先例，对完整证据环节缺口的负向判断只有低至中等置信，并禁止据此声称新算法、首个数字孪生、首个控制模型或全球首次。
  - protected_id: PCR-010
    prior_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Resources and governance; Risk and automatic alternative matrix; Remaining execution gates; Identity and final stop boundary; Expected outputs, falsification criteria, and interpretations > Falsification and stop criteria"
    revised_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Feasibility and resources; Working assumptions; Limitations and boundary conditions; Risks, alternatives, and stop conditions"
    semantic_status: preserved
    evidence: >-
      v043 在同一权威 H2 下完整汇集访问与团队承诺、G1 支持、标签和泄漏、状态可重建性、非随机缺失与低治疗支持、跨数据库不更新参数的必要性、月 12/月 20/月 24 时间约束、试验数据与语义、共同生理测量及观测映射、最接近工作证据强度，以及每类失败对应的替代和停止后果。Working assumptions 逐项保留备份数据库、时间方案、依赖 G1 的最终数值、临床尺度到模拟参数的映射、多类别校准估计量与置信区间、共同生理测量和试验映射等待定规范及其决策时点、允许信息和未解决后果。限制第 1 项明确筛选下限不能替代经验有效样本量与模拟稳定性；限制第 8 项及风险表明确试验方向不一致或区间过宽时只能报告无支持或跨场景适用性有限，不能选择亚组改变结论。
  - protected_id: PCR-011
    prior_locator: "Research content and work packages > Twenty-four-month minimum and dated gates; Identity and final stop boundary"
    revised_locator: "Research content and work packages > 二十四个月主体计划与日期节点; Research design and methods > 随机对照试验稀疏随访测量的条件性观测映射与临床状态次要分析, especially 共享前提 and 并列分析路径、估计目标与停止条件; Feasibility, resources, risks, alternatives, and stop conditions > Limitations and boundary conditions 第 7–8 项"
    semantic_status: preserved
    evidence: >-
      v043 明确阶段 I–II 是 24 个月主体研究，阶段 III 位于最低交付之外且不能补足阶段 II。方法权威小节先列出阶段 II 合取成功并冻结、相应试验个体级授权以及核心试验语义可核验这三项共享前提；随后分别规定观测映射成立时分析访视投影摘要，观测映射不成立但 SOFA 与核心语义可核验时开展独立临床状态分析，核心第 7 日或第 8 日及随机化、中心、生存或住院语义不能核验时不开展新访视结局分析。完整资格、两条分析路径与停止逻辑集中在该方法位置，摘要、目标、时间表、证据链、产物和限制位置只保留各自功能所需的输入、输出或边界。
  - protected_id: PCR-012
    prior_locator: "Research question, objectives, and core hypothesis > Core hypothesis and non-hypotheses; Feasibility, resources, risks, alternatives, and stop conditions"
    revised_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Limitations and boundary conditions 第 11 项"
    semantic_status: preserved
    evidence: >-
      v043 在权威限制位置一次性保留完整禁止主张清单：观察性数据和预测表现不能支持真实因果网络、治疗因果效应、反事实策略、机制、中介、系统控制或数字孪生；条件性试验分析不能验证未测潜在动力学、转移关系或整个候选表征；当前计划不能写成已验证模型、临床决策工具、药物平台、无条件临床推广依据、新算法或全球首次。其他章节仅保留与邻近估计目标或解释直接相关的局部边界，没有把完整清单重复为替代性权威位置。
undeclared_scientific_changes: []
findings: []
unresolved_issues: []
---

# Content-preservation check

## Decision rationale

结论为 `scientific_content_preserved`。冻结 register 中 PCR-001 至 PCR-012 的身份、对象、资源状态、设计顺序、数值与时间规则、分支资格、替代和停止后果、主张强度、限制以及待定规范，均能在 v043 正文中以相同含义和强度直接定位。v043 的变化属于术语替换、定义补充、段落拆分与合并、顺序调整、桥接以及权威位置归并；没有改变核心问题或研究对象，没有加入未经登记的数据、方法、结果或证据，没有把计划性验证写成已经完成，也没有削弱可行性限制或把条件性路径改成无条件路径。

revision delta 将本轮声明为编辑修订，且未声明科学变更；本结论并非依据该声明作出，而是由 prior dossier、冻结 register 与 v043 正文的逐项语义比较得到。完整性核对结果为：register 共 12 个 ID，报告恰有 12 项检查；缺失 0、重复 0、未知 0。

## Protected-content trace

- PCR-002 将冻结 register 已授权的“高水平论文、可审计科学证据、不得收缩为单一预测工具”恢复到一句话摘要、定位段和计划产物，未改变研究方法或证据状态。
- PCR-010 的完整资源、限制、待定规范、风险、替代与停止体系归并到 `Feasibility, resources, risks, alternatives, and stop conditions`；其他章节仅保留推进相邻设计推理所需的局部边界。
- PCR-011 的完整阶段 III 资格、两条互斥分析路径及停止逻辑归并到试验方法权威小节；阶段 II 的 24 个月边界和不可补足关系保留在时间与限制位置。
- PCR-012 的完整禁止提高主张清单只在 `Limitations and boundary conditions` 第 11 项权威呈现，其他位置的短边界仅服务于局部估计目标和解释。
- 其余条目主要经历自然语言化、术语统一、表格重组或章节归位；所有受保护数值、时间窗、状态顺序、外部数据分区、模拟标准和证据强度保持不变。

## Required routing

v043 可进入新的独立叙事评估与学术语言评估；后续实例不得继承本报告作为其评分依据。
