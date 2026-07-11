# SAP Evaluation Rubric

This rubric is used by `sap-evaluator` to evaluate a frozen Statistical Analysis Plan. It does not evaluate Novelty or Impact.

## Dimensions

Use a 1–5 scale for each dimension.

### Clarity

Assesses whether the SAP clearly defines endpoints, analysis population, variables, primary analysis, secondary analyses, assumptions, and decision rules.

### Feasibility

Assesses whether available data, sample, variables, time, and resources can support the specified analyses.

### Completion

Assesses whether the SAP contains the essential components needed for execution and downstream statistical review.

### Methodological Rigor

Assesses whether the design, model choice, comparison strategy, adjustment strategy, assumptions, bias control, and interpretation rules are appropriate.

### Endpoint-Analysis Alignment

Assesses whether endpoints or metrics are matched to the stated analysis population, estimands, models, contrasts, and interpretation plan.

### Data-Method Fit

Assesses whether the data type, measurement level, repeated-measures structure, censoring, clustering, missingness, and sampling design are compatible with the proposed statistical methods.

### Clinical Data Readiness

Assesses whether clinical data source, provenance, index date, baseline/exposure/outcome/follow-up windows, coding or measurement systems, endpoint ascertainment, validation status, and clinical interpretation thresholds are specified when relevant.

### Clinical Feature Descriptives

Assesses whether the SAP proactively identifies clinically important population features and specifies descriptive summaries for baseline, disease, severity, treatment, comorbidity, care-context, socioeconomic, data availability, and follow-up characteristics when relevant. This dimension also checks that descriptive-only features are not automatically treated as adjustment variables.

### Prespecification Discipline

Assesses whether prespecified primary and secondary analyses are separated from post hoc and exploratory analyses, whether confirmatory language is limited to prespecified analyses, and whether data-driven analyses are labeled with interpretation limits.

### Missing Data Handling

Assesses whether missingness is anticipated, characterized, and handled with appropriate primary and sensitivity strategies.

### Sensitivity / Robustness

Assesses whether robustness checks address plausible alternative assumptions, model choices, confounding, measurement error, and analytic decisions.

### Reproducibility

Assesses whether software, versions, analysis sets, variable derivations, random seeds, code expectations, and documentation requirements are sufficiently specified.

## Decision Mapping

- `accept`: SAP is methodologically coherent, executable, and has no hard gate failure.
- `revise`: SAP has repairable deficiencies.
- `reject`: SAP has an unrecoverable fatal flaw under current conditions.
- `stop_no_gain`: revision failed to materially improve prior defects.
