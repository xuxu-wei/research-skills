# Loop Control and Stop Rules

Revision loop limits, targeted repair rules, independent re-evaluation, and stop conditions for `article-refinement-controller` and `article-orchestrator`.

## Revision Round Limits

- Default maximum: 2 substantive revision rounds.
- One concentrated editorial repair does not consume a substantive revision round.
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
6. Return through content preservation and fresh narrative/language readiness before the orchestrator delegates a fresh final `article-evaluator` instance without prior scores or decisions.

### When the Claim Auditor Returns `downscale_and_proceed`

1. Route to refinement with primary mode `claim_downscaling`.
2. Require author confirmation before advancing a manuscript with downscaled primary claims.

### When Editorial Readiness Fails

1. Freeze `protected-content-register.yaml` before changing prose.
2. Run fresh `research-narrative-assessor` and `academic-language-assessor` instances in parallel against the same reader-facing bundle.
3. Normalize all included critical/major actions into one validated `editorial-repair-brief-rNNN.yaml`; resolve overlap or conflict before routing.
4. Let the existing body and frontmatter owners execute only their assigned brief actions. They do not read raw reports. Use bounded section passes only when needed for attention control and retain one complete artifact per owner.
5. Validate action conformance, then delegate an independent content-preservation check and fresh narrative/language reassessment.
6. Missing major action returns to the same writer before freeze. A localized minor miss that does not change science, readiness, decision, or broad output is recorded in the maintained test observation report without opening a new reproduction/fix loop.
7. If either independent reviewer cannot run, return `independent_review_pending` with a continuation brief and stop; never assess inline.
8. Do not infer context overload from a miss. Diagnose `context_attention` only after excluding input, assessor coverage, and brief normalization, and only when the same writer misses an action with the complete allowed context but succeeds with a bounded view.

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
2. Give it only the latest complete frozen manuscript/frontmatter, current display assets, stable rubric, and minimal factual/outlet constraints. Do not provide prior artifacts, context/blueprint plans, audits, narrative/language reports, repair briefs, protected registers, preservation reports, deltas, scores, decisions, or anonymized must-fix lists.
3. Seal the new report before any cross-round comparison.
4. After the fresh report returns, the orchestrator compares sealed reports with the separately held delta, performs the Thesis Integrity check, and decides improvement, another permitted revision, or `stop_no_gain`.
5. If the core claim became less clear, route to `revise` with a subtractive repair direction.
6. If a fresh evaluator cannot run, return `independent_review_pending` with a continuation brief and stop. Never re-evaluate inline.

## Delta Report Quality Gate

Before routing to re-evaluation, verify that:

- The delta is not empty and does not contain only vague claims such as "polished expression" or "improved clarity."
- The revised manuscript/frontmatter bundle is complete, its artifact IDs/versions/paths are registered under unique current pointers, content preservation passed, fresh editorial readiness passed, and its identity anchor is preserved; otherwise stop or route back before evaluation.
- Every evaluator concern is marked `addressed`, `partially_addressed`, or `not_addressed_with_reason`.
- An insufficient delta returns to `article-refinement-controller` for completion before re-evaluation.
