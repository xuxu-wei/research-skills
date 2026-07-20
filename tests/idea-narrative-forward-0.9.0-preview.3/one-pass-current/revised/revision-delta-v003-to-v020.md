---
schema_version: research-idea-revision-delta.v1
plugin_version: 0.9.0-preview.3
artifact_id: revision-delta-I01-001-v003-to-v020
workflow_id: RID-SEPSIS-CSM-20260717-001
idea_id: I01-001
version_id: v020
path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/revised/revision-delta-v003-to-v020.md
source_version: v003
target_version: v020
change_type: editorial_repair
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
revised_artifact:
  artifact_id: idea-dossier-I01-001-v020
  version: v020
  path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/revised/idea-dossier-v020.md
source_skill: multi-path-idea-generator
identity_status: preserved
---

# Revision delta: idea dossier v003 to v020

## Scope and result

This revision is a single-pass editorial repair. It preserves the research identity, evidence status, numerical specifications, citations, planned-versus-completed distinctions, and all protected scientific boundaries. It changes narrative order, first-use explanations, sentence structure, terminology, redundancy, and the placement of limitations. No method value, evidence, result, or claim strength was added.

## Narrative action map

| Action | Revised locator | Resolution | Acceptance-test evidence |
|---|---|---|---|
| NRP-001 | `## Background, current state, gap, significance, and rationale` | Split the former mixed paragraphs into the required five reader functions and rewrote transitions so that the problem, current evidence, unresolved question, importance, and design rationale are distinguishable. | The section contains exactly five non-empty H3 headings in this order: `Background`, `Current state`, `Gap`, `Significance`, `Rationale`. `Significance` states the value for cross-database interpretation, reproducibility, reusable comparison resources, and translational decisions without listing methods. `Rationale` explicitly connects dual-time recording, variable-use separation, simulation recovery, isolated external testing, and trial-observation mapping to the preceding gaps. |
| NRP-002 | `## Title, summary, audience, and positioning` → `One-sentence complete-Idea summary` | Replaced the overloaded sentence with one reader-facing sentence naming the study object, 24-month stage I–II scope, two audited public ICU databases, full disease continuum, untouched external test, and conditional post-stage-II RCT layer. | The sentence answers what is studied, which evidence path is used, what the 24-month boundary is, and why the RCT layer is conditional. It contains none of the former undefined labels for absolute recovery, frozen projection, or death-ranked SOFA. |
| NRP-003 | `## Structured abstract` | Rewrote all five abstract fields in the order problem and gap, objective and hypothesis, overall approach, planned results, and contribution. Necessary specialized concepts are described by scientific function at first use. | Reading only the five fields identifies the known evidence, unresolved cross-stage and cross-database problem, significance, falsifiable hypothesis, sequential design, planned outputs, and bounded contribution. Detailed thresholds and branch mechanics appear only in the technical sections. |
| NRP-004 | `## Feasibility, resources, risks, alternatives, and stop conditions` | Consolidated the complete limitations, unresolved specifications, risks, alternatives, and stop consequences into section 14. Removed grouped limitation catalogues from other sections while retaining only boundaries needed to define a nearby estimand, design choice, scope, or falsification result. | Section 14 independently covers access and support, team commitments, G1 support, labels and leakage, recoverability, MNAR and overlap, external transport, timing, trial authorization and semantics, shared anchors and observation mapping, causal and clinical interpretation, and closest-work uncertainty. No dossier text contains “见第 14 节”, “参见第 14 节”, or an equivalent pointer. All 15 required H2 sections remain non-empty. |
| NRP-005 | `## Evidence chains` | Removed every chain-level `Limits and failure conditions` item and retained only evidence lineage. | There are exactly five evidence chains. Each contains exactly `Input`, `Method / analysis / processing`, `Output`, and `Supports`; no fifth limitation field or substitute cross-reference appears. The removed scientific limitations are retained self-contained in section 14. |
| NRP-006 | `## Required analyses and evidence` | Converted repeated schedules, procedures, thresholds, and consequences into a concise list of checkable records and deliverables. | Each of the eight stage II items and the RCT paragraph identifies an auditable artifact or result record. Time order remains in `Research content and work packages`, implementation remains in `Research design and methods`, falsification interpretations remain in section 11, and complete limitations remain in section 14. |

## Critical and major language finding map

No critical language finding was reported. All three major findings were resolved as follows.

| Finding | Revised locators | Resolution | Acceptance-test evidence |
|---|---|---|---|
| LANG-R020-001 | Section 1 summary and positioning; section 2 `Objective and hypothesis` and `Approach`; section 4 primary question and objectives 3–4; section 7 `Prespecified simulation recovery and erroneous-confidence control` and `Conditional trial-observation mapping and independent alternative` | Replaced the three opaque term groups with direct definitions. The simulation standard now states that it tests state, transition, and structure recovery and controls confident errors in null or misspecified settings. The trial summary is defined as a one-dimensional quantity computed from a frozen observation model and trial-shared measured indicators, not the latent state itself. The alternative endpoint has one Chinese name and immediately states its death, in-hospital SOFA, and alive-discharge ordering and independence from stage II. | A reader can identify the object and failure meaning of the simulation test before reaching the threshold table; can state the source, dimension, meaning, and non-meaning of the trial summary at abstract level; and can understand the three-level independent clinical-state analysis at first mention in the methods. The former competing English labels do not appear in reader-facing prose. |
| LANG-R020-002 | Section 1 one-sentence summary; section 4 primary research question; section 7 `Observational target, anchoring and abstention`, `试验语义与共同锚点资格核验`, and `测量一致性、校准和映射保真度核验` | Split object, condition, procedure, threshold, and consequence into separate sentences or structured tables. The primary question is now two questions: the stage II identity question and the conditional trial question. Observation-target notation, anchoring, missingness, support, trial eligibility, deterministic mapping, and fidelity criteria each occupy distinct paragraphs. | The main clause of each revised sentence is identifiable without backtracking. The summary remains one grammatical sentence as required but uses a semicolon to separate stage II from the conditional trial layer. The two trial subsections first state purpose and data, then criteria; branch consequences are stated separately. |
| LANG-R020-003 | Sections 4, 9, 10, 11, 12, 13, and 14 | Removed repeated catalogues of prohibited claims and repeated failure consequences. Section 9 now contains lineage only; section 10 contains deliverables; section 11 pairs each observable falsification result with one direct interpretation; sections 12–13 state positive contribution and claim calibration; section 14 contains the complete boundary and contingency statements. | Repeated sequences such as prediction not rescuing recovery, limited updating not replacing no-update failure, and RCT results not validating latent dynamics are each stated fully only in section 14. Elsewhere any retained boundary is local and necessary to define the adjacent estimand or output, without a pointer to section 14. |

## Minor language resolutions

| Finding | Compact resolution | Evidence in v020 |
|---|---|---|
| LANG-R020-004 | Replaced process metaphors with direct scientific language: “门” became prespecified standard, audit, eligibility check, or decision; “防火墙” became variable-use isolation; “封印” became external-test data isolation and frozen development decisions; “阶梯/闭合” became evidence levels and explicit evidence correspondence. | Section 1 positioning; sections 5 and 7 subsection names; section 8 technique names; section 12 `Contribution and evidence levels`. Required contract term `Evidence chain` is retained only as the schema heading. |
| LANG-R020-005 | Expanded non-general abbreviations at first reader-facing use and standardized Chinese primary names. | DUA in section 5; G1 in section 5; FAS/PPS in section 6; CIF, MNAR, MAR, ESS, MCSE, ARI, MAE, and FDR in section 7; MI, FWER, and mITT in the trial table; CRPS in secondary diagnostics. English workflow labels such as zero-update, fallback, prediction-only, and pass/fail were replaced with stable Chinese expressions. |

## Protected-content disposition

| Protected item | Revised locator | Disposition evidence |
|---|---|---|
| PCR-001 | Frontmatter `identity_anchor`; sections 1, 4, and final paragraph of section 14 | Retains the sepsis-centered pre-onset, onset, post-onset, and outcome continuum; the study remains a candidate dynamic-system representation rather than general ICU risk prediction. |
| PCR-002 | Frontmatter; section 1 summary; section 4 objectives; section 5 scope | Retains the 24-month stage I–II objective, literature and expert constraints, public ICU data, system identification, cross-database validation, and auditable scientific-evidence orientation. |
| PCR-003 | Frontmatter; section 4 primary question; section 7 observation target; final paragraph of section 14 | Retains longitudinal sepsis-centered ICU patients, comparable pre-onset intervals and post-onset trajectories, and patient-time state/transition inference with patient and hospital clustering. |
| PCR-004 | Section 6 resource-status table and public-database roles; section 14 feasibility | Retains MIMIC-IV and eICU-CRD as core public databases, HiRID or AmsterdamUMCdb as prespecified backup, and all access, DUA, extraction, cohort, personnel, and result statuses as unverified or not generated. |
| PCR-005 | Section 6 local RCT evidence; section 14 limitations | Retains EXIT-SEP and XBJ-SCAP only as conditional stage III sources and preserves the distinction between derivative reports and individual-level authorization or original CRF/SAP and trial semantics. |
| PCR-006 | Sections 5, 7, and 8 | Retains the ordered route from resource audit through simple baselines, simulation recovery, at most one complex candidate, two primary tasks, two diagnostics, frozen external testing, and only then conditional trial analysis; retains separation of state, action, and observation. |
| PCR-007 | Section 5 conjunctive definition; section 7 cross-database validation; section 14 limitations | Retains conjunctive success across support, recovery, scoring and calibration, leakage, untouched no-update performance, alignment, and structure stability; limited adaptation remains separately reported and cannot replace failure. |
| PCR-008 | Section 7 protocol table and mutually exclusive state table | Retains the two clinical tasks, event/availability times, incident risk set, delayed entry, mutually exclusive states, competing events, as-of features, calibration and proper scores, clustered uncertainty, and leakage protection. |
| PCR-009 | Sections 1–2, 6 resource table, section 12, and section 13 | Retains planned status, absence of current model or validation results, conditional integration/validation/resource contribution, established module precedents, and low-to-moderate confidence in the combination gap. |
| PCR-010 | Section 14 throughout | Retains once, at the sole complete authority location, access, personnel, G1 support, label and leakage, recoverability, MNAR and overlap, transport, timing, trial data and semantics, shared anchors and mapping, and closest-work uncertainty, with triggers and responses. |
| PCR-011 | Section 14 `Time and resources` boundary and risk table | Retains the 24-month stage I–II deadline, conditional post-24-month stage III, and the rule that trial results cannot complete or rescue stage II. |
| PCR-012 | Section 14 `Causal and application claims` boundary | Retains the complete prohibition on causal-network, treatment-effect, counterfactual-policy, mechanism, mediation, control, digital-twin, validated-model, clinical-tool, drug-platform, and unconditional-implementation claims. |

## Writer verification

- The H1 title exactly matches the section 1 `Title` field.
- The dossier contains all 15 required H2 sections in contract order.
- Section 3 contains the five required H3 functions in exact order.
- The five evidence chains contain the four required fields and no additional limitation field.
- The title, summary, research question, contribution, and core design relations were reread after all moves; all necessary specialized concepts are defined at or before first reader-facing use.
- Section 14 is the only complete location for limitations, working assumptions, risks, alternatives, and stop conditions; no cross-reference to it was inserted elsewhere.
- Identity and claim strength remain unchanged; all outputs and results remain explicitly planned or not generated.
