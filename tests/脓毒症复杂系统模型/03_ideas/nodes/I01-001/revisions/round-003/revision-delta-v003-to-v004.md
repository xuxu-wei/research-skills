---
schema_version: research-idea-revision-delta.v1
plugin_version: "0.10.0"
artifact_id: revision-delta-I01-001-v003-to-v004
workflow_id: sepsis-complex-system-idea-generation-v001
idea_id: I01-001
version_id: v003-to-v004
change_type: editorial_repair_delta
source_artifact:
  artifact_id: idea-dossier-I01-001-v003
  version: v003
  path: 03_ideas/nodes/I01-001/dossiers/idea-dossier-v003.md
revised_artifact:
  artifact_id: idea-dossier-I01-001-v004
  version: v004
  path: 03_ideas/nodes/I01-001/dossiers/idea-dossier-v004.md
writer_brief:
  artifact_id: editorial-repair-writer-brief-I01-001-r001
  version: r001
  path: 03_ideas/nodes/I01-001/revisions/round-003/editorial-repair-writer-brief-r001.yaml
protected_content_register:
  register_id: protected-content-register-v001
  version: v001
  path: 05_state/protected-content-register-v001.yaml
---

# Editorial repair delta: v003 to v004

v004 是对 v003 的一次集中 editorial-only repair。完整 v004 经检查并冻结后才创建本记录；未生成片段稿或中间 delta，也未计算、请求、报告或保存内容哈希、摘要、校验和或时间戳。

## Repair-action execution

| Repair item | Revised locator | Executed operation | Text-grounded acceptance result |
|---|---|---|---|
| NRP-001 | Abstract；interpretations；contribution；claim-support table；limitations | consolidate | 十一项完整限制集中在限制小节；摘要与贡献恢复正向功能，解释表仅保留相邻结果所需边界，支持表不复写限制。 |
| NRP-002 | Conditional follow-up；opening；work packages；inputs；resources；limitations；stops | consolidate | 随机试验与动物研究的完整启动、解释和不可补救逻辑只在专门方法小节成组出现；其他位置仅留局部功能所需事实。 |
| NRP-003 | opening；abstract；rationale；work packages；inputs；evidence chains；contribution；feasibility | replace | 正文改用“建模前文献—专家约束”“12–18 个月核心实证研究”“四项预定验证任务”“条件性后续研究”；无“用户”目标来源或裸阶段编号。 |
| LANG-001 | Abstract objective；Significance；research question；H3；interpretations | replace | 任务三统一为“部分观测下的临床测量值预测”；H3 保留全部既定对象、遮蔽、评分、权重和金标准边界。 |
| LANG-002 | Abstract approach；objectives；work package 2；complexity；techniques；chains；analyses；outputs；stops | define | 首用写明检验参数和潜在状态能否可靠恢复；后文统一为“参数与潜在状态恢复诊断”，患者事件仍称“持续恢复”。 |
| LANG-003 | Task hypotheses；technique 6；limitation 8 | replace | 统一“目标值被观测的概率”“逆观测概率权重”“逆删失概率权重”；全部权重规则不变。 |
| LANG-004 | Confirmatory family；task table；methods；chains；analyses | define | 首用“预定预测起始时点（landmark）”定义风险集、信息截断和时域起点；后文仅用中文。 |
| LANG-005 | Abstract expected result | replace | 改为“四项分别报告且互不替代的任务级比较结果”；Holm 家族和分别判定不变。 |
| LANG-006 | Required inputs opening and database table | replace | 使用平行资格句；开发库行明确患者级标识与事件记录通过资格审计，未把未确认状态写成已满足。 |

## Protected-content register receipt

| ID | Revised locator(s) | Item-level preservation evidence | Disposition |
|---|---|---|---|
| PCR-001 | Research question；identity_anchor | 人群、统一模型、两库、四任务、迁移问题均在；仅修订任务三读者措辞 | retained_same_meaning |
| PCR-002 | Objectives 1–4 | 资格、开发冻结、外部四任务、迁移与范围限定逐项保留 | retained_same_meaning |
| PCR-003 | Opening definitions | 全病程、同一状态空间、四定义、冻结外部应用均在 | retained_same_meaning |
| PCR-004 | Full-course population/time/state | 起止、未发病者、首次发生、重复住院同分割、五类组成均在 | retained_same_meaning_at_method_authority |
| PCR-005 | Opening；conditional follow-up；stops | 12–18 个月核心、后续非必需及不得改写核心失败均在 | retained_same_meaning |
| PCR-006 | Pre-model constraint prerequisite | 字段、角色、转移、专家构成、80% 规则、异议保存均在 | retained_same_meaning_at_input_authority |
| PCR-007 | Required inputs | 两库、未确认状态、预登记选择、无表现驱动换库均在 | retained_same_meaning_at_input_authority |
| PCR-008 | Database/team/compute；assumptions | 样例项目、五角色、计算实测与不得假设替代均在 | retained_same_meaning_at_input_authority |
| PCR-009 | Inputs；WA-02 | 第三库仅压力测试；试验数据仅条件性后续且未核实 | retained_same_meaning_at_input_authority |
| PCR-010 | Full-course population/time/state | 持续恢复、24 小时、后续恶化、出 ICU 区分、真实时间与网格均在 | retained_same_meaning_at_method_authority |
| PCR-011 | Primary model/comparators | 隐半马尔可夫结构、观测过程、治疗输入角色、八比较模型及共同评分均在 | retained_same_meaning_at_method_authority |
| PCR-012 | Confirmatory family | 四原假设、患者内汇总、最不利差、max-t、上界、Holm 与双侧区间均在 | retained_same_meaning_at_method_authority |
| PCR-013 | H1 | 起始点、风险集、四结局、三时域、损失、比较与判定均在 | retained_same_meaning_at_method_authority |
| PCR-014 | H2 | 五起始点、风险集、四事件、绝对时域、比较与判定均在 | retained_same_meaning_at_method_authority |
| PCR-015 | H3 | 六器官域、三支持、12 小时遮蔽、真实目标、评分、权重、比较、校准均在 | retained_same_meaning_at_method_authority |
| PCR-016 | H4 | 起始点、风险集、四时域、可观测组成、吸收编码、比较与判定均在 | retained_same_meaning_at_method_authority |
| PCR-017 | Weighting paragraphs | 基础权重、逆删失/观测权重、归一化、冻结、截止信息、聚类、敏感性均在 | retained_same_meaning_at_method_authority |
| PCR-018 | Complexity；development；stops | 模拟诊断、阈值冻结、四步简化与最小模型失败后果均在 | retained_same_meaning_at_method_authority |
| PCR-019 | External application/state transfer | 冻结对象、无外部重估、锚定、迁移/合并/拆分、观测过程单列均在 | retained_same_meaning_at_method_authority |
| PCR-020 | External application/state transfer | 必需状态定义、迁移失败、任务可执行性和部分支持均在 | retained_same_meaning_at_method_authority |
| PCR-021 | Multiplicity/interpretation | 并行任务、10,000 次、Holm 顺序、总体/部分/失败、有限校准均在 | retained_same_meaning_at_method_authority |
| PCR-022 | Work packages | 月 1–2、3–6、7–12、13–18 活动交付、第三库单列、后续不入时表均在 | retained_same_meaning_at_method_authority |
| PCR-023 | Conditional follow-up | EXIT-SEP 资格、分配治疗解释、XBJ-SCAP 适配及不可改写核心失败均在 | retained_same_meaning_at_method_authority |
| PCR-024 | Conditional follow-up | 人类证据触发、机制、平台/伦理/样本量、MQTiPSS/ARRIVE、动物边界均在 | retained_same_meaning_at_method_authority |
| PCR-025 | Evidence base；limitation 1 | 代表性依据保持；新颖性/完整性不支持集中至限制权威 | retained_same_strength |
| PCR-026 | Abstract；limitations 5–7 | 产物均为预期；可证伪贡献与不支持主张完整保留 | retained_same_strength |
| PCR-027 | Contribution；limitations 1,5–7 | 三项贡献不变；首创、生物实体、效用和因果边界集中保留 | retained_same_strength |
| PCR-028 | Interpretations；limitations 5–7 | 六种结果模式均在；成功模式保留不推断真实状态/因果的局部边界 | retained_same_strength |
| PCR-029 | WA-01 | 论文组织假设、核心不变、月 3 验证和不成立后果均在 | retained_same_meaning_at_assumption_authority |
| PCR-030 | WA-02 | 第三库时机、不入 Holm/总体/月12、资格不足取消均在 | retained_same_meaning_at_assumption_authority |
| PCR-031 | Limitation 1 | 有界检索、全部新颖性禁限及 2026 复核均在 | retained_not_weakened |
| PCR-032 | Limitation 2 | 访问、样例、字典、共同变量和信息量未确认均在 | retained_not_weakened |
| PCR-033 | Limitation 3 | 跨库人群、实践、语义、采样、结局与差异来源均在 | retained_not_weakened |
| PCR-034 | Limitation 4 | 入口、标签、索引、时域、恢复定义与敏感性均在 | retained_not_weakened |
| PCR-035 | Limitation 5 | 观察性混杂及边、权重、治疗系数全部非因果边界均在 | retained_not_weakened |
| PCR-036 | Limitation 6 | 无潜在状态金标准及锚定、任务、重建三类边界均在 | retained_not_weakened |
| PCR-037 | Limitation 7 | 适用范围及效用、真实世界、部署等边界均在 | retained_not_weakened |
| PCR-038 | Limitation 8 | 三个规范概率/权重名、冻结历史、极端权重与残余偏倚均在 | retained_not_weakened |
| PCR-039 | Limitation 9 | 试验数据/变量/功效未核实、重叠风险和中介边界均在 | retained_not_weakened |
| PCR-040 | Limitation 10 | 动物机制、平台、样本量、伦理、预算、转化冲突、非外部验证均在 | retained_not_weakened |
| PCR-041 | Limitation 11 | 约束、团队、计算未完成；核心时间范围与后续无承诺均在 | retained_not_weakened |
| PCR-042 | Stop row 1 | 月2两库失败、盲于表现的替代顺序和停止均在 | retained_not_weakened |
| PCR-043 | Stop row 2 | 约束缺项响应、禁止代填和月2停止均在 | retained_not_weakened |
| PCR-044 | Stop row 3 | 团队/计算不足的削减顺序和核心不足停止均在 | retained_not_weakened |
| PCR-045 | Stop row 4 | 不可恢复的四步简化、重跑诊断和最小模型后果均在 | retained_not_weakened |
| PCR-046 | Stop row 5 | 迁移失败、禁止重定义/强配、完整失败与其他最多部分支持均在 | retained_not_weakened |
| PCR-047 | Stop row 6 | 未通过任务继续报告、其他检验不变和全部不可补救分支均在 | retained_not_weakened |
| PCR-048 | Stop row 7 | 复现失败时暂停、核查及仍失败时的提交禁限均在 | retained_not_weakened |
| PCR-049 | Limitation 1 | 首个、完整、无人研究、完整人体系统、首次动态状态方法均明确不支持 | retained_as_explicitly_unsupported |
| PCR-050 | Limitation 5 | 边、权重、治疗系数仅作预测关联，因果/治疗/中介类别明确不支持 | retained_as_explicitly_unsupported |
| PCR-051 | Limitations 6–7 | 真实状态、效用、真实世界、部署、治疗、机制、监管均明确不支持 | retained_as_explicitly_unsupported |
| PCR-052 | Conditional follow-up；stop row 6 | RCT/动物不可改写核心任务；分配不识别中介；动物不作外部验证 | retained_as_explicitly_unsupported |

identity_anchor 的五个值从 v003 逐字、同序复制。PCR-031…041 已在唯一完整限制权威位置逐项重开；PCR-042…048 已在停止条件表逐项重开。随机试验与动物研究的资格和后果仍分别适用，未把一个分支的前提提升为共同前提。

## Reader-facing role concordance

| Role | One reader-facing name | First use | Competing forms removed/reclassified | All-occurrence result |
|---|---|---|---|---|
| central object | 受约束的脓毒症全病程动态状态模型 | H1/Title | “人体开放复杂巨系统”仅作操作化视角 | 标题、摘要、问题、贡献一致 |
| primary question/task | 构建并跨库验证统一全病程模型 | Summary | 删除“用户目标”来源措辞 | 问题、目标、方法一致 |
| primary outcome | 四项分别判定且互不替代的患者级损失差 | Abstract expected result | 删除“相互独立” | Confirmatory family、H1–H4、Holm 一致 |
| contribution | 方法整合、外部验证和失效边界证据 | Abstract contribution | 完整否定清单移至限制权威 | 摘要、贡献、支持表一致 |
| task-three target | 部分观测下的临床测量值预测 | Abstract objective | 删除 reader-facing 状态估计竞争形式 | 问题、H3、解释表一致 |
| model recovery | 参数与潜在状态恢复诊断 | Abstract approach | 含混简称均加对象 | 开发、技术、证据链、分析、产物、停止一致 |
| missingness weighting | 逆观测概率权重与逆删失概率权重 | Task-hypothesis opening | 删除概率/权重层级混用 | 权重规则、H3、技术、限制一致 |
| prediction origin | 预测起始时点 | Confirmatory family | landmark 仅首用括注 | H1–H4、比较、证据链、实施一致 |

## Deterministic checks and scanner receipt

- Exact structural lint for plugin 0.10.0 在最终冻结稿上重跑并 exited 0；唯一 advisory 是 brief 要求的首用中文定义括注 landmark。
- Reader-facing short-form diff 的 new-reader-facing-short-form 为空。
- 五项 identity_anchor 内容及顺序在 v003 与 v004 间相同。
- git diff --check 对 v004 无错误。

Scanner 每个候选的唯一处置如下：

| Candidate(s) | Disposition | Locator/rationale |
|---|---|---|
| reader-entry lines 37,41 | retained-and-clear | H1 与 Title 精确一致 |
| reader-entry line 42 | retained-and-clear | Summary 自足说明对象、输入、模型、验证、贡献 |
| reader-entry line 43 | retained-and-clear | Audience 明确 |
| reader-entry line 44 | retained-and-clear | Positioning 正向且四任务结构清楚 |
| reader-entry line 46 | defined | 五个核心词均原位定义 |
| reader-entry line 48 | retained-and-clear | 核心与条件后续的最小范围句 |
| reader-entry line 52 | retained-and-clear | 标准背景与证据缺口 |
| reader-entry line 53 | replaced | 任务三改为临床测量值预测 |
| reader-entry line 54 | defined | 参数与潜在状态对象明确 |
| reader-entry line 55 | replaced | 删除统计独立性暗示 |
| reader-entry line 56 | retained-and-clear | 正向计划贡献 |
| 动态状态模型、全病程、受约束、外部验证（line 46） | defined | 均有即时自然语言定义 |
| 人体开放复杂巨系统（line 46） | replaced | 改作操作化视角而非既定类别 |
| Singer；Klouwenberg；Raghu；Sauer；et；al（所报行） | not-reader-facing | 引文作者/缩写组成 |
| Holm（所报行） | retained-and-clear | 标准命名程序且规则完整 |
| D_；Delta_；H_（line 84 及后续） | defined | 同句定义后全篇一致 |
| max_（line 84） | retained-and-clear | 定义内标准最大值运算符 |
| s00134-026-08361-1；1.1.1；1.0.8；bmj-2023-078378；bmj-2024-082505 | not-reader-facing | 参考文献 DOI、版本或 URL 标识 |

## Scientific-scope disposition

未遇到需要科学选择才能解决的问题。研究对象、四任务、人群、数据库、时间轴、事件、比较模型、权重、推断、阈值、证据状态、假设、资源、主张和分支逻辑均保持 v003 与 PCR-001…052 的内容；差异仅来自九项规范化编辑动作，没有新增数据、方法、结果、证据、更强主张或已完成暗示。
