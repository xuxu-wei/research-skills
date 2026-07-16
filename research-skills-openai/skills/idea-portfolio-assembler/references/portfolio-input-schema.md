# Portfolio Input Schema

Require route profile; current Idea node, complete dossier, version, path, and
SHA-256; qualifying dossier-only evaluation; reference ledger; lineage; sealed
orchestrator decision; and status-relevant fatal/blocking/dissent summaries.

For a focused Proposal-handoff candidate, require a fresh digest-matched
`promote` decision and `adversarial_panel_reports`
containing every role report and no unresolved blocking finding. For bounded exploration, require two or
three current dossiers, one terminal fresh evaluation per dossier, and the
`human_direction_selection_required` decision.

Reject incomplete/stale dossiers, digest mismatch, non-isolated or non-dossier-
only evaluation, missing ledger/lineage, hidden dissent, or a bounded-exploration
preselection. Use the assembly-failure report instead of guessing.
