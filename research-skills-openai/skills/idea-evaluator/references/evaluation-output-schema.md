# Evaluation Output Schema

管理 evaluation report 的核心输出字段。

## Required Output Sections

- review ID, reviewer skill, and reviewer instance ID
- workflow ID and round ID
- frozen input artifact IDs and versions
- exact files read and review scope
- `isolation_mode: fresh_subagent`
- `prior_scores_visible: false`
- `prior_versions_visible: false`
- `revision_delta_visible: false`
- `source_edits_performed: false`
- reviewed snapshot SHA-256
- complete snapshot confirmation
- identity drift status
- idea identifier and title
- independence status
- input sufficiency status
- six dimension scores
- overall simple average
- hard gate status
- failed gates
- fatal flaws
- reviewer objections
- recommendation
- targeted repair direction
- suggested next skill
- evaluation limitations

## Allowed Recommendations

- promote
- revise_then_promote
- revise
- reframe
- merge
- keep_as_backup
- reject
