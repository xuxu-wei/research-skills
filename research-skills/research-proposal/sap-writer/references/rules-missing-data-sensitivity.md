# Missing Data and Sensitivity Rules

## Purpose
Define minimum expectations for missing data handling, robustness checks, and sensitivity analyses in SAP drafting.

## Missing data plan
The SAP should state:
- Which variables may have missingness
- Expected or known missingness pattern, if available
- Primary handling approach
- Assumptions behind the approach
- Sensitivity analysis for important missingness assumptions, when feasible

## Sensitivity analysis
Sensitivity analyses should target the most important threats to inference or interpretation, such as:
- Missing data assumptions
- Confounding or adjustment strategy
- Alternative endpoint definitions
- Alternative analytic population definitions
- Outlier or influential observation handling
- Measurement error or misclassification
- Model specification choices
- Informative censoring, competing risks, or loss to follow-up in clinical time-to-event analyses
- Site/provider clustering or repeated measures in clinical datasets
- Immortal time, indication bias, or selection bias in observational clinical studies

## Avoid
- Generic “missing data will be handled appropriately” statements
- Sensitivity analyses unrelated to the core analysis risk
- Excessive exploratory analyses that dilute the primary analysis
- Claims that missing data are ignorable without justification
- Sensitivity analyses invented after seeing results without being labeled post hoc
