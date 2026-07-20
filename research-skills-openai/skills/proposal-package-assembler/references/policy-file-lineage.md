# File Lineage Policy

## Purpose
Preserve traceability from initial proposal draft to final package.

## Required Records
- initial_proposal_file_path
- initial_proposal_version
- final_proposal_file_path
- final_proposal_version
- final_proposal_artifact_id
- qualifying_evaluation_proposal_ref
- revision_history_path, if available
- revision_delta_report_paths, if available
- latest_evaluation_report_path
- panel_summary_report_path, if available
- sap_file_path, only when SAP branch was requested
- content_plan_path, reader_handoff_path, editorial repair/preservation paths, and journal-route paths when those branches occurred

## Rules
- Do not replace file paths with narrative summaries.
- If multiple versions exist, identify the final version explicitly.
- If lineage is incomplete, state that the package contains incomplete lineage.
- Use `10_state/artifact-index.md` and `10_state/workflow-state.yaml` as the source of truth for current, superseded, stale, and final artifacts.
- Do not infer file lineage from narrative summaries when versioned artifact paths are missing.
- Match final proposal and qualifying evaluation by `{artifact_id, version, path}` and complete index records. Preserve legacy digest metadata when present, but never require or compare it.
