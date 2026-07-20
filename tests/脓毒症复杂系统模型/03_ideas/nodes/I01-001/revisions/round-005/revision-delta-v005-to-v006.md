---
schema_version: research-idea-revision-delta.v1
plugin_version: "0.10.0"
artifact_id: revision-delta-I01-001-v005-to-v006
workflow_id: sepsis-complex-system-idea-generation-v001
idea_id: I01-001
version_id: v005-to-v006
path: 03_ideas/nodes/I01-001/revisions/round-005/revision-delta-v005-to-v006.md
source_dossier_ref:
  artifact_id: idea-dossier-I01-001-v005
  version: v005
  path: 03_ideas/nodes/I01-001/dossiers/idea-dossier-v005.md
target_dossier_ref:
  artifact_id: idea-dossier-I01-001-v006
  version: v006
  path: 03_ideas/nodes/I01-001/dossiers/idea-dossier-v006.md
writer_brief_ref:
  artifact_id: editorial-repair-writer-brief-I01-001-r002
  version: r002
  path: 03_ideas/nodes/I01-001/revisions/round-005/editorial-repair-writer-brief-r002.yaml
protected_register_ref:
  artifact_id: protected-content-register-v002
  version: v002
  path: 05_state/protected-content-register-v002.yaml
source_skill: multi-path-idea-generator
created_round: 6
change_type: editorial_repair_delta
frozen: true
---

# I01-001 从 v005 到 v006 的编辑修订记录

## 修订范围与顺序

本次只执行批准的 LANG-001 和 LANG-002。v006 先完成四个有界区段的修订与全文一致性检查，随后通过编排端冻结前合规检查并设为冻结，最后才生成本记录。未对批准范围以外的非阻断观察项开展修订、复现或额外测试。

冻结前合规结论为 **PASS**：LANG-001 和 LANG-002 均完整执行；五项研究身份字段逐字保留；58 项保护内容均可在 v006 定位且语义、条件和主张强度保持不变；未发现范围外修订或需要同一作者返修的重大问题。

## 批准修订项的逐项证据

| 修订项 | 操作 | v006 实际定位 | 文本证据与验收结果 |
|---|---|---|---|
| LANG-001 | 替换 | H1 题名；`Title, summary, audience, and positioning` 的 Title 字段；`Title and positioning claim-support table` 的数据库设计关系行 | H1 与 Title 字段均逐字为“受约束的脓毒症全病程动态状态模型：在一个数据库中开发并在异质数据库中外部验证”；定位表第一列逐字为“在一个数据库中开发并在异质数据库中外部验证”。正文中“跨数据库构建”为 0 处；方法部分仍明确外部数据库不参与潜在状态重估、重命名、结构选择或阈值修改。 |
| LANG-002 | 定义并替换 | `Title, summary, audience, and positioning` 的定义段；`Structured abstract`；第 3–14 节所有相关表述 | 外部验证定义后逐字加入批准的首次定义，完整列出六个器官功能域、同期生命体征、当前器官支持和短时变化方向，并说明开发状态在外部数据库中的占用、分布距离和可分离性以及它与患者病程内状态转移的区别。正文中“临床锚定”“锚定分布”“锚定距离”“状态迁移”“表示迁移”“迁移诊断”“状态表示的跨库可重复性”和“跨库可分离性”均为 0 处；“状态转移”仅保留 1 处，明确指患者病程内时间演化。方法权威仍完整保留冻结占用、距离、可分离规则以及未迁移、合并、拆分的条件和任务后果。 |

## 保护内容逐项追踪

保护结果：**58/58 保留**。

| 保护项 | v006 实际定位 | 条目级保留证据 |
|---|---|---|
| PCR-001 | `Research question, objectives, and core hypothesis` 的 Primary research question；`Research design and methods` 的 H3 行 | 人群、受约束低维全病程模型、一个开发库、一个异质外部库、四项任务及 H3 不以潜在状态为真值的边界均保留；仅把外部状态比较改为已定义的明确名称。 |
| PCR-002 | `Research question, objectives, and core hypothesis` 的 Objectives 1–4 | 约束与资源验收、开发期可辨识性与冻结、外部四任务平行评价、按任务和外部冻结规则限定结论的四项目标均保留。 |
| PCR-003 | `Title, summary, audience, and positioning` 的术语定义段 | 全病程边界、生理—观测—处置区分、文献—专家约束、一个开发库与一个异质外部库的冻结后直接应用关系及动态临床系统视角均保留。 |
| PCR-004 | `Research design and methods` > `Unified full-course population, time axis, and state space` | 感染风险入口至出 ICU、死亡或删失的队列边界，未发病与发病患者贡献、患者隔离及五类状态空间组成均未改变。 |
| PCR-005 | 首节实证核心段；`Research design and methods` > `Conditional randomized-trial and animal follow-up` | 12–18 个月两库核心研究、随机试验与动物研究的条件性和时间表外地位，以及两类后续研究不能补救核心失败的边界均保留。 |
| PCR-006 | `Data, materials, and existing evidence base` > `Pre-model constraint-table prerequisite` | 约束表范围、专家构成、独立判断与匿名反馈、80% 支持要求、临床与方法学双重支持及异议保存规则均保留。 |
| PCR-007 | `Data, materials, and existing evidence base` > `Required inputs and database constitution` | 一个公开开发库和一个异质外部库的资格、独立性、6 小时网格、共同变量、冻结阈值及不得按外部结果选库的要求均保留。 |
| PCR-008 | `Data, materials, and existing evidence base` > `Database, team, and compute qualification` | 真实样例审计项目、有效转移定义、五个核心角色、计算基准、替代或停止规则及不采用通用事件数硬阈值均保留。 |
| PCR-009 | `Required inputs and database constitution` 的第三数据库及试验数据行 | 第三库仅作锁定核心结果后的可选压力测试且不进入 Holm 家族；EXIT-SEP 与 XBJ-SCAP 仍为资格未核实的条件性资源。 |
| PCR-010 | `Research design and methods` > `Unified full-course population, time axis, and state space` | 持续恢复的存活、脱离三类器官支持与六域连续 24 小时条件，任务二首次事件属性、随后恶化可能性及真实时间与 6 小时评分网格的区别均保留。 |
| PCR-011 | `Research design and methods` > `Primary model and task-specific comparators` | 隐半马尔可夫模型的状态、停留时间、观测、观测过程和治疗输入角色，以及四任务各两个比较模型、相同输入规范与最不利损失差判定均保留。 |
| PCR-012 | `Research question, objectives, and core hypothesis` 的 Confirmatory family | 前置条件与统计假设分离、患者级汇总、D_kc 与 Delta_k、max-t、单侧 95% 上界、最大 p 值、Holm 0.05 及双侧区间规则均保留。 |
| PCR-013 | `Research design and methods` > `Four task-level summary hypotheses` 的 H1 行 | 每 6 小时起点、风险集、6/12/24 小时四类结局、Brier 损失、删失、权重、两个比较模型和共同通过规则均保留。 |
| PCR-014 | 同一任务表的 H2 行 | 索引后 6/12/24/48/72 小时起点、24/48/72/168 小时结局、四类竞争结局、患者内汇总、比较模型和 Delta_2 判定均保留。 |
| PCR-015 | 同一任务表的 H3 行 | 六个器官功能域和三类器官支持、12 小时连续块遮蔽、实际测得目标、九域等权、逆观测概率权重、两个比较模型及潜在状态非真值边界均保留。 |
| PCR-016 | 同一任务表的 H4 行 | 每 6 小时起点、24/48/72/168 小时状态向量、吸收编码、结果域与时域等权、两个比较模型及 Delta_4 判定均保留。 |
| PCR-017 | `Four task-level summary hypotheses` 表前后的权重说明 | 开发期冻结基础权重、患者内再归一、外部权重算法的信息截断、患者级重采样、事件与删失区分以及敏感性不改主判定均保留。 |
| PCR-018 | `Research design and methods` > `Complexity selection and identifiability` | 模拟与内部时间诊断、阈值冻结时点、复杂度缩减顺序、逐步重跑及最小统一模型失败时停止全病程潜在状态主张均保留。 |
| PCR-019 | `Research design and methods` > `External application and cross-database state-representation diagnostics` 第一段；`Key techniques and implementation` 第 7 项 | 外部仅直接应用冻结模型且不重估或重命名；预定临床特征四部分、占用/距离/可分离规则、无一一匹配、未迁移/合并/拆分条件及禁用验证结局改规则均保留。 |
| PCR-020 | 同一方法小节第二段 | 必需状态定义、任一必需状态未迁移或同阶段合并/拆分时的完整表示后果、任务可执行性后果及其他任务最多部分支持的边界均保留。 |
| PCR-021 | `Research design and methods` > `Multiplicity and overall interpretation` | 四任务平行、10,000 次 max-t、Holm 阈值顺序、总体/部分/失败定义、有限校准限制及第三库不能替代无调整判定均保留。 |
| PCR-022 | `Research content and work packages` 全表 | 月 1–2、3–6、7–12、13–18 的资格、开发、外部验证、敏感性与复现顺序和交付均保留，后续试验与动物研究仍不在核心时间表内。 |
| PCR-023 | `Research design and methods` > `Conditional randomized-trial and animal follow-up` 第一段 | 总体支持、模型与代码冻结、EXIT-SEP 权限与逐时变量、交互功效和重叠核验等启动条件，以及随机分配和 XBJ-SCAP 边界均保留。 |
| PCR-024 | 同一小节第二段 | 动物研究须由合格试验与人类观察共同提出具体可干预机制并具备平台、伦理、样本量依据；MQTiPSS、ARRIVE 2.0 及不能补救核心失败均保留。 |
| PCR-025 | `Data, materials, and existing evidence base` > `Existing evidence base` | 各类代表性来源、标签实现的单项针对性证据、试验与表型来源的直接支持及证据只作为设计依据的强度均未提升。 |
| PCR-026 | `Structured abstract` 的 Expected result 与 Contribution and impact | 模型、四任务结果、两类诊断和支持/失败均保持为预期产物；贡献仍是可证伪的预测性表示路线，不是已完成结果或因果、部署主张。 |
| PCR-027 | `Contribution, innovation, impact, application, and closest-work comparison` > `Bounded contribution frame` | 信息结构决定复杂度、一个统一模型下四项患者级确认性假设、冻结模型外部应用与观测过程分列三项贡献均保留，性质仍限于方法整合、外部验证和失效边界证据。 |
| PCR-028 | `Expected outputs, falsification criteria, and interpretations` > `Result-dependent interpretations` | 全通过、部分通过、非必需状态未全满足规则、仅 H3 通过、外部全部失败及有限校准/第三库更优的六类允许解释均保留且未增强。 |
| PCR-029 | `Feasibility, resources, risks, alternatives, and stop conditions` > `Working assumptions` 的 WA-01 | 成果组织尚未确认、核心研究可独立成文的暂定条件、月 3 确认点及不成立时只调整组织与分工均保留。 |
| PCR-030 | 同一表的 WA-02 | 第三库仅在两库结果锁定且资源允许时加入、不进入核心判定、月 12 后确认及不足时取消均保留。 |
| PCR-031 | `Limitations and boundary conditions` 第 1 项 | 有界检索、不能声称“首个”或“完整系统”及 2026 年来源需复核的限制均保留。 |
| PCR-032 | 同一清单第 2 项 | 数据访问、真实样例和完整变量字典尚未取得，数据库存在不等于本项目可用的限制均保留。 |
| PCR-033 | 同一清单第 3 项 | 人群、实践、语义、采样和结局差异及其可能混合病例、标签与观测过程的边界均保留。 |
| PCR-034 | 同一清单第 4 项 | 感染风险入口、标签、索引时点、任务时域和持续恢复定义需冻结代码与敏感性分析界定的限制均保留。 |
| PCR-035 | 同一清单第 5 项 | 治疗与测量受病情和既往处置影响，模型仅支持预测性条件时间关联而不支持因果、最优治疗、反事实或中介主张的边界均保留。 |
| PCR-036 | 同一清单第 6 项；`Working assumptions` 的任务三固定操作化说明 | 跨数据库状态表示诊断、开发期恢复诊断和观测重建的各自判定对象均保留，三者仍不能证明真实生物状态；H3 仍只评价遮蔽实测变量预测。 |
| PCR-037 | `Limitations and boundary conditions` 第 7 项 | 外部验证适用范围及预测改善不等于临床效用、真实世界效果、部署、治疗建议、机制或监管用途的边界均保留。 |
| PCR-038 | 同一清单第 8 项 | 观测与删失权重依赖冻结模型和可观测历史，极端权重、未测量因素与跨数据库观测政策差异可致残余偏倚的限制均保留。 |
| PCR-039 | 同一清单第 9 项 | EXIT-SEP 与 XBJ-SCAP 的权限、逐时变量和功效未核实、既有表型分析重叠及随机分配不自动识别中介网络均保留。 |
| PCR-040 | 同一清单第 10 项 | 动物研究的机制、平台、样本量、伦理、预算缺口，人鼠转化证据冲突及动物结果不能作临床外部验证均保留。 |
| PCR-041 | 同一清单第 11 项 | 约束表、核心团队和计算承诺尚未完成，12–18 个月只约束核心研究且条件性后续无时间资源承诺均保留。 |
| PCR-042 | `Risks, alternatives, and stop conditions` 的两库资格行 | 月 2 末失败后只能按预登记顺序核验替代库且不看模型表现，仍失败即停止跨库主分析的规则均保留。 |
| PCR-043 | 同一表的约束表不合格行 | 补齐专家轮次与逐项记录、禁止数据团队代填及月 2 末仍不合格则不拟合的后果均保留。 |
| PCR-044 | 同一表的团队或计算不足行 | 先取消第三库、额外亚组和非必需消融，五角色或核心计算仍不足即停止复杂模型路线的规则均保留。 |
| PCR-045 | 同一表的最小统一模型不可恢复行 | 按状态数、转移、停留时间和交互顺序简化并重跑，最小模型仍失败即停止统一潜在状态主张均保留。 |
| PCR-046 | 同一表的外部必需状态未迁移、合并或拆分行 | 保留开发标签、禁止结局重定义或强制匹配、完整表示失败、受影响任务失败及其他任务最多部分支持均保留。 |
| PCR-047 | 同一表的 Holm 未通过行 | 仍报告估计与区间、不改变其他任务检验、未通过任务不受支持且不能由其他任务、校准、第三库、试验或动物研究补救均保留。 |
| PCR-048 | 同一表的独立复现失败行 | 暂停解释、核对字段血缘/聚类/权重/代码及仍不能复现则不提交核心主张的规则均保留；诊断名称仅按 LANG-002 统一。 |
| PCR-049 | `Limitations and boundary conditions` 第 1 项 | “首个”“完整系统”“无人研究”及相关首次性主张继续被明确排除。 |
| PCR-050 | 同一清单第 5 项 | 模型边、权重和治疗系数仍只作预测性条件时间关联解释，因果调控、最优治疗、治疗作用、个体反事实和中介网络主张继续被明确排除。 |
| PCR-051 | 同一清单第 6–7 项；任务三固定操作化说明 | 状态诊断、潜在状态恢复、任务预测和观测重建仍不能证明真实生物状态；临床效用、部署、治疗、机制与监管用途继续被明确排除。 |
| PCR-052 | `Research design and methods` > `Conditional randomized-trial and animal follow-up` | 随机试验与动物研究仍不能改写核心未通过任务；随机分配不自动识别中介网络，动物结果不构成临床模型外部验证。 |
| PCR-053 | 同一小节末句 | 随机试验与动物研究仍按各自资格和后果独立启动，一项不可行不取消另一项，且两者均不能替代或补救核心两库研究。 |
| PCR-054 | `Working assumptions` 的任务三固定操作化说明；方法任务表 H3 行 | H3 仍固定为从部分已观测历史预测按规则遮蔽但实际测得的临床变量，只支持测量补全；目标变量、遮蔽块、权重稳定性与外部可执行性仍须实证通过。 |
| PCR-055 | `Research question, objectives, and core hypothesis` 的 Core hypothesis；方法任务表 H3 行 | 四项外部患者级汇总损失均低于各自比较模型的假设、H3 仅以遮蔽实测值计分及必需开发状态在预定临床特征上的外部可分离性均保留。 |
| PCR-056 | `Title, summary, audience, and positioning` 的 Positioning and contribution frame | 统一全病程动态复杂系统模型的核心身份、同一冻结模型覆盖三个病程阶段、四任务各有一个确认性假设且无跨任务总准确率均保留。 |
| PCR-057 | `Key techniques and implementation` 第 2 项 | 每个共同概念的原始字段、单位、时间戳、聚合窗、异常值和缺失编码记录要求，以及数据库特异变量不得进入主要跨库模型均保留。 |
| PCR-058 | `Required analyses and evidence` > `During development` 第 3 项；`Falsification criteria` 末项 | 患者级时间泄漏、跨切分、未来信息、比较模型不一致及外部数据参与选择的审计均保留；由测量强度、标签、泄漏或不一致权重造成的增益仍构成证伪情形。 |

## 全文核心角色一致性

| 核心角色 | v006 统一名称 | 首次读者可见定位 | 被删除或重新归类的竞争形式 | 全篇扫描结果 |
|---|---|---|---|---|
| 中央研究对象 | 受约束的脓毒症全病程动态状态模型 | H1 题名 | “统一低维动态状态模型”等仅保留为描述性短语，不作为竞争题名 | 题名、摘要、问题、方法与贡献均指向同一全病程对象。 |
| 数据库设计关系 | 在一个数据库中开发并在异质数据库中外部验证 | H1 题名 | “跨数据库构建与外部验证”删除 | 精确短语只用于 H1、Title 字段和定位表三处；其他段落均保持一个开发库与一个异质外部库的分工。 |
| 外部状态比较程序 | 跨数据库状态表示诊断 | 首节外部验证定义后的新增句 | 临床锚定状态迁移诊断、状态迁移、表示迁移及无明确对象的迁移诊断删除 | 所有相关用例均采用统一名称或直接写明开发状态在外部数据库中的占用和可分离性。 |
| 外部状态比较所用变量 | 预定临床特征 | 首节新增定义 | 临床锚定特征、预定临床锚定特征和生理临床锚定删除 | 首次定义与方法权威均列明六个器官功能域、同期生命体征、当前器官支持和短时变化方向。 |
| 患者病程时间演化 | 患者病程中的状态转移 | 首节新增定义 | 不再用“状态迁移”指代外部数据库比较 | 正文“状态转移”仅 1 处，明确限定为患者病程内时间演化；方法中的具体转移结构含义未改变。 |
| 主要研究任务 | 四项预定预测任务 | 首节完整构想摘要 | 无竞争任务集合 | H1–H4 的风险集、时域、结果、损失和比较模型均保持原定义。 |
| 主要统计判定 | 每项任务的患者级汇总损失差 Delta_k | 第 4 节 Confirmatory family | 时点、时域和结果域仅为患者内组成，不作为竞争主要判定 | 四个任务各只有一个原假设，并保持 max-t 与 Holm 判定。 |
| 计划贡献 | 方法整合、外部验证和失效边界证据 | 第 12 节 Bounded contribution frame | 未引入科学、数据或方法首创性主张 | 题名、摘要、贡献段和定位表的主张强度一致，仍以计划实施和实际外部结果为限。 |

## 冻结后检查

| 检查 | 结果 |
|---|---|
| 编排端冻结前行动合规 | PASS；2/2 批准修订项完整，5/5 研究身份字段逐字相同，58/58 保护内容可定位，无范围外修订。 |
| 确定性结构 lint | `lint_idea_dossier.py ... --expected-plugin-version 0.10.0` 返回码 0 和 `OK`。唯一 advisory 指向“跨数据库状态表示诊断”；该合法科学术语已在首次出现处立即给出变量、操作、判定对象及与患者病程状态转移的区别，因此已按规则处置。 |
| 题名与定位 | H1、Title 字段及定位表关系短语各精确匹配 1 次；正文“跨数据库构建”为 0 处。 |
| LANG-002 禁用形式 | 九组禁用或歧义形式在读者可见正文中均为 0 处；机器可读 identity_anchor 按 brief 要求逐字保留，不纳入读者用语替换。 |
| 开发库—外部库关系 | 方法正文明确外部库不重新估计潜在状态、状态数、转移参数或观测参数，不重命名状态，且外部数据不触发结构选择或阈值修改。 |
| 科学范围与证据状态 | v005 与 v006 的正文数字标记集合、行内公式集合、参考文献全文和 Markdown 表格数分别一致；除批准术语修订外未增加或改变数据、方法、结果、证据或主张强度。 |
| 文档完整性 | 15 个固定 H2 章节顺序完整；表格、公式和参考文献无断裂；冻结后全文检查失败项为 0。 |

本记录仅证明批准的编辑修订及保护内容追踪已经完成，不构成叙事质量、语言质量或研究构想评价结论；后续仍须由新的独立审阅者基于冻结的 v006 开展相应审阅。
