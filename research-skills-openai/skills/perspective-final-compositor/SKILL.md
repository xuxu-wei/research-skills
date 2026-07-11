---
name: perspective-final-compositor
description: "Independently assemble and verify final Perspective artifacts for journal fit, citations, claim consistency, and human review without substantive source edits."
---
# perspective-final-compositor

## Purpose

Perspective 终稿前的最后一层合规审计。不替代 evaluator 或 panel，不做实质修改。只做 polish + audit。发现实质问题须 return route，不能通过编辑绕过去。

## Independent Execution Contract

- Run this skill only in a fresh, independent subagent or delegated thread. Never run it in the context that generated, drafted, or revised the artifact under verification.
- Accept only frozen input artifacts identified by artifact ID, exact file path, and version. Treat every source artifact as read-only.
- Write only final verification/composition artifacts permitted below. Do not draft, rewrite, polish, fix, or substantively modify the reviewed source manuscript; the permitted final copy may contain only the explicitly allowed non-substantive edits.
- Do not use hidden reasoning from the parent task, an expected answer or readiness decision, or output from individual evaluators or reviewers beyond the frozen panel summary allowed by the I/O contract.
- Report the exact files read and the verification scope in the output.
- If a fresh independent subagent/delegated thread cannot be created, return `independent_review_pending` with a self-contained continuation brief and stop. Never fall back to inline verification or self-review.

Every completed verification report must include:

```yaml
review_id:
reviewer_skill: perspective-final-compositor
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

- 不可新增核心主张、删除核心主张、改变 claim strength、添加未登记证据
- 不可解决 substantive scientific disagreement
- 不可将 manuscript 从 "not ready" 通过编辑转为 "ready"
- 发现 unsupported central claim / unregistered new claim / citation 不支持主张 → 停止 finalization，return route
- 仅声明 readiness 当无实质未解决问题
- Generic Profile 场景：仅声明 "ready for outlet targeting"

## I/O Contract

```
Allowed Inputs（隔离包白名单）:
  draft-final, claim-ledger, claim-evidence-matrix, citation-risk-log,
  contrary-evidence-log, evidence-limitations, target-outlet-profile,
  panel-summary, reference-list, README.md

Required Outputs:
  - 08_final/final-perspective.md
  - final-edit-log.md
  - final-compositor-report.md
  - submission-readiness-report.md

May Read: 隔离包内所有文件
May Write: 08_final/ 目录
Must Not Read: individual evaluator reports, individual panel reviews, delta reports, claim-change-requests
Must Not Write: claim-ledger, argument-skeleton
May Call: 无。若需要 `medical-journal-review`，由 orchestrator 另行显式派发 fresh independent reviewer，并在进入 compositor 前处理其 return route。
Must Not Call: drafter / architect / curator
```

## Permitted Edits (7项)

1. formatting normalization
2. title/abstract polishing without changing thesis
3. grammar and style edits
4. citation formatting（非内容）
5. section heading refinement
6. removal of duplicated phrasing
7. consistency edits that do not alter claim strength

## Prohibited Edits (6项)

1. adding new claims
2. adding new evidence
3. changing causal language or claim strength
4. upgrading or downgrading claim strength
5. deleting caveats that support evidentiary accuracy
6. resolving reviewer disagreement by rewriting substance

## Five Audits

### 1. Journal Fit Audit
- 篇幅是否在范围内？结构是否符合栏目要求？语气是否适合目标读者？

### 2. Citation Audit
- 每条引用是否准确支持其对应主张？是否有遗漏关键文献？引用格式是否一致？

### 3. Title & Abstract Audit
- 标题是否体现判断力（非描述性）？摘要是否完整传达论证弧线？

### 4. Anti-Pattern Scan
- 最终扫描所有已知反模式（与 evaluator 清单一致）

### 5. Claim-Ledger Consistency Audit
- 终稿主张是否与 ledger 一致？是否有未登记新主张？

## Output Files

### final-edit-log.md
记录 compositor 做的每一项修改：文件位置、修改类型、修改内容、原因。

### final-compositor-report.md
五项审计结果 + 通过/不通过 + 风险标注。

### submission-readiness-report.md
```
Ready for human review and sign-off: yes / no / conditional / outlet-targeting-only
Remaining risks: [列表]
Required author verification: [列表]
Suggested target outlets: [如使用 Generic Profile]
```

## Return Routes

发现实质问题时输出诊断 + 路由建议：
- unsupported central claim → return_to_curator
- unregistered new claim → return_to_drafter
- citation 不支持主张 → return_to_curator
- outlet 不匹配 → outlet_retarget
- 多项实质问题 → return_to_refinement

## Pitfalls

- 越权做实质修改
- 编辑掩盖实质问题
- 把 Generic Profile 场景误标为 ready for human sign-off；只能声明 ready for outlet targeting
- 忽略 citation risk log 中的已知风险

## References

- Read `references/journal-fit-checklist.md` when its named guidance or contract applies.
- Read `references/citation-audit-checklist.md` when its named guidance or contract applies.
- Read `references/final-anti-pattern-scan.md` when its named guidance or contract applies.
- Read `references/permitted-edits.md` when its named guidance or contract applies.
