# Minimal Analysis Route Rules

This file defines the boundary between preflight and full analysis planning.

## What Counts as a Minimal Analysis Route

A minimal analysis route is a short, plausible outline showing how the research question could be answered. It should include:

- target population, system, dataset, sample, or study object;
- endpoint, outcome, metric, benchmark, or primary analysis target;
- key exposure, intervention, predictor, design factor, method, or comparison if applicable;
- minimal data preparation or measurement requirement;
- primary analytic approach or design logic;
- at least one way to check robustness, validity, error, bias, or uncertainty when relevant.

## What Is Not Required

Do not require a full SAP or full protocol. Preflight does not need:

- full model formula;
- complete covariate list;
- complete sample size calculation;
- code;
- final reporting checklist compliance;
- final table shells;
- final submission language.

## Pass Standard

Preflight can pass when a credible minimal route is fully specified at preflight
resolution. If a remaining detail is needed to execute that route, conditional pass is
allowed only through `proceed_with_assumptions` with a specific bounded assumption
explicitly accepted in the report and designated for one occurrence in the downstream
artifact's authoritative `Assumptions` location. Do not delegate an unspecified choice
to a writer, evaluator, statistician, or domain expert.

## Failure Standard

Preflight should fail if no coherent route exists without inventing new data, endpoints, variables, experimental conditions, or design assumptions.

## Repair Directions

- Define the missing endpoint or metric.
- Specify data source and key variables.
- Narrow or reframe the question.
- Change method to fit available data.
- Add minimal validation, baseline, comparator, or sensitivity plan.
- Move to user clarification when assumptions would materially alter the study.
