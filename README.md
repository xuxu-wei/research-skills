# Research Skills

`research-skills` 是一个研究工作流技能库。当前有效的技能来源是 `research-skills/`。

这个仓库不是把所有能力写进一个巨型 prompt，而是把研究任务拆成可组合的技能包。每个技能包包含：

- `SKILL.md`：技能入口，负责说明触发条件、角色边界、执行步骤和必要引用。
- `references/`：规则、schema、rubric、artifact contract、命名规范、路由规则和质量门。
- `templates/`：面向最终产物或中间报告的模板。
- `scripts/`：用于检索、转换、审计或一致性检查的辅助脚本。

核心设计目标是：让复杂研究任务可以被分层拆解、隔离评估、循环修订、保留版本血缘，并最终组装成可审阅的研究产物。

## 技能包归属

本仓库中的技能包分为两类：**Xuxu 开发的技能包**和**外部依赖技能包**。

### Xuxu 开发的技能包

**`research/` 下的通用研究技能（4 个）：**

| 技能包 | 用途 |
| --- | --- |
| `academic-language-assessor` | 评估学术语言、语域、母语干扰和可投稿表达问题 |
| `medical-journal-review` | 从医学期刊编辑和审稿标准出发评估研究设计或稿件 |
| `methodology-statistics-preflight` | 在进入 proposal、SAP 或 manuscript 前检查方法学和统计分析可行性 |
| `research-opportunity-mapper` | 把文献、指南、数据机会或临床问题转成 evidence map / opportunity map |

**研究工作流技能包（4 个顶级目录，含全部子技能）：**

| 技能包目录 | 目标产物 |
| --- | --- |
| `research-idea/` | Research Idea Portfolio |
| `research-proposal/` | Proposal / SAP / Final Proposal Package |
| `research-article/` | Manuscript / Submission Package |
| `research-perspective/` | Perspective / Viewpoint / Commentary |

### 外部依赖技能包

以下技能包非 Xuxu 开发，但为上述工作流提供基础能力支撑，是潜在依赖：

- **`research/` 下的其余技能：** `academic-deep-search`、`arxiv`、`blogwatcher`、`llm-wiki`、`polymarket`、`pubmed` — 提供文献检索、知识整理和数据源查询能力。
- **`data-science/`：** `jupyter-live-kernel`、`python-environments` — 提供 Python 环境和 Jupyter 交互支持。
- **`office-toolkit/`：** Office 文档处理入口。
- **`productivity/`：** `maps`、`nano-pdf`、`ocr-and-documents`、`powerpoint` — 提供文档处理、OCR、演示文稿等通用工具能力。

## 仓库分层

### 第一层：基础工具与通用研究能力

这些模块为上层工作流提供检索、评审、文档处理和运行环境支持。

| 模块 | 主要内容 | 典型用途 |
| --- | --- | --- |
| `research/` | 文献检索、证据图谱、研究机会映射、方法学预审、医学期刊审稿、学术语言评估、PubMed/arXiv 辅助检索 | 为 idea、proposal、article、perspective 提供证据和方法学支撑 |
| `data-science/` | Python 环境、Jupyter live kernel | 数据分析、实验环境、Notebook 协作 |
| `productivity/` | PDF、OCR、PowerPoint、地图、文档处理等工具 | 处理研究材料、提取文档信息、生成演示文稿 |
| `office-toolkit/` | Office 文档处理入口 | Word / PowerPoint / Office 文件相关操作 |

### 第二层：研究工作流技能包

这些是仓库的核心研究生产系统。

| 技能包 | 目标产物 | 主要任务 |
| --- | --- | --- |
| `research-idea/` | Research Idea Portfolio | 从粗糙方向、临床问题、数据资产、文献线索或 funding call 中生成、评估和筛选研究 idea |
| `research-proposal/` | Proposal / SAP / Final Proposal Package | 将成熟 idea 转化为 proposal，进行独立评价、修订、模拟评审和最终打包 |
| `research-article/` | Manuscript / Submission Package | 从研究数据、结果和方法信息出发，构建论文、评估、修订并准备投稿包 |
| `research-perspective/` | Perspective / Viewpoint / Commentary | 从核心观点出发，构建 claim ledger、论证骨架、文章初稿、评估和终稿合规检查 |

### 第三层：工作流治理机制

所有 research 系列工作流共享几类治理机制：

- 角色隔离：生成、起草、评估、审稿、修订、打包分别由不同技能承担。
- 独立评估：evaluator、auditor、reviewer、triage 等角色应通过隔离子 agent 执行，不能既生成又评价。
- 版本血缘：产物记录 `source_skill`、`based_on`、`change_type`、artifact ID、version ID、round ID 等字段。
- 质量门：关键节点设置 hard gate，防止证据不足、方法学不可行、过度主张或未独立评估的产物继续流转。
- 任务循环：评估结果进入 refinement controller，再由 drafter 更新，随后重新评估或进入 panel / compositor。
- 打包只组装：assembler / compositor 只汇总已有产物，不负责偷偷重写、降级或掩盖未解决问题。

## `research/` 通用研究技能

`research/` 是其他研究技能包的基础能力层。

主要技能包括：

- `academic-deep-search`：深度学术检索，用于复杂研究问题的多轮证据搜索。
- `research-opportunity-mapper`：把文献、指南、数据机会或临床问题转成 evidence map / opportunity map。
- `methodology-statistics-preflight`：在进入 proposal、SAP 或 manuscript 前检查方法学和统计分析可行性。
- `medical-journal-review`：从医学期刊编辑和审稿标准出发评估研究设计或稿件。
- `academic-language-assessor`：评估学术语言、语域、母语干扰和可投稿表达问题。
- `pubmed`、`arxiv`：面向 PubMed 和 arXiv 的检索辅助技能。
- `llm-wiki`、`blogwatcher`、`polymarket` 等：用于知识整理、内容监控和特定数据源查询。

这个模块通常不直接产出最终研究方案，而是为上层工作流提供证据、检索记录、机会判断和方法学诊断。

## `research-idea/`：研究想法生成与组合

### 目标

把粗糙研究方向、临床/实践问题、数据资产、文献线索或 funding call 转换成 1-3 个可供 PI 审阅的候选研究 idea，并给出 promoted / backup / rejected / merged 等状态。

### 主要角色

| 技能 | 角色 | 不能做什么 |
| --- | --- | --- |
| `research-idea-orchestrator` | 总控工作流、维护状态、调度子任务、控制循环和 handoff | 不直接替代 evaluator 做评分 |
| `research-context-builder` | 抽取研究背景、目标、数据、方法、限制和假设 | 不生成完整 idea portfolio |
| `research-opportunity-mapper` | 检索证据、建立 evidence map 和 opportunity map | 不替代 idea generator |
| `multi-path-idea-generator` | 用多条路径生成候选 idea | 不评分、不 promote、不写 proposal |
| `methodology-statistics-preflight` | 对方法学和统计路径做预审 | 不负责 idea 排名 |
| `idea-evaluator` | 独立评分、hard gate、fatal flaw 判断、promote/reject 建议 | 不生成 idea、不写 proposal |
| `idea-adversarial-review-panel` | 在 proposal handoff 前攻击 novelty、feasibility、PI strategy 风险 | 不重新打分、不重写 idea |
| `idea-portfolio-assembler` | 汇总 promoted / backup / merged / rejected ideas，保留 lineage | 不重新评估 idea |

### 标准流程

```text
research-context-builder
  -> research-opportunity-mapper
  -> multi-path-idea-generator
  -> methodology-statistics-preflight
  -> idea-evaluator
  -> idea-adversarial-review-panel
  -> idea-portfolio-assembler
```

### 任务循环设计

1. Context 不足：回到 `research-context-builder`，补充用户目标、数据资产、方法约束或临床问题定义。
2. Evidence 不足：回到 `research-opportunity-mapper`，补齐 evidence map、opportunity map 或证据不足报告。
3. Idea 质量不足：回到 `multi-path-idea-generator`，换生成路径或合并/重构 idea。
4. 方法学不可行：回到 `methodology-statistics-preflight` 或降级目标期刊/研究设计。
5. Evaluation 未通过：由 orchestrator 根据 evaluator 结果执行 revise / reframe / merge / reject。
6. Handoff 被 adversarial panel 阻断：回到证据、方法学、生成或 evaluation 环节；不能直接进入 proposal。

### 产出结构

典型产物包括：

- Research Context Brief
- Evidence Map
- Opportunity Map
- Generated Idea Set
- Methodology / Statistics Preflight Report
- Idea Evaluation Report
- Adversarial Handoff Review
- Research Idea Portfolio

面向用户的最终产物应为可读的 Markdown；只有 agent-to-agent 状态传递才使用 YAML 中间结构。

## `research-proposal/`：Proposal 与 SAP 工作流

### 目标

把成熟 idea 转化为 proposal，并支持独立评价、定向修订、模拟评审、最终打包，以及可选的 SAP（Statistical Analysis Plan）分支。

### 主要角色

| 技能 | 角色 | 不能做什么 |
| --- | --- | --- |
| `proposal-orchestrator` | 总控 proposal 工作流、调度 triage/evaluator/panel/SAP 分支 | 不内联替代独立 evaluator |
| `proposal-context-brief-builder` | 把 idea、funding call、临床问题或数据机会整理成 proposal context brief | 不写完整 proposal |
| `proposal-readiness-triage` | 判断 idea 是否成熟到可以进入 proposal drafting | 不起草 proposal |
| `proposal-drafter` | 起草和维护 proposal 文件，修订时生成 response / change summary | 不评价 proposal |
| `proposal-evaluator` | 独立评价 novelty、feasibility、impact、clarity、method fit 等 | 不重写 proposal |
| `proposal-refinement-controller` | 把 evaluator feedback 转成 revision plan，控制修订循环 | 不直接伪装成 evaluator |
| `proposal-review-panel` | 多角色模拟评审 | reviewer 之间不得互相看输出 |
| `proposal-package-assembler` | 汇总最终 proposal package、lineage、unresolved issues、panel dissent | 不清洗或改写 proposal |
| `sap-writer` | 写 SAP | 不替代 SAP evaluation |
| `sap-evaluator` | 独立评价 SAP | 不修改 SAP |
| `sap-refinement-controller` | 控制 SAP 修订循环和再评价 | 不把未评价 SAP 标为 accepted |

### 标准流程

```text
proposal-context-brief-builder
  -> research-opportunity-mapper
  -> proposal-readiness-triage
  -> proposal-drafter
  -> proposal-evaluator
  -> proposal-refinement-controller
  -> proposal-review-panel
  -> proposal-package-assembler
```

可选 SAP 分支：

```text
sap-writer -> sap-evaluator -> sap-refinement-controller
```

### 任务循环设计

Proposal 循环：

```text
draft-vNNN
  -> proposal-evaluator
  -> proposal-refinement-controller
  -> proposal-drafter revision
  -> revision-delta + response
  -> independent re-evaluation
```

SAP 循环：

```text
sap-vNNN
  -> sap-evaluator
  -> sap-refinement-controller
  -> sap-writer revision
  -> independent SAP re-evaluation
```

停止条件包括：

- readiness triage 阻断；
- evaluator 发现不可修复 fatal flaw；
- 修订需要凭空发明 endpoint、sample size、变量、数据结构或统计模型；
- 多轮修订无实质增益；
- 最新 proposal / SAP 版本缺少独立评价。

### 档位参数设计

`proposal-review-panel` 支持三档 panel：

| 档位 | Reviewer 数 | 适用场景 | 默认角色 |
| --- | ---: | --- | --- |
| `lightweight_panel` | 3 | 快速预审、早期 mock review、小规模 critique | domain expert、methodology/statistics、submission-guard |
| `standard_panel` | 5 | 默认档位，常规 proposal mock review | broad-field、domain expert、methodology/statistics、skeptical、submission-guard |
| `full_panel` | 7 | 高风险、高投入或接近正式提交的 proposal | standard 角色 + cross-disciplinary senior、translational/end-user |

医学、临床实践或公共卫生相关 proposal 中，domain expert 默认由 `practicing-clinician reviewer` 承担。`submission-guard reviewer` 必须保留；`skeptical reviewer` 默认启用，除非用户明确关闭。

### 产出结构

典型目录和文件包括：

- `context-brief`
- `evidence-map` / `opportunity-map`
- `readiness-report`
- `proposal-vNNN.md`
- `evaluation-vNNN.md`
- `revision-plan-rNNN.md`
- `revision-delta-rNNN.md`
- `response-to-reviewers-rNNN.md`
- `panel-summary`
- `sap-vNNN.md`
- `sap-evaluation-vNNN.md`
- `final-proposal-package`
- workflow state / artifact index

最终 package 必须保留 unresolved issues、dissenting reviewer opinions 和版本血缘，不能把不确定性“清洗掉”。

## `research-article/`：论文写作与投稿包工作流

### 目标

从研究数据、结果、方法描述、图表、参考文献和目标期刊信息出发，构建 evidence-constrained manuscript，并完成方法学审查、claim audit、独立评价、修订、模拟审稿、frontmatter 和 submission package。

### 主要角色

| 技能 | 角色 | 不能做什么 |
| --- | --- | --- |
| `article-orchestrator` | 总控论文工作流、维护 state、调度隔离 auditor/evaluator/reviewer | 不替代 reviewer/evaluator 评分 |
| `article-readiness-triage` | 判断研究是否具备进入写作系统的最低条件 | 不写稿 |
| `article-context-builder` | 标准化研究设计、结果、方法、目标期刊、reporting standard | 不凭空补数据 |
| `article-literature-grounder` | 检索和定位文献、评估 novelty、记录 citation risk | 不替代 manuscript drafter |
| `article-methods-statistics-auditor` | 写作前审查方法与统计是否支持主要推断 | 不用文字修补真实方法学缺陷 |
| `article-architect` | 构建 blueprint、claim-evidence matrix、evidence provenance ledger、display plan | 不直接写完整稿件 |
| `article-drafter` | 根据 blueprint 起草正文和修订稿 | 不做独立评价 |
| `article-claim-auditor` | 检查每个 claim 是否被证据支持 | 不替代 drafter 改稿 |
| `article-evaluator` | 综合评价科学性、证据-主张一致性、报告完整性、语言、期刊匹配等 | 不修改 manuscript |
| `article-refinement-controller` | 控制修订模式、response、delta report 和再评价 | 不伪造外部行动 |
| `article-review-panel` | 多角色模拟同行评审 | reviewer 之间保持隔离 |
| `article-frontmatter-drafter` | Draft abstract, title options, key points, running title, highlights | Does not draft cover letter or change core conclusions |
| `article-cover-letter` | Draft standalone journal cover letter; for biomedical papers run cover-letter-only `medical-journal-review` tier assessment | Does not draft frontmatter, modify manuscript, or provide manuscript text to the cover-letter reviewer |
| `article-submission-compositor` | 组装 submission package 并做投稿前核查 | 不重写正文或掩盖 unresolved items |

### 标准流程

```text
article-context-builder
  -> article-readiness-triage
  -> article-literature-grounder
  -> article-methods-statistics-auditor
  -> article-architect
  -> article-drafter
  -> article-claim-auditor
  -> article-evaluator
  -> article-refinement-controller
  -> article-review-panel
  -> article-frontmatter-drafter
  -> article-cover-letter
  -> article-submission-compositor
```

### 入口模式设计

`article-orchestrator` 支持多种 entry mode：

| 模式 | 用途 |
| --- | --- |
| `standard` | 从研究输入开始跑完整论文工作流 |
| `fast_track_has_draft` | 用户已有草稿，但仍需补齐上下文、证据、方法学和评价门 |
| `fast_track_draft_eval` | 重点对已有稿件做评价和修订路由 |
| `blueprint_only` | 只产出论文架构、claim-evidence matrix、display plan 等 |
| `section_specific` | 只处理 Introduction、Methods、Discussion 等局部章节 |
| `submission_only` | 已有稿件基本完成，只做投稿包组装和提交前核查 |

Fast-track 模式不能跳过最低 backfill gate。若参考文献、结果一致性、期刊要求或伦理声明没有完全核查，最终状态不能超过 `ready_for_author_check`。

### Panel 档位与模式

`article-review-panel` 的结构包括：

- `panel_mode`: `blind_external_simulation` 或 `internal_diagnostic_review`
- `panel_tier`: `lightweight`、`standard`、`full`

盲审模拟模式下 reviewer 只看稿件和角色说明，不看 context brief、evaluation report、blueprint 或其他 reviewer 输出。内部诊断模式可以看到更多材料，用于区分“稿件没写清楚”和“研究设计本身有问题”。

### 任务循环设计

论文修订循环：

```text
manuscript-vNNN
  -> claim-auditor / evaluator
  -> article-refinement-controller
  -> revision-plan-rNNN
  -> article-drafter revision
  -> response-to-reviewers-rNNN
  -> revision-delta-rNNN
  -> re-audit / re-evaluation / panel / compositor
```

修订模式包括：

- `textual_revision`
- `structural_revision`
- `evidence_relinking`
- `reporting_completion`
- `claim_downscaling`
- `methods_detailing`
- `journal_retargeting`
- `language_polishing`

若需要重新分析、补数据、重做研究设计或修复不可由写作解决的方法学缺陷，流程必须停止并返回给用户，而不是用文字修补。

### 产出结构

典型产物包括：

- Minimal Intake Summary
- Article Readiness Report
- Article Context Brief
- Literature Grounding Report
- Methods Audit Report
- Article Blueprint
- Evidence Provenance Ledger
- Manuscript Draft
- Claim Audit Report
- Article Evaluation Report
- Revision Plan
- Response to Reviewers
- Revision Delta
- Panel Report
- Frontmatter
- Cover Letter
- Submission Package

投稿包状态包括：

- `ready_for_author_signoff`
- `ready_for_author_check`
- `minor_revision_pending`
- `major_revision_required`
- `blocked`
- `partial`

`ready_for_author_signoff` 需要满足独立评价、参考文献核查、表图结果一致性、期刊要求核查、伦理声明完整性等条件。

## `research-perspective/`：Perspective / Viewpoint / Commentary 工作流

### 目标

从一个核心观点或争议判断出发，构建 claim ledger、证据边界、论证骨架、Perspective 初稿、独立评价、修订、模拟 panel 和终稿合规检查。

### 主要角色

| 技能 | 角色 | 不能做什么 |
| --- | --- | --- |
| `perspective-orchestrator` | 总控 Perspective 工作流，选择 Lite / Standard / Full 模式 | 不替代 evaluator 或 panel reviewer |
| `perspective-input-builder` | 生成输入模板、读取用户填写内容、产出 Input Brief 和 Target Outlet Profile | 不直接写全文 |
| `perspective-claim-evidence-curator` | 维护 claim ledger、claim-evidence matrix、citation risk、contrary evidence | 不写 narrative 正文 |
| `perspective-argument-architect` | 构建问题场、贡献类型、论证链、反方预埋和 contestability 约束 | 不写完整文章 |
| `perspective-drafter` | 将论证骨架转成正文，段落映射到 argument step + claim ID | 不改写 claim ledger 的事实基础 |
| `perspective-evaluator` | 独立评价文章质量、论证、证据、叙事和合规风险 | 不修稿 |
| `perspective-refinement-controller` | 控制定向修订、delta report、caveat budget 和停止规则 | 不直接代替 panel |
| `perspective-review-panel` | Counter-position、Evidence、Narrative 等隔离 reviewer 角色 | reviewer 之间不共享输出 |
| `perspective-final-compositor` | 做 journal-fit、citation、title-abstract、anti-pattern、claim consistency 终稿检查 | 只做非实质编辑，不能解决实质缺陷 |

### 模式档位设计

`perspective-orchestrator` 支持三档：

| 模式 | 适用场景 | 路由 | 典型产出 |
| --- | --- | --- | --- |
| `Lite` | “帮我理一下思路”“这个方向能不能写成 Perspective” | STEP 1 -> STEP 2-lite -> STEP 3 | input brief、provisional claim-ledger、最小 claim-evidence matrix、argument skeleton、early feasibility report |
| `Standard` | “帮我写一篇 Perspective 初稿” | STEP 1 -> STEP 2 -> STEP 3 -> STEP 4 -> STEP 5 -> STEP 6 一轮 | draft-v1/v2、完整 claim-ledger、evaluation report、delta report、response |
| `Full` | “要投 X 刊”或需要投稿前检查 | 完整 STEP 1 到 STEP 9 | final manuscript、panel summary、final compositor report、submission readiness |

Lite 模式不启动完整外部检索，只显式标注 evidence gap。Standard 默认只进行一轮 refinement。Full 需要明确目标 outlet；若只有 generic profile，不能直接声明 ready for submission。

### 标准流程

```text
perspective-input-builder
  -> perspective-claim-evidence-curator
  -> perspective-argument-architect
  -> perspective-drafter
  -> perspective-evaluator
  -> perspective-refinement-controller
  -> perspective-review-panel
  -> perspective-final-compositor
```

### 任务循环设计

Perspective 修订循环：

```text
draft-vNNN
  -> perspective-evaluator
  -> perspective-refinement-controller
  -> perspective-drafter revision
  -> revision-delta
  -> isolated re-evaluation
  -> panel / final compositor / stop
```

Panel 后循环通常限制更严：若 panel 返回 `support_after_major_revision`，最多进行一轮 panel -> revise -> panel，避免无限打磨。

### 产出结构

典型目录包括：

- `00_input/`
- `01_claims/`
- `02_evidence/`
- `03_skeletons/`
- `04_drafts/`
- `05_evaluations/`
- `06_revisions/`
- `07_panel/`
- `08_final/`
- `09_state/`
- `10_delegates/`

典型文件包括：

- `01-input-brief.md`
- `target-outlet-profile.md`
- `claim-ledger.md`
- `claim-evidence-matrix.md`
- `evidence-limitations.md`
- `existing-discourse-baseline.md`
- `argument-skeleton.md`
- `draft-vNNN.md`
- `evaluation-report.md`
- `revision-delta-rNNN.md`
- `response-to-reviewers-rNNN.md`
- `panel-summary.md`
- `final-compositor-report.md`

## 角色设计总览

research 系列技能整体上分成六类角色。

| 角色类型 | 代表技能 | 职责 | 关键边界 |
| --- | --- | --- | --- |
| Orchestrator | `research-idea-orchestrator`、`proposal-orchestrator`、`article-orchestrator`、`perspective-orchestrator` | 选择模式、调度技能、维护状态、控制循环、执行 stop rule | 不替代 evaluator/reviewer 评分 |
| Builder / Curator | context builder、claim curator、literature grounder、architect | 结构化输入、维护证据、构建蓝图 | 不越权生成最终评分或结论 |
| Generator / Drafter | idea generator、proposal drafter、article drafter、perspective drafter、SAP writer | 生成候选 idea 或文本产物 | 不评价自己生成的内容 |
| Auditor / Evaluator / Triage | readiness triage、methods auditor、claim auditor、proposal/article/perspective/idea evaluator | 应用 hard gate、评分、指出 fatal flaw | 不起草、不重写、不降低标准 |
| Review Panel | proposal/article/perspective review panel、idea adversarial panel | 多角色模拟审稿或 handoff 攻击 | reviewer 互相隔离，聚合时不能制造虚假共识 |
| Assembler / Compositor | portfolio assembler、proposal package assembler、article submission compositor、perspective final compositor | 汇总、组装、检查完整性 | 不清洗 unresolved issues，不掩盖 dissent |

## 任务循环设计总览

所有核心工作流都采用类似的闭环：

```text
输入标准化
  -> 证据 / 方法 / 结构预处理
  -> 生成或起草
  -> 独立评价
  -> 定向修订
  -> 再评价或 panel
  -> 最终组装
```

循环控制依赖以下机制：

- Hard gate：阻断不可行任务，而不是继续生成。
- Revision plan：把 evaluator / reviewer 的问题转成可执行修订项。
- Response file：逐条解释如何处理评审意见。
- Delta report：记录本轮变化、未解决问题和新增风险。
- Re-evaluation：实质性修改后必须重新独立评价。
- Stop rule：当修改无增益、需要外部数据、需要重做分析、或存在不可修复 fatal flaw 时停止。

## 档位参数设计总览

### Workflow Mode

用于控制完整度和成本。

| 参数 | 出现位置 | 含义 |
| --- | --- | --- |
| `Lite` | Perspective | 快速可行性和论证骨架，不做完整检索和投稿前检查 |
| `Standard` | Perspective / 默认工作流 | 完整初稿或标准生产流程，通常带一轮修订 |
| `Full` | Perspective / 高投入场景 | 完整投稿前流程，包含 panel 和 final compositor |
| `standard` | Article entry mode | 从研究材料开始完整跑论文流程 |
| `fast_track_*` | Article entry mode | 已有草稿或只需评价/补齐关键 gate |
| `blueprint_only` | Article entry mode | 只产出论文架构，不写全文 |
| `section_specific` | Article entry mode | 只处理局部章节 |
| `submission_only` | Article entry mode | 只做投稿包组装和投稿前检查 |

### Panel Tier

用于控制 reviewer 数量和审查强度。

| 参数 | 出现位置 | 含义 |
| --- | --- | --- |
| `lightweight_panel` / `lightweight` | Proposal / Article panel | 小规模快速审查 |
| `standard_panel` / `standard` | Proposal / Article panel | 默认强度 |
| `full_panel` / `full` | Proposal / Article panel | 高强度、多角色审查 |

### Status / Gate

用于控制流程能否继续。

常见状态包括：

- `ready`
- `conditionally_ready`
- `not_ready`
- `blocked`
- `revise`
- `reject`
- `stop_no_gain`
- `ready_for_author_check`
- `ready_for_author_signoff`

## 产出结构总览

### 面向用户的 Markdown 产物

这些是用户直接阅读和使用的主要成果：

- Context Brief
- Evidence Map
- Opportunity Map
- Generated Idea Set
- Research Idea Portfolio
- Proposal Draft
- SAP
- Manuscript Draft
- Perspective Draft
- Evaluation Report
- Review Panel Summary
- Revision Plan
- Revision Delta Report
- Response to Reviewers
- Final Package / Submission Package

### 面向 agent 协作的状态结构

这些结构用于跨技能传递状态：

- workflow state
- artifact index
- schema version
- artifact ID
- source skill
- based_on
- change_type
- version / round
- scope limitations
- unresolved issues
- independence status
- verification status

### 目录命名原则

工作流产物通常放在用户项目目录中，而不是技能包目录中。目录名带数字前缀，用于保持顺序和可追踪性，例如：

```text
00_input/
01_context/
02_evidence/
03_literature/
04_blueprint/
05_methods/
06_drafts/
07_audits/
08_evaluations/
09_revisions/
10_panel/
11_frontmatter/
12_package/
13_state/
```

不同技能包会有自己的目录编号，但共同原则是：不要跳过版本号，不要覆盖旧版本，不要把修订后的产物伪装成原始产物。

## 当前审查结论

已运行核心一致性审计：

```bash
python scripts/audit_research_workflows.py
```

当前结果：

```text
errors: 0
warnings: 8
```

通过的硬性检查包括：

- 核心 research 工作流包存在；
- `related_skills` 引用可解析；
- evaluator / reviewer / auditor / triage 角色具备隔离和禁止越权的说明；
- orchestrator 包含 artifact governance、language governance 和 lineage 字段；
- Markdown 引用文件存在；
- research-article 的投稿包、修订、panel、状态字段和 dry-run 路由一致；
- 没有残留的旧 shared-skill 引用。

8 个 warning 都是 `SKILL.md` 文件超过 300 行的长度提醒。后续维护建议是继续把长示例、边界条件和 checklist 下沉到 `references/`，让 `SKILL.md` 更像激活时使用的操作手册，而不是百科式总文档。

## 维护命令

运行 research 工作流审计：

```bash
python scripts/audit_research_workflows.py
```

查看所有技能入口：

```bash
rg --files -g SKILL.md research-skills
```

生成 flatten skills 元数据：

```bash
python generate_flatten_skills.py
```

## 维护原则

- `research-skills/` 是当前唯一主要维护源。
- 不要随意重命名 skill 前缀，例如 `article-*` 不应改成 `research-article-*`。
- evaluator、auditor、reviewer、triage、final-compositor 等评价型角色必须保持隔离。
- drafter / writer 不应评价自己的产物。
- assembler / compositor 只做组装和核查，不负责偷偷修稿。
- 任何实质性文本、方法、证据或结论变化，都应留下 revision delta 和 lineage。
- 对已经成为流程依赖的规则，应同步加入审计脚本，避免后续重构破坏工作流。
