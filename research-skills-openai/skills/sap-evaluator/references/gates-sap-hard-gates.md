# SAP Hard Gates

SAP hard gates are minimum requirements for a Statistical Analysis Plan to proceed.

## Required Gates

- Primary endpoint, outcome, metric, or analysis target is defined.
- Analysis population or analysis set is identifiable.
- Primary analysis route is specified.
- Proposed method is compatible with endpoint type and data structure.
- Data source can support the primary analysis.
- Clinical data source, index date/baseline/follow-up windows, endpoint ascertainment, and coding/proxy definitions are specified when required by the design.
- Clinically important population features are considered for descriptive statistics, including relevant features not used in primary modeling.
- Prespecified primary and secondary analyses are separated from post hoc and exploratory analyses.
- Post hoc or exploratory analyses are not used as confirmatory evidence.
- Missing data strategy is adequate for the primary analysis risk level.
- Sensitivity or robustness checks are included when assumptions are material.
- SAP is aligned with proposal, context brief, or study objective.
- Major confounding, bias, clustering, censoring, or repeated-measures structure is addressed when relevant.

## Gate Outcomes

- `pass`: all required gates pass.
- `repairable_failure`: gate failure can likely be fixed through targeted revision.
- `blocking_failure`: gate failure prevents meaningful SAP execution.
