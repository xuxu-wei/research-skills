# BMJ Statistical Review Standards

Distilled from Riley et al., *BMJ* 2022;379:e072883 — findings from an internal survey of BMJ statistical editors on the most common review issues. These 12 items apply primarily to methodological/statistical review and should be consulted when performing Step 7 (Methodological Review) and Step 9 (Simulated Reviewer Comments → Methodological/statistical expert).

For each item, applicability is noted: ⚕ Traditional (clinical statistics), 🤖 AI/ML (prediction models, machine learning), or ⚕🤖 Both.

---

## Design & Research Question

⚕🤖 **1. Unclear research question and estimand.** The most fundamental pitfall. Is the study descriptive, associative, causal, or predictive? For observational data, clarify whether the aim is causal inference, prognostic factor identification, or prediction model development. Define the target estimand explicitly — the population, treatments being compared, outcome measure, and summary measure. In AI/ML papers: distinguish prediction from causation; specify the prediction time point and clinical use scenario.

⚕🤖 **2. P-value fixation — ignoring estimates, confidence intervals, and clinical relevance.** Statistical significance ≠ clinical importance. A large trial may yield P < 0.001 with a risk ratio of 0.97 (trivial benefit); a small trial may yield P > 0.05 with a risk ratio of 0.70 (potentially large benefit). Report effect estimates with confidence intervals. Interpret in context of minimal clinically important differences (MCID). In ML papers: the parallel error is fixating on AUC to the exclusion of calibration, net benefit, and clinical utility.

## Data Handling

⚕🤖 **3. Inadequate handling of missing data.** Complete case analysis is rarely appropriate — it reduces power and may bias estimates. Report the amount and pattern of missing data. For RCTs: consider mean imputation or multiple imputation by group. For observational studies: multiple imputation is generally preferred. In ML: imputation choices affect both training and evaluation — never silently drop incomplete cases.

⚕ **4. Dichotomising continuous variables.** Splitting age, blood pressure, or biomarkers at arbitrary cut points wastes information, reduces power, and leads to non-replicable findings. Analyse continuous variables on their continuous scale. *Note: ML models naturally accommodate continuous features; this applies primarily to traditional analyses. For both: clinical interpretability may tempt dichotomisation — resist for primary analyses.*

⚕ **5. Assuming linear relationships.** Relationships between continuous covariates and outcomes are often non-linear. Use restricted cubic splines or fractional polynomials. *Note: tree-based methods and neural networks capture non-linearity by design; traditional regression requires explicit modelling. For both: report the functional form, don't just note that the model "handles it."*

## Analysis & Interpretation

⚕🤖 **6. Not quantifying subgroup differences.** A common mistake: concluding treatment works in subgroup A (P < 0.05) but not in B (P > 0.05), without testing the interaction. Always test and report the interaction effect. In ML: the parallel concern is fairness/equity auditing — model performance across subgroups must be explicitly compared.

⚕🤖 **7. Ignoring clustering in the data.** Patients nested within hospitals, repeated measures, or multi-trial meta-analyses introduce clustering that inflates type I error. Use cluster-robust SEs, multilevel models, or GEEs. ML models trained on clustered data without accounting for structure may produce overconfident predictions on new clusters.

⚕ **8. Inappropriate covariate adjustment — especially adjusted odds ratios.** In RCTs, covariate adjustment improves power and is encouraged, but adjusted odds ratios from logistic regression are not collapsible and differ from marginal odds ratios. Prefer adjusted risk differences or risk ratios. *Note: primarily a traditional statistics concern due to OR non-collapsibility; does not directly translate to most ML loss functions.*

## Prediction Models & AI/ML

🤖 **9. Assessing discrimination without calibration.** Most ML papers report only AUC but ignore calibration. A well-discriminating but miscalibrated model may be clinically harmful. Always report: calibration plots (loess-smoothed observed vs. predicted), calibration-in-the-large, calibration slope. Decision curve analysis assesses net benefit — more informative than AUC alone.

⚕🤖 **10. P-value-based variable selection.** Univariable screening based on unadjusted P values is inappropriate. In causal research: select confounders based on subject-matter knowledge and DAGs, not statistical significance. In prediction modelling: use penalisation (lasso, elastic net, ridge) rather than stepwise selection. *ML practitioners: document the feature selection rationale; avoid "throw everything in and let the model figure it out."*

⚕🤖 **11. Not assessing the sensitivity of results to assumptions.** Demonstrate that conclusions hold when key assumptions are varied. For ML: sensitivity to hyperparameter choices, train/test split, feature set, and population drift should be examined.

## Reporting

⚕🤖 **12. Incomplete reporting and overinterpretation.** Use reporting guidelines: CONSORT (RCTs), STROBE (observational), STARD (diagnostic), TRIPOD (prediction models), PRISMA (systematic reviews). For AI/ML: CONSORT-AI, TRIPOD-AI, STARD-AI. Avoid spin — unjustified claims of causality, generalisability, or clinical impact. Distinguish exploratory from confirmatory analyses.

---

## Reference

Riley RD, Cole TJ, Deeks J, et al. On the 12th Day of Christmas, a Statistician Sent to Me… *BMJ*. 2022;379:e072883. doi:10.1136/bmj-2022-072883
