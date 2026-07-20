---
schema_version: research-idea-revision-delta.v1
artifact_id: revision-delta-I01-001-v009-to-v011
workflow_id: RID-SEPSIS-CSM-20260717-001
idea_id: I01-001
version_id: v009-to-v011
path: tests/idea-narrative-forward-0.9.0-preview.3/run-001/release/revision-delta-v009-to-v011.md
from_dossier_ref:
  artifact_id: idea-dossier-I01-001-v009
  version: v009
  path: tests/idea-narrative-forward-0.9.0-preview.3/run-001/release/idea-dossier-v009.md
to_dossier_ref:
  artifact_id: idea-dossier-I01-001-v011
  version: v011
  path: tests/idea-narrative-forward-0.9.0-preview.3/run-001/release/idea-dossier-v011.md
based_on:
  - artifact_id: idea-dossier-I01-001-v009
    version: v009
    path: tests/idea-narrative-forward-0.9.0-preview.3/run-001/release/idea-dossier-v009.md
  - artifact_id: idea-dossier-I01-001-v010
    version: v010
    path: tests/idea-narrative-forward-0.9.0-preview.3/run-001/release/idea-dossier-v010.md
  - artifact_id: content-preservation-I01-001-r007
    version: r007
    path: tests/idea-narrative-forward-0.9.0-preview.3/run-001/release/content-preservation-r007.md
  - artifact_id: protected-content-register-I01-001-v009
    version: v009
    path: tests/idea-narrative-forward-0.9.0-preview.3/run-001/release/protected-content-register-v009.yaml
  - artifact_id: revision-delta-I01-001-v009-to-v010
    version: v009-to-v010
    path: tests/idea-narrative-forward-0.9.0-preview.3/run-001/release/revision-delta-v009-to-v010.md
source_skill: multi-path-idea-generator
created_round: 8
change_type: editorial_repair_delta
---

# Revision delta: idea dossier v009 to v011

## Scope and outcome

v011 是针对 content-preservation r007 两项 blocking finding 的窄范围保真修复。它保留 v010 的其他叙事与语言编辑，只撤销两项未经授权的方法选择：医院规模分层指标不再被具体化，主要临床任务的 95% 上置信限也不再被具体化为任何特定区间构造。两项内容均改为范围明确、冻结时间与隔离条件明确的待定规范。

本次修复没有改变研究身份、问题、目标、对象、推断单位、数据角色、研究范围、主要任务、验证路线、数值门槛、判定方向、证据状态、主张强度、限制、替代方案或停止条件；没有新增方法、数据、结果、引文、外部证据或主张。使用的项目输入仅为 frontmatter 中列出的五个逻辑引用。

## Preserved v010 editorial outcomes

以下 v010 编辑成果原样保留：

- 完整构想摘要、概念桥和四类证据区分先于三阶段导航；三阶段导航保持三条并行说明，完整时间表仍在 section 5。
- structured abstract 的总问题、待恢复对象及状态对齐和预设结构稳定性定义保持拆分后的可读结构。
- 主要研究问题保持三个依赖顺序明确的编号问题。
- XBJ-SCAP 的 671 人群继续用中文操作定义表述，并保留“全分析集且基线 SOFA 至少 2 分”的原有含义。
- 阶段 III 的局部导航仍只保留其依赖阶段 II 成功且不改变阶段 II 独立成败的最短边界。
- v010 其余术语统一、重复删除、section 14 集中化以及所有研究设计、证据链、阈值和引用均保持不变。

## r007 blocking findings and corrective disposition

| r007 finding | Protected item | v010 scope violation | v011 corrective disposition | Protected elements retained unchanged |
|---|---|---|---|---|
| CPR-007-F001 / USC-001 | PCR-020 | 把尚未冻结的 95% 上置信限具体化为一种区间上限，并附带改用另一种置信界的分支 | 删除全部特定区间类型及切换分支。阈值表恢复为“95% 上置信限”；section 14 明确待确认的是该上置信限的具体构造，并规定在月 6 前、模型拟合和查看任何预先隔离外部验证结果前冻结 | +0.01 阈值；上置信限高于 +0.01 即任务不获支持的方向；校准斜率 0.80–1.20；绝对风险误差 0.02；次要诊断、试验结果或复杂模型不得替代失败 |
| CPR-007-F002 / USC-002 | PCR-021 | 把“合格体量四分位”具体化为一个医院层指标，并附带更换分层变量和重做分组的分支 | 删除该具体指标及更换分支。方法段只说明医院规模指标的具体定义尚待冻结；section 14 明确待确认的是指标及计算定义，并规定在月 4–6 双数据库审计完成后、查看验证结局或模型表现前、验证数据仍由独立数据保管人隔离且不释放结果时冻结 | 接口完整性分层；医院标识符；固定种子 20260717；30% 适配医院和 70% 预先隔离验证医院；结局前冻结；跨分区患者排除、报告和敏感性分析 |

这两项修复将 PCR-020 与 PCR-021 回退到 protected-content register v009 允许的范围：保留已固定的阈值、方向、比例、随机种子、隔离和停止后果，不替研究方案选择尚未冻结的统计或验证设计规范。r007 已记录为 preserved 的其余 37 项不受本轮编辑影响。

## Section 14 authority and local boundaries

Section 14 继续作为 assumptions、limitations、feasibility findings、interpretation boundaries、alternatives、contingencies 和 stop conditions 的唯一完整权威位置。两项待定规范的完整内容只在 section 14 各陈述一次。

其他位置仅保留推进紧邻设计所必需的最短局部说明：医院分组段说明医院规模指标在验证结果隔离下先冻结再分组；主要任务阈值行说明 95% 上置信限的构造在月 6 前、模型拟合和外部结果访问前冻结。未增加重复的全局限制或跨节指引。

## Lineage and verification

- v011 以 v010 为直接叙事基础，以 v009 和 protected-content register v009 为受保护内容基线，并以 content-preservation r007 和 v009-to-v010 delta 界定本次修复范围。
- dossier 绑定已更新为 `idea-dossier-I01-001-v011`、`v011` 和准确的 release 路径；研究身份状态仍为 `preserved`，产物仍为冻结的完整 dossier。
- generator structural lint 已通过，退出码为 0。
- 本 delta 不作叙事、语言、保真或科学质量判定。v011 发生实质性产物变更后，仍须由新的独立实例重新进行适用的保真与后续评估。
