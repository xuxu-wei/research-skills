# File Lineage Policy

## Purpose

Ensure proposal revisions remain file-centered and traceable.

## Required State Fields

- `proposal_file_path`
- `proposal_version`
- `previous_proposal_file_path`, if a new file is created
- `change_summary`
- `revision_round`
- `revision_history_path`, if available
- `unresolved_issues`

## Versioning Rules

- Substantive edits must create a new versioned file path following `proposal-orchestrator/references/artifact-naming-and-directory-rules.md`.
- Minor targeted edits may update the same file only when the workflow state preserves a previous immutable version or the user explicitly requested in-place editing.
- Major structural rewrites must create a new versioned file path.
- Every updated file must have a version label.
- Every version must remain linked to the previous proposal version.
- Revision plans, responses, and delta reports live under `06_revisions/round-NNN/`.

## Prohibited Behavior

- Creating an unlinked new proposal from conversation memory.
- Replacing a proposal without change summary.
- Removing unresolved issues without actual revision.
- Treating formatting or copy-editing as substantive improvement.
