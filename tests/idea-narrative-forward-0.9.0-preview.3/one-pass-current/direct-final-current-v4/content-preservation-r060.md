---
schema_version: research-idea-content-preservation-check.v1
check_id: content-preservation-I01-001-v003-to-v037-r060
review_id: content-preservation-review-I01-001-r060
reviewer_skill: idea-narrative-assessor
reviewer_instance_id: fresh-content-preservation-r060
workflow_id: RID-SEPSIS-CSM-20260717-001
round_id: r060
input_artifact_ids:
  - idea-dossier-I01-001-v003
  - idea-dossier-I01-001-v037
  - protected-content-register-I01-001-v003-r003
  - revision-delta-I01-001-v003-to-v037
input_versions:
  - v003
  - v037
  - r003
  - v003-to-v037
inputs:
  prior_dossier:
    artifact_id: idea-dossier-I01-001-v003
    version: v003
    path: tests/idea-test-0.9.0-preview.1/0.9.0-preview.1/03_ideas/nodes/I01-001/dossiers/idea-dossier-v003.md
  revised_dossier:
    artifact_id: idea-dossier-I01-001-v037
    version: v037
    path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v4/idea-dossier-v037.md
  protected_content_register:
    artifact_id: protected-content-register-I01-001-v003-r003
    version: r003
    path: tests/idea-narrative-forward-0.9.0-preview.3/run-001/inputs/protected-content-register-v003.yaml
  revision_delta:
    artifact_id: revision-delta-I01-001-v003-to-v037
    version: v003-to-v037
    path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v4/revision-delta-v003-to-v037.md
files_read:
  - tests/idea-test-0.9.0-preview.1/0.9.0-preview.1/03_ideas/nodes/I01-001/dossiers/idea-dossier-v003.md
  - tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v4/idea-dossier-v037.md
  - tests/idea-narrative-forward-0.9.0-preview.3/run-001/inputs/protected-content-register-v003.yaml
  - tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v4/revision-delta-v003-to-v037.md
isolation_mode: fresh_subagent
prior_scores_visible: false
source_edits_performed: false
decision: scientific_content_preserved
protected_item_checks:
  - protected_id: PCR-001
    prior_locator: "YAML frontmatter identity_anchor; Research question, objectives, and core hypothesis > Primary research question"
    revised_locator: "YAML frontmatter identity_anchor; Title, summary, audience, and positioning; Research question, objectives, and core hypothesis > Primary research question; Feasibility, resources, risks, alternatives, and stop conditions > Identity and final stop boundary"
    semantic_status: preserved
    evidence: >-
      v003 与 v037 均把研究身份限定为以脓毒症为中心的 ICU 全病程候选动态系统表征，覆盖未发病在险时段、首次发病、发病后互斥状态演化以及出 ICU 或死亡等结局。v037 的主问题仍以患者时间状态及状态转移为对象，并在最终身份边界明确排除普通预测和泛 ICU 风险分层；标题增加“患者状态及转移”是对象的展开说明，不改变研究身份。
  - protected_id: PCR-002
    prior_locator: "YAML frontmatter identity_anchor.primary_objective; Research question, objectives, and core hypothesis > Objectives"
    revised_locator: "YAML frontmatter identity_anchor.primary_objective; Structured abstract > Objective and hypothesis; Research question, objectives, and core hypothesis > Objectives; Research content and work packages; Expected outputs, falsification criteria, and interpretations > Planned outputs"
    semantic_status: preserved
    evidence: >-
      v037 保留阶段 I–II 必须在 24 个月内完成的目标，并保留文献与专家先验、公共 ICU 纵向数据、系统辨识与尺度约束、模拟恢复、时间外/医院外/未触碰跨数据库检验和全过程状态表征。计划产物仍面向高水平论文和可审计科学证据，而非仅产出预测工具。
  - protected_id: PCR-003
    prior_locator: "YAML frontmatter identity_anchor.study_object and primary_unit_of_inference; Research design and methods"
    revised_locator: "YAML frontmatter identity_anchor.study_object and primary_unit_of_inference; Research design and methods > 两个主要分析任务的固定规范; Feasibility, resources, risks, alternatives, and stop conditions > Identity and final stop boundary"
    semantic_status: preserved
    evidence: >-
      研究对象仍为纵向、以脓毒症为中心的 ICU 患者系统，包含可比较的未发病在险时段和发病后轨迹。主要推断单位仍是患者—时间状态及状态转移；每次住院总权重为 1，并继续以患者与医院两层 bootstrap 处理聚类不确定性。
  - protected_id: PCR-004
    prior_locator: "Data, materials, and existing evidence base > Current verified-resource versus prospective-gate status; Public ICU database roles and G1 audit"
    revised_locator: "Data, materials, and existing evidence base > 当前资源证据状态; 公共 ICU 数据库角色与 G1 可观测性审计; Feasibility, resources, risks, alternatives, and stop conditions > Feasibility and resources; 尚待核验的规格与执行条件"
    semantic_status: preserved
    evidence: >-
      核心输入仍为文献/专家先验、MIMIC-IV v3.1 与 eICU-CRD v2.0；HiRID 或 AmsterdamUMCdb 仍只能在月 0–3 预先指定并经同等审计后作为备份。v037 仍只把数据库公开存在和版本列为已核实；团队凭证、DUA、可运行提取、项目队列支持、具名人员与工时均为未核实，候选模型、模拟恢复、外部检验和 RCT 新分析结果均为尚未生成，未出现资源状态升级。
  - protected_id: PCR-005
    prior_locator: "Data, materials, and existing evidence base > Local RCT evidence and present limits"
    revised_locator: "Data, materials, and existing evidence base > 当前资源证据状态; 本地 RCT 证据及当前限制; Research design and methods > 条件性试验跨数据映射与阶段 II 模型独立的 SOFA 访视结局分析; Feasibility, resources, risks, alternatives, and stop conditions > Feasibility and resources"
    semantic_status: preserved
    evidence: >-
      EXIT-SEP 与 XBJ-SCAP 仍只是条件性阶段 III 的潜在个体级数据来源。v037 原样保留两项试验的样本、访视与缺失计数及其用途边界，并继续把现有本地材料限定为项目内衍生清洗或验证报告；它们不能替代个体数据授权、原始 CRF/SAP、随机化、中心、实际访视时序以及死亡、生存、住院、出院和转院语义核验。
  - protected_id: PCR-006
    prior_locator: "Research content and work packages; Research design and methods, including Observational target, anchoring and abstention"
    revised_locator: "Research content and work packages > 工作包及最小顺序; Data, materials, and existing evidence base > 变量角色分离; Research design and methods > 观察性目标、预设识别与尺度约束、状态对齐和停止解释; 预设模拟恢复与不当高置信标准; 医院优先、未触碰的跨数据库检验; 条件性试验跨数据映射与阶段 II 模型独立的 SOFA 访视结局分析"
    semantic_status: preserved
    evidence: >-
      v037 保留资源/G1→标签、状态与医院拆分→竞争风险和多状态基线→线性状态空间→模拟恢复与不当高置信检查→至多一个切换或非线性候选→两个主要任务和两个次要诊断→开发冻结→未触碰外部检验→条件性试验核验的顺序，并继续分离 Y_t、A_t 与 M_t。停止解释规则完整保留：20 个随机种子对齐率<90%、bootstrap 保留率<80%、外部符号一致率<80%、状态对齐<0.70 或区间未校准时，须删除、合并或标为仅数据库/照护政策特异；较好预测不能豁免。模拟重复数、Monte Carlo 标准误、恢复误差、覆盖、FDR、假关系和校准等绝对标准亦逐项相同。
  - protected_id: PCR-007
    prior_locator: "Research content and work packages > Conjunctive minimum success definition; Research design and methods > Hospital-primary genuine cross-database validation"
    revised_locator: "Research content and work packages > 阶段 II 的合取成功定义; Research design and methods > 医院优先、未触碰的跨数据库检验; Feasibility, resources, risks, alternatives, and stop conditions > Limitations and boundary conditions; Identity and final stop boundary"
    semantic_status: preserved
    evidence: >-
      阶段 II 成功仍是数据支持、候选模型在正确/零边/错设情景中的模拟恢复、两个主要任务的 Brier 或多类别 Brier 与校准、严重泄漏清零、未触碰参数不更新外部检验、状态对齐和结构符号稳定性的合取结果。+0.01、0.80–1.20、0.02、至少 20 个测试医院、状态对齐≥0.70 和符号一致率≥0.80 等阈值不变。仅校准更新和仅观测层更新继续与参数不更新结果分开，不能替代其失败；阶段 III 不能计入、绕过或补足阶段 II。
  - protected_id: PCR-008
    prior_locator: "Research design and methods > Protocol locks for the two primary clinical tasks; Mutually exclusive post-onset state/event system"
    revised_locator: "Research design and methods > 两个主要分析任务的固定规范; 发病后互斥状态与事件系统; Required analyses and evidence"
    semantic_status: preserved
    evidence: >-
      两个主要临床任务、临床事件时间/信息可得时间双时钟、首次发病风险集、延迟进入、互斥发病后状态、竞争终止、as-of 取数、Brier/校准目标及患者与医院聚类均保留。培养在先时抗菌药须在其后 72 小时内、给药在先时标本须在其后 24 小时内；baseline SOFA、滚动 24 小时成分、感染前 48 小时至后 24 小时的 +2 规则及首个可排序时刻均不变。仍只分析首次发病，重叠预测时点每次住院总权重为 1；同一时间格内 A_t 与下一状态的顺序、无法排序的同时间戳转移排除，以及同窗治疗、未来测量频率、重复住院、跨拆分处理和结局驱动时间格/阈值的泄漏检查均有正文证据。
  - protected_id: PCR-009
    prior_locator: "Structured abstract; Contribution, innovation, impact, application, and closest-work comparison > Contribution and evidence ladder"
    revised_locator: "Structured abstract; Data, materials, and existing evidence base > 当前资源证据状态; Expected outputs, falsification criteria, and interpretations > Planned outputs; Contribution, innovation, impact, application, and closest-work comparison; Title and positioning claim-support table"
    semantic_status: preserved
    evidence: >-
      v037 明确候选模型、模拟恢复、预测、外部测试与 RCT 新分析均尚未生成，所有结果都是计划产物。贡献强度仍限于条件性的整合、验证、可复用基准/资源与研究治理；各单项模块已有先例，完整组合缺口仅有低至中等置信，不支持新算法或全球首次。RCT 正向结果从“有限随机化扰动”改写为同一按死亡/出院分层 P_obs 访视结局的随机组间差异；固定映射、排序、概率指数/获胜概率比较及禁止验证潜在动力学或整个模型的边界均未改变，因此没有新增或增强推断主张。
  - protected_id: PCR-010
    prior_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Resources and governance; Risk and automatic alternative matrix; Remaining execution gates; Identity and final stop boundary; Expected outputs, falsification criteria, and interpretations > Falsification and stop criteria"
    revised_locator: "Expected outputs, falsification criteria, and interpretations > Falsification criteria; Feasibility, resources, risks, alternatives, and stop conditions > Feasibility and resources; 尚待核验的规格与执行条件; Limitations and boundary conditions; Risks, alternatives, and stop conditions; Identity and final stop boundary"
    semantic_status: preserved
    evidence: >-
      v037 第 14 节集中保留访问/资源、具名团队与独立保管、G1 支持、标签与泄漏、状态恢复、MNAR 与低重叠、参数不更新外部检验、时间节点、RCT 数据与语义、共同参照测量/跨数据映射及最接近研究不确定性，并为每项失败保留备份、减少维度、改变时间格、删除/合并、停止解释、独立 SOFA 分支或停止新访视结局等后果。临床尺度到模拟参数的映射，以及精确多类别校准估计量、置信界和阈值登记仍明确待定；事件/参数筛选下限不能替代经验有效样本量和模拟稳定性。两项试验方向不一致或区间过宽时，只能报告支持不足或跨场景适用性有限，不能挑选亚组挽救结论。
  - protected_id: PCR-011
    prior_locator: "Research content and work packages > Twenty-four-month minimum and dated gates; Identity and final stop boundary"
    revised_locator: "Research content and work packages > 24 个月主体计划与时间里程碑; Feasibility, resources, risks, alternatives, and stop conditions > Limitations and boundary conditions; Risks, alternatives, and stop conditions; Identity and final stop boundary"
    semantic_status: preserved
    evidence: >-
      阶段 I–II 仍须在 24 个月内完成，月 0–3、4–6、7–12、13–18/20、21–24 及 24 月后的里程碑和停止后果均保留。阶段 III 仍位于最低交付之外，须在阶段 II 成功后按试验数据、核心语义和预设跨数据映射/独立分支条件开展；任何后续试验结果均不能补足资源、模拟恢复、主要任务或未触碰外部检验失败。
  - protected_id: PCR-012
    prior_locator: "Research question, objectives, and core hypothesis > Core hypothesis and non-hypotheses; Feasibility, resources, risks, alternatives, and stop conditions"
    revised_locator: "Structured abstract > Contribution and impact; Expected outputs, falsification criteria, and interpretations > Interpretation matrix; Feasibility, resources, risks, alternatives, and stop conditions > Limitations and boundary conditions; Title and positioning claim-support table"
    semantic_status: preserved
    evidence: >-
      v037 继续明确：观察性数据和预测表现不能识别真实因果网络、治疗因果效应、反事实策略、机制、中介、控制或数字孪生；条件性 RCT 次要分析也不能验证未测潜在动力学、状态转移或整个阶段 II 模型。当前计划仍不得表述为已经验证的模型、临床决策工具、药物平台或无条件临床推广依据。
undeclared_scientific_changes: []
findings: []
unresolved_issues: []
---

# Content-preservation check

## Decision rationale

结论为 `scientific_content_preserved`。冻结 register 中 PCR-001 至 PCR-012 均在 v037 正文中具有可识别的新位置，研究身份、推断对象、资源与证据状态、设计顺序、分析目标、数值标准、失败解释、主张强度和停止边界均保持原意。章节拆分、术语展开、重复限制集中到第 14 节，以及把 RCT 的“有限扰动”改写为同一正式估计目标下的“随机组间访视结局差异”，属于编辑性重述，没有改变公式、排序、分析集、估计量或允许解释。

revision delta 只用于检查作者是否声明科学变更和确认产物血缘；其中的保留自述没有作为本报告的正文证据。所有判定均来自 v003 与 v037 正文的直接语义比较。本报告不评价研究设计本身是否正确或可行。

## Protected-content trace

### 数值与时间规则

- 时间与数据支持规则保持不变：阶段 I–II 为 24 个月；月 3、6、7–12、18/20、21–24 的资源、审计、恢复、冻结和外部检验节点仍在。主要时间格仍为 12 小时，审计不支持时只能在拟合和外部结果访问前改锁 24 小时或事件时间。每个自由风险/转移参数的开发/外部支持仍为 20/10 个事件或转移；每个共同维度至少两个参照测量，每项在两库至少 30% 合格时间格实测，并覆盖至少 70% 合格医院和 80% 合格患者；K≤4，状态机制数≤3。
- 主要任务规则保持不变：培养先于给药时为后 72 小时内、给药先于培养时为后 24 小时内；baseline SOFA 使用 0 或入 ICU 前 24 小时最低可计算值，成分取滚动 24 小时最差值，+2 发生窗为感染前 48 小时至后 24 小时。首次预测从 ICU 第 12 小时起每 12 小时更新，使用最多 24 小时且至少 12 小时历史，预测未来 12 小时；发病后主要观察到第 7 日，第 14 日为敏感性分析。Brier 非劣界 +0.01、校准斜率 0.80–1.20 和绝对风险误差≤0.02 均不变。
- 状态识别、缺失和恢复规则保持不变：首参照测量载荷 +1，滞后只允许 1 或 2 个时间格，使用 20 个固定随机种子；MNAR delta 为 −1、−0.5、0、+0.5、+1 个开发库标准差；行动比例<5% 或>95% 或加权 ESS<20% 时停止治疗作用解释。模拟每核心情景至少 1,000 次或至 Monte Carlo 标准误≤0.02；ARI/典型相关≥0.80、转移 MAE≤0.05、95% 覆盖 0.90–0.98、关系恢复率≥0.80、灵敏度≥0.80、FDR≤0.10、假关系排除 0 的比例≤0.05、错设识别/停止解释比例≥80%、错误结构高置信比例≤0.05 及概率校准标准均保留。
- 外部检验规则保持不变：固定种子 20260717，eICU 医院 30% 进入适配区、70% 进入未触碰测试区；测试区至少 20 个合格医院，每个自由参数至少 10 个外部事件或转移，跨分区排除超过原合格测试患者或主要事件 10% 时触发备份或降级。状态对齐≥0.70、符号一致率≥0.80 仍进入阶段 II 合取判定。
- RCT 分支规则保持不变：每项试验至少两个合格共同参照测量；R1 仍要求第一奇异轴解释能量≥50%、P_state 与 P_obs 相关≥0.70、归一化 MAE≤0.50、|α|≤0.20 个标准差、β=0.80–1.20、95% 覆盖 0.90–0.98、各参照测量斜率 0.80–1.20 和标准化截距绝对值≤0.20；遮蔽试验数据中至少 80% 测量落入合理范围，至少 60% 的存活在院访视可由不少于两个实测参照测量计算 P_obs。EXIT-SEP 的 D7、XBJ-SCAP 的 D8、delta ±0.5/±1 个标准差、Holm 家族错误率 0.05 和分试验分析集规则均保留。

### 分支、失败解释与禁止挽救规则

- 简单基线先行、至多一个切换或非线性候选、失败后转回多状态/线性/仅预测的分析分支未变。模拟恢复、零边或错设检查失败时，较好的预测表现不能使候选模型重新获得结构解释。
- 未触碰测试区首先报告参数不更新结果；仅校准更新、仅观测层更新及迁移后再开发均单独标记。有限更新成功只支持适配后迁移，不能挽救参数不更新失败。
- R0/R1 满足时分析按死亡和出院分层、以 P_obs 排序的访视结局；共同参照测量或 R1 不满足但核心试验语义可核验时，转入与阶段 II 模型独立的 SOFA 访视结局；核心随机化、中心、D7/D8、生存或住院/出院语义不能核验时停止新访视结局分析。较好的随机组间差异不能挽救 R1 失败，任何 RCT 结果不能补足阶段 II 失败；试验方向不一致或区间过宽时也不能选择亚组挽救结论。

### 证据、资源、主张与可行性状态

- MIMIC-IV/eICU 的公开存在与版本仍是已核实；访问凭证、DUA、可运行提取、实际队列支持、具名人员和工时仍未核实；模型、模拟恢复、外部检验和 RCT 新分析仍尚未生成。两项 RCT 的本地材料仍仅为项目内衍生材料。
- 当前贡献仍限于条件性的整合、验证、可复用基准与资源。单项模块已有先例的判断保持高置信，完整组合缺口保持低至中等置信；新算法、全球首次、因果网络、机制、控制、数字孪生、临床决策工具、药物平台和无条件推广主张仍不受支持。
- 临床尺度到模拟参数的映射，以及精确多类别校准估计量、置信界和阈值登记仍为待解决执行条件；事件或参数筛选下限仍不能替代经验有效样本量和模拟稳定性。

## Required routing

v037 可进入全新的叙事与语言评估；无需因内容保真问题返回科学审查。
