# Context Extraction Rules

## Input Type Classification

Classify the user's starting point before extraction.

| Input type | Indicators | Primary extraction focus |
|---|---|---|
| `broad_direction` | broad field, theme, disease area, technique, or problem space | domain, goal, intended output, constraints, evidence need |
| `raw_idea` | a proposed study, hypothesis, or project concept | research question, target object, data, method, endpoint/metric clarity |
| `clinical_problem` | patient care, diagnosis, treatment, prognosis, guideline, implementation issue | population, clinical setting, endpoint, data source, evidence need |
| `practical_problem` | workflow, operational, engineering, education, or implementation issue | stakeholder, value need, setting, feasible data, metric |
| `data_asset` | dataset, registry, cohort, EHR, lab data, images, text corpus | data access, variables, population/system, limitations, possible endpoints |
| `method_asset` | technique, model, assay, algorithm, platform, framework | method maturity, target use case, validation route, data requirement |
| `funding_call` | grant topic, RFA, sponsor priority, call text | funder goal, eligibility, required deliverable, constraints, review criteria |
| `literature_material` | review, paper, guideline, report, bibliography | evidence materials provided, topic, unresolved questions, downstream evidence mapping |
| `mixed_input` | multiple categories present | extract all relevant fields and flag ambiguity |
| `unclear` | too little information to classify | produce clarification request or insufficiency report |

## Extraction Priorities

Extract in this order:

1. User goal and intended output.
2. Research domain and study object.
3. Available data and access status.
4. Available methods and maturity.
5. Endpoint/metric constraints.
6. Time, resource, access, method, and collaboration constraints.
7. Evidence materials provided.
8. Known facts, assumptions, and uncertainties.
9. Downstream needs.

## Evidence Materials

Only record whether evidence materials exist and what type they are. Do not judge quality, novelty, or guideline alignment. Those tasks belong to `research-opportunity-mapper`.

## Endpoint/Metric Handling

Record endpoint/metric status as:

- `clear`: explicitly defined and aligned with the research object.
- `partially_clear`: plausible but underspecified.
- `unclear`: missing, ambiguous, or inconsistent.
- `not_applicable`: not relevant to the task type.

Do not validate endpoint/metric feasibility. That belongs to `methodology-statistics-preflight`.
