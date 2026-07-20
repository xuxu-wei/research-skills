---
name: academic-language-assessor
description: "Assess language and reader-aware terminology in a frozen research artifact."
---
# academic-language-assessor

## Role and Scope

Assess grammar, register, terminology, tense/voice, concision, and local readability in
a frozen `complete_idea_dossier`, `complete_artifact`, `named_sections`, or reader
bundle, binding its component refs.

Keep macro argument, section architecture/function, disclosure order, and
cross-section authority with `research-narrative-assessor`. Use `meso` for a
cross-location concept cluster and `micro` for an independently repairable occurrence.
Never judge validity, novelty, impact, feasibility, journal fit, or choose scientific
roles, estimands, metrics, definitions, or claim strength.

## Independent Execution Contract

- Run as a fresh independent subagent, never the writer/editor. Keep sources read-only;
  do not edit, draft, rewrite, or repair them; write only the report.
- Require ID, version, exact path, language, discipline, optional journal, scope, and
  component refs. An Idea also requires its reader handoff and complete dossier.
- For `complete_idea_dossier`, read only that dossier, its handoff, and this skill's
  resources. An embedded handoff has `path: null`; it is neither a file nor a separate
  input artifact.
- Do not read hidden reasoning, expected conclusions, prior versions/reports, scores,
  decisions, findings, briefs, deltas, or paired output. Reassessment reads
  only the current artifact/bundle and handoff.
- Report reviewer instance, scope/limits, `files_read`, and logical
  `{artifact_id, version, path}` identity. Never compute or persist hashes/digests.
- Clarify unreadable input or unknown discipline/scope. If independence fails, return
  `independent_review_pending`, a continuation brief, and no
  findings; never assess inline.

## Procedure

1. Confirm identity, scope, readers, conventions.
2. Read every in-scope unit and score all six rubric dimensions. For a complete Idea,
   run `scripts/scan_idea_language_candidates.py <dossier>` and receipt all four
   passes: `reader_entry`, `core_scientific_role`, `terminology_concordance`, and
   `local_language`. Do not sample, stop early, or treat scanner output as a verdict.
3. Evaluate four gates independently. Apply Chinese/bilingual conventions when needed.
   Check bilingual drift, metaphor, workflow-language leakage, repetition,
   and qualifier stacking. Preserve distinct local conditions; narrative assessment
   decides cross-section need, placement, and the authoritative location.
4. Report the smallest evidenced set. Each needs locator, severity,
   `meso`/`micro`, and readable
   `finding_level|scientific_role|normalized_locator|failure_mode` fingerprint. Split
   different operations/locators; route macro findings to narrative.
5. Apply decisions; report current-text findings only.

## Reader-Aware Terminology

Trigger focused review only when a term may impede declared readers. For an Idea, use
scanner candidates only as prompts: inspect every reader entry and each
mixed/internal prose token; run dossier concordance only for triggered terms. A
candidate, quotation, abbreviation, proper name, standard defined term, description,
or removed form is not a finding.

Read `references/terminology-review.md` only when a term seems coined, nonstandard,
ambiguous, disputed, misleading, bilingual-drifting, or inaccessible. Apply its
core-role, actor-operation-object-criterion, title/modifier, consequence, first-use,
and transient concordance checks. Follow its evidence hierarchy: one paper is
insufficient, and exact-phrase absence is not adverse evidence.

Every confirmed terminology finding must:

- set `finding_kind: terminology`; give exact locator, reader effect, term, evidence,
  competing forms/locators (or `[]`), executable change, and acceptance test;
- give an exact verified standard replacement or, without adequate evidence, a direct
  plain-language description, plus exact first-use wording naming referent and function;
- retest the replacement for trigger, evidence, reader baseline, first use, and
  modifier attachment; never substitute another unverified compact label;
- use `meso`/`concept_cluster` for cross-location forms and `micro`/`occurrence` for a
  local repair. Map roles, preserve distinctions, and require whole-dossier
  concordance in the acceptance test.

If wording requires a scientific choice, name alternatives and use
`clarification_required`; never choose one. Persist no term inventory,
passing-candidate/per-term list, or separate terminology artifact/workflow/skill.

Flag project/software/state-machine prose standing for a scientific
condition, operation, decision, object, or consequence; give the exact scientific/plain
replacement. Fixed scaffolding is exempt: for
`research-idea.v3`, do not score, translate, rename, or report its 15 H2 headings, five
reasoning H3 headings, section-1/structured-abstract labels, evidence-chain labels, or
Claim-Support headers unless copied into prose/free-form labels. Preserve field
cardinality and format.

## Report and Decisions

Use `templates/language-assessment-report.md` exactly. Required frontmatter includes
`review_id`, `reviewer_skill`, `reviewer_instance_id`, `workflow_id`, `round_id`,
`input_artifact_ids`, `input_versions`, `scope`, `files_read`, `isolation_mode`,
`prior_scores_visible`, `source_edits_performed`, `decision`, `findings`, and
`unresolved_issues`; bind `dossier_ref`, component refs, and `reader_handoff` when
applicable. Every actionable (`critical`, `major`, `minor`) finding needs all repair
fields; terminology fields exist only for confirmed actionable terminology.

A completed Idea report records `status: completed`, count, and basis for four coverage
receipts; these prove coverage, not quality/status. Stop reports state omissions and
omit receipts. Keep terminology inside this report; never add a
SHA, content-hash, or digest field.

- Decisions: `submission_ready`, `minor_language_revision`,
  `major_language_revision`, `needs_professional_editing`,
  `clarification_required`, or `independent_review_pending`.
- Any hard-gate failure or actionable finding prevents `submission_ready`; `major`
  requires major-or-worse and `critical` requires `needs_professional_editing`. Apply
  compound-gate constraints. An unresolved misleading, inaccessible, or unverified
  core term blocks readiness. Preferences are suggestions; mark uncertain convention.
- Use `clarification_required` only when missing input prevents judgment or repair
  requires a scientific choice; identify the input/alternatives. It is not language-ready.

Run `scripts/validate_language_assessment.py <report.md>` before every handoff.

## Resource and Helper Conditions

- Always read `references/language-assessment-rubric.md`; always read `references/language-hard-gates.md`.
- Read `references/english-academic-language-conventions.md` for English.
- Read `references/chinese-academic-language-conventions.md` for Chinese/bilingual.
- Read `references/discipline-language-conventions.md` for the discipline.
- Read `references/common-l1-interference-patterns.md` for recurring transfer.
- Always use `templates/language-assessment-report.md`.
- After validator changes, run `scripts/test_validate_language_assessment.py`; after scanner changes, run `scripts/test_scan_idea_language_candidates.py`.
- Only after an Idea repair with terminology actions, run `scripts/diff_reader_facing_short_forms.py <source-dossier> <revised-dossier>` as an attention aid, never a verdict.
- Only after changing that helper, run `scripts/test_diff_reader_facing_short_forms.py`.

## Completion

Stop on unreadable input, scope mismatch, clarification, or independence failure.
Confirm all checks, locators, unchanged sources, a valid report, and no scientific or
macro narrative evaluation.
