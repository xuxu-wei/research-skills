# Post-evaluation journal matching

Run this phase only after the dossier-only evaluation block is complete and
frozen. Journal matching is advisory and cannot change a score, gate, fatal
flaw, decision, finding, repair direction, limitation, or unresolved issue.

## Retrieval boundary

- Use the dossier to identify a small defensible candidate set; an empty set is
  valid. Do not add a weak candidate to fill a quota.
- Retrieve only official journal or publisher pages describing aims and scope,
  accepted article types, or instructions that define an article type.
- Do not retrieve citation evidence, journal metrics, rankings, acceptance
  rates, editorials, news, aggregators, or competitor articles.
- If an intended official scope or article-type URL unexpectedly redirects to a
  page containing disallowed material, record the URL as
  `discarded_disallowed_content`, do not quote, use, or cite that material, and
  continue with a clean official source. Incidental exposure does not invalidate
  the already frozen evaluation unless the material was used or changed an
  evaluation field; if it was used, discard the evaluator instance.
- Keep project `files_read` equal to the dossier path. Record each opened web
  page under `external_urls_consulted`; a URL is not a project file.
- If current official information is unavailable, state that uncertainty. Do
  not infer current scope or article types from memory.

## Output contract

```yaml
evaluation_frozen_before_journal_search: true
evaluation_changed_after_journal_search: false
external_urls_consulted:
  - source_id:
    url:
    publisher_or_journal:
    page_type: aims_and_scope | article_types | instructions_for_authors
    source_status: usable | discarded_disallowed_content
    checked_at:
journal_matching:
  status: completed | no_defensible_candidate | official_information_insufficient
  match_basis: official_scope_and_article_type_only
  candidate_brief:
    schema_version: research-idea-journal-candidate-brief.v1
    brief_id:
    matching_source_skill: idea-evaluator
    source_dossier_ref: {artifact_id: "", version: "", path: ""}
    evaluation_fields_included: false
    scoring_present: false
    ranking_present: false
    publication_probability_present: false
    candidates:
      - candidate_id:
        publication_unit: {unit_id: "", dossier_locator: "", whole_idea_reason: null}
        journal_title:
        proposed_article_type:
        scope_fit:
        article_type_fit:
        mismatch_risks: []
        official_source_ids: []
    no_candidate_reason: null
  unresolved_issues: []
```

Every candidate must cite only `usable` recorded official sources and must have
at least one such source for scope and,
when an article type is proposed, official support for that type. `scope_fit`
and `article_type_fit` describe fit to the dossier; they do not predict
acceptance or restate evaluation scores. Candidate order is not a journal
ranking.

`publication_unit` binds the candidate to one expected paper or analysis output
named at a recognizable dossier locator. Use `unit_id: whole_idea` only when the
dossier exposes no separable publication unit, and state why in
`whole_idea_reason`. This binding is editorial metadata, not an evaluator
finding.

The nested `candidate_brief` is deliberately free of scores, gates, decisions,
findings, and repair directions. It may be passed, by value or as a separately
saved logical artifact, with the same dossier to a fresh
`medical-journal-review` instance. That reviewer may confirm, reject, or replace
candidates without seeing this evaluation report.

When a file-backed brief is required, the orchestrator materializes this exact
semantic payload and adds only `artifact_id`, `version`, `workflow_id`,
`round_id`, `materialized_by_skill: research-idea-orchestrator`, and `frozen`.
It does not repeat the journal search, alter a candidate, or derive content from
the frozen evaluation fields.
