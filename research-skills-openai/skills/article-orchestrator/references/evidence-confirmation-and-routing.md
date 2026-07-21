# Evidence Confirmation and Routing Rules

Rules for confirming user-provided evidence materials and routing to `research-landscape-mapper` when evidence is insufficient.

## Evidence Confirmation Flow

### At Workflow Start (Standard Entry)

1. Ask the user what evidence materials they have:
   - Study protocol or SAP
   - Primary results (numerical, tables, figures)
   - Statistical outputs
   - Prior publications or preprints
   - Literature review materials
   - Data availability statement

2. Classify evidence status:
   - `user_provided_sufficient`: All major evidence types present → proceed
   - `user_provided_partial`: Some evidence present, some gaps → proceed with assumptions, note gaps
   - `user_provided_minimal`: Very limited evidence → flag in scope_limitations; readiness triage may block

3. Record evidence status in context brief: `data_summary.data_completeness`.

### Evidence Gate Before Literature Grounding

Before Step 3 (Literature Grounding), check:
- Does the user have a clear research question with contextual literature?
- Do they have competing or contradictory evidence awareness?
- Is the novelty claim grounded in literature comparison?

If any answer is "no", `article-literature-grounder` must attempt retrieval.

### Evidence Gate Before Claim Audit

Before Step 9 (Claim Audit), check:
- Does every claim in the manuscript have a traceable evidence source?
- Are there claims based on user assertion without data?

If claims lack evidence sources, mark them in the Evidence Provenance Ledger as `verification_status: user_supplied_unverified` or `inferred`.

## Evidence-change routing

For literature gaps, `[evidence]` findings, missing seminal or competing work,
or an unverified novelty position, first record `evidence_change_assessment`:

- `none`: reuse the current grounding and relink claims if needed;
- `bounded`: use Built-in Search for exact citations or one claim, or
  `focused-literature-synthesizer` for a 2-5-paper close synthesis;
- `major`: call `research-landscape-mapper` for a core-claim, novelty,
  landscape, or material-conflict rebuild.

Language and editorial revision never triggers retrieval. Do not combine
several focused syntheses into a broad grounding rebuild.

### Landscape Mapper Invocation Pattern

Invoke `research-landscape-mapper` as a named skill using the host's native skill mechanism.

Provide:
- Research question and domain
- Specific evidence needs (gap literature, competing evidence, comparison studies)
- Scope constraints
- Prior search results (to avoid duplication)

### Post-Mapper Integration

- Newly retrieved evidence → update Literature Grounding Report
- New evidence → update Evidence Provenance Ledger with `verification_status: verified`
- Evidence retrieval does not consume a revision round

## Evidence Sufficiency by Study Type

| Study Type | Minimum Evidence | Recommended |
|------------|-----------------|-------------|
| RCT | Primary endpoint results, safety data, baseline table | Protocol, SAP, secondary endpoints, subgroup |
| Observational | Adjusted association estimates, baseline by exposure, sensitivity | DAG, E-value, negative control |
| Diagnostic | Sensitivity/specificity, reference standard, participant flow | ROC, decision curve, subgroup performance |
| Prediction model | Discrimination, calibration, predictors, sample size | External validation, DCA, missing data handling |
| Systematic review | Search strategy, study characteristics, risk of bias, forest plot | PRISMA checklist, GRADE, funnel plot |
| Mechanistic | Phenotype, perturbation, rescue, validation | Raw data, reagent info, full experimental conditions |
| AI/ML | Benchmark table, ablation, training details, data description | Code, environment, error analysis, generalization test |
| Qualitative | Themes, participant quotes, coding framework | Reflexivity, saturation, deviant cases |
