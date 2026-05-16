# research-article Skills: Design Document v2

> **Status**: Draft v0.2.0
> **Author**: Xuxu Wei
> **Date**: 2026-05-16
> **Previous**: v0.1.0 (`research-article-skills-design.md`)
> **Review basis**: `roadmap/review-v1.md`
>
> **v2 核心变更**：将系统定位从"论文写作器"升级为"证据约束下的投稿级 manuscript 构建与审查系统"。新增 readiness triage、literature grounder、claim auditor、frontmatter drafter 四个 skill；拆分 compositor；升级 evaluation 体系为 non-compensatory gates；引入 Evidence Provenance Ledger；扩展研究类型矩阵和 Results 组织模式。

---

## 1. 定位修正

### 1.1 原定位（v1）

> 以已有研究数据、结果、研究设计背景信息为起点，通过结构化规划、分步起草、独立评估和定向优化，交付一份高质量、符合报告规范、可直接投稿的 manuscript。

### 1.2 修正后定位（v2）

> 以已有研究数据、结果、研究设计背景信息为起点，通过**输入治理 → 架构治理 → 证据约束起草 → 多层质量审查 → 投稿组装**五个阶段，交付一份 **submission-ready manuscript package**。所有未验证数据、缺失材料、作者需确认事项和不可由写作修复的方法学问题均明确标注。

### 1.3 核心理念修正

| 维度 | v1 | v2 |
|------|-----|-----|
| 系统本质 | 论文写作器 | 证据约束下的 manuscript 构建与审查系统 |
| 写作位置 | 流程中心 | 输入治理和架构治理之后 |
| 质量保证 | 评估 + 修订循环 | 多层 gate（readiness → methods audit → claim audit → evaluation → panel） |
| 最终产出 | 可直接投稿的 manuscript | submission-ready package + human sign-off checklist |
| 证据追踪 | Claim-Evidence Matrix | Evidence Provenance Ledger（段落级挂接） |

---

## 2. 顶层模型（不变）

```
Question → Design → Evidence → Inference → Boundary → Meaning
```

### 2.1 三层结构（不变，增强）

```
Layer 1: 普遍论证规律（所有研究共有）
Layer 2: 研究类型与报告规范（按研究设计区分）
Layer 3: 期刊约束系统（hard constraints + soft preferences + strategic fit）
```

Layer 3 从 v1 的"期刊风格分类"升级为**三类约束系统**（见第 9 节）。

---

## 3. 修订后的 Skill 架构

### 3.1 完整 Skill 清单（16 个：15 功能 + 1 shared）

```
research-article/
  research-article-orchestrator/          # 工作流编排器
  article-readiness-triage/               # [NEW] 写作就绪判断
  article-context-builder/                # 输入标准化（含研究类型识别 + 报告规范选择）
  article-literature-grounder/            # [NEW] 文献定位与引用支撑
  article-architect/                      # 论文架构（含 EDP）
  article-methods-statistics-auditor/     # [NEW] 方法与统计预审
  article-drafter/                        # 正文起草
  article-claim-auditor/                  # [NEW] 主张—证据逐条核查
  article-evaluator/                      # 独立质量评估
  article-refinement-controller/          # 定向修订控制
  article-review-panel/                   # 模拟审稿 Panel
  article-frontmatter-drafter/            # [NEW] 摘要/标题/Key Points/Cover Letter
  article-submission-compositor/          # [RENAMED] 只组装，不重写
  _shared/                                # 跨 skill 契约
```

### 3.2 Skill 职责与执行方式

| Skill | 角色 | 执行方式 | 核心产出 | 阶段 |
|-------|------|---------|---------|------|
| research-article-orchestrator | 编排器 | inline | workflow state, routing | — |
| article-readiness-triage | 门禁 | isolated subagent | Readiness Report | 输入治理 |
| article-context-builder | 构建 | inline | Context Brief | 输入治理 |
| article-literature-grounder | 构建 | inline | Literature Grounding Report | 输入治理 |
| article-architect | 构建 | inline | Article Blueprint (含 EDP) | 架构治理 |
| article-methods-statistics-auditor | 审计 | isolated subagent | Methods Audit Report | 架构治理 |
| article-drafter | 构建 | inline | Manuscript Draft | 写作 |
| article-claim-auditor | 审计 | isolated subagent | Claim Audit Report | 质量控制 |
| article-evaluator | 评估 | isolated subagent | Evaluation Report | 质量控制 |
| article-refinement-controller | 控制 | inline | Revision Plan + Revised Draft | 质量控制 |
| article-review-panel | 评估 | isolated subagents | Panel Report | 质量控制 |
| article-frontmatter-drafter | 构建 | inline | Abstract/Title/Key Points/Cover Letter | 投稿交付 |
| article-submission-compositor | 组装 | inline | Submission Package | 投稿交付 |
| _shared | 参考 | reference-only | artifact contracts, handoff rules | — |

### 3.3 隔离规则（v1 基础 + v2 增强）

- **article-drafter** 写入或修订 manuscript；**article-evaluator** 独立评价；**article-refinement-controller** 管理修订循环。三个角色不得合并。
- **article-architect** 设计蓝图；**article-drafter** 按蓝图起草。架构师不评价自己的设计，起草者不评价自己的稿件。
- **article-readiness-triage** 判断是否可进入写作。若 triage 发现阻断性缺陷，orchestrator 不得跳过 triage 直接进入 drafting。
- **article-methods-statistics-auditor** 在 drafting 前审计方法和统计。若存在不可由写作修复的缺陷，标记 `methodologically_blocked`，不得继续 drafting。
- **article-claim-auditor** 在 drafting 后逐条核查主张—证据对应关系。发现 `absent` 或 `overstated` 的主张时，进入 claim downscaling 或 evidence relinking。
- **article-review-panel** 的每个 reviewer 必须是隔离子 agent。盲审模式下的输入边界见第 12 节。
- **article-submission-compositor** 只组装已有产物，不得重写、修补、重新评分或隐藏未解决问题。

---

## 4. 修订后的标准流程（15 步，5 阶段）

```
Phase 1: 输入治理 (Input Governance)
  1. Article Readiness Triage
  2. Context Brief
  3. Reporting Standard & Journal Requirement Selection
  4. Literature Grounding

Phase 2: 架构治理 (Architecture Governance)
  5. Article Blueprint
  6. Claim–Evidence Matrix (含 Evidence Provenance Ledger)
  7. Evidence Display Plan
  8. Methods / Statistics Audit

Phase 3: 写作 (Writing)
  9. Manuscript Drafting

Phase 4: 质量控制 (Quality Control)
  10. Claim-Level Audit
  11. Independent Evaluation
  12. Targeted Refinement
  13. Mock Review Panel

Phase 5: 投稿交付 (Submission Delivery)
  14. Frontmatter Drafting
  15. Submission Compositor
```

**关键设计原则**：写作（Step 9）被推后到输入治理和架构治理完成之后。研究是否可写、主张是否有证据支撑、报告规范是否匹配、方法是否可审计——这些问题必须在动笔之前解决。

---

## 5. 入口模式（v1 基础 + v2 调整）

| 模式 | 触发条件 | 路由 |
|------|---------|------|
| **Standard** | 用户提供数据/结果/设计信息 | 完整 15 步 |
| **Fast-Track: Has Draft** | 用户已有 manuscript 草稿 | 跳过 Phase 1–2，从 Step 10 (Claim Audit) 或 Step 11 (Evaluation) 进入 |
| **Fast-Track: Draft + Eval** | 用户有草稿和评估 | 从 Step 12 (Refinement) 或 Step 13 (Panel) 进入 |
| **Blueprint-Only** | 用户想在起草前审查架构 | 停在 Step 8，等待用户确认 |
| **Section-Specific** | 只需特定章节 | 路由到 drafter 的 section 模式 |
| **Submission-Only** | 用户有终稿，仅需投稿材料 | 从 Step 14 (Frontmatter) 进入 |

跳过的步骤不回溯，但在 workflow state 和 final package 中标记 `scope_limitation`。

---

## 6. 新增/重大修改的 Skill 详解

### 6.1 article-readiness-triage [NEW]

**职责**：在进入写作前判断研究是否具备"可写成 manuscript"的最低条件。

这不等同于 context building。Context builder 负责标准化输入；readiness triage 负责判断"能不能写"。

**核心判断**：

1. 材料是否足够进入写作？
2. 适合什么 article type（original article / brief report / research letter / data descriptor / methods article / case report / review / other）？
3. 是否存在阻断性缺陷（缺少主要结果、研究设计不清、方法不可审计等）？
4. 是否需要回到分析阶段、补实验、补数据、补文献？
5. 用户目标是否现实（target journal / article type 是否与手头研究匹配）？

**输出**：`ArticleReadinessReport`

```yaml
article_readiness_report:
  schema_version: "research-article.v2"
  artifact_id: "readiness-001"
  source_skill: "article-readiness-triage"
  readiness_status: ready | conditionally_ready | not_ready | wrong_article_type
  recommended_article_type: original_article | brief_report | research_letter | methods_article | data_descriptor | case_report | review | other
  minimum_inputs_present:
    research_question: true | false
    study_design: true | false
    primary_results: true | false
    methods_details: true | false
    ethics_info: true | false
    figures_tables: true | false
    references: true | false
  blocking_gaps:
    - gap: ""
      why_blocking: ""
      required_action: ""           # data_analysis | experiment | literature_review | methods_documentation | ethics_approval | user_clarification
  nonblocking_gaps:
    - gap: ""
      mitigation: ""
  target_journal_realism:
    stated_target: ""
    realism_assessment: realistic | ambitious_but_possible | mismatch
    mismatch_details: ""
  recommended_route: blueprint | methods_preflight | data_analysis | literature_review | stop
```

**执行方式**：隔离子 agent。Triage 结果不受用户期望影响，不得为推进流程而放宽判断。

**Stop 条件**：若 `readiness_status = not_ready` 且 `blocking_gaps` 中有 `required_action = data_analysis | experiment`，orchestrator 必须停止，告知用户先完成研究本身。

---

### 6.2 article-context-builder [MODIFIED]

**变更**：内部明确三步处理，报告规范映射不再写死为一对一。

**三步内部流程**：

1. **Normalize**：将用户原始输入标准化为统一字段
2. **Classify**：识别研究类型、文章类型、报告规范
3. **Gate**：判断是否可继续（`proceed | proceed_with_assumptions | clarification_stop`）

**报告规范映射规则**（从 v1 的硬编码表升级）：

- 允许**多规范并用**（如 RCT + 成本效益分析 → CONSORT + CHEERS）
- **extension 优先**（如 cluster RCT → CONSORT extension，而非基础 CONSORT）
- **期刊特定要求覆盖默认规范**（目标期刊明确要求某规范时，以期刊为准）
- **研究设计混合时的主规范 + 辅助规范**（如 RCT 嵌套机制子研究）
- **没有合适规范时标记** `no_exact_guideline_found`，不强行映射
- 报告规范的检索依据 EQUATOR Network 数据库，支持按 study type、clinical area 和 report section 查找

**输出**：`ArticleContextBrief`（结构基本不变，增加 `reporting_standard_selection` 字段）

```yaml
reporting_standard_selection:
  primary_standard: ""
  primary_source: "EQUATOR"
  extensions: []
  supplementary_standards: []
  journal_override: ""              # 目标期刊明确要求的规范
  mapping_confidence: high | medium | low
  no_exact_match: true | false
  rationale: ""
```

---

### 6.3 article-literature-grounder [NEW]

**职责**：为 manuscript 提供文献定位和引用支撑。不替代 `research-opportunity-mapper`（后者用于 idea generation 和 opportunity discovery），而是聚焦于 manuscript 写作所需的文献 grounding。

**为什么需要独立 skill**：
- Introduction 的 gap 必须是真实的文献空白，而非泛化陈述；
- Discussion 的 comparison 需要具体、可引用的文献；
- novelty claim 需要文献支撑，否则审稿人容易否定；
- overclaim control 需要文献边界。

**输出**：`LiteratureGroundingReport`

```yaml
literature_grounding_report:
  schema_version: "research-article.v2"
  artifact_id: "lit-ground-001"
  source_skill: "article-literature-grounder"
  key_background_claims:
    - claim: ""
      references: []
      manuscript_location: "Introduction"
  novelty_position:
    prior_work_summary: ""
    what_is_new: ""
    what_is_not_new: ""
    novelty_confidence: strong | moderate | weak
  competing_evidence:
    - finding: ""
      relation: supports | contradicts | complicates
      references: []
  discussion_comparison_points:
    - manuscript_finding: ""
      comparable_studies: []
      interpretation: ""
  citation_risk:
    missing_seminal_work: []
    overreliance_on_low_quality_sources: []
    outdated_references: []
  grounding_confidence: high | medium | low
```

**使用方式**：
- `article-architect` 在构建 novelty claim 和 Introduction gap 时引用此报告
- `article-drafter` 在写 Introduction 和 Discussion 时引用此报告
- `article-claim-auditor` 在核查 claim 时交叉验证文献支撑

---

### 6.4 article-architect [MODIFIED]

**变更**：
1. Evidence Display Plan 保持在 architect 内部，但增加了从 Evidence Provenance Ledger 到 EDP 的溯源
2. Results 组织模式从 2 种扩展为 6 种
3. Reviewer Risk Matrix 初版在此阶段生成

**Results Organization Mode 扩展**：

| 模式 | 适用场景 | Results 逻辑 |
|------|---------|-------------|
| `norm_driven` | RCT、观察性、诊断、预测模型、系统综述、卫生经济学 | 按规范、对象、终点、预设分析报告 |
| `argument_driven` | 机制、转化、组学发现 | 按主张递进 |
| `hybrid` | 临床 + 机制子研究、RCT + biomarker、AI + 临床验证 | 主研究按规范，子研究按论证 |
| `artifact_driven` | 数据资源、软件、工具、方法平台 | 构建 → 验证 → 用例 → 边界 |
| `theory_driven` | 理论、数学模型、人文学术、法律/政策分析 | 概念 → 命题 → 证明/解释 → 边界 |
| `evidence_synthesis_driven` | 系统综述、scoping review、umbrella review、realist review、定性证据综合 | 文献流 → 证据图谱 → 质量 → 综合结论 |

**Reviewer Risk Matrix — Blueprint 阶段初版**：

在 blueprint 阶段预判审稿风险，指导 EDP 设计：

```yaml
reviewer_risk_matrix:
  stage: blueprint
  risks:
    - risk_id: "R001"
      description: ""
      category: design | methods | evidence | novelty | interpretation | reporting | fit
      severity: high | medium | low
      preemptive_display: ""        # 在 EDP 中哪个 display 提前防御
      mitigation: ""
```

**输出**：`ArticleBlueprint`（v2 增强版）

```yaml
article_blueprint:
  schema_version: "research-article.v2"
  artifact_id: "blueprint-001"
  source_skill: "article-architect"
  # --- v1 字段保留 ---
  contribution: { ... }
  study_type_confirmation: { ... }
  core_question_and_answer: { ... }
  claim_evidence_matrix: { ... }
  evidence_display_plan: { ... }
  results_skeleton:
    organization_mode: norm_driven | argument_driven | hybrid | artifact_driven | theory_driven | evidence_synthesis_driven
    sections: []
  journal_adapter: { ... }
  # --- v2 新增 ---
  evidence_provenance_ledger: []    # 从 C-E Matrix 派生，见 7.2
  reviewer_risk_preview: []         # Blueprint 阶段初版
```

---

### 6.5 article-methods-statistics-auditor [NEW]

**职责**：在 drafting 之前审计研究方法和统计分析的可辩护性。不是替代 `methodology-statistics-preflight`（后者用于 idea 阶段的可行性评估），而是针对"已完成的研究"——Methods 写的是已执行的方案，而非计划。

**核心审计点**：

1. 研究设计是否匹配研究问题？
2. 主要终点/结局定义是否清晰、预设？
3. 样本量是否充分（或事后功效是否报告）？
4. 统计方法与数据特征是否匹配？
5. 缺失值处理是否合理？
6. 混杂控制是否充分？
7. 敏感性分析是否覆盖主要威胁？
8. 多重比较是否处理？
9. Methods 是否包含报告规范要求的所有条目？
10. 是否存在不可由写作修复的方法学缺陷？

**输出**：`MethodsAuditReport`

```yaml
methods_audit_report:
  schema_version: "research-article.v2"
  artifact_id: "methods-audit-001"
  source_skill: "article-methods-statistics-auditor"
  audit_status: pass | conditionally_pass | methodologically_blocked
  design_question_alignment:
    assessment: strong | adequate | weak | mismatch
    issues: []
  primary_endpoint:
    clarity: clear | partially_clear | unclear
    pre_specification: registered | stated_in_protocol | stated_in_methods_only | unclear
  sample_size:
    basis: a_priori_power | convenience | pragmatically_determined | unclear
    post_hoc_power_reported: true | false
    adequacy_for_primary: adequate | borderline | inadequate | unclear
  statistical_approach:
    primary_model_appropriate: true | false | unclear
    assumptions_checked: true | false | not_reported
    missing_data_handling: adequate | inadequate | not_reported
    confounding_control: adequate | partially_adequate | inadequate
    sensitivity_analyses_adequate: true | false | partial
    multiplicity_handled: true | false | not_applicable
  reporting_items_coverage:
    standard: ""
    critical_missing_items: []
    non_critical_missing_items: []
  unfixable_by_writing:
    - issue: ""
      why_unfixable: ""             # requires_reanalysis | requires_additional_data | design_flaw
  recommendation: proceed_to_drafting | fix_methods_text | requires_reanalysis | requires_data_collection | stop
```

**执行方式**：隔离子 agent。若 `audit_status = methodologically_blocked`，orchestrator 必须停止，告知用户方法学问题不可由写作修复。

**关键区分**：
- `fix_methods_text`：Methods 描述不完整 → drafter 可修复
- `requires_reanalysis`：分析方法有问题 → 需用户回到分析阶段
- `requires_additional_data`：数据不足以支撑结论 → 需用户补数据
- `design_flaw`：研究设计本身不能回答研究问题 → 阻断

---

### 6.6 article-drafter [MODIFIED]

**变更**：
1. 起草顺序不变（Methods → Results → Introduction → Discussion），但增加 literature grounding 和 methods audit 的约束输入
2. 段落级输出挂接 `claim_id` 和 `evidence_id`
3. 增加 reporting checklist item 的逐条覆盖

**新增输入**：
- `LiteratureGroundingReport`（Introduction 和 Discussion 的文献约束）
- `MethodsAuditReport`（Methods 的审计建议）

**段落级输出**（见 7.3 Manuscript Draft v2）

---

### 6.7 article-claim-auditor [NEW]

**职责**：在 drafting 完成后，逐条核查 manuscript 中每个核心主张是否有证据支撑、推断是否成立、措辞是否恰当。这是 evaluator 之前的一道精细化质量门。

**为什么需要独立于 evaluator**：
- Evaluator 做整体六维评价，容易漏掉个别 claim 的 overclaim
- Claim auditor 逐条审计，能发现"整体不错但某个主张过度"的问题
- 两个评估视角互补：evaluator 看森林，claim auditor 看树木

**审计维度**：

```yaml
claim_audit_report:
  schema_version: "research-article.v2"
  artifact_id: "claim-audit-001"
  source_skill: "article-claim-auditor"
  claim_evaluations:
    - claim_id: "C001"
      claim_text: ""
      manuscript_location: ""       # section + paragraph_id
      evidence_support: strong | moderate | weak | absent
      evidence_ids: []
      inference_validity: valid | overstated | invalid
      wording_status: appropriate | overclaimed | underclaimed
      boundary_clarity: clear | vague | missing
      required_action: retain | strengthen | downscale | remove | move_to_discussion | move_to_supplementary
      action_rationale: ""
  overall_assessment:
    total_claims: 0
    strong_support: 0
    moderate_support: 0
    weak_support: 0
    absent_evidence: 0
    overclaimed: 0
    requires_downscaling: 0
    fatal_overclaims: []            # 主张远超证据，不修复不可投稿
  recommendation: pass | downscale_and_proceed | revise_and_reaudit | blocked
```

**执行方式**：隔离子 agent。不得由 drafter 自行审计。

**与 evaluator 的关系**：
- Claim auditor 先跑，evaluator 后跑
- Claim auditor 发现的问题若为 `fatal_overclaims`，进入 refinement 修复后再 evaluation
- Claim auditor 通过但 evaluator 不通过 → 问题可能在结构、清晰度、完整性，而非证据链

---

### 6.8 article-evaluator [MODIFIED]

**变更**：评分体系从 simple average 升级为 non-compensatory gate 体系；增加 claim-level evaluation 引用；hard gates 分层。

#### 六维评分（调整后）

| 维度 | 说明 | 补偿性 |
|------|------|--------|
| Scientific Validity | 研究设计、方法和分析是否合理 | **Non-compensatory** |
| Evidence-Claim Alignment | 证据是否充分支持每个主张（引用 claim auditor 结果） | **Non-compensatory** |
| Reporting Completeness | 是否满足报告规范和期刊要求 | Compensatory |
| Journal Fit | 与目标期刊的 scope、格式、新颖性阈值是否匹配 | Compensatory |
| Clarity & Structure | 结构逻辑和可读性 | Compensatory |
| Contribution Significance | 知识贡献是否明确 | Compensatory |

#### 三层 Hard Gates

```yaml
gate_failures:
  fatal_scientific: []
    # 研究问题不可回答
    # 核心变量/终点定义不清
    # 主要结论没有数据支撑
    # 研究设计不能支持主要推断
    # 统计分析存在不可修复缺陷
  reporting: []
    # checklist 缺关键项
    # Methods 描述不完整
    # 图表说明不清
    # 缺少伦理/数据可用性/代码可用性声明
  genre_rhetoric: []
    # 观察性研究语言为因果推断
    # Results 中叙事化临床场景替代客观报告
    # Discussion 中教学式修辞问句替代论证
    # 过度宣传化（claim远超evidence边界）
    # 口吻不符合目标期刊
```

#### 总体评估（替代 simple average）

```yaml
overall_assessment:
  readiness_level: submission_ready | minor_revision | major_revision | not_ready | methodologically_blocked
  score_profile:
    scientific_validity: 0
    evidence_claim_alignment: 0
    reporting_completeness: 0
    journal_fit: 0
    clarity: 0
    contribution: 0
  noncompensatory_gates:
    - gate: "methods_support_primary_claim"
      status: pass | fail
      consequence: "blocked"
    - gate: "primary_evidence_exists"
      status: pass | fail
      consequence: "blocked"
    - gate: "no_fatal_overclaim"
      status: pass | fail
      consequence: "blocked"
  decision: accept | revise | reject | stop_no_gain
```

**Decision 路由**：
- `accept` → review panel 或 compositor（需 claim auditor 也通过）
- `revise` → refinement-controller
- `reject` → 停止，记录 fatal flaws
- `stop_no_gain` → 仅 re-evaluation；修订无实质改进

---

### 6.9 article-refinement-controller [MODIFIED]

**变更**：增加修订模式分类、claim downscaling 机制。

#### 修订模式分类

```yaml
revision_mode:
  primary: textual_revision | structural_revision | evidence_relinking | reporting_completion | claim_downscaling | methods_detailing | journal_retargeting
  secondary: []
```

| 修订模式 | 触发条件 | 处理方式 |
|---------|---------|---------|
| `textual_revision` | clarity / rhetoric gate 失败 | drafter 重写 |
| `structural_revision` | 结构/逻辑问题 | architect 调整蓝图 → drafter 重写 |
| `evidence_relinking` | claim auditor 发现证据链断裂 | 回到 evidence provenance ledger |
| `reporting_completion` | reporting gate 失败 | drafter 补充缺失条目 |
| `claim_downscaling` | overclaim / overstated | drafter 降低主张强度 |
| `methods_detailing` | Methods 描述不完整 | drafter 补充方法细节 |
| `journal_retargeting` | journal fit 差 | 更新 journal adapter → 调整格式/风格 |

**不可由写作修复的模式**（refinement-controller 必须拒绝处理）：
- `analysis_required`：需要重新分析数据
- `study_redesign_required`：研究设计本身有问题

这两种情况标记为 `methodologically_blocked`，告知用户回到研究阶段。

#### Claim Downscaling 机制

```yaml
claim_revision_action:
  claim_id: "C001"
  original_wording: "X causes Y"
  issue: "observational study, causal language not justified"
  action: downscale
  revised_wording: "X was associated with Y after adjustment for..."
  strength_change: strong_causal → moderate_association
```

Downscaling 的类型：
- `retain`：维持原主张
- `strengthen`：加强（需额外证据）
- `downscale`：降低强度（因果 → 关联；预测 → 初步判别；确定 → 可能）
- `remove`：删除主张
- `move_to_discussion`：从 Results 移到 Discussion 作为推测
- `move_to_supplementary`：从主文移到补充材料

---

### 6.10 article-review-panel [MODIFIED]

**变更**：明确两种 panel 模式下不同 reviewer 的输入边界；增加 methodology reviewer 的 diagnostic 模式。

#### Panel 模式

| 模式 | 用途 | Reviewer 输入 |
|------|------|--------------|
| `blind_external_simulation` | 模拟投稿后外审 | manuscript + target journal + reviewer role/scope |
| `internal_diagnostic_review` | 投稿前深度修稿 | 按 reviewer 角色差异化输入 |

#### Internal Diagnostic Review 下的差异化输入

| Reviewer 角色 | 输入 |
|--------------|------|
| Domain Expert | manuscript + target journal + scope |
| Methodology/Statistics | manuscript + **context brief + protocol/SAP + tables** |
| Evidence-Claim | manuscript + **claim audit report + evidence provenance ledger** |
| Clarity & Structure | manuscript only |
| Submission-Guard | manuscript + **journal author instructions** |

**Methodology reviewer 的特殊性**：如果 manuscript 的 Methods 写得不完整，blind simulation 下 method reviewer 只能指出"不清楚"。但在 internal diagnostic 模式下，method reviewer 有权查看 protocol/SAP，判断"原始研究设计是否真的有问题"，而非仅判断"稿件是否写得清楚"。

#### Panel 规模

| Tier | 人数 | Reviewer 组成 |
|------|------|-------------|
| `lightweight` | 3 | Domain Expert + Methodology/Statistics + Submission-Guard |
| `standard` | 5 | Domain Expert + Methodology/Statistics + Evidence-Claim + Clarity/Structure + Submission-Guard |
| `full` | 7 | 以上 5 人 + 2 位条件性 reviewer（如 practicing-clinician + outlet-fit editor） |

---

### 6.11 article-frontmatter-drafter [NEW]

**职责**：起草和优化论文的"前置信息"——摘要、Key Points、标题、Running title、Highlights、Graphical abstract text、Cover letter 初稿。

**为什么独立于 submission-compositor**：
- Frontmatter 是**实质性写作**（需要压缩全文、提炼核心信息、匹配期刊格式）
- Compositor 是**组装和核查**（不重写任何文本）
- 两者混在一个 skill 里导致职责冲突

**输入约束**：
- Article Blueprint（核心 Q&A、contribution statement）
- Final Manuscript Draft
- Evaluation Report（尤其是 evidence-claim alignment 和 contribution 评价）
- Panel Report（如有）
- Journal Adapter（abstract format、word limit）

**起草项**：

| 起草项 | 约束来源 | 可否重写 |
|--------|---------|---------|
| Abstract | journal adapter abstract format | 是，受 Blueprint 和 Evaluation 约束 |
| Key Points | journal requirement | 是 |
| Title | journal style | 是，建议 2-3 个备选 |
| Running title | character limit | 是 |
| Highlights | journal requirement | 是 |
| Graphical abstract text | journal requirement | 是 |
| Cover letter 初稿 | journal adapter + contribution statement | 是 |

**禁止行为**：
- 不得修改 manuscript 正文
- 不得改变 contribution statement 的核心主张
- 不得在 abstract 中引入 manuscript 中没有的结果或主张
- 不得在 cover letter 中做出 manuscript 不支持的 novelty claim

---

### 6.12 article-submission-compositor [RENAMED, NARROWED]

**职责**：只组装最终投稿包，不进行任何实质性写作。

**具体任务**：
1. 汇编所有已完成的 artifacts（manuscript + frontmatter + figures/tables + supplementary）
2. 格式核对（word limit、figure/table count、reference format、abstract structure）
3. 附上 reporting checklist（item-level mapping）
4. 生成 submission checklist（所有期刊要求项的逐条确认）
5. 生成 Reviewer Risk Matrix 终版（整合 blueprint + evaluation + panel 阶段的风险）
6. 标记所有未解决问题（`unresolved_items`）
7. 生成 `submission_readiness_summary`
8. 输出 human sign-off checklist

**Human Sign-off Checklist**（v2 新增）：

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

**禁止行为**：
- 不得重写、修补或润色任何文本
- 不得重新评分或修改 evaluation/panel 结论
- 不得隐藏或删除 unresolved issues
- 发现需要修订的问题时，标记为 `human_review_notes`，路由回 refinement-controller 或 frontmatter-drafter

**Submission Package 状态**：

```yaml
submission_package:
  status: ready | minor_revision_pending | major_revision_required | blocked | partial
  unresolved_items: []
  human_review_notes: []
```

---

## 7. 增强的 Artifact Contracts

### 7.1 Evidence Provenance Ledger [NEW]

这是 v2 最重要的 artifact 增强。每个进入 manuscript 的证据都应有可追踪来源。

```yaml
evidence_provenance_ledger:
  - evidence_id: "E001"
    evidence_type: primary_data | secondary_data | experiment | statistical_result | literature_reference | user_assertion | assumption
    source_location: ""              # 数据文件、分析脚本或文献位置
    source_file: ""
    source_table_or_figure: ""
    numeric_values:
      estimate: ""
      ci_lower: ""
      ci_upper: ""
      p_value: ""
      sample_size: ""
      model: ""
    supports_claims: ["C001"]
    appears_in:
      manuscript_section: "Results"
      paragraph_id: "R-P03"
      display_id: "D001"             # 对应的 table/figure
    verification_status: verified | user_supplied_unverified | inferred | missing
    risk_level: low | medium | high
    notes: ""
```

**使用场景**：
- `article-architect`：从 C-E Matrix 生成 ledger
- `article-drafter`：每个结果段落挂接 evidence_id
- `article-claim-auditor`：逐条验证 evidence 是否支撑 claim
- `article-evaluator`：评估 evidence-claim alignment
- `article-submission-compositor`：检查是否有 `verification_status = missing` 的条目

### 7.2 Manuscript Draft v2（段落级挂接）

```yaml
manuscript_draft:
  schema_version: "research-article.v2"
  draft_id: "manuscript-v001"
  source_skill: "article-drafter"
  version: 1
  blueprint_ref: ""
  sections:
    title_page:
      content: ""
      status: drafted | revised | final
    abstract:
      content: ""
      status: pending | drafted | revised | final
      word_count: 0
    introduction:
      content: ""
      word_count: 0
      claim_ids: []
      paragraph_ids: []
    methods:
      content: ""
      word_count: 0
      reporting_items_covered: []     # 覆盖的报告规范条目 ID
    results:
      content: ""
      word_count: 0
      display_ids: []                 # 引用的 table/figure ID
      claim_ids: []
      evidence_ids: []
    discussion:
      content: ""
      word_count: 0
      claim_ids: []
  paragraphs:
    - paragraph_id: "I-P01"           # I=Introduction, M=Methods, R=Results, D=Discussion
      section: "Introduction"
      text: ""
      supported_by:
        claims: ["C001"]
        evidence: []
        references: []
    - paragraph_id: "R-P03"
      section: "Results"
      text: ""
      supported_by:
        claims: ["C002"]
        evidence: ["E001", "E002"]
        display_items: ["D001"]
  figures: []
  tables: []
  display_items:                      # 统一的图/表 metadata（见 7.3）
    - display_id: "D001"
      type: table | figure | flow_diagram | forest_plot | model_diagram | supplementary_table | supplementary_figure
      title: ""
      legend_or_caption: ""
      supported_claims: ["C002"]
      evidence_ids: ["E001"]
      source_data: ""
      placement: main | supplementary
      required_by_reporting_guideline: true | false
      journal_limit_impact: ""
      status: planned | drafted | final | missing
  references:
    entries: []
  reporting_checklist_mapping:        # 见 7.4
    standard: ""
    items: []
  unresolved_issues: []
  drafting_assumptions: []
```

### 7.3 Reporting Checklist — Item-Level Mapping（升级）

从 v1 的单一 status 字段升级为逐条映射：

```yaml
reporting_checklist_mapping:
  standard: "STROBE"
  version: "2007"
  items:
    - item_id: "STROBE-01"
      requirement: "Title and abstract"
      manuscript_location: "Title; Abstract"
      status: satisfied | partial | missing | not_applicable
      notes: ""
    - item_id: "STROBE-02"
      requirement: "Background/rationale"
      manuscript_location: "Introduction P1-P2"
      status: satisfied
      notes: ""
    - item_id: "STROBE-12"
      requirement: "Statistical methods"
      manuscript_location: "Methods: Statistical Analysis"
      status: partial
      notes: "missing: handling of missing data"
```

**使用方式**：
- `article-drafter`：在起草 Methods 和 Results 时逐条覆盖
- `article-evaluator`：在 reporting gate 中检查 completeness
- `article-submission-compositor`：在终稿中附上完整 mapping

### 7.4 Journal Adapter v2（约束系统）

从风格描述升级为三类约束系统：

```yaml
journal_adapter:
  target_journal: ""
  source_checked_date: ""             # 上次核实日期
  source_documents:
    - type: author_instructions
      location: ""                    # URL or file path
      retrieval_status: verified | user_supplied | not_checked
  hard_constraints:                   # 必须满足
    article_types: []
    word_limit: 0
    abstract_format: ""               # structured_250 | structured_300 | unstructured_150 | ...
    abstract_subheadings: []
    figure_limit: 0
    table_limit: 0
    reference_limit: 0
    reporting_checklist_required: true | false
    trial_registration_required: true | false
    data_availability_statement_required: true | false
    code_availability_statement_required: true | false
    ethics_statement_required: true | false
    conflict_of_interest_required: true | false
    author_contribution_required: true | false
    supplementary_material_policy: ""
  soft_preferences:                   # 影响写作风格
    results_subheading_style: descriptive | declarative | mixed
    discussion_sections: []
    cover_letter_focus: clinical_impact | conceptual_advance | methodological_rigor | policy_implication
    values_transparency: true | false
    values_reproducibility: true | false
  strategic_fit:                      # 投稿策略
    scope_fit: high | moderate | low
    novelty_threshold: exceptional | high | moderate | incremental
    article_type_fit: high | moderate | low
    audience_fit: high | moderate | low
    likely_desk_rejection_risks: []
  confidence: high | medium | low     # 以上信息的可信度
```

### 7.5 Reviewer Risk Matrix — 三阶段版本

```yaml
reviewer_risk_matrix:
  stage: blueprint | post_evaluation | final_submission
  risks:
    - risk_id: ""
      description: ""
      category: design | methods | evidence | novelty | interpretation | reporting | fit
      severity: high | medium | low
      manuscript_defense_location: "" # section / paragraph_id / display_id
      defense_strategy: ""
      requires_additional_analysis: true | false
      status: addressed | partially_addressed | unaddressed | accepted_limitation
```

三个阶段：
1. **Blueprint 阶段**：预判风险 → 影响 EDP 设计
2. **Post-Evaluation 阶段**：evaluator 识别的 reviewer defensibility concerns → 影响 refinement
3. **Final Submission 阶段**：整合所有阶段风险 → 提交给作者作为审稿预案

---

## 8. 扩展的研究类型矩阵

（v1 基础 + v2 新增）

| 研究类型 | organization_mode | 典型 EDP | 主要报告规范 |
|---------|-------------------|---------|------------|
| RCT | norm_driven | flowchart, baseline table, primary endpoint, forest plot, KM curve, AE table | CONSORT |
| 队列研究 | norm_driven | selection flow, baseline by exposure, adjusted association, survival curve, sensitivity | STROBE |
| 病例对照 | norm_driven | selection flow, baseline, adjusted OR, sensitivity | STROBE |
| 诊断准确性 | norm_driven | participant flow, index vs reference, ROC, sensitivity/specificity, decision curve | STARD |
| 预测模型 | norm_driven | population, predictors, discrimination, calibration, DCA, external validation | TRIPOD |
| 系统综述/Meta | evidence_synthesis_driven | PRISMA flow, study characteristics, forest plot, heterogeneity, funnel plot, GRADE | PRISMA |
| Scoping review | evidence_synthesis_driven | search flow, evidence map, theme table | PRISMA-ScR |
| Umbrella review | evidence_synthesis_driven | review characteristics, overlap matrix, certainty summary | PRIOR |
| Realist review | theory_driven / synthesis | context-mechanism-outcome matrix, programme theory | RAMESES |
| 机制/转化 | argument_driven | phenotype → omics → perturbation → rescue → in vivo → clinical validation | (无专用规范) |
| 组学/多组学 | argument_driven | discovery → validation → characterization → clinical association → mechanism | (无专用规范) |
| AI/ML 预测模型 | norm_driven（如临床预测）/ argument_driven（如基础算法） | data flow, benchmark table, ablation, calibration, error analysis, generalization | TRIPOD-AI |
| 因果推断/准实验 | norm_driven | DAG, event study, balance diagnostics, placebo, robustness | STROBE + 因果推断补充 |
| 定性研究 | argument_driven | setting, participants, themes, deviant cases, theoretical model | COREQ |
| 定性证据综合 | evidence_synthesis_driven | study selection, themes, confidence in evidence | ENTREQ |
| 混合方法 | hybrid | integration matrix, joint display, convergence/divergence | APA JARS-Mixed |
| 卫生经济学 | norm_driven | cost table, ICER, sensitivity, acceptability curve | CHEERS |
| 实施科学 | norm_driven / hybrid | setting, strategy, adoption, fidelity, outcome | StaRI |
| 调查工具验证 | norm_driven | factor structure, reliability, validity, invariance | APA JARS |
| 心理测量 | norm_driven | item analysis, CFA/EFA, reliability, validity | APA JARS |
| 数据/资源型 | artifact_driven | source flow, structure, quality control, coverage, use case | (无专用规范) |
| 工程/系统 | artifact_driven | architecture, components, performance, baseline comparison, failure mode | (无专用规范) |
| 理论/数学模型 | theory_driven | assumptions, propositions, derivation, special cases, boundary | (无专用规范) |
| 历史/人文学术 | theory_driven | source corpus, timeline, case evidence, counterargument | (无专用规范) |
| 法律/政策分析 | argument_driven | doctrine/policy framework, case table, comparative matrix | (无专用规范) |
| 动物实验 | argument_driven | species, experimental groups, outcomes, reproducibility | ARRIVE |

---

## 9. 工作流状态管理

### 9.1 Workflow State Schema v2

```yaml
workflow_state:
  schema_version: "research-article.v2"
  project_slug: ""
  entry_mode: standard | fast_track_has_draft | fast_track_draft_eval | blueprint_only | section_specific | submission_only
  user_goal: ""
  target_journal: ""
  current_phase: input_governance | architecture_governance | writing | quality_control | submission_delivery
  current_step: 0
  phase_gates:
    input_governance: not_started | in_progress | passed | blocked
    architecture_governance: not_started | in_progress | passed | blocked
    writing: not_started | in_progress | passed | blocked
    quality_control: not_started | in_progress | passed | blocked
    submission_delivery: not_started | in_progress | passed | blocked
  artifacts:
    readiness_report_path: ""
    context_brief_path: ""
    literature_grounding_path: ""
    blueprint_path: ""
    methods_audit_path: ""
    draft_path: ""
    draft_version: 0
    claim_audit_path: ""
    evaluation_report_path: ""
    panel_report_path: ""
    frontmatter_path: ""
    package_path: ""
  revision:
    round: 0
    max_rounds: 2
    history: []
  unresolved_issues: []
  scope_limitations: []
  human_signoff: []
  workflow_status: in_progress | completed | blocked | stopped_by_user
```

### 9.2 项目目录结构

```
<workspace>/research-article-projects/<project-slug>/
  input/
    raw-materials.md
  state/
    workflow-state.yaml
    artifact-index.md
  readiness/
    article-readiness-report.md
  context/
    article-context-brief.md
  literature/
    literature-grounding-report.md
  blueprint/
    article-blueprint.md
  audit/
    methods-audit-report.md
  drafts/
    manuscript-v001.md
    manuscript-v002.md
  claim-audit/
    claim-audit-report-v001.md
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
  frontmatter/
    abstract.md
    cover-letter.md
  package/
    manuscript-final.md
    reporting-checklist-mapping.md
    reviewer-risk-matrix.md
    submission-checklist.md
    human-signoff-checklist.md
    submission-readiness-summary.md
```

---

## 10. 跨 Skill Handoff 校验

| Handoff | 必须条件 |
|---------|---------|
| Readiness Triage → Context Builder | `readiness_status ∈ {ready, conditionally_ready}` |
| Context Builder → Literature Grounder | `proceed_status ∈ {proceed, proceed_with_assumptions}` |
| Literature Grounder → Architect | `grounding_confidence ∈ {high, medium}` |
| Architect → Methods Auditor | blueprint 完整；`results_skeleton` 非空 |
| Methods Auditor → Drafter | `audit_status ∈ {pass, conditionally_pass}`；若 `methodologically_blocked`，停止 |
| Drafter → Claim Auditor | draft 可读；所有 sections status ∈ {drafted, revised} |
| Claim Auditor → Evaluator | `recommendation ≠ blocked`；若 `fatal_overclaims` 非空，先 refinement |
| Evaluator → Refinement Controller | `decision = revise`；`revision_priorities` 非空 |
| Refinement Controller → Evaluator (re-eval) | 新 draft version；delta report；response-to-reviewer |
| Evaluator → Review Panel | `decision = accept`；`readiness_level ∈ {submission_ready, minor_revision}` |
| Review Panel → Frontmatter Drafter | `recommendation ∈ {strong_support, support_with_minor_revision}` |
| Frontmatter Drafter → Submission Compositor | frontmatter 全部 status = final |
| Submission Compositor → Human Review | 所有 `human_signoff_required` 项显式标记 |

---

## 11. 实现路线图（v2 修订版）

### Phase 1: 核心基础设施（v0.1.0 → v0.3.0）
1. `_shared/` — artifact contracts v2、handoff validation、Evidence Provenance Ledger schema
2. `research-article-orchestrator/` — workflow state v2、phase gates、entry path routing
3. `article-readiness-triage/` — 写作就绪判断

### Phase 2: 输入治理（v0.4.0 → v0.5.0）
4. `article-context-builder/` — 三步输入标准化 + 报告规范映射
5. `article-literature-grounder/` — 文献定位与引用支撑

### Phase 3: 架构治理（v0.6.0 → v0.7.0）
6. `article-architect/` — 论文架构 + EDP + Evidence Provenance Ledger
7. `article-methods-statistics-auditor/` — 方法与统计预审

### Phase 4: 写作与审计（v0.8.0 → v0.9.0）
8. `article-drafter/` — 段落级挂接的正文起草
9. `article-claim-auditor/` — 主张—证据逐条核查

### Phase 5: 质量控制（v0.10.0 → v0.11.0）
10. `article-evaluator/` — non-compensatory 六维评估
11. `article-refinement-controller/` — 修订模式分类 + claim downscaling

### Phase 6: 审稿与交付（v0.12.0 → v1.0.0）
12. `article-review-panel/` — 双模式 panel + 差异化 reviewer 输入
13. `article-frontmatter-drafter/` — 摘要/标题/Key Points/Cover Letter
14. `article-submission-compositor/` — 组装、格式核对、human sign-off

### Phase 7: 扩展（v1.1.0+）
- 更多研究类型的 Results 模板和 EDP 模板
- 更多期刊 adapter 的 hard constraint 数据
- 非医学领域（工程、CS、社会科学、人文）的专项适配
- Reference manager 集成
- 中文期刊适配

---

## 12. 风险与开放问题（v2 更新）

### 12.1 已识别风险

1. **Skill 数量膨胀**：v2 从 9 个 skill 增加到 15 个功能 skill。缓解：Phase 分步实现；可选的合并路径（reporting-standard-selector 内嵌于 context-builder；claim-auditor 可作为 evaluator 的增强模式）。
2. **Readiness triage 可能过于保守**：如果 triage 门槛太高，可能导致用户永远走不到 drafting。缓解：`conditionally_ready` 状态允许 proceed with assumptions。
3. **Methods auditor 需要较强的统计专业知识**：可能在某些领域（如 AI/ML、工程）能力不足。缓解：审计范围可配置；标记 `unclear` 而非强行判断。
4. **文献 grounder 的检索质量依赖外部检索能力**：如果检索不充分，literature grounding report 本身可能不可靠。缓解：标记 `grounding_confidence`；允许用户补充文献。
5. **隔离评估在单 agent 环境下的 fallback**：与 idea/proposal 系列一致。缓解：遵循 `_shared/references/runtime-delegation.md`。

### 12.2 开放问题

1. Figure/Table 实际生成：Article 系列规划展示方案（EDP），但不生成实际图表。是否集成 `office-toolkit` 或外部工具进行图表创建？
2. 参考文献格式：Compositor 是否需要验证引用格式（Vancouver、APA、Nature style）和 DOI 有效性？
3. 中文期刊适配：当前设计以英文期刊为主，中文期刊（结构、语言、投稿系统）需单独适配层。
4. LaTeX vs Word 输出：Compositor 是否需要支持多种输出格式？
5. Evidence Provenance Ledger 的初始化：如果用户只提供汇总结果而非原始数据文件，ledger 中 `verification_status = user_supplied_unverified` 的条目比例可能很高。这对后续 claim audit 和 evaluation 的影响需要评估。
6. Claim auditor 与 evaluator 的边界：如果 claim auditor 已经做了逐条审计，evaluator 的 evidence-claim alignment 维度是否还需要独立打分？当前设计是两者互补（auditor 看树木，evaluator 看森林），但需在实践中验证。

---

## 13. v1 → v2 变更总结

| 维度 | v1 | v2 |
|------|-----|-----|
| **系统定位** | 论文写作器 | 证据约束下的 manuscript 构建与审查系统 |
| **Skill 数量** | 9（8 功能 + 1 shared） | 15（14 功能 + 1 shared） |
| **流程阶段** | 3 个隐含阶段 | 5 个显式阶段（输入治理→架构治理→写作→质量控制→投稿交付） |
| **写作位置** | Step 7（Methods/Results/Intro/Discussion 一次性起草） | Step 9（输入治理和架构治理完成后） |
| **前置门禁** | context builder 的 proceed 判断 | readiness triage + context builder + literature grounder 三道门禁 |
| **评估体系** | simple average + flat hard gates | non-compensatory gates + 三层 gate failure 分类 |
| **主张管理** | Claim-Evidence Matrix（静态） | Evidence Provenance Ledger + Claim Auditor + Claim Downscaling |
| **Results 组织** | 2 种模式 | 6 种模式 |
| **研究类型覆盖** | ~10 种（偏医学） | ~25 种（医学+AI+工程+社科+人文） |
| **期刊适配** | 风格分类 | 三类约束系统（hard + soft + strategic） |
| **Compositor** | 组装 + 优化摘要/标题（职责冲突） | 拆为 frontmatter-drafter + submission-compositor |
| **文献处理** | 依赖上游 mapper | 独立 literature grounder |
| **方法审计** | 无 | 独立 methods-statistics-auditor |
| **Human Sign-off** | 无 | 显式 human sign-off checklist |
| **最终产出** | 可直接投稿的 manuscript | submission-ready package + human sign-off checklist |
