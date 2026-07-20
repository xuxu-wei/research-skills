# Endpoint and Metric Checks

Use this file to assess whether the endpoint, outcome, metric, benchmark, or primary analysis target is sufficiently clear for downstream work.

## General Checks

A usable endpoint or metric should be:

- aligned with the research question or objective;
- measurable or observable;
- supported by the available data or planned data collection;
- specific enough to guide method choice;
- compatible with the intended output;
- not merely a vague value claim.

Calibrate specificity to the artifact stage. An Idea must identify the
scientific function, estimand or metric family, calculation inputs, comparison,
direction, decision timing, and failure meaning well enough to prevent
result-driven choice. It need not invent a universal numerical threshold or a
protocol-level implementation detail that can only be set after a declared data
audit, simulation, or pilot. Record that pending specification with an owner,
deadline, allowed information, and false consequence, and freeze it before the
relevant results are visible.

Do not force every systems, identification, or multi-task study into a single
clinical endpoint. A prespecified validation vector or hierarchy is acceptable
when each component has a unique role and the joint decision and multiplicity
rule are explicit. Conversely, `metric A or metric B` is not operational merely
because both are standard; either select one or state a result-blind selection
rule and its deadline.

## Common Failure Modes

- Endpoint is absent.
- Endpoint is named but not operationalized.
- Outcome cannot be measured in the proposed data source.
- Metric does not reflect the stated objective.
- Multiple endpoints compete without a primary target.
- Benchmark metric is standard but not appropriate for the task.
- Outcome timing is unclear.
- Unit of analysis is unclear.
- Target population or system is not matched to the metric.

## Repair Directions

- Define a primary endpoint, outcome, metric, benchmark, or analysis target.
- Specify measurement source and timing.
- Align endpoint with population, intervention/exposure, comparator, and method.
- Separate primary from secondary or exploratory metrics.
- Replace broad value claims with measurable outcomes.

## Domain Notes

- Clinical or observational studies usually need outcome definition, time window, population, exposure/comparator, and confounding-relevant variables.
- Prediction models need target label, prediction horizon, intended use, and performance metrics.
- Experiments need measurable response variables and control conditions.
- Benchmarks need task definition, dataset, baseline, metric, and failure criteria.
- Qualitative studies need a clear phenomenon, analytic focus, sampling logic, and trustworthiness criteria rather than quantitative endpoints.
