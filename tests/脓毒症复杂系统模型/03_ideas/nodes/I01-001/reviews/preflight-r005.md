---
review_id: methodology-statistics-preflight-I01-001-r005
reviewer_skill: methodology-statistics-preflight
reviewer_instance_id: methodology-statistics-preflight-I01-001-r005-20260720T132103+0800
workflow_id: sepsis-complex-system-idea-generation-v001
round_id: r005
input_artifact_ids:
  - idea-dossier-I01-001-v005
  - user-idea-v001
input_versions:
  - v005
  - v001
files_read:
  - AGENTS.md
  - research-skills-openai/AGENTS.md
  - research-skills-openai/skills/methodology-statistics-preflight/SKILL.md
  - research-skills-openai/skills/methodology-statistics-preflight/references/endpoint-metric-checks.md
  - research-skills-openai/skills/methodology-statistics-preflight/references/data-method-fit-rules.md
  - research-skills-openai/skills/methodology-statistics-preflight/references/working-assumption-rules.md
  - research-skills-openai/skills/methodology-statistics-preflight/references/preflight-schema.md
  - research-skills-openai/skills/methodology-statistics-preflight/references/downstream-handoff-rules.md
  - research-skills-openai/skills/methodology-statistics-preflight/templates/template-methodology-statistics-preflight-report.md
  - tests/脓毒症复杂系统模型/03_ideas/nodes/I01-001/dossiers/idea-dossier-v005.md
  - tests/脓毒症复杂系统模型/00_input/user-idea-v001.md
isolation_mode: fresh_subagent
prior_scores_visible: false
source_edits_performed: false
decision: pass
findings:
  - finding_id: F-01
    finding_class: working_assumption
    summary: 核心实证研究可独立形成完整论文，后续研究的成果组织不改变核心科学路线。
  - finding_id: F-02
    finding_class: working_assumption
    summary: 第三数据库只在两库核心结果锁定且资源允许时作为可选压力测试。
  - finding_id: F-03
    finding_class: nonblocking_advice
    summary: 按既定开发期流程用不查看外部结果的审计与模拟冻结任务三的遮蔽生成、预测分布和权重实现细节。
  - finding_id: F-04
    finding_class: nonblocking_advice
    summary: 月 1–2 资格审计必须实证确认两库共同目标变量、可评分遮蔽块、观测概率权重稳定性和外部可执行性。
unresolved_issues:
  - 两个核心数据库的项目级许可、真实样例字段映射与信息量尚未实证通过。
  - 建模前约束表、五个核心团队角色和计算基准尚未完成验收。
  - WA-01 与 WA-02 尚待各自预定验证点确认。
---

# Methodology-Statistics Preflight Report

## 1. Preflight Subject

- **Preflight subject:** 成人重症监护感染风险人群中，受文献—专家约束的低维全病程隐半马尔可夫动态状态模型之开发、冻结和异质数据库外部验证。
- **Input type:** `idea`
- **Downstream task:** `idea_evaluation`
- **Brief subject summary:** 该 Idea 以一个公开纵向开发数据库和一个异质公开外部数据库为核心，统一覆盖感染风险、首次脓毒症发生、发病后器官功能与支持、持续恢复、恶化、存活出重症监护和死亡；四项预测任务分别形成患者级确认性假设，并在共同家族错误率控制下独立判定。
- **Assessment scope:** 仅评估端点或指标、数据—方法匹配、最小分析路线和执行可行性；不评价创新性、影响力、期刊适配性或总体研究价值。
- **Explicit project inputs:** `idea-dossier-I01-001-v005`（v005）和 `user-idea-v001`（v001）。未读取任何既往 preflight、assessment、plan、brief、delta、register、evaluation、map、context、state、portfolio 或父级历史。

## 2. Preflight Decision

- **Preflight decision:** `pass`
- **Decision rationale:** 在 Idea 阶段所需的科学功能、任务级估计目标、计算输入、比较模型、方向、判定时点和失败含义均已充分限定；数据、团队与计算的不确定性被作为进入建模前必须实证通过的资格门槛，并有替代、简化和停止规则，而没有被假设为已经满足。四个任务各自具有不可互换的用途，任务内形成唯一患者级摘要，四任务再以预定 Holm 程序联合控制错误率，因此无需强行设置单一总终点。当前未发现需要修改端点、数据源、方法或分析路线的必需修复。
- **Idea handoff decision:** `proceed_with_assumptions`
- **Handoff rationale:** 最小可行科学路线已经存在；仅 WA-01 和 WA-02 属于有界、可核验且即使不成立也不改变核心问题、核心输入、主要测量或推断强度的工作假设。项目级数据资格、共同变量、团队、计算、任务三可评分目标和权重稳定性均未被当作工作假设。

## 3. Endpoint / Metric Status

- **Status:** `adequate`
- **Comments:**
  - 任务一明确从感染风险入口开始，以重复的 6 小时预测起始时点构造风险集，评价随后 6、12、24 小时的首次脓毒症、先存活出 ICU、先死亡或均未发生，并用多类别 Brier 损失汇总。
  - 任务二以首次脓毒症后的多个预测起始时点为条件，评价后续首次死亡、首次持续恢复、先存活出 ICU 且未先恢复或均未发生；持续恢复具有可执行的 24 小时临床定义，且不与存活出 ICU 混同。
  - 任务三把用户提出的“由部分状态或序列补全未观测状态”一致地操作化为：只使用遮蔽块开始前及其他未遮蔽的临床历史，预测按预定规则被有意遮蔽、但在原始数据中实际测得的六个器官功能域和三类器官支持变量。评分采用冻结预测分布在真实测得目标上的负对数评分，九个结果域先等权、域内再汇总，并用逆观测概率权重处理只有实际测得目标才可评分的问题。其比较模型、方向、置信界、任务级判定和校准诊断角色均已给出。
  - dossier 在研究问题、目标、核心假设、H3 任务表、证据链、预期交付、结果解释、工作假设和局限中均明确：潜在生理状态不是任务三的真值、标签或验证端点；任务三成功只支持遮蔽实测变量的测量补全用途，不证明潜在状态恢复或真实生物状态。该操作化可测量且没有潜在状态金标准验证主张。
  - 任务四从全病程重复预测起始时点评价 24、48、72、168 小时的可观测病程向量，结果域、吸收事件编码、患者级汇总和比较模型均已指定。
  - 四项任务各自形成一个交并假设，任务内以相对全部比较模型的最不利患者级平均损失差及同时单侧上置信界判定，四个任务再进入 Holm 程序。该验证向量符合系统/多任务研究的不同科学角色，不需要额外制造一个跨任务总准确率或单一临床终点。
- **Required repairs:** none.

## 4. Data-Method Fit Status

- **Status:** `adequate`
- **Comments:**
  - 所需数据结构与方法一致：患者级标识、原始时间戳、重复纵向测量、治疗和器官支持记录、测量过程、首次脓毒症、持续恢复、出 ICU、死亡、随访及删失共同支持隐半马尔可夫状态、观测过程、竞争事件和重复预测任务。
  - 开发库承担结构与参数估计、模拟校准、内部时间验证以及全部实现规则冻结；异质外部库只接受冻结模型、标签、变量映射、比较模型、权重算法和判定规则的直接应用，不参与状态数、参数、标签、锚定或阈值选择。该分工支持真正的跨库验证并限制结果驱动调整。
  - 观测过程、治疗输入和生理状态被分开建模；治疗系数只解释为条件预测关系。dossier 明确排除因果治疗效应、最优治疗、反事实个体效应和中介网络主张，符合观察性公共 ICU 数据的识别能力。
  - 患者内重复起始时点先汇总为患者级损失，患者级重采样保留重复住院聚类；竞争事件、删失和只有实际测得值才可评分的组成分别编码，并预定逆删失或逆观测概率权重、截断与敏感性分析。患者分割、未来信息、外部选择和比较模型处理一致性均列入泄漏审计。
  - 数据库尚未被指定为已经可用。Idea 采用项目许可、真实样例抽取、逐概念映射、目标变量与遮蔽块可评分性、事件和有效转移、观测概率权重稳定性及外部可执行性的实证资格审计；资格失败时按不查看模型表现的预登记顺序替换，仍失败则停止。这使不确定的数据可得性成为明确的执行门槛，而不是被掩盖的数据—方法错配。
- **Required repairs:** none at Idea stage.

## 5. Minimal Analysis Route Status

- **Status:** `adequate`
- **Minimal route:**
  1. 月 1–2 完成文献—专家约束、两个数据库的项目级许可与真实样例资格、共同变量和事件映射、核心团队承诺及计算基准；任一不可替代条件失败则不进入主模型。
  2. 在合格开发结构下模拟状态占用、缺失、删失和弱转移，检查参数偏倚、区间覆盖、标签交换、潜在状态恢复和预测稳定性；按固定顺序减少状态数、合并无支持转移、简化停留时间并移除非必要交互。
  3. 最小统一模型可辨识后，冻结主要模型、状态标签、变量映射、任务结果编码、预测起始时点、时域、风险集、遮蔽规则、预测分布、比较模型、权重、迁移规则和四任务检验程序。
  4. 在异质外部库中直接应用冻结对象，先锁定不使用验证结局的临床锚定迁移诊断和分开的观测过程诊断，再平行估计四项任务的患者级损失差、区间和 Holm 调整结果。
  5. 将无调整结果与有限校准、敏感性、亚组和可选第三库严格分开，并由未参与主建模的分析者复现核心队列计数、任务摘要、Holm 结论与迁移诊断。
- **Missing elements:** 没有妨碍 Idea 继续评估的结构性缺失。协议冻结前仍需由不查看外部结果的资格审计、模拟或内部试点确定具体状态数、任务三连续目标的预测分布实现、遮蔽生成细节、权重模型与截断规则，以及状态迁移数值规则；dossier 已为这些事项指定负责阶段、允许信息和失败后果，不需要在 Idea 阶段预设跨疾病通用阈值。

## 6. Domain-Specific Checks Applied

- **Research type:** 临床观察性纵向预测研究、动态状态/系统辨识方法研究和多任务外部验证。
- **Checks applied:**
  - 目标人群、感染风险入口、患者级推断单位、重复风险集、预测起始时点、预测时域、竞争事件和删失角色是否明确。
  - 预测标签或评分目标、基线比较、患者级聚类、时间泄漏、缺失与信息性测量、外部验证冻结和跨库概念映射是否匹配。
  - 潜在状态可辨识性是否仅由设定模型下的模拟恢复诊断支持，以及跨库状态表示是否用不含验证结局的临床锚定特征评估。
  - 多任务是否保留各自科学角色、任务级估计量和失败含义，并控制任务内比较和四任务家族错误率。
  - 观察性治疗输入是否被限制为预测性条件关联，而没有越界为因果、机制或治疗推荐。
- **Not applicable checks:** 随机试验治疗效应、动物实验效应、定性研究可信度和干预部署效用不属于 12–18 个月核心实证路线；RCT 与动物研究仅是另行资格审查后的条件性后续分支。

## 7. Feasibility Blockers

当前未识别需要修订 Idea 才能解除的方法学阻断。以下均是 dossier 已明确承认并配有验证点、替代路线和停止后果的条件性执行门槛，而不是已满足事实或可由工作假设替代的条件。

| Conditional execution gate | Severity if failed | Repairable? | Repair direction or consequence |
|---|---|---:|---|
| 月 2 末无法形成一个合格开发库与一个独立异质外部库，或任务三缺少共同实测目标、可评分遮蔽块、稳定观测概率权重或外部可执行性 | Blocking at execution | 有限 | 按不查看性能的预登记顺序审计替代库；仍失败则停止跨库主分析，不进入潜在状态模型 |
| 建模前约束表缺少规定字段、专家构成、独立判断、共识与异议记录 | Blocking at execution | 是 | 补齐结构化专家程序；月 2 末仍不合格则不拟合主模型 |
| 五个核心团队角色未书面落实，或计算基准不足以完成两库模拟、重采样、外部评分和独立复现 | Blocking at execution | 有限 | 先取消第三库、额外亚组和非必需消融并重新基准；核心路线仍不足则停止复杂模型路线 |
| 最小预定统一模型在开发结构模拟和内部诊断中仍不能恢复关键状态与转移 | Blocking at execution | 有限 | 按固定顺序降复杂度并重复诊断；最小模型仍失败则停止统一潜在状态和全病程成功主张 |

## 8. Repair Directions

**Required repairs:** none.

**Nonblocking implementation advice:**

1. 继续按 dossier 已规定的月 1–2 资格报告，逐库记录任务三九个结果域的实际测量覆盖、遮蔽块可形成性、目标被观测概率的重叠与极端权重表现；不以模型或外部任务结果选择数据库。
2. 在任何外部任务结果或外部状态可分离性可见前，用开发期审计、模拟和内部时间验证冻结任务三的连续变量预测分布、尺度变换、12 小时遮蔽块生成、临床样式遮蔽敏感性、观测概率权重、截断和失败规则。无需采用跨数据集通用数值阈值。
3. 保持四项任务的独立报告、任务内全部比较模型交并判定、四任务 Holm 程序和任务三“仅支持测量补全”的解释边界；不得让其他任务、有限校准、第三库、RCT 或动物研究补救未通过任务。

### Finding classification

| Finding | Class (`required_repair` / `working_assumption` / `nonblocking_advice`) | Reason |
|---|---|---|
| WA-01：核心实证研究暂按可独立形成完整论文推进 | `working_assumption` | 仅影响成果组织和作者分工；有月 3 协议冻结前的验证点，不改变核心问题、数据、方法、端点或主张强度 |
| WA-02：第三数据库只在两库核心结果锁定且资源允许时加入 | `working_assumption` | 第三库明确不进入四任务家族、总体判定或月 12 核心交付；不成立时可直接取消 |
| 用开发期、结果盲的审计和模拟冻结任务三实现细节 | `nonblocking_advice` | H3 的科学功能、目标、比较、评分方向和失败含义已清楚；剩余是协议级实现，不需修改核心路线 |
| 实证核验两库共同变量、任务三可评分性、权重稳定性、团队与计算 | `nonblocking_advice` | 这些是既定执行资格门槛并带停止规则，不应被转化为假设或用通用阈值替代 |

### Working assumptions for Idea handoff

| assumption_id | unconfirmed_detail | working_assumption | basis_for_planning | impact_if_false | verification_needed | verification_point | affected_design_component |
|---|---|---|---|---|---|---|---|
| WA-01 | 最终论文是否只呈现核心实证研究 | 核心实证研究可独立形成完整实证论文，后续研究可另文或后续整合 | 核心身份、四项任务、两库路线和核心交付不依赖成果组织 | 仅调整成果组织、作者分工与后续整合，不改变核心分析路线 | 确认核心论文边界、后续分支的归属和作者责任 | 月 3 协议冻结前 | 成果组织与作者分工 |
| WA-02 | 可选第三数据库是否具备资格与资源 | 只有两库核心结果锁定且资源允许时加入第三库压力测试 | 第三库不参与四任务 Holm 家族、总体判定、核心身份或月 12 必需交付 | 取消第三库压力测试；两库核心路线和结论规则不变 | 核验第三库许可、共同变量映射、样例资格、计算与分析资源 | 月 12 两库核心外部结果锁定后 | 可选外部压力测试 |

## 9. Downstream Handoff Recommendation

- **Recommended next skill or workflow:** `idea-evaluator`
- **Reason:** 方法学/统计学最小路线已通过，只有两项已经明确接受、范围有限且可核验的工作假设；可在保留本报告的条件性执行门槛和解释边界后进入独立 Idea 评价。
- **Evaluation isolation required:** yes.

## 10. Limitations and Uncertainties

- **Missing information:** 两个数据库的项目级许可与实际字段适配、样例信息量、任务三目标覆盖与权重稳定性、完成的约束表、团队书面承诺和计算基准目前均未被实证提供。
- **Assumptions not verified:** WA-01 和 WA-02 尚未到各自验证点；它们不得被表述为事实。
- **User clarification needed:** none before independent Idea evaluation. 若月 1–2 的任一不可替代资格门槛失败，应按 dossier 的替代或停止规则处理，而不是由下游写作者猜测数据、变量、状态数、阈值或方法。
- **Inference boundary:** 本 preflight 只确认 Idea 阶段的端点、数据—方法和最小分析路线充分性；不确认数据库实际可用、模型最终可辨识、四项任务会通过、潜在状态是真实生理状态、治疗关系具有因果性，或模型具有临床部署效用。
