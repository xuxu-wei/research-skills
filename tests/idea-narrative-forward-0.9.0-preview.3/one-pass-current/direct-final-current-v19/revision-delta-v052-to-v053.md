---
schema_version: research-idea.revision-delta.v1
plugin_version: 0.9.0-preview.3
artifact_id: revision-delta-I01-001-v052-to-v053
workflow_id: RID-SEPSIS-CSM-20260717-001
idea_id: I01-001
from_dossier:
  artifact_id: idea-dossier-I01-001-v052
  version: v052
  path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v18/idea-dossier-v052.md
to_dossier:
  artifact_id: idea-dossier-I01-001-v053
  version: v053
  path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v19/idea-dossier-v053.md
based_on:
  - artifact_id: method-clarification-I01-001-r115
    version: r115
    path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v18/method-clarification-r115.md
  - artifact_id: method-clarification-r116
    version: r116
    path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v18/method-clarification-r116.md
source_skill: multi-path-idea-generator
created_round: 116
change_type: scientific_method_clarification
identity_status: preserved
frozen: true
---

# Revision delta: v052 to v053

## Scope

本次修订只落实两项已经独立方法学审查并获条件性通过的科学规格，不属于语言或叙事修复。完整 v053 保留 v052 的标题、摘要、研究身份、研究边界、数据与证据状态、主张强度、24 个月安排、阶段先后和既有停止规则。

## Change index

| 工作假设 | v053 权威位置 | 已落实的科学定义 | 假设不成立或未按时确认的后果 |
|---|---|---|---|
| WA-CCR-001 | 第 7 节“Absolute simulation and semi-synthetic recovery criteria”；第 14 节“Working assumptions” | 连续分支只比较真实连续潜在状态与估计后验均值；每次模拟重复取覆盖全部真实连续维度的最小典型相关；维度不等、任一侧秩不足或无法得到全部相关的奇异情形记为 0；以重复间均值的双侧 95% 正态近似区间下限至少 0.80 作为情景达标条件；系统辨识负责人确认，纵向统计负责人独立复核 | 复杂候选不得依据连续状态恢复晋级，只保留预设的线性、多状态或仅预测路线。若在查看结果后才改变定义，既有连续恢复结论失效，须在结果不可见的重新设计中完成新的独立方法学评估后方可重新考虑复杂候选 |
| WA-R116-PI | 第 7 节“Conditional trial-observation mapping and independent analysis”；第 10 节“Required analyses and evidence”；第 14 节“Working assumptions” | 每项符合启动条件的试验以分层标准化概率指数作为新访视有序结局的唯一主要估计目标，并列对两组各计半分；原随机化层、目标分析集和两治疗组合并后的层权重在任何治疗组结局比较前固定；严格胜概率、胜负比或其他量仅可预设为次要或敏感性分析；每项试验的具名统计负责人须在治疗组比较和分析计划及代码冻结前书面确认 | 停止相应试验新的访视有序结局主要比较，不得改用事后分层或事后切换主要估计目标；仅保留原试验终点复现或数据审计记录。主体阶段 I–II 路线不受影响 |

## Structured working assumptions

```yaml
- assumption_id: WA-CCR-001
  unconfirmed_detail: 连续潜在状态恢复的多维典型相关序列和多次模拟重复如何归约为唯一准入统计量，以及维度、秩和状态对象如何处理。
  working_assumption: >-
    连续分支只评价生成的连续潜在生理状态与其估计后验均值；每次模拟重复先计算覆盖全部真实连续潜在维度的最小典型相关，维度不等、任一侧秩不足或无法得到全部相关的奇异情形记为 0，再以该重复级统计量均值的双侧 95% 正态近似区间下限作为情景级统计量；只有下限至少为 0.80 才达标。
  basis_for_planning: >-
    该定义要求恢复全部真实连续维度，并将蒙特卡洛不确定性纳入准入；它不改变研究问题、临床主要任务或推断对象，且保留既定简单路线。
  impact_if_false: >-
    若系统辨识负责人和纵向统计负责人未在规定时点确认，复杂候选不得凭连续状态恢复晋级，只保留线性、多状态或仅预测路线。若在查看结果后才改变定义，既有连续恢复结论失效，须在结果不可见的重新设计中完成新的独立方法学评估。
  verification_needed: >-
    复核真实连续潜在状态矩阵、估计后验均值、评价格点、维度、秩处理、重复级计算、情景级汇总，以及完全恢复、仅恢复首维和维度不匹配的确定性测试例。
  verification_point: 首次模拟拟合和任何模拟结果查看之前，最迟在月 7 模拟方案与代码冻结时。
  affected_design_component: WP2 的绝对模拟与半合成恢复、复杂候选准入及基于连续状态恢复的结构解释。
  owner: 系统辨识负责人；纵向统计负责人独立复核。
  deadline: 月 7 模拟方案与代码冻结前，且必须早于首次模拟拟合或结果查看。

- assumption_id: WA-R116-PI
  unconfirmed_detail: 条件性试验新访视有序结局的唯一主要估计目标、并列处理、随机化分层和标准化权重尚待责任人书面确认。
  working_assumption: >-
    每项符合启动条件的试验均以分层标准化概率指数作为新访视有序结局的唯一主要估计目标，并列对两组各计半分；原随机化层、目标分析集和两治疗组合并后的层权重在任何组间结局比较前固定。
  basis_for_planning: >-
    有序结局、方向和结构性并列已经给出；该定义不改变结局层级、主体研究问题或试验分析的条件性从属地位。
  impact_if_false: >-
    停止相应试验新的访视有序结局主要比较；在治疗组结果保持不可见时修订估计目标并接受新的独立方法学审查，不得事后切换为严格胜概率、胜负比或其他主要量。主体阶段 I–II 路线和原试验终点复现不受影响。
  verification_needed: >-
    与原始病例报告表、统计分析计划、随机化资料和数据字典核对公式与方向、并列各计半分、目标分析集、原随机化中心或分层因素及两治疗组合并后的层权重。
  verification_point: 每项试验完成核心语义核验后、治疗标签用于任何组间结局计算和分析计划及代码冻结前。
  affected_design_component: 有前置条件的随机试验次要分析中的新访视有序结局主要比较。
  owner: 每项试验的具名统计负责人；项目负责人记录确认。
  deadline: 每项试验分析计划和比较代码冻结前，且早于任何治疗组比较。
```

## Preservation and verification

- 五项 identity anchors 与 `identity_status: preserved` 保持不变。
- `plugin_version: 0.9.0-preview.3`、直接父稿 v052 和 `frozen: true` 已写入 v053。
- 条件性试验仍仅在主体阶段 II 达到合取标准、相应个体资料获授权且核心随机化与访视语义可核验后开展；两项试验仍分别分析，不形成跨试验合并效应，也不计入阶段 II 成功。
- 未修改标题、摘要、背景、研究问题、目标、数据或证据状态、主张强度、24 个月时间表、阶段顺序、限制清单或既有停止规则。
- 已运行 `python research-skills-openai/skills/multi-path-idea-generator/scripts/lint_idea_dossier.py tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v19/idea-dossier-v053.md --expected-plugin-version 0.9.0-preview.3`，结构检查结果为 `OK`。
