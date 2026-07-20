---
schema_version: research-idea-content-preservation-check.v1
check_id: content-preservation-I01-001-r021
review_id: content-preservation-I01-001-r021
reviewer_skill: idea-narrative-assessor
reviewer_instance_id: fresh-content-preservation-r021
workflow_id: RID-SEPSIS-CSM-20260717-001
round_id: r021
input_artifact_ids:
  - idea-dossier-I01-001-v003
  - idea-dossier-I01-001-v020
  - protected-content-register-I01-001-v003
  - revision-delta-I01-001-v003-to-v020
input_versions:
  - v003
  - v020
  - v003
  - v020
inputs:
  prior_dossier:
    artifact_id: idea-dossier-I01-001-v003
    version: v003
    path: tests/idea-test-0.9.0-preview.1/0.9.0-preview.1/03_ideas/nodes/I01-001/dossiers/idea-dossier-v003.md
  revised_dossier:
    artifact_id: idea-dossier-I01-001-v020
    version: v020
    path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/revised/idea-dossier-v020.md
  protected_content_register:
    artifact_id: protected-content-register-I01-001-v003
    version: v003
    path: tests/idea-narrative-forward-0.9.0-preview.3/run-001/inputs/protected-content-register.yaml
  revision_delta:
    artifact_id: revision-delta-I01-001-v003-to-v020
    version: v020
    path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/revised/revision-delta-v003-to-v020.md
files_read:
  - tests/idea-test-0.9.0-preview.1/0.9.0-preview.1/03_ideas/nodes/I01-001/dossiers/idea-dossier-v003.md
  - tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/revised/idea-dossier-v020.md
  - tests/idea-narrative-forward-0.9.0-preview.3/run-001/inputs/protected-content-register.yaml
  - tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/revised/revision-delta-v003-to-v020.md
isolation_mode: fresh_subagent
prior_scores_visible: false
source_edits_performed: false
decision: editorial_scope_violation
protected_item_checks:
  - protected_id: PCR-001
    prior_locator: "YAML frontmatter > identity_anchor; Research question, objectives, and core hypothesis > Primary research question"
    revised_locator: "YAML frontmatter > identity_anchor; Research question, objectives, and core hypothesis > Primary research question; Feasibility, resources, risks, alternatives, and stop conditions > final identity paragraph"
    semantic_status: preserved
    evidence: >-
      v020 retains the sepsis-centered pre-onset, first-onset, post-onset, and outcome continuum, the candidate dynamic-system representation, and the distinction from general ICU risk prediction. The identity-anchor values are unchanged, and the final identity paragraph expressly treats alteration of these elements as a new research idea.
  - protected_id: PCR-002
    prior_locator: "YAML frontmatter > identity_anchor.primary_objective; Research question, objectives, and core hypothesis > Objectives; Research content and work packages"
    revised_locator: "YAML frontmatter > identity_anchor.primary_objective; Title, summary, audience, and positioning; Research question, objectives, and core hypothesis > Objectives; Required analyses and evidence"
    semantic_status: preserved
    evidence: >-
      v020 retains completion of stages I-II within 24 months, literature and expert constraints, public ICU data, system identification, cross-database validation, and an auditable evidence package rather than a prediction-only product. The protected reference to publication direction is not repeated verbatim, but v003 likewise does not make publication venue or publication status part of the scientific estimand; the protected scientific objective and delivery orientation remain traceable.
  - protected_id: PCR-003
    prior_locator: "YAML frontmatter > identity_anchor.study_object and primary_unit_of_inference; Research design and methods > Observational target, anchoring and abstention"
    revised_locator: "YAML frontmatter > identity_anchor.study_object and primary_unit_of_inference; Research question, objectives, and core hypothesis > Core hypothesis; Feasibility, resources, risks, alternatives, and stop conditions > final identity paragraph"
    semantic_status: preserved
    evidence: >-
      v020 retains the longitudinal sepsis-centered ICU system, comparable pre-onset intervals and post-onset trajectories, and patient-time states and transitions as the inference unit. Patient and hospital clustering remains explicit in the unchanged identity anchor and in the two-level bootstrap specification.
  - protected_id: PCR-004
    prior_locator: "Data, materials, and existing evidence base > Current verified-resource versus prospective-gate status; Public ICU database roles and G1 audit"
    revised_locator: "Data, materials, and existing evidence base > Current verified-resource versus prospective status; Public ICU database roles and G1 audit; Feasibility, resources, risks, alternatives, and stop conditions > Feasibility and resources"
    semantic_status: preserved
    evidence: >-
      v020 keeps MIMIC-IV and eICU-CRD as the two core public databases and HiRID or AmsterdamUMCdb as a prespecified backup. It continues to classify access, DUA, executable extraction, project-specific support, named personnel, models, simulations, and external results as unverified or not generated rather than available.
  - protected_id: PCR-005
    prior_locator: "Data, materials, and existing evidence base > Local RCT evidence and present limits"
    revised_locator: "Data, materials, and existing evidence base > Local RCT evidence and present status; Feasibility, resources, risks, alternatives, and stop conditions > Feasibility and resources; Limitations and boundary conditions items 7-8"
    semantic_status: preserved
    evidence: >-
      v020 continues to treat EXIT-SEP and XBJ-SCAP as conditional post-stage-II sources. It identifies the current materials as project-local derivative reports and states that they do not replace individual-level authorization, original CRF/SAP or data-holder confirmation, randomization and center information, visit timing, or survival and hospitalization semantics.
  - protected_id: PCR-006
    prior_locator: "Research content and work packages > Work packages and minimum route; Research design and methods > Candidate variable-role firewall; Observational target, anchoring and abstention"
    revised_locator: "Research content and work packages > Work packages and minimum route; Research design and methods > Candidate variable-use isolation; Observational target, anchoring and abstention; Prespecified simulation recovery and erroneous-confidence control; Hospital-primary cross-database validation"
    semantic_status: preserved
    evidence: >-
      The ordered route remains resource and observability audit, protocol and hospital split lock, simple baselines, simulation recovery and erroneous-confidence control, at most one complex candidate, two primary tasks and two diagnostics, frozen development decisions, isolated external testing, and only then conditional trial analysis. Y_t, A_t, and M_t remain separated, and interpretation remains restricted by anchoring, alignment, recovery, external stability, and abstention.
  - protected_id: PCR-007
    prior_locator: "Research content and work packages > Conjunctive minimum success definition; Research design and methods > Hospital-primary genuine cross-database validation"
    revised_locator: "Research content and work packages > Conjunctive minimum success definition; Research design and methods > Hospital-primary cross-database validation; Feasibility, resources, risks, alternatives, and stop conditions > Limitations and boundary conditions items 5-6"
    semantic_status: preserved
    evidence: >-
      v020 retains conjunctive stage-II success across data support, simulation recovery, proper scoring and calibration, leakage control, no-update external performance, state alignment, and structural stability. It reports calibration-only and observation-layer updates separately, classifies full refitting as new development, and states that later trial results cannot compensate for a stage-II failure.
  - protected_id: PCR-008
    prior_locator: "Research design and methods > Protocol locks for the two primary clinical tasks, rows Event clock, First onset/repeats, Within-bin order, Pass/fail, and following leakage paragraph; Mutually exclusive post-onset state/event system"
    revised_locator: "Research design and methods > Protocol locks for the two primary clinical tasks, rows 事件时间 through 不确定性 and following paragraph; Mutually exclusive post-onset state/event system; Required analyses and evidence items 2-3"
    semantic_status: changed
    evidence: >-
      v020 preserves the two tasks, dual times, incident and delayed-entry populations, mutually exclusive states, competing events, Brier and calibration targets, clustered uncertainty, and a general requirement to use information available before the landmark. It does not, however, retain all frozen operational commitments. The v003 event-clock row specifies the 72-hour/24-hour specimen-antibiotic pairing, baseline-SOFA rules, rolling 24-hour component calculation, and first sortable onset; v020 reduces this to an unspecified pairing plus the +2 window. The v003 First onset/repeats and Within-bin order rows also require first-onset-only analysis, total stay weight 1 for overlapping landmarks, explicit A_t/next-state ordering, and exclusion of unsortable same-timestamp edges; those rows have no equivalent in v020. The v003 leakage paragraph's explicit same-bin action, future measurement-frequency, repeated-stay, and outcome-driven grid/threshold checks are reduced to general pre-landmark availability and later audit-record language. These omissions weaken reproducibility and future-information protection without a declared scientific change.
  - protected_id: PCR-009
    prior_locator: "Structured abstract; Contribution, innovation, impact, application, and closest-work comparison > Contribution and evidence ladder"
    revised_locator: "Structured abstract; Data, materials, and existing evidence base > Current verified-resource versus prospective status; Contribution, innovation, impact, application, and closest-work comparison > Contribution and evidence levels; final closest-work paragraph"
    semantic_status: preserved
    evidence: >-
      v020 repeatedly describes models, simulations, external validation, and trial analyses as planned or not generated. The contribution remains conditional integration, validation, and benchmark/resource value; individual modules are acknowledged as established, and the complete-combination gap remains explicitly low-to-moderate confidence with no new-algorithm or global-first claim.
  - protected_id: PCR-010
    prior_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Resources and governance; Risk and automatic alternative matrix; Remaining execution gates; Identity and final stop boundary"
    revised_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Feasibility and resources; Working assumptions; Limitations and boundary conditions; Risks, alternatives, and stop conditions"
    semantic_status: preserved
    evidence: >-
      The revised section is the sole complete authority location and covers access and personnel, G1 support, labels and leakage, recoverability, MNAR and overlap, external transport, timing, trial authorization and semantics, common anchors and mapping, causal and application boundaries, and closest-work uncertainty. Its risk table retains the corresponding backup, downgrade, or stop consequences, including the numerical cross-hospital support triggers, and no other section substitutes a competing complete limitations catalogue.
  - protected_id: PCR-011
    prior_locator: "Research content and work packages > Twenty-four-month minimum and dated gates; Feasibility, resources, risks, alternatives, and stop conditions > Identity and final stop boundary"
    revised_locator: "Research content and work packages > Twenty-four-month scope and dated decisions; Feasibility, resources, risks, alternatives, and stop conditions > Limitations and boundary conditions item 6; Risks, alternatives, and stop conditions"
    semantic_status: preserved
    evidence: >-
      v020 states that stages I-II must finish within 24 months and that stage III is outside the minimum delivery and conditional on stage-II success, trial data and semantics, and observation mapping. It also states that subsequent trial results cannot compensate for failures in resources, simulation recovery, primary tasks, leakage, or external testing.
  - protected_id: PCR-012
    prior_locator: "Research question, objectives, and core hypothesis > Core hypothesis and non-hypotheses; Feasibility, resources, risks, alternatives, and stop conditions"
    revised_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Limitations and boundary conditions item 9"
    semantic_status: preserved
    evidence: >-
      v020 retains the full prohibition on inferring a causal network, treatment causal effect, counterfactual policy, mechanism, mediation, control, or digital twin from observational data or prediction, and on treating the conditional trial analysis as validation of unmeasured dynamics, transition relations, or the full system. It also retains the exclusions of a validated model, clinical decision tool, drug platform, and unconditional implementation basis.
undeclared_scientific_changes:
  - change_id: USC-R021-001
    protected_id: PCR-008
    change: >-
      v020 removes prespecified event-clock, baseline-SOFA, repeated-landmark, within-bin temporal-ordering, and explicit leakage-control commitments while the revision delta declares that numerical specifications and all protected scientific boundaries were preserved.
findings:
  - finding_id: CPF-R021-001
    severity: major
    protected_id: PCR-008
    prior_locator: "Research design and methods > Protocol locks for the two primary clinical tasks"
    revised_locator: "Research design and methods > Protocol locks for the two primary clinical tasks"
    finding: >-
      The revised protocol table is not merely a shorter restatement. It no longer makes several frozen operational rules traceable, including infection-pairing windows, baseline SOFA construction, overlapping-landmark handling, within-bin action and next-state ordering, and exclusion of unsortable same-timestamp edges. Because these rules determine cohort membership, temporal eligibility, and leakage control, their omission exceeds an editorial move or merge.
  - finding_id: CPF-R021-002
    severity: major
    locator: "Revision delta > Scope and result; Protected-content disposition > PCR-008"
    finding: >-
      The delta says that numerical specifications and all protected scientific boundaries were preserved and reports PCR-008 as retained, but it does not declare the protocol-detail removals above. The declaration therefore does not provide the scientific-change routing required for scientific_change_declared.
unresolved_issues: []
---

# Content-preservation check

## Decision rationale

The research identity, evidence status, stage conditionality, principal limitations, and unsupported-claim boundaries remain intact. The decision is nevertheless `editorial_scope_violation` because PCR-008 is only partially traceable in v020. The missing protocol rules govern event construction, repeated observations, temporal ordering, and leakage prevention; removing them changes the executable scientific specification even though no replacement values were introduced. The revision delta labels the work as editorial and does not declare these removals as scientific changes, so `scientific_change_declared` does not apply. The central object and question are unchanged, so `identity_drift_detected` does not apply.

## Protected-content trace

PCR-001 through PCR-007 and PCR-009 through PCR-012 remain traceable through the revised frontmatter, research question, staged work plan, resource-status table, methods, and the consolidated limitations and risk section. PCR-008 retains the high-level task definitions and most endpoints, but v003's exact event-clock and temporal-ordering safeguards are absent from v020 rather than moved to another location. The later audit-deliverable list asks for records of leakage checks but does not restore the omitted operational definitions.

## Required routing

The dossier must return for correction or scientific review before fresh narrative or language assessment. It may proceed only after the missing PCR-008 commitments are restored with the same meaning, or after the revision delta explicitly declares and routes the scientific changes for review, followed by a new independent preservation check.
