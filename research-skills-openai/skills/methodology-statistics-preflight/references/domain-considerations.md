# Domain considerations

Read only the parts relevant to the study; these are prompts for scientific judgment.

## Clinical and observational studies

Align the target population, time origin, exposure or treatment, comparison, outcome, follow-up, and intended estimand. Consider selection, confounding, measurement error, loss to follow-up, competing events, and changes in treatment where relevant.

Check whether adjustment variables are justified by subject-matter knowledge and the causal question. Automatically adjusting for every available variable can introduce bias. Sensitivity analyses should probe assumptions that could change the conclusion.

## Prediction and machine learning

Match validation to the intended use and population. Prevent leakage across preprocessing, feature selection, tuning, and evaluation. Account for repeated observations, sites, time, and other dependence when splitting data.

Assess calibration, discrimination, uncertainty, and performance across relevant groups. External validity and practical utility require evidence beyond an improvement on one benchmark. Compare against credible baselines.

## Experiments and benchmarks

Distinguish biological or independent experimental units from technical replicates. Examine randomization, blinding, controls, batch effects, measurement reliability, and the match between the analysis and allocation.

For computational comparisons, use comparable data, tuning opportunities, evaluation conditions, and uncertainty estimates. A favorable metric alone does not establish a useful scientific advance.

## Qualitative and mixed-methods research

Match sampling, data generation, analysis, and interpretation to the question and methodological tradition. Consider reflexivity, the credibility of interpretations, negative cases, and how evidence supports the account.

For mixed methods, explain what integration contributes. Do not impose statistical power or numerical representativeness as universal quality criteria.

## Information and feasibility

Use a sample-size or precision rationale appropriate to the question and design, with assumptions visible. When necessary quantities are unknown, identify a pilot, sensitivity range, or information-gathering step rather than fabricating precision.

Check that endpoints and metrics represent the phenomenon of interest and can be measured at the relevant time. Address missingness through plausible mechanisms and appropriate analyses; no single imputation method is a universal remedy.
