---
schema_version: research-idea-content-preservation-check.v1
check_id: content-preservation-I01-001-r080
review_id: content-preservation-r080
reviewer_skill: idea-narrative-assessor
reviewer_instance_id: fresh-content-preservation-reviewer-r080
workflow_id: RID-SEPSIS-CSM-20260717-001
round_id: r080
input_artifact_ids:
  - idea-dossier-I01-001-v003
  - idea-dossier-I01-001-v046
  - protected-content-register-I01-001-v004-r004
  - revision-delta-I01-001-v003-to-v046
input_versions:
  - v003
  - v046
  - r004
  - v046
inputs:
  prior_dossier:
    artifact_id: idea-dossier-I01-001-v003
    version: v003
    path: tests/idea-test-0.9.0-preview.1/0.9.0-preview.1/03_ideas/nodes/I01-001/dossiers/idea-dossier-v003.md
  revised_dossier:
    artifact_id: idea-dossier-I01-001-v046
    version: v046
    path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v12/idea-dossier-v046.md
  protected_content_register:
    artifact_id: protected-content-register-I01-001-v004-r004
    version: r004
    path: tests/idea-narrative-forward-0.9.0-preview.3/run-001/inputs/protected-content-register-v004.yaml
  revision_delta:
    artifact_id: revision-delta-I01-001-v003-to-v046
    version: v046
    path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v12/revision-delta-v003-to-v046.md
files_read:
  - tests/idea-test-0.9.0-preview.1/0.9.0-preview.1/03_ideas/nodes/I01-001/dossiers/idea-dossier-v003.md
  - tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v12/idea-dossier-v046.md
  - tests/idea-narrative-forward-0.9.0-preview.3/run-001/inputs/protected-content-register-v004.yaml
  - tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v12/revision-delta-v003-to-v046.md
isolation_mode: fresh_subagent
prior_scores_visible: false
source_edits_performed: false
decision: scientific_content_preserved
protected_item_checks:
  - protected_id: PCR-001
    prior_locator: "YAML frontmatter identity_anchor; Research question, objectives, and core hypothesis > Primary research question"
    revised_locator: "YAML frontmatter identity_anchor; H1; Research question, objectives, and core hypothesis > Primary research question"
    semantic_status: preserved
    evidence: >-
      v046 的身份锚点逐字段保留原核心问题、主要目标、研究对象、证据基础和推断单位；正文仍以脓毒症发病前在险期、首次发病、发病后互斥状态与结局的连续体为对象，并明确跨数据库状态与结构检验以及观察性表征与治疗因果效应的边界。题名缩短未把研究收缩为普通临床预测或泛 ICU 风险分层。
  - protected_id: PCR-002
    prior_locator: "YAML frontmatter identity_anchor.primary_objective; Research question, objectives, and core hypothesis > Objectives; authorized source_context_locator in the frozen register"
    revised_locator: "YAML frontmatter identity_anchor.primary_objective; Title, summary, audience, and positioning > Positioning and contribution frame; Research question, objectives, and core hypothesis > Objectives; Expected outputs, falsification criteria, and interpretations > 计划产物; Contribution, innovation, impact, application, and closest-work comparison > 正向贡献与证据层次"
    semantic_status: preserved
    evidence: >-
      v046 保留三项独立承诺：二十四个月内完成主体研究，对受文献与专家知识约束的候选表征开展公共 ICU 数据分析、系统辨识和跨数据库检验；交付可审查科学证据与高水平论文；产物不收缩为单一预测工具。高水平论文与“不是只产出预测工具”来自冻结登记已授权的上下文值，未被改写为已有成果。
  - protected_id: PCR-003
    prior_locator: "YAML frontmatter identity_anchor.study_object and primary_unit_of_inference; Research design and methods"
    revised_locator: "YAML frontmatter identity_anchor.study_object and primary_unit_of_inference; Structured abstract > Objective and hypothesis; Research design and methods > 两项主要临床任务的预定分析规则; 观察性目标、状态锚定与弃权规则"
    semantic_status: preserved
    evidence: >-
      研究对象仍是纵向、以脓毒症为中心的 ICU 患者系统，同时包含尚未发病的在险时段和发病后轨迹；主要推断单位仍是患者—时间状态及状态转移。v046 在两项主要任务和不确定性处理中继续要求患者与医院层面的聚类处理，没有改成单次住院、单个时间点或医院层面的不同推断对象。
  - protected_id: PCR-004
    prior_locator: "Data, materials, and existing evidence base > Current verified-resource versus prospective-gate status; Public ICU database roles and G1 audit"
    revised_locator: "Data, materials, and existing evidence base > 现有资源与计划要求的证据状态; 公共 ICU 数据库角色与 G1 可观测性审计; Feasibility, resources, risks, alternatives, and stop conditions > 可行性与资源"
    semantic_status: preserved
    evidence: >-
      v046 保留文献与专家先验、MIMIC-IV v3.1、eICU-CRD v2.0，以及须在月 0–3 预先指定的 HiRID 或 AmsterdamUMCdb 条件性备份。数据库存在和版本仍是已核验状态；团队访问资格、数据使用协议、可运行提取、存储和具名人员仍未核验；项目特异 G1 支持、候选模型、模拟、预测和外部结果仍尚未生成。共同生理测量的支持规则也未改变，包括每个维度至少两项测量、每项在两库至少 30% 合格时间区间实测并覆盖至少 70% 合格医院和 80% 合格患者，以及开发和外部每个自由参数分别至少 20 和 10 个事件或转移。
  - protected_id: PCR-005
    prior_locator: "Data, materials, and existing evidence base > Local RCT evidence and present limits"
    revised_locator: "Data, materials, and existing evidence base > 现有资源与计划要求的证据状态; 本地随机试验证据的当前状态; Research design and methods > 条件性随机试验次要分析：实测变量映射、独立临床状态分析与停止规则"
    semantic_status: preserved
    evidence: >-
      EXIT-SEP 与 XBJ-SCAP 仍只是在主体研究之后可能使用的个体级随机试验来源；衍生清洗或验证报告没有被提升为分析授权、原始病例报告表或统计分析计划，也没有替代随机化、中心、访视时序及死亡、住院和出院语义核验。资源计数保持不变：EXIT-SEP 为随机 1,817 人、28 日状态明确 1,760 人、死亡 395 人、状态未知 57 人，SOFA 第 1/4/7 日为 1,750/1,542/1,296，乳酸由 855 降至 223；XBJ-SCAP 为随机 710 人、FAS 675 人、PPS 617 人、操作性脓毒症样人群 671 人、严格重叠 658 人，SOFA 为 703/628/610，WBC 为 704/634/614，CRP 为 579/503/467，28 日状态明确 675 人。结构性缺失字段和未核验的 D-dimer 单位仍不得推测或填造。
  - protected_id: PCR-006
    prior_locator: "Research content and work packages; Research design and methods, including Observational target, anchoring, missingness and abstention"
    revised_locator: "Research content and work packages > 工作包与最小实施顺序; Research design and methods > 观察性目标、状态锚定与弃权规则; 基于预设生成情景和半合成数据的模拟可恢复性检验; 以医院为划分单位的跨数据库检验; 条件性随机试验次要分析"
    semantic_status: preserved
    evidence: >-
      实施依赖仍按资源与 G1、标签/状态/医院划分、竞争风险和多状态基线、线性状态空间、模拟可恢复性、至多一个复杂候选、两项主要任务与两项次要诊断、固定开发选择、独立外部检验的顺序推进，随机试验分析只能随后条件性开展。X_t、Y_t、A_t、M_t 与 B 的角色继续分离；K≤4、状态体制数≤3、滞后限 1 或 2 个时间区间。模拟仍要求每个核心情景至少 1,000 次重复或关键比例 Monte Carlo 标准误≤0.02，并保留状态重建≥0.80、转移 MAE≤0.05、95% 覆盖率 0.90–0.98、符号/滞后重建率≥0.80、灵敏度≥0.80、FDR≤0.10、零边假结构率≤0.05、错设识别与弃权≥80%、高置信错误结构≤0.05、校准斜率 0.80–1.20 和绝对概率偏差≤0.02 等判据。任一状态或关系在 20 个随机种子中的对应率<90%、自助法保留率<80%、外部符号一致率<80%、跨库状态对应<0.70 或区间未校准时，仍须删除、合并或标为数据库/照护政策特异；预测表现不能豁免这些处置。
  - protected_id: PCR-007
    prior_locator: "Research content and work packages > Conjunctive minimum success definition; Research design and methods > Hospital-primary genuine cross-database validation"
    revised_locator: "Research content and work packages > 主体研究的合取成功定义; Research design and methods > 以医院为划分单位的跨数据库检验; Expected outputs, falsification criteria, and interpretations > 证伪与停止判据; 工作包与最小实施顺序 > 工作包 5"
    semantic_status: preserved
    evidence: >-
      合取成功仍同时要求双库数据支持、正确指定/零边/核心错设情景中的模拟可恢复性、两项主要任务的严格适当评分与校准、无未解决的高严重度泄漏，以及完全不更新的独立外部验证、跨库状态对应和结构符号稳定。任务判据仍为 Brier 差值上侧 95% 置信界不超过 +0.01、校准斜率 0.80–1.20、绝对风险误差≤0.02；外部测试集仍须至少 20 个合格医院，状态相关或一致性系数≥0.70，结构符号一致率≥0.80。仅重新校准、仅更新观测模型或全模型重新拟合仍分开报告，均不能替代完全不更新的失败；二十四个月后的试验结果也不计入或补足主体研究的合取成功。
  - protected_id: PCR-008
    prior_locator: "Research design and methods > Protocol locks for the two primary clinical tasks; Mutually exclusive post-onset state/event system"
    revised_locator: "Research design and methods > 两项主要临床任务的预定分析规则; 发病后互斥临床状态与事件; 两项主要任务表后的敏感性标签与信息泄漏检查"
    semantic_status: preserved
    evidence: >-
      两项主要临床任务、临床事件时刻与信息可用时刻、首次发病风险集、延迟进入、互斥发病后状态、竞争终止、当时可用特征、严格适当评分和校准目标及患者/医院聚类不确定性均未改变。感染配对仍是先采集标本则抗菌药在随后 72 小时内、先给抗菌药则标本在随后 24 小时内；无慢性器官功能障碍时基线 SOFA=0，有记录时取入 ICU 前 24 小时最低可计算值；各组成取滚动 24 小时最差值，并以感染前 48 小时至后 24 小时内首次可排序的 SOFA 增加≥2 定义发病。仍只分析首次发病，重叠评估时点的单次住院总权重为 1；每 12 小时评估，发病前使用至多 24 小时且至少 12 小时历史并预测未来 12 小时，发病后以第 7 日为主、第 14 日为敏感性。A_t 与下一状态的区间顺序、同时间戳不可排序关系的排除，以及同区间治疗、未来测量频率、重复住院、跨分区处理和结局驱动变量、时间方案或阈值的泄漏检查均可定位。
  - protected_id: PCR-009
    prior_locator: "Structured abstract; Contribution, innovation, impact, application, and closest-work comparison > Contribution and evidence ladder"
    revised_locator: "Structured abstract > Expected result and Contribution and impact; Data, materials, and existing evidence base > 现有资源与计划要求的证据状态; Contribution, innovation, impact, application, and closest-work comparison > 正向贡献与证据层次; 最接近工作的代表性比较; Title and positioning claim-support table"
    semantic_status: preserved
    evidence: >-
      v046 仍把候选模型、模拟重建、外部验证和随机试验新分析明确标为尚未生成。可支持的贡献仍限于条件性的证据整合、跨数据库验证、可复用基准与研究资源；各单项模块已有先例。完整组合的负向检索判断仍只有低至中等置信，并限定为截至 2026-07-17 的有界代表性检索尚未找到，而非证明相关工作不存在。新算法、全球首次、已经验证的系统或临床效用等更强主张仍被排除。
  - protected_id: PCR-010
    prior_locator: "Feasibility, resources, risks, alternatives, and stop conditions; Research design and methods; Expected outputs, falsification criteria, and interpretations"
    revised_locator: "Feasibility, resources, risks, alternatives, and stop conditions > 可行性与资源; 尚待确认的工作假设; 限制与适用边界; 风险、替代方案与停止条件; Research design and methods 的相应权威小节; Expected outputs, falsification criteria, and interpretations > 证伪与停止判据; 结果解释矩阵"
    semantic_status: preserved
    evidence: >-
      第 14 节集中保留资源与访问、人员承诺、G1 支持、标签与泄漏、状态与关系的可恢复性、非随机缺失与低治疗支持、完全不更新的外部验证、时间节点、试验数据与语义、共同生理测量与观测代理关系以及最接近工作不确定性等限制。尚待确认的工作假设仍分别列出临床尺度到模拟参数的精确映射，以及多类别校准估计量、置信界和判定阈值的精确定义；事件/转移筛选下限仍不能替代经验有效样本量和模拟稳定性评价。各设计资格、互斥分支及其失败后的替代或停止后果保留在相应方法小节，结果证伪和结果依赖解释保留在计划产物与解释章节。两项试验方向不一致或区间过宽时仍只能报告无支持或跨场景适用性有限，不能通过选择亚组改变主要解释。
  - protected_id: PCR-011
    prior_locator: "Research content and work packages > Twenty-four-month minimum and dated gates; Identity and final stop boundary"
    revised_locator: "Research content and work packages > 二十四个月主体研究与时间节点; 工作包与最小实施顺序 > 工作包 5; Research design and methods > 条件性随机试验次要分析及其 R0、确定性映射、R1、观测代理结局、独立临床状态和试验表; Evidence chains > 条件性随机试验访视结局; Required analyses and evidence; Expected outputs > 计划产物; Title and positioning claim-support table; Feasibility, resources, risks, alternatives, and stop conditions"
    semantic_status: preserved
    evidence: >-
      阶段 I–II 对应的主体研究仍须在 24 个月内完成，试验分析位于 24 个月后且以主体研究成功、个体数据授权和核心试验语义可核验为共享前提。方法权威位置先陈述共享前提，再给出三种互斥去向：R0/R1 通过时分析基于冻结观测方程的一维观测代理；共同测量不足或适用性检验失败、但 SOFA 与核心语义成立时分析与候选表征独立的临床状态；核心访视、随机化、中心或生存语义不能核验时停止新的访视状态结局。R0 仍要求每项试验至少两项合格共同生理测量；R1 仍要求第一奇异轴能量≥50%、P_state 与 P_obs 相关≥0.70、标准化 MAE≤0.50、|α|≤0.20 个标准差、β 为 0.80–1.20、95% 覆盖率为 0.90–0.98、各测量校准斜率 0.80–1.20 且标准化截距绝对值≤0.20、至少 80% 实测值在合理范围、至少 60% 存活在院者能以不少于两项实测值计算 P_obs；任一门失败均不能由组间差异挽救。第 7/8 日、EXIT 1,817 人与 XBJ-SCAP 710 人的主要分析边界、Holm 家族错误率 0.05、缺失敏感性 δ=±0.5/±1 个标准差和停止规则也未改变。标题与结构化摘要只作高层条件性预告；研究问题、目标、时间表、证据链、分析清单、计划产物、贡献和主张表分别只保留其本节功能所需的信息。任何试验结果仍不能补足主体研究失败。
  - protected_id: PCR-012
    prior_locator: "Research question, objectives, and core hypothesis > Core hypothesis and non-hypotheses; Feasibility, resources, risks, alternatives, and stop conditions"
    revised_locator: "Research question, objectives, and core hypothesis > Core hypothesis and non-hypotheses; Feasibility, resources, risks, alternatives, and stop conditions > 限制与适用边界，第 10 项 因果与转化边界; Expected outputs, falsification criteria, and interpretations > 结果解释矩阵; Title and positioning claim-support table"
    semantic_status: preserved
    evidence: >-
      第 14 节的完整边界继续排除真实因果网络、治疗因果效应、反事实政策、机制、中介、控制策略和数字孪生；随机试验次要分析仍不能验证未测潜在动态、状态转移或完整模型。当前研究仍不得写成已经验证的模型、临床决策工具、药物开发平台或无条件临床推广依据。其他章节只在邻近的估计目标、结果解释或主张核查处保留必要的局部边界，没有把条件性计划改写成更强结论。
undeclared_scientific_changes: []
findings: []
unresolved_issues: []
---

# Content-preservation check

## Decision rationale

v046 对 v003 的变更均可归入标题与摘要压缩、章节重排、概念定义、技术内容集中和重复限制合并。冻结登记中的 PCR-001 至 PCR-012 均能在修订稿中找到同等语义、同等证据状态和同等主张强度的权威位置；所列数值、时间规则、阶段与组件依赖、条件性分支、失败后的替代或停止后果均未改变。修订说明明确声明没有科学变更，四个输入之间也未发现未声明的科学新增、删减或强化。

## Protected-content trace

- 研究身份和主要推断单位保留在 YAML 身份锚点，并在研究问题和方法中展开。
- 两项主要临床任务、模拟可恢复性、跨数据库检验及其全部数值判据集中在主体研究的方法权威位置。
- 条件性随机试验扩展的共享前提、R0/R1、观测代理分支、独立 SOFA 分支和语义不足停止分支集中在随机试验方法小节；摘要与其他章节只保留各自功能所需的高层信息。
- 完整工作假设、限制、因果与转化边界集中在第 14 节；结果证伪与结果依赖解释保留在计划产物和解释章节。
- 资源、授权、数据语义与结果状态仍按“已核验”“未核验”“尚未生成”区分，没有把计划工作表述为已经完成。

## Required routing

修订稿可以进入全新的叙事与学术语言评估，无须返回科学评审。
