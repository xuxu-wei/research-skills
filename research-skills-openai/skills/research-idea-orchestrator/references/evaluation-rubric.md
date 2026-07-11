# Evaluation Rubric

## Contents

<!-- toc:start -->
- [1. Scoring Scale](#1-scoring-scale)
- [2. Core Dimensions](#2-core-dimensions)
  - [Novelty](#novelty)
  - [Feasibility](#feasibility)
  - [Impact](#impact)
  - [Relevance](#relevance)
  - [Clarity](#clarity)
  - [Completion](#completion)
- [3. Score Anchors](#3-score-anchors)
- [4. Hard Gates](#4-hard-gates)
- [5. Decision Rules](#5-decision-rules)
- [6. Fatal or Unfixable Flaws](#6-fatal-or-unfixable-flaws)
- [7. Required Evaluation Output](#7-required-evaluation-output)
<!-- toc:end -->

本文件定义 `idea-evaluator` 和 isolated independent evaluation 子 agent 必须使用的评分规则。Orchestrator 只调用本文件，不在 `SKILL.md` 中内嵌评分表。

## 1. Scoring Scale

所有维度使用 1-5 分。

- 1 = 不成立或严重不足
- 2 = 明显薄弱
- 3 = 基本可接受但需要修订
- 4 = 较强，可推进
- 5 = 很强，具备明确竞争力

Overall score 使用六个维度的简单平均：

```text
overall = mean(novelty, feasibility, impact, relevance, clarity, completion)
```

不得使用加权平均。

## 2. Core Dimensions

### Novelty

是否存在可辩护的新意？所声称的 gap 是否可能真实？

### Feasibility

在现有数据、方法、时间、伦理和资源条件下是否可执行？

### Impact

结果是否具有科学、临床、工程、社会或方法学价值？

### Relevance

是否符合用户目标、目标产出、领域问题和实际约束？

### Clarity

研究问题、假设、对象、endpoint/metric 和方法路线是否清楚？

### Completion

当前 idea 是否完整到足以支持下一步？

## 3. Score Anchors

- 1：不成立或严重缺失。
- 2：明显薄弱，需要大幅重构。
- 3：基本成立，但需要修订或补证据。
- 4：较强，可进入下一步优化或 proposal pre-drafting。
- 5：很强，可直接支持后续 proposal 工作。

## 4. Hard Gates

```yaml
idea_hard_gates:
  feasibility_min: 3.0
  relevance_min: 3.0
  clarity_min: 3.0
  completion_min: 3.0
```

任一 hard gate 不通过时，不得直接 promote。

## 5. Decision Rules

```text
A: overall >= 4.2 and all hard gates pass -> promote
B: 3.6 <= overall < 4.2 and all hard gates pass -> revise_then_promote
C: 3.0 <= overall < 3.6 or fixable gate failure -> revise / reframe / merge
D: 2.5 <= overall < 3.0 or severe but potentially salvageable gate failure -> keep_as_backup / major_reframe
F: overall < 2.5 or unfixable gate failure -> reject
```

## 6. Fatal or Unfixable Flaws

以下问题通常阻止 promote：

- research question 不可回答；
- endpoint/metric 无法定义；
- data source 无法支持核心问题；
- method 与 hypothesis 不匹配；
- 用户目标或目标产出明显不匹配；
- novelty claim 经 evidence 检查明显不成立；
- feasibility 依赖无法满足的资源、伦理或监管条件；
- 临床相关 idea 未联网且无用户 evidence 时，仍声称 novelty 或 guideline alignment 已确认。

## 7. Required Evaluation Output

Evaluation 子 agent 必须输出：

- 六维分数；
- 简单平均 overall；
- hard gate pass/fail；
- failed gates；
- fatal or unfixable flaws；
- reviewer objections；
- recommendation；
- targeted repair direction；
- assigned next path if repair is needed。

若任一核心字段缺失，orchestrator 必须判定 evaluation invalid，并按 `SKILL.md` 规则重派一次。
