# Clinical Data Analysis SAP Rules

Use these rules when the SAP concerns clinical medicine, public health, EHR, registry, claims, trial, diagnostic, prognostic, or prediction-model data.

## Required clinical data context

The SAP should state:
- study design context: trial, observational cohort, case-control, cross-sectional, diagnostic, prediction, registry, EHR, claims, or mixed source;
- data source, provenance, extraction date, and linkage sources if applicable;
- coding systems or source instruments used for diagnoses, procedures, medications, laboratory values, symptoms, and outcomes;
- index date or baseline definition;
- baseline, exposure, outcome, and follow-up windows;
- censoring, loss to follow-up, death, competing risk, transfer, or disenrollment rules when relevant;
- unit of analysis: patient, encounter, episode, lesion, sample, site, provider, or cluster.

## Endpoint and variable definition

Clinical endpoints must include:
- clinical meaning and measurement source;
- ascertainment method: adjudicated, coded, chart-reviewed, device-measured, laboratory-derived, patient-reported, registry-derived, or proxy;
- validation status or known limitations;
- timing and hierarchy when multiple data sources can define the endpoint;
- minimal clinically important difference or clinically meaningful threshold when available.

Variables must include derivation rules for:
- exposure/intervention/predictor/comparator;
- covariates and confounders;
- time-varying variables;
- baseline values and changes from baseline;
- composite endpoints and component endpoints.

## Clinically important features and descriptive statistics

The SAP writer must actively infer clinically important features from the research question, disease area, exposure/intervention, endpoint, and care context. These features should be considered for descriptive statistics even when they are not part of the primary model.

Common feature groups:
- demographics: age, sex/gender, race/ethnicity, region, socioeconomic context when relevant and appropriate;
- disease state: diagnosis, subtype, duration, severity/stage, baseline risk, prior events, baseline symptoms/function, biomarkers, laboratory values, imaging or physiologic measures;
- treatment history: prior treatment, concomitant therapy, medication class, dose/intensity, adherence, procedural history;
- care context: site, provider, care setting, calendar period, treatment era, referral pathway;
- comorbidities and competing risks: clinically important chronic conditions, frailty, pregnancy status, renal/hepatic function, immunosuppression, or mortality risk when relevant;
- data context: availability, missingness, measurement frequency, coding reliability, and validation status.

For each important feature, state its role:
- `descriptive only`: summarize to characterize the cohort, not used in inferential modeling;
- `candidate covariate/confounder`: may be adjusted for if justified by design or causal/prediction objective;
- `effect modifier/subgroup`: may define a subgroup or interaction;
- `stratification factor`: used for design or reporting strata;
- `not available/unresolved`: clinically relevant but unavailable or insufficiently defined.

Do not automatically include all clinically important features in the primary model. Descriptive importance and adjustment necessity are separate decisions.

## Bias and design risks

Address when relevant:
- confounding by indication;
- selection bias;
- immortal time bias;
- informative censoring;
- competing risks;
- measurement error and misclassification;
- site/provider clustering;
- repeated measures and within-patient correlation;
- calendar time, secular trends, and treatment era;
- diagnostic verification bias;
- leakage in prediction models.

## Interpretation

Clinical SAP language should distinguish:
- statistical significance from clinical importance;
- association from causation unless design supports causal inference;
- prediction performance from clinical utility;
- internal validation from external validation;
- exploratory signal from confirmatory evidence.
