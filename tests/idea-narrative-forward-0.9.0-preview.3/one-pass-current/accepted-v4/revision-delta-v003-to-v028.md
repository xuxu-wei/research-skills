---
schema_version: research-idea-revision-delta.v1
plugin_version: 0.9.0-preview.3
artifact_id: revision-delta-I01-001-v003-to-v028
workflow_id: RID-SEPSIS-CSM-20260717-001
idea_id: I01-001
version_id: v028
path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/accepted-v4/revision-delta-v003-to-v028.md
based_on:
  - artifact_id: idea-dossier-I01-001-v003
    version: v003
    path: tests/idea-test-0.9.0-preview.1/0.9.0-preview.1/03_ideas/nodes/I01-001/dossiers/idea-dossier-v003.md
revised_artifact:
  artifact_id: idea-dossier-I01-001-v028
  version: v028
  path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/accepted-v4/idea-dossier-v028.md
source_skill: multi-path-idea-generator
created_round: 28
change_type: editorial_repair_delta
frozen: true
---

# Revision delta: idea dossier v003 to v028

## Revision boundary

本次修订仅执行叙事结构、学术语言、术语定义、重复删除、限制归并和读者顺序调整。研究身份、主要问题、主要目标、研究对象、证据基础、推断单位、数值与时间规则、分析处理、证据状态和主张强度均保持不变。未新增未经评审的科学内容，未把计划写成已完成结果，也未把任何限制、假设或停止条件改弱。

- **Source logical reference:** `idea-dossier-I01-001-v003`, `v003`, `tests/idea-test-0.9.0-preview.1/0.9.0-preview.1/03_ideas/nodes/I01-001/dossiers/idea-dossier-v003.md`
- **Revised logical reference:** `idea-dossier-I01-001-v028`, `v028`, `tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/accepted-v4/idea-dossier-v028.md`
- **Dossier change type:** `editorial_repair`
- **Delta change type:** `editorial_repair_delta`

## Narrative repair plan mapping — 6/6

| Action | Revised locator | Operation | Text-grounded acceptance evidence |
|---|---|---|---|
| NRP-001 | `Background, current state, gap, significance, and rationale > Background / Current state / Gap / Significance / Rationale` | split, reorder, add_bridge | 该 H2 下依次只有五个必需 H3。`Background` 说明脓毒症时间演化和双时刻问题；`Current state` 说明公共数据库差异、相关研究与治疗—测量过程；`Gap` 以“现有证据尚不能回答”明确跨全病程、跨数据库和 RCT 访视问题；`Significance` 以“有助于区分‘单一数据库中的预测有效’与‘跨数据库仍可解释的患者状态证据’”说明价值；`Rationale` 将双时钟、变量用途区分、绝对模拟恢复、按医院隔离外部测试和试验访视映射逐项连接到前述缺口。 |
| NRP-002 | `Title, summary, audience, and positioning > One-sentence complete-Idea summary` | replace | 新句按“24 个月内的研究对象与构建—未参与开发的外部测试—只有条件满足才开展 RCT 次要分析”形成单一清楚主干；原有全病程范围、两个公共 ICU 数据库、24 个月阶段 I–II、外部验证和 RCT 不补足阶段 II 均在句内直接出现，未使用恢复门、投影门或英文替代分析短称。 |
| NRP-003 | `Structured abstract > Background and gap / Objective and hypothesis / Approach / Expected result / Contribution and impact` | reorder, replace, define | 五项依次说明问题与缺口、目标与假设、总体设计、计划产物、贡献。首次使用动态预测时点时写为“重复设定的动态预测时点（landmark）”；首次说明 RCT 关系时直接写“把预先确定的阶段 II 模型映射到 RCT 实际访视指标，由这些指标计算低维状态摘要”；`Expected result` 明确“所有内容均为计划产物，而非现有模型或已完成结果”。 |
| NRP-004 | `Feasibility, resources, risks, alternatives, and stop conditions > Feasibility and resources / Working assumptions / Limitations and boundary conditions / Risks, alternatives, and stop conditions` | consolidate, move, merge, delete | 第 14 节自包含保留数据与人员状态、标签和泄漏、状态可识别性、缺失和治疗支持、跨数据库验证、试验授权与语义、试验证据范围、文献定位、解释边界、两个未决执行规格，以及逐项风险、替代和停止后果。其他章节没有限制位置指针，也没有复制完整限制清单；局部保留只直接界定相邻估计对象或结果解释。 |
| NRP-005 | `Evidence chains >` 五条 `Evidence chain` | delete | 五条链各自只含 `Input`、`Method / analysis / processing`、`Output`、`Supports` 四项；已删除全部 `Limits and failure conditions` 字段，未用跨章节指针替代。链的输入、处理、输出和所支持目标均仍在正文中。 |
| NRP-006 | `Required analyses and evidence` | consolidate, delete | 该节现仅列八类阶段 II 可核验交付和一组 RCT 启动前记录；每项均对应审计表、单元测试、证明、结果、日志、校验和或分析规范。日期顺序保留在 `Research content and work packages`，实现细节保留在 `Research design and methods`，可证伪结果保留在 `Expected outputs...`，完整限制与后果保留在第 14 节。 |

## Language assessment mapping — 9/9

| Finding | Revised locator | Operation | Text-grounded acceptance evidence |
|---|---|---|---|
| LA-R035-001 | `Title, summary, audience, and positioning > One-sentence complete-Idea summary` | replace, split | 一句话保留单句形式，但仅使用两个由分号连接的主层次：核心 24 个月公共 ICU 研究，以及“只有……时，才……”开展的 RCT 次要分析。研究对象、外部验证和条件性角色均可在该句独立识别。 |
| LA-R035-002 | `Structured abstract > Expected result`; `Research question... > Primary research question / Objective 4`; `Research design and methods > Trial-specific mapping... > 预先确定的映射、映射输出和一致程度` | replace, define | 摘要和研究问题均直接写从阶段 II 模型到实际访视指标的“映射”和“由这些指标计算的低维状态摘要”。方法首次定义处分别给出 `P_state=V_1'X`、`P_obs=D_1^(-1)U_1'(Z_C−a_C)`，并明确相关、归一化误差和校准描述“一致程度”，三个功能不再共用一个“投影”词根。 |
| LA-R035-003 | `Structured abstract`; `Research content and work packages`; `Key techniques and implementation`; `Expected outputs...` | replace | 正文用“预先规定的模拟恢复检验”“未参与模型开发或参数调整的外部测试集”“使用适配集重新校准”“仅更新观测模型”“变量用途预先区分”和“按医院隔离外部测试”等科学动作直接表达判定功能；未保留门、封印、防火墙、自动降级等内部控制隐喻。 |
| LA-R035-004 | H1 与 `Title` 字段；`Research question... > Objective 4` | replace | 标题明确写“在预设条件满足后”修饰“利用 RCT 稀疏访视数据开展次要分析”；Objective 4 写“预设条件满足后使用 RCT 稀疏访视数据开展次要分析”。“稀疏”只修饰访视数据，RCT 是数据来源，次要修饰分析。 |
| LA-R035-005 | `Structured abstract > Contribution and impact`; `Data... > Local RCT evidence`; `Research design and methods > Trial-specific mapping...` | replace, define | proper scoring rule 在首次出现时括注为“如实报告预测概率时可使期望评分最优的评分规则”。D7、D8 首次出现时均写为“试验规定的”访视并明确相对随机化或首剂的时间参照待原始方案核验。正文统一使用“死亡置于最差等级、存活者按 SOFA 排序的临床状态”“全体随机化受试者分析集”“改良意向治疗分析”和“该低维访视摘要与阶段 II 状态表示的一致程度”，未混用 fallback、projection-pass、death-ranked、all-randomized、mITT 或 fidelity。 |
| LA-R035-006 | 全文；完整权威版本位于 `Feasibility... > Limitations and boundary conditions` | consolidate, delete | 因果网络、治疗因果效应、反事实策略、机制、中介、控制、数字孪生、潜在动力学、转移边、整个系统模型、临床工具和药物平台的完整边界只在第 14 节第 9 条集中列出。摘要只保留“RCT 扩展不用于补足阶段 II 或验证整个系统模型”，方法只保留直接界定观察性估计目标和试验估计对象的最小自足限定。全文无跨章节限制指针。 |
| LA-R035-007 | `Structured abstract > Approach` | define | landmark 首次出现即写为“重复设定的动态预测时点（landmark）”，同句给出最多 24 小时历史和未来 12 小时预测窗。后文优先使用“预测时点”。 |
| LA-R035-008 | `Background... > Current state`; `Contribution... > Representative related research comparison` | replace | 正文统一使用“与本研究最接近的既有研究”和“代表性相关研究比较”，不再使用“最近近邻”、`verified representative neighbor` 或 `closest-work` 作为读者正文短称；合同固定 H2 标题保持不变。 |
| LA-R035-009 | `Structured abstract > Approach`; `Research design and methods > Hospital-based cross-database validation`; `Evidence chain: 按医院隔离的计划跨数据库验证`; `Expected outputs... > Falsification criteria and result interpretation`; `Feasibility... > Limitations and boundary conditions / risk table` | split, replace | 每个实例均明确属于四类之一：不更新模型参数的外部验证；该外部测试达到或未达到标准；使用适配集重新校准或只更新观测模型；在目标数据库重新拟合或重新开发。正文没有用“运输/运输性”或 zero-update 包办这些角色，并明确“在目标数据库重新拟合或重新开发完整模型……不属于外部验证”。 |

## Protected-content preservation mapping — 12/12

### PCR-001 — identity and question

- **Source locator:** `YAML frontmatter identity_anchor; Research question, objectives, and core hypothesis > Primary research question`
- **Revised locator:** YAML `identity_anchor`; `Title, summary, audience, and positioning > Positioning and contribution frame`; `Research question, objectives, and core hypothesis > Primary research question`; `Data, materials, and existing evidence base > Prespecified variable roles`
- **Operation:** retain, replace for clarity
- **Text-grounded preservation evidence:** Frontmatter 原样保留研究问题、研究对象与推断单位。主问题逐项写明“发病前在险时段、首次发病、发病后互斥状态演化和结局”，并把研究对象限定为“知识约束、不确定性感知的 ICU 患者候选动态系统表征”。定位字段明确写“核心科学问题不是普通临床预测或泛 ICU 风险分层”；变量表明确生理测量、治疗行动、观测过程和标签的不同角色。

### PCR-002 — primary objective and delivery

- **Source locator:** `YAML frontmatter identity_anchor.primary_objective; Research question, objectives, and core hypothesis > Objectives`
- **Revised locator:** YAML `identity_anchor.primary_objective`; `Title, summary, audience, and positioning > One-sentence complete-Idea summary / Positioning and contribution frame`; `Research content and work packages > Twenty-four-month programme`; `Contribution... > Contribution and evidence progression`
- **Operation:** retain, reorder
- **Text-grounded preservation evidence:** Frontmatter 仍为“construct and validate ... with stage II completed within 24 months”；一句话摘要写“在 24 个月内利用文献与专家知识和两个……公共 ICU 数据库”构建并外部验证；时间表覆盖月 0–24 的系统辨识、恢复和外部测试；定位字段原文写“交付方向是高水平论文和可审查的科学证据，而不是仅提供一个预测工具”。

### PCR-003 — study object and unit of inference

- **Source locator:** `YAML frontmatter identity_anchor.study_object and primary_unit_of_inference; Research design and methods`
- **Revised locator:** YAML `identity_anchor.study_object / primary_unit_of_inference`; `Background... > Gap`; `Research design and methods > Protocol specifications... / Mutually exclusive post-onset state... / Observational target...`
- **Operation:** retain, define
- **Text-grounded preservation evidence:** Frontmatter 原样保留纵向脓毒症中心 ICU 系统、可比较未发病在险时段、发病后轨迹和“patient-time state and state transition”。`Primary research question` 在问题前直接写“研究对象是纵向、以脓毒症为中心的 ICU 患者系统，包括可比较的未发病在险时段和发病后轨迹；主要推断单位是尊重患者与医院聚类的患者—时间状态及状态转移。”协议表另保留首次发病和发病后队列，重叠预测时点行保留一次住院总权重为 1。

### PCR-004 — public ICU inputs and current status

- **Source locator:** `Data, materials, and existing evidence base > Current verified-resource versus prospective-gate status; Public ICU database roles and G1 audit`
- **Revised locator:** `Data, materials, and existing evidence base > Current resource and evidence status / Public ICU database roles and observability audit`; `Feasibility... > Feasibility and resources`
- **Operation:** replace labels, retain status
- **Text-grounded preservation evidence:** 资源表写 MIMIC-IV v3.1 与 eICU-CRD v2.0“数据库存在与版本已核实；团队访问与项目可执行性尚未核实”，双数据库项目计数“尚未生成”；公共数据库角色列出 HiRID 或 AmsterdamUMCdb 作为须预先指定并同等审计的备份；团队凭证、数据使用协议、提取、具名承诺与模型结果分别标为尚未核实或尚未生成。第 14 节再次以完整限制说明这些状态不能等同于已具备资源。

### PCR-005 — trial inputs and current status

- **Source locator:** `Data, materials, and existing evidence base > Local RCT evidence and present limits`
- **Revised locator:** `Data, materials, and existing evidence base > Current resource and evidence status / Local RCT evidence`; `Feasibility... > Limitations and boundary conditions` 第 6 条
- **Operation:** split, define, retain status
- **Text-grounded preservation evidence:** 资源表明确 EXIT-SEP 与 XBJ-SCAP 的现有材料是“项目本地衍生报告”，可说明稀疏性和字段缺口，但“不是原始资料审计或独立同行评审”；第 14 节明确它们“只构成潜在个体级数据来源”，现有材料不能替代个体数据授权、原始 CRF、SAP、随机化、中心、D7/D8 时间参照及死亡、住院、出院和转院语义核验。

### PCR-006 — design order, separation and stability thresholds

- **Source locator:** `Research content and work packages; Research design and methods, including Observational target, anchoring, missingness and abstention`
- **Revised locator:** `Research content and work packages > Twenty-four-month programme / Work packages / minimum analysis sequence`; `Data... > Prespecified variable roles`; `Research design and methods > Observational target, anchoring and abstention / Absolute simulation... / Hospital-based cross-database validation`
- **Operation:** reorder, replace vocabulary, retain all rules
- **Text-grounded preservation evidence:** 
  - 顺序在 `minimum analysis sequence` 逐项写为资源与观测支持审计、标签/状态/医院划分、竞争风险与多状态基线、线性状态空间模型、绝对模拟恢复、至多一个复杂候选、两项主要任务与两项次要诊断、确定开发结果、外部最终测试；第 14 节把 RCT 明确置于阶段 II 之后。
  - 变量表分别定义 Y_t 生理测量、A_t 治疗行动、M_t 观测过程、仅用于标签和 B 基线协变量，并写明双重用途的隔离规则。
  - `Observational target...` 原样保留状态或边的定量判定：20 个随机种子对齐率<90%、bootstrap 保留率<80%、外部符号一致率<80%、状态对齐<0.70 或区间未校准时，删除、合并或标记为数据库/照护政策特异；同句明确较好的预测表现不改变该判定。
  - `Absolute simulation...` 保留正确、零边、过拟合、遗漏状态、错误滞后或观测模型和全部恢复阈值；`Hospital-based cross-database validation` 保留不更新参数的外部验证及适配集有限更新的分离。

### PCR-007 — conjunctive stage-II success

- **Source locator:** `Research content and work packages > Conjunctive minimum success definition; Research design and methods > Hospital-primary genuine cross-database validation`
- **Revised locator:** `Research content and work packages > Conjunctive stage-II success definition`; `Research design and methods > Hospital-based cross-database validation`; `Feasibility... > Limitations and boundary conditions` 第 5 条
- **Operation:** consolidate, replace terminology
- **Text-grounded preservation evidence:** 合取定义逐项要求两库数据支持、绝对恢复、两项主要任务 Brier 或多类别 Brier 与校准、无高严重度泄漏、至少 20 个外部测试医院、不更新参数的外部 Brier、状态对齐≥0.70 和符号一致率≥0.80。方法节把“不更新模型参数的外部验证”“使用预留适配集重新校准”“仅更新观测模型”和“完整模型再开发”分开；第 14 节明确有限更新的较好表现不能替代不更新参数的外部测试未达标，且 RCT 不能补足阶段 II。

### PCR-008 — two primary tasks, clocks, states and leakage controls

- **Source locator:** `Research design and methods > Protocol locks for the two primary clinical tasks; Mutually exclusive post-onset state/event system`
- **Revised locator:** `Research design and methods > Protocol specifications for the two primary clinical tasks / Mutually exclusive post-onset state and event system`; `Data... > Prespecified variable roles`
- **Operation:** retain, split for readability
- **Text-grounded preservation evidence:** 
  - 协议表保留两项主要任务及双时钟：`Event clock` 和 `Availability clock` 分列；培养先发生时给药须在后 72 小时内，给药先发生时采集须在后 24 小时内。
  - 同一表保留基线 SOFA：无已记录慢性器官功能障碍者为 0，有记录者取入 ICU 前 24 小时最低可计算 SOFA；各成分按滚动 24 小时最差值计算，相对基线 +2 须位于感染前 48 小时至后 24 小时，首次可排序满足时刻为发病时刻。
  - `Prediction time, history and horizon` 保留 ICU 第 12 小时起每 12 小时预测、最多 24 小时且至少 12 小时历史、未来 12 小时首次发病，以及发病后第 7 日主时点和第 14 日敏感性。
  - `First onset and repeats` 保留只分析首次发病、重叠预测时点和一次住院总权重为 1；`Within-bin order` 保留 A_t 与下一状态的排序，并明确无法排序的同时间戳边不进入分析。
  - `Competing and intercurrent events` 与互斥状态表保留存活出 ICU、死亡、转院/失访、行政结束、恢复、恶化/新器官衰竭、持续脓毒症及其优先顺序。
  - `Metric`、`Uncertainty` 和敏感性段保留 Brier 或多类别 Brier、绝对校准、患者与医院 bootstrap，以及发病后信息、同时间格治疗、未来测量频率、跨划分插补、患者或 stay 跨集合、重叠窗口权重和结局驱动变量、网格或阈值的泄漏检查。

### PCR-009 — claim and evidence status

- **Source locator:** `Structured abstract; Contribution, innovation, impact, application, and closest-work comparison > Contribution and evidence ladder`
- **Revised locator:** `Structured abstract > Expected result / Contribution and impact`; `Data... > Current resource and evidence status`; `Contribution... > Contribution and evidence progression / Representative related research comparison`; `Title and positioning claim-support table`
- **Operation:** consolidate, retain strength
- **Text-grounded preservation evidence:** Structured abstract 明确“所有内容均为计划产物，而非现有模型或已完成结果”；资源表把当前模型、模拟恢复、预测、外部测试或 RCT 新分析结果标为“尚未生成”。贡献节只主张条件性的证据整合、验证、可复用基准资源和透明度；相关研究比较与 claim-support 表均说明各模块已有先例、完整组合缺口只有低至中等置信，当前不主张新算法或全球首次。

### PCR-010 — complete limitations, assumptions, contingencies and stop rules

- **Source locator:** `Feasibility, resources, risks, alternatives, and stop conditions > Resources and governance; Risk and automatic alternative matrix; Remaining execution gates; Identity and final stop boundary; Expected outputs... > Falsification and stop criteria`
- **Revised locator:** `Feasibility, resources, risks, alternatives, and stop conditions` 全节，尤其 `Working assumptions`、`Limitations and boundary conditions` 第 1–9 条和 `Risks, alternatives, and stop conditions` 全表
- **Operation:** consolidate, merge, retain once at authority location
- **Text-grounded preservation evidence:** 
  - 第 14 节限制清单逐项保留资源与访问、人员承诺、双数据库观测支持、标签与泄漏、状态可识别性、非随机缺失与低重叠、不更新参数的外部验证、时间进度、试验数据授权与语义、共同锚点和映射、文献检索不确定性以及完整解释边界。
  - 风险表逐项给出触发条件、预设替代和停止或有界结论，包括月 3、6、12、20、24 的时间节点，12 小时改 24 小时或事件时间，备份数据库，模型简化，泄漏未消除不访问最终测试，外部验证未达标的有限更新报告，以及试验语义或映射不足时的独立临床状态或原终点复现。
  - `Working assumptions` 完整保留“临床尺度到模拟参数的映射”和“多类别校准的精确估计量、置信界和细化阈值登记”两项未决规格，分别写明已固定内容、决策时点、允许信息与未解决后果；同节明确事件或参数下限不能替代经验有效样本量和模拟稳定性。
  - `Limitations...` 第 7 条与风险表明确两试验方向不一致或区间过宽时只报告无支持或跨场景适用性有限，不合并效应，也不以事后亚组选择改变结论。

### PCR-011 — 24-month boundary and conditional stage III

- **Source locator:** `Research content and work packages > Twenty-four-month minimum and dated gates; Identity and final stop boundary`
- **Revised locator:** `Feasibility, resources, risks, alternatives, and stop conditions > Feasibility and resources` 第二段；`Risks, alternatives, and stop conditions` 时间进度与 RCT 行
- **Operation:** consolidate, retain once at authority location
- **Text-grounded preservation evidence:** 第 14 节原文写“阶段 I–II 必须在 24 个月内完成。阶段 III 位于最低交付之外，只能在阶段 II 合取证据成立，且相应试验的个体数据授权、原始语义和实际访视指标支持预定分析时开展；任何 RCT 结果均不能补足阶段 II 的资源、模拟恢复、主要任务或外部验证缺口。”风险表另给月 20 和月 24 的停止条件以及试验不足时的有界替代。

### PCR-012 — unsupported claim classes

- **Source locator:** `Research question, objectives, and core hypothesis > Core hypothesis and non-hypotheses; Feasibility, resources, risks, alternatives, and stop conditions`
- **Revised locator:** `Feasibility, resources, risks, alternatives, and stop conditions > Limitations and boundary conditions` 第 9 条
- **Operation:** consolidate, retain same boundary
- **Text-grounded preservation evidence:** 第 9 条完整写明观察性数据和预测表现不支持“真实因果网络、治疗因果效应、反事实策略、机制、中介、控制或数字孪生主张”；RCT 次要分析不能验证“未测潜在动力学、转移边或整个阶段 II 系统模型”；当前计划不是“已验证模型、临床决策工具或药物平台”，也不支持无条件临床推广。主张强度与 v003 相同，完整清单仅在此权威位置出现。

## Locator re-open verification

在完成 v028 后，对本 delta 引用的每一个 revised locator 重新读取，并把 protected register 中每个枚举元素与该 locator 的实际正文逐项比较。核验使用正文句子、表格单元格和 frontmatter 值作为证据；未把章节主题、修订意图或本 delta 的陈述本身当作保存证据。

| Register | Required | Mapped | Actual-text verification |
|---|---:|---:|---|
| Narrative repair plan | 6 | 6 | 每项均有 revised locator、operation 和正文验收证据 |
| Language assessment | 9 | 9 | 每项均有 revised locator、operation 和正文验收证据 |
| Protected-content register | 12 | 12 | 每项所有枚举元素均在上列 revised locator 的实际正文中找到；无缺项 |

## Structural lint

Command:

```powershell
python research-skills-openai/skills/multi-path-idea-generator/scripts/lint_idea_dossier.py tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/accepted-v4/idea-dossier-v028.md --expected-plugin-version 0.9.0-preview.3
```

Result: `OK: tests\idea-narrative-forward-0.9.0-preview.3\one-pass-current\accepted-v4\idea-dossier-v028.md`

该结果只证明结构和版本绑定通过确定性检查，不构成叙事或语言就绪判定。
