---
review_id: preflight-r002
reviewer_skill: methodology-statistics-preflight
reviewer_instance_id: methodology-statistics-preflight-r002-20260720
workflow_id: sepsis-complex-system-idea-generation-v001
round_id: r002
input_artifact_ids:
  - idea-dossier-I01-001-v002
input_versions:
  - v002
files_read:
  - research-skills-openai/skills/methodology-statistics-preflight/SKILL.md
  - research-skills-openai/skills/methodology-statistics-preflight/references/preflight-schema.md
  - research-skills-openai/skills/methodology-statistics-preflight/references/working-assumption-rules.md
  - research-skills-openai/skills/methodology-statistics-preflight/references/endpoint-metric-checks.md
  - research-skills-openai/skills/methodology-statistics-preflight/references/data-method-fit-rules.md
  - research-skills-openai/skills/methodology-statistics-preflight/references/minimal-analysis-route-rules.md
  - research-skills-openai/skills/methodology-statistics-preflight/references/feasibility-blockers.md
  - research-skills-openai/skills/methodology-statistics-preflight/references/domain-specific-checks.md
  - research-skills-openai/skills/methodology-statistics-preflight/references/downstream-handoff-rules.md
  - research-skills-openai/skills/methodology-statistics-preflight/templates/template-methodology-statistics-preflight-report.md
  - tests/脓毒症复杂系统模型/03_ideas/nodes/I01-001/dossiers/idea-dossier-v002.md
isolation_mode: fresh_subagent
prior_scores_visible: false
source_edits_performed: false
decision: revise_endpoint_or_metric
findings:
  - finding_id: PF-R002-01
    finding_class: required_repair
    summary: 主要推断窗口与完整病程模型边界尚未对齐
  - finding_id: PF-R002-02
    finding_class: required_repair
    summary: 综合 Brier 分数尚未形成唯一且可复现的主要度量
  - finding_id: PF-R002-03
    finding_class: required_repair
    summary: 外部状态的产生方式与对齐失败规则仍不明确
  - finding_id: PF-R002-04
    finding_class: required_repair
    summary: 顺序门控与 Holm 调整的联合实施规则尚未唯一化
  - finding_id: PF-R002-05
    finding_class: required_repair
    summary: 两库资格、团队和计算条件仍须在建模前实证确认
  - finding_id: PF-R002-06
    finding_class: nonblocking_advice
    summary: 可选第三库和论文组织可继续保留为非核心安排
unresolved_issues:
  - 同一个冻结模型是否明确覆盖感染风险期、首次脓毒症发生和发病后演化
  - 综合 Brier 分数的分量编码、权重、风险集、观察权重和患者级汇总规则
  - 外部状态是由冻结开发模型直接推断还是在外部库重新估计后再对齐
  - 顺序门控、Holm 调整、同时置信区间和任务内多时域的唯一检验算法
  - 两个公开数据库的项目级访问、共同变量、时间精度、信息量和团队资源
---

# Methodology-Statistics Preflight Report

## 1. Preflight Subject

- **Input type:** `idea`
- **Downstream task:** `idea_evaluation`（须先完成方法学修订）
- **Brief subject summary:** 构建受文献—专家约束的隐半马尔可夫脓毒症动态状态模型，在一个公开重症监护数据库开发并在一个异质公开数据库外部验证；计划同时评价可观测动态病程、状态表示可重复性及四项分层临床任务。
- **Assessment scope:** 仅评估终点与度量、数据—方法匹配、最小分析路线、外部验证和 12–18 个月可执行性；不评价新颖性、影响力、叙事或语言。

## 2. Preflight Decision

- **Decision:** `revise_endpoint_or_metric`
- **Decision rationale:** 方案已经形成可辨识性诊断、冻结开发、两个比较模型、外部验证、患者级不确定性估计和停止规则组成的最小可行骨架。但当前主要研究问题、主要估计量和主模型评价均从脓毒症索引后开始，感染风险期和首次发病仅作为通过主要门控后才确认性检验的关键任务。由此，现有设计首先能支持“已发生脓毒症患者的动态预后状态模型”，尚不能无歧义地支持覆盖发病前—首次发病—发病后演化的完整脓毒症复杂系统模型。与此同时，综合 Brier 分数、外部状态生成与对齐、门控和多重性规则仍存在会改变主要结论的操作歧义，不能交由下游作者自行选择。
- **Idea handoff decision:** `clarification_stop`

修订可以保留“索引后 6、12、24、48、72 小时、预测未来 48 小时”作为主要外部验证窗口，但必须先说明该窗口只是验证估计量，而不是主模型的病程边界；并说明同一冻结模型如何在感染风险期进入、识别首次发生并继续表示发病后转移。若研究本意仅是索引后预后，则应相应收窄研究身份，而不能继续以完整病程模型为主要方法学主张。

## 3. Endpoint / Metric Status

- **Status:** `inadequate`
- **Comments:** 未来 48 小时、五个重复预测时点、六个器官功能域、三类器官支持、死亡和持续恢复均已给出，死亡与持续恢复也定义为吸收事件；这些内容使目标具有可测量基础。主要不足有两项。第一，主要估计量只纳入索引后仍在观察且符合风险集资格的脓毒症患者，没有把发病前状态与首次发病转移纳入核心推断。第二，“在时间网格和可观测组成上按预先冻结权重积分”的综合 Brier 分数仍不是唯一可复现的度量：六个器官功能域是按类别概率、阈值概率还是其他形式计分，三类器官支持与吸收事件如何共同编码，各分量和各时点如何归一化，以及同一患者多个预测时点如何加权，均未确定。
- **Required repairs:** 
  1. 冻结研究病程边界及其与主要验证窗口的关系：明确同一模型的状态空间、学习样本、允许转移和预测接口是否覆盖感染风险期、首次脓毒症发生及发病后演化；若覆盖，关键任务一不能只是与核心模型脱节的附加生存模型。
  2. 给出综合 Brier 分数的最小可执行定义，包括每个分量的结果编码和预测概率、时间权重、分量权重、患者与预测时点的汇总单位、吸收事件后的计分规则、出院和转院处理、删失权重及观察权重的估计、截断与敏感性规则。
  3. 明确主要模型分别对两个比较模型的患者级平均差是两个共同主要比较，并保留“两个置信区间上限均小于 0”的交并检验判据。

## 4. Data-Method Fit Status

- **Status:** `partially_adequate`
- **Comments:** 方案要求共同变量、单位、时间戳、测量密度、患者数、事件数、有效转移、随访、删失、重复住院、版本和许可均通过资格审计；显式区分生理观测、测量过程和治疗记录，并规定患者级隔离和外部数据不参与复杂度选择。这些安排与纵向隐状态模型和外部预测验证基本匹配。尚未确认项目级访问、完整变量字典、样例提取及两个数据库对六个器官域、三类器官支持、感染时间、持续恢复和观察过程的共同可实现性，因此目前只能判为条件性可行。
- **Required repairs:** 
  1. 在主模型拟合前，用真实样例提取完成两库逐概念映射，证明核心标签、6 小时时间精度、预测窗口、死亡/恢复/出院/转院以及观察过程均可同义实现；资格失败必须执行已登记的替代顺序或停止。
  2. 将信息量门槛写成可执行的模拟判据：至少规定需要达到的参数偏倚或预测误差、区间覆盖、状态占用、有效患者级转移、标签匹配稳定性和多初值一致性标准，并在任何外部结局评价前冻结。
  3. 区分“外部数据库结构资格信息可见”与“外部结局性能不可见”，保存门槛制定时间和数据访问日志，避免根据外部性能或外部状态可分离性反向调整状态数和阈值。

## 5. Minimal Analysis Route Status

- **Status:** `partially_adequate`
- **Minimal route, if available:** 验收约束表与两库资格；在开发库结构下模拟并做参数恢复；按预定顺序简化至可恢复的受约束隐半马尔可夫模型；冻结模型、两个比较模型、主要度量、状态锚定与检验规则；在外部库先进行无调整验证；以患者级重采样估计主要差值；之后按冻结规则评价状态表示和四项任务；最后完成敏感性分析和独立复现。
- **Missing elements:** 完整病程模型与索引后验证窗口的映射、综合 Brier 分数的唯一计算规则、外部状态产生机制、状态对齐失败规则，以及顺序门控与 Holm 调整的唯一算法。

外部状态对齐目前还存在一个关键分叉：若只用冻结的开发参数对外部患者做状态后验推断，状态标签本来继承开发模型标号，所谓“一一匹配”主要是在检验锚定特征的迁移；若在外部库重新估计状态，则这不是单纯应用冻结模型，需要规定哪些参数可重估、如何避免验证结局参与、如何处理状态数不等及状态拆分或合并。二者不能在看到外部结果后选择。另应避免强制一一匹配掩盖不可分离状态；测量强度可作为观察过程的辅助锚定信息，但应与器官功能、生命体征和当前支持所定义的临床锚定结果分开报告，以免把数据库测量习惯误作生理状态可重复性。

## 6. Domain-Specific Checks Applied

- **Research type:** 临床观察性纵向预测研究、潜在状态/机器学习方法研究及外部验证。
- **Checks applied:** 人群与时间零点；标签和预测时域；重复测量与患者级聚类；目标与比较模型；信息性观察和删失；时间泄漏；模型复杂度相对于患者、事件和有效转移的信息量；校准、外部验证与独立复现；潜在状态无金标准时的表示可重复性；预测性关联与因果解释边界。
- **Not applicable checks:** 随机治疗效应和动物机制实验不是本次 12–18 个月核心分析，未按试验或动物研究要求进行预检。

## 7. Feasibility Blockers

| Blocker | Severity | Repairable? | Repair Direction |
|---|---|---:|---|
| 主要模型是否覆盖发病前—首次发病—发病后全过程尚不明确 | 高 | 是 | 冻结统一状态空间、样本和转移边界，或收窄研究身份；不得由下游作者猜测 |
| 综合 Brier 分数存在多种统计上不同的实现 | 高 | 是 | 在外部验证前冻结分量编码、权重、风险集、观察/删失权重和患者级汇总 |
| 外部状态是直接推断还是重新估计未确定 | 高 | 是 | 选择并冻结一种验证设计，规定不可分离、未匹配、拆分和合并状态的失败处理 |
| 顺序门控与 Holm 调整的组合规则不唯一 | 中高 | 是 | 列出假设族、检验顺序、显著性阈值、调整置信区间和任务内多时域处理 |
| 两库项目级访问、共同字段、时间精度和信息量尚未实证确认 | 高但属于前置资格 | 是 | 在月 1–2 完成授权和样例提取；未通过则按预登记替代顺序处理或停止 |
| 核心团队角色和计算预算尚未落实 | 中高 | 是 | 协议冻结前落实负责人和计算基准，优先保留两库核心验证、重采样和复现 |

## 8. Repair Directions

1. 先解决研究边界：保留索引后 48 小时主要验证窗口时，明确它只评价统一模型的一个核心外部用途；同一模型的构建对象和状态转移必须显式包含感染风险、首次发生和发病后阶段。若做不到，则把研究问题、题名和结论边界收窄为已发生脓毒症患者的动态预后模型。
2. 在一个不依赖具体软件的计分规范中冻结综合 Brier 分数，确保所有模型使用完全相同的风险集、观测定义、权重和患者级汇总；对每一组成给出可计算的概率预测和结果编码。
3. 冻结外部状态验证设计。不得在看到结局后选择直接推断或重新估计；不可分离或无法匹配应产生明确失败或部分支持结果，而不是强制匹配。
4. 把多重性程序写成单一算法。主要模型对两个比较模型的判定可维持交并检验；四项任务需明确是严格固定顺序检验、Holm 检验，还是预先定义的组合程序，并说明任务内多时域和复合成功条件如何进入同一假设族。
5. 将月 1–2 设为真正的可行性判定期：完成两库授权、样例提取、共同变量和计数审计、团队确认及计算基准。核心条件失败时按既有停止规则结束，不把未确认的数据资格当作工作假设。

### Finding classification

| Finding | Class (`required_repair` / `working_assumption` / `nonblocking_advice`) | Reason |
|---|---|---|
| PF-R002-01 主要推断窗口与完整病程模型边界未对齐 | `required_repair` | 涉及研究对象、核心问题和主要推断边界，不能由写作者补选 |
| PF-R002-02 综合 Brier 分数未唯一操作化 | `required_repair` | 不同编码、权重和风险集会改变主要估计量和优效判定 |
| PF-R002-03 外部状态产生与对齐失败规则不明确 | `required_repair` | 两种设计回答不同问题，也影响“外部验证”和“表示可重复性”的含义 |
| PF-R002-04 门控与多重性算法未唯一化 | `required_repair` | 影响确认性结论和家族错误率，必须在外部数据评价前确定 |
| PF-R002-05 数据、人员和计算资格未实证确认 | `required_repair` | 属于不可替代的实施前提；可通过月 1–2 审计修复，但不能假定已经满足 |
| PF-R002-06 可选第三库与论文组织 | `nonblocking_advice` | 取消或调整均不改变两库核心路线、主要测量或推断强度 |

### Working assumptions for Idea handoff

无。当前 handoff 为 `clarification_stop`，工作假设表按规则保持为空。原构想中关于论文组织和可选第三数据库的安排是有界、可核验且可取消的非核心安排，可以保留，但不能替代上述主要终点、数据或方法修订。

## 9. Downstream Handoff Recommendation

- **Recommended next skill or workflow:** 返回 `research-idea-orchestrator` 做一次有界方法学修订；完成后由新的 `methodology-statistics-preflight` 独立实例复检，再进入 `idea-evaluator`。
- **Reason:** 当前问题集中在研究边界、主要度量和验证算法，不需要重写完整方案；但它们会改变主要推断和成功判据，不能在评估或写作阶段临时决定。
- **Evaluation isolation required:** yes

## 10. Limitations and Uncertainties

- **Missing information:** 两库项目级访问与样例提取、逐概念字段映射、冻结信息量阈值、完整计分规范、外部状态产生方式、最终多重性算法、团队承诺与计算基准。
- **Assumptions not verified:** 未假定任何核心数据、终点或方法条件已经满足。12–18 个月可行性仅在月 1–2 资格、团队和计算门槛通过后成立；在有经验团队、两库及时取得访问且最小模型通过恢复诊断的条件下，删去第三库和非必要探索后，核心路线具有条件性可执行性。
- **User clarification needed:** 需要确认研究身份究竟是覆盖感染风险至发病后演化的统一复杂系统模型，还是仅针对已发生脓毒症患者的动态预后模型。前者必须补齐统一模型边界；后者必须收窄主要问题和主张。
- **Isolation limitation:** 本报告只读取指定 v002 dossier 和当前 methodology/statistics preflight 的直接适用规则与模板；未读取任何早期 dossier、既往 preflight、修订材料、context/maps、fixture 或其他评审报告。
