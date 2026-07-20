```yaml
review_id: language-assessment-I01-001-r005
reviewer_skill: academic-language-assessor
reviewer_instance_id: academic-language-assessor-v006-r005-fresh-01
workflow_id: RID-SEPSIS-CSM-20260717-001
round_id: r005
input_artifact_ids:
  - idea-dossier-I01-001-v006
  - reader-handoff-forward-001
input_versions:
  - v006
  - v001
input_bindings:
  - artifact_id: idea-dossier-I01-001-v006
    version: v006
    path: tests/idea-narrative-forward-0.9.0-preview.3/run-001/repaired/idea-dossier-v006.md
  - artifact_id: reader-handoff-forward-001
    version: v001
    path: tests/idea-narrative-forward-0.9.0-preview.3/run-001/inputs/reader-handoff.yaml
files_read:
  - AGENTS.md
  - research-skills-openai/AGENTS.md
  - research-skills-openai/skills/academic-language-assessor/SKILL.md
  - research-skills-openai/skills/academic-language-assessor/templates/language-assessment-report.md
  - research-skills-openai/skills/academic-language-assessor/references/language-assessment-rubric.md
  - research-skills-openai/skills/academic-language-assessor/references/language-hard-gates.md
  - research-skills-openai/skills/academic-language-assessor/references/chinese-academic-language-conventions.md
  - research-skills-openai/skills/academic-language-assessor/references/discipline-language-conventions.md
  - research-skills-openai/skills/academic-language-assessor/references/terminology-review.md
  - tests/idea-narrative-forward-0.9.0-preview.3/run-001/inputs/reader-handoff.yaml
  - tests/idea-narrative-forward-0.9.0-preview.3/run-001/repaired/idea-dossier-v006.md
isolation_mode: fresh_subagent
prior_scores_visible: false
source_edits_performed: false
decision: minor_language_revision
findings:
  - id: LANG-R005-001
    severity: minor
    category: terminology_consistency
    locator: lines 44, 48, 68, 93, 210, 290, 309, 355, and 376
  - id: LANG-R005-002
    severity: minor
    category: terminology_quality
    locator: lines 68, 377, 388, 429, and 456
  - id: LANG-R005-003
    severity: minor
    category: terminology_clarity
    locator: lines 237, 357, 458, 459, and 460
  - id: LANG-R005-004
    severity: minor
    category: terminology_definition
    locator: line 452
  - id: LANG-R005-005
    severity: minor
    category: readability_flow
    locator: lines 44, 68, 82, 177, 218, 263, 391, 438, and 466
  - id: LANG-R005-006
    severity: minor
    category: readability_flow
    locator: lines 444-462, especially line 460
  - id: LANG-R005-007
    severity: minor
    category: grammar_syntax
    locator: line 214
  - id: LANG-R005-008
    severity: minor
    category: grammar_syntax
    locator: lines 51 and 365
  - id: LANG-R005-009
    severity: minor
    category: academic_register_and_formatting
    locator: lines 472, 492, 494, and 507
  - id: LANG-R005-010
    severity: suggestion
    category: academic_register_and_reader_access
    locator: lines 291 and 295
unresolved_issues:
  - LANG-R005-001
  - LANG-R005-002
  - LANG-R005-003
  - LANG-R005-004
  - LANG-R005-005
  - LANG-R005-006
  - LANG-R005-007
  - LANG-R005-008
  - LANG-R005-009
  - LANG-R005-010
```

# Language Assessment Report

**Assessment ID**: language-assessment-I01-001-r005  
**Target Language**: Chinese（zh-CN）  
**Discipline**: 重症医学与临床流行病学，兼及纵向统计、系统辨识和医学人工智能  
**Target Journal**: 未指定  
**Scope**: 完整 Idea dossier 的读者可见文本（第 35–507 行）。机器 frontmatter、契约固定的 H2 标题和字段标签作为结构性脚手架排除；正文、表格内容、数学式周围文字和参考文献注释纳入评估。  
**Sections assessed**: 标题与摘要、背景与缺口、研究问题与目标、工作包、数据与方法、技术实现、证据链、分析要求、预期产物、贡献定位、可行性与边界、操作阈值及参考文献。  
**Date**: 2026-07-18

---

## Overall Language Readiness

**Level**: `minor_language_revision`

**Recommendation**: `polish`

正文整体已达到正式、可理解的中文学术表达基线，四项语言硬门槛均通过。当前问题可定位且不需要全面重写，主要是统一两个核心术语簇、解释两处局部技术标签、拆分若干负载过高的句子和表格单元格，并清理参考文献注释中的内部版本用语及中英混排。

---

## Dimension Scores

| Dimension | Score (1–10) | Severity |
|---|---:|---|
| Grammar & Syntax | 9 | pass |
| Academic Register & Tone | 8 | pass |
| Terminology Consistency | 6 | borderline |
| Tense & Voice Conventions | 9 | pass |
| Conciseness & Redundancy | 7 | borderline |
| Readability & Flow | 6 | borderline |

评分依据是全文模式而非最差单句。术语与可读性得分较低，源于跨章节重复出现的局部命名和高密度句法；并非语法错误、非正式语体或科学内容判断。

---

## Hard Gate Status

**Overall**: `pass`

| Gate | Status | Detail |
|---|---|---|
| Grammar error density | pass | 全文未发现明确且无歧义的语法错误；因此为 0/500 词。下列挂接和并列问题属于清晰度修订，不计作硬门槛中的明确语法错误。 |
| Academic register | pass | 未见任何章节以会话语体为主，也未见两个以上章节系统出现非正式表达。 |
| Terminology coherence | pass | 发现两个核心概念簇需要统一或改用直述表达，但未达到“三个核心概念各自无理由使用多种名称”的阈值；上下文仍能使目标读者识别其指称和功能。 |
| Tense systematic violation | pass | 本文是研究构想而非完成后的 Methods/Results 报告；现状、计划、条件分支和预期结果的时间状态区分一致，未见系统性时态或语态误用。 |

---

## Strengths

1. 正文持续使用克制、客观的计划性表述，能清楚区分既有证据、拟开展工作、条件性分支和拟生成结果。
2. CIF、IPCW、ARI、MCSE 等缩写均在首次进入正文时给出中英文全称；数学符号 (X_t)、(Y_t)、(A_t)、(M_t)、(B) 和 (S) 也在公式前集中定义。
3. 标题层级、比较表和编号步骤总体有效地组织了高度技术化的内容；绝大多数段落有明确主题，跨章节术语也大体稳定。
4. 对预测、关联、随机分组比较和因果解释使用了强度相称的限定语，没有采用宣传性或情绪化表达。
5. 中文标点、英文缩写、数字、单位和公式周围的格式总体一致。

---

## Specific Issues

### Chinese Academic Clarity

#### LANG-R005-005 — 多个句子承载过多独立关系

- **Location**: “跨学科概念桥”（第 44 行）、“Gap”（第 68 行）、“Primary research question”（第 82 行）、两项主要任务的方案表（第 177 行）、模拟研究（第 218 行）、映射忠实度（第 263 行）、最接近工作定位（第 391 行）、资源配置（第 438 行）和研究边界（第 466 行）。
- **Excerpt**: “研究中的四类证据回答不同问题：任务表现……；模拟恢复……；跨数据库稳定性……；条件性试验分析则……”（第 44 行）。
- **Severity / category**: minor / readability & flow。
- **Issue**: 这些句子通常同时表达定义、条件、比较对象、评价量和解释边界。信息均可辨认，但跨学科读者需要回读才能恢复各分句的平行关系。
- **Directional guidance**: 以“一句一个主要关系”为原则拆分；先给主句，再分别列出条件或评价对象。保留全部科学条件，不据语言评估删除任何局部必要限制。

#### LANG-R005-006 — 操作阈值表的单元格扫描负担过高

- **Location**: “Operational thresholds, alternatives, and stop conditions”表（第 444–462 行），尤以“观测映射外部忠实度”（第 460 行）为甚。
- **Excerpt**: 第 460 行在一个触发条件单元格内连续列出九项阈值，并在同一行给出多层后果。
- **Severity / category**: minor / readability & flow。
- **Issue**: 表格已经提供结构，但部分单元格仍混合阈值、分母、方向和后果；读者难以快速对应“哪一项触发哪一种处理”。
- **Directional guidance**: 在不改变阈值或停止条件的前提下，为每项触发条件使用一致的编号和短句，并将共同后果与条件特异后果分开呈现。

#### LANG-R005-007 — 并列修饰范围不清

- **Location**: “Observational model target, anchoring, and reporting”，第 214 行。
- **Excerpt**: “主要拟合采用显式测量过程的缺失随机或选择模型基线”。
- **Severity / category**: minor / grammar & syntax。
- **Issue**: “显式测量过程”究竟同时修饰“缺失随机”和“选择模型”，还是只修饰前者，句法上无法确定；“基线”与两个模型类别的对应关系也不够清楚。
- **Directional guidance**: 明确列出并列的模型类别，再分别说明“显式测量过程”和“基线”适用于哪一类；本评估不判断应采用哪种模型。

### Grammar & Syntax

#### LANG-R005-008 — 局部并列项的语法层级不完全对称

- **Location**: “Expected result”（第 51 行）和“Interpretation of the planned evidence”（第 365 行）。
- **Excerpt**: “还将分别报告两个试验……的组间差异，或采用预先设定的独立临床状态端点”；“每一模型层均按……报告为获得支持、未获支持或无法估计”。
- **Severity / category**: minor / grammar & syntax。
- **Issue**: 第 51 行把“报告差异”和“采用端点”置于同一选择层级，动作与对象不平行；第 365 行以“模型层”为主语、以结果状态为补语，读者需要推断究竟被判定的是模型层还是各评价对象。
- **Directional guidance**: 使选择项采用相同的谓语—宾语结构；在第 365 行明确判定对象，再列出三种报告状态。

### Academic Register & Tone

#### LANG-R005-009 — 参考文献注释含内部版本语言和未解释的英文状态词

- **Location**: References，第 472、492、494 和 507 行。
- **Excerpt**: “partial”“本次 v003 未读取 participant-level 工作簿”“search-through date 2026-07-17”。
- **Severity / category**: minor / academic register & mixed Chinese-English formatting。
- **Issue**: 这些表达更像项目内部记录，而非面向跨学科研究者的稳定来源说明；其中“本次 v003”还会使 v006 文本的读者误以为需要掌握旧版本语境。
- **Directional guidance**: 保留来源身份和证据范围，但用当前版本无关、可独立理解的中文说明表达核验范围；英文状态词若必须保留，应在首次出现时给出一致的中文对应。

#### LANG-R005-010 — 少量技术实现用语具有内部行话或隐喻色彩

- **Location**: “Key techniques and implementation”，第 291 和 295 行。
- **Excerpt**: “使每次状态与结构比较可重放”“完整结果与来源账本”。
- **Severity / category**: suggestion / academic register & reader access。
- **Issue**: “重放”和“账本”在软件工程语境中可以理解，但对不熟悉该语境的临床读者并不直接，也未在此处定义。
- **Directional guidance**: 优先采用能直接说明功能的标准学术表达，例如强调“可复现的比较记录”和“结果及来源记录”；若保留技术术语，应在首次出现时说明其功能。

### Terminology Consistency

#### LANG-R005-001 — 同一核心输出存在三种近义名称

- **Location**: 第 44、48、68、93、210、290、309、355 和 376 行。
- **Excerpt**: “锚点预测”“锚点层预测”“共同观测指标预测”。
- **Severity / category**: minor / terminology consistency。
- **Issue**: 上下文提示这些表达可能指同一模型输出，但未明确三者是否完全等价，还是分别指锚点变量层和一般共同观测指标层。该输出属于研究问题、恢复检验和结果登记中的核心对象。
- **Directional guidance**: 依据实际指称选择一个主名称，在首次出现时给出直接定义；若三者并不等价，则逐一说明层级和包含关系，之后固定使用。

#### LANG-R005-002 — “运输”词簇在中文学术语境中不够自然且指称范围不稳

- **Location**: 第 68、377、388、429 和 456 行。
- **Excerpt**: “证据能否恢复、运输和连接”“跨数据运输研究”“运输性结果”。
- **Severity / category**: minor / terminology quality。
- **Issue**: “运输”容易被理解为一般物理动作；文本实际讨论的似乎是模型、结果或证据在数据库之间的外部适用性。不同位置又分别以“证据”“研究”和“结果”为语义主体，增加了歧义。
- **Directional guidance**: 根据真实指称统一为经过核验的领域标准词，或直接写明“跨数据库外部适用性/可迁移性”；不要仅因英文术语存在而保留逐字直译。

#### LANG-R005-003 — “新状态分析/新状态端点”是可恢复但不够明确的简写

- **Location**: 第 237、357、458、459 和 460 行。
- **Excerpt**: “两项新状态分析”“未进入新状态分析时”“停止新状态端点”。
- **Severity / category**: minor / terminology clarity。
- **Issue**: 前文能够帮助读者推断其大致指向一维状态摘要或独立 SOFA 临床状态分析，但“新状态”本身可能被理解为新发现的潜在状态，而不是新增的试验次要分析端点。
- **Directional guidance**: 在这些位置直接使用已定义的两项分析名称，或首次明确说明该简写包含哪些端点；后续保持同一称谓。

#### LANG-R005-004 — “自助法保留率”缺少读者可执行的定义

- **Location**: “概率校准和结构稳定性”，第 452 行。
- **Excerpt**: “自助法保留率低于 80%”。
- **Severity / category**: minor / terminology definition。
- **Issue**: 目标读者可以理解自助法，但无法仅凭该短语确定被“保留”的对象、分子和分母。该术语直接参与停止阈值，因此需要局部定义。
- **Directional guidance**: 在首次使用处说明保留对象、计算单位及分母；公式和数值阈值可以留在后文，但指称和功能须在此处可识别。

| id | term_or_phrase | locator | reader_baseline | problem | recommended_replacement | first_use_definition | basis | acceptance_test |
|---|---|---|---|---|---|---|---|---|
| LANG-R005-001 | 锚点预测／锚点层预测／共同观测指标预测 | 44, 48, 68, 93, 210, 290, 309, 355, 376 | 熟悉纵向临床数据、但不精通所有参与学科 | 同一核心输出的名称及层级关系不明 | 一个经作者确认的主名称；若对象不同则保留两个明确分层名称 | 首次说明预测对象、所在层级及与其他名称的关系 | 当前文本跨位置语义比较；按复合术语的语义中心“预测”评估 | 全文每一处都能唯一判断指向哪一类预测，不需读者自行推断同义关系 |
| LANG-R005-002 | 证据运输／跨数据运输／运输性结果 | 68, 377, 388, 429, 456 | 重症、临床流行病学、统计、系统辨识和医学人工智能的混合读者 | 逐字直译不自然，且语义主体在证据、研究和结果间变化 | 经核验的标准词，或“跨数据库外部适用性/可迁移性”等直接描述 | 首次明确被迁移或外部检验的是模型、估计量、结果还是证据结论 | 中文学术清晰性规则、reader handoff 与当前文本上下文；未进行外部术语来源核验 | 删除“运输”后，各处仍准确指明对象、来源数据库、目标数据库和所指性质 |
| LANG-R005-003 | 新状态分析／新状态端点 | 237, 357, 458-460 | 不熟悉项目内部简称 | 可能误读为新发现的潜在状态 | 一维状态摘要分析／独立 SOFA 临床状态分析，或二者的明确定义性总称 | 首次列出该总称覆盖的两项分析 | 当前文本前后指称比较 | 单独阅读任一停止条件时，读者均能知道受影响的是哪一项试验分析 |
| LANG-R005-004 | 自助法保留率 | 452 | 了解验证与不确定性，但不掌握项目特定统计量 | 缺少被保留对象和分母 | 直接描述统计量，或保留术语并附计算定义 | 首次说明对象、重复单位、分子和分母 | 当前文本中无局部定义；未进行外部术语来源核验 | 不查阅项目内部材料即可复算或至少唯一解释该 80% 阈值 |

### Tense & Voice Conventions

未发现需要修订的问题。计划性动作使用“拟、将、须、只有……才”等形式；现有证据、尚未核验状态和条件性结果均有明确语言标记。本文没有把拟开展的 Methods 或 Results 写成已完成事实。

### Conciseness & Redundancy

未见无信息量的铺垫、宣传性修饰或成段重复。主要负担来自 LANG-R005-005、LANG-R005-006 和 LANG-R005-007 所列的长并列、名词化结构和限定语堆叠。修订时应压缩句法负担，但不得因相似限定语在不同科学关系中出现，就判定其中任一处可以删除。

### Readability & Flow

章节顺序和段落主题总体清楚。局部阅读阻力主要集中在跨学科概念桥、研究问题、模拟因素列表、映射评价量列表和操作阈值表；对应 LANG-R005-005 与 LANG-R005-006。建议只做局部拆分和视觉层级调整，不改变证据关系或限制内容的所在位置。

---

## Language Revision Priorities

1. **Terminology**: 4 issues — 先统一“锚点预测”词簇和跨数据库外部适用性词簇，再为“新状态分析”和“自助法保留率”补足局部指称。
2. **Readability & flow**: 2 recurring patterns — 拆分负载过高的句子，并把阈值表中的触发条件和后果改为可逐项扫描的结构。
3. **Grammar & syntax**: 2 local patterns — 澄清并列修饰范围和谓语—宾语平行关系。
4. **Register & formatting**: 2 issues — 将参考文献中的内部版本注释和未解释英文状态词改为稳定、读者可独立理解的中文来源说明；酌情替换少量软件工程行话。

---

## Re-Assessment Status

本次为只看当前文本的独立评估。未提供匿名问题清单，因此不判断任何既往问题是否已解决，也不比较旧版本、旧分数或旧决定。

| Check | Current assessment |
|---|---|
| Listed issues no longer present | 未评估；未提供匿名问题清单 |
| Listed issues still present | 未评估；未提供匿名问题清单 |
| New current-text issues | 不作“新增”比较；仅记录当前文本的 LANG-R005-001 至 LANG-R005-010 |

---

## Assessment Notes

- 产物输入严格限定为 `idea-dossier-I01-001-v006`（v006）和 `reader-handoff-forward-001`（v001）；未读取旧 dossier、既往 narrative/language/plan/delta/preflight/evaluation/preservation、测试断言或预期答案。
- 术语审查仅由普通阅读中发现的“锚点预测”词簇触发，并随后局限于当前文本中确实影响跨学科可读性的术语。任务范围未包含外部术语来源核验，因此对无法在当前文本内确认标准性的词语，建议采用直接描述，而不宣称某个替换词已获领域权威确认。
- 必需的机器 frontmatter、契约固定 H2 标题和字段标签不计入读者语言得分；只有正文中实际出现的内部版本用语或内部行话被记录。
- 本报告只评估语言。未评价科学有效性、研究设计、创新性、期刊适配性、可行性、叙事结构，也未裁决限制或解释边界应放置在哪一章节。
- 未修改 dossier 或 reader handoff。
