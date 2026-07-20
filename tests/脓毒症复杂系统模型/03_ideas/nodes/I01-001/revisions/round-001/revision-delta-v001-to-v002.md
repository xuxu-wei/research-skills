---
schema_version: research-idea.v3
plugin_version: "0.10.0"
artifact_id: revision-delta-I01-001-v001-to-v002
workflow_id: sepsis-complex-system-idea-generation-v001
idea_id: I01-001
version_id: v001-to-v002
round_id: round-001
path: 03_ideas/nodes/I01-001/revisions/round-001/revision-delta-v001-to-v002.md
source_skill: multi-path-idea-generator
change_type: scientific_revision_delta
based_on:
  - artifact_id: idea-dossier-I01-001-v001
    version: v001
    path: 03_ideas/nodes/I01-001/dossiers/idea-dossier-v001.md
  - artifact_id: preflight-r001
    version: r001
    path: 03_ideas/nodes/I01-001/reviews/preflight-r001.md
revised_artifact:
  artifact_id: idea-dossier-I01-001-v002
  version: v002
  path: 03_ideas/nodes/I01-001/dossiers/idea-dossier-v002.md
frozen: true
---

# I01-001 scientific revision delta: v001 to v002

## Revision outcome

v002 保持同一研究身份：在成人重症监护纵向数据中构建受约束的脓毒症动态状态模型，并在异质外部数据库中验证。修订没有把研究改写为单纯发病预测，没有新增数据、结果或已验证主张。主要变化是把主要推断、潜在状态验证、数据资格、数据库构成、时间表和第一阶段约束表前置条件变成可执行的方法学规定。

## Finding-to-revision map

| Finding | v001 problem | v002 revision and locator | Closure evidence |
|---|---|---|---|
| PF-01 | 主要推断目标、四项任务层级、联合成功规则和多重性未冻结 | `Research question, objectives, and core hypothesis` 定义外部未来 48 小时可观测病程综合 Brier 分数差、两个比较模型、方向与 95% 置信区间；`Research design and methods / Fixed sequential gates and multiplicity` 固定“资格与可辨识性→外部主要目标→四个关键任务”；`Four hierarchically tested key tasks` 逐项规定估计对象、时域、比较、方向和区间；`Overall decision rules frozen before external results` 定义总体支持、部分支持和失败 | 主要目标直接评价动态复杂系统模型的外部预测；四项用户任务均保留且不合并；Holm 方法控制四项任务家族错误率，所有规则在外部揭盲前冻结 |
| PF-02 | 潜在状态无金标准，观测重建可能被误作状态正确性的证据 | `Research design and methods / External state alignment without a gold standard` 规定仅用六个器官功能域、同期生命体征、当前器官支持、测量强度和短时变化方向对齐状态，排除死亡、持续恢复、未来支持变化及四项任务验证结局；`Evidence chains / 从临床锚定特征到状态表示可重复性` 给出独立对齐流程；`Limitations and boundary conditions` 明确重建、对齐和预测各自只能支持有限结论 | 外部状态在读取验证结局前匹配；正文明确区分状态表示可重复性、预测用途和真实生物状态，并明确重建性能不能证明潜在状态正确 |
| PF-03 | 两库共同变量、事件与有效转移、测量密度和可辨识性未证明 | `Data, materials, and existing evidence base / Database qualification audit` 要求共同变量、时间戳、测量密度、患者数、事件数、候选状态占用、有效转移、随访、删失、重复住院、版本、许可和用途；`Complexity selection and identifiability` 用项目特异模拟、参数恢复和内部试点决定复杂度，并在外部揭盲前冻结；`Risks, alternatives, and stop conditions` 给出按状态数、转移、停留时间和交互简化以及最终停止路线 | 未设置跨疾病通用事件数阈值；最高复杂度失败即顺序减模，最小模型仍失败即停止潜在状态主张，不能用外部结果选择复杂度 |
| PF-04 | 必需数据库数量与第 12、13 个月交付不一致 | `Research content and work packages` 和 `Required inputs and database constitution` 固定一个开发库加一个异质外部库，共两个；第三库只在月 13 后作可选压力测试；时间表统一为月 1–2 资格、月 3–6 开发、月 7–12 核心外部验证、月 13–18 敏感性/独立复现/论文 | 月 12 核心交付只要求一个开发库和一个外部库；第三库不参与主要门控、月 12 完成点或核心成功判定 |
| PF-05 | 第一阶段约束表、核心输入和人员条件可能被放入工作假设 | `Data, materials, and existing evidence base / First-stage constraint-table prerequisite` 固定约束表最低字段、至少五类必要专家席位、独立判断、匿名反馈、80% 共识、跨临床与方法支持、少数意见和未解决异议记录；`Working assumptions` 只保留成果组织和可选第三库两个不改变核心身份或主要测量的条件性事项 | 约束表未合格时不拟合主模型；两库资格、标签、主要终点、状态复杂度、对齐和成功判据均明确排除在工作假设之外 |

## Preserved boundaries

- 保留成人脓毒症、纵向重症监护数据、受约束动态状态表示、反馈和系统辨识的原始科学对象。
- 保留用户给定的四个候选标准，转化为四个有顺序、独立估计和独立解释的关键任务。
- 保留第二阶段 12–18 个月限制；第一阶段是必须验收的结构输入，第三阶段没有既定时间承诺。
- 保留公开数据库优先和跨数据库外部验证；核心仅为一个开发库与一个异质外部库。
- 保留 EXIT-SEP、XBJ-SCAP 为数据权限、时点、功效和既有分析重叠均核验后的条件性后续。
- 保留动物研究为单一明确人类机制假设、试验证据、平台、伦理和样本量均满足后的可选后续；动物结果不作为临床模型外部验证。
- 保留观察性解释边界：时间关联与网络权重不等于因果调控、最优治疗、反事实效应或临床控制作用。
- 保留证据强度限制：不作“首个”“完整”“已识别真实生物状态”“已验证临床效用”主张。

## Remaining working assumptions

| 假设编号 | 条件性推进内容 | 负责人 | 截止时间 | 条件不成立的后果 |
|---|---|---|---|---|
| WA-01 | 第二阶段可独立形成完整实证论文；最终是否与后续阶段整合只影响成果组织 | 研究负责人 | 月 3 协议冻结前 | 只调整成果组织、作者分工和后续整合，不改变主要估计量、两库路线或核心身份 |
| WA-02 | 第三数据库仅在核心外部验证完成且资源允许时加入压力测试 | 数据负责人和统计负责人 | 月 12 核心外部结果锁定后 | 取消第三库，不影响两库主要分析、核心交付和主要判定 |

没有把核心数据、主要终点、状态定义、状态对齐、第一阶段约束表、信息量或成功门槛作为工作假设。

## Structural check

- Command: `python research-skills-openai/skills/multi-path-idea-generator/scripts/lint_idea_dossier.py tests/脓毒症复杂系统模型/03_ideas/nodes/I01-001/dossiers/idea-dossier-v002.md --expected-plugin-version 0.10.0`
- First run: exit code 0，报告一条 `assumption_id` 读者文本候选提示；已把表头改为自然语言“假设编号”，未改变科学内容。
- Final run: exit code 0；输出 `OK: tests\\脓毒症复杂系统模型\\03_ideas\\nodes\\I01-001\\dossiers\\idea-dossier-v002.md`，无提示或错误。

## Downstream handoff

v002 已冻结，下一步应由新的独立方法学实例针对 v002 重新预审；本轮作者不宣告方法学通过、叙事就绪、语言就绪或评价结果。
