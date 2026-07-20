# Editorial Readiness and Content Preservation

## Contents

- [Readiness inputs and isolation](#readiness-inputs-and-isolation)
- [Repair bundle](#repair-bundle)
- [Preservation review](#preservation-review)
- [Fresh reassessment](#fresh-reassessment)
- [Repair outcome attribution](#repair-outcome-attribution)

Use this contract after scientific/methodological revision and before every
Idea evaluation.

## Readiness inputs and isolation

Freeze the current dossier by `{artifact_id, version, path}`. Dispatch two fresh
reviewers in parallel:

- `idea-narrative-assessor`: current dossier, target-reader profile, reader
  prior-knowledge handoff, and its own skill references only;
- `academic-language-assessor`: the complete current dossier, target language,
  discipline, and the same reader handoff.

Neither reviewer reads preflight, evaluator output, prior reports, prior
versions, deltas, workflow state, portfolio, or parent hidden reasoning.
Narrative review never judges scientific correctness, novelty, impact, or
feasibility. Language review never judges argument quality or scientific merit.

## Repair bundle

When either reviewer reports an actionable blocking editorial finding, set
`editorial_revision_required`. Ordinary repair decisions are
`major_narrative_revision` and `major_language_revision`; a `critical` or
`major` finding is also blocking even if a malformed report gives a weaker
decision. Route `clarification_required` to `clarification_stop` until the
missing information is supplied and freshly assessed. Route
`needs_professional_editing` to `editorial_revision_required`, but require
external language support rather than the ordinary scientific-writer repair;
the resulting complete dossier still requires preservation when science-facing
text changed and fresh language assessment. For an ordinary actionable repair,
freeze `protected-content-register.yaml` and `included_repair_item_ids` in one
approved writer brief. A repair item is either a narrative repair-plan action
or an actionable language finding; do not call both kinds findings. Bind the
source narrative assessment, narrative plan, and language assessment by logical
ID, version, and path. Include actions that cover every `critical` and `major`
source finding;
include a `minor` or `suggestion` only when it will be repaired, and record why
any reported non-blocking finding is omitted. Every included repair item must
have executable fields before delegation. Each normalized action records its
`repair_item_id`, source item IDs, and the source finding IDs it addresses.
Compare actions that touch the same
locator or reader-facing role before delegation. Do not give the writer
incompatible prescriptions to interpret: keep the narrative action's required
rhetorical function and content placement, keep the language action's
reader-facing wording and terminology constraint, and record one compatible
combined target in the brief. If both cannot be satisfied without a scientific
choice, route to `clarification_required`. Normalize every included narrative
or language item into one complete repair action in the writer brief, retaining
its source ID, locator, operation, problem, target, required function or term,
preserved content, move/delete disposition, dependencies, and acceptance test.
The narrative and language reports and the assessor's YAML plan remain audit
inputs to the orchestrator, not writer inputs. Then give a fresh scientific
writer only:

- the current dossier;
- the approved writer brief containing the frozen IDs, normalized actions, and
  any combined target and disposition for overlapping actions;
- the protected-content register; and
- the output paths for one complete next dossier and one revision delta.

Before freezing the brief, run the bundled validator with all three audit
sources and the frozen register; an internal-consistency-only pass is
insufficient for delegation:

```powershell
python scripts/validate_editorial_repair_writer_brief.py <brief.yaml> --narrative-assessment <assessment.md> --narrative-plan <plan.yaml> --language-assessment <assessment.md> --protected-register <register.yaml>
```

The register's `source_artifact` must be the exact dossier supplied to the
writer. An ancestral lineage register remains part of history but cannot
authorize a later repair round.

The writer performs one concentrated editorial repair. It must execute delete,
move, merge, and consolidation actions as well as additions. It must not infer
review history or change science to improve prose. Record the complete dossier as
`change_type: editorial_repair` and the paired delta as
`change_type: editorial_repair_delta`.

For an editorial-only revision, copy every `identity_anchor` frontmatter value
verbatim from the current dossier. Reader-facing titles and prose may be revised,
but the writer must not paraphrase this machine-facing identity record. Any
requested anchor change leaves editorial scope and follows the applicable
scientific-change or new-Idea route.

“One concentrated repair” permits bounded internal section passes when the
bundle is long. One writer maintains one complete target dossier and processes
sections 1--4, 5--11, 12--14, then references and whole-dossier concordance.
Do not persist section fragments or assign different writers to independent
fragments; both would weaken cross-section terminology and content-preservation
checks. The writer must not reopen either assessor report or plan; the approved
brief is the sole writer-facing repair interface.

Before the target dossier is frozen, the orchestrator checks every included
repair item against the actual candidate text and reruns the brief's named
script, inputs, and arguments. A missing action, false completion claim, or new
nearby wording regression returns the still-unfrozen candidate to the same
writer for a bounded correction and complete rerun. Do not dispatch preservation
or readiness reviewers yet. This is workflow-conformance checking, not another
scientific or language assessment; a successful production run need not persist
a separate compliance report.

First triage the impact. A localized omitted action or instruction deviation
that is only `minor` or `suggestion`, causes no scientific/content-preservation
change, does not alter a decision or reader eligibility, and has no broad
recurrence is a nonblocking observation: keep it visible and continue without a
new correction, reproduction attempt, or extra test. During plugin development,
record it only in the single maintained report at
`tests/idea-narrative-forward-0.9.0-preview.3/error-localization-report-r001.md`
with plugin version, observed symptom, suspected diagnosis, and proposed
solution for owner prioritization. Do not create a case-specific minor-issue
report or convert the observation into a repair or regression-test requirement.
The bounded-correction rule above still applies to critical/major findings,
content drift, decision/readiness effects, broad contamination, or an invalid
deterministic result; never downgrade those to avoid a repair.

The writer creates or finalizes the delta only after the whole-dossier scan and
deterministic lint pass and after freezing the complete dossier. A later dossier
edit invalidates that delta and requires a new scan and rewritten delta;
timestamps or content hashes are not substitutes for this order.

Before handoff, the delta must map every frozen included repair item ID to the
revised locator, operation, and text-grounded result of its acceptance test. A
missing mapping or an unsupported completion claim
blocks preservation review; it is not deferred to the fresh assessor.
Use compact locator-level rows rather than copying report instructions,
protected content, or long dossier excerpts into the delta.

Before condensing, deleting, or moving any registered passage, the writer must
open every `source_locator` in the prior dossier and preserve each scientific
commitment found there, including numerical and temporal rules, analysis
handling, evidence status, and claim boundaries. The register summary is an
index, not permission to discard details at its locator. The delta maps every
`protected_id` to revised locator(s) and item-level preservation evidence. If a
commitment cannot be retained, declare a scientific change instead of labeling
the revision editorial. A binding user/context value omitted from the prior
dossier may be frozen with `source_context_locator`; the orchestrator resolves
that locator before repair and copies the exact value into `protected_content`.
Its restoration is authorized baseline content, not an undeclared scientific
addition, and does not require the writer to read another source artifact.

When the source has mutually exclusive or fallback branches, the register and
delta distinguish shared prerequisites from each branch's eligibility and
consequence. A condition belonging to one branch must not become a prerequisite
for the whole component, and failure of one branch must not erase an available
alternative branch. Preserve the complete logic once at its technical authority;
other mandatory sections keep only their distinct functional statement. Content
preservation never requires a full branch tree or limitation family to recur.

## Preservation review

Run `idea-narrative-assessor` in its separate preservation mode with only the
old dossier, new dossier, protected-content register, and revision delta.
Allowed decisions are:

- `scientific_content_preserved`;
- `editorial_scope_violation`;
- `identity_drift_detected`;
- `scientific_change_declared`.

Only `scientific_content_preserved` can advance directly. A declared scientific
change returns to the applicable scientific review/preflight; identity drift
returns `new_idea_required`; an undeclared scope violation returns to the
writer. Editorial repair alone cannot trigger promotion.

## Fresh reassessment

After a preserved repair, new narrative and language instances assess only the
new current dossier and reader handoff. Do not give them the prior report,
repair plan, old dossier, delta, or preservation decision. If major findings
remain after the concentrated repair, retain `editorial_revision_required` and
stop before evaluation rather than accumulating another additive patch. Minor
findings remain visible but do not by themselves force another repair cycle.

The Idea is editorially eligible only when:

- narrative decision is `narrative_ready` or `minor_narrative_revision`, with no
  unresolved `major` finding;
- language decision is `submission_ready` or `minor_language_revision`, with no
  unresolved `critical` or `major` finding;
- preservation is `scientific_content_preserved` when a repair occurred;
- no blocking clarification remains; and
- the artifact index and current pointers are complete.

The later `idea-evaluator` receives exactly the eligible current dossier. It
never receives any readiness or preservation artifact.

## Repair outcome attribution

Record one orchestrator-owned attribution in
`decisions.editorial_repair_failure_attribution` only when fresh reassessment
retains a blocking finding or an explicit validation/debug run requests outcome
attribution. A successful production repair may leave this nullable field
empty; `fresh_reassessment_closed` is an optional validation receipt, not a
mandatory workflow artifact. The record is an audit explanation, not a reviewer
score or repair instruction.

```yaml
editorial_repair_failure_attribution:
  repair_brief_ref: {artifact_id: "", version: "", path: ""}
  source_dossier_ref: {artifact_id: "", version: "", path: ""}
  repaired_dossier_ref: {artifact_id: "", version: "", path: ""}
  fresh_reassessment_refs: []
  attribution: source_input_or_context_handoff_failure | assessor_coverage_failure | assessor_variance | brief_normalization_failure | writer_execution_failure | writer_regression | context_attention_failure | workflow_contract_conflict | fresh_reassessment_closed
  fingerprint:
    finding_level: critical | major | minor | suggestion | not_applicable
    scientific_role:
    normalized_locator:
    failure_mode:
  evidence:
    explicit_brief_action_id:
    full_context_result:
    bounded_section_view_result:
    same_writer_instance_confirmed: false
  rationale:
```

The fingerprint is readable and stable enough for human comparison: combine
finding level, scientific role, normalized locator, and failure mode. Do not
compute or store a hash. Normalize a locator to the smallest stable section,
table, field, or paragraph label that identifies the failed operation; do not
use a line number alone when the document can be repaginated.

Test `context_attention_failure` only in an opt-in diagnostic run. Use that
attribution only when all of the following are recorded:

- the approved brief contains an explicit executable action and acceptance test;
- the same writer instance omitted or failed that action while operating on the
  complete allowed context;
- the same writer instance then succeeds on that action when given a
  deterministic bounded section view containing the required source and target
  context; and
- no source/context omission, assessor coverage gap, normalization defect,
  workflow conflict, scientific clarification, or writer regression explains
  the result.

Without that paired same-writer evidence, choose the supported alternative and
do not infer an attention failure. A normal successful repair needs no
attribution record.
