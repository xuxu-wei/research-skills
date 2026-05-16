# research-article Skills: Design Document

> **Status**: Draft v0.1.0
> **Author**: Xuxu Wei
> **Date**: 2026-05-16
> **Package**: `research-article/`

---

## 1. 问题定位：为什么需要 Article 系列

当前 skill 体系覆盖了从粗糙研究方向到 proposal 的完整流程：

- `research-idea/`：方向 → idea generation → evaluation → portfolio
- `research-proposal/`：idea → proposal drafting → evaluation → SAP → panel → package
- `research-perspective/`：观点 → argument → drafting → evaluation → compositor

但存在一个关键缺口：**从已有研究数据、结果和研究设计背景信息，到可直接投稿的 manuscript**，没有对应的 skill 包。

`research-proposal/` 解决的是"计划做什么"，而 `research-article/` 解决的是"已经做了，怎么写出来"。两者的起点、逻辑和产出完全不同。

---

## 2. 设计目标

### 2.1 核心定位

> 以已有研究数据、结果、研究设计背景信息为起点，通过结构化规划、分步起草、独立评估和定向优化，交付一份高质量、符合报告规范、可直接投稿的 manuscript。

### 2.2 关键区分

| 维度 | research-proposal | research-article |
|------|-------------------|------------------|
| 起点 | idea / funding call | 已有数据、结果、研究设计 |
| 核心问题 | 我们计划做什么 | 我们做了什么，发现了什么 |
| 产出 | proposal / SAP | manuscript + cover letter + 审稿预案 |
| Methods | 计划使用的方法 | 已经执行的方法 |
| Results | 预期结果 | 实际结果 |
| Discussion | 预期意义 | 实际意义和边界 |

### 2.3 设计原则

1. **通用 → 类型特定 → 期刊特定** 三层递进，不把某一种文章类型的写法当作普遍规律
2. **主张—证据—推理—边界** 作为底层论证结构，而非"讲故事模板"
3. **Evidence Display Plan** 替代 Figure Plan，适配所有研究类型
4. **研究类型感知** 的 Results 组织方式（规范驱动型 vs 论证驱动型）
5. **报告规范** 作为基础约束，而非事后检查清单
6. **隔离评估**：drafter 和 evaluator 必须为独立子 agent

---

## 3. 顶层模型

所有研究论文共有的写作逻辑：

```
Question → Design → Evidence → Inference → Boundary → Meaning
```

即：

1. **Question**：研究问题是否重要、明确？
2. **Design**：研究设计是否能回答该问题？
3. **Evidence**：数据是否充分、可靠、透明？
4. **Inference**：从结果到结论的推理是否成立？
5. **Boundary**：结论的适用边界在哪里？
6. **Meaning**：对知识、实践或未来研究的意义是什么？

Article 系列的每个 skill 都在为这个模型服务。

---

## 4. 写作顺序（通用版）

本文定义的写作顺序是 Article 系列 skill 编排的基础：

1. **Contribution Statement** — 本文的知识贡献是什么？
2. **Study Type & Reporting Standard** — 研究类型 + 对应报告规范
3. **Core Question & Main Answer** — 研究问题 + 主要答案
4. **Claim–Evidence Matrix** — 每个主张的证据、推理基础、潜在质疑、防御策略
5. **Evidence Display Plan** — 每个证据的最佳呈现形式（图/表/文字/补充）
6. **Results Skeleton** — 按研究类型、终点或机制链条组织的结果结构
7. **Methods & Statistical Analysis** — 研究设计、数据、变量、模型、稳健性
8. **Introduction** — 问题重要性 → 已知 → 空白 → 本文贡献
9. **Discussion** — 主要发现 → 文献比较 → 意义 → 优势局限 → 结论
10. **Abstract / Key Points** — 压缩全文核心信息
11. **Title** — 准确表达设计或核心发现
12. **Cover Letter** — 说明研究重要性和期刊适配性
13. **Reviewer Risk Matrix** — 预判审稿攻击点并提前防御

---

## 5. Skill 包架构

### 5.1 目录总览

```
research-article/
  research-article-orchestrator/     # 工作流入口和编排器
  article-context-builder/           # 输入标准化 → Article Context Brief
  article-architect/                 # 论文架构设计（Step 1–6）
  article-drafter/                   # 全文起草（Step 7–9）
  article-evaluator/                 # 独立质量评估
  article-refinement-controller/     # 定向修订控制
  article-review-panel/              # 模拟审稿 Panel
  article-compositor/                # 终稿合规 + 投稿材料（Step 10–13）
  _shared/                           # 跨 skill 契约和共享规则
```

### 5.2 Skill 职责一览

| Skill | 角色 | 执行方式 | 核心产出 |
|-------|------|---------|---------|
| research-article-orchestrator | 编排器 | inline | workflow state, routing decisions |
| article-context-builder | 构建 | inline | Article Context Brief |
| article-architect | 构建 | inline | Article Blueprint |
| article-drafter | 构建 | inline | Manuscript Draft |
| article-evaluator | 评估 | isolated subagent | Evaluation Report |
| article-refinement-controller | 控制 | inline | Revision Plan + Revised Draft |
| article-review-panel | 评估 | isolated subagents | Panel Report |
| article-compositor | 构建 | inline | Submission Package |
| _shared | 参考 | reference-only | artifact contracts, handoff rules |

### 5.3 隔离规则

- **article-drafter** 写入或修订 manuscript；**article-evaluator** 独立评价；**article-refinement-controller** 管理修订循环。三个角色不得合并。
- **article-architect** 设计蓝图；**article-drafter** 按蓝图起草。架构师不评价自己的设计，起草者不评价自己的稿件。
- **article-review-panel** 的每个 reviewer 必须是隔离子 agent，盲审模式下不得接收 context brief、evaluation report 或 unresolved issues。
- **article-compositor** 只组装已有产物，不得重写、修补、重新评分或隐藏未解决问题。

---

## 6. 核心 Artifact 定义

### 6.1 Article Context Brief

```yaml
article_context_brief:
  schema_version: "research-article.v1"
  artifact_id: "article-context-001"
  source_skill: "article-context-builder"
  study_design:
    type: ""                     # RCT | cohort | case-control | cross-sectional | diagnostic | prediction_model | systematic_review | meta_analysis | qualitative | mixed_methods | mechanistic | omics | AI_ML | health_policy | engineering | theoretical | data_resource | other
    subtype: ""                  # e.g., cluster RCT, nested case-control, scoping review
    phase: ""                    # 如适用：phase I/II/III, discovery/validation
  reporting_standard: ""         # CONSORT | STROBE | STARD | TRIPOD | PRISMA | ARRIVE | COREQ | SQUIRE | CARE | APA_JARS | other | not_applicable
  target_journal:
    name: ""
    article_type: ""             # original_article | brief_report | research_letter | other
    figure_table_limits: ""
    abstract_structure: ""       # structured | unstructured
    reporting_requirements: []
  research_question:
    primary: ""
    secondary: []
    pico_or_framework: ""        # PICO | PECO | SPIDER | SPICE | not_applicable
  study_object:
    population_or_sample: ""
    setting: ""
    time_period: ""
    sample_size: ""
  data_summary:
    data_sources: []
    data_types: []
    data_completeness: ""        # complete | partially_complete | with_missing | unknown
    known_limitations: []
  results_summary:
    primary_findings: []
    secondary_findings: []
    negative_or_null_findings: []
    unexpected_findings: []
    robustness_checks_done: []
  methods_summary:
    study_design_details: ""
    variable_definitions: ""
    statistical_approach: ""
    pre_registration: ""         # registered | not_registered | not_applicable
    protocol_or_sap: ""          # path or not_available
  user_goal: ""
  user_constraints:
    word_limit: ""
    figure_limit: ""
    table_limit: ""
    reference_limit: ""
    supplementary_limits: ""
    formatting_requirements: []
  assumptions: []
  uncertainties: []
  proceed_status: proceed | proceed_with_assumptions | clarification_stop
```

### 6.2 Article Blueprint

```yaml
article_blueprint:
  schema_version: "research-article.v1"
  artifact_id: "blueprint-001"
  source_skill: "article-architect"
  contribution:
    type: ""                     # mechanism_discovery | intervention_evidence | practice_refutation | prediction_diagnostic_tool | causal_evidence | evidence_synthesis | classification_framework | data_resource | method_platform | policy_decision_support | other
    statement: ""                # 一句话贡献陈述
  study_type_confirmation:
    type: ""
    subtype: ""
    reporting_standard: ""
    reporting_checklist: ""
  core_question_and_answer:
    research_question: ""
    main_answer: ""
    answer_strength: ""          # definitive | strong | moderate | suggestive | exploratory
  claim_evidence_matrix:
    - claim_id: "C001"
      claim: ""
      evidence: ""
      inference_basis: ""
      potential_challenges: []
      defense_strategy: ""
      display_location: ""       # main_text | supplementary | appendix
  evidence_display_plan:
    - display_id: "D001"
      supported_claims: []       # claim_ids
      module: ""                 # study_object | descriptive_foundation | main_evidence | inference_support | heterogeneity_boundary | mechanism_explanation | reproducibility_transparency
      content: ""
      best_form: ""              # table | figure | flowchart | forest_plot | survival_curve | model_diagram | text_only | supplementary_table | supplementary_figure | appendix | code_repository
      placement: ""              # main_text | supplementary
      rationale: ""
  results_skeleton:
    organization_mode: ""        # norm_driven | argument_driven
    sections: []
  journal_adapter:
    target_journal: ""
    style_notes: ""
    special_requirements: []
  reviewer_risk_preview: []      # 初步识别的审稿风险
```

### 6.3 Manuscript Draft

```yaml
manuscript_draft:
  schema_version: "research-article.v1"
  draft_id: "draft-v001"
  source_skill: "article-drafter"
  version: 1
  blueprint_ref: ""
  sections:
    methods:
      status: drafted | revised | final
      word_count: 0
    results:
      status: drafted | revised | final
      word_count: 0
      organization_mode: ""     # norm_driven | argument_driven
    introduction:
      status: drafted | revised | final
      word_count: 0
    discussion:
      status: drafted | revised | final
      word_count: 0
  figures: []
  tables: []
  references_count: 0
  reporting_checklist_status: pending | attached | not_applicable
  unresolved_issues: []
  drafting_assumptions: []
```

### 6.4 Article Evaluation Report

```yaml
article_evaluation:
  schema_version: "research-article.v1"
  evaluation_id: "eval-001"
  source_skill: "article-evaluator"
  draft_version: 1
  independence_status: valid | invalid
  dimension_scores:
    scientific_validity: 0       # 研究设计、方法、分析是否合理
    evidence_claim_alignment: 0  # 证据是否支持主张
    clarity_and_structure: 0     # 结构、逻辑、可读性
    completeness: 0              # 是否满足报告规范和期刊要求
    argument_boundary: 0         # 结论边界是否清晰、克制
    contribution_significance: 0 # 知识贡献是否明确、有意义
  overall_score_simple_average: 0
  hard_gate_status: pass | fail
  failed_gates: []
  fatal_flaws: []
  major_strengths: []
  major_weaknesses: []
  revision_priorities:
    - priority: ""
      category: evidence | clarity | substance | other
      location: ""
      description: ""
      suggested_fix: ""
  reviewer_defensibility_concerns: []
  decision: accept | revise | reject | stop_no_gain
  decision_rationale: ""
```

### 6.5 Panel Report

```yaml
panel_report:
  schema_version: "research-article.v1"
  panel_id: "panel-001"
  panel_mode: blind_mock_review | context_aware_internal_review
  panel_tier: lightweight | standard | full
  reviewers: []
  aggregated_recommendation: strong_support | support_with_minor_revision | support_after_major_revision | revise_and_resubmit | not_ready | reject_or_redesign
  consensus_summary: ""
  dissenting_opinions: []
  must_fix_items: []
  suggestion_items: []
```

### 6.6 Submission Package

```yaml
submission_package:
  schema_version: "research-article.v1"
  package_id: "package-001"
  status: ready | minor_revision_pending | major_revision_required | blocked | partial
  contents:
    manuscript: ""
    abstract: ""
    key_points: ""
    title: ""
    cover_letter: ""
    reviewer_risk_matrix: ""
    reporting_checklist: ""
    supplementary_materials_index: ""
    figure_files: []
    table_files: []
  unresolved_items: []
  human_review_notes: []
```

---

## 7. Workflow 设计

### 7.1 入口模式

#### Standard Entry（完整流程）

用户提供研究数据、结果和设计背景信息。走完整 pipeline：

```
Context Brief → Blueprint → Draft → Evaluation → Refinement → Review Panel → Compositor
```

#### Fast-Track Entry（快速通道）

用户提供已有 manuscript 草稿。

- **仅需评估**：创建 minimal workflow state，直接路由到 evaluation
- **草稿 + 评估报告**：路由到 refinement-controller 或 review panel
- **完整材料**：路由到 compositor

跳过的步骤不回溯，但在 workflow state 和最终 package 中标记 `evaluation_scope_limitation`。

#### Blueprint-Only Entry（仅架构）

用户希望在起草前先审查论文架构。停在 blueprint 阶段，等待用户确认后再进入 drafting。

#### Section-Specific Entry（特定章节）

用户只需起草或修订特定章节（如只需 Results 或 Discussion）。orchestrator 路由到 drafter 的对应 section 模式。

### 7.2 标准流程详细步骤

#### Step 1: Build Context Brief

调用 `article-context-builder`。

**输入**：用户提供的原始材料（数据摘要、结果概要、研究设计描述、目标期刊、约束条件等）

**输出**：标准化的 Article Context Brief

**关键任务**：
- 识别研究类型（RCT / 观察性 / 诊断 / 预测模型 / 机制 / AI / 系统综述 / 定性 / ...）
- 匹配报告规范（CONSORT / STROBE / STARD / TRIPOD / PRISMA / ARRIVE / COREQ / APA JARS / ...）
- 提取 PICO/PECO/SPIDER 框架
- 识别数据缺口、不确定性和假设
- 当输入信息不足以确定研究类型或报告规范时，不猜测，标记 `clarification_stop`

**Orchestrator 状态更新**：
- 设置 `context_brief_path`
- 更新 `study_type`、`reporting_standard`、`target_journal`
- 添加 `unresolved_issues`

#### Step 2: Design Blueprint

调用 `article-architect`。

**输入**：Article Context Brief

**输出**：Article Blueprint（包含 Contribution Statement、Study Type Confirmation、Core Q&A、Claim-Evidence Matrix、Evidence Display Plan、Results Skeleton）

**关键任务**：
1. 确定贡献类型（机制发现 / 干预证据 / 预测工具 / 证据综合 / 数据资源 / 方法平台 / ...）
2. 撰写一句话核心问题和主要答案
3. 构建 Claim-Evidence Matrix：
   - 列出每个核心主张
   - 为每个主张匹配证据、推理基础、潜在质疑和防御策略
4. 设计 Evidence Display Plan：
   - 从主张出发，而非从"有什么图"出发
   - 判断每个证据的最优呈现形式（表格 / 图 / 流程图 / 森林图 / 生存曲线 / 模型图 / 文字 / 补充材料）
   - 区分主文展示 vs 补充材料展示
5. 确定 Results 组织方式：
   - **norm_driven**：RCT、观察性研究、诊断研究、预测模型、系统综述等 → 按人群、终点、预设分析组织
   - **argument_driven**：机制研究、转化研究、组学发现等 → 按主张递进组织
6. 生成 Results Skeleton（各 section 的小标题和关键内容要点）
7. 初步识别审稿风险

**Orchestrator 状态更新**：
- 设置 `blueprint_path`
- 更新 `contribution_type`、`results_organization_mode`
- 添加 `reviewer_risk_preview`

#### Step 3: Draft Manuscript

调用 `article-drafter`。

**输入**：Article Blueprint + Article Context Brief

**输出**：Manuscript Draft（Methods + Results + Introduction + Discussion）

**起草顺序**：
1. **Methods**：先写 Methods，因为 Methods 决定 Results 的可信度
2. **Results**：按 Blueprint 中的 Results Skeleton 组织；根据 `organization_mode` 选择规范驱动或论证驱动写法
3. **Introduction**：四段式（大问题 → 已知 → 空白 → 本文贡献）
4. **Discussion**：五段式（主要发现 → 文献比较 → 意义 → 优势局限 → 结论）

**起草规则**：
- Methods 必须覆盖：研究设计、数据来源、对象、纳排标准、变量定义、主要/次要终点、样本量、缺失值处理、统计模型、敏感性分析、伦理审批
- Results 的 Discussion 部分不放解释性文本（规范驱动型尤其如此）
- Discussion 中的结论不得超出证据边界；观察性研究不得写为因果陈述
- 匹配目标期刊的报告规范要求
- 如果 Blueprint 的 journal_adapter 有特殊要求，按期刊风格调整

**Orchestrator 状态更新**：
- 设置 `draft_path`、`draft_version`
- 设置 `draft_status: drafted`

#### Step 4: Independent Evaluation

使用 `delegate_task` 调用隔离的 `article-evaluator` 子 agent。

**输入（给 evaluator）**：
- draft file path + version
- context brief
- blueprint
- 用户目标和约束
- 目标期刊要求
- previous evaluation report（如为 re-evaluation）

**不传给 evaluator 的内容**：drafter 的隐含推理、内部讨论、草稿修订历史

**六维评分**：
1. **Scientific Validity**：研究设计、方法和分析是否合理
2. **Evidence-Claim Alignment**：证据是否充分支持每个主张
3. **Clarity & Structure**：结构逻辑和可读性
4. **Completeness**：是否满足报告规范和期刊要求
5. **Argument Boundary**：结论边界是否清晰、措辞是否克制
6. **Contribution Significance**：知识贡献是否明确

**Hard Gates**（任一不通过 → `fail`）：
- Research question 是否可回答？
- 核心变量/终点是否定义清楚？
- Methods 是否足以支撑主要结论？
- 是否存在致命方法学缺陷？
- 报告规范要求的关键条目是否缺失？
- 是否存在明显的 evidence-claim mismatch（主张远超证据）？
- Genre Fit：是否存在以下体裁违规——
  - （a）将观察性研究结果写成因果陈述
  - （b）Results 中以叙事化临床场景替代客观报告
  - （c）Discussion 中以教学式修辞问句替代论证
  - （d）残留的审稿回应标记或版本注释
  - （e）过度故事化，损害科学可信度

**Decision**：
- `accept`：可进入 review panel 或 compositor
- `revise`：存在可修复问题，进入 refinement
- `reject`：存在不可修复的 fatal flaw
- `stop_no_gain`：仅 re-evaluation；修订后无实质改进

**Revision Priority 分类**：
- `[evidence]`：主张缺乏证据/引用/数据支撑
- `[clarity]`：表述不清
- `[substance]`：实质性缺陷（方法、逻辑、范围）
- `[other]`：无法归入以上三类

**Orchestrator 状态更新**：
- 设置 `evaluation_report_path`
- 设置 `draft_status: evaluated`
- 复制 revision priorities 和 unresolved issues

#### Step 5: Revision Loop

当 evaluation 返回 `revise` 时，调用 `article-refinement-controller`。

**默认上限**：2 轮。每轮包括：
1. 定向修订计划（基于 evaluator 的 revision priorities）
2. 修订后的 manuscript + response-to-reviewer 文件
3. 版本 lineage 和 delta report
4. 隔离子 agent 独立 re-evaluation

**Thesis Integrity 检查**（仅 re-evaluation 时）：
- 5：核心主张比上一版更清晰且更集中
- 3：清晰度与上一版持平
- 1：被更多 caveat/hedging 层覆盖，比上一版更模糊
- 若 thesis integrity ≤ 2，decision 必须为 `revise`，修订方向为**删减**

**Orchestrator 状态更新**：
- 递增 `revision_round`
- 追加 `revision_history`
- 更新 `draft_path`、`draft_version`、`evaluation_report_path`

#### Step 6: Review Panel

在 evaluation 通过后，或用户明确请求 mock review 时使用。

**默认模式**：`blind_mock_review`

**Panel Tier**：
- `lightweight_panel`（3 人）：domain expert + methodology/statistics reviewer + submission-guard reviewer
- `standard_panel`（5 人）
- `full_panel`（7 人）

**盲审规则**（`blind_mock_review` 模式）：
- 单个 reviewer 只接收：manuscript file + user goal + target journal + reviewer role/scope
- 不传给 reviewer：context brief、evaluation report、revision delta、unresolved issues、blueprint
- 这些材料由 orchestrator 保留，仅供聚合 context

**Reviewer 角色设计**（默认）：
1. **Domain Expert**：领域知识、创新性、贡献意义
2. **Methodology/Statistics Reviewer**：设计、方法、分析、报告规范
3. **Evidence-Claim Alignment Reviewer**：每个主张是否有足够证据支撑，结论边界是否合理
4. **Clarity & Structure Reviewer**：逻辑、结构、可读性、图文质量
5. **Submission-Guard Reviewer**：期刊适配性、格式合规、投稿材料完整性

**Panel Decision 路由**：
- `strong_support` → compositor
- `support_with_minor_revision` → compositor（标记 minor revision pending）
- `support_after_major_revision` → revision loop
- `revise_and_resubmit` → revision loop + re-evaluation gate
- `not_ready` → 返回 drafting 或 blueprint
- `reject_or_redesign` → 停止，建议回到研究设计阶段

#### Step 7: Final Compositor

调用 `article-compositor`。

**输入**：final draft + evaluation + panel report + blueprint + context brief

**输出**：Submission Package

**关键任务**：
1. 生成/优化 Abstract（按目标期刊的结构化格式）
2. 生成/优化 Key Points（Question / Findings / Meaning）
3. 生成/优化 Title
4. 撰写 Cover Letter
5. 构建 Reviewer Risk Matrix
6. 附加报告规范 checklist
7. 整理投稿材料清单
8. 标注未解决问题和人工审阅建议

**Reviewer Risk Matrix** 结构：

| 审稿人可能质疑 | 风险等级 | 文章中防御位置 | 防御策略 | 是否需要额外分析 |
|--------------|---------|--------------|---------|----------------|
| ... | high/medium/low | section/paragraph | ... | yes/no |

**Compositor 约束**：
- 只组装已有产物，不得重写、修补或重新评分
- 发现需要修订的内容时，标记为 `human_review_notes`，不静默修改
- 如果实质性缺陷仍需 drafting 修复，路由回 refinement-controller
- Package 状态必须明确：ready / minor_revision_pending / major_revision_required / blocked / partial

---

## 8. 跨 Skill 契约

### 8.1 Handoff 校验

每个 skill 边界的最小校验（定义在 `_shared/references/handoff-validation.md`）：

| Handoff | 必须条件 |
|---------|---------|
| Context Builder → Architect | context brief 存在；study_design.type 非空；proceed_status ≠ clarification_stop |
| Architect → Drafter | blueprint 存在；claim_evidence_matrix 至少 1 条；results_skeleton 非空 |
| Drafter → Evaluator | draft 文件可读；所有 sections status = drafted 或 revised |
| Evaluator → Refinement Controller | evaluation report 存在；decision = revise；revision_priorities 非空 |
| Refinement Controller → Evaluator (re-eval) | 新 draft version；delta report；response-to-reviewer |
| Evaluator → Compositor | decision = accept；hard_gate_status = pass |
| Review Panel → Compositor | panel report 存在；recommendation 为 strong_support 或 support_with_minor_revision |

### 8.2 文件命名和目录结构

```
<workspace>/research-article-projects/<project-slug>/
  input/
    raw-materials.md              # 用户原始输入
  state/
    workflow-state.yaml           # workflow 状态机
    artifact-index.md             # 人类可读的产物清单
  context/
    article-context-brief.md      # 标准化 context brief
  blueprint/
    article-blueprint.md          # 论文架构
  drafts/
    manuscript-v001.md
    manuscript-v002.md
    ...
  evaluations/
    evaluation-v001.md
    evaluation-v002.md
  revisions/
    round-001/
      revision-plan.md
      response-to-reviewer.md
      delta-report.md
  panel/
    panel-report.md
    reviewer-briefs/
  package/
    manuscript-final.md
    abstract.md
    cover-letter.md
    reviewer-risk-matrix.md
    submission-checklist.md
    reporting-checklist.md
```

### 8.3 版本命名

- Draft：`manuscript-vNNN.md`（v001, v002, ...）
- 实质性修改始终创建新版本，不覆盖旧版本
- `state/workflow-state.yaml` 记录当前版本
- `state/artifact-index.md` 记录人类可读的产物清单

---

## 9. 研究类型适配矩阵

Article 系列的核心创新之一是**研究类型感知**。不同研究类型在 Blueprint、Drafter 和 Evaluator 中走不同的逻辑分支。

### 9.1 Results 组织方式

| 研究类型 | organization_mode | 典型 Results 结构 |
|---------|-------------------|------------------|
| RCT | norm_driven | Participants → Baseline → Primary Outcome → Secondary Outcomes → Subgroup → Safety → Sensitivity |
| 队列/病例对照 | norm_driven | Study Population → Baseline by Exposure → Primary Association → Secondary → Subgroup → Sensitivity |
| 诊断研究 | norm_driven | Participant Flow → Index Test vs Reference → Diagnostic Performance → Subgroup → False Pos/Neg |
| 预测模型 | norm_driven | Population → Candidate Predictors → Model Development → Internal Validation → External Validation → Calibration → Clinical Utility |
| 系统综述/Meta | norm_driven | Study Selection → Characteristics → Risk of Bias → Primary Synthesis → Secondary → Heterogeneity → Subgroup → Sensitivity → GRADE |
| 机制/转化研究 | argument_driven | Phenomenon → Characterization → Perturbation → Functional Validation → In Vivo → Clinical Relevance → Integrated Model |
| 组学/多组学 | argument_driven | Discovery → Validation → Characterization → Clinical Association → Mechanistic Link → Translation Potential |
| AI/ML 模型 | argument_driven | Task Definition → Data → Model Architecture → Benchmark → Ablation → Error Analysis → Generalization → Clinical/Applied Utility |
| 定性研究 | argument_driven | Setting & Participants → Thematic Framework → Main Themes → Deviant Cases → Integration → Theoretical Model |
| 工程/系统 | argument_driven | System Architecture → Key Components → Performance Metrics → Baseline Comparison → Stress Test → Failure Mode → Cost/Benefit |
| 数据/资源型 | argument_driven | Data Source → Construction → Structure → Quality Control → Coverage → Use Case → Access |

### 9.2 Evidence Display Plan 适配

不同研究类型的 EDP 模块权重不同（定义在 `article-architect/references/evidence-display-plan-guide.md`）：

| 模块 | RCT | 观察性 | 诊断 | 预测模型 | 系统综述 | 机制 | AI/ML |
|------|-----|--------|------|---------|---------|------|------|
| Study Object | 高 | 高 | 高 | 高 | 高 | 中 | 中 |
| Descriptive Foundation | 高 | 高 | 中 | 高 | 高 | 中 | 中 |
| Main Evidence | 高 | 高 | 高 | 高 | 高 | 高 | 高 |
| Inference Support | 中 | 高 | 中 | 高 | 中 | 高 | 高 |
| Heterogeneity/Boundary | 高 | 高 | 高 | 高 | 高 | 中 | 高 |
| Mechanism/Explanation | 低 | 中 | 低 | 低 | 低 | 高 | 中 |
| Reproducibility/Transparency | 中 | 中 | 中 | 高 | 高 | 中 | 高 |

### 9.3 报告规范映射

`article-context-builder` 根据研究类型自动映射报告规范：

| 研究类型 | 默认报告规范 | 来源 |
|---------|------------|------|
| RCT | CONSORT | EQUATOR Network |
| 观察性研究 | STROBE | EQUATOR Network |
| 诊断准确性 | STARD | EQUATOR Network |
| 预测模型 | TRIPOD | EQUATOR Network |
| 系统综述/Meta | PRISMA | EQUATOR Network |
| 动物实验 | ARRIVE | EQUATOR Network |
| 定性研究 | COREQ | EQUATOR Network |
| 质量改进 | SQUIRE | EQUATOR Network |
| 病例报告 | CARE | EQUATOR Network |
| 经济学评估 | CHEERS | EQUATOR Network |
| AI/ML 预测模型 | TRIPOD-AI | EQUATOR Network |
| 社会科学定量 | APA JARS | APA |
| 社会科学定性 | APA JARS-Qual | APA |
| 混合方法 | APA JARS-Mixed | APA |

---

## 10. 期刊适配层

Article 系列的第二个核心创新是**三层结构**：普遍规律 → 研究类型规范 → 期刊风格。

### 10.1 期刊风格分类

| 期刊群 | 典型期刊 | 核心偏好 | 对写作的影响 |
|--------|---------|---------|------------|
| 临床医学顶刊 | NEJM, Lancet, JAMA, BMJ | 临床问题重要性、设计强度、实践改变潜力 | 强调临床意义；Results 严格规范驱动；Introduction 简洁有力 |
| 综合科学顶刊 | Nature, Science | 概念突破、跨领域意义、新范式 | 强调新颖性和广泛兴趣；论证驱动型 Results |
| 高影响力子刊 | Nature Medicine, Nature Communications, STTT | 机制完整性 + 转化潜力 | 机制解释要求高；证据链条要求完整 |
| Cell 系列 | Cell, Cell Medicine, Cell Reports Medicine | 机制深度、概念创新 | 机制链条和实验验证要求高 |
| 方法学/数据期刊 | Nature Methods, Scientific Data | 方法创新、数据质量、可复用性 | 透明性、基准比较、可复现性权重高 |
| 创新导向期刊 | The Innovation | 创新性、跨学科、未来应用价值 | 前瞻性和应用潜力 |

### 10.2 期刊适配器

`article-architect` 中的 `journal_adapter` 字段根据目标期刊调整：

- Abstract 结构（structured vs unstructured；不同期刊的 structured abstract 格式不同）
- Figure/Table 数量和引用格式限制
- Results 小标题风格（描述性 vs 结论性）
- Discussion 的长度和结构期望
- Cover Letter 的侧重点

---

## 11. 与现有 Skill 包的关系

### 11.1 上游依赖

- `research-idea/`：research-article 的上游。Article workflow 假定研究已经完成（数据已收集、分析已完成），不处理 idea 阶段的问题。
- `research-proposal/`：平行包。Proposal 是"计划"，Article 是"报告已完成的研究"。
- `research/research-opportunity-mapper`：当 drafter 需要补充文献证据或在 Discussion 中比较文献时，可由 mapper 检索。
- `research/methodology-statistics-preflight`：当 context builder 或 evaluator 发现方法学问题时，可调 preflight 进行评估。

### 11.2 下游入口

- Article workflow 的产出是 submission-ready manuscript package，直接面向人工投稿。

### 11.3 共享依赖

Article 系列不直接依赖 idea 或 proposal 的 shared contracts。Artifact 命名空间独立（`research-article.v1`）。

---

## 12. 实现路线图

### Phase 1: 核心基础设施（v0.1.0 → v0.3.0）

1. `_shared/` — artifact contracts、handoff validation、workflow manifest schema
2. `research-article-orchestrator/` — 编排器，workflow state 管理
3. `article-context-builder/` — 输入标准化

### Phase 2: 架构与起草（v0.4.0 → v0.6.0）

4. `article-architect/` — 论文架构设计
5. `article-drafter/` — 全文起草

### Phase 3: 评估与优化（v0.7.0 → v0.8.0）

6. `article-evaluator/` — 独立评估
7. `article-refinement-controller/` — 修订控制

### Phase 4: 审稿与交付（v0.9.0 → v1.0.0）

8. `article-review-panel/` — 模拟审稿
9. `article-compositor/` — 终稿合规和投稿材料

### Phase 5: 扩展（v1.1.0+）

- 更多研究类型的 Results 模板完善
- 更多期刊适配器
- 特定学科（工程、CS、社会科学、人文）的 Evidence Display Plan 模板
- 与 reference manager 集成
- 预注册/SAP 交叉校验

---

## 13. 风险与开放问题

### 13.1 已识别风险

1. **研究类型边界模糊**：某些研究跨多个类型（如 RCT + 机制子研究）。处理：取主导研究类型，子类型在 blueprint 的 `subtype` 中标注。
2. **报告规范过载**：某些期刊在通用规范上有额外要求。处理：journal_adapter 层处理额外要求，不修改基础模板。
3. **drafter 质量依赖 blueprint 质量**：blueprint 不完整时，drafter 可能产生次优输出。处理：drafter 必须校验 blueprint 完整性，发现问题时反馈给 orchestrator。
4. **隔离评估在单 agent 环境下的 fallback**：与 idea/proposal 系列一样，evaluator 依赖 `delegate_task`。处理：遵循 `_shared/references/runtime-delegation.md` 的 fallback 机制。

### 13.2 开放问题

1. Figure/Table 的实际生成：Article 系列负责规划展示方案（EDP），但实际的图表绘制可能需要外部工具。是否集成 `office-toolkit` 或 `nano-pdf` 进行图表生成？
2. 参考文献管理：是否需要在 compositor 中集成引用格式检查和 DOI 验证？
3. 中文期刊适配：当前设计以英文期刊为主，中文期刊（如《中华医学杂志》《中国科学》等）的结构和语言要求不同，需要单独适配。
4. LaTeX vs Word：不同学科和期刊的投稿格式差异大（LaTeX vs Word vs 在线投稿系统）。Compositor 是否需要支持多种输出格式？

---

## 14. 附录：与用户原始方法论文档的映射

| 用户方法论文档章节 | 对应的 Article Skill |
|------------------|---------------------|
| 一、先区分三层结构 | `article-architect` — study type confirmation |
| 二、重新定义写作顺序 | `research-article-orchestrator` — workflow steps |
| 三、Evidence Display Plan | `article-architect` — evidence_display_plan |
| 四、Results 的两种写法 | `article-architect` — results_skeleton + `article-drafter` |
| 五、Claims 不是故事 | `article-architect` — claim_evidence_matrix |
| 六、通用原则 | 贯穿所有 skill |
| 七、顶刊核心模型 | `article-architect` — contribution + blueprint |
| 八、通用写作顺序改进版 | `research-article-orchestrator` — workflow |
| 九、Evidence Display Plan 构建 | `article-architect` — evidence_display_plan |
| 十、按主张类型设计展示 | `article-architect` — claim evidence matrix + EDP |
| 十一、去哪里找 EDP 线索 | `article-context-builder` + `article-architect` references |
| 十二、通用工作表 | `article-architect` — blueprint template |
| 十三、最短操作流程 | `research-article-orchestrator` — entry paths |
