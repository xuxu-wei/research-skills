---
schema_version: research-idea-revision-delta.v1
plugin_version: 0.9.0-preview.3
artifact_id: revision-delta-I01-001-v003-to-v048
workflow_id: RID-SEPSIS-CSM-20260717-001
idea_id: I01-001
version_id: v003-to-v048
path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v14/revision-delta-v003-to-v048.md
based_on:
  - artifact_id: idea-dossier-I01-001-v003
    version: v003
    path: tests/idea-test-0.9.0-preview.1/0.9.0-preview.1/03_ideas/nodes/I01-001/dossiers/idea-dossier-v003.md
  - artifact_id: editorial-repair-writer-brief-I01-001-r096
    version: r096
    path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/baseline-current/editorial-repair-writer-brief-r096.yaml
  - artifact_id: protected-content-register-I01-001-v004-r004
    version: r004
    path: tests/idea-narrative-forward-0.9.0-preview.3/run-001/inputs/protected-content-register-v004.yaml
source_skill: multi-path-idea-generator
change_type: editorial_repair_delta
revised_dossier:
  artifact_id: idea-dossier-I01-001-v048
  version: v048
  path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v14/idea-dossier-v048.md
  frozen: true
frozen: true
---

# Revision delta: idea dossier v003 to v048

本次变更只调整表达、结构和信息位置；研究身份、科学问题、数据与证据状态、数值和时序规则、分析处理、条件关系及主张强度未改变。保真回归检查后，v048 曾仅为修正 frontmatter 而暂时解除冻结：`identity_anchor` 五个字段均恢复为 v003 的逐值原文，正文与标题未改；完整 dossier 随后重新通过确定性结构检查并冻结，本 delta 在该冻结之后重写。

## Identity-anchor verbatim preservation

| Identity-anchor field | Source locator | Revised locator | Preservation result |
|---|---|---|---|
| `primary_research_question` | v003 frontmatter `identity_anchor.primary_research_question` | v048 同名字段 | **verbatim preserved**；逐值比较相等 |
| `primary_objective` | v003 frontmatter `identity_anchor.primary_objective` | v048 同名字段 | **verbatim preserved**；逐值比较相等 |
| `study_object` | v003 frontmatter `identity_anchor.study_object` | v048 同名字段 | **verbatim preserved**；逐值比较相等 |
| `core_data_or_evidence_base` | v003 frontmatter `identity_anchor.core_data_or_evidence_base` | v048 同名字段 | **verbatim preserved**；逐值比较相等 |
| `primary_unit_of_inference` | v003 frontmatter `identity_anchor.primary_unit_of_inference` | v048 同名字段 | **verbatim preserved**；逐值比较相等 |

Parsed comparison result: **5/5 fields equal; the complete `identity_anchor` mappings are equal**.

## Included repair items

| Repair item | Revised locator | Actual operation | Acceptance evidence in v048 |
|---|---|---|---|
| NRP-001 | `Background, current state, gap, significance, and rationale` 下五个规定 H3 | split, move, consolidate | `Background` 说明 Sepsis-3、SOFA、病程和双时钟；`Current state` 说明数据库与方法近邻；`Gap` 明确现有证据不能回答的全病程模型恢复与跨库稳定性问题；`Significance` 说明区分可复现关系与数据/政策伪结构的科学后果；`Rationale` 以双时钟、变量角色、已知生成机制模拟和外部测试连接差距与设计。五段均非空，未以组合新颖性代替证据问题，未列完整限制或指向第 14 节。 |
| NRP-002 | H1；`Title, summary, audience, and positioning` | replace, reorder, move | H1 与 `Title` 均为“脓毒症全病程动态复杂系统模型的构建与跨数据库验证”；标题不含试验或后续阶段。完整 Idea 摘要以研究问题、24 个月阶段 I–II 主体研究、总体设计和预期贡献为主干，只有末尾一个高层条件性用途，且全字段只有一个结尾句号。 |
| NRP-003 | `Research design and methods > 主体研究后的条件性分试验次要分析` | consolidate, rename, move | 连续方法小节先给阶段 II、授权和试验核心语义等共享前提，再分别给共同指标与固定计算满足要求时的访视状态分数分析，以及固定计算不满足但试验核心信息完整时的预设独立临床状态分析；随后给核心语义不足时不开展新访视结局分析。输入指标、公式、数值标准、死亡/住院/出院排序、概率指数或胜率、缺失、多重性、分试验报告和停止条件仅在该方法权威位置完整出现。 |
| NRP-004 | `Feasibility, resources, risks, alternatives, and stop conditions`；第 7、11 节 | consolidate, move, delete | 第 14 节分别设置可行性与资源、工作假设、限制与边界条件、运行风险四项功能；11 个限制条目一次覆盖全部家族和不支持主张。第 7 节保留方法资格与互斥分析，第 11 节只保留结果证伪和结果依赖解释；五条证据链均无 `Limits and failure conditions` 字段，全篇无第 14 节指针。 |
| NRP-005 | `Key techniques and implementation` | replace | 十行复现表均按“数据字段或科学构念—计算关系—输出记录—核查用途与依赖”组织，覆盖双时钟、数据支持、变量角色、队列状态、模型输入输出、模拟、医院分区、试验共同指标、不确定性和阴性对照；没有工具隐喻、方法理由的整段复述或完整限制。 |
| L-001 | H1、section 1 首次定义、structured abstract、研究问题、目标 2 及全篇 | replace, define, concordance | 首次定义稳定使用“候选动态复杂系统模型”，并明确患者状态及状态转移表示是该模型组成；标题、摘要、问题、方法、贡献与主张表未把研究身份改写为普通纵向表示、状态表示或单一预测模型。旧竞争形式全篇扫描无正文命中。 |
| L-002 | `Data, materials, and existing evidence base > 公共重症监护数据库角色与观测数据支持` | define, replace | 首次写为“观测数据可用性与支持审计（G1）”，同句列明访问、事件/转移、时间戳、单位、共同指标密度、医院覆盖和接口，并明确它不是状态空间可观测性秩判定；后续 G1 均指同一数据支持检查。 |
| L-003 | structured abstract、目标 3、`相对已知生成机制的模拟检验`、evidence chain 2、第 11 与 14 节 | replace, expand | 方法逐项写明正确生成、零边、过拟合、遗漏状态、错误滞后和错误观测方程；表中直接标出状态、转移、符号/滞后、关系检出、错误关系、错设结构和概率校准的指标、阈值、重复比例与处理后果。正文没有“假置信”“绝对门”“恢复门”或新造替代短称。 |
| L-004 | `观察性目标、锚定、缺失与可解释范围`、模拟表、第 9、11、14 节 | replace | 每一处均直接说明被停止解释的状态或关系、触发原因及删除、合并、改用较简单模型或限定为数据库/照护政策特异的结果；预测用途和结构解释分别处理。全文“弃权”扫描为零。 |
| L-005 | structured abstract、阶段 II 成功定义、`医院优先的跨数据库评估`、evidence chain 4、第 11–14 节 | define, consolidate | 方法首次分别定义“预先隔离且未用于模型选择的外部测试集”和“未更新外部性能评估”，再区分基于适配区的重新校准、观测层更新和全模型更新与再开发；明确三类更新不能替代主要未更新评估未达到标准的结果。禁用英文旧称扫描为零。 |
| L-006 | `主体研究后的条件性分试验次要分析` | replace, define | 该小节直接列出试验实测且语义、单位、时间合格的共同指标，给出阶段 II 固定标准化、载荷奇异值分解和 P_obs 公式，说明输出是一维访视状态分数，并以随机分配组间的概率指数或胜率比较。全文无“观测投影”“投影可观测”“投影摘要”“projection-pass”或“随机化扰动”。 |
| L-007 | 同一方法小节的“固定计算不满足要求但试验核心信息完整时的预设独立分析”及试验表 | replace, expand | 首次直接写明死亡最不利、访视时存活住院者按 SOFA 从高到低、访视前活着出院最有利；两试验分别使用实际第 7/8 日、中心或分层相容的概率指数或胜率及规定缺失处理，并明确该分析不使用 P_obs、不作为阶段 II 模型证据。全文无 `death-ranked`、`fallback` 或含混的“独立 SOFA”短称。 |
| L-008 | section 3 首次术语；第 6–8 节；所有自由 H3、表格与正文 | define, replace, concordance | ICU、EHR、SOFA、CRF、SAP、RCT、G1、MNAR、ESS、MCSE、ARI、MAE、FDR 均在首次读者可见位置给出中文科学功能；自由 H3 使用中文，正式数据库/试验名称、公式变量与参考文献题名保持原名。正文无“门、降级、封印、防火墙、审计器、投影器”等项目隐喻。 |
| L-009 | section 1 的 `One-sentence complete-Idea summary` | replace | 摘要以候选动态复杂系统模型及其全病程问题开头，随即说明 24 个月阶段 I–II 主体研究、两库、模拟、跨库评估和正向贡献，末尾只有一个从属的条件性用途；检查结果为一个中文句号且位于字段末尾。 |
| L-010 | 第 7、11、14 节及全篇 | consolidate, delete | 第 14 节第 11 个限制条目一次完整列出观察性、试验和当前计划不支持的主张类别；第 7 节仅保留改变估计对象或分析选择的局部边界，第 11 节仅保留结果特异解释。其他位置没有重复多项清单、完整限制复述或跨节指针。 |

Coverage: **15/15 included repair items mapped and accepted**.

## Protected-content preservation

| Protected ID | Revised locator(s) | Item-level preservation evidence in v048 |
|---|---|---|
| PCR-001 | frontmatter `identity_anchor.primary_research_question`；section 1 positioning；section 4 主要研究问题 | `primary_research_question` 与 v003 **verbatim preserved**；正文保留构建并验证以脓毒症为中心、覆盖未发病在险时段、首次发病、发病后互斥状态和结局的动态复杂系统模型身份，并明确它不是普通风险评分或单一预测器。 |
| PCR-002 | frontmatter `identity_anchor.primary_objective`；section 1 摘要；section 3 `Significance`；section 11 `计划产物` | `primary_objective` 与 v003 **verbatim preserved**；正文保留 24 个月阶段 I–II、文献与专家知识约束、公共 ICU 数据、模型构建与跨数据库验证，同时明确高水平论文、可审计证据和可复用资源为交付方向，且交付不收缩为单一预测工具。 |
| PCR-003 | frontmatter `identity_anchor.study_object` 与 `identity_anchor.primary_unit_of_inference`；sections 1、2、4；第 7 节任务方案 | `study_object` 与 `primary_unit_of_inference` 均与 v003 **verbatim preserved**；正文保留纵向、脓毒症中心的 ICU 患者系统及可比较未发病时段和发病后轨迹，主要推断单位仍为尊重患者与医院聚类的患者—时间状态及状态转移。 |
| PCR-004 | frontmatter `identity_anchor.core_data_or_evidence_base`；section 6 `当前证据与后续要求`、数据库角色与 G1 表 | `core_data_or_evidence_base` 与 v003 **verbatim preserved**；正文保留文献/专家先验、MIMIC-IV、eICU 及预定 HiRID/AmsterdamUMCdb 备份，且数据库访问、项目队列支持、具名人员及模型结果仍为未核验或未生成，没有提升状态。 |
| PCR-005 | section 6 `本地随机试验证据与当前状态`；第 7 节条件性试验方法首段 | 保留 EXIT-SEP 与 XBJ-SCAP 仅为阶段 III 潜在个体数据来源；现有材料仍明确为衍生报告，不能替代授权、原始 CRF/SAP、随机化、中心、访视时序和生存/住院/出院语义核验。原样保留两试验样本、缺失和字段可用数字。 |
| PCR-006 | section 5 固定执行顺序；第 7 节变量角色、观察性目标、模拟和外部评估 | 保留资源/G1→标签状态与医院分区→简单基线→已知真值模拟→至多一个复杂候选→两主两次任务→冻结→跨库评估→条件性试验的顺序；保留 Y_t/A_t/M_t 分离和 20 种子对齐 90%、自助保留 80%、外部符号 80%、状态对齐 0.70 与区间校准判定及删除、合并或限定解释后果。 |
| PCR-007 | section 5 `合取式最低成功定义`；第 7 节外部评估；第 11 节证伪与解释 | 阶段 II 仍由数据支持、已知真值恢复、两项主要任务的 Brier/多类别 Brier 与校准、泄漏清除、未更新外部性能、状态对齐和结构符号稳定共同决定；适配区更新另报且不能替代主要失败，阶段 III 不补足该合取结果。 |
| PCR-008 | 第 7 节 `两项主要临床任务的方案规定`、互斥状态表及相邻泄漏段 | 保留 72 小时/24 小时标本—抗菌药配对、基线 SOFA、滚动 24 小时成分、感染前 48 小时至后 24 小时窗口和首次可排序发病时刻；保留首次发病、重叠界标每次 ICU 停留总权重 1、延迟进入、竞争终止、同窗 A_t 与下一状态顺序、不能排序边排除，以及同窗治疗、未来测量频率、重复住院和结局驱动时间或阈值检查。两项任务、校准、严格适当评分和聚类不确定性均在表中。 |
| PCR-009 | structured abstract；section 6 当前证据表；section 12 贡献、近邻与 Claim-Support | 明确当前没有已生成模型、模拟、外部或试验新结果；贡献只在条件性整合、验证、基准和资源范围内。各模块已有先例为高置信，完整组合缺口为低至中等置信；未提出新算法或全球首次。 |
| PCR-010 | 第 7 节方法权威；第 11 节证伪与解释；第 14 节工作假设、11 个限制条目和运行风险 | 第 14 节一次覆盖访问、团队、G1、标签泄漏、可恢复性、非随机缺失与低重叠、未更新外部评估、时间、试验数据语义、共同指标计算、近邻检索与不支持主张；工作假设保留临床尺度到模拟参数映射及精确多类别校准估计量、置信区间和阈值记录。事件/参数筛选下限不替代经验有效样本量和模拟稳定性。两试验方向不一致或区间过宽的解释与不选亚组规则保留在方法及结果位置。 |
| PCR-011 | section 5 的阶段定义、时间节点及唯一依赖工作包；第 7 节条件性试验方法；sections 9–11 的单项功能记录；第 14 节时间限制 | 阶段 I–II 仍须在 24 个月内完成；阶段 III 共享前提为阶段 II 成功、个体数据可用和核心语义可核验。方法先给共享前提，再并列固定访视分数分析与独立临床状态分析，最后给核心语义不足时不开展新结局分析；一个分支的条件未上提为共享条件。标题和摘要只保留高层条件用途，后续结果不补足阶段 II。 |
| PCR-012 | 第 14 节 `限制与边界条件` 第 11 项；第 4、7、11 节的最小局部边界 | 完整且唯一的主张清单保留：观察性数据与预测不证明因果网络、治疗因果效应、反事实策略、机制、中介或控制；试验次要分析不验证未测动力学、转移边或整个模型；当前计划不是已验证模型、数字孪生、临床工具、药物平台或无条件推广依据，也不支持新算法或首次性。并保留 2026 指南对未获当地监管批准辖区使用血必净的谨慎立场。[4] |

Coverage: **12/12 protected items mapped with locator-level evidence; no protected commitment changed in status or strength**.

## Whole-dossier concordance

| Scientific role or check | One reader-facing name and first-use locator | Competing forms removed or reclassified | All-occurrence result |
|---|---|---|---|
| Frontmatter identity anchor | v003 与 v048 的 `identity_anchor` 五个同名字段 | 未以面向读者的名称统一替换 frontmatter 原值；正文编辑与逻辑身份字段分开处理 | 五字段逐值比较 5/5 相等；完整 mapping 相等；`identity_status: preserved` |
| Central object | “候选动态复杂系统模型”，section 1 `Positioning and contribution frame` | “候选动态系统表征”“候选全病程表示”“候选状态表示”“候选架构”“阶段 II 表征”不再指代研究对象；“患者状态及状态转移表示”只指模型组成 | 全篇对象名称一致；规定竞争形式正文 0 命中 |
| Primary question and task | “脓毒症全病程动态复杂系统模型的构建与跨数据库验证”，H1/Title | 条件性试验用途从标题和主任务层级移除 | H1 与 Title 完全一致；研究问题平行列出两项主要任务与跨库检验，只有一个高层条件用途 |
| Primary outcomes | “未来 12 小时首次发病累积发生风险”与“第 7 日有利状态占用概率”，structured abstract `Approach` | 首次发病预测、状态诊断和技术分支不再混为一个结局 | 方案表、证据链、必需分析和计划产物使用相同两项主要结局；数值与时间窗一致 |
| Contribution | “条件性的证据整合、跨数据库验证、基准与可复用资源”，section 1 positioning | 单项算法新颖性、首次性和条件试验分析的平行贡献定位移除 | section 12 与 Claim-Support 使用相同范围及高/低至中等证据强度 |
| Data-support function | “观测数据可用性与支持审计（G1）”，section 6 | “可观测性审计”“系统可观测性”和裸 G1 分开处理；状态空间可观测性仅作为被排除的不同概念解释一次 | 首次定义在所有正文 G1 之前；后续均指访问、事件/转移、时间戳、单位、密度、医院和接口支持 |
| Simulation roles | “相对已知生成机制的状态、转移、结构及错误关系检验”，section 7 | “绝对恢复”“假置信”“绝对门”“错误结构的高置信支持控制”全部删除 | 每个出现位置均说明对象、指标或已固定阈值和具体后果；禁用形式 0 命中 |
| External evaluation | “预先隔离且未用于模型选择的外部测试集”与“未更新外部性能评估”，section 7 | `untouched`、`zero-update`、“真正未触碰”等混合名称删除 | 测试集状态、主要评估、适配区重新校准、适配区观测层更新和全模型再开发在方法、证据链、结果解释及 Claim-Support 中一致 |
| Conditional trial outcome | “一维访视状态分数”及“预设独立次要临床状态分析”，section 7 | “观测投影”“投影可观测”“投影摘要”“随机化扰动”“death-ranked”“fallback”删除 | 输入、固定计算、输出、排序、随机组比较与独立关系在方法中完整；其他章节仅保留各自功能所需的高层信息 |
| Abbreviations | ICU、EHR、SOFA 首见于 section 3 Background；CRF/SAP、G1、RCT 首见于 section 6；MNAR/ESS、MCSE/ARI/MAE/FDR 首见于 section 7 | 低收益英文普通词展开为中文；正式数据库、试验名称、公式变量和参考文献题名保留 | 每个必要缩写首次出现均有中文科学功能；公式符号在同句定义；未发现未定义的核心科学缩写 |
| Limitation authority | “限制与边界条件”，section 14 | 证据链限制字段、完整禁止清单复述和第 14 节指针删除 | section 14 是完整限制、工作假设和不支持主张的唯一位置；全文限制位置指针 0 命中 |

## Deterministic and mechanical checks

- Structure: 15/15 required H2 headings in exact order; section 3 contains exactly the five required non-empty H3 headings in order; one substantive H1; H1 and `Title` exact match.
- Identity anchor: v003 and v048 frontmatter were parsed and compared field by field; `primary_research_question`, `primary_objective`, `study_object`, `core_data_or_evidence_base`, and `primary_unit_of_inference` are all verbatim-equal, and the complete mappings compare equal.
- Summary: one complete sentence with one terminal Chinese period; primary study precedes the one high-level conditional use.
- Lineage: dossier and delta each contain exactly three `based_on` mappings, namely v003 dossier, r096 writer brief, and r004 protected register; each mapping contains artifact ID, version, and path.
- Citations: body citations resolve to references 1–38; 38 numbered references are present; no cited or uncited reference-number discrepancy was found.
- Duplication: no duplicate substantive line of at least 50 characters; five evidence chains contain only Input, Method / analysis / processing, Output, and Supports functions.
- Forbidden compact forms: prose scan returned zero matches for the old object names, “可观测性审计”, “绝对门”, “恢复门”, “假置信”, “弃权”, `zero-update`, `untouched`, “观测投影”, “投影可观测”, “投影摘要”, “随机化扰动”, `death-ranked`, `fallback`, “门”, “降级”, “封印”, “防火墙”, “审计器” and “投影器”. The fixed contract H2 text is excluded from this prose-language count.
- Deterministic lint after the controlled anchor correction and again after dossier re-freeze: `OK` for plugin version `0.9.0-preview.3`, with zero errors and zero advisories.

Handoff status: `editorial_assessment_needed: true`; no narrative-readiness or scientific-evaluation verdict is asserted here.
