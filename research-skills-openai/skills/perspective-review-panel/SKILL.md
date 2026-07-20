---
name: perspective-review-panel
description: "Independently review a frozen Perspective from one assigned counter-position, evidence, narrative, method, or outlet role."
---
# perspective-review-panel

## Purpose

Perspective 文章的科学外部模拟审稿。默认只要求 Counter-position Reviewer（攻击论证链）和 Evidence Reviewer（检查证据-主张匹配）。Target-reader / Outlet Simulation 是按需角色，只模拟特定读者或编辑如何理解页面内容，不充当 narrative readiness assessor。每个角色必须显式派发到独立 fresh subagent/delegated thread，互不知晓，不接触 evaluator reports。

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

For `target_reader_outlet_simulation`, set `decision: observations_only`; this is an
advisory report disposition, not a panel recommendation or readiness decision.

## Core Rules

- 默认两个科学角色由 orchestrator 显式并行派发，每个角色使用不同的 fresh subagent/delegated thread
- Reviewer 之间互不知晓对方意见
- 所有 reviewer 不接触 evaluator reports
- Target-reader / Outlet Simulation 不接收 argument-skeleton、ledger、readiness 或其他 assessment
- required/conditional scientific reviewer 须说明更宽/更窄 outlet 是否改变建议；optional simulation 只说明观察如何变化
- Orchestrator 必须等待全部 required reviewers 返回后才合成 panel-summary
- 合成必须保留冲突、少数意见和 dissent，不得伪造共识
- required scientific reviewers 的共识问题自动升级 must-fix；若均为低严重度措辞问题，则标为 editorial must-fix。optional simulation 不能单独形成 readiness gate
- 默认面板保持两个科学角色；仅在触发条件存在时增加 conditional reviewer

## Required Reviewer Roles

### Counter-position Reviewer

| 项目 | 内容 |
|------|------|
| 隔离包文件 | draft, argument-skeleton |
| 核心任务 | 持相反立场，攻击核心判断和论证链每一步 |
| 核心问题 | "如果我完全不同意你的前提，你的论证哪一步最先崩溃？" |
| 输出 | 论证链每环抵抗力评分(1-5) + 最弱一环 + 总体建议 + outlet 变化影响声明 |

```
Must Not Read: claim-ledger, evidence-matrix, evaluator reports, 其他 reviewer 评审
```

### Evidence Reviewer

| 项目 | 内容 |
|------|------|
| 隔离包文件 | draft, claim-evidence-matrix, claim-ledger, contrary-evidence-log |
| 核心任务 | 检查证据-主张匹配度、选择性引用、遗漏关键反证、过度推断 |
| 核心问题 | "最硬的主张是否匹配最硬的证据？有没有被忽略的反证？" |
| 输出 | 每步证据充分性评分(1-5) + 证据缺口标注 + 总体建议 + outlet 变化影响声明 |

```
Must Not Read: evaluator reports, 其他 reviewer 评审
```

## Optional Target-Reader / Outlet Simulation

Only add this role when the declared reader baseline is uncertain, a concrete outlet
simulation would materially inform routing, or the user asks for a reader/editor
simulation. It is not a second `research-narrative-assessor`, language assessor, final
evaluator, or readiness gate.

| 项目 | 内容 |
|------|------|
| 隔离包文件 | draft, embedded reader handoff, target-outlet-profile（仅在模拟具体 outlet 时） |
| 核心任务 | 以指定目标读者或编辑身份记录理解断点、概念负担与 outlet-sensitive reactions |
| 核心问题 | "这一类读者在页面上会如何理解、误解或停止跟随论证？" |
| 输出 | locatable reader/editor observations + outlet sensitivity；不得给 narrative readiness 或投稿就绪结论 |

```
Must Not Read: skeleton, evaluator reports, evidence, claim-ledger, readiness, repair history, 其他 reviewer 评审
```

Legacy `Narrative Reviewer` and `Outlet-Fit Editor Reviewer` labels
(`narrative_reviewer`, `outlet_fit_editor_reviewer`) may be read from older projects,
but new dispatches normalize them to
`target_reader_outlet_simulation` and must not run both aliases.

## Conditional Reviewers

Use conditional reviewers only when the trigger is present. They are additive to the default two-reviewer scientific panel and must remain isolated from evaluator reports and other reviewers.

### Methodology / Statistics Reviewer

Trigger when the Perspective contains method-heavy, causal, predictive, statistical, benchmark, or design-quality claims.

Allowed files: draft, claim-evidence-matrix, claim-ledger, and an anonymous frozen methods-facts bundle if needed. The bundle must not expose a reviewer identity, score, decision, route, or report path.

Task: audit whether methodological or statistical claims are properly bounded and whether the article overstates what the methods can establish.

### Practicing-Clinician Reviewer

Trigger when the Perspective involves clinical medicine, public health practice, patient care, guideline interpretation, screening, diagnosis, treatment, or implementation in care settings.

Allowed files: draft, target-outlet-profile, clinical evidence subset if available.

Task: audit clinical plausibility, endpoint relevance, practice-facing implications, and whether the framing would be credible to a frontline clinician.

## Panel Summary (Orchestrator 合成)

Orchestrator 等待并收集全部 required individual reviews 后，结合 lineage 生成（不得向 reviewer 暴露 evaluator reports）：

- 个体评审汇总
- 冲突、少数意见与 dissent
- required scientific reviewers 的共识问题（默认两者均指出 → must-fix；低严重度措辞问题 → editorial must-fix）
- optional simulation 观察单独保存；除非被 required reviewer 独立支持，否则只路由到后续 narrative/outlet 检查，不单独形成 readiness 结论
- Panel 建议评级
- 决策路由

## Decision Routing

| Panel 建议 | 路由 |
|-----------|------|
| strong_support | → STEP 9 editorial quality cycle |
| support_with_minor_revision | → STEP 8.5 → fresh scientific evaluation → STEP 9 |
| support_after_major_revision | → STEP 7 scientific revision（至多一轮 panel major revision） |
| not_ready | → STEP 4 architect（结构变化）或 STEP 5 drafter（skeleton 仍有效） |
| reject_or_redesign | → 停止 |

## Pitfalls

- Panel reviewer 接触 evaluator reports → 破坏独立性
- Target-reader / Outlet Simulation 看到 skeleton 或 readiness history → 失去真实读者视角
- 角色间互相影响 → 必须并行隔离
- Optional simulation 或 conditional reviewers default to always-on → panel becomes too heavy; add them only when triggered.
- Strawman 反方 → Counter-position Reviewer 须持最强版本反对意见

## References

- Read `references/reviewer-role-definitions.md` when its named guidance or contract applies.
- Read `references/panel-summary-template.md` when its named guidance or contract applies.
- Read `references/decision-routing.md` when its named guidance or contract applies.
