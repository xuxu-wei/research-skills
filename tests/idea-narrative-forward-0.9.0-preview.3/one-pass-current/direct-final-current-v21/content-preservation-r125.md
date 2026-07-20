---
schema_version: research-idea-content-preservation-review.v1
plugin_version: 0.9.0-preview.3
artifact_id: content-preservation-review-I01-001-r125
workflow_id: RID-SEPSIS-CSM-20260717-001
round_id: r125
idea_id: I01-001
source_skill: research-idea-orchestrator
review_mode: scientific_content_preservation
review_scope: complete_dossier_bounded_editorial_correction
fresh_independent_review: true
source_edits_performed: false
old_dossier_ref:
  artifact_id: idea-dossier-I01-001-v054
  version: v054
  path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v20/idea-dossier-v054.md
new_dossier_ref:
  artifact_id: idea-dossier-I01-001-v055
  version: v055
  path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v21/idea-dossier-v055.md
protected_register_ref:
  artifact_id: protected-content-register-I01-001-v054-v006
  version: v006
  path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v20/protected-content-register-v006.yaml
revision_delta_ref:
  artifact_id: revision-delta-I01-001-v054-to-v055
  version: v054-to-v055
  path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v21/revision-delta-v054-to-v055.md
files_read:
  - E:/BaiduNetdiskWorkspace/Jupyter/my_repos/xuxu-hermes/research-skills/tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v20/idea-dossier-v054.md
  - E:/BaiduNetdiskWorkspace/Jupyter/my_repos/xuxu-hermes/research-skills/tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v21/idea-dossier-v055.md
  - E:/BaiduNetdiskWorkspace/Jupyter/my_repos/xuxu-hermes/research-skills/tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v20/protected-content-register-v006.yaml
  - E:/BaiduNetdiskWorkspace/Jupyter/my_repos/xuxu-hermes/research-skills/tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v21/revision-delta-v054-to-v055.md
protected_items_reviewed: 64
protected_items_preserved: 64
identity_anchors_reviewed: 5
identity_anchors_verbatim: 5
identity_drift_detected: false
editorial_scope_violation_detected: false
scientific_change_declared: false
decision: scientific_content_preserved
violations: []
frozen: true
---

# Scientific-content preservation review: v054 to v055

## Decision

**Decision: `scientific_content_preserved`.**

The candidate preserves all 64 registered scientific-content items and all five identity anchors. No protected commitment was deleted, weakened, strengthened, relocated away from its authority, or made unconditional. No new scientific content was introduced, no planned work was presented as completed, and no adverse feasibility finding was concealed. There are no violations.

The bounded reader-facing change is an editorial terminology correction at four locations: the technical subsection heading and its three direct references change from `试验观察映射和独立分析` to `试验观测映射和独立分析`. The correction makes the label consistent with the established technical term “观测映射”; it does not change the mapping definition, data requirements, eligibility conditions, estimand, analysis, fallback branch, stop rule, evidence role, or permitted interpretation. The remaining dossier differences are version and provenance fields needed to identify v055. They do not alter study identity or scientific content.

## Review isolation and comparison basis

Only the four project artifacts listed in `files_read` were used. No assessment, preflight, evaluation, writer-compliance report, expected result, or other project artifact was read.

The comparison covered the complete v054 and v055 dossiers, every source locator named in the exact-source register, the 64 delta mappings, and the complete five-field identity record. A direct full-text comparison found four reader-facing substitutions of `观察` with `观测`, all in the same subsection label or its cross-references; the rest of the reader-facing dossier is unchanged. The delta identifies PCR-001 through PCR-064 once each, and those mappings agree with the source and candidate text.

## Identity-anchor comparison

| Identity field | Verbatim value in v054 and v055 | Result |
|---|---|---|
| `primary_research_question` | `can a knowledge-constrained, uncertainty-aware dynamic system representation of ICU patients cover the sepsis-centered pre-onset, onset, post-onset, and outcome continuum, demonstrate cross-database state/structure validity, and then test limited randomized intervention perturbations without conflating prediction with causality?` | Verbatim match |
| `primary_objective` | `construct and validate the sepsis complex-system model, with stage II completed within 24 months.` | Verbatim match |
| `study_object` | `the longitudinal sepsis-centered ICU patient system, including comparable at-risk non-onset intervals and post-onset trajectories.` | Verbatim match |
| `core_data_or_evidence_base` | `literature/expert priors; longitudinal public ICU data; conditionally available EXIT-SEP and XBJ-SCAP individual-level RCT data.` | Verbatim match |
| `primary_unit_of_inference` | `patient-time state and state transition, with patient and hospital clustering respected.` | Verbatim match |

Result: **5/5 anchors are identical; no identity drift is present.**

## Cross-cutting scientific checks

| Check | Independent comparison result |
|---|---|
| Study identity and scope | The sepsis-centered full-course object, four objectives, 24-month stage I–II boundary, subordinate stage III trial work, core evidence base, and patient-time/state-transition inference unit are unchanged. |
| Limitation authority | All 11 numbered limitation families remain at the same authority location with the same scope and consequences. None is weakened, displaced, or converted into a general prerequisite. |
| Conditionality and branch logic | Stage-II success remains a shared prerequisite for new trial visit analyses. Mapping eligibility remains branch-specific; failure of the mapping branch still permits the independent SOFA branch when its separate conditions hold, and unverifiable core semantics still stop all new visit-outcome analyses. Trials remain separate and unpooled. |
| Claim strength | The representation remains a candidate and all results remain planned. Simulation recovery, prediction, observational representation, limited adaptation, and trial secondary analyses retain their stated noncausal and nonvalidation boundaries. No algorithmic-novelty, global-first, clinical-effectiveness, decision-tool, drug-platform, control, mechanism, or digital-twin claim was added. |
| Evidence state | Verified database existence and version remain distinct from unverified access, extracts, project support, staffing, trial authorization, original trial semantics, anchor mappings, and all not-yet-generated model or analysis results. Trial derivative counts and their evidentiary limits are unchanged. |
| Feasibility findings | Required roles, absent personnel commitments, database and support audits, complexity caps, backup rules, data-isolation requirements, month-12/month-20/month-24 consequences, and trial-data limitations remain unchanged and visible. |
| Numerical and temporal rules | All event windows, landmarks, sample-support rules, anchor-density rules, simulation criteria, alignment and calibration thresholds, hospital split, mapping-fidelity criteria, visit days, multiplicity rules, and deadlines are unchanged. |
| Delta fidelity | The delta's four terminology corrections match the actual candidate. Its PCR-001–PCR-064 preservation map is complete and consistent with the dossiers and exact-source register. |

## Complete protected-content coverage

Category coverage is complete: identity and question 3/3; object scope and boundaries 4/4; inputs and resources 6/6; design, analysis, and inference 25/25; claims and evidence status 5/5; assumptions and limitations 17/17; unsupported claim classes 4/4. Total: **64/64 preserved**.

| Protected ID | Scientific commitment independently checked | Candidate disposition |
|---|---|---|
| PCR-001 | Five machine-facing identity values | Retained verbatim |
| PCR-002 | Full-course question; four objectives; subordinate, trial-specific extension; paper and auditable-evidence deliverables | Preserved |
| PCR-003 | Support and pre-fixation conditions; recoverable invariants; untouched-external stability; noncausal estimand boundary | Preserved |
| PCR-004 | Longitudinal sepsis-centered object; patient-time state/transition inference; clustered joint predictive or generative target | Preserved |
| PCR-005 | Pre-onset and post-onset cohorts; first-onset rule; landmarks; competing terminations; left truncation and censoring handling | Preserved |
| PCR-006 | Twelve-hour mutually exclusive state priority; absorbing, terminal, relapse, and transition properties | Preserved |
| PCR-007 | Separation of physiology, actions, measurement process, labels, and baseline variables; no leakage or pseudo-measurements | Preserved |
| PCR-008 | MIMIC-IV development role, eICU external role, prespecified backup rule, and auditable common-concept restriction | Preserved |
| PCR-009 | Unexecuted support audit; hospital/event/transition minima; anchor density and coverage; complexity and time-grid fallback rules | Preserved |
| PCR-010 | Verified database existence/version versus unverified access, support, staffing, models, tests, and bounded closest-work evidence | Preserved |
| PCR-011 | EXIT-SEP and XBJ-SCAP counts, missingness, unavailable fields, D-dimer uncertainty, and derivative-report evidence limits | Preserved |
| PCR-012 | Unverified trial authorization, original documents, randomization/center/visit/outcome semantics, and anchor mappings | Preserved |
| PCR-013 | Six required team functions, unverified commitments, bounded model scope, and work outside the 24-month plan | Preserved |
| PCR-014 | Fixed minimum precedence, simpler alternatives or stop, no bypass by added complexity or trial findings, and subordinate stage III | Preserved |
| PCR-015 | Complete conjunctive stage-II success definition, fixed thresholds, no-update primacy, and non-compensation rules | Preserved |
| PCR-016 | Pre-onset task population, 12-hour cumulative incidence estimand, landmarks/history, metrics, clustered intervals, and pass criteria | Preserved |
| PCR-017 | Post-onset day-7 favorable-state occupancy, component reporting, multistate method, sensitivity, metrics, and failure authority | Preserved |
| PCR-018 | Infection-pairing windows, SOFA baseline and organ window, event versus availability clocks, and two nonreplacement sensitivities | Preserved |
| PCR-019 | Recovery, deterioration, ICU exit, transfer/loss, and death definitions with their timing and missingness consequences | Preserved |
| PCR-020 | Two anchors per dimension; loading, scale, sparsity, dimensionality, state, lag, cycle, seed-alignment, and interpretation constraints | Preserved |
| PCR-021 | Explicit missingness modeling; five pattern-mixture shifts; tipping analysis; action prevalence and effective-sample-size limits | Preserved |
| PCR-022 | Months 7–10 simulation regimen, repeat/Monte Carlo precision rule, generator set, and crossed misspecification factors | Preserved |
| PCR-023 | Continuous-state canonical-correlation object, zero-on-failure rules, no result-driven deletion, interval formula, 0.80 criterion, and pre-fixation | Preserved |
| PCR-024 | Discrete, transition, sign/lag, edge, zero-edge, misspecification, calibration, alignment, retention, and failure rules | Preserved |
| PCR-025 | Seeded 30%/70% hospital split, patient-link handling, pre-outcome reporting, bipartite sensitivity, support triggers, and backup consequence | Preserved |
| PCR-026 | No-update, calibration-only, observation-layer-only, and full-refit order and distinct evidence roles; no test-driven selection | Preserved |
| PCR-027 | Shared trial prerequisites versus branch-specific anchor/fidelity conditions; post-stage-II, secondary, separate, unpooled status | Preserved; subsection label corrected only |
| PCR-028 | Trial anchor eligibility, frozen SVD mapping, sign and tie rules, external fidelity thresholds, blinded-trial coverage, and ineligibility conditions | Preserved; subsection label corrected only |
| PCR-029 | Ordered outcome, stratified standardized probability-index formula, half-credit ties, pooled-arm stratum weights, direction, and separate estimates | Preserved; subsection label corrected only |
| PCR-030 | Independent SOFA fallback when mapping fails, complete stop when core semantics fail, and protection of the still-eligible alternative branch | Preserved; subsection label corrected only |
| PCR-031 | EXIT-SEP and XBJ-SCAP target sets, visit days, missing-data and bounds rules, unavailable fields, Holm family, interactions, and no interpolation | Preserved; subsection label corrected only |
| PCR-032 | Pseudo-mask and future-trajectory diagnostic targets, scores, strata, separate reporting, and inability to reverse primary decisions | Preserved |
| PCR-033 | Full stage-II evidence requirements and trial authorization, semantics, mapping, outcome, missingness, center, multiplicity, and interaction requirements | Preserved; direct subsection reference corrected only |
| PCR-034 | Leakage and insufficient-support triggers, correction/deletion/backup/stop responses, and external-test block | Preserved |
| PCR-035 | Recovery, missingness, action support, and no-update external failure interpretations; prediction and limited adaptation cannot reverse failure | Preserved |
| PCR-036 | Mapping-specific failure, independent SOFA fallback, all-new-outcomes semantic stop, and no subgroup repair of discordance | Preserved; subsection label corrected only |
| PCR-037 | Month-12, month-20, and month-24 stop conditions and their distinct consequences | Preserved |
| PCR-038 | Database, role, test-isolation, cross-hospital support, trial-access, time, and novelty contingencies with object-specific consequences | Preserved |
| PCR-039 | Candidate/planned title and outputs, conditional integration/validation position, non-algorithmic contribution, and subordinate trial extension | Preserved |
| PCR-040 | Evidence ladder from traceability through task and cross-database support to limited within-trial evidence and absent causal/application evidence | Preserved; direct subsection reference corrected only |
| PCR-041 | Component precedents, bounded-search date and scope, low-to-moderate full-combination confidence, and no global-first claim | Preserved |
| PCR-042 | Seven result-pattern interpretations and their prohibited overinterpretations, including no causal or clinical-effectiveness inference | Preserved |
| PCR-043 | Separate secondary actual-visit results or no-analysis record; no stage-II compensation, pooling, common mechanism, or excess causal interpretation | Preserved; subsection label corrected only |
| PCR-044 | Continuous-recovery working assumption, owners, pre-result deadline, failure consequence, and unaffected simpler route | Preserved |
| PCR-045 | Trial probability-index working assumption, owner verification, pre-comparison deadline, stop consequence, and unaffected stages I–II | Preserved |
| PCR-046 | Month-7 clinical-scale-to-simulation mapping inputs, fixed objects/criteria, exclusion of external results, and unresolved-specification stop | Preserved |
| PCR-047 | Month-6 multicategory-calibration specification, allowed information, fixed task thresholds, no-relaxation rule, and unresolved-specification stop | Preserved |
| PCR-048 | Database access, executable extract, named commitment, dual-database support, and official-scale limitations at their authority | Preserved at authority |
| PCR-049 | Nonunique EHR onset, label sensitivity, leakage sources, and high-severity-leakage evidence boundary at their authority | Preserved at authority |
| PCR-050 | Recoverability under allowed transformations and generators, nonidentification by simulation, non-substitution by prediction, and failed-object handling | Preserved at authority |
| PCR-051 | Partial reach of missingness sensitivity and care-policy-only interpretation under low action support | Preserved at authority |
| PCR-052 | Cross-database heterogeneity, interface absence, no-update primacy, limited-adaptation role, and non-repair of no-update failure | Preserved at authority |
| PCR-053 | Twenty-four-month stage I–II boundary; month-12/20/24 consequences; stage-III inability to repair stage-I/II deficiencies | Preserved at authority |
| PCR-054 | Conditional trial-data availability, derivative-report limits, sparse visits, population/field differences, and no pseudo-continuous or pooled effect | Preserved at authority |
| PCR-055 | Candidate rather than established anchors, unverified D-dimer units and fidelity, mapping-outcome scope, and independent SOFA separation | Preserved at authority |
| PCR-056 | Non-systematic closest-work search, unsearched sources, terminology/preprint limits, component precedents, and low-to-moderate gap confidence | Preserved at authority |
| PCR-057 | Regulatory caution and prohibition on unconditional international clinical promotion | Preserved at authority |
| PCR-058 | Complete causal, counterfactual, mechanism, mediation, control, digital-twin, system-validation, tool/platform, promotion, and subgroup-repair prohibitions | Preserved at authority |
| PCR-059 | Role signatures as responsibilities rather than commitments; independent test-data custody; no external-result-driven change after month 20 | Preserved |
| PCR-060 | Event-per-parameter minima as design screens, not substitutes; timely specification resolution and no post hoc invented numbers | Preserved |
| PCR-061 | Real causal network, treatment effect, counterfactual policy, mechanism, mediation, control, and digital-twin claim classes remain unsupported | Preserved explicitly as unsupported |
| PCR-062 | Validated model, decision tool, drug platform, clinical effectiveness, and unconditional promotion claims remain unsupported; extra evidence remains required | Preserved explicitly as unsupported |
| PCR-063 | New-algorithm, first-in-field/global-first, worldwide-absence, and patent-absence claims remain unsupported; stronger-search requirements remain | Preserved explicitly as unsupported |
| PCR-064 | Trial visit-outcome differences cannot validate latent dynamics, edges, external structure, or the whole system; no pooled effect, common mechanism, or subgroup repair | Preserved explicitly as unsupported; subsection label corrected only |

## Violations

None.

## Final determination

The change from v054 to v055 is an allowed, bounded terminology correction. It does not constitute a scientific change. The candidate is eligible to proceed on scientific-content preservation grounds, subject to any separate editorial reassessment required by the governing workflow.
