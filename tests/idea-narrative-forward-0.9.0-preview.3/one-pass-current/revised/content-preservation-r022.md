---
schema_version: research-idea-content-preservation-check.v1
check_id: content-preservation-I01-001-r022
review_id: content-preservation-review-I01-001-r022
reviewer_skill: idea-narrative-assessor
reviewer_instance_id: fresh-preservation-r022
workflow_id: RID-SEPSIS-CSM-20260717-001
round_id: r022
input_artifact_ids:
  - idea-dossier-I01-001-v003
  - idea-dossier-I01-001-v021
  - protected-content-register-I01-001-v003
  - revision-delta-I01-001-v003-to-v021
input_versions:
  - v003
  - v021
  - v003
  - v021
inputs:
  prior_dossier:
    artifact_id: idea-dossier-I01-001-v003
    version: v003
    path: tests/idea-test-0.9.0-preview.1/0.9.0-preview.1/03_ideas/nodes/I01-001/dossiers/idea-dossier-v003.md
  revised_dossier:
    artifact_id: idea-dossier-I01-001-v021
    version: v021
    path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/revised/idea-dossier-v021.md
  protected_content_register:
    artifact_id: protected-content-register-I01-001-v003
    version: v003
    path: tests/idea-narrative-forward-0.9.0-preview.3/run-001/inputs/protected-content-register.yaml
  revision_delta:
    artifact_id: revision-delta-I01-001-v003-to-v021
    version: v021
    path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/revised/revision-delta-v003-to-v021.md
files_read:
  - tests/idea-test-0.9.0-preview.1/0.9.0-preview.1/03_ideas/nodes/I01-001/dossiers/idea-dossier-v003.md
  - tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/revised/idea-dossier-v021.md
  - tests/idea-narrative-forward-0.9.0-preview.3/run-001/inputs/protected-content-register.yaml
  - tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/revised/revision-delta-v003-to-v021.md
isolation_mode: fresh_subagent
prior_scores_visible: false
source_edits_performed: false
decision: scientific_content_preserved
protected_item_checks:
  - protected_id: PCR-001
    prior_locator: "YAML frontmatter identity_anchor; Research question, objectives, and core hypothesis > Primary research question"
    revised_locator: "YAML frontmatter identity_anchor; Research question, objectives, and core hypothesis > Primary research question; Research design and methods > Mutually exclusive post-onset state and event system"
    semantic_status: preserved
    evidence: >-
      The identity-anchor values are unchanged. The revised question still concerns a knowledge-constrained, uncertainty-aware sepsis-centered ICU dynamic-system representation spanning comparable pre-onset risk periods, first onset, post-onset evolution, and outcomes. The mutually exclusive state system retains recovery, persistent sepsis, worsening or new organ failure, live ICU discharge, transfer or loss of observation, and death; the study is not reframed as generic ICU risk stratification or an ordinary prediction-only project.
  - protected_id: PCR-002
    prior_locator: "YAML frontmatter identity_anchor.primary_objective; Research question, objectives, and core hypothesis > Objectives"
    revised_locator: "YAML frontmatter identity_anchor.primary_objective; Research question, objectives, and core hypothesis > Objectives; Research content and work packages"
    semantic_status: preserved
    evidence: >-
      The primary objective remains verbatim in frontmatter, and the revised objectives and work sequence retain literature and expert constraints, public-ICU system identification, whole-course representation, planned cross-database validation, and completion of stages I-II within 24 months. Deliverables remain auditable scientific evidence, benchmarks, and resources rather than only a prediction tool; all outputs are still prospective.
  - protected_id: PCR-003
    prior_locator: "YAML frontmatter identity_anchor.study_object and primary_unit_of_inference; Research design and methods"
    revised_locator: "YAML frontmatter identity_anchor.study_object and primary_unit_of_inference; Research design and methods > Protocol for the two primary clinical tasks; Observational target, anchoring and abstention"
    semantic_status: preserved
    evidence: >-
      The revised frontmatter preserves the longitudinal sepsis-centered ICU patient system, including at-risk non-onset intervals and post-onset trajectories, and the patient-time state and transition as the unit of inference. The task protocol retains first eligible stays, incident onset and delayed entry, overlapping-landmark weighting, and patient- and hospital-level clustering and bootstrap uncertainty.
  - protected_id: PCR-004
    prior_locator: "Data, materials, and existing evidence base > Current verified-resource versus prospective-gate status; Public ICU database roles and G1 audit"
    revised_locator: "Data, materials, and existing evidence base > Current resource and evidence status; Public ICU database roles and G1 audit; Feasibility, resources, risks, alternatives, and stop conditions > Limitations and boundary conditions, item 1"
    semantic_status: preserved
    evidence: >-
      MIMIC-IV v3.1 and eICU-CRD v2.0 remain the two principal public ICU sources, with HiRID or AmsterdamUMCdb restricted to a predesignated, equivalently audited backup role; literature and expert knowledge remain the model constraints. Only database existence and version are verified. Team credentials, data-use agreements, executable extraction, named personnel and work effort remain unverified, while project-specific G1 support and all model, simulation, prediction, external-test, and trial-analysis results remain not generated.
  - protected_id: PCR-005
    prior_locator: "Data, materials, and existing evidence base > Local RCT evidence and present limits"
    revised_locator: "Data, materials, and existing evidence base > Current resource and evidence status; Local RCT evidence; Research design and methods > Conditional trial-observation mapping and independent analysis; Feasibility, resources, risks, alternatives, and stop conditions > Limitations and boundary conditions, item 7"
    semantic_status: preserved
    evidence: >-
      EXIT-SEP and XBJ-SCAP remain conditional stage-III data sources and are not promoted into the stage-II evidence base. The revised dossier retains the trial and derivative-report counts and explicitly classifies the local reports as derivative cleaning or quality-control material. Individual-data authorization, original CRF and SAP, randomization and analysis-set definitions, center or stratification information, actual visit timing relative to randomization and first dose, and survival, hospitalization, discharge, and transfer semantics all still require primary verification.
  - protected_id: PCR-006
    prior_locator: "Research content and work packages; Research design and methods"
    revised_locator: "Research content and work packages; Research design and methods > Protocol for the two primary clinical tasks; Variable-use separation; Observational target, anchoring and abstention; Prespecified simulation recovery and erroneous-confidence control; Hospital-primary cross-database validation; Conditional trial-observation mapping and independent analysis"
    semantic_status: preserved
    evidence: >-
      The required order remains resource and observability audit, label/state/hospital-split lock, competing-risk and multistate baselines, linear state-space baseline, absolute simulation recovery and erroneous-confidence control, at most one complex candidate, two primary tasks and two secondary diagnostics, development freeze, and untouched cross-database testing before any conditional trial analysis. Physiological measurements, treatment actions, measurement processes, labels, and baseline covariates remain separated. Interpretation is still limited to anchored and aligned state occupancy, transitions, anchor predictions, and prespecified signs or lags, with deletion, merging, database- or policy-specific labeling, or abstention when support criteria fail.
  - protected_id: PCR-007
    prior_locator: "Research content and work packages > Conjunctive minimum success definition; Research design and methods > Hospital-primary genuine cross-database validation"
    revised_locator: "Research content and work packages > five-item conjunctive success definition; Research design and methods > Hospital-primary cross-database validation; Feasibility, resources, risks, alternatives, and stop conditions > Limitations and boundary conditions, item 6; Risks, alternatives, and stop conditions"
    semantic_status: preserved
    evidence: >-
      Stage-II success still requires the conjunction of two-database support, absolute recovery and null or misspecification control, both primary tasks' proper scores and calibration, clearance of high-severity leakage, untouched external zero-update performance, state alignment, and structural sign stability. The +0.01 Brier noninferiority limit, calibration slope 0.80-1.20, absolute risk error 0.02, at least 20 test hospitals, alignment at least 0.70, and sign agreement at least 0.80 remain unchanged. Calibration-only and observation-layer updates are reported separately and cannot replace zero-update failure; full refitting remains redevelopment, and stage III cannot count toward stage-II success.
  - protected_id: PCR-008
    prior_locator: "Research design and methods > Protocol locks for the two primary clinical tasks; Mutually exclusive post-onset state/event system"
    revised_locator: "Research design and methods > Protocol for the two primary clinical tasks; Mutually exclusive post-onset state and event system; Feasibility, resources, risks, alternatives, and stop conditions > Limitations and boundary conditions, item 2"
    semantic_status: preserved
    evidence: >-
      Both primary tasks and their exact operational rules remain: specimen-antibiotic pairing of 72 hours when sampling precedes treatment and 24 hours when treatment precedes sampling; baseline-SOFA rules; rolling 24-hour component values; the infection -48/+24-hour window and first sortable onset; separate event and label-availability clocks; first-onset-only analysis; total overlapping-landmark stay weight of one; delayed entry; mutually exclusive post-onset states and competing terminal events; as-of features; A_t before next-boundary physiology; and exclusion of unsortable same-timestamp edges. The CIF and day-7 occupancy estimands, Brier and calibration targets, patient/hospital uncertainty, and checks for same-bin treatment, future measurement frequency, repeated stays, cross-split preprocessing, and outcome-driven variables, grids, or thresholds are retained without numerical change.
  - protected_id: PCR-009
    prior_locator: "Structured abstract; Contribution, innovation, impact, application, and closest-work comparison > Contribution and evidence ladder"
    revised_locator: "Structured abstract; Title, summary, audience, and positioning; Contribution, innovation, impact, application, and closest-work comparison; Title and positioning claim-support table; Feasibility, resources, risks, alternatives, and stop conditions > Limitations and boundary conditions, items 10-11"
    semantic_status: preserved
    evidence: >-
      The revised dossier consistently describes the candidate representation, simulation, validation, and trial analyses as planned, and states that no current model or validation result exists. The allowable contribution remains conditional integration, validation, benchmark, resource, and reproducible failure evidence. It retains high confidence that individual modules have precedents and only low-to-moderate confidence that the full combination lacks a representative precedent; no new-algorithm, first, or global-first claim is added.
  - protected_id: PCR-010
    prior_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Resources and governance; Risk and automatic alternative matrix; Remaining execution gates; Identity and final stop boundary"
    revised_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Feasibility and resources; Working assumptions; Limitations and boundary conditions; Risks, alternatives, and stop conditions"
    semantic_status: preserved
    evidence: >-
      The revised authority section retains the complete limitations concerning access and staffing, G1 support, label uncertainty and leakage, state recoverability, MNAR and action overlap, external transport, schedule, trial authorization and semantics, common anchors and observation mapping, claim scope, and closest-work uncertainty. Pending decisions keep their decision times and allowed information. Every substantive trigger retains an alternative and a downgrade or stop result, including database-access failure, support loss after cross-partition exclusion, unresolved leakage, recovery or false-structure failure, MNAR or overlap failure, zero-update failure, projection failure, trial-semantic failure, schedule failure, and requests for unsupported novelty or clinical claims.
  - protected_id: PCR-011
    prior_locator: "Research content and work packages > Twenty-four-month minimum and dated gates; Identity and final stop boundary"
    revised_locator: "Research content and work packages > opening, timetable, and minimum route; Feasibility, resources, risks, alternatives, and stop conditions > Limitations and boundary conditions, item 12; Risks, alternatives, and stop conditions; final identity-boundary paragraph"
    semantic_status: preserved
    evidence: >-
      Stages I-II remain the required 24-month minimum, with the month 3, 6, 12, 18/20, 20, 21-24, and post-24-month conditions retained. Stage III remains outside the minimum and may begin only after stage-II success plus trial authorization, semantic verification, and an eligible observation mapping or independent endpoint. No trial result can rescue or bypass a resource, recovery, primary-task, leakage, or untouched-external failure.
  - protected_id: PCR-012
    prior_locator: "Research question, objectives, and core hypothesis > Core hypothesis and non-hypotheses; Feasibility, resources, risks, alternatives, and stop conditions"
    revised_locator: "Research question, objectives, and core hypothesis > Core hypothesis and scientific scope; Feasibility, resources, risks, alternatives, and stop conditions > Limitations and boundary conditions, items 5 and 8-10"
    semantic_status: preserved
    evidence: >-
      The revised dossier preserves the boundary that observational data and task performance do not identify a real causal network, treatment effects, counterfactual policies, mechanisms, mediation, or control. A trial mapping, even when eligible, remains a one-dimensional measured summary rather than the latent state; neither trial branch validates unmeasured dynamics, transition edges, the full system, mechanisms, mediation, or control. The plan is still not a validated model, digital twin, clinical decision tool, drug platform, or unconditional basis for clinical implementation.
undeclared_scientific_changes: []
findings: []
unresolved_issues: []
---

# Content-preservation check

## Decision rationale

The revision is an editorial reorganization and language clarification. All twelve protected items remain traceable with the same research identity, evidence status, numerical and temporal rules, design commitments, conditional branches, claim strength, and limitation strength. Detailed limitations and contingencies were consolidated into the authoritative feasibility section without removing their triggers or consequences. The revision delta declares no scientific change, and direct comparison found no undeclared addition of data, methods, results, evidence, or supported claim classes.

## Protected-content trace

The principal moves are the consolidation of complete limitations, working assumptions, alternatives, and stopping conditions under `Feasibility, resources, risks, alternatives, and stop conditions`; replacement of compact internal labels with direct scientific descriptions; and separation of the trial observation mapping from the independent SOFA-based analysis. The protocol tables retain the full onset definition, dual clocks, state system, estimands, leakage controls, uncertainty handling, and thresholds. The external-validation section retains hospital-first partitioning, complete exclusion of cross-partition patients in the primary analysis, untouched zero-update precedence, and the non-substitutability of limited updates. The trial section retains authorization and semantic prerequisites, the frozen deterministic mapping, every absolute fidelity criterion, the independent analysis branch, trial-specific populations and visits, missing-data and multiplicity rules, and stopping conditions.

## Required routing

The revised dossier may proceed to fresh narrative and academic-language assessment. It does not require return to scientific review on content-preservation grounds.
