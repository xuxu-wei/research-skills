# TELE-HF90 final human-review package

**Package status:** `human_signoff_required`
**Final proposal:** v003
**Final SAP:** v002
**External submission:** not authorized
**Stop point:** PI review and signature

No browsing was performed, no citations or results were invented, and no repository/project files were written.

## 1. Final proposal v003

### Title

**TELE-HF90: A Pragmatic Multicenter Randomized Trial of 90-Day Connected Monitoring After Hospitalization for Acute Heart Failure**

### Core thesis and rationale

TELE-HF90 will determine whether assignment to 90 days of connected weight and symptom monitoring, centralized pharmacist-nurse review, and protocol-guided escalation reduces all-cause readmission or death through day 90 compared with usual post-discharge care.

Remote-monitoring effects in heart failure are heterogeneous. Implementation intensity is a plausible modifier, but neither benefit nor global novelty is assumed. The trial therefore tests the complete delivery strategy—including centralized review and escalation—under pragmatic conditions.

### Objectives

The primary objective is to estimate the day-90 intention-to-treat risk ratio for all-cause readmission or death.

Secondary objectives compare:

- Days alive and out of hospital through day 90.
- Heart-failure readmission.
- All-cause mortality.
- KCCQ change from baseline to day 90.

Safety objectives assess:

- Intervention-triggered emergency-department visits.
- Documented treatment-related hypotension.
- Documented treatment-related acute kidney injury.

Exploratory treatment-effect interactions are prespecified for hospital, LVEF stratum, sex, and age below 65 versus 65 or older.

### Design and population

TELE-HF90 is a pragmatic, parallel, individually randomized trial at six hospitals. It will enroll 2,600 adults before discharge home following an admission for acute heart failure.

Detailed eligibility definitions—including clinical confirmation, consent and capacity provisions, accessibility, caregiver support, device-use requirements, and relevant exclusions—must be finalized as PI-controlled protocol content before activation. No unsupplied eligibility threshold is inferred here.

### Intervention and comparator

Participants assigned to the intervention will receive 90 days of:

- Daily connected-weight monitoring.
- Daily connected-symptom monitoring.
- Review by a centralized pharmacist-nurse team.
- Escalation classified as routine, same-day clinician review, or urgent evaluation.

The exact clinical alert and escalation thresholds remain in a version-controlled, PI-approved protocol appendix. Before activation, that appendix must define responsibility, response times, after-hours coverage, failed-contact handling, emergency instructions, permitted clinical overrides, and documentation.

The comparator is usual post-discharge care without study-provided monitoring. Routine-care monitoring will not be prohibited; any overlap or contamination that is captured will be reported.

### Randomization and masking

Allocation will be 1:1 through concealed web randomization, stratified by:

- Hospital.
- LVEF below 40% versus 40% or higher.

Hospital will be represented analytically by five fixed indicators, with LVEF represented by one binary indicator. Individual randomization does not require cluster-design inflation.

Participants and intervention personnel cannot be blinded to monitoring delivery. Endpoint adjudication will be blinded to randomized assignment.

### Outcomes and ascertainment

The primary outcome is any all-cause readmission or death from index discharge through day 90.

Death will be obtained through the national death registry, is always counted as a primary event, and is nonmissing. Readmissions will be ascertained through the supplied hospital EHR feeds and blinded adjudication.

The adjudication charter must prospectively define qualifying admissions, observation stays, transfers, contiguous episodes, planned admissions, same-day events, date conflicts, and the handling of any outside-system event information encountered.

Hospital EHR feeds may not capture all outside-system readmissions. Because the intervention could influence where care is sought, this under-ascertainment could be differential by group. No additional ascertainment source is assumed. This remains an explicit identification limitation addressed through completeness monitoring and prespecified sensitivity analyses, but it cannot be eliminated statistically without validation data.

Primary reporting will include:

- Arm-specific composite risks.
- Adjusted risk ratio and 95% confidence interval.
- Supportive risk difference.
- Separate readmission and mortality components.

### Primary estimand and analysis

The primary estimand comprises:

- **Population:** all randomized participants.
- **Treatment conditions:** assignment to TELE-HF90 versus usual care.
- **Intercurrent-event strategy:** treatment policy; participants remain analyzed by assignment regardless of adherence, crossover, discontinuation, or subsequent care.
- **Variable:** occurrence of all-cause readmission or death through day 90.
- **Summary measure:** intervention-to-control risk ratio.

The primary analysis will use log-binomial regression with treatment, hospital, and LVEF stratum covariates. If the model meets prespecified convergence, boundary, admissibility, or estimability failure criteria, modified Poisson regression with participant-level robust variance will be used.

The primary endpoint alone controls the study-wise two-sided alpha of 0.05. Secondary, safety, subgroup, component, and sensitivity analyses are supportive or exploratory and use nominal confidence intervals and P values.

### Missing primary-outcome data

Death is never imputed. Confirmed death fixes the composite as an event regardless of readmission completeness.

Among participants confirmed alive through day 90:

- Observed qualifying readmission fixes the composite as an event.
- Complete ascertainment with no qualifying readmission fixes a non-event.
- Only unresolved all-cause readmission status is eligible for imputation.

The primary missing-data implementation uses multiple imputation under MAR. Complete-case and delta-adjusted MNAR analyses are sensitivity analyses. Full executable specifications are in SAP v002.

### Secondary and safety analyses

Days alive and out of hospital will be bounded from 0 to 90, with death assigned zero, and analyzed supportively using an adjusted mean difference with robust inference.

HF readmission and mortality will use adjusted binary risk-ratio models analogous to the primary model.

KCCQ will use a constrained longitudinal model with baseline included as a response and a treatment-by-time contrast at day 90. A worst-rank-for-death analysis will rank deaths below all surviving KCCQ outcomes.

Safety outcomes will be summarized by randomized group as participant incidence and event counts. Treatment attribution, risk windows, severity, recurrence, and any supportive exposure-based presentation require final protocol signoff.

Subgroup analyses will use treatment-by-subgroup interactions. Hospital heterogeneity will use a joint five-degree-of-freedom interaction test. Findings remain exploratory.

### Intervention fidelity, workload, and equity

Prespecified implementation measures will include:

- Adherence days and missing transmissions.
- Alert counts and classifications.
- Review latency.
- Contact success.
- Escalation initiation and completion.
- Documented clinical action.
- Central-team workload and peak demand.
- Protocol crossover and usual-care monitoring.
- Accommodations and unresolved barriers involving language, disability, digital access, cognition, or caregiver support.

These measures support interpretation and do not replace the intention-to-treat estimand.

### Blinded aggregate review

One pooled blinded review will occur when total enrollment reaches N=1,300.

Permitted information is limited to aggregate recruitment, follow-up completion, EHR/registry linkage completeness, missingness, data quality, endpoint-processing status, KCCQ operability, and operational performance.

The review may support procedural improvements but may not:

- Reveal arm-specific summaries.
- Estimate treatment effects.
- test efficacy or futility.
- Change sample size.
- Modify endpoints or inferential methods using comparative outcomes.
- Apply an efficacy stopping rule.

No interim efficacy analysis is planned.

### Sample size and feasibility

Planning assumptions are:

- Usual-care primary-event risk: 30%.
- Target intervention risk: 24%.
- Two-sided alpha: 0.05.
- Power: 90%.
- Allocation: 1:1.
- Supplied independently calculated analyzable N: 2,300.
- Inflation for up to 10% incomplete non-death ascertainment: \(2,300/0.90=2,556\).
- Rounded randomized target: 2,600.

Recruitment capacity stated as six sites × 18 participants/site/month × 24 months equals 2,592, eight below the randomized target. This discrepancy requires an explicit operational resolution before activation; it is not silently corrected here.

Recruitment lasts 24 months. Intervention and follow-up overlap recruitment and extend through approximately month 27. Closeout lasts six months, all within a 42-month award.

Devices and EHR integration are already contracted. Staffing includes the centralized pharmacist-nurse team, site coordinators, statistician, data manager, and endpoint committee.

### Budget

The funding envelope is USD 2.4 million. Final allocation must remain within this total and cover the supplied staffing, site operations, monitoring, data management, statistics, adjudication, safety and quality activities, contracted device/EHR obligations, and closeout. No unsupported dollar split is assigned.

### Principal risks

The package retains the following risks:

- The 2,592-versus-2,600 recruitment discrepancy.
- Potentially differential outside-system readmission under-ascertainment.
- Alert burden, delayed response, and insufficient after-hours coverage.
- Variable implementation and usual-care contamination.
- Missing KCCQ and death-related truncation.
- Device, connectivity, EHR, or randomization-system failure.
- Treatment-related hypotension or kidney injury.
- Overinterpretation of exploratory subgroup findings.

### PI go/no-go attestations

Before launch, the PI must affirm that:

- Eligibility criteria and endpoint definitions are finalized.
- The escalation-threshold appendix is approved and version-locked.
- Response ownership, after-hours coverage, overrides, and failed-contact rules are operational.
- The eight-participant recruitment discrepancy has an approved resolution.
- The EHR-only readmission limitation and potentially differential capture risk are accepted.
- The N=1,300 blinded-review charter is approved.
- Safety definitions, attribution rules, and oversight authority are established.
- Workload, contamination, fidelity, and equity monitoring are operational.
- Required ethics, privacy, institutional, and data-governance approvals are complete.
- The USD 2.4M budget and 42-month schedule are reconciled.
- SAP v002 is approved as the controlling executable analysis document.
- Preserved panel dissent has been reviewed.

## 2. Final SAP v002

### Governance and analysis populations

The SAP must be signed before comparative unblinding and, where feasible, before database lock. Subsequent changes require versioning, justification, timing, and disclosure of whether treatment information was available.

The primary efficacy and participant-incidence safety population is all randomized participants analyzed by assigned group. No per-protocol population is used for confirmatory inference.

### Primary endpoint derivation

Day 0 is index hospital discharge. The analysis interval extends through day 90.

A primary event occurs with either:

- Confirmed death through day 90; or
- At least one qualifying all-cause readmission through day 90.

Vital status is always ascertained and nonmissing through the national death registry. Confirmed death fixes the composite as an event, irrespective of incomplete readmission information.

Among confirmed day-90 survivors, unresolved all-cause readmission status is the only imputed primary component.

Exact timestamp inclusivity, date-only fallback, observation-stay rules, transfers, planned admissions, and adjudication precedence remain approval items.

### Primary model

The log-binomial model includes:

- Randomized treatment.
- Five hospital indicators.
- Binary LVEF stratum.

The treatment coefficient estimates the adjusted risk ratio.

Modified Poisson regression with participant-level robust sandwich variance replaces the log-binomial model if it fails prespecified convergence or admissibility criteria, including nonconvergence, nonestimable coefficients, materially invalid fitted probabilities, boundary termination, singular information, or inability to estimate the treatment interval reliably.

Arm-specific risks, unadjusted effects, adjusted risk ratio, and a supportive standardized risk difference will be reported.

### Multiple imputation

Multiple imputation under MAR applies only to unresolved all-cause readmission status among participants confirmed alive through day 90.

The proposed implementation for signoff is:

- 50 imputations, increased if Monte Carlo error is excessive.
- Logistic fully conditional specification.
- Predictors including treatment, hospital, LVEF stratum, available endpoint information, follow-up-completeness indicators, prespecified baseline covariates, and approved auxiliary predictors.
- Fixed seeds and retained diagnostics.
- Primary-model fitting in every completed dataset.
- Rubin’s-rule pooling of log-risk-ratio estimates and variances.

Death and vital status are never imputed.

Sensitivity analyses include:

- Complete-case analysis.
- Modified-Poisson analysis.
- Delta-adjusted pattern-mixture MI.
- Deterministic extreme-case bounds.
- Tipping-point expansion.

The proposed delta grid is −1.0, −0.5, 0, 0.5, and 1.0 on the log-odds scale, including asymmetric scenarios that make missing intervention outcomes worse. The final grid requires statistician approval.

### Secondary outcomes

**DAOH90:** bounded 0–90 with post-death days equal to zero. The principal contrast is the adjusted mean difference using linear regression with hospital and LVEF adjustment and HC3 robust standard errors. A stratification-respecting bootstrap is supportive.

**HF readmission:** binary adjusted risk-ratio analysis using the primary model and fallback. Death is not itself an HF-readmission event. Any competing-event analysis is supportive.

**Mortality:** adjusted day-90 risk-ratio analysis. Kaplan–Meier curves and Cox modeling may be supportive.

**KCCQ:** constrained longitudinal analysis with baseline and day-90 scores modeled jointly. Fixed effects include visit, treatment-by-visit, hospital, and LVEF; equal baseline group means are imposed. The treatment-by-day-90 contrast estimates the adjusted difference.

KCCQ sensitivities include complete-case ANCOVA, survivor MI, and worst-rank death. Deaths rank below all survivors; earlier death ranks worse than later death; same-day deaths tie.

### Safety and subgroups

Safety tables will report:

- Participants with at least one event.
- Total and recurrent events.
- Severity, seriousness, and attribution.
- Time to first event.
- Events leading to interruption or discontinuation, if applicable.

All safety inference is nominal.

Interaction tests are specified for hospital, LVEF, sex, and age category. Hospital uses a joint five-degree-of-freedom interaction test. No within-subgroup significance comparison establishes heterogeneity.

### Multiplicity and outputs

Only the primary composite controls alpha at two-sided 0.05. All other analyses are supportive or exploratory.

Planned outputs include participant flow, baseline characteristics, primary estimates and sensitivities, component outcomes, DAOH, HF readmission, mortality, KCCQ, safety, completeness/missingness, subgroup interactions, adherence, protocol deviations, and data-quality findings.

### Reproducibility and lock

Before analysis:

- Outcome definitions, code lists, windows, and derivations are frozen.
- Randomization is reconciled.
- Transfers, duplicate admissions, death records, and adjudication records are reconciled.
- Analysis datasets are versioned and checksummed.
- Software versions and random seeds are controlled.
- The primary derivation and estimate receive independent validation.
- Lock, unmasking, SAP approval, and program-release timestamps are retained.

## 3. Independent evaluations and revision record

| Stage | Frozen artifact | Instance | Decision |
|---|---|---|---|
| Readiness | Concept v001 | `/root/readiness_telehf90` | `ready_for_proposal` |
| Proposal evaluation 1 | Proposal v001 | `proposal-evaluator-telehf90-eval001-20260712-a7f3` | `accept` |
| Method/statistics preflight | Frozen design | `/root/method_preflight` | Initially blocked; amended to `ready_for_sap` after distinguishing statistical choices from invented facts |
| SAP evaluation 1 | SAP v001 | `sap-eval-001` | `revise` |
| SAP evaluation 2 | SAP v002 | `sap-eval-002` | `accept` |
| Proposal evaluation 2 | Proposal v002 | `/root/proposal_eval_v2` | `accept` |
| Proposal evaluation 3 | Proposal v003 | `TELE-HF90-proposal-evaluator-003` | `accept` |
| Language QA | Proposal v003 | `TELE-HF90-language-001` | `pass` |

Revision rounds:

- **Proposal round 1:** v001 → v002, substantive clarification after panel-001.
- **Proposal round 2:** v002 → v003, editorial consolidation. An erroneous draft reference to “N=1,300 per arm” and “regression discontinuity” was rejected before freezing; canonical v003 correctly uses one pooled review at total N=1,300 and “risk difference.”
- **SAP round 1:** v001 → v002, explicitly restricting primary imputation to unresolved all-cause readmission among confirmed survivors and fixing every death as a composite event.

No third revision round was required.

## 4. Final blind panel

Panel-003 used three fresh, mutually blinded roles against proposal v003:

| Role | Recommendation |
|---|---|
| Practicing clinician/domain | Support funding with pre-activation conditions |
| Methodology/statistics | Conditional accept; no fatal or blocking flaw |
| Submission guard | Proceed to final PI review |

No reviewer saw prior scores, decisions, deltas, SAP contents, unresolved-issue files, or peer outputs. No reviewer edited the proposal.

### Preserved dissent

The central minority concern is not suppressed:

> Outside-system readmission capture may be differential by randomized group. Multiple imputation, complete-case analysis, and delta sensitivities can test assumptions but cannot establish identification if substantial differential under-capture exists without validation data.

The clinician additionally conditions activation on finalized escalation ownership, after-hours coverage, staffing/workload safeguards, and locked clinical thresholds.

The submission guard found v003 clearer than a clean first draft, subject to mechanical confirmation that every governing rule has exactly one authoritative location and unambiguous cross-references.

## 5. Compact execution receipt

```yaml
workflow_id: TELE-HF90-STD-SAP-001
plugin_version: 0.5.0-preview.1
entry_mode: standard
status: human_signoff_required
sap_requested: true

final_artifacts:
  proposal:
    artifact_id: proposal-telehf90
    version: v003
    path: memory://04_drafts/proposal-v003.md
    evaluation: eval-003
    decision: accept
    language_qa: pass
    frozen: true
  sap:
    artifact_id: sap-telehf90
    version: v002
    path: memory://07_sap/sap-v002.md
    evaluation: sap-eval-002
    decision: accept
    frozen: true
  package:
    path: memory://09_package/final-proposal-package
    status: human_signoff_required

actual_and_canonical_instances:
  readiness:
    actual: /root/readiness_telehf90
    canonical: TELE-HF90-STD-SAP-001-READINESS-001
  proposal_writers:
    - /root/proposal_drafter_v1
    - /root/proposal_drafter_v2
    - /root/proposal_cleanup_v3
  proposal_evaluators:
    - actual: /root/proposal_eval_v1
      canonical: proposal-evaluator-telehf90-eval001-20260712-a7f3
    - actual: /root/proposal_eval_v2
      canonical: eval-002
    - actual: /root/proposal_eval_v3
      canonical: TELE-HF90-proposal-evaluator-003
  methodology_preflight:
    actual: /root/method_preflight
    canonical: preflight-001-amendment
  sap_writer:
    actual: /root/sap_writer_v1
  sap_evaluators:
    - actual: /root/sap_eval_v1
      canonical: sap-eval-001
    - actual: /root/sap_eval_v2
      canonical: sap-eval-002
  language_assessor:
    actual: /root/language_qa_v3
    canonical: TELE-HF90-language-001
  final_panel:
    clinician: /root/panel3_clinician
    methodology_statistics: /root/panel3_methods
    submission_guard: /root/panel3_submission
    canonical_panel: panel-003
  assembler:
    actual: /root/package_assembler

event_order:
  - readiness_ready
  - proposal_v001_drafted
  - proposal_v001_evaluated_accept
  - methodology_preflight_amended_ready
  - sap_v001_drafted
  - sap_v001_evaluated_revise
  - sap_v002_created
  - sap_v002_evaluated_accept
  - panel_001_completed
  - proposal_v002_created
  - proposal_v002_evaluated_accept
  - panel_002_completed
  - proposal_v003_created
  - proposal_v003_evaluated_accept
  - language_qa_pass
  - panel_003_completed
  - package_assembled

isolation:
  readiness_fresh: true
  every_proposal_evaluation_fresh: true
  methodology_preflight_fresh: true
  every_sap_evaluation_fresh: true
  every_panel_role_fresh: true
  panel_roles_concurrent: true
  prior_scores_visible_to_re_evaluators: false
  peer_outputs_visible_during_panel_review: false
  reviewer_source_edits: false

panel:
  tier: lightweight_panel
  mode: blind_mock_review
  roles:
    - practicing_clinician_domain
    - methodology_statistics
    - submission_guard
  dissent_preserved: true
  fatal_findings: []
  final_route: PI_review

files_read:
  - proposal-orchestrator/SKILL.md
  - references/workflow-state-schema.md
  - references/artifact-naming-and-directory-rules.md
  - references/delegate-brief-templates.md
  - references/reviewer-brief-templates.md
  - references/delegation-rules-pattern.md
  - references/proposal-writing-methodology.md
  - memory://00_input/concept-v001
  - memory://04_drafts/proposal-v001.md
  - memory://04_drafts/proposal-v002.md
  - memory://04_drafts/proposal-v003.md
  - memory://07_sap/sap-v001.md
  - memory://07_sap/sap-v002.md

files_written: []
browsing_performed: false
external_actions_performed: false

unresolved_for_PI:
  - approve detailed eligibility criteria
  - approve escalation thresholds and coverage rules
  - resolve 2592-versus-2600 recruitment capacity
  - accept or mitigate outside-system readmission limitation
  - approve endpoint/adjudication charter
  - approve remaining SAP signoff-controlled conventions
  - approve safety, workload, equity, and N1300-review governance
  - approve budget allocation and activation readiness
  - review preserved panel dissent
  - sign proposal-v003 and SAP-v002

stop_condition: PI_review_and_signature
external_submission_authorized: false
```

The package stops here for PI review and signature. No submission, registration, communication, or other external action has been performed.
