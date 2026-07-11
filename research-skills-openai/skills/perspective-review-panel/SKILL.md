---
name: perspective-review-panel
description: "Independently review a frozen Perspective from one assigned counter-position, evidence, narrative, methodology, clinician, or outlet-fit role without peer-output access."
---
# perspective-review-panel

## Purpose

Perspective 文章的外部模拟审稿。三角色定制：Counter-position Reviewer（攻击论证链）、Evidence Reviewer（检查证据-主张匹配）、Narrative Reviewer（读者体验与反模式）。每个角色必须显式派发到独立 fresh subagent/delegated thread，互不知晓，不接触 evaluator reports。

## Independent Execution Contract

- Run each reviewer role only in its own fresh, independent subagent or delegated thread. Never run a role in the context that generated, drafted, or revised the artifact under review.
- Accept only frozen input artifacts identified by artifact ID, exact file path, and version. Treat every source artifact as read-only.
- Write only individual review or verification artifacts. Do not draft, rewrite, polish, fix, or otherwise modify the reviewed manuscript or any source file.
- Do not use hidden reasoning from the parent task, an expected answer or decision, evaluator output, or output from any other reviewer.
- Report the exact files read and the assigned review scope in every individual output.
- If fresh independent subagents/delegated threads cannot be created, return `independent_review_pending` with a self-contained continuation brief and stop. Never use inline self-review.

Every individual reviewer report must include:

```yaml
review_id:
reviewer_skill: perspective-review-panel
reviewer_instance_id:
reviewer_role:
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

- 三角色由 orchestrator 显式并行派发，每个角色使用不同的 fresh subagent/delegated thread
- Reviewer 之间互不知晓对方意见
- 所有 reviewer 不接触 evaluator reports
- Narrative Reviewer 不接收 argument-skeleton
- 每个 reviewer 须说明：如 target outlet 更宽/更窄，建议是否会改变
- Orchestrator 必须等待全部 required reviewers 返回后才合成 panel-summary
- 合成必须保留冲突、少数意见和 dissent，不得伪造共识
- 共识问题（≥2 reviewer 指出）自动升级 must-fix；若均为低严重度措辞问题，则标为 editorial must-fix，不得阻断终稿
- 默认三角色保持精简；仅在触发条件存在时增加 conditional reviewer

## Three Reviewer Roles

### Counter-position Reviewer

| 项目 | 内容 |
|------|------|
| 隔离包文件 | draft, argument-skeleton, README.md |
| 核心任务 | 持相反立场，攻击核心判断和论证链每一步 |
| 核心问题 | "如果我完全不同意你的前提，你的论证哪一步最先崩溃？" |
| 输出 | 论证链每环抵抗力评分(1-5) + 最弱一环 + 总体建议 + outlet 变化影响声明 |

```
Must Not Read: claim-ledger, evidence-matrix, evaluator reports, 其他 reviewer 评审
```

### Evidence Reviewer

| 项目 | 内容 |
|------|------|
| 隔离包文件 | draft, claim-evidence-matrix, claim-ledger, contrary-evidence-log, README.md |
| 核心任务 | 检查证据-主张匹配度、选择性引用、遗漏关键反证、过度推断 |
| 核心问题 | "最硬的主张是否匹配最硬的证据？有没有被忽略的反证？" |
| 输出 | 每步证据充分性评分(1-5) + 证据缺口标注 + 总体建议 + outlet 变化影响声明 |

```
Must Not Read: evaluator reports, 其他 reviewer 评审
```

### Narrative & Anti-pattern Reviewer

| 项目 | 内容 |
|------|------|
| 隔离包文件 | draft, target-outlet-profile（最多）, README.md |
| 核心任务 | 检查叙事连贯性、论证推进力、反模式、读者体验 |
| 核心问题 | "读者读完是改变了理解还是只是知道了更多信息？" |
| 输出 | 整体叙事力评分(1-5) + 反模式检出清单 + 总体建议 + outlet 变化影响声明 |

```
Must Not Read: skeleton, evaluator reports, evidence, claim-ledger, 其他 reviewer 评审
```

## Conditional Reviewers

Use conditional reviewers only when the trigger is present. They are additive to the default three-reviewer panel and must remain isolated from evaluator reports and other reviewers.

### Methodology / Statistics Reviewer

Trigger when the Perspective contains method-heavy, causal, predictive, statistical, benchmark, or design-quality claims.

Allowed files: draft, claim-evidence-matrix, claim-ledger, methodology/statistics preflight if available, README.md.

Task: audit whether methodological or statistical claims are properly bounded and whether the article overstates what the methods can establish.

### Practicing-Clinician Reviewer

Trigger when the Perspective involves clinical medicine, public health practice, patient care, guideline interpretation, screening, diagnosis, treatment, or implementation in care settings.

Allowed files: draft, target-outlet-profile, clinical evidence subset if available, README.md.

Task: audit clinical plausibility, endpoint relevance, practice-facing implications, and whether the framing would be credible to a frontline clinician.

### Outlet-Fit Editor Reviewer

Trigger when a concrete target journal, outlet, article type, or commissioned format is specified.

Allowed files: draft, target-outlet-profile, title/abstract if separate, README.md.

Task: audit fit with outlet audience, article type, stance strength, structure, word/reference constraints, and likely editor objections.

## Panel Summary (Orchestrator 合成)

Orchestrator 等待并收集全部 required individual reviews 后，结合 lineage 生成（不得向 reviewer 暴露 evaluator reports）：

- 个体评审汇总
- 冲突、少数意见与 dissent
- 共识问题（≥2 reviewer 指出 → must-fix；低严重度措辞问题 → editorial must-fix）
- Panel 建议评级
- 决策路由

## Decision Routing

| Panel 建议 | 路由 |
|-----------|------|
| strong_support | → final compositor |
| support_with_minor_revision | → STEP 8.5 → final compositor |
| support_after_major_revision | → refinement（≤1轮 panel→revise→panel，仅 major_revision_draft） |
| not_ready | → architect 或 drafter |
| reject_or_redesign | → 停止 |

## Pitfalls

- Panel reviewer 接触 evaluator reports → 破坏独立性
- Narrative Reviewer 看到 skeleton → 失去真实读者视角
- 角色间互相影响 → 必须并行隔离
- Conditional reviewers default to always-on → panel becomes too heavy; add them only when triggered.
- Strawman 反方 → Counter-position Reviewer 须持最强版本反对意见

## References

- Read `references/reviewer-role-definitions.md` when its named guidance or contract applies.
- Read `references/panel-summary-template.md` when its named guidance or contract applies.
- Read `references/decision-routing.md` when its named guidance or contract applies.
