# Perspective Editorial Repair Contract

Use this contract only after scientific revision and applicable panel routes have
closed on one frozen Perspective version. Editorial repair cannot change the thesis,
scope, claim strength, evidence status, source binding, or scientific meaning of a
counterargument or boundary.

## Entry binding

Bind the frozen Perspective by `{artifact_id, version, path}`, its exact
`writer_instance_id`, the complete embedded reader-reasoning handoff payload, and a
frozen protected-content register. Because the writer cannot read the manifest or
skeleton, copy that payload into the normalized repair brief. Do not require or
generate a digest. A legacy digest may be read and ignored.
Create the register with
`../../research-narrative-assessor/templates/protected-content-register.yaml` and
apply that skill's content-preservation contract; do not invent a reduced Perspective
register.

## Parallel assessment

Dispatch one fresh `research-narrative-assessor` with profile `perspective` and one
fresh `academic-language-assessor` against the same source version. Each sees only the
Perspective and the minimum handoff its own contract requires. They do not see each
other, scientific evaluator or panel material, repair history, scores, or decisions.

## One normalized brief

The controller reads the narrative repair plan and language assessment and writes one
`editorial-repair-brief-rNNN.yaml`.

- Include every actionable finding exactly once or record a blocking conflict.
- Preserve source finding IDs, locators, required content, protected content, and
  acceptance tests.
- Split actions when operations, locators, or scientific risks differ.
- Allow only `replace`, `define`, `move`, `split`, `merge`, `delete`, `reorder`,
  `add_bridge`, and `consolidate`.
- Language actions may contain a verified exact replacement. Narrative actions state
  a function and placement, not substitute wording.
- Name the counterargument/boundary family and single authority location whenever an
  action touches one. Do not create cross-references to omitted repetitions.
- If an action requires scientific judgment or changes protected content, return it to
  scientific revision or clarification instead of placing it in the brief.

Give the writer only the current Perspective, this brief, and the protected-content
register. Raw assessments and prior evaluations remain excluded.

## Same-writer repair and delta

The writer instance must equal the frozen source's `writer_instance_id`. If that
instance is unavailable, return `editorial_repair_pending` and stop. The writer saves
a new Perspective version, updated paragraph map, and YAML delta. Every action has one
disposition: `applied`, `not_applied_with_reason`, or
`scientific_change_required`. Undeclared edits are prohibited.

## Conformance, preservation, and reassessment

1. Run the deterministic conformance template. Require exact action coverage,
   acyclic dependencies, declared operations only, acceptance-test receipts, and
   complete Claim ID, Binding ID, terminology-order, and authority-family mappings.
   The template is fail-closed: change `decision` to `pass` only when every required
   check is true, no failure remains, and `scientific_change_declared` is false.
2. Dispatch a fresh narrative assessor in content-preservation mode. It reads only
   prior and revised Perspectives, the protected-content register, and the writer
   delta.
3. After `scientific_content_preserved`, dispatch fresh narrative and language
   reassessments in parallel against only the revised Perspective and their minimal
   handoffs. Do not give them prior reports or the delta.
4. Proceed only when conformance passes, content is preserved, narrative is
   `narrative_ready`, and language is `submission_ready`.

The final evaluator receives none of these artifacts.
