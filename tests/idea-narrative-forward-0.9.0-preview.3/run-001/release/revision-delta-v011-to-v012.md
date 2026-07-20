---
schema_version: research-idea-revision-delta.v1
plugin_version: 0.9.0-preview.3
artifact_id: revision-delta-I01-001-v011-to-v012
workflow_id: RID-SEPSIS-CSM-20260717-001
idea_id: I01-001
version_id: v011-to-v012
path: tests/idea-narrative-forward-0.9.0-preview.3/run-001/release/revision-delta-v011-to-v012.md
based_on:
  - artifact_id: idea-dossier-I01-001-v011
    version: v011
    path: tests/idea-narrative-forward-0.9.0-preview.3/run-001/release/idea-dossier-v011.md
  - artifact_id: narrative-repair-plan-I01-001-r009
    version: r009
    path: tests/idea-narrative-forward-0.9.0-preview.3/run-001/release/narrative-repair-plan-r009.yaml
  - artifact_id: language-assessment-I01-001-r009
    version: r009
    path: tests/idea-narrative-forward-0.9.0-preview.3/run-001/release/language-assessment-r009.md
  - artifact_id: protected-content-register-I01-001-v011
    version: v011
    path: tests/idea-narrative-forward-0.9.0-preview.3/run-001/release/protected-content-register-v011.yaml
source_skill: multi-path-idea-generator
created_round: 9
change_type: editorial_repair_delta
---

# Revision delta: idea dossier v011 to v012

## Scope

本轮仅执行 LANG-001 至 LANG-005 所要求的语言修订。研究身份、问题、对象、证据基础、推断单位、科学方法、数据、阈值、估计目标、验证顺序、主张强度、可行性状态、条件性与停止后果均未改变。

## Editorial changes

1. Claim-Support 表及其图例仅保留自然中文的贡献类型和支持状态；“验收”“签署”等内部管理措辞改为具体的科学输出、核验记录或独立数据保管人核验要求。
2. Section 14 新设一份完整的“Working assumptions and pending specifications”清单。清单逐项覆盖医院规模分层指标、主要任务 95% 上置信限构造、临床尺度到模拟参数的映射、多类别校准估计量和依赖双数据库审计的阈值登记表，并分别说明待选对象、已固定内容、决定时点与可用信息、未解决后果。可行性表仅报告这五项的对应状态。
3. 摘要、按医院开展的跨数据库验证和高密度条件表述改为一个主要动作配一组直接条件的短句；原有数据隔离、时间边界、失败后果和禁止替代规则均保留。
4. 修正月 21–24 产物的并列层级、医院规模指标修饰范围，以及观测映射分析中“主要结局状态”的标签。
5. 首次使用时写作“蒙特卡洛（Monte Carlo）”“蒙特卡洛标准误（MCSE）”和“D-二聚体（D-dimer）”，后文分别统一为“蒙特卡洛”“MCSE”和“D-二聚体”。

## Protected-content dispositions

下表逐项记录 72 个受保护项目在 v012 中的处置。处置用自然中文表述，并与登记表要求一一对应。

| 受保护项目 | 要求 | v012 实际处置 | 主要保留位置 |
|---|---|---|---|
| PCR-001 | 保留原意 | 已保留原意 | Research question；frontmatter identity anchor |
| PCR-002 | 保留原意 | 已保留原意 | Structured abstract；三阶段导航 |
| PCR-003 | 保留原主张强度 | 已保留原主张强度及全部条件 | Core hypothesis |
| PCR-004 | 保留原主张强度 | 已保留有界整合、验证、基准与资源定位 | Section 1；Contribution and evidence ladder |
| PCR-005 | 保留原边界 | 已保留原研究身份边界 | Section 14 > Research identity and final boundary |
| PCR-006 | 保留原意 | 已保留研究对象与主要推断单位 | frontmatter identity anchor；研究问题 |
| PCR-007 | 保留原边界 | 已保留三阶段范围与 24 个月最低交付边界 | 三阶段导航；work packages |
| PCR-008 | 保留原边界 | 已保留发病前与发病后人群边界 | Protocol locks > 人群 |
| PCR-009 | 保留原边界 | 已保留互斥状态、优先级及终止处理 | Mutually exclusive post-onset state and event system |
| PCR-010 | 保留原边界 | 已保留数据库、模型与分析范围 | Section 14 > Feasibility and resources |
| PCR-011 | 保留原边界 | 已保留医院分层、固定种子、30%/70% 分组及分开报告要求 | Hospital-based cross-database validation；Section 14 待冻结规范 |
| PCR-012 | 保留原边界 | 已保留两试验分开分析、人群、降级条件与访视 | Analysis targets |
| PCR-013 | 保留原边界 | 已保留四类证据分别报告且不得互相替代 | Section 1；Interpretation of the planned evidence |
| PCR-014 | 保留原意 | 已保留 MIMIC-IV、eICU 与备份数据库角色 | Public ICU databases and planned roles |
| PCR-015 | 保留原意 | 已保留共同概念纳入条件与双数据库审计范围 | Public ICU databases and planned roles；审计表 |
| PCR-016 | 保留原状态 | 已保留已核验、未核验和尚未生成的区别 | Section 14 > Current feasibility and evidence status |
| PCR-017 | 保留原状态 | 已保留两项试验的全部样本与缺失计数 | Trial data considered for conditional stage III analyses |
| PCR-018 | 保留原意 | 已保留文献、专家先验、公共 ICU 数据和条件性试验数据组成 | frontmatter identity anchor；Evidence chains |
| PCR-019 | 保留原意 | 已保留五类变量角色分离规则 | Variable-role separation |
| PCR-020 | 保留原状态 | 已保留人员角色已定义但具名人员与工时未核验 | Section 14 > Feasibility and resources；feasibility table |
| PCR-021 | 保留原意 | 已保留阶段 III 授权、原始文件与语义核验条件 | Trial semantics and common-observation eligibility |
| PCR-022 | 保留原状态 | 已保留本地材料局限、共同指标未核验与字段禁止推测边界 | Section 14 > Current feasibility and evidence status |
| PCR-023 | 保留原意 | 已保留发病前估计目标、模型与全部评价指标 | Protocol locks > 主要发病前任务 |
| PCR-024 | 保留原意 | 已保留发病后估计目标、模型、时间点与评价指标 | Protocol locks > 主要发病后任务 |
| PCR-025 | 保留原意 | 已保留感染配对、SOFA 基线、时间窗、事件时间与可用时间 | Protocol locks > 事件时间；信息可用时间 |
| PCR-026 | 保留原意 | 已保留竞争事件、同窗排序、两种敏感性标签和泄漏检查 | Protocol locks；紧随表格的敏感性定义 |
| PCR-027 | 保留原意 | 已保留恢复、恶化和持续脓毒症操作定义 | Mutually exclusive post-onset state and event system |
| PCR-028 | 保留原意 | 已保留联合分布、变量含义与模型输出 | Observational model target, anchoring, and reporting |
| PCR-029 | 保留原意 | 已保留锚点、维度、机制、滞后、结构与 20 个种子约束 | Observational model target, anchoring, and reporting |
| PCR-030 | 保留原意 | 已保留两类缺失基线、偏移值、临界点和重叠报告 | Observational model target, anchoring, and reporting |
| PCR-031 | 保留原意 | 已保留蒙特卡洛与半合成模拟的隔离条件、情景因素和评价范围 | Simulation and semi-synthetic recovery study |
| PCR-032 | 保留原意 | 已保留跨医院患者处理的四步顺序和敏感性规则 | Hospital-based cross-database validation |
| PCR-033 | 保留原意 | 已保留三层外部分析顺序和全模型重拟合定性 | Hospital-based cross-database validation |
| PCR-034 | 保留原意 | 已保留阶段 II 成功所需五类证据及全满足条件 | Minimum success definition |
| PCR-035 | 保留原意 | 已保留阶段 III 启动条件、共同变量资格和禁止重估权重 | Trial semantics and common-observation eligibility |
| PCR-036 | 保留原意 | 已保留标准化、截断、SVD 映射、选轴、符号及试验分离 | Pre-specified deterministic observation mapping |
| PCR-037 | 保留原意 | 已保留映射忠实度的全部九项失败阈值与禁止调参 | External projection fidelity assessment；Section 14 thresholds |
| PCR-038 | 保留原意 | 已保留结局排序、概率指数、独立 SOFA、缺失处理、Holm 家族与亚组限制 | Analysis targets |
| PCR-039 | 保留原意 | 已保留两项次要表征诊断及其全部评价与分层 | Secondary representation diagnostics |
| PCR-040 | 保留原意 | 已保留患者与医院层级区间、权重、分层和转移数 | Protocol locks > 不确定性 |
| PCR-041 | 保留原意 | 已保留模拟重复、MCSE、恢复、覆盖、结构与错设全部阈值 | Section 14 > Risks, alternatives, and stop conditions |
| PCR-042 | 保留原意 | 已保留校准、Brier、种子、自助法、符号一致与对齐阈值 | Section 14 > Risks, alternatives, and stop conditions |
| PCR-043 | 保留原意 | 已保留事件、转移、锚点、覆盖、医院与跨分区阈值 | Section 14 > Risks, alternatives, and stop conditions |
| PCR-044 | 保留原主张强度 | 已保留所有产物均为计划或拟生成结果的状态 | Structured abstract；Planned outputs；feasibility table |
| PCR-045 | 保留原主张强度 | 已保留一个有界支持定位与三个限定支持定位 | Title and positioning claim-support table |
| PCR-046 | 保留原主张强度 | 已保留逐估计对象报告及五层证据完整记录要求 | Interpretation of the planned evidence；Contribution ladder |
| PCR-047 | 保留原主张强度 | 已保留两类试验分析的次要或探索性性质与解释范围 | Conditional trial analyses；Section 14 boundaries |
| PCR-048 | 保留原主张强度 | 已保留模块先例高置信与组合缺口低至中等置信 | Representative closest-work comparison；feasibility table |
| PCR-049 | 保留原状态 | 已把全部五项尚待冻结规范完整列于唯一清单 | Section 14 > Working assumptions and pending specifications |
| PCR-050 | 仅在权威位置保留一次 | 已在 Section 14 的唯一完整清单保留医院指标与上置信限规范 | Section 14 > Working assumptions and pending specifications |
| PCR-051 | 仅在权威位置保留一次 | 已保留数据、人员、时间方案、降维、备份与停止后果 | Section 14 > Risks, alternatives, and stop conditions |
| PCR-052 | 仅在权威位置保留一次 | 已保留阈值登记依据、时间、只能收紧和补齐要求 | Section 14 > Working assumptions；Risks and stop conditions |
| PCR-053 | 仅在权威位置保留一次 | 已保留不达阈值后的降级、淘汰与禁止替代后果 | Section 14 > Risks, alternatives, and stop conditions |
| PCR-054 | 仅在权威位置保留一次 | 已保留高严重度泄漏的修正要求及外部结果访问限制 | Section 14 > Risks, alternatives, and stop conditions |
| PCR-055 | 仅在权威位置保留一次 | 已保留缺失敏感、行动发生率、有效样本量与解释停止条件 | Section 14 > Risks, alternatives, and stop conditions |
| PCR-056 | 仅在权威位置保留一次 | 已保留主要任务失败、不更新验证优先和有限更新解释边界 | Section 14 > Risks, alternatives, and stop conditions |
| PCR-057 | 仅在权威位置保留一次 | 已保留独立核验、备份数据库、降级及命名限制 | Section 14 > Risks, alternatives, and stop conditions |
| PCR-058 | 仅在权威位置保留一次 | 已保留月 12、20、24 的封存、禁止访问和未完成后果 | Section 14 > Risks, alternatives, and stop conditions |
| PCR-059 | 仅在权威位置保留一次 | 已保留试验语义、锚点、映射忠实度与 SOFA 分支停止条件 | Section 14 > Risks, alternatives, and stop conditions |
| PCR-060 | 仅在权威位置保留一次 | 已保留方向、区间、Holm、缺失敏感、亚组与禁止合并边界 | Section 14 > Risks, alternatives, and stop conditions |
| PCR-061 | 仅在权威位置保留一次 | 已保留 12 小时方案、动态测量处理和稀疏访视不插值边界 | Section 14 > Limitations and boundary conditions |
| PCR-062 | 仅在权威位置保留一次 | 已保留 XBJ-SCAP 人群、缺失字段及 D-二聚体单位边界 | Section 14 > Limitations and boundary conditions |
| PCR-063 | 保留原边界 | 已保留观察性关联与预测不识别因果、网络或反事实策略 | Section 14 > Limitations and boundary conditions |
| PCR-064 | 保留原边界 | 已保留试验分支与独立 SOFA 不支持的主张类别 | Section 14 > Limitations and boundary conditions |
| PCR-065 | 保留原边界 | 已保留算法、首次、全球不存在、专利、数字孪生和控制主张限制 | Section 14 > Limitations；Risks and stop conditions |
| PCR-066 | 保留原边界 | 已保留临床工具、药物平台、国际推广与监管边界 | Section 14 > Limitations；Risks and stop conditions |
| PCR-067 | 保留原边界 | 已保留有限更新不能替代不更新外部验证及重拟合定性 | Section 14 > Limitations and boundary conditions |
| PCR-068 | 保留原边界 | 已保留阶段 III 不补足阶段 II 失败且不改变其成败 | Section 14 > Limitations and boundary conditions |
| PCR-069 | 保留原边界 | 已保留禁止推测字段、单位、访视语义和连续轨迹 | Section 14 > Limitations；Risks and stop conditions |
| PCR-070 | 保留原边界 | 已保留两试验不得合并、亚组不得改结论且只报告交互 | Section 14 > Risks, alternatives, and stop conditions |
| PCR-071 | 保留原边界 | 已保留尚未生成工作不支持完成性或结果主张 | Structured abstract；Planned outputs；feasibility table |
| PCR-072 | 保留原边界 | 已保留有界检索非系统综述及未覆盖来源的完整限制 | Representative closest-work comparison；Section 14 limitations |

## Files written

- `idea-dossier-v012.md`
- `revision-delta-v011-to-v012.md`
