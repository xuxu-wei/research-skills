---
review_id: preflight-r001
reviewer_skill: methodology-statistics-preflight
reviewer_instance_id: methodology-statistics-preflight-I01-001-r001-fresh
workflow_id: sepsis-complex-system-idea-generation-v001
round_id: r001
input_artifact_ids:
  - idea-dossier-I01-001-v001
input_versions:
  - v001
files_read:
  - AGENTS.md
  - research-skills-openai/skills/methodology-statistics-preflight/SKILL.md
  - research-skills-openai/skills/methodology-statistics-preflight/references/preflight-schema.md
  - research-skills-openai/skills/methodology-statistics-preflight/references/working-assumption-rules.md
  - research-skills-openai/skills/methodology-statistics-preflight/references/downstream-handoff-rules.md
  - research-skills-openai/skills/methodology-statistics-preflight/templates/template-methodology-statistics-preflight-report.md
  - research-skills-openai/skills/methodology-statistics-preflight/templates/template-preflight-failure-report.md
  - tests/脓毒症复杂系统模型/03_ideas/nodes/I01-001/dossiers/idea-dossier-v001.md
isolation_mode: fresh_subagent
prior_scores_visible: false
source_edits_performed: false
decision: revise_endpoint_or_metric
findings:
  - PF-01-primary-success-rule-not-defined
  - PF-02-latent-state-validation-target-not-operationalized
  - PF-03-data-information-adequacy-not-yet-demonstrated
  - PF-04-required-external-database-count-and-timeline-inconsistent
  - PF-05-core-inputs-cannot-be-treated-as-working-assumptions
unresolved_issues:
  - 主要推断目标及四项任务之间的层级、成功判据和多重性处理尚未冻结
  - 缺少不依赖潜在状态金标准的跨库状态对应与稳定性判据
  - 两库共同变量、事件数、有效转移数、测量密度及模型可辨识性门槛尚未核验
  - 第 12 个月最低交付所需的外部数据库数量与第 7–13 个月工作安排尚未统一
---

# Methodology-Statistics Preflight Report

## 1. Preflight Subject

- Input type: `idea`
- Downstream task: `idea_evaluation`
- Brief subject summary: 在成人重症监护纵向数据库中建立受约束隐半马尔可夫动态状态模型，并在异质数据库中检验状态、转移时间、部分观测重建和未来轨迹预测。
- Frozen input binding: `artifact_id: idea-dossier-I01-001-v001`; `version: v001`; `path: 03_ideas/nodes/I01-001/dossiers/idea-dossier-v001.md`。
- Assessment scope: 仅检查方法学与统计可行性、内部一致性、第二阶段 12–18 个月约束及工作假设边界；未评价新颖性、影响、资助价值或语言表达。

## 2. Preflight Decision

- Decision: `revise_endpoint_or_metric`
- Decision rationale: dossier 已给出可辨认的研究对象、候选数据路线、主模型、比较模型、四类任务、外部验证顺序及停止条件，因此存在最低可行的科学路线。但主要推断成功规则仍未形成：潜在状态没有金标准，现有重建指标不能直接验证“状态估计校准”或“状态语义保持”；四类任务也缺少预先确定的主次层级、联合判定规则和多重性安排。与此同时，两库信息量和必需数据库数量尚未确认。上述缺口涉及主要测量、推断目标或不可替代的数据前提，不能作为工作假设交给下游补选。
- Idea handoff decision: `clarification_stop`

这不是对整体研究价值的判断。停止点仅表示：在进入下一轮完整 idea 评价或科学写作前，应先完成下列最小方法学修订；不得由下游人员自行选择状态验证标准、主要终点或数据库要求。

## 3. Endpoint / Metric Status

- Status: `inadequate`
- Comments:
  - 四类任务分别列出了合理的指标族，并正确区分了发病时间、竞争结局、观测重建和未来轨迹，避免了单一合成准确率。
  - 然而，核心假设要求跨库保持“状态语义”“状态估计”及任务校准。潜在状态没有直接参照标准；连续块遮蔽的重建误差、覆盖率和重复遮蔽一致性只评价观测模型或后验稳定性，不能单独证明潜在状态已被正确识别或校准。
  - 尚未规定哪个任务或估计量是主要推断目标、哪些是关键次要目标、怎样判定“动态表示得到支持”，以及多个状态、时间窗、预测时距和指标的多重性如何控制或解释。
  - “优于简单基准”“达到外部门槛”和“有限校准后恢复”尚无可执行判据；这些判据决定结论强度和后续随机试验是否可触发，不能留给看到结果后的选择。
- Required repairs:
  1. 指定一个主要推断目标，或给出明确的任务层级与门控顺序；为每个关键目标定义估计量、时间范围、比较对象、方向和不确定区间。
  2. 为跨库状态对应建立可执行、在查看外部结局前冻结的判据。该判据应说明状态标签如何对齐、哪些临床特征用于对齐、如何避免用同一结果既定义又验证状态，以及何种结果只支持观测重建而不支持潜在状态有效性。
  3. 冻结总体支持、部分支持和失败的决策规则，并说明多时间窗、多状态、多任务和多数据库比较的多重性处理；后续随机试验触发门槛须与这些规则一致。

## 4. Data-Method Fit Status

- Status: `partially_adequate`
- Comments:
  - 公开成人重症监护纵向数据在概念上能够提供生命体征、实验室检查、治疗、测量行为和结局；开发库与独立外部库的分离也与问题相符。
  - 显式建模不规则时间、停留时间和测量过程，与高缺失、临床驱动采样的数据特征相匹配。患者级隔离、时间分割、外部结构冻结和竞争风险处理方向合理。
  - 当前尚无项目级访问证明、共同变量审计、事件数、有效状态转移数、测量密度、随访和标签复现结果。受约束隐半马尔可夫模型同时包含潜在状态、停留时间、治疗输入和测量过程，参数量与可辨识性高度依赖这些信息；数据库“存在”不足以证明该模型可估计。
  - 第一阶段约束表、专家名册和共识材料尚未形成，而它们决定状态空间与允许转移，是主模型的必要输入，不是可由数据分析人员补写的附属材料。
- Required repairs:
  1. 将两库资格审计写成进入建模的硬门槛，至少包括共同变量覆盖、时间戳精度、测量密度、病例数、各任务事件数、候选转移数、删失和重复住院处理，以及许可用途。
  2. 对预定状态数范围给出与有效样本、状态占用和转移事件相联系的信息量标准；在资格审计前不得承诺复杂模型能够稳定估计。
  3. 明确第一阶段约束表的最低完整性、专家构成、共识与异议记录何时达到可冻结状态。未达到该门槛时，不开始主模型拟合。

## 5. Minimal Analysis Route Status

- Status: `partially_adequate`
- Minimal route, if available:
  1. 在一个合格开发数据库中建立患者级隔离的感染风险队列和脓毒症队列；冻结标签、时间零点、预测时距、恢复、死亡、删失和竞争事件。
  2. 先拟合同队列、同时间轴、同结局定义的简单多状态模型和透明任务基准。
  3. 仅在约束表和信息量门槛通过后，估计最小预定状态数的受约束隐半马尔可夫模型；用多初值、重复分割、状态占用、转移稀疏性和后验检查判断可辨识性。
  4. 冻结结构、参数、变量映射、任务代码和成功判据后，在一个合格异质外部数据库先作无调整验证；有限校准使用与最终评价互斥的样本。
  5. 按预定规则分别报告四类任务和失效位置；若最小模型或外部资格门槛失败，停止潜在状态解释并保留数据协调及简单基准结果。
- Missing elements: 主要推断与门控规则、潜在状态外部对应判据、任务与模型信息量阈值、有限校准的精确范围、外部数据库必需数量，以及参数和状态后验不确定性如何传播到各任务指标。

## 6. Domain-Specific Checks Applied

- Research type: 纵向观察性临床数据、潜在状态模型、动态预测和跨数据库外部验证。
- Checks applied: 时间零点与信息泄漏、患者级切分、竞争事件与删失、临床驱动测量和信息性缺失、潜在状态可辨识性、状态标签对齐、预测校准、模型选择与外部验证隔离、数据库迁移、事件与转移信息量。
- Not applicable checks: 当前第二阶段不估计因果治疗效应，不包含随机试验二次分析或动物实验；因此未对其因果识别、试验交互功效或动物样本量作通过判断。

## 7. Feasibility Blockers

| Blocker | Severity | Repairable? | Repair Direction |
|---|---|---:|---|
| 潜在状态的外部有效性没有可执行参照或判据，重建指标不能替代状态校准 | 高；阻断核心推断 | 是 | 冻结状态对齐、外部一致性和结论边界，并把可直接评价与只能间接支持的目标分开 |
| 四项任务缺少主要目标、层级和联合成功规则 | 高；阻断“验证通过”判断及后续试验门控 | 是 | 指定主要估计量、关键次要目标、门控顺序、阈值和多重性安排 |
| 两库共同变量、事件数、有效转移数和测量密度未核验 | 高；阻断第二阶段模型拟合 | 条件性 | 月 1–2 完成资格审计；任一候选组合不满足最低门槛则按已列替代顺序更换，仍失败则停止跨库主分析 |
| 第一阶段约束表和专家资源尚未形成 | 高；阻断主模型结构冻结 | 条件性 | 在第二阶段拟合前形成可审计约束表、专家构成、共识规则和异议记录；失败则不拟合主模型 |
| 第 12 个月“两个异质数据库的核心外部验证”与“一个开发库加至少一个外部库”、工作单元 3 延至第 13 个月之间未统一 | 中高；阻断可靠的 12–18 个月资源判断 | 是 | 明确必需的是两个数据库总计还是两个外部数据库，并据此统一第 12 月最低交付和第 13 月工作边界 |
| 团队、独立复现人员和计算资源未确认 | 中高；可能阻断复现和不确定性估计 | 是 | 在协议冻结前落实角色与最低计算预算；资源不足时只可删减可选压力测试，不可删减核心外部验证或预定不确定性分析 |

## 8. Repair Directions

1. 先修订主要终点、潜在状态验证判据和整体成功规则；这是当前首要修订方向。
2. 在分析方案中加入可量化的数据与信息量资格门槛，并把资格审计结果作为是否进入潜在状态建模的正式决定点。
3. 统一必需数据库数量和第 12、13、18 个月交付边界；将第三数据库、随机试验和动物研究继续保留为可选或后续内容，不得挤占第二阶段核心路线。
4. 明确主模型失败时的最小科学交付：数据协调、简单多状态基准和否定性可辨识性结果可以保留，但不能被解释为潜在动态状态模型成立。

### Finding classification

| Finding | Class (`required_repair` / `working_assumption` / `nonblocking_advice`) | Reason |
|---|---|---|
| PF-01：主要成功规则和任务层级未定义 | `required_repair` | 决定主要推断和结论强度，不能由下游或结果后选择 |
| PF-02：潜在状态外部验证目标未操作化 | `required_repair` | 关系到主要测量是否可验证；观测重建不能替代状态有效性 |
| PF-03：数据与转移信息量未证明 | `required_repair` | 是复杂潜在状态模型可估计性的必要数据前提 |
| PF-04：必需数据库数量和时间表未统一 | `required_repair` | 会实质改变 12–18 个月工作量和外部验证范围 |
| PF-05：第一阶段约束表与关键人员未确认 | `required_repair` | 属于不可替代的结构输入和执行资源 |
| 目标论文最终独立成文还是与后续阶段整合 | `nonblocking_advice` | 仅影响成果组织，不改变第二阶段研究问题、数据、方法或推断 |
| 第三个地域或高时间分辨率数据库 | `nonblocking_advice` | dossier 已把它限定为资格通过后的可选压力测试，不应成为核心交付前提 |

### Working assumptions for Idea handoff

本轮 `idea_handoff_decision` 为 `clarification_stop`，因此不接受结构化工作假设；按规则，`working_assumptions` 必须为空。

```yaml
working_assumptions: []
```

下列事项在全部 `required_repair` 完成后，可作为有界条件继续推进，但本轮尚未激活为工作假设：

- 第二阶段按独立实证研究完成，最终是否与后续阶段整合只在成果组织层面决定。
- 必需路线仅包含一个开发库和经确认数量的外部验证库；第三个地域或高时间分辨率数据库只在不影响核心时间表且通过资格审计时加入。

以下事项不允许作为工作假设：至少两个合格数据库是否存在、Sepsis-3 标签与时间零点、主要终点及成功门槛、状态数与允许转移、第一阶段约束表是否可用、有效事件与转移数是否足够。任一事项为假都会改变核心问题、主要测量、不可替代输入或推断强度。

## 9. Downstream Handoff Recommendation

- Recommended next skill or workflow: 返回 `research-idea-orchestrator` 的方法学修订环节；修订后由新的 `methodology-statistics-preflight` 独立实例复核。通过后方可交给 `idea-evaluator`。
- Reason: 当前所需选择属于科学测量、数据资格和统计判定，不应由 idea evaluator 或下游写作者补定。
- Evaluation isolation required: yes

## 10. Limitations and Uncertainties

- Missing information: 未读取任何数据库样例、变量字典、事件计数、专家约束表、计算基准或人员承诺；因此不能确认模型拟合、收敛时间和外部验证样本量。
- Assumptions not verified: 数据访问、共同变量、标签可复现、状态转移信息量、团队与计算资源均未验证；本报告未将这些条件视为已成立。
- User clarification needed: 最小且必要的决定是：第二阶段必需的数据库构成究竟是“一开发加一外部”还是“一开发加两个外部”，以及哪一个估计量/任务承担主要推断。其余参数可在上述决定后由临床和统计负责人按预定审计结果冻结。
- Evidence boundary: 本报告只依据绑定的 frozen dossier 与所列方法学规则；未读取任何其他测试产物、既往评审、评分、语言报告或预期答案。
