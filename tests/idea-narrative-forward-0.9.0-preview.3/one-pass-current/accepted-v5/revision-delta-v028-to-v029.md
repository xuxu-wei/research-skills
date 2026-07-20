---
schema_version: research-idea-revision-delta.v1
plugin_version: 0.9.0-preview.3
artifact_id: revision-delta-I01-001-v028-to-v029
workflow_id: RID-SEPSIS-CSM-20260717-001
idea_id: I01-001
version_id: v029
path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/accepted-v5/revision-delta-v028-to-v029.md
based_on:
  - artifact_id: idea-dossier-I01-001-v028
    version: v028
    path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/accepted-v4/idea-dossier-v028.md
target_artifact:
  artifact_id: idea-dossier-I01-001-v029
  version: v029
  path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/accepted-v5/idea-dossier-v029.md
source_skill: multi-path-idea-generator
created_round: 29
change_type: editorial_repair_delta
scientific_change: false
frozen: true
---

# Revision delta: idea dossier v028 to v029

## Scope and lineage

This editorial repair is based only on the logical reference to `idea-dossier-I01-001-v028`. It preserves the research identity, scientific design, numerical and temporal rules, evidence state, claim strength, assumptions, limitations, alternatives, and stop conditions. The complete revised Idea is `idea-dossier-I01-001-v029`; this delta is not a substitute for it and does not declare editorial readiness.

## Narrative repair mapping

### NRP-001

- **Revised locator:** `Title, summary, audience, and positioning > One-sentence complete-Idea summary`.
- **Actual-text acceptance evidence:** The summary first states the 24-month objective, literature and expert knowledge, two public ICU databases subject to access and observability audit, and the full pre-onset–onset–post-onset–outcome scope. It then directly names external prediction/calibration, patient-state agreement, and structural-sign stability. A second clause defines the five requirements for “阶段 II 达标” and makes trial-specific RCT analysis conditional on actual visits and original semantics.
- **Preservation evidence:** The summary retains the 24-month route; literature/expert knowledge; both audited public databases; the complete disease-course scope; independent hospital/database testing; and conditional, separate RCT analyses. It removes the repeated full negative boundary from the summary without changing that boundary in its authoritative and method-specific locations.

### NRP-002

- **Revised locator:** `Structured abstract`, all five labeled entries.
- **Actual-text acceptance evidence:** `Background and gap` states the Sepsis-3/information-time problem and the untested evidence relation; `Objective and hypothesis` states the 24-month goal and testable stability hypothesis; `Approach` states the two main tasks, audit-determined complexity, simple-model sequence, hospital split, and three separately reported external analyses; `Expected result` states planned artifacts and the conditional mapped/independent trial outcomes; `Contribution and impact` states the distinction between single-database prediction and cross-database state evidence, reproducibility value, continue/stop judgment value, and reusable non-attainment records and benchmark resources.
- **Preservation evidence:** The abstract keeps the label boundary, two main tasks, audit-controlled complexity, simple-model-first sequence, isolated external testing, prospective status of every output, conditional trial-specific RCT scope, and reusable failure/benchmark resources. The RCT non-substitution boundary is not repeated in `Contribution and impact`.

### NRP-003

- **Revised locator:** `Research question, objectives, and core hypothesis > Primary research question`; fallback retained at `Objectives > objective 4` and `Research design and methods > Trial-specific mapping to observed visits and independent clinical-state analysis > Independent clinical-state analysis`.
- **Actual-text acceptance evidence:** The primary question is now one general question followed by three independent subquestions covering full-course representation, cross-hospital/database stability, and the conditional RCT mapped summary. It contains no “否则” branch. Objective 4 and the method subsection still specify the independent death–SOFA ordered clinical-state endpoint when mapping requirements are insufficient.
- **Preservation evidence:** The study object, patient–time inference boundary, observational/randomized evidence distinction, full-course coverage, cross-database stability, and conditional RCT relation remain explicit.

## Language finding mapping

### LANG-R041-01

- **Revised locators:** `Title, summary, audience, and positioning > One-sentence complete-Idea summary`; later uses in `Structured abstract`, `Research question, objectives, and core hypothesis`, `Research content and work packages`, methods, outputs, contribution, and section 14.
- **Actual-text acceptance evidence:** At first use, the summary defines “阶段 II 达标” as simultaneous attainment of dual-database support, simulation recovery testing, two main tasks, leakage checks, and no-parameter-update cross-database external validation. Later reader-facing uses consistently say “阶段 II 达标”, “阶段 II 达标判定”, or “阶段 II 达标后冻结的模型”, so each occurrence names either the decision or the frozen model resulting from it.
- **Content preserved:** Five scientific decision classes, the 24-month boundary, trial-specific conditional initiation, and the rule that RCT results cannot fill a missing class.

### LANG-R041-02

- **Revised locators:** first definition in the one-sentence summary; `Rationale`; `Objectives > objective 3`; `Simulation and semi-synthetic recovery tests`; evidence, output, contribution, assumption, and falsification passages.
- **Actual-text acceptance evidence:** First use states “在模拟和半合成数据中按预设绝对阈值检验状态、转移、结构和概率的恢复能力” before introducing “模拟恢复检验”. The technical subsection retains correct, zero-edge, overfitting, omitted-state, and misspecified generators and every state, transition, edge, coverage, false-confidence, and probability-calibration standard. Isolated “绝对恢复” and “绝对模拟恢复” are removed.
- **Content preserved:** All generator scenarios, quantities, thresholds, separate structural/calibration decisions, and the consequence of not interpreting quantities that fail their standards.

### LANG-R041-03

- **Revised locators:** `Positioning and contribution frame`; `Structured abstract`; `Core hypothesis`; work-package outputs; `Evidence chains`; `Required analyses and evidence`; `Planned outputs`; `Contribution and evidence progression`; `Title and positioning claim-support table`.
- **Actual-text acceptance evidence:** Reader prose now says “五类证据同时满足”, “两项主要任务的预测与校准表现”, “未达标结果及其图表”, “不作相应结构解释”, and “三种外部分析方式”. The contribution paragraph directly names its three scientific operations rather than using input/transform/output layers. Contract-required `Evidence chain:` headings remain structural headings only.
- **Content preserved:** Simultaneous five-class requirement, separate judgment of linked research parts, separate reporting of three external analyses, and narrower interpretation after non-attainment.

### LANG-R041-04

- **Revised locators:** H1 title and exact `Title` field.
- **Actual-text acceptance evidence:** “脓毒症全病程 ICU 患者系统的候选动态表征” makes “候选” and “动态” modify “表征”; “RCT 稀疏访视数据” makes “稀疏” modify visit data; “满足预设条件后” modifies only the RCT secondary analysis.
- **Content preserved:** Full sepsis course, ICU patient system, candidate rather than validated status, planned cross-database validation, sparse RCT visits, secondary analysis, and prespecified prerequisites.

### LANG-R041-05

- **Revised locators:** `Public ICU database roles and observability audit`; primary-task protocol; `Local RCT evidence`; `Observational target, anchoring and abstention`; trial analysis table; `Key techniques and implementation`; `Working assumptions`; `Limitations and boundary conditions`.
- **Actual-text acceptance evidence:** Reader prose uses “本研究方案”, “ICU 入住记录”, first defines “自助法（bootstrap）” then uses “自助法”, first defines “模式混合敏感性分析的偏移参数 δ（pattern-mixture delta）” then uses “偏移参数 δ”, and replaces `sepsis-like` with “符合操作性类脓毒症标准的人群”. Database and trial names, RCT, SOFA, CRF, SAP, WBC, CRP, and mathematical symbols remain unchanged.
- **Content preserved:** Method identity, analysis-set definitions, named sources, standard abbreviations, and every numerical value.

### LANG-R041-06

- **Revised locators:** one-sentence summary; `Primary research question`; `Core hypothesis`; `Working assumptions` items 1–2.
- **Actual-text acceptance evidence:** The summary has two semicolon-separated main lines. The research question uses one general question and three subquestions. The hypothesis is split into prerequisite, testable hypothesis, and separately judged secondary outputs. Each working assumption separately states what is fixed, what remains to be registered, when and from what information it may be registered, and the consequence of non-registration.
- **Content preserved:** All prerequisites, three scientific questions, the five jointly required evidence classes, both secondary diagnostics, RCT non-substitution, and both assumption decision times.

### LANG-R041-07

- **Revised locators:** `Structured abstract > Background and gap`; `Current state`; trial analysis table; section 14 risk row for inconsistent or imprecise trial results.
- **Actual-text acceptance evidence:** The abstract says “现有有界检索尚未发现”; Current state says the databases differ in centers, eras, sampling, and interfaces; the trial table says “目标分析集为全部 1,817/710 名随机化受试者” and “不视为未受干预影响的基线”; the risk trigger says the uncertainty interval remains compatible with no between-group difference.
- **Content preserved:** Bounded-search status, database heterogeneity, full randomized analysis-set priority, post-randomization measurement boundary, and non-affirmative interpretation under uncertainty.

### LANG-R041-08

- **Revised locators:** one-sentence summary and positioning; `Rationale`; `Objectives > objective 1`; month 4–6 programme row; WP1; primary-task protocol; first evidence chain; required analyses and planned outputs.
- **Actual-text acceptance evidence:** First explanatory use names event occurrence time and information availability time. Later joint references use “双时刻设计”; references to the second time alone use “标签信息可用时刻”. “全病程时钟”, “双时钟”, and “标签可用性时钟” are removed.
- **Content preserved:** Separate recording of event and availability, prohibition on backfilling later-entered information, and feature queries restricted to information available before prediction.

## Protected-content mapping and element-level preservation

### PCR-001

- **Revised locators:** complete `Research question, objectives, and core hypothesis`; stage criteria; trial mapping methods.
- **Actual-text evidence:** The study object includes comparable at-risk non-onset and post-onset trajectories; the unit is clustered patient–time state and transition; the three subquestions retain full-course coverage, external state/structure stability, and conditional RCT summaries; objectives retain audit support, prespecified state/scale/anchor/lag, simulation recovery testing, and the independent clinical-state fallback; the hypothesis keeps randomized and observational evidence separate.
- **Disposition:** retained_same_meaning.

### PCR-002

- **Revised locators:** complete `Title, summary, audience, and positioning`; `Structured abstract`.
- **Actual-text evidence:** The dossier remains an evidence-integration, planned cross-database validation, reusable benchmark/resource, and falsifiable-design study rather than ordinary prediction. It names literature/expert knowledge, two audited public ICU databases, conditional trial data, an isolated final test, separate RCT analyses, and the integration of dual times, state/action/measurement separation, recovery testing, external validation, and conditional RCT work.
- **Disposition:** retained_same_meaning.

### PCR-003

- **Revised locator:** `Data, materials, and existing evidence base > Current resource and evidence status`.
- **Actual-text evidence:** The table retains verified database existence/version but unverified access, agreements, extraction, storage, exact project counts, RCT authorization/semantics, anchor qualification, named personnel, and all not-yet-generated analyses. It retains the 2026-07-17 bounded-search confidence levels.
- **Disposition:** retained_same_strength.

### PCR-004

- **Revised locator:** `Data, materials, and existing evidence base > Local RCT evidence`.
- **Actual-text evidence:** EXIT-SEP retains 1,817 randomized, 1,760 known 28-day status, 395 deaths, 57 unknown, SOFA 1,750/1,542/1,296, lactate 855 to 223, and unresolved D1/D7 timing. XBJ-SCAP retains 710, 675, 617, 671, 658; SOFA 703/628/610, WBC 704/634/614, CRP 579/503/467, 675 known status; unresolved D0/D8 timing; SCAP/Sepsis-3 distinction; unavailable variables; and unresolved D-dimer units.
- **Disposition:** retained_same_strength.

### PCR-005

- **Revised locators:** `Twenty-four-month programme`; `Work packages`; minimum analysis order.
- **Actual-text evidence:** The five time windows and their exact work remain: resources/backup at months 0–3; audits and fixed design at 4–6; simple baselines, Monte Carlo/semi-synthetic recovery and at most one complex candidate at 7–12; internal/temporal/hospital evaluation and frozen package at 13–18/20; no-update final test followed by recalibration and observation-model-only update at 21–24. The minimum order is unchanged except for direct terminology.
- **Disposition:** retained_same_meaning.

### PCR-006

- **Revised locator:** `Public ICU database roles and observability audit`, complete subsection and table.
- **Actual-text evidence:** MIMIC development, eICU hospital-split external role, audited backup, first eligible ICU record, first linked admission, ≥20 external hospitals, 20/10 event and transition support, terminal-state handling, 12-hour or prespecified alternative timing, two anchors per dimension, 30% measured grids, 70% hospitals/80% patients, missingness indicators, K≤4, ≤3 state patterns, and limited forward-fill exceptions all remain.
- **Disposition:** retained_same_meaning.

### PCR-007

- **Revised locator:** `Prespecified variable roles`, complete table.
- **Actual-text evidence:** Y_t, A_t, M_t, B and label-only roles retain all measurements/actions/processes, duplicate separation, time availability, unknown coding, prohibition on using treatment as physiological anchors, and common-layer audit requirements.
- **Disposition:** retained_same_meaning.

### PCR-008

- **Revised locator:** `Protocol specifications for the two primary clinical tasks`, complete table.
- **Actual-text evidence:** Adult/first-stay/history criteria; infection-pair windows 72/24 hours; SOFA baselines and −48/+24 window; non-backfilled availability; 12-hour landmarks/history/horizon; first onset, delayed entry, total stay weight, competing events, within-bin order, day-7 endpoint, Brier/calibration metrics, and patient/hospital clustered uncertainty remain with every number unchanged.
- **Disposition:** retained_same_meaning.

### PCR-009

- **Revised locator:** paragraph immediately after the primary-task protocol table.
- **Actual-text evidence:** Exactly two sensitivity labels remain (symmetric ±24-hour pairing; infection-preceding 24-hour minimum SOFA with ±24-hour organ window), cannot replace the main result, and the full leakage checklist remains, including future information/treatment/measurement, split-crossing imputation, repeated admissions, patient or ICU-record crossing, overlap weights, and outcome-driven design choices.
- **Disposition:** retained_same_meaning.

### PCR-010

- **Revised locator:** `Mutually exclusive post-onset state and event system`, complete subsection.
- **Actual-text evidence:** The six-state priority, 12-hour assignment, event-time sensitivity, persistent sepsis, recovery definition and availability, worsening definition, action/physiology separation, discharge not equated with recovery, transfer handling, and death priority remain.
- **Disposition:** retained_same_meaning.

### PCR-011

- **Revised locator:** `Observational target, anchoring and abstention`, complete subsection.
- **Actual-text evidence:** The joint predictive/generative target, noncausal A_t interpretation, two anchors per dimension, +1 first loading, sparse loading, K≤4, state patterns≤3, lag 1/2, no same-grid cycles, 20-seed alignment, MAR/selection baseline, δ values −1/−0.5/0/+0.5/+1, overlap/effective-sample thresholds, and 90%/80%/80%/0.70 interpretation thresholds remain.
- **Disposition:** retained_same_meaning.

### PCR-012

- **Revised locator:** `Simulation and semi-synthetic recovery tests`, complete subsection and table.
- **Actual-text evidence:** Months 7–10, ≥1,000 repetitions or Monte Carlo SE≤0.02, all generator dimensions, ARI/canonical correlation≥0.80, 20-seed alignment≥90%, transition MAE≤0.05, coverage 0.90–0.98, sign/lag≥0.80, sensitivity≥0.80, FDR≤0.10, zero-edge false exclusion≤0.05, misspecification response≥80%, false high confidence≤0.05, slope 0.80–1.20, and probability bias≤0.02 remain. Separate structural and probability judgment remains.
- **Disposition:** retained_same_meaning.

### PCR-013

- **Revised locator:** `Hospital-based cross-database validation`, complete subsection.
- **Actual-text evidence:** Pre-outcome stratified hospital split with seed 20260717 and 30/70 roles, hospital priority, linked cross-partition exclusion, first eligible record, pre-performance exclusion reporting, test-priority connected-component sensitivity, independent custodian support check, frozen package, and separately reported no-update/recalibration/observation-only update remain; full refit remains outside external validation.
- **Disposition:** retained_same_meaning.

### PCR-014

- **Revised locators:** trial semantics/common-anchor paragraph and prespecified mapping paragraph.
- **Actual-text evidence:** Both endpoints remain post-result secondary exploratory analyses; 28-day replication and trials remain separate; authorization, CRF/SAP/dictionary, randomization, analysis set, center/strata, D7/D8 relative timing, and outcome semantics must be verified. Anchor eligibility/exclusions, ≥2 anchors, WBC/CRP candidate status, D-dimer exclusion, fixed MIMIC scaling/truncation, SVD formulas, tie/sign rules, and prohibition on RCT group/outcome/cross-trial fitting remain.
- **Disposition:** retained_same_meaning.

### PCR-015

- **Revised locators:** agreement/error, mapped-estimand, and independent-clinical-state paragraphs.
- **Actual-text evidence:** The eICU D7/D8 evaluation retains ≥50% Frobenius energy, correlation≥0.70, normalized MAE≤0.50, |α|≤0.20 SD, β 0.80–1.20, coverage 0.90–0.98, anchor calibration limits, ≥80% plausible anchors and ≥60% calculable visits. Death/resident/discharge ordering, center-compatible probability comparison, SOFA fallback, and no-new-endpoint stop remain.
- **Disposition:** retained_same_meaning.

### PCR-016

- **Revised locators:** trial analysis table and final sparse-visit paragraph.
- **Actual-text evidence:** EXIT target 1,817 and 1,760 complete-outcome subset; XBJ target 710, fallback 675 modified intention-to-treat, 617/671/658 sensitivity sets; actual D7/D8 and post-randomization D1/D0 baseline restrictions; death/discharge ranks; multiple-imputation inputs and Rubin/clustered self-resampling; δ and tipping-point analyses; transfer bounds; structural-missingness/D-dimer rules; Holm 0.05 family; exploratory FDR; interaction-only subgroups; and no pseudo-continuous interpolation remain.
- **Disposition:** retained_same_meaning.

### PCR-017

- **Revised locator:** `Prespecified criteria for completing the 24-month validation stage`, complete subsection.
- **Actual-text evidence:** The five jointly required classes retain dual-database support, all recovery criteria or simpler naming, main-task Brier upper 95% bound≤+0.01 plus calibration 0.80–1.20 and risk error≤0.02, availability/split/leakage rules, ≥20 final-test hospitals, no-update Brier noninferiority, state agreement≥0.70, structural sign agreement≥0.80, separate adaptation results, month-6 registration, and tighten-only hard standards.
- **Disposition:** retained_same_strength.

### PCR-018

- **Revised locators:** `Planned outputs`; `Contribution and evidence progression`; current-resource table.
- **Actual-text evidence:** Every artifact remains prospective. Planned products include dual-time labels/12-hour risk sets, states, variable/interface/missingness/split records, simple baselines, recovery and false-confidence control, at most one supported complex candidate or simpler model, main tasks/diagnostics across development and external settings, calibration/uncertainty/alignment/figures, and conditional separate RCT outputs. The text retains not-yet-generated status, cross-database stability as the minimum endpoint, bounded randomized inference, high-confidence module precedents, and low-to-moderate-confidence combination gap.
- **Disposition:** retained_same_strength.

### PCR-019

- **Revised locator:** section 14 `Working assumptions`, complete subsection.
- **Actual-text evidence:** Item 1 retains every required simulation scenario, month-7 registration by the three leads, allowed information, and invalid recovery conclusion if unresolved. Item 2 retains pending multiclass estimators/limits/refined thresholds, fixed multiclass Brier/favorable-state calibration/cluster uncertainty, tighten-only hard standards, pre-final-result registration sources, exclusion from the success decision if unregistered, and the effective-sample/simulation-stability requirement.
- **Disposition:** retained_once_at_authority_location.

### PCR-020

- **Revised locator:** section 14 `Limitations and boundary conditions`, items 1–5.
- **Actual-text evidence:** These items retain access/resource uncertainty; all label/time leakage sources; latent-state noninterpretability and the full anchor/recovery/alignment/resampling/external/calibration requirements; missingness and treatment-support limits; negative-control limit; and the exclusive evidentiary role of no-update external testing versus adaptation/redevelopment.
- **Disposition:** retained_once_at_authority_location.

### PCR-021

- **Revised locator:** section 14 `Limitations and boundary conditions`, items 6–9.
- **Actual-text evidence:** These items retain potential-only RCT status and all semantic/authorization gaps; trial separation, sparse-visit scope, inconsistent/imprecise-result interpretation, and no post hoc subgroup rescue; non-systematic-search scope and omitted sources; all unsupported causal/mechanistic/control/digital-twin claims; bounded RCT inference; and non-clinical-tool status.
- **Disposition:** retained_once_at_authority_location.

### PCR-022

- **Revised locator:** section 14 `Risks, alternatives, and stop conditions`, rows from public-data access through timeline.
- **Actual-text evidence:** The rows retain every month-3, month-6, cross-partition support, month-20 leakage, month-12 recovery, missingness/overlap, no-update validation, month-20 package, and month-24 result trigger; each backup, simplification, sensitivity, reporting alternative, and stop/bounded conclusion remains with all numerical thresholds.
- **Disposition:** retained_once_at_authority_location.

### PCR-023

- **Revised locator:** section 14 risk rows for RCT authorization/mapping, inconsistent trial results, and literature positioning.
- **Actual-text evidence:** The rows retain authorization/semantic/<2-anchor/agreement-error triggers; conditional independent death–SOFA endpoint; original-endpoint/audit fallback and endpoint stop; separate no-support/limited-applicability reporting without pooling or post hoc subgroup changes; and the additional systematic/citation/patent/non-English evidence required for first/new/nonexistence claims.
- **Disposition:** retained_once_at_authority_location.

### PCR-024

- **Revised locators:** section 14 `Limitations and boundary conditions`, items 7–9; bounded-search claim-support row.
- **Actual-text evidence:** The dossier still rejects causal networks/effects, counterfactual strategy, mechanism, mediation, control, digital twins, RCT validation of latent dynamics/edges/the whole system, pseudo-continuous trajectories, relabeling adaptation as no-update success, completed-model/tool/platform/deployment claims, systematic-review/global-nonexistence/new-algorithm/global-first claims, and any stronger than low-to-moderate confidence for the combination gap.
- **Disposition:** retained_same_boundary.

### PCR-025

- **Revised locator:** `Falsification criteria and result interpretation`, complete table.
- **Actual-text evidence:** The table retains all eight result-to-interpretation mappings: temporal leakage; insufficient dual-database support; failed recovery; missingness/overlap sensitivity; failed no-update external testing; failed trial mapping; unauditable trial semantics; and support only when all five stage criteria pass. The final supported state remains a candidate audited/recovered/task-evaluated/externally validated representation, not a causal mechanism or clinical tool.
- **Disposition:** retained_same_strength.

## Mechanical checks recorded for handoff

- The H1 and `Title` field are identical.
- The dossier contains the 15 required H2 sections in order and the five required section-3 H3 functions in order.
- `based_on` contains only the logical reference to v028; the dossier uses `editorial_repair` and this delta uses `editorial_repair_delta`.
- Section 14 remains the only complete authority for limitations, assumptions, contingencies, alternatives, and stop conditions; no reader-facing pointer to that section was added.
- The writer re-opened every revised locator listed above and compared the actual dossier text with each protected element before handoff; headings or this delta alone were not treated as evidence.
