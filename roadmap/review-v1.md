下面是我的评估。结论先说：**这个架构方向是对的，而且已经超过普通“写作助手”层级；它更像一个 manuscript production system。** 但现在的问题是：它仍然把“写作”放在中心，而真实的顶级论文生产更应该把 **证据治理、主张约束、报告规范、期刊适配、审稿风险控制** 放在中心。

你现在的设计已经明确区分了 `research-proposal` 和 `research-article` 的起点、目标和产出，并把 Article 系列定位为“已有数据、结果、研究设计 → manuscript + cover letter + 审稿预案”，这是合理的基本定位。你还把底层模型抽象为 **Question → Design → Evidence → Inference → Boundary → Meaning**，并用 **Claim–Evidence Matrix** 和 **Evidence Display Plan** 替代单纯 Figure Plan，这些是该设计中最有价值的部分。

------

# 一、总体评价

## 1. 架构方向正确

你现在的设计不是简单的“帮我写论文”，而是一个完整 pipeline：

> Context Brief → Blueprint → Draft → Evaluation → Refinement → Review Panel → Compositor

这个顺序基本成立。尤其是你把 `article-context-builder`、`article-architect`、`article-drafter`、`article-evaluator`、`article-refinement-controller`、`article-review-panel`、`article-compositor` 分开，说明你已经意识到写作、评估、修订、模拟审稿不能混成一个 agent。文档中对 drafter、evaluator、review panel 的隔离规则也写得比较清楚。

## 2. 底层理念比普通论文写作模板强

你没有把某一种论文模板，例如 Nature 机制论文或 JAMA 临床论文，当作通用模式，而是提出了：

> 通用规律 → 研究类型规范 → 期刊风格

这很重要。EQUATOR 官方也强调报告规范是针对特定研究类型开发的 checklist、flow diagram 或 structured text，用于指导作者报告相应研究类型，而不是所有研究共用一个写作模板。([EQUATOR Network](https://www.equator-network.org/about-us/what-is-a-reporting-guideline/?utm_source=chatgpt.com))

## 3. 最大优点是 Evidence Display Plan

你把 Figure Plan 升级成 Evidence Display Plan 是正确的。医学、AI、工程、社会科学、系统综述、机制研究、定性研究的证据呈现载体都不同。把图、表、文字、补充材料、代码仓库、数据说明统一看成 evidence display，是这个技能包最有原创价值的部分。

------

# 二、最重要的问题

## 问题 1：缺少一个独立的 “Article Readiness / Triage” 阶段

你现在的第一步是 `article-context-builder`。它负责输入标准化、识别研究类型、匹配报告规范、识别缺口和不确定性。这个角色太重。

在真实论文生产中，最早应该先判断：

> 这项研究是否已经具备“可写成 manuscript”的最低条件？

这和 context building 不是一回事。

建议新增：

```text
article-readiness-triage/
```

职责：

1. 判断是否已经有足够材料进入写作；
2. 判断是 full article、short report、research letter、brief communication、data descriptor、methods article，还是不应写成 original article；
3. 判断是否存在阻断性缺陷；
4. 判断需要回到分析阶段、补实验、补数据、补文献，还是可以进入 blueprint；
5. 判断用户目标是否现实，例如“Nature 主刊”是否明显不匹配。

建议输出：

```yaml
article_readiness_report:
  readiness_status: ready | conditionally_ready | not_ready | wrong_article_type
  recommended_article_type: original_article | brief_report | research_letter | methods_article | data_descriptor | case_report | review | other
  blocking_gaps:
    - gap: ""
      why_blocking: ""
      required_action: ""
  nonblocking_gaps:
    - gap: ""
      mitigation: ""
  minimum_inputs_present:
    research_question: true
    study_design: true
    primary_results: true
    methods_details: true
    ethics_info: false
    figures_tables: false
    references: false
  recommended_route: blueprint | methods_preflight | data_analysis | literature_review | stop
```

这个 triage 很关键。否则 skill 会在材料不足时“硬写”，最后生成看起来完整但实际上不可投稿的稿件。

------

## 问题 2：Context Builder 不应该承担过多判断责任

现在 `article-context-builder` 同时做：

- 研究类型识别；
- 报告规范匹配；
- PICO/PECO/SPIDER 提取；
- 数据缺口识别；
- 不确定性识别；
- proceed / clarification_stop 判断。

这会导致它既是 parser，又是 classifier，又是 evaluator。

建议拆成三层：

```text
article-intake-normalizer
article-study-type-classifier
article-reporting-standard-selector
```

或者保留一个 skill（推荐），但内部明确三步：

1. **Normalize**：把用户输入标准化；
2. **Classify**：识别研究类型、文章类型、报告规范；
3. **Gate**：判断是否可继续。

EQUATOR 的数据库支持按 study type、clinical area 和 report section 查找报告规范，而不是简单的一对一映射；它还提供选择合适 reporting guideline 的工具和流程。([EQUATOR Network](https://www.equator-network.org/reporting-guidelines/?utm_source=chatgpt.com))
因此，报告规范映射不应只写死为 “RCT → CONSORT，观察性 → STROBE”。应该允许：

- 多规范并用；
- extension 优先；
- 期刊特定要求覆盖默认规范；
- 研究设计混合时的主规范 + 辅助规范；
- 没有合适规范时标记 `no_exact_guideline_found`。

------

## 问题 3：缺少 Evidence Provenance Ledger

这是目前最需要补的模块。

你已经有 Claim–Evidence Matrix，但还不够。因为 manuscript drafting 最大风险不是结构不清，而是：

> 某个主张在正文中出现了，但没有明确来源、数据支撑或引用支撑。

建议新增：

```text
evidence-provenance-ledger
```

它可以作为 `_shared` contract，也可以内嵌到 Blueprint 和 Draft。

建议字段：

```yaml
evidence_provenance_ledger:
  - evidence_id: "E001"
    evidence_type: primary_data | secondary_data | experiment | statistical_result | literature_reference | user_assertion | assumption
    source_location: ""
    source_file: ""
    source_table_or_figure: ""
    numeric_values:
      estimate: ""
      ci: ""
      p_value: ""
      sample_size: ""
    supports_claims: ["C001"]
    appears_in:
      manuscript_section: "Results"
      paragraph_id: "R-P03"
      display_id: "D001"
    verification_status: verified | user_supplied_unverified | inferred | missing
    risk_level: low | medium | high
```

这个 ledger 能解决三个问题：

1. 防止 hallucinated result；
2. 防止 conclusion 超出 evidence；
3. 让 evaluator 能逐条追踪 manuscript 里的主张是否有支撑。

Nature Portfolio 的报告政策也强调材料、数据、代码和相关 protocol 应能被读者获取，以便他人复制和建立在作者主张之上。这个原则对你的 skill 包设计很有启发：论文系统不仅要“写得好”，还要让主张可追踪、可审查、可复核。([Nature](https://www.nature.com/nature-portfolio/editorial-policies/reporting-standards?utm_source=chatgpt.com))

------

## 问题 4：Compositor 的职责存在内部冲突

你写道：

> article-compositor 只组装已有产物，不得重写、修补、重新评分或隐藏未解决问题。

但同一部分又写：

> 生成/优化 Abstract、Key Points、Title、Cover Letter、Reviewer Risk Matrix。

这其实是实质性写作，不是单纯组装。

建议拆成两个 skill：

```text
article-frontmatter-drafter/
article-submission-compositor/
```

其中：

## `article-frontmatter-drafter`

负责：

- Abstract；
- Key Points；
- Title；
- Running title；
- Highlights；
- Graphical abstract text；
- Cover letter 初稿。

它可以重写，但必须受 Blueprint、Evaluation、Panel Report 约束。

## `article-submission-compositor`

只负责：

- 组装；
- 格式核对；
- checklist；
- 文件清单；
- 未解决问题标记；
- submission readiness summary。

这样职责才一致。

------

## 问题 5：Results 的二分法仍然偏粗

你现在将 Results 组织方式分为：

- `norm_driven`
- `argument_driven`

这个比之前更好，但仍然不够。

更准确的分类至少应包括：

```yaml
results_organization_mode:
  primary: norm_driven | argument_driven | hybrid | artifact_driven | theory_driven | evidence_synthesis_driven
```

建议扩展如下：

| 类型                        | 适用场景                                          | Results 逻辑                        |
| --------------------------- | ------------------------------------------------- | ----------------------------------- |
| `norm_driven`               | RCT、观察性、诊断、预测、系统综述                 | 按规范、对象、终点、预设分析报告    |
| `argument_driven`           | 机制、转化、发现型研究                            | 按主张递进                          |
| `hybrid`                    | 临床 + 机制子研究、RCT + biomarker、AI + 临床验证 | 主研究按规范，子研究按论证          |
| `artifact_driven`           | 数据资源、软件、工具、方法平台                    | 构建 → 验证 → 用例 → 可复用性       |
| `theory_driven`             | 理论、模型、数学推导、人文学术论文                | 概念 → 命题 → 证明/解释 → 边界      |
| `evidence_synthesis_driven` | 系统综述、scoping review、umbrella review         | 文献流 → 证据图谱 → 质量 → 综合结论 |

尤其是 AI/ML，不应默认 `argument_driven`。很多 AI 医学模型论文本质是 `norm_driven + benchmark_driven + validation_driven`。如果是 clinical prediction，则应受 TRIPOD 类规范约束；如果是基础算法，则按 benchmark / ablation / generalization 组织。

------

# 三、建议新增的核心 skill

我建议将架构调整为下面版本。

```text
research-article/
  research-article-orchestrator/
  article-readiness-triage/             # 新增：判断是否可进入写作
  article-context-builder/              # 输入标准化
  article-reporting-standard-selector/  # 新增或内嵌：规范选择
  article-literature-grounder/          # 新增：文献定位和引用支撑
  article-architect/                    # 论文架构
  article-evidence-display-planner/     # 可从 architect 拆出
  article-methods-statistics-auditor/   # 新增：方法与统计预审
  article-drafter/                      # 正文起草
  article-claim-auditor/                # 新增：主张—证据逐条核查
  article-evaluator/                    # 独立质量评估
  article-refinement-controller/        # 修订控制
  article-review-panel/                 # 模拟审稿
  article-frontmatter-drafter/          # 新增：摘要、标题、Key Points、Cover Letter
  article-submission-compositor/        # 只组装，不重写
  _shared/
```

其中最值得优先新增的是四个：

1. `article-readiness-triage`
2. `article-literature-grounder`
3. `article-claim-auditor`
4. `article-frontmatter-drafter`

------

# 四、需要加强的 artifact contract

## 1. Manuscript Draft 需要包含正文内容，而不只是状态

你现在的 `manuscript_draft` 主要记录 section status、word count、figures、tables、references_count。这个更像 metadata，而不是 draft artifact。

建议改成：

```yaml
manuscript_draft:
  draft_id: "manuscript-v001"
  sections:
    title_page:
      content: ""
      status: drafted
    abstract:
      content: ""
      status: pending
    introduction:
      content: ""
      word_count: 0
      claim_ids: []
    methods:
      content: ""
      word_count: 0
      reporting_items_covered: []
    results:
      content: ""
      word_count: 0
      display_ids: []
      claim_ids: []
    discussion:
      content: ""
      word_count: 0
      claim_ids: []
    references:
      entries: []
  paragraphs:
    - paragraph_id: "R-P01"
      section: "Results"
      text: ""
      supported_by:
        claims: ["C001"]
        evidence: ["E001"]
```

如果每个段落能挂接 `claim_id` 和 `evidence_id`，后续 evaluation 会强很多。

------

## 2. Figure / Table 需要独立 metadata

现在 `figures: []` 和 `tables: []` 太粗。

建议定义：

```yaml
display_item:
  display_id: "D001"
  type: table | figure | flow_diagram | forest_plot | model_diagram | supplementary_table
  title: ""
  legend_or_caption: ""
  supported_claims: ["C001"]
  evidence_ids: ["E001"]
  source_data: ""
  placement: main | supplementary
  required_by_reporting_guideline: true
  journal_limit_impact: ""
  status: planned | drafted | final | missing
```

这样 EDP 可以落地到实际 manuscript。

------

## 3. Reporting checklist 应该从 status 变成 item-level mapping

现在只有：

```yaml
reporting_checklist_status: pending | attached | not_applicable
```

建议改为：

```yaml
reporting_checklist_mapping:
  standard: "STROBE"
  items:
    - item_id: "STROBE-01"
      requirement: "Title and abstract"
      manuscript_location: "Title; Abstract"
      status: satisfied | partial | missing | not_applicable
      notes: ""
```

原因是报告规范不应只在最后“附上 checklist”。它应该约束 Methods、Results、Abstract 的内容。EQUATOR 明确把 reporting guideline 定义为列出论文中应出现的报告项目的结构化工具，这与 item-level mapping 的思路一致。([EQUATOR Network](https://www.equator-network.org/about-us/what-is-a-reporting-guideline/?utm_source=chatgpt.com))

------

## 4. Journal Adapter 需要可审计来源

你现在的 `journal_adapter` 有：

- abstract structure；
- figure/table limits；
- Results 小标题风格；
- Discussion 长度；
- Cover Letter 侧重点。

建议增加：

```yaml
journal_adapter:
  target_journal: ""
  source_checked_date: ""
  source_documents:
    - type: author_instructions
      location: ""
      retrieval_status: verified | user_supplied | not_checked
  constraints:
    word_limit: ""
    figure_limit: ""
    table_limit: ""
    abstract_format: ""
    data_availability_policy: ""
    code_availability_policy: ""
    reporting_guideline_policy: ""
  confidence: high | medium | low
```

因为期刊说明会更新。ICMJE recommendations 当前页面显示其建议有 2026 年 1 月更新版本；这类外部规范应作为动态信息处理，而不是写死在 skill 中。([icmje.org](https://www.icmje.org/recommendations/?utm_source=chatgpt.com))

------

# 五、Evaluation 体系需要调整

## 1. 不建议使用 simple average 作为 overall score

你现在有：

```yaml
overall_score_simple_average: 0
```

这在论文评估中不可靠。原因是某些维度是 hard gate，不应被平均分抵消。

例如：

- Scientific validity = 2/10；
- Clarity = 9/10；
- Contribution = 9/10。

平均分可能还不错，但文章不能投稿。

建议改成：

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
```

也就是说，关键维度应是 **non-compensatory**，不能平均。

------

## 2. Hard Gates 需要分层

你现在的 hard gates 很好，但可以分为三类：

### A. Fatal scientific gates

失败后不应继续写作：

- 研究问题不可回答；
- 核心变量/终点定义不清；
- 主要结论没有数据；
- 研究设计不能支持主要推断；
- 统计分析存在不可修复缺陷。

### B. Reporting gates

失败后可以修：

- checklist 缺项；
- Methods 描述不完整；
- 图表说明不清；
- 缺少伦理、数据可用性、代码可用性说明。

### C. Genre / rhetoric gates

失败后通过重写修：

- 观察性研究写成因果；
- Results 过度解释；
- Discussion 过度教学化；
- 过度宣传化；
- 口吻不符合期刊。

建议 evaluator 输出时明确：

```yaml
gate_failures:
  fatal_scientific: []
  reporting: []
  genre_rhetoric: []
```

这样 refinement-controller 才知道是“补方法/补分析”还是“改写文本”。

------

## 3. 增加 Claim-Level Evaluation

现在 evaluator 是整篇文章六维评分。建议增加 claim-level 审计：

```yaml
claim_level_evaluation:
  - claim_id: "C001"
    claim_text: ""
    evidence_support: strong | moderate | weak | absent
    inference_validity: valid | overstated | invalid
    wording_status: appropriate | overclaimed | underclaimed
    required_revision: ""
```

这会显著提升评估精度。

------

# 六、Refinement Loop 需要更精确

你设置默认最多 2 轮，这是合理的。但需要区分修订类型。

建议 refinement-controller 先分类：

```yaml
revision_mode:
  - textual_revision
  - structural_revision
  - evidence_relinking
  - reporting_completion
  - claim_downscaling
  - methods_detailing
  - journal_retargeting
  - analysis_required
  - study_redesign_required
```

如果是 `analysis_required` 或 `study_redesign_required`，skill 不应该假装能通过写作解决。

这点非常重要。否则系统会把“研究本身的问题”误处理成“文字问题”。

------

# 七、Review Panel 的盲审规则需要微调

你现在的 blind mock review 规则是：

> reviewer 只接收 manuscript file + user goal + target journal + reviewer role/scope，不接收 context brief、evaluation report、revision delta、unresolved issues、blueprint。

这个原则正确，但需要补一个例外：

## Methodology / Statistics Reviewer 需要部分 protocol-level 信息

如果 manuscript 本身 Methods 写得不完整，method reviewer 只看稿件是合理的，因为真实审稿人也只看稿件。但如果你的目标是内部改进，而不是模拟真实外审，则 method reviewer 应该有两种模式：

```yaml
reviewer_mode:
  blind_external_simulation:
    input: manuscript_only
  internal_diagnostic_review:
    input: manuscript + context_brief + protocol_or_sap + tables
```

否则 panel 只能指出“Methods 不清楚”，但不能判断“用户原始研究设计是否真的有问题”。

所以建议保留两种 panel：

1. **Blind Mock Review**：模拟投稿后外审；
2. **Internal Diagnostic Review**：用于投稿前深度修稿。

你已经有 `blind_mock_review | context_aware_internal_review`，但需要明确不同 reviewer 在两种模式下的输入边界。

------

# 八、需要增加 Literature Grounding

你现在把文献检索放在上游依赖里，提到 `research/research-opportunity-mapper` 可在 Discussion 比较文献时使用。

这不够。

对 manuscript 来说，文献不是附属材料，而是以下部分的基础：

- Introduction 的 gap；
- Discussion 的 comparison；
- novelty claim；
- clinical / scientific significance；
- target journal fit；
- reviewer risk；
- overclaim control。

建议新增：

```text
article-literature-grounder/
```

输出：

```yaml
literature_grounding_report:
  key_background_claims:
    - claim: ""
      references: []
      manuscript_location: "Introduction"
  novelty_position:
    prior_work_summary: ""
    what_is_new: ""
    what_is_not_new: ""
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
```

这可以防止两类常见问题：

1. Introduction 的空白是伪空白；
2. Discussion 的新颖性被审稿人轻易否定。

------

# 九、期刊适配层需要从“风格分类”升级为“约束系统”

你现在的期刊风格分类有用，但容易变成静态描述。建议把 `journal_adapter` 分成三类约束：

## 1. Hard Constraints

必须满足：

- article type；
- word limit；
- abstract format；
- figure/table limits；
- reference limits；
- reporting checklist；
- trial registration；
- data availability；
- code availability；
- ethics statement；
- conflict of interest；
- author contribution taxonomy。

ICMJE 对医学期刊投稿准备、表格、图、参考文献、利益冲突等都有通用建议，而具体期刊还会有自己的 author instructions；因此期刊适配层应该从这些要求生成 submission checklist，而不是只做风格描述。([icmje.org](https://www.icmje.org/recommendations/browse/manuscript-preparation/preparing-for-submission.html?utm_source=chatgpt.com))

## 2. Soft Style Preferences

可以影响写作：

- Results 小标题风格；
- Discussion 长度；
- Cover letter 侧重点；
- 是否偏好 clinical relevance；
- 是否偏好 conceptual advance；
- 是否偏好 transparency / reproducibility。

## 3. Strategic Fit

决定是否值得投：

- scope fit；
- novelty threshold；
- article type fit；
- audience fit；
- likely desk rejection risks。

建议增加：

```yaml
journal_fit_assessment:
  fit_level: high | moderate | low | poor
  likely_editorial_screening_risks: []
  recommended_retargeting:
    primary: ""
    alternatives: []
```

------

# 十、你的研究类型矩阵需要扩展

目前矩阵主要覆盖医学、机制、组学、AI/ML、定性、工程、数据资源。建议再加入：

| 研究类型                            | 建议模式                  | 常见 EDP                                                     |
| ----------------------------------- | ------------------------- | ------------------------------------------------------------ |
| scoping review                      | evidence_synthesis_driven | search flow、evidence map、theme table                       |
| umbrella review                     | evidence_synthesis_driven | review characteristics、overlap matrix、certainty summary    |
| realist review                      | theory_driven / synthesis | context–mechanism–outcome matrix                             |
| implementation study                | norm_driven / hybrid      | setting、implementation strategy、adoption/fidelity/outcome  |
| health economics                    | norm_driven               | cost table、ICER、sensitivity analysis、acceptability curve  |
| causal inference / quasi-experiment | norm_driven / causal      | DAG、event study、balance、placebo、robustness               |
| survey instrument validation        | norm_driven               | factor structure、reliability、validity、measurement invariance |
| psychometric study                  | norm_driven               | item analysis、CFA/EFA、reliability、validity                |
| qualitative evidence synthesis      | synthesis                 | study selection、themes、confidence in evidence              |
| historical / humanities article     | theory_driven             | source corpus、timeline、case evidence、counterargument      |
| legal / policy analysis             | argument_driven           | doctrine/policy framework、case table、comparative matrix    |

这能让 Article 系列真正脱离“医学论文助手”的限制。

------

# 十一、建议修改后的标准流程

我建议标准流程改成：

```text
1. Article Readiness Triage
2. Context Brief
3. Reporting Standard & Journal Requirement Selection
4. Literature Grounding
5. Article Blueprint
6. Claim–Evidence Matrix
7. Evidence Display Plan
8. Methods / Statistics Audit
9. Manuscript Drafting
10. Claim-Level Audit
11. Independent Evaluation
12. Targeted Refinement
13. Mock Review Panel
14. Frontmatter Drafting
15. Submission Compositor
```

其中：

- **1–4** 是输入治理；
- **5–8** 是架构治理；
- **9** 是写作；
- **10–13** 是质量控制；
- **14–15** 是投稿交付。

这比当前流程更稳，因为它把“写作”推后，把“研究是否可写、主张是否可证、规范是否匹配”放在前面。

------

# 十二、对你现有设计的具体修改建议

## 建议 1：把“可直接投稿”改成更严谨的表述

原表述：

> 交付一份高质量、符合报告规范、可直接投稿的 manuscript。

建议改成：

> 交付一份 submission-ready manuscript package，所有未验证数据、缺失材料、作者需确认事项和不可由写作修复的方法学问题均明确标注。

原因：AI 或 skill 包不能替作者保证数据真实性、伦理合规、统计正确性和作者责任。它可以生成 submission-ready package，但必须保留 human verification gate。

------

## 建议 2：增加 Human Sign-off Gate

建议在最终 package 前加入：

```yaml
human_signoff_required:
  data_accuracy: true
  statistical_results_verified: true
  author_contributions_verified: true
  ethics_and_consent_verified: true
  conflicts_of_interest_verified: true
  journal_requirements_verified: true
```

这对真实投稿非常必要。

------

## 建议 3：把 “compositor” 降权

`article-compositor` 不应该“优化摘要和标题”。这会导致它越权。

建议：

```text
article-frontmatter-drafter → writes title/abstract/key points/cover letter
article-submission-compositor → packages and checks
```

------

## 建议 4：把 Reviewer Risk Matrix 提前

你现在把 Reviewer Risk Matrix 放在 compositor 阶段。太晚。

建议它在三个阶段出现：

1. **Blueprint 阶段**：初版风险；
2. **Evaluation 阶段**：证据与方法风险；
3. **Compositor 阶段**：最终投稿风险矩阵。

也就是说：

```yaml
reviewer_risk_matrix:
  stage: blueprint | post_evaluation | final_submission
```

------

## 建议 5：加入 “claim downscaling” 机制

很多论文修订不是补数据，而是降低主张强度。

例如：

- “X causes Y” → “X was associated with Y”
- “X predicts Y” → “X showed moderate discrimination in internal validation”
- “X is clinically useful” → “X may support risk stratification pending prospective validation”

建议 refinement-controller 支持：

```yaml
claim_revision_action:
  retain | strengthen | downscale | remove | move_to_discussion | move_to_supplementary
```

这比笼统的 revise 更实用。

------

# 十三、最终判断

你的设计已经有一个坚实的核心：

1. `research-article` 与 `research-proposal` 的边界清楚；
2. 三层结构“通用 → 类型特定 → 期刊特定”是正确方向；
3. **Question → Design → Evidence → Inference → Boundary → Meaning** 可以作为整个系统的底层逻辑；
4. Claim–Evidence Matrix 和 Evidence Display Plan 是最重要的核心 artifact；
5. 独立 evaluator 和 mock review panel 的隔离设计是必要的。

但要让它真正成为顶级 manuscript production system，需要补强五件事：

1. **前置 readiness triage**：先判断能不能写，而不是直接写；
2. **证据来源追踪**：每个主张都要能追溯到 evidence；
3. **文献 grounding**：Introduction、Discussion、novelty claim 不能靠泛化写作；
4. **方法/统计 gate**：写作不能掩盖设计和分析缺陷；
5. **compositor 职责拆分**：前置信息写作和最终组装不能混在一个 skill 里。

最关键的一句话是：

> `research-article` 不应被设计成“论文写作器”，而应被设计成“证据约束下的投稿级 manuscript 构建与审查系统”。

这样改之后，这套 Article 系列 skills 才能稳定支持 Nature/Science/JAMA/Lancet 级别论文，也能泛化到 AI、工程、社会科学、数据资源、理论论文等不同类型。