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
- A credible `FATAL` or blocking finding is non-compensatory: the panel recommendation cannot be `strong_support` or `support_with_minor_revision`. Route to `support_after_major_revision`, `revise_and_resubmit`, `not_ready`, or `reject_or_redesign` according to fixability.
- An unfixable fatal flaw requires `reject_or_redesign`; a fatal flaw that cannot be resolved with the available artifacts requires `not_ready`.
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
