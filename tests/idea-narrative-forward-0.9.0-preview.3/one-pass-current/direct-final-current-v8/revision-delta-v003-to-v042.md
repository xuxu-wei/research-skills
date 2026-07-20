---
schema_version: research-idea-revision-delta.v1
plugin_version: 0.9.0-preview.3
artifact_id: revision-delta-I01-001-v003-to-v042
workflow_id: RID-SEPSIS-CSM-20260717-001
idea_id: I01-001
version_id: v042
path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v8/revision-delta-v003-to-v042.md
based_on:
  - artifact_id: idea-dossier-I01-001-v003
    version: v003
    path: tests/idea-test-0.9.0-preview.1/0.9.0-preview.1/03_ideas/nodes/I01-001/dossiers/idea-dossier-v003.md
revised_artifact:
  artifact_id: idea-dossier-I01-001-v042
  version: v042
  path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v8/idea-dossier-v042.md
repair_inputs:
  narrative_plan: narrative-repair-plan-I01-001-r056
  language_assessment: language-assessment-r059
  protected_register: protected-content-register-I01-001-v003-r003
  reader_handoff: reader-handoff-forward-001
source_skill: multi-path-idea-generator
change_type: editorial_repair_delta
frozen: true
---

# Revision delta: idea dossier v003 to v042

## Scope, lineage, and editorial boundary

- **Source:** `idea-dossier-I01-001-v003`, version `v003`, at the single logical path recorded in `based_on`.
- **Revised artifact:** `idea-dossier-I01-001-v042`, version `v042`.
- **Active plugin binding:** `0.9.0-preview.3` for both revised outputs.
- **Change route:** editorial repair only. The primary question, objective, study object, evidence base, unit of inference, design choices, numerical and temporal rules, evidence status, claim strength, alternatives, and stopping logic are unchanged.
- **Operations used:** replacement, definition, movement, splitting, merging, deletion of duplicate wording, reordering, bridges, and consolidation. No data, method, result, assumption, restriction, or scientific route was added.
- **Readiness boundary:** this delta records writer-side execution and mechanical checks only. It does not declare narrative, language, scientific, or evaluation readiness; any such decision requires a fresh independent review.
- **Evidence rule:** the revised dossier text at each locator below is the preservation evidence. This delta's assertion by itself is not evidence.

## Narrative-repair action coverage

| Action | Operation and revised locator | Text-grounded acceptance evidence |
|---|---|---|
| NRP-001 | Replaced and split `Background, current state, gap, significance, and rationale` into the required ordered H3 sequence: `Background`, `Current state`, `Gap`, `Significance`, `Rationale`. | `Gap` now asks whether a public-ICU-supported patient-time representation can be reconstructed and remain stable across databases, explicitly stating that the gap is not merely absence of an identical module combination. `Significance` explains why distinguishing physiology from care and measurement policy matters. `Rationale` connects dual clocks, role separation, prespecified generative-data checks, and independent cross-database testing to that gap, with only a bounded stage-III preview. All source facts and citations [1-3,5-10,14-18,21-37] remain in the five-part chain. |
| NRP-002 | Replaced the one-sentence summary in `Title, summary, audience, and positioning` and functionally separated the five fields in `Structured abstract`. | The summary has two top-level trunks: the 24-month stage-I–II object, validation, and deliverables; then the downstream trial component under shared prerequisites, its two alternative branches, and overall stop. Each abstract bullet performs only its named function. Core terms used there are defined in reader language; detailed thresholds remain in methods. |
| NRP-003 | Consolidated complete stage-III eligibility, mapping, R0, R1, estimand, independent analysis, missingness, multiplicity, and stopping rules in `Research design and methods > Trial analyses after stage II`. | The authority subsection begins with shared prerequisites, defines `试验语义与共同生理锚点合格性标准（R0）`, the frozen mapping and `一维投影摘要（P_obs）`, `测量一致性、校准与投影重建误差标准（R1）`, the projection-summary comparison, the independent clinical-state analysis, and the overall semantic stop. The question, objective 4, WP5, fifth evidence chain, planned outputs, contribution ladder, and Claim-Support table retain only the content required by their own function. |
| NRP-004 | Consolidated full limitations, pending specifications, contingencies, alternatives, and operational stops in `Feasibility, resources, risks, alternatives, and stop conditions`; removed the fifth standalone limitation field from every evidence chain. | There are five evidence-chain H3s. Each contains exactly `Input`, `Method / analysis / processing`, `Output`, and `Supports`, with no `Limits and failure conditions`. Section 14 contains the complete resource, access, G1, label/leakage, reconstruction, missingness/overlap, external-testing, timing, trial-data, bridge, closest-work, and unsupported-claim boundaries. Local boundaries retained elsewhere directly delimit the adjacent estimand, variable role, analysis eligibility, or interpretation and do not point to section 14. |
| NRP-005 | Replaced the technique-only list with an implementation graph in `Key techniques and implementation`. | Each of ten rows names an implementation unit and states its inputs, outputs, persistent audit record, upstream/downstream interface, and freeze or version boundary. The rows cover the dual-clock label package, G1 audit, variable-role register, baseline/candidate pipeline, anchor/alignment register, missingness and policy-support diagnostics, hospital split and freeze list, trial projection package, uncertainty/multiplicity specification, and negative-control/unsatisfied-standard publication package. |
| NRP-006 | Consolidated repeated specifications while retaining all 15 H2 sections and their distinct contracts. | Section 5 now carries dates, dependencies, deliverables, consequences, five work packages, and minimum order; section 6 carries sources and current evidence states; section 7 carries complete protocols and thresholds; section 8 carries implementation objects; section 9 carries traceability; section 10 carries required acceptance evidence; section 11 carries outputs, falsification, and interpretation; sections 12 and 13 carry contribution explanation and claim audit; section 14 carries global constraints and stops. Full simulation, external-data, and R0/R1 specifications each have one technical authority location. |
| NRP-007 | Defined or replaced cross-disciplinary terms at first use throughout the dossier. | First uses now explain: candidate representation in the summary; event and label-availability times in `Background`; state/action/measurement-process separation and simulation reconstruction in the abstract; G1 in section 5; proper probability scores in the stage-II success definition; assessment time, CIF, and other primary-task roles in methods; the two external hospital sets and four parameter operations in external validation; P_obs and independent clinical-state analysis in the trial authority subsection. No new compressed substitute label was introduced. |

## Language-action coverage

| Finding | Revised locators and operation | Acceptance evidence and all-occurrence result |
|---|---|---|
| LNG-R059-001 | Replaced the H1 and `Title` field with the supplied title; synchronized section 1 positioning, question, objective 4, fifth evidence-chain title, contribution text, and Claim-Support rows. | The title reads `脓毒症全病程候选动态系统表征：计划开展跨数据库检验，并在满足预设条件时对随机对照试验的稀疏随访测量进行次要分析`. The condition attaches to conducting the secondary analysis, and “稀疏” modifies follow-up measurements. Whole-file scans find no `稀疏 RCT`, `实际稀疏 RCT`, or `条件性稀疏 RCT`. |
| LNG-R059-002 | Defined `脓毒症全病程候选动态系统表征（下称“候选表征”）` in the summary; reserved `复杂候选模型` for the optional switching/nonlinear implementation and `阶段 II 冻结的候选表征` or an explicit frozen observation equation for stage-II outputs. | The central object is consistently `候选表征`; the implementation is consistently `复杂候选模型`. Whole-file scans find no `候选架构`, `候选系统表征`, `最小全病程候选表示`, or unscoped `整个系统模型/整个模型` referring to the central object. |
| LNG-R059-003 | Separated clinical, simulation, and error-support roles throughout summary, methods, work packages, evidence chains, outputs, interpretations, contribution, and risks. | Patient outcome is `生理恢复状态`; simulation evaluation is `模拟重建性能`, first defined as reconstruction of prespecified states, transitions, and structure under known generative mechanisms; erroneous confidence is `错误结构被高置信度支持的频率` or the direct noun phrase `错误结构高置信度支持率`. A scan finds no `绝对恢复` or `假置信`, and unqualified “恢复” is not used for simulation. |
| LNG-R059-004 | Replaced generic gate metaphors with scientific condition types; defined G1, R0, and R1 in full at first use. | `双数据库可观测性审计最低标准（G1）` first appears in section 5; `试验语义与共同生理锚点合格性标准（R0）` and `测量一致性、校准与投影重建误差标准（R1）` first appear in the stage-III authority subsection. Scientific prose uses `启动条件`, `最低标准`, `判定标准`, or `停止条件`; the character `门` does not occur as a condition metaphor. All original dates, thresholds, conjunctions, and consequences remain. |
| LNG-R059-005 | Defined external data roles and parameter operations in `Hospital-primary cross-database validation`; synchronized all other sections. | Data roles are only `适配医院集` and `最终检验医院集`, with the latter defined as unavailable for outcome or performance inspection during development and adaptation. The four operations are only `不更新任何模型参数`, `仅用适配医院集重新估计校准参数`, `仅用适配医院集重新估计观测层参数`, and `用目标数据库重新拟合全模型（属于模型再开发，不作为外部验证）`. Scans find no `adaptation/test`, `untouched`, `zero-update`, `decoder adaptation`, `full refit`, or `transport updating`. |
| LNG-R059-006 | Defined P_obs and the independent branch in the stage-III authority subsection; synchronized overview, question, objective, schedule, evidence chain, outputs, contribution, Claim-Support, and section 14. | The quantity is `基于实际 D7 或 D8 观测值计算的一维投影摘要（P_obs）`; its result is `随机分组在该访视投影摘要上的差异`. The alternative is `独立于阶段 II 候选表征、按死亡和 SOFA 排序的试验特异性次要临床状态分析（下称“独立临床状态分析”）`. Scans find no `death-ranked`, `fallback`, `projection-pass`, `trial-specific clinical-state`, or result named only as a “扰动”. |
| LNG-R059-007 | Replaced internal English status strings and workflow state prose in data, evidence-chain, claim-support, and identity sections. | Resource evidence uses only `已有公开资料支持/尚未核验/尚未生成/项目内衍生资料`; transport results use `跨数据库稳定/仅适用于特定数据库/证据不足而不作解释`; claim support uses `有支持/有条件支持/无支持`. Reader prose contains no `identity_status`, `new_idea_required`, or English `verified/unverified/not generated/project-local derivative/supported/qualified/unsupported` status values. |
| LNG-R059-008 | Replaced disposition and workflow metaphors with direct scientific operations across the complete dossier. | The dossier now says which analysis stops, which alternative is used, which result remains reportable, and which claim is no longer supported—for example, `停止继续评价该复杂候选模型，转用多状态、线性或仅预测基线`. Scans find no `降级`, `淘汰`, `晋级`, `挽救`, `救回`, `豁免`, `封存`, `封印`, `防火墙`, `data-access no-go`, `fallback`, `stop`, `失败图`, or `失败产物` in reader-facing prose. |
| LNG-R059-009 | Split high-density R0, R1, and trial-start passages into definition sentences and categorized bullet lists; split closest-work conclusion into three sentences; retained one-sentence summary. | The summary remains one sentence with a stage-I–II trunk and a conditional downstream-trial trunk. R0 and R1 each have a definition, one-condition-per-bullet list, and a distinct failure consequence. Trial-start evidence in section 10 is a four-bullet list. The closest-work paragraph separately states the search finding, uncovered sources, and allowed positioning. No threshold, condition, branch, or evidence-strength statement was deleted. |

## Protected-content preservation evidence

Every row below points to actual revised-dossier text. Multiple commitments within a protected item are separated rather than represented by a section topic alone.

### PCR-001 — identity and question

| Independent protected commitment | Revised body locator | Revised-dossier evidence |
|---|---|---|
| Central object is a sepsis-centered dynamic representation spanning at-risk non-onset, first onset, post-onset evolution, recovery, deterioration, organ failure, ICU exit, and death. | `Title, summary, audience, and positioning > One-sentence complete-Idea summary`; `Research question, objectives, and core hypothesis > Primary research question` | The summary names `发病前在险时段、首次发病以及发病后生理恢复状态、持续恶化、器官衰竭、离开 ICU 或死亡结局`; the question repeats the same continuum. |
| The idea is not ordinary clinical prediction or generic ICU risk stratification. | `Title, summary, audience, and positioning > Positioning and contribution frame`; `Research question, objectives, and core hypothesis`, paragraph after objectives | The positioning defines integration, validation, benchmark/resource, and falsifiable research governance; the objective paragraph states `不得把研究收缩为只产出一个预测工具`. |

### PCR-002 — primary objective and deliverables

| Independent protected commitment | Revised body locator | Revised-dossier evidence |
|---|---|---|
| Complete stages I–II within 24 months, constrain candidate structure by literature and expert knowledge, use public ICU data for system identification, cross-database validation, and whole-course state characterization. | `Research question, objectives, and core hypothesis`, paragraph after objectives; `Research content and work packages > Twenty-four-month minimum and dated stages` | The paragraph states exactly that 24-month objective and the literature/expert, public-ICU, system-identification, cross-database, whole-course elements; the dated-stage opening states that stages I–II must finish within 24 months. |
| High-level papers and auditable scientific evidence remain explicit deliverable directions. | Section 1 summary and positioning; `Expected outputs > Planned outputs`, item 6 | The summary commits to `可审计科学证据、高水平同行评议论文`; item 6 specifies an auditable evidence package for high-level peer-reviewed papers. |
| Deliverable is not narrowed to only a prediction tool. | Section 1 positioning; section 4 paragraph after objectives; `Expected outputs > Planned outputs`, item 6 | Each location explicitly says the work is not reduced to a single prediction tool. |

### PCR-003 — object, scope, and unit of inference

| Independent protected commitment | Revised body locator | Revised-dossier evidence |
|---|---|---|
| Study object is the longitudinal sepsis-centered ICU patient system, including comparable at-risk non-onset intervals and post-onset trajectories. | `Research question, objectives, and core hypothesis`, paragraph immediately before `Core hypothesis and non-hypotheses` | The body states `研究对象是纵向、以脓毒症为中心的 ICU 患者系统，包括可比较的未发病在险时段和发病后轨迹`. |
| Primary unit is patient-time state and state transition, respecting patient and hospital clustering. | Same locator; `Research design and methods > Protocol locks for the two primary clinical tasks`, uncertainty row | The body states `主要推断单位是患者—时间状态及状态转移` and that inference respects patient/hospital clustering; the protocol uses patient/hospital two-level bootstrap intervals. |

### PCR-004 — public ICU inputs and current status

| Independent protected commitment | Revised body locator | Revised-dossier evidence |
|---|---|---|
| Core inputs are literature/expert priors and longitudinal MIMIC-IV/eICU-CRD data; HiRID or AmsterdamUMCdb is a prespecified conditional backup. | Section 1 summary; `Data, materials, and existing evidence base > Public ICU database roles and G1 audit` | The summary names literature/expert priors and the two public ICU databases; the database-role list permits HiRID or AmsterdamUMCdb only as a month-0–3 prespecified, equivalently audited backup. |
| Database existence and versions are supported, but team credentials, data-use agreements, runnable extraction, and project cohort support are not established. | `Data, materials, and existing evidence base > Current resource and evidence status`, first three rows | Rows distinguish `已有公开资料支持` for existence/version from `尚未核验` credentials and `尚未生成` G1 cohort/event/interface counts. |
| Named personnel, commitments, and model results remain absent or not generated. | Same table, team-role, personnel, and result rows | The team-role row says a role specification is not a personnel commitment; the personnel row is `尚未核验`; the model/simulation/prediction/final-test/trial-result row is `尚未生成`. |

### PCR-005 — randomized-trial inputs and current limits

| Independent protected commitment | Revised body locator | Revised-dossier evidence |
|---|---|---|
| EXIT-SEP and XBJ-SCAP are only potential individual-level data sources for conditional stage III. | Section 1 summary; `Research design and methods > Trial analyses after stage II`, opening paragraph | Stage III begins only after stage-II success, data availability, and core semantic verification; both trials are analyzed separately and only after those prerequisites. |
| Current local materials are derivative cleaning/validation reports, not substitutes for authorization, original CRF/SAP, randomization, center, visit timing, or survival/hospital semantics. | `Data, materials, and existing evidence base > Current resource and evidence status`, trial rows; `Local randomized-trial evidence and present limits` | The table and trial paragraphs explicitly state the reports' derivative status and list authorization, CRF/SAP, randomization, center, D0/D1/D7/D8 timing, death, hospital, discharge, and transfer semantics as unverified. |

### PCR-006 — design sequence, role separation, and interpretation thresholds

| Independent protected commitment | Revised body locator | Revised-dossier evidence |
|---|---|---|
| Fixed order is resource/observability audit; label/state/hospital split lock; simple baselines; simulation reconstruction and erroneous-confidence checks; at most one complex candidate; two primary and two secondary tasks; freeze; independent cross-database test; only then conditional trial analysis. | `Research content and work packages > Work packages and minimum route`, final paragraph | The arrow-separated sequence states every step in that order, and the following sentence prohibits later trial results from bypassing or filling earlier stage-II requirements. |
| State, treatment action, and observation process are separated. | `Structured abstract > Approach`; `Data, materials, and existing evidence base > Candidate variable-role separation`; `Research design and methods > Observational target, anchoring, missingness and abstention` | The abstract explains the scientific purpose; the role table gives Y_t/A_t/M_t and label-only rules; the methods define the joint distribution with separate variables. |
| Interpretable quantities are bounded by anchoring, alignment, reconstructability, cross-database performance, and abstention. | `Research design and methods > Observational target, anchoring, missingness and abstention` | Only aligned state occupancy, transitions, anchor prediction, and prespecified sign/lag are interpretable; raw latent labels, arbitrary rotations, and unaudited edges are excluded. |
| Alignment <90%, bootstrap retention <80%, external sign agreement <80%, state alignment <0.70, or uncalibrated intervals cause deletion, merging, or database/policy-specific interpretation. | Same locator, final paragraph | All five thresholds and their delete/merge/database-or-policy-specific consequence appear in one sentence. |
| Better prediction cannot override those decisions. | Same locator; `Simulation and semi-synthetic reconstruction criteria` | The methods state `较好的预测表现不能抵消这些判定`; the simulation table states recalibration cannot offset structural reconstruction failure. |

### PCR-007 — conjunctive stage-II success and external parameter handling

| Independent protected commitment | Revised body locator | Revised-dossier evidence |
|---|---|---|
| Stage-II success is conjunctive across data support, simulation reconstruction, two primary-task proper scores and calibration, no severe leakage, final-test performance without parameter updates, state alignment, and structural stability. | `Research content and work packages > Conjunctive minimum success definition`; `Structured abstract > Contribution and impact` | The five numbered requirements and abstract contribution sentence jointly name every conjunct; exact primary-task thresholds and external-state thresholds are in the method authority subsections. |
| Limited updates learned only in the adaptation hospitals are reported separately and cannot replace failure without parameter updates. | `Conjunctive minimum success definition`, closing paragraph; `Hospital-primary cross-database validation`, four-operation list | The dossier explicitly separates recalibrating or re-estimating observation parameters from no-update results and says they cannot replace the latter. |
| Stage III neither counts toward nor fills stage-II success. | Same closing paragraph; section 14 stage-III authority paragraph | Both state that stage III does not count toward or make up the stage-II conjunction. |

### PCR-008 — primary-task protocol and leakage safeguards

| Independent protected commitment | Revised body locator | Revised-dossier evidence |
|---|---|---|
| Two primary tasks, event/availability dual clocks, first-onset risk set, delayed entry, mutually exclusive post-onset states, and competing termination remain fixed. | `Research design and methods > Protocol locks for the two primary clinical tasks`; `Mutually exclusive post-onset state and event system` | The two-column task table defines populations, clocks, horizons, competing events, estimands, metrics, uncertainty, and pass/fail; the state table defines the mutually exclusive priority system and terminal states. |
| Infection pairing is specimen first then antibiotic within 72h or antibiotic first then specimen within 24h; baseline SOFA, rolling 24h components, and first sortable onset remain fixed. | Protocol table, `Event clock` row | The row contains the 72h/24h pair, baseline SOFA=0 or pre-ICU 24h minimum, rolling 24h worst components, −48h/+24h SOFA window, and first sortable qualifying onset. |
| Only first onset is analyzed; overlapping assessment times have total stay weight 1. | Protocol table, `First onset and repeats` row | The row states both commitments verbatim in reader language. |
| A_t within an interval precedes the next-state measurement; unorderable same-timestamp edges are excluded. | Protocol table, `Within-interval order` row | The row defines [t,t+12h) action A_t, next-boundary physiology, and exclusion of unorderable same-timestamp transitions for both tasks. |
| As-of features, calibration/proper-score targets, and patient/hospital clustered uncertainty remain fixed. | Protocol table, `Label-availability clock`, `Metric`, `Uncertainty`, and `Pass or fail` rows | The rows define information availability, Brier/calibration targets, two-level bootstrap, and exact +0.01, 0.80–1.20, and 0.02 criteria. |
| Leakage checks include same-interval treatment, future measurement frequency, repeat admissions or stays, and outcome-driven grids or thresholds. | Paragraph immediately after the protocol table | The paragraph lists later-available physiology/treatment, same-interval actions, future measurement frequency, cross-split processing, patient/ICU-stay crossings, overlap weights, and outcome-driven variables, grids, or thresholds. |

### PCR-009 — planned evidence and claim strength

| Independent protected commitment | Revised body locator | Revised-dossier evidence |
|---|---|---|
| Candidate representation and validation are planned; there is no current model, simulation reconstruction, external validation, or new trial result. | `Structured abstract > Expected result`; resource-status table, current-result row | The abstract states all are planned outputs; the row marks every named result class `尚未生成`. |
| Defensible contribution is conditional integration, validation, and benchmark/resource value. | Section 1 positioning; `Contribution and evidence ladder` | Both use those bounded contribution frames and condition them on execution. |
| Individual modules have precedents; complete-combination gap is low-to-moderate confidence; no global-first or new-algorithm claim. | `Verified representative closest-work comparison`, final three-sentence paragraph; Claim-Support table | The first sentence distinguishes high-confidence module precedent from low-to-moderate confidence negative conjunction; the third permits only conditional integration/validation. Claim-Support gives global originality `无支持`. |

### PCR-010 — section-14 authority, unresolved specifications, and stops

| Independent protected commitment | Revised body locator | Revised-dossier evidence |
|---|---|---|
| Section 14 is the complete authority for resource/access, team commitment, G1 support, label/leakage, state reconstruction, missingness/overlap, no-update external testing, timing, trial data/semantics, common anchors/observation mapping, closest-work uncertainty, and unsupported claim classes. | `Feasibility, resources, risks, alternatives, and stop conditions > Feasibility and resources`; `Limitations and boundary conditions` items 1–9 | The nine-item list names all protected limitation classes and keeps evidence states unstrengthened. |
| Every operational failure trigger has a bounded alternative and stopping or claim consequence. | `Risks, alternatives, and stop conditions` table | Eleven rows separately cover access/support, cross-hospital links, leakage, reconstruction, missingness/overlap, transport, shared trial prerequisites, observational bridge, independent-analysis eligibility, discordant/uncertain trial results, time, and closest-work overreach. |
| Clinical-scale-to-simulation-parameter mapping remains unresolved. | `Working assumptions`, first table row | It is explicitly a pending specification, with fixed content, allowed decision information, named decision point, and consequence; no assumed value is supplied. |
| Exact multiclass calibration estimator, confidence-bound implementation, and threshold-registry format remain unresolved. | `Working assumptions`, second row | It is explicitly pending with fixed endpoints/thresholds, allowed evidence, decision point, and consequence; no method is guessed. |
| Event/parameter screening floors do not replace empirical effective sample size or simulation stability. | Paragraph after `Working assumptions` table | The dossier states this boundary directly. |
| Discordant trial directions or wide intervals yield no support or limited cross-setting applicability; subgroup selection cannot rescue the conclusion. | Risk table, `两项试验结果不一致或不精确` row; `Expected outputs > Falsification criteria` | Both preserve the no-subgroup-rescue rule and bounded interpretation. |

### PCR-011 — stage-III branch fidelity

| Independent protected commitment | Revised body locator | Revised-dossier evidence |
|---|---|---|
| Stages I–II finish within 24 months; stage III is outside the minimum deliverable. | Section 1 summary; section 5 opening and dated table; section 14 `Limitations and boundary conditions`, item 6 | Each distinguishes the 24-month stage-I–II minimum from the downstream trial component. |
| Shared prerequisites are stage-II success, availability of the relevant individual-level trial data, and verifiable core trial semantics. | Section 1 summary; structured-abstract approach; primary question; objective 4; dated stage-III row; method opening; fifth evidence-chain input; planned output 5; Claim-Support overall trial row; section 14 authority paragraph | Each location starts the trial logic with only these shared prerequisites; observational bridging is not promoted to a shared prerequisite. |
| Mapping branch additionally requires an established observational bridge and yields a comparison of randomized groups on the visit projection summary. | Same overview and authority locators; method `R0`, frozen mapping, `R1`, and `观测桥接成立时的访视投影摘要比较` | The branch adds R0 common-anchor eligibility and R1, then reports randomized-group differences on the actual-visit P_obs summary. |
| If the observational bridge fails but SOFA, randomization, center, and survival/hospital semantics are verifiable, the independent branch remains available and is independent of the candidate representation. | Same overview and authority locators; method `观测桥接不成立但独立分析条件满足时的分析` | The method defines the death/SOFA ordering, the independent-analysis name, and the prohibition on calling it candidate-representation validation. |
| If core visit, randomization, center, survival, or hospital semantics cannot be verified, no new visit outcome analysis is conducted. | Method opening, independent-analysis subsection, trial table, evidence chain, outputs, risk table, section 14 authority paragraph | Each location gives the same overall stop and permits only original-endpoint reproduction or data audit where appropriate. |
| No stage-III result fills stage-II resource, simulation, primary-task, or external-test requirements. | Section 1 summary; section 5 conjunction and sequence; fifth evidence-chain support; planned output 5; section 14 item 6, risk table, and authority paragraph | Each says the downstream results do not count toward or make up stage-II requirements. |

### PCR-012 — explicitly unsupported claim classes

| Independent protected commitment | Revised body locator | Revised-dossier evidence |
|---|---|---|
| Observational data and prediction do not support a true causal network, treatment effect, counterfactual policy, mechanism, mediation, control, or digital twin. | `Core hypothesis and non-hypotheses`; section 14 `Limitations and boundary conditions`, item 9 | Both locators state the full boundary in direct scientific language. |
| Conditional randomized-trial reanalysis does not validate unmeasured latent dynamics, transition edges, or the whole candidate representation. | Structured-abstract contribution; method projection-summary interpretation; section 11 interpretation matrix; section 14 item 9 | Each preserves the limited visit-summary or independent clinical-state estimand and rejects system-level validation. |
| Current plan is not a validated model, clinical decision tool, drug platform, or unconditional clinical-promotion basis. | Section 1 positioning; section 14 item 9; Claim-Support table final row | The plan and current evidence states are kept prospective and the unsupported translational claim classes are marked `无支持`. |

## Compact concordance and first-use check

| Scientific or reader role | Single reader-facing name | First-use locator | Competing forms removed or reclassified | Whole-file result |
|---|---|---|---|---|
| Central object | `候选表征`, after the first full form `脓毒症全病程候选动态系统表征` | Section 1 one-sentence summary | `候选架构`, `候选系统表征`, `最小全病程候选表示`, and unscoped `整个系统模型` removed; `复杂候选模型` reserved for the optional implementation | All central-object uses checked; no removed form remains in reader prose |
| Primary tasks and outcomes | `未来 12 小时首次发病概率` and `第 7 日有利状态占用概率` | Section 5 WP3, fully specified in section 7 protocol table | Formula symbol CIF retained only after definition; no compressed project label introduced | Every task mention maps to one of the two tasks; stage-III endpoints are not called primary tasks |
| Secondary representation diagnostics | `伪遮蔽重建` and `未来轨迹诊断` | Section 5 WP3; section 7 `Secondary representation diagnostics` | Generic `两项次要任务` replaced with the two direct names where role resolution is needed | All occurrences retain diagnostic status and cannot substitute for primary tasks |
| Contingent trial branches and outcomes | `一维投影摘要（P_obs）` / `随机分组在该访视投影摘要上的差异`; `独立临床状态分析` | Section 7 frozen mapping and the two branch subsections | `投影可观测状态摘要`, `death-ranked`, `fallback`, `projection-pass`, and English trial-specific branch labels removed | All overview and authority locations preserve shared prerequisites, branch-specific eligibility, alternative branch, and overall stop |
| Resource or availability status | `已有公开资料支持`, `尚未核验`, `尚未生成`, `项目内衍生资料` | Section 6 resource-status introduction | English evidence-state strings removed | Resource table uses only the four defined Chinese states; none is used as claim-support status |
| External-test data and parameter-update state | `适配医院集`, `最终检验医院集`; four direct parameter-operation names | Section 7 `Hospital-primary cross-database validation` | All adaptation/test/untouched and zero/calibration/decoder/full-refit short forms removed | Every external-test occurrence identifies the data role, and every result states exactly which parameters are re-estimated |
| Model disposition | Direct statements such as `停止继续评价该复杂候选模型`, `转用多状态、线性或仅预测基线`, `停止结构解释`, `仅作数据库层面的描述` | Section 5 dated stages | Workflow metaphors such as downgrade, eliminate, advance, rescue, seal, firewall, no-go, fallback, and stop removed | Each disposition sentence states the stopped analysis, retained alternative, reportable output, and unsupported claim |

### Abbreviation and symbol first-use scan

| Item | First reader-facing definition | Check result |
|---|---|---|
| ICU | Section 1 summary: `公共重症监护病房（ICU）` | Defined before subsequent use |
| D7/D8 | Section 1 summary: `第 7 日（D7）或第 8 日（D8）` | Defined before branch overview use |
| SOFA | Section 1 summary: `序贯器官衰竭评估（SOFA）`; section 3 supplies the standard English full name and scientific context | Defined before use as an endpoint or branch condition |
| G1 | Section 5: `双数据库可观测性审计最低标准（G1）` with its function | No earlier G1 use in reader prose |
| CRF/SAP | Section 6 resource table: `病例报告表（CRF）` and `统计分析计划（SAP）` | Defined before use in trial-status and methods text |
| CIF | Section 7 protocol table: `累积发生函数（CIF）` | Used only for the defined first-onset estimand |
| R0/R1 | Section 7 headings give the full Chinese scientific names and functions | Later short labels point only to those definitions |
| P_obs | Section 7 frozen mapping: `基于实际 D7 或 D8 观测值计算的一维投影摘要（P_obs）` | Used only as the formula symbol for that quantity |

## Structural, branch, and mechanical checks

- Required H2 count: 15, in contract order.
- Section 3 H3 sequence: Background → Current state → Gap → Significance → Rationale, all non-empty.
- Evidence chains: 5 H3s; each has exactly one Input, Method / analysis / processing, Output, and Supports field, and no standalone limitation field.
- Claim-Support table: all seven contract dimensions retained; claim cells contain their own scope qualification; contribution and support states use natural Chinese.
- Frontmatter: `schema_version: research-idea.v3`; `plugin_version: 0.9.0-preview.3`; `change_type: editorial_repair`; one `based_on` mapping only, with v003 artifact ID, version, and path.
- Branch fidelity: every mandated overview and authority location has the same order—shared prerequisites first, projection-summary branch eligibility and outcome second, independent clinical-state branch eligibility and outcome third, overall semantic stop fourth, and no stage-III rescue of stage II.
- Protected-content coverage: exactly PCR-001 through PCR-012, no missing, duplicate, or unknown protected ID; each independent enumerated commitment above has a revised body locator and actual body wording.
- No section-14 pointer: the dossier does not use “see section 14” or an equivalent cross-reference; necessary local boundaries are self-contained.
- Structural linter command: `python research-skills-openai/skills/multi-path-idea-generator/scripts/lint_idea_dossier.py <v042 dossier> --expected-plugin-version 0.9.0-preview.3`.
- Structural linter result: `OK`.

## Unresolved items

No NRP-001..007 action, LNG-R059-001..009 finding, or PCR-001..012 preservation mapping remains unresolved within this editorial repair bundle. The two source scientific specifications that were already pending—clinical-scale-to-simulation-parameter mapping and the exact multiclass-calibration implementation/registry—remain explicitly pending in the dossier without a guessed value or method. Narrative/language readiness and scientific acceptance remain for fresh independent review.
