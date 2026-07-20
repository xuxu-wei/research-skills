---
schema_version: research-idea-revision-delta.v1
plugin_version: 0.9.0-preview.3
artifact_id: revision-delta-I01-001-v003-to-v021
workflow_id: RID-SEPSIS-CSM-20260717-001
idea_id: I01-001
version_id: v021
path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/revised/revision-delta-v003-to-v021.md
source_dossier:
  artifact_id: idea-dossier-I01-001-v003
  version: v003
  path: tests/idea-test-0.9.0-preview.1/0.9.0-preview.1/03_ideas/nodes/I01-001/dossiers/idea-dossier-v003.md
revised_dossier:
  artifact_id: idea-dossier-I01-001-v021
  version: v021
  path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/revised/idea-dossier-v021.md
based_on:
  - artifact_id: idea-dossier-I01-001-v003
    version: v003
    path: tests/idea-test-0.9.0-preview.1/0.9.0-preview.1/03_ideas/nodes/I01-001/dossiers/idea-dossier-v003.md
  - artifact_id: narrative-repair-plan-r014
    version: r014
    path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/baseline/narrative-repair-plan-r014.yaml
  - artifact_id: language-assessment-r020
    version: r020
    path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/baseline/language-assessment-r020.md
  - artifact_id: protected-content-register-I01-001-v003
    version: v003
    path: tests/idea-narrative-forward-0.9.0-preview.3/run-001/inputs/protected-content-register.yaml
source_skill: multi-path-idea-generator
change_type: editorial_repair_delta
identity_status: preserved
scientific_change: false
---

# Revision delta: idea dossier v003 to v021

## Scope and disposition

This editorial repair preserves the research identity, evidence base, scientific commitments, evidence status, numerical and temporal rules, analysis-handling rules, conditional branches, and claim boundaries of v003. It changes reader order, terminology, sentence structure, repetition, and the location of limitation and contingency statements. The revised dossier is a complete artifact; this delta is lineage and acceptance evidence only.

No new evidence, result, method value, threshold, data field, or claim class was introduced. All planned work remains described as planned. Section 14 is the sole complete authority for limitations, working assumptions, operational alternatives, and stop conditions. Elsewhere, only self-contained boundaries needed to define the immediately adjacent estimand or design choice remain; no section-14 pointer or equivalent cross-reference was added.

## Narrative repair action mapping

| Action | Revised locator(s) | Editorial operation and acceptance evidence |
|---|---|---|
| NRP-001 | `Background, current state, gap, significance, and rationale > Background`; `> Current state`; `> Gap`; `> Significance`; `> Rationale` | Split the mixed prose into exactly five non-empty H3 functions in the required order. Background explains the evolving sepsis and label-time problem; Current state summarizes public ICU resources and existing module precedents; Gap states the unresolved cross-stage and cross-database question; Significance gives reproducibility, interpretation, and translation-selection value without listing methods; Rationale connects dual clocks, process separation, simulation recovery, untouched external testing, and the conditional RCT design to the preceding gap. All original Sepsis-3, database heterogeneity, closest-work confidence, treatment–measurement feedback, and trial sparsity commitments remain present. |
| NRP-002 | `Title, summary, audience, and positioning > One-sentence complete-Idea summary` | Replaced the overloaded sentence with one readable compound sentence that identifies the study object, public ICU evidence path, 24-month stage I–II scope, untouched external testing, and the conditional RCT layer. Project-specific labels and detailed failure branches were removed from the summary; the RCT layer is explicitly outside and cannot complete the 24-month delivery. |
| NRP-003 | `Structured abstract` | Reordered and rewrote all five abstract fields as problem/gap, objective/hypothesis, overall approach, planned results, and contribution. Each core concept is described by scientific function before any shorthand: the simulation criterion states what it tests and what erroneous output it controls; the one-dimensional trial summary states its data source, frozen weights, dimension, and distinction from latent state; the independent SOFA analysis states its death/SOFA/discharge ordering and independence from stage II. Threshold and imputation details remain in Methods. |
| NRP-004 | `Feasibility, resources, risks, alternatives, and stop conditions > Working assumptions`; `> Limitations and boundary conditions`; `> Risks, alternatives, and stop conditions` | Consolidated all complete resource, access, data-support, identification, leakage, missingness, overlap, transport, RCT authorization/semantics/mapping, causal/clinical interpretation, closest-work, time, staffing, alternative, and stop statements in section 14. Removed full repeated lists from the abstract, core hypothesis, evidence chains, required analyses, expected outputs, contribution prose, and claim-support table. Section 14 contains 12 self-contained limitation classes, five pending-choice records, and ten trigger/alternative/stop rows. A text check confirms no `见第 14 节`, `见第14节`, `section 14`, or equivalent pointer occurs in the dossier. |
| NRP-005 | `Evidence chains` | Retained exactly five evidence chains. Every chain contains only Input, Method / analysis / processing, Output, and Supports. Deleted all five deprecated `Limits and failure conditions` fields. Their unique commitments are preserved in section 14: EHR onset non-uniqueness and two-library support; simulation-family and prediction boundaries; primary-task and leakage requirements; external isolation and zero-update precedence; and trial separation plus interpretation boundaries. |
| NRP-006 | `Required analyses and evidence` | Converted the section into eight auditable stage-II deliverable classes plus one RCT pre-analysis verification paragraph and the bounded closest-work positioning record. Removed repeated month-by-month ordering, implementation algorithms, numerical thresholds, and complete failure consequences. The time sequence remains self-contained in Research content; implementation remains in Methods; planned outputs and scientific falsification remain in section 11; complete operational limitations and stops remain in section 14. |

## Language finding mapping

### Critical and major findings

No critical language finding was issued. Every major finding and each itemized terminology subfinding is mapped below.

| Finding | Revised locator(s) | Resolution | Item-level acceptance evidence |
|---|---|---|---|
| LANG-R020-001a | `Structured abstract > Objective and hypothesis`; `Research question, objectives, and core hypothesis > Objectives` objective 3; `Research design and methods > Prespecified simulation recovery and erroneous-confidence control` | Replaced “绝对模拟恢复门／假置信门” with “预设模拟恢复与错误高置信输出控制标准” and direct descriptions. | The abstract states that predetermined data-generating scenarios must meet state, transition, and structure recovery thresholds and avoid high-confidence errors in null or misspecified scenarios. The Methods table gives the exact ARI/correlation, MAE, recovery-rate, FDR, false-edge, abstention, and calibration criteria and associated analysis responses. A reader can identify both the tested object and the consequence of failure without decoding an internal label. |
| LANG-R020-001b | `Structured abstract > Approach`; `Research question, objectives, and core hypothesis > Primary research question`; `Research design and methods > Conditional trial-observation mapping and independent analysis` | Replaced “冻结观测投影门／投影可观测状态摘要” at first use with a direct definition of a one-dimensional summary calculated from the frozen observation model and jointly measured trial indicators. | The abstract specifies the data source, one-dimensionality, frozen-weight meaning, and that the summary is not the latent state. Methods define C_r, Z_C, L_C=UDV', P_state and P_obs, the development-set standardization, sign convention, trial-specific mapping, and prohibition on using treatment groups or outcomes. |
| LANG-R020-001c | `Structured abstract > Expected result`; `Research question, objectives, and core hypothesis > Objectives` objective 4; `Research design and methods > Independent secondary clinical-state analysis`; `Evidence chains > Conditional RCT observation summary or independent clinical-state analysis` | Standardized the Chinese primary name to “试验特异性次要临床状态分析”; removed competing English shorthand from reader prose. | At first use, the abstract defines the ordering as death, inpatient SOFA, and alive discharge and states that the analysis is independent of stage II. Methods repeat the exact frozen endpoint definition only where it directly defines the analysis. The trial table retains all-randomized/mITT, missingness, center, multiplicity, and stop rules. |
| LANG-R020-001 | `Structured abstract`; `Primary research question`; three Methods subsections above | Resolved all three first-use terminology failures through function-first definitions and stable names. | Each subitem 001a–001c has a distinct first-use definition and full technical implementation later; no required concept depends on a later definition for basic comprehension. |
| LANG-R020-002 | `One-sentence complete-Idea summary`; `Primary research question`; `Observational target, anchoring and abstention`; `Prespecified simulation recovery and erroneous-confidence control`; `Conditional trial-observation mapping and independent analysis` | Split overloaded prose so that study object, condition, method, threshold, branch, and claim scope are expressed in separate sentences, paragraphs, bullets, or table rows. | The primary question is three sentences. The observational target is separated from anchoring and abstention rules. Simulation criteria occupy a seven-row table. Trial semantics, deterministic mapping, fidelity, mapped estimand, independent analysis, and trial-specific rules are separate labeled paragraphs or tables. No scientific condition or threshold was dropped. |
| LANG-R020-003 | `Core hypothesis and scientific scope`; `Evidence chains`; `Required analyses and evidence`; `Scientific falsification criteria`; `Interpretation of planned result patterns`; `Title and positioning claim-support table`; entire section 14 | Consolidated repeated limitation and failure lists while retaining each section’s unique scientific function. | Core hypothesis states only the hypothesis and immediate observational estimand boundary. Chains have four contract fields only. Required analyses list checkable records. Falsification criteria contain scientific challenges rather than operational contingency lists. The interpretation table contains allowed scopes without a repetitive prohibited-claim column. The claim-support table states supported scope in each claim cell. Complete boundaries and operational consequences occur once in section 14. |

### Minor findings

| Finding | Revised locator(s) | Resolution | Item-level acceptance evidence |
|---|---|---|---|
| LANG-R020-004 | `Positioning and contribution frame`; `Research content and work packages`; `Key techniques and implementation`; `Evidence chains`; `Contribution, innovation, impact, application, and closest-work comparison` | Replaced workflow metaphors such as “门、防火墙、封印、闭合、阶梯” with direct academic terms: criteria, variable-use separation, external-test access isolation, evidence relation, and evidence path. | Reader-facing headings and prose use direct scientific descriptions. The only remaining occurrence of “停止” describes a literal analysis stop, not a metaphor. No “防火墙”, “封印”, “证据阶梯”, or “证据链闭合” occurs in the revised dossier. |
| LANG-R020-005 | `Data, materials, and existing evidence base`; `Research design and methods`; `Key techniques and implementation` | Expanded nonshared abbreviations at first reader-facing use and standardized Chinese primary labels. | CIF, IPCW, MNAR, MAR, ESS, ARI, MAE, FDR, MCSE, NMAE, MI, FAS, PPS, mITT, FWER, CRPS, CRF, SAP, and CRRT are introduced with Chinese meaning and/or English full form. “Zero update” is consistently “完全不更新”; “finite update” is “有限更新”; “fallback” is described as an independent analysis; “prediction-only” is “仅预测”; pass/fail is rendered as a prespecified criterion. Database formal names and conventional SOFA/RCT abbreviations remain stable. |

## Protected-content preservation mapping

Each register summary was used only as an index. The full v003 passage at every `source_locator` was compared with the revised text before compression or movement.

| Protected ID | Revised locator(s) | Item-level preservation evidence |
|---|---|---|
| PCR-001 | YAML `identity_anchor`; `Primary research question`; `Objectives`; `Core hypothesis and scientific scope` | Preserves the knowledge-constrained, uncertainty-aware sepsis-centered dynamic representation; the comparable pre-onset risk period, first onset, post-onset evolution, recovery, worsening, organ failure, ICU discharge and death continuum; and the patient–time state/transition focus. The question is not reframed as ordinary prediction or generic ICU risk stratification. |
| PCR-002 | YAML `identity_anchor.primary_objective`; section 1 summary; `Objectives`; `Research content and work packages` | Preserves the 24-month stage I–II objective, literature/expert constraints, public-ICU system identification, cross-database validation and whole-course state representation. Planned scholarly and auditable evidence outputs remain broader than a prediction tool; no completed result is asserted. |
| PCR-003 | YAML `identity_anchor.study_object` and `primary_unit_of_inference`; `Protocol for the two primary clinical tasks`; `Observational target, anchoring and abstention` | Preserves the longitudinal sepsis-centered ICU system, comparable at-risk non-onset intervals, post-onset trajectories, patient–time states and transitions, and patient/hospital clustering. Adult, first eligible stay, incident/delayed-entry, weighting, and cluster-bootstrap handling remain explicit. |
| PCR-004 | `Current resource and evidence status`; `Public ICU database roles and G1 audit`; section 14 limitations item 1 | Preserves literature/expert priors, MIMIC-IV and eICU-CRD, and predesignation of HiRID or AmsterdamUMCdb as the conditional backup. Database existence/version is “已核验”; credentials, DUA, executable extraction, named staff and work hours are “未核验”; G1 support and all model results are “尚未生成”. No status was strengthened. |
| PCR-005 | `Local RCT evidence`; `Current resource and evidence status`; `Conditional trial-observation mapping and independent analysis`; section 14 limitations item 7 | Preserves EXIT-SEP and XBJ-SCAP only as conditional stage-III sources. Retains all trial and derivative-report counts, the derivative/QC evidence status, and the requirement for individual-data authorization, original CRF/SAP, randomization, center, actual visit timing, and survival/hospital/discharge semantics. |
| PCR-006 | `Research content and work packages`; `Variable-use separation`; `Observational target, anchoring and abstention`; all Methods subsections | Preserves the ordered sequence: resource/observability audit, label/state/hospital split lock, simple baselines, absolute recovery and erroneous-confidence checks, at most one complex candidate, two primary tasks and two secondary diagnostics, development freeze, untouched external testing, then conditional trial analysis. Preserves separate Y_t/A_t/M_t roles and limits interpretation to anchored, aligned, recoverable, transportable quantities with abstention rules. |
| PCR-007 | `Research content and work packages` conjunctive five-item definition; `Hospital-primary cross-database validation`; section 14 external-transport limitations and risk row | Preserves data support, absolute recovery, two primary tasks’ proper scores and calibration, leakage clearance, untouched external zero-update performance, state alignment and structural stability as a conjunction. Retains +0.01, 0.80–1.20, 0.02, ≥20 hospitals, ≥0.70 alignment and ≥0.80 sign agreement. Limited updates remain separately reported and cannot substitute for zero-update failure. Stage III cannot count toward stage II. |
| PCR-008 | `Protocol for the two primary clinical tasks`; `Mutually exclusive post-onset state and event system`; section 14 leakage limitations | Preserves the two primary tasks; event/availability clocks; specimen–antibiotic 72-hour/24-hour pairing; baseline SOFA rules; rolling 24-hour component calculation; infection −48/+24-hour window and first sortable onset; first-onset-only analysis; overlapping-landmark total stay weight of 1; delayed entry; mutually exclusive states and competing termination; as-of features; within-bin A_t/next-state order; exclusion of unsortable equal-timestamp edges; calibration/proper-score targets; patient/hospital clustered uncertainty; and checks for same-bin treatment, future measurement frequency, repeat admissions and outcome-driven grids or thresholds. |
| PCR-009 | `Structured abstract`; section 1 positioning; `Contribution, innovation, impact, application, and closest-work comparison`; claim-support table; section 14 limitations items 10–11 | Preserves that every model, recovery, external validation and trial reanalysis result is planned and not generated. Maintains conditional integration, validation, benchmark and resource contribution; high confidence that modules have precedents; low-to-moderate confidence in the full-combination gap; and no global-first or new-algorithm claim. |
| PCR-010 | Entire section 14, especially `Working assumptions`, `Limitations and boundary conditions`, and `Risks, alternatives, and stop conditions` | Preserves once at the authority location all access/team/G1, label/leakage, recoverability, MNAR/overlap, transport, time, trial authorization/semantics, common-anchor/mapping, closest-work and interpretation limits. Each trigger retains its bounded alternative and stop/downgrade consequence, including all numerical support, recovery, external, projection and schedule thresholds. Complete lists were removed elsewhere. |
| PCR-011 | `Research content and work packages` opening and timetable; section 14 limitations item 12; time and trial rows in the risk table | Preserves stage I–II completion within 24 months and stage III outside the minimum delivery. Trial work requires stage-II success plus data, semantic and mapping eligibility. Trial results cannot rescue or bypass resource, recovery, primary-task or untouched-external requirements. Month 3, 6, 12, 18/20, 20, 21–24 and post-24-month rules are retained. |
| PCR-012 | `Core hypothesis and scientific scope` local estimand boundary; section 14 limitations items 5, 9 and 10 | Preserves the full authority statement that observational data and prediction do not identify a real causal network, treatment causal effects, counterfactual policies, mechanisms, mediation, control or a digital twin; RCT secondary analyses do not validate unmeasured latent dynamics, transition edges or the whole system. The plan is not described as a validated model, clinical decision tool, drug platform or unconditional implementation basis. |

## Mechanical and lineage checks

- Research identity anchors are unchanged from v003; the edit remains in node `I01-001`.
- The revised dossier frontmatter binds plugin version `0.9.0-preview.3`, artifact/version/path, and exactly four logical `based_on` mappings.
- The revised dossier contains one H1, all 15 required H2 sections in contract order, and exactly the five required non-empty H3 reader functions under section 3.
- The H1 and section-1 Title field match exactly.
- Five evidence chains are present, each with exactly four required fields and no deprecated fifth field.
- The claim-support table uses the seven-field contract and has no separate qualifier column.
- Section 14 is the only complete limitations, assumptions, alternatives, and stop authority; no cross-reference pointer is present.
- The deterministic dossier linter is run separately against expected plugin version `0.9.0-preview.3`; a passing result establishes structural conformance only and is not a narrative-readiness or scientific-evaluation verdict.
