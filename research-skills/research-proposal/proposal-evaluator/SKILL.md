---
name: proposal-evaluator
description: Evaluate a proposal file as an isolated independent evaluator. Assesses
  Novelty, Feasibility, Impact, Relevance, Clarity, Completion, Thesis Integrity,
  fatal flaws, reviewer defensibility, and revision priorities. Does not draft,
  rewrite, or evaluate SAP.
version: 1.3.0
author: Xuxu Wei
license: MIT
metadata:
  hermes:
    tags:
    - research-proposal
    - proposal
    - evaluation
    - evaluator
    - review
    - quality-gate
    - revision
    related_skills:
    - proposal-orchestrator
    - proposal-context-brief-builder
    - proposal-readiness-triage
    - proposal-drafter
    - proposal-refinement-controller
    - proposal-review-panel
    - proposal-package-assembler
    - academic-language-assessor
---

# proposal-evaluator

## When to Use

当 proposal 文件已经由 `proposal-drafter` 生成或修订，并需要独立判断其质量、缺陷、可辩护性和下一步处理意见时，使用本 skill。

本 skill 只评价 proposal 文件，不评价 SAP。SAP 应由 `sap-evaluator` 单独评价。

## Core Principles

- 必须作为隔离、独立的 evaluator 子 agent 执行。
- 只评价 frozen proposal 文件，不参与 drafting 或 revision。
- 不依赖 drafter 的隐含推理过程，只依据可见文件、context brief、用户约束和证据摘要评价。
- 评价必须覆盖 Novelty、Feasibility、Impact、Relevance、Clarity、Completion。
- 对接近提交、package 或 language polishing 后的 proposal，调用 `academic-language-assessor` 或整合其 `language-assessment-vNNN.md`，不要凭直觉评价语言质量。
- 必须检查 fatal flaws 和 hard gates。
- 必须给出明确 decision：accept、revise、reject 或 stop_no_gain。
- 不在本 SKILL.md 中内嵌 schema、template、rubric、reference 正文或代码；只引用对应文件路径。

## Inputs

通常由 `proposal-orchestrator` 提供：

- `proposal_file_path`
- `proposal_version`
- proposal context brief
- readiness report
- 用户目标和目标产出
- 用户约束
- evidence summary，如有
- funding call 或格式要求，如有
- previous evaluation report，如为 re-evaluation
- revision delta report，如为 re-evaluation

若缺少 `proposal_file_path`，应停止评价并返回输入缺口。

## Outputs

本 skill 输出 proposal evaluation report，至少包含：

- overall decision
- scores by dimension
- hard gate status
- fatal flaws, if any
- major strengths
- major weaknesses
- reviewer defensibility concerns
- revision priorities
- accept / revise / reject / stop_no_gain rationale

不得输出 revised proposal。

### Revision Priority Classification

每条 revision priority 必须附带以下分类前缀：
- `[evidence]`：某主张缺乏证据/引用/数据支撑
- `[clarity]`：表述不清、需要改写但内容本身正确
- `[substance]`：实质性缺陷（方法缺陷、范围不匹配、可行性问题、逻辑矛盾）
- `[other]`：无法归入以上三类

分类只需要判断问题的类型，不要求 evaluator 验证证据是否存在。
无法确定时默认 `[other]`。

## Procedure

### 1. Confirm Evaluation Scope

确认评价对象是 proposal 文件，而不是 idea、SAP、protocol 或 reviewer panel summary。

若任务要求评价 SAP，应返回 scope mismatch，并建议交由 `sap-evaluator`。

### 2. Read Proposal File and Context

基于以下材料评价：

- proposal 文件；
- context brief；
- readiness report；
- 用户目标和约束；
- evidence summary，如有；
- prior evaluation 或 revision delta，如为再评价。

不得根据未提供的信息替 proposal 补强。

### 3. Evaluate Core Dimensions

按照六个维度评价 proposal：

- Novelty：创新点是否可辩护，是否只是重复已有工作。
- Feasibility：数据、方法、资源、时间和执行路径是否支持完成。
- Impact：科学、临床、工程、社会或方法学价值是否足够。
- Relevance：是否符合用户目标、研究领域、目标产出和约束。
- Clarity：研究问题、目标、对象、方法和预期成果是否清楚一致。
- Completion：作为 proposal 文件是否完整，是否足以支持下一步评审或修订。

**Thesis Integrity（仅 re-evaluation 时评估）**：当本次为修订后再评价时，必须额外评估 thesis integrity。比较当前版本与上一版本的核心主张清晰度——"这一版的核心主张比上一版更清晰了还是更模糊了？" 评分标准：
- 5：核心主张比上一版更清晰且更集中，限定词更少
- 3：清晰度与上一版基本持平
- 1：核心主张被更多 caveat/hedging 层覆盖，比上一版更模糊

**Thesis integrity 硬规则**：若 thesis integrity ≤ 2（明显更模糊），即使其他维度总分改善，decision 必须为 `revise`，修订方向为**删减**（移除多余的限定层或审稿回应沉积），不得继续追加新内容。

### 4. Check Hard Gates and Fatal Flaws

必须检查 proposal 是否存在不可继续推进的问题，包括但不限于：

- research question 不可回答；
- 研究对象或核心变量不清；
- 方法无法支撑研究目标；
- 数据路径与研究问题不匹配；
- 关键可行性条件缺失；
- novelty claim 不成立；
- 用户目标明显不匹配；
- ethical、regulatory 或 implementation blocker；
- proposal 结构缺失导致无法评审；
- Genre Fit：proposal 中是否存在以下任一体裁违规——（a）叙事化临床场景（"一位医生在查房时……"式故事），（b）教学式修辞问句（"为什么是X？因为……"），（c）审稿回应标记残留（"vX新增""回应Review Panel"等版本标注），（d）以降低理解门槛为由添加的解释性段落（术语词典、概念翻译表作为独立正文段而非附录引用）。任一条目出现即判定 genre unfit，需记录具体位置。

若存在 fatal flaw，应明确指出其位置、性质和是否可修复。

### 5. Assess Reviewer Defensibility

从潜在评审人视角判断 proposal 是否容易被质疑。

重点检查：

- 立项依据是否支撑研究意义；
- 国内外现状和发展趋势是否足以支持 gap；
- 研究内容、目标和关键科学问题是否聚焦；
- 研究方案是否与目标一致；
- 可行性分析是否具体；
- 特色与创新是否可信；
- 时间计划和预期成果是否合理。

### 6. Decide Next Action

根据评价结果给出 decision：

- `accept`：proposal 可进入 proposal review panel 或下一步人工审阅。
- `revise`：存在明确且可修复的问题，应进入 targeted revision。
- `reject`：存在不可修复 fatal flaw，或核心目标、方法、数据、价值不成立。
- `stop_no_gain`：仅用于 re-evaluation；修订后无实质改进，关键问题仍未解决。

decision 必须有简短理由，并列出最高优先级修订项。

### 7. Re-evaluation Rules

若本次是 revision 后再评价，必须比较前后版本。

重点判断：

- evaluator 上轮指出的问题是否被解决；
- 是否引入新问题；
- 是否只是语言润色而无实质改进；
- 是否应继续修订或触发 stop_no_gain。

不得因表述更流畅而自动提高评价。

## Delegation Rules

本 skill 本身应由 `proposal-orchestrator` 或 `proposal-refinement-controller`
以 `delegate_task` 隔离子 agent 形式调用。

子 agent 必须接收完整任务上下文（proposal file path、context brief、
evidence artifacts/limitations、user goal、constraints、version）——
不得依赖父会话隐含上下文。

执行期间不得再调用 drafter、refiner、sap-writer 或 reviewer panel 共同判断。

若发现需要修订，应返回 evaluation report，由 orchestrator 调度后续 skill。

## Stop Conditions

以下情况应停止评价并返回问题说明：

- 缺少 `proposal_file_path`；
- proposal 文件无法读取；
- 输入对象不是 proposal；
- 任务要求评价 SAP；
- context brief 缺失到无法判断 relevance 和 feasibility；
- 用户要求 evaluator 直接重写 proposal。

若可以完成有限评价，应说明评价范围和不确定性。

## Pitfalls

- 不要修改 proposal 文件。
- 不要替代 proposal-drafter。
- 不要评价 SAP。
- 不要把 proposal 写得好看等同于可执行。
- 不要忽略 fatal flaw。
- 不要仅给分数而不给理由。
- 不要放宽 hard gates 以推动流程继续。
- 不要把未解决问题归类为已解决。
- 不要用一般性赞美替代具体评审意见。
- 不要基于未提供证据确认 novelty 或 feasibility。

## Verification

完成前检查：

- 是否只评价 proposal 文件；
- 是否未评价 SAP；
- 是否覆盖六个核心维度；
- 是否检查 hard gates；
- 是否检查 fatal flaws；
- 是否给出 decision；
- 是否列出 revision priorities；
- 若为 re-evaluation，是否比较前后版本；
- 是否未修改 proposal 文件；
- 是否未替代 drafter 或 review panel。

## References

- `references/rubric-proposal-evaluation.md`：定义 Novelty、Feasibility、Impact、Relevance、Clarity、Completion 六维评价标准和评分解释。
- `references/gates-proposal-hard-gates.md`：定义 proposal 必须通过的最低门槛和 gate failure 处理规则。
- `references/criteria-fatal-flaws.md`：定义 proposal 中不可忽略的 fatal flaws 及其可修复性判断。
- `references/policy-reviewer-defensibility.md`：定义从评审人视角检查 proposal 可辩护性的规则。
- `references/policy-re-evaluation.md`：定义 revision 后再评价、版本比较和 stop_no_gain 判断规则。
- `references/schema-proposal-evaluation-report.md`：定义 proposal evaluation report 的结构要求，仅供输出校验使用。
- `templates/template-proposal-evaluation-report.md`：定义 proposal evaluation report 的输出格式。
