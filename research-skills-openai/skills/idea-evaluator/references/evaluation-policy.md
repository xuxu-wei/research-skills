# Evaluation Policy

This file consolidates scoring, hard gates, decision rules, and fatal flaw handling for `idea-evaluator`.

## Scoring Scale

Use 1-5 scores for each dimension.

- 1: severe failure.
- 2: weak or poorly supported.
- 3: minimally acceptable.
- 4: strong.
- 5: exceptional.

## Dimensions

- Novelty.
- Feasibility.
- Impact.
- Relevance.
- Clarity.
- Completion.

Overall score is the simple average of the six dimensions. Do not use weighted averages.

## Evidence-Limited Scoring

- Missing or unverified evidence blocks high novelty claims.
- Clinical or guideline-alignment claims require current web evidence or user-provided evidence.
- Unsupported claims must be downgraded or marked `unverified`.

## Hard Gates

Hard gates block `promote` even when the overall score is acceptable.

- Feasibility minimum: 3.0.
- Relevance minimum: 3.0.
- Clarity minimum: 3.0.
- Completion minimum: 3.0.

An idea that fails any hard gate cannot receive `promote`. It may receive `revise_then_promote`, `revise`, `reframe`, `merge`, `keep_as_backup`, or `reject`.

## Decision Rules

- `promote`: strong idea, all hard gates pass, no fatal flaw.
- `revise_then_promote`: nearly ready, all gates pass or only minor repair is needed.
- `revise`: fixable weakness within the same framing.
- `reframe`: core framing is weak but the underlying opportunity may be salvageable.
- `merge`: overlaps with another idea and should be combined.
- `keep_as_backup`: not top-tier but useful as fallback.
- `reject`: unfixable weakness, fatal flaw, or poor fit.

Threshold guidance:

- Overall >= 4.2 and all gates pass: consider `promote`.
- Overall 3.6-4.1 and all gates pass: consider `revise_then_promote`.
- Overall 3.0-3.5 or fixable gate issue: consider `revise`, `reframe`, or `merge`.
- Overall 2.5-2.9: consider `keep_as_backup` or major reframe.
- Overall < 2.5 or unfixable fatal flaw: reject.

## Fatal Flaws

Fatal flaws override numerical score.

Examples:

- no plausible data source;
- endpoint or metric cannot be defined;
- method cannot answer the research question;
- core claim contradicts available evidence;
- clinical claim lacks evidence and cannot be verified;
- relevance to user goal is absent;
- idea is essentially duplicate and adds no distinct value.

If a fatal flaw is fixable, recommend repair. If unfixable, recommend reject.
