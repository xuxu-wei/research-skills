---
schema_version: research-idea-content-preservation-check.v1
check_id: content-preservation-I01-001-r006
review_id: content-preservation-review-I01-001-r006
reviewer_skill: idea-narrative-assessor
reviewer_instance_id: fresh-preservation-reviewer-I01-001-r006
workflow_id: RID-SEPSIS-CSM-20260717-001
round_id: r006
input_artifact_ids:
  - idea-dossier-I01-001-v008
  - idea-dossier-I01-001-v009
  - protected-content-register-I01-001-v008
  - revision-delta-I01-001-v008-to-v009
input_versions:
  - v008
  - v009
  - v008
  - v008-to-v009
inputs:
  prior_dossier:
    artifact_id: idea-dossier-I01-001-v008
    version: v008
    path: tests/idea-narrative-forward-0.9.0-preview.3/run-001/delivery/idea-dossier-v008.md
  revised_dossier:
    artifact_id: idea-dossier-I01-001-v009
    version: v009
    path: tests/idea-narrative-forward-0.9.0-preview.3/run-001/release/idea-dossier-v009.md
  protected_content_register:
    artifact_id: protected-content-register-I01-001-v008
    version: v008
    path: tests/idea-narrative-forward-0.9.0-preview.3/run-001/delivery/protected-content-register-v008.yaml
  revision_delta:
    artifact_id: revision-delta-I01-001-v008-to-v009
    version: v008-to-v009
    path: tests/idea-narrative-forward-0.9.0-preview.3/run-001/release/revision-delta-v008-to-v009.md
files_read:
  - tests/idea-narrative-forward-0.9.0-preview.3/run-001/delivery/idea-dossier-v008.md
  - tests/idea-narrative-forward-0.9.0-preview.3/run-001/release/idea-dossier-v009.md
  - tests/idea-narrative-forward-0.9.0-preview.3/run-001/delivery/protected-content-register-v008.yaml
  - tests/idea-narrative-forward-0.9.0-preview.3/run-001/release/revision-delta-v008-to-v009.md
isolation_mode: fresh_subagent
prior_scores_visible: false
source_edits_performed: false
decision: scientific_content_preserved
protected_item_checks:
  - protected_id: PCR-V008-001
    prior_locator: "YAML identity_anchor；标题；Title, summary, audience, and positioning；Primary research question"
    revised_locator: "YAML identity_anchor；标题；Title, summary, audience, and positioning（Three-stage map 与 One-sentence complete-Idea summary）；Primary research question"
    semantic_status: preserved
    evidence: >-
      两版 identity_anchor 的主要问题、主要目标、研究对象、核心证据基础和推断单位逐项相同；标题与主要研究问题仍以覆盖发病前、首次发病、发病后和结局的脓毒症候选动态系统模型为研究身份，而非普通临床预测或泛 ICU 风险模型。v009 新增的三阶段图把 v008 已有的 WP1 月 0–6、WP2 自月 3 起、WP2–WP4 至月 24 以及 WP5 在 24 月后的排期显式对应到阶段 I–III，仍要求阶段 I–II 在 24 个月内完成，未改变问题、目的或时间边界。
  - protected_id: PCR-V008-002
    prior_locator: "YAML identity_anchor；Primary research question；Protocol locks for the two primary clinical tasks；Observational model target, anchoring, and reporting"
    revised_locator: "YAML identity_anchor；Primary research question；Protocol locks for the two primary clinical tasks；Observational model target, anchoring, and reporting"
    semantic_status: preserved
    evidence: >-
      研究对象仍是纵向、以脓毒症为中心的 ICU 患者系统，包括可比的未发病风险时段与发病后轨迹。主要推断单位仍为患者—时间状态及状态转移；两项主要任务、互斥发病后状态、患者层和医院层聚类处理均未改变。v009 仅将共同观测指标、锚点、状态对齐和观测方程的定义移至模型小节并在首次使用处作简释，没有更换对象、系统边界或推断单位。
  - protected_id: PCR-V008-003
    prior_locator: "Data, materials, and existing evidence base；Current feasibility and evidence status"
    revised_locator: "Data, materials, and existing evidence base；Current feasibility and evidence status"
    semantic_status: preserved
    evidence: >-
      文献与专家先验、MIMIC-IV v3.1、eICU-CRD v2.0、预先指定的备份数据库以及条件性 EXIT-SEP 和 XBJ-SCAP 个体数据来源均保持不变。两版对访问凭证与数据使用协议标为未核验，对双数据库项目内样本、事件、转移、医院、共同指标和接口计数标为尚未生成，对试验材料仅认定为项目内衍生材料，并继续要求另行核验授权、原始试验文件和关键语义。v009 把“支持度审计”展开为变量覆盖、样本与事件充分性、允许转移数及治疗行动覆盖和重叠；这些对象在 v008 的审计表、方法和停止条件中已经存在，未新增数据或把待审计状态写成已经具备。
  - protected_id: PCR-V008-004
    prior_locator: "Research content and work packages；Research design and methods；Required analyses and evidence；Scientific falsification criteria；Operational thresholds, alternatives, and stop conditions"
    revised_locator: "Research content and work packages；Research design and methods；Required analyses and evidence；Scientific falsification criteria；Operational thresholds, alternatives, and stop conditions"
    semantic_status: preserved
    evidence: >-
      分阶段顺序、WP1–WP5、两项主要临床任务、两项次要表征诊断、发病前与发病后估计目标、模拟机制、跨数据库隔离验证、三层外部分析和条件性试验分析均保持相同。试验人群、分析集、访视、概率指数、缺失处理、Holm 家族和亚组交互规则只在重排后的表格列间迁移。所有核验到的数值标准及后果保持不变，包括事件与转移的 20/10 门槛、每个潜在维度至少 2 个共同锚点、状态维度不超过 4、切换机制不超过 3、1,000 次模拟与 MCSE 0.02、状态恢复 0.80、固定随机种子匹配率 90%、转移误差 0.05、区间覆盖 0.90–0.98、结构恢复 0.80、错误发现率 0.10、外部状态对齐 0.70、主要任务 Brier 差值上侧界 +0.01，以及观测映射各项门槛。科学证伪标准与失败后的简化、降级、停止或禁止替代后果均未改变。“失败图”改为按数据库和医院展示未达预设标准项目的分层分布图，“伪遮蔽重建”改为“遮蔽后重建检验”，均是对既有操作的定义性改写。
  - protected_id: PCR-V008-005
    prior_locator: "Structured abstract；Planned outputs；Contribution and evidence ladder；Title and positioning claim-support table；Current feasibility and evidence status"
    revised_locator: "Structured abstract；Planned outputs；Contribution and evidence ladder；Title and positioning claim-support table；Current feasibility and evidence status"
    semantic_status: preserved
    evidence: >-
      模型、模拟恢复、主要任务、外部验证和随机试验新分析在两版中均为计划产物；v009 继续明确“拟生成”“计划生成”或“尚未生成”，没有把计划中的验证写成已经完成。贡献仍限定为证据整合、预先设定的跨数据库验证、研究基准和可复用资源；完整组合缺口仍只有低至中等置信支持。主张支持表仅把 supported、qualified 和 none 的读者可见标签分别显示为“获得支持”“限定支持”和“无可主张增量”，各行边界、证据状态与主张强度不变。
  - protected_id: PCR-V008-006
    prior_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Authoritative limitations, feasibility findings, interpretation boundaries, alternatives, and stop conditions"
    revised_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Authoritative limitations, feasibility findings, interpretation boundaries, alternatives, and stop conditions"
    semantic_status: preserved
    evidence: >-
      v009 仍把第 14 节指定为当前可行性、限制、解释边界、替代方案和停止条件的唯一完整权威位置，并保留全部资源状态、七项科学与解释边界、治理范围以及操作阈值表。数据与人员不足、双数据库审计失败、泄漏未解决、模拟恢复或结构识别失败、主要任务失败、外部医院或结果不足、月 20/月 24 未完成、试验语义不明、共同变量不足、观测映射不忠实和随机试验结果不稳定时的替代、降级、禁止替代或停止后果均未删除或弱化。v009 顶部三阶段图明确重申阶段 III 不能补足阶段 II 的任何失败；其他邻近重复语句虽被压缩，完整条件仍只在权威小节保留一次，阶段 III 继续保持条件性。
  - protected_id: PCR-V008-007
    prior_locator: "Scientific and interpretive boundaries；Research identity and final boundary"
    revised_locator: "Scientific and interpretive boundaries；Research identity and final boundary"
    semantic_status: preserved
    evidence: >-
      七项科学与解释边界及最终研究身份边界逐项保留。观察性关联和预测表现仍不识别治疗因果效应、真实反馈网络或反事实策略；试验分支仍不验证未测潜在动力学、状态转移边、中介机制、个体控制或完整动态系统，也不支持无条件国际临床推广。对新算法、全球首次、数字孪生、控制模型、已验证临床决策工具和药物平台的禁止主张保持不变；有限更新不能替代不更新模型的外部验证失败，阶段 III 也不能补足阶段 II 失败。定义移动和术语统一没有扩大任何可支持主张类别。
undeclared_scientific_changes: []
findings: []
unresolved_issues: []
---

# Content-preservation check

## Decision rationale

判定为 `scientific_content_preserved`。七个保护项均能从 v008 定位到 v009，含义、主张强度、证据状态、数值阈值、关键限制和停止后果保持不变。修订说明所列操作与实际差异一致：三阶段关系被显式标注，技术定义被移至方法位置并在首次使用处简释，含混短语改为可观察对象，试验分析表改按同一字段顺序排列，固定状态标签改用中文显示。未发现修订说明之外的数据、方法、结果、证据或科学对象变化。

## Protected-content trace

| 保护项 | v009 中的定位与非平凡变动 | 保留结论 |
|---|---|---|
| PCR-V008-001 | YAML `identity_anchor`、标题、顶部三阶段图、主要研究问题；阶段名称与既有工作包月份显式对应 | 研究身份、全病程问题和 24 个月阶段 I–II 边界不变 |
| PCR-V008-002 | YAML `identity_anchor`、主要研究问题、两项主要任务方案、观测模型目标；技术定义移至观测模型小节 | 对象、范围、推断单位及患者/医院聚类不变 |
| PCR-V008-003 | 数据与材料小节、第 14 节当前可行性表；含混的审计术语展开为原有可观察量 | 数据来源、可用性、授权、语义和结果状态不变 |
| PCR-V008-004 | 工作包、研究方法、必需分析、证伪标准及第 14 节阈值表；术语定义和试验表格重排 | 方法顺序、估计目标、全部阈值、验证逻辑和阶段依赖不变 |
| PCR-V008-005 | 结构化摘要、计划产物、贡献阶梯、主张支持表和当前状态表；状态标签汉化 | 所有研究结果仍为计划产物，贡献与可行性主张未增强 |
| PCR-V008-006 | 第 14 节唯一完整权威小节；顶部只保留阶段 III 入口的必要摘要 | 限制、替代方案、停止条件及阶段 III 条件性均未弱化 |
| PCR-V008-007 | 第 14 节科学与解释边界及最终研究身份边界 | 因果、机制、控制、数字孪生和无条件应用等禁止主张不变 |

## Required routing

该稿可进入新的独立行文与学术语言复核，无需返回科学审查。
