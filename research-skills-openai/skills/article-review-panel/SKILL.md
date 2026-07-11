---
name: article-review-panel
description: "Use when an article orchestrator needs role-specific peer-review instructions for isolated reviewer subagents and non-compensatory aggregation rules that preserve fatal flaws and dissent."
---
# article-review-panel

## Purpose

Define role-specific peer-review instructions used by the orchestrator to pressure-test a manuscript. This skill is instantiated separately for each reviewer role; it is never run as one large reviewer or panel coordinator. The orchestrator alone aggregates sealed reports.

This skill does NOT evaluate the manuscript as a single evaluator (that is `article-evaluator`'s job), rewrite text, or draft responses. It simulates external review.

## Core Rules

- Default mode: `blind_external_simulation`. Reviewers receive only the manuscript (no context brief, no evaluation report, no unresolved issues).
- The orchestrator creates one fresh independent subagent or delegated thread per reviewer role and dispatches all roles concurrently.
- Non-compensatory aggregation: a fatal flaw from the methodology reviewer caps the aggregated recommendation at `not_ready`.
- Dissenting opinions must be recorded and addressed, not averaged away.
- Reviewers evaluate only. They must not draft, revise, rewrite, or broaden scope.
- Panel tiers: `lightweight` (3 reviewers), `standard` (5), `full` (7).

## Independent Execution Contract

- Run each reviewer role as a separate instance of this skill in its own fresh independent subagent or delegated thread. Do not create a panel-coordinator reviewer.
- Receive frozen artifact IDs, file paths, and versions. Treat every source artifact as read-only.
- Write only the assigned individual reviewer report. Do not aggregate, edit, rewrite, polish, or fix any source artifact.
- Individual reviewers must not access parent hidden reasoning, expected answers, prior evaluation scores or decisions, or outputs from other reviewers.
- Every reviewer must report `files_read` and `review_scope`, together with the standard review identity and isolation fields.
- The orchestrator waits for all roles, then reads sealed reports and preserves conflicts and dissent without manufacturing consensus.
- If any required reviewer role cannot run in a fresh independent subagent or delegated thread, return `independent_review_pending` plus a self-contained continuation brief and stop. Never run the missing review inline and never produce an aggregate recommendation from an incomplete panel.

```yaml
review_id:
reviewer_skill: article-review-panel
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

## I/O Contract

```yaml
io_contract:
  allowed_inputs:
    - manuscript_draft
    - article_blueprint (journal_adapter only, for submission-guard reviewer)
  required_outputs:
    - assigned_reviewer_report
  may_read:
    - "06_drafts/**"
    - "04_blueprint/**"
  may_write:
    - "10_panel/reviewer-briefs/"
  must_not_read:
    - "08_evaluations/**"
    - "07_claim-audit/**"
    - "02_context/**"
  must_not_write:
    - "06_drafts/**"
  may_call: []
  must_not_call:
    - article-drafter
    - article-evaluator
    - article-claim-auditor
  failure_modes:
    - "fresh independent subagent unavailable for any required reviewer → return independent_review_pending with a continuation brief; do not review or aggregate inline"
    - "reviewer returns insufficient detail → request elaboration, do not fill gaps"
  escalation_route: "article-orchestrator"
```

## Panel Composition

### Standard Panel (5 reviewers)

| Role | Focus | Receives |
|------|-------|---------|
| Methodology & Statistics Reviewer | Study design, analysis validity | Manuscript only |
| Evidence-Claim Alignment Reviewer | Whether evidence supports each claim | Manuscript only |
| Clinical / Domain Significance Reviewer | Contribution importance, clinical relevance | Manuscript only |
| Submission-Guard Reviewer | Journal fit, reporting completeness, format | Manuscript + journal adapter |
| Clarity & Language Reviewer | Structure, clarity, language quality | Manuscript only |

### Lightweight Panel (3 reviewers)

Methodology, Evidence-Claim, Submission-Guard reviewers.

### Full Panel (7 reviewers)

Standard 5 + Internal Diagnostic Methodology Reviewer + Evidence Retrieval Completeness Reviewer.

## Reviewer Brief

Each reviewer brief specifies:
- Role and evaluation focus
- Frozen manuscript artifact ID, version, and path
- Explicit prohibited actions (do not draft, revise, rewrite)
- Output format (structured review with recommendation)
- `prior_scores_visible: false`, `source_edits_performed: false`, `files_read`, and `review_scope`

Reviewers receive only the manuscript, except the Submission-Guard reviewer also receives the frozen journal adapter. Do not include context brief, evaluation report, claim audit, other reviewer output, or unresolved issues.

## Orchestrator Aggregation Rules

```yaml
panel_aggregation_rules:
  - rule: "methodology reviewer fatal flaw"
    condition: "any methodology reviewer reports fatal_scientific_flaw"
    effect: "aggregated_recommendation ≤ not_ready"
  - rule: "evidence-claim reviewer fatal overclaim"
    condition: "any evidence-claim reviewer flags fatal_overclaim"
    effect: "require refinement before submission regardless of other reviewers"
  - rule: "submission-guard blocks"
    condition: "submission-guard reviewer flags missing required journal items"
    effect: "package_status cannot be ready_for_author_signoff"
  - rule: "dissenting opinion"
    condition: "any reviewer recommendation differs by ≥ 2 levels from others"
    effect: "dissent must be explicitly addressed in panel summary, not averaged away"
```

### Recommendation Levels

`strong_support` > `support_with_minor_revision` > `support_after_major_revision` > `revise_and_resubmit` > `not_ready` > `reject_or_redesign`

## Panel Route Decision

| Aggregated Recommendation | Route |
|--------------------------|-------|
| `strong_support` | Frontmatter drafting |
| `support_with_minor_revision` | Frontmatter (mark minor pending) |
| `support_after_major_revision` | Refinement controller (revision loop) |
| `revise_and_resubmit` | Refinement + re-evaluation gate |
| `not_ready` | Back to drafter or architect |
| `reject_or_redesign` | **Stop**. Return to study design. |

## Output

- `10_panel/panel-report.md`: Orchestrator-owned aggregate with panel composition, mode, tier, individual recommendations, aggregation result, dissenting opinions, and route decision.
- `10_panel/reviewer-briefs/`: Individual reviewer reports.

Each individual report follows the standard review identity and isolation fields. The orchestrator-owned aggregate records every reviewer instance ID, completion status, individual recommendation, conflict, and dissent.

## Pitfalls

- Do not give reviewers the evaluation report or context brief. They must be blind.
- Do not average dissenting opinions into consensus. Record and address them.
- Do not let the methodology reviewer's fatal flaw be overridden by other reviewers' enthusiasm.
- Do not skip the submission-guard reviewer in any tier. Journal compliance is always checked.
- Do not draft responses to panel concerns within the panel report.

## Verification

- Panel mode and tier explicitly documented
- Every reviewer role ran in a distinct fresh independent subagent or delegated thread
- Every reviewer received only their designated inputs
- All required reviewers completed before aggregation
- Aggregation follows non-compensatory rules
- Dissenting opinions recorded with reviewer identity
- Route decision matches the most severe non-compensatory finding

## References

- `references/reviewer-role-definitions.md`: Detailed role descriptions, evaluation criteria, and output formats for each reviewer role.
- `references/panel-aggregation-guide.md`: Aggregation logic, dissent handling, and recommendation level mapping.
- `article-orchestrator/references/artifact-contracts.md`: Canonical panel report and reviewer brief schemas.
- `article-orchestrator/references/delegate-brief-templates.md`: Subagent brief templates for each reviewer role.
- `article-orchestrator/references/delegation-rules-pattern.md`: Concurrent delegation and isolation pattern.
