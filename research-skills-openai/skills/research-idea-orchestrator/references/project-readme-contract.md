# Project README Contract

Load this contract only when an orchestrated task is about to finish, pause, or stop.

Create or update one `README.md` at the project root. It is a human navigation page, not evidence, workflow state, an artifact index, or a substitute for the final package. Never give it to a reviewer or list it in reviewer `files_read`.

Use ordinary Markdown without frontmatter. Keep only these sections:

```markdown
# Project delivery

## Current delivery
- [Label](relative/path)

## Current artifact
- ID / version / path: ...
- Summary: ...

## Status
- State: ...
- Pause or stop reason: ...
- Updated: YYYY-MM-DD HH:MM TZ

## Review summary
- Fatal: ...
- Blocking: ...
- Dissent: ...
- Unresolved: ...

## Next action
- Human action or resume entry: ...
```

For an Article or Perspective, insert `## Publication probability` after `Current artifact` only when the current `medical-journal-review` report contains an assessment. Copy, without recalculation, its eventual-acceptance interval, confidence, and `assessment_scope`, and link that report with a relative path. Omit the section when no assessment exists.

All delivery links and displayed paths must be relative to the project root and resolve to current artifacts. Summaries stay brief. Do not copy full artifacts, reports, complete lineage, or digests. Derive status and the next action from authoritative state, then write the README as the final persistence action before returning to the user.
