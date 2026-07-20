---
schema_version: research-idea-revision-delta.v1
plugin_version: 0.9.0-preview.3
artifact_id: revision-delta-I01-001-v003-to-v051
workflow_id: RID-SEPSIS-CSM-20260717-001
idea_id: I01-001
version_id: v051
path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v17/revision-delta-v003-to-v051.md
source_skill: multi-path-idea-generator
change_type: editorial_repair_delta
based_on:
  - artifact_id: idea-dossier-I01-001-v003
    version: v003
    path: tests/idea-test-0.9.0-preview.1/0.9.0-preview.1/03_ideas/nodes/I01-001/dossiers/idea-dossier-v003.md
  - artifact_id: idea-dossier-I01-001-v051
    version: v051
    path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v17/idea-dossier-v051.md
  - artifact_id: editorial-repair-writer-brief-I01-001-r106
    version: r106
    path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/baseline-current/editorial-repair-writer-brief-r106.yaml
  - artifact_id: protected-content-register-I01-001-v004-r004
    version: r004
    path: tests/idea-narrative-forward-0.9.0-preview.3/run-001/inputs/protected-content-register-v004.yaml
frozen: true
editorial_assessment_needed: true
---

# Editorial revision delta: v003 to v051

## Scope and frozen order

同一 writer 在一个完整 v051 文件上依次完成 reader core（第 1–4 节）、研究计划与技术权威（第 5–11 节）、定位与主张及第 14 节权威（第 12–14 节），再核对 References 并执行整篇术语、角色、数值、时间、引用和章节功能扫描。完整 dossier 通过确定性 linter 和整篇检查后冻结；本 delta 仅在该冻结之后创建，未再编辑 dossier。修订只改变叙述顺序、权威位置和读者称名，没有改变研究身份、科学规则、数值、时间、数据状态、分支资格或主张强度，也不作编辑就绪或科学评价结论。

## Included repair actions

| Repair item | Revised locator | Actual operation | Text-grounded acceptance evidence in v051 |
|---|---|---|---|
| NRP-001 | `Background, current state, gap, significance, and rationale` > `Background`; `Current state`; `Gap`; `Significance`; `Rationale` | split; move | 五个 H3 按规定顺序各承担一个功能：问题与双时钟、现有数据库和近邻、尚未解决的全病程跨数据库证据问题、对重症研究与后续干预判断的后果，以及“双时钟 → 变量角色分离 → 模拟重建 → 跨数据库检验”的设计理由；阶段 III 只剩一项从属关系说明。
| NRP-002 | H1；`Title, summary, audience, and positioning` > Title、One-sentence；`Structured abstract` | replace; reorder | H1 和 Title 完全一致，只呈现全病程候选表征与 24 个月阶段 I–II 跨数据库检验；One-sentence 恰为一个句子和三个分句；Structured abstract 只在 Approach 中一次高层提及主体达标后的分试验次要分析，入口没有试验名、访视日、映射符号、资格清单或分支标签。
| NRP-003 | `Research design and methods` > `Conditional trial-observation mapping and independent analysis` | consolidate; move | 连续方法权威先列阶段 II 成功、个体资料可用、核心试验语义可核验三项共享前提，再分别定义观测映射分支、独立的 SOFA 有序临床状态端点和核心语义不足时停止；共同锚点与忠实度只属于映射分支；两试验、分析集、死亡与出院排序、缺失敏感性、Holm 检验族和解释对象均保持分开。
| NRP-004 | `Feasibility, resources, risks, alternatives, and stop conditions` 的四个 H3；`Evidence chains` | consolidate; delete repeated fields | 第 14 节分别完整承载资源状态、两项工作假设、十一类限制与证据边界及非方法型运行风险；五条证据链均且仅有 Input、Method / analysis / processing、Output、Supports 四字段；全文没有指向第 14 节的提示，也没有在证据链复现限制清单。
| NRP-005 | `Key techniques and implementation` 的十行可复现单元表 | replace | 每行均给出输入数据或研究构念、派生或计算关系、输出记录以及核查用途与依赖；覆盖双时钟、变量角色、队列与状态、模型、模拟、医院分区、四种更新操作、试验接口、不确定性及阴性对照，没有工具或项目管理隐喻，也没有复述完整阶段 III 分支。
| LAR-105-01 | `Research design and methods` > `Conditional trial-observation mapping and independent analysis` 首段 | replace; define | 首次技术称名为“仅在预设条件满足后利用随机对照试验稀疏访视资料开展的次要再分析”，明确稀疏性修饰访视资料、预设条件约束分析资格，随后统一使用“有前置条件的随机试验次要分析”；入口只保留高层直接描述。
| LAR-105-02 | 同一方法小节 > 观测映射成立时的有序访视结局分析 | define; replace | 公式处分别把 P-state 定义为潜在状态投影、把 P-obs 定义为由冻结观测方程和试验实际访视共同生理测量计算的一维可观测代理，并把治疗组比较对象固定为由死亡、一维可观测代理和存活出院共同排序的访视结局；后续接口、证伪和解释均使用这些角色名。
| LAR-105-03 | 同一方法小节 > 观测映射不成立但独立分析条件成立时的分析 | define; replace | 首次完整定义“与阶段 II 表征独立的 SOFA 有序临床状态端点”，按死亡最差、存活住院者 SOFA 从高到低、存活出院最有利排序；后文统一使用“独立的 SOFA 有序临床状态端点”，不再使用英文复合短称或替代分支标签。
| LAR-105-04 | `Structured abstract` > Objective and hypothesis；`Research design and methods` > `Observational target, anchoring, and evidence-qualified interpretation` | define; consolidate | 摘要先以状态占用率、转移概率、锚点预测和预设符号或滞后作高层说明；方法再明确允许的重参数化与预设模拟生成机制，统一称为“可恢复不变量”；全文没有“锚定不变量”或“冻结不变量”作为新类别。
| LAR-105-05 | `Research design and methods` > `Hospital-primary cross-database validation` | replace; define | 四种操作依次完整定义为不更新外部检验、仅校准适配、仅观测层适配和全模型重拟合，并分别说明可更新对象与证据身份；后文使用同一组名称，且明确有限适配不改变主要不更新外部检验未达标的结论。
| LAR-105-06 | 第 5–14 节各保留科学功能的判定、访问、替代和停止语句 | replace | 时间表写明被判定对象、标准、替代或停止动作；最终测试写成授权访问、权限隔离和分析冻结；失败后果直接写为改用具体简单表征、启用备份、停止端点或不能补偿。整篇扫描未见所列内部隐喻，也未使用无对象的通用替代词。
| LAR-105-07 | `Structured abstract` > Expected result；`Key techniques and implementation` > 阴性对照与负向结果；`Expected outputs...` > Planned outputs | replace | 首次负向产物写为按对象记录未达到标准、停止解释或不晋级决定及原因的图表；实现表按医院、状态、变量或结构输出记录；计划产物保持负向结果与正向结果共同发布，不使用无对象的“失败图”或“弃权”。
| LAR-105-08 | `Title, summary, audience, and positioning` > One-sentence complete-Idea summary | replace | 单句用两个分号形成三个清楚分句：24 个月阶段 I–II 主体、主体达标后的高层从属延伸、预测和观察性表征的非因果解释；句中无试验名、访视日、映射量、资格或分支清单。
| LAR-105-09 | `Feasibility, resources, risks, alternatives, and stop conditions` > `Limitations and boundary conditions`；第 7、11 节必要局部边界 | consolidate; delete repetition | 完整限制和禁止主张只在第 14 节列一次；第 7 节只保留直接决定估计对象或分析资格的局部边界，第 11 节只保留结果依赖解释；五条证据链没有限制字段，全篇没有完整限制串的重复或位置指针。

## Protected-content preservation

| Protected item | Revised locator(s) | Item-level preservation evidence in v051 |
|---|---|---|
| PCR-001 | YAML `identity_anchor`；`Research question, objectives, and core hypothesis` > Primary research question | 五个 identity_anchor 值逐字符保留，identity_status 为 preserved；正文问题仍是以脓毒症为中心、覆盖可比未发病在险时段、首次发病、发病后演化和结局的候选动态系统表征，而非普通预测或泛重症风险分层。
| PCR-002 | YAML `identity_anchor.primary_objective`；同一 H2 > Objectives | primary_objective 原文保留；正文明确阶段 I–II 在 24 个月内完成，并单列“一篇或多篇高水平论文和可审计科学证据，而不是仅产出预测工具”的交付方向。
| PCR-003 | YAML `identity_anchor.study_object` 与 `primary_unit_of_inference`；`Research design and methods` > `Observational target, anchoring, and evidence-qualified interpretation` | 原文锚点值保留；方法正文明确研究对象包括未发病在险时段和发病后轨迹，推断单位为患者—时间状态及状态转移，并在不确定性估计中尊重患者与医院聚类。
| PCR-004 | `Data, materials, and existing evidence base` > Current resource and result status、Public intensive-care database roles and support audit；第 14 节 > Feasibility and resources | 表格分别记录数据库存在与版本已核验，而团队访问、数据使用协议、可运行提取、双库项目计数、具名人员及所有模型或验证结果尚未核验或尚未生成；HiRID 或 AmsterdamUMCdb 仍是须预先指定并同等审计的条件性备份。
| PCR-005 | `Data, materials, and existing evidence base` > Local randomized-trial evidence status；`Research design and methods` > Conditional trial-observation mapping and independent analysis | EXIT-SEP 与 XBJ-SCAP 的样本和访视非缺失数保持不变；正文明确衍生报告不等于个体资料授权、原始病例报告表或统计分析计划，也未核验随机化、中心、访视及生存或住院语义；两试验仅为条件性潜在个体数据来源。
| PCR-006 | `Research content and work packages` > Work packages and minimum route；`Research design and methods` > 变量角色、模拟恢复及外部检验小节 | 资源审计到条件性试验分析的规定顺序完整；生理、治疗和测量过程保持分离；20 个随机种子对齐 90%、自助重采样保留 80%、外部符号一致 80%、状态对齐 0.70 及区间校准标准均保留，并规定删除、合并或限定为数据库或照护政策特异，预测表现不能改变判定。
| PCR-007 | `Research content and work packages` > Conjunctive minimum success definition；`Research design and methods` > Hospital-primary cross-database validation | 合取成功仍包括双库支持、绝对恢复、两项主要任务适当评分与校准、无高严重度信息泄漏、不更新外部检验、状态对齐和结构稳定性；两种有限适配与主要外部证据分开且不能补偿其未达标，阶段 III 不计入或补足阶段 II。
| PCR-008 | `Research design and methods` > Protocol locks for the two primary clinical tasks；Mutually exclusive post-onset state and event system | 两项主要任务、事件与信息可用双时钟、首次发病风险集、延迟进入、互斥状态、竞争终止、当时可见特征、适当评分和聚类区间均保留；72 小时与 24 小时配对、基线 SOFA、滚动 24 小时组成、首次可排序发病时刻、每次住院总权重 1、同窗行动与后继状态排序及重复住院、未来测量频率和结局驱动网格等泄漏核查均有正文证据。
| PCR-009 | `Structured abstract`；`Contribution, innovation, impact, application, and closest-work comparison` > Contribution and evidence ladder、Verified representative closest-work comparison | 摘要明确所有产物待生成且不是现成模型或验证结果；贡献只到条件性整合、验证、基准或研究资源；各模块已有先例、完整组合缺口低至中等置信，正文不声称新算法或全球首次。
| PCR-010 | 第 7 节技术方法；`Expected outputs, falsification criteria, and interpretations`；第 14 节四个 H3 | 第 7 节唯一连续定义设计资格与互斥分析，第 11 节唯一集中结果证伪和结果依赖解释；第 14 节完整保留资源、团队、支持、标签与泄漏、可恢复性、非随机缺失与低重叠、外部检验、时间、试验语义、共同锚点与最接近工作不确定性，以及两项工作假设。试验方向不一致或区间过宽时不以亚组改变解释，筛选下限不替代有效样本量和模拟稳定性。
| PCR-011 | `Research content and work packages` > 24 个月最低交付与时间节点、Work packages and minimum route；`Research design and methods` > Conditional trial-observation mapping and independent analysis；其余各功能位置 | 24 个月阶段 I–II、阶段 III 位于最低交付之外及不可补足关系均保留；方法先只列三项共享前提，再并列观测映射、独立 SOFA 与核心语义不足停止，两个试验分开。时间表只有一个依赖工作包，证据链、Required analyses、Planned outputs 和 Claim-Support 各保留完成自身功能的一项，未把映射条件写成共享条件。
| PCR-012 | `Feasibility, resources, risks, alternatives, and stop conditions` > Limitations and boundary conditions；摘要、核心假设与 Interpretation matrix 的必要局部边界 | 第 14 节一次列出观察性数据、预测和条件性试验分析均不能支持的真实因果网络、治疗效应、反事实策略、机制、中介、控制、数字孪生、未测潜在动力学、转移边或整个系统，以及当前不是已验证模型、临床工具、药物平台或无条件推广依据；其他位置只保留直接限定相邻估计目标或结果解释的短句。

## Reader-facing scientific-role concordance

| Scientific role | One reader-facing name | First-use locator | Competing-form disposition | All-occurrence result |
|---|---|---|---|---|
| 中央研究对象 | 脓毒症全病程候选动态系统表征 | H1 | 普通预测工具、泛重症风险分层及已验证系统均未作为对象称名 | 标题、问题、工作包、贡献和主张表保持同一对象与“候选”状态 |
| 主要问题与任务 | 未来 12 小时首次发病风险；发病后第 7 日有利状态占用 | `Structured abstract` > Approach | 累积发生风险和状态占用只在技术位置进一步展开，不以缩写替代任务 | 问题、目标、方法、证据链和计划产物中的时间窗及对象一致 |
| 主要证据结果 | 阶段 II 合取成功 | `Research content and work packages` > Conjunctive minimum success definition | 单项预测、有限适配或阶段 III 结果均未改称总体成功 | 五项合取组成在工作包、方法、证伪、解释和第 14 节保持一致 |
| 贡献 | 条件性的整合、验证和基准或研究资源增量 | `Title, summary, audience, and positioning` > Positioning and contribution frame | 新算法、全球首次和并列阶段 III 贡献均作为不支持主张移除 | 摘要、贡献梯级、近邻比较和 Claim-Support 使用同一强度 |
| 从属试验分析 | 有前置条件的随机试验次要分析 | `Research design and methods` > Conditional trial-observation mapping and independent analysis 首段 | 入口采用高层用途描述；旧复合称名和“层”式短称删除 | 首次完整定义后，证据链、核查、产物、贡献和限制均使用同一名称 |
| 阶段 II 映射量 | 潜在状态投影 | 同一方法小节 > 观测映射成立时的有序访视结局分析 | “投影摘要”等同时指多个对象的形式删除 | 该名称只指公式中的 P-state，后续不与实测代理或访视结局混用 |
| 试验实测代理 | 由冻结观测方程和试验实际访视共同生理测量计算的一维可观测代理 | 同一公式段 | “投影可观测摘要”和其他压缩形式删除 | 该名称只指公式中的 P-obs，映射标准、结局、缺失和实现接口一致 |
| 映射分支结局 | 由死亡、一维可观测代理和存活出院共同排序的访视结局 | 同一方法小节 > 观测映射成立时的有序访视结局分析 | 不再用“投影摘要”同时充当代理与治疗组比较结局 | 定义、缺失处理、实现接口、证伪、解释和限制中的排序对象一致 |
| 独立分支端点 | 独立的 SOFA 有序临床状态端点 | 同一方法小节 > 观测映射不成立但独立分析条件成立时的分析 | 英文复合短称和多种中文替代称名删除 | 三层排序、独立性、缺失处理、证伪、解释和限制均指同一端点 |
| 阶段 I–II 结构量 | 可恢复不变量 | `Structured abstract` > Objective and hypothesis | “锚定不变量”和“冻结不变量”删除；受锚定约束和冻结后外部检验只描述状态 | 首次高层解释、方法完整定义、证据链、贡献和限制使用同一名称 |
| 外部更新操作 | 不更新外部检验；仅校准适配；仅观测层适配；全模型重拟合 | `Research design and methods` > Hospital-primary cross-database validation | 英文与混合更新称名以及裸用跨库迁移词删除 | 四种名称在方法、实现、证据链、证伪、解释和限制中各自对应同一参数范围与证据身份 |
| 负向产物与停止动作 | 按对象记录未达到标准、停止解释或不晋级决定及原因的记录与图表 | `Structured abstract` > Expected result | 无对象的失败产物名和通用停止词删除 | 所有出现均直接给出对象、标准、动作和后果；没有一个词跨指多种科学动作 |

## Advisory short-form-diff candidate disposition

The repository short-form comparison reported ten advisory candidates. Each is dispositioned below by its function in the frozen dossier; semantic review does not require a dossier edit for any candidate.

| Candidate | Reported line(s) | Disposition | Semantic reason |
|---|---:|---|---|
| `24 个月跨数据库系统表征` | 99, 469 | `descriptive_not_label` | A full duration-setting-object description repeated in the stopping condition and long-horizon risk statement; neither occurrence substitutes for a longer technical definition. |
| `各模块已有先例` | 145, 422 | `descriptive_not_label` | A complete evidence-status proposition quoted for scope, not a coined scientific role. |
| `待审计` | 154, 158, 159, 160, 161, 162, 163, 164 | `standard_and_defined` | The status is defined at first use as indicating that no result is yet available and is then applied consistently to the corresponding audit entries. |
| `不更新外部检验` | 260 | `standard_and_defined` | It follows the full definition of an external evaluation in which model parameters are not updated. |
| `仅校准适配` | 261 | `standard_and_defined` | It follows the full definition limiting updates to calibration intercept and slope. |
| `仅观测层适配` | 262 | `standard_and_defined` | It follows the full definition that freezes state and transition components and updates only observation parameters. |
| `全模型重拟合` | 263 | `standard_and_defined` | It follows the full definition in which the complete model is refitted. |
| `双库支持、锚定与绝对恢复` | 320, 428 | `fixed_scaffolding` | It is the required Evidence-chain heading and its exact reuse in the traceability table, where it locates the supporting section rather than naming an additional scientific construct. |
| `候选` | 33, 37, 38, 40, 44, 45, 46, 62, 66, 76, 81, 82, 89, 101, 108, 111, 123, 128, 141, 144, 240, 241, 273, 303, 304, 318, 324, 339, 371, 379, 384, 390, 391, 396, 407, 418, 428, 440, 446, 458, 460, 473 | `descriptive_not_label` | An ordinary epistemic qualifier used across the dossier to distinguish proposed from established work; it does not name a method, endpoint, or evidence object. |
| `计划` | 33, 37, 38, 40, 45, 47, 48, 76, 82, 95, 108, 116, 134, 139, 140, 142, 144, 149, 150, 271, 334, 339, 343, 361, 406, 410, 414, 419, 428, 429, 431, 432, 440, 453, 459, 463, 500, 501 | `descriptive_not_label` | An ordinary study-status word used across the dossier to distinguish intended work from completed results; it is not a compact scientific name. |

## Verification summary

| Check | Result |
|---|---|
| 同一 writer 四个 bounded section passes，且没有章节碎片 | 通过；始终只编辑一个完整 v051 目标文件 |
| Identity anchor 与研究身份 | 五个值逐字符一致；identity_status 为 preserved；正文研究对象和推断单位未漂移 |
| 15 个 H2、第 3 节五个有序 H3、五条四字段 Evidence chains | 确定性结构检查通过 |
| One-sentence、读者入口和阶段 III 信息粒度 | 单句一个终止符、三个分句；入口无技术分支清单；Structured abstract 仅一次高层用途 |
| 术语、科学角色、数值、时间、数据状态和引用 | 整篇扫描通过；v003 正文引文集合完整保留，References 为连续 1–38 |
| 第 7、11、14 节权威与限制去重 | 完整方法树、结果解释和限制或假设分别位于其权威位置；无第 14 节位置指针 |
| Markdown 表格与逻辑血缘 | 表格列数一致；dossier 与 delta 使用完整逻辑 ID、版本和路径 |
| Deterministic dossier linter | Passed with `OK` and no advisory. Actual command: `python -B research-skills-openai/skills/multi-path-idea-generator/scripts/lint_idea_dossier.py tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v17/idea-dossier-v051.md --expected-plugin-version 0.9.0-preview.3` |
| Repository short-form comparison | Returned 10 advisory candidates; all 10 have an allowed semantic disposition and reason above, with no resulting dossier edit. Actual command: `python -B research-skills-openai/skills/academic-language-assessor/scripts/diff_reader_facing_short_forms.py tests/idea-test-0.9.0-preview.1/0.9.0-preview.1/03_ideas/nodes/I01-001/dossiers/idea-dossier-v003.md tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v17/idea-dossier-v051.md` |
| Dossier freeze and delta order | v051 在本 delta 创建前已冻结；创建 delta 后没有编辑 v051 |

本 delta 仅支持定位与保全复查；完整科学内容仍以冻结的 `idea-dossier-I01-001-v051` 为准，并需要新的独立叙事与语言评估。
