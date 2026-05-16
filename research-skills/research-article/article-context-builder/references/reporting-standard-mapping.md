# Reporting Standard Mapping

Use reporting standards as checklists, not as claims of quality.

## Core Mapping

| Study Type | Primary Standard |
|---|---|
| randomized_controlled_trial | CONSORT |
| observational cohort/case-control/cross-sectional | STROBE |
| diagnostic_accuracy | STARD |
| prediction_model | TRIPOD |
| systematic_review_and_meta_analysis | PRISMA |
| qualitative | COREQ or SRQR |
| mixed_methods | Mixed Methods Appraisal / journal-specific checklist |
| economic evaluation | CHEERS |
| case_report | CARE |
| animal/mechanistic experiment | ARRIVE when animals are involved |
| quality improvement | SQUIRE |
| ai_ml clinical model | TRIPOD-AI or CONSORT-AI/STARD-AI when applicable |
| data_resource | journal data descriptor checklist |

## Selection Rules

- Select one primary standard and any necessary auxiliary standards.
- Extensions override base standards for extension-specific items but do not replace the base standard.
- Journal instructions override generic defaults; record `journal_override`.
- If no exact standard exists, set `no_exact_match: true` and use the nearest checklist only as a structural aid.
