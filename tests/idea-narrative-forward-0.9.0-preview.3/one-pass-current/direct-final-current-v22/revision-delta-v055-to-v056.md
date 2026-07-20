---
schema_version: research-idea-revision-delta.v1
plugin_version: 0.9.0-preview.3
artifact_id: revision-delta-I01-001-v055-to-v056
workflow_id: RID-SEPSIS-CSM-20260717-001
idea_id: I01-001
version_id: v055-to-v056
path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v22/revision-delta-v055-to-v056.md
source_artifact:
  artifact_id: idea-dossier-I01-001-v055
  version: v055
  path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v21/idea-dossier-v055.md
target_artifact:
  artifact_id: idea-dossier-I01-001-v056
  version: v056
  path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v22/idea-dossier-v056.md
writer_brief:
  artifact_id: editorial-repair-writer-brief-I01-001-r127
  version: r127
  path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v21/editorial-repair-writer-brief-r127.yaml
protected_content_register:
  register_id: protected-content-register-I01-001-v055-v007
  version: v007
  path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v21/protected-content-register-v007.yaml
source_skill: multi-path-idea-generator
created_round: 127
change_type: editorial_repair_delta
frozen: true
---

# v055 至 v056 修订差异

## 范围与合规结果

- 编排器冻结前合规检查：**PASS**。检查确认 NRP-001 与 NRP-002 已完整执行，五个身份锚点逐字符一致，PCR-001 至 PCR-064 全部保留，结构完整，未纳入的次要项目未被执行。
- 本次只执行 `NRP-001` 和 `NRP-002`。`NRP-003` 与 `LA-001` 至 `LA-006` 未执行，也不在下列修订映射中。
- v056 是一个完整 dossier，已在合规检查后由 `frozen: false` 改为 `frozen: true`；其后未再修改 dossier 正文。
- 科学身份、数据、方法、证据状态、阈值、公式、分支后果和主张强度均未新增或加强。

## NRP-001：条件性试验延伸的单一方法权威

### 执行动作与验收

| 项目 | v056 中的实际处理 | 文本证据与验收结果 |
|---|---|---|
| 唯一完整权威 | `Research design and methods > 试验观测映射和独立分析` | 共享前提、两试验分别授权和语义核验、试验特异共同生理锚点、外部忠实度、死亡—一维可观测代理—存活出院有序结局、独立 SOFA 端点、分层标准化概率指数、访视与分析集、缺失和界限、多重性及所有停止后果均完整保留。 |
| 主体路线 | 标题、摘要、背景—理由链不再展开条件性试验延伸；问题和目标仅保留从属问题身份 | 24 个月阶段 I–II 从资源审计、状态和模型、绝对恢复、两项主要任务到未触碰跨数据库检验连续展开；阶段 III 没有获得与阶段 II 相当的叙事权重。 |
| 分支边界 | 方法权威及第 11 节对应的最小后果和解释 | 观测映射失败只阻断死亡—代理—出院结局；独立 SOFA 条件仍可单独成立；核心语义不可核验时停止所有新访视结局。 |
| 阶段边界 | 里程碑、WP5、方法权威和第 14 节第 6 项 | EXIT-SEP 与 XBJ-SCAP 分开；阶段 III 位于 24 个月最低交付之后，不能计入、绕过、补足或修复阶段 II。 |

### 全出现位置清单

下表按一个连续段落、表格行或同一小节中的单一功能记为一个出现位置。保留在方法权威之外的每个读者文本出现位置只承担一个获准功能；机器身份字段和参考文献记录另行标明，不参与读者文本的局部功能判定。

| v055 来源出现位置 | v056 处置或准确位置 | 唯一功能 |
|---|---|---|
| frontmatter `identity_anchor.core_data_or_evidence_base` | 原样保留 | 机器身份字段；不属于读者文本功能判定 |
| Title, summary, audience, and positioning > one-sentence summary 中的条件性试验从句 | 删除 | — |
| Title, summary, audience, and positioning > positioning 中的从属延伸说明 | 删除 | — |
| Structured abstract > Background and gap 中的试验二次分析先例 | 删除 | — |
| Structured abstract > Approach 末尾的条件性试验从句 | 删除 | — |
| Background > Current state 中的试验二次分析先例 | 删除；先例比较只在第 12 节保留 | — |
| Background > Significance 中的后续干预研究和随机分配解释 | 删除 | — |
| Background > Rationale 中的试验延伸及其不能替代阶段 I–II 的说明 | 删除 | — |
| Primary research question | 原位置保留一句从属问题 | `primary_question_identity` |
| Objectives > objective 4 | 原位置保留一句从属目标及不计入阶段 II | `objective` |
| 24 个月最低交付与时间节点 > 开头对阶段 III 的重复说明 | 删除 | — |
| 24 个月最低交付与时间节点 > 24 月后里程碑行 | 原位置压缩为依赖、时间和不计入或补足阶段 II | `timing_dependency` |
| Conjunctive minimum success definition > 末句阶段 III 重复说明 | 删除 | — |
| Work packages and minimum route > WP5 | 原位置保留依赖、时间、分试验输出及不属于阶段 II | `work_package` |
| Work packages and minimum route > 最低顺序末端 | 原位置保留终端先后关系和不得用试验结果绕过失败步骤 | `work_package` |
| Current resource and result status > 本地衍生报告行 | 原位置保留来源性质和当前证据状态 | `current_factual_status` |
| Current resource and result status > 授权和原始语义行 | 原位置保留尚未核验事实 | `current_factual_status` |
| Current resource and result status > 共同生理锚点、单位和访视映射行 | 删除“两锚点”准入阈值的重复，只保留候选、单位缺口和待核验输入 | `current_factual_status` |
| Current resource and result status > 当前结果行 | 原位置保留尚无新试验分析结果 | `current_factual_status` |
| Local randomized-trial evidence status > EXIT-SEP 段落 | 原位置保留 1,817、1,760、395、57、SOFA 1,750/1,542/1,296 和乳酸 855 至 223 等登记事实及仍待核验事项 | `current_factual_status` |
| Local randomized-trial evidence status > XBJ-SCAP 段落 | 原位置保留 710、675、617、671、658、SOFA/WBC/CRP 和 28 日状态计数及字段缺口 | `current_factual_status` |
| Protocol locks > 发病后任务达标行中的“试验结果不能改变失败” | 删除 | — |
| Research design and methods > 试验观测映射和独立分析 | 原位置完整保留 | 唯一完整方法权威 |
| Key techniques > 试验观测映射接口 | 压缩为分试验输入及实现须生成的资格、参数、忠实度、结局和执行状态记录 | `implementation_record` |
| Key techniques > 不确定性与多重性中的试验插补和 Holm 重述 | 删除试验专属处理；该行只保留跨估计目标的一般实现记录 | — |
| Evidence chain: 有前置条件的随机试验次要分析 | 保留完整 Input、Method / analysis / processing、Output、Supports 四项；方法行仅称分试验核验并执行预设实际访视有序结局分析 | `evidence_chain` |
| Required analyses and evidence > 试验段落 | 压缩为授权、原始语义、试验特异资格和执行固定方法 | `method_eligibility` |
| Planned outputs > 第 5 项 | 原位置保留分试验结果或不开展新分析的原因记录 | `planned_output` |
| Falsification and stop criteria > 试验观测映射 | 原位置只保留映射失败的对象和独立 SOFA 可保留的后果 | `falsification_consequence` |
| Falsification and stop criteria > 试验核心语义 | 原位置只保留全部新访视结局停止、方向不一致或区间过宽的解释后果 | `falsification_consequence` |
| Interpretation matrix > 合格观测映射结果行 | 原位置保留结果特异的允许与禁止解释，不含构造或资格方法 | `interpretation` |
| Interpretation matrix > 独立 SOFA 结果行 | 原位置保留独立临床状态差异及其不能说明阶段 II 表征 | `interpretation` |
| Contribution and evidence ladder > 开头段落的试验延伸句 | 删除 | — |
| Contribution and evidence ladder > 从属试验证据行 | 删除技术要求清单，只保留分试验实际访视差异的主张强度和条件性范围 | `contribution_positioning` |
| Verified representative closest-work comparison > 随机试验次要分析行 | 原位置保留先例和主体研究成功后、按试验分开、从属于阶段 I–II 的差异 | `contribution_positioning` |
| Title and positioning claim-support table > 试验行 | 原位置保留从属主张、证据链、条件状态、分试验范围和非主要角色，不含分支方法 | `claim_audit` |
| Feasibility and resources > 当前结果句中的试验新分析 | 删除；当前事实只在第 6 节权威行保留 | — |
| Working assumptions > 试验主要估计目标行 | 保留分层标准化概率指数确认事项、具名统计负责人、截止点、受影响部分和未确认后果；公式与分支仍只在方法权威 | `assumption_governance` |
| Limitations > 第 6 项时间与交付边界 | 完整保留 | `limitation_authority` |
| Limitations > 第 7 项试验数据与语义 | 完整保留 | `limitation_authority` |
| Limitations > 第 8 项共同生理锚点与观测映射 | 完整保留，但没有展开第二套资格树 | `limitation_authority` |
| Limitations > 第 10 项监管适用范围 | 完整保留 | `limitation_authority` |
| Limitations > 第 11 项禁止主张中的试验边界 | 完整保留 | `limitation_authority` |
| Risks > 关键时间节点行中的“阶段 III 不改变状态” | 删除重复说明 | — |
| Risks > 试验个体数据或核心语义不可获得 | 原位置保留触发、原终点复现或数据审计响应，以及不开展新访视结局的后果 | `risk_response` |
| References > [17]、[18]、[21]–[25]、[28]、[37] | 原样保留 | 文献记录；不属于方法出现位置 |

## NRP-002：第 14 节作为完整限制条件的唯一权威

### 执行动作与验收

第 14 节 `Limitations and boundary conditions` 中的十一类限制条件完整保留且各出现一次：资源与访问；标签、时钟和信息泄漏；状态可恢复性和结构范围；非随机缺失和低行动重叠；跨数据库证据；时间和交付；试验数据和语义；共同生理锚点和观测映射；最接近工作不确定性；监管适用范围；完整禁止主张。其他位置只保留紧邻正向论证、方法资格、当前事实、证伪后果、结果解释或风险响应所不可缺少的最小自足文本。没有指向第 14 节的限制条件指针。

### 十一类限制条件的全出现位置清单

连续段落或同一表格行如具有同一处置和同一功能则合并为一个出现位置。第 14 节完整权威不属于“外部保留文本”；其余每个保留行只列一个获准功能。

| 类别 | v055 来源出现位置 | v056 处置或准确位置 | 唯一功能 |
|---:|---|---|---|
| 1 | one-sentence summary 中“须经访问与可观测性审计” | 删除 | — |
| 1 | 24 个月最低交付与时间节点 > 负责人签署句 | 拆为独立句并原意保留 | `current_factual_status` |
| 1 | 24 个月最低交付与时间节点 > 最终测试资料隔离句 | 拆为独立句并原意保留 | `method_eligibility` |
| 1 | Current resource and result status > 访问、审计、职责和当前结果各行 | 保留各行当前存在、未核验或未生成的事实；删除可在权威行之外省略的试验结果重复 | `current_factual_status` |
| 1 | Public intensive-care database roles and support audit | 保留数据库角色、访问和项目支持的执行门槛 | `method_eligibility` |
| 1 | Required analyses and evidence > 第 1、7 项 | 保留资源确认、权限和冻结记录要求 | `method_eligibility` |
| 1 | Feasibility and resources > 两段 | 保留数据库、人员和计算范围的当前状态 | `current_factual_status` |
| 1 | Risks > 数据库访问、团队职责、测试隔离行 | 保留每行的具体触发、响应和后果 | `risk_response` |
| 1 | Limitations > 第 1 项 | 完整保留一次 | 第 14 节完整权威 |
| 2 | Structured abstract > Background and gap；Background | 保留标签随配对、基线、观察窗和可用时刻改变这一问题理由 | `positive_reasoning` |
| 2 | Objectives > objective 1 | 保留双时钟和敏感标签这一研究目标 | `positive_reasoning` |
| 2 | 里程碑和合取成功定义中的泄漏条件 | 保留授权最终测试所需的时钟和泄漏门槛 | `method_eligibility` |
| 2 | Protocol locks；Variable roles | 保留事件/可用时钟、标签隔离和跨拆分规则 | `method_eligibility` |
| 2 | Evidence chain: 可用性时钟；Required analyses 第 2、3 项 | 保留执行与核查标签、时钟和隔离所需内容 | `method_eligibility` |
| 2 | Falsification > 时钟与信息泄漏 | 保留失败对象、触发及阻断最终外部测试的后果 | `falsification_consequence` |
| 2 | Limitations > 第 2 项 | 完整保留一次 | 第 14 节完整权威 |
| 3 | Structured abstract > Objective and hypothesis；Gap；Core hypothesis | 保留可恢复不变量及非因果系统解释这一正向科学问题边界 | `positive_reasoning` |
| 3 | 里程碑、合取成功定义和工作包中的恢复门槛 | 保留复杂候选能否进入后续检验的条件 | `method_eligibility` |
| 3 | Observational target；Absolute simulation and semi-synthetic recovery criteria | 保留锚定、允许重参数化、绝对恢复和失败动作 | `method_eligibility` |
| 3 | Key techniques；相关 Evidence chain；Required analyses | 保留恢复记录及复杂候选准入证据 | `method_eligibility` |
| 3 | Falsification > 绝对恢复 | 保留复杂候选不晋级及预测优势不能逆转的后果 | `falsification_consequence` |
| 3 | Interpretation matrix > 简单基线、模拟恢复和未支持状态/边各行 | 保留每种结果模式的限定解释 | `interpretation` |
| 3 | Contribution/evidence ladder 与 closest-work 中的候选表征定位 | 保留整合、验证和基准的支持范围 | `positive_reasoning` |
| 3 | Limitations > 第 3 项 | 完整保留一次 | 第 14 节完整权威 |
| 4 | Current state > 测量过程偏倚句 | 保留作为研究理由 | `positive_reasoning` |
| 4 | Observational target > 非随机缺失和行动支持 | 保留偏移、临界点、行动概率和有效样本量的分析资格 | `method_eligibility` |
| 4 | Key techniques、Evidence chains、Required analyses 中的缺失与行动核查 | 保留执行相应分析所需的记录和证据 | `method_eligibility` |
| 4 | Falsification > 非随机缺失与行动支持 | 保留敏感性范围、照护政策特异解释和不估计治疗作用的后果 | `falsification_consequence` |
| 4 | Limitations > 第 4 项 | 完整保留一次 | 第 14 节完整权威 |
| 5 | Current state；Gap；Significance；Rationale | 保留异质数据库、共同概念和跨数据库问题的正向理由 | `positive_reasoning` |
| 5 | 里程碑、合取成功定义和 WP4 | 保留未触碰测试、有限适配分离及支持门槛 | `method_eligibility` |
| 5 | Data > 数据库角色和支持审计 | 保留中心、接口和共同变量的当前状态与准入规则 | `current_factual_status` |
| 5 | Hospital-primary cross-database validation | 保留医院分区、跨分区患者、四种更新操作和失败后果 | `method_eligibility` |
| 5 | 跨数据库 Evidence chain；Required analyses | 保留冻结、权限、排除和分操作证据 | `method_eligibility` |
| 5 | Falsification > 外部结果 | 保留不更新外部检验失败及有限适配的解释后果 | `falsification_consequence` |
| 5 | Interpretation matrix > 外部检验和适配各行 | 保留结果特异的允许与禁止解释 | `interpretation` |
| 5 | Contribution、closest-work 和 claim-support 中的跨数据库定位 | 保留计划性验证和基准主张的支持范围 | `positive_reasoning` |
| 5 | Risks > 跨院患者支持和测试隔离 | 保留具体触发、备份或降级后果 | `risk_response` |
| 5 | Limitations > 第 5 项 | 完整保留一次 | 第 14 节完整权威 |
| 6 | Title、summary、objective 和研究问题中的 24 个月主体范围 | 保留主体研究身份和正向目标 | `positive_reasoning` |
| 6 | 时间节点、合取定义和工作包 | 删除重复阶段 III 说明；保留每个时间点直接决定执行资格的规则 | `method_eligibility` |
| 6 | Falsification > 时间 | 保留月 12、20、24 的对象特异后果 | `falsification_consequence` |
| 6 | Risks > 关键时间节点 | 删除“阶段 III 不改变状态”的重复；保留延误触发、响应和后果 | `risk_response` |
| 6 | Limitations > 第 6 项 | 完整保留一次 | 第 14 节完整权威 |
| 7 | summary、positioning、abstract、Background/Significance/Rationale 中的试验延伸或试验限制 | 删除 | — |
| 7 | Primary research question；objective 4 | 保留从属试验问题及不计入阶段 II 的最小边界 | `positive_reasoning` |
| 7 | Current resource and result status；Local randomized-trial evidence status | 保留授权、原始语义、计数、字段缺口和结果尚未生成的事实 | `current_factual_status` |
| 7 | 试验观测映射和独立分析 | 保留试验资格、分析和停止逻辑的完整科学方法 | `method_eligibility` |
| 7 | Key techniques；Evidence chain；Required analyses | 压缩为执行所需的输入、记录、核验和固定方法 | `method_eligibility` |
| 7 | Planned outputs > 第 5 项 | 保留结果或不分析原因记录的输出含义 | `interpretation` |
| 7 | Falsification > 两个试验条目 | 保留映射失败、语义失败、方向不一致和宽区间的对象特异后果 | `falsification_consequence` |
| 7 | Interpretation matrix > 两个试验结果行 | 保留各结果模式的允许与禁止解释 | `interpretation` |
| 7 | Contribution、closest-work 和 claim-support 的从属试验行 | 删除技术清单，只保留从属、分试验和条件性定位 | `positive_reasoning` |
| 7 | Feasibility and resources > 试验新结果状态 | 删除；当前事实已在第 6 节保留 | — |
| 7 | Risks > 试验授权或核心语义 | 保留触发、原终点复现/数据审计响应和不开展新分析的后果 | `risk_response` |
| 7 | Limitations > 第 7 项 | 完整保留一次 | 第 14 节完整权威 |
| 8 | Current resource and result status > 共同生理锚点、单位和映射行 | 删除准入阈值重复，只保留候选、单位和映射待核验事实 | `current_factual_status` |
| 8 | 试验观测映射和独立分析 | 保留锚点资格、映射、忠实度、有序结局和独立 SOFA 方法 | `method_eligibility` |
| 8 | Key techniques；Evidence chain；Required analyses | 压缩为输入、实现记录、资格核验和执行固定方法 | `method_eligibility` |
| 8 | Falsification > 试验观测映射 | 保留映射结局失败及独立 SOFA 不被抹除的后果 | `falsification_consequence` |
| 8 | Interpretation matrix > 两个试验结果行 | 保留结果特异的允许与禁止解释 | `interpretation` |
| 8 | Contribution/claim-support 的从属试验行 | 只保留主张强度，不列技术方法 | `positive_reasoning` |
| 8 | Limitations > 第 8 项 | 完整保留一次 | 第 14 节完整权威 |
| 9 | Structured abstract > Contribution 中“并非新算法” | 删除重复警示 | — |
| 9 | Current resource and result status > closest-work 状态 | 保留检索范围和置信状态的当前事实 | `current_factual_status` |
| 9 | Required analyses and evidence > closest-work 追加段落 | 删除 | — |
| 9 | Verified representative closest-work comparison；claim-support 最后一行 | 保留组件先例、完整组合低至中等置信及条件性整合定位 | `positive_reasoning` |
| 9 | Risks > 最接近工作定位变化 | 保留新证据触发、更新检索响应和主张后果 | `risk_response` |
| 9 | Limitations > 第 9 项 | 完整保留一次 | 第 14 节完整权威 |
| 10 | Limitations > 第 10 项 | 完整保留一次；正文其他位置没有监管限制条件复述 | 第 14 节完整权威 |
| 11 | one-sentence summary | 保留“不把预测与观察性表征作因果证据”的身份边界 | `positive_reasoning` |
| 11 | Structured abstract > Background 中的非因果重复 | 删除 | — |
| 11 | Gap；Primary research question；Core hypothesis | 保留不混淆预测、观察性表征与因果解释的核心问题边界 | `positive_reasoning` |
| 11 | Observational target 和试验方法中的对象特异解释规则 | 保留直接决定估计和解释的科学规则 | `method_eligibility` |
| 11 | Falsification 和 Interpretation matrix | 保留各失败或结果模式不能推出的结论 | `interpretation` |
| 11 | Contribution/evidence ladder、closest-work 和 claim-support | 保留整合、验证、基准主张及新颖性主张的最小支持边界 | `positive_reasoning` |
| 11 | Limitations > 第 11 项 | 完整保留一次 | 第 14 节完整权威 |

全扫描结果：十一类完整限制条件只在第 14 节出现；外部保留文本均有上表中的一个必要功能；无功能的出现位置已删除；没有插入指向第 14 节的说明。

## PCR-001 至 PCR-064 逐项保留映射

| 保护项 | v056 修订位置 | dossier 中的简要保留证据 |
|---|---|---|
| PCR-001 | frontmatter > `identity_anchor` | 五个引号内值与 register v007 逐字符一致。 |
| PCR-002 | Research question, objectives, and core hypothesis > Primary research question；Objectives | 完整研究问题、四项目标、阶段 I–II 优先和从属分试验问题均在。 |
| PCR-003 | Core hypothesis and evidence boundary | 共同支持、预先固定、绝对恢复、允许重参数化下的不变量及非因果估计边界均在。 |
| PCR-004 | Research design and methods > Observational target, anchoring, and evidence-qualified interpretation | 研究对象、患者—时间推断单位及 (X,Y,A,M,B,S) 联合预测/生成目标均在。 |
| PCR-005 | Protocol locks for the two primary clinical tasks | 两人群、首次发病、延迟进入、总权重、互斥终止、出院和行政结束规则均在。 |
| PCR-006 | Mutually exclusive post-onset state and event system | 12 小时赋值、固定优先级、无法排序处理、吸收/竞争/可复发状态均在。 |
| PCR-007 | Data > Variable roles | 生理、治疗、测量、标签和基线分离及隔离副本、缺失和静态值规则均在。 |
| PCR-008 | Public intensive-care database roles and support audit | MIMIC-IV、eICU、预指定备份和只允许可审计共同概念的角色均在。 |
| PCR-009 | Public intensive-care database roles and support audit > audit table | 医院、事件/转移、锚点密度与覆盖、复杂度和时间网格的全部支持规则均在。 |
| PCR-010 | Current resource and result status | 访问和审计未完成、尚无模型或结果，以及 closest-work 证据置信状态均在。 |
| PCR-011 | Local randomized-trial evidence status | EXIT-SEP 与 XBJ-SCAP 的全部登记计数、来源性质、字段缺口和 D-二聚体单位状态均在。 |
| PCR-012 | Current resource and result status > trial rows；Local randomized-trial evidence status | 授权、原始表单/计划、随机化、中心、访视与生存语义及映射输入均明确尚未核验。 |
| PCR-013 | Feasibility and resources | 六类职责、人员未核验、两库/四维/三机制/两主任务/两诊断/一复杂候选范围及排除活动均在。 |
| PCR-014 | Work packages and minimum route；24-month milestone；Limitations item 6 | 固定最小顺序、失败替代、阶段 I–II 的 24 个月最低交付及从属阶段 III 均在。 |
| PCR-015 | Conjunctive minimum success definition；24-month milestone；Limitations item 6 | 全部合取标准、阈值只能收紧、有限适配不能改变失败，以及阶段 III 不能补足阶段 II 均在。 |
| PCR-016 | Protocol locks > primary pre-onset task | 12 小时首次发病、landmark/history/weight、指标、聚类区间及所有达标阈值均在。 |
| PCR-017 | Protocol locks > primary post-onset task | 第 7 日有利集合、Aalen–Johansen、第 14 日敏感性、分层、指标及主任务优先均在。 |
| PCR-018 | Protocol locks > event clock and information-availability clock | 72/24 小时配对、基线 SOFA、48 小时前至 24 小时后窗口、可用时钟和两种敏感标签均在。 |
| PCR-019 | Mutually exclusive post-onset state and event system | 生理恢复、恶化、新器官支持、出院、转院和死亡的完整定义与信息时刻均在。 |
| PCR-020 | Observational target, anchoring, and evidence-qualified interpretation | 两锚点、+1 载荷、维数/机制/滞后上限、无瞬时循环、20 种子对齐和可解释对象均在。 |
| PCR-021 | Observational target > missingness and action support | −1 至 +1 偏移、临界点、5%/95% 行动比例、20% 有效样本及不估计治疗作用均在。 |
| PCR-022 | Absolute simulation and semi-synthetic recovery criteria > regimen | 至少 1,000 次或 MCSE ≤0.02，全部生成机制和交叉情景均在。 |
| PCR-023 | Absolute simulation > continuous branch | 同一患者—时间点、最小未平方典型相关、失败记 0、(L) 公式和 0.80 门槛均在。 |
| PCR-024 | Absolute simulation > recovery table and closing rule | ARI、转移 MAE/覆盖、符号/滞后、FDR、零边、错设、校准及失败动作全部在。 |
| PCR-025 | Hospital-primary cross-database validation > partition and linked-patient rules | 种子 20260717、30%/70%、跨分区排除、二部图敏感性和全部支持/10% 后果均在。 |
| PCR-026 | Hospital-primary cross-database validation > four update operations | 不更新、仅校准、仅观测层和全模型重拟合的顺序、角色及不可补偿规则均在。 |
| PCR-027 | 试验观测映射和独立分析 > 共享前提 | 阶段 II 合取成功、授权、核心语义、分试验和不合并等共享规则均在。 |
| PCR-028 | 试验观测映射和独立分析 > 观测映射成立时的分析及忠实度 | 锚点资格、两锚点、冻结参数、SVD、符号、eICU 忠实度和盲态试验阈值全部在。 |
| PCR-029 | 试验观测映射和独立分析 > 分层标准化概率指数 | 死亡—代理—出院排序、完整 θ 公式、合并组权重、方向、并列半分和替代量限制均在。 |
| PCR-030 | 试验观测映射和独立分析 > 独立 SOFA 分支；核心语义停止 | 映射失败时的独立 SOFA 分支和核心语义失败停止所有新访视结局均在。 |
| PCR-031 | 试验观测映射和独立分析 > trial table and closing paragraph | 两试验人群/访视/分析集、插补、偏移、界限、Holm、亚组和稀疏访视规则全部在。 |
| PCR-032 | Secondary representation diagnostics | 伪遮蔽与未来轨迹的全部评分、分层及不改变主要判定的规则均在。 |
| PCR-033 | Required analyses and evidence；试验观测映射和独立分析 | 阶段 II 八组证据要求及试验授权、语义、资格与固定方法均在。 |
| PCR-034 | Falsification and stop criteria > 时钟与信息泄漏；数据支持 | 未来信息/跨拆分失败及事件、医院、排除或锚点支持不足的动作均在。 |
| PCR-035 | Falsification > 绝对恢复；非随机缺失与行动支持；外部结果 | 复杂候选不晋级、敏感性范围、低支持解释和外部失败含义均在。 |
| PCR-036 | Falsification > 试验观测映射；试验核心语义 | 映射失败、独立 SOFA 保留、核心语义停止、方向不一致/宽区间和禁止亚组修复均在。 |
| PCR-037 | Falsification > 时间 | 月 12、20、24 的封存、不可访问和最低端点未完成后果均在。 |
| PCR-038 | Risks, alternatives, and stop conditions | 访问/支持、职责、隔离、跨院支持、试验语义和 closest-work 的对象特异触发—响应—后果均在。 |
| PCR-039 | Title/summary/abstract；question/objectives；milestone | 候选和计划状态、待生成输出、条件性整合/验证贡献及从属试验地位均在。 |
| PCR-040 | Contribution and evidence ladder | 数据、状态/任务、跨数据库和从属分试验证据的逐级主张强度均在。 |
| PCR-041 | Verified representative closest-work comparison | 各研究线先例、截至 2026-07-17 的置信状态及条件性整合与验证定位均在。 |
| PCR-042 | Interpretation matrix | 简单基线、恢复/外部失败、适配、任务、两试验分支和完整阶段 II 的解释边界均在。 |
| PCR-043 | 试验观测映射和独立分析；trial evidence chain；Planned outputs | 分试验次要结果或不分析记录、不计入阶段 II、不合并及随机分配的有限解释均在。 |
| PCR-044 | Working assumptions > continuous recovery；Absolute simulation > continuous branch | 唯一定义、双负责人、月 7 前截止、未确认后果和受影响部分均在。 |
| PCR-045 | 试验观测映射和独立分析 > probability index；Working assumptions > trial estimator | 完整估计目标在方法权威；具名统计负责人、确认时点、未确认停止和阶段 I–II 不受影响均在。 |
| PCR-046 | Working assumptions > clinical-scale-to-simulation mapping | 月 7、允许信息、固定生成/恢复对象和未解决时不启动或不晋级均在。 |
| PCR-047 | Working assumptions > multicategory calibration | 月 6、允许信息、固定指标/阈值和未解决时不判成功或不授权外部测试均在。 |
| PCR-048 | Limitations > 1. 资源、访问与团队状态 | 数据库存在不等于访问、职责不等于承诺、项目计数和支持仍待审计完整在。 |
| PCR-049 | Limitations > 2. 标签、时钟与信息泄漏 | 发病时刻不唯一、标签依赖项、泄漏来源和高严重度门槛完整在。 |
| PCR-050 | Limitations > 3. 状态可恢复性与结构范围 | 允许重参数化、模拟非真实识别、预测不可替代恢复证据及失败动作完整在。 |
| PCR-051 | Limitations > 4. 非随机缺失与低行动重叠 | 缺失敏感性不能识别未测生理真值及低支持不能估计治疗作用完整在。 |
| PCR-052 | Limitations > 5. 跨数据库证据 | 数据库差异、整院接口、不更新主证据、适配/重拟合角色及不能改变失败完整在。 |
| PCR-053 | Limitations > 6. 时间与交付边界 | 24 个月、月 12/20/24 后果、阶段 III 在外及不能补足阶段 I–II 完整在。 |
| PCR-054 | Limitations > 7. 试验数据与语义 | 条件性来源、衍生报告不能替代原始材料、稀疏/人群/字段差异及不合并完整在。 |
| PCR-055 | Limitations > 8. 共同生理锚点变量与观测映射 | WBC/CRP 候选、D-二聚体单位、无忠实度结果及两分支解释边界完整在。 |
| PCR-056 | Limitations > 9. 最接近工作不确定性 | 非系统综述、未覆盖来源、术语/预印本影响及低至中等置信完整在。 |
| PCR-057 | Limitations > 10. 监管适用范围 | 2026 指南的监管谨慎及不能支持无条件国际推广完整在。 |
| PCR-058 | Limitations > 11. 完整禁止主张 | 因果、机制、控制、数字孪生、整系统验证、已验证工具/平台和亚组修复等禁止主张完整在。 |
| PCR-059 | 24 个月最低交付与时间节点 | 职责签署不等于承诺、测试资料隔离至月 18–20 冻结及月 20 后不许测试驱动修改均在。 |
| PCR-060 | Working assumptions > closing qualification | 事件/参数下限只是筛选、不能替代有效样本量等，以及按时解决否则执行后果均在。 |
| PCR-061 | Limitations > 11 | 观察性表征不支持真实因果网络、治疗效应、反事实、机制、中介、控制或数字孪生均明列。 |
| PCR-062 | Limitations > 11；Contribution/evidence ladder | 不能称已验证模型、决策工具、药物平台或临床有效；因果和应用需要额外证据均在。 |
| PCR-063 | Verified representative closest-work comparison；Risks > closest-work | 不支持新算法、全球首次/不存在、首次或专利不存在；加强主张所需检索及低至中等置信定位均在。 |
| PCR-064 | 试验观测映射和独立分析；Interpretation matrix；Limitations > 11 | 试验差异不能验证潜在动力学、转移边或整系统；不合并、不主张共同机制和不以亚组改变解释均在。 |

保留计数：**64/64**。

## 五个机器身份锚点逐字符比较

| 字段 | register v007 位置 | v056 位置 | 比较结果 |
|---|---|---|---|
| `primary_research_question` | `identity_anchor.primary_research_question` | frontmatter 同名字段 | 完全一致，包括问号、连字符和大小写 |
| `primary_objective` | `identity_anchor.primary_objective` | frontmatter 同名字段 | 完全一致，包括句号和 `stage II` 大小写 |
| `study_object` | `identity_anchor.study_object` | frontmatter 同名字段 | 完全一致，包括连字符和句号 |
| `core_data_or_evidence_base` | `identity_anchor.core_data_or_evidence_base` | frontmatter 同名字段 | 完全一致，包括分号、连字符、试验名称和句号 |
| `primary_unit_of_inference` | `identity_anchor.primary_unit_of_inference` | frontmatter 同名字段 | 完全一致，包括连字符和句号 |

身份锚点计数：**5/5**。v056 同时使用 `artifact_id: idea-dossier-I01-001-v056`、`version_id: v056`、v22 路径、`plugin_version: 0.9.0-preview.3` 和 `change_type: editorial_repair`。

## 最终一致性和结构检查

| 检查 | 结果 |
|---|---|
| 冻结前动作合规 | 编排器检查 **PASS**；之后只把 `frozen` 改为 `true`。 |
| 必需结构 | 15 个 H2 按契约顺序存在；Background、Current state、Gap、Significance、Rationale 五个 H3 顺序正确。 |
| 证据链 | 5 条；每条均有 Input、Method / analysis / processing、Output、Supports，共 20/20 个字段。 |
| 试验方法权威 | `试验观测映射和独立分析` 恰有 1 个；θ 公式、Holm、Rubin、Frobenius 忠实度、mITT 和映射投影等试验技术规范在该权威之外出现数为 0。 |
| 分支和阶段 | 映射失败不抹除独立 SOFA；核心语义失败停止全部新访视结局；两试验分开；阶段 III 不计入或补足阶段 II。 |
| 限制条件权威 | 第 14 节有且仅有 11 个完整类别；限制条件指针数为 0。 |
| 未纳入项目 | dossier 中没有 `NRP-003` 或 `LA-001` 至 `LA-006` 的执行记录或对应修复。 |
| 参考文献 | v055 的 38 条参考文献原样保留。 |

最终运行的命令为：

```text
python research-skills-openai/skills/multi-path-idea-generator/scripts/lint_idea_dossier.py tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v22/idea-dossier-v056.md --expected-plugin-version 0.9.0-preview.3
```

结果：退出码 `0`，并报告 `OK: ...\idea-dossier-v056.md`。提示位置中的“锚点观测值/锚点预测值”、(X_b,d_b,r_b,s_r)、(Y_0,Y_1,ω_s) 和“记为 0”均是紧邻定义的科学术语、公式符号或数值处理规则；本次没有借这些提示执行任何未纳入的语言修订。

