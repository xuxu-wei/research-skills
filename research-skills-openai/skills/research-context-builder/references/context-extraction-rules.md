# Context Extraction Rules

Normalize every starting point under one top-level type:

```yaml
input_type: problem
problem_subtype: broad_direction | raw_idea | clinical_problem | practical_problem | data_asset | method_asset | funding_call | literature_material | mixed | unclear
```

`input_type` remains `problem`; `problem_subtype` preserves the useful intake
distinction.

## Subtype focus

| Problem subtype | Primary extraction focus |
|---|---|
| `broad_direction` | domain, goal, audience/output, constraints, evidence need |
| `raw_idea` | question, objective, object, data, method, endpoint/metric |
| `clinical_problem` | population, setting, decision need, endpoint, data, evidence need |
| `practical_problem` | stakeholder, setting, value need, feasible data, metric |
| `data_asset` | access, population/system, variables, provenance, limitations |
| `method_asset` | maturity, target use, validation route, data requirements |
| `funding_call` | sponsor goal, eligibility, deliverable, constraints, review criteria |
| `literature_material` | supplied sources, topic, unresolved questions, mapping need |
| `mixed` | all applicable fields plus material ambiguities |
| `unclear` | missing information and the smallest useful clarification |

## Extraction order

1. User goal, intended audience, and output.
2. Research question, object, setting, and intended contribution.
3. Available data/evidence, access, provenance, and limitations.
4. Available methods and maturity.
5. Endpoint or metric status.
6. Time, resources, access, collaboration, and other binding constraints.
7. Supplied evidence materials.
8. Facts, assumptions, uncertainties, and impact if wrong.
9. Direction clarity and downstream needs.

Set endpoint/metric status to `clear`, `partially_clear`, `unclear`, or
`not_applicable`. Characterize direction clarity as `clear`, `underdefined`, or
`ambiguous`. Do not judge evidence quality, value, novelty, feasibility,
publishability, or promotion; route those tasks downstream.
