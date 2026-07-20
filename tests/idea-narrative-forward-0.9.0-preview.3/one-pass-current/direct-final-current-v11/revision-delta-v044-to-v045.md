---
artifact_id: revision-delta-I01-001-v044-to-v045
workflow_id: RID-SEPSIS-CSM-20260717-001
idea_id: I01-001
version_id: v001
path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v11/revision-delta-v044-to-v045.md
source_artifact:
  artifact_id: idea-dossier-I01-001-v044
  version: v044
  path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v10/idea-dossier-v044.md
revised_artifact:
  artifact_id: idea-dossier-I01-001-v045
  version: v045
  path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v11/idea-dossier-v045.md
plugin_version: 0.9.0-preview.3
source_skill: multi-path-idea-generator
change_type: editorial_repair
scientific_change_declared: false
dossier_frozen: true
---

# Revision delta: idea dossier v044 to v045

## Scope and lineage

This delta records an editorial repair of the complete Idea dossier. The study
identity, scientific design, numerical and temporal rules, evidence status,
claim strength, working assumptions, limitations, contingencies, and stopping
consequences were not intentionally changed. No scientific change is declared.

The writer used only the following review instructions and protected-content
source in addition to the two dossier versions:

- `narrative-repair-plan-r075.yaml`;
- the YAML frontmatter of `language-assessment-r075.md`;
- `protected-content-register-v005.yaml`.

This is a writer-side change record, not an independent preservation or quality
verdict. It supplies explicit locators for a fresh preservation and editorial
review.

## Editorial changes at a glance

- Updated the logical dossier identity from v044 to v045, with `based_on`
  containing only the complete logical v044 reference and with plugin version
  `0.9.0-preview.3`.
- Rebuilt the title-to-contribution reader chain so the primary 24-month study
  precedes the conditional, trial-specific secondary analysis.
- Defined the central object and the anchor terminology at first use.
- Split stacked qualifications in the reader entry points and Methods while
  retaining their original scientific conditions and consequences.
- Replaced internal implementation labels with direct names for scientific
  objects, analysis procedures, research records, access controls, and version
  requirements.
- Consolidated the complete limitation and pending-specification families in
  section 14 while retaining only function-specific local boundaries elsewhere.
- Froze the complete revised dossier only after the repeated full-text scan and
  structural lint passed without an advisory.

## Narrative repair mapping

| Narrative finding and action | Actual v045 locator | Editorial operation performed | Scientific content retained |
|---|---|---|---|
| NAR-001 / NRP-001 | `Research question, objectives, and core hypothesis > Core hypothesis and non-hypotheses` | Added the functional definition: clinical anchors are audited physiological measurements that can be compared across databases and used to fix or interpret the scale and clinical meaning of patient states; “state anchor” names the scale-fixing role of those clinical anchors and not a second set of measurements. | Retained the prerequisite of adequate common variables, events, and transitions; advance specification of anchors, scale, state count, and lags; and the full hypothesis covering state occupancy, transition probability, anchor prediction, relationship direction and lag, simulation reconstruction, and final-hospital testing. No threshold or method detail was moved into the reader core. |
| NAR-002 / NRP-002 | `Background, current state, gap, significance, and rationale > Rationale`, second paragraph | Added a short bridge stating that trial visit analyses provide limited information specific to each trial after completion of the main study, are not a parallel primary contribution, and neither count toward nor repair the main success judgment. | Retained the requirement that the main study meet its prespecified standards first, the separate comparison of randomized groups within each trial, and the rule that later follow-up findings cannot replace cross-database evidence. Eligibility, mapping, missing-data, multiplicity, and stopping logic remain only in the complete Methods subsection. |

## Language finding mapping

| Finding | Actual v045 locator | Actual repair and disposition | Content and strength retained |
|---|---|---|---|
| LNG-R075-001 | H1 and section-1 Title; section-1 one-sentence summary; section 4 `Primary research question` and `Core hypothesis and non-hypotheses`; section 7 `Observation target...`, `Cross-database testing...`, and the conditional trial-analysis subsection | The title separates the main study from the subordinate trial analysis with a semicolon. The 227-character summary remains one sentence with one main study clause and one conditional layer. The primary question is now three ordered sentences. Method conditions, failure triggers, and trial-specific rules are expressed as separate paragraphs, lists, or subsections with explicit subjects. | Retained the 24-month main study; pre-onset, first onset, post-onset, and outcome scope; patient-time states and transitions; knowledge constraints and uncertainty; simulation reconstruction and cross-database testing; patient and hospital clustering; conditional separate trial analyses; and the non-causal interpretation boundary. |
| LNG-R075-002 | Section 7 conditional trial-analysis opening; section 8 implementation table; all five evidence chains; section 10 items 1, 3, 7, and 9; section 11 planned-output item 2 | Replaced opaque software and document labels with direct scientific or reproducibility functions. The final full-text scan found no occurrence of “组件、权威位置、引擎、注册表、流水线、诊断包、锁定包、分析包、发布包、执行器、只读、回写、接口压力” or bare “锁定”. | Retained label and time-rule versioning; one role per source field and its provenance; no model modification after development; isolated final-test access; no reuse of fitted results between trials; mandatory reporting of negative controls and failed criteria; and all input, output, permission, and version boundaries. |
| LNG-R075-003 | H1 and section-1 Title; section-1 one-sentence summary; later uses throughout sections 1–14 | The first ordinary prose occurrence defines “候选表征” as a set of literature- and expert-constrained longitudinal models and their state, transition, and observation relationships for patient-time states and transitions across the complete sepsis course. The title now attaches the course scope directly to patient states and transitions. | Retained candidate status, all four course phases, the separation of physiology, treatment actions, and measurement records, the simple models and at most one complex implementation, and both simulation and cross-database tests. |
| LNG-R075-004 | Structured abstract `Contribution and impact`; section 3 `Background`, `Significance`, and `Rationale`; section 12 `Positive planned contribution...` | Replaced abstract movement metaphors with direct statements of the evaluation dimensions, prevention of late-information leakage, planned deliverables, and cross-database comparisons. The only remaining use of “推进” is “按下列顺序推进” in the 24-month schedule, where it has the ordinary temporal meaning of proceeding through work and does not describe value, evidence, or promotion. | Retained joint evaluation of reconstructability, auditability, and cross-database stability; deliverables beyond a prediction tool; separation of event and information-availability times; and the planned status of all tests. |
| LNG-R075-005 | Section 14 free H3 immediately after `Feasibility and resources` | Replaced `Working assumptions（待确认规格）` with the Chinese heading `尚待确认的分析规格`. Contract-fixed English H2 headings and evidence-chain field labels were not changed. | Retained each pending specification, what is already fixed, its decision point and allowed information, and the consequence if unresolved. |
| LNG-R075-006 | Section 7 `Measurement consistency, calibration, and projection reconstruction error standards (R1)`, first criterion | Replaced the incomplete construction with `第一奇异轴所解释的 L_C Frobenius 能量占比至少为 50%`. | Retained the first singular axis, `L_C`, Frobenius energy, and the 50% threshold without altering the statistic. |
| LNG-R075-007 | Section 5 `24-month main study and date requirements`, introductory paragraph and month 13–20 row | Expanded `月 13–18/20` into an explicit schedule: evaluation starts in month 13, ordinarily completes in month 18, and the analysis specification and model record are finalized no later than month 20. The row also states the prohibition on changes based on final-test results after month 20. | Retained development-database, temporal, and hospital-held-out evaluation; the development finalization record; final-test access isolation; and the month-20 prohibition. |

### Internal-term replacements used in v045

| v044 expression | v045 reader-facing expression |
|---|---|
| 下游组件；完整方法权威位置 | 条件性试验访视次要分析；本小节集中说明其完整预设方法 |
| 标签与时间引擎 | 标签定义与时间处理程序 |
| 复杂度注册表 | 模型复杂度上限记录 |
| 变量角色注册表 | 字段用途、使用时点与来源记录 |
| 基线与候选模型流水线 | 基线与候选模型拟合程序及版本记录 |
| 临床锚定与状态对齐注册表 | 临床锚定与状态对齐记录 |
| 缺失与照护政策支持诊断包；接口压力 | 缺失与照护政策支持分析记录；整院接口缺失分析 |
| 医院分组与开发锁定包 | 医院分组、开发定稿与访问控制记录 |
| 试验访视分析包 | 试验访视分析规范与执行记录 |
| 阴性对照与未满足标准的发布包 | 阴性对照与未满足标准的结果记录 |
| 执行器、只读版本、只读模型 | 最终检验分析只使用已经定稿且不再修改的版本或模型 |
| 回写参数 | 不据试验结果重新估计或修改主体模型参数 |
| 开发包；验收包 | 带版本记录且不再修改的分析规范与模型记录；独立的分析核验材料 |

## Protected-content mapping

The following is a writer-side traceability map for every item in
`protected-content-register-v005.yaml`. It records where the protected meaning
is expressed; it does not replace an independent semantic preservation check.

| Protected item | Actual v045 locator or authority | Protected content retained in v045 | Writer-side disposition |
|---|---|---|---|
| PCR-001 | Frontmatter identity anchor; section 3 `Background` and `Significance`; section 4 `Primary research question`; section 14 limitation 11 | The object remains the sepsis-centered longitudinal ICU system spanning comparable at-risk non-onset periods, first onset, recovery, persistent deterioration or organ failure, ICU exit, and death. It is not reframed as generic prediction or generic ICU risk stratification. | Same identity and question are carried through the reader chain. |
| PCR-002 | Section-1 summary; section 3 `Significance`; section 4 `Objectives`; section 5 schedule | The main construction and testing are due within 24 months, use literature and expert constraints with public longitudinal ICU data and system identification, and target auditable scientific evidence, benchmark resources, and one or more high-level papers rather than only a prediction tool. | All three commitments remain separately locatable. |
| PCR-003 | Frontmatter `study_object` and `primary_unit_of_inference`; section 3 `Background`; section 4 `Primary research question`; section 7 `Observation target...` | The object remains longitudinal and sepsis-centered; the inferential unit remains the patient-time state and transition with patient and hospital clustering respected. | Object, scope, and unit are unchanged. |
| PCR-004 | Section 6 evidence-status table and public-data subsection; section 14 feasibility table and first operational risk | Inputs remain literature and expert knowledge, MIMIC-IV and eICU-CRD, with HiRID or AmsterdamUMCdb as a conditional backup. Database existence and versions are supported, while team access, data-use agreements, runnable extraction, project-level support, named personnel, and model results remain unverified or ungenerated. | Resource status is not upgraded. |
| PCR-005 | Section 6 evidence-status table and conditional trial-data subsection; section 14 feasibility table and limitation 7 | EXIT-SEP and XBJ-SCAP remain only potential individual-level sources for conditional post-main-study analyses. Local reports remain derived materials and do not replace authorization, original CRF/SAP review, randomization and center semantics, visit timing, or survival and hospital-status verification. | Trial data and semantic status remain conditional and unverified. |
| PCR-006 | Section 5 schedule and work packages; section 7 audit, observation target, simulation reconstruction, and evidence-insufficiency rules; section 8 analysis-record table | The ordered design, separation of physiology, treatment, and measurement records, at most one complex candidate, and interpretability restrictions are retained. The method authority retains alignment below 90% across 20 starts, bootstrap retention below 80%, cross-database direction consistency below 80%, state alignment below 0.70, or uncalibrated intervals as triggers for deletion, merging, or database/care-policy-specific description; prediction cannot override failure. | Design order, thresholds, and consequences remain in Methods. |
| PCR-007 | Section 5 conjunctive success definition; section 7 cross-database parameter-handling states; section 11 falsification and interpretation matrix; section 14 limitation 12 | Main-study support remains conjunctive across data support, simulation reconstruction, both primary tasks and calibration, leakage clearance, zero-update final testing, state alignment, and structural stability. Limited adaptation is reported separately and cannot repair zero-update failure; later trial work does not count toward main-study success. | Conjunctive logic and zero-update priority are retained. |
| PCR-008 | Section 7 `Two primary clinical tasks...` and `Mutually exclusive post-onset states and events` | The event/availability clocks, first-onset risk set, delayed entry, mutually exclusive states, competing termination, as-of features, proper scores and calibration, clustering, and leakage controls remain explicit. The specimen–antimicrobial 72-hour/24-hour pairing, baseline and rolling SOFA rules, first sortable onset, first-onset-only rule, admission weight of 1, within-window ordering, and exclusion of unorderable same-timestamp edges remain unchanged. | Full scientific task definitions remain at the method authority. |
| PCR-009 | Section 1 positioning; section 2 expected result; section 6 evidence status; section 12 planned contribution and closest-work comparison; section 13 claim-support table; section 14 limitations 1 and 9 | The dossier continues to describe planned construction and tests, not completed models or results. The defensible contribution remains conditional integration, validation, and benchmark/resource value; component precedents are acknowledged, the complete-combination gap remains low-to-moderate confidence, and no new-algorithm or global-first claim is made. | Claim scope and evidence strength are unchanged. |
| PCR-010 | Section 7 method authorities; section 11 falsification criteria and interpretation matrix; section 14 feasibility, pending specifications, limitations, and operational risks | Section 14 is the sole complete authority for resource/access, personnel, data support, label and leakage, recoverability, non-random missingness and overlap, zero-update validation, timing, trial semantics, mapping, and closest-work limitations. The two unresolved specification families remain the clinical-scale-to-simulation mapping and exact multicategory calibration estimator/interval/registration choice. Method branch logic remains in section 7; result-dependent interpretations remain in section 11. | Complete limitation and assumption families are retained once at their respective authorities. |
| PCR-011 | Title and summary; abstract approach; section 4 question and objective 4; section 5 WP5; section 6 trial-data status; section 7 complete trial-analysis method; section 8 trial analysis records; the single trial-specific entry in each of sections 9–11; section 12 subordinate contribution; one section-13 claim row; section 14 resource, pending-specification, limitation, and operational-risk functions | The 24-month main study is independent of the later trial analyses. Shared prerequisites remain main-study success, authorized individual data, and verifiable core trial semantics. Mapping analysis requires its additional R0/R1 conditions; if mapping fails but SOFA and core semantics are verifiable, the independent clinical-state analysis remains available; if core semantics fail, no new visit outcome is analyzed. Later results cannot repair any main-study failure. | The contingent component is projected once per distinct dossier function; its full eligibility, alternatives, stopping, and interpretation logic occurs only in section 7. |
| PCR-012 | Section 4 local non-hypothesis boundary; section 7 observation-target and trial-analysis interpretation boundaries; section 11 interpretation matrix; section 12 closest-work and claim audit; section 14 limitations 3, 7, and 8 | Observational associations and prediction do not establish treatment effects, causal networks, counterfactual policies, mechanisms, mediation, or control. Conditional trial analyses do not validate unmeasured dynamics, transitions, or the whole representation. The complete prohibition against presenting the plan as a validated model, clinical tool, drug platform, digital twin, controllable system, or unconditional implementation basis remains in section 14. | The complete unsupported-claim family remains in section 14; other occurrences are only the minimal boundary needed for the adjacent estimand, result interpretation, closest-work comparison, or claim audit. |

## Title-to-contribution reconciliation

| Reader function | Actual v045 locator | Reconciled content and hierarchy |
|---|---|---|
| Research title | H1 line 27 and section-1 Title field line 31 | Names patient states and transitions across the complete sepsis course, the planned simulation and cross-database tests, and the trial-specific analysis only after the main study succeeds. H1 and Title field match exactly. |
| Complete-Idea summary | Section-1 one-sentence summary, line 32 | Defines the candidate representation, states the 24-month construction and primary tests, names the auditable evidence and benchmark contribution, and uses one conditional layer for the subordinate trial analysis. |
| Primary question | Section 4 `Primary research question`, line 76 | States the main object and course coverage first, then reconstruction/cross-database testing with patient and hospital clustering, then a separately marked subordinate trial question. |
| Planned contribution | Section 12 `Positive planned contribution...`, line 490 | Matches the same object and tests, describes reconstructability, auditability, and cross-database stability as planned evaluation dimensions, and states that trial analyses are limited, trial-specific, and not parallel primary contributions. |
| Claim support | Section 13 | Contains one supported object claim and three conditionally supported positioning claims. Access, data support, and results remain pending; no claim is strengthened to a completed result. |

## Terminology, first-use, and synonym scan

### Central object

- The exact phrase `候选表征` occurs 37 times. Its first ordinary prose
  occurrence is the section-1 summary, where it is immediately defined.
- The full title phrase
  `脓毒症全病程患者状态及转移的候选动态系统表征` occurs in the H1, the
  Title field, and the first claim-support row.
- `复杂候选模型` is retained as a defined, distinct method object: at most one
  switching or nonlinear implementation beyond the simple baselines. It is not
  treated as a synonym for the complete candidate representation.
- `候选结构` refers only to the literature- and expert-constrained structural
  specification. It is not used as a second name for the complete representation.

### Anchors and contingent analyses

- The first occurrence of `临床锚点` and `状态锚点` is their joint functional
  definition in section 4. Later `生理测量锚点`, `共同临床锚点`, and `共同锚点`
  name qualified subsets or roles of those measurements and do not introduce a
  competing definition.
- `观测映射分析` and `独立临床状态分析` remain distinct, mutually exclusive
  analytical routes under their own eligibility conditions. Neither is a synonym
  for the complete candidate representation, and their technical labels do not
  appear in the title, summary, abstract, question, or contribution statement.
- The final reader-facing text contains no `阶段 I`, `阶段 II`, `阶段 III`,
  `下游`, or `分支` label.

### Whole-text vocabulary scan

- Zero occurrences: `组件`, `权威位置`, `引擎`, `注册表`, `流水线`, `诊断包`,
  `锁定包`, `分析包`, `发布包`, `执行器`, `只读`, `回写`, `接口压力`, and bare
  `锁定`.
- Zero occurrences: ambiguous `18/20`, bilingual free heading
  `Working assumptions`, abstract movement patterns such as `推进到`,
  `从……推进为`, `收缩为`, or `保护时间顺序`, and reader pointers to section 14.
- The single retained phrase `按下列顺序推进` occurs in the chronological
  schedule and has the standard scientific-project meaning of proceeding through
  ordered work; it is not a metaphor for increasing evidential value.
- Standard scientific names, abbreviations, formulas, database names, method
  names, contract-fixed English headings and evidence-chain fields, and reference
  titles remain unchanged where needed.

## Limitation and authority reconciliation

- `### 限制与边界条件` occurs once, inside section 14.
- `### 尚待确认的分析规格` occurs once, inside section 14.
- The clinical-scale-to-simulation mapping, exact multicategory calibration
  specification, closest-work search limitation, and complete prohibited-claim
  family each have one complete section-14 occurrence.
- Full eligibility and alternative logic for the conditional trial analyses occurs
  once in section 7. Result-dependent interpretations occur in section 11.
- Sections 1–13 contain no pointer to section 14. Local boundaries outside section
  14 remain only where omission would distort the immediately adjacent estimand,
  result interpretation, closest-work comparison, or claim-support judgment.

## Lint and structural reconciliation

- Pre-freeze structural lint: `OK`; no advisory was emitted.
- After the final terminology repair, the full scan and structural lint were
  repeated: `OK`; no advisory was emitted.
- Frozen-state structural lint: `OK`; no advisory was emitted.
- Advisory disposition: there were no remaining linter advisories to retain or
  repair. The broader manual candidate scan is documented above; the one retained
  use of `推进` was reviewed in context and retained for its ordinary chronological
  meaning.
- Structure: 1 H1, 15 required H2 sections, 36 H3 headings, and 8 H4 headings.
  Section 3 contains exactly `Background`, `Current state`, `Gap`, `Significance`,
  and `Rationale` in that order.
- Evidence chains: 5. Each contains exactly one Input, Method/analysis/processing,
  Output, and Supports field.
- The complete-Idea summary contains 227 characters, one full stop, and one
  semicolon; it remains one sentence.
- The claim-support table contains one supported object claim and three
  conditionally supported positioning claims.
- The dossier body retains the complete set of numerical literals from v044. The
  only removed numeric literal outside the body was `03` in the superseded v003
  lineage path, because v045 is based only on logical v044.
- Final dossier metadata: plugin version `0.9.0-preview.3`; `based_on` contains only
  logical v044; change type `editorial_repair`; `frozen: true`.

