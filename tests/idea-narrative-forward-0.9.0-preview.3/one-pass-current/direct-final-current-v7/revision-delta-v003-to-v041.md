---
schema_version: research-idea-revision-delta.v1
plugin_version: 0.9.0-preview.3
artifact_id: revision-delta-I01-001-v003-to-v041
workflow_id: RID-SEPSIS-CSM-20260717-001
idea_id: I01-001
from_dossier_ref:
  artifact_id: idea-dossier-I01-001-v003
  version: v003
  path: tests/idea-test-0.9.0-preview.1/0.9.0-preview.1/03_ideas/nodes/I01-001/dossiers/idea-dossier-v003.md
to_dossier_ref:
  artifact_id: idea-dossier-I01-001-v041
  version: v041
  path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v7/idea-dossier-v041.md
change_type: editorial_repair_delta
frozen: true
---

# Revision delta: idea dossier v003 to v041

## Scope, lineage, and editorial boundary

- v041 is a complete editorial repair of v003. It preserves the primary question, objective, study object, evidence base, unit of inference, methods, thresholds, evidence states, contingencies, and claim strength.
- The dossier frontmatter binds `plugin_version: 0.9.0-preview.3` and contains exactly one `based_on` entry: the logical artifact ID, version, and path of v003.
- No method, data source, result, assumed value, scientific restriction, or stronger claim was inferred. Pending specifications remain pending, and no working assumption was created.
- This delta records text-grounded implementation and preservation evidence. It does not make a narrative, language, preservation, scientific, or overall readiness decision.

## Narrative repair action map

| Action | Operation completed | Revised body locator | Text-grounded acceptance evidence |
|---|---|---|---|
| NRP-001 | Replaced and reordered the combined background section into five reader functions | `Background, current state, gap, significance, and rationale` > the five ordered H3 subsections | `Background` defines the sepsis time and label-time problem; `Current state` states what databases and neighboring work can answer; `Gap` asks whether auditable, reconstructable and alignable patient-time states exist across databases; `Significance` explains why separating physiology from care and measurement policy matters; `Rationale` links dual clocks, role separation, simulation reconstruction, and the isolated final cross-database test to that gap. Stage III receives one concluding preview sentence only. |
| NRP-002 | Replaced the one-sentence summary and rebalanced every structured-abstract field | `Title, summary, audience, and positioning`; `Structured abstract` | The one-sentence summary has two parallel trunks separated by a semicolon: stage I–II study object/validation/deliverable, then the conditional two-trial extension and its alternative branch. Each abstract bullet now performs only its labeled function; the approach defines G1 and the two external data roles without reconstructing the full branch logic. |
| NRP-003 | Consolidated the complete stage III procedure into one technical authority subsection; reduced other sections to role-specific statements | `Research design and methods` > `条件性试验观测桥接与独立临床状态分析` | This subsection alone contains shared prerequisites, R0, the frozen mapping, R1, Branch A, Branch B, overall stopping, trial-specific missing/death handling, Holm multiplicity, and sparse-visit interpretation. The question, Objective 4, WP5, fifth evidence chain, planned output, contribution ladder, and claim-support table retain only their distinct question, objective, schedule, evidence, deliverable, or claim-audit functions. |
| NRP-004 | Removed the fifth limitations field from every evidence chain and consolidated the complete limitation inventory in section 14 | `Evidence chains`; `Feasibility, resources, risks, alternatives, and stop conditions` | Each of five chains contains exactly `Input`, `Method / analysis / processing`, `Output`, and `Supports`. Section 14 now contains feasibility/resources, the complete limitations and claim boundaries, a trigger/alternative/stop matrix, unresolved specifications, and the identity/overall stopping boundary. No pointer such as “see section 14” appears. |
| NRP-005 | Replaced a technique recap with an implementation map | `Key techniques and implementation` | The 10-row table names the implementation unit, accepted input, produced output, persistent audit/interface record, and freeze/version boundary for the dual-clock engine, G1 record, role registry, model pipeline, alignment registry, missingness/policy diagnostics, hospital split, trial bridge package, uncertainty/multiplicity specification, and negative-control/publication package. |
| NRP-006 | Assigned one authority function to each required H2 while preserving all required components | All 15 required H2 sections | Schedule and work packages contain time/dependency/deliverable consequences; data sections contain source and evidence status; methods contain complete estimands and thresholds; implementation contains objects and interfaces; chains contain four traceability fields; required analyses contain acceptance evidence; expected outputs contain products, falsification and interpretation; contribution and claim-support sections perform positioning and claim audit; section 14 holds the full limitation and stopping inventory. Complete reconstruction, external-split/update, and R0/R1 specifications each have one technical authority location. |
| NRP-007 | Defined cross-disciplinary terms at first reader-facing use and replaced unnecessary internal labels with direct scientific language | Summary; structured-abstract approach; first paragraph of primary-task methods; simulation subsection; external-validation subsection; conditional-trial subsection | First uses define `候选表征`, simulation reconstruction performance, G1, prediction time point, label-availability time, strictly proper scoring, the two external hospital sets and four parameter operations, one-dimensional projection summary `P_obs`, and the independent clinical-state analysis. Later uses retain those names without repeated definitions. |

## Language finding map

| Finding | Revised body locator | Operation and actual body evidence | Acceptance evidence |
|---|---|---|---|
| LNG-R059-001 | H1 and section 1 `Title`; all stage III summaries | Used the supplied title verbatim: `脓毒症全病程候选动态系统表征：计划开展跨数据库检验，并在满足预设条件时对随机对照试验的稀疏随访测量进行次要分析`. Other sections use grammatical equivalents in which the condition modifies initiation of the analysis and “稀疏” modifies follow-up measurements. | Whole-dossier scan found no `稀疏 RCT`, `实际稀疏 RCT 访视`, or `条件性稀疏 RCT`; H1 and `Title` are identical. |
| LNG-R059-002 | Section 1 one-sentence summary; Objectives 2–4; methods and interpretation | First use defines `脓毒症全病程候选动态系统表征（下称“候选表征”）`. `复杂候选模型` is restricted to the optional switching/nonlinear implementation; `阶段 II 冻结的候选表征` is restricted to the frozen output. | Whole-dossier scan found no competing `候选架构`, `候选系统表征`, `最小全病程候选表示`, or unbounded `整个系统模型/整个模型`. |
| LNG-R059-003 | Summary; `模拟与半合成重建判定标准`; post-onset state table | The clinical state is consistently `生理恢复状态`; simulation first use is `在已知生成机制下重建预设状态、转移和结构的性能` and then `模拟重建性能`; false confidence is written as `错误结构被高置信度支持的频率`. | Every occurrence of `恢复` in the scientific body belongs to `生理恢复状态`; simulation evaluation uses `重建`, and no `假置信` remains. |
| LNG-R059-004 | Month 4–6 row; R0 and R1 subsection headings | First use states `双数据库可观测性审计最低标准（G1）`; the trial subsections define `试验语义与共同生理锚点合格性标准（R0）` and `测量一致性、校准与投影重建误差标准（R1）`. Other criteria are named as standards, conditions, or decision points. | No bare scientific “gate” metaphor remains; G1/R0/R1 are used only after their full Chinese functional definitions, with every threshold and consequence retained. |
| LNG-R059-005 | Structured-abstract approach; external-database roles; `医院优先的跨数据库验证` | Uses only `适配医院集` and `最终检验医院集`. The latter is defined as not exposing outcomes or performance during development/adaptation. Four operations are: no parameter update; re-estimate calibration intercept/slope only; re-estimate observation-layer parameters only; refit the full model as redevelopment. | Whole-dossier scan found no `adaptation`, `untouched`, `zero-update`, `decoder adaptation`, `full refit`, or `transport updating`; every operation states which parameters change. |
| LNG-R059-006 | Conditional-trial mapping and Branch A/B subsections; fifth chain; outputs and interpretation | Defines `基于实际第 7/8 日观测值计算的一维投影摘要 P_obs`; Branch A result is `随机分组在该访视投影摘要上的差异`; Branch B is `独立于阶段 II 候选表征、按死亡和 SOFA 排序的试验特异性次要临床状态分析（下称“独立临床状态分析”）`. | Whole-dossier scan found no `death-ranked`, `fallback`, `projection-pass`, `trial-specific clinical-state`, or standalone “扰动” name. The two branch names do not cross roles. |
| LNG-R059-007 | Resource-status table; fourth evidence chain output; claim-support table; identity boundary | Resource states are `已有公开资料支持/尚未核验/尚未生成/项目内衍生资料`; transport results are `跨数据库稳定/仅适用于特定数据库/证据不足而不作解释`; claim states are `有支持/有条件支持/无支持`. Identity is described in ordinary Chinese. | Each table uses only its own status dimension. No reader-facing `verified/unverified/not generated/project-local derivative`, `stable/database-specific/abstained`, `supported/qualified/unsupported`, `identity_status`, or `new_idea_required` remains. |
| LNG-R059-008 | Dated decision table; simulation response table; external support rule; section 14 risk matrix | Every disposition says what stops, what is retained, and what can no longer be claimed, e.g. `停止继续评估复杂候选模型并转用多状态或线性基线` and `只作数据库层面的跨场景描述，不声称医院层面稳健`. | Whole-dossier scan found no `降级`, `淘汰`, `晋级`, `挽救`, `救回`, `豁免`, `封存`, `封印`, `防火墙`, `no-go`, or workflow-style `fallback/stop`. |
| LNG-R059-009 | One-sentence summary; R0; R1; required stage III evidence; closest-work conclusion | The summary retains one sentence with two main trunks. R0 and R1 use a definition sentence, single-purpose bullets, then one consequence paragraph. Stage III requirements are separated by semicolons according to evidence type. The closest-work conclusion uses three sentences for search result, coverage limit, and allowed positioning. | All numerical standards, branch consequences, search coverage, and evidence strength remain explicit without nested condition stacks. |

## Compact concordance and all-occurrence check

| Core reader role | One reader-facing name | First-use locator | Competing forms removed or reclassified | All-occurrence scan result |
|---|---|---|---|---|
| Central object | 候选表征 | Section 1 one-sentence summary: `脓毒症全病程候选动态系统表征（下称“候选表征”）` | `候选全病程表示`, `候选架构`, `候选状态表示`, `候选系统表征`, `最小全病程候选表示`, unbounded `整个系统模型` | Stable; optional implementation is separately named `复杂候选模型`, and the frozen output is explicitly `阶段 II 冻结的候选表征`. |
| Primary pre-onset task and outcome | 未来 12 小时首次发病累积发生函数 | `Research content and work packages` > WP3; fully defined in the two-task protocol table | Mixed `12h CIF`, `first-onset` and unlabeled risk shorthand | Stable Chinese name; the formula role is expanded in methods before abbreviated use. |
| Primary post-onset task and outcome | 第 7 日有利状态集合占用概率 | Structured-abstract approach, then the two-task protocol table | `日 7 状态占用`, `post-onset task` shorthand | Stable; `生理恢复状态` and `存活离开 ICU` are always separately reported. |
| Diagnostic analysis | 两项次要表征诊断 | Structured-abstract expected result; fully named in `次要表征诊断` | Generic `representation diagnostics` and mixed recovery wording | Stable; pseudo-masking and future-trajectory diagnostics remain separate and cannot substitute for primary tasks. |
| Contingent projection branch | 访视投影摘要分析 | `条件性试验观测桥接与独立临床状态分析` > `分支 A：访视投影摘要分析` | `投影可观测状态摘要`, `投影可观测摘要`, `RCT 可观测代理`, `death-ranked 投影摘要`, `projection-pass` | Stable; formula symbol `P_obs` appears only after definition. |
| Projection-branch outcome | 随机分组在该访视投影摘要上的差异 | `分支 A：访视投影摘要分析` final sentence | `状态扰动估计`, `访视特异扰动`, `有限随机化扰动`, `组间不同` | Stable in question, objective, fifth chain, output, interpretation, contribution and claim-support locations. |
| Alternative branch and outcome | 独立临床状态分析 | `分支 B：独立临床状态分析` definition | `独立 death-ranked SOFA`, `独立 SOFA 分支`, `trial-specific clinical-state`, `fallback` | Stable; every use states or inherits independence from stage II, and no use calls it a validation of the candidate representation. |
| Evidence and availability status | 已有公开资料支持 / 尚未核验 / 尚未生成 / 项目内衍生资料 | `Data, materials, and existing evidence base` > `当前资源与证据状态` | English machine status strings | Stable within the resource-status table; claim and transport status vocabularies remain distinct. |
| External-test data roles | 适配医院集 / 最终检验医院集 | Structured-abstract approach | `适配区`, `测试区`, `adaptation/test`, `untouched`, `未触碰 test` | Stable across data, schedule, methods, chains, evidence, outputs, interpretation and risks. |
| Parameter-update state | 不更新任何模型参数 / 仅重新估计校准截距和斜率 / 仅重新估计观测层参数 / 用目标数据库重新拟合全模型 | External-validation four-item list | `zero update`, `zero-update`, `calibration`, `decoder adaptation`, `full refit`, `transport updating` | Stable; abbreviated later uses preserve the same changed/frozen parameter set, and full refitting is always classified as redevelopment. |
| Model disposition | 停止继续评估复杂候选模型并转用多状态或线性基线 | Month 7–12 row; simulation response table | `自动降级`, `淘汰`, `准入`, `晋级`, `挽救`, `封存` | Stable direct-operation language; all occurrences identify the stopped analysis, retained analysis or reportable product, and unsupported claim. |

## Multi-branch fidelity check

### Shared prerequisites

- **Body locator:** `Research design and methods` > `条件性试验观测桥接与独立临床状态分析` > `共享前提与分试验设置`.
- **Body evidence:** the dossier states that stage II must be completed and frozen; individual-level authorization and original CRF/SAP/data-dictionary or data-holder confirmation must establish randomization, analysis set, center/strata, D7/D8 timing, and death/hospital/discharge/transfer semantics; each trial keeps its own anchors, mapping, thresholds, code and seed, all frozen before treatment-group comparison.
- **Preserved consequence:** `任何试验结果均不能补足阶段 II 未满足的资源、模拟重建、主要任务或跨数据库检验要求。`

### Branch A: visit projection-summary analysis

- **Eligibility:** R0 requires at least two G1-retained, directly observed, semantically/unit/time-consistent physiological anchors that are not treatment, measurement frequency, labels or derived states. R1 retains all six original classes of criteria: ≥50% first-axis energy, correlation ≥0.70, normalized MAE ≤0.50, intercept/slope and 95% coverage, per-anchor calibration, and blinded trial-range/computability support.
- **Mapping:** the body retains development-data standardization and percentile truncation, `Z_C=a_C+L_C X+e`, `L_C=UDV'`, `P_state=V_1'X`, `P_obs=D_1^(-1)U_1'(Z_C−a_C)`, dictionary-order tie resolution, SOFA-oriented sign, and the prohibition on trial-arm/outcome/pooled-data use.
- **Outcome and interpretation:** D7/D8 pre-visit death is worst, hospitalized survivors are ordered by P_obs, and pre-visit live discharge is best; the comparison is a center/stratum-compatible probabilistic index or win probability and is named only `随机分组在该访视投影摘要上的差异`.

### Branch B: independent clinical-state analysis

- **Eligibility:** if the shared-anchor part of R0 or any R1 criterion fails, but SOFA, death, hospital/discharge, randomization and center semantics remain verifiable, the branch remains available.
- **Outcome and interpretation:** death is worst, hospitalized survivors are ordered by SOFA high-to-low, live discharge is best; the dossier explicitly defines the analysis as independent of stage II and forbids calling it a difference in or validation of the candidate representation.

### Overall stop and trial separation

- **Overall stop:** if core D7/D8 timing, randomization, center, survival or hospitalization semantics cannot be verified, no new visit-outcome analysis is performed; only original-endpoint reproduction or data audit remains.
- **Trial-specific preservation:** the EXIT-SEP and XBJ-SCAP table retains all-randomized versus complete-outcome/FAS/mITT distinctions, actual D7/D8 visits, post-randomization D1/D0 restrictions, death/discharge ranking, multiple imputation, Rubin/cluster bootstrap, ±0.5/±1 SD and best/worst tipping analyses, bounds for transfer/unknown state, structural non-imputation, Holm FWER 0.05, exploratory FDR, and interaction-only subgroup reporting. The trials remain separate and sparse visits are not interpolated into continuous trajectories.

## Protected-content preservation map

Every item below cites revised dossier words or a precisely named table row. Delta assertions alone were not used as evidence.

### PCR-001 — identity and core question

1. **Sepsis-centered full continuum:** Section 1 summary states `覆盖脓毒症发病前在险时段、首次发病、发病后互斥状态演化和结局`; the mutually exclusive state table enumerates persistent sepsis, physiological recovery, deterioration/new organ failure, live ICU exit, transfer/loss and death.
2. **Dynamic complex-system representation identity:** the H1 and section 1 title retain `脓毒症全病程候选动态系统表征`; the primary question asks whether this representation can cover and be tested across the continuum.
3. **Not ordinary prediction or generic ICU stratification:** section 14 identity boundary states that shrinking the study to ordinary prediction requires separate evaluation as a new research idea; the section 3 gap remains a patient-time state/transition and cross-database reconstruction question rather than generic risk stratification.

### PCR-002 — primary objective and deliverables

1. **Twenty-four-month stage I–II objective with knowledge constraints, public ICU data, system identification and cross-database/full-course validation:** section 1 summary, Objectives 1–3, the dated table and WP1–WP4 jointly retain the 24-month objective, literature/expert priors, MIMIC-IV/eICU, anchoring/system-identification design, full-course tasks and final cross-database test.
2. **High-level paper and auditable scientific evidence:** section 1 summary states `形成可审计的阶段 I–II 科学证据和高水平论文方向`; Planned output 6 and section 14 feasibility repeat the deliverable as a paper-facing evidence package and reusable resource.
3. **Not prediction-tool-only:** section 14 identity boundary says `把研究收缩为普通预测` requires a new idea; the contribution ladder requires simulation reconstruction, task validity, state alignment and cross-database evidence beyond prediction output.

### PCR-003 — study object, scope, and unit of inference

1. **Study object and scope:** section 1 summary and the primary question retain the longitudinal sepsis-centered ICU system, including comparable pre-onset at-risk intervals and post-onset trajectories.
2. **Unit of inference:** section 1 positioning states `以患者—时间状态和状态转移为推断单位`.
3. **Clustering:** the two-task protocol table preserves patient- and hospital-level bootstrap, and overlapping pre-onset time points keep total hospitalization weight 1 with patient/hospital clustering.

### PCR-004 — public ICU inputs and present status

1. **Irreplaceable inputs:** section 14 feasibility states `核心输入为文献与专家先验、MIMIC-IV 和 eICU-CRD 的纵向公共 ICU 数据`.
2. **Conditional backup:** the same paragraph and the public-database roles subsection retain pre-specified HiRID or AmsterdamUMCdb as the conditional backup.
3. **Verified existence/version only:** the resource table marks MIMIC-IV/eICU existence, versions and literature as `已有公开资料支持`.
4. **Access/DUA/extract/cohort support/named staff/results remain unverified or ungenerated:** separate resource-table rows state `尚未核验` for credentials, DUA, extract, personnel and trial semantics, and `尚未生成` for G1 counts and all model/simulation/external/trial results. The evidence column explicitly says database existence does not prove team access or an executable risk set.

### PCR-005 — conditional randomized-trial inputs

1. **Only potential stage III sources:** section 14 feasibility states that EXIT-SEP and XBJ-SCAP are potential data sources only after stage II and only if individual data and original semantics are verifiable.
2. **Local material remains derivative:** the resource table classifies both local reports as `项目内衍生资料`.
3. **No substitution for authorization or original semantics:** the resource table and local-trial subsection explicitly state that those reports do not replace individual-level authorization, original CRF/SAP, randomization, center, visit timing, or death/hospital/discharge verification.

### PCR-006 — staged design, role separation, and interpretation constraints

1. **Full ordered design:** the `minimum route` sentence retains resource/G1 → labels/states/hospital split → simple baselines → simulation reconstruction and false-structure checks → at most one complex model → two primary tasks and two diagnostics → development freeze → final cross-database test → conditional trial analysis.
2. **State/action/observation separation:** section 1 positioning, section 3 rationale, the variable-role table and the observational target retain separate X/Y physiology, A treatment, M observation, label-only and baseline roles.
3. **Anchoring and alignment constraints:** the observational-target subsection preserves two anchors per dimension, +1 first loading, scale, cross-loading restrictions, K≤4, regime≤3, one/two-bin lags, no instantaneous cycle, 20 seeds and permutation/sign alignment; only aligned occupancies, transitions, anchor predictions and prespecified sign/lag invariants are interpreted.
4. **All five disposition thresholds:** the final paragraph of that subsection preserves alignment across 20 seeds <90%, bootstrap retention <80%, external sign agreement <80%, state alignment <0.70, or uncalibrated intervals.
5. **Required responses:** the same sentence requires deletion, merging, or an explicit database/care-policy-specific label.
6. **No prediction override:** it ends `较好的预测表现不能改变这些操作`.

### PCR-007 — conjunctive stage II success and external parameter handling

1. **Conjunctive success components:** the five-item `阶段 II 合取成功定义` retains data support; simulation reconstruction and false-structure control; both primary tasks' Brier/proper-score and calibration; zero high-severity leakage; no-parameter-update final external performance; state alignment; and structural sign consistency.
2. **No-update evidence is primary:** external-validation operation 1 names `不更新任何模型参数` as the primary external test.
3. **Limited updates separate:** operations 2 and 3 separately re-estimate calibration intercept/slope and observation-layer parameters from the adaptation hospitals while keeping other parameter blocks frozen.
4. **Limited updates cannot substitute:** conjunctive item 5 states `由适配医院集重新估计参数后的结果不能替代这一项`; the interpretation matrix limits them to adapted applicability.
5. **Stage III cannot complete stage II:** the paragraph after the five conjunctive criteria states `阶段 III 永不计入或补足阶段 II 的合取成功`.

### PCR-008 — primary-task clocks, estimands, states, and leakage control

1. **Two primary tasks:** the protocol table preserves future-12-hour first-onset cumulative incidence and day-7 favorable-state occupancy, with separate reporting of physiological recovery and live ICU exit.
2. **Event and availability clocks:** the first methods paragraph defines prediction time and label-availability time; table rows separately preserve event clock and availability clock.
3. **First-onset risk set and delayed entry:** population and repeat rows retain exclusion of baseline-onset cases from the pre-onset task, incident onset, auditable delayed entry, stratification and left truncation without back-calculating onset.
4. **Mutually exclusive post-onset states and competing termination:** the fixed priority and six-row state/event table retain death, transfer/loss, live ICU exit, deterioration/new organ failure, physiological recovery and persistent sepsis; competing/intercurrent rows retain death, discharge and transfer treatment.
5. **Time-point-available features, scoring and clustered uncertainty:** the table requires feature availability before the prediction time, uses Brier/multicategory Brier and calibration, and retains patient/hospital bootstrap.
6. **Specimen–antibiotic pairing:** the pre-onset event-clock cell retains specimen-first medication within 72 hours and medication-first specimen within 24 hours, with the earlier event as infection time.
7. **Baseline SOFA:** the same cell retains baseline SOFA=0 when no chronic dysfunction is recorded; otherwise the lowest computable SOFA in the 24 hours before ICU, with unauditable cases excluded from the main risk set.
8. **Rolling window and first sortable onset:** the same cell retains worst components over a rolling 24 hours, relative SOFA +2 within infection −48/+24 hours, and the first sortable qualifying time as onset.
9. **First onset and overlapping time points:** the repeats row retains first onset only and total weight 1 per hospitalization for overlapping prediction points.
10. **Within-bin action/state order:** the same-time-period row retains `[t,t+12h)` actions as A_t, next-boundary measured physiology as next state, and exclusion of unsortable same-timestamp edges.
11. **Leakage checks:** the paragraph after the table explicitly checks post-onset physiology/treatment, unavailable culture/antibiotics, same-period actions, future measurement frequency, cross-split imputation/standardization, patients or ICU stays crossing sets, overlapping-window weights, and outcome-driven variables, time grids or thresholds.

### PCR-009 — planned evidence and claim strength

1. **No completed model or new result:** the resource table marks current candidate models, simulation reconstruction, prediction, cross-database and randomized-trial results `尚未生成`; the abstract says all outputs are planned.
2. **Conditional contribution only:** section 1 positioning, the contribution ladder and claim-support table describe evidence integration, validation, benchmark/resource and governance value at conditional scope.
3. **Modules have precedent:** the closest-work table and summary cite [26-37] and state that each module has high-confidence precedent.
4. **Combination gap is low-to-moderate confidence:** the three-sentence closest-work conclusion retains that evidence strength and the incomplete search coverage.
5. **No global-first or new-algorithm claim:** claim-support rows mark both as `无支持`; section 14 prohibits those claims.

### PCR-010 — authoritative limitations, risks, unresolved specifications, and trial inconsistency

1. **Single global authority:** section 14 contains the complete resource/access, staff, G1 support, label/leakage, reconstruction, nonrandom missingness/overlap, no-parameter-update external validation, timing, trial data/semantics, common-anchor/mapping, closest-work, claim-boundary and regulatory limitations.
2. **Every trigger has an alternative and stop consequence:** the four-column risk matrix gives `触发条件`, `保留的替代分析或产物`, and `停止的分析或不能支持的主张` for access, cross-hospital links, leakage, reconstruction, missingness/overlap, external performance, trial bridge, trial semantics, inconsistent trials, timing and closest-work overreach.
3. **Clinical-scale-to-simulation mapping remains pending:** `尚未解决的执行规格` explicitly lists `临床尺度到模拟参数的映射`.
4. **Exact multicategory calibration estimator, confidence bound, and threshold registry remain pending:** the same paragraph lists `精确的多类别校准估计量、置信界和阈值登记表`.
5. **Screening thresholds are not empirical adequacy:** the paragraph states `用于筛选的事件或参数下限不能替代经验有效样本量和模拟稳定性`.
6. **Inconsistent or imprecise trials:** the risk row `两项试验方向不一致或区间过宽` retains separate reporting of no support or limited cross-context applicability and explicitly says not to select a subgroup to alter the overall conclusion.

### PCR-011 — phase boundary and mutually exclusive trial branches

1. **24-month minimum and later stage III:** section 5 opening and section 14 feasibility state that stage I–II must finish within 24 months and stage III lies outside the minimum deliverable.
2. **Shared prerequisites:** the stage III technical subsection requires completed/frozen stage II, available individual data, and verifiable core trial semantics.
3. **Bridge-qualified branch:** Branch A occurs only when R0 and R1 are both satisfied and analyzes the visit projection summary derived from the frozen stage II mapping.
4. **Alternative branch remains available:** Branch B occurs when the bridge fails but SOFA and core trial semantics remain verifiable, and is explicitly independent of the stage II candidate representation.
5. **Overall stop:** the `Overall stop` paragraph says that unverifiable D7/D8 timing, randomization, center, survival or hospital semantics means no new visit-outcome analysis.
6. **No stage III compensation:** shared prerequisite 1 and the section 14 overall boundary state that trial results cannot complete unmet stage II resource, simulation, primary-task or cross-database requirements.

### PCR-012 — unsupported claim classes

1. **Observational and predictive boundaries:** section 14 limitations state that observational modeling, measurement-process modeling, negative controls and time reversal do not identify nonrandom-missing truth, treatment causal effects, a true feedback network, counterfactual policy, mechanism or mediation.
2. **Control and digital-twin boundaries:** the same list and the interpretation matrix exclude control and digital-twin conclusions.
3. **Randomized-trial boundary:** section 14 states that either trial branch cannot validate unmeasured latent dynamics, transition edges, the complete candidate representation, treatment mechanism, control or a digital twin.
4. **No completed product or unrestricted promotion:** section 14 states that the plan cannot be written as a validated model, clinical decision tool, drug platform or basis for unconditional clinical promotion; it also retains the SSC 2026 caution for XueBiJing.[4]

## Reopened-locator evidence check

After drafting, the following revised authority locations were reopened and compared with every enumerated element claimed above:

- section 1 title, summary, audience and positioning;
- all five H3 functions in section 3;
- the complete dated table, conjunctive success list, work-package table and minimum route;
- the resource-status table, G1 audit table, variable-role table and both local-trial evidence paragraphs;
- the complete two-task protocol table, state/event table, observational/anchoring paragraph, simulation table, hospital split/update rules, and all stage III branch subsections and trial rows;
- all five four-field evidence chains;
- planned outputs, falsification criteria and interpretation matrix;
- contribution ladder, closest-work table and claim-support table;
- every section 14 limitation bullet, risk row, unresolved specification and identity/overall stopping sentence.

The dossier body contains the cited values, statuses, operations, alternatives and claim boundaries at those locations; no preservation claim relies only on this delta.

## Mechanical and consistency checks

- Dossier linter: `OK` with expected plugin version `0.9.0-preview.3`.
- Structure: one H1; exactly 15 required non-empty H2 headings in contract order; exactly five ordered non-empty H3 functions under section 3.
- Evidence chains: five chain H3 headings; each has exactly one `Input`, `Method / analysis / processing`, `Output`, and `Supports`, with no fifth limitations field.
- Claim-support table: seven required columns, reader-language contribution frames and support states, and no separate repeated-qualifier column.
- Lineage: one `based_on` mapping only, containing v003 artifact ID, version, and exact path.
- Branch check: shared prerequisites, Branch A eligibility and outcome, Branch B eligibility and outcome, and overall stop are all separate; both trial rows and nonpooling rules remain present.
- Whole-dossier terminology scan: no prohibited competing title, object, external-data, parameter-update, trial-branch, machine-status, model-disposition or workflow-metaphor forms listed in LNG-R059-001..008 remain in reader-facing scientific text.
- Planned-versus-observed scan: planned work remains prospective; all current unverified and ungenerated states remain explicit.
- Readiness language scan: the dossier and delta contain no self-assigned narrative, language, preservation, scientific, evaluation, promotion, or overall readiness verdict.

## Unresolved items

- **Editorial findings:** none left unresolved in this writer pass; NRP-001..007 and LNG-R059-001..009 each have revised body evidence above.
- **Protected content:** no protected commitment was intentionally changed or omitted; PCR-001..012 each has item-level revised-body evidence above.
- **Scientific/execution items:** all pre-existing unresolved access, staffing, G1, parameter-mapping, calibration-estimator/threshold-registry, model-result, external-result, trial-authorization/semantics, common-anchor, and R0/R1 items remain unresolved in section 14. No answer was inferred for them.
- **Independent decisions:** narrative, language and content-preservation reassessment remain the responsibility of fresh independent reviewers; this writer makes no decision on them.
