---
schema_version: research-idea-revision-delta.v1
plugin_version: "0.10.0"
artifact_id: revision-delta-I01-001-v004-to-v005
workflow_id: sepsis-complex-system-idea-generation-v001
idea_id: I01-001
round_id: round-004
version_id: v004-to-v005
path: 03_ideas/nodes/I01-001/revisions/round-004/revision-delta-v004-to-v005.md
based_on:
  - artifact_id: idea-dossier-I01-001-v004
    version: v004
    path: 03_ideas/nodes/I01-001/dossiers/idea-dossier-v004.md
  - artifact_id: methodology-statistics-preflight-I01-001-r004
    version: r004
    path: 03_ideas/nodes/I01-001/reviews/preflight-r004.md
output:
  artifact_id: idea-dossier-I01-001-v005
  version: v005
  path: 03_ideas/nodes/I01-001/dossiers/idea-dossier-v005.md
change_type: scientific_revision_delta
identity_status: preserved
---

# Idea dossier v004 至 v005 修订差异

## 修订摘要

本次修订没有更换全病程复杂系统研究身份、潜在状态模型或四任务设计；它只把任务三的外部验证对象从可能误读为潜在状态恢复的表述，统一为对被有意遮蔽但实际测得的临床变量进行预测。

| 修订位置 | v005 的同步结果 |
|---|---|
| Frontmatter | 版本更新为 v005；`based_on` 直接绑定 v004 dossier 与 preflight-r004；`change_type` 为 `scientific_revision`。 |
| 身份锚点与读者主线 | 主要问题、目标、摘要、研究问题和核心假设均把任务三写为从部分已观测历史预测遮蔽实测临床变量；研究对象、核心数据、患者级推断单位与其余任务保持不变。 |
| 任务三方法与推断 | 保留 12 小时连续遮蔽、九个结果域等权、域内变量/遮蔽块/预测起始时点等权、逆观测概率权重、负对数评分、两类冻结比较模型、患者级最不利平均损失差及原有置信界与 Holm 判定；明确潜在状态不是任务三的真值、标签或验证端点。 |
| 证据与解释 | 证据链、预期输出、结果模式和 Claim-Support 将任务三输出限定为遮蔽实测变量的预测比较；成功只支持测量补全用途，不支持潜在生理状态恢复。 |
| 第 14 节权威说明 | Working assumptions 一次性记录公开观察性重症监护数据没有潜在状态金标准，说明用户“补全未观测的其他状态”准则以留出实测变量操作化，并记录解释风险；资格审计仍须实证确认共同目标变量、可评分遮蔽块、权重稳定性和外部可执行性。 |

## 保持不变的科学内容

保留全病程复杂系统核心 Idea、任务一/二/四、开发期潜在状态可辨识性诊断、数据库资格与冻结顺序、全部比较模型和多重性控制、状态迁移诊断、资源与时间安排、限制与停止条件、随机试验和动物研究的条件性地位、参考文献及原有主张强度；未增加结果、证据或数值阈值。

## 验证记录

- 运行 `python research-skills-openai/skills/multi-path-idea-generator/scripts/lint_idea_dossier.py tests/脓毒症复杂系统模型/03_ideas/nodes/I01-001/dossiers/idea-dossier-v005.md --expected-plugin-version 0.10.0`：通过，无错误或提示。
- 精确结构检查：15 个 H2 章节及第 3 节五个 H3 功能顺序正确，H1 与 Title 一致，一句话摘要非空，插件版本、artifact ID、版本、路径和两个 `based_on` 逻辑引用正确，且未使用 `editorial_repair`。
- 科学同步检查：旧的“部分观测下状态估计”身份表述不存在；任务三标签、实测留出目标、潜在状态非端点、负对数评分与 `\(\Delta_{3}\)` 角色、校准诊断边界、测量补全解释和资格审计条件均存在；潜在状态金标准与操作化风险的权威说明在 Working assumptions 中出现一次。
- 完整性检查：条件性随机试验与动物研究、28 条参考文献以及其余任务、方法和停止条件均保留；v004→v005 差异仅涉及逻辑血缘、任务三科学同步和为消除 linter 提示而删除的冗余英文括注，未新增结果、证据或阈值。
