---
schema_version: research-idea-revision-delta.v1
artifact_id: revision-delta-I01-001-v009-to-v010
workflow_id: RID-SEPSIS-CSM-20260717-001
idea_id: I01-001
version_id: v009-to-v010
path: tests/idea-narrative-forward-0.9.0-preview.3/run-001/release/revision-delta-v009-to-v010.md
from_dossier_ref:
  artifact_id: idea-dossier-I01-001-v009
  version: v009
  path: tests/idea-narrative-forward-0.9.0-preview.3/run-001/release/idea-dossier-v009.md
to_dossier_ref:
  artifact_id: idea-dossier-I01-001-v010
  version: v010
  path: tests/idea-narrative-forward-0.9.0-preview.3/run-001/release/idea-dossier-v010.md
based_on:
  - artifact_id: idea-dossier-I01-001-v009
    version: v009
    path: tests/idea-narrative-forward-0.9.0-preview.3/run-001/release/idea-dossier-v009.md
  - artifact_id: narrative-repair-plan-I01-001-r008
    version: r008
    path: tests/idea-narrative-forward-0.9.0-preview.3/run-001/release/narrative-repair-plan-r008.yaml
  - artifact_id: language-assessment-I01-001-r008
    version: r008
    path: tests/idea-narrative-forward-0.9.0-preview.3/run-001/release/language-assessment-r008.md
  - artifact_id: protected-content-register-I01-001-v009
    version: v009
    path: tests/idea-narrative-forward-0.9.0-preview.3/run-001/release/protected-content-register-v009.yaml
source_skill: multi-path-idea-generator
created_round: 7
change_type: editorial_repair_delta
---

# Revision delta: idea dossier v009 to v010

## Scope and outcome

This revision is a single concentrated editorial repair. It changes organization, sentence structure, first-use definitions, terminology precision, and local redundancy only. It does not change the research identity, research object, question, objectives, scope, unit of inference, data roles, design, analyses, measurements, validation commitments, thresholds, claim strength, evidence status, limitations, alternatives, contingencies, or stop conditions. It adds no data, method, result, citation, or external evidence and does not present planned work as completed.

The project inputs used were exactly the four logical references listed in frontmatter. No external terminology search was used. Two locally ambiguous terms were completed under explicit working assumptions because each has a feasible confirmation path and would require only a bounded wording correction if the assumption is false; both assumptions appear once, in section 14.

## Narrative repair mapping

| Action | Finding | Status | Concrete v010 edit location | Editorial disposition |
|---|---|---|---|---|
| NRP-001 | NAR-001 | implemented | Section 1, after the interdisciplinary concept bridge and the paragraph distinguishing four evidence types | Moved the three-stage navigation below the complete-Idea summary, audience, positioning, concept bridge, and evidence distinctions. All stage timing, overlap, and conditionality remain locatable. |
| NRP-002 | NAR-001 | implemented | Section 1, “三阶段导航”; section 5, “Twenty-four-month minimum deliverable and dated milestones,” “Minimum success definition: all required evidence,” and “Work packages and minimum route” | Reduced the opening navigation to three stage-level bullets. Removed opening WP labels, the repeated five-item success list, and prematurely introduced technical labels; retained the full executable schedule, WP mapping, five necessary evidence classes, and failure consequences in section 5. |

Narrative finding status: 1 of 1 finding addressed through 2 of 2 required actions.

## Language finding mapping

| Finding | Status | Concrete v010 edit location | Editorial disposition |
|---|---|---|---|
| LANG-R008-001 | implemented | Section 1, “三阶段导航” | Replaced the single nested stage sentence with three parallel stage bullets and one concise conditional boundary. |
| LANG-R008-002 | implemented | Section 2, “Background and gap” | Split the core gap into a total question, the recovery objects, their definitions, and the external validation objects; citations and scientific content were retained. |
| LANG-R008-003 | implemented | Section 4, “Primary research question” | Recast the three dependent questions as a numbered, parallel sequence without changing their order or content. |
| LANG-R008-004 | implemented | Section 2, “Background and gap”; consistent later use in section 7, “Observational model target, anchoring, and reporting” | Defined “预设结构稳定性” at first use as the cross-database preservation of the signs and time lags of prespecified relationships. |
| LANG-R008-005 | implemented under an explicit working assumption | Section 7, “Hospital-based cross-database validation”; section 14, “工作假设” | Replaced the indeterminate hospital-volume label with “每院合格患者数四分位.” Recorded once in section 14 that this definition must be confirmed before validation outcomes are viewed; if corrected, the same prespecified allocation process is rerun without changing the 30%/70% split or isolation rules. |
| LANG-R008-006 | implemented | Section 6, “Trial data considered for conditional stage III analyses”; section 7, “Analysis targets” table | Replaced the mixed-language label with “符合预先规定操作定义的脓毒症样人群” and stated the defining condition as full-analysis-set membership with baseline SOFA at least 2. |
| LANG-R008-007 | implemented under an explicit working assumption | Section 14, “工作假设” and “Operational thresholds, alternatives, and stop conditions,” row “两项主要临床任务” | Resolved the interval-type ambiguity as the upper limit of a two-sided 95% confidence interval. Recorded once that the interval construction must be confirmed at freezing; the +0.01 threshold and decision direction are unchanged. |
| LANG-R008-008 | implemented | Section 1, stage III bullet; section 14, “Scientific and interpretive boundaries,” item 7 | Shortened the local navigation boundary to the independent stage II decision while retaining the complete authoritative limitation in section 14. |

Language finding status: 8 of 8 findings addressed.

## Additional required editorial normalization

- Updated the v010 dossier binding to the v010 artifact, version, and path; set round 7 and change type to editorial repair.
- Limited the v010 dossier’s `based_on` list to the four authorized logical inputs.
- Restated hospital allocation as a reproducible split based on hospital identifiers and fixed seed 20260717, without changing the allocation rule, proportions, freezing point, or cross-hospital patient handling.
- Retained all 15 required H2 sections, all five ordered section-3 H3 functions, all five evidence chains, and the title/positioning claim-support table.
- Kept section 14 as the only complete authority for limitations, working assumptions, risks, alternatives, contingencies, and stop conditions.

## Protected-content disposition

| Protected item | Disposition in v010 | Principal v010 location |
|---|---|---|
| PCR-001 | retained with the same meaning | Frontmatter identity anchor; section 4 |
| PCR-002 | retained with the same meaning; split into parallel questions | Section 4, “Primary research question” |
| PCR-003 | retained with the same meaning | Section 4, “Objectives” and “Core hypothesis” |
| PCR-004 | retained with the same meaning | Section 4; section 7, primary-task protocol locks |
| PCR-005 | retained with the same meaning; opening navigation shortened, executable detail unchanged | Section 1, “三阶段导航”; section 5 |
| PCR-006 | retained with the same meaning | Section 14, “Resources and governance” |
| PCR-007 | retained with the same meaning | Section 7, conditional trial analyses and analysis targets |
| PCR-008 | retained with the same meaning | Section 6, public ICU databases and planned roles |
| PCR-009 | retained with the same meaning; subgroup label defined in standard Chinese | Section 6, conditional stage III trial data |
| PCR-010 | retained with the same meaning and status | Section 14, “Current feasibility and evidence status” |
| PCR-011 | retained with the same meaning and status | Section 14, current feasibility and resources |
| PCR-012 | retained with the same meaning | Section 7, protocol locks and sensitivity definitions |
| PCR-013 | retained with the same meaning | Section 7, primary pre-onset task |
| PCR-014 | retained with the same meaning | Section 7, primary post-onset task and mutually exclusive states |
| PCR-015 | retained with the same meaning | Section 6, variable-role separation; section 7, leakage audit |
| PCR-016 | retained with the same meaning | Section 7, observational model target, anchoring, and reporting |
| PCR-017 | retained with the same meaning | Section 7, missingness and treatment paragraph |
| PCR-018 | retained with the same meaning | Section 7, simulation and semi-synthetic recovery study |
| PCR-019 | all numerical gates retained unchanged | Section 14, operational thresholds |
| PCR-020 | decision direction and +0.01, calibration, overlap, and nonreplacement gates retained; interval label clarified under a working assumption | Section 14, working assumptions and operational thresholds |
| PCR-021 | split, proportions, fixed seed, freezing, exclusions, reporting, and sensitivity analysis retained; hospital-volume label clarified under a working assumption | Section 7, hospital-based cross-database validation |
| PCR-022 | retained with the same meaning and sequence | Section 7, three external analyses |
| PCR-023 | all external support, result, and timing gates retained unchanged | Section 14, operational thresholds |
| PCR-024 | retained with the same meaning | Section 7, trial semantics and common-observation eligibility |
| PCR-025 | retained with the same meaning | Section 7, prespecified deterministic observation mapping |
| PCR-026 | all mapping-fidelity thresholds and stop consequence retained unchanged | Section 14, operational thresholds |
| PCR-027 | retained with the same meaning | Section 7, analysis targets and trial table |
| PCR-028 | retained with the same meaning and strength | Section 5, minimum success definition; section 11, falsification criteria |
| PCR-029 | retained with the same strength | Sections 1 and 12 |
| PCR-030 | retained with the same planned-status language | Sections 2 and 11 |
| PCR-031 | retained with the same evidence strength and qualification | Section 12; section 13 |
| PCR-032 | retained with the same strength and separation of evidence types | Section 11; section 14, interpretive boundaries |
| PCR-033 | retained once at the authoritative location where applicable; core hypothesis conditionality unchanged | Section 4, core hypothesis; section 14 |
| PCR-034 | retained in full at the authoritative limitation location | Section 14, scientific and interpretive boundaries |
| PCR-035 | retained in full at the authoritative alternatives and stop-condition location | Section 14, operational thresholds |
| PCR-036 | retained in full at the authoritative trial alternatives and stop-condition location | Section 14, operational thresholds |
| PCR-037 | retained with the same unsupported-claim boundary | Section 14, scientific and interpretive boundaries |
| PCR-038 | retained with the same unsupported-claim boundary | Section 14, scientific and interpretive boundaries and closest-work row |
| PCR-039 | retained with the same unsupported-claim boundary | Section 14, scientific and interpretive boundaries and trial rows |

Protected-content status: 39 of 39 protected items retained with their required meaning, strength, conditionality, authority location, or unsupported-claim boundary.

## Unimplemented items and verification

- Unimplemented narrative actions: none.
- Unimplemented language findings: none.
- Unresolved protected-content dispositions: none.
- Structural lint: passed with exit code 0 using the Skill-bundled dossier linter.
- Remaining editorial warnings: none.
