# Panel Decision Routing

| Panel recommendation | Required route | Constraints |
| --- | --- | --- |
| `strong_support` | STEP 9 editorial quality cycle | all substantive must-fix items closed |
| `support_with_minor_revision` | STEP 8.5, fresh scientific evaluation, then STEP 9 | only wording, ordering, title, abstract, paragraph-local clarity |
| `support_after_major_revision` | STEP 7 scientific revision | one panel major revision maximum |
| `not_ready` | STEP 4 or STEP 5 | choose STEP 4 if the argument structure changes; choose STEP 5 for a local redraft when the skeleton remains valid |
| `reject_or_redesign` | stop or STEP 1 with user confirmation | user confirmation required before thesis redesign |

Consensus rule:
- An issue raised by both default required scientific reviewers, or independently by at least two applicable required scientific/specialist reviewers, becomes `must-fix`.
- If all agreeing reviewers mark the issue low severity and editorial, classify it as `editorial must-fix`; it may be handled by STEP 8.5 and must not force major revision.
- Optional target-reader/outlet simulation is advisory; unless a required reviewer independently supports the issue, route it to STEP 9 narrative assessment or STEP 11 outlet matching without treating it as readiness evidence.

Panel summary must preserve individual issue IDs so the orchestrator does not lose dissenting evidence.
