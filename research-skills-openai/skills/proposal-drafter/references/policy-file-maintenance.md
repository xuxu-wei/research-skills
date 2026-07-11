# policy-file-maintenance

## Purpose

定义 proposal 文件路径、版本、lineage、change summary 和 unresolved issues 的维护规则。

## Required State

每次创建或修改 proposal 文件时，必须记录：

- `proposal_file_path`
- `proposal_version`
- source context 或上游输入
- change summary
- unresolved issues
- next recommended step

## Versioning

建议版本命名：

- v0.1 initial draft
- v0.2 targeted revision
- v0.3 evaluator-driven revision
- v1.0 evaluator-accepted draft

实际命名可由 orchestrator 或运行环境决定，但必须可追踪。

## Lineage Rules

- 修订应基于既有 proposal 文件。
- 若生成新文件，应记录 previous file path。
- 不得生成无法追踪来源的独立 proposal。
- 不得删除 evaluator 或 reviewer 指出的 unresolved issues，除非修订已实际解决。

## Handoff Note

交给下游 evaluator 或 orchestrator 时，应包含：

- 当前 proposal 文件路径；
- 当前版本；
- 主要修改；
- 未解决问题；
- 需要 evaluator 特别关注的问题。
