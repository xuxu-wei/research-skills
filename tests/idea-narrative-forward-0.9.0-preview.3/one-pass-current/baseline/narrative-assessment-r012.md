---
schema_version: research-idea-narrative-assessment.v1
assessment_id: narrative-assessment-I01-001-r012
review_id: narrative-review-I01-001-r012
reviewer_skill: idea-narrative-assessor
reviewer_instance_id: idea-narrative-assessor-forward-r012
workflow_id: RID-SEPSIS-CSM-20260717-001
round_id: r012
input_artifact_ids:
  - idea-dossier-I01-001-v003
  - reader-handoff-forward-001
input_versions:
  - v003
  - v001
input_dossier:
  artifact_id: idea-dossier-I01-001-v003
  version: v003
  path: tests/idea-test-0.9.0-preview.1/0.9.0-preview.1/03_ideas/nodes/I01-001/dossiers/idea-dossier-v003.md
reader_handoff:
  artifact_id: reader-handoff-forward-001
  version: v001
  path: tests/idea-narrative-forward-0.9.0-preview.3/run-001/inputs/reader-handoff.yaml
files_read:
  - tests/idea-test-0.9.0-preview.1/0.9.0-preview.1/03_ideas/nodes/I01-001/dossiers/idea-dossier-v003.md
  - tests/idea-narrative-forward-0.9.0-preview.3/run-001/inputs/reader-handoff.yaml
isolation_mode: fresh_subagent
prior_scores_visible: false
forbidden_project_artifacts_read: false
source_edits_performed: false
decision: major_narrative_revision
findings:
  - finding_id: NAR-001
    severity: major
    category: reader_reasoning_chain
    dossier_locator:
      section_heading: "Background, current state, gap, significance, and rationale"
      subsection_heading: null
      content_anchor: "The five paragraphs beginning with ‘脓毒症随时间形成’ and ending with the EXIT-SEP/XBJ-SCAP paragraph"
    observed_evidence: "The section supplies background, prior work, a defensible integration gap, several inferential boundaries, and a later RCT design justification, but it does not give significance its own explicit reader-facing function and does not close the main integration gap with one concise bridge to the staged design."
    current_reader_effect: "Readers can infer why the project may matter and why several safeguards are proposed, but must assemble those links themselves before reaching the research question and extensive protocol detail."
    target_function: "Present an explicit five-part route from problem through current knowledge, unresolved gap, significance, and design rationale, with each function distinct and the rationale tied directly to the stated gap."
  - finding_id: NAR-002
    severity: major
    category: progressive_disclosure
    dossier_locator:
      section_heading: "Title, summary, audience, and positioning"
      subsection_heading: null
      content_anchor: "The one-sentence complete-Idea summary beginning ‘本研究计划在 24 个月内’"
    observed_evidence: "The opening summary and the following structured abstract introduce a dense sequence of specialized constructs and branch conditions, including absolute recovery gates, untouched cross-database testing, frozen observation projection, projected observable-state summaries, and death-ranked SOFA, before the dossier has established or defined them for all declared disciplines."
    current_reader_effect: "The multidisciplinary reader encounters the full validation machinery before obtaining a stable account of the question, importance, and staged response, increasing concept burden and encouraging rereading."
    target_function: "Lead with the research question, importance, evidence gap, and high-level staged response; introduce specialized constructs only when their role is needed and define each cross-disciplinary core term at first use."
  - finding_id: NAR-003
    severity: major
    category: limitations_location_and_repetition
    dossier_locator:
      section_heading: "Feasibility, resources, risks, alternatives, and stop conditions"
      subsection_heading: "Remaining execution gates"
      content_anchor: "The paragraph beginning ‘仍未解决且必须显式保留’ together with limitation statements repeated throughout earlier sections"
    observed_evidence: "A plausible authoritative limitations location exists, but access, ungenerated evidence, causal boundaries, transport failure, RCT projection failure, and prohibited interpretations are restated in the summary, abstract, background, hypotheses, work packages, data tables, methods, evidence chains, required analyses, expected outputs, contribution tables, and risk matrix."
    current_reader_effect: "Repeated cautions displace the positive argument, obscure which statement is authoritative, and force readers to distinguish genuine local design boundaries from duplicated global limitations."
    target_function: "Maintain one complete authoritative limitations location, while retaining elsewhere only a concise boundary that is indispensable to understanding the immediately connected design choice."
  - finding_id: NAR-004
    severity: major
    category: repetition_and_navigation
    dossier_locator:
      section_heading: "Evidence chains"
      subsection_heading: null
      content_anchor: "The five ‘Evidence chain’ subsections, read against Work packages, Required analyses, Planned outputs, the evidence ladder, and the claim-support table"
    observed_evidence: "The same staged route, gates, outputs, fallback branches, and interpretation boundaries are repeatedly narrated across several mandatory sections, often at similar levels of detail rather than with a section-specific function."
    current_reader_effect: "The dossier’s auditable structure is preserved, but the reader repeatedly traverses the same plan and loses the distinction among design specification, evidence traceability, acceptance criteria, planned deliverables, and contribution interpretation."
    target_function: "Keep every required section and reader-auditable function, but make each occurrence perform only its promised function and refer to the authoritative detailed specification instead of restating it."
unresolved_issues: []
---

# Narrative assessment

## Overall judgment

The dossier contains a coherent research object, a stable primary question, a conservative contribution frame, and a staged design that can be followed with sustained close reading. It is not yet narratively ready for the stated multidisciplinary audience. The opening compresses the full technical and conditional architecture before establishing a simple reader route; the central background section leaves significance and the main gap-to-design connection implicit; and later sections repeatedly restate both the plan and its limitations. These are structural reader-navigation problems rather than judgments about scientific merit, and they require revision across the main route rather than isolated copyediting.

## Findings

### NAR-001 — The five-step reasoning chain is not explicit

The background section establishes the clinical problem, describes available databases and neighboring research, and identifies a defensible integration gap. It then shifts into inferential cautions and a detailed justification for the conditional RCT layer. What is missing is a distinct statement of why resolving the integration and validation gap matters to the declared research communities, followed by one direct bridge explaining why the staged design is the appropriate response. The current content should be reorganized, not scientifically expanded by the editor.

### NAR-002 — Technical machinery arrives before the reader-facing core

The title is appropriately qualified, but the one-sentence summary asks readers to process most of the study architecture and its fallback logic at once. The structured abstract continues with technical gates and branch labels before several constructs have been introduced in shared language. This is particularly burdensome for readers who are expert in one participating discipline but not all of them. The opening should first establish the question, importance, gap, contribution, and broad sequence; detailed gate terminology should appear where the corresponding design is explained.

### NAR-003 — Limitations do not have one authoritative home

The dossier repeatedly states access limitations, absent results, inferential prohibitions, transport boundaries, RCT projection failure conditions, and prohibited claims. Some local qualifications are essential—for example, a causal boundary adjacent to the observational estimand or the meaning of an RCT fallback adjacent to that branch. Many other repetitions do not advance the local reasoning. The complete limitation set should be maintained in the existing `Remaining execution gates` location, with other sections retaining only the minimum boundary needed to interpret the design choice at hand.

### NAR-004 — Required functions are obscured by repeated specification

Work packages, methods, evidence chains, required analyses, planned outputs, the evidence ladder, and the claim-support table are all legitimate and should remain. Their present overlap, however, makes several sections function as parallel summaries of the entire project. Revision should preserve their distinct contracts: work packages describe sequence and ownership; methods specify implementation; evidence chains trace input to supported claim; required analyses define acceptance evidence; outputs name deliverables; and contribution sections interpret the resulting value.

## Preserved strengths

The revision should preserve the qualified title, the complete primary research question, the four objectives, the separation of observational prediction from causal interpretation, the stage II/stage III boundary, the two primary clinical tasks, the hospital-prioritized external-test design, the conditional trial projection and independent fallback, the evidence chains, all stop rules, and the conservative closest-work positioning. It should also preserve all required dossier sections and the distinct scientific content currently carried by their tables.

## Handoff

See the paired `narrative-repair-plan-r012.yaml` for executable actions.
