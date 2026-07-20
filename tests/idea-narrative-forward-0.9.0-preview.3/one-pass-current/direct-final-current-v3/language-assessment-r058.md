---
review_id: language-assessment-r058
reviewer_skill: academic-language-assessor
reviewer_instance_id: academic-language-assessor-r058-fresh-001
workflow_id: RID-SEPSIS-CSM-20260717-001
round_id: r058
input_artifact_ids:
  - idea-dossier-I01-001-v036
  - reader-handoff-forward-001
input_versions:
  - v036
  - v001
scope: complete_idea_dossier
dossier_ref:
  artifact_id: idea-dossier-I01-001-v036
  version: v036
  path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v3/idea-dossier-v036.md
reader_handoff:
  artifact_id: reader-handoff-forward-001
  version: v001
  path: tests/idea-narrative-forward-0.9.0-preview.3/run-001/inputs/reader-handoff.yaml
files_read:
  - AGENTS.md
  - research-skills-openai/skills/academic-language-assessor/SKILL.md
  - research-skills-openai/skills/academic-language-assessor/references/language-assessment-rubric.md
  - research-skills-openai/skills/academic-language-assessor/references/language-hard-gates.md
  - research-skills-openai/skills/academic-language-assessor/references/terminology-review.md
  - research-skills-openai/skills/academic-language-assessor/references/chinese-academic-language-conventions.md
  - research-skills-openai/skills/academic-language-assessor/references/discipline-language-conventions.md
  - research-skills-openai/skills/academic-language-assessor/templates/language-assessment-report.md
  - research-skills-openai/skills/academic-language-assessor/scripts/validate_language_assessment.py
  - tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v3/idea-dossier-v036.md
  - tests/idea-narrative-forward-0.9.0-preview.3/run-001/inputs/reader-handoff.yaml
isolation_mode: fresh_subagent
prior_scores_visible: false
source_edits_performed: false
decision: major_language_revision
findings:
  - finding_id: LANG-R058-01
    severity: major
    category: terminology_modifier_attachment
    dossier_locator:
      - "标题及 Title, summary, audience, and positioning（第 39、43、46 行）"
      - "Objectives 4（第 91 行）"
      - "Conditional trial-observation projection（第 256–275 行）"
      - "Evidence chain: 条件性稀疏 RCT 访视结局及 Planned outputs（第 328–333、351 行）"
    current_problem: >-
      “条件性稀疏随机对照试验次要再分析”“条件性稀疏 RCT”及“稀疏 D1/D4/D7”使“稀疏”在通常句法中修饰试验或日期，而实际所指是稀疏的访视测量数据。该短语位于标题、摘要和目标中，目标读者可能把它理解为稀疏试验设计、小样本试验或稀疏随机化。
    target_state: >-
      让“稀疏”只修饰“访视数据/访视测量”，并让“条件性”明确修饰次要分析的启动条件，而不修饰 RCT 本身。
    required_change_or_replacement: >-
      标题可改为“脓毒症全病程候选动态系统表征：跨数据库检验计划及基于稀疏访视数据的条件性随机对照试验次要分析”；正文统一使用“基于稀疏访视数据的条件性 RCT 次要分析”或等义的完整描述，并把“稀疏 D1/D4/D7”改为“D1、D4、D7 的稀疏访视数据”。
    content_to_preserve: >-
      保留阶段 III 位于 24 个月最低交付之后、逐试验核验适用条件、EXIT-SEP 与 XBJ-SCAP 分开分析以及 D7/D8 实际访视的全部边界。
    acceptance_test: >-
      重读标题、完整 Idea 摘要、目标 4、阶段 III 方法、证据链和计划产物；每一处“稀疏”均只附着于“访视数据/测量”，每一处“条件性”均指向分析启动条件，且不再出现“稀疏 RCT”“稀疏随机对照试验”或“稀疏 D1/D4/D7”。
  - finding_id: LANG-R058-02
    severity: major
    category: endpoint_concordance
    dossier_locator:
      - "One-sentence complete-Idea summary（第 44 行）"
      - "Primary research question 与 Objective 4（第 84、91 行）"
      - "跨数据映射成立时的估计目标及独立 SOFA 分析（第 266–273 行）"
      - "阶段 III evidence chain、planned outputs、interpretation matrix 和 evidence ladder（第 331–333、351、368–369、383–384 行）"
      - "Title and positioning claim-support table（第 407–408 行）"
    current_problem: >-
      核心结局交替称为“实测指标汇总结局”“实测指标汇总访视结局”“访视结局”和“按死亡和出院分层的 SOFA 访视结局”。前两种名称没有说明映射分支也把死亡置于最差层、活着出院置于最有利层，只用实测指标代理值排序在院存活者；摘要则只在替代分支中明说死亡/出院分层。因而同一核心终点在摘要、目标、方法和解释矩阵中的组成看似不同。
    target_state: >-
      为映射分支和独立 SOFA 分支各保留一个角色明确的完整名称，并在首次出现时说明死亡、活着出院和在院存活者的排序规则；之后才使用稳定短称。
    required_change_or_replacement: >-
      首次描述映射分支时写为“死亡最差、活着出院最有利、在院存活者按实测指标汇总代理值排序的 D7/D8 分层访视结局”，其后可简称“实测指标代理值分层访视结局”；替代分支写为“死亡最差、活着出院最有利、在院存活者按 SOFA 排序的独立 D7/D8 分层访视结局”，其后简称“独立 SOFA 分层访视结局”。摘要、目标、方法、证据链、解释矩阵和定位表均按这两个名称对齐。
    content_to_preserve: >-
      保留 P_obs 与 SOFA 两条分支的适用条件、死亡和活着出院的层级、在院存活者的排序变量、分试验估计目标，以及概率指数/胜率作为组间比较量。
    acceptance_test: >-
      全 dossier 检查“结局”“访视结局”“汇总结局”和“SOFA 结局”的每一处核心用法；所有出现均能唯一映射到上述两条分支之一，首次出现含完整层级定义，后续短称不丢失分支角色，摘要与第 266–273 行的方法定义一致。
  - finding_id: LANG-R058-03
    severity: major
    category: cross_database_task_and_status_terminology
    dossier_locator:
      - "One-sentence summary、Structured abstract 和 Core hypothesis（第 44、51–53、95 行）"
      - "milestones、minimum success 和 work packages（第 103–125 行）"
      - "Hospital-primary genuine cross-database validation（第 244–254 行）"
      - "跨数据库 evidence chain 与 interpretation matrix（第 321–326、355–370 行）"
      - "closest-work comparison、claim-support table、limitations 和 risks（第 393–406、433–450 行）"
    current_problem: >-
      跨数据库工作的对象、分析设置和结果状态在“未触碰（测试/数据库/跨库结果）”“零更新”“冻结跨库成功”“运输/运输性/运输更新”“跨数据库检验/验证/稳定”等表达之间切换。“未触碰”和“零更新”是项目或软件式简称；“运输”又可能被理解为数据搬运。目标读者不能据此稳定区分独立测试数据、参数更新规则、检验动作和达到阈值后的结论。
    target_state: >-
      用四个互不混淆的角色描述：独立外部测试数据、参数完全固定的外部检验、仅在适配数据中进行的有限更新，以及达到预设阈值后的跨数据库稳定性结论。
    required_change_or_replacement: >-
      首次出现时写明“完全独立、未用于模型开发、变量或阈值选择及参数估计的外部测试集”，后续简称“独立外部测试集”；把“零更新”展开为“所有模型参数保持固定的外部检验”；把“运输/运输更新”改为“在另一数据库中的适用性”或直接写明“仅用适配区估计校准参数/观测层参数后的外部表现”；仅在标准实际达到时使用“跨数据库稳定”，计划阶段使用“跨数据库稳定性检验”。
    content_to_preserve: >-
      保留医院优先分区、跨分区患者排除、测试数据不参与开发、完全固定参数与两种有限更新分开报告、全模型重拟合作为新开发，以及阶段 II 合取判定。
    acceptance_test: >-
      全 dossier 对“未触碰、零更新、冻结、运输、运输性、检验、验证、稳定”作语境复核；数据集、参数状态、分析动作和结果结论各有唯一表述，摘要首次出现已能被所列跨学科读者理解，且不再以“未触碰”“运输”或未定义的“零更新”代替科学条件。
  - finding_id: LANG-R058-04
    severity: major
    category: model_disposition_and_output_terminology
    dossier_locator:
      - "Structured abstract: Expected result（第 53 行）"
      - "milestones、work packages 和 simulation standards（第 109、123–125、230–242 行）"
      - "Key techniques and implementation（第 287–296 行）"
      - "Required analyses、planned outputs 和 risks（第 337、349–350、448、454 行）"
    current_problem: >-
      “准入”“弃权”“失败图”“冻结包/冻结清单”等简称承担候选模型是否继续、哪些量不再解释以及失败如何呈现等关键科学状态，但首次出现时没有说明其具体动作。“弃权”尤其可能指选择性预测、模型拒答、淘汰模型或研究者停止结构解释；“失败图”也不能让读者知道是诊断图、流程图还是按失败条件归类的结果图。
    target_state: >-
      每个模型处置状态直接说明触发条件、允许继续的分析和停止解释的对象；每个交付物名称直接说明其内容。
    required_change_or_replacement: >-
      把“模型准入”首次展开为“候选模型达到预设模拟恢复标准后进入主要任务检验”；按具体语境把“弃权”改为“停止该模型分支”“不作该状态/边的结构解释”或“不给出预测”；把“失败图”改为“按预设失败条件归类的结果图表”；把“冻结包/清单”改为“预先确定且不得根据外部测试结果修改的模型、参数、阈值和代码清单”。
    content_to_preserve: >-
      保留所有模拟阈值、降级路线、删除/合并规则、外部测试前的锁定边界、失败结果也须交付，以及不以预测排名挽救结构失败的限制。
    acceptance_test: >-
      逐一复核摘要、里程碑、模拟标准、实现表、必要证据、计划产物和风险表中的模型处置词；每个词都能直接回答“触发什么、停止或继续什么、交付什么”，且不再使用未定义的“弃权”“失败图”“准入”或“冻结包”作为唯一说明。
  - finding_id: LANG-R058-05
    severity: minor
    category: central_object_role_concordance
    dossier_locator:
      - "标题、摘要、Research question 和 Objectives（第 39–54、84–95 行）"
      - "simulation standards、interpretation matrix 和 contribution（第 230–242、364–376 行）"
      - "claim-support table 与 final stop boundary（第 405、463 行）"
    current_problem: >-
      中心对象在“候选动态系统表征、全病程候选表征、受限表示、候选状态表示、候选模型、阶段 II 模型、最小全病程候选表示”之间切换，但没有用一句话说明“表征”“模型实现”和“对齐后的状态量”的层级关系，读者可能把科学对象与其候选计算模型视为同义。
    target_state: >-
      以“脓毒症全病程候选动态系统表征”为中心对象的唯一全称；仅在定义后使用“候选表征”，并把“候选模型/阶段 II 选定模型”和“状态表示”限定为明确的实现或数学对象。
    required_change_or_replacement: >-
      在摘要或研究问题后增加一句简短角色说明，并按角色统一后文称谓；不要用“阶段 II 模型”指代整个研究对象，也不要在未说明关系时交替使用“表征”和“表示”。
    content_to_preserve: >-
      保留简单基线、至多一个附加候选模型、潜在状态 X_t、对齐后的可解释量和阶段 II 的降级路线。
    acceptance_test: >-
      全 dossier 中中心科学对象只保留上述全称及已定义短称；每个“模型”均指具体计算模型，每个“状态表示”均指明确数学对象，标题、研究问题、核心假设、解释矩阵和最终边界的指称一致。
  - finding_id: LANG-R058-06
    severity: minor
    category: bilingual_terminology_and_formatting
    dossier_locator:
      - "G1 audit、cross-database validation 和 implementation tables（第 137、156–167、191–205、215–220、246、288–295 行）"
      - "Working assumptions 和 risks（第 426–449 行）"
    current_problem: >-
      同一概念在中英文之间来回切换，如“校验和/checksum”“SOFA 基线/baseline SOFA”“事件时刻/event time”“适当概率评分/proper score”，并保留未解释的 transient、absorbing、terminal competing、threshold registry、tie rule 等英文片段；“12 小时/12h”和“24 小时/24h”也未统一。
    target_state: >-
      中文正文采用稳定中文术语，确需保留的英文或缩写在首次出现时给出中英文对应，之后只保留一种形式；时间单位格式一致。
    required_change_or_replacement: >-
      例如统一用“校验和”“SOFA 基线”“事件时刻”“适当评分规则”“阈值登记表条目”“并列时的判定规则”，并在状态表首次给出“暂态/吸收态/终末竞争事件”等对应；全篇统一“12 小时、24 小时”或由同一版式规则处理。
    content_to_preserve: >-
      保留数据库名、试验名、标准缩写、数学符号、D7/D8、模型指标和可复现所需的技术含义。
    acceptance_test: >-
      对上述触发词作全篇检查；每个概念只有一种主形式，首次双语对应完整，后续不无故切换，时间单位和中英文标点一致。
  - finding_id: LANG-R058-07
    severity: minor
    category: concision_and_stacked_qualifiers
    dossier_locator:
      - "One-sentence complete-Idea summary（第 44 行）"
      - "Core hypothesis 与 minimum success definition（第 95、116 行）"
      - "Required analyses and evidence（第 337、339 行）"
      - "Contribution and evidence ladder、Remaining execution requirements（第 376、459 行）"
    current_problem: >-
      多处单句同时堆叠数据条件、时间条件、模型条件、例外分支、状态限定和交付清单，主语—动作—对象被长串定语与分号后的新层级掩盖。完整 Idea 摘要虽需保持单句，但目前读者需回读才能区分阶段 II 主线与阶段 III 条件分支。
    target_state: >-
      每句先给中心动作和对象，再按“条件—动作—否则”的平行顺序安放限定；非单句字段拆成两至三句，清单移入并列项目或表格。
    required_change_or_replacement: >-
      保持摘要为一句，但前置阶段 I–II 主目标，把阶段 III 作为句末独立条件分句；将第 337、339、376、459 行按证据类别或阶段拆句，删除已由邻近表格完整表达的重复修饰。
    content_to_preserve: >-
      保留所有科学边界、条件分支、停止条件和明确未生成状态；不得因压缩而删除不同阶段所需的独立条件。
    acceptance_test: >-
      目标读者可在首次阅读时从每句识别主语、主要动作、对象、证据状态和条件分支；非模板要求的句子不再承载三个以上彼此独立的条件层级，摘要仍保持单句且两阶段关系清楚。
  - finding_id: LANG-R058-08
    severity: minor
    category: local_syntax_and_calque
    dossier_locator:
      - "milestones 与 risk alternatives（第 108、445 行）"
      - "Protocol locks 引导句（第 191 行）"
      - "cross-database support rule（第 252 行）"
    current_problem: >-
      “改为并预先固定 24 小时或事件时间”缺少“改用/固定为”的完整搭配；“在真实分布处期望最优”是英语式压缩，不能自然说明适当评分规则；“只报告数据库级运输或描述”并列成分不完整。
    target_state: >-
      使用完整、自然且可直接理解的中文谓语搭配。
    required_change_or_replacement: >-
      分别改为“改用并预先固定为 24 小时时间格或事件时间方案”；“当预测分布等于真实分布时，其期望评分达到最优”；“只报告在该数据库层面的表现，或仅作描述性分析”。
    content_to_preserve: >-
      保留时间方案降级规则、适当评分规则的定义功能和外部支持不足时的降级边界。
    acceptance_test: >-
      四处句子均有完整谓语和并列结构，不再依赖英语词序或省略关键中心词，且原有科学条件不变。
unresolved_issues:
  - LANG-R058-01
  - LANG-R058-02
  - LANG-R058-03
  - LANG-R058-04
  - LANG-R058-05
  - LANG-R058-06
  - LANG-R058-07
  - LANG-R058-08
---

# Language Assessment Report

**Assessment ID**: language-assessment-r058  
**Target Language**: Chinese（zh-CN，含必要英文术语与缩写）  
**Discipline**: 重症医学、临床流行病学、纵向统计、系统辨识、系统科学与医学人工智能  
**Target Journal**: 未指定  
**Scope**: complete_idea_dossier  
**Date**: 2026-07-19

---

## Overall Language Readiness

**Level**: major_language_revision

**Recommendation**: revise_language

全文总体语法稳健、语域正式，计划、待核实事项与尚未生成结果的时态和证据状态也基本一致。当前阻断提交准备度的是四组核心命名问题：标题中的修饰关系、两条阶段 III 结局的全篇指称、跨数据库检验的任务/参数/结果状态，以及候选模型的处置与失败产物名称。共记录 0 项 critical、4 项 major、4 项 minor。

---

## Dimension Scores

| Dimension | Score (1–10) | Severity |
|-----------|-------------|----------|
| Grammar & Syntax | 8 | pass |
| Academic Register & Tone | 7 | pass |
| Terminology Consistency | 4 | fail |
| Tense & Voice Conventions | 9 | pass |
| Conciseness & Redundancy | 5 | borderline |
| Readability & Flow | 6 | borderline |

---

## Hard Gate Status

**Overall**: fail

| Gate | Status | Detail |
|------|--------|--------|
| Grammar error density | pass | 明确语法错误估计少于 1 项/500 字；未见系统性语法障碍 |
| Academic register | pass | 无两个以上章节出现系统性非正式语域；问题主要是内部化技术简称，而非口语化 |
| Terminology coherence | fail | 4 组核心命名存在误导性修饰、分支指称不一致或读者不可及的简称；标题中的“稀疏随机对照试验”本身已构成误导性核心术语 |
| Tense systematic violation | pass | 这是前瞻性研究构想；计划、条件性动作、当前未核实状态和尚未生成结果的表达一致，无 Methods/Results 式系统时态冲突 |

---

## Strengths

- 全文持续区分“计划开展”“当前未核实”和“尚未生成”，没有把拟议模型、跨数据库结果或 RCT 次要分析写成既有发现。
- “临床事件时刻”与“标签可用时刻”先用自然语言说明，再引出“双时钟”；这一术语铺垫符合跨学科读者的知识基线。
- 主要分析任务、次要诊断性分析和阶段 III 条件分支在方法层面的数量与顺序总体一致，且因果、预测和结构解释边界措辞克制。
- 中文语域整体正式客观，未见宣传性断言、口语表达或无依据的“首创”“突破”等措辞。
- 多数缩写在首次关键使用处有中文全称或功能说明，数学符号与变量角色表也提供了必要的局部定位。

---

## Specific Issues

### Chinese Academic Clarity (if applicable)

- **LANG-R058-07（minor）**：第 44、95、116、337、339、376、459 行存在条件和定语层级堆叠。摘要可继续保持单句，但应先陈述阶段 I–II 的主动作，再用平行条件分句引出阶段 III；其余长句宜按阶段或证据类别拆分。
- **LANG-R058-08（minor）**：第 108、191、252、445 行有局部不完整搭配或英语式压缩。建议分别采用“改用并预先固定为……”“当预测分布等于真实分布时，其期望评分达到最优”“只报告……表现，或仅作描述性分析”等完整句式。

### Grammar & Syntax

- 未见达到硬门槛的语法错误密度。可定位的局部问题集中在 LANG-R058-08，不影响大部分段落的理解，但应在术语修改后统一校读。

### Academic Register & Tone

- 正式语域通过。LANG-R058-03 与 LANG-R058-04 所述“未触碰、零更新、弃权、失败图”等不是口语问题，而是项目/软件式简称进入研究者正文后造成的角色不透明，应按科学条件展开。

### Terminology Consistency

#### LANG-R058-01 — 标题中“稀疏”的修饰对象（major）

- **Dossier locator**：第 39、43、46、91、256–275、328–333、351 行。
- **Current problem**：“稀疏”按通常句法修饰 RCT 或日期，不能准确指向稀疏访视测量。
- **Target state**：“稀疏”只修饰“访视数据/测量”，“条件性”只修饰次要分析的启动。
- **Required change or replacement**：统一为“基于稀疏访视数据的条件性 RCT 次要分析”；标题使用 frontmatter 中给出的完整候选表述。
- **Content to preserve**：阶段 III 的时间边界、逐试验条件、分开分析和实际 D7/D8 访视。
- **Acceptance test**：全 dossier 不再出现“稀疏 RCT/稀疏随机对照试验/稀疏 D1/D4/D7”，且每处修饰关系唯一。

#### LANG-R058-02 — 两条阶段 III 结局的全篇指称（major）

- **Dossier locator**：第 44、84、91、266–273、331–333、351、368–369、383–384、407–408 行。
- **Current problem**：“实测指标汇总结局”等短称省略了死亡、活着出院和在院存活者的层级，摘要与方法看似定义了不同结局。
- **Target state**：映射分支和独立 SOFA 分支各有一个完整定义和一个稳定短称。
- **Required change or replacement**：采用“实测指标代理值分层访视结局”和“独立 SOFA 分层访视结局”，并在首次出现时写全死亡/出院/在院存活者排序规则。
- **Content to preserve**：P_obs 与 SOFA 的分支条件、层级规则、分试验目标和概率指数/胜率。
- **Acceptance test**：所有核心结局用法均唯一对应两条分支之一，摘要与第 266–273 行一致。

#### LANG-R058-03 — 跨数据库任务、参数设置与结果状态（major）

- **Dossier locator**：第 44、51–53、95、103–125、244–254、321–326、355–370、393–406、433–450 行。
- **Current problem**：“未触碰、零更新、冻结、运输/运输性、检验/验证/稳定”混合表示数据、参数、动作与结论。
- **Target state**：独立外部测试数据、参数完全固定的检验、有限更新和跨数据库稳定性结论四个角色分开命名。
- **Required change or replacement**：使用 frontmatter 中的描述性表述，不以“未触碰”“运输”或未定义“零更新”作为唯一名称。
- **Content to preserve**：医院级隔离、患者排除、测试集不参与开发、更新层级和阶段 II 合取判定。
- **Acceptance test**：全 dossier 每个相关词均只承担一个角色，计划动作不预写成已验证状态。

#### LANG-R058-04 — 模型处置和失败产物（major）

- **Dossier locator**：第 53、109、123–125、230–242、287–296、337、349–350、448、454 行。
- **Current problem**：“准入、弃权、失败图、冻结包/清单”没有直接说明触发条件、停止对象或交付内容。
- **Target state**：每个状态直接说明达到何种标准、继续或停止哪项分析、哪些量不再解释以及交付何种图表。
- **Required change or replacement**：展开为“达到模拟恢复标准后进入主要任务检验”“停止该模型分支/不作相应结构解释”“按预设失败条件归类的结果图表”“预先确定且不得据外部结果修改的模型与代码清单”。
- **Content to preserve**：全部阈值、降级路线、删除/合并规则、锁定边界和失败结果交付。
- **Acceptance test**：各章节不再用上述简称代替具体科学动作。

#### LANG-R058-05 — 中心对象与模型实现的角色关系（minor）

- **Location and issue**：第 39–54、84–95、230–242、364–376、405、463 行在“候选动态系统表征/表示/状态表示/候选模型/阶段 II 模型”间切换，未明示层级。
- **Direction**：以“脓毒症全病程候选动态系统表征”为唯一全称，定义短称；“模型”只指计算实现，“状态表示”只指明确数学对象，并作全篇角色检查。

#### LANG-R058-06 — 中英文术语与格式（minor）

- **Location and issue**：第 137、156–167、191–205、215–220、246、288–295、426–449 行存在“校验和/checksum”“SOFA 基线/baseline SOFA”等切换及未解释英文片段。
- **Direction**：中文术语为主，必要英文在首次出现时给出对应，后文只用一种形式；统一时间单位和中英文标点。

| id | term_or_phrase | locator | reader_baseline | problem | recommended_replacement | first_use_definition | basis | acceptance_test |
|---|---|---|---|---|---|---|---|---|
| LANG-R058-01 | 条件性稀疏 RCT | 第 39、43、46、91、256–275、328–333、351 行 | 不假定熟悉项目新标签；跨学科一般方法知识 | “稀疏”错误附着于 RCT/日期 | 基于稀疏访视数据的条件性 RCT 次要分析 | 在适用条件成立时，基于 D7/D8 稀疏实际访视数据开展的分试验次要分析 | 句法修饰关系与 dossier 自身的方法定义；未作外部检索 | 全篇“稀疏”仅修饰访视数据 |
| LANG-R058-02 | 实测指标汇总结局 / 访视结局 / SOFA 结局 | 第 44、84、91、266–273、331–333、351、368–369、383–384、407–408 行 | 熟悉临床结局，但不应猜测项目特定层级 | 名称未稳定呈现死亡、出院和在院存活者排序 | 实测指标代理值分层访视结局；独立 SOFA 分层访视结局 | 首次分别写全三层及排序变量 | 全篇内部定义与指称比较；未作外部检索 | 每一处结局名唯一对应一个分支 |
| LANG-R058-03 | 未触碰 / 零更新 / 运输性 / 跨库稳定 | 第 44、51–53、95、103–125、244–254、321–326、355–370、393–406、433–450 行 | 熟悉外部验证概念，但不熟悉项目内部简称 | 混合数据身份、参数状态、分析动作和结果结论 | 独立外部测试集；参数完全固定的外部检验；适配区有限更新；跨数据库稳定性 | 首次明确测试数据未参与开发、选择或估计 | reader handoff 与文本内部角色比较；未作外部检索 | 四个角色全篇互不替代 |
| LANG-R058-04 | 准入 / 弃权 / 失败图 / 冻结包 | 第 53、109、123–125、230–242、287–296、337、349–350、448、454 行 | 不熟悉项目工作用语 | 无法直接识别继续、停止和交付动作 | 达标后进入主要任务；停止分支/不作结构解释；按失败条件归类的结果图表；预先锁定的模型与代码清单 | 首次直接写出触发条件、对象和动作 | reader handoff 与局部语义；未作外部检索 | 不保留无定义简称作为唯一说明 |
| LANG-R058-05 | 候选动态系统表征 / 表示 / 候选模型 / 阶段 II 模型 | 第 39–54、84–95、230–242、364–376、405、463 行 | 对各参与学科仅有一般知识 | 科学对象与计算实现的层级未明 | 中心对象统一为“脓毒症全病程候选动态系统表征”，其余按实现角色命名 | 首次说明表征、候选模型和状态量的关系 | 全篇内部指称比较；未作外部检索 | 每个形式只对应一个角色 |

以上仅列出触发问题的术语，不是全篇术语清单。

### Tense & Voice Conventions

none。全文作为前瞻性 Idea dossier，使用“拟、将、若……则、尚未、不能”等形式区分计划动作、条件结果和当前证据状态；未发现把计划工作系统写成已完成结果的时态问题。

### Conciseness & Redundancy

- LANG-R058-07 所列句子存在多层限定堆叠。修改时应保留科学上不同的条件，不应仅因词语相近而删除；重点是重新安排主句和条件层级。
- 限制与停止条件在多个结构化章节中重复出现，但其跨章节必要性属于叙事评估范围。本报告只要求局部句法压缩，不指定删除哪个论证位置。

### Readability & Flow

- 主要阅读障碍来自术语角色切换和长句，而非段落顺序。完成 LANG-R058-01 至 LANG-R058-06 后，再处理 LANG-R058-07 和 LANG-R058-08，可避免在旧术语上进行无效润色。

---

## Language Revision Priorities

1. **Terminology Consistency**：4 项 major — 先修正标题修饰关系、两条阶段 III 结局名称、跨数据库检验角色和模型处置词。
2. **Central-object concordance**：1 项 minor — 明确“表征—候选模型—状态量”的层级并作全篇一致性检查。
3. **Bilingual consistency**：1 项 minor — 统一中英文术语、缩写首用和时间单位。
4. **Concision and syntax**：2 项 minor — 在术语稳定后重排堆叠条件并修正四处不自然搭配。

---

## Re-Assessment Status (if applicable)

不适用。本次为 Idea dossier 的全新独立评估，未读取匿名问题清单、先前文本、修订差异、先前评分或先前决定。

| Check | Current assessment |
|--------|--------------------|
| Listed issues no longer present | 不适用 |
| Listed issues still present | 不适用 |
| New current-text issues | LANG-R058-01 至 LANG-R058-08 |

---

## Assessment Notes

- 评估范围仅为绑定的 v036 dossier 与 v001 reader handoff；dossier frontmatter 中列出的其他产物没有被读取，引用文献也未用于判断科学正确性。
- 目标读者按 handoff 处理为具有重症研究、纵向数据、验证和不确定性一般知识，但不熟悉项目内部词汇、隐喻或新造简称的跨学科研究者。
- 本次未进行 focused verification。阻断结论来自标题的句法修饰关系、同一 dossier 内的分支指称不一致和 reader handoff 明示的知识基线；建议均为描述性表述，不声称某个替代短语是经外部来源验证的标准术语。验证结果：不适用，未检索外部术语来源。
- 未建立术语登记表或证据包，也未采用词频阈值。术语表仅覆盖实际触发问题的五组表达，并完成了中心对象、主要终点、主要任务、诊断性分析和证据状态的全篇临时一致性检查。
- 本报告只评价语言，不判断研究设计、统计阈值、科学有效性、新颖性、影响或期刊适配性；未修改源 dossier。
