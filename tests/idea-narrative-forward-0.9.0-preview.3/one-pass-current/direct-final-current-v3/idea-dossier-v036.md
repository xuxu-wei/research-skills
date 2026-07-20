---
schema_version: research-idea.v3
plugin_version: 0.9.0-preview.3
artifact_id: idea-dossier-I01-001-v036
workflow_id: RID-SEPSIS-CSM-20260717-001
idea_id: I01-001
version_id: v036
path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v3/idea-dossier-v036.md
parent_idea_ids: []
based_on:
  - artifact_id: idea-dossier-I01-001-v003
    version: v003
    path: tests/idea-test-0.9.0-preview.1/0.9.0-preview.1/03_ideas/nodes/I01-001/dossiers/idea-dossier-v003.md
  - artifact_id: narrative-repair-plan-I01-001-r056
    version: r056
    path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/baseline-current/narrative-repair-plan-r056.yaml
  - artifact_id: language-assessment-r056
    version: r056
    path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/baseline-current/language-assessment-r056.md
  - artifact_id: protected-content-register-I01-001-v003-r003
    version: r003
    path: tests/idea-narrative-forward-0.9.0-preview.3/run-001/inputs/protected-content-register-v003.yaml
  - artifact_id: reader-handoff-forward-001
    version: v001
    path: tests/idea-narrative-forward-0.9.0-preview.3/run-001/inputs/reader-handoff.yaml
source_skill: multi-path-idea-generator
created_round: 56
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

# 脓毒症全病程候选动态系统表征：计划跨数据库检验与条件性稀疏随机对照试验次要再分析

## Title, summary, audience, and positioning

- **Title:** 脓毒症全病程候选动态系统表征：计划跨数据库检验与条件性稀疏随机对照试验次要再分析
- **One-sentence complete-Idea summary:** 本研究拟在 24 个月内以文献和专家知识约束，在 MIMIC-IV 与 eICU-CRD 两个重症监护病房（ICU）数据库中构建并检验脓毒症发病前、首次发病、发病后状态演化及结局的候选动态系统表征——即对患者时间状态及其转移作可检验描述而不预设因果机制——并交付可审计的模拟恢复、主要临床任务和未触碰跨数据库检验证据；此后仅在预设的试验数据、语义和跨数据映射条件成立时，才分别比较 EXIT-SEP 第 7 日与 XBJ-SCAP 第 8 日随机组的实测指标汇总结局，否则改做与阶段 II 模型独立、按死亡和出院分层的序贯器官衰竭评估（SOFA）访视结局次要分析。
- **Primary audience:** 重症医学、临床流行病学、纵向统计、系统辨识、系统科学、医学人工智能（AI）与转化研究共同体；当前不预设具体期刊。
- **Positioning and contribution frame:** 本项目的计划性贡献是候选表征的证据整合、跨数据库验证、可复用基准与资源，以及可证伪的研究治理。各单项模块已有先例；只有全过程时间处理、状态—行动—观察分离（把生理测量、治疗行为和测量过程分开建模）、预设模拟恢复标准、未触碰跨数据库检验和条件性随机对照试验层按计划衔接时，才可能形成增量的整合与验证价值。[26-38]

## Structured abstract

- **Background and gap:** Sepsis-3 为感染相关器官功能障碍提供操作基础，但疑似感染配对、SOFA 基线、观察窗和标签可用时间会改变电子健康记录中的发病定义。[1-3] 既有纵向、多状态、动态表型和跨库研究尚不能可靠回答：患者时间状态与结构能否在分开生理状态、治疗行动和测量过程后被恢复、审计并在另一数据库保持稳定。[26-37]
- **Objective and hypothesis:** 阶段 I（数据与模型开发）和阶段 II（跨数据库检验）的目标是在 24 个月内构建并检验一个知识约束、不确定性感知的全病程候选表征。核心假设是，若双库数据支持充分，并预先固定参照测量的载荷、符号和尺度，再对状态标签作置换和符号对齐，至少一种受限表示可在预设模拟中恢复，并在时间外、医院外和未触碰数据库中维持任务校准与对齐后结构稳定。
- **Approach:** 研究先审计数据访问、事件、医院、共同测量和时间支持，再锁定标签、状态、变量角色和医院拆分；随后依次检验竞争风险、多状态与线性状态空间基线，以及从预先列明的切换或非线性模型族中选出的至多一个候选模型。阶段 II 以两个主要分析任务、两个次要诊断性分析和隔离的跨数据库检验构成。
- **Expected result:** 计划产物包括可执行的标签与时钟协议、双库可观测性和变量角色审计、模拟恢复与弃权记录、主要任务及诊断结果、未触碰跨库结果和失败图。这些是拟生成的科学证据，不是现有模型或验证结果。
- **Contribution and impact:** 成功实施可提供一个有明确失败结果的全病程整合与验证框架，并说明哪些患者时间状态和结构能跨数据库解释。24 个月后的条件性随机对照试验（randomized controlled trial, RCT）次要分析只比较实际访视结局，不改变阶段 II 的成功判定。

## Background, current state, gap, significance, and rationale

### Background

脓毒症随时间形成，并与治疗和检测行为共同演化。Sepsis-3 将其定义为感染所致失调宿主反应引起的危及生命器官功能障碍，研究中常以相对基线 SOFA 增加至少 2 分操作化，但这并不产生唯一的电子健康记录发病时刻。[1,2] 疑似感染配对、SOFA 基线和观察窗的合理变化会改变病例与预测表现。[3] 因此，本研究区分临床事件时刻与标签可用时刻：前者表示事件发生，后者表示组成标签的信息在数据库中已经可计算；每次分析只使用当时已经可见的信息。

### Current state

MIMIC-IV、eICU-CRD、HiRID 和 AmsterdamUMCdb 提供纵向生命体征、实验室、治疗与结局，但中心、年代、采样和接口不等价。[5-8] BlendedICU 与 ricu 说明跨库统一只能在单位、语义、时间戳和可见性均可审计的共同概念上成立。[9,10]

多状态 Markov、SOFA 或生命体征轨迹、动态表型、隐马尔可夫模型和器官交互图已描述发病后演化；观察性决策过程和状态空间模型已处理干预条件下的转移；脓毒症数字孪生、模型预测控制、离线强化学习、跨库验证及 RCT 表型—治疗二次分析也已有代表性工作。[26-37] 这些研究说明各组成方法均非空白，也表明时间错位、照护政策和跨数据库差异会限制解释。

### Gap

现有证据仍不能可靠判断：在发病前在险时段、首次发病、发病后互斥状态和结局组成的同一研究对象中，是否存在可由数据恢复、可审计且能跨数据库比较的患者时间状态及结构。仅有预测准确度不能区分可迁移的生理结构与特定数据库中的治疗和测量政策，也不能证明潜在状态得到识别。

### Significance

回答这一问题将决定研究者能否把跨库预测表现解释为患者状态的稳定证据，哪些关系只能视为数据库或照护政策特异，以及何时应停止结构解释。明确这些界限可避免把采样、接口或治疗行为误写为生理机制，并为后续验证、资源建设和审慎的试验再分析提供可追溯依据。

### Rationale

本研究用双时钟控制未来信息，用状态—行动—观察分离来区分生理测量、治疗行为和测量过程，再用固定绝对阈值的模拟恢复检验判断候选表示能否重建已知结构。最后，医院优先的适配区与未触碰测试区检验这些结果能否跨数据库保持。该顺序直接对应数据可计算性、状态可恢复性和跨库稳定性三个证据缺口；阶段 III（条件性试验再分析）仅作为阶段 II 完成后的下游扩展。

## Research question, objectives, and core hypothesis

### Primary research question

能否构建一个知识约束、不确定性感知的 ICU 患者候选动态系统表征，使其覆盖以脓毒症为中心的发病前、首次发病、发病后和结局连续体，在医院和数据库之间检验患者时间状态与候选结构的有效性，并在预设条件成立时进一步比较稀疏 RCT 实际访视中由实测指标形成的结局？

### Objectives

1. **全病程边界与可追溯时钟：** 锁定实时可实施的主 Sepsis-3 标签、标签可用时间、固定预测时点（landmark）风险集、互斥发病后状态与竞争事件，并用两种合理标签作敏感性分析。
2. **审计约束的候选状态表示：** 由双库可观测性审计确定共同模块、时间方案和复杂度上限，显式分离生理状态、治疗行动和观察过程，并只解释对齐后可比较的量。
3. **绝对模拟恢复与计划性跨数据库检验：** 以固定阈值而非相对模型排名检验正确、零边、过拟合和错设生成情景；在第二数据库隔离适配区与未触碰测试区，检验两个主要分析任务和两个次要诊断性分析。
4. **条件性稀疏 RCT 次要再分析：** 在阶段 II 先完成且每项试验的适用条件成立时，分别比较 EXIT-SEP D7 与 XBJ-SCAP D8 的实测指标汇总访视结局；跨数据映射不成立时，转入与阶段 II 模型独立的死亡/出院分层 SOFA 次要分析。

### Core hypothesis

若共同测量与事件支持达到预设数据就绪条件，状态维度、状态机制数、滞后阶数、识别与尺度约束均在建模前固定，且候选模型达到模拟恢复标准，则部分状态占用、转移概率、参照测量预测及预设依赖的符号和滞后可在未触碰外部库中维持预定义稳定性。五条证据链分别对应数据边界、可恢复表示、任务效度、跨库稳定性和条件性试验输出；观察性任务检验的仍是实际照护与测量政策下的表示，而不是治疗因果效应。

## Research content and work packages

本节规定时间、依赖和阶段交付。数据就绪条件（G1）是月 4–6 对两库访问、事件、转移、医院、共同测量、接口和时间支持是否足以进入建模的综合判定；它不是模型性能标准。

### Twenty-four-month minimum and dated milestones

阶段 I–II 的最低顺序为：资源确认与 G1 → 标签、状态和医院拆分固定 → 简单基线 → 模拟恢复与假结构检查 → 至多一个切换或非线性候选模型 → 两个主要分析任务和两个次要诊断性分析 → 开发冻结 → 未触碰跨数据库检验。阶段 III 位于 24 个月最低交付之后。

| 时间与里程碑 | 必须交付 | 完成判定与后续动作 |
|---|---|---|
| 月 0–3：资源确认 | 两个主库的团队访问、数据使用协议（DUA）、存储和算力确认；临床、统计、系统辨识与数据工程角色具名；备份库角色预指定 | 任一主库不可承担角色即启动备份；月 3 仍无两个可访问数据库则停止 24 个月跨库路线 |
| 月 4–6：G1 与协议冻结 | 双库队列流、事件/转移、医院、跨院患者、共同测量、接口和缺失审计；标签、时钟、状态、拆分、时间方案和参数上限冻结 | 12 小时方案无支持时，在建模前改为并预先固定 24 小时或事件时间；支持仍不足则降级或停止跨库阶段成功判定 |
| 月 7–12：模型恢复与准入 | 简单基线、Monte Carlo 与半合成检验；至多一个附加候选模型及阈值冻结 | 候选模型未达到关键恢复、零边或错设标准即退回线性、多状态或仅作预测的分析 |
| 月 13–18/20：开发冻结 | 开发库内部、时间外和医院外验证；标签、预处理、模型、阈值及评价代码形成校验和包 | 主要任务或泄漏检查未达到预设标准则不开放最终外部测试；月 20 后不按测试结果修改 |
| 月 21–24：未触碰外部检验 | 第二数据库测试区完全冻结参数的外部测试结果，以及适配区学得的有限更新结果和失败图 | 按合取标准判定阶段 II；未达到标准仍交付基准与资源，但不称跨库表征成功 |
| 24 月后：条件性 RCT 分析 | 阶段 II 完成；试验数据、语义和跨数据映射资格逐试验核验；输出分开报告 | 仅开展适用条件允许的访视结局分析；任何试验结果均不补足阶段 II |

### Conjunctive minimum success definition

阶段 II 的计划性成功必须同时满足：两库可构造主要队列并达到冻结的数据支持下限；附加候选模型若进入则达到绝对模拟恢复、零边和错设标准；两个主要分析任务达到预设的适当概率评分与校准标准；高严重度泄漏清零；未触碰外部测试在完全冻结参数时达到任务、状态对齐和结构稳定标准。适配区学得的有限更新与完全冻结参数的结果分开报告，不能替代后者未达到标准。阶段 III 不计入该判定。

### Work packages and minimum route

| 工作包 | 月份 | 主要工作 | 交付 |
|---|---:|---|---|
| 工作包 1：标签、队列和 G1 | 0–6 | 访问与版本、样本流、双时钟、变量角色、跨院患者、时间网格和接口审计 | 可执行风险集、多状态、医院优先拆分和共同测量清单 |
| 工作包 2：知识结构、基线与模拟恢复 | 3–12 | 候选图、预设识别与尺度约束、简单基线、Monte Carlo 与半合成分析 | 达到标准的至多一个附加候选模型，或明确降级模型 |
| 工作包 3：主要任务与诊断 | 8–18 | 未来 12 小时首次发病风险、第 7 日状态占用、伪遮蔽重建、未来轨迹诊断及敏感性分析 | 适当概率评分、校准、覆盖、泄漏和弃权记录 |
| 工作包 4：隔离的跨库检验 | 14–24 | 冻结包；医院级适配/测试拆分；跨分区患者处理；零更新与有限更新 | 未触碰外部结果、排除审计、跨库状态分类和失败图 |
| 工作包 5：条件性阶段 III | 24 月后 | 逐试验核验语义、共同测量和冻结映射；分析访视结局 | EXIT-SEP 与 XBJ-SCAP 分开的次要分析或停止记录 |

## Data, materials, and existing evidence base

### Current resource and evidence status

资源证据状态在本节统一为“已核实、未核实、尚未生成、仅有项目内衍生材料”。

| 资源或结果 | 当前证据 | 资源证据状态 | 后续要求 |
|---|---|---|---|
| MIMIC-IV v3.1 与 eICU-CRD v2.0 的公开存在、版本和文献 | PhysioNet 与原始数据库论文提供稳定 DOI 和版本记录。[5,6] | 已核实 | 不等于团队可访问或项目队列可执行 |
| 团队访问凭证、DUA、下载/存储、提取版本与 checksum | 当前材料未提供完成记录 | 未核实 | 月 3 前确认；否则启动备份或停止跨库路线 |
| 双库样本、事件、转移、医院、跨院患者、共同测量和接口支持 | G1 尚未执行 | 尚未生成 | 月 6 前生成并冻结 |
| EXIT-SEP 与 XBJ-SCAP 本地验证报告 | 两份报告记录工作簿构建与复现/QC，但不是独立同行评审或原始审计。[22,24] | 仅有项目内衍生材料 | 不替代个体数据授权、CRF/SAP 或数据持有人确认 |
| RCT 个体数据授权、原始病例报告表（CRF）/统计分析计划（SAP）、随机化、中心、访视时序及生存/住院/出院语义 | 现有衍生报告未完成原始语义证明 | 未核实 | 影响估计目标的核心语义无法核验时停止新访视结局分析 |
| 阶段 II 与试验的共同生理测量、单位和实际访视映射 | 白细胞计数（WBC）/C 反应蛋白（CRP）等只是候选；D-dimer 单位等仍有缺口 | 未核实 | 每项试验另行核验，不推测缺失字段或单位 |
| 所需团队角色 | 职责已定义 | 已核实 | 角色规范不等于人员承诺 |
| 具名人员与可用工时 | 无可核验名单或承诺 | 未核实 | 月 3 前具名 |
| 模型、模拟恢复、预测、外部测试或 RCT 新分析结果 | 当前没有已生成结果 | 尚未生成 | 按时间表生成，不能在标题或摘要中写成既有结果 |
| 截至 2026-07-17 的最接近工作刷新 | 项目内有界检索汇总正式论文、预印本和注册记录 | 仅有项目内衍生材料 | 支持模块非新颖判断；完整组合缺口只具低至中等置信 |

### Public ICU database roles and G1 audit

- **开发库：** MIMIC-IV v3.1，用于标签与模型开发、内部和时间外验证；须核验凭证、DUA 和确切表版本。[5]
- **外部库：** eICU-CRD v2.0，用于医院级适配和未触碰测试；整院接口缺失按医院审计。[6]
- **备份库：** HiRID 或 AmsterdamUMCdb 只能在月 0–3 预先指定并完成同等审计后替代失败角色，不能在查看测试结果后选择。[7,8]
- **共同概念：** 仅保留单位、语义、时间戳和可见性均可审计的变量；数据库特异信息只进入探索性观测模型。[9,10]

| G1 审计字段 | MIMIC-IV 开发库 | eICU 外部库 | 使用条件 |
|---|---|---|---|
| 访问/DUA、版本、提取日期/checksum | 待 G1 | 待 G1 | 未完成不得承担确认性角色 |
| 成年患者、住院、ICU 住院记录（stay）、可链接重复 stay | 待 G1 | 待 G1 | 每次住院仅首个合格 stay；可链接重复住院仅患者首次合格住院 |
| 医院及每院患者数 | 待 G1 | 待 G1 | 外部测试至少 20 个有事件支持的医院 |
| 12 小时 landmarks 与首次发病事件 | 待 G1 | 待 G1 | 每个自由风险参数在开发/外部至少 20/10 个事件 |
| 出 ICU 存活、死亡、转院/失访、行政结束 | 待 G1 | 待 G1 | 分开计数；稀少类可合并为其他终止，但不作普通独立删失 |
| incident/delayed-entry 人群与允许转移 | 待 G1 | 待 G1 | 每个自由转移参数在开发/外部至少 20/10 次转移 |
| 时戳精度与随访 | 待 G1 | 待 G1 | 不支持 12 小时排序则在建模前改为 24 小时；仍不足则用事件时间 |
| 参照测量的单位、源表和可用时间 | 每项待填 | 每项待填 | 单位或可用时间不清者退出共同层 |
| 参照测量密度 | 每项待填 | 每项待填 | 每维至少两个共同测量；各库每项至少 30% 合格时间格实测 |
| 医院接口与患者覆盖 | 每项待填 | 每项待填 | 至少覆盖 70% 合格医院和 80% 合格患者 |
| 缺失、观察间隔与跨院链接 | 待填 | 待填 | 保留缺失指示、实测时刻和间隔；不无条件向前填充 |
| 有效支持与复杂度上限 | 待计算 | 待计算 | 潜在状态维度 K=min(通过模块数,4)，状态机制数≤3；事件/参数比不足则继续降维 |

主时间方案为 12 小时；24 小时与事件时间是预写的敏感性或降级路线。除有明确起止的输注、器官支持状态和静态基线外，不作无条件向前填充；每个动态值保留是否实测、实测时刻和距上次实测时间。

### Candidate variable-role firewall

| 主角色 | 示例与允许用途 | 双重用途处理 |
|---|---|---|
| 生理测量 Y_t | 实测生命体征、血气/实验室、器官功能测量及 G1 保留的参照测量 | 不含治疗启停、剂量或测量频率；同源 SOFA 标签副本进入隔离标签管线 |
| 治疗行动 A_t | 抗菌药、液体、血管活性药、机械通气、连续性肾脏替代治疗（CRRT）、激素的启停或剂量 | 不作潜在生理参照测量；用于恶化标签时生成带事件时戳的隔离副本 |
| 测量过程 M_t | 是否检测、次数、间隔、医嘱/采样/结果可用时刻和医院接口 | 未检测不等于正常；接口缺失不作患者状态 |
| 仅作标签 | 疑似感染配对、隔离 SOFA 事件、互斥状态、死亡/出院/转院 | 不进入相同或更早 landmark；抗菌药双用遵循可用时间并与行动通道分离 |
| 基线协变量 B | 年龄、性别、入院类型/来源、既往病史等 landmark 前固定信息 | 不复制为伪时间测量；未知值显式编码 |

### Local RCT evidence and present limits

EXIT-SEP 在中国 45 个 ICU 随机 1,817 例 Sepsis-3 患者。本地衍生报告记录 1,760 例 28 日状态明确、395 例死亡、57 例状态未知，SOFA D1/D4/D7 非缺失为 1,750/1,542/1,296，乳酸 D1–D7 由 855 降至 223。[17,21-23]

XBJ-SCAP 随机 710 例重症社区获得性肺炎患者。本地衍生报告记录 FAS 675、PPS 617、FAS 且基线 SOFA≥2 的操作性 sepsis-like 人群 671、严格重叠 658；SOFA D0/D4/D8 非缺失为 703/628/610，WBC 为 704/634/614，CRP 为 579/503/467，28 日状态 675。[18,24,25] SCAP 入组不等于确认 Sepsis-3；PaO2/FiO2、乳酸、休克、CRRT、CNS 等患者级变量不可用，D-dimer 单位尚需核验。

## Research design and methods

### Protocol locks for the two primary clinical tasks

阶段 II 包含两个主要分析任务和两个次要诊断性分析。第一项主要任务的估计目标是未来 12 小时首次发病累积发生风险；第二项是发病后第 7 日有利状态占用概率。概率型适当评分（proper score）是对完整预测概率分布进行评价、并在真实分布处期望最优的评分。

| 项目 | 发病前主要分析任务 | 发病后主要分析任务 |
|---|---|---|
| 人群 | ≥18 岁；每次住院首个合格 ICU stay；至少 12 小时可见历史；landmark 尚未达主标签。观察起点已发病者排除 | 首次 incident onset；入 ICU 已发病者仅在首个可审计时点 delayed entry，分层并左截断 |
| 事件时钟 | 疑似感染使用微生物标本采集与系统抗菌药首次实际给药配对：采集先则药在 72h 内，给药先则采集在 24h 内；感染时刻取较早。无已记录慢性器官功能障碍者 baseline SOFA=0；有记录者取入 ICU 前 24h 最低可计算 SOFA，不可审计则不入主风险集。成分在滚动 24h 取最差，SOFA 相对 baseline +2 必须在感染前 48h 至后 24h，onset 为首次可排序满足时刻。[1,2] | incident 以主 onset event time 为零点；后发病状态按临床 event time 进入 |
| 标签可用时钟 | 配对较晚事件及必要 SOFA 数据在源系统可见或最终化时刻取最大值，之后信息不回填到事件时刻 | 恢复需连续 24h，可用时间为窗结束；恶化、死亡、出院和转院以记录可用时刻为准 |
| Landmark/历史/预测窗 | ICU 第 12h 起每 12h；此前最多 24h、至少 12h 截至该预测时点已经可见的历史（as-of 历史）；未来 12h 首次 onset | onset/延迟入组（delayed entry）后每 12h；主时间点为病程第 7 日，14 日作敏感性分析 |
| 首次发病与重复 | 只分析首次 onset；重叠 landmark 保留，但每次住院总权重为 1；按患者与医院聚类 | incident 与 delayed entry 分层；delayed entry 不反推 onset |
| 竞争/中间事件 | onset 前活着出 ICU、院内死亡、转院/失访为互斥终止；行政结束独立删失并作逆概率删失加权（IPCW）/界限检查 | 死亡、活着出 ICU、转院为终止状态；恢复不由出院代替；作 IPCW 敏感性分析 |
| 同一时间格顺序 | landmark t 特征仅允许可用时间<t；[t,t+12h) 新行动为 A_t，下一边界的实测生理为 next-state；同戳无法排序者不用于该边 | 同样处理；器官支持是行动，隔离事件标签只在形成后定义恶化 |
| 估计目标/模型 | 条件于历史的未来 12h 首次 onset 累积发生函数（CIF）；离散 multinomial cause-specific hazard 转 CIF | 第 7 日“生理恢复或活着出 ICU”有利集合占用概率，二者另报；互斥离散多状态/Aalen–Johansen |
| 指标 | 12h Brier、绝对校准截距/斜率；精确率—召回率曲线下面积（AUPRC）、提前量和假警报为次要 | 第 7 日多类别 Brier 与有利状态绝对校准；各状态/转移校准为次要 |
| 不确定性 | 患者总权重；患者/医院分层自助法（bootstrap）95% 区间 | 患者/医院层 bootstrap；incident/delayed-entry 分层并报有效转移数 |
| 预设通过标准 | 开发及未触碰测试均须 Brier 相对最强简单基线差值的上侧 95% 界不超过 +0.01、校准斜率 0.80–1.20、绝对风险误差≤0.02，并清除高严重度泄漏 | 同一标准；次要诊断不能改变主要任务判定 |

主标签之外仅两种敏感性：培养—抗菌药改为对称 ±24h；所有人使用感染前 24h 最低可计算 SOFA，并把器官功能窗限制为前后各 24h。敏感性结果单独报告，不替代主结果。泄漏审计检查 onset 后生理或治疗、尚未可用的培养或抗菌药、同一时间格行动、未来测量频率、跨拆分插补或标准化、患者或 stay 跨集合、重叠窗口权重，以及由结局决定变量、时间网格或阈值。

### Mutually exclusive post-onset state/event system

每 12 小时赋值，优先级固定为：死亡 > 转院/无法继续观察 > 活着出 ICU > 恶化/新器官衰竭 > 生理恢复 > 持续脓毒症。源时间无法排序时使用更高优先级，并作事件时间敏感性分析。

| 状态/事件 | 操作定义与可用时间 | 角色保护 |
|---|---|---|
| 持续脓毒症 | ICU 内存活且未满足其他状态；transient | 隔离为仅作标签，不作参照测量 |
| 生理恢复 | 相对 onset 参考 SOFA 下降≥2 且连续 24h 无新恶化；event 为窗起点，可用时间为窗结束；可复发 | SOFA 仅作标签；无支持升级只是标签条件，行动留在 A_t |
| 恶化/新器官衰竭 | 相对此前 24h 最低 SOFA +2，或新启/升级血管活性药、有创通气或 CRRT；同时发生只记一次 | 生理与行动派生标签副本隔离；行动不作参照测量 |
| 活着出 ICU | 存活离开 ICU；absorbing | 不等于生理恢复；去向另报 |
| 转院/无法继续观察 | 转往不可追踪 ICU/医院或记录终止；terminal competing | 不编码为恢复或普通独立删失；作 IPCW/界限分析 |
| 死亡 | ICU 内或可追踪病程死亡；absorbing | 不作 MAR 缺失；同戳优先 |

### Observational target, identification, alignment, and abstention

令潜在患者状态为 X_t，生理测量为 Y_t，行动为 A_t，测量指示或强度为 M_t，基线为 B，数据库或医院为 S。主要目标是在实际照护与测量政策下估计联合预测/生成分布 p(X_0:T,Y_0:T,M_0:T,A_0:T | B,S)，及其导出的风险、对齐状态占用和转移、参照测量预测以及预设符号和滞后。

预设识别与尺度约束用于解决潜在状态的尺度和符号不确定性：每个维度至少两个跨库参照测量；首个参照测量的载荷固定为 +1 并标准化尺度；非指定交叉载荷为 0 或按预写稀疏模式处理；K≤4、状态机制数≤3，滞后仅 1 或 2 个冻结时间格；允许图无同一时间格瞬时循环。20 个固定随机种子拟合后执行状态标签置换与符号对齐。对齐后可解释量仅包括状态占用、转移概率、参照测量层预测和预设边的符号或滞后。

非随机缺失（MNAR）敏感性主拟合使用显式测量过程的 MAR/selection 基线，并对未测生理值执行 pattern-mixture delta −1、−0.5、0、+0.5、+1 个开发库标准差及 selection tipping-point。每个对齐状态、医院和时间层报告行动概率与有效样本量（ESS）；行动比例<5%或>95%，或加权 ESS<20% 名义样本时，不估计相应治疗作用。任一状态或边若 20 个随机种子的对齐率<90%、bootstrap 保留率<80%、外部符号一致率<80%、状态对齐<0.70 或区间未校准，则删除、合并或归为仅数据库或照护政策特异。

### Absolute simulation and semi-synthetic recovery standards

月 7–10 在不读取临床最终测试结果的条件下，每个核心情景至少运行 1,000 次重复，或运行至关键比例的 Monte Carlo 标准误≤0.02。生成器包括正确指定、零边或独立状态、多余状态或过拟合、遗漏状态、错误滞后或观测模型，并交叉改变状态分离、切换率、1/2 时间格滞后、政策反馈、隐藏混杂、MNAR、标签误差、访视密度、整院接口缺失和数据库漂移。

| 恢复量 | 预设通过标准 | 未达到标准后的动作 |
|---|---|---|
| 状态恢复 | 离散调整 Rand 指数（ARI）或连续主要典型相关≥0.80；20 种子对齐≥90% | 合并或删除状态，或退回线性/多状态模型 |
| 转移概率 | 主要允许转移的平均绝对误差（MAE）≤0.05；95% 覆盖率为 0.90–0.98 | 删除该转移或停止结构解释 |
| 预设符号/滞后 | 正确恢复率≥0.80 | 该边不进入共同结构 |
| 边检测 | 敏感度≥0.80 且错误发现率（FDR）≤0.10 | 降低稀疏度或降维；仍未达到则仅作预测 |
| 零边假结构 | 任一假边 95% 区间排除 0 的重复比例≤0.05 | 淘汰附加候选模型，不通过调阈值挽救 |
| 错设假置信与弃权 | ≥80% 重复触发失配或弃权；错误结构高置信≤0.05 | 淘汰或只解释已恢复量 |
| 概率校准 | 斜率 0.80–1.20；绝对概率偏差≤0.02 | 仅重校准不能修复结构未恢复，须降级 |

### Hospital-primary genuine cross-database validation

在任何结局导向选择前，先按合格体量四分位和接口完整性分层，以固定种子 20260717 对 eICU 医院 ID 哈希：30% 医院分配至适配区，70% 分配至未触碰测试区。医院分区优先于患者规则；分区表、链接算法版本和 checksum 在查看测试结局前冻结。

1. 完成医院哈希后，只用患者链接键识别跨院记录。患者若跨适配区与测试区，其全部记录从主要外部分析排除，不按患者哈希重分配。
2. 仅出现在同一分区的患者保留预定义的首次合格住院及首个合格 ICU stay，同一患者不跨集合。
3. 在揭示测试性能前，报告跨分区排除人数、比例、涉及医院数及结局前可得的年龄、性别、入院类型/来源、首个 landmark 生理负担和观察密度。
4. 敏感性分析使用“以测试区为主的患者—医院连通分量规则”：冻结医院角色后建立患者—医院二部图；纯适配或纯测试分量保留原角色；混合分量从适配区删除相关患者记录，只保留预分配测试医院中的首次合格 stay。测试医院不移入适配区，也不借用测试数据训练。
5. 独立数据保管人在不释放模型性能的条件下检查支持。若测试区少于 20 个合格医院、任一自由风险/转移参数少于 10 个事件/转移、共同测量不再覆盖至少 70% 合格医院和 80% 患者，或跨分区排除超过原合格测试患者或主要事件的 10%，则启动预指定备份库；仍不足时只报告数据库级运输或描述。

冻结标签、变量协调、状态、预处理、可用时间、模型、超参数、阈值和评价代码后，测试区按以下顺序执行：零更新，即不在外部测试库重新估计任何参数；仅校准更新，即只在适配区估计预测时间范围特异的截距和斜率；仅观测层更新，即只在适配区更新观测模型而冻结状态与转移。全模型重新拟合属于运输更新和新一轮开发，不属于外部验证。测试区不参与变量、时间方案、状态数、参照测量、分区、更新层级或阈值选择。

### Conditional trial-observation projection and independent alternative analysis

本小节是阶段 III 的完整技术规范。两项访视结局均为原试验结果之后提出的次要、探索性再分析；原 28 日终点复现独立报告，两试验不合并。每项试验 r 的映射、阈值、代码和随机种子均在治疗组比较前冻结。

**试验语义与共同测量适用条件（R0）。** 阶段 II 必须先完成并冻结；须获得个体级分析授权，并由原始 CRF/SAP、数据字典或数据持有人确认随机化与分析集、中心或分层因素、D7（EXIT-SEP）或 D8（XBJ-SCAP）相对随机化和首剂的实际访视窗，以及死亡、住院、活着出院和转院语义。候选共同集 C_r 只含阶段 II G1 保留、在实际访视直接测得、构念/标本/单位一致或有预先验证确定性转换、采样和结果可用时刻位于冻结访视窗，且不属于治疗、测量频率、SOFA、结局标签或事后状态的生理测量。每项试验至少两个合格共同测量。WBC/CRP 只是当前候选；单位不明的 D-dimer 和不存在字段不进入。共同测量不足两个时不建立跨数据映射；若 SOFA 及试验核心语义可核验，转入独立 SOFA 分析。

**冻结的确定性映射。** 对试验 r 的 C_r，使用 MIMIC 开发集锁定的均值、标准差和第 1/99 百分位截断得到 Z_C；从阶段 II 冻结观测方程 Z_C=a_C+L_C X+e 对 L_C 作奇异值分解（SVD），取第一奇异向量组 L_C=UDV'。阶段 II 潜在状态的一维投影定义为 P_state=V_1'X；由试验实际测量指标计算的一维代理定义为 P_obs=D_1^(-1)U_1'(Z_C−a_C)。奇异值并列时按预先固定的测量字典序决胜；符号在阶段 II 开发集固定为与同日 SOFA 总分非负相关，使数值越高表示状态越不利。映射不使用 RCT 治疗分组、RCT 结局或试验间合并数据；每项试验有自己的 C_r 和映射。

**测量不变性、校准与投影忠实度适用条件（R1）。** 先在阶段 II 未触碰 eICU 零更新测试的相应发病后 D7/D8 窗验证，不按 RCT 结果调参。必须同时满足：第一奇异轴解释 L_C Frobenius 能量≥50%；P_state 与 P_obs 相关≥0.70；相对 P_state 标准差的归一化 MAE≤0.50；回归 P_state=α+βP_obs 的 |α|≤0.20 SD、β=0.80–1.20、95% 区间覆盖为 0.90–0.98；每个共同测量的外部校准斜率为 0.80–1.20、标准化截距绝对值≤0.20。随后在遮蔽治疗标签的试验数据中检查：至少 80% 观测值落在冻结阶段 II 生理合理范围，且至少 60% 的访视时存活在院者可由不少于两个实测指标直接计算 P_obs。任一标准未达到、单位或时间不变性不成立，或需要试验特异重新估计权重时，不进入映射分支，且不以随机组差异挽救。

**跨数据映射成立时的估计目标。** D7/D8 前死亡置最差层；访视时存活在院者按 P_obs 从高到低排序；访视前活着出院置单独最有利层。主要比较为与中心或分层随机化相容的概率指数/胜率（probabilistic index/win probability），表示随机分组在该按死亡和出院分层的访视结局上的差异。

**与阶段 II 模型独立的 SOFA 访视结局次要分析。** 若 R0 的共同测量部分或 R1 不成立，但该试验的 SOFA、死亡、住院/出院、随机化和中心语义可核验，则使用预先固定的独立结局：死亡最差；访视时存活在院者按 SOFA 从高到低；活着出院最有利。若核心 D7/D8 或随机化、中心、生存语义也无法核验，则停止新访视结局分析，只做原终点复现或数据审计。

| 试验 | 人群与访视 | 缺失、死亡和分析 | 多重性与停止条件 |
|---|---|---|---|
| EXIT-SEP | 随机 1,817；目标为所有随机分配者的治疗策略估计目标（all-randomized treatment-policy）。已知结局 1,760 仅称完整结局子集。实际第 7 日（D7）；第 1 日（D1）若在随机化后，不作未受影响 baseline | 死亡/活着出院按层级处理；存活在院但 P_obs 或 SOFA 缺失时，在每个多重插补（MI）数据集中用治疗、中心、确认的随机化前协变量和既往实际访视信息插补后重算冻结结局，再以 Rubin/cluster bootstrap 合并；delta ±0.5/±1 SD 和 best/worst tipping；转院或未知状态作界限，不作 MAR | 遵循中心/分层；两个试验的主要访视结局组成 Holm 家族错误率（FWER）0.05 家族；其他访视或模块作探索性 FDR；亚组只报告 treatment×subgroup interaction。关键 D7 或中心语义无法核验则停止 |
| XBJ-SCAP | 随机 710 为目标；无法重建全随机集时降级为全分析集（FAS）675 例的改良意向治疗（mITT）分析并明示；符合方案集（PPS）、操作性脓毒症样 671 例和严格重叠 658 例仅作敏感性。实际第 8 日（D8）；第 0 日（D0）若非随机化前，不作 baseline/change | 同一死亡/出院、MI、delta、tipping 和界限策略；不填补结构性不存在的 PaO2/FiO2、乳酸、休克、CRRT 或 CNS；D-dimer 单位未核验即排除 | 同一 Holm 家族；亚组只报交互；全随机集不可重建则明确 mITT；关键 D8、中心或生存语义无法核验则停止 |

稀疏 D1/D4/D7 或 D0/D4/D8 仅支持访视特异或离散变化，不插值为伪连续轨迹。两试验的人群、访视、共同测量或估计目标不同即保持独立。

### Secondary representation diagnostics

部分状态重建使用伪遮蔽平均绝对误差、均方根误差（RMSE）、对数评分和区间覆盖；未来轨迹使用连续分级概率评分（CRPS）、负对数似然、状态占用与结局校准。伪遮蔽只对原本已测值有效。诊断按变量、状态、医院与观察密度分层，并作为表示质量证据，不改变主要分析任务的判定。

## Key techniques and implementation

本节规定可版本化实现对象及其接口；科学估计目标和阈值由方法规范控制，不在此重复。

| 实现对象 | 输入 | 输出 | 持久化记录 | 接口与冻结边界 |
|---|---|---|---|---|
| 双时钟标签包 | 原始事件表、SOFA 成分、标本与用药时戳、标签版本 | event time、label-availability time、主/敏感标签、样本流 | 源表、字段、时戳、排除原因和单元测试日志 | 向风险集与状态构建器供数；协议冻结后版本变更须重建全链 |
| G1 审计包 | 访问记录、患者/stay/医院链接、事件/转移、单位、接口、密度和缺失 | 两库支持矩阵、时间网格、共同测量和复杂度上限 | DUA/版本/checksum、计数表、签署与决定记录 | 向协议、模型注册和医院拆分供数；月 6 冻结 |
| 变量角色注册表 | 字段字典、临床裁定、可用时刻 | Y_t、A_t、M_t、仅作标签和 B 的单一主角色 | 双用副本、隔离与 lag 断言 | 连接特征查询、标签和观测模型；每版数据提取均校验 |
| 基线与模型准入流水线 | 冻结队列、角色注册、候选图和模拟情景 | 简单基线、候选模型结果、准入或降级决定 | 随机种子、参数、恢复指标、假结构和弃权日志 | 只向通过准入的冻结模型开放主要任务；候选至多一个 |
| 识别与状态对齐注册 | 共同测量、载荷与尺度约束、20 种子拟合 | 状态标签映射、符号对齐和对齐后可解释量 | 参照测量顺序、置换、符号、保留/删除量 | 连接跨库比较、状态图和解释输出；开发冻结后不改 |
| MNAR 与政策支持诊断包 | 测量过程、未测值、行动概率和医院接口 | delta/tipping、overlap、ESS、接口压力结果 | 分层支持表、敏感性区间和不解释标记 | 向主要任务、跨库分类和失败图提供诊断；与模型版本绑定 |
| 医院分区与外部冻结清单 | eICU 医院、患者链接、固定种子、模型包 | 适配区/测试区、排除表、零更新和有限更新运行清单 | 哈希、二部图、权限日志、checksum 和揭盲时间 | 独立保管人控制测试访问；月 20 后输入只读 |
| RCT 观测映射包 | 冻结阶段 II 观测方程、逐试验共同测量、CRF/SAP 语义 | P_state/P_obs 映射、R0/R1 结果和所选分析分支 | 单位、访视窗、SVD、符号、范围和治疗标签遮蔽记录 | 每项试验独立接入访视结局分析；治疗比较前冻结 |
| 不确定性与多重性规范 | 患者/医院聚类、模拟重复、缺失模式、中心和结局家族 | bootstrap、Monte Carlo 标准误、MI 合并、Holm/FDR 结果 | 重采样种子、插补模型、tie rule 和家族定义 | 供所有估计输出调用；首次确认性运行前版本冻结 |
| 负向控制与失败发布包 | 时间反转、临床预裁定阴性对照、所有准入和外部记录 | 阴性对照结果、缺失与降级档案、失败图和可复用资源 | 分析版本、失败触发点、替代路线和发布清单 | 接收全流程记录；无论模型或跨库结果如何均形成交付 [16] |

## Evidence chains

### Evidence chain: 可用时间、风险集与互斥病程

- **Input:** Sepsis-3、标本/抗菌药与 SOFA 时戳、死亡/出院/转院事件、公共 ICU 数据字典和 G1 审计。[1-10]
- **Method / analysis / processing:** 主标签与两种敏感标签；事件/可用双时钟；12 小时 landmark；首次发病和 delayed entry；互斥状态、竞争事件、患者权重与泄漏断言。
- **Output:** 可执行的未来 12 小时首次发病 CIF 队列、第 7 日多状态队列、标签差异矩阵与泄漏报告。
- **Supports:** 目标 1，以及候选表示覆盖发病前、首次发病、发病后和结局的可审计边界。

### Evidence chain: 数据支持、状态识别与模拟恢复

- **Input:** 双库共同测量、接口、事件与转移审计，知识先验、变量角色注册，以及正确、零边、过拟合和错设生成器。
- **Method / analysis / processing:** 复杂度限制；预设识别与尺度约束；状态对齐；Monte Carlo；MNAR、政策反馈、接口缺失和数据库漂移压力分析；绝对恢复、FDR、coverage 和假结构检验。
- **Output:** 达到全部准入标准的至多一个切换或非线性候选模型，或明确降级的多状态、线性或仅作预测的基准，附删除、合并与弃权清单。
- **Supports:** 目标 2 与 3 中对齐后可解释、且可由预设生成情景恢复的患者时间状态和转移。

### Evidence chain: 两个主要分析任务与两个次要诊断性分析

- **Input:** 冻结队列与状态、准入模型、开发/时间外/医院外切分和预设指标。
- **Method / analysis / processing:** 未来 12 小时首次发病 CIF、第 7 日状态占用、适当概率评分、校准、聚类 bootstrap、伪遮蔽和未来轨迹诊断，以及标签、MNAR、行动/观察消融和负向控制。
- **Output:** 两个主要任务的 Brier、校准与状态概率，两个诊断性分析的评分、覆盖和按中心、亚组及观察密度分层的图。
- **Supports:** 目标 3 的患者时间任务效度与阶段 II 合取成功判定。

### Evidence chain: 医院优先的未触碰跨数据库检验

- **Input:** 开发冻结包、按医院预分配的 eICU 适配区与测试区、跨院患者链接、共同测量和预设阈值。
- **Method / analysis / processing:** 主要分析排除跨分区患者；同分区保留首次合格 stay；以测试区为主的连通分量敏感性；依次执行零更新、仅校准更新和仅观测层更新；完成聚类不确定性、状态对齐和测量不变性检查。
- **Output:** 跨分区排除与支持审计、零更新和有限更新结果、全模型重新拟合的独立标识，以及“跨库稳定、仅数据库特异、证据不足而不解释”的分类与失败图。
- **Supports:** 目标 3 和阶段 II 的计划性跨数据库候选表征判定。

### Evidence chain: 条件性稀疏 RCT 访视结局

- **Input:** 冻结阶段 II 观测方程、每项试验实际 D7/D8 的合格共同测量、条件性个体数据，以及原始 CRF/SAP、中心、时序和生存/住院语义。[17,18,21-25]
- **Method / analysis / processing:** 逐试验核验 R0；构造冻结 P_state/P_obs 映射并核验 R1；依适用条件比较实测指标汇总访视结局或独立 SOFA 访视结局，采用预定分析集、缺失处理、中心处理和 Holm 多重性。
- **Output:** EXIT-SEP D7 与 XBJ-SCAP D8 分开的随机组访视结局差异，或语义不足的停止记录，并列出不可估计内容。
- **Supports:** 目标 4；跨数据映射成立时支持实际访视实测指标汇总结局的随机组比较，否则仅支持独立 SOFA 访视结局的试验内比较。

## Required analyses and evidence

阶段 II 的验收证据包括：资源与具名角色记录；填满并签署的 G1 审计；主标签、两种敏感标签、双时钟、landmark、多状态、delayed entry、竞争事件和泄漏防护的单元测试；变量角色隔离证明；简单基线、模拟恢复、假结构和降级记录；MNAR、行动支持、接口缺失、标签误差、时间反转和阴性对照结果；两个主要分析任务与两个次要诊断性分析的评分、校准、覆盖和患者/医院聚类区间；医院哈希、跨分区排除、结局前特征比较、连通分量敏感性、权限日志、冻结 checksum 和分层更新结果；以及月 24 合取判定表。

RCT 分析启动证据包括：逐试验个体数据授权；原始 CRF/SAP、随机化、中心、D1/D0/D7/D8 相对首剂时序及生存/住院/出院语义核验；EXIT 57 例未知状态和 XBJ all-randomized/FAS 差异的处理记录；逐试验 C_r、单位、访视窗、SVD 映射、R0/R1、分支标签、probabilistic-index tie rule、MI 合并、中心处理、Holm 家族和亚组交互的治疗比较前冻结记录。

截至 2026-07-17 的最接近工作综合足以支持保守定位；提出全球首创、专利不存在或临床数字孪生主张仍需要系统综述、引文网络、专利和非英语数据库核验。

## Expected outputs, falsification criteria, and interpretations

### Planned outputs

1. 双时钟标签、12 小时风险集、互斥发病后状态、G1 规范和可重复代码。
2. 变量角色注册、共同概念与缺失资源、医院优先拆分和跨院患者排除审计。
3. 简单基线、绝对模拟恢复、假结构与弃权基准，以及至多一个准入候选模型或明确降级结果。
4. 两个主要分析任务和两个次要诊断性分析的开发、时间外、医院外与未触碰跨库结果，含校准、不确定性、状态对齐和失败图。
5. 条件满足时分开报告的 EXIT-SEP D7 与 XBJ-SCAP D8 次要访视结局分析；语义不足时报告停止原因。

### Falsification criteria

- 若结果由后录入标签、同一时间格未来行动、未来测量频率或跨拆分处理驱动，则相应临床任务的可执行性主张被否证。
- 若候选模型不能在预设生成情景恢复状态、转移、符号或滞后，或频繁产生零边假结构，则结构可恢复假设被否证。
- 若开发任务达标但未触碰零更新外部结果在适当概率评分、校准、状态对齐或预设结构上不稳定，则跨数据库稳定假设被否证。
- 若 RCT 的共同测量无法形成忠实的一维代理，则不检验基于阶段 II 映射的访视结局；若试验核心语义无法核验，则不产生新访视结局分析。

### Interpretation matrix

| 观察结果 | 允许解释 | 不允许解释 |
|---|---|---|
| 简单基线有用，附加候选模型恢复不足 | 多状态或预测基准有价值，并形成失败证据 | 潜在结构已识别 |
| 模拟恢复达到标准但零更新外部结果不足 | 在开发数据与预设生成族内可恢复，存在跨库不稳定 | 跨库共同系统有效 |
| 零更新不足、有限更新成功 | 适配后可以运输，或观测层存在差异 | 冻结模型天然稳健 |
| 两个主要任务达标但部分状态或边证据不足 | 支持任务级预测表示 | 支持完整结构或反馈关系 |
| 跨数据映射成立且 RCT 访视结局有组间差异 | 该试验实际访视中实测指标汇总结局存在随机组差异 | 潜在动力学、转移边、中介或整个模型获验证 |
| 转入独立 SOFA 分析且有组间差异 | 该试验的独立次要临床状态存在组间差异 | 阶段 II 表征受到干预或获验证 |
| 所有阶段 II 合取标准达到 | 最小全病程候选表示获得审计、恢复、任务和未触碰外部支持 | 因果网络、可控系统、数字孪生或药物平台成立 |

## Contribution, innovation, impact, application, and closest-work comparison

### Contribution and evidence ladder

计划增量由三层组成：输入层连接可比的未发病 landmarks、首次 onset 和互斥发病后状态；转换层用变量角色分离、预设识别与尺度约束、绝对模拟恢复和医院优先分区限制潜在状态解释；输出层连接未触碰外部检验与条件性 RCT 访视结局。若执行成功，它可形成整合、验证、基准、资源和研究治理价值，而不是新算法或全球首次。交付方向是可审计的科学证据和据此形成的高水平论文，而不是仅产出预测工具。

| 证据层级 | 允许主张 | 所需证据 | 当前范围 |
|---|---|---|---|
| 数据可追溯 | 标签、时钟、风险集、变量与接口可审计 | 双库 G1、角色注册、泄漏清零 | 计划，尚未生成 |
| 状态恢复与任务效度 | 观察政策下候选状态具有任务效度 | 模拟恢复、主要任务、诊断、校准与弃权 | 阶段 II 必需 |
| 跨库状态与结构稳定 | 对齐后可解释量在未触碰测试区稳定 | 医院优先零更新、有限更新分开、状态对齐和失败图 | 阶段 II 最低交付 |
| 随机组访视结局差异 | 分配组在实际访视的实测指标汇总结局不同 | R0/R1、分析集、死亡/缺失/中心/多重性 | 条件性阶段 III，仅跨数据映射成立时 |
| 独立试验临床状态差异 | 分配组在死亡/出院分层 SOFA 结局不同 | 跨数据映射不成立但试验核心语义可核验 | 条件性独立分析 |
| 因果机制、控制或数字孪生 | 需要额外识别、干预、前瞻安全性、效用与治理证据 | 当前未满足 | 不属于当前贡献 |

### 已核实的代表性最接近工作比较

| 研究线 | 已核实的代表性近邻 | 已知非新颖内容 | 本研究拟检验的条件性差异 |
|---|---|---|---|
| 纵向/多状态 | Klein Klouwenberg et al. 2019，多状态 Markov，DOI 10.1186/s13054-019-2687-z；Xu et al. 2022，72h SOFA 轨迹，DOI 10.1186/s13054-022-04071-4。[26,27] | 已发病脓毒症的日级转移、轨迹聚类与外部复现 | 在同一风险集中连接发病前 landmark、首次 onset 与互斥后发病状态，并使用双时钟 |
| 动态表型/干预条件转移 | Boussina et al. 2023，DOI 10.2196/45614；Ghassemi et al. 2017，PMID 28815112；Feng et al. 2025，DOI 10.1016/j.eclinm.2025.103691。[29-31] | 潜在状态、动态表型、观察性干预条件转移与器官交互图 | 分开 Y_t、A_t、M_t、标签和 B，并以零边与错设情景限制解释 |
| 数字孪生/模型预测控制（MPC） | Lal et al. 2020，DOI 10.1097/CCE.0000000000000249；Pickard et al. 2026，arXiv:2607.08793。[32,33] | 脓毒症数字孪生、患者特异模拟及模型预测控制已有原型 | 当前只检验候选表示、恢复和运输性 |
| 强化学习/运输 | Komorowski et al. 2018，DOI 10.1038/s41591-018-0213-5；Nauka et al. 2025；Tang et al. 2026；Kalimouttou et al. 2025。[19,34-36] | 离线策略学习、跨观察数据库验证、离策略评估和时间构造风险 | 阶段 II 将时间顺序、医院隔离、模拟恢复和弃权作为先决条件，不学习控制策略 |
| RCT 次要分析 | Bhavani et al. 2022，DOI 10.1007/s00134-022-06890-z；NCT05287477。[28,37] | RCT 中的表型—治疗二次交互和观察性影子部署已有先例 | 每项试验先核验冻结阶段 II 观测映射，再分析实际访视结局；映射不成立时转入独立 SOFA 分析 |

截至 2026-07-17 的有界代表性检索对“各模块已有先例”给出高置信判断；它未找到同时覆盖五层并分开状态、行动和观察过程的代表性工作，但这一负向合取判断只有低至中等置信。[38] 本次检索不是系统综述，也未穷举引文网络、专利、CNKI/万方、Scopus、Web of Science、Embase 或全部注册平台。因此，最强可辩护定位是条件性的证据整合与验证增量。

## Title and positioning claim-support table

本表的主张支持程度统一为“有支持、有限支持、无支持”。

| 按证据范围书写的标题或定位主张 | 贡献类型 | 支持它的现有设计 | 支持它的证据链输出 | 文献或现有结果依据 | 实际增量或无增量说明 | 主张支持程度 |
|---|---|---|---|---|---|---|
| 研究对象是计划构建的脓毒症全病程候选动态系统表征 | 整合与验证 | 双时钟、首次发病任务、互斥发病后状态和变量角色分离 | “可用时间、风险集与互斥病程”及“数据支持、状态识别与模拟恢复” | Sepsis 基础 [1,2]；多状态与轨迹近邻 [26,27] | 连接全病程输入、状态转换和验证输出；不声称已发现真实系统 | 有支持 |
| 阶段 II 计划执行跨数据库检验 | 验证与基准 | 医院优先适配/测试拆分、跨分区患者排除、零更新优先 | “医院优先的未触碰跨数据库检验” | 公共数据库与有限 harmonization [5-10]；运输失败近邻 [12,34] | 增加未触碰测试、患者不跨集合和失败图；结果尚未生成 | 有限支持 |
| 24 个月后可在严格适用条件下开展稀疏 RCT 次要再分析 | 验证与转化 | 逐试验 R0/R1、冻结映射、独立 SOFA 替代分析和分试验估计目标 | “条件性稀疏 RCT 访视结局” | EXIT-SEP/XBJ-SCAP 及衍生材料限制 [17,18,21-25]；RCT 二次分析近邻 [28] | 把跨数据映射设为治疗比较前条件，并保留独立分析路线 | 有限支持 |
| 跨数据映射成立时可比较实际 D7/D8 实测指标汇总访视结局 | 验证 | 冻结 P_state/P_obs 映射、eICU 忠实度与校准标准、死亡/出院分层估计目标 | “条件性稀疏 RCT 访视结局” | 动态表型与 RCT 近邻 [28,29]；本项目尚无结果 | 从阶段 II 观测层到实际访视建立确定性桥接 | 有限支持 |
| 计划贡献是整合、验证以及基准与资源 | 整合、验证与资源 | G1、角色注册、绝对模拟标准、外部隔离和失败产物 | 前四条阶段 II 证据链的联合输出 | 模块近邻 [26-37]；有界检索 [38] | 条件式五层组合与证据治理 | 有支持 |
| 本次有界检索未建立完整五层组合的代表性先例 | 有界 novelty 定位 | 截止日期固定的代表性检索与五链计划 | 最接近工作比较及五链输出 | 截至 2026-07-17 的有界检索 [38] | 执行和更广检索前不主张科学或方法增量 | 有限支持 |
| 当前方案具有全球科学或方法首创性 | 科学发现或方法 | 无 | 无 | 各模块已有先例 [26-37]，负向检索有限 [38] | 不主张任何全球首创增量 | 无支持 |
| 当前已形成因果网络、可控系统、数字孪生、临床工具或药物平台 | 科学、转化或实际应用 | 无 | 无 | 因果与控制边界 [14,19,32-37] | 当前无此增量 | 无支持 |

## Feasibility, resources, risks, alternatives, and stop conditions

### Feasibility and resources

最低角色为具名重症临床/表型负责人、纵向统计负责人、系统辨识负责人、数据工程负责人、模型实现者和独立测试数据保管人；当前仅定义角色，尚无可核验人员承诺。计算范围限两个主库、K≤4、状态机制数≤3、两个主要分析任务、两个次要诊断性分析和至多一个附加候选模型。动物实验、RCT 完成、因果机制和控制不属于 24 个月成立条件。

数据库存在和版本可核验并不证明团队已取得访问凭证、DUA、可运行提取或本项目队列支持。当前也没有模型、模拟恢复、外部检验或 RCT 新分析结果。EXIT-SEP 与 XBJ-SCAP 只有项目内衍生清洗或验证材料，不能替代个体数据授权和原始试验语义核验。

### Working assumptions

| 待确认的科学或统计规格 | 已固定内容 | 决策时点与允许信息 | 未解决的后果 |
|---|---|---|---|
| 临床尺度如何映射到模拟参数 | 生成情景类型、恢复量、绝对阈值和候选模型上限已固定 | 月 6 后、模拟运行前，由临床容许误差、开发库 bootstrap 和不接触外部测试结果的 pilot simulation 决定 | 不得据此准入切换或非线性候选模型，只保留简单基线和可审计的未解决记录 |
| 精确的多类别校准估计量、置信界计算与 threshold registry 条目 | 第 7 日多类别 Brier、有利状态校准目标、校准斜率范围及绝对风险误差上限已固定 | 月 6 前由统计负责人使用开发库 bootstrap、临床容许误差和不接触外部测试结果的 pilot simulation 冻结 | 不得开放最终测试或宣称阶段 II 达到合取标准 |

筛选用事件或参数下限不替代经验有效样本量或模拟稳定性；如果上述规格需要作者、方法学家或数据持有人给出当前材料没有批准的答案，则保持未解决，不自行选择。

### Limitations and boundary conditions

1. **证据状态：** 当前研究是计划，不是已验证模型。公共数据库访问、具名团队、G1 计数、模型结果、外部结果、RCT 授权和原始语义均未完成或未生成。
2. **观察性解释：** 治疗—病情反馈、测量过程和 MNAR 使观测数据只能支持实际照护与测量政策下的预测或生成表示。联合建模、负向控制或良好预测均不能识别真实因果网络、治疗效应、反事实策略、机制、中介或控制。[14-16]
3. **状态解释：** 只解释对齐后且达到恢复、稳定性和校准标准的状态占用、转移、参照测量预测及预设符号或滞后；任意潜变量编号、旋转坐标、未经审计边和证据不足的状态不进入结构解释。
4. **跨库解释：** 有限更新成功只支持适配后运输，不能替代零更新不足。全模型重新拟合属于新开发。医院或共同测量支持不足时，不作医院稳健或完整跨库表征主张。
5. **试验解释：** 条件性 RCT 分析不能验证未测潜在状态、连续动力学、转移边、中介、控制或整个阶段 II 模型。独立 SOFA 分析与阶段 II 模型无关；任何结果不支持无条件临床推广。[4,17,18]
6. **近邻证据：** 各模块已有先例的判断置信度高；完整组合缺口只有低至中等置信。当前不能声称新算法、全球首次、专利不存在、数字孪生、可控系统、临床决策工具或药物平台。[26-38]
7. **阶段边界：** 阶段 I–II 必须在 24 个月内完成。阶段 III 位于最低交付之外，仅在阶段 II 成功以及相应试验数据、语义和跨数据映射适用条件成立时开展，且不能补足阶段 II 的任何失败。

### Risks, alternatives, and stop conditions

| 风险 | 触发条件 | 有界替代 | 停止或降级动作 |
|---|---|---|---|
| 访问或数据支持不足 | 月 3 无两个可访问库；月 6 事件、共同测量或医院支持不足 | 启动预指定备份；改为并固定 24h 或事件时间；删除模块或边 | 无两库全病程支持则停止跨库阶段成功判定 |
| 跨院患者破坏隔离或支持 | 患者跨适配/测试；排除后<20 医院、低于事件/转移/共同测量标准，或排除>10% | 主要分析全排；以测试区为主的连通分量敏感性；备份库 | 不重分测试医院，不让患者跨集合；支持仍不足则仅报告数据库级运输或停止 |
| 标签或时间泄漏 | 结果受后可用信息、同一时间格行动、未来测量频率或跨拆分处理驱动 | 修正 as-of 查询、删除变量、保留可执行标签 | 高严重度项未清零则不开放测试区 |
| 状态不可恢复或产生假结构 | 恢复、FDR、coverage、零边或错设标准未达到 | 退回多状态、线性或仅作预测的分析 | 淘汰附加候选模型，不以预测排名挽救 |
| MNAR 或行动支持不足 | delta tipping 改变解释；行动<5%或>95%，或 ESS<20% | 报敏感性区间，合并/删除，归为照护政策特异 | 不解释相应未测值或治疗关系 |
| 外部运输不足 | 零更新的适当概率评分、校准、状态对齐或符号稳定性不足 | 单独报告仅校准更新、仅观测层更新和全模型新开发 | 有限更新不计为冻结跨库成功 |
| RCT 共同测量或映射不足 | 每项试验<2 个共同测量、单位/时序不一致，或 R1 任一标准未达到 | 转入独立、死亡/出院分层的 SOFA 访视结局次要分析 | 不把替代分析解释为阶段 II 表征的干预或验证 |
| RCT 核心语义不足 | 随机化、中心、D7/D8、生存、住院或出院语义无法核验 | 原 28 日终点复现或数据审计 | 停止新访视结局分析，不推测轨迹或字段 |
| RCT 结果异质或不精确 | 两试验方向不一致或区间过宽 | 分试验报告无支持或跨场景适用性有限 | 不选择亚组挽救结论，不作合并机制解释 |
| 时间超限 | 月 12 无准入候选模型；月 20 未冻结；月 24 无未触碰结果 | 封存当前降级层及失败产物 | 分别判定附加模型开发、外部检验或阶段 II 最低交付未完成 |
| 最接近工作过度外推 | 需要 first、专利不存在或全球不存在主张 | 开展系统综述、引文网络、专利与非英语数据库补检 | 当前仅保留有界、条件性增量定位 |

### Remaining execution requirements

仍未解决的执行事项包括：公共数据库访问、DUA 与可运行提取；具名团队和独立数据保管承诺；G1 的样本、事件、转移、医院、跨院患者、共同测量、接口和复杂度结果；模型、模拟与外部结果；RCT 个体数据授权、原始 CRF/SAP、随机化、中心、时序及生存/住院/出院语义；逐试验共同测量和 R0/R1 结果。每项只能由计划指定的角色在相应时点用允许信息解决，不能在本修订中猜测。

### Identity and final stop boundary

本修订保持原研究问题、24 个月目标、纵向脓毒症 ICU 研究对象、文献/专家先验与公共 ICU/RCT 核心证据基础，以及患者时间状态和状态转移推断单位。若后续取消发病前—发病—发病后—结局连续体、改成普通预测、替换核心数据基础或改变推断单位，则须建立新的 Idea。月 24 无论成功或降级均封存阶段 II；阶段 III 始终不能补足其合取失败。

## References

1. Singer M, Deutschman CS, Seymour CW, et al. The Third International Consensus Definitions for Sepsis and Septic Shock (Sepsis-3). JAMA. 2016;315:801-810. doi:10.1001/jama.2016.0287.
2. Seymour CW, Liu VX, Iwashyna TJ, et al. Assessment of Clinical Criteria for Sepsis. JAMA. 2016;315:762-774. doi:10.1001/jama.2016.0288.
3. Subtle variation in sepsis-III definitions markedly influences predictive performance within and across methods. 2024. PMCID: PMC10803347.（仅完成页面/摘要层核验。）
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
23. EXIT-SEP participants clean/SAP subset/field-coverage audit workbooks. 项目本地只读 QC 材料.（本次未读取 participant-level 工作簿。）
24. XBJ-SCAP 数据集构建验证报告. 项目本地衍生验证材料，2026-07-13；rct-data/xbj_scap_dataset_validation_report.md.（非原始 EDC/CRF 审计。）
25. XBJ-SCAP participants clean/reproduction-transportability QC workbooks. 项目本地只读 QC 材料.（本次未读取 participant-level 工作簿。）
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
38. 脓毒症复杂系统模型：最接近工作刷新. 项目本地有界检索综合，search-through date 2026-07-17；closest-work-update-v001.md.（仅部分核验；不是系统综述或全球不存在性证明。）
