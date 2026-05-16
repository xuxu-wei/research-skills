# research-article Skills: Design Document v4

> **Status**: Draft v0.4.0 — Full Architecture, All Skills Core
> **Author**: Xuxu Wei
> **Date**: 2026-05-16
> **Previous**: v0.1.0 → v0.2.0 → v0.3.0
> **Review basis**: `roadmap/review-v1.md`, `roadmap/review-v2.md`
>
> **v4 核心变更**：(1) 新增 research 公共 skill `academic-language-assessor`，供 article/proposal/perspective 系列复用；(2) article-literature-grounder、article-review-panel、article-frontmatter-drafter、article-submission-compositor 全部纳入第一版核心实现，不再暂缓；(3) 在 evaluator 和 refinement-controller 中集成语言评估。

---

## 1. 定位与顶层模型（v3 确认，不变）

**系统本质**：证据约束下的投稿级 manuscript 构建与审查系统。

**顶层模型**：

```
Question → Design → Evidence → Inference → Boundary → Meaning
```

**三层结构**：

```
Layer 1: 普遍论证规律 → Layer 2: 研究类型与报告规范 → Layer 3: 期刊约束系统
```

**产出定位**：

> 交付一份 submission-ready manuscript package。所有未验证数据、缺失材料、作者需确认事项和不可由写作修复的方法学问题均明确标注。系统不替代作者对数据真实性、统计正确性、伦理合规和作者责任的最终确认。

---

## 2. 核心设计原则（v3 原则 + v4 补充）

### 2.1 Primary Responsibility 原则

> 每个 skill 只拥有一个不可替代的主职责。其他职责只能作为辅助，不得决定最终路由。

### 2.2 Non-Compensatory Gate 原则

> 关键质量维度（Scientific Validity, Evidence-Claim Alignment, Language Baseline）不可被其他维度平均抵消。

### 2.3 Safe Degradation 原则

> 输入不完整时安全降级，而非静默填补缺口。宁标记 `partial` 也不伪称 `verified`。

### 2.4 Cross-Package Reuse 原则 [v4 NEW]

> 可在多个 skill 系列间复用的能力（方法审计、文献检索、语言评估）应设计为 research 公共 skill，不内嵌于特定系列。

---

## 3. 完整 Skill 架构

### 3.1 Article 系列（14 个目录：13 功能 + 1 shared）

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
  article-evaluator/                      # [评估] 整体 non-compensatory 评价
  article-refinement-controller/          # [控制] 修订循环 + 修订模式路由
  article-review-panel/                   # [评估] 多角色模拟审稿
  article-frontmatter-drafter/            # [构建] 摘要/标题/Key Points/Cover Letter
  article-submission-compositor/          # [组装] 组装 + 格式核对 + human sign-off
  _shared/                                # [参考] artifact contracts + reporting standards library + handoff rules
```

**全部 13 功能 skill 为第一版核心实现，不再区分 MVP/暂缓。**

### 3.2 依赖的 Research 公共 Skill

| Skill | 位置 | 用途 | 被哪些 article skill 调用 |
|-------|------|------|--------------------------|
| research-opportunity-mapper | `research/` | 证据检索、文献 mapping | literature-grounder（辅助检索） |
| methodology-statistics-preflight | `research/` | 研究设计/方法可行性预检 | methods-statistics-auditor（深度审计前的快速筛查） |
| **academic-language-assessor** [NEW v4] | `research/` | **学术语言质量评估** | **article-evaluator, article-refinement-controller** |

### 3.3 职责与隔离规则

| Skill | 角色 | 执行方式 | 是否可路由 |
|-------|------|---------|-----------|
| orchestrator | 编排 | inline | 控制全部路由 |
| readiness-triage | 门禁 | isolated subagent | 输出 readiness_status |
| context-builder | 构建 | inline | 输出 proceed_status |
| literature-grounder | 构建 | inline | 输出 grounding_confidence |
| architect | 构建 | inline | 输出 blueprint |
| methods-auditor | 审计 | isolated subagent | 输出 audit_status |
| drafter | 构建 | inline | 输出 manuscript draft |
| claim-auditor | 审计 | isolated subagent | 输出 claim audit report |
| evaluator | 评估 | isolated subagent | 输出 evaluation report |
| refinement-controller | 控制 | inline | 管理修订循环 |
| review-panel | 评估 | isolated subagents | 输出 panel report |
| frontmatter-drafter | 构建 | inline | 输出 frontmatter |
| submission-compositor | 组装 | inline | 输出 package + human sign-off |

**隔离规则**（v3 确认，v4 不变）：
- drafter / evaluator / refinement-controller 不得合并
- architect / drafter 不得合并
- claim-auditor / evaluator 独立运行，互补不互替
- 所有 auditor 和 evaluator 角色必须通过隔离子 agent 执行

---

## 4. 新增 Research 公共 Skill: academic-language-assessor

### 4.1 定位

`academic-language-assessor` 是一个 **research 公共 skill**，位于 `research/` 包下，与 `methodology-statistics-preflight` 和 `research-opportunity-mapper` 同级。

它评估学术文稿的语言质量，输出结构化评估报告。不重写文本——重写由各系列的 drafter/refinement-controller 执行。

### 4.2 为什么独立为公共 skill

- **跨系列复用**：article、proposal、perspective 三个系列都需要语言评估
- **专业性**：学术语言评估需要独立的评估框架和标准，不应内嵌在某个 evaluator 中
- **一致性**：统一的语言质量标准跨系列适用，避免各系列自行定义导致不一致
- **可审计**：独立子 agent 执行的语言评估不会被稿件的其他维度干扰

### 4.3 评估维度

| 维度 | 说明 | 硬门禁 |
|------|------|--------|
| **Grammar & Syntax** | 语法错误、句子结构、标点使用 | 是（错误密度过高 → `fail`） |
| **Academic Register & Tone** | 学术语域、正式程度、避免口语化 | 是（语域整体不匹配 → `fail`） |
| **Terminology Consistency** | 术语使用一致性、缩写定义与使用规范 | 否 |
| **Tense & Voice Conventions** | 各章节时态惯例、语态使用 | 否 |
| **Conciseness & Redundancy** | 冗余表达、赘词、不必要的重复 | 否 |
| **Readability & Flow** | 句子长度、段落连贯性、信息密度 | 否 |

### 4.4 学科惯例参考

语言评估应参考目标学科和期刊的惯例：

- **生物医学/临床**：Methods 用过去时；Results 用过去时；Introduction 用现在时（已知事实）和过去时（前人研究）；Discussion 用现在时（解释）和过去时（本研究结果）
- **CS/AI/工程**：Methods/System 可用现在时描述系统设计；实验用过去时
- **数学/理论**：定理和证明用现在时
- **社会科学**：参照 APA 7th 语言指引
- **人文学科**：可用现在时进行文本分析

### 4.5 输入

由调用方（orchestrator 或 evaluator）提供：

- manuscript 文本（全文或指定章节）
- 目标语言（默认英语）
- 目标学科领域（用于惯例匹配）
- 目标期刊（如有，用于期刊特定语言偏好）
- 评估范围（全文评估 / 指定章节 / 指定维度）
- 已有评估报告（如为再评估）

### 4.6 输出：Language Assessment Report

```yaml
language_assessment_report:
  schema_version: "research.v1"
  assessment_id: "lang-001"
  source_skill: "academic-language-assessor"
  target_language: "English"
  discipline: ""                     # biomedical_clinical | cs_ai_engineering | mathematics_theory | social_sciences | humanities | general_science
  target_journal: ""
  scope: full_manuscript | specified_sections
  dimension_scores:
    grammar_syntax:
      score: 0                       # 1–10
      error_density: ""              # errors per 1000 words
      severity: pass | borderline | fail
    academic_register_tone:
      score: 0
      severity: pass | borderline | fail
    terminology_consistency:
      score: 0
      severity: pass | borderline | fail
    tense_voice_conventions:
      score: 0
      severity: pass | borderline | fail
    conciseness_redundancy:
      score: 0
      severity: pass | borderline | fail
    readability_flow:
      score: 0
      severity: pass | borderline | fail
  overall_language_readiness:
    level: submission_ready | minor_language_revision | major_language_revision | needs_professional_editing
  hard_gate_status: pass | fail
  failed_gates: []
  specific_issues:
    - issue_id: "L001"
      dimension: grammar_syntax | academic_register_tone | terminology_consistency | tense_voice_conventions | conciseness_redundancy | readability_flow
      severity: critical | major | minor | suggestion
      location: ""                    # section + paragraph_id + sentence
      original: ""
      issue_description: ""
      suggested_correction: ""        # not a rewrite, but a directional suggestion
      category: ""                    # e.g., "subject-verb agreement", "informal register", "tense shift", "term variation"
  strengths: []
  language_revision_priorities: []
  recommendation: accept | polish | revise_language | professional_editing_required
```

### 4.7 Hard Gates

```yaml
language_hard_gates:
  - gate: "grammar_error_density"
    threshold: "> 3 clear errors per 500 words"
    consequence: "fail — overall_language_readiness ≤ major_language_revision"
  - gate: "academic_register_pervasive"
    threshold: "systematic use of informal/colloquial register in ≥ 2 sections"
    consequence: "fail — overall_language_readiness ≤ needs_professional_editing"
  - gate: "terminology_incoherence"
    threshold: "≥ 3 core concepts with inconsistent terminology across sections"
    consequence: "fail — overall_language_readiness ≤ major_language_revision"
  - gate: "tense_systematic_violation"
    threshold: "systematic tense misuse in Methods or Results"
    consequence: "fail — overall_language_readiness ≤ major_language_revision"
```

### 4.8 执行方式

作为隔离子 agent 执行。不参与 manuscript 起草、修订或整体质量评估。

**调用模式**：

| 模式 | 调用方 | 用途 |
|------|--------|------|
| **evaluator-embedded** | article-evaluator | evaluator 在评估 Language & Academic Register 维度时调用，作为其评分依据 |
| **standalone-preflight** | article-refinement-controller | 在 `language_polishing` 修订模式下，先评估后润色 |
| **standalone-audit** | 用户直接调用 | 独立检查任意文稿的语言质量 |

### 4.9 不负责

- 不重写文本（由各系列的 drafter 或 refinement-controller 执行）
- 不评估科学内容和逻辑（由 evaluator 和 claim-auditor 负责）
- 不判断期刊适配性（由 submission-guard reviewer 或 journal-adapter 负责）
- 不处理参考文献格式、图表质量、文件格式等非语言问题

---

## 5. 标准流程（15 步，5 阶段）

```
Phase 1: 输入治理 (Input Governance)
  0. Minimal Intake Summary
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
  10. Independent Evaluation (含 Language Assessment)
  11. Targeted Refinement (含 Language Polishing)
  12. Mock Review Panel

Phase 5: 投稿交付 (Submission Delivery)
  13. Frontmatter Drafting
  14. Submission Compositor
```

### 5.1 Language Assessment 在流程中的锚点

Language assessment 在三个位置被调用：

```
Phase 4:
  Step 10 (Evaluation):
    article-evaluator → 调用 academic-language-assessor (evaluator-embedded 模式)
    → Language & Academic Register 维度评分 + hard gate 判断

  Step 11 (Refinement):
    IF language gate fail → refinement mode = language_polishing
    → article-refinement-controller → 调用 academic-language-assessor (standalone-preflight 模式)
    → 生成 detailed issues list → drafter 执行语言润色
    → re-assessment by academic-language-assessor

  Step 12 (Review Panel):
    Clarity & Language Reviewer (如有) → 可用 academic-language-assessor 的评估报告作为参考
```

---

## 6. article-evaluator 的 v4 更新

### 6.1 七维评分（新增 Language & Academic Register）

| 维度 | 说明 | 补偿性 | 评估依据 |
|------|------|--------|---------|
| **Scientific Validity** | 研究设计、方法和分析是否合理 | **Non-compensatory** | 独立评估 |
| **Evidence-Claim Alignment** | 证据是否充分支持每个主张 | **Non-compensatory** | claim auditor 报告 + 独立评估 |
| **Reporting Completeness** | 是否满足报告规范和期刊要求 | Compensatory | reporting checklist mapping |
| **Journal Fit** | 与目标期刊的 scope、格式、新颖性阈值是否匹配 | Compensatory | journal adapter |
| **Clarity & Structure** | 逻辑、结构是否清晰 | Compensatory | 独立评估 |
| **Language & Academic Register** [UPDATED] | **语法、语域、术语、时态、可读性** | **Non-compensatory（hard gates）; Compensatory（score）** | **academic-language-assessor 报告** |
| **Contribution Significance** | 知识贡献是否明确 | Compensatory | blueprint + 独立评估 |

### 6.2 Hard Gates v4（新增 Language gate）

```yaml
gate_failures:
  fatal_scientific: []
  reporting: []
  genre_rhetoric:
    # v3 条目保留
    - observational_causal_language
    - narrative_clinical_vignette_in_results
    - didactic_rhetorical_questions_in_discussion
    - promotional_overclaim
    - tone_mismatch_with_journal
    # v4 新增：语言相关 genre/rhetoric gates
    - informal_colloquial_register_in_academic_text
    - non_standard_abbreviation_undefined
    - chinglish_or_l1_interference_patterns
  language_baseline: [NEW v4]
    - grammar_error_density_exceeds_threshold
    - terminology_inconsistent_across_sections
    - tense_systematic_violation_in_methods_or_results
```

### 6.3 Evaluator 调用 Language Assessor 的流程

```
article-evaluator (isolated subagent):
  1. 接收 manuscript draft
  2. 独立评估 Scientific Validity, Evidence-Claim Alignment, etc.
  3. 调用 academic-language-assessor (evaluator-embedded 模式)
     → 获得 Language Assessment Report
  4. 将 language 维度分数和 hard gate 结果纳入 evaluation report
  5. 语言 hard gate 失败时，decision 至少为 revise
  6. 输出完整 evaluation report
```

---

## 7. article-refinement-controller 的 v4 更新

### 7.1 新增 language_polishing 修订模式

```yaml
revision_mode:
  primary:
    - textual_revision
    - structural_revision
    - evidence_relinking
    - reporting_completion
    - claim_downscaling
    - methods_detailing
    - journal_retargeting
    - language_polishing        # [NEW v4] 系统性语言润色
  secondary: []
```

| 修订模式 | 触发条件 | 处理方式 | 是否消耗 revision round |
|---------|---------|---------|----------------------|
| **language_polishing** [NEW] | language hard gate fail 或 author request | academic-language-assessor → 生成 issue list → drafter 逐条修复 → re-assessment | 否（语言润色不算实质性修订轮次） |

### 7.2 Language Polishing 流程

```
article-refinement-controller:
  1. 调用 academic-language-assessor (standalone-preflight 模式)
     → 获取 detailed issues list
  2. 分类 issues: critical / major / minor / suggestion
  3. 生成 Language Polishing Plan:
     - critical & major → 必须修复
     - minor → 建议修复
     - suggestion → 可选
  4. 路由到 article-drafter (language_polishing 模式):
     - drafter 只修复语言问题，不改变实质内容
     - drafter 输出 revised draft + language change log
  5. 调用 academic-language-assessor 进行 re-assessment
  6. 若 re-assessment 通过 → 继续后续流程
  7. 若 re-assessment 仍未通过 → 标记 needs_professional_editing
```

### 7.3 Language Change Log

```yaml
language_change_log:
  - change_id: "LC001"
    issue_id: "L001"
    location: "Methods/P3/S2"
    original: "..."
    revised: "..."
    change_type: grammar_fix | register_upgrade | terminology_standardization | tense_correction | conciseness | readability
    substance_changed: false          # 关键约束：语言修改不得改变实质含义
```

---

## 8. 研究类型矩阵（v3 完整版 + AI/ML 细分）

（同 v3，略。完整矩阵见 v3 第 9 节。）

---

## 9. 路由决策表（v3 完整版 + v4 补充）

### 9.1 Phase Gate 路由

（同 v3 第 8.1 节，增加以下条目）

| 当前 Phase | Gate 结果 | 路由 |
|-----------|----------|------|
| Quality Control | evaluator language_baseline gate = fail | 路由到 refinement-controller，revision_mode = language_polishing |
| Quality Control | language_polishing 后 re-assessment = fail | 标记 `language_status: needs_professional_editing`；不影响继续流程，但在 package 中显式标注 |

### 9.2 Refinement 路由

（同 v3 第 8.2 节，增加 language_polishing 行）

---

## 10. 安全降级策略（v3 完整版 + v4 补充）

（同 v3 第 11 节，增加以下条目）

| 场景 | 降级策略 |
|------|---------|
| `academic-language-assessor` 不可用（如 fallback 环境） | evaluator 自行评估 Language & Academic Register 维度；标记 `language_assessment_mode: evaluator_inline_degraded` |
| Language polishing 后仍不达标 | 标记 `language_status: needs_professional_editing`；package 不超过 `ready_for_author_check`；明确告知作者需要专业语言编辑 |

---

## 11. 实现路线图（v4 修订版）

### Phase 1: 基础 + 公共 skill（v0.1.0 → v0.3.0）
1. `_shared/` — artifact contracts v4 + CONSORT/STROBE/PRISMA item libraries
2. **`academic-language-assessor/`** [NEW v4] — research 公共 skill，语言质量评估
3. `research-article-orchestrator/` — 编排 + minimal intake + backfill + workflow state
4. `article-readiness-triage/` — 写作就绪判断
5. `article-context-builder/` — 三步标准化 + 报告规范映射

### Phase 2: 架构与审计（v0.4.0 → v0.6.0）
6. `article-literature-grounder/` — 文献定位与检索追溯
7. `article-architect/` — 论文架构 + EDP + EPL (Level 1)
8. `article-methods-statistics-auditor/` — 方法/统计阻断判断

### Phase 3: 写作与审计（v0.7.0 → v0.8.0）
9. `article-drafter/` — 按蓝图起草正文
10. `article-claim-auditor/` — 主张—证据逐条核查

### Phase 4: 质量控制（v0.9.0 → v0.11.0）
11. `article-evaluator/` — non-compensatory 评估（含 language assessment 集成）
12. `article-refinement-controller/` — 修订循环（含 language_polishing）
13. `article-review-panel/` — 双模式审稿

### Phase 5: 投稿交付（v0.12.0 → v1.0.0）
14. `article-frontmatter-drafter/` — 摘要/标题/Cover Letter
15. `article-submission-compositor/` — 组装 + human sign-off

### Phase 6: 扩展（v1.1.0+）
- Provenance 粒度升级（Level 1 → Level 2）
- 更多 reporting standards item library
- 更多期刊 adapter hard constraint 数据
- 非医学领域专项适配
- 中文期刊适配

---

## 12. v3 → v4 变更总结

| 维度 | v3 | v4 |
|------|-----|-----|
| **新增公共 skill** | 无 | `academic-language-assessor` 加入 `research/` 包 |
| **语言评估** | 未独立设计 | 六维评估 + hard gates + 三种调用模式 |
| **article-evaluator 维度** | 六维 | 七维（新增 Language & Academic Register） |
| **Hard gates** | 三类（fatal_scientific, reporting, genre_rhetoric） | 四类（增加 language_baseline） |
| **Refinement 模式** | 7 种 | 8 种（新增 language_polishing） |
| **Phase 2 暂缓** | 4 个 skill 暂缓 | 全部 13 功能 skill 为第一版核心 |
| **Language change log** | 无 | 有，约束润色不改变实质内容 |
| **降级策略** | 9 种 | 11 种（新增 language assessor 不可用和不达标两种） |
| **跨包复用** | methodology-statistics-preflight | + academic-language-assessor |
