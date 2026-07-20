---
schema_version: research-idea-revision-delta.v1
plugin_version: 0.9.0-preview.3
artifact_id: revision-delta-I01-001-v003-to-v024
workflow_id: RID-SEPSIS-CSM-20260717-001
change_type: editorial_repair_delta
source:
  artifact_id: idea-dossier-I01-001-v003
  version: v003
  path: tests/idea-test-0.9.0-preview.1/0.9.0-preview.1/03_ideas/nodes/I01-001/dossiers/idea-dossier-v003.md
target:
  artifact_id: idea-dossier-I01-001-v024
  version: v024
  path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/final/idea-dossier-v024.md
---

# Editorial revision delta: v003 to v024

本次修改是从 v003 直接完成的一轮集中叙事与语言修订。科学问题、研究对象、数据状态、方法参数、证据强度、关键限制和条件性阶段关系均按 protected-content register 保留；未新增数据、方法、结果或外部证据。

## Narrative repair actions

### NRP-001

- **Operation:** split and reorder
- **v024 locator:** “Background, current state, gap, significance, and rationale”下的五个 H3：Background、Current state、Gap、Significance、Rationale。
- **Revision evidence:** 五个子节按要求依次出现且各自非空。Gap 直接写明“当前证据尚不能回答”全病程贯通、模拟恢复、外部稳定和试验观测联系四类问题；Significance 以“解决这一缺口有三方面意义”分别说明结构解释、跨库可重复性和后续研究推进价值；Rationale 以“设计选择逐项回应上述缺口”连接双时钟、三类过程分离、用于固定状态尺度的共同生理测量、模拟恢复、医院层外部检验，以及从试验实际访视测量计算一维分数的条件性分析。
- **Acceptance-test evidence:** Background 只建立脓毒症时间演化与标签问题；Current state 只概括数据和邻近研究；Gap 回答现有证据不能回答什么；Significance 回答为何重要；Rationale 回答为何采用相应设计，没有以方法清单代替意义。

### NRP-002

- **Operation:** replace
- **v024 locator:** “Title, summary, audience, and positioning” > “One-sentence complete-Idea summary”。
- **Revision evidence:** 摘要重写为“本研究拟依据文献和专家知识构建一个用于描述脓毒症发病前、首次发病、发病后演化直至恢复、持续恶化、器官衰竭、出 ICU 或死亡的复杂系统模型，以随时间变化的患者状态及其转移为核心，区分治疗行动与测量过程并量化不确定性，在 24 个月内使用两个公共 ICU 数据库完成系统辨识和跨数据库验证，并只在主验证成功且相应试验资料适用时分别开展随机对照试验次要分析。”
- **Acceptance-test evidence:** 该字段只有一个句号结句，主干依次为患者状态与转移、24 个月双数据库主验证和条件性分试验次要分析；数据库或试验专名、访问审计、具体分数算法、失败分支和完整限制均不在该句。

### NRP-003

- **Operation:** reorder and define
- **v024 locator:** “Structured abstract”的 Background and gap、Objective and hypothesis、Approach、Expected result、Contribution and impact。
- **Revision evidence:** Background and gap 先写“仍缺少一条经同一协议检验的证据链”，并说明其对跨库解释和后续干预研究的意义；Objective 同句定义阶段 I、II 和条件性阶段 III，并解释共同生理指标用于固定状态尺度、预测实测指标和跨库对齐；Approach 说明如何按阶段 II 已确定的状态—测量关系从试验实际访视指标计算一维分数，以及如何检验状态信息保留和实测指标重建；Expected result 明示“这些是拟生成的产物，而非现有验证结果”；Contribution 以可重复性和可证伪价值为主。
- **Acceptance-test evidence:** 五项按问题与意义、目标、总体设计、计划结果和贡献展开；必要专门概念在首次出现处得到定义，摘要不包含完整实施清单。

### NRP-004

- **Operation:** consolidate
- **v024 locator:** “Feasibility, resources, risks, alternatives, and stop conditions” > “假设、限制与对应处理”，L1–L13。
- **Revision evidence:** L1–L13 分别集中记录访问与人员、G1 支持、标签与泄漏、识别与模拟、MNAR 与行动重叠、外部隔离与运输、试验资料与语义、共同生理测量与访视一维分数、试验稀疏性与异质性、时间与阶段依赖、最接近工作、解释与应用边界及研究身份。每项均拆为“当前状态/限制”“核验或触发条件”“处理”短段，不再把多组限定压入单个表格单元。
- **Acceptance-test evidence:** 第 14 个 H2 单独阅读即可获得全部关键假设、限制、风险、替代方案和停止范围；其他章节不再保留成组的完整限制清单，也没有写入跨章节指针。方法部分只保留直接定义估计对象或分支所必需的局部条件。

### NRP-005

- **Operation:** delete
- **v024 locator:** “Evidence chains”下的五条证据链。
- **Revision evidence:** 每条链只保留 Input、Method / analysis / processing、Output 和 Supports 四个字段。例如“可用时间、风险集与互斥病程”链依次给出 Sepsis-3 与时间数据、双时钟与互斥状态处理、两类队列和泄漏报告、以及对全病程边界的支持；其余四链采用相同四字段结构。
- **Acceptance-test evidence:** 五条链均没有第五个限制或失败字段，也没有用指向第 14 节的文字替代被删除字段；原字段的独有科学限制分别落在 L2–L12。

### NRP-006

- **Operation:** consolidate
- **v024 locator:** “Required analyses and evidence”。
- **Revision evidence:** 阶段 II 部分只列八类可核验交付；第 7 项为“医院分区、跨分区患者排除、结局前特征比较、连通分量敏感性、访问权限、完整文件清单，以及不作更新和有限更新的独立标识”，第 8 项为阶段 II 合取结论表。条件性阶段 III 的独立段只列授权、语义、共同变量、R0/R1、映射、分析规则和输出记录。
- **Acceptance-test evidence:** 该节每项均对应一个可检查产物；月度路线留在 Research content，实施参数留在 Methods，失败判据与科学输出留在 Expected outputs，完整限制留在第 14 个 H2。

## Blocking language findings

### LA-R027-001

- **Operation:** replace
- **v024 locator:** H1 与 “Title”字段。
- **Revision evidence:** 标题改为“脓毒症全病程患者状态与状态转移的复杂系统模型构建和跨数据库验证，以及条件性随机对照试验次要分析”。
- **Acceptance-test evidence:** 标题直接给出患者状态与状态转移、复杂系统模型构建、跨数据库验证和条件性试验次要分析；不再以未定义的总括短称为语义中心，也不存在“稀疏”误附到随机对照试验的问题。

### LA-R027-002

- **Operation:** replace, define, and standardize
- **v024 locator:** H1；一句话摘要；Primary research question；Objectives。
- **Revision evidence:** 标题和摘要先以自然中文说明“患者状态与状态转移的复杂系统模型”；摘要进一步写明“以随时间变化的患者状态及其转移为核心，区分治疗行动与测量过程并量化不确定性”。技术章节才使用“候选结构”“状态—测量关系”等具体名称。
- **Acceptance-test evidence:** 读者无需先理解“候选动态系统表征”即可说明研究对象、三类过程及候选性质；全文不再用“表征/表示”交替指称同一中央对象。

### LA-R027-003

- **Operation:** define and reorder
- **v024 locator:** Structured abstract > Objective and hypothesis；Research content and work packages。
- **Revision evidence:** 首次出现时写明“把依据文献和专家知识构建包含反馈、时滞、非线性、未测量因素及观测过程的候选复杂系统结构称为阶段 I，把使用公共 ICU 数据进行系统辨识、跨数据库验证和全过程状态表征称为阶段 II，二者均在 24 个月内完成；把 24 个月后可能开展的随机试验次要再分析称为条件性阶段 III”。
- **Acceptance-test evidence:** 同一位置给出每个阶段的内容、24 个月边界和阶段 III 的后置关系。

### LA-R027-004

- **Operation:** replace
- **v024 locator:** Structured abstract > Approach；Rationale；“Simulation recovery and false-structure control”。
- **Revision evidence:** 项目化简称统一改为“按预设数值阈值进行的模拟恢复与伪结构控制检验”；方法表逐项说明状态、转移、符号或滞后、边检测、零边伪结构、错设下伪确信与概率校准的判定对象和数值标准。
- **Acceptance-test evidence:** 首次表述已说明恢复对象、受控错误和预设数值判定，不再使用“绝对恢复门”或“假置信门”。

### LA-R027-005

- **Operation:** define, replace, and split
- **v024 locator:** Rationale；“条件性试验访视分数与独立临床状态分析” > “按阶段 II 已确定关系计算访视一维分数”、R1、“一维访视分数符合预设要求后的分析”。
- **Revision evidence:** Rationale 首次写明“使用阶段 II 已确定的状态—测量关系，从随机试验实际访视指标计算一维分数”，随后说明在未用于开发的公共 ICU 数据中检验状态信息保留和实测指标重建。方法把 P_state 定义为阶段 II 患者状态的一维参照分数，把 P_obs 定义为由试验实际访视测量按阶段 II 已确定关系计算的一维分数；合格后的输出明确为包含死亡、在院分数和活着出院三个层级的访视状态排序摘要。
- **Acceptance-test evidence:** 读者首次接触该分析时即可识别输入、计算关系、检验对象和组间比较对象；正文不再使用“观测变量投影”“投影状态摘要”“冻结观测投影门”或“投影忠实度”。

### LA-R027-006

- **Operation:** define and replace
- **v024 locator:** “预先规定的独立临床状态分析”以及 EXIT-SEP/XBJ-SCAP 特异规则和计划产物。
- **Revision evidence:** 首次完整定义为“死亡者为最差层，访视时存活在院者按 SOFA 从高到低排序，访视前活着出院者为最有利层；下文称‘独立的死亡分层 SOFA 再分析’”。
- **Acceptance-test evidence:** 三个排序层级出现在短称之前；后文只用该中文短称或“独立临床状态分析”，不使用 death-ranked 或 fallback。

### LA-R027-007

- **Operation:** define
- **v024 locator:** Research content and work packages > “24 个月最低交付与时间节点”，月 4–6 行；Data > 公共 ICU 数据库角色与 G1 子节。
- **Revision evidence:** G1 首次出现为“双数据库可观测性与数据支持审计（G1）”，并在同一行列出标签、双时钟、多状态、医院拆分、共同模块、时间网格和复杂度。
- **Acceptance-test evidence:** 其后每个 G1 均唯一回指同一审计，没有未定义的首次用法。

### LA-R027-008

- **Operation:** replace and define
- **v024 locator:** Research design and methods > “试验语义与共同生理测量合格性检验（R0）”与“测量一致性、校准、状态信息保留与重建检验（R1）”。
- **Revision evidence:** R0 按所需材料、语义核验、测量资格、角色排除、最低支持和预设分支列项；R1 按 eICU 状态信息保留、分数与实测指标重建、治疗标签遮蔽支持度和预设分支列项。
- **Acceptance-test evidence:** 仅看两个标题即可区分试验语义/共同生理测量与状态信息保留/实测指标重建，后文 R0/R1 均唯一回指该科学名称。

### LA-R027-009

- **Operation:** replace and split content across sections
- **v024 locator:** 一句话摘要；Research design and methods 的 RCT 子节；第 14 个 H2。
- **Revision evidence:** 一句话摘要只保留患者状态与转移、两个公共 ICU 数据库、全病程、文献/专家知识、不确定性、24 个月主验证路径和条件性分试验角色；数据库和试验专名、R0/R1、分数算法、三层排序、缺失与多重性均后置到正文；完整边界保留在 L7–L12。
- **Acceptance-test evidence:** 摘要只有一个句号结句，且可独立回答研究什么、如何验证和试验分析为何是条件性的。

### LA-R027-010

- **Operation:** split and consolidate
- **v024 locator:** R0 六组项目；访视一维分数四步计算；R1 四组项目；共同缺失数据与推断规则；EXIT-SEP/XBJ-SCAP 特异规则；每项试验的分析前记录。
- **Revision evidence:** R0 将材料、语义、测量资格、角色排除、最低支持和分支分开；一维分数将标准化、参照分数、实际访视分数和方向/独立性分开；R1 将状态信息保留、实测指标重建、遮蔽支持和分支分开；共同缺失处理只定义一次；两个原有长表格单元改成两组试验特异列表；分析前记录按授权、访视语义、分数计算、估计规则和分析分支分列。
- **Acceptance-test evidence:** 原有阈值、来源、死亡/出院排序、缺失、中心、多重性和停止条件均有唯一清晰位置，每个列表项只承担一种核对功能。

### LA-R027-011

- **Operation:** define and standardize
- **v024 locator:** “两项主要临床任务的协议定义”；“观察性估计对象、尺度固定与低支持处理”；“模拟恢复与伪结构控制”；R1；共同缺失规则与两个试验特异列表；“次要状态表征诊断”。
- **Revision evidence:** 首次出现分别写为界标时点（landmark）、当时可用（as-of）、累积发生函数（CIF）、逆概率删失加权（IPCW）、精确率—召回率曲线下面积（AUPRC）、有效样本量（ESS）、Monte Carlo 标准误（MCSE）、调整兰德指数（ARI）、平均绝对误差（MAE）、错误发现率（FDR）、奇异值分解（SVD）、归一化平均绝对误差（NMAE）、多重插补（MI）、族错误率（FWER）、改良意向治疗分析（mITT）和连续秩概率评分（CRPS）。不作任何更新、适配区、最终测试区、完整重拟合、合并效应和仅预测均使用中文功能表达。
- **Acceptance-test evidence:** 每个跨学科缩写首次出现均附中文全称，后文用法一致；普通流程动作不再以裸露英文出现。

### LA-R027-012

- **Operation:** consolidate and delete
- **v024 locator:** “Feasibility, resources, risks, alternatives, and stop conditions” > L1–L13；Structured abstract；Core hypothesis；试验方法；Evidence chains。
- **Revision evidence:** 完整限制集中在 L1–L13，每项拆为限制或当前状态、核验或触发条件、对应处理。Structured abstract 只保留计划状态和证据顺序；Core hypothesis 只保留定义观察性估计对象所需的“治疗因果效应不是该核心假设的组成部分”；试验方法只保留直接决定三个分析分支的局部条件；五条 evidence chain 只有四个合同字段，没有限制清单。
- **Acceptance-test evidence:** 非因果、非控制、非数字孪生、试验稀疏性、阶段依赖和失败后果的完整版本各只在 L1–L13 出现一次；其他位置没有重复长清单或跨章节指针，保留的局部边界均直接决定相邻估计对象或分析分支。

### LA-R027-013

- **Operation:** replace, translate, and remove editorial language
- **v024 locator:** 正文非合同 H3 与表头；模拟方法；References 22–25 和 38；全篇普通流程表达。
- **Revision evidence:** 非合同小标题和表头改为自然中文，例如“24 个月最低交付与时间节点”“两项主要临床任务的协议定义”“可证伪判据与允许解释”。模拟方法把“不读取临床最终测试结果”改为“不查看临床最终测试结果”。References 22–25 统一为“材料类型—证据局限—纳入当前证据基础的用途”，例如第 22 条写明“项目内衍生质量控制报告……不替代原始 CRF/SAP 或独立同行评审；纳入当前证据基础仅用于描述衍生数据的访视覆盖与缺失状态”。
- **Acceptance-test evidence:** 正文不再使用“打开 test”“重救”“fallback”“death-ranked”等评审口令或口语式流程词；References 22–25 不含“本次修订”“本次 v024”“读取”“只读”或本地路径式叙述，中英文并列修饰关系明确。

## Protected-content disposition

### PCR-001 — identity and core question

- **v024 locator:** frontmatter identity_anchor；一句话摘要；Primary research question。
- **Item-level evidence:** 摘要明确覆盖“脓毒症发病前、首次发病、发病后演化直至恢复、持续恶化、器官衰竭、出 ICU 或死亡”，并把随时间变化的患者状态及其转移作为核心；Primary research question 分为全病程覆盖、模拟与跨数据库验证、条件性试验访视分析三个连续部分，没有改为普通预后或泛 ICU 风险模型。
- **Disposition:** retained_same_meaning

### PCR-002 — primary objective and deliverable direction

- **v024 locator:** Positioning and contribution frame；Structured abstract > Objective；Research content and work packages。
- **Item-level evidence:** 明示阶段 I–II 均在 24 个月内完成，阶段 I 依据文献和专家知识构建候选结构，阶段 II 使用公共 ICU 数据进行系统辨识、全过程表征和跨数据库验证；Positioning 写明“高水平论文”以及方法整合、验证基准和可复用资源，而非仅交付预测工具。
- **Disposition:** retained_same_meaning

### PCR-003 — study object and inference unit

- **v024 locator:** frontmatter study_object 与 primary_unit_of_inference；Primary research question；两项主要临床任务协议表。
- **Item-level evidence:** 保留可比较的发病前在险期和发病后轨迹；核心问题明确“患者—时间状态和状态转移”，协议同时保留患者层与医院层聚类区间。
- **Disposition:** retained_same_meaning

### PCR-004 — public data and resource status

- **v024 locator:** Data > “当前资源与证据状态”；“公共 ICU 数据库角色与双数据库可观测性和数据支持审计（G1）”；第 14 个 H2 的 L1、L2。
- **Item-level evidence:** MIMIC-IV 与 eICU-CRD 的存在和版本为“已核验”，访问、协议和提取为“未核验”，G1 结果与模型结果为“尚未生成”；HiRID 或 AmsterdamUMCdb 仍只是月 0–3 预先指定并同等审计的备份。
- **Disposition:** retained_same_status

### PCR-005 — conditional trial inputs

- **v024 locator:** Data > “本地 RCT 材料与当前证据状态”；第 14 个 H2 的 L7–L9。
- **Item-level evidence:** EXIT-SEP 与 XBJ-SCAP 仍只由项目内衍生材料描述；L7 明确这些材料不替代个体数据授权、原始病例报告表、统计分析计划、随机化、中心、访视与生存/住院语义核验。
- **Disposition:** retained_same_status

### PCR-006 — design sequence and interpretation constraints

- **v024 locator:** “工作包与最低研究顺序”；完整 Research design and methods。
- **Item-level evidence:** 最低顺序仍为资源/G1、标签/状态/医院拆分、简单基线、模拟恢复、至多一个复杂候选、两项主要任务和两项次要诊断、开发结果锁定、未用于开发的跨库检验、条件性试验分析；方法分别定义 Y_t、A_t 和 M_t，并把解释限制在由共同生理测量固定尺度、经对齐且稳定的量。
- **Disposition:** retained_same_meaning

### PCR-007 — conjunctive stage-II success

- **v024 locator:** “阶段 II 合取成功定义”；“以医院为主要单位的真正跨数据库验证”；第 14 个 H2 的 L6 与 L10。
- **Item-level evidence:** 五项合取仍包括双数据库支持、模拟恢复、两项主要任务的 Brier/校准数值、泄漏清零，以及未用于开发测试区的不作更新表现、状态对齐不低于 0.70 和符号一致率不低于 0.80；只在适配区学习的更新分开报告；L10 明确任何阶段 III 结果都不能补足阶段 II 失败。
- **Disposition:** retained_same_meaning

### PCR-008 — clocks, landmarks, ordering, leakage, and trial analysis

- **v024 locator:** “两项主要临床任务的协议定义”；“发病后互斥状态与事件系统”；“条件性试验访视分数与独立临床状态分析”。
- **Item-level evidence:** 协议完整保留标本与抗菌药 72/24 小时配对、基线 SOFA、滚动 24 小时成分、首次可排序发病、事件/可用双时钟、首次发病、延迟进入、每次住院重叠界标总权重为 1、[t,t+12h) 行动与下一边界状态排序及同时间戳边排除；泄漏审计逐项保留同时间格治疗、未来测量频率、重复住院和结局驱动变量/网格/阈值。RCT 方法完整保留 R0/R1、SVD 计算关系、全部数值阈值、死亡/出院排序、MI/delta/临界点、中心、Holm 家族、mITT 和分试验规则。
- **Disposition:** retained_same_meaning

### PCR-009 — planned status and claim strength

- **v024 locator:** Structured abstract > Expected result；Data 资源表；“贡献与证据层级”；“已核验的代表性最接近工作比较”；L11。
- **Item-level evidence:** Structured abstract 明示“拟生成的产物，而非现有验证结果”，资源表把模型与所有分析结果标为“尚未生成”；最接近工作段仅称有界检索在低至中等置信度下未识别完整组合，贡献定位为条件性整合、验证和基准或资源增量。
- **Disposition:** retained_same_strength

### PCR-010 — complete limitations, alternatives, and stop rules

- **v024 locator:** 第 14 个 H2 > L1–L13。
- **Item-level evidence:** L1 覆盖访问、人员与算力；L2 覆盖 G1；L3 覆盖标签与泄漏；L4 覆盖识别、模拟和未生成结果；L5 覆盖 MNAR 与低重叠；L6 覆盖外部隔离和运输；L7–L9 覆盖试验资料、语义、共同生理测量、访视一维分数、稀疏性与异质性；L10 覆盖时间和阶段依赖；L11 覆盖最接近工作；L12 覆盖科学解释；L13 覆盖研究身份。每项均有当前限制、核验或触发条件、有限替代及停止后果。
- **Disposition:** retained_once_at_authority_location

### PCR-011 — 24-month boundary and conditional stage III

- **v024 locator:** “24 个月最低交付与时间节点”；Structured abstract > Objective；第 14 个 H2 的 L10。
- **Item-level evidence:** “阶段 I–II 的全部最低交付在 24 个月内完成；条件性阶段 III 位于这一时间范围之后”；L10 进一步要求阶段 II 成功、试验资料/语义/访视一维分数计算条件满足，并写明“任何阶段 III 结果都不能补足阶段 II 的失败”。
- **Disposition:** retained_once_at_authority_location

### PCR-012 — unsupported claim classes

- **v024 locator:** 第 14 个 H2 的 L12；Core hypothesis and non-hypotheses 的局部估计对象定义。
- **Item-level evidence:** L12 完整保留观察性数据不识别真实因果网络、治疗因果效应、反事实策略、机制、中介、控制或数字孪生，随机试验次要分析不验证未测潜在动力学、转移边或整个系统模型，并禁止把当前计划写成已验证模型、临床决策工具、药物平台或临床效用证据。
- **Disposition:** retained_same_boundary

## Scope declaration

- Scientific facts added: none.
- Scientific facts removed: none.
- Claim strength increased: no.
- Planned work presented as completed: no.
- Critical limitations removed or weakened: no; all are itemized once in L1–L13.
- Identity change: none.
