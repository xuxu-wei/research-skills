---
review_id: preflight-r003
reviewer_skill: methodology-statistics-preflight
reviewer_instance_id: fresh-methodology-statistics-preflight-r003
workflow_id: sepsis-complex-system-idea-generation-v001
round_id: r003
input_artifact_ids:
  - idea-dossier-I01-001-v003
input_versions:
  - v003
files_read:
  - research-skills/research/methodology-statistics-preflight/SKILL.md
  - research-skills/research/methodology-statistics-preflight/references/preflight-schema.md
  - research-skills/research/methodology-statistics-preflight/references/endpoint-metric-checks.md
  - research-skills/research/methodology-statistics-preflight/references/data-method-fit-rules.md
  - research-skills/research/methodology-statistics-preflight/references/minimal-analysis-route-rules.md
  - research-skills/research/methodology-statistics-preflight/references/feasibility-blockers.md
  - research-skills/research/methodology-statistics-preflight/references/domain-specific-checks.md
  - research-skills/research/methodology-statistics-preflight/references/downstream-handoff-rules.md
  - research-skills/research/methodology-statistics-preflight/templates/template-methodology-statistics-preflight-report.md
  - research-skills/research/methodology-statistics-preflight/templates/template-preflight-failure-report.md
  - research-skills-openai/skills/methodology-statistics-preflight/SKILL.md
  - research-skills-openai/skills/methodology-statistics-preflight/references/preflight-schema.md
  - research-skills-openai/skills/methodology-statistics-preflight/references/endpoint-metric-checks.md
  - research-skills-openai/skills/methodology-statistics-preflight/references/data-method-fit-rules.md
  - research-skills-openai/skills/methodology-statistics-preflight/references/minimal-analysis-route-rules.md
  - research-skills-openai/skills/methodology-statistics-preflight/references/feasibility-blockers.md
  - research-skills-openai/skills/methodology-statistics-preflight/references/domain-specific-checks.md
  - research-skills-openai/skills/methodology-statistics-preflight/references/downstream-handoff-rules.md
  - research-skills-openai/skills/methodology-statistics-preflight/references/working-assumption-rules.md
  - research-skills-openai/skills/methodology-statistics-preflight/templates/template-methodology-statistics-preflight-report.md
  - research-skills-openai/skills/methodology-statistics-preflight/templates/template-preflight-failure-report.md
  - tests/脓毒症复杂系统模型/03_ideas/nodes/I01-001/dossiers/idea-dossier-v003.md
isolation_mode: fresh_subagent
prior_scores_visible: false
source_edits_performed: false
decision: pass
findings:
  - PF-R003-01
  - PF-R003-02
  - PF-R003-03
  - PF-R003-04
  - PF-R003-05
unresolved_issues:
  - 数据库访问、字段可映射性、信息量、团队承诺和计算能力尚未实证通过，必须作为启动前置门核验。
---

# 方法学与统计学预审报告

## 1. 预审对象

- **输入类型：** idea
- **下游任务：** idea_evaluation
- **对象：** `idea-dossier-I01-001-v003`；逻辑引用为 `I01-001 / v003 / 03_ideas/nodes/I01-001/dossiers/idea-dossier-v003.md`。
- **审查范围：** 端点与指标、数据—方法匹配、最小分析路线、统一模型覆盖范围、四项任务级假设、多重性、外部冻结应用与状态迁移诊断、12–18 个月可行性及前置条件。
- **明确不在范围内：** 新颖性、影响力、总体研究价值及语言叙事质量。

## 2. 预审结论

- **一般结论：** `pass`
- **Idea 交接结论：** `proceed_with_assumptions`
- **理由：** v003 已给出可执行的统一全病程模型边界、四个且仅四个任务级主要推断目标、患者级汇总规则、比较模型、方向、置信界与 Holm 家族控制，并把外部模型应用和状态迁移诊断限定为结果盲的冻结路线。尚未证实的数据、团队和计算条件被正确保留为硬性前置门和停止条件，而非以假设代替。两项既有工作假设只影响成果组织和可选第三库，不改变核心问题、主要测量、推断目标或结论强度。

## 3. 端点与指标状态

- **状态：** `adequate`

### PF-R003-01：统一模型确实覆盖完整预定病程

- **类别：** `nonblocking_advice`
- 训练样本从冻结的感染风险入口开始；未发生脓毒症者继续贡献风险期与全病程信息，发生者经首次 Sepsis-3 事件进入发病后状态，并随访至持续恢复、恶化、存活出 ICU、死亡或删失。
- 状态空间、允许转移、训练样本和预测接口均覆盖“感染风险 → 首次发生 → 发病后演化”，索引后窗口仅用于任务评分，没有把主模型退化为索引后模型。
- 若最小统一模型不能同时恢复三个阶段的关键状态或转移，计划要求停止统一模型主张；因此覆盖声明可证伪，且不会由局部任务结果补救。

### PF-R003-02：四项任务各有唯一、可计算的主要目标

- **类别：** `nonblocking_advice`
- 每项任务先把所有预定 landmark、时域和结果组成汇总为每位患者一个标准化损失，再以相对全部冻结比较模型的最不利平均损失差 \(\Delta_k=\max_c D_{kc}\) 形成唯一原假设 \(H_{0k}:\Delta_k\ge 0\)。
- H1、H2、H3、H4 分别对应首次发生、死亡或持续恢复、部分观测下可观测临床量、后续全病程演化。H4 与 H1/H2 共享部分可观测事件，但其风险集、时域、结果向量和汇总目标不同，不构成同一任务内可择优的竞争主指标。
- 每项的结果编码、风险集、时域、评分规则、比较模型、方向和通过条件均已明确到足以编程实现；剩余数值阈值可在声明的开发期模拟或数据审计后按结果盲规则冻结。

### PF-R003-03：Holm 程序与任务执行顺序不冲突

- **类别：** `nonblocking_advice`
- 任务内以交并假设要求同时优于全部比较模型，并使用最大单侧配对检验 p 值及同时上置信界；四个有效任务级 p 值再共同进入 Holm step-down。
- 四项任务平行估计，不设预先的任务优先级，也不因某项结果停止其他任务。Holm 的阈值序列按观察到的 p 值排序使用；“并列时按任务编号”仅是确定性并列处理，不是固定顺序检验。因而原先可能出现的固定任务顺序与 Holm 排序冲突已消除。
- 同时要求任务级上置信界小于 0 和 Holm 调整后 p 值小于 0 属于较保守但可执行的双重通过规则，不产生结果依赖的指标选择。

## 4. 数据—方法匹配状态

- **状态：** `partially_adequate`

### PF-R003-04：外部冻结模型与状态诊断路线唯一

- **类别：** `nonblocking_advice`
- 开发完成后冻结模型参数、状态数与标签、标准化、变量映射、允许转移、任务代码、比较模型、权重及诊断规则；外部库只接收该冻结对象，不重新估计、命名或匹配潜在状态。
- 状态未迁移、合并和拆分均由开发期冻结的临床锚定分布、占用、距离和可分离规则判定，且不得使用验证结局修改。观测频率等测量过程指标与生理锚定分开，不能提高状态迁移判定。
- 该路线在 Idea 阶段已唯一。具体距离、最小占用、可分离阈值及拆分诊断算法可由开发数据的模拟、恢复诊断和内部试点结果盲地确定；无需在本阶段再发明数值阈值，但必须在接触外部结局或外部状态可分离结果前冻结。
- 数据—方法匹配仍为 `partially_adequate`，因为两库许可、共同变量、时间戳、事件数、有效转移和测量密度目前均未实证。dossier 已把这些条件设为不可用工作假设替代的前置门，处理方式正确。

## 5. 最小分析路线状态

- **状态：** `adequate`
- **最小路线：** 审计并冻结两库共同变量和完整病程标签；在开发结构下用模拟与恢复诊断确定可辨识的最小统一隐半马尔可夫模型；冻结模型、四项任务和全部比较规则；在外部库无调整直接应用；先完成结果盲状态迁移与观测过程诊断，再估计四个患者级任务摘要并执行 Holm；最后由独立分析者复现。
- **Idea 阶段细节边界：** 6 小时评分网格、主要时域、12 小时遮蔽、24 小时持续恢复、80% 专家支持和 10,000 次重采样已被写为预定设计值。前四类直接界定测量或主要任务，足以防止结果驱动选择；后两类更接近执行细节。它们不阻断当前路线，但应在协议中给出依据并保持结果盲，不应被表述为普适阈值。当前预审不要求补充新的协议级数值阈值。

## 6. 可行性与前置条件

### PF-R003-05：12–18 个月仅在硬性前置门及时通过时可行

- **类别：** `nonblocking_advice`
- 月 1–2 同时完成两库项目级访问、真实样例提取、逐概念映射、约束表验收、五个核心角色确认和计算基准，执行风险较高；但研究已给出预登记替代顺序、非核心工作削减和停止条件，因此没有把不确定资源写成既成事实。
- 12–18 个月可作为第二阶段的条件性执行窗口：月 3–6 开发与冻结，月 7–12 核心外部验证，月 13–18 敏感性、独立复现和论文。若月 2 前置门未通过，正确结论是停止或延后复杂模型路线，而不是压缩资格审计或以假设继续。
- 随机试验、动物研究和第三库压力测试均不属于核心时限与必需交付，也不能补救第二阶段失败，范围控制合理。

## 7. 可行性阻断项

| 潜在阻断项 | 当前严重度 | 可修复？ | 最小处置 |
|---|---|---:|---|
| 两库访问、共同变量、标签、测量密度、事件数和有效转移尚未实证 | 启动前高；当前不是 Idea 阶段失败 | 可能 | 月 1–2 按预登记顺序完成真实样例资格审计；无合格组合则停止跨库主分析 |
| 第一阶段约束表、专家构成、共识与异议记录尚未完成 | 启动前高 | 是 | 按既定字段和独立判断程序验收；月 2 仍不合格则不拟合主模型 |
| 五个核心角色与工时尚未书面落实 | 启动前高 | 可能 | 月 2 前确认；任一核心角色缺失则不启动复杂模型开发 |
| 模拟、多初值拟合、10,000 次患者级重采样和独立复现的计算能力未实测 | 启动前中至高 | 可能 | 先完成样例基准并取消非核心分析；核心仍不足则停止复杂路线 |
| 最小统一模型可能不可辨识 | 开发期高 | 可能 | 按冻结顺序简化并重跑恢复诊断；最小模型仍失败则停止全病程统一模型主张 |

当前未发现必须在 Idea 文本中进一步发明端点、变量、样本量或协议阈值才能修复的阻断项。

## 8. Findings 分类与修订方向

| Finding | 分类 | 处理 |
|---|---|---|
| PF-R003-01 统一模型覆盖三阶段 | `nonblocking_advice` | 保持当前全病程边界和不可辨识即停止规则 |
| PF-R003-02 四项任务唯一且可计算 | `nonblocking_advice` | 保持一个患者级摘要、固定方向和任务特异比较模型 |
| PF-R003-03 Holm 无固定顺序冲突 | `nonblocking_advice` | 保持平行估计、p 值排序及确定性并列规则 |
| PF-R003-04 外部冻结诊断唯一 | `nonblocking_advice` | 在开发阶段结果盲冻结具体诊断规则，不增加外部重估路线 |
| PF-R003-05 时限依赖前置门 | `nonblocking_advice` | 保持资格、团队、计算和可辨识性为硬门及停止条件 |

`required_repair`：无。

## 9. Idea 交接工作假设

以下两项满足“已有最小可行路线、细节有界且可核验、不改变核心问题或主要推断、假设错误时仍可局部调整”的条件，可在下游写作中仅于权威假设表记录一次。

| assumption_id | unconfirmed_detail | working_assumption | basis_for_planning | impact_if_false | verification_needed | verification_point | affected_design_component |
|---|---|---|---|---|---|---|---|
| WA-01 | 最终论文是否只呈现第二阶段 | 第二阶段可独立形成完整实证论文，后续阶段可另文或在以后整合 | 两库路线、四项任务和核心交付本身构成完整实证单元 | 只调整成果组织、作者分工和后续整合，不改变核心模型或推断 | 确认论文范围与整合方案 | 月 3 协议冻结前 | 成果组织与作者计划 |
| WA-02 | 是否加入可选第三数据库 | 仅在两库核心结果锁定且资源允许时增加第三库压力测试 | 第三库不属于四任务 Holm 家族、总体判定或月 12 必需交付 | 取消第三库，不改变两库核心路线和第二阶段结论 | 核验第三库资格、资源和核心结果锁定状态 | 月 12 核心外部结果锁定后 | 可选压力测试 |

不得转为工作假设的事项：数据库访问与字段适配、共同变量、团队和计算能力、主要状态空间、任务结果编码、患者级权重、比较模型、状态迁移规则及成功判据。这些事项须在各自节点实证通过并冻结，失败时执行停止条件。

## 10. 下游交接与局限

- **建议：** 可交给全新的独立 Idea evaluator；交接时保留上述两项工作假设和所有硬性前置门，不进行语言叙事评分。
- **评估隔离：** 必须保持；本预审实例不得兼任该 dossier 的下游质量评价者。
- **局限：** 本报告只依据 v003 dossier 中声明的计划判断可执行性，未核验任何数据库、样例数据、约束表、人员承诺、计算基准、模型代码或统计模拟结果。因此 `pass` 表示 Idea 阶段存在可信最小路线，不表示实际资格门已通过，也不表示模型最终可辨识或四项任务会获得支持。
