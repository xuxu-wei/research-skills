---
review_id: language-assessment-r001
reviewer_skill: academic-language-assessor
reviewer_instance_id: fresh-academic-language-assessor-r001
workflow_id: sepsis-complex-system-idea-generation-v001
round_id: r001
input_artifact_ids:
  - idea-dossier-I01-001-v003
input_versions:
  - v003
scope: complete_idea_dossier
dossier_ref:
  artifact_id: idea-dossier-I01-001-v003
  version: v003
  path: tests/脓毒症复杂系统模型/03_ideas/nodes/I01-001/dossiers/idea-dossier-v003.md
reader_handoff:
  artifact_id: embedded-reader-handoff-cross-disciplinary-pi
  version: embedded
  path: null
files_read:
  - AGENTS.md
  - research-skills-openai/AGENTS.md
  - research-skills-openai/skills/academic-language-assessor/SKILL.md
  - research-skills-openai/skills/academic-language-assessor/references/language-assessment-rubric.md
  - research-skills-openai/skills/academic-language-assessor/references/language-hard-gates.md
  - research-skills-openai/skills/academic-language-assessor/references/terminology-review.md
  - research-skills-openai/skills/academic-language-assessor/references/chinese-academic-language-conventions.md
  - research-skills-openai/skills/academic-language-assessor/references/discipline-language-conventions.md
  - research-skills-openai/skills/academic-language-assessor/references/common-l1-interference-patterns.md
  - research-skills-openai/skills/academic-language-assessor/templates/language-assessment-report.md
  - research-skills-openai/skills/academic-language-assessor/scripts/scan_idea_language_candidates.py
  - research-skills-openai/skills/academic-language-assessor/scripts/diff_reader_facing_short_forms.py
  - research-skills-openai/skills/academic-language-assessor/scripts/validate_language_assessment.py
  - research-skills-openai/skills/academic-language-assessor/scripts/test_scan_idea_language_candidates.py
  - research-skills-openai/skills/academic-language-assessor/scripts/test_diff_reader_facing_short_forms.py
  - research-skills-openai/skills/academic-language-assessor/scripts/test_validate_language_assessment.py
  - tests/脓毒症复杂系统模型/03_ideas/nodes/I01-001/dossiers/idea-dossier-v003.md
isolation_mode: fresh_subagent
prior_scores_visible: false
source_edits_performed: false
decision: major_language_revision
coverage_receipt:
  reader_entry:
    status: completed
    reviewed_count: 13
    basis: 已逐项检查 scanner 界定的标题、摘要、受众、定位、核心定义及结构式摘要入口单元。
  core_scientific_role:
    status: completed
    reviewed_count: 11
    basis: 已按跨学科 PI 读者核对实际出现的研究对象、四项任务、模型与比较、外部迁移、失败输出、条件性后续和贡献等角色组。
  terminology_concordance:
    status: completed
    reviewed_count: 4
    basis: 已对四个实际触发的概念簇完成全 dossier 形式与语义核对，未建立完整术语清单。
  local_language:
    status: completed
    reviewed_count: 198
    basis: 已检查全部非空正文、列表项和表格内容单元；固定标题与字段标签仅作定位，不参与评分。
findings:
  - finding_id: LANG-001
    severity: major
    finding_kind: terminology
    finding_level: meso
    finding_scope: concept_cluster
    scientific_role: task-three-prediction-target
    normalized_locator: task-three-entry-and-hypothesis
    failure_mode: latent-state-versus-observed-value
    fingerprint: meso|task-three-prediction-target|task-three-entry-and-hypothesis|latent-state-versus-observed-value
    category: 核心任务对象命名
    dossier_locator: lines 62, 83, 91, 175, and 303
    current_problem: >-
      “部分观测下其他临床状态”“有限观测下状态估计”等入口性表述会使跨学科 PI 把任务三理解为潜在状态估计；但第 175 行把目标明确限定为被遮蔽但真实测得的器官功能和器官支持值，第 303 行也将其解释为可观测值预测。
    target_state: >-
      所有任务三入口、假设标题和解释均直接表明研究预测的是部分观测条件下未提供给模型的临床测量值，而不是估计潜在状态。
    required_change_or_replacement: >-
      将任务三的统称统一为“部分观测下的临床测量值预测”；H3 标题可写为“部分观测下预测未观测的临床测量值”。同步替换第 62、83、91 和 175 行的状态估计表述，并保留第 175 行已固定的结果域、遮蔽设计、评分和“不把潜在状态当金标准”的边界。
    content_to_preserve: >-
      保留六个器官功能域、三类器官支持、12 小时连续块遮蔽、真实测量值目标、负对数评分、权重规则、比较模型和 H3 判定标准。
    acceptance_test: >-
      全 dossier 检索任务三的所有读者可见表述；每处均明确指向临床测量值预测，且没有任何一处可被合理读成潜在状态估计或状态识别。
    term_or_phrase: 部分观测下其他临床状态；有限观测下状态估计
    recommended_form_or_plain_description: 部分观测下的临床测量值预测
    evidence_basis: >-
      第 175 行明确规定目标为被遮蔽但真实存在的值并排除潜在状态金标准；第 303 行明确写为“有限观测下的可观测值预测”。这两处足以恢复既定科学角色，无需选择新的 estimand。
    first_use_definition: >-
      任务三在部分观测条件下预测被遮蔽但真实测得的六个器官功能域和三类器官支持值，不以潜在状态为金标准。
    competing_forms_and_locators:
      - “部分观测下其他临床状态” — lines 62 and 91
      - “有限观测下状态估计” — line 83
      - “部分观测下估计其他临床状态” — line 175
      - “有限观测下的可观测值预测” — line 303
  - finding_id: LANG-002
    severity: minor
    finding_kind: terminology
    finding_level: meso
    finding_scope: concept_cluster
    scientific_role: model-recovery-diagnostic
    normalized_locator: approach-and-recovery-mentions
    failure_mode: clinical-versus-model-recovery
    fingerprint: meso|model-recovery-diagnostic|approach-and-recovery-mentions|clinical-versus-model-recovery
    category: 方法诊断命名
    dossier_locator: lines 63, 87, 98, 109, 139, 151, 163, 165, 210, 221-222, 227, 261, 268, 283, 291, 311, and 380
    current_problem: >-
      “恢复诊断”在同一 dossier 中与患者“持续恢复”并存，且有时与“参数恢复”“状态恢复”交替出现。跨学科 PI 在第 63 行首次遇到该词时，不能立即判断它是临床恢复诊断，还是通过模拟检验参数与潜在状态可恢复性的模型诊断。
    target_state: >-
      首次出现即直接说明这是对模型参数和潜在状态能否从模拟数据中被可靠恢复的诊断，后续统称与具体指标保持一致。
    required_change_or_replacement: >-
      第 63 行改为“开展模拟并检验参数和潜在状态能否被可靠恢复”；需要统称时使用“参数与潜在状态恢复诊断”，并保留第 163 和 210 行已经列出的参数偏倚、区间覆盖、标签交换、弱转移和状态恢复等具体检查。
    content_to_preserve: >-
      保留模拟、参数偏倚、区间覆盖、潜在状态恢复、标签交换、弱转移恢复、预测稳定性、复杂度缩减和停止规则。
    acceptance_test: >-
      全 dossier 检索“恢复诊断”“参数恢复”和“状态恢复”；每处均能在本句识别其模型诊断对象，且不会与患者持续恢复事件混淆，也不删除参数或潜在状态任一恢复检查。
    term_or_phrase: 恢复诊断
    recommended_form_or_plain_description: 参数与潜在状态恢复诊断
    evidence_basis: >-
      第 163 行列出参数偏倚、标签交换和弱转移恢复，第 210 行同时列出参数偏倚与状态恢复，说明该统称覆盖参数和潜在状态两类恢复检查；问题在于首用和后续简称没有说出对象。
    first_use_definition: >-
      通过模拟检验模型参数和潜在状态能否从已知生成机制的数据中被可靠恢复，以下简称参数与潜在状态恢复诊断。
    competing_forms_and_locators:
      - “参数恢复” — lines 87, 98, 139, 163, and 221
      - “恢复诊断”或“模拟与恢复诊断” — lines 63, 109, 151, 165, 210, 222, 227, 261, 268, 283, 291, 311, and 380
      - “状态恢复” — line 210
  - finding_id: LANG-003
    severity: minor
    finding_kind: terminology
    finding_level: meso
    finding_scope: concept_cluster
    scientific_role: missingness-weighting
    normalized_locator: weighting-specification-and-limitations
    failure_mode: inconsistent-observation-probability-terms
    fingerprint: meso|missingness-weighting|weighting-specification-and-limitations|inconsistent-observation-probability-terms
    category: 权重术语一致性
    dossier_locator: lines 169, 178, 211, and 368
    current_problem: >-
      同一权重机制被写成“逆观察概率权重”“目标可观察概率”“观测权重”“观察/删失权重”和“观测概率与删失权重”，混用了观察/观测、概率/权重以及主动可观察/实际被观测三个层次。
    target_state: >-
      对概率、逆概率权重和与删失权重并列的表述分别采用单一、直接且语法平行的名称。
    required_change_or_replacement: >-
      权重统一写为“逆观测概率权重”，其概率模型写为“目标值被观测的概率”；与删失并列时写为“逆观测概率权重与逆删失概率权重”。按此规则改写第 169、178、211 和 368 行，不改变协变量、截断、归一化或敏感性分析。
    content_to_preserve: >-
      保留患者内归一化、外部资料截止时点、目标可评分条件、权重模型冻结、截断方案和敏感性分析边界。
    acceptance_test: >-
      全 dossier 核对该概念簇：概率一律指目标值被观测的概率，权重一律明确为其逆概率权重，并与逆删失概率权重保持同一语法层级。
    term_or_phrase: 逆观察概率权重；目标可观察概率；观测权重
    recommended_form_or_plain_description: 逆观测概率权重；目标值被观测的概率
    evidence_basis: >-
      第 169 行说明该权重只在目标实际可评分时使用，第 178 行说明它只用于实际测量才可评分的组成，因此既定角色是对目标值被观测概率取逆后加权，而不是泛指观测过程。
    first_use_definition: >-
      对仅在实际测量时可评分的目标，使用目标值被观测概率的逆概率权重进行校正。
    competing_forms_and_locators:
      - “逆观察概率权重”与“目标可观察概率” — line 169
      - “观测权重” — line 178
      - “观察/删失权重” — line 211
      - “观测概率与删失权重” — line 368
  - finding_id: LANG-004
    severity: minor
    finding_kind: terminology
    finding_level: meso
    finding_scope: concept_cluster
    scientific_role: dynamic-prediction-time-origin
    normalized_locator: confirmatory-family-and-task-definitions
    failure_mode: undefined-english-method-term
    fingerprint: meso|dynamic-prediction-time-origin|confirmatory-family-and-task-definitions|undefined-english-method-term
    category: 跨学科首用定义
    dossier_locator: lines 93, 153, 159, 169, 171, 173-176, 190, 206, 211, 213, and 234
    current_problem: >-
      英文术语“landmark”从第 93 行起反复承担风险集和预测时域起点的核心角色，但首次出现没有中文说明；临床、系统科学与人工智能 PI 不一定共享动态预测方法中的该术语基线。
    target_state: >-
      首次出现即用普通中文说明其为每次预测的起始时点，随后使用稳定的中文形式或中文加英文括注。
    required_change_or_replacement: >-
      第 93 行首次出现时写为“预定预测起始时点（landmark）”；后文统一写为“预测起始时点”，仅在表头或确需与方法文献对应时保留括号内英文。
    content_to_preserve: >-
      保留每项任务的起始时点集合、风险集、预测时域、患者内汇总和重复测量结构。
    acceptance_test: >-
      跨学科 PI 无需外部术语表即可在第一次出现处说明 landmark 的功能；全 dossier 不再出现无中文锚定的裸用“landmark”。
    term_or_phrase: landmark
    recommended_form_or_plain_description: 预测起始时点（landmark）
    evidence_basis: >-
      第 153 和 173-176 行均把它用作预测窗口与风险集的起点；直接描述该时间功能即可恢复含义，无需另立项目标签。
    first_use_definition: >-
      预测起始时点（landmark）是每次界定风险集、截断可用信息并开始计算后续预测时域的时点。
    competing_forms_and_locators: []
  - finding_id: LANG-005
    severity: minor
    finding_kind: language
    finding_level: micro
    finding_scope: occurrence
    scientific_role: task-result-relation
    normalized_locator: structured-abstract-expected-result
    failure_mode: unintended-statistical-independence
    fingerprint: micro|task-result-relation|structured-abstract-expected-result|unintended-statistical-independence
    category: 科学措辞精度
    dossier_locator: line 64
    current_problem: >-
      “四个相互独立的任务级比较结果”容易被理解为四项结果在统计上独立；同一模型、可能重叠的患者以及统一 Holm 家族并不支持这一读法。上下文实际强调的是分别报告且不可互相补救。
    target_state: >-
      只表达四项结果分别报告、分别判定且互不补救，不引入统计独立性主张。
    required_change_or_replacement: >-
      将“四个相互独立的任务级比较结果”改为“四项分别报告且互不替代的任务级比较结果”。
    content_to_preserve: >-
      保留四项任务分别比较、统一控制家族错误率以及任务间不可补救的设计边界。
    acceptance_test: >-
      修订句不再出现“独立”来描述任务结果，同时仍明确四项结果分别报告并分别形成支持或不支持结论。
  - finding_id: LANG-006
    severity: minor
    finding_kind: language
    finding_level: meso
    finding_scope: concept_cluster
    scientific_role: database-qualification-status
    normalized_locator: data-constitution-and-qualification-table
    failure_mode: nonparallel-and-incomplete-predication
    fingerprint: meso|database-qualification-status|data-constitution-and-qualification-table|nonparallel-and-incomplete-predication
    category: 句法与搭配
    dossier_locator: lines 119 and 124
    current_problem: >-
      第 119 行把“取得项目访问、字段适配或足够信息量”并列在同一动词后，动作与状态不平行；第 124 行以“患者和事件信息通过”收尾，缺少“通过”所支配的审计或标准，形成不完整谓语。
    target_state: >-
      数据资格陈述为每项条件配置明确、平行的动作或状态，并完整说出通过何种资格检查。
    required_change_or_replacement: >-
      第 119 行改为“当前尚未确认任何组合已取得项目级访问许可、完成字段适配并具备足够信息量。”第 124 行改为“患者级标识与事件记录通过资格审计。”
    content_to_preserve: >-
      保留项目访问、字段适配、信息量、患者级识别和事件记录均需在建模前实证核验的要求。
    acceptance_test: >-
      两处句子均具有明确主语和完整谓语，三个资格条件保持语法平行，且没有新增或删除任何数据资格条件。
unresolved_issues:
  - LANG-001
  - LANG-002
  - LANG-003
  - LANG-004
  - LANG-005
  - LANG-006
---

# Language Assessment Report

**Assessment ID**: language-assessment-r001  
**Target Language**: Chinese  
**Discipline**: 脓毒症与重症医学、纵向统计、系统辨识和临床人工智能交叉研究  
**Target Journal**: 未指定  
**Scope**: complete_idea_dossier  
**Date**: 2026-07-20

---

## Overall Language Readiness

**Level**: major_language_revision

**Recommendation**: revise_language

任务三的读者入口把实际的“临床测量值预测”写成“状态估计”，跨学科 PI 可能据此误判一个核心确认性任务的对象。该问题可以根据 dossier 内已明确的目标直接修复，不需要在不同 estimand、指标或模型角色之间作新的科学选择。其余问题均为次要措辞或术语问题。

---

## Dimension Scores

| Dimension | Score (1–10) | Severity |
|-----------|-------------|----------|
| Grammar & Syntax | 8 | pass |
| Academic Register & Tone | 9 | pass |
| Terminology Consistency | 6 | borderline |
| Tense & Voice Conventions | 9 | pass |
| Conciseness & Redundancy | 7 | pass |
| Readability & Flow | 7 | pass |

---

## Hard Gate Status

**Overall**: pass

| Gate | Status | Detail |
|------|--------|--------|
| Grammar error density | pass | 发现 2 处明确的句法或搭配问题；相对于约 13,698 个汉字的全文规模，远低于每 500 词 3 处的门槛。中文不以空格分词，因此按全文密度作保守判断。 |
| Academic register | pass | 正文保持正式、审慎的学术语体；未见两个或以上章节的系统性口语化。 |
| Terminology coherence | pass | 1 个核心任务对象存在实质性竞争表述；其余为可从近文恢复的次级方法术语或首用定义问题，未达到 3 个核心概念同时失配的门槛。 |
| Tense systematic violation | pass | 全文一致采用前瞻性计划语气，没有把拟开展的研究系统性写成已完成结果。 |

---

## Strengths

- 标题后的定义段及时限定“动态状态模型”“全病程”“受约束”和“外部验证”，显著降低跨学科读者的概念进入成本。
- 全文一致区分预测性表示、真实生物状态、因果作用和临床部署，语气克制，没有宣传性结论。
- “状态转移”主要用于患者病程内变化，“状态迁移”主要用于跨数据库可重复性，整体区分清楚。
- 任务、失败标准和允许解释采用平行表格与直接条件句呈现，未来时态与条件语气一致。

---

## Specific Issues

### Chinese Academic Clarity (if applicable)

- **LANG-001（major）**：任务三入口性命名把可观测临床测量值预测写成状态估计，可能改变跨学科 PI 对核心任务对象的理解。
- **LANG-005（minor）**：“相互独立”在统计语境中产生超出上下文意图的含义；上下文支持“分别报告且互不替代”。
- **LANG-006（minor）**：两处数据库资格陈述分别存在不平行搭配和不完整谓语。

### Grammar & Syntax

- **LANG-006（minor）**：问题限于第 119 和 124 行，未形成系统性语法错误。

### Academic Register & Tone

未发现可执行问题。全文语体正式，限制条件和未验证状态表达审慎。

### Terminology Consistency

| id | term_or_phrase | locator | reader_effect | action_in_frontmatter |
|---|---|---|---|---|
| LANG-001 | 部分观测下其他临床状态；有限观测下状态估计 | lines 62, 83, 91, 175, 303 | 可能把临床测量值预测误读为潜在状态估计 | yes |
| LANG-002 | 恢复诊断 | lines 63, 87, 98, 109, 139, 151, 163, 165, 210, 221-222, 227, 261, 268, 283, 291, 311, 380 | 可能与患者持续恢复混淆，且诊断对象首用不明 | yes |
| LANG-003 | 逆观察概率权重；目标可观察概率；观测权重 | lines 169, 178, 211, 368 | 概率、权重和被观测状态的语义层次不稳定 | yes |
| LANG-004 | landmark | lines 93, 153, 159, 169, 171, 173-176, 190, 206, 211, 213, 234 | 非动态预测专业的 PI 首次阅读时缺少时间功能锚点 | yes |

### Tense & Voice Conventions

未发现可执行问题。研究计划、预期结果、条件性后续与已知证据的时间状态保持一致。

### Conciseness & Redundancy

未发现需要单列的可执行问题。若干句子信息密度较高，但限定语大多承载设计边界；是否跨章节删减完整限制条件属于叙事安排，不在本报告中决定。

### Readability & Flow

主要阅读负担来自 **LANG-001 至 LANG-004** 所列任务与方法术语，而不是段落顺序。完成这些局部修订后，跨学科读者可在不改变章节结构的情况下恢复主要科学角色。

---

## Language Revision Priorities

1. **任务三对象命名**：1 个主要问题——先统一为“部分观测下的临床测量值预测”，并对全 dossier 作一致性检查。
2. **方法术语首用与一致性**：3 个次要问题——明确模型恢复诊断对象、统一逆观测概率权重名称，并在首次使用时解释预测起始时点。
3. **局部句法精度**：2 个次要问题——去除统计独立性的非预期含义，并补全数据库资格陈述。

---

## Re-Assessment Status (if applicable)

不适用。本次为针对 v003 的全新完整评估，没有读取旧版本、修订记录、既往评分或其他评审报告。

---

## Assessment Notes

- 读者基线按任务指定为跨学科 PI：重症医学、系统科学与系统辨识、临床人工智能及临床研究方法学负责人均应能在首次出现处识别核心科学角色。
- 仅评估指定 v003 dossier 的读者可见语言；固定的 research-idea.v3 标题、字段标签和机器元数据未参与评分。
- scanner 已实际运行；候选仅用于定位，未把候选本身当作问题，也未保存候选清单。
- 未评价科学有效性、创新性、可行性、期刊适配度或论证结构，未替研究者选择 estimand、指标、模型角色或主张强度。
