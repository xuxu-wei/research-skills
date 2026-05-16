---
name: article-review-panel
description: Simulate a multi-role peer review panel using isolated subagents. Produce an aggregated panel report with non-compensatory aggregation rules that prevent averaging away fatal flaws.
version: 0.1.0
author: Xuxu Wei
license: MIT
metadata:
  hermes:
    tags: [research-article, review, panel, peer-review, simulation, blind]
    related_skills:
      - article-orchestrator
      - article-evaluator
      - article-refinement-controller
---

# article-review-panel

## Purpose

Simulate a multi-role peer review panel to pressure-test the manuscript from diverse reviewer perspectives before real submission. Produce an aggregated panel report that predicts what real reviewers will flag.

This skill does NOT evaluate the manuscript as a single evaluator (that is `article-evaluator`'s job), rewrite text, or draft responses. It simulates external review.

## Core Rules

- Default mode: `blind_external_simulation`. Reviewers receive only the manuscript (no context brief, no evaluation report, no unresolved issues).
- Every reviewer is an isolated subagent dispatched concurrently via `delegate_task`.
- Non-compensatory aggregation: a fatal flaw from the methodology reviewer caps the aggregated recommendation at `not_ready`.
- Dissenting opinions must be recorded and addressed, not averaged away.
- Reviewers evaluate only. They must not draft, revise, rewrite, or broaden scope.
- Panel tiers: `lightweight` (3 reviewers), `standard` (5), `full` (7).

## I/O Contract

```yaml
io_contract:
  allowed_inputs:
    - manuscript_draft
    - article_blueprint (journal_adapter only, for submission-guard reviewer)
  required_outputs:
    - panel_report (aggregated)
    - reviewer_briefs (individual)
  may_read:
    - "06_drafts/**"
  may_write:
    - "10_panel/panel-report.md"
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
    - "delegate_task unavailable → run reviewers inline with strict isolation instructions"
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
- Manuscript version and path
- Explicit prohibited actions (do not draft, revise, rewrite)
- Output format (structured review with recommendation)

Reviewers receive only the manuscript. Do not include context brief, evaluation report, claim audit, or unresolved issues.

## Aggregation Rules

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

- `10_panel/panel-report.md`: Aggregated report with panel composition, mode, tier, individual recommendations, aggregation result, dissenting opinions, and route decision.
- `10_panel/reviewer-briefs/`: Individual reviewer reports.

## Pitfalls

- Do not give reviewers the evaluation report or context brief. They must be blind.
- Do not average dissenting opinions into consensus. Record and address them.
- Do not let the methodology reviewer's fatal flaw be overridden by other reviewers' enthusiasm.
- Do not skip the submission-guard reviewer in any tier. Journal compliance is always checked.
- Do not draft responses to panel concerns within the panel report.

## Verification

- Panel mode and tier explicitly documented
- Every reviewer dispatched as an isolated subagent
- Every reviewer received only their designated inputs
- Aggregation follows non-compensatory rules
- Dissenting opinions recorded with reviewer identity
- Route decision matches the most severe non-compensatory finding

## References

- `references/reviewer-role-definitions.md`: Detailed role descriptions, evaluation criteria, and output formats for each reviewer role.
- `references/panel-aggregation-guide.md`: Aggregation logic, dissent handling, and recommendation level mapping.
- `article-orchestrator/references/artifact-contracts.md`: Canonical panel report and reviewer brief schemas.
- `article-orchestrator/references/delegate-brief-templates.md`: Subagent brief templates for each reviewer role.
- `article-orchestrator/references/delegation-rules-pattern.md`: Concurrent delegation and isolation pattern.
