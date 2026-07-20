---
review_id: language-assessment-r095
reviewer_skill: academic-language-assessor
reviewer_instance_id: focused_language_r095
workflow_id: RID-SEPSIS-CSM-20260717-001
round_id: r095
input_artifact_ids: [idea-dossier-I01-001-v003]
input_versions: [v003]
scope: complete_idea_dossier
dossier_ref: {artifact_id: idea-dossier-I01-001-v003, version: v003, path: "tests/idea-test-0.9.0-preview.1/0.9.0-preview.1/03_ideas/nodes/I01-001/dossiers/idea-dossier-v003.md"}
reader_handoff: {artifact_id: embedded-reader-handoff, version: embedded, path: null}
files_read:
  - "research-skills-openai/skills/academic-language-assessor/SKILL.md"
  - "research-skills-openai/skills/academic-language-assessor/references/language-assessment-rubric.md"
  - "research-skills-openai/skills/academic-language-assessor/references/language-hard-gates.md"
  - "research-skills-openai/skills/academic-language-assessor/references/chinese-academic-language-conventions.md"
  - "research-skills-openai/skills/academic-language-assessor/references/discipline-language-conventions.md"
  - "research-skills-openai/skills/academic-language-assessor/references/terminology-review.md"
  - "research-skills-openai/skills/academic-language-assessor/templates/language-assessment-report.md"
  - "tests/idea-test-0.9.0-preview.1/0.9.0-preview.1/03_ideas/nodes/I01-001/dossiers/idea-dossier-v003.md"
isolation_mode: fresh_subagent
prior_scores_visible: false
source_edits_performed: false
decision: major_language_revision
findings:
  - finding_id: L-001
    severity: major
    finding_kind: terminology
    category: central study-object naming
    dossier_locator: "Title and Title field (lines 27, 31); structured abstract Objective (line 39); primary question (line 60); Objective 2 (line 65)"
    current_problem: "The same central object is alternately called ‘候选动态系统表征’, ‘候选全病程表示’, ‘候选状态表示’, ‘候选架构’, and ‘阶段 II 表征’. For the stated cross-disciplinary reader, the shifts leave it unclear whether the object is a state representation, a dynamic-system model, or the whole protocol."
    target_state: "One descriptive name identifies the patient-time representation and its observational scope; shorter forms retain that referent."
    required_change_or_replacement: "Use ‘脓毒症全病程候选动态状态表示’ as the title and first-use form, then ‘候选状态表示’ only after that definition. Do not use ‘候选架构’ or ‘阶段 II 表征’ as alternate names for the same object."
    content_to_preserve: "Candidate status; the sepsis-centred pre-onset, onset, post-onset, and outcome scope; and the separation of state, treatment action, and observation process."
    acceptance_test: "A reader from each named discipline can point to one named study object at its first use; a whole-dossier search finds no alternate label unless it denotes a genuinely different component. The replacement remains a direct description rather than an undefined project label."
    term_or_phrase: "候选动态系统表征 and competing central-object labels"
    recommended_form_or_plain_description: "脓毒症全病程候选动态状态表示"
    evidence_basis: "Focused whole-dossier concordance found five competing forms at the listed locators. No supplied source verifies the project-specific composite; direct descriptive wording is therefore preferable under the terminology review."
    first_use_definition: "‘脓毒症全病程候选动态状态表示’指在已观测的照护和测量政策下，对患者时间状态及其转移进行的候选表示；它不等同于已识别的真实系统、因果网络或控制模型。"
    competing_forms_and_locators:
      - "候选动态系统表征 — lines 27, 31, 32, 60"
      - "候选全病程表示 — line 39"
      - "候选状态表示 — line 65"
      - "候选架构 — line 50"
      - "阶段 II 表征 — lines 67, 246, 254"
  - finding_id: L-002
    severity: major
    finding_kind: terminology
    category: observability versus data support
    dossier_locator: "One-sentence summary and Objective (lines 32, 39); Objective 2 (line 65); WP1 (line 106); G1 audit heading (line 131)"
    current_problem: "‘可观测性审计’ and ‘G1 可观测性’ name an audit of data access, timing, units, coverage, and support, but readers trained in system identification can reasonably read ‘可观测性’ as the state-space property of recovering all states from outputs."
    target_state: "The data audit and any state-space observability claim have distinct names."
    required_change_or_replacement: "Replace reader-facing ‘可观测性审计/G1 可观测性’ with ‘观测数据可用性与支持审计（G1）’; reserve ‘系统可观测性’ for a separately specified state-space property only if it is actually tested."
    content_to_preserve: "The G1 thresholds for access, events, transitions, hospitals, anchor density, timestamps, units, interfaces, and coverage."
    acceptance_test: "At first G1 use, the text defines the audited data properties and never implies that all latent states are observable. A system-identification reader can distinguish G1 from a rank-based observability test without consulting later sections."
    term_or_phrase: "可观测性审计 / G1 可观测性"
    recommended_form_or_plain_description: "观测数据可用性与支持审计（G1）"
    evidence_basis: "MathWorks defines observability of a state-space model as knowing all states from outputs and determines it from the observability matrix/rank: https://uk.mathworks.com/help/control/ref/statespacemodel.obsv.html. The dossier's G1 table instead audits data availability and support; the replacement describes that function directly."
    first_use_definition: "‘观测数据可用性与支持审计（G1）’是对双库访问、事件与转移数量、时间戳、单位、锚点密度、医院覆盖和接口可用性的预设核查，不是对潜在状态能否由输出完全重建的判定。"
    competing_forms_and_locators:
      - "访问及可观测性审计 — line 32"
      - "双库可观测性审计 — lines 39, 65"
      - "G1 可观测性 — line 106"
      - "G1 audit — line 131"
  - finding_id: L-003
    severity: major
    finding_kind: terminology
    category: simulation recovery and error claims
    dossier_locator: "Summary and objectives (lines 32, 34, 39, 41-42, 66, 71); recovery table (lines 216-226); evidence chain (lines 290-297); falsification criteria (lines 345, 353)"
    current_problem: "‘绝对模拟恢复’, ‘绝对恢复’, and ‘假置信’ are central gate labels but do not state what is recovered, against what truth, or what error is being controlled. ‘假置信’ can be read as poor calibration, false discovery, or an unsupported structural claim."
    target_state: "Each gate names the simulated target, the prespecified threshold, and the error state in direct statistical language."
    required_change_or_replacement: "Use ‘预设生成情景下的状态、转移和结构恢复评估’ for the simulation gate. Replace ‘假置信门’ with ‘错误结构的高置信支持控制’ and state the relevant threshold beside it. Retain ‘绝对’ only when it explicitly means prespecified performance thresholds rather than relative model ranking."
    content_to_preserve: "Correct-, null-edge-, overfit-, and misspecified-generator scenarios; recovery metrics; thresholds; and automatic downgrading."
    acceptance_test: "Every first reader-facing occurrence states the target quantity, the simulated reference, and the predefined criterion; no occurrence of ‘假置信’ remains without ‘错误结构’ and the stated error condition. The reader can distinguish recovery, calibration, and false structural support."
    term_or_phrase: "绝对模拟恢复 / 绝对恢复 / 假置信"
    recommended_form_or_plain_description: "预设生成情景下的状态、转移和结构恢复评估；错误结构的高置信支持控制"
    evidence_basis: "The supplied Morris et al. simulation-guidance source (https://pmc.ncbi.nlm.nih.gov/articles/PMC6492164/) supports reporting simulation performance against known data-generating scenarios, but does not establish these compact labels as standard. Direct descriptions are used because no further source search was permitted."
    first_use_definition: "‘预设生成情景下的状态、转移和结构恢复评估’比较候选方法在已知生成真值下恢复预先指定目标的表现；‘错误结构的高置信支持控制’指错误结构被高置信地支持的重复比例不得超过预设上限。"
    competing_forms_and_locators:
      - "绝对模拟恢复门 — line 32"
      - "绝对恢复 — lines 34, 42, 66, 71"
      - "绝对 Monte Carlo 门 — line 40"
      - "绝对 recovery/FDR/coverage/假置信门 — line 293"
      - "假置信 — lines 39, 41, 52, 85, 225"
  - finding_id: L-004
    severity: major
    finding_kind: terminology
    category: abstention action
    dossier_locator: "Background (line 52); recovery table (line 225); observational target (line 212); evidence-chain outputs (lines 294, 310); planned outputs and falsification criteria (lines 345, 353, 381)"
    current_problem: "‘弃权’ is used as a failure action for unstable states or edges, but it does not say whether the model withholds a prediction, declines structural interpretation, or omits a result. The reader can mistakenly import the machine-learning reject-option meaning."
    target_state: "The text names the actor, affected claim, and consequence: no structural interpretation is made for the affected state or edge."
    required_change_or_replacement: "Replace standalone ‘弃权’ with ‘不作该状态或边的结构性解释（弃权）’; where prediction is also withheld, state that separately."
    content_to_preserve: "The predetermined conditions under which a result is not interpreted and the resulting deletion, merger, downgrade, or database/policy-specific label."
    acceptance_test: "Each occurrence identifies what is withheld and why. No reader-facing use leaves ‘弃权’ as an unexplained output label, and no replacement implies a clinical or participant-level action."
    term_or_phrase: "弃权"
    recommended_form_or_plain_description: "不作该状态或边的结构性解释（弃权）"
    evidence_basis: "Hendrickx et al. describe machine learning with rejection as abstaining from making a prediction when it is likely wrong: https://arxiv.org/abs/2107.11277. The dossier instead limits interpretation of structure, so the direct replacement prevents a false equivalence."
    first_use_definition: "‘不作该状态或边的结构性解释（弃权）’指达到预设失败条件后，不把该结果用于结构或机制结论；它不表示自动拒绝临床预测或对患者采取行动。"
    competing_forms_and_locators:
      - "强制弃权 — line 52"
      - "恢复/假置信/弃权记录 — line 41"
      - "失配/弃权 — line 225"
      - "删除、合并或标记 database/policy-specific — line 212"
  - finding_id: L-005
    severity: major
    finding_kind: terminology
    category: external-test isolation
    dossier_locator: "Summary and objectives (lines 32, 34, 39-42, 66, 71); success definition (line 98); validation section (lines 230-240); R1 (line 250); evidence chain (lines 308-312)"
    current_problem: "‘真正未触碰’, ‘未触碰’, ‘untouched’, and ‘zero-update’ appear as if interchangeable, while the dossier distinguishes a pre-isolated test set from the separate condition of no re-estimation. The mixed labels obscure which safeguard is being claimed."
    target_state: "Dataset isolation and the analysis action are named separately at first use."
    required_change_or_replacement: "At first use write ‘预先隔离、未用于模型选择的外部测试集；主要分析不作任何重新估计（zero-update）’. Thereafter retain the defined English shorthand only in technical tables if needed."
    content_to_preserve: "Hospital-first allocation, patient separation, frozen choices, the sequence of calibration and observation-layer updates, and the rule that later updates do not rescue the primary external test."
    acceptance_test: "The first use distinguishes the test set's prior isolation from the no-update analysis. All later ‘zero-update’ uses refer only to no re-estimation; all claims of ‘未触碰’ identify the protected test data or test result."
    term_or_phrase: "真正未触碰 / 未触碰 / untouched / zero-update"
    recommended_form_or_plain_description: "预先隔离、未用于模型选择的外部测试集；主要分析不作任何重新估计（zero-update）"
    evidence_basis: "TRIPOD+AI is the supplied reporting-guidance source for transparent distinction of development and validation claims: https://www.bmj.com/content/385/bmj-2023-078378. The wording is a direct description because the supplied page was not retrievable in this assessment and no further search was allowed."
    first_use_definition: "‘预先隔离、未用于模型选择的外部测试集’指在变量、状态数、阈值和更新层级确定前不用于这些选择的数据；‘不作任何重新估计’指在该测试集上不重新拟合或调整模型参数。"
    competing_forms_and_locators:
      - "真正未触碰的跨数据库检验 — line 32"
      - "未触碰数据库外测试 — line 39"
      - "未触碰最终测试 — line 66"
      - "untouched final test — lines 230-240"
      - "zero-update — lines 98, 240, 250, 355"
  - finding_id: L-006
    severity: major
    finding_kind: terminology
    category: RCT projection estimand
    dossier_locator: "One-sentence summary and primary question (lines 32, 60); Objective 4 (line 67); R0-R1 and estimand (lines 246-252); evidence chain (lines 314-320); interpretation matrix (line 368)"
    current_problem: "‘冻结观测投影’, ‘投影可观测状态摘要’, and ‘有限随机化扰动’ are introduced before a reader knows what is mapped, what is observable, or what the randomized comparison estimates. The modifier attachment in ‘投影可观测状态摘要’ is especially unclear."
    target_state: "The first use describes a fixed mapping from measured common anchors to a one-dimensional visit-specific summary and describes the contrast as a randomized group difference."
    required_change_or_replacement: "Replace first reader-facing use with ‘由冻结观测方程将实测共同锚点映射得到的一维访视状态摘要；随机分配导致的该摘要组间差异’. Use ‘投影摘要’ only after that sentence-level definition."
    content_to_preserve: "The frozen mapping, common-anchor eligibility, the R0/R1 criteria, visit-specific scope, and the stated exclusion of claims about latent dynamics, mediation, control, or the whole model."
    acceptance_test: "Before any RCT branch label, a reader can identify the input measurements, fixed operation, output summary, and randomized contrast. The replacement contains no undefined compact label and does not imply that the latent state or complete model is observed."
    term_or_phrase: "冻结观测投影 / 投影可观测状态摘要 / 随机化扰动"
    recommended_form_or_plain_description: "由冻结观测方程将实测共同锚点映射得到的一维访视状态摘要；随机分配导致的该摘要组间差异"
    evidence_basis: "The dossier gives the mapping only later at line 248. ICH E9(R1) requires the treatment effect of interest to be described precisely through an estimand and aligned analysis: https://www.ema.europa.eu/en/documents/scientific-guideline/ich-e9-r1-addendum-estimands-and-sensitivity-analysis-clinical-trials-guideline-statistical-principles-clinical-trials-step-5_en.pdf. The direct description supplies the missing first-use orientation without changing the estimand."
    first_use_definition: "该一维访视状态摘要由每项试验实际访视中直接测得、并通过语义与单位审计的共同锚点按阶段 II 冻结映射计算；随机分配比较只估计该摘要在该访视的组间差异。"
    competing_forms_and_locators:
      - "冻结观测投影门 — lines 32, 40, 60"
      - "投影可观测状态摘要 — lines 32, 42, 60, 252"
      - "投影可观测摘要扰动 — lines 67, 318, 319"
      - "投影门 / projection-pass — lines 88, 252, 383"
  - finding_id: L-007
    severity: major
    finding_kind: terminology
    category: fallback endpoint
    dossier_locator: "One-sentence summary and objectives (lines 32, 41, 67); automatic independent fallback (line 254); evidence chain and outputs (lines 317, 347); interpretation matrix (lines 369, 384)"
    current_problem: "‘death-ranked SOFA’ and ‘fallback’ are bare English labels for a ranking rule and an alternative analysis. They do not immediately tell a non-trial reader how death, in-hospital SOFA, and alive discharge are ordered, nor that the analysis is independent of stage II."
    target_state: "The endpoint and the pre-specified alternative analysis are named in direct Chinese before any shorthand."
    required_change_or_replacement: "Use ‘按死亡、访视时 SOFA 和活着出院排序的独立次要临床状态再分析（预设替代分析）’ at first use. If an English shorthand is retained, define it after this form and use it consistently."
    content_to_preserve: "Death as worst, visit-time SOFA ordering among survivors in hospital, alive discharge as most favourable, trial-specific analysis, and independence from stage II representation."
    acceptance_test: "At first use, every target reader can reconstruct the ranking and recognize that it is an alternative analysis rather than a projected-state result. No bare ‘fallback’ or ‘death-ranked’ remains in prose, titles, summaries, or figure captions."
    term_or_phrase: "death-ranked SOFA / fallback"
    recommended_form_or_plain_description: "按死亡、访视时 SOFA 和活着出院排序的独立次要临床状态再分析（预设替代分析）"
    evidence_basis: "ICH E9(R1) treats terminal and other intercurrent events as elements requiring explicit alignment to the clinical question: https://www.ema.europa.eu/en/documents/scientific-guideline/ich-e9-r1-addendum-estimands-and-sensitivity-analysis-clinical-trials-guideline-statistical-principles-clinical-trials-step-5_en.pdf. The dossier already supplies the ranking at line 254; the replacement moves that reader orientation to first use."
    first_use_definition: "该预设替代分析在投影条件未满足而试验核心语义可核验时使用：死亡排为最差，访视时存活住院者按 SOFA 排序，访视前活着出院排为最有利；它不检验阶段 II 表示。"
    competing_forms_and_locators:
      - "death-ranked SOFA 临床状态再分析 — lines 32, 41"
      - "独立 death-ranked SOFA 临床状态端点 — line 67"
      - "Automatic independent fallback — line 254"
      - "death-ranked 投影摘要 / death-ranked SOFA — lines 317, 347"
      - "fallback — lines 246, 254, 335, 405, 428"
  - finding_id: L-008
    severity: minor
    finding_kind: language
    category: unexplained internal labels, English compounds, and metaphors
    dossier_locator: "Title and structured abstract (lines 27-42); first G1 use (line 84); key techniques (lines 270-276); evidence-chain and output tables (lines 310, 317, 335, 376, 403-407)"
    current_problem: "G1, R0/R1, ‘门’, ‘降级’, ‘封印’, ‘防火墙’, and many bare English compounds occur before a functional explanation. Some terms are standard to one field, but the stated reader group cannot infer an internal gate’s content or a metaphor’s scientific consequence from its label alone."
    target_state: "First uses give a Chinese functional description; later technical shorthand is limited and stable."
    required_change_or_replacement: "Define G1 as the named data-support audit at first use; define R0/R1 by their trial-semantic and measurement-mapping functions. Prefer ‘预设通过标准/未通过后的处理’, ‘冻结并隔离的外部测试程序’, and ‘变量角色隔离规则’ to standalone ‘门/降级/封印/防火墙’. Define or translate reader-facing English compounds at first use; retain established abbreviations only after the Chinese form."
    content_to_preserve: "The protocol’s stopping rules, isolation safeguards, variable-role separation, and technical precision."
    acceptance_test: "A reader new to the project can explain G1, R0, R1, each protected-data procedure, and each variable-role rule from its first occurrence. Remaining English abbreviations are defined at first use or are universally standard for the stated audience."
  - finding_id: L-009
    severity: minor
    finding_kind: language
    category: one-sentence-summary readability
    dossier_locator: "One-sentence complete-Idea summary (line 32)"
    current_problem: "The required single sentence carries the study object, data eligibility, all stage-II gates, two RCT mappings, the fallback endpoint, and five exclusions. The semicolon does not provide enough local orientation for the mixed specialist audience."
    target_state: "One contract-compliant sentence with a clear main clause and three visibly grouped clauses."
    required_change_or_replacement: "Keep one sentence, but lead with the study object and phase-II aim; use parallel semicolon-separated clauses for (i) external test, (ii) conditional RCT projection, and (iii) fallback and excluded claims. Replace compact labels according to L-002 through L-007 rather than adding new shorthand."
    content_to_preserve: "The 24-month scope, planned status, conditional sequence, fallback, and causal/control exclusions."
    acceptance_test: "The field remains exactly one sentence and lets a reader identify its principal aim, condition, and fallback on one uninterrupted read."
  - finding_id: L-010
    severity: minor
    finding_kind: language
    category: near-verbatim limitation repetition
    dossier_locator: "Structured abstract Contribution and impact (line 42); non-hypotheses (line 73); RCT limits (lines 252, 320); interpretation matrix (lines 368-369); evidence ladder (lines 383-384)"
    current_problem: "The same long list excluding latent dynamics, transfer edges, mediation, control, and whole-model validation recurs with only small lexical changes. This repetition makes the central limitation harder, rather than easier, to scan."
    target_state: "Each required section retains its locally necessary boundary in a short, stable form."
    required_change_or_replacement: "Use one stable short formulation for the shared exclusion list and remove only near-verbatim duplicate wording within the relevant field. Keep the distinct projection and independent-analysis boundaries; do not decide which section owns the complete scientific limitation."
    content_to_preserve: "All limitations on causal, mechanistic, control, digital-twin, and whole-model claims."
    acceptance_test: "A whole-dossier search finds a stable form for the shared limitation and no duplicate multi-item list that adds no local distinction; every affected contract field remains complete."
unresolved_issues: [L-001, L-002, L-003, L-004, L-005, L-006, L-007, L-008, L-009, L-010]
---

# Language Assessment Report

**Assessment ID**: language-assessment-r095  
**Target Language**: bilingual (Chinese prose with English technical terms)  
**Discipline**: critical care, clinical epidemiology, longitudinal statistics, system identification, medical AI, and translational research  
**Scope**: complete idea dossier  
**Date**: 2026-07-20

## Overall Language Readiness

**Level**: major_language_revision

**Recommendation**: revise_language

## Dimension Scores

| Dimension | Score (1–10) | Severity |
|---|---:|---|
| Grammar & Syntax | 8 | pass |
| Academic Register & Tone | 7 | borderline |
| Terminology Consistency | 3 | fail |
| Tense & Voice Conventions | 8 | pass |
| Conciseness & Redundancy | 5 | borderline |
| Readability & Flow | 5 | borderline |

## Hard Gate Status

**Overall**: fail

| Gate | Status | Detail |
|---|---|---|
| Grammar error density | pass | No pattern approaching three clear grammatical errors per 500 words was found. |
| Academic register | pass | Formal research register is sustained; English-heavy technical labels are a clarity issue, not pervasive informality. |
| Terminology coherence | fail | Several title-, design-, and endpoint-controlling labels are inconsistent, misleading across disciplines, or undefined at first use (L-001–L-007). |
| Tense systematic violation | pass | This is a prospective Idea dossier; future and conditional formulations match that status. |

## Strengths

- The dossier consistently distinguishes planned work from completed results.
- Causal, control, and digital-twin exclusions are stated explicitly.
- Prospective conditional language is appropriate throughout the protocol and trial sections.
- Tables make many quantitative thresholds and alternative actions locatable.

## Specific Issues

### Chinese Academic Clarity

L-008 through L-010 address the dense mixed-language labels, metaphors, one-sentence summary, and lexical repetition. The recommended actions preserve the one-sentence and table-field constraints.

### Terminology Consistency

| id | term_or_phrase | locator | reader_effect | action_in_frontmatter |
|---|---|---|---|---|
| L-001 | central study-object labels | title, summary, question, Objective 2 | unclear referent | yes |
| L-002 | 可观测性审计 / G1 | summary through WP1 | conflates data support with system observability | yes |
| L-003 | 绝对恢复 / 假置信 | summary, objectives, recovery gate | unclear simulated target and error claim | yes |
| L-004 | 弃权 | background through outputs | unclear withheld action | yes |
| L-005 | 未触碰 / zero-update | summary through validation | conflates isolation with no re-estimation | yes |
| L-006 | projection terms / randomized perturbation | summary through RCT estimand | opaque mapping and contrast | yes |
| L-007 | death-ranked SOFA / fallback | summary through interpretation | opaque endpoint and alternative analysis | yes |

### Conciseness & Redundancy

L-009 preserves the mandated one-sentence summary while improving its clause structure. L-010 is a lexical-duplication finding only; it does not select a single narrative location for the full scientific limitation.

### Readability & Flow

The key readability barrier is not sentence grammar but readers’ need to decode several project-local labels before the later operational definitions. Addressing L-001 through L-008 before shortening prose will have the largest effect.

## Candidate Disposition and Replacement Re-check

The bounded scanner’s specified candidate groups were all reviewed. L-001 addresses the central object; L-002 covers G1 and observability; L-003 covers recovery and false-confidence labels; L-004 abstention; L-005 untouched/zero-update; L-006 projection and randomized-effect language; L-007 death-ranked and fallback language; L-008 gates, downgrade, sealing, firewall, abbreviations, and bare English; L-009 and L-010 cover the title/summary/question/limitation repetition pattern. Each terminology replacement was re-checked for a direct referent, unambiguous modifier attachment, first-use definition, and absence of a newly invented compact label. The limited supplied evidence did not verify project-specific composites; those findings therefore use direct descriptions rather than substitute jargon.

## Language Revision Priorities

1. **Terminology**: 7 major issues — establish reader-ready first uses and one name per core role.
2. **Mixed-language clarity**: 1 minor issue — define internal labels and replace metaphors with scientific functions.
3. **Concision and readability**: 2 minor issues — restructure the one-sentence summary and remove only near-verbatim repetition.

## Assessment Notes

This was a language-only assessment, not a judgment of validity, feasibility, novelty, or scientific merit. The embedded reader profile was: zh-CN readers from critical care, clinical epidemiology, longitudinal statistics, system identification, medical AI, and translational research; each has domain training but does not know project-internal labels or coined composites.

The dossier was read in three contiguous segments (lines 1–110, 111–230, and 231–480) and scanned with the required bounded candidate scanner. No prior report, plan, brief, revised dossier, or test artifact was read. The only external terminology/method sources consulted were the five URLs supplied in the task; the Morris and TRIPOD+AI pages were not retrievable through the supplied URLs during this assessment, so their findings use direct descriptive wording rather than additional search evidence.
