# SAP Fatal Flaws

Fatal flaws are defects that can invalidate or block the SAP unless corrected.

## Common Fatal Flaws

- Primary endpoint is undefined.
- Analysis population cannot be determined.
- Primary analysis is absent or not executable.
- Statistical method does not match endpoint type or data structure.
- Data cannot support the proposed primary analysis.
- SAP contradicts the proposal or stated objective.
- Clinical data source, index date, follow-up window, or endpoint ascertainment is missing when required to execute the analysis.
- Clinically important population features are omitted from the descriptive statistics plan, preventing interpretation of study population, generalizability, or baseline comparability.
- Prespecified and post hoc/exploratory analyses are mixed such that confirmatory claims cannot be identified.
- Exploratory or data-driven analyses are presented as confirmatory evidence.
- Key variable definitions are missing.
- Confounding or bias is material and unaddressed.
- Missing data is likely material and unaddressed.
- Sensitivity analysis is absent where assumptions are central.
- Core assumptions are untestable, implausible, or incompatible with available data.
- The plan requires data, sample size, timing, or measurements not available.

## Repairability

Classify each fatal flaw as:

- `repairable`: can be fixed with available information and targeted revision.
- `needs_user_input`: requires missing facts from user or study team.
- `blocked`: cannot be fixed under current design or data conditions.
