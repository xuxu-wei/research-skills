---
schema_version: research-idea-revision-delta.v1
plugin_version: 0.9.0-preview.3
artifact_id: revision-delta-I01-001-v003-to-v026
workflow_id: RID-SEPSIS-CSM-20260717-001
idea_id: I01-001
version_id: v003-to-v026
path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/accepted-v2/revision-delta-v003-to-v026.md
change_type: editorial_repair_delta
source_artifact:
  artifact_id: idea-dossier-I01-001-v003
  version: v003
  path: tests/idea-test-0.9.0-preview.1/0.9.0-preview.1/03_ideas/nodes/I01-001/dossiers/idea-dossier-v003.md
target_artifact:
  artifact_id: idea-dossier-I01-001-v026
  version: v026
  path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/accepted-v2/idea-dossier-v026.md
bound_inputs:
  - narrative-repair-plan-r014
  - language-assessment-I01-001-r035
  - protected-content-register-I01-001-v003-r002
independent_pass_status: not_assessed
---

# Revision delta: idea dossier v003 to v026

## Scope and status

本次变更以 v003 为唯一 dossier 来源，执行 narrative-repair-plan-r014、language-assessment-r035 和 protected-content-register-r002 所允许的集中编辑修订。修改类型限于 replace、define、move、split、merge、delete、reorder、add_bridge 和 consolidate；没有增加数据、方法、结果或证据，没有提高主张强度，也没有把计划写成已完成工作。

v026 仍须由未参与写作的独立实例重新进行叙事、语言和科学内容保真评估。本 delta 仅记录修改及其文本证据，不等于任何独立通过、晋级或最终评价。

## Narrative repair actions

### NRP-001 — split

- **New locator:** `Background, current state, gap, significance, and rationale > Background / Current state / Gap / Significance / Rationale`。
- **Operation:** 把原有混排段落拆成恰好五个非空且顺序固定的 H3，并增加从缺口到意义、再到设计依据的桥接。
- **Text-grounded evidence:** Gap 明确写为“一个描述以脓毒症为中心、从尚未发病到结局的患者状态及状态转移，并区分治疗行动与测量过程的候选复杂系统模型，能否在预设模拟中恢复可解释的不变量……”。Significance 独立回答价值：“闭合这一证据缺口，可把表面上较好的预测表现与可恢复、可跨数据库复现的状态信息区分开……”。Rationale 随后逐项连接双时间轴、变量角色分离、模拟恢复、按医院外部验证和模型—试验指标映射。
- **Acceptance test result:** 五个必需 H3 均非空且顺序正确；Significance 不以方法清单代替价值；Rationale 中每个主要设计选择均对应 Gap 中的未解问题。

### NRP-002 — replace

- **New locator:** `Title, summary, audience, and positioning > One-sentence complete-Idea summary`。
- **Operation:** 用一个主干清楚的完整句替换原 303 个中文字符的多层技术清单。
- **Text-grounded evidence:** “本研究拟在 24 个月内依据文献和专家知识构建一个描述脓毒症发病前、首次发病、发病后演化及结局的候选复杂系统模型，模型分别表示随时间变化的患者状态与状态转移、治疗行动和测量过程，并利用两个公共 ICU 数据库完成系统辨识和跨数据库验证；仅在核心验证成功且试验实际访视数据能够支持预定分析时，才分别使用随机对照试验的稀疏访视数据开展次要分析。”
- **Acceptance test result:** 该句独立交代研究对象、24 个月核心验证路线和条件性试验扩展；只含一个完整句和一个句号，不含算法分支、完整限制清单或未定义项目短称。

### NRP-003 — reorder

- **New locator:** `Structured abstract` 的五个固定项目。
- **Operation:** 按问题与缺口、目标与假设、总体设计、计划结果、贡献与影响的顺序重写，并把首次出现的非共享概念改为功能性描述。
- **Text-grounded evidence:** Background and gap 先说明“既有研究已分别覆盖……却仍缺少一条……连续证据路径”；Approach 先写“模型和分析方案在查看最终外部结果前确定，并在未参与开发或参数调整的外部测试集中评价”，再写条件性试验映射；Expected result 明示“这些均为拟生成产物，当前尚无模型、恢复、外部验证或试验新分析结果”。
- **Acceptance test result:** 只读五项即可复述问题、现状、缺口、意义、总体设计和计划贡献；实施阈值与分析分支留在方法及第 14 节。

### NRP-004 — consolidate

- **New locator:** `Feasibility, resources, risks, alternatives, and stop conditions` 全节，尤其 `Current resources and working assumptions`、`Complete risk, limitation and prespecified response matrix` 与 `Scientific interpretation boundaries`。
- **Operation:** 把完整资源限制、工作假设、风险触发、替代路线、停止后果和解释边界集中到第 14 节；其他章节只保留直接定义相邻科学对象或判定所必需的自足表述，没有增加跨节指针。
- **Text-grounded evidence:** 第 14 节一次性列出公共数据库与团队状态、G1、标签与泄漏、状态恢复、MNAR 与重叠、不更新参数的外部验证、全部时间节点、试验授权与语义、共同指标与映射、两项试验不一致、代表性研究检索不确定性，以及完整科学解释边界。其总结句明确：“任何后续试验结果都不能挽救阶段 II 失败，也不能绕过资源、恢复、主要任务或外部验证要求。”
- **Acceptance test result:** 第 14 节可独立提供完整限制、假设、风险、替代和停止后果；其他章节没有“见第 14 节”或同义指针，也没有重复完整禁止清单。

### NRP-005 — delete

- **New locator:** `Evidence chains` 下五条证据链。
- **Operation:** 删除五条链原有的 `Limits and failure conditions` 第五字段，保留血缘审计所需四字段。
- **Text-grounded evidence:** 每条链均按且仅按 `Input`、`Method / analysis / processing`、`Output`、`Supports` 排列；例如“按医院划分且不更新参数的跨数据库验证”链由四个字段完整记录输入、分析、输出和支持的目标。
- **Acceptance test result:** 共五条链，每条恰有四项；不存在 Limits、Limitations、failure conditions 或指向第 14 节的替代字段。

### NRP-006 — consolidate

- **New locator:** `Required analyses and evidence`。
- **Operation:** 把该节收缩为可检查的证据和记录，不再复制完整时间路线、阈值、算法步骤或风险后果。
- **Text-grounded evidence:** 八项阶段 II 清单分别以“访问与版本记录”“单元测试”“隔离和滞后证明”“模拟结果和处置记录”“敏感性结果”“评分与区间”“医院分配与访问日志”“合取结论表”等可核查名词收束；试验段只要求授权、语义、共同指标、映射、适用性结果和分析规范。
- **Acceptance test result:** 每一项对应可提交产物；Research content、Methods、Expected outputs 和第 14 节分别保留时间顺序、实施方法、可证伪产物与完整限制的独有功能。

## Language repair actions

### LA-R035-001 — replace

- **New locator:** `Title, summary, audience, and positioning > One-sentence complete-Idea summary`。
- **Operation and evidence:** 使用 NRP-002 所引完整句，以“研究对象与 24 个月目标—公共 ICU 系统辨识与跨数据库验证—条件满足后的试验次要分析”为唯一信息顺序。
- **Acceptance test result:** 一次阅读可区分核心研究与条件性扩展，不依赖后文定义。

### LA-R035-002 — define / replace

- **New locators:** `Structured abstract > Approach`、`Gap`、`Rationale`、`Primary research question` 与 `Research design and methods > Conditional mapping to trial observations and independent clinical-state analysis`。
- **Operation:** 不再用“观测投影”词根混合映射、输出和一致程度，分别使用“模型—试验指标映射”“由实际访视指标计算的一维观测摘要”“观测摘要与阶段 II 状态表示的一致程度及误差标准”。
- **Text-grounded evidence:** 方法首先解释“该操作把阶段 II 状态模型与试验实际测得的共同生理指标连接起来”，随后分别定义“P_state=V_1'X”为阶段 II 状态的一维参照分数，“P_obs=D_1^(-1)U_1'(Z_C−a_C)”为由实际访视指标计算的一维观测摘要；下一段独立列出相关、误差与校准标准。
- **Acceptance test result:** 映射、输出和一致程度三种功能一一对应，不再由同一紧缩词承担。

### LA-R035-003 — replace

- **New locators:** Structured abstract、第三节五个 H3、Research content、Key techniques、Expected outputs。
- **Operation:** 把项目治理词改为具体科学动作、预设标准和未满足标准后的分析后果。
- **Text-grounded evidence:** Approach 直接写明复杂候选须达到模拟恢复标准、在零边或独立状态情景下控制虚假关系发现，并在模型错设情景中检验错误模型是否被高置信接受以及能否触发失配或弃权；外部测试写为“未参与开发或参数调整的外部测试集”；变量分类写为“变量使用规则”；医院隔离和简单模型替代也均按科学动作直接陈述。G1 在 `Current state` 首次定义为“双数据库可观测性与样本支持审计”。
- **Acceptance test result:** 每处都直接写出科学动作、判定依据或后果，不要求读者先学习状态机隐喻。

### LA-R035-004 — replace

- **New locator:** 文档标题、Title 字段及 Objective 4。
- **Operation and evidence:** 标题改为“脓毒症发病前至结局的患者状态与转移：候选复杂系统模型的构建、跨数据库验证，以及仅在预设条件满足时使用随机试验的稀疏访视数据开展的次要分析”；Objective 4 写为“在预设条件满足时开展随机试验次要分析”。
- **Acceptance test result:** “预设条件满足”修饰是否开展，“随机试验”限定数据来源，“稀疏”只修饰访视数据，“次要”只修饰分析。

### LA-R035-005 — define / replace

- **New locators:** Research content、Data、Methods、Evidence chains 与 Contribution。
- **Operation:** 统一使用“可复用的基准数据与分析资源”“严格适当评分规则（proper scoring rule，即如实报告预测概率时使期望评分最优的规则）”“试验特异的独立次要临床状态分析”“全体随机化受试者分析集”等功能描述；D7/D8 首次作为“试验规定访视”出现并保持其相对随机化或首剂的时间待核验。
- **Text-grounded evidence:** 独立临床状态首次完整定义为“死亡者置于最差等级，访视时存活住院者按 SOFA 从高到低排序，活着出院者置于最有利等级”；EXIT-SEP 与 XBJ-SCAP 表格分别区分全部随机化分析、完整结局子集、mITT 与各敏感性人群。
- **Acceptance test result:** 未定义的 fallback、projection-pass、fidelity、death-ranked SOFA 和 trial-specific 英文短称不再承担正文核心概念；保留的英文统计或分析集术语均由中文功能说明限定。

### LA-R035-006 — consolidate / delete

- **New locator:** `Feasibility, resources, risks, alternatives, and stop conditions > Scientific interpretation boundaries`。
- **Operation:** 把因果、机制、中介、控制、数字孪生、整个系统模型和临床推广边界完整保留一次；从标题、摘要、核心假设、证据链、解释矩阵和定位表删除成组副本。
- **Text-grounded evidence:** 权威文本为“观察性公共 ICU 数据和预测表现不能直接支持真实因果网络、治疗因果效应、反事实治疗策略、机制、中介、控制或数字孪生主张……条件性随机试验次要分析……不能验证未测潜在动力学、状态转移边、中介、整个阶段 II 系统模型或个体控制。”其他章节只在定义局部分析对象时保留必要的单句区别，例如独立 SOFA 结局“与阶段 II 状态表征没有映射关系”。
- **Acceptance test result:** 每项独特边界完整存在且强度不变；全文没有相同完整禁止清单的副本，也没有新增跨章节指针。

### LA-R035-007 — define

- **New locator:** `Research question, objectives, and core hypothesis > Objectives > Objective 1`。
- **Operation and evidence:** 首次写为“重复设定的动态预测时点（landmark）风险集”，其后才使用 landmark；方法表同时明确每 12 小时设点、历史窗和预测窗。
- **Acceptance test result:** 首次出现即可判断 landmark 是预测时点，而非结局或时间窗。

### LA-R035-008 — replace

- **New locators:** `Current state`、`Representative related-study comparison` 及其正文。
- **Operation and evidence:** 用“与本研究最接近的既有研究”和“代表性相关研究比较”替代“最近近邻”“verified representative neighbor”和项目短称；仅固定 H2 合同与参考文献题名保留原机器或来源表达。
- **Acceptance test result:** 读者无需理解内部检索标签即可知道该部分在比较既有研究。

### LA-R035-009 — split roles / replace

- **New locators:** `Hospital-primary cross-database validation`、相关 Evidence chain、Interpretation matrix、Contribution 与第 14 节外部验证风险条目。
- **Operation:** 把四种角色逐句分开为“不更新模型参数的外部验证”“使用预留适配集重新校准”“只使用预留适配集更新观测模型”“在目标数据库完整重新拟合或重新开发模型”。
- **Text-grounded evidence:** 方法明确写出：“第一，不更新模型参数的外部验证（zero-update validation），这是主要跨数据库验证；第二，只使用预留适配集重新校准……；第三，只使用预留适配集更新观测模型……；第四，在目标数据库上完整重新拟合或重新开发模型，此项属于模型更新或再开发，不属于外部验证。”
- **Acceptance test result:** 每个实例仅属于四种角色之一；除来源题名和第一次括注外，不以“运输”词根替代不同操作。

## Protected-content preservation matrix

### PCR-001 — retained_same_meaning

- **New locators:** YAML `identity_anchor`；`Primary research question`；`One-sentence complete-Idea summary`。
- **Text-grounded evidence:** identity anchor 五字段原义保持不变；研究问题明确覆盖“发病前、首次发病、发病后状态演化及恢复、持续恶化、器官衰竭、活着出 ICU 或死亡结局”。全文没有把核心改成普通已发病预后或泛 ICU 风险分层。

### PCR-002 — retained_same_meaning

- **New locators:** YAML `identity_anchor.primary_objective`；一句话摘要；`Twenty-four-month minimum and dated criteria`；Positioning。
- **Text-grounded evidence:** 摘要保留“在 24 个月内依据文献和专家知识构建……并利用两个公共 ICU 数据库完成系统辨识和跨数据库验证”；Positioning 明示“主要交付面向一篇或多篇高水平论文及可核查的科学证据，而非单一预测工具”。

### PCR-003 — retained_same_meaning

- **New locators:** YAML `study_object` 与 `primary_unit_of_inference`；`Objective and hypothesis`；`Observational target, anchoring, missingness and abstention`。
- **Text-grounded evidence:** 推断单位仍是“患者—时间状态及状态转移”，并在 protocol 的 Uncertainty 行保留患者层和医院层 bootstrap；研究对象仍含可比较的未发病风险时段和发病后轨迹。

### PCR-004 — retained_same_status

- **New locators:** `Current evidence and prospective requirements`；`Public ICU database roles and G1 audit`；第 14 节 `Current resources and working assumptions`。
- **Text-grounded evidence:** MIMIC-IV 与 eICU-CRD 仍为主数据库，HiRID 或 AmsterdamUMCdb 仍是月 0–3 预指定且须同等审计的备份。文本明确区分“已核验”的数据库存在与版本，以及“未核验”的访问凭证、DUA、提取、人员承诺和“尚未生成”的队列及模型结果。

### PCR-005 — retained_same_status

- **New locators:** `Current evidence and prospective requirements`；`Local randomized-trial evidence and present status`；第 14 节资源现状与试验风险条目。
- **Text-grounded evidence:** EXIT-SEP 与 XBJ-SCAP 只作为条件性阶段 III 的潜在个体数据来源；本地报告仍被称为项目衍生证据，且明确“不能代替个体数据分析授权、原始 CRF/SAP、随机化和分析集、中心或分层因素……语义核验”。

### PCR-006 — retained_same_meaning

- **New locators:** `Work packages and minimum route`；`Observational target, anchoring, missingness and abstention`；`Prespecified simulation and semi-synthetic recovery assessment`；第 14 节状态恢复风险条目。
- **Text-grounded evidence:** 设计顺序完整保留为资源与 G1、标签/状态/医院划分、简单基线、绝对模拟恢复，以及在零边或独立状态与模型错设情景中评价虚假关系、错误高置信、失配和弃权；随后依次是至多一个复杂候选、两项主要任务和两项次要诊断、开发方案确定、不更新参数的外部测试，最后才考虑条件性试验分析。Y_t、A_t 和 M_t 仍分别定义。关键规则明确写为：“若预设模拟恢复标准未达到、20 个随机种子的对齐率<90%、bootstrap 保留率<80%、外部符号一致率<80%、状态对齐<0.70 或区间校准不合格，则删除或合并……或明确标为数据库或照护政策特异；较好的预测表现不豁免这些判定。”

### PCR-007 — retained_same_meaning

- **New locators:** `Conjunctive minimum success definition`；`Hospital-primary cross-database validation`；第 14 节外部验证风险条目。
- **Text-grounded evidence:** 阶段 II 成功仍由数据库支持、模拟恢复、两项主要任务的 Brier 或多类别 Brier、校准、泄漏清零、不更新参数外部结果、状态对齐≥0.70 和预设结构符号一致率≥0.80 合取决定。方法把不更新参数、重新校准、只更新观测模型和完整重新开发分开；第 14 节明示“有限更新或完整重新开发后的成功不能替代不更新参数外部验证的失败，也不能补足阶段 II 的合取成功”。

### PCR-008 — retained_same_meaning

- **New locators:** `Protocol specifications for the two primary clinical tasks`；`Mutually exclusive post-onset state/event system`。
- **Text-grounded evidence:** 两项主要任务、事件时间和信息可用时间、首次发病风险集、延迟进入、互斥状态、竞争终止、当时可用特征、评分与校准、患者和医院聚类均逐项保留。完整协议仍写明：标本先采时抗菌药在其后 72 小时内、抗菌药先给时标本在其后 24 小时内；无慢性器官障碍记录者 baseline SOFA=0，有记录者取入 ICU 前 24 小时最低可计算 SOFA；成分滚动 24 小时取最差，SOFA 增加≥2 须在感染前 48 小时至后 24 小时，首次可排序满足时刻为发病；只分析首次发病且同一次住院重叠预测时点总权重为 1；[t,t+12h) 新治疗定义 A_t，下一边界实测生理定义下一状态，同一时间戳无法排序者不用于该边。泄漏审计仍逐项检查同一时间窗治疗、未来测量频率、重复患者或住院和结局决定的时间网格或阈值。

### PCR-009 — retained_same_strength

- **New locators:** `Structured abstract > Expected result`；Positioning；`Contribution and evidence ladder`；`Representative related-study comparison`。
- **Text-grounded evidence:** 摘要明示“这些均为拟生成产物，当前尚无模型、恢复、外部验证或试验新分析结果”。贡献限于条件性的证据整合、跨数据库验证和可复用基准资源；相关研究段保持“各单项模块已有先例”为高置信，完整组合缺口为低至中等置信，并写明“不是新算法或全球首次”。

### PCR-010 — retained_once_at_authority_location

- **New locator:** 第 14 节三个 H3，尤其 `Complete risk, limitation and prespecified response matrix`。
- **Text-grounded evidence:** 第 14 节完整覆盖资源与访问、人员承诺、G1、标签与泄漏、状态与转移恢复、零边情景中的虚假关系、错设情景中的错误高置信与弃权、MNAR 与低重叠、不更新参数的外部验证、时间节点、试验数据和语义、共同生理指标与映射、文献检索不确定性及每个失败后的替代或停止后果。两项试验规则逐字实质保留为：“EXIT-SEP 与 XBJ-SCAP 的效应方向不一致，或任一关键区间过宽而不能排除实质不同的解释”时，只能分别报告“无一致支持”或“跨试验场景适用性有限”；“不选择亚组、符合方案集、sepsis-like 人群或 strict-overlap 人群来挽救总体结论”。其他章节不重复该完整限制清单。

### PCR-011 — retained_once_at_authority_location

- **New locator:** 第 14 节 `Scientific interpretation boundaries` 末段。
- **Text-grounded evidence:** “阶段 I–II 必须在 24 个月内完成……阶段 III 位于最低交付之外，只能在阶段 II 成功且相应试验数据、语义和模型—试验指标映射满足预设条件后开展；任何后续试验结果都不能挽救阶段 II 失败，也不能绕过资源、恢复、主要任务或外部验证要求。”

### PCR-012 — retained_same_boundary

- **New locator:** 第 14 节 `Scientific interpretation boundaries`。
- **Text-grounded evidence:** 观察性数据与预测表现对真实因果网络、治疗因果效应、反事实策略、机制、中介、控制和数字孪生的边界完整保留；条件性试验分析对未测潜在动力学、状态转移边、中介、整个阶段 II 系统模型和个体控制的边界完整保留；当前计划仍不得写成已验证模型、临床决策工具、药物平台或无条件国际临床推广依据。

## Replacement self-check

| Check | Revised locator and evidence | Result |
|---|---|---|
| 标题直接命名研究对象和动作 | H1 与 Title 均写为“脓毒症发病前至结局的患者状态与转移：候选复杂系统模型的构建、跨数据库验证，以及仅在预设条件满足时使用随机试验的稀疏访视数据开展的次要分析”；claim-support 第一行同步为“脓毒症发病前至结局的患者状态与转移” | 研究对象、模型动作、跨数据库验证、条件、数据属格和次要分析的修饰关系均唯一 |
| 一句话摘要首次定义模型所表示的对象 | 摘要写明模型“分别表示随时间变化的患者状态与状态转移、治疗行动和测量过程”，随后才说明系统辨识、跨数据库验证和条件性试验扩展 | 一个完整句、一个中文句号；无需依赖总括短称 |
| 零边与独立状态情景 | Approach 和模拟表直接写明“控制虚假关系发现”，表格写“任一虚假关系的 95% 区间排除 0 的重复比例≤0.05” | 科学对象与数值标准直接可读 |
| 模型错设情景 | Approach 直接写明检验错误模型是否被高置信接受以及能否触发失配或弃权；表格写“≥80% 重复触发失配或弃权；错误结构被高置信接受的比例≤0.05” | 错误高置信、失配和弃权三项功能分开 |
| Compact-label search | 对 v026 reader prose 与本 delta 搜索三项已拒绝的模拟压缩标签及旧总括标题短语 | 0 occurrences |
| 科学内容保护 | 对齐率 90%、bootstrap 保留率 80%、外部符号一致率 80%、状态对齐 0.70、区间校准触发，试验方向不一致或区间过宽的解释、不得选择亚组挽救及阶段 III 不得挽救阶段 II 均仍在第 14 节 | retained |

## Mechanical completion record

- NRP actions covered: NRP-001 through NRP-006（6/6）。
- Language findings covered: LA-R035-001 through LA-R035-009（9/9）。
- Protected items mapped: PCR-001 through PCR-012（12/12）。
- Dossier structure: 15 required H2 retained; the third H2 contains exactly five nonempty ordered H3; Evidence chains contains five chains with exactly four fields each.
- Lineage: source v003 and target v026 are bound by logical artifact identifiers, versions and paths.
- Evaluation status: no narrative, language, preservation or idea-evaluator decision is claimed by this writer output.
