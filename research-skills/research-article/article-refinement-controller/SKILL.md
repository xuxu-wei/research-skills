---
name: article-refinement-controller
description: Manage the revision loop after evaluation. Route to the appropriate revision mode, produce revision plan and response-to-reviewer, track revision deltas, manage language polishing cycles, and enforce revision round limits.
version: 0.1.0
author: Xuxu Wei
license: MIT
metadata:
  hermes:
    tags: [research-article, refinement, revision, response-to-reviewer, language-polishing]
    related_skills:
      - article-orchestrator
      - article-evaluator
      - article-drafter
      - academic-language-assessor
---

# article-refinement-controller

## Purpose

Manage the revision cycle triggered by evaluator `revise` decisions. Route issues to the correct revision mode, produce the three-file revision package (plan, response, delta), and enforce revision round limits.

This skill does NOT write manuscript text (that is `article-drafter`'s job), evaluate quality (that is `article-evaluator`'s job), or draft frontmatter. It controls the revision process.

## Core Rules

- Maximum 2 revision rounds. After round 2, stop and mark `major_revision_required`.
- Every round produces exactly three files: `revision-plan`, `response-to-reviewer`, `revision-delta`.
- Every issue from the evaluator gets an entry strategy: `enter_manuscript` (modify manuscript) | `response_only` (respond only, no text change) | `decline` (explicitly decline).
- `decline` decisions must include a rationale.
- The manuscript body must NEVER contain reviewer-response language.
- Language polishing does not consume a revision round.
- Revision delta reports must describe substantive changes. "Polished expression" alone is insufficient.
- Modes `analysis_required` and `study_redesign_required` must NOT be processed — stop and inform the user.

## I/O Contract

```yaml
io_contract:
  allowed_inputs:
    - evaluation_report
    - manuscript_draft
    - article_blueprint
    - claim_audit_report (optional)
  required_outputs:
    - revision_plan
    - response_to_reviewers
    - revision_delta
  may_read:
    - "08_evaluations/**"
    - "06_drafts/**"
    - "04_blueprint/**"
    - "07_claim-audit/**"
  may_write:
    - "09_revisions/round-*/**"
  must_not_read: []
  must_not_write:
    - "06_drafts/**"
    - "04_blueprint/**"
    - "08_evaluations/**"
  may_call:
    - academic-language-assessor
    - article-drafter
  must_not_call:
    - article-evaluator
  failure_modes:
    - "evaluator issues lack entry_strategy → assign default strategies based on severity"
    - "delta report only lists 'polished expression' → reject delta, require specific changes"
    - "revision round exceeds limit → stop loop, mark major_revision_required"
  escalation_route: "article-orchestrator"
```

## Procedure

### Step 1: Parse Evaluation Issues

Extract and categorize all issues from the evaluation report:

- Group by dimension and severity
- Identify which revision mode each issue requires
- Flag any `analysis_required` or `study_redesign_required` issues → stop, inform user

### Step 2: Classify Revision Mode

Map issues to revision modes:

| Mode | Issue Type | Consumes Round |
|------|-----------|---------------|
| `textual_revision` | Minor wording, clarity, flow | Yes |
| `structural_revision` | Section reorganization | Yes |
| `evidence_relinking` | Evidence-claim misalignment | Yes |
| `reporting_completion` | Missing reporting standard items | Yes |
| `claim_downscaling` | Overclaim remediation | Yes (requires author confirmation) |
| `methods_detailing` | Methods description gaps | Yes |
| `journal_retargeting` | Journal mismatch | Yes (requires author decision) |
| `language_polishing` | Language hard gate failure | **No** |

### Step 3: Produce Revision Plan

```yaml
revision_plan:
  round: 1
  evaluation_ref: "evaluation-v001.md"
  manuscript_version: "manuscript-v001.md"
  target_version: "manuscript-v002.md"
  revision_entries:
    - entry_id: "RE001"
      issue_ids: ["E001-C003"]
      revision_mode: textual_revision | structural_revision | evidence_relinking | reporting_completion | claim_downscaling | methods_detailing | journal_retargeting | language_polishing
      description: ""
      entry_strategy: enter_manuscript | response_only | decline
      rationale_for_strategy: ""         # required if decline
      requires_author_confirmation: true | false
  items_requiring_author: []
  expected_improvements: []
```

### Step 4: Dispatch to Drafter

Send the revision plan to `article-drafter` in revision mode. The drafter applies changes and returns the new manuscript version.

### Step 5: Produce Response-to-Reviewer

```yaml
response_to_reviewers:
  round: 1
  manuscript_version: "manuscript-v002.md"
  evaluation_ref: "evaluation-v001.md"
  responses:
    - concern_id: "E001-C003"
      concern_summary: ""
      action: revised | response_only | declined
      manuscript_location: ""
      response_text: ""
      change_summary: ""
  unresolved_issues: []
  new_issues_introduced: []
```

### Step 6: Produce Revision Delta

```yaml
revision_delta:
  round: 1
  previous_manuscript: "manuscript-v001.md"
  updated_manuscript: "manuscript-v002.md"
  evaluator_concerns:
    addressed: []
    partially_addressed: []
    not_addressed_with_reason: []
  new_issues_introduced: []
  substantive_changes:
    methods_changed: false
    results_changed: false
    primary_claim_strength_changed: false
    contribution_statement_changed: false
  new_assumptions_requiring_author_confirmation: []
  recommended_next_step: re_evaluate | panel | compositor
```

**Delta quality gate**: If the delta contains only vague descriptions like "polished expression" or "improved clarity" without specifying what was changed and why, reject it and require specifics.

### Step 7: Language Polishing (if needed)

When language hard gate fails:
1. Call `academic-language-assessor` (standalone-preflight mode) → get detailed issues
2. Classify issues: critical / major / minor / suggestion
3. Route to `article-drafter` in language_polishing mode (critical + major must be fixed)
4. Drafter returns revised draft + language change log
5. Re-assess with `academic-language-assessor`
6. If still failing → mark `language_status: needs_professional_editing`

## Output

Each round produces in `09_revisions/round-NNN/`:
- `revision-plan-rNNN.md`
- `response-to-reviewers-rNNN.md`
- `revision-delta-rNNN.md`

## Stop Conditions

- Round 2 complete and issues remain → `major_revision_required`
- `analysis_required` or `study_redesign_required` mode triggered → stop, inform user
- Language polishing fails after 2 attempts → mark `needs_professional_editing`
- Author declines required downscaling → stop, cannot proceed

## Pitfalls

- Do not write the revised manuscript directly. Route to drafter.
- Do not skip response-to-reviewer generation. Every evaluator concern must have a response.
- Do not embed reviewer-response language in the manuscript body.
- Do not accept vague delta reports. "Improved clarity" is not a change description.
- Do not process `analysis_required` or `study_redesign_required`. These require user action.
- Language polishing does not consume a round but does not exempt from re-evaluation of language gates.

## Verification

- Three files per round in correct directory
- Every evaluator concern has a response entry
- Every revision entry has an explicit entry strategy
- `decline` entries have rationale
- Manuscript body contains no reviewer-response language
- Delta report describes substantive changes, not vague improvements
- Round counter incremented correctly
- Language change log present if language polishing was done

## References

- `references/revision-mode-routing.md`: Detailed routing logic from issue type to revision mode.
- `references/response-to-reviewer-guide.md`: Response writing conventions, tone, and format.
- `references/delta-report-standards.md`: Minimum content requirements for valid delta reports.
- `article-orchestrator/references/artifact-contracts.md`: Canonical revision artifact schemas.
- `article-orchestrator/references/loop-control-rules.md`: Revision round limits, targeted repair rules, stop conditions.
- `article-orchestrator/references/artifact-naming-and-directory-rules.md`: Directory and naming conventions.
