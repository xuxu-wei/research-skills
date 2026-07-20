---
schema_version: research-idea-content-preservation-check.v1
check_id: "content-preservation-check-I01-001-r030"
review_id: "content-preservation-review-I01-001-r030"
reviewer_skill: idea-narrative-assessor
reviewer_instance_id: "fresh-preservation-r030"
workflow_id: "RID-SEPSIS-CSM-20260717-001"
round_id: "r030"
input_artifact_ids:
  - "idea-dossier-I01-001-v003"
  - "idea-dossier-I01-001-v023"
  - "protected-content-register-I01-001-v003"
  - "revision-delta-I01-001-v003-to-v023"
input_versions:
  - "v003"
  - "v023"
  - "v003"
  - "v003-to-v023"
inputs:
  prior_dossier:
    artifact_id: "idea-dossier-I01-001-v003"
    version: "v003"
    path: "tests/idea-test-0.9.0-preview.1/0.9.0-preview.1/03_ideas/nodes/I01-001/dossiers/idea-dossier-v003.md"
  revised_dossier:
    artifact_id: "idea-dossier-I01-001-v023"
    version: "v023"
    path: "tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/revised/idea-dossier-v023.md"
  protected_content_register:
    artifact_id: "protected-content-register-I01-001-v003"
    version: "v003"
    path: "tests/idea-narrative-forward-0.9.0-preview.3/run-001/inputs/protected-content-register.yaml"
  revision_delta:
    artifact_id: "revision-delta-I01-001-v003-to-v023"
    version: "v003-to-v023"
    path: "tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/revised/revision-delta-v003-to-v023.md"
files_read:
  - "tests/idea-test-0.9.0-preview.1/0.9.0-preview.1/03_ideas/nodes/I01-001/dossiers/idea-dossier-v003.md"
  - "tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/revised/idea-dossier-v023.md"
  - "tests/idea-narrative-forward-0.9.0-preview.3/run-001/inputs/protected-content-register.yaml"
  - "tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/revised/revision-delta-v003-to-v023.md"
isolation_mode: fresh_subagent
prior_scores_visible: false
source_edits_performed: false
decision: scientific_content_preserved
protected_item_checks:
  - protected_id: PCR-001
    prior_locator: "YAML frontmatter identity_anchor; Research question, objectives, and core hypothesis > Primary research question"
    revised_locator: "YAML frontmatter identity_anchor; Title, summary, audience, and positioning; Research question, objectives, and core hypothesis > Primary research question; Feasibility, resources, risks, alternatives, and stop conditions > Identity boundary"
    semantic_status: preserved
    evidence: >-
      The frontmatter research question is unchanged. The revised question, summary, and identity boundary retain the knowledge-constrained, uncertainty-aware sepsis-centered candidate representation across comparable pre-onset risk intervals, first onset, mutually exclusive post-onset evolution, and outcomes. Recovery, persistent sepsis, deterioration or new organ failure, live ICU exit, transfer or loss of observation, and death remain explicit in the revised state system. The study is not reframed as ordinary prediction or generic ICU risk stratification.
  - protected_id: PCR-002
    prior_locator: "YAML frontmatter identity_anchor.primary_objective; Research question, objectives, and core hypothesis > Objectives"
    revised_locator: "YAML frontmatter identity_anchor.primary_objective; Title, summary, audience, and positioning; Research question, objectives, and core hypothesis > Objectives; Research content and work packages; Expected outputs, falsification criteria, and interpretations"
    semantic_status: preserved
    evidence: >-
      The frontmatter objective remains completion of stages I-II within 24 months. The revised summary, objectives, milestones, work packages, and planned outputs retain literature and expert constraints, public ICU data, system identification, full-course state representation, independent cross-database validation, auditable evidence, a high-level publication direction, reusable benchmarks, and research resources. The objective is not reduced to producing a prediction tool.
  - protected_id: PCR-003
    prior_locator: "YAML frontmatter identity_anchor.study_object and primary_unit_of_inference; Research design and methods"
    revised_locator: "YAML frontmatter identity_anchor.study_object and primary_unit_of_inference; Research question, objectives, and core hypothesis; Research design and methods > Prespecified protocol for the two primary clinical tasks; Observational estimand, anchoring, missingness, and support; Feasibility, resources, risks, alternatives, and stop conditions > Identity boundary"
    semantic_status: preserved
    evidence: >-
      The study object and inference-unit fields are unchanged. The revised question and protocol continue to include comparable not-yet-onset risk intervals and post-onset trajectories, while the observational estimand and uncertainty procedures retain patient-time states and state transitions with patient and hospital clustering. No different population, object, or primary inference unit is introduced.
  - protected_id: PCR-004
    prior_locator: "Data, materials, and existing evidence base > Current verified-resource versus prospective-gate status; Public ICU database roles and G1 audit"
    revised_locator: "Data, materials, and existing evidence base > Current resource and evidence status; Public ICU database roles and observability audit; Feasibility, resources, risks, alternatives, and stop conditions > Feasibility and resources; Working assumptions and specifications still to be frozen; Limitations and boundary conditions"
    semantic_status: preserved
    evidence: >-
      The revised dossier retains literature and expert priors, MIMIC-IV v3.1 as the planned development database, eICU-CRD v2.0 as the planned external database, and HiRID or AmsterdamUMCdb as a prospectively selected conditional backup. Database existence and versions remain verified, whereas team credentials, data-use agreements, runnable extraction, project-specific cohort support, named personnel, and all model or analysis results remain unverified or not generated. These prospective resources are never presented as already available.
  - protected_id: PCR-005
    prior_locator: "Data, materials, and existing evidence base > Local RCT evidence and present limits"
    revised_locator: "Data, materials, and existing evidence base > Current resource and evidence status; Available local evidence for the two randomized trials; Research design and methods > Conditional trial observation mapping and independent alternative analysis; Feasibility, resources, risks, alternatives, and stop conditions > Working assumptions and specifications still to be frozen; Limitations and boundary conditions"
    semantic_status: preserved
    evidence: >-
      EXIT-SEP and XBJ-SCAP remain only potential individual-level sources for conditional stage III secondary analyses. The revised resource table and trial paragraphs continue to classify the local materials as derivative reports describing cleaning, coverage, and visit sparsity. Individual-data authorization, original case-report forms or statistical analysis plans, randomization and center information, visit timing, and survival, hospitalization, discharge, and transfer semantics remain subject to primary-source verification before any new state endpoint.
  - protected_id: PCR-006
    prior_locator: "Research content and work packages; Research design and methods"
    revised_locator: "Research content and work packages > Twenty-four-month minimum and dated milestones; Work packages and fixed sequence; Research design and methods; Key techniques and implementation; Feasibility, resources, risks, alternatives, and stop conditions > Risks, alternatives, and stop conditions"
    semantic_status: preserved
    evidence: >-
      The revised fixed sequence remains resources and observability audit, labels and states and hospital split, simple baselines, prespecified simulation recovery and false-structure checks, at most one complex candidate, two primary tasks and two secondary diagnostics, development freeze, untouched cross-database testing, and only then conditional trial analysis. The physiological state, treatment-action, measurement-process, label, and baseline roles remain separated. Anchoring, alignment, recoverability, transportability, numerical support thresholds, and abstention or downgrade rules retain the same interpretive limits.
  - protected_id: PCR-007
    prior_locator: "Research content and work packages > Conjunctive minimum success definition; Research design and methods > Hospital-primary genuine cross-database validation"
    revised_locator: "Research content and work packages > Conjunctive minimum success definition; Research design and methods > Hospital-primary independent cross-database validation; Expected outputs, falsification criteria, and interpretations; Feasibility, resources, risks, alternatives, and stop conditions > Limitations and boundary conditions; Risks, alternatives, and stop conditions"
    semantic_status: preserved
    evidence: >-
      Stage II remains a conjunction of data support, simulation recovery and false-structure control, proper scoring and calibration for both primary tasks, clearance of severe leakage, zero-update untouched external performance, state alignment, and structural sign stability. The +0.01 Brier upper-bound criterion, 0.80-1.20 calibration slope, 0.02 absolute-risk error, at least 20 test hospitals, at least 0.70 state alignment, and at least 0.80 sign consistency are unchanged. Calibration-only and observation-model updates remain separate from zero update and cannot replace its failure; stage III remains outside and cannot complete stage II.
  - protected_id: PCR-008
    prior_locator: "Research design and methods > Protocol locks for the two primary clinical tasks; Mutually exclusive post-onset state/event system"
    revised_locator: "Research design and methods > Prespecified protocol for the two primary clinical tasks; Mutually exclusive post-onset state and event system; Observational estimand, anchoring, missingness, and support; Feasibility, resources, risks, alternatives, and stop conditions > Limitations and boundary conditions; Risks, alternatives, and stop conditions"
    semantic_status: preserved
    evidence: >-
      Both primary tasks retain event and availability clocks, the first-onset risk set, delayed entry, mutually exclusive post-onset states, competing termination, as-of features, proper scoring and calibration, clustered uncertainty, and leakage safeguards. The full protocol still includes specimen-antibiotic pairing with 72-hour and 24-hour directions, baseline SOFA rules, rolling 24-hour component calculation, the first sortable onset, first onset only, total overlapping-landmark stay weight of 1, within-bin action followed by next-boundary physiology, exclusion of unsortable same-timestamp transitions, and checks for same-bin treatment, future measurement frequency, repeated stays, cross-split processing, and outcome-driven variables, grids, or thresholds. Recovery still requires 24 hours; the day-7 target and day-14 sensitivity remain unchanged.
  - protected_id: PCR-009
    prior_locator: "Structured abstract; Contribution, innovation, impact, application, and closest-work comparison > Contribution and evidence ladder"
    revised_locator: "Structured abstract; Data, materials, and existing evidence base > Current resource and evidence status; Contribution, innovation, impact, application, and closest-work comparison; Title and positioning claim-support table; Feasibility, resources, risks, alternatives, and stop conditions > Limitations and boundary conditions"
    semantic_status: preserved
    evidence: >-
      The revised dossier consistently describes a planned candidate representation and planned validation; no model, recovery result, external validation result, or new trial analysis is presented as existing. It retains the 2026-07-17 bounded representative search, the high-confidence conclusion that individual modules have precedents, and only low-to-moderate confidence for the unlocated complete combination. It explicitly states that the search is not systematic and cannot establish global absence. The contribution remains conditional integration, validation, benchmark, resource, and failure evidence, with no new-algorithm or global-first claim.
  - protected_id: PCR-010
    prior_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Resources and governance; Risk and automatic alternative matrix; Remaining execution gates; Identity and final stop boundary"
    revised_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Feasibility and resources; Working assumptions and specifications still to be frozen; Limitations and boundary conditions; Risks, alternatives, and stop conditions; Identity boundary"
    semantic_status: preserved
    evidence: >-
      Section 14 is the single complete authority location in the revision. Its feasibility statement, nine unresolved-specification rows, five limitation domains, ten risk rows, and identity boundary retain resource and access limits, personnel commitments, G1 support, label and leakage uncertainty, recoverability, nonrandom missingness and low overlap, external transport, schedule gates, trial data and semantics, common anchors and observation mapping, and closest-work uncertainty. Each source trigger retains a bounded alternative and stopping or downgrade consequence, including the event-per-parameter, anchor-density and coverage, cross-partition exclusion, simulation, external-test, trial-mapping, and timing conditions.
  - protected_id: PCR-011
    prior_locator: "Research content and work packages > Twenty-four-month minimum and dated gates; Identity and final stop boundary"
    revised_locator: "Title, summary, audience, and positioning; Research content and work packages > Twenty-four-month minimum and dated milestones; Work packages and fixed sequence; Feasibility, resources, risks, alternatives, and stop conditions > Working assumptions and specifications still to be frozen; Risks, alternatives, and stop conditions"
    semantic_status: preserved
    evidence: >-
      Stages I-II remain due within 24 months and stage III remains after the minimum deliverable. Trial analysis still requires successful and frozen stage II plus qualified individual data, trial semantics, and a successful observation mapping or the prespecified independent alternative. The month 12, month 20, and month 24 consequences remain explicit, and the revised timing rule states that stage III cannot change a stage II failure or bypass resource, recovery, primary-task, or external-validation requirements.
  - protected_id: PCR-012
    prior_locator: "Research question, objectives, and core hypothesis > Core hypothesis and non-hypotheses; Feasibility, resources, risks, alternatives, and stop conditions"
    revised_locator: "Research design and methods > Observational estimand, anchoring, missingness, and support; Conditional trial observation mapping and independent alternative analysis; Expected outputs, falsification criteria, and interpretations; Title and positioning claim-support table; Feasibility, resources, risks, alternatives, and stop conditions > Limitations and boundary conditions"
    semantic_status: preserved
    evidence: >-
      The observational estimand still excludes intervention effects and counterfactual policies, and the limitations retain the prohibition on interpreting observational prediction or joint modeling as a true causal network, treatment effect, mechanism, mediation, or control. Trial analyses remain limited to visit-specific randomized-group differences in an observed-variable projection or an independent clinical-state endpoint and cannot validate unmeasured dynamics, transition edges, latent targets, or the full system. The plan is still not presented as an already validated model, clinical decision tool, drug platform, digital twin, or unconditional basis for clinical promotion.
undeclared_scientific_changes: []
findings: []
unresolved_issues: []
---

# Content-preservation check

## Decision rationale

The scientific content is preserved. Independent comparison of every frozen item and every complete source-locator passage found no change to the study identity, objective, study object, evidence base, inference unit, protocol, numerical or temporal commitments, estimands, validation logic, feasibility status, claim strength, or conditional stage structure. The revision delta declares an editorial-only change, and the source-to-revision comparison supports that declaration. No new data, method, endpoint, result, evidence source, or stronger claim was added.

## Protected-content trace

The revision redistributes detail without changing its scientific function. Identity anchors remain in frontmatter and are restated in the question and final identity boundary. Numerical thresholds and protocol details remain in the methods, while complete limitations, unresolved specifications, alternatives, and stopping consequences are consolidated in section 14. The two trial branches remain mutually exclusive and trial-specific: a frozen observed-variable projection is analyzed only after all semantic and fidelity criteria are met; otherwise the analysis uses the independent death-ranked SOFA endpoint or stops when core trial semantics cannot be established. All source numerical thresholds, temporal commitments, trial counts, missing-data rules, and external-test isolation rules remain traceable in the revised dossier.

## Required routing

The revised dossier may proceed to fresh narrative and academic-language assessment. Any later substantive change requires a new preservation comparison before further progression.
