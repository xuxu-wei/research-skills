---
schema_version: research-idea-content-preservation-check.v1
check_id: content-preservation-I01-001-r087
review_id: content-preservation-review-I01-001-r087
reviewer_skill: idea-narrative-assessor
reviewer_instance_id: fresh-preservation-r087
workflow_id: RID-SEPSIS-CSM-20260717-001
round_id: r087
input_artifact_ids:
  - idea-dossier-I01-001-v003
  - idea-dossier-I01-001-v047
  - protected-content-register-I01-001-v004-r004
  - revision-delta-I01-001-v003-to-v047
input_versions:
  - v003
  - v047
  - r004
  - v003-to-v047
inputs:
  prior_dossier:
    artifact_id: idea-dossier-I01-001-v003
    version: v003
    path: tests/idea-test-0.9.0-preview.1/0.9.0-preview.1/03_ideas/nodes/I01-001/dossiers/idea-dossier-v003.md
  revised_dossier:
    artifact_id: idea-dossier-I01-001-v047
    version: v047
    path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v13/idea-dossier-v047.md
  protected_content_register:
    artifact_id: protected-content-register-I01-001-v004-r004
    version: r004
    path: tests/idea-narrative-forward-0.9.0-preview.3/run-001/inputs/protected-content-register-v004.yaml
  revision_delta:
    artifact_id: revision-delta-I01-001-v003-to-v047
    version: v003-to-v047
    path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v13/revision-delta-v003-to-v047.md
files_read:
  - tests/idea-test-0.9.0-preview.1/0.9.0-preview.1/03_ideas/nodes/I01-001/dossiers/idea-dossier-v003.md
  - tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v13/idea-dossier-v047.md
  - tests/idea-narrative-forward-0.9.0-preview.3/run-001/inputs/protected-content-register-v004.yaml
  - tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v13/revision-delta-v003-to-v047.md
isolation_mode: fresh_subagent
prior_scores_visible: false
source_edits_performed: false
decision: scientific_content_preserved
protected_item_checks:
  - protected_id: PCR-001
    prior_locator: "YAML frontmatter identity_anchor; Research question, objectives, and core hypothesis > Primary research question"
    revised_locator: "YAML frontmatter identity_anchor; H1 and one-sentence summary; Background; Gap; Research question, objectives, and core hypothesis > Primary research question"
    semantic_status: preserved
    evidence: >-
      The frontmatter identity anchor is unchanged. The revised background and question still cover the sepsis-centred longitudinal ICU system from comparable pre-onset risk intervals through first onset, mutually exclusive post-onset evolution, recovery or persistent deterioration, organ failure, alive ICU exit, and death. The question remains recovery and cross-database testing of a candidate dynamic-system representation and is not recast as generic prediction or generic ICU risk stratification.
  - protected_id: PCR-002
    prior_locator: "YAML frontmatter identity_anchor.primary_objective; Research question, objectives, and core hypothesis > Objectives; frozen register source_context_locator"
    revised_locator: "One-sentence summary; Structured abstract > Objective and hypothesis; Research content and work packages; Contribution and evidence ladder"
    semantic_status: preserved
    evidence: >-
      The revised dossier separately retains the 24-month stage-I–II commitment, literature and expert knowledge constraints, public-ICU system identification and cross-database testing, and full-course representation. It also explicitly commits to one or more high-level papers, auditable scientific evidence, and reusable resources, and states that delivery does not contract to a single prediction tool.
  - protected_id: PCR-003
    prior_locator: "YAML frontmatter identity_anchor.study_object and primary_unit_of_inference; Research design and methods"
    revised_locator: "YAML frontmatter identity_anchor; one-sentence summary; Structured abstract > Objective and hypothesis; Protocol definitions for the two primary clinical tasks; Observational target, anchoring, missingness, and abstention"
    semantic_status: preserved
    evidence: >-
      The study object remains the longitudinal sepsis-centred ICU patient system with comparable at-risk non-onset intervals and post-onset trajectories. Patient–time state and transition remain the primary inference unit; overlapping assessment times retain total stay weight 1, and patient and hospital clustering remains part of uncertainty estimation.
  - protected_id: PCR-004
    prior_locator: "Data, materials, and existing evidence base > Current verified-resource versus prospective-gate status; Public ICU database roles and G1 audit"
    revised_locator: "Data, materials, and existing evidence base > Current resource and evidence status; Public ICU database roles and G1 audit fields; Feasibility and resources; Limitations and boundary conditions items 1–2"
    semantic_status: preserved
    evidence: >-
      Inputs remain literature and expert knowledge, MIMIC-IV and eICU-CRD, with HiRID or AmsterdamUMCdb prospectively selected as a conditional backup. Only database existence and public versions are verified. Team credentials, data-use agreements, runnable extraction, exact cohort support, named staff commitments, and model or analysis results remain unverified or not generated; none is presented as already available.
  - protected_id: PCR-005
    prior_locator: "Data, materials, and existing evidence base > Local RCT evidence and present limits"
    revised_locator: "Data, materials, and existing evidence base > Current resource and evidence status; 本地随机对照试验证据及当前状态; 主体研究完成后的两项随机对照试验次要分析 > 共同前提; Limitations and boundary conditions items 8–9"
    semantic_status: preserved
    evidence: >-
      EXIT-SEP and XBJ-SCAP remain potential individual-level sources only for conditional work after the primary study. Their local reports remain derivative cleaning and validation evidence and do not substitute for individual-data authorization, original CRF or SAP, randomization and centre information, visit timing, or death, hospital, discharge, and transfer semantics.
  - protected_id: PCR-006
    prior_locator: "Research content and work packages; Research design and methods, including Observational target, anchoring and abstention"
    revised_locator: "Research content and work packages > Work packages and minimum sequence; Variable-use separation; Observational target, anchoring, missingness, and abstention; Absolute simulation and semi-synthetic recovery criteria; Hospital-primary cross-database validation"
    semantic_status: preserved
    evidence: >-
      The minimum order remains resources and G1 audit, label/state/hospital-partition fixation, simple baselines, absolute recovery and false-confidence checks, at most one complex candidate, two primary tasks and two secondary diagnostics, fixed analysis specification, and untouched cross-database testing, with trial work only after stage II. X_t, Y_t, A_t, M_t, labels, and baseline variables remain separated. The 20-seed alignment below 90%, bootstrap retention below 80%, external sign consistency below 80%, state alignment below 0.70, and uncalibrated-interval rules still require deletion, merging, or database/policy-specific interpretation, and predictive performance cannot change those dispositions.
  - protected_id: PCR-007
    prior_locator: "Research content and work packages > Conjunctive minimum success definition; Research design and methods > Hospital-primary genuine cross-database validation"
    revised_locator: "Research content and work packages > Conjunctive minimum success definition; Research design and methods > Hospital-primary cross-database validation; Expected outputs, falsification criteria, and interpretations; Limitations and boundary conditions items 6–7"
    semantic_status: preserved
    evidence: >-
      Stage-II support remains conjunctive across data support, absolute recovery, proper scores and calibration for both primary tasks, leakage clearance, zero-update external performance, state alignment, and structural sign stability. Recalibration, observation-layer updating, and complete refitting remain separately labelled and cannot replace zero-update failure. Work after 24 months is outside the minimum delivery and cannot supply missing stage-II evidence.
  - protected_id: PCR-008
    prior_locator: "Research design and methods > Protocol locks for the two primary clinical tasks; Mutually exclusive post-onset state/event system"
    revised_locator: "Research design and methods > Protocol definitions for the two primary clinical tasks; Mutually exclusive post-onset state and event system; Key techniques and implementation items 1 and 4"
    semantic_status: preserved
    evidence: >-
      Both primary tasks retain the event and availability clocks, incident risk set, delayed entry, mutually exclusive post-onset states, competing termination, as-of feature rules, calibration and proper-score targets, and patient/hospital clustering. The specimen–antibiotic 72-hour/24-hour pairing, baseline-SOFA rule, rolling 24-hour calculation, first sortable onset, first-onset-only rule, total stay weight 1, within-window A_t/next-state ordering, exclusion of unsortable same-time transitions, and all listed future-information, treatment, measurement-frequency, repeated-record, split, imputation, grid, and threshold leakage checks remain explicit.
  - protected_id: PCR-009
    prior_locator: "Structured abstract; Contribution, innovation, impact, application, and closest-work comparison > Contribution and evidence ladder"
    revised_locator: "Title, summary, audience, and positioning; Structured abstract; Data, materials, and existing evidence base > Current resource and evidence status; Contribution and evidence ladder; Verified representative closest-work comparison; Title and positioning claim-support table"
    semantic_status: preserved
    evidence: >-
      The revised dossier consistently describes a planned candidate representation and planned analyses; model fitting, simulation recovery, external testing, and new trial results remain not generated. The contribution remains conditional evidence integration, validation, benchmark, and reusable-resource value. Individual modules are acknowledged as prior art, the complete-work gap remains a low-to-medium-confidence bounded-search finding, and no global-first or new-algorithm claim is made.
  - protected_id: PCR-010
    prior_locator: "Feasibility, resources, risks, alternatives, and stop conditions; Research design and methods; Expected outputs, falsification criteria, and interpretations"
    revised_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Working assumptions; Limitations and boundary conditions; Research design and methods; Expected outputs, falsification criteria, and interpretations"
    semantic_status: preserved
    evidence: >-
      Section 14 is the sole complete authority for resource/access, team, G1, label/leakage, recoverability, MNAR and overlap, zero-update external testing, dated gates, trial-data semantics, observation mapping, closest-work uncertainty, and claim boundaries. It retains both unresolved specifications: clinical-scale-to-simulation-parameter mapping and the exact multicategory-calibration estimator, confidence bounds, and threshold registration. Screening counts do not replace empirical effective support or simulation stability. Method eligibility and method-specific consequences remain in section 7, falsification and result-dependent interpretations in section 11, and inconsistent or imprecise trial directions cannot be reinterpreted through subgroup selection.
  - protected_id: PCR-011
    prior_locator: "Research content and work packages > Twenty-four-month minimum and dated gates; Identity and final stop boundary"
    revised_locator: "H1 and summary; Research question, objectives, and core hypothesis; Research content and work packages > Work packages and minimum sequence; 主体研究完成后的两项随机对照试验次要分析; function-specific trial entries in sections 6 and 8–11; Limitations and boundary conditions items 7–9"
    semantic_status: preserved
    evidence: >-
      Stage I–II remains the 24-month minimum. The trial-method authority first states the shared prerequisites of successful stage II, available individual data, and verifiable core trial semantics, then separately presents the observation-mapping route, the independent clinical-state route when mapping fails but its own conditions hold, and the semantic stop. Mapping-specific eligibility is not made a shared prerequisite. No later trial result can supplement stage-II failure. The title omits trial work, the summary and abstract each keep only a high-level subordinate purpose, and other sections carry only their data-status, interface, evidence, analysis, output, limitation, or operational-risk function rather than duplicating the branch tree.
  - protected_id: PCR-012
    prior_locator: "Research question, objectives, and core hypothesis > Core hypothesis and non-hypotheses; Feasibility, resources, risks, alternatives, and stop conditions"
    revised_locator: "Feasibility, resources, risks, alternatives, and stop conditions > Claims not supported by the current design; minimal adjacent boundaries in the primary question, observational target, trial methods, and interpretation matrix"
    semantic_status: preserved
    evidence: >-
      The complete prohibited-claim inventory appears once in section 14: observational data and prediction do not establish a true causal network, treatment effects, counterfactual policy, mechanism, mediation, control, or digital twin; trial secondary analyses do not validate unmeasured dynamics, transition edges, or the whole representation; and the plan is not an already validated model, clinical decision tool, drug platform, global first, new algorithm, or unconditional promotion basis. Elsewhere only a locally necessary interpretation boundary remains, without a second grouped inventory.
undeclared_scientific_changes: []
findings: []
unresolved_issues: []
---

# Content-preservation check

## Decision rationale

All twelve frozen protected items remain traceable in v047 with the same study identity, scientific meaning, numerical and temporal rules, evidence status, claim strength, limitations, contingencies, and stopping consequences. The revised dossier changes titles, terminology, disclosure order, consolidation, and section function, but it does not add data, methods, results, or evidence; present planned work as completed; strengthen novelty or clinical claims; conceal a feasibility finding; or make a conditional branch unconditional.

The frontmatter identity anchor is unchanged field for field. The reader-facing question remains centred on a longitudinal sepsis ICU system and retains the conditional downstream randomized-trial purpose without converting the dossier to ordinary prediction. The revised title and summary narrow the prominence of downstream trial work while the sole technical authority preserves its shared prerequisites, two mutually exclusive routes, and stopping rule.

## Protected-content trace

- The complete limitation and working-assumption inventory was consolidated into section 14. Method eligibility and consequences remain at their section-7 authority, and falsification and result-dependent interpretation remain in section 11.
- Trial detail was removed from the title and compressed in the summary and abstract to a subordinate purpose. The full EXIT-SEP and XBJ-SCAP eligibility, mapping, independent-analysis, missing-data, multiplicity, non-pooling, and stop logic remains in the trial-method subsection.
- G1, zero-update external testing, and the independent trial endpoint were expanded or renamed without changing their referents, thresholds, update restrictions, or evidential meaning.
- Claim language remains prospective and bounded. Resource, access, staffing, audit, model, external-test, and trial-analysis statuses remain unverified or not generated where they were unverified or not generated in v003.

## Revision-delta fidelity

The delta's protected-content mapping is consistent with the frozen v047 dossier for PCR-001 through PCR-012. Its statements that the work was editorial-only, that scientific identity and conditions were retained, that trial logic was consolidated at the method authority, and that limitation and unsupported-claim inventories were consolidated in section 14 are supported by the prior-to-revised comparison. The delta does not declare a scientific change, and no undeclared scientific change was found.

## Required routing

The dossier may proceed to fresh narrative and academic-language assessment.
