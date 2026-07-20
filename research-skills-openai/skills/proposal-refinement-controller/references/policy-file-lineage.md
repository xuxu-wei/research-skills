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
- Every saved substantive, structural, editorial-only, language-only, or formatting-only proposal change creates a new versioned proposal path. Multiple edits within one writer task may share one not-yet-frozen target, but a prior frozen proposal is never overwritten.
- Major structural rewrites must create a new versioned file path.
- Every updated file must have a version label.
- Every version must remain linked to the previous proposal version.
- Revision plans, responses, and delta reports live under `06_revisions/round-NNN/`.
- Editorial repair briefs, protected-content registers, and action-execution reports live under `06_revisions/round-NNN/` and link source and target proposal logical identities.

## Prohibited Behavior

- Creating an unlinked new proposal from conversation memory.
- Replacing a proposal without change summary.
- Removing unresolved issues without actual revision.
- Treating formatting or copy-editing as substantive improvement.
