---
schema_version: research-idea-revision-delta.v1
plugin_version: 0.9.0-preview.3
artifact_id: revision-delta-I01-001-v003-to-v025
workflow_id: RID-SEPSIS-CSM-20260717-001
idea_id: I01-001
source_artifact:
  artifact_id: idea-dossier-I01-001-v003
  version: v003
  path: tests/idea-test-0.9.0-preview.1/0.9.0-preview.1/03_ideas/nodes/I01-001/dossiers/idea-dossier-v003.md
target_artifact:
  artifact_id: idea-dossier-I01-001-v025
  version: v025
  path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/accepted/idea-dossier-v025.md
change_type: editorial_repair_delta
repair_plan:
  artifact_id: narrative-repair-plan-r014
  version: r014
  path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/baseline/narrative-repair-plan-r014.yaml
language_assessment:
  artifact_id: language-assessment-I01-001-r035
  version: r035
  path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/baseline/language-assessment-r035.md
protected_content_register:
  artifact_id: protected-content-register-I01-001-v003
  version: v003
  path: tests/idea-narrative-forward-0.9.0-preview.3/run-001/inputs/protected-content-register.yaml
writer_self_check_only: true
independent_reassessment_claimed: false
---

# Revision delta: v003 to v025

v025 是直接以 v003 为科学内容源完成的一次集中 editorial repair。修改只重排、定义、拆分、合并、删除重复或增加逻辑桥接；没有新增数据、方法、结果、证据、数值阈值或科学选择。本记录只报告 writer 的逐项执行与机械自检，不声称已通过独立 narrative assessor、language assessor、content-preservation reviewer 或 idea evaluator。

## Narrative repair actions and acceptance evidence

| Action | Findings | Operation | Exact v025 locator | Text-grounded revision evidence | Re-run acceptance evidence |
|---|---|---|---|---|---|
| NRP-001 | NAR-001 | split / reorder / add_bridge | `Background, current state, gap, significance, and rationale`, lines 44–64 | lines 46, 50, 54, 58 and 62 contain the exact ordered H3 headings `Background`, `Current state`, `Gap`, `Significance`, `Rationale`; Significance states that closing the gap enables whole-course representation, separates three evidence levels, improves reproducibility and guides later trial research; Rationale maps dual clocks, process separation, recovery experiments, independent external testing and conditional trial mapping to the preceding gap | Mechanical heading scan returned exactly five non-empty H3 in the required order. Each subsection has a unique function: problem basis, current evidence, unanswered question, value, and design response. Significance contains no method inventory, and each major rationale item names the gap it addresses. |
| NRP-002 | NAR-002 | replace / delete / reorder | `Title, summary, audience, and positioning > One-sentence complete-Idea summary`, line 32 | The sentence begins with the whole-course sepsis system and 24-month public-ICU construction/validation, then uses one conditional clause for trial secondary analysis; it contains no algorithmic failure branch, database or trial proper name, or undefined workflow label | Isolated sentence check: one grammatically complete sentence and one terminal Chinese full stop; reader can identify object, core validation route, 24-month boundary and conditional trial extension without later definitions. |
| NRP-003 | NAR-002 | reorder / replace / move | `Structured abstract`, lines 36–42 | The five items now proceed from current knowledge and unanswered gap with significance, to objective and falsifiable hypothesis, overall design, planned outputs, then positive contribution; detailed thresholds and alternative algorithms occur only in later technical sections | Each of the five items independently states its rhetorical function. A sequential read yields problem, current state, gap, value, rationale, intended outputs and contribution without requiring G1, zero-update or projection labels. All outputs remain explicitly planned. |
| NRP-004 | NAR-003, NAR-004 | consolidate / delete / move | `Feasibility, resources, risks, alternatives, and stop conditions`, lines 409–440 | lines 411–421 give a single self-contained set of working assumptions and complete limitations; lines 423–436 give every trigger, bounded alternative and consequence; lines 438–440 retain identity, 24-month boundary and stage relationship | A whole-document search found no cross-section pointer such as “see section 14”. The full grouped lists of data/access, identification, leakage, missingness/overlap, external validation, trial data/mapping, causal interpretation, closest-work, time and personnel limitations occur together only here. Outside this section, retained boundaries are short and directly define an adjacent estimand, decision or data status. |
| NRP-005 | NAR-003 | delete | `Evidence chains`, lines 288–323 | Five chains occur at lines 290, 297, 304, 311 and 318; every chain contains only `Input`, `Method / analysis / processing`, `Output` and `Supports` | Mechanical field count returned five instances for each required field and zero instances of `Limits and failure conditions`; no chain-level fifth field or cross-section pointer remains. Inputs, processing, planned outputs and supported objective are retained for all five chains. |
| NRP-006 | NAR-004 | consolidate / delete | `Required analyses and evidence`, lines 325–338 | Eight stage-II bullets now name checkable records or outputs; the trial paragraph names authorization, semantic verification, mapping specification and analysis-rule records without reproducing algorithms or failure matrices | Every list item denotes an inspectable artifact, table, test result, record or specification. Date sequence remains in lines 85–120, algorithms remain in lines 183–272, observable falsification remains in lines 351–359, and complete limitations remain in lines 411–440. No new cross-section limitation pointer was added. |

## Language findings and acceptance evidence

| Finding | Severity | Operation | Exact v025 locator | Text-grounded revision evidence | Re-run acceptance evidence |
|---|---|---|---|---|---|
| LA-R035-001 | major | replace / reorder / delete | line 32 | “本研究拟在 24 个月内……构建并跨数据库验证……；只有在……满足预设分析条件后，才开展……分试验次要分析” supplies one clear main clause and one subordinate conditional extension | The sentence contains one terminal full stop, preserves whole-course scope, 24-month core, cross-database validation and conditional trial role, and omits technical thresholds, named datasets, failure algorithms and grouped caveats. |
| LA-R035-002 | major | replace / define / split | lines 68, 77, 250–260 | The primary question says “由这些访视指标计算的低维状态摘要”; lines 256 and 258 separately define the mapping, its outputs `P_state` and `P_obs`, and “摘要与阶段 II 状态表示的一致程度” | Reader-role check at title, abstract, question and first method definition: mapping is the predetermined transformation, output is the visit-state summary, and consistency is the separately evaluated relationship. No use of `观测投影` or `投影可观测` remains. |
| LA-R035-003 | major | replace / define / delete | lines 38–42, 46–64, 85–120, 275–286, 340–371 | Workflow metaphors were replaced by actions such as “预先规定的模拟恢复标准”, “未参与模型开发或参数调整的另一数据库测试集”, “未满足标准时改用较简单模型”, “预先区分变量用途” and “按医院隔离外部测试” | Whole-text scan found zero standalone uses of `门`, `冻结`, `降级`, `防火墙`, `封印` and `未触碰` in reader prose. G1 is first defined at line 92 as “双数据库可观测性与样本支持核验（G1）”. |
| LA-R035-004 | major | replace / reattach modifiers | title lines 27 and 31; summary line 32; objective line 77 | Title says “预设条件满足后使用随机试验稀疏访视数据开展的次要分析”; objective states that the analysis occurs only after public-data validation and trial semantics satisfy conditions | Modifier parse is unique: conditions modify whether analysis is undertaken, randomized trial specifies the data source, sparse modifies visit data, and secondary modifies analysis. Stage III is not written as a fixed component of stage II. |
| LA-R035-005 | major | replace / define / consolidate | lines 104, 175–179, 250–268, 318–323 | line 104 defines `proper scoring rule`; lines 177 and 179 introduce D1/D4/D7 and D0/D4/D8 as trial-specified visits and preserve their unverified temporal reference; lines 260–264 define the low-dimensional-summary estimand, the independent death/SOFA/discharge clinical state and the full randomized analysis set in Chinese | Focused term scan found no `death-ranked`, `fallback`, `projection-pass`, `fidelity`, `all-randomized` or `mITT`. Necessary symbols and probabilistic index receive adjacent functional definitions; uncertain visit timing remains explicitly pending CRF/SAP verification. |
| LA-R035-006 | major | consolidate / delete | lines 411–421, with local estimand definitions at lines 214–220 and 250–268 | The complete causal, control, digital-twin, trial-evidence and current-status boundaries are stated once in the authority section; earlier sections use only the minimum boundary required to define an adjacent estimand or stage relation | Semantic-cluster check found no repeated full prohibited-claim list outside lines 411–421 and no cross-section pointer. The observational target at line 216 and trial estimand at line 260 retain only the local distinction needed to avoid changing what is estimated. |
| LA-R035-007 | minor | define | line 48, then lines 74 onward | First reader-facing occurrence is “重复设定的动态预测时点（landmark）”; later uses retain the defined short form | The first occurrence distinguishes prediction time from history window, prediction window and outcome without a backward or forward lookup. |
| LA-R035-008 | minor | replace / consolidate | lines 50 and 387–397 | The prose now uses “与本研究最接近的既有研究” and the heading `Representative related-work comparison`; confidence and search boundary remain explicit at line 397 | No reader-facing use of “最近近邻” remains. `closest-work` appears only in the contract-fixed H2 heading and the cited project artifact title, not as a prose label for literature comparison. |
| LA-R035-009 | major | split / replace / define | lines 236–248, 311–316, 355–367, 404 | line 248 gives four distinct roles: “不更新模型参数的外部验证”, “仅……重新校准”, “仅……更新观测模型”, and “完整重新拟合或重新开发模型”; lines 365–367 describe failure and limited-update results without reusing a common ambiguous root | Every former transport/zero-update instance maps to exactly one role. `zero-update validation` appears only once after its complete Chinese definition;正文没有使用“运输/运输性”概括不同操作，正式文献题名保持原题。 |

## Replacement-term and modifier self-audit

| Term or construction introduced in v025 | Reader baseline and role | Evidence or reason for use | Attachment and consistency check | Result |
|---|---|---|---|---|
| 候选动态复杂系统模型 | Cross-disciplinary researchers understand a planned dynamic-system model; “候选” carries evidence status | Direct descriptive expression already supported by v003 identity anchor; not a new branded label | “候选” modifies model, while “动态复杂系统” describes the modeled system and its representation | retained |
| 低维访视状态摘要 | Readers understand a summary calculated from measurements at a specified trial visit | Directly describes the output of the preserved SVD formula; avoids replacing one coined term with another compressed metaphor | Always denotes `P_obs`; mapping and consistency are named separately | retained with first definition at line 256 |
| 阶段 II 状态得分 | Readers can recognize a scalar derived from the stage-II state representation | Directly describes `P_state=V_1'X`; no claim that the latent state is observed | Always denotes `P_state` and is not used for the RCT measurement summary | retained with first definition at line 256 |
| 摘要与阶段 II 状态表示的一致程度 | Readers can identify an evaluated relationship rather than an object | Direct description of preserved correlation, NMAE, calibration and coverage criteria | “一致程度” applies only to the relation between `P_obs` and `P_state`, not to the mapping or summary | retained at line 258 |
| 不更新模型参数的外部验证 | Readers know the model is evaluated in another database without parameter estimation there | Directly names the primary external-validation operation | “不更新模型参数” modifies validation; limited updating and full redevelopment have separate names | retained; optional English appears once after definition |
| 预留适配集上的重新校准 / 只更新观测模型 / 完整重新拟合或重新开发 | Readers can distinguish three target-database operations | Direct descriptions preserved from v003; no shared compressed root | Each phrase names one and only one operation | retained consistently |
| 预设条件满足后使用随机试验稀疏访视数据开展的次要分析 | Readers know randomized trials, visits and secondary analysis | Descriptive title construction required by LA-R035-004 | “预设条件满足后” modifies开展, “随机试验” specifies source, “稀疏” modifies访视数据, “次要” modifies分析 | retained |
| 双数据库可观测性与样本支持核验（G1） | Readers need a concise repeat label only after a full first definition | The process is repeatedly used and its complete function is known from v003 | First definition occurs before subsequent G1 uses in reader prose | retained |
| probabilistic index | Method-aware readers may know the term; other target readers need its estimand | Standard method name retained with a direct Chinese functional definition at line 260 | The definition states the pairwise probability and tie handling role; no new compressed translation introduced | retained with definition |

## Protected-content disposition

| Protected item | Required disposition | Exact v025 locator | Item-level text-grounded preservation evidence |
|---|---|---|---|
| PCR-001 | retained_same_meaning | frontmatter lines 18–22; summary line 32; primary question line 68; identity lines 438–440 | v025 retains the sepsis-centered continuum from not-yet-onset through first onset and post-onset evolution to recovery, persistent sepsis, deterioration or organ failure, ICU discharge or death; line 440 explicitly excludes conversion to a post-onset prognosis study or generic ICU risk model. |
| PCR-002 | retained_same_meaning | positioning line 34; objectives lines 72–77; work plan lines 83–120; outputs lines 342–349 | The core remains literature/expert-informed system construction, public-ICU system identification and cross-database validation within 24 months; line 34 and output 6 retain high-level papers, reproducible evidence and reusable resources rather than a prediction tool alone. |
| PCR-003 | retained_same_meaning | frontmatter lines 20 and 22; primary question line 68; observational target lines 214–220 | Study object remains the longitudinal sepsis-centered ICU system including comparable pre-onset risk intervals and post-onset trajectories; the unit remains patient-time state and transition with patient and hospital clustering. |
| PCR-004 | retained_same_status | lines 126–163 | MIMIC-IV and eICU-CRD remain primary public databases, with HiRID or AmsterdamUMCdb as a preselected conditional backup; database existence is verified while credentials, DUA, runnable extract, cohort support, named staff and results remain unverified or not generated. |
| PCR-005 | retained_same_status | lines 130–132, 175–179, 250–268 and 413–419 | EXIT-SEP and XBJ-SCAP remain conditional individual-level trial sources; local reports remain derivative and cannot substitute for authorization, original CRF/SAP, randomization, center, visit timing or survival and disposition semantics. |
| PCR-006 | retained_same_meaning | lines 85–120 and 181–272 | Sequence remains resources and support → labels/states/hospital split → simple baselines → absolute recovery and false-structure checks → at most one complex candidate → two primary and two secondary tasks → completed development plan → independent external test → conditional trial work; state, action and observation processes remain separate. |
| PCR-007 | retained_same_meaning | lines 98–108 and 236–248 | Stage-II success remains conjunctive across data support, absolute recovery, two primary tasks, proper score and calibration, leakage control, external testing without parameter updating, state alignment and structural stability; finite adaptation is separately reported and stage III does not count toward stage-II success. |
| PCR-008 | retained_same_meaning | lines 183–212, especially 188–199 | Full protocol detail is retained: specimen/antibiotic pairing uses 72 hours after specimen or 24 hours after antibiotic; baseline SOFA and rolling 24-hour components define the first sortable onset; only first onset is analyzed; overlapping landmarks sum to weight 1 per stay; delayed entry, mutually exclusive states, competing endpoints, as-of constraints, cluster uncertainty and proper-score/calibration targets remain; line 193 preserves within-bin A_t/next-state ordering and excludes unordered same-timestamp edges; line 199 checks same-bin treatment, future measurement frequency, repeated stays and outcome-driven grid or thresholds. |
| PCR-009 | retained_same_strength | abstract lines 38–42; evidence status lines 126–136; contribution lines 373–397; limitations lines 411–421 | All model, simulation, external-validation and trial results remain planned or not generated; contribution remains conditional integration, validation and reusable benchmark/resource value; each module has prior work, and the combined-gap statement remains a bounded-search finding with low-to-moderate confidence rather than a first or global absence claim. |
| PCR-010 | retained_once_at_authority_location | complete authority lines 409–440 | Working assumptions and complete limitations cover resources/access, team commitment, G1 support, labels/leakage, recoverability, MNAR/overlap, external testing, timing, trial data/semantics, common anchors/mapping and related-work uncertainty; the risk table preserves every trigger, bounded alternative and stopping consequence. |
| PCR-011 | retained_once_at_authority_location | lines 417 and 438–440 | Stage I–II remains due within 24 months; stage III lies outside the minimum deliverable and requires stage-II success plus supported trial data, semantics and mapping; line 440 states it cannot bypass or repair resource, recovery, primary-task or external-validation failure. |
| PCR-012 | retained_same_boundary | lines 419 and 438–440 | The complete authority states that observational data and prediction do not identify causal networks, treatment effects, counterfactual policy, mechanism, mediation, control or a digital twin, and trial secondary analysis does not validate unmeasured dynamics, transition edges or the whole model; the plan is not presented as a validated model, clinical tool, drug platform or unconditional recommendation. |

## Writer mechanical checks

- Required structure: 15 H2 headings retained.
- Reader chain: section 3 contains exactly five non-empty H3 headings in the required order.
- Evidence chains: exactly five chains; each contains exactly the four required fields and no fifth limitation field.
- Summary: one grammatically complete sentence with one terminal full stop; no database or trial proper names, detailed failure algorithm or grouped limitation list.
- Terminology: proposed replacements and newly introduced expressions were checked for reader baseline, evidence need, modifier attachment and consistent role; ambiguous projection and transport word families are absent from reader prose.
- Limitation authority: complete limitations appear once in section 14; no cross-section pointer was added.
- Scientific content: all PCR-001 through PCR-012 have an item-level v025 locator and preservation evidence.
- Evidence status: v025 does not state or imply that an independent assessment, content-preservation review or idea evaluation has passed.
