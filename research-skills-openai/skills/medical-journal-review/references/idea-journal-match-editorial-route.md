# Idea journal-match editorial route

Use this narrow route to independently test a journal-candidate brief produced
after an Idea evaluation. This is not a second Idea evaluation, a general
medical-design review, or an acceptance forecast.

## Contents

- [Isolated inputs](#isolated-inputs)
- [Procedure](#procedure)
- [Output schema](#output-schema)

## Isolated inputs

Accept only:

- one complete current Idea dossier bound by `{artifact_id, version, path}`;
- one `research-idea-journal-candidate-brief.v1`, embedded or saved as a
  separate logical artifact, whose `source_dossier_ref` matches the dossier;
- this skill's instructions and official journal or publisher pages describing
  scope or article types.

The candidate brief must contain `evaluation_fields_included: false` and only
publication-unit bindings, candidate names, proposed article types, fit
rationales, mismatch risks, and official source references. Do not read an
evaluator report or accept scores, gates, decisions, findings, repairs, or a
prior journal-review report. If those fields are exposed, return
`not_reviewable_with_current_materials` and
request a clean brief in a fresh instance.

List the dossier and a file-backed brief under `files_read`. An embedded brief
uses `path: null` and is not a fictitious file. List every web page separately
under `external_urls_consulted`.

## Procedure

1. Validate reviewer freshness, dossier identity, candidate-brief schema, exact
   source-dossier match, and absence of evaluation fields.
2. Read the dossier for topic, target readers, design, expected output, evidence
   status, and intended scholarly contribution. Verify that each candidate's
   publication unit and dossier locator identify the expected paper or analysis
   output being matched. Do not score or gate the Idea.
3. Re-open current official scope and article-type pages for every candidate.
   Do not treat the candidate brief's conclusion as evidence.
4. Give every submitted candidate one disposition:
   `confirmed`, `rejected`, or `replaced`. State the official-source support,
   fit rationale, and mismatch risk.
5. Search additional official journal or publisher scope/article-type pages only
   when a submitted candidate is rejected or a materially better fit is
   apparent. A replacement must meet the same evidence standard and name the
   candidate it replaces. If an intended official URL unexpectedly redirects to
   disallowed metrics, rankings, acceptance rates, news, or competitor content,
   record it as `discarded_disallowed_content`, do not use or cite it, and
   continue with a clean official source. Discard the reviewer instance only if
   the disallowed material affected a disposition or replacement.
6. Return no candidate when none is defensible. Do not fill a quota, rank by
   prestige, use metrics or acceptance rates, predict publication, or alter the
   Idea's evaluation or workflow state.

## Output schema

```yaml
schema_version: research-idea-journal-match-review.v1
review_id:
reviewer_skill: medical-journal-review
reviewer_instance_id:
workflow_id:
round_id:
review_route: idea_journal_match_editorial_review
reviewed_idea_ref: {artifact_id: "", version: "", path: ""}
candidate_brief_ref: {artifact_id: embedded-candidate-brief, version: embedded, path: null}
files_read: []
external_urls_consulted:
  - source_id:
    url:
    publisher_or_journal:
    page_type: aims_and_scope | article_types | instructions_for_authors
    checked_at:
isolation_mode: fresh_subagent
evaluator_report_visible: false
evaluator_scores_visible: false
source_edits_performed: false
publication_probability_assessment: null
decision: journal_candidates_confirmed | journal_candidates_revised | no_supported_journal_candidate | not_reviewable_with_current_materials
candidate_dispositions:
  - candidate_id:
    publication_unit: {unit_id: "", dossier_locator: "", whole_idea_reason: null}
    submitted_journal:
    submitted_article_type:
    disposition: confirmed | rejected | replaced
    rationale:
    mismatch_risks: []
    official_source_ids: []
replacement_candidates:
  - replacement_id:
    replaces_candidate_id:
    publication_unit: {unit_id: "", dossier_locator: "", whole_idea_reason: null}
    journal_title:
    proposed_article_type:
    rationale:
    mismatch_risks: []
    official_source_ids: []
unresolved_issues: []
```

Use `journal_candidates_confirmed` when all retained candidates are supported
without replacement; `journal_candidates_revised` when any submitted candidate
is rejected or replaced but a supported set remains;
`no_supported_journal_candidate` when no submitted or replacement candidate is
defensible; and `not_reviewable_with_current_materials` only for invalid,
contaminated, mismatched, or unreadable inputs.

Use `unit_id: whole_idea` only when no separable expected publication or
analysis output exists in the dossier, with a dossier locator and a concise
`whole_idea_reason`.

`publication_probability_assessment` is always `null` on this route. Adequate
inputs for another medical-review route do not broaden this route's scope.
