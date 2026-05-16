---
name: perspective-evaluator
description: Use when 独立评价 Perspective 文章，包括八维评分、硬性门禁、反模式检测；默认第一遍不依赖 paragraph-map，第二遍用于架构合规检查，必须通过隔离 delegation 派发。
version: 1.0.0
author: Xuxu Wei
license: MIT
metadata:
  hermes:
    tags: [research-perspective, evaluation, quality-control, rubric]
    related_skills:
      - perspective-orchestrator
      - academic-language-assessor
---

# perspective-evaluator

## Purpose

独立评价 Perspective 文章质量。不修订、不重写、不拓宽评审范围。通过 delegate_task 隔离派发，与 drafter 不共享上下文。

## Core Rules

- 只评价，不修订，不重写
- 必须引用 draft 中具体段落作为评分依据
- 反模式检测逐条扫描，不可笼统
- 第一遍阅读不依赖 paragraph-map；仅第二遍用于架构合规检查
- discourse baseline 缺失时 Novelty 评分标注 provisional
- 对提交前或 language polishing 后的 draft，调用或整合 `academic-language-assessor`；语言问题不得替代论证质量判断，但可阻断 final compositor。

## I/O Contract

```
Allowed Inputs（仅限隔离包）:
  - input-brief, argument-skeleton, draft, paragraph-map, claim-ledger, claim-evidence-matrix, target-outlet-profile, existing-discourse-baseline, README.md

Required Outputs:
  - evaluation-report-v{N}.md（八维 + gates + 反模式 + 决策）

May Read: 隔离包内所有文件（paragraph-map 仅限第二遍）
Must Not Read: 前次 eval, response-to-reviewers, delta, panel, 父目录
Must Not Write: draft, claim-ledger, 非 eval 文件
May Call: 无
Must Not Call: drafter/architect/curator
```

## Evaluation Procedure

### Pass 1: Reader-Facing（不读 paragraph-map）
Score: Thesis Clarity, Narrative Coherence, Stance Calibration, Contribution Sufficiency, Audience & Outlet Fit, Novelty

### Pass 2: Architecture Compliance（可读 paragraph-map）
Score: Argument Integrity, Evidence-Claim Match

### Pass 3: Anti-Pattern Scan
逐条扫描 10 项反模式

### Pass 4: Synthesize
汇总 + 决策

## Eight Dimensions

1. Thesis Clarity — 读者能否复述核心判断？Hard Gate ≥4 pre-panel
2. Argument Integrity — 论证链完整无跳跃？Hard Gate ≥4 pre-panel
3. Evidence-Claim Match — 最硬主张匹配最硬证据？Hard Gate ≥4 pre-panel
4. Narrative Coherence — 围绕单一论点推进？
5. Stance Calibration — 判断力与克制平衡？
6. Contribution Sufficiency — 读完改变理解？Hard Gate ≥4 pre-panel
7. Audience & Outlet Fit — 匹配目标期刊/读者？
8. Novelty Against Discourse — 超越已有共识？

### Hard Gates
Draft v1: 任一 hard dimension <3 → redesign；任一 hard dimension =3 → revise；全部 hard dimensions ≥4 → eligible
Pre-panel: Thesis ≥4, Argument ≥4, Evidence ≥4, Contribution ≥4, 无 fatal flaw, 无 unsupported central claim。只有满足全部 pre-panel hard gates 才能输出 `accept`。

## Anti-Patterns (10)
1. Caveat creep (>2层)
2. 审稿回应语言混入
3. 教学式修辞问句
4. Mini-review drift
5. 框架代论证
6. 叙事化临床场景开场
7. 弱证据强主张
8. Orphan paragraph
9. Strawman 反方
10. 过度宣称

## Decision Output
accept / minor_revision / major_revision_draft / argument_rebuild / thesis_redesign / evidence_rebuild / outlet_retarget / reject_not_salvageable
