# Data-Method Fit Policy

This policy guides evaluation of whether proposed statistical methods fit available data.

## Checkpoints

- Outcome type matches model family.
- Repeated measures, clustering, pairing, censoring, competing risks, or hierarchy are handled when relevant.
- Sample size and event count are plausible for the proposed model.
- Variable definitions and derivations are sufficient.
- Missingness assumptions are plausible and addressed.
- Confounders, predictors, exposures, or covariates are available.
- Model assumptions are stated or testable.
- Planned subgroup or interaction analyses are feasible.

## High-Risk Mismatches

- Time-to-event endpoint analyzed as simple binary outcome without justification.
- Clustered or repeated observations treated as independent.
- Prediction model planned without sufficient event count or validation strategy.
- Confounding ignored in observational causal questions.
- Missingness is likely informative but handled with complete-case analysis only.
