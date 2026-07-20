---
schema_version: research-idea-revision-delta.v1
plugin_version: 0.9.0-preview.3
artifact_id: revision-delta-I01-001-v003-to-v033
workflow_id: RID-SEPSIS-CSM-20260717-001
idea_id: I01-001
version_id: v003-to-v033
path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final/revision-delta-v003-to-v033.md
based_on:
  - artifact_id: idea-dossier-I01-001-v003
    version: v003
    path: tests/idea-test-0.9.0-preview.1/0.9.0-preview.1/03_ideas/nodes/I01-001/dossiers/idea-dossier-v003.md
source_skill: multi-path-idea-generator
created_round: 33
change_type: editorial_repair_delta
frozen: true
---

# Revision delta: idea-dossier-I01-001 v003 to v033

## Scope and lineage

- **Source:** `idea-dossier-I01-001-v003`，版本 `v003`，路径 `tests/idea-test-0.9.0-preview.1/0.9.0-preview.1/03_ideas/nodes/I01-001/dossiers/idea-dossier-v003.md`。
- **Revised dossier:** `idea-dossier-I01-001-v033`，版本 `v033`，路径 `tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final/idea-dossier-v033.md`。
- **Revision type:** 编辑性修订；研究问题、主要目标、研究对象、核心数据基础和主要推断单位保持不变。
- **Inputs used:** v003 完整 dossier、`narrative-repair-plan-r014.yaml`、`language-assessment-r035.md` 和 `protected-content-register-v003.yaml`，以及当前通用 dossier 合同、模板、生成质量要求、下游交接规则、术语审查规则和结构 linter。
- **Decision boundary:** 本次修订不作叙事或语言就绪判定；修订后的完整 dossier 仍需新的独立评估。

## Narrative repair actions: 6/6

| Action | Revised locator | Operation completed | Locator-level acceptance evidence |
|---|---|---|---|
| NRP-001 | `Background, current state, gap, significance, and rationale` 下的 `Background`、`Current state`、`Gap`、`Significance`、`Rationale` | 将原有五段混排内容拆为合同规定的五个连续、非空功能段 | `Background` 说明脓毒症时间演化、Sepsis-3 与双时钟；`Current state` 概括公共 ICU 数据、既有研究与试验材料；`Gap` 明确全病程可恢复性和不更新参数的跨数据库稳定性尚不能回答；`Significance` 说明跨数据库解释、可重复性和转化判断价值；`Rationale` 逐项连接双时钟、变量角色分离、绝对模拟恢复、隔离外部测试和试验指标映射。五个 H3 顺序与合同完全一致。 |
| NRP-002 | `Title, summary, audience, and positioning > One-sentence complete-Idea summary` | 用一条主干清楚的单句替换原超长技术清单 | 单句按“研究对象—主要验证—条件性扩展”展开：先写全病程候选动态系统，再写模拟恢复和另一数据库外部验证，最后写只有核心验证与试验资料支持时才开展的分试验次要分析；保留 24 个月、两个公共 ICU 数据库、发病前至结局范围和试验层不补足核心验证失败，不含未定义项目短称。 |
| NRP-003 | `Structured abstract` 五个字段 | 重新安排信息先后，先写科学功能，再写必要方法 | `Background and gap` 闭合现状、缺口和意义；`Objective and hypothesis` 明确对象、推断单位和可证伪假设；`Approach` 按双数据库审计、简单基线、复杂候选、外部验证和后续试验映射展开；`Expected result` 明确全部为计划产物；`Contribution and impact` 以证据整合、验证和可复用资源为正向增量。 |
| NRP-004 | `Feasibility, resources, risks, alternatives, and stop conditions`，尤其 `Working assumptions`、`Limitations and boundary conditions`、`Risks, alternatives, and stop conditions` | 将完整限制、未决规格、风险、替代方案和停止条件集中到第 14 节 | 第 14 节单独包含访问与人员、标签与泄漏、状态可恢复性、缺失与重叠、不更新参数的外部验证、试验授权与语义、共同锚点与映射、时间关系、文献证据强度及科学与临床解释边界；两项待方法学确认的规格列入 `Working assumptions`。其他章节没有限制位置指针，保留的局部边界只解释紧邻估计目标或证据功能。 |
| NRP-005 | `Evidence chains` 下五条链 | 删除所有第五字段，只保留合同规定的四项 | 五条链分别为“信息可用时钟、风险集与互斥病程”“数据支持、锚定识别与绝对恢复”“两项主要任务与两项次要诊断”“按医院隔离的跨数据库验证”“试验实际访视低维摘要或独立临床状态”；每条恰含 `Input`、`Method / analysis / processing`、`Output`、`Supports`，无 `Limits`、`Limitations` 或 `failure conditions` 字段。 |
| NRP-006 | `Required analyses and evidence` | 压缩为可检查交付和记录 | 阶段 II 部分仅列访问与审计、标签单元测试、变量角色隔离、基线与恢复、缺失和重叠、主要任务、外部数据隔离和合取结论八类交付；试验部分只列启动前授权、语义、分析集、共同锚点、映射、推断和多重性记录，不重复完整月份路线、方法公式或限制清单。 |

## Language repair findings: 9/9

| Finding | Revised locator(s) | Repair evidence | Acceptance evidence |
|---|---|---|---|
| LA-R035-001 | `One-sentence complete-Idea summary` | 重建为一条有三个可见阶段的句子，删除阈值、完整替代操作和禁止性长串 | 读者可在单句内识别全病程研究对象、模拟恢复与独立外部验证、24 个月核心范围，以及试验次要分析的后续和条件性角色。 |
| LA-R035-002 | `Structured abstract > Approach`；`Primary research question`；`Conditions, mapping, and estimands for the later randomized-trial analyses` | 不再用同一“投影”词根混合三种功能 | `Approach` 和研究问题直接写“将既定模型映射到试验实际访视指标，并由这些指标计算低维状态摘要”；方法部分分别定义“从模型到试验指标的预定映射”、输出 `P_obs` 和“摘要与模型状态表示的一致程度”，三者名称和作用一一对应。 |
| LA-R035-003 | 结构式摘要、五功能背景、研究内容、`Key techniques and implementation`、预期输出 | 将项目控制隐喻改为科学动作、判定依据和后果 | 正文使用“预先规定的模拟恢复标准”“未参与模型开发或参数调整的最终测试集”“未达到标准时改用较简单表征或独立临床状态”等直接描述；没有读者正文中的“门、冻结、降级、防火墙、封印、未触碰”等项目控制词。 |
| LA-R035-004 | H1、`Title` 字段、目标 4、主张支持表 | 重新解析标题修饰关系 | 标题写为“仅在预设条件满足时使用随机对照试验的稀疏访视数据开展的次要分析”：条件修饰是否开展，随机对照试验是数据来源，“稀疏”只修饰访视数据，“次要”只修饰分析。 |
| LA-R035-005 | 数据现状、试验方法、证据链、预期输出、贡献表 | 统一中英文和分析集名称，先给中文功能再给必要英文或缩写 | 统一使用“独立 SOFA 临床状态”“全体随机化受试者的治疗策略分析”“修正意向治疗分析”“摘要与模型状态表示的一致程度”；首次展开 CRF、SAP、SVD、NMAE、MI、FWER、FAS、PPS 等；D7/D8 明确为试验规定访视，且相对随机化或首剂的时间参照保留为待核验。 |
| LA-R035-006 | 摘要、核心假设、证据链、解释矩阵、主张支持表、第 14 节 | 删除成串重复的禁止性解释，保留独特证据边界 | 完整不支持主张类别只在第 14 节 `Limitations and boundary conditions > 科学与临床解释` 列出；摘要仅保留防止把观察性表征解释为因果、控制或数字孪生证据的最小边界；试验估计目标只保留防止把低维摘要组间差异误解为系统级验证的局部边界。无跨节指针。 |
| LA-R035-007 | `Structured abstract > Approach` | 在首次读者正文使用处定义 landmark | 首次写为“每 12 小时重复设定的动态预测时点（landmark）”，后文主要使用“动态预测时点”，读者可区分预测时点、历史窗和预测窗。 |
| LA-R035-008 | `Current state`；`Representative related-research comparison` | 用自然文献功能描述替代项目检索标签 | 正文使用“与本研究最接近的既有研究”和“代表性相关研究比较”；`closest-work` 只保留在合同固定 H2 标题、机器路径或参考资料文件名中。 |
| LA-R035-009 | 结构式摘要、研究内容、跨数据库方法、证据链、解释矩阵、风险表 | 将四种功能分开命名 | 分别使用“不更新模型参数的外部验证”“不更新参数的外部测试未达标”“使用预留适配集重新校准或只更新观测模型”“在目标数据库重新拟合或重新开发整个模型”；每个实例只承担一个角色，正文不使用 zero-update 或“运输性”包办不同操作。 |

## Protected-content preservation: 12/12

| Protected ID | Source locator and protected elements | Revised locator(s) | Item-level preservation evidence |
|---|---|---|---|
| PCR-001 | `identity_anchor`；`Primary research question`：以脓毒症为中心，覆盖未发病、首次发病、发病后演化与结局；不是普通预测或泛 ICU 风险分层 | v033 `identity_anchor`；H1 与完整摘要；`Primary research question` | `study_object` 和 `primary_research_question` 原义保留；标题和问题均以“脓毒症全病程候选动态系统表征”为对象，问题列明发病前、首次发病、发病后和结局连续体，并要求验证患者时间状态和结构，而非泛化为普通风险预测。 |
| PCR-002 | `primary_objective`；`Objectives`：24 个月内完成阶段 I–II，以知识约束、公共 ICU 数据、系统辨识和跨数据库验证形成可审计证据 | `One-sentence complete-Idea summary`；`Objectives` 2–3；`Twenty-four-month minimum and dated decisions`；`Contribution and evidence ladder` | 摘要明确 24 个月、文献与专家知识、两个公共 ICU 数据库、候选动态系统、模拟恢复和外部验证；目标 2–3 保留知识约束、系统辨识和跨数据库验证；贡献段明确交付方向包括可审计科学证据和高水平论文，而非只产出预测工具。 |
| PCR-003 | `study_object`、`primary_unit_of_inference`；方法：纵向脓毒症中心 ICU 系统、未发病在险时段、发病后轨迹；患者时间状态和转移，尊重患者与医院聚类 | v033 `identity_anchor`；完整摘要；`Objective and hypothesis`；两项主要任务表的 `不确定性` | frontmatter 原样保留研究对象和推断单位；摘要保留发病前在险时段至结局；结构式目标明确“以患者时间状态及状态转移为推断单位”；方法表为两项任务均规定患者与医院层自助法或聚类处理。 |
| PCR-004 | 数据章节：文献或专家先验、MIMIC-IV、eICU-CRD、HiRID/AmsterdamUMCdb 备份；数据库存在与版本已核验，但访问、DUA、提取、队列、人员和结果未核验或未生成 | `Current resource and evidence status`；`Public ICU database roles and observability audit`；第 14 节 `数据访问与资源` | 状态表逐项写明两主数据库存在和版本已核验，访问、DUA 和项目计数“尚未核验/尚未生成”，团队只定义角色，模型与结果尚未生成；备份数据库只能预先指定并经同等审计。 |
| PCR-005 | `Local RCT evidence and present limits`：EXIT-SEP 与 XBJ-SCAP 仅为条件性阶段 III 数据；本地材料是衍生报告，不替代授权、CRF/SAP、随机化、中心、时序及生存/住院/出院语义 | `Current resource and evidence status` 中试验两行；`Local randomized-trial evidence`；第 14 节 `随机对照试验资料与映射` | 状态表把本地报告标为项目衍生证据并逐项列出尚未核验的授权和原始语义；两试验段保留样本、访视非缺失数和“时间参照待核验”；第 14 节明确两试验只是条件性来源且本地报告不能替代原始核验。 |
| PCR-006 | 研究顺序与方法：审计→标签/状态/医院划分→简单基线→绝对恢复→至多一个复杂候选→两主两次→开发方案确定→独立外部验证→条件性试验；状态、治疗、观测分离；对齐、保留、符号、一致性和区间阈值 | `Work packages and minimum route` 后的“最低顺序”；`Candidate variable roles`；`Observational target, anchoring, missingness, and abstention`；`Absolute simulation and semi-synthetic recovery standards`；`Hospital-prioritized cross-database validation` | 最低顺序完整保留且试验位于最后；角色表分别定义 Y_t、A_t、M_t、标签和 B；方法保留 20 种子对齐<90%、自助法保留<80%、外部符号一致<80%、状态对齐<0.70、区间未校准时删除、合并或标明适用范围；外部验证保留不更新参数、有限适配分开及最终测试隔离。 |
| PCR-007 | 阶段 II 合取成功：数据支持、绝对恢复、两主任务 proper score 与校准、泄漏清零、不更新参数的外部表现、状态对齐与结构稳定；有限更新不替代；阶段 III 不补足 | `Conjunctive minimum success definition` 1–5 及末段；`Falsification and stop criteria > 外部验证` | 五项合取标准逐条保留，包括 Brier 差上侧 95% 界≤+0.01、校准斜率 0.80–1.20、绝对风险误差≤0.02、无高严重度泄漏、≥20 医院、状态一致性≥0.70 和结构符号≥0.80；明确有限适配不替代不更新参数未达标，阶段 III 不计入合取成功。 |
| PCR-008 | 两项主要任务与双时钟、首次发病、延迟进入、互斥状态、竞争终止、相应时点特征、校准与概率评分、患者和医院聚类、泄漏防护；培养—抗菌药 72/24 小时、基线 SOFA、滚动 24 小时、首个可排序发病时刻、首次发病、重叠时点总权重 1、同窗 A_t 排序和同戳排除 | `Protocol specifications for the two primary clinical tasks` 全表；紧随其后的敏感性与泄漏段；`Mutually exclusive post-onset state and event system` | `事件时钟` 保留 72 小时/24 小时配对、基线 SOFA 和滚动 24 小时及首个可排序时刻；`信息可用时钟` 分开可用时间；`首个发病与重复时点` 保留首次发病和每次 ICU 住院总权重 1；`同一时间单元内排序` 保留 A_t、下一状态和无法排序同戳边排除；表中保留竞争事件、IPCW、校准、proper score 和患者/医院自助法；后段检查未来测量频率、重复住院、插补和结局驱动网格或阈值。 |
| PCR-009 | 结构式摘要与贡献：当前为计划候选和拟执行验证，无现成模型或结果；贡献限于条件性整合、验证和基准资源；单项有先例，组合缺口低至中等置信；无全球首次或新算法 | `Structured abstract > Expected result`；`Contribution and evidence ladder`；`Representative related-research comparison`；主张支持表 | 预期结果明确“均为拟生成的结果，目前没有现成模型、恢复、外部验证或新试验分析结果”；贡献段写明单项模块不增加新颖性且当前不主张新算法；相关研究比较和末段将完整组合负向判断限定为低至中等置信；主张表把文献缺口列为限定性支持。 |
| PCR-010 | 第 14 节唯一完整权威：资源与访问、人员、数据支持、标签与泄漏、恢复、MNAR 与重叠、不更新参数外部验证、时间、试验授权与语义、共同锚点与映射、文献不确定性；失败触发和替代；两项未决方法规格；事件数下限不替代有效样本量；试验方向不一致或区间宽时不挑亚组 | 第 14 节 `Feasibility and resources`、`Working assumptions`、`Limitations and boundary conditions`、`Risks, alternatives, and stop conditions` | `Working assumptions` 精确保留临床尺度到模拟参数映射，以及多类别校准估计量、置信界与阈值登记两项未决规格，并限定可用信息和决定时点；同时明确事件数或参数数不能替代有效样本量和模拟稳定性。完整限制表覆盖全部九类内容；风险表逐项提供触发、替代和停止规则；试验限制行保留方向不一致或区间宽时只报无支持或适用有限且不选择亚组。 |
| PCR-011 | 24 个月内完成阶段 I–II；阶段 III 在最低交付之外，仅在阶段 II 成功和试验条件满足时开展；不能挽救或绕过阶段 II | `Twenty-four-month minimum and dated decisions` 首段及时间表；`Limitations and boundary conditions > 时间和阶段关系` | 首段先自然定义 24 个月核心公共数据库研究，再给阶段 I–II 标签；定义试验扩展为 24 个月后阶段 III。第 14 节完整写明阶段 III 只能在阶段 II 成功及试验数据、语义和映射满足条件后开展，不能补足或绕过阶段 II。 |
| PCR-012 | 观察性与试验证据不支持真实因果网络、治疗因果效应、反事实策略、机制、中介、控制、数字孪生、未测潜在动力学、转移边或整个系统；不得写成已验证模型、临床工具、药物平台或无条件推广 | `Limitations and boundary conditions > 科学与临床解释`；摘要与试验估计目标的局部最小边界 | 第 14 节在一个权威条目中完整保留所有不支持主张类别及不得升级的产品或临床主张；摘要仅以“观察性表征或预测结果不解释为因果、控制或数字孪生证据”防止身份误读；试验估计目标只限定为实际访视低维摘要的组间差异。 |

## Full-dossier downstream checks

| Check | Evidence reviewed in v033 | Result |
|---|---|---|
| Title, summary, question, hypothesis, and contribution identify the same study object | H1/Title、完整摘要、`Primary research question`、`Core hypothesis and non-hypotheses` 和 `Contribution and evidence ladder` 均以“脓毒症全病程候选动态系统表征”为对象；随机对照试验始终是条件性后续扩展 | 通过 |
| Modifier attachment | 标题中的“预设条件”修饰是否开展，“随机对照试验”修饰数据来源，“稀疏”修饰访视数据，“次要”修饰分析；问题和目标中的条件分句均有明确动作 | 通过 |
| Summary sequence | 一句话摘要可见顺序为全病程研究对象 → 模拟恢复和不参与开发的另一数据库验证 → 条件满足后的分试验次要分析 | 通过 |
| Stage, programme, and organizational labels | 首次先解释 24 个月核心公共数据库研究的内容，再引入阶段 I–II；先解释 24 个月后的试验扩展，再引入阶段 III；不再使用 G1、WP、R0、R1 等项目标签承担科学含义 | 通过 |
| Core and cross-disciplinary abbreviations | 首次展开 EHR、SOFA、ICU、MIMIC-IV、eICU-CRD、HiRID、AmsterdamUMCdb、DUA、DOI、CRF、SAP、WBC、CRP、CRRT、IPCW、CIF、AUPRC、MAR、MNAR、ESS、MCSE、ARI、MAE、FDR、SVD、NMAE、MI、FWER、FAS、PPS、mITT、CNS、RMSE、CRPS 和 SMART；数学符号在相邻句定义 | 通过 |
| Compressed model and method labels | 用直接科学描述替代“观测投影、运输性、fallback、death-ranked”等压缩标签；SVD、proper scoring rule 等保留方法名均在首次出现处解释其操作或统计功能 | 通过 |
| Chinese-English coherence | 主要正文使用稳定中文功能名；英文只用于正式数据库或试验名、首次括注的标准术语、数学符号和正式参考文献题名 | 通过 |
| Nested conditions and qualifiers | 回读完整摘要、研究问题、核心假设、两项 working assumptions、跨数据库更新顺序和试验映射句；每个“若、仅在、否则”均连接一个明确动作和结果 | 通过 |
| Replacement self-sufficiency | “从模型到试验指标的映射”“由实际指标计算的低维摘要”“摘要与模型状态表示的一致程度”“不更新参数的外部验证”等替换语在本句或紧邻句即可识别对象、操作和作用 | 通过 |
| Section 14 authority | 完整限制、未决规格、风险、替代和停止条件只在第 14 节集中列出；全文没有“见第 14 节”或其他限制位置指针；局部边界只推进相邻估计目标或证据解释 | 通过 |
| Evidence-chain contract | 五条证据链，每条恰含 Input、Method / analysis / processing、Output、Supports | 通过 |
| Frontmatter and lineage | `plugin_version: 0.9.0-preview.3`；`change_type: editorial_repair`；`based_on` 仅含 v003 的 `{artifact_id, version, path}` 逻辑引用 | 通过 |

## Unresolved author or methodology confirmations

下列事项在修订输入中没有获批准答案，v033 保留原科学状态，没有猜测数值、时间参照或新增限制：

1. 临床尺度到各模拟生成情景具体参数的映射；已固定情景类别、重复量和绝对恢复标准，但参数化仍待方法学确认。
2. 精确多类别校准估计量、置信界构造和阈值登记格式；已固定主要评分和校准范围，但实现规格仍待确认。
3. EXIT-SEP 与 XBJ-SCAP 的个体数据授权、原始 CRF/SAP、随机化、中心、D7/D8 相对随机化或首剂的具体时间参照，以及生存、住院、出院和转院语义。
4. 两项试验与阶段 II 的共同生理锚点、单位、时间语义及映射一致性结果；WBC 和 CRP 仍只是候选，D-dimer 单位仍待核验。
5. 公共数据库访问、DUA、可运行提取、项目队列支持、具名人员和工时承诺，以及所有模型、模拟恢复、外部测试和新试验分析结果。

## Structural lint

Command:

```powershell
python research-skills-openai/skills/multi-path-idea-generator/scripts/lint_idea_dossier.py tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final/idea-dossier-v033.md --expected-plugin-version 0.9.0-preview.3
```

Result after the complete dossier was written: `OK`.
