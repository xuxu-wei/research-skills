# Feasibility Blockers

Use this file to identify blockers that prevent a methodology-statistics preflight pass.

## Blocking Issues

Mark as `blocked` when one or more of the following cannot be repaired within the current information or constraints:

- research question is not answerable by any plausible method under the constraints;
- endpoint, outcome, metric, or benchmark cannot be defined;
- data source cannot support the primary endpoint or method;
- required variables, labels, measurements, controls, baselines, or experimental conditions are unavailable;
- proposed method does not match the question or data;
- causal interpretation is central but no plausible identification strategy exists;
- time, resource, data access, privacy, ethics, or regulatory constraints prevent execution;
- sample size, event count, measurement density, or data volume is clearly insufficient for the intended method;
- missingness, bias, confounding, leakage, or measurement error is severe and unaddressable;
- minimal analysis route cannot be specified without inventing facts.

## Repairable Issues

Use a revision decision rather than `blocked` when a plausible fix exists:

- endpoint needs operationalization;
- metric should be changed;
- method should be simplified;
- data source should be narrowed or replaced;
- analysis route should shift from confirmatory to exploratory;
- causal claim should be reframed as association or prediction;
- benchmark needs baseline or validation plan.

## Reporting Requirements

For each blocker, state:

- blocker type;
- why it matters;
- whether it is repairable;
- minimal repair direction;
- whether user clarification is required.
