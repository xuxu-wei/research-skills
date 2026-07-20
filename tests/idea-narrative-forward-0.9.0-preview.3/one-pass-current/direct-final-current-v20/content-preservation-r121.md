---
schema_version: research-idea-content-preservation-check.v1
check_id: content-preservation-I01-001-r121
review_id: content-preservation-I01-001-r121
reviewer_skill: idea-narrative-assessor
reviewer_instance_id: fresh-preservation-r121
workflow_id: RID-SEPSIS-CSM-20260717-001
round_id: r121
input_artifact_ids:
  - idea-dossier-I01-001-v053
  - idea-dossier-I01-001-v054
  - protected-content-register-I01-001-v053-v005
  - revision-delta-I01-001-v053-to-v054
input_versions:
  - v053
  - v054
  - v005
  - v053-to-v054
inputs:
  prior_dossier:
    artifact_id: idea-dossier-I01-001-v053
    version: v053
    path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v19/idea-dossier-v053.md
  revised_dossier:
    artifact_id: idea-dossier-I01-001-v054
    version: v054
    path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v20/idea-dossier-v054.md
  protected_content_register:
    artifact_id: protected-content-register-I01-001-v053-v005
    version: v005
    path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v19/protected-content-register-v005.yaml
  revision_delta:
    artifact_id: revision-delta-I01-001-v053-to-v054
    version: v053-to-v054
    path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v20/revision-delta-v053-to-v054.md
files_read:
  - tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v19/idea-dossier-v053.md
  - tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v20/idea-dossier-v054.md
  - tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v19/protected-content-register-v005.yaml
  - tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v20/revision-delta-v053-to-v054.md
isolation_mode: fresh_subagent
prior_scores_visible: false
source_edits_performed: false
decision: scientific_content_preserved
protected_item_checks:
  - protected_id: PCR-001
    prior_locator: "frontmatter > identity_anchor"
    revised_locator: "frontmatter > identity_anchor"
    semantic_status: preserved
    evidence: "All five identity-anchor strings are byte-for-byte identical between v053 and v054."
  - protected_id: PCR-002
    prior_locator: "Research question, objectives, and core hypothesis > Primary research question; Objectives"
    revised_locator: "Research question, objectives, and core hypothesis > Primary research question; Objectives"
    semantic_status: preserved
    evidence: "The full-course question, four objectives, subordinate trial extension, and paper/evidence objective are line-for-line unchanged."
  - protected_id: PCR-003
    prior_locator: "Research question, objectives, and core hypothesis > Core hypothesis and evidence boundary"
    revised_locator: "Research question, objectives, and core hypothesis > Core hypothesis and evidence boundary"
    semantic_status: preserved
    evidence: "The recoverable-invariant hypothesis and noncausal evidentiary boundary are unchanged."
  - protected_id: PCR-004
    prior_locator: "Research design and methods > Observational target, anchoring, and evidence-qualified interpretation"
    revised_locator: "Research design and methods > Observational target, anchoring, and evidence-qualified interpretation"
    semantic_status: preserved
    evidence: "Study object, patient-time/state-transition unit, clustering, and joint observational target remain unchanged."
  - protected_id: PCR-005
    prior_locator: "Research design and methods > Protocol locks for the two primary clinical tasks"
    revised_locator: "Research design and methods > Protocol locks for the two primary clinical tasks"
    semantic_status: preserved
    evidence: "Cohort eligibility, first-onset handling, landmark weighting, competing terminations, and recovery/discharge distinction are unchanged."
  - protected_id: PCR-006
    prior_locator: "Research design and methods > Mutually exclusive post-onset state and event system"
    revised_locator: "Research design and methods > Mutually exclusive post-onset state and event system"
    semantic_status: preserved
    evidence: "The 12-hour assignment, six-state priority, absorbing/terminal behavior, relapse, and unsortable-time rule are unchanged."
  - protected_id: PCR-007
    prior_locator: "Data, materials, and existing evidence base > Variable roles"
    revised_locator: "Data, materials, and existing evidence base > Variable roles"
    semantic_status: preserved
    evidence: "Y/A/M/B and label-only separation, isolated dual-use copies, and missingness/interface boundaries are unchanged."
  - protected_id: PCR-008
    prior_locator: "Data, materials, and existing evidence base > Public intensive-care database roles and support audit"
    revised_locator: "Data, materials, and existing evidence base > Public intensive-care database roles and support audit"
    semantic_status: preserved
    evidence: "MIMIC/eICU roles, backup substitution timing, and common-concept eligibility are unchanged."
  - protected_id: PCR-009
    prior_locator: "Data, materials, and existing evidence base > Public intensive-care database roles and support audit > audit table"
    revised_locator: "Data, materials, and existing evidence base > Public intensive-care database roles and support audit > audit table"
    semantic_status: preserved
    evidence: "All audit fields, hospital/event/transition minima, anchor coverage, complexity limits, and time-grid fallback rules are unchanged."
  - protected_id: PCR-010
    prior_locator: "Data, materials, and existing evidence base > Current resource and result status"
    revised_locator: "Data, materials, and existing evidence base > Current resource and result status"
    semantic_status: preserved
    evidence: "Verified database existence is still separated from unverified access/support, and no planned result is presented as completed."
  - protected_id: PCR-011
    prior_locator: "Data, materials, and existing evidence base > Local randomized-trial evidence status"
    revised_locator: "Data, materials, and existing evidence base > Local randomized-trial evidence status"
    semantic_status: preserved
    evidence: "EXIT-SEP and XBJ-SCAP counts, derivative-report status, missing fields, and unverified D-dimer-unit boundary are unchanged."
  - protected_id: PCR-012
    prior_locator: "Data, materials, and existing evidence base > Current resource and result status > trial rows"
    revised_locator: "Data, materials, and existing evidence base > Current resource and result status > trial rows"
    semantic_status: preserved
    evidence: "Authorization, original-document, randomization, center, visit, outcome-semantic, anchor, and unit unknowns are unchanged."
  - protected_id: PCR-013
    prior_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Feasibility and resources"
    revised_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Feasibility and resources"
    semantic_status: preserved
    evidence: "Required roles, unverified commitments, model scope, and excluded animal/RCT/causal/control work remain unchanged."
  - protected_id: PCR-014
    prior_locator: "Research content and work packages > Work packages and minimum route"
    revised_locator: "Research content and work packages > Work packages and minimum route"
    semantic_status: preserved
    evidence: "The full precedence chain, fallback/stop consequences, 24-month minimum, and inability of trial work to bypass earlier failure are unchanged."
  - protected_id: PCR-015
    prior_locator: "Research content and work packages > Conjunctive minimum success definition"
    revised_locator: "Research content and work packages > Conjunctive minimum success definition"
    semantic_status: preserved
    evidence: "Every dual-database, simulation, primary-task, leakage, external-split, alignment, threshold, and stage-III exclusion conjunct is unchanged."
  - protected_id: PCR-016
    prior_locator: "Research design and methods > Protocol locks for the two primary clinical tasks > primary pre-onset task column"
    revised_locator: "Research design and methods > Protocol locks for the two primary clinical tasks > primary pre-onset task column"
    semantic_status: preserved
    evidence: "The 12-hour cumulative-incidence target, landmarks/history, metrics, clustered uncertainty, and success criteria are unchanged."
  - protected_id: PCR-017
    prior_locator: "Research design and methods > Protocol locks for the two primary clinical tasks > primary post-onset task column"
    revised_locator: "Research design and methods > Protocol locks for the two primary clinical tasks > primary post-onset task column"
    semantic_status: preserved
    evidence: "Day-7 favorable occupancy, component reporting, multistate/Aalen-Johansen method, sensitivity, and non-reversal rule are unchanged."
  - protected_id: PCR-018
    prior_locator: "Research design and methods > Protocol locks for the two primary clinical tasks > event clock and information-availability clock"
    revised_locator: "Research design and methods > Protocol locks for the two primary clinical tasks > event clock and information-availability clock"
    semantic_status: preserved
    evidence: "Infection pairing, baseline/rolling SOFA, onset and availability clocks, exclusions, and the two sensitivity labels are unchanged."
  - protected_id: PCR-019
    prior_locator: "Research design and methods > Mutually exclusive post-onset state and event system > state definitions"
    revised_locator: "Research design and methods > Mutually exclusive post-onset state and event system > state definitions"
    semantic_status: preserved
    evidence: "Recovery, deterioration/new organ failure, exit, transfer/lost observation, and death definitions are unchanged."
  - protected_id: PCR-020
    prior_locator: "Research design and methods > Observational target, anchoring, and evidence-qualified interpretation"
    revised_locator: "Research design and methods > Observational target, anchoring, and evidence-qualified interpretation"
    semantic_status: preserved
    evidence: "Anchor/loadings, dimension/mechanism/lag limits, seed alignment, and interpretable-invariant restrictions are unchanged."
  - protected_id: PCR-021
    prior_locator: "Research design and methods > Observational target, anchoring, and evidence-qualified interpretation > missingness and action support"
    revised_locator: "Research design and methods > Observational target, anchoring, and evidence-qualified interpretation > missingness and action support"
    semantic_status: preserved
    evidence: "Measurement-model baseline, five pattern-mixture shifts, tipping analysis, overlap/ESS thresholds, and no-treatment-effect consequence are unchanged."
  - protected_id: PCR-022
    prior_locator: "Research design and methods > Absolute simulation and semi-synthetic recovery criteria > simulation regimen"
    revised_locator: "Research design and methods > Absolute simulation and semi-synthetic recovery criteria > simulation regimen"
    semantic_status: preserved
    evidence: "Months, repeat/Monte-Carlo rule, generator set, and crossed misspecification factors are unchanged."
  - protected_id: PCR-023
    prior_locator: "Research design and methods > Absolute simulation and semi-synthetic recovery criteria > continuous branch"
    revised_locator: "Research design and methods > Absolute simulation and semi-synthetic recovery criteria > continuous branch"
    semantic_status: preserved
    evidence: "Evaluation rows, all-dimension minimum canonical correlation, zero assignment, lower-bound formula, 0.80 criterion, and result-blind fixation are unchanged."
  - protected_id: PCR-024
    prior_locator: "Research design and methods > Absolute simulation and semi-synthetic recovery criteria > recovery criteria table"
    revised_locator: "Research design and methods > Absolute simulation and semi-synthetic recovery criteria > recovery criteria table"
    semantic_status: preserved
    evidence: "All state, transition, sign/lag, edge, zero-edge, misspecification, calibration, seed/bootstrap/external, and failure-action rules are unchanged."
  - protected_id: PCR-025
    prior_locator: "Research design and methods > Hospital-primary cross-database validation > partition and cross-hospital-patient rules"
    revised_locator: "Research design and methods > Hospital-primary cross-database validation > partition and cross-hospital-patient rules"
    semantic_status: preserved
    evidence: "Seeded hospital split, patient exclusions, sensitivity, support triggers, backup, and narrowed-claim consequence are unchanged."
  - protected_id: PCR-026
    prior_locator: "Research design and methods > Hospital-primary cross-database validation > four update operations"
    revised_locator: "Research design and methods > Hospital-primary cross-database validation > four update operations"
    semantic_status: preserved
    evidence: "The four ordered update operations, pre-test freeze, prohibited test-driven choices, and non-compensation rule are unchanged."
  - protected_id: PCR-027
    prior_locator: "Research design and methods > Conditional trial-observation mapping and independent analysis > Shared prerequisites"
    revised_locator: "Research design and methods > 试验观察映射和独立分析 > 共享前提"
    semantic_status: preserved
    evidence: "The complete trial section moved after secondary diagnostics; stage-II success, authorization, original-semantic verification, branch-specific mapping eligibility, timing, secondary status, and separate-trial rules are unchanged."
  - protected_id: PCR-028
    prior_locator: "Research design and methods > Conditional trial-observation mapping and independent analysis > observation mapping eligibility and fidelity"
    revised_locator: "Research design and methods > 试验观察映射和独立分析 > 观测映射成立时的有序访视结局分析"
    semantic_status: preserved
    evidence: "All anchor eligibility, frozen scaling/SVD mapping, sign/tie rules, external-fidelity thresholds, blinded-trial coverage, and failure conditions remain; 'Frobenius energy' was only clarified as the first-axis explained proportion, still at 50%."
  - protected_id: PCR-029
    prior_locator: "Research design and methods > Conditional trial-observation mapping and independent analysis > stratified standardized probability index"
    revised_locator: "Research design and methods > 试验观察映射和独立分析 > 分层标准化概率指数公式与确认规则"
    semantic_status: preserved
    evidence: "Outcome ordering, unique theta_PI estimand, formula, direction, half-credit ties, strata, pooled-arm weights, separate trials, and secondary-only alternatives are unchanged."
  - protected_id: PCR-030
    prior_locator: "Research design and methods > Conditional trial-observation mapping and independent analysis > fallback and stop branches"
    revised_locator: "Research design and methods > 试验观察映射和独立分析 > 观测映射不成立但独立分析条件成立时的分析; 核心语义不足时停止"
    semantic_status: preserved
    evidence: "The independent ordered-SOFA fallback remains available after mapping failure, while unverified visit/randomization/center/outcome semantics still stop new visit analyses."
  - protected_id: PCR-031
    prior_locator: "Research design and methods > Conditional trial-observation mapping and independent analysis > trial table"
    revised_locator: "Research design and methods > 试验观察映射和独立分析 > trial table"
    semantic_status: preserved
    evidence: "Both trial populations, actual visits, analysis sets, missingness/imputation/bounds, structural absences, Holm family, subgroup interactions, and stop rules are unchanged."
  - protected_id: PCR-032
    prior_locator: "Research design and methods > Secondary representation diagnostics"
    revised_locator: "Research design and methods > Secondary representation diagnostics"
    semantic_status: preserved
    evidence: "The complete diagnostic paragraph moved intact before the trial section; metrics, strata, pseudo-mask scope, and non-reversal role are identical."
  - protected_id: PCR-033
    prior_locator: "Required analyses and evidence"
    revised_locator: "Required analyses and evidence; Research design and methods > 试验观察映射和独立分析"
    semantic_status: preserved
    evidence: "All stage-II evidence requirements remain unchanged. The repeated trial checklist was consolidated to authorization, original semantics, trial-specific eligibility, and execution of the fixed method; every removed trial detail remains fully authoritative in the relocated trial-method subsection."
  - protected_id: PCR-034
    prior_locator: "Expected outputs, falsification criteria, and interpretations > Falsification and stop criteria > clocks, leakage, and data support"
    revised_locator: "Expected outputs, falsification criteria, and interpretations > Falsification and stop criteria > 时钟与信息泄漏; 数据支持"
    semantic_status: preserved
    evidence: "Leakage correction/deletion, external-test blocking, support-driven simplification/backup, and stop consequences are unchanged."
  - protected_id: PCR-035
    prior_locator: "Expected outputs, falsification criteria, and interpretations > Falsification and stop criteria > recovery, missingness, action support, and external result"
    revised_locator: "Expected outputs, falsification criteria, and interpretations > Falsification and stop criteria > 绝对恢复; 非随机缺失与行动支持; 外部结果"
    semantic_status: preserved
    evidence: "Recovery non-promotion, sensitivity reporting, no-effect interpretation under poor overlap, and no-update external failure consequences are unchanged."
  - protected_id: PCR-036
    prior_locator: "Expected outputs, falsification criteria, and interpretations > Falsification and stop criteria > trial criteria"
    revised_locator: "Research design and methods > 试验观察映射和独立分析; Expected outputs, falsification criteria, and interpretations > Falsification and stop criteria > 试验观测映射; 试验核心语义"
    semantic_status: preserved
    evidence: "The stop section now invokes the fixed mapping eligibility/fidelity authority instead of repeating each component; mapping-outcome blocking, independent-SOFA fallback, core-semantic stop, direction/imprecision interpretation, and no subgroup repair are all retained."
  - protected_id: PCR-037
    prior_locator: "Expected outputs, falsification criteria, and interpretations > Falsification and stop criteria > time"
    revised_locator: "Expected outputs, falsification criteria, and interpretations > Falsification and stop criteria > 时间"
    semantic_status: preserved
    evidence: "Month-12 simple-route freeze, month-20 no-test-access, and month-24 incomplete-stage-II consequences are unchanged."
  - protected_id: PCR-038
    prior_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Risks, alternatives, and stop conditions"
    revised_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Risks, alternatives, and stop conditions"
    semantic_status: preserved
    evidence: "All access/support, staffing, test-contamination, cross-hospital, trial-semantic, and novelty contingencies and consequences are unchanged."
  - protected_id: PCR-039
    prior_locator: "Title, summary, audience, and positioning; Structured abstract"
    revised_locator: "Title, summary, audience, and positioning; Structured abstract"
    semantic_status: preserved
    evidence: "Candidate/planned status, planned outputs, conditional integration contribution, and subordinate trial extension are unchanged."
  - protected_id: PCR-040
    prior_locator: "Contribution, innovation, impact, application, and closest-work comparison > Contribution and evidence ladder"
    revised_locator: "Contribution, innovation, impact, application, and closest-work comparison > Contribution and evidence ladder"
    semantic_status: preserved
    evidence: "Every evidence tier and claim ceiling is unchanged; the trial-evidence row only replaces a stale section-number pointer with the named method subsection."
  - protected_id: PCR-041
    prior_locator: "Contribution, innovation, impact, application, and closest-work comparison > Verified representative closest-work comparison"
    revised_locator: "Contribution, innovation, impact, application, and closest-work comparison > Verified representative closest-work comparison"
    semantic_status: preserved
    evidence: "All precedents, bounded-search date, confidence levels, and conditional integration rather than novelty/global-first position are unchanged."
  - protected_id: PCR-042
    prior_locator: "Expected outputs, falsification criteria, and interpretations > Interpretation matrix"
    revised_locator: "Expected outputs, falsification criteria, and interpretations > Interpretation matrix"
    semantic_status: preserved
    evidence: "All seven result patterns retain the same allowed and prohibited interpretations, including separate mapping and SOFA trial outcomes."
  - protected_id: PCR-043
    prior_locator: "Research design and methods > Conditional trial-observation mapping and independent analysis; Evidence chain: conditional randomized-trial secondary analysis"
    revised_locator: "Research design and methods > 试验观察映射和独立分析; Evidence chain: 有前置条件的随机试验次要分析; Planned outputs"
    semantic_status: preserved
    evidence: "Separate secondary trial reporting or audit-only output, noncontribution to stage-II success, no pooled effect/common mechanism, and bounded randomization interpretation remain unchanged."
  - protected_id: PCR-044
    prior_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Working assumptions > continuous latent-state recovery row"
    revised_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Working assumptions > continuous latent-state recovery row"
    semantic_status: preserved
    evidence: "WA-R117-01's definition, owner, deadline, failure consequence, affected component, and result-blinded re-review condition are line-for-line unchanged in the dossier."
  - protected_id: PCR-045
    prior_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Working assumptions > trial probability-index row"
    revised_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Working assumptions > trial probability-index row"
    semantic_status: preserved
    evidence: "WA-R117-02's unique probability index, tie handling, strata/weights, confirmation owner and timing, stop consequence, and stage-I/II independence are unchanged."
  - protected_id: PCR-046
    prior_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Working assumptions > clinical-scale-to-simulation mapping row"
    revised_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Working assumptions > clinical-scale-to-simulation mapping row"
    semantic_status: preserved
    evidence: "Month-7 information sources, fixed generators/targets, external-result exclusion, and no-start/no-promotion consequence are unchanged."
  - protected_id: PCR-047
    prior_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Working assumptions > multicategory-calibration row"
    revised_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Working assumptions > multicategory-calibration row"
    semantic_status: preserved
    evidence: "Month-6 inputs, fixed metrics/thresholds, tighten-not-relax rule, and no-success/no-test-access consequence are unchanged."
  - protected_id: PCR-048
    prior_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Limitations and boundary conditions > 1. Resources, access, and team status"
    revised_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Limitations and boundary conditions > 1. 资源、访问与团队状态"
    semantic_status: preserved
    evidence: "The complete resource/access/team limitation remains line-for-line at the sole limitations authority."
  - protected_id: PCR-049
    prior_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Limitations and boundary conditions > 2. Labels, clocks, and leakage"
    revised_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Limitations and boundary conditions > 2. 标签、时钟与信息泄漏"
    semantic_status: preserved
    evidence: "The complete label/clock/leakage limitation remains line-for-line at the sole limitations authority."
  - protected_id: PCR-050
    prior_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Limitations and boundary conditions > 3. State recoverability and structural scope"
    revised_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Limitations and boundary conditions > 3. 状态可恢复性与结构范围"
    semantic_status: preserved
    evidence: "The complete recoverability/scope limitation and deletion/merge/qualification consequence remain line-for-line at the authority."
  - protected_id: PCR-051
    prior_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Limitations and boundary conditions > 4. Nonrandom missingness and low action overlap"
    revised_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Limitations and boundary conditions > 4. 非随机缺失与低行动重叠"
    semantic_status: preserved
    evidence: "The missing-physiology and no-treatment-effect boundaries remain line-for-line at the sole limitations authority."
  - protected_id: PCR-052
    prior_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Limitations and boundary conditions > 5. Cross-database evidence"
    revised_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Limitations and boundary conditions > 5. 跨数据库证据"
    semantic_status: preserved
    evidence: "The database-difference, interface-missingness, update-role, and non-compensation limitation remains line-for-line at the authority."
  - protected_id: PCR-053
    prior_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Limitations and boundary conditions > 6. Time and delivery boundary"
    revised_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Limitations and boundary conditions > 6. 时间与交付边界"
    semantic_status: preserved
    evidence: "The 24-month boundary, month-12/20/24 consequences, subordinate stage III, and inability of trial results to repair stage II remain line-for-line."
  - protected_id: PCR-054
    prior_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Limitations and boundary conditions > 7. Trial data and semantics"
    revised_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Limitations and boundary conditions > 7. 试验数据与语义"
    semantic_status: preserved
    evidence: "Conditional trial-data access, original-material/semantic requirements, sparse-visit boundary, and no pooled effect remain line-for-line."
  - protected_id: PCR-055
    prior_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Limitations and boundary conditions > 8. Common anchors and observation mapping"
    revised_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Limitations and boundary conditions > 8. 共同生理锚点变量与观测映射"
    semantic_status: preserved
    evidence: "Candidate-anchor and unit uncertainty, absent fidelity results, mapping-only interpretation, and SOFA independence remain line-for-line."
  - protected_id: PCR-056
    prior_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Limitations and boundary conditions > 9. Closest-work uncertainty"
    revised_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Limitations and boundary conditions > 9. 最接近工作不确定性"
    semantic_status: preserved
    evidence: "The non-systematic search coverage and low-to-moderate complete-combination confidence remain line-for-line."
  - protected_id: PCR-057
    prior_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Limitations and boundary conditions > 10. Regulatory applicability"
    revised_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Limitations and boundary conditions > 10. 监管适用范围"
    semantic_status: preserved
    evidence: "The XueBiJing regulatory-applicability and no-unconditional-international-promotion limitation remains line-for-line."
  - protected_id: PCR-058
    prior_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Limitations and boundary conditions > 11. Complete prohibited claims"
    revised_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Limitations and boundary conditions > 11. 完整禁止主张"
    semantic_status: preserved
    evidence: "All causal, counterfactual, mechanism, mediation, control, digital-twin, latent-system validation, tool/platform, promotion, and subgroup-repair prohibitions remain line-for-line."
  - protected_id: PCR-059
    prior_locator: "Research content and work packages > 24-month minimum deliverables and milestones"
    revised_locator: "Research content and work packages > 24 个月最低交付与时间节点"
    semantic_status: preserved
    evidence: "Role signatures as responsibilities rather than commitments, custodian-controlled test isolation, and no post-month-20 external-result modification are unchanged."
  - protected_id: PCR-060
    prior_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Working assumptions > closing qualification"
    revised_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Working assumptions > closing qualification"
    semantic_status: preserved
    evidence: "The screening-not-ESS boundary, on-time resolution requirement, explicit consequences, and no post-hoc numerical invention are unchanged."
  - protected_id: PCR-061
    prior_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Limitations and boundary conditions > 11. Complete prohibited claims"
    revised_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Limitations and boundary conditions > 11. 完整禁止主张"
    semantic_status: preserved
    evidence: "Real causal network, treatment effect, counterfactual policy, mechanism, mediation, control, and digital-twin claims remain explicitly unsupported."
  - protected_id: PCR-062
    prior_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Limitations and boundary conditions > 11. Complete prohibited claims; Contribution and evidence ladder"
    revised_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Limitations and boundary conditions > 11. 完整禁止主张; Contribution and evidence ladder"
    semantic_status: preserved
    evidence: "Validated-model/tool/platform/effectiveness/promotion claims remain prohibited, and extra evidence required for causal/control/application claims remains explicit."
  - protected_id: PCR-063
    prior_locator: "Contribution, innovation, impact, application, and closest-work comparison > Verified representative closest-work comparison"
    revised_locator: "Contribution, innovation, impact, application, and closest-work comparison > Verified representative closest-work comparison"
    semantic_status: preserved
    evidence: "New-algorithm/global-first/absence claims remain unsupported, stronger novelty still requires expanded searches, and the bounded conditional position is unchanged."
  - protected_id: PCR-064
    prior_locator: "Expected outputs, falsification criteria, and interpretations > Interpretation matrix; Research design and methods > Conditional trial-observation mapping and independent analysis"
    revised_locator: "Expected outputs, falsification criteria, and interpretations > Interpretation matrix; Research design and methods > 试验观察映射和独立分析"
    semantic_status: preserved
    evidence: "The moved trial section and unchanged interpretation matrix still prohibit whole-system/latent-dynamics/edge validation, pooled effects, common mechanisms, and subgroup rescue."
undeclared_scientific_changes: []
findings: []
unresolved_issues: []
---

# Content-preservation check

## Decision rationale

`scientific_content_preserved`. The five identity-anchor values are exactly identical.
The dossier comparison contains 24 added and 24 removed lines, including lineage
frontmatter. In the scientific text, the secondary-diagnostics paragraph and the
complete conditional trial-analysis subsection were reordered without changing their
requirements. One sentence now states explicitly that the first singular axis explains
at least 50% of the (L_C) Frobenius energy; this clarifies the same numerator/threshold
rather than changing it. Repeated trial-analysis details in required evidence and stop
criteria were consolidated into the still-complete method authority, while the local
eligibility, consequence, and independent-SOFA branch functions remain present.

All 64 protected items are traceable with the same meaning and claim strength. The four
working assumptions retain their fixed content, owner/timing or information constraint,
and failure consequence. All 11 limitation families remain complete in the single
`Limitations and boundary conditions` authority. No new data, method, result, evidence,
claim-strength increase, conditional-to-unconditional conversion, hidden feasibility
issue, undeclared scientific change, or identity drift was found. The revision delta
also declares `scientific_change_declared: false`.

## Protected-content trace

- PCR-027 through PCR-031, PCR-043, and PCR-064 now resolve to `Research design and
  methods > 试验观察映射和独立分析`; the full branch prerequisites, mapping rules,
  probability-index estimand, independent SOFA fallback, stop conditions, trial-specific
  rules, and interpretation bounds remain together there.
- PCR-032 moved intact to immediately precede that trial subsection.
- PCR-033 and PCR-036 retain their local required-evidence and falsification functions;
  only duplicated technical detail was removed, with the complete protected meaning
  remaining at the method authority.
- PCR-040's evidence-ladder locator and the matching claim-support locator now name the
  method subsection instead of using a stale section number. Their evidence role and
  claim ceiling did not change.
- PCR-048 through PCR-058 and PCR-061 through PCR-062 remain in the sole limitations
  authority; consolidation elsewhere does not constitute deletion of protected meaning.

## Required routing

The revised dossier may proceed to fresh narrative and academic-language assessment.
