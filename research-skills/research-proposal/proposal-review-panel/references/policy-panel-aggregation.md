# Panel Aggregation Policy

## Purpose

Convert individual reviewer reports into a panel-level summary without erasing important dissent.

## Aggregation Rules

Panel summary must distinguish:
- consensus strengths;
- consensus weaknesses;
- reviewer disagreements;
- skeptical objections;
- must-fix items;
- optional improvements;
- unresolved risks;
- likely reviewer attack points;
- final recommendation.

## Recommendation Labels

Use one of:
- `strong_support`
- `support_with_minor_revision`
- `support_after_major_revision`
- `revise_and_resubmit`
- `not_ready`
- `reject_or_redesign`

## Handling Disagreement

- Do not suppress minority criticism.
- If one reviewer identifies a credible fatal flaw, flag it even if others are positive.
- Separate broad enthusiasm from technical acceptability.
- If methodology/statistics reviewer raises a severe concern, escalate it as high priority.
- If skeptical reviewer raises a plausible attack point, include it in panel risks.

## Must-Fix Criteria

Classify an issue as must-fix when it threatens:
- answerability of the research question;
- credibility of novelty claim;
- feasibility of research plan;
- alignment between aims and methods;
- reviewer defensibility;
- submission readiness.
