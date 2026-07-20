---
schema_version: research-idea.v3
plugin_version: "0.10.0"
artifact_id: artifact-index-v001
version_id: v001
workflow_id: sepsis-complex-system-idea-generation-v001
round_id: round-001
path: 05_state/artifact-index.md
source_skill: research-idea-orchestrator
created_by_instance_id: fresh-idea-portfolio-assembler-v001
change_type: create
status: current
frozen: false
coverage_scope: all_standard_artifacts_complete_history
expected_standard_artifact_count: 56
legacy_unresolved_provenance: []
artifacts:
  - artifact_id: user-idea-v001
    idea_id: not_applicable
    role: input
    version_id: v001
    workflow_id: sepsis-complex-system-idea-generation-v001
    round_id: unknown
    plugin_version: unknown
    source_skill: user
    created_by_instance_id: user
    path: 00_input/user-idea-v001.md
    based_on: []
    change_type: create
    status: frozen_input
    frozen: true
  - artifact_id: research-context-brief-v001
    idea_id: not_applicable
    role: context_brief
    version_id: v001
    workflow_id: sepsis-complex-system-idea-generation-v001
    round_id: round-001
    plugin_version: "0.10.0"
    source_skill: research-context-builder
    created_by_instance_id: unknown
    path: 01_context/research-context-brief-v001.md
    based_on: [{artifact_id: user-idea-v001, version: v001}]
    change_type: create
    status: current
    frozen: true
  - artifact_id: evidence-map-v001
    idea_id: not_applicable
    role: evidence_map
    version_id: v001
    workflow_id: sepsis-complex-system-idea-generation-v001
    round_id: round-001
    plugin_version: unknown
    source_skill: research-opportunity-mapper
    created_by_instance_id: unknown
    path: 02_evidence/evidence-map-v001.md
    based_on: [{artifact_id: user-idea-v001, version: v001}, {artifact_id: research-context-brief-v001, version: v001}]
    change_type: create
    status: current
    frozen: true
  - artifact_id: opportunity-map-v001
    idea_id: not_applicable
    role: opportunity_map
    version_id: v001
    workflow_id: sepsis-complex-system-idea-generation-v001
    round_id: round-001
    plugin_version: unknown
    source_skill: research-opportunity-mapper
    created_by_instance_id: unknown
    path: 02_evidence/opportunity-map-v001.md
    based_on: [{artifact_id: evidence-map-v001, version: v001}]
    change_type: create
    status: current
    frozen: true
  - artifact_id: idea-routing-decision-v001
    idea_id: not_applicable
    role: routing_decision
    version_id: v001
    workflow_id: sepsis-complex-system-idea-generation-v001
    round_id: round-001
    plugin_version: "0.10.0"
    source_skill: research-idea-orchestrator
    created_by_instance_id: fresh-idea-portfolio-assembler-v001
    path: 05_state/idea-routing-decision-v001.yaml
    based_on: [{artifact_id: research-context-brief-v001, version: v001}, {artifact_id: evidence-map-v001, version: v001}, {artifact_id: opportunity-map-v001, version: v001}, {artifact_id: idea-dossier-I01-001-v006, version: v006}]
    change_type: create
    status: current
    frozen: true
  - artifact_id: idea-node-I01-001
    idea_id: I01-001
    role: idea_node
    version_id: v001
    workflow_id: sepsis-complex-system-idea-generation-v001
    round_id: round-001
    plugin_version: "0.10.0"
    source_skill: research-idea-orchestrator
    created_by_instance_id: fresh-idea-portfolio-assembler-v001
    path: 03_ideas/nodes/I01-001/node.yaml
    based_on: [{artifact_id: idea-dossier-I01-001-v006, version: v006}, {artifact_id: evaluation-I01-001-r008, version: r008}]
    change_type: create
    status: revision_required
    frozen: false
  - artifact_id: idea-index-v001
    idea_id: not_applicable
    role: idea_index
    version_id: v001
    workflow_id: sepsis-complex-system-idea-generation-v001
    round_id: round-001
    plugin_version: "0.10.0"
    source_skill: research-idea-orchestrator
    created_by_instance_id: fresh-idea-portfolio-assembler-v001
    path: 03_ideas/idea-index-v001.yaml
    based_on: [{artifact_id: idea-routing-decision-v001, version: v001}, {artifact_id: idea-node-I01-001, version: v001}]
    change_type: create
    status: current
    frozen: true
  - artifact_id: reference-ledger-I01-001-v001
    idea_id: I01-001
    role: reference_ledger
    version_id: v001
    workflow_id: sepsis-complex-system-idea-generation-v001
    round_id: round-001
    plugin_version: "0.10.0"
    source_skill: research-idea-orchestrator
    created_by_instance_id: fresh-idea-portfolio-assembler-v001
    path: 03_ideas/nodes/I01-001/references/reference-ledger.md
    based_on: [{artifact_id: evidence-map-v001, version: v001}, {artifact_id: opportunity-map-v001, version: v001}, {artifact_id: idea-dossier-I01-001-v006, version: v006}, {artifact_id: narrative-assessment-I01-001-r007, version: r007}, {artifact_id: language-assessment-I01-001-r007, version: r007}]
    change_type: create
    status: current
    frozen: false
  - artifact_id: idea-dossier-I01-001-v001
    idea_id: I01-001
    role: idea_dossier
    version_id: v001
    workflow_id: sepsis-complex-system-idea-generation-v001
    round_id: unknown
    plugin_version: "0.10.0"
    source_skill: unknown
    created_by_instance_id: unknown
    path: 03_ideas/nodes/I01-001/dossiers/idea-dossier-v001.md
    based_on: []
    change_type: create
    status: superseded
    frozen: true
  - artifact_id: idea-dossier-I01-001-v002
    idea_id: I01-001
    role: idea_dossier
    version_id: v002
    workflow_id: sepsis-complex-system-idea-generation-v001
    round_id: round-001
    plugin_version: "0.10.0"
    source_skill: multi-path-idea-generator
    created_by_instance_id: unknown
    path: 03_ideas/nodes/I01-001/dossiers/idea-dossier-v002.md
    based_on: [{artifact_id: idea-dossier-I01-001-v001, version: v001}, {artifact_id: preflight-r001, version: r001}]
    change_type: scientific_revision
    status: superseded
    frozen: true
  - artifact_id: idea-dossier-I01-001-v003
    idea_id: I01-001
    role: idea_dossier
    version_id: v003
    workflow_id: sepsis-complex-system-idea-generation-v001
    round_id: r002
    plugin_version: "0.10.0"
    source_skill: multi-path-idea-generator
    created_by_instance_id: unknown
    path: 03_ideas/nodes/I01-001/dossiers/idea-dossier-v003.md
    based_on: [{artifact_id: idea-dossier-I01-001-v002, version: v002}, {artifact_id: preflight-r002, version: r002}, {artifact_id: revision-plan-I01-001-r002-v002, version: v002}]
    change_type: scientific_revision
    status: superseded
    frozen: true
  - artifact_id: idea-dossier-I01-001-v004
    idea_id: I01-001
    role: idea_dossier
    version_id: v004
    workflow_id: sepsis-complex-system-idea-generation-v001
    round_id: round-003
    plugin_version: "0.10.0"
    source_skill: multi-path-idea-generator
    created_by_instance_id: unknown
    path: 03_ideas/nodes/I01-001/dossiers/idea-dossier-v004.md
    based_on: [{artifact_id: idea-dossier-I01-001-v003, version: v003}, {artifact_id: editorial-repair-writer-brief-I01-001-r001, version: r001}, {artifact_id: protected-content-register-v001, version: v001}]
    change_type: editorial_repair
    status: superseded
    frozen: true
  - artifact_id: idea-dossier-I01-001-v005
    idea_id: I01-001
    role: idea_dossier
    version_id: v005
    workflow_id: sepsis-complex-system-idea-generation-v001
    round_id: round-004
    plugin_version: "0.10.0"
    source_skill: multi-path-idea-generator
    created_by_instance_id: unknown
    path: 03_ideas/nodes/I01-001/dossiers/idea-dossier-v005.md
    based_on: [{artifact_id: idea-dossier-I01-001-v004, version: v004}, {artifact_id: methodology-statistics-preflight-I01-001-r004, version: r004}]
    change_type: scientific_revision
    status: superseded
    frozen: true
  - artifact_id: idea-dossier-I01-001-v006
    idea_id: I01-001
    role: idea_dossier
    version_id: v006
    workflow_id: sepsis-complex-system-idea-generation-v001
    round_id: round-006
    plugin_version: "0.10.0"
    source_skill: multi-path-idea-generator
    created_by_instance_id: unknown
    path: 03_ideas/nodes/I01-001/dossiers/idea-dossier-v006.md
    based_on: [{artifact_id: idea-dossier-I01-001-v005, version: v005}, {artifact_id: editorial-repair-writer-brief-I01-001-r002, version: r002}, {artifact_id: protected-content-register-v002, version: v002}]
    change_type: editorial_repair
    status: current_revision_required
    frozen: true
  - artifact_id: revision-plan-I01-001-r001-v001
    idea_id: I01-001
    role: revision_plan
    version_id: v001
    workflow_id: sepsis-complex-system-idea-generation-v001
    round_id: round-001
    plugin_version: "0.10.0"
    source_skill: multi-path-idea-generator
    created_by_instance_id: unknown
    path: 03_ideas/nodes/I01-001/revisions/round-001/revision-plan-v001.md
    based_on: [{artifact_id: idea-dossier-I01-001-v001, version: v001}, {artifact_id: preflight-r001, version: r001}]
    change_type: scientific_revision_plan
    status: executed_lineage
    frozen: true
  - artifact_id: revision-delta-I01-001-v001-to-v002
    idea_id: I01-001
    role: revision_delta
    version_id: v001-to-v002
    workflow_id: sepsis-complex-system-idea-generation-v001
    round_id: round-001
    plugin_version: "0.10.0"
    source_skill: multi-path-idea-generator
    created_by_instance_id: unknown
    path: 03_ideas/nodes/I01-001/revisions/round-001/revision-delta-v001-to-v002.md
    based_on: [{artifact_id: idea-dossier-I01-001-v001, version: v001}, {artifact_id: preflight-r001, version: r001}]
    change_type: scientific_revision_delta
    status: lineage
    frozen: true
  - artifact_id: revision-delta-I01-001-v002-to-v003
    idea_id: I01-001
    role: revision_delta
    version_id: v003
    workflow_id: sepsis-complex-system-idea-generation-v001
    round_id: r002
    plugin_version: "0.10.0"
    source_skill: multi-path-idea-generator
    created_by_instance_id: unknown
    path: 03_ideas/nodes/I01-001/revisions/round-002/revision-delta-v002-to-v003.md
    based_on: [{artifact_id: idea-dossier-I01-001-v002, version: v002}, {artifact_id: preflight-r002, version: r002}, {artifact_id: revision-plan-I01-001-r002-v002, version: v002}]
    change_type: scientific_revision_delta
    status: lineage
    frozen: true
  - artifact_id: revision-delta-I01-001-v003-to-v004
    idea_id: I01-001
    role: revision_delta
    version_id: v003-to-v004
    workflow_id: sepsis-complex-system-idea-generation-v001
    round_id: round-003
    plugin_version: "0.10.0"
    source_skill: unknown
    created_by_instance_id: unknown
    path: 03_ideas/nodes/I01-001/revisions/round-003/revision-delta-v003-to-v004.md
    based_on: [{artifact_id: idea-dossier-I01-001-v003, version: v003}, {artifact_id: editorial-repair-writer-brief-I01-001-r001, version: r001}, {artifact_id: protected-content-register-v001, version: v001}]
    change_type: editorial_repair_delta
    status: lineage
    frozen: true
  - artifact_id: revision-delta-I01-001-v004-to-v005
    idea_id: I01-001
    role: revision_delta
    version_id: v004-to-v005
    workflow_id: sepsis-complex-system-idea-generation-v001
    round_id: round-004
    plugin_version: "0.10.0"
    source_skill: unknown
    created_by_instance_id: unknown
    path: 03_ideas/nodes/I01-001/revisions/round-004/revision-delta-v004-to-v005.md
    based_on: [{artifact_id: idea-dossier-I01-001-v004, version: v004}, {artifact_id: methodology-statistics-preflight-I01-001-r004, version: r004}]
    change_type: scientific_revision_delta
    status: lineage
    frozen: true
  - artifact_id: revision-delta-I01-001-v005-to-v006
    idea_id: I01-001
    role: revision_delta
    version_id: v005-to-v006
    workflow_id: sepsis-complex-system-idea-generation-v001
    round_id: round-005
    plugin_version: "0.10.0"
    source_skill: multi-path-idea-generator
    created_by_instance_id: unknown
    path: 03_ideas/nodes/I01-001/revisions/round-005/revision-delta-v005-to-v006.md
    based_on: [{artifact_id: idea-dossier-I01-001-v005, version: v005}, {artifact_id: editorial-repair-writer-brief-I01-001-r002, version: r002}, {artifact_id: protected-content-register-v002, version: v002}]
    change_type: editorial_repair_delta
    status: lineage
    frozen: true
  - artifact_id: revision-plan-I01-001-r002-v002
    idea_id: I01-001
    role: revision_plan
    version_id: v002
    workflow_id: sepsis-complex-system-idea-generation-v001
    round_id: r002
    plugin_version: unknown
    source_skill: unknown
    created_by_instance_id: unknown
    path: 03_ideas/nodes/I01-001/revisions/round-002/revision-plan-v002.md
    based_on: [{artifact_id: idea-dossier-I01-001-v002, version: v002}, {artifact_id: preflight-r002, version: r002}]
    change_type: revision_plan
    status: lineage
    frozen: true
  - artifact_id: editorial-repair-writer-brief-I01-001-r001
    idea_id: I01-001
    role: editorial_repair_writer_brief
    version_id: r001
    workflow_id: sepsis-complex-system-idea-generation-v001
    round_id: round-003
    plugin_version: unknown
    source_skill: research-idea-orchestrator
    created_by_instance_id: unknown
    path: 03_ideas/nodes/I01-001/revisions/round-003/editorial-repair-writer-brief-r001.yaml
    based_on: [{artifact_id: idea-dossier-I01-001-v003, version: v003}, {artifact_id: protected-content-register-v001, version: v001}]
    change_type: create
    status: lineage
    frozen: true
  - artifact_id: editorial-repair-writer-brief-I01-001-r002
    idea_id: I01-001
    role: editorial_repair_writer_brief
    version_id: r002
    workflow_id: sepsis-complex-system-idea-generation-v001
    round_id: round-005
    plugin_version: unknown
    source_skill: research-idea-orchestrator
    created_by_instance_id: unknown
    path: 03_ideas/nodes/I01-001/revisions/round-005/editorial-repair-writer-brief-r002.yaml
    based_on: [{artifact_id: idea-dossier-I01-001-v005, version: v005}, {artifact_id: protected-content-register-v002, version: v002}]
    change_type: create
    status: lineage_current_repair
    frozen: true
  - artifact_id: protected-content-register-v001
    idea_id: I01-001
    role: protected_content_register
    version_id: v001
    workflow_id: sepsis-complex-system-idea-generation-v001
    round_id: round-003
    plugin_version: unknown
    source_skill: research-idea-orchestrator
    created_by_instance_id: unknown
    path: 05_state/protected-content-register-v001.yaml
    based_on: [{artifact_id: idea-dossier-I01-001-v003, version: v003}]
    change_type: create
    status: superseded
    frozen: true
  - artifact_id: protected-content-register-v002
    idea_id: I01-001
    role: protected_content_register
    version_id: v002
    workflow_id: sepsis-complex-system-idea-generation-v001
    round_id: round-005
    plugin_version: unknown
    source_skill: research-idea-orchestrator
    created_by_instance_id: unknown
    path: 05_state/protected-content-register-v002.yaml
    based_on: [{artifact_id: idea-dossier-I01-001-v005, version: v005}]
    change_type: create
    status: current_repair_register
    frozen: true
  - artifact_id: preflight-r001
    idea_id: I01-001
    role: preflight_report
    version_id: r001
    workflow_id: sepsis-complex-system-idea-generation-v001
    round_id: round-001
    plugin_version: unknown
    source_skill: methodology-statistics-preflight
    created_by_instance_id: unknown
    path: 03_ideas/nodes/I01-001/reviews/preflight-r001.md
    based_on: [{artifact_id: idea-dossier-I01-001-v001, version: v001}]
    change_type: review
    status: superseded
    frozen: true
  - artifact_id: preflight-r002
    idea_id: I01-001
    role: preflight_report
    version_id: r002
    workflow_id: sepsis-complex-system-idea-generation-v001
    round_id: r002
    plugin_version: unknown
    source_skill: methodology-statistics-preflight
    created_by_instance_id: unknown
    path: 03_ideas/nodes/I01-001/reviews/preflight-r002.md
    based_on: [{artifact_id: idea-dossier-I01-001-v002, version: v002}]
    change_type: review
    status: superseded
    frozen: true
  - artifact_id: methodology-statistics-preflight-I01-001-r004
    idea_id: I01-001
    role: preflight_report
    version_id: r004
    workflow_id: sepsis-complex-system-idea-generation-v001
    round_id: round-004
    plugin_version: unknown
    source_skill: methodology-statistics-preflight
    created_by_instance_id: unknown
    path: 03_ideas/nodes/I01-001/reviews/preflight-r004.md
    based_on: [{artifact_id: idea-dossier-I01-001-v004, version: v004}]
    change_type: review
    status: superseded
    frozen: true
  - artifact_id: methodology-statistics-preflight-I01-001-r005
    idea_id: I01-001
    role: preflight_report
    version_id: r005
    workflow_id: sepsis-complex-system-idea-generation-v001
    round_id: r005
    plugin_version: "0.10.0"
    source_skill: methodology-statistics-preflight
    created_by_instance_id: methodology-statistics-preflight-I01-001-r005-20260720T132103+0800
    path: 03_ideas/nodes/I01-001/reviews/preflight-r005.md
    based_on: [{artifact_id: idea-dossier-I01-001-v005, version: v005}, {artifact_id: user-idea-v001, version: v001}]
    change_type: review
    status: current_scientific_preflight_preserved_into_v006
    frozen: true
  - artifact_id: revision-plan-I01-001-r004-v003
    idea_id: I01-001
    role: revision_plan
    version_id: v003
    workflow_id: sepsis-complex-system-idea-generation-v001
    round_id: round-004
    plugin_version: "0.10.0"
    source_skill: unknown
    created_by_instance_id: unknown
    path: 03_ideas/nodes/I01-001/revisions/round-004/revision-plan-v003.md
    based_on: [{artifact_id: idea-dossier-I01-001-v004, version: v004}, {artifact_id: methodology-statistics-preflight-I01-001-r004, version: r004}]
    change_type: scientific_revision_plan
    status: executed_lineage
    frozen: true
  - artifact_id: preflight-r003
    idea_id: I01-001
    role: preflight_report
    version_id: r003
    workflow_id: sepsis-complex-system-idea-generation-v001
    round_id: r003
    plugin_version: "0.10.0"
    source_skill: methodology-statistics-preflight
    created_by_instance_id: fresh-methodology-statistics-preflight-r003
    path: 03_ideas/nodes/I01-001/reviews/preflight-r003.md
    based_on: [{artifact_id: idea-dossier-I01-001-v003, version: v003}]
    change_type: review
    status: superseded_pass
    frozen: true
  - artifact_id: content-preservation-I01-001-r002
    idea_id: I01-001
    role: content_preservation_report
    version_id: r002
    workflow_id: sepsis-complex-system-idea-generation-v001
    round_id: editorial-repair-round-003
    plugin_version: "0.10.0"
    source_skill: idea-narrative-assessor
    created_by_instance_id: new_preservation_r002
    path: 03_ideas/nodes/I01-001/reviews/content-preservation-r002.md
    based_on: [{artifact_id: idea-dossier-I01-001-v003, version: v003}, {artifact_id: idea-dossier-I01-001-v004, version: v004}, {artifact_id: protected-content-register-v001, version: v001}, {artifact_id: revision-delta-I01-001-v003-to-v004, version: v003-to-v004}]
    change_type: review
    status: superseded_scientific_content_preserved
    frozen: true
  - artifact_id: narrative-assessment-I01-001-r001
    idea_id: I01-001
    role: narrative_assessment
    version_id: r001
    workflow_id: sepsis-complex-system-idea-generation-v001
    round_id: r001
    plugin_version: "0.10.0"
    source_skill: idea-narrative-assessor
    created_by_instance_id: new-narrative-r001
    path: 03_ideas/nodes/I01-001/reviews/narrative-assessment-r001.md
    based_on: [{artifact_id: idea-dossier-I01-001-v003, version: v003}]
    change_type: review
    status: superseded_major_narrative_revision
    frozen: true
  - artifact_id: narrative-repair-plan-I01-001-r001
    idea_id: I01-001
    role: narrative_repair_plan
    version_id: r001
    workflow_id: sepsis-complex-system-idea-generation-v001
    round_id: r001
    plugin_version: "0.10.0"
    source_skill: idea-narrative-assessor
    created_by_instance_id: new-narrative-r001
    path: 03_ideas/nodes/I01-001/reviews/narrative-repair-plan-r001.yaml
    based_on: [{artifact_id: narrative-assessment-I01-001-r001, version: r001}, {artifact_id: idea-dossier-I01-001-v003, version: v003}]
    change_type: review_plan
    status: superseded_major_repair_plan
    frozen: true
  - artifact_id: narrative-assessment-I01-001-r003
    idea_id: I01-001
    role: narrative_assessment
    version_id: r003
    workflow_id: sepsis-complex-system-idea-generation-v001
    round_id: r003
    plugin_version: "0.10.0"
    source_skill: idea-narrative-assessor
    created_by_instance_id: fresh-new-narrative-r003
    path: 03_ideas/nodes/I01-001/reviews/narrative-assessment-r003.md
    based_on: [{artifact_id: idea-dossier-I01-001-v004, version: v004}]
    change_type: review
    status: superseded_narrative_ready
    frozen: true
  - artifact_id: narrative-repair-plan-I01-001-r003
    idea_id: I01-001
    role: narrative_repair_plan
    version_id: r003
    workflow_id: sepsis-complex-system-idea-generation-v001
    round_id: r003
    plugin_version: "0.10.0"
    source_skill: idea-narrative-assessor
    created_by_instance_id: fresh-new-narrative-r003
    path: 03_ideas/nodes/I01-001/reviews/narrative-repair-plan-r003.yaml
    based_on: [{artifact_id: narrative-assessment-I01-001-r003, version: r003}, {artifact_id: idea-dossier-I01-001-v004, version: v004}]
    change_type: review_plan
    status: superseded_empty_ready_plan
    frozen: true
  - artifact_id: narrative-assessment-I01-001-r004
    idea_id: I01-001
    role: narrative_assessment
    version_id: r004
    workflow_id: sepsis-complex-system-idea-generation-v001
    round_id: r004
    plugin_version: "0.10.0"
    source_skill: idea-narrative-assessor
    created_by_instance_id: idea-narrative-assessor-r004-fresh-01
    path: 03_ideas/nodes/I01-001/reviews/narrative-assessment-r004.md
    based_on: [{artifact_id: idea-dossier-I01-001-v004, version: v004}]
    change_type: review
    status: superseded_clarification_required
    frozen: true
  - artifact_id: narrative-repair-plan-I01-001-r004
    idea_id: I01-001
    role: narrative_repair_plan
    version_id: r004
    workflow_id: sepsis-complex-system-idea-generation-v001
    round_id: r004
    plugin_version: "0.10.0"
    source_skill: idea-narrative-assessor
    created_by_instance_id: idea-narrative-assessor-r004-fresh-01
    path: 03_ideas/nodes/I01-001/reviews/narrative-repair-plan-r004.yaml
    based_on: [{artifact_id: narrative-assessment-I01-001-r004, version: r004}, {artifact_id: idea-dossier-I01-001-v004, version: v004}]
    change_type: review_plan
    status: superseded_clarification_plan
    frozen: true
  - artifact_id: narrative-assessment-I01-001-r006
    idea_id: I01-001
    role: narrative_assessment
    version_id: r006
    workflow_id: sepsis-complex-system-idea-generation-v001
    round_id: r006
    plugin_version: "0.10.0"
    source_skill: idea-narrative-assessor
    created_by_instance_id: idea-narrative-assessor-r006-fresh-20260720
    path: 03_ideas/nodes/I01-001/reviews/narrative-assessment-r006.md
    based_on: [{artifact_id: idea-dossier-I01-001-v005, version: v005}]
    change_type: review
    status: superseded_minor_narrative_revision
    frozen: true
  - artifact_id: narrative-repair-plan-I01-001-r006
    idea_id: I01-001
    role: narrative_repair_plan
    version_id: r006
    workflow_id: sepsis-complex-system-idea-generation-v001
    round_id: r006
    plugin_version: "0.10.0"
    source_skill: idea-narrative-assessor
    created_by_instance_id: idea-narrative-assessor-r006-fresh-20260720
    path: 03_ideas/nodes/I01-001/reviews/narrative-repair-plan-r006.yaml
    based_on: [{artifact_id: narrative-assessment-I01-001-r006, version: r006}, {artifact_id: idea-dossier-I01-001-v005, version: v005}]
    change_type: review_plan
    status: superseded_minor_repair_plan
    frozen: true
  - artifact_id: language-assessment-I01-001-r001
    idea_id: I01-001
    role: language_assessment
    version_id: r001
    workflow_id: sepsis-complex-system-idea-generation-v001
    round_id: r001
    plugin_version: "0.10.0"
    source_skill: academic-language-assessor
    created_by_instance_id: fresh-academic-language-assessor-r001
    path: 03_ideas/nodes/I01-001/reviews/language-assessment-r001.md
    based_on: [{artifact_id: idea-dossier-I01-001-v003, version: v003}]
    change_type: review
    status: superseded_major_language_revision
    frozen: true
  - artifact_id: language-assessment-I01-001-r003
    idea_id: I01-001
    role: language_assessment
    version_id: r003
    workflow_id: sepsis-complex-system-idea-generation-v001
    round_id: r003
    plugin_version: "0.10.0"
    source_skill: academic-language-assessor
    created_by_instance_id: new_language_r003
    path: 03_ideas/nodes/I01-001/reviews/language-assessment-r003.md
    based_on: [{artifact_id: idea-dossier-I01-001-v004, version: v004}]
    change_type: review
    status: superseded_minor_language_revision
    frozen: true
  - artifact_id: language-assessment-I01-001-r004
    idea_id: I01-001
    role: language_assessment
    version_id: r004
    workflow_id: sepsis-complex-system-idea-generation-v001
    round_id: r004
    plugin_version: "0.10.0"
    source_skill: academic-language-assessor
    created_by_instance_id: new-blind-language-r004
    path: 03_ideas/nodes/I01-001/reviews/language-assessment-r004.md
    based_on: [{artifact_id: idea-dossier-I01-001-v004, version: v004}]
    change_type: review
    status: superseded_minor_language_revision
    frozen: true
  - artifact_id: language-assessment-I01-001-r006
    idea_id: I01-001
    role: language_assessment
    version_id: r006
    workflow_id: sepsis-complex-system-idea-generation-v001
    round_id: r006
    plugin_version: "0.10.0"
    source_skill: academic-language-assessor
    created_by_instance_id: academic-language-assessor-fresh-r006-20260720
    path: 03_ideas/nodes/I01-001/reviews/language-assessment-r006.md
    based_on: [{artifact_id: idea-dossier-I01-001-v005, version: v005}]
    change_type: review
    status: superseded_major_language_revision
    frozen: true
  - artifact_id: writer-action-compliance-I01-001-r002
    idea_id: I01-001
    role: writer_action_compliance_report
    version_id: r002
    workflow_id: sepsis-complex-system-idea-generation-v001
    round_id: r002
    plugin_version: "0.10.0"
    source_skill: research-idea-orchestrator
    created_by_instance_id: unknown
    path: 03_ideas/nodes/I01-001/reviews/writer-action-compliance-r002.md
    based_on: [{artifact_id: idea-dossier-I01-001-v003, version: v003}, {artifact_id: editorial-repair-writer-brief-I01-001-r001, version: r001}, {artifact_id: idea-dossier-I01-001-v004, version: v004}, {artifact_id: revision-delta-I01-001-v003-to-v004, version: v003-to-v004}]
    change_type: compliance_audit
    status: historical_all_actions_closed
    frozen: true
  - artifact_id: content-preservation-I01-001-r007
    idea_id: I01-001
    role: content_preservation_report
    version_id: r007
    workflow_id: sepsis-complex-system-idea-generation-v001
    round_id: r007
    plugin_version: "0.10.0"
    source_skill: idea-narrative-assessor
    created_by_instance_id: fresh-scientific-content-preservation-checker-r007
    path: 03_ideas/nodes/I01-001/reviews/content-preservation-r007.md
    based_on: [{artifact_id: idea-dossier-I01-001-v005, version: v005}, {artifact_id: idea-dossier-I01-001-v006, version: v006}, {artifact_id: protected-content-register-v002, version: v002}, {artifact_id: revision-delta-I01-001-v005-to-v006, version: v005-to-v006}]
    change_type: review
    status: scientific_content_preserved
    frozen: true
  - artifact_id: narrative-assessment-I01-001-r007
    idea_id: I01-001
    role: narrative_assessment
    version_id: r007
    workflow_id: sepsis-complex-system-idea-generation-v001
    round_id: r007
    plugin_version: "0.10.0"
    source_skill: idea-narrative-assessor
    created_by_instance_id: fresh-idea-narrative-assessor-r007
    path: 03_ideas/nodes/I01-001/reviews/narrative-assessment-r007.md
    based_on: [{artifact_id: idea-dossier-I01-001-v006, version: v006}]
    change_type: review
    status: minor_narrative_revision
    frozen: true
  - artifact_id: narrative-repair-plan-I01-001-r007
    idea_id: I01-001
    role: narrative_repair_plan
    version_id: r007
    workflow_id: sepsis-complex-system-idea-generation-v001
    round_id: r007
    plugin_version: "0.10.0"
    source_skill: idea-narrative-assessor
    created_by_instance_id: fresh-idea-narrative-assessor-r007
    path: 03_ideas/nodes/I01-001/reviews/narrative-repair-plan-r007.yaml
    based_on: [{artifact_id: narrative-assessment-I01-001-r007, version: r007}, {artifact_id: idea-dossier-I01-001-v006, version: v006}]
    change_type: review_plan
    status: open_minor_actions
    frozen: true
  - artifact_id: language-assessment-I01-001-r007
    idea_id: I01-001
    role: language_assessment
    version_id: r007
    workflow_id: sepsis-complex-system-idea-generation-v001
    round_id: language-review-r007
    plugin_version: "0.10.0"
    source_skill: academic-language-assessor
    created_by_instance_id: academic-language-assessor-new-v006-r007b
    path: 03_ideas/nodes/I01-001/reviews/language-assessment-r007.md
    based_on: [{artifact_id: idea-dossier-I01-001-v006, version: v006}]
    change_type: review
    status: minor_language_revision
    frozen: true
  - artifact_id: evaluation-I01-001-r008
    idea_id: I01-001
    role: evaluation_report
    version_id: r008
    workflow_id: sepsis-complex-system-idea-generation-v001
    round_id: r008
    plugin_version: "0.10.0"
    source_skill: idea-evaluator
    created_by_instance_id: idea-evaluator-fresh-r008-v006
    path: 03_ideas/nodes/I01-001/reviews/evaluation-r008.md
    based_on: [{artifact_id: idea-dossier-I01-001-v006, version: v006}]
    change_type: review
    status: revise_then_promote
    frozen: true
  - artifact_id: candidate-journal-match-I01-001-r008
    idea_id: I01-001
    role: candidate_journal_match_brief
    version_id: r008
    workflow_id: sepsis-complex-system-idea-generation-v001
    round_id: r008
    plugin_version: "0.10.0"
    source_skill: research-idea-orchestrator
    created_by_instance_id: unknown
    path: 03_ideas/nodes/I01-001/reviews/candidate-journal-match-r008.yaml
    based_on: [{artifact_id: idea-dossier-I01-001-v006, version: v006}]
    change_type: materialize_score_free_candidate_payload
    status: current_unscored_unranked
    frozen: true
  - artifact_id: medical-journal-review-I01-001-r008
    idea_id: I01-001
    role: medical_journal_review
    version_id: r008
    workflow_id: sepsis-complex-system-idea-generation-v001
    round_id: r008
    plugin_version: "0.10.0"
    source_skill: medical-journal-review
    created_by_instance_id: fresh-medical-journal-review-I01-001-r008-20260720T163512+0800
    path: 03_ideas/nodes/I01-001/reviews/medical-journal-review-r008.md
    based_on: [{artifact_id: idea-dossier-I01-001-v006, version: v006}, {artifact_id: candidate-journal-match-I01-001-r008, version: r008}]
    change_type: review
    status: journal_candidates_confirmed
    frozen: true
  - artifact_id: research-idea-portfolio-v001
    idea_id: not_applicable
    role: portfolio
    version_id: v001
    workflow_id: sepsis-complex-system-idea-generation-v001
    round_id: round-001
    plugin_version: "0.10.0"
    source_skill: idea-portfolio-assembler
    created_by_instance_id: fresh-idea-portfolio-assembler-v001
    path: 04_portfolio/research-idea-portfolio-v001.md
    based_on: [{artifact_id: idea-dossier-I01-001-v006, version: v006}, {artifact_id: evaluation-I01-001-r008, version: r008}, {artifact_id: candidate-journal-match-I01-001-r008, version: r008}, {artifact_id: medical-journal-review-I01-001-r008, version: r008}, {artifact_id: narrative-assessment-I01-001-r007, version: r007}, {artifact_id: language-assessment-I01-001-r007, version: r007}]
    change_type: assemble
    status: revision_required
    frozen: true
  - artifact_id: workflow-state-v001
    idea_id: not_applicable
    role: workflow_state
    version_id: v001
    workflow_id: sepsis-complex-system-idea-generation-v001
    round_id: round-001
    plugin_version: "0.10.0"
    source_skill: research-idea-orchestrator
    created_by_instance_id: fresh-idea-portfolio-assembler-v001
    path: 05_state/workflow-state.yaml
    based_on: [{artifact_id: idea-index-v001, version: v001}, {artifact_id: research-idea-portfolio-v001, version: v001}]
    change_type: create
    status: revision_required
    frozen: false
  - artifact_id: artifact-index-v001
    idea_id: not_applicable
    role: artifact_index
    version_id: v001
    workflow_id: sepsis-complex-system-idea-generation-v001
    round_id: round-001
    plugin_version: "0.10.0"
    source_skill: research-idea-orchestrator
    created_by_instance_id: fresh-idea-portfolio-assembler-v001
    path: 05_state/artifact-index.md
    based_on: []
    change_type: create
    status: current
    frozen: false
  - artifact_id: round-001-manifest
    idea_id: not_applicable
    role: round_manifest
    version_id: v001
    workflow_id: sepsis-complex-system-idea-generation-v001
    round_id: round-001
    plugin_version: "0.10.0"
    source_skill: research-idea-orchestrator
    created_by_instance_id: fresh-idea-portfolio-assembler-v001
    path: 05_state/round-001-manifest.md
    based_on: [{artifact_id: workflow-state-v001, version: v001}, {artifact_id: research-idea-portfolio-v001, version: v001}]
    change_type: create
    status: revision_required
    frozen: true
---

# Artifact Index

## Coverage summary

| Category | Registered artifacts |
|---|---:|
| Input | 1 |
| Context | 1 |
| Evidence and opportunity maps | 2 |
| Routing decision | 1 |
| Idea metadata: node, immutable Idea index, reference ledger | 3 |
| Complete dossier versions | 6 |
| Revision lineage: plans, deltas, writer briefs, protected registers | 12 |
| Preflight reports | 5 |
| Narrative assessments and repair plans | 10 |
| Language assessments | 5 |
| Content-preservation and writer-compliance reports | 3 |
| Evaluation, candidate journal match, and medical journal review | 3 |
| Portfolio and state artifacts | 4 |
| **Total** | **56** |

The index registers every standard artifact currently present in the test directory, including superseded, failed, invalid, and otherwise historical reviewer and revision lineage. Each registered path is retained for traceability; current pointers remain separate from historical status.

## Current pointers

| Pointer | Artifact ID | Version | Path | Status |
|---|---|---|---|---|
| Current dossier | idea-dossier-I01-001-v006 | v006 | `03_ideas/nodes/I01-001/dossiers/idea-dossier-v006.md` | current; revision required |
| Current node | idea-node-I01-001 | v001 | `03_ideas/nodes/I01-001/node.yaml` | current |
| Current Idea index | idea-index-v001 | v001 | `03_ideas/idea-index-v001.yaml` | current |
| Qualifying evaluation | evaluation-I01-001-r008 | r008 | `03_ideas/nodes/I01-001/reviews/evaluation-r008.md` | revise-then-promote |
| Candidate journal match | candidate-journal-match-I01-001-r008 | r008 | `03_ideas/nodes/I01-001/reviews/candidate-journal-match-r008.yaml` | current, unscored, unranked |
| Medical journal review | medical-journal-review-I01-001-r008 | r008 | `03_ideas/nodes/I01-001/reviews/medical-journal-review-r008.md` | candidates confirmed |
| Portfolio | research-idea-portfolio-v001 | v001 | `04_portfolio/research-idea-portfolio-v001.md` | revision required |
| Workflow state | workflow-state-v001 | v001 | `05_state/workflow-state.yaml` | revision required |

## Integrity notes

- Every registered `(artifact_id, version_id)` pair is unique.
- The complete dossier lineage is v001 → v002 → v003 → v004 → v005 → v006; v006 is the sole current Idea body.
- The evaluator report, candidate journal-match brief, and medical journal review remain three separate logical artifacts and paths.
- Current node, Idea index, workflow state, manifest, portfolio, and this index all point to dossier v006 and evaluation r008.
- Open r007 minor narrative and language findings remain visible in the portfolio and workflow state; they are not reclassified or silently repaired.
