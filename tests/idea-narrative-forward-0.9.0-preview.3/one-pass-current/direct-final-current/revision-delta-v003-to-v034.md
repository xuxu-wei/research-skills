---
schema_version: research-idea-revision-delta.v1
plugin_version: 0.9.0-preview.3
artifact_id: revision-delta-I01-001-v003-to-v034
workflow_id: RID-SEPSIS-CSM-20260717-001
idea_id: I01-001
from_version: v003
to_version: v034
change_type: editorial_repair_delta
source_artifact:
  artifact_id: idea-dossier-I01-001-v003
  version: v003
  path: tests/idea-test-0.9.0-preview.1/0.9.0-preview.1/03_ideas/nodes/I01-001/dossiers/idea-dossier-v003.md
revised_artifact:
  artifact_id: idea-dossier-I01-001-v034
  version: v034
  path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current/idea-dossier-v034.md
source_skill: multi-path-idea-generator
frozen: true
---

# Revision delta: idea-dossier v003 → v034

## Scope and identity

本次仅实施叙事与语言修复。主要问题、主要目标、研究对象、核心证据基础和患者—时间状态及状态转移的推断单位均未改变；`identity_status` 保持 `preserved`。修订没有新增科学假设、阈值、数据状态、分析结果或文献主张。

## Repair-plan disposition

| Action | Revised locator | Acceptance evidence |
|---|---|---|
| NRP-050-001 | `Background, current state, gap, significance, and rationale` 的五个 H3 | 五段依次承担问题背景、现有能力、尚未解决的证据连接、误读后果和设计响应；`Gap` 明确写为“该缺口不是‘尚无相同模块组合’本身，而是这些证据层之间缺少可证伪的连接”。投影实现细节仅出现在方法中的 `Conditional trial-observation projection and independent clinical-state analysis`。 |
| NRP-050-002 | `Title, summary, audience, and positioning` 的 complete-Idea summary | 单句由三个顶层分句组成，依次给出研究对象与 24 个月证据路线、24 个月后的条件性分试验扩展、预测与因果边界；未包含 D7/D8、R0/R1、投影公式或降级端点细节。 |
| NRP-050-003 | `Structured abstract`；`Research content and work packages`；`Research design and methods` | 摘要先用科学功能定义阶段 I–II、阶段 III、绝对恢复检验、未触碰外部检验、观测投影摘要和独立等级结局，再在后文引入 G1、R0 和 R1。 |
| NRP-050-004 | `Evidence chains`；`Feasibility, resources, risks, alternatives, and stop conditions` | 五条证据链均只含 Input、Method / analysis / processing、Output 和 Supports；全文完整限制、工作假设、风险、替代和停止条件集中于第 14 节，未使用任何“见第 14 节”式指针。 |

## Language-finding disposition

| Finding | Revised locator | Acceptance-test evidence |
|---|---|---|
| LANG-R050-001 | H1 与 section 1 `Title` | 标题改为“脓毒症全病程候选动态系统表征：计划跨数据库检验与基于 RCT 稀疏访视数据的条件性次要分析”；“稀疏”直接修饰“访视数据”，“条件性”限定次要分析启动。 |
| LANG-R050-002 | `Structured abstract > Approach` 首次出现；section 4 研究问题与目标 4；试验方法 | 首次定义为“由冻结的阶段 II 观测模型根据 EXIT-SEP 第 7 日或 XBJ-SCAP 第 8 日实测指标确定性计算一维状态摘要（下称‘观测投影摘要’）”，并说明用途是“比较随机分配组间的访视摘要差异”；全文不再使用“随机化扰动”。 |
| LANG-R050-003 | `Structured abstract > Approach` 首次出现；试验方法的独立分支 | 首次完整写出“死亡为最差等级、访视时仍住院存活者按 SOFA 评分由高到低排序、访视前存活出院者为最佳等级”，并明确该分支与阶段 II 无关。 |
| LANG-R050-004 | `Structured abstract > Objective and hypothesis / Approach`；section 5 时间表；section 7 R0/R1 | 阶段 I–II 首次定义为公共 ICU 数据上的队列审计、模型恢复与跨数据库检验；阶段 III 定义为其后的 RCT 次要分析；G1、R0、R1 均先写科学判定功能再给简称。一般正文以“预设标准”“判定”“停止”替代裸用“门”。 |
| LANG-R050-005 | H1 与 section 1 首次全称；section 3 后文；section 4 目标 2 | 整体对象统一为“脓毒症全病程候选动态系统表征”及“该候选表征”；`X_t` 明确为“候选表征中的潜在患者状态”，非线性或切换方案明确为“候选表征的复杂模型备选方案”。 |
| LANG-R050-006 | section 3 `Current state`；section 7 各方法小节；section 10 | 首次展开 HMM、MDP、MPC、RL、CIF、ARI、MNAR、ESS、NMAE；一般流程词改为“基准评测与可复用资源”“因数据访问不足而停止”“不作更新”“仅作预测”。`proper scoring rule` 保留英文标准术语，未擅定中文译名。 |
| LANG-R050-007 | complete-Idea summary；section 4 研究问题；section 7 观察性目标与跨库规则 | 单句摘要只有三个顶层分句；研究问题三项各有单一谓语中心；概率式单列并紧跟不依赖符号的自然语言解释；跨库规则按医院分区、患者排除、支持判定与分析层级分段。 |
| LANG-R050-008 | 全文边界陈述；section 14 | 完整非因果、非机制、非系统验证和失败不可挽救清单只在第 14 节集中出现；其他位置仅保留直接限定相邻推理的短句。证据链不再附加限制清单。 |

## Protected-content preservation evidence

下表中的证据均引用 v034 的实际修订文本，而不是章节主题或保存声明。

| Protected ID | Revised locator(s) | Item-level preservation evidence from v034 |
|---|---|---|
| PCR-001 | YAML `identity_anchor`；`Research question, objectives, and core hypothesis > Primary research question` | Frontmatter 原样保留研究问题、研究对象和推断单位；主问题正文明确覆盖“发病前、首次发病、发病后和结局连续体”，并要求医院和数据库间的状态/结构检验，未改成普通预测或泛 ICU 风险分层。 |
| PCR-002 | YAML `identity_anchor.primary_objective`；section 1 summary；section 5 时间表和工作包 | Frontmatter 保留“construct and validate ... within 24 months”；摘要写明“在 24 个月内利用文献与专家先验及两个公共重症监护数据库”构建并检验该候选表征；WP1–WP4 保留系统辨识、恢复、任务验证和跨库验证交付，section 12 将交付定位为整合、验证、基准评测与可复用资源，而非仅预测工具。 |
| PCR-003 | YAML `identity_anchor.study_object / primary_unit_of_inference`；section 4 主问题；section 7 `Protocol locks` | Frontmatter 保留“longitudinal sepsis-centered ICU patient system”、可比较未发病在险时段与发病后轨迹，以及患者—时间状态/转移和患者、医院聚类；方法表保留重叠评估点每住院总权重为 1，并按患者和医院聚类。 |
| PCR-004 | section 6 `Current verified-resource versus prospective status`；`Public ICU database roles and G1 audit` | 表中明确 MIMIC-IV/eICU 的“公开存在、版本和文献已核验”，但“团队凭证、数据使用协议、可运行提取和项目队列支持尚未核验”；HiRID/AmsterdamUMCdb 仍是条件性备份；团队只有角色定义且无具名承诺，候选模型、模拟和外部结果“均未生成”。 |
| PCR-005 | section 6 `Current verified-resource versus prospective status` 与 `Local RCT evidence`；section 14 `Working assumptions` | v034 明确两项本地材料是“衍生清洗和验证材料”，不是原始病例报告表、统计分析计划或独立审计；试验个体数据授权、随机化、中心、访视时序和生存/住院/出院语义仍“尚未核验”，且仅作条件性阶段 III 输入。 |
| PCR-006 | section 5 `minimum route`；section 6 变量角色表；section 7 `Observational target...` | 路线逐项保留“资源与 G1 → 标签、状态和医院拆分锁定 → 简单基线 → 绝对模拟检验 → 至多一个复杂模型备选方案 → 两主两次 → 冻结 → 未触碰外部检验 → 条件性试验”；Y_t、A_t、M_t 分离完整保留；弃权句逐字保留阈值：20 种子对齐<90%、bootstrap 保留<80%、外部符号一致<80%、状态对齐<0.70 或区间未校准时删除、合并或标为数据库/政策特异。 |
| PCR-007 | section 5 `Conjunctive minimum success definition`；section 7 跨库检验；section 14 风险表与末段 | 合取定义逐项保留两库数据支持、绝对恢复、两项主要任务 Brier/校准、泄漏清零、不作更新外部表现、状态对齐≥0.70 和结构符号一致≥0.80；跨库方法分开报告不作更新、只校准和只更新观测层；第 14 节明确“更新成功不算冻结跨库成功”和阶段 III 不能补足阶段 II 失败。 |
| PCR-008 | section 7 `Protocol locks for the two primary clinical tasks`；`Mutually exclusive post-onset state/event system` | 方法表保留标本先时给药在 72 小时内、给药先时采集在 24 小时内；基线 SOFA=0 或入 ICU 前 24 小时最低可计算值；滚动 24 小时最差组件、感染前 48 小时至后 24 小时、首次可排序时刻；仅首次 onset、重叠评估点每住院权重 1；`availability<t`、同格 A_t 与下一状态排序及排除无法排序边；泄漏段逐项保留同格治疗、未来测量频率、重复住院/跨集合和结局驱动网格或阈值检查。两项任务、延迟进入、竞争终止、Brier/校准和聚类不确定性均在同表保留。 |
| PCR-009 | section 1 positioning；structured abstract 的 `Expected result` 与 `Contribution and impact`；section 12 | 摘要明确“这些均为计划产物，并非现有模型或结果”；定位只主张条件性的整合、验证、基准评测与可复用资源；section 12 明确各模块已有代表性近邻、完整连接缺口仅低至中等置信，结论为“而非新算法或全球首次”。 |
| PCR-010 | section 14 全部小节 | `Working assumptions` 逐项列出访问/团队、G1、临床尺度到模拟参数映射、多类别校准估计量/置信界/阈值登记、proper scoring rule 译名、试验授权/语义、共同锚点/R0/R1 和结果未生成；`Limitations` 集中保留标签、数据库差异、MNAR/重叠、模拟范围、外部更新层级、试验稀疏访视与主张边界、closest-work 不确定性；风险表为每项给出触发、替代和停止后果，并明确事件/参数筛选下限不替代经验有效样本量与模拟稳定性，两试验方向不一致或区间过宽时不得挑选亚组挽救。 |
| PCR-011 | section 14 风险表与末段 | 末段明确“阶段 I–II 必须在 24 个月内完成；月 24 无论成功或降级均封存阶段 II”，并规定阶段 III 只在阶段 II 成功及试验数据、语义和观测连接满足条件时开展，“任何试验结果都不能补足资源、恢复、主要任务或未触碰外部检验的失败”。 |
| PCR-012 | section 14 `Limitations and boundary conditions` | 完整边界原文保留：观察性数据和预测表现不支持“真实因果网络、治疗因果效应、反事实策略、机制、中介、控制或数字孪生主张”；试验分支“不验证未测潜在动力学、转移边、完整系统模型或因果机制”；当前也不能支持全球首次、已验证临床决策工具、药物平台或无条件国际临床推广。 |

## Unresolved items

这些事项需要作者、纵向统计负责人、系统辨识负责人或数据持有人确认；输入没有批准答案，因此 v034 未自行填值或改变科学状态：

1. 临床尺度到模拟参数的具体映射。
2. 精确多类别校准估计量、置信界和阈值登记表。
3. `proper scoring rule` 的最终中文译名。
4. 公共库访问、数据使用协议、可运行提取、具名团队和独立数据保管承诺。
5. G1 的实际样本、事件、转移、医院、跨院患者、锚点、接口和复杂度结果。
6. 候选模型、模拟恢复、外部验证和试验新分析结果。
7. 两项试验的个体数据授权、原始病例报告表/统计分析计划、随机化、中心、访视时序和生存/住院/出院语义。
8. 每项试验的共同锚点资格、单位一致性及 R0/R1 结果。

## Files read

- `AGENTS.md`
- `research-skills-openai/skills/multi-path-idea-generator/SKILL.md`
- `research-skills-openai/skills/research-idea-orchestrator/references/idea-artifact-lifecycle.md`
- `research-skills-openai/skills/research-idea-orchestrator/references/idea-dossier-contract.md`
- `research-skills-openai/skills/multi-path-idea-generator/templates/idea-dossier.md`
- `research-skills-openai/skills/multi-path-idea-generator/references/generation-quality-gates.md`
- `research-skills-openai/skills/multi-path-idea-generator/references/downstream-handoff-rules.md`
- `research-skills-openai/skills/multi-path-idea-generator/scripts/lint_idea_dossier.py`
- `tests/idea-test-0.9.0-preview.1/0.9.0-preview.1/03_ideas/nodes/I01-001/dossiers/idea-dossier-v003.md`
- `tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/baseline-current/narrative-repair-plan-r050.yaml`
- `tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/baseline-current/language-assessment-r050.md`
- `tests/idea-narrative-forward-0.9.0-preview.3/run-001/inputs/protected-content-register-v003.yaml`
- `tests/idea-narrative-forward-0.9.0-preview.3/run-001/inputs/reader-handoff.yaml`

## Handoff

- `editorial_assessment_needed: true`
- Fresh narrative and full-dossier language reassessment are required before any evaluation.
- This delta is not an evaluation or readiness verdict.
