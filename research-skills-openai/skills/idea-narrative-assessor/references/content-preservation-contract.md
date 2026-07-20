# Content-preservation contract

## Contents

Inputs; protected content; decision rules.

Use this mode only after editorial repair. Run it in a fresh subagent distinct from
the writer and narrative assessor.

## Inputs

Read only:

- the prior dossier;
- the revised dossier;
- `protected-content-register.yaml` created before repair;
- the writer's revision delta.

Identify file artifacts by logical ID, version, and path. Do not require content
digests. Do not read preflight, evaluation, narrative assessment, workflow state, or
portfolio outputs.

## Protected content

Before repair, copy all five frontmatter `identity_anchor` values verbatim and
record every source-present study question, purpose, object and scope, boundary,
irreplaceable input, design and analysis commitment, measurement or inference
target, validation logic, claim scope and strength, working assumption,
limitation, contingency, and explicitly unsupported claim class. Give every
source-present protected item a source locator and required revised-artifact
disposition.

The current register schema separates category coverage from protected items.
Declare all seven categories in `category_coverage`. Use `source_present` with
one or more referenced protected-item IDs when the source contains that class.
Use `source_absent` with an empty ID list and a concise
`not_applicable_reason` only when the source genuinely contains no item in that
class. A simple Idea therefore need not invent an assumption, limitation, or
unsupported-claim class, and a source-absent category has no locator. Never use
`source_absent` to omit content that is present in the frozen dossier. The five
identity categories remain source-present, and the separate `identity_anchor`
mapping always contains exactly `primary_research_question`,
`primary_objective`, `study_object`, `core_data_or_evidence_base`, and
`primary_unit_of_inference`.

Historical v1 registers remain valid lineage records. New registers use v2 and
its explicit `register_id`, `register_version`, source-artifact identity,
identity-anchor, and category-coverage fields. The register version is the
logical artifact version used by downstream briefs; it is not a content digest.

The orchestrator owns and freezes this register. Every `source_locator` must
resolve inside the register's `source_artifact`, which is the prior authoritative
dossier supplied to the writer. Node state may be used to cross-check protected
values, but any binding user/context value that must survive repair is copied
explicitly into `protected_content`. When it was omitted from the prior dossier,
record its optional `source_context_locator` while keeping `source_artifact`
bound to the prior dossier. The frozen register then authorizes restoration of
that binding value; a preservation reviewer must not reclassify it as an
undeclared scientific addition merely because it was absent from the prior
dossier. The orchestrator resolves the context locator before freezing, so the
writer and preservation reviewer need not open another project artifact. Do not
create a locator that the orchestrator cannot resolve.
The narrative assessor validates and later compares the register; it does not
silently redefine protected science.

`protected_content` is not a category summary. For every cited source locator,
enumerate each numerical or temporal rule and, when present, each analysis
branch, dependency or precedence rule, fallback condition, stopping consequence,
failure interpretation, and claim-strength boundary whose omission would change
the science. When one locator is too dense to record reliably,
split it into additional protected items instead of compressing it into “all
thresholds” or “all stopping rules.” Conversely, keep related rules from the
same locator, semantic function, and required disposition in one enumerated
item; do not create one protected item per threshold by default. The writer still opens the locator; the
explicit register makes omission detectable before reassessment.

For a component with mutually exclusive or fallback branches, record shared
prerequisites separately from each branch's own eligibility and consequence.
Never turn a condition for one branch into a prerequisite for the whole
component, and never omit a fallback that remains available when another branch
fails. The writer and preservation reviewer must compare this branch logic at
the revised authoritative location, not infer it from the presence of isolated
phrases elsewhere.

The required revised disposition describes where the full protected meaning is
authoritative, not how many times it must be repeated. In particular,
`retained_once_at_authority_location` requires one complete occurrence. Other
mandatory sections retain only their own functional input, output, objective,
decision, or claim boundary; preservation does not require the complete branch
logic or limitation family to recur there.

Editorial changes may replace wording, define a concept, split or merge prose, reorder
material, move technical detail, consolidate duplicate limitations into the authority
location, add a bridge, or use a verified language-assessor replacement. They may not
change protected meaning, add data/method/results/evidence, strengthen a claim, present
planned validation as completed, hide a feasibility issue, weaken an assumption or
limitation, or turn a conditional element into an unconditional one.

In an editorial-only revision, compare the old and revised frontmatter
`identity_anchor` mappings field by field and require identical values. This
machine-facing record is copied verbatim even when the title or reader-facing
description is improved; paraphrasing it fails preservation until corrected.

## Decision rules

- `scientific_content_preserved`: every protected item remains traceable with the same
  meaning and strength, and all changes are editorial.
- `editorial_scope_violation`: an undeclared change exceeds the authorized editorial
  operations without clearly changing the study identity.
- `identity_drift_detected`: the central question, object, scope, purpose, or other
  identity anchor changes.
- `scientific_change_declared`: the delta explicitly declares a scientific change;
  return it to scientific review rather than deciding whether it is acceptable.

Report semantic comparison evidence and revised locators. Do not judge whether either
scientific design is correct. Only `scientific_content_preserved` may proceed directly
to fresh narrative and language assessment. The report must contain exactly one
check for every source-present `protected_id` in the frozen register, with no
duplicate or unknown IDs. Source-absent category declarations are coverage
evidence, not protected items, and therefore do not receive fictitious prior or
revised locators.

Validate the report:

```powershell
python scripts/validate_narrative_outputs.py --register <protected-register.yaml>
python scripts/validate_narrative_outputs.py --preservation <report.md> --register <protected-register.yaml>
```
