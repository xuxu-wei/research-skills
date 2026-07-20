---
schema_version: research-idea-content-preservation-check.v1
check_id: content-preservation-I01-001-v048-r091
review_id: content-preservation-review-I01-001-r091
reviewer_skill: idea-narrative-assessor
reviewer_instance_id: fresh-preservation-v048-r091
workflow_id: RID-SEPSIS-CSM-20260717-001
round_id: r091
input_artifact_ids:
  - idea-dossier-I01-001-v003
  - idea-dossier-I01-001-v048
  - protected-content-register-I01-001-v004-r004
  - revision-delta-I01-001-v003-to-v048
input_versions:
  - v003
  - v048
  - r004
  - v003-to-v048
inputs:
  prior_dossier:
    artifact_id: idea-dossier-I01-001-v003
    version: v003
    path: tests/idea-test-0.9.0-preview.1/0.9.0-preview.1/03_ideas/nodes/I01-001/dossiers/idea-dossier-v003.md
  revised_dossier:
    artifact_id: idea-dossier-I01-001-v048
    version: v048
    path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v14/idea-dossier-v048.md
  protected_content_register:
    artifact_id: protected-content-register-I01-001-v004-r004
    version: r004
    path: tests/idea-narrative-forward-0.9.0-preview.3/run-001/inputs/protected-content-register-v004.yaml
  revision_delta:
    artifact_id: revision-delta-I01-001-v003-to-v048
    version: v003-to-v048
    path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v14/revision-delta-v003-to-v048.md
files_read:
  - tests/idea-test-0.9.0-preview.1/0.9.0-preview.1/03_ideas/nodes/I01-001/dossiers/idea-dossier-v003.md
  - tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v14/idea-dossier-v048.md
  - tests/idea-narrative-forward-0.9.0-preview.3/run-001/inputs/protected-content-register-v004.yaml
  - tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v14/revision-delta-v003-to-v048.md
isolation_mode: fresh_subagent
prior_scores_visible: false
source_edits_performed: false
decision: scientific_content_preserved
protected_item_checks:
  - protected_id: PCR-001
    prior_locator: "v003 frontmatter identity_anchor.primary_research_question；Research question, objectives, and core hypothesis > Primary research question"
    revised_locator: "v048 frontmatter identity_anchor.primary_research_question；Title, summary, audience, and positioning > Positioning and contribution frame；Research question, objectives, and core hypothesis > 主要研究问题"
    semantic_status: preserved
    evidence: >-
      primary_research_question 的原始字符串逐值相等。正文仍以构建并验证脓毒症全病程候选动态复杂系统模型为核心问题，覆盖未发病在险时段、首次发病、发病后互斥状态和结局，并明确该模型不是普通风险评分或单一预测器。
  - protected_id: PCR-002
    prior_locator: "v003 frontmatter identity_anchor.primary_objective；Research question, objectives, and core hypothesis > Objectives"
    revised_locator: "v048 frontmatter identity_anchor.primary_objective；One-sentence complete-Idea summary；Background... > Significance；Expected outputs... > 计划产物"
    semantic_status: preserved
    evidence: >-
      primary_objective 的原始字符串逐值相等。v048 同时保留 24 个月内完成阶段 I–II、以文献与专家知识约束并使用公共 ICU 数据完成模型构建和跨数据库验证、高水平论文与可审计科学证据的交付方向，以及交付不收缩为单一预测工具的边界。
  - protected_id: PCR-003
    prior_locator: "v003 frontmatter identity_anchor.study_object and primary_unit_of_inference；Research design and methods"
    revised_locator: "v048 frontmatter identity_anchor.study_object and primary_unit_of_inference；Title, summary, audience, and positioning；Research question, objectives, and core hypothesis；Research design and methods"
    semantic_status: preserved
    evidence: >-
      study_object 与 primary_unit_of_inference 两个原始字符串均逐值相等。研究对象仍是以脓毒症为中心的纵向 ICU 患者系统，包含可比较的未发病在险时段和发病后轨迹；推断单位仍是尊重患者与医院聚类的患者—时间状态及状态转移。
  - protected_id: PCR-004
    prior_locator: "v003 Data, materials, and existing evidence base > Current verified-resource versus prospective-gate status；Public ICU database roles and G1 audit"
    revised_locator: "v048 frontmatter identity_anchor.core_data_or_evidence_base；Data, materials, and existing evidence base > 当前证据与后续要求；公共重症监护数据库角色与观测数据支持"
    semantic_status: preserved
    evidence: >-
      core_data_or_evidence_base 的原始字符串逐值相等。文献与专家先验、MIMIC-IV、eICU-CRD 以及预先指定的 HiRID 或 AmsterdamUMCdb 备份角色均保留；数据库存在与版本和团队访问、协议、可运行提取、项目计数、具名人员及模型结果的状态继续严格分开，未核验或未生成内容没有被写成已经具备。
  - protected_id: PCR-005
    prior_locator: "v003 Data, materials, and existing evidence base > Local RCT evidence and present limits"
    revised_locator: "v048 Data, materials, and existing evidence base > 本地随机试验证据与当前状态；Research design and methods > 主体研究后的条件性分试验次要分析"
    semantic_status: preserved
    evidence: >-
      EXIT-SEP 与 XBJ-SCAP 仍仅是阶段 III 的潜在个体数据来源。v048 保留两项试验的样本、访视非缺失与字段缺口数字，并继续说明衍生报告不能替代个体数据授权、原始 CRF/SAP、随机化、中心、访视时序以及生存、住院、出院和转院语义核验。
  - protected_id: PCR-006
    prior_locator: "v003 Research content and work packages；Research design and methods > Observational target, anchoring and abstention；Absolute simulation and semi-synthetic recovery gate"
    revised_locator: "v048 Research content and work packages > 工作包与最低执行顺序；Research design and methods > 观察性目标、锚定、缺失与可解释范围；相对已知生成机制的模拟检验"
    semantic_status: preserved
    evidence: >-
      资源与数据支持、标签与状态和医院分区、简单基线、已知生成机制模拟、至多一个复杂候选、两项主要任务与两项次要诊断、开发冻结、跨数据库评估、条件性试验分析的先后关系保留。Y_t、A_t、M_t 的分离保留；20 个随机种子对齐率 90%、自助保留率 80%、外部符号一致率 80%、状态对齐 0.70 和区间校准等判定及删除、合并、改用简单模型或限定解释的后果均保留，预测表现不能豁免这些判定。
  - protected_id: PCR-007
    prior_locator: "v003 Research content and work packages > Conjunctive minimum success definition；Research design and methods > Hospital-primary genuine cross-database validation"
    revised_locator: "v048 Research content and work packages > 合取式最低成功定义；Research design and methods > 医院优先的跨数据库评估；Expected outputs, falsification criteria, and interpretations"
    semantic_status: preserved
    evidence: >-
      阶段 II 仍由两库数据支持、正确生成与零边及错设情景下的恢复、两项主要任务的严格适当评分和校准、泄漏清除、未更新外部性能、状态对齐与结构符号稳定共同决定。适配区确定的重新校准、观测层更新及全模型再开发继续与未更新评估分开，不能替代其失败；阶段 III 结果不计入也不补足该合取判定。
  - protected_id: PCR-008
    prior_locator: "v003 Research design and methods > Protocol locks for the two primary clinical tasks；Mutually exclusive post-onset state/event system"
    revised_locator: "v048 Research design and methods > 两项主要临床任务的方案规定；互斥的发病后状态与事件系统"
    semantic_status: preserved
    evidence: >-
      两项主要任务、临床事件与信息可用双时钟、72 小时后或 24 小时后标本—抗菌药配对、基线 SOFA、滚动 24 小时组成计算、感染前 48 小时至后 24 小时窗口和首次可排序发病时刻均保留。首次发病、重叠界标每次 ICU 停留总权重为 1、延迟进入、互斥状态、竞争终止、同一时间段 A_t 与下一状态的顺序、同时间戳不能排序的转移排除、校准与严格适当评分、患者和医院聚类不确定性，以及同窗治疗、未来测量频率、重复住院和结局驱动时间或阈值的泄漏防护均可定位。
  - protected_id: PCR-009
    prior_locator: "v003 Structured abstract；Contribution, innovation, impact, application, and closest-work comparison > Contribution and evidence ladder"
    revised_locator: "v048 Structured abstract；Data, materials, and existing evidence base > 当前证据与后续要求；Contribution, innovation, impact, application, and closest-work comparison；Title and positioning claim-support table"
    semantic_status: preserved
    evidence: >-
      v048 仍把模型、模拟、预测、外部测试和试验新分析写为计划或尚未生成结果。贡献范围仍限于条件性的整合、跨数据库验证、基准和可复用资源；各模块已有先例的证据状态与完整组合缺口的低至中等置信均保留，没有新增新算法、首次或全球首次主张。
  - protected_id: PCR-010
    prior_locator: "v003 Feasibility, resources, risks, alternatives, and stop conditions；Research design and methods；Expected outputs, falsification criteria, and interpretations"
    revised_locator: "v048 Research design and methods；Expected outputs, falsification criteria, and interpretations；Feasibility, resources, risks, alternatives, and stop conditions > 工作假设、限制与边界条件、运行风险"
    semantic_status: preserved
    evidence: >-
      第 14 节集中保留资源与访问、人员承诺、G1 支持、标签和泄漏、状态可恢复性、非随机缺失与低重叠、未更新外部评估、时间节点、试验数据与语义、共同指标与固定计算以及最接近工作不确定性，并保留完整不支持主张边界。临床尺度到模拟参数的映射、多类别校准估计量与置信区间及阈值记录仍为未解决工作假设；事件或参数筛选下限不能替代经验有效样本量和模拟稳定性。方法部分保留资格、互斥分支、失败触发和替代或停止后果，第 11 节保留结果证伪和结果依赖解释；两项试验方向不一致或区间过宽时不以亚组选择改变主要解释。
  - protected_id: PCR-011
    prior_locator: "v003 Research content and work packages > Twenty-four-month minimum and dated gates；Identity and final stop boundary；Research design and methods > Conditional trial-observation projection and independent fallback"
    revised_locator: "v048 Research content and work packages > 二十四个月最低交付与时间节点、工作包与最低执行顺序；Research design and methods > 主体研究后的条件性分试验次要分析；Feasibility... > 时间范围"
    semantic_status: preserved
    evidence: >-
      阶段 I–II 必须在 24 个月内完成，阶段 III 仍位于最低交付之外，且不能补足阶段 II 的资源、模拟恢复、主要任务或外部评估要求。阶段 III 方法先给阶段 II 达标与冻结、个体数据可用及核心试验语义可核验等共享前提；随后分别保留共同指标与固定计算合格时的访视状态分数分析，以及固定计算不合格但核心信息完整时仍可开展的独立临床状态分析；核心访视、随机化、中心或生存语义不完整时不开展新访视结局分析。一个分支的资格没有被上提为整个阶段 III 的共同条件。
  - protected_id: PCR-012
    prior_locator: "v003 Research question, objectives, and core hypothesis > Core hypothesis and non-hypotheses；Feasibility, resources, risks, alternatives, and stop conditions"
    revised_locator: "v048 Feasibility, resources, risks, alternatives, and stop conditions > 限制与边界条件，第 11 项；Research question and methods/result interpretation 的局部边界"
    semantic_status: preserved
    evidence: >-
      第 14 节完整保留观察性数据和预测表现不支持真实因果网络、治疗因果效应、反事实策略、机制、中介或控制，条件性试验次要分析不验证未测潜在动力学、转移边或整个系统模型的边界。当前计划仍不能被称为已验证模型、数字孪生、临床决策工具、药物平台、无条件推广依据、新算法或首次性成果；其他位置只保留与相邻估计目标或结果解释直接相关的局部边界。
undeclared_scientific_changes: []
findings: []
unresolved_issues: []
---

# Content-preservation check

## Decision rationale

决定为 `scientific_content_preserved`。逐项比较显示，PCR-001 至 PCR-012 均在 v048 中保留相同科学含义、条件关系、证据状态和主张强度；修订 delta 明确声明为编辑性调整，四份输入之间没有出现未声明的科学增删、把条件性内容改成无条件内容、把计划工作改成已完成结果，或弱化限制与停止后果的情况。

对 frontmatter `identity_anchor` 进行了序数字符串逐值比较：`primary_research_question`、`primary_objective`、`study_object`、`core_data_or_evidence_base` 和 `primary_unit_of_inference` 均为相等，结果为 5/5；两个完整 mapping 相等。标题和正文的读者可见改写没有替换或改写这五个机器可读值。

## Protected-content trace

v048 的主要编辑性变化是把完整限制与不支持主张集中到第 14 节，把阶段 III 的完整资格、两条互斥分析路径和停止逻辑集中到方法部分，并把结果证伪与结果依赖解释集中到第 11 节。数值标准、时序规则、分区优先级、适配与测试关系、缺失处理、试验分支资格及失败后果仍可在相应权威位置找到；摘要、目标、证据链、计划产物和实现表只保留各自功能所需的较高层表述。未发现保护内容因移动、合并或术语展开而改变含义。

## Required routing

该 dossier 可进入新的叙事与学术语言评估；本核验不对叙事质量、语言质量或科学设计质量作判断。
