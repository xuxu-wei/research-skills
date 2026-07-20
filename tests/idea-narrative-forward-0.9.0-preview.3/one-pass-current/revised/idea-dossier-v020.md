---
schema_version: research-idea.v3
plugin_version: 0.9.0-preview.3
artifact_id: idea-dossier-I01-001-v020
workflow_id: RID-SEPSIS-CSM-20260717-001
idea_id: I01-001
version_id: v020
path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/revised/idea-dossier-v020.md
parent_idea_ids: []
based_on:
  - artifact_id: idea-dossier-I01-001-v003
    version: v003
    path: tests/idea-test-0.9.0-preview.1/0.9.0-preview.1/03_ideas/nodes/I01-001/dossiers/idea-dossier-v003.md
  - artifact_id: narrative-repair-plan-r014
    version: r014
    path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/baseline/narrative-repair-plan-r014.yaml
  - artifact_id: language-assessment-r020
    version: r020
    path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/baseline/language-assessment-r020.md
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

# 脓毒症全病程候选动态系统表征：计划跨数据库检验与条件性稀疏 RCT 次要再分析

## Title, summary, audience, and positioning

- **Title:** 脓毒症全病程候选动态系统表征：计划跨数据库检验与条件性稀疏 RCT 次要再分析
- **One-sentence complete-Idea summary:** 本研究计划在 24 个月内利用文献与专家先验以及两个经访问和可观测性审计的公共重症监护数据库，构建覆盖脓毒症发病前、首次发病、发病后演化至结局的知识约束且能表达不确定性的候选动态系统表征，并以未参与开发的外部数据库检验其任务表现和结构稳定性；只有这一路径成功后，才分试验开展不计入阶段 II 成功判定的条件性随机对照试验次要再分析。
- **Primary audience:** 重症医学、临床流行病学、纵向统计、系统辨识、医学人工智能与转化研究共同体；当前不预设具体期刊。
- **Positioning and contribution frame:** 主要贡献定位是候选表征的证据整合、计划性跨数据库验证、可复用基准与资源，以及可证伪的分析框架；条件性随机对照试验（randomized controlled trial, RCT）次要再分析是后续独立证据层。各单项模块已有高置信先例，本项目不主张新算法或全球首次。只有全过程时间轴、状态—行动—观测分工、预设模拟恢复标准、未参与开发的外部检验和条件性 RCT 层均按计划实施，才可能形成增量的整合与验证贡献。[26-38]

## Structured abstract

- **Background and gap:** Sepsis-3 提供感染相关器官功能障碍及序贯器官衰竭评分（Sequential Organ Failure Assessment, SOFA）的操作基础，但疑似感染配对、基线、时间窗和标签可用时间会改变电子健康记录中的发病标签。[1-3] 纵向多状态、动态表型、干预条件转移、跨数据库验证及 RCT 表型—治疗次要分析均已有代表性先例；现有证据仍不能回答，同一候选表征能否以可审计的时间定义贯通发病前至结局，并在隔离的外部数据中同时保持临床任务表现和可解释结构。这一问题关系到跨数据库结果的可重复解释，以及后续转化研究是否具有可靠起点。[26-38]
- **Objective and hypothesis:** 目标是在 24 个月内构建并检验以患者—时间状态及状态转移为推断单位的候选全病程表征。核心可证伪假设是：经过双库数据支持审计，并在预先规定的数据生成情景中达到状态、转移和结构恢复阈值，同时能在空结构或错设情景中避免高置信错误后，至多一个受限复杂候选可在时间外、医院外和未参与开发的数据库测试中维持预设校准、状态对齐与结构稳定。
- **Approach:** 研究先锁定可追溯的发病时间和发病后互斥状态，再完成数据支持审计、简单基线比较及模拟恢复检验；随后冻结全部开发决策，在第二数据库中把适配医院与最终测试医院隔离，并以不使用外部数据更新模型的结果作为主要检验。24 个月后的试验分析只在前述工作成功且试验语义可核验时启动；它使用由冻结观测模型和试验共同实测指标计算的一维状态摘要，该摘要表示可测量的低维信息而非潜在状态本身。[17,18,21-25]
- **Expected result:** 计划产物包括可执行的标签与时间协议、双库观测和变量用途审计、互斥多状态定义、模拟恢复与错误置信控制记录、两项主要临床任务、两项次要表征诊断，以及隔离外部数据库中的结果和失败图。若试验数据满足预设条件，还将分别报告 EXIT-SEP 第 7 日与 XBJ-SCAP 第 8 日的状态摘要比较；这些均是计划产物，不是现有模型或验证结果。
- **Contribution and impact:** 预期增量是把全病程输入、受约束的候选表征、任务评价和未参与开发的外部检验连成可审计证据，并为后续试验次要分析规定可检验的观测桥接。该贡献属于条件性的整合、验证和基准资源价值。

## Background, current state, gap, significance, and rationale

### Background

脓毒症随时间形成，并与治疗和检测行为共同演化。Sepsis-3 将其定义为感染所致失调宿主反应引起的危及生命器官功能障碍，研究中常以相对基线 SOFA 增加至少 2 分进行操作化，但这并不产生唯一的电子健康记录发病时刻。[1,2] 疑似感染配对、SOFA 基线或观察窗的合理改变会改变病例判定与预测表现，因此“临床事件发生时刻”必须与“标签在数据库中可计算的时刻”分开记录。[3]

### Current state

MIMIC-IV、eICU-CRD、HiRID 和 AmsterdamUMCdb 提供纵向生命体征、实验室、治疗与结局数据，但中心、年代、采样和接口并不等价。[5-8] BlendedICU 与 ricu 也表明，跨库统一只能在受限的共同概念上成立。[9,10] 日级多状态模型、SOFA 与生命体征轨迹、动态表型、隐马尔可夫模型、器官交互图、状态空间模型、数字孪生原型、模型预测控制、离线强化学习、跨库验证和 RCT 表型—治疗分析均已有代表性研究。[26-37]

### Gap

这些工作尚不能回答：一个以脓毒症为中心的候选动态表征，能否在同一可追溯时间体系中连接未发病在险片段、首次发病、发病后互斥状态和结局，同时在不同医院与数据库间保持任务表现、状态对齐和候选结构稳定。截止 2026-07-17 的有界检索未找到同时覆盖这些证据层且分开患者状态、治疗行动和观测过程的代表性框架；这一负向判断仅有低至中等置信度。[26-38]

### Significance

若这一缺口得到检验，研究者将能区分可跨数据库重复的患者状态信息、依赖医院测量政策的表象和只在开发数据成立的结构，从而减少把预测表现误读为系统规律的风险。透明记录失败与降级结果也可为后续表型研究、外部验证和随机试验次要分析提供可复用的比较基准，并帮助转化研究在投入更大资源前判断证据是否足以继续。

### Rationale

双时间记录直接回应发病标签不唯一和未来信息进入预测的问题；患者状态、治疗行动与观测过程的用途分离，用于识别由照护和测量政策造成的混合。预设的模拟恢复与错误高置信输出控制标准检验候选模型能否在已知情景中恢复状态、转移和结构，并在空结构或错设情景中拒绝错误解释。医院优先的数据隔离及未参与开发的外部测试用于检验运输性。只有这些观察性证据成立后，才利用冻结观测模型和试验共同实测指标建立低维状态摘要，以限定 RCT 次要分析所检验的对象。[14-18,21-25]

## Research question, objectives, and core hypothesis

### Primary research question

能否构建一个知识约束、能表达不确定性的 ICU 患者候选动态系统表征，使其覆盖以脓毒症为中心的发病前、首次发病、发病后和结局连续体，并在医院与数据库间检验患者状态、临床任务表现和候选结构的稳定性？若这些检验成功，能否进一步用实际稀疏 RCT 访视数据，对由冻结观测模型和试验共同实测指标计算的一维状态摘要进行有限的随机化比较？

### Objectives

1. **全病程边界与可追溯时间：** 锁定可实时实施的主 Sepsis-3 标签、标签可用时间、固定时点风险集、互斥发病后状态与竞争事件，并用两种合理标签作敏感性分析。
2. **审计约束的候选状态表示：** 由双库可观测性审计确定共同模块、时间方案和复杂度上限，显式分离生理状态、治疗行动和观测过程，只解释在允许重参数化下保持不变的量。
3. **模拟恢复与真正外部检验：** 用正确、空结构、过拟合和错设的数据生成情景检验状态、转移和结构恢复，并控制错误的高置信输出；在第二数据库隔离适配数据与最终测试数据，评价两项主要临床任务和两项次要表征诊断。
4. **条件性稀疏 RCT 次要再分析：** 在阶段 II 成功且试验语义可核验后，分别检验冻结阶段 II 表征与实际第 7 日或第 8 日共同实测指标之间的一维映射，并在映射成立时估计该摘要的访视特异随机化差异。

### Core hypothesis

核心假设是：若共同锚点与事件支持达到审计标准，锚定方式、尺度、状态数和滞后均已锁定，且复杂候选达到预设的模拟恢复与错误置信控制标准，则部分状态占用、转移概率、锚点预测及预设依赖的符号和滞后可在未参与开发的外部数据库维持预定义稳定性。主要推断对象是实际照护与测量政策下的患者—时间状态和状态转移；这一界定使后续方法选择以可估计的观察性关系为目标。

## Research content and work packages

### Twenty-four-month scope and dated decisions

阶段 I–II 在 24 个月内完成。阶段 III 位于最低交付之外，仅在阶段 II 成功且相应试验数据、语义和观测桥接满足预设条件时开展。下列日期用于锁定分析范围；“负责人签署”表示计划所需角色，不表示已有具名人员承诺。

| 时间 | 必需交付 | 可测量的决定 |
|---|---|---|
| 月 0–3：资源确认 | MIMIC-IV v3.1 与 eICU-CRD v2.0 的团队访问、数据使用协议（data use agreement, DUA）、存储和算力确认；临床、统计、系统辨识与数据工程角色具名；预先指定 HiRID 或 AmsterdamUMCdb 作为备份 | 任一主库不可用则启动备份；月 3 仍无两个可访问数据库则停止 24 个月跨库路线 |
| 月 4–6：双库可观测性与资源审计（G1） | 队列流、事件和转移、医院、跨院患者、锚点密度、接口及缺失审计；冻结主标签、双时间、多状态、医院优先拆分、时间方案、共同模块和参数上限 | 达到预设支持下限；12 小时不获支持则在建模前改为 24 小时或事件时间；最终测试数据仍不可见 |
| 月 7–12：模型恢复与准入 | 竞争风险、多状态和线性状态空间基线；蒙特卡洛与半合成情景检验；至多一个复杂切换或非线性候选 | 关键恢复、空结构或错设情景未达标则终止复杂扩张并降级 |
| 月 13–20：开发冻结 | 开发库内部、时间外和医院外验证；冻结标签、锚点、预处理、模型、超参数、更新层级、指标及外部阈值 | 严重泄漏未清零或主要任务未达冻结标准则不开放最终外部测试；月 20 后不得按测试结果修改 |
| 月 21–24：未参与开发的外部检验 | 第二数据库最终测试区的不更新结果；适配区学得的仅校准和仅观测层更新结果；聚类不确定性、状态对齐和失败图 | 按合取定义判定阶段 II；未达标仍形成基准与资源 |
| 24 月后：条件性 RCT 分析 | 阶段 II 成功；个体数据授权、原始病例报告表与统计分析计划（case report form/statistical analysis plan, CRF/SAP）及试验语义核验；分试验完成观测映射核验和预注册分支 | 映射成立时分析低维状态摘要；映射不成立时采用独立次要临床状态分析；核心试验语义不足则停止新状态端点 |

### Conjunctive minimum success definition

阶段 II 的计划跨数据库候选系统表征成功必须同时满足：

1. 两库均可构造主发病前风险集与发病后状态队列，并达到冻结的事件、转移、医院和共同锚点支持下限；
2. 复杂候选如被采用，须通过正确生成、空结构及核心错设情景中的预设模拟标准；
3. 两个主要任务在开发和时间外验证中，Brier 评分相对最强简单基线的差值上侧 95% 界不超过 +0.01，校准斜率为 0.80–1.20，校准截距对应的绝对风险误差不超过 0.02；
4. 泄漏清单无未解决的高严重度项目，所有特征遵守标签可用时间，患者、医院、重复住院及插补均不跨数据拆分；
5. 医院优先外部拆分后仍有至少 20 个合格测试医院并满足事件与转移支持，未参与开发的测试数据在不更新模型时达到 Brier 非劣标准；对齐后的主要状态相关或一致性系数至少 0.70，预设结构符号一致率至少 0.80。

依赖 G1 的阈值只能在月 6 前根据临床容许误差、开发库自助法和不接触外部结果的先导模拟写入注册表；本 dossier 的硬标准只能收紧，不能放宽。

### Work packages and minimum route

| 工作包 | 月份 | 主要工作 | 计划输出 |
|---|---:|---|---|
| WP1：标签、队列和 G1 审计 | 0–6 | 访问与版本、样本流、双时间、变量用途、跨院患者、时间网格和接口审计 | 可执行风险集、多状态、医院优先拆分和共同模块 |
| WP2：知识结构、基线与模拟恢复 | 3–12 | 候选图、锚定限制、竞争风险、多状态、线性基线及模拟情景 | 至多一个复杂候选或降级模型 |
| WP3：主要任务与次要诊断 | 8–18 | 首次发病 12 小时累积发生风险、病程第 7 日状态占用、伪遮蔽重建和未来轨迹诊断 | 评分、校准、覆盖、泄漏和弃权记录 |
| WP4：隔离的跨库检验 | 14–24 | 冻结开发包；医院级适配与测试；跨分区患者主要分析剔除；不更新、仅校准及仅观测层更新 | 未参与开发的外部结果、剔除审计与失败图 |
| WP5：条件性阶段 III | 24 月后 | 核验试验语义；建立并检验冻结观测映射；按结果进入状态摘要或独立临床状态分支 | 两项试验分开的次要再分析 |

最低顺序固定为：资源与 G1 审计 → 标签、状态和医院拆分锁定 → 竞争风险与多状态基线 → 线性状态空间模型 → 模拟恢复检验 → 至多一个复杂候选 → 两项主要任务与两项次要诊断 → 冻结开发决策 → 未参与开发的外部检验 → 条件性试验分析。

## Data, materials, and existing evidence base

### Current verified-resource versus prospective status

| 资源或结果 | 当前证据 | 当前状态 | 计划核验 |
|---|---|---|---|
| MIMIC-IV v3.1 与 eICU-CRD v2.0 的公开存在、版本和文献 | PhysioNet 与原始数据库论文提供稳定标识。[5,6] | 已核验数据库存在 | 核验团队访问与本项目队列可执行性 |
| 团队访问凭证、DUA、下载、存储、提取版本与校验和 | 当前材料未提供完成证据 | 尚未核验 | 月 3 前确认 |
| 双库实际样本、事件、转移、医院、跨院患者、锚点密度和接口支持 | G1 尚未运行 | 尚未生成 | 月 6 前冻结 |
| EXIT-SEP 与 XBJ-SCAP 本地验证报告 | 两份项目本地衍生报告记录工作簿构建、关键非缺失和复现质量控制。[22,24] | 项目本地衍生证据 | 核验个体数据授权及原始语义 |
| RCT 个体数据授权及原始试验语义 | 现有衍生报告未完成证明 | 尚未核验 | 在任何新状态端点分析前核验 |
| 所需团队角色 | 已定义临床、统计、系统辨识、数据工程、模型实现与独立数据保管职责 | 角色规范已定义 | 月 3 前取得具名承诺 |
| 当前候选模型、模拟恢复、预测、外部测试或 RCT 新分析结果 | 当前材料没有生成结果 | 尚未生成 | 按日期计划生成 |
| 截止 2026-07-17 的最接近工作更新 | 项目内有界检索综合了代表性论文、预印本与注册记录 | 项目本地衍生证据 | 用更广检索支持更强主张 |

### Public ICU database roles and G1 audit

- **开发库：** MIMIC-IV v3.1，计划用于标签与模型开发以及内部和时间外验证。[5]
- **外部库：** eICU-CRD v2.0，计划用于医院级适配与未参与开发的最终测试；整院接口缺失按医院审计。[6]
- **备份库：** HiRID 或 AmsterdamUMCdb 只能在月 0–3 预先指定并完成同等审计后替代失败角色。[7,8]
- **共同概念：** 只保留单位、语义、时间戳和可见性均可审计的共同变量；数据库特异信息只用于探索性观测模型。[9,10]

G1 将统计患者、住院、重症监护停留、医院、固定时点、首次发病事件、竞争结局、允许转移、时间戳精度、锚点单位与密度、医院接口覆盖、缺失模式及跨院患者。主分析每次住院只用首个合格重症监护停留；外部测试至少需要 20 个有事件支持的医院。每个自由风险参数在开发库与外部库分别至少需要 20 和 10 个事件，每个自由转移参数分别至少需要 20 和 10 次转移。共同状态每个维度至少有两个锚点；每个锚点在两库至少 30% 的合格时间窗实测，并覆盖至少 70% 的合格医院和 80% 的合格患者。有效状态维度不超过通过审计的模块数与 4 的较小值，状态制式不超过 3。

主时间方案为 12 小时，24 小时与事件时间是预写的敏感性或降级方案。动态测量保留实测标志、实测时刻和距上次实测时间；只有具有明确起止时间的输注、器官支持状态和静态基线可在限定范围内向前延用。

### Candidate variable-use isolation

| 主要用途 | 变量示例与允许用途 | 隔离规则 |
|---|---|---|
| 生理测量 Y_t | 实测生命体征、血气、实验室和器官功能测量 | 不含治疗启停、剂量或测量频率；SOFA 标签副本进入独立标签流程 |
| 治疗行动 A_t | 抗菌药、液体、血管活性药、机械通气、连续肾脏替代治疗和激素 | 不作为潜在生理锚点；用于恶化标签时只生成带事件时间的独立副本 |
| 观测过程 M_t | 是否检测、次数、间隔、医嘱、采样和结果可用时刻 | 未检测不编码为正常，接口缺失不编码为患者状态 |
| 仅用于标签 | 疑似感染配对、隔离 SOFA 事件、互斥状态、死亡、出院和转院 | 不进入相同或更早固定时点的特征 |
| 基线协变量 B | 年龄、性别、入院类型、来源和既往病史 | 不复制成随时间变化的伪测量，未知值显式编码 |

### Local RCT evidence and present status

EXIT-SEP 在中国 45 个 ICU 随机分配 1,817 例 Sepsis-3 患者；本地衍生报告记录 1,760 例 28 日状态明确、395 例死亡、57 例状态未知，SOFA 第 1、4、7 日非缺失数为 1,750、1,542 和 1,296，乳酸从第 1 日的 855 例降至第 7 日的 223 例。[17,21-23]

XBJ-SCAP 随机分配 710 例重症社区获得性肺炎患者；本地衍生报告记录全分析集（full analysis set, FAS）675 例、符合方案集（per-protocol set, PPS）617 例、FAS 中基线 SOFA≥2 的操作性类脓毒症人群 671 例，以及严格重叠人群 658 例。SOFA 第 0、4、8 日非缺失数为 703、628 和 610，白细胞为 704、634 和 614，C 反应蛋白为 579、503 和 467，28 日状态有 675 例。[18,24,25]

## Research design and methods

### Protocol locks for the two primary clinical tasks

| 项目 | 发病前主要任务 | 发病后主要任务 |
|---|---|---|
| 人群 | ≥18 岁；每次住院首个合格 ICU 停留；至少 12 小时可见历史；固定时点尚未达到主标签 | 首次发病；入 ICU 已发病者仅在首个可审计时点延迟进入，并按左截断处理 |
| 事件时间 | 主疑似感染以微生物标本采集和系统抗菌药首次实际给药配对；SOFA 相对基线 +2 须位于感染前 48 小时至后 24 小时，首次可排序满足时刻为发病 | 主发病时刻为零点；后续状态按临床事件时间进入 |
| 标签可用时间 | 配对较晚事件及必要 SOFA 数据在源系统可见或最终化的最晚时刻；之后信息不回填 | 恢复的可用时间为连续 24 小时观察窗结束；其他事件采用记录可用时刻 |
| 固定时点、历史和观察期 | ICU 第 12 小时起每 12 小时；此前最多 24 小时且至少 12 小时历史；观察未来 12 小时首次发病 | 发病或延迟进入后每 12 小时；主要观察至病程第 7 日，14 日为敏感性分析 |
| 竞争事件 | 发病前活着离开 ICU、院内死亡、转院或失访为互斥终止；行政结束按删失处理 | 死亡、活着离开 ICU和转院为终止状态；另作删失权重敏感性分析 |
| 估计对象与模型 | 条件于历史的未来 12 小时首次发病累积发生函数（cumulative incidence function, CIF）；离散多项原因别风险转换为 CIF | 第 7 日“生理恢复或活着离开 ICU”的有利状态占用概率；互斥离散多状态模型与 Aalen–Johansen 估计 |
| 评价 | 12 小时 Brier 评分和绝对校准；精确率—召回率曲线下面积、提前量及假警报为次要指标 | 第 7 日多类别 Brier 评分和有利状态绝对校准；各状态与转移校准为次要指标 |
| 不确定性 | 每次停留总权重为 1；患者与医院两层自助法 95% 区间 | 患者与医院两层自助法；首次发病与延迟进入分层并报告有效转移数 |

主标签之外仅使用两种敏感性定义：培养与抗菌药改为对称 ±24 小时；所有人使用感染前 24 小时最低可计算 SOFA，并把器官功能窗限制为前后各 24 小时。特征仅使用固定时点之前已可用的信息，这是保证所估计风险可在该时刻实施的必要条件。

### Mutually exclusive post-onset state/event system

每 12 小时赋值一次，优先顺序为死亡、转院或无法继续观察、活着离开 ICU、恶化或新器官衰竭、生理恢复、持续脓毒症。

| 状态或事件 | 操作定义与可用时间 | 用途约束 |
|---|---|---|
| 持续脓毒症 | ICU 内存活且未满足其他状态，可继续转移 | 只用于标签 |
| 生理恢复 | 相对发病参考 SOFA 下降≥2 且连续 24 小时无新恶化；事件为窗起点，可用时间为窗结束 | SOFA 只用于标签，器官支持作为行动记录 |
| 恶化或新器官衰竭 | 相对此前 24 小时最低 SOFA +2，或新启或升级血管活性药、有创通气或连续肾脏替代治疗 | 生理指标与行动派生标签副本隔离 |
| 活着离开 ICU | 存活离开 ICU，为吸收状态 | 与生理恢复分开记录 |
| 转院或无法继续观察 | 转往不可追踪 ICU 或医院，或记录终止 | 作为竞争终止并进行界限分析 |
| 死亡 | ICU 内或可追踪病程中的死亡，为吸收状态 | 不作为缺失；相同时间戳时优先 |

### Observational target, anchoring and abstention

令锚定的潜在患者状态为 X_t，生理测量为 Y_t，行动为 A_t，测量指示或强度为 M_t，基线为 B，数据库或医院为 S。主要目标是在实际照护与测量政策下估计联合预测或生成分布 p(X_0:T,Y_0:T,M_0:T,A_0:T | B,S)，并由此得到风险、对齐后的状态占用与转移、锚点预测和预设的符号与滞后关系。

每个状态维度至少使用两个跨库锚点。首个锚点的载荷固定为 +1 并标准化尺度；非指定交叉载荷为 0 或预写的稀疏模式。状态维度 K≤4，状态制式不超过 3，滞后仅允许 1 或 2 个冻结时间窗；20 个固定随机种子拟合后进行排列与符号对齐。只解释对齐后的状态占用、转移概率、锚点层预测和预设关系。

非随机缺失（missing not at random, MNAR）分析以显式测量过程的随机缺失（missing at random, MAR）或选择模型为基线，并对未测生理值执行模式混合位移及选择模型临界点分析。每个状态、医院和时间层报告行动概率与有效样本量（effective sample size, ESS）；行动比例低于 5% 或高于 95%，或加权 ESS 低于名义样本的 20% 时，不估计相应治疗作用。状态或关系在多随机种子、重抽样或外部数据中不稳定时，将被删除、合并或标记为数据库或照护政策特异。

### Prespecified simulation recovery and erroneous-confidence control

月 7–10 在不读取最终外部测试结果的条件下，对每个核心情景至少重复 1,000 次，或运行至关键比例的蒙特卡洛标准误（Monte Carlo standard error, MCSE）≤0.02。数据生成情景包括正确指定、空结构或独立状态、多余状态、遗漏状态、错误滞后或观测模型，并交叉改变状态分离度、切换率、政策反馈、隐藏混杂、MNAR、标签误差、访视密度、整院接口缺失和数据库漂移。

| 恢复对象 | 预设标准 | 未达标时的模型处理 |
|---|---|---|
| 状态恢复 | 离散状态的调整兰德指数（adjusted Rand index, ARI）或连续状态的主要典型相关≥0.80；20 个随机种子对齐≥90% | 合并或删除状态，或改用线性或多状态模型 |
| 转移概率 | 主要允许转移的平均绝对误差（mean absolute error, MAE）≤0.05；95% 区间覆盖率 0.90–0.98 | 删除该转移或停止结构解释 |
| 预设符号和滞后 | 正确恢复率≥0.80 | 不把该关系纳入共同结构 |
| 关系检测 | 灵敏度≥0.80，错误发现率（false discovery rate, FDR）≤0.10 | 降低稀疏度或维度，仍未达标则仅用于预测 |
| 空结构错误 | 任一虚假关系的 95% 区间排除 0 的重复比例≤0.05 | 淘汰复杂候选 |
| 错设情景中的拒绝能力 | ≥80% 重复触发失配或弃权，错误结构高置信比例≤0.05 | 淘汰候选或只解释已恢复的不变量 |
| 概率校准 | 斜率 0.80–1.20，绝对概率偏差≤0.02 | 降级模型用途 |

### Hospital-primary cross-database validation

在任何结局导向选择前，按合格体量四分位和接口完整性分层，并以固定种子 20260717 对 eICU 医院标识符进行哈希分配：30% 医院用于适配，70% 医院用于未参与开发的最终测试。医院分配、患者链接算法和校验和均在查看测试结局前冻结。

先按医院分区，再识别跨院患者。一个患者若同时出现在适配医院和测试医院，其全部记录从主要外部分析中排除；同一分区内只保留首次合格住院及其首个合格 ICU 停留。揭示模型性能前，报告排除人数、比例、涉及医院数及仅用结局前变量的组间比较。预写敏感性分析保留预分配测试医院中的首次合格停留，但不把测试医院或记录用于适配。独立数据保管人只检查支持条件，不释放模型性能。

开发阶段冻结标签、数据统一规则、状态、预处理、时间可用性、模型、超参数、阈值与评价代码后，依次执行三种外部分析：不使用外部数据更新模型的主要检验；只用适配区学习校准截距和斜率；只用适配区更新观测层而保持状态和转移固定。全模型重新拟合作为新的运输性开发工作单独报告。

### Conditional trial-observation mapping and independent alternative

两项新状态端点均为原试验结果之后提出的次要、探索性再分析；原 28 日终点另行复现，两项试验分开报告。所有映射、阈值、代码和随机种子在治疗组比较前冻结。

**试验语义与共同锚点资格核验。** 每项试验须有个体数据分析授权、原始 CRF/SAP 或数据持有人确认，以核验随机化、分析集、中心或分层因素、实际第 7 日或第 8 日访视窗，以及死亡、住院、活着出院和转院语义。候选共同指标只包括阶段 II 保留且在试验目标访视直接测得的生理锚点；其临床构念、标本、单位和可用时间须一致或可作预先验证的确定性转换。每项试验至少需要两个锚点。

**冻结的确定性映射。** 对每项试验的共同锚点，使用 MIMIC 开发集锁定的均值、标准差和第 1/99 百分位截断得到标准化测量。阶段 II 冻结观测方程为 Z_C=a_C+L_C X+e；对载荷矩阵作奇异值分解 L_C=UDV'，定义一维阶段 II 状态投影 P_state=V_1'X，以及由试验共同实测指标计算的可观测摘要 P_obs=D_1^(-1)U_1'(Z_C−a_C)。奇异值并列时按固定锚点字典序决定，符号在阶段 II 开发集中固定为与同日 SOFA 总分非负相关，使数值越高表示状态越不利。该一维摘要是冻结观测模型所允许的可测量近似，不等同于完整潜在状态。

**测量一致性、校准和映射保真度核验。** 在未参与开发的 eICU 数据中，第一奇异轴须解释共同锚点载荷矩阵至少 50% 的 Frobenius 能量；P_state 与 P_obs 相关系数≥0.70；相对 P_state 标准差的标准化 MAE≤0.50；回归 P_state=α+βP_obs 时 |α|≤0.20 个标准差、β为 0.80–1.20，95% 区间覆盖率为 0.90–0.98；每个共同锚点的外部校准斜率为 0.80–1.20，标准化截距绝对值≤0.20。治疗分组遮蔽的试验数据还须有至少 80% 的观测锚点落在冻结生理范围内，且至少 60% 的访视时存活住院者能由不少于两个实测锚点计算 P_obs。

**映射成立时的估计对象。** 目标访视前死亡者置于最不利层；访视时仍存活住院者按 P_obs 从高到低排序；访视前活着出院者置于最有利层。主要对比为与中心或分层随机化相容的概率指数或胜率。

**独立次要临床状态分析。** 若共同锚点或映射保真度不满足要求，但 SOFA、死亡、住院或出院、随机化和中心语义可核验，则采用统一中文名称“按死亡、住院期 SOFA 及存活出院状态分层排序的试验特异性次要临床状态分析”。该分析把死亡置于最不利层、存活住院者按 SOFA 从高到低排序、活着出院者置于最有利层，并与阶段 II 表征独立。

| 试验 | 人群与访视 | 缺失、死亡与分析 | 多重性 |
|---|---|---|---|
| EXIT-SEP | 随机分配 1,817 例；目标为所有随机分配者的治疗策略估计。实际第 7 日访视 | 死亡与活着出院按层级处理；存活住院但摘要或 SOFA 缺失时，在每个多重插补（multiple imputation, MI）数据集中重算摘要，再用 Rubin 规则和聚类自助法合并；转院或状态未知作界限分析 | 两项试验的主要状态端点采用 Holm 方法控制家族错误率（family-wise error rate, FWER）为 0.05；亚组只报告治疗与亚组交互 |
| XBJ-SCAP | 随机分配 710 例；无法重建全随机集时降级为 FAS 675 例的修正意向治疗（modified intention-to-treat, mITT）分析。实际第 8 日访视 | 采用相同的死亡、出院、插补、位移与界限策略；不填补结构性不存在的变量 | 采用同一 Holm 家族；亚组只报告交互 |

### Secondary representation diagnostics

部分状态重建采用伪遮蔽 MAE、均方根误差、对数评分和区间覆盖；未来轨迹采用连续等级概率评分（continuous ranked probability score, CRPS）、负对数似然、状态占用与结局校准。诊断按变量、状态、医院和观察密度分层。

## Key techniques and implementation

1. **按可用时间构建标签：** 同时输出临床事件时间、标签可用时间、源表与时间戳、主标签、敏感标签和样本流，并限制特征查询只能使用固定时点前已可用信息。[1-3]
2. **双库数据支持审计：** 生成患者、住院、医院、跨院链接、固定时点、事件、转移、单位、接口、密度和缺失矩阵，据预设规则冻结时间网格、模块、状态维度、状态制式和参数数目。
3. **变量用途隔离：** 每个字段只有一个主要用途；标签派生副本隔离并强制滞后；器官支持不作生理锚点。
4. **简单模型先行：** 先完成竞争风险、多状态、Aalen–Johansen 和线性状态空间模型；至多一个复杂候选进入模拟检验。
5. **锚定与稳定量：** 固定载荷、尺度、符号、维度、允许关系和滞后，多随机种子对齐后只解释稳定量。
6. **缺失与政策支持分析：** 模式混合位移、选择模型临界点、接口压力分析和行动重叠共同决定是否弃权。
7. **外部测试数据隔离：** 医院哈希、跨分区患者剔除、预写敏感性、权限和校验和由独立数据保管人控制。
8. **试验观测映射：** 每项试验使用合格共同锚点和冻结观测载荷构造一维可观测摘要，并在治疗比较前检验映射保真度。
9. **不确定性与多重性：** 使用患者和医院自助法、模拟 MCSE、多重插补、临界点分析、分层概率指数及 Holm 校正。
10. **负向对照与失败结果：** 使用临床预先裁定的时间反转和阴性对照，并发布标签、审计、数据统一、缺失与降级记录。[16]

## Evidence chains

### Evidence chain: 可用时间、风险集与互斥病程

- **Input:** Sepsis-3、培养与抗菌药时间、SOFA 时间、死亡、出院和转院事件、公共 ICU 数据字典及待执行的 G1 审计。[1-10]
- **Method / analysis / processing:** 主标签与两种敏感标签；临床事件时间与标签可用时间；12 小时固定时点；首次发病与延迟进入；互斥状态、竞争事件、患者权重和泄漏检查。
- **Output:** 可执行的 12 小时首次发病 CIF 队列、第 7 日多状态队列、标签差异矩阵和泄漏报告。
- **Supports:** 目标 1，以及候选表征覆盖发病前、首次发病、发病后和结局的可审计边界。

### Evidence chain: 数据支持、锚定识别与模拟恢复

- **Input:** 双库锚点、接口与事件审计，知识先验，患者状态、行动与观测过程，以及正确、空结构、过拟合和错设的数据生成情景。
- **Method / analysis / processing:** 共同模块和复杂度限制；载荷、尺度、关系和滞后锚定；蒙特卡洛模拟；缺失、政策反馈、接口缺失和数据库漂移压力分析；恢复、覆盖、错误发现及错误置信控制。
- **Output:** 一个达到全部预设标准的受限复杂候选，或降级的多状态、线性或仅预测基准，附删除、合并和弃权清单。
- **Supports:** 目标 2 与 3 中可估计的稳定量。

### Evidence chain: 两项主要任务与两项次要诊断

- **Input:** 冻结的队列与状态、准入模型、开发及时间外与医院外数据拆分和预设指标。
- **Method / analysis / processing:** 12 小时首次发病 CIF、第 7 日状态占用、严格适当评分规则、校准、聚类自助法、伪遮蔽、轨迹诊断、标签与观测消融及负向对照。
- **Output:** 两个主要任务的 Brier 评分、校准和状态概率，以及两个次要诊断的评分、覆盖和分层失败图。
- **Supports:** 目标 3 的患者—时间状态任务效度与合取成功判定。

### Evidence chain: 医院优先且未参与开发的跨数据库检验

- **Input:** 冻结开发包、按医院预分配的 eICU 适配区与测试区、跨院患者链接审计、共同锚点和预设阈值。
- **Method / analysis / processing:** 主要分析排除跨分区患者；同分区保留首次合格住院；执行预写敏感性；依次开展不更新、仅校准和仅观测层更新分析；估计患者与医院聚类不确定性、状态对齐和测量一致性。
- **Output:** 跨分区排除统计、数据支持判定、不更新与有限更新结果、重新开发结果的独立标识，以及稳定、数据库特异和弃权清单。
- **Supports:** 目标 3 和阶段 II 的计划跨数据库候选系统表征结果。

### Evidence chain: 条件性 RCT 观测映射或独立临床状态分析

- **Input:** 成功并冻结的阶段 II 观测方程；每项试验实际目标访视的共同锚点；EXIT-SEP 随机分配 1,817 例与 XBJ-SCAP 随机分配 710 例的条件性个体数据；原始 CRF/SAP、中心、时序和生存与住院语义。[17,18,21-25]
- **Method / analysis / processing:** 分试验核验语义与共同锚点；建立冻结奇异值分解映射；在 eICU 中评价相关、误差、校准和覆盖；根据映射结果分析一维可观测摘要或独立次要临床状态；采用多重插补、敏感性分析、Holm 校正和亚组交互规则。
- **Output:** EXIT-SEP 第 7 日与 XBJ-SCAP 第 8 日分开的状态摘要比较、独立次要临床状态分析或停止记录，并列出不可估计内容。
- **Supports:** 目标 4；只有映射成立的分支支持随机分配对该试验实际访视中一维可观测摘要的比较。

## Required analyses and evidence

阶段 II 的完整证据包须包含以下可核验交付：

1. 公共数据库访问、版本、提取和具名职责记录，以及完成的 G1 样本、事件、转移、医院、跨院患者、锚点和接口审计表。
2. 主标签、两种敏感标签、临床事件时间与标签可用时间、固定时点、互斥状态、延迟进入和竞争事件的单元测试记录。
3. 变量用途表、双用字段的副本隔离记录，以及未来信息和跨数据拆分泄漏检查报告。
4. 简单基线、模拟恢复、空结构和错设情景的结果，以及复杂候选的准入、降级、删除与弃权记录。
5. 缺失机制、行动重叠、医院接口、标签误差、时间反转和临床阴性对照的敏感性分析记录。
6. 两项主要任务和两项次要诊断的评分、绝对校准、覆盖、不确定性和分层结果。
7. 医院分配、跨分区患者排除、结局前特征比较、权限日志、冻结校验和，以及不更新与有限更新分开报告的外部检验记录。
8. 阶段 II 合取判定表，逐项记录达到、降级或未达到。

RCT 启动证据包须按试验分别包含个体数据分析授权、原始 CRF/SAP 或数据持有人确认、随机化与中心信息、实际访视时序、生存和住院语义、共同锚点及单位核验、冻结映射和保真度结果、预注册估计对象、缺失处理、多重性及亚组交互规则。最接近工作定位应保留检索范围、日期和证据置信度，以支持保守的贡献表述。

## Expected outputs, falsification criteria, and interpretations

### Planned outputs

1. 双时间标签、12 小时风险集、互斥发病后状态、G1 数据支持规范和可重复代码。
2. 变量用途隔离、共同概念、接口与缺失资源、医院优先拆分和跨院患者排除审计。
3. 简单基线、模拟恢复和错误置信控制基准，以及至多一个准入复杂候选或降级结果。
4. 两项主要任务与两项次要诊断的开发、时间外、医院外和未参与开发的跨数据库结果，含校准、不确定性、状态对齐和失败图。
5. 条件满足时分别报告两项 RCT 的一维可观测状态摘要比较；若预设映射不成立但试验核心语义完整，则报告独立次要临床状态分析；若语义不完整，则报告停止原因。

### Falsification criteria and direct interpretations

| 可观察结果 | 对核心假设的含义 | 允许的直接解释 |
|---|---|---|
| 标签或任务表现由后录入信息、同时间窗未来行动、未来测量频率或跨拆分处理驱动 | 相应临床任务被证伪 | 当前标签或特征流程不可用于计划时点 |
| 复杂候选不能恢复预设状态或转移，或在空结构和错设情景产生高置信错误 | 复杂结构假设被证伪 | 保留简单基准及失败证据 |
| 两项主要任务未达到评分或校准标准 | 任务效度假设未获支持 | 报告任务级失败，不晋级阶段 II 成功 |
| 未参与开发的外部数据中不更新模型时未达到评分、对齐或符号标准 | 跨数据库稳定性假设被证伪 | 报告运输失败以及有限适配后的表现 |
| 试验共同锚点、测量一致性、映射相关、误差、校准或覆盖未达到预设标准 | 一维观测桥接假设被证伪 | 转入独立次要临床状态分析 |
| 两项试验方向不一致或区间宽 | 共同随机化差异未获支持 | 分试验报告不确定结果 |
| 阶段 II 所有合取标准均达到 | 核心观察性假设获得预设范围内支持 | 候选全病程表征获得审计、模拟恢复、任务及外部数据支持 |

## Contribution, innovation, impact, application, and closest-work comparison

### Contribution and evidence levels

实际增量是条件性的三层组合：输入层连接可比的未发病固定时点、首次发病和互斥发病后状态；转换层以变量用途隔离、锚定稳定量、模拟恢复检验和医院优先分区约束候选表征；输出层把未参与开发的外部检验与具有明确失败分支的 RCT 次要分析组织为可审计证据。若执行成功，它可形成整合、验证、基准资源和方法治理价值。

| 证据层 | 可形成的贡献 | 所需证据 | 当前范围 |
|---|---|---|---|
| 数据可追溯 | 标签、时间、风险集、变量和接口可审计 | G1 审计、变量用途表和泄漏检查 | 计划中，尚未生成 |
| 状态重建与任务效度 | 观察政策下候选状态具有任务效度 | 模拟恢复、两项主要任务、校准和弃权记录 | 阶段 II 必需 |
| 跨库状态与结构稳定 | 冻结稳定量在未参与开发的数据中保持一致 | 医院优先不更新检验、状态对齐和失败图 | 阶段 II 最低结果 |
| 随机化状态摘要比较 | 分配组在实际访视的一维可观测摘要不同 | 观测映射、试验语义、死亡与缺失处理、中心和多重性 | 条件性阶段 III |
| 独立试验临床状态比较 | 分配组在分层临床状态上不同 | 试验核心语义和独立端点 | 条件性替代分析 |

### Verified representative closest-work comparison

| 研究线 | 代表性近邻 | 已有工作 | 本研究拟检验的条件性差异 |
|---|---|---|---|
| 纵向与多状态 | Klein Klouwenberg 等 2019；Xu 等 2022。[26,27] | 已发病脓毒症的日级转移、轨迹聚类与外部复现 | 在同一风险集中连接发病前固定时点、首次发病和互斥发病后状态，并使用双时间避免未来信息 |
| 动态表型与干预条件转移 | Boussina 等 2023；Ghassemi 等 2017；Feng 等 2025。[29-31] | 潜在状态、动态表型、观察性干预条件转移和器官交互图 | 分开生理测量、行动、观测过程、标签与基线，并用空结构和错设情景限制解释 |
| 数字孪生与模型预测控制 | Lal 等 2020；Pickard 等 2026。[32,33] | 脓毒症数字孪生原型、患者特异模拟和模型预测控制 | 当前只检验候选表征的恢复与运输性 |
| 强化学习与运输性 | Komorowski 等 2018；Nauka 等 2025；Tang 等 2026；Kalimouttou 等 2025。[19,34-36] | 离线策略学习、跨观察数据库验证、离策略评价和时间构造风险 | 把时间顺序、医院级数据隔离、模拟恢复与弃权作为候选表征的前置要求 |
| RCT 次要分析 | Bhavani 等 2022；ClinicalTrials.gov NCT05287477。[28,37] | RCT 中的表型—治疗次要交互及观察性影子部署已有先例 | 分试验检验冻结观测映射，并在不成立时使用独立临床状态分析 |

截止 2026-07-17 的有界代表性检索对“各模块已有先例”给出高置信判断；对完整组合缺口的负向判断只有低至中等置信。[38] 因而可辩护创新是条件性的证据整合与验证增量。

## Title and positioning claim-support table

| Title or positioning claim, written at its supported scope | Contribution frame in the dossier language | Existing implementation that supports it | Supporting evidence-chain output | Literature or existing-result basis | Actual increment, or a natural-language no-increment statement | Support status in the dossier language |
|---|---|---|---|---|---|---|
| “脓毒症全病程候选动态系统表征”是拟研究对象 | 整合与验证 | 双时间、首次发病任务、互斥发病后状态及变量用途分离 | 可用时间、风险集与互斥病程；数据支持、锚定识别与模拟恢复 | Sepsis 基础文献 [1,2]；多状态与轨迹近邻 [26,27] | 连接全病程输入、受约束转换和可审计输出 | 在“候选”和“计划”范围内有支持 |
| “计划跨数据库检验”是阶段 II 动作 | 验证与基准资源 | 医院优先适配与测试分区、跨分区患者剔除和不更新外部检验 | 医院优先且未参与开发的跨数据库检验 | 公共数据库与有限数据统一 [5-10]；运输性近邻 [12,34] | 未参与开发的数据测试、患者不跨集合及失败图 | 当前为有依据的计划，结果尚未生成 |
| “条件性稀疏 RCT 次要再分析”是阶段 III 动作 | 条件性转化验证 | 试验语义核验、冻结观测映射、独立临床状态分支及分试验估计 | 条件性 RCT 观测映射或独立临床状态分析 | EXIT-SEP、XBJ-SCAP 及衍生证据 [17,18,21-25]；RCT 次要分析近邻 [28] | 把阶段 II 观测信息到试验实际访视的映射设为可证伪条件 | 在次要、条件性和分试验范围内有限支持 |
| 贡献是整合、验证和基准资源增量 | 证据整合与资源 | G1 审计、变量用途隔离、模拟检验、外部数据隔离和失败分支 | 前四条阶段 II 证据链的联合输出 | 模块近邻 [26-37]；有界更新 [38] | 条件式组合与可审计证据关系 | 定位有支持，实际增量取决于执行结果 |
| 本次有界检索未发现完整代表性组合 | 最接近工作定位 | 截止日期明确的有界检索 | 最接近工作比较及五条计划证据链 | 有界检索 [38] | 尚无已实现增量，也不作不存在性判断 | 低至中等置信的有限支持 |

## Feasibility, resources, risks, alternatives, and stop conditions

### Feasibility and resources

最低团队配置包括具名重症临床与表型负责人、纵向统计负责人、系统辨识负责人、数据工程负责人、模型实现者和独立测试数据保管人。当前只有角色规范，没有可核验的人员承诺。计算范围限于两个主数据库、最多 4 个状态维度、最多 3 个状态制式、两项主要任务、两项次要诊断和至多一个复杂候选。公共数据库存在与版本已核验，但团队访问凭证、DUA、可运行提取、项目队列支持、具名人员、候选模型、模拟结果和外部测试结果均尚未核验或尚未生成。EXIT-SEP 与 XBJ-SCAP 目前只有项目本地衍生报告；个体数据授权和原始试验语义尚未核验。

### Working assumptions

| 待定选择 | 已固定内容 | 决定时点与允许信息 | 未解决的后果 |
|---|---|---|---|
| 12 小时、24 小时或事件时间网格 | 主方案为 12 小时；备选仅限 24 小时或事件时间 | 月 6 前，只用 G1 的时间戳精度、事件和转移支持，不查看最终测试结果 | 不能支持任一方案则停止相应跨库时序端点 |
| 共同模块、状态维度、状态制式和参数上限 | K≤4、状态制式≤3，简单基线先行，复杂候选至多一个 | 月 6 前，只用双库可观测性与事件支持；月 12 前用预设模拟 | 支持不足则降维；模拟不稳定则不采用复杂候选 |
| 临床尺度到模拟参数的映射 | 模拟须覆盖正确、空结构、过拟合和错设情景 | 月 6 前由临床容许误差、开发库重抽样和不接触外部结果的先导模拟决定 | 无法形成可信映射则模拟结果不能支持结构解释 |
| 精确的多类别校准估计量、置信界和注册阈值 | 本文硬标准只能收紧，不能放宽 | 月 6 前，仅用开发数据、临床容许误差和先导模拟 | 未冻结则不得进入确认性外部检验 |
| 试验共同锚点与观测映射 | 每项试验至少两个阶段 II 保留且直接实测的共同锚点；映射公式与外部保真度标准已固定 | 24 个月后，在治疗分组比较前，只用已冻结阶段 II 模型、试验语义和遮蔽治疗标签的数据 | 共同锚点或映射不足则不用一维状态摘要 |

### Limitations and boundary conditions

1. **数据访问与支持：** 数据库公开存在不等于团队已获得访问、DUA、可运行提取或项目特定队列支持。eICU 整院接口缺失可能伪装成患者层未测量；跨院患者排除可能削弱医院、事件、转移或锚点支持。
2. **标签与泄漏：** Sepsis-3 不能确定唯一电子健康记录发病时刻。疑似感染配对、基线、时间窗和可用时间均可能改变队列；未来信息、同时间窗行动、未来测量频率、患者或医院跨数据拆分及跨拆分插补会使结果失效。
3. **可恢复性与识别：** 预设模拟只能评价所覆盖的数据生成情景。潜在状态的编号和任意旋转坐标不可解释；在空结构、错设情景或多随机种子中不稳定的状态、转移或关系不能获得结构性解释。
4. **缺失、观测政策与重叠：** 显式建模观测过程不能识别 MNAR 真值。低行动重叠或低 ESS 限制行动相关估计；阴性对照或时间反转的阴性结果不证明模型正确。[14-16]
5. **外部运输性：** 有限校准或观测层更新只能说明适配后的运输性，不能替代不更新模型时的外部失败。全模型重新拟合属于新开发。患者跨分区、医院接口差异和支持不足均限制医院稳健性与跨数据库解释。
6. **时间和资源：** 阶段 I–II 必须在 24 个月内完成；阶段 III 不属于最低交付。任何后续试验结果都不能补足阶段 II 在资源、模拟恢复、主要任务、泄漏或外部检验上的失败。
7. **试验数据与语义：** 现有本地衍生材料不能替代个体数据授权、原始 CRF/SAP、随机化、中心、访视相对首剂时序及生存、住院、出院和转院语义。EXIT-SEP 和 XBJ-SCAP 的人群、访视、变量与估计对象不同，两项试验不能合并。
8. **观测映射：** 一维可观测摘要只使用冻结阶段 II 观测模型与试验共同实测指标，不直接观测完整潜在状态。单位、时间、测量一致性或保真度不足时，独立次要临床状态分析与阶段 II 表征无关。
9. **因果与应用主张：** 观察性数据和预测表现不支持真实因果网络、治疗因果效应、反事实策略、机制、中介、控制或数字孪生主张；条件性 RCT 次要分析也不能验证未测潜在动力学、转移关系或整个系统模型。当前计划不是已验证模型、临床决策工具、药物平台或无条件临床推广依据。
10. **贡献置信度：** 各单项模块已有先例。完整组合缺口仅来自截止 2026-07-17 的有界检索，未覆盖系统综述、完整引文网络、专利及全部非英语数据库；因此不支持新算法、全球首次或不存在性主张。[26-38]

### Risks, alternatives, and stop conditions

| 风险 | 触发条件 | 有界替代方案 | 降级或停止结果 |
|---|---|---|---|
| 访问或双库支持不足 | 月 3 无双库访问；月 6 事件、锚点或医院支持不足 | 启用预指定备份；改用 24 小时或事件时间；删除模块或关系 | 无两库全病程支持则停止跨库系统端点 |
| 跨院患者破坏隔离或支持 | 患者跨适配与测试分区；剔除后测试医院<20、事件/转移/锚点不足或排除>10% | 主要分析全排；采用预写测试优先敏感性；启用备份库 | 支持不足则降级为数据库级运输或描述 |
| 标签或时间泄漏 | 高严重度泄漏未清零 | 修正按可用时间查询、删除变量、保留可实施标签 | 不开放最终测试数据 |
| 状态不可恢复或产生错误结构 | 恢复、覆盖、空结构或错设标准未达到 | 改用多状态、线性或仅预测模型 | 淘汰复杂候选，不作相应结构解释 |
| MNAR 或低行动重叠 | 临界点改变解释；行动比例<5%或>95%；加权 ESS<20% | 报告敏感区间，合并或删除状态，标记照护政策特异 | 不解释相应未测值或行动关系 |
| 外部运输失败 | 不更新模型时的评分、对齐或符号标准未达到 | 报告仅校准、仅观测层更新和重新开发结果 | 判定冻结跨库端点失败 |
| RCT 共同锚点或映射失败 | 每试验<2 个锚点，单位或时间不一致，或任一保真度标准未达到 | 使用独立次要临床状态分析 | 不分析一维状态摘要 |
| RCT 核心语义不足 | 随机化、中心、目标访视、生存或住院语义不可核验 | 只复现原终点或报告数据审计 | 停止新状态端点 |
| 时间超限 | 月 12 无准入候选；月 20 未冻结；月 24 无外部测试结果 | 封存当前已完成层级 | 分别判定复杂端点、外部端点或阶段 II 未完成 |
| 最接近工作过度外推 | 需要全球首次、专利不存在或新算法主张 | 增加系统综述、引文、专利和非英语数据库检索 | 当前仅保留有界、条件性的整合与验证定位 |

研究身份保持为以脓毒症为中心、覆盖未发病、首次发病、发病后状态演化及结局的候选动态系统表征；核心证据基础仍为文献与专家先验、公共 ICU 数据和条件性个体级 RCT 数据，推断单位仍为尊重患者和医院聚类的患者—时间状态及状态转移。改变这些要素将构成新的研究构想，而不是本研究的编辑修订。

## References

1. Singer M, Deutschman CS, Seymour CW, et al. The Third International Consensus Definitions for Sepsis and Septic Shock (Sepsis-3). JAMA. 2016;315:801-810. doi:10.1001/jama.2016.0287.
2. Seymour CW, Liu VX, Iwashyna TJ, et al. Assessment of Clinical Criteria for Sepsis. JAMA. 2016;315:762-774. doi:10.1001/jama.2016.0288.
3. Subtle variation in sepsis-III definitions markedly influences predictive performance within and across methods. 2024. PMCID: PMC10803347.（页面与摘要层核验，部分可得。）
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
23. EXIT-SEP participants clean/SAP subset/field-coverage audit workbooks. 项目本地只读质量控制材料.（本次未读取参与者级工作簿。）
24. XBJ-SCAP 数据集构建验证报告. 项目本地衍生验证材料，2026-07-13；rct-data/xbj_scap_dataset_validation_report.md.（非原始 EDC/CRF 审计。）
25. XBJ-SCAP participants clean/reproduction-transportability quality-control workbooks. 项目本地只读质量控制材料.（本次未读取参与者级工作簿。）
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
38. 脓毒症复杂系统模型：最接近工作刷新. 项目本地有界检索综合，检索截止 2026-07-17；closest-work-update-v001.md.（部分可得；不是系统综述或全球不存在性证明。）
