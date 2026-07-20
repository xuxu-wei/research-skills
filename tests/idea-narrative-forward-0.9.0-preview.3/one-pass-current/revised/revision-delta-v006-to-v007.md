---
schema_version: research-idea-revision-delta.v1
plugin_version: 0.9.0-preview.3
artifact_id: revision-delta-I01-001-v006-to-v007
workflow_id: RID-SEPSIS-CSM-20260717-001
idea_id: I01-001
version_id: v007
path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/revised/revision-delta-v006-to-v007.md
from_artifact:
  artifact_id: idea-dossier-I01-001-v006
  version: v006
  path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/revised/idea-dossier-v006.md
to_artifact:
  artifact_id: idea-dossier-I01-001-v007
  version: v007
  path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/revised/idea-dossier-v007.md
based_on:
  - artifact_id: idea-dossier-I01-001-v006
    version: v006
    path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/revised/idea-dossier-v006.md
  - artifact_id: narrative-repair-plan-I01-001-r016
    version: r016
    path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/revised/narrative-repair-plan-r016.yaml
  - artifact_id: language-assessment-I01-001-r017
    version: r017
    path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/revised/language-assessment-r017.md
  - artifact_id: protected-content-register-I01-001-v006
    version: v006
    path: tests/idea-narrative-forward-0.9.0-preview.3/one-pass-current/revised/protected-content-register-v006.yaml
source_skill: multi-path-idea-generator
change_type: editorial_repair_delta
identity_status: preserved
scientific_change_declared: false
---

# Editorial repair delta: v006 to v007

## Scope

This revision applies the locatable language actions in
`language-assessment-I01-001-r017`. The narrative repair plan contained no
actions, so the 15-section dossier structure, the five ordered functions in
section 3, and the scientific design were not expanded or reorganized.

## Executed language repairs

| Finding | Dossier locations | Editorial operation | Result |
|---|---|---|---|
| L017-001 | Structured abstract; Rationale; research question; data table; conditional trial bridge; evidence chain; section 14 | replace; define | Replaced ambiguous references to “共同生理指标” with a direct statement that each trial separately uses indicators measured at its target visit and semantically and unit-wise matched to the prespecified stage-II physiological anchors. Retained separate trial-specific sets and analyses. |
| L017-002 | Structured abstract; objective 3; work packages; simulation recovery; evidence chains; required analyses; expected outputs | replace; define | Defined the target event as an erroneous structure receiving high-confidence support and named the measured quantity as its false-positive proportion or high-confidence misclassification rate. Preserved the existing `≤0.05` direction and all simulation scenarios. |
| L017-003 | Positioning; work packages; data; methods; evidence chains; required analyses; claim-support table; section 14 | replace; delete | Removed `G1`, “普通语言路线”, “合取成功/合取标准”, and “分析治理”. Replaced each use of “冻结” with the actual scientific action and time point: prespecifying, finalizing before test-result access, prohibiting parameter re-estimation, restricting data access, or preserving a final version. |
| L017-004 | Objectives; data audit; methods; key techniques; evidence chains; required analyses; expected outputs; section 14 | define; replace | Defined landmark analysis, ICU stay, proper scoring rule, bootstrap, pattern-mixture delta, selection tipping-point, and the operational `sepsis-like` subgroup at first reader-facing use; used consistent Chinese terms thereafter. |
| L017-005 | One-sentence summary; hospital-priority external validation; trial analysis table | split; consolidate | Kept the required one-sentence summary but placed the 24-month primary objective before the conditional trial analysis. Split long method and table-cell statements into condition, action, and consequence sentences without removing any condition. |
| L017-006 | Positioning; abstract; work packages; methods; evidence chains; expected outputs; feasibility | replace | Restored omitted head nouns: “复杂度受限的候选模型”, “显示未达预设标准项目的结果图”, “24 个月内必须完成阶段 I–II”, and “主要临床任务的预测与校准表现”. |

## Content-preservation statement

- The identity anchor, core question, study object, data sources, inference unit,
  task definitions, estimands, thresholds, validation order, conditional trial
  branches, feasibility findings, and claim strengths are unchanged.
- No data source, method, result, threshold, evidence, or scientific claim was
  added or removed.
- Section 14 remains the sole global authority for limitations, unresolved
  specifications, risks, alternatives, and stop conditions. No pointer such as
  “see section 14” was introduced elsewhere.
- All 56 protected items remain represented at their required meaning, status,
  strength, boundary, or authority location. Final preservation status remains
  for an independent preservation reviewer to determine.

## Scientific changes

None declared. This is an editorial-only repair.
