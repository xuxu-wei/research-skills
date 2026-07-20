---
schema_version: research-idea.v3
plugin_version: 0.9.0-preview.1
artifact_id: idea-dossier-I01-001-v004
workflow_id: RID-SEPSIS-CSM-20260717-001
idea_id: I01-001
version_id: v004
parent_idea_ids: []
based_on:
  - artifact_id: idea-dossier-I01-001-v003
    version: v003
    path: tests/idea-test-0.9.0-preview.1/0.9.0-preview.1/03_ideas/nodes/I01-001/dossiers/idea-dossier-v003.md
  - artifact_id: narrative-repair-plan-I01-001-r013
    version: r013
    path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/baseline/narrative-repair-plan-r013.yaml
  - artifact_id: language-assessment-I01-001-r010
    version: r010
    path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass/baseline/language-assessment-r010.md
  - artifact_id: protected-content-register-I01-001-v003
    version: v003
    path: tests/idea-narrative-forward-0.9.0-preview.3/run-001/inputs/protected-content-register.yaml
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
frozen: true
---

# 脓毒症全病程候选动态系统表征及其计划性跨数据库检验

## Title, summary, audience, and positioning

- **Title:** 脓毒症全病程候选动态系统表征及其计划性跨数据库检验
- **One-sentence complete-Idea summary:** 本研究计划在 24 个月内，利用文献与专家先验以及两个须先完成访问和可观测性审计的公共 ICU 数据库，构建并检验一种知识约束且能表达不确定性的候选动态系统表征；该统计表征连接脓毒症发病前在险时段、首次发病、发病后互斥状态及结局，并明确区分患者状态、状态转移、治疗过程和观测过程，其阶段 I–II 证据来自基于预设绝对阈值的模拟恢复检验和独立保留数据库上的外部验证。
- **Primary audience:** 重症医学、临床流行病学、纵向统计、系统辨识、医学人工智能与转化研究共同体；当前不预设具体期刊。
- **Positioning and contribution frame:** 主要贡献定位是候选动态系统表征的条件性整合与验证，以及可复用的基准和研究资源。各单项模块已有高置信度先例；本项目不主张新算法或全球首次。完整组合的文献缺口仅由截至 2026-07-17 的有界检索以低至中等置信度支持。[26-38]
- **24 个月后条件性扩展:** 阶段 III 不属于最低交付，也不参与阶段 II 成功判定。只有在阶段 II 完成，且试验资料语义与观测映射均满足预设标准时，才分别对 EXIT-SEP 第 7 日和 XBJ-SCAP 第 8 日开展次要分析。其一维可观测状态摘要由实际访视时测得的共同生理指标，经阶段 II 预先确定的观测模型计算，用于访视时点排序比较；若该映射不合格，则改用与阶段 II 表征独立的死亡优先排序 SOFA 复合状态端点。

## Structured abstract

- **Background and gap:** Sepsis-3 为感染相关器官功能障碍及 SOFA 提供操作基础，但疑似感染配对、基线、时间窗和标签可用时间都会改变电子健康记录中的发病标签。[1-3] 纵向多状态模型、动态表型、干预条件转移、数字孪生、模型预测控制、离线强化学习、跨数据库验证以及随机对照试验的表型—治疗次要分析均已有代表性先例。[26-37] 现有有界检索尚未以充分置信度找到一种同时连接全病程时间轴、状态—行动—观测分离、绝对恢复、独立外部验证和条件性试验扩展的代表性架构。[38]
- **Objective and hypothesis:** 目标是在 24 个月内完成阶段 I–II，构建并计划检验一个以患者—时间状态及状态转移为主要推断单位的候选动态系统表征。核心可证伪假设是：完成双库可观测性审计并锁定锚定方式、尺度、状态数和滞后后，至多一个受限复杂候选能够在预设生成情景中恢复可解释的不变量，并在时间外、医院外和独立保留数据库的测试中维持预设校准、状态对齐和结构稳定性。
- **Approach:** 发病前主要任务在每 12 小时评价时点使用此前最多 24 小时、至少 12 小时的当时可用信息，估计未来 12 小时首次发病的累积发生风险。发病后主要任务采用互斥多状态系统，估计第 7 日有利状态占用概率。竞争风险、多状态和线性状态空间基线先行；复杂候选只有通过模拟恢复和错误高置信判断的预设绝对标准才进入后续分析。外部数据库按医院预先划分适配集和独立保留测试集；主要外部验证不利用测试集重新估计任何参数，并与仅用适配集完成的校准更新及观测模型更新分开报告。
- **Expected result:** 计划产物包括可执行的标签和双时钟协议、双库观测与变量角色审计、互斥状态定义、模拟恢复与错误高置信判断记录、两项主要任务、两项次要表征诊断、独立外部验证结果及失败分布图。阶段 III 条件满足时，再分别估计 EXIT-SEP 第 7 日和 XBJ-SCAP 第 8 日的一维可观测状态摘要差异；若映射不合格，则使用死亡为最差、住院存活者按 SOFA 排序、活着出院为最有利的独立复合状态端点。这些均为计划产物，并非已有模型或结果。
- **Contribution and impact:** 阶段 II 的成功要求数据支持、模拟恢复、两项主要任务的适当评分与校准、无未解决的高严重度泄漏，以及独立保留数据库上不更新参数的外部验证同时成立。若执行成功，项目可提供条件性的整合、验证和基准资源价值，为判断脓毒症全病程候选表征是否值得继续研究提供可审计证据。

## Background, current state, gap, significance, and rationale

### Background

脓毒症随时间形成，并与治疗和检测行为共同演化。Sepsis-3 将其定义为感染所致失调宿主反应引起的危及生命器官功能障碍，研究中常以相对基线 SOFA 增加至少 2 分操作化，但这一定义不会产生唯一的电子健康记录发病时戳。[1,2] 改变疑似感染配对、SOFA 基线或观察窗会改变病例识别与预测表现。[3] 因此，本研究区分临床事件时刻与标签在数据库中可计算的时刻，避免把后录入信息用于更早的预测评价时点。

### Current state

MIMIC-IV、eICU-CRD、HiRID 和 AmsterdamUMCdb 提供纵向生命体征、实验室、治疗与结局资料，但中心、年代、采样方式和接口并不等价。[5-8] BlendedICU 与 ricu 表明，跨数据库统一只能建立在受限且经过审计的共同概念上。[9,10] 现有研究已经覆盖日级多状态转移、SOFA 或生命体征轨迹、动态表型、隐马尔可夫模型、器官交互图、观察性干预条件转移、状态空间模型、动态治疗方案、脓毒症数字孪生原型、模型预测控制、离线强化学习及其跨库和时间构造问题。[26-37] EXIT-SEP 与 XBJ-SCAP 提供随机分配证据，但重复测量访视较少，研究人群、变量和实际访视也不同。[17,18,21-25]

### Gap

这些单项工作不能共同回答：一个以脓毒症为中心的候选动态系统表征，能否在同一可追溯时间轴上连接尚未发病的在险片段、首次发病、发病后互斥状态和结局；能否把患者状态、治疗行动和观测过程分开；能否先证明预设不变量可恢复，再在独立保留数据库中检验状态和结构稳定性。现有有界检索仅以低至中等置信度支持这一组合缺口，不能证明此类架构在全球范围内不存在。[38]

### Significance

弥合这一缺口能够区分三类常被混合的证据：预测任务表现、候选结构的可恢复性，以及跨中心或跨数据库的稳定性。对重症研究者而言，这种区分可避免把局部预测优势误读为真实机制或可迁移系统；对纵向统计和系统辨识研究者而言，它提供了明确的失败结果与替代分析；对后续试验研究而言，它规定了何时只能报告独立临床状态差异，而不能把试验结果归因于阶段 II 表征。

### Rationale

双时钟直接处理发病事件与标签可用时间不一致的问题。患者状态、治疗行动和观测过程的分离回应治疗—病情反馈及测量强度携带照护政策信息的问题。[14,15] 基于预设绝对阈值的模拟恢复检验用于判断哪些状态、转移和结构量可以解释；阴性对照与时间反转只用于提示部分偏倚。[16] 按医院预先划分且独立保留的数据库测试用于检验不更新参数时的外部稳定性，并与适配后分析区分。阶段 III 仅在资料语义和冻结观测映射合格时检验一维可观测状态摘要；否则采用独立 SOFA 复合状态端点。SSC 2026 对未获当地监管批准辖区使用 XueBiJing 的建议仍保持谨慎。[4]

## Research question, objectives, and core hypothesis

### Primary research question

能否构建一个知识约束且能表达不确定性的 ICU 患者候选动态系统表征，在不混淆预测与因果的前提下，覆盖脓毒症发病前、首次发病、发病后状态演化和结局，并在医院之间和独立数据库之间检验患者状态及候选结构的稳定性？

### Conditional extension question

只有阶段 II 成功后，才进一步询问：若冻结的阶段 II 观测模型能够由 EXIT-SEP 第 7 日或 XBJ-SCAP 第 8 日实际测得的共同生理指标计算一维可观测状态摘要，随机分配是否改变该访视摘要；若不能，是否仅能在与阶段 II 独立的死亡优先排序 SOFA 复合状态端点上描述试验特异差异？该扩展不参与阶段 II 成功判定。

### Objectives

1. **阶段 I–II：全病程边界与可追溯时钟。** 锁定可实时实施的主 Sepsis-3 标签、标签可用时间、动态评价风险集、互斥发病后状态与竞争事件，并用两种合理标签作敏感性分析。
2. **阶段 I–II：审计约束的候选动态系统表征。** 由双库可观测性审计确定共同模块、时间方案和复杂度上限，显式分离生理状态、治疗行动和观测过程，只解释在允许重参数化下保持不变的量。
3. **阶段 I–II：模拟恢复与独立外部验证。** 用正确、零边、过拟合和错设生成情景检验绝对恢复及错误高置信判断；在第二数据库隔离适配集与独立保留测试集，检验两项主要临床任务和两项次要表征诊断。
4. **阶段 III：访视稀疏随机对照试验的条件性次要分析。** 分别检验冻结阶段 II 表征能否映射到 EXIT-SEP 第 7 日和 XBJ-SCAP 第 8 日的一维可观测状态摘要；合格时估计访视特异的随机化扰动，不合格时采用独立 SOFA 复合状态端点，并列出不可估计内容。

### Core hypothesis and non-hypotheses

核心假设是：若共同锚点与事件支持满足审计标准，锚定方式、尺度、状态数和滞后均预先锁定，且复杂候选通过模拟恢复与错误高置信判断检验，则部分状态占用、转移概率、锚点预测以及预设依赖的符号与滞后可在独立保留数据库中维持预定义稳定性。五条证据链分别连接数据边界、可恢复不变量、任务效度、跨数据库稳定性和条件性试验输出。

本研究不假设观察性数据能够识别治疗因果效应、真实反馈网络或反事实策略，也不假设随机对照试验能够识别未测靶点、潜在动力学、转移边、中介或个体控制。当前计划不是已验证模型、数字孪生、可控系统、临床决策工具或药物平台。

## Research content and work packages

阶段 I–II 的最低交付期为 24 个月；阶段 III 位于此期限之后。下列时间点规定产物、判定标准和预设后果，其中负责人签署只表示所需职责，不表示目前已有具名人员承诺。独立数据保管人在开发方案冻结前不开放外部最终测试结果。

| 时间 | 必需产物 | 判定及预设后果 |
|---|---|---|
| 月 0–3 | 确认 MIMIC-IV v3.1 与 eICU-CRD v2.0 的团队访问、数据使用协议、存储和算力；具名临床、统计、系统辨识和数据工程角色；预指定 HiRID 或 AmsterdamUMCdb 作为备份 | 任一主库无法承担预定角色即启动备份；月 3 仍无两个可访问数据库则停止 24 个月跨数据库路线 |
| 月 4–6 | 完成双库队列流、事件与转移、医院、跨院患者、锚点密度、接口和缺失审计；冻结主标签、双时钟、多状态、医院优先拆分、时间方案、共同模块和参数上限 | 若 12 小时方案不获支持，在拟合前改为 24 小时或事件时间；若跨院排除破坏支持，则启动备份或限制结论范围 |
| 月 7–12 | 完成竞争风险、多状态和线性状态空间基线；完成 Monte Carlo 与半合成模拟；评估至多一个切换或非线性复杂候选 | 任一关键恢复、零边错误高置信判断或错设检验不合格，即停止复杂扩展并采用预设简单模型 |
| 月 13–18/20 | 完成开发库内部、时间外和医院外验证；冻结标签、锚点、预处理、模型、超参数、更新层级、指标与外部阈值 | 高严重度泄漏未清除，或主要任务校准和适当评分不合格，则不开放最终外部测试；月 20 后不按测试结果修改 |
| 月 21–24 | 在第二数据库独立保留测试集报告不更新参数的结果，并另报仅用适配集完成的校准更新和观测模型更新；封存聚类不确定性、对齐及失败分布图 | 按合取标准判定阶段 II；失败仍可形成基准和研究资源，但不构成跨数据库候选动态系统表征成功 |
| 24 个月后 | 阶段 II 成功后，核验个体数据授权、原始 CRF/SAP 与试验资料语义；每项试验分别评价观测映射并执行预注册分支 | 映射合格时分析一维可观测状态摘要；映射不合格时采用独立 SOFA 端点；核心试验语义不明时停止新状态端点 |

阶段 II 成功必须同时满足：两库均能构造主发病前风险集和发病后状态队列，并达到冻结的事件、转移、医院和共同锚点支持下限；复杂候选通过正确生成、零边生成及核心错设情景的全部绝对标准；两个主要任务在开发及时间外验证中，相对最强简单基线的 Brier 或多类别 Brier 差值上侧 95% 界不超过 +0.01，校准斜率为 0.80–1.20，校准截距对应的绝对风险误差不超过 0.02；泄漏清单无未解决高严重度项目；外部测试仍包含至少 20 个合格医院，主要任务在不更新参数时达到 Brier 非劣标准，对齐后主要状态相关或一致性系数至少 0.70，预设结构符号一致率至少 0.80。适配后分析不能替代主要外部验证。

| 工作包 | 月份 | 主要内容 | 产物 |
|---|---:|---|---|
| WP1：标签、队列和可观测性审计 | 0–6 | 访问与版本、样本流、双时钟、变量角色、跨院患者、时间网格和接口 | 可执行风险集、多状态、医院优先拆分和共同模块 |
| WP2：知识结构、基线与模拟恢复 | 3–12 | 候选图、锚定限制、竞争风险、多状态、线性基线、Monte Carlo 与半合成模拟 | 至多一个复杂候选或预设简单模型 |
| WP3：主要任务与次要诊断 | 8–18 | 未来 12 小时首次发病累积发生风险、第 7 日状态占用、伪遮蔽重建、未来轨迹诊断及敏感性分析 | 适当评分、校准、覆盖、泄漏和弃权记录 |
| WP4：独立外部验证 | 14–24 | 冻结方案；医院级适配集和测试集；跨分区患者排除；不更新参数、校准更新和观测模型更新 | 独立外部结果、排除审计和失败分布图 |
| WP5：条件性阶段 III | 24 个月后 | 试验资料语义核验；冻结观测映射；一维摘要或独立 SOFA 分支 | 两项试验分开报告的次要分析 |

## Data, materials, and existing evidence base

下表将资源状态统一为“已核验”“未核验”“尚未生成”和“项目内衍生材料”。

| 资源或结果 | 当前证据 | 状态 | 后续要求 |
|---|---|---|---|
| MIMIC-IV v3.1 与 eICU-CRD v2.0 的公开存在、版本和文献 | PhysioNet 与原始数据库论文提供稳定 DOI 和版本记录。[5,6] | 已核验 | 仅证明数据库存在，不证明团队访问或本项目队列可执行 |
| 团队访问凭证、数据使用协议、下载与存储、确切提取版本及校验值 | 当前材料未提供完成证据 | 未核验 | 月 3 前确认；否则启动备份或停止双库路线 |
| 双库实际样本、事件、转移、医院、跨院患者、锚点密度和接口支持 | 尚未执行项目队列审计 | 尚未生成 | 月 6 前冻结；不足时减小维度、改变时间方案、启用备份或停止相应端点 |
| EXIT-SEP 与 XBJ-SCAP 本地验证报告 | 记录工作簿构建、关键非缺失及复现质量控制，但不是独立同行评审或原始审计。[22,24] | 项目内衍生材料 | 只能支持访视和字段缺口描述，不能替代个体数据授权、CRF/SAP 或数据持有人确认 |
| 随机对照试验个体数据授权、原始 CRF/SAP、随机化、中心、实际访视时序及生存和住院语义 | 现有衍生报告没有完成原始语义证明 | 未核验 | 任一影响估计对象的核心语义无法核验时，停止新状态端点 |
| 阶段 II 与试验的共同生理锚点、单位和实际访视映射 | WBC 和 CRP 只是候选；共同锚点资格与单位一致性尚未证明，D-dimer 单位仍有缺口 | 未核验 | 每项试验至少两个合格锚点；不足时采用独立 SOFA 分支 |
| 所需团队职责 | 临床与表型、纵向统计、系统辨识、数据工程、模型实现和独立数据保管职责已定义 | 已核验 | 职责规范不等于人员承诺 |
| 已承诺人员及可用工时 | 无可核验名单或承诺记录 | 未核验 | 月 3 前具名；缺少关键职责时不得签署审计或冻结方案 |
| 当前模型、模拟恢复、预测、外部测试或试验新分析结果 | 当前材料未提供任何已生成结果 | 尚未生成 | 所有结果须按时间表生成，不得写成既成事实 |
| 截至 2026-07-17 的最接近工作更新 | 项目内有界检索汇总代表性正式论文、预印本和注册记录 | 项目内衍生材料 | 模块已有先例为高置信度判断；完整组合缺口仅低至中等置信度 |

MIMIC-IV v3.1 计划作为开发库，eICU-CRD v2.0 计划作为外部库；HiRID 或 AmsterdamUMCdb 只能在月 0–3 预先指定并完成同等审计后替代失败角色，不能依据最终测试结果选择。[5-8] 共同层只保留单位、语义、时间戳和可见性均可审计的变量。[9,10]

月 6 前须按数据库生成并冻结：访问和版本记录；成年患者、住院和 ICU 记录；医院数和每院患者数；12 小时评价时点与首次发病事件；死亡、活着出院、转院或失访及行政结束；允许的状态转移；时戳精度；锚点单位、来源、密度、医院与患者覆盖；缺失、观测间隔和跨院链接；有效支持和复杂度上限。外部测试至少需要 20 个有事件支持的医院；每个自由风险参数在开发和外部分别至少有 20 和 10 个事件，每个自由转移参数分别至少有 20 和 10 次转移。每个共同维度至少需要两个锚点，每个锚点在两库至少 30% 合格时间段实测，并覆盖至少 70% 合格医院和 80% 合格患者。复杂度上限为通过审计的模块数与 4 的较小值，状态机制数不超过 3。

变量按主角色分为生理测量、治疗行动、测量过程、仅用于标签的信息和基线协变量。同一来源的标签副本须隔离，器官支持不作为潜在生理锚点；未检测不能解释为正常，医院接口缺失不能解释为患者状态。除有明确起止的输注或器官支持状态及静态基线外，不作无条件前向填充；每个动态值保留是否实测、实测时刻与距上次实测时间。

EXIT-SEP 在中国 45 个 ICU 随机分配 1,817 例 Sepsis-3 患者；本地衍生报告记录 1,760 例 28 日状态明确、395 例死亡、57 例状态未知，SOFA 第 1、4、7 日非缺失数为 1,750、1,542、1,296，乳酸第 1 至第 7 日由 855 降至 223。[17,21-23] XBJ-SCAP 随机分配 710 例重症社区获得性肺炎患者；本地衍生报告记录全分析集 675 例、符合方案集 617 例、全分析集中基线 SOFA≥2 的操作性 sepsis-like 人群 671 例、严格重叠人群 658 例；SOFA 第 0、4、8 日非缺失数为 703、628、610，WBC 为 704、634、614，CRP 为 579、503、467，28 日状态明确者 675 例。[18,24,25] 这些数字仅描述衍生清洗层和访视稀疏性。

## Research design and methods

### Two primary clinical tasks

| 项目 | 发病前主要任务 | 发病后主要任务 |
|---|---|---|
| 人群 | ≥18 岁；每次住院首个合格 ICU 记录；至少 12 小时可见历史；评价时尚未达到主标签 | 首次发病；入 ICU 时已发病者仅在首个可审计时点延迟进入，分层并左截断 |
| 事件与可用时间 | 疑似感染由微生物标本与系统抗菌药首次实际给药配对；采集先则给药须在 72 小时内，给药先则采集须在 24 小时内，感染时刻取较早者。无记录慢性器官功能障碍时 baseline SOFA=0；有记录者取入 ICU 前 24 小时最低可计算 SOFA；不可审计者不进入主风险集。滚动 24 小时最差 SOFA 相对基线增加至少 2 分，且位于感染前 48 小时至后 24 小时；首次满足时刻为发病事件。标签可用时间取配对较晚事件与所需 SOFA 数据在源系统可见或最终化时刻的最大值。[1,2] | 发病事件时刻为零点；恢复须连续 24 小时，可用时间为观察窗结束；恶化、死亡、出院和转院使用记录可用时刻 |
| 评价时点、历史和结局窗 | ICU 第 12 小时起每 12 小时评价；使用此前最多 24 小时、至少 12 小时的当时可用历史；估计未来 12 小时首次发病 | 发病或延迟进入后每 12 小时评价；主要结局时点为病程第 7 日，第 14 日作敏感性分析 |
| 重复、竞争和时间顺序 | 只分析首次发病；重叠评价窗保留，但每次 ICU 记录总权重为 1。发病前活着出 ICU、院内死亡、转院或失访为互斥终止；行政结束独立删失并作逆概率删失加权或界限检查。评价时点特征只使用此前已可见数据 | 首次发病与延迟进入分层；死亡、活着出 ICU 和转院为终止状态；恢复不由出院替代；同样只使用当时可见标签 |
| 估计对象与模型 | 给定历史，未来 12 小时首次发病累积发生函数；离散多项原因别风险转换为累积发生风险 | 第 7 日“生理恢复或活着出 ICU”有利状态集合占用概率，并分别报告两者；互斥离散多状态模型与 Aalen–Johansen 估计 |
| 评价与不确定性 | 12 小时 Brier 评分、绝对校准截距与斜率；精确率—召回率曲线下面积、提前量和假警报为次要指标；患者及医院层 bootstrap 95% 区间 | 第 7 日多类别 Brier 评分、有利状态绝对校准及患者和医院层 bootstrap；按首次发病和延迟进入分层，并报告有效转移数 |
| 合格标准 | 开发集与独立测试集均须满足 Brier 非劣 +0.01、校准斜率 0.80–1.20、绝对风险误差≤0.02，且无高严重度泄漏 | 同一标准 |

主标签之外仅设置两种敏感性定义：培养—抗菌药配对改为对称 ±24 小时；所有人使用感染前 24 小时最低可计算 SOFA，并把器官功能窗限制为前后各 24 小时。敏感性结果不替换主结果。泄漏审计覆盖发病后生理或治疗、尚不可用的培养或抗菌药、同一时间段行动、未来测量频率、跨拆分插补或标准化、患者及 ICU 记录跨集合、重叠窗口权重以及由结局决定的变量、时间网格或阈值。

### Mutually exclusive post-onset states

每 12 小时按固定优先级赋值：死亡，转院或无法继续观察，活着出 ICU，恶化或新器官衰竭，生理恢复，持续脓毒症。持续脓毒症指 ICU 内存活且未满足其他状态；生理恢复指相对发病参考 SOFA 下降至少 2 分并连续 24 小时无新恶化；恶化指相对此前 24 小时最低 SOFA 增加至少 2 分，或新启或升级血管活性药、有创通气或连续肾脏替代治疗。恢复事件时刻为观察窗起点，可用时间为窗结束。死亡和活着出 ICU 为吸收状态；转院或记录终止作为竞争终止。相同时戳无法排序时使用更高优先级，并作事件时间敏感性分析。

### Observational target, anchoring, and abstention

令锚定的潜在患者状态为 X_t，生理测量为 Y_t，治疗行动为 A_t，测量指示或强度为 M_t，基线为 B，数据库或医院为 S。目标是在实际照护与测量政策下估计联合分布 p(X_0:T,Y_0:T,M_0:T,A_0:T | B,S)，并由此得到风险、对齐后的状态占用与转移、锚点预测以及预设符号和滞后不变量。

每个维度至少有两个跨库锚点；首个锚点 loading 固定为 +1 并标准化尺度；非指定交叉载荷为 0 或预写稀疏模式；维度 K≤4，状态机制数≤3，滞后仅为 1 或 2 个冻结时间段；允许图不含同一时间段瞬时循环。使用 20 个固定随机种子后进行置换和符号对齐。只解释对齐后的状态占用、转移概率、锚点层预测及预设边的符号和滞后。

对于非随机缺失，主拟合使用显式测量过程的随机缺失或选择模型基线，并对未测生理值执行 pattern-mixture delta 为开发库标准差 −1、−0.5、0、+0.5、+1 的分析及选择模型临界点分析。每个对齐状态、医院和时间层报告行动概率与有效样本量；行动比例低于 5% 或高于 95%，或加权有效样本量低于名义样本的 20% 时，不估计治疗作用。状态或边在模拟恢复、20 个随机种子对齐、bootstrap 保留、外部符号一致、状态对齐或区间校准方面不合格时，按预设规则删除、合并或标为数据库或照护政策特异。

### Simulation and semi-synthetic recovery

月 7–10 在不读取临床最终测试结果的条件下，对每个核心情景至少重复 1,000 次，或运行至关键比例的 Monte Carlo 标准误≤0.02。生成情景包括正确指定、零边或独立状态、多余状态或过拟合、遗漏状态、错误滞后或观测模型，并交叉改变状态分离、切换率、1 或 2 个时间段滞后、政策反馈、隐藏混杂、非随机缺失、标签误差、访视密度、整院接口缺失和数据库差异。

| 恢复量 | 预设绝对标准 | 不满足时的处理 |
|---|---|---|
| 状态恢复 | 离散调整兰德指数或连续主要典型相关≥0.80；20 个随机种子对齐≥90% | 合并或删除状态，或采用线性或多状态模型 |
| 转移概率 | 主要允许转移平均绝对误差≤0.05；95% 覆盖率为 0.90–0.98 | 删除该转移或停止结构解释 |
| 预设符号和滞后 | 正确恢复率≥0.80 | 该边不进入共同结构 |
| 边检测 | 敏感度≥0.80 且错误发现率≤0.10 | 减小稀疏度或维度；仍不合格则限于预测 |
| 零边假结构 | 任一假边 95% 区间排除 0 的重复比例≤0.05 | 淘汰复杂候选，不再通过调整阈值恢复资格 |
| 错设时的错误高置信判断 | ≥80% 重复触发失配或弃权；错误结构高置信比例≤0.05 | 淘汰候选或仅解释已恢复不变量 |
| 概率校准 | 斜率 0.80–1.20；绝对概率偏差≤0.02 | 采用简单模型；重新校准不改变结构结论 |

### Independent held-out cross-database validation

在任何依据结局的选择之前，按医院合格体量四分位和接口完整性分层，以固定种子 20260717 对 eICU 医院 ID 进行哈希分配：30% 医院进入适配集，70% 医院进入独立保留的最终测试集。医院分区优先；测试医院不会因患者链接进入适配集。分区表、链接算法版本和校验值在查看测试结局前冻结。

若同一可链接患者跨越适配医院和测试医院，其全部记录从主要外部分析排除。同一分区内仅保留预先定义的首次合格住院及其首个合格 ICU 记录。揭示测试性能前，报告跨分区排除人数、比例、涉及医院数及仅用结局前信息计算的年龄、性别、入院类型或来源、首个评价时点生理负担和观测密度。敏感性分析采用测试集优先的患者—医院连通分量规则：混合分量从适配集删除相关患者记录，仅保留其预分配测试医院中的首次合格记录。

独立数据保管人在不释放模型性能的前提下检查支持。若排除后测试集少于 20 个合格医院，任一自由风险或转移参数少于 10 个事件或转移，共同锚点覆盖低于 70% 合格医院或 80% 患者，或跨分区排除超过原合格测试患者或主要事件的 10%，则启动预指定备份库；无可用备份时只作数据库层面的可迁移性描述。

冻结标签、共同变量、状态、预处理、数据可用时间、模型、超参数、阈值和评价代码后，最终测试依次报告：不利用外部测试集重新估计任何参数的主要外部验证；仅用适配集学习的结局时点特异校准截距和斜率；仅用适配集学习的观测模型更新，同时保持状态与转移固定。全模型重新拟合属于新的模型开发，不属于外部验证。

### Conditional trial observation mapping and independent alternative

普通语言路线依次为：核验试验资料语义；确定共同生理指标；冻结由阶段 II 观测模型得到的映射；在独立 eICU 测试集中检验映射；遮蔽试验治疗分组后检查试验数据支持；然后才比较随机分配组。两项试验分别分析，不合并。

首先核验阶段 II 已完成并冻结，且存在个体数据授权、原始 CRF/SAP 或数据持有人确认；核验随机化、分析集、中心或分层因素、第 7 日或第 8 日相对随机化和首剂的实际访视窗，以及死亡、住院、活着出院和转院语义。每项试验的共同变量集 C_r 只包括阶段 II 保留的生理锚点、在实际访视直接测得且构念与单位一致的变量；治疗、测量频率、SOFA、结局标签和事后状态不进入。每项试验至少需要两个锚点。

对 C_r，使用 MIMIC 开发集锁定的均值、标准差和第 1/99 百分位截断得到 Z_C。由冻结观测方程 Z_C=a_C+L_C X+e 对 L_C 作奇异值分解 L_C=UDV'，定义阶段 II 状态投影 P_state=V_1'X，以及可由试验观测直接计算的一维可观测状态摘要 P_obs=D_1^(-1)U_1'(Z_C−a_C)。奇异值并列时按预先固定的锚点字典序决定；符号在阶段 II 开发集中固定为与同日 SOFA 总分非负相关，使较高值表示较差状态。映射不使用试验治疗分组、试验结局或跨试验汇总数据；P_state 是模型状态在一维轴上的投影，P_obs 是由实测共同指标计算的摘要。

映射须先在独立 eICU 测试集相应第 7 或第 8 日窗口中满足全部标准：第一奇异轴解释 L_C Frobenius 能量≥50%；P_state 与 P_obs 相关≥0.70；相对 P_state 标准差的归一化平均绝对误差≤0.50；回归 P_state=α+βP_obs 时 |α|≤0.20 个标准差、β为 0.80–1.20，95% 区间覆盖率为 0.90–0.98；各共同锚点外部校准斜率为 0.80–1.20、标准化截距绝对值≤0.20。治疗标签遮蔽的试验数据还须有至少 80% 观测锚点位于冻结生理合理范围，并有至少 60% 访视时存活在院者能够由不少于两个实测锚点计算 P_obs。

映射合格时，死亡置于最差层；访视时存活在院者按 P_obs 从高到低排序；访视前活着出院置于最有利层。主要对比为与中心或分层随机化相容的概率指数或胜率。若共同锚点资格或映射标准不合格，但 SOFA、随机化、中心及生存和住院语义可核验，则使用独立 SOFA 复合状态端点：死亡最差，访视时存活在院者按 SOFA 从高到低排序，活着出院最有利。

EXIT-SEP 的目标分析集为随机分配的 1,817 例；已知结局的 1,760 例只能称完整结局子集。XBJ-SCAP 的目标分析集为随机分配的 710 例；若无法重建，则采用全分析集 675 例的改良意向治疗分析，并将符合方案集、sepsis-like 和严格重叠人群限于敏感性分析。存活在院但摘要或 SOFA 缺失时，在各多重插补数据集中使用治疗、中心、已确认的随机化前协变量和既往实际访视信息插补后重新计算端点，再以 Rubin 规则或聚类 bootstrap 合并；另作 ±0.5 和 ±1 个标准差、最佳/最差及临界点分析。转院或状态未知作界限分析。两个试验的主要状态端点构成 Holm 家族错误率 0.05 的检验家族；其他访视或模块采用探索性错误发现率，亚组只报告治疗与亚组的交互。访视稀疏仅支持访视特异或离散变化，不插值为连续轨迹。

### Secondary representation diagnostics

部分状态重建使用伪遮蔽平均绝对误差、均方根误差、对数评分和区间覆盖；未来轨迹使用连续排名概率评分、负对数似然、状态占用和结局校准。诊断按变量、状态、医院和观测密度分层，用于说明任务表现和失败分布。

## Key techniques and implementation

1. **按数据可用时间执行的标签引擎：** 同时输出事件时刻、标签可用时刻、来源表和时戳、主标签与敏感性标签及样本流，并强制特征在评价时点前可用。[1-3]
2. **双库可观测性审计：** 生成患者、ICU 记录、医院、跨院链接、评价时点、事件、转移、单位、接口、密度和缺失矩阵，据预设规则冻结时间网格、模块、维度、状态机制数和参数数。
3. **变量角色隔离：** 每个字段只有一个主要角色；标签派生副本隔离并设置时间滞后；器官支持不作为生理锚点。
4. **简单模型先行：** 先完成竞争风险、多状态、Aalen–Johansen 和线性状态空间模型，再评价至多一个复杂候选。
5. **锚定与不变量：** 固定载荷、尺度、符号、维度、允许图和滞后；多随机种子对齐后只解释不变量。
6. **缺失与照护政策支持分析：** pattern-mixture delta、选择模型临界点、接口压力测试和行动重叠及有效样本量共同确定何时不作解释。
7. **医院优先的外部数据隔离：** 医院哈希、跨分区患者排除、测试集优先连通分量敏感性、权限和校验值由独立数据保管人控制。
8. **冻结的试验观测映射：** 各试验使用合格共同锚点和冻结观测载荷的一维映射；先评价外部忠实度，再进行治疗比较。
9. **不确定性与多重性：** 患者及医院 bootstrap、模拟标准误、多重插补、delta 与临界点分析、中心分层概率指数和 Holm 校正均预先编码。
10. **阴性对照与失败结果：** 使用临床预裁定的时间反转和阴性对照；发布标签、审计、共同变量、缺失和替代分析记录。[16]

## Evidence chains

### Evidence chain: 可用性时钟、风险集与互斥病程

- **Input:** Sepsis-3、培养或抗菌药与 SOFA 时戳、死亡、出院和转院事件、公共 ICU 数据字典及待执行的双库可观测性审计。[1-10]
- **Method / analysis / processing:** 主标签与两种敏感性标签；事件时刻和标签可用时刻；12 小时动态评价；首次发病与延迟进入；互斥状态、竞争事件、患者权重和泄漏检查。
- **Output:** 可执行的未来 12 小时首次发病累积发生风险队列、第 7 日多状态队列、标签差异矩阵和泄漏报告。
- **Supports:** 目标 1，以及候选动态系统表征覆盖发病前、首次发病、发病后和结局的可审计边界。

### Evidence chain: 数据支持、锚定与模拟恢复

- **Input:** 待执行的双库锚点、接口和事件审计，知识先验，三类过程角色，以及正确、零边、过拟合和错设生成情景。
- **Method / analysis / processing:** 共同模块和复杂度标准；锚定载荷、尺度、图和滞后；至少 1,000 次 Monte Carlo 重复；非随机缺失、政策反馈、接口缺失和数据库差异压力情景；恢复、错误发现、覆盖和错误高置信判断的绝对标准。
- **Output:** 一个满足全部标准的受限复杂候选，或预设多状态、线性或仅预测模型，并附删除、合并和不作解释清单。
- **Supports:** 目标 2 和 3 中可估计不变量的识别范围。

### Evidence chain: 两项主要任务与两项次要诊断

- **Input:** 冻结队列和状态、符合分析条件的模型、开发与时间外及医院外切分和预设指标。
- **Method / analysis / processing:** 未来 12 小时首次发病累积发生风险、第 7 日状态占用、适当评分、校准、聚类 bootstrap、伪遮蔽、轨迹诊断、标签与缺失敏感性、行动及观测消融和阴性对照。
- **Output:** 两个主要任务的 Brier 评分、校准和状态概率，两个次要诊断的评分与覆盖，以及按中心、亚组和观测密度展示的失败分布图。
- **Supports:** 目标 3 的患者—时间状态任务效度及阶段 II 合取成功标准。

### Evidence chain: 医院优先的独立外部验证

- **Input:** 开发方案冻结包、按医院预分配的 eICU 适配集和独立测试集、跨院患者链接审计、共同锚点和预设阈值。
- **Method / analysis / processing:** 主要分析排除跨分区患者；同分区保留首次合格 ICU 记录；测试集优先连通分量敏感性；依次报告不更新参数的验证、仅用适配集的校准更新和观测模型更新；评价患者和医院聚类、对齐、测量一致性及失败分布。
- **Output:** 跨分区排除数量与结局前特征、数据支持判定、不更新参数和有限更新结果，以及稳定、数据库特异和不作解释项目清单。
- **Supports:** 目标 3 及阶段 II 的独立保留数据库外部验证。

### Evidence chain: 条件性试验观测映射或独立临床状态分析

- **Input:** 通过并冻结的阶段 II 观测方程；每项试验第 7 或第 8 日的合格共同锚点；EXIT-SEP 1,817 例和 XBJ-SCAP 710 例的条件性个体数据；原始 CRF/SAP、中心、时序及生存和住院语义。[17,18,21-25]
- **Method / analysis / processing:** 各试验分别完成资料语义和共同锚点核验；冻结一维映射；在 eICU 独立测试集中检验相关、归一化平均绝对误差、校准和覆盖，并在遮蔽治疗分组的试验数据中检查支持；映射合格时分析死亡优先排序的一维可观测状态摘要，不合格时分析独立 SOFA 复合状态端点；保留分析集、中心、多重插补、敏感性分析、Holm 校正和亚组交互规则。
- **Output:** EXIT-SEP 第 7 日与 XBJ-SCAP 第 8 日分开的访视特异一维可观测状态摘要扰动估计、独立临床状态差异，或资料语义不足的停止记录，并列出不可估计内容。
- **Supports:** 目标 4；只有观测映射合格分支支持随机分配对该访视一维可观测状态摘要的有限扰动。

## Required analyses and evidence

阶段 II 主张前须完成：月 3 资源确认与具名角色；月 6 双库可观测性审计和版本及校验值冻结；主标签、两种敏感性标签、双时钟、12 小时动态评价、第 7 日状态、延迟进入和竞争事件的单元测试；变量角色及双用副本隔离证明；简单模型、Monte Carlo 模拟、零边和错设判断及预设替代记录；非随机缺失和行动重叠分析；两项主要任务与两项次要诊断的适当评分、绝对校准、覆盖、警报负担和聚类区间；医院分配表、跨分区排除表、结局前特征、连通分量敏感性、权限日志及冻结校验值；月 24 合取标准逐项结果。

阶段 III 启动前还须获得个体数据分析授权，核验原始 CRF/SAP、随机化、中心、实际访视时序及生存和住院语义；处理 EXIT-SEP 57 例未知状态与 XBJ-SCAP 随机全集和全分析集差异；对每项试验冻结共同变量、单位、访视窗、一维映射和分支标签；在治疗组比较前锁定概率指数并列规则、多重插补合并推断、中心处理、Holm 检验家族及亚组交互。

最接近工作综合已更新至 2026-07-17，可支持保守定位。在提出全球首次、专利不存在或临床数字孪生主张之前，仍需系统综述、引文网络、专利和非英语数据库核验。[38]

## Expected outputs, falsification criteria, and interpretations

### Planned outputs

1. 双时钟标签、12 小时风险集、互斥发病后状态、双库支持规范和可重复代码。
2. 变量角色、共同概念、接口、缺失、医院优先拆分和跨院患者排除审计。
3. 简单模型、模拟恢复和错误高置信判断基准，以及至多一个受限复杂候选或预设替代结果。
4. 两项主要任务和两项次要诊断的开发、时间外、医院外与独立数据库结果，包括校准、不确定性、对齐和失败分布图。
5. 条件满足时分别报告两项试验的访视特异一维可观测状态摘要分析，或与阶段 II 独立的 SOFA 复合状态分析；资料语义不足时报告停止原因。

### Falsification criteria

阶段 II 假设在以下任一情形下被相应证据否定：结果受后录入标签、同一时间段未来行动、未来测量频率或跨拆分插补驱动；两库事件、转移、医院或锚点支持不足；状态、转移、覆盖、零边错误高置信判断或错设时弃权不合格；缺失敏感性改变解释或行动重叠不足；不更新参数的外部任务表现、对齐或符号稳定性不合格。阶段 III 的映射解释在共同锚点、单位、时序、低维性、相关、误差、校准或覆盖任一项不合格时被否定；试验新状态端点在随机化、中心、访视或生存和住院语义不可核验时停止。

### Interpretation matrix

| 观察结果 | 允许解释 |
|---|---|
| 简单模型有用而复杂候选恢复失败 | 获得多状态或预测基准及复杂模型失败证据 |
| 模拟恢复合格而不更新参数的外部验证失败 | 候选在开发数据和预设生成情景内可恢复，但跨数据库稳定性不足 |
| 主要外部验证失败而适配后分析成功 | 适配后可迁移性或观测模型差异 |
| 两项主要任务合格但状态或边不作解释 | 任务层面的预测表征 |
| 试验观测映射合格且组间不同 | 该试验、实际访视的一维可观测状态摘要受到随机分配的有限扰动 |
| 试验观测映射不合格而独立 SOFA 组间不同 | 该试验的独立次要临床状态差异 |
| 阶段 II 全部合取标准满足 | 候选动态系统表征获得审计、恢复、任务和独立外部支持 |

## Contribution, innovation, impact, application, and closest-work comparison

实际增量有三层。输入层连接可比的未发病动态评价时点、首次发病和互斥发病后状态；转换层分离患者状态、治疗行动和观测过程，并以锚定不变量、模拟恢复和医院优先分区限制解释；输出层把独立外部验证与具有映射失败分支的访视稀疏随机对照试验次要分析置于有顺序的证据路线中。若执行成功，项目可形成整合、验证和基准资源价值；不构成新算法或全球首次。

代表性最接近工作包括：脓毒症日级多状态 Markov 与 SOFA 轨迹研究；动态表型、状态空间模型与器官交互图；数字孪生和模型预测控制原型；离线强化学习及跨库和时间构造研究；在随机对照试验中开展的表型—治疗次要分析。[26-37] 这些工作使各单项模块不具新颖性。当前方案的条件性差异在于把发病前、首次发病、发病后和结局置于同一双时钟设计中，分离状态、行动和观测过程，先检验绝对恢复，再检验独立外部稳定性，最后才考虑试验观测映射。该完整组合缺口的证据仍为低至中等置信度。[38]

## Title and positioning claim-support table

| Title or positioning claim, written at its supported scope | Contribution frame / claim type | Existing implementation that supports it | Supporting evidence-chain output | Literature or existing-result basis | Actual increment, or `none` | Support status |
|---|---|---|---|---|---|---|
| “脓毒症全病程候选动态系统表征”是计划研究对象 | integration / validation | 双时钟、首次发病任务、互斥发病后状态和三过程分离 | 可用性时钟、风险集与互斥病程；数据支持、锚定与模拟恢复 | Sepsis 基础 [1,2]；多状态和轨迹近邻 [26,27] | 全病程输入、转换和输出连接 | supported |
| “计划性跨数据库检验”指独立保留数据库上不更新参数的阶段 II 验证 | validation / benchmark | 医院优先适配集和测试集、跨分区患者排除及不更新参数验证 | 医院优先的独立外部验证 | 公共数据库与受限共同变量 [5-10]；外部验证近邻 [12,34] | 独立保留测试、患者不跨集合和失败分布图 | qualified |
| 阶段 III 是访视稀疏随机对照试验的条件性次要分析 | validation / translational | 资料语义核验、冻结一维观测映射、独立 SOFA 分支和分试验估计对象 | 条件性试验观测映射或独立临床状态分析 | EXIT-SEP、XBJ-SCAP 及衍生材料限制 [17,18,21-25]；RCT 次要分析近邻 [28] | 将观测映射前置为预设合格标准并设置独立替代分析 | qualified |
| 一维可观测状态摘要的随机化扰动只在映射合格分支成立 | validation | 冻结观测载荷、eICU 外部忠实度和校准检验、死亡优先排序概率指数 | 条件性试验观测映射或独立临床状态分析 | 动态表型及 RCT 近邻 [28,29]；本项目尚无结果 | 从阶段 II 观测模型到实际试验访视的确定性桥接 | qualified |
| 贡献是条件性的整合、验证和基准资源 | editorial_repositioning / integration / resource | 双库审计、角色分离、模拟恢复、独立外部验证和预设替代分析 | 前四条证据链的联合输出 | 模块近邻 [26-37]；有界更新 [38] | 条件式五层组合与可审计证据路线 | supported |
| 截至 2026-07-17 的有界检索尚未找到完整五层组合的代表性先例 | scientific novelty | 有界检索未建立完整合取工作 | 最接近工作比较及五条证据链计划 | 有界检索 [38] | `none` until execution and broader search | qualified |
| 当前方案具有全球科学或方法首创性 | scientific_discovery / method | 无 | 无 | 模块已有先例 [26-37]，负向检索有限 [38] | `none` | unsupported |
| 当前已形成因果网络、可控系统、数字孪生、临床工具或药物平台 | scientific / translational / practical | 无 | 无 | 因果和控制边界 [14,19,32-37] | `none` | unsupported |

## Feasibility, resources, risks, alternatives, and stop conditions

### Feasibility and resources

最低团队配置包括具名重症临床与表型负责人、纵向统计负责人、系统辨识负责人、数据工程负责人、模型实现者和独立测试数据保管人；当前只有职责定义，没有可核验的人员承诺。计算范围限于两个主数据库、维度 K≤4、状态机制数≤3、两项主要任务、两项次要诊断和至多一个复杂候选。动物实验、随机对照试验实施、因果机制和控制不属于 24 个月成立条件。

公共数据库存在和版本已经核验，但团队访问凭证、数据使用协议、可运行提取、确切队列支持、人员工时、候选模型、模拟恢复、预测、外部验证和试验新分析均未核验或尚未生成。EXIT-SEP 与 XBJ-SCAP 的现有本地材料只是衍生清洗或验证报告，不能替代个体数据分析授权、原始 CRF/SAP 或数据持有人对随机化、中心、访视和结局语义的确认。

### Working assumptions

1. 月 3 前能够获得两个可承担预定角色的 ICU 数据库，并具名所有关键职责；若不能，停止 24 个月双库路线。
2. 月 6 审计能够在至少一种预写时间方案下支持发病前风险集、发病后互斥状态、共同锚点、医院分区和参数上限；12 小时方案不足时，只能在模型拟合和测试数据访问前改为 24 小时或事件时间。
3. 锚定方式、尺度、维度、状态机制数、允许图和滞后足以把可恢复不变量与任意潜变量编号或旋转坐标区分；模拟生成情景只能检验预设生成族，不能证明真实系统结构。
4. 显式建模测量过程和敏感性分析能够描述部分非随机缺失风险，但不能识别非随机缺失的真实机制。行动重叠不足时，相关关系只适用于观察到的照护政策。
5. 有界检索能够支持保守的整合与验证定位，但不能支持全球不存在、首次、专利空白或新算法主张。

### Limitations and boundary conditions

EHR 脓毒症发病时刻不是唯一真值；标签定义、基线、时间窗、数据可用时间和医院接口会改变风险集与结果。未来信息、同一时间段行动、未来测量频率、跨拆分插补、患者或 ICU 记录跨集合以及结局驱动的变量或阈值都可能造成泄漏。高严重度泄漏若未清除，则不能进入独立外部测试。

状态、转移和边只有在锚定、随机种子对齐、模拟恢复、区间覆盖、错误发现、错误高置信判断、外部符号一致和状态对齐均满足预设标准时才可解释。两项主要任务或外部验证失败时，次要诊断、适配后结果或阶段 III 结果不能补足阶段 II。主要外部验证必须使用预先独立保留的测试医院且不重新估计参数；适配集校准更新、观测模型更新和全模型重新开发须分别标识。

非随机缺失、低行动重叠、整院接口缺失、跨院患者排除和数据库差异会限制可解释范围。若患者排除使医院、事件、转移或锚点支持低于预设标准，或排除超过测试患者或主要事件的 10%，则采用预指定备份库；无可用备份时只报告数据库层面的可迁移性描述。

阶段 III 的两项试验数据、原始资料语义、共同锚点及观测映射目前均未核验。EXIT-SEP 与 XBJ-SCAP 的人群、访视、锚点和估计对象须分别处理，不能合并；访视稀疏不能插值为连续轨迹。若共同锚点不足、单位或时序不一致、外部映射忠实度不合格，或需依据试验治疗组重新估计权重，则采用独立 SOFA 复合状态端点。若随机化、中心、关键访视或生存和住院语义不可核验，则停止新状态端点，只复现原终点或报告数据审计。

观察性数据和预测表现不能识别真实因果网络、治疗因果效应、反事实策略、机制、中介、控制或数字孪生。即使试验观测映射合格，随机化也只支持分配组对实际访视一维可观测状态摘要的有限扰动，不能验证未测潜在动力学、转移边、完整观测模型或整个阶段 II 表征。独立 SOFA 分支只支持试验特异临床状态差异。当前结果不能作为临床决策工具、药物平台或无条件国际临床推广依据；SSC 2026 对未获当地监管批准辖区使用 XueBiJing 的建议仍保持谨慎。[4]

### Risks, alternatives, and stop conditions

| 风险 | 触发条件 | 预设替代方案或停止后果 |
|---|---|---|
| 数据访问或支持不足 | 月 3 无两个可访问数据库；月 6 事件、锚点或医院不足 | 启用预指定备份库，或改为 24 小时或事件时间并删除不获支持的模块；仍不足则停止跨数据库系统端点 |
| 跨院患者破坏隔离或支持 | 患者跨适配集与测试集；排除后医院、事件、转移或锚点不足，或排除比例>10% | 主要分析排除其全部记录；执行测试集优先连通分量敏感性；启用备份；不得移动测试医院或让患者跨集合 |
| 标签或时间泄漏 | 结果受后可用信息、同一时间段行动、未来测量或跨拆分处理驱动 | 修正按数据可用时间的处理并删除变量；高严重度项目未清除则不开放测试集 |
| 状态不可恢复或出现假结构 | 状态恢复、转移误差、覆盖率、错误发现率、零边或错设标准不合格 | 删除或合并状态和边，采用多状态、线性或仅预测模型；复杂候选停止结构解释 |
| 非随机缺失或行动重叠不足 | delta 或临界点分析改变解释；行动比例<5%或>95%，或加权有效样本量<20% | 报告敏感区间，合并或删除相关状态和边，并限于照护政策特异描述 |
| 独立外部验证失败 | 不更新参数时的适当评分、校准、对齐或符号稳定性不合格 | 分开报告校准更新、观测模型更新和新的模型开发；不得称为冻结模型的跨数据库成功 |
| 试验共同锚点或观测映射失败 | 少于两个锚点；单位、时序、低维性、相关、误差、校准、覆盖或试验支持任一项不合格 | 自动采用死亡优先排序的独立 SOFA 复合状态端点，不将其解释为阶段 II 表征的扰动或验证 |
| 试验核心语义不足 | 随机化、中心、关键访视、生存、住院或出院语义不可核验 | 停止新状态端点，只复现原终点或报告数据审计 |
| 时间超限 | 月 12 无合格复杂候选；月 20 未冻结；月 24 无独立外部结果 | 分别停止复杂候选、不开启最终测试，或判定阶段 II 最低端点未完成并保存当前简单结果 |
| 最接近工作过度外推 | 需要首次、专利或全球不存在主张 | 增加系统综述、引文网络、专利和非英语数据库检索；当前只保留有界、条件性的增量定位 |

阶段 I–II 必须在 24 个月内完成。阶段 III 位于最低交付之外，只有阶段 II 成功且相应试验数据、资料语义和观测映射满足预设条件时才开展；任何试验结果都不能绕过或补足资源、恢复、主要任务或独立外部验证要求。若未来取消发病前—首次发病—发病后—结局连续体，把项目改为普通预测，替换公共 ICU 与随机试验核心证据基础，或改变患者—时间状态及状态转移这一主要推断单位，则须建立新的研究构想，而不是沿用本版本。

## References

1. Singer M, Deutschman CS, Seymour CW, et al. The Third International Consensus Definitions for Sepsis and Septic Shock (Sepsis-3). JAMA. 2016;315:801-810. doi:10.1001/jama.2016.0287.
2. Seymour CW, Liu VX, Iwashyna TJ, et al. Assessment of Clinical Criteria for Sepsis. JAMA. 2016;315:762-774. doi:10.1001/jama.2016.0288.
3. Subtle variation in sepsis-III definitions markedly influences predictive performance within and across methods. 2024. PMCID: PMC10803347.（页面和摘要层核验，partial。）
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
23. EXIT-SEP participants clean/SAP subset/field-coverage audit workbooks. 项目本地只读 QC 材料.（本任务未读取参与者层工作簿。）
24. XBJ-SCAP 数据集构建验证报告. 项目本地衍生验证材料，2026-07-13；rct-data/xbj_scap_dataset_validation_report.md.（非原始 EDC/CRF 审计。）
25. XBJ-SCAP participants clean/reproduction-transportability QC workbooks. 项目本地只读 QC 材料.（本任务未读取参与者层工作簿。）
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
38. 脓毒症复杂系统模型：最接近工作刷新. 项目本地有界检索综合，检索截止 2026-07-17；closest-work-update-v001.md.（partial；不是系统综述或全球不存在性证明。）
