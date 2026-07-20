# policy-file-maintenance

## Purpose

定义 content plan、proposal 文件路径、逻辑版本、lineage、change summary 和 unresolved issues 的维护规则。

## Required State

每次创建或修改 proposal 文件时，必须记录：

- `artifact_id`
- `proposal_file_path`
- `proposal_version`
- source context 或上游输入
- change summary
- unresolved issues
- next recommended step

## Versioning

使用 orchestrator 的单调 `vNNN` 文件版本。规划文件使用 `proposal-content-plan-vNNN.yaml`；计划版本与目标 proposal 版本都必须在 artifact index 中以逻辑引用记录。不得要求 writer 计算或返回 SHA/digest。

## Lineage Rules

- 初稿必须基于冻结的 content plan，并由不同于 planner 的 writer instance 创建。
- 修订应基于既有 proposal 文件。
- 若生成新文件，应记录 previous file path。
- 不得生成无法追踪来源的独立 proposal。
- 不得删除 evaluator 或 reviewer 指出的 unresolved issues，除非修订已实际解决。
- Editorial repair 必须记录 normalized brief、protected register、action execution report 与新 proposal 之间的 lineage；原始 assessor reports 不属于 writer 输入。

## Handoff Note

交给下游 evaluator 或 orchestrator 时，应包含：

- 当前 proposal 文件路径；
- 当前版本；
- 主要修改；
- 未解决问题；
- 需要 evaluator 特别关注的问题仅能由 orchestrator 匿名化后决定是否进入允许的最小 factual input；writer 不直接给 final evaluator 写审查提示。
