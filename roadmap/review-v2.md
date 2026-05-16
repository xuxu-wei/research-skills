总体判断：**v2 已经从“论文写作工作流”升级成了一个相当完整的 manuscript production architecture。核心方向基本稳定，可以作为后续实现的主设计文档。**
但它现在的问题也很明确：**架构正确，但复杂度已经接近系统工程级别；下一步不应继续增加 skill，而应收敛职责、补齐路由细节、定义最小可运行版本。**

我依据你上传的 v2 设计文档评估，其中 v2 明确新增 readiness triage、literature grounder、claim auditor、frontmatter drafter，并引入 Evidence Provenance Ledger、non-compensatory gates、human sign-off checklist 等关键机制。

------

# 一、总体评价

## 1. v2 的核心修订是成功的

你已经解决了 v1 中几个关键问题：

1. **系统定位修正正确**
   从“论文写作器”改成“证据约束下的 manuscript 构建与审查系统”，这是本质升级。论文写作不再是中心，而是输入治理和架构治理之后的执行步骤。
2. **新增 readiness triage 很必要**
   这能避免材料不足、研究设计不清、主要结果缺失时系统硬写 manuscript。
3. **Evidence Provenance Ledger 是关键增强**
   这使得 manuscript 中的主张能够追踪到数据、统计结果、文献、用户断言或假设。这个设计很重要，应该保留为核心 artifact。
4. **claim auditor 与 evaluator 分离是正确的**
   Claim auditor 逐条检查主张—证据；evaluator 判断整体质量。这个分工合理。
5. **frontmatter drafter 与 submission compositor 拆分正确**
   摘要、标题、Key Points、Cover Letter 是实质性写作；compositor 只应负责组装和核查。v2 已经修正了 v1 的职责冲突。
6. **non-compensatory gates 比 simple average 更科学**
   科学有效性、证据—主张一致性不能被语言质量或结构清晰度“平均抵消”。这个改动正确。

所以，v2 的方向没有大问题。

------

# 二、目前最主要的风险：复杂度过高

v2 最大问题不是理念，而是**可执行性**。

你现在设计了一个 15 步、5 阶段、多 artifact、多 gate、多 reviewer 的完整系统。它适合最终目标，但作为初始实现版本过重。

尤其是以下模块之间存在潜在重叠：

| 模块                       | 可能重叠点                                                 |
| -------------------------- | ---------------------------------------------------------- |
| readiness triage           | 与 context builder 的 proceed gate 重叠                    |
| methods-statistics-auditor | 与 evaluator 的 scientific validity 重叠                   |
| claim-auditor              | 与 evaluator 的 evidence-claim alignment 重叠              |
| literature-grounder        | 与 architect 的 novelty positioning 重叠                   |
| review-panel               | 与 evaluator 的部分评估维度重叠                            |
| submission-compositor      | 与 frontmatter-drafter、submission-guard reviewer 部分重叠 |

这些重叠不是错误，但需要通过明确的 **primary responsibility** 控制，否则实现后会出现重复评估、重复修改、循环路由和状态混乱。

建议你引入一个原则：

> 每个 skill 只能拥有一个不可替代的主职责；其他职责只能作为辅助，不得决定最终路由。

例如：

- readiness triage：只判断“能不能进入写作系统”；
- context builder：只标准化输入和分类；
- methods auditor：只判断“方法/统计是否阻断写作”；
- claim auditor：只判断“主张是否有证据支撑”；
- evaluator：只判断“整体 manuscript 是否达到目标质量”；
- panel：只模拟外部审稿视角；
- compositor：只组装和检查投稿包。

------

# 三、文档中有一个明显不一致：skill 数量

v2 写道：

> 完整 Skill 清单（16 个：15 功能 + 1 shared）

但实际列出的目录是：

1. research-article-orchestrator
2. article-readiness-triage
3. article-context-builder
4. article-literature-grounder
5. article-architect
6. article-methods-statistics-auditor
7. article-drafter
8. article-claim-auditor
9. article-evaluator
10. article-refinement-controller
11. article-review-panel
12. article-frontmatter-drafter
13. article-submission-compositor
14. _shared

也就是 **13 个功能 skill + 1 shared = 14 个**，不是 15 + 1。

这需要修正。否则后续实现路线图、目录结构和 manifest 会不一致。

建议写成：

> 完整 Skill 清单：14 个目录，其中 13 个功能 skill + 1 个 shared。

或者如果你确实想保留 15 个功能 skill，那么需要补出缺失的两个，例如：

- `article-reporting-standard-selector/`
- `article-journal-adapter/`

但我不建议现在继续拆。当前已经足够复杂。

------

# 四、Readiness triage 的位置需要微调

你现在把 `article-readiness-triage` 放在 `article-context-builder` 之前。逻辑上可以成立，但有一个问题：

> triage 要判断研究是否可写，必须先知道研究类型、输入材料、主要结果、目标期刊和最小字段是否存在。
> 这些信息其实需要先被初步标准化。

所以建议加一个很轻量的前置步骤，不必变成独立 skill：

```text
Raw Input → Minimal Intake Summary → Readiness Triage → Full Context Brief
```

也就是说：

## Minimal Intake Summary

只提取：

```yaml
minimal_intake_summary:
  study_topic: ""
  apparent_study_type: ""
  available_materials:
    protocol: true | false
    results: true | false
    tables_figures: true | false
    statistical_outputs: true | false
    references: true | false
    target_journal: ""
  obvious_missing_items: []
```

然后 triage 基于这个最小摘要判断能否继续。

这样可以避免 triage 和 context builder 重复解析原始输入。

------

# 五、Fast-track entry 需要补一个“反向构建”机制

你设计了 Fast-Track: Has Draft，可以从 Step 10 claim audit 或 Step 11 evaluation 进入。这个入口很实用，但存在一个技术问题：

> Claim auditor 需要 Claim–Evidence Matrix 和 Evidence Provenance Ledger。
> 如果用户只给了 manuscript 草稿，没有 blueprint，也没有 ledger，claim auditor 无法直接运行。

所以 fast-track 不能真的完全跳过 Phase 1–2。它应该走一个轻量反向构建流程：

```text
Existing Draft
→ manuscript parser
→ inferred claim map
→ inferred evidence map
→ minimal context brief
→ claim audit / evaluation
```

建议新增一个 fast-track 内部模式：

```yaml
backfill_mode:
  required_for_fast_track: true
  artifacts_to_reconstruct:
    - minimal_context_brief
    - inferred_claim_evidence_matrix
    - inferred_evidence_provenance_ledger
    - journal_adapter_minimal
```

否则 fast-track 会在实际运行时卡住。

------

# 六、Literature Grounder 需要定义检索纪律

v2 已经把 literature-grounder 独立出来，这是正确的。但它现在的 contract 仍然偏“结果报告”，缺少检索过程记录。

如果要让它可审计，建议增加：

```yaml
search_protocol:
  databases_searched: []
  search_queries: []
  date_searched: ""
  inclusion_logic: ""
  exclusion_logic: ""
  source_priority:
    - guidelines
    - landmark_trials
    - systematic_reviews
    - recent_original_studies
    - editorials_or_commentaries
```

还要增加：

```yaml
coverage_assessment:
  seminal_literature_covered: yes | partial | no | unclear
  recent_literature_covered: yes | partial | no | unclear
  conflicting_literature_checked: yes | partial | no
```

否则 literature grounding 很容易变成“找了几篇文献来支持写作”，而不是系统性地定位 novelty、gap 和 competing evidence。

尤其对顶刊 manuscript，最危险的是：

- gap 是假的；
- novelty 被已有文献覆盖；
- Discussion 忽略了相反证据；
- 引用全是近年小样本研究，缺少经典文献。

------

# 七、Methods auditor 的输入边界需要再明确

Methods auditor 在 drafting 前运行是正确的，但它需要审计的是“已完成研究的方法”，不是 manuscript 里的 Methods 文本。

因此它的输入应该明确包括：

```yaml
methods_auditor_inputs:
  context_brief: required
  protocol_or_sap: optional
  statistical_output: recommended
  analysis_plan_description: required_if_no_sap
  tables_figures: optional
  raw_data: optional
  manuscript_methods_section: optional
```

同时它的判断语言要非常谨慎。很多时候它无法知道真实方法是否错误，只能判断：

- reported information insufficient；
- potential issue；
- requires author/statistician verification；
- likely methodologic flaw；
- definite methodologic flaw。

建议把 `audit_status` 改成更审慎的层级：

```yaml
audit_status:
  pass
  conditionally_pass_with_author_verification
  requires_methods_clarification
  requires_reanalysis
  methodologically_blocked
```

这样比 `pass | conditionally_pass | methodologically_blocked` 更适合真实场景。

------

# 八、Evidence Provenance Ledger 很重要，但要防止过度工程化

EPL 是 v2 的核心增强，但段落级挂接会显著增加实现成本。

建议分两级：

## Level 1：claim-level provenance

最小可运行版本先做到：

```yaml
claim_id → evidence_id → source → verification_status
```

## Level 2：paragraph-level provenance

高级版本再做到：

```yaml
paragraph_id → claim_id → evidence_id → display_id
```

否则 v0.1 就要求段落级 provenance，会导致 drafter 和 auditor 过重。

建议在设计中写明：

```yaml
provenance_granularity:
  minimum: claim_level
  preferred: paragraph_level
  advanced: sentence_level
```

不要一开始就把 paragraph-level 作为硬要求。

------

# 九、Reporting checklist mapping 需要 item library 支撑

你已经把 reporting checklist 从简单 status 升级为 item-level mapping，这是正确的。

但这会引出一个实现问题：

> 如果系统没有内置 CONSORT、STROBE、PRISMA、TRIPOD 等 checklist 的 item library，它无法可靠生成 item-level mapping。

所以 `_shared` 里需要有：

```text
_shared/reporting-standards/
  CONSORT.yaml
  STROBE.yaml
  PRISMA.yaml
  TRIPOD.yaml
  STARD.yaml
  ARRIVE.yaml
  COREQ.yaml
  CHEERS.yaml
```

每个文件至少包括：

```yaml
standard: STROBE
version: "2007"
items:
  - item_id: "STROBE-01"
    section: "Title and abstract"
    requirement: ""
    criticality: critical | recommended
    expected_location: []
```

没有 item library，item-level mapping 会变成形式化输出。

------

# 十、Journal Adapter 需要拆成“已验证”和“用户提供”两种路径

v2 的 journal adapter 已经从风格分类升级为 hard constraints、soft preferences、strategic fit，这是正确的。

但实际使用中会有两种情况：

## A. 系统可以联网核查期刊要求

此时：

```yaml
retrieval_status: verified
source_checked_date: ""
```

## B. 用户只提供目标期刊名称，系统没有实际核查 author instructions

此时：

```yaml
retrieval_status: not_checked
confidence: low
```

在 B 情况下，不应该输出“满足目标期刊要求”，只能输出：

> 依据用户提供信息进行初步适配；正式投稿前必须人工核对 author instructions。

建议在 compositor 中增加 gate：

```yaml
journal_requirements_verified:
  status: verified | user_supplied_only | not_checked
  package_consequence:
    verified: can_mark_ready
    user_supplied_only: ready_for_author_check
    not_checked: partial
```

否则 `submission-ready` 这个词会过度承诺。

------

# 十一、Submission package 的 status 建议改名

现在 package status 有：

```yaml
ready | minor_revision_pending | major_revision_required | blocked | partial
```

但 v2 又加入了 human sign-off checklist。既然最终投稿必须由作者确认数据、统计、伦理、COI、作者贡献、期刊要求等，系统不应轻易标记 `ready`。

建议改为：

```yaml
status:
  ready_for_author_signoff
  minor_revision_pending
  major_revision_required
  blocked
  partial
```

只有在人类确认后，才可以在外部流程中叫 submission ready。

这样更符合你 v2 中“所有未验证数据、缺失材料、作者需确认事项明确标注”的定位。

------

# 十二、Results organization modes 已明显改进，但还可以再细化 AI/ML

v2 把 Results 组织方式从 2 种扩展为 6 种，这是很好的改动。

但 AI/ML 仍然容易混乱。建议在 AI/ML 下再分：

| AI/ML 类型                           | 组织逻辑                                                     |
| ------------------------------------ | ------------------------------------------------------------ |
| clinical prediction model            | norm_driven，重点是数据、开发、验证、校准、临床效用          |
| diagnostic AI                        | norm_driven，类似诊断研究，需 index test/reference standard  |
| algorithmic method                   | artifact_driven / argument_driven，重点是模型创新、benchmark、ablation |
| foundation model / general AI system | artifact_driven，重点是数据、训练、能力评估、安全性、泛化    |
| deployment study                     | norm_driven / hybrid，重点是真实环境表现、工作流、效用、安全性 |

否则 AI/ML 文章会被过早归到 `argument_driven`，导致写作像技术故事，而不是规范化验证论文。

------

# 十三、Refinement controller 设计很好，但需要加入“禁止修订”的判断

v2 已经加入：

- textual_revision
- structural_revision
- evidence_relinking
- reporting_completion
- claim_downscaling
- methods_detailing
- journal_retargeting

并明确 `analysis_required` 和 `study_redesign_required` 不可由写作修复。这个非常重要。

建议进一步增加：

```yaml
revision_allowed:
  yes | no | conditional
reason_if_no: ""
required_external_action:
  reanalysis | new_experiment | statistician_review | ethics_confirmation | journal_requirement_check
```

这样 refinement-controller 不会在遇到研究本身缺陷时继续“润色”。

------

# 十四、Review panel 的双模式设计是对的

v2 区分：

- `blind_external_simulation`
- `internal_diagnostic_review`

并且给不同 reviewer 设置差异化输入，这个设计是成熟的。尤其是 methodology/statistics reviewer 在 diagnostic 模式下可以看到 context brief、protocol/SAP 和 tables，这能区分“稿件写得不清楚”与“研究设计本身有问题”。

唯一建议是增加一个 panel aggregation rule。

例如：

```yaml
panel_aggregation_rules:
  if_methodology_reviewer_rejects_for_fatal_flaw: aggregated_recommendation_cannot_exceed_not_ready
  if_evidence_claim_reviewer_flags_fatal_overclaim: require_refinement_before_submission
  if_submission_guard_blocks_for_missing_required_items: package_status_cannot_be_ready
```

否则 panel report 聚合时可能出现多数支持、但方法学 reviewer 发现致命问题的矛盾。

------

# 十五、最小可运行版本建议

v2 现在已经足够完整。下一步不要继续扩展，而是定义 MVP。

我建议 MVP 只包含 8 个核心模块：

```text
1. research-article-orchestrator
2. article-readiness-triage
3. article-context-builder
4. article-architect
5. article-methods-statistics-auditor
6. article-drafter
7. article-claim-auditor
8. article-evaluator
```

暂缓：

```text
article-literature-grounder
article-review-panel
article-frontmatter-drafter
article-submission-compositor
```

原因：

- 没有 readiness / context / blueprint / audit / draft / claim audit / evaluation，后面的投稿交付没有意义；
- literature grounder 和 review panel 很重要，但依赖外部检索与 subagent 能力，适合作为第二阶段；
- frontmatter 和 compositor 可以在正文稳定后再做。

MVP 的交付目标不要设为“完整投稿包”，而是：

> 生成一份 evidence-constrained manuscript draft，并附带 claim audit 和 evaluation report。

这更现实。

------

# 十六、建议你现在修改 v2 的具体位置

## 必改项

1. 修正 skill 数量：当前是 13 功能 + 1 shared，不是 15 + 1。
2. 增加 Minimal Intake Summary，避免 readiness triage 和 context builder 重复。
3. 为 Fast-Track 增加 backfill mechanism。
4. 给 Literature Grounder 增加 search protocol。
5. 把 Evidence Provenance Ledger 分成 claim-level minimum 和 paragraph-level advanced。
6. 把 submission package `ready` 改为 `ready_for_author_signoff`。
7. 为 reporting checklist mapping 增加 item library 依赖。
8. 为 panel aggregation 增加 non-compensatory rule。

## 可选增强项

1. AI/ML 子类型再细分。
2. Methods auditor 增加 `requires_methods_clarification` 状态。
3. Journal adapter 增加 `ready_for_author_check` 与 `verified` 区分。
4. Refinement controller 增加 `revision_allowed` 判断。
5. Human sign-off 作为最终硬门禁，而不是 checklist 附件。

------

# 最终结论

v2 已经是一个合理、严肃、可扩展的 Article 系列 skill 总体设计。它的核心结构可以保留：

> Input Governance → Architecture Governance → Writing → Quality Control → Submission Delivery

其中最有价值的三个设计是：

1. **Evidence Provenance Ledger**
2. **Claim Auditor**
3. **Non-compensatory Evaluation Gates**

但 v2 还不是最优实现蓝图。它现在偏“大而全”，需要进入收敛阶段。

我建议你把下一版 v3 的目标定为：

> 不再增加新 skill，而是压实 execution contract、routing logic、MVP 范围和 artifact granularity。

最重要的一句话：

> v2 的理念已经成熟；v3 应该解决“如何稳定运行、如何避免重复判断、如何在材料不完整时安全降级”的问题。