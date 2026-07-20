---
review_id:
reviewer_skill: academic-language-assessor
reviewer_instance_id:
workflow_id:
round_id:
input_artifact_ids: []
input_versions: []
scope: <complete_idea_dossier | complete_artifact | named_sections>
dossier_ref: {artifact_id: "", version: "", path: ""}
input_component_refs: []
reader_handoff: {artifact_id: embedded-reader-handoff, version: embedded, path: null}
files_read: []
isolation_mode: fresh_subagent
prior_scores_visible: false
source_edits_performed: false
decision: <submission_ready | minor_language_revision | major_language_revision | needs_professional_editing | clarification_required | independent_review_pending>
coverage_receipt: # required for every completed complete_idea_dossier assessment
  reader_entry: {status: completed, reviewed_count: 0, basis: ""}
  core_scientific_role: {status: completed, reviewed_count: 0, basis: ""}
  terminology_concordance: {status: completed, reviewed_count: 0, basis: ""}
  local_language: {status: completed, reviewed_count: 0, basis: ""}
findings:
  - finding_id:
    severity: <critical | major | minor | suggestion>
    finding_kind: <language | terminology>
    finding_level: <meso | micro>
    finding_scope: <concept_cluster | occurrence> # optional
    scientific_role: <readable-kebab-case-role>
    normalized_locator: <readable-kebab-case-locator>
    failure_mode: <readable-kebab-case-mode>
    fingerprint: <finding_level|scientific_role|normalized_locator|failure_mode>
    category:
    dossier_locator:
    current_problem:
    target_state:
    required_change_or_replacement:
    content_to_preserve:
    acceptance_test:
    # Required only for a confirmed actionable terminology problem. Do not add
    # a finding for an acceptable scanner or short-form-diff candidate.
    term_or_phrase:
    recommended_form_or_plain_description:
    evidence_basis:
    first_use_definition:
    competing_forms_and_locators: [] # keep empty when no competing form exists
unresolved_issues: []
---

# Language Assessment Report

Use logical artifact identity (`artifact_id`, `version`, and `path`) and
`files_read` for provenance. Do not add SHA, content-hash, or digest fields.
For `complete_idea_dossier`, the dossier reference and reader handoff are
required. A file-backed handoff must occur in `files_read`; an embedded handoff
uses `path: null` and is not added as a fictitious file or input artifact.
Validate this file with `scripts/validate_language_assessment.py` before handoff.
For a completed `complete_idea_dossier` assessment, all four coverage receipts
use `status: completed`; this records coverage rather than language quality or a
per-term status. Use bounded counts and a concise basis. Never create a terminology
inventory, per-term status list, separate artifact, or separate skill.
Omit `coverage_receipt` from a clarification or independence stop report.

**Assessment ID**: lang-001
**Target Language**: {{English | Chinese | bilingual}}
**Discipline**: {{discipline}}
**Target Journal**: {{target_journal}} (if specified)
**Scope**: {{scope}}
**Date**: {{date}}

---

## Overall Language Readiness

**Level**: {{submission_ready | minor_language_revision | major_language_revision | needs_professional_editing | clarification_required | independent_review_pending}}

**Recommendation**: {{accept | polish | revise_language | professional_editing_required | clarify_input | wait_for_independent_review}}

---

## Dimension Scores

| Dimension | Score (1–10) | Severity |
|-----------|-------------|----------|
| Grammar & Syntax | {{score}} | {{pass / borderline / fail}} |
| Academic Register & Tone | {{score}} | {{pass / borderline / fail}} |
| Terminology Consistency | {{score}} | {{pass / borderline / fail}} |
| Tense & Voice Conventions | {{score}} | {{pass / borderline / fail}} |
| Conciseness & Redundancy | {{score}} | {{pass / borderline / fail}} |
| Readability & Flow | {{score}} | {{pass / borderline / fail}} |

---

## Hard Gate Status

**Overall**: {{pass | fail}}

| Gate | Status | Detail |
|------|--------|--------|
| Grammar error density | {{pass / fail}} | {{error count per 500 words}} |
| Academic register | {{pass / fail}} | {{sections affected}} |
| Terminology coherence | {{pass / fail}} | {{inconsistent concepts count}} |
| Tense systematic violation | {{pass / fail}} | {{sections affected}} |

---

## Strengths

{{List 2-5 specific things done well. Be concrete: "Consistent use of past tense throughout Methods" rather than "Good grammar".}}

---

## Specific Issues

For every actionable (`critical`, `major`, or `minor`) finding, provide a bounded dossier locator,
current problem, target state, required change or verified replacement,
content to preserve, and an acceptance test. If one pattern needs different
operations in different places, split it into separate findings. Do not use
`throughout` or `full dossier` as the only locator for a blocking finding.
Every proposed repair must preserve any contract-fixed sentence count, field
cardinality, and table or list format. A recommended definition or replacement
must not depend on another undefined compact label.
Classify a cross-location concept cluster as `meso` and a localized expression
as `micro`; macro argument or section-architecture findings belong to narrative
assessment. Build the readable `fingerprint` exactly from the four declared
components. It is a stable finding key, not a content hash.
Put those six executable fields in structured frontmatter so the handoff can
be validated mechanically. The Markdown body references finding IDs and gives
only concise evidence, reader effect, and prioritization; do not duplicate the
full action fields or replacement instructions there.

### Chinese Academic Clarity (if applicable)

{{For Chinese or bilingual text: location, original, issue description, deletion-or-revision direction, severity. Prioritize concise, clear, explicit prose; flag unnecessary metaphor, decorative modifiers, redundant caveats, and promotional phrasing.}}

### Grammar & Syntax

{{For each issue: location, original, issue description, suggested correction, severity}}

### Academic Register & Tone

{{For each issue...}}

### Terminology Consistency

{{For each issue...}}

For each confirmed actionable terminology finding, set
`finding_kind: terminology` and record the
term or phrase, recommended verified form or plain description, evidence basis,
first-use definition, and every observed competing form with a locator; use an
empty list when the problem has only one form. These
fields are required only for a terminology finding and avoid a separate term
register. Record the complete action in frontmatter. The
body may use this compact human-readable index without restating the action:

| id | term_or_phrase | locator | reader_effect | action_in_frontmatter |
|---|---|---|---|---|
|  |  |  |  | yes |

When no actionable terminology finding exists, state `none`; do not list acceptable
quoted or parenthetical forms, abbreviations, proper names, or other scanner candidates,
and do not generate inventories, dispositions, or per-term statuses.

For a core-concept coherence or internal-vocabulary finding, list every observed
competing form and its locator in the finding. The acceptance test must name the
single retained verified or descriptive form and require a whole-dossier check;
repairing only the illustrative excerpts does not close the finding.

For a complete Idea dossier, the temporary coherence pass must cover the central
object, primary question or task, hypothesis target quantity, primary outcome,
validation or update operation, failure or negative-result output, conditional
downstream component, and contribution when those roles exist. Mark an absent
role not applicable in memory; report only roles that trigger a finding and do
not persist the complete temporary list.

Re-parse a recommended title replacement before handoff. Its modifiers must
attach unambiguously to the intended semantic heads.

### Tense & Voice Conventions

{{For each issue...}}

### Conciseness & Redundancy

{{For each issue...}}

### Readability & Flow

{{For each issue...}}

---

## Language Revision Priorities

1. **{{dimension}}**: {{issue_count}} issues — {{fix_approach}}
2. ...

---

## Re-Assessment Status (if applicable)

Reassessment is a fresh complete reading of the current artifact and reader handoff.
Do not compare prior scores, decisions, issue lists, text versions, repair briefs, or
revision deltas. Report only current-text findings and the current decision.

---

## Assessment Notes

{{Any uncertainty, scope limitations, assumptions, or caveats. If discipline conventions were ambiguous, state what was assumed.}}
