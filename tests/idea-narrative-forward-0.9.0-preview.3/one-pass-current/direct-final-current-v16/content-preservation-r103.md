---
schema_version: research-idea-content-preservation-check.v1
check_id: content-preservation-I01-001-r103
review_id: content-preservation-review-I01-001-r103
reviewer_skill: idea-narrative-assessor
reviewer_instance_id: preservation-reviewer-r103
workflow_id: RID-SEPSIS-CSM-20260717-001
round_id: r103
input_artifact_ids:
  - idea-dossier-I01-001-v003
  - idea-dossier-I01-001-v050
  - protected-content-register-I01-001-v004-r004
  - revision-delta-I01-001-v003-to-v050
input_versions:
  - v003
  - v050
  - r004
  - v003-to-v050
inputs:
  prior_dossier:
    artifact_id: idea-dossier-I01-001-v003
    version: v003
    path: tests/idea-test-0.9.0-preview.1/0.9.0-preview.1/03_ideas/nodes/I01-001/dossiers/idea-dossier-v003.md
  revised_dossier:
    artifact_id: idea-dossier-I01-001-v050
    version: v050
    path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v16/idea-dossier-v050.md
  protected_content_register:
    artifact_id: protected-content-register-I01-001-v004-r004
    version: r004
    path: tests/idea-narrative-forward-0.9.0-preview.3/run-001/inputs/protected-content-register-v004.yaml
  revision_delta:
    artifact_id: revision-delta-I01-001-v003-to-v050
    version: v003-to-v050
    path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v16/revision-delta-v003-to-v050.md
files_read:
  - tests/idea-test-0.9.0-preview.1/0.9.0-preview.1/03_ideas/nodes/I01-001/dossiers/idea-dossier-v003.md
  - tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v16/idea-dossier-v050.md
  - tests/idea-narrative-forward-0.9.0-preview.3/run-001/inputs/protected-content-register-v004.yaml
  - tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v16/revision-delta-v003-to-v050.md
isolation_mode: fresh_subagent
prior_scores_visible: false
source_edits_performed: false
decision: scientific_content_preserved
protected_item_checks:
  - protected_id: PCR-001
    prior_locator: "YAML frontmatter identity_anchor; Research question, objectives, and core hypothesis > Primary research question"
    revised_locator: "YAML frontmatter identity_anchor; Research question, objectives, and core hypothesis > Primary research question"
    semantic_status: preserved
    evidence: >-
      五个 identity_anchor 字段逐字段完全相同。正文仍以纵向脓毒症中心 ICU 患者系统为对象，覆盖可比较未发病在险时段、首次发病、发病后互斥演化和结局；预测仍只是检验任务，而不是研究身份。
  - protected_id: PCR-002
    prior_locator: "YAML frontmatter identity_anchor.primary_objective; Research question, objectives, and core hypothesis > Objectives"
    revised_locator: "One-sentence complete-Idea summary; Research question, objectives, and core hypothesis > Objectives item 1; Background, current state, gap, significance, and rationale > Significance"
    semantic_status: preserved
    evidence: >-
      修订稿分别保留了三项承诺：阶段 I–II 在 24 个月内完成，以文献和专家知识约束候选结构并用公共 ICU 数据进行系统辨识、全病程表征和跨数据库验证；目标支持一篇或多篇高水平论文；交付不得收缩为预测工具。
  - protected_id: PCR-003
    prior_locator: "YAML frontmatter identity_anchor.study_object and primary_unit_of_inference; Research design and methods"
    revised_locator: "YAML frontmatter identity_anchor.study_object and primary_unit_of_inference; Structured abstract > Objective and hypothesis; Primary research question; Protocol locks for the two primary clinical tasks"
    semantic_status: preserved
    evidence: >-
      study_object 与 primary_unit_of_inference 两个锚点原样保留。修订正文仍将可比较的未发病在险时段和发病后轨迹纳入同一纵向系统，并以尊重患者及医院聚类的患者—时间状态和状态转移为主要推断单位。
  - protected_id: PCR-004
    prior_locator: "Data, materials, and existing evidence base > Current verified-resource versus prospective-gate status; Public ICU database roles and G1 audit"
    revised_locator: "Data, materials, and existing evidence base > Current verified-resource versus prospective-gate status; Public ICU database roles and support status; Feasibility, resources, risks, alternatives, and stop conditions > Resource and evidence limitations"
    semantic_status: preserved
    evidence: >-
      文献和专家先验、MIMIC-IV v3.1 与 eICU-CRD v2.0 仍是核心输入，HiRID 或 AmsterdamUMCdb 仍须在结果揭示前预指定为备份。数据库存在与版本和团队实际可用性继续分开：访问凭证、DUA、可运行提取、项目队列支持、具名人员承诺尚未核验，模型及各类结果尚未生成。
  - protected_id: PCR-005
    prior_locator: "Data, materials, and existing evidence base > Local RCT evidence and present limits"
    revised_locator: "Data, materials, and existing evidence base > Local RCT evidence and present limits; Research design and methods > Conditional trial-specific secondary analyses > Shared prerequisites; Feasibility, resources, risks, alternatives, and stop conditions > Resource and evidence limitations"
    semantic_status: preserved
    evidence: >-
      EXIT-SEP 与 XBJ-SCAP 仍仅是条件性阶段 III 的潜在个体级数据来源，现有材料仍明确为项目本地衍生报告。个体数据授权、原始 CRF、SAP、数据字典或数据持有人确认，以及随机化、中心、访视时序、生存、住院、出院和转院语义仍须在分析前核验。
  - protected_id: PCR-006
    prior_locator: "Research content and work packages; Research design and methods, including Observational target, anchoring and abstention"
    revised_locator: "Research content and work packages > Work packages and minimum route; Research design and methods > Design sequence and database-support criteria; Variable roles; Observational target, anchoring, missingness, and abstention"
    semantic_status: preserved
    evidence: >-
      方法顺序仍从资源与可观测性核验、标签和状态及医院拆分锁定、简单基线、绝对模拟恢复与错误结构检查，进入至多一个复杂候选、两项主要任务和两项次要诊断、开发冻结及未触碰外部验证，之后才可能进入试验分析。生理状态、治疗行动和观测过程继续分离。20 个种子对齐率低于 90%、自助法保留率低于 80%、外部符号一致率低于 80%、状态对齐低于 0.70 或区间未校准时的删除、合并或数据库/照护政策特异标记均保留，且预测表现不能豁免这些后果。
  - protected_id: PCR-007
    prior_locator: "Research content and work packages > Conjunctive minimum success definition; Research design and methods > Hospital-primary genuine cross-database validation"
    revised_locator: "Research content and work packages > Conjunctive minimum success definition; Research design and methods > Hospital-prioritized independent cross-database validation; Expected outputs, falsification criteria, and interpretations > Falsification and stop criteria"
    semantic_status: preserved
    evidence: >-
      阶段 II 成功仍是数据支持、绝对恢复、两项主要任务的 Brier 或多类别 Brier 评分与校准、严重泄漏清除、冻结模型不重估参数的外部表现、状态对齐和结构符号稳定性的合取。只重估结局校准或只重估观测方程的结果与冻结模型结果分开报告，不能替代冻结模型失败；阶段 III 不计入或补足阶段 II 成功。
  - protected_id: PCR-008
    prior_locator: "Research design and methods > Protocol locks for the two primary clinical tasks; Mutually exclusive post-onset state/event system"
    revised_locator: "Research design and methods > Protocol locks for the two primary clinical tasks; Mutually exclusive post-onset state/event system; Variable roles"
    semantic_status: preserved
    evidence: >-
      两项主要任务、事件与信息可用双时钟、首次发病风险集、延迟进入、互斥状态、竞争终止、按当时可用信息构造特征、评分与校准目标，以及患者和医院聚类不确定性均未改变。标本先发生时抗菌药须在 72 小时内、给药先发生时标本须在 24 小时内，基线 SOFA 与滚动 24 小时成分规则、感染前 48 小时至后 24 小时器官功能窗和首个可排序发病时刻均保留；仍只分析首次发病，重叠评估点的每次住院总权重为 1，同一时间格内 A_t 先于下一状态且无法排序的同时间戳边被排除。泄漏检查仍覆盖同格治疗、未来测量频率、重复住院或患者跨集合、跨拆分处理及结局驱动的网格或阈值。
  - protected_id: PCR-009
    prior_locator: "Structured abstract; Contribution, innovation, impact, application, and closest-work comparison > Contribution and evidence ladder"
    revised_locator: "Structured abstract > Expected result and Contribution and impact; Data, materials, and existing evidence base > Current verified-resource versus prospective-gate status; Contribution, innovation, impact, application, and closest-work comparison; Feasibility, resources, risks, alternatives, and stop conditions > Unsupported claims and interpretation boundaries"
    semantic_status: preserved
    evidence: >-
      修订稿仍把候选模型、模拟恢复、主要任务、外部验证和试验新分析表述为计划且尚未生成。可支持的贡献仍限于条件性的整合、验证、基准和资源增量；各单项模块已有代表性先例，完整组合缺口仍明确为低至中等置信，并明确排除新算法和全球首次主张。
  - protected_id: PCR-010
    prior_locator: "Feasibility, resources, risks, alternatives, and stop conditions; Research design and methods; Expected outputs, falsification criteria, and interpretations"
    revised_locator: "Feasibility, resources, risks, alternatives, and stop conditions; Research design and methods; Expected outputs, falsification criteria, and interpretations"
    semantic_status: preserved
    evidence: >-
      第 14 节保留资源与访问、人员承诺、数据库支持、标签与泄漏、可恢复性、缺失非随机与低重叠、冻结模型外部验证、时间节点、试验数据和语义、共同锚点及观测映射、最接近工作不确定性等完整限制，并保留临床尺度到模拟参数的映射、多类别校准估计量、置信界和阈值登记等未决规范，以及事件或参数下限不能替代经验有效样本量和模拟稳定性的边界。设计资格与互斥路线保留在 Methods，结果证伪和结果依赖解释保留在第 11 节；第 14 节中的试验方向与区间陈述仅作为主张边界，未改变该结果解释。两项试验方向不一致或区间过宽时仍只能报告无支持或跨场景适用性有限，且不能选择亚组改变主要解释。
  - protected_id: PCR-011
    prior_locator: "Research content and work packages > Twenty-four-month minimum and dated gates; Identity and final stop boundary"
    revised_locator: "Research content and work packages > Twenty-four-month minimum and dated gates; Research design and methods > Conditional trial-specific secondary analyses; Feasibility, resources, risks, alternatives, and stop conditions"
    semantic_status: preserved
    evidence: >-
      阶段 I–II 的 24 个月边界及阶段 III 位于最低交付之外的关系未变。Methods 先列阶段 II 成功、个体数据可用和核心试验语义可核验三个共享前提，再分别列出共同实测锚点映射成立时的访视层级结局路线，以及映射不成立但 SOFA 和核心语义可核验时的独立临床状态路线；核心 D7 或 D8、随机化、中心、生存或住院语义不可核验时停止新访视状态结局。后续试验结果仍不能补足阶段 II 的数据支持、模拟恢复、主要任务或外部验证失败。标题与摘要只保留高层条件性用途，其他章节只保留各自功能所需的信息，完整资格、两条路线和停止逻辑只在 Methods 权威小节出现。
  - protected_id: PCR-012
    prior_locator: "Research question, objectives, and core hypothesis > Core hypothesis and non-hypotheses; Feasibility, resources, risks, alternatives, and stop conditions"
    revised_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Unsupported claims and interpretation boundaries; Research design and methods > Observational target, anchoring, missingness, and abstention; Expected outputs, falsification criteria, and interpretations > Interpretation matrix"
    semantic_status: preserved
    evidence: >-
      第 14 节完整保留了观察性数据和预测表现不能支持真实因果网络、治疗因果效应、反事实策略、机制、中介、控制或数字孪生的边界，也保留了条件性试验分析不能验证未测潜在动力学、转移边或整个系统模型的边界。当前计划仍不得写成已验证模型、临床决策工具、药物平台或无条件临床推广依据；完整禁止主张集中在第 14 节，Methods 和第 11 节只保留定义估计目标或解释结果所需的局部边界。
undeclared_scientific_changes: []
findings: []
unresolved_issues: []
---

# Content-preservation check

## Decision rationale

修订稿完整保留了冻结登记表中的十二项科学内容。五个身份锚点逐字段相同；定量标准、时间规则、分析先后顺序、互斥与后备路线、停止后果、证据状态、主张强度、限制和工作假设均可在修订稿中定位，且没有把计划中的工作写成已经完成。修订说明声明的操作均为拆分、合并、移动、定义、替换和删去重复表达，没有声明或引入科学变更。

## Protected-content trace

- 研究身份、24 个月阶段 I–II 目标、研究对象、核心证据基础和推断单位保留在原样复制的 frontmatter，并在摘要、研究问题和目标中以读者可理解的形式展开。
- 数据支持数量、时钟和标签规则、模拟恢复标准、外部验证顺序及弃权后果集中到 Methods；数值、方向、不等式和失败后果与先前稿一致。
- 条件性试验分析的共享前提、共同锚点路线、独立临床状态路线和停止条件集中到 `Conditional trial-specific secondary analyses`，其他位置仅保留各章节所需的高层功能。
- 完整限制、工作假设和禁止主张集中到第 14 节；方法资格保留在 Methods，结果依赖解释保留在第 11 节。

## Required routing

该 dossier 可进入新的叙事与学术语言评估。
