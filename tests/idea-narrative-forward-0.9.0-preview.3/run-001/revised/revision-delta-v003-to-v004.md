---
schema_version: research-idea-revision-delta.v1
artifact_id: revision-delta-I01-001-v003-to-v004
version_id: v001
workflow_id: RID-SEPSIS-CSM-20260717-001
idea_id: I01-001
source_artifact:
  artifact_id: idea-dossier-I01-001-v003
  version: v003
  path: tests/idea-test-0.9.0-preview.1/0.9.0-preview.1/03_ideas/nodes/I01-001/dossiers/idea-dossier-v003.md
revised_artifact:
  artifact_id: idea-dossier-I01-001-v004
  version: v004
  path: tests/idea-narrative-forward-0.9.0-preview.3/run-001/revised/idea-dossier-v004.md
repair_inputs:
  - artifact_id: narrative-repair-plan-I01-001-r001
    version: r001
    path: tests/idea-narrative-forward-0.9.0-preview.3/run-001/baseline/narrative-repair-plan-r001.yaml
  - artifact_id: language-assessment-r001
    version: r001
    path: tests/idea-narrative-forward-0.9.0-preview.3/run-001/baseline/language-assessment-r001.md
  - artifact_id: protected-content-register-I01-001-v003
    version: v003
    path: tests/idea-narrative-forward-0.9.0-preview.3/run-001/inputs/protected-content-register.yaml
  - artifact_id: reader-handoff-forward-001
    version: v001
    path: tests/idea-narrative-forward-0.9.0-preview.3/run-001/inputs/reader-handoff.yaml
source_skill: multi-path-idea-generator
change_type: editorial_repair_delta
identity_status: preserved
scientific_content_change: false
method_change: false
threshold_change: false
claim_strength_change: false
editorial_assessment_needed: true
---

# Revision delta: idea-dossier-I01-001 v003 to v004

## Revision scope

本轮是一次仅限编辑与科学写作的集中修订。修订依据为叙事修订计划、学术语言评估、受保护内容注册表和读者交接文件。未新增数据、方法、分析、阈值、文献或科学主张；未改变主要研究问题、主要目标、研究对象、核心证据基础、推断单位或阶段顺序；未把计划工作改写为既有结果，也未弱化任何可行性发现。

v004 是完整 dossier，不是补丁。v003 保持不变。所有新产物和输入均以 `{artifact_id, version, path}` 逻辑身份引用，未增加内容哈希字段。

## Identity and scientific preservation

| 受保护身份要素 | v003 含义 | v004 处理 |
|---|---|---|
| 主要研究问题 | 构建知识约束且量化不确定性的脓毒症全病程动态系统表征，检验跨数据库状态与结构稳定性，再开展条件性随机试验分析 | 含义不变；用“候选动态系统模型”明确数学对象，并在摘要首次出现时说明其以患者—时间状态和状态转移为对象 |
| 主要目标 | 24 个月内完成阶段 I–II 的构建、系统辨识和跨数据库验证 | 完全保留；阶段 III 仍位于 24 个月最低交付之后 |
| 研究对象 | 纵向、以脓毒症为中心的 ICU 患者系统，包括可比较的未发病在险时段和发病后轨迹 | 完全保留；标题、摘要、研究问题和方法均继续覆盖发病前、首次发病、发病后和结局 |
| 核心证据基础 | 文献和专家先验、MIMIC-IV、eICU-CRD，以及条件性 EXIT-SEP 和 XBJ-SCAP 个体数据 | 完全保留；HiRID 或 AmsterdamUMCdb 的预指定备份角色也保留 |
| 主要推断单位 | 尊重患者和医院聚类的患者—时间状态及状态转移 | 完全保留并在标题摘要后即时说明 |

方法顺序、状态定义、试验访视、分析集、缺失数据方法、外部数据库分组、所有日期和所有数值阈值均原样保留。仅将重复出现的操作触发条件和解释边界移至第 14 节的权威小节。

## Repair-plan actions completed

### NRP-001 — rebuild the reader chain in section 3

- 将原来没有功能性 H3 的第三节改写为合同要求的五个非空 H3，顺序严格为 `Background`、`Current state`、`Gap`、`Significance` 和 `Rationale`。
- `Background` 解释脓毒症时间演变、Sepsis-3 与事件时间和信息可用时间的区别，保留引文 [1-3]。
- `Current state` 分别说明公共 ICU 数据库可提供什么、跨库共同概念的已有能力、各方法模块的既有先例，以及随机试验的稀疏访视特点，保留引文 [5-10]、[17,18,21-37]。
- `Gap` 改为科学和证据缺口：候选状态与结构能否恢复、能否在未参与开发的数据库中保持、能否用冻结观测模型连接稀疏试验实测指标。删除以“没有完整组合”替代缺口的叙述。
- `Significance` 说明关闭该缺口对识别数据泄漏、不可辨识状态、测量政策差异和数据库运输失败的意义，不把意义等同于创新性。
- `Rationale` 按依赖关系解释双时间记录、变量角色分离、数据审计、简单模型与模拟恢复、按医院隔离的外部验证，以及条件性试验观测映射为何响应前述缺口。

### NRP-002 — simplify the complete-Idea summary

- 将 v003 中约 345 个字符、同时包含全部执行条件和禁止性清单的一句话摘要，改为一个可一次解析的主干句。
- 保留 24 个月阶段 I–II、全病程连续体、知识和专家约束、两个经审计的公共 ICU 数据库、计划性外部验证及阶段 III 从属关系。
- 将模拟判据名称、外部更新层级、EXIT-SEP 第 7 日、XBJ-SCAP 第 8 日、独立 SOFA 排序细节和完整禁止性枚举移至结构化摘要、方法或第 14 节。
- 摘要只保留一条改变允许解释范围的最小边界：预测表现或随机分组差异不等同于完整因果系统证据。

### NRP-003 — reorder and define the structured abstract

- 结构化摘要现在按背景与缺口、目标与假设、方法、预期结果、贡献与影响的读者顺序展开。
- 首先用普通科学语言说明发病前风险、发病后互斥状态、双数据库审计、由简单到复杂的模型比较、未用于开发的外部验证和条件性试验层的功能，再在正文方法中给出技术细节。
- 将 `landmark` 改为“动态预测时点”并在方法首次出现时定义；将原英文更新层级改为“不更新模型的外部验证”；将稀疏对象明确为“访视测量”，而非随机试验本身。
- 摘要明确所有结果均为计划产物，不把模型、模拟、外部验证或试验分析写成已经完成。

### NRP-004 — consolidate limitations and stopping logic

- 在第 14 节建立唯一 H3：`Authoritative limitations, feasibility findings, interpretation boundaries, alternatives, and stop conditions`。
- 该小节一次性收纳当前资源和结果状态、观察性与因果解释边界、外部验证更新层级的解释边界、随机试验映射和独立 SOFA 分支的解释边界、创新和应用边界、资源配置、全部数值触发条件、备选方案、停止后果及研究身份边界。
- 从结构化摘要、核心假设、日期表、证据链、计划产物、解释矩阵、贡献表和重复风险表中删除完整限制或停止条件副本。
- 第 11 节仅保留科学证伪标准，因为这些标准定义什么结果会挑战核心假设；不在那里重复操作性停止后果。
- 其他章节只保留直接决定相邻设计含义的最小限定，例如同一时间窗的信息可用规则、变量角色禁止混用、两项试验不合并，以及阶段 III 不属于 24 个月最低交付。

## Language findings addressed

| Finding | v004 disposition |
|---|---|
| ZH-001 | 一句话摘要压缩为一个清楚的研究对象—阶段 II 验证—阶段 III 从属关系主句；执行细节移至相应章节 |
| ZH-002 | 机器前置元数据只保留必要版本、血缘、身份和冻结信息，并将 `based_on` 改为逻辑引用；科研正文删除内部状态词，改为“重新界定为另一项研究” |
| GRA-001 | 改为“预设图结构中不允许同一时间窗内出现瞬时循环” |
| GRA-002 | 模拟运行规则改为完整主谓结构；在第 14 节明确每个核心情景至少 1,000 次重复，且在关键比例 MCSE 大于 0.02 时继续模拟 |
| GRA-003 | 明确为“第一奇异轴所解释的载荷矩阵 Frobenius 范数平方占比”，并说明 50% 的分母 |
| REG-001 | 将“变量角色防火墙、外部封印、填满、清零、救回”等内部或隐喻表达改为“变量角色分离、外部测试数据隔离与访问控制、完成审计、不存在未解决问题、不得事后调整阈值”等标准科学表达 |
| REG-002 | 将“真正未触碰、最近近邻、当前禁止”等防御性表达改为“预先隔离且未用于开发的外部验证数据、最接近的既有研究、现有证据不足以支持”等学术表达 |
| TERM-001 | 将“候选动态系统表征”统一为“候选动态系统模型”，并说明其输入为纵向观测、治疗和测量过程，输出为患者—时间状态、状态转移和任务结果 |
| TERM-002 | 将“条件性稀疏 RCT 次要再分析”统一为“基于稀疏访视测量的条件性随机试验次要分析”，明确稀疏的是随访时点和变量覆盖 |
| TERM-003 | 将“绝对模拟恢复门、假置信、零边假结构”展开为基于预设数据生成机制和绝对阈值的模拟恢复、错设识别及无结构边情景中的错误结构判断；指标和阈值完整保留 |
| TERM-004 | 将项目自定义的投影和排序端点标签改写为“一维可观测状态摘要的随机分组间差异”和明示的死亡—存活住院—存活出院排序；定义概率指数 |
| TERM-005 | 全文统一使用“开发数据、适配数据、预先隔离且未用于开发的外部验证数据、不更新模型的外部验证、只用适配数据再校准、只用适配数据更新观测层、全模型重新拟合” |
| TERM-006 | G1、R0、R1 不再作为主要叙事词；首次出现分别给出“双数据库可观测性与支持度审计”“试验语义与共同观测变量资格检查”“观测映射的外部忠实度检查”。CIF、IPCW、ARI、MCSE 等在首次使用时给出中文或英文全称 |
| CONC-001 | 随机试验完整分支只在方法和第 14 节的触发—后果表中保留；证据链、产物和贡献处只描述与本节功能相符的输入、处理或输出 |
| CONC-002 | 外部数据库的完整医院分组和患者处理流程只在方法部分定义；第 14 节仅保留支持度触发条件和解释后果 |
| READ-001 | 原 R0、R1 超长段落拆为“试验语义和共同变量资格”“冻结观测映射”“外部映射忠实度”“分析目标”四个功能段，并用列表或公式分开条件 |
| READ-002 | 表头和主叙事统一为中文；减少斜线与中英混排，保留的缩写均在首次出现时定义 |

## Protected-content disposition

| Protected ID | Required disposition | v004 location and preservation result |
|---|---|---|
| PCR-001 | retained_same_meaning | 前置元数据、标题摘要、主要研究问题、两项临床任务和互斥状态系统；研究仍是全病程动态系统模型而非普通预测 |
| PCR-002 | retained_same_meaning | 一句话摘要、目标、24 个月节点和工作包；阶段 I–II 仍以模型构建、系统辨识、跨数据库验证和可审计证据为目标 |
| PCR-003 | retained_same_meaning | 前置元数据、研究问题、观测模型目标和证据链；患者—时间状态及状态转移仍为主要推断单位，并处理患者和医院聚类 |
| PCR-004 | retained_same_status | 数据与材料节保留 MIMIC-IV、eICU、HiRID/AmsterdamUMCdb 角色；第 14 节明确数据库存在已核验，但访问、协议、提取、队列支持、人员和结果仍未核验或未生成 |
| PCR-005 | retained_same_status | 数据与材料节保留两试验样本与访视事实；第 14 节明确本地材料只为衍生报告，不能替代个体数据授权和原始试验语义核验 |
| PCR-006 | retained_same_meaning | 工作包和方法完整保留审计—锁定—简单基线—模拟恢复—复杂候选—主要与次要任务—冻结—外部验证—试验分析顺序，以及状态、治疗、测量过程分离 |
| PCR-007 | retained_same_meaning | 阶段 II 合取成功定义、外部验证方法和第 14 节外部解释边界；有限更新仍与不更新模型的外部验证分开，阶段 III 不补足阶段 II |
| PCR-008 | retained_same_meaning | 两项主要任务方案表、互斥状态表和必要分析；双时间、首次发病、延迟进入、竞争终止、信息可用规则、评分、校准、聚类和数据泄漏保护均保留 |
| PCR-009 | retained_same_strength | 结构化摘要、贡献与最接近工作比较、主张支持表和第 14 节当前状态；未增加结果或创新强度，完整组合缺口仍为低至中等置信 |
| PCR-010 | retained_once_at_authority_location | 第 14 节唯一权威 H3 完整保留资源、审计、标签、恢复、非随机缺失、外部运输、时间、试验语义、共同观测映射和最接近工作限制，以及一一对应的替代或停止后果 |
| PCR-011 | retained_once_at_authority_location | 第 14 节明确阶段 I–II 的 24 个月边界、阶段 III 的条件和不得补足阶段 II 失败；其他章节只保留说明工作时序所需的最小表述 |
| PCR-012 | retained_same_boundary | 第 14 节科学与解释边界集中保留观察性、预测和随机试验结果不能支持的因果、机制、控制、数字孪生、临床工具、药物平台或无条件推广主张 |

## Section-by-section change map

| H2 section | Editorial change | Scientific preservation |
|---|---|---|
| 1. Title, summary, audience, and positioning | 标题改用“候选动态系统模型”和“基于稀疏访视”；压缩一句话摘要；定位改为自然中文 | 保留全病程、24 个月、跨数据库验证和条件性试验身份；未增强贡献 |
| 2. Structured abstract | 重排为完整读者路线；解释模型对象和每层功能；删除阈值级堆叠 | 所有阶段、任务、数据角色和计划状态保留 |
| 3. Background, current state, gap, significance, and rationale | 新增合同要求的五个 H3；将创新防御改为证据缺口 | 引文与背景事实保留；未新增科学内容 |
| 4. Research question, objectives, and core hypothesis | 拆分长研究问题；将非假设完整清单移至第 14 节 | 四项目标和核心假设含义不变 |
| 5. Research content and work packages | 日期表改为产物和判断内容；停止后果移至第 14 节 | 时间、工作包、顺序和合取成功域保留 |
| 6. Data, materials, and existing evidence base | 分开公共数据库角色、审计字段、变量角色和试验数据；当前限制集中到第 14 节 | 数据库、试验、人数和非缺失计数保留 |
| 7. Research design and methods | 统一标准术语，定义缩写，拆分 R0/R1 长段并保留公式；外部验证分组与更新层级只在此完整定义 | 标签、状态、模型、模拟、分组、估计目标、缺失、多重性和阈值均未改变 |
| 8. Key techniques and implementation | 删除隐喻与内部实施口吻 | 十项技术功能完整保留 |
| 9. Evidence chains | 每条链仅保留合同规定的 Input、Method、Output、Supports；删除重复限制段 | 五条链及其输入、处理、输出和目标对应关系保留 |
| 10. Required analyses and evidence | 改为完整分析要求和自然科学术语；删除重复停止后果 | 所有必要分析、审计和试验启动前要求保留 |
| 11. Expected outputs, falsification criteria, and interpretations | 保留计划产物和科学证伪标准；删除重复解释矩阵 | 计划输出与会挑战核心假设的结果类型保留 |
| 12. Contribution, innovation, impact, application, and closest-work comparison | 将增量写成输入、转换和输出三层；统一最接近工作表述 | 代表性研究、稳定标识符、各模块已有先例和低至中等置信定位保留 |
| 13. Title and positioning claim-support table | 改为合同规定的七列；把限定直接写入主张单元格，移除不应进入主要定位的 unsupported 行 | 每个标题和主要定位主张均有实现、证据链、文献、实际增量和支持状态 |
| 14. Feasibility, resources, risks, alternatives, and stop conditions | 建立唯一权威 H3，并按当前状态、解释边界、资源、触发—后果和身份边界组织 | 所有可行性 finding、阈值、自动替代和停止条件完整保留且未弱化 |
| 15. References | 只作轻微中文标点自然化 | 38 条参考文献、编号和稳定标识符保留 |

## Numerical and design-preservation checklist

以下内容在 v004 中均保持不变：

- 24 个月阶段 I–II 和阶段 III 的时间位置；月 3、月 6、月 12、月 20、月 24 节点。
- 12 小时动态预测时点、最多 24 小时历史、未来 12 小时首次发病范围、第 7 日主要发病后终点和第 14 日敏感性分析。
- Sepsis-3 感染配对的 72 小时与 24 小时规则、感染前 48 小时至后 24 小时 SOFA 窗，以及两种标签敏感性定义。
- 状态优先级、SOFA 变化至少 2 分、连续 24 小时恢复要求及竞争终止处理。
- 每个自由参数的 20/10 个开发或外部事件或转移、至少两个共同锚点、30% 实测覆盖、70% 医院覆盖、80% 患者覆盖、最多 4 个状态维度、最多 3 个切换机制。
- 每个核心模拟情景至少 1,000 次重复或关键比例 MCSE 不超过 0.02，以及全部 ARI、典型相关、平均绝对误差、覆盖、恢复率、灵敏度、错误发现率、错设识别、错误高置信判断和校准阈值。
- 模式混合偏移 \(-1\)、\(-0.5\)、0、\(+0.5\)、\(+1\) 个标准差，行动比例 5% 和 95% 界，以及有效样本量 20% 界。
- 两项主要临床任务的 Brier 非劣 +0.01、校准斜率 0.80–1.20 和绝对风险误差 0.02。
- eICU 医院 30% 适配、70% 验证、固定种子 20260717、至少 20 个验证医院、跨分区排除 10% 界，以及外部状态对齐 0.70 和结构符号一致 0.80。
- 随机试验至少两个共同锚点、第一奇异轴 50%、相关 0.70、归一化平均绝对误差 0.50、截距 0.20 个标准差、斜率 0.80–1.20、覆盖 0.90–0.98、80% 生理范围和 60% 可计算访视标准。
- EXIT-SEP 和 XBJ-SCAP 的样本数、访视时点、非缺失计数、分析集、多重插补、\(\pm0.5\) 和 \(\pm1\) 个标准差敏感性分析、Holm 家族总体第一类错误率 0.05，以及仅报告亚组交互的规则。

## Clarification and guessing report

不需要澄清，也没有猜测修订计划中的修改位置、目标功能、术语、受保护内容或完成标准。四项叙事动作均给出明确章节、内容锚点、保留内容、移动目的地和验收条件；语言评估给出逐项术语替换方向；受保护内容注册表明确规定不得改变的科学内容；读者交接文件明确读者知识边界。

## Handoff

- revised_dossier: `{artifact_id: idea-dossier-I01-001-v004, version: v004, path: tests/idea-narrative-forward-0.9.0-preview.3/run-001/revised/idea-dossier-v004.md}`
- revision_delta: `{artifact_id: revision-delta-I01-001-v003-to-v004, version: v001, path: tests/idea-narrative-forward-0.9.0-preview.3/run-001/revised/revision-delta-v003-to-v004.md}`
- route_profile: `focused_optimization`
- identity_status: `preserved`
- editorial_assessment_needed: `true`

本 delta 不给出叙事、语言或科学准备度结论。v004 发生了实质性编辑变化，须由新的独立实例进行叙事与语言复评后，才可进入后续 dossier-only 评估。
