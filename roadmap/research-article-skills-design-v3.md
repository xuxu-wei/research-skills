# research-article Skills: Design Document v3

> **Status**: Draft v0.3.0 — Convergence & Execution Contract
> **Author**: Xuxu Wei
> **Date**: 2026-05-16
> **Previous**: v0.1.0 (`research-article-skills-design.md`), v0.2.0 (`research-article-skills-design-v2.md`)
> **Review basis**: `roadmap/review-v1.md`, `roadmap/review-v2.md`
>
> **v3 定位**：不再增加新 skill。在 v2 架构方向确认的基础上，压实 execution contract、routing logic、MVP 范围和 artifact granularity。解决"如何稳定运行、如何避免重复判断、如何在材料不完整时安全降级"的问题。

---

## 1. 定位（v2 确认，v3 微调措辞）

> 以已有研究数据、结果、研究设计背景信息为起点，通过**输入治理 → 架构治理 → 证据约束起草 → 多层质量审查 → 投稿组装**五个阶段，交付一份 **submission-ready manuscript package**。
>
> 所有未验证数据、缺失材料、作者需确认事项和不可由写作修复的方法学问题均明确标注。系统不替代作者对数据真实性、统计正确性、伦理合规和作者责任的最终确认。

**系统本质**：证据约束下的投稿级 manuscript 构建与审查系统——不是论文写作器。

**顶层模型**（不变）：

```
Question → Design → Evidence → Inference → Boundary → Meaning
```

**三层结构**（不变）：

```
Layer 1: 普遍论证规律 → Layer 2: 研究类型与报告规范 → Layer 3: 期刊约束系统
```

---

## 2. 核心设计原则

### 2.1 Primary Responsibility 原则

> 每个 skill 只拥有一个不可替代的主职责。其他职责只能作为辅助，不得决定最终路由。

| Skill | Primary Responsibility | 不可由其他 skill 替代 |
|-------|----------------------|---------------------|
| readiness-triage | 判断"能不能进入写作系统" | context builder 不判断 readiness |
| context-builder | 标准化输入和分类 | triage 不做深层标准化 |
| literature-grounder | 系统性文献定位与检索追溯 | architect 不替代检索 |
| architect | 设计论文架构和 EDP | drafter 不设计架构 |
| methods-auditor | 判断"方法/统计是否阻断写作" | evaluator 不做 pre-drafting audit |
| drafter | 按蓝图起草 manuscript 正文 | 无替代 |
| claim-auditor | 逐条判断"主张是否有证据支撑" | evaluator 不做逐条审计 |
| evaluator | 判断"整体 manuscript 是否达到目标质量" | claim-auditor 不做整体评价 |
| refinement-controller | 管理修订循环和修订模式路由 | orchestrator 不管理修订细节 |
| review-panel | 模拟外部审稿视角 | evaluator 不模拟多角色审稿 |
| frontmatter-drafter | 起草摘要/标题/Key Points/Cover Letter | drafter 不起草 frontmatter |
| submission-compositor | 组装投稿包 + 格式核对 | frontmatter-drafter 不组装 |

### 2.2 Non-Compensatory Gate 原则

> 关键质量维度不可被其他维度的平均分抵消。

- Scientific Validity 和 Evidence-Claim Alignment 是 non-compensatory
- 若 fatal_scientific gate 失败，无论其他维度多高，manuscript 不得标记为可投稿

### 2.3 Safe Degradation 原则

> 当输入材料不完整或某 skill 无法满血运行时，系统应安全降级，而非静默填补缺口或硬写。

降级策略：
- 标记 `verification_status: user_supplied_unverified`
- 标记 `confidence: low`
- 将 package status 限制为 `partial` 或 `ready_for_author_check`
- 不将 `not_checked` 伪称为 `verified`

---

## 3. 修订后的 Skill 架构

### 3.1 Skill 清单（14 个目录：13 功能 + 1 shared）

```
research-article/
  research-article-orchestrator/          # [编排器] 工作流编排 + 路由决策
  article-readiness-triage/               # [门禁] 判断能否进入写作系统
  article-context-builder/                # [构建] 输入标准化 + 研究类型分类 + 报告规范选择
  article-literature-grounder/            # [构建] 文献定位、检索追溯与引用支撑
  article-architect/                      # [构建] 论文架构 + EDP + Evidence Provenance Ledger
  article-methods-statistics-auditor/     # [审计] 起草前方法/统计阻断判断
  article-drafter/                        # [构建] 按蓝图起草 manuscript 正文
  article-claim-auditor/                  # [审计] 逐条主张—证据核查
  article-evaluator/                      # [评估] 整体质量 non-compensatory 评价
  article-refinement-controller/          # [控制] 修订循环 + 修订模式路由
  article-review-panel/                   # [评估] 多角色模拟审稿
  article-frontmatter-drafter/            # [构建] 摘要/标题/Key Points/Cover Letter
  article-submission-compositor/          # [组装] 只组装 + 格式核对 + human sign-off
  _shared/                                # [参考] artifact contracts + reporting standards library + handoff rules
```

**计数修正说明**：v2 误写为"15 功能 + 1 shared"。实际目录为 13 功能 + 1 shared = 14。reporting-standard-selector 和 evidence-display-planner 内嵌于 context-builder 和 architect，不独立成 skill。

### 3.2 职责与隔离规则

| Skill | 角色 | 执行方式 | 是否可路由 |
|-------|------|---------|-----------|
| orchestrator | 编排 | inline | 控制全部路由 |
| readiness-triage | 门禁 | isolated subagent | 输出 readiness_status 决定是否继续 |
| context-builder | 构建 | inline | 输出 proceed_status |
| literature-grounder | 构建 | inline | 输出 grounding_confidence |
| architect | 构建 | inline | 输出 blueprint |
| methods-auditor | 审计 | isolated subagent | 输出 audit_status；若 blocked 则停止 |
| drafter | 构建 | inline | 按蓝图起草 |
| claim-auditor | 审计 | isolated subagent | 输出 recommendation；若 blocked 则停止 |
| evaluator | 评估 | isolated subagent | 输出 decision；若 reject 则停止 |
| refinement-controller | 控制 | inline | 管理修订循环 |
| review-panel | 评估 | isolated subagents | 输出 aggregated_recommendation |
| frontmatter-drafter | 构建 | inline | 输出 frontmatter |
| submission-compositor | 组装 | inline | 输出 package + human sign-off checklist |

**隔离规则**：
- drafter / evaluator / refinement-controller 不得合并
- architect / drafter 不得合并
- claim-auditor / evaluator 独立运行，互补不互替
- 所有 auditor 和 evaluator 角色必须通过隔离子 agent 执行
- 若运行时不支持 subagent delegation，按 `_shared/references/runtime-delegation.md` 执行 fallback

---

## 4. 标准流程（15 步，5 阶段）

```
Phase 1: 输入治理 (Input Governance)
  0. Minimal Intake Summary           [NEW v3] 轻量前置提取
  1. Article Readiness Triage
  2. Context Brief + Reporting Standard Selection
  3. Literature Grounding

Phase 2: 架构治理 (Architecture Governance)
  4. Article Blueprint
  5. Claim–Evidence Matrix + Evidence Provenance Ledger
  6. Evidence Display Plan
  7. Methods / Statistics Audit

Phase 3: 写作 (Writing)
  8. Manuscript Drafting

Phase 4: 质量控制 (Quality Control)
  9. Claim-Level Audit
  10. Independent Evaluation
  11. Targeted Refinement (if needed)
  12. Mock Review Panel (if requested)

Phase 5: 投稿交付 (Submission Delivery)
  13. Frontmatter Drafting
  14. Submission Compositor
```

### 4.1 Step 0: Minimal Intake Summary [NEW v3]

**为什么需要**：readiness triage 需要知道研究类型、可用材料和目标期刊才能判断"能不能写"，但这些信息在 context builder 标准化之前尚未整理。Minimal Intake Summary 是一个极轻量的前置提取，避免 triage 和 context builder 重复解析原始输入。

**不由独立 skill 执行**——由 orchestrator 在调用 readiness triage 之前 inline 完成。

**提取内容**：

```yaml
minimal_intake_summary:
  study_topic: ""
  apparent_study_type: ""             # rough classification
  available_materials:
    protocol_or_sap: true | false
    primary_results: true | false
    tables_figures: true | false
    statistical_outputs: true | false
    methods_description: true | false
    references: true | false
  stated_target_journal: ""
  obvious_missing_items: []           # e.g., "no primary outcome defined", "no sample size"
```

**输出**：传给 readiness triage 作为输入。不替代 context brief。

### 4.2 Phase Gates

每个 phase 结束时，orchestrator 检查 phase gate：

```yaml
phase_gates:
  input_governance:
    required: [readiness_status ∈ {ready, conditionally_ready}, proceed_status ∈ {proceed, proceed_with_assumptions}]
    block_if: readiness_status = not_ready OR proceed_status = clarification_stop
  architecture_governance:
    required: [blueprint complete, methods_audit_status ∈ {pass, conditionally_pass_with_author_verification, requires_methods_clarification}]
    block_if: methods_audit_status ∈ {requires_reanalysis, methodologically_blocked}
  writing:
    required: [draft exists, all sections != pending]
    block_if: draft unreadable
  quality_control:
    required: [claim_audit passes, evaluation decision ∈ {accept, revise}]
    block_if: evaluation decision = reject
  submission_delivery:
    required: [frontmatter complete, package assembled]
```

---

## 5. 入口模式与路由

### 5.1 入口模式总览

| 模式 | 触发条件 | 起点 | 终点 |
|------|---------|------|------|
| **Standard** | 用户提供数据/结果/设计信息 | Step 0 | Step 14 |
| **Fast-Track: Has Draft** | 用户有 manuscript 草稿 | Step 0 → backfill → Step 9 | Step 14 |
| **Fast-Track: Draft + Eval** | 用户有草稿和外部评估 | Step 0 → backfill → Step 11 | Step 14 |
| **Blueprint-Only** | 用户想在起草前审查架构 | Step 0 | Step 7 |
| **Section-Specific** | 只需特定章节 | Step 0 → backfill → Step 8 (section mode) | Step 8 |
| **Submission-Only** | 用户有终稿，仅需投稿材料 | Step 0 → backfill → Step 13 | Step 14 |

### 5.2 Fast-Track Backfill Mechanism [NEW v3]

**问题**：Fast-track 入口跳过 Phase 1–2，但 claim-auditor 需要 Claim–Evidence Matrix 和 Evidence Provenance Ledger 才能运行。不能真的跳过。

**方案**：Fast-track 走一个轻量反向构建流程，从已有 manuscript 草稿反向提取最小必要 artifact：

```yaml
backfill_mode:
  required_for_fast_track: true
  source: existing_manuscript_draft
  artifacts_to_reconstruct:
    - minimal_context_brief             # 从 Methods 提取研究设计、对象、变量
    - inferred_claim_evidence_matrix    # 从 Results/Discussion 提取主张
    - inferred_evidence_provenance_ledger # 从 Results 段落提取证据引用
    - journal_adapter_minimal           # 从用户提供的目标期刊名构建
  reconstruction_confidence: high | medium | low   # 低时标记 scope_limitation
  skipped_permanently:                  # 不可反向构建的
    - readiness_triage                  # 跳过，但记录 limitation
    - methods_audit                     # 跳过，但记录 limitation
    - literature_grounding              # 跳过，但记录 limitation
```

**反向构建流程**（由 orchestrator 调度，不新增独立 skill）：

1. **Manuscript Parser**（orchestrator inline）：
   - 从 Methods 提取：研究设计描述、对象、纳排标准、变量定义、统计方法
   - 从 Results 提取：段落级主张、figure/table 引用、数值结果
   - 从 Introduction 提取：研究问题、gap 描述
   - 从 Discussion 提取：主要发现、局限性
2. **Inferred Claim Map**：
   - 每个 Results/Discussion 段落提取一个 claim
   - 标注推断类型：作者原文 / 系统推断
3. **Inferred Evidence Map**：
   - 每个数值结果或引用提取一个 evidence entry
   - 标注 `verification_status: inferred`（因为未验证原始数据）
4. **Minimal Context Brief**：
   - 从草稿反向填充 context brief 的必要字段
   - `source: reverse_engineered_from_draft`
5. 所有反向构建的 artifact 标记 `confidence: low | medium`
6. 在 workflow state 中记录 `scope_limitation: fast_track_backfill`

---

## 6. 核心 Skill 执行合约（压缩版）

以下只列出 v3 中执行逻辑有实质变更的 skill。v2 中已稳定且 v3 未修改的 skill 不再重复。

### 6.1 article-readiness-triage

**输入**：`minimal_intake_summary`（来自 Step 0）

**主职责**：判断"这个研究是否具备进入 manuscript 写作系统的最低条件"。

**不可被替代的决策**：
- `ready`：进入 context builder
- `conditionally_ready`：进入 context builder，附带 nonblocking gaps
- `not_ready`：停止，返回 blocking gaps
- `wrong_article_type`：建议更换 article type 后重新 triage

**不负责**：
- 不标准化输入（由 context builder 负责）
- 不检索文献（由 literature grounder 负责）
- 不审计方法细节（由 methods auditor 负责）

**输出**：`ArticleReadinessReport`（结构同 v2，略）

### 6.2 article-context-builder

**输入**：原始用户材料 + readiness report

**主职责**：标准化输入 + 分类研究类型 + 匹配报告规范。

**内部三步**：
1. Normalize：统一字段
2. Classify：研究类型 + 文章类型 + 报告规范
3. Gate：`proceed | proceed_with_assumptions | clarification_stop`

**报告规范映射规则**（v2 确认，v3 补充实现依赖）：
- 多规范并用
- Extension 优先
- 期刊特定要求覆盖默认规范
- 混合设计 → 主规范 + 辅助规范
- 无合适规范 → 标记 `no_exact_guideline_found`
- 映射结果写入 `reporting_standard_selection`
- **依赖**：需 `_shared/reporting-standards/` 中的 item library（见 8.1）

### 6.3 article-literature-grounder

**输入**：context brief

**主职责**：通过可审计的检索过程，为 manuscript 提供文献定位。

**检索纪律** [NEW v3]：

```yaml
search_protocol:
  databases_searched: []             # e.g., PubMed, Web of Science, Scopus
  search_queries: []                 # 实际使用的检索式
  date_searched: ""
  inclusion_logic: ""                # 为什么纳入某些文献
  exclusion_logic: ""                # 为什么排除某些文献
  source_priority:                   # 检索优先级
    - guidelines                     # 指南/共识
    - landmark_trials_or_studies     # 里程碑研究
    - systematic_reviews             # 系统综述
    - recent_original_studies        # 近期原始研究
    - editorials_or_commentaries     # 述评（低优先级）
  coverage_assessment:               # [NEW v3] 检索充分性自评
    seminal_literature_covered: yes | partial | no | unclear
    recent_literature_covered: yes | partial | no | unclear
    conflicting_literature_checked: yes | partial | no
```

**不负责**：
- 不替代 `research-opportunity-mapper`（后者用于 idea/opportunity discovery）
- 不决定 novelty claim 是否成立（由 architect 和 claim-auditor 判断）
- 不生成 manuscript 正文（由 drafter 负责）

**输出**：`LiteratureGroundingReport`（结构同 v2，增加 search_protocol 和 coverage_assessment）

### 6.4 article-methods-statistics-auditor

**输入**：context brief + protocol/SAP（如有）+ statistical output（推荐）+ analysis plan description（如无 SAP）

**主职责**：在 drafting 前判断方法/统计是否存在阻断写作的缺陷。

**输入边界** [v3 明确]：

```yaml
methods_auditor_inputs:
  context_brief: required
  protocol_or_sap: optional
  statistical_output: recommended
  analysis_plan_description: required_if_no_sap
  tables_figures: optional            # 用于交叉检查
  raw_data: optional
```

**审计状态** [v3 扩展]：

```yaml
audit_status:
  pass                                          # 方法可辩护，可进入 drafting
  conditionally_pass_with_author_verification   # 有不确定项，需作者确认
  requires_methods_clarification                # Methods 描述不完整，需补充但不阻断
  requires_reanalysis                           # 分析需重做，不可由写作修复
  methodologically_blocked                      # 研究设计缺陷，不可由写作修复
```

**对路由的影响**：
- `pass` / `conditionally_pass_with_author_verification` → 进入 drafting
- `requires_methods_clarification` → 进入 drafting，但标记 methods 段落需特别关注
- `requires_reanalysis` → 停止，告知用户先重新分析
- `methodologically_blocked` → 停止

**不负责**：
- 不评价 manuscript 写得好不好（由 evaluator 负责）
- 不逐条审计主张（由 claim-auditor 负责）
- 不替代统计咨询（标记 uncertain 而非强行判断）

### 6.5 article-claim-auditor

**主职责**：逐条核查每个核心主张是否有证据支撑、推断是否成立、措辞是否恰当。

**不可被 evaluator 替代**：evaluator 评价整体质量，claim-auditor 逐条审计。

**对路由的影响**：
- `pass` → 进入 evaluator
- `downscale_and_proceed` → 进入 refinement（claim downscaling）
- `revise_and_reaudit` → 进入 refinement
- `blocked`（fatal overclaims 非空）→ 停止，必须先修复

**不负责**：
- 不评价整体结构和清晰度（由 evaluator 负责）
- 不重写 claims（由 drafter 通过 refinement 执行）
- 不判断期刊适配性（由 evaluator 和 submission-guard reviewer 负责）

### 6.6 article-evaluator

**主职责**：判断整体 manuscript 是否达到目标期刊的投稿质量。

**不负责**：
- 不逐条审计 claims（由 claim-auditor 负责）
- 不审计方法细节（由 methods-auditor 负责）
- 不判断能否进入写作（由 readiness-triage 负责）

**Non-Compensatory Gates**（v2 确认）：

```yaml
noncompensatory_gates:
  - gate: "methods_support_primary_claim"
    status: pass | fail
    consequence: "blocked — readiness_level = methodologically_blocked"
  - gate: "primary_evidence_exists"
    status: pass | fail
    consequence: "blocked — readiness_level = not_ready"
  - gate: "no_fatal_overclaim"
    status: pass | fail
    consequence: "blocked — must downscale before submission"
  - gate: "no_fatal_scientific_flaw"
    status: pass | fail
    consequence: "blocked — readiness_level = methodologically_blocked"
```

**Decision 路由**（v2 确认，v3 补充）：

| Decision | 条件 | 路由 |
|----------|------|------|
| `accept` | 所有 non-compensatory gates pass + 整体达标 | review panel（如请求）或 compositor |
| `revise` | 存在可修复问题 | refinement-controller |
| `reject` | 存在不可修复 fatal flaw | 停止，记录 |
| `stop_no_gain` | re-evaluation 无实质改进 | 停止 |

### 6.7 article-refinement-controller

**修订模式分类**（v2 确认，v3 增加 `revision_allowed` gate）[NEW v3]：

```yaml
revision_allowed:
  yes | no | conditional
  reason_if_no: ""                    # e.g., "requires reanalysis, not fixable by writing"
  required_external_action:           # 当 revision_allowed = no 时必填
    reanalysis | new_experiment | statistician_review | ethics_confirmation | journal_requirement_check
```

**修订模式**（v2 确认）：

| 模式 | 可在 skill 内处理 | 需要用户介入 |
|------|------------------|-------------|
| textual_revision | 是 | 否 |
| structural_revision | 是 | 否（需确认新结构） |
| evidence_relinking | 是 | 否 |
| reporting_completion | 是 | 否 |
| claim_downscaling | 是 | **是**（降低主张强度需作者确认） |
| methods_detailing | 是 | 可能需要作者补充信息 |
| journal_retargeting | 是 | **是**（换期刊是作者决策） |
| analysis_required | 否 | **是** |
| study_redesign_required | 否 | **是** |

**Claim Downscaling**（v2 确认，v3 补充作者确认要求）：

```yaml
claim_revision_action:
  claim_id: "C001"
  action: downscale
  original_wording: "X significantly reduces Y"
  issue: "observational design, causal language not justified"
  revised_wording: "X was associated with lower Y after adjustment for confounders..."
  requires_author_confirmation: true  # downscale 必须作者确认
```

### 6.8 article-review-panel

**双模式**（v2 确认，v3 增加 aggregation rule）：

**Panel Aggregation Rule** [NEW v3]：

```yaml
panel_aggregation_rules:
  - rule: "methodology reviewer fatal flaw"
    condition: "any methodology reviewer reports fatal_scientific_flaw"
    effect: "aggregated_recommendation CANNOT exceed not_ready"
  - rule: "evidence-claim reviewer fatal overclaim"
    condition: "any evidence-claim reviewer flags fatal_overclaim"
    effect: "require refinement before submission regardless of other reviewers"
  - rule: "submission-guard blocks"
    condition: "submission-guard reviewer flags missing required journal items"
    effect: "package_status cannot be ready_for_author_signoff"
  - rule: "dissenting opinion"
    condition: "any reviewer recommendation differs by >= 2 levels from others"
    effect: "dissent must be explicitly addressed in panel summary, not averaged away"
```

### 6.9 article-frontmatter-drafter

**主职责**：起草摘要、Key Points、标题、Running title、Highlights、Graphical abstract text、Cover letter 初稿。

**约束**：
- 不得修改 manuscript 正文
- 不得改变 contribution statement 的核心主张
- Abstract 中不得引入 manuscript 没有的结果
- Cover letter 中不得做出 manuscript 不支持的 novelty claim

### 6.10 article-submission-compositor

**主职责**：只组装 + 核查 + human sign-off。

**Journal Requirements Verification Tier** [NEW v3]：

```yaml
journal_requirements_verified:
  status: verified | user_supplied_only | not_checked
  package_consequence:
    verified: can_mark "ready_for_author_signoff"
    user_supplied_only: must_mark "ready_for_author_check"
    not_checked: must_mark "partial"
```

**Package Status** [v3 修改]：

```yaml
status:
  ready_for_author_signoff        # 所有 system 可验证的 gate 通过 + journal verified
  ready_for_author_check          # journal requirements 未验证，需作者核实
  minor_revision_pending          # 存在 minor revision 未完成
  major_revision_required         # 存在 major revision 未完成
  blocked                         # 存在不可由写作修复的阻断项
  partial                         # 材料不完整
```

`ready` 不再作为系统状态。`ready_for_author_signoff` 是系统能给出的最高状态——之后还需作者确认。

**Human Sign-off Checklist**（v2 确认，v3 升级为 hard gate）：

```yaml
human_signoff_required:
  data_accuracy: true
  statistical_results_verified: true
  author_contributions_verified: true
  ethics_and_consent_verified: true
  conflicts_of_interest_verified: true
  journal_requirements_verified: true
  figure_quality_verified: true
  reference_accuracy_verified: true
  corresponding_author_confirmed: true
```

**Sign-off 作为最终门禁**：若 `human_signoff_required` 中任何项未经作者显式确认，package status 不得超过 `ready_for_author_check`。

---

## 7. 核心 Artifact 合约（v3 调整）

### 7.1 Evidence Provenance Ledger — 分级粒度 [NEW v3]

v2 要求段落级挂接。v3 将 provenance 分为三级，minimum 为 claim-level：

```yaml
provenance_granularity:
  minimum: claim_level           # v0.1.0 MVP 目标
  preferred: paragraph_level     # v0.5.0+
  advanced: sentence_level       # v1.0.0+
```

**Level 1: Claim-Level Provenance（MVP）**：

```yaml
evidence_provenance_ledger:
  - evidence_id: "E001"
    claim_ids: ["C001"]
    evidence_type: statistical_result | literature_reference | user_assertion | assumption
    source_description: ""        # 人类可读的来源描述
    verification_status: verified | user_supplied_unverified | inferred | missing
    risk_level: low | medium | high
```

**Level 2: Paragraph-Level Provenance（v0.5.0+）**：

在 Level 1 基础上增加：

```yaml
    appears_in:
      manuscript_section: "Results"
      paragraph_id: "R-P03"
      display_id: "D001"
    numeric_values:
      estimate: ""
      ci_lower: ""
      ci_upper: ""
      p_value: ""
      sample_size: ""
```

### 7.2 Manuscript Draft v3

```yaml
manuscript_draft:
  schema_version: "research-article.v3"
  draft_id: "manuscript-v001"
  version: 1
  sections:
    introduction:
      content: ""
      word_count: 0
    methods:
      content: ""
      word_count: 0
      reporting_items_covered: []
    results:
      content: ""
      word_count: 0
    discussion:
      content: ""
      word_count: 0
  # paragraph-level linking (Level 2+, not required for MVP)
  paragraphs: []
  display_items:
    - display_id: "D001"
      type: table | figure | flow_diagram | forest_plot | model_diagram | supplementary_table | supplementary_figure
      title: ""
      supported_claims: ["C002"]
      evidence_ids: ["E001"]
      placement: main | supplementary
      status: drafted | final | missing
  reporting_checklist_mapping:
    standard: ""
    items: []
  unresolved_issues: []
```

### 7.3 Reporting Standards Item Library [NEW v3]

`_shared/reporting-standards/` 目录下的 item library 是 item-level checklist mapping 的支撑：

```
_shared/reporting-standards/
  CONSORT.yaml
  STROBE.yaml
  PRISMA.yaml
  TRIPOD.yaml
  STARD.yaml
  ARRIVE.yaml
  COREQ.yaml
  CHEERS.yaml
  SQUIRE.yaml
  CARE.yaml
```

每个文件至少包含：

```yaml
standard: STROBE
version: "2007"
last_verified: ""
source_url: "https://www.equator-network.org/reporting-guidelines/strobe/"
items:
  - item_id: "STROBE-01"
    section: "Title and abstract"
    requirement: "Indicate the study's design with a commonly used term in the title or the abstract"
    criticality: critical | recommended
    expected_location: ["Title", "Abstract"]
  - item_id: "STROBE-02"
    section: "Introduction: Background/rationale"
    requirement: "Explain the scientific background and rationale for the investigation being reported"
    criticality: critical
    expected_location: ["Introduction"]
  # ...
```

无 item library，item-level mapping 退化为形式输出——系统无法可靠验证 checklist item 是否被覆盖。

---

## 8. 路由决策表（v3 新增）

### 8.1 Phase Gate 路由

| 当前 Phase | Gate 结果 | 路由 |
|-----------|----------|------|
| Input Governance | readiness = not_ready | **停止**。返回 blocking gaps。建议补数据/补分析/补设计。 |
| Input Governance | readiness = wrong_article_type | **重路由**。建议更换 article type 后重新 triage。 |
| Input Governance | proceed = clarification_stop | **停止**。向用户提出最小阻塞问题。 |
| Architecture Governance | methods_audit = requires_reanalysis | **停止**。告知用户需重新分析。不可由 drafter 修复。 |
| Architecture Governance | methods_audit = methodologically_blocked | **停止**。研究设计缺陷。建议回到研究设计阶段。 |
| Architecture Governance | methods_audit = requires_methods_clarification | **继续**，但标记 methods 段落需作者补充。 |
| Quality Control | claim_audit = blocked | **停止**。fatal overclaims 必须先经 refinement 修复。 |
| Quality Control | evaluator = reject | **停止**。记录 fatal flaws。 |
| Quality Control | evaluator = revise | **路由**到 refinement-controller。 |
| Quality Control | evaluator = stop_no_gain | **停止**。修订无实质改进。 |
| Quality Control | panel methodology reviewer → fatal flaw | 强制 `not_ready`，无论其他 reviewer 评分如何。 |
| Submission Delivery | journal_requirements = not_checked | Package status 不超过 `partial`。 |

### 8.2 Refinement 路由

| 修订模式 | 路由目标 | 是否消耗 revision round |
|---------|---------|----------------------|
| textual_revision | drafter (重写指定段落) | 是 |
| structural_revision | architect → drafter | 是 |
| evidence_relinking | architect (更新 ledger) → drafter | 否（仅 relink，不重写） |
| reporting_completion | drafter (补充缺失条目) | 否（补充 checklist 不算修订轮次） |
| claim_downscaling | drafter → 作者确认 | 是 |
| methods_detailing | drafter | 否（补充方法细节不算修订轮次） |
| journal_retargeting | architect (更新 adapter) → drafter | 是 |
| analysis_required | **外部：用户重新分析** | 不计入（系统不能处理） |
| study_redesign_required | **外部：用户重新设计** | 不计入（系统不能处理） |

**修订轮次上限**：默认 2 轮。超过后标记为 `major_revision_required`，不继续循环。

---

## 9. 研究类型矩阵（v3 扩展 AI/ML 子类型）

（v2 矩阵基础上增加 AI/ML 细分 [NEW v3]）

| 研究类型 | organization_mode | 主要报告规范 |
|---------|-------------------|------------|
| RCT | norm_driven | CONSORT |
| 队列研究 | norm_driven | STROBE |
| 病例对照 | norm_driven | STROBE |
| 诊断准确性 | norm_driven | STARD |
| **AI 临床预测模型** | **norm_driven** | **TRIPOD-AI** |
| **AI 诊断模型** | **norm_driven** | **STARD-AI** |
| **AI 算法/方法创新** | **artifact_driven 或 argument_driven** | **(无专用规范)** |
| **AI 基础模型/通用系统** | **artifact_driven** | **(无专用规范)** |
| **AI 部署/实施研究** | **norm_driven 或 hybrid** | **(无专用规范)** |
| 预测模型（非 AI） | norm_driven | TRIPOD |
| 系统综述/Meta | evidence_synthesis_driven | PRISMA |
| Scoping review | evidence_synthesis_driven | PRISMA-ScR |
| Umbrella review | evidence_synthesis_driven | PRIOR |
| 机制/转化 | argument_driven | (无专用规范) |
| 组学/多组学 | argument_driven | (无专用规范) |
| 因果推断/准实验 | norm_driven | STROBE + 因果推断补充 |
| 定性研究 | argument_driven | COREQ |
| 混合方法 | hybrid | APA JARS-Mixed |
| 卫生经济学 | norm_driven | CHEERS |
| 实施科学 | norm_driven / hybrid | StaRI |
| 调查工具验证 | norm_driven | APA JARS |
| 数据/资源型 | artifact_driven | (无专用规范) |
| 工程/系统 | artifact_driven | (无专用规范) |
| 理论/数学模型 | theory_driven | (无专用规范) |

---

## 10. MVP 定义（v3 新增）

### 10.1 MVP 范围

MVP 不追求完整 15 步流程。目标是：

> 生成一份 evidence-constrained manuscript draft，并附带 claim audit 和 evaluation report。

**MVP 包含 8 个核心模块**：

```
1. research-article-orchestrator       # 编排 + minimal intake summary + backfill
2. article-readiness-triage            # 写作就绪判断
3. article-context-builder             # 输入标准化 + 研究类型分类 + 报告规范选择
4. article-architect                   # 论文架构 + EDP + Evidence Provenance Ledger (Level 1)
5. article-methods-statistics-auditor  # 方法/统计阻断判断
6. article-drafter                     # 正文起草（无段落级挂接）
7. article-claim-auditor               # 主张—证据逐条核查
8. article-evaluator                   # 整体 non-compensatory 评价
```

**MVP 暂缓**：

```
article-literature-grounder     → Phase 2（依赖外部检索能力）
article-review-panel            → Phase 2（依赖多 subagent 并发）
article-frontmatter-drafter     → Phase 2（正文稳定后再做）
article-submission-compositor   → Phase 2（正文稳定后再做）
```

### 10.2 MVP 简化

| 维度 | 完整版 | MVP |
|------|--------|-----|
| Provenance 粒度 | paragraph-level | claim-level |
| 文献定位 | 独立 literature-grounder | 内嵌于 architect（基础文献检索） |
| Panel | 多角色盲审 | 暂缓；evaluator 承担初审角色 |
| Frontmatter | 独立 drafter | orchestrator 内联生成基础版本 |
| Compositor | 独立组装 | orchestrator 输出 draft + evaluation 即交付 |
| Reporting item library | 完整 10+ 规范 | CONSORT + STROBE + PRISMA（3 个最常用） |
| Fast-track backfill | 完整反向构建 | 仅 minimal context brief + inferred claim map |

### 10.3 MVP 入口限制

MVP 只支持：
- **Standard Entry**：完整 8 步
- **Fast-Track: Has Draft**：backfill → claim audit → evaluation
- **Blueprint-Only**：停在 Step 4

暂不支持：Section-Specific、Submission-Only。

---

## 11. 安全降级策略（v3 新增）

当材料不完整或 skill 能力不足时，系统降级而非硬写：

| 场景 | 降级策略 |
|------|---------|
| 用户只提供汇总结果，无原始数据文件 | evidence `verification_status = user_supplied_unverified`；package 不超过 `ready_for_author_check` |
| 用户未提供 protocol/SAP | methods auditor 标记 `conditionally_pass_with_author_verification` |
| 目标期刊 author instructions 无法联网核查 | journal adapter `retrieval_status = not_checked`；package 不超过 `ready_for_author_check` |
| 运行时不支持 subagent delegation | claim auditor 和 evaluator 标记 `independence_status = fallback_degraded`；或延后到独立会话 |
| 文献检索不充分 | literature grounder 标记 `grounding_confidence = low`；覆盖评估标记 `partial` 或 `unclear` |
| 报告规范无对应 item library | checklist mapping 标记 `standard_library_unavailable`；退化为按通用原则报告 |
| 研究类型在分类体系之外 | 标记 `study_type = other`；使用通用 argument_driven 骨架；不做规范驱动的 checklist 映射 |
| Claim downscaling 后主张强度显著降低 | 在 package summary 中明确标注；不影响 contribution statement 的原始措辞（需作者确认） |

**核心降级原则**：宁可标记 `partial` 或 `ready_for_author_check`，也不将未验证输出标记为 `ready_for_author_signoff`。

---

## 12. 实现路线图（v3 修订版）

### Phase 1: MVP 核心（v0.1.0 → v0.4.0）
1. `_shared/` — artifact contracts v3 + CONSORT/STROBE/PRISMA item libraries
2. `research-article-orchestrator/` — 编排 + minimal intake + backfill + workflow state
3. `article-readiness-triage/` — 写作就绪判断
4. `article-context-builder/` — 三步标准化 + 报告规范映射

### Phase 2: 架构与审计（v0.5.0 → v0.7.0）
5. `article-architect/` — 论文架构 + EDP + Evidence Provenance Ledger (Level 1)
6. `article-methods-statistics-auditor/` — 方法/统计阻断判断

### Phase 3: 写作与评估（v0.8.0 → v0.9.0）
7. `article-drafter/` — 按蓝图起草正文
8. `article-claim-auditor/` — 主张—证据逐条核查
9. `article-evaluator/` — non-compensatory 整体评估

**→ MVP 交付：evidence-constrained manuscript draft + claim audit + evaluation report**

### Phase 4: 质量控制扩展（v0.10.0 → v0.12.0）
10. `article-refinement-controller/` — 修订循环 + downscaling
11. `article-literature-grounder/` — 文献定位与检索追溯
12. `article-review-panel/` — 双模式模拟审稿

### Phase 5: 投稿交付（v0.13.0 → v1.0.0）
13. `article-frontmatter-drafter/` — 摘要/标题/Cover Letter
14. `article-submission-compositor/` — 组装 + human sign-off

### Phase 6: 扩展（v1.1.0+）
- Provenance 粒度升级（Level 1 → Level 2）
- 更多 reporting standards item library
- 更多期刊 adapter hard constraint 数据
- 非医学领域专项适配
- 中文期刊适配

---

## 13. v2 → v3 变更总结

| 维度 | v2 | v3 |
|------|-----|-----|
| **版本定位** | 架构扩展 | 收敛压实 |
| **Skill 数量** | 误标 15+1，实际 13+1 | 明确 13+1（14）；不再新增 |
| **前置步骤** | readiness triage 直接对原始输入 | Step 0: Minimal Intake Summary → triage |
| **Fast-Track** | 跳过 Phase 1–2 | backfill mechanism：反向构建最小 artifact |
| **Literature Grounder** | 无检索记录要求 | search_protocol + coverage_assessment |
| **Provenance 粒度** | 段落级（单一级别） | 三级：claim-level (MVP) → paragraph-level → sentence-level |
| **Methods Auditor** | 3 级 audit_status | 5 级（增加 requires_methods_clarification 和 conditionally_pass_with_author_verification） |
| **Package Status** | ready | ready_for_author_signoff（系统最高状态；作者确认后才叫 submission-ready） |
| **Journal Adapter** | 单一 confidence | 三级 verification tier（verified / user_supplied_only / not_checked）|
| **Panel Aggregation** | 无显式规则 | non-compensatory rule：方法学 reviewer 一票否决 |
| **Refinement** | revision_mode 分类 | 增加 revision_allowed gate + 外部 action 路由 |
| **Reporting Checklist** | 依赖无说明 | 明确依赖 _shared/reporting-standards/ item library |
| **路由决策** | 分散在各 skill | 集中路由决策表（Phase Gate 路由 + Refinement 路由） |
| **安全降级** | 未系统定义 | 9 种降级场景 + 统一降级原则 |
| **AI/ML** | 笼统归入 argument_driven | 5 种子类型，各自独立组织方式 |
| **MVP 定义** | 无 | 8 模块 MVP + 暂缓清单 + MVP 入口限制 |
| **Human Sign-off** | checklist 附件 | 最终硬门禁：未确认则 package 不超过 ready_for_author_check |
