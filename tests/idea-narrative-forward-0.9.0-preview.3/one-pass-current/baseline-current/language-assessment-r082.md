---
review_id: language-assessment-r082
reviewer_skill: academic-language-assessor
reviewer_instance_id: fresh-academic-language-assessor-r082
workflow_id: RID-SEPSIS-CSM-20260717-001
round_id: r082
input_artifact_ids:
  - idea-dossier-I01-001-v003
  - reader-handoff-forward-001
input_versions:
  - v003
  - v001
scope: complete_idea_dossier
dossier_ref:
  artifact_id: idea-dossier-I01-001-v003
  version: v003
  path: tests/idea-test-0.9.0-preview.1/0.9.0-preview.1/03_ideas/nodes/I01-001/dossiers/idea-dossier-v003.md
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
  - research-skills-openai/skills/academic-language-assessor/references/chinese-academic-language-conventions.md
  - research-skills-openai/skills/academic-language-assessor/references/discipline-language-conventions.md
  - research-skills-openai/skills/academic-language-assessor/references/terminology-review.md
  - research-skills-openai/skills/academic-language-assessor/templates/language-assessment-report.md
  - tests/idea-test-0.9.0-preview.1/0.9.0-preview.1/03_ideas/nodes/I01-001/dossiers/idea-dossier-v003.md
  - tests/idea-narrative-forward-0.9.0-preview.3/run-001/inputs/reader-handoff.yaml
isolation_mode: fresh_subagent
prior_scores_visible: false
source_edits_performed: false
decision: major_language_revision
findings:
  - finding_id: TERM-001
    severity: major
    finding_kind: terminology
    category: "复合标题中的修饰关系"
    dossier_locator: "标题（第27行）及 Title 条目（第31行）：‘脓毒症全病程候选动态系统表征：计划跨数据库检验与条件性稀疏 RCT 次要再分析’"
    current_problem: "‘条件性稀疏 RCT 次要再分析’按通常句法可被理解为 RCT 本身具有‘条件性’或‘稀疏’属性；正文实际表达的是：次要分析仅在预设条件满足后开展，且所用 RCT 数据的访视稀疏。两个修饰语目前附着于错误或不明确的语义中心。"
    target_state: "标题明确区分候选研究对象、计划开展的跨数据库检验、分析启动条件和稀疏访视这一数据属性。"
    required_change_or_replacement: "将标题改为直接说明修饰关系的形式，例如：‘脓毒症全病程动态状态表征候选方案：计划开展跨数据库检验，并在预设条件满足后对稀疏访视 RCT 数据进行次要分析’。可作等义压缩，但‘预设条件’必须修饰分析是否启动，‘稀疏访视’必须修饰数据或观测。"
    content_to_preserve: "候选和计划的证据状态、跨数据库检验、RCT 次要分析、分析具有前置条件、RCT 访视稀疏。"
    acceptance_test: "重新解析修改后的标题：普通读者只能把‘稀疏访视’理解为 RCT 数据属性，只能把‘满足预设条件后’理解为次要分析的启动条件；标题不得暗示 RCT 设计本身‘稀疏’或‘条件性’。"
    term_or_phrase: "条件性稀疏 RCT 次要再分析"
    term_role: "阶段 III 研究设计及数据属性的标题级说明"
    recommended_form_or_plain_description: "在预设条件满足后，使用稀疏访视 RCT 数据开展次要分析"
    evidence_basis: "依据标题的修饰语附着检查，以及正文第244–261行对启动条件、访视稀疏性和次要分析性质的分别说明；建议采用直接描述，不主张该替换是某个外部标准术语。"
    first_use_definition: "在标题后的首句说明：该次要分析仅在阶段 II 及试验语义等预设条件满足后启动，‘稀疏’指试验仅在少数实际访视测量相关指标。"
    competing_forms_and_locators: []
  - finding_id: TERM-002
    severity: major
    finding_kind: terminology
    category: "核心研究对象的跨段命名一致性"
    dossier_locator: "标题/Title（第27、31行）、Structured abstract—Objective and hypothesis（第39行）、Primary research question（第60行）、阶段 II 成功定义（第92行）、Interpretation matrix（第370行）及 Identity and final stop boundary（第439行）"
    current_problem: "同一核心研究对象在读者入口和结论位置被称为‘候选动态系统表征’、‘候选全病程表示’、‘候选系统表征’、‘最小全病程候选表示’和‘跨库系统端点’；局部又出现‘模型’。未说明这些形式是同一对象的简称、不同成熟度，还是不同分析对象，跨学科读者需要自行猜测。"
    target_state: "首次出现以直接描述界定研究对象，此后使用一个固定短称；‘模型’仅指实际拟合的统计模型，‘验证结论/研究结论’仅指评价结果，不再用‘系统端点’代替研究对象或结论。"
    required_change_or_replacement: "首次定义为‘一种以患者—时间状态及状态转移为单位，并明确区分生理状态、治疗行动与观察过程的脓毒症全病程动态状态表征（下称“候选状态表征”）’；此后用‘候选状态表征’指该对象。把‘跨库系统端点’改为‘关于该候选状态表征的跨数据库验证结论’或与原句功能相符的直接说法。"
    content_to_preserve: "研究对象覆盖发病前、首次发病、发病后及结局；以患者—时间状态和状态转移为单位；候选而非已验证对象；阶段 II 的跨数据库评价边界。"
    acceptance_test: "全文核查核心研究对象的每次读者可见命名：保留首次全称及固定短称‘候选状态表征’；任何‘模型’均能明确指向具体拟合模型；任何‘端点’均指可测结局而非项目成功状态。不得遗留未定义的‘候选全病程表示’、‘候选系统表征’、‘最小全病程候选表示’或‘系统端点’作为同一对象的竞争形式。"
    term_or_phrase: "候选动态系统表征"
    term_role: "标题、主要问题、核心假设和阶段 II 结论共同指向的中心研究对象"
    recommended_form_or_plain_description: "脓毒症全病程动态状态表征；首次定义后简称‘候选状态表征’"
    evidence_basis: "来自完整 dossier 的同一角色全文一致性核查；在受限输入条件下未外部验证某个紧凑标签，因而采用能直接说明对象、单位和过程区分的描述性表达。"
    first_use_definition: "一种以患者—时间状态及状态转移为单位，并明确区分生理状态、治疗行动与观察过程的脓毒症全病程动态状态表征。"
    competing_forms_and_locators:
      - "候选动态系统表征（第27、31、32行）"
      - "候选全病程表示（第39行）"
      - "候选状态表示（第65行）"
      - "候选系统表征（第92、370行）"
      - "最小全病程候选表示（第370行）"
      - "跨库系统端点/系统端点（第238、320、337、358、430、439行）"
  - finding_id: TERM-003
    severity: major
    finding_kind: terminology
    category: "模拟评价与候选准入标准的命名"
    dossier_locator: "One-sentence summary（第32行）、Positioning（第34行）、Structured abstract—Objective（第39行）、Objectives 3（第66行）、Core hypothesis（第71行）、日期门与工作包（第85、107、112行）、Absolute simulation and semi-synthetic recovery gate（第214–226行）"
    current_problem: "决定复杂候选能否继续的同一组模拟评价标准被轮换称为‘绝对模拟恢复门’、‘绝对恢复/假置信门’、‘绝对 Monte Carlo 门’、‘恢复与准入门’和‘错设弃权门’。‘绝对’修饰恢复量、阈值还是判断方式并不清楚；‘假置信’也未在首次出现处说明是错误结构被高置信支持。"
    target_state: "读者在首次出现时即知道该组标准检查三件事：模拟数据中的参数或状态恢复、对不存在结构的错误支持、模型错设时能否识别失败；此后以单一短称指代。"
    required_change_or_replacement: "将首次出现改为‘预先规定的模拟恢复、虚假结构控制和模型错设识别标准（下称“模拟准入标准”）’；后文统一使用‘模拟准入标准’，需要指单项时分别写‘恢复标准’、‘虚假结构错误支持率标准’或‘错设识别标准’，不再用裸露的‘绝对门’或‘假置信门’。"
    content_to_preserve: "阈值为预先规定的绝对数值而非仅作相对模型排名；正确、零边、过拟合和错设生成情景；失败时复杂候选不得晋级。"
    acceptance_test: "从标题摘要至方法和失败标准进行全文检索：首次出现含三项直接说明及短称；同一组标准之后只用‘模拟准入标准’；单项判断使用功能特异名称；不得遗留‘绝对模拟恢复门’、‘绝对恢复/假置信门’、‘绝对 Monte Carlo 门’、裸露‘绝对门’或‘错设弃权门’。"
    term_or_phrase: "绝对恢复/假置信门"
    term_role: "控制复杂候选能否进入后续评价的模拟准入标准"
    recommended_form_or_plain_description: "预先规定的模拟恢复、虚假结构控制和模型错设识别标准；简称‘模拟准入标准’"
    evidence_basis: "依据第214–226行对三类评价量和自动处理的直接定义，以及全文竞争形式核查；没有在受限输入外验证紧凑标签，故采用描述性名称。"
    first_use_definition: "一组预先规定的模拟评价标准，用于检查候选方法能否恢复预设状态或参数、避免对不存在的结构给出高置信支持，并在模型错设时识别失败。"
    competing_forms_and_locators:
      - "绝对模拟恢复门（第32行）"
      - "绝对恢复、绝对恢复/假置信门（第34、71、345、353行）"
      - "绝对 Monte Carlo 门（第40、329行）"
      - "恢复与准入门（第85行）"
      - "绝对模拟门（第112行）"
      - "绝对门（第250、276、356行；其中第250、276、356行用于不同的投影评价操作，修订时必须改为该操作的特异名称）"
      - "错设弃权门（第353行）"
  - finding_id: TERM-004
    severity: major
    finding_kind: terminology
    category: "RCT 可观测投影及分析结局的首次解释与一致性"
    dossier_locator: "One-sentence summary（第32行）、Structured abstract—Approach/Expected result/Contribution（第40–42行）、Primary research question（第60行）、Objective 4（第67行）、Conditional trial-observation projection（第242–261行）、Key techniques 8（第276行）及 RCT evidence chain（第314–320行）"
    current_problem: "核心阶段 III 设计在摘要和问题中先后称为‘冻结观测投影门’、‘投影可观测状态摘要’、‘投影可观测摘要’、‘RCT 观测投影’和‘投影摘要’，但其可计算对象直到第246–250行才显现。读者在前约半篇无法判断这是潜状态、观测指标的加权组合、验证程序还是分析结局。"
    target_state: "在首次读者可见使用处直接说明：该摘要由阶段 II 冻结观测模型映射，并仅使用试验实际访视中实测且语义一致的共同生理指标计算；后文用一个固定名称区分映射、评价标准和最终结局。"
    required_change_or_replacement: "首次使用时写为‘由阶段 II 冻结观测模型映射、且仅由试验实际访视中的共同实测生理指标计算的一维摘要（下称“访视可观测投影摘要”）’。把计算操作称为‘冻结映射’，把决定能否使用该摘要的 R0/R1 条件称为‘试验语义与投影适用性标准’，把分析结局称为‘访视可观测投影摘要结局’；不要再用同一个‘投影门/观测投影’涵盖三种角色。"
    content_to_preserve: "映射在治疗组比较前冻结；仅用合格共同锚点；每项试验分别构造；需先通过语义、测量一致性、校准和投影忠实度标准；随机化结论仅限实际访视的可观测摘要。"
    acceptance_test: "全文核查该设计关系：首次出现即含数据来源、冻结映射和一维摘要的功能说明；计算操作、适用性判断和分析结局分别使用固定名称；删除或改写所有未定义的‘冻结观测投影门’、‘投影可观测状态摘要’、‘RCT 观测投影’和裸露‘投影摘要’。在摘要、研究问题、方法、证据链和预期产物中，固定短称‘访视可观测投影摘要’指向同一对象。"
    term_or_phrase: "投影可观测状态摘要"
    term_role: "连接阶段 II 观测模型与稀疏 RCT 实际访视数据的映射结果及阶段 III 分析结局"
    recommended_form_or_plain_description: "由冻结观测模型映射、仅用试验实际访视中的共同实测生理指标计算的一维摘要；简称‘访视可观测投影摘要’"
    evidence_basis: "依据 reader handoff 对跨学科首次定义的要求，以及第246–252行给出的共同锚点、冻结映射和分析结局说明；建议为直接描述，不依赖未执行的外部术语验证。"
    first_use_definition: "由阶段 II 冻结观测模型映射，并仅使用试验实际访视中语义和单位一致的共同实测生理指标计算的一维摘要。"
    competing_forms_and_locators:
      - "冻结观测投影门（第32行）"
      - "投影可观测状态摘要（第32、41、60、67行）"
      - "投影可观测摘要（第42、252、368行）"
      - "trial-observation projection/观测投影（第242、246、314行）"
      - "投影摘要（第252、258、347、368行）"
      - "RCT 冻结投影器（第276行）"
  - finding_id: TERM-005
    severity: minor
    finding_kind: terminology
    category: "两个分层 RCT 结局的角色区分"
    dossier_locator: "One-sentence summary（第32行）、Expected result（第41行）、Projection-pass estimand（第252行）、Automatic independent fallback（第254行）、Planned outputs（第347行）"
    current_problem: "‘death-ranked’在首次出现时未作中文解释，随后同时用于按投影摘要排序和按 SOFA 排序的两个不同结局；英文短标签掩盖了死亡、在院存活和活着出院三层的具体排序规则，也弱化了两个结局与阶段 II 关系不同这一点。"
    target_state: "用两个功能特异的中文名称分别指代投影分支和独立 SOFA 分支，并在首次出现处说明三层排序。"
    required_change_or_replacement: "投影分支写为‘死亡最差、活着出院最优、在院存活者按访视可观测投影摘要排序的分层结局’；独立分支写为‘死亡最差、活着出院最优、在院存活者按 SOFA 排序的独立分层临床结局’。如保留英文，只能在中文全称后括注一次，不能作为首要名称。"
    content_to_preserve: "死亡置于最差层、活着出院置于最有利层；在院存活者分别按投影摘要或 SOFA 排序；后者与阶段 II 表征独立。"
    acceptance_test: "全文分别检索两个结局：每处名称都能仅凭文字判定在院存活者按何种量排序，并明确 SOFA 分支与阶段 II 独立；首次出现不得仅写‘death-ranked SOFA’或‘death-ranked 投影摘要’，两个结局不得共用无法区分角色的短称。"
    term_or_phrase: "death-ranked SOFA / death-ranked 投影摘要"
    term_role: "投影通过分支与独立降级分支的两个不同访视分层结局"
    recommended_form_or_plain_description: "分别使用‘按访视可观测投影摘要排序的分层结局’和‘按 SOFA 排序的独立分层临床结局’，并明确死亡最差、活着出院最优"
    evidence_basis: "依据第252、254行对两个结局的不同排序变量和证据关系的直接说明；建议为不需项目词汇表即可理解的描述性表达。"
    first_use_definition: "投影分支：死亡最差、活着出院最优、在院存活者按访视可观测投影摘要由差到好排序；独立分支：前两层相同，但在院存活者按 SOFA 由高到低排序。"
    competing_forms_and_locators:
      - "death-ranked SOFA 临床状态再分析（第32、41行）"
      - "death-ranked 投影摘要（第317、347行）"
      - "trial-specific independent secondary clinical-state reanalysis（第254行）"
      - "独立 SOFA 端点/分支（第246、254、276、347、356、369、384、405、428行）"
  - finding_id: LANG-006
    severity: major
    finding_kind: language
    category: "中文学术清晰度与限定堆叠"
    dossier_locator: "One-sentence complete-Idea summary（第32行）及 Primary research question（第60行）"
    current_problem: "两个最重要的读者入口句同时承载研究对象、四段病程、两个数据来源、阶段 I–III、多个前置条件、两条 RCT 分支和禁止性结论；长串定语与条件从句使主谓宾关系延迟，读者难以在一次阅读中提取主问题和主要设计。"
    target_state: "首句先呈现研究对象、核心任务和主要证据路径；必要条件与降级分支保持完整但按并列层级展开，每个修饰语紧邻其中心词。"
    required_change_or_replacement: "在不改变固定字段功能的前提下重组两句：One-sentence summary 保留一个明确主干，并将阶段 II 证据与条件性 RCT 分支组织为至多两个并列分句；Primary research question 将三个编号问题保持平行句式，每项只含一个主要动作，避免在第（3）项内再次嵌套‘仅在……否则……’的多层条件。"
    content_to_preserve: "24 个月阶段 I–II、全病程研究对象、跨数据库检验、阶段 III 的严格前置条件、投影失败时的独立 SOFA 分支，以及不支持因果网络、连续动力学、控制或数字孪生的边界。"
    acceptance_test: "修改后两句均能在首次阅读中直接标出一个主语和一个主要谓语；每个编号问题句法平行；任何名词前不连续堆叠超过三个未经解释的抽象限定语；所有原有条件和证据边界仍可逐项定位。"
  - finding_id: LANG-007
    severity: minor
    finding_kind: language
    category: "学术语域中的内部版本与流程措辞"
    dossier_locator: "资源现状表（第121–129行）、Key techniques/Evidence chains（第269–320行）、Required analyses（第326–337行）、Identity and final stop boundary（第439行）及参考文献注释（第464–467行）"
    current_problem: "普通研究叙述中混入‘本 v003 只修复’、‘new_idea_required’、‘fallback/stop’、‘no-go’、‘projection-pass’、‘test-dominant component’及‘context/evidence artifacts’等版本控制、流程状态或内部资料称呼。它们不是所给读者可假定掌握的科学术语，并使文体在学术方案与内部执行记录之间切换。"
    target_state: "研究正文仅保留科学条件、分析操作和相应后果；版本变更与内部资料状态放在机器元数据或独立版本记录中，不进入面向研究者的论述。"
    required_change_or_replacement: "把每个内部短语改为其科学含义，例如将‘data-access no-go’改为‘因数据访问条件不足而停止该研究路线’，将‘fallback/stop’改为‘改用预设替代分析/停止新结局分析’，将‘projection-pass’改为‘满足投影适用性标准的分支’，将‘test-dominant component’首次写成其患者—医院连通分量处理规则；删除第439行关于 v003 修复内容和‘new_idea_required’的内部版本说明，或移至非读者正文的版本记录。"
    content_to_preserve: "所有停止条件、替代分析条件、数据访问限制、患者—医院连通分量规则、投影适用性判断，以及研究对象边界确有变化时需重新立项的科学含义。"
    acceptance_test: "全文检索所列内部短语：正文中均已替换为可独立理解的中文科学条件、操作或后果；保留的必要英文统计缩写均在首次出现处定义；版本号和内部产物名称只出现在机器元数据、来源引用或明确的版本记录中。"
unresolved_issues:
  - TERM-001
  - TERM-002
  - TERM-003
  - TERM-004
  - TERM-005
  - LANG-006
  - LANG-007
---

# Language Assessment Report

**Assessment ID**: language-assessment-r082  
**Target Language**: Chinese  
**Discipline**: 重症医学与临床流行病学，兼具纵向统计、系统辨识和医学人工智能方法  
**Target Journal**: 未指定  
**Scope**: 完整 Idea dossier  
**Date**: 2026-07-19

---

## Overall Language Readiness

**Level**: major_language_revision

**Recommendation**: revise_language

---

## Dimension Scores

| Dimension | Score (1–10) | Severity |
|-----------|-------------|----------|
| Grammar & Syntax | 8 | pass |
| Academic Register & Tone | 6 | borderline |
| Terminology Consistency | 4 | fail |
| Tense & Voice Conventions | 9 | pass |
| Conciseness & Redundancy | 4 | fail |
| Readability & Flow | 5 | borderline |

---

## Hard Gate Status

**Overall**: fail

| Gate | Status | Detail |
|------|--------|--------|
| Grammar error density | pass | 未见达到阈值的明确语法错误；明确错误低于 3/500 词 |
| Academic register | pass | 无两个章节呈现系统性口语；主要问题是内部流程式和中英混合表达，而非口语化 |
| Terminology coherence | fail | 至少三个核心角色对既定跨学科读者不够一致或未在首次使用时可识别：中心研究对象、模拟准入标准、RCT 可观测投影结局 |
| Tense systematic violation | pass | 计划性研究稳定使用将来或条件表达，未把未完成工作系统写成既有结果 |

---

## Strengths

- 计划、未生成结果和可支持结论之间的时态与证据状态大体分明，未将未来分析普遍写成既成事实。
- 因果、预测、结构解释和随机化证据的语言边界反复保持明确，避免了直接的因果或临床推广式夸张。
- 数值阈值、时间窗、分析人群和停止条件通常给出明确量值，减少了“适当”“较好”等空泛判断。
- 中文语法总体稳定，复杂技术段落虽密集，但主干通常完整，没有普遍的残句或搭配错误。

---

## Specific Issues

### Chinese Academic Clarity

- **LANG-006（major）**：摘要首句和主要研究问题存在限定堆叠，核心主干被多层条件与分支延迟。
- **LANG-007（minor）**：研究正文多处混入版本控制、流程状态和内部资料称呼，削弱面向跨学科研究者的自然学术语域。

### Grammar & Syntax

未发现需要单独列项的系统性语法问题。

### Academic Register & Tone

主要语域问题已记录为 LANG-007；未见系统性口语、感叹或面向读者的随意表达。

### Terminology Consistency

| id | term_or_phrase | locator | reader_effect | action_in_frontmatter |
|---|---|---|---|---|
| TERM-001 | 条件性稀疏 RCT 次要再分析 | 第27、31行 | 修饰语似乎落在错误的研究对象上 | yes |
| TERM-002 | 候选动态系统表征 | 第27、31、39、60、92、370、439行 | 无法确认多个短称是否指同一中心对象 | yes |
| TERM-003 | 绝对恢复/假置信门 | 第32、34、39、66、71、85、107、112、214–226行 | 无法在首次出现处识别评价对象和失败含义 | yes |
| TERM-004 | 投影可观测状态摘要 | 第32、40–42、60、67、242–261、276、314–320行 | 映射、适用性判断和分析结局三种角色混称 | yes |
| TERM-005 | death-ranked SOFA / death-ranked 投影摘要 | 第32、41、252、254、347行 | 两个不同分层结局共享未解释的英文短标签 | yes |

### Tense & Voice Conventions

无单独发现。作为研究设想，全文对计划动作、条件分支和尚未获得的结果使用了合适的前瞻性表达。

### Conciseness & Redundancy

限定堆叠的主要可执行问题见 LANG-006。关于证据边界的重复在不同推理位置可能承担不同功能，本次语言评估不决定删除哪一处科学条件。

### Readability & Flow

读者入口的句法负担见 LANG-006；核心术语的跨段角色混用见 TERM-002 至 TERM-005。

---

## Language Revision Priorities

1. **核心术语**：5 项——先修复标题修饰关系，再统一中心研究对象、模拟准入标准和 RCT 两类结局的名称与首次定义。
2. **中文清晰度**：1 项——重组摘要首句和主要研究问题，使核心主干先出现，条件分支保持平行。
3. **学术语域**：1 项——将内部版本、流程状态和软件式短语改为直接的科学条件、操作与后果。

---

## Re-Assessment Status (if applicable)

不适用。本次是对 v003 完整 dossier 的全新独立评估，未读取匿名问题清单、先前评分、先前决定、修订差异或其他评审报告。

---

## Assessment Notes

- 目标读者按 reader handoff 界定为重症医学、临床流行病学、纵向统计、系统辨识、系统科学、医学人工智能和转化研究人员；不能假定其熟悉项目内部词汇或新造标签。
- 评估仅覆盖中文学术语言、术语可理解性、一致性、简洁性和可读性；不判断科学有效性、研究设计优劣、可行性、新颖性、影响力或期刊适配性。
- 项目输入严格限于所列 dossier 与 reader handoff。术语替换采用 dossier 内可证实的直接描述，没有把未作外部核验的紧凑标签宣称为领域标准术语。
- research-idea.v3 固定标题和字段标签仅作为结构定位使用，未被评分、翻译或列为语言问题。
- 源 dossier 与 reader handoff 均未编辑；本次只新增本 Language Assessment Report。
