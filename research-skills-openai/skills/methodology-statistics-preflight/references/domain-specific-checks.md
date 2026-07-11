# Domain-Specific Checks

Apply these checks selectively. Do not impose irrelevant domain rules on unrelated research types.

## Clinical, Biomedical, or Observational Research

Check:

- population and eligibility;
- exposure, intervention, comparator, or predictor;
- primary outcome and time window;
- confounding and bias risks;
- data source and variable availability;
- missing data and measurement error;
- data access, measurement, workflow, and tooling constraints;
- whether causal, predictive, descriptive, or exploratory claims are appropriate.

## Prediction Model or Machine Learning Study

Check:

- target label and prediction horizon;
- intended use case;
- training, validation, and test separation;
- leakage risk;
- class imbalance or outcome prevalence;
- performance metrics;
- calibration, discrimination, robustness, fairness, and external validation if relevant;
- sample size or event count relative to model complexity.

## Experimental Study

Check:

- experimental unit;
- intervention or condition;
- control or comparator;
- randomization or allocation if relevant;
- replication;
- outcome measurement;
- key confounders or nuisance variables;
- feasibility of materials, instruments, and timeline.

## Engineering Benchmark or Evaluation Study

Check:

- task definition;
- dataset or testbed;
- baseline methods;
- evaluation metrics;
- reproducibility requirements;
- failure cases;
- comparability with existing benchmarks;
- compute, tool, or platform constraints.

## Methods Study

Check:

- method objective;
- target problem class;
- comparator methods;
- synthetic or real data evaluation plan;
- assumptions;
- stress tests;
- limitations and failure modes.

## Qualitative or Mixed-Methods Study

Check:

- phenomenon of interest;
- sampling strategy;
- data collection method;
- analytic framework;
- credibility, dependability, reflexivity, or triangulation approach;
- integration logic for mixed-methods designs.
