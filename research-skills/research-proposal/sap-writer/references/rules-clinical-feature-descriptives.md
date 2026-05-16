# Clinical Feature Descriptives Rules

Use this file when drafting SAPs for clinical medicine, public health, registry, EHR, claims, diagnostic, prognostic, or prediction studies.

## Required behavior

When `sap-writer` is invoked, it must actively infer which clinical features are likely important for describing the study population from:
- research question and primary endpoint;
- disease area and natural history;
- exposure, intervention, predictor, comparator, or grouping;
- clinical care pathway and setting;
- known prognostic factors, treatment-selection factors, and outcome ascertainment factors;
- data source and available variable classes.

These features should be included in a descriptive statistics plan even if they are not included in the primary model.

## Feature inventory

For each feature or feature group, record:
- feature name;
- clinical rationale;
- source and derivation;
- expected missingness or availability;
- role: `descriptive only`, `candidate covariate/confounder`, `effect modifier/subgroup`, `stratification factor`, or `not available/unresolved`.

## Typical clinical feature groups

- Demographics: age, sex/gender, race/ethnicity or region when relevant and appropriate.
- Disease characteristics: diagnosis/subtype, duration, severity/stage, baseline risk, prior events, symptoms/function, biomarkers, laboratory values, imaging or physiologic measures.
- Treatment and care: prior treatment, concomitant therapy, medication/procedure history, adherence, site/provider, care setting, calendar period or treatment era.
- Comorbidities and competing risks: chronic conditions, frailty, renal/hepatic function, immunosuppression, pregnancy status, mortality risk.
- Data characteristics: measurement frequency, variable completeness, coding reliability, validation status.

## Descriptive statistics plan

Specify descriptive summaries for:
- total cohort;
- exposure/intervention/comparator or outcome-relevant groups when useful;
- clinically meaningful strata when they clarify generalizability or imbalance;
- key feature missingness.

Default summaries:
- continuous variables: mean (SD) and median (IQR) when distribution is uncertain; range when clinically useful;
- categorical variables: n/N (%);
- follow-up: median (IQR), minimum/maximum, person-time when relevant;
- time-to-event availability: number with event, censored, competing event, and follow-up duration when relevant.

## Boundaries

- Do not convert every descriptive feature into an adjustment variable.
- Do not choose descriptive features only because they are available; tie them to clinical rationale.
- Do not omit clinically important unavailable features; list them as unresolved if their absence affects interpretation.
- Do not use descriptive imbalance alone as proof of confounding without design rationale.

