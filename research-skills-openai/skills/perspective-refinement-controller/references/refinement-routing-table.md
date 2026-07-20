# Refinement Routing Table

| Evaluator route | Controller action | User confirmation |
| --- | --- | --- |
| `accept` | proceed to panel, or after closed scientific/panel work enter the editorial quality cycle; Standard may finish only a scientific draft package | no |
| `minor_revision` | one targeted drafter revision | no, unless outlet/thesis changes |
| `major_revision_draft` | revision plan plus drafter revision, max two regular rounds | no by default |
| `argument_rebuild` | return to architect | no, unless thesis changes |
| `evidence_rebuild` | return to curator | maybe, if external retrieval/material is needed |
| `thesis_redesign` | return to input-builder | yes |
| `outlet_retarget` | update target-outlet-profile | yes |
| `reject_not_salvageable` | stop with diagnostic report | yes before further work |

Never route directly from a substantive evaluator finding to final compositor.

Editorial-cycle routes:

- conformance or preservation failure -> `editorial_repair` if purely editorial, otherwise scientific revision;
- narrative or language reassessment not ready -> normalize one new brief and reuse the same writer, within loop limits;
- final evaluator non-accept -> route by finding type to scientific or editorial repair, then rerun the required gates;
- journal/medical review requiring text change -> route back before composition and invalidate downstream version-specific reviews.
