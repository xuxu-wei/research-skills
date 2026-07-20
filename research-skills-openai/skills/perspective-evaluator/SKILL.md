---
name: perspective-evaluator
description: "Independently evaluate only the final reader-ready Perspective for argument, evidence, contribution, and outlet fit."
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
evaluation_stage: scientific | final
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
- 科学评价第一遍不依赖 paragraph-map；仅第二遍可用于架构合规检查
- final evaluation 只读取 final Perspective、installed stable rubric 和一份 minimal evidence/outlet facts bundle；项目内其他文件一律禁止
- final facts 中 discourse 状态为 `incomplete` 或 `unavailable` 时，Novelty 评分必须标注 provisional；不得把未提供的检索当作领域空白
- 对提交前或 language polishing 后的 draft，由 orchestrator 另行显式派发 fresh independent `academic-language-assessor`。本 evaluator 不调用或读取该 assessor 的输出；orchestrator 分别依据两份独立报告路由，语言问题不得替代论证质量判断，但可阻断 final compositor。

## I/O Contract

```
Scientific-evaluation inputs（仅限隔离包）:
  - input-brief, argument-skeleton, draft, paragraph-map, claim-ledger, claim-evidence-matrix, target-outlet-profile, existing-discourse-baseline

Final-evaluation inputs（exact whitelist）:
  - one final frozen Perspective
  - one minimal-evidence-outlet-facts-vNNN.yaml
  - installed references/stable-evaluation-rubric.md and anti-pattern-checklist.md

Required Outputs:
  - scientific: evaluation-report-v{N}.md（八维 + gates + 反模式 + 决策）
  - final: final-evaluation-report-v{N}.md（同一稳定 rubric，严格最小输入）

May Read: 隔离包内所有文件（paragraph-map 仅限第二遍）
Must Not Read: 前次 eval/score/decision, response-to-reviewers, panel, 父目录, 项目 README, previous draft, revision delta。Final evaluation 还禁止 input brief、argument skeleton、paragraph map、claim ledger/matrix、readiness、repair brief、conformance/preservation output、narrative/language report、artifact index 和 workflow state。
Must Not Write: draft, claim-ledger, 非 eval 文件
May Call: 无
Must Not Call: drafter/architect/curator
```

## Evaluation Procedure

先记录 `evaluation_stage: scientific | final`。

### Scientific Evaluation

### Pass 1: Reader-Facing（不读 paragraph-map）
Score: Thesis Clarity, Narrative Coherence, Stance Calibration, Contribution Sufficiency, Audience & Outlet Fit, Novelty

### Pass 2: Architecture Compliance（可读 paragraph-map）
Score: Argument Integrity, Evidence-Claim Match

### Pass 3: Anti-Pattern Scan
逐条扫描 12 项反模式

### Pass 4: Synthesize
汇总 + 决策

### Final Evaluation

1. Read the final Perspective alone and assess thesis clarity, on-page argument integrity, narrative coherence, stance, and contribution.
2. Read only `minimal-evidence-outlet-facts-vNNN.yaml` to assess evidence-claim match, novelty bounds, declared readers, prior knowledge, knowledge to introduce, intended shift, terminology/disclosure order, and outlet constraints. Do not infer the skeleton or ledger from that bundle. Treat `discourse_facts.status: incomplete | unavailable` as a provisional novelty basis rather than evidence of absence.
3. Apply the installed stable rubric and anti-pattern checklist; judge only the current text and clean facts.
4. Return a fresh decision without comparing earlier versions, scores, findings, repair actions, or readiness declarations.

The orchestrator may run deterministic plan/ledger/map conformance before dispatch,
but neither its inputs nor its receipt may enter the final evaluator package.

## Eight Dimensions

1. Thesis Clarity — 读者能否复述核心判断？Hard Gate ≥4 pre-panel
2. Argument Integrity — 论证链完整无跳跃？Hard Gate ≥4 pre-panel
3. Evidence-Claim Match — 最硬主张匹配最硬证据？Hard Gate ≥4 pre-panel
4. Narrative Coherence — 围绕单一论点推进？
5. Stance Calibration — 判断力与克制平衡？
6. Contribution Sufficiency — 读完改变理解？Hard Gate ≥4 pre-panel
7. Audience & Outlet Fit — 匹配目标期刊/读者？
8. Novelty Against Discourse — 超越已有共识？

Use `references/stable-evaluation-rubric.md` as the controlling definitions and
gates. This section remains a concise discovery summary.

### Hard Gates
Draft v1: 任一 hard dimension <3 → redesign；任一 hard dimension =3 → revise；全部 hard dimensions ≥4 → eligible
Pre-panel: Thesis ≥4, Argument ≥4, Evidence ≥4, Contribution ≥4, 无 fatal flaw, 无 unsupported central claim。只有满足全部 pre-panel hard gates 才能输出 `accept`。

## Anti-Patterns (12)
1. Caveat creep（限定堆叠使核心判断难以识别或失去贡献）
2. 审稿回应语言混入
3. 教学式修辞问句
4. Mini-review drift
5. 框架代论证
6. 叙事化临床场景开场
7. 弱证据强主张
8. Orphan paragraph
9. Strawman 反方
10. 过度宣称
11. 同一 counterargument/boundary family 在多个位置完整重复
12. 用“见限制部分”一类指针替代紧邻推理所需的自包含局部边界

## Decision Output
accept / minor_revision / major_revision_draft / argument_rebuild / thesis_redesign / evidence_rebuild / outlet_retarget / reject_not_salvageable

## Conditional Resource

- Read `references/anti-pattern-checklist.md` during Pass 3 when performing the required anti-pattern scan.
- Always read `references/stable-evaluation-rubric.md`; it is the stable rubric for both stages and the only rubric admitted to final evaluation.
- Use `templates/minimal-evidence-outlet-facts.yaml` only when the orchestrator prepares the clean final-evaluation facts bundle; the evaluator never writes or expands that bundle.
