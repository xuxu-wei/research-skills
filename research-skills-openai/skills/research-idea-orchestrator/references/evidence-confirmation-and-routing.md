# Evidence Confirmation and Routing

Load this reference when deciding how supplied materials should enter context
and opportunity mapping.

## Intake

- If the user already supplied literature, reports, standards, datasets, calls,
  or prior evidence work, record their exact paths or source locators and do not
  ask for them again.
- If no usable evidence is supplied, route retrieval and mapping to
  `research-landscape-mapper`.
- Treat a single research article as a hypothesis-generating source, not a field
  consensus or novelty verdict. Verify its proposed gap against broader sources.
- Do not let the orchestrator or context builder judge evidence quality,
  novelty, value, or guideline alignment.

## Mapper brief

Ask the mapper to distinguish:

- established findings, live disputes, and unresolved gaps;
- closest prior work and the current Idea's honest incremental value;
- data, measurement, validation, implementation, and audience opportunities;
- source-backed direction signals and their confidence;
- claims that remain unverified or need qualification.

Use built-in Search for current, exact, or bounded retrieval. Use Deep Research
for genuinely multi-stage or multi-direction synthesis; if it is unavailable,
return its normal handoff state rather than simulating it.

## Confidence labels

- `high`: several directly relevant, credible sources agree.
- `moderate`: direct support exists but coverage or agreement is limited.
- `low`: support is indirect, sparse, or conflicting.
- `not_verified`: retrieval or source verification is incomplete.

Low or conflicting direction signals require
`direction_route_confirmation_required`. No defensible direction returns
`no_defensible_direction`.

The complete dossier must restate all evidence needed for independent review
using normal academic citations. Maps and internal IDs never substitute for
dossier evidence.
