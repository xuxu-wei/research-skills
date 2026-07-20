---
schema_version: research-idea-narrative-assessment.v1
assessment_id: narrative-assessment-I01-001-r011
review_id: narrative-assessment-I01-001-r011
reviewer_skill: idea-narrative-assessor
reviewer_instance_id: idea-narrative-assessor-forward-r011
workflow_id: RID-SEPSIS-CSM-20260717-001
round_id: r011
input_artifact_ids:
  - idea-dossier-I01-001-v004
  - reader-handoff-forward-001
input_versions:
  - v004
  - v001
input_dossier:
  artifact_id: idea-dossier-I01-001-v004
  version: v004
  path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass/revised/idea-dossier-v004.md
reader_handoff:
  artifact_id: reader-handoff-forward-001
  version: v001
  path: tests/idea-narrative-forward-0.9.0-preview.3/run-001/inputs/reader-handoff.yaml
files_read:
  - tests/idea-narrative-forward-0.9.0-preview.3/one-pass/revised/idea-dossier-v004.md
  - tests/idea-narrative-forward-0.9.0-preview.3/run-001/inputs/reader-handoff.yaml
isolation_mode: fresh_subagent
prior_scores_visible: false
forbidden_project_artifacts_read: false
source_edits_performed: false
decision: major_narrative_revision
findings:
  - finding_id: NAR-001
    severity: major
    category: progressive_disclosure_and_concept_burden
    dossier_locator:
      section_heading: "Title, summary, audience, and positioning / Structured abstract"
      subsection_heading: null
      content_anchor: "One-sentence complete-Idea summary and the Objective and hypothesis and Approach bullets"
    observed_evidence: "The opening route introduces a knowledge-constrained, uncertainty-aware dynamic system representation, audit gate G1, recovery of invariants, zero-update external validation, state alignment, observation-model updating, and a trial observation mapping before giving the multidisciplinary reader a short plain-language account of what is represented, what the two primary tasks test, and why the ordered design answers the gap. Several of these concepts are explained only in later methods sections."
    current_reader_effect: "Readers who may know validation and longitudinal clinical data but not every participating discipline must retain multiple undefined dependencies or search forward before they can interpret the central proposal. The background-gap-significance-rationale chain is present later, but the abstract reaches technical contingencies before that chain has established a stable route through the study."
    target_function: "The title, summary, and structured abstract should first establish the study object, unresolved gap, two primary clinical tasks, ordered validation logic, and conditional contribution in language shared across the declared disciplines; specialized constructs and thresholds should follow after their purpose is clear and be defined at first necessary use."
  - finding_id: NAR-002
    severity: major
    category: core_element_priority_and_repetition
    dossier_locator:
      section_heading: "Title, summary, audience, and positioning through Expected outputs, falsification criteria, and interpretations"
      subsection_heading: null
      content_anchor: "Repeated stage III trial-observation mapping and independent SOFA alternative branch"
    observed_evidence: "The post-24-month, conditional stage III trial branch appears in the title, complete-Idea summary, positioning, three abstract bullets, rationale, primary research question, an objective, dated gates, a work package, local evidence, a long methods subsection, an evidence chain, required analyses, planned outputs, falsification criteria, interpretation matrices, contribution ladder, closest-work comparison, and claim-support table. Many occurrences restate the same eligibility, mapping-failure, and independent-SOFA boundary rather than performing a new local function."
    current_reader_effect: "A downstream extension that explicitly does not contribute to stage II success competes with the 24-month stage I–II study for narrative weight. Readers can reasonably mistake the dossier for two co-primary studies and must repeatedly leave the principal route of audit, recovery, clinical-task evaluation, and zero-update external validation to revisit the same conditional branch."
    target_function: "Keep stage I–II as the unambiguous main study route, introduce stage III once as a bounded downstream extension, retain its full specification in one authoritative methods location and the limitations location, and reduce every other occurrence to the minimum statement needed for that section's distinct function."
unresolved_issues: []
---

# Narrative assessment

## Overall judgment

The dossier contains a complete and logically defensible reader-reasoning chain: it establishes the time-varying sepsis problem, summarizes relevant existing approaches, identifies the unresolved question of whether one bounded representation can earn several distinct kinds of support, explains why separating those support levels matters, and links the gap to an ordered design. The decision is nevertheless `major_narrative_revision` because the reader reaches that chain only after a technically saturated opening, and because the conditional trial extension repeatedly interrupts the primary stage I–II route. Repair therefore requires redistribution and consolidation across several sections rather than a localized wording change.

## Findings

### NAR-001 — The opening asks readers to decode the design before it establishes a common conceptual route

The early summary and abstract name many valid design safeguards, but their sequence assumes detailed familiarity with constructs that the reader handoff explicitly does not permit the dossier to assume across all participating disciplines. Later sections explain the study object, task structure, audit, recovery testing, external isolation, and observation mapping in sufficient detail. The problem is disclosure order: the reader must understand several later explanations retrospectively to interpret the opening. The opening should lead with the scientific question and the purpose of each design stage, then introduce specialized constructs when they become necessary.

### NAR-002 — The conditional trial extension displaces the main study route

Stage III is carefully bounded in scientific terms, but its narrative footprint is disproportionate to its stated role after the 24-month minimum and after successful stage II completion. Repeated accounts of its eligibility checks, observation mapping, failure branch, and SOFA alternative obscure the central progression from data support to recovery, clinical-task evaluation, and independent external validation. The full trial specification should remain available and auditable, but repeated versions should be consolidated so each required section performs only its own distinct function.

## Preserved strengths

The five functions under “Background, current state, gap, significance, and rationale” are present, distinct, and connected. The dossier consistently distinguishes prediction, recoverability, transportability, and causal interpretation; gives the two primary tasks explicit roles; separates zero-update validation from adaptation; preserves evidence-chain traceability; and supplies one declared authoritative limitations location. These functions and boundaries should remain intact during repair.

## Handoff

See the paired `narrative-repair-plan-r011.yaml` for executable actions.
