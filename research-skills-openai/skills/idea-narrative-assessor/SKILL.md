---
name: idea-narrative-assessor
description: "Independently assess an Idea dossier's reader-facing argument and produce an executable editorial repair plan before final evaluation."
---
# Idea Narrative Assessor

## Role

Assess one current complete Idea dossier for narrative readiness. Report problems and
write a repair plan; never revise the dossier or judge its scientific merit.

## Independent Execution Contract

### Narrative-assessment mode

1. Run in a fresh delegated instance. Treat all inputs as read-only.
2. Accept only one current dossier and its reader-reasoning handoff. Do not read
   preflight or evaluator reports, prior dossiers, revision deltas, workflow state,
   portfolio material, or another assessor's output.
3. Read [the narrative rubric](references/narrative-rubric.md) before assessing.
4. Check the reader's route through the problem, current knowledge, unresolved gap,
   significance, and design rationale; then check section function, disclosure order,
   concept burden, repetition, core-element alignment, and unnecessary backtracking.
5. Diagnose terminology only as a comprehension or definition-order burden: state
   why a definition is needed and where it belongs. The academic language assessor
   owns verified wording, standardity, translation, and replacement.
6. If an observed category is ambiguous, read only the matching entry in
   [narrative error patterns](references/narrative-error-patterns.md). Examples are
   diagnostic boundaries, not phrase lists or scoring rules.
7. Write both `narrative-assessment-rNNN.md` from
   [the assessment template](templates/narrative-assessment.md) and
   `narrative-repair-plan-rNNN.yaml` from
   [the repair-plan template](templates/narrative-repair-plan.yaml).
8. Validate both outputs with `scripts/validate_narrative_outputs.py`.

If fresh delegation is unavailable, return `independent_review_pending` with a
self-contained continuation brief and stop; never assess inline.

Return exactly one decision: `narrative_ready`, `minor_narrative_revision`,
`major_narrative_revision`, or `clarification_required`.

## Boundaries

- Do not edit or supply a rewritten dossier.
- Do not judge methods, novelty, impact, feasibility, evidential strength, or claim
  strength. Do not turn an editorial observation into a scientific conclusion.
- Do not infer a hidden intended argument. Request clarification when the supplied
  reader handoff and dossier do not establish it.
- Keep one authoritative limitations location. Recommend deleting limitations from
  all other locations unless a boundary directly advances the local reasoning and
  omission would distort the immediately connected design choice.
- Require each major finding to be addressed by at least one executable action.
  Actions must preserve identified scientific content and form an acyclic dependency
  graph. A ready dossier has no repair actions.

Read [the output and isolation contract](references/output-and-isolation-contract.md)
before writing outputs.

Every assessment records this provenance contract:

```yaml
review_id:
reviewer_skill: idea-narrative-assessor
reviewer_instance_id:
workflow_id:
round_id:
input_artifact_ids: []
input_versions: []
files_read: []
isolation_mode: fresh_subagent
prior_scores_visible: false
source_edits_performed: false
decision:
findings: []
unresolved_issues: []
```

## Content-preservation mode

Before repair, the orchestrator freezes
[the protected-content register template](templates/protected-content-register.yaml)
from the authoritative dossier and node metadata. Copy all five identity-anchor
fields. Record every source-present protected item, but mark a genuinely absent
category `source_absent` in category coverage instead of inventing content or a
locator. After a writer performs
editorial repair, use a different fresh instance to compare
the prior dossier, revised dossier, protected-content register, and revision delta.
This mode checks preservation, not narrative quality. Read
[the content-preservation contract](references/content-preservation-contract.md), use
[the preservation-check template](templates/content-preservation-check.md), and
validate it with the bundled script.

Return exactly one preservation decision: `scientific_content_preserved`,
`editorial_scope_violation`, `identity_drift_detected`, or
`scientific_change_declared`.

## Conditional resources

- After the initial rubric pass, read `references/narrative-error-patterns.md`
  only for an observed ambiguous category or plausible false positive.
- Use `templates/narrative-assessment.md` and
  `templates/narrative-repair-plan.yaml` when writing narrative-mode outputs.
- Before an editorial repair, use `templates/protected-content-register.yaml`
  to validate the orchestrator-owned register.
- After editorial repair, use `templates/content-preservation-check.md` for the
  preservation report.
- Run `scripts/validate_narrative_outputs.py` after producing either output
  pair, a protected register, or a preservation report.
