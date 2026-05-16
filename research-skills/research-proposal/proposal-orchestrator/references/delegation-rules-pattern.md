# Unified Delegation Rules Pattern

跨 research-idea 和 research-proposal 两个 orchestrator，所有 evaluator 技能的 Delegation Rules 遵循统一的四人要素模板。

## 四人要素

```
## Delegation Rules

本 skill 本身应由 <orchestrator>                      ← [1] 谁调用我
以 `delegate_task` 隔离子 agent 形式调用。              ← [2] 怎么被调用

子 agent 必须接收完整任务上下文（<字段清单>）——          ← [3] 上下文完整性
不得依赖父会话隐含上下文。

执行期间不得再调用 <其他 evaluator 名单>。              ← [4] 禁止事项

若发现需要修订，应返回 <report>，                      ← [5] 异常路由
由 orchestrator 决定 <后续动作>。
```

## 五个要素（[1]—[5]）

1. **调用者身份** — 列出哪个 orchestrator 应调用此 skill。多个调用者用 `或` 连接（如 `research-idea-orchestrator` 或 `proposal-orchestrator`）。

2. **调用方式** — 必须包含字面量 `delegate_task` 和 `隔离子 agent`。不得使用模糊词如"Delegate to"、"Call"、"交给"。

3. **上下文完整性** — 必须列出子 agent 需要接收的输入字段清单，并声明"不得依赖父会话隐含上下文"。

4. **禁止事项** — 列出执行期间不得调用的其他 skill 名单。应包含所有可能产生协作效应的 evaluator/generator。

5. **异常路由** — 定义当 evaluator 认为需要修订时如何返回结果，以及 orchestrator 如何处理。

## 已应用该模式的所有技能

| 技能 | 调用者 | 输入字段 | 禁止调用 |
|------|--------|---------|---------|
| idea-evaluator | research-idea-orchestrator | candidate ideas, context brief, evidence/opportunity map, preflight report, constraints, lineage | idea generator, methodology-statistics-preflight, portfolio assembler |
| methodology-statistics-preflight | research-idea-orchestrator / proposal-orchestrator | idea, context brief, evidence/opportunity map, endpoint/metric, data route, method | idea-evaluator, proposal-drafter, sap-writer |
| proposal-readiness-triage | proposal-orchestrator | original idea, context brief, evidence artifacts, user goal, constraints, target output | drafter, sap-writer, review panel |
| proposal-evaluator | proposal-orchestrator / proposal-refinement-controller | proposal file path, context brief, evidence artifacts, user goal, constraints, version | drafter, refiner, sap-writer, reviewer panel |
| sap-evaluator | proposal-orchestrator / sap-refinement-controller | SAP file path, context brief, preflight report, endpoint/metric definitions, data description | sap-writer, proposal-drafter, proposal-evaluator, reviewer panel |

## Orchestrator 侧的配套要求

对应每个 evaluator 技能，orchestrator 必须：

1. 在 workflow 步骤中显式写出 `使用 delegate_task 派发隔离的 <skill> 子 agent`
2. 写出 `不得在自己的会话中加载 <skill> 的 SKILL.md 内联执行`
3. 提供包含 rubric/schema/template 路径的 brief 模板（参考 `delegate-brief-templates.md`）
4. 对于多 reviewer 并行场景（如 review panel），使用 `delegate_task(tasks=[...])` 批量派发

## Runtime Adapter

`delegate_task` is the preferred Hermes implementation, but isolation is the requirement. If the current runtime does not provide `delegate_task`, use the runtime's available isolated subagent mechanism or create a fresh independent session with an explicit brief and frozen file paths.

If no isolated execution path is available, do not silently evaluate inline. Mark the affected gate as `isolation_unavailable`, preserve the draft/package as partial, and require a later independent evaluation before final-ready status.

For `skill_view(...)` references, load the same referenced file directly from the named skill's `references/` directory or include its contents in the delegate brief when the runtime lacks `skill_view`.

## 审计方法

对每个 evaluator 技能检查：
- [ ] SKILL.md 是否有 `## Delegation Rules` 章节
- [ ] 章节是否包含 `delegate_task` 字面量
- [ ] 章节是否包含 `不得依赖父会话隐含上下文`
- [ ] 章节是否包含 `执行期间不得再调用` 及其它 evaluator 名单
- [ ] Orchestrator 是否在对应步骤中显式写了 `delegate_task` 和内联禁止
- [ ] Orchestrator 是否有对应的 brief 模板（含 rubric/schema/template 路径）
