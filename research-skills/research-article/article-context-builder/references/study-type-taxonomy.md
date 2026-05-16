# Study Type Taxonomy

Classify by actual design, not author label.

## Primary Types

- `randomized_controlled_trial`: prospective allocation by randomization.
- `prospective_cohort`: exposure measured before outcome follow-up.
- `retrospective_cohort`: existing records define exposure and outcome follow-up.
- `case_control`: sampled by outcome status, exposure assessed retrospectively.
- `cross_sectional`: exposure and outcome measured at one time point.
- `diagnostic_accuracy`: index test compared against reference standard.
- `prediction_model`: development, validation, or update of a prognostic/diagnostic model.
- `systematic_review_and_meta_analysis`: explicit search and synthesis protocol.
- `mechanistic_experimental`: lab, animal, cell, or mechanism-focused experiment.
- `qualitative`: interviews, focus groups, ethnography, thematic analysis.
- `mixed_methods`: integrated quantitative and qualitative components.
- `ai_ml`: model or algorithm study where model performance is central.
- `data_resource`: dataset, registry, atlas, or resource descriptor.
- `other`: only when no category fits; explain why.

## Edge Rules

- RCT plus economic evaluation uses `randomized_controlled_trial` as primary and CHEERS as auxiliary.
- Prediction model using observational data is `prediction_model` when model performance is the contribution.
- Secondary analysis keeps the original design type and records `secondary_analysis: true`.
