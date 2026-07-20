---
schema_version: research-idea.v3
plugin_version: 0.9.0-preview.3
artifact_id: idea-dossier-I01-001-v050
workflow_id: RID-SEPSIS-CSM-20260717-001
idea_id: I01-001
version_id: v050
path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v16/idea-dossier-v050.md
parent_idea_ids: []
based_on:
  - artifact_id: idea-dossier-I01-001-v003
    version: v003
    path: tests/idea-test-0.9.0-preview.1/0.9.0-preview.1/03_ideas/nodes/I01-001/dossiers/idea-dossier-v003.md
  - artifact_id: editorial-repair-writer-brief-I01-001-r102
    version: r102
    path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/baseline-current/editorial-repair-writer-brief-r102.yaml
  - artifact_id: protected-content-register-I01-001-v004-r004
    version: r004
    path: tests/idea-narrative-forward-0.9.0-preview.3/run-001/inputs/protected-content-register-v004.yaml
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

# 脓毒症全病程候选动态系统表征：24 个月跨数据库构建与检验计划

## Title, summary, audience, and positioning

- **Title:** 脓毒症全病程候选动态系统表征：24 个月跨数据库构建与检验计划
- **One-sentence complete-Idea summary:** 本研究拟在 24 个月内以文献和专家知识约束候选结构，利用两个人群、事件与变量支持须先核验的纵向公共 ICU 数据库，构建覆盖可比未发病在险时段、首次发病、发病后互斥状态演化和结局的脓毒症候选动态复杂系统表征，以未来 12 小时首次发病累积发生风险和第 7 日有利状态占用概率为两项主要任务，通过预设生成情景中的模拟恢复检验和不重新估计任何参数的独立外部验证形成可审计证据，目标是支持一篇或多篇高水平论文而非仅产出预测工具；主体研究达到标准后，可在科学前提满足时按试验分别开展次要分析。
- **Primary audience:** 重症医学、临床流行病学、纵向统计、系统辨识、医学 AI 与转化研究共同体；当前不预设具体期刊。
- **Positioning and contribution frame:** 研究主体是全病程候选复杂系统表征的构建、恢复检验、临床任务检验和跨数据库验证，预期价值在于条件性的证据整合、验证以及可复用的基准与资源；各单项模块已有代表性先例，当前工作仍是计划，不是现成模型或已完成验证。[26-38]

## Structured abstract

- **Background and gap:** Sepsis-3 为感染相关器官功能障碍提供操作基础，但疑似感染配对、基线、时间窗和标签可用时刻会改变电子健康记录中的发病标签。[1-3] 现有纵向多状态、动态表型和跨数据库工作尚未回答：一个覆盖可比较未发病时段、首次发病、发病后演化和结局的候选复杂系统表征，能否同时获得模拟可恢复性、临床任务效度和独立跨数据库稳定性的前瞻性证据。[26-38]
- **Objective and hypothesis:** 目标是在 24 个月内完成阶段 I–II，构建并计划检验一个以患者—时间状态及状态转移为推断单位、由知识约束且能表达不确定性的候选全病程表征；核心假设是，经过双数据库支持核验、参数锚定和绝对模拟恢复检验后，至多一个受限复杂候选可在时间外、医院外和未触碰数据库外数据中维持预设校准、状态对齐和结构稳定性。
- **Approach:** 发病前主要任务估计每 12 小时评估点之后 12 小时内的首次发病累积发生风险，发病后主要任务估计第 7 日有利状态占用概率；简单竞争风险、多状态和线性状态空间模型先行，复杂候选须通过预设生成情景中的恢复与错误结构控制标准，随后在按医院隔离的外部数据中先应用冻结模型而不重新估计任何参数。主体研究达到标准后，仅在各试验的科学前提满足时开展彼此独立的次要分析。[17,18,21-25]
- **Expected result:** 计划产物包括可执行的标签与时钟协议、双数据库变量和支持记录、互斥状态定义、模拟恢复与弃权记录、两项主要任务和两项次要表示诊断、不重新估计参数的外部验证结果，以及清楚说明未达到标准对象、判据、分层和科学后果的表图；这些均尚未生成。
- **Contribution and impact:** 若阶段 II 的数据支持、模拟恢复、主要任务评分与校准、泄漏清除、外部验证、状态对齐和结构稳定标准同时达到，研究将提供一个可审计的全病程候选复杂系统表征及其跨数据库证据，并形成可复用的基准、资源和失败记录，为后续高水平论文提供科学基础。

## Background, current state, gap, significance, and rationale

### Background

脓毒症随时间形成，并与治疗和检测行为共同演化。Sepsis-3 将其界定为感染所致失调宿主反应引起的危及生命器官功能障碍，研究中常以相对基线 SOFA 增加至少 2 分操作化，但这一规则不产生唯一的电子健康记录发病时刻。[1,2] MIMIC-IV、eICU-CRD、HiRID 和 AmsterdamUMCdb 提供纵向生命体征、实验室、治疗和结局数据；纵向多状态、动态表型、状态空间模型、跨数据库验证以及随机试验中的表型次要分析也已有代表性研究。[5-10,26-37]

### Current state

合理改变疑似感染配对、SOFA 基线或观察窗会改变病例界定与预测表现，临床事件发生时刻和标签在数据库中可计算的时刻也可能不同。[3] 同时，治疗随病情变化，测量频率和缺失反映照护行为；如果不区分患者生理状态、治疗行动、观测过程和标签生成过程，模型可能把记录方式或未来信息误作病程结构。[14-16]

### Gap

仍待回答的科学问题不是能否再训练一个脓毒症预测器，而是能否在同一纵向患者系统中界定可比较的未发病在险时段、首次发病、发病后互斥状态和结局，并用预先规定的恢复标准、两项临床任务和完全隔离的外部数据库共同检验其可解释不变量与结构稳定性。这个问题要求证据从数据边界一直连接到跨数据库表现，而不能由单一预测分数替代。

### Significance

回答该问题可区分能够跨医院和数据库保持的患者—时间状态信息，与仅反映特定接口、测量政策或数据处理方式的模式。无论复杂候选是否达到标准，研究都将留下可执行标签、支持审计、基准模型、外部验证和明确的阴性结果，从而提高脓毒症纵向建模的可重复性、可证伪性和证据可审计性，并为一篇或多篇高水平论文提供实质内容。

### Rationale

研究因此以知识约束限定候选结构，以未来 12 小时首次发病风险和第 7 日有利状态占用概率连接发病前与发病后病程，以预设生成情景检验可恢复量，再把冻结模型应用于未参与开发的医院和数据库。只有这些阶段 I–II 证据形成后，才考虑用彼此独立的试验次要分析检验实际访视中可观测临床状态是否随随机分配而不同。

## Research question, objectives, and core hypothesis

### Primary research question

能否构建并验证一个以脓毒症为中心、知识约束且能表达不确定性的 ICU 患者候选动态复杂系统表征，使其覆盖可比较的未发病在险时段、首次发病、发病后状态演化和结局，在患者与医院聚类得到尊重的前提下显示跨数据库状态与结构有效性，并在不把预测等同于因果的情况下为后续有限随机化比较提供基础？

### Objectives

1. 在 24 个月内完成阶段 I–II，以文献和专家知识约束候选结构，使用纵向公共 ICU 数据开展系统辨识、跨数据库验证与全病程状态表征，并形成可审计证据及一篇或多篇高水平论文的研究基础，而不是把交付收缩为预测工具。
2. 锁定实时可实施的主要 Sepsis-3 标签、标签可用性时钟、首次发病风险集、发病后互斥状态和竞争事件，并以两种合理标签定义进行敏感性分析。
3. 由双数据库样本、事件、转移、医院、共同锚点和接口支持决定共同模块、时间方案与复杂度上限，以预设生成情景检验可恢复性，并在第二数据库隔离适配医院与未触碰最终评价医院，检验两项主要临床任务和两项次要表示诊断。
4. 主体研究达到标准后，仅在相应试验个体数据可用且核心试验语义可核验时，按试验分别开展预先规定的次要临床状态分析。

### Core hypothesis

若两个数据库对共同生理锚点、事件和转移提供足够支持，候选模型的锚定、尺度、状态数和滞后得到预先锁定，且复杂候选在正确指定、零边和错设生成情景中达到绝对恢复标准，则部分对齐后的状态占用、转移概率、锚点预测以及预设依赖关系的符号和滞后可在未触碰外部数据库中维持预定义稳定性。五条证据链分别闭合到数据边界、可恢复不变量、任务效度、跨数据库运输和条件性试验输出；较好的预测表现本身不足以替代恢复、主要任务或外部验证证据。

## Research content and work packages

### Twenty-four-month minimum and dated gates

阶段 I–II 必须在 24 个月内完成；阶段 III 位于最低交付之外。下表中的负责人签署是计划所需角色，不表示当前已有具名人员承诺，外部最终评价结果在月 18–20 的冻结包签署前由独立数据保管人保持不可访问。

| Time | Required deliverable | Planned disposition |
|---|---|---|
| 月 0–3 | MIMIC-IV v3.1 与 eICU-CRD v2.0 的团队访问、DUA、存储和算力确认；临床、统计、系统辨识、数据工程和独立保管角色具名；预指定 HiRID 或 AmsterdamUMCdb 之一作为备份 | 确认两个可承担研究角色的数据库及完整人员责任 |
| 月 4–6 | 冻结双数据库队列流、事件与转移、医院、跨院患者、共同锚点密度、接口、缺失、主标签、双时钟、多状态、医院优先拆分、时间方案、共同模块和参数上限 | 在任何模型拟合和外部结果访问前完成数据支持与方案锁定 |
| 月 7–12 | 完成竞争风险、多状态和线性状态空间基线，以及 Monte Carlo 与半合成恢复检验；至多保留一个复杂切换或非线性候选 | 按预设恢复结果保留复杂候选或降级到较简单表示 |
| 月 13–18/20 | 完成开发数据库内部、时间外和医院外验证，并冻结标签、锚点、预处理、模型、超参数、允许更新、指标和外部判据 | 形成带校验和的冻结包；月 20 后不按最终评价结果修改 |
| 月 21–24 | 在第二数据库未触碰评价医院完成不重新估计任何参数的外部验证，并分开报告只重估结局校准参数和只重估观测方程的结果 | 按全部预设标准共同判定阶段 II，并封存未达到标准的对象及其科学后果 |
| 24 月后 | 依赖阶段 II 成功、相应试验个体数据可用及核心试验语义可核验的分试验次要分析 | 不计入或补足阶段 II 的最低交付与成功判定 |

### Conjunctive minimum success definition

阶段 II 的“计划跨数据库候选系统表征成功”必须同时满足：

1. 两个数据库均可构造主要发病前风险集与发病后状态队列，并达到冻结的事件、转移、医院和共同锚点支持下限；
2. 复杂候选若被保留，须通过正确生成器、零边生成器和核心错设情景的全部绝对标准；若自动降级，只有相应线性或多状态表示可获支持；
3. 两项主要任务在开发与时间外验证中，Brier 评分或多类别 Brier 评分相对最强简单基线的差值上侧 95% 界不超过 +0.01，校准斜率为 0.80–1.20，校准截距对应的绝对风险误差不超过 0.02；
4. 泄漏清单没有未解决的高严重度项目，所有特征遵循标签可用时刻，患者、医院、重复住院和插补均不跨拆分；
5. 医院优先外部拆分后仍有至少 20 个合格最终评价医院，并满足外部事件和转移支持；冻结模型不重新估计任何参数时，两项主要任务达到 Brier 评分非劣标准，对齐后主要状态相关或一致性系数至少为 0.70，预设结构符号一致率至少为 0.80。

依赖数据支持的阈值只能在月 6 前根据临床容许误差、开发数据库自助法和未接触外部结果的先导模拟写入登记表；本方案给出的硬标准只能收紧，不能放宽。适配医院中学得的有限更新必须与冻结模型结果分开报告，不能替代冻结模型失败；阶段 III 永不计入或补足上述合取成功。

### Work packages and minimum route

| Work package | Months | Main work | Gate-linked output |
|---|---:|---|---|
| WP1：标签、队列和双数据库支持 | 0–6 | 访问与版本、样本流、双时钟、变量角色、跨院患者、时间网格和接口核验 | 可执行风险集、多状态、医院优先拆分和共同模块，或预指定降级记录 |
| WP2：知识结构、基线与绝对恢复 | 3–12 | 候选图、锚定限制、竞争风险、多状态、线性基线、Monte Carlo 和半合成模拟 | 至多一个达到预设标准的复杂候选，或自动降级模型 |
| WP3：主要任务与次要诊断 | 8–18 | 首次发病 12 小时累积发生风险、第 7 日状态占用、伪遮蔽重建、未来轨迹诊断、缺失非随机、重叠和消融 | Brier 评分、连续排名概率评分、校准、覆盖、泄漏和弃权记录 |
| WP4：隔离的跨数据库检验 | 14–24 | 冻结包；医院级适配与最终评价；跨分区患者主要剔除；冻结模型、仅校准和仅观测方程更新 | 未触碰外部结果、剔除审计和按失败对象命名的阴性结果表图 |
| WP5：条件性阶段 III | 24 月后 | 在共享前提满足后，按试验分别执行预先冻结的次要分析 | 两个试验分开报告的次要分析或停止记录；不属于阶段 II 成功 |

固定顺序为：资源和双数据库支持核验 → 标签、状态和医院拆分锁定 → 竞争风险与多状态基线 → 线性状态空间模型 → 绝对模拟恢复检验 → 至多一个复杂候选 → 两项主要任务和两项次要诊断 → 开发冻结 → 未触碰外部验证 → 条件性试验分析。任何未达到标准的环节都沿预先规定的路线降级，不能以试验结果或更复杂模型绕过。

## Data, materials, and existing evidence base

### Current verified-resource versus prospective-gate status

| Resource or result | Current evidence | Status | Prospective requirement / no-go |
|---|---|---|---|
| MIMIC-IV v3.1 与 eICU-CRD v2.0 的公开存在、版本和文献 | PhysioNet 和原始数据库论文提供稳定 DOI 与版本记录。[5,6] | 已由公开资料核验 | 当前证据只确认数据库存在和版本 |
| 团队访问凭证、DUA、下载与存储、确切提取版本和校验和 | 当前材料没有已完成凭证或提取证据 | 尚未核验 | 月 3 前确认两个可承担研究角色的数据库 |
| 双数据库实际样本、事件、转移、医院、跨院患者、共同锚点密度和接口支持 | 尚未运行项目队列核验，官方规模不能替代项目计数 | 尚未生成 | 月 6 前形成冻结记录 |
| EXIT-SEP 与 XBJ-SCAP 本地验证报告 | 两份报告日期为 2026-07-12/13，记录工作簿构建、关键非缺失和复现/QC；不是独立同行评审或原始审计。[22,24] | 项目本地衍生材料 | 只能支持稀疏访视和字段缺口描述 |
| 随机试验个体数据授权、原始 CRF/SAP、随机化、中心、实际访视相对首剂时序和生存、住院、出院语义 | 现有衍生报告没有完成这些原始语义证明 | 尚未核验 | 每项试验分析启动前核验 |
| 阶段 II 与两项试验的共同生理锚点、单位和实际访视映射 | WBC、CRP 等候选访视信息可见于衍生材料，是否属于冻结阶段 II 锚点及跨源语义和单位一致尚未证明，D-dimer 单位等仍有缺口 | 尚未核验 | 按试验形成变量、单位和时窗核验记录 |
| 所需团队角色 | 临床与表型、纵向统计、系统辨识、数据工程、模型实现和独立数据保管职责已定义 | 角色规范已确定 | 这不表示已有人员承诺 |
| 当前具名人员、承诺和可用工时 | 无可核验名单或承诺记录 | 尚未核验 | 月 3 前具名并确认责任 |
| 当前候选模型、模拟恢复、预测、外部评价或随机试验新分析结果 | 当前材料未提供已生成结果 | 尚未生成 | 按日期计划前瞻生成 |
| 截至 2026-07-17 的最接近工作检索 | 项目内有界检索综合代表性正式论文、预印本和注册记录及稳定标识符 | 项目本地衍生材料 | 支持单项模块已有先例；完整组合缺口仅为低至中等置信 |

### Public ICU database roles and support status

- **开发数据库：** MIMIC-IV v3.1，计划用于标签和模型开发、内部验证与时间外验证；团队凭证、DUA 和确切表版本尚待确认。[5]
- **外部数据库：** eICU-CRD v2.0，计划用于按医院隔离的适配和未触碰最终评价；整院接口完整性尚待按医院核验，整院接口缺失可能表现为患者级未测量。[6]
- **备份数据库：** HiRID 或 AmsterdamUMCdb 只能在月 0–3 预先指定并完成同等核验后替代失败角色，不能依据最终评价结果选择。[7,8]
- **共同变量：** 计划只保留单位、语义、时间戳和可见性均可核验的共同概念；数据库特异信息仅用于探索性观测方程。[9,10]

目前成人患者、住院和 ICU stay 数、重复或可链接住院、医院数、12 小时评估点、首次发病事件、竞争结局、允许转移、时间戳精度、共同锚点单位与密度、医院接口覆盖、缺失与跨院链接、有效支持和复杂度上限均尚未生成项目计数。这些字段将由数据工程角色生成、临床与统计角色核验，并在月 6 前冻结。

### Local RCT evidence and present limits

EXIT-SEP 和 XBJ-SCAP 只作为条件性阶段 III 的潜在个体级随机试验数据来源；其当前证据状态不改变阶段 I–II 的公共 ICU 数据主体。

EXIT-SEP 在中国 45 个 ICU 随机 1,817 例 Sepsis-3 患者；本地衍生报告记录 1,760 例 28 日状态明确、395 例死亡、57 例状态未知，SOFA D1/D4/D7 非缺失为 1,750/1,542/1,296，乳酸 D1–D7 由 855 降至 223。[17,21-23] 这些数字描述衍生清洗层的稀疏性；个体数据授权、D1/D7 相对随机化和首剂时序、中心语义以及死亡、住院和出院状态尚未由原始 CRF/SAP 核验。

XBJ-SCAP 随机 710 例重症社区获得性肺炎患者；本地衍生报告记录全分析集（FAS）675 例、符合方案集（PPS）617 例、FAS 且基线 SOFA≥2 的操作性类脓毒症人群 671 例、严格重叠人群 658 例；SOFA D0/D4/D8 非缺失 703/628/610，WBC 为 704/634/614，CRP 为 579/503/467，28 日状态 675。[18,24,25] SCAP 入组与确认 Sepsis-3 并不等价；PaO2/FiO2、乳酸、休克、CRRT 和 CNS 等患者级字段在现有衍生材料中不可用，D-dimer 单位尚待核验。

## Research design and methods

### Design sequence and database-support criteria

方法顺序固定为资源与可观测性核验、标签与状态定义和医院拆分锁定、简单基线、绝对模拟恢复和错误结构检查、至多一个复杂候选、两项主要任务和两项次要诊断、开发冻结、未触碰跨数据库验证，随后才可能进入条件性试验次要分析。

两个公共数据库必须逐项记录访问与版本、成人患者、住院和 ICU stay、医院、首次发病事件、竞争事件、允许转移、时间戳、共同锚点、接口覆盖、缺失、跨院链接和有效参数支持。活着出院、死亡、转院或失访和行政观察结束分别计数；稀少类别可合并为“其他终止”，但不作普通独立删失。主要分析每次住院只用首个合格 ICU stay，可链接重复住院保留患者首次合格住院；外部最终评价至少需要 20 个有事件支持的医院。每个自由风险参数在开发与外部数据中分别至少有 20 和 10 个事件，每个自由转移参数分别至少有 20 和 10 次转移；不足时降维或删除相应边。无法支持 12 小时排序时，须在模型拟合前统一改锁 24 小时，仍不足则改用事件时间。

每个共同状态维度至少需要两个生理锚点；每个锚点在两个数据库中均须至少 30% 合格时间格内有实测值，并存在于至少 70% 合格医院且覆盖 80% 合格患者，不能用向前填充达到该标准。除有明确起止的输注或器官支持状态和静态基线外，不作无条件向前填充；每个动态值保留是否实测、实测时刻和距上次实测时间。复杂度上限为 K=min(通过支持要求的共同模块数,4)，切换机制数≤3。

### Variable roles

| Primary role | Examples and allowed use | Prohibited use / dual-use rule |
|---|---|---|
| 生理测量 Y_t | 实测生命体征、血气、实验室和器官功能测量；支持核验后保留的共同锚点 | 不含治疗启停、剂量或测量频率；同源 SOFA 标签副本进入隔离标签管线，不回流为特征 |
| 治疗行动 A_t | 抗菌药、液体、血管活性药、机械通气、CRRT、激素的启动、停止和剂量 | 不作潜在生理锚点；若用于恶化标签，只生成带事件时刻的隔离副本并在事件后使用 |
| 观测过程 M_t | 是否检测、次数、间隔、医嘱、采样、结果可用时刻和医院接口 | 未检测不等于正常，接口缺失不作患者状态 |
| 仅用于标签 | 疑似感染配对、隔离 SOFA 事件、互斥状态、死亡、出院和转院 | 不进入相同或更早评估点；抗菌药双重用途遵循可用性时钟并与行动通道分离 |
| 基线协变量 B | 年龄、性别、入院类型与来源、既往病史等评估点前固定信息 | 不随时间复制为伪测量，未知值显式编码 |

### Protocol locks for the two primary clinical tasks

| Item | Primary pre-onset task | Primary post-onset task |
|---|---|---|
| Population | ≥18 岁；每次住院首个合格 ICU stay；至少 12 小时可见历史；评估点尚未达到主要标签；观察起点已经发病者排除 | 首次发病；入 ICU 时已经发病者仅在首个可审计时点延迟进入，分层并左截断 |
| Event clock | 主要疑似感染定义为微生物标本采集和系统抗菌药首次实际给药的配对：采集先发生时给药须在其后 72 小时内，给药先发生时采集须在其后 24 小时内；感染时刻取较早者；无记录慢性器官功能障碍时基线 SOFA=0，有记录时取入 ICU 前 24 小时最低可计算 SOFA，不可审计者不进入主要风险集；SOFA 成分在滚动 24 小时取最差值，相对基线增加至少 2 分须发生在感染前 48 小时至后 24 小时，发病时刻为首个可排序的满足时刻。[1,2] | 首次发病以主要临床事件时刻为零点；发病后状态按临床事件时刻进入 |
| Availability clock | 配对中较晚事件及必要 SOFA 数据在源系统可见或最终化时刻取最大值，之后信息不回填 event time | 恢复需连续 24 小时，availability 为窗结束；恶化、死亡、出院和转院采用记录可用时刻，只使用当时可见标签 |
| Landmark/history/horizon | ICU 第 12 小时起每 12 小时；此前最多 24 小时且至少 12 小时按当时可用信息构造的历史；预测未来 12 小时首次发病 | 首次发病或延迟进入后每 12 小时；主要观察时域为病程第 7 日，14 日为敏感性分析 |
| First onset/repeats | 只分析首次发病；重叠评估点保留，但每次住院总权重为 1，并按患者与医院聚类 | 首次发病与延迟进入分层；延迟进入不反推发病时刻 |
| Competing/intercurrent | 发病前活着出 ICU、院内死亡、转院或失访为互斥终止；行政结束独立删失并进行逆概率删失加权与界限检查 | 死亡、活着出 ICU 和转院为终止状态；恢复不由出院代替；进行逆概率删失加权敏感性分析 |
| Within-bin order | 评估点 t 的特征只含 availability<t 的信息；[t,t+12h) 新行动为 A_t，下一边界实测生理定义 next-state；同时间戳无法排序者不用于该边 | 相同；器官支持是行动，隔离事件标签只在形成后定义恶化 |
| Estimand/model | 给定历史，未来 12 小时首次发病的累积发生函数；离散多项式原因特异风险模型转换为累积发生函数 | 第 7 日“生理恢复或活着出 ICU”有利集合占用概率，二者另报；互斥离散多状态模型与 Aalen–Johansen 估计 |
| Metric | 12 小时 Brier 评分、绝对校准截距和斜率；精确率—召回率曲线下面积、提前量和假警报为次要指标 | 第 7 日多类别 Brier 评分和有利状态绝对校准；各状态和转移校准为次要指标 |
| Uncertainty | 每次住院总权重为 1；患者与医院层自助法 95% 区间 | 患者与医院层自助法；首次发病与延迟进入分层并报告有效转移数 |
| Pass/fail | 开发与未触碰外部评价均须满足 Brier 评分非劣 +0.01、校准斜率 0.80–1.20、绝对风险误差≤0.02，并清除全部高严重度泄漏 | 同一标准；次要表示诊断或后续试验结果不能替代失败的主要任务 |

主要标签之外只采用两种标签敏感性分析：把培养与抗菌药配对改为对称 ±24 小时；所有人均使用感染前 24 小时最低可计算 SOFA，并把器官功能窗限制为感染前后各 24 小时。敏感性分析不替换主要结果。泄漏检查逐项检验发病后生理或治疗、尚未可用的培养或抗菌药、同一时间格行动、未来测量频率、跨拆分插补或标准化、患者或 ICU stay 跨集合、重叠窗口权重以及结局驱动的时间网格或阈值；未清除高严重度项目时不打开最终外部评价数据。

### Mutually exclusive post-onset state/event system

每 12 小时赋值，优先级固定为死亡 > 转院或无法继续观察 > 活着出 ICU > 恶化或新器官衰竭 > 生理恢复 > 持续脓毒症。源时间无法排序时采用较高优先级，并进行事件时间敏感性分析。

| State/event | Operational definition and availability | Role safeguard |
|---|---|---|
| 持续脓毒症 | ICU 内存活且未满足其他状态；可转移状态 | 隔离为仅用于标签的信息，不作生理锚点 |
| 生理恢复 | 相对发病参考 SOFA 下降≥2，且连续 24 小时无新恶化；临床事件时刻为窗起点，信息可用时刻为窗结束；可复发 | SOFA 只用于标签；无器官支持升级只是标签条件，行动仍留在 A_t |
| 恶化或新器官衰竭 | 相对此前 24 小时最低 SOFA 增加≥2，或新启动或升级血管活性药、有创通气或 CRRT；同时发生只记一次 | 生理值和由行动派生的标签副本隔离，行动不作锚点 |
| 活着出 ICU | 存活离开 ICU；分析中为吸收状态 | 不等同于生理恢复，去向另行报告 |
| 转院或无法继续观察 | 转往不可追踪 ICU 或医院，或记录终止；终止性竞争事件 | 不编码为恢复或普通独立删失，进行逆概率删失加权与界限分析 |
| 死亡 | ICU 内或可追踪病程死亡；吸收状态 | 不作随机缺失，同时间戳时优先 |

### Observational target, anchoring, missingness, and abstention

令锚定潜在患者状态为 X_t，生理测量为 Y_t，治疗行动为 A_t，观测指示或强度为 M_t，基线为 B，数据库或医院为 S。主要目标是在实际照护与测量政策下估计联合预测与生成分布 p(X_0:T,Y_0:T,M_0:T,A_0:T | B,S)，以及由其导出的风险、对齐状态占用和转移、锚点预测与预设符号和滞后不变量；该估计目标不把行动条件关系解释为治疗效应。

每个维度至少有两个跨数据库锚点；第一个锚点的载荷固定为 +1 并标准化尺度；非指定交叉载荷为 0 或遵循预写稀疏模式；K≤4、切换机制数≤3，滞后只允许 1 或 2 个冻结时间格，允许图中没有同一时间格瞬时循环。采用 20 个固定随机种子后进行排列与符号对齐。只解释对齐后的状态占用、转移概率、锚点层预测及预设关系的符号和滞后。

缺失非随机敏感性分析的主要拟合采用显式观测过程的随机缺失与选择模型基线，并对未测生理值使用模式混合 delta −1、−0.5、0、+0.5、+1 个开发数据库标准差以及选择模型临界点分析。每个对齐状态、医院和时间层报告行动概率与有效样本量；行动比例<5%或>95%，或加权有效样本量低于名义样本的 20% 时，相应关系标为低支持和照护政策特异，不估计治疗作用。

任一状态或边在预设模拟中未达到恢复标准、20 个随机种子中的对齐率<90%、自助法保留率<80%、外部符号一致率<80%、状态对齐<0.70 或区间未校准时，必须删除、合并或标为数据库或照护政策特异。较好的预测表现不能豁免这些判定。

### Absolute simulation and semi-synthetic recovery

月 7–10 在不读取临床最终外部评价结果的情况下，对每个核心情景至少重复 1,000 次，或运行到关键比例的蒙特卡洛标准误≤0.02。生成情景包括正确指定、零边或独立状态、多余状态或过拟合、遗漏状态、错误滞后或观测模型，并交叉改变状态分离、切换率、1 或 2 个时间格滞后、政策反馈、隐藏混杂、缺失非随机、标签误差、访视密度、整院接口缺失和数据库偏移。

| Recovery quantity | Absolute criterion | Prespecified response |
|---|---|---|
| 状态恢复 | 离散调整 Rand 指数≥0.80，或连续状态的主要典型相关系数≥0.80；20 个随机种子对齐≥90% | 合并或删除状态，或降级为线性或多状态模型 |
| 转移概率 | 主要允许转移的平均绝对误差≤0.05；95% 区间覆盖率为 0.90–0.98 | 删除该转移或停止结构解释 |
| 预设符号和滞后 | 正确恢复率≥0.80 | 该关系不进入共同结构 |
| 边检测 | 灵敏度≥0.80 且错误发现率≤0.10 | 降低稀疏度或维度；仍不满足时只保留预测用途 |
| 零边生成情景中的错误结构 | 任一假边的 95% 区间排除 0 的重复比例≤0.05 | 淘汰复杂候选，不根据结果调整阈值重新挽救 |
| 错设生成情景中的错误高置信 | ≥80% 重复触发失配识别或弃权；错误结构获得高置信的比例≤0.05 | 淘汰候选，或只解释已恢复的不变量 |
| 概率校准 | 斜率 0.80–1.20；绝对概率偏差≤0.02 | 重校准不能修复结构恢复失败，转用较简单模型 |

### Hospital-prioritized independent cross-database validation

在任何结局导向选择前，先按合格体量四分位和接口完整性分层，以固定种子 20260717 对 eICU 医院 ID 进行哈希分配：30% 医院用于适配，70% 医院用于未触碰最终评价。医院分区优先于患者规则，最终评价医院不因患者链接进入适配区；分区表、链接算法版本和校验和在查看最终评价结局前冻结。

主要外部分析按以下规则执行：

1. 先完成医院哈希，再仅以患者链接键识别跨院记录；若一个可链接患者的记录跨越适配医院和最终评价医院，该患者的全部记录从主要外部分析中排除，不按患者哈希重新分配。
2. 对只出现在同一分区的患者，只保留预先定义的首次合格住院及其首个合格 ICU stay，保证同一患者不跨集合。
3. 在揭示最终评价性能前，报告跨分区排除人数、占原合格患者比例、涉及医院数，以及只使用结局前信息计算的年龄、性别、入院类型或来源、首个评估点生理负担和观测密度；不依据结局或模型误差决定排除。
4. 预写敏感性分析在冻结医院角色后建立患者—医院二部图：纯适配或纯最终评价组件保持原角色；混合组件从适配区删除全部相关患者记录，仅保留其预分配最终评价医院中的首次合格 ICU stay 进入最终评价。该规则不把最终评价医院移入适配区，不让患者跨集合，也不借用最终评价数据训练。
5. 独立数据保管人在不释放模型性能的条件下检查支持。主要剔除或敏感性规则实施后，如果最终评价区少于 20 个合格医院、任一自由风险或转移参数低于外部 10 个事件或转移、共同锚点不再覆盖至少 70% 合格医院和 80% 患者，或跨分区排除超过原合格最终评价患者或主要事件的 10%，则启动预指定备份数据库；备份仍不能满足时，只报告数据库级运输或描述结果。

冻结标签、跨数据库统一规则、状态、预处理、可用性时钟、模型、超参数、阈值和评价代码后，依次进行四项不同操作：首先把冻结模型直接应用于最终评价数据而不重新估计任何参数，作为主要外部验证；其次只用适配医院重估各预测时域的结局校准截距和斜率；再次只用适配医院重估观测方程而保持状态和转移参数冻结；最后，如需重新估计全部模型参数，这构成新的模型开发，不属于外部验证结果。最终评价数据不用于选择变量、时间方案、状态数、锚点、分区、更新方式或阈值，只重估校准参数或只重估观测方程的成功也不能替代冻结模型未达到标准。

### Conditional trial-specific secondary analyses

两项试验的新访视状态结局均是在原试验结果之后提出的次要或探索性分析；原 28 日终点复现独立报告，两项试验不合并。完整分析资格、两条互斥路线、停止条件和允许解释如下，并且所有变量映射、阈值、代码与随机种子都在治疗组比较前冻结。

**Shared prerequisites.** 阶段 II 必须先达到全部成功标准并被冻结；相应试验须获得个体数据分析授权，并以原始 CRF、SAP、数据字典或数据持有人确认核验随机化与分析集、中心或分层因素、实际 D7（EXIT-SEP）或 D8（XBJ-SCAP）相对随机化与首剂的访视窗，以及死亡、住院、活着出院和转院语义。任何后续试验结果都不能补足阶段 II 未满足的数据支持、模拟恢复、主要任务或外部验证要求。

**Mapping-based route: common measured anchors and frozen computation.** 对每项试验 r，候选共同变量集 C_r 只包含阶段 II 保留的 Y_t 生理锚点，且须在该试验实际 D7 或 D8 访视中直接测得，临床构念、标本和单位一致或有预先验证的确定性单位转换，采样与结果可用时刻落入冻结访视窗，并且不是治疗、测量频率、SOFA、结局标签或事后派生状态。每项试验至少需要两个合格锚点，每个锚点都须在阶段 II 与试验中通过范围、时间和测量语义核验；WBC 和 CRP 只是现有衍生报告提示的候选，单位不明的 D-dimer 和不存在的字段不能进入。

使用 MIMIC 开发集锁定的均值、标准差和第 1、99 百分位截断得到 Z_C；从阶段 II 冻结观测方程 Z_C=a_C+L_C X+e 取 L_C 的第一奇异向量组 L_C=UDV'，定义一维阶段 II 状态量 P_state=V_1'X，并定义由共同实测生理锚点计算的一维观测状态量 **P_obs=D_1^(-1)U_1'(Z_C−a_C)**。奇异值并列时按预先固定的锚点字典序决定；符号在阶段 II 开发集中固定为与同日 SOFA 总分非负相关，使数值越高表示状态越不利。整个计算不使用试验治疗分组、试验结局或试验间合并数据，每项试验有自己的 C_r 和冻结计算。

**Mapping-based route: empirical fidelity criteria.** 首先在阶段 II 未触碰 eICU 最终评价数据的相应发病后 D7 或 D8 时间窗检验，且不按试验结果调参。必须同时满足：第一奇异轴解释 L_C 的 Frobenius 范数平方总能量至少 50%；P_state 与 P_obs 相关系数≥0.70；相对 P_state 标准差的归一化平均绝对误差≤0.50；回归 P_state=α+βP_obs 时 |α|≤0.20 个标准差、β 为 0.80–1.20，95% 区间覆盖率为 0.90–0.98；每个共同锚点的外部校准斜率为 0.80–1.20、标准化截距绝对值≤0.20。随后在遮蔽治疗标签的试验数据中检查：至少 80% 观测锚点落在冻结阶段 II 生理合理范围内，且至少 60% 访视时存活在院者能由不少于两个实测锚点直接计算 P_obs。任何标准未达到、单位或时间不变性不成立，或需要根据试验重新估计权重时，该路线不成立，不能依据随机分组差异修改判据。

**Visit-level hierarchical outcome and randomized comparison.** 上述计算和经验标准均成立时，构造访视层级状态结局：D7 或 D8 前死亡者置于最不利层；访视时仍存活在院者按共同锚点一维观测状态量从高到低排序；访视前活着出院者置于单独的最有利层。主要随机分组比较为与中心或随机化分层相容的优势概率，即从两组各随机抽取一名参与者时，治疗组参与者处于更有利访视层级的概率，并按预先规定处理并列。该比较只检验随机分配对实际访视中这一可观测状态结局的有限差异。

**Independent trial-specific clinical-state route and stopping condition.** 如果共同锚点不足两个、单位或时间语义不一致，或经验映射标准未达到，但该试验的 SOFA、死亡、住院与出院、随机化和中心语义均可核验，则使用试验特异独立临床状态结局：死亡置于最不利层，访视时存活在院者按 SOFA 从高到低排序，活着出院者置于最有利层。该结局与阶段 II 候选表征独立，不使用共同锚点一维观测状态量。如果核心 D7 或 D8、随机化、中心或生存与住院语义无法核验，则不开展新的访视状态结局分析，只复现原终点或报告数据审计。

| Trial | Population and visit | Missingness/death and analysis | Multiplicity and stop rules |
|---|---|---|---|
| EXIT-SEP | 随机 1,817 例；目标为全随机化人群的治疗策略估计，已知结局 1,760 例只能称完整结局子集；实际 D7，若 D1 位于随机化后则不作未受影响基线 | 死亡和活着出院按层级进入；存活在院但共同锚点一维观测状态量或 SOFA 缺失时，在每个多重插补数据集中使用治疗、中心、已确认的随机化前协变量和既往实际访视信息插补后重算冻结摘要，再以 Rubin 方法或聚类自助法合并；进行 delta ±0.5、±1 个标准差与最佳或最差情景临界点分析；转院或状态未知作界限，不当作随机缺失 | 遵循中心或分层；两个试验的主要访视状态结局构成一个由 Holm 法控制家族错误率为 0.05 的检验家族；其他访视或模块用探索性错误发现率；亚组只报告治疗×亚组交互项；关键 D7 或中心语义失败时停止新访视状态结局 |
| XBJ-SCAP | 随机 710 例为目标；无法重建全随机集时降级为 FAS 675 例的修正意向治疗分析并明示；PPS 617 例、操作性类脓毒症 671 例和严格重叠人群 658 例只作敏感性分析；实际 D8，若 D0 不是随机化前测量则不作基线或变化量 | 使用相同的死亡、出院、多重插补、delta、临界点和界限策略；不填补结构性不存在的 PaO2/FiO2、乳酸、休克、CRRT 或 CNS，D-dimer 单位未核验时排除 | 使用同一 Holm 检验家族；亚组只报告交互项；不能重建全随机集时明确为修正意向治疗分析；关键 D8、中心或生存语义失败时停止新访视状态结局 |

稀疏 D1/D4/D7 或 D0/D4/D8 数据只支持访视特异或离散变化，不插值为伪连续轨迹。两项试验的人群、访视、共同锚点或估计目标不同即保持独立；方向一致也不构成合并效应或共同机制。

### Secondary representation diagnostics

部分状态重建使用伪遮蔽平均绝对误差、均方根误差、对数评分和区间覆盖；未来轨迹使用连续排名概率评分、负对数似然、状态占用和结局校准。伪遮蔽只对原本已测值计算。诊断按变量、状态、医院和观测密度分层，不能替代主要任务、绝对恢复或外部验证标准。

## Key techniques and implementation

| Reproducibility record | Inputs or constructs | Computation | Output record and audit use | Dependency |
|---|---|---|---|---|
| 事件与信息可用时刻记录 | 标本、抗菌药、SOFA 成分、死亡、出院、转院的源表和时间戳 | 按冻结规则分别计算临床事件时刻与数据库可用时刻，并强制信息可用时刻早于评估点时刻 | 标签版本、时间戳来源、样本流和逐评估点泄漏断言，用于复现风险集 | 数据提取版本和标签规范 |
| 变量、单位和角色记录 | Y_t、A_t、M_t、仅用于标签字段、B，以及源单位和转换 | 核验单位、语义、可见性和角色；为双重用途字段生成隔离副本并记录滞后 | 共同变量字典、单位转换表、角色冲突和排除理由，用于跨数据库一致性审计 | 双数据库字段与临床核验 |
| 队列与状态记录 | 患者、住院、ICU stay、评估点、首次发病、延迟进入和竞争事件 | 应用首次合格住院、总权重、状态优先级和允许转移规则 | 队列流程、状态占用、转移计数和不可排序同时间戳记录，用于核验两项主要任务 | 标签与变量记录 |
| 模型输入与输出记录 | 冻结特征、锚点、状态数、切换机制数、滞后、允许图和随机种子 | 依次拟合竞争风险、多状态、线性状态空间和至多一个复杂候选 | 设计矩阵校验和、参数、状态对齐、预测和弃权记录，用于复现每个候选的输入输出 | 数据支持和队列记录 |
| 模拟记录 | 正确、零边、过拟合、遗漏状态、错误滞后和错误观测模型等生成情景 | 对每个核心情景重复模拟并计算恢复、错误结构、覆盖和失配识别量 | 生成参数、种子、估计量及达到标准或未达到标准的对象清单，用于决定模型保留范围 | 冻结候选定义与模型接口 |
| 医院分区与外部评价记录 | eICU 医院 ID、体量、接口完整性、患者链接键和固定种子 | 完成医院哈希、跨分区患者主要剔除和患者—医院组件敏感性分析 | 分区表、链接算法版本、排除人数和特征、权限日志及校验和，用于证明最终评价隔离 | 双数据库队列与独立数据保管 |
| 试验共同变量与冻结计算记录 | 每项试验的共同生理锚点、单位、访视窗、a_C、L_C、开发集标准化参数 | 核验变量和语义，执行冻结奇异值分解计算，并在遮蔽治疗标签时计算支持率 | 每项试验独立的变量集、公式参数、范围和可计算率记录，用于确认所采用的访视结局 | 阶段 II 冻结观测方程和试验原始语义 |
| 不确定性与多重性记录 | 患者、医院、中心、随机化分层、多重插补数据集和检验家族 | 执行患者与医院自助法、蒙特卡洛标准误、Rubin 合并、中心相容比较和 Holm 调整 | 区间、有效样本量、并列规则、调整后推断和敏感性记录，用于复核每项结论 | 相应模型或试验分析输出 |
| 负向控制与阴性结果记录 | 临床预裁定时间反转、阴性对照、接口缺失和标签误差情景 | 使用与主分析一致的拆分和评分计算偏倚指标 | 以未达到标准的对象、判据、分层和科学后果命名的表图，用于发布可证伪结果 | 冻结标签、模型和评价代码 |

## Evidence chains

### Evidence chain: 可用性时钟、风险集与互斥病程

- **Input:** Sepsis-3、培养与抗菌药和 SOFA 时间戳、死亡、出院、转院事件、公共 ICU 数据字典及双数据库支持记录。[1-10]
- **Method / analysis / processing:** 主要和两种敏感标签；事件与信息可用双时钟；12 小时评估点；首次发病与 delayed entry；互斥状态、竞争事件、患者权重和泄漏断言。
- **Output:** 可执行的 12 小时首次发病累积发生风险队列、第 7 日多状态队列、标签差异矩阵和泄漏记录。
- **Supports:** 候选表示覆盖可比较未发病时段、首次发病、发病后演化和结局的可审计边界。

### Evidence chain: 数据支持、锚定识别与绝对恢复

- **Input:** 双数据库锚点、接口、事件和转移记录，知识先验，状态、治疗和观测三类过程，以及正确、零边、过拟合和错设生成情景。
- **Method / analysis / processing:** 共同模块和复杂度选择；载荷、尺度、图和滞后锚定；至少 1,000 次蒙特卡洛重复；缺失非随机、政策反馈、接口缺失和数据库偏移压力测试；恢复、错误发现率、区间覆盖率、错误结构与失配识别计算。
- **Output:** 一个达到全部标准的受限复杂候选，或自动降级的多状态、线性或仅预测基准，并附删除、合并和弃权清单。
- **Supports:** 可估计和可解释的不变量，而不是任意潜在状态坐标。

### Evidence chain: 两项主要任务与两项次要诊断

- **Input:** 冻结队列和状态、准入模型、开发、时间外和医院外拆分及预设指标。
- **Method / analysis / processing:** 12 小时首次发病累积发生风险、第 7 日状态占用；Brier 或多类别 Brier 评分、校准和聚类自助法；伪遮蔽、连续排名概率评分、轨迹诊断、标签、缺失、行动和观测消融及负向控制。
- **Output:** 两项主要任务的评分、校准和状态概率，两项次要诊断的评分、覆盖，以及按未达到标准对象、判据和分层命名的表图。
- **Supports:** 患者—时间状态任务效度及阶段 II 合取成功判定。

### Evidence chain: 医院优先、未触碰的跨数据库检验

- **Input:** 开发冻结包、按医院预分配的 eICU 适配区和最终评价区、跨院患者链接记录、共同锚点和预设判据。
- **Method / analysis / processing:** 主要分析排除跨分区患者；同分区保留首次合格 ICU stay；患者—医院组件敏感性分析；依次执行冻结模型不重新估计任何参数、只重估结局校准、只重估观测方程和全部参数重新拟合，并进行患者与医院聚类、状态对齐和测量不变性计算。
- **Output:** 跨分区排除数量和结局前特征、支持判定、四类外部操作的分开结果，以及稳定、数据库特异和弃权对象清单。
- **Supports:** 阶段 II 的计划性跨数据库候选系统表征端点。

### Evidence chain: 条件性分试验次要分析

- **Input:** 已达到标准并冻结的阶段 II 表征，以及条件性可获得且核心语义可核验的试验个体数据。[17,18,21-25]
- **Method / analysis / processing:** 按试验冻结共同变量或独立临床状态结局，使用随机化相容的访视层级优势概率、预设缺失处理和多重性控制。
- **Output:** 两项试验分别报告的次要访视状态分析，或因科学前提不满足而形成的停止记录。
- **Supports:** 在不替代阶段 II 证据的前提下，检验试验特异实际访视状态的随机分组差异。

## Required analyses and evidence

阶段 II 主张前必须完成：

1. 月 3 资源确认和具名角色承诺；月 6 完成版本与校验和、队列、事件、医院、跨院患者、共同锚点、接口和复杂度的冻结记录。
2. 主要标签、两种敏感标签、事件和信息可用时钟、12 小时评估点、第 7 日状态、优先级、delayed entry 以及竞争和删失规则的单元测试。
3. 变量角色表及双重用途副本的滞后与隔离证明；无条件向前填充、未来测量频率和跨拆分插补检查。
4. 简单基线、绝对 Monte Carlo、零边错误结构、错设情景失配识别和自动降级记录，不能只报告相对预测排名。
5. 缺失非随机 delta 与 tipping-point、行动重叠和有效样本量、接口缺失、标签误差、时间反转和临床阴性对照。
6. 两项主要任务和两项次要诊断的 Brier 评分、连续排名概率评分、绝对校准、覆盖、警报负担及患者与医院聚类区间，并按规则处理状态和边的弃权。
7. 医院哈希分配表、跨分区患者排除表、结局前特征比较、患者—医院组件敏感性分析、权限日志与冻结校验和，以及四种外部参数处理方式的明确区分。
8. 月 24 合取表逐项记录达到、降级或未达到，并把基准和资源价值与跨数据库系统表征成功分开。
9. 若进入 24 月后的试验工作，须按试验完成个体数据与核心语义核验、预先冻结访视状态结局和随机分组比较，并保留未开展分析的原因记录。

## Expected outputs, falsification criteria, and interpretations

### Planned outputs

1. 双时钟标签、12 小时风险集、互斥发病后状态、双数据库支持规范和可重复代码。
2. 变量角色记录、共同概念、接口与缺失资源、医院优先拆分和跨院患者排除审计。
3. 基线、绝对恢复、错误结构与弃权基准，以及至多一个准入复杂候选或自动降级结果。
4. 两项主要任务和两项次要诊断的开发、时间外、医院外和未触碰跨数据库结果，包括校准、不确定性、对齐及按未达到标准对象和判据命名的表图。
5. 条件满足时形成两个分开报告的试验次要分析；科学前提不满足时报告停止原因。

### Falsification and stop criteria

- **时钟和泄漏：** 若结果由后录入标签、同一时间格未来行动、未来测量频率或跨拆分插补驱动，则相应端点未获支持；高严重度泄漏未清除时不打开最终评价数据。
- **数据库支持：** 若两个数据库的事件、转移、医院、跨院排除或共同锚点未达到预设数量与覆盖标准，则删除相应模块或边、改用预写时间网格、启动备份数据库，或停止跨数据库复杂表示。
- **绝对恢复：** 若状态或转移恢复、区间覆盖、零边错误结构比例或错设情景失配识别未达到预设标准，则淘汰复杂候选；相对预测优势不能改变该结论。
- **缺失和行动支持：** 若 delta tipping-point 改变解释，或行动概率和有效样本量显示低重叠，则报告敏感性或照护政策特异性，并对相关状态或关系弃权。
- **外部验证：** 若冻结模型不重新估计任何参数时的 Brier 评分、校准、状态对齐或符号一致性未达到标准，则跨数据库端点未获支持；只重估结局校准参数或观测方程后的改善只支持适配后的运输。
- **试验结果：** 采用何种访视状态结局由治疗组比较前冻结的科学标准决定；若核心试验语义不能核验则不开展新访视状态结局分析。两个试验方向不一致或区间过宽时，只报告无支持或跨场景适用性有限，不选择亚组改变主要解释。
- **时间：** 月 12 没有准入复杂候选时封存降级模型；月 20 未冻结时不打开最终评价数据；月 24 没有未触碰外部结果时，阶段 II 最低端点未完成。

### Interpretation matrix

| Observed pattern | Allowed interpretation | Prohibited interpretation |
|---|---|---|
| 简单基线有用，复杂候选恢复失败 | 多状态或预测基准有用，并获得复杂表示未恢复的证据 | 复杂结构已被识别 |
| 模拟恢复达到标准，但冻结模型外部验证失败 | 候选在开发数据和预设生成情景内可恢复，同时存在跨数据库运输失败 | 跨数据库共同系统有效 |
| 冻结模型外部验证失败，只重估校准或观测方程后达到标准 | 适配后可运输，且观测层或校准存在数据库差异 | 冻结模型天然稳健 |
| 两项主要任务达到标准，但部分状态或边被弃权 | 获得任务级患者—时间预测表示 | 被弃权结构正确 |
| 共同锚点访视状态结局显示随机组差异 | 该试验实际访视中的可观测层级状态存在随机组差异 | 阶段 II 全部潜在状态或结构获得随机化验证 |
| 试验特异独立临床状态结局显示随机组差异 | 该试验的独立次要临床状态存在随机组差异 | 阶段 II 候选表征受到验证 |
| 所有阶段 II 合取标准均达到 | 最小全病程候选表示获得数据、恢复、任务和未触碰外部支持 | 获得因果或控制解释 |

## Contribution, innovation, impact, application, and closest-work comparison

### Contribution and evidence ladder

计划中的实际增量有三层。输入层连接可比较未发病评估点、首次发病和互斥发病后状态；表征层分开患者状态、治疗行动和观测过程，并以锚定不变量和绝对模拟恢复限制解释；验证层把两项主要任务与医院优先、未触碰的跨数据库评价连接起来，同时保留未达到标准的可复用记录。若执行成功，这一主体研究可形成条件性的整合、验证、基准和资源贡献，并支持一篇或多篇高水平论文；24 月后的试验工作是依赖阶段 II 的次要延伸，不作为并列贡献。

| Evidence level | Allowed claim | Necessary evidence | Current scope |
|---|---|---|---|
| 数据可追溯 | 标签、时钟、风险集、变量和接口可审计 | 双数据库支持记录、角色表和泄漏清除 | 计划，尚未生成 |
| 状态恢复与任务效度 | 观察政策下的候选状态具有任务效度 | 绝对恢复、两项主要任务和两项次要诊断、校准与弃权 | 阶段 II 必需 |
| 跨数据库状态与结构稳定 | 冻结不变量在未触碰最终评价数据中稳定 | 医院优先外部验证、允许更新分开报告、对齐和阴性结果表图 | 阶段 II 最低端点 |

### Verified representative closest-work comparison

| Research line | Representative verified neighbor and stable identifier | What is already non-novel | Conditional difference tested here |
|---|---|---|---|
| 纵向与多状态 | Klein Klouwenberg et al. 2019，多状态 Markov，DOI 10.1186/s13054-019-2687-z，PMID 31831072；Xu et al. 2022，72h SOFA 轨迹，DOI 10.1186/s13054-022-04071-4，PMID 35786445。[26,27] | 已发病脓毒症的日级转移、轨迹聚类和外部复现已有先例 | 在同一风险集内连接发病前评估点、首次发病和互斥发病后状态，并以双时钟排除未来信息；证据尚待生成 |
| 动态表型与干预条件转移 | Boussina et al. 2023，动态表征、聚类和马尔可夫决策过程（MDP），DOI 10.2196/45614，PMID 37351927；Ghassemi et al. 2017，切换状态空间预测干预开始，PMID 28815112，PMCID PMC5543372；Feng et al. 2025，器官交互轨迹，DOI 10.1016/j.eclinm.2025.103691，PMID 41497501。[29-31] | 潜在状态、动态表型、观察性干预条件转移和器官交互图已有先例 | 显式分开 Y_t、A_t、M_t、标签和 B，并以零边和错设生成情景限制结构解释 |
| 数字孪生与模型预测控制 | Lal et al. 2020，治疗反应 digital-twin 原型，DOI 10.1097/CCE.0000000000000249，PMID 33225302；Pickard et al. 2026，生成式 EHR twin 与模型预测控制（MPC），arXiv:2607.08793。[32,33] | 脓毒症数字孪生、患者特异模拟和孪生上的模型预测控制原型与命名已有先例 | 当前研究检验候选表征的恢复和运输，不把数字孪生或控制作为贡献 |
| 强化学习与运输 | Komorowski et al. 2018，AI Clinician，DOI 10.1038/s41591-018-0213-5，PMID 30349085；Nauka et al. 2025，运输性，DOI 10.1038/s41746-025-01485-6，PMID 39915643；Tang et al. 2026，时间错位，DOI 10.1038/s41746-026-02625-2，PMID 42098339；Kalimouttou et al. 2025，OVISS，DOI 10.1001/jama.2025.3046，PMID 40098600。[19,34-36] | 离线策略学习、跨观察数据库评价、离策略评估和时间构造风险已有先例 | 阶段 II 聚焦时间顺序、医院外隔离、绝对恢复和弃权，不学习控制策略 |
| 随机试验次要分析 | Bhavani et al. 2022，轨迹亚型开发和验证并在 SMART RCT 中分析治疗交互，DOI 10.1007/s00134-022-06890-z，PMID 36152041；AI Clinician 影子评估注册 NCT05287477 界定部署边界。[28,37] | 在随机试验中进行表型与治疗二次交互及观察性影子部署已有先例 | 本研究只在主体证据达到标准后按试验开展预先规定的访视状态次要分析 |

截至 2026-07-17 的有界代表性检索以高置信度表明，表中每一研究模块都已有代表性先例；它没有找到同时覆盖发病前、发病时刻、发病后演化、任务与节点级跨数据库运输和稀疏随机试验层且分开状态、行动与观测过程的代表性工作，但这一完整组合缺口只有低至中等置信。[38] 因而当前最强可辩护定位是条件性的证据整合与验证增量，而不是新算法或全球首次。

## Title and positioning claim-support table

| Title or positioning claim | Contribution frame / claim type | Existing implementation that supports it | Supporting evidence-chain output | Literature or existing-result basis | Actual increment, or none | Support status |
|---|---|---|---|---|---|---|
| “脓毒症全病程候选动态系统表征”是研究对象 | integration / validation | 计划中的双时钟、首次发病任务、互斥发病后状态及状态、行动与观测分工 | “可用性时钟、风险集与互斥病程”及“数据支持、锚定识别与绝对恢复” | Sepsis 基础 [1,2]；多状态和轨迹近邻 [26,27] | 全病程输入、表征与验证连接 | 有文献和计划支持；模型须始终表述为拟构建和拟检验的对象，不得写成已经建立的系统 |
| “24 个月跨数据库构建与检验计划”是阶段 I–II 动作 | validation / benchmark | 计划中的医院优先适配与最终评价、跨分区患者剔除、冻结模型首先应用 | “医院优先、未触碰的跨数据库检验” | 公共数据库和有限统一 [5-10]；运输失败近邻 [12,34] | 未触碰评价、患者不跨集合及阴性结果记录 | 有条件支持；访问、项目支持和结果尚未生成，有限更新不替代冻结模型结果 |
| 主体研究达到全部标准后，两个试验才分别提供预先规定的访视状态次要分析 | validation / translational | 计划中的共享前提、按试验冻结访视状态结局和随机化相容比较 | 证据链记录主体研究达标后按试验分别执行预先规定的访视状态次要分析，并在科学前提不满足时形成停止记录 | EXIT-SEP、XBJ-SCAP 及衍生材料 [17,18,21-25]；随机试验次要分析近邻 [28] | 把试验工作明确置于阶段 II 之后并分试验实施 | 有条件支持；次要、条件性且不计入阶段 II 成功 |
| 贡献是整合、验证和基准或资源 | editorial_repositioning / integration / resource | 计划中的数据支持记录、变量角色、绝对恢复、外部隔离和阴性结果发布 | 前四条证据链的联合输出 | 模块近邻 [26-37]；有界检索 [38] | 条件式全病程证据连接 | 有文献和计划支持；单项模块已有先例，贡献须待执行结果确认 |
| 有界检索未找到完整代表性先例 | scientific novelty | 截至 2026-07-17 的项目内有界检索 | 最接近工作比较及五条计划证据链 | 有界检索 [38] | 当前不形成已实现增量 | 低至中等置信；只表述本次检索未找到，不推断全球不存在 |

## Feasibility, resources, risks, alternatives, and stop conditions

### Resource and evidence limitations

核心证据基础是文献与专家先验、MIMIC-IV 和 eICU-CRD 的纵向公共 ICU 数据，以及条件性可用的 EXIT-SEP 和 XBJ-SCAP 个体级试验数据。各公共数据库的中心、年代、采样和接口并不等价，跨数据库统一只能建立在经核验的受限共同概念上。公共数据库的存在与版本已经核验，但团队访问凭证、DUA、可运行提取、存储、项目队列中的样本、事件、转移、医院、跨院患者和共同锚点支持尚未核验或生成；HiRID 或 AmsterdamUMCdb 仅是须预先指定并同等核验的备份。临床、统计、系统辨识、数据工程、模型实现和独立数据保管角色已经定义，但没有可核验的具名人员承诺或工时记录。当前也没有候选模型、模拟恢复、主要任务、外部验证或试验新分析结果。

现有 EXIT-SEP 和 XBJ-SCAP 材料是项目本地衍生清洗与验证报告，不能替代个体数据分析授权、原始 CRF、SAP、数据字典或数据持有人确认，也不能替代随机化、中心、实际访视相对首剂时序以及死亡、住院、出院和转院语义核验。阶段 II 与试验之间的共同生理锚点、单位和观测映射均尚未成立。阶段 I–II 的时间节点依赖按期完成资源、数据支持、开发冻结和未触碰外部评价，阶段 III 位于 24 个月最低交付之外。

截至 2026-07-17 的最接近工作证据来自有界代表性检索，不是 PRISMA 双人筛选的系统综述，也未穷举引文网络、专利、CNKI、万方、Scopus、Web of Science、Embase、非英语数据库和全部注册平台；预印本和术语差异还会改变检索结果。因此，完整组合缺口只有低至中等置信，不能支持全球不存在性判断。

### Unresolved working assumptions and analytic specifications

仍待以数据或预先登记规范解决的工作假设包括：临床可容许尺度到模拟参数的映射；精确的多类别校准估计量、置信界和阈值登记；12 小时时间格、共同模块、状态数、切换机制数和滞后能否获得足够事件与转移支持；疑似感染和基线 SOFA 标签在两个数据库中的可执行性；观测模型能否在缺失非随机、低行动重叠、整院接口缺失和数据库偏移下恢复预定不变量；不重新估计任何参数的冻结模型能否跨数据库保持评分、校准、状态对齐和结构稳定。筛选所用事件或参数下限不能替代经验有效样本量与模拟稳定性。

测量过程模型不能识别未测生理真值；低重叠关系只能解释为相应照护政策下的低支持关系。模拟恢复只覆盖预设生成情景，时间反转和阴性对照只能揭示部分偏倚。只重估结局校准参数、只重估观测方程或重新估计全部模型参数都改变了冻结模型的评价含义，不能替代不重新估计任何参数的外部验证。试验中的共同变量、观测映射和访视结局依赖原始语义、单位、时窗、实测覆盖与缺失处理假设；稀疏访视不支持连续轨迹插值。

### Unsupported claims and interpretation boundaries

观察性数据和较好的预测表现不支持真实因果网络、治疗因果效应、反事实策略、机制、中介、控制或数字孪生主张；条件性随机试验次要分析也不能验证未测潜在动力学、转移边或整个系统模型。当前计划不能写成已验证模型、临床决策工具、药物平台或无条件临床推广依据，也不能声称新算法、首次动态表型、首个脓毒症数字孪生、首个控制模型、首次外部验证或全球首次。2026 年版 Surviving Sepsis Campaign 对未获当地监管批准辖区使用 XueBiJing 的建议仍持谨慎态度，任何后续结果都不能据此作无条件国际临床推广。[4] 若未来两个试验的方向不一致或区间过宽，只能报告无支持或跨场景适用性有限，不能选择亚组改变主要解释。

### Research identity and substantive-change boundary

本次修订只改变叙事结构、术语定义、重复内容的位置和可复现记录的表达；研究问题、24 个月阶段 I–II 目标、纵向脓毒症中心 ICU 患者系统、文献与专家先验和公共 ICU 数据及条件性试验数据的核心证据基础，以及尊重患者与医院聚类的患者—时间状态和状态转移推断单位均保持不变。若后续取消发病前、发病、发病后和结局连续体，把研究改为普通预测，替换公共 ICU 与随机试验的核心证据基础，或改变主要推断单位，则须作为实质不同的新研究问题重新立项。

### Operational risks, bounded responses, and consequences

| Risk | Trigger | Bounded response | Consequence |
|---|---|---|---|
| 公共数据库访问或支持不足 | 月 3 没有两个可访问数据库；月 6 的事件、转移、共同锚点或医院支持不足 | 启动预指定备份；在拟合前改为 24 小时或事件时间；删除模块或边 | 没有两个数据库的全病程支持时，停止 24 个月跨数据库系统表征端点并保留资源不足记录 |
| 跨院患者破坏隔离或支持 | 患者跨适配与最终评价分区；剔除后少于 20 个医院、低于事件、转移或锚点标准，或排除超过 10% | 主要分析删除该患者全部记录；执行患者—医院组件敏感性分析；必要时启用备份数据库 | 不重新分配最终评价医院，不让患者跨集合；仍不足时只报告数据库级运输或描述结果 |
| 标签或时间信息泄漏 | 结果受后可用信息、同一时间格行动、未来测量频率或跨拆分处理驱动 | 修正按当时可用信息构造的查询，删除变量并重建可执行标签 | 高严重度泄漏未清除时不打开最终评价数据，相应端点不能获得支持 |
| 状态无法恢复或出现错误结构 | 状态、转移、错误发现率、区间覆盖率、零边错误结构或错设情景失配识别未达到标准 | 删除或合并状态与边，改用多状态、线性或仅预测模型 | 淘汰复杂候选，不以预测分数重新挽救 |
| 缺失非随机或行动低重叠 | delta tipping 改变解释；行动比例<5%或>95%，或加权有效样本量<20% 名义样本 | 报告敏感区间，合并或删除对象，并标明照护政策特异 | 不解释相应未测状态或治疗关系 |
| 冻结模型跨数据库运输失败 | 不重新估计任何参数时的 Brier、校准、状态对齐或符号标准未达到 | 分开报告只重估结局校准、只重估观测方程和全部参数重估 | 更新后的成功不算冻结模型的跨数据库成功 |
| 条件性试验数据或语义不足 | 个体数据、原始语义、随机化、中心、访视、生存或住院信息不能核验 | 只复现原终点或进行数据审计 | 不开展新的访视状态结局分析，不制造字段或连续轨迹 |
| 时间超限 | 月 12 无准入复杂候选；月 20 未冻结；月 24 无未触碰外部结果 | 分别封存当前较简单模型、延迟最终评价或封存已有外部准备记录 | 分别判定复杂候选、外部端点或阶段 II 最低交付未完成 |
| 最接近工作证据被过度外推 | 需要声称首次、专利不存在或全球不存在 | 开展系统综述、引文与专利检索和非英语数据库补检 | 当前只保留有界、条件性的整合与验证定位 |

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
