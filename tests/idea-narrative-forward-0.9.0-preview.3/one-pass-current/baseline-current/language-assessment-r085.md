---
review_id: language-assessment-I01-001-v003-r085
reviewer_skill: academic-language-assessor
reviewer_instance_id: fresh-language-v003-r085
workflow_id: RID-SEPSIS-CSM-20260717-001
round_id: r085
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
  - research-skills-openai/AGENTS.md
  - research-skills-openai/skills/academic-language-assessor/SKILL.md
  - research-skills-openai/skills/academic-language-assessor/templates/language-assessment-report.md
  - research-skills-openai/skills/academic-language-assessor/references/language-assessment-rubric.md
  - research-skills-openai/skills/academic-language-assessor/references/language-hard-gates.md
  - research-skills-openai/skills/academic-language-assessor/references/english-academic-language-conventions.md
  - research-skills-openai/skills/academic-language-assessor/references/chinese-academic-language-conventions.md
  - research-skills-openai/skills/academic-language-assessor/references/discipline-language-conventions.md
  - research-skills-openai/skills/academic-language-assessor/references/terminology-review.md
  - research-skills-openai/skills/academic-language-assessor/scripts/scan_idea_language_candidates.py
  - research-skills-openai/skills/academic-language-assessor/scripts/validate_language_assessment.py
  - tests/idea-test-0.9.0-preview.1/0.9.0-preview.1/03_ideas/nodes/I01-001/dossiers/idea-dossier-v003.md
  - tests/idea-narrative-forward-0.9.0-preview.3/run-001/inputs/reader-handoff.yaml
isolation_mode: fresh_subagent
prior_scores_visible: false
source_edits_performed: false
decision: major_language_revision
findings:
  - finding_id: LANG-R085-001
    severity: major
    finding_kind: terminology
    category: reader-inaccessible project-specific stage label
    dossier_locator: "Research content and work packages > Twenty-four-month minimum and dated gates, line 84; Data, materials, and existing evidence base > Public ICU database roles and G1 audit, lines 138-153"
    current_problem: >-
      “G1” first appears in a decision table without expansion and later alternates among “G1 硬下限”, “G1 支持”, “G1 可观测性” and “G1 审计”. The supplied readers cannot be assumed to know this project-specific label, although it determines model complexity, database eligibility, stopping and downgrade decisions.
    target_state: >-
      The first reader-facing occurrence identifies G1 as the planned cross-database observability and data-support audit, after which one stable short form is used for the same audit.
    required_change_or_replacement: >-
      At the first occurrence, use “双库可观测性与数据支持审计（G1 审计）”; thereafter use “G1 审计” for the audit and direct phrases such as “G1 审计预设的最低支持标准” when the threshold rather than the audit is meant.
    content_to_preserve: >-
      Preserve every existing audit component, date, support threshold, role assignment, model-complexity consequence, backup-database condition and stopping rule.
    acceptance_test: >-
      A whole-dossier search shows that the first “G1” occurrence includes the direct definition, every later occurrence distinguishes the audit from its thresholds or results, and no bare “G1” requires a project glossary.
    term_or_phrase: G1
    recommended_form_or_plain_description: 双库可观测性与数据支持审计（G1 审计）
    evidence_basis: >-
      The dossier itself enumerates the referent in the G1 audit table: access, sample and event support, hospitals, timestamps, common anchors, interfaces, missingness and the complexity cap. Direct descriptive wording is therefore available without inventing a new label.
    first_use_definition: >-
      “G1 审计”是模型拟合前对两个数据库的数据访问、事件与转移支持、医院覆盖、时间戳、共同生理锚点、接口和缺失情况进行的可观测性与数据支持审计，其结果决定时间网格、模型复杂度及是否继续跨数据库分析。
    competing_forms_and_locators:
      - "G1 硬下限 — line 84"
      - "G1 可观测性 — lines 103 and 138"
      - "G1 支持 — lines 284-296 and 380-404"
  - finding_id: LANG-R085-002
    severity: major
    finding_kind: terminology
    category: inconsistent cross-language name for the primary external-validation condition
    dossier_locator: "Structured abstract, line 42; Conjunctive minimum success definition, lines 92-100; Hospital-primary genuine cross-database validation, lines 230-240; Interpretation matrix, lines 364-366"
    current_problem: >-
      The central external-validation condition is named “零更新”, “zero update” and “zero-update”, often beside the separate labels “calibration-only” and “observation-layer update”. The form changes across Chinese prose and tables, and its meaning is not defined at first use for the multidisciplinary reader.
    target_state: >-
      One Chinese term names the test in which external test data do not update model parameters, and any English short form appears only after a direct first-use explanation.
    required_change_or_replacement: >-
      Replace the first occurrence with “不使用外部测试数据更新任何模型参数的外部检验（下称‘零更新外部检验’）” and use “零更新外部检验” thereafter; retain separate direct names for recalibration-only, observation-layer-only updating and full refitting.
    content_to_preserve: >-
      Preserve the ordering of the external analyses, the isolation of the final test set, the distinction among zero update, recalibration, observation-layer updating and full refitting, and the rule that limited updating cannot compensate for failure of the primary external test.
    acceptance_test: >-
      A whole-dossier search finds one defined retained form, “零更新外部检验”, for this condition; “zero update”, “zero-update” and bare “零更新” no longer occur in reader-facing prose or free-form table cells, and the three alternative update levels remain distinguishable.
    term_or_phrase: 零更新 / zero update / zero-update
    recommended_form_or_plain_description: 不使用外部测试数据更新任何模型参数的外部检验（零更新外部检验）
    evidence_basis: >-
      The method section directly states that this is the primary external test performed before adaptation-only recalibration or observation-layer updating. A plain description therefore conveys the intended operation more reliably than the mixed-language compact forms.
    first_use_definition: >-
      零更新外部检验是指冻结标签、预处理、模型、参数、阈值和评价代码后，在未触碰的外部测试数据上直接评价模型，不利用该测试数据调整任何模型部分。
    competing_forms_and_locators:
      - "零更新 / 零更新外部检验 — lines 42, 98, 355 and 404"
      - "zero update — lines 109, 240 and 309"
      - "zero-update — lines 250, 355, 365-366, 382 and 427"
  - finding_id: LANG-R085-003
    severity: major
    finding_kind: terminology
    category: inaccessible and competing names for the fallback RCT outcome
    dossier_locator: "Title, summary, audience, and positioning > one-sentence summary, line 32; Background, current state, gap, significance, and rationale, line 54; Conditional trial-observation projection and independent fallback, lines 246-259; Evidence chains, lines 314-320"
    current_problem: >-
      The fallback outcome is introduced as “death-ranked SOFA” before its ranking rule is explained, then appears as “独立 SOFA”, “独立 death-ranked SOFA”, “trial-specific independent secondary clinical-state reanalysis” and “trial-specific clinical-state 再分析”. These forms obscure whether the label refers to an outcome, an analysis or a branch, and they are not accessible at the supplied cross-disciplinary baseline.
    target_state: >-
      The first use states the clinical ordering and identifies the analysis as independent of the stage-II representation; one stable Chinese name is then used for the endpoint and one for the reanalysis.
    required_change_or_replacement: >-
      At first use, describe the fallback as “按死亡最差、访视时住院存活者的 SOFA 评分由高到低、访视前存活出院最优排序的试验特异独立次要临床状态再分析”; thereafter use “独立次要临床状态端点” for the ordered endpoint and “试验特异独立次要临床状态再分析” for the analysis.
    content_to_preserve: >-
      Preserve the exact death, in-hospital SOFA and alive-discharge ordering; the D7/D8 visit specificity; trial separation; randomization-compatible analysis; and the prohibition on interpreting this fallback as perturbing or validating the stage-II representation.
    acceptance_test: >-
      The summary contains the complete ordering in direct Chinese, the methods use distinct stable names for endpoint and analysis, and a whole-dossier search finds no undefined “death-ranked”, “trial-specific clinical-state” or “独立 SOFA” shorthand.
    term_or_phrase: death-ranked SOFA / 独立 SOFA / trial-specific clinical-state reanalysis
    recommended_form_or_plain_description: 按死亡、住院存活者 SOFA 评分和存活出院结局排序的试验特异独立次要临床状态再分析
    evidence_basis: >-
      The dossier supplies the complete ordering in the “Automatic independent fallback” paragraph and distinguishes this fallback from the projection endpoint. The recommended wording is a direct description of that stated operation, not a newly coined label.
    first_use_definition: >-
      该独立次要临床状态端点将死亡列为最差等级，将访视时仍住院存活者按 SOFA 评分从高到低排序，并将访视前存活出院列为最优等级；它不使用阶段 II 的投影摘要。
    competing_forms_and_locators:
      - "death-ranked SOFA / death-ranked 投影摘要 — lines 32, 41, 67, 317 and 347"
      - "独立 SOFA — lines 88, 254, 356, 369 and 428"
      - "trial-specific independent secondary clinical-state reanalysis — line 254"
      - "trial-specific clinical-state 再分析 — line 318"
  - finding_id: LANG-R085-004
    severity: major
    finding_kind: language
    category: reader-entry sentence overload
    dossier_locator: "Title, summary, audience, and positioning > One-sentence complete-Idea summary, line 32"
    current_problem: >-
      The contract-fixed one-sentence summary carries the population, data-access caveat, four-part disease continuum, model properties, two evidence stages, three stage-III conditions, two trial visits, the fallback and six prohibited interpretations in one heavily nested sentence. The main research object and decision sequence are recoverable only after repeated reading.
    target_state: >-
      A single sentence presents, in order, the planned representation, the stage-II validation objective, the conditional RCT analysis or fallback, and the interpretation boundary, using only terms defined at or before their use.
    required_change_or_replacement: >-
      Preserve the one-sentence field but reduce nested modifiers, replace internal shorthand with direct descriptions, group the three stage-III prerequisites once, and compress the final prohibition list into one precise evidence-boundary clause without deleting any distinct branch.
    content_to_preserve: >-
      Preserve the 24-month stage-I–II horizon, two auditable public ICU databases, pre-onset/onset/post-onset/outcome coverage, knowledge and uncertainty constraints, simulation recovery and untouched external testing, conditional separate EXIT-SEP D7 and XBJ-SCAP D8 analyses, the independent SOFA fallback, and the boundary against causal-network, continuous-dynamics, control and digital-twin claims.
    acceptance_test: >-
      The field remains exactly one sentence; its grammatical subject and main action occur before the stage conditions; each condition has one explicit consequence; all compact labels are defined or removed; and the four required information blocks can be identified without resolving a backward reference.
  - finding_id: LANG-R085-005
    severity: major
    finding_kind: language
    category: project-management and software metaphors in scientific prose
    dossier_locator: "Background, current state, gap, significance, and rationale, lines 50-54; Research content and work packages, lines 83-112; Hospital-primary genuine cross-database validation, lines 230-240; Key techniques and implementation, lines 269-278; Falsification and stop criteria, lines 349-358"
    current_problem: >-
      Core scientific decisions are repeatedly expressed through project-internal or software metaphors such as “按门实施”, “恢复门”, “假置信门”, “外部门”, “打开 test”, “外部封印”, “角色防火墙”, “预测好不能豁免”, “挽救” and “调阈救回”. These phrases sound operational rather than academic and force readers to infer whether each instance denotes a criterion, an access restriction, a failed estimand, a reporting consequence or a model-selection rule.
    target_state: >-
      Each sentence directly names the scientific criterion or data-governance action and its consequence, while short labels are retained only after an explicit definition and only when they denote one stable function.
    required_change_or_replacement: >-
      Replace metaphorical uses with direct phrases such as “预先设定的判定标准”, “在满足泄漏审计要求前不访问外部测试结果”, “不能抵消该项失败”, “变量用途隔离规则” and “失败模式可视化”; revise each listed section locally so the actor, assessed object, criterion and consequence are explicit.
    content_to_preserve: >-
      Preserve every model-admission threshold, access restriction, downgrade path, abstention rule, failed-criterion consequence, data-role separation and prohibition on compensating for a failed primary criterion with another result.
    acceptance_test: >-
      In each bounded section, every occurrence of “门”, “封印”, “打开”, “防火墙”, “挽救”, “救回” or “豁免” either has an immediately stated single scientific referent or is replaced by a direct description; no replacement merges distinct criteria, failure states or actions.
  - finding_id: LANG-R085-006
    severity: major
    finding_kind: terminology
    category: ambiguous modifier attachment in the title
    dossier_locator: "H1 title, line 27; Title field, line 31; Background, current state, gap, significance, and rationale, line 54; Conditional trial-observation projection and independent fallback, line 261"
    current_problem: >-
      In “条件性稀疏 RCT 次要再分析”, ordinary Chinese attachment makes “稀疏” appear to modify the randomized controlled trial itself. The dossier later shows that the sparse property belongs to repeated visit measurements, while “条件性” belongs to whether the secondary analysis may proceed.
    target_state: >-
      The title unambiguously attaches the conditional status to initiation of the secondary analysis and the sparse property to the trial visit data.
    required_change_or_replacement: >-
      Use the title “脓毒症全病程的候选动态系统表征：计划开展跨数据库检验，并在条件满足时次要分析含稀疏访视数据的随机对照试验” in both the H1 and Title field, or an equally direct form with the same modifier attachments.
    content_to_preserve: >-
      Preserve “候选” and “计划” evidence status, the sepsis full-course scope, planned cross-database testing, the conditional nature of stage III, the secondary-analysis status, and the fact that the RCT visit measurements are sparse.
    acceptance_test: >-
      The H1 and Title field match; a grammatical parse assigns “稀疏” only to visit data and “条件满足” only to proceeding with the secondary analysis; the title does not imply completed validation, a sparse randomization design or pooled trials.
    term_or_phrase: 条件性稀疏 RCT 次要再分析
    recommended_form_or_plain_description: 在条件满足时次要分析含稀疏访视数据的随机对照试验
    evidence_basis: >-
      The dossier states that EXIT-SEP and XBJ-SCAP have sparse repeated D1/D4/D7 or D0/D4/D8 measurements and that stage III proceeds only after stage-II, trial-semantics and projection conditions are met. The ambiguity is therefore established by the dossier's own use, and direct wording is sufficient.
    first_use_definition: >-
      “条件满足”指预先规定的阶段 II、试验语义和观测投影条件均达到要求；“稀疏访视数据”指试验仅在少数离散访视时点记录相关测量。
    competing_forms_and_locators: []
unresolved_issues:
  - LANG-R085-001
  - LANG-R085-002
  - LANG-R085-003
  - LANG-R085-004
  - LANG-R085-005
  - LANG-R085-006
---

# Language Assessment Report

**Assessment ID**: language-assessment-I01-001-v003-r085  
**Target Language**: Chinese  
**Discipline**: Critical-care medicine and clinical epidemiology, with longitudinal statistics, systems identification, and medical AI  
**Target Journal**: Not specified  
**Scope**: Complete Idea dossier  
**Date**: 2026-07-20

---

## Overall Language Readiness

**Level**: major_language_revision

**Recommendation**: revise_language

---

## Dimension Scores

| Dimension | Score (1–10) | Severity |
|-----------|-------------|----------|
| Grammar & Syntax | 8 | pass |
| Academic Register & Tone | 5 | borderline |
| Terminology Consistency | 4 | fail |
| Tense & Voice Conventions | 9 | pass |
| Conciseness & Redundancy | 5 | borderline |
| Readability & Flow | 4 | fail |

---

## Hard Gate Status

**Overall**: fail

| Gate | Status | Detail |
|------|--------|--------|
| Grammar error density | pass | Approximately 0–1 clear grammatical errors per 500 Chinese word-equivalents; the dominant problems are terminology and sentence load, not grammar |
| Academic register | pass | Formal tone is sustained, although project-management and software metaphors reduce disciplinary naturalness in five bounded section groups |
| Terminology coherence | fail | At least three core decision terms are undefined, competing across languages, or misleading at first use: G1, zero-update, and the death-ranked/independent SOFA fallback; the title also misattaches “稀疏” |
| Tense systematic violation | pass | Prospective and conditional language is appropriate for a planned Idea dossier; no completed study is systematically described as planned or vice versa |

---

## Strengths

- The dossier consistently marks proposed work as planned, conditional, unverified, or not yet generated, and does not use tense to imply completed validation.
- Causal, predictive, transportability, projection, and fallback interpretations are repeatedly distinguished with explicit evidence-status limits.
- Tables generally keep populations, criteria, metrics, consequences, and stop rules locatable, which supports targeted language revision without changing the scientific design.
- Standard clinical abbreviations and mathematical symbols are mostly used consistently once their technical context is established.

---

## Specific Issues

### Chinese Academic Clarity

- **LANG-R085-004 (major):** The one-sentence summary is structurally overloaded at the main reader-entry point; the fixed one-sentence format can be preserved while reducing nested modifiers and backward references.
- **LANG-R085-005 (major):** Five bounded section groups use internal operational metaphors where direct scientific descriptions of criteria, access restrictions, failure states and consequences are needed.

### Grammar & Syntax

No recurring grammatical error pattern met the threshold for an actionable finding. Long dependency chains affect readability but do not constitute pervasive grammatical errors.

### Academic Register & Tone

- **LANG-R085-005 (major):** “门”, “封印”, “打开 test”, “防火墙”, “挽救” and “救回” create a project-management or software register in otherwise formal scientific prose.

### Terminology Consistency

| id | term_or_phrase | locator | reader_effect | action_in_frontmatter |
|---|---|---|---|---|
| LANG-R085-001 | G1 | lines 84 and 138-153 | Project-specific stage label is undefined where it first controls decisions | yes |
| LANG-R085-002 | 零更新 / zero update / zero-update | lines 42, 92-100, 230-250 and 364-366 | Central external-test condition changes form and lacks a direct first-use definition | yes |
| LANG-R085-003 | death-ranked SOFA / 独立 SOFA / trial-specific clinical-state reanalysis | lines 32, 54, 246-259 and 314-320 | Readers cannot immediately distinguish the ordered endpoint, the analysis and the fallback branch | yes |
| LANG-R085-006 | 条件性稀疏 RCT 次要再分析 | title and lines 54 and 261 | “稀疏” appears to modify the trial rather than its visit data | yes |

### Tense & Voice Conventions

No actionable issue. Prospective wording is appropriate for planned methods, outputs and conditional later-stage analyses; established literature and current evidence limits are stated in compatible present or past forms.

### Conciseness & Redundancy

- **LANG-R085-004 (major):** The summary combines too many individually necessary conditions in one nested construction. The revision should compress expression, not remove scientifically distinct conditions.
- **LANG-R085-005 (major):** Repeated short metaphors save words locally but create explanatory burden and force readers to reconstruct the intended operation.

### Readability & Flow

- **LANG-R085-004 (major):** The primary summary delays the main decision sequence behind stacked modifiers and subordinate conditions.
- **LANG-R085-001, LANG-R085-002, LANG-R085-003 and LANG-R085-006 (major):** Undefined compact labels and ambiguous modifier attachment interrupt the cross-disciplinary reasoning chain at the title, summary, stage gates and external-validation sections.

---

## Language Revision Priorities

1. **Terminology consistency and reader entry**: 4 issues — define G1 and the primary external-test condition, replace competing fallback labels with direct Chinese descriptions, and repair the title's modifier attachment.
2. **Readability and flow**: 1 issue — retain the required one-sentence summary while restoring a direct object-to-validation-to-conditional-analysis sequence.
3. **Academic register**: 1 issue — replace project-management and software metaphors with explicit scientific criteria, actions and consequences in the bounded sections.

---

## Re-Assessment Status (if applicable)

Not applicable. This is a fresh complete-Idea assessment; no prior issue list, score, decision, dossier version, or revision delta was read.

---

## Assessment Notes

The assessment used the supplied `zh-CN` reader handoff and treated the dossier as a planned cross-disciplinary clinical-methodological Idea rather than a completed empirical report. No target journal was supplied, so the Chinese academic-language, biomedical/clinical, computer-science/engineering, and cross-cutting scientific conventions were applied. The fixed research-idea.v3 headings, field labels, evidence-chain labels and Claim-Support schema headers were treated as exempt scaffolding. The bounded candidate scan was run after terminology triggers were identified; its output was used only to prompt semantic review and was not persisted. Scientific validity, novelty, feasibility, impact and journal fit were not assessed, and the source dossier and reader handoff were not edited.
