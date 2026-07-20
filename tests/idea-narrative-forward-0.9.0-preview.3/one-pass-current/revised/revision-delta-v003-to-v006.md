---
schema_version: research-idea-revision-delta.v1
plugin_version: 0.9.0-preview.3
artifact_id: revision-delta-I01-001-v003-to-v006
workflow_id: RID-SEPSIS-CSM-20260717-001
idea_id: I01-001
version_id: v006
path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/revised/revision-delta-v003-to-v006.md
based_on:
  - artifact_id: idea-dossier-I01-001-v003
    version: v003
    path: tests/idea-test-0.9.0-preview.1/0.9.0-preview.1/03_ideas/nodes/I01-001/dossiers/idea-dossier-v003.md
  - artifact_id: narrative-repair-plan-r014
    version: r014
    path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/baseline/narrative-repair-plan-r014.yaml
  - artifact_id: language-assessment-I01-001-r010
    version: r010
    path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass/baseline/language-assessment-r010.md
  - artifact_id: protected-content-register-I01-001-v003
    version: v003
    path: tests/idea-narrative-forward-0.9.0-preview.3/run-001/inputs/protected-content-register.yaml
source_artifact:
  artifact_id: idea-dossier-I01-001-v003
  version: v003
  path: tests/idea-test-0.9.0-preview.1/0.9.0-preview.1/03_ideas/nodes/I01-001/dossiers/idea-dossier-v003.md
revised_artifact:
  artifact_id: idea-dossier-I01-001-v006
  version: v006
  path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/revised/idea-dossier-v006.md
change_type: editorial_repair_delta
identity_status: preserved
---

# Revision delta: idea dossier v003 to v006

本次变更仅执行叙事与语言修复。研究问题、目标、研究对象、证据基础、主要推断单位、科学设计、阈值、条件分支、可行性发现和主张强度均未改变；没有选择新的方法或把计划工作写成已完成结果。

## Narrative repair actions

| Action | Disposition in v006 |
|---|---|
| NRP-001 | 将第三节重组为且仅为依次排列的 Background、Current state、Gap、Significance、Rationale 五个三级标题。背景交代脓毒症时间演化和标签问题，现状概括数据库与相邻研究，缺口提出跨阶段和跨数据库证据问题，意义说明可重复性与后续转化价值，依据逐项连接双时钟、过程分离、模拟恢复、独立外部验证与条件性试验分析。 |
| NRP-002 | 重写一语摘要，使研究对象、公共 ICU 数据、24 个月范围、独立保留数据库外部验证及条件性试验层的地位可直接理解；删除摘要中未经定义的流程标签和替代端点操作细节，但保留试验层不补足阶段 II 失败及非因果边界。 |
| NRP-003 | 按问题与缺口、目标与假设、总体设计、计划结果、贡献的顺序重写结构式摘要。首次出现时先解释候选动态系统表征、独立外部验证和一维可观测状态摘要的科学功能，再在方法节给出实现细节。 |
| NRP-004 | 将数据访问、人员、数据支持、标签与泄漏、模型可识别性、缺失与重叠、外部可迁移性、试验授权与语义、观测桥接、因果与临床解释、时间和最接近工作不确定性完整集中于第 14 节。其他章节只保留完成相邻科学推理所需的局部边界，未增加任何跨节指针。 |
| NRP-005 | 五条证据链均保留输入、处理、输出和支持四个字段，删除原有第五个限制与失败条件字段。被删除字段中独有的限制和失败后果已在第 14 节完整保留。 |
| NRP-006 | 将 Required analyses and evidence 收敛为可核验交付和记录，不再复制完整日期路线、实现算法或限制清单；八类阶段 II 证据、试验启动前核验和最接近工作定位要求均保留。 |

## Language repair dispositions

| Finding | Disposition in v006 |
|---|---|
| TERM-01 | 标题和全文统一为“访视稀疏随机对照试验的条件性次要分析”或等义完整短语，明确稀疏的是实际访视和重复测量，不是随机分配或样本。 |
| TERM-02 | 统一主名称为“一维可观测状态摘要”，首次说明其由试验实际访视共同生理指标和阶段 II 预定观测模型计算，用于访视时点排序比较；P_state 与 P_obs 在公式前后分别定义。 |
| TERM-03 | 统一核心研究对象为“候选动态系统表征”，首次说明其包含患者状态、状态转移以及生理测量、治疗行动和测量过程之间的受限关系，并明确只解释可恢复部分。 |
| TERM-04 | 区分并固定“不更新任何参数的独立保留数据库外部验证”“仅用适配集的校准更新”“仅用适配集的观测模型更新”和“全模型更新或开发”；不再用同一名称混指这些分析。 |
| TERM-05 | 将 death-ranked SOFA 统一为“死亡优先排序的 SOFA 复合状态端点”，并明确死亡最差、存活住院者按 SOFA 排序、活着出院最有利；对应可观测摘要端点采用同一层级定义。 |
| TERM-06 | 把“门、准入、假置信、打开 test”等流程词改为“预设合格标准”“基于预设绝对阈值的模拟恢复检验”“错误高置信判断检验”“观测桥接合格标准”“不开放最终测试”等标准研究语言。 |
| REG-01 | 将“封印、防火墙、挽救、闭合、降级”等运行手册式表达改为“独立保留、变量角色隔离、不改变判定、证据链连接、采用预设简单模型或缩小主张”。 |
| REG-02 | 用具体的评价对象、阈值与后果替代“真正、绝对门、强制、永不”等强调性表达，同时保留不可放宽阈值和不得越过设计边界的原意。 |
| CON-01 | 删除跨章节成组重复的限制和停止条件；在第 14 节保留一次完整权威版本。预期输出和解释矩阵只陈述其独有功能。 |
| CON-02 | 将斜线并列和连续名词链改为“以及”“或”“分别”及完整中心词；条件改为后置从句或列表，保留原逻辑关系。 |
| READ-01 | 一语摘要改为一条结构清楚的完整 Idea 摘要；详细试验分支和禁止性清单后置到相应方法与第 14 节。 |
| READ-02 | 主要研究问题改为一个总问题和两个顺承子问题，目标和核心假设分别陈述；在试验公式前增加资料核验、共同指标、预定映射、外部检验、组间比较和替代分析的普通语言路线。 |

资源状态表中的 reader-facing 状态全部改为“已核验数据库存在与版本”“尚未核验”“尚未生成”“项目本地衍生证据”等自然中文；主张支持表使用“得到支持”“有条件支持”“不支持”等自然状态说明，并在主张单元格本身限定支持范围。

## Protected-content dispositions

| Protected item | Required disposition | v006 disposition | Preserved location and content |
|---|---|---|---|
| PCR-001 | retained_same_meaning | retained_same_meaning | frontmatter identity_anchor、第一节定义和第四节主要研究问题保留以脓毒症为中心、覆盖未发病在险时段、首次发病、发病后状态演化和结局的候选动态系统表征；未改为普通预测或泛 ICU 风险分层。 |
| PCR-002 | retained_same_meaning | retained_same_meaning | frontmatter primary_objective、第一节摘要、第四节目标和第五节时间表保留 24 个月完成阶段 I–II，以知识约束、公共 ICU 数据、系统辨识和跨数据库验证形成可审计科学证据与论文方向。 |
| PCR-003 | retained_same_meaning | retained_same_meaning | frontmatter study_object 与 primary_unit_of_inference，以及第四、七节保留纵向脓毒症中心 ICU 系统、可比较未发病在险时段、发病后轨迹、患者—时间状态和状态转移，并保留患者与医院聚类。 |
| PCR-004 | retained_same_status | retained_same_status | 第六节资源状态表和数据库审计完整保留文献与专家先验、MIMIC-IV、eICU-CRD、HiRID 或 AmsterdamUMCdb 的角色；数据库存在与版本已核验，但访问、数据使用协议、提取、项目队列支持、具名人员和模型结果仍为尚未核验或尚未生成。 |
| PCR-005 | retained_same_status | retained_same_status | 第六、七和十四节明确 EXIT-SEP 与 XBJ-SCAP 仅为条件性阶段 III 数据来源，现有材料是项目本地衍生报告，不能替代个体数据授权、原始 CRF/SAP、随机化、中心、访视和生存住院语义核验。 |
| PCR-006 | retained_same_meaning | retained_same_meaning | 第五节固定完整顺序，第七节保留患者状态、治疗行动和测量过程分离，以及锚定、对齐、恢复、外部可迁移性和弃权约束；没有增加或选择未批准方法。 |
| PCR-007 | retained_same_meaning | retained_same_meaning | 第五节合取成功定义、第七节外部验证设计和第十四节风险表保留数据支持、模拟恢复、两项主要任务 proper score 与校准、泄漏清除、不更新参数外部表现、状态对齐及符号稳定的全部条件；适配后分析与主要验证分开，阶段 III 不补足阶段 II。 |
| PCR-008 | retained_same_meaning | retained_same_meaning | 第七节两项主要任务表和互斥状态表完整保留事件与信息可用双时钟、首次发病风险集、延迟进入、竞争终止、as-of 特征、校准与 proper score、患者与医院聚类不确定性和全部泄漏防护。 |
| PCR-009 | retained_same_strength | retained_same_strength | 第一、二、十一、十二和十三节持续使用计划时态；明确没有现成模型、模拟、外部验证或新试验分析结果。贡献仍限于条件性的整合、验证和基准或资源增量；单项模块已有先例，完整组合缺口为低至中等置信，不主张全球首次或新算法。 |
| PCR-010 | retained_once_at_authority_location | retained_once_at_authority_location | 第十四节一次性完整保留访问与人员、数据支持、标签与泄漏、可恢复性、非随机缺失与行动重叠、外部可迁移性、时间、试验数据与语义、共同锚点、观测桥接及最接近工作不确定性，并逐项保留触发条件、替代方案和停止后果。其他章节没有完整限制清单或跨节指针。 |
| PCR-011 | retained_once_at_authority_location | retained_once_at_authority_location | 第十四节末完整规定阶段 I–II 的 24 个月期限、阶段 III 的成功与资料前提、试验结果不能改变阶段 II 失败且不能越过资源、恢复、主要任务和独立外部验证要求。第五节只保留研究范围与日期安排的独有功能。 |
| PCR-012 | retained_same_boundary | retained_same_boundary | 第四节保留研究目标的最小非因果边界；第十四节完整规定观察性数据和预测不识别因果网络、治疗作用、反事实策略、机制、中介或控制，试验分析不验证潜在动力学、转移边或整个系统，并排除已验证模型、临床工具、数字孪生、可控系统、药物平台及无条件推广主张。 |

## Structural and lineage changes

- dossier 仍为一个完整 Idea，保留 15 个必需 H2；第三节包含且仅包含五个必需 H3，顺序不变。
- 五条证据链各含且仅含 Input、Method / analysis / processing、Output、Supports 四个字段。
- 第 14 节为限制、工作假设、风险、替代方案和停止条件的唯一完整权威位置；其他章节未增加跨节指针。
- v006 frontmatter 使用 active plugin version 0.9.0-preview.3、非空 path、change_type editorial_repair，并以四个 `{artifact_id, version, path}` 映射记录全部授权输入。
