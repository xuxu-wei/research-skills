---
name: perspective-evaluator
description: "Independently evaluate a frozen Perspective for argument, evidence, contribution, narrative, claim discipline, and outlet fit."
---
# perspective-evaluator

## Purpose

独立评价 Perspective 文章质量。不修订、不重写、不拓宽评审范围。必须显式派发到 fresh independent subagent/delegated thread，与 drafter 不共享上下文。

## Independent Execution Contract

- Run this skill only in a fresh, independent subagent or delegated thread. Never run it in the context that generated, drafted, or revised the artifact under review.
- Accept only frozen input artifacts identified by artifact ID, exact file path, and version. Treat every source artifact as read-only.
- Write only review or verification artifacts. Do not draft, rewrite, polish, fix, or otherwise modify the reviewed manuscript or any source file.
- Do not use hidden reasoning from the parent task, an expected answer or decision, or output from any other reviewer. A fresh re-evaluation must not receive prior scores or the prior decision.
- Report the exact files read and the evaluation scope in the output.
- If a fresh independent subagent/delegated thread cannot be created, return `independent_review_pending` with a self-contained continuation brief and stop. Never fall back to inline self-review.

Every completed report must include:

```yaml
review_id:
reviewer_skill: perspective-evaluator
reviewer_instance_id:
workflow_id:
round_id:
input_artifact_ids:
input_versions:
files_read:
review_scope:
isolation_mode: fresh_subagent
prior_scores_visible: false
source_edits_performed: false
decision:
findings:
unresolved_issues:
```

## Core Rules

- 只评价，不修订，不重写
- 必须引用 draft 中具体段落作为评分依据
- 反模式检测逐条扫描，不可笼统
- 第一遍阅读不依赖 paragraph-map；仅第二遍用于架构合规检查
- discourse baseline 缺失时 Novelty 评分标注 provisional
- 对提交前或 language polishing 后的 draft，由 orchestrator 另行显式派发 fresh independent `academic-language-assessor`。本 evaluator 不调用或读取该 assessor 的输出；orchestrator 分别依据两份独立报告路由，语言问题不得替代论证质量判断，但可阻断 final compositor。

## I/O Contract

```
Allowed Inputs（仅限隔离包）:
  - input-brief, argument-skeleton, draft, paragraph-map, claim-ledger, claim-evidence-matrix, target-outlet-profile, existing-discourse-baseline

Required Outputs:
  - evaluation-report-v{N}.md（八维 + gates + 反模式 + 决策）

May Read: 隔离包内所有文件（paragraph-map 仅限第二遍）
Must Not Read: 前次 eval/score/decision, response-to-reviewers, panel, 父目录, 项目 README, previous draft, revision delta；复评仅可按需读取匿名 must-fix 清单
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

## Conditional Resource

- Read `references/anti-pattern-checklist.md` during Pass 3 when performing the required anti-pattern scan.
