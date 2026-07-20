---
schema_version: research-idea-content-preservation-check.v1
check_id: content-preservation-I01-001-r128
review_id: content-preservation-I01-001-r128
reviewer_skill: idea-narrative-assessor
reviewer_instance_id: fresh-content-preservation-r128b
workflow_id: RID-SEPSIS-CSM-20260717-001
round_id: r128
input_artifact_ids:
  - idea-dossier-I01-001-v055
  - idea-dossier-I01-001-v056
  - protected-content-register-I01-001-v055-v007
  - revision-delta-I01-001-v055-to-v056
input_versions: [v055, v056, v007, v055-to-v056]
inputs:
  prior_dossier:
    artifact_id: idea-dossier-I01-001-v055
    version: v055
    path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v21/idea-dossier-v055.md
  revised_dossier:
    artifact_id: idea-dossier-I01-001-v056
    version: v056
    path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v22/idea-dossier-v056.md
  protected_content_register:
    artifact_id: protected-content-register-I01-001-v055-v007
    version: v007
    path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v21/protected-content-register-v007.yaml
  revision_delta:
    artifact_id: revision-delta-I01-001-v055-to-v056
    version: v055-to-v056
    path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v22/revision-delta-v055-to-v056.md
files_read:
  - tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v21/idea-dossier-v055.md
  - tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v22/idea-dossier-v056.md
  - tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v21/protected-content-register-v007.yaml
  - tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v22/revision-delta-v055-to-v056.md
isolation_mode: fresh_subagent
prior_scores_visible: false
source_edits_performed: false
decision: scientific_content_preserved
protected_item_checks:
  - protected_id: PCR-001
    prior_locator: "frontmatter > identity_anchor"
    revised_locator: "frontmatter > identity_anchor"
    semantic_status: preserved
    evidence: >-
      All five registered values are copied verbatim in v056; the question, objective, study object, evidence base, and unit of inference are unchanged.
  - protected_id: PCR-002
    prior_locator: "Research question, objectives, and core hypothesis > Primary research question; Objectives"
    revised_locator: "Research question, objectives, and core hypothesis > Primary research question; Objectives"
    semantic_status: preserved
    evidence: >-
      v056 retains the full-course question, all four objectives, the stage-I–II priority, the trial-specific subordinate question, and the scientific-evidence deliverable.
  - protected_id: PCR-003
    prior_locator: "Research question, objectives, and core hypothesis > Core hypothesis and evidence boundary"
    revised_locator: "Research question, objectives, and core hypothesis > Core hypothesis and evidence boundary"
    semantic_status: preserved
    evidence: >-
      The shared-support conditions, prespecification, absolute recovery, permitted reparameterizations, recoverable invariants, and noncausal estimand boundary are unchanged.
  - protected_id: PCR-004
    prior_locator: "Research design and methods > Observational target, anchoring, and evidence-qualified interpretation"
    revised_locator: "Research design and methods > Observational target, anchoring, and evidence-qualified interpretation"
    semantic_status: preserved
    evidence: >-
      The longitudinal study object, patient–time/state-transition inference unit, clustering, joint distribution over X, Y, A, M, B, and S, and derived targets are unchanged.
  - protected_id: PCR-005
    prior_locator: "Research design and methods > Protocol locks for the two primary clinical tasks"
    revised_locator: "Research design and methods > Protocol locks for the two primary clinical tasks"
    semantic_status: preserved
    evidence: >-
      Cohort ages, first-stay and first-onset rules, delayed entry, history, total weighting, mutually exclusive terminations, discharge distinction, and administrative-end handling remain unchanged.
  - protected_id: PCR-006
    prior_locator: "Research design and methods > Mutually exclusive post-onset state and event system"
    revised_locator: "Research design and methods > Mutually exclusive post-onset state and event system"
    semantic_status: preserved
    evidence: >-
      The 12-hour assignment, fixed priority, unsortable-time handling, absorbing and competing states, relapse, and transition rules are identical.
  - protected_id: PCR-007
    prior_locator: "Data, materials, and existing evidence base > Variable roles"
    revised_locator: "Data, materials, and existing evidence base > Variable roles"
    semantic_status: preserved
    evidence: >-
      Physiological, treatment, measurement, label-only, and baseline roles remain separate, including isolated dual-use copies, missingness meaning, and static-value handling.
  - protected_id: PCR-008
    prior_locator: "Data, materials, and existing evidence base > Public intensive-care database roles and support audit"
    revised_locator: "Data, materials, and existing evidence base > Public intensive-care database roles and support audit"
    semantic_status: preserved
    evidence: >-
      MIMIC-IV and eICU roles, the month-0–3 prespecified backup rule, equivalent audit, prohibition on test-driven selection, and common-concept eligibility are unchanged.
  - protected_id: PCR-009
    prior_locator: "Data, materials, and existing evidence base > Public intensive-care database roles and support audit > audit table"
    revised_locator: "Data, materials, and existing evidence base > Public intensive-care database roles and support audit > audit table"
    semantic_status: preserved
    evidence: >-
      Every audit input, event/transition minimum, anchor-density and coverage threshold, complexity cap, time-grid fallback, and no-unconditional-carry-forward rule remains unchanged.
  - protected_id: PCR-010
    prior_locator: "Data, materials, and existing evidence base > Current resource and result status"
    revised_locator: "Data, materials, and existing evidence base > Current resource and result status"
    semantic_status: preserved
    evidence: >-
      Verified database existence is still distinguished from unverified access and audits; no model, recovery, prediction, external-test, or new trial-analysis result is presented as existing, and closest-work confidence is unchanged.
  - protected_id: PCR-011
    prior_locator: "Data, materials, and existing evidence base > Local randomized-trial evidence status"
    revised_locator: "Data, materials, and existing evidence base > Local randomized-trial evidence status"
    semantic_status: preserved
    evidence: >-
      EXIT-SEP and XBJ-SCAP source qualifications, all participant and visit counts, unavailable fields, Sepsis-3 qualification, and unresolved D-dimer units are unchanged.
  - protected_id: PCR-012
    prior_locator: "Data, materials, and existing evidence base > Current resource and result status > trial rows"
    revised_locator: "Data, materials, and existing evidence base > Current resource and result status > trial rows; Local randomized-trial evidence status; Research design and methods > 试验观测映射和独立分析"
    semantic_status: preserved
    evidence: >-
      Authorization, original-source semantics, timing, randomization, centers, survival status, units, mappings, and anchor eligibility remain unverified; WBC and CRP remain candidates, and each mapping still requires at least two eligible anchors in the method authority.
  - protected_id: PCR-013
    prior_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Feasibility and resources"
    revised_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Feasibility and resources"
    semantic_status: preserved
    evidence: >-
      All six required roles, unverified commitments, computational scope, and activities outside the 24-month resource plan are unchanged.
  - protected_id: PCR-014
    prior_locator: "Research content and work packages > Work packages and minimum route"
    revised_locator: "Research content and work packages > Work packages and minimum route; 24 个月最低交付与时间节点; Limitations and boundary conditions > 6"
    semantic_status: preserved
    evidence: >-
      The fixed precedence, simpler-route and backup consequences, no-bypass rule, 24-month stage-I–II minimum, and subordinate post-24-month stage III all remain explicit.
  - protected_id: PCR-015
    prior_locator: "Research content and work packages > Conjunctive minimum success definition"
    revised_locator: "Research content and work packages > Conjunctive minimum success definition; 24 个月最低交付与时间节点; Limitations and boundary conditions > 6"
    semantic_status: preserved
    evidence: >-
      Every conjunct, numerical threshold, tighten-only rule, and no-update/adaptation distinction is unchanged; milestone and limitation authorities retain that stage III cannot count toward or repair stage-II success.
  - protected_id: PCR-016
    prior_locator: "Research design and methods > Protocol locks for the two primary clinical tasks > primary pre-onset task column"
    revised_locator: "Research design and methods > Protocol locks for the two primary clinical tasks > primary pre-onset task column"
    semantic_status: preserved
    evidence: >-
      The 12-hour cumulative-incidence target, landmark/history/weight rules, metrics, clustered intervals, and all noninferiority, calibration, risk-error, and leakage criteria are unchanged.
  - protected_id: PCR-017
    prior_locator: "Research design and methods > Protocol locks for the two primary clinical tasks > primary post-onset task column"
    revised_locator: "Research design and methods > Protocol locks for the two primary clinical tasks > primary post-onset task column; Research content and work packages > Work packages and minimum route"
    semantic_status: preserved
    evidence: >-
      The day-7 favorable set, separate components, multistate/Aalen–Johansen analysis, day-14 sensitivity, strata, metrics, and gates are unchanged; the global no-bypass rule still prevents trial results from reversing a failed primary task.
  - protected_id: PCR-018
    prior_locator: "Research design and methods > Protocol locks for the two primary clinical tasks > event clock and information-availability clock"
    revised_locator: "Research design and methods > Protocol locks for the two primary clinical tasks > event clock and information-availability clock"
    semantic_status: preserved
    evidence: >-
      The 72/24-hour infection pairing, baseline and rolling SOFA rules, −48/+24-hour organ window, availability clock, non-backfilling rule, and two sensitivity labels are identical.
  - protected_id: PCR-019
    prior_locator: "Research design and methods > Mutually exclusive post-onset state and event system > state definitions"
    revised_locator: "Research design and methods > Mutually exclusive post-onset state and event system > state definitions"
    semantic_status: preserved
    evidence: >-
      Recovery, deterioration/new organ failure, alive ICU exit, transfer/lost observation, and death retain their definitions, timing, action separation, and missingness consequences.
  - protected_id: PCR-020
    prior_locator: "Research design and methods > Observational target, anchoring, and evidence-qualified interpretation"
    revised_locator: "Research design and methods > Observational target, anchoring, and evidence-qualified interpretation"
    semantic_status: preserved
    evidence: >-
      Two anchors per dimension, +1 loading, scale and sparsity rules, dimension/mechanism/lag caps, acyclicity, 20-seed alignment, and interpretability limits are unchanged.
  - protected_id: PCR-021
    prior_locator: "Research design and methods > Observational target, anchoring, and evidence-qualified interpretation > missingness and action support"
    revised_locator: "Research design and methods > Observational target, anchoring, and evidence-qualified interpretation > missingness and action support"
    semantic_status: preserved
    evidence: >-
      The measurement/selection-model approach, −1 to +1 shift grid, tipping analysis, action-probability bounds, 20% effective-sample threshold, and no-treatment-effect consequence are unchanged.
  - protected_id: PCR-022
    prior_locator: "Research design and methods > Absolute simulation and semi-synthetic recovery criteria > simulation regimen"
    revised_locator: "Research design and methods > Absolute simulation and semi-synthetic recovery criteria > simulation regimen"
    semantic_status: preserved
    evidence: >-
      The month-7–10 timing, 1,000-repeat or MCSE criterion, all generator classes, and all crossed perturbation scenarios are unchanged.
  - protected_id: PCR-023
    prior_locator: "Research design and methods > Absolute simulation and semi-synthetic recovery criteria > continuous branch"
    revised_locator: "Research design and methods > Absolute simulation and semi-synthetic recovery criteria > continuous branch"
    semantic_status: preserved
    evidence: >-
      Same-row comparison, all canonical correlations, zero assignment for dimension/rank/algorithm failure, no result-driven deletion, the full L formula, and the 0.80 threshold are identical.
  - protected_id: PCR-024
    prior_locator: "Research design and methods > Absolute simulation and semi-synthetic recovery criteria > recovery criteria table"
    revised_locator: "Research design and methods > Absolute simulation and semi-synthetic recovery criteria > recovery criteria table; closing rule"
    semantic_status: preserved
    evidence: >-
      ARI, seed alignment, transition MAE/coverage, sign/lag, FDR, zero-edge, misspecification, calibration, retention/alignment thresholds, and all failure actions are unchanged.
  - protected_id: PCR-025
    prior_locator: "Research design and methods > Hospital-primary cross-database validation > partition and cross-hospital-patient rules"
    revised_locator: "Research design and methods > Hospital-primary cross-database validation > partition and cross-hospital-patient rules"
    semantic_status: preserved
    evidence: >-
      Seed 20260717, 30%/70% hospital assignment, cross-partition exclusions, first-stay handling, bipartite sensitivity, support thresholds, 10% trigger, backup, and fallback claims are unchanged.
  - protected_id: PCR-026
    prior_locator: "Research design and methods > Hospital-primary cross-database validation > four update operations"
    revised_locator: "Research design and methods > Hospital-primary cross-database validation > four update operations"
    semantic_status: preserved
    evidence: >-
      Freeze inputs, the ordered no-update/calibration-only/observation-layer/full-refit operations, their evidentiary roles, prohibited test selection, and no-compensation rule are unchanged.
  - protected_id: PCR-027
    prior_locator: "Research design and methods > 试验观测映射和独立分析 > 共享前提"
    revised_locator: "Research design and methods > 试验观测映射和独立分析 > 共享前提"
    semantic_status: preserved
    evidence: >-
      Stage-II success, authorization, original semantic verification, trial separation, exploratory status, post-24-month timing, and no pooling remain; mapping-anchor and fidelity criteria remain branch-specific rather than shared prerequisites.
  - protected_id: PCR-028
    prior_locator: "Research design and methods > 试验观测映射和独立分析 > 观测映射成立时的有序访视结局分析及外部忠实度判定"
    revised_locator: "Research design and methods > 试验观测映射和独立分析 > 观测映射成立时的有序访视结局分析及外部忠实度判定"
    semantic_status: preserved
    evidence: >-
      Trial-specific anchor eligibility, frozen standardization and SVD, sign convention, blinded mapping, every eICU fidelity threshold, trial range/density threshold, and ineligibility consequence are identical.
  - protected_id: PCR-029
    prior_locator: "Research design and methods > 试验观测映射和独立分析 > 分层标准化概率指数"
    revised_locator: "Research design and methods > 试验观测映射和独立分析 > 分层标准化概率指数"
    semantic_status: preserved
    evidence: >-
      Death–proxy–discharge ordering, the complete stratified probability-index estimand, pooled-arm weights, favorable direction, half-credit ties, interpretation, and secondary-quantity restriction are unchanged.
  - protected_id: PCR-030
    prior_locator: "Research design and methods > 试验观测映射和独立分析 > 观测映射不成立但独立分析条件成立时的分析; 核心语义不足时停止"
    revised_locator: "Research design and methods > 试验观测映射和独立分析 > 观测映射不成立但独立分析条件成立时的分析; 核心语义不足时停止"
    semantic_status: preserved
    evidence: >-
      Mapping failure still leaves the separately eligible SOFA endpoint available, while unverifiable visit/randomization/center/survival semantics still stop every new visit-outcome analysis.
  - protected_id: PCR-031
    prior_locator: "Research design and methods > 试验观测映射和独立分析 > EXIT-SEP and XBJ-SCAP trial table"
    revised_locator: "Research design and methods > 试验观测映射和独立分析 > EXIT-SEP and XBJ-SCAP trial table; closing paragraph"
    semantic_status: preserved
    evidence: >-
      Trial populations, visits, analysis sets, imputation inputs, Rubin combination, shifts, bounds, structural absence, D-dimer exclusion, Holm family, subgroup interactions, and sparse-visit rule are identical.
  - protected_id: PCR-032
    prior_locator: "Research design and methods > Secondary representation diagnostics"
    revised_locator: "Research design and methods > Secondary representation diagnostics"
    semantic_status: preserved
    evidence: >-
      Pseudo-mask and future-trajectory diagnostics retain all scores, stratification, separate reporting, and inability to alter primary, recovery, or cross-database decisions.
  - protected_id: PCR-033
    prior_locator: "Required analyses and evidence; Research design and methods > 试验观测映射和独立分析"
    revised_locator: "Required analyses and evidence; Research design and methods > 试验观测映射和独立分析"
    semantic_status: preserved
    evidence: >-
      All eight stage-II evidence groups remain; trial authorization, original semantics, trial-specific qualification, analysis sets, mapping, estimand, missingness, centers, multiplicity, and subgroup rules remain authoritative in methods.
  - protected_id: PCR-034
    prior_locator: "Expected outputs, falsification criteria, and interpretations > Falsification and stop criteria > clocks, leakage, and data support"
    revised_locator: "Expected outputs, falsification criteria, and interpretations > Falsification and stop criteria > clocks, leakage, and data support"
    semantic_status: preserved
    evidence: >-
      Future-information and cross-split failures, corrective actions, external-test block, and event/hospital/exclusion/anchor support fallbacks are unchanged.
  - protected_id: PCR-035
    prior_locator: "Expected outputs, falsification criteria, and interpretations > Falsification and stop criteria > recovery, missingness, action support, and external result"
    revised_locator: "Expected outputs, falsification criteria, and interpretations > Falsification and stop criteria > recovery, missingness, action support, and external result"
    semantic_status: preserved
    evidence: >-
      Complex-candidate nonpromotion, prediction nonoverride, missingness reporting, low-support interpretation, no treatment-effect estimation, and no-update external-test failure meaning are unchanged.
  - protected_id: PCR-036
    prior_locator: "Expected outputs, falsification criteria, and interpretations > Falsification and stop criteria > trial criteria"
    revised_locator: "Expected outputs, falsification criteria, and interpretations > Falsification and stop criteria > trial criteria"
    semantic_status: preserved
    evidence: >-
      Mapping failure blocks only the proxy outcome, separately eligible SOFA remains, core semantic failure stops all new visit outcomes, and discordance/imprecision cannot be repaired through subgroup selection.
  - protected_id: PCR-037
    prior_locator: "Expected outputs, falsification criteria, and interpretations > Falsification and stop criteria > time"
    revised_locator: "Expected outputs, falsification criteria, and interpretations > Falsification and stop criteria > time"
    semantic_status: preserved
    evidence: >-
      The month-12 simple-representation freeze, month-20 test-access prohibition, and month-24 incomplete stage-II endpoint consequences are unchanged.
  - protected_id: PCR-038
    prior_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Risks, alternatives, and stop conditions"
    revised_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Risks, alternatives, and stop conditions"
    semantic_status: preserved
    evidence: >-
      Resource, role, isolation, linked-patient support, trial authorization/semantics, timing, and closest-work contingencies retain their object-specific triggers, responses, and consequences.
  - protected_id: PCR-039
    prior_locator: "Title, summary, audience, and positioning; Structured abstract"
    revised_locator: "Title, summary, audience, and positioning; Structured abstract; Research question, objectives, and core hypothesis; Research content and work packages > 24 个月最低交付与时间节点"
    semantic_status: preserved
    evidence: >-
      Candidate and planned status, pending outputs, conditional integration/validation contribution, noncausal scope, and subordinate post-success trial status remain; deleted overview repetitions do not alter these claims.
  - protected_id: PCR-040
    prior_locator: "Contribution, innovation, impact, application, and closest-work comparison > Contribution and evidence ladder"
    revised_locator: "Contribution, innovation, impact, application, and closest-work comparison > Contribution and evidence ladder"
    semantic_status: preserved
    evidence: >-
      The evidence ladder retains the data, reconstruction/task, cross-database, subordinate trial, and absent causal/application evidence levels with the same claim strength.
  - protected_id: PCR-041
    prior_locator: "Contribution, innovation, impact, application, and closest-work comparison > Verified representative closest-work comparison"
    revised_locator: "Contribution, innovation, impact, application, and closest-work comparison > Verified representative closest-work comparison"
    semantic_status: preserved
    evidence: >-
      Component precedents, the 2026-07-17 bounded-search status, high component confidence, low-to-moderate combination-gap confidence, and conditional integration/validation position are unchanged.
  - protected_id: PCR-042
    prior_locator: "Expected outputs, falsification criteria, and interpretations > Interpretation matrix"
    revised_locator: "Expected outputs, falsification criteria, and interpretations > Interpretation matrix"
    semantic_status: preserved
    evidence: >-
      Every result pattern retains the same allowed interpretation and prohibited inference for simple baselines, recovery, external testing, adaptation, tasks, trial branches, and full stage-II conjunction.
  - protected_id: PCR-043
    prior_locator: "Research design and methods > 试验观测映射和独立分析; Evidence chain: 有前置条件的随机试验次要分析"
    revised_locator: "Research design and methods > 试验观测映射和独立分析; Evidence chain: 有前置条件的随机试验次要分析; Planned outputs"
    semantic_status: preserved
    evidence: >-
      Trial outputs remain separate secondary actual-visit results or a no-analysis record, outside stage-II success, without pooled effect or common mechanism, and with randomized interpretation limited to the prespecified within-trial outcome.
  - protected_id: PCR-044
    prior_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Working assumptions > continuous latent-state recovery row"
    revised_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Working assumptions > continuous latent-state recovery row; Research design and methods > Absolute simulation and semi-synthetic recovery criteria > continuous branch"
    semantic_status: preserved
    evidence: >-
      The unique continuous-recovery computation, dual responsible roles, pre-result month-7 deadline, nonconfirmation consequence, and unaffected simpler route are unchanged.
  - protected_id: PCR-045
    prior_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Working assumptions > trial probability-index row"
    revised_locator: "Research design and methods > 试验观测映射和独立分析 > 分层标准化概率指数; Feasibility, resources, risks, alternatives, and stop conditions > Working assumptions > trial probability-index row"
    semantic_status: preserved
    evidence: >-
      The complete unique estimand remains at the method authority; written statistical confirmation, source checks, timing, stopping consequence, and unaffected stage-I–II route remain unchanged in the assumption row.
  - protected_id: PCR-046
    prior_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Working assumptions > clinical-scale-to-simulation mapping row"
    revised_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Working assumptions > clinical-scale-to-simulation mapping row"
    semantic_status: preserved
    evidence: >-
      The month-7 deadline, permitted information, frozen generators/recovery objects/criteria, external-result exclusion, and no-start/no-promotion consequence are unchanged.
  - protected_id: PCR-047
    prior_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Working assumptions > multicategory-calibration row"
    revised_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Working assumptions > multicategory-calibration row"
    semantic_status: preserved
    evidence: >-
      The month-6 specification deadline, permitted evidence, fixed tasks and thresholds, tighten-only rule, and no-success/no-external-test consequence are unchanged.
  - protected_id: PCR-048
    prior_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Limitations and boundary conditions > 1. Resources, access, and team status"
    revised_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Limitations and boundary conditions > 1. Resources, access, and team status"
    semantic_status: preserved
    evidence: >-
      The complete resource, access, commitment, project-count, and unaudited-support limitation is retained once at the limitation authority.
  - protected_id: PCR-049
    prior_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Limitations and boundary conditions > 2. Labels, clocks, and leakage"
    revised_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Limitations and boundary conditions > 2. Labels, clocks, and leakage"
    semantic_status: preserved
    evidence: >-
      The complete onset-time, label-dependence, leakage-source, and unresolved-high-severity boundary is retained once at the limitation authority.
  - protected_id: PCR-050
    prior_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Limitations and boundary conditions > 3. State recoverability and structural scope"
    revised_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Limitations and boundary conditions > 3. State recoverability and structural scope"
    semantic_status: preserved
    evidence: >-
      The complete reparameterization, simulation-versus-identification, evidence non-substitution, and delete/merge/qualify limitation is retained once.
  - protected_id: PCR-051
    prior_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Limitations and boundary conditions > 4. Nonrandom missingness and low action overlap"
    revised_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Limitations and boundary conditions > 4. Nonrandom missingness and low action overlap"
    semantic_status: preserved
    evidence: >-
      The complete partial-sensitivity, unmeasured-physiology, low-overlap, effective-sample, and no-treatment-effect limitation is retained once.
  - protected_id: PCR-052
    prior_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Limitations and boundary conditions > 5. Cross-database evidence"
    revised_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Limitations and boundary conditions > 5. Cross-database evidence"
    semantic_status: preserved
    evidence: >-
      The complete database-difference, interface-absence, no-update primacy, adaptation/refit role, and no-repair limitation is retained once.
  - protected_id: PCR-053
    prior_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Limitations and boundary conditions > 6. Time and delivery boundary"
    revised_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Limitations and boundary conditions > 6. Time and delivery boundary"
    semantic_status: preserved
    evidence: >-
      The 24-month requirement, month-12/20/24 consequences, stage-III exclusion, and inability of later trial results to repair stage-I–II failures are retained once.
  - protected_id: PCR-054
    prior_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Limitations and boundary conditions > 7. Trial data and semantics"
    revised_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Limitations and boundary conditions > 7. Trial data and semantics"
    semantic_status: preserved
    evidence: >-
      Conditional data availability, source-verification requirements, sparse visits, population/field differences, and prohibition on pseudo-trajectories and pooled effects are retained once.
  - protected_id: PCR-055
    prior_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Limitations and boundary conditions > 8. Common physiological anchor variables and observation mapping"
    revised_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Limitations and boundary conditions > 8. Common physiological anchor variables and observation mapping"
    semantic_status: preserved
    evidence: >-
      Candidate-only WBC/CRP status, unresolved D-dimer units, absent fidelity results, and distinct proxy-outcome versus independent-SOFA interpretation remain complete.
  - protected_id: PCR-056
    prior_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Limitations and boundary conditions > 9. Closest-work uncertainty"
    revised_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Limitations and boundary conditions > 9. Closest-work uncertainty"
    semantic_status: preserved
    evidence: >-
      The nonsystematic scope, omitted sources, terminology/preprint uncertainty, component precedents, and low-to-moderate combination-gap confidence are retained once.
  - protected_id: PCR-057
    prior_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Limitations and boundary conditions > 10. Regulatory applicability"
    revised_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Limitations and boundary conditions > 10. Regulatory applicability"
    semantic_status: preserved
    evidence: >-
      The 2026 regulatory caution and prohibition on unconditional international clinical promotion are retained once without weakening.
  - protected_id: PCR-058
    prior_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Limitations and boundary conditions > 11. Complete prohibited claims"
    revised_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Limitations and boundary conditions > 11. Complete prohibited claims"
    semantic_status: preserved
    evidence: >-
      All causal, mechanistic, control, digital-twin, whole-system-validation, validated-tool/platform, promotion, and subgroup-repair prohibitions are retained once.
  - protected_id: PCR-059
    prior_locator: "Research content and work packages > 24 个月最低交付与时间节点"
    revised_locator: "Research content and work packages > 24 个月最低交付与时间节点"
    semantic_status: preserved
    evidence: >-
      Role signatures remain explicitly noncommitments, final test data remain inaccessible until the month-18–20 custodian-signed freeze, and no test-driven change is allowed after month 20.
  - protected_id: PCR-060
    prior_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Working assumptions > closing qualification"
    revised_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Working assumptions > closing qualification"
    semantic_status: preserved
    evidence: >-
      Screening minima remain non-substitutes for effective sample size, stability, or clustered uncertainty, and unresolved specifications still trigger stated consequences rather than post hoc numerical invention.
  - protected_id: PCR-061
    prior_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Limitations and boundary conditions > 11. Complete prohibited claims"
    revised_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Limitations and boundary conditions > 11. Complete prohibited claims"
    semantic_status: preserved
    evidence: >-
      Real causal network, treatment-effect, counterfactual-policy, mechanism, mediation, control, and digital-twin claims remain explicitly unsupported.
  - protected_id: PCR-062
    prior_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Limitations and boundary conditions > 11. Complete prohibited claims; Contribution and evidence ladder"
    revised_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Limitations and boundary conditions > 11. Complete prohibited claims; Contribution and evidence ladder"
    semantic_status: preserved
    evidence: >-
      The plan remains explicitly not an already validated model, decision tool, drug platform, proof of effectiveness, or promotion basis; causal/application claims still require absent additional evidence.
  - protected_id: PCR-063
    prior_locator: "Contribution, innovation, impact, application, and closest-work comparison > Verified representative closest-work comparison"
    revised_locator: "Contribution, innovation, impact, application, and closest-work comparison > Verified representative closest-work comparison; Risks, alternatives, and stop conditions > closest-work row"
    semantic_status: preserved
    evidence: >-
      New-algorithm, global-first, first-in-field, worldwide-absence, and patent-absence claims remain unsupported; stronger novelty still requires expanded searches and the current position remains conditional with low-to-moderate gap confidence.
  - protected_id: PCR-064
    prior_locator: "Expected outputs, falsification criteria, and interpretations > Interpretation matrix; Research design and methods > 试验观测映射和独立分析"
    revised_locator: "Expected outputs, falsification criteria, and interpretations > Interpretation matrix; Research design and methods > 试验观测映射和独立分析; Limitations and boundary conditions > 11"
    semantic_status: preserved
    evidence: >-
      Trial visit-outcome differences still cannot validate latent dynamics, transition edges, measurement-external structure, or the whole stage-II system; trials remain separate and subgroup selection cannot change the primary interpretation.
undeclared_scientific_changes: []
findings: []
unresolved_issues: []
---

# Content-preservation check

## Decision rationale

The decision is `scientific_content_preserved`. The five machine-facing identity anchors are verbatim identical in register v007, v055, and v056. All 64 source-present protected items remain traceable with the same scientific meaning, evidentiary status, feasibility qualification, claim strength, numerical or temporal rule, contingency, and failure consequence. The revision delta declares editorial repair only, and direct comparison found no undeclared scientific addition, no planned result presented as completed, no weakened limitation, and no strengthened claim.

The conditional trial extension retains its full branch structure. Stage-II conjunctive success and original-source verification remain shared prerequisites; mapping eligibility and fidelity remain confined to the mapping branch; failure of that branch does not erase the independently eligible SOFA endpoint; unverifiable core trial semantics still stop all new visit-outcome analyses. Stage III remains after the 24-month stage-I–II minimum and cannot count toward, bypass, supplement, or repair stage-II success.

## Identity-anchor verification

| Field | Prior and register locator | Revised locator | Result |
|---|---|---|---|
| `primary_research_question` | register v007 `identity_anchor.primary_research_question`; v055 frontmatter | v056 frontmatter `identity_anchor.primary_research_question` | Verbatim match |
| `primary_objective` | register v007 `identity_anchor.primary_objective`; v055 frontmatter | v056 frontmatter `identity_anchor.primary_objective` | Verbatim match |
| `study_object` | register v007 `identity_anchor.study_object`; v055 frontmatter | v056 frontmatter `identity_anchor.study_object` | Verbatim match |
| `core_data_or_evidence_base` | register v007 `identity_anchor.core_data_or_evidence_base`; v055 frontmatter | v056 frontmatter `identity_anchor.core_data_or_evidence_base` | Verbatim match |
| `primary_unit_of_inference` | register v007 `identity_anchor.primary_unit_of_inference`; v055 frontmatter | v056 frontmatter `identity_anchor.primary_unit_of_inference` | Verbatim match |

Identity-anchor result: **5/5 preserved verbatim**.

## Protected-content trace

- PCR-001 through PCR-064 are each checked exactly once above; the result is **64/64 preserved**.
- Repeated descriptions of the conditional trial extension were removed from the title/summary, abstract, background, significance, rationale, and contribution overview. Its complete scientific authority remains in `Research design and methods > 试验观测映射和独立分析`, with the subordinate question, objective, milestone, work package, evidence chain, outputs, interpretations, limitations, and risks retaining only their local scientific function.
- Trial-specific technical repetition in `Key techniques and implementation`, the trial evidence chain, `Required analyses and evidence`, and the trial working-assumption row was compressed. The complete anchor-eligibility, SVD/proxy, fidelity, ordered-outcome, probability-index, analysis-set, missingness, multiplicity, subgroup, and stop rules remain unchanged at the method authority.
- The eleven complete limitation families remain once, without weakening, in `Limitations and boundary conditions`. Necessary local statements of current fact, method eligibility, falsification consequence, interpretation, and risk response remain where they govern the connected scientific decision.
- Repeated stage-III statements were reduced, while the post-24-month dependency, separate-trial status, no-pooling rule, and inability to count toward or repair stage II remain explicit at the milestone, WP5, fixed minimum route, trial-method authority, and limitation authority.
- Feasibility and evidence status remain unchanged: access, personnel commitments, dual-database support, trial authorization and semantics, common anchors and units, and every new model or analysis result remain unverified or not yet generated as applicable.

## Required routing

The dossier may proceed to fresh narrative and academic-language assessment. Any later substantive change requires a new protected-content comparison before promotion.
