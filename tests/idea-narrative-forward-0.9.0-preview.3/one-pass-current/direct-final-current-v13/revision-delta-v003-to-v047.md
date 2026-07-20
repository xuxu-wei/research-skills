---
schema_version: research-idea-revision-delta.v1
plugin_version: 0.9.0-preview.3
artifact_id: revision-delta-I01-001-v003-to-v047
workflow_id: RID-SEPSIS-CSM-20260717-001
idea_id: I01-001
version_id: v003-to-v047
path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v13/revision-delta-v003-to-v047.md
change_type: editorial_repair_delta
source_artifact:
  artifact_id: idea-dossier-I01-001-v003
  version: v003
  path: tests/idea-test-0.9.0-preview.1/0.9.0-preview.1/03_ideas/nodes/I01-001/dossiers/idea-dossier-v003.md
revised_artifact:
  artifact_id: idea-dossier-I01-001-v047
  version: v047
  path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v13/idea-dossier-v047.md
based_on:
  - artifact_id: idea-dossier-I01-001-v003
    version: v003
    path: tests/idea-test-0.9.0-preview.1/0.9.0-preview.1/03_ideas/nodes/I01-001/dossiers/idea-dossier-v003.md
  - artifact_id: editorial-repair-writer-brief-I01-001-r086
    version: r086
    path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/baseline-current/editorial-repair-writer-brief-r086.yaml
  - artifact_id: protected-content-register-I01-001-v004-r004
    version: r004
    path: tests/idea-narrative-forward-0.9.0-preview.3/run-001/inputs/protected-content-register-v004.yaml
source_skill: multi-path-idea-generator
created_round: 86
dossier_frozen_before_delta: true
frozen: true
---

# Revision delta: idea dossier v003 to v047

## Scope and ordering

This was an editorial-only repair of one complete dossier. The research identity, scientific design, numerical and temporal rules, evidence states, claim strength, contingencies, and stop conditions were retained. The complete v047 dossier was written, scanned as a whole, passed deterministic lint without an advisory, and was frozen before this delta was created; no dossier edit followed delta creation.

## Included repair-item mapping

| Repair item | Source and finding IDs | Operation | Revised locator | Acceptance evidence in frozen v047 |
|---|---|---|---|---|
| NRP-001 | source: NRP-001, NAR-001; finding: NAR-001 | split | `Background, current state, gap, significance, and rationale` | The H2 now contains, in order, the five non-empty H3s `Background`, `Current state`, `Gap`, `Significance`, and `Rationale`. The gap asks whether the full-course candidate representation is recoverable and transportable rather than treating module combination as novelty; significance states the scientific consequences of timing, measurement-policy, and transport errors; rationale connects dual clocks, separation of patient state/treatment/measurement, absolute recovery, and cross-database testing without carrying a limitation inventory or a section-14 pointer. |
| NRP-002 | source: NRP-002, NAR-002, NAR-003; findings: NAR-002, NAR-003 | replace | H1; `Title, summary, audience, and positioning` > `Title` and `One-sentence complete-Idea summary` | H1 and Title are identical—`脓毒症全病程候选动态系统表征：计划跨数据库检验`—and contain only the 24-month primary study. The summary has one field, one sentence, one full stop, and a visible sequence of study object → two primary outcomes and overall tests → evidence-integration/validation/benchmark/resource contribution → one subordinate purpose-level statement about separately analysing randomized trials with sparse visit data; it contains no trial name, visit day, branch label, ranking, eligibility tree, or grouped prohibited-claim list. |
| NRP-003 | source: NRP-003, NAR-003; finding: NAR-003 | consolidate | `Research design and methods` > `主体研究完成后的两项随机对照试验次要分析` | The subsection is continuous and ordered as `共同前提` → `观测映射成立时的分析` → `观测映射不成立时的独立分析` → `试验语义不足时的停止`. It contains the separate EXIT-SEP D7 and XBJ-SCAP D8 semantics, common-anchor eligibility, fixed SVD mapping, every absolute fidelity criterion, death/discharge ranking, randomized comparison, missing-data and centre handling, the independent endpoint and analysis, multiplicity, non-pooling rule, and the stop condition. Shared prerequisites do not include conditions that apply only to the observation-mapping analysis. |
| NRP-004 | source: NRP-004, NAR-004; finding: NAR-004 | consolidate | `Feasibility, resources, risks, alternatives, and stop conditions` > `Working assumptions`, `Limitations and boundary conditions`, `Claims not supported by the current design`, and `Operational risks, responses, and consequences`; method decisions in section 7; falsification and result-dependent interpretation in section 11 | Section 14 is the only complete inventory of resource/access, team, G1, label/leakage, recoverability, MNAR/overlap, external-test, time, trial-data/semantics, observation-mapping, closest-work, and claim boundaries. Its two working-assumption rows each state the pending choice, fixed content, decision point and allowed information, and unresolved consequence. Section 7 retains scientific eligibility, alternatives, and method-specific consequences; section 11 retains falsification and result-dependent interpretation. All five evidence chains have only Input, Method/analysis/processing, Output, and Supports fields. A whole-body scan found no section-14 pointer and no second complete limitation or prohibited-claim list. |
| NRP-005 | source: NRP-005, NAR-005; finding: NAR-005 | replace | `Key techniques and implementation` > numbered items 1–10 | Each item now names its inputs, computation or transformation, output record, verification use, and dependency. The ten items cover clocks, G1 data support, variables and units, cohorts and states, baseline/candidate-model inputs and outputs, anchor alignment, simulation, hospital partitioning, the trial interface, and uncertainty/negative checks. No item uses a tool metaphor, repeats the full method rationale or limitation inventory, or points to section 14. |
| LANG-R085-001 | source/finding: LANG-R085-001 | define | First use: `Research content and work packages` > `Twenty-four-month minimum and dated decisions`; later G1 occurrences throughout sections 5–14 | First use reads `双库可观测性与数据支持审计（G1 审计）` and immediately enumerates access, events/transitions, hospitals, timestamps, common physiological anchors, interfaces, and missingness, plus the decisions controlled by the audit. Every later occurrence is `G1 审计`; minimum standards, observations, and consequences are stated separately, with no bare G1 or replacement shorthand. |
| LANG-R085-002 | source/finding: LANG-R085-002 | consolidate | First use: `Structured abstract` > `Approach`; method authority: `Hospital-primary cross-database validation`; result interpretation in section 11 | First use defines `不使用外部测试数据更新任何模型参数的外部检验（零更新外部检验）` after stating that labels, preprocessing, model, parameters, thresholds, and evaluation code are fixed and the untouched final test data are evaluated without adjustment. Every subsequent occurrence uses `零更新外部检验`; re-calibration, observation-layer update, and complete refitting remain separately named. Whole-body scan found no English or bare alternative. |
| LANG-R085-003 | source/finding: LANG-R085-003 | replace | `Research design and methods` > `观测映射不成立时的独立分析`; later function-specific uses in sections 8 and 11 | First use defines `独立次要临床状态端点` as death worst, visit-time survivors still in hospital ordered from high to low SOFA, and alive discharge before the visit best. The same sentence defines `试验特异独立次要临床状态再分析` as separate trial analyses that do not use the stage-II projection summary. Later occurrences use those names only. Whole-body scan found no `death-ranked`, `独立 SOFA`, or other compressed fallback name. |
| LANG-R085-004 | source/finding: LANG-R085-004 | replace | `Title, summary, audience, and positioning` > `One-sentence complete-Idea summary` | The subject and main action occur before the condition; the sentence presents the longitudinal study object, 24-month candidate-representation work and two primary outcomes, absolute simulation and untouched external testing, positive planned contribution, and the subordinate later purpose in parallel clauses. It contains one semicolon for the final subordinate clause and one full stop ending the single sentence. |
| LANG-R085-005 | source/finding: LANG-R085-005 | replace | Whole dossier, especially sections 3, 5, 7, 8, 10, and 11 | Ambiguous action metaphors were replaced with direct trigger–object–action/consequence wording: e.g., final-test results are not accessed before leakage review is satisfied; variables are separated by scientific use; external results are evaluated under three explicit update levels; and failure modes are visualized or recorded. A body-only scan found no `防火墙`, `封印`, `打开`, `挽救`, `救回`, `豁免`, internal review/revision vocabulary, or version-history prose. |
| LANG-R085-006 | source/finding: LANG-R085-006 | replace | H1/Title; summary; `Research design and methods` > `主体研究完成后的两项随机对照试验次要分析` | The title omits all later trial work. The summary says only that, after the primary study and corresponding trial data/semantics meet requirements, the study will separately conduct secondary analyses of randomized controlled trials with sparse visit data. At method first use, the text states that “sparse” modifies visit data and “conditions met” determines whether analysis proceeds. Whole-body scan found no compressed phrase implying sparse randomization, completed validation, or pooled trials. |

All 11 IDs in `included_repair_item_ids` have exactly one row above; none is unresolved.

## Protected-content preservation mapping

| Protected ID | Revised locator(s) | Item-level preservation evidence in frozen v047 |
|---|---|---|
| PCR-001 | Frontmatter `identity_anchor`; H1 and summary; section 3 `Background` and `Gap`; section 4 `Primary research question` | The study remains the longitudinal sepsis-centred ICU patient system spanning comparable pre-onset risk intervals, first onset, mutually exclusive post-onset evolution, recovery/persistent illness/organ failure, alive ICU exit, and death. The question asks whether the named full-course candidate dynamic-system representation can recover and transport patient states and structure; it is not recast as generic risk prediction. |
| PCR-002 | Summary and structured abstract `Objective and hypothesis`; section 5; section 12 `Contribution and evidence ladder` | The dossier retains all three commitments: stage I–II is the 24-month minimum and uses literature/expert knowledge plus public ICU data for full-course representation, system identification/recovery, and cross-database testing; delivery explicitly includes one or more high-level papers and auditable scientific evidence/resources; and the contribution paragraph states that delivery does not contract to a single prediction tool. |
| PCR-003 | Frontmatter `study_object` and `primary_unit_of_inference`; summary; structured abstract `Objective and hypothesis`; sections 4, 7, and 8 | The object is still the longitudinal sepsis-centred ICU system with pre-onset at-risk intervals and post-onset trajectories. The primary unit remains the patient–time state and transition; overlapping landmarks receive total stay weight 1, and uncertainty and inference retain patient and hospital clustering. |
| PCR-004 | Section 6 `Current resource and evidence status` and `Public ICU database roles and G1 audit fields`; section 14 `Feasibility and resources` and limitation 1 | Inputs remain literature/expert knowledge, MIMIC-IV, and eICU-CRD, with HiRID or AmsterdamUMCdb selected prospectively as a backup. Database existence and public version are verified; team credentials, data-use agreements, runnable extraction, exact project support, named staff, and model/results remain unverified or not generated rather than being presented as available. |
| PCR-005 | Section 6 trial-status table and `本地随机对照试验证据及当前状态`; section 7 `共同前提`; section 14 limitations 8–9 | EXIT-SEP and XBJ-SCAP remain only potential individual-level sources for work after the primary study. Local reports remain derivative cleaning/validation evidence and do not replace individual-data authorization, original CRF/SAP, randomization, centre, visit timing, or death/hospital/discharge/transfer semantics. |
| PCR-006 | Section 5 `Work packages and minimum sequence`; section 6 `Variable-use separation`; section 7 `Observational target, anchoring, missingness, and abstention`, absolute simulation, and external validation | The sequence remains resources/G1 → labels/states/hospital partition → simple baselines → absolute recovery and false-confidence checks → at most one complex candidate → two primary tasks/two secondary diagnostics → fixed analysis specification → untouched cross-database test, with later trial work only afterwards. X, Y, A, M, B, and site roles remain separated. The method retains 20-seed alignment below 90%, bootstrap retention below 80%, external sign consistency below 80%, state alignment below 0.70, and uncalibrated intervals as triggers for deletion, merging, or database/policy-specific interpretation; prediction cannot override them. |
| PCR-007 | Section 5 `Conjunctive minimum success definition`; section 7 `Hospital-primary cross-database validation`; section 11 interpretation matrix; section 14 limitations 6–7 | Stage-II support remains conjunctive across data support, absolute recovery, both primary-task proper scores and calibration, leakage clearance, zero-update external performance, state alignment, and structural stability. Re-calibration, observation-layer updating, and complete refitting are reported separately and cannot replace failure of the zero-update external test. Work after 24 months cannot count toward or repair stage-II success. |
| PCR-008 | Section 7 `Protocol definitions for the two primary clinical tasks` and `Mutually exclusive post-onset state and event system`; section 8 items 1 and 4 | Both primary tasks and their scientific rules are retained: specimen–antibiotic 72-hour/24-hour pairing, baseline-SOFA rule, rolling 24-hour component calculation, first sortable onset, event/availability clocks, incident risk set and delayed entry, mutually exclusive post-onset states and competing termination, as-of features, total weight 1 across overlapping landmarks, within-bin A_t/next-state ordering and exclusion of unsortable same-time edges, proper-score/calibration targets, patient/hospital clustering, and checks for future data, treatment, measurement-frequency, repeated-record, split, imputation, grid, and threshold leakage. |
| PCR-009 | Sections 1–2; section 6 evidence-status table; section 12; section 13 claim-support table | The dossier consistently describes a planned candidate representation and planned tests; model fitting, simulation recovery, external validation, and new trial results remain not generated. The contribution is bounded to conditional evidence integration, validation, benchmark, and reusable-resource value. Individual modules are acknowledged as prior art, and the complete-combination gap retains low-to-medium confidence rather than supporting a first or new-algorithm claim. |
| PCR-010 | Section 14 `Working assumptions`, `Limitations and boundary conditions`, and trial-related limitations; section 7 method authorities; section 11 falsification and interpretation | Section 14 alone holds the complete limitation families and both unresolved specifications: clinical-scale-to-simulation-parameter mapping, and the exact multicategory-calibration estimator/confidence bounds/threshold-registration details. Each assumption has a decision point, allowed information, and consequence. Screening event/parameter counts do not replace empirical effective sample size or simulation stability. Method eligibility/alternatives remain in section 7, result falsification and result-dependent interpretation in section 11, and inconsistent or imprecise trial directions cannot be rescued through subgroup selection. |
| PCR-011 | Title and summary; section 4 one subordinate question and objective; section 5 work package 5; section 6 status-only trial material; section 7 full trial-method authority; sections 8–11 one function-specific item each; section 12 bounded closest-work row; section 14 resource, limitation, and operational-risk entries | Stage I–II remains the 24-month minimum. The method authority first states shared prerequisites—successful stage II, available individual data, and verifiable core trial semantics—then separates observation mapping from the independent clinical-state analysis, followed by the semantic stop. Mapping conditions are not applied to the independent analysis. The title omits later work; the summary contains only a subordinate purpose; other sections carry only their contract-specific data, interface, evidence, required-analysis, or output role. No branch is represented as a parallel primary contribution or title claim, and no later result can supplement stage II. |
| PCR-012 | Section 14 `Claims not supported by the current design`; minimal local boundaries in section 4 question, section 7 observational estimand and trial interpretation, and section 11 result matrix | The complete prohibited-claim list appears once in section 14: observational data and prediction do not establish a true causal network, treatment effects, counterfactual policy, mechanism, mediation, control, or digital twin; trial secondary analyses do not validate unmeasured dynamics, transition edges, or the whole representation; the plan is not an already validated model, clinical decision tool, drug platform, global first, new algorithm, or unconditional clinical-promotion basis. Elsewhere only the boundary needed to interpret the adjacent estimand or result is retained, without a grouped repetition or section-14 pointer. |

All protected IDs PCR-001 through PCR-012 have exactly one row above and retain their required scientific meaning, evidence status, or authority location.

## Core-role concordance

| Scientific role | Stable reader-facing name | First-use locator | Competing forms removed or reclassified | All-occurrence result |
|---|---|---|---|---|
| Central study object | `脓毒症全病程候选动态系统表征` | H1, then repeated in the one-sentence summary | `候选全病程表征`, `跨数据库候选系统表征`, and other compressed core names were removed; after the full name, `候选表征` is used only as its defined short form. | Full-name and defined-short-form occurrences refer to the same longitudinal object; no alternate core object remains. |
| Primary research question | Whether the named candidate representation can cover the sepsis-centred pre-onset/onset/post-onset/outcome continuum and obtain quantifiable state/structure support across hospitals and databases | Section 4 `Primary research question` | Generic prediction and generic ICU risk stratification are excluded from the question; the later trial purpose remains subordinate. | Question, objectives, methods, and claim table preserve the same object, tasks, evidence base, and unit of inference. |
| Pre-onset primary task | `未来 12 小时首次发病风险`, technically estimated as the `未来 12 小时首次发病累积发生函数（CIF）` | Summary; technical estimator first defined in section 7 protocol table | The plain-language outcome and its technical estimator are explicitly related, not competing outcomes. | Every primary-task occurrence uses the 12-hour first-onset horizon; alarm burden and AUPRC remain secondary metrics. |
| Post-onset primary outcome | `第 7 日有利状态占用概率` | Summary | `第 7 日状态占用` was replaced in primary-task prose; `第 7 日多状态队列` remains only as the input dataset and per-state calibration remains a secondary analysis. | Summary, abstract, work package 3, protocol estimand, and evidence chain agree that the favourable set is physiological recovery or alive ICU exit, reported separately as well. |
| Primary contribution | `证据整合、验证、基准与可复用资源` | Summary | English or slash-compressed benchmark/resource labels and algorithm-novelty framing were removed. | Positioning, contribution ladder, and claim-support table use the same bounded planned contribution and planned evidence status. |
| Data-support audit | `双库可观测性与数据支持审计（G1 审计）` | Section 5 `Twenty-four-month minimum and dated decisions` | Bare G1 and forms that used one label for audit, threshold, result, or decision were removed. | Every later G1 occurrence means the audit; standards, results, and consequences are named separately. |
| Primary external test | `不使用外部测试数据更新任何模型参数的外部检验（零更新外部检验）` | Structured abstract `Approach` | `zero update`, `zero-update`, and bare `零更新` were removed; re-calibration, observation-layer update, and full refit remain distinct procedures. | Every later occurrence uses `零更新外部检验` with the same no-update meaning. |
| Conditional downstream purpose | `条件满足后的随机对照试验次要分析` | Summary as a purpose-level clause; full method name in section 7 | `条件性稀疏 RCT`, unexplained stage/branch labels, and wording that made sparse modify randomization were removed. | “Conditions met” always controls whether analysis proceeds; “sparse” always modifies visit data; the two trials remain separate. |
| Independent trial endpoint and analysis | `独立次要临床状态端点`; `试验特异独立次要临床状态再分析` | Section 7 `观测映射不成立时的独立分析` | `death-ranked`, `独立 SOFA`, and generic fallback labels were removed. | Every later occurrence distinguishes the endpoint from the analysis and does not associate either with the stage-II projection summary. |
| Time-varying scientific roles | `患者状态 X_t`, `生理测量 Y_t`, `治疗行动 A_t`, and `测量过程 M_t` | Section 6 role table for Y_t/A_t/M_t; complete notation in section 7 observational target | The variable “firewall” metaphor and ambiguous state/action/measurement labels were replaced by role-specific names and allowed uses. | Role table, estimand, implementation record, and contribution section preserve the same separation without dual-role ambiguity. |

## Authority and section-function checks

| Check | Result in frozen v047 |
|---|---|
| Limitation authority | Complete limitation families, working assumptions, unsupported claims, and non-method operational risks occur in section 14. Retained local boundaries occur only where their removal would misstate an adjacent background inference, estimand, method decision, falsification result, data-status statement, or claim-support judgment. No section-14 pointer remains. |
| Trial-component projection | Title omits the component; summary gives one purpose-level clause; abstract gives one short purpose-and-sequence statement; section 3 omits it; section 4 has one subordinate question and one objective; section 5 has one dependent work-package row; section 6 gives availability/status only; section 7 is the sole complete authority; sections 8–11 each give one interface/evidence/required-analysis/output role; section 12 contains only a bounded closest-work comparison and no parallel contribution; section 13 has no trial claim row; section 14 gives resource status, complete limitations, and one operational delay risk without repeating the method tree. |
| Reader-language scan | Core abbreviations with scientific roles are expanded at first use; contract-fixed scaffold labels remain unchanged; free headings and table labels use natural scientific language. The body contains no internal assessment, revision-history, or hidden process prose. |
| Trigger–object–consequence scan | Decisions distinguish the diagnostic result, affected scientific object, required action, and consequence. No compact action word carries multiple roles. |

## Deterministic validation

- Command executed on the frozen v047 dossier only: `python research-skills-openai/skills/multi-path-idea-generator/scripts/lint_idea_dossier.py tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v13/idea-dossier-v047.md --expected-plugin-version 0.9.0-preview.3`
- Final result: `OK`; exit code 0; no advisory.
- Independent mechanical checks: H1 equals the Title field; 15 required H2 sections are present in order; section 3 contains the five required H3 functions in order; the summary is one field and one sentence; five evidence chains each contain Input, Method/analysis/processing, Output, and Supports.
- This validation establishes deterministic structure and plugin-version binding only; it does not declare narrative or language readiness.

## Files read

### Project artifacts read

Only these three project inputs were read:

1. `tests/idea-test-0.9.0-preview.1/0.9.0-preview.1/03_ideas/nodes/I01-001/dossiers/idea-dossier-v003.md`
2. `tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/baseline-current/editorial-repair-writer-brief-r086.yaml`
3. `tests/idea-narrative-forward-0.9.0-preview.3/run-001/inputs/protected-content-register-v004.yaml`

The frozen v047 output was then reopened only for locator verification and deterministic validation. No narrative or language assessment, assessor repair plan, older dossier, prior revision, temporary draft, revision delta, preflight, evaluation, or project test script was read.

### Operating instructions read

1. `AGENTS.md`
2. `research-skills-openai/AGENTS.md`

### Development skill-contract files read

1. `research-skills-openai/skills/multi-path-idea-generator/SKILL.md`
2. `research-skills-openai/skills/multi-path-idea-generator/references/idea-schema.md`
3. `research-skills-openai/skills/multi-path-idea-generator/references/generation-quality-gates.md`
4. `research-skills-openai/skills/multi-path-idea-generator/references/downstream-handoff-rules.md`
5. `research-skills-openai/skills/multi-path-idea-generator/templates/idea-dossier.md`
6. `research-skills-openai/skills/research-idea-orchestrator/references/idea-artifact-lifecycle.md`
7. `research-skills-openai/skills/research-idea-orchestrator/references/idea-dossier-contract.md`
8. `research-skills-openai/skills/multi-path-idea-generator/references/novelty-claim-rules.md`

The deterministic linter was executed as a validation tool but was not opened or inspected as a project input.

## Handoff status

- Complete revised dossier: frozen.
- Revision delta: frozen after dossier freeze.
- Included repair items mapped: 11 of 11.
- Protected items mapped: 12 of 12.
- Scientific change required: no.
- Identity drift detected: no.
- Missing scientific confirmation introduced by the editorial repair: no.
- Fresh independent preservation and narrative/language reassessment remain downstream decisions; this writer does not issue those verdicts.
