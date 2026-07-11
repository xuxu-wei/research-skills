# Panel Decision Routing

| Panel recommendation | Required route | Constraints |
| --- | --- | --- |
| `strong_support` | final compositor | all substantive must-fix items closed |
| `support_with_minor_revision` | STEP 8.5 then final compositor | only wording, ordering, title, abstract, paragraph-local clarity |
| `support_after_major_revision` | STEP 6 | one panel major revision maximum |
| `not_ready` | STEP 3 or STEP 4 | choose STEP 3 if argument structure changes; choose STEP 4 if skeleton remains valid |
| `reject_or_redesign` | stop or STEP 1 with user confirmation | user confirmation required before thesis redesign |

Consensus rule:
- Issue raised by at least two reviewers becomes `must-fix`.
- If all agreeing reviewers mark the issue low severity and editorial, classify it as `editorial must-fix`; it may be handled by STEP 8.5 and must not force major revision.

Panel summary must preserve individual issue IDs so the orchestrator does not lose dissenting evidence.
