---
schema_version: research-idea-revision-delta.v1
artifact_id: revision-delta-I01-001-v007-to-v008
workflow_id: RID-SEPSIS-CSM-20260717-001
idea_id: I01-001
version_id: v008
from_version: v007
to_version: v008
change_type: editorial_repair
based_on:
  - artifact_id: idea-dossier-I01-001-v007
    version: v007
    path: tests/idea-narrative-forward-0.9.0-preview.3/run-001/finalized/idea-dossier-v007.md
  - artifact_id: narrative-repair-plan-I01-001-r006
    version: r006
    path: tests/idea-narrative-forward-0.9.0-preview.3/run-001/finalized/narrative-repair-plan-r006.yaml
  - artifact_id: language-assessment-I01-001-r006
    version: r006
    path: tests/idea-narrative-forward-0.9.0-preview.3/run-001/finalized/language-assessment-r006.md
  - artifact_id: protected-content-register-I01-001-v007
    version: v007
    path: tests/idea-narrative-forward-0.9.0-preview.3/run-001/finalized/protected-content-register-v007.yaml
---

# Revision delta: v007 to v008

## Revision scope

本轮仅实施叙事修复计划 r006 与语言评估 r006 有明确依据的编辑性修订。未改变核心研究问题、研究对象、数据或证据基础、阶段关系、估计目标、数值阈值、主张强度、关键限制、停止条件或可行性判断；未新增证据、方法或结果。

实际读取文件仅为：

1. tests/idea-narrative-forward-0.9.0-preview.3/run-001/finalized/idea-dossier-v007.md
2. tests/idea-narrative-forward-0.9.0-preview.3/run-001/finalized/narrative-repair-plan-r006.yaml
3. tests/idea-narrative-forward-0.9.0-preview.3/run-001/finalized/language-assessment-r006.md
4. tests/idea-narrative-forward-0.9.0-preview.3/run-001/finalized/protected-content-register-v007.yaml

## Itemized revisions

| 输入问题或 action | 具体定位与操作 | 保留内容 | 删除或移动内容 | 科学含义是否改变 | Protected-content disposition |
|---|---|---|---|---|---|
| NRP-001 / NAR-001：首次论证用途前未定义“状态对齐”和“观测方程” | “Title, summary, audience, and positioning”中的“跨学科概念桥”；增加两项功能性定义：状态对齐用于将不同随机种子拟合或数据库中的对应潜在状态匹配到共同参照；观测方程描述潜在状态与实测生理指标的关系，并作为阶段 III 冻结观测映射的来源 | 候选动态系统模型、共同观测指标、共同生理锚点、共同生理锚点预测的原有定义；四类证据导航；阶段 I–II 与条件性阶段 III 的顺序和边界 | 无删除、无移动；未加入公式、阈值或实现步骤 | 否 | PCR-V007-001 retained_same_meaning；PCR-V007-004 retained_same_meaning；PCR-V007-005 retained_same_strength；PCR-V007-006 retained_once_at_authority_location |
| NRP-002 / NAR-002：最终身份段重复阶段 II—III 失败边界 | “Feasibility, resources, risks, alternatives, and stop conditions”中的“Research identity and final boundary”；删除重复末句 | “Scientific and interpretive boundaries”第 7 项保留完整陈述；最终身份段保留研究问题、目标、对象、证据基础、推断单位及何种改变构成另一项研究的判据 | 删除“阶段 III 永不补足阶段 II 任一必要条件未满足所造成的失败。”；未移动其他内容 | 否 | PCR-V007-006 retained_once_at_authority_location；PCR-V007-007 retained_same_boundary |
| LANG-R006-001：阶段 II、阶段 III 首用不可达 | “One-sentence complete-Idea summary”首次使用处直接说明阶段 II 包括模型开发、恢复检验、两项主要临床任务和跨数据库验证，阶段 III 为条件性随机试验次要分析；“Structured abstract”中以同样的工作范围名称辅助独立阅读 | 24 个月最低交付、阶段 I–II 的既有编号与顺序、阶段 II 全部必要证据、阶段 III 条件性及其位于最低交付之后的关系 | 未删除阶段标签；未重新命名或另行划分阶段 I | 否 | PCR-V007-001 retained_same_meaning；PCR-V007-004 retained_same_meaning；PCR-V007-006 retained_once_at_authority_location |
| LANG-R006-002：“结构符号”可被误读为结构边方向 | 首次定义及后续相关位置统一为“预设关系的正负符号与时间滞后”；首用明确正负符号指关系系数正负号而非结构边方向；阈值表分别保留结构边检测与正负符号一致率 | 结构边、关系正负符号、时间滞后原有评价对象；全部恢复率、一致率、灵敏度、错误发现率和后果 | 删除含混词面“结构符号或滞后”“外部符号一致率”等；未删除任何评价对象，未移动阈值 | 否 | PCR-V007-004 retained_same_meaning |
| LANG-R006-003：“状态对齐”首次出现时多义 | “跨学科概念桥”首用改为“潜在状态跨拟合或跨数据库匹配（状态对齐）”，并说明允许的潜在状态维度排列与符号变换；“Observational model target...”及阈值表明确匹配对象为潜在状态和随机种子拟合或数据库 | 20 个固定随机种子、跨数据库比较、共同参照、原有对齐率与 0.70/90% 阈值 | 无科学内容删除或移动；仅替换含混简称并保留后续简称 | 否 | PCR-V007-004 retained_same_meaning |
| LANG-R006-004：“状态占用”混合概率与经验比例 | “跨学科概念桥”将主要估计对象定义为“状态占用概率”，另将样本频率命名为“观察到的状态比例”；正文涉及估计、恢复、输出和校准处统一使用“状态占用概率” | 原有状态对象、时间点、任务、恢复和校准含义 | 删除“概率或比例”的合并定义；未删除任何状态估计或输出 | 否 | PCR-V007-004 retained_same_meaning |
| LANG-R006-005：单次“任务效度”与全文术语不一致 | “Evidence chain: 两项主要临床任务与两项次要表征诊断”的 Supports 改为“任务级预测表现”；“Contribution and evidence ladder”改为“模型恢复与任务表现” | Brier 分数、校准、状态概率及两项任务的证据职责 | 删除可能暗示构念效度的单次词面；无内容移动 | 否 | PCR-V007-005 retained_same_strength |
| LANG-R006-006：模型属性的中文修饰结构不平行 | “Primary research question”将“知识约束且量化不确定性的”改为“受知识约束且能够量化不确定性的” | 知识约束和不确定性量化两项原有模型性质 | 无删除、无移动 | 否 | PCR-V007-001 retained_same_meaning |
| LANG-R006-007：变量角色表并列项缺少同层中心语 | “Variable-role separation”中的“生理测量”行；改为“实测生命体征、血气指标、实验室检验指标和器官功能指标” | 四类原有生理测量及其角色分离规则 | 无删除、无移动 | 否 | PCR-V007-002 retained_same_meaning；PCR-V007-004 retained_same_meaning |
| LANG-R006-008：奇异值并列句缺少选定对象 | “Pre-specified deterministic observation mapping”；明确“用于定义第一奇异轴的奇异值并列”时由锚点字典顺序选定该轴 | 原有锚点字典、\(V_1\)、符号固定规则、观测映射及其冻结关系 | 无删除、无移动；未新增选择标准 | 否 | PCR-V007-004 retained_same_meaning |
| LANG-R006-009：“患者或住院跨集合”记录单位不明 | “Protocol locks for the two primary clinical tasks”后的数据泄漏审计句，以及“Operational thresholds...”中的“标签与数据分组”行；改为“同一患者或其重复住院或 ICU 入住记录被分配到不同数据集合” | 患者、住院与 ICU 入住记录不跨数据集合的原分组规则；未解决高严重度泄漏的原后果 | 无删除、无移动 | 否 | PCR-V007-002 retained_same_meaning；PCR-V007-004 retained_same_meaning |
| LANG-R006-010：项目内部或文档控制式措辞 | “Trial semantics...”与“External projection...”删除 R0/R1 代码，仅保留描述性检查名称；第 14 节开头改为自然表述“均以本小节的完整陈述为准”；“Research identity and final boundary”将“本 Idea”改为“本研究构想”，并把修订控制式开句改为研究身份的直接陈述 | 两项检查的全部资格和评价内容；第 14 节的全局权威地位；研究身份边界 | 删除 R0/R1 代码及“唯一完整权威位置”“本 Idea”等词面；未删除或移动任何限制 | 否 | PCR-V007-001 retained_same_meaning；PCR-V007-006 retained_once_at_authority_location；PCR-V007-007 retained_same_boundary |
| LANG-R006-011：四项技术对象清单重复 | 在首次完整定义后引入不含歧义的集合名“预定状态与结构对象”；在开篇证据导航、“Gap”、统一模型接口和贡献阶梯中使用集合名；结构化摘要、核心假设、方法目标和恢复评价等需局部精确的位置保留完整对象 | 状态占用概率、转移概率、共同生理锚点预测、预设关系正负符号与时间滞后四类对象；所有预先设定、隔离、锁定与冻结限定 | 仅删除部分重复列举的词面；未删除对象、限定条件或叙事职责，无移动 | 否 | PCR-V007-004 retained_same_meaning；PCR-V007-005 retained_same_strength |
| LANG-R006-012：证伪标准中的“预定的适当评分和校准”搭配含混 | “Scientific falsification criteria”；改为“两项主要临床任务不能……达到预定的评分与校准标准” | 两项任务、开发与跨时间数据、原有证伪逻辑及全部数值阈值 | 无删除、无移动 | 否 | PCR-V007-004 retained_same_meaning |
| LANG-R006-013：分析目标表和操作阈值表的单元格层级过深 | “Analysis targets”两个试验行按人群、访视、缺失、敏感性、多重性和亚组分项；“Operational thresholds, alternatives, and stop conditions”各行将触发条件与对应后果拆为短而平行的编号分项 | 所有人群数、访视、分析集、插补、偏移、界限、多重性、阈值、优先级、替代方案和停止后果 | 无删除、无移动；所有数值、逻辑连接词和后果保持原值 | 否 | PCR-V007-004 retained_same_meaning；PCR-V007-006 retained_once_at_authority_location |

## Protected-content disposition

| Protected ID | Required disposition | v008 disposition |
|---|---|---|
| PCR-V007-001 | retained_same_meaning | 已保留：核心问题、全病程身份、24 个月阶段 I–II 边界和非普通预测模型定位未改变 |
| PCR-V007-002 | retained_same_meaning | 已保留：纵向脓毒症 ICU 患者系统、患者—时间状态与状态转移、患者和医院聚类均未改变 |
| PCR-V007-003 | retained_same_status | 已保留：文献与专家先验、公共 ICU 数据、条件性试验数据及其授权、语义和可用状态均未改变 |
| PCR-V007-004 | retained_same_meaning | 已保留：阶段顺序、两项主要任务、估计目标、全部数值阈值、模拟恢复、跨数据库验证、证伪标准和阶段依赖均未改变 |
| PCR-V007-005 | retained_same_strength | 已保留：模型、恢复、外部验证和试验分析仍为计划产物；贡献、创新和可行性主张未加强 |
| PCR-V007-006 | retained_once_at_authority_location | 已保留：第 14 节仍集中、完整规定关键限制、可行性发现、解释边界、替代方案和停止条件；阶段 II—III 失败边界在该权威位置保留一次，阈值、后果与风险未削弱 |
| PCR-V007-007 | retained_same_boundary | 已保留：观察性与预测证据不支持真实因果网络、机制、控制或数字孪生；试验分支的禁止主张未改变 |

## Structural and provenance checks

- v008 保留 v007 的 15 个既有 H2，名称与顺序不变。
- 第三个 H2 “Background, current state, gap, significance, and rationale”仍含五个非空 H3：“Background”“Current state”“Gap”“Significance”和“Rationale”。
- “Evidence chains”仍含五条证据链；每条均保留非空的 Input、Transformation、Output 和 Supports 字段。
- “Title and positioning claim-support table”仍保留主张、设计、证据链输出、文献基础、实际增量和支持状态结构。
- dossier frontmatter 已更新为 artifact_id: idea-dossier-I01-001-v008、version_id: v008 和 change_type: editorial_repair。
- dossier 与本 delta 的来源记录仅使用 artifact_id、version 和 path，未加入其他校验字段。

## Unexecuted or unresolved items

无。四个获准输入足以安全决定上述编辑性修订；未对其范围外的科学内容作推测，也未评价 narrative readiness。
