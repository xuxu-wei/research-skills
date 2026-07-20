# Journal-review and portfolio artifact contracts

## Contents

Biomedical or clinical journal review; lineage and portfolio navigation.

## Biomedical or clinical journal review

Run this route only after the final effective evaluation of the current dossier
has been sealed and no further revision is planned in that loop. Applicability
is based on the dossier's biomedical or clinical domain and setting, not on an
evaluator score. After the evaluator freezes its complete evaluation and runs
the separate official-scope match, the orchestrator materializes the
evaluator's score-free candidate payload as a frozen logical artifact. It does
not repeat the search, reinterpret fit, or copy any evaluation field.

```yaml
candidate_journal_match_brief:
  schema_version: research-idea-journal-candidate-brief.v1
  artifact_id:
  version:
  workflow_id:
  round_id:
  source_skill: research-idea-orchestrator
  matching_source_skill: idea-evaluator
  materialized_by_skill: research-idea-orchestrator
  brief_id:
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
  frozen: true

idea_medical_journal_review:
  schema_version: research-idea-journal-match-review.v1
  review_id:
  reviewer_skill: medical-journal-review
  reviewer_instance_id:
  workflow_id:
  round_id:
  input_artifact_ids: []
  input_versions: []
  files_read: []
  review_route: idea_journal_match_editorial_review
  reviewed_idea_ref: {artifact_id: "", version: "", path: ""}
  candidate_brief_ref: {artifact_id: "", version: "", path: ""}
  isolation_mode: fresh_subagent
  evaluator_report_visible: false
  evaluator_scores_visible: false
  source_edits_performed: false
  decision:
  candidate_dispositions: []
  replacement_candidates: []
  publication_probability_assessment: null
  unresolved_issues: []
```

The candidate brief is a current public-scope matching aid, not an evaluation,
journal selection, ladder, endorsement, or acceptance estimate. It contains no
evaluator report reference or material derived from evaluator scores, findings,
decision, or limitations. The reviewer receives exactly the current dossier and
brief; it follows the dedicated Idea journal-match route and reopens current
official journal sources independently.
For Idea artifacts, `files_read` and both references use logical artifact ID,
version, and path. Do not compute, request, persist, or compare a SHA or digest.

## Lineage and portfolio navigation

```yaml
idea_lineage_record:
  schema_version: research-idea.v3
  lineage_id:
  idea_id:
  parent_idea_ids: []
  route_profile: focused_optimization | bounded_exploration
  change_type: create | revise | evidence_claim_sync | editorial_reposition | editorial_repair
  decision_history: []

portfolio_navigation_entry:
  idea_id:
  title:
  dossier_ref:
  dossier_version:
  evaluation_ref:
  candidate_journal_match_ref:
  medical_journal_review_ref:
  journal_review_applicability: applicable | not_applicable
  narrative_readiness_ref:
  language_readiness_ref:
  content_preservation_ref:
  reference_ledger_ref:
  status:
  fatal_or_blocking_findings: []
  dissent: []
  unresolved_issues: []
  next_human_action:
```

The portfolio links the qualifying dossier and never serializes its body again.
