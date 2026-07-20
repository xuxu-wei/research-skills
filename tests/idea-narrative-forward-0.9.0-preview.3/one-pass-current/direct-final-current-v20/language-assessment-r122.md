---
review_id: language-assessment-I01-001-r122
reviewer_skill: academic-language-assessor
reviewer_instance_id: /root/old_language_r122
workflow_id: RID-SEPSIS-CSM-20260717-001
round_id: r122
input_artifact_ids:
  - idea-dossier-I01-001-v054
input_versions:
  - v054
scope: complete_idea_dossier
dossier_ref:
  artifact_id: idea-dossier-I01-001-v054
  version: v054
  path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v20/idea-dossier-v054.md
reader_handoff:
  artifact_id: embedded-reader-handoff
  version: embedded
  path: null
files_read:
  - tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v20/idea-dossier-v054.md
isolation_mode: fresh_subagent
prior_scores_visible: false
source_edits_performed: false
decision: minor_language_revision
coverage_receipt:
  reader_entry:
    status: completed
    reviewed_count: 12
    basis: "完整检查标题及标题字段、完整 Idea 摘要、结构式摘要五个字段、主要研究问题和核心假设；未因首个问题而提前结束句内检查。"
  core_scientific_role:
    status: completed
    reviewed_count: 10
    basis: "检查 dossier 实际出现的研究对象、两项主要任务、状态与转移表征、两项次要诊断、独立外部检验、条件性试验分析、失败输出和贡献等读者名称。"
  terminology_concordance:
    status: completed
    reviewed_count: 8
    basis: "对普通阅读触发的八个核心或后果性概念簇完成首次定义、跨位置同义项和读者知识基线检查；其中五个形成可执行术语 finding。"
  local_language:
    status: completed
    reviewed_count: 371
    basis: "逐一检查正文 371 个非空行中的段落、列表项、表格行、公式说明与参考文献条目，覆盖语法、语域、时态、局部连贯和冗余。"
findings:
  - finding_id: LANG-R122-001
    severity: minor
    finding_kind: terminology
    finding_level: meso
    finding_scope: concept_cluster
    scientific_role: independent-external-test-evidence
    normalized_locator: reader-entry-methods-evidence-and-risk-sections
    failure_mode: physical-metaphor-conflates-data-isolation-test-operation-and-result
    fingerprint: meso|independent-external-test-evidence|reader-entry-methods-evidence-and-risk-sections|physical-metaphor-conflates-data-isolation-test-operation-and-result
    category: terminology-naturalness-and-role-separation
    dossier_locator: "结构式摘要 Objective and hypothesis、Expected result、Contribution and impact；Objectives 3；Core hypothesis；时间节点、WP4、公共数据库角色；主要任务协议；Hospital-primary cross-database validation；试验观测映射；Key techniques；Evidence chains；Expected outputs；Interpretation matrix；Contribution、Claim-Support、Risks（行 45、47-48、82、89、105、127、130、152、207、259、292、325、391、403、415、421、427、448、450、492、494）"
    current_problem: "“未触碰”把物理接触隐喻用于三种不同角色：冻结前的数据访问隔离、冻结模型且不更新的独立外部检验，以及该检验产生的结果。附近方法能够恢复其含义，但跨学科读者需反复推断短语究竟指数据状态、分析操作还是结果来源。"
    target_state: "分别用直接描述标明数据隔离、分析操作和结果来源；首次出现时说明独立外部测试集在模型与判定标准冻结前保持不可访问且不参与开发，后文按角色使用“独立外部测试集”“冻结模型的不更新外部检验”或“独立外部检验结果”。"
    required_change_or_replacement: "将表示数据分区的“未触碰测试区/最终测试区/测试资料”改为“冻结前保持不可访问且不参与开发的独立外部测试集”（首次）或“独立外部测试集”（后续）；将表示分析操作的“未触碰数据库/跨数据库检验”改为“使用冻结模型且不作更新的独立外部检验”；将表示产出的“未触碰外部/跨数据库结果”改为“独立外部检验结果”。不要用一个新短标签统称这三种角色。"
    content_to_preserve: "第二数据库的医院级适配区与最终测试区隔离、冻结前不可访问、测试资料不参与变量或模型及阈值选择、不更新外部检验优先于有限适配、只分析一次、失败结论不得由适配补偿，以及全部数值标准和时间节点。"
    acceptance_test: "全篇检索不再出现“未触碰”；每个原位置均能仅凭本句区分数据分区、分析操作或结果来源；首次定义明确冻结前不可访问且不参与开发；不更新、有限适配、一次分析和失败解释均未改变。"
    term_or_phrase: "未触碰（数据库、测试区、外部结果、跨数据库资料或检验）"
    recommended_form_or_plain_description: "按科学角色分别写为“冻结前保持不可访问且不参与开发的独立外部测试集”“使用冻结模型且不作更新的独立外部检验”或“独立外部检验结果”"
    evidence_basis: "dossier 自身在 Hospital-primary cross-database validation 中已直接规定权限隔离、冻结、一次分析和不更新操作；因此可用这些现有科学条件作直接描述，无须保留或另造压缩标签。"
    first_use_definition: "独立外部测试集是指在模型、预处理、更新操作、指标和判定标准冻结前保持不可访问，且不用于变量、模型或阈值选择的数据分区。"
    competing_forms_and_locators:
      - "未触碰数据库检验：行 45"
      - "未触碰跨数据库结果/检验/资料/支持：行 47-48、130、391、415、421、450"
      - "未触碰外部数据库：行 89"
      - "未触碰最终测试区：行 82、259"
      - "未触碰测试区/测试/测试资料：行 105、152、207、325、427、448"
      - "未触碰外部结果：行 127、403、494"
      - "未触碰 eICU 不更新外部检验：行 292"
      - "未触碰的不更新外部检验证据：行 492"
  - finding_id: LANG-R122-002
    severity: minor
    finding_kind: terminology
    finding_level: meso
    finding_scope: concept_cluster
    scientific_role: stage-two-minimum-success-rule
    normalized_locator: success-definition-downstream-eligibility-and-interpretation
    failure_mode: formal-logic-label-burdens-cross-disciplinary-reader
    fingerprint: meso|stage-two-minimum-success-rule|success-definition-downstream-eligibility-and-interpretation|formal-logic-label-burdens-cross-disciplinary-reader
    category: reader-baseline-and-terminology
    dossier_locator: "时间节点与 Conjunctive minimum success definition、共享前提、Evidence chains、Required analyses、Interpretation matrix、Working assumptions（行 105、108、110、118、286、351、362、378、415、468）"
    current_problem: "“合取定义/合取标准/合取成功/合取表”借用形式逻辑术语命名“所有列出的条件必须同时满足”。统计或系统科学读者可以推断，但临床读者要到后续枚举才能确认含义，而且同一规则有四种压缩形式。"
    target_state: "用一个无需形式逻辑背景的直接表达贯穿成功定义、后续试验资格和解释，例如“全部条件同时满足的阶段 II 最低成功标准”；表格按用途称为“阶段 II 最低成功条件核对表”。"
    required_change_or_replacement: "将标题改为“全部条件同时满足的最低成功定义”；将“合取定义/合取标准/合取成功”统一改为“全部条件同时满足的阶段 II 最低成功标准（或满足该标准）”；将“合取表”改为“阶段 II 最低成功条件核对表”。首次出现后可用“阶段 II 最低成功标准”，但不得缩回“合取”。"
    content_to_preserve: "五项成功条件的全部内容、条件之间的“且”关系、阈值只能收紧不能放宽、有限适配不得补偿失败、试验分析的阶段 II 前置条件及阶段 III 不补足阶段 II 的边界。"
    acceptance_test: "全篇检索不再出现“合取”；所有原位置均明确表示列出的成功条件必须全部同时满足；成功条件数量、阈值、下游资格和失败后果保持不变。"
    term_or_phrase: "合取定义、合取标准、合取成功、合取表"
    recommended_form_or_plain_description: "全部条件同时满足的阶段 II 最低成功标准；阶段 II 最低成功条件核对表"
    evidence_basis: "dossier 行 110-116 已以五项编号条件完整表达逻辑关系；直接复述“全部条件同时满足”比项目内逻辑标签更适合声明的跨学科读者。"
    first_use_definition: "阶段 II 只有在下列五项最低条件全部同时满足时才判定成功。"
    competing_forms_and_locators:
      - "合取定义：行 105"
      - "合取标准：行 286、362、415"
      - "合取成功/合取成功判断：行 118、351、468"
      - "合取表：行 378"
  - finding_id: LANG-R122-003
    severity: minor
    finding_kind: terminology
    finding_level: meso
    finding_scope: concept_cluster
    scientific_role: candidate-model-selection-consequence
    normalized_locator: abstract-simulation-implementation-evidence-and-assumptions
    failure_mode: promotion-metaphor-replaces-scientific-analysis-consequence
    fingerprint: meso|candidate-model-selection-consequence|abstract-simulation-implementation-evidence-and-assumptions|promotion-metaphor-replaces-scientific-analysis-consequence
    category: academic-register-and-terminology
    dossier_locator: "Structured abstract Expected result；绝对模拟判定表；Key techniques；Evidence chains；Planned outputs；Falsification；Working assumptions（行 47、246、323、328、343、390、398、465）"
    current_problem: "“晋级/不晋级”是项目流程隐喻，未直接说明未达到恢复标准的复杂候选究竟是不进入临床任务、不进入独立外部检验，还是仅停止结构解释；同一句中的“停止解释”又是另一种科学后果。"
    target_state: "按对象和后果直接写明：复杂候选是否进入后续临床任务与独立外部检验，特定状态或边是否继续作结构性解释，以及是否改用预设的简单表征。"
    required_change_or_replacement: "将“复杂候选不得晋级/不晋级”改为“复杂候选不得进入后续临床任务和独立外部检验”；将“按对象记录……不晋级决定”改为“按对象记录不纳入后续验证或不再作结构性解释的决定”。保留“停止解释”时必须带出对象，例如“停止对该状态或边作结构性解释”。"
    content_to_preserve: "连续或离散状态、边和复杂候选各自的恢复阈值；未达标后的合并、删除、简单模型替代和结构解释限制；预测优势不得改变恢复判定；负责人确认的时间与后果。"
    acceptance_test: "全篇检索不再出现“晋级/不晋级”；每个原位置均明确受影响对象和后续科学动作；状态或边的解释后果不与整个复杂候选的分析资格混为一项。"
    term_or_phrase: "晋级、不晋级"
    recommended_form_or_plain_description: "复杂候选进入或不进入后续临床任务和独立外部检验；状态或边继续或停止结构性解释"
    evidence_basis: "dossier 的恢复标准表、最低路线和外部检验章节已经给出这些具体后果，因而可直接陈述而不依赖项目流程隐喻。"
    first_use_definition: "只有达到全部适用恢复标准的复杂候选才进入后续临床任务和独立外部检验；未达到标准的状态或边不再作结构性解释。"
    competing_forms_and_locators:
      - "不晋级决定：行 47、323、328、343、390"
      - "复杂候选不得晋级：行 246、465"
      - "复杂候选不晋级：行 398"
  - finding_id: LANG-R122-004
    severity: minor
    finding_kind: terminology
    finding_level: meso
    finding_scope: concept_cluster
    scientific_role: observed-data-generating-regime
    normalized_locator: gap-hypothesis-method-and-evidence-ladder
    failure_mode: observation-policy-form-obscures-care-action-and-measurement-process
    fingerprint: meso|observed-data-generating-regime|gap-hypothesis-method-and-evidence-ladder|observation-policy-form-obscures-care-action-and-measurement-process
    category: terminology-consistency
    dossier_locator: "Gap、Core hypothesis、Observational target、Contribution evidence ladder（行 62、89、226、426）"
    current_problem: "同一解释边界交替写成“观察政策”和“实际照护与测量政策”。“观察政策”容易只指检测或随访安排，而方法同时纳入治疗行动和测量过程；“政策”也可能被误读为正式制度，而非数据生成中的实际行为与过程。"
    target_state: "用直接且一致的表达指明结果条件于实际照护行为与测量过程，例如“在实际照护行为和测量过程下的预测或生成表征”。"
    required_change_or_replacement: "将行 62 和 426 的“观察政策下”以及行 89、226 的“实际照护与测量政策下”统一为“在实际照护行为和测量过程下”；如需指向联合分布，可写“由实际照护行为和测量过程共同形成的数据条件下”。"
    content_to_preserve: "治疗行动 A 与测量过程 M 的区分、实际临床数据生成环境、预测或生成分布的非因果解释边界，以及低行动支持只允许照护环境特异关系的限制。"
    acceptance_test: "四个定位位置采用同一直接表达；读者可从本句识别治疗行动和测量过程两个角色；不得把二者合并为仅指检测的“观察”，也不得增强因果主张。"
    term_or_phrase: "观察政策；实际照护与测量政策"
    recommended_form_or_plain_description: "在实际照护行为和测量过程下"
    evidence_basis: "dossier 的变量角色表已将治疗行动 A 与测量过程 M 分开，并在联合分布中同时建模；直接点名两个过程最符合其已声明科学角色。"
    first_use_definition: "本研究的预测和生成表征以实际发生的治疗行动与测量过程为条件，不将这些观察性关系解释为治疗因果作用。"
    competing_forms_and_locators:
      - "观察政策下：行 62、426"
      - "实际照护与测量政策下：行 89、226"
  - finding_id: LANG-R122-005
    severity: minor
    finding_kind: terminology
    finding_level: meso
    finding_scope: concept_cluster
    scientific_role: reproducible-analysis-specification-contribution
    normalized_locator: positioning-contribution-and-claim-support
    failure_mode: governance-label-does-not-name-concrete-scientific-practice
    fingerprint: meso|reproducible-analysis-specification-contribution|positioning-contribution-and-claim-support|governance-label-does-not-name-concrete-scientific-practice
    category: terminology-and-reader-accessibility
    dossier_locator: "Positioning and contribution frame、Contribution and evidence ladder、Title and positioning claim-support table（行 40、421、450）"
    current_problem: "“可证伪的分析治理”“方法治理价值”“可审计证据治理”以治理标签概括实际贡献，却没有在这些读者入口直接说明治理指预设判定标准、限制结果驱动修改、记录阴性结果和限定解释范围。该词并非错误，但对临床、统计和系统科学联合读者的科学产出指向不够具体。"
    target_state: "在贡献表述中直接列出可复核的分析规范及其作用，不再用“治理”作为科学贡献的名称。"
    required_change_or_replacement: "行 40 将“可证伪的分析治理”改为“预设判定标准、保留阴性结果并限制解释范围的可复核分析规范”；行 421 将“方法治理价值”改为“可复核的分析规范价值”；行 450 将“可审计证据治理”改为“预先规定且可复核的证据生成与解释规范”。"
    content_to_preserve: "预设标准、数据隔离、结果驱动修改限制、负向结果发布、解释边界、条件性整合与验证定位，以及不把贡献提高为新算法。"
    acceptance_test: "三处贡献表述不再以“治理”作未定义标签；每处均可直接识别至少一个具体分析规范或证据实践；贡献强度和证据范围不提高。"
    term_or_phrase: "可证伪的分析治理；方法治理价值；可审计证据治理"
    recommended_form_or_plain_description: "预设判定标准、保留阴性结果并限制解释范围的可复核分析规范"
    evidence_basis: "dossier 的时间节点、模拟标准、数据隔离、负向结果和解释矩阵已经列明这些实践，可直接描述现有内容而无须保留抽象治理标签。"
    first_use_definition: "可复核的分析规范包括预先规定判定标准、限制依据外部结果修改分析、记录阴性结果并按证据强度限定解释。"
    competing_forms_and_locators:
      - "可证伪的分析治理：行 40"
      - "方法治理价值：行 421"
      - "可审计证据治理：行 450"
  - finding_id: LANG-R122-006
    severity: minor
    finding_kind: language
    finding_level: micro
    finding_scope: occurrence
    scientific_role: noncausal-interpretation-boundary
    normalized_locator: one-sentence-complete-idea-summary-line-38
    failure_mode: unnatural-evidence-interpretation-collocation
    fingerprint: micro|noncausal-interpretation-boundary|one-sentence-complete-idea-summary-line-38|unnatural-evidence-interpretation-collocation
    category: chinese-academic-clarity
    dossier_locator: "Title, summary, audience, and positioning → One-sentence complete-Idea summary，行 38，末分句“所有预测与观察性表征只按非因果证据解释”"
    current_problem: "“按非因果证据解释”把证据类别与解释动作搭配在一起，读者虽能恢复边界，但需判断作者是说证据来源非因果，还是要求结论仅作非因果解释。"
    target_state: "在一句话摘要中直接说明预测和观察性表征的解释范围。"
    required_change_or_replacement: "将末分句改为“所有预测结果与观察性表征均仅作非因果解释”。"
    content_to_preserve: "该分句覆盖预测结果和观察性表征两类对象；不得删除非因果边界，也不得扩展为因果、机制、控制或数字孪生主张。"
    acceptance_test: "一句话摘要仍为一个句子；末分句明确以预测结果和观察性表征为对象并写明“仅作非因果解释”；句中不再出现“按非因果证据解释”。"
  - finding_id: LANG-R122-007
    severity: minor
    finding_kind: language
    finding_level: micro
    finding_scope: occurrence
    scientific_role: observation-mapping-fidelity-criteria
    normalized_locator: research-design-observation-mapping-line-292
    failure_mode: overloaded-criteria-sentence-and-missing-mathematical-attachment
    fingerprint: micro|observation-mapping-fidelity-criteria|research-design-observation-mapping-line-292|overloaded-criteria-sentence-and-missing-mathematical-attachment
    category: grammar-syntax-and-local-readability
    dossier_locator: "Research design and methods → 试验观察映射和独立分析，行 292，自“须同时满足”至“随机组间差异不能改变该判定”"
    current_problem: "一个段落连续承载外部忠实度五项阈值、治疗标签遮蔽后的两项覆盖条件和失败后果；其中“第一奇异轴所解释的 L_C Frobenius 能量比例”缺少清楚的所属与分母关系。读者可以借助 SVD 上下文恢复含义，但需要回读。"
    target_state: "将外部忠实度条件、试验资料覆盖条件和失败后果分成并列句或编号项；第一项直接写明第一奇异轴对应的奇异值平方在 L_C Frobenius 范数平方中的占比。"
    required_change_or_replacement: "保留开头的判定时点后，把“须同时满足”后的五项外部忠实度条件列为平行编号项；将第一项写为“第一奇异轴对应的奇异值平方占 L_C 的 Frobenius 范数平方的比例至少为 50%”。另起句列出治疗标签遮蔽后的 80% 与 60% 条件，再以独立句保留全部失败触发条件和“随机组间差异不能改变判定”。"
    content_to_preserve: "第 7 或第 8 日窗口、不按试验结果调参、50%、0.70、0.50、截距与斜率及覆盖率、每个锚点变量的校准条件、80% 与 60% 覆盖条件、单位与时间不变性、不得按试验重估权重及失败后果。"
    acceptance_test: "该段可逐项对应原有五项外部忠实度、两项试验覆盖和失败后果，所有数值及方向不变；不再出现“L_C Frobenius 能量比例”；第一项同时明示分子和分母；读者无需跨句寻找随机组间差异不改变判定的对象。"
unresolved_issues:
  - LANG-R122-001
  - LANG-R122-002
  - LANG-R122-003
  - LANG-R122-004
  - LANG-R122-005
  - LANG-R122-006
  - LANG-R122-007
---

# Language Assessment Report

**Assessment ID**: language-assessment-I01-001-r122  
**Target Language**: Chinese  
**Discipline**: 重症医学、临床流行病学、纵向统计、系统辨识、医学人工智能与转化研究  
**Target Journal**: 未指定  
**Scope**: complete_idea_dossier  
**Date**: 2026-07-20

---

## Overall Language Readiness

**Level**: minor_language_revision

**Recommendation**: polish

正文已经能够稳定传达研究对象、主要任务、证据边界和计划状态。当前问题均可在不选择新估计目标、不改变模型角色和不提高主张强度的情况下作局部或全篇一致性修订。

---

## Dimension Scores

| Dimension | Score (1–10) | Severity |
|-----------|-------------|----------|
| Grammar & Syntax | 8 | pass |
| Academic Register & Tone | 8 | pass |
| Terminology Consistency | 7 | pass |
| Tense & Voice Conventions | 10 | pass |
| Conciseness & Redundancy | 7 | pass |
| Readability & Flow | 7 | pass |

---

## Hard Gate Status

**Overall**: pass

| Gate | Status | Detail |
|------|--------|--------|
| Grammar error density | pass | 仅 1 处明确局部构式问题，低于每 500 词 1 处；没有系统性语法错误 |
| Academic register | pass | 少数项目流程或物理隐喻分布在局部位置，不构成两个以上章节的系统性口语语域 |
| Terminology coherence | pass | 没有三个核心概念各自出现互不相容的命名；五个 finding 是自然度、读者基线或角色直陈问题，而非核心概念混乱 |
| Tense systematic violation | pass | 全文持续采用计划、条件与尚未生成结果的时态；没有把计划写成已完成结果 |

---

## Strengths

- 标题、摘要、研究问题和核心假设均把研究对象限定为覆盖发病前、首次发病、发病后演化和结局的候选动态系统表征，没有退化为已发病预后模型。
- 计划状态、已有资源状态和尚未生成的结果在摘要、资源表和方法中保持一致，时态没有制造“已经验证”的错误印象。
- “共同生理锚点变量”“锚点观测值”“锚点预测值”“潜在状态投影”和“一维可观测代理”均在首次关键使用处给出功能性定义，后文数学符号与角色基本一致。
- 预测、观察性表征与因果解释的边界在正文中表达明确；本报告只建议改善局部搭配，不改变该科学边界。

---

## Specific Issues

### Chinese Academic Clarity

- **LANG-R122-006（minor）**：一句话摘要末分句的“按非因果证据解释”搭配不自然。具体替换、保留项和单句验收条件见 frontmatter。
- **LANG-R122-007（minor）**：观测映射忠实度段落把多组阈值和失败后果压入一个长句，并有一处数学所属关系不清。分项方式与数值保真要求见 frontmatter。

### Grammar & Syntax

- **LANG-R122-007（minor）**：行 292 的“\(L_C\) Frobenius 能量比例”缺少清楚的所属和分母表达；建议使用 frontmatter 中的数学等价直述。

### Academic Register & Tone

- **LANG-R122-003（minor）**：“晋级/不晋级”应改为模型是否进入后续分析与验证的直接科学后果。
- **LANG-R122-005（minor）**：“治理”应展开为预设标准、结果隔离、阴性结果记录和解释限制等实际规范。

### Terminology Consistency

| id | term_or_phrase | locator | reader_effect | action_in_frontmatter |
|---|---|---|---|---|
| LANG-R122-001 | 未触碰 | 摘要、方法、证据链、解释与风险多处 | 混合数据隔离、检验操作与结果来源 | yes |
| LANG-R122-002 | 合取 | 成功定义、阶段 III 资格与解释多处 | 要求临床读者先理解形式逻辑标签 | yes |
| LANG-R122-003 | 晋级/不晋级 | 模拟判定、输出与失败条件多处 | 以流程隐喻代替具体科学后果 | yes |
| LANG-R122-004 | 观察政策/实际照护与测量政策 | Gap、假设、方法和贡献 | “观察”可能遮蔽治疗行动角色 | yes |
| LANG-R122-005 | 分析/方法/证据治理 | 定位与贡献三处 | 抽象标签未直接说明科学实践 | yes |

### Tense & Voice Conventions

未发现可执行问题。作为 Idea，全文使用计划性、条件性和将来实施表述，符合研究尚未执行的状态。

### Conciseness & Redundancy

未单列跨章节重复问题。局部术语替换会减少项目化压缩词，但完整 limitation 的放置、跨章节保留与删除属于 narrative assessment，不在本报告中决定。

### Readability & Flow

- **LANG-R122-007（minor）**：行 292 需要按判定角色拆分局部并列信息；这是句内可读性修订，不改变章节结构或论证顺序。

---

## Language Revision Priorities

1. **术语与读者基线**：5 个概念簇——分别直陈独立外部测试、全部条件同时满足、候选模型后续资格、实际照护与测量过程和分析规范。
2. **局部中文清晰度**：2 处——修正摘要末分句搭配，并拆分观测映射阈值句且明确 Frobenius 范数平方占比。

---

## Re-Assessment Status (if applicable)

不适用。本次为仅绑定当前 v054 dossier 的 fresh complete-Idea assessment，未接收先前问题清单或任何旧版本。

---

## Assessment Notes

本评估只判断中文学术语言、读者可理解性与触发式术语问题，不判断论证质量、创新性、影响力、可行性或方法正确性。固定 research-idea.v3 标题与字段未被当作语言错误。术语复核仅针对普通阅读触发的概念簇；数学符号、数据库版本、文献标识符、已定义缩写和自然的描述性表达未形成术语清单。项目输入仅为当前 v054 dossier；reader handoff 来自 dossier 内嵌的 Primary audience。
