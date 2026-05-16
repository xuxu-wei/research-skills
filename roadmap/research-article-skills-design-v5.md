# research-article Skills: Design Document v5

> **Status**: Draft v0.5.0 — Structural Hardening
> **Author**: Xuxu Wei
> **Date**: 2026-05-16
> **Previous**: v0.1.0 → v0.2.0 → v0.3.0 → v0.4.0
> **Audit basis**: Cross-package comparison against research-idea, research-proposal, research-perspective
>
> **v5 核心变更**：(1) 补充材料全生命周期（规划→组织→审查）；(2) 审稿回应与修订记录分离机制；(3) 项目目录编号前缀；(4) SKILL 命名统一为 `article-*`；(5) 引入 proposal 风格的 artifact-index 和 artifact-naming-and-directory-rules；(6) 引入 perspective 风格的 I/O 合约；(7) SKILL.md 尺寸控制策略。

---

## 0. 跨包审计发现与 v4 缺口

对 research-idea、research-proposal、research-perspective 三个技能包的系统审计识别出 v4 的以下缺口：

| 缺口 | 严重程度 | 现有包的最佳实践 |
|------|---------|----------------|
| 补充材料无全生命周期管理 | **高** | 无现有包处理（皆为 article 独有需求） |
| 审稿回应/修订记录未与 draft 分离 | **高** | proposal/perspective 使用 `revisions/round-NNN/` 三文件模型 |
| 项目目录无编号前缀 | **中** | research-idea 使用 `00-round-<n>-manifest.md`；proposal 使用语义目录名 |
| SKILL 命名不一致 | **中** | proposal 和 perspective 统一使用 `<prefix>-<role>` 模式 |
| 缺少独立的 artifact-naming-and-directory-rules | **中** | proposal 有专门的 `artifact-naming-and-directory-rules.md` |
| 缺少 state/artifact-index.md | **中** | proposal 维护人类可读产物清单 |
| 缺少 perspective 风格的 I/O 合约 | **低** | perspective 使用结构化 `Allowed Inputs / Required Outputs / Must Not` 合约 |
| SKILL.md 尺寸无上限约束 | **低** | 现有包 54–336 行，中位 ~170 行，所有 schema/rubric 外置到 references/ |

---

## 1. 定位与顶层模型（v4 确认，不变）

**系统本质**：证据约束下的投稿级 manuscript 构建与审查系统。

**顶层模型**：`Question → Design → Evidence → Inference → Boundary → Meaning`

**三层结构**：`普遍论证规律 → 研究类型与报告规范 → 期刊约束系统`

---

## 2. SKILL 命名统一 [v5 NEW]

v4 中 orchestrator 命名为 `research-article-orchestrator`，其他 skill 命名为 `article-*`，与 proposal 和 perspective 包的模式不一致（两者统一使用单前缀）。

**v5 统一为 `article-*` 前缀**，与 `proposal-*` 和 `perspective-*` 对齐：

| 旧名 (v4) | 新名 (v5) |
|-----------|-----------|
| `research-article-orchestrator` | `article-orchestrator` |
| `article-readiness-triage` | 不变 |
| `article-context-builder` | 不变 |
| `article-literature-grounder` | 不变 |
| `article-architect` | 不变 |
| `article-methods-statistics-auditor` | 不变 |
| `article-drafter` | 不变 |
| `article-claim-auditor` | 不变 |
| `article-evaluator` | 不变 |
| `article-refinement-controller` | 不变 |
| `article-review-panel` | 不变 |
| `article-frontmatter-drafter` | 不变 |
| `article-submission-compositor` | 不变 |

**包目录**：`research-article/`（与 `research-proposal/`、`research-perspective/` 对齐）

---

## 3. 完整 Skill 架构

### 3.1 Article 系列（14 个目录：13 功能 + 1 shared）

```
research-article/
  article-orchestrator/                   # [编排器] 工作流编排 + 路由决策
  article-readiness-triage/               # [门禁] 判断能否进入写作系统
  article-context-builder/                # [构建] 输入标准化 + 研究类型分类 + 报告规范选择
  article-literature-grounder/            # [构建] 文献定位、检索追溯与引用支撑
  article-architect/                      # [构建] 论文架构 + EDP + EPL + Supplementary Plan
  article-methods-statistics-auditor/     # [审计] 起草前方法/统计阻断判断
  article-drafter/                        # [构建] 按蓝图起草正文 + 组织补充材料
  article-claim-auditor/                  # [审计] 逐条主张—证据核查
  article-evaluator/                      # [评估] 整体 non-compensatory 评价（含语言评估）
  article-refinement-controller/          # [控制] 修订循环 + 修订模式路由 + 审稿回应管理
  article-review-panel/                   # [评估] 多角色模拟审稿
  article-frontmatter-drafter/            # [构建] 摘要/标题/Key Points/Cover Letter
  article-submission-compositor/          # [组装] 组装 + 格式核对 + 补充材料核查 + human sign-off
  _shared/                                # [参考] artifact contracts + reporting standards library + naming rules + handoff rules
```

### 3.2 依赖的 Research 公共 Skill

| Skill | 用途 | 调用方 |
|-------|------|--------|
| `research-opportunity-mapper` | 证据检索、文献 mapping | article-literature-grounder（辅助检索） |
| `methodology-statistics-preflight` | 研究方法可行性预检 | article-methods-statistics-auditor（快速筛查） |
| `academic-language-assessor` | 学术语言质量评估 | article-evaluator, article-refinement-controller |

---

## 4. 补充材料全生命周期管理 [v5 NEW]

这是 v4 最大缺口。补充材料不是草稿的附属品——它是一个独立的、需要规划、组织、审查的交付物。

### 4.1 三阶段责任分配

| 阶段 | 负责 Skill | 职责 | 产出 |
|------|-----------|------|------|
| **规划** | article-architect | 在 EDP 中标记每个 display 的 placement（main vs supplementary）；确定哪些分析、表格、图表、方法细节进入补充材料；生成 Supplementary Index | `supplementary_index`（blueprint 的一部分） |
| **组织** | article-drafter | 按 Supplementary Index 起草补充材料内容（补充图注、补充表题、补充方法、补充分析）；确保主文中每个引用 `(Supplement S1)` 有对应内容 | 补充材料文件（与 manuscript draft 同版本） |
| **审查** | article-evaluator + article-submission-compositor | evaluator 检查：关键证据是否被错误地埋在补充材料中 / 补充材料的完整性 / 补充内容是否有独立的 claim 未在主文中交代。compositor 检查：期刊补充材料限制合规、文件格式 | evaluator 报告中的 supplementary audit 章节 + compositor checklist |

### 4.2 Supplementary Index（由 architect 生成）

```yaml
supplementary_index:
  schema_version: "research-article.v5"
  source_skill: "article-architect"
  items:
    - supp_id: "S1"
      type: supplementary_table | supplementary_figure | supplementary_methods | supplementary_analysis | supplementary_note | data_deposition | code_repository
      title: ""
      content_summary: ""
      supports_claims: ["C003"]
      supports_display_items: ["D002"]
      referenced_from: "Results/P5"      # 主文中的引用位置
      required_by_reporting_guideline: true | false
      required_by_journal_policy: true | false
      status: planned | drafted | final | missing
  journal_limits:
    max_supplementary_items: 0
    max_supplementary_files: 0
    supplementary_file_format: ""
    data_availability_policy: ""
    code_availability_policy: ""
  cross_reference_map:                    # 主文 ↔ 补充材料交叉引用
    - main_text_location: "Results/P3"
      supp_ids: ["S1", "S2"]
      reference_text: "(Supplementary Table S1, Supplementary Fig. S2)"
```

### 4.3 Evaluator Supplementary Audit

evaluator 在评估时增加 supplementary audit 维度：

```yaml
supplementary_audit:
  critical_evidence_buried: []            # 支撑主要结论的证据被放在补充材料中
  missing_supplementary_content: []       # 主文引用了但补充材料缺失
  orphan_supplementary_content: []        # 补充材料中有主文未引用的内容
  overstuffed_supplementary: []           # 不应进入主文但占据补充材料大量篇幅（接近重复投稿）
  journal_limit_compliance: pass | fail   # 补充材料数量/格式是否超标
  data_code_availability_compliance: pass | fail | partial
```

---

## 5. 审稿回应与修订记录分离机制 [v5 NEW]

v4 的 refinement-controller 提到了 response-to-reviewer 但未定义完整的分离机制。v5 采纳 proposal 和 perspective 的"三文件每轮"模型。

### 5.1 修订轮次目录结构

```
revisions/
  round-001/
    revision-plan-r001.md              # 定向修订计划
    response-to-reviewer-r001.md       # 逐条回应（独立于 manuscript）
    revision-delta-r001.md             # 版本差异报告
  round-002/
    revision-plan-r002.md
    response-to-reviewer-r002.md
    revision-delta-r002.md
```

### 5.2 入文策略（Entry Strategy）

每个修订条目必须标注入文策略，与 proposal 和 perspective 一致：

```yaml
entry_strategy:
  入正文: "修改进入 manuscript 正文"
  仅入回应: "仅在 response 中说明，不修改正文"
  不处理: "明确拒绝修订，给出理由"
```

### 5.3 Response-to-Reviewer 文件

**独立于 manuscript draft**。Manuscript 正文中不得出现审稿回应语言（"根据审稿人建议...""回应XX的质疑...""对此问题，我们补充..."）。

```yaml
response_to_reviewer:
  round: 1
  manuscript_version: "manuscript-v002"
  evaluation_ref: "evaluation-v001.md"
  responses:
    - concern_id: "E001-C003"              # 引用 evaluator 的 issue ID
      concern_summary: ""
      action: 已修改 | 仅回应 | 不处理
      manuscript_location: ""              # 如修改：修改位置
      response_text: ""                    # 给审稿人的回应文本
      change_summary: ""                   # 实际修改内容摘要
  unresolved_issues: []
  new_issues_introduced: []
```

### 5.4 Revision Delta Report

```yaml
revision_delta:
  round: 1
  previous_manuscript: "manuscript-v001.md"
  updated_manuscript: "manuscript-v002.md"
  revision_plan_summary: ""
  evaluator_concerns:
    addressed: []
    partially_addressed: []
    not_addressed_with_reason: []
  new_issues_introduced: []
  substantive_changes:
    methods_changed: false
    results_changed: false
    primary_claim_strength_changed: false
    contribution_statement_changed: false
  new_assumptions_requiring_author_confirmation: []
  recommended_next_step: re_evaluate | panel | compositor
```

**Delta report 关键约束**：不得仅写 "polished expression" 或 "improved clarity"。必须说明哪些 evaluator 关切被处理、哪些未处理、是否引入新问题、核心主张是否变化。

---

## 6. 项目目录结构与编号前缀 [v5 NEW]

### 6.1 编号前缀方案

采纳 `00_` 到 `NN_` 的两位数字前缀，确保文件浏览器中按工作流顺序排列：

```
<workspace>/research-article-projects/<project-slug>/
  00_input/                             # 用户原始材料
  01_readiness/                         # Readiness Triage Report
  02_context/                           # Article Context Brief
  03_literature/                        # Literature Grounding Report
  04_blueprint/                         # Article Blueprint + EDP + EPL + Supplementary Index
  05_audit/                             # Methods & Statistics Audit Report
  06_drafts/                            # manuscript-v001.md, manuscript-v002.md, ...
  07_claim-audit/                       # Claim Audit Reports
  08_evaluations/                       # Evaluation Reports
  09_revisions/                         # Revision rounds
     round-001/
     round-002/
  10_panel/                             # Panel Report + reviewer briefs
  11_frontmatter/                       # Abstract, Key Points, Title, Cover Letter
  12_package/                           # Submission Package
  13_state/                             # workflow-state.yaml, artifact-index.md
  14_delegates/                         # Isolated subagent briefs (for audit trail)
```

### 6.2 编号原则

- 目录编号 = 该阶段在标准流程中首次出现的位置
- 不跳号（即使某个阶段在特定 entry mode 中被跳过）
- `13_state/` 固定为最后一个编号目录
- `14_delegates/` 存放隔离子 agent 的输入/输出包，用于审计追溯

### 6.3 Artifact Index（`13_state/artifact-index.md`）

采用 proposal 风格的人类可读产物清单：

```markdown
# Artifact Index — {{project_slug}}

| Artifact ID | Role | Version | Path | Source Skill | Created | Status |
|------------|------|---------|------|-------------|---------|--------|
| readiness-001 | Readiness Report | v1 | 01_readiness/readiness-report.md | article-readiness-triage | Step 1 | final |
| context-001 | Context Brief | v1 | 02_context/context-brief.md | article-context-builder | Step 2 | final |
| lit-ground-001 | Literature Grounding | v1 | 03_literature/literature-grounding.md | article-literature-grounder | Step 3 | final |
| blueprint-001 | Blueprint | v1 | 04_blueprint/article-blueprint.md | article-architect | Step 4 | final |
| methods-audit-001 | Methods Audit | v1 | 05_audit/methods-audit.md | article-methods-statistics-auditor | Step 7 | final |
| manuscript-v001 | Draft | v1 | 06_drafts/manuscript-v001.md | article-drafter | Step 8 | superseded |
| manuscript-v002 | Draft | v2 | 06_drafts/manuscript-v002.md | article-drafter | Step 11 | current |
| claim-audit-001 | Claim Audit | v1 | 07_claim-audit/claim-audit-v001.md | article-claim-auditor | Step 9 | final |
| eval-001 | Evaluation | v1 | 08_evaluations/evaluation-v001.md | article-evaluator | Step 10 | final |
| ... | ... | ... | ... | ... | ... | ... |
```

### 6.4 独立的 Artifact Naming and Directory Rules

`_shared/references/artifact-naming-and-directory-rules.md` 定义：
- 完整目录树和每个目录的用途
- 文件命名规则（版本号格式、artifact ID 格式）
- 当前版本指针规则（state/workflow-state.yaml 为唯一权威）
- 禁止覆盖规则（prior versions must never be overwritten）
- Clean 版本规则（仅用于终稿提交，需记录源版本）

---

## 7. SKILL.md 尺寸控制策略 [v5 NEW]

### 7.1 目标

- **上限**：每个 SKILL.md ≤ 250 行
- **中位目标**：~150–180 行
- **原则**：不在 SKILL.md 中内嵌 schema、rubric、template 正文或代码；只引用对应文件路径

### 7.2 分拆规则

| 内容类型 | 放置位置 | 示例 |
|---------|---------|------|
| 流程指令 | SKILL.md 正文 | When to Use, Core Rules, Procedure steps, Pitfalls |
| Schema / 字段定义 | `references/schema-*.md` | schema-manuscript-draft.md |
| 评分标准 / 锚点 | `references/rubric-*.md` | rubric-article-evaluation.md |
| 硬门禁规则 | `references/gates-*.md` | gates-article-evaluation.md |
| 模板 | `templates/template-*.md` | template-manuscript.md |
| 长篇方法论 | `references/` 中单独文件 | writing-methodology.md |
| I/O 合约 | SKILL.md 中用紧凑 YAML | 见第 8 节 |
| 反模式 / 案例 | `references/anti-pattern-*.md` | anti-pattern-results.md |

### 7.3 参照现有包的尺寸

| 包 | 最大 SKILL.md | orchestrator 行数 | 其他 skill 行数范围 |
|----|-------------|------------------|-------------------|
| research-idea | 194 | 105 | 54–194 |
| research-proposal | 336 | 302 | 103–336 |
| research-perspective | 246 | 246 | 86–170 |

Article 系列的 orchestrator 因需要定义 15 步流程 + 多种 entry path + 路由决策，预计 ~280 行。其他 skill 应控制在 120–200 行。

---

## 8. Perspective 风格的 I/O 合约 [v5 NEW]

采纳 perspective 包的结构化 I/O 合约模式，使每个 skill 的输入输出边界更清晰：

```yaml
# 每个 article skill 的 SKILL.md 中包含此合约块

io_contract:
  allowed_inputs: []          # 可以接收的 artifact 类型
  required_outputs: []        # 必须输出的 artifact 类型
  may_read: []                # 可以读取的文件路径模式
  may_write: []               # 可以写入的文件路径模式
  must_not_read: []           # 禁止读取的内容（隔离保证）
  must_not_write: []          # 禁止写入的内容（角色边界）
  may_call: []                # 可以调用的其他 skill
  must_not_call: []           # 禁止调用的 skill
  failure_modes: []           # 已知失效模式及处理
  escalation_route: ""        # 不可自行解决的问题的上报路径
```

### 8.1 示例：article-drafter 的 I/O 合约

```yaml
io_contract:
  allowed_inputs:
    - article_blueprint
    - article_context_brief
    - literature_grounding_report
    - methods_audit_report
    - revision_plan (in revision mode)
  required_outputs:
    - manuscript_draft (versioned)
    - supplementary_materials_draft (versioned, if applicable)
  may_read:
    - "04_blueprint/**"
    - "02_context/**"
    - "03_literature/**"
    - "05_audit/**"
    - "09_revisions/**" (in revision mode)
  may_write:
    - "06_drafts/manuscript-v*.md"
    - "06_drafts/supplementary-v*.md"
  must_not_read:
    - "08_evaluations/**"       # 不接触评估报告，避免自我审查
    - "07_claim-audit/**"       # 不接触 claim audit，避免预判
    - "10_panel/**"             # 不接触 panel 报告
  must_not_write:
    - "08_evaluations/**"
    - "07_claim-audit/**"
    - "04_blueprint/**"         # 不修改蓝图
  may_call:
    - academic-language-assessor (for language check before delivery)
  must_not_call:
    - article-evaluator
    - article-claim-auditor
  failure_modes:
    - "blueprint missing results_skeleton → request architect rework"
    - "context_brief missing key variable definitions → flag in unresolved_issues"
  escalation_route: "article-orchestrator"
```

---

## 9. 文件版本管理规范 [v5 强化]

### 9.1 版本触发规则

| 变更类型 | 触发新版本 | 说明 |
|---------|----------|------|
| 实质性内容修改（claim, evidence, analysis） | 是 | `manuscript-v001` → `manuscript-v002` |
| 结构性重组（section reorder） | 是 | 同上 |
| 语言润色（language polishing） | 否 | 在原版本上覆盖，记录 change log |
| 格式调整（formatting only） | 否 | 同上 |
| 补充 checklist 条目 | 否 | 同上 |
| 终稿 clean 版本 | 是（`-clean` 后缀） | `manuscript-v003-clean.md` |

### 9.2 禁止覆盖规则

- `state/workflow-state.yaml` 始终记录当前版本指针
- Prior versions **不得被覆盖或删除**
- Clean 版本仅在源版本存在并已记录后才可创建

### 9.3 Manuscrip 版本与补充材料版本联动

- `manuscript-v002.md` 配套 `supplementary-v002.md`
- 补充材料版本号始终与主 manuscript 版本号一致
- 仅语言润色时两者同步覆盖，不增版本号

---

## 10. 标准流程（15 步，5 阶段，v5 更新）

```
Phase 1: 输入治理 (Input Governance)
  0. Minimal Intake Summary
  1. Article Readiness Triage
  2. Context Brief + Reporting Standard Selection
  3. Literature Grounding

Phase 2: 架构治理 (Architecture Governance)
  4. Article Blueprint
  5. Claim–Evidence Matrix + Evidence Provenance Ledger
  6. Evidence Display Plan + Supplementary Index
  7. Methods / Statistics Audit

Phase 3: 写作 (Writing)
  8. Manuscript Drafting + Supplementary Materials Organization

Phase 4: 质量控制 (Quality Control)
  9. Claim-Level Audit
  10. Independent Evaluation（含 Language Assessment + Supplementary Audit）
  11. Targeted Refinement（含 Response-to-Reviewer + Revision Delta）
  12. Mock Review Panel

Phase 5: 投稿交付 (Submission Delivery)
  13. Frontmatter Drafting
  14. Submission Compositor（含 Supplementary Compliance Check）
```

### 10.1 Supplementary Materials 在流程中的锚点

```
Step 6:  article-architect → Supplementary Index（规划）
Step 8:  article-drafter → 起草补充材料内容（组织）
Step 10: article-evaluator → Supplementary Audit（审查一）
Step 14: article-submission-compositor → Supplementary Compliance Check（审查二）
```

### 10.2 修订记录在流程中的锚点

```
Step 11: article-refinement-controller →
  revisions/round-NNN/
    revision-plan-rNNN.md
    response-to-reviewer-rNNN.md
    revision-delta-rNNN.md
  → article-drafter (修订模式) → 新 manuscript + 新 supplementary
  → article-evaluator (re-evaluation, isolated)
```

---

## 11. 关键 Skill 执行合约更新

以下仅列出 v5 中有实质更新的 skill。

### 11.1 article-architect（新增 Supplementary Index 职责）

**主职责**：设计论文架构 + EDP + Evidence Provenance Ledger + **Supplementary Index**。

**新增输出**：

```yaml
supplementary_index:
  # 完整结构见第 4.2 节
```

**EDP 中的 placement 字段**直接决定 display_item 进入主文还是补充材料：

```yaml
display_item:
  placement: main | supplementary
  supp_id: "S1"                        # 仅当 placement = supplementary
```

### 11.2 article-drafter（新增 Supplementary Organization 职责）

**主职责**：按蓝图起草 manuscript 正文 + **组织补充材料内容**。

**新增输出**：
- `supplementary-vNNN.md`（与 `manuscript-vNNN.md` 同版本）
- 补充图注、补充表题、补充方法、补充分析

**新增 I/O 合约**：

```yaml
io_contract:
  required_outputs:
    - manuscript_draft
    - supplementary_materials_draft     # [v5 NEW]
  may_write:
    - "06_drafts/manuscript-v*.md"
    - "06_drafts/supplementary-v*.md"   # [v5 NEW]
```

**补充材料起草规则**：
- 每个补充条目标题与 Supplementary Index 中的 `supp_id` 对应
- 补充方法应独立可读（不依赖翻阅主文）
- 补充图注、表题格式与主文一致
- 不得在补充材料中引入新的核心主张

### 11.3 article-evaluator（新增 Supplementary Audit + 语言评估）

**主职责**：整体 non-compensatory 评价（v4）+ **Supplementary Audit**（v5）+ Language Assessment 集成。

**七维评分**（v4 确认，v5 保持）：

| 维度 | 补偿性 |
|------|--------|
| Scientific Validity | Non-compensatory |
| Evidence-Claim Alignment | Non-compensatory |
| Reporting Completeness | Compensatory |
| Journal Fit | Compensatory |
| Clarity & Structure | Compensatory |
| Language & Academic Register | Non-compensatory (hard gates); Compensatory (score) |
| Contribution Significance | Compensatory |

**新增 Supplementary Audit**（见第 4.3 节）：

```yaml
supplementary_audit:
  critical_evidence_buried: []
  missing_supplementary_content: []
  orphan_supplementary_content: []
  journal_limit_compliance: pass | fail
  data_code_availability_compliance: pass | fail | partial
```

### 11.4 article-refinement-controller（新增审稿回应管理）

**主职责**：修订循环 + 修订模式路由 + 语言润色 + **审稿回应与修订记录管理**。

**新增输出**（每轮三个文件）：

```
revisions/round-NNN/
  revision-plan-rNNN.md
  response-to-reviewer-rNNN.md
  revision-delta-rNNN.md
```

**新增 I/O 合约**：

```yaml
io_contract:
  required_outputs:
    - revision_plan
    - response_to_reviewer           # [v5 NEW] 独立于 manuscript
    - revision_delta                 # [v5 NEW]
  may_write:
    - "09_revisions/round-*/**"      # [v5 NEW]
  must_not_write:
    - "06_drafts/**"                 # 修订内容由 drafter 写入，controller 不直接修改
```

**Response-to-Reviewer 生成规则**（与 proposal/perspective 一致）：
- 逐条引用 evaluator concern ID
- 每条标注 入文策略：`入正文` / `仅入回应` / `不处理`
- "不处理"的建议必须给出理由
- Manuscript 正文中**不得出现**审稿回应语言
- Response 文件独立保存在修订轮次目录中

### 11.5 article-submission-compositor（新增 Supplementary Compliance Check）

**主职责**：组装投稿包 + 格式核对 + **补充材料期刊合规检查** + human sign-off。

**新增检查项**：

```yaml
supplementary_compliance:
  item_count_within_limit: true | false
  file_format_matches_journal_spec: true | false
  data_availability_statement_present: true | false
  code_availability_statement_present: true | false
  supplementary_references_included_in_main_reference_list: true | false | not_applicable
  supplementary_content_cross_referenced_from_main_text: true | false
```

---

## 12. _shared Skill 设计 [v5 强化]

采纳 research-idea 的 `_shared/` 模式，article 的 shared skill 包含：

```
_shared/
  SKILL.md                                   # ~60 行，声明为 reference-only dependency
  references/
    artifact-contracts.md                    # 所有跨 skill artifact schema
    artifact-naming-and-directory-rules.md   # [v5 NEW] 目录结构、文件命名、版本规则
    handoff-validation.md                    # 跨 skill handoff 校验
    workflow-manifest-schema.md              # round manifest schema
    runtime-delegation.md                    # delegate_task fallback
    evidence-provenance-ledger-schema.md     # EPL schema（从 architect 分离）
  reporting-standards/                       # [v5 NEW] item library
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
  templates/
    round-manifest.md
```

**加载方式**：

```text
skill_view(name="research-article-shared", file_path="references/artifact-contracts.md")
```

---

## 13. 路由决策表（v5 更新）

（v3/v4 基础 + v5 补充）

### 13.1 补充材料相关路由

| 触发条件 | 路由 |
|---------|------|
| Evaluator 发现 critical evidence buried in supplementary | 路由到 refinement → drafter 将关键证据移至主文 |
| Compositor 发现 supplementary 缺少主文引用的条目 | 路由到 drafter 补充缺失内容 |
| Compositor 发现 supplementary 超过期刊数量/格式限制 | 路由到 architect 重新规划 → drafter 调整 |
| Evaluator 发现 supplementary 中有主文未引用的孤立内容 | 标记为 `orphan_supplementary` → 删除或建立引用 |
| Data/code availability statement 缺失 | compositor 标记 `partial`，不阻止流程但必须在 human sign-off 中标注 |

### 13.2 修订记录相关路由

| 触发条件 | 路由 |
|---------|------|
| Refinement 完成 | 生成 `revision-plan` + `response-to-reviewer` + `revision-delta` → 触发 re-evaluation |
| Response 中选择 `不处理` 的建议 | 必须在 response 中给出理由；若为 critical issue，re-evaluator 将再次标记 |
| Delta report 显示 primary claim strength changed | 标记 `substantive_changes.primary_claim_strength_changed: true` → 需用户确认 |
| Delta report 只写"polished expression"无实质内容 | Refinement controller 退回 delta，要求具体化 |

---

## 14. 安全降级策略（v5 补充）

（v3/v4 基础 + v5 补充）

| 场景 | 降级策略 |
|------|---------|
| Supplementary Index 中有条目缺失 | drafter 标记 `status: missing`；evaluator 记录；compositor 在 package 中显式列出缺失条目 |
| 用户未提供数据/代码存放信息 | compositor 生成模板 statement，标记 `ready_for_author_check` |
| Revision round 超过上限（2 轮） | 停止循环；标记 `major_revision_required`；在 package 中列出未解决问题 |
| Response-to-reviewer 缺少某条 evaluator concern | refinement controller 在 delta report 中标记 `partially_addressed` |
| 补充材料组织时发现蓝图 supplementary index 不完整 | drafter 标记，回退到 architect 更新 index |

---

## 15. 实现路线图（v5 修订版）

所有 13 个功能 skill + 1 shared + 1 research 公共 skill 为第一版核心。

### Phase 1: 基础设施（v0.1.0 → v0.3.0）
1. `_shared/` — artifact contracts v5 + reporting standards item library + naming rules
2. `academic-language-assessor/` — （已完成）research 公共 skill
3. `article-orchestrator/` — 编排 + minimal intake + backfill + workflow state + artifact index

### Phase 2: 输入与架构治理（v0.4.0 → v0.6.0）
4. `article-readiness-triage/`
5. `article-context-builder/`
6. `article-literature-grounder/`
7. `article-architect/` — 含 Supplementary Index
8. `article-methods-statistics-auditor/`

### Phase 3: 写作与审计（v0.7.0 → v0.9.0）
9. `article-drafter/` — 含 Supplementary Materials Organization
10. `article-claim-auditor/`
11. `article-evaluator/` — 含 Language Assessment + Supplementary Audit

### Phase 4: 质量控制（v0.10.0 → v0.11.0）
12. `article-refinement-controller/` — 含 Response-to-Reviewer + Revision Delta
13. `article-review-panel/`

### Phase 5: 投稿交付（v0.12.0 → v1.0.0）
14. `article-frontmatter-drafter/`
15. `article-submission-compositor/` — 含 Supplementary Compliance Check

---

## 16. v4 → v5 变更总结

| 维度 | v4 | v5 |
|------|-----|-----|
| **补充材料** | 无生命周期管理 | 三阶段：architect 规划 → drafter 组织 → evaluator+compositor 审查 |
| **Supplementary Index** | 无 | architect 产出，记录每个补充条目的类型、支撑主张、主文引用位置 |
| **审稿回应** | 提及但未定义结构 | 三文件模型：revision-plan + response-to-reviewer + revision-delta |
| **入文策略** | 无 | 入正文 / 仅入回应 / 不处理 |
| **修订记录位置** | 未明确分离 | `revisions/round-NNN/` 独立目录 |
| **目录编号前缀** | 无 | `00_input/` 到 `14_delegates/` |
| **SKILL 命名** | `research-article-orchestrator` + `article-*` | 统一 `article-*`，与 proposal/perspective 对齐 |
| **独立的命名规则文件** | 分散在 blueprint 和 compositor | `_shared/references/artifact-naming-and-directory-rules.md` |
| **Artifact Index** | 无 | `13_state/artifact-index.md` |
| **I/O 合约** | 无 | 每个 skill 包含 perspective 风格的 `io_contract` 块 |
| **SKILL.md 尺寸** | 无约束 | ≤ 250 行上限；所有 schema/rubric 外置到 references/ |
| **版本联动** | 未定义 | manuscript 与 supplementary 版本号同步 |
| **Delta report 约束** | 无 | 禁止 "polished expression" 式空洞描述 |
| **Response 禁止嵌入正文** | 未规定 | 明确禁止 manuscript 中出现审稿回应语言 |
