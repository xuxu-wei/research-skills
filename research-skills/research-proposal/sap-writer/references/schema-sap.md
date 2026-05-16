# SAP Structure Requirements

This file defines the expected structure for SAP output. It is a validation aid, not content to paste into SKILL.md.

## Required metadata
- sap_file_path
- sap_version
- linked proposal_file_path, if available
- source context
- methodology/statistics preflight reference
- authoring date or version marker, if available

## Required content areas
- Study and analysis objectives
- Prespecified hypotheses and decision rules
- Estimand or analysis target, when applicable
- Endpoint or metric definitions
- Clinical data source and study design context, when applicable
- Clinically important feature inventory and descriptive statistics plan, when applicable
- Population and analysis sets
- Variables and covariates
- Prespecified primary analysis
- Prespecified secondary analyses
- Post hoc and exploratory analyses, clearly separated
- Missing data plan
- Sensitivity and robustness analyses
- Subgroup analyses, if applicable
- Multiplicity, if applicable
- Sample size or power, if applicable and supported
- Software and reproducibility notes
- Data governance and clinical data access constraints, when applicable
- Assumptions and limitations
- Unresolved SAP issues

## Validation notes
Missing required elements should be marked as unresolved issues rather than silently omitted or invented.

For clinical medical data analysis, validation must also confirm:
- clinical question, design context, data source, index date/baseline/follow-up windows are stated;
- endpoint ascertainment or coding/proxy definition is stated;
- clinically important baseline, disease, severity, treatment, comorbidity, care-context, and socioeconomic features are considered for descriptive statistics even when not used in modeling;
- features are labeled as descriptive only, candidate covariate/confounder, effect modifier/subgroup, stratification factor, or unavailable/unresolved;
- confounding, selection bias, censoring, competing risk, clustering, repeated measures, and measurement error are addressed when relevant;
- prespecified hypotheses are not mixed with post hoc or exploratory analyses;
- data-driven analyses are labeled and interpreted as exploratory.
