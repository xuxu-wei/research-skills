# Data-Method Fit Rules

Use this file to judge whether the available or planned data can support the proposed method, study design, or analysis route.

## Core Fit Questions

- Does the data contain the variables, labels, measurements, texts, images, signals, logs, samples, or experimental conditions needed to answer the question?
- Is the unit of analysis clear?
- Is the sample, cohort, dataset, or system aligned with the target population or object?
- Does the data structure support the proposed method?
- Are timing, follow-up, repeated measures, or temporal ordering sufficient when relevant?
- Are comparator, control, baseline, or reference conditions available when required?
- Are missingness, measurement error, selection bias, confounding, leakage, or label quality concerns addressed at least minimally?

## Common Fit Failures

- Method assumes variables not present in the data.
- Causal claim is proposed using data without plausible causal identification strategy.
- Prediction model lacks a clear label or prediction horizon.
- Experimental claim lacks control or replication.
- Benchmark claim lacks baseline, dataset, or metric.
- Generalization claim exceeds the sampling frame.
- Data access is speculative or blocked.
- Privacy, ethics, or regulatory constraints prevent required data use.

## Repair Directions

- Narrow the research question to match available data.
- Replace the method with one supported by the data.
- Define required variables and data acquisition path.
- Add comparator, control, baseline, validation set, or measurement plan.
- Reframe as feasibility, descriptive, exploratory, simulation, benchmark, or methods study if confirmatory analysis is unsupported.
