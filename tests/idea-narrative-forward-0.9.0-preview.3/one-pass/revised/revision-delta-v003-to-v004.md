---
schema_version: research-idea-revision-delta.v1
plugin_version: 0.9.0-preview.3
artifact_id: revision-delta-I01-001-v003-to-v004
workflow_id: RID-SEPSIS-CSM-20260717-001
idea_id: I01-001
source_version: v003
target_version: v004
created_round: 1
change_type: editorial_repair
based_on:
  - artifact_id: idea-dossier-I01-001-v003
    version: v003
    path: tests/idea-test-0.9.0-preview.1/0.9.0-preview.1/03_ideas/nodes/I01-001/dossiers/idea-dossier-v003.md
  - artifact_id: narrative-repair-plan-I01-001-r010
    version: r010
    path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass/baseline/narrative-repair-plan-r010.yaml
  - artifact_id: language-assessment-I01-001-r010
    version: r010
    path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass/baseline/language-assessment-r010.md
  - artifact_id: protected-content-register-I01-001-v003
    version: v003
    path: tests/idea-narrative-forward-0.9.0-preview.3/run-001/inputs/protected-content-register.yaml
---

# Revision delta: idea dossier v003 to v004

## Scope and outcome

本轮只执行一次集中式科学编辑修订，不评价研究构想是否就绪，也不新增证据、方法、结果或可行性判断。v004 保留 `research-idea.v3` 的 15 个 H2；第三个 H2 下保留 `Background`、`Current state`、`Gap`、`Significance` 和 `Rationale` 五个非空 H3；五条 Evidence chain 与 Title and positioning claim-support table 均保留合同结构。完整限制、假设、解释边界、替代方案和停止条件集中于第 14 节。

## Actual source files read

编辑阶段只读取以下四个输入：

1. `tests/idea-test-0.9.0-preview.1/0.9.0-preview.1/03_ideas/nodes/I01-001/dossiers/idea-dossier-v003.md`
2. `tests/idea-narrative-forward-0.9.0-preview.3/one-pass/baseline/narrative-repair-plan-r010.yaml`
3. `tests/idea-narrative-forward-0.9.0-preview.3/one-pass/baseline/language-assessment-r010.md`
4. `tests/idea-narrative-forward-0.9.0-preview.3/run-001/inputs/protected-content-register.yaml`

写入后仅重新读取本轮生成的 v004 进行结构与术语自检；未读取其他 dossier、修订稿、评审、delta、测试预期或项目产物。

## Narrative repair actions

| Action | Revised locator | Operation | Retained content | Deleted or moved content | Scientific meaning changed | Protected-content disposition | Unexecuted item and reason |
|---|---|---|---|---|---|---|---|
| NRP-001 | `Background, current state, gap, significance, and rationale` 下的 `Current state` 与 `Gap` | replace、split、move | 保留各单项模块已有先例、完整组合负向判断仅有界且置信度有限、患者状态与行动及测量过程分离、发病前至结局为同一对象 | 删除“可辩护空间仅是特定组合”作为唯一缺口的表述；代表性近邻明细移至第 12 节，完整检索局限移至第 14 节 | 否 | PCR-001、PCR-003、PCR-009 保留同义与同等强度；PCR-010 的 closest-work 不确定性集中到第 14 节 | 无 |
| NRP-002 | 同一 H2 下新增 `Significance`，并以 `Rationale` 承接 | add_bridge | 保留整合、验证、基准或资源及可证伪研究治理价值；保留计划结果尚未生成和阶段 III 不补足阶段 II | 未删除科学内容；将分散的正向价值压缩为独立段落 | 否 | PCR-009 保留计划状态与条件性贡献；PCR-011 保留阶段关系 | 无 |
| NRP-003 | `Title, summary, audience, and positioning` 的一语摘要 | replace、shorten | 保留 24 个月阶段 I–II、文献和专家先验、两个公共 ICU 数据库、全病程连续体、跨数据库验证、阶段 III 的条件性和预测不等同因果 | 模拟恢复细节、试验第 7/8 日、观测映射阈值、独立 SOFA 分支细节和完整禁止解释清单分别移至结构式摘要、方法及第 14 节 | 否 | PCR-001、PCR-002、PCR-009、PCR-011、PCR-012 均按原强度保留 | 无；受固定 `One-sentence` 字段约束，采用显著缩短的单句，而非多句 |
| NRP-004 | `Structured abstract` 的 `Objective and hypothesis`、`Approach` 与 `Expected result`，以及后续首次出现处 | define、replace | 保留基线先行、复杂候选须经模拟恢复、独立测试隔离、观测映射须先检验、方法中的全部阈值和失败路线 | 删除未解释的流程标签；不必要的项目代码留至方法首次定义 | 否 | PCR-006、PCR-007、PCR-008 的顺序、阈值、任务和拆分规则完整保留 | 无 |
| NRP-005 | 第 11 节保留局部产物判定；第 14 节集中完整边界 | consolidate、move、delete | 保留方法中决定估计目标、替代分析或停止的规则；保留 Evidence chains 的 Input、Method、Output、Supports；保留 Required analyses、正向贡献、Claim-Support 审计和风险触发功能 | 从摘要、核心假设、技术清单、计划产出、贡献表和最接近工作结语中删除重复的完整禁止解释清单；将全局限制、失败含义、替代方案和解释矩阵集中到第 14 节 | 否 | PCR-010、PCR-011、PCR-012 在第 14 节完整保留；其余受保护方法边界在局部最短保留 | repair plan 原建议由第 11 节 Interpretation matrix 承担权威汇总；因本轮直接约束及 PCR-010 明确指定第 14 节为唯一权威位置，改在第 14 节完成同一整合功能，第 11 节只保留非空的局部分析处置矩阵 |

## Language findings

| Finding | Revised locator | Operation | Retained content | Deleted or moved content | Scientific meaning changed | Protected-content disposition | Unexecuted item and reason |
|---|---|---|---|---|---|---|---|
| TERM-01 | 标题、摘要、目标 4、方法、证据链和 Claim-Support 表 | replace、define | 保留 EXIT-SEP 与 XBJ-SCAP 的实际访视和重复测量稀疏性 | 将悬空的“稀疏 RCT”统一改为“访视稀疏随机对照试验”，首次出现说明稀疏对象是访视时点和可用重复测量 | 否 | PCR-005 的试验数据状态与 PCR-011 的阶段关系不变 | 无 |
| TERM-02 | 结构式摘要、主要问题、目标 4、试验方法、证据链、产出与 Claim-Support 表 | define、replace | 保留由阶段 II 观测方程和共同锚点构造 P_obs 的公式、用途、映射检验与试验特异性 | 多种“投影可观测摘要”名称统一为“一维可观测状态摘要”；在公式前区分模型状态投影 P_state 与试验可计算摘要 P_obs | 否 | PCR-006、PCR-008 的观测模型、映射和估计目标不变 | 无 |
| TERM-03 | 标题、一语摘要、结构式摘要、主要问题、目标和全文同层级名称 | define、standardize | 保留患者状态、状态转移、治疗行动和测量过程的关系，以及只解释可恢复不变量的边界 | 核心对象统一为“候选动态系统表征”；状态、观测模型和任务输出只作为有明确定义的下层对象 | 否 | PCR-001、PCR-002、PCR-003 保留同义 | 无 |
| TERM-04 | 结构式摘要、时间节点、跨数据库方法、证据链、产出和贡献 | define、standardize | 保留医院级拆分、适配集、独立最终测试、零更新先行、仅校准、仅观测模型更新和全模型重拟合的四层顺序 | 将“真正外部”“运输性检验”“外部门”等改为“独立保留数据库上的零更新外部验证”“适配后校准”“观测模型更新”和“可迁移性更新” | 否 | PCR-006、PCR-007 保留同一外部验证顺序和合取标准 | 无 |
| TERM-05 | 结构式摘要、试验方法、证据链、计划产出、贡献和第 14 节 | define、replace | 保留死亡、住院存活和活着出院的三层排序及 SOFA 或 P_obs 排序方向 | 英文 `death-ranked` 改为“死亡优先排序”；首次出现即定义三个层级 | 否 | PCR-005、PCR-008 的试验端点和语义要求不变 | 无 |
| TERM-06 | 摘要、时间节点、模拟、外部验证、试验方法、技术清单和风险表 | replace、define | 保留 G1、R0、R1 的评价对象、阈值性质及不满足后的分析后果 | 将“绝对恢复门”“假置信门”“观测投影门”“语义门”和“准入门”改为具体检验或核验名称；代码标签仅在定义后使用 | 否 | PCR-006、PCR-007、PCR-008 的全部标准和失败路线不变 | 无 |
| REG-01 | 全文读者可见正文和表格 | replace | 保留预先锁定、数据隔离、采用替代分析和停止分析的实际功能 | 将“按门实施”“打开测试”“封印”“挽救”“防火墙”“降级”等流程化隐喻改为标准研究语言；固定合同标题除外 | 否 | PCR-010、PCR-011 的触发与后果保持同强度 | 无 |
| REG-02 | 摘要、方法、证据链和风险内容 | replace、moderate | 保留独立最终测试、绝对阈值和禁止越级的必要强度 | 将“真正”“永不”“强制”等强调语改为可核查的条件与后果；必要的禁止性边界集中到第 14 节 | 否 | PCR-012 保持同等禁止边界 | 无 |
| CON-01 | 摘要、核心假设、Evidence chains、Required analyses、Expected outputs、Contribution 和 Claim-Support | consolidate、delete | 保留每条局部方法、证据链和主张审计所需的最短限定 | 删除零更新、独立 SOFA、机制禁令和阶段停止条件的同义重复；完整版本集中到第 14 节 | 否 | PCR-010、PCR-011、PCR-012 均在权威位置完整保留 | 无 |
| CON-02 | 全文，重点为摘要、目标、方法公式前说明、技术清单与表格 | split、expand | 保留所有变量、时间点、阈值、估计目标和分析集 | 将斜线并列改为“以及”“或”“分别”；拆分连续名词链，并在缩写首次出现处给出中文名称 | 否 | PCR-006、PCR-008 的设计承诺不变 | 无 |
| READ-01 | 一语摘要 | replace、shorten | 保留研究对象、阶段 I–II 主问题、24 个月时间界限和阶段 III 从属关系 | 逐项标准、访视、观测映射计算、独立端点细节和完整解释边界移至相应专节 | 否 | PCR-001、PCR-002、PCR-011 同义保留 | 未按方向性建议拆成多句，因为固定字段要求 `One-sentence`；通过缩短为两个并列主干的单句完成可读性目标 |
| READ-02 | Primary research question、Core hypothesis and non-hypotheses、试验公式前导引 | split、add_bridge | 保留主问题的三个科学层次、核心假设条件、P_state 和 P_obs 公式及全部阈值 | 将替代分析从主问题长句中分为后续短句；在公式前新增“资料核验—共同指标—映射—外部检验—试验比较—替代分析”的普通语言路线 | 否 | PCR-001、PCR-006、PCR-008 保留同义 | 无 |

## Protected-content disposition

| Protected ID | Disposition in v004 | Locator |
|---|---|---|
| PCR-001 | retained_same_meaning | frontmatter identity anchor；Primary research question；Title summary |
| PCR-002 | retained_same_meaning | frontmatter；Objectives；Research content and work packages |
| PCR-003 | retained_same_meaning | frontmatter；Structured abstract；Research design and methods |
| PCR-004 | retained_same_status | Data, materials, and existing evidence base；第 14 节 assumptions item 1–2 |
| PCR-005 | retained_same_status | Local RCT evidence and present limits；试验方法；第 14 节 assumptions item 8–9 |
| PCR-006 | retained_same_meaning | Work packages；Research design and methods；Evidence chains |
| PCR-007 | retained_same_meaning | Conjunctive minimum success definition；跨数据库验证方法；第 14 节解释矩阵 |
| PCR-008 | retained_same_meaning | Protocol locks；Mutually exclusive state system；Required analyses |
| PCR-009 | retained_same_strength | Structured abstract；Contribution and evidence ladder；Claim-Support 表 |
| PCR-010 | retained_once_at_authority_location | 第 14 节 assumptions、interpretation boundaries、risk matrix、remaining execution gates |
| PCR-011 | retained_once_at_authority_location | 第 14 节 assumptions item 7、interpretation boundaries、identity and final stop boundary |
| PCR-012 | retained_same_boundary | Core hypothesis 中保留身份所需最短限定；第 14 节 authoritative interpretation boundaries 完整陈述 |

## Outputs written

1. `tests/idea-narrative-forward-0.9.0-preview.3/one-pass/revised/idea-dossier-v004.md`
2. `tests/idea-narrative-forward-0.9.0-preview.3/one-pass/revised/revision-delta-v003-to-v004.md`

## Unresolved items

- **Editorial repair actions or language findings left unexecuted:** 无。READ-01 的多句形式建议未采用，但其可读性目标已在固定单句字段内完成；NRP-005 的权威位置按本轮直接约束和 PCR-010 调整到第 14 节。
- **Scientific content requiring invention:** 无。输入不足以核验的访问、团队、G1、模型、外部结果和试验原始语义均保持为未核验或尚未生成，并集中列入第 14 节。
- **Readiness judgment:** 未作判断。

## Lint result

- **Command:** `python research-skills-openai/skills/multi-path-idea-generator/scripts/lint_idea_dossier.py tests/idea-narrative-forward-0.9.0-preview.3/one-pass/revised/idea-dossier-v004.md`
- **Exit code:** `0`
- **Result:** `OK: tests\idea-narrative-forward-0.9.0-preview.3\one-pass\revised\idea-dossier-v004.md`
- **Errors:** 无。
- **Warnings:** 无。
