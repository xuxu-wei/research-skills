---
schema_version: research-idea-revision-plan.v1
plugin_version: "0.10.0"
artifact_id: revision-plan-I01-001-r004-v003
workflow_id: sepsis-complex-system-idea-generation-v001
idea_id: I01-001
round_id: round-004
version_id: v003
path: 03_ideas/nodes/I01-001/revisions/round-004/revision-plan-v003.md
based_on:
  - artifact_id: idea-dossier-I01-001-v004
    version: v004
    path: 03_ideas/nodes/I01-001/dossiers/idea-dossier-v004.md
  - artifact_id: methodology-statistics-preflight-I01-001-r004
    version: r004
    path: 03_ideas/nodes/I01-001/reviews/preflight-r004.md
change_type: scientific_revision_plan
---

# 第四轮有界科学修订计划

## 修订目标

把任务三的外部评分对象统一为“从部分已观测历史预测被有意遮蔽但实际测得的临床变量”，并明确该任务不直接验证未观测潜在生理状态的恢复。

## 修订范围

1. 同步 dossier 的逻辑引用、身份锚点、摘要、主要研究问题、目标、核心假设和任务三名称。
2. 保持任务三现有 12 小时连续遮蔽、九个结果域、负对数评分、患者内汇总、逆观测概率权重、比较模型、最不利平均损失差和 Holm 程序；只澄清这些方法所对应的实测留出目标。
3. 同步证据链、预期输出、结果解释和 Claim-Support，使任务三成功只支持测量补全用途。
4. 在第 14 节 Working assumptions 中一次性记录公开观察性重症监护数据没有潜在状态金标准，以及用户“补全未观测的其他状态”准则的可测量操作化和解释风险。
5. 保留其余三项任务、数据资格、模型、方法、限制、随机试验与动物研究条件、时间安排和主张强度。

## 完成条件

输出完整 v005 dossier 与 v004→v005 delta；`change_type` 使用科学修订类型；以插件版本 0.10.0 运行结构 linter 并完成逻辑引用、章节顺序、H1/Title、一句话摘要、身份一致性、任务三端点—指标—解释一致性及仅限三项输出的检查。
