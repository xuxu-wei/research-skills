# Loop Control and Stop Rules

Revision loop limits, targeted repair rules, independent re-evaluation, and stop conditions for `article-refinement-controller` and `article-orchestrator`.

## Revision Round Limits

- Default maximum: 2 substantive revision rounds.
- Language polishing does not consume a revision round.
- Reporting completion that only adds checklist mappings does not consume a revision round.
- Evidence relinking without manuscript text changes does not consume a revision round.
- If a third round is needed, record `major_revision_required` and stop for author intervention.

## Targeted Repair Rules

### When the Evaluator Returns `revise`

1. `article-refinement-controller` classifies the revision mode using `artifact-contracts.md`.
2. Stop immediately for `analysis_required` or `study_redesign_required`; do not attempt text-only fixes.
3. For other modes, create the revision plan with an entry strategy for every item: `enter_manuscript`, `response_only`, or `decline`.
4. Route `article-drafter` in revision mode.
5. Produce the three required revision files in `09_revisions/round-NNN/`.
6. Return to the orchestrator, which delegates a fresh `article-evaluator` instance without prior scores or decisions.

### When the Claim Auditor Returns `downscale_and_proceed`

1. Route to refinement with primary mode `claim_downscaling`.
2. Require author confirmation before advancing a manuscript with downscaled primary claims.

### When Language Hard Gates Fail

1. Route to refinement with primary mode `language_polishing`.
2. Delegate `academic-language-assessor` in standalone-preflight mode to a fresh independent subagent.
3. Let `article-drafter` fix only the identified language issues; substance must not change.
4. Generate `language_change_log`.
5. Delegate re-assessment to another fresh `academic-language-assessor` instance without the prior score or decision.
6. If either independent assessor cannot run, return `independent_review_pending` with a continuation brief and stop; never assess inline.

## Stop Conditions

| Condition | Trigger | Action |
|-----------|---------|--------|
| Readiness blocked | `readiness_status = not_ready` | Return blocking gaps and required actions |
| Methods blocked | `audit_status` is `requires_reanalysis` or `methodologically_blocked` | Return audit and required external action |
| Fatal overclaims | Claim-audit recommendation is `blocked` | Return claim audit; repair and re-audit or stop |
| Fatal flaws | Evaluation decision is `reject` | Return evaluation and document unfixable flaws |
| No gain | Orchestrator comparison of sealed evaluation reports and revision delta finds no substantive improvement | Return evidence of no improvement and set `stop_no_gain` |
| Max rounds reached | Revision round exceeds the maximum | Stop and mark `major_revision_required` |
| Panel rejects | Aggregated recommendation is `reject_or_redesign` | Stop and return to study design |
| Independent review unavailable | Any required reviewer cannot run in a fresh independent context | Return `independent_review_pending` and a continuation brief |

## Re-Evaluation Rules

After each revision round:

1. Create a new independent evaluator instance; never reuse the prior evaluator context.
2. Give it only the latest frozen draft, stable rubric, necessary factual artifacts, and—if required—an anonymized must-fix list plus revision delta. Do not provide prior scores or decisions.
3. Seal the new report before any cross-round comparison.
4. The orchestrator compares the current and prior sealed reports with the revision delta, performs the Thesis Integrity check, and decides whether the result improved, requires another permitted revision, or is `stop_no_gain`.
5. If the core claim became less clear, route to `revise` with a subtractive repair direction.
6. If a fresh evaluator cannot run, return `independent_review_pending` with a continuation brief and stop. Never re-evaluate inline.

## Delta Report Quality Gate

Before routing to re-evaluation, verify that:

- The delta is not empty and does not contain only vague claims such as "polished expression" or "improved clarity."
- Every evaluator concern is marked `addressed`, `partially_addressed`, or `not_addressed_with_reason`.
- An insufficient delta returns to `article-refinement-controller` for completion before re-evaluation.
