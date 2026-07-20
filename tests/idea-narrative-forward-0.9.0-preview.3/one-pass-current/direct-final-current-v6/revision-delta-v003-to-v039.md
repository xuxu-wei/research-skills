---
schema_version: research-idea-revision-delta.v1
plugin_version: 0.9.0-preview.3
artifact_id: revision-delta-I01-001-v003-to-v039
workflow_id: RID-SEPSIS-CSM-20260717-001
idea_id: I01-001
source_version: v003
revised_version: v039
change_type: editorial_repair_delta
source_artifact:
  artifact_id: idea-dossier-I01-001-v003
  version: v003
  path: tests/idea-test-0.9.0-preview.1/0.9.0-preview.1/03_ideas/nodes/I01-001/dossiers/idea-dossier-v003.md
revised_artifact:
  artifact_id: idea-dossier-I01-001-v039
  version: v039
  path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v6/idea-dossier-v039.md
scientific_change_declared: false
---

# Editorial revision delta: v003 to v039

本次只实施叙事结构、术语、句法、合并、移动和读者可及性修订。研究问题、目标、对象、证据基础、推断单位、方法选择、数值与时间规则、分析分支、证据状态和主张强度均未改变。本记录只说明修订覆盖情况，不判断叙事或语言就绪性。

## Narrative action map

| Action | Operation | Revised locator | Text-grounded acceptance evidence |
|---|---|---|---|
| NRP-001 | replace, split, reorder, add bridge | `Background, current state, gap, significance, and rationale` 的五个有序 H3 | `Background` 界定 Sepsis-3 与双时间问题；`Current state` 分别说明公共数据库和纵向、多状态、跨数据库与试验近邻能回答什么；`Gap` 明确“状态与结构的可重建性及跨数据库证据缺口”，并排除以组合新颖性代替缺口；`Significance` 说明区分生理信息与照护、测量政策表象的研究价值；`Rationale` 把双时间、三类过程分离、模拟重建和最终检验医院集逐一连接到缺口，只用末句预告阶段 III。 |
| NRP-002 | replace, compress | `Title, summary, audience, and positioning`; `Structured abstract` | 一句话摘要只有“24 个月阶段 I–II 主体证据”和“共享前提满足后的两个试验次要分析”两个并列主干；依次呈现研究对象、双公共数据库、模拟重建、隔离的跨数据库检验与条件性扩展。结构式摘要五项分别承担背景与缺口、目标与假设、方法、预期结果、贡献与影响功能，不重建完整分支流程。 |
| NRP-003 | consolidate | `Research design and methods > Randomized-trial observation bridge and independent clinical-state analysis under prespecified conditions`；其他章节的最小角色性陈述 | 技术权威小节完整保留共享前提、R0、冻结映射、R1 六项标准、一维投影摘要分析、独立临床状态分析、共享语义不足时的全组件停止、两个试验的分析集、缺失与死亡处理、Holm 多重性和亚组规则。主问题、Objective 4、WP5、第五证据链、计划产物和 Claim-Support 只保留各自所需的问题、目标、时间、链、产物或允许主张。 |
| NRP-004 | consolidate, delete duplicates | `Evidence chains`; `Feasibility, resources, risks, alternatives, and stop conditions` | 五条证据链均且仅含 `Input`、`Method / analysis / processing`、`Output`、`Supports` 四项，没有独立 limitations 字段。全局限制、未决规范、风险、替代和停止条件集中在第 14 个 H2；方法只保留直接改变估计目标、参数处理或分析分支的局部条件。 |
| NRP-005 | replace | `Key techniques and implementation` | 十个实现单元逐项给出接收输入、产生输出、持久审计记录、上下游接口和冻结或版本边界；末段明确标签与 G1 → 队列与变量注册 → 模型 → 锚定、模拟与敏感性 → 跨数据库检验 → 试验包的依赖。原十项科学内容均进入对应实现对象。 |
| NRP-006 | consolidate | 全部 15 个 H2，重点为 sections 5–14 | 时间与工作包只说明依赖、交付和后果；数据节只说明来源、现状和支持边界；方法节保存完整协议与数值标准；实现节保存对象与接口；证据链保存四项追踪；验收证据、产物与解释、贡献、主张审计和风险各自保持独立功能。15 个 H2 和五个证据链 H3 均保留。 |
| NRP-007 | define, replace | 首次出现位置：section 1 summary；section 3 `Background`; section 5 月 4–6；section 7 protocol、simulation、external validation、R0/R1 与 mapping | 首次出现即解释候选表征、临床事件时刻与标签可用时刻、G1、模拟重建性能、严格适当评分、适配医院集与最终检验医院集、四种参数处理状态、一维投影摘要（P_obs）、独立临床状态分析；R0/R1 先给中文科学全称再用短标签。 |

## Language finding map

| Finding | Operation | Revised locator | Acceptance-test evidence |
|---|---|---|---|
| LNG-R059-001 | replace all occurrences | H1、Title、summary、Primary question、Objective 4、第五证据链、贡献与 Claim-Support | 标题采用“计划开展跨数据库检验，并在满足预设条件时对随机对照试验的稀疏随访测量进行次要分析”；全文扫描无“稀疏 RCT”“实际稀疏 RCT 访视”或“条件性稀疏 RCT”。“稀疏”只修饰随访测量。 |
| LNG-R059-002 | define and concordance repair | section 1 summary；全篇中央对象、复杂模型和冻结产物处 | 首次定义“脓毒症全病程候选动态系统表征（下称‘候选表征’）”；中央对象后续只称“候选表征”；切换或非线性实现只称“复杂候选模型”；正式指冻结输出时使用“阶段 II 冻结的候选表征”。扫描无“候选架构”“候选系统表征”“最小全病程候选表示”或无范围的“整个系统模型”。 |
| LNG-R059-003 | define and replace all occurrences | Structured abstract；state table；simulation criteria；evidence and risk sections | 患者结局统一为“生理恢复状态”；模拟评价首次定义为“在已知生成机制下重建预设状态、转移和结构的性能（模拟重建性能）”；错误结构评价统一写为“错误结构被高置信度支持的频率”。扫描无“绝对恢复”“恢复门”“假置信”或跨角色裸用“恢复”。 |
| LNG-R059-004 | replace metaphors and define labels | 月 4–6 行；`试验语义与共同生理锚点合格性标准（R0）`；`测量一致性、校准与投影重建误差标准（R1）` | G1 首次以双数据库事件、转移、医院、锚点、时间精度和接口最低使用要求定义；R0/R1 先有中文全称。正文以启动条件、最低标准、判定标准或停止条件直接命名科学功能，不以裸用“门”定义条件；所有数值和后果保留。 |
| LNG-R059-005 | define and normalize | Structured abstract `Approach`; Data roles；Hospital-primary validation；第四证据链 | 数据集只称“适配医院集”和“最终检验医院集”，并说明后者在开发和适配期间不查看结局或模型性能。四种状态只用“不更新任何模型参数”“仅用适配医院集重新估计校准截距和斜率”“仅用适配医院集重新估计观测层参数”“用目标数据库重新拟合全模型（模型再开发）”。扫描无 adaptation/test、untouched、zero-update、decoder adaptation、full refit 或 transport updating。 |
| LNG-R059-006 | define and normalize | section 7 frozen mapping、两分析分支；第五证据链；Interpretation matrix；Claim-Support | 正式定义“基于实际 D7/D8 观测值计算的一维投影摘要（P_obs）”，结果统一为“随机分组在该访视投影摘要上的差异”；另一分支正式定义为“独立临床状态分析”。扫描无 death-ranked、fallback、projection-pass、trial-specific clinical-state 或以“扰动”命名结果。 |
| LNG-R059-007 | translate status dimensions | `Current resource and evidence status`; 第四证据链 output；Claim-Support；Identity boundary | 资源状态只用“已有公开资料支持/尚未核验/尚未生成/项目内衍生资料”；跨数据库结果只用“跨数据库稳定/仅适用于特定数据库/证据不足而不作解释”；主张状态只用“有支持/有条件支持/无支持”。读者正文以自然句表达研究身份边界；`identity_status` 仅保留在机器 frontmatter。 |
| LNG-R059-008 | replace all workflow metaphors with operations | 日期表、模拟响应、外部分析、outputs、risk matrix、identity boundary | 每个处置句直接写明停止哪一分析、转用何种分析、仍可报告什么、不能支持何种主张。例如零边不满足时“停止继续评估该复杂候选模型”，支持不足时“只作数据库层面的描述”。扫描无自动降级、降级、淘汰、晋级、挽救、救回、豁免、封存、封印、防火墙、no-go、fallback、失败图或失败产物。 |
| LNG-R059-009 | split dense conditions | one-sentence summary；R0；R1；Required analyses trial block；closest-work conclusion | 摘要保留一个句子和两个并列主干；R0/R1 采用定义句后接单类条件项目；试验启动证据改为四个项目；最接近工作段分为所得、未覆盖范围和允许定位三句。所有阈值、范围和分支均保留。 |

## Compact reader-facing concordance

| Core role | One reader-facing name | First-use locator | Competing forms removed or reclassified | All-occurrence result |
|---|---|---|---|---|
| Central object | 候选表征 | section 1 one-sentence summary，在全称后定义 | “候选架构”“候选系统表征”“候选全病程表示”“最小全病程候选表示”“整个系统模型”已删除；“复杂候选模型”只指可选实现；“阶段 II 冻结的候选表征”只指冻结产物 | 全文角色扫描通过；中央对象没有竞争名称 |
| Primary task and outcome 1 | 未来 12 小时首次发病风险任务；未来 12 小时首次发病累积发生概率 | Structured abstract `Approach`; protocol table | “主发病前任务”“12h CIF”改为描述性全称；CIF 仅在模型解释处以中文累积发生概率表达 | 所有任务、证据链和产物指向同一人群、历史与结局 |
| Primary task and outcome 2 | 发病后第 7 日状态占用任务；第 7 日“生理恢复状态或活着离开 ICU”的有利状态占用概率 | Structured abstract `Approach`; protocol table | “主发病后任务”“日 7 状态占用”统一；生理恢复不与模拟重建共用裸词 | 所有任务、证据链和产物指向同一互斥状态结局 |
| Diagnostic analyses | 伪遮蔽重建诊断；未来轨迹诊断 | `Research design and methods > Secondary representation diagnostics` | “部分状态重建”“轨迹诊断”等非唯一形式改为两个完整名称；“两项次要表征诊断”仅作集合称谓 | 两项诊断的输入、指标、范围与不能补足主体证据的角色一致 |
| Contingent projection branch and outcome | 一维投影摘要（P_obs）；随机分组在该访视投影摘要上的差异 | frozen mapping；随后的一维投影摘要分析 | “投影可观测状态摘要”“投影可观测摘要”“状态扰动”“有限随机化扰动”“projection-pass”已删除 | 正式定义后只使用投影摘要分析和固定结果句式 |
| Contingent independent branch and outcome | 独立临床状态分析 | section 1 用完整描述首次出现；section 7 正式定义短名 | “独立 death-ranked SOFA”“独立 SOFA 分支”“fallback”“trial-specific clinical-state”已删除 | 所有出现均保留死亡最差、SOFA 排序、活着出院最有利及与候选表征独立的含义 |
| Evidence and availability status | 四类资源状态；临床事件时刻和标签可用时刻 | resource-status table；section 3 `Background` | 英文证据状态串已删除；event/availability/as-of 竞争形式改为两个中文时间名称 | 状态维度不混用；时间名称在标签、任务和泄漏检查中一致 |
| External-test data roles | 适配医院集；最终检验医院集 | Structured abstract `Approach` | 适配区、最终测试区、adaptation/test、untouched final test、未触碰 test 等已删除 | 医院 30%/70% 分配、访问隔离和患者冲突规则均使用这两个名称 |
| Parameter-update states | 四个直接操作名称 | Hospital-primary cross-database validation | 零更新、仅校准、仅观测层更新、decoder adaptation、full refit 和 transport updating 已删除或展开 | 每次出现都能判断哪些参数改变；重新拟合全模型始终标为模型再开发 |
| Model disposition | 停止具体分析、转用具体模型、保留具体产物、停止具体主张 | date table 首次处置；simulation table 系统展开 | 降级、淘汰、晋级、挽救、封存、封印、no-go、stop 等压缩标签已展开；合同要求的英文 H2 标题不承担科学处置定义 | 每个处置句均明确停止、替代、可报告结果和不可支持主张 |
| Stage and decision labels | 阶段 I–II（24 个月最低交付）；阶段 III（最低交付之后） | summary and dated decisions | 内部流程状态词已删除；G1/R0/R1 只在中文全称定义后使用 | 阶段 III 从未写成阶段 II 的组成或补足手段 |

## Protected-content preservation map

| Protected item | Revised locator(s) | Item-level preservation evidence |
|---|---|---|
| PCR-001 | frontmatter identity anchor；Primary research question；mutually exclusive state system | 保留脓毒症中心、未发病在险时段、首次发病、发病后状态和结局连续体；互斥状态仍含持续脓毒症、生理恢复状态、恶化或新器官衰竭、活着离开 ICU、转院或无法继续观察和死亡；核心问题仍是候选动态系统表征而非普通预测。 |
| PCR-002 | one-sentence summary；Objectives 1–4；dated decisions；work packages | 保留 24 个月阶段 I–II、文献与专家知识约束、公共 ICU 数据、系统辨识和跨数据库检验，以及可审计科学证据、基准与资源的交付方向；没有把目标缩减为预测工具。 |
| PCR-003 | frontmatter identity anchor；Primary question；Observational target | 保留纵向脓毒症中心 ICU 患者系统、可比较未发病时段和发病后轨迹；主要目标分布仍以患者—时间状态和状态转移为单位，并在 protocol 与不确定性中保留患者和医院聚类。 |
| PCR-004 | Current resource and evidence status；Public ICU database roles and G1 audit | 保留文献与专家先验、MIMIC-IV、eICU-CRD 和预指定 HiRID/AmsterdamUMCdb 备份；数据库存在与版本已有支持，但团队访问、数据使用协议、提取、队列支持、具名人员与模型结果仍分别标为尚未核验或尚未生成。 |
| PCR-005 | Local randomized-trial evidence and present limits；stage III shared prerequisites | 保留 EXIT-SEP 与 XBJ-SCAP 仅为阶段 III 的条件性来源；本地材料仍是项目内衍生清洗或验证资料；授权、原始 CRF/SAP、随机化、中心、访视时序及死亡、住院、出院语义仍须核验。 |
| PCR-006 | minimum route；variable-role separation；anchoring；simulation criteria；conditions for non-interpretation | 保留固定顺序、状态/行动/测量过程分离、锚定与对齐、模拟重建和跨数据库约束。正文明确：20 种子对齐率<90%、自助法保留率<80%、外部符号一致率<80%、状态对齐<0.70 或区间未校准时，删除、合并或标为特定数据库/政策适用；预测表现不能抵消。 |
| PCR-007 | Conjunctive minimum success definition；Quantitative criteria for stage II；Hospital-primary validation | 保留数据支持、模拟重建、两项主要任务评分与校准、泄漏清零、不更新参数的最终检验、状态对齐和结构稳定的合取；两种适配参数重估与不更新参数分开报告且不能替代；阶段 III 不计入阶段 II。 |
| PCR-008 | complete protocol table；sensitivity paragraph；leakage audit；state system | 保留 72 小时/24 小时标本—抗菌药配对、基线 SOFA、滚动 24 小时成分、感染前 48 小时至后 24 小时窗口和首个可排序发病时刻；只分析首次发病、每住院重叠时间点总权重 1；同窗 A_t 与下一状态排序及同戳边排除；未来治疗、未来测量频率、重复住院、跨分配处理和结局驱动变量、时间方案、阈值均进入泄漏检查。 |
| PCR-009 | Structured abstract；Contribution and evidence ladder；closest-work comparison；Claim-Support | 保留所有模型、模拟、跨数据库和试验新结果尚未生成；贡献仍为条件性的整合、验证、基准与资源；各模块已有先例，完整组合缺口仅低至中等置信；无全球首次或新算法主张。 |
| PCR-010 | section 14 全部 H3；section 11 falsification criteria | 第 14 节一次性覆盖访问与团队、G1、标签泄漏、模拟重建、非随机缺失与低重叠、外部不更新参数、时间节点、试验数据与语义、共同锚点与映射以及最接近工作不确定性；风险矩阵逐项给出触发、替代、停止分析和主张后果；未决表保留临床尺度到模拟参数映射、多类别校准估计量/置信区间/阈值登记，并说明事件或参数下限不替代有效样本量与模拟稳定性；试验方向不一致或区间宽时不选择亚组改变结论。 |
| PCR-011 | dated decisions；stage III authority subsection；section 14 global boundaries | 保留阶段 I–II 24 个月、阶段 III 在其后；共享前提明确为阶段 II 成功并冻结、个体数据授权和核心试验语义。投影分支另需共同锚点与 R1；这些额外条件不提升为整个组件前提。观测关系不成立但 SOFA 与共享语义可核验时仍可开展独立临床状态分析；核心语义不可核验时两种新访视结局均停止；试验结果不能补足阶段 II。 |
| PCR-012 | Core hypothesis and non-hypotheses；Global limitations and boundary conditions；Interpretation matrix | 保留观察性数据和预测表现不支持真实因果网络、治疗因果效应、反事实策略、机制、中介、控制或数字孪生；随机试验次要分析不验证未测潜在动力学、转移边或候选表征整体；当前不是已验证模型、临床决策工具、药物平台或无条件推广依据。 |

## Shared-prerequisite and branch-fidelity check

| Component | Dossier evidence | Fidelity result |
|---|---|---|
| Shared prerequisites for either new trial visit analysis | section 7 stage III opening paragraph enumerates: stage II success and freeze; individual-data authorization; verifiable randomization/analysis set, center/strata, D7/D8 timing, death, hospitalization, live discharge and transfer semantics | These three conditions govern both branches and are not omitted from either trial row. |
| Projection-summary branch eligibility | R0 separates the shared trial-semantics part from the projection-only common-anchor part; frozen mapping defines one-dimensional projection summary (P_obs); R1 lists all six external and blinded-trial criteria | Common-anchor count, unit/time agreement and R1 are conditions only for the projection-summary branch, not for the entire stage III component. |
| Projection-summary consequence | `One-dimensional projection-summary analysis` preserves pre-visit death as worst, in-hospital P_obs ordering, live discharge as best and center/strata-compatible probabilistic index | Allowed output remains only random-group difference at the actual visit summary; no latent dynamics or whole-representation claim. |
| Independent clinical-state branch eligibility | `Independent clinical-state analysis` begins with failure of R0 common-anchor portion or R1, while requiring SOFA and shared trial semantics | Failure of observation bridging does not remove this branch; no projection-only condition is promoted to a shared prerequisite. |
| Independent clinical-state consequence | Same subsection preserves death worst, in-hospital SOFA high-to-low, live discharge best, and explicit independence from stage II frozen candidate representation | Result is a trial-specific secondary clinical-state difference, never a perturbation or validation of the candidate representation. |
| Whole-component stopping consequence | Same subsection and each trial row state that unverifiable D7/D8, randomization, center or survival semantics preclude both new visit-outcome analyses; only original-endpoint reproduction or data audit remains | Shared-semantic failure stops the component; it is distinct from projection-only failure. |
| Stage II non-substitution | Conjunctive success definition and section 14 time boundary state that stage III is after the minimum deliverable and cannot fill stage II resource, reconstruction, primary-task or external-validation requirements | No downstream branch is allowed to replace a failed stage II condition. |

## Mechanical and scope checks

- Complete dossier: one H1 and all 15 required H2 headings in required order.
- Section 3: exactly five non-empty ordered H3 functions — Background, Current state, Gap, Significance, Rationale.
- Evidence chains: five human-readable H3 chains; each has exactly Input, Method / analysis / processing, Output and Supports.
- Frontmatter: `plugin_version: 0.9.0-preview.3`; `change_type: editorial_repair`; `based_on` contains only the v003 logical artifact ID, version and path.
- Dossier lint: `OK` with `--expected-plugin-version 0.9.0-preview.3`.
- Files written: only `idea-dossier-v039.md` and this delta in the assigned directory.

## Unresolved items

No unresolved narrative action, language finding or protected-content mapping remains in this editorial repair. Scientific specifications that were already unresolved in v003 remain explicitly pending in section 14; no value or method was inferred. Fresh independent preservation, narrative and language assessment is still required before any readiness decision.
