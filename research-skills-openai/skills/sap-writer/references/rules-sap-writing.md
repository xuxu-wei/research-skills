# SAP Writing Rules

## Purpose
Guide `sap-writer` in drafting a Statistical Analysis Plan only when SAP has been explicitly requested and methodology/statistics preflight permits proceeding.

## Required scope
A SAP should describe what will be analyzed, in whom, using which variables, with which primary and secondary analyses, what was prespecified, what is exploratory or post hoc, and how uncertainty, missingness, robustness, clinical interpretation, and reproducibility will be handled.

## Required sections
- Study objective and analysis objective
- Prespecified hypotheses and decision rules
- Estimand or analysis target, when applicable
- Endpoint, outcome, or metric definitions
- Clinical data source and study design context, when applicable
- Clinically important features and descriptive statistics plan, when applicable
- Study population and analysis sets
- Exposure, intervention, predictor, comparator, grouping variables, or benchmark conditions
- Covariates and adjustment strategy
- Prespecified primary analysis
- Prespecified secondary analyses
- Post hoc and exploratory analyses, clearly separated
- Missing data plan
- Sensitivity and robustness analyses
- Subgroup analyses, if justified
- Multiplicity control, if relevant
- Sample size or power considerations, if information is sufficient
- Software, reproducibility, and reporting notes
- Assumptions, limitations, and unresolved issues

## Boundaries
- Do not invent endpoint definitions, data structures, sample sizes, analysis populations, or model choices.
- Do not write a full SAP when preflight has returned `blocked`, `needs_clarification`, or a decision that does not permit SAP drafting.
- Do not evaluate the SAP; hand off to `sap-evaluator`.
- Do not alter the proposal research question implicitly to make analysis easier.
- Do not present data-driven post hoc or exploratory analyses as prespecified confirmatory analyses.
- Do not let exploratory analyses dilute or replace the primary analysis.
- Do not use generic clinical-statistical language to hide missing index dates, follow-up windows, endpoint ascertainment, or coding rules.

## Handling missing information
If a required element is unavailable, mark it as an unresolved SAP issue and explain what information is needed. Do not fill it with generic language.
