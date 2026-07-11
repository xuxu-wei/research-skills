# File Lineage Policy

## Purpose
Preserve traceability from initial proposal draft to final package.

## Required Records
- initial_proposal_file_path
- initial_proposal_version
- final_proposal_file_path
- final_proposal_version
- revision_history_path, if available
- revision_delta_report_paths, if available
- latest_evaluation_report_path
- panel_summary_report_path, if available
- sap_file_path, only when SAP branch was requested

## Rules
- Do not replace file paths with narrative summaries.
- If multiple versions exist, identify the final version explicitly.
- If lineage is incomplete, state that the package contains incomplete lineage.
- Use `10_state/artifact-index.md` and `10_state/workflow-state.yaml` as the source of truth for current, superseded, stale, and final artifacts.
- Do not infer file lineage from narrative summaries when versioned artifact paths are missing.
