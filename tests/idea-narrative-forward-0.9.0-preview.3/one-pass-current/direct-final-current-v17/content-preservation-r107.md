---
schema_version: research-idea-content-preservation-check.v1
check_id: content-preservation-I01-001-v051-r107
review_id: content-preservation-I01-001-v051-r107
reviewer_skill: idea-narrative-assessor
reviewer_instance_id: idea-narrative-preservation-r107-fresh-20260720
workflow_id: RID-SEPSIS-CSM-20260717-001
round_id: r107
input_artifact_ids:
  - idea-dossier-I01-001-v003
  - idea-dossier-I01-001-v051
  - protected-content-register-I01-001-v004-r004
  - revision-delta-I01-001-v003-to-v051
input_versions:
  - v003
  - v051
  - r004
  - v051
inputs:
  prior_dossier:
    artifact_id: idea-dossier-I01-001-v003
    version: v003
    path: tests/idea-test-0.9.0-preview.1/0.9.0-preview.1/03_ideas/nodes/I01-001/dossiers/idea-dossier-v003.md
  revised_dossier:
    artifact_id: idea-dossier-I01-001-v051
    version: v051
    path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v17/idea-dossier-v051.md
  protected_content_register:
    artifact_id: protected-content-register-I01-001-v004-r004
    version: r004
    path: tests/idea-narrative-forward-0.9.0-preview.3/run-001/inputs/protected-content-register-v004.yaml
  revision_delta:
    artifact_id: revision-delta-I01-001-v003-to-v051
    version: v051
    path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v17/revision-delta-v003-to-v051.md
files_read:
  - tests/idea-test-0.9.0-preview.1/0.9.0-preview.1/03_ideas/nodes/I01-001/dossiers/idea-dossier-v003.md
  - tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v17/idea-dossier-v051.md
  - tests/idea-narrative-forward-0.9.0-preview.3/run-001/inputs/protected-content-register-v004.yaml
  - tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v17/revision-delta-v003-to-v051.md
isolation_mode: fresh_subagent
prior_scores_visible: false
source_edits_performed: false
decision: scientific_content_preserved
protected_item_checks:
  - protected_id: PCR-001
    prior_locator: "YAML frontmatter identity_anchor; Research question, objectives, and core hypothesis > Primary research question; Mutually exclusive post-onset state/event system"
    revised_locator: "YAML frontmatter identity_anchor; Research question, objectives, and core hypothesis > Primary research question; Research design and methods > Mutually exclusive post-onset state and event system"
    semantic_status: preserved
    evidence: >-
      The five identity_anchor values are character-for-character identical in v003 and v051. The revised primary question still concerns a sepsis-centered candidate dynamic-system representation spanning comparable at-risk non-onset intervals, first onset, post-onset evolution, and outcomes; the state authority still includes recovery, persistent sepsis, deterioration or new organ failure, live ICU exit, transfer or loss of observation, and death. The revised dossier keeps this distinct from ordinary prediction or general ICU risk stratification and retains the non-causal boundary.
  - protected_id: PCR-002
    prior_locator: "YAML frontmatter identity_anchor.primary_objective; Research question, objectives, and core hypothesis > Objectives; frozen PCR-002 source_context_locator for the binding delivery direction"
    revised_locator: "YAML frontmatter identity_anchor.primary_objective; Research question, objectives, and core hypothesis > Objectives and delivery-direction sentence"
    semantic_status: preserved
    evidence: >-
      The primary_objective value is unchanged. The revised objectives retain completion of stages I-II within 24 months, literature and expert constraints, public-ICU-data model construction, recovery testing, and cross-database validation. The register-authorized context value omitted from the prior dossier is restored explicitly as one or more high-level papers and auditable scientific evidence, rather than delivery of only a predictive tool; this restoration is declared in the frozen register and is not an undeclared scientific addition.
  - protected_id: PCR-003
    prior_locator: "YAML frontmatter identity_anchor.study_object and identity_anchor.primary_unit_of_inference; Research design and methods > Observational target, anchoring and abstention"
    revised_locator: "YAML frontmatter identity_anchor.study_object and identity_anchor.primary_unit_of_inference; Research design and methods > Observational target, anchoring, and evidence-qualified interpretation"
    semantic_status: preserved
    evidence: >-
      Both machine-facing values are exactly unchanged. The revised method authority states that the study object is the longitudinal sepsis-centered ICU patient system containing comparable at-risk non-onset intervals and post-onset trajectories, and that inference concerns patient-time states and state transitions with patient and hospital clustering respected.
  - protected_id: PCR-004
    prior_locator: "Data, materials, and existing evidence base > Current verified-resource versus prospective-gate status; Public ICU database roles and G1 audit"
    revised_locator: "Data, materials, and existing evidence base > Current resource and result status; Public intensive-care database roles and support audit; Feasibility, resources, risks, alternatives, and stop conditions > Feasibility and resources"
    semantic_status: preserved
    evidence: >-
      Literature and expert priors, MIMIC-IV, and eICU-CRD remain the core inputs, while HiRID or AmsterdamUMCdb remains a conditionally pre-specified and equivalently audited backup. Database existence and versions are verified, but team credentials, data-use agreements, runnable extraction and exact extract version, project-cohort support, named personnel and available effort, and all model, simulation-recovery, prediction, external-test, or trial-reanalysis results remain unverified or not generated. No planned resource or result is presented as already available.
  - protected_id: PCR-005
    prior_locator: "Data, materials, and existing evidence base > Local RCT evidence and present limits"
    revised_locator: "Data, materials, and existing evidence base > Local randomized-trial evidence status; Feasibility, resources, risks, alternatives, and stop conditions > Limitations and boundary conditions item 7"
    semantic_status: preserved
    evidence: >-
      EXIT-SEP and XBJ-SCAP remain only conditional potential sources of individual-level randomized-trial data for stage III. The revised dossier preserves the reported sample and visit-availability counts and states that the local derivative reports do not establish individual-data authorization or replace original case-report forms, statistical analysis plans, or verification of randomization, centers, visit timing, and survival, hospitalization, or discharge semantics.
  - protected_id: PCR-006
    prior_locator: "Research content and work packages > Work packages and minimum route; Research design and methods > Observational target, anchoring and abstention; Absolute simulation and semi-synthetic recovery gate"
    revised_locator: "Research content and work packages > Work packages and minimum route; Research design and methods > Variable roles; Observational target, anchoring, and evidence-qualified interpretation; Absolute simulation and semi-synthetic recovery criteria"
    semantic_status: preserved
    evidence: >-
      The revised minimum route retains the ordered sequence from resource and observability audit through label, state, and hospital-split locking, simple competing-risk, multistate, and linear baselines, absolute simulation recovery and false-confidence checks, at most one complex candidate, two primary tasks and two secondary diagnostics, development freeze, untouched cross-database testing, and only then conditional trial analysis. Physiological state, treatment action, and measurement process remain separated. The authority text retains every protected action threshold: alignment below 90% across 20 seeds, bootstrap retention below 80%, external sign agreement below 80%, state alignment below 0.70, or uncalibrated intervals requires deletion, merging, or a database- or care-policy-specific limitation, regardless of predictive performance.
  - protected_id: PCR-007
    prior_locator: "Research content and work packages > Conjunctive minimum success definition; Research design and methods > Hospital-primary genuine cross-database validation"
    revised_locator: "Research content and work packages > Conjunctive minimum success definition; Research design and methods > Hospital-primary cross-database validation"
    semantic_status: preserved
    evidence: >-
      Stage-II success remains conjunctive across two-database support, absolute recovery, proper scoring and calibration for both primary tasks, absence of unresolved high-severity leakage, untouched no-update external performance, state alignment, and structural sign stability. Calibration-only and observation-layer adaptation remain separately reported and cannot compensate for failure of the no-update external test. Stage III remains outside, and cannot contribute to or repair, the stage-II conjunction.
  - protected_id: PCR-008
    prior_locator: "Research design and methods > Protocol locks for the two primary clinical tasks; Mutually exclusive post-onset state/event system"
    revised_locator: "Research design and methods > Protocol locks for the two primary clinical tasks; Mutually exclusive post-onset state and event system"
    semantic_status: preserved
    evidence: >-
      Both primary tasks, the event and information-availability clocks, first-onset risk set, delayed entry, mutually exclusive post-onset states, competing terminations, as-of features, proper-score and calibration targets, and patient- and hospital-clustered uncertainty remain intact. The revised protocol retains the specimen-antibiotic pairing windows of 72 hours and 24 hours, baseline-SOFA rule, rolling 24-hour component calculation, first sortable onset, first-onset-only analysis, total overlapping-landmark weight of 1 per stay, ordering of within-window action before the next state, and exclusion of unorderable same-timestamp edges. It also explicitly checks same-window treatment, future measurement frequency, repeat admissions, cross-split handling, and outcome-driven variables, grids, or thresholds.
  - protected_id: PCR-009
    prior_locator: "Structured abstract; Data, materials, and existing evidence base > Current verified-resource versus prospective-gate status; Contribution, innovation, impact, application, and closest-work comparison > Contribution and evidence ladder"
    revised_locator: "Structured abstract > Expected result and Contribution and impact; Data, materials, and existing evidence base > Current resource and result status; Contribution, innovation, impact, application, and closest-work comparison > Contribution and evidence ladder and closest-work comparison"
    semantic_status: preserved
    evidence: >-
      The revised dossier describes a planned candidate representation and planned validation: model, simulation-recovery, prediction, external-test, and trial-reanalysis results are expressly not generated. The defensible contribution remains conditional integration, validation, and benchmark or research-resource value. It retains that individual modules have precedents and that the apparent full-combination gap has only low-to-moderate confidence, and it makes no new-algorithm or global-first claim.
  - protected_id: PCR-010
    prior_locator: "Research design and methods; Expected outputs, falsification criteria, and interpretations; Feasibility, resources, risks, alternatives, and stop conditions"
    revised_locator: "Research design and methods; Expected outputs, falsification criteria, and interpretations; Feasibility, resources, risks, alternatives, and stop conditions > Working assumptions; Limitations and boundary conditions; Risks, alternatives, and stop conditions"
    semantic_status: preserved
    evidence: >-
      Section 14 is the single complete authority for limitations and working assumptions. It preserves resource and access status, team commitments, two-database support, labels and leakage, state recoverability, non-random missingness and low action overlap, no-update external evidence, timing, trial data and semantics, common anchors and observation mapping, and closest-work uncertainty. It retains both unresolved specifications: mapping clinical scales to simulation parameters, and the exact multicategory calibration estimator, confidence-bound calculation, and threshold-registration form. It also states that screening event or parameter minima do not replace empirical effective sample size, simulation stability, or clustered uncertainty. Full eligibility and mutually exclusive trial analyses remain in Methods; result falsification and result-dependent interpretation remain in section 11. Trial directions that disagree or have intervals that are too wide can support only no common direction or limited cross-setting applicability, and subgroup selection cannot change the primary interpretation.
  - protected_id: PCR-011
    prior_locator: "Research content and work packages > Twenty-four-month minimum and dated gates; Work packages and minimum route; Research design and methods > Conditional trial-observation projection and independent fallback; Identity and final stop boundary"
    revised_locator: "Title, summary, audience, and positioning; Structured abstract; Research question, objectives, and core hypothesis; Research content and work packages > 24-month minimum and timeline and Work packages and minimum route; Research design and methods > Conditional trial-observation mapping and independent analysis; downstream functional references in Evidence chains, Required analyses and evidence, Planned outputs, Contribution, claim-support, and section 14"
    semantic_status: preserved
    evidence: >-
      Stages I-II remain mandatory within 24 months and stage III remains outside the minimum delivery. The method authority first states only the three shared prerequisites: conjunctive stage-II success, analyzable individual data for the relevant trial, and verifiable core trial semantics. It then separately defines the observation-mapping branch, the independent SOFA ordered clinical-state endpoint available when mapping fails but its own data and semantic conditions hold, and stopping all new visit-outcome analysis when core semantics cannot be verified; mapping-specific anchor and fidelity conditions are explicitly excluded from the shared prerequisites. Later trial results cannot compensate for unmet stage-II resource, simulation-reconstruction, primary-task, or cross-database requirements. Reader-entry locations use only the high-level, conditional, per-trial secondary-analysis description; the timeline keeps one dependent work package, and the data, implementation, evidence-chain, required-analysis, output, contribution, claim-support, and section-14 locations retain only their own functions rather than duplicating the full branch logic.
  - protected_id: PCR-012
    prior_locator: "Research question, objectives, and core hypothesis > Core hypothesis and non-hypotheses; Feasibility, resources, risks, alternatives, and stop conditions"
    revised_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Limitations and boundary conditions item 11; local estimate- and result-specific boundaries in the summary, core hypothesis, and interpretation matrix"
    semantic_status: preserved
    evidence: >-
      Section 14 contains one complete prohibited-claim authority: observational data and predictive performance do not support a true causal network, treatment causal effects, counterfactual policies, mechanism, mediation, control, or digital-twin claims; the conditional trial secondary analyses cannot validate unmeasured latent dynamics, transition edges, structure beyond the measurement model, or the complete stage-II system. The plan is not described as an already validated model, clinical decision tool, drug platform, or basis for unconditional clinical promotion. Elsewhere, only locally necessary non-causal, estimand-specific, or result-specific boundaries remain, and no prohibited positive claim appears.
undeclared_scientific_changes: []
findings: []
unresolved_issues: []
---

# Content-preservation check

## Decision rationale

All twelve source-present protected items have one corresponding check and remain traceable in v051 with the same scientific meaning, evidence status, conditionality, and claim strength. The five machine-facing identity-anchor values are exactly unchanged. Direct comparison of the dossier text found no added data, method, result, evidence, strengthened claim, weakened limitation, or conditional element made unconditional. The revision delta declares no scientific change; its claims were not used as substitutes for evidence in the revised dossier.

## Protected-content trace

- Study identity and inference unit remain in the unchanged frontmatter and are restated at the observational-method authority.
- Resource and result states are consolidated in the data-status tables and section 14 without converting unverified access, team, cohort-support, model, validation, or trial-analysis status into completed work.
- Numeric rules, temporal rules, task definitions, branch eligibility, external-test precedence, and failure consequences remain at their method authorities.
- The complete limitation family, working assumptions, and prohibited-claim classes are consolidated in section 14; only locally necessary estimate- or result-specific boundaries occur elsewhere.
- Conditional stage III is presented at high level outside Methods, while its shared prerequisites, observation-mapping branch, independent SOFA branch, and semantic-stop condition remain fully specified once in the trial-method authority.

## Required routing

The revised dossier may proceed to fresh narrative and academic-language assessment. No return to scientific review is required on content-preservation grounds.
