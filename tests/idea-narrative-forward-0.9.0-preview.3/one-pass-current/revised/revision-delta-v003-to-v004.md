---
schema_version: research-idea-revision-delta.v1
artifact_id: revision-delta-I01-001-v003-to-v004
workflow_id: RID-SEPSIS-CSM-20260717-001
idea_id: I01-001
from_version: v003
to_version: v004
based_on:
  - artifact_id: idea-dossier-I01-001-v003
    version: v003
    path: tests/idea-test-0.9.0-preview.1/0.9.0-preview.1/03_ideas/nodes/I01-001/dossiers/idea-dossier-v003.md
  - artifact_id: narrative-repair-plan-I01-001-r013
    version: r013
    path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/baseline/narrative-repair-plan-r013.yaml
  - artifact_id: language-assessment-I01-001-r010
    version: r010
    path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass/baseline/language-assessment-r010.md
  - artifact_id: protected-content-register-I01-001-v003
    version: v003
    path: tests/idea-narrative-forward-0.9.0-preview.3/run-001/inputs/protected-content-register.yaml
revised_artifact:
  artifact_id: idea-dossier-I01-001-v004
  version: v004
  path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/revised/idea-dossier-v004.md
source_skill: multi-path-idea-generator
change_type: editorial_repair_delta
identity_status: preserved
---

# Revision delta: idea-dossier-I01-001 v003 → v004

## Scope

本轮仅执行叙事结构和学术语言修订。研究问题、研究对象、主要目标、数据基础、推断单位、数值阈值、分析顺序、可行性状态、证据强度和条件分支均未改变。未新增科学、统计或临床选择。

## Narrative repair actions

| Action | Disposition in v004 |
|---|---|
| NRP-001 | 第 3 节改为严格依次出现的 Background、Current state、Gap、Significance 和 Rationale 五个 H3。意义小节说明区分任务效度、可恢复性和外部稳定性的价值；设计理由逐项回连双时钟、过程分离、模拟恢复、独立外部验证和条件性试验扩展。 |
| NRP-002 | 标题仅保留 24 个月阶段 I–II 主轴。第 1 节先定义候选动态系统表征、主要证据路线和条件性贡献，再用独立条目说明 24 个月后试验扩展及其依赖关系。 |
| NRP-003 | 主研究问题只定义阶段 I–II。条件性扩展另列为独立问题；四项目标保留原顺序，并明确前三项属于阶段 I–II、第四项属于阶段 III。 |
| NRP-004 | 五条证据链均删除完整限制字段，只保留 Input、Method / analysis / processing、Output 和 Supports。完整限制、假设、风险、替代方案与停止条件集中至第 14 节；其他章节只保留直接决定相邻设计或本节功能的最短边界。 |
| NRP-005 | 结构化摘要先用普通科学语言说明两项主要任务、模拟恢复、独立外部验证和条件性试验扩展。项目内短标签不再承担首次解释；数学符号和数值标准保留在方法专节，并在公式前增加普通语言路线。 |

## Language repairs

| Finding | Disposition in v004 |
|---|---|
| TERM-01 | 删除标题中的“稀疏 RCT”。正文统一为“访视稀疏随机对照试验的条件性次要分析”，明确稀疏对象是访视和重复测量。 |
| TERM-02 | 核心试验对象统一为“一维可观测状态摘要”；首次出现时说明其由实际访视共同生理指标经阶段 II 预定观测模型计算并用于排序比较。P_state 与 P_obs 在方法中分别定义。 |
| TERM-03 | 核心研究对象统一为“候选动态系统表征”；首次出现时将其定义为连接患者状态、状态转移、治疗过程和观测过程的统计表征。 |
| TERM-04 | 主要外部分析统一为“独立保留数据库上的外部验证”或“不更新参数的主要外部验证”；“仅用适配集的校准更新”“观测模型更新”和“新的模型开发”分别命名。 |
| TERM-05 | `death-ranked SOFA` 改为“死亡优先排序 SOFA 复合状态端点”，并在摘要首次出现时说明死亡、住院存活和活着出院的排序。 |
| TERM-06 | 将“恢复门”“假置信门”“投影门”“语义门”等改为“基于预设绝对阈值的模拟恢复检验”“错误高置信判断检验”“观测映射合格标准”和“试验资料语义核验标准”。 |
| REG-01 / REG-02 | 用“预设标准”“符合分析条件”“不进入下一分析阶段”“采用预设替代方案”“独立保留测试集”等研究设计用语替换流程隐喻和强调性措辞。 |
| CON-01 / CON-02 | 删除证据链限制字段及多处完整限制复述；拆解斜线并列和连续名词链，在各章节只保留其独有功能。 |
| READ-01 / READ-02 | 将开篇信息分为核心摘要、定位和阶段 III 扩展；将主研究问题与条件性扩展问题分开；核心假设拆分为可检验假设和简短非假设声明。 |

## Protected-content disposition

| Protected ID | Required disposition | v004 disposition | Location and preservation note |
|---|---|---|---|
| PCR-001 | retained_same_meaning | retained_same_meaning | Frontmatter identity anchor；第 1、3、4、7 节。保留以脓毒症为中心的发病前、首次发病、发病后互斥状态与结局连续体；没有改成普通预测或泛 ICU 风险分层。 |
| PCR-002 | retained_same_meaning | retained_same_meaning | Frontmatter；第 1、4、5 节。保留 24 个月内完成阶段 I–II、文献和专家知识约束、公共 ICU 数据、系统辨识及跨数据库验证；产物仍定位为可审计科学证据与基准资源。 |
| PCR-003 | retained_same_meaning | retained_same_meaning | Frontmatter；第 4、7 节。保留纵向 ICU 患者系统、未发病在险时段、发病后轨迹，以及尊重患者和医院聚类的患者—时间状态与状态转移推断单位。 |
| PCR-004 | retained_same_status | retained_same_status | 第 6、14 节。保留文献和专家先验、MIMIC-IV、eICU-CRD 及 HiRID/AmsterdamUMCdb 条件性备份；访问、DUA、可运行提取、项目队列、具名人员和结果仍为未核验或尚未生成。 |
| PCR-005 | retained_same_status | retained_same_status | 第 1、6、7、14 节。保留 EXIT-SEP 和 XBJ-SCAP 仅为条件性阶段 III 来源；现有材料仍明确为不能替代授权、原始 CRF/SAP 及试验语义核验的衍生报告。 |
| PCR-006 | retained_same_meaning | retained_same_meaning | 第 5、7、8、9 节。保留资源和可观测性审计、锁定标签与拆分、简单模型、模拟恢复、至多一个复杂候选、两主两次任务、冻结、独立外部验证、条件性试验扩展的顺序；保留状态、治疗和观测过程分离及解释约束。 |
| PCR-007 | retained_same_meaning | retained_same_meaning | 第 5、7、10、14 节。保留阶段 II 的数据支持、模拟恢复、适当评分、校准、泄漏清除、无参数更新外部表现、对齐和结构稳定性的合取定义；适配后分析及阶段 III 均不能替代主要外部验证失败。 |
| PCR-008 | retained_same_meaning | retained_same_meaning | 第 7 节。保留两项主要任务、事件与可用时间双时钟、首次发病风险集、延迟进入、互斥状态、竞争终止、当时可用特征、校准和适当评分、患者及医院聚类不确定性和泄漏防护，包括所有原数值标准。 |
| PCR-009 | retained_same_strength | retained_same_strength | 第 1、2、6、12、13、14 节。保留当前没有模型或结果、贡献仅为条件性整合与验证及基准资源、各模块已有先例、完整组合缺口仅低至中等置信度，并明确不主张全球首次或新算法。 |
| PCR-010 | retained_once_at_authority_location | retained_once_at_authority_location | 第 14 节集中保留资源与访问、团队、双库支持、标签与泄漏、可恢复性、非随机缺失和低重叠、外部可迁移性、时间、试验资料语义、共同锚点、观测映射和最接近工作不确定性，以及各触发条件的替代或停止后果。 |
| PCR-011 | retained_once_at_authority_location | retained_once_at_authority_location | 第 14 节最终段为权威陈述：阶段 I–II 必须在 24 个月内完成；阶段 III 位于最低交付之外，依赖阶段 II 成功与试验条件，不能补足阶段 II 失败。第 1、4、5 节仅保留界定研究层级所需的局部短句。 |
| PCR-012 | retained_same_boundary | retained_same_boundary | 第 4 节保留界定研究身份所需的简短非假设声明；第 14 节完整保留观察性和随机试验证据均不支持因果网络、治疗因果作用、潜在动力学、转移边、中介、控制、数字孪生、临床工具、药物平台或无条件推广。 |

## Structural disposition

- 保留 research-idea.v3 的 15 个必需 H2，顺序不变。
- 第 3 节仅含依次排列且非空的 Background、Current state、Gap、Significance 和 Rationale 五个 H3。
- 五条 evidence chain 均且仅含 Input、Method / analysis / processing、Output 和 Supports。
- 第 13 节删除 `Required qualifier` 列；所有 qualified 主张已直接写在受支持范围内。
- 第 14 节为唯一完整 limitations、assumptions、risks、alternatives 和 stop conditions 权威位置。

## Handoff

本次仅建立新的完整 dossier 版本和配对 delta。未作叙事、语言、科学或方法学自评，也未声明准备就绪；后续状态应由新的独立评估实例确定。
