---
schema_version: research-idea-content-preservation-check.v1
check_id: content-preservation-I01-001-v003-to-v024-r033
review_id: content-preservation-r033
reviewer_skill: idea-narrative-assessor
reviewer_instance_id: one_pass_preservation_r033
workflow_id: RID-SEPSIS-CSM-20260717-001
round_id: one-pass-current-r033
input_artifact_ids:
  - idea-dossier-I01-001-v003
  - idea-dossier-I01-001-v024
  - protected-content-register-I01-001-v003
  - revision-delta-I01-001-v003-to-v024
input_versions:
  - v003
  - v024
  - v003
  - v003-to-v024
inputs:
  prior_dossier:
    artifact_id: idea-dossier-I01-001-v003
    version: v003
    path: tests/idea-test-0.9.0-preview.1/0.9.0-preview.1/03_ideas/nodes/I01-001/dossiers/idea-dossier-v003.md
  revised_dossier:
    artifact_id: idea-dossier-I01-001-v024
    version: v024
    path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/final/idea-dossier-v024.md
  protected_content_register:
    artifact_id: protected-content-register-I01-001-v003
    version: v003
    path: tests/idea-narrative-forward-0.9.0-preview.3/run-001/inputs/protected-content-register.yaml
  revision_delta:
    artifact_id: revision-delta-I01-001-v003-to-v024
    version: v003-to-v024
    path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/final/revision-delta-v003-to-v024.md
files_read:
  - tests/idea-test-0.9.0-preview.1/0.9.0-preview.1/03_ideas/nodes/I01-001/dossiers/idea-dossier-v003.md
  - tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/final/idea-dossier-v024.md
  - tests/idea-narrative-forward-0.9.0-preview.3/run-001/inputs/protected-content-register.yaml
  - tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/final/revision-delta-v003-to-v024.md
isolation_mode: fresh_subagent
prior_scores_visible: false
source_edits_performed: false
decision: scientific_content_preserved
protected_item_checks:
  - protected_id: PCR-001
    prior_locator: "YAML frontmatter identity_anchor; Research question, objectives, and core hypothesis > Primary research question"
    revised_locator: "YAML frontmatter identity_anchor; Title, summary, audience, and positioning > One-sentence complete-Idea summary; Research question, objectives, and core hypothesis > Primary research question; Feasibility, resources, risks, alternatives, and stop conditions > L13 研究身份"
    semantic_status: preserved
    evidence: >-
      v024 仍以脓毒症发病前在险期、首次发病、发病后互斥状态演化以及恢复、持续恶化、器官衰竭、出 ICU 或死亡为连续研究对象，并以患者状态及其随时间转移为核心。L13 明确普通已发病预后或泛 ICU 风险模型属于身份改变，因此没有把研究改写为普通预测任务。
  - protected_id: PCR-002
    prior_locator: "YAML frontmatter identity_anchor.primary_objective; Research question, objectives, and core hypothesis > Objectives"
    revised_locator: "Title, summary, audience, and positioning > Positioning and contribution frame; Structured abstract > Objective and hypothesis; Research content and work packages > 24 个月最低交付与时间节点; 工作包与最低研究顺序"
    semantic_status: preserved
    evidence: >-
      v024 把文献和专家知识约束的候选结构列为阶段 I，把公共 ICU 数据系统辨识、全过程状态表征及跨数据库验证列为阶段 II，并要求二者在 24 个月内完成。定位段仍把高水平论文、科学证据、验证基准和可复用资源作为交付方向，而不是只交付预测工具。
  - protected_id: PCR-003
    prior_locator: "YAML frontmatter identity_anchor.study_object and primary_unit_of_inference; Research design and methods"
    revised_locator: "YAML frontmatter identity_anchor.study_object and primary_unit_of_inference; Research question, objectives, and core hypothesis > Primary research question; Research design and methods > 两项主要临床任务的协议定义; Feasibility, resources, risks, alternatives, and stop conditions > L13 研究身份"
    semantic_status: preserved
    evidence: >-
      v024 的 frontmatter 未改变研究对象或推断单位；正文保留可比较的发病前在险期和发病后轨迹，并在两项任务中保留患者层与医院层聚类、不重复使用跨集合患者以及患者—时间状态和状态转移的推断结构。
  - protected_id: PCR-004
    prior_locator: "Data, materials, and existing evidence base > Current verified-resource versus prospective-gate status; Public ICU database roles and G1 audit"
    revised_locator: "Data, materials, and existing evidence base > 当前资源与证据状态; 公共 ICU 数据库角色与双数据库可观测性和数据支持审计（G1）; Feasibility, resources, risks, alternatives, and stop conditions > L1 访问、人员与计算资源; L2 双数据库数据支持"
    semantic_status: preserved
    evidence: >-
      v024 仍把 MIMIC-IV v3.1 与 eICU-CRD v2.0 的存在和版本列为已核验，把团队访问、数据使用协议、提取、具名人员和项目特异 G1 支持列为未核验或尚未生成，把所有模型、模拟、外部检验和试验新分析结果列为尚未生成。HiRID 或 AmsterdamUMCdb 仍只能在月 0–3 预先指定并接受同等审计后作为备份。
  - protected_id: PCR-005
    prior_locator: "Data, materials, and existing evidence base > Local RCT evidence and present limits"
    revised_locator: "Data, materials, and existing evidence base > 本地 RCT 材料与当前证据状态; Feasibility, resources, risks, alternatives, and stop conditions > L7 试验数据、授权与核心语义; L8 共同生理测量与访视一维分数; L9 试验稀疏性、异质性与推断"
    semantic_status: preserved
    evidence: >-
      v024 仍把 EXIT-SEP 与 XBJ-SCAP 材料限定为项目内衍生清洗或验证材料。L7 明确这些材料不替代个体数据授权、原始病例报告表、统计分析计划、随机化、中心、实际访视时序和生存、住院、出院或转院语义核验，两项试验仍只是条件性阶段 III 的潜在输入。
  - protected_id: PCR-006
    prior_locator: "Research content and work packages; Research design and methods"
    revised_locator: "Research content and work packages > 工作包与最低研究顺序; Research design and methods > 两项主要临床任务的协议定义; 发病后互斥状态与事件系统; 观察性估计对象、尺度固定与低支持处理; 模拟恢复与伪结构控制; 以医院为主要单位的真正跨数据库验证; 条件性试验访视分数与独立临床状态分析"
    semantic_status: preserved
    evidence: >-
      v024 的最低研究顺序仍依次包含资源与 G1、标签与状态和医院拆分、简单基线、模拟恢复与伪结构控制、至多一个复杂候选、两项主要任务和两项次要诊断、开发结果锁定、未用于开发的跨库检验，最后才是条件性试验分析。Y_t、A_t 与 M_t 继续分离，解释范围仍受尺度锚定、跨库对齐、模拟可恢复性、运输性和低支持处理约束。
  - protected_id: PCR-007
    prior_locator: "Research content and work packages > Conjunctive minimum success definition; Research design and methods > Hospital-primary genuine cross-database validation"
    revised_locator: "Research content and work packages > 阶段 II 合取成功定义; Research design and methods > 以医院为主要单位的真正跨数据库验证; Feasibility, resources, risks, alternatives, and stop conditions > L6 外部隔离与运输; L10 时间与阶段依赖"
    semantic_status: preserved
    evidence: >-
      v024 的阶段 II 合取定义仍同时要求双数据库数据支持、模拟恢复与伪结构控制、两项主要任务的 proper score 和校准、泄漏清零，以及未用于开发测试区的不作更新表现、状态对齐和结构符号稳定。只在适配区学习的有限更新被分开报告且不能替代不作更新的主要检验；L10 明确阶段 III 结果不能补足阶段 II 失败。
  - protected_id: PCR-008
    prior_locator: "Research design and methods > Protocol locks for the two primary clinical tasks; Mutually exclusive post-onset state/event system"
    revised_locator: "Research design and methods > 两项主要临床任务的协议定义; 发病后互斥状态与事件系统; 观察性估计对象、尺度固定与低支持处理; 条件性试验访视分数与独立临床状态分析"
    semantic_status: preserved
    evidence: >-
      v024 逐项保留标本与抗菌药物 72/24 小时配对、基线 SOFA、滚动 24 小时成分和首次可排序发病时刻，保留事件与信息可用双时钟、首次发病、延迟进入、互斥发病后状态、竞争终止、重叠界标单次住院总权重为 1，以及 [t,t+12h) 行动和下一状态的顺序与同时间戳边排除。泄漏审计仍覆盖同时间格行动、未来测量频率、重复住院及结局驱动的变量、网格或阈值。试验部分保留 R0/R1、预先确定的 SVD 计算关系和全部数值标准、死亡与出院层级、缺失数据与中心处理、Holm 家族、分析集和分试验规则。
  - protected_id: PCR-009
    prior_locator: "Structured abstract; Contribution, innovation, impact, application, and closest-work comparison > Contribution and evidence ladder"
    revised_locator: "Structured abstract > Expected result; Data, materials, and existing evidence base > 当前资源与证据状态; Contribution, innovation, impact, application, and closest-work comparison > 贡献与证据层级; 已核验的代表性最接近工作比较; Feasibility, resources, risks, alternatives, and stop conditions > L11 最接近工作与贡献强度"
    semantic_status: preserved
    evidence: >-
      v024 明确所有模型和验证输出都是拟生成产物，当前结果尚未生成。最接近工作结论仍限定为截至 2026-07-17 的有界代表性检索，在低至中等置信度下未识别完整组合；L11 明确该检索不是系统综述并禁止据此声称全球首次或新算法。贡献强度仍是条件性的整合、验证及基准或资源增量。
  - protected_id: PCR-010
    prior_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Resources and governance; Risk and automatic alternative matrix; Remaining execution gates; Identity and final stop boundary"
    revised_locator: "Feasibility, resources, risks, alternatives, and stop conditions > 假设、限制与对应处理 > L1–L13"
    semantic_status: preserved
    evidence: >-
      v024 在第 14 个 H2 的 L1–L13 集中保留访问与人员、G1 数据支持、标签与泄漏、识别与模拟、MNAR 与低重叠、外部隔离与运输、试验数据及核心语义、共同生理测量和访视分数、试验稀疏性与推断、时间与阶段依赖、最接近工作、解释与应用边界以及研究身份。每类均保留当前状态或限制、核验或触发条件和对应的有限替代、降级或停止后果；其他章节保留的是直接定义相邻估计对象或分析分支所需的局部条件。
  - protected_id: PCR-011
    prior_locator: "Research content and work packages > Twenty-four-month minimum and dated gates; Identity and final stop boundary"
    revised_locator: "Structured abstract > Objective and hypothesis; Research content and work packages > 24 个月最低交付与时间节点; Feasibility, resources, risks, alternatives, and stop conditions > L10 时间与阶段依赖"
    semantic_status: preserved
    evidence: >-
      v024 仍要求阶段 I–II 的最低交付在 24 个月内完成，把阶段 III 放在该时限之外，并要求阶段 II 成功以及对应试验资料、语义和访视一维分数计算条件均满足后才可开展。L10 原义保留“任何阶段 III 结果都不能补足阶段 II 的失败”。
  - protected_id: PCR-012
    prior_locator: "Research question, objectives, and core hypothesis > Core hypothesis and non-hypotheses; Feasibility, resources, risks, alternatives, and stop conditions"
    revised_locator: "Research question, objectives, and core hypothesis > Core hypothesis and non-hypotheses; Feasibility, resources, risks, alternatives, and stop conditions > L12 科学解释与应用边界"
    semantic_status: preserved
    evidence: >-
      v024 的核心假设仍把治疗因果效应排除在观察性估计对象之外。L12 完整保留观察性数据与预测表现不识别真实因果网络、治疗因果效应、反事实策略、机制、中介、控制或数字孪生，条件性随机试验次要分析不验证未测潜在动力学、转移边或整个系统模型，并禁止把计划写成已验证模型、临床决策工具、药物平台或临床效用证据。
undeclared_scientific_changes: []
findings: []
unresolved_issues: []
---

# Content-preservation check

## Decision rationale

逐项直接比较 v003 与 v024 后，PCR-001 至 PCR-012 均能在 v024 中定位到同义、同强度且状态一致的内容。修改把读者主线、方法细节和限制重新分区，并将项目内部短称替换为功能性科学表达；未发现研究身份、主要任务或估计对象、阶段关系、数值标准、数据可用性状态、证据强度、关键限制、条件性后续阶段或禁止升级主张发生改变。修订 delta 声明没有科学变更，正文比较也未发现未声明的新增数据、方法、结果或证据。

## Protected-content trace

最显著的移动是把 v003 分散在摘要、证据链、可证伪判据、解释矩阵和风险表中的完整限制集中到 v024 第 14 个 H2 的 L1–L13；方法节只保留直接决定估计对象、资格判断或分析分支的条件。RCT 的“观测投影”相关项目内短称被拆解为共同生理测量资格、由阶段 II 状态—测量关系计算的一维访视分数、R1 状态信息保留与实测指标重建检验，以及独立的死亡分层 SOFA 再分析；其输入、公式、阈值、死亡和出院排序、缺失处理、中心、多重性与停止条件均保持不变。没有发现工作假设被删除、改写为事实或借文字流畅性提高其证据状态；尚未核验和尚未生成的项目仍以相同状态出现。

## Required routing

结论为 `scientific_content_preserved`。该 dossier 可进入全新的 narrative assessment 与 academic language assessment；无需因本次编辑修订返回科学或方法学复审。
