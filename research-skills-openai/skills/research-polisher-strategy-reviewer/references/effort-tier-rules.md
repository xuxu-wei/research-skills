# Effort-tier rules

## Shared requirement

Classify effort relative to the dossier's declared resources, access, and work ceiling. Do not use fixed day or budget thresholds across domains. Each cell must contain one option or `no_defensible_option`.

## `reposition_only`

Allowed:

- Change the contribution statement, claim hierarchy, story arc, audience, outlet archetype, title direction, discussion emphasis, or ordering/presentation of existing results.
- Redesign a display using already computed values without producing a new result.
- Add contextual citations that position an existing result without turning the citation work into a new research finding.

Forbidden:

- Any new statistical, computational, qualitative, subgroup, sensitivity, mechanism, validation, benchmark, or model analysis.
- Any new data collection, extraction, labeling, coding, adjudication, sample, experiment, replication, or external validation.
- Any claim that depends on evidence absent from the frozen source.

Require `added_work_items: []`. If repositioning cannot improve value without new evidence, return `no_defensible_option`.

## `small_extension`

Allow one bounded work package that uses existing assets or one narrow new validation. It must not change the core research question or design, require a new core cohort, or become a standalone study.

Require:

- feasibility `certain` or `high`;
- a dossier-grounded feasibility basis;
- named data, resource, technical, and time dependencies;
- a claim delta that depends only on the stated work;
- a failure fallback and stop condition.

## `moderate_extension`

Allow one coherent, bounded evidence layer such as an additional analysis family, validation module, mechanism experiment, robustness package, or translational assessment.

Forbid a new independent study, wholesale redesign, core sample reconstruction, open-ended data collection, or work whose feasibility cannot be defended from declared resources.

Require the same fields as `small_extension`, plus boundaries that show why the module remains an extension of the frozen research.

## Feasibility vocabulary

- `certain`: required assets and route are already verified.
- `high`: dependencies are identified and available with no unresolved blocker.
- `insufficient`: a material dependency or route remains unknown; this cannot be presented as a small/moderate option and must become `no_defensible_option` or a clarification request.
