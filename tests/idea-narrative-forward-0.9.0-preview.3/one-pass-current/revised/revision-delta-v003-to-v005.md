---
schema_version: research-idea.v3
plugin_version: 0.9.0-preview.3
artifact_id: revision-delta-I01-001-v003-to-v005
workflow_id: RID-SEPSIS-CSM-20260717-001
idea_id: I01-001
version_id: v005
from_dossier_ref:
  artifact_id: idea-dossier-I01-001-v003
  version: v003
  path: tests/idea-test-0.9.0-preview.1/0.9.0-preview.1/03_ideas/nodes/I01-001/dossiers/idea-dossier-v003.md
to_dossier_ref:
  artifact_id: idea-dossier-I01-001-v005
  version: v005
  path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/revised/idea-dossier-v005.md
based_on:
  - tests/idea-test-0.9.0-preview.1/0.9.0-preview.1/03_ideas/nodes/I01-001/dossiers/idea-dossier-v003.md
  - tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/baseline/narrative-repair-plan-r014.yaml
  - tests/idea-narrative-forward-0.9.0-preview.3/one-pass/baseline/language-assessment-r010.md
  - tests/idea-narrative-forward-0.9.0-preview.3/run-001/inputs/protected-content-register.yaml
source_skill: multi-path-idea-generator
created_round: 1
change_type: editorial_repair_delta
identity_status: preserved
scientific_change_declared: false
frozen: true
---

# Revision delta: idea-dossier v003 to v005

## Scope

本次变更是一次完整 dossier 的编辑修复。研究问题、主要目标、研究对象、核心数据与证据基础、主要推断单位、分析设计、阈值、条件分支、可行性状态和主张强度均未改变；未增加未经审查的科学内容，也未把计划工作写成既有结果。

## Input binding

本次修复只依据以下四个冻结输入：

1. `tests/idea-test-0.9.0-preview.1/0.9.0-preview.1/03_ideas/nodes/I01-001/dossiers/idea-dossier-v003.md`
2. `tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/baseline/narrative-repair-plan-r014.yaml`
3. `tests/idea-narrative-forward-0.9.0-preview.3/one-pass/baseline/language-assessment-r010.md`
4. `tests/idea-narrative-forward-0.9.0-preview.3/run-001/inputs/protected-content-register.yaml`

## Narrative action disposition

| Action | Disposition | Revised location and result |
|---|---|---|
| NRP-001 | completed | 第 3 节拆分为且仅包含依次排列的 Background、Current state、Gap、Significance 和 Rationale 五个 H3；每项承担独立读者功能，Rationale 将双时钟、变量角色分离、模拟恢复、独立外部数据库检验和条件性试验分析逐项连接到缺口。 |
| NRP-002 | completed | 第 1 节的一句话完整 Idea 摘要改为先说明研究对象、24 个月公共 ICU 证据路径和独立保留数据库检验，再说明试验层的条件地位；实施细节移入方法。 |
| NRP-003 | completed | 结构式摘要保留五项合同字段，按问题与缺口、目标与假设、总体方法、计划结果、贡献展开；专门概念在首次出现时以科学功能解释。 |
| NRP-004 | completed | 第 14 节成为资源、假设、限制、风险、替代方案和停止条件的唯一完整权威；其他章节只保留完成本节科学功能或解释紧邻设计选择所需的最小边界，未新增跨节指针。 |
| NRP-005 | completed | 五条证据链各自只保留 Input、Method / analysis / processing、Output 和 Supports；删除全部链级限制字段。 |
| NRP-006 | completed | Required analyses and evidence 只列可核查交付与记录，不再成组复述月份路线、完整方法和限制清单。 |

## Language action disposition

| Finding | Disposition | Editorial repair |
|---|---|---|
| TERM-01 | addressed | 标题和正文统一为“访视稀疏随机对照试验的条件性次要分析”，明确稀疏对象是访视时点与可用重复测量。 |
| TERM-02 | addressed | 统一主名称为“一维可观测状态摘要”，首次出现即说明其由实际访视共同生理指标和阶段 II 预先确定的观测模型计算；P_state 与 P_obs 在方法中分别定义。 |
| TERM-03 | addressed | 统一核心对象为“候选动态系统表征”，并在第 1 节定义其包含患者状态、状态转移、生理观测、治疗行动和测量过程；次级对象按层次命名。 |
| TERM-04 | addressed | 区分“不更新模型的独立外部数据库验证”“只利用适配区的校准更新”“观测模型更新”和“新的迁移开发分析”，避免以多个名称指代同一分析。 |
| TERM-05 | addressed | 将英文复合端点改为“死亡优先排序的一维可观测状态摘要”与“死亡优先排序的 SOFA 复合状态端点”，并在方法中明确三层排序。 |
| TERM-06 | addressed | 将流程化的“门”改为“审计”“预设绝对标准”“合格标准”或“资料语义核验”，每项均说明评价对象、判定标准和不满足时的分析处理。 |
| REG-01 | addressed | 将“准入、打开 test、挽救、封印、防火墙”等内部流程隐喻改为标准研究设计表述。 |
| REG-02 | addressed | 将“真正外部、绝对门、强制、永不”等强调词改为“独立保留数据”“预设绝对阈值”和具体条件—后果表述。 |
| CON-01 | addressed | 合并跨章节重复的限制与禁止性解释；完整限制集中在第 14 节，预期结果、贡献和 claim-support 表各自只保留独有功能。 |
| CON-02 | addressed | 减少斜线并列和连续名词链，将逻辑关系改写为完整短语、短句或列表。 |
| READ-01 | addressed | 一句话摘要缩减为研究对象、总体证据路径、24 个月边界和条件性试验层，不再承载全部实现细节。 |
| READ-02 | addressed | 主要研究问题拆为三个平行问题；核心假设将适用条件、可观察量和解释范围分开陈述。 |

## Protected-content disposition

| Protected ID | Required disposition | Actual disposition | Revised location |
|---|---|---|---|
| PCR-001 | retained_same_meaning | retained_same_meaning | Frontmatter identity anchor；Research question, objectives, and core hypothesis；Title, summary, audience, and positioning |
| PCR-002 | retained_same_meaning | retained_same_meaning | Frontmatter identity anchor；Research question, objectives, and core hypothesis；Research content and work packages |
| PCR-003 | retained_same_meaning | retained_same_meaning | Frontmatter identity anchor；Title, summary, audience, and positioning；Research design and methods |
| PCR-004 | retained_same_status | retained_same_status | Data, materials, and existing evidence base；Feasibility and resources；Limitations and boundary conditions |
| PCR-005 | retained_same_status | retained_same_status | Data, materials, and existing evidence base；Conditional trial observation mapping and independent alternative；Limitations and boundary conditions |
| PCR-006 | retained_same_meaning | retained_same_meaning | Research content and work packages；Research design and methods；Key techniques and implementation |
| PCR-007 | retained_same_meaning | retained_same_meaning | Conjunctive minimum success definition；Hospital-based cross-database validation；Expected outputs, falsification criteria, and interpretations；第 14 节 |
| PCR-008 | retained_same_meaning | retained_same_meaning | Protocol definitions for the two primary clinical tasks；Mutually exclusive post-onset state and event system；Required analyses and evidence |
| PCR-009 | retained_same_strength | retained_same_strength | Structured abstract；Contribution, innovation, impact, application, and closest-work comparison；Title and positioning claim-support table |
| PCR-010 | retained_once_at_authority_location | retained_once_at_authority_location | Feasibility, resources, risks, alternatives, and stop conditions（第 14 节） |
| PCR-011 | retained_once_at_authority_location | retained_once_at_authority_location | Feasibility, resources, risks, alternatives, and stop conditions（第 14 节）；Research content 仅保留时间范围和顺序的独有功能 |
| PCR-012 | retained_same_boundary | retained_same_boundary | Core hypothesis and non-hypotheses 保留研究目标定义所需最小边界；第 14 节完整保留因果与临床解释边界 |

## Structural disposition

- 保留一个 H1，且与第 1 节 Title 字段完全一致。
- 保留 15 个必需 H2，顺序不变。
- 第 3 节保留且仅保留五个必需 H3，顺序为 Background、Current state、Gap、Significance、Rationale。
- 保留五条完整证据链；每条严格使用四个字段。
- Claim-support 表删除独立限定语列；所有 qualified 主张直接写在受支持范围内。
- 新 dossier 与本 delta 均绑定 `plugin_version: 0.9.0-preview.3`；dossier 的 `change_type` 为 `editorial_repair`，delta 的 `change_type` 为 `editorial_repair_delta`。

## Downstream status

本 delta 不作叙事、语言、科学内容保存或 Idea 质量判定。v005 需要由新的独立实例进行内容保存核验以及叙事和语言复评。
