---
schema_version: research-idea.v3
plugin_version: "0.10.0"
artifact_id: idea-dossier-I01-001-v001
workflow_id: sepsis-complex-system-idea-generation-v001
idea_id: I01-001
version_id: v001
path: 03_ideas/nodes/I01-001/dossiers/idea-dossier-v001.md
parent_idea_ids: []
based_on:
  - artifact_id: user-idea-v001
    version: v001
    path: 00_input/user-idea-v001.md
  - artifact_id: research-context-brief-v001
    version: v001
    path: 01_context/research-context-brief-v001.md
  - artifact_id: evidence-map-v001
    version: v001
    path: 02_evidence/evidence-map-v001.md
  - artifact_id: opportunity-map-v001
    version: v001
    path: 02_evidence/opportunity-map-v001.md
source_skill: multi-path-idea-generator
created_round: 1
change_type: create
identity_anchor:
  primary_research_question: >-
    在成人重症监护患者中，预先限定的低维脓毒症动态状态表示能否从公开纵向临床数据中得到稳定估计，并在异质外部数据库中保持状态估计、转移时间和未来轨迹预测的校准？
  primary_objective: >-
    构建并跨数据库验证一个区分生理过程、观测过程和临床处置过程的受约束动态状态模型，同时给出其可迁移范围和失效边界。
  study_object: >-
    成人重症监护期间感染、脓毒症发生及其后器官功能状态随时间的演化。
  core_data_or_evidence_base: >-
    文献与临床专家形成的结构约束，以及至少两个异质公开成人重症监护纵向数据库中的生命体征、实验室检查、治疗记录和临床事件。
  primary_unit_of_inference: >-
    成人重症监护患者的一次住院或重症监护经历及其中按时间定位的状态与状态转移。
frozen: true
---

# 受约束的脓毒症动态状态模型：跨数据库状态估计、转移预测与失效边界

## Title, summary, audience, and positioning

- **Title:** 受约束的脓毒症动态状态模型：跨数据库状态估计、转移预测与失效边界
- **One-sentence complete-Idea summary:** 本研究聚焦成人重症监护患者脓毒症随时间演化的临床状态，以文献与专家知识限定的低维动态状态模型在公开纵向数据库中估计状态及允许转移，并在未参与建模的异质数据库中分项检验，从而形成可检验的动态表示、迁移能力与失效边界，同时为达到预定门槛后研究随机治疗效果是否随患者状态而异及开展单一机制桥接提供冻结模型。
- **Primary audience:** 脓毒症与重症医学研究者、系统科学与系统辨识研究者、临床人工智能研究者、临床研究方法学与统计学研究者，以及医学期刊编辑和同行评审者。
- **Positioning and contribution frame:** 科学主线是受约束的动态状态表示；跨数据库任务基准是检验该表示的验证框架和可独立报告的研究贡献，而不是另一项研究身份。模型用于估计预测性状态和时间关联，不把电子病历中的边或权重解释为因果作用、临床控制策略或数字孪生。

本构想中的“动态状态模型”是用少量临床可解释状态概括患者在一个时点的生理与器官功能构型，并描述这些状态随时间转移的概率模型。“受约束”是指状态含义、变量角色、允许转移和时间尺度先由文献与结构化专家知识限定，数据仅在这些边界内估计转移、观测和不确定性。“跨数据库验证”是把结构和参数冻结后，在未参与建模的数据库中检验；其中“校准”指预测的概率或时间分布与实际发生频率或时间是否一致。用户提出的“人体开放复杂巨系统”在本研究中被操作化为一个与治疗、测量和外部环境持续交换信息的临床系统视角；当前模型只表示公共重症监护数据可观测并可检验的部分。

本 dossier 的 12–18 个月实证核心对应用户设定的第二阶段。第一阶段形成的文献—专家结构是其输入；随机试验二次分析和动物机制研究均为满足明确证据门槛后的后续研究，不进入这 12–18 个月的必需交付范围。

## Structured abstract

- **Background and gap:** 脓毒症是感染相关、随时间变化且高度异质的器官功能障碍；现有轨迹、表型、多状态和状态空间研究已覆盖若干局部问题，但尚缺一个在分析前限定、明确区分生理—观测—处置过程、分别验证不同预测任务并接受异质数据库检验的状态—转移表示（Singer et al., 2016；Klouwenberg et al., 2019；Raghu et al., 2017；Sauer et al., 2022）。
- **Objective and hypothesis:** 目标是构建一个低维、临床可解释的受约束动态状态模型，并检验其状态估计、转移时间和未来轨迹预测能否在外部数据库维持校准；核心假设是，预先限定结构并显式表示测量过程的模型会比简单多状态基准产生更稳定、可复核的跨库表示。
- **Approach:** 先完成数据访问、变量语义、时间戳、事件率和标签实现审计，把文献与结构化专家意见转化为有限状态及允许转移；随后在一个公开成人重症监护数据库中估计受约束的隐半马尔可夫模型，即同时估计未直接观测的临床状态、各状态停留时间及其转移的概率模型，并在至少一个异质数据库中冻结验证。脓毒症发生时间、死亡或恢复转移时间、部分观测下状态估计和未来轨迹预测使用各自的参照标准与指标。
- **Expected result:** 预期得到一个可复现的状态定义与转移模型、四类任务的分项性能与校准结果、简单基准比较，以及不作外部再训练时和仅作预定校准时的跨库迁移与失效图谱。
- **Contribution and impact:** 计划贡献是给出一个可证伪的脓毒症动态表示及其跨库证据边界，为动态风险研究、有限观测下状态估计和后续冻结模型的随机试验问题提供共同坐标。

## Background, current state, gap, significance, and rationale

### Background

Sepsis-3 将脓毒症定义为感染所致宿主反应失调引起的危及生命的器官功能障碍，当前成人指南同时强调脓毒症仍是临床诊断，不能由单一筛查分数替代（Singer et al., 2016；Prescott et al., 2026）。患者的感染负荷、器官功能、治疗暴露、测量频率和结局均随时间变化，并通过临床处置和资料记录过程彼此关联。因而，本研究把脓毒症视为一个开放的临床复杂系统：系统持续接收治疗和环境输入，生理与器官功能构成内部状态，死亡、恢复和其他临床事件构成可观测输出。这里的“反馈回路”指既往状态影响后续处置、后续观测又影响下一步处置的时间有向循环；约束表提出允许回路，观察性数据估计其中的预测性时间关联。

### Current state

MIMIC-IV、eICU-CRD、HiRID、AmsterdamUMCdb 和 SICdb 等公开资源提供了不同中心、地域和采样密度的成人重症监护纵向数据（Johnson et al., 2024；Pollard et al., 2018；Hyland et al., 2020；Thoral et al., 2021；SICdb, 2025）。既有研究已描述静态脓毒症表型、体温和器官功能轨迹、多状态病程、连续或切换状态空间、动态贝叶斯网络及个体化模拟原型；其中，多状态模型把病程划为互斥临床状态并估计转移，状态空间模型用未直接观测的状态连接重复测量与随时间的演化，动态贝叶斯网络则表示跨时点变量之间的概率依赖。近期工作也已开展跨数据库恶化轨迹预测（Seymour et al., 2019；Klouwenberg et al., 2019；Xu et al., 2022；Raghu et al., 2017；Ghassemi et al., 2017；De Blasi et al., 2021；Lal et al., 2020；npj Digital Medicine, 2026）。外部验证研究则显示，重症监护预测模型迁移后常出现性能或校准下降（Wong et al., 2021；ICU AI External Validation Review, 2025）。

### Gap

现有证据尚不能回答：能否在建模前固定一个维度受限、临床可解释的状态集合与转移结构，使它在区分生理变化、测量行为和治疗记录的同时，分别完成当前状态估计、状态转移时间和未来轨迹预测，并在异质数据库中维持可辨认的状态语义和校准。脓毒症标签实现的细微差异能够改变病例识别和预测结果，缺失模式又携带临床测量行为的信息，因此单一总体准确率不能证明这一动态表示成立（Sepsis-3 Label Variation Study, 2024；Che et al., 2018；TRIPOD+AI, 2024；PROBAST+AI, 2025）。

### Significance

若同一状态—转移表示能在独立数据库中复现，它可为发病风险、器官功能演变、有限观测下状态估计和后续轨迹预测提供一致但分项验证的坐标。若该表示不能迁移，预先规定的外部检验仍可指出哪些状态、时间尺度、变量组合或测量过程不能由常规重症监护数据稳定辨识，从而避免把单中心相关结构直接带入临床研究或后续干预问题。

### Rationale

先用文献和结构化专家意见限定少量状态、变量角色、允许转移及时间尺度，可把原始“反馈系统”设想缩减为可以估计和证伪的模型；再让纵向数据只估计允许结构内的状态、停留时间和转移不确定性，可区分先验结构与数据贡献。将四类目标拆成独立任务，并以至少一个异质外部数据库检验冻结模型，使跨库迁移性成为动态状态模型的验证证据。只有该模型和分析问题冻结并达到预定门槛后，随机试验才用于检验预先规定的治疗效应修饰，即随机治疗效果是否随冻结状态而异；动物研究才可能用于单一、明确的人类机制假设。

## Research question, objectives, and core hypothesis

**Primary research question.** 在成人重症监护患者中，一个由文献与专家知识预先限定、显式区分生理状态、测量过程和治疗记录的低维动态状态模型，能否从公开纵向数据中得到稳定估计，并在异质外部数据库中保持状态语义、转移时间预测和未来轨迹预测的校准？

**Objectives.**

1. 建立可审计的变量本体和结构约束表，明确临床指标、治疗输入、观测行为和事件结局的角色、时间尺度及允许转移。
2. 在开发数据库中估计受约束的隐半马尔可夫动态状态模型，输出患者时点的状态后验概率（结合已观测资料后属于各状态的概率）、状态停留时间、允许转移概率及不确定区间。
3. 分别评价脓毒症发生及时间、死亡或恢复转移时间、部分观测下状态估计和未来轨迹预测，不使用一个合成准确率替代四项任务。
4. 在至少一个异质外部数据库中冻结检验状态定义、转移、校准和任务表现，并区分无调整迁移与预先规定的有限校准。

**Core hypothesis.** 与仅由结局驱动的无约束模型或简单多状态模型相比，预先限制状态维度和转移图、并显式表示测量过程的动态模型，将在开发数据中形成更稳定的状态估计，并在外部数据库中保留更好的状态对应关系和任务校准；这种增益应体现在多个独立任务的预定指标上，而不是单一内部区分度。

**Supporting hypotheses.**

- 对测量指示、距上次测量时间和测量频率进行显式建模，可提高临床样式遮蔽下的观测重建覆盖率和状态估计稳定性。
- 在外部数据库不重新学习状态结构时仍可识别相近状态语义和转移顺序，将支持该表示具有跨库可迁移性；只在有限校准后恢复性能，则支持参数层面的迁移而非完整结构迁移。
- 若状态语义、转移或校准不能外部复现，预先规定的失败模式能够定位变量语义、时间尺度、标签或测量过程所决定的边界。

## Research content and work packages

| 研究单元 | 时间 | 核心活动 | 主要交付物 |
|---|---:|---|---|
| 1. 协议、数据与约束冻结 | 第 0–3 个月 | 核验数据库准入和版本；完成变量、单位、时间戳、标签、事件率与缺失模式审计；把第一阶段的文献与专家知识转为状态候选、变量角色、允许转移和异议记录；预先规定任务、切分、指标和外部验证顺序 | 版本固定的研究方案、队列和标签定义、共同变量字典、约束表、分析计划 |
| 2. 动态状态模型建立 | 第 3–8 个月 | 建立简单多状态基准；估计受约束隐半马尔可夫模型；检查状态可分性、停留时间、参数稳定性、后验不确定性和测量过程拟合；冻结模型与代码 | 基准模型、冻结的动态状态模型、状态说明书、诊断报告 |
| 3. 分项任务与外部验证 | 第 7–13 个月 | 在患者级隔离的内部时间划分中完成四类任务；在外部数据库首先进行无调整验证，再进行预定的有限校准分析；比较状态匹配、转移、校准和任务指标 | 四项任务的分项结果、外部验证结果、基准比较、迁移矩阵 |
| 4. 压力测试、复现与论文产出 | 第 12–18 个月 | 进行标签实现、时间窗、测量遮蔽、变量子集和数据库差异的预定敏感性分析；在数据条件满足时增加一个地域压力测试；由未参与主建模的分析者复现核心结果；整理代码、数据字典和论文 | 失效边界图谱、复现记录、可共享代码与变量映射、以第二阶段为核心的论文稿 |

第 12 个月的最低完成点是冻结模型、两个异质数据库的核心外部验证和四项任务的分项报告；第 13–18 个月用于地域压力测试、复现、敏感性分析和论文整合。随机试验和动物实验不占用该时间表。

## Data, materials, and existing evidence base

### Planned data and materials

| 数据或材料 | 在本研究中的角色 | 当前证据或访问状态 |
|---|---|---|
| 第一阶段文献—专家约束表 | 提供候选状态、变量角色、允许转移、时间尺度及异议；进入第二阶段前冻结 | 用户已规定该来源类型，但尚未提供完成的约束表、专家名册或征询记录 |
| MIMIC-IV | 计划作为开发数据库，构建成人重症监护队列、估计模型并作内部时间验证 | 官方数据库及访问条件已有可核验资料；本项目的账户准入、字段覆盖和样例提取尚未核验（Johnson et al., 2024） |
| eICU-CRD | 计划作为主要多中心外部验证数据库 | 官方数据库及访问条件已有可核验资料；本项目的账户准入、字段映射和标签复现尚未核验（Pollard et al., 2018） |
| HiRID、AmsterdamUMCdb 或 SICdb | 在共同变量、事件率和时间戳满足预定要求时，选择其中一个作为额外地域或高时间分辨率压力测试 | 数据资源存在得到官方来源支持；项目级访问和共同变量审计未完成（Hyland et al., 2020；Thoral et al., 2021；SICdb, 2025） |
| 中国感染重症监护数据 | 候选地域压力测试，不承担模型开发 | 官方资料显示约 2,790 例、单中心且存在较多缺失；拟用变量覆盖尚未核验（Zigong ICU Infection Data, 2022） |
| EXIT-SEP 个体数据 | 仅在模型冻结并达到门槛后，用于预先规定的随机治疗效应修饰问题 | 试验论文已发表；用户称有机会获取原始数据，但使用权、代码本、逐时变量和分析功效均未核实（Liu et al., 2023） |
| XBJ-SCAP 个体数据 | 仅在疾病范围和变量适配时作为后续补充或独立检验 | 试验论文已发表；数据访问与逐时变量未核实，且研究对象是重症社区获得性肺炎而非一般脓毒症队列（Song et al., 2019） |
| 临床专家调查资源 | 结构化界定状态、变量角色、允许转移和临床解释 | 用户允许使用；专家来源、人数、专业构成、时间投入和一致性程序尚未确定 |

### Variable roles

- **外部输入与处置记录：** 抗感染治疗、液体、血管活性药物、呼吸支持和其他有可靠时间戳的临床处置；在模型中作为时间变化的观测输入。
- **生理和器官功能观测：** 生命体征、实验室检查、器官支持和能够跨库协调的临床指标；这些变量通过观测模型连接到低维状态。
- **观测过程：** 是否测量、测量频率、距上次测量的时间和记录来源；该过程与生理观测分开表示。
- **临床事件与结局：** 脓毒症发生、恢复、死亡、出重症监护和其他预先规定事件；不同任务使用各自参照标准。

### Existing evidence base

总体证据只部分覆盖拟议研究对象。临床定义、公开数据库存在性、数据库异质性、外部性能下降、缺失信息的重要性以及动态表型和状态空间最近邻均有已发表来源支持（Singer et al., 2016；Sauer et al., 2022；Che et al., 2018；Klouwenberg et al., 2019；Raghu et al., 2017）。标签实现对结果的影响目前主要由单一针对性研究支持（Sepsis-3 Label Variation Study, 2024）。EXIT-SEP、XBJ-SCAP 和 EXIT-SEP 表型事后分析分别有单一直接来源（Liu et al., 2023；Song et al., 2019；EXIT-SEP Phenotype Analysis, 2025）。人鼠炎症反应的可转化性证据存在冲突（Seok et al., 2013；Takao and Miyakawa, 2015）。任何“首个”或“完整系统”表述均未获得核实。

## Research design and methods

### Population, timing, and reference standards

研究建立两个相互关联但估计目标不同的成人重症监护队列。感染风险队列从满足预先规定的疑似感染条件、且尚未达到脓毒症标签的时点开始，用于脓毒症发生及发生时间预测；脓毒症队列从冻结的 Sepsis-3 电子病历实现所定义的索引时点开始，用于当前状态、死亡或恢复转移时间及未来轨迹。患者级数据在任何特征构建前隔离，开发数据库采用时间分割和中心分层重采样，外部数据库不参与状态结构选择。

每项任务单独冻结纳入标准、时间零点、预测时距、参照标准、删失和竞争事件处理。感染窗口、器官功能基线和预测提前量采用可执行代码定义，并在模型训练前完成标签版本比较。恢复作为一个与死亡竞争的临床状态，其操作性定义在协议冻结时确定；出院或停止测量不自动等同于生理恢复。

### Constraint register and variable mapping

第一阶段输出被转换为可审计约束表，逐项记录状态候选、变量角色、允许和禁止的转移、可能的时间滞后、文献依据、专家支持及异议。约束只规定模型可以估计哪些关系，不预设关系强度或方向。变量映射以临床概念为单位，明确原始字段、单位换算、聚合窗、异常值规则和数据库特异差异；同一变量若在不同时间承担不同角色，必须在约束表中分别说明。

专家意见采用结构化、分轮征询，临床医学、系统科学、系统辨识和人工智能代表分别作答；共识规则在查看结局关联前固定，未达共识的关系不作为强制边。数据团队只在共同变量和时间戳审计后把约束映射到可估计对象，并保留无法映射的项目。

### Primary model and comparators

主要模型为受约束的隐半马尔可夫动态状态模型。有限个潜在状态表示低维生理与器官功能构型；半马尔可夫停留时间分布允许转移风险依赖患者已处于当前状态的时长；观测模型把生命体征和实验室检查连接到状态；单独的测量模型表示测量指示、距上次测量时间和频率。治疗记录作为时间变化输入进入转移模型，其系数只描述给定观测条件下的时间关联。

状态数从协议预定的小范围中选择，选择依据限于开发数据内的状态可分性、参数可辨识性、后验稳定性、临床一致性和预测外样本拟合，不使用外部数据库结果调节结构。输出包括每个患者时点的状态后验概率、停留时间分布、允许转移概率、观测重建分布和不确定区间。

最低比较模型是使用同一队列、时间轴和结局定义的简单多状态 Markov 模型。各预测任务另设一个透明的任务基准：发病和结局任务使用预定的 landmark 回归或生存模型，即在固定评估时点只用此前信息估计后续风险；观测重建使用最近一次有效观测和按开发集估计的简单条件模型。所有基准共享同一数据切分，避免把数据处理差异误认为模型增益。

### Four separated evaluation tasks

| 任务 | 参照标准与信息时点 | 主要输出 | 预定指标族 |
|---|---|---|---|
| 脓毒症是否及何时发生 | 感染风险队列中的冻结 Sepsis-3 标签；仅使用预测时点之前的信息 | 各预测时距的发生风险和时间分布 | 时间依赖区分度、精确率—召回率、综合 Brier 分数、校准曲线、校准截距与斜率、提前量分布 |
| 何时转向死亡或恢复 | 脓毒症索引时点后的竞争状态定义 | 状态特异累积发生概率、转移时间分布 | 状态特异 Brier 分数、累积发生校准、时间误差、预测区间覆盖率 |
| 部分观测下的状态估计 | 对真实已测量值进行符合临床测量模式的连续块遮蔽；潜在状态不设虚构金标准 | 已测量变量的后验重建、状态后验及不确定性 | 连续与分类变量的重建误差、对数评分、预测区间覆盖率、重复遮蔽下状态一致性 |
| 后续演化过程及结果 | 预定 landmark 时点之后的生理轨迹、状态转移和临床事件 | 多步状态概率、轨迹分布和事件风险 | 多步对数评分、轨迹误差、动态 Brier 分数、校准、状态序列相似度 |

四项任务分别报告样本量、事件数、缺失模式、指标及不确定区间，不构造一个总体“成功分数”。部分观测任务把已测量值重建与潜在状态估计分开；前者可由保留真值评价，后者由未来观测、状态转移和外部稳定性间接检验。

### Validation and transport

开发数据库中的内部验证使用患者级时间分割，并通过 bootstrap 或重复分割估计不确定性。冻结状态定义、变量映射、模型参数、任务代码和阈值后，在 eICU-CRD 首先进行完全无调整的外部验证；随后仅在预先指定的校准子集中估计截距、基线风险或状态占比校准，并在互斥验证子集中评价有限校准后的结果。外部数据不得用于增加状态、改变允许转移或选择报告指标。

跨库验证同时比较：变量可获得率和测量强度；状态后验分布及临床特征；转移矩阵和停留时间；每项任务的区分度、校准和不确定性；简单基准与主要模型的相对表现。若额外数据库通过数据审计，则以同样冻结的流程作地域或高时间分辨率压力测试。

### Design authority for alternatives and conditional follow-up

1. **数据库资格与替代。** 主要分析要求至少两个在患者构成或地域上异质、且能执行同一核心标签和共同变量表的数据库。若 MIMIC-IV 或 eICU-CRD 不能满足预定数据要求，可在 HiRID、AmsterdamUMCdb 或 SICdb 中替代一个；若不能形成两个合格数据库，则不开始跨库模型估计，并把研究设计退回数据范围重定。
2. **模型结构与停止。** 若预定候选状态数中没有任何模型达到开发数据内的参数可辨识性和重复分割稳定性要求，则按预定顺序减少状态数；最小状态模型仍不能稳定估计时，停止对潜在动态结构的解释，保留数据协调和简单多状态基准作为否定证据，但不把它改写为已建立的复杂系统模型。
3. **外部失效处理。** 外部无调整验证失败时，保留冻结结构并报告失败位置；只执行预定的有限校准分析，不使用外部结局重新选择状态、边或任务。有限校准仍失败时，结论限定为开发环境内表示。
4. **随机试验后续。** 只有在状态定义、代码和分析问题完全冻结，至少一个异质外部数据库达到预先规定的任务与校准门槛，且 EXIT-SEP 的使用权、逐时变量、分析时点、交互功效和与既有表型分析的差异均经核验后，才检验一个预先规定的随机治疗效应修饰问题。若研究中介路径，即治疗通过某个中间变量影响结局的路径，必须另行写明可识别的有限路径和中介—结局混杂假设。XBJ-SCAP 仅在重症社区获得性肺炎的疾病边界与变量时点适合该问题时使用。任一条件不满足即不开展相应分析。
5. **动物机制后续。** 只有公开数据与合格随机试验分析共同指向一个具体、可干预且在人类资料中可测量的机制，且该机制需要实验区分替代解释时，才设计一个符合 MQTiPSS 与 ARRIVE 2.0 的动物研究；否则不启动动物实验，也不把动物结果视作临床预测模型的外部验证。

## Key techniques and implementation

1. **可执行队列与标签。** 将感染窗口、器官功能基线、索引时点、预测时距、恢复、死亡和删失规则实现为可测试代码；保存数据库版本、字段来源和每一步队列计数。
2. **跨库概念协调。** 为每个概念保存原始字段、单位、采样频率、时间聚合、异常值规则和缺失编码；所有站点共用核心字典，数据库特异扩展不进入主要跨库模型。
3. **约束与异议管理。** 结构化专家征询保存专业背景、独立评分、理由、共识和少数意见；模型代码从冻结约束表读取允许转移，防止分析者在看到结果后修改网络。
4. **不规则时间与测量过程。** 保留真实时间间隔，以停留时间分布和距上次测量时间处理非规则采样；同时建模测量指示，避免把常规填补值当作直接观测。
5. **参数估计与诊断。** 使用多初值拟合、患者级重采样、后验预测检查、状态占用与转移稀疏性检查、参数不确定区间及状态标签对齐，区分数值收敛与科学可辨识性。
6. **外部验证隔离。** 由独立脚本加载冻结模型；无调整验证完成并锁定后才运行预定校准分析。开发、校准和验证患者互斥。
7. **可复现交付。** 固定软件环境、随机种子和数据版本，提供数据字典、抽取查询、模型配置、评估代码和报告模板；受许可限制的数据不导出，只发布可复现的生成步骤。
8. **报告规范。** 按 TRIPOD+AI 报告模型、数据和验证，使用 PROBAST+AI 项目检查偏倚风险与适用性；随机试验后续若被触发，再使用 CONSORT 亚组解释原则和 AGReMA 中介报告要求。

## Evidence chains

### Evidence chain: 从临床知识到可估计的动态结构

- **Input:** Sepsis-3 临床定义、已发表的多状态和状态空间近邻、第一阶段文献—专家材料、公开数据库字段与时间戳（Singer et al., 2016；Klouwenberg et al., 2019；Raghu et al., 2017）。
- **Method / analysis / processing:** 将变量分为治疗输入、生理观测、观测过程和临床事件，结构化征询少量状态与允许转移，完成跨库概念映射和可辨识性审计，在查看外部结局前冻结约束。
- **Output:** 带来源和异议记录的变量本体、有限状态说明、允许转移图、时间尺度和可估计对象清单。
- **Supports:** 目标 1，并为“受约束”这一标题和定位主张提供可执行依据。

### Evidence chain: 从纵向观测到状态与转移估计

- **Input:** 开发数据库中的患者级生命体征、实验室检查、治疗时间戳、测量行为和事件结局，以及冻结约束表。
- **Method / analysis / processing:** 估计受约束隐半马尔可夫模型，分别拟合状态停留时间、允许转移、生理观测和测量过程；用多初值、重复分割、后验检查和简单多状态基准检验稳定性。
- **Output:** 患者时点的状态后验、状态停留时间、允许转移概率、观测重建分布和参数不确定区间。
- **Supports:** 目标 2，以及动态状态可以在预先限定结构内被估计的核心假设。

### Evidence chain: 从冻结模型到四项独立任务证据

- **Input:** 冻结模型、感染风险队列、脓毒症队列、任务特异的时间零点与参照标准、患者级隔离的内部验证数据。
- **Method / analysis / processing:** 分别评价脓毒症发生时间、死亡或恢复转移时间、临床样式遮蔽下的观测重建与状态稳定性，以及未来状态和结局轨迹；与透明任务基准在相同数据切分中比较。
- **Output:** 每项任务的区分度、校准、时间误差、对数评分、覆盖率、基准差异和不确定区间。
- **Supports:** 目标 3，并检验一个动态表示能否在不同估计任务中提供一致而非合成的证据。

### Evidence chain: 从外部数据库到迁移能力与失效边界

- **Input:** 完全冻结的状态定义、变量映射、模型、任务代码和阈值，以及至少一个未参与建模的异质重症监护数据库（Sauer et al., 2022；ICU AI External Validation Review, 2025）。
- **Method / analysis / processing:** 先进行无调整外部验证，再在互斥样本中进行预定的有限校准；比较状态语义、占用、停留时间、转移、任务校准和基准相对表现，并按数据库差异定位失效。
- **Output:** 无调整和有限校准结果、跨库状态对应矩阵、迁移结果与按变量、标签、时间尺度和测量过程组织的失效边界图谱。
- **Supports:** 目标 4，以及跨数据库验证作为动态状态模型验证与可发表贡献的定位。

## Required analyses and evidence

### Before model fitting

- 数据库准入、许可、版本、可用字段、时间戳精度、事件率、随访、重复住院和跨表链接审计。
- 共同变量的语义、单位、采样窗、异常值和缺失编码映射，以及数据库特异变量的隔离规则。
- Sepsis-3 标签版本比较、时间零点验证、预测信息截断检查、恢复定义和竞争事件规则。
- 专家遴选、结构化征询、共识阈值、异议保留和文献来源记录。
- 状态数候选范围、允许转移、时间尺度、任务层级、指标、数值门槛和外部验证顺序的协议冻结。

### During model development

- 状态占用、转移稀疏性、停留时间、参数可辨识性、多初值一致性、重复分割稳定性和后验预测检查。
- 对测量指示、测量频率和距上次测量时间的拟合检查，以及随机遮蔽与临床样式连续块遮蔽的对照。
- 与简单多状态模型和透明任务基准的相同切分比较；去除专家约束、去除测量模型和改变状态数的预定消融分析。
- 患者级时间泄漏、同一患者跨切分、标签由未来信息构建和外部测试集调参的审计。

### External evidence and reporting

- 外部数据库中的队列流程、变量覆盖、标签复现、状态对应、转移与停留时间、任务指标、校准和不确定区间。
- 无调整迁移与有限校准的分开结果，以及病例组合、测量密度、标签和时间尺度对失效的分解。
- 按数据库、中心、关键临床亚组和数据缺失强度进行预定的稳健性分析；亚组结果只用于描述异质性。
- 核心分析的独立代码复现、完整数据字典和 TRIPOD+AI 报告清单。

后续随机试验研究必须另行取得个体数据权限、变量字典、测量时点、事件数、交互功效和既有分析重叠核验；动物研究必须另行取得单一机制链、人类可测指标、实验平台、伦理和样本量证据。这些材料不作为第二阶段模型完成的替代证据。

## Expected outputs, falsification criteria, and interpretations

### Expected outputs

1. 一个可执行的成人重症监护感染风险队列与脓毒症队列定义，以及标签版本和时间零点说明。
2. 一个带来源、角色、允许转移和异议记录的跨学科约束表与共同变量字典。
3. 一个冻结的受约束动态状态模型、简单多状态基准、状态说明书和不确定性输出。
4. 脓毒症发生时间、死亡或恢复转移时间、部分观测下状态估计和未来轨迹四项分开的验证结果。
5. 至少一个异质外部数据库中的无调整验证、有限校准分析和跨库状态对应结果。
6. 一个说明哪些变量、状态、时间尺度和测量过程可以或不能迁移的失效边界图谱，以及可复现代码和论文稿。

### Falsification criteria

- 在预定最小状态数下，状态仍不能在重复分割和多初值中稳定辨认，或允许转移参数无法估计。
- 状态语义或转移顺序在外部数据库中不能对应，且预定的有限校准不能恢复任务校准。
- 主要模型在外部任务上不优于使用相同数据与标签的简单基准，或增益只来自某一数据库的测量频率。
- 临床样式遮蔽显示观测重建区间覆盖不足，状态后验随测量策略大幅改变，不能支持有限观测下的稳定状态估计。
- 预定外部检验发现发病、转移或未来轨迹预测存在系统时间偏差，因而不支持跨库动态表示假设。

### Result-dependent interpretations

| 结果模式 | 允许的科学解释 |
|---|---|
| 状态语义、转移和各任务校准在无调整外部验证中保持 | 支持该低维预测性状态表示在已研究数据库和共同变量范围内可迁移；不推导因果治疗关系 |
| 无调整验证下降，但有限校准后恢复且状态语义稳定 | 支持结构层面部分迁移、参数和基线风险需要本地校准 |
| 开发数据库表现稳定，外部状态或校准不能复现 | 支持数据库特异表示，并由失效图谱界定其边界；不作普适系统主张 |
| 简单多状态基准与主要模型相当或更好 | 不支持复杂潜在状态模型带来额外预测价值；数据协调和任务基准仍作为实证输出报告 |
| 观测重建较好但事件转移或未来轨迹较差 | 只支持测量重建能力，不支持临床状态转移模型 |
| 后续随机试验出现预定交互 | 只解释为随机治疗效应在预定状态上的效应修饰证据，并按交互、多重性和适用人群报告；不自动解释为中介机制 |

## Contribution, innovation, impact, application, and closest-work comparison

### Bounded contribution frame

本研究计划形成三项相互依赖的贡献。第一，建立一个把文献—专家约束与数据估计分开的低维脓毒症动态状态对象，使“反馈系统”设想转化为有限状态、允许转移、停留时间和不确定性。第二，把四类候选成功标准变成同一模型下相互独立的估计任务，避免以一个总体准确率替代发生时间、竞争状态、部分观测和未来轨迹。第三，把跨数据库无调整验证、有限校准和失效定位作为该模型的主要验证与可发表贡献。

这些贡献定位为方法整合、外部验证和基准资源价值，不声称已证明临床有效性、治疗控制作用或个体化干预模拟。科学差异集中在预先限定结构、显式观测过程、任务分离和冻结跨库检验的组合及其输出边界。

### Closest-work comparison

| 最近邻工作 | 已有贡献 | 本研究计划增加的可检验增量 |
|---|---|---|
| Klouwenberg et al. (2019) 的多状态脓毒症病程；Xu et al. (2022) 的 SOFA 轨迹跨队列验证；2026 年跨库恶化轨迹模型 | 已证明多状态病程、器官功能轨迹和动态恶化预测可以在脓毒症中研究 | 在分析前限定状态和允许转移，显式表示测量过程，并让发生、转移、部分观测和未来轨迹共用状态对象但分别验证 |
| Raghu et al. (2017)、Ghassemi et al. (2017) 的连续或切换状态空间；De Blasi et al. (2021) 的动态贝叶斯网络 | 已覆盖潜在状态、转移、器官关系和治疗记录的若干局部建模问题 | 把专家约束与数据估计分开，限制关系为预测性时间关联，并用冻结结构检验跨库状态语义、停留时间和校准 |
| Lal et al. (2020) 的脓毒症数字孪生原型 | 展示了个体化模拟概念 | 本研究不承担个体治疗反事实模拟，而是检验常规重症监护数据中低维状态表示的可估计性、可迁移性和失效边界 |
| Wong et al. (2021) 与 2025 年重症监护人工智能外部验证综述 | 说明开发环境性能不能直接外推 | 把外部验证嵌入状态定义、转移结构和四项任务，而不仅验证单一风险分数 |
| EXIT-SEP 表型事后分析 (2025) | 已检验 SENECA 表型与血必净效应，正式交互未达显著 | 当前研究不重复静态表型分层；只有冻结动态状态且资源、时点和功效满足条件时，才提出一个预定效应修饰问题 |

### Anticipated impact and application

直接应用是研究用途：为跨库脓毒症纵向研究提供可复用的变量字典、状态说明、任务定义、验证代码和失效边界。若外部验证支持，该表示可作为未来动态风险研究和随机试验效应修饰问题的预定分层坐标；若外部验证不支持，结果可明确常规重症监护数据不能稳定承载的状态和时间尺度。任何临床部署、治疗建议或机制主张均需要独立的后续研究。

## Title and positioning claim-support table

| Title or positioning claim, written at its supported scope | Contribution frame in the dossier language | Existing implementation that supports it | Supporting evidence-chain output | Literature or existing-result basis | Actual increment, or a natural-language no-increment statement | Support status in the dossier language |
|---|---|---|---|---|---|---|
| 受约束的脓毒症动态状态模型 | 方法整合：以有限状态、允许转移和停留时间表示可观测范围内的脓毒症演化 | 研究单元 1–2 的约束表、隐半马尔可夫模型、测量模型和简单基准 | “从临床知识到可估计的动态结构”的约束表输出；“从纵向观测到状态与转移估计”的状态后验与转移输出 | 多状态、状态空间和动态贝叶斯网络已有直接近邻，文献基础充分但差异化只得到部分核验（Klouwenberg et al., 2019；Raghu et al., 2017；De Blasi et al., 2021） | 增量是把专家约束、观测过程和状态停留时间组合为一个预先冻结、可外部检验的表示；不主张首次使用动态状态方法 | 作为拟实施方法得到支持；其科学差异须由数据审计和针对性最近邻核验进一步限定 |
| 跨数据库状态估计和转移预测 | 外部验证：以至少一个异质数据库检验冻结模型 | 研究单元 3 的无调整验证、有限校准和状态对应分析 | “从外部数据库到迁移能力与失效边界”的迁移矩阵与校准输出 | 公开数据库异质性和外部性能下降得到较强来源支持（Sauer et al., 2022；Wong et al., 2021；ICU AI External Validation Review, 2025） | 增量是同时检验状态语义、转移、停留时间和四项任务，而非只验证单一风险分数 | 计划内容与证据基础相匹配；结果主张以实际外部验证为限 |
| 用分项任务界定迁移能力与失效边界 | 基准与资源：对发生时间、竞争状态、部分观测和未来轨迹分别给出参照标准、指标与失败位置 | 研究单元 3–4 的四项任务报告、敏感性分析和失效图谱 | “从冻结模型到四项独立任务证据”的分项指标；“从外部数据库到迁移能力与失效边界”的失效图谱 | 标签敏感性、缺失信息和分项报告要求有来源支持，其中标签敏感性主要来自单一针对性研究（Sepsis-3 Label Variation Study, 2024；Che et al., 2018；TRIPOD+AI, 2024） | 增量是把这些要求落实到同一动态状态对象的冻结跨库验证；不声称建立新的通用评价理论 | 在限定为计划中的任务基准和边界图谱时得到支持 |
| 冻结模型可在门槛满足后支持一个随机治疗效应修饰问题 | 条件性转化：把观察性模型作为预先规定分层坐标，而不是因果调控网络 | 方法节规定的模型冻结、外部门槛和试验数据资格条件 | 当前证据链只提供可冻结状态表示；治疗效应输出须由后续随机试验分析另行产生 | EXIT-SEP 试验及其既有表型分析有单一直接来源；个体数据访问与逐时变量未核实（Liu et al., 2023；EXIT-SEP Phenotype Analysis, 2025） | 若被触发，增量须是与既有静态表型分析不同的预定动态效应修饰问题；当前不声称已具备该增量 | 仅作为条件性后续用途成立，不能写成已获得的治疗或机制证据 |

## Feasibility, resources, risks, alternatives, and stop conditions

### Feasibility and resources

| 资源维度 | 已知状态 | 本研究所需安排 |
|---|---|---|
| 时间 | 用户明确第二阶段须在 12–18 个月完成；第一和第三阶段没有给定期限 | 按第 0–13 个月完成两个数据库的核心模型与外部验证，第 12–18 个月重叠完成压力测试、复现和论文整合；不把随机试验或动物实验纳入该时限 |
| 公开数据库 | 多个成人重症监护数据库存在且有官方访问路径；“公开”通常仍需培训、协议或认证；本项目准入尚未核实 | 第 1 个月完成账户、许可和样例提取，第 2 个月完成共同字段与事件率审计；主方案需要开发库和至少一个异质外部库 |
| 专家资源 | 用户允许使用临床专家调查，但没有专家名册、人数和可投入时间 | 在模型拟合前完成临床医学、系统科学、系统辨识和人工智能的独立结构化征询，并保留异议 |
| 协作与计算 | 用户列出的合作领域包括数学与系统科学、控制论、系统辨识、人工智能、中医学和临床医学；具体人员、职责、计算与存储未确认 | 至少需要临床负责人、数据协调负责人、动态模型负责人、统计验证负责人和独立复现分析者；计算资源按两库纵向抽取与多初值拟合配置 |
| EXIT-SEP 与 XBJ-SCAP | 用户陈述为“有机会获取”；论文可核验，但数据使用权、代码本、时点和共同变量未核实 | 只在后续资格核验后使用，不是第二阶段资源前提 |
| 动物研究 | 当前没有具体机制、模型、平台、样本量、伦理路径或预算；转化证据存在冲突 | 不作为第二阶段资源；只有单一机制假设和全部研究条件成立后另行设计 |
| 证据基础 | 当前证据地图为有界检索，临床定义、数据资源、近邻工作和方法边界已有代表性来源 | 定稿前补充针对固定模型对象的最近邻检索，并在论文写作时复核 2026 年来源、勘误和后续验证 |

### Working assumptions

| 待定选择 | 已固定内容 | 决定时点和允许依据 | 未解决的后果 |
|---|---|---|---|
| 目标论文是否以第二阶段单独成文，还是最终与其他阶段整合 | 当前 dossier 和 12–18 个月交付均以第二阶段动态状态模型及跨库验证为核心；第三阶段保持条件性 | 研究方案冻结前由负责人依据论文目标和各阶段实际交付范围确认，不以模型结果反向决定 | 若仍未确认，无法冻结论文主问题、交付边界和作者分工 |
| 主要开发库与外部库的最终组合 | 至少两个异质公开成人重症监护数据库；当前计划为 MIMIC-IV 开发、eICU-CRD 外部验证，额外数据库只作压力测试 | 第 1–2 个月依据实际准入、字段字典、共同变量、时间戳、事件率和许可用途决定；不得依据模型性能选库 | 若不能形成合格的两库组合，不能开展本 Idea 的跨库主分析 |
| 感染窗口、Sepsis-3 电子标签、时间零点、预测时距和恢复定义 | 四项任务必须分开；只使用预测时点前的信息；死亡与恢复按竞争状态处理 | 数据审计后、模型拟合前，由临床与统计负责人依据指南、可执行代码、事件率和标签敏感性分析冻结 | 若未冻结，队列、任务参照标准和性能指标均不可解释 |
| 状态数、核心变量、允许转移、停留时间分布和时间网格 | 状态必须低维、临床可解释；结构来自文献—专家约束；治疗、生理、测量和事件角色分开；外部数据不参与结构选择 | 查看外部结局前，依据共同变量审计、专家共识、开发数据可辨识性和预定诊断选择 | 若未解决，无法估计或冻结动态状态模型 |
| 每项任务的数值成功门槛和进入随机试验后续的外部门槛 | 指标族、至少一个异质外部验证、无调整结果优先、简单基准比较和校准要求已经固定 | 最终训练前，由临床和统计负责人依据预定用途、事件率、基准表现的开发阶段估计和最小可接受校准确定；不得查看外部测试结果 | 若没有预定数值门槛，不得宣称第二阶段“验证通过”，也不得触发随机试验后续 |

### Limitations and boundary conditions

1. 当前证据基础来自面向研究设计的有界检索，不是按系统综述方法完成的穷尽性检索；代表性近邻不能证明不存在同类工作，因而不支持“首个”“完整”或文献空白主张。2026 年来源在定稿时仍需复核正式版本、勘误和后续独立验证。
2. 尚未取得候选公开数据库或随机试验的个体数据、项目账户批准、数据使用协议、样例抽取和完整变量字典；数据库存在或论文发表不等于本项目已经具备访问权、逐时变量和允许用途。
3. 数据库之间的人群、临床实践、变量语义、单位、采样频率、设备记录、治疗时点、缺失编码和结局定义不同。共同变量交集可能使状态表示变窄，外部性能变化可能同时反映病例组合、标签和测量过程差异。
4. 脓毒症标签、感染窗口、SOFA 基线、索引时点、预测提前量和恢复定义会改变病例与任务结果；标签敏感性的直接实证基础目前主要来自一项针对性研究，具体定义尚未完成项目级验证。
5. 重症监护电子病历属于观察性资料。治疗受到病情和既往治疗影响，测量行为也由临床判断驱动；模型边和权重只能解释为条件时间关联，不能识别因果调控、临床控制作用、最优治疗策略或反事实个体治疗效果。
6. 潜在状态没有直接金标准。真实保留测量可以评价观测重建，但不能证明潜在状态为真实生理实体；状态数、时间尺度、弱转移、非规则采样和高缺失均可能造成结构或参数不可辨识。
7. 在选定数据库中的外部验证只支持相应人群、时间、字段和医疗环境。区分度或校准良好不等于临床效用、真实世界效果或可部署性；额外地域数据规模较小或选择机制不同，也不能替代前瞻性影响研究。
8. EXIT-SEP 个体数据、逐时变量和交互功效未核实，且已有 SENECA 表型事后分析造成直接重叠风险；XBJ-SCAP 的疾病范围是重症社区获得性肺炎，不能与一般脓毒症队列直接等同。随机分配支持分配治疗的比较，但不自动识别中介网络。
9. 动物研究目前缺少具体机制、模型、平台、样本量、伦理和预算，人鼠炎症反应的可转化性证据存在冲突；动物结果不能作为电子病历预测模型的笼统外部验证。
10. 12–18 个月限制只适用于第二阶段。第一阶段约束表尚未作为项目材料提供，第三阶段没有时间和资源承诺；具体团队成员、职责、计算资源及最终论文是否整合多个阶段仍待确认。

### Risks, alternatives, and stop conditions

| 操作风险触发条件 | 响应或替代 | 后果与停止条件 |
|---|---|---|
| 第 1 个月末仍未取得计划开发库或外部库的合规访问 | 立即核验已列候选库中许可和字段满足要求的替代库，保留同一共同变量与外部验证原则 | 第 2 个月末仍不能确认两个合格数据库时，停止第二阶段执行并重定数据范围 |
| 第 2 个月共同字段审计显示核心状态域或事件时间戳不足 | 在查看模型结果前按专家预定优先级缩减变量域，或选择字段更合适的候选外部库 | 缩减后仍不能构成两个数据库的共同核心状态域时，停止跨库主分析 |
| 专家征询延迟或对关键状态、角色和允许转移持续分歧 | 增加一轮匿名理由反馈；把无共识关系改为不强制的敏感性项目，保留少数意见 | 协议冻结日仍无法形成最小约束表时，不开始主要模型拟合 |
| 数据抽取、单位转换或标签代码不能由第二名分析者复现 | 冻结开发，逐表核对字段血缘、队列计数和测试用例，修复后重新生成全部衍生数据 | 核心队列与标签无法独立复现时，不进入外部验证或论文结果阶段 |
| 多初值拟合和重复分割导致计算量超出既定资源 | 先减少并行候选状态数和重采样次数的探索部分，保留预定最终验证次数；增加批处理和检查点 | 资源仍不足以完成预定最终拟合与不确定性估计时，停止复杂模型结果解释 |
| 数据库版本或字段定义在分析期间更新 | 锁定已批准版本并记录版本差异；新版本仅作独立敏感性分析 | 无法取得锁定版本或重现原抽取时，暂停发布并重新完成数据审计 |
| 关键临床、数据、模型或统计负责人在连续两个里程碑缺席 | 重新分配书面职责并由替补负责人签署冻结决定；不由单一学科代替跨学科判断 | 无法补齐临床与方法双重负责人时，不冻结约束、阈值或主要结果 |

## References

1. Singer M, Deutschman CS, Seymour CW, et al. The Third International Consensus Definitions for Sepsis and Septic Shock (Sepsis-3). JAMA. 2016. https://pmc.ncbi.nlm.nih.gov/articles/PMC4968574/
2. Prescott HC, et al. Surviving Sepsis Campaign: International Guidelines for Management of Sepsis and Septic Shock 2026. Intensive Care Medicine. 2026. https://doi.org/10.1007/s00134-026-08361-1
3. Johnson AEW, et al. MIMIC-IV, version 3.1. PhysioNet. 2024. https://physionet.org/content/mimiciv/3.1/
4. Pollard TJ, et al. The eICU Collaborative Research Database, version 2.0. PhysioNet. 2018. https://physionet.org/content/eicu-crd/2.0/
5. Hyland SL, et al. HiRID, a high time-resolution ICU dataset, version 1.1.1. PhysioNet. 2020. https://www.physionet.org/content/hirid/1.1.1/
6. Thoral PJ, et al. AmsterdamUMCdb: An anonymised clinical database with 60,000 ICU admissions. 2021. https://github.com/AmsterdamUMC/AmsterdamUMCdb
7. SICdb. Salzburg Intensive Care Database, version 1.0.8. PhysioNet. https://www.physionet.org/content/sicdb/1.0.8/
8. Zigong Fourth People’s Hospital. ICU data of infection patients in Zigong Fourth People’s Hospital, version 1.1. PhysioNet; data description in Frontiers in Public Health. 2022. https://physionet.org/content/icu-infection-zigong-fourth/1.1/ ; https://pubmed.ncbi.nlm.nih.gov/35372245/
9. Sauer CM, et al. Systematic review and comparison of publicly available ICU data resources. Critical Care. 2022. https://pmc.ncbi.nlm.nih.gov/articles/PMC9150442/
10. Subtle variation in Sepsis-III definitions markedly influences predictive performance. 2024. https://pmc.ncbi.nlm.nih.gov/articles/PMC10803347/
11. Che Z, Purushotham S, Cho K, Sontag D, Liu Y. Recurrent neural networks for multivariate time series with missing values. Scientific Reports. 2018. https://pubmed.ncbi.nlm.nih.gov/29666385/
12. Informative missingness in ICU patient data: an observational study. Journal of Medical Internet Research. 2019. https://pubmed.ncbi.nlm.nih.gov/30622091/
13. Missing laboratory patterns across multiple hospitals. Journal of Biomedical Informatics. 2023. https://pmc.ncbi.nlm.nih.gov/articles/PMC10849195/
14. Seymour CW, et al. Derivation, validation, and potential treatment implications of novel clinical phenotypes for sepsis. JAMA. 2019. https://jamanetwork.com/journals/jama/fullarticle/2733996
15. Klouwenberg PMCK, et al. Independently validated multistate modeling of infection, sepsis, and subsequent clinical course. Critical Care. 2019. https://pmc.ncbi.nlm.nih.gov/articles/PMC6909511/
16. Xu Z, et al. SOFA trajectories and validation across three independent ICU cohorts. Critical Care. 2022. https://pmc.ncbi.nlm.nih.gov/articles/PMC9250715/
17. Externally validated prediction of sepsis deterioration trajectories across MIMIC and eICU. npj Digital Medicine. 2026. https://pmc.ncbi.nlm.nih.gov/articles/PMC13187286/
18. Raghu A, Komorowski M, Celi LA, Szolovits P, Ghassemi M. Continuous state-space models for optimal sepsis treatment. Proceedings of Machine Learning Research. 2017. https://proceedings.mlr.press/v68/raghu17a.html
19. Ghassemi M, et al. A switching state-space model of ICU interventions. KDD. 2017. https://pmc.ncbi.nlm.nih.gov/articles/PMC5543372/
20. De Blasi R, et al. Dynamic Bayesian network analysis of organ failure in intensive care. PLOS ONE. 2021. https://pmc.ncbi.nlm.nih.gov/articles/PMC8081190/
21. Lal A, et al. Development and verification of a digital twin patient model for critically ill patients with sepsis: a pilot study. Critical Care Explorations. 2020. https://pmc.ncbi.nlm.nih.gov/articles/PMC7671877/
22. Collins GS, et al. TRIPOD+AI statement: updated guidance for reporting clinical prediction models using regression or machine learning methods. BMJ. 2024. https://www.bmj.com/content/385/bmj-2023-078378
23. Moons KGM, et al. PROBAST+AI: updated tool for assessing risk of bias and applicability of prediction models. BMJ. 2025. https://www.bmj.com/content/388/bmj-2024-082505
24. External validation of artificial intelligence models in intensive care: systematic review and meta-analysis. BMC Medical Informatics and Decision Making. 2025. https://pmc.ncbi.nlm.nih.gov/articles/PMC11702098/
25. Wong A, et al. External validation of a widely implemented proprietary sepsis prediction model in hospitalized patients. JAMA Internal Medicine. 2021. https://jamanetwork.com/journals/jamainternalmedicine/fullarticle/2781307
26. Liu S, et al. Effect of an herbal-based injection on 28-day mortality in patients with sepsis: the EXIT-SEP randomized clinical trial. JAMA Internal Medicine. 2023. https://pmc.ncbi.nlm.nih.gov/articles/PMC10152378/
27. Song Y, et al. XueBiJing injection versus placebo for critically ill patients with severe community-acquired pneumonia. Critical Care Medicine. 2019. https://pmc.ncbi.nlm.nih.gov/articles/PMC6727951/
28. Post hoc analysis of EXIT-SEP by SENECA clinical phenotype. 2025. https://pmc.ncbi.nlm.nih.gov/articles/PMC12257024/
29. Lee H, et al. AGReMA statement for reporting mediation analyses of randomized trials and observational studies. JAMA. 2021. https://jamanetwork.com/journals/jama/fullarticle/2784353
30. CONSORT 2025 explanation and elaboration: subgroup analyses and interpretation. 2025. https://pmc.ncbi.nlm.nih.gov/articles/PMC11995452/
31. Daniel RM, Cousens SN, De Stavola BL, Kenward MG, Sterne JAC. Methods for dealing with time-dependent confounding. BMJ. 2017. https://www.bmj.com/content/359/bmj.j4587
32. Osuchowski MF, et al. Minimum Quality Threshold in Pre-Clinical Sepsis Studies (MQTiPSS). Shock. 2019. https://pmc.ncbi.nlm.nih.gov/articles/PMC6093828/
33. Percie du Sert N, et al. The ARRIVE guidelines 2.0. PLOS Biology. 2020. https://journals.plos.org/plosbiology/article?id=10.1371/journal.pbio.3000410
34. Seok J, et al. Genomic responses in mouse models poorly mimic human inflammatory diseases. Proceedings of the National Academy of Sciences. 2013. https://pmc.ncbi.nlm.nih.gov/articles/PMC3587220/
35. Takao K, Miyakawa T. Genomic responses in mouse models greatly mimic human inflammatory diseases. Proceedings of the National Academy of Sciences. 2015. https://pmc.ncbi.nlm.nih.gov/articles/PMC4313832/
