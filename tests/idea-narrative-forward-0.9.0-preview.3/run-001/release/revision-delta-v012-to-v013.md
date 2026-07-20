---
schema_version: research-idea-revision-delta.v1
plugin_version: 0.9.0-preview.3
artifact_id: revision-delta-I01-001-v012-to-v013
workflow_id: RID-SEPSIS-CSM-20260717-001
idea_id: I01-001
version_id: v012-to-v013
path: tests/idea-narrative-forward-0.9.0-preview.3/run-001/release/revision-delta-v012-to-v013.md
source_skill: multi-path-idea-generator
created_round: 10
change_type: editorial_repair_delta
from_dossier:
  artifact_id: idea-dossier-I01-001-v012
  version: v012
  path: tests/idea-narrative-forward-0.9.0-preview.3/run-001/release/idea-dossier-v012.md
to_dossier:
  artifact_id: idea-dossier-I01-001-v013
  version: v013
  path: tests/idea-narrative-forward-0.9.0-preview.3/run-001/release/idea-dossier-v013.md
repair_inputs:
  - artifact_id: narrative-repair-plan-I01-001-r011
    version: r011
    path: tests/idea-narrative-forward-0.9.0-preview.3/run-001/release/narrative-repair-plan-r011.yaml
  - artifact_id: language-assessment-I01-001-r012
    version: r012
    path: tests/idea-narrative-forward-0.9.0-preview.3/run-001/release/language-assessment-r012.md
  - artifact_id: protected-content-register-I01-001-v012
    version: v012
    path: tests/idea-narrative-forward-0.9.0-preview.3/run-001/release/protected-content-register-v012.yaml
identity_status: preserved
scientific_content_change: none
---

# Revision delta: v012 to v013

## Scope

This revision is a concentrated editorial repair of the complete dossier. The
narrative repair plan contained no actions, so no additional narrative
restructuring was introduced. The changes implement the eight language findings
in the assigned language assessment without selecting unresolved scientific or
statistical specifications.

## Applied repairs

| Finding | Locator | Operation | Result |
|---|---|---|---|
| L001 | Reader-facing core, research question, contribution/evidence chain, stage III methods and risk table | define / replace | Defined each trial's “合格共同指标” as the indicators measured at that trial's relevant visit that match stage II physiological anchors in construct, specimen, unit, and visit timing. Stated that the two trials need not use the same set, then used the same term consistently. |
| L002 | Reader-facing core and all references to the two scored clinical tasks | define / replace | Defined the two main prediction tasks by their prediction targets and stated that performance is assessed by the prespecified scores and calibration measures. Replaced ambiguous task labels with “主要预测任务” or “预测任务表现”. |
| L003 | Abstract, hypothesis, work packages, evidence chains and feasibility/risk text | define / replace | Standardized the model label to “受预设约束的复杂候选模型” and explained at first use that the constraints come from the dual-database audit, anchoring, and prespecified state count and lags. |
| L004 | Complete-Idea summary, stage navigation, work-package framing and time consequence | replace | Replaced project-delivery language with “24 个月内必须完成的研究范围”, “24 个月完成标准”, and “阶段 II 的预定目标未完成”, while retaining the original months, stage scope and consequences. |
| L005 | Section 14 risk, alternative and stop-condition table | replace | Converted state-machine-style labels into complete action or consequence clauses. All triggers, thresholds, alternatives, prohibitions and stop consequences remain present. |
| L006 | Structured abstract, Background and gap | split | Split the gap statement, recoverable-object definitions and external-validation definitions into three reading units without moving formulas, thresholds or implementation details forward. |
| L007 | Abstract, milestones, external-validation methods and planned-output descriptions | replace | Standardized the hospital-validation wording to “在未参与开发的医院中开展的验证” or its grammatically equivalent local form. |
| L008 | First abstract mention and subsequent stage III references | define / replace | Defined the SOFA clinical-state analysis at first use as not relying on the stage II observation mapping, retained its outcome ordering, and then used the single short form “SOFA 临床状态分析”. |
| Dossier contract | Five evidence chains | replace label | Replaced the legacy “Transformation” field label with the required “Method / analysis / processing” label; chain content and scientific meaning are unchanged. |

## Content retained

- The identity anchor, research question, primary objective, study object,
  evidence base and patient-time/state-transition unit of inference are
  unchanged.
- The pre-onset, first-onset, post-onset and outcome continuum remains intact.
- All data sources, populations, visits, estimands, model sequence, thresholds,
  validation order, evidence states and planned-versus-completed distinctions
  are unchanged.
- All five pending specifications remain listed once in section 14 with their
  fixed components, decision points, allowed information and unresolved
  consequences.
- Section 14 remains the sole full authority for assumptions, limitations,
  risks, alternatives and stop conditions. No cross-reference was added where
  repeated limitation text had been removed.
- The conditions on stage III and its inability to replace a failed stage II
  result remain unchanged.
- No method, data source, result, evidence or scientific claim was added,
  removed or strengthened.

## Structural verification

- Complete dossier retained all 15 required H2 sections.
- Section 3 retained the five non-empty H3 functions in the required order.
- Dossier frontmatter points to the active plugin version and the four assigned
  source artifacts using logical artifact ID, version and path.
- Deterministic dossier lint passed with expected plugin version
  `0.9.0-preview.3`.
