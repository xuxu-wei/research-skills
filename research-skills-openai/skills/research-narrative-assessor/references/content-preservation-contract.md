# Content-preservation contract

Use this mode only after editorial repair and in a fresh instance distinct from the
writer and assessor.

## Inputs

Read only the prior artifact, revised artifact, frozen protected-content register, and
writer's revision delta. Identify each by artifact ID, version, and path.

## Register enumerations

Declare every category using `source_status: source_present | source_absent`:

- `identity_and_question`
- `object_scope_and_boundaries`
- `inputs_and_resources`
- `design_analysis_and_inference`
- `claims_and_evidence_status`
- `assumptions_limitations_and_counterarguments`
- `unsupported_claim_classes`
- `source_intent_and_binding_constraints`

Every source-present category references one or more protected item IDs. Every
source-absent category has an empty list and a reason. Do not invent content or a
locator to populate an absent category.

Enumerate each protected scientific item with a source locator and exactly one required
disposition: `retained_same_meaning`, `retained_same_strength`,
`retained_once_at_authority`, or `retained_at_family_authority`. Preserve numerical and
temporal rules, branch eligibility, fallbacks, stopping consequences, failure
interpretations, assumptions, limitation families, and claim-strength boundaries when
present. Split an item when one locator becomes unreliable to check.

For a Perspective, give every protected counterargument or boundary item a
`family_id` and its authority locator. Preservation requires one complete occurrence
at that family's authority, not repetition across the artifact.

Permitted editorial operations are `replace`, `define`, `move`, `split`, `merge`,
`delete`, `reorder`, `add_bridge`, and `consolidate`. They may not change identity,
add unreviewed science, alter evidence status or claim strength, weaken an assumption
or limitation, or present planned work as completed.

## Decisions

- `scientific_content_preserved`: every protected item remains traceable with the same
  meaning and strength.
- `editorial_scope_violation`: an undeclared change exceeds editorial operations
  without changing the central identity.
- `identity_drift_detected`: a core question, thesis, object, scope, objective, or
  inference anchor changes.
- `scientific_change_declared`: the delta declares scientific change; return it to
  scientific review.

The preservation report contains exactly one check for every source-present protected
item, with no unknown or duplicate IDs. Do not judge whether the science is correct.
