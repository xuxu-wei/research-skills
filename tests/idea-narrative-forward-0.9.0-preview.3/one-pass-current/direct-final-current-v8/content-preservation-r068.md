---
schema_version: research-idea-content-preservation-check.v1
check_id: content-preservation-I01-001-r068
review_id: content-preservation-r068
reviewer_skill: idea-narrative-assessor
reviewer_instance_id: preservation-v042-independent-r068
workflow_id: RID-SEPSIS-CSM-20260717-001
round_id: round-001
input_artifact_ids:
  - idea-dossier-I01-001-v003
  - idea-dossier-I01-001-v042
  - protected-content-register-I01-001-v003-r003
  - revision-delta-I01-001-v003-to-v042
input_versions:
  - v003
  - v042
  - r003
  - v042
inputs:
  prior_dossier:
    artifact_id: idea-dossier-I01-001-v003
    version: v003
    path: tests/idea-test-0.9.0-preview.1/0.9.0-preview.1/03_ideas/nodes/I01-001/dossiers/idea-dossier-v003.md
  revised_dossier:
    artifact_id: idea-dossier-I01-001-v042
    version: v042
    path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v8/idea-dossier-v042.md
  protected_content_register:
    artifact_id: protected-content-register-I01-001-v003-r003
    version: r003
    path: tests/idea-narrative-forward-0.9.0-preview.3/run-001/inputs/protected-content-register-v003.yaml
  revision_delta:
    artifact_id: revision-delta-I01-001-v003-to-v042
    version: v042
    path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v8/revision-delta-v003-to-v042.md
files_read:
  - tests/idea-test-0.9.0-preview.1/0.9.0-preview.1/00_input/user-idea-v001.md
  - tests/idea-test-0.9.0-preview.1/0.9.0-preview.1/03_ideas/nodes/I01-001/dossiers/idea-dossier-v003.md
  - tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v8/idea-dossier-v042.md
  - tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v8/revision-delta-v003-to-v042.md
  - tests/idea-narrative-forward-0.9.0-preview.3/run-001/inputs/protected-content-register-v003.yaml
  - research-skills-openai/skills/idea-narrative-assessor/SKILL.md
  - research-skills-openai/skills/idea-narrative-assessor/references/content-preservation-contract.md
  - research-skills-openai/skills/idea-narrative-assessor/templates/content-preservation-check.md
  - research-skills-openai/skills/idea-narrative-assessor/templates/protected-content-register.yaml
isolation_mode: fresh_subagent
prior_scores_visible: false
source_edits_performed: false
decision: scientific_content_preserved
protected_item_checks:
  - protected_id: PCR-001
    prior_locator: "YAML frontmatter identity_anchor; Research question, objectives, and core hypothesis > Primary research question"
    revised_locator: "YAML frontmatter identity_anchor; Title, summary, audience, and positioning > One-sentence complete-Idea summary; Research question, objectives, and core hypothesis > Primary research question; paragraph after Objectives"
    semantic_status: preserved
    evidence: >-
      v003 将对象限定为以脓毒症为中心、覆盖发病前、首次发病、发病后状态与结局的候选动态系统表征，而非普通预测或泛 ICU 风险分层。v042 的 identity_anchor 五项与 v003 保持同值；摘要和主要研究问题直接保留“发病前在险时段、首次发病以及发病后生理恢复状态、持续恶化、器官衰竭、离开 ICU 或死亡结局”，并保留“不得把研究收缩为只产出一个预测工具”。研究对象始终限定为脓毒症全病程而非泛 ICU 风险。
  - protected_id: PCR-002
    prior_locator: "00_input/user-idea-v001.md > 不可改变的项目约束; idea-dossier-v003.md YAML frontmatter identity_anchor.primary_objective; Research question, objectives, and core hypothesis > Objectives"
    revised_locator: "Title, summary, audience, and positioning > One-sentence complete-Idea summary and Positioning and contribution frame; Research question, objectives, and core hypothesis > paragraph after Objectives; Expected outputs, falsification criteria, and interpretations > Planned outputs, item 6"
    semantic_status: preserved
    evidence: >-
      原始输入要求 24 个月内完成阶段 II、以文献和专家知识建模并以公共 ICU 数据检验，目标为高水平论文且不能只产出预测模型。v042 正文直接写明“主要目标是在 24 个月内完成阶段 I–II：以文献和专家知识约束候选结构，使用公共 ICU 数据开展系统辨识、跨数据库验证和全过程状态表征”，摘要承诺“可审计科学证据、高水平同行评议论文”，并在定位段、目标后段落和计划产物第 6 项重复“不把研究收缩为单一预测工具”的边界。
  - protected_id: PCR-003
    prior_locator: "YAML frontmatter identity_anchor.study_object and primary_unit_of_inference; Research design and methods"
    revised_locator: "YAML frontmatter identity_anchor.study_object and primary_unit_of_inference; Research question, objectives, and core hypothesis > paragraph immediately before Core hypothesis and non-hypotheses; Protocol locks for the two primary clinical tasks > Uncertainty"
    semantic_status: preserved
    evidence: >-
      v042 正文直接保留“研究对象是纵向、以脓毒症为中心的 ICU 患者系统，包括可比较的未发病在险时段和发病后轨迹；主要推断单位是患者—时间状态及状态转移，推断和不确定性分析均尊重患者与医院聚类”。两项主要任务继续使用患者和医院两层自助法；对应的 frontmatter 身份字段与 v003 同值。
  - protected_id: PCR-004
    prior_locator: "Data, materials, and existing evidence base > Current verified-resource versus prospective-gate status; Public ICU database roles and G1 audit"
    revised_locator: "Title, summary, audience, and positioning > One-sentence complete-Idea summary; Data, materials, and existing evidence base > Current resource and evidence status; Public ICU database roles and G1 audit; Feasibility, resources, risks, alternatives, and stop conditions > Feasibility and resources"
    semantic_status: preserved
    evidence: >-
      v042 仍以文献和专家先验、MIMIC-IV 与 eICU-CRD 的纵向公共 ICU 数据为核心输入，并规定 HiRID 或 AmsterdamUMCdb 只能作为月 0–3 预先指定且完成同等审计的备份。资源表将数据库存在与版本列为“已有公开资料支持”，将团队访问凭证、数据使用协议和可运行提取列为“尚未核验”，将 G1 队列、事件和接口支持及模型、模拟、预测、最终检验和试验新结果列为“尚未生成”；具名人员及工时仍为“尚未核验”，角色规范明确不等于人员承诺。
  - protected_id: PCR-005
    prior_locator: "Data, materials, and existing evidence base > Local RCT evidence and present limits"
    revised_locator: "Data, materials, and existing evidence base > Current resource and evidence status, randomized-trial rows; Local randomized-trial evidence and present limits; Research design and methods > Trial analyses after stage II, opening paragraph"
    semantic_status: preserved
    evidence: >-
      v042 把 EXIT-SEP 与 XBJ-SCAP 保持为最低交付之外、满足预设条件后才可使用的阶段 III 潜在个体级数据来源。资源表把现有本地报告标为“项目内衍生资料”，并直接说明其“不替代个体数据授权、原始病例报告表（CRF）或统计分析计划（SAP）”。试验资料段和阶段 III 方法开头继续要求核验随机化、分析集、中心或分层因素、D0/D1/D7/D8 相对随机化与首剂的访视时序，以及死亡、住院、活着出院和转院语义；核心语义不能核验时不开展新的访视结局分析。
  - protected_id: PCR-006
    prior_locator: "Research content and work packages; Research design and methods, including Observational target, anchoring, missingness and abstention"
    revised_locator: "Research content and work packages > Work packages and minimum route, final paragraph; Data, materials, and existing evidence base > Candidate variable-role separation; Research design and methods > Observational target, anchoring, missingness and abstention; Simulation and semi-synthetic reconstruction criteria"
    semantic_status: preserved
    evidence: >-
      v042 直接保留固定顺序：“资源与可观测性审计 → 标签、状态和医院分区锁定 → 竞争风险与多状态基线 → 线性状态空间基线 → 模拟重建检查 → 至多一个复杂候选模型 → 两项主要任务和两项次要诊断 → 开发方案冻结 → 最终检验医院集分析 → 满足共享前提后的试验次要分析”。Y_t、A_t、M_t、仅用于标签和 B 的角色仍分开。只解释对齐后的状态占用、转移、锚点预测及预设符号和滞后。正文逐项保留 20 个随机种子对齐率低于 90%、自助法保留率低于 80%、外部符号一致率低于 80%、状态对齐低于 0.70 或区间未校准时删除、合并或限于特定数据库或照护政策的后果，并明确“较好的预测表现不能抵消这些判定”；模拟表另保留各重建失败的删除、停止解释或转用简单模型后果。
  - protected_id: PCR-007
    prior_locator: "Research content and work packages > Conjunctive minimum success definition; Research design and methods > Hospital-primary genuine cross-database validation"
    revised_locator: "Structured abstract > Contribution and impact; Research content and work packages > Conjunctive minimum success definition; Research design and methods > Hospital-primary cross-database validation"
    semantic_status: preserved
    evidence: >-
      v042 将阶段 II 成功继续定义为数据支持、模拟重建、两项主要任务的恰当概率评分与校准、严重泄漏清零、最终检验医院集中不更新任何模型参数的表现、状态对齐和结构稳定性的合取。外部方法列出“不更新任何模型参数”“仅用适配医院集重新估计校准参数”“仅用适配医院集重新估计观测层参数”和“用目标数据库重新拟合全模型”四种状态，并明确有限参数结果须与不更新参数结果分开、不能替代后者；全模型重拟合只属于再开发。合取定义末句直接保留“阶段 III 不计入或补足上述合取成功”。
  - protected_id: PCR-008
    prior_locator: "Research design and methods > Protocol locks for the two primary clinical tasks; Mutually exclusive post-onset state/event system"
    revised_locator: "Research design and methods > Protocol locks for the two primary clinical tasks, complete table and following leakage paragraph; Mutually exclusive post-onset state and event system"
    semantic_status: preserved
    evidence: >-
      两项主要任务、临床事件时间与标签可用时间、首次发病风险集、延迟进入、互斥发病后状态、竞争终止、截至时点特征、校准与恰当概率评分目标以及患者和医院聚类不确定性均保留。事件规则仍为先采标本则 72 小时内给药、先给药则 24 小时内采标本；无慢性器官功能障碍记录者基线 SOFA=0，有记录者取入 ICU 前 24 小时最低可计算 SOFA；成分取滚动 24 小时最差值，SOFA 增加至少 2 分须位于感染前 48 小时至后 24 小时，首次可排序满足时刻为发病时间。正文仍规定只分析首次发病、重叠评估时点每次 ICU 住院总权重为 1；[t,t+12h) 新行动为 A_t，下一边界实测生理为下一状态，同时间戳不能排序者不用于该转移。通过标准继续使用 Brier 差值上侧 95% 界不超过 +0.01、校准斜率 0.80–1.20、绝对风险误差不超过 0.02。泄漏段直接检查同一时间段行动、未来测量频率、跨分区处理、患者或 ICU 住院跨集合、重叠窗口权重以及由结局决定的变量、时间网格或阈值；合取定义和 G1 表另保留重复住院不跨分区及首次合格住院规则。
  - protected_id: PCR-009
    prior_locator: "Structured abstract; Contribution, innovation, impact, application, and closest-work comparison > Contribution and evidence ladder"
    revised_locator: "Structured abstract > Expected result; Data, materials, and existing evidence base > Current resource and evidence status, current-result row; Title, summary, audience, and positioning > Positioning and contribution frame; Contribution, innovation, impact, application, and closest-work comparison > Contribution and evidence ladder and final closest-work paragraph; Title and positioning claim-support table"
    semantic_status: preserved
    evidence: >-
      v042 明确说明标签、模型、模拟重建、外部检验和试验分析均为计划产物，“不是现有模型、验证结果或试验新分析结果”；资源表把所有当前结果列为“尚未生成”。可辩护贡献仍限定为有条件的整合、验证以及基准与资源增量。最接近工作段保留各模块已有先例的高置信判断、完整组合缺口仅低至中等置信，并明确当前定位“不是新算法、首次数字孪生、首次控制模型或全球首次”；Claim-Support 表把全球首创和已形成因果或转化产品的主张列为“无支持”。
  - protected_id: PCR-010
    prior_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Resources and governance; Risk and automatic alternative matrix; Remaining execution gates; Identity and final stop boundary; Expected outputs, falsification criteria, and interpretations > Falsification and stop criteria"
    revised_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Feasibility and resources; Working assumptions; Limitations and boundary conditions; Risks, alternatives, and stop conditions; Identity and final boundary"
    semantic_status: preserved
    evidence: >-
      v042 在同一权威章节集中列出资源与访问、人员承诺、G1 支持、标签与泄漏、状态重建、非随机缺失与低重叠、不更新参数的外部检验、24 个月时间边界、试验数据与语义、共同锚点和观测映射、最接近工作不确定性以及不支持的因果与转化主张。风险表逐行保留访问不足、跨院患者、泄漏、重建失败、缺失或重叠不足、运输失败、阶段 III 共享前提、观测桥接、独立分析语义、试验不一致、时间和最接近工作外推的触发条件、有限替代和停止或主张后果。Working assumptions 仍将“临床尺度如何映射为模拟生成参数”及“精确的多类别校准估计量、置信界实现和判定标准登记格式”列为待定规范，不填入猜测值；其后直接保留“事件数或参数数下限不替代经验有效样本量与模拟稳定性”。试验方向不一致或区间过宽时仍只报告无支持或跨场景适用性有限，并明确不选择亚组改变结论。
  - protected_id: PCR-011
    prior_locator: "Research content and work packages > Twenty-four-month minimum and dated gates; Identity and final stop boundary"
    revised_locator: "Title, summary, audience, and positioning > One-sentence complete-Idea summary; Structured abstract > Approach; Research question, objectives, and core hypothesis > Primary research question and Objective 4; Research content and work packages > Twenty-four-month minimum and dated stages and WP5; Research design and methods > Trial analyses after stage II; Evidence chains > randomized-trial chain; Expected outputs > Planned outputs, item 5; Title and positioning claim-support table, trial rows; Feasibility, resources, risks, alternatives, and stop conditions > trial-risk rows and final branch paragraph"
    semantic_status: preserved
    evidence: >-
      v042 在所有规定位置均先写共享前提“阶段 II 成功、相应试验个体数据可用且核心试验语义可核验”，没有把观测桥接提升为整个阶段 III 的共享条件。随后并列两条路线：观测桥接额外满足 R0 共同锚点条件和 R1 时，比较随机分组在实际 D7 或 D8 访视一维投影摘要上的差异；观测桥接不成立但 SOFA、随机化、中心及生存和住院语义可核验时，仍进行独立于候选表征、按死亡和 SOFA 排序的试验特异性次要临床状态分析。若核心 D7/D8、随机化、中心或生存和住院语义不能核验，则不开展新的访视结局分析。摘要、研究问题、目标 4、24 月后时间行、WP5、方法权威段、第五证据链、计划产物第 5 项、Claim-Support 试验行及第 14 节均保持这一顺序；各处同时保留任何阶段 III 结果都不计入或补足阶段 II 数据、模拟重建、主要任务或跨数据库要求的边界。
  - protected_id: PCR-012
    prior_locator: "Research question, objectives, and core hypothesis > Core hypothesis and non-hypotheses; Feasibility, resources, risks, alternatives, and stop conditions"
    revised_locator: "Research question, objectives, and core hypothesis > Core hypothesis and non-hypotheses; Structured abstract > Contribution and impact; Research design and methods > projection-summary and independent-analysis subsections; Expected outputs > Interpretation matrix; Feasibility, resources, risks, alternatives, and stop conditions > Limitations and boundary conditions, item 9; Title and positioning claim-support table, final row"
    semantic_status: preserved
    evidence: >-
      v042 直接保留“观察性关联或预测表现”不支持真实因果网络、治疗因果效应、反事实策略、机制、中介、控制或数字孪生的边界。试验投影摘要段和限制第 9 项明确说明试验次要分析不验证未测潜在动力学、转移边或候选表征整体；独立临床状态分支不得称为候选表征受到干预或得到验证。限制第 9 项还直接写明当前计划“不是已验证模型、临床决策工具、药物平台或无条件临床推广依据”，Claim-Support 最后一行将这些当前主张列为“无支持”。
undeclared_scientific_changes: []
findings: []
unresolved_issues: []
---

# Content-preservation check

## Decision rationale

结论为 scientific_content_preserved。冻结登记中的 PCR-001 至 PCR-012 均可在 v042 正文找到与 v003 相同含义、相同证据状态和相同主张强度的直接证据。数值与时间规则、失败解释、不可挽回条件及阶段 III 的共享前提和互斥分支均保留；表述替换、定义补充、移动、拆分、合并、重排和限制集中属于登记允许的编辑操作。revision delta 声明的是 editorial repair only，没有明示科学变更；该声明未被当作正文证据。

## Protected-content trace

- PCR-001 至 PCR-003：身份锚点、全病程范围、24 个月目标、论文与证据交付、研究对象及推断单位从原来的分散位置改为在摘要、研究问题和目标附近直接说明，含义未变。
- PCR-004 至 PCR-005：公共数据库和试验资料状态改为自然中文证据状态；公开存在、尚未核验、尚未生成及项目内衍生资料之间的边界未被加强，试验授权和原始语义要求未被删除。
- PCR-006 至 PCR-008：设计顺序、变量角色、模拟重建、外部检验、两项主要任务、全部数值判定标准和泄漏防护集中在研究设计方法中；没有把较好预测表现改成结构判定的替代证据。
- PCR-009：计划性证据状态、条件性贡献和低至中等置信的完整组合缺口仍受同一主张边界约束。
- PCR-010：限制、待定规范、替代方案和停止后果集中到 Feasibility, resources, risks, alternatives, and stop conditions；其他位置只保留直接限定相邻估计目标或分析资格所需的局部边界。
- PCR-011：摘要、问题、目标、时间表、方法、证据链、计划产物、Claim-Support 与限制权威位置均先写共享前提，再写观测桥接分支、独立临床状态分支和整体停止条件；阶段 III 不补足阶段 II。
- PCR-012：因果、机制、控制、数字孪生、临床工具、药物平台和无条件推广等不支持的主张类别继续明确排除。

## Protected-ID integrity check

- Frozen register IDs: PCR-001 through PCR-012, 12 total.
- Report checks: PCR-001 through PCR-012, 12 total, each represented exactly once in protected_item_checks.
- Missing IDs: none.
- Duplicate IDs: none.
- Unknown IDs: none.

## Required routing

该修订可进入新的叙事与学术语言评估。本报告只核验科学内容保存情况，不判断研究设计本身是否正确，也不替代后续独立评估。
