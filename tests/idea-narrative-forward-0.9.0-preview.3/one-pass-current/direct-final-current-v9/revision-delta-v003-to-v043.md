---
schema_version: research-idea-revision-delta.v1
plugin_version: 0.9.0-preview.3
artifact_id: revision-delta-I01-001-v003-to-v043
workflow_id: RID-SEPSIS-CSM-20260717-001
idea_id: I01-001
version_id: v043
path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v9/revision-delta-v003-to-v043.md
based_on:
  - artifact_id: idea-dossier-I01-001-v003
    version: v003
    path: tests/idea-test-0.9.0-preview.1/0.9.0-preview.1/03_ideas/nodes/I01-001/dossiers/idea-dossier-v003.md
target_artifact:
  artifact_id: idea-dossier-I01-001-v043
  version: v043
  path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v9/idea-dossier-v043.md
source_skill: multi-path-idea-generator
change_type: editorial_repair_delta
frozen: true
---

# I01-001 从 v003 到 v043 的修订增量

本次修订保持原研究构想的核心问题、目标、研究对象、证据基础和推断单位，只重组叙事、统一术语、显化方法边界并恢复可审计的章节职责。以下定位均指向冻结的 `idea-dossier-v043.md`。

## Narrative repair actions

| 修订编号 | 修订后定位 | 操作 | 可观察结果 |
|---|---|---|---|
| NRP-001 | `Background, current state, gap, significance, and rationale` 下的五个同名功能小节 | 重写并排序 | 背景、当前状态、未解决证据缺口、意义和设计理由依次展开；阶段 III 只作一句下游预告。 |
| NRP-002 | `Title, summary, audience, and positioning`；`Structured abstract` | 压缩并分工 | 一句话摘要先给候选表征、两个公共 ICU 数据库、主体检验和计划贡献，只保留一句条件性下游用途；结构化摘要五项各自完成单一功能。 |
| NRP-003 | `Research design and methods > 随机对照试验稀疏随访测量的条件性观测映射与临床状态次要分析` | 汇总 | R0、冻结映射、R1、两个互斥分析分支、缺失与死亡处理、多重性和停止条件只在该方法位置完整出现。 |
| NRP-004 | `Evidence chains`；`Feasibility, resources, risks, alternatives, and stop conditions` | 汇总 | 五条证据链均且仅含 Input、Method / analysis / processing、Output、Supports；完整限制族、假设、风险、替代和停止后果集中在第 14 个 H2。 |
| NRP-005 | `Key techniques and implementation` 的实现单元表 | 替换 | 每个实现单元明确输入、输出、持久记录、接口以及固定或版本边界，覆盖原有十类科学实现内容。 |
| NRP-006 | 全部 15 个 H2，重点为 `Research content and work packages` 至 `Feasibility, resources, risks, alternatives, and stop conditions` | 按章节职责归位 | 时间表、数据状态、完整方法、实现对象、证据链、验收证据、产物与解释、贡献、主张依据和完整限制分别留在对应章节；未用单一新表替代必需章节。 |
| NRP-007 | 一句话摘要；`Rationale`；`二十四个月主体计划与日期节点`；`双数据库可观测性最低标准`；两项主要任务、模拟、跨数据库及试验方法小节 | 定义并核对首次使用 | 候选表征、状态—行动—观察分离、G1、双时间、适当评分规则、四种参数处理状态、一维投影摘要和独立临床状态分析在首次承担推理功能时均有自然语言定义。 |

## Language repair findings

| 修订编号 | 修订后定位 | 操作 | 可观察结果 |
|---|---|---|---|
| LNG-R059-001 | H1、Title、定位段、Objective 4、第五条证据链、计划产物和主张依据表 | 统一修饰关系 | “稀疏”只修饰“随访测量”，“满足预设条件”只限制是否进行随机对照试验次要分析；正文不再使用“稀疏 RCT”等形式。 |
| LNG-R059-002 | 一句话摘要首次定义；全篇候选对象、复杂实现和冻结产物表述 | 角色分名 | 中央对象统一为“候选表征”，可选切换或非线性实现称“复杂候选模型”，阶段 II 产物称“阶段 II 冻结的候选表征”。 |
| LNG-R059-003 | `Rationale`；发病后状态；`模拟重建性能与错误结构高置信度支持率的判定标准` | 消除同词异义 | 患者结局只称“生理恢复状态”，模拟评价只称“模拟重建性能”，错误关系评价直接写为“对错误结构的高置信度支持”。 |
| LNG-R059-004 | `二十四个月主体计划与日期节点`；G1、R0、R1 方法小节；全部科学判定句 | 改为科学条件名称 | G1、R0、R1 首次出现均有中文全称和功能说明；全文不再用裸用“门”定义科学条件。 |
| LNG-R059-005 | `二十四个月主体计划与日期节点`；`医院优先的跨数据库检验与参数处理状态`；后续结果与限制位置 | 统一角色与操作名称 | 数据只区分适配医院集和最终检验医院集；四种参数处理状态均使用可直接判断哪些参数被重新估计的中文操作名称。 |
| LNG-R059-006 | 试验方法权威小节；第五条证据链；解释矩阵；贡献阶梯；主张依据表 | 统一分支名 | 投影量称“一维投影摘要（P_obs）”，对应结果称“随机分组在该访视投影摘要上的差异”，另一分支称“独立临床状态分析”。 |
| LNG-R059-007 | `现有资源、证据与待核验状态`；跨数据库证据链输出；主张依据表；末段研究构想边界 | 自然语言化 | 资源、跨数据库结果和主张支持三类状态分别使用自然中文且不混用；机器字段只留在元数据，不进入读者正文。 |
| LNG-R059-008 | 日期表、工作包、模拟与跨数据库方法、证据链、解释矩阵和第 14 个 H2 | 展开科学后果 | 每一处直接说明停止哪项分析、转用何种有数据支持的分析、仍报告什么以及不能再主张什么；叙述中的处置隐喻和英文流程标签已移除，合同规定的英文节标题保持不变。 |
| LNG-R059-009 | 一句话摘要；R0 与 R1；试验并列路径；最接近工作限制段 | 降低从句密度 | 摘要仅有两个并列主干；R0、R1 和分支条件采用定义句加分项；最接近工作段分别陈述检索所得、覆盖限制和允许定位。 |

## Protected-content preservation

| 保护编号 | 冻结稿定位 | 处理 | 可观察结果 |
|---|---|---|---|
| PCR-001 | frontmatter `identity_anchor`；`Primary research question`；末段研究构想边界 | 原样保留研究身份 | 研究仍覆盖脓毒症发病前、首次发病、发病后演化与结局的连续范围，没有收缩为普通预测。 |
| PCR-002 | 一句话摘要与定位段；`二十四个月主体计划与日期节点`；`计划产物` | 保留时间和交付边界 | 阶段 I–II 固定为 24 个月主体研究，目标是双库系统辨识、跨数据库检验、全流程可审计证据、高水平论文和可复用资源，而非单一预测器。 |
| PCR-003 | frontmatter `primary_unit_of_inference`；`Research design and methods` 首段 | 保留推断单位 | 推断单位仍为患者—时间状态及状态转移，不确定性估计同时保留患者与医院聚类。 |
| PCR-004 | `Data, materials, and existing evidence base`；`现有资源、证据与待核验状态`；公共 ICU 数据库角色 | 保留输入与证据状态 | 文献和专家先验、MIMIC-IV、eICU-CRD 仍为核心输入，HiRID 或 AmsterdamUMCdb 仅为预先指定备份；存在与版本、访问、DUA、提取、团队和结果状态继续分开。 |
| PCR-005 | `随机对照试验现有证据与边界`；资源状态表；第 14 个 H2 | 限定本地资料作用 | EXIT-SEP 与 XBJ-SCAP 的本地材料只支持衍生清洗、字段和稀疏访视描述，不替代授权、原始 CRF、SAP 或原始语义核验。 |
| PCR-006 | `工作包与最低执行顺序`；任务协议、状态—行动—观察、模拟、跨数据库及试验方法 | 保留设计次序和数值标准 | 设计顺序未改；两任务、模拟重复与误差、90% 对齐、80% 自助法保留、80% 外部符号一致、0.70 状态对齐及 R0/R1 标准均保留。 |
| PCR-007 | `阶段 II 的合取成功定义`；跨数据库方法；证伪标准；第 14 个 H2 | 保留合取与不可替代关系 | 阶段 II 成功仍要求数据支持、模拟重建、两项主要任务、无高严重度泄漏及不更新任何模型参数的跨数据库结果同时满足；有限重新估计和阶段 III 均不能补足失败项。 |
| PCR-008 | `两项主要临床任务的协议规范`；`发病后互斥状态与事件系统` | 保留完整任务协议 | 保留标本与抗菌药 72/24 小时配对、SOFA 基线与窗口、首次发病、患者权重、同一时间片顺序、标签可用时间和信息泄漏检查。 |
| PCR-009 | 标题、摘要、定位、贡献段和主张依据表 | 保持计划性证据语言 | 所有模型、模拟、跨数据库和试验结果均写为拟开展或待生成；试验整合仍受条件限制，未声称全球首次或新算法。 |
| PCR-010 | `Working assumptions`；`Limitations and boundary conditions`；`Risks, alternatives, and stop conditions` | 建立单一完整边界位置 | 待定规范逐项列出待定选择、已固定内容、决策时点、允许信息和未解决后果；限制族与风险、替代和停止条件完整保留，筛选阈值不替代经验有效样本量或模拟稳定性。 |
| PCR-011 | `Research design and methods > 随机对照试验稀疏随访测量的条件性观测映射与临床状态次要分析`；阶段计划与产物位置 | 保留下游树和阶段边界 | 阶段 III 位于 24 个月后并共享三个前提；完整路径只在方法权威位置出现，分别为观测映射成立、独立临床状态分析条件成立和核心语义不足时不开展新访视结局分析，且不新增试验终点。 |
| PCR-012 | `Limitations and boundary conditions` 第 11 项 | 完整保留禁止提高的主张 | 观察性与预测结果不支持真实因果网络、治疗效应、反事实策略、机制、中介、系统控制或数字孪生；条件性试验分析也不验证未测动力学、转移关系或整个候选表征。 |

## Terminology concordance

| 角色 | 唯一读者表述 | 首次定义定位 | 已移除或改作其他角色的竞争形式 | 全文检索结果 |
|---|---|---|---|---|
| CON-001 中央研究对象 | 候选表征；首次给出全称“脓毒症全病程候选动态系统表征” | `Title, summary, audience, and positioning` 的一句话摘要 | “候选架构”“候选系统表征”“最小全病程候选表示”已移除；“复杂候选模型”和“阶段 II 冻结的候选表征”只指各自不同角色 | 中央对象的竞争形式 0 处。 |
| CON-002 两项主要任务 | “未来 12 小时首次发病风险任务”；“第 7 日有利状态占用任务” | `Structured abstract > Approach` | 首次发病预测、一般有利状态概率等未定义短称不再作为任务名 | 两个正式名称分别贯穿任务协议、证据链、产物和判定位置。 |
| CON-003 两项次要诊断 | “已测值伪遮蔽重建诊断”；“未来轨迹概率诊断” | `Structured abstract > Expected result` | 裸用伪遮蔽、轨迹重建或代理诊断不再作为正式名称 | 两个正式名称各 5 处，角色无交叉。 |
| CON-004 模拟与患者结局 | “模拟重建性能”；“错误结构被高置信度支持的频率”；“生理恢复状态” | `Rationale`；模拟判定小节；发病后状态小节 | “绝对恢复”“假置信”“恢复门”已移除 | 裸用“恢复”未跨越模拟与临床两类语境。 |
| CON-005 条件性试验量与分支 | “一维投影摘要（P_obs）”；“随机分组在该访视投影摘要上的差异”；“独立临床状态分析” | 试验方法小节的映射定义与并列分析路径 | projection-pass、扰动、death-ranked、fallback、临床状态比较等竞争名称已移除 | P_obs 只在公式定义后使用；两个结果名在后续证据链、产物、解释和主张位置保持一致。 |
| CON-006 资源、跨库结果与主张状态 | 资源：“已有公开资料支持/尚未核验/尚未生成/项目内衍生资料”；跨库结果：“跨数据库稳定/仅适用于特定数据库/证据不足而不作解释”；主张：“有支持/有条件支持/无支持” | 三张对应状态表或输出清单 | verified/unverified/not generated、stable/database-specific/abstained、supported/qualified/unsupported 已移除 | 三组中文状态按证据维度分开使用，机器状态串在正文为 0 处。 |
| CON-007 外部数据角色 | “适配医院集”；“最终检验医院集” | `二十四个月主体计划与日期节点` 的角色定义段 | adaptation/test、untouched、未触碰测试区等已移除 | 正式名称分别出现 17 与 24 处，角色边界不变。 |
| CON-008 参数处理状态 | “不更新任何模型参数”；“仅用适配医院集重新估计校准截距和斜率”；“仅用适配医院集重新估计观测层参数”；“用目标数据库重新拟合全模型” | `二十四个月主体计划与日期节点` 的操作名称段；方法小节逐项说明 | zero-update、calibration-only、decoder adaptation、full refit、transport updating 等已移除 | 四个中文操作名称分别出现 14、10、10、6 处；每处均可判断重新估计范围。 |
| CON-009 模型和分析处置 | “停止继续评估该复杂候选模型”“转用多状态、线性或仅预测分析”“停止相应结构解释”“仅作数据库层面的描述”等具体后果 | 日期表、模拟判定表、解释矩阵及风险表 | 降级、准入、晋级、淘汰、挽救、封存、封印、防火墙、no-go、fallback 已移除；`stop` 只保留在合同规定的两个英文节标题中 | 所列流程隐喻在叙述性正文为 0 处；`stop` 仅有 2 处，均为固定节标题。 |
| CON-010 阶段名称 | “阶段 I–II”“阶段 II 合取成功”“阶段 III” | `Research content and work packages > 二十四个月主体计划与日期节点` | 阶段三、RCT 层、试验扩展层等竞争阶段名未作为正式名称使用 | 阶段 III 始终位于 24 个月后，且不计入阶段 II 合取成功。 |

## Remaining specifications

未决编辑项：无。仍待确定的科学规范和资源核验事项继续保留在 `Working assumptions`、`Limitations and boundary conditions` 与 `Risks, alternatives, and stop conditions`，包括备份数据库、时间方案替代、依赖 G1 的数值、临床尺度到模拟参数的映射、多类别校准估计与置信区间、共同生理测量以及试验授权和原始语义；本增量不把这些事项写成已经成立的证据。
