---
schema_version: research-idea-revision-delta.v1
plugin_version: 0.9.0-preview.3
artifact_id: revision-delta-I01-001-v003-to-v050
workflow_id: RID-SEPSIS-CSM-20260717-001
idea_id: I01-001
version_id: v003-to-v050
path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v16/revision-delta-v003-to-v050.md
change_type: editorial_repair_delta
source_artifact:
  artifact_id: idea-dossier-I01-001-v003
  version: v003
  path: tests/idea-test-0.9.0-preview.1/0.9.0-preview.1/03_ideas/nodes/I01-001/dossiers/idea-dossier-v003.md
target_artifact:
  artifact_id: idea-dossier-I01-001-v050
  version: v050
  path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v16/idea-dossier-v050.md
target_frozen_before_delta: true
rewritten_after_reader_facing_short_form_correction: true
frozen: true
---

# Revision delta: idea dossier v003 to v050

The earlier delta became invalid when four reader-facing phrases in `idea-dossier-v050.md` were corrected. This file is the rewritten delta. It was written only after the dossier was complete again, marked `frozen: true`, scanned for whole-dossier concordance, accepted by the source-dossier linter, and accepted by the reader-facing short-form comparison. Provenance is recorded only through logical artifact ID, version, path, and freeze order. This delta records editorial operations and their text-grounded evidence; it does not evaluate the science or add findings.

## Repair-item map

### NRP-001 — separate the five reasoning functions in section 3

- **Revised locator:** `Background, current state, gap, significance, and rationale` > `Background`, `Current state`, `Gap`, `Significance`, `Rationale`.
- **Operation:** Split and reorder; moved detailed closest-work comparison to section 12 and computational criteria to Methods.
- **Text-grounded acceptance evidence:** `Background` establishes Sepsis-3, the longitudinal databases, and the existence of relevant methodological precedents. `Current state` explains why label construction, treatment, measurement, and missingness create the scientific problem. `Gap` asks whether one longitudinal patient system can connect comparable pre-onset intervals, first onset, mutually exclusive post-onset states, recovery checks, clinical tasks, and an isolated external database; it does not rely on a claim that no prior combination exists. `Significance` states the consequence—distinguishing transportable patient-time information from interface or care-policy patterns—and names reproducibility, falsifiability, auditable evidence, and future high-level papers. `Rationale` links that problem to the two clinical tasks, prespecified generative scenarios, and application of the frozen model to unseen hospitals and a second database without importing thresholds.
- **Acceptance:** All five exact H3 headings are present, nonempty, ordered, and independently summarizable.

### NRP-002 — repair title, summary, and structured abstract

- **Revised locator:** H1; `Title, summary, audience, and positioning`; `Structured abstract`.
- **Operation:** Replace and subordinate.
- **Text-grounded acceptance evidence:** The H1 and `Title` both read `脓毒症全病程候选动态系统表征：24 个月跨数据库构建与检验计划`. The one-sentence summary begins with the whole-course scientific object and the 24-month stage-I/II objective, names the future-12-hour first-onset risk and day-7 favorable-state occupancy tasks, then names simulation recovery and external validation without parameter re-estimation. It locates the goal of one or more high-level papers and explicitly says the work is not being reduced to a prediction tool. Trial work appears only as a later, trial-separated secondary use when scientific prerequisites are met. Across the structured abstract, that later use appears once at a high level; trial names, visit days, equations, route conditions, and alternative endpoints are absent.
- **Acceptance:** A reader can recover the object, objective, main tasks, principal validation logic, prospective value, and time horizon from the first two sections without looking up an internal label.

### NRP-003 — consolidate conditional trial analyses in Methods

- **Revised locator:** `Research design and methods` > `Conditional trial-specific secondary analyses`.
- **Operation:** Consolidate, define, and delete repetition elsewhere.
- **Text-grounded acceptance evidence:** The subsection first states only the shared prerequisites: completed and frozen stage II, individual-level authorization, original CRF/SAP/data-dictionary or holder confirmation, randomized analysis-set and center semantics, visit timing, and survival/hospital status. It then presents, continuously and once, the mutually exclusive routes: (1) at least two eligible common measured anchors, the frozen equation and SVD-derived computation, the external and treatment-blinded empirical criteria, the visit-level hierarchical outcome, and the randomized-group advantage probability; (2) an independent death/discharge/SOFA clinical-state outcome when mapping-specific criteria fail but its own trial semantics are verifiable. It finally states that unverifiable core visit, randomized, center, survival, or hospitalization semantics stop the new visit-state outcome. EXIT-SEP and XBJ-SCAP populations, visits, missingness, center handling, multiplicity, and stopping rules remain separate.
- **Acceptance:** No route-specific criterion is promoted to a shared prerequisite, the trials are never pooled, and later trial results cannot replace any stage-II requirement.

### NRP-004 — make section 14 the complete limitations authority

- **Revised locator:** `Feasibility, resources, risks, alternatives, and stop conditions`; Methods for eligibility and alternatives; `Expected outputs, falsification criteria, and interpretations` for result-dependent decisions.
- **Operation:** Consolidate and delete repeated limitation families.
- **Text-grounded acceptance evidence:** Section 14 contains, once, the complete resource and access status, database comparability limits, personnel status, absence of generated results, trial-data and semantic limits, closest-work uncertainty, unresolved analytic specifications, missingness and overlap assumptions, external-validation distinctions, unsupported claim classes, identity boundary, and the operational trigger–response–consequence matrix. Methods retains the scientific eligibility criteria and mutually exclusive analysis logic. Section 11 alone states falsification and the interpretation permitted by each observed pattern. Each of the five evidence chains now has exactly four fields—Input, Method / analysis / processing, Output, and Supports—and no limits field. A whole-text search found no prose pointer directing the reader to section 14.
- **Acceptance:** Complete limitations are not repeated in the opening, evidence chains, contribution ladder, or claim-support table; locally indispensable estimand and interpretation boundaries remain brief and self-contained.

### NRP-005 — replace technique metaphors with reproducibility records

- **Revised locator:** `Key techniques and implementation`.
- **Operation:** Replace with a nine-row reproducibility table.
- **Text-grounded acceptance evidence:** Separate records now cover event and information-availability times; variables, units, and scientific roles; cohorts and mutually exclusive states; model inputs and outputs; simulation scenarios; hospital partitioning and external evaluation; trial common variables and frozen computation; uncertainty and multiplicity; and negative controls and negative-result publication. Every row states its input fields or constructs, computation, output record and audit use, and dependency. For example, the hospital row records eICU hospital IDs, interface completeness, patient linkage, the fixed seed, partition and exclusion computations, and the partition table, algorithm version, excluded-patient characteristics, permission log, and checksum needed to demonstrate isolation.
- **Acceptance:** No implementation item merely renames a Methods rule, and threshold rationales remain at their scientific authority.

### LANG-R101-01 — separate the four trial scientific roles

- **Revised locator:** `Research design and methods` > `Conditional trial-specific secondary analyses`; section 11 interpretation matrix.
- **Operation:** Split, define, and rename with direct Chinese scientific descriptions.
- **Text-grounded acceptance evidence:** The frozen formula introduces `P_obs` only as `P_obs=D_1^(-1)U_1'(Z_C−a_C)` and names it the one-dimensional observed-state quantity computed from common measured physiological anchors. The next paragraph separately defines the visit-level hierarchical state outcome, including death, the measured quantity among participants alive in hospital, and live discharge. The randomized comparison is separately defined as the center- or stratification-compatible advantage probability. The alternative outcome is separately named the trial-specific independent clinical-state outcome and is explicitly composed of death, SOFA among participants alive in hospital, and live discharge. Section 11 uses those role names when interpreting results.
- **Acceptance:** No reader-facing role is named by generic `projection`, `perturbation`, `death-ranked`, `fallback`, or an English project label.

### LANG-R101-02 — distinguish external validation, updating, and scoring

- **Revised locator:** `Research design and methods` > `Hospital-prioritized independent cross-database validation`; primary-task table; secondary diagnostics; evidence chains and section 11.
- **Operation:** Split and define.
- **Text-grounded acceptance evidence:** The principal external operation is stated as applying the frozen model to final-evaluation data without re-estimating any parameter. The three other operations are described separately: re-estimating only outcome-calibration intercepts and slopes; re-estimating only the observation equation while state and transition parameters remain frozen; and, if all model parameters are re-estimated, treating the work as new model development rather than an external-validation result. The dossier repeatedly states that success after either limited update cannot replace failure of the frozen model. Criteria name the Brier score or multicategory Brier score; trajectory diagnostics name the continuous ranked probability score.
- **Acceptance:** No `zero-update` variant or unexplained `proper score` remains in reader-facing prose.

### LANG-R101-03 — replace internal support and failure labels

- **Revised locator:** Methods > `Design sequence and database-support criteria`, `Absolute simulation and semi-synthetic recovery`, `Hospital-prioritized independent cross-database validation`; section 8 negative-result record; sections 11 and 14.
- **Operation:** Replace with explicit quantity–criterion–consequence statements.
- **Text-grounded acceptance evidence:** Database support is specified directly through patient/stay handling, at least 20 final-evaluation hospitals, 20/10 development/external events per free risk parameter, 20/10 transitions per free transition parameter, at least two anchors per state dimension, at least 30% measured eligible bins, and 70% hospital/80% patient coverage. Null-edge error is stated as the repeated proportion in which any false edge's 95% interval excludes zero, with a maximum of 0.05 and immediate rejection of the complex candidate. Misspecification error is separately stated as at least 80% mismatch detection or abstention and no more than 0.05 high-confidence wrong structures. Negative-result tables and figures must identify the object that missed the standard, the criterion, the stratification, and the scientific consequence.
- **Acceptance:** `G1`, generic false-confidence wording, and generic failure-figure names are absent; fixed schema headings containing `gate`, `no-go`, or `stop` do not carry scientific meaning in the prose.

### LANG-R101-04 — remove reader-facing workflow-state language

- **Revised locator:** Whole dossier free prose and table cells.
- **Operation:** Replace while preserving machine scaffolding.
- **Text-grounded acceptance evidence:** Evidence-status cells now use natural Chinese descriptions such as public-source verified, not yet verified, not yet generated, and project-local derivative material. The identity paragraph says that a substantive change would require a new research question rather than using an internal state token. External stability and inability to interpret are expressed through the measured quantity and scientific consequence. Standard technical abbreviations retained in prose are either established source names or defined at first use.
- **Acceptance:** Contract-fixed frontmatter, H2/H3 headings, formula symbols, references, and Claim-Support field labels remain unchanged where required; their presence is not used as hidden workflow semantics.

## Post-repair reader-facing phrase corrections

| Revised locator | Direct wording now used | Text-grounded result |
|---|---|---|
| Methods > independent cross-database validation, final operation | Re-estimating every model parameter constitutes new model development and is not an external-validation result | The operation is stated as a complete scientific sentence rather than assigned a compact update label; the distinction among frozen-model validation, calibration-only re-estimation, observation-equation-only re-estimation, and new model development is unchanged |
| Section-12 closest-work conclusion | The bounded search provides high-confidence evidence that every research module in the comparison table already has representative precedents | The evidence conclusion is stated directly without quotation marks or a label-like noun phrase; low-to-moderate confidence in the complete-combination gap is unchanged |
| Claim-Support status for the whole-course model | The model must always be described as an object that remains to be constructed and tested, not as an established system | Prospective evidence status is expressed through the scientific action and state rather than a quoted one-word qualifier |
| Claim-Support trial row and supporting output | Only after the main study meets all criteria do the two trials separately provide prespecified visit-state secondary analyses; the evidence-chain cell describes execution by trial and a recorded non-execution reason when prerequisites are absent | Both cells state actor, timing, operation, and scope in full; no replacement compact name was introduced |

## Protected-content disposition map

The evidence below identifies item-level preservation without reproducing the protected-register wording.

### PCR-001 — identity and primary question

- **Revised locators:** Frontmatter `identity_anchor`; one-sentence summary; structured-abstract objective; `Primary research question`.
- **Item-level evidence:** All five frontmatter anchor scalars are byte-for-byte equal to v003. The question and summary retain the longitudinal sepsis-centered system from comparable pre-onset risk intervals through first onset, mutually exclusive post-onset evolution, and outcomes, and they frame prediction as one task within system identification and validation rather than the study identity.
- **Disposition:** Same scientific meaning retained.

### PCR-002 — 24-month objective, publications, and non-reduction to prediction

- **Revised locators:** One-sentence summary; `Objectives` item 1; section-3 `Significance`; section-12 contribution paragraph.
- **Item-level evidence:** Objective 1 joins the 24-month stage-I/II horizon, literature and expert constraints, public ICU system identification, cross-database validation, and whole-course representation in one sentence. The summary and significance explicitly retain one or more high-level papers as a future aim and say the deliverable is not only a prediction tool.
- **Disposition:** All three commitments are separately locatable and retain prospective status.

### PCR-003 — study object and unit of inference

- **Revised locators:** Frontmatter `study_object` and `primary_unit_of_inference`; summary; structured-abstract objective; `Primary research question`; primary-task uncertainty rows.
- **Item-level evidence:** The dossier retains comparable at-risk non-onset intervals and post-onset trajectories in a longitudinal ICU patient system. The structured abstract names patient-time states and transitions as the inference unit; the research question and task table require patient and hospital clustering.
- **Disposition:** Object, boundaries, and clustering unit retained.

### PCR-004 — public-data inputs and current resource status

- **Revised locators:** `Current verified-resource versus prospective-gate status`; `Public ICU database roles and support status`; section-14 `Resource and evidence limitations`.
- **Item-level evidence:** MIMIC-IV v3.1 and eICU-CRD v2.0 retain development and external roles; one of HiRID or AmsterdamUMCdb must be selected prospectively as the backup. The resource table distinguishes verified database existence/version from unverified credentials, DUA, extraction, staffing, and not-yet-generated cohort and model results. Section 14 repeats these only as the complete limitation authority and adds that cross-database harmonization is restricted to audited common concepts.
- **Disposition:** Inputs and every evidence-status distinction retained without implying readiness.

### PCR-005 — conditional trial-data status

- **Revised locators:** `Local RCT evidence and present limits`; Methods > `Conditional trial-specific secondary analyses` > shared prerequisites; section-14 resource limitations.
- **Item-level evidence:** The data section says EXIT-SEP and XBJ-SCAP are only potential individual-level sources for conditional stage III and that current local reports are derivative. Methods still requires individual-level authorization, original CRF/SAP/data-dictionary or holder confirmation, randomization and center information, visit timing, and survival/hospital-state semantics before analysis.
- **Disposition:** Conditional status and original-source requirements retained.

### PCR-006 — ordered design and interpretability restrictions

- **Revised locators:** `Work packages and minimum route`; Methods > `Design sequence and database-support criteria`, `Variable roles`, `Observational target, anchoring, missingness, and abstention`.
- **Item-level evidence:** The fixed order runs from resource/support assessment through labels, states, hospital partition, simple baselines, simulation recovery, at most one complex candidate, two primary and two secondary tasks, freezing, unseen external validation, and only then possible trial analyses. Separate tables preserve physiological measurement, treatment action, observation process, label-only information, and baseline-covariate roles. The dossier retains the <90% seed-alignment, <80% bootstrap retention, <80% external sign agreement, <0.70 state alignment, and uncalibrated-interval consequences of deletion, merging, or database/care-policy-specific labeling; prediction cannot waive them.
- **Disposition:** Sequence, role separation, thresholds, and claim consequences retained at Methods authority.

### PCR-007 — conjunctive stage-II success

- **Revised locators:** `Conjunctive minimum success definition`; Methods > independent cross-database validation; section-11 external falsification; section-12 evidence ladder.
- **Item-level evidence:** Success still requires data support, absolute recovery, both primary-task Brier and calibration criteria, removal of high-severity leakage, frozen-model external performance without parameter re-estimation, state alignment, and structural sign stability. Outcomes after recalibration or observation-equation re-estimation are reported separately and cannot replace frozen-model failure. The 24-month-after trial work is excluded from stage-II success.
- **Disposition:** Conjunctive logic and update hierarchy retained.

### PCR-008 — primary-task, clock, state, and leakage commitments

- **Revised locators:** Methods > `Protocol locks for the two primary clinical tasks`; `Mutually exclusive post-onset state/event system`; `Variable roles`.
- **Item-level evidence:** The primary-task table retains the specimen/first-antimicrobial pairing windows (72 hours when specimen comes first and 24 hours when medication comes first), baseline SOFA rules, rolling 24-hour component maxima, infection-relative −48/+24-hour organ-dysfunction interval, and first sortable onset. It retains first-onset analysis, total stay weight one across overlapping assessment points, delayed entry, competing events, patient/hospital uncertainty, within-bin ordering of A_t before the next measured state, and exclusion of unorderable same-time edges. The leakage paragraph explicitly checks same-bin treatment, future measurement frequency, repeated stays or patients across sets, cross-split preprocessing, and outcome-driven grids or thresholds.
- **Disposition:** Scientific design commitments and numerical conditions retained.

### PCR-009 — prospective evidence and claim strength

- **Revised locators:** Structured abstract `Expected result`; data-status table; section-12 contribution and closest-work comparison; Claim-Support table; section-14 unsupported claims.
- **Item-level evidence:** The abstract says every listed deliverable is planned and not yet generated. Section 12 states directly, without a quoted label, that the bounded search provides high-confidence evidence that every research module shown in the table already has representative precedents, while confidence in the gap for the complete combination remains only low to moderate. The claim audit describes the model as an object still to be constructed and tested, and section 14 prohibits new-algorithm and global-first wording.
- **Disposition:** Evidence status and claim strength retained.

### PCR-010 — unique limitation authority and unresolved specifications

- **Revised locators:** Section 14 in full; Methods for design eligibility and alternatives; section 11 for falsification and result-dependent interpretation.
- **Item-level evidence:** Section 14 contains resource/access, staffing, database support, labels and leakage, recoverability, missing-not-at-random and overlap, frozen-model external validation, time nodes, trial data and semantics, common anchors and mapping, and closest-work uncertainty. It also retains the unresolved mapping from clinically tolerable scales to simulation parameters, exact multicategory calibration estimator and confidence limits, and threshold registration, and it states that event/parameter screening limits do not replace empirical effective sample size or simulation stability. Section 11 alone handles inconsistent trial directions or wide intervals and prohibits subgroup selection from changing the main interpretation.
- **Disposition:** Complete limitation families retained once at section 14; method and result authorities retain only their proper functions.

### PCR-011 — stage boundary and trial-route placement

- **Revised locators:** Section-5 schedule and work packages; Methods > conditional trial-specific analyses; one high-level trial item in each of evidence chains, required analyses, and planned outputs; section-12 contribution; section-13 Claim-Support; section 14.
- **Item-level evidence:** The schedule makes stage I–II a 24-month minimum and includes one dependent post-24-month trial work package. Methods first states stage-II success, individual data, and core semantics as shared prerequisites, then separates the common-anchor mapped outcome from the independent death/discharge/SOFA outcome, and finally stops the new visit outcome when core semantics cannot be verified. It states that no later trial result can repair stage-II resource, recovery, primary-task, or external-validation failure. The title and abstracts use only a high-level conditional purpose; data reports availability/status; implementation reports interfaces; the evidence chain, required analyses, and planned outputs each contain one function-specific item; contribution does not treat stage III as a parallel contribution. The Claim-Support row now states in full that only after the main study meets all criteria do the two trials separately provide prespecified visit-state secondary analyses, and its supporting-output cell describes the same function rather than naming it with a compact label.
- **Disposition:** Timing, shared prerequisites, mutually exclusive routes, stopping condition, and non-substitution retained with the prescribed placement.

### PCR-012 — unsupported claim classes

- **Revised locators:** Section 14 > `Unsupported claims and interpretation boundaries`; minimal estimand boundary in Methods; result-specific cells in section 11.
- **Item-level evidence:** Section 14 contains the complete prohibition on interpreting observational prediction as a true causal network, treatment effect, counterfactual policy, mechanism, mediation, control, or digital twin, and on interpreting conditional trial analyses as validation of unmeasured dynamics, transition edges, or the whole system. It also excludes present-tense validated-model, clinical-tool, drug-platform, unconditional clinical-use, new-algorithm, and first/global-first claims. Elsewhere, only the minimum local boundary needed to define an estimand or interpret a result remains.
- **Disposition:** Complete prohibition list retained once at the designated authority.

## Reader-facing short-form audit

The required source-to-v050 comparison accepted the repaired dossier with `--fail-on-new`, so no new compact reader-facing label, metaphor, acronym, or adjective-plus-candidate name remains. Retained short forms are source-standard scientific notation, proper study/database names, or contract-fixed structure:

| Retained form | First revised use | Scientific role | Authorization and definition status |
|---|---|---|---|
| ICU | H1/summary | Intensive-care setting | Existing standard clinical abbreviation from the source and identity anchors; used only for the setting |
| SOFA | Section 3 `Background` | Sequential Organ Failure Assessment score and label component | Existing standard source term; its operational baseline and rolling-window rules are defined in Methods |
| AI | `Primary audience` | Medical artificial intelligence community | Existing standard field abbreviation; not a model or claim label |
| MIMIC-IV, eICU-CRD, HiRID, AmsterdamUMCdb | Summary/data section | Named public ICU databases | Proper database names from the protected evidence base |
| EXIT-SEP, XBJ-SCAP | Data section | Named randomized trials | Proper trial names from the protected evidence base; absent from title and summaries |
| DUA | Resource table | Data-use agreement | Existing resource abbreviation; appears only in access status and requirements |
| CRF, SAP | Data table / Methods shared prerequisites | Original case-report form and statistical analysis plan | Existing standard trial-document abbreviations; used only for source-semantic verification |
| FAS, PPS | `Local RCT evidence and present limits` | Full-analysis and per-protocol populations | Defined in Chinese at first use, then used consistently for XBJ-SCAP populations |
| WBC, CRP, CRRT, CNS, PaO2/FiO2 | Local trial evidence / trial Methods | Standard laboratory, organ-support, neurological, and gas-exchange fields | Existing source-standard clinical forms; used only for measured or structurally unavailable fields |
| WP1–WP5 | Work-package table | Ordered work packages | Contract-preserved project structure; each row immediately defines its months, work, and output |
| X_t, Y_t, A_t, M_t, B, S | Methods observational target | Latent state, physiology, action, measurement process, baseline, and site | Existing source formula notation; each symbol is defined in the sentence that introduces the joint distribution |
| K | Methods database-support criteria | Number of retained shared state dimensions | Existing source formula symbol, immediately defined by `K=min(...,4)` |
| C_r, Z_C, a_C, L_C, U, D, V | Methods trial mapping | Trial-specific anchor set, standardized anchors, observation-equation and singular-vector terms | Formula notation retained under the brief's explicit frozen-equation requirement and defined locally |
| P_state | Methods frozen computation | One-dimensional stage-II state quantity | Existing source formula symbol, defined as `V_1'X` at first use |
| P_obs | Methods frozen computation | One-dimensional observed-state quantity computed from common measured anchors | Explicitly authorized by LANG-R101-01; introduced only with its complete formula and direct Chinese role name |
| D0, D1, D4, D7, D8 | Data section / trial Methods | Trial visit-day notation | Existing trial visit notation tied locally to the named trial and actual visit semantics |
| MDP, MPC | Section-12 closest-work table | Markov decision process and model predictive control | Existing standard technical abbreviations; each is expanded in Chinese at first revised use |

Reference-only identifiers such as DOI, PMID, PMCID, and arXiv remain part of citation scaffolding rather than reader-facing scientific role names.

## Source-to-revision competing-form concordance

| Repair ID | Source competing forms checked | Revised concordant form or disposition | Whole-text result |
|---|---|---|---|
| LANG-R101-01 | projection/proxy/summary, death-ranked endpoint, perturbation, fallback, English independent-outcome label | Four direct roles: common-anchor one-dimensional observed-state quantity; visit-level hierarchical state outcome; randomized-group advantage probability; trial-specific independent clinical-state outcome | Technical roles appear only after their Methods definitions; `P_obs` occurs with its formula; no generic role label remains outside identity-anchor text |
| LANG-R101-02 | zero update / zero-update, recalibration, decoder or observation-layer update, full refit, proper score | Frozen model applied without parameter re-estimation; outcome-calibration-only re-estimation; observation-equation-only re-estimation; a direct statement that re-estimating every parameter is new model development and not an external-validation result; named Brier/multicategory Brier/continuous ranked probability scores | Operations remain distinct and ordered; limited updates never replace frozen-model failure; no unexplained English variant or `proper score` remains |
| LANG-R101-03 | G1, false-confidence shorthand, failure figures/maps, generic gate/no-go/stop labels | Direct sample/event/transition/hospital/anchor quantities; direct null-edge and misspecification error criteria; negative outputs named by object, criterion, stratum, and consequence | `G1`, generic false-confidence language, and generic failure-output names are absent; five linter advisories occur only in contract-fixed headings/field labels |
| LANG-R101-04 | verified/unverified/not generated/project-local derivative, stable/database-specific/abstained, preserved/new-idea workflow tokens | Natural Chinese evidence status, stability, interpretation inability, preserved identity, and requirement for a substantively new research question | Reader-facing prose contains no workflow-state token; exact frontmatter and required English scaffolding remain machine-facing or contract-fixed |

## Whole-dossier concordance and freeze record

| Check | Result | Evidence |
|---|---|---|
| Target freeze before rewritten delta | Passed | The earlier delta was invalidated by the four wording edits; the target is bound only by artifact ID, version, and path, its frontmatter has `frozen: true`, both required checks passed, and this rewritten delta was created afterward |
| Verbatim identity anchors | Passed | Direct comparison with v003 returned exact equality for all five scalar lines |
| Complete structure | Passed | One H1, 15 H2 sections, and exactly five section-3 H3 headings in required order |
| H1/Title equality | Passed | Exact case-sensitive equality |
| Reader entry | Passed | One summary sentence; main whole-course study and 24-month objective lead; trial work remains subordinate |
| Section-14 authority | Passed | Complete limitations and unsupported claims occur there; no evidence-chain limits field and no section-14 pointer occurs elsewhere |
| Evidence chains | Passed | Five chains, each with exactly Input, Method / analysis / processing, Output, and Supports |
| Trial authority | Passed | Complete shared prerequisites, two mutually exclusive routes, stopping condition, populations, visits, missingness, multiplicity, and interpretations occur continuously in the section-7 authority |
| Prospective evidence status | Passed | No model, simulation, external validation, or trial result is presented as completed; high-level papers remain a future aim |
| Reader-facing short forms | Passed | The required source-to-v050 comparison completed with exit code 0 under `--fail-on-new`; no new compact label remained, and formula symbols and source-standard forms are defined or proper names |
| References | Passed | References 1–38 are present in uninterrupted numerical order; cited ranges resolve within that set |
| Source-dossier linter | Passed with contract-fixed advisories | Final command: `python -B research-skills-openai/skills/multi-path-idea-generator/scripts/lint_idea_dossier.py tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v16/idea-dossier-v050.md --expected-plugin-version 0.9.0-preview.3`; result `OK`, exit code 0 |
| Reader-facing short-form comparison | Passed | Final command: `python -B research-skills-openai/skills/academic-language-assessor/scripts/diff_reader_facing_short_forms.py tests/idea-test-0.9.0-preview.1/0.9.0-preview.1/03_ideas/nodes/I01-001/dossiers/idea-dossier-v003.md tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v16/idea-dossier-v050.md --fail-on-new`; exit code 0 |

The final linter advisories concern only the contract-fixed strings `Gate-linked output`, `Current verified-resource versus prospective-gate status`, `Prospective requirement / no-go`, `Multiplicity and stop rules`, and `Falsification and stop criteria`. They were retained because the canonical brief requires headings and field labels to remain unchanged; none is used as a reader-facing scientific shorthand.
