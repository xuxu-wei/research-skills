---
schema_version: research-idea-content-preservation-check.v1
check_id: content-preservation-I01-001-r014
review_id: content-preservation-review-I01-001-r014
reviewer_skill: idea-narrative-assessor
reviewer_instance_id: fresh-scientific-content-preservation-reviewer-r014
workflow_id: RID-SEPSIS-CSM-20260717-001
round_id: one-pass-current-r014
input_artifact_ids:
  - idea-dossier-I01-001-v003
  - idea-dossier-I01-001-v005
  - protected-content-register-I01-001-v003
  - revision-delta-I01-001-v003-to-v005
input_versions:
  - v003
  - v005
  - v003
  - v005
inputs:
  prior_dossier:
    artifact_id: idea-dossier-I01-001-v003
    version: v003
    path: tests/idea-test-0.9.0-preview.1/0.9.0-preview.1/03_ideas/nodes/I01-001/dossiers/idea-dossier-v003.md
  revised_dossier:
    artifact_id: idea-dossier-I01-001-v005
    version: v005
    path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/revised/idea-dossier-v005.md
  protected_content_register:
    artifact_id: protected-content-register-I01-001-v003
    version: v003
    path: tests/idea-narrative-forward-0.9.0-preview.3/run-001/inputs/protected-content-register.yaml
  revision_delta:
    artifact_id: revision-delta-I01-001-v003-to-v005
    version: v005
    path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/revised/revision-delta-v003-to-v005.md
files_read:
  - tests/idea-test-0.9.0-preview.1/0.9.0-preview.1/03_ideas/nodes/I01-001/dossiers/idea-dossier-v003.md
  - tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/revised/idea-dossier-v005.md
  - tests/idea-narrative-forward-0.9.0-preview.3/run-001/inputs/protected-content-register.yaml
  - tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/revised/revision-delta-v003-to-v005.md
isolation_mode: fresh_subagent
prior_scores_visible: false
source_edits_performed: false
decision: editorial_scope_violation
protected_item_checks:
  - protected_id: PCR-001
    prior_locator:
      section_heading: YAML frontmatter identity_anchor; Research question, objectives, and core hypothesis
      content_anchor: primary_research_question and the sepsis-centered pre-onset, onset, post-onset, and outcome continuum
    revised_locator:
      section_heading: YAML frontmatter identity_anchor; Research question, objectives, and core hypothesis
      content_anchor: unchanged primary_research_question and the three-part Primary research question
    semantic_status: preserved
    evidence: >-
      The identity-anchor question is verbatim unchanged. The revised question still concerns a knowledge-constrained, uncertainty-aware sepsis-centered dynamic-system representation spanning at-risk pre-onset time, first onset, post-onset evolution, and outcomes; it is not recast as ordinary prediction or generic ICU risk stratification.
  - protected_id: PCR-002
    prior_locator:
      section_heading: YAML frontmatter identity_anchor; Research question, objectives, and core hypothesis
      content_anchor: primary_objective and Objectives 2-3
    revised_locator:
      section_heading: YAML frontmatter identity_anchor; Research question, objectives, and core hypothesis; Research content and work packages
      content_anchor: unchanged primary_objective, Objectives 2-3, and the 24-month Stage I-II minimum
    semantic_status: preserved
    evidence: >-
      The primary objective remains verbatim in the identity anchor, and v005 retains completion of Stage I-II within 24 months, knowledge-constrained construction, public-ICU system identification, cross-database validation, and auditable evidence and benchmark outputs rather than a prediction-only product.
  - protected_id: PCR-003
    prior_locator:
      section_heading: YAML frontmatter identity_anchor; Research design and methods
      content_anchor: study_object, primary_unit_of_inference, and patient-time states and transitions with patient and hospital clustering
    revised_locator:
      section_heading: YAML frontmatter identity_anchor; Research design and methods
      content_anchor: unchanged study_object and primary_unit_of_inference; task tables and clustered uncertainty
    semantic_status: preserved
    evidence: >-
      The study object and unit of inference are verbatim unchanged. The revised design still includes comparable at-risk non-onset intervals and post-onset trajectories and retains patient-time states and transitions with patient- and hospital-level clustering.
  - protected_id: PCR-004
    prior_locator:
      section_heading: Data, materials, and existing evidence base
      content_anchor: Current verified-resource versus prospective-gate status; Public ICU database roles and G1 audit
    revised_locator:
      section_heading: Data, materials, and existing evidence base; Feasibility, resources, risks, alternatives, and stop conditions
      content_anchor: Current resource and evidence status; Public ICU database roles and G1 audit; Feasibility and resources
    semantic_status: preserved
    evidence: >-
      v005 retains literature and expert priors, MIMIC-IV and eICU-CRD as the two main public ICU sources, and HiRID or AmsterdamUMCdb as a pre-specified conditional backup. It continues to label access credentials, data-use agreements, executable extraction, project cohort support, named personnel, and model results as unverified or not generated rather than available.
  - protected_id: PCR-005
    prior_locator:
      section_heading: Data, materials, and existing evidence base
      content_anchor: Local RCT evidence and present limits
    revised_locator:
      section_heading: Data, materials, and existing evidence base; Research design and methods; Feasibility, resources, risks, alternatives, and stop conditions
      content_anchor: Local randomized-trial evidence; Conditional trial observation mapping and independent alternative; trial-data limitations
    semantic_status: preserved
    evidence: >-
      EXIT-SEP and XBJ-SCAP remain conditional Stage III sources. Their local reports remain project-derived materials that do not replace participant-level authorization, original CRF/SAP, randomization and center information, actual visit timing, or survival, hospitalization, discharge, and transfer semantics.
  - protected_id: PCR-006
    prior_locator:
      section_heading: Research content and work packages; Research design and methods
      content_anchor: minimum route; variable-role separation; anchoring, recovery, transport, and abstention
    revised_locator:
      section_heading: Research content and work packages; Research design and methods; Key techniques and implementation
      content_anchor: minimum sequence; Candidate variable roles; Observational target, anchoring and abstention
    semantic_status: preserved
    evidence: >-
      The sequence remains resource and G1 audit, label/state/hospital-split lock, simple baselines, absolute simulation and false-confidence checks, at most one complex candidate, two primary tasks and two secondary diagnostics, development freeze, untouched cross-database validation, and only then conditional trial analysis. X_t, Y_t, A_t, M_t, labels, and baseline covariates remain separated, and interpretation remains limited by anchoring, alignment, recovery, transport, and abstention criteria.
  - protected_id: PCR-007
    prior_locator:
      section_heading: Research content and work packages; Research design and methods
      content_anchor: Conjunctive minimum success definition; Hospital-primary genuine cross-database validation
    revised_locator:
      section_heading: Research content and work packages; Research design and methods; Expected outputs, falsification criteria, and interpretations; Feasibility, resources, risks, alternatives, and stop conditions
      content_anchor: Conjunctive minimum success definition; Hospital-based cross-database validation; external-stability risk and time boundary
    semantic_status: preserved
    evidence: >-
      v005 retains the conjunctive requirement for data support, recovery, primary-task proper scores and calibration, zero unresolved high-severity leakage, untouched zero-update external performance, state alignment of at least 0.70, and structural-sign agreement of at least 0.80. Calibration-only and observation-model updates use only the adaptation partition and are separately reported; the limitations and risk table explicitly state that such updates cannot replace zero-update failure. Stage III remains outside and cannot supplement Stage II success.
  - protected_id: PCR-008
    prior_locator:
      section_heading: Research design and methods
      content_anchor: Protocol locks for the two primary clinical tasks; Mutually exclusive post-onset state/event system
    revised_locator:
      section_heading: Research design and methods
      content_anchor: Protocol definitions for the two primary clinical tasks; Mutually exclusive post-onset state and event system
    semantic_status: preserved
    evidence: >-
      Both primary estimands and their event and information-availability clocks, 12-hour landmarks and horizon, delayed entry, mutually exclusive states and competing terminal events, as-of ordering, Brier and absolute-calibration criteria, patient and hospital bootstrap uncertainty, and leakage protections remain. The main thresholds remain +0.01 for Brier noninferiority, calibration slope 0.80-1.20, and absolute risk error at most 0.02.
  - protected_id: PCR-009
    prior_locator:
      section_heading: Structured abstract; Contribution, innovation, impact, application, and closest-work comparison
      content_anchor: planned outputs, evidence ladder, and bounded closest-work claim
    revised_locator:
      section_heading: Structured abstract; Contribution, innovation, impact, application, and closest-work comparison; Title and positioning claim-support table
      content_anchor: Expected result; Contribution and evidence ladder; bounded search and unsupported first/global-first claims
    semantic_status: preserved
    evidence: >-
      v005 explicitly states that no current model, simulation recovery, external validation, or new trial result exists. The contribution remains conditional integration, validation, benchmark, and research-resource value; component precedents remain acknowledged, and the five-layer gap remains only a low-to-moderate-confidence result of a bounded search rather than a global-first or new-algorithm claim.
  - protected_id: PCR-010
    prior_locator:
      section_heading: Feasibility, resources, risks, alternatives, and stop conditions
      content_anchor: Resources and governance; Risk and automatic alternative matrix; Remaining execution gates
    revised_locator:
      section_heading: Feasibility, resources, risks, alternatives, and stop conditions
      content_anchor: Feasibility and resources; Working assumptions; Limitations and boundary conditions; Risks, alternatives, and stop conditions; no complete counterpart to Remaining execution gates
    semantic_status: changed
    evidence: >-
      v005 consolidates most resource, access, staffing, G1 support, leakage, recoverability, missingness and overlap, external transport, trial-data, mapping, timing, closest-work, fallback, and stop conditions at the authority location. However, v003 explicitly listed the clinical-scale-to-simulation-parameter mapping and the exact multicategory-calibration estimator, confidence bound, and threshold registry as unresolved execution requirements. v005 retains general simulation and calibration procedures but no longer identifies those two specifications as unresolved feasibility findings. This omission weakens the frozen feasibility status and is not disclosed in the revision delta.
  - protected_id: PCR-011
    prior_locator:
      section_heading: Research content and work packages; Feasibility, resources, risks, alternatives, and stop conditions
      content_anchor: Twenty-four-month minimum and dated gates; Identity and final stop boundary
    revised_locator:
      section_heading: Research content and work packages; Feasibility, resources, risks, alternatives, and stop conditions
      content_anchor: Twenty-four-month minimum and dated decisions; time and stage limitation; final stop paragraph
    semantic_status: preserved
    evidence: >-
      Stage I-II remains the mandatory 24-month minimum. Stage III remains after month 24 and conditional on successful Stage II plus trial authorization, semantics, and observation mapping. v005 expressly states that no Stage III result counts toward, supplements, or bypasses Stage II resource, recovery, primary-task, leakage, or external-validation requirements.
  - protected_id: PCR-012
    prior_locator:
      section_heading: Research question, objectives, and core hypothesis; Feasibility, resources, risks, alternatives, and stop conditions
      content_anchor: Core hypothesis and non-hypotheses; causal and clinical interpretation boundary
    revised_locator:
      section_heading: Research question, objectives, and core hypothesis; Expected outputs, falsification criteria, and interpretations; Feasibility, resources, risks, alternatives, and stop conditions; Title and positioning claim-support table
      content_anchor: Core hypothesis and non-hypotheses; Interpretation matrix; causal and clinical interpretation limitation; unsupported claims
    semantic_status: preserved
    evidence: >-
      v005 continues to exclude causal treatment effects, true feedback networks, counterfactual strategies, mechanisms, mediation, individual control, latent dynamics, and transition-edge validation. It also keeps the current plan outside claims of a validated model, digital twin, controllable system, clinical decision tool, drug platform, or unconditional clinical recommendation; the independent SOFA branch remains unrelated to Stage II validation.
undeclared_scientific_changes:
  - change: >-
      Two previously explicit unresolved feasibility requirements are absent from v005: mapping clinical scales to simulation parameters, and specifying the exact multicategory-calibration estimator, confidence bound, and threshold registry.
    prior_locator: Feasibility, resources, risks, alternatives, and stop conditions > Remaining execution gates
    revised_locator: Feasibility, resources, risks, alternatives, and stop conditions; no equivalent unresolved-status statement
    effect: >-
      The revision presents the feasibility specification as more complete than v003 and weakens the required limitation status without declaring a scientific change.
findings:
  - finding_id: CPF-001
    protected_id: PCR-010
    finding: >-
      The authority section does not retain all frozen unresolved feasibility findings.
    required_correction: >-
      Restore, at the section-14 authority location, the unresolved status of the clinical-scale-to-simulation-parameter mapping and of the exact multicategory-calibration estimator, confidence bound, and threshold registry. Do not imply that these specifications are complete unless a separately reviewed scientific change is declared.
unresolved_issues:
  - >-
    PCR-010 must be restored and the resulting dossier must receive a new independent content-preservation review before downstream assessment.
---

# Content-preservation check

## Decision rationale

The central study identity, claim strength, primary methods, numerical thresholds, conditional branches, most feasibility findings, and all unsupported-claim boundaries remain traceable from v003 to v005. The revision delta declares no scientific change. Nevertheless, v005 omits two items that v003 explicitly classified as unresolved execution requirements: the mapping from clinical scales to simulation parameters, and the exact specification of the multicategory-calibration estimator, confidence bound, and threshold registry. Because removing an unresolved feasibility finding weakens a protected limitation without changing the study identity, the appropriate decision is `editorial_scope_violation`, not `identity_drift_detected` or `scientific_change_declared`.

## Protected-content trace

PCR-001 through PCR-009 and PCR-011 through PCR-012 are preserved. Their content was mainly split, renamed, or consolidated: identity remains in the unchanged frontmatter and research question; task and validation commitments remain in the methods and conjunctive success definition; trial-data status and claim boundaries remain in the evidence-status table, interpretation matrix, claim-support table, and section 14. PCR-010 is only partially preserved. Most limitations and every listed risk response remain in section 14, but the two unresolved feasibility specifications identified above have no revised counterpart.

## Required routing

The dossier must return for bounded editorial correction of PCR-010. After correction, a new independent content-preservation review is required. It may not proceed directly to fresh narrative or language assessment on the basis of this report.
