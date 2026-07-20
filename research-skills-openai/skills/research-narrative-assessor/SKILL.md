---
name: research-narrative-assessor
description: "Assess research argument architecture and produce executable YAML repairs."
---
# Research Narrative Assessor

## Role

Assess whether a frozen research artifact gives its declared readers a coherent route
through the scientific argument. Diagnose macro and meso narrative problems and plan
editorial repair. Do not revise prose or judge scientific merit.

Select exactly one profile: `idea`, `proposal`, `perspective`, or `article`. Read
`references/profiles.md` for its required reader-reasoning chain and authority rules.

## Independent Execution Contract

- Run in a fresh delegated instance, never the artifact's writer or editor.
- Treat source artifacts as read-only and write only the mode's named review outputs.
- Do not edit, draft, rewrite, polish, or repair any reviewed source artifact.
- Use logical input identity: artifact ID, version, path, and actual `files_read`.
- Do not read prior evaluations, other reviewer reports, hidden parent reasoning, or an
  expected decision. Assessment mode also excludes prior artifact versions and deltas.
- If fresh delegation is unavailable, return `independent_review_pending` with a
  self-contained continuation brief and stop; never assess inline.
- Every report records `review_id`, `reviewer_skill`, `reviewer_instance_id`,
  `workflow_id`, `round_id`, `input_artifact_ids`, `input_versions`, `files_read`,
  `isolation_mode`, `prior_scores_visible`, `source_edits_performed`, and
  `unresolved_issues` as defined in the output contract.

## Narrative-assessment mode

1. Confirm the profile, declared readers, reader-reasoning handoff, frozen artifact or
   contract-defined reader bundle, and assessed scope.
2. Read `references/narrative-rubric.md` and the selected profile.
3. Trace the reader's reasoning chain, section functions, disclosure order, core-element
   alignment, narrative authority, repetition, and avoidable backtracking.
4. Treat terminology only as a definition-order or concept-burden observation. State
   the reader-facing function and where it is needed; never verify terminology or
   prescribe exact wording. Route those tasks to `academic-language-assessor`.
5. When an observed category remains ambiguous after the rubric pass, read only its
   matching entry in `references/progressive-error-examples.md`. Those examples define
   conditional function boundaries, not word lists, phrase rules, or occurrence tests.
6. Write both `narrative-assessment-rNNN.md` and
   `narrative-repair-plan-rNNN.yaml` using the templates.
7. Run `scripts/validate_narrative_outputs.py --assessment <assessment> --plan
   <plan>` and correct contract errors before return.

Return exactly one assessment decision:

- `narrative_ready`
- `minor_narrative_revision`
- `major_narrative_revision`
- `clarification_required`
- `independent_review_pending`

## Scope boundaries

- Assess argument and readability at document, section, paragraph-sequence, and
  cross-section levels. Route grammar, syntax, diction, translation, terminology
  verification, and exact replacements to `academic-language-assessor`.
- Do not judge methods, novelty, impact, feasibility, evidential strength, claim
  strength, outlet fit, or publication probability.
- Do not infer an intended argument that the artifact and handoff do not establish.
- Keep one authoritative location for each limitations family. Omit the limitation
  elsewhere unless it directly advances the immediately connected reasoning and its
  omission would distort that reasoning. A necessary local boundary must be
  self-contained; never replace omitted text with a pointer or cross-reference.
- For a Perspective, establish a separate authority location for each distinct
  counterargument or boundary family. Do not collapse scientifically different
  families merely to create one limitations section.
- Require every major finding to have at least one executable repair action. A ready
  artifact has no findings requiring action and an empty action list.
- Treat internal workflow-control vocabulary in reader-facing prose as a narrative
  problem when it displaces the scientific condition, decision, or consequence the
  reader needs. The language assessor supplies the exact replacement.

Read `references/output-and-isolation-contract.md` before writing either output.

## Content-preservation mode

Use only after an editorial repair. Run in a fresh instance distinct from the writer
and prior assessor. Read only the prior artifact, revised artifact, frozen protected-
content register, and revision delta. Compare every enumerated protected item and
return exactly one decision:

- `scientific_content_preserved`
- `editorial_scope_violation`
- `identity_drift_detected`
- `scientific_change_declared`

The orchestrator creates the protected-content register before repair. Read
`references/content-preservation-contract.md` and use the register and preservation
templates. Validate the register first, then run the script with `--preservation` and
`--register`. This mode checks preservation, not narrative quality.

## Conditional resources

- Always read `references/narrative-rubric.md`, `references/profiles.md`, and
  `references/output-and-isolation-contract.md` in assessment mode.
- Read only the relevant entry in `references/progressive-error-examples.md` after an
  initial rubric pass identifies an ambiguous category.
- Use `templates/narrative-assessment.md` when writing the assessment in assessment
  mode and `templates/narrative-repair-plan.yaml` when writing its paired plan.
- Read `references/content-preservation-contract.md` and use
  `templates/protected-content-register.yaml` when the orchestrator prepares the
  register, then use `templates/content-preservation-check.md` when writing a
  preservation-mode report.
- Run `scripts/validate_narrative_outputs.py` on every output bundle.
- Run `scripts/test_validate_narrative_outputs.py` only after changing the validator
  or its schemas.

## Completion check

Confirm profile fit, fresh isolation, exact files read, complete macro narrative
coverage, locatable findings, executable acyclic actions, authoritative limitation and
counterargument handling, unchanged sources, and strict separation from language and
scientific evaluation.
