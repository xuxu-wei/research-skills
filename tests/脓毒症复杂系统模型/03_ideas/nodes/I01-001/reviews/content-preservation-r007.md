---
schema_version: research-idea-content-preservation-check.v1
check_id: content-preservation-I01-001-r007
review_id: content-preservation-I01-001-r007
reviewer_skill: idea-narrative-assessor
reviewer_instance_id: fresh-scientific-content-preservation-checker-r007
workflow_id: sepsis-complex-system-idea-generation-v001
round_id: r007
input_artifact_ids:
  - idea-dossier-I01-001-v005
  - idea-dossier-I01-001-v006
  - protected-content-register-v002
  - revision-delta-I01-001-v005-to-v006
input_versions: [v005, v006, v002, v005-to-v006]
inputs:
  prior_dossier:
    artifact_id: idea-dossier-I01-001-v005
    version: v005
    path: 03_ideas/nodes/I01-001/dossiers/idea-dossier-v005.md
  revised_dossier:
    artifact_id: idea-dossier-I01-001-v006
    version: v006
    path: 03_ideas/nodes/I01-001/dossiers/idea-dossier-v006.md
  protected_content_register:
    artifact_id: protected-content-register-v002
    version: v002
    path: 05_state/protected-content-register-v002.yaml
  revision_delta:
    artifact_id: revision-delta-I01-001-v005-to-v006
    version: v005-to-v006
    path: 03_ideas/nodes/I01-001/revisions/round-005/revision-delta-v005-to-v006.md
files_read:
  - 03_ideas/nodes/I01-001/dossiers/idea-dossier-v005.md
  - 03_ideas/nodes/I01-001/dossiers/idea-dossier-v006.md
  - 05_state/protected-content-register-v002.yaml
  - 03_ideas/nodes/I01-001/revisions/round-005/revision-delta-v005-to-v006.md
isolation_mode: fresh_subagent
prior_scores_visible: false
source_edits_performed: false
identity_anchor_checks:
  - field: primary_research_question
    prior_locator: {section_heading: "frontmatter.identity_anchor", content_anchor: "primary_research_question"}
    revised_locator: {section_heading: "frontmatter.identity_anchor", content_anchor: "primary_research_question"}
    status: verbatim_match
    evidence: "v005、v006 与冻结登记表中的值逐字相同，标点与限定语均无变化。"
  - field: primary_objective
    prior_locator: {section_heading: "frontmatter.identity_anchor", content_anchor: "primary_objective"}
    revised_locator: {section_heading: "frontmatter.identity_anchor", content_anchor: "primary_objective"}
    status: verbatim_match
    evidence: "v005、v006 与冻结登记表中的值逐字相同，四任务与任务三边界均未变化。"
  - field: study_object
    prior_locator: {section_heading: "frontmatter.identity_anchor", content_anchor: "study_object"}
    revised_locator: {section_heading: "frontmatter.identity_anchor", content_anchor: "study_object"}
    status: verbatim_match
    evidence: "v005、v006 与冻结登记表中的值逐字相同，全病程研究对象未变化。"
  - field: core_data_or_evidence_base
    prior_locator: {section_heading: "frontmatter.identity_anchor", content_anchor: "core_data_or_evidence_base"}
    revised_locator: {section_heading: "frontmatter.identity_anchor", content_anchor: "core_data_or_evidence_base"}
    status: verbatim_match
    evidence: "v005、v006 与冻结登记表中的值逐字相同，约束表及两库证据基础未变化。"
  - field: primary_unit_of_inference
    prior_locator: {section_heading: "frontmatter.identity_anchor", content_anchor: "primary_unit_of_inference"}
    revised_locator: {section_heading: "frontmatter.identity_anchor", content_anchor: "primary_unit_of_inference"}
    status: verbatim_match
    evidence: "v005、v006 与冻结登记表中的值逐字相同，患者级汇总与患者间推断单位未变化。"
decision: scientific_content_preserved
protected_item_checks:
  - protected_id: PCR-001
    prior_locator: {section_heading: "## Research question, objectives, and core hypothesis", content_anchor: "**Primary research question.** 在成人重症监护感染风险患者中"}
    revised_locator: {section_heading: "## Research question, objectives, and core hypothesis", content_anchor: "**Primary research question.** 在成人重症监护感染风险患者中"}
    semantic_status: preserved
    evidence: >-
      人群、预先限定的低维全病程模型、一个开发库和一个异质外部库、四项预测任务及任务三不以潜在状态为真值的边界均相同；修订仅把外部状态比较明确写为开发状态在预定临床特征上的跨数据库可分离性。
  - protected_id: PCR-002
    prior_locator: {section_heading: "## Research question, objectives, and core hypothesis", content_anchor: "**Objectives.**"}
    revised_locator: {section_heading: "## Research question, objectives, and core hypothesis", content_anchor: "**Objectives.**"}
    semantic_status: preserved
    evidence: >-
      四项目标仍依次要求实施前约束与资源验收、开发期可辨识性与模型冻结、外部四任务平行评价，以及按通过任务和冻结状态规则限定结论；仅替换了外部状态诊断的名称和展开表述。
  - protected_id: PCR-055
    prior_locator: {section_heading: "## Research question, objectives, and core hypothesis", content_anchor: "**Core hypothesis.** 在所有实施前置条件满足且最小统一模型可辨识的条件下"}
    revised_locator: {section_heading: "## Research question, objectives, and core hypothesis", content_anchor: "**Core hypothesis.** 在所有实施前置条件满足且最小统一模型可辨识的条件下"}
    semantic_status: preserved
    evidence: >-
      四项外部患者级汇总损失均须低于各自比较模型、任务三仅以遮蔽实测值计分，以及必需开发状态须在同一组预定临床特征上跨数据库可分离，均保持原义与原强度。
  - protected_id: PCR-003
    prior_locator: {section_heading: "## Title, summary, audience, and positioning", content_anchor: "“动态状态模型”在本研究中指"}
    revised_locator: {section_heading: "## Title, summary, audience, and positioning", content_anchor: "“动态状态模型”在本研究中指"}
    semantic_status: preserved
    evidence: >-
      全病程边界、生理—观测—处置区分、文献—专家约束、冻结后由开发库直接应用至异质外部库及开放动态临床系统视角均保留；新增句只前置定义既有外部状态比较程序。
  - protected_id: PCR-004
    prior_locator: {section_heading: "## Research design and methods", subsection_heading: "### Unified full-course population, time axis, and state space", content_anchor: "统一训练样本从成人 ICU 住院中首次满足冻结感染风险入口的时点开始"}
    revised_locator: {section_heading: "## Research design and methods", subsection_heading: "### Unified full-course population, time axis, and state space", content_anchor: "统一训练样本从成人 ICU 住院中首次满足冻结感染风险入口的时点开始"}
    semantic_status: preserved
    evidence: >-
      队列入口和终点、未发病与发病患者的贡献、患者隔离与重复住院分割，以及五类状态空间组成在 v006 中逐项不变。
  - protected_id: PCR-005
    prior_locator: {section_heading: "## Title, summary, audience, and positioning", content_anchor: "本构想的实证核心是在 12–18 个月内完成"}
    revised_locator: {section_heading: "## Title, summary, audience, and positioning", content_anchor: "本构想的实证核心是在 12–18 个月内完成"}
    semantic_status: preserved
    evidence: >-
      12–18 个月仍仅涵盖一个开发库和一个异质外部库的构建、验证、复现与论文；随机试验和动物研究仍为时间表外的条件性后续，且方法段继续禁止其补救核心研究失败。
  - protected_id: PCR-056
    prior_locator: {section_heading: "## Title, summary, audience, and positioning", content_anchor: "- **Positioning and contribution frame:** 核心身份是统一全病程动态复杂系统模型的构建与外部验证"}
    revised_locator: {section_heading: "## Title, summary, audience, and positioning", content_anchor: "- **Positioning and contribution frame:** 核心身份是统一全病程动态复杂系统模型的构建与外部验证"}
    semantic_status: preserved
    evidence: >-
      同一冻结模型覆盖感染风险、首次发生和发病后演化，四项任务各自形成确认性假设，且不设跨任务总准确率或索引后统领指标；该定位段未发生科学变化。
  - protected_id: PCR-006
    prior_locator: {section_heading: "## Data, materials, and existing evidence base", subsection_heading: "### Pre-model constraint-table prerequisite", content_anchor: "主模型拟合前，约束表必须覆盖"}
    revised_locator: {section_heading: "## Data, materials, and existing evidence base", subsection_heading: "### Pre-model constraint-table prerequisite", content_anchor: "主模型拟合前，约束表必须覆盖"}
    semantic_status: preserved
    evidence: >-
      约束表覆盖范围、最低专家构成、利益冲突和缺席记录、先独立判断后匿名反馈、80% 支持门槛、临床与方法学双重支持及异议保存要求均未改变。
  - protected_id: PCR-007
    prior_locator: {section_heading: "## Data, materials, and existing evidence base", subsection_heading: "### Required inputs and database constitution", content_anchor: "12–18 个月核心实证研究固定使用一个公开成人重症监护纵向开发数据库"}
    revised_locator: {section_heading: "## Data, materials, and existing evidence base", subsection_heading: "### Required inputs and database constitution", content_anchor: "12–18 个月核心实证研究固定使用一个公开成人重症监护纵向开发数据库"}
    semantic_status: preserved
    evidence: >-
      两库的数量、公开性与异质性、月 1–2 资格程序、禁止按外部表现选库、开发库与外部库分工、独立性、6 小时网格及共同变量要求均相同；只将外部状态可分离性的对象写得更明确。
  - protected_id: PCR-008
    prior_locator: {section_heading: "## Data, materials, and existing evidence base", subsection_heading: "### Database, team, and compute qualification", content_anchor: "每个候选库均须报告共同变量及单位"}
    revised_locator: {section_heading: "## Data, materials, and existing evidence base", subsection_heading: "### Database, team, and compute qualification", content_anchor: "每个候选库均须报告共同变量及单位"}
    semantic_status: preserved
    evidence: >-
      真实样例审计项目、有效转移定义、五个核心角色、计算基准、替代或停止后果，以及以开发结构模拟确定信息量而不采用通用事件数硬阈值的规则均未变化。
  - protected_id: PCR-009
    prior_locator: {section_heading: "## Data, materials, and existing evidence base", subsection_heading: "### Required inputs and database constitution", content_anchor: "| 第三公开数据库 |"}
    revised_locator: {section_heading: "## Data, materials, and existing evidence base", subsection_heading: "### Required inputs and database constitution", content_anchor: "| 第三公开数据库 |"}
    semantic_status: preserved
    evidence: >-
      第三库仍仅在两库核心结果锁定后作可选压力测试且不进入 Holm 家族或总体判定；EXIT-SEP 与 XBJ-SCAP 仍为权限、逐时变量和功效未核实的条件性资源。
  - protected_id: PCR-057
    prior_locator: {section_heading: "## Key techniques and implementation", content_anchor: "2. **跨库概念协调：**"}
    revised_locator: {section_heading: "## Key techniques and implementation", content_anchor: "2. **跨库概念协调：**"}
    semantic_status: preserved
    evidence: >-
      每个共同概念须保存原始字段、单位、时间戳来源、聚合窗、异常值和缺失编码，且数据库特异变量不得进入主要跨库模型；该条在 v006 中未改动。
  - protected_id: PCR-010
    prior_locator: {section_heading: "## Research design and methods", subsection_heading: "### Unified full-course population, time axis, and state space", content_anchor: "持续恢复定义为存活"}
    revised_locator: {section_heading: "## Research design and methods", subsection_heading: "### Unified full-course population, time axis, and state space", content_anchor: "持续恢复定义为存活"}
    semantic_status: preserved
    evidence: >-
      持续恢复仍要求存活、脱离三类器官支持且六个器官功能域连续 24 小时不再恶化；其任务二首次事件地位、随后可恶化或出 ICU、存活出 ICU 不等同恢复，以及真实时间与 6 小时评分网格的区分均不变。
  - protected_id: PCR-011
    prior_locator: {section_heading: "## Research design and methods", subsection_heading: "### Primary model and task-specific comparators", content_anchor: "主要模型为受约束隐半马尔可夫全病程动态状态模型"}
    revised_locator: {section_heading: "## Research design and methods", subsection_heading: "### Primary model and task-specific comparators", content_anchor: "主要模型为受约束隐半马尔可夫全病程动态状态模型"}
    semantic_status: preserved
    evidence: >-
      隐半马尔可夫状态、停留时间、观测与观测过程、治疗作为时间变化输入及非因果治疗系数均不变；四任务各两个比较模型、相同分析输入和最不利损失差共同通过规则亦未改变。
  - protected_id: PCR-012
    prior_locator: {section_heading: "## Research question, objectives, and core hypothesis", content_anchor: "**Confirmatory family.**"}
    revised_locator: {section_heading: "## Research question, objectives, and core hypothesis", content_anchor: "**Confirmatory family.**"}
    semantic_status: preserved
    evidence: >-
      前置资格与统计假设分离、患者内先汇总、D_kc 与 Delta_k 定义、max-t、单侧 95% 上界、最大单侧 p 值、Holm 0.05、双侧区间及双条件通过规则在 v006 中逐字未变。
  - protected_id: PCR-013
    prior_locator: {section_heading: "## Research design and methods", subsection_heading: "### Four task-level summary hypotheses", content_anchor: "| **H1：是否及何时首次发生脓毒症** |"}
    revised_locator: {section_heading: "## Research design and methods", subsection_heading: "### Four task-level summary hypotheses", content_anchor: "| **H1：是否及何时首次发生脓毒症** |"}
    semantic_status: preserved
    evidence: >-
      每 6 小时起点、风险集、6/12/24 小时四类结局、多类别 Brier 损失、删失、患者内等权、两个比较模型及 Delta_1 通过规则均未变化。
  - protected_id: PCR-014
    prior_locator: {section_heading: "## Research design and methods", subsection_heading: "### Four task-level summary hypotheses", content_anchor: "| **H2：何时转向死亡或持续恢复** |"}
    revised_locator: {section_heading: "## Research design and methods", subsection_heading: "### Four task-level summary hypotheses", content_anchor: "| **H2：何时转向死亡或持续恢复** |"}
    semantic_status: preserved
    evidence: >-
      索引后 6/12/24/48/72 小时起点、晚于起点的 24/48/72/168 小时绝对时域、四类结局、患者内汇总、两个比较模型及 Delta_2 判定均未变化。
  - protected_id: PCR-015
    prior_locator: {section_heading: "## Research design and methods", subsection_heading: "### Four task-level summary hypotheses", content_anchor: "| **H3：从部分已观测历史预测被有意遮蔽的实测临床变量** |"}
    revised_locator: {section_heading: "## Research design and methods", subsection_heading: "### Four task-level summary hypotheses", content_anchor: "| **H3：从部分已观测历史预测被有意遮蔽的实测临床变量** |"}
    semantic_status: preserved
    evidence: >-
      六个器官功能域、三类器官支持、12 小时连续块遮蔽、仅用先前和未遮蔽观测、实测目标、负对数评分、九域等权、逆观测概率权重、两个比较模型及潜在状态非真值边界逐字未变。
  - protected_id: PCR-016
    prior_locator: {section_heading: "## Research design and methods", subsection_heading: "### Four task-level summary hypotheses", content_anchor: "| **H4：预测后续演化过程及结果** |"}
    revised_locator: {section_heading: "## Research design and methods", subsection_heading: "### Four task-level summary hypotheses", content_anchor: "| **H4：预测后续演化过程及结果** |"}
    semantic_status: preserved
    evidence: >-
      每 6 小时起点、存活且在 ICU 的风险集、24/48/72/168 小时可观测状态向量、吸收编码、域与时域等权、两个比较模型及 Delta_4 判定均未变化。
  - protected_id: PCR-017
    prior_locator: {section_heading: "## Research design and methods", subsection_heading: "### Four task-level summary hypotheses", content_anchor: "所有基础权重均在开发阶段冻结"}
    revised_locator: {section_heading: "## Research design and methods", subsection_heading: "### Four task-level summary hypotheses", content_anchor: "所有基础权重均在开发阶段冻结"}
    semantic_status: preserved
    evidence: >-
      基础权重与患者内再归一、权重模型冻结内容、外部信息截断、外部潜在状态与结局排除、患者级聚类重采样、事件与删失区分以及主分析和敏感性分析边界均逐字保留。
  - protected_id: PCR-018
    prior_locator: {section_heading: "## Research design and methods", subsection_heading: "### Complexity selection and identifiability", content_anchor: "若最高复杂度未通过"}
    revised_locator: {section_heading: "## Research design and methods", subsection_heading: "### Complexity selection and identifiability", content_anchor: "若最高复杂度未通过"}
    semantic_status: preserved
    evidence: >-
      开发模拟与内部时间诊断、阈值冻结时点、依次减少状态数/合并转移/简化停留时间/移除交互并逐步重跑，以及最小统一模型失败即停止全病程潜在状态主张，均保持不变。
  - protected_id: PCR-019
    prior_locator: {section_heading: "## Research design and methods", subsection_heading: "### External application and state-transfer diagnostics", content_anchor: "开发完成后，状态数、全部参数、状态标签"}
    revised_locator: {section_heading: "## Research design and methods", subsection_heading: "### External application and cross-database state-representation diagnostics", content_anchor: "开发完成后，状态数、全部参数、状态标签"}
    semantic_status: preserved
    evidence: >-
      冻结对象、外部直接应用和禁止重估或重命名均未变；六个器官功能域、同期生命体征、当前器官支持和短时变化方向仍是唯一状态比较特征，占用、距离、可分离、未迁移、合并、拆分、禁止强制一一匹配和禁用验证结局修改规则均完整保留。
  - protected_id: PCR-020
    prior_locator: {section_heading: "## Research design and methods", subsection_heading: "### External application and state-transfer diagnostics", content_anchor: "“必需状态”在开发阶段定义为"}
    revised_locator: {section_heading: "## Research design and methods", subsection_heading: "### External application and cross-database state-representation diagnostics", content_anchor: "“必需状态”在开发阶段定义为"}
    semantic_status: preserved
    evidence: >-
      必需状态仍须服务至少一个任务并满足最小占用和有效转移；未迁移或同阶段合并/拆分仍否定完整状态表示，受影响任务仍按可执行性失败，其他可观测预测任务最多获得部分支持。
  - protected_id: PCR-021
    prior_locator: {section_heading: "## Research design and methods", subsection_heading: "### Multiplicity and overall interpretation", content_anchor: "实施前条件满足后，四项任务同时估计"}
    revised_locator: {section_heading: "## Research design and methods", subsection_heading: "### Multiplicity and overall interpretation", content_anchor: "实施前条件满足后，四项任务同时估计"}
    semantic_status: preserved
    evidence: >-
      四任务平行、10,000 次患者级 max-t、最大单侧 p 值、最不利同时单侧 95% 上界、Holm 阈值与停止顺序、总体/部分/失败定义，以及有限校准和第三库不得替代无调整判定均保留。
  - protected_id: PCR-022
    prior_locator: {section_heading: "## Research content and work packages", content_anchor: "| 1. 实施前资格与约束验收 | 月 1–2 |"}
    revised_locator: {section_heading: "## Research content and work packages", content_anchor: "| 1. 实施前资格与约束验收 | 月 1–2 |"}
    semantic_status: preserved
    evidence: >-
      月 1–2、3–6、7–12、13–18 的资格、开发、外部验证、敏感性、复现与论文顺序和交付不变；月 7–12 仅将既有外部状态程序换成定义后的明确名称，后续试验和动物研究仍不在核心时间表内。
  - protected_id: PCR-023
    prior_locator: {section_heading: "## Research design and methods", subsection_heading: "### Conditional randomized-trial and animal follow-up", content_anchor: "只有 12–18 个月核心实证研究达到总体支持"}
    revised_locator: {section_heading: "## Research design and methods", subsection_heading: "### Conditional randomized-trial and animal follow-up", content_anchor: "只有 12–18 个月核心实证研究达到总体支持"}
    semantic_status: preserved
    evidence: >-
      总体支持、模型和代码冻结、EXIT-SEP 权限与逐时变量、交互功效及既有表型重叠核验仍是试验分析前提；随机分配、中介网络、XBJ-SCAP 适用边界及不得改写核心失败均未变化。
  - protected_id: PCR-024
    prior_locator: {section_heading: "## Research design and methods", subsection_heading: "### Conditional randomized-trial and animal follow-up", content_anchor: "只有合格随机试验分析与人类观察结果共同提出"}
    revised_locator: {section_heading: "## Research design and methods", subsection_heading: "### Conditional randomized-trial and animal follow-up", content_anchor: "只有合格随机试验分析与人类观察结果共同提出"}
    semantic_status: preserved
    evidence: >-
      动物研究仍须由合格试验与人类观察共同提出具体、可干预且可测机制，并具备平台、伦理和样本量依据；MQTiPSS、ARRIVE 2.0 及其不能验证或补救核心临床模型的边界均未变化。
  - protected_id: PCR-053
    prior_locator: {section_heading: "## Research design and methods", subsection_heading: "### Conditional randomized-trial and animal follow-up", content_anchor: "随机试验与动物研究各自按其资格和后果启动"}
    revised_locator: {section_heading: "## Research design and methods", subsection_heading: "### Conditional randomized-trial and animal follow-up", content_anchor: "随机试验与动物研究各自按其资格和后果启动"}
    semantic_status: preserved
    evidence: >-
      随机试验与动物研究继续按各自资格独立启动，一项不可行不取消另一项满足自身资格后的可能性；两者均不得替代两库核心研究或补救其失败。
  - protected_id: PCR-054
    prior_locator: {section_heading: "## Feasibility, resources, risks, alternatives, and stop conditions", subsection_heading: "### Working assumptions", content_anchor: "**任务三的固定操作化说明。**"}
    revised_locator: {section_heading: "## Feasibility, resources, risks, alternatives, and stop conditions", subsection_heading: "### Working assumptions", content_anchor: "**任务三的固定操作化说明。**"}
    semantic_status: preserved
    evidence: >-
      任务三仍固定为从部分已观测历史预测按规则遮蔽但实际测得的临床变量，只支持测量补全而不支持潜在状态恢复；目标变量、遮蔽块、观测权重稳定性和外部可执行性仍须资格审计实证通过。
  - protected_id: PCR-058
    prior_locator: {section_heading: "## Required analyses and evidence", subsection_heading: "### During development", content_anchor: "审计患者级时间泄漏、同一患者跨切分"}
    revised_locator: {section_heading: "## Required analyses and evidence", subsection_heading: "### During development", content_anchor: "审计患者级时间泄漏、同一患者跨切分"}
    semantic_status: preserved
    evidence: >-
      患者级时间泄漏、同一患者跨切分、未来信息建标签、比较模型处理不一致和外部数据参与选择的审计逐字保留；证伪标准仍排除由测量强度、标签实现、泄漏或不一致权重产生的表面增益。
  - protected_id: PCR-025
    prior_locator: {section_heading: "## Data, materials, and existing evidence base", subsection_heading: "### Existing evidence base", content_anchor: "临床定义、公开数据库存在性"}
    revised_locator: {section_heading: "## Data, materials, and existing evidence base", subsection_heading: "### Existing evidence base", content_anchor: "临床定义、公开数据库存在性"}
    semantic_status: preserved
    evidence: >-
      代表性来源类别、标签实现的一项针对性证据及 EXIT-SEP、XBJ-SCAP 和表型事后分析的直接来源均未变化；参考文献与证据仅作设计依据，未被改写为研究结果或首创证据。
  - protected_id: PCR-026
    prior_locator: {section_heading: "## Structured abstract", content_anchor: "- **Expected result:**"}
    revised_locator: {section_heading: "## Structured abstract", content_anchor: "- **Expected result:**"}
    semantic_status: preserved
    evidence: >-
      状态与转移模型、四任务比较、外部状态诊断、观测过程诊断及总体/部分/失败仍全部是预期产物；计划贡献仍限于可证伪预测性表示，不新增完成结果、因果网络或部署主张。
  - protected_id: PCR-027
    prior_locator: {section_heading: "## Contribution, innovation, impact, application, and closest-work comparison", subsection_heading: "### Bounded contribution frame", content_anchor: "本研究的计划贡献有三项"}
    revised_locator: {section_heading: "## Contribution, innovation, impact, application, and closest-work comparison", subsection_heading: "### Bounded contribution frame", content_anchor: "本研究的计划贡献有三项"}
    semantic_status: preserved
    evidence: >-
      由信息结构决定复杂度、用一个模型形成四项患者级确认性假设并控制家族错误率、冻结模型外部应用且观测过程单列三项贡献均保留，贡献性质仍仅为方法整合、外部验证和失效边界证据。
  - protected_id: PCR-028
    prior_locator: {section_heading: "## Expected outputs, falsification criteria, and interpretations", subsection_heading: "### Result-dependent interpretations", content_anchor: "| 结果模式 | 允许解释 |"}
    revised_locator: {section_heading: "## Expected outputs, falsification criteria, and interpretations", subsection_heading: "### Result-dependent interpretations", content_anchor: "| 结果模式 | 允许解释 |"}
    semantic_status: preserved
    evidence: >-
      全通过、部分通过、非必需状态未全满足、仅 H3 通过、外部任务或状态诊断失败及有限校准/第三库更优的允许解释均保持原范围；只用明确的冻结规则表述替代“迁移”，未增强任何结论。
  - protected_id: PCR-029
    prior_locator: {section_heading: "## Feasibility, resources, risks, alternatives, and stop conditions", subsection_heading: "### Working assumptions", content_anchor: "| WA-01 |"}
    revised_locator: {section_heading: "## Feasibility, resources, risks, alternatives, and stop conditions", subsection_heading: "### Working assumptions", content_anchor: "| WA-01 |"}
    semantic_status: preserved
    evidence: >-
      最终论文组织尚未确认、核心实证研究暂按可独立成文推进、月 3 确认，以及不成立时只调整成果组织、作者分工和后续整合的假设与后果逐字未变。
  - protected_id: PCR-030
    prior_locator: {section_heading: "## Feasibility, resources, risks, alternatives, and stop conditions", subsection_heading: "### Working assumptions", content_anchor: "| WA-02 |"}
    revised_locator: {section_heading: "## Feasibility, resources, risks, alternatives, and stop conditions", subsection_heading: "### Working assumptions", content_anchor: "| WA-02 |"}
    semantic_status: preserved
    evidence: >-
      第三库仅在两库核心结果锁定且资源允许时加入、不进入 Holm 家族或总体判定、月 12 后确认及资格或资源不足即取消，均逐字未变。
  - protected_id: PCR-031
    prior_locator: {section_heading: "## Feasibility, resources, risks, alternatives, and stop conditions", subsection_heading: "### Limitations and boundary conditions", content_anchor: "1. 当前证据来自有界检索"}
    revised_locator: {section_heading: "## Feasibility, resources, risks, alternatives, and stop conditions", subsection_heading: "### Limitations and boundary conditions", content_anchor: "1. 当前证据来自有界检索"}
    semantic_status: preserved
    evidence: >-
      有界而非穷尽性检索、“首个”“完整系统”“无人研究”及相关首次性主张不受支持、2026 年来源需复核的限制逐字未变。
  - protected_id: PCR-032
    prior_locator: {section_heading: "## Feasibility, resources, risks, alternatives, and stop conditions", subsection_heading: "### Limitations and boundary conditions", content_anchor: "2. 尚未取得候选数据库"}
    revised_locator: {section_heading: "## Feasibility, resources, risks, alternatives, and stop conditions", subsection_heading: "### Limitations and boundary conditions", content_anchor: "2. 尚未取得候选数据库"}
    semantic_status: preserved
    evidence: >-
      候选数据库项目访问、真实样例和完整变量字典尚未取得，且数据库存在不等于项目具备许可、共同变量和足够信息量的限制逐字未变。
  - protected_id: PCR-033
    prior_locator: {section_heading: "## Feasibility, resources, risks, alternatives, and stop conditions", subsection_heading: "### Limitations and boundary conditions", content_anchor: "3. 数据库之间的人群、实践、变量语义、采样和结局定义不同"}
    revised_locator: {section_heading: "## Feasibility, resources, risks, alternatives, and stop conditions", subsection_heading: "### Limitations and boundary conditions", content_anchor: "3. 数据库之间的人群、实践、变量语义、采样和结局定义不同"}
    semantic_status: preserved
    evidence: >-
      跨库人群、实践、变量语义、采样和结局定义差异，以及外部差异可能混合病例组合、标签和观测过程的限制逐字未变。
  - protected_id: PCR-034
    prior_locator: {section_heading: "## Feasibility, resources, risks, alternatives, and stop conditions", subsection_heading: "### Limitations and boundary conditions", content_anchor: "4. 感染风险入口、脓毒症标签、首次索引时点"}
    revised_locator: {section_heading: "## Feasibility, resources, risks, alternatives, and stop conditions", subsection_heading: "### Limitations and boundary conditions", content_anchor: "4. 感染风险入口、脓毒症标签、首次索引时点"}
    semantic_status: preserved
    evidence: >-
      感染风险入口、脓毒症标签、首次索引时点、任务时域和持续恢复定义会影响结果，须以冻结代码和预定敏感性分析界定的限制逐字未变。
  - protected_id: PCR-035
    prior_locator: {section_heading: "## Feasibility, resources, risks, alternatives, and stop conditions", subsection_heading: "### Limitations and boundary conditions", content_anchor: "5. 观察性电子病历中的治疗和测量"}
    revised_locator: {section_heading: "## Feasibility, resources, risks, alternatives, and stop conditions", subsection_heading: "### Limitations and boundary conditions", content_anchor: "5. 观察性电子病历中的治疗和测量"}
    semantic_status: preserved
    evidence: >-
      治疗和测量受病情与既往处置影响，模型边、权重和治疗系数仅是预测性条件时间关联，不能识别因果调控、最优治疗、治疗作用、反事实个体效应或中介网络；该边界逐字未变。
  - protected_id: PCR-036
    prior_locator: {section_heading: "## Feasibility, resources, risks, alternatives, and stop conditions", subsection_heading: "### Limitations and boundary conditions", content_anchor: "6. 临床锚定迁移只评价表示的跨库可重复性"}
    revised_locator: {section_heading: "## Feasibility, resources, risks, alternatives, and stop conditions", subsection_heading: "### Limitations and boundary conditions", content_anchor: "6. 跨数据库状态表示诊断只评价开发状态在外部数据库中的占用和可分离性"}
    semantic_status: preserved
    evidence: >-
      外部诊断仍仅评价开发状态在预定临床特征上的跨库占用和可分离性，开发期恢复诊断仍只评价设定模型下的可辨识性，观测重建仍只评价观测过程，三者均不能证明真实生物状态；任务三的实测变量边界亦未改变。
  - protected_id: PCR-037
    prior_locator: {section_heading: "## Feasibility, resources, risks, alternatives, and stop conditions", subsection_heading: "### Limitations and boundary conditions", content_anchor: "7. 外部验证只适用于"}
    revised_locator: {section_heading: "## Feasibility, resources, risks, alternatives, and stop conditions", subsection_heading: "### Limitations and boundary conditions", content_anchor: "7. 外部验证只适用于"}
    semantic_status: preserved
    evidence: >-
      外部验证适用范围仍限于研究人群、共同变量、风险集、时域和医疗环境；预测改善仍不等于临床效用、真实世界效果、可部署性、治疗建议、机制或监管用途。
  - protected_id: PCR-038
    prior_locator: {section_heading: "## Feasibility, resources, risks, alternatives, and stop conditions", subsection_heading: "### Limitations and boundary conditions", content_anchor: "8. 目标值被观测的概率"}
    revised_locator: {section_heading: "## Feasibility, resources, risks, alternatives, and stop conditions", subsection_heading: "### Limitations and boundary conditions", content_anchor: "8. 目标值被观测的概率"}
    semantic_status: preserved
    evidence: >-
      观测概率、逆观测概率权重和逆删失概率权重依赖冻结模型与可观测历史，极端权重、未测量驱动因素和跨库观测政策差异可造成残余偏倚；该限制逐字未变。
  - protected_id: PCR-039
    prior_locator: {section_heading: "## Feasibility, resources, risks, alternatives, and stop conditions", subsection_heading: "### Limitations and boundary conditions", content_anchor: "9. EXIT-SEP 与 XBJ-SCAP"}
    revised_locator: {section_heading: "## Feasibility, resources, risks, alternatives, and stop conditions", subsection_heading: "### Limitations and boundary conditions", content_anchor: "9. EXIT-SEP 与 XBJ-SCAP"}
    semantic_status: preserved
    evidence: >-
      两项试验的数据权限、逐时变量和功效仍未核实，EXIT-SEP 既有表型分析仍构成重叠风险，随机分配仍不自动识别中介网络；该限制逐字未变。
  - protected_id: PCR-040
    prior_locator: {section_heading: "## Feasibility, resources, risks, alternatives, and stop conditions", subsection_heading: "### Limitations and boundary conditions", content_anchor: "10. 动物研究缺少"}
    revised_locator: {section_heading: "## Feasibility, resources, risks, alternatives, and stop conditions", subsection_heading: "### Limitations and boundary conditions", content_anchor: "10. 动物研究缺少"}
    semantic_status: preserved
    evidence: >-
      动物研究仍缺具体机制、平台、样本量、伦理和预算，人鼠可转化证据仍有冲突，动物结果仍不能作为临床模型外部验证；该限制逐字未变。
  - protected_id: PCR-041
    prior_locator: {section_heading: "## Feasibility, resources, risks, alternatives, and stop conditions", subsection_heading: "### Limitations and boundary conditions", content_anchor: "11. 建模前文献—专家约束表"}
    revised_locator: {section_heading: "## Feasibility, resources, risks, alternatives, and stop conditions", subsection_heading: "### Limitations and boundary conditions", content_anchor: "11. 建模前文献—专家约束表"}
    semantic_status: preserved
    evidence: >-
      文献—专家约束表、核心团队和计算承诺尚未完成，12–18 个月只约束核心研究且条件性后续无既定时间与资源承诺；该可行性边界逐字未变。
  - protected_id: PCR-042
    prior_locator: {section_heading: "## Feasibility, resources, risks, alternatives, and stop conditions", subsection_heading: "### Risks, alternatives, and stop conditions", content_anchor: "| 月 2 末不能形成一个开发库和一个异质外部库的合格组合 |"}
    revised_locator: {section_heading: "## Feasibility, resources, risks, alternatives, and stop conditions", subsection_heading: "### Risks, alternatives, and stop conditions", content_anchor: "| 月 2 末不能形成一个开发库和一个异质外部库的合格组合 |"}
    semantic_status: preserved
    evidence: >-
      月 2 末不能形成合格两库组合时仍只能按预登记顺序核验替代库且不查看模型表现，替代后仍失败则停止跨库主分析且不进入潜在状态模型；规则逐字未变。
  - protected_id: PCR-043
    prior_locator: {section_heading: "## Feasibility, resources, risks, alternatives, and stop conditions", subsection_heading: "### Risks, alternatives, and stop conditions", content_anchor: "| 约束表缺少核心字段、最低专家构成、共识或异议记录 |"}
    revised_locator: {section_heading: "## Feasibility, resources, risks, alternatives, and stop conditions", subsection_heading: "### Risks, alternatives, and stop conditions", content_anchor: "| 约束表缺少核心字段、最低专家构成、共识或异议记录 |"}
    semantic_status: preserved
    evidence: >-
      约束表缺项时须补齐专家轮次和逐项记录、不得由数据团队代填，月 2 末仍不合格则不开始主模型拟合；规则逐字未变。
  - protected_id: PCR-044
    prior_locator: {section_heading: "## Feasibility, resources, risks, alternatives, and stop conditions", subsection_heading: "### Risks, alternatives, and stop conditions", content_anchor: "| 核心团队角色未书面落实或计算基准不足 |"}
    revised_locator: {section_heading: "## Feasibility, resources, risks, alternatives, and stop conditions", subsection_heading: "### Risks, alternatives, and stop conditions", content_anchor: "| 核心团队角色未书面落实或计算基准不足 |"}
    semantic_status: preserved
    evidence: >-
      团队或计算不足时仍先取消第三库、额外亚组和非必需消融并重新基准；五个核心角色或两库核心计算仍不能完成时仍停止复杂模型路线。
  - protected_id: PCR-045
    prior_locator: {section_heading: "## Feasibility, resources, risks, alternatives, and stop conditions", subsection_heading: "### Risks, alternatives, and stop conditions", content_anchor: "| 模拟或内部时间验证显示最小统一模型不可恢复 |"}
    revised_locator: {section_heading: "## Feasibility, resources, risks, alternatives, and stop conditions", subsection_heading: "### Risks, alternatives, and stop conditions", content_anchor: "| 模拟或内部时间验证显示最小统一模型不可恢复 |"}
    semantic_status: preserved
    evidence: >-
      最小统一模型不可恢复时仍按状态数、转移、停留时间和交互的顺序简化并重跑；最小模型仍不能覆盖全病程则停止统一潜在状态主张，规则逐字未变。
  - protected_id: PCR-046
    prior_locator: {section_heading: "## Feasibility, resources, risks, alternatives, and stop conditions", subsection_heading: "### Risks, alternatives, and stop conditions", content_anchor: "| 外部必需状态未迁移、合并或拆分 |"}
    revised_locator: {section_heading: "## Feasibility, resources, risks, alternatives, and stop conditions", subsection_heading: "### Risks, alternatives, and stop conditions", content_anchor: "| 外部必需状态未迁移、合并或拆分 |"}
    semantic_status: preserved
    evidence: >-
      外部必需状态未迁移、合并或拆分时仍保留开发标签、报告受影响状态并禁止结局重定义或强制匹配；完整表示失败、受影响任务失败及其他任务最多部分支持的后果逐字未变。
  - protected_id: PCR-047
    prior_locator: {section_heading: "## Feasibility, resources, risks, alternatives, and stop conditions", subsection_heading: "### Risks, alternatives, and stop conditions", content_anchor: "| 一个或多个任务未通过 Holm 调整 |"}
    revised_locator: {section_heading: "## Feasibility, resources, risks, alternatives, and stop conditions", subsection_heading: "### Risks, alternatives, and stop conditions", content_anchor: "| 一个或多个任务未通过 Holm 调整 |"}
    semantic_status: preserved
    evidence: >-
      未通过 Holm 的任务仍报告估计量和区间且不影响其他任务检验；未通过任务仍明确不受支持，且不能被其他任务、有限校准、第三库、随机试验或动物研究补救。
  - protected_id: PCR-048
    prior_locator: {section_heading: "## Feasibility, resources, risks, alternatives, and stop conditions", subsection_heading: "### Risks, alternatives, and stop conditions", content_anchor: "| 数据抽取、任务摘要、Holm 结论或迁移诊断不能由独立分析者复现 |"}
    revised_locator: {section_heading: "## Feasibility, resources, risks, alternatives, and stop conditions", subsection_heading: "### Risks, alternatives, and stop conditions", content_anchor: "| 数据抽取、任务摘要、Holm 结论或跨数据库状态表示诊断不能由独立分析者复现 |"}
    semantic_status: preserved
    evidence: >-
      独立复现失败仍触发暂停解释并核对字段血缘、患者聚类、权重和代码；核心结果仍不能复现则不得提交全病程状态或外部验证主张，仅诊断名称被明确化。
  - protected_id: PCR-049
    prior_locator: {section_heading: "## Feasibility, resources, risks, alternatives, and stop conditions", subsection_heading: "### Limitations and boundary conditions", content_anchor: "不能支持“首个”“完整”"}
    revised_locator: {section_heading: "## Feasibility, resources, risks, alternatives, and stop conditions", subsection_heading: "### Limitations and boundary conditions", content_anchor: "不能支持“首个”“完整”"}
    semantic_status: preserved
    evidence: >-
      “首个”“完整系统”“无人研究”、首次建立完整人体系统和首次使用动态状态方法仍被明确列为不受支持的主张类别，措辞与强度未变。
  - protected_id: PCR-050
    prior_locator: {section_heading: "## Feasibility, resources, risks, alternatives, and stop conditions", subsection_heading: "### Limitations and boundary conditions", content_anchor: "模型中的边、权重和治疗系数只能解释为预测性条件时间关联"}
    revised_locator: {section_heading: "## Feasibility, resources, risks, alternatives, and stop conditions", subsection_heading: "### Limitations and boundary conditions", content_anchor: "模型中的边、权重和治疗系数只能解释为预测性条件时间关联"}
    semantic_status: preserved
    evidence: >-
      模型边、权重和治疗系数仍只支持预测性条件时间关联，不支持因果调控、最优治疗、治疗作用、反事实个体效应或中介网络；排除范围逐字未变。
  - protected_id: PCR-051
    prior_locator: {section_heading: "## Feasibility, resources, risks, alternatives, and stop conditions", subsection_heading: "### Limitations and boundary conditions", content_anchor: "预测改善不等于临床效用"}
    revised_locator: {section_heading: "## Feasibility, resources, risks, alternatives, and stop conditions", subsection_heading: "### Limitations and boundary conditions", content_anchor: "预测改善不等于临床效用"}
    semantic_status: preserved
    evidence: >-
      外部状态诊断、开发期潜在状态恢复和观测重建仍不能证明真实生物状态；预测改善仍不支持临床效用、真实世界效果、部署、治疗建议、机制或监管用途，任务三也仍不验证潜在状态。
  - protected_id: PCR-052
    prior_locator: {section_heading: "## Research design and methods", subsection_heading: "### Conditional randomized-trial and animal follow-up", content_anchor: "任何 RCT 结果都不能把核心实证研究未通过的任务改写为通过"}
    revised_locator: {section_heading: "## Research design and methods", subsection_heading: "### Conditional randomized-trial and animal follow-up", content_anchor: "任何 RCT 结果都不能把核心实证研究未通过的任务改写为通过"}
    semantic_status: preserved
    evidence: >-
      随机试验或动物研究仍不能改写核心未通过任务；随机分配仍不自动识别中介网络，动物结果仍不构成临床模型外部验证且不能补救核心研究失败。
undeclared_scientific_changes: []
findings: []
unresolved_issues: []
---

# Content-preservation check

## Decision rationale

结论为 `scientific_content_preserved`。冻结登记表中的五项研究身份字段在 v005、v006 与登记表之间逐字相同；58 项保护内容均在 v006 中有可解析的权威定位，且研究对象、数据来源、模型结构、任务定义、时点与时域、结果编码、权重、比较模型、推断与多重性规则、停止条件、可行性边界、证据状态和不受支持的主张类别均未改变。

修订记录仅声明两项编辑性改动：题名改为明确区分一个开发数据库与一个异质外部验证数据库；把原先容易与患者病程内状态转移混淆的外部状态比较统一定义为“跨数据库状态表示诊断”。逐处比较表明，后一术语仍使用原有四类预定临床特征，仍按冻结的占用、分布距离和可分离规则判断未迁移、合并与拆分，且仍与观测过程诊断分开。因此该变化没有新增数据、方法、结果或证据，没有改变主张强度，也没有把计划工作表述为已完成工作。

## Identity-anchor verification

| 身份字段 | v005 与 v006 | 与冻结登记表 | 结论 |
|---|---|---|---|
| `primary_research_question` | 逐字相同 | 逐字相同 | 保留 |
| `primary_objective` | 逐字相同 | 逐字相同 | 保留 |
| `study_object` | 逐字相同 | 逐字相同 | 保留 |
| `core_data_or_evidence_base` | 逐字相同 | 逐字相同 | 保留 |
| `primary_unit_of_inference` | 逐字相同 | 逐字相同 | 保留 |

## Protected-content trace

唯一涉及保护内容表述移动或替换的部分是外部状态比较程序。v006 在 `Title, summary, audience, and positioning` 首次定义“预定临床特征”和“跨数据库状态表示诊断”，并在 `Research design and methods` 的 `External application and cross-database state-representation diagnostics` 小节保留完整权威规则。原有六个器官功能域、同期生命体征、当前器官支持、短时变化方向、冻结占用和距离规则、可分离性、未迁移/合并/拆分后果、禁止外部重估与重命名、禁止结局驱动修改和观测过程分离均完整保留。其余保护项位于原有章节和条目，未发生科学内容改变。

## Required routing

v006 可进入全新的叙事与学术语言评估；无需返回科学审查。
