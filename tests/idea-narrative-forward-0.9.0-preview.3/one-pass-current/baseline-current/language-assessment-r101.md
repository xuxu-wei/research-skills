---
review_id: language-assessment-r101
reviewer_skill: academic-language-assessor
reviewer_instance_id: fresh-language-assessor-r101
workflow_id: RID-SEPSIS-CSM-20260717-001
round_id: baseline-current-r101
input_artifact_ids:
  - idea-dossier-I01-001-v003
input_versions:
  - v003
scope: complete_idea_dossier
dossier_ref:
  artifact_id: idea-dossier-I01-001-v003
  version: v003
  path: tests/idea-test-0.9.0-preview.1/0.9.0-preview.1/03_ideas/nodes/I01-001/dossiers/idea-dossier-v003.md
reader_handoff:
  artifact_id: embedded-reader-handoff
  version: embedded
  path: null
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
  - research-skills-openai/skills/academic-language-assessor/scripts/scan_idea_language_candidates.py
  - research-skills-openai/skills/academic-language-assessor/scripts/validate_language_assessment.py
  - tests/idea-test-0.9.0-preview.1/0.9.0-preview.1/03_ideas/nodes/I01-001/dossiers/idea-dossier-v003.md
  - https://sites.stat.washington.edu/raftery/Research/PDF/Gneiting2007jasa.pdf
  - https://www.tripod-statement.org/scope/
  - https://www.fda.gov/regulatory-information/search-fda-guidance-documents/e9r1-statistical-principles-clinical-trials-addendum-estimands-and-sensitivity-analysis-clinical
  - https://www.consort-spirit.org/item14-outcomes
isolation_mode: fresh_subagent
prior_scores_visible: false
source_edits_performed: false
decision: major_language_revision
findings:
  - finding_id: LANG-R101-01
    severity: major
    finding_kind: terminology
    category: core-rct-endpoint-and-contrast-language
    dossier_locator: "lines 32, 41-42, 60, 67, 88, 242-261, 314-320, 347, 368-369, 383-384, 405-406, and 428"
    current_problem: >-
      The reader-entry text names three core RCT roles with compact or mixed-language labels—“投影可观测状态摘要”, “随机化扰动”, and “death-ranked SOFA”—before the measurement, ranking, and comparison operations are identifiable. Later passages alternate among “投影摘要”, “投影可观测摘要”, P_obs, several “扰动” forms, “组间不同”, “独立 SOFA 端点”, and an English project label. A multidisciplinary reader therefore cannot tell at first use which variable is analysed, how participants are ranked, what population-level comparison is estimated, or what the fallback endpoint contains.
    target_state: >-
      The first reader-facing occurrence directly identifies the projected endpoint, the randomized-group comparison, and the independent fallback endpoint; one stable short form is used for each role only after that definition.
    required_change_or_replacement: >-
      In the one-sentence summary, retain one sentence but replace the three compact labels with direct role descriptions: (a) an one-dimensional state summary mapped by the frozen stage-II observation equation and calculable from measured common anchors at the actual D7/D8 visit; (b) the prespecified randomized-group contrast on that visit-specific hierarchical outcome, reported with the stated probabilistic index or win probability; and (c) if projection fails, a trial-specific hierarchical clinical-state outcome that ranks pre-visit death worst, in-hospital survivors by SOFA from worse to better, and pre-visit live discharge best. Define a short Chinese form for each and apply it consistently thereafter.
    content_to_preserve: >-
      Preserve the conditional stage-II dependency, separate analysis of the two trials, actual-visit restriction, projection-failure fallback, treatment-policy and missing-data specifications, one-sentence summary cardinality, and all explicit limits on causal, mechanistic, control, and whole-system interpretation.
    acceptance_test: >-
      A fresh reader can identify from line 32 alone the measured/mapped variable, participant ranking, comparison between randomized groups, and fallback composition; the summary remains one sentence; P_obs is introduced only with its formula; a whole-dossier check finds one defined name per RCT role and no unexplained “death-ranked”, generic “扰动”, or competing endpoint label.
    term_or_phrase: "投影可观测状态摘要；随机化扰动；death-ranked SOFA"
    recommended_form_or_plain_description: >-
      “由冻结阶段-II观测方程映射且可由实际 D7/D8 实测共同锚点计算的一维状态摘要”；“随机分配组在该预设访视层级结局上的概率指数/胜出概率比较”；“死亡最差、住院存活者按 SOFA 由高到低排序、存活出院最优的试验特异次要层级临床状态结局”。
    evidence_basis: >-
      FDA ICH E9(R1) requires the treatment effect of interest to be described clearly enough to avoid misunderstanding, and CONSORT-SPIRIT Item 14 requires the outcome variable, participant-level metric, aggregation, and time point to be completely defined. Focused verification did not establish the dossier's compact English fallback label as a reader-independent standard, so direct descriptive wording is preferred.
    first_use_definition: >-
      At first use, state that the projection branch compares randomized groups on a D7/D8 hierarchical endpoint built from a frozen, anchor-calculable one-dimensional summary, whereas the independent fallback replaces that summary with the explicitly ranked death/discharge/SOFA clinical state.
    competing_forms_and_locators:
      - "投影可观测状态摘要 (lines 32, 252); 投影可观测摘要 (lines 42, 60, 88, 318-319, 347, 368, 383, 406); 投影摘要 (lines 67, 317, 383); P_obs (lines 248-252)"
      - "随机化扰动 (lines 60, 67, 368); 访视特异扰动 (lines 42, 88); 摘要扰动 (lines 318, 383, 406); 组间不同 (lines 368-369)"
      - "death-ranked SOFA (lines 32, 41, 67, 317, 347, 384, 428); 独立 SOFA 端点/分支 (lines 42, 88, 110, 125, 276, 356, 369, 395, 405); trial-specific independent secondary clinical-state reanalysis (line 254); 独立试验临床状态 (line 384)"
  - finding_id: LANG-R101-02
    severity: minor
    finding_kind: terminology
    category: validation-update-and-scoring-terminology
    dossier_locator: "lines 40-42, 86-110, 187-189, 228-240, 250, 301-312, 331, 355, 365-366, 382, 404, and 427"
    current_problem: >-
      The same external-evaluation operation alternates among “零更新”, “zero-update”, and “zero update”, while calibration, observation-layer updating, decoder adaptation, and full refitting are named in mixed Chinese-English forms. The success criteria also use “proper score”, although the standard statistical concept is a proper scoring rule and the dossier later names Brier and CRPS. These variants obscure which model components remain frozen and which performance rule is applied.
    target_state: >-
      External validation without model updating, recalibration, observation-model updating, and full refitting are named as distinct operations in one stable bilingual mapping; proper scoring rules are named correctly and linked to the prespecified score actually used.
    required_change_or_replacement: >-
      Define the principal operation once as applying the frozen model to external data without re-estimating any parameter, then use one Chinese short form consistently. Separately name recalibration, observation-model updating, and full refitting. Replace “proper score” with “适当评分规则” or “严格适当评分规则” as warranted, followed by the named Brier or CRPS measure used in that task.
    content_to_preserve: >-
      Preserve the hospital-prioritized split, untouched final evaluation, the order of no-update evaluation and limited updates, the rule that updating cannot rescue failure of the frozen model, all numerical thresholds, and the distinction between main and secondary tasks.
    acceptance_test: >-
      A whole-dossier concordance check finds one defined term for evaluation without updating and distinct terms for each allowed update; every English short form has a first-use Chinese mapping; “proper score” no longer appears, and each success criterion names a proper scoring rule or its specific Brier/CRPS instance.
    term_or_phrase: "零更新 / zero-update / zero update；proper score"
    recommended_form_or_plain_description: >-
      “不使用外部数据重估任何参数的外部验证” followed by a stable short form; distinct Chinese descriptions for recalibration, observation-model updating, and full refitting; “适当评分规则（如 Brier 评分）” for the forecast-evaluation criterion.
    evidence_basis: >-
      TRIPOD+AI distinguishes evaluation in other data from model updating and gives recalibration and refitting as updating operations. Gneiting and Raftery define the standard concept as a proper scoring rule and identify the Brier score as an example.
    first_use_definition: >-
      State at first use that the principal external evaluation applies the frozen model unchanged to data not used for development, whereas the subsequent analyses separately re-estimate only calibration or the observation component; identify Brier or CRPS as the applicable proper scoring rule.
    competing_forms_and_locators:
      - "零更新 (lines 40, 42, 87, 98, 310, 312); zero-update (lines 98, 250, 355, 365-366, 382, 404, 427); zero update (lines 240, 309); zero/calibration/observation (line 109)"
      - "proper score (lines 42, 86, 108, 301, 331, 355, 427); Brier (lines 96, 98, 187, 189, 302); CRPS (line 265)"
  - finding_id: LANG-R101-03
    severity: minor
    finding_kind: terminology
    category: project-specific-gate-and-negative-output-labels
    dossier_locator: "lines 39-41, 50-52, 71, 84-112, 122-125, 212-225, 278, 293-318, 329-346, 353, 376, 382, 404, and 435"
    current_problem: >-
      Project-specific labels such as “G1”, “假置信门”, and “失败图” occur in the summary, hypothesis, decision consequences, and planned outputs before their scientific referents are directly named. “G1” is never expanded as a compact label, “假置信” receives quantitative detail only much later, and “失败图” does not identify which result, criterion, stratification, or consequence the figure displays.
    target_state: >-
      Each stage label is introduced after a direct description of the scientific threshold it abbreviates, and every negative-result artifact states the failed quantity, comparison or subgroup, threshold, and resulting interpretation or action.
    required_change_or_replacement: >-
      At first use, describe G1 as the frozen minimum support requirements for the two databases' samples, events/transitions, hospitals, and common anchors; describe false confidence as high-confidence support for an incorrect structure under null-edge or misspecified simulations; replace each generic “失败图” with a context-specific name that states the metric or object failing its prespecified criterion and the displayed stratification or consequence.
    content_to_preserve: >-
      Preserve all gate thresholds, dates, automatic fallback or stopping consequences, abstention rules, publication of negative results, and distinctions among data insufficiency, model misspecification, external transport failure, and RCT projection failure.
    acceptance_test: >-
      The first occurrence of G1 and false-confidence language gives a direct scientific definition before the short form; every later short form maps to that definition; each former “失败图” occurrence names the result and criterion shown; and all negative-result outputs remain explicitly deliverable under failure.
    term_or_phrase: "G1；假置信（门）；失败图"
    recommended_form_or_plain_description: >-
      “双库样本、事件/转移、医院及共同锚点的最低支持要求（G1）”；“零边或模型错设情景下错误结构被高置信支持的比例及拒绝解释标准”；“显示未达到预设标准的指标、分层对象和后续处置的结果图”，并按各处实际内容具体命名。
    evidence_basis: >-
      Whole-dossier concordance and the stated multidisciplinary reader baseline show that these are project-specific labels rather than shared terms across critical care, clinical epidemiology, longitudinal statistics, system identification, and medical AI. No standard-term claim is needed because direct descriptive wording is available from the dossier's own later criteria.
    first_use_definition: >-
      Introduce each short label only after naming its measured quantity, threshold class, and decision consequence; for a negative-result figure, name what failed and what the figure permits the reader to conclude.
    competing_forms_and_locators:
      - "G1, G1 硬下限, G1 审计, G1 支持 and G1 可观测性 (lines 84, 98, 100, 106, 112, 122, 127, 131, 138, 142-153, 161, 246, 270, 290, 326, 343, 352, 380, 403, 407, 422, 435)"
      - "假置信门, 零边假置信, 错设假置信, 错误结构高置信 and 假置信/弃权 (lines 39, 41, 52, 66, 71, 85, 225, 293, 329, 345, 353, 376)"
      - "失败图 (lines 41, 87, 109, 309, 346, 382, 404); 失败中心/亚组/观察密度图 (line 302); stable/database-specific/abstained 清单 (line 310)"
  - finding_id: LANG-R101-04
    severity: minor
    finding_kind: language
    category: reader-facing-internal-and-mixed-status-labels
    dossier_locator: "lines 121-129, 310, 403-410, and 439"
    current_problem: >-
      Free-form reader-facing tables and prose expose unexplained English or workflow-state labels, including “project-local derivative”, “not generated”, “supported/qualified/unsupported”, “editorial_repositioning”, “scientific_discovery”, “stable/database-specific/abstained”, and the prose forms “identity_status” and “new_idea_required”. Unlike fixed scaffold fields, these occurrences are ordinary prose or free-form table cells and interrupt a Chinese academic reading path.
    target_state: >-
      Reader-facing prose and free-form labels use natural Chinese scientific descriptions, with an English technical term retained only when it is standard and mapped at first use.
    required_change_or_replacement: >-
      Replace status-machine and project-management labels in prose and free-form tables with direct Chinese descriptions of evidence status, scope qualification, stability, abstention, preserved research identity, or the need to formulate a substantively new research idea. Keep required machine frontmatter unchanged.
    content_to_preserve: >-
      Preserve the exact evidence-status distinctions, the separation of verified resources from prospective results, the claim-support judgments, the identity boundary, and all stopping consequences; do not rename contract-fixed headings or frontmatter fields.
    acceptance_test: >-
      The listed reader-facing lines can be read without knowledge of workflow-state vocabulary; each status retains its original evidential meaning in natural Chinese; required machine scaffolding remains unchanged; and a scan of ordinary prose and free-form labels finds no unexplained internal state token.
unresolved_issues:
  - LANG-R101-01
  - LANG-R101-02
  - LANG-R101-03
  - LANG-R101-04
---

# Language Assessment Report

**Assessment ID**: language-assessment-r101  
**Target Language**: Chinese  
**Discipline**: Cross-disciplinary critical-care medicine, clinical epidemiology, longitudinal statistics, system identification, and medical AI  
**Target Journal**: Not specified  
**Scope**: Complete Idea dossier, including all reader-facing prose, free-form table labels, and references; contract-fixed research-idea.v3 scaffolding was excluded from scoring  
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
| Academic Register & Tone | 7 | pass |
| Terminology Consistency | 4 | fail |
| Tense & Voice Conventions | 9 | pass |
| Conciseness & Redundancy | 6 | borderline |
| Readability & Flow | 5 | borderline |

---

## Hard Gate Status

**Overall**: fail

| Gate | Status | Detail |
|------|--------|--------|
| Grammar error density | pass | No pattern of clear grammatical errors approached the threshold of more than 3 per 500 words/lexical units in the complete dossier. |
| Academic register | pass | No section is dominated by colloquial or conversational register; mixed internal labels are localized terminology/register issues rather than pervasive informality. |
| Terminology coherence | fail | Three core RCT roles (projected endpoint, randomized-group contrast, and independent fallback endpoint) are inaccessible or inconsistently named at reader entry; core external-evaluation and gate labels add further instability. |
| Tense systematic violation | pass | Prospective actions, planned outputs, and conditional results are consistently distinguished from completed findings; no Methods/Results tense contradiction was found. |

---

## Strengths

- Prospective language is consistently maintained: planned analyses and outputs are not grammatically presented as completed findings.
- The prose repeatedly distinguishes prediction, association, randomization, and causal or mechanistic claims with appropriately bounded modal language.
- Most consequence statements name a condition and a concrete stopping, fallback, or interpretation consequence in the same local context.
- Dataset names, trial names, standard clinical abbreviations, mathematical symbols, and visit labels are generally stable once introduced.
- Tables and local paragraph sequencing make the dense protocol easier to navigate despite the terminology burden.

---

## Specific Issues

### Chinese Academic Clarity (if applicable)

- **LANG-R101-01 (major):** The reader-entry summary compresses three unfamiliar RCT roles into mixed or project-specific labels. This is the main barrier to understanding the conditional branch before the detailed methods.
- **LANG-R101-03 (minor):** Stage and negative-output labels should name their scientific referents rather than require readers to infer an internal gate vocabulary.
- **LANG-R101-04 (minor):** Internal English status labels in ordinary prose and free-form tables break the otherwise Chinese academic register.

### Grammar & Syntax

No actionable grammatical pattern was identified. Several long sentences are dense, but their clause relations remain grammatically recoverable; the reader-entry density is addressed under LANG-R101-01 without changing the one-sentence field contract.

### Academic Register & Tone

The overall register is formal and appropriately cautious. LANG-R101-04 is the only actionable register issue: workflow-state and project-management labels appear in reader-facing text.

### Terminology Consistency

| id | term_or_phrase | locator | reader_effect | action_in_frontmatter |
|---|---|---|---|---|
| LANG-R101-01 | 投影可观测状态摘要；随机化扰动；death-ranked SOFA | Lines 32, 41–42, 60, 67 and RCT-method/consequence passages | Core endpoint, contrast, and fallback roles are not identifiable at first use | yes |
| LANG-R101-02 | 零更新 / zero-update / zero update；proper score | External evaluation and success-criterion passages | Frozen evaluation, updating, and scoring operations blur across languages | yes |
| LANG-R101-03 | G1；假置信（门）；失败图 | Summary, gate, consequence, and planned-output passages | Project labels conceal the measured criterion or negative-result artifact | yes |

### Tense & Voice Conventions

No actionable issue. Future and conditional forms match a planned Idea dossier, while established evidence and existing resources are described in present or past forms as appropriate.

### Conciseness & Redundancy

No separate deletion finding is warranted. Repetition of causal boundaries and failure consequences often serves a distinct local function. The principal concision gain should come from replacing compact labels with direct definitions once and then using stable short forms, as specified in LANG-R101-01 to LANG-R101-03.

### Readability & Flow

Global section order is outside this assessment. Locally, the main readability cost is delayed decoding: reader-entry sentences present project labels whose referents become clear only much later. The executable repairs for LANG-R101-01 and LANG-R101-03 address that delay while preserving the fixed section and sentence contracts.

---

## Language Revision Priorities

1. **Core RCT endpoint and contrast language**: 1 major finding — define the projection endpoint, randomized-group contrast, and fallback endpoint directly at reader entry, then standardize all later forms.
2. **Validation and gate terminology**: 2 minor findings — establish one bilingual mapping for external evaluation/updating/scoring and expand project-specific stage or failure labels at first use.
3. **Reader-facing status language**: 1 minor finding — replace internal state labels in ordinary prose and free-form tables with natural Chinese evidence descriptions.

---

## Re-Assessment Status (if applicable)

Not applicable. This is a fresh baseline assessment of one frozen Idea dossier; no prior issue list, score, decision, revision delta, or earlier assessment was read.

| Check | Current assessment |
|--------|--------------------|
| Listed issues no longer present | Not applicable |
| Listed issues still present | Not applicable |
| New current-text issues | LANG-R101-01 to LANG-R101-04 |

---

## Assessment Notes

- The embedded reader handoff was taken from line 33: readers span critical care, clinical epidemiology, longitudinal statistics, system identification, medical AI, and translational research. The working prior-knowledge baseline assumes discipline-standard ICU/RCT/statistical terms but not project-specific labels imported from another listed field.
- The bounded read-only scanner was run in full and every candidate was disposed in sentence context, in the required order: reader-entry **13/13**, compact-reader-label **153/153**, mixed-language/version/internal-token **314/314**, and consequence-statement **127/127**. Compact-label candidates were treated as attention prompts, not a blacklist; standard names, defined abbreviations, direct descriptions, citations, versions, mathematical symbols, and fixed scaffolding were passed without findings.
- The reader-entry actor–operation–object–criterion pass covered the title, summary, audience, positioning, structured abstract, primary question, hypothesis, and non-hypotheses. No reader-entry role was closed merely because another phrase in the same sentence had already triggered a finding.
- The temporary role check covered the central scientific object, two primary tasks, hypothesis target quantities, primary task outcomes, external validation and update operations, negative/failure outputs, conditional RCT projection and fallback components, and the contribution. The central object, primary tasks, hypothesis quantities, and main observational outcomes were directly identifiable in context; the triggered RCT, validation/update, failure-output, and contribution/status language is represented in LANG-R101-01 to LANG-R101-04. No absent role was invented, and no complete term inventory was persisted.
- Focused terminology verification was limited to the triggered concepts: treatment-effect/outcome definition, external validation versus updating, and proper scoring rules. No broader literature, novelty, feasibility, or scientific-validity search was undertaken.
- All 480 dossier lines were read in four bounded segments (1–120, 121–240, 241–360, and 361–480). No local file read was truncated, so no truncation re-read was required. Two inaccessible web fetch attempts returned no substantive content and were not used or listed in `files_read`.
- Only language, terminology, and local readability were assessed. The dossier remained read-only, and no source edit was performed.
