---
schema_version: research-idea-content-preservation-check.v1
check_id: content-preservation-I01-001-r002
review_id: content-preservation-r002
reviewer_skill: idea-narrative-assessor
reviewer_instance_id: new_preservation_r002
workflow_id: sepsis-complex-system-idea-generation-v001
round_id: editorial-repair-round-003
input_artifact_ids:
  - idea-dossier-I01-001-v003
  - idea-dossier-I01-001-v004
  - protected-content-register-v001
  - revision-delta-I01-001-v003-to-v004
input_versions:
  - v003
  - v004
  - v001
  - v003-to-v004
inputs:
  prior_dossier:
    artifact_id: idea-dossier-I01-001-v003
    version: v003
    path: tests/脓毒症复杂系统模型/03_ideas/nodes/I01-001/dossiers/idea-dossier-v003.md
  revised_dossier:
    artifact_id: idea-dossier-I01-001-v004
    version: v004
    path: tests/脓毒症复杂系统模型/03_ideas/nodes/I01-001/dossiers/idea-dossier-v004.md
  protected_content_register:
    artifact_id: protected-content-register-v001
    version: v001
    path: tests/脓毒症复杂系统模型/05_state/protected-content-register-v001.yaml
  revision_delta:
    artifact_id: revision-delta-I01-001-v003-to-v004
    version: v003-to-v004
    path: tests/脓毒症复杂系统模型/03_ideas/nodes/I01-001/revisions/round-003/revision-delta-v003-to-v004.md
files_read:
  - tests/脓毒症复杂系统模型/03_ideas/nodes/I01-001/dossiers/idea-dossier-v003.md
  - tests/脓毒症复杂系统模型/03_ideas/nodes/I01-001/dossiers/idea-dossier-v004.md
  - tests/脓毒症复杂系统模型/05_state/protected-content-register-v001.yaml
  - tests/脓毒症复杂系统模型/03_ideas/nodes/I01-001/revisions/round-003/revision-delta-v003-to-v004.md
isolation_mode: fresh_subagent
prior_scores_visible: false
source_edits_performed: false
decision: scientific_content_preserved
protected_item_checks:
  - protected_id: PCR-001
    prior_locator: 'Research question, objectives, and core hypothesis > Primary research question'
    revised_locator: 'Research question, objectives, and core hypothesis > Primary research question; frontmatter identity_anchor.primary_research_question'
    semantic_status: preserved
    evidence: '人群、预先约束、三个过程、统一全病程模型、开发与异质外部库、四项任务和临床锚定迁移均保留；任务三仅把读者用语明确为临床测量值预测。'
  - protected_id: PCR-002
    prior_locator: 'Research question, objectives, and core hypothesis > Objectives 1–4'
    revised_locator: 'Research question, objectives, and core hypothesis > Objectives 1–4'
    semantic_status: preserved
    evidence: '约束与资源资格、开发期复杂度诊断和冻结、外部四任务与状态迁移、任务级支持和失效边界四项目标逐项保留。'
  - protected_id: PCR-003
    prior_locator: 'Title, summary, audience, and positioning > definitions paragraphs'
    revised_locator: 'Title, summary, audience, and positioning > definitions paragraphs; Research design and methods > Unified full-course population, time axis, and state space'
    semantic_status: preserved
    evidence: '成人 ICU 全病程对象、同一状态空间和预测接口、三个过程的区分、文献—专家约束及冻结后外部直接应用的范围未变。'
  - protected_id: PCR-004
    prior_locator: 'Research design and methods > Unified full-course population, time axis, and state space'
    revised_locator: 'Research design and methods > Unified full-course population, time axis, and state space'
    semantic_status: preserved
    evidence: '风险入口至出 ICU、死亡或删失的起止边界，未发病与已发病患者贡献，重复住院分割及五类状态组成均完整保留。'
  - protected_id: PCR-005
    prior_locator: 'Title, summary, audience, and positioning > scope paragraph'
    revised_locator: 'Title, summary, audience, and positioning > scope paragraph; Research design and methods > Conditional randomized-trial and animal follow-up; Risks, alternatives, and stop conditions'
    semantic_status: preserved
    evidence: '12–18 个月核心仍是两库建模与验证；随机试验和动物研究仍为时间表外条件性后续，且不能改写核心任务失败。'
  - protected_id: PCR-006
    prior_locator: 'Data, materials, and existing evidence base > First-stage constraint-table prerequisite'
    revised_locator: 'Data, materials, and existing evidence base > Pre-model constraint-table prerequisite'
    semantic_status: preserved
    evidence: '约束表覆盖范围、五类专家构成、利益冲突与缺席记录、独立判断和匿名反馈、80% 双专业支持规则及异议保存均保留。'
  - protected_id: PCR-007
    prior_locator: 'Data, materials, and existing evidence base > Required inputs and database constitution'
    revised_locator: 'Data, materials, and existing evidence base > Required inputs and database constitution'
    semantic_status: preserved
    evidence: '一个公开开发库加一个异质公开外部库、尚未确认的访问与信息量、真实样例和概念映射、预登记选择及禁止按表现换库均保留。'
  - protected_id: PCR-008
    prior_locator: 'Data, materials, and existing evidence base > Database, team, and compute qualification'
    revised_locator: 'Data, materials, and existing evidence base > Database, team, and compute qualification; Feasibility and resources; Working assumptions'
    semantic_status: preserved
    evidence: '真实样例资格项目、有效转移定义、五个核心角色、计算实测以及失败后换库、削减非核心分析或停止的后果均在；这些条件仍明确不能用工作假设替代。'
  - protected_id: PCR-009
    prior_locator: 'Data, materials, and existing evidence base > Required inputs and database constitution'
    revised_locator: 'Data, materials, and existing evidence base > Required inputs and database constitution; Working assumptions WA-02; Conditional randomized-trial and animal follow-up'
    semantic_status: preserved
    evidence: '第三库仍仅为两库结果锁定后的可选压力测试且不进入 Holm 或总体判定；两项试验数据仍未核实且仅属条件性后续。'
  - protected_id: PCR-010
    prior_locator: 'Research design and methods > Unified full-course population, time axis, and state space'
    revised_locator: 'Research design and methods > Unified full-course population, time axis, and state space'
    semantic_status: preserved
    evidence: '持续恢复的存活、三类支持脱离、六器官域连续 24 小时标准，随后可恶化或出 ICU，出 ICU 独立编码及真实时间和 6 小时评分网格均未改变。'
  - protected_id: PCR-011
    prior_locator: 'Research design and methods > Primary model and task-specific comparators'
    revised_locator: 'Research design and methods > Primary model and task-specific comparators'
    semantic_status: preserved
    evidence: '隐半马尔可夫模型、潜在状态、停留时间、观测与观测过程、治疗输入的预测角色，以及四任务各两个比较模型和最不利损失差规则均保留。'
  - protected_id: PCR-012
    prior_locator: 'Research question, objectives, and core hypothesis > Confirmatory family'
    revised_locator: 'Research question, objectives, and core hypothesis > Confirmatory family'
    semantic_status: preserved
    evidence: '资格与可辨识性仍是进入四假设评价的实证条件；患者级汇总、D_kc、Delta_k、max-t、最大 p 值、Holm 0.05、置信区间及双重通过规则均一致。'
  - protected_id: PCR-013
    prior_locator: 'Research design and methods > Four task-level summary hypotheses > H1'
    revised_locator: 'Research design and methods > Four task-level summary hypotheses > H1'
    semantic_status: preserved
    evidence: '每 6 小时起始点、风险集、6/12/24 小时四类结局、Brier 损失、删失、患者内等权、两个比较模型及 Delta_1 判定均保留。'
  - protected_id: PCR-014
    prior_locator: 'Research design and methods > Four task-level summary hypotheses > H2'
    revised_locator: 'Research design and methods > Four task-level summary hypotheses > H2'
    semantic_status: preserved
    evidence: '五个索引后起始点、风险集、24/48/72/168 小时四类状态、绝对时域、患者内汇总、两个比较模型与 Delta_2 规则均保留。'
  - protected_id: PCR-015
    prior_locator: 'Research design and methods > Four task-level summary hypotheses > H3'
    revised_locator: 'Research design and methods > Four task-level summary hypotheses > H3'
    semantic_status: preserved
    evidence: '六器官域和三类支持、12 小时连续块遮蔽、只用既往与未遮蔽输入、真实测得目标、负对数评分、九域权重、两个比较模型、Delta_3 和校准诊断边界均保留；新标题准确描述同一测量目标。'
  - protected_id: PCR-016
    prior_locator: 'Research design and methods > Four task-level summary hypotheses > H4'
    revised_locator: 'Research design and methods > Four task-level summary hypotheses > H4'
    semantic_status: preserved
    evidence: '每 6 小时起始点、存活 ICU 风险集、四时域全病程可观测向量、吸收编码、域级 Brier 损失、汇总、两个比较模型和 Delta_4 均不变。'
  - protected_id: PCR-017
    prior_locator: 'Research design and methods > Four task-level summary hypotheses > weighting paragraphs'
    revised_locator: 'Research design and methods > Four task-level summary hypotheses > weighting paragraphs'
    semantic_status: preserved
    evidence: '基础权重、患者内归一化、开发期冻结、外部截止信息、逆删失与逆观测权重、禁止外部状态或结局进入权重模型、患者聚类及敏感性边界均保留。'
  - protected_id: PCR-018
    prior_locator: 'Research design and methods > Complexity selection and identifiability'
    revised_locator: 'Research design and methods > Complexity selection and identifiability'
    semantic_status: preserved
    evidence: '全病程模拟输入、恢复与稳定性诊断、外部评价前冻结、四步复杂度简化次序及最小模型失败后停止统一全病程主张均保留；恢复对象被明确为参数与潜在状态。'
  - protected_id: PCR-019
    prior_locator: 'Research design and methods > External application and state-transfer diagnostics'
    revised_locator: 'Research design and methods > External application and state-transfer diagnostics'
    semantic_status: preserved
    evidence: '全部开发对象冻结、外部不重估或重命名、临床锚定构成、占用与距离规则、未迁移/合并/拆分判定及观测过程单列均一致。'
  - protected_id: PCR-020
    prior_locator: 'Research design and methods > External application and state-transfer diagnostics > required-state paragraph'
    revised_locator: 'Research design and methods > External application and state-transfer diagnostics > required-state paragraph'
    semantic_status: preserved
    evidence: '必需状态的任务服务与占用/有效转移要求、迁移失败对完整表示的后果、可观测任务的有限支持及不可执行任务直接失败均保留。'
  - protected_id: PCR-021
    prior_locator: 'Research design and methods > Multiplicity and overall interpretation'
    revised_locator: 'Research design and methods > Multiplicity and overall interpretation'
    semantic_status: preserved
    evidence: '四任务并行、10,000 次 max-t、Holm 顺序及阈值、总体/部分/失败定义、有限校准允许范围和第三库敏感性地位均保留。'
  - protected_id: PCR-022
    prior_locator: 'Research content and work packages > four work-package rows'
    revised_locator: 'Research content and work packages > four work-package rows; Title, summary, audience, and positioning > scope paragraph'
    semantic_status: preserved
    evidence: '月 1–2、3–6、7–12、13–18 的活动与交付，月 12 核心结果、复现和论文、第三库单列及后续研究不入时表均一致。'
  - protected_id: PCR-023
    prior_locator: 'Research design and methods > Conditional randomized-trial and animal follow-up > randomized-trial paragraph'
    revised_locator: 'Research design and methods > Conditional randomized-trial and animal follow-up > randomized-trial paragraph'
    semantic_status: preserved
    evidence: '核心总体支持、模型代码冻结、EXIT-SEP 权限与逐时变量、交互功效和差异核验仍为共同前提；随机分配与中介边界、XBJ-SCAP 适配及不得改写核心失败均保留。'
  - protected_id: PCR-024
    prior_locator: 'Research design and methods > Conditional randomized-trial and animal follow-up > animal paragraph'
    revised_locator: 'Research design and methods > Conditional randomized-trial and animal follow-up > animal paragraph'
    semantic_status: preserved
    evidence: '合格试验分析与人类观察共同提出可干预可测机制、平台伦理样本量、MQTiPSS/ARRIVE 以及动物结果不作临床外部验证或补救核心失败均保留。'
  - protected_id: PCR-025
    prior_locator: 'Data, materials, and existing evidence base > Existing evidence base'
    revised_locator: 'Data, materials, and existing evidence base > Existing evidence base; Feasibility, resources, risks, alternatives, and stop conditions > Limitations and boundary conditions item 1'
    semantic_status: preserved
    evidence: '各证据类别及其代表性支持保持；非穷尽检索和不支持首个、完整或无人研究等结论集中到限制权威位置，未提高证据强度。'
  - protected_id: PCR-026
    prior_locator: 'Structured abstract > Expected result and Contribution and impact'
    revised_locator: 'Structured abstract > Expected result and Contribution and impact; Limitations and boundary conditions items 5–7'
    semantic_status: preserved
    evidence: '所有产物仍以预期或计划时态呈现；可证伪预测性表示贡献保留，真实生物状态、因果和部署边界集中保留在限制权威位置。'
  - protected_id: PCR-027
    prior_locator: 'Contribution, innovation, impact, application, and closest-work comparison > Bounded contribution frame'
    revised_locator: 'Contribution, innovation, impact, application, and closest-work comparison > Bounded contribution frame; Limitations and boundary conditions items 1, 5–7'
    semantic_status: preserved
    evidence: '三项计划贡献和方法整合、外部验证、失效边界性质未变；首创、生物实体、临床效用、因果及个体治疗禁限移至唯一限制权威位置。'
  - protected_id: PCR-028
    prior_locator: 'Expected outputs, falsification criteria, and interpretations > Result-dependent interpretations'
    revised_locator: 'Expected outputs, falsification criteria, and interpretations > Result-dependent interpretations; Limitations and boundary conditions items 5–7'
    semantic_status: preserved
    evidence: '六种结果模式的支持范围逐项保留；真实状态与因果边界仍在成功解释行，其他通用禁限在限制权威位置完整保留。'
  - protected_id: PCR-029
    prior_locator: 'Feasibility, resources, risks, alternatives, and stop conditions > Working assumptions > WA-01'
    revised_locator: 'Feasibility, resources, risks, alternatives, and stop conditions > Working assumptions > WA-01'
    semantic_status: preserved
    evidence: '论文组织的暂定假设、核心身份与四任务两库不变、月 3 验证点及不成立时只调整成果组织和分工均保留。'
  - protected_id: PCR-030
    prior_locator: 'Feasibility, resources, risks, alternatives, and stop conditions > Working assumptions > WA-02'
    revised_locator: 'Feasibility, resources, risks, alternatives, and stop conditions > Working assumptions > WA-02'
    semantic_status: preserved
    evidence: '第三库在两库结果锁定且资源允许时才加入、不进入 Holm/总体/月 12 交付，以及资格或资源不足即取消均保留。'
  - protected_id: PCR-031
    prior_locator: 'Feasibility, resources, risks, alternatives, and stop conditions > Limitations and boundary conditions item 1'
    revised_locator: 'Feasibility, resources, risks, alternatives, and stop conditions > Limitations and boundary conditions item 1'
    semantic_status: preserved
    evidence: '有界而非系统综述、首个/完整/无人研究禁限及 2026 年来源复核均保留，并明确涵盖完整人体系统和首次动态状态方法。'
  - protected_id: PCR-032
    prior_locator: 'Feasibility, resources, risks, alternatives, and stop conditions > Limitations and boundary conditions item 2'
    revised_locator: 'Feasibility, resources, risks, alternatives, and stop conditions > Limitations and boundary conditions item 2'
    semantic_status: preserved
    evidence: '项目访问、真实样例和完整字典尚未取得，以及数据库存在不等于许可、共同变量和信息量可用的限制逐字义保留。'
  - protected_id: PCR-033
    prior_locator: 'Feasibility, resources, risks, alternatives, and stop conditions > Limitations and boundary conditions item 3'
    revised_locator: 'Feasibility, resources, risks, alternatives, and stop conditions > Limitations and boundary conditions item 3'
    semantic_status: preserved
    evidence: '人群、实践、语义、采样和结局差异及其病例组合、标签和观测过程来源均保留。'
  - protected_id: PCR-034
    prior_locator: 'Feasibility, resources, risks, alternatives, and stop conditions > Limitations and boundary conditions item 4'
    revised_locator: 'Feasibility, resources, risks, alternatives, and stop conditions > Limitations and boundary conditions item 4'
    semantic_status: preserved
    evidence: '入口、标签、索引时点、任务时域和持续恢复定义的影响，以及冻结代码与预定敏感性处理均保留。'
  - protected_id: PCR-035
    prior_locator: 'Feasibility, resources, risks, alternatives, and stop conditions > Limitations and boundary conditions item 5'
    revised_locator: 'Feasibility, resources, risks, alternatives, and stop conditions > Limitations and boundary conditions item 5'
    semantic_status: preserved
    evidence: '观察性治疗与测量混杂和仅能解释为预测性条件时间关联均保留；因果调控、最优治疗、治疗作用、反事实个体效应及中介网络均明确排除。'
  - protected_id: PCR-036
    prior_locator: 'Feasibility, resources, risks, alternatives, and stop conditions > Limitations and boundary conditions item 6'
    revised_locator: 'Feasibility, resources, risks, alternatives, and stop conditions > Limitations and boundary conditions item 6'
    semantic_status: preserved
    evidence: '潜在状态无金标准，锚定、任务预测和观测重建分别只评价表示、用途和观测模型，均不能证明真实生物状态。'
  - protected_id: PCR-037
    prior_locator: 'Feasibility, resources, risks, alternatives, and stop conditions > Limitations and boundary conditions item 7'
    revised_locator: 'Feasibility, resources, risks, alternatives, and stop conditions > Limitations and boundary conditions item 7'
    semantic_status: preserved
    evidence: '适用人群、变量、风险集、时域和环境边界，以及不等同临床效用、真实世界效果或部署的限制保留，并增列治疗建议、机制与监管用途。'
  - protected_id: PCR-038
    prior_locator: 'Feasibility, resources, risks, alternatives, and stop conditions > Limitations and boundary conditions item 8'
    revised_locator: 'Feasibility, resources, risks, alternatives, and stop conditions > Limitations and boundary conditions item 8'
    semantic_status: preserved
    evidence: '观测和删失概率/权重依赖冻结模型与可观测历史，极端权重、未测量驱动及跨库政策差异导致残余偏倚均保留。'
  - protected_id: PCR-039
    prior_locator: 'Feasibility, resources, risks, alternatives, and stop conditions > Limitations and boundary conditions item 9'
    revised_locator: 'Feasibility, resources, risks, alternatives, and stop conditions > Limitations and boundary conditions item 9'
    semantic_status: preserved
    evidence: '两项试验的数据权限、逐时变量与功效未核实、EXIT-SEP 重叠风险以及随机分配不识别中介网络均保留。'
  - protected_id: PCR-040
    prior_locator: 'Feasibility, resources, risks, alternatives, and stop conditions > Limitations and boundary conditions item 10'
    revised_locator: 'Feasibility, resources, risks, alternatives, and stop conditions > Limitations and boundary conditions item 10'
    semantic_status: preserved
    evidence: '动物机制、平台、样本量、伦理、预算、人鼠转化冲突和不构成临床模型外部验证的限制均保留。'
  - protected_id: PCR-041
    prior_locator: 'Feasibility, resources, risks, alternatives, and stop conditions > Limitations and boundary conditions item 11'
    revised_locator: 'Feasibility, resources, risks, alternatives, and stop conditions > Limitations and boundary conditions item 11'
    semantic_status: preserved
    evidence: '建模前约束表、团队和计算承诺未完成，12–18 个月只约束核心实证研究，条件性后续无既定时间和资源承诺均保留。'
  - protected_id: PCR-042
    prior_locator: 'Feasibility, resources, risks, alternatives, and stop conditions > Risks, alternatives, and stop conditions row 1'
    revised_locator: 'Feasibility, resources, risks, alternatives, and stop conditions > Risks, alternatives, and stop conditions row 1'
    semantic_status: preserved
    evidence: '月 2 两库组合失败、盲于模型表现的预登记替代及替代仍失败后停止跨库分析和潜在状态建模均保留。'
  - protected_id: PCR-043
    prior_locator: 'Feasibility, resources, risks, alternatives, and stop conditions > Risks, alternatives, and stop conditions row 2'
    revised_locator: 'Feasibility, resources, risks, alternatives, and stop conditions > Risks, alternatives, and stop conditions row 2'
    semantic_status: preserved
    evidence: '约束表缺项时补齐专家轮次与记录、禁止数据团队代填以及月 2 仍不合格不拟合主模型均保留。'
  - protected_id: PCR-044
    prior_locator: 'Feasibility, resources, risks, alternatives, and stop conditions > Risks, alternatives, and stop conditions row 3'
    revised_locator: 'Feasibility, resources, risks, alternatives, and stop conditions > Risks, alternatives, and stop conditions row 3'
    semantic_status: preserved
    evidence: '团队或计算不足时先取消第三库、亚组和非必需消融，重新基准后五角色或两库核心计算仍不足即停止复杂模型路线。'
  - protected_id: PCR-045
    prior_locator: 'Feasibility, resources, risks, alternatives, and stop conditions > Risks, alternatives, and stop conditions row 4'
    revised_locator: 'Feasibility, resources, risks, alternatives, and stop conditions > Risks, alternatives, and stop conditions row 4'
    semantic_status: preserved
    evidence: '最小模型恢复失败时按状态数、转移、停留时间、交互次序简化并重跑诊断，仍失败则停止统一潜在状态主张。'
  - protected_id: PCR-046
    prior_locator: 'Feasibility, resources, risks, alternatives, and stop conditions > Risks, alternatives, and stop conditions row 5'
    revised_locator: 'Feasibility, resources, risks, alternatives, and stop conditions > Risks, alternatives, and stop conditions row 5'
    semantic_status: preserved
    evidence: '外部必需状态迁移失败时保留开发标签、不以结局重定义或强配，完整表示失败、受影响任务失败和其他任务最多部分支持均保留。'
  - protected_id: PCR-047
    prior_locator: 'Feasibility, resources, risks, alternatives, and stop conditions > Risks, alternatives, and stop conditions row 6'
    revised_locator: 'Feasibility, resources, risks, alternatives, and stop conditions > Risks, alternatives, and stop conditions row 6'
    semantic_status: preserved
    evidence: '未通过 Holm 的任务仍报告估计量和区间、其他任务检验不变、该任务不支持且不能由其他任务、校准、第三库、RCT 或动物研究补救。'
  - protected_id: PCR-048
    prior_locator: 'Feasibility, resources, risks, alternatives, and stop conditions > Risks, alternatives, and stop conditions row 7'
    revised_locator: 'Feasibility, resources, risks, alternatives, and stop conditions > Risks, alternatives, and stop conditions row 7'
    semantic_status: preserved
    evidence: '复现失败时暂停解释，核对字段血缘、患者聚类、权重和代码，仍失败则不提交全病程状态或外部验证主张，均保留。'
  - protected_id: PCR-049
    prior_locator: 'Contribution, innovation, impact, application, and closest-work comparison > Bounded contribution frame'
    revised_locator: 'Feasibility, resources, risks, alternatives, and stop conditions > Limitations and boundary conditions item 1'
    semantic_status: preserved
    evidence: '首个、完整、无人研究、首次完整人体系统和首次动态状态方法均在唯一限制权威位置明确列为不受支持。'
  - protected_id: PCR-050
    prior_locator: 'Limitations and boundary conditions item 5; Primary model and task-specific comparators'
    revised_locator: 'Feasibility, resources, risks, alternatives, and stop conditions > Limitations and boundary conditions item 5'
    semantic_status: preserved
    evidence: '边、权重与治疗系数仅作预测性条件时间关联；因果调控、最优治疗、治疗作用、反事实个体效应和中介网络均明确不受支持。'
  - protected_id: PCR-051
    prior_locator: 'Contribution > Anticipated impact and application; Result-dependent interpretations'
    revised_locator: 'Feasibility, resources, risks, alternatives, and stop conditions > Limitations and boundary conditions items 6–7'
    semantic_status: preserved
    evidence: '潜在状态/锚定/预测/重建不证明真实生物状态，预测改善不支持临床效用、真实世界效果、部署、治疗建议、机制或监管用途，均完整保留。'
  - protected_id: PCR-052
    prior_locator: 'Research design and methods > Conditional randomized-trial and animal follow-up; Risks, alternatives, and stop conditions row 6'
    revised_locator: 'Research design and methods > Conditional randomized-trial and animal follow-up; Risks, alternatives, and stop conditions row 6'
    semantic_status: preserved
    evidence: 'RCT 或动物研究不能改写核心任务失败；随机分配不自动识别中介网络，动物结果不构成临床模型外部验证，三项禁限均保留。'
undeclared_scientific_changes: []
findings: []
unresolved_issues: []
---

# Content-preservation check

## Decision rationale

v003 与 v004 的五项 `identity_anchor` 值逐字段、逐字一致。PCR-001 至 PCR-052 均能在 v004 中找到同义且同强度的对应内容；没有新增数据、方法、结果或证据，没有把计划写成已完成，也没有把条件性研究改写为确定性研究。修订差异属于术语明确、定义补足、段落聚合和重复内容删除。

## Protected-content trace

主要位置变化是将 PCR-031 至 PCR-041 的完整限制集中在 `Limitations and boundary conditions`，并将 PCR-042 至 PCR-048 保留在紧邻的停止条件表。摘要、贡献、证据链和结果解释删除了重复的完整限制清单，但唯一权威位置仍覆盖原有限制及其强度。PCR-049 至 PCR-051 所列不支持主张也可在该权威位置逐项定位。PCR-023、PCR-024 和 PCR-052 的随机试验与动物研究仍保留各自资格、解释边界和不可补救后果；新增的分支独立说明只是把原有两个条件分支的关系写明，没有改变任一分支的前提或后果。

任务三由“部分观测下状态估计”在面向读者处明确为“部分观测下的临床测量值预测”，但其六个器官功能域、三类器官支持、连续块遮蔽、真实测量目标、评分、权重、比较模型与判定规则均不变；机器可核验的身份锚仍逐字保留。因此该变化没有改变推断目标。

## Required routing

保真结论为 `scientific_content_preserved`。该修订稿可进入新的独立叙事与语言评估，无需返回科学审查。
