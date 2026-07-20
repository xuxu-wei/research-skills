---
schema_version: research-idea.v3
plugin_version: 0.9.0-preview.3
artifact_id: idea-dossier-I01-001-v025
workflow_id: RID-SEPSIS-CSM-20260717-001
idea_id: I01-001
version_id: v025
path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/accepted/idea-dossier-v025.md
parent_idea_ids: []
based_on:
  - artifact_id: idea-dossier-I01-001-v003
    version: v003
    path: tests/idea-test-0.9.0-preview.1/0.9.0-preview.1/03_ideas/nodes/I01-001/dossiers/idea-dossier-v003.md
source_skill: multi-path-idea-generator
created_round: 1
change_type: editorial_repair
identity_anchor:
  primary_research_question: "can a knowledge-constrained, uncertainty-aware dynamic system representation of ICU patients cover the sepsis-centered pre-onset, onset, post-onset, and outcome continuum, demonstrate cross-database state/structure validity, and then test limited randomized intervention perturbations without conflating prediction with causality?"
  primary_objective: "construct and validate the sepsis complex-system model, with stage II completed within 24 months."
  study_object: "the longitudinal sepsis-centered ICU patient system, including comparable at-risk non-onset intervals and post-onset trajectories."
  core_data_or_evidence_base: "literature/expert priors; longitudinal public ICU data; conditionally available EXIT-SEP and XBJ-SCAP individual-level RCT data."
  primary_unit_of_inference: "patient-time state and state transition, with patient and hospital clustering respected."
identity_status: preserved
frozen: false
---

# 脓毒症全病程候选动态系统模型的构建与跨数据库验证，以及预设条件满足后使用随机试验稀疏访视数据开展的次要分析

## Title, summary, audience, and positioning

- **Title:** 脓毒症全病程候选动态系统模型的构建与跨数据库验证，以及预设条件满足后使用随机试验稀疏访视数据开展的次要分析
- **One-sentence complete-Idea summary:** 本研究拟在 24 个月内结合文献与专家知识以及两个公共 ICU 数据库，构建并跨数据库验证一个覆盖脓毒症尚未发生、首次发病、发病后状态演化至恢复、持续恶化、器官衰竭、出 ICU 或死亡的知识约束且能表达不确定性的候选动态复杂系统模型；只有在该模型的公共数据验证成功且试验实际访视数据满足预设分析条件后，才开展基于随机对照试验稀疏访视数据的分试验次要分析，作为不补足前述验证的后续扩展。
- **Primary audience:** 重症医学、临床流行病学、纵向统计、系统辨识、系统科学、医学 AI 与转化研究的跨学科研究者；当前不预设具体期刊。
- **Positioning and contribution frame:** 研究以脓毒症复杂系统模型的构建与验证为核心，预期贡献是把全病程状态定义、知识约束的系统辨识、预先规定的模拟恢复标准和严格隔离的跨数据库验证连接成可复核的证据路径，并形成面向高水平论文的验证结果、可复用基准数据与分析资源，而非仅产出预测工具；后续试验次要分析只在预设条件满足时提供有限的随机化证据扩展。

## Structured abstract

- **Background and gap:** 脓毒症发病标签受疑似感染配对、基线 SOFA、观察窗和信息可用时间影响，而公共 ICU 数据库在中心、年代、采样和接口方面并不等价；现有研究分别覆盖多状态病程、动态表型、干预条件转移、跨数据库验证和随机试验二次分析，但尚缺少经有界检索确认的、把发病前至结局的统一系统表征与严格跨数据库验证连接起来的代表性证据路径，这使跨数据库可解释性、可重复性和后续转化判断仍不充分。[1-3,5-16,26-38]
- **Objective and hypothesis:** 目标是在 24 个月内完成公共 ICU 数据阶段，构建并检验一个以患者—时间状态及状态转移为推断单位、受知识约束且表达不确定性的候选动态系统模型；可证伪假设是，至多一个复杂候选在满足数据支持、锚定和模拟恢复标准后，能在时间外、医院外以及未参与模型开发或参数调整的另一数据库测试集中保持预设的概率校准、状态对齐和候选结构稳定性。
- **Approach:** 研究先用文献与专家知识提出包含反馈、时滞、非线性、未测因素和观测过程的候选结构，再由两个公共 ICU 数据库确定共同变量、时间尺度和可支持复杂度；竞争风险、多状态和线性状态空间模型先于复杂候选实施，随后评价首次发病风险、发病后状态占用、模拟恢复以及不更新模型参数的外部验证，并把目标数据库预留适配集上的重新校准或观测模型更新与主要外部验证分开报告；只有公共数据阶段成功且试验授权、语义、实际访视指标及预定映射均获得支持后，才对两项试验分别开展次要分析。[17,18,21-25]
- **Expected result:** 计划产物包括可执行的标签与双时钟协议、双数据库变量和样本支持记录、互斥病程状态、模拟恢复与不确定性结果、两项主要任务和两项次要表示诊断、独立外部测试结果及失败模式图；满足预设条件时，另报告由随机试验实际访视指标计算的低维状态摘要，或使用与公共数据模型独立的临床状态结局进行试验次要分析，所有这些均为拟生成产物而非现有结果。
- **Contribution and impact:** 该研究将为脓毒症复杂系统模型提供从构建、系统辨识到跨数据库验证的连续证据，并明确区分模型在不更新参数时的外部表现、有限适配后的表现和目标数据库内重新开发；成功实施可形成整合、验证与基准资源价值，并为是否值得开展后续试验扰动研究提供更可靠依据。

## Background, current state, gap, significance, and rationale

### Background

脓毒症随时间形成，并与治疗和检测行为共同演化。Sepsis-3 将其定义为感染所致失调宿主反应引起的危及生命器官功能障碍，研究中常以相对基线 SOFA 增加至少 2 分操作化，但这一标准并不产生唯一的电子健康记录发病时刻。[1,2] 疑似感染配对、SOFA 基线和观察窗的合理变化会改变病例识别与预测表现，因此本研究区分临床事件时刻与标签在数据库中可计算的时刻，并在重复设定的动态预测时点（landmark）只使用当时已经可获得的信息。[3]

### Current state

MIMIC-IV、eICU-CRD、HiRID 和 AmsterdamUMCdb 提供纵向生命体征、实验室、治疗与结局数据，但中心、年代、采样和接口不等价；BlendedICU 与 ricu 也表明跨数据库统一只能建立在语义、单位和时间均可核验的共同概念上。[5-10] 与本研究最接近的既有研究已经分别描述日级多状态转移、SOFA 或生命体征轨迹、动态表型、隐马尔可夫模型、器官交互图、观察性治疗条件转移、状态空间模型、数字孪生原型、模型预测控制、离线强化学习、跨数据库验证及随机试验中的表型—治疗二次分析，因此各单项模块本身并非新颖。[26-37]

### Gap

现有证据仍不能回答：一个以脓毒症为中心的候选复杂系统模型，能否在同一研究边界内连接尚未发病的在险时段、首次发病、发病后互斥状态与结局，能否在显式区分患者状态、治疗行动和观测过程后恢复可解释的不变量，以及这些状态和结构能否在未参与开发的另一公共 ICU 数据库中保持预先规定的有效性。截至 2026-07-17 的有界代表性检索只以低至中等置信度未发现同时贯通这些证据层的已发表代表性架构，这一判断不是系统综述结论。[26-38]

### Significance

回答这一缺口可把脓毒症研究从单一时间点风险或已发病预后推进到可检验的全过程系统表征，并让研究者区分模型在开发数据中表现良好、在另一数据库中保持稳定以及经有限适配后恢复性能这三类不同证据。由此获得的标签、状态定义、模拟恢复结果和跨数据库失败模式可提高研究的可重复性与可证伪性，帮助跨学科团队判断哪些结构值得进入后续试验研究，也能在复杂模型未获支持时留下有用的基准资源。

### Rationale

双时钟与重复动态预测时点直接处理电子健康记录发病时刻和信息可用时刻不一致的问题；把生理状态、治疗行动、测量过程与结局标签分开，可以避免把照护和检测行为误作自然病程信号；用正确、零边、过拟合和错设数据生成情景检验绝对恢复，可筛除只在预测分数上占优却不能稳定恢复预设结构的候选；按医院预先划分且不参与模型开发或参数调整的外部测试集，可检验模型在另一数据库中的状态和结构稳定性；在公共数据验证完成后，再按预先确定规则把阶段 II 模型映射到随机试验实际访视指标并由这些指标计算低维状态摘要，使随机化信息只回答试验数据实际支持的问题。[14-18,21-25]

## Research question, objectives, and core hypothesis

### Primary research question

能否构建并验证一个知识约束、能够表达不确定性的 ICU 患者候选动态复杂系统模型，使其覆盖以脓毒症为中心的发病前、首次发病、发病后状态演化和结局连续体，在医院与数据库之间保持可量化的状态和候选结构有效性，并在公共数据验证成功且试验实际访视数据支持预定分析时，分别评价随机分配对由这些访视指标计算的低维状态摘要的影响？

### Objectives

1. **界定全病程与信息时钟：** 预先规定可实时实施的主 Sepsis-3 标签、标签可用性时钟、landmark 风险集、互斥发病后状态和竞争事件，并用两种合理标签开展敏感性分析。
2. **构建可辨识的候选状态模型：** 由双数据库可观测性与样本支持核验确定共同模块、时间方案和复杂度上限，显式分离生理状态、治疗行动和观测过程，只解释在允许重参数化下保持不变的量。
3. **检验恢复能力和跨数据库有效性：** 用正确、零边、过拟合和错设生成情景评价绝对恢复与错误结构置信度，在第二数据库分开预留适配集和最终测试集，检验两项主要临床任务与两项次要表示诊断。
4. **开展条件性试验次要分析：** 公共数据验证和试验语义均满足预设条件后，为每项试验分别检验从阶段 II 模型到实际访视指标的预定映射；达到一致性和误差标准时分析由访视指标计算的低维状态摘要，否则改用试验特异的独立次要临床状态分析。

### Core hypothesis and non-hypotheses

核心假设是：若共同锚点与事件支持充分，锚定、尺度、状态数和滞后已经预先确定，且复杂候选达到绝对恢复和错误结构控制标准，则部分状态占用、转移概率、锚点预测以及预设依赖的符号和滞后可在独立外部数据库中维持预定义稳定性。研究的估计目标是观察到的照护和测量政策下的预测与生成表征，而不是治疗因果模型；后续试验分析是单独的条件性目标，不构成公共数据阶段成功定义的一部分。

## Research content and work packages

### Twenty-four-month minimum and dated decisions

阶段 I–II 构成 24 个月最低交付，阶段 III 位于其后。下表中的负责人签署表示计划所需的职责确认，不表示当前已有具名人员承诺；最终外部测试结果在月 18–20 的开发方案确定前由独立数据保管人保持不可访问。

| Time | Required deliverable | Predefined decision and consequence |
|---|---|---|
| 月 0–3 | 确认 MIMIC-IV v3.1 与 eICU-CRD v2.0 的团队访问、DUA、存储和算力；具名临床、统计、系统辨识和数据工程角色；预先指定 HiRID 或 AmsterdamUMCdb 之一为备份 | 任一主数据库无法承担预定角色时启用备份；月 3 仍无两个可访问数据库则终止 24 个月跨数据库系统表征路线并记录数据访问不足 |
| 月 4–6 | 完成双数据库队列流、事件和转移、医院、跨院患者、锚点密度、接口及缺失核验；确定主标签、时钟、多状态、医院优先拆分、时间方案、共同模块和参数上限 | 以“双数据库可观测性与样本支持核验（G1）”结果判定；12 小时方案不受支持时，在模型拟合前改用 24 小时或事件时间；跨院排除破坏外部支持时启用备份或缩小研究范围，最终测试结果仍不可见 |
| 月 7–12 | 完成竞争风险、多状态和线性状态空间基线；Monte Carlo 与半合成恢复实验；评价至多一个复杂切换或非线性候选 | 任一关键恢复、零边错误结构或错设识别标准未满足时，停止扩展复杂候选并改用相应简单模型；预测分数不改变该判定 |
| 月 13–18/20 | 完成开发数据库内部、时间外和医院外验证；记录标签、锚点、预处理、模型、超参数、更新层级、指标及外部判定标准 | 严重泄漏未消除或主要任务概率校准与评分未达标准时不访问最终外部测试；月 20 后不依据测试结果修改方案 |
| 月 21–24 | 在第二数据库最终测试集中报告不更新模型参数的结果，并分开报告仅重新校准和仅更新观测模型的结果；记录聚类不确定性、状态对齐和失败模式 | 按合取定义判定阶段 II；未满足时仍形成基准数据与分析资源，但不认定跨数据库系统表征验证成功 |
| 24 月后 | 在阶段 II 成功并核验个体数据授权、原始 CRF/SAP 和试验语义后，为每项试验分别评价预定访视映射及相应分析 | 映射达到预设一致性和误差标准时分析低维访视状态摘要；不满足时改用独立 SOFA 临床状态；核心试验语义不足时不开展新状态结局分析 |

### Conjunctive minimum success definition

阶段 II 的“跨数据库候选系统表征验证成功”必须同时满足：

1. 两个数据库均可构造主发病前风险集和发病后状态队列，并达到预先记录的事件、转移、医院和共同锚点支持下限；
2. 复杂候选（若实施）在正确生成器、零边生成器和核心错设情景中达到全部绝对标准；若改用线性或多状态表示，只能报告该表示获得支持；
3. 两个主要任务在开发与时间外验证中，Brier 或多类别 Brier 相对最强简单基线的差值上侧 95% 界不超过 +0.01，校准斜率为 0.80–1.20，校准截距对应绝对风险误差不超过 0.02；Brier 属于 proper scoring rule，即如实报告预测概率时可使期望评分最优的评分规则；
4. 无未解决的高严重度泄漏，所有特征遵循标签可用时间和 as-of 时钟，患者、医院、重复住院与插补均不跨数据划分；
5. 医院优先的外部划分后仍有至少 20 个合格测试医院并满足 G1 的事件和转移支持，在不更新模型参数的外部测试中两项主要任务达到 Brier 非劣标准，对齐后主要状态相关或一致性系数至少 0.70，预设结构符号一致率至少 0.80；预留适配集上的有限更新结果单独报告。

依赖 G1 的阈值只能在月 6 前依据临床容许误差、开发数据库 bootstrap 和未接触外部结果的先导模拟写入注册记录；本 dossier 已列出的数值标准只能收紧，不能放宽。阶段 III 不计入上述成功定义。

### Work packages and minimum route

| Work package | Months | Main work | Output tied to the decision sequence |
|---|---:|---|---|
| WP1：标签、队列和样本支持 | 0–6 | 访问与版本、样本流、双时钟、变量角色、跨院患者、时间网格和接口核验 | 可执行风险集、多状态、医院优先划分和共同模块，或预设的备份与范围调整 |
| WP2：知识结构、基线和绝对恢复 | 3–12 | 候选图、锚定限制、竞争风险、多状态、线性基线及 Monte Carlo/半合成实验 | 至多一个复杂候选或获得支持的简单模型 |
| WP3：主要任务和次要诊断 | 8–18 | 未来 12 小时首次发病累积发生风险、第 7 日状态占用、伪遮蔽重建、未来轨迹诊断、MNAR、重叠和消融 | 概率评分、校准、覆盖、泄漏和弃权记录 |
| WP4：隔离的跨数据库验证 | 14–24 | 确定开发方案；按医院划分适配集与测试集；排除跨划分患者；依次评价不更新参数、重新校准和更新观测模型 | 独立外部结果、排除记录和失败模式图 |
| WP5：条件性阶段 III | 24 月后 | 核验试验语义；评价阶段 II 到实际访视指标的预定映射；实施低维摘要或独立 SOFA 临床状态分析 | 两项试验分开报告的次要分析 |

最低实施顺序为：资源与样本支持核验 → 标签、状态和医院划分确定 → 竞争风险与多状态基线 → 线性状态空间模型 → 绝对模拟恢复 → 至多一个复杂候选 → 两项主要任务与两项次要诊断 → 完成开发方案 → 独立外部测试 → 条件性试验数据核验与分析。

## Data, materials, and existing evidence base

### Current evidence and prospective requirements

| Resource or result | Current evidence | Status | Prospective requirement |
|---|---|---|---|
| MIMIC-IV v3.1 与 eICU-CRD v2.0 的公开存在、版本和文献 | PhysioNet 与原始数据库论文提供稳定 DOI 和版本记录。[5,6] | **verified** | 仅确认数据库存在；团队访问和项目队列可执行性另行核验 |
| 团队访问凭证、DUA、下载与存储、确切提取版本 | 当前材料未提供已完成凭证或提取证据 | **unverified** | 月 3 前确认；两个数据库不能承担预定角色时终止跨数据库路线 |
| 双数据库实际样本、事件、转移、医院、跨院患者、锚点密度和接口支持 | 尚未执行 G1，官方规模不能替代项目计数 | **not generated** | 月 6 前记录；不达标准时减少维度、改变时间网格、启用备份或停止相应端点 |
| EXIT-SEP 与 XBJ-SCAP 本地验证报告 | 两份 2026-07-12/13 报告记录工作簿构建、关键非缺失和复现/QC；不是独立同行评审或原始数据核验。[22,24] | **project-local derivative** | 仅支持稀疏访视和字段缺口描述，不能替代个体数据授权、CRF/SAP 或数据持有人确认 |
| 试验个体数据授权、原始 CRF/SAP、随机化、中心、试验规定访视相对随机化或首剂的时间、生存与去向语义 | 现有衍生报告没有完成这些原始语义核验 | **unverified** | 影响估计对象的核心语义无法核验时不开展新状态结局分析，不推测字段 |
| 阶段 II 与两项试验的共同生理锚点、单位和实际访视映射 | WBC、CRP 等候选访视信息见衍生材料，但是否属于阶段 II 锚点及跨数据源语义和单位是否一致尚未证明；D-dimer 单位仍有缺口 | **unverified** | 每项试验至少两个合格共同锚点，否则改用独立 SOFA 临床状态分析 |
| 所需团队角色 | 临床与表型、纵向统计、系统辨识、数据工程、模型实现和独立数据保管职责已定义 | **verified** | 这是角色规范，不是人员承诺 |
| 已承诺或具名的人员及可用工时 | 无可核验名单或承诺记录 | **unverified** | 月 3 前具名；关键角色缺失时不得确认 G1、阈值或开发方案 |
| 当前候选模型、模拟、恢复、预测、外部测试或试验新分析结果 | 当前项目材料未提供已生成结果 | **not generated** | 按时间计划生成，任何拟开展工作不写成已完成结果 |
| 截至 2026-07-17 的代表性相关研究检索 | 项目内有界检索综合了代表性论文、预印本、注册记录及稳定标识符 | **project-local derivative** | 各模块已有先例为高置信判断；完整组合缺口为低至中等置信判断 |

### Public ICU database roles and G1 support assessment

- **开发数据库：** MIMIC-IV v3.1，计划用于标签与模型开发、内部和时间外验证；需要确认访问、DUA 和确切表版本。[5]
- **外部数据库：** eICU-CRD v2.0，计划用于医院级预留适配集和独立最终测试集；整院接口缺失按医院核验。[6]
- **备份数据库：** HiRID 或 AmsterdamUMCdb 只能在月 0–3 预先指定并完成同等核验后替代失败角色，不能依据最终测试结果选择。[7,8]
- **共同概念：** 只保留单位、语义、时间和可见性均可核验的共同变量；数据库特异信息仅用于探索性观测模型。[9,10]

下表数值由数据工程角色生成、临床与统计角色核验，并在月 6 前记录；“待 G1”表示尚无结果。

| Assessment field | MIMIC-IV development | eICU external | Predefined use rule |
|---|---|---|---|
| Access/DUA, release and extract record | 待 G1 | 待 G1 | 未完成者不承担确认性角色 |
| Adult patients, hospitalizations, ICU stays and repeat/linkable stays | 待 G1 | 待 G1 | 主分析每次住院只用首个合格 stay；可链接重复住院保留患者首次合格住院 |
| Hospitals and patients per hospital | 待 G1 | 待 G1 | 外部测试至少 20 个有事件支持的医院 |
| 12-hour landmarks and first-onset events | 待 G1 | 待 G1 | 每个自由风险参数在开发和外部数据中至少有 20/10 个事件 |
| Alive discharge, death, transfer/loss and administrative end | 待 G1 | 待 G1 | 分开计数；稀少类可合并为其他终止，但不作普通独立删失 |
| Incident/delayed-entry population and allowed transitions | 待 G1 | 待 G1 | 每个自由转移参数在开发和外部数据中至少有 20/10 次转移 |
| Timestamp precision and follow-up | 待 G1 | 待 G1 | 不能支持 12 小时排序时在拟合前统一改用 24 小时，仍不足时改用事件时间 |
| Anchor unit, source table and result availability | 每锚点待填 | 每锚点待填 | 单位或可用时间不清者不进入共同层 |
| Anchor density by time interval/state | 每锚点待填 | 每锚点待填 | 每共同维度至少两个锚点；每锚点在各数据库至少 30% 合格时段实测，不用延续填充值达标 |
| Hospital interface and patient coverage | 每锚点待填 | 每锚点待填 | 锚点存在于至少 70% 合格医院并覆盖 80% 合格患者 |
| Missingness, observation gap and cross-hospital links | 每锚点/患者待填 | 每锚点/患者待填 | 保留缺失指示、实测时刻和间隔；不作无条件末次观测延续；按预定规则处理跨划分患者 |
| Effective support and complexity cap | 待计算 | 待计算 | K=min(通过标准的模块数,4)，regime≤3；事件与参数比不足时继续降维 |

主时间方案为 12 小时，24 小时和事件时间为预写替代方案；方案改变只能由模型拟合和最终测试访问前的样本支持结果触发。除具有明确起止时间的输注或器官支持状态和静态基线外，不作无条件末次观测延续；每个动态值记录是否实测、实测时刻及距上次实测时间。

### Predefined variable-use roles

| Primary role | Examples and allowed use | Separation rule |
|---|---|---|
| Physiological measurement Y_t | 实测生命体征、血气与实验室、器官功能测量；G1 后保留的锚点 | 不包含治疗启停、剂量或测量频率；同源 SOFA 标签副本仅进入标签流程 |
| Treatment/action A_t | 抗菌药、液体、血管活性药、机械通气、CRRT、激素的启动、停止和剂量 | 不作为潜在生理锚点；用于恶化标签时生成带事件时刻的独立副本 |
| Measurement process M_t | 是否检测、次数、间隔、医嘱、采样、结果可用时刻及医院接口 | 未检测不编码为正常，接口缺失不编码为患者状态 |
| Label-only | 疑似感染配对、独立 SOFA 事件、互斥状态、死亡、出院和转院 | 不进入相同或更早 landmark；抗菌药双用遵循可用时间并与行动通道分离 |
| Baseline covariate B | 年龄、性别、入院类型和来源、既往病史等 landmark 前固定信息 | 不随时间复制为伪测量，未知值显式编码 |

### Local RCT evidence and present status

EXIT-SEP 在中国 45 个 ICU 随机分配 1,817 例 Sepsis-3 患者；本地衍生报告记录 1,760 例 28 日状态明确、395 例死亡、57 例状态未知，试验规定的 D1、D4 和 D7 访视中 SOFA 非缺失例数为 1,750、1,542 和 1,296，乳酸非缺失例数由 D1 的 855 降至 D7 的 223。[17,21-23] 这些数字描述衍生清洗层的访视稀疏性；D1 与 D7 相对随机化或首剂的具体时间、中心及生存和去向语义仍待原始 CRF/SAP 核验。

XBJ-SCAP 随机分配 710 例重症社区获得性肺炎患者；本地衍生报告记录全分析集 675 例、符合方案集 617 例、全分析集且基线 SOFA≥2 的操作性 sepsis-like 人群 671 例、严格重叠人群 658 例；试验规定的 D0、D4 和 D8 访视中 SOFA 非缺失例数为 703、628 和 610，WBC 为 704、634 和 614，CRP 为 579、503 和 467，28 日状态为 675 例。[18,24,25] SCAP 入组不等同于确认 Sepsis-3；PaO2/FiO2、乳酸、休克、CRRT 和 CNS 等患者级变量不可用，D-dimer 单位尚待核验。

## Research design and methods

### Protocol specifications for the two primary clinical tasks

| Item | Primary pre-onset task | Primary post-onset task |
|---|---|---|
| Population | ≥18 岁；每次住院首个合格 ICU stay；至少 12 小时可见历史；landmark 尚未达到主标签；观察起点已发病者排除 | 首次 incident onset；入 ICU 已发病者仅在首个可核验时点 delayed entry，分层并左截断 |
| Event clock | 主疑似感染使用微生物标本采集与系统抗菌药首次实际给药：采集在先则给药须在其后 72 小时内，给药在先则采集须在其后 24 小时内，感染时刻取两者较早者；无已记录慢性器官功能障碍者 baseline SOFA=0，有记录者取入 ICU 前 24 小时最低可计算 SOFA，不可核验者不进入主风险集；各成分在滚动 24 小时取最差值，SOFA 相对 baseline +2 必须位于感染前 48 小时至后 24 小时，onset 为首个可排序的满足时刻。[1,2] | incident 以主 onset event time 为零点；发病后状态按临床 event time 进入 |
| Availability clock | 配对较晚事件及必要 SOFA 数据在源系统中可见或最终确定时刻取最大值，之后出现的信息不回填 event time | 恢复要求连续 24 小时，availability 为时间窗结束；恶化、死亡、出院和转院使用记录可用时刻，只使用当时可见标签 |
| Landmark/history/horizon | ICU 第 12 小时起每 12 小时设定；此前最多 24 小时且至少 12 小时的 as-of 历史；预测未来 12 小时首次 onset | onset 或 delayed-entry 后每 12 小时设定；主 horizon 为病程第 7 日，第 14 日作为敏感性分析 |
| First onset/repeats | 只分析首次 onset；保留重叠 landmark，但一次住院的总权重为 1，并按患者和医院聚类 | incident 与 delayed-entry 分层；delayed-entry 不反推 onset |
| Competing/intercurrent | onset 前活着出 ICU、院内死亡和转院或失访为互斥终止；行政结束作独立删失并开展 IPCW 与界限检查 | 死亡、活着出 ICU 和转院为终止状态；恢复不由出院替代；开展 IPCW 敏感性分析 |
| Within-bin order | landmark t 的特征仅允许 availability<t；[t,t+12h) 内的新行动为 A_t，下一边界实测生理为 next-state；无法区分先后的同时间戳边不纳入分析 | 同一规则；器官支持属于行动，独立事件标签只在形成后定义恶化 |
| Estimand/model | 给定历史的未来 12 小时首次 onset 累积发生风险；离散 multinomial cause-specific hazard 转换为累积发生风险 | 第 7 日“生理恢复或活着出 ICU”有利状态集合的占用概率，两者另行报告；采用互斥离散多状态模型与 Aalen–Johansen 估计 |
| Metric | 12 小时 Brier、绝对校准截距和斜率；AUPRC、提前量和假警报为次要指标 | 第 7 日多类别 Brier 与有利状态绝对校准；各状态和转移校准为次要指标 |
| Uncertainty | 患者总权重；患者层与医院层 bootstrap 95% 区间 | 患者层与医院层 bootstrap；incident 与 delayed-entry 分层并报告有效转移数 |
| Decision standard | 开发与独立外部测试均要求 Brier 非劣界 +0.01、校准斜率 0.80–1.20、绝对风险误差≤0.02，且不存在高严重度泄漏 | 使用相同标准；表示诊断和试验分析不计入主要任务判定 |

主标签之外仅使用两种敏感性定义：把培养与抗菌药配对改为对称 ±24 小时；对所有人使用感染前 24 小时最低可计算 SOFA，并把器官功能时间窗限制为前后各 24 小时。敏感性结果不替换主结果。泄漏检查覆盖 onset 后生理与治疗、尚不可用的培养或抗菌药、同一时间段行动、未来测量频率、跨划分插补与标准化、患者或 stay 跨集合、重叠窗口权重以及由结局驱动的变量、时间网格或阈值。

### Mutually exclusive post-onset state/event system

每 12 小时赋值一次，优先级为死亡 > 转院或无法继续观察 > 活着出 ICU > 恶化或新器官衰竭 > 生理恢复 > 持续脓毒症。源事件无法排序时使用较高优先级，并开展事件时间敏感性分析。

| State/event | Operational definition and availability | Variable-use rule |
|---|---|---|
| 持续脓毒症 | ICU 内存活且未满足其他状态；transient | 独立标签，不作锚点 |
| 生理恢复 | 相对 onset 参考 SOFA 下降≥2 且连续 24 小时无新恶化；event 为时间窗起点，availability 为时间窗结束；可复发 | SOFA 只用于标签；无支持升级仅为标签条件，行动仍保留在 A_t |
| 恶化或新器官衰竭 | 相对此前 24 小时最低 SOFA +2，或新启或升级血管活性药、有创通气或 CRRT；同时发生只记一次 | 生理与行动派生标签使用独立副本；行动不作锚点 |
| 活着出 ICU | 存活离开 ICU；分析中 absorbing | 与生理恢复分开，另行报告去向 |
| 转院或无法继续观察 | 转往不可追踪 ICU 或医院，或记录终止；terminal competing | 不编码为恢复，使用 IPCW 与界限分析 |
| 死亡 | ICU 内或可追踪病程死亡；absorbing | 不作 MAR 缺失，同时间戳时优先 |

### Observational target, anchoring and abstention

令锚定潜在患者状态为 X_t，生理测量为 Y_t，行动为 A_t，测量指示或强度为 M_t，基线为 B，数据库或医院为 S。主要目标是在实际照护与测量政策下估计联合预测或生成分布 p(X_0:T,Y_0:T,M_0:T,A_0:T | B,S)，以及由其导出的风险、对齐状态占用与转移、锚点预测和预设符号或滞后不变量。治疗变量在此目标中作为观察到的行动通道，而不是干预效应的估计对象。

每个维度至少有两个跨数据库锚点；第一个锚点的 loading 固定为 +1 并标准化尺度；非指定 cross-loading 为 0 或采用预写稀疏模式；K≤4、regime≤3，滞后仅为 1 或 2 个预定时间间隔；允许图不含同一时间间隔的瞬时循环；20 个固定随机种子后实施 permutation/sign alignment。解释对象限于对齐后的状态占用、转移概率、锚点层预测以及预设边的符号和滞后。

MNAR 主拟合使用显式测量过程的 MAR/selection 基线，并对未测生理值实施 pattern-mixture delta −1、−0.5、0、+0.5、+1 个开发数据库标准差及 selection tipping-point 分析。每个对齐状态、医院和时间层报告行动概率与有效样本量（ESS）；行动比例<5%或>95%，或加权 ESS<20% 名义样本时，将相关关系标记为低支持和 policy-specific。任一状态或边在模拟恢复、20 个随机种子对齐、bootstrap 保留、外部符号一致、状态对齐或区间校准方面未达到预设数值时，删除、合并或标记为数据库或照护政策特异。

### Absolute simulation and semi-synthetic recovery assessment

月 7–10 在不读取最终临床外部测试结果的条件下，每个核心情景至少重复 1,000 次，或重复至关键比例的 Monte Carlo SE≤0.02。数据生成器包括正确指定、零边或独立状态、多余状态或过拟合、遗漏状态、错误滞后或观测模型，并交叉改变状态分离、切换率、1/2 个时间间隔滞后、政策反馈、隐藏混杂、MNAR、标签误差、访视密度、整院接口缺失及数据库差异。

| Recovery quantity | Predefined absolute standard | Response when not met |
|---|---|---|
| 状态恢复 | 离散 ARI 或连续主要 canonical correlation≥0.80；20 个随机种子对齐≥90% | 合并或删除状态，或改用线性或多状态模型 |
| 转移概率 | 主要允许转移 MAE≤0.05；95% coverage 0.90–0.98 | 删除该转移或停止结构解释 |
| 预设符号或滞后 | 正确恢复率≥0.80 | 该边不进入共同结构 |
| 边检测 | sensitivity≥0.80 且 FDR≤0.10 | 降低稀疏度或维度；仍未达到时只保留预测任务 |
| 零边错误结构 | 任一假边 95% 区间排除 0 的重复比例≤0.05 | 不再使用复杂候选，不按结果调整标准后重新纳入 |
| 错设识别与弃权 | ≥80% 重复识别失配或触发弃权；错误结构高置信≤0.05 | 不再使用该候选，或只保留已恢复的不变量 |
| 概率校准 | 斜率 0.80–1.20；绝对概率偏差≤0.02 | 重新校准只处理概率偏差，不改变结构恢复判定 |

### Hospital-primary cross-database validation

在任何结局导向选择之前，先按合格体量四分位和接口完整性分层，以固定种子 20260717 的预先编程确定性算法将 eICU 医院分为 30% 预留适配集和 70% 最终测试集。医院划分优先于患者规则，测试医院不因患者链接进入适配集。医院分配表与患者链接算法版本在查看测试结局前记录。

主要外部分析按以下规则实施：

1. 先完成医院分配，再只用患者链接键识别跨院记录；一个可链接患者的记录若跨越适配集与测试集，该患者全部记录从主要外部分析排除，不按患者重新分配。
2. 对只出现在同一划分内的患者，仅保留预先定义的首次合格住院及其首个合格 ICU stay，确保同一患者不跨集合。
3. 在查看测试性能前报告跨划分排除人数、占原合格患者比例、涉及医院数，以及仅使用结局前信息得到的年龄、性别、入院类型与来源、首个 landmark 生理负担和观察密度；排除规则不使用结局或模型误差。
4. 预写敏感性分析采用 test-dominant patient–hospital component 规则：医院角色确定后建立患者—医院二部图；纯适配或纯测试组件保留原角色；混合组件从适配集删除相关患者全部记录，只保留其预分配测试医院中的首次合格 stay 进入测试集。
5. 独立数据保管人在不释放模型性能的情况下检查支持。主要排除或敏感性分析后，若测试集少于 20 个合格医院、任一自由风险或转移参数低于外部 10 个事件或转移、共同锚点不再覆盖至少 70% 合格医院和 80% 患者，或跨划分排除超过原合格测试患者或主要事件的 10%，则启用预先指定的备份数据库；备份仍不足时只报告数据库层结果。

在标签、共同变量处理、状态、预处理、信息可用时间、模型、超参数、判定标准和评价代码确定后，最终测试依次实施：不更新模型参数的外部验证（zero-update validation）；仅使用预留适配集重新校准特定预测时间的截距和斜率；仅使用预留适配集更新观测模型，同时保持状态和转移参数不变。在目标数据库上完整重新拟合或重新开发模型单独标记，不属于外部验证。测试集不用于选择变量、时间方案、状态数、锚点、划分、更新层级或数值标准。

### Conditional mapping to RCT visit measurements and independent clinical-state analysis

两项新状态结局均为原试验结果公布后提出的次要或探索性再分析，原 28 日结局复现单独报告，两项试验分别分析。每项试验的指标映射、数值标准、代码和随机种子在治疗组比较前确定。

**试验语义与共同锚点资格。** 阶段 II 必须先完成；需要获得个体数据分析授权，并由原始 CRF、SAP、数据字典或数据持有人确认核验随机化和分析集、中心或分层因素、EXIT-SEP 规定的 D7 访视与 XBJ-SCAP 规定的 D8 访视相对随机化和首剂的实际时间窗，以及死亡、住院、活着出院和转院语义。试验 r 的候选共同变量集 C_r 只包含同时满足以下条件的变量：在阶段 II G1 中保留的 Y_t 生理锚点；在该试验实际 D7 或 D8 访视中直接测得；临床构念、标本和单位一致或有预先验证的确定性单位转换；采样与结果可用时刻落入预定访视窗；不属于治疗、测量频率、SOFA 或结局标签，也不是事后派生状态。每项试验至少需要两个锚点，且每个锚点在阶段 II 与试验中均通过范围、时间及测量语义核验。WBC 和 CRP 只是当前衍生报告提示的候选；单位不明的 D-dimer 和不存在的字段不进入该集合。共同锚点不足两个时改用独立 SOFA 临床状态，但前提是 SOFA 和生存与去向语义可核验。

**预先确定的映射及其输出。** 对试验 r 的 C_r，使用 MIMIC 开发集预先记录的均值、标准差和第 1/99 百分位截断得到 Z_C；从阶段 II 已确定的观测方程 Z_C=a_C+L_C X+e 对 L_C 作奇异值分解 L_C=UDV'。V_1'X 定义为阶段 II 状态得分 P_state，D_1^(-1)U_1'(Z_C−a_C) 定义为由 RCT 实际访视指标计算的低维访视状态摘要 P_obs。奇异值并列时按预先规定的锚点字典序决定，符号在阶段 II 开发集中设为与同日 SOFA 总分非负相关，使数值越高表示状态越不利。映射不使用 RCT 治疗分组、RCT 结局或跨试验合并数据；每项试验使用各自的 C_r 和映射。

**摘要与阶段 II 状态表示的一致程度。** 首先在阶段 II 的 eICU 独立外部测试数据相应 D7 或 D8 时间窗中评价，不依据 RCT 结果调整参数。须同时满足：第一奇异轴解释 L_C Frobenius 能量至少 50%；P_state 与 P_obs 相关≥0.70；相对 P_state 标准差的归一化 MAE≤0.50；回归 P_state=α+βP_obs 时 |α|≤0.20 SD、β为 0.80–1.20，95% 区间覆盖为 0.90–0.98；每个共同锚点的外部校准斜率为 0.80–1.20、标准化截距绝对值≤0.20。随后在遮蔽治疗标签的试验数据中检查：至少 80% 观测锚点位于阶段 II 预定的生理合理范围内，且至少 60% 访视时存活在院者能够由不少于两个实测锚点直接计算 P_obs。任一数值标准未达到、单位或时间不一致，或必须使用试验数据重新估计权重时，改用独立 SOFA 临床状态分析。

**低维访视状态摘要的估计对象。** D7 或 D8 前死亡者置于最差等级；访视时仍存活在院者按 P_obs 从高到低排序；访视前活着出院者置于单独的最有利等级。主要比较为与中心或分层随机化相容的 probabilistic index（即一名随机抽取治疗组受试者的结局优于一名随机抽取对照组受试者的概率，并按并列规则计分）。该比较估计随机分配对试验实际访视指标所形成低维摘要的影响。

**试验特异的独立次要临床状态分析。** 当共同锚点或摘要一致性与误差标准未满足，但 SOFA、死亡、住院或出院、随机化和中心语义可核验时，使用预先规定的独立临床状态：死亡置于最差等级，访视时存活在院者按 SOFA 从高到低排序，活着出院者置于最有利等级。若 D7 或 D8、随机化、中心、生存或去向的核心语义也无法核验，则只复现原结局或报告数据核验结果，不开展新状态结局分析。

| Trial | Population and visit | Missingness/death and analysis | Multiplicity and predefined stopping condition |
|---|---|---|---|
| EXIT-SEP | 目标为全部 1,817 名随机分配受试者构成的全体随机化受试者分析集；现有 1,760 例只能称结局完整子集；使用试验规定的 D7 访视，D1 若在随机化后不得作不受治疗影响的基线 | 死亡和活着出院按等级处理；存活在院但访视摘要锚点或 SOFA 缺失时，在每个 MI 数据集中用治疗、中心、已确认的随机化前协变量及既往实际访视信息插补后重新计算摘要，再用 Rubin 规则或 cluster bootstrap 合并；开展 delta ±0.5/±1 SD 与 best/worst tipping；转院或状态未知使用界限分析，不作 MAR | 遵循中心或分层因素；两项试验的主要状态结局构成 Holm FWER 0.05 家族；其他访视与模块按探索性 FDR；亚组只报告 treatment×subgroup interaction；关键 D7 或中心语义不足时不开展新状态结局分析 |
| XBJ-SCAP | 目标为全部 710 名随机分配受试者；不能重建全体随机化受试者分析集时使用全分析集 675 例的改良意向治疗分析并明确说明；PPS 617、sepsis-like 671 和 strict-overlap 658 只用于敏感性分析；使用试验规定的 D8 访视，D0 若不在随机化前不得作基线或变化量起点 | 使用相同的死亡与出院等级、MI、delta、tipping 和界限策略；不填补结构性不存在的 PaO2/FiO2、乳酸、休克、CRRT 或 CNS；D-dimer 单位未核验时排除 | 使用同一 Holm 家族；亚组只报告交互；不能重建全体随机化受试者分析集时明确改良意向治疗分析；关键 D8、中心、生存或去向语义不足时不开展新状态结局分析 |

稀疏的 D1、D4、D7 或 D0、D4、D8 访视只支持访视特异或离散变化分析，不插值成连续轨迹。两项试验的人群、访视、锚点或估计对象不同，因此始终分别报告。

### Secondary representation diagnostics

部分状态重建使用伪遮蔽 MAE、RMSE、对数评分和区间覆盖；未来轨迹使用 CRPS、负对数似然、状态占用和结局校准。诊断按变量、状态、医院和观察密度分层。伪遮蔽只评价原本已测值的重建，诊断结果与两项主要任务及模拟恢复结果分别报告。

## Key techniques and implementation

1. **按信息可用时间构建标签：** 同时输出 event time、label-availability time、源表和时间、主标签与敏感标签以及样本流；特征查询要求 availability<landmark。[1-3]
2. **双数据库可观测性与样本支持核验：** 生成患者、stay、医院、跨院链接、landmark、事件、转移、单位、接口、密度和缺失矩阵，据预定规则确定时间网格、模块、K、regime 和参数数。
3. **预先区分变量用途：** 每个字段只有一个主要角色；标签派生副本独立并强制滞后，器官支持不作生理锚点。
4. **先实施简单基线：** 先完成竞争风险、多状态或 Aalen–Johansen 和线性状态空间模型，再评价至多一个复杂候选。
5. **锚定和不变量：** 预先规定 loading、尺度、符号、维度、允许图和滞后，多随机种子对齐后只解释稳定不变量。
6. **缺失非随机与行动支持：** pattern-mixture delta、selection tipping-point、接口压力分析与行动重叠或 ESS 共同确定需要弃权的关系。
7. **按医院隔离外部测试：** 医院预先划分、主要分析排除跨划分患者、实施 test-dominant component 敏感性，并由独立保管人控制测试数据访问。
8. **从阶段 II 模型映射到试验实际访视指标：** 每项试验使用合格共同锚点和阶段 II 观测 loading 的 SVD 计算一维访视状态摘要，在治疗比较前评价摘要与阶段 II 状态的一致程度；未达到标准时改用独立 SOFA 临床状态。
9. **不确定性与多重性：** 预先编码患者和医院 bootstrap、模拟 MCSE、MI、delta、tipping-point、中心分层 probabilistic index 和 Holm 家族。
10. **负向控制与完整结果报告：** 使用临床预裁定的时间反转与阴性对照，并报告标签、共同变量处理、缺失模式、复杂模型未获支持、外部测试未达标和试验映射未达标的结果。[16]

## Evidence chains

### Evidence chain: 信息可用时间、风险集与互斥病程

- **Input:** Sepsis-3、培养与抗菌药和 SOFA 时间、死亡、出院与转院事件、公共 ICU 数据字典以及待执行的 G1。[1-10]
- **Method / analysis / processing:** 主标签与两种敏感标签；event/availability 双时钟；12 小时 landmark；首次发病与 delayed entry；互斥状态、竞争事件、患者权重和泄漏检查。
- **Output:** 可执行的未来 12 小时首次发病累积发生风险队列、第 7 日多状态队列、标签差异矩阵和泄漏报告。
- **Supports:** 目标 1，以及候选模型覆盖发病前、首次发病、发病后和结局的研究边界。

### Evidence chain: 样本支持、锚定与绝对恢复

- **Input:** 待执行的双数据库锚点、接口与事件核验、知识先验、三类时变过程角色，以及正确、零边、过拟合和错设数据生成器。
- **Method / analysis / processing:** 共同模块和复杂度标准；锚定 loading、尺度、图和 lag；至少 1,000 次 Monte Carlo；MNAR、政策反馈、接口缺失与数据库差异；绝对 recovery、FDR、coverage 和错误结构检查。
- **Output:** 一个达到全部标准的受限复杂候选，或获得支持的多状态、线性或仅预测基准模型，附删除、合并和弃权清单。
- **Supports:** 目标 2 和 3 中可估计的不变量。

### Evidence chain: 两项主要任务与两项次要诊断

- **Input:** 已确定的队列、状态、候选模型、开发与时间外及医院外数据划分和预设指标。
- **Method / analysis / processing:** 未来 12 小时首次发病累积发生风险、第 7 日状态占用、概率评分、校准、cluster bootstrap、伪遮蔽、轨迹诊断、标签和 MNAR 与行动或观测消融及负向控制。
- **Output:** 两个主要任务的 Brier、校准和状态概率，两个次要诊断的评分、覆盖及失败中心、亚组和观察密度图。
- **Supports:** 目标 3 的患者—时间状态任务有效性和合取成功定义。

### Evidence chain: 按医院隔离的跨数据库验证

- **Input:** 已确定的开发模型与分析方案、按医院预先分配的 eICU 适配集和测试集、跨院患者链接记录、共同锚点和预设数值标准。
- **Method / analysis / processing:** 主要分析排除跨划分患者；同一划分内保留首次合格 stay；实施 test-dominant component 敏感性；依次评价不更新参数的外部验证、仅重新校准和仅更新观测模型，并报告患者与医院聚类、状态对齐和失败模式。
- **Output:** 跨划分排除数量和结局前特征、样本支持判定、不更新参数与有限更新结果、完整重新开发的独立标记，以及 stable、database-specific 和 abstained 清单。
- **Supports:** 目标 3 和阶段 II 的跨数据库候选系统表征验证。

### Evidence chain: 条件性试验访视摘要或独立临床状态分析

- **Input:** 已完成的阶段 II 观测方程；每项试验实际 D7 或 D8 访视的合格共同锚点；EXIT-SEP 随机分配 1,817 例和 XBJ-SCAP 随机分配 710 例的条件性个体数据；原始 CRF/SAP、中心、时间和生存与去向语义。[17,18,21-25]
- **Method / analysis / processing:** 分试验核验语义与共同锚点；用预先确定的 SVD 映射计算低维访视状态摘要；在 eICU 数据中评价相关、NMAE、校准、coverage，并在遮蔽治疗分组的试验数据中评价可计算比例；达到标准时分析按死亡和出院分层的访视摘要，未达到时分析按死亡和出院分层的独立 SOFA 临床状态；按全体随机化受试者或明确的改良意向治疗分析集、中心、MI、delta、tipping、Holm 和亚组交互规则实施。
- **Output:** EXIT-SEP D7 与 XBJ-SCAP D8 分开报告的低维访视状态摘要比较、试验特异的独立次要临床状态分析，或核心语义不足记录，并列出不可估计内容。
- **Supports:** 目标 4 的条件性、分试验次要分析。

## Required analyses and evidence

阶段 II 必须形成以下可核验交付：

1. 公共数据库访问与角色确认记录，以及填写完整的 G1 样本、事件、转移、医院、跨院患者、锚点、接口与复杂度表。
2. 主标签、两种敏感标签、event/availability 双时钟、12 小时 landmark、第 7 日状态、优先级、delayed entry、竞争事件与删失的单元测试记录。
3. 变量用途表、双用字段独立副本和滞后规则，以及未来信息、测量频率、患者、住院和数据处理跨划分泄漏检查。
4. 简单基线、绝对 Monte Carlo、零边和错设情景结果，以及复杂候选未获支持时的模型选择记录。
5. MNAR delta 和 tipping-point、行动重叠与 ESS、接口缺失、标签误差、时间反转和临床阴性对照结果。
6. 两项主要任务与两项次要诊断的概率评分、绝对校准、覆盖、警报负担和患者与医院聚类区间，以及状态与边的弃权记录。
7. 医院分配表、跨划分患者排除表、结局前特征比较、test-dominant component 敏感性、数据访问记录，以及不更新参数、重新校准、更新观测模型和完整重新开发四类结果的明确标识。
8. 月 24 的合取结论表，逐项记录达到、采用较简单模型或未达到，并将基准资源价值与跨数据库验证成功分开。

试验次要分析启动前还须形成：个体数据分析授权及原始 CRF/SAP、随机化、中心、访视时间、生存与去向语义核验记录；EXIT-SEP 57 例未知状态与 XBJ-SCAP 全体随机化受试者和全分析集差异处理记录；每项试验的 C_r、单位、时间窗、SVD 映射、摘要一致性与误差结果、分析分支标识、probabilistic-index 并列规则、MI 结合推断、中心处理、Holm 家族和亚组交互分析规范。代表性相关研究综合须继续支持保守的贡献定位。

## Expected outputs, falsification criteria, and interpretations

### Planned outputs

1. 双时钟标签、12 小时风险集、互斥发病后状态、G1 样本支持规范及可重复代码。
2. 变量用途规则、共同概念、接口和缺失资源、医院优先划分及跨院患者排除记录。
3. 简单基线、绝对恢复、错误结构与弃权基准结果，以及至多一个达到预设标准的复杂候选或较简单模型结果。
4. 两项主要任务与两项次要诊断的开发、时间外、医院外及独立外部测试结果，包括校准、不确定性、状态对齐和失败模式图。
5. 条件满足时分别报告两项试验的次要分析：由实际访视指标形成的低维状态摘要，或与阶段 II 独立的 SOFA 临床状态；核心语义不足时报告数据核验结果。
6. 以一篇或多篇高水平论文为目标的研究报告，以及可复用的标签、基准数据说明和分析资源。

### Observable falsification criteria

- 后录入标签、同一时间段的未来行动、未来测量频率或跨划分数据处理实质驱动结果时，相应临床任务未得到支持。
- 两个数据库的事件、转移、医院、跨院排除或共同锚点未达到 G1 数值时，相应跨数据库复杂表示未得到支持。
- 状态与转移恢复、区间覆盖、零边错误结构或错设识别未达到预设标准时，复杂候选未得到结构恢复支持。
- MNAR tipping-point 改变结论或行动重叠不足时，相应关系只报告敏感区间或照护政策特异结果。
- 预先确定的模型在未更新参数的外部测试中，其概率评分、状态对齐或结构符号未达到预设标准时，跨数据库稳定性未得到支持；预留适配集上的重新校准或观测模型更新结果作为不同证据报告。
- 阶段 II 到试验实际访视指标的映射在共同锚点、单位、时间、低维性、相关、误差、校准或覆盖方面未达到预设标准时，只实施独立 SOFA 临床状态分析；随机化、中心、访视、生存或去向语义不足时不实施新状态结局分析。
- 月 12 无达到标准的复杂候选、月 20 未完成开发方案或月 24 无独立外部测试结果时，分别记录复杂候选、外部测试准备或阶段 II 最低交付未完成。

### Interpretation matrix

| Observed pattern | Interpretation supported at that evidence level |
|---|---|
| 简单基线有用而复杂候选恢复标准未达到 | 多状态或预测基准具有任务价值，并形成复杂结构未获支持的证据 |
| 模拟恢复达到标准但未更新参数的外部测试未达标 | 候选在开发数据与预设生成情景中可恢复，但未建立跨数据库稳定性 |
| 未更新参数的外部测试未达标而有限更新后达标 | 预留适配集上的重新校准或观测模型更新改善目标数据库表现，属于有限适配证据 |
| 两项主要任务达标但某些状态或边触发弃权 | 支持任务级状态表示，相关结构只保留获得稳定支持的部分 |
| 试验访视摘要达到预设映射标准且组间不同 | 支持该试验随机分配对实际访视指标所形成低维摘要的影响 |
| 访视摘要映射未达标而独立 SOFA 临床状态组间不同 | 支持该试验中的独立次要临床状态差异 |
| 阶段 II 全部合取标准达到 | 支持最小全病程候选模型获得模拟恢复、任务有效性与跨数据库验证证据 |

## Contribution, innovation, impact, application, and closest-work comparison

### Contribution and evidence ladder

研究的增量是三层连接：输入层把可比较的未发病预测时点、首次发病与互斥发病后状态置于同一风险集；模型层以预先区分的患者状态、治疗行动和观测过程、锚定不变量、绝对恢复以及医院优先数据划分约束复杂模型；输出层把独立外部验证与条件性随机试验次要分析排列为前后相继而不互相替代的证据层。若执行成功，可形成整合、验证、可复用基准数据与分析资源以及方法规范价值。

| Evidence level | Positive claim | Necessary evidence | Current scope |
|---|---|---|---|
| 数据可追溯 | 标签、时钟、风险集、变量和接口可复核 | 双数据库 G1、角色表和泄漏检查 | 计划，尚未生成 |
| 状态重建与任务有效性 | 观察到的照护政策下候选状态具有任务有效性 | 绝对恢复、两项主要任务、两项次要诊断、校准和弃权 | 阶段 II 必需 |
| 跨数据库状态与结构稳定 | 预先确定的不变量在独立测试数据库中稳定 | 按医院隔离的不更新参数验证、有限更新分开报告、对齐和失败模式图 | 阶段 II 最低端点 |
| 随机化访视摘要影响 | 分配组在实际访视低维状态摘要上不同 | 语义与共同锚点核验、映射标准、全体随机化受试者或明确改良意向治疗分析、死亡与缺失处理、中心和多重性 | 条件性阶段 III |
| 独立试验临床状态 | 分配组在按死亡与出院分层的 SOFA 临床状态上不同 | SOFA 与核心试验语义充分，独立于阶段 II 映射 | 条件性阶段 III 的替代分析 |

### Representative related-work comparison

| Research line | Representative related study and stable identifier | Established work | Conditional increment evaluated here |
|---|---|---|---|
| 纵向与多状态 | Klein Klouwenberg et al. 2019，DOI 10.1186/s13054-019-2687-z，PMID 31831072；Xu et al. 2022，DOI 10.1186/s13054-022-04071-4，PMID 35786445。[26,27] | 已发病脓毒症的日级转移、轨迹聚类与外部复现 | 在同一风险集中连接发病前预测时点、首次发病和互斥发病后状态，并按双时钟防止未来信息 |
| 动态表型与治疗条件转移 | Boussina et al. 2023，DOI 10.2196/45614，PMID 37351927；Ghassemi et al. 2017，PMID 28815112，PMCID PMC5543372；Feng et al. 2025，DOI 10.1016/j.eclinm.2025.103691，PMID 41497501。[29-31] | 潜状态、动态表型、观察性治疗条件转移和器官交互图 | 分开 Y_t、A_t、M_t、标签与 B，并以零边和错设模拟限制结构解释 |
| 数字孪生与模型预测控制 | Lal et al. 2020，DOI 10.1097/CCE.0000000000000249，PMID 33225302；Pickard et al. 2026，arXiv:2607.08793。[32,33] | 患者特异模拟、脓毒症数字孪生原型及模型预测控制原型 | 本研究评价候选系统表示、恢复与跨数据库稳定性 |
| 强化学习与跨数据库评价 | Komorowski et al. 2018，DOI 10.1038/s41591-018-0213-5，PMID 30349085；Nauka et al. 2025，DOI 10.1038/s41746-025-01485-6，PMID 39915643；Tang et al. 2026，DOI 10.1038/s41746-026-02625-2，PMID 42098339；Kalimouttou et al. 2025，DOI 10.1001/jama.2025.3046，PMID 40098600。[19,34-36] | 离线策略学习、跨观察数据库评价、离策略评估和时间构造风险 | 以时间顺序、医院隔离、绝对恢复与弃权作为候选系统模型评价条件 |
| 随机试验次要分析 | Bhavani et al. 2022，DOI 10.1007/s00134-022-06890-z，PMID 36152041；AI Clinician 影子评估注册 NCT05287477。[28,37] | 在随机试验中进行表型—治疗二次交互及观察性影子部署 | 先评价阶段 II 模型到各试验实际访视指标的预定映射，再按试验分别分析实际访视摘要或独立临床状态 |

截至 2026-07-17 的有界代表性检索对“各模块已有先例”给出高置信判断；该检索未发现同时覆盖发病前、发病时刻、发病后演化、任务或节点级跨数据库验证和随机试验稀疏访视分析，并分开状态、行动和观测过程的完整代表性工作，但这一负向合取判断只有低至中等置信。[38] 因此当前可支持的定位是条件性的证据整合与验证增量。

## Title and positioning claim-support table

| Title or positioning claim | Contribution frame | Planned implementation | Evidence-chain output | Current support | Required wording |
|---|---|---|---|---|---|
| “脓毒症全病程候选动态系统模型”界定研究对象 | integration / validation | 双时钟、首次发病任务、互斥发病后状态及三类时变过程分工 | 信息可用时间、风险集与互斥病程；样本支持、锚定与绝对恢复 | supported as a planned candidate | 保留“候选、构建与验证”的计划性表述 |
| “跨数据库验证”界定阶段 II 核心动作 | 验证与基准资源 | 按医院预先分配适配集与测试集、排除跨划分患者、首先评价不更新模型参数的外部表现 | 按医院隔离的跨数据库验证 | 访问、G1 和结果均有待获得的条件性支持 | 明确不更新参数的外部验证与有限适配结果分开 |
| “预设条件满足后使用随机试验稀疏访视数据开展次要分析”界定后续动作 | 验证与转化研究 | 分试验核验语义与共同锚点、预定 SVD 映射、独立 SOFA 临床状态分析和分试验估计对象 | 条件性试验访视摘要或独立临床状态分析 | 条件性且前瞻性的支持 | 条件修饰分析是否开展，稀疏修饰访视数据，次要修饰分析 |
| 贡献是整合、验证和可复用基准资源 | 整合、验证与资源 | G1、变量用途规则、绝对恢复、独立外部测试和预定替代分析 | 前四条证据链的联合输出 | 支持作为贡献定位 | 各单项模块已有先例，增量取决于执行结果 |
| 完整组合缺口 | 科学创新定位 | 截至 2026-07-17 的有界代表性检索 | 代表性相关研究比较 | 低至中等置信度的条件性支持 | 只写本次有界检索未发现代表性工作 |

## Feasibility, resources, risks, alternatives, and stop conditions

### Working assumptions and complete limitations

以下假设仅用于推进计划，均不是已确认事实：团队可在月 3 前获得两个公共 ICU 数据库的访问和 DUA；两个数据库能够支持同一主发病前风险集、发病后状态队列以及足够的医院、事件、转移和共同锚点；临床、纵向统计、系统辨识、数据工程、模型实现和独立数据保管角色能够具名并投入所需工时；临床量表能够在不读取最终测试结果的情况下映射为模拟参数；预先规定的多类别校准估计量、置信区间和数值注册记录能够在月 6 前完成；条件性阶段 III 所需的个体数据授权、原始 CRF/SAP、随机化、中心、实际访视时间、生存和去向语义以及至少两个共同锚点可能获得核验。任何假设只有经相应记录确认后才能作为后续分析前提。

本研究的完整限制如下：数据库公开存在和版本可核验，并不表示团队已获得凭证、DUA、可运行提取或项目队列支持；当前没有具名人员承诺，也没有候选模型、模拟恢复、预测、外部测试或试验新分析结果。电子健康记录中的脓毒症发病时刻依赖疑似感染配对、基线 SOFA、观察窗和信息可用时间；接口缺失可能是医院层问题，未来信息、同一时间段行动、测量频率、重复住院和跨划分数据处理均可能造成泄漏。隐藏状态可能因锚定不足、任意旋转、状态数或滞后错设而不可恢复；预设模拟只覆盖所列生成情景。缺失非随机、测量政策、治疗—病情反馈和行动低重叠限制相关关系的解释，阴性对照或时间反转未发现偏倚也不能证明模型正确。

不同公共 ICU 数据库在中心、年代、采样、变量语义和接口方面存在差异；在不更新参数的外部测试中未达到预设标准，不能由预留适配集上的重新校准、观测模型更新或目标数据库内完整重新开发所替代。跨医院患者链接和排除可能使测试医院、事件、转移或锚点支持不足。阶段 I–II 必须在 24 个月内完成，阶段 III 不属于最低交付，不能补足阶段 II 的任何失败。

EXIT-SEP 与 XBJ-SCAP 的现有本地材料只是衍生清洗或验证报告，不能替代个体数据授权、原始 CRF/SAP、随机化、中心、访视相对随机化或首剂的时间、生存和去向语义核验。两项试验的人群、访视、变量和分析集不同，稀疏访视不支持连续轨迹插值；共同锚点、单位、时间或从阶段 II 模型到实际访视指标的映射不足时，独立 SOFA 临床状态分析与阶段 II 模型没有验证关系。两项试验不合并，后续试验结果不改变阶段 II 判定。

观察性数据和预测表现不能识别真实因果网络、治疗因果效应、反事实策略、机制、中介、控制或数字孪生；条件性随机试验次要分析也不能验证未测潜在动力学、转移边或整个系统模型。当前计划不是已验证模型、临床决策工具、药物平台或无条件临床推广依据。代表性相关研究检索截至 2026-07-17，未采用 PRISMA 双人筛选、完整引文网络、专利、CNKI、万方、Scopus、Web of Science、Embase 或所有注册平台，且预印本和术语变化可能造成遗漏，因此不能支持全球首次、新算法或类似不存在性主张。

### Risks, bounded alternatives, and stopping rules

| Risk | Observable trigger | Bounded alternative | Consequence |
|---|---|---|---|
| 数据访问或支持不足 | 月 3 无两个可访问数据库；月 6 的事件、锚点或医院支持不足 | 启用预先指定的备份数据库；改用 24 小时或事件时间；删除模块或边 | 两个数据库仍不能支持全病程研究时，停止跨数据库系统端点 |
| 跨院患者破坏隔离或支持 | 患者跨适配集与测试集；排除后少于 20 个医院、低于事件、转移或锚点标准，或排除比例>10% | 主要分析排除全部相关患者；实施 test-dominant component 敏感性；启用备份数据库 | 不重新分配测试医院，不允许患者跨集合；支持仍不足时缩小为数据库层描述或停止相应端点 |
| 标签或时间泄漏 | 结果受后可用信息、同一时间段行动、未来测量频率或跨划分处理驱动 | 修正 as-of 规则、删除变量并保留可执行标签 | 高严重度泄漏未消除时不访问最终测试集 |
| 状态不可识别或错误结构 | 恢复、FDR、coverage、零边或错设标准未达到 | 改用多状态、线性或仅预测模型 | 复杂候选不再用于结构解释，不能由预测分数重新纳入 |
| MNAR 或行动低重叠 | delta tipping 改变结论；行动比例<5%或>95%，或 ESS<20% | 报告敏感区间，合并或删除相应关系并标记照护政策特异 | 不估计相应未测值真值或治疗作用 |
| 不更新参数的外部测试未达标 | 概率评分、状态对齐或结构符号标准未达到 | 分开报告预留适配集上的重新校准和观测模型更新 | 有限更新达标不认定原模型跨数据库验证成功 |
| 试验共同锚点或映射不足 | 共同锚点少于 2 个、单位或时间不一致，或摘要一致性与误差任一标准未达到 | 使用死亡置于最差等级、存活者按 SOFA 排序的独立临床状态 | 该结果只解释为试验特异次要临床状态差异 |
| 试验核心语义不足 | 随机化、中心、D7/D8、生存或去向语义无法核验 | 复现原结局或报告数据核验 | 不开展新状态结局分析，不推测轨迹或字段 |
| 时间超限 | 月 12 无达到标准的复杂候选；月 20 未完成开发方案；月 24 无最终外部测试结果 | 封存当时获得支持的较简单模型或完成部分 | 分别记录复杂候选、外部测试准备或阶段 II 最低交付未完成 |
| 代表性相关研究结论外推 | 需要声称全球首次、专利不存在或类似排他性结论 | 开展系统综述、引文与专利检索及非英语数据库补检 | 在完成补充证据前只保留有界、条件性的整合与验证定位 |

### Identity and final boundary

核心身份始终是构建和验证以脓毒症为中心、覆盖尚未发病、首次发病、发病后状态演化以及恢复、持续恶化、器官衰竭、出 ICU 或死亡的候选动态复杂系统模型，推断单位为尊重患者和医院聚类的患者—时间状态与状态转移。项目不改为已发病病例预后模型或泛 ICU 风险模型。阶段 I–II 在 24 个月内形成最低交付；月 24 无论获得完整支持、仅支持较简单模型或未完成，均如实记录阶段 II 结果。阶段 III 只有在阶段 II 成功且相应试验数据、语义和访视映射满足预设条件时才开展，不能绕过或补救资源、恢复、主要任务及外部验证的失败。

## References

1. Singer M, Deutschman CS, Seymour CW, et al. The Third International Consensus Definitions for Sepsis and Septic Shock (Sepsis-3). JAMA. 2016;315:801-810. doi:10.1001/jama.2016.0287.
2. Seymour CW, Liu VX, Iwashyna TJ, et al. Assessment of Clinical Criteria for Sepsis. JAMA. 2016;315:762-774. doi:10.1001/jama.2016.0288.
3. Subtle variation in sepsis-III definitions markedly influences predictive performance within and across methods. 2024. PMCID: PMC10803347.（页面/摘要层核验，partial。）
4. Surviving Sepsis Campaign: International Guidelines for Management of Sepsis and Septic Shock 2026. Intensive Care Medicine. 2026. doi:10.1007/s00134-026-08361-1; Critical Care Medicine version doi:10.1097/CCM.0000000000007075.
5. MIMIC-IV Clinical Database, version 3.1. PhysioNet. doi:10.13026/kpb9-mt58; Johnson AEW, et al. Scientific Data. 2023;10:1. doi:10.1038/s41597-022-01899-x.
6. eICU Collaborative Research Database, version 2.0. PhysioNet. doi:10.13026/C2WM1R; Pollard TJ, et al. Scientific Data. 2018;5:180178. doi:10.1038/sdata.2018.178.
7. HiRID, version 1.1.1. PhysioNet. doi:10.13026/323r-nk04.
8. Thoral PJ, Peppink JM, Driessen RH, et al. Amsterdam University Medical Centers Database. Critical Care Medicine. 2021;49:e563-e577. doi:10.1097/CCM.0000000000004916.
9. Oliver M, et al. BlendedICU: A comprehensive, harmonized dataset of intensive care data. Journal of Biomedical Informatics. 2023;146:104502. doi:10.1016/j.jbi.2023.104502.
10. Bennett N, et al. ricu: R's interface to intensive care data. GigaScience. 2023;12:giad041. doi:10.1093/gigascience/giad041.
11. Predicting sepsis using deep learning across international sites: a retrospective development and validation study. PMCID: PMC10425671.
12. Wong A, Otles E, Donnelly JP, et al. External Validation of a Widely Implemented Proprietary Sepsis Prediction Model. JAMA Internal Medicine. 2021;181:1065-1070. doi:10.1001/jamainternmed.2021.2626.
13. Seymour CW, Kennedy JN, Wang S, et al. Derivation, Validation, and Potential Treatment Implications of Novel Clinical Phenotypes for Sepsis. JAMA. 2019;321:2003-2017. doi:10.1001/jama.2019.5791.
14. Robins JM, Hernán MA, Brumback B. Marginal Structural Models and Causal Inference in Epidemiology. Epidemiology. 2000;11:550-560. doi:10.1097/00001648-200009000-00011.
15. Agniel D, Kohane IS, Weber GM. Biases in electronic health record data due to processes within the healthcare system. BMJ. 2018;361:k1479. doi:10.1136/bmj.k1479.
16. Lipsitch M, Tchetgen Tchetgen E, Cohen T. Negative Controls. Epidemiology. 2010;21:383-388. doi:10.1097/EDE.0b013e3181d61eeb.
17. Liu S, et al. Effect of Xuebijing Injection on 28-Day Mortality Among Patients With Sepsis: EXIT-SEP. JAMA Internal Medicine. 2023;183:647-655. doi:10.1001/jamainternmed.2023.0780.
18. Song Y, et al. XueBiJing Injection Versus Placebo for Severe Community-Acquired Pneumonia. Critical Care Medicine. 2019;47:e735-e743. doi:10.1097/CCM.0000000000003842.
19. Komorowski M, Celi LA, Badawi O, Gordon AC, Faisal AA. The Artificial Intelligence Clinician. Nature Medicine. 2018;24:1716-1720. doi:10.1038/s41591-018-0213-5; PMID 30349085.
20. Gottesman O, Johansson F, Komorowski M, et al. Guidelines for reinforcement learning in healthcare. Nature Medicine. 2019;25:16-18. doi:10.1038/s41591-018-0310-5.
21. Efficacy of Xuebijing Injection for Sepsis (EXIT-SEP): protocol for a randomised controlled trial. PMCID: PMC6720249.
22. EXIT-SEP 数据集构建验证报告. 项目本地衍生验证材料，2026-07-12；rct-data/exit_sep_dataset_validation_report.md.（非原始 CRF/SAP 或独立同行评审。）
23. EXIT-SEP participants clean/SAP subset/field-coverage audit workbooks. 项目本地只读 QC 材料.（本次 v003 未读取 participant-level 工作簿。）
24. XBJ-SCAP 数据集构建验证报告. 项目本地衍生验证材料，2026-07-13；rct-data/xbj_scap_dataset_validation_report.md.（非原始 EDC/CRF 审计。）
25. XBJ-SCAP participants clean/reproduction-transportability QC workbooks. 项目本地只读 QC 材料.（本次 v003 未读取 participant-level 工作簿。）
26. Klein Klouwenberg PMC, et al. Predicting the clinical trajectory in critically ill patients with sepsis: a cohort study. Critical Care. 2019. doi:10.1186/s13054-019-2687-z; PMID 31831072.
27. Xu Z, et al. Sepsis subphenotyping based on organ dysfunction trajectory. Critical Care. 2022. doi:10.1186/s13054-022-04071-4; PMID 35786445.
28. Bhavani SV, et al. Development and validation of novel sepsis subphenotypes using trajectories of vital signs. Intensive Care Medicine. 2022. doi:10.1007/s00134-022-06890-z; PMID 36152041.
29. Boussina A, et al. Representation Learning and Spectral Clustering for Development and External Validation of Dynamic Sepsis Phenotypes. JMIR. 2023. doi:10.2196/45614; PMID 37351927.
30. Feng Y, et al. Subphenotyping sepsis based on organ interaction trajectory using a deep temporal graph clustering model. eClinicalMedicine. 2025. doi:10.1016/j.eclinm.2025.103691; PMID 41497501.
31. Ghassemi M, et al. Predicting intervention onset in the ICU with switching state space models. 2017. PMID 28815112; PMCID: PMC5543372.
32. Lal A, et al. Development and Verification of a Digital Twin Patient Model to Predict Specific Treatment Response During the First 24 Hours of Sepsis. Critical Care Explorations. 2020. doi:10.1097/CCE.0000000000000249; PMID 33225302.
33. Pickard J, et al. Inference-Time Control for Sepsis Treatment with Generative Patient Digital Twins. 2026. arXiv:2607.08793.
34. Nauka PC, et al. Challenges with reinforcement learning model transportability for sepsis treatment in emergency care. npj Digital Medicine. 2025. doi:10.1038/s41746-025-01485-6; PMID 39915643.
35. Tang S, et al. Off by a beat: the effects of temporal misalignment in reinforcement learning for sepsis treatment. npj Digital Medicine. 2026. doi:10.1038/s41746-026-02625-2; PMID 42098339.
36. Kalimouttou A, et al. Optimal Vasopressin Initiation in Septic Shock: The OVISS Reinforcement Learning Study. JAMA. 2025. doi:10.1001/jama.2025.3046; PMID 40098600.
37. Passive Evaluation in Operational Environment of the AI Clinician Decision Support System for Sepsis Treatment. ClinicalTrials.gov: NCT05287477.
38. 脓毒症复杂系统模型：最接近工作刷新. 项目本地有界检索综合，search-through date 2026-07-17；closest-work-update-v001.md.（partial；不是系统综述或全球不存在性证明。）
