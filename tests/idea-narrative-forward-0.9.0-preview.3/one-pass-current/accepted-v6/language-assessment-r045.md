---
review_id: language-assessment-r045
reviewer_skill: academic-language-assessor
reviewer_instance_id: fresh-language-r045
workflow_id: RID-SEPSIS-CSM-20260717-001
round_id: r045
input_artifact_ids:
  - idea-dossier-I01-001-v030
  - reader-handoff-forward-001
input_versions:
  - v030
  - v001
scope: complete_idea_dossier
dossier_ref:
  artifact_id: idea-dossier-I01-001-v030
  version: v030
  path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/accepted-v6/idea-dossier-v030.md
reader_handoff:
  artifact_id: reader-handoff-forward-001
  version: v001
  path: tests/idea-narrative-forward-0.9.0-preview.3/run-001/inputs/reader-handoff.yaml
files_read:
  - AGENTS.md
  - research-skills-openai/AGENTS.md
  - research-skills-openai/skills/academic-language-assessor/SKILL.md
  - research-skills-openai/skills/academic-language-assessor/references/language-assessment-rubric.md
  - research-skills-openai/skills/academic-language-assessor/references/language-hard-gates.md
  - research-skills-openai/skills/academic-language-assessor/references/terminology-review.md
  - research-skills-openai/skills/academic-language-assessor/templates/language-assessment-report.md
  - research-skills-openai/skills/academic-language-assessor/scripts/validate_language_assessment.py
  - tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/accepted-v6/idea-dossier-v030.md
  - tests/idea-narrative-forward-0.9.0-preview.3/run-001/inputs/reader-handoff.yaml
isolation_mode: fresh_subagent
prior_scores_visible: false
source_edits_performed: false
decision: major_language_revision
findings:
  - finding_id: LANG-R045-001
    severity: major
    category: terminology_and_modifier_attachment
    dossier_locator: "主标题（第 27 行）及 Title（第 31 行）"
    current_problem: "短语‘脓毒症全病程重症监护病房（ICU）患者系统’使‘全病程’在通常汉语句法中可能附着于‘重症监护病房’，而不是患者的脓毒症相关病程；‘患者系统’这一中心语又出现得较晚，标题不能让跨学科读者立即、唯一地识别研究对象。"
    target_state: "标题直接依次指明 ICU 患者、从发病前在险期至结局的脓毒症相关病程、候选动态表征、跨数据库验证及有条件的 RCT 次要分析，各修饰语只有一个合理附着对象。"
    required_change_or_replacement: "采用直接描述且修饰关系唯一的标题，例如‘ICU 患者脓毒症相关病程的候选动态表征：从发病前在险期至结局的跨数据库验证，以及满足预设条件后的 RCT 稀疏访视数据次要分析’；定稿时可进一步压缩，但不得重新造成‘全病程’的附着歧义。"
    content_to_preserve: "候选而非已验证表征的证据状态；发病前在险期至结局的时间范围；跨数据库验证；RCT 分析的预设前置条件、稀疏访视数据和次要分析属性。"
    acceptance_test: "仅阅读标题的重症医学、临床流行病学或纵向统计读者均能回答研究对象是谁、覆盖哪段病程、验证在哪里进行以及 RCT 分析何时启动；标题中每个范围、条件和数据属性修饰语均能唯一附着于预期中心语。"
  - finding_id: LANG-R045-002
    severity: major
    category: readability_and_flow
    dossier_locator: "Title, summary, audience, and positioning，One-sentence complete-Idea summary（第 32 行）"
    current_problem: "该摘要行共 333 个字符，单句同时嵌入数据访问与审计限制、四段病程、两种表征描述、外部验证限制、五类证据、两个项目简称和 RCT 启动条件。三层条件嵌套遮蔽了‘构建—外部验证—条件性试验分析’这一主干，跨学科读者需要回读才能恢复阶段顺序。"
    target_state: "在保持单句摘要形式的前提下，读者一次阅读即可按顺序识别构建对象、主要验证方式和 RCT 次要分析的启动条件；项目简称的解释不打断主干。"
    required_change_or_replacement: "将摘要重组为三个平行、长度相近的分句，分别只承担‘构建什么’、‘如何作主要外部验证’和‘何时启动分试验次要分析’；先给出各分句的主要谓语与对象，再放必要条件，并把‘模拟恢复检验’和‘阶段 II 达标’的短定义置于其首次出现后的最短可读位置。"
    content_to_preserve: "24 个月期限、两个公共 ICU 数据库及其审计前提、四段病程、知识约束与不确定性、未参与开发或参数调整的数据、五类达标证据、试验授权与语义条件，以及各 RCT 分别分析。"
    acceptance_test: "摘要仍为一个完整句子，但三个阶段各只有一个主要谓语；任何条件从句都能唯一对应一个阶段；三类目标读者无需回读即可复述构建、验证和后续试验分析的顺序。"
  - finding_id: LANG-R045-003
    severity: major
    category: terminology_first_use
    dossier_locator:
      - "Structured abstract，Objective and hypothesis（第 39 行）"
      - "Research question, objectives, and core hypothesis，Core hypothesis（第 89 行）"
    current_problem: "‘受限复杂候选’首次出现时没有明确的科学中心语；后文又使用‘复杂候选’，但读者仍需从基线模型、候选表征和图结构等上下文猜测它究竟指候选模型、候选表征还是候选结构。该简称承载核心假设和停止条件，却未在首次使用处说明对象与功能。"
    target_state: "首次出现即用自然语言指出这是相对于简单基线、复杂度受限的候选动态表征模型，并在后文使用同一简称。"
    required_change_or_replacement: "首次用作核心假设时改为‘至多一个复杂度受限的候选动态表征模型（下称“复杂候选模型”）’，并将后续‘受限复杂候选’或‘复杂候选’统一为‘复杂候选模型’；若实际所指不是模型，应以实际科学对象替换‘模型’，但必须保留明确中心语。"
    content_to_preserve: "至多一个候选、复杂度受审计与预设上限约束、须通过模拟恢复检验、相对于简单基线后置评估，以及未达标时退回较简单层级。"
    acceptance_test: "读者在第 39 行首次读到该词时，无需查阅后文即可说出候选对象的类别、与简单基线的关系和简称；第 89、101、110、126、228、303、348、403、409、432 行的用法均指向同一对象。"
  - finding_id: LANG-R045-004
    severity: minor
    category: terminology_first_use
    dossier_locator:
      - "Twenty-four-month programme（第 101 行）"
      - "Public ICU database roles and observability audit，有效支持与复杂度上限（第 166 行）"
    current_problem: "‘状态模式不超过 3’没有说明‘模式’是每个维度的离散状态数、整体状态类别数、切换机制数，还是其他模型数量。该数量约束随后在可行性段落重复出现，但始终没有直接定义。"
    target_state: "数量约束以其实际计数对象的标准科学名称或直接描述呈现，并在首次出现时给出符号或简称。"
    required_change_or_replacement: "由作者确认该数量的实际对象后，直接写出计数对象，例如若所指为每个潜在维度允许的离散状态数，则写为‘每个潜在维度的离散状态数不超过 3’；不得只保留‘状态模式’这一未定义短语。"
    content_to_preserve: "上限为 3、该上限属于复杂度控制、数据支持不足时继续简化。"
    acceptance_test: "首次出现处明确给出被计数对象；全文四处相关用法采用同一名称；读者不需要根据 K 或后续模型描述猜测‘3’限制的是什么。"
  - finding_id: LANG-R045-005
    severity: minor
    category: terminology_and_parallelism
    dossier_locator:
      - "Objectives，第 3 项（第 84 行）"
      - "Simulation and semi-synthetic recovery tests，首段（第 228 行）"
    current_problem: "‘正确、零边、过拟合和错设生成器’把设定状态、参数真值和模型复杂度作为不平行的定语并列；‘零边’对非建模专业读者也未定义。第 228 行的‘错误滞后或观测模型’还可能被读成只有滞后错误、观测模型本身不一定错设。"
    target_state: "各模拟情景使用平行的直接描述，并在首次出现时说明‘零边’所指的真实参数状态。"
    required_change_or_replacement: "改用平行表达，例如‘正确设定、候选边真实参数为零、状态数过多以及模型错设的生成情景’，并把‘错误滞后或观测模型’拆为‘错误的滞后设定或错设的观测模型’；若保留‘零边’，先写‘真实参数为零的候选边（零边）’。"
    content_to_preserve: "正确设定、零边、过拟合、遗漏状态、错误滞后和错设观测模型等全部恢复检验情景，以及它们的不同科学功能。"
    acceptance_test: "每个情景名称都能独立补全为同一语法结构；首次读到‘零边’时即可知道其参数真值为零；‘错误’分别、明确修饰滞后设定和观测模型。"
  - finding_id: LANG-R045-006
    severity: minor
    category: readability_and_flow
    dossier_locator:
      - "Trial-specific mapping to observed visits and independent clinical-state analysis，试验语义与共同锚点资格（第 256 行）"
      - "同节，预先确定的映射、映射输出和一致程度（第 258 行）"
      - "同节，一致性与误差标准（第 260 行）"
    current_problem: "三个连续段落分别长 374、377 和 371 个字符，资格条件、符号定义、公式、方向约定和多项阈值都压缩在段内长句中。内容本身有顺序，但句法层级没有把‘资格—映射—判定’内部的步骤显式分开，读者容易把定义、计算规则和通过标准混读。"
    target_state: "资格、符号定义、计算步骤、方向约定和通过标准在视觉和句法上分开，同时保留现有先后顺序。"
    required_change_or_replacement: "将第 256 行的资格条件改为编号条件；第 258 行依次单列符号、分解、两个摘要和符号方向；第 260 行把外部数据判定标准与遮蔽治疗组后的试验数据检查分成两个编号列表。公式与阈值原样保留，只重组句界和列表层级。"
    content_to_preserve: "所有数据授权和语义要求、共同锚点资格、公式、符号约定、相关与误差阈值、校准和覆盖标准、合理范围和可计算比例，以及不得按试验重新估计权重的限制。"
    acceptance_test: "读者可分别定位每个资格条件、每个符号定义、每一步计算和每项通过阈值；任一列表项只承担一种功能，且重组后数值、方向和条件数量与原文一致。"
  - finding_id: LANG-R045-007
    severity: suggestion
    category: target_language_consistency
    dossier_locator:
      - "读者可见的英文主标题和表头，例如第 29、36、44、68、91、128、186、290、327、342、365、399、424 行"
      - "Evidence chains 中的 Input、Method / analysis / processing、Output、Supports 标签（第 294-325 行）"
    current_problem: "目标语言为 zh-CN，但多数读者可见的章节标题、表头和证据链标签保留英文；正文则为中文。这不妨碍专业读者理解，却造成版式语言不一致。若这些标签是固定契约字段，它们属于显示层问题，而不是作者正文错误。"
    target_state: "非固定的读者可见标题与正文语言一致；固定契约标签在不改动契约的前提下有清晰的中文显示名称。"
    required_change_or_replacement: "仅在这些标题并非契约固定标签时统一为中文；若为固定标签，不修改 dossier 语义或字段，而向模板维护方提出非阻断性的中文显示本地化建议。"
    content_to_preserve: "现有章节层级、表格结构、证据链四个组成部分及任何固定契约含义。"
    acceptance_test: "读者界面中的非固定标题与 zh-CN 正文一致；任何固定标签仍保持契约值不变，同时不要求作者在正文中混用两套同义标题。"
unresolved_issues:
  - LANG-R045-001
  - LANG-R045-002
  - LANG-R045-003
  - LANG-R045-004
  - LANG-R045-005
  - LANG-R045-006
---

# Language Assessment Report

**Assessment ID**: language-assessment-r045  
**Target Language**: Chinese (zh-CN)  
**Discipline**: 重症医学、临床流行病学、纵向统计、系统辨识、医学人工智能与转化研究  
**Target Journal**: 未指定  
**Scope**: complete_idea_dossier  
**Date**: 2026-07-19

---

## Overall Language Readiness

**Level**: major_language_revision

**Recommendation**: revise_language

---

## Dimension Scores

| Dimension | Score (1–10) | Severity |
|-----------|-------------|----------|
| Grammar & Syntax | 9 | pass |
| Academic Register & Tone | 9 | pass |
| Terminology Consistency | 5 | fail |
| Tense & Voice Conventions | 9 | pass |
| Conciseness & Redundancy | 6 | borderline |
| Readability & Flow | 5 | borderline |

---

## Hard Gate Status

**Overall**: fail

| Gate | Status | Detail |
|------|--------|--------|
| Grammar error density | pass | 完整文本检查未发现达到每 500 词当量 3 个以上的明确语法错误；未见影响理解的系统性句法错误。 |
| Academic register | pass | 0 个章节呈现系统性口语或宣传性语体；措辞总体正式、克制，并持续标明计划与结果的区别。 |
| Terminology coherence | fail | 未发现 3 个以上核心概念被无理由换名，但 Idea 专项门槛被触发：标题中的“全病程”修饰关系可误指研究对象，“受限复杂候选”在核心假设首次出现时没有可识别的科学中心语。 |
| Tense systematic violation | pass | 0 个章节存在系统性时态或研究状态错置；计划工作、既有证据和条件性后续分析区分稳定。 |

---

## Strengths

1. 正文始终以计划、条件和预期措辞描述尚未完成的工作，没有把拟开展分析写成既有结果。
2. 学术语体正式且克制；未见口语、直接对读者讲话、夸张宣传或修辞性设问。
3. “模拟恢复检验”在首次进入完整摘要时即以“检验候选表征可恢复性的模拟与半合成实验”说明功能，“阶段 II 达标”也在同句给出五类证据的概括，后文再展开标准。
4. Sepsis-3、SOFA、RCT、CRF、SAP、MAR、AUPRC 等缩写通常在首次读者可见处给出全称、中文说明或可识别的专业语境。
5. “事件发生时刻”与“信息可用时刻”、“不更新模型参数的外部验证”与有限更新、候选表征与独立临床状态等关键对照在全文保持清楚。

---

## Specific Issues

### Chinese Academic Clarity

- **LANG-R045-001（major）**：主标题中“全病程”的附着对象不唯一，“患者系统”的中心语出现过晚。应改为直接依次命名患者、病程范围和研究操作的标题；可采用前述候选标题，但定稿仍须重新检查全部修饰语。
- **LANG-R045-002（major）**：第 32 行单句 333 个字符，过多前置限制和括注遮蔽三阶段主干。应保持单句字段，但用三个平行分句分别承载构建、外部验证和条件性 RCT 分析。
- **LANG-R045-006（minor）**：第 256、258、260 行连续三个超长技术段落把资格、公式、定义和阈值压在段内长句中。应只调整句界与列表层级，不删减任何科学条件或数值。

### Grammar & Syntax

未发现需单列的明确语法错误。LANG-R045-005 所述问题属于并列结构和修饰范围不清，而非普遍语法失范。

### Academic Register & Tone

未发现口语化、宣传性或不符合学术语体的措辞。

### Terminology Consistency

| id | term_or_phrase | locator | reader_baseline | problem | recommended_replacement | first_use_definition | basis | acceptance_test |
|---|---|---|---|---|---|---|---|---|
| LANG-R045-001 | 脓毒症全病程重症监护病房（ICU）患者系统 | 主标题第 27、31 行 | 跨重症医学、临床流行病学、纵向统计、系统辨识和医学 AI 的研究者 | “全病程”可能误附着于“重症监护病房”，研究对象不能由标题唯一解析 | ICU 患者脓毒症相关病程的候选动态表征：从发病前在险期至结局的跨数据库验证，以及满足预设条件后的 RCT 稀疏访视数据次要分析 | 标题直接命名研究对象和时间范围，无需另设项目简称 | 汉语修饰关系与提供的读者基线；无需外部术语检索 | 不看摘要也能唯一识别患者、病程范围、验证对象和 RCT 条件 |
| LANG-R045-003 | 受限复杂候选／复杂候选 | 第 39、89 行首次核心用法；后续第 101、110、126 等行 | 可理解验证和纵向模型，但不熟悉项目简称的跨学科研究者 | 缺少“模型”“表征”或“结构”等科学中心语，读者须猜测简称所指 | 复杂度受限的候选动态表征模型（复杂候选模型） | 相对于简单基线、复杂度受审计与预设上限约束、且须通过恢复检验的候选动态表征模型 | 首次使用可识别性与全文指称；无需外部术语检索 | 首次出现即可说出对象类别、基线关系和简称，后文统一指同一对象 |
| LANG-R045-004 | 状态模式 | 第 101、166 行；后续第 403 行等 | 不假定熟悉项目内模型参数命名 | “模式”未说明实际计数对象 | 确认科学对象后采用直接计数名称；若意指每个潜在维度的离散状态数，则直接如此表述 | 首次出现时定义计数对象及上限 | 文本内部无法唯一确定所指数目；不宜凭 dossier 猜测并另造术语 | 读者明确知道“3”限制的对象，全文用名一致 |
| LANG-R045-005 | 零边；正确、零边、过拟合和错设生成器 | 第 84、228 行 | 不假定所有读者都有图模型专门知识 | 情景标签语法不平行，“零边”未解释参数真值，“错误滞后或观测模型”修饰范围含混 | 正确设定、候选边真实参数为零、状态数过多以及模型错设的生成情景；错误的滞后设定或错设的观测模型 | 如需简称，首次写“真实参数为零的候选边（零边）” | 句法平行性与首次使用可理解性；无需外部术语检索 | 各情景能以同一语法结构独立读懂，且“错误”分别修饰两个对象 |

本次没有发现必须依赖权威外部来源才能判定的标准术语争议；问题均可由修饰关系、科学中心语和首次使用可理解性直接判定，因此未读取外部来源。

### Tense & Voice Conventions

未发现系统性问题。计划工作使用“拟”“计划”“须”“若……则……”等形式，既有研究和当前资源状态使用完成或现状表达，二者没有混淆。

### Conciseness & Redundancy

没有把科学条件的重复出现判定为可删除内容。主要问题是少数段落把过多限定条件放入同一句，而不是 dossier 总体信息量过大。修订时应调整句界和列表结构，不应由语言编辑决定删除哪一项科学条件。

### Readability & Flow

- **LANG-R045-002（major）**：完整摘要的阶段顺序被条件嵌套遮蔽。
- **LANG-R045-006（minor）**：试验映射部分的定义、计算和判定标准缺少可扫描的内部层级。
- 其余章节的标题层级、表格组织和“背景—缺口—研究问题—设计—证据链—停止条件”顺序总体清楚。
- **LANG-R045-007（suggestion）**：若英文标题和表头并非固定契约标签，可统一为中文；若属于固定标签，只提出显示本地化建议，不要求作者改动契约字段。

---

## Language Revision Priorities

1. **标题与核心术语**：2 个 major、2 个 minor — 先消除标题修饰歧义，再为“复杂候选模型”“状态模式”和“零边”补足科学中心语或直接定义。
2. **摘要可读性**：1 个 major — 保持单句要求，以三个平行分句重建“构建—验证—条件性试验分析”的可见顺序。
3. **技术段落层级**：1 个 minor — 将试验资格、映射定义和判定阈值分别改为可扫描的编号结构，保留全部公式和数值。
4. **显示语言一致性**：1 个 suggestion — 仅对非固定标题作中文化；固定标签交由模板显示层处理。

---

## Re-Assessment Status

本次为 Idea dossier 的全新完整评估，未接收也未读取任何既往问题清单、评分或决定，因此不进行前后版本问题对照。

| Check | Current assessment |
|--------|--------------------|
| Listed issues no longer present | 不适用；没有既往问题清单 |
| Listed issues still present | 不适用；没有既往问题清单 |
| New current-text issues | 6 个待处理问题：LANG-R045-001 至 LANG-R045-006；另有 1 个非阻断性建议 LANG-R045-007 |

---

## Assessment Notes

- 完整读取并评估了 v030 dossier 的 frontmatter、标题与摘要、背景与缺口、研究问题和假设、工作包、数据与材料、研究设计与方法、证据链、所需分析、预期产物、贡献与相关研究比较、可行性、限制、风险和参考文献。
- 完整读取了 reader handoff 的目标读者、阅读目的、可假定与不可假定的先验知识、核心术语定义规则、阅读推理顺序和 zh-CN 语言要求。
- 指令依据限于列入 `files_read` 的 OpenAI academic-language-assessor 主文件、直接评分标准、语言门槛、术语核查规范、报告模板、validator 及最近的 AGENTS.md。按照本次输入边界，未读取其他语言惯例文件。
- 未读取其他 dossier、修订记录、差异报告、保留性材料、叙事评估、预检、其他评估报告、组合报告、历史语言报告、测试脚本或 Hermes 对应 Skill。
- 未检索外部来源：实际触发的问题是中文修饰语附着、项目简称缺少科学中心语和首次使用不可识别，不需要以外部标准术语证据作判断。
- 本报告只评估语言、术语和可读性；不评价论证、研究方法、创新性、可行性、影响力或研究设计是否成立。源 dossier 与 reader handoff 均未修改。
