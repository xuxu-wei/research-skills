---
name: proposal-refinement-controller
description: "Control targeted proposal revision loops after independent proposal evaluation."
---
# proposal-refinement-controller

## When to Use

当 `proposal-evaluator` 对 proposal 文件给出 `revise`，且问题被判断为可修复时，使用本 skill。

本 skill 负责把 evaluation report 转化为 targeted revision plan，调度 `proposal-drafter` 修改 proposal 文件，并要求独立 re-evaluation。它不直接重写 proposal，也不替代 evaluator 做质量判断。

## Core Principles

- revision loop 必须围绕明确的 `proposal_file_path` 工作。
- 每轮 revision 必须针对 evaluator 的具体问题，不做无目标全文重写。
- `proposal-drafter` 负责修改 proposal 文件；本 skill 负责控制修订计划、版本 lineage 和 re-evaluation。
- 每轮修订后必须由新的隔离、独立 evaluator 子 agent 进行 re-evaluation。
- 当 revision mode 为 language_polishing 时，先调用 `academic-language-assessor`，保存 `05_evaluations/language-assessment-vNNN.md`；drafter 修改后保存 `06_revisions/round-NNN/language-change-log-rNNN.md` 并请求语言 re-assessment。
- 不允许 drafter、refiner 或上一轮 evaluator 自证修订成功。
- 修订收益不足或关键问题未解决时，应触发 `stop_no_gain`。

## Inputs

通常由 `proposal-orchestrator` 提供：

- `proposal_file_path`
- `proposal_version`
- proposal context brief
- readiness report
- proposal evaluation report
- evaluator decision
- revision priorities
- fatal flaws, if any
- user goal and constraints
- previous revision history, if any
- maximum revision rounds, default 2

若缺少 proposal 文件路径或 evaluation report，应停止并返回输入缺口。

## Outputs

本 skill 输出：

- revision plan
- updated `proposal_file_path`
- updated `proposal_version`
- revision delta report
- independent re-evaluation report
- next decision: `accept`, `revise`, `reject`, or `stop_no_gain`
- unresolved issues

不得输出未经独立评价的 accept 结论。

## Procedure

### 1. Confirm Revision Eligibility

先检查 evaluator decision 是否为 `revise`。

若 decision 为：

- `accept`：默认不启动 revision，交回 orchestrator 进入下一步。**例外——用户要求 polish pass**：当 evaluator 判定为 ACCEPT 但用户明确要求执行修订轮次（如"执行一轮定向修订"），应继续执行。此时 revision priorities 视为 polish-level（非 must-fix），修订范围严格限制为 evaluator 指定的 optimization items，不做结构性重写。
- `reject`：不启动 revision，除非 orchestrator 明确要求尝试 major redesign。
- `stop_no_gain`：停止 revision loop。
- `revise`：继续制定 revision plan。

若 evaluation report 指出不可修复 fatal flaw，应停止并返回 reject rationale。

### 2. Build Targeted Revision Plan

根据 evaluation report 提取最高优先级问题。

revision plan 应区分：

- must-fix issues；
- should-fix issues；
- optional improvements；
- issues not fixable without new user input；
- issues requiring methodology or evidence clarification。

对每条 must-fix issue，必须规划修改策略，而不是默认追加新段落：
- **追加**：仅在内容确实缺失且无法被现有段落覆盖时使用
- **替换**：用更精准或更有力的表述替换现有弱内容，不增加篇幅
- **浓缩**：合并多个相关段落为一个更紧凑的版本
- **删减**：当 reviewer 指出某内容是多余的或不可验证时，直接删除或缩减
- **澄清**：在现有段落内增加一两句限定或过渡，而非新增整段

**每条修改必须标注入文策略**：
- `入正文`：修改直接融入 proposal 正文
- `仅入回应`：仅写入 response-to-reviewers 文件，不修改 proposal 正文（适用于：审稿人误解的澄清、不采纳意见的解释、对非核心主张的讨论）
- `不处理`：不在此轮修订中处理（适用于：需要用户决策、超出本轮 scope、与核心主张冲突的意见）

规划时思考：
- 这个问题有多重要？是否需要用一段去回应，还是一句话就够了？
- 修改后 proposal 是否更接近申请书体裁（说服性、简洁）还是更接近教材（解释性、冗长）？
- 修改与现有内容的关系：是否重复？是否可以被已有段落吸收？
- 是否有更小的改动能达到同样效果？

### 3. Coordinate Proposal Update

将 revision plan 交给 `proposal-drafter`。

任务 brief 必须包含：

- current `proposal_file_path`
- current `proposal_version`
- evaluation report
- revision plan（含每条修改的入文策略标注：入正文 / 仅入回应 / 不处理）
- user constraints
- **required output: (a) updated proposal file, (b) response-to-reviewers file, (c) change summary**

`proposal-drafter` 必须维护同一个 proposal 文件，或生成明确版本化的新文件路径。审稿回应文件按 `06_revisions/round-NNN/response-to-reviewers-rNNN.md` 命名。

#### 3a. Direct Execution Mode（无需子 agent 时）

当用户直接要求执行修订（未使用 drafter 子 agent），本 agent 应直接执行修订。工作流：

1. 先写出 revision plan 文件（`revision-plan-v{N}-v{N+1}.md`），锁定所有修改意图和入文策略。
2. 按从上到下的文档顺序执行修订（避免跳转造成的 patch 上下文冲突）：
   - §1 区域修改 → §3 区域修改 → §5 区域修改 → Unresolved Issues
3. 使用 `patch` 工具（skill_manage action=patch）逐条修改，精确匹配 old_string：
   - old_string 必须足够长以保证唯一（含周围 1-2 行上下文）
   - 每次 patch 后检查 diff 输出确认修改正确
4. 结构性修改（删除+重新定位）分两步：先删除源位置，再在目标位置追加。
5. 全部 patch 完成后，更新版本 header（Proposal Version: v{N} → v{N+1}）。
6. 将修改后的文件复制为版本化输出（如 `I201-proposal-v9.md`）。
7. 生成 changelog（`06_revisions/round-NNN/revision-delta-rNNN.md`）和 response-to-reviewers（`06_revisions/round-NNN/response-to-reviewers-rNNN.md`）。

Pitfalls for direct execution:
- 不要用全文重写替代 patch——patch 保留文件的其他部分不受扰动。
- 不要在 old_string 中使用会因前序 patch 而改变的内容。
- 删除某段落后，检查是否存在指向该段落的交叉引用（孤儿引用）。
- 版本化输出文件通过 `cp` 从修改后的工作文件生成，不要另行写入。

### 4. Require Revision Delta Report

收到 updated proposal 后，生成或要求生成 revision delta report。

delta report 应说明：

- 哪些 evaluator concerns 已处理；
- 哪些问题未处理；
- 是否引入新问题；
- 是否改变研究问题、目标、方法或核心 claim；
- 是否存在需要用户确认的新假设。

不得只记录“已润色”或“已优化表达”。

### 5. Delegate Independent Re-evaluation

修订后必须将 `proposal-evaluator` 显式派发给新的隔离、独立 evaluator 子 agent 或 delegated thread；不得内联复评，也不得复用上一轮 evaluator 实例。

re-evaluation brief 至少包含：

- updated `proposal_file_path`
- previous `proposal_file_path` 或 previous version
- anonymized prior must-fix issue list（不得包含上一轮分数、总评理由或 decision）
- revision delta report
- context brief
- user goal and constraints
- 明确要求：比较前后版本，只评价，不重写

不得由本 skill 自行判断修订是否通过。

### 6. Compare Revision Outcome

根据 re-evaluation report 和 delta report 判断下一步：

- `accept`：proposal 已通过 gate，可交回 orchestrator 进入 proposal review panel。
- `revise`：仍有可修复问题，且未超过最大 revision rounds。
- `reject`：出现不可修复 fatal flaw。
- `stop_no_gain`：关键问题未解决，或修订收益不足，不应继续循环。

**Caveat budget 停止条件**：除上述判断外，每轮修订后必须检查核心主张的限定层数。当核心主张的 caveat/hedging 层数超过 2 层（即原始主张已被"如果A则X，如果B则Y，如果C则Z"或等价的多层条件句修饰），触发 `stop_no_gain`——修订不再改善 thesis clarity，应交由 orchestrator 做结构性决策（砍主张或砍审稿意见）。

默认最多 2 轮 revision。超过限制后，若仍未 accept，应返回 unresolved issues 和 stop rationale。

### 7. Handoff

将结果交回 `proposal-orchestrator`。

handoff 内容至少包括：

- current `proposal_file_path`
- current `proposal_version`
- latest evaluation report
- revision delta report
- revision round count
- next decision
- unresolved issues
- recommended next step

## Delegation Rules

本 skill 应由 `proposal-orchestrator` 调用，负责管理 revision 文件、delta report 和修订版本 lineage。

以下任务必须显式派发给 fresh 隔离子 agent 或 delegated thread：

- proposal re-evaluation（派发新的 `proposal-evaluator` 实例）——子 agent 不得访问前轮 evaluator 的评分、总评理由或 decision；
- any gate decision after revision；
- any skeptical or reviewer-style judgment。

本 skill 不得：
- 自行评价 proposal 是否通过；
- 让 proposal-drafter 自评；
- 复用上一轮 evaluator 作为唯一 re-evaluator；
- 合并 drafting 和 evaluation 角色。

## Stop Conditions

以下情况应停止 revision loop：

- 缺少 `proposal_file_path`；
- 缺少 evaluation report；
- evaluator decision 不是 `revise`；
- 存在不可修复 fatal flaw；
- 修订需要用户提供关键新信息；
- 已达到最大 revision rounds；
- re-evaluation 显示关键问题未解决；
- 修订只改善表述但未解决核心缺陷；
- 修订引入新的严重问题；
- 触发 `stop_no_gain`；
- **核心主张的 caveat/hedging 层数超过 2 层**——修订已无法改善 thesis clarity，应触发结构性决策。

## Pitfalls

- 不要无目标全文重写。
- 不要用语言润色冒充实质修订。
- 不要脱离 `proposal_file_path` 生成新 proposal。
- 不要忽略 evaluator 的 must-fix issues。
- 不要删除 unresolved issues，除非已实际解决。
- 不要让 drafter、refiner 或上一轮 evaluator 自证成功。
- 不要无限循环修订。
- 不要在缺少关键新信息时继续假设。
- 不要将 `revise` 自动解释为 accept。
- 删除某段落后，检查并修复指向被删内容的交叉引用（孤儿引用）——如"上述临床场景"在场景被删除后没有指向目标。

## Verification

完成前检查：

- 是否存在明确 `proposal_file_path`；
- 是否存在 proposal evaluation report；
- revision plan 是否针对 evaluator 的具体问题；
- proposal-drafter 是否维护同一文件或清晰版本 lineage；
- 是否生成 revision delta report；
- re-evaluation 是否由隔离、独立 evaluator 完成；
- 是否比较了修订前后版本；
- 是否记录 unresolved issues；
- 是否给出 next decision；
- 是否未自行宣布未经评价的 accept。

## References

- `templates/template-revision-delta-report.md`: defines revision delta report output format.
- `references/case-notes/diagnostic-revision-death-spiral.md`: case-derived diagnostic note; use as supporting guidance, not as a standalone hard gate.
- `references/case-notes/pitfalls-revision-loop.md`: case-derived revision-loop note for skipped re-evaluation and panel-version mismatch.

- `references/policy-revision-loop.md`：定义 revision round、最大轮数、revision priority 和 loop control 规则。
- `references/policy-re-evaluation.md`：定义独立 re-evaluation、前后版本比较和 evaluator 隔离要求。
- `references/policy-no-gain-stop.md`：定义 stop_no_gain 的触发条件和停止说明。
- `references/policy-file-lineage.md`：定义 proposal 文件路径、版本号、变更摘要和 lineage 维护规则。
- `references/schema-revision-delta-report.md`：定义 revision delta report 的结构要求，仅供输出校验使用。
- `templates/template-revision-plan.md`：定义 targeted revision plan 的输出格式。
- `references/diagnostic-revision-death-spiral.md`：多轮修订导致 proposal 崩坏的诊断模式——症状、机制、预防和响应。
