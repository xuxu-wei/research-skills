---
schema_version: research-idea-revision-delta.v1
artifact_id: revision-delta-I01-001-v004-to-v005
workflow_id: RID-SEPSIS-CSM-20260717-001
idea_id: I01-001
version_id: v001
change_type: editorial_repair_delta
source_artifact:
  artifact_id: idea-dossier-I01-001-v004
  version: v004
  path: tests/idea-narrative-forward-0.9.0-preview.3/run-001/revised/idea-dossier-v004.md
revised_artifact:
  artifact_id: idea-dossier-I01-001-v005
  version: v005
  path: tests/idea-narrative-forward-0.9.0-preview.3/run-001/final/idea-dossier-v005.md
repair_plan:
  artifact_id: narrative-repair-plan-I01-001-r002
  version: r002
  path: tests/idea-narrative-forward-0.9.0-preview.3/run-001/revised/narrative-repair-plan-r002.yaml
protected_content_register:
  artifact_id: protected-content-register-I01-001-v004
  version: v004
  path: tests/idea-narrative-forward-0.9.0-preview.3/run-001/revised/protected-content-register-v004.yaml
scientific_content_change: false
method_change: false
threshold_change: false
claim_strength_change: false
actions:
  - action_id: NRP-001
    status: completed
    operation: replace
    guessing_required: false
    source_locator:
      section_heading: "Feasibility, resources, risks, alternatives, and stop conditions"
      subsection_heading: "Authoritative limitations, feasibility findings, interpretation boundaries, alternatives, and stop conditions"
    removed_navigation: "第 11 节"
    replacement_navigation: "Scientific falsification criteria"
    completion_note: "已用全文可见且唯一的小节标题替换不可由可见标题核对的序号指引；证伪标准与操作性停止条件的章节职责保持分离。"
frozen: true
---

# Revision delta: idea dossier v004 to v005

## Completed editorial action

NRP-001 已完成。第 14 节权威限制小节中的导航句，现直接指向可见且唯一的 “Scientific falsification criteria” 小节；读者无需按隐藏序号计数即可定位科学证伪标准。该修改依据 repair plan 的明确指令完成，无需猜测或补充未提供的内容。

## Preservation statement

除 frontmatter 的版本身份与三项逻辑血缘引用外，v005 相对 v004 仅修改上述导航指引。科学内容、研究方法、全部阈值、主张强度，以及第 14 节作为限制、可行性发现、解释边界、替代方案和停止条件唯一权威位置的安排均保持不变。
