# Panel Aggregation Format — Consolidated Must-Fix Items

## Purpose

This reference defines the 4-category format for grouping reviewer must-fix items into consolidated, deduplicated, actionable items in the panel summary report.

## Four Categories

When aggregating individual reviewer reports into a panel summary, group all must-fix items into four categories:

### Category A: Methodological Design
Items related to study design, simulation parameters, statistical rigor, endpoint specification, and analytical plan.
- Examples: MC replication levels, ordering protocol, coverage criteria, comparator selection, excitation factor operationalization.

### Category B: Domain Positioning & Literature
Items related to literature engagement, novelty claim precision, benchmark selection, and domain-standard alignment.
- Examples: reference list adequacy, "first" claim qualification, TSA category mismatch, engagement with existing finite-sample methods.

### Category C: Framing & Conceptual Architecture
Items related to proposal narrative, terminology, scope claims, and conceptual overreach.
- Examples: "新范式" vs "新数学表述", SCM formalism invocation, cross-disciplinary claim justification.

### Category D: Translation & Adoption
Items related to end-user pathway, software usability, stakeholder engagement, and real-world implementation.
- Examples: adoption pathway, R package documentation, GRADE integration, training strategy, gatekeeper engagement.

## Format for Each Consolidated MF Item

```
**MF-N. Short title**
(Source reviewers + Severity)

Brief functional description of the issue, its consequence, and why it is actionable.

**Fix**: Concrete action + location in proposal where it should be applied.
```

## Deduplication

When multiple reviewers raise the same issue in different language:
- Merge into one consolidated MF item.
- List all source reviewers.
- Take the highest severity assessment across sources.

## Must-Fix vs Optional

- Must-Fix: any credible finding that threatens answerability, scientific validity, feasibility, binding requirements, or reviewer defensibility. A single well-supported severe finding is sufficient; reviewer counts do not determine severity.
- Optional: a preference or local improvement whose omission does not threaten the proposal's logic, validity, feasibility, or binding requirements.

Any credible FATAL/blocking item sets `supportive_recommendation_allowed: false`. It cannot be deduplicated, averaged, or relabeled into a minor issue.
