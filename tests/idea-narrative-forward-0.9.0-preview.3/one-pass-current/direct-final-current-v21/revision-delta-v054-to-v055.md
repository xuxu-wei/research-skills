---
schema_version: research-idea-revision-delta.v1
plugin_version: 0.9.0-preview.3
artifact_id: revision-delta-I01-001-v054-to-v055
workflow_id: RID-SEPSIS-CSM-20260717-001
idea_id: I01-001
version_id: v054-to-v055
source_artifact:
  artifact_id: idea-dossier-I01-001-v054
  version: v054
  path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v20/idea-dossier-v054.md
target_artifact:
  artifact_id: idea-dossier-I01-001-v055
  version: v055
  path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v21/idea-dossier-v055.md
compliance_input:
  artifact_id: writer-action-compliance-I01-001-r123
  version: r123
  path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v20/writer-action-compliance-r123.md
protected_content_register:
  artifact_id: protected-content-register-I01-001-v054-v006
  version: v006
  path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v20/protected-content-register-v006.yaml
change_type: editorial_repair_delta
scientific_change_declared: false
frozen: true
---

# Revision delta: v054 → v055

## Bounded compliance correction

This version closes the determinate F-01 execution failure and its nearby terminology regression. It changes the subsection heading and its three direct references from `试验观察映射和独立分析` to the already approved `试验观测映射和独立分析`. It does not address any separate language finding and makes no other scientific or editorial change.

| Occurrence | v055 locator | Executed correction | Compliance result |
|---|---|---|---|
| 1 | Research design and methods > heading at line 282 | `试验观察映射和独立分析` → `试验观测映射和独立分析` | The technical authority now uses the approved term. |
| 2 | Required analyses and evidence at line 380 | Direct subsection reference changed to `试验观测映射和独立分析` | The reference resolves to the corrected heading. |
| 3 | Contribution and evidence ladder > 从属的试验访视结局证据 > 必需证据 at line 428 | Direct subsection reference changed to `试验观测映射和独立分析` | F-01 now uses the approved locatable term while retaining all six evidence roles. |
| 4 | Title and positioning claim-support table > subordinate trial-analysis row at line 449 | Direct subsection reference changed to `试验观测映射和独立分析` | Claim audit and technical authority now use the same term. |

The source-to-target dossier diff contains only version/provenance frontmatter changes and these four one-character terminology corrections. Formulas, thresholds, eligibility branches, trial-specific processing, assumptions, limitations, milestones, identity anchors, evidence status and claim strength are unchanged.

## Protected-content preservation receipt

| Protected ID | v055 locator(s) | Preservation evidence |
|---|---|---|
| PCR-001 | frontmatter > identity_anchor | All five protected values remain verbatim; only artifact version, path, provenance and round changed. |
| PCR-002 | Primary research question；Objectives | Full-course question, four objectives, subordinate trial extension and paper/evidence deliverable remain unchanged. |
| PCR-003 | Core hypothesis and evidence boundary | Support conditions, recoverable invariants, untouched external stability and noncausal estimand boundary remain unchanged. |
| PCR-004 | Observational target, anchoring, and evidence-qualified interpretation | Sepsis-centered longitudinal object and patient-time state/transition inference unit remain unchanged. |
| PCR-005 | Protocol locks for the two primary clinical tasks | Both task populations, clocks, landmarks, estimands, metrics and clustered uncertainty remain unchanged. |
| PCR-006 | Mutually exclusive post-onset state and event system | Twelve-hour assignment, fixed state priority and all state/event definitions remain unchanged. |
| PCR-007 | Variable roles | Y, A, M, label-only and B roles and their separation remain unchanged. |
| PCR-008 | Public intensive-care database roles and support audit | MIMIC-IV, eICU and prespecified backup roles remain unchanged. |
| PCR-009 | Public intensive-care database roles and support audit > audit table | All access, cohort, event, hospital, anchor, interface, missingness and support audit fields remain unchanged. |
| PCR-010 | Current resource and result status | Verified database existence/version and all unverified access, support, staffing and result states remain unchanged. |
| PCR-011 | Local randomized-trial evidence status | EXIT-SEP/XBJ-SCAP derivative-report facts and original-evidence limitations remain unchanged. |
| PCR-012 | Current resource and result status > trial rows | Authorization, original documents and core trial semantics remain explicitly unverified. |
| PCR-013 | Feasibility and resources | Six required team functions, absent commitments/hours and bounded model scope remain unchanged. |
| PCR-014 | Work packages and minimum route | Fixed precedence, simpler alternatives and prohibition on bypass by trial results remain unchanged. |
| PCR-015 | Conjunctive minimum success definition | All five stage-II conjunctive criteria, thresholds and non-compensation rules remain unchanged. |
| PCR-016 | Protocol locks > primary pre-onset task | Twelve-hour first-onset cumulative-incidence task, population, timing, metrics and pass conditions remain unchanged. |
| PCR-017 | Protocol locks > primary post-onset task | Day-7 favorable-state occupancy task, components, multistate method, metrics and uncertainty remain unchanged. |
| PCR-018 | Protocol locks > event and information-availability clocks | Infection pairing, SOFA baseline/window and event-versus-availability timing remain unchanged. |
| PCR-019 | Mutually exclusive post-onset state system > definitions | Recovery, deterioration, ICU exit, transfer/loss and death definitions remain unchanged. |
| PCR-020 | Observational target and anchoring | Anchor counts, loading/scale rules, complexity limits, seeds and recoverable invariants remain unchanged. |
| PCR-021 | Observational target > missingness and action support | Measurement-process model, shift values, tipping points and action-support thresholds remain unchanged. |
| PCR-022 | Absolute simulation > regimen | Months 7–10, repeat/Monte Carlo precision rule and full generator/misspecification set remain unchanged. |
| PCR-023 | Absolute simulation > continuous branch | Canonical-correlation object, failure-to-zero rules, confidence-bound formula, 0.80 criterion and confirmation remain unchanged. |
| PCR-024 | Absolute simulation > recovery table | Discrete recovery, transition, edge, zero-edge, misspecification and calibration standards remain unchanged. |
| PCR-025 | Hospital-primary validation > partition and cross-hospital rules | Seed 20260717, 30%/70% hospital split, linked-patient handling and support triggers remain unchanged. |
| PCR-026 | Hospital-primary validation > four update operations | No-update, calibration-only, observation-layer-only and full-refit order and evidence roles remain unchanged. |
| PCR-027 | 试验观测映射和独立分析 > shared prerequisites | Stage-II success, data authorization and core-semantics prerequisites remain unchanged; only the heading term was corrected. |
| PCR-028 | 试验观测映射和独立分析 > mapping eligibility and fidelity | Anchor eligibility, SVD mapping, fidelity thresholds, blinded-trial coverage and failure rule remain unchanged. |
| PCR-029 | 试验观测映射和独立分析 > stratified standardized probability index | Outcome ordering, unique estimand, formula, tie handling, weights, direction and separate-trial estimates remain unchanged. |
| PCR-030 | 试验观测映射和独立分析 > fallback and stop branches | Independent SOFA fallback, core-semantics stop and owner-confirmation consequence remain unchanged. |
| PCR-031 | 试验观测映射和独立分析 > trial table | Trial-specific populations, visits, missing-data handling, multiplicity and stop rules remain unchanged. |
| PCR-032 | Secondary representation diagnostics | Pseudo-mask and future-trajectory diagnostics, metrics, strata and non-promotion role remain unchanged. |
| PCR-033 | Required analyses and evidence；试验观测映射和独立分析 | All stage-II requirements and compact trial authorization/semantics/eligibility/fixed-method requirement remain unchanged apart from the corrected reference. |
| PCR-034 | Falsification and stop criteria > clocks, leakage and data support | Leakage and insufficient-support triggers and their original consequences remain unchanged. |
| PCR-035 | Falsification and stop criteria > recovery, missingness, action support and external result | Non-promotion, sensitivity qualification and no-update failure consequences remain unchanged. |
| PCR-036 | 试验观测映射和独立分析；Falsification > trial mapping/core semantics | Full eligibility criteria, mapping-specific block, independent SOFA fallback and all-new-outcomes stop remain unchanged. |
| PCR-037 | Falsification and stop criteria > time | Month-12, month-20 and month-24 triggers and consequences remain unchanged. |
| PCR-038 | Risks, alternatives, and stop conditions | All object-specific triggers, responses and consequences remain unchanged. |
| PCR-039 | Title/summary/positioning；Structured abstract | Candidate/planned status, pending outputs and subordinate trial role remain unchanged. |
| PCR-040 | Contribution and evidence ladder | Four evidence levels and their claim-strength functions remain unchanged; only the method-subsection reference was corrected. |
| PCR-041 | Verified representative closest-work comparison | Component precedents, conditional differences and low-to-moderate combination-gap confidence remain unchanged. |
| PCR-042 | Interpretation matrix | All permitted and prohibited interpretations for seven result patterns remain unchanged. |
| PCR-043 | 试验观测映射和独立分析；trial evidence chain | Separate secondary trial results/no-analysis record, non-compensation and non-pooling boundaries remain unchanged. |
| PCR-044 | Working assumptions > continuous latent-state recovery | Unique definition, owners, deadline and false/unconfirmed consequences remain unchanged. |
| PCR-045 | Working assumptions > trial probability index | Unique probability index, ties, target set/strata/weights, owner, deadline and stop consequence remain unchanged. |
| PCR-046 | Working assumptions > clinical-scale-to-simulation mapping | Month-7 information restriction and unresolved-specification consequence remain unchanged. |
| PCR-047 | Working assumptions > multicategory calibration | Month-6 information restriction, fixed metrics/thresholds and unresolved-specification consequence remain unchanged. |
| PCR-048 | Limitations > 1 | Resources, access, team and unaudited project support remain once at the authority location. |
| PCR-049 | Limitations > 2 | Labels, clocks and leakage limitation remains once at the authority location. |
| PCR-050 | Limitations > 3 | Recoverability and structural-scope limitation remains once at the authority location. |
| PCR-051 | Limitations > 4 | Nonrandom-missingness and low-action-overlap limitation remains once at the authority location. |
| PCR-052 | Limitations > 5 | Cross-database and no-update-versus-adaptation limitation remains once at the authority location. |
| PCR-053 | Limitations > 6 | Twenty-four-month boundary and stage-III non-repair rule remain once at the authority location. |
| PCR-054 | Limitations > 7 | Conditional trial data, unverified semantics and no pseudo-continuous/pooled-effect limitation remain once at the authority location. |
| PCR-055 | Limitations > 8 | Candidate anchors, unverified units/fidelity and mapping-versus-independent-SOFA scope remain once at the authority location. |
| PCR-056 | Limitations > 9 | Non-systematic closest-work search and low-to-moderate gap confidence remain once at the authority location. |
| PCR-057 | Limitations > 10 | Regulatory-applicability and no-unconditional-promotion limitation remains once at the authority location. |
| PCR-058 | Limitations > 11 | Complete causal, mechanism, control, digital-twin, validation and promotion prohibitions remain once at the authority location. |
| PCR-059 | 24 个月最低交付与时间节点 | Role-signature meaning, test-data isolation and post-month-20 freeze boundary remain unchanged. |
| PCR-060 | Working assumptions > closing qualification | Screening-rule status, resolution timing and no-invented-number boundary remain unchanged. |
| PCR-061 | Limitations > 11 | Real causal network, treatment effect, counterfactual policy, mechanism, mediation, control and digital twin remain unsupported. |
| PCR-062 | Limitations > 11；Contribution and evidence ladder | Validated-model, decision-tool, drug-platform, effectiveness and unconditional-promotion claims remain unsupported. |
| PCR-063 | Verified representative closest-work comparison | New-algorithm/global-first/absence/patent-absence claims remain unsupported; stronger-search requirements remain unchanged. |
| PCR-064 | 试验观测映射和独立分析；Interpretation matrix | No latent-dynamics/edge/whole-system validation, pooled effect/common mechanism or subgroup repair remains unchanged. |

## Identity-anchor comparison

| Field | v054 and v055 value | Result |
|---|---|---|
| primary_research_question | `can a knowledge-constrained, uncertainty-aware dynamic system representation of ICU patients cover the sepsis-centered pre-onset, onset, post-onset, and outcome continuum, demonstrate cross-database state/structure validity, and then test limited randomized intervention perturbations without conflating prediction with causality?` | identical |
| primary_objective | `construct and validate the sepsis complex-system model, with stage II completed within 24 months.` | identical |
| study_object | `the longitudinal sepsis-centered ICU patient system, including comparable at-risk non-onset intervals and post-onset trajectories.` | identical |
| core_data_or_evidence_base | `literature/expert priors; longitudinal public ICU data; conditionally available EXIT-SEP and XBJ-SCAP individual-level RCT data.` | identical |
| primary_unit_of_inference | `patient-time state and state transition, with patient and hospital clustering respected.` | identical |

Result: 5/5 identity-anchor fields are verbatim matches.

## Deterministic check receipts

The following commands were executed after the v055 dossier text was final:

1. `python research-skills-openai/skills/multi-path-idea-generator/scripts/lint_idea_dossier.py tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v21/idea-dossier-v055.md --expected-plugin-version 0.9.0-preview.3`

   Exit code 0; the linter reported `OK` for v055. It emitted advisory implementation-vocabulary candidates, which are not errors and were not modified in this bounded correction.

2. `python research-skills-openai/skills/academic-language-assessor/scripts/diff_reader_facing_short_forms.py tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v20/idea-dossier-v054.md tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/direct-final-current-v21/idea-dossier-v055.md`

   Exit code 0; it emitted one candidate: `quoted-label  试验观测映射和独立分析` at lines 282, 380, 428 and 449.

| Candidate occurrence | Permitted disposition | Text-grounded reason |
|---|---|---|
| line 282 | `fixed_scaffolding` | This is the approved subsection heading, not a newly coined scientific construct. |
| line 380 | `fixed_scaffolding` | This is a direct reference to the approved subsection heading. |
| line 428 | `fixed_scaffolding` | This is F-01's direct, locatable reference to the approved subsection heading. |
| line 449 | `fixed_scaffolding` | This is a claim-audit reference to the same approved subsection heading. |

No `试验观察映射和独立分析` occurrence remains. The candidate is internally consistent at all four locations and introduces no unresolved terminology problem.

## Closure

The bounded F-01 compliance failure and adjacent `观察映射`/`观测映射` regression are closed in v055. The exact linter and short-form diff commands pass, the receipts report the commands and candidate dispositions faithfully, all 64 protected items remain, and 5/5 identity anchors match. No separate nonblocking language finding was changed.
